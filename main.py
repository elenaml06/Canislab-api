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
from motor_completo import resolver as resolver_v2, especie_de
from constructor import cargar as cargar_v2, MARGENES as MARGENES_V2
from verificar import verificar as verificar_v2
from seguridad import revisar_seguridad as revisar_seguridad_v2
from seguridad import avisos_rotacion as avisos_rotacion_v2

# ⚠️ AÑADIDO (5 agosto, madrugada) — DOS CASOS REALES ENCONTRADOS
# AUDITANDO: (1) avisos_rotacion() ya existía en seguridad.py, con
# mensajes bien redactados sobre mercurio, cefalópodos, congelación y
# riesgo de hueso -- pero nunca se llamaba desde ningún sitio, así que
# nunca llegaban al usuario. (2) _recalcular_con_motor() (el camino de
# EDITAR un menú ya generado) nunca calculaba problemas_seguridad en
# absoluto -- los avisos de seguridad se perdían cada vez que se
# editaba un alimento, aunque sí funcionaran al generar por primera
# vez. Esta función combina ambas cosas en un solo sitio, para usarla
# en TODOS los puntos donde se devuelve un menú (generación Y edición).
def _seguridad_completa(gramos, al, der, etapa, patologias=None, peso_perro_kg=None):
    problemas = list(revisar_seguridad_v2(gramos, al, der, etapa, patologias,
                                          peso_perro_kg=peso_perro_kg) or [])
    problemas += list(avisos_rotacion_v2(gramos, al) or [])
    return problemas


# ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO, pedido
# expreso por segunda vez: la vitamina D seguía apareciendo como aviso
# tras haber convertido los 5 límites de seguridad crónica (vitD,
# yodo, mercurio, tiaminasa, selenio) en restricciones DURAS dentro de
# resolver(). La causa real: el catálogo de menús PRE-CALCULADOS
# (motor/catalogo_menus.py, generado el 5 de agosto con una versión
# vieja del motor) se sigue sirviendo directamente en 4 sitios de este
# archivo para ir más rápido, SIN volver a pasar por el solver nunca
# -- así que cualquier menú servido desde ahí nunca ve las
# restricciones nuevas, y puede violarlas indefinidamente, hasta que
# alguien regenere ese catálogo a mano. Esta función valida un menú
# precalculado directamente contra los 5 límites duros (misma lógica,
# mismas constantes que dentro de resolver() -- sin resolver nada, solo
# calculando), para poder descartarlo y caer al solver en vivo si ya
# no es seguro según las reglas actuales, en vez de servirlo ciego.
def _menu_precalculado_es_seguro(gramos, al, der, peso_perro_kg=None):
    from seguridad import (
        TIAMINASA, MERCURIO_ALTO, TOPE_TIAMINASA_KCAL, TOPE_MERCURIO_KCAL,
        TOPE_VITD_KCAL, TOPE_VITD_KG075, TOPE_YODO_KCAL, TOPE_SELENIO_G_DIETA, _es,
    )
    if not der:
        return True  # sin DER no se puede evaluar nada -- no bloquear por falta de dato
    total_g = sum(gramos.values()) or 1.0

    kcal_tia = sum(al.get(n, {}).get("energia", 0) * g / 100.0 for n, g in gramos.items() if _es(n, TIAMINASA))
    if kcal_tia > der * TOPE_TIAMINASA_KCAL:
        return False

    kcal_merc = sum(al.get(n, {}).get("energia", 0) * g / 100.0 for n, g in gramos.items() if _es(n, MERCURIO_ALTO))
    if kcal_merc > der * TOPE_MERCURIO_KCAL:
        return False

    vitd_ug = sum(al.get(n, {}).get("nutrientes", {}).get("vitD", 0) * g / 100.0 for n, g in gramos.items())
    tope_vitd = TOPE_VITD_KCAL * der / 1000.0
    if peso_perro_kg and peso_perro_kg > 0:
        tope_vitd = min(tope_vitd, TOPE_VITD_KG075 * (peso_perro_kg ** 0.75))
    if vitd_ug > tope_vitd:
        return False

    yodo_ug = sum(al.get(n, {}).get("nutrientes", {}).get("yodo", 0) * g / 100.0 for n, g in gramos.items())
    if yodo_ug > TOPE_YODO_KCAL * der / 1000.0:
        return False

    selenio_ug = sum(al.get(n, {}).get("nutrientes", {}).get("selenio", 0) * g / 100.0 for n, g in gramos.items())
    if (selenio_ug / total_g) > TOPE_SELENIO_G_DIETA:
        return False

    return True

# ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL: varias veces esta noche
# el problema resultó ser que Render seguía sirviendo una versión VIEJA
# de main.py, aunque el archivo correcto ya estuviera subido a GitHub --
# /verificar comprobaba los DATOS (JSON, der.py) pero nunca el propio
# main.py, así que no había forma de confirmar esto sin pegar el
# archivo entero para compararlo a mano. Con esto, /verificar dice
# desde CUÁNDO lleva corriendo este proceso -- si acabas de subir algo
# nuevo y este número es de hace horas, esa es la prueba de que el
# despliegue no se ha aplicado todavía.
import datetime
_ARRANCADO_EN = datetime.datetime.utcnow().isoformat() + "Z"

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
    # ⚠️ CORREGIDO (5 agosto, noche): mismo fallo que en PeticionMenu --
    # tipo estricto con default None en vez de Optional, rechazaba con
    # 422 cualquier petición que mandara null explícito para estos campos.
    peso_adulto_esperado_kg: Optional[float] = None
    peso_ideal_kg: Optional[float] = None
    convivencia: str = "solo"
    macho_entero: bool = False
    raza: Optional[str] = None
    semana_gestacion: Optional[int] = None
    n_cachorros: Optional[int] = None
    semana_lactancia: int = 3
    peso_actual_kg: float
    etapa: str
    actividad_idx: int  # 0=sedentario .. 4=trabajo
    esterilizado: bool
    # ⚠️ AÑADIDO (5 agosto, noche) — FALLO GRAVE ENCONTRADO: el endpoint
    # nunca mandaba estos tres campos a calcular_der(), aunque la función
    # SÍ los acepta y los necesita para deducir el peso adulto de la
    # curva de crecimiento real del cachorro (edad + peso actual), no de
    # la media de su raza. Sin "meses", la curva nunca se activaba --
    # el DER de CUALQUIER cachorro de una raza con rango amplio de peso
    # adulto (como el Am Staff, 18-34 kg) salía calculado con la media,
    # nunca con su trayectoria real. Caso real: Cairo con 5 meses y 18kg
    # apunta a 34kg de adulto, no a los 26kg de la media -- 192 kcal/día
    # de diferencia, confirmado.
    meses: Optional[float] = None
    peso_min_raza: Optional[float] = None
    peso_max_raza: Optional[float] = None


class PeticionMenu(BaseModel):
    # ⚠️ CORREGIDO (5 agosto, noche) — FALLO GRAVE ENCONTRADO: todos estos
    # campos declaraban un tipo estricto ("float", "str", "list"...) con
    # valor por defecto None, en vez de "Optional[tipo]". Eso funciona
    # bien cuando el campo NO viene en la petición -- pero si el cliente
    # manda el campo con valor null EXPLÍCITO (que es justo lo que hace
    # el frontend a partir del segundo menú para "tamano", una vez ya
    # hay especies excluidas), Pydantic rechaza la petición entera con un
    # 422, porque None no es un valor válido para el tipo declarado. Por
    # eso el primer menú automático siempre salía bien y los siguientes
    # fallaban siempre: "tamano" pasaba de un texto real a null a partir
    # del segundo. Ahora cualquiera de estos campos admite null de verdad.
    peso_perro_kg: Optional[float] = None
    # peso ADULTO esperado: activa el tope de calcio de raza grande en cachorros
    peso_adulto_esperado_kg: Optional[float] = None
    nombres_excluidos: Optional[list] = None
    patologias: Optional[list] = None
    # ⚠️ AÑADIDO (5 agosto): "Toy"/"Mini"/"Pequeño"/"Mediano"/"Grande"/
    # "Gigante" -- para poder intentar primero la vía rápida del catálogo
    # fijo (mismo tamaño y etapa) antes de la búsqueda libre completa.
    tamano: Optional[str] = None
    # Lo que el usuario ha elegido A MANO en Personalizar o Aprovechar. Sin
    # esto, el optimizador podia ponerlo a 0 gramos y el usuario veia que su
    # eleccion desaparecia del menu sin explicacion.
    forzar_presencia: Optional[list] = None
    nombres_alimentos: list[str]
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []
    # ⚠️ AÑADIDO (5 agosto, noche): "Todo el/la {especie}" en
    # personalizar/aprovechar -- {categoria: especie}. Restringe esa
    # categoría a solo esa especie, dejando que el motor elija
    # libremente qué corte/pieza usar dentro de ella.
    restringir_especie: Optional[dict] = None
    # ⚠️ AÑADIDO (5 agosto, madrugada) — pedido expreso: perros que no
    # pueden masticar hueso carnoso con normalidad (senior, dientes en
    # mal estado...) necesitan poder excluir la categoría ENTERA de la
    # ración -- lista de nombres de categoría (típicamente solo "Hueso
    # carnoso") que quedan a 0g, sin excepción. El calcio que
    # normalmente aportaría el hueso lo cubre el motor automáticamente
    # con un suplemento de calcio, dado que los 30 requisitos siempre
    # se cumplen matemáticamente y el calcio ya es un candidato
    # disponible sin necesidad de forzarlo aparte.
    categorias_excluidas: Optional[list] = None
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CAMBIO DE ARQUITECTURA PEDIDO
    # EXPRESAMENTE: presupuesto semanal RESTANTE de seguridad crónica
    # (tiaminasa/mercurio/vitD/yodo/selenio_g_dieta), calculado por
    # quien orquesta la generación de varios menús -- se propaga hasta
    # resolver() como una restricción DURA para este menú concreto, no
    # como un aviso posterior. Ver docstring de resolver() en
    # motor_completo.py para el mecanismo completo.
    presupuesto_semanal_restante: Optional[dict] = None
    # ⚠️ AÑADIDO (5 agosto, madrugada): para la rotación de proteína entre
    # varios menús automáticos -- antes iba mezclada con especies_excluidas
    # (una exclusión DURA, pensada para alergias reales), así que si la
    # especie del menú anterior era la única forma razonable de cerrar los
    # 30 requisitos, la rotación podía volver el problema imposible sin
    # que el usuario hubiera pedido nada de eso. Ahora es una preferencia
    # SUAVE: el motor la evita si puede, nunca falla por su culpa.
    evitar_especies: Optional[list] = None
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
    # ⚠️ CORREGIDO (5 agosto, noche): mismo fallo que en PeticionMenu.
    peso_perro_kg: Optional[float] = None
    nombres_excluidos: Optional[list] = None
    patologias: Optional[list] = None
    menu_actual: list[str]
    alimento_viejo: str
    alimento_nuevo: str
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []
    # ⚠️ AÑADIDO (5 agosto, noche): para que el tope de calcio de razas
    # grandes/gigantes en crecimiento se respete también al editar un
    # alimento, no solo al generar el menú por primera vez.
    peso_adulto_esperado_kg: Optional[float] = None
    # ⚠️ AÑADIDO (5 agosto, madrugada): mismo motivo que en PeticionMenu
    # -- si el perro no puede masticar hueso carnoso, esa exclusión debe
    # respetarse también al editar, no solo al generar por primera vez.
    categorias_excluidas: Optional[list] = None


class PeticionAnadirQuitarAlimento(BaseModel):
    # ⚠️ CORREGIDO (5 agosto, noche): mismo fallo que en PeticionMenu.
    peso_perro_kg: Optional[float] = None
    nombres_excluidos: Optional[list] = None
    patologias: Optional[list] = None
    menu_actual: list[str]
    alimento: str
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []
    # ⚠️ AÑADIDO (5 agosto, noche): mismo motivo que en PeticionCambiarAlimento.
    peso_adulto_esperado_kg: Optional[float] = None


# ⚠️ AÑADIDO (5 agosto, madrugada) — pedido expreso: comprueba el
# aporte de tiaminasa a lo largo de TODA la semana de rotación, no
# solo dentro de un menú aislado (ver revisar_seguridad_semanal en
# seguridad.py para el motivo completo).
class MenuConDias(BaseModel):
    gramos: dict[str, float]
    dias: int


class PeticionVerificarSemana(BaseModel):
    menus: list[MenuConDias]
    der_objetivo: float
    # ⚠️ AÑADIDO (5 agosto, madrugada): mismo motivo que en PeticionMenu.
    categorias_excluidas: Optional[list] = None
    # ⚠️ AÑADIDO (5 agosto, madrugada): para el chequeo por peso^0.75 de
    # vitamina D (ver revisar_seguridad_semanal / TOPE_VITD_KG075).
    peso_perro_kg: Optional[float] = None


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
        semana_lactancia=datos.semana_lactancia,
        # ⚠️ AÑADIDO (5 agosto, noche): sin esto, la curva de crecimiento
        # real nunca se activaba -- ver nota en PeticionDER.
        meses=datos.meses,
        peso_min_raza=datos.peso_min_raza,
        peso_max_raza=datos.peso_max_raza)
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
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO en
    # auditoría exhaustiva: este endpoint (el motor VIEJO, "optimizar_menu",
    # anterior al motor MILP de motor_completo.py) nunca pasa por
    # resolver() en absoluto -- así que nunca ha visto ninguna de las
    # restricciones duras de seguridad crónica de esta sesión. El
    # frontend actual no lo llama (confirmado: cero referencias a "/menu"
    # sin v2 en App.jsx), pero sigue expuesto públicamente, y "ningún
    # límite se puede sobrepasar nunca" no puede depender de que nadie
    # descubra y use este camino. Se valida el resultado igual que en
    # el catálogo pre-calculado antes de devolverlo.
    gramos_resultado = resultado.get("gramos") or resultado.get("menu")
    if resultado.get("factible") and gramos_resultado and not _menu_precalculado_es_seguro(
            gramos_resultado, {a["nombre"]: a for a in alimentos}, datos.der_objetivo, datos.peso_perro_kg):
        return {"factible": False,
                "motivo": "Este motor (antiguo) no puede garantizar los límites de seguridad "
                          "crónica actuales -- usa /menu/v2 en su lugar."}
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
        if not _menu_precalculado_es_seguro(gramos_escalados, al, der_objetivo, peso_perro_kg):
            return {"encontrado": False,
                    "motivo": "El menú de catálogo para este tamaño/etapa, reescalado a "
                              "este peso y calorías, superaría un límite de seguridad -- "
                              "pide el menú por /menu/v2 en su lugar, que resuelve en vivo "
                              "respetando siempre esos límites."}
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


# ⚠️ AÑADIDO (5 agosto, madrugada) — CAMBIO DE ARQUITECTURA PEDIDO
# EXPRESAMENTE: los límites de seguridad crónica (tiaminasa, mercurio,
# vitamina D, yodo, selenio) tienen sentido SEMANAL, no solo por
# ración -- pero hasta ahora cada menú de la rotación se generaba en
# una llamada aparte del frontend, sin que el servidor supiera nada de
# lo que ya llevaban los menús anteriores de esa misma semana. El
# resultado era que solo se avisaba DESPUÉS de generar, cuando ya era
# tarde -- y un aviso es algo que el usuario puede ignorar, cuando la
# responsabilidad de que esto no pase nunca es del sistema, no suya.
#
# Este endpoint genera TODOS los menús de una semana en una sola
# llamada al servidor, para que el propio servidor pueda ir calculando
# cuánto presupuesto semanal queda tras cada menú y pasárselo a
# resolver() como una restricción DURA para el siguiente -- así, por
# diseño, es matemáticamente imposible que la SUMA de una semana
# entera supere el límite seguro, sin depender de ningún aviso.
from seguridad import (
    TOPE_TIAMINASA_KCAL, TOPE_MERCURIO_KCAL, TOPE_VITD_KCAL, TOPE_YODO_KCAL,
    TOPE_SELENIO_G_DIETA,
)


def _presupuesto_semanal_inicial(der_objetivo):
    """Presupuesto SEGURO para la semana completa, para cada uno de los
    5 puntos de riesgo crónico. tiaminasa/mercurio son fracción de kcal
    (0-1); vitD/yodo son µg por 1000kcal; selenio_g_dieta es µg por
    gramo de dieta -- cada uno se reparte en su propia unidad, ver
    resolver() en motor_completo.py para cómo se usa cada una.

    ⚠️ CORREGIDO en el mismo momento, ANTES de entregarlo -- AUTOCRÍTICA
    real: la primera versión de esto multiplicaba el tope diario × 7
    sin más margen. Probando el cálculo con datos reales, esto resultó
    ser matemáticamente redundante con el tope diario ya endurecido en
    la Fase 1 -- si CADA menú individual ya respeta su propio tope
    diario, la suma de 7 días respetando cada uno NUNCA puede superar
    7× el tope diario, así que el mecanismo semanal nunca podría
    dispararse de forma distinta al diario. Mismo fallo que ya se
    encontró y corrigió antes con el chequeo de tiaminasa en
    seguridad.py. El valor real de un límite semanal es capturar que
    el consumo SOSTENIDO es más peligroso que un pico puntual -- eso es
    justo lo que dice la propia investigación de estos nutrientes
    (vitD, yodo, mercurio, selenio son riesgos principalmente
    crónicos). MARGEN_SEGURIDAD_CRONICA aplica ese margen real: el
    presupuesto semanal total es más bajo que "tope diario × 7", no
    igual -- así el mecanismo semanal SÍ añade protección genuina
    sobre el diario, en vez de ser matemáticamente redundante con él.
    """
    MARGEN_SEGURIDAD_CRONICA = 0.75  # criterio de desarrollo, no de una fuente concreta
    return {
        "tiaminasa": TOPE_TIAMINASA_KCAL,       # fracción de kcal, igual cada día (no acumula)
        "mercurio": TOPE_MERCURIO_KCAL,          # fracción de kcal, igual cada día (no acumula)
        "vitD": TOPE_VITD_KCAL * der_objetivo / 1000.0 * 7 * MARGEN_SEGURIDAD_CRONICA,
        "yodo": TOPE_YODO_KCAL * der_objetivo / 1000.0 * 7 * MARGEN_SEGURIDAD_CRONICA,
        "selenio_g_dieta": TOPE_SELENIO_G_DIETA,  # µg/g de dieta, igual cada día (no depende del DER)
    }


def _consumo_real_menu(gramos, al, der_objetivo):
    """Cuánto de cada uno de los 5 puntos de riesgo aportó REALMENTE un
    menú ya generado, en las mismas unidades que _presupuesto_semanal_inicial
    -- para poder restar del presupuesto según pasan los menús."""
    from seguridad import TIAMINASA, MERCURIO_ALTO, _es
    total_g = sum(gramos.values()) or 1.0
    kcal_tia = sum(al.get(n, {}).get("energia", 0) * g / 100.0 for n, g in gramos.items() if _es(n, TIAMINASA))
    kcal_merc = sum(al.get(n, {}).get("energia", 0) * g / 100.0 for n, g in gramos.items() if _es(n, MERCURIO_ALTO))
    vitd_ug = sum(al.get(n, {}).get("nutrientes", {}).get("vitD", 0) * g / 100.0 for n, g in gramos.items())
    yodo_ug = sum(al.get(n, {}).get("nutrientes", {}).get("yodo", 0) * g / 100.0 for n, g in gramos.items())
    selenio_ug = sum(al.get(n, {}).get("nutrientes", {}).get("selenio", 0) * g / 100.0 for n, g in gramos.items())
    return {
        "tiaminasa": (kcal_tia / der_objetivo) if der_objetivo else 0,
        "mercurio": (kcal_merc / der_objetivo) if der_objetivo else 0,
        "vitD": vitd_ug,   # µg reales de ESTE menú (se multiplicará por sus días al acumular)
        "yodo": yodo_ug,
        "selenio_g_dieta": (selenio_ug / total_g) if total_g else 0,
    }


def _presupuesto_para_menu_actual(restante, dias_restantes_incluido_este):
    """Reparte el presupuesto que queda entre los días que faltan
    (incluido el menú que se va a generar ahora), para dar el tope
    DIARIO efectivo de ESTE menú -- lo que resolver() usa como techo.
    tiaminasa/mercurio/selenio_g_dieta ya son "por día" (no se dividen,
    son una fracción/densidad, no un total acumulable); vitD/yodo SÍ
    son totales acumulados, así que sí se dividen entre los días."""
    dias = max(1, dias_restantes_incluido_este)
    return {
        "tiaminasa": max(0.0, restante["tiaminasa"]),
        "mercurio": max(0.0, restante["mercurio"]),
        "vitD": max(0.0, restante["vitD"]) / dias,
        "yodo": max(0.0, restante["yodo"]) / dias,
        "selenio_g_dieta": max(0.0, restante["selenio_g_dieta"]),
    }


@app.post("/menu/semana")
def endpoint_menu_semana(datos: PeticionMenu, numero_de_menus: int = 1):
    """Genera TODOS los menús de una rotación semanal en una sola
    llamada, con el presupuesto semanal de seguridad crónica repartido
    y endurecido en cada uno según lo que ya llevan los anteriores --
    ver el bloque de comentarios justo arriba para el porqué completo."""
    try:
        al, req = cargar_v2()
        n = max(1, min(8, numero_de_menus))
        base_dias = 7 // n
        resto_dias = 7 % n
        dias_por_menu = [base_dias + (1 if i < resto_dias else 0) for i in range(n)]

        presupuesto_restante = _presupuesto_semanal_inicial(datos.der_objetivo)
        menus_generados = []
        especies_usadas = []

        for i in range(n):
            dias_este = dias_por_menu[i]
            dias_restantes_incluido_este = sum(dias_por_menu[i:])
            presupuesto_para_este = _presupuesto_para_menu_actual(
                presupuesto_restante, dias_restantes_incluido_este)

            datos_este = datos.model_copy(update={
                "presupuesto_semanal_restante": presupuesto_para_este,
                "evitar_especies": list(datos.evitar_especies or []) + especies_usadas,
            })
            resultado = _resolver_menu_v2_interno(datos_este)

            if not resultado.get("factible"):
                # ⚠️ si YA se generó al menos un menú, se devuelven los que
                # sí se consiguieron con aviso, en vez de tirar todo lo
                # bueno por un fallo en el último -- mismo criterio que ya
                # se usa en el resto de la app (mejor una respuesta parcial
                # honesta que nada).
                if menus_generados:
                    return {"factible": True, "menus": menus_generados,
                            "aviso": f"Se generaron {len(menus_generados)} de {n} menús pedidos -- "
                                     f"el siguiente no encontró una combinación que respetara los "
                                     f"límites de seguridad semanales que ya llevaban los anteriores."}
                return resultado

            gramos = resultado.get("menu") or resultado.get("gramos") or {}
            menus_generados.append({**resultado, "dias": dias_este})

            consumo = _consumo_real_menu(gramos, al, datos.der_objetivo)
            presupuesto_restante = {
                "tiaminasa": presupuesto_restante["tiaminasa"],  # fracción diaria, no se acumula
                "mercurio": presupuesto_restante["mercurio"],
                "vitD": presupuesto_restante["vitD"] - consumo["vitD"] * dias_este,
                "yodo": presupuesto_restante["yodo"] - consumo["yodo"] * dias_este,
                "selenio_g_dieta": presupuesto_restante["selenio_g_dieta"],  # densidad diaria, no se acumula
            }

            for cat in ("Carne muscular", "Pescados y mariscos", "Hueso carnoso", "Vísceras", "Hígado"):
                principal = sorted(
                    ((nom, g) for nom, g in gramos.items()
                    if al.get(nom, {}).get("categoria") == cat), key=lambda x: -x[1])
                if principal:
                    especies_usadas.append(especie_de(principal[0][0]))

        return {"factible": True, "menus": menus_generados}
    except Exception as e:
        import traceback
        traceback.print_exc()
        return {"factible": False,
                "motivo": f"Ha fallado algo inesperado generando la semana ({type(e).__name__}). "
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
    # ⚠️ AJUSTADO (5 agosto, madrugada) — CASO REAL ENCONTRADO: para
    # perros muy pequeños en etapas exigentes (ej. Toy CachorroJoven de
    # 1.5kg), el requisito de yodo es genuinamente difícil de cumplir de
    # forma consistente por la aleatoriedad del solver -- con 18s de
    # presupuesto solo caben 4-6 intentos, y con ~50-60% de probabilidad
    # de éxito por intento, hay una probabilidad real (no despreciable)
    # de que todos fallen y el sistema devuelva "no factible" aunque SÍ
    # exista una solución. Subido a 24s -- deja 6s de margen antes del
    # límite real de 30s de Render, y da más intentos al solver, bajando
    # la probabilidad de fallo total. No elimina el problema del todo
    # (sigue siendo un caso genuinamente difícil), pero lo mitiga de
    # forma medible sin arriesgar el límite de tiempo de Render.
    PRESUPUESTO_SEGUNDOS = 24.0

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
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CONECTADO CON LAS VARIANTES
    # PRE-RESUELTAS: si en Personalizar el usuario solo pidió "Todo
    # el/la X" en Carne muscular o Pescados y mariscos (nada más forzado,
    # sin alergias ni patologías), eso es EXACTAMENTE lo mismo que una
    # de las variantes ya calculadas para este tamaño y etapa -- no
    # tiene sentido resolverlo de nuevo en caliente. Se sirve al
    # instante si hay una coincidencia exacta; si no la hay (más de una
    # restricción, alimentos concretos forzados, alergias...), se sigue
    # abajo con el camino normal de Personalizar, resolviendo en vivo.
    if (datos.modo == "personalizar" and datos.tamano and not excluidos
            and not datos.patologias and not (datos.forzar_presencia or datos.nombres_alimentos)
            and datos.restringir_especie and len(datos.restringir_especie) == 1):
        (cat_pedida, especie_pedida), = datos.restringir_especie.items()
        if cat_pedida in ("Carne muscular", "Pescados y mariscos"):
            from catalogo_menus import CATALOGO_VARIANTES
            clave_v = f"{datos.tamano}_{datos.etapa_requisitos}"
            variantes = CATALOGO_VARIANTES.get(clave_v, [])
            coincide = next((v for v in variantes
                             if v["proteina"].strip().lower() == especie_pedida.strip().lower()), None)
            if coincide:
                SUP_COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                                   "Calcio", "Hierro", "Vitamina B")
                der_base = sum(al[n]["energia"] * g / 100 for n, g in coincide["gramos"].items())
                factor = datos.der_objetivo / der_base if der_base else 1.0
                gramos_r = {}
                for n, g in coincide["gramos"].items():
                    a = al.get(n, {})
                    if a.get("categoria") in SUP_COMERCIALES:
                        techo = dosis_maxima_fabricante(a, datos.peso_perro_kg)
                        gramos_r[n] = round(min(g * factor, techo), 2) if techo else round(g * factor, 2)
                    else:
                        gramos_r[n] = round(g * factor, 2)
                ficha_r = verificar_v2(gramos_r, al, req, datos.der_objetivo, datos.etapa_requisitos)
                if ficha_r["semaforo"] == "verde" and _menu_precalculado_es_seguro(
                        gramos_r, al, datos.der_objetivo, datos.peso_perro_kg):
                    problemas_r = _seguridad_completa(gramos_r, al, datos.der_objetivo,
                                                       datos.etapa_requisitos, datos.patologias,
                                                       peso_perro_kg=datos.peso_perro_kg)
                    return {
                        "factible": True, "menu": gramos_r, "ficha": ficha_r,
                        "problemas_seguridad": problemas_r,
                        "kcal_total": sum(al[n]["energia"] * g / 100 for n, g in gramos_r.items()),
                        "gramos_total": sum(gramos_r.values()),
                        "via_catalogo": True,
                    }
                # si al reescalar por las kcal reales sale de verde pero viola alguno
                # de los 5 límites de seguridad crónica (o directamente no sale verde),
                # se sigue abajo con Personalizar normal, resolviendo en vivo.
                # sigue abajo con Personalizar normal, resolviendo en vivo.

    # ⚠️ AÑADIDO (5 agosto, madrugada) — PEDIDO EXPRESO: si en
    # Personalizar el usuario elige 1-2 carnes (o pescados, o huesos
    # carnosos), antes el motor podía añadir OTRA especie de esa misma
    # categoría sin que hiciera falta, solo porque le convenía para
    # cuadrar algo -- el usuario nunca pidió esa tercera carne. Ahora se
    # restringe cada una de estas tres categorías a SOLO lo elegido a
    # mano (dejando los gramos libres, eso sí), y solo si con eso no hay
    # solución viable se cae a dejar que el motor añada más -- avisando
    # de qué tuvo que añadir, con el mismo criterio que ya se usa en
    # todos los demás avisos de esta app. Vísceras, hígado, verduras y
    # extras se quedan siempre libres, tal como se pidió.
    CATEGORIAS_A_RESTRINGIR = ("Carne muscular", "Pescados y mariscos", "Hueso carnoso")

    def _restriccion_desde_elegidos(nombres):
        restringir = {}
        for n in nombres:
            cat = al.get(n, {}).get("categoria")
            if cat in CATEGORIAS_A_RESTRINGIR:
                restringir.setdefault(cat, []).append(n)
        return restringir

    if datos.modo == "personalizar":
        forzar = list(datos.forzar_presencia or datos.nombres_alimentos or [])
    elif datos.modo == "aprovechar":
        preferir = list(datos.nombres_alimentos or [])
    elif datos.modo == "automatico" and not excluidos and not datos.patologias and not datos.categorias_excluidas:
        # ⚠️ AÑADIDO (5 agosto, madrugada) — VARIANTES PRE-RESUELTAS: caso
        # real encontrado con datos exactos de producción -- resolver un
        # menú en caliente con una proteína evitada tardó 19,4 segundos
        # en el servidor real (confirmado con las herramientas de
        # desarrollador del navegador), demasiado cerca del límite de
        # 30s de Render. En vez de resolver nada, si hay variantes
        # pre-calculadas para este tamaño y etapa, se sirve directamente
        # la primera cuya proteína NO esté en evitar_especies -- al
        # instante, sin resolver, igual que ya hacía el primer menú con
        # la vía rápida, pero ahora para CUALQUIER menú de la sesión,
        # no solo el primero. Solo se reescala por las kcal reales del
        # perro (los suplementos comerciales se topan aparte por su
        # dosis real, igual que ya hace /catalogo).
        from catalogo_menus import CATALOGO_VARIANTES
        clave_variantes = f"{datos.tamano}_{datos.etapa_requisitos}" if datos.tamano else None
        variantes = CATALOGO_VARIANTES.get(clave_variantes) if clave_variantes else None
        if variantes:
            evitar_lower = {e.strip().lower() for e in (datos.evitar_especies or [])}
            elegida = next((v for v in variantes if v["proteina"].strip().lower() not in evitar_lower), None)
            if elegida is None:
                elegida = variantes[0]  # si ya se evitaron todas, se repite alguna antes que fallar
            SUP_COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                               "Calcio", "Hierro", "Vitamina B")
            der_base = sum(al[n]["energia"] * g / 100 for n, g in elegida["gramos"].items())
            factor = datos.der_objetivo / der_base if der_base else 1.0
            gramos_reescalados = {}
            for n, g in elegida["gramos"].items():
                a = al.get(n, {})
                if a.get("categoria") in SUP_COMERCIALES:
                    techo = dosis_maxima_fabricante(a, datos.peso_perro_kg)
                    gramos_reescalados[n] = round(min(g * factor, techo), 2) if techo else round(g * factor, 2)
                else:
                    gramos_reescalados[n] = round(g * factor, 2)
            ficha_variante = verificar_v2(gramos_reescalados, al, req, datos.der_objetivo, datos.etapa_requisitos)
            if ficha_variante["semaforo"] == "verde" and _menu_precalculado_es_seguro(
                    gramos_reescalados, al, datos.der_objetivo, datos.peso_perro_kg):
                problemas_variante = _seguridad_completa(gramos_reescalados, al, datos.der_objetivo,
                                                          datos.etapa_requisitos, datos.patologias,
                                                          peso_perro_kg=datos.peso_perro_kg)
                return {
                    "factible": True, "menu": gramos_reescalados, "ficha": ficha_variante,
                    "problemas_seguridad": problemas_variante,
                    "kcal_total": sum(al[n]["energia"] * g / 100 for n, g in gramos_reescalados.items()),
                    "gramos_total": sum(gramos_reescalados.values()),
                    "via_catalogo": True,
                }
            # si al reescalar por las kcal del perro concreto (no el peso
            # representativo del catálogo) se sale de verde, o viola alguno
            # de los 5 límites de seguridad crónica, se sigue abajo con el
            # camino normal -- nunca se entrega algo que no esté en verde
            # de verdad ni que se salte un límite de seguridad.

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
        # ⚠️ CORREGIDO (5 agosto, madrugada) — FALLO GRAVE ENCONTRADO,
        # confirmado con datos reales: esta vía fuerza SIEMPRE la MISMA
        # base fija (la que se guardó una vez, hace días) -- no tiene en
        # cuenta evitar_especies en absoluto. Si el atajo nuevo de
        # variantes (arriba) no llegaba a verde al reescalar, caía AQUÍ
        # como siguiente intento, y como esto es determinista, el menú 2
        # y el 3 daban EXACTAMENTE el mismo resultado -- mismos
        # alimentos, solo cambiaban los gramos totales por el reescalado.
        # Caso real confirmado: perfil adulto, menú 2 y 3 idénticos.
        # Ahora, si hay algo que evitar (no es el primer menú de la
        # sesión), esta vía NO se usa -- se salta directa a la búsqueda
        # libre de abajo, que sí respeta evitar_especies de verdad.
        clave = f"{datos.tamano}_{datos.etapa_requisitos}" if (datos.tamano and not datos.evitar_especies) else None
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
                    presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
                )
                if not ok_rapido:
                    break
                ficha_rapida = verificar_v2(gramos_rapido, al, req, datos.der_objetivo, datos.etapa_requisitos)
                if ficha_rapida["semaforo"] == "verde":
                    problemas_rapido = _seguridad_completa(gramos_rapido, al, datos.der_objetivo,
                                                            datos.etapa_requisitos, datos.patologias,
                                                            peso_perro_kg=datos.peso_perro_kg)
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

    # ⚠️ REESTRUCTURADO (5 agosto, madrugada) — PEDIDO EXPRESO: antes
    # había solo dos niveles (forzar lo elegido, o libre total si eso
    # fallaba). Ahora hay TRES, cada vez menos restrictivo, para poder
    # intentar primero "solo lo que elegiste en carne/pescado/hueso" sin
    # tener que renunciar a la solidez de que, si de verdad no cabe, el
    # menú se siga generando igual (con aviso), en vez de fallar del
    # todo.
    def _intentar_generacion(forzar_este, restringir_a_elegidos_este):
        """Un intento completo: llamada + reintentos para mejorar a
        verde mientras quede presupuesto de tiempo -- misma lógica que
        ya existía, solo que reutilizable para los tres niveles."""
        ok_i, gramos_i = resolver_v2(
            datos.der_objetivo, datos.etapa_requisitos, al, req,
            datos.peso_perro_kg, dosis_maxima_fabricante,
            excluidos=excluidos or None,
            margenes_categoria=MARGENES_V2, max_suplementos=2, time_limit=tiempo_restante(),
            forzar=forzar_este, preferir=preferir,
            patologias=datos.patologias, restringir_especie=datos.restringir_especie,
            peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
            evitar_especies=datos.evitar_especies,
            restringir_a_elegidos=restringir_a_elegidos_este,
            categorias_excluidas=datos.categorias_excluidas,
            presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
        )
        ficha_i = None
        while ok_i and time.time() - t_inicio_total < PRESUPUESTO_SEGUNDOS:
            ficha_i = verificar_v2(gramos_i, al, req, datos.der_objetivo, datos.etapa_requisitos)
            if ficha_i["semaforo"] == "verde":
                break
            ok2, gramos2 = resolver_v2(
                datos.der_objetivo, datos.etapa_requisitos, al, req,
                datos.peso_perro_kg, dosis_maxima_fabricante,
                excluidos=excluidos or None,
                margenes_categoria=MARGENES_V2, max_suplementos=2, time_limit=tiempo_restante(),
                forzar=forzar_este, preferir=preferir,
                patologias=datos.patologias, restringir_especie=datos.restringir_especie,
                peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
                evitar_especies=datos.evitar_especies,
                restringir_a_elegidos=restringir_a_elegidos_este,
                categorias_excluidas=datos.categorias_excluidas,
                presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
            )
            if ok2:
                ok_i, gramos_i = ok2, gramos2
            else:
                break
        return (ok_i and ficha_i and ficha_i["semaforo"] == "verde"), gramos_i, ficha_i

    aviso_extra_carne = None
    if datos.modo == "personalizar" and forzar:
        restriccion = _restriccion_desde_elegidos(forzar)
    else:
        restriccion = None

    if restriccion:
        # NIVEL 1: solo lo elegido a mano en carne/pescado/hueso, nada más
        ok, gramos, ficha_intento = _intentar_generacion(forzar, restriccion)
        if not ok:
            # NIVEL 2: se afloja la restricción de especie, pero se
            # sigue forzando que lo elegido esté presente -- el motor
            # puede añadir OTRA especie más si de verdad hace falta
            ok, gramos, ficha_intento = _intentar_generacion(forzar, None)
            if ok:
                # ⚠️ aviso solo si de verdad se añadió algo que el
                # usuario no pidió en esas categorías -- comparando
                # contra lo que se le pidió mantener EXCLUSIVO
                elegidos_restringidos = [n for lista in restriccion.values() for n in lista]
                anadidos = [n for n in gramos
                           if al.get(n, {}).get("categoria") in CATEGORIAS_A_RESTRINGIR
                           and n not in elegidos_restringidos]
                if anadidos:
                    aviso_extra_carne = (
                        "Con solo lo que elegiste no había una combinación viable, así que "
                        "también se ha añadido: " + ", ".join(anadidos) + "."
                    )
    else:
        ok, gramos, ficha_intento = _intentar_generacion(forzar, None)

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
            presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
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
    problemas_seguridad = _seguridad_completa(gramos, al, datos.der_objetivo,
                                               datos.etapa_requisitos,
                                               datos.patologias,
                                               peso_perro_kg=datos.peso_perro_kg)
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
    # ⚠️ AÑADIDO (5 agosto, madrugada) — PEDIDO EXPRESO: si hubo que
    # añadir alguna especie extra en carne/pescado/hueso más allá de lo
    # elegido a mano, se avisa aquí -- distinto de "no_se_pudo_forzar"
    # (que es cuando NADA de lo elegido se pudo mantener); esto es "casi
    # todo se mantuvo, pero hizo falta una cosa más".
    if aviso_extra_carne:
        resultado["aviso"] = aviso_extra_carne
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
def _recalcular_con_motor(datos, forzar=None, excluir_nombres=None, restringir_especie=None):
    al, req = cargar_v2()
    excluidos = list(datos.especies_excluidas or [])
    nombres_excl = set(datos.nombres_excluidos or [])
    if excluir_nombres:
        nombres_excl |= set(excluir_nombres)

    def _intentar(forzar_este, margen_intentos=3):
        """Un intento completo: hasta 3 vueltas hasta que sea verde de
        verdad, igual que ya hacía esto antes de separarlo en función."""
        ok, gramos, ficha = False, None, None
        for _intento in range(margen_intentos):
            ok, gramos = resolver_v2(
                datos.der_objetivo, datos.etapa_requisitos, al, req,
                datos.peso_perro_kg, dosis_maxima_fabricante,
                excluidos=(excluidos + list(nombres_excl)) or None,
                margenes_categoria=MARGENES_V2, max_suplementos=2,
                forzar=forzar_este,
                restringir_especie=restringir_especie,
                peso_adulto_esperado_kg=getattr(datos, "peso_adulto_esperado_kg", None),
                categorias_excluidas=getattr(datos, "categorias_excluidas", None),
            )
            if not ok:
                break
            ficha = verificar_v2(gramos, al, req, datos.der_objetivo, datos.etapa_requisitos)
            if ficha["semaforo"] == "verde":
                break
        return (ok and ficha and ficha["semaforo"] == "verde"), gramos, ficha

    # ⚠️ AÑADIDO (5 agosto, madrugada) — PEDIDO EXPRESO: antes, editar UN
    # alimento dejaba que el motor reconstruyera el menú ENTERO desde
    # cero, libre de usar lo que quisiera para el resto -- aunque el
    # resultado fuera nutricionalmente correcto, podía cambiar TODO lo
    # demás sin necesidad, cuando lo único que el usuario pedía era UN
    # cambio puntual. Ahora se intenta PRIMERO mantener todos los demás
    # alimentos que ya había (dejando que gramos, extras y suplementos
    # se ajusten libres) -- solo si eso no da un menú viable, se cae al
    # comportamiento de antes (el motor elige libremente), avisando de
    # qué otros alimentos tuvo que cambiar además del pedido.
    menu_actual = list(getattr(datos, "menu_actual", None) or [])
    aviso_cambios_extra = None
    # ⚠️ CORREGIDO en el mismo momento: esto solo se activaba si había
    # "forzar" (cambiar/añadir un alimento) -- al QUITAR uno, forzar es
    # None, así que "preservar el resto" nunca se activaba ahí, cuando
    # es exactamente el mismo caso: quitar algo también debería intentar
    # mantener todo lo demás, dejando que el motor rellene el hueco.
    if menu_actual and (forzar or excluir_nombres):
        # ⚠️ CORREGIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO: "Sal
        # común" desaparecía al editar OTRO alimento, sin ningún aviso.
        # Motivo: "Extras" estaba en esta lista de categorías "libres de
        # perderse sin avisar" -- pensada para los suplementos que el
        # MOTOR elige solo (multivitamínico, omega-3...), no para
        # ingredientes concretos que la usuaria puso a mano con su
        # propio nombre, como la sal o un aceite específico. Esos
        # merecen el mismo trato que la carne o la verdura: se intenta
        # preservarlos, y si no se puede, se avisa de que se perdieron.
        SUP_CATS = ("Multivitamínico", "Omega-3", "Yodo", "Fibra", "Calcio",
                   "Hierro", "Vitamina B")
        nombres_excl_actuales = nombres_excl | set(forzar or [])
        a_preservar = [n for n in menu_actual
                      if n not in nombres_excl_actuales
                      and al.get(n, {}).get("categoria") not in SUP_CATS]
        if a_preservar:
            ok_pres, gramos_pres, ficha_pres = _intentar(list(forzar or []) + a_preservar)
            if ok_pres:
                resultado = {"factible": True, "gramos": gramos_pres, "ficha": ficha_pres}
                # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL: esta
                # función nunca calculaba avisos de seguridad, en
                # NINGUNO de sus caminos -- se perdían al editar,
                # aunque sí funcionaran al generar por primera vez.
                resultado["problemas_seguridad"] = _seguridad_completa(
                    gramos_pres, al, datos.der_objetivo, datos.etapa_requisitos, datos.patologias,
                    peso_perro_kg=datos.peso_perro_kg)
                return resultado
            # no se pudo manteniendo todo -- se sigue abajo con el
            # comportamiento libre, y se avisa de qué se perdió
            ok_libre, gramos_libre, ficha_libre = _intentar(forzar)
            if ok_libre:
                perdidos = [n for n in a_preservar if n not in gramos_libre]
                if perdidos:
                    aviso_cambios_extra = (
                        "Para que este cambio funcionara, también tuvimos que cambiar: "
                        + ", ".join(perdidos) + "."
                    )
                resultado = {"factible": True, "gramos": gramos_libre, "ficha": ficha_libre}
                if aviso_cambios_extra:
                    resultado["aviso"] = aviso_cambios_extra
                resultado["problemas_seguridad"] = _seguridad_completa(
                    gramos_libre, al, datos.der_objetivo, datos.etapa_requisitos, datos.patologias,
                    peso_perro_kg=datos.peso_perro_kg)
                return resultado
            ok, gramos, ficha = ok_libre, gramos_libre, ficha_libre
        else:
            ok, gramos, ficha = _intentar(forzar)
    else:
        ok, gramos, ficha = _intentar(forzar)

    if not ok:
        return {"factible": False,
                "motivo": "Con este cambio no existe ninguna combinación que cumpla "
                          "los 30 requisitos. Prueba con otro alimento."}
    return {
        "factible": True, "gramos": gramos, "ficha": ficha,
        "problemas_seguridad": _seguridad_completa(
            gramos, al, datos.der_objetivo, datos.etapa_requisitos, datos.patologias,
            peso_perro_kg=datos.peso_perro_kg),
    }


@app.post("/menu/cambiar")
def endpoint_cambiar_alimento(datos: PeticionCambiarAlimento):
    """Sustituye un alimento por otro (el lapiz de editar), resolviendo TODO
    de nuevo con el motor real -- el alimento nuevo se fuerza a entrar."""
    # ⚠️ AÑADIDO (5 agosto, madrugada): "Todo el/la {especie}" ahora
    # también funciona aquí, no solo al elegir por primera vez -- antes
    # solo se podía restringir a una especie completa en Personalizar,
    # nunca al editar un alimento ya puesto en el menú.
    if datos.alimento_nuevo.startswith("Todo: "):
        especie = datos.alimento_nuevo[len("Todo: "):]
        al, _ = cargar_v2()
        categoria = al.get(datos.alimento_viejo, {}).get("categoria")
        if categoria:
            return _recalcular_con_motor(datos, excluir_nombres=[datos.alimento_viejo],
                                         restringir_especie={categoria: especie})
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
    # ⚠️ CORREGIDO (5 agosto, noche): mismo fallo que en PeticionMenu --
    # tipo estricto con default None en vez de Optional, rechazaba con
    # 422 cualquier petición que mandara null explícito.
    gramos_por_alimento: dict   # {"Carcasa de pollo": 680, "Calabaza": 68, ...}
    der_objetivo: Optional[float] = None  # si no viene, se calcula con peso/etapa/actividad
    etapa_requisitos: str = "Adulto"
    # alternativa a mandar el DER ya calculado: mandar el perfil del perro
    peso_kg: Optional[float] = None
    etapa_der: Optional[str] = None       # clave de der.py: adulto, cachorro_crecimiento...
    actividad: Optional[str] = None
    esterilizado: bool = False
    # Datos del metodo europeo. Sin ellos el DER sale con valores prudentes,
    # pero para un CACHORRO el peso adulto esperado es lo que decide el tramo
    # (hasta 50% / 50-80% / desde 80%), asi que conviene mandarlo siempre.
    peso_adulto_esperado_kg: Optional[float] = None
    peso_ideal_kg: Optional[float] = None
    convivencia: str = "solo"
    macho_entero: bool = False
    raza: Optional[str] = None
    semana_gestacion: Optional[int] = None
    n_cachorros: Optional[int] = None
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
    """
    ⚠️ CORREGIDO (5 agosto, madrugada) — FALLO DE DISEÑO ENCONTRADO: los
    JSON se comparaban por hash de los BYTES CRUDOS del archivo -- eso
    hace que cualquier diferencia de FORMATO de texto (otro orden de
    líneas al guardar, otro tipo de salto de línea, indentación
    distinta) dé "NO COINCIDE" aunque los DATOS sean idénticos, porque
    json.load() no le importa el formato, solo la estructura. Esto dio
    una falsa alarma real: un archivo con los datos correctos pareció
    "alterado" solo por cómo se había guardado el texto. Ahora, para los
    JSON, se compara el CONTENIDO real (cargado y reordenado de forma
    canónica antes de hashear) -- invariante al formato, sensible a
    cualquier cambio real de datos. der.py sigue comparando bytes
    crudos porque es código, donde eso sí puede importar.
    """
    import hashlib, os, json
    SELLOS = {
        "alimentos_v3_final.json":      "230bb7378b9e97ec",
        "requerimientos_v2_final.json": "7b023fcdebdd4391",
    }
    SELLOS_CRUDOS = {
        "der.py": "1c5c8bb91ceac481",
    }
    base = os.path.dirname(os.path.abspath(__file__))
    detalle, todo_ok = [], True
    for fichero, esperado in SELLOS.items():
        ruta = os.path.join(base, fichero)
        if not os.path.exists(ruta):
            detalle.append({"archivo": fichero, "estado": "NO EXISTE"})
            todo_ok = False
            continue
        try:
            datos = json.load(open(ruta, encoding="utf-8"))
            canonico = json.dumps(datos, sort_keys=True, ensure_ascii=True).encode("utf-8")
            actual = hashlib.sha256(canonico).hexdigest()[:16]
        except Exception as e:
            detalle.append({"archivo": fichero, "estado": f"NO SE PUDO LEER COMO JSON: {e}"})
            todo_ok = False
            continue
        ok = actual == esperado
        todo_ok = todo_ok and ok
        detalle.append({
            "archivo": fichero,
            "esperado": esperado,
            "encontrado": actual,
            "estado": "correcto (contenido real, no formato de texto)" if ok else "EL CONTENIDO NO COINCIDE — esto sí es un cambio de datos real",
        })
    for fichero, esperado in SELLOS_CRUDOS.items():
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

    # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL: nunca había forma de
    # confirmar que Render estuviera sirviendo la versión de main.py
    # que se acababa de subir, sin pegar el archivo entero para
    # comparar a mano. No se compara contra un "esperado" fijo (eso
    # sería un archivo intentando conocerse a sí mismo antes de
    # guardarse -- una paradoja) -- simplemente se MUESTRA el sello
    # real de este main.py, tal como está corriendo ahora mismo, junto
    # con desde cuándo lleva encendido el proceso. Si acabas de subir
    # cambios y "arrancado_en" es de hace horas, el despliegue no se
    # ha aplicado todavía -- fuérzalo a mano desde el panel de Render.
    hash_main = hashlib.sha256(open(__file__, "rb").read()).hexdigest()[:16]

    return {
        "ok": todo_ok,
        "resumen": ("Los tres pilares estan intactos" if todo_ok
                    else "ALGO NO CUADRA — revisa el detalle y vuelve a subir el archivo"),
        "alimentos_cargados": n_alimentos,
        "detalle": detalle,
        "arrancado_en": _ARRANCADO_EN,
        "sello_main_py_actual": hash_main,
    }


@app.post("/menu/verificar_semana")
def endpoint_verificar_semana(datos: PeticionVerificarSemana):
    """⚠️ AÑADIDO (5 agosto, madrugada) — pedido expreso: comprueba el
    aporte de tiaminasa, mercurio, vitamina D, yodo y selenio a lo
    largo de TODA la semana de rotación (todos los menús generados
    juntos, ponderados por sus días), no solo dentro de un menú
    aislado -- ver revisar_seguridad_semanal."""
    from seguridad import revisar_seguridad_semanal
    al, req = cargar_v2()
    menus_con_dias = [(m.gramos, m.dias) for m in datos.menus]
    avisos = revisar_seguridad_semanal(menus_con_dias, al, datos.der_objetivo,
                                       peso_perro_kg=datos.peso_perro_kg)
    return {"avisos_semana": avisos}


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
