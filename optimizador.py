"""
CANISLAB - Optimizador matematico de menus

=====================================================================
CLASIFICACION DE LAS RESTRICCIONES  (importante: leer antes de tocar)
=====================================================================
Las restricciones de este motor NO son todas iguales. Hay dos clases,
y conviene no confundirlas nunca:

[CIENCIA] -- respaldadas por una fuente veterinaria concreta y citada.
             NO tocar sin volver a la fuente.
  1. Los 27 nutrientes FEDIAF (min y max)      -> FEDIAF 2021
     (escalados por DER/1000: los valores FEDIAF son POR 1000 kcal)
  2. Kcal exactas = DER                        -> estandar
  3. Higado <= 5% del peso total               -> hipervitaminosis A
  4. Higado + visceras <= 10%                  -> ACVIM
  5. Yodo de algas <= 1400 ug/1000kcal         -> SUL del NRC 2006
  6. Espinaca + acelga <= 4%                   -> oxalatos; Chai &
                                                  Liebman 2005, JAFC
  7. Verdura + fruta <= 10% de las kcal        -> consenso WSAVA

[CRITERIO] -- puestas por el desarrollo para que los menus sean
              practicos y realistas. Resuelven problemas REALES que se
              observaron generando menus de prueba (salian 600g de un
              solo corte, 0g de pescado, 2.5% de hueso, 369g de
              arandanos), pero NO salen de ninguna fuente veterinaria.
              >>> DEBEN SER VALIDADAS POR UN VETERINARIO NUTRICIONISTA
  8.  Carne muscular >= 80g (escalado por DER)
  9.  Verdura >= 50g (escalado por DER)
  10. Visceras >= 30g (escalado por DER)
  11. Ningun alimento individual > 30% del peso total
  12. Hueso carnoso >= 8% del peso total
  13. Pescado >= 5% del peso total
  14. Cada verdura/fruta individual <= 15% del peso total
  15. Grasa <= 35% de las kcal (prudencia pancreatitis; FEDIAF NO fija
      maximo numerico de grasa, asi que esto es criterio, no norma)
  16. Suplementos <= 2% del peso total
=====================================================================
"""
import json
import math
from scipy.optimize import linprog

NUTRIENTES_CLAVE = [
    "proteina", "grasa", "dha", "epa", "linoleico", "linolenico", "araquidonico",
    "vitA", "vitD", "vitE", "folato", "niacina", "riboflavina", "tiamina",
    "vitB12", "vitB6", "calcio", "hierro", "potasio", "magnesio", "sodio",
    "fosforo", "yodo", "selenio", "zinc", "cobre", "manganeso",
    "acidoPantotenico", "colina", "cloruro",
]

# mapea el nombre de requerimientos.json a la clave interna de nutrientes
MAPA_REQUISITO_A_NUTRIENTE = {
    "Proteína_total": "proteina",
    "Grasa_total": "grasa",
    "Linoleico": "linoleico",
    "Linolénico": "linolenico",
    "Araquidónico": "araquidonico",
    "Vitamina_A": "vitA",
    "Vitamina_D": "vitD",
    "Vitamina_E": "vitE",
    "Folato": "folato",
    "Niacina": "niacina",
    "Riboflavina": "riboflavina",
    "Tiamina": "tiamina",
    "Vitamina_B12": "vitB12",
    "Vitamina_B6": "vitB6",
    "Calcio": "calcio",
    "Hierro": "hierro",
    "Potasio": "potasio",
    "Magnesio": "magnesio",
    "Sodio": "sodio",
    "Fósforo": "fosforo",
    "Yodo": "yodo",
    "Selenio": "selenio",
    "Zinc": "zinc",
    "Cobre": "cobre",
    "Manganeso": "manganeso",
    "Acido_pantotenico": "acidoPantotenico",
    "Colina": "colina",
    "Cloruro": "cloruro",
}


def cargar_requerimientos(path="requerimientos_v2_final.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# =====================================================================
# EQUIVALENCIA DE ETAPAS (segun como las agrupa FEDIAF)
# =====================================================================
# La app ofrece 6 etapas pero requerimientos_v2_final.json solo tiene
# columnas para 3. No es un hueco que haya que rellenar inventando datos:
# FEDIAF NO define tablas separadas para gestacion, lactancia ni senior.
#   - Gestacion y lactancia: FEDIAF las agrupa junto al crecimiento en una
#     unica categoria "Growth and Reproduction" (AAFCO hace lo mismo). Se
#     entiende bien: en los tres casos el animal esta construyendo tejido
#     nuevo y necesita el mismo perfil reforzado.
#   - Senior: FEDIAF no le da tabla propia; usa la de adulto. La unica
#     particularidad documentada es subir la proteina para cubrir a los
#     perros mayores (FEDIAF eleva la RA de 40 a 45 g/1000kcal por este
#     motivo), lo que se aplica abajo con SENIOR_PROTEINA_MINIMA.
EQUIVALENCIA_ETAPAS = {
    "Gestante": "CachorroCrecimiento",   # Growth and Reproduction
    "Lactante": "CachorroCrecimiento",   # Growth and Reproduction
    "Senior": "Adulto",                  # sin tabla propia en FEDIAF
}
# FEDIAF sube la proteina recomendada para perros mayores (40 -> 45
# g/1000kcal). Si nuestro valor de adulto ya es mas alto, se respeta el
# nuestro y esto no hace nada.
SENIOR_PROTEINA_MINIMA = 45.0


def resolver_etapa(etapa_pedida):
    """Devuelve la etapa cuyos requisitos hay que usar realmente."""
    return EQUIVALENCIA_ETAPAS.get(etapa_pedida, etapa_pedida)


def _valor_o_none(v):
    if v is None or v == "-" or v == "":
        return None
    return float(v)


# PREFERENCIA SUAVE (no regla dura): cada alimento tiene un "coste" distinto
# segun su rol tipico en una racion BARF. Esto NO impide que el optimizador
# use mas de lo habitual si un nutriente concreto lo exige de verdad -- solo
# hace que, cuando hay varias soluciones matematicamente validas, prefiera
# la que se parece mas a una racion BARF realista (base de carne/hueso, no
# cantidades enormes de verdura de hoja suelta).
PESO_POR_CATEGORIA = {
    "Carne muscular": 1.0,
    "Hueso carnoso": 1.0,
    "Vísceras": 8.0,
    "Hígado": 12.0,
    "Pescados y mariscos": 3.0,
    "Verduras y frutas": 6.0,
    "Extras": 5.0,
    "Suplementos comerciales": 8.0,
}


def _resolver_lp(alimentos_elegidos: list, der_objetivo: float, etapa_requisitos: str = "Adulto",
                  forzar_presencia: list = None):
    """
    alimentos_elegidos: lista de dicts (formato alimentos_v3_final.json), uno
                         por cada "ranura" del menu (ej: carne, hueso, viscera,
                         higado, verdura -- lo que se haya elegido)
    etapa_requisitos: "Adulto" | "CachorroJoven" | "CachorroCrecimiento"
                       (sufijo usado en requerimientos_v2_final.json)

    Devuelve dict con:
      - "factible": True/False
      - "gramos": {nombre_alimento: gramos} si factible
      - "kcal_total", "total_gramos"
      - "motivo" si NO es factible (para el aviso al usuario, punto 6)
    """
    requerimientos = cargar_requerimientos()
    n = len(alimentos_elegidos)

    # energia por 100g de cada alimento (columna objetivo: minimizar gramos totales)
    kcal_100g = [a["energia"] for a in alimentos_elegidos]

    c = [PESO_POR_CATEGORIA.get(a["categoria"], 1.0) for a in alimentos_elegidos]

    A_ub = []
    b_ub = []
    A_eq = []
    b_eq = []

    # restriccion de igualdad: las kcal deben cuadrar EXACTO con el DER
    A_eq.append(kcal_100g)
    b_eq.append(der_objetivo)

    detalles_restricciones = []

    # Los valores de FEDIAF (requerimientos_v2_final.json) estan expresados
    # POR CADA 1000kcal de Energia Metabolizable -- NO son cantidades fijas
    # diarias absolutas. Sin este escalado, un perro pequeño (ej. 400kcal)
    # se le exigian nutrientes calculados para 1000kcal con mucha menos
    # comida disponible (infeasibilidad real, verificado con pruebas: fallaba
    # ~50% en perros pequeños), y a un perro grande posiblemente se le estaba
    # exigiendo de menos. Este es EL escalado correcto y estandar en FEDIAF.
    escala_fediaf = der_objetivo / 1000

    # ===================================================================
    # SALVAGUARDA: etapa sin requisitos definidos
    # ===================================================================
    # La app ofrece 6 etapas (Adulto, CachorroJoven, CachorroCrecimiento,
    # Gestante, Lactante, Senior) pero requerimientos_v2_final.json solo
    # tiene columnas para las 3 primeras. Sin esta comprobacion, al elegir
    # Gestante/Lactante/Senior el motor no encontraba NINGUN requisito y
    # devolvia un menu "factible" que en realidad solo cuadraba las kcal,
    # sin validar un solo nutriente -- el peor fallo posible, porque
    # aparenta funcionar. Mejor negarse a generar que dar un menu falso.
    # traducir la etapa pedida a la que tiene requisitos reales
    # (Gestante/Lactante -> CachorroCrecimiento; Senior -> Adulto)
    etapa_datos = resolver_etapa(etapa_requisitos)

    _requisitos_de_esta_etapa = sum(
        1 for req in requerimientos
        if MAPA_REQUISITO_A_NUTRIENTE.get(req["nutriente"])
        and _valor_o_none(req.get(f"min{etapa_datos}")) is not None
    )
    if _requisitos_de_esta_etapa == 0:
        return {
            "factible": False,
            "motivo": (
                f"Todavia no tenemos los requisitos nutricionales de la etapa "
                f"'{etapa_requisitos}' cargados, asi que no podemos calcular un "
                f"menu fiable para ella. Usa otra etapa o consulta con tu "
                f"veterinario para esta situacion."
            ),
            "detalle_tecnico": f"sin columnas min{etapa_datos} en requerimientos_v2_final.json",
        }

    for req in requerimientos:
        nutriente_key = MAPA_REQUISITO_A_NUTRIENTE.get(req["nutriente"])
        if nutriente_key is None:
            continue  # ratio Ca:P y casos especiales se tratan aparte

        minimo = _valor_o_none(req.get(f"min{etapa_datos}"))
        maximo = _valor_o_none(req.get(f"max{etapa_datos}"))
        # Senior: FEDIAF sube la proteina para perros mayores
        if etapa_requisitos == "Senior" and req["nutriente"] == "Proteína_total":
            if minimo is None or minimo < SENIOR_PROTEINA_MINIMA:
                minimo = SENIOR_PROTEINA_MINIMA

        if minimo is not None:
            # MARGEN DE REDONDEO: los gramos finales se redondean a 0.1g, y
            # en cantidades pequeñas (un perro de 150kcal, o un ingrediente
            # concentrado como el kelp) ese redondeo puede recortar hasta un
            # 10% del aporte de ese alimento. Si pidieramos el minimo exacto,
            # el menu redondeado quedaria POR DEBAJO de lo que decimos que
            # cumple. Se pide un 2% de mas para absorber el redondeo.
            minimo *= escala_fediaf * 1.02
        if maximo is not None:
            # simetrico al margen de los minimos: como los gramos se
            # redondean hacia arriba, se pide un 2% menos de maximo para que
            # ese redondeo no acabe pasandose del limite de seguridad
            maximo *= escala_fediaf * 0.98

        valores = [a["nutrientes"].get(nutriente_key, 0) for a in alimentos_elegidos]

        if minimo is not None and minimo > 0:
            # -sum(valor_i * x_i) <= -minimo  ==  sum(valor_i * x_i) >= minimo
            A_ub.append([-v for v in valores])
            b_ub.append(-minimo)
            detalles_restricciones.append(f"min {req['nutriente']} >= {minimo:.2f}{req['unidad']}")

        if maximo is not None and maximo > 0:
            A_ub.append(valores)
            b_ub.append(maximo)
            detalles_restricciones.append(f"max {req['nutriente']} <= {maximo:.2f}{req['unidad']}")

    # MINIMO garantizado de verdura y de visceras (no solo higado) -- no es
    # una regla de porcentaje artificial, es una garantia razonada de que la
    # dieta tenga fibra vegetal (transito intestinal) y variedad de organos
    # (nutrientes que el listado de 27 no recoge del todo), aunque los 27
    # nutrientes trackeados ya se puedan cumplir sin ellos matematicamente.
    # IMPORTANTE: estos minimos son PROPORCIONALES al DER (gramos por cada
    # 100kcal), no gramos fijos -- un perro pequeño (ej. 400kcal) tiene una
    # racion total mucho mas pequeña, y un minimo fijo pensado para un perro
    # de tamaño medio (ej. 80g en 1200kcal) podria ser casi la mitad de toda
    # su racion, chocando con las kcal exactas. Verificado con pruebas en
    # perros de 400 a 3000kcal -- con gramos fijos fallaba ~50% en perros
    # pequeños, con esto pasa a ser factible de verdad en cualquier tamaño.
    factor_escala = der_objetivo / 1223  # 1223kcal = caso de referencia validado (Cairo)

    idx_verduras = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Verduras y frutas"]
    if idx_verduras:
        fila = [0.0] * n
        for i in idx_verduras:
            fila[i] = -1.0
        A_ub.append(fila)
        b_ub.append(-0.5 * factor_escala)  # ~50g de verdura/fruta a 1223kcal, escalado

    idx_visceras_no_higado = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Vísceras"]
    if idx_visceras_no_higado:
        fila = [0.0] * n
        for i in idx_visceras_no_higado:
            fila[i] = -1.0
        A_ub.append(fila)
        b_ub.append(-0.3 * factor_escala)  # ~30g de visceras a 1223kcal, escalado

    # MISMA LOGICA para Carne muscular: sin esto, si otro alimento (ej. un
    # hueso con mucho calcio) resuelve todo por si solo, la carne muscular
    # se queda casi a cero -- razonable poner un minimo real de presencia.
    # IMPORTANTE: la carne que viene PEGADA a un hueso carnoso (ej. Cuello
    # de ternera tiene un 40% de carne real, segun la tabla pct_carne) es
    # carne de verdad y debe contar tambien para este minimo -- si no, el
    # motor exige mas "carne pura" de la necesaria, contando dos veces de
    # menos la carne que ya viene en los huesos. Señalado por el usuario.
    idx_carne = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Carne muscular"]
    idx_hueso_con_carne = [(i, a.get("pct_carne", 0)) for i, a in enumerate(alimentos_elegidos)
                            if a["categoria"] == "Hueso carnoso" and a.get("pct_carne")]
    if idx_carne or idx_hueso_con_carne:
        fila = [0.0] * n
        for i in idx_carne:
            fila[i] = -1.0
        for i, pct in idx_hueso_con_carne:
            fila[i] = -pct
        A_ub.append(fila)
        b_ub.append(-0.8 * factor_escala)  # ~80g de carne muscular equivalente a 1223kcal, escalado

    # LIMITE REAL DE SEGURIDAD DIGESTIVA para el Higado (NO es la regla BARF
    # "70/10/5" que se rechazo antes -- esto es un limite de tolerancia
    # digestiva documentado de verdad: el higado, por su riqueza en grasa,
    # puede causar diarrea por intolerancia digestiva incluso si la Vitamina A
    # se queda dentro del maximo FEDIAF. Varias fuentes veterinarias/raw
    # feeding coinciden en ~5% del total de la racion como limite practico
    # seguro, independiente del calculo de nutrientes.
    idx_higado = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Hígado"]
    if idx_higado:
        fila = [0.0] * n
        for i in range(n):
            fila[i] = -0.05  # -0.05 * cada alimento (para el total de la racion)
        for i in idx_higado:
            fila[i] += 1.0  # +1.0 * higado -- resultado: higado - 0.05*total <= 0
        A_ub.append(fila)
        b_ub.append(0.0)

    # MISMO CRITERIO para Visceras (riñon, pulmon, lengua...) -- varias
    # fuentes veterinarias (ACVIM, veterinarios holisticos) recomiendan que
    # TODOS los organos juntos (higado + visceras) no superen el 10% de la
    # dieta, por el mismo motivo digestivo real (alto contenido en grasa,
    # riesgo de diarrea/pancreatitis en exceso). Con el higado ya limitado
    # al 5%, se pone otro 5% para visceras, sumando el 10% recomendado
    idx_visceras_cap = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Vísceras"]
    if idx_visceras_cap:
        fila = [0.0] * n
        for i in range(n):
            fila[i] = -0.05
        for i in idx_visceras_cap:
            fila[i] += 1.0
        A_ub.append(fila)
        b_ub.append(0.0)

    # TOPE REAL en gramos absolutos para Suplementos comerciales (kelp,
    # levadura de cerveza...): son productos MUY concentrados en un nutriente
    # concreto (ej. kelp = 109900 microgramos de yodo por 100g) -- esa
    # diferencia de escala tan grande frente al resto de nutrientes puede
    # hacer que el solver matematico devuelva cantidades absurdas (varios
    # kilos) por un problema de precision numerica, no porque haga falta
    # nutricionalmente.
    # OJO: los 15 suplementos NO usan la categoria "Suplementos comerciales"
    # en los datos reales (estan repartidos en Calcio/Fibra/Hierro/
    # Multivitaminico/Omega-3/VitaminaB/Yodo) -- lo fiable es el campo
    # "tipo", que SI es consistente ("Suplemento" en los 15)
    # CORREGIDO: el 30g fijo anterior NO estaba sacado de ninguna fuente real
    # y ademas no escalaba con el tamaño del perro (mismo fallo que el
    # escalado FEDIAF de mas arriba). Fuentes reales de dosificacion
    # comercial (ej. kelp: 1/4 cucharadita por cada 10 libras de peso) dan
    # cantidades de solo 1-5g para la mayoria de perros -- se usa un 2% del
    # total de la racion como red de seguridad matematica razonable (escala
    # con el tamaño del perro), NO como dosis prescriptiva -- la app ya le
    # dice al usuario que siga la dosis del fabricante en el envase para
    # cada producto concreto
    idx_suplementos = [i for i, a in enumerate(alimentos_elegidos) if a.get("tipo") == "Suplemento"]
    if idx_suplementos:
        fila = [0.0] * n
        for i in range(n):
            fila[i] = -0.02
        for i in idx_suplementos:
            fila[i] += 1.0
        A_ub.append(fila)
        b_ub.append(0.0)  # maximo 2% del total de la racion en suplementos

    # TOPE ESPECIFICO DE YODO POR KELP/ALGAS -- investigado (Research): el
    # yodo del kelp varia hasta 100 VECES entre lotes/especies de alga
    # (Aakre et al., Frontiers in Nutrition -- oarweed 7800, sugarkelp 4469,
    # kombu 2276 microgramos/g de media, con enorme variabilidad), y hay
    # casos reales de tirotoxicosis documentados (Veterinary Record 2017)
    # por kelp mal dosificado. El 2% generico de suplementos NO es
    # suficiente proteccion especifica -- se limita el YODO TOTAL aportado
    # por productos tipo "Yodo" (kelp, algas) a un maximo mas conservador
    # que el limite legal FEDIAF, usando el Safe Upper Limit de NRC 2006
    # (1400 microgramos por 1000kcal, mas prudente que el maximo legal
    # FEDIAF de 2750 microgramos/1000kcal)
    idx_yodo_kelp = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Yodo"]
    if idx_yodo_kelp:
        fila = [0.0] * n
        for i in idx_yodo_kelp:
            fila[i] = alimentos_elegidos[i]["nutrientes"].get("yodo", 0)
        A_ub.append(fila)
        b_ub.append(1400 * escala_fediaf)  # SUL NRC 2006, escalado por DER

    # TOPE DE GRASA TOTAL -- FEDIAF no fija un maximo numerico de grasa,
    # pero la prudencia veterinaria general (WSAVA, y consenso clinico
    # amplio aunque cuestionado por revisiones recientes) recomienda no
    # superar ~35-40% de las kcal en forma de grasa para evitar sobrecargar
    # el margen de seguridad frente a pancreatitis, sobre todo en cachorros.
    # 1g de grasa = 9kcal -- limitar la grasa total a 35% de las kcal del DER
    idx_grasa_todos = list(range(n))
    fila = [0.0] * n
    for i in idx_grasa_todos:
        fila[i] = alimentos_elegidos[i]["nutrientes"].get("grasa", 0) * 9  # kcal de grasa aportadas
    A_ub.append(fila)
    b_ub.append(der_objetivo * 0.35)  # maximo 35% de las kcal totales como grasa

    # TOPE DE VERDURAS+FRUTA TOTAL -- consenso veterinario general (WSAVA):
    # los vegetales/fruta no deberian superar ~10% de las kcal diarias,
    # para no diluir nutrientes esenciales de origen animal y evitar
    # molestias digestivas por fibra cruda en exceso
    idx_verdura_cap = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Verduras y frutas"]
    if idx_verdura_cap:
        fila = [0.0] * n
        for i in idx_verdura_cap:
            fila[i] = alimentos_elegidos[i]["energia"]  # kcal aportadas por verdura/fruta
        A_ub.append(fila)
        b_ub.append(der_objetivo * 0.10)  # maximo 10% de las kcal totales en verdura/fruta

    # TOPE POR VERDURA/FRUTA INDIVIDUAL -- problema real detectado al generar
    # menus de prueba: salian 369g de arandanos o 197g de espinaca en un solo
    # dia. Cumplen el tope global del 10% de kcal (la fruta/verdura tiene muy
    # pocas kcal por gramo), pero en la practica son cantidades absurdas de
    # dar. Se limita cada verdura/fruta individual al 15% del PESO total
    # (probado: al 8% la tasa de factibilidad caia al 69%, al 15% queda en
    # 81% y sigue evitando las cantidades absurdas).
    for i in idx_verdura_cap:
        fila = [0.0] * n
        for j in range(n):
            fila[j] = -0.15
        fila[i] += 1.0
        A_ub.append(fila)
        b_ub.append(0.0)

    # LIMITE DE OXALATOS -- espinaca y acelga son ricas en oxalatos, que en
    # cantidad favorecen los calculos de oxalato calcico. Chai & Liebman
    # (2005, J Agric Food Chem) demostraron que hervirlas reduce el oxalato
    # soluble un 30-87%, y la recomendacion veterinaria es darlas de forma
    # ocasional, no en cantidad diaria. Nuestras verduras ya van siempre
    # cocidas (lo que ayuda mucho), pero se limita ademas la cantidad
    OXALATO_ALTO = {"Espinaca", "Acelga"}
    idx_oxalato = [i for i, a in enumerate(alimentos_elegidos) if a["nombre"] in OXALATO_ALTO]
    if idx_oxalato:
        fila = [0.0] * n
        for j in range(n):
            fila[j] = -0.04
        for i in idx_oxalato:
            fila[i] += 1.0
        A_ub.append(fila)
        b_ub.append(0.0)  # espinaca+acelga juntas <= 4% del peso total

    # ===================================================================
    # LIMITES DE INCLUSION POR ALIMENTO INDIVIDUAL
    # ===================================================================
    # PROBLEMA REAL DETECTADO al generar menus de prueba: el LP minimiza
    # gramos totales y, sin topes por alimento individual, encuentra
    # soluciones "de esquina" matematicamente optimas pero absurdas en la
    # practica: 600g de un solo corte de carne, 368g de arandanos, 0g de
    # pescado, solo 29g de hueso. Es el problema clasico del "Diet Problem"
    # (Stigler/Dantzig 1947): la solucion optima cumple los nutrientes pero
    # "puede no ser comestible" (NEOS Guide). Los motores profesionales de
    # formulacion (FAO, piensos) lo resuelven poniendo BOUNDS de inclusion
    # minima y maxima POR INGREDIENTE, no solo por categoria.

    # (a) Ningun alimento individual puede pasar del 30% del peso total --
    #     evita el "600g de un solo corte" y fuerza variedad real
    for i in range(n):
        fila = [0.0] * n
        for j in range(n):
            fila[j] = -0.30
        fila[i] += 1.0
        A_ub.append(fila)
        b_ub.append(0.0)

    # (b) Minimo real de Hueso carnoso: es la fuente de calcio de la dieta
    #     BARF y ademas cumple funcion dental/digestiva. Sin esto el motor
    #     usaba solo 29g (2.5%), nutricionalmente valido pero no es BARF
    idx_hueso_min = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Hueso carnoso"]
    if idx_hueso_min:
        fila = [0.0] * n
        for i in range(n):
            fila[i] = 0.08
        for i in idx_hueso_min:
            fila[i] -= 1.0
        A_ub.append(fila)
        b_ub.append(0.0)  # hueso carnoso >= 8% del peso total

    # (c) Minimo real de Pescado: es la fuente principal de omega-3 (EPA/DHA)
    #     de la dieta. El motor lo descartaba entero por ser "ineficiente"
    #     en gramos, aunque el usuario lo hubiera elegido expresamente
    idx_pescado_min = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Pescados y mariscos"]
    if idx_pescado_min:
        fila = [0.0] * n
        for i in range(n):
            fila[i] = 0.05
        for i in idx_pescado_min:
            fila[i] -= 1.0
        A_ub.append(fila)
        b_ub.append(0.0)  # pescado >= 5% del peso total, si hay pescado disponible

    # PRESENCIA FORZADA: cuando el usuario AÑADE un alimento a mano (ej. un
    # suplemento con el boton de la app), el motor a veces le asignaba 0,00g
    # porque matematicamente "no hacia falta" -- desde fuera parece que el
    # boton no hace nada. Si el usuario lo ha puesto expresamente, debe
    # aparecer con una cantidad real y visible en el menu.
    if forzar_presencia:
        for nombre_forzado in forzar_presencia:
            idx_f = [i for i, a in enumerate(alimentos_elegidos) if a["nombre"] == nombre_forzado]
            if not idx_f:
                continue
            i = idx_f[0]
            es_suplemento = alimentos_elegidos[i].get("tipo") == "Suplemento"
            # los suplementos se dosifican en pocos gramos; el resto de
            # alimentos, una cantidad minima que se vea en el plato
            minimo_g = 1.0 if es_suplemento else 20.0
            fila = [0.0] * n
            fila[i] = -1.0
            A_ub.append(fila)
            b_ub.append(-minimo_g / 100)

    bounds = [(0, None) for _ in range(n)]  # gramos no pueden ser negativos

    resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if not resultado.success:
        return {
            "factible": False,
            "motivo": (
                "No encontramos una combinación de estos alimentos que cumpla todos los "
                "nutrientes a la vez con las kcal exactas. Prueba a quitar alguna restricción "
                "o cambiar alguno de los alimentos elegidos."
            ),
            "detalle_tecnico": resultado.message,
        }

    gramos_por_alimento = {}
    kcal_total = 0
    total_gramos = 0
    descartados = []
    for a, x in zip(alimentos_elegidos, resultado.x):
        # REDONDEO HACIA ARRIBA (no al mas cercano): redondear a la baja
        # deja el menu por DEBAJO del minimo que decimos cumplir -- en
        # cantidades pequeñas, bajar 0.65g a 0.6g pierde un 8% del aporte de
        # ese alimento. Hacia arriba el error siempre juega a favor.
        gramos = math.ceil(x * 1000) / 10  # x en unidades de 100g -> 0.1g arriba
        if gramos > 0.1:
            gramos_por_alimento[a["nombre"]] = gramos
            kcal_total += a["energia"] * gramos / 100
            total_gramos += gramos
        elif x > 0:
            # el solver le dio una cantidad ridicula (<0.1g)
            descartados.append(a["nombre"])

    # IMPORTANTE: no se puede descartar en silencio. El LP contaba con esas
    # cantidades minusculas para cumplir los nutrientes (p.ej. 0.05g de
    # higado aportando la vitamina A), asi que si las tiramos sin mas, el
    # menu que devolvemos YA NO cumple lo que decimos que cumple. La unica
    # salida correcta es rehacer el calculo sin esos alimentos, para que el
    # solver reparta esa carga entre los que si se quedan.
    if descartados and len(alimentos_elegidos) - len(descartados) >= 4:
        restantes = [a for a in alimentos_elegidos if a["nombre"] not in descartados]
        reintento = _resolver_lp(restantes, der_objetivo, etapa_requisitos, forzar_presencia)
        if reintento["factible"]:
            return reintento
        # si sin ellos no hay solucion, es que de verdad hacian falta:
        # se devuelven con una cantidad minima pesable en vez de tirarlos
        for nombre in descartados:
            a = next(x for x in alimentos_elegidos if x["nombre"] == nombre)
            gramos_por_alimento[nombre] = 0.2
            kcal_total += a["energia"] * 0.2 / 100
            total_gramos += 0.2

    return {
        "factible": True,
        "gramos": gramos_por_alimento,
        "kcal_total": round(kcal_total, 1),
        "total_gramos": round(total_gramos, 1),
    }


if __name__ == "__main__":
    from especies import cargar_alimentos

    alimentos = cargar_alimentos()
    por_nombre = {a["nombre"]: a for a in alimentos}

    # CASO REAL: menu de Cairo, sin pollo ni pavo (su alergia real)
    elegidos = [
        por_nombre["Ternera con grasa"],       # Carne muscular
        por_nombre["Costillas de ternera"],    # Hueso carnoso
        por_nombre["Corazón de vaca"],         # Viscera/carne
        por_nombre["Hígado de vaca"],          # Higado
        por_nombre["Calabaza"],                # Verdura
    ]

    print("=== OPTIMIZANDO MENU REAL DE CAIRO (sin pollo ni pavo, DER 1120kcal) ===")
    resultado = optimizar_menu(elegidos, der_objetivo=1120, etapa_requisitos="CachorroCrecimiento")

    if resultado["factible"]:
        print(f"\n✅ FACTIBLE — {resultado['total_gramos']}g totales, {resultado['kcal_total']}kcal")
        for nombre, gramos in resultado["gramos"].items():
            print(f"   {nombre}: {gramos}g")
    else:
        print(f"\n❌ NO FACTIBLE: {resultado['motivo']}")
        print(f"   (detalle tecnico: {resultado['detalle_tecnico']})")


# =====================================================================
# CAPA DE USABILIDAD: menus con pocos alimentos
# =====================================================================
# El LP puro reparte los gramos entre TODOS los candidatos que le vengan
# bien, y salian menus de 13-14 alimentos distintos: nutricionalmente
# correctos, pero nada practicos de comprar, preparar y pesar cada dia.
# Un LP no puede limitar "el numero de alimentos distintos" directamente
# (eso requeriria programacion entera), asi que se resuelve por pasos:
# se calcula, se quitan los alimentos que salen en cantidades
# insignificantes o los mas pequeños, y se vuelve a calcular solo con el
# resto. Se repite hasta llegar al numero objetivo de alimentos, y si en
# algun paso deja de haber solucion, se devuelve el ultimo menu valido.

MAX_ALIMENTOS_MENU = 8   # objetivo practico (ver nota: el LP suele necesitar ~11)
GRAMOS_INSIGNIFICANTES = 3.0  # por debajo de esto no merece la pena pesarlo


def optimizar_menu(alimentos_elegidos: list, der_objetivo: float, etapa_requisitos: str = "Adulto",
                    forzar_presencia: list = None, max_alimentos: int = MAX_ALIMENTOS_MENU):
    """
    Calcula el menu y ademas lo simplifica para que sea practico de usar:
    pocos alimentos y sin cantidades ridiculas de pesar.
    """
    resultado = _resolver_lp(alimentos_elegidos, der_objetivo, etapa_requisitos, forzar_presencia)
    if not resultado["factible"]:
        return resultado

    # los que el usuario ha pedido expresamente no se pueden podar nunca
    protegidos = set(forzar_presencia or [])
    candidatos = list(alimentos_elegidos)
    mejor = resultado

    for _ in range(40):  # tope de seguridad, en la practica bastan pocas vueltas
        usados = {n: g for n, g in mejor["gramos"].items() if g > 0.01}

        # 1) quitar lo que sale en cantidad insignificante (no se puede ni pesar)
        insignificantes = [n for n, g in usados.items()
                           if g < GRAMOS_INSIGNIFICANTES and n not in protegidos]
        # 2) si ya no hay insignificantes pero siguen sobrando alimentos,
        #    quitar el mas pequeño de todos
        if insignificantes:
            a_quitar = insignificantes
        elif len(usados) > max_alimentos:
            candidato_menor = min(
                ((n, g) for n, g in usados.items() if n not in protegidos),
                key=lambda x: x[1], default=None)
            if candidato_menor is None:
                break
            a_quitar = [candidato_menor[0]]
        else:
            break  # ya esta simplificado

        nuevos_candidatos = [a for a in candidatos if a["nombre"] not in a_quitar]
        # nunca dejar el menu sin alimentos suficientes para cuadrarlo
        if len(nuevos_candidatos) < 4:
            break

        intento = _resolver_lp(nuevos_candidatos, der_objetivo, etapa_requisitos, forzar_presencia)
        if not intento["factible"]:
            # quitar ese alimento rompe el menu -> nos quedamos con el ultimo bueno
            break
        candidatos = nuevos_candidatos
        mejor = intento

    # NO se limpian aqui los restos pequeños: el bucle de arriba ya intenta
    # quitarlos recalculando, y si alguno ha sobrevivido es porque el menu
    # NO cuadra sin el. Tirarlo ahora dejaria un menu que incumple los
    # nutrientes que decimos que cumple (mismo error que ya se corrigio en
    # _resolver_lp). Si una cantidad es dificil de pesar, eso se resuelve
    # avisando en la app, no falseando el calculo.
    return mejor
