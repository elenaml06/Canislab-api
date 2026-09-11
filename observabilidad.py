"""
Rawku - Observabilidad (Sentry)

Captura automaticamente los errores del backend (los 500 de /menu/v2,
/analizar, /menu/semana...) y los manda a Sentry, para poder verlos con
traza completa en vez de tener que ir a rebuscar en los logs de Render,
que se pierden cuando el servicio reinicia.

Que hace falta para que funcione en produccion:
    1. Crear un proyecto gratuito en https://sentry.io (plataforma: FastAPI)
    2. Copiar el DSN que da Sentry
    3. En Render -> el servicio de la API -> Environment, anadir:
           SENTRY_DSN = https://....ingest.sentry.io/....
    4. Guardar (Render redespliega solo)

Sin SENTRY_DSN NO pasa nada malo: iniciar_sentry() no hace nada y la API
arranca exactamente igual que antes. Eso es a proposito, para que en
local y en los tests no haga falta configurar nada ni se manden errores
de pruebas al panel de produccion.

Variables opcionales (todas tienen un valor por defecto razonable):
    SENTRY_ENVIRONMENT        "production" en Render, "local" fuera. Sirve
                              para separar en el panel los errores reales
                              de los de desarrollo.
    SENTRY_RELEASE            version desplegada. Por defecto usa el commit
                              que Render expone en RENDER_GIT_COMMIT, asi
                              cada error queda atado al codigo exacto.
    SENTRY_TRACES_SAMPLE_RATE porcentaje de peticiones con traza de
                              rendimiento (0.0 = ninguna). Por defecto 0.0:
                              el plan gratuito tiene pocas transacciones al
                              mes y lo que interesa aqui son los ERRORES,
                              que no consumen esa cuota.
    SENTRY_SAMPLE_RATE        porcentaje de errores que se mandan (1.0 =
                              todos). Solo tocar si algun dia el plan
                              gratuito se queda corto de eventos.
    SENTRY_PRUEBA             "1" para habilitar el endpoint /sentry/prueba,
                              que provoca un error a proposito para
                              comprobar que los errores llegan al panel.
"""
import os
import re

# Se pone a True solo si sentry_sdk.init() ha llegado a ejecutarse de
# verdad. Todas las funciones de este modulo lo consultan antes de hacer
# nada, para que llamarlas sin Sentry configurado sea gratis y seguro.
_ACTIVO = False

# Rutas cuyo CUERPO de peticion nunca debe salir del servidor: /stripe/*
# recibe email del usuario, user_id y el id de cliente de Stripe.
#
# ⚠️ EL RESTO DE ENDPOINTS NO ESTAN LIMPIOS POR SER DE PERRO (11
# septiembre). Durante un tiempo este comentario decia que los demas
# "solo manejan datos del perro -- peso, etapa, alimentos", y dejo de ser
# cierto el 29 de agosto, cuando /menu/* y /formular/* empezaron a recibir
# `token_usuario`, que es la sesion de Supabase de quien pide el menu. Lo
# que los mantiene limpios no es su contenido: es el tachado por nombre de
# clave y por forma (ver CLAVES_SENSIBLES, _JWT). Si algun dia un endpoint
# de estos recibe algo que ninguna de las dos cosas sepa reconocer, su ruta
# tiene que entrar aqui.
RUTAS_SIN_CUERPO = ("/stripe",)

# Trozos de nombre de clave que se borran de cualquier sitio del evento,
# aunque lleguen por una via que no habiamos previsto.
#
# ⚠️ SON TROZOS, NO NOMBRES ENTEROS (11 septiembre) — CASO REAL, y el
# agujero estuvo abierto desde el 29 de agosto. Esto se comparaba con
# `k.lower() in CLAVES_SENSIBLES`, o sea IGUALDAD EXACTA. La lista tenia
# "token"... y el campo por el que viaja la sesion de Supabase se llama
# `token_usuario`. No es "token", asi que no se tachaba.
#
# Y el cuerpo de la peticion solo se borra entero en las rutas de /stripe
# (ver RUTAS_SIN_CUERPO), asi que cualquier error en /menu/v2,
# /menu/cambiar, /menu/varios-perros o /formular/autocompletar mandaba a
# Sentry el JWT de sesion de quien pedia el menu, vivo y entero. Con ese
# token se es esa persona ante Supabase hasta que caduca.
#
# Comparar por trozo tacha de mas, y eso es justo lo que se quiere: el
# coste de borrar un campo que no hacia falta es no poder reproducir un
# fallo; el de dejar pasar uno que si, es una credencial en un panel de
# terceros.
CLAVES_SENSIBLES = (
    "email", "user_id", "customer", "signature", "authorization",
    "cookie", "apikey", "api_key", "token", "password", "secret",
    "clave", "jwt", "bearer",
)

# Cualquier cosa con forma de email se tacha, este donde este dentro del
# evento -- incluidas las variables locales que Sentry adjunta a la traza.
_EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

# ⚠️ Y CUALQUIER COSA CON FORMA DE JWT (11 septiembre). Borrar por nombre
# de clave no basta: Sentry adjunta las VARIABLES LOCALES de cada linea de
# la traza, y ahi el token no viaja como campo sino dentro de un texto ya
# montado, tipo
#     datos = PeticionMenu(token_usuario='eyJhbGciOi...', peso_perro_kg=20.0)
# Eso es un string, no un dict, y ninguna limpieza por clave puede verlo.
# Un JWT son tres trozos de base64url separados por puntos, y el primero
# empieza siempre por "eyJ" ({" en base64). Se tacha este donde este.
_JWT = re.compile(r"eyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]+")

# Las claves de servicio del formato nuevo de Supabase y las de Stripe no
# son JWT y no llevan puntos: se reconocen por el prefijo.
_CLAVES_CON_PREFIJO = re.compile(
    r"\b(?:sb_secret_|sb_publishable_|sk_live_|sk_test_|rk_live_|rk_test_|whsec_)"
    r"[A-Za-z0-9_-]{6,}")


def _es_clave_sensible(clave):
    """True si el NOMBRE del campo dice que su valor no puede salir de aqui."""
    if not isinstance(clave, str):
        return False
    bajo = clave.lower()
    return any(trozo in bajo for trozo in CLAVES_SENSIBLES)


def _tasa(nombre, por_defecto):
    """Lee una variable de entorno como porcentaje 0.0-1.0 sin reventar."""
    try:
        valor = float(os.environ.get(nombre) or por_defecto)
    except (TypeError, ValueError):
        valor = float(por_defecto)
    return max(0.0, min(1.0, valor))


def _limpiar_datos(valor, profundidad=0):
    """
    Recorre dicts/listas anidados del evento haciendo dos cosas:
      - vaciar las claves de CLAVES_SENSIBLES vengan de donde vengan
      - tachar cualquier cosa con forma de email dentro de un texto

    Lo segundo hace falta porque Sentry adjunta las VARIABLES LOCALES de
    cada linea de la traza, y ahi el email no viaja como campo "email"
    sino dentro de un texto ya montado, tipo
        datos = PeticionCheckout(user_id='...', email='elena@...')
    -- que ninguna limpieza por nombre de clave puede pillar.
    """
    if profundidad > 12:
        return valor
    if isinstance(valor, dict):
        limpio = {}
        for k, v in valor.items():
            if _es_clave_sensible(k):
                limpio[k] = "[borrado]"
            else:
                limpio[k] = _limpiar_datos(v, profundidad + 1)
        return limpio
    if isinstance(valor, (list, tuple)):
        return [_limpiar_datos(v, profundidad + 1) for v in valor]
    if isinstance(valor, str):
        limpio = _EMAIL.sub("[email borrado]", valor)
        limpio = _JWT.sub("[token borrado]", limpio)
        return _CLAVES_CON_PREFIJO.sub("[clave borrada]", limpio)
    return valor


def _quitar_variables_locales(evento):
    """
    Borra las variables locales de TODAS las lineas de la traza.

    Se usa solo en las rutas de /stripe: ahi las locales llevan el email,
    el user_id y el objeto entero que se le manda a Stripe, y no hay forma
    fiable de distinguir por nombre lo que se puede enviar de lo que no.
    En el resto de endpoints las locales se conservan, porque son
    justamente lo que permite entender por que ha fallado el motor.
    """
    for excepcion in (evento.get("exception") or {}).get("values") or []:
        for linea in (excepcion.get("stacktrace") or {}).get("frames") or []:
            linea.pop("vars", None)
    for hilo in (evento.get("threads") or {}).get("values") or []:
        for linea in (hilo.get("stacktrace") or {}).get("frames") or []:
            linea.pop("vars", None)


def _limpiar(evento, pista):
    """
    Ultimo filtro antes de mandar nada a Sentry. send_default_pii=False ya
    evita cabeceras e IP, pero el cuerpo de la peticion y las variables
    locales de la traza SI se adjuntan (y son justo lo que hace falta para
    reproducir un menu que ha fallado), asi que aqui se quita a mano lo
    que no debe salir de este servidor.
    """
    try:
        peticion = evento.get("request") or {}
        # de "https://canislab-api.onrender.com/stripe/checkout" -> "/stripe/checkout"
        url = peticion.get("url") or ""
        ruta = "/" + url.split("://", 1)[-1].partition("/")[2] if url else ""
        if any(ruta.startswith(prefijo) for prefijo in RUTAS_SIN_CUERPO):
            peticion.pop("data", None)
            evento["request"] = peticion
            _quitar_variables_locales(evento)
        return _limpiar_datos(evento)
    except Exception:
        # Un fallo limpiando NUNCA debe tumbar la peticion del usuario ni
        # dejar pasar un evento sin limpiar: si algo va mal, no se manda.
        return None


def iniciar_sentry():
    """
    Arranca Sentry si hay DSN configurado. Devuelve True/False segun si ha
    quedado activo, para poder decirlo en /verificar y no tener que
    adivinarlo desde fuera.

    Se llama lo ANTES posible en main.py -- antes de crear el FastAPI() --
    porque la integracion de Sentry instrumenta Starlette/FastAPI en el
    momento del init: si se hiciera despues, la app ya creada no quedaria
    cubierta y los errores de los endpoints no llegarian al panel.
    """
    global _ACTIVO
    dsn = (os.environ.get("SENTRY_DSN") or "").strip()
    if not dsn:
        print("[sentry] SENTRY_DSN no configurado -- errores solo en los logs de Render")
        return False

    try:
        import sentry_sdk
        from sentry_sdk.integrations.fastapi import FastApiIntegration
        from sentry_sdk.integrations.starlette import StarletteIntegration
    except ImportError:
        # requirements.txt lo incluye, pero si algun dia se despliega sin
        # instalar dependencias, mejor arrancar la API sin Sentry que no
        # arrancarla en absoluto.
        print("[sentry] sentry-sdk no instalado -- la API sigue funcionando sin el")
        return False

    en_render = bool(os.environ.get("RENDER") or os.environ.get("RENDER_SERVICE_ID"))
    sentry_sdk.init(
        dsn=dsn,
        environment=os.environ.get("SENTRY_ENVIRONMENT") or ("production" if en_render else "local"),
        release=os.environ.get("SENTRY_RELEASE") or os.environ.get("RENDER_GIT_COMMIT") or None,
        integrations=[StarletteIntegration(), FastApiIntegration()],
        # Los errores no gastan cuota de transacciones; las trazas de
        # rendimiento si, y el plan gratuito da pocas. Por eso 0.0 por
        # defecto y se sube con la variable de entorno si algun dia hace
        # falta medir cuanto tarda el solver.
        traces_sample_rate=_tasa("SENTRY_TRACES_SAMPLE_RATE", 0.0),
        sample_rate=_tasa("SENTRY_SAMPLE_RATE", 1.0),
        # NADA de datos personales automaticos (IP, cabeceras, cookies).
        send_default_pii=False,
        # El cuerpo de la peticion SI, recortado: sin el no hay forma de
        # reproducir que menu concreto ha fallado. _limpiar() lo quita
        # entero en las rutas de Stripe.
        max_request_body_size="small",
        before_send=_limpiar,
    )
    sentry_sdk.set_tag("componente", "canislab-api")
    _ACTIVO = True
    print("[sentry] activo (entorno: %s)" % (
        os.environ.get("SENTRY_ENVIRONMENT") or ("production" if en_render else "local")))
    return True


def activo():
    """Para poder informarlo en /verificar sin importar sentry_sdk fuera."""
    return _ACTIVO


def capturar(exc, **contexto):
    """
    Manda a Sentry una excepcion que el codigo YA ha capturado.

    Hace falta explicitamente porque varios endpoints (/menu/v2,
    /menu/semana, /stripe/*) envuelven todo en un try/except a proposito,
    para devolverle siempre JSON valido al frontend en vez de un 500 --
    eso es correcto de cara al usuario, pero significa que la excepcion
    nunca llega a salir de la app, y por tanto Sentry NO la ve por su
    cuenta. Sin esta llamada, justo los fallos mas importantes serian los
    unicos invisibles en el panel.

    contexto: pares clave=valor con datos del perro/peticion (etapa, peso,
    numero de alimentos...) que aparecen junto al error para poder
    reproducirlo. No meter aqui nada personal.
    """
    if not _ACTIVO:
        return None
    try:
        import sentry_sdk
        with sentry_sdk.new_scope() as scope:
            if contexto:
                scope.set_context("peticion_rawku", _limpiar_datos(contexto))
            return sentry_sdk.capture_exception(exc)
    except Exception:
        # Que la telemetria falle jamas puede romper la respuesta al usuario.
        return None


def etiquetar(**etiquetas):
    """Etiquetas del evento en curso (endpoint, etapa...) para filtrar en el panel."""
    if not _ACTIVO:
        return
    try:
        import sentry_sdk
        for clave, valor in etiquetas.items():
            if valor is not None:
                sentry_sdk.set_tag(clave, str(valor)[:200])
    except Exception:
        pass
