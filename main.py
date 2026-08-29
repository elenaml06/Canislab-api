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
from constructor import tabla_imputacion_maximos, valor_para_maximo
from motor_completo import PATOLOGIAS, topes_de_patologias
from exclusiones import filtrar as filtrar_exclusiones
from constructor import cargar as cargar_v2, MARGENES as MARGENES_V2
from verificar import verificar as verificar_v2
from verificar import peso_objetivo_desde_bcs, BCS_ESCALA_SATURADA
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
    _topes, _pct, avisos_por_la_etapa = topes_de_patologias(patologias, etapa)
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
        TOPE_VITD_KCAL, TOPE_VITD_KG075, TOPE_YODO_KCAL, TOPE_SELENIO_KCAL, _es,
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

    # ⚠️ El selenio se topa POR ENERGÍA y no por peso de comida. Antes iba
    # a 2 µg por gramo de dieta, que es el número de Merck pero en base
    # MATERIA SECA aplicado sobre el peso fresco: con un 70-75% de agua,
    # eso dejaba pasar entre tres y cuatro veces el límite real. Ver
    # TOPE_SELENIO_KCAL en seguridad.py.
    selenio_ug = sum(al.get(n, {}).get("nutrientes", {}).get("selenio", 0) * g / 100.0 for n, g in gramos.items())
    if selenio_ug > TOPE_SELENIO_KCAL * der / 1000.0:
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


def _tope_patologia_roto(gramos, al, patologias, etapa="Adulto"):
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
    """
    if not patologias or not gramos:
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
    topes, pct, _ = topes_de_patologias(patologias, etapa)
    for clave, tope in topes.items():
        v = por_1000(clave)
        if v > tope * MARGEN:
            rotos.append(f"{clave} {v:.1f} (tope {tope:.1f} por patología)")
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

    Solo aplica a raza grande/gigante (peso adulto esperado >= 25 kg) y en
    crecimiento; para el resto, el mínimo bueno es el genérico y esta
    función no dice nada. Es el mismo criterio y la misma fila de la tabla
    que usa el solver -- si se leyera aquí de otra manera, la comprobación
    y la restricción podrían discrepar.
    """
    RAZA_GRANDE_O_GIGANTE_KG = 25
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
            return derivado, "derivado_del_bcs"
        # Por debajo de BCS 5 no se estima: la regla no existe hacia abajo
        # y AAHA 2021 dice lo contrario -«base feeding calculations on
        # current weight if ideal or underweight»-. Se usa el peso real.
    if actual:
        return float(actual), "peso_real_sin_objetivo"
    return None, "sin_peso"


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
    topes_rotos = _tope_patologia_roto(gramos, al, patologias, etapa)
    calcio_corto = _minimo_calcio_raza_grande_roto(gramos, al, req, etapa,
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
            "verificacion": {"topes_de_patologia_rotos": topes_rotos},
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
            "verificacion": {"minimo_calcio_raza_grande_roto": calcio_corto},
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
        verificado = _garantizar_verificado(
            {"factible": True, "gramos": gramos_escalados},
            der_objetivo, etapa, peso_perro_kg, origen="/catalogo", al=al, req=_req_cat)
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
        _resp_v2 = _garantizar_verificado(
            _resolver_menu_v2_interno(datos),
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
                    margenes_categoria=MARGENES_V2, max_suplementos=2, forzar=base, time_limit=tiempo_restante(),
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
                             margenes=None, max_supl=2):
        """Un intento completo: llamada + reintentos para mejorar a
        verde mientras quede presupuesto de tiempo -- misma lógica que
        ya existía, solo que reutilizable para los tres niveles."""
        ok_i, gramos_i = resolver_v2(
            datos.der_objetivo, datos.etapa_requisitos, al, req,
            datos.peso_perro_kg, dosis_maxima_fabricante,
            excluidos=excluidos or None,
            margenes_categoria=(margenes if margenes is not None else MARGENES_V2),
            max_suplementos=max_supl, time_limit=tiempo_restante(),
            forzar=forzar_este, preferir=preferir,
            patologias=datos.patologias, restringir_especie=datos.restringir_especie,
            peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg,
            peso_objetivo_kg=_peso_de_referencia(datos)[0],
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
                margenes_categoria=(margenes if margenes is not None else MARGENES_V2),
                max_suplementos=max_supl, time_limit=tiempo_restante(),
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
            else:
                break
        return (ok_i and ficha_i and ficha_i["semaforo"] == "verde"), gramos_i, ficha_i

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
            margenes_categoria=MARGENES_V2, max_suplementos=2, time_limit=tiempo_restante(),
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
    hay_comida = _hay_comida_de_verdad(al, excluidos, datos.categorias_excluidas)
    if not ok:
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
        # ⚠️ SIN EL NÚMERO ESCRITO (29 agosto). Aquí ponía "los 30
        # requisitos" y el motor ya verifica 42 desde que se encendieron los
        # aminoácidos: el mensaje que ve la usuaria decía una cifra y el
        # motor comprobaba otra. Es el mismo fallo que describe el CLAUDE.md
        # sobre el DER -- un número escrito en dos sitios se separa, y el
        # que está en un texto no lo cubre ninguna prueba.
        # Encontrado pidiendo un menú de hepatopatía contra producción.
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

        def hay_tiempo_para_otra_ronda():
            """Una ronda es un menú para CADA perro. Si no cabe entera, se
            para: media ronda dejaría a unos perros con más menús que a
            otros, y entonces la semana de la casa no cuadra."""
            return queda() >= por_llamada + SEGUNDOS_AMOLDARSE * (n - 1)

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

            for i in orden[1:]:
                r = generar(i, j, forzar_estos=list(gramos_base))
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
    ⚠️ MATIZADO (20 agosto) — auditando los caminos por los que sale un
    menú: esto devuelve lo que hay GUARDADO, y la tabla `menus` solo
    almacena nombre, gramos y kcal -- no la etapa ni el DER contra los
    que se verificó en su día. Es decir: un menú sacado de aquí no se
    puede verificar, ni siquiera en principio, porque falta el dato de
    contra qué habría que verificarlo. Y si el perro ha cambiado de
    etapa desde que se guardó, puede haber dejado de cumplir sin que
    nada lo detecte (ver /menu/revalidar).
    Se marca explícitamente para que nadie lo confunda con un menú
    verificado: quien lo use tiene que pasarlo por /menu/revalidar con
    los datos actuales del perro antes de dárselo a nadie.
    """
    menus = persistencia.obtener_menus(perro_id)
    for m in menus:
        m["verificado"] = False
        m["aviso"] = ("Menú guardado: no se ha comprobado contra la etapa actual del "
                      "perro. Pásalo por /menu/revalidar antes de usarlo.")
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
        # ⚠️ ACTUALIZADO (21 agosto) al añadir 7 alimentos con fuente
        # verificada (corazón y molleja de pavo, hígado de pavo y de pato,
        # y completar corazón/molleja de pollo, molleja de pavo y timo de
        # ternera). Este sello SOLO se toca cuando el cambio de datos es a
        # propósito y está documentado: si no coincide sin haberlo tocado,
        # es que alguien alteró el catálogo, y eso es lo que vigila.
        "alimentos_v3_final.json":      "4d634b9cf5f19fdc",   # 28 ago (2): EL HIGADO Y EL CORAZON DE PAVO, resembrados desde el pollo del USDA -- su aminograma venia del pavo del USDA, que tiene la isoleucina y la valina un 40% bajas (Leu/Ile 2,52 contra 1,47-1,98 del resto). Reescalados a NUESTRA proteina. Las otras cinco fichas de pavo NO se cargan: traian histidina = isoleucina = valina exactos, y eso es una copia, no una medida. Ver el BLOQUE 27. // 28 ago: PURINAS DE CUATRO VISCERAS con cifra publicada (timo 525, bazo de cordero 322, bazo de vaca 185, pulmon de ternera 117). NO se uso la banda generica 84-243 que se habia propuesto: para el timo habria declarado ~160 cuando la cifra son 525, un factor de 3 a 4 POR ABAJO, y es el alimento solido con mas purinas de las tablas. Pancreas, testiculos y pulmon de cordero se quedan como hueco: no hay dato. Ver el BLOQUE 33
        "requerimientos_v2_final.json": "68f335c24a4ec898",   # 28 ago: EL ANCLA DE 110. Cada nutriente lleva ahora `minAdulto110`, la columna de DER 110 de la Tabla III-3b, sacada de NUESTRA transcripcion auditada del PDF y no de fuera. Con las dos anclas se puede aplicar la ecuacion del apartado 7.2.5: cuando el perro come menos, el minimo por 1000 kcal sube. Los 38 cuadraron con el minAdulto de siempre sin una discrepancia, o sea que nuestra columna ES la de 95. Ver el BLOQUE 34
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
