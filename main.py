"""
Rawku - API del motor nutricional BARF

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
from requisitos import ETAPAS_VALIDAS, dosis_maxima_fabricante
from transicion import calcular_tramo_transicion, menu_activo_y_bloqueados, nivel_indicador_nutrientes
from analizador import analizar_dieta
import persistencia

# ⚠️ EL MOTOR NUEVO (5 agosto) — programación lineal entera mixta, decide
# QUÉ alimentos usar Y cuánto de cada uno a la vez, comprobado contra los
# 30 requisitos de FEDIAF de forma EXACTA (no heurística). Vive en
# ./motor/ y NO sustituye a /menu todavía: se añade como /menu/v2 para
# poder comparar los dos antes de decidir el cambio definitivo.
from motor_completo import resolver as resolver_v2, especie_de
# PATOLOGIAS: los topes por patología, para poder comprobarlos también
# en la puerta de verificación (ver _tope_patologia_roto).
from constructor import tabla_imputacion_maximos, valor_para_maximo, valor_nutriente
from motor_completo import PATOLOGIAS, topes_de_patologias, RAZA_GRANDE_O_GIGANTE_KG
from exclusiones import filtrar as filtrar_exclusiones
from constructor import cargar as cargar_v2, MARGENES as MARGENES_V2
from verificar import verificar as verificar_v2
from verificar import (peso_objetivo_desde_bcs, BCS_ESCALA_SATURADA,
                       BCS_NEUTRO as BCS_NEUTRO_MAIN)
# ⚠️ El DER por kg de peso metabólico, que es lo que dispara el escalado de los
# mínimos. Se importa de `verificar` y no se recalcula aquí: es el único sitio
# que sabe hacerlo, y dos copias de esta cuenta serían dos criterios.
from verificar import der_efectiva_de
from seguridad import revisar_seguridad as revisar_seguridad_v2
from seguridad import avisos_rotacion as avisos_rotacion_v2

# ⚠️ CÓMO SE ESCRIBE UN NUTRIENTE EN UN MENSAJE (8 septiembre).
#
# Lo necesita el diagnóstico de choque entre patologías, que tiene que
# escribir «el fósforo de la renal, 1200 mg por cada 1000 kcal» a partir de
# la clave interna `fosforo`. Se DERIVA del `MAPA` del verificador y de la
# tabla de FEDIAF, nunca se escribe a mano: una lista de nombres copiada es
# exactamente el fallo del que avisa la regla 5 del CLAUDE.md -- el día que
# se añada un nutriente, una lista a mano se queda corta EN SILENCIO y el
# mensaje enseña la clave interna al veterinario.
_NOMBRE_NUTRIENTE = {}
_UNIDAD_DE = {}
# ⚠️ LA TABLA DE FEDIAF, CARGADA UNA VEZ AL ARRANCAR Y COMPARTIDA (10 sep). Ya se
# leia aqui para el nombre y la unidad de cada nutriente; ahora tambien la usa
# `_seguridad_completa` para saber el maximo de calcio sin volver a cargar el
# fichero en cada peticion ni tener una segunda copia. Si la carga falla, se
# queda en None y el aviso que depende de ella simplemente no sale.
_REQ_FEDIAF = None
try:
    from verificar import MAPA as _MAPA_NUTRIENTES
    # `cargar_v2()` devuelve los requisitos como dict indexado por el nombre
    # de FEDIAF, que es la misma clave que usa el MAPA del verificador.
    _, _req_unidades = cargar_v2()
    _REQ_FEDIAF = _req_unidades
    for _fediaf, _clave in _MAPA_NUTRIENTES.items():
        _NOMBRE_NUTRIENTE[_clave] = _fediaf.replace("_", " ").lower()
        _u = (_req_unidades.get(_fediaf) or {}).get("unidad") or ""
        _UNIDAD_DE[_clave] = "" if _u == "ratio" else _u
except Exception as _e:   # nunca puede impedir que arranque la API
    print(f"[aviso] no se pudo montar el nombre legible de los nutrientes: {_e}")


def _num_bonito(v):
    """1200.0 -> «1200»; 14.1875 -> «14,19». Para texto, no para cálculo."""
    try:
        f = float(v)
    except (TypeError, ValueError):
        return str(v)
    if abs(f - round(f)) < 1e-9:
        return str(int(round(f)))
    return f"{f:.2f}".replace(".", ",")

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
    # ⚠️ AQUI SOLO VA LO QUE TIENE QUE VER EL DUEÑO (10 septiembre, corregido el
    # mismo dia). Esta lista sale por `problemas_seguridad`, y la app la pinta
    # en las DOS vistas -- la del dueño y la del profesional --, asi que lo que
    # se meta aqui lo lee todo el mundo.
    #
    # La SEGUNDA lista que devuelve `revisar_seguridad` (`avisos`) NO va aqui:
    # son notas de interpretacion clinica -- «puede hacer falta mas zinc»,
    # «conviene mirar la taurina en sangre» -- y decirle eso a alguien que solo
    # quiere alimentar bien a su perro es ruido que ademas asusta. Elena, hoy:
    # «esos avisos nunca tiene que verlos un usuario, solo un veterinario».
    #
    # Van por `avisos_profesional`, y se ponen en UN SOLO SITIO: dentro de
    # `_garantizar_verificado`, que es por donde pasa TODO menu antes de salir
    # (regla 1). Asi no hay once sitios que acordarse de tocar.
    problemas = list(revisar_seguridad_v2(gramos, al, der, etapa, patologias,
                                          peso_perro_kg=peso_perro_kg) or [])
    problemas += list(avisos_rotacion_v2(gramos, al) or [])
    # ⚠️ AÑADIDO (25 agosto) — CASO REAL ENCONTRADO: un cachorro con
    # pancreatitis recibía su menú con el tope de grasa QUITADO y sin que
    # nadie se lo dijera. El tope de 20 g/1000 kcal no se puede aplicar en
    # crecimiento (el mínimo que FEDIAF exige ahí, 21,25 g, es MAYOR que el
    # tope), así que soltarlo es correcto -- pero callárselo no lo es.
    #
    # El aviso ya existía: `topes_de_patologias` lo devuelve como tercer
    # valor. Solo que en el motor se recogía en `_avisos_pat` y se tiraba, y
    # aquí no se pedía. O sea que la regla de "se baja de peldaño y SE DICE"
    # se cumplía para las proporciones del BARF y se saltaba justo para un
    # tope clínico, que es donde más importa.
    #
    # Va por `problemas_seguridad` a propósito: es el canal que la app ya
    # pinta en TODOS los caminos (generar, semana, varios perros, editar,
    # revalidar), así que con ponerlo en esta función sale en los ocho
    # sitios sin tocar la app ni añadir una clave nueva que alguien tenga
    # que acordarse de leer.
    _topes, _pct, avisos_por_la_etapa, _suelos = topes_de_patologias(patologias, etapa)
    problemas += avisos_por_la_etapa
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
        TOPE_VITD_KCAL, TOPE_VITD_KG075, TOPE_YODO_KCAL, TOPE_SELENIO_KCAL,
        TOPE_YODO_KG075, TOPE_SELENIO_KG075, _es,
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
    # ⚠️ EL PERRO DE TRABAJO (11 septiembre): el yodo y el selenio se topan
    # también por PESO METABÓLICO, igual que la vitamina D dos bloques arriba.
    # Un tope por energía deja pasar el doble a quien come el doble, y NRC 2006
    # cap.11 dice que el invariante es el de peso. El filtro final tiene que
    # mirar lo mismo que el solver o construiría menús que él mismo rechaza --
    # que es la lección del 8 de septiembre con los suelos de patología.
    tope_yodo = TOPE_YODO_KCAL * der / 1000.0
    if peso_perro_kg and peso_perro_kg > 0:
        tope_yodo = min(tope_yodo, TOPE_YODO_KG075 * (peso_perro_kg ** 0.75))
    if yodo_ug > tope_yodo:
        return False

    # ⚠️ El selenio se topa POR ENERGÍA y no por peso de comida. Antes iba
    # a 2 µg por gramo de dieta, que es el número de Merck pero en base
    # MATERIA SECA aplicado sobre el peso fresco: con un 70-75% de agua,
    # eso dejaba pasar entre tres y cuatro veces el límite real. Ver
    # TOPE_SELENIO_KCAL en seguridad.py.
    selenio_ug = sum(al.get(n, {}).get("nutrientes", {}).get("selenio", 0) * g / 100.0 for n, g in gramos.items())
    tope_selenio = TOPE_SELENIO_KCAL * der / 1000.0
    if peso_perro_kg and peso_perro_kg > 0:
        tope_selenio = min(tope_selenio, TOPE_SELENIO_KG075 * (peso_perro_kg ** 0.75))
    if selenio_ug > tope_selenio:
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
# =====================================================================
# ⚠️ AÑADIDO (20 agosto) — EL ÚNICO PUNTO POR EL QUE SALE UN MENÚ
#
# CASO REAL ENCONTRADO AUDITANDO: hasta ahora, "el menú siempre está
# verificado" dependía de que CADA camino se acordara de comprobarlo por
# su cuenta. La mayoría lo hacía. Tres no:
#
#   1. /catalogo servía un menú pre-calculado y reescalado comprobando
#      SOLO los 5 límites de seguridad crónica -- nunca los 30
#      requisitos de FEDIAF ni el ratio Ca:P.
#   2. /menu (el motor viejo) hacía exactamente lo mismo: pasaba por
#      _menu_precalculado_es_seguro y se entregaba, sin verificar_v2.
#   3. Dentro de /menu/v2, el reintento libre de "personalizar" (cuando
#      forzar lo elegido a mano no da solución) llama a resolver_v2 y
#      devuelve el resultado SIN mirar el semáforo, a diferencia de
#      todos los demás caminos, que exigen verde. Que ese reintento
#      exista, y que los otros reintenten hasta 3 veces "hasta que sea
#      verde", demuestra que el solver por sí solo no siempre sale verde.
#
# El fallo de fondo es de diseño, no de despiste: una garantía que hay
# que acordarse de aplicar en N sitios se rompe en cuanto aparece el
# sitio N+1. Esta función es ese sitio único. Cualquier endpoint que
# devuelva un menú lo pasa por aquí, y aquí se verifica de cero contra
# los 30 requisitos + Ca:P + los límites de seguridad, venga de donde
# venga. Si no está verde, NO se entrega: se devuelve "no factible".
#
# Preferimos no dar menú a dar uno que no cumple. Ese es el trato.
# =====================================================================
# ⚠️ AÑADIDO (20 agosto) — CUMPLIR NO ES LO MISMO QUE SER DABLE.
# Encontrado midiendo la escalera de relajación: soltando el MÁXIMO de
# verdura, el motor resolvía un cachorro de 10 kg con 3,1 kg de canónigos
# más 1,2 kg de espinaca -- 4,7 kg de comida al día, el 47% del peso del
# perro. Verde en los 30 requisitos, y físicamente imposible de dar.
#
# El truco es que las kcal SÍ están atadas al DER, pero la hoja verde
# tiene tan poca energía que se puede apilar volumen sin pasarse de
# calorías. Hasta ahora lo único que lo impedía era, de rebote, el tope
# del 10% de verdura -- una protección accidental, no buscada.
#
# Medido sobre los menús reales de 21 combinaciones de peso y etapa: van
# del 1,66% del peso del perro (senior de 60 kg) al 13% (cachorro de
# 1,5 kg, que come mucho para su tamaño). El tope se pone al 25%: casi el
# doble del peor caso legítimo, así que no puede saltar por un menú
# normal, y corta en seco cualquier cosa como la de los canónigos.
TOPE_GRAMOS_SOBRE_PESO = 0.25


def _valor_num(v):
    """Un nutriente puede venir como número, como texto o como None (dato que
    no tenemos). Solo cuenta si es un número de verdad."""
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def _tope_patologia_roto(gramos, al, patologias, etapa="Adulto",
                         req=None, der_efectiva=None,
                         peso_adulto_esperado_kg=None):
    """¿Este menú se pasa de algún tope por patología? Devuelve la lista de
    los que se pasa, vacía si está bien.

    ⚠️ AÑADIDO (24 agosto) — SEGUNDA CAPA, y hace falta.

    El fallo que la motivó: editar el menú de un perro renal daba 3084 mg de
    fósforo con el tope en 1400, y el menú SALÍA IGUAL. La causa era que el
    camino de edición no le pasaba las patologías al motor (arreglado), pero
    lo que dejó pasar el menú fue esto: `verificar_v2` comprueba los 30
    requisitos de FEDIAF, que son los de un perro SANO. 3084 mg de fósforo
    está dentro del máximo de FEDIAF, así que el semáforo salía VERDE.

    Un perro renal no es un perro sano. Los topes por patología son duros
    (regla 2 del CLAUDE.md), así que tienen que comprobarse aquí también:
    si mañana otro camino se olvida de pasarlos, el menú no sale igualmente.

    Se mide sobre las kcal REALES del menú, no sobre las pedidas: es como se
    definen los topes y como se lo va a comer el perro.

    ⚠️ AMPLIADO (8 septiembre) — TAMBIÉN COMPRUEBA LOS TECHOS DEL PERRO ADULTO
    SANO (`motor/recomendaciones.py`): el fósforo y el sodio que SACN5
    recomienda para CUALQUIER adulto, tenga lo que tenga. Por eso ya no vale
    salirse cuando no hay ninguna patología marcada: el perro sin nada es
    justamente al que se le aplican.
    """
    if not gramos:
        return []
    kcal = sum((al.get(n, {}).get("energia", 0) or 0) / 100.0 * g
               for n, g in gramos.items())
    if kcal <= 0:
        return []

    # ⚠️ Los topes por patología son TECHOS, así que se miden con el mismo
    # criterio que los máximos de FEDIAF (28 agosto): un hueco del catálogo
    # no puede valer cero justo aquí. Un renal con el fósforo de un alimento
    # sin dato saldría por debajo del tope sin que nadie lo haya medido.
    _tabla_max = tabla_imputacion_maximos(al)

    def por_1000(clave):
        total = 0.0
        for n, g in gramos.items():
            v, _estado = valor_para_maximo(al.get(n, {}), clave, _tabla_max)
            total += v / 100.0 * g
        return total / kcal * 1000.0

    # Un pelo de margen (0,5%) por el redondeo de los gramos a 2 decimales:
    # el motor ya aprieta un 0,1% al construir la restricción, así que lo que
    # llegue por encima de esto no es redondeo, es un tope que no se aplicó.
    MARGEN = 1.005
    rotos = []
    # ⚠️ LOS MISMOS TOPES QUE USÓ EL SOLVER, resueltos por la misma función
    # (25 agosto). Si aquí se leyeran otra vez a mano de la tabla, esta
    # comprobación y la restricción podrían decir cosas distintas -- que es
    # exactamente lo que pasó entre el analizador y el semáforo con la fibra.
    topes, pct, _, suelos = topes_de_patologias(patologias, etapa)
    # ⚠️ Y LOS DEL PERRO SANO, con el mismo `min()` que usa el solver (8
    # septiembre). Tienen que resolverse EXACTAMENTE igual que allí o esta
    # comprobación y la restricción dirían cosas distintas, que es el fallo
    # que este bloque entero existe para no repetir.
    # ⚠️ CON `req` Y `der_efectiva` EL TECHO DEL LIBRO PUEDE CEDER, exactamente
    # igual que en el solver. Tienen que decidirlo con el MISMO criterio o esta
    # comprobación tiraría menús que el solver construyó bien: a DER 49 el
    # mínimo de fósforo de FEDIAF (2249) supera al techo del libro (2000), el
    # solver deja de aplicarlo y el menú sale con 2216 -- correcto. Sin
    # pasarle `req` aquí, este filtro lo rechazaría por «pasarse» de un techo
    # que ya no está puesto.
    # ⚠️ Y CON EL PESO ADULTO ESPERADO (9 septiembre), por lo mismo: los techos
    # de crecimiento tienen dos columnas segun el perro pase o no de 25 kg de
    # adulto. Si el solver aplica el de 2750 y este filtro midiera contra el de
    # 4250, el filtro dejaria pasar menus que el solver no habria construido --
    # y al reves, que es peor: tiraria menus buenos.
    from recomendaciones import topes_de_la_etapa as _topes_etapa
    _del_libro = set()
    for _clave_r, _valor_r in _topes_etapa(etapa, req, der_efectiva,
                                           peso_adulto_esperado_kg).items():
        _actual_r = topes.get(_clave_r)
        if _actual_r is None or _valor_r < _actual_r:
            topes[_clave_r] = _valor_r
            # Quién manda en este nutriente, para poder decirlo bien más abajo:
            # «por patología» sobre un techo que viene del libro sería mentira, y
            # a quien lo lee le mandaría a mirar la patología equivocada.
            _del_libro.add(_clave_r)
    for clave, tope in topes.items():
        v = por_1000(clave)
        if v > tope * MARGEN:
            _de = ("recomendado para el perro adulto sano" if clave in _del_libro
                   else "por patología")
            rotos.append(f"{clave} {v:.1f} (tope {tope:.1f} {_de})")

    # ⚠️ AÑADIDO (7 septiembre) — EL ESPEJO DEL CHEQUEO DE ARRIBA, PARA LOS
    # SUELOS. Sin margen de redondeo A FAVOR (al revés que el tope: aquí lo
    # que preocupa es quedarse CORTO, así que no se resta margen). Se usa
    # `valor_nutriente` sin imputar huecos -- lo contrario que el tope de
    # arriba, que imputa al percentil alto de la familia porque ahí el
    # hueco preocuparía si se contara de menos. En un suelo, un hueco
    # contado como algo que no se ha medido sería INFLAR el mínimo real;
    # contarlo como 0 es el lado seguro.
    def _por_1000_min(clave):
        total = 0.0
        for n, g in gramos.items():
            total += valor_nutriente(al.get(n, {}).get("nutrientes", {}), clave) / 100.0 * g
        return total / kcal * 1000.0

    # ⚠️ Y LOS SUELOS DEL LIBRO PARA EL PERRO SANO (11 septiembre), con el
    # mismo `max()` y la misma función que usa el solver. La vitamina E que
    # SACN5 pide a CUALQUIER adulto es un límite duro desde hoy, así que tiene
    # que comprobarse también aquí: la regla 2 no distingue entre un tope y un
    # suelo, distingue entre «lo mira el filtro final» y «no lo mira nadie».
    from recomendaciones import suelos_de_la_etapa as _suelos_libro
    _del_libro_suelo = set()
    for _clave_r3, _valor_r3 in _suelos_libro(etapa, req,
                                              peso_adulto_esperado_kg).items():
        _actual_r3 = suelos.get(_clave_r3)
        if _actual_r3 is None or _valor_r3 > _actual_r3:
            suelos[_clave_r3] = _valor_r3
            _del_libro_suelo.add(_clave_r3)

    # ⚠️ Y LOS SUELOS CONDICIONALES (8 septiembre, noche), con el mismo `max()`
    # que usa el solver: la proteína de gestación y lactancia, que FEDIAF calcula
    # suponiendo hidratos que una ración BARF no lleva. Si el solver lo exige y
    # este filtro no lo mirara, el hueco sería justo el de la regla 2 -- un menú
    # construido bien que nadie vuelve a comprobar.
    from condicionales import suelos_de_la_etapa as _suelos_cond
    for _clave_c, _valor_c in _suelos_cond(etapa).items():
        _actual_c = suelos.get(_clave_c)
        if _actual_c is None or _valor_c > _actual_c:
            suelos[_clave_c] = _valor_c
            _del_libro_suelo.add(_clave_c)

    MARGEN_SUELO = 0.995
    for clave, suelo in suelos.items():
        v = _por_1000_min(clave)
        if v < suelo * MARGEN_SUELO:
            _de_s = ("exigido por la etapa, no por una patología"
                     if clave in _del_libro_suelo else "por patología")
            rotos.append(f"{clave} {v:.1f} (suelo {suelo:.1f} {_de_s})")
    # ⚠️ AÑADIDO (10 septiembre) — LOS RATIOS QUE PIDE UNA PATOLOGÍA.
    #
    # Es el mismo agujero de siempre visto en un cociente: el semáforo comprueba
    # el Ca:P contra el rango de FEDIAF, que en adulto es 1,0-2,0, y la Tabla
    # 40-5 del oxalato pide 1,1-2,0. Un menú con 1,06 sale VERDE y está por
    # debajo de lo que pide la fuente para ese perro. Medido: pasaba en el perro
    # de 30 kg.
    #
    # Se mide con `valor_nutriente` -- el valor DECLARADO, sin imputar huecos --
    # y con el mismo 0,5 % de margen que usa el semáforo para este mismo ratio,
    # porque el solver construye su fila con exactamente estos números. Si aquí
    # se imputaran los huecos y allí no, este filtro tiraría menús que el solver
    # construyó bien: es la lección del 8 de septiembre, y en un cociente pesa el
    # doble porque el hueco puede caer en el numerador o en el denominador.
    from motor_completo import ratios_de_patologias as _ratios_pat
    for (_n_r, _d_r), _cotas_r in _ratios_pat(patologias, etapa).items():
        _tot_n = sum(valor_nutriente(al.get(n, {}).get("nutrientes", {}), _n_r) / 100.0 * g
                     for n, g in gramos.items())
        _tot_d = sum(valor_nutriente(al.get(n, {}).get("nutrientes", {}), _d_r) / 100.0 * g
                     for n, g in gramos.items())
        if _tot_d <= 0:
            continue
        _ratio_real = _tot_n / _tot_d
        if _cotas_r.get("min") is not None and _ratio_real < _cotas_r["min"] * 0.995:
            rotos.append(f"{_n_r}:{_d_r} {_ratio_real:.2f} "
                         f"(mínimo {_cotas_r['min']:.2f} por patología)")
        if _cotas_r.get("max") is not None and _ratio_real > _cotas_r["max"] * MARGEN:
            rotos.append(f"{_n_r}:{_d_r} {_ratio_real:.2f} "
                         f"(máximo {_cotas_r['max']:.2f} por patología)")

    if pct is not None:
        grasa_g = sum((_valor_num(al.get(n, {}).get("nutrientes", {}).get("grasa")) or 0.0) / 100.0 * g
                      for n, g in gramos.items())
        v = grasa_g * 9.0 / kcal
        if v > pct * MARGEN:
            rotos.append(f"grasa {v*100:.0f}% de las kcal (tope {pct*100:.0f}% por patología)")
    return rotos


# ⚠️ AÑADIDO (28 agosto) — TERCERA CAPA, misma familia que
# `_tope_patologia_roto`, y encontrada contando cuántos de los 43
# requisitos de la tabla se verifican de verdad.
#
# `Calcio_LateGrowth_RazaGrande` es el requisito 31: un cachorro de raza
# grande o gigante en crecimiento necesita un MÍNIMO de calcio más alto
# (2500 mg/1000 kcal en vez de los 2000 genéricos), porque no tiene margen
# para quedarse corto en la fase en que forma el hueso. Estaba puesto como
# restricción dura dentro del solver desde el 5 de agosto -- y SOLO ahí.
#
# El problema es el de siempre: `verificar()` no sabe qué raza es el perro,
# así que su semáforo mide contra el mínimo del cachorro genérico y sale
# VERDE con 2100 mg. Y hay al menos dos caminos que no pasan por esa
# restricción del solver: el menú del catálogo precalculado reescalado
# (que no resuelve nada) y la vía rápida de /menu/v2, que llamaba a
# `resolver_v2` sin `peso_adulto_esperado_kg` -- exactamente el mismo
# olvido que en su día tiró el tope de fósforo del renal en la edición.
#
# Medido antes de arreglarlo: 0 de 12 menús de cachorro de raza grande
# se quedaban por debajo de 2500 (salían entre 2618 y 4500), porque una
# dieta con hueso carnoso va sobrada de calcio por abajo -- el que aprieta
# es el techo. O sea: el agujero era real en el código y no estaba dando
# menús malos hoy. Se cierra igual, porque lo que lo mantenía tapado es
# una propiedad del catálogo de hoy, no una garantía.
def _minimo_calcio_raza_grande_roto(gramos, al, req, etapa, peso_adulto_esperado_kg):
    """¿Este menú se queda por debajo del mínimo de calcio REFORZADO de las
    razas grandes en crecimiento? Devuelve el texto del fallo, o None.

    Solo aplica a raza grande/gigante (peso adulto esperado >= 15 kg) y en
    crecimiento; para el resto, el mínimo bueno es el genérico y esta
    función no dice nada. Es el mismo criterio y la misma fila de la tabla
    que usa el solver -- si se leyera aquí de otra manera, la comprobación
    y la restricción podrían discrepar.

    ⚠️ CORREGIDO (7 septiembre): el umbral era 25 kg y tenía que ser 15,
    igual que en motor_completo.py -- ver el comentario largo de allí, con
    la cita literal de la footnote "b" de la Tabla III-3b de FEDIAF 2025
    (página 21 del PDF, leída a mano, no de memoria).
    """
    if not gramos or not peso_adulto_esperado_kg:
        return None
    if peso_adulto_esperado_kg < RAZA_GRANDE_O_GIGANTE_KG:
        return None
    if etapa not in ("CachorroJoven", "CachorroCrecimiento"):
        return None
    fila = (req or {}).get("Calcio_LateGrowth_RazaGrande")
    if not fila:
        return None
    minimo = _valor_num(fila.get(f"min{etapa}"))
    if not minimo:
        return None
    kcal = sum((al.get(n, {}).get("energia", 0) or 0) / 100.0 * g
               for n, g in gramos.items())
    if kcal <= 0:
        return None
    ca = sum((_valor_num(al.get(n, {}).get("nutrientes", {}).get("calcio")) or 0.0) / 100.0 * g
             for n, g in gramos.items())
    tasa = ca / kcal * 1000.0
    # El mismo 0,5% de margen por redondeo que en los topes de patología,
    # aquí por abajo: el semáforo de FEDIAF ya usa 0,995 para lo mismo.
    if tasa < minimo * 0.995:
        return (f"calcio {tasa:.0f} mg/1000 kcal (mínimo {minimo:.0f} en raza "
                f"grande en crecimiento)")
    return None


# ⚠️ AÑADIDO (8 septiembre) — LA OTRA MITAD DE LA MISMA NOTA b.
#
# La nota b de la Tabla III-3b de FEDIAF 2025 manda DOS cosas para el cachorro
# de raza grande, y hasta hoy solo se aplicaba una. Literal, del PDF (pág. 21),
# leído a mano:
#
#   «For puppies of breeds with adult body weight over 15 kg, until the age of
#    about 6 months. Only after that time, calcium can be reduced to 0.8 % DM
#    (2 g/1000 kcal or 0.48 g/MJ) AND THE CALCIUM-PHOSPHORUS RATIO CAN BE
#    INCREASED TO 1.8/1.»
#
# Y la propia fila del ratio en la III-3b: «Late growth: 1.8/1a (N) or 1.6/1b
# (N)». O sea: 1,8 es el techo del cachorro de raza PEQUEÑA y 1,6 el de la
# grande. El motor aplicaba 1,8 a los dos, así que un cachorro de raza grande
# podía recibir un menú con el ratio entre 1,6 y 1,8 -- por encima del techo
# que su propia fuente le pone-- y salir VERDE, porque el semáforo mide contra
# la fila genérica.
#
# Es el mismo agujero que ya se cerró con el mínimo de calcio y por el mismo
# motivo: `verificar()` no sabe qué raza es el perro. Y aquí importa más que
# allí, porque el mínimo reforzado de calcio EMPUJA EL RATIO HACIA ARRIBA: las
# dos mitades de la nota b tiran en sentidos opuestos y aplicar solo una deja
# al perro justo del lado malo.
#
# ⚠️ MEDIDO ANTES DE PONERLO: 0 de 32 menús de cachorro de raza grande caían
# entre 1,6 y 1,8, así que el agujero era real en las reglas y no estaba dando
# menús malos hoy. Se cierra igual: lo que lo tapaba es una propiedad del
# catálogo de hoy, no una garantía.
def _ratio_cap_raza_grande_roto(gramos, al, req, etapa, peso_adulto_esperado_kg):
    """¿Este menú se pasa del techo de Ca:P REFORZADO de las razas grandes en
    crecimiento? Devuelve el texto del fallo, o None.

    Mismo umbral y misma fila de la tabla que usa el solver: si se leyera aquí
    de otra manera, la comprobación y la restricción podrían discrepar.
    """
    if not gramos or not peso_adulto_esperado_kg:
        return None
    if peso_adulto_esperado_kg < RAZA_GRANDE_O_GIGANTE_KG:
        return None
    if etapa not in ("CachorroJoven", "CachorroCrecimiento"):
        return None
    fila = (req or {}).get("Calcio_LateGrowth_RazaGrande")
    techo = _valor_num((fila or {}).get("maxRatioCaP"))
    if not techo:
        return None
    ca = sum((_valor_num(al.get(n, {}).get("nutrientes", {}).get("calcio")) or 0.0) / 100.0 * g
             for n, g in gramos.items())
    p = sum((_valor_num(al.get(n, {}).get("nutrientes", {}).get("fosforo")) or 0.0) / 100.0 * g
            for n, g in gramos.items())
    if p <= 0:
        return None
    ratio = ca / p
    # El mismo 0,5 % de margen por redondeo que usa el semáforo para el ratio.
    if ratio > techo * 1.005:
        return (f"ratio Ca:P {ratio:.2f}:1 (máximo {techo}:1 en raza grande en "
                f"crecimiento, nota b de FEDIAF)")
    return None
# ⚠️ LA ESCALERA DEL PESO DE REFERENCIA (28 agosto). UN SOLO SITIO.
#
# La DER efectiva -y con ella todos los mínimos escalados- se mide sobre un
# peso, y ese peso tiene que ser el mismo con el que se calcularon las kcal.
# Si una cuenta usa un peso y la otra usa otro, se reconstruye en pequeño el
# fallo del 263 → 413: dos fórmulas sobre dos pesos distintos, pegadas.
#
# Por eso esto está aquí y no repartido: quien llama pide el peso UNA vez y
# se lleva también de dónde salió, para poder decirlo.
#
# Los tres peldaños, en orden, y el motivo de que no se pare en el primero:
# no escalar falla EN SILENCIO -devuelve los mínimos de mantenimiento para
# una ración restringida, que es justo el defecto que esto arregla- y
# escalar de más falla RUIDOSAMENTE -sale infactible, o sale un menú más
# denso de lo necesario, y se ve-. Cuando un fallo es silencioso y el otro
# visible, se elige el visible.
def _peso_de_referencia(datos):
    """(peso_kg, de_dónde_salió). Nunca devuelve None en el peso si hay
    peso real: el último peldaño es usarlo tal cual, y decirlo."""
    obj = getattr(datos, "peso_objetivo_kg", None)
    if obj:
        return float(obj), "declarado"
    actual = getattr(datos, "peso_perro_kg", None)
    bcs = getattr(datos, "bcs", None)
    if actual and bcs is not None:
        derivado = peso_objetivo_desde_bcs(actual, bcs)
        if derivado:
            # ⚠️ EL 9 SE MARCA APARTE (29 agosto). Hay cifra publicada -el
            # 40 % de la Tabla 1 de AAHA- pero la escala se satura ahí:
            # Broome et al. (2023) ven perros que «exceed the description
            # for score 9» con más del 40 % por DXA. Si el perro está un
            # 60 % por encima y la escala lo topa en 40, el objetivo sale
            # DEMASIADO ALTO y con él demasiadas kcal, justo en el que peor
            # lo lleva. Se estima igual -una cota inferior es mejor que
            # nada- pero quien lea la respuesta tiene que poder verlo.
            if float(bcs) >= BCS_ESCALA_SATURADA:
                return derivado, "derivado_del_bcs_cota_inferior"
            # ⚠️ Y POR DEBAJO DE 5 TAMBIEN SE ESTIMA DESDE EL 9 DE SEPTIEMBRE,
            # hacia ARRIBA: el peso óptimo de un perro delgado es mayor que el
            # suyo. Aquí ponía que «la regla no existe hacia abajo», apoyándose
            # en AAHA 2021 -- y era verdad de AAHA y falso del conjunto: FEDIAF
            # tiene las cuatro filas de BCS 1 a 4 en su Tabla VII-2, y su §7.1.1
            # dice que la energía se calcula sobre el peso óptimo sin distinguir
            # dirección. Manda FEDIAF.
            #
            # Se devuelve con procedencia propia porque la corrección al alza va
            # topada al 20 % (un perro muy delgado suele estarlo por una
            # enfermedad), así que en BCS 1, 2 y 3 el número es el tope y no la
            # estimación.
            if float(bcs) < BCS_NEUTRO_MAIN:
                return derivado, "derivado_del_bcs_por_debajo_del_ideal"
            return derivado, "derivado_del_bcs"
    if actual:
        return float(actual), "peso_real_sin_objetivo"
    return None, "sin_peso"


def _avisos_para_el_profesional(gramos, al, der, etapa, patologias=None,
                                peso_perro_kg=None, actividad=None):
    """Las notas que solo tienen sentido para quien sabe interpretarlas.

    ⚠️ POR QUE ESTAN SEPARADAS (10 septiembre). `revisar_seguridad` devuelve dos
    listas: `problemas`, que son cosas que el dueño tiene que hacer o saber
    ("compra el pescado bien frio", "la uva no se da"), y `avisos`, que son
    lecturas del menu que solo sirven si se sabe que hacer con ellas:

      · la vitamina A viene de tres fuentes a la vez, y el total esta dentro
      · el calcio va al 99 % de su techo, y FEDIAF avisa de que con el calcio
        alto puede hacer falta mas zinc y mas cobre
      · el menu lleva cordero, y FEDIAF relaciona el cordero con la taurina baja
        en las razas que la sintetizan peor

    Ninguna de las tres es un incumplimiento y ninguna se arregla cambiando el
    menu. A un dueño le sobran; a un veterinario le dicen exactamente que mirar.

    Y hasta hoy NO SALIAN DE LA API: `_seguridad_completa` llamaba a
    `revisar_seguridad` sin `devolver_avisos=True`, asi que la segunda lista se
    construia y se tiraba. Llevaba asi desde agosto.
    """
    try:
        _, avisos = revisar_seguridad_v2(gramos, al, der, etapa, patologias,
                                         peso_perro_kg=peso_perro_kg,
                                         devolver_avisos=True,
                                         requerimientos=_REQ_FEDIAF)
        avisos = list(avisos or [])
        avisos += _aviso_del_perro_de_trabajo(etapa, actividad, der, peso_perro_kg)
        return avisos
    except Exception as e:      # nunca puede tumbar la entrega de un menu
        print(f"[aviso] no se pudieron calcular los avisos del profesional: {e}")
        return []


# Los dos escalones de actividad que las fuentes llaman «perro de trabajo».
ACTIVIDADES_DE_TRABAJO = ("muy_activo", "trabajo")


def _aviso_del_perro_de_trabajo(etapa, actividad, der, peso_perro_kg):
    """La nota del perro de trabajo: su fuente le pide MÁS fósforo del que le
    dejamos, y eso lo tiene que saber quien firma la pauta.

    ⚠️ POR QUÉ EXISTE (11 septiembre). Elena: «pero nosotros si tenemos lo de
    perro de trabajo no? no se puede aplicar?». Sí lo tenemos -- la ficha lo
    pregunta -- y hasta hoy **no llegaba al motor**: la app lo usaba para
    calcular las kcal y mandaba solo el número.

    Lo que el motor SÍ hace ya sin este dato es apretar los topes crónicos por
    peso metabólico, que es aritmética y va del lado seguro. Lo que NO puede
    hacer solo es lo contrario: el techo de fósforo de 2000 mg/1000 kcal sale de
    la Tabla 13-3 de SACN5, que es la del perro adulto JOVEN en mantenimiento, y
    la Tabla 4.2 de Fascetti da al perro de resistencia **3 g/Mcal, o sea 3000**.
    Un 50 % más.

    Aflojar un techo es decisión clínica y no la toma el motor. Lo que sí puede
    hacer es **decirlo**, que es para lo que existe este canal.
    """
    if actividad not in ACTIVIDADES_DE_TRABAJO:
        return []
    if etapa not in ("Adulto", "Senior"):
        return []
    return [
        "PERRO DE TRABAJO. A este menú se le aplica el techo de fósforo del perro adulto sano "
        "(2000 mg/1000 kcal en adulto, 1750 en sénior), que sale de SACN5 cap.13, Tabla 13-3 -- "
        "la del perro en mantenimiento. La fuente del perro de trabajo propone MÁS: Fascetti & "
        "Delaney 2ª ed., Tabla 4.2, da al perro de resistencia 3 g de fósforo por Mcal, o sea "
        "3000 mg/1000 kcal, un 50 % por encima. El motor NO afloja ese techo solo: aflojarlo es "
        "una decisión clínica. || Y en sentido contrario, el motor SÍ aprieta por su cuenta los "
        "topes de seguridad crónica (yodo, selenio, mercurio, tiaminasa y vitamina D), porque un "
        "tope por 1000 kcal deja pasar el doble a quien come el doble. NRC 2006 cap.11: «Safe "
        "upper limits expressed relative to body weight will remain the same». Eso es aritmética "
        "y va del lado seguro, así que no espera a que nadie lo decida."]


def _garantizar_verificado(respuesta, der, etapa, peso_perro_kg,
                           origen, al=None, req=None, patologias=None,
                           peso_adulto_esperado_kg=None,
                           peso_objetivo_kg=None):
    """
    Último filtro antes de devolver cualquier menú. Devuelve la respuesta
    tal cual (con la ficha recalculada) si el menú está verificado, o una
    respuesta de rechazo si no.

    al/req se pasan cuando quien llama ya los tiene cargados: cargar_v2()
    lee y parsea los dos JSON enteros cada vez, y no tiene sentido
    hacerlo dos veces en la misma petición.
    """
    if not isinstance(respuesta, dict) or not respuesta.get("factible"):
        return respuesta
    gramos = respuesta.get("menu") or respuesta.get("gramos")
    if not gramos:
        return respuesta
    if al is None or req is None:
        al, req = cargar_v2()

    # ⚠️ El peso de referencia va TAMBIEN aqui (28 agosto): el filtro final
    # tiene que medir con los mismos minimos que uso el solver. Si el solver
    # escalara y el semaforo no, un menu construido para una dieta de bajada
    # saldria verde con la densidad de un perro normal -- que es el mismo
    # fallo de la fibra, con otro nombre.
    ficha = verificar_v2(gramos, al, req, der, etapa,
                         peso_referencia_kg=(peso_objetivo_kg or peso_perro_kg))
    seguro = _menu_precalculado_es_seguro(gramos, al, der, peso_perro_kg)
    topes_rotos = _tope_patologia_roto(
        gramos, al, patologias, etapa, req=req,
        der_efectiva=der_efectiva_de(der, peso_objetivo_kg or peso_perro_kg),
        peso_adulto_esperado_kg=peso_adulto_esperado_kg)
    calcio_corto = _minimo_calcio_raza_grande_roto(gramos, al, req, etapa,
                                                   peso_adulto_esperado_kg)
    ratio_pasado = _ratio_cap_raza_grande_roto(gramos, al, req, etapa,
                                               peso_adulto_esperado_kg)

    # ¿es dable? Ver TOPE_GRAMOS_SOBRE_PESO, arriba.
    total_g = sum(gramos.values())
    dable = True
    if peso_perro_kg and peso_perro_kg > 0:
        dable = total_g <= peso_perro_kg * 1000 * TOPE_GRAMOS_SOBRE_PESO
    if not dable:
        observabilidad.capturar(
            RuntimeError(f"Menu imposible de dar bloqueado en {origen}: "
                         f"{total_g:.0f} g para un perro de {peso_perro_kg} kg"),
            endpoint=origen, etapa=etapa, der_objetivo=der,
            peso_perro_kg=peso_perro_kg, gramos_totales=round(total_g),
            pct_del_peso=round(100 * total_g / (peso_perro_kg * 1000), 1))
        return {
            "factible": False,
            "motivo": ("El único menú que cumplía sería demasiado voluminoso para "
                       "este perro. Quita alguna restricción y vuelve a probar."),
            "verificacion": {
                "gramos_totales": round(total_g),
                "pct_del_peso_del_perro": round(100 * total_g / (peso_perro_kg * 1000), 1),
                "tope_pct": round(100 * TOPE_GRAMOS_SOBRE_PESO),
            },
        }

    # ⚠️ CADA RECHAZO DICE **TODOS** LOS MOTIVOS, NO SOLO EL PRIMERO (9
    # septiembre). Los cuatro `if` de abajo devuelven en cuanto encuentran lo
    # suyo, así que un menú que rompía tres cosas contaba una: arreglabas esa y
    # aparecía la siguiente, y desde fuera parecía que el arreglo no había
    # servido de nada.
    #
    # CASO REAL, y lo cazó el BLOQUE 53 al aplicar el techo de calcio del
    # cachorro de raza grande: un menú con el ratio Ca:P a 1,79 lo empezó a
    # parar el techo de calcio -- que va antes-- en vez de la guardia del ratio,
    # y el test que comprueba que esa guardia sigue enchufada se quedó sin ver
    # su motivo. El menú se paraba igual; lo que se perdía era saber por qué.
    _todos_los_motivos = {}
    if topes_rotos:
        _todos_los_motivos["topes_de_patologia_rotos"] = topes_rotos
    if calcio_corto:
        _todos_los_motivos["minimo_calcio_raza_grande_roto"] = calcio_corto
    if ratio_pasado:
        _todos_los_motivos["ratio_cap_raza_grande_roto"] = ratio_pasado

    if topes_rotos:
        # Que esto salte significa que algún camino ha construido un menú
        # saltándose un tope por patología. No se entrega, y va a Sentry:
        # es un fallo del motor, no de lo que haya pedido nadie.
        observabilidad.capturar(
            RuntimeError(f"Menu por encima del tope de patologia bloqueado en "
                         f"{origen}: {'; '.join(topes_rotos)}"),
            endpoint=origen, etapa=etapa, der_objetivo=der,
            peso_perro_kg=peso_perro_kg, patologias=list(patologias or []),
            topes_rotos=topes_rotos, n_alimentos=len(gramos))
        return {
            "factible": False,
            "motivo": ("El menú que salía se pasa de los límites de la patología "
                       "de este perro, así que no te lo damos. Prueba a cambiar "
                       "algún alimento o a quitar alguna restricción."),
            "verificacion": dict(_todos_los_motivos),
        }

    if calcio_corto:
        # Mismo trato que un tope de patología roto: es un fallo del motor
        # (algún camino no aplicó el mínimo reforzado), no de lo que haya
        # pedido nadie, así que no se entrega y va a Sentry.
        observabilidad.capturar(
            RuntimeError(f"Menu por debajo del minimo de calcio de raza grande "
                         f"bloqueado en {origen}: {calcio_corto}"),
            endpoint=origen, etapa=etapa, der_objetivo=der,
            peso_perro_kg=peso_perro_kg,
            peso_adulto_esperado_kg=peso_adulto_esperado_kg,
            calcio_corto=calcio_corto, n_alimentos=len(gramos))
        return {
            "factible": False,
            "motivo": ("El menú que salía se queda corto de calcio para un cachorro "
                       "de raza grande, que necesita más que uno pequeño mientras "
                       "crece. No te lo damos. Prueba a cambiar algún alimento o a "
                       "quitar alguna restricción."),
            "verificacion": dict(_todos_los_motivos),
        }

    if ratio_pasado:
        # La otra mitad de la nota b de FEDIAF, mismo trato que el mínimo de
        # calcio: es un fallo del motor, no de lo que haya pedido nadie.
        observabilidad.capturar(
            RuntimeError(f"Menu por encima del techo de Ca:P de raza grande "
                         f"bloqueado en {origen}: {ratio_pasado}"),
            endpoint=origen, etapa=etapa, der_objetivo=der,
            peso_perro_kg=peso_perro_kg,
            peso_adulto_esperado_kg=peso_adulto_esperado_kg,
            ratio_pasado=ratio_pasado, n_alimentos=len(gramos))
        return {
            "factible": False,
            "motivo": ("El menú que salía lleva demasiado calcio para el fósforo "
                       "que tiene. En un cachorro de raza grande ese margen es más "
                       "estrecho que en uno pequeño, porque un exceso durante el "
                       "crecimiento afecta al hueso. No te lo damos. Prueba a "
                       "cambiar algún alimento o a quitar alguna restricción."),
            "verificacion": dict(_todos_los_motivos),
        }

    if ficha["semaforo"] != "verde" or not seguro:
        # Que esto salte significa que algún camino ha construido un menú
        # que no cumple. Es justo el tipo de fallo que no puede quedarse
        # en un log de Render: va a Sentry con el detalle.
        fallos = [f["nutriente"] for f in ficha.get("rojos", [])]
        observabilidad.capturar(
            RuntimeError(f"Menu no verificado bloqueado en {origen}: "
                         f"semaforo={ficha['semaforo']} seguridad_ok={seguro}"),
            endpoint=origen, etapa=etapa, der_objetivo=der,
            peso_perro_kg=peso_perro_kg, semaforo=ficha["semaforo"],
            nutrientes_en_rojo=fallos, limites_seguridad_ok=seguro,
            n_alimentos=len(gramos))
        return {
            "factible": False,
            "motivo": ("El menú que salía para este perro no cumple todos los "
                       "requisitos, así que no te lo damos. Prueba a cambiar "
                       "algún alimento o a quitar alguna restricción."),
            "verificacion": {
                "semaforo": ficha["semaforo"],
                "cumple": ficha["correctos"],
                "de": ficha["total"],
                "nutrientes_en_rojo": fallos,
                "limites_de_seguridad_ok": seguro,
            },
        }

    # La ficha que se entrega es SIEMPRE la de este filtro, calculada
    # sobre los gramos que de verdad se devuelven -- no una arrastrada de
    # un paso anterior que pueda haberse quedado vieja.
    respuesta["ficha"] = ficha
    respuesta["verificado"] = {
        "contra": etapa,
        "der_objetivo": der,
        "cumple": ficha["correctos"],
        "de": ficha["total"],
        "ratio_ca_p": ficha.get("ratio_ca_p"),
    }
    # ⚠️ LAS NOTAS DEL PROFESIONAL SE PONEN AQUI Y EN NINGUN OTRO SITIO
    # (10 septiembre). Este filtro es por donde pasa TODO menu antes de salir
    # -- la regla 1 --, asi que poniendolas aqui salen en los once caminos sin
    # que nadie tenga que acordarse de anadir la clave en cada uno. Es
    # exactamente el motivo por el que la ficha tambien se calcula aqui y no en
    # cada endpoint.
    #
    # Son NOTAS, no incumplimientos: van en su propia clave para que la app
    # pueda enseñarselas SOLO al veterinario. Al dueño no le sirven -- ninguna
    # se arregla cambiando el menu -- y algunas asustan sin motivo.
    respuesta["avisos_profesional"] = _avisos_para_el_profesional(
        gramos, al, der, etapa, patologias, peso_perro_kg,
        actividad=respuesta.get("actividad"))
    return respuesta


import datetime
_ARRANCADO_EN = datetime.datetime.utcnow().isoformat() + "Z"

# ⚠️ AÑADIDO (20 agosto) — SENTRY. Hasta ahora, cuando un endpoint
# fallaba en producción la única pista era el log de Render: hay que
# entrar a buscarlo a mano, se pierde al reiniciar el servicio y no
# avisa de nada. Con esto, cualquier error de /menu/v2, /analizar,
# /menu/semana, etc. llega al panel de Sentry con la traza completa y
# el cuerpo de la petición que lo provocó, así que se puede reproducir
# sin depender de que el usuario recuerde qué estaba haciendo.
#
# Va AQUÍ, justo ANTES de crear el FastAPI(), y no más abajo, porque la
# integración instrumenta Starlette/FastAPI en el momento del init: si
# se llamara después, la app ya estaría construida sin instrumentar y
# no se capturaría nada.
#
# Sin la variable de entorno SENTRY_DSN esto no hace absolutamente
# nada y la API arranca igual que siempre (ver observabilidad.py).
import observabilidad
observabilidad.iniciar_sentry()

app = FastAPI(title="Rawku API")

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
    # ⚠️ AÑADIDO (28 agosto) — el peso de referencia para la DER efectiva.
    # En un perro con sobrepeso las kcal se calculan sobre el peso IDEAL,
    # así que la densidad de nutrientes tiene que medirse sobre el mismo
    # peso: si se midiera sobre el real, la DER efectiva saldría más baja
    # de lo que es y los mínimos subirían de más. Si no llega, se usa el
    # peso real, que escala un poco de más -- el lado seguro.
    peso_objetivo_kg: Optional[float] = None
    # El BCS de 9 puntos, para derivar el objetivo cuando no viene
    # declarado. Ver `_peso_de_referencia`.
    bcs: Optional[float] = None
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
    # ⚠️ EL TOKEN, NO UN BOOLEANO (29 agosto). Es la sesión de Supabase de
    # quien pide el menú. Sirve para saber si es un veterinario acreditado,
    # y con eso se le formulan las patologías que al dueño se le bloquean.
    # No se acepta un `modo_profesional` porque eso lo manda cualquiera.
    # Ver `_es_profesional_acreditado`.
    token_usuario: Optional[str] = None
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
    # ⚠️ AÑADIDO (28 agosto) — el peso de referencia para la DER efectiva.
    # En un perro con sobrepeso las kcal se calculan sobre el peso IDEAL,
    # así que la densidad de nutrientes tiene que medirse sobre el mismo
    # peso: si se midiera sobre el real, la DER efectiva saldría más baja
    # de lo que es y los mínimos subirían de más. Si no llega, se usa el
    # peso real, que escala un poco de más -- el lado seguro.
    peso_objetivo_kg: Optional[float] = None
    # El BCS de 9 puntos, para derivar el objetivo cuando no viene
    # declarado. Ver `_peso_de_referencia`.
    bcs: Optional[float] = None
    # ⚠️ AÑADIDO (11 septiembre) — LA ACTIVIDAD, QUE LA APP YA SABE Y NO MANDABA.
    #
    # Elena: «pero nosotros si tenemos lo de perro de trabajo no? no se puede
    # aplicar?». Sí lo tenemos: la ficha lo pregunta y la app lo usa para
    # calcular el DER. Lo que pasaba es que **se quedaba ahí**: a este endpoint
    # solo llegaban las kcal ya calculadas, así que el motor veía un número y no
    # sabía si era un galgo de sofá o un perro de trineo.
    #
    # El motor puede DEDUCIRLO del cociente DER/peso^0,75 -- de ahí salen los
    # topes crónicos por peso metabólico del 11 de septiembre, y esa deducción
    # se queda como respaldo para cuando este campo no venga. Pero deducir un
    # dato que existe es peor que recibirlo, y aquí se ve por qué: FEDIAF pone
    # al Gran Danés en 200 kcal/kg^0,75 POR RAZA, no por actividad (§7.2.3.4:
    # la cifra de raza va EN VEZ del nivel de actividad), así que por el
    # cociente sale «perro de trabajo» un perro que está tumbado.
    #
    # Valores: los cinco de `der.ACTIVIDAD_KEY` -- sedentario, normal, activo,
    # muy_activo, trabajo. Opcional a propósito: mientras el frontend no lo
    # mande, el motor sigue deduciendo y NO cambia de comportamiento.
    actividad: Optional[str] = None
    nombres_excluidos: Optional[list] = None
    patologias: Optional[list] = None
    # ⚠️ AÑADIDO (8 septiembre) — EL PELDAÑO DE LA ESCALERA, ELEGIDO.
    # Sin esto (lo normal, y todo lo que manda la app del tutor) el motor
    # recorre la escalera como siempre. Con esto se formula EN ese peldaño y
    # no se baja solo. Ver `_peldanos_publicos` y `GET /relajacion`.
    peldano: Optional[str] = None
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
    # (tiaminasa/mercurio/vitD/yodo/selenio), calculado por
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
    # ⚠️ AÑADIDO (25 agosto) — CASO REAL: "he lanzado el regenerar menús
    # cambiando el peso del perro desde evolución, pero me los ha cambiado
    # BASTANTE, el primero lo ha respetado un poco más pero el segundo...
    # prácticamente nada".
    #
    # El botón promete "regenera con los mismos ingredientes", y no había
    # forma de pedir eso: `nombres_alimentos` solo se mira en los modos
    # "personalizar" y "aprovechar", y esa pantalla manda "automatico", que
    # los IGNORA los dos. La petición salía correcta y el servidor la
    # tiraba a la basura.
    #
    # Esto es una PREFERENCIA, no una imposición, y por eso va aparte de
    # `nombres_alimentos`: sirve en cualquier modo (en Personalizar convive
    # con lo que el usuario forzó) y nunca puede volver el menú imposible.
    # Llega tal cual al `preferir` del motor: abarata usar esos alimentos,
    # no obliga a nada.
    preferir_alimentos: Optional[list] = None
    # Lo mismo pero para /menu/semana, que genera N menús de una vez: una
    # lista por menú, en el mismo orden. Tiene que ser por menú -- el fallo
    # que ella vio era exactamente ése, que el segundo menú recibía los
    # alimentos del PRIMERO.
    preferir_por_menu: Optional[list] = None
    # ⚠️ AÑADIDO para /menu/v2 (5 agosto): el frontend dice explícitamente
    # qué modo quiere, en vez de que el backend tenga que adivinarlo por
    # lo que manda en nombres_alimentos/forzar_presencia.
    #   "automatico"   -> el motor elige libre, ignora las dos listas
    #   "personalizar" -> los alimentos de forzar_presencia (o si viene
    #                     vacío, los de nombres_alimentos) SÍ O SÍ entran
    #   "aprovechar"   -> los de nombres_alimentos se PRIORIZAN, pero el
    #                     motor puede añadir más si hace falta para cerrar
    modo: str = "automatico"
    # ⚠️ AÑADIDO (21 agosto) — presupuesto de TIEMPO para este menú, en
    # segundos. Lo pone quien orquesta varias generaciones seguidas, no
    # el usuario. Nació con /menu/varios-perros: ahí hay que resolver N
    # menús dentro de la MISMA petición, y el presupuesto de 24s por
    # menú que hay fijado abajo es de un único menú -- con dos perros
    # serían 48s y Render corta la conexión a los 30s. Quien orquesta
    # reparte el presupuesto y lo pasa aquí.
    #
    # Nunca puede AFLOJARLO, solo apretarlo: se toma el mínimo con el de
    # por defecto (mismo criterio que presupuesto_semanal_restante).
    presupuesto_segundos: Optional[float] = None


class PeticionCambiarAlimento(BaseModel):
    # ⚠️ EL TOKEN, NO UN BOOLEANO (29 agosto). Es la sesión de Supabase de
    # quien pide el menú. Sirve para saber si es un veterinario acreditado,
    # y con eso se le formulan las patologías que al dueño se le bloquean.
    # No se acepta un `modo_profesional` porque eso lo manda cualquiera.
    # Ver `_es_profesional_acreditado`.
    token_usuario: Optional[str] = None
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
    # ⚠️ AÑADIDO (28 agosto) — el peso de referencia para la DER efectiva.
    # En un perro con sobrepeso las kcal se calculan sobre el peso IDEAL,
    # así que la densidad de nutrientes tiene que medirse sobre el mismo
    # peso: si se midiera sobre el real, la DER efectiva saldría más baja
    # de lo que es y los mínimos subirían de más. Si no llega, se usa el
    # peso real, que escala un poco de más -- el lado seguro.
    peso_objetivo_kg: Optional[float] = None
    # El BCS de 9 puntos, para derivar el objetivo cuando no viene
    # declarado. Ver `_peso_de_referencia`.
    bcs: Optional[float] = None
    # ⚠️ AÑADIDO (5 agosto, madrugada): mismo motivo que en PeticionMenu
    # -- si el perro no puede masticar hueso carnoso, esa exclusión debe
    # respetarse también al editar, no solo al generar por primera vez.
    categorias_excluidas: Optional[list] = None


class PeticionAnadirQuitarAlimento(BaseModel):
    # ⚠️ EL TOKEN, NO UN BOOLEANO (29 agosto). Es la sesión de Supabase de
    # quien pide el menú. Sirve para saber si es un veterinario acreditado,
    # y con eso se le formulan las patologías que al dueño se le bloquean.
    # No se acepta un `modo_profesional` porque eso lo manda cualquiera.
    # Ver `_es_profesional_acreditado`.
    token_usuario: Optional[str] = None
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
    # ⚠️ AÑADIDO (28 agosto) — el peso de referencia para la DER efectiva.
    # En un perro con sobrepeso las kcal se calculan sobre el peso IDEAL,
    # así que la densidad de nutrientes tiene que medirse sobre el mismo
    # peso: si se midiera sobre el real, la DER efectiva saldría más baja
    # de lo que es y los mínimos subirían de más. Si no llega, se usa el
    # peso real, que escala un poco de más -- el lado seguro.
    peso_objetivo_kg: Optional[float] = None
    # El BCS de 9 puntos, para derivar el objetivo cuando no viene
    # declarado. Ver `_peso_de_referencia`.
    bcs: Optional[float] = None
    # ⚠️ AÑADIDO (25 agosto) — CASO REAL: /menu/anadir y /menu/quitar
    # devolvían HTTP 500. `_recalcular_con_motor` lee
    # `datos.categorias_excluidas`, y este modelo era el único de los tres
    # de edición que no lo tenía -- PeticionCambiarAlimento sí.
    #
    # No reventaba siempre, y por eso llevaba semanas ahí: solo se llega a
    # esa línea cuando la edición ha tenido que RELAJAR alguna proporción
    # de BARF. Con el catálogo de todos los días casi nunca pasa; con una
    # patología que aprieta, constantemente. Afectaba a "Añadir suplemento"
    # desde agosto y a la papelera de quitar un alimento desde hoy mismo.
    categorias_excluidas: Optional[list] = None


# ⚠️ AÑADIDO (20 agosto) — CASO 3: EL PERRO CAMBIA DE CATEGORÍA.
# Ver el bloque de comentarios del endpoint /menu/revalidar para el caso
# real completo. menu_actual aquí lleva GRAMOS, no solo nombres como en
# los modelos de edición: para poder verificar el menú que el perro está
# comiendo de verdad hace falta saber cuánto de cada cosa, no solo qué.
class PeticionRevalidar(BaseModel):
    # ⚠️ EL TOKEN, NO UN BOOLEANO (29 agosto). Es la sesión de Supabase de
    # quien pide el menú. Sirve para saber si es un veterinario acreditado,
    # y con eso se le formulan las patologías que al dueño se le bloquean.
    # No se acepta un `modo_profesional` porque eso lo manda cualquiera.
    # Ver `_es_profesional_acreditado`.
    token_usuario: Optional[str] = None
    menu_actual_gramos: dict          # {"Lengua de ternera": 485.3, ...}
    der_objetivo: float               # el DER de AHORA, no el de cuando se generó
    etapa_requisitos: str             # la etapa de AHORA
    peso_perro_kg: Optional[float] = None
    peso_adulto_esperado_kg: Optional[float] = None
    # ⚠️ AÑADIDO (28 agosto) — el peso de referencia para la DER efectiva.
    # En un perro con sobrepeso las kcal se calculan sobre el peso IDEAL,
    # así que la densidad de nutrientes tiene que medirse sobre el mismo
    # peso: si se midiera sobre el real, la DER efectiva saldría más baja
    # de lo que es y los mínimos subirían de más. Si no llega, se usa el
    # peso real, que escala un poco de más -- el lado seguro.
    peso_objetivo_kg: Optional[float] = None
    # El BCS de 9 puntos, para derivar el objetivo cuando no viene
    # declarado. Ver `_peso_de_referencia`.
    bcs: Optional[float] = None
    nombres_excluidos: Optional[list] = None
    patologias: Optional[list] = None
    especies_excluidas: list[str] = []
    categorias_excluidas: Optional[list] = None

    @property
    def menu_actual(self):
        """_recalcular_con_motor() espera una lista de nombres."""
        return list(self.menu_actual_gramos or {})


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
            peso_objetivo_kg=_peso_de_referencia(datos)[0],
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


# ⚠️ QUITADO (26 agosto) — aquí estaba `POST /menu`, el endpoint del motor
# ANTERIOR al MILP (`optimizar_menu()` en el viejo optimizador.py). El
# frontend no lo llamaba (comprobado: cero referencias en todo canislab-web)
# y arrastraba consigo 1.000 líneas con SU PROPIA tabla de patologías, que
# llevaba semanas desincronizada de la de verdad -- fósforo renal a 1.400 en
# vez de 1.200, cobre en hepatopatía a 3,0 sin bloquear, grasa en
# pancreatitis al 25% de las kcal, y urato, cistinuria y "otra" sin existir.
#
# No llegó a dar menús malos porque `_garantizar_verificado()` los volvía a
# comprobar contra las tablas buenas antes de entregarlos: los habría
# rechazado. Pero eso significa que este camino, además de duplicado, estaba
# construyendo menús que el filtro final iba a tirar.
#
# Lo que quedaba vivo de aquel archivo (cargar_requerimientos, resolver_etapa,
# _valor_o_none, SENIOR_PROTEINA_MINIMA, ETAPAS_VALIDAS y
# dosis_maxima_fabricante) vive ahora en `requisitos.py`, sin nada más
# alrededor.

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
    al, _req_cat = cargar_v2()
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
        # ⚠️ CORREGIDO (20 agosto) — CASO REAL ENCONTRADO AUDITANDO: aquí
        # solo se miraban los 5 límites de seguridad crónica. Un menú del
        # catálogo, reescalado a otras kcal y con los suplementos topados
        # por peso, puede quedarse CORTO en nutrientes sin superar ningún
        # tope -- y se servía igual. Ahora se verifica de verdad contra
        # los 30 requisitos por el mismo filtro que el resto.
        # ⚠️ Y CON EL PESO ADULTO ESPERADO DEL TAMAÑO (9 septiembre). Este
        # endpoint no recibe el peso adulto del perro -- solo su tamaño --,
        # pero el tamaño ES eso: la entrada `<tamaño>_Adulto` del catálogo
        # dice cuánto pesa de adulto un perro de ese grupo. Sin pasarlo, un
        # menú de cachorro «Gigante» se comprobaría contra el techo de calcio
        # del cachorro pequeño (4250 en vez de 2750) y este endpoint sería el
        # agujero de la regla 1 para justo el perro al que más le importa.
        _padu_cat = (CATALOGO.get(f"{tamano}_Adulto") or {}).get("peso_kg")
        verificado = _garantizar_verificado(
            {"factible": True, "gramos": gramos_escalados},
            der_objetivo, etapa, peso_perro_kg, origen="/catalogo", al=al, req=_req_cat,
            peso_adulto_esperado_kg=_padu_cat)
        if not verificado.get("factible"):
            return {"encontrado": False,
                    "motivo": "El menú de catálogo para este tamaño/etapa, reescalado a "
                              "este peso y calorías, ya no cumple todos los requisitos -- "
                              "pide el menú por /menu/v2 en su lugar, que resuelve en vivo "
                              "comprobándolos siempre.",
                    "verificacion": verificado.get("verificacion")}
        return {"encontrado": True, **entrada, "gramos": gramos_escalados,
                "der_escalado_a": der_objetivo,
                "ficha": verificado["ficha"], "verificado": verificado["verificado"]}

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
    observabilidad.etiquetar(endpoint="/menu/v2", etapa=datos.etapa_requisitos)
    try:
        # ⚠️ LA ACTIVIDAD VIAJA CON LA RESPUESTA (11 septiembre), porque
        # `_garantizar_verificado` es quien monta los avisos del profesional y
        # necesita saber si es un perro de trabajo. Se pone ANTES de verificar,
        # no después: si se pusiera después, un menú rechazado saldría sin el
        # aviso y el único perro al que le importa es justo el que más come.
        _interno_v2 = _resolver_menu_v2_interno(datos)
        if isinstance(_interno_v2, dict) and datos.actividad:
            _interno_v2["actividad"] = datos.actividad
        _resp_v2 = _garantizar_verificado(
            _interno_v2,
            datos.der_objetivo, datos.etapa_requisitos, datos.peso_perro_kg,
            origen="/menu/v2", patologias=datos.patologias,
            peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
            peso_objetivo_kg=_peso_de_referencia(datos)[0])
        # ⚠️ SE DICE SOBRE QUÉ PESO SE HA MEDIDO, y de dónde salió. Los
        # mínimos escalan con la DER efectiva, y la DER efectiva se calcula
        # sobre un peso: si ese peso no es el mismo con el que se hicieron
        # las kcal, las dos cuentas hablan de perros distintos. Que se vea
        # es lo único que separa un desajuste de un desajuste EN SILENCIO.
        if isinstance(_resp_v2, dict):
            _p_ref, _p_de = _peso_de_referencia(datos)
            # ⚠️ EL AVISO DE LA PATOLOGÍA VIAJA CON EL MENÚ (29 agosto).
            # Antes no viajaba ninguno: la app tenía su propia copia del
            # texto para las patologías que BLOQUEAN, y para las que sí se
            # formulaban enseñaba un rojo genérico. Eso deja de valer en
            # cuanto el veterinario formula las que al dueño se le bloquean:
            # un menú de urato que NO restringe purinas y no lo dice es peor
            # que no dar menú. Y el aviso no puede vivir en la app, porque
            # lo que hay que contar es lo que hizo el MOTOR.
            from motor_completo import avisos_de_patologias as _avfn
            _prof_v2 = _es_profesional_acreditado(getattr(datos, "token_usuario", None))
            _av = _avfn(getattr(datos, "patologias", None),
                        datos.etapa_requisitos, es_profesional=_prof_v2)
            if _av:
                _resp_v2["avisos_patologia"] = _av
                _resp_v2["formulado_como_profesional"] = _prof_v2
            _resp_v2["peso_de_referencia"] = {
                "kg": _p_ref, "procedencia": _p_de,
                "der_efectiva": (round(datos.der_objetivo / _p_ref ** 0.75, 1)
                                 if _p_ref else None),
            }
        return _resp_v2
    except Exception as e:
        import traceback
        traceback.print_exc()  # queda en los logs de Render para poder investigarlo
        # ⚠️ AÑADIDO (20 agosto) — este try/except es a proposito (el
        # frontend tiene que recibir JSON valido pase lo que pase), pero
        # tiene un efecto secundario que hay que compensar a mano: al no
        # dejar salir nunca la excepcion, Sentry NO la ve por su cuenta.
        # Sin esta linea, justo el fallo mas importante -- que el motor
        # reviente generando un menu -- seria el unico invisible.
        observabilidad.capturar(e, endpoint="/menu/v2",
                                etapa=datos.etapa_requisitos,
                                der_objetivo=datos.der_objetivo,
                                peso_perro_kg=datos.peso_perro_kg,
                                tamano=datos.tamano,
                                n_alimentos=len(datos.nombres_alimentos or []),
                                patologias=datos.patologias)
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
    TOPE_SELENIO_KCAL, TOPE_EPA_DHA_SEMANAL_KCAL,
)


def _presupuesto_semanal_inicial(der_objetivo):
    """Presupuesto SEGURO para la semana completa, para cada uno de los
    5 puntos de riesgo crónico. tiaminasa/mercurio son fracción de kcal
    (0-1); vitD, yodo y selenio son µg -- cada uno se reparte en su
    propia unidad, ver resolver() en motor_completo.py para cómo se usa
    cada una.

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
        # El selenio no acumula: es una densidad (µg por cada 1000 kcal),
        # igual cada día. Va en µg absolutos del día como vitD y yodo, pero
        # SIN el ×7 ni el reparto, porque no es un depósito que se vacíe.
        "selenio": TOPE_SELENIO_KCAL * der_objetivo / 1000.0,
        # ⚠️ AÑADIDO (26 agosto) — EPA+DHA ES UN LÍMITE DE LA DIETA HABITUAL,
        # NO DE UN PLATO.
        #
        # Estuvo un día puesto como máximo por menú en requerimientos_v2_final
        # y estaba mal, con una consecuencia medida: 19 de los 20 pescados del
        # catálogo pasan de 2800 mg/1000 kcal ELLOS SOLOS (el boquerón llega a
        # ~11.000), porque el pescado tiene mucho omega-3 y pocas calorías. El
        # tope por menú no protegía de nada: borraba el pescado azul entero.
        # Los menús con pescado cayeron de 13 de cada 24 a 4.
        #
        # FEDIAF 2025 deja la columna Maximum VACÍA para EPA+DHA. Los 2800 son
        # el SUL del NRC 2006 (Lenox & Bauer, JVIM 2013;27:217-226), y un SUL
        # es una concentración de la dieta CRÓNICA. Así que va aquí, con vitD
        # y yodo: un total para la semana que se reparte entre los días que
        # quedan. El motor equilibra solo -- unos días con pescado azul y
        # otros sin él -- que es exactamente lo que hace una rotación.
        #
        # Sin margen extra (a diferencia de vitD y yodo): 2800 YA es el límite
        # crónico, no un tope diario multiplicado por siete. Apretarlo más
        # sería inventarse una cifra.
        "epa_dha": TOPE_EPA_DHA_SEMANAL_KCAL * der_objetivo / 1000.0 * 7,
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
    # EPA+DHA en GRAMOS reales de este menú, que es la unidad del catálogo y
    # la del requisito (0,11 g = 110 mg). Se suman los dos: el requisito se
    # llama EPA+DHA y comprobar solo una mitad fue el fallo del 25 de agosto.
    epa_dha_g = sum(((al.get(n, {}).get("nutrientes", {}).get("epa") or 0)
                     + (al.get(n, {}).get("nutrientes", {}).get("dha") or 0)) * g / 100.0
                    for n, g in gramos.items())
    return {
        "tiaminasa": (kcal_tia / der_objetivo) if der_objetivo else 0,
        "mercurio": (kcal_merc / der_objetivo) if der_objetivo else 0,
        "vitD": vitd_ug,   # µg reales de ESTE menú (se multiplicará por sus días al acumular)
        "yodo": yodo_ug,
        "selenio": selenio_ug,   # µg reales de ESTE menú (no acumula: no se resta)
        "epa_dha": epa_dha_g,   # g reales de ESTE menú (se multiplica por sus días al acumular)
    }


def _restar_del_presupuesto(restante, consumo, dias_de_este_menu):
    """Descuenta del presupuesto semanal lo que se ha llevado un menú ya
    generado, y devuelve lo que queda para los siguientes.

    ⚠️ EXTRAÍDO (26 agosto). Esta resta estaba escrita DOS VECES, idéntica,
    en /menu/semana y en /menu/varios-perros. Dos copias de la misma
    aritmética es como el analizador y el semáforo acabaron discrepando sobre
    la fibra: una se toca y la otra no.

    Y hacía falta por un segundo motivo: escrita dentro de los endpoints, la
    parte que de verdad importa -- el `* dias` -- no se podía comprobar sin
    generar una semana entera, y generando semanas NO SE CAZA (medido: con el
    `* dias` quitado, ningún escenario alcanzable da un promedio distinto,
    porque el presupuesto de EPA+DHA hoy nunca llega a morder). Aquí sí se
    puede probar la aritmética sola, que es donde vive el fallo.

    QUÉ ACUMULA Y QUÉ NO:
      · tiaminasa y mercurio son una FRACCIÓN de las kcal del día, y selenio
        una DENSIDAD por cada 1000 kcal. No son totales: no se acumulan y no
        se restan.
      · vitD, yodo y epa_dha SÍ son totales de la semana. Y se descuentan
        MULTIPLICADOS POR LOS DÍAS que se come ese menú: uno que se repite 4
        días gasta cuatro veces lo suyo, no una. Sin ese factor, el
        presupuesto saldría bien justo en el caso que más importa -- pocos
        menús repetidos muchos días -- y dejaría de proteger sin dar ningún
        error.
    """
    dias = max(1, dias_de_este_menu)
    salida = dict(restante)
    for clave in ("vitD", "yodo", "epa_dha"):
        salida[clave] = restante.get(clave, 0.0) - consumo.get(clave, 0.0) * dias
    return salida


def _presupuesto_para_menu_actual(restante, dias_restantes_incluido_este):
    """Reparte el presupuesto que queda entre los días que faltan
    (incluido el menú que se va a generar ahora), para dar el tope
    DIARIO efectivo de ESTE menú -- lo que resolver() usa como techo.
    tiaminasa/mercurio/selenio ya son "por día" (no se dividen, son una
    fracción/densidad, no un total acumulable); vitD/yodo SÍ son totales
    acumulados, así que sí se dividen entre los días."""
    dias = max(1, dias_restantes_incluido_este)
    return {
        "tiaminasa": max(0.0, restante["tiaminasa"]),
        "mercurio": max(0.0, restante["mercurio"]),
        "vitD": max(0.0, restante["vitD"]) / dias,
        "yodo": max(0.0, restante["yodo"]) / dias,
        "selenio": max(0.0, restante["selenio"]),
        # EPA+DHA acumula igual que vitD y yodo: es un promedio de la semana.
        "epa_dha": max(0.0, restante.get("epa_dha", 0.0)) / dias,
    }


# ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO, pedido
# expreso por segunda vez: seguía apareciendo el aviso de sardina/vitD
# en un único menú de Personalizar, a pesar del arreglo anterior. Causa
# real: aquel arreglo reutilizaba _presupuesto_semanal_inicial +
# _presupuesto_para_menu_actual, que SOLO endurecen vitD/yodo (los que
# de verdad se "dividen entre días" en el caso de rotación real con
# varios menús) -- pero tiaminasa/mercurio, al ser una FRACCIÓN diaria
# plana (no un total acumulable), nunca se tocaban: su tope diario
# seguía siendo el mismo 10% de siempre, tanto si el menú es "uno de
# varios en rotación variada" como si es "el único, repetido los 7
# días" -- y estos dos casos son genuinamente distintos en riesgo real.
# Esta función es la correcta para el caso de UN SOLO menú asumido para
# toda la semana: aplica el mismo margen de seguridad crónica (0.75) a
# los 5 límites de forma UNIFORME, incluidos tiaminasa y mercurio --
# porque si este único menú se va a repetir todos los días, su propio
# tope diario de "pescado con tiaminasa" debe ser más estricto que el
# de un menú que solo aparece 2-3 días dentro de una rotación variada.
# =====================================================================
# ⚠️ AÑADIDO (20 agosto) — LA ESCALERA: QUE NUNCA SE QUEDE SIN MENÚ
#
# CASO REAL MEDIDO: un adulto de 20 kg con tres alergias (pollo, ternera,
# cordero) devolvía "no existe ninguna combinación". Medido de verdad, no
# era cierto: SÍ existía, y salía verde 30/30. Lo que lo bloqueaba no era
# la nutrición sino el mínimo de "Vísceras 2%" -- con esas tres especies
# fuera solo quedaban bazo y páncreas de vaca, y no cabían sin chocar con
# un límite de seguridad. El solver lo declaraba infactible en 0,0s.
#
# Y los márgenes de categoría (hueso 20-60%, carne 10-60%, vísceras
# 2-12%...) son la FORMA del BARF -- criterio de producto, nuestro. No
# son FEDIAF: verificar() ni los mira. Estábamos negándole el menú a un
# perro alérgico para defender una proporción que ninguna guía exige.
#
# Esta escalera se recorre SOLO si el intento estricto ha fallado, y va
# soltando esas proporciones peldaño a peldaño. Lo que NO se suelta
# nunca, en ningún peldaño:
#     · los 30 requisitos de FEDIAF y el ratio Ca:P
#     · los límites de seguridad crónica (vitD, yodo, selenio, mercurio,
#       tiaminasa) -- van dentro de resolver() como restricción dura
#     · las alergias y las categorías que el usuario excluyó a mano
#     · las patologías que bloquean la generación
#     · los MÁXIMOS por categoría (que son los que evitan un menú de 90%
#       hígado); solo se tocan los MÍNIMOS
# Cada peldaño que se usa se cuenta en la respuesta, para que la app
# pueda decir por qué este menú no se parece a los demás.
# =====================================================================
# ⚠️ CORREGIDO (20 agosto) — FALLO REAL ENCONTRADO CRUZANDO CON LA WEB:
# ETAPAS_VALIDAS viene de optimizador.py (el motor viejo) y solo tiene
# Adulto/CachorroJoven/CachorroCrecimiento. Pero el motor v2 admite
# además Senior, Gestante y Lactante -- verificar.py las mapea con
# EQUIVALENCIA (Senior usa el perfil de Adulto; gestación y lactancia el
# de crecimiento temprano; lo que cambia en esas etapas son las kcal, y
# de eso se encarga der.py). /menu/v2 las acepta sin problema.
#
# El fallo: /menu/revalidar validaba con _etapa_ok(), que usa la lista
# vieja, así que devolvía 400 para CUALQUIER perro senior. La web manda
# "Senior" y se traga el error en silencio (el .catch deja la revisión
# en reposo), así que la revalidación por cambio de etapa simplemente NO
# ocurría para los perros senior, sin que nada lo dijera. Justo el tipo
# de fallo invisible que llevamos todo el día cazando.
from verificar import EQUIVALENCIA as EQUIVALENCIA_V2
ETAPAS_MOTOR_V2 = set(ETAPAS_VALIDAS) | set(EQUIVALENCIA_V2)


CATEGORIAS_SECUNDARIAS = ("Vísceras", "Hígado", "Verduras y frutas")


CATEGORIAS_QUE_HACEN_RACION = ("Carne muscular", "Hueso carnoso")


def _hay_comida_de_verdad(al, excluidos=None, categorias_excluidas=None):
    """
    ¿Le queda al motor carne muscular Y hueso carnoso de donde elegir?

    No es una pregunta de estilo: es la que decide si el último peldaño de
    la escalera se puede pisar. Ese peldaño suelta los TECHOS de vísceras,
    hígado y verdura, y lo único que impide que el motor monte una ración
    de hígado y calabaza con suplementos es que la carne y el hueso sigan
    teniendo su SUELO. Si no hay ni carne ni hueso entre lo accesible, ese
    suelo no restringe nada -- una restricción sobre una categoría vacía se
    cumple sola -- y el peldaño deja de ser "soltar la forma" para pasar a
    inventar comida.

    Se mira lo que de verdad queda: la categoría excluida a mano, y también
    la que se ha quedado sin nada por las alergias (excluir "pollo" puede
    vaciar una categoría entera en un catálogo reducido).
    """
    fuera = set(categorias_excluidas or [])
    prohibidos = set(excluidos or [])
    for cat in CATEGORIAS_QUE_HACEN_RACION:
        if cat in fuera:
            return False
        de_la_cat = [n for n, a in (al or {}).items() if a.get("categoria") == cat]
        permitidos, _f, _av = filtrar_exclusiones(de_la_cat, prohibidos)
        if not permitidos:
            return False
    return True


def _escalera_de_relajacion(hay_comida_de_verdad=True):
    """Peldaños (margenes, max_suplementos, qué se soltó), de más
    estricto a menos. El primero es exactamente lo de siempre."""
    sin_minimo_secundarias = {
        c: ((0.0 if c in CATEGORIAS_SECUNDARIAS else mn), mx)
        for c, (mn, mx) in MARGENES_V2.items()
    }
    sin_ningun_minimo = {c: (0.0, mx) for c, (mn, mx) in MARGENES_V2.items()}
    # ⚠️ AÑADIDO (29 agosto) — LA ESCALERA SOLTABA LOS MÍNIMOS Y NUNCA LOS
    # MÁXIMOS, Y HAY CASOS DONDE EL QUE BLOQUEA ES UN MÁXIMO.
    #
    # CASO REAL MEDIDO, contra producción: un adulto de 25 kg con
    # PANCREATITIS no obtenía menú NUNCA -- cinco de cinco intentos --, y la
    # usuaria leía "no existe ninguna combinación de alimentos accesibles que
    # cumpla todos los requisitos, ni siquiera soltando las proporciones
    # habituales del BARF". Era mentira: sí existe.
    #
    # Aislado peldaño a peldaño:
    #     proporciones tal cual ................................ no sale
    #     último peldaño de la escalera (mínimos a 0) .......... no sale
    #     mínimos intactos y MÁXIMOS sueltos ................... SALE, 0,4 s
    #
    # Y el culpable es UNO solo: el techo del 10 % de "Verduras y frutas".
    # Soltando ese, sale. Tiene sentido: en pancreatitis la grasa se limita a
    # menos de 20 g/1000 kcal, y para llegar ahí hay que diluir con algo que
    # no engorde -- y lo único que hay es verdura, que está topada al 10 %.
    #
    # Soltar un máximo de categoría es EXACTAMENTE lo que la regla 3 del
    # CLAUDE.md autoriza: "lo que se puede relajar es la FORMA, nunca la
    # nutrición. Se sueltan las proporciones de BARF (hueso 20-60 %, etc.),
    # que son criterio nuestro y no de FEDIAF". El 10 % de verdura es
    # criterio nuestro. Los requisitos y los topes de seguridad no se tocan,
    # y el menú sigue pasando por _garantizar_verificado() igual que todos.
    #
    # Va al FINAL de la escalera a propósito: solo se llega aquí cuando todo
    # lo demás ha fallado, y se dice qué se soltó -- nunca en silencio.
    #
    # ⚠️ Y SOLO LAS SECUNDARIAS. El primer intento de este arreglo añadía un
    # peldaño más que soltaba TODAS las proporciones, mínimos y máximos. Lo
    # tiró el BLOQUE 9 en el acto: "sin carne, hueso ni pescado: se inventó
    # un menú donde no hay comida posible". Sin el techo de la carne y sin el
    # suelo del hueso, el motor monta una ración de hígado, verdura y
    # suplementos que cumple los 42 requisitos EN EL PAPEL -- y eso no es
    # comida para un perro.
    #
    # Los mínimos de "Carne muscular" y "Hueso carnoso" se quedan intactos en
    # este peldaño: son lo que hace que la ración siga siendo una ración. Lo
    # que se suelta es el techo de lo accesorio, que es criterio nuestro.
    sin_max_secundarias = {
        c: ((0.0 if c in CATEGORIAS_SECUNDARIAS else mn),
            (1.0 if c in CATEGORIAS_SECUNDARIAS else mx))
        for c, (mn, mx) in MARGENES_V2.items()
    }
    peldanos = [
        (MARGENES_V2, 2, None),
        (sin_minimo_secundarias, 2, "proporcion_minima_visceras_higado_verdura"),
        (sin_ningun_minimo, 2, "proporcion_minima_de_todas_las_categorias"),
        (sin_ningun_minimo, 3, "proporcion_minima_y_un_suplemento_mas"),
        (sin_ningun_minimo, 4, "proporcion_minima_y_dos_suplementos_mas"),
    ]
    # El último peldaño solo existe si la ración sigue teniendo carne y
    # hueso de donde tirar -- ver _hay_comida_de_verdad(). Sin eso, soltar
    # los techos de lo accesorio no relaja la forma: inventa comida.
    if hay_comida_de_verdad:
        peldanos.append(
            (sin_max_secundarias, 4, "tope_maximo_de_visceras_higado_y_verdura"))
    return peldanos


# ─── LA ESCALERA, ELEGIBLE POR UN PROFESIONAL ────────────────────────────────
#
# ⚠️ PEDIDO EXPRESO, y estaba escrito desde el 28 de agosto en la fase 1 de
# VETERINARIOS.md: "que peldano de la escalera de relajacion se uso, Y PODER
# ELEGIRLO. Hoy se baja solo y se avisa; un profesional quiere decidir si
# prefiere otro reparto antes que soltar la proporcion de hueso".
#
# La diferencia con el tutor no es de permisos, es de trabajo. A un dueno la
# escalera le resuelve el problema: no le sale menu, se sueltan las
# proporciones de BARF -- que son criterio NUESTRO, no de FEDIAF -- y se le
# dice. Un veterinario tiene una opinion propia sobre ese reparto: puede
# preferir subir el higado antes que quedarse sin visceras, o al reves. Que
# el motor decida por el es quitarle justo la decision que el sabe tomar.
#
# LO QUE ESTO NO ES: no relaja NADA nutricional. Un peldano solo mueve las
# proporciones de categoria y cuantos suplementos caben. Los 43 requisitos,
# el ratio Ca:P, los topes de seguridad cronica y los de patologia son
# identicos en todos los peldanos, y el menu sigue pasando por
# `_garantizar_verificado()` igual. Es la regla 3 del CLAUDE.md: se relaja la
# FORMA, nunca la nutricion.
#
# El primer peldano se llama "estricto" y no `None`: una clave que viaja por
# HTTP tiene que poder escribirse.
PELDANO_ESTRICTO = "estricto"

# Que suelta cada uno, dicho para quien lo va a elegir. Sin esto el selector
# ofreceria "proporcion_minima_visceras_higado_verdura", que es el nombre de
# una variable, no una opcion.
PELDANOS_EN_CRISTIANO = {
    PELDANO_ESTRICTO: (
        "Proporciones BARF completas",
        "Carne, hueso, vísceras, hígado y verdura dentro de sus rangos habituales, "
        "y hasta 2 suplementos."),
    "proporcion_minima_visceras_higado_verdura": (
        "Sin mínimo de vísceras, hígado y verdura",
        "Pueden quedarse a cero si no hacen falta. Sus topes máximos siguen puestos, "
        "y los de la carne y el hueso no se tocan."),
    "proporcion_minima_de_todas_las_categorias": (
        "Sin ningún mínimo de categoría",
        "Ninguna categoría está obligada a aparecer. Los máximos siguen puestos: la ración "
        "no se puede convertir en hígado y suplementos."),
    "proporcion_minima_y_un_suplemento_mas": (
        "Sin mínimos, y hasta 3 suplementos",
        "Un suplemento más de los dos habituales, para cerrar un nutriente que la comida "
        "no alcanza."),
    "proporcion_minima_y_dos_suplementos_mas": (
        "Sin mínimos, y hasta 4 suplementos",
        "Dos suplementos más. Es lo más lejos que llega la escalera sin tocar ningún techo."),
    "tope_maximo_de_visceras_higado_y_verdura": (
        "Sin tope de vísceras, hígado y verdura",
        "Se levanta el techo de lo accesorio — el 10 % de verdura es lo que suele bloquear "
        "una pancreatitis. Los mínimos de carne y hueso siguen intactos: son lo que hace "
        "que la ración siga siendo una ración."),
}


def _peldanos_publicos(hay_comida_de_verdad=True):
    """La escalera con nombre y explicacion, en su orden real.

    Se construye recorriendo `_escalera_de_relajacion()` y NO escribiendo la
    lista a mano: si manana se anade un peldano y esta lista fuera aparte, el
    selector del veterinario ofreceria una escalera que ya no es la que
    aplica el motor. Es la misma razon por la que los topes de patologia se
    sirven leyendo `patologias.json` en vez de copiarlos.
    """
    salida = []
    for orden, (_m, supl, clave) in enumerate(_escalera_de_relajacion(hay_comida_de_verdad)):
        clave = clave or PELDANO_ESTRICTO
        titulo, detalle = PELDANOS_EN_CRISTIANO.get(clave, (clave, ""))
        salida.append({"clave": clave, "orden": orden, "titulo": titulo,
                       "que_se_suelta": detalle, "max_suplementos": supl})
    return salida


def _peldano_por_clave(clave, hay_comida_de_verdad=True):
    """(margenes, max_suplementos) del peldano pedido, o None si no existe.

    Devolver None y no reventar es deliberado: una clave que no existe se
    trata como "no ha pedido ninguno" y se recorre la escalera de siempre.
    Un 400 aqui dejaria sin menu a alguien por un nombre mal escrito.
    """
    if not clave:
        return None
    for margenes, supl, k in _escalera_de_relajacion(hay_comida_de_verdad):
        if (k or PELDANO_ESTRICTO) == clave:
            return margenes, supl
    return None


@app.get("/relajacion")
def listar_peldanos():
    """Los peldanos de la escalera, para que un profesional pueda elegir.

    Se sirven los siete -- el ultimo incluido -- porque esto es la tabla, no
    una decision sobre un paciente concreto: si al formular no hay carne y
    hueso de donde tirar, ese peldano simplemente no se aplica (ver
    `_hay_comida_de_verdad`). Decir aqui que no existe seria esconder una
    opcion que para casi todos los pacientes si existe.
    """
    return {
        "que_es": ("Los peldaños que el motor recorre cuando no existe menú con las "
                   "proporciones de BARF habituales. Solo mueven la FORMA de la ración: "
                   "los 43 requisitos de FEDIAF, el ratio Ca:P y los topes de seguridad y "
                   "de patología son idénticos en todos."),
        "peldanos": _peldanos_publicos(True),
    }


def _aviso_de_lo_que_falta(gramos, al, categorias_excluidas=None):
    """
    Qué categorías del BARF se han quedado fuera del menú. Se dice en
    cristiano y sin alarmar: el menú cumple los 30 requisitos igual, pero
    la usuaria tiene derecho a saber por qué este no lleva vísceras
    cuando todos los demás sí.
    """
    presentes = {al.get(n, {}).get("categoria") for n in gramos}
    # Lo que el usuario quitó a propósito no es una sorpresa que haya que
    # explicarle: ya sabe por qué no está. El aviso es solo para lo que
    # falta SIN que nadie lo pidiera.
    a_proposito = set(categorias_excluidas or [])
    ausentes = [c for c in MARGENES_V2 if c not in presentes and c not in a_proposito]
    if not ausentes:
        return None
    nombres = {"Hueso carnoso": "hueso carnoso", "Carne muscular": "carne muscular",
               "Verduras y frutas": "verdura o fruta", "Vísceras": "vísceras",
               "Hígado": "hígado"}
    lista = [nombres.get(c, c.lower()) for c in ausentes]
    if len(lista) == 1:
        que = lista[0]
    else:
        que = ", ".join(lista[:-1]) + " ni " + lista[-1]
    return ("Con las restricciones de este perro no había forma de incluir " + que +
            " sin incumplir algo. El menú cumple igualmente los 30 requisitos "
            "y todos los límites de seguridad.")


MARGEN_SEGURIDAD_CRONICA_MENU_UNICO = 0.75  # mismo criterio que el de /menu/semana


def _presupuesto_menu_unico_semana_completa(der_objetivo):
    from seguridad import (
        TOPE_TIAMINASA_KCAL, TOPE_MERCURIO_KCAL, TOPE_VITD_KCAL, TOPE_YODO_KCAL,
        TOPE_SELENIO_KCAL,
    )
    return {
        "tiaminasa": TOPE_TIAMINASA_KCAL * MARGEN_SEGURIDAD_CRONICA_MENU_UNICO,
        "mercurio": TOPE_MERCURIO_KCAL * MARGEN_SEGURIDAD_CRONICA_MENU_UNICO,
        "vitD": TOPE_VITD_KCAL * der_objetivo / 1000.0 * MARGEN_SEGURIDAD_CRONICA_MENU_UNICO,
        "yodo": TOPE_YODO_KCAL * der_objetivo / 1000.0 * MARGEN_SEGURIDAD_CRONICA_MENU_UNICO,
        "selenio": TOPE_SELENIO_KCAL * der_objetivo / 1000.0 * MARGEN_SEGURIDAD_CRONICA_MENU_UNICO,
    }



@app.post("/menu/semana")
def endpoint_menu_semana(datos: PeticionMenu, numero_de_menus: int = 1):
    """Genera TODOS los menús de una rotación semanal en una sola
    llamada, con el presupuesto semanal de seguridad crónica repartido
    y endurecido en cada uno según lo que ya llevan los anteriores --
    ver el bloque de comentarios justo arriba para el porqué completo."""
    observabilidad.etiquetar(endpoint="/menu/semana", etapa=datos.etapa_requisitos)
    # se declara FUERA del try porque el except de abajo lo lee para
    # contarle a Sentry cuántos menús se habían generado antes del fallo:
    # si se inicializara dentro, un error en cargar_v2() dejaría la
    # variable sin definir y el propio except reventaría.
    menus_generados = []
    try:
        al, req = cargar_v2()
        n = max(1, min(8, numero_de_menus))
        base_dias = 7 // n
        resto_dias = 7 % n
        dias_por_menu = [base_dias + (1 if i < resto_dias else 0) for i in range(n)]

        presupuesto_restante = _presupuesto_semanal_inicial(datos.der_objetivo)
        especies_usadas = []

        for i in range(n):
            dias_este = dias_por_menu[i]
            dias_restantes_incluido_este = sum(dias_por_menu[i:])
            presupuesto_para_este = _presupuesto_para_menu_actual(
                presupuesto_restante, dias_restantes_incluido_este)

            # ⚠️ AÑADIDO (25 agosto) — CADA MENÚ CONSERVA LO SUYO. El fallo
            # que ella vio: "el primero lo ha respetado un poco más pero el
            # segundo... prácticamente nada". El frontend recogía los
            # alimentos de menus[0] y los mandaba para TODOS, así que el
            # menú 2 recibía los del 1.
            preferir_este = list((datos.preferir_por_menu or [])[i] or []) \
                if i < len(datos.preferir_por_menu or []) else []

            # ⚠️ Y SI SE CONSERVA, NO SE ROTA. `especies_usadas` está para
            # que dos menús automáticos no salgan con la misma proteína --
            # pero conservando, la variedad ya la da el menú original, y
            # evitar la especie del menú 1 es justo empujar al menú 2 fuera
            # de sus propios alimentos. Las dos cosas a la vez se anulan:
            # se pide conservar y se obliga a cambiar.
            datos_este = datos.model_copy(update={
                "presupuesto_semanal_restante": presupuesto_para_este,
                "evitar_especies": list(datos.evitar_especies or [])
                                   + ([] if preferir_este else especies_usadas),
                "preferir_alimentos": preferir_este or None,
            })
            resultado = _garantizar_verificado(
                _resolver_menu_v2_interno(datos_este),
                datos.der_objetivo, datos.etapa_requisitos, datos.peso_perro_kg,
                origen="/menu/semana", al=al, req=req,
                patologias=datos.patologias,
                peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
                peso_objetivo_kg=_peso_de_referencia(datos)[0])

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
            presupuesto_restante = _restar_del_presupuesto(
                presupuesto_restante, consumo, dias_este)

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
        # mismo motivo que en /menu/v2: el except se traga la excepcion
        # a proposito, asi que hay que avisar a Sentry explicitamente.
        observabilidad.capturar(e, endpoint="/menu/semana",
                                etapa=datos.etapa_requisitos,
                                der_objetivo=datos.der_objetivo,
                                peso_perro_kg=datos.peso_perro_kg,
                                numero_de_menus=numero_de_menus,
                                menus_ya_generados=len(menus_generados))
        return {"factible": False,
                "motivo": f"Ha fallado algo inesperado generando la semana ({type(e).__name__}). "
                          "Inténtalo de nuevo -- si se repite, dínoslo."}


# ─────────────────────────────────────────────────────────────────────────────
# LO QUE ELIGES A MANO ES LO QUE HAY
#
# ⚠️ CASO REAL ENCONTRADO POR LA USUARIA (24 agosto): "este menú de
# personalizar me ha metido 3 verduras, no debería... yo puse zanahoria y ha
# metido dos más". Cierto: Zanahoria, y además Espinaca y Canónigos.
#
# Esta lista existía desde el 5 de agosto con solo TRES categorías dentro
# (carne, pescado, hueso), y el comentario decía "vísceras, hígado, verduras
# y extras se quedan siempre libres, tal como se pidió". Lo que se pidió
# entonces fue que no metiera una tercera CARNE; que las verduras siguieran
# libres no se pidió, se dio por bueno de paso. Y es incoherente: la
# pantalla de Personalizar ofrece SEIS categorías, así que elegir en las
# otras tres no servía de nada y no había forma de saberlo mirando.
#
# La regla ahora es una sola, y se puede explicar en una frase: LA APP
# RESPETA TODAS LAS CATEGORÍAS QUE TE DEJA ELEGIR. Si esta lista y la
# pantalla dejan de coincidir, el fallo vuelve — por eso van con el mismo
# nombre en los dos sitios (ver CATEGORIAS en App.jsx, canislab-web).
#
# Lo que NO entra aquí, a propósito: suplementos (Multivitamínico, Omega-3,
# Calcio, Yodo, Hierro, Fibra, Vitamina B) y Extras (sal, aceites, semillas,
# huevo). No se eligen a mano en ninguna pantalla, y son justo la
# herramienta con la que el motor cierra los 30 requisitos. Cerrarlos sería
# quitarle el destornillador.
#
# Y no es una restricción dura: si con SOLO lo elegido no hay menú posible,
# se baja al nivel 2 (lo elegido sí o sí, el motor puede añadir) y se DICE
# qué tuvo que añadir. Sin menú no se queda nadie.
CATEGORIAS_QUE_ELIGE_EL_USUARIO = (
    "Carne muscular", "Pescados y mariscos", "Hueso carnoso",
    "Vísceras", "Hígado", "Verduras y frutas",
)


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
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO,
    # pedido expreso: "si generas UN SOLO menú en Personalizar y se le
    # va a dar al perro toda la semana, los límites semanales (vitamina
    # D, tiaminasa/pescado) tienen que protegerse YA en ese único menú,
    # como restricción dura -- no como aviso". Hasta ahora, el sistema
    # de presupuesto semanal (MARGEN_SEGURIDAD_CRONICA, ver
    # _presupuesto_semanal_inicial más arriba) SOLO se activaba cuando
    # se pedían varios menús a la vez vía /menu/semana -- un único menú
    # generado aquí (el camino que usa Personalizar, o Automático con
    # 1 solo menú) usaba solo el tope DIARIO, sin margen de repetición
    # semanal, aunque ese único menú fuera literalmente lo único que el
    # perro comería cada día de la semana. Por diseño, NO se puede saber
    # de antemano si este menú es "uno de varios" o "el único, comido
    # los 7 días" -- así que, salvo que quien llama (como /menu/semana)
    # ya haya calculado su propio presupuesto más preciso y lo pase
    # explícitamente, se asume aquí el caso más exigente por defecto:
    # que este menú se coma TODOS los días de la semana.
    #
    # ⚠️ CORREGIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO, pedido
    # expreso por segunda vez: el aviso de sardina/vitD seguía
    # apareciendo en un único menú de Personalizar a pesar del arreglo
    # de arriba. Causa real: _presupuesto_semanal_inicial +
    # _presupuesto_para_menu_actual (las funciones de /menu/semana)
    # SOLO endurecen vitD/yodo -- tiaminasa/mercurio, al ser una
    # fracción diaria plana en vez de un total acumulable, nunca se
    # tocaban con ese mecanismo. Se usa ahora la función dedicada al
    # caso de un único menú, que sí endurece los 5 límites por igual.
    if datos.presupuesto_semanal_restante is None:
        datos.presupuesto_semanal_restante = _presupuesto_menu_unico_semana_completa(
            datos.der_objetivo)
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
    # Quien orquesta varias generaciones dentro de una misma petición
    # (ver /menu/varios-perros) reparte el tiempo. Solo puede apretar.
    if datos.presupuesto_segundos is not None:
        PRESUPUESTO_SEGUNDOS = max(3.0, min(PRESUPUESTO_SEGUNDOS, float(datos.presupuesto_segundos)))

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

    def tiempo_de_un_intento():
        """Lo que se le da a UNA llamada del solver, que NO es todo lo que
        queda.

        ⚠️ AÑADIDO (8 septiembre, noche) — CASO REAL MEDIDO, y el fallo era de
        REPARTO, no del motor.

        Al poner el techo de fósforo del perro adulto sano (2000 mg/1000 kcal,
        SACN5 Tabla 13-3), el toy de 1,5 kg empezó a quedarse sin menú 1 de cada
        3 veces con el presupuesto apretado a 3 s -- que es como el BLOQUE 43
        imita a Render, que va 6-10 veces más lento que este equipo.

        Diagnosticado, y no era infactibilidad:

            sin el techo, 1 s ....  0 sin menú de 15
            con el techo, 1 s ....  3 de 15        (el problema es MÁS LENTO)
            con el techo, 8 s ....  0 de 15        (con tiempo, sale siempre)

        Y aflojar la exigencia de optimalidad NO lo arregla (`mip_rel_gap` a
        0,30 / 0,50 / 0,80 falla igual, 2-6 de 15): lo que le cuesta a HiGHS no
        es demostrar el óptimo, es encontrar la primera solución entera.

        Lo que SÍ lo arregla es **bajar de peldaño**:

            peldaño 0 (2 suplementos), 3 s ....  3 sin menú de 15
            peldaño 4 (4 suplementos), 3 s ....  0 de 15

        Con cuatro huecos de suplemento el motor puede meter cáscara de huevo
        --calcio con un Ca:P de 370:1, o sea calcio sin fósforo-- y el techo
        deja de apretar. Es exactamente para lo que existe la escalera.

        **El problema era que nunca llegaba a bajar.** `time_limit` era
        `tiempo_restante()`, o sea TODO el presupuesto: con 3 s, la primera
        llamada se los comía enteros, los dos reintentos recibían el mínimo de
        1 s cada uno (y ya está medido que reintentar el mismo peldaño no
        ayuda), y el bucle de la escalera se encontraba con `tiempo_restante()
        <= 1.5` y se rompía sin pisar un solo peldaño.

        Ahora una llamada nunca se lleva más del 40 % del presupuesto, así que
        siempre queda para bajar. Con 24 s (lo normal) son 9,6 s a la primera,
        de sobra para cualquier caso medido; con 3 s son 1,2 s y quedan casi 2
        para la escalera, que es donde está la solución.
        """
        return max(1.0, min(tiempo_restante(), PRESUPUESTO_SEGUNDOS * 0.4))

    excluidos = list(datos.especies_excluidas or []) + list(datos.nombres_excluidos or [])

    # ⚠️ CONECTADO (5 agosto, noche): las patologías existían en el modelo
    # y en el perfil que manda la app, pero el motor nunca las miraba.
    # Las que dependen de analíticas (estruvita/cistina/urato) BLOQUEAN
    # la generación automática — se deriva al veterinario en vez de dar
    # un menú que podría empeorar el problema.
    from motor_completo import patologias_bloquean, avisos_de_patologias
    # ⚠️ CON LA ETAPA (25 agosto): la insuficiencia renal se puede apoyar en
    # un adulto bajando el fósforo, pero en un cachorro o una gestante el
    # fósforo que hay que quitarle es MENOS del que necesita para crecer.
    # Ahí no hay menú que dar, y decirlo es mejor que dar uno que no sirve.
    # ⚠️ AL VETERINARIO ACREDITADO NO SE LE BLOQUEA (29 agosto). El motivo
    # de bloquear era «esto lo tiene que pautar un veterinario»; cuando el
    # que está delante ES el veterinario, el muro solo lo manda a hacerlo
    # en una hoja de cálculo, donde nadie verifica nada. La frontera de
    # verdad —la que sí exige firma— es pautar por DEBAJO de los mínimos de
    # FEDIAF, y eso sigue sin hacerse. Ver VETERINARIOS.md.
    _prof = _es_profesional_acreditado(getattr(datos, "token_usuario", None))
    bloqueantes = patologias_bloquean(datos.patologias, datos.etapa_requisitos,
                                      es_profesional=_prof)
    if bloqueantes:
        return {"factible": False, "requiere_veterinario": True,
                "motivo": " ".join(avisos_de_patologias(bloqueantes, datos.etapa_requisitos))}

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
    # ⚠️ `not datos.preferir_alimentos` (25 agosto): las vías rápidas sirven
    # un menú YA CALCULADO, de catálogo. No miran ni pueden mirar qué
    # alimentos se quieren conservar, así que si hay algo que preferir hay
    # que resolver de verdad. Sin este guardia, "regenerar con los mismos
    # ingredientes" devolvía un menú enlatado y la preferencia no se
    # aplicaba nunca -- que es justo el fallo que esto viene a arreglar.
    if (datos.modo == "personalizar" and datos.tamano and not excluidos
            and not datos.patologias and not (datos.forzar_presencia or datos.nombres_alimentos)
            and not datos.preferir_alimentos
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
    # restringe cada una de estas categorías a SOLO lo elegido a mano
    # (dejando los gramos libres, eso sí), y solo si con eso no hay
    # solución viable se cae a dejar que el motor añada más -- avisando
    # de qué tuvo que añadir, con el mismo criterio que ya se usa en
    # todos los demás avisos de esta app.
    CATEGORIAS_A_RESTRINGIR = CATEGORIAS_QUE_ELIGE_EL_USUARIO

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
    elif (datos.modo == "automatico" and not excluidos and not datos.patologias
          and not datos.categorias_excluidas and not datos.preferir_alimentos):
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
                    margenes_categoria=MARGENES_V2, max_suplementos=2, forzar=base, time_limit=tiempo_de_un_intento(),
                    presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
                    # ⚠️ AÑADIDO (28 agosto): esta vía era la única de las
                    # cuatro que llaman al motor que NO le pasaba el peso
                    # adulto esperado, así que el mínimo reforzado de calcio
                    # de las razas grandes en crecimiento no entraba como
                    # restricción -- el mismo olvido que en su día tiró el
                    # tope de fósforo del renal al editar.
                    peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
                    # ⚠️ La via rapida tambien: si escalara sobre el peso real
                    # de un perro con sobrepeso pediria mas nutriente del que
                    # toca, y si no escalara daria la densidad de un perro de
                    # mantenimiento a una racion de bajada. Las dos mal.
                    peso_objetivo_kg=_peso_de_referencia(datos)[0],
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

    # Vale en cualquier modo: en "aprovechar" se suma a lo que ya venía por
    # `nombres_alimentos`, y en "personalizar" convive con lo forzado -- lo
    # elegido a mano entra sí o sí, y del resto se prefiere lo que ya había.
    if datos.preferir_alimentos:
        preferir = list(dict.fromkeys([*(preferir or []), *datos.preferir_alimentos]))

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
    def _intentar_generacion(forzar_este, restringir_a_elegidos_este,
                             margenes=None, max_supl=None, soltar=None):
        """Un intento completo: llamada + reintentos para mejorar a
        verde mientras quede presupuesto de tiempo -- misma lógica que
        ya existía, solo que reutilizable para los tres niveles.

        `soltar` SOLO lo usa el diagnóstico de choque entre patologías, que
        tira los menús que construye y se queda con el texto. Ningún camino
        que entregue un menú lo pasa nunca: lo comprueba el BLOQUE 52."""
        # ⚠️ EL ESTADO DEL SOLVER, PARA NO REINTENTAR LO IMPOSIBLE (10
        # septiembre). Ver el comentario largo del bucle de reintentos de más
        # abajo: distinguir «HiGHS ha PROBADO que no hay» de «se le acabó el
        # reloj» es lo que ahorra 10 de las 16 llamadas al solver del perro
        # pequeño con patología. El diccionario se reutiliza en cada llamada:
        # siempre vale lo que dijo la ÚLTIMA.
        _estado_solver = {}
        ok_i, gramos_i = resolver_v2(
            datos.der_objetivo, datos.etapa_requisitos, al, req,
            datos.peso_perro_kg, dosis_maxima_fabricante,
            excluidos=excluidos or None,
            margenes_categoria=(margenes if margenes is not None else _margenes_base),
            max_suplementos=(max_supl if max_supl is not None else _supl_base),
            time_limit=tiempo_de_un_intento(),
            estado_del_solver=_estado_solver,
            forzar=forzar_este, preferir=preferir,
            patologias=datos.patologias, restringir_especie=datos.restringir_especie,
            peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
            peso_objetivo_kg=_peso_de_referencia(datos)[0],
            evitar_especies=datos.evitar_especies,
            restringir_a_elegidos=restringir_a_elegidos_este,
            categorias_excluidas=datos.categorias_excluidas,
            presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
            soltar_limites_patologia=soltar,
        )
        # ⚠️ VERIFICAR CUESTA 1,6 ms: NO SE PUEDE QUEDAR SIN TIEMPO (29 agosto).
        #
        # Aquí la comprobación del presupuesto estaba en el `while` que
        # envuelve al `verificar_v2`, así que cuando el solver devolvía el
        # menú justo al agotarse el reloj -- que es lo normal en Render, que
        # va 6-10 veces más lento que este equipo -- el bucle no llegaba a
        # entrar NI UNA VEZ, `ficha_i` se quedaba en None y un menú perfecto
        # se tiraba. Después salía "el cálculo está tardando más de lo
        # normal", con el menú ya calculado en la mano.
        #
        # Es el mismo fallo que el de aceptar la solución del solver cuando
        # salta su time_limit, un piso más arriba: teníamos la respuesta y la
        # tirábamos por mirar el reloj. El presupuesto existe para limitar lo
        # CARO -- resolver, que son segundos --, no lo que cuesta menos que
        # parpadear.
        ficha_i = (verificar_v2(gramos_i, al, req, datos.der_objetivo, datos.etapa_requisitos)
                   if ok_i else None)
        while (ok_i and ficha_i and ficha_i["semaforo"] != "verde"
               and time.time() - t_inicio_total < PRESUPUESTO_SEGUNDOS):
            ok2, gramos2 = resolver_v2(
                datos.der_objetivo, datos.etapa_requisitos, al, req,
                datos.peso_perro_kg, dosis_maxima_fabricante,
                excluidos=excluidos or None,
                margenes_categoria=(margenes if margenes is not None else MARGENES_V2),
                max_suplementos=max_supl, time_limit=tiempo_de_un_intento(),
                forzar=forzar_este, preferir=preferir,
                patologias=datos.patologias, restringir_especie=datos.restringir_especie,
                peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
            peso_objetivo_kg=_peso_de_referencia(datos)[0],
                evitar_especies=datos.evitar_especies,
                restringir_a_elegidos=restringir_a_elegidos_este,
                categorias_excluidas=datos.categorias_excluidas,
                presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
            )
            if ok2:
                ok_i, gramos_i = ok2, gramos2
                ficha_i = verificar_v2(gramos_i, al, req, datos.der_objetivo,
                                       datos.etapa_requisitos)
            else:
                break

        # ⚠️ AÑADIDO (7 septiembre) — CASO REAL: al corregir el umbral de
        # calcio de raza grande (25kg -> 15kg, ver motor_completo.py), un
        # cachorro de 10kg con peso adulto esperado 20kg, sin hueso carnoso
        # y con 3 alergias (Pollo/Ternera/Cordero excluidas) empezó a fallar
        # de forma intermitente: "infactible" 2 de 6 veces con la misma
        # petición exacta, probado en aislado. No es un caso imposible --es
        # un caso AL LÍMITE, igual que el toy de 1,5kg del BLOQUE 43-- y el
        # bucle de arriba no lo cubría: solo reintenta cuando YA hay una
        # solución de la que partir (`ok_i` true) para mejorarla a verde,
        # nunca cuando la primera llamada sale directamente infactible.
        # Mismo argumento que ya se aplicó a /menu/varios-perros: "el motor
        # lleva aleatoriedad a propósito... la misma petición sale casi
        # siempre a la segunda". Tope de 2 intentos extra (no ilimitados
        # como el bucle de arriba) porque aquí cada intento es una llamada
        # entera al solver, no un ajuste rápido -- si el caso es de verdad
        # irresoluble, más vueltas solo queman el presupuesto de Render.
        #
        # ⚠️ Y NO SE REINTENTA LO QUE ESTÁ DEMOSTRADO IMPOSIBLE (10 septiembre).
        #
        # Este bucle se puso porque «el motor lleva aleatoriedad a propósito» y
        # la misma petición sale casi siempre a la segunda. Es verdad cuando lo
        # que pasó fue que se acabó el reloj -- ahí otra semilla llega antes --,
        # y es FALSO cuando HiGHS ha demostrado que no hay solución: lo único
        # que cambia entre llamadas es el ruido del OBJETIVO, y un objetivo no
        # vuelve factible un problema infactible.
        #
        # CASO REAL MEDIDO: chihuahua de 3 kg (DER 260) con `renal`. La API
        # tardaba 21-24 s y hacía 16 llamadas al solver; DIEZ eran reintentos de
        # peldaños que ya habían salido `status 2` (infactible demostrado), con
        # las tres semillas probadas dando lo mismo en los cinco primeros
        # peldaños y menú siempre en el sexto. La escalera sola tarda 7,2 s. En
        # Render, 6-10 veces más lento, eso es la diferencia entre dar menú y
        # contestar «está tardando más de lo normal» -- que es lo que pasaba.
        #
        # Se mira SOLO el status 2. Si el solver devolvió una solución que
        # rechazó la red de seguridad de las categorías (status 0 y `ok_i`
        # falso), reintentar SÍ sirve: ahí otra semilla da otro menú.
        _reintentos_infactible = 0
        while (not ok_i and _reintentos_infactible < 2
               and not _estado_solver.get("infactible_demostrado")
               and time.time() - t_inicio_total < PRESUPUESTO_SEGUNDOS):
            _reintentos_infactible += 1
            ok_i, gramos_i = resolver_v2(
                datos.der_objetivo, datos.etapa_requisitos, al, req,
                datos.peso_perro_kg, dosis_maxima_fabricante,
                excluidos=excluidos or None,
                margenes_categoria=(margenes if margenes is not None else MARGENES_V2),
                max_suplementos=max_supl, time_limit=tiempo_de_un_intento(),
                forzar=forzar_este, preferir=preferir,
                patologias=datos.patologias, restringir_especie=datos.restringir_especie,
                peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
                peso_objetivo_kg=_peso_de_referencia(datos)[0],
                evitar_especies=datos.evitar_especies,
                restringir_a_elegidos=restringir_a_elegidos_este,
                categorias_excluidas=datos.categorias_excluidas,
                presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
                estado_del_solver=_estado_solver,
            )
            ficha_i = (verificar_v2(gramos_i, al, req, datos.der_objetivo, datos.etapa_requisitos)
                       if ok_i else None)
        return (ok_i and ficha_i and ficha_i["semaforo"] == "verde"), gramos_i, ficha_i

    # ⚠️ EL PELDANO ELEGIDO (8 septiembre). Ver `_peldanos_publicos`.
    #
    # Sin `peldano` esto vale (MARGENES_V2, 2) y no cambia absolutamente
    # nada: es el primer peldano de la escalera, o sea lo de siempre. Con
    # `peldano`, se formula EN ese peldano y NO se baja solo -- que es justo
    # lo que pide un profesional: si el elige soltar el tope de la verdura,
    # no quiere que ademas se le suelte el minimo del hueso por detras.
    _hay_comida_para_peldano = _hay_comida_de_verdad(al, excluidos, datos.categorias_excluidas)
    _peldano_pedido = _peldano_por_clave(getattr(datos, "peldano", None),
                                         _hay_comida_para_peldano)
    _margenes_base = _peldano_pedido[0] if _peldano_pedido else MARGENES_V2
    _supl_base = _peldano_pedido[1] if _peldano_pedido else 2

    aviso_extra_alimentos = None
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
                    aviso_extra_alimentos = (
                        "Con solo lo que elegiste no había una combinación viable, así que "
                        "también se ha añadido: " + ", ".join(anadidos) + "."
                    )
    else:
        ok, gramos, ficha_intento = _intentar_generacion(forzar, None)

    if not ok and datos.modo == "personalizar":
        # igual que hacía /menu (el viejo): si forzar lo elegido a mano
        # deja sin solución, se reintenta libre — mejor un menú con aviso
        # que un error sin más.
        #
        # ⚠️ CORREGIDO (21 agosto) — FALLO GRAVE ENCONTRADO EN UNA PRUEBA
        # DE ESFUERZO: este reintento se dejaba por el camino DOS cosas
        # que no son opinables.
        #
        #   · `categorias_excluidas`. Un perro al que se le ha quitado el
        #     hueso carnoso (senior sin dientes, mandíbula operada) recibía
        #     costillas de cordero en cuanto el forzado fallaba y se caía
        #     aquí. La regla del proyecto es explícita: las categorías
        #     excluidas a mano no se tocan jamás, pueden ser médicas. Y el
        #     filtro final no lo cazaba, porque un menú CON hueso cumple
        #     los 30 requisitos perfectamente -- "este perro no puede
        #     masticar" no es un nutriente.
        #
        #   · `peso_adulto_esperado_kg`. Es lo que activa el tope de
        #     calcio de cachorro de raza grande. Sin él, el menú de
        #     rescate de un cachorro de raza grande se calculaba sin ese
        #     tope: exactamente el problema (osteocondrosis) que ese
        #     límite existe para evitar.
        #
        # Lo que SÍ se suelta aquí a propósito es la elección manual que
        # acaba de fallar (`forzar` y `restringir_especie`): ése es el
        # sentido de este rescate, y se avisa con `no_se_pudo_forzar`.
        # `evitar_especies` se pasa porque es solo una preferencia (nunca
        # puede hacer fallar nada) y sin ella la rotación de proteína de
        # una semana se rompía justo en los menús que caían aquí.
        ok, gramos = resolver_v2(
            datos.der_objetivo, datos.etapa_requisitos, al, req,
            datos.peso_perro_kg, dosis_maxima_fabricante,
            excluidos=excluidos or None,
            margenes_categoria=_margenes_base, max_suplementos=_supl_base,
            time_limit=tiempo_de_un_intento(),
            patologias=datos.patologias,
            categorias_excluidas=datos.categorias_excluidas,
            peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
            peso_objetivo_kg=_peso_de_referencia(datos)[0],
            evitar_especies=datos.evitar_especies,
            presupuesto_semanal_restante=datos.presupuesto_semanal_restante,
        )
        no_se_pudo_forzar = ok
    else:
        no_se_pudo_forzar = False

    # ⚠️ AÑADIDO (20 agosto) — LA ESCALERA. Antes, llegar aquí sin menú
    # era el final: "no existe ninguna combinación". Medido, casi nunca
    # era verdad -- lo que no existía era una combinación que además
    # respetara nuestras proporciones de BARF. Antes de rendirse se
    # recorren los peldaños, soltando SOLO esas proporciones (ver
    # _escalera_de_relajacion, arriba, para lo que no se suelta jamás).
    relajaciones = []
    hay_comida = _hay_comida_para_peldano
    # ⚠️ CON PELDANO ELEGIDO NO SE BAJA SOLO (8 septiembre). Bajar seria
    # cambiarle la decision sin decirselo, que es lo contrario de por que
    # existe poder elegirlo. Si en ese peldano no hay menu, se dice que no en
    # ese peldano -- y el elige otro.
    if not ok and not _peldano_pedido:
        for margenes_peldano, supl_peldano, que_se_suelta in _escalera_de_relajacion(hay_comida)[1:]:
            if tiempo_restante() <= 1.5:
                break  # sin tiempo: mejor no factible que un timeout de Render
            ok, gramos, ficha_intento = _intentar_generacion(
                forzar, None, margenes=margenes_peldano, max_supl=supl_peldano)
            if ok:
                relajaciones.append(que_se_suelta)
                break

    if not ok:
        # ⚠️ SI EL MOTOR DICE QUE ES IMPOSIBLE POR ARITMETICA, SE DICE ESO
        # (28 agosto). Cuando el minimo escalado de un nutriente supera su
        # maximo, no hay ninguna combinacion que lo arregle y tampoco la hay
        # quitando restricciones. El mensaje de siempre -«quita alguna
        # restriccion y vuelve a probar»- manda a la usuaria a un callejon
        # sin salida: puede quitarlas todas y seguira sin salir.
        _imp = (gramos or {}).get("_imposible") if isinstance(gramos, dict) else None
        if _imp:
            return {"factible": False, "motivo": _imp, "imposible_por_aritmetica": True}
        # ⚠️ QUEDARSE SIN TIEMPO NO ES QUE NO EXISTA (29 agosto).
        #
        # Si el presupuesto se ha agotado, aquí se llegaba igual que si se
        # hubieran recorrido todos los peldaños, y se le contestaba a la
        # usuaria "no existe ninguna combinación... quita alguna restricción
        # y vuelve a probar". Es MENTIRA, y de la peor clase: la manda a
        # deshacer alergias o patologías para arreglar algo que no tiene
        # nada que ver, y el menú que sí existe se lo habría dado si le
        # hubiera dado tiempo.
        #
        # CASO REAL REPRODUCIDO, con el presupuesto apretado a mano para
        # que no dependa de lo rápido que vaya la máquina (`presupuesto_
        # segundos`, que es lo que hace /menu/varios-perros al repartir):
        #     cachorro en crecimiento de 10 kg, 24 s -> menú, 8 de 8
        #     el mismo cachorro con  4 s -> "no existe ninguna combinación"
        #     el mismo cachorro con  6 s -> "no existe ninguna combinación"
        # y el tiempo de respuesta era exactamente el presupuesto (4,0 s y
        # 6,0 s): se acabó el tiempo, no las combinaciones.
        #
        # Importa más de lo que parece porque el reparto de /menu/varios-
        # perros y /menu/semana da a cada perro una fracción de los 24 s, y
        # Render va más lento que cualquier portátil. El cachorro en
        # crecimiento es el caso más caro que hay (yodo y calcio a la vez).
        #
        # El mensaje es el MISMO que ya se daba unas líneas más arriba
        # cuando el presupuesto se agotaba en la vía del catálogo, a
        # propósito: el mismo motivo tiene que decir lo mismo.
        if time.time() - t_inicio_total >= PRESUPUESTO_SEGUNDOS - 1.5:
            return {"factible": False,
                    "motivo": "El cálculo está tardando más de lo normal para este "
                              "perro. Inténtalo de nuevo en un momento.",
                    "se_agoto_el_tiempo": True}
        # ⚠️ SIN EL NÚMERO ESCRITO (29 agosto). Aquí ponía "los 30
        # requisitos" y el motor ya verifica 42 desde que se encendieron los
        # aminoácidos: el mensaje que ve la usuaria decía una cifra y el
        # motor comprobaba otra. Es el mismo fallo que describe el CLAUDE.md
        # sobre el DER -- un número escrito en dos sitios se separa, y el
        # que está en un texto no lo cubre ninguna prueba.
        # Encontrado pidiendo un menú de hepatopatía contra producción.
        # ⚠️ ANTES DE RENDIRSE, DECIR QUÉ CHOCA (8 septiembre).
        #
        # CASO REAL MEDIDO: un adulto de 25 kg con `renal` + `pancreatitis`
        # no obtiene menú en ninguno de los seis peldaños -- y cada patología
        # POR SEPARADO sí lo obtiene. Lo único que se decía era el texto de
        # abajo, «quita alguna restricción y vuelve a probar», que está
        # escrito para un dueño. A un veterinario no le sirve: no hay ninguna
        # restricción que él pueda quitar, y sin saber cuál es el choque
        # tampoco puede decidir cuál cedería.
        #
        # `diagnosticar_choque_de_patologias` lo averigua por eliminación:
        # vuelve a resolver soltando UN límite cada vez y el que desbloquea
        # es culpable. En el caso medido tarda 2,2 s y contesta «el fósforo
        # de la renal (≤1200) contra la grasa de la pancreatitis (≤20)».
        #
        # ⚠️ NO ENTREGA NINGÚN MENÚ. Los menús que construye para preguntar
        # se tiran: de aquí solo sale texto, y el tope se sigue aplicando
        # igual. Lo vigila el BLOQUE 52.
        _choque = None
        if datos.patologias and tiempo_restante() > 3.0:
            try:
                from motor_completo import diagnosticar_choque_de_patologias
                _choque = diagnosticar_choque_de_patologias(
                    datos.patologias, datos.etapa_requisitos,
                    lambda soltar: _intentar_generacion(
                        forzar, None,
                        margenes=_escalera_de_relajacion(hay_comida)[-1][0],
                        max_supl=_escalera_de_relajacion(hay_comida)[-1][1],
                        soltar=soltar)[0],
                    peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg)
            except Exception as e:   # el diagnóstico NUNCA puede tumbar la respuesta
                observabilidad.capturar(e, endpoint="/menu/v2",
                                        nota="diagnostico de choque de patologias")
                _choque = None

        if _choque:
            _l = _choque["limites_que_chocan"]

            # ⚠️ UN RATIO NO SE DICE IGUAL QUE UN TOPE (10 septiembre). Su clave
            # es «calcio:fosforo:min», no un nutriente, y no va «por cada 1000
            # kcal» porque es adimensional. Sin esta rama la frase salía «exige
            # como mucho 1,1 de calcio:fosforo:min por cada 1000 kcal», que está
            # mal en las tres cosas: el sentido, la unidad y el nombre. Y este
            # texto es justo el que lee alguien que tiene que decidir qué límite
            # cede.
            def _frase_de_limite(x):
                if x["tipo"] == "ratio":
                    _n_r, _d_r, _s_r = x["clave"].split(":")
                    return (f"{x['nombre_patologia']} exige una relación "
                            f"{_NOMBRE_NUTRIENTE.get(_n_r, _n_r)}:"
                            f"{_NOMBRE_NUTRIENTE.get(_d_r, _d_r)} de "
                            f"{'al menos' if _s_r == 'min' else 'como mucho'} "
                            f"{_num_bonito(x['valor'])}:1")
                return (f"{x['nombre_patologia']} exige "
                        f"{'como mucho' if x['tipo'] != 'suelo' else 'al menos'} "
                        f"{_num_bonito(x['valor'])} {_UNIDAD_DE.get(x['clave'], '')} "
                        f"de {_NOMBRE_NUTRIENTE.get(x['clave'], x['clave'])} "
                        f"por cada 1000 kcal").strip()

            _texto = " y ".join(_frase_de_limite(x) for x in _l)
            return {
                "factible": False,
                "motivo": (
                    "No hay ninguna ración que cumpla a la vez los límites de las "
                    "patologías marcadas: " + _texto + ". Cada una por separado sí "
                    "tiene menú; juntas no queda margen. Elegir cuál de los dos "
                    "límites cede es una decisión clínica, así que no la toma la app."),
                "choque_de_patologias": [
                    {"patologia": x["patologia"],
                     "nombre_patologia": x["nombre_patologia"],
                     "nutriente": (x["clave"].rsplit(":", 1)[0] if x["tipo"] == "ratio"
                                   else x["clave"]),
                     "nombre_nutriente": _NOMBRE_NUTRIENTE.get(x["clave"], x["clave"]),
                     "tipo": x["tipo"],
                     "valor": x["valor"],
                     # Un ratio es adimensional: decir «/1000 kcal» de un
                     # cociente sería inventarse una unidad que no existe.
                     "unidad": ("ratio" if x["tipo"] == "ratio"
                                else ((_UNIDAD_DE.get(x["clave"]) or "") + "/1000 kcal").lstrip("/")),
                     "fuente": x["fuente"],
                     "por_que": x["por_que"]}
                    for x in _l],
                "se_intento_relajando": [p[2] for p in _escalera_de_relajacion(hay_comida)[1:]]}

        return {"factible": False,
                "motivo": "No existe ninguna combinación de alimentos accesibles "
                          "que cumpla todos los requisitos para este perro, ni "
                          "siquiera soltando las proporciones habituales del "
                          "BARF. Quita alguna restricción y vuelve a probar.",
                "se_intento_relajando": [p[2] for p in _escalera_de_relajacion(hay_comida)[1:]]}
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
    if aviso_extra_alimentos:
        resultado["aviso"] = aviso_extra_alimentos
    # ⚠️ AÑADIDO (20 agosto): si hubo que bajar por la escalera, se dice.
    # Un menú sin vísceras es perfectamente válido -- cumple los 30
    # requisitos igual -- pero no se parece a los demás, y la usuaria
    # tiene derecho a saber por qué, sin tener que preguntarlo.
    if relajaciones:
        resultado["se_relajo"] = relajaciones
        aviso_falta = _aviso_de_lo_que_falta(gramos, al, datos.categorias_excluidas)
        if aviso_falta:
            resultado["aviso_composicion"] = aviso_falta
    # ⚠️ EN QUE PELDANO SALIO, SIEMPRE (8 septiembre). `se_relajo` solo
    # aparece cuando hubo que bajar, asi que un menu normal no decia en que
    # peldano estaba -- y "no dice nada" y "estricto" se leen igual. Un
    # profesional que va a firmar necesita poder afirmar lo segundo.
    resultado["peldano"] = (
        getattr(datos, "peldano", None) if _peldano_pedido
        else (relajaciones[-1] if relajaciones else PELDANO_ESTRICTO))
    resultado["peldano_lo_eligio_el_profesional"] = bool(_peldano_pedido)
    return resultado


# ─────────────────────────────────────────────────────────────────────────────
# VARIOS PERROS EN LA MISMA CASA
#
# PEDIDO EXPRESO: "que el usuario tenga la opción de hacer menús totalmente
# diferentes para cada perro, o que pueda generar los menús para las
# características de todos los perros lo más parecidos posibles. Si un menú
# para dos perros cuadra y solo hay que cambiar las cantidades, perfecto. Si
# hay que cambiar uno, dos, tres alimentos, los menos cambios posibles."
#
# POR QUÉ NO SE RESUELVE "TODO A LA VEZ"
# La tentación era un único problema matemático con los dos perros dentro.
# No hace falta: el modo PERSONALIZAR ya hace exactamente la escalera que
# esto necesita, y está probado desde hace meses:
#
#   nivel 1 → solo los alimentos dados, nada más   → mismos alimentos, otras cantidades
#   nivel 2 → esos sí o sí, el motor puede añadir  → mismos + los que hagan falta
#   nivel 3 → libre                                → menú distinto
#
# Así que se resuelve UN perro y a los demás se les pide su menú "personalizado"
# con los alimentos del primero. Cada menú sigue pasando por
# _garantizar_verificado(): que se parezcan no es motivo para relajar nada.
#
# QUÉ PERRO VA PRIMERO — IMPORTA, Y MUCHO
# El primero manda: los demás se amoldan a él. Va primero el MÁS RESTRINGIDO
# (más alergias/categorías fuera/patologías y, a igualdad, el de ración más
# pequeña). Al revés no funciona: forzar los 7 alimentos de un pastor alemán
# en un chihuahua de 3 kg no cabe -- la ración entera del pequeño son ~137 g,
# y cada alimento forzado tiene un mínimo de porción real. Al perro grande le
# sobra sitio para amoldarse; al pequeño no.
# ─────────────────────────────────────────────────────────────────────────────

class PeticionVariosPerros(BaseModel):
    # ⚠️ EL TOKEN, NO UN BOOLEANO (29 agosto). Es la sesión de Supabase de
    # quien pide el menú. Sirve para saber si es un veterinario acreditado,
    # y con eso se le formulan las patologías que al dueño se le bloquean.
    # No se acepta un `modo_profesional` porque eso lo manda cualquiera.
    # Ver `_es_profesional_acreditado`.
    token_usuario: Optional[str] = None
    # Un PeticionMenu completo por perro: cada uno con SUS kcal, SU etapa,
    # SUS alergias. No se comparte nada entre ellos salvo, si se pide,
    # la lista de alimentos.
    perros: list[PeticionMenu]
    # Solo para poder redactar los avisos ("el menú de Cairo lleva..."). Si
    # no vienen, se dice "el segundo perro" y tan honesto.
    nombres: Optional[list[str]] = None
    # "parecidos" = amoldar los demás al primero. "distintos" = cada perro
    # su mejor menú, sin mirar a los otros (que es lo que pasa hoy si los
    # generas por separado).
    modo_conjunto: str = "parecidos"
    # ⚠️ AÑADIDO (21 agosto) — PEDIDO EXPRESO: "cuando generas los menús
    # para los dos perros no tienes ni el automático ni el personalizar,
    # solo te crea un menú y punto. Tiene que ser todo igual que cuando lo
    # generas para un perro, pero para dos".
    #
    # Cuántos menús distintos quiere cada perro para su semana. Con más de
    # uno se rota la proteína y se reparte el presupuesto semanal de
    # seguridad crónica entre ellos, exactamente igual que /menu/semana --
    # por perro, porque cada uno tiene sus propias kcal y por tanto su
    # propio presupuesto.
    numero_de_menus: int = 1
    # ⚠️ AÑADIDO (23 agosto) — CASO REAL ENCONTRADO POR LA USUARIA:
    # "he puesto en el menú 1 carne, hueso e hígado de conejo, y en el 2
    # todo de pollo, y me los ha dado los dos de pollo".
    #
    # Con UN perro la app manda una llamada por menú, cada una con lo suyo.
    # Con varios se manda UNA sola llamada, y los campos de personalizar
    # viven en cada perro -- o sea, uno solo para toda su semana. Lo
    # elegido para el último menú acababa aplicándose a todos.
    #
    # POR QUÉ SE ARREGLA AQUÍ Y NO EN LA APP: partirlo en una llamada por
    # menú desde la app habría dado a CADA menú el presupuesto semanal
    # entero de vitamina D, yodo, selenio y mercurio, cubriendo cada uno
    # solo 3 o 4 días. La semana sumada se pasaría de los límites de
    # seguridad crónica sin que nada avisara. Ese reparto lo lleva este
    # endpoint (`presupuesto`, `dias_por_menu`, `anotar_consumo`), así que
    # la personalización tiene que entrar aquí dentro, no partirse fuera.
    #
    # Una entrada por menú, en orden. `None` en una posición = ese menú va
    # como venga en el perro (compatibilidad: si no se manda nada, todo
    # funciona como antes). Cada entrada:
    #     {"forzar_presencia": [...], "restringir_especie": {cat: especie}}
    # Con las dos vacías, ese menú se hace en automático.
    personalizacion_por_menu: Optional[list[Optional[dict]]] = None


PRESUPUESTO_SEGUNDOS_VARIOS_PERROS = 24.0

# ⚠️ AÑADIDO (21 agosto) — SUELO DE TIEMPO POR MENÚ.
#
# Repartir el presupuesto a partes iguales entre perros x menús parecía
# razonable y no lo era: con 3 perros y 3 menús salían 2,7s por llamada, y
# medido, un cachorro con peso adulto esperado NO se resuelve en 3s (sí en
# 8). El resultado era que la casa entera se quedaba sin menús -- no por
# los datos, sino por asfixia de tiempo.
#
# Con un suelo, algunas combinaciones no caben enteras en el presupuesto.
# Eso se resuelve dando MENOS menús, no menús peores: se paran las rondas
# cuando se acaba el tiempo y se dice cuántos salieron, igual que ya hace
# /menu/semana. Un menú de menos es una molestia; un menú calculado a
# medias sería otra cosa.
SEGUNDOS_MINIMOS_POR_MENU = 6.0

# El PRIMER menú del perro que manda es el único que no puede fallar: sin
# él no hay nada a lo que amoldar a los demás y la casa entera se queda sin
# menús. Y es el más caro, porque es una búsqueda libre de verdad --
# medido, un cachorro con peso adulto esperado tarda ~8s. A los demás
# perros se les pasa la lista de alimentos ya decidida, así que su
# resolución es mucho más barata (medido: décimas de segundo).
#
# Por eso el reparto NO es a partes iguales: holgura para ese primer menú,
# y lo justo para los que solo tienen que encajar cantidades.
SEGUNDOS_PRIMER_MENU_DE_LA_BASE = 12.0
SEGUNDOS_AMOLDARSE = 4.0

# Solo lo toca el BLOQUE 48, para comparar la versión de antes con la de
# ahora en la misma máquina. En producción vale siempre False.
_PEOR_CASO_SIEMPRE_SOLO_PRUEBAS = False


def _comparar_menus(base_gramos, otro_gramos):
    """Qué cambia entre dos menús, en alimentos (no en cantidades).

    Las cantidades SIEMPRE cambian -- son perros distintos con kcal
    distintas -- así que cambiar de cantidad no cuenta como "un cambio".
    Lo que la usuaria nota al comprar y al porcionar es tener que comprar
    OTRA cosa, y eso es lo que se cuenta aquí.
    """
    base = set(base_gramos or {})
    otro = set(otro_gramos or {})
    return {
        "iguales": sorted(base & otro),
        "anadidos": sorted(otro - base),
        "quitados": sorted(base - otro),
        "cuantos_cambios": len(base ^ otro),
    }


def _resumen_de_parecido(cambios, nombre_perro, nombre_base):
    """Lo mismo, en cristiano. Quien lee esto está mirando la lista de la
    compra, no una tabla de diferencias."""
    if cambios["cuantos_cambios"] == 0:
        return (f"El menú de {nombre_perro} lleva exactamente los mismos alimentos "
                f"que el de {nombre_base}: solo cambian las cantidades. "
                f"Compras una vez y repartes.")
    partes = []
    if cambios["anadidos"]:
        partes.append("lleva además " + ", ".join(cambios["anadidos"]))
    if cambios["quitados"]:
        partes.append("no lleva " + ", ".join(cambios["quitados"]))
    cuantos = cambios["cuantos_cambios"]
    return (f"El menú de {nombre_perro} comparte {len(cambios['iguales'])} alimentos "
            f"con el de {nombre_base}, pero " + " y ".join(partes) + ". "
            f"{'Es un cambio' if cuantos == 1 else f'Son {cuantos} cambios'} "
            f"respecto a la compra de {nombre_base}.")


def _respuesta_varios_perros(perros_salida, modo_conjunto, nombre_base, numero_de_menus,
                             menus_no_dados=0, por_que_faltan="tiempo"):
    """La respuesta, con el resumen de parecido de toda la semana."""
    cambios_totales = sum((p.get("cambios") or {}).get("cuantos_cambios", 0)
                          for p in perros_salida)
    salida = {
        "factible": all(p.get("factible") for p in perros_salida),
        "modo_conjunto": modo_conjunto,
        "numero_de_menus": numero_de_menus,
        "cambios_totales": cambios_totales,
        "compra_unica": cambios_totales == 0,
        "perros": perros_salida,
    }
    if nombre_base:
        salida["perro_base"] = nombre_base
    if menus_no_dados > 0:
        # Se dice cuántos faltan y por qué. Callarlo dejaría a la usuaria
        # pensando que pidió 3 y le dimos 1 sin motivo.
        #
        # ⚠️ Y SE DICE TAMBIÉN EN UN CAMPO, NO SOLO EN LA FRASE (7
        # septiembre). Hasta hoy esto solo ponía `aviso`, un texto en
        # español: la pantalla puede enseñarlo, pero no puede DECIDIR con él
        # -- para saber si faltan menús habría que leer la prosa. El número
        # va aparte, que es lo que permite que la app reaccione (y que una
        # prueba lo compruebe sin buscar palabras dentro de una frase).
        salida["menus_pedidos_no_dados"] = menus_no_dados
        salida["por_que_faltan"] = por_que_faltan
        dados = numero_de_menus - menus_no_dados
        # ⚠️ Y EL MOTIVO DE VERDAD (28 agosto). Este aviso decía SIEMPRE
        # "no daba tiempo", y desde hoy hay un segundo camino que llega
        # aquí: que el menú del perro base no salga ni reintentando. Decir
        # "no daba tiempo" cuando lo que pasó es que no había combinación
        # manda a la usuaria a esperar en vez de a soltar una restricción.
        if por_que_faltan == "tiempo":
            _por_que = (f"con {len(perros_salida)} perros no daba tiempo a calcularlos "
                        f"todos sin que se cortara la conexión. Puedes pedir el resto "
                        f"en otra tanda.")
        else:
            _por_que = (f"no hemos encontrado una combinación distinta que cumpla todos "
                        f"los requisitos para {nombre_base or 'el perro con menos margen'}, "
                        f"que es el que manda. Con los menús que sí han salido puedes ir "
                        f"tirando; para tener más, prueba a quitarle alguna restricción.")
        salida["aviso"] = (
            f"Has pedido {numero_de_menus} menús por perro y han salido {dados}: {_por_que}")
        salida["numero_de_menus"] = dados
    # ⚠️ TEMPORAL — compatibilidad con la versión de la app que había
    # desplegada cuando esto cambió de forma (antes: un solo menú por perro
    # en la clave "menus"). Render despliega antes que Vercel, así que
    # durante unos minutos convive la API nueva con la app vieja, y sin
    # esto la usuaria vería un error en ese hueco. Se puede quitar en
    # cuanto la app esté desplegada: nada más lo usa.
    if numero_de_menus == 1:
        salida["menus"] = [{k: v for k, v in p.items() if k != "menus"}
                           | (p["menus"][0] if p.get("menus") else {})
                           for p in perros_salida]
    return salida


@app.post("/menu/varios-perros")
def endpoint_varios_perros(datos: PeticionVariosPerros):
    """Un menú por perro, en una sola llamada.

    En modo "parecidos", los menús se amoldan al del perro más
    restringido para que la compra y el porcionado sean uno solo. Ver el
    bloque de comentarios de arriba para el porqué de cada decisión.
    """
    observabilidad.etiquetar(endpoint="/menu/varios-perros",
                             cuantos_perros=len(datos.perros or []),
                             modo_conjunto=datos.modo_conjunto)
    resultados = []
    try:
        if not datos.perros:
            return {"factible": False,
                    "motivo": "No has mandado ningún perro."}
        if len(datos.perros) > 6:
            return {"factible": False,
                    "motivo": "Como mucho 6 perros a la vez."}

        al, req = cargar_v2()
        n = len(datos.perros)
        m = max(1, min(8, datos.numero_de_menus or 1))
        nombres = list(datos.nombres or [])
        # Sin nombre no se puede decir "el menú de Cairo", pero tampoco se
        # va a inventar uno: se dice por su sitio en la lista.
        while len(nombres) < n:
            nombres.append(f"el perro {len(nombres) + 1}")

        # El tiempo se reparte ANTES de empezar, entre TODAS las llamadas
        # que se van a hacer (perros x menús): pasarse significa que Render
        # corta la conexión y la usuaria no ve nada, ni el primer menú.
        # Nunca por debajo del suelo -- ver SEGUNDOS_MINIMOS_POR_MENU.
        t_inicio_casa = time.time()
        por_llamada = max(SEGUNDOS_MINIMOS_POR_MENU,
                          PRESUPUESTO_SEGUNDOS_VARIOS_PERROS / (n * m))

        def queda():
            return PRESUPUESTO_SEGUNDOS_VARIOS_PERROS - (time.time() - t_inicio_casa)

        # ⚠️ LO QUE CUESTA UNA RONDA SE MIDE, NO SE SUPONE (7 septiembre).
        #
        # CASO REAL, el del PENDIENTE §1.0: la casa de dos perros pidiendo 3
        # menús devolvía 1 para cada uno, sin error. La aritmética de aquel
        # análisis es correcta y sigue siéndolo:
        #
        #     ronda 0: primer menú de la base 12 s + amoldar 4 s = 16 s
        #     ronda 1: menú 6 s + amoldar 4 s                    = 10 s
        #     ronda 2: otros                                     = 10 s
        #                                        TOTAL 36 s, presupuesto 24
        #
        # Pero esos 12, 6 y 4 son TOPES, no costes: `presupuesto_segundos`
        # es un techo y el solver vuelve en cuanto encuentra solución. La
        # petición real tarda 9-15 s de los 24. Lo que fallaba era la
        # DECISIÓN de seguir: preguntaba "¿caben otros 10 s en el peor
        # caso?" incluso cuando la ronda anterior había costado 3. Con el
        # peor caso, dos perros y tres menús no caben NUNCA y siempre se
        # devuelve uno; con lo que costó de verdad, casi siempre caben.
        #
        # Así que se mide. Nunca se es optimista más allá de lo observado:
        # la estimación es el máximo de lo que han costado las rondas
        # anteriores, con un 25 % de margen, y mientras no haya nada medido
        # se usa el peor caso de siempre. Si la máquina va lenta (Render, o
        # la batería entera corriendo), las rondas cuestan más, la
        # estimación sube sola y se corta antes -- que es lo correcto.
        duraciones_ronda = []

        def coste_estimado_de_la_proxima_ronda():
            peor_caso = por_llamada + SEGUNDOS_AMOLDARSE * (n - 1)
            # ⚠️ INTERRUPTOR SOLO PARA LA BATERÍA, mismo criterio que el
            # `CANISLAB_CATALOGO` de `auditar_catalogo.py`: sirve para que
            # el BLOQUE 48 pueda medir las DOS versiones en la misma máquina
            # y en el mismo momento. Comparar contra un número apuntado otro
            # día no vale, porque cuánto rinde depende de lo cargada que
            # esté la máquina -- y la batería entera la carga mucho. Nunca
            # se pone a True en producción.
            if globals().get("_PEOR_CASO_SIEMPRE_SOLO_PRUEBAS"):
                return peor_caso
            if len(duraciones_ronda) > 1:
                # Ya hay rondas de las BARATAS medidas (la 0 no cuenta: es la
                # única con búsqueda libre del primer menú).
                return min(peor_caso, max(duraciones_ronda[1:]) * 1.25)
            if duraciones_ronda:
                # Solo se ha hecho la ronda 0, que es la cara. Las siguientes
                # no pueden costar más que ella, así que sirve de techo.
                return min(peor_caso, duraciones_ronda[0])
            return peor_caso

        def hay_tiempo_para_otra_ronda():
            """Una ronda es un menú para CADA perro. Si no cabe entera, se
            para: media ronda dejaría a unos perros con más menús que a
            otros, y entonces la semana de la casa no cuadra."""
            return queda() >= coste_estimado_de_la_proxima_ronda()

        menus_pedidos_no_dados = 0
        por_que_faltan = "tiempo"

        # Días que cubre cada menú de la rotación, igual que /menu/semana:
        # de ahí sale cuánto presupuesto semanal de seguridad gasta cada uno.
        base_dias, resto_dias = divmod(7, m)
        dias_por_menu = [base_dias + (1 if i < resto_dias else 0) for i in range(m)]

        # ⚠️ El presupuesto semanal de seguridad crónica (vitamina D, yodo,
        # tiaminasa, mercurio, selenio) es POR PERRO: depende de sus kcal.
        # Compartir uno solo entre varios perros sería mezclar lo que come
        # cada uno, que no tiene ningún sentido físico.
        presupuesto = {i: _presupuesto_semanal_inicial(p.der_objetivo)
                       for i, p in enumerate(datos.perros)}
        # Proteína ya usada, para rotarla entre los menús de un mismo perro.
        especies_usadas = {i: [] for i in range(n)}

        def personalizacion_de(j):
            """Lo elegido a mano para el menú j, si se mandó. None = ese
            menú va con lo que traiga el perro (como antes de existir
            esto)."""
            lista = datos.personalizacion_por_menu
            if not lista or j >= len(lista):
                return None
            return lista[j]

        def segundos_para(i, j, amoldandose):
            if amoldandose:
                return SEGUNDOS_AMOLDARSE
            if j == 0:
                return SEGUNDOS_PRIMER_MENU_DE_LA_BASE
            return por_llamada

        def generar(i, j, forzar_estos=None):
            """El menú j del perro i. `forzar_estos` es la lista de
            alimentos a la que tiene que parecerse (modo "parecidos")."""
            perro = datos.perros[i]
            dias_restantes = sum(dias_por_menu[j:])
            cambios_peticion = {
                # nunca más de lo que queda: una sola llamada no puede, ella
                # sola, hacer que se pase el presupuesto entero
                "presupuesto_segundos": max(2.0, min(segundos_para(i, j, bool(forzar_estos)),
                                                     queda())),
                "presupuesto_semanal_restante": _presupuesto_para_menu_actual(
                    presupuesto[i], dias_restantes),
                "evitar_especies": list(perro.evitar_especies or []) + especies_usadas[i],
            }
            if forzar_estos:
                # Parecerse se pide como Personalizar, que es el camino que
                # ya sabe intentar "solo estos alimentos", luego "estos sí o
                # sí pudiendo añadir", luego libre. Ver el bloque de arriba.
                cambios_peticion["modo"] = "personalizar"
                cambios_peticion["forzar_presencia"] = list(forzar_estos)
            elif personalizacion_de(j) is not None:
                # ⚠️ Lo que se eligió PARA ESTE MENÚ, no para la semana.
                # Va sólo cuando no hay `forzar_estos`: los perros que se
                # amoldan reciben ya la lista del menú de la base, que sale
                # de haber aplicado esto mismo. Aplicarlo dos veces sería
                # pisar el amoldado.
                pm = personalizacion_de(j)
                elegidos = list(pm.get("forzar_presencia") or [])
                especies = pm.get("restringir_especie") or None
                if elegidos or especies:
                    cambios_peticion["modo"] = "personalizar"
                    cambios_peticion["forzar_presencia"] = elegidos
                    cambios_peticion["nombres_alimentos"] = list(
                        pm.get("nombres_alimentos") or elegidos)
                    cambios_peticion["restringir_especie"] = especies
                else:
                    # Ese menú no se tocó: automático, aunque otros sí.
                    cambios_peticion["modo"] = "automatico"
                    cambios_peticion["forzar_presencia"] = []
                    cambios_peticion["nombres_alimentos"] = []
                    cambios_peticion["restringir_especie"] = None
            return _garantizar_verificado(
                _resolver_menu_v2_interno(perro.model_copy(update=cambios_peticion)),
                perro.der_objetivo, perro.etapa_requisitos, perro.peso_perro_kg,
                origen="/menu/varios-perros", al=al, req=req,
                patologias=perro.patologias,
                peso_adulto_esperado_kg=getattr(perro, "peso_adulto_esperado_kg", None),
                peso_objetivo_kg=_peso_de_referencia(perro)[0])

        def anotar_consumo(i, j, gramos):
            """Descuenta del presupuesto semanal del perro lo que gasta este
            menú, y apunta su proteína para no repetirla en el siguiente."""
            consumo = _consumo_real_menu(gramos, al, datos.perros[i].der_objetivo)
            dias = dias_por_menu[j]
            presupuesto[i] = _restar_del_presupuesto(presupuesto[i], consumo, dias)
            for cat in ("Carne muscular", "Pescados y mariscos", "Hueso carnoso",
                        "Vísceras", "Hígado"):
                principal = sorted(((nom, g) for nom, g in gramos.items()
                                    if al.get(nom, {}).get("categoria") == cat),
                                   key=lambda x: -x[1])
                if principal:
                    especies_usadas[i].append(especie_de(principal[0][0]))

        def gramos_de(r):
            return r.get("menu") or r.get("gramos") or {}

        por_perro = {i: {"indice": i, "nombre": nombres[i], "es_la_base": False,
                         "menus": [], "cambios": None, "resumen_parecido": None}
                     for i in range(n)}

        # ── Modo "distintos": cada perro su semana, sin mirar a los otros ──
        if datos.modo_conjunto != "parecidos":
            for i in range(n):
                for j in range(m):
                    if j > 0 and queda() < por_llamada:
                        menus_pedidos_no_dados = max(menus_pedidos_no_dados, m - j)
                        break
                    r = generar(i, j)
                    if not r.get("factible"):
                        if not por_perro[i]["menus"]:
                            por_perro[i]["motivo"] = r.get("motivo")
                        break
                    por_perro[i]["menus"].append({**r, "dias": dias_por_menu[j]})
                    anotar_consumo(i, j, gramos_de(r))
                por_perro[i]["factible"] = bool(por_perro[i]["menus"])
            perros_salida = [por_perro[i] for i in range(n)]
            return _respuesta_varios_perros(perros_salida, "distintos", None, m,
                                            menus_pedidos_no_dados)

        # ── Modo "parecidos" ─────────────────────────────────────────────
        # Cuánto margen tiene cada perro: más restricciones y menos ración
        # = menos margen. El de menos margen manda, y los demás se amoldan.
        # Al revés no cabe: forzar los alimentos de un perro grande en uno
        # de 3 kg no entra en su ración.
        def margen(par):
            _, p = par
            restricciones = (len(p.nombres_excluidos or []) + len(p.especies_excluidas or [])
                             + len(p.categorias_excluidas or []) + len(p.patologias or []))
            return (-restricciones, p.der_objetivo or 0.0)

        orden = [i for i, _ in sorted(enumerate(datos.perros), key=margen)]
        i_base = orden[0]
        por_perro[i_base]["es_la_base"] = True

        for j in range(m):
            if j > 0 and not hay_tiempo_para_otra_ronda():
                menus_pedidos_no_dados = m - j
                break
            _t_ronda = time.time()
            base = generar(i_base, j)
            # ⚠️ REINTENTO (28 agosto) — CASO REAL, el del PENDIENTE §1.0:
            # la casa de un cachorro de 12 kg y una adulta de 24,5 pedía 3
            # menús y devolvía 1 para cada uno, sin error y sin aviso.
            #
            # Medido hoy: 5 de 6 tiradas del MISMO caso salen 3/3 y una sale
            # 1/1. O sea que no es que el menú 2 sea imposible -- es que el
            # motor lleva aleatoriedad a propósito (para dar variedad) y de
            # vez en cuando esa tirada concreta no cierra. Y hasta hoy, una
            # sola vez que fallara cortaba la casa entera.
            #
            # Reintentar es la respuesta correcta y no relaja nada: cada
            # intento vuelve a pasar por `_garantizar_verificado`, así que
            # ningún menú sale sin cumplir. Lo único que cambia es que no se
            # rinde a la primera. Se reintenta mientras quede tiempo para
            # una ronda entera, que es el mismo criterio del bucle.
            _intentos_base = 0
            while (not base.get("factible") and _intentos_base < 2
                   and hay_tiempo_para_otra_ronda()):
                _intentos_base += 1
                base = generar(i_base, j)
            if not base.get("factible"):
                if j == 0:
                    # Si el perro que menos margen tiene no saca ni el
                    # primero, no hay a qué amoldarse. Se dice cuál es, que
                    # es lo accionable.
                    return {"factible": False, "modo_conjunto": "parecidos",
                            "numero_de_menus": m,
                            "motivo": f"No se ha podido hacer el menú de {nombres[i_base]}, "
                                      f"que es el que menos margen tiene. "
                                      + (base.get("motivo") or ""),
                            "perro_que_falla": nombres[i_base],
                            "perros": [por_perro[i] for i in range(n)]}
                # ⚠️ Y SI AUN ASI NO SALE, SE DICE (28 agosto). Antes esto
                # era un `break` a secas: los menús que ya había se
                # devolvían y nadie se enteraba de que faltaban. Pedir 3 y
                # recibir 1 sin una palabra es exactamente el fallo que no
                # se ve. `menus_pedidos_no_dados` ya lo cuenta la rama del
                # tiempo, unas líneas más arriba; aquí faltaba.
                menus_pedidos_no_dados = max(menus_pedidos_no_dados, m - j)
                por_que_faltan = "sin_combinacion"
                break  # los menús que ya salieron valen; se devuelven esos
            gramos_base = gramos_de(base)
            por_perro[i_base]["menus"].append({**base, "dias": dias_por_menu[j]})
            anotar_consumo(i_base, j, gramos_base)

            # ⚠️ EL AVISO DEL PERRO BASE VIAJA CON SU MENU (11 de septiembre).
            #
            # CASO REAL ENCONTRADO por el BLOQUE 15, y es la regla 5 otra vez:
            # «lo que eliges a mano se respeta [...] y si con lo elegido no hay
            # menu posible, se baja de peldano y SE DICE — nunca se cambia en
            # silencio. Eso incluye la pantalla de varios perros».
            #
            # Medido: en las tres tiradas del caso del BLOQUE 15, el menu de
            # Rufo (la base) llevaba «Pollo con piel» y «Pecho de ternera con
            # hueso» sin que nadie los eligiera, y lo DECIA. El de Cairo llevaba
            # exactamente los mismos dos y su `aviso` venia a `None`, las tres
            # veces. No es aleatorio: para el perro que se amolda, esos dos
            # alimentos entran por `forzar_presencia`, asi que desde dentro de
            # `_resolver_menu_v2_interno` son «lo que se pidio» y no hay nada
            # que avisar. El aviso se pierde justo en la costura.
            #
            # Y no se puede arreglar volviendo a aplicarle su propia eleccion al
            # que se amolda -- eso pisaria el amoldado, y esta escrito arriba --,
            # asi que lo que viaja es el aviso.
            _aviso_base = (base.get("aviso") or "").strip()

            for i in orden[1:]:
                r = generar(i, j, forzar_estos=list(gramos_base))
                if r.get("factible") and _aviso_base:
                    _suyo = (r.get("aviso") or "").strip()
                    _heredado = (f"Este menu se ha hecho para parecerse al de {nombres[i_base]}, "
                                 f"y aquel necesito alimentos que no elegiste. " + _aviso_base)
                    r["aviso"] = (_suyo + " " + _heredado).strip() if _suyo else _heredado
                if not r.get("factible"):
                    # Amoldarse no puede costarle a nadie quedarse sin menú:
                    # antes de rendirse, se le hace el suyo libremente.
                    r = generar(i, j)
                    if r.get("factible"):
                        r["aviso"] = (f"No había forma de acercar este menú de {nombres[i]} "
                                      f"al de {nombres[i_base]}, así que es el suyo propio. "
                                      + (r.get("aviso") or "")).strip()
                if not r.get("factible"):
                    if not por_perro[i]["menus"]:
                        por_perro[i]["motivo"] = r.get("motivo")
                    continue
                cambios = _comparar_menus(gramos_base, gramos_de(r))
                por_perro[i]["menus"].append({**r, "dias": dias_por_menu[j], "cambios": cambios})
                anotar_consumo(i, j, gramos_de(r))

            # Lo que ha costado ESTA ronda entera, para decidir si cabe la
            # siguiente. Ver `coste_estimado_de_la_proxima_ronda`.
            duraciones_ronda.append(time.time() - _t_ronda)

        for i in range(n):
            por_perro[i]["factible"] = bool(por_perro[i]["menus"])
            if i == i_base:
                continue
            # El parecido de la SEMANA entera: se suman los cambios de cada
            # menú. Decir solo el del primero engañaría cuando el segundo se
            # tuvo que separar más.
            todos = [mm.get("cambios") for mm in por_perro[i]["menus"] if mm.get("cambios")]
            if todos:
                cambios_semana = {
                    "iguales": sorted({x for c in todos for x in c["iguales"]}),
                    "anadidos": sorted({x for c in todos for x in c["anadidos"]}),
                    "quitados": sorted({x for c in todos for x in c["quitados"]}),
                    "cuantos_cambios": sum(c["cuantos_cambios"] for c in todos),
                }
                por_perro[i]["cambios"] = cambios_semana
                por_perro[i]["resumen_parecido"] = _resumen_de_parecido(
                    cambios_semana, nombres[i], nombres[i_base])

        return _respuesta_varios_perros([por_perro[i] for i in range(n)],
                                        "parecidos", nombres[i_base], m,
                                        menus_pedidos_no_dados, por_que_faltan)
    except Exception as e:
        import traceback
        traceback.print_exc()
        # mismo motivo que en /menu/v2 y /menu/semana: el except se traga
        # la excepción a propósito, así que hay que avisar a Sentry.
        observabilidad.capturar(e, endpoint="/menu/varios-perros",
                                cuantos_perros=len(datos.perros or []),
                                modo_conjunto=datos.modo_conjunto,
                                menus_ya_generados=len(resultados))
        return {"factible": False,
                "motivo": f"Ha fallado algo inesperado generando los menús "
                          f"({type(e).__name__}). Inténtalo de nuevo -- si se repite, dínoslo."}


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
# ⚠️ AÑADIDO (20 agosto) — DECIR POR QUÉ, NO SOLO QUE NO.
# CASO REAL ENCONTRADO AUDITANDO: añadir sardina a un perro de 3 kg
# fallaba siempre, y el mensaje era "no existe ninguna combinación que
# cumpla los 30 requisitos" -- que suena a que el perro es imposible de
# alimentar. La verdad era mucho más concreta y mucho más útil: la
# sardina lleva tiaminasa (destruye la vitamina B1), el límite es el 10%
# de las calorías del día, y en un perro de 3 kg eso son 18 g escasos --
# una ración mínima ya se pasa. Negarse es correcto; no explicarlo, no.
def _por_que_no_cabe(nombre, al, der, peso_perro_kg=None):
    """Si un alimento no cabe por un límite de seguridad concreto, decirlo
    en cristiano y con la cantidad real que sí cabría. None si no es
    ninguno de estos casos."""
    from seguridad import (TIAMINASA, MERCURIO_ALTO, TOPE_TIAMINASA_KCAL,
                           TOPE_MERCURIO_KCAL, TOPE_VITD_KCAL, TOPE_VITD_KG075, _es)
    a = al.get(nombre) or {}
    kcal_100 = a.get("energia") or 0
    if kcal_100 and _es(nombre, TIAMINASA):
        cabe = 100.0 * der * TOPE_TIAMINASA_KCAL / kcal_100
        return (f"{nombre} lleva tiaminasa, que destruye la vitamina B1, así que no "
                f"puede pasar del {int(TOPE_TIAMINASA_KCAL * 100)}% de las calorías del "
                f"día: como mucho unos {cabe:.0f} g para este perro, y una ración "
                f"normal ya se pasa. Puedes dárselo de vez en cuando, pero no a diario.")
    if kcal_100 and _es(nombre, MERCURIO_ALTO):
        cabe = 100.0 * der * TOPE_MERCURIO_KCAL / kcal_100
        return (f"{nombre} acumula mercurio, así que no puede pasar del "
                f"{int(TOPE_MERCURIO_KCAL * 100)}% de las calorías del día: como mucho "
                f"unos {cabe:.0f} g para este perro.")
    vitd_100 = (a.get("nutrientes") or {}).get("vitD") or 0
    if vitd_100:
        tope = TOPE_VITD_KCAL * der / 1000.0
        if peso_perro_kg and peso_perro_kg > 0:
            tope = min(tope, TOPE_VITD_KG075 * (peso_perro_kg ** 0.75))
        cabe = 100.0 * tope / vitd_100
        if cabe < 20:
            return (f"{nombre} lleva mucha vitamina D, y en un perro de este tamaño el "
                    f"tope diario se alcanza con unos {cabe:.0f} g.")
    return None


def _con_aviso_composicion(resultado, al, datos):
    """
    ⚠️ AÑADIDO (20 agosto): el aviso de "este menú no lleva vísceras" se
    emitía solo cuando hacía falta bajar por la escalera, y NUNCA se
    quitaba. Al editar un alimento eso da el caso contrario del que hace
    falta: si al editar vuelven a entrar las vísceras, el aviso tiene que
    DESAPARECER, y se quedaba puesto diciendo algo que ya no era verdad.

    Aquí se recalcula sobre el menú que de verdad se devuelve, y se pone
    la clave SIEMPRE -- también a None -- para que quien la pinte pueda
    borrar el aviso viejo, no solo añadir uno nuevo.
    """
    gramos = resultado.get("gramos") or resultado.get("menu")
    if resultado.get("factible") and gramos:
        resultado["aviso_composicion"] = _aviso_de_lo_que_falta(
            gramos, al, getattr(datos, "categorias_excluidas", None))
    return resultado


def _recalcular_con_motor(datos, forzar=None, excluir_nombres=None, restringir_especie=None,
                          preservar_siempre=False):
    """
    preservar_siempre (añadido 20 agosto): normalmente "intentar mantener
    el resto del menú" solo se activa cuando hay una edición de por medio
    (se fuerza o se excluye algo). /menu/revalidar necesita esa misma
    mecánica SIN edición ninguna: el menú no cambia por lo que pida el
    usuario, sino porque el perro ha cambiado de etapa.
    """
    al, req = cargar_v2()
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO,
    # pedido expreso: "si cambio un alimento de un menú, pero hay más
    # menús para esa semana, ¿sigue teniendo en cuenta los límites de
    # seguridad semanales?" -- la respuesta era NO, en absoluto. Los
    # modelos que usa editar (PeticionCambiarAlimento,
    # PeticionAnadirQuitarAlimento) nunca tuvieron el campo
    # presupuesto_semanal_restante -- así que _intentar(), más abajo,
    # llamaba a resolver_v2() sin pasarlo nunca, ni con el valor real de
    # la rotación ni con ningún default de seguridad. Confirmado con un
    # caso real: forzar aceite de hígado de bacalao en GENERACIÓN da 0g
    # (el límite lo bloquea), pero el MISMO forzado en una EDICIÓN daba
    # 5g reales, sin ninguna barrera -- un menú podía generarse seguro y
    # luego, con una sola edición, dejar de estarlo, sin que nada lo
    # impidiera. Los modelos de edición no llevan información de cuántos
    # menús más hay en la rotación ni cuánto consumen -- así que, igual
    # que en la generación de un único menú, se asume aquí el caso más
    # exigente: que este menú (el que se está editando) se coma todos
    # los días de la semana. getattr con default None, porque estos
    # modelos ni siquiera tienen el campo -- acceder directamente
    # lanzaría AttributeError.
    presupuesto_ya_definido = getattr(datos, "presupuesto_semanal_restante", None)
    if presupuesto_ya_definido is None:
        presupuesto_ya_definido = _presupuesto_menu_unico_semana_completa(datos.der_objetivo)
    excluidos = list(datos.especies_excluidas or [])
    nombres_excl = set(datos.nombres_excluidos or [])
    if excluir_nombres:
        nombres_excl |= set(excluir_nombres)

    def _intentar(forzar_este, margen_intentos=3, margenes=None, max_supl=2):
        """Un intento completo: hasta 3 vueltas hasta que sea verde de
        verdad, igual que ya hacía esto antes de separarlo en función."""
        ok, gramos, ficha = False, None, None
        for _intento in range(margen_intentos):
            ok, gramos = resolver_v2(
                datos.der_objetivo, datos.etapa_requisitos, al, req,
                datos.peso_perro_kg, dosis_maxima_fabricante,
                excluidos=(excluidos + list(nombres_excl)) or None,
                margenes_categoria=(margenes if margenes is not None else MARGENES_V2),
                max_suplementos=max_supl,
                forzar=forzar_este,
                restringir_especie=restringir_especie,
                peso_adulto_esperado_kg=getattr(datos, "peso_adulto_esperado_kg", None),
                peso_objetivo_kg=_peso_de_referencia(datos)[0],
                categorias_excluidas=getattr(datos, "categorias_excluidas", None),
                presupuesto_semanal_restante=presupuesto_ya_definido,
                # ⚠️ AÑADIDO (24 agosto) — FALLO GRAVE ENCONTRADO MIDIENDO:
                # EDITAR UN MENÚ SE SALTABA LOS TOPES POR PATOLOGÍA.
                #
                # Medido, con el tope y lo que salía de verdad:
                #     renal        fósforo  tope 1400  →  3084   (+120%)
                #     hepatopatía  cobre    tope 3.0   →  4.05
                #     pancreatitis grasa    tope 25%   →  47%
                #
                # Es EXACTAMENTE el mismo fallo que ya tuvo esta misma
                # función con el presupuesto semanal (ver el comentario
                # largo de arriba, 5 de agosto): resolver() recibe las
                # patologías en todos los demás caminos, y aquí no se le
                # pasaban nunca. El menú se generaba respetando el tope y
                # una sola edición lo tiraba, sin que nada lo impidiera.
                #
                # Y no lo paraba la verificación: verificar_v2 comprueba
                # los 30 requisitos de FEDIAF, que son los de un perro
                # SANO -- 3084 mg de fósforo está dentro del máximo de
                # FEDIAF, así que el menú salía en verde. Un perro renal
                # no es un perro sano, y ese es justo el sentido del tope.
                #
                # getattr con default None: los modelos de edición sí
                # tienen el campo, pero /menu/revalidar usa esta misma
                # función con otro modelo.
                patologias=getattr(datos, "patologias", None),
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
    if menu_actual and (forzar or excluir_nombres or preservar_siempre):
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
                return _con_aviso_composicion(_garantizar_verificado(
                    resultado, datos.der_objetivo, datos.etapa_requisitos,
                    datos.peso_perro_kg, origen="edicion (preservando)",
                    patologias=getattr(datos, "patologias", None),
                    peso_adulto_esperado_kg=getattr(datos, "peso_adulto_esperado_kg", None),
                    peso_objetivo_kg=_peso_de_referencia(datos)[0],
                    al=al, req=req), al, datos)
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
                return _con_aviso_composicion(_garantizar_verificado(
                    resultado, datos.der_objetivo, datos.etapa_requisitos,
                    datos.peso_perro_kg, origen="edicion (libre)", patologias=getattr(datos, "patologias", None),
                    peso_adulto_esperado_kg=getattr(datos, "peso_adulto_esperado_kg", None),
                    peso_objetivo_kg=_peso_de_referencia(datos)[0],
                    al=al, req=req), al, datos)
            ok, gramos, ficha = ok_libre, gramos_libre, ficha_libre
        else:
            ok, gramos, ficha = _intentar(forzar)
    else:
        ok, gramos, ficha = _intentar(forzar)

    # ⚠️ AÑADIDO (20 agosto) — la misma escalera que en la generación:
    # editar un alimento chocaba contra el mismo muro (las proporciones
    # de BARF, no la nutrición), y ahí duele más todavía, porque la
    # usuaria ya tiene un menú delante y solo quería cambiar una cosa.
    relajaciones_edicion = []
    hay_comida = _hay_comida_de_verdad(al, excluidos + list(nombres_excl),
                                       getattr(datos, "categorias_excluidas", None))
    if not ok:
        for margenes_peldano, supl_peldano, que_se_suelta in _escalera_de_relajacion(hay_comida)[1:]:
            ok, gramos, ficha = _intentar(forzar, margen_intentos=2,
                                          margenes=margenes_peldano, max_supl=supl_peldano)
            if ok:
                relajaciones_edicion.append(que_se_suelta)
                break

    if not ok:
        # ¿es culpa del alimento que se ha pedido meter? Se comprueba en vez
        # de suponerlo: si sin él sí hay menú, el problema es él, y muchas
        # veces se puede decir exactamente por qué (ver _por_que_no_cabe).
        motivo = ("Con este cambio no existe ninguna combinación que cumpla "
                  "los 30 requisitos, ni siquiera soltando las proporciones "
                  "habituales del BARF. Prueba con otro alimento.")
        culpable = None
        if forzar:
            ok_sin, _, _ = _intentar(None, margen_intentos=1)
            if ok_sin:
                culpable = forzar[0] if len(forzar) == 1 else None
                explicacion = (_por_que_no_cabe(culpable, al, datos.der_objetivo,
                                                datos.peso_perro_kg) if culpable else None)
                if explicacion:
                    motivo = explicacion
                elif culpable:
                    motivo = (f"{culpable} no cabe en la ración de este perro sin "
                              f"incumplir algún requisito. El resto del menú sí "
                              f"funciona: prueba con otro alimento.")
        respuesta = {"factible": False, "motivo": motivo}
        if culpable:
            respuesta["alimento_que_no_cabe"] = culpable
        return respuesta
    resultado_final = {
        "factible": True, "gramos": gramos, "ficha": ficha,
        "problemas_seguridad": _seguridad_completa(
            gramos, al, datos.der_objetivo, datos.etapa_requisitos, datos.patologias,
            peso_perro_kg=datos.peso_perro_kg),
    }
    if relajaciones_edicion:
        resultado_final["se_relajo"] = relajaciones_edicion
        aviso_falta = _aviso_de_lo_que_falta(gramos, al, datos.categorias_excluidas)
        if aviso_falta:
            resultado_final["aviso_composicion"] = aviso_falta
    return _con_aviso_composicion(_garantizar_verificado(
        resultado_final, datos.der_objetivo, datos.etapa_requisitos,
        datos.peso_perro_kg, origen="edicion", al=al, req=req,
        patologias=getattr(datos, "patologias", None),
        peso_adulto_esperado_kg=getattr(datos, "peso_adulto_esperado_kg", None),
            peso_objetivo_kg=_peso_de_referencia(datos)[0]), al, datos)


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


# =====================================================================
# ⚠️ AÑADIDO (20 agosto) — CASO 3: EL PERRO CAMBIA DE CATEGORÍA
#
# CASO REAL, REPRODUCIDO: se genera un menú para un cachorro de 15 kg en
# CachorroCrecimiento con DER 1200. Sale VERDE, 30 de 30 requisitos.
# Meses después el perro es adulto: 30 kg, DER 1500, etapa Adulto. Ese
# MISMO menú, verificado contra la etapa nueva, sale ROJO -- 26 de 30,
# con manganeso al 68% y linoleico al 75%. Y sigue llevando dentro
# "V-INTEGRA Cachorro", un multivitamínico formulado para crecimiento.
#
# Hasta ahora no había NINGÚN camino en el backend para esto. Al editar
# un alimento el menú se rehacía entero con el motor, pero al cambiar el
# perro no se rehacía nada: el menú guardado se seguía sirviendo tal
# cual, y lo único que cambiaba era el DER. Los requisitos de FEDIAF no
# son los mismos para un cachorro que para un adulto -- no es solo
# cuestión de escalar las calorías.
#
# Este endpoint es ese camino. Recibe el menú que el perro está comiendo
# y los datos de AHORA, y:
#   · si el menú sigue cumpliendo con la etapa nueva, lo dice y no toca
#     nada -- no se cambia un menú que funciona solo porque el perro
#     haya cumplido años;
#   · si ya no cumple, lo REHACE con motor_completo.py, intentando
#     conservar todos los alimentos que se puedan (los suplementos no:
#     esos los vuelve a elegir el motor, que es justo lo que hace falta
#     cuando el multivitamínico era el de cachorro), y dice qué falló y
#     qué cambió.
# En los dos casos la respuesta sale por _garantizar_verificado().
# =====================================================================
@app.post("/menu/revalidar")
def endpoint_revalidar(datos: PeticionRevalidar):
    al, req = cargar_v2()
    gramos = datos.menu_actual_gramos or {}
    if not gramos:
        raise HTTPException(400, "Hace falta el menú actual con sus gramos para revalidarlo.")

    desconocidos = [n for n in gramos if n not in al]
    if desconocidos:
        raise HTTPException(400, "Estos alimentos del menú no existen en la base de "
                                 "datos: " + ", ".join(desconocidos))

    if datos.etapa_requisitos not in ETAPAS_MOTOR_V2:
        raise HTTPException(400, f"Etapa '{datos.etapa_requisitos}' no valida. "
                                 f"Usa una de: {sorted(ETAPAS_MOTOR_V2)}")

    ficha = verificar_v2(gramos, al, req, datos.der_objetivo, datos.etapa_requisitos)
    seguro = _menu_precalculado_es_seguro(gramos, al, datos.der_objetivo, datos.peso_perro_kg)

    if ficha["semaforo"] == "verde" and seguro:
        return _garantizar_verificado({
            "factible": True,
            "sigue_siendo_valido": True,
            "menu": gramos,
            "problemas_seguridad": _seguridad_completa(
                gramos, al, datos.der_objetivo, datos.etapa_requisitos,
                datos.patologias, peso_perro_kg=datos.peso_perro_kg),
            "kcal_total": sum(al[n]["energia"] * g / 100 for n, g in gramos.items()),
            "gramos_total": sum(gramos.values()),
        }, datos.der_objetivo, datos.etapa_requisitos, datos.peso_perro_kg,
            origen="/menu/revalidar (sin cambios)", al=al, req=req,
            patologias=getattr(datos, "patologias", None),
            peso_adulto_esperado_kg=getattr(datos, "peso_adulto_esperado_kg", None),
            peso_objetivo_kg=_peso_de_referencia(datos)[0])

    # Ya no cumple: se rehace con el motor, conservando lo que se pueda.
    motivo = []
    for f in ficha.get("rojos", []):
        if f.get("cubre_pct") is not None:
            motivo.append(f"{f['nutriente']} se queda en el {f['cubre_pct']}%")
        else:
            motivo.append(f"{f['nutriente']} se pasa del máximo")
    if not seguro:
        motivo.append("supera un límite de seguridad crónica con las calorías de ahora")

    resultado = _recalcular_con_motor(datos, preservar_siempre=True)
    if not resultado.get("factible"):
        return {
            "factible": False,
            "sigue_siendo_valido": False,
            "motivo": ("Este menú ya no cumple los requisitos de la etapa actual del perro "
                       "y no hemos encontrado forma de arreglarlo conservando sus alimentos. "
                       "Genera un menú nuevo."),
            "por_que_ya_no_vale": motivo,
        }

    nuevos = resultado.get("gramos") or resultado.get("menu") or {}
    resultado["sigue_siendo_valido"] = False
    resultado["por_que_ya_no_vale"] = motivo
    resultado["cambios"] = {
        "quitados": sorted(n for n in gramos if n not in nuevos),
        "anadidos": sorted(n for n in nuevos if n not in gramos),
        "se_mantienen": sorted(n for n in nuevos if n in gramos),
    }
    return resultado


@app.get("/perro/{perro_id}/menus")
def endpoint_obtener_menus(perro_id: int):
    """
    ⚠️ ARREGLADO EL 7 DE SEPTIEMBRE — ERA EL ÚNICO CAMINO QUE ENTREGABA
    MENÚS SIN PASAR POR `_garantizar_verificado()`, o sea el único agujero
    en la regla 1 del CLAUDE.md.

    Lo que decía la nota de antes (20 de agosto) era cierto y por eso el
    agujero no se podía tapar entonces: la tabla `menus` guardaba nombre,
    gramos y kcal, y NADA MÁS. Sin la etapa ni el DER contra los que se
    verificó, un menú sacado de aquí no se podía verificar **ni siquiera
    en principio** -- no faltaba código, faltaba el dato. Se marcaba
    `verificado: false` con un aviso, que era honesto pero dejaba en manos
    de quien llamara el acordarse de pasarlo por /menu/revalidar. Y un
    aviso se puede ignorar; por eso este proyecto no los usa para lo que
    importa.

    Ahora `guardar_menu` escribe el contexto JUNTO al menú (etapa, DER,
    pesos, patologías) y aquí se verifica de cero, con el mismo filtro que
    todos los demás caminos. Tres resultados posibles, y los tres se dicen:

      · `verificado: true`   — pasó el filtro. Lleva su `ficha` completa.
      · `verificado: false` con `motivo` — se verificó y NO cumple. Es lo
        que hace falta saber: un menú guardado hace meses puede haber
        dejado de cumplir porque cambió el catálogo debajo.
      · `verificado: null`   — es una fila anterior al 7 de septiembre, sin
        contexto. No se puede verificar y no se finge que sí; esas siguen
        necesitando /menu/revalidar con los datos de hoy.

    Lo que sigue SIN cambiar, y hay que tenerlo claro: esto verifica contra
    la etapa de ENTONCES, que es la pregunta "¿este menú cumplía cuando se
    guardó, y sigue cumpliendo con el catálogo de hoy?". Si el perro ha
    crecido o ha cambiado de etapa, la pregunta es otra y la contesta
    /menu/revalidar.
    """
    menus = persistencia.obtener_menus(perro_id)
    if not menus:
        return menus
    al, req = cargar_v2()
    for m in menus:
        ctx = m.get("contexto") or {}
        if not ctx.get("etapa_requisitos") or not ctx.get("der_objetivo"):
            m["verificado"] = None
            m["aviso"] = ("Menú guardado antes de que se guardara el contexto de "
                          "verificación: no se puede comprobar contra nada. Pásalo por "
                          "/menu/revalidar con los datos actuales del perro.")
            continue
        comprobado = _garantizar_verificado(
            {"factible": True, "menu": m["alimentos"]},
            ctx["der_objetivo"], ctx["etapa_requisitos"], ctx.get("peso_perro_kg"),
            origen=f"/perro/{perro_id}/menus", al=al, req=req,
            patologias=ctx.get("patologias"),
            peso_adulto_esperado_kg=ctx.get("peso_adulto_esperado_kg"),
            peso_objetivo_kg=ctx.get("peso_objetivo_kg"))
        if comprobado.get("factible"):
            m["verificado"] = True
            m["ficha"] = comprobado.get("ficha")
        else:
            # ⚠️ NO SE DEVUELVEN LOS GRAMOS DE UN MENÚ QUE NO CUMPLE. Es la
            # regla 1: preferimos no dar menú a dar uno que no cumple. Se
            # dice qué pasó y con qué se guardó, para que se pueda regenerar.
            m.pop("alimentos", None)
            m["verificado"] = False
            m["motivo"] = comprobado.get("motivo") or "no pasa la verificación"
        m["verificado_contra"] = {"etapa": ctx["etapa_requisitos"],
                                  "der": ctx["der_objetivo"],
                                  "cuando_se_guardo": m.get("creado_en")}
    return menus


@app.get("/")
def raiz():
    return {"estado": "Rawku API funcionando"}


# =====================================================================
# STRIPE — pagos y suscripciones
# =====================================================================
import os
import stripe

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# ⚠️ CORREGIDO (20 agosto) — LOS PRICE ID SON DISTINTOS EN MODO PRUEBA Y
# EN MODO REAL. En Stripe, un precio creado en modo real NO existe en modo
# prueba, y al revés. Estando escritos en duro, no había forma de hacer un
# pago de prueba con una tarjeta falsa sin tocar el código y volver a
# desplegar -- que es justo lo que hay que hacer ANTES de cobrarle a
# nadie de verdad. Ahora se pueden cambiar desde las variables de entorno
# de Render, sin tocar nada:
#
#   modo prueba : STRIPE_PRICE_MENSUAL / STRIPE_PRICE_ANUAL con los price
#                 id de prueba (empiezan igual, pero son otros), y
#                 STRIPE_SECRET_KEY con la clave sk_test_...
#   modo real   : se quitan esas variables y vuelven los de siempre.
#
# ⚠️ CORREGIDO (20 agosto) — CASO REAL: aquí ponía que los valores por
# defecto eran "los de producción". NO LO SON. Comprobado en el panel de
# Stripe: estos dos price id se crearon el 19 de agosto DENTRO DE UNA
# SANDBOX, así que son precios de mentira. Con una clave sk_live_ no
# existen, y el primer cobro real habría fallado con "No such price" --
# justo en el peor momento posible, con una clienta delante intentando
# pagar.
#
# Se dejan como están porque son los que hacen falta AHORA para probar
# (con clave sk_test_ funcionan), pero marcados por lo que son, y con la
# comprobación de _precio_de_sandbox() más abajo para que no puedan
# llegar a producción por descuido.
PRECIOS_DE_SANDBOX = {
    "price_1U6G2EDnx1sWAUrF2v88kDWZ",   # 4,99 €/mes, creado en sandbox el 19 ago
    "price_1U6G3DDnx1sWAUrF5DseuSG1",   # 39 €/año,   creado en sandbox el 19 ago
}
PRICE_MENSUAL = os.environ.get("STRIPE_PRICE_MENSUAL") or "price_1U6G2EDnx1sWAUrF2v88kDWZ"
PRICE_ANUAL   = os.environ.get("STRIPE_PRICE_ANUAL") or "price_1U6G3DDnx1sWAUrF5DseuSG1"


def _modo_stripe():
    """
    "real", "prueba" o "sin configurar", deducido del prefijo de la clave.
    NUNCA devuelve la clave ni parte de ella.
    """
    clave = stripe.api_key or ""
    if clave.startswith("sk_live_"):
        return "real"
    if clave.startswith("sk_test_") or clave.startswith("rk_test_"):
        return "prueba"
    return "sin configurar"


def _precio_de_sandbox(price_id):
    """
    ¿Este precio es uno de los de mentira? Se comprueba ANTES de llamar a
    Stripe para poder dar un motivo entendible en vez del "resource_missing"
    del error de la librería, que no le dice nada a nadie.
    """
    return price_id in PRECIOS_DE_SANDBOX
# También configurable: para probar contra un despliegue de vista previa
# de Vercel en vez de contra el dominio real.
URL_BASE      = os.environ.get("URL_BASE") or "https://rawku.app"

# ⚠️ CORREGIDO (20 agosto) — CASO REAL DE COBRO INDEBIDO: el precio se
# elegía con `PRICE_MENSUAL if plan == "mensual" else PRICE_ANUAL`. Es
# decir: CUALQUIER cosa que no fuera exactamente la palabra "mensual"
# --un "Mensual" con mayúscula, un typo, un campo vacío, un plan que
# alguien añada mañana-- caía en el anual, que es el caro. Un fallo de
# tecleo cobraba un año por adelantado sin que nada lo impidiera.
# Ahora los planes válidos están explícitos y cualquier otra cosa se
# rechaza con un 400 antes de crear nada en Stripe.
PLANES = {"mensual": PRICE_MENSUAL, "anual": PRICE_ANUAL}


class PeticionCheckout(BaseModel):
    user_id: str
    email: str
    plan: str  # "mensual" o "anual"


@app.post("/stripe/checkout")
def crear_checkout(datos: PeticionCheckout):
    """Crea una sesión de checkout de Stripe con 7 días de trial."""
    price_id = PLANES.get((datos.plan or "").strip().lower())
    if not price_id:
        raise HTTPException(400, f"Plan '{datos.plan}' no válido. "
                                 f"Usa uno de: {sorted(PLANES)}")

    # ⚠️ AÑADIDO (20 agosto) — LA RED: cobrar de verdad con un precio de
    # sandbox no da un error entendible, da un "resource_missing" de la
    # librería de Stripe con la clienta delante. Peor: es un fallo que
    # solo aparece la PRIMERA vez que alguien paga en serio, que es
    # exactamente cuando no puedes permitírtelo. Se corta antes.
    if _modo_stripe() == "real" and _precio_de_sandbox(price_id):
        observabilidad.capturar(
            RuntimeError("Clave de Stripe REAL con un precio de SANDBOX: "
                         "hay que crear los precios de verdad y ponerlos en "
                         "STRIPE_PRICE_MENSUAL / STRIPE_PRICE_ANUAL"),
            endpoint="/stripe/checkout", plan=datos.plan, modo="real",
            price_id=price_id)
        raise HTTPException(
            status_code=500,
            detail="El cobro no está bien configurado en el servidor (los precios "
                   "son de prueba y la clave es real). No se te ha cobrado nada.")
    # ⚠️ AÑADIDO (20 agosto): si ya tiene una suscripción viva, no se le
    # crea otra -- se le manda a gestionar la que tiene. Ver
    # _suscripciones_vivas() para el caso real que lo motivó.
    vivas, se_pudo = _suscripciones_vivas(datos.user_id)
    if vivas:
        cliente = vivas[0].get("customer")
        url_portal = None
        try:
            url_portal = stripe.billing_portal.Session.create(
                customer=cliente, return_url=URL_BASE).url
        except Exception as e:
            observabilidad.capturar(e, endpoint="/stripe/checkout",
                                    paso="portal para quien ya está suscrito")
        return {"ya_suscrito": True, "url": url_portal,
                "motivo": ("Ya tienes una suscripción activa. Desde aquí puedes "
                           "cambiarla o cancelarla, pero no hace falta pagar otra vez.")}
    if not se_pudo:
        # Stripe no contesta: no sabemos si ya tiene una. Ante la duda, NO
        # se cobra -- es reintentable, y un cobro duplicado no.
        raise HTTPException(
            status_code=503,
            detail="No hemos podido comprobar si ya tienes una suscripción. "
                   "Inténtalo en un minuto: no se te ha cobrado nada.")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            payment_method_types=["card"],
            customer_email=datos.email,
            subscription_data={
                "trial_period_days": 7,
                "metadata": {"user_id": datos.user_id},
            },
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=f"{URL_BASE}/?pago=ok&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{URL_BASE}/?pago=cancelado",
            metadata={"user_id": datos.user_id},
        )
        return {"url": session.url}
    except Exception as e:
        # ⚠️ AÑADIDO (20 agosto) — esto devuelve 400, no 500, así que
        # Sentry tampoco lo vería solo: un 400 es "el cliente ha mandado
        # algo mal" y no se reporta por defecto. Pero aquí el 400 tapa
        # también los fallos NUESTROS (clave de Stripe mal puesta, price
        # id que ya no existe, Stripe caído) -- y que nadie pueda pagar
        # es el peor fallo posible de toda la API. Sin el email ni el
        # user_id: eso lo borra observabilidad.py antes de enviarlo.
        observabilidad.capturar(e, endpoint="/stripe/checkout", plan=datos.plan)
        raise HTTPException(status_code=400, detail=str(e))


class PeticionPortal(BaseModel):
    stripe_customer_id: str


# =====================================================================
# ⚠️ AÑADIDO (20 agosto) — PROBAR EL COBRO DESDE EL MÓVIL, SIN TOCAR LA WEB
#
# Para probar el pago de punta a punta hacía falta encender el muro de
# pago en producción, y eso se lo pone delante a cualquiera que entre en
# rawku.app mientras tanto. Esto abre el mismo checkout de Stripe que
# abriría la app, pero desde una URL que se pega en el navegador.
#
# Tres cerrojos, porque una URL que crea cobros no puede quedarse abierta:
#   1. Apagada salvo que STRIPE_PRUEBA=1 esté puesta en Render.
#   2. NUNCA funciona con una clave real, aunque la variable esté puesta.
#      Esto no es una comodidad, es la diferencia entre una prueba y
#      cobrarle a alguien de verdad sin querer.
#   3. Hace falta el user_id del perfil, así que no se puede usar a ciegas.
#
# Cuando termines de probar: se borra la variable y la URL vuelve a dar
# 404, como /sentry/prueba.
# =====================================================================
@app.get("/stripe/prueba")
def stripe_prueba(user_id: str = None, plan: str = "mensual"):
    from fastapi.responses import RedirectResponse

    if os.environ.get("STRIPE_PRUEBA") != "1":
        raise HTTPException(404, "No encontrado")

    modo = _modo_stripe()
    if modo != "prueba":
        # El cerrojo importante: con clave real esto crearía un cobro de
        # verdad desde una URL sin autenticar. Jamás.
        raise HTTPException(
            403, f"Esta prueba solo funciona con una clave de Stripe de pruebas "
                 f"(ahora mismo el modo es '{modo}'). Con la clave real está "
                 f"bloqueada a propósito.")

    if not user_id:
        raise HTTPException(
            400, "Falta el user_id del perfil. Añádelo a la dirección así: "
                 "/stripe/prueba?user_id=EL-ID-DE-TU-PERFIL — lo encuentras en "
                 "Supabase, tabla profiles, columna id.")

    price_id = PLANES.get((plan or "").strip().lower())
    if not price_id:
        raise HTTPException(400, f"Plan '{plan}' no válido. Usa uno de: {sorted(PLANES)}")

    try:
        session = stripe.checkout.Session.create(
            mode="subscription",
            payment_method_types=["card"],
            subscription_data={"trial_period_days": 7,
                               "metadata": {"user_id": user_id}},
            line_items=[{"price": price_id, "quantity": 1}],
            success_url=f"{URL_BASE}/?pago=ok&session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{URL_BASE}/?pago=cancelado",
            metadata={"user_id": user_id},
        )
    except Exception as e:
        observabilidad.capturar(e, endpoint="/stripe/prueba", plan=plan)
        raise HTTPException(400, f"Stripe no ha aceptado la petición: {e}")

    # Se redirige directamente al checkout: así se abre desde el móvil
    # pegando una sola dirección, sin herramientas raras.
    return RedirectResponse(session.url, status_code=303)


@app.post("/stripe/portal")
def portal_cliente(datos: PeticionPortal):
    """Abre el portal de Stripe para gestionar la suscripción."""
    try:
        session = stripe.billing_portal.Session.create(
            customer=datos.stripe_customer_id,
            return_url=URL_BASE,
        )
        return {"url": session.url}
    except Exception as e:
        # mismo motivo que en /stripe/checkout: si esto falla, el usuario
        # no puede gestionar ni cancelar su suscripción.
        observabilidad.capturar(e, endpoint="/stripe/portal")
        raise HTTPException(status_code=400, detail=str(e))


# =====================================================================
# ⚠️ REESCRITO (20 agosto) — EL WEBHOOK NO HABÍA FUNCIONADO NUNCA
#
# Comprobado mandando un webhook FIRMADO de verdad contra el endpoint,
# no leyendo el código: devolvía 500 siempre, con cualquier evento.
# Cuatro fallos independientes, todos en el camino del dinero:
#
#   1. `import supabase as sb` en la primera línea. Ese paquete NO está
#      en requirements.txt, así que en Render lanza ModuleNotFoundError
#      antes de hacer nada. Y encima no se usaba para nada: la
#      actualización se hace con httpx. Un import muerto tumbaba el
#      webhook entero, siempre.
#   2. sub["current_period_end"]. Stripe QUITÓ ese campo del objeto
#      Subscription en la versión Basil (31 marzo 2025): ahora el
#      periodo vive en items.data[].current_period_end. La librería
#      instalada fija la versión 2026-07-29.dahlia, muy posterior, así
#      que ese campo no existe y era un KeyError garantizado.
#   3. La respuesta de Supabase no se miraba NUNCA. Si el PATCH fallaba
#      (clave mal, RLS, columna que no existe), el webhook devolvía
#      {"ok": true} igual: el usuario pagaba y se quedaba en "free" sin
#      que nadie se enterara jamás.
#   4. Un pago sin user_id en la metadata se ignoraba en silencio: dinero
#      cobrado que no se puede asociar a ninguna cuenta.
#
# Los cuatro se cobran igual de caros: alguien paga y no recibe nada.
# Ahora, cuando algo falla aquí, se devuelve 5xx a propósito -- Stripe
# reintenta con espera creciente durante días, así que un fallo pasajero
# de Supabase se recupera solo en vez de perderse -- y se manda a Sentry.
# =====================================================================
# =====================================================================
# QUIEN ES UN VETERINARIO ACREDITADO -- Y POR QUE NO SE PREGUNTA AL CLIENTE
# =====================================================================
#
# ⚠️ ESTO ES UNA FRONTERA DE AUTORIZACION (29 agosto). De este rol cuelga
# formular para patologias que al dueño se le bloquean, y mañana pautar por
# debajo de los minimos de FEDIAF con una firma detras.
#
# LO QUE NO SE PUEDE HACER, y es la tentacion obvia: aceptar un campo
# `modo_profesional: true` en la peticion. Eso lo manda cualquiera con la
# consola del navegador abierta, y entonces el rol no acredita nada.
#
# LO QUE TAMPOCO VALE: aceptar un `usuario_id`. Un UUID no es una
# credencial -- es un identificador, y el de un veterinario se puede
# copiar. Mandar el id de otro no puede darte sus permisos.
#
# LO QUE SI: la app manda su TOKEN de sesion de Supabase, que solo tiene
# quien ha iniciado sesion de verdad. La API se lo da a Supabase, Supabase
# dice de quien es, y solo entonces se mira `profiles` con la clave de
# servicio. Dos viajes, y ninguno se cree nada del cliente.
#
# Y LA MISMA REGLA QUE `rol.js` EN LA APP, escrita igual: hacen falta LAS
# DOS -- `rol == 'profesional'` (lo que la persona PIDE) y
# `rol_verificado_en` con fecha (que alguien miro su numero de colegiado).
# Un rol que se autoconcede no puede sostener una prescripcion.
#
# FALLA CERRADO. Sin Supabase configurado, con el token caducado, con la
# red caida o con cualquier excepcion, devuelve False -- y False es el
# comportamiento del dueño, que nunca es peligroso. Lo contrario seria que
# una caida de red abriera la puerta.
def _es_profesional_acreditado(token_usuario):
    """True solo si el token es de una cuenta con el rol verificado."""
    if not token_usuario:
        return False
    url = (os.environ.get("SUPABASE_URL") or "").rstrip("/")
    clave = (os.environ.get("SUPABASE_SERVICE_KEY") or "").strip()
    if not url or not clave:
        return False
    try:
        import requests
        # (1) ¿De quien es este token? Lo dice Supabase, no el cliente.
        r = requests.get(f"{url}/auth/v1/user", timeout=6, headers={
            "apikey": clave, "Authorization": f"Bearer {str(token_usuario).strip()}"})
        if r.status_code != 200:
            return False
        uid = (r.json() or {}).get("id")
        if not uid:
            return False
        # (2) Y ahora si, su fila de `profiles`, con la clave de servicio.
        cab = _cabeceras_supabase(clave)
        cab.pop("Prefer", None)
        r2 = requests.get(f"{url}/rest/v1/profiles",
                          params={"id": f"eq.{uid}", "select": "rol,rol_verificado_en"},
                          headers=cab, timeout=6)
        if r2.status_code != 200:
            return False
        filas = r2.json() or []
        if not filas:
            return False
        fila = filas[0]
        return fila.get("rol") == "profesional" and bool(fila.get("rol_verificado_en"))
    except Exception:
        # Ni un aviso a Sentry: esto se llama en cada menu y un Supabase
        # caido llenaria el buzon. Lo que importa es que falle cerrado.
        return False


def _cabeceras_supabase(clave):
    """
    ⚠️ CORREGIDO (20 agosto) — CASO REAL, y el fallo era NUESTRO: un pago
    de prueba con la clave secreta CORRECTA puesta seguía dando 403 al
    escribir el plan. Se perdieron dos rondas buscándolo en la
    configuración de Supabase cuando estaba aquí.

    Causa: esto mandaba la clave en DOS cabeceras, `apikey` y
    `Authorization: Bearer`. Con las claves antiguas (JWT) eso es lo
    correcto y funciona. Pero las claves del formato nuevo
    (sb_secret_... / sb_publishable_...) NO son JWT: al llegar en
    Authorization, Supabase intenta interpretarlas como tal, no puede, y
    rechaza la petición entera con 403 -- aunque la clave sea la buena y
    tenga todos los permisos.

    Las nuevas van SOLO en `apikey`. Las antiguas siguen yendo en las dos,
    que es como estaban documentadas, para no romper a quien no haya
    migrado.
    """
    cabeceras = {
        "apikey": clave,
        "Content-Type": "application/json",
        "Prefer": "return=representation",
    }
    # Un JWT son tres trozos separados por puntos. Si no lo es, es del
    # formato nuevo y no puede viajar como Bearer.
    if len(clave.split(".")) == 3:
        cabeceras["Authorization"] = f"Bearer {clave}"
    return cabeceras


def _tipo_de_clave_supabase():
    """
    ⚠️ AÑADIDO (20 agosto) — CASO REAL: un 403 de Supabase al activar un
    premium, y dos rondas de "prueba a cambiar la clave, a ver". Adivinar
    a ciegas es lento y desesperante, y la respuesta estaba dentro de la
    propia clave todo el rato.

    Las claves de Supabase dicen lo que son:
      · las nuevas, por el prefijo (sb_secret_ / sb_publishable_)
      · las antiguas son JWT, y su parte central es un JSON en base64 con
        el campo "role": "anon" o "service_role"
    Leerlo NO expone nada: lo secreto de un JWT es la FIRMA, que aquí no
    se toca, y el rol no es un secreto. Nunca se devuelve la clave, solo
    de qué tipo es.

    El webhook necesita service_role, porque escribe en el perfil de otra
    persona -- y la clave pública no puede (ni debe) hacer eso.
    """
    clave = (os.environ.get("SUPABASE_SERVICE_KEY") or "").strip()
    if not clave:
        return "sin configurar"
    if clave.startswith("sb_secret_"):
        return "secreta (formato nuevo) — correcta"
    if clave.startswith("sb_publishable_"):
        return "PÚBLICA (formato nuevo) — no sirve, hace falta la secreta"
    if clave.startswith("sk_") or clave.startswith("pk_") or clave.startswith("whsec_"):
        return "¡es una clave de STRIPE, no de Supabase!"
    partes = clave.split(".")
    if len(partes) == 3:
        import base64, json as _json
        try:
            relleno = partes[1] + "=" * (-len(partes[1]) % 4)
            datos = _json.loads(base64.urlsafe_b64decode(relleno))
        except Exception:
            return "no reconocida"
        rol = datos.get("role")
        if rol == "service_role":
            return "service_role — correcta"
        return f"rol '{rol}' — no sirve, hace falta service_role"
    return "no reconocida"


# Estados de Stripe en los que una suscripción todavía cuenta: la persona
# tiene premium, o está a punto de perderlo pero aún no. "past_due" es
# alguien cuyo cobro falló pero que sigue teniendo acceso mientras Stripe
# reintenta -- crearle una segunda suscripción ahí sería lo peor posible.
ESTADOS_VIVOS = ("active", "trialing", "past_due", "unpaid")


def _suscripciones_vivas(user_id, excluir_id=None):
    """
    ⚠️ AÑADIDO (20 agosto) — CASO REAL ENCONTRADO PROBANDO: se crearon
    SEIS suscripciones activas para el mismo user_id sin que nada lo
    impidiera. En la sandbox da igual; en producción son seis cobros
    mensuales a la misma persona, y el webhook las trataría como buenas
    las seis.

    Devuelve (lista, se_pudo_comprobar). Lo segundo importa: si Stripe no
    contesta, NO se puede concluir "no tiene ninguna" -- eso es justo lo
    que llevaría a cobrar dos veces. Quien llama decide qué hacer con la
    duda, y aquí la duda nunca se resuelve a favor de cobrar.
    """
    try:
        res = stripe.Subscription.search(
            query=f"metadata['user_id']:'{user_id}'", limit=100)
        datos = res["data"] if isinstance(res, dict) else list(res)
    except Exception as e:
        observabilidad.capturar(e, endpoint="_suscripciones_vivas",
                                paso="buscar suscripciones en Stripe")
        return [], False
    vivas = []
    for s in datos:
        s = _plano(s)
        if s.get("status") in ESTADOS_VIVOS and s.get("id") != excluir_id:
            vivas.append(s)
    return vivas, True


def _plano(obj):
    """
    Un StripeObject NO es un dict: no admite .get(), lanza AttributeError.
    El código original hacía sub.get("metadata", {}) directamente, así que
    aunque se arreglara el import muerto, el webhook habría seguido
    reventando en la línea siguiente. Aquí se convierte una sola vez, en
    profundidad, y a partir de ahí es un dict normal.
    """
    for metodo in ("to_dict_recursive", "to_dict"):
        if hasattr(obj, metodo):
            try:
                return getattr(obj, metodo)()
            except Exception:
                pass
    return obj if isinstance(obj, dict) else {}


def _fin_de_periodo(sub):
    """
    Timestamp de fin del periodo, buscándolo donde Stripe lo pone HOY y
    donde lo ponía antes. Devuelve None si no está en ninguno de los dos,
    en vez de reventar: que no sepamos la fecha de renovación no es razón
    para no darle el premium a quien ha pagado.
    """
    items = ((sub.get("items") or {}).get("data")) or []
    fines = [i.get("current_period_end") for i in items if i.get("current_period_end")]
    if fines:
        return max(fines)
    return sub.get("current_period_end")  # forma anterior a Basil


def _actualizar_perfil(user_id, campos, evento):
    """
    Escribe en Supabase y COMPRUEBA que ha ido bien. Devuelve True/False.
    """
    import httpx
    supabase_url = os.environ.get("SUPABASE_URL", "")
    supabase_key = os.environ.get("SUPABASE_SERVICE_KEY", "")
    if not (supabase_url and supabase_key):
        observabilidad.capturar(
            RuntimeError("Webhook de Stripe sin SUPABASE_URL/SUPABASE_SERVICE_KEY"),
            endpoint="/stripe/webhook", evento=evento)
        return False
    try:
        r = httpx.patch(
            f"{supabase_url}/rest/v1/profiles?id=eq.{user_id}",
            headers=_cabeceras_supabase(supabase_key),
            json=campos,
            timeout=20.0,
        )
    except Exception as e:
        observabilidad.capturar(e, endpoint="/stripe/webhook", evento=evento,
                                paso="llamada a Supabase")
        return False
    if r.status_code >= 400:
        # ⚠️ Se dice QUÉ clave hay puesta: un 403 a secas obliga a adivinar,
        # y "la clave configurada es la pública" se arregla en diez segundos.
        tipo = _tipo_de_clave_supabase()
        observabilidad.capturar(
            RuntimeError(f"Supabase rechazó la actualización del plan: HTTP {r.status_code} "
                         f"(la clave configurada es: {tipo})"),
            endpoint="/stripe/webhook", evento=evento,
            tipo_de_clave_supabase=tipo,
            respuesta_supabase=r.text[:300], campos=list(campos))
        return False
    # 200 con lista vacía = no existe ninguna fila con ese id. Alguien ha
    # pagado y su perfil no está: hay que enterarse, no dar el ok.
    try:
        filas = r.json()
        if isinstance(filas, list) and not filas:
            observabilidad.capturar(
                RuntimeError("Pago de Stripe sin perfil que actualizar en Supabase"),
                endpoint="/stripe/webhook", evento=evento)
            return False
    except Exception:
        pass  # sin cuerpo que leer: el status ya dijo que fue bien
    return True


@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    """Recibe eventos de Stripe y actualiza Supabase."""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    webhook_secret = os.environ.get("STRIPE_WEBHOOK_SECRET", "")
    try:
        if webhook_secret:
            event = stripe.Webhook.construct_event(payload, sig_header, webhook_secret)
        else:
            # Sin secreto configurado no se puede verificar que el evento
            # venga de Stripe de verdad, así que no se toca ningún plan.
            observabilidad.capturar(
                RuntimeError("Webhook de Stripe recibido sin STRIPE_WEBHOOK_SECRET configurado"),
                endpoint="/stripe/webhook")
            return {"ok": False, "motivo": "webhook sin secreto configurado"}
    except Exception as e:
        # Firma inválida: puede ser un intento de suplantación. No se
        # manda a Sentry para que nadie pueda gastarnos la cuota
        # mandando basura firmada mal a propósito.
        raise HTTPException(status_code=400, detail=str(e))

    tipo = event["type"]

    if tipo in ("customer.subscription.created", "customer.subscription.updated",
                "customer.subscription.deleted"):
        sub = _plano(event["data"]["object"])
        user_id = (sub.get("metadata") or {}).get("user_id")
        if not user_id:
            # Alguien ha pagado y no sabemos de quién es. Hay que verlo.
            observabilidad.capturar(
                RuntimeError(f"Evento {tipo} de Stripe sin user_id en la metadata"),
                endpoint="/stripe/webhook", evento=tipo,
                suscripcion=sub.get("id"))
            return {"ok": False, "motivo": "sin user_id en la metadata"}

        if tipo == "customer.subscription.deleted":
            # ⚠️ AÑADIDO (20 agosto): antes se ponía "free" a ciegas. Con
            # varias suscripciones (ver _suscripciones_vivas), cancelar una
            # dejaba a la persona SIN premium teniendo otras pagadas.
            otras, se_pudo = _suscripciones_vivas(user_id, excluir_id=sub.get("id"))
            if otras:
                return {"ok": True,
                        "motivo": f"le quedan {len(otras)} suscripciones activas"}
            if not se_pudo:
                # Sin poder comprobarlo, quitar el premium puede dejar sin
                # servicio a quien paga. 5xx para que Stripe reintente.
                raise HTTPException(
                    status_code=503,
                    detail="No se pudo comprobar si quedan otras suscripciones")
            campos = {"plan": "free"}
        else:
            campos = {"plan": "premium",
                      "stripe_customer_id": sub.get("customer"),
                      "stripe_subscription_id": sub.get("id")}
            fin = _fin_de_periodo(sub)
            if fin:
                campos["suscripcion_activa_hasta"] = datetime.datetime.fromtimestamp(
                    fin, datetime.timezone.utc).isoformat()
            else:
                # Sin fecha de renovación se le da el premium igual -- ha
                # pagado -- pero queremos saber por qué no venía.
                observabilidad.capturar(
                    RuntimeError("Suscripción de Stripe sin fecha de fin de periodo"),
                    endpoint="/stripe/webhook", evento=tipo, suscripcion=sub.get("id"))

        if not _actualizar_perfil(user_id, campos, tipo):
            # 500 a propósito: Stripe reintenta con espera creciente
            # durante días, así que un fallo pasajero se recupera solo.
            raise HTTPException(status_code=500,
                                detail="No se pudo actualizar el plan; reintentadlo")

    return {"ok": True}


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
    # ⚠️ AÑADIDO (28 agosto) — el peso de referencia para la DER efectiva.
    # En un perro con sobrepeso las kcal se calculan sobre el peso IDEAL,
    # así que la densidad de nutrientes tiene que medirse sobre el mismo
    # peso: si se midiera sobre el real, la DER efectiva saldría más baja
    # de lo que es y los mínimos subirían de más. Si no llega, se usa el
    # peso real, que escala un poco de más -- el lado seguro.
    peso_objetivo_kg: Optional[float] = None
    # El BCS de 9 puntos, para derivar el objetivo cuando no viene
    # declarado. Ver `_peso_de_referencia`.
    bcs: Optional[float] = None
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
# ⚠️ LOS SELLOS DE LOS DATOS, A NIVEL DE MÓDULO (29 agosto). Vivían dentro
# de /verificar, y en cuanto hicieron falta en un segundo sitio -- la pauta
# firmada, que guarda con qué datos se calculó -- había que copiarlos. Un
# número copiado se separa: es lo mismo que ya pasó con la tabla de
# patologías del motor viejo, con el fósforo renal a 1400 en un lado y a
# 1200 en el otro.
def _fecha_utc_ahora():
    """Ahora, en UTC y en ISO. Con import local: ver el comentario de quien
    la usa -- este archivo tiene un `import datetime` de módulo que gana
    sobre el `from datetime import datetime`, y confundirlos revienta en
    tiempo de ejecución, no al arrancar."""
    from datetime import datetime as _Fecha, timezone as _Zona
    return _Fecha.now(_Zona.utc).isoformat()


def _sello_de_main_py():
    """El sello del código que está corriendo. Es el mismo número que enseña
    /verificar en `sello_main_py_actual`, y va con cada pauta firmada para
    poder responder "¿con qué versión del motor se calculó esto?" sin
    adivinar."""
    import hashlib
    return hashlib.sha256(open(__file__, "rb").read()).hexdigest()[:16]


SELLOS_DE_LOS_DATOS = {
        # ⚠️ ACTUALIZADO (21 agosto) al añadir 7 alimentos con fuente
        # verificada (corazón y molleja de pavo, hígado de pavo y de pato,
        # y completar corazón/molleja de pollo, molleja de pavo y timo de
        # ternera). Este sello SOLO se toca cuando el cambio de datos es a
        # propósito y está documentado: si no coincide sin haberlo tocado,
        # es que alguien alteró el catálogo, y eso es lo que vigila.
        # 7 sep (4): TAURINA Y L-CARNITINA en las 159 fichas -- claves nuevas, no requisitos de FEDIAF, no verificadas todavia (ver UNIDADES.md). Valor real donde hay fuente (Spitze et al. 2003 para taurina, principalmente) y sin_dato donde no. Nada activa nada en el motor: es trabajo de catalogo para cuando haya un suelo real por patologia (candidata: dcm_taurina_respondedora / cardiopatias). Mapeo por nombre exacto revisado a mano ficha a ficha, sin confundir familias (p.ej. "Repollo" nunca hereda el dato de "Pollo": Spitze confirma taurina=0 en todos los vegetales).
        # 7 sep (3): "Laringe de vacuno" pasa de categoria "Hueso carnoso" a "Extras" -- bloqueada por tejido tiroideo desde el 6 de septiembre, nunca puede aportar hueso a ningun menu, y su categoria antigua solo servia para disparar dos avisos ya conocidos en auditar_catalogo.py ("hueso con poco calcio, es cartilago"). 0 referencias en catalogo_menus.json (comprobado), asi que no afecta a los menus precalculados. Decision pendiente desde el 25 de agosto en PENDIENTE_NUTRICION.md, cerrada.
        # 7 sep (2): linoleico de "Grasa de pollo" (19,5 g/100g) -- USDA FDC 173564 "Fat, chicken", cuya proteina (0) y grasa (99,8) ya coincidian exactas con esta ficha. Cierra el hueco que quedaba en PENDIENTE_NUTRICION.md desde el 25 de agosto.
        # 7 sep: 4 visceras (Bazo de vaca, Pancreas de vaca, Bazo de cordero, Cerebro de ternera) con `sin_dato` incompleto -- sus propias notas ya decian que faltaban ciertos minerales/vitaminas ("sin dato fiable... se dejan en 0"), pero el campo estructurado no los tenia, asi que contra un maximo contaban como cero MEDIDO en vez de hueco. Encontrado auditando alimentos_v3_final.json de verdad (comparando texto contra estructura), no solo comprobando formato. Ningun valor numerico cambia, solo que estas claves antes contadas como "0 real" pasan a "no lo sabemos".
        # 7 sep (5): NUEVO ALIMENTO -- "Pets Purest Aceite de Salmón Escocés" (160ª ficha), añadido a petición explícita de la usuaria con foto de la etiqueta real. Mismo patrón que los otros dos aceites de salmón del catálogo: grasa/proteína/fibra de la propia etiqueta, EPA/DHA en el extremo bajo de los rangos declarados, linoleico = omega-6 total (aproximación ya usada en esta familia de productos), vitamina E en sin_dato pese a que la etiqueta menciona "0,5% tocoferoles" en INGREDIENTES -- no es una cifra analítica, mismo criterio que ya se aplicó a los otros dos. Sin dosis de fabricante (no se pudo determinar el volumen de una pulsación en ml). Detalle completo en su nota_datos.
        # 8 sep (4): "Atun" y "Caballa" ganan `restricciones_patologia` para la patologia nueva `reaccion_adversa_alimento` -- SACN5 5a ed., cap.31, Tabla 31-3: «Vasoactive amines -- Avoid foods that contain certain fish ingredients (e.g., tuna, mackerel, skipjack, bonito)». Ningun valor nutricional cambia: es el mismo mecanismo por el que el Platano no entra en un menu de diabetes. El "bonito" y el "listado" (skipjack) no estan en el catalogo. Sello recalculado a proposito.
        # 8 sep (3): SIN CAMBIOS, y hubo que REVERTIR un cambio equivocado del mismo dia. Se puso aqui "20a15984bafa669f" creyendo que el sello estaba roto en main -- NO lo estaba: estos sellos NO son el SHA del fichero crudo sino el del CONTENIDO CANONICO (json.dumps con sort_keys y ensure_ascii), a proposito, para que reordenar claves o cambiar la indentacion no dispare una falsa alarma. Se comparo contra el crudo, que da otro hash, y de ahi salio una "correccion" que rompio el sello de verdad. El BLOQUE 12 la cazo. La leccion no es el numero: es que el metodo de comprobacion hay que leerlo antes de usarlo.
        "alimentos_v3_final.json":      "2172e3d9b8e29346",   # ver la nota (4), justo arriba
        # 6 sep: nota_datos de los 4 alimentos excluidos por tejido tiroideo (Cuello de pavo/pato/ternera, Laringe de vacuno) documenta el bloqueo -- ver seguridad.TIROIDES_EXCLUIR.
        # 28 ago (2): EL HIGADO Y EL CORAZON DE PAVO, resembrados desde el pollo del USDA -- su aminograma venia del pavo del USDA, que tiene la isoleucina y la valina un 40% bajas (Leu/Ile 2,52 contra 1,47-1,98 del resto). Reescalados a NUESTRA proteina. Las otras cinco fichas de pavo NO se cargan: traian histidina = isoleucina = valina exactos, y eso es una copia, no una medida. Ver el BLOQUE 27. // 28 ago: PURINAS DE CUATRO VISCERAS con cifra publicada (timo 525, bazo de cordero 322, bazo de vaca 185, pulmon de ternera 117). NO se uso la banda generica 84-243 que se habia propuesto: para el timo habria declarado ~160 cuando la cifra son 525, un factor de 3 a 4 POR ABAJO, y es el alimento solido con mas purinas de las tablas. Pancreas, testiculos y pulmon de cordero se quedan como hueco: no hay dato. Ver el BLOQUE 33
        # 7 sep (2): nueva fila "Fibra", con los seis campos (minAdulto..maxCachorroCrecimiento) a "-" -- FEDIAF no da minimo ni maximo de fibra en la Tabla III-3b, asi que esta fila NO es un requisito nuevo: no exige ni limita nada a un perro sano. Existe para que verificar.MAPA pueda leer la clave "fibra" y topes_de_patologias() pueda ponerle un suelo por patologia con fuente real (primer uso: hiperlipidemia, SACN5 cap.28). auditar_fediaf.py la lista en NO_SON_NUTRIENTES_DE_LA_TABLA y ademas comprueba que nunca lleve un numero, para que no repita el fallo del 25 de agosto (fila "Fibra" con minimo/maximo inventados que el analizador exigia). Ver PENDIENTE_NUTRICION.md.
        # 7 sep: nota_auditoria de Vitamina_E ampliada con la cita exacta de FEDIAF (Tabla VII-14, "Conversion factors - Vitamin source to activity") tras la pregunta que dejo abierta Fascetti & Delaney 2a ed. -- CONFIRMA el x0.67 ya usado (tocoferol NATURAL de alimentos frescos, no el acetato SINTETICO de suplemento que cita Fascetti, que da un numero distinto). Ningun numero cambia, solo el texto de una fila.
        # 7 sep (4): QUITADO el maxAdulto=4000 de Fosforo -- no tenia fuente, llevaba asi desde el primer PR del repo. Investigado a fondo antes de quitarlo: FEDIAF no da numero (solo nota "h" informativa), NRC 2006 dice explicitamente que no hay datos para fijar un SUL de fosforo en perros, y Dobenecker et al. 2021 (PLOS ONE, el estudio mas centrado en el tema) concluye que todavia no se puede definir un no-effect-level. El numero recortaba de verdad el menu automatico estandar de un adulto (justo en el limite) contra un maximo sin origen -- encontrado revisando la Tabla III-3b entera del PDF contra la transcripcion de auditar_fediaf.py, celda a celda. Fosforo pasa a SIN_MAXIMO, igual que Vitamina_E.
        # 7 sep (3): dos filas nuevas, "Taurina" y "L_carnitina", MISMO PATRON que "Fibra" -- las seis columnas a "-", no exigen ni limitan nada a un perro sano. Existen para que verificar.MAPA pueda leer las claves y topes_de_patologias() pueda ponerles un suelo por patologia con fuente real -- primer uso: dcm_taurina_respondedora (250/50 mg/1000kcal, SACN5 cap.36 Tabla 36-4). auditar_fediaf.py las lista en NO_SON_NUTRIENTES_DE_LA_TABLA y comprueba que nunca lleven un numero, igual que Fibra.
        # 8 sep (5): ACTUALIZADO POR UN SELLO QUE LLEVABA ROTO DESDE EL COMMIT 19e8358 DE ESTA MISMA RAMA. Ese commit anadio la fila "Omega3_total" (seis campos a "-", mismo patron que Fibra/Taurina/L_carnitina/EPA: no exige ni limita nada a un perro sano, existe para que verificar.MAPA pueda leer la clave y una patologia pueda ponerle un suelo con fuente) y "EPA", y NO toco este sello. La bateria lo habria dicho en el BLOQUE 12; no se ejecuto entera despues de aquel commit -- se ejecuto tres minutos ANTES. Asi que el fallo no es del sello, que hizo su trabajo: es de haber empujado sin correr la bateria. El contenido esta comprobado fila a fila por auditar_fediaf.py (248 comprobaciones, 0 discrepancias) antes de mover este numero.
        # 8 sep (6): DEVUELTO EL MAXIMO DE FOSFORO EN ADULTO (4000 mg/1000 kcal). Se habia quitado el 7 de septiembre escribiendo que «ni FEDIAF ni NRC ni Dobenecker dan un maximo» y que la Tabla III-3a/b solo traia la nota h informativa. La parte de NRC y Dobenecker es CIERTA (hablan del SUL toxicologico, que no existe); la de FEDIAF es FALSA: su maximo NUTRICIONAL de 4 g/1000 kcal esta en la Tabla III-3b («Adult: 4.00 (N)»), en la III-3a («Adult: 1.60 (N)» g/100 g MS, que por 2,5 son 4,00) y en el texto de 3.3.1 con todas las letras. Se colo porque en el texto extraido del PDF la columna de maximos cae visualmente sobre la fila ANTERIOR: leyendo linea a linea, el calcio parece tener cuatro maximos y el fosforo ninguno. Entre el 7 y el 8 de septiembre el motor NO TUVO techo de fosforo en adulto y el catalogo precalculado llego a tener un menu con 4124 mg, por encima del maximo de FEDIAF. auditar_fediaf.py corregido a la vez, y ademas ahora comprueba que una etapa SIN maximo en FEDIAF lleve «-» en el JSON -- antes ni la miraba, que es el mismo agujero.
        # 10 sep: DOS MAXIMOS DONDE FEDIAF PUBLICA DOS, y la etiqueta de cual es cual en las trece filas que tienen maximo. Ningun numero que aplique el motor cambia. Lo que se anade es (a) `maximo_origen`: si ese techo es LEGAL (L) o NUTRICIONAL (N), que NO es lo mismo -- §3.1.3 dice que el legal solo aplica si el nutriente se ANADE como aditivo, y si viene solo del alimento manda el nutricional; y (b) el maximo NUTRICIONAL de la vitamina D (20,0 µg/1000 kcal, «320.00 (N)» en la Tabla III-3a), que es el unico nutriente del perfil canino con los dos publicados y con el legal por debajo. Hasta hoy ese numero vivia solo en prosa dentro de una `nota_auditoria`, asi que el dia que cambie la ley no habria de donde sacarlo. Pedido por Elena: «aunque el legal sea mas bajo debes dejar anotado el limite nutricional tambien porque lo legal podria cambiar». Y desde hoy `auditar_transcripcion_fediaf.py` REHACE los 18 maximos desde `fediaf_tabla_III_3a.txt` -- la columna de maximos no la comprobaba NADIE, y es justo la que se rompio el 7 de septiembre cuando el motor se quedo un dia sin techo de fosforo en adulto.
        # 10 sep (2): SOLO TEXTO. La regla del maximo LEGAL que llevan citada las
        # 14 filas con techo legal (`nota_maximo_origen`) estaba copiada mal: unia
        # dos frases de FEDIAF sin marcar el corte y remataba con «instead the
        # nutritional maximum applies», cuando la fuente dice «instead the
        # nutritional maximum, WHEN INCLUDED IN THE RELEVANT TABLES, should be
        # taken into account» -- que es una condicion, y la habiamos borrado.
        # Y en la misma pasada, la cita del maximo nutricional de Ca y P
        # («AAFCO introduced a nutritional maximum...») unia dos frases sin
        # marcar el corte donde va «(Dzanis DA, 1994)».
        # Ningun numero cambia; lo caza `auditar_citas.py` (BLOQUE 85).
        # ⚠️ Y AQUI SE VOLVIO A CAER EN LA MISMA TRAMPA QUE EL 8 DE SEPTIEMBRE,
        # con la advertencia escrita cuatro lineas mas arriba: el sello se
        # calculo con `ensure_ascii=False` y `/verificar` lo calcula con
        # `ensure_ascii=True`. Da otro hash, tiene la misma pinta, y el numero
        # equivocado no lo caza nadie salvo el BLOQUE 12 -- que lo cazo. La
        # forma de sacarlo sin equivocarse no es repetir la cuenta a mano: es
        # leer lo que devuelve `/verificar` en `encontrado`.
        "requerimientos_v2_final.json": "d79627207a0231d2",
        # 6 sep (2): nota_auditoria de los 12 aminoacidos corregida -- decia "el motor todavia no lo verifica porque ningun alimento tiene aminograma", que era cierto ANTES del 28 de agosto y llevaba mas de una semana desactualizado (los 12 SI estan en verificar.MAPA desde entonces, 94/159 fichas con aminograma). Ningun numero cambia, solo el texto de 12 filas.
        # 6 sep: VITAMINA D AL TECHO LEGAL. Es el UNICO nutriente del perfil canino con techo legal (UE) por debajo del nutricional -- 227.00 UI (L) frente a 320.00 UI (N) en la Tabla III-3a, confirmado dos veces en el PDF de FEDIAF. El max de antes (20 ug = 800 UI) era el nutricional; el que manda por ser mas estricto es el legal, 227 x 2.5 = 567.5 UI = 14.1875 ug/1000kcal. auditar_fediaf.py actualizado a la vez para no comparar contra el numero equivocado. Ver PENDIENTE_NUTRICION.md.
        # 28 ago: EL ANCLA DE 110. Cada nutriente lleva ahora `minAdulto110`, la columna de DER 110 de la Tabla III-3b, sacada de NUESTRA transcripcion auditada del PDF y no de fuera. Con las dos anclas se puede aplicar la ecuacion del apartado 7.2.5: cuando el perro come menos, el minimo por 1000 kcal sube. Los 38 cuadraron con el minAdulto de siempre sin una discrepancia, o sea que nuestra columna ES la de 95. Ver el BLOQUE 34
    }


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
    SELLOS = SELLOS_DE_LOS_DATOS
    SELLOS_CRUDOS = {
        "der.py": "72c85a11b2289dec",   # 10 sep: la Tabla 5-3 de SACN5 da LA CIFRA del frio que FEDIAF deja como rango de 1 a 9 -- pelo corto +95 %, pelo largo +59,5 %, Labrador +25 %, Gran Danes +22 %, cada una con su salto de temperatura. El comentario decia que no hay cifra y era falso: lo era de FEDIAF, no del conjunto de las fuentes. Lo que falta sigue siendo la PREGUNTA en la ficha, que es producto. | 9 sep (3): la §7.2.3.5 de FEDIAF, leida entera, escrita en der.py -- las tres cosas que anade a la Tabla VII-7 y por que no se aplica ninguna: el frio (10-90 % mas de calorias durmiendo fuera en invierno; hueco real, falta la pregunta en la ficha), el suelo de 70 kcal/kg^0,75 de la literatura contra nuestros 95 de la recomendacion, y la termogenesis de la comida (~10 %, sube con proteina y con mas tomas, sin cifra para ninguna de las dos). | 9 sep (2): el escalon de edad pasa a ser el de la Tabla VII-6 de FEDIAF -- 130 (1-2 anos) / 110 (3-7) / 95 (>7), o sea +20 el joven y -15 el senior contra el +15/-7 de Thes 2014 que habia; nuestro -7 era un -6,4 % cuando FEDIAF dice -13,6 % y SACN5 cap.5 dice 10-20 %. Y el grupo "joven" era CODIGO MUERTO: existia en AJUSTE_EDAD y no se pasaba nunca, ni aqui ni en el front, asi que un perro de ano y medio recibia lo mismo que uno de cinco. | 9 sep: la cifra de raza de la Tabla VII-7 va EN VEZ del nivel de actividad, y lo dice la propia guia (la frase que presenta la tabla, y la seccion 7.2.3.4: la diferencia de raza YA CONTIENE la de actividad). Cierra PREGUNTAS_ABIERTAS.md P-11; lo separa de las lecturas «suelo» y «sumar» el BLOQUE 54 apartado 2-bis. | 8 sep: el DER verificado contra FEDIAF 2025 (Tablas VII-7 y VII-8b) y cerrado -- ver DECISIONES.md D-11. Cambian TRES cosas: se quita el tope de x6 RER en lactancia (no es de FEDIAF y recortaba hasta un 33 %), se adoptan las dos razas con cifra propia de FEDIAF (Gran Danes 200, Terranova 105; un Gran Danes recibia el 55 % de lo que le toca), y el respaldo de crecimiento pasa a la regla de SACN5 por edad (3 x RER hasta los 4 meses, 2 x RER despues) -- de sus tres escalones viejos, DOS eran codigo muerto. Lo vigila el BLOQUE 54.
        # 6 sep: 3 correcciones de cita en comentarios (VII-7 no VII-6, Thes 2015 no 2014, y el escalon 210/175/140 no es tabla de FEDIAF) -- ningun numero ni comportamiento cambia.
        # ⚠️ 9 sep: SELLO MOVIDO, y solo cambia UN numero. El BCS 9 pasa de un
        # exceso del 40 % a uno del 45 %, porque la Tabla VII-2 del Anexo 7.1 de
        # FEDIAF dice «>45 %» y la recta del 10 % por punto se queda corta justo
        # ahi. La misma tabla CONFIRMA la recta en los otros ocho puntos: nuestro
        # 10 % lineal es el extremo bajo de cada uno de sus rangos, de BCS 1 a 8.
        # || Ninguno de los 100 casos de `der_casos.json` usa `condicion_idx`, asi
        # que el contrato del DER no se mueve y no hay que regenerarlo ni copiarlo
        # al otro repo. Lo que SI hay que hacer alli es el mismo cambio en la copia
        # de `src/der.js`: esta anotado en PENDIENTE_NUTRICION.md.
        # || Lo vigila el BLOQUE 63, que compara la tabla de FEDIAF fila a fila y
        # ademas las DOS copias de la regla de BCS que hay en este repo.
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
        # ⚠️ AÑADIDO (20 agosto) — para poder confirmar desde el móvil, sin
        # terminal, si el despliegue tiene Sentry recogiendo errores o si
        # falta poner SENTRY_DSN en las variables de entorno de Render.
        "sentry_activo": observabilidad.activo(),
        # ⚠️ AÑADIDO (20 agosto) — para poder ver de un vistazo, desde el
        # móvil, si el cobro está bien montado. NUNCA sale la clave ni un
        # trozo: solo si es la real o la de pruebas, deducido del prefijo.
        # "coherente" es la comprobación que importa: clave real con
        # precios de sandbox es la combinación que rompería el primer
        # cobro de verdad.
        "stripe": {
            "modo": _modo_stripe(),
            "precios": ("de sandbox" if _precio_de_sandbox(PRICE_MENSUAL)
                        else "propios"),
            "webhook_configurado": bool(os.environ.get("STRIPE_WEBHOOK_SECRET")),
            "coherente": not (_modo_stripe() == "real"
                              and _precio_de_sandbox(PRICE_MENSUAL)),
        },
        # ⚠️ AÑADIDO (20 agosto): para ver de un vistazo, sin pagar nada y
        # sin enseñar la clave, si la que hay puesta puede escribir en los
        # perfiles. Un 403 al activar un premium sale casi siempre de aquí.
        "supabase": {
            "url_configurada": bool(os.environ.get("SUPABASE_URL")),
            "clave": _tipo_de_clave_supabase(),
        },
    }


@app.post("/analizar")
def analizar(req: AnalisisRequest):
    observabilidad.etiquetar(endpoint="/analizar", etapa=req.etapa_requisitos)
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


# =====================================================================
# EL FORMULADOR DEL VETERINARIO
#
# Dos endpoints, y los dos existen por la misma razón: un profesional no
# elige entre "automático" y "personalizar" -- formula. Pone los alimentos
# y los gramos, ve lo que va saliendo, y cuando quiere que el motor le
# cierre lo que falta, se lo pide.
#
# ⚠️ POR QUÉ NO SE HACE EN EL NAVEGADOR. La tentación era llevarse la tabla
# de composición y los requisitos de FEDIAF a la app y calcular ahí, que
# sería instantáneo. Es exactamente el fallo que el CLAUDE.md describe con
# el DER, calculado en dos sitios: el día que uno de los dos cambie, la
# pantalla dirá una cosa y el motor comprobará otra, y no saltará ningún
# error. Aquí se calcula donde vive `MAPA`, y punto.
#
# Y hay una segunda razón, más seria: lo que la pantalla enseña tiene que
# ser lo MISMO que decide si un menú se entrega. Eso incluye los topes por
# patología, que el semáforo de FEDIAF no ve -- son los requisitos de un
# perro SANO, y un renal con 3084 mg de fósforo salía verde (regla 2).
# =====================================================================
class PeticionFormular(BaseModel):
    """Lo que el veterinario tiene puesto en la mesa ahora mismo."""
    gramos_por_alimento: dict = {}
    der_objetivo: float
    etapa_requisitos: str = "Adulto"
    peso_perro_kg: Optional[float] = None
    peso_adulto_esperado_kg: Optional[float] = None
    peso_objetivo_kg: Optional[float] = None
    bcs: Optional[float] = None
    patologias: Optional[list] = None
    # Solo para autocompletar: lo que NO puede entrar.
    especies_excluidas: list[str] = []
    nombres_excluidos: Optional[list] = None
    categorias_excluidas: Optional[list] = None
    # Solo para autocompletar: si el total de gramos lo fija él.
    gramos_totales: Optional[float] = None
    # ⚠️ AÑADIDO (8 septiembre) — EL PELDAÑO DE LA ESCALERA.
    # Aquí importa más que en `/menu/v2`: autocompletar no recorría la
    # escalera NUNCA -- formulaba con las proporciones completas y, si no
    # salía, decía que no. O sea que el veterinario tenía menos margen que un
    # tutor, al que el motor sí le baja de peldaño solo. Ahora lo elige él.
    peldano: Optional[str] = None


def _estado_de_la_racion(datos):
    """La foto completa de unos gramos: los 43 requisitos, el ratio, los
    topes de seguridad crónica y los de patología, y las kcal de verdad.

    Es lo que `_garantizar_verificado` mira antes de dejar salir un menú,
    puesto donde el veterinario pueda verlo MIENTRAS formula en vez de
    enterarse al final."""
    al, req = cargar_v2()
    gramos = {n: float(g) for n, g in (datos.gramos_por_alimento or {}).items()
              if _num_positivo(g)}
    desconocidos = [n for n in gramos if n not in al]
    if desconocidos:
        raise HTTPException(400, "No tenemos datos de: " + ", ".join(desconocidos))

    kcal = sum((al[n].get("energia", 0) or 0) / 100.0 * g for n, g in gramos.items())
    salida = {
        "gramos_total": round(sum(gramos.values()), 1),
        "kcal": round(kcal, 1),
        "der_objetivo": datos.der_objetivo,
        "desvio_kcal_pct": (round(100.0 * (kcal - datos.der_objetivo) / datos.der_objetivo, 1)
                            if datos.der_objetivo else None),
        "reparto_categorias": {},
    }
    for n, g in gramos.items():
        cat = al[n].get("categoria") or "Sin categoría"
        salida["reparto_categorias"][cat] = round(
            salida["reparto_categorias"].get(cat, 0.0) + g, 1)

    if not gramos:
        salida.update({"ficha": None, "problemas_seguridad": [],
                       "topes_de_patologia_rotos": []})
        return salida

    peso_ref, _ = _peso_de_referencia(datos)
    salida["ficha"] = verificar_v2(gramos, al, req, datos.der_objetivo,
                                   datos.etapa_requisitos,
                                   peso_referencia_kg=peso_ref)
    salida["problemas_seguridad"] = _seguridad_completa(
        gramos, al, datos.der_objetivo, datos.etapa_requisitos, datos.patologias,
        peso_perro_kg=datos.peso_perro_kg)
    # ⚠️ Y LOS TOPES DE PATOLOGÍA, que el semáforo no ve. Sin esto, la
    # pantalla del veterinario le enseñaría un renal en verde con el fósforo
    # por las nubes -- verde de FEDIAF, que son los requisitos de un perro
    # sano. Es la regla 2, y se comprueba aquí por lo mismo que se comprueba
    # en `_garantizar_verificado`: porque el que se olvida no da error.
    salida["topes_de_patologia_rotos"] = _tope_patologia_roto(
        gramos, al, datos.patologias, datos.etapa_requisitos, req=req,
        der_efectiva=der_efectiva_de(datos.der_objetivo,
                                     _peso_de_referencia(datos)[0]),
        peso_adulto_esperado_kg=getattr(datos, "peso_adulto_esperado_kg", None))
    salida["huecos"] = _huecos_en_cristiano(salida["ficha"])
    # ⚠️ DE DONDE SALE CADA TECHO DE FEDIAF, Y CUAL ES EL OTRO (10 septiembre).
    #
    # Un maximo de FEDIAF puede venir de dos sitios que NO son lo mismo, y hasta
    # hoy la pantalla ensenaba un solo numero sin decir cual:
    #
    #   (L) LEGAL, del Reglamento (UE) 2017/1492. Y §3.1.3: «A legal maximum only
    #       applies when the particular trace element or vitamin is ADDED to the
    #       recipe as an additive. If the nutrient comes exclusively from feed
    #       materials, the legal maximum does not apply, instead the nutritional
    #       maximum applies».
    #   (N) NUTRICIONAL, que es criterio de FEDIAF y admite lectura profesional.
    #
    # MEDIDO sobre los 216 menus del catalogo (10-sep-2026): en 215 de 216 los
    # ocho nutrientes con techo llevan parte ANADIDA por un suplemento -- el yodo
    # un 91 % de mediana, la vitamina D un 70 %, el zinc un 60 %. O sea que el
    # techo legal es el que corresponde por la §3.1.3 en casi todos los menus, y
    # aplicarlo tambien al que falta es mas estricto que la norma, nunca menos.
    # Por eso el motor sigue aplicando SIEMPRE el mas bajo, y aqui se dice cual
    # es y cual seria el otro, en vez de esconderlo.
    salida["techos_de_fediaf"] = _techos_de_fediaf(req, datos.etapa_requisitos)
    return salida


def _techos_de_fediaf(req, etapa):
    """Los maximos de FEDIAF con su procedencia, para la pantalla del profesional.

    No calcula nada: lee lo que ya esta en `requerimientos_v2_final.json`, que es
    la Tabla III-3a/b transcrita y auditada contra el PDF celda a celda
    (`auditar_transcripcion_fediaf.py`, BLOQUE 77). Calcularlo aqui seria la
    tercera copia de la misma tabla.
    """
    from verificar import MAPA, maximo_de, EQUIVALENCIA, SUFIJO
    etapa_req = SUFIJO.get(EQUIVALENCIA.get(etapa, etapa), "Adulto")
    # `req` llega como un dict {nombre del requisito: fila}, que es la forma que
    # devuelve `cargar_v2()`. Se recorre por el MAPA para no depender de eso.
    salida = []
    for nombre, fila in sorted((req or {}).items()):
        if not isinstance(fila, dict):
            continue
        clave = MAPA.get(nombre)
        tope = maximo_de(fila, nombre, etapa_req)
        if tope is None:
            continue
        salida.append({
            "nutriente": nombre,
            "clave": clave,
            "unidad": fila.get("unidad"),
            "maximo_por_1000kcal": tope,
            # «legal_UE» o «nutricional». Es la diferencia que decide si un
            # profesional puede leerlo con criterio o no lo mueve nadie.
            "origen": fila.get("maximo_origen"),
            "en_la_fuente": fila.get("maximo_en_la_fuente"),
            # El otro numero, donde FEDIAF publica los dos. Hoy solo la
            # vitamina D: 14,1875 el legal y 20,0 el nutricional.
            "maximo_nutricional_por_1000kcal": fila.get("maximo_nutricional_por_1000kcal"),
            "maximo_nutricional_en_la_fuente": fila.get("maximo_nutricional_en_la_fuente"),
        })
    salida.sort(key=lambda x: (x["origen"] != "legal_UE", x["nutriente"]))
    return salida


def _huecos_en_cristiano(ficha):
    """Los huecos del catálogo de esta ración, con el nombre del nutriente y
    los alimentos a los que les falta.

    ⚠️ AÑADIDO (29 agosto) — CASO REAL DE LA USUARIA mirando la pantalla de
    firmar: «esto que sale aquí asusta y no se entiende bien», y debajo una
    lista de claves en crudo: `calcio, araquidonico, dha, epa, ..., vitA`.
    Veinticuatro palabras sin frase, justo encima del botón de firmar.

    El hueco NO es un fallo del menú y la pantalla tiene que poder decirlo:
    es que de ALGÚN ALIMENTO de la ración no está publicado ese dato. Se
    cuenta como cero, así que contra un mínimo es conservador -- como mucho
    sobra un suplemento -- y contra un máximo se imputa por familia.

    La traducción se hace AQUÍ y no en la app porque el nombre de cada clave
    vive en `MAPA`, junto a la tabla de FEDIAF. Una segunda lista en el
    frontend sería otra copia que se separa."""
    from verificar import MAPA
    nombre_de = {clave: nombre.replace("_", " ") for nombre, clave in MAPA.items()}
    salida = []
    for tipo, origen in (("sin_dato", ficha.get("datos_incompletos") or {}),
                         ("dato_dudoso", ficha.get("datos_dudosos") or {})):
        for clave, alimentos in origen.items():
            salida.append({
                "clave": clave,
                # Si un día aparece una clave que no está en MAPA -- las hay,
                # como `purinas`, que es de seguridad y no un requisito de
                # FEDIAF -- se enseña la clave en vez de esconder la fila.
                "nombre": nombre_de.get(clave, clave),
                "tipo": tipo,
                "alimentos": sorted(set(alimentos)),
            })
    salida.sort(key=lambda x: (x["tipo"] != "dato_dudoso", x["nombre"].lower()))
    return salida


def _num_positivo(v):
    try:
        return float(v) > 0
    except (TypeError, ValueError):
        return False


@app.post("/formular/estado")
def formular_estado(datos: PeticionFormular):
    """Qué tiene esta ración ahora mismo. Se llama en cada cambio de gramos."""
    observabilidad.etiquetar(endpoint="/formular/estado", etapa=datos.etapa_requisitos)
    return _estado_de_la_racion(datos)


@app.post("/formular/autocompletar")
def formular_autocompletar(datos: PeticionFormular):
    """Cierra lo que falta SIN tocar lo que el veterinario ya ha puesto.

    Sus gramos son gramos fijos, no una sugerencia: el motor completa la
    ración alrededor. Si con esas cantidades no existe una ración que cumpla
    los requisitos, se dice -- no se cambian sus cifras por la puerta de
    atrás. Lo que devuelve es editable: es un punto de partida, no un
    resultado cerrado."""
    observabilidad.etiquetar(endpoint="/formular/autocompletar", etapa=datos.etapa_requisitos)
    al, req = cargar_v2()
    fijos = {n: float(g) for n, g in (datos.gramos_por_alimento or {}).items()
             if _num_positivo(g)}
    desconocidos = [n for n in fijos if n not in al]
    if desconocidos:
        raise HTTPException(400, "No tenemos datos de: " + ", ".join(desconocidos))

    excluidos = list(datos.especies_excluidas or []) + list(datos.nombres_excluidos or [])
    _hay_comida_f = _hay_comida_de_verdad(al, excluidos, datos.categorias_excluidas)

    # ⚠️ AUTOCOMPLETAR RECORRE LA ESCALERA (11 de septiembre de 2026), COMO
    #     HACE `/menu/v2` DESDE SIEMPRE.
    #
    # CASO REAL, medido ese dia contra este mismo endpoint. Un adulto de 22 kg
    # y estas cantidades, que son lo que escribe un veterinario cualquiera:
    #
    #     Conejo 400 g + Espinazo de conejo 150 g
    #
    #     peldano 0 (estricto) ................... no sale
    #     peldano 1 .............................. no sale
    #     peldano 2 .............................. no sale
    #     peldano 3 .............................. SALE
    #
    # Y esto probaba UN peldano y se rendia. Medido sobre seis entradas
    # realistas: CERO salian. La pantalla, mientras tanto, prometia «el motor
    # completa alrededor» -- Elena: «hay un aviso que dice que se autocompleta
    # el menu con los gramos que ya ha puesto y en la mayoria de casos no
    # pasa».
    #
    # No es relajar nada: la escalera solo suelta las proporciones de BARF, que
    # son criterio NUESTRO (regla 3), y cada intento vuelve a pasar por los 43
    # requisitos, el ratio Ca:P y los topes de seguridad y de patologia. Es lo
    # mismo que ya hacia el generador del dueño; lo raro era que aqui no.
    #
    # ⚠️ Y SI EL VETERINARIO HA ELEGIDO PELDAÑO, NO SE BAJA. Esa es la regla
    # escrita en CLAUDE.md para `/menu/v2` y vale igual aqui: bajar seria
    # cambiarle la decision a quien la ha tomado, que es lo contrario de por
    # que se puede elegir. Con peldaño elegido se prueba ese y solo ese.
    if datos.peldano and _peldano_por_clave(datos.peldano, _hay_comida_f):
        _escalones_f = [(_peldano_por_clave(datos.peldano, _hay_comida_f) + (datos.peldano,))]
    else:
        _escalones_f = [(m, sup, k or PELDANO_ESTRICTO)
                        for m, sup, k in _escalera_de_relajacion(_hay_comida_f)]

    ok, gramos = False, None
    _peldano_usado_f = datos.peldano or PELDANO_ESTRICTO
    for _margenes_f, _supl_f, _clave_f in _escalones_f:
        ok, gramos = resolver_v2(
            datos.der_objetivo, datos.etapa_requisitos, al, req,
            datos.peso_perro_kg, dosis_maxima_fabricante,
            excluidos=excluidos or None,
            margenes_categoria=_margenes_f, max_suplementos=_supl_f, time_limit=20.0,
            forzar=list(fijos) or None,
            gramos_fijos=fijos or None,
            patologias=datos.patologias,
            peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
            peso_objetivo_kg=_peso_de_referencia(datos)[0],
            categorias_excluidas=datos.categorias_excluidas,
        )
        _peldano_usado_f = _clave_f
        if ok:
            break
        # ⚠️ Si es imposible POR ARITMETICA, bajar de peldaño no puede
        # arreglarlo: no hay combinacion de proporciones que cambie que un
        # minimo esté por encima de un maximo. Se para y se dice, como en
        # `/menu/v2`.
        if isinstance(gramos, dict) and gramos.get("_imposible"):
            break
    if not ok:
        _imp = (gramos or {}).get("_imposible") if isinstance(gramos, dict) else None
        respuesta_no = {"factible": False,
                        "motivo": _imp or ("Con esas cantidades fijas no existe ninguna ración "
                                           "que cumpla los requisitos de este paciente."),
                        "imposible_por_aritmetica": bool(_imp),
                        # En qué peldaño no ha salido. Sin esto, "no sale" no
                        # dice si queda algo que probar o no queda nada.
                        #
                        # ⚠️ Desde el 11 de septiembre es el ÚLTIMO que se
                        # probó, no el primero: ahora se recorre la escalera
                        # entera, así que decir «no sale en estricto» cuando se
                        # han probado los seis sería mandar al veterinario a
                        # bajar un peldaño que ya está probado.
                        "peldano": _peldano_usado_f,
                        "peldanos_probados": [k for _m, _s, k in _escalones_f]}
        # ⚠️ "NO SE PUEDE" A SECAS NO LE SIRVE A NADIE (29 agosto). Cuando no
        # sale, la pregunta del veterinario es "¿es POR LOS ALIMENTOS o por
        # LAS CANTIDADES?", y eso se puede contestar midiéndolo en vez de
        # suponerlo: se reintenta con los mismos alimentos y las cantidades
        # libres. Si así sale, el problema son las cifras, y encima se le
        # puede enseñar una ración que sí cuadra con SUS ingredientes -- para
        # aceptarla o para ver de dónde se ha movido.
        #
        # No se entrega en silencio: va como `alternativa`, aparte del menú,
        # y con `factible: false`. Cambiarle las cantidades por la puerta de
        # atrás sería exactamente lo que este endpoint promete no hacer.
        if not _imp and fijos:
            ok2, gramos2 = resolver_v2(
                datos.der_objetivo, datos.etapa_requisitos, al, req,
                datos.peso_perro_kg, dosis_maxima_fabricante,
                excluidos=excluidos or None,
                margenes_categoria=_margenes_f, max_suplementos=_supl_f, time_limit=12.0,
                forzar=list(fijos) or None,
                patologias=datos.patologias,
                peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
                peso_objetivo_kg=_peso_de_referencia(datos)[0],
                categorias_excluidas=datos.categorias_excluidas)
            if ok2 and isinstance(gramos2, dict) and "_imposible" not in gramos2:
                respuesta_no["motivo"] = (
                    "Con esas cantidades no sale, pero con estos mismos alimentos sí. "
                    "Lo que no cuadra son las cifras, no los ingredientes.")
                respuesta_no["alternativa"] = gramos2
                respuesta_no["cambios_de_la_alternativa"] = {
                    n: {"tuyo": round(g, 1), "propuesto": round(float(gramos2.get(n, 0)), 1)}
                    for n, g in fijos.items()
                    if abs(float(gramos2.get(n, 0)) - g) > 0.5}
            else:
                respuesta_no["motivo"] += (" Tampoco existe con esos alimentos dejando las "
                                           "cantidades libres, así que el problema no son las "
                                           "cifras: es la combinación.")
        return respuesta_no

    # ⚠️ SUS GRAMOS SE COMPRUEBAN, NO SE PROMETEN. El motor los recibe como
    # límites, así que deberían volver iguales; si alguna vez no volvieran,
    # el veterinario tiene que enterarse -- callarlo sería cambiarle la
    # formulación por dentro, que es justo lo que este endpoint promete no
    # hacer.
    movidos = [n for n, g in fijos.items()
               if abs(float(gramos.get(n, 0)) - g) > 0.5]
    if movidos:
        # ⚠️ Y SI SE HAN MOVIDO, NO ES UN SÍ (29 agosto). Esto se detectaba y
        # se devolvía junto al menú, con `factible: true` -- o sea que la
        # promesa de "tus gramos no se tocan" se rompía en una clave que
        # nadie mira, mientras la pantalla enseñaba un menú verde. Es la
        # familia de fallos que persigue este proyecto entero: sin error,
        # sin aviso, y el veterinario creyendo que ha formulado lo que
        # escribió.
        return {"factible": False,
                "motivo": ("No se ha podido formular respetando estas cantidades: " +
                           ", ".join(movidos) + ". Cambia esas cifras o quita el alimento."),
                "gramos_fijos_movidos": movidos,
                "alternativa": gramos}

    # ⚠️ Y SE DICE EN QUÉ PELDAÑO SALIÓ, siempre — no solo cuando hubo que
    # bajar. «No dice nada» y «estricto» se leían igual, y quien firma
    # necesita poder afirmar lo segundo. Es la misma regla que `/menu/v2`.
    respuesta = {"factible": True, "menu": gramos, "gramos_fijos_movidos": movidos,
                 "peldano": _peldano_usado_f,
                 "se_bajo_de_peldano": bool(not datos.peldano
                                            and _peldano_usado_f != PELDANO_ESTRICTO)}
    respuesta = _garantizar_verificado(
        respuesta, datos.der_objetivo, datos.etapa_requisitos, datos.peso_perro_kg,
        origen="formulador del veterinario", patologias=datos.patologias,
        peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
        peso_objetivo_kg=_peso_de_referencia(datos)[0], al=al, req=req)
    if respuesta.get("factible"):
        # El estado completo, para no obligar a la app a pedirlo otra vez
        # justo después: es la misma ración.
        datos_estado = datos.model_copy(update={"gramos_por_alimento": gramos})
        respuesta["estado"] = _estado_de_la_racion(datos_estado)
    return respuesta


# =====================================================================
# LA PAUTA FIRMADA
#
# Lo que se firma es un DOCUMENTO, no "el menú". Y no es una distinción de
# abogado: hoy la tabla `menus` guarda nombre, gramos y kcal, y con eso un
# menú guardado no se puede verificar ni en principio -- falta contra qué:
# no está la etapa, ni el DER, ni las patologías con las que se calculó.
# Por eso `/perro/{id}/menus` marca lo que devuelve como `verificado: False`.
#
# Firmar eso no se puede, porque un documento firmado tiene que seguir
# diciendo lo mismo dentro de un año, y aquí no se queda quieto NADA:
#
#   · La ficha del perro cambia. Caso real de este repo: Lola pesaba 7,0 kg
#     y dos meses después 6,2. Si se firmó a 7,0, el documento dice 7,0.
#   · El catálogo cambia. También real, dos veces en una semana: fuera la
#     borraja el 27 de agosto, fuera cinco suplementos el 26. Un menú
#     firmado que llevara borraja no se puede regenerar hoy.
#   · El motor cambia. El tope de fósforo en renal pasó de 1400 a 1200 el
#     25 de agosto. El mismo menú, verificado antes y después, no da lo
#     mismo.
#
# Así que se congela entero: el menú, la ficha verificada con sus 42 filas,
# el contexto con el que se calculó, los huecos del catálogo y los sellos de
# los datos y del código. Y encima un sello propio, para poder comprobar un
# año después que el papel que alguien enseña es el que se firmó.
# =====================================================================
class Firmante(BaseModel):
    nombre: str
    num_colegiado: str


class PeticionFirmar(BaseModel):
    gramos_por_alimento: dict
    der_objetivo: float
    etapa_requisitos: str = "Adulto"
    peso_perro_kg: Optional[float] = None
    peso_adulto_esperado_kg: Optional[float] = None
    peso_objetivo_kg: Optional[float] = None
    bcs: Optional[float] = None
    patologias: Optional[list] = None
    especies_excluidas: list[str] = []
    nombres_excluidos: Optional[list] = None
    categorias_excluidas: Optional[list] = None
    firmante: Firmante
    # Lo que identifica al paciente EN EL DOCUMENTO. Se copia, no se apunta:
    # la ficha del perro cambia y lo firmado no puede cambiar con ella.
    paciente: dict = {}
    # ⚠️ EL "CÓMO DARLO" VA DENTRO DE LO FIRMADO (29 agosto). Una pauta son
    # los gramos Y qué hacer con ellos: cómo se prepara cada cosa, qué se
    # congela, cómo se hace la transición desde lo que comía. Si eso viviera
    # fuera del documento, el papel firmado diría cantidades y el tutor se
    # quedaría sin las instrucciones -- o peor, con unas que cambiaron
    # después. Lo propone Rawku y lo escribe el veterinario; aquí llega ya
    # como texto suyo y se congela tal cual, sin tocarlo.
    indicaciones: str = ""


def _sello_de(documento):
    """El sello de lo firmado: SHA-256 de la copia canónica, 16 hex.

    Mismo criterio que el sello de los datos en `/verificar`: se hashea el
    CONTENIDO -- json ordenado, sin espacios -- y no el texto, para que
    reordenar una clave o cambiar el formato no dé una falsa alarma y
    cambiar un número sí.

    ⚠️ LO CALCULA LA API, sobre lo que acaba de verificar, nunca el
    frontend sobre lo que pintó. Si lo calculara la pantalla habría dos
    ideas de "lo firmado" -- la del motor y la de la vista -- y el día que
    se separen el sello seguiría cuadrando consigo mismo sin decir nada. Es
    la misma familia de fallo que la duplicación del DER.
    """
    import hashlib, json as _json

    # ⚠️ 5.0 Y 5 SON EL MISMO NÚMERO, Y EL SELLO TIENE QUE VERLO ASÍ.
    #
    # CASO REAL, cazado el 29 de agosto por el script que habla con la API de
    # verdad: se firmaba una pauta, la app la guardaba, y al comprobarla el
    # sello NO cuadraba -- sobre un documento que nadie había tocado.
    #
    # La causa es de las que no se ven leyendo Python: JavaScript no
    # distingue enteros de decimales. `JSON.stringify(5.0)` escribe `5`, así
    # que en cuanto el documento pasa por el navegador -- que es SIEMPRE, es
    # el camino real -- los 300.0 gramos vuelven como 300, y la copia
    # canónica de Python cambia de "300.0" a "300". Mismo número, otro sello.
    #
    # Se normaliza antes de hashear: un decimal cuyo valor es entero se
    # escribe como entero. Es lo único que hacía falta -- para el resto de
    # los números, Python y JavaScript escriben ya la misma representación
    # más corta que redondea de vuelta al mismo valor.
    def _numeros_comparables(v):
        if isinstance(v, bool):
            return v
        if isinstance(v, float) and v.is_integer() and abs(v) < 1e15:
            return int(v)
        if isinstance(v, dict):
            return {k: _numeros_comparables(x) for k, x in v.items()}
        if isinstance(v, (list, tuple)):
            return [_numeros_comparables(x) for x in v]
        return v

    copia = _numeros_comparables({k: v for k, v in documento.items() if k != "sello"})
    canonico = _json.dumps(copia, sort_keys=True, ensure_ascii=False,
                           separators=(",", ":"))
    return hashlib.sha256(canonico.encode("utf-8")).hexdigest()[:16]


@app.post("/pauta/firmar")
def pauta_firmar(datos: PeticionFirmar):
    """Congela y sella una ración para que se pueda firmar.

    ⚠️ NO AUTENTICA, y hay que decirlo en voz alta: esta API no tiene
    puerta todavía (ver VETERINARIOS.md §10). Que quien firma sea un
    profesional acreditado lo garantiza la seguridad por fila de Supabase,
    que es donde se guarda la pauta -- la política solo deja insertar a una
    cuenta con `rol = 'profesional'` y `rol_verificado_en` puesto. Este
    endpoint no da acceso a nada: calcula y sella. El día que una
    prescripción pueda BAJAR un mínimo de FEDIAF (fase 4), eso deja de
    bastar y hay que validar el JWT aquí.
    """
    observabilidad.etiquetar(endpoint="/pauta/firmar", etapa=datos.etapa_requisitos)
    al, req = cargar_v2()
    gramos = {n: float(g) for n, g in (datos.gramos_por_alimento or {}).items()
              if _num_positivo(g)}
    if not gramos:
        raise HTTPException(400, "No hay ninguna ración que firmar.")
    desconocidos = [n for n in gramos if n not in al]
    if desconocidos:
        raise HTTPException(400, "No tenemos datos de: " + ", ".join(desconocidos))

    peso_ref, origen_peso = _peso_de_referencia(datos)
    ficha = verificar_v2(gramos, al, req, datos.der_objetivo, datos.etapa_requisitos,
                         peso_referencia_kg=peso_ref)
    problemas = _seguridad_completa(gramos, al, datos.der_objetivo, datos.etapa_requisitos,
                                    datos.patologias, peso_perro_kg=datos.peso_perro_kg)
    topes_rotos = _tope_patologia_roto(
        gramos, al, datos.patologias, datos.etapa_requisitos, req=req,
        der_efectiva=der_efectiva_de(datos.der_objetivo, peso_ref),
        peso_adulto_esperado_kg=getattr(datos, "peso_adulto_esperado_kg", None))

    # ⚠️ NO SE FIRMA LO QUE NO ESTÁ VERDE. Es la regla 1 leída donde más
    # importa: "ningún menú sale sin verificar, y si no está verde no se
    # entrega". Una pauta firmada es la forma más difícil de retirar que
    # tiene un menú de salir de aquí.
    #
    # Un profesional colegiado SÍ puede pautar por debajo de FEDIAF -- una
    # dieta renal de verdad baja el fósforo por debajo del mínimo de un
    # perro sano --, y para eso está la fase 4: una prescripción declarada,
    # que viaja con el menú y contra la que se verifica. Hasta que exista,
    # decir que no es más honesto que firmar un rojo sin dejar constancia de
    # contra qué se comprobó.
    if ficha.get("semaforo") != "verde" or topes_rotos:
        return {
            "factible": False,
            "motivo": ("Esta ración todavía no cumple todo lo que hay que cumplir, así que "
                       "no se puede firmar. Lo que falta está en la ficha, nutriente a "
                       "nutriente."),
            "semaforo": ficha.get("semaforo"),
            "faltan": ficha.get("faltan"),
            "se_pasa": ficha.get("se_pasa"),
            "topes_de_patologia_rotos": topes_rotos,
        }

    kcal = sum((al[n].get("energia", 0) or 0) / 100.0 * g for n, g in gramos.items())
    documento = {
        # La versión del documento, para poder leer mañana lo firmado hoy.
        "version": 1,
        "firmante": {"nombre": datos.firmante.nombre,
                     "num_colegiado": datos.firmante.num_colegiado},
        # ⚠️ Import local a propósito: en este archivo hay un `import
        # datetime` de módulo (línea ~514) que gana sobre cualquier
        # `from datetime import datetime` de arriba, y `datetime.now` no
        # existe en el módulo. Se pide la clase con su nombre y no se toca
        # el import de nadie.
        "firmada_en": _fecha_utc_ahora(),
        "paciente": datos.paciente or {},
        "indicaciones": datos.indicaciones or "",
        "menu": {n: round(g, 1) for n, g in gramos.items()},
        "ficha_verificada": ficha,
        "contexto": {
            "etapa_requisitos": datos.etapa_requisitos,
            "der_objetivo": datos.der_objetivo,
            "kcal_reales": round(kcal, 1),
            "gramos_total": round(sum(gramos.values()), 1),
            "peso_perro_kg": datos.peso_perro_kg,
            "peso_objetivo_kg": datos.peso_objetivo_kg,
            "peso_de_referencia_kg": peso_ref,
            "de_donde_sale_el_peso": origen_peso,
            "bcs": datos.bcs,
            "patologias": list(datos.patologias or []),
            "especies_excluidas": list(datos.especies_excluidas or []),
            "nombres_excluidos": list(datos.nombres_excluidos or []),
            "categorias_excluidas": list(datos.categorias_excluidas or []),
        },
        # ⚠️ LOS HUECOS VAN EN EL DOCUMENTO, no solo en pantalla. Si la
        # ración se calculó con alimentos a los que les falta un dato, o con
        # alguno de los valores que no nos creemos, eso sale impreso. Es
        # incómodo y es exactamente por eso: lo contrario es firmar sobre
        # datos incompletos sin que conste en ninguna parte.
        "huecos": {
            "sin_dato": ficha.get("datos_incompletos") or {},
            "dato_dudoso": ficha.get("datos_dudosos") or {},
            "no_verificable": ficha.get("no_verificable") or [],
            # Con el nombre de cada nutriente y a qué alimento le falta: un
            # documento firmado tiene que poder leerse dentro de un año sin
            # tener delante el diccionario de claves del catálogo.
            "en_cristiano": _huecos_en_cristiano(ficha),
        },
        "seguridad": problemas,
        "sellos": {**SELLOS_DE_LOS_DATOS,
                   "main.py": _sello_de_main_py()},
    }
    documento["sello"] = _sello_de(documento)
    return {"factible": True, "documento": documento}


@app.post("/pauta/comprobar")
def pauta_comprobar(documento: dict):
    """¿Este papel es el que se firmó?

    Se recalcula el sello sobre lo que llega y se compara con el que trae.
    Sirve un año después, con el catálogo y el motor ya cambiados, porque no
    vuelve a calcular la ración: comprueba el documento consigo mismo."""
    esperado = documento.get("sello")
    if not esperado:
        raise HTTPException(400, "Este documento no lleva sello.")
    real = _sello_de(documento)
    return {
        "coincide": real == esperado,
        "sello_del_documento": esperado,
        "sello_recalculado": real,
        "explicacion": ("El documento es exactamente el que se firmó."
                        if real == esperado else
                        "Este documento NO es el que se firmó: algo ha cambiado desde entonces."),
    }


# =====================================================================
# QUE UN VETERINARIO PUEDA VER QUE CAMBIA CADA PATOLOGIA
#
# ⚠️ PEDIDO EXPRESO (7 septiembre): "cuando pones una patologia te deberia
# dar una cuando estas como veterinario? Te deberia salir algo sobre esa
# patologia? Que cambia que no, que puedes modificar y que no, de que
# margen puede salir".
#
# Hoy el veterinario marca "Insuficiencia renal cronica" y lo unico que ve
# es una casilla azul. El motor, por dentro, le pone un tope de 1200 mg de
# fosforo por 1000 kcal, y ese numero -- con su fuente, su motivo y lo cerca
# que queda del minimo de FEDIAF (1160) -- es exactamente lo que decide si
# el menu sale o no sale. Quien FIRMA una pauta tiene derecho a leerlo antes
# de firmarla; es la fase 1 de VETERINARIOS.md ("ver mas, no poder mas").
#
# POR QUE UN ENDPOINT Y NO UNA TABLA EN LA APP. Porque seria la tercera copia
# de los mismos numeros (patologias.json, el solver, y la app), y de esas
# copias ya sabemos como acaban: es la duplicacion del DER, y es la tabla de
# patologias desincronizada que arrastraba el POST /menu que se borro el 26
# de agosto -- fosforo renal a 1.400 en vez de 1.200 durante semanas, sin
# que nadie lo viera. Aqui se sirve lo que el solver aplica de verdad, leido
# del mismo archivo, y la app solo lo pinta.
#
# El MARGEN (que es lo que ella pregunta con "de que margen puede salir") no
# se puede leer de ningun sitio de un vistazo: es la distancia entre el tope
# de la patologia y el minimo de FEDIAF del mismo nutriente. Cuando esa
# distancia es estrecha -- renal: 1200 contra 1160, un 3,4 % -- el menu casi
# no tiene sitio donde moverse, y saberlo ANTES de formular es la diferencia
# entre entender por que no sale menu y creer que la app esta rota.
# =====================================================================

# =====================================================================
# GET /vocabulario — TODO LO QUE EL MOTOR ENUMERA, PARA QUE LA APP LO REFLEJE
# =====================================================================
#
# ⚠️ POR QUE EXISTE (11 de septiembre de 2026). Elena, despues de encontrar que
# la app ofrecia cinco niveles de actividad y la base de datos guardaba tres:
#
#     «no hay que hacer que el motor coincida con lo de la app. hay que hacer
#      que la app coincida con lo del motor [...] si el motor dice que hay
#      dieciocho niveles de actividad, la app tiene que tener 18 niveles de
#      actividad porque si no no sirve de nada, y asi con todo»
#
# Y tiene razon en la direccion: la FUENTE manda, el MOTOR la implementa y la
# APP la ofrece. Cuando la app se copia una lista a mano, esa copia se
# desincroniza y nadie se entera -- ya paso tres veces documentadas:
#
#   · `CATEGORIAS_QUE_ELIGE_EL_USUARIO` contra `CATEGORIAS` de App.jsx: durante
#     tres semanas se respetaban tres de las seis, y 15 de cada 36 menus
#     personalizados metian algo que nadie habia pedido, callando.
#   · Las patologias: el motor tiene 47 y la app ofrece 37. Diez no se pueden
#     marcar, siete de ellas formulables (`FRONTEND_VS_MOTOR.md` §1).
#   · Los niveles de actividad: cinco en la pantalla, tres en la base de datos.
#     Un perro de trabajo volvia como «normal» y recibia un 37 % menos de comida.
#
# LA IDEA: que la app deje de copiar y LEA. Este endpoint sirve las siete listas
# que el motor enumera, cada una con lo que hace falta para pintarla. El que la
# app siga teniendo su copia es ahora comprobable: `tests/vocabulario.spec.js`
# en `canislab-web` compara las dos.
#
# NO sustituye a `GET /patologias` ni a `GET /relajacion`, que sirven la tabla
# ENTERA con sus cifras y sus fuentes. Esto es el vocabulario: los nombres y
# cuantos hay.

# =====================================================================
# LAS DOS FORMAS DE DECIR LO MISMO: AL DUEÑO Y AL VETERINARIO
# =====================================================================
#
# ⚠️ POR QUE VIVEN AQUI Y NO EN LA APP (11 de septiembre de 2026). Elena:
#
#     «aunque coja los datos directos del motor, el vocabulario que usa la app
#      en modo usuario tiene que ser entendible para el usuario y el que se usa
#      en modo veterinario tiene que ser mas tecnico»
#
# Y tiene razon en las dos mitades. Lo que NO puede pasar es que esas etiquetas
# vivan copiadas en la app: el dia que el motor anada un nivel -- o que la fuente
# parta uno en dos -- la app se queda con su lista vieja y el usuario elige algo
# que el motor no sabe recibir, o al reves. Es el mismo fallo que ya tuvimos con
# las categorias y con las patologias, y el que acabamos de encontrar con los
# cinco niveles contra los tres de la base de datos.
#
# Asi que la CLAVE y las DOS etiquetas salen del mismo sitio: de aqui.
#
#   · `dueno`       — como se lo decimos a quien quiere alimentar bien a su
#                     perro. Sin jerga y con un ejemplo de lo que hace el perro.
#   · `veterinario` — la fila de la fuente, con sus palabras y sus horas. Quien
#                     firma una pauta necesita poder citar la tabla.
ETIQUETAS_ACTIVIDAD = {
    "sedentario": {
        "dueno": {"titulo": "Sedentario", "detalle": "Paseos cortos, se mueve poco"},
        "veterinario": {"titulo": "Actividad baja",
                        "detalle": "Menos de 1 h/día, p. ej. paseo con correa (FEDIAF VII-7)"},
    },
    "normal": {
        "dueno": {"titulo": "Normal", "detalle": "Paseos diarios de siempre"},
        "veterinario": {"titulo": "Actividad moderada, bajo impacto",
                        "detalle": "1 a 3 h/día de bajo impacto (FEDIAF VII-7)"},
    },
    "activo": {
        "dueno": {"titulo": "Activo", "detalle": "Paseos largos, juega bastante"},
        "veterinario": {"titulo": "Actividad moderada, alto impacto",
                        "detalle": "1 a 3 h/día de alto impacto (FEDIAF VII-7)"},
    },
    # ⚠️ LOS DOS DE ABAJO SON LA MISMA FILA DE LA FUENTE, y el vocabulario del
    # veterinario tiene que decirlo: FEDIAF da «High activity (3 – 6 h/day)
    # (working dogs, e.g. sheep dogs) 150 - 175» en UNA sola fila con un rango, y
    # el motor la parte en dos. Al dueño se le dan dos casillas porque son dos
    # perros distintos de reconocer; a quien firma se le dice de qué fila salen
    # y en qué punto del rango cae. Escrito en `niveles_de_actividad.json`.
    "muy_activo": {
        "dueno": {"titulo": "Muy activo", "detalle": "Corre, hace deporte, no para"},
        "veterinario": {"titulo": "Actividad alta (extremo bajo del rango)",
                        "detalle": "3 a 6 h/día; FEDIAF VII-7 da 150-175 en una sola fila y aquí "
                                   "se aplica 150"},
    },
    "trabajo": {
        "dueno": {"titulo": "Trabajo", "detalle": "Pastoreo, guarda, o similar"},
        "veterinario": {"titulo": "Actividad alta (extremo alto del rango)",
                        "detalle": "3 a 6 h/día, perro de trabajo; FEDIAF VII-7 da 150-175 en una "
                                   "sola fila y aquí se aplica 175"},
    },
}

# ─────────────────────────────────────────────────────────────────────────────
# LOS DOS REGISTROS, PARA TODO LO DEMAS (11 de septiembre de 2026)
#
# Elena, el mismo dia que lo de la actividad: «esto tiene que ser para TODO,
# razas, tamaño, etapa, actividad, preguntas para las patologias de
# veterinarios, todo».
#
# Asi que lo que se hizo con los cinco niveles de actividad se hace aqui con lo
# demas que la ficha ENUMERA. La regla es la misma y no cambia:
#
#   · `dueno`       — sin jerga, con un ejemplo de lo que se ve o se toca.
#   · `veterinario` — la palabra de la fuente, con su tabla y su cifra.
#
# Lo que NO se duplica: el numero. Los escalones del dueño son los MISMOS
# valores de BCS que usa el veterinario (1, 3, 5, 7 y 9); si cada pantalla
# tuviera su escala, el mismo perro tendria dos pesos objetivo y dos DER segun
# quien abriera la ficha. Eso ya esta resuelto en `der.BCS_DESDE_CONDICION` y
# aqui solo se ETIQUETA.
# Las 255 razas y los seis tamaños, de `razas.json`. Se cargan una vez al
# arrancar, como el catalogo: son datos, no calculo.
import json as _json
import os as _os
from razas import RAZAS as _RAZAS, TAMANOS as _TAMANOS, cargar_crudo as _cargar_razas
from der import BCS_DESDE_CONDICION, BCS_PCT_POR_PUNTO as der_BCS_PCT_POR_PUNTO

_RAZAS_META = _cargar_razas().get("_meta", {})

# Quien puede marcar cada patologia y que pregunta falta en la ficha. Se lee del
# fichero y no se copia aqui: seria la segunda copia de una tabla que ya tiene
# su auditor (BLOQUE 79).
with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                        "quien_formula_cada_patologia.json"), encoding="utf-8") as _f:
    _DERIVACION = _json.load(_f)["patologias"]

# Que pregunta decide la cifra de cada patologia, que respuestas tiene, y a que
# clave del motor lleva cada respuesta.
#
# ⚠️ Elena, 11-sep-2026: «tendra que haber preguntas para cada patologia
# preguntando resultados de analiticas o lo que sea para que pueda coger segun
# la respuesta los limites para cada estadio o cada caso». Aqui no hay ni una
# cifra escrita: el fichero las DERIVA de `patologias.json`, y donde el motor no
# tiene una clave por respuesta lo dice en vez de inventarla.
with open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                        "preguntas_por_patologia.json"), encoding="utf-8") as _f:
    _PREGUNTAS_PAT = _json.load(_f)


def _rango_de_tamano(tamano):
    """El rango de peso adulto que de verdad tienen las razas de ese tamaño.

    Se MIDE sobre `razas.json` en vez de escribirse: los seis tamaños se
    solapan (Pequeño llega a 18,5 kg de peso medio y Mediano empieza en 15) y
    un corte escrito a mano seria un numero que la tabla no dice.
    """
    medios = [r["pesoMedio"] for r in _RAZAS if r["tamano"] == tamano]
    if not medios:
        return None
    propias = [r for r in _RAZAS if r["tamano"] == tamano]
    return {"peso_medio_min": min(medios), "peso_medio_max": max(medios),
            # ⚠️ Y EL RANGO ANCHO, que es el que hay que ENSEÑAR a quien elige
            # tamaño sin saber la raza: va del perro mas ligero de la raza mas
            # ligera al mas pesado de la mas pesada. La app lo tenia escrito a
            # mano («Toy: 1,5-6kg») y cuatro de los seis ya estaban caducados,
            # porque la lista de razas creció debajo y la tabla no.
            "peso_min": min(r["pesoMin"] for r in propias),
            "peso_max": max(r["pesoMax"] for r in propias),
            "cuantas_razas": len(medios)}


def _etiqueta_tamano(tamano):
    """Las dos etiquetas de un tamaño, con el detalle clinico ya relleno."""
    import copy
    e = copy.deepcopy(ETIQUETAS_TAMANO[tamano])
    rango = _rango_de_tamano(tamano)
    if rango and e.get("veterinario") is not None:
        e["veterinario"]["detalle"] = (
            f"{rango['cuantas_razas']} razas del catalogo, de {rango['peso_medio_min']} a "
            f"{rango['peso_medio_max']} kg de peso adulto medio")
    return e


ETIQUETAS_CONDICION = {
    1: {"dueno": {"titulo": "Muy flaquito", "detalle": "Costillas muy marcadas, sin nada de grasa"},
        "veterinario": {"titulo": "BCS 1/9 — Emaciado",
                        "detalle": "≥40 % por debajo del ideal (FEDIAF Tabla VII-2)"}},
    2: {"dueno": None,
        "veterinario": {"titulo": "BCS 2/9 — Muy delgado",
                        "detalle": "30 a 40 % por debajo del ideal (FEDIAF Tabla VII-2)"}},
    3: {"dueno": {"titulo": "Flaquito", "detalle": "Costillas se notan facil al tacto"},
        "veterinario": {"titulo": "BCS 3/9 — Delgado",
                        "detalle": "20 a 30 % por debajo del ideal (FEDIAF Tabla VII-2)"}},
    4: {"dueno": None,
        "veterinario": {"titulo": "BCS 4/9 — Por debajo del ideal",
                        "detalle": "10 a 15 % por debajo del ideal (FEDIAF Tabla VII-2)"}},
    5: {"dueno": {"titulo": "Ideal", "detalle": "Costillas se palpan, cintura visible desde arriba"},
        "veterinario": {"titulo": "BCS 5/9 — Ideal",
                        "detalle": "En su peso; la racion se calcula sobre el peso actual"}},
    6: {"dueno": None,
        "veterinario": {"titulo": "BCS 6/9 — Por encima del ideal",
                        "detalle": "10 a 15 % por encima del ideal (FEDIAF Tabla VII-2)"}},
    7: {"dueno": {"titulo": "Rellenito", "detalle": "Cuesta notar las costillas, poca cintura"},
        "veterinario": {"titulo": "BCS 7/9 — Sobrepeso",
                        "detalle": "20 a 30 % por encima del ideal (FEDIAF Tabla VII-2)"}},
    8: {"dueno": None,
        "veterinario": {"titulo": "BCS 8/9 — Obeso",
                        "detalle": "30 a 45 % por encima del ideal (FEDIAF Tabla VII-2)"}},
    9: {"dueno": {"titulo": "Muy gordete", "detalle": "No se notan las costillas, sin cintura"},
        "veterinario": {"titulo": "BCS 9/9 — Obesidad morbida",
                        "detalle": "Mas del 45 % por encima del ideal; la estimacion es una COTA "
                                   "INFERIOR (FEDIAF Tabla VII-2, fila «9. Grossly Obese»)"}},
}

# Los seis tamaños. La cifra de referencia de cada uno NO se inventa aqui: es el
# peso con el que esta calculado su menu de la vista previa en
# `catalogo_menus.json`, o sea el que el motor ya usa.
ETIQUETAS_TAMANO = {
    "Toy":     {"dueno": {"titulo": "Toy", "detalle": "Cabe en brazos"},
                "veterinario": {"titulo": "Toy", "detalle": None}},
    "Mini":    {"dueno": {"titulo": "Mini", "detalle": "Pequeñito, de bolso"},
                "veterinario": {"titulo": "Miniatura", "detalle": None}},
    "Pequeño": {"dueno": {"titulo": "Pequeño", "detalle": "Se coge en brazos sin esfuerzo"},
                "veterinario": {"titulo": "Pequeño", "detalle": None}},
    "Mediano": {"dueno": {"titulo": "Mediano", "detalle": "Ni pequeño ni grande"},
                "veterinario": {"titulo": "Mediano", "detalle": None}},
    "Grande":  {"dueno": {"titulo": "Grande", "detalle": "Cuesta cogerlo en brazos"},
                "veterinario": {"titulo": "Grande", "detalle": None}},
    "Gigante": {"dueno": {"titulo": "Gigante", "detalle": "De los mas grandes que hay"},
                "veterinario": {"titulo": "Gigante", "detalle": None}},
}
# ⚠️ EL `detalle` DEL VETERINARIO VA A None A PROPOSITO Y LO RELLENA EL
# ENDPOINT, con el rango que de verdad tienen las razas de ese tamaño en
# `razas.json` y con el peso con el que esta calculado su menu de la vista
# previa. La primera version de esto llevaba los kilos escritos a mano («8 a 15
# kg» para Pequeño) y eran FALSOS: medido sobre las 255 razas, Pequeño llega a
# 18,5 kg de peso medio y Mediano empieza en 15, o sea que los tamaños se
# SOLAPAN -- son etiquetas de raza, no cortes de peso. Escribir un corte que la
# tabla no tiene es inventarse un dato con forma de dato bueno, que es justo lo
# que este fichero viene a evitar.

# Las etapas, que es lo unico de esta lista que NO elige quien rellena la ficha:
# sale de la fecha de nacimiento, del sexo y de si esta gestante o lactando. Se
# sirven igual porque la app las ESCRIBE en pantalla y porque el veterinario
# necesita saber a que tabla de FEDIAF corresponde la suya.
ETIQUETAS_ETAPA = {
    "CachorroJoven": {
        "dueno": {"titulo": "Cachorro", "detalle": "Menos de 14 semanas"},
        "veterinario": {"titulo": "Early Growth (< 14 weeks) & Reproduction",
                        "detalle": "Tabla III-3b de FEDIAF, tercera columna. Es TAMBIEN la de "
                                   "gestacion y lactancia: la cabecera dice «& Reproduction»"}},
    "CachorroCrecimiento": {
        "dueno": {"titulo": "Cachorro mayor", "detalle": "Desde las 14 semanas hasta que termina "
                                                         "de crecer"},
        "veterinario": {"titulo": "Late Growth (≥ 14 weeks)",
                        "detalle": "Tabla III-3b de FEDIAF, cuarta columna"}},
    "Adulto": {
        "dueno": {"titulo": "Adulto", "detalle": "Ya ha terminado de crecer"},
        "veterinario": {"titulo": "Adult maintenance",
                        "detalle": "Tabla III-3b de FEDIAF, columnas de 95 y 110 kcal/kg^0,75"}},
    "Senior": {
        "dueno": {"titulo": "Senior", "detalle": "Perro mayor"},
        "veterinario": {"titulo": "Senior (sin columna propia en FEDIAF)",
                        "detalle": "Usa la de adulto, con la proteina subida a 45 g/1000 kcal "
                                   "(`requisitos.SENIOR_PROTEINA_MINIMA`) y el techo de fosforo "
                                   "de 1750 mg/1000 kcal"}},
    "GestanteTardia": {
        "dueno": {"titulo": "Embarazada", "detalle": "Ultimas semanas de la gestacion"},
        "veterinario": {"titulo": "Late gestation",
                        "detalle": "Va a la columna «Early Growth & Reproduction», mas el "
                                   "requisito condicional de proteina de "
                                   "`requisitos_condicionales.json`"}},
    "Lactante": {
        "dueno": {"titulo": "Dando de mamar", "detalle": "Con la camada"},
        "veterinario": {"titulo": "Lactation",
                        "detalle": "Va a la columna «Early Growth & Reproduction», mas el "
                                   "requisito condicional de proteina"}},
}
# ⚠️ LA ETAPA NO LA CALCULA EL MOTOR, Y ESO HAY QUE SABERLO PARA LEER ESTO.
# La decide la app a partir de la fecha de nacimiento (`determinarEtapa` en
# `src/der.js`, que corta Early Growth en 98 dias = 14 semanas) y llega ya hecha
# en `etapa_requisitos`. O sea que el motor no puede comprobar que la etapa que
# recibe sea la que le toca a ese perro: solo que EXISTA. Es la misma
# duplicacion que el DER, y esta apuntada igual.

@app.get("/vocabulario")
def endpoint_vocabulario():
    from der import BASE_ACTIVIDAD, RAZAS_CIFRA_FEDIAF
    from requisitos import ETAPAS_VALIDAS, EQUIVALENCIA_ETAPAS

    from motor.patologias import cargar_crudo
    from catalogo_menus import CATALOGO

    al_v, _req_v = cargar_v2()
    _pat_v = (cargar_crudo() or {}).get("patologias") or {}

    return {
        "que_es": ("Todo lo que el motor enumera. La app tiene que ofrecer ESTO, ni mas ni menos: "
                   "una lista que la app se copia a mano se desincroniza y nadie se entera."),
        "niveles_de_actividad": {
            "de_donde": "FEDIAF 2025, Tabla VII-7 «Recommendations for DER in relation to activity»",
            "cuantos": len(BASE_ACTIVIDAD),
            "niveles": [dict({"clave": k, "kcal_kg075": v}, **ETIQUETAS_ACTIVIDAD[k])
                        for k, v in BASE_ACTIVIDAD.items()],
            "ojo": ("⚠️ La Tabla VII-7 tiene CUATRO filas de actividad para el perro normal (95, "
                    "110, 125 y un rango de 150-175), y el motor parte la cuarta en DOS niveles. "
                    "Eso es decision nuestra y esta escrita en `niveles_de_actividad.json`. "
                    "Y falta una fila de la fuente que no esta ni aqui ni en la app: «Obese prone "
                    "adults ≤ 90»."),
        },
        # ── LAS 255 RAZAS ────────────────────────────────────────────────
        # Vivian SOLO en `src/App.jsx`. Ahora viven en `razas.json` y la app se
        # las pide aqui: una lista que la app se copia a mano se desincroniza y
        # nadie se entera. ⚠️ Estas cifras NO tienen fuente publicada -- ninguna
        # de las cuatro fuentes del motor trae una tabla de peso por raza --, y
        # eso esta escrito en el `_meta` del fichero y en `DATOS_QUE_FALTAN.md`.
        "razas": {
            "de_donde": "razas.json (movidas desde src/App.jsx el 11-sep-2026)",
            "ojo": _RAZAS_META.get("de_donde_salen_estas_cifras"),
            "cuantas": len(_RAZAS),
            "razas": _RAZAS,
        },
        # ── LOS SEIS TAMAÑOS ─────────────────────────────────────────────
        "tamanos": {
            "de_donde": ("Las seis claves con las que `catalogo_menus.json` indexa sus menus "
                         "precalculados (`{tamano}_{etapa}`). Si la app mandara un septimo, la "
                         "clave no existiria y la vista previa se quedaria sin menu."),
            "ojo": ("Son etiquetas de RAZA, no cortes de peso: medido sobre las 255 razas, "
                    "«Pequeño» llega a 18,5 kg de peso medio y «Mediano» empieza en 15. Se "
                    "solapan a proposito. El rango que se sirve aqui es el OBSERVADO en "
                    "`razas.json`, no un corte inventado."),
            "tamanos": [dict({"clave": t,
                              "peso_kg_del_menu_de_muestra": (
                                  CATALOGO.get(f"{t}_Adulto") or {}).get("peso_kg"),
                              "rango_observado_kg": _rango_de_tamano(t)},
                             **_etiqueta_tamano(t))
                        for t in _TAMANOS],
        },
        # ── LA CONDICION CORPORAL ────────────────────────────────────────
        # Es UN SOLO numero y UNA SOLA formula: los cinco escalones del dueño
        # son cinco valores del BCS (1, 3, 5, 7 y 9). Si cada pantalla tuviera
        # su escala, el mismo perro tendria dos pesos objetivo y dos DER.
        "condicion_corporal": {
            "de_donde": "FEDIAF 2025, Anexo 7.1, Tabla VII-2 («% BW below or above BCS 5»)",
            "escala": "1 a 9",
            "ideal": BCS_NEUTRO_MAIN,
            "pct_por_punto": der_BCS_PCT_POR_PUNTO,
            "ojo": ("El BCS 9 NO sigue la recta del 10 % por punto: FEDIAF dice «>45 %» y la "
                    "recta da 40. Se aplica 45 y la estimacion es una COTA INFERIOR. || Los "
                    "cinco escalones del dueño son los BCS de `der.BCS_DESDE_CONDICION`; el "
                    "veterinario pone el BCS exacto, que es el que manda para calcular."),
            "escalones_del_dueno": {str(i): b for i, b in sorted(BCS_DESDE_CONDICION.items())},
            "puntos": [dict({"bcs": b,
                             "ofrecido_al_dueno": b in set(BCS_DESDE_CONDICION.values())},
                            **ETIQUETAS_CONDICION[b])
                       for b in sorted(ETIQUETAS_CONDICION)],
        },
        # ── LAS PREGUNTAS QUE LA APP TIENE QUE HACER ─────────────────────
        # ⚠️ Elena, 11-sep-2026: «preguntas para las patologias de
        # veterinarios». No es opinion de producto: cada linea sale de la CITA
        # de la fuente de esa patologia. Si su tabla condiciona la cifra a un
        # dato clinico -- el estadio IRIS que decide el techo de fosforo, los
        # trigliceridos que bajan la grasa de 37,5 a 25 --, entonces no la puede
        # marcar quien no tiene ese dato, y la pregunta que falta en la ficha es
        # la que hace falta para ELEGIR EL NUMERO.
        "preguntas_por_patologia": {
            "de_donde": "quien_formula_cada_patologia.json",
            "ojo": ("`quien_puede_marcarla` dice quien puede tocar la casilla; "
                    "`pregunta_que_falta` es lo que la app NO pregunta todavia y sin lo cual la "
                    "cifra se elige a ciegas. Una patologia con pregunta sin hacer no deberia "
                    "poder marcarse desde la app del dueño."),
            "cuantas_sin_preguntar": sum(1 for v in _DERIVACION.values()
                                         if v.get("pregunta_que_falta")),
            # ⚠️ Y LO QUE DECIDE CADA RESPUESTA, que es la otra mitad
            # (11-sep). Saber que falta una pregunta no sirve de nada si no se
            # sabe a que cifra lleva cada respuesta. Las cifras se LEEN de
            # `patologias.json`: aqui no hay copia.
            "que_decide_cada_respuesta": _PREGUNTAS_PAT["preguntas"],
            "como_leerlo": _PREGUNTAS_PAT["_meta"]["los_cinco_estados"],
            "por_patologia": {k: {"nombre": v.get("nombre"),
                                  "quien_puede_marcarla": v.get("quien_puede_marcarla"),
                                  "necesita_dato_clinico": v.get("necesita_dato_clinico"),
                                  "que_dato": v.get("que_dato"),
                                  "pregunta_que_falta": v.get("pregunta_que_falta")}
                              for k, v in sorted(_DERIVACION.items())},
        },
        "razas_con_cifra_propia": {
            "de_donde": "FEDIAF 2025, Tabla VII-7, fila «Breed specific differences»",
            "ojo": "La cifra de raza va EN VEZ del nivel de actividad, no sumada (§7.2.3.4).",
            "razas": [{"nombre": k, "kcal_kg075": v[0], "rango": [v[1], v[2]]}
                      for k, v in RAZAS_CIFRA_FEDIAF.items()],
        },
        "etapas": {
            "de_donde": "requerimientos_v2_final.json (Tabla III-3b de FEDIAF) y sus equivalencias",
            "con_tabla_propia": sorted(ETAPAS_VALIDAS),
            "equivalencias": {k: v for k, v in EQUIVALENCIA_ETAPAS.items()},
            # ⚠️ La etapa NO la calcula el motor: la decide la app desde la
            # fecha de nacimiento y llega ya hecha en `etapa_requisitos`. El
            # motor solo puede comprobar que EXISTA. Misma duplicacion que el
            # DER, y apuntada igual.
            "quien_la_calcula": ("La app (`determinarEtapa` en src/der.js), que corta Early "
                                 "Growth en 98 dias = 14 semanas. El motor la recibe hecha."),
            "etapas": [dict({"clave": k}, **v) for k, v in ETIQUETAS_ETAPA.items()],
        },
        "patologias": {
            "cuantas": len(_pat_v),
            "formulables": sorted(k for k, v in _pat_v.items() if v.get("formulable")),
            "no_formulables": sorted(k for k, v in _pat_v.items() if not v.get("formulable")),
            "ojo": ("La tabla entera, con sus topes y sus fuentes, va por `GET /patologias`. "
                    "Quien puede marcar cada una esta en `quien_formula_cada_patologia.json`."),
        },
        "categorias_que_elige_el_usuario": {
            "de_donde": "main.CATEGORIAS_QUE_ELIGE_EL_USUARIO",
            "ojo": ("Tiene que coincidir con `CATEGORIAS` de App.jsx. El dia que dejen de "
                    "coincidir, elegir en las que sobran no hara nada y el menu saldra verde "
                    "igual."),
            "categorias": list(CATEGORIAS_QUE_ELIGE_EL_USUARIO),
        },
        "categorias_del_catalogo": {
            "ojo": ("Las que NO estan en la lista de arriba (Suplementos y Extras) van siempre "
                    "libres: son la herramienta con la que el motor cierra los 43 requisitos."),
            "categorias": sorted({a.get("categoria") for a in al_v.values() if a.get("categoria")}),
        },
        "peldanos_de_la_escalera": {
            "de_donde": "main.PELDANOS_EN_CRISTIANO, y los recorre `_escalera_de_relajacion`",
            "ojo": "Lo que suelta cada uno va por `GET /relajacion`.",
            "peldanos": list(PELDANOS_EN_CRISTIANO),
        },
    }

@app.get("/patologias")
def listar_patologias():
    """Los topes por patologia con su fuente, su motivo y su margen.

    Solo lectura y sin datos de nadie: es la tabla, no un paciente. No pide
    acreditacion por eso mismo -- lo que exige acreditacion es FORMULAR por
    debajo de FEDIAF (ver `_es_profesional_acreditado`), no leer el numero
    que ya viaja dentro de cada menu.
    """
    from motor.patologias import cargar_crudo
    from motor.verificar import MAPA, maximo_de
    from requisitos import cargar_requerimientos

    reqs = cargar_requerimientos()
    # De la clave interna del nutriente ("fosforo") a su fila de FEDIAF.
    # Se recorre MAPA y no los nombres a mano por lo de siempre: MAPA es LA
    # lista de requisitos, y una copia se separa.
    por_clave = {}
    for fila in reqs:
        clave = MAPA.get(fila.get("nutriente"))
        if clave:
            por_clave[clave] = fila

    def _num(v):
        try:
            n = float(v)
            return n if n == n else None
        except (TypeError, ValueError):
            return None

    def _limites_fediaf(clave):
        """Minimo y maximo de FEDIAF en adulto, para poder dar el margen.

        Adulto y no la etapa del paciente a proposito: esto es la ficha de la
        PATOLOGIA, no la de un perro. La etapa la aplica el solver cuando
        formula, y las patologias con `solo_en_adulto` ni siquiera llegan a
        crecimiento.
        """
        fila = por_clave.get(clave)
        if not fila:
            return None, None, None
        return (_num(fila.get("minAdulto")),
                maximo_de(fila, fila.get("nutriente"), "Adulto"),
                fila.get("unidad"))

    def _limites(bloque, es_tope):
        salida = []
        for clave, t in (bloque or {}).items():
            valor = _num(t.get("valor"))
            minimo, maximo, unidad = _limites_fediaf(clave)
            margen = None
            if valor is not None:
                # Un tope aprieta desde arriba: el hueco es lo que queda por
                # encima del minimo de FEDIAF. Un suelo aprieta desde abajo:
                # el hueco es lo que queda por debajo del maximo.
                referencia = minimo if es_tope else maximo
                if referencia:
                    margen = round((valor - referencia) / referencia * 100, 1)
            salida.append({
                "nutriente": clave,
                "unidad": unidad,
                "valor": valor,
                "minimo_fediaf_adulto": minimo,
                "maximo_fediaf_adulto": maximo,
                # Porcentaje de holgura contra el limite de FEDIAF que le
                # queda enfrente. Negativo = por debajo del minimo, o sea una
                # dieta de prescripcion: eso solo lo firma un profesional.
                "margen_pct": margen,
                # ⚠️ AÑADIDO (10 septiembre) — HASTA DONDE PUEDE MOVERLA EL
                # PROFESIONAL, Y HASTA DONDE NO. `margen_pct` de arriba dice
                # cuanta holgura hay contra UN limite de FEDIAF; esto dice la
                # ventana entera con su procedencia: el suelo (bajo el cual hace
                # falta firma), el techo (que puede ser LEGAL, y entonces no se
                # sale nadie) y de donde sale cada uno. Vive en el fichero y no
                # se calcula aqui a proposito: si la app o esta funcion lo
                # recalcularan por su cuenta, seria la tercera copia de la misma
                # tabla -- que es exactamente como se desincronizo la del
                # POST /menu. Lo rehace `auditar_margen_profesional.py` contra
                # la fuente viva, en el BLOQUE 80.
                "margen_profesional": t.get("margen_profesional"),
                "fuente": t.get("fuente"),
                "por_que": t.get("por_que"),
            })
        salida.sort(key=lambda x: x["nutriente"])
        return salida

    def _ratios_servidos(bloque):
        """Los ratios de la patologia, con el de FEDIAF del mismo par al lado."""
        # El unico ratio que FEDIAF pone es el Ca:P, y esta en su propia fila de
        # la tabla (no en `MAPA`, porque no es un nutriente). Se lee de ahi y no
        # se escribe a mano: una segunda copia del 1,0-2,0 es exactamente como
        # se desincronizo la tabla de patologias del POST /menu.
        _fediaf_por_par = {}
        for fila in reqs:
            if fila.get("nutriente") == "Relacion_Ca_P":
                _fediaf_por_par[("calcio", "fosforo")] = (_num(fila.get("minAdulto")),
                                                          _num(fila.get("maxAdulto")))
        salida = []
        for clave, r in (bloque or {}).items():
            _par = (r.get("numerador"), r.get("denominador"))
            _f_min, _f_max = _fediaf_por_par.get(_par, (None, None))
            _valor = _num(r.get("valor"))
            _referencia = _f_min if r.get("sentido") == "min" else _f_max
            _margen = None
            if _valor is not None and _referencia:
                _margen = round((_valor - _referencia) / _referencia * 100, 1)
            salida.append({
                "clave": clave,
                "numerador": r.get("numerador"),
                "denominador": r.get("denominador"),
                "sentido": r.get("sentido"),
                "valor": _valor,
                "minimo_fediaf_adulto": _f_min,
                "maximo_fediaf_adulto": _f_max,
                "margen_pct": _margen,
                "margen_profesional": r.get("margen_profesional"),
                "aplicado_por_el_solver": bool(r.get("aplicado_por_el_solver")),
                "fuente": r.get("fuente"),
                "por_que": r.get("por_que"),
            })
        salida.sort(key=lambda x: x["clave"])
        return salida

    crudo = cargar_crudo()
    salida = {}
    for clave, p in crudo["patologias"].items():
        avisos = p.get("avisos") or {}
        salida[clave] = {
            "nombre": p.get("nombre"),
            "formulable": bool(p.get("formulable")),
            "formulable_por_profesional": bool(p.get("formulable_por_profesional")),
            "necesita_bajo_fediaf": bool(p.get("necesita_bajo_fediaf")),
            "motivo_no_formulable": p.get("motivo_no_formulable"),
            "solo_en_adulto": bool(p.get("solo_en_adulto")),
            "en_crecimiento": p.get("en_crecimiento"),
            "nutriente_frontera": p.get("nutriente_frontera"),
            "objetivo_terapeutico_por_1000kcal": p.get("objetivo_terapeutico_por_1000kcal"),
            "excluye_fruta": bool(p.get("excluye_fruta")),
            "max_pct_kcal_grasa_si_ademas": p.get("max_pct_kcal_grasa_si_ademas"),
            "nota": p.get("nota"),
            "topes": _limites(p.get("topes_por_1000kcal"), es_tope=True),
            "suelos": _limites(p.get("suelos_por_1000kcal"), es_tope=False),
            # ⚠️ AÑADIDO (10 septiembre) — LOS TOPES QUE SOLO APLICAN CON OTRA
            # PATOLOGIA MARCADA. Existen desde el 8 de septiembre (la grasa de
            # la pancreatitis baja de 37,5 a 25 si ademas hay obesidad o
            # hipertrigliceridemia) y este endpoint no los servia, asi que quien
            # leia la ficha veia 37,5 y no sabia que hay un segundo escalon. Es
            # el mismo hueco de los `avisos_extra`: escrito, aplicado, y sin
            # llegar a ninguna pantalla.
            "topes_si_ademas": [
                dict(t, requiere=list((p.get("topes_por_1000kcal_si_ademas") or {})
                                      .get(t["nutriente"], {}).get("requiere") or []))
                for t in _limites(p.get("topes_por_1000kcal_si_ademas"), es_tope=True)],
            # ⚠️ AÑADIDO (10 septiembre) — LOS RATIOS QUE PIDE LA PATOLOGIA.
            # Se sirven con el limite de FEDIAF del MISMO ratio al lado, que es
            # el sentido entero de este endpoint: el oxalato pide Ca:P >= 1,1 y
            # FEDIAF pide >= 1,0 en adulto, o sea que aprieta un 10 %. Sin ese
            # numero enfrente, «1,1» no dice si es un limite estrecho o un
            # adorno. Van con `aplicado_por_el_solver` explicito porque hasta
            # hoy estos dos estaban escritos y NO se aplicaban.
            "ratios": _ratios_servidos(p.get("ratios")),
            # El aviso que ya le llega dentro del menu, aqui tambien: al
            # ELEGIR la patologia, que es cuando decide, no despues de
            # formular.
            "aviso_profesional": avisos.get("profesional"),
            "aviso_profesional_crecimiento": avisos.get("profesional_crecimiento"),
            "aviso_general": avisos.get("general"),
            # ⚠️ AÑADIDO (8 septiembre) — los avisos que no son ninguno de los
            # cuatro con nombre propio. Ver `avisos_extra` en patologias.py:
            # antes se cargaban del JSON y no llegaban a ningún sitio. Aquí
            # importan más que en el menú: son las frases donde la fuente pide
            # algo que el motor NO puede hacer solo (una o dos proteínas y
            # novel, no formular durante la fase de diagnóstico), y quien firma
            # una pauta necesita leerlas antes de elegir la patología.
            "avisos_extra": [avisos[k] for k in sorted(avisos)
                             if k not in ("general", "crecimiento", "profesional",
                                          "profesional_crecimiento") and avisos[k]],
            # ⚠️ Y LO QUE ESTÁ ESCRITO PERO NO SE APLICA, DICIENDO QUE NO SE
            # APLICA. Una cifra de la fuente que el motor no puede imponer
            # (porque no cabe, o porque depende de un dato clínico que no
            # tenemos) se guarda igual con su fuente para no perderla -- pero
            # servirla sin la etiqueta sería peor que no servirla: parecería un
            # límite. Mismo criterio que `aplicado_por_el_solver`, que desde el
            # 10 de septiembre viaja también con cada ratio: los dos Ca:P de los
            # urolitos de calcio eran el ejemplo de aquí y ya SÍ se aplican.
            "limites_escritos_que_el_solver_no_aplica":
                p.get("limites_escritos_que_el_solver_no_aplica"),
        }
    return {"unidad": crudo["_meta"]["unidad"], "patologias": salida}


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


# =====================================================================
# COMPROBAR QUE SENTRY RECOGE DE VERDAD — se abre en el navegador
#   https://canislab-api.onrender.com/sentry/prueba
# Provoca un error a proposito para verificar que llega al panel de
# Sentry. Va apagado salvo que se ponga SENTRY_PRUEBA=1 en Render, para
# que no quede una URL publica que cualquiera pueda usar para llenar de
# ruido el proyecto (el plan gratuito tiene un limite de eventos al mes).
# Cuando ya se ha comprobado, se quita esa variable y listo.
# =====================================================================
@app.get("/sentry/prueba")
def sentry_prueba():
    if os.environ.get("SENTRY_PRUEBA") != "1":
        raise HTTPException(404, "No encontrado")
    if not observabilidad.activo():
        raise HTTPException(
            400, "Sentry no esta activo: falta la variable SENTRY_DSN en el entorno.")
    raise RuntimeError("Error de prueba de Rawku: si ves esto en Sentry, funciona.")
