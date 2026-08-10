"""
CANISLAB - API real del motor nutricional

Envuelve todo el codigo Python YA VALIDADO (especies.py, der.py,
optimizador.py, transicion.py, persistencia.py, y desde el 5 de agosto
motor/motor_completo.py como motor de generación real) como un servicio
web de verdad, para que la app pueda consultarlo por internet en vez de
simular nada.

Para probarlo en local:
    pip install fastapi uvicorn --break-system-packages
    uvicorn main:app --reload
    -> abre http://localhost:8000/docs para probarlo interactivamente

Para desplegarlo de verdad (gratis o muy barato), opciones sencillas:
    - Render.com (capa gratuita, sube el codigo y listo)
    - Railway.app (capa gratuita generosa)
    - Fly.io (capa gratuita)
Cualquiera de las tres funciona con este mismo archivo sin cambios.
"""
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from typing import Optional

import sys
import time
sys.path.insert(0, ".")
sys.path.insert(0, "./motor")
from especies import cargar_alimentos, filtrar_alimentos_disponibles
from der import calcular_der
from optimizador import ETAPAS_VALIDAS
from optimizador import optimizar_menu, dosis_maxima_fabricante
from transicion import calcular_tramo_transicion, menu_activo_y_bloqueados, nivel_indicador_nutrientes
from analizador import analizar_dieta
import persistencia

# ⚠️ EL MOTOR NUEVO (5 agosto) — programación lineal entera mixta, decide
# QUÉ alimentos usar Y cuánto de cada uno a la vez, comprobado contra los
# 30 requisitos de FEDIAF de forma EXACTA (no heurística). Vive en
# ./motor/ y NO sustituye a /menu todavía: se añade como /menu/v2 para
# poder comparar los dos antes de decidir el cambio definitivo.
from motor_completo import resolver as resolver_v2
from constructor import cargar as cargar_v2, MARGENES as MARGENES_V2
from verificar import verificar as verificar_v2
from seguridad import revisar_seguridad as revisar_seguridad_v2

app = FastAPI(title="CANISLAB API")

# permite que la app (en el navegador) pueda llamar a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en produccion, poner aqui el dominio real de la app
    allow_methods=["*"],
    allow_headers=["*"],
)

persistencia.crear_tablas()


# ---------- modelos de entrada ----------
class PeticionDER(BaseModel):
    # Datos del método europeo. Todos OPCIONALES: sin ellos el cálculo
    # sigue funcionando con valores prudentes.
    peso_adulto_esperado_kg: float = None
    peso_ideal_kg: float = None
    convivencia: str = "solo"
    macho_entero: bool = False
    raza: str = None
    semana_gestacion: int = None
    n_cachorros: int = None
    semana_lactancia: int = 3
    peso_actual_kg: float
    etapa: str
    actividad_idx: int  # 0=sedentario .. 4=trabajo
    esterilizado: bool


class PeticionMenu(BaseModel):
    peso_perro_kg: float = None
    # peso ADULTO esperado: activa el tope de calcio de raza grande en cachorros
    peso_adulto_esperado_kg: float = None
    nombres_excluidos: list = None
    patologias: list = None
    # ⚠️ AÑADIDO (5 agosto): "Toy"/"Mini"/"Pequeño"/"Mediano"/"Grande"/
    # "Gigante" -- para poder intentar primero la vía rápida del catálogo
    # fijo (mismo tamaño y etapa) antes de la búsqueda libre completa.
    tamano: str = None
    # Lo que el usuario ha elegido A MANO en Personalizar o Aprovechar. Sin
    # esto, el optimizador podia ponerlo a 0 gramos y el usuario veia que su
    # eleccion desaparecia del menu sin explicacion.
    forzar_presencia: list = None
    nombres_alimentos: list[str]
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []
    # ⚠️ AÑADIDO (5 agosto, noche): "Todo el/la {especie}" en
    # personalizar/aprovechar -- {categoria: especie}. Restringe esa
    # categoría a solo esa especie, dejando que el motor elija
    # libremente qué corte/pieza usar dentro de ella.
    restringir_especie: dict = None
    # ⚠️ AÑADIDO para /menu/v2 (5 agosto): el frontend dice explícitamente
    # qué modo quiere, en vez de que el backend tenga que adivinarlo por
    # lo que manda en nombres_alimentos/forzar_presencia.
    #   "automatico"   -> el motor elige libre, ignora las dos listas
    #   "personalizar" -> los alimentos de forzar_presencia (o si viene
    #                     vacío, los de nombres_alimentos) SÍ O SÍ entran
    #   "aprovechar"   -> los de nombres_alimentos se PRIORIZAN, pero el
    #                     motor puede añadir más si hace falta para cerrar
    modo: str = "automatico"


class PeticionCambiarAlimento(BaseModel):
    peso_perro_kg: float = None
    nombres_excluidos: list = None
    patologias: list = None
    menu_actual: list[str]
    alimento_viejo: str
    alimento_nuevo: str
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []


class PeticionAnadirQuitarAlimento(BaseModel):
    peso_perro_kg: float = None
    nombres_excluidos: list = None
    patologias: list = None
    menu_actual: list[str]
    alimento: str
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []


class PeticionTransicion(BaseModel):
    fecha_inicio: str  # "2026-07-25"
    num_menus_elegidos: int
    fecha_hoy: Optional[str] = None


# ---------- endpoints ----------

@app.post("/der")
def endpoint_der(datos: PeticionDER):
    ACTIVIDAD_KEY = ["sedentario", "normal", "activo", "muy_activo", "trabajo"]
    actividad = ACTIVIDAD_KEY[datos.actividad_idx] if datos.etapa in ("adulto", "senior") else None
    resultado = calcular_der(
        datos.peso_actual_kg, datos.etapa, actividad, datos.esterilizado,
        peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
        peso_ideal_kg=datos.peso_ideal_kg,
        convivencia=datos.convivencia,
        macho_entero=datos.macho_entero,
        raza=datos.raza,
        semana_gestacion=datos.semana_gestacion,
        n_cachorros=datos.n_cachorros,
        semana_lactancia=datos.semana_lactancia)
    return resultado


@app.post("/menu")
def endpoint_menu(datos: PeticionMenu):
    alimentos = cargar_alimentos()
    # Se filtra SIEMPRE, aunque no haya especies excluidas: los alimentos
    # concretos que el usuario marco para evitar tambien tienen que caer.
    alimentos = filtrar_alimentos_disponibles(
        alimentos, set(datos.especies_excluidas or []), set(datos.nombres_excluidos or []))
    por_nombre = {a["nombre"]: a for a in alimentos}
    candidatos = [por_nombre[n] for n in datos.nombres_alimentos if n in por_nombre]
    if not candidatos:
        raise HTTPException(400, "Ninguno de los alimentos indicados existe en la base de datos")
    resultado = optimizar_menu(candidatos, datos.der_objetivo, datos.etapa_requisitos,
                               forzar_presencia=datos.forzar_presencia,
                               peso_perro_kg=datos.peso_perro_kg,
                               patologias=datos.patologias,
                               peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg)
    # Si forzar lo que el usuario eligio deja el menu sin solucion, se
    # reintenta sin forzar: mejor darle un menu (avisando) que un error.
    if not resultado.get("factible") and datos.forzar_presencia:
        resultado = optimizar_menu(candidatos, datos.der_objetivo, datos.etapa_requisitos,
                                   peso_perro_kg=datos.peso_perro_kg,
                                   patologias=datos.patologias)
        if resultado.get("factible"):
            resultado["no_se_pudo_forzar"] = True
    return resultado


@app.get("/catalogo/{tamano}/{etapa}")
def endpoint_catalogo(tamano: str, etapa: str, der_objetivo: float = None, peso_perro_kg: float = None):
    """
    Devuelve al instante (sin resolver nada) el menú del catálogo fijo más
    cercano a este tamaño y etapa — para enseñarlo como vista previa
    aproximada mientras /menu/v2 calcula el menú exacto del perro real.
    ⚠️ Esto NO es el menú del perro: usa un peso representativo del grupo,
    no su peso exacto. El frontend tiene que dejarlo claro en pantalla.

    ⚠️ CORREGIDO (5 agosto): si se dan der_objetivo y peso_perro_kg, el
    reescalado a las kcal reales SE HACE AQUÍ, no en el frontend -- porque
    los suplementos comerciales NO se pueden reescalar por kcal sin más.
    Su dosis máxima la marca el fabricante por el PESO del perro, no por
    sus calorías, y las dos proporciones no tienen por qué coincidir. Se
    escala el resto de alimentos por kcal (ahí sí es correcto, porque los
    requisitos de FEDIAF se miden por cada 1000 kcal), pero cada
    suplemento se topa aparte en su dosis máxima real, calculada con el
    peso de verdad del perro.
    """
    from catalogo_menus import CATALOGO
    al, _ = cargar_v2()
    clave = f"{tamano}_{etapa}"
    entrada = CATALOGO.get(clave)
    if not entrada:
        return {"encontrado": False}

    if der_objetivo and peso_perro_kg:
        SUP_COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                           "Calcio", "Hierro", "Vitamina B")
        factor = der_objetivo / entrada["der"]
        gramos_escalados = {}
        for n, g in entrada["gramos"].items():
            a = al.get(n, {})
            if a.get("categoria") in SUP_COMERCIALES:
                techo = dosis_maxima_fabricante(a, peso_perro_kg)
                gramos_escalados[n] = round(min(g * factor, techo), 2) if techo else round(g * factor, 2)
            else:
                gramos_escalados[n] = round(g * factor, 2)
        return {"encontrado": True, **entrada, "gramos": gramos_escalados,
                "der_escalado_a": der_objetivo}

    return {"encontrado": True, **entrada}


@app.post("/menu/v2")
def endpoint_menu_v2(datos: PeticionMenu):
    """
    ⚠️ AÑADIDO (5 agosto, tarde) -- BLINDAJE: toda la logica real vive en
    _resolver_menu_v2_interno(). Aqui SOLO se la envuelve en un try/except
    que atrapa CUALQUIER fallo no previsto y devuelve JSON valido siempre,
    en vez de dejar que una excepcion sin capturar rompa la respuesta y
    el frontend reciba algo que no es JSON ("Expecting value: line 1
    column 1", que es literalmente lo que da json.parse con una respuesta
    vacia o cortada). Esto no sustituye arreglar la causa real (timeouts,
    etc.) -- es la red de seguridad para que, pase lo que pase, la app
    reciba SIEMPRE algo que sepa interpretar.
    """
    try:
        return _resolver_menu_v2_interno(datos)
    except Exception as e:
        import traceback
        traceback.print_exc()  # queda en los logs de Render para poder investigarlo
        return {"factible": False,
                "motivo": f"Ha fallado algo inesperado en el servidor ({type(e).__name__}). "
                          "Inténtalo de nuevo -- si se repite, dínoslo."}


def _resolver_menu_v2_interno(datos: PeticionMenu):
    """
    EL MOTOR NUEVO. Misma petición que /menu (mismo modelo PeticionMenu),
    pero resuelto con programación lineal entera mixta: decide qué
    alimentos usar y cuánto de cada uno A LA VEZ, de entre TODOS los
    accesibles — no solo entre los `nombres_alimentos` que mande el
    frontend. Si `nombres_alimentos` viene vacío, el motor elige libre.

    ⚠️ TEMPORAL mientras se compara con /menu (el viejo). El límite de
    2 suplementos, la verdura al 10%, extras+suplementos al 5% y el
    criterio "todo diario en cualquier etapa" son fijos aquí — decisiones
    ya tomadas, no parámetros que mande el frontend.
    """
    al, req = cargar_v2()
    # ⚠️ AÑADIDO (5 agosto, tarde) — PRESUPUESTO DE TIEMPO TOTAL: Render
    # (plan gratis) corta la conexión a los 30s si no hay respuesta.
    # Antes esto se controlaba solo contando "número de intentos", y la
    # suma se escapó dos veces (llegó a 96s, y luego a 50s) porque no se
    # medía el tiempo real acumulado. Con esto se para de reintentar en
    # cuanto se acerca al límite, en vez de solo contar cuántas veces.
    t_inicio_total = time.time()
    PRESUPUESTO_SEGUNDOS = 18.0

    def tiempo_restante():
        """
        ⚠️ AÑADIDO (5 agosto, tarde): comprobar el presupuesto SOLO antes
        de cada intento no basta -- una llamada individual puede seguir
        corriendo su propio time_limit COMPLETO sin enterarse de que el
        presupuesto global ya casi se había acabado. Esto calcula cuánto
        queda de verdad y se lo pasa a CADA llamada del motor, para que
        ninguna pueda, por sí sola, hacer que el total supere los 18s.
        Nunca menos de 1s (para no mandar un time_limit inútil).
        """
        return max(1.0, PRESUPUESTO_SEGUNDOS - (time.time() - t_inicio_total))

    excluidos = list(datos.especies_excluidas or []) + list(datos.nombres_excluidos or [])

    # ⚠️ CONECTADO (5 agosto, noche): las patologías existían en el modelo
    # y en el perfil que manda la app, pero el motor nunca las miraba.
    # Las que dependen de analíticas (estruvita/cistina/urato) BLOQUEAN
    # la generación automática — se deriva al veterinario en vez de dar
    # un menú que podría empeorar el problema.
    from motor_completo import patologias_bloquean, avisos_de_patologias
    bloqueantes = patologias_bloquean(datos.patologias)
    if bloqueantes:
        return {"factible": False, "requiere_veterinario": True,
                "motivo": " ".join(avisos_de_patologias(bloqueantes))}

    forzar, preferir = None, None
    if datos.modo == "personalizar":
        forzar = list(datos.forzar_presencia or datos.nombres_alimentos or [])
    elif datos.modo == "aprovechar":
        preferir = list(datos.nombres_alimentos or [])
    elif datos.modo == "automatico" and not excluidos and not datos.patologias:
        # ⚠️ AÑADIDO (5 agosto): en automático, sin alergias ni patologías,
        # se prueba PRIMERO con la base de alimentos del catálogo fijo más
        # cercano (mismo tamaño y etapa) forzada -- el motor solo tiene que
        # decidir cuánto de cada uno y qué añadir para cerrar lo que falte,
        # en vez de buscar desde cero. Probado: 0.1-0.5s en vez de 2-13s, y
        # sale verde en la mayoría de los casos. Si con esa base no llega a
        # cerrar los 30 requisitos (pasa a veces con pesos muy distintos al
        # representativo del catálogo), se descarta el intento rápido y se
        # sigue abajo con la búsqueda libre de siempre -- nunca se entrega
        # un menú que no esté en verde de verdad.
        from catalogo_menus import CATALOGO
        SUP_COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                           "Calcio", "Hierro", "Vitamina B")
        clave = f"{datos.tamano}_{datos.etapa_requisitos}" if datos.tamano else None
        entrada = CATALOGO.get(clave) if clave else None
        if entrada:
            base = [n for n in entrada["gramos"]
                   if al.get(n, {}).get("categoria") not in SUP_COMERCIALES]
            # ⚠️ AÑADIDO (5 agosto, mañana) — CASO REAL ENCONTRADO: para
            # Cairo, el atajo salía "ámbar" a la primera y se descartaba
            # entero, cayendo a la búsqueda libre completa (13-19s con
            # reintentos). Pero con la aleatoriedad que se le puso al
            # motor, reintentar la MISMA base forzada unas pocas veces (el
            # resto de ingredientes sí varía entre intentos) suele llegar
            # a verde en la primera o segunda vuelta, en fracciones de
            # segundo cada una -- mucho más barato que rendirse tan
            # pronto e ir al camino lento.
            while time.time() - t_inicio_total < PRESUPUESTO_SEGUNDOS:
                ok_rapido, gramos_rapido = resolver_v2(
                    datos.der_objetivo, datos.etapa_requisitos, al, req,
                    datos.peso_perro_kg, dosis_maxima_fabricante,
                    margenes_categoria=MARGENES_V2, max_suplementos=2, forzar=base, time_limit=tiempo_restante(),
                )
                if not ok_rapido:
                    break
                ficha_rapida = verificar_v2(gramos_rapido, al, req, datos.der_objetivo, datos.etapa_requisitos)
                if ficha_rapida["semaforo"] == "verde":
                    problemas_rapido = revisar_seguridad_v2(gramos_rapido, al, datos.der_objetivo,
                                                            datos.etapa_requisitos, datos.patologias)
                    return {
                        "factible": True, "menu": gramos_rapido, "ficha": ficha_rapida,
                        "problemas_seguridad": problemas_rapido,
                        "kcal_total": sum(al[n]["energia"] * g / 100 for n, g in gramos_rapido.items()),
                        "gramos_total": sum(gramos_rapido.values()),
                        "via_catalogo": True,
                    }
                # si no salió verde, se prueba otra vez -- si se agota el
                # presupuesto de tiempo, se descarta y se sigue con la búsqueda libre

    # ⚠️ AÑADIDO: si el presupuesto YA se agotó en la vía catálogo, no
    # tiene sentido intentar la búsqueda libre (que tarda más por
    # intento) -- se rinde ya, con una respuesta clara, en vez de gastar
    # más tiempo del que Render permite.
    if time.time() - t_inicio_total >= PRESUPUESTO_SEGUNDOS:
        return {"factible": False,
                "motivo": "El cálculo está tardando más de lo normal para este perro. "
                          "Inténtalo de nuevo en un momento."}

    ok, gramos = resolver_v2(
        datos.der_objetivo, datos.etapa_requisitos, al, req,
        datos.peso_perro_kg, dosis_maxima_fabricante,
        excluidos=excluidos or None,
        margenes_categoria=MARGENES_V2, max_suplementos=2, time_limit=tiempo_restante(),
        forzar=forzar, preferir=preferir,
        patologias=datos.patologias, restringir_especie=datos.restringir_especie,
    )
    # ⚠️ AÑADIDO (5 agosto): con la aleatoriedad puesta en el motor, un
    # intento puede salir "factible" (cumple matemáticamente) pero no del
    # todo en verde -- reintentar tiene sentido de verdad ahora, porque
    # cada intento explora una combinación distinta. Mientras quede
    # presupuesto de tiempo, no un número fijo de intentos.
    ficha_intento = None
    while time.time() - t_inicio_total < PRESUPUESTO_SEGUNDOS:
        ficha_intento = verificar_v2(gramos, al, req, datos.der_objetivo, datos.etapa_requisitos)
        if ficha_intento["semaforo"] == "verde":
            break
        ok2, gramos2 = resolver_v2(
            datos.der_objetivo, datos.etapa_requisitos, al, req,
            datos.peso_perro_kg, dosis_maxima_fabricante,
            excluidos=excluidos or None,
            margenes_categoria=MARGENES_V2, max_suplementos=2, time_limit=tiempo_restante(),
            forzar=forzar, preferir=preferir,
            patologias=datos.patologias, restringir_especie=datos.restringir_especie,
        )
        if ok2:
            ok, gramos = ok2, gramos2
    if not ok and datos.modo == "personalizar":
        # igual que hacía /menu (el viejo): si forzar lo elegido a mano
        # deja sin solución, se reintenta libre — mejor un menú con aviso
        # que un error sin más.
        ok, gramos = resolver_v2(
            datos.der_objetivo, datos.etapa_requisitos, al, req,
            datos.peso_perro_kg, dosis_maxima_fabricante,
            excluidos=excluidos or None,
            margenes_categoria=MARGENES_V2, max_suplementos=2, time_limit=tiempo_restante(),
            patologias=datos.patologias,
        )
        no_se_pudo_forzar = ok
    else:
        no_se_pudo_forzar = False

    if not ok:
        return {"factible": False,
                "motivo": "No existe ninguna combinación de alimentos accesibles "
                          "que cumpla los 30 requisitos con máximo 2 suplementos "
                          "para este perro."}
    ficha = verificar_v2(gramos, al, req, datos.der_objetivo, datos.etapa_requisitos)
    problemas_seguridad = revisar_seguridad_v2(gramos, al, datos.der_objetivo,
                                               datos.etapa_requisitos,
                                               datos.patologias)
    resultado = {
        "factible": True,
        "menu": gramos,
        "ficha": ficha,
        "problemas_seguridad": problemas_seguridad,
        "kcal_total": sum(al[n]["energia"] * g / 100 for n, g in gramos.items()),
        "gramos_total": sum(gramos.values()),
    }
    if no_se_pudo_forzar:
        resultado["no_se_pudo_forzar"] = True
    return resultado


@app.post("/transicion")
def endpoint_transicion(datos: PeticionTransicion):
    fecha_inicio = date.fromisoformat(datos.fecha_inicio)
    fecha_hoy = date.fromisoformat(datos.fecha_hoy) if datos.fecha_hoy else None
    tramo = calcular_tramo_transicion(fecha_inicio, fecha_hoy)
    menus = menu_activo_y_bloqueados(fecha_inicio, datos.num_menus_elegidos, fecha_hoy)
    nivel = nivel_indicador_nutrientes(fecha_inicio, datos.num_menus_elegidos, fecha_hoy)
    return {**tramo, **menus, "nivel_indicador_nutrientes": nivel}


# ⚠️ REESCRITOS (5 agosto, noche) — estos tres endpoints seguian llamando a
# recalculo.py, que usa el LP VIEJO abandonado. Por eso el lapiz de editar
# rompia el menu (pulpo duplicado, 313 g totales, y el badge "27/27 OK" --
# que ni siquiera es un dato real, es texto fijo en el frontend -- seguia
# diciendo que todo iba bien). Ahora los tres pasan por motor_completo.py,
# igual que /menu/v2: se FUERZA el alimento nuevo (o se excluye el
# quitado) y se resuelve de cero con el MILP, así que el resultado SIEMPRE
# esta comprobado de verdad contra los 30 requisitos, nunca puede quedar
# a medias ni duplicado.
def _recalcular_con_motor(datos, forzar=None, excluir_nombres=None):
    al, req = cargar_v2()
    excluidos = list(datos.especies_excluidas or [])
    nombres_excl = set(datos.nombres_excluidos or [])
    if excluir_nombres:
        nombres_excl |= set(excluir_nombres)
    # ⚠️ CORREGIDO (5 agosto, mañana): esto llamaba UNA vez y devolvía
    # "factible: True" con lo que saliera, SIN comprobar si el resultado
    # era verde de verdad -- solo si el programa encontraba algo que
    # cumpliera matemáticamente el problema que se le planteó. Con la
    # aleatoriedad puesta en el motor, eso podía devolver un menú
    # incompleto o al límite como si fuera bueno. Ahora reintenta hasta 3
    # veces hasta que sea verde de verdad, igual que ya hace la
    # generación normal de /menu/v2.
    ok, gramos, ficha = False, None, None
    for _intento in range(3):
        ok, gramos = resolver_v2(
            datos.der_objetivo, datos.etapa_requisitos, al, req,
            datos.peso_perro_kg, dosis_maxima_fabricante,
            excluidos=(excluidos + list(nombres_excl)) or None,
            margenes_categoria=MARGENES_V2, max_suplementos=2,
            forzar=forzar,
        )
        if not ok:
            break
        ficha = verificar_v2(gramos, al, req, datos.der_objetivo, datos.etapa_requisitos)
        if ficha["semaforo"] == "verde":
            break
    if not ok or ficha["semaforo"] != "verde":
        return {"factible": False,
                "motivo": "Con este cambio no existe ninguna combinación que cumpla "
                          "los 30 requisitos. Prueba con otro alimento."}
    return {"factible": True, "gramos": gramos, "ficha": ficha}


@app.post("/menu/cambiar")
def endpoint_cambiar_alimento(datos: PeticionCambiarAlimento):
    """Sustituye un alimento por otro (el lapiz de editar), resolviendo TODO
    de nuevo con el motor real -- el alimento nuevo se fuerza a entrar."""
    return _recalcular_con_motor(datos, forzar=[datos.alimento_nuevo],
                                  excluir_nombres=[datos.alimento_viejo])


@app.post("/menu/anadir")
def endpoint_anadir_alimento(datos: PeticionAnadirQuitarAlimento):
    """Añade un alimento (ej. un suplemento) forzándolo a entrar, y resuelve
    TODO de nuevo con el motor real."""
    return _recalcular_con_motor(datos, forzar=[datos.alimento])


@app.post("/menu/quitar")
def endpoint_quitar_alimento(datos: PeticionAnadirQuitarAlimento):
    """Quita un alimento (excluyéndolo) y resuelve TODO de nuevo con el
    motor real."""
    return _recalcular_con_motor(datos, excluir_nombres=[datos.alimento])


@app.get("/perro/{perro_id}/menus")
def endpoint_obtener_menus(perro_id: int):
    return persistencia.obtener_menus(perro_id)


@app.get("/")
def raiz():
    return {"estado": "CANISLAB API funcionando"}


# =====================================================================
# MODO ANALIZADOR — el usuario mete lo que YA le da y le decimos que tal
# =====================================================================
class AnalisisRequest(BaseModel):
    gramos_por_alimento: dict   # {"Carcasa de pollo": 680, "Calabaza": 68, ...}
    der_objetivo: float = None  # si no viene, se calcula con peso/etapa/actividad
    etapa_requisitos: str = "Adulto"
    # alternativa a mandar el DER ya calculado: mandar el perfil del perro
    peso_kg: float = None
    etapa_der: str = None       # clave de der.py: adulto, cachorro_crecimiento...
    actividad: str = None
    esterilizado: bool = False
    # Datos del metodo europeo. Sin ellos el DER sale con valores prudentes,
    # pero para un CACHORRO el peso adulto esperado es lo que decide el tramo
    # (hasta 50% / 50-80% / desde 80%), asi que conviene mandarlo siempre.
    peso_adulto_esperado_kg: float = None
    peso_ideal_kg: float = None
    convivencia: str = "solo"
    macho_entero: bool = False
    raza: str = None
    semana_gestacion: int = None
    n_cachorros: int = None
    semana_lactancia: int = 3


@app.exception_handler(ValueError)
async def _valueerror_legible(request, exc):
    """
    Los modulos del motor lanzan ValueError con mensajes pensados para leerse
    (etapa desconocida, peso <= 0...). Sin esto FastAPI devolveria un 500 y el
    usuario veria "Internal Server Error" en vez del motivo real.
    """
    return JSONResponse(status_code=400, content={"ok": False, "motivo": str(exc)})


def _etapa_ok(etapa):
    """Traduce el ValueError de resolver_etapa en un 400 legible."""
    if etapa not in ETAPAS_VALIDAS:
        raise HTTPException(400, f"Etapa de requisitos '{etapa}' no valida. "
                                 f"Usa una de: {sorted(ETAPAS_VALIDAS)}")


# =====================================================================
# COMPROBACION DE INTEGRIDAD — se abre en el navegador, sin terminal
#   https://canislab-api.onrender.com/verificar
# Dice si los tres pilares (alimentos, requisitos y DER) llegaron intactos
# al servidor. Nace de que el usuario trabaja desde el movil y no puede
# ejecutar verificar_pilares.py a mano.
# =====================================================================
@app.get("/verificar")
def verificar():
    import hashlib, os
    SELLOS = {
        "alimentos_v3_final.json":      "938f139a8ddf5839",
        "requerimientos_v2_final.json": "73ab445f9881f543",
        "der.py":                       "1c5c8bb91ceac481",
    }
    base = os.path.dirname(os.path.abspath(__file__))
    detalle, todo_ok = [], True
    for fichero, esperado in SELLOS.items():
        ruta = os.path.join(base, fichero)
        if not os.path.exists(ruta):
            detalle.append({"archivo": fichero, "estado": "NO EXISTE"})
            todo_ok = False
            continue
        actual = hashlib.sha256(open(ruta, "rb").read()).hexdigest()[:16]
        ok = actual == esperado
        todo_ok = todo_ok and ok
        detalle.append({
            "archivo": fichero,
            "esperado": esperado,
            "encontrado": actual,
            "estado": "correcto" if ok else "NO COINCIDE — el archivo llego alterado",
        })

    # ademas, que los datos se puedan leer de verdad
    try:
        alimentos = cargar_alimentos()
        n_alimentos = len(alimentos)
    except Exception as e:
        n_alimentos = f"ERROR: {e}"
        todo_ok = False

    return {
        "ok": todo_ok,
        "resumen": ("Los tres pilares estan intactos" if todo_ok
                    else "ALGO NO CUADRA — revisa el detalle y vuelve a subir el archivo"),
        "alimentos_cargados": n_alimentos,
        "detalle": detalle,
    }


@app.post("/analizar")
def analizar(req: AnalisisRequest):
    der = req.der_objetivo
    if der is None:
        if req.peso_kg is None or req.etapa_der is None:
            raise HTTPException(400, "Hacen falta el DER, o bien peso y etapa del perro.")
        d = calcular_der(
            req.peso_kg, req.etapa_der, req.actividad, req.esterilizado,
            peso_adulto_esperado_kg=req.peso_adulto_esperado_kg,
            peso_ideal_kg=req.peso_ideal_kg,
            convivencia=req.convivencia,
            macho_entero=req.macho_entero,
            raza=req.raza,
            semana_gestacion=req.semana_gestacion,
            n_cachorros=req.n_cachorros,
            semana_lactancia=req.semana_lactancia)
        der = d["der"] if isinstance(d, dict) else d
    return analizar_dieta(req.gramos_por_alimento, der, req.etapa_requisitos)


@app.get("/alimentos")
def listar_alimentos():
    """Catalogo agrupado por categoria, para que la app pinte los selectores
    del analizador sin tener que llevar la lista duplicada en el frontend."""
    from especies import cargar_alimentos as _ca
    por_cat = {}
    for a in _ca():
        por_cat.setdefault(a["categoria"], []).append({
            "nombre": a["nombre"],
            "kcal_100g": a["energia"],
            "especie": a.get("especie"),
        })
    for v in por_cat.values():
        v.sort(key=lambda x: x["nombre"])
    return por_cat
