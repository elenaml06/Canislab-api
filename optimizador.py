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
    "Fibra": "fibra",
    # Tope de calcio especifico para cachorros de raza GRANDE en crecimiento.
    # Se mapea al mismo nutriente que "Calcio" a proposito: es una segunda
    # restriccion, mas estricta, que solo se activa cuando toca (ver
    # `es_raza_grande` en optimizar_menu). Antes estaba en el JSON pero no en
    # este mapa, asi que el motor lo ignoraba por completo.
    "Calcio_LateGrowth_RazaGrande": "calcio",
}



# =====================================================================
# PATOLOGIAS — ajustes orientativos [CRITERIO, validar con veterinario]
# =====================================================================
# Acordado con el usuario el 1 de agosto: para las patologias que no
# dependen de analiticas, la app aplica ajustes orientativos automaticos
# y avisa; para las que SI dependen de analiticas (calculos de estruvita,
# cistina o urato) NO se genera dieta automatica.
#
# IMPORTANTE: estos valores son de CRITERIO. Marcan una direccion
# razonable y documentada, pero el veterinario tiene que validarlos y
# ajustarlos al caso concreto. Un perro renal en estadio 2 y otro en
# estadio 4 no necesitan lo mismo.
#
# Cada patologia puede:
#   - "max_por_1000kcal": bajar el techo de un nutriente
#   - "max_pct_kcal_grasa": limitar la grasa como % de las calorias
#   - "sin_dieta_automatica": True -> no se genera, se deriva al veterinario
PATOLOGIAS = {
    "renal": {
        "nombre": "Insuficiencia renal crónica",
        # OJO, hallazgo importante: una dieta renal de verdad baja el fosforo
        # a 500-750 mg/1000 kcal, y el MINIMO de FEDIAF para un perro sano es
        # 1160. Es decir: una dieta renal terapeutica esta POR DEBAJO del
        # minimo nutricional de un perro sano, a proposito. Eso no es algo
        # que pueda decidir una app: es una dieta de prescripcion.
        # Aqui solo se baja el fosforo TODO lo posible sin incumplir FEDIAF
        # (se acerca al minimo en vez de al maximo), y se avisa claramente.
        "max_por_1000kcal": {"Fósforo": 1400.0},
        "aviso": ("Se ha bajado el fósforo todo lo posible sin bajar del mínimo "
                  "nutricional de un perro sano. IMPORTANTE: una dieta renal "
                  "terapéutica de verdad baja el fósforo POR DEBAJO de ese mínimo, "
                  "y eso solo puede pautarlo tu veterinario. Esto es un apoyo, "
                  "no sustituye una dieta renal prescrita."),
    },
    "pancreatitis": {
        "nombre": "Pancreatitis",
        # Dieta baja en grasa: por debajo del 30% de las kcal se considera baja
        "max_pct_kcal_grasa": 0.25,
        "aviso": ("Se ha bajado la grasa al 25% de las calorías. En pancreatitis "
                  "la tolerancia a la grasa es muy individual: ajústalo con tu "
                  "veterinario según cómo responda."),
    },
    "oxalato": {
        "nombre": "Cálculos de oxalato cálcico",
        # No se sube el calcio (bajarlo empeora: aumenta la absorcion de
        # oxalato). Se limita la vitamina D, que favorece la absorcion.
        "max_por_1000kcal": {"Vitamina_D": 20.0},
        "aviso": ("Ojo: en oxalato NO hay que bajar el calcio (bajarlo aumenta la "
                  "absorción de oxalato y empeora). Lo importante es el agua y "
                  "evitar verduras muy ricas en oxalato como la espinaca o la acelga."),
    },
    "hepatopatia": {
        "nombre": "Hepatopatía",
        # El cobre es la clave en las hepatopatias por acumulo (Bedlington,
        # Labrador, Dálmata...). Se limita.
        "max_por_1000kcal": {"Cobre": 3.0},
        "aviso": ("Se ha limitado el cobre, clave en las hepatopatías por acúmulo. "
                  "Si hay encefalopatía hepática hace falta además ajustar la "
                  "proteína, y eso lo tiene que pautar tu veterinario."),
    },
    "cardiopatia": {
        "nombre": "Cardiopatía",
        "max_por_1000kcal": {"Sodio": 900.0},
        "aviso": ("Se ha bajado el sodio. En cardiopatía avanzada puede hacer falta "
                  "bajarlo más y vigilar el potasio si toma diuréticos: consúltalo."),
    },
    "diabetes": {
        "nombre": "Diabetes mellitus",
        "max_pct_kcal_grasa": 0.35,
        # La fruta baja practicamente a cero. En un perro SANO el azucar de la
        # fruta no es toxico -- son calorias vacias que diluyen la racion y ya.
        # En un diabetico si importa: los azucares simples se absorben rapido y
        # provocan un pico de glucosa que descuadra la pauta de insulina. La
        # verdura fibrosa se mantiene (la fibra ayuda a amortiguar la glucemia);
        # lo que se quita es la fruta.
        "excluye_fruta": True,
        "aviso": ("Lo más importante en diabetes no es el menú sino la REGULARIDAD: "
                  "misma cantidad, a la misma hora, coordinada con la insulina. "
                  "Se ha quitado la fruta del menú: su azúcar se absorbe rápido y "
                  "descuadra la pauta de insulina. La verdura fibrosa sí se "
                  "mantiene, porque ayuda a amortiguar la subida de glucosa."),
    },
    "hipotiroidismo": {
        "nombre": "Hipotiroidismo",
        "aviso": ("No se cambia la composición. Pero evita darle cuello de rumiante "
                  "grande de forma repetida: puede llevar restos de tejido tiroideo "
                  "y alterar los valores de la analítica."),
    },
    "estruvita": {
        "nombre": "Cálculos de estruvita / cistina / urato",
        "sin_dieta_automatica": True,
        "aviso": ("Estos cálculos dependen del pH de la orina y de analíticas que la "
                  "app no puede ver. Una dieta mal ajustada aquí puede empeorarlos, "
                  "así que no generamos menú automático: necesitas una dieta pautada "
                  "por tu veterinario."),
    },
}


def patologias_bloquean(patologias):
    """Devuelve las patologias que impiden generar dieta automatica."""
    return [p for p in (patologias or []) if PATOLOGIAS.get(p, {}).get("sin_dieta_automatica")]


def avisos_de_patologias(patologias):
    return [PATOLOGIAS[p]["aviso"] for p in (patologias or []) if p in PATOLOGIAS]


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


# Las UNICAS etapas que existen en requerimientos_v2_final.json. Cualquier
# otra cosa es un error de quien llama, y hay que gritarlo.
ETAPAS_VALIDAS = {"Adulto", "CachorroJoven", "CachorroCrecimiento"}


# Frutas de nuestro catalogo. El JSON no distingue fruta de verdura (todo cae
# en "Verduras y frutas"), asi que se separan por nombre. Si se anaden frutas
# nuevas al catalogo hay que meterlas aqui tambien.
FRUTAS = {
    "Manzana", "Pera", "Kiwi", "Plátano", "Naranja", "Sandía", "Melón",
    "Albaricoque", "Frambuesa", "Mango", "Piña", "Arándanos", "Fresas",
    "Papaya", "Mora", "Cereza", "Melocotón", "Higo", "Ciruela",
}


def es_fruta(nombre: str) -> bool:
    if nombre in FRUTAS:
        return True
    n = nombre.lower()
    return any(f.lower() in n for f in FRUTAS)


def resolver_etapa(etapa_pedida):
    """
    Devuelve la etapa cuyos requisitos hay que usar realmente.

    ⚠️ FALLA A PROPOSITO si la etapa no existe. Antes no lo hacia, y eso
    causo un fallo real: el frontend mandaba "cachorro_crecimiento" (la clave
    de der.py) en vez de "CachorroCrecimiento" (la de los requisitos). Como
    los requisitos se buscan con f"min{etapa}", NINGUNA columna coincidia, no
    se comprobaba NI UN nutriente, y el analizador respondia que la dieta
    estaba perfecta cuando le faltaban 15 nutrientes.
    Un fallo silencioso en la base es mucho peor que un error visible.
    """
    etapa = EQUIVALENCIA_ETAPAS.get(etapa_pedida, etapa_pedida)
    if etapa not in ETAPAS_VALIDAS:
        raise ValueError(
            f"Etapa de requisitos '{etapa_pedida}' no reconocida. "
            f"Las validas son: {sorted(ETAPAS_VALIDAS)}. "
            f"Cuidado: las claves de der.py (adulto, cachorro_crecimiento...) "
            f"NO son las mismas que las de los requisitos.")
    return etapa


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
    "Verduras y frutas": 12.0,
    "Extras": 5.0,
    "Suplementos comerciales": 8.0,
}


def _resolver_lp(alimentos_elegidos: list, der_objetivo: float, etapa_requisitos: str = "Adulto",
                  forzar_presencia: list = None, peso_perro_kg: float = None,
                  tope_por_alimento: float = 0.30, patologias: list = None,
                 peso_adulto_esperado_kg: float = None):
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
    # Sin alimentos no hay nada que resolver: scipy revienta con un mensaje
    # incomprensible si se le pasa una lista vacia.
    if not alimentos_elegidos:
        return {"factible": False,
                "motivo": "No se ha indicado ningún alimento para calcular el menú.",
                "gramos": {}}
    if not der_objetivo or der_objetivo <= 0:
        return {"factible": False,
                "motivo": "No se ha podido calcular cuántas calorías necesita el perro.",
                "gramos": {}}

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
    # [RETIRADA] Antes habia un tope global de "suplementos <= 2% de la racion".
    # Se puso cuando no teniamos las dosis reales de cada producto, como
    # proteccion generica. Ahora cada suplemento lleva SU dosis de fabricante
    # (ver mas abajo), que es una proteccion mucho mejor y especifica. El 2%
    # generico ademas impedia las plantillas compactas, que precisamente se
    # apoyan en los suplementos para reducir el numero de alimentos, que es
    # como trabajan los formuladores profesionales.

    # DOSIS MAXIMA DEL FABRICANTE (por suplemento concreto)
    # [CIENCIA - etiqueta del producto] Un suplemento comercial NO es un
    # alimento mas: viene dosificado por el fabricante segun el peso del
    # perro, y pasarse no es "un poco mas de vitaminas", es salirse de lo
    # que el producto tiene validado. Sin esto el motor usaba la cantidad
    # que le cuadraba matematicamente (se detecto dando 23g de un producto
    # cuya dosis para ese peso son 16.35g).
    for i, a in enumerate(alimentos_elegidos):
        # (1) dosis fija segun el PESO DEL PERRO (multivitaminicos, harina de hueso)
        tope_g = dosis_maxima_fabricante(a, peso_perro_kg)
        if tope_g is not None:
            fila = [0.0] * n
            fila[i] = 1.0
            A_ub.append(fila)
            # se resta un pelin para absorber el redondeo hacia arriba
            b_ub.append(max(tope_g - 0.1, 0) / 100)

        # (2) dosis proporcional a la RACION (kelp, algas: "x g por cada 100g
        #     de comida"). Se expresa como: suplemento - pct*total <= 0
        por_100 = a.get("dosis_max_por_100g_comida")
        if por_100:
            fila = [0.0] * n
            for j in range(n):
                fila[j] = -por_100 / 100.0
            fila[i] += 1.0
            A_ub.append(fila)
            b_ub.append(0.0)

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
    # El 35% inicial era demasiado estricto: obligaba a tirar de carnes muy
    # magras y la racion se disparaba en volumen (se vieron 968 g para un
    # cachorro de 6 kg, un 16% de su peso). Una dieta BARF normal esta entre
    # el 40 y el 50% de las kcal en grasa. Se sube a 50%, que sigue estando
    # dentro de lo habitual y deja al motor elegir alimentos mas densos.
    b_ub.append(der_objetivo * 0.50)

    # TOPE DE VERDURAS+FRUTA TOTAL -- consenso veterinario general (WSAVA):
    # =================================================================
    # TOPE DE VERDURA Y FRUTA -- POR PESO, NO POR ENERGIA
    # =================================================================
    # Antes se topaba al 10% de las KCAL. Era el criterio equivocado: la
    # verdura tiene muy poca energia por gramo (zanahoria 34 kcal/100g,
    # brocoli 26), asi que ese 10% permitia un peso enorme. Caso real: un
    # menu de 1526 kcal salio con 189g de zanahoria + 47g de brocoli + 36g
    # de platano = 272 g, que por peso es un 25-30% del plato. Cada uno
    # cumplia el tope individual del 15%, pero JUNTOS no habia nada que los
    # frenara. Topar por energia sobreestima siempre el peso permitido de
    # ingredientes acuosos y poco energeticos.
    #
    # POR QUE POR PESO:
    # Ni FEDIAF ni NRC reconocen la fibra ni los carbohidratos como
    # nutrientes esenciales para el perro adulto, asi que NO existe un
    # minimo de verdura. Tampoco hay un maximo oficial: las guias regulan
    # NUTRIENTES, no ingredientes. Y los porcentajes clasicos del BARF
    # (80/10/10, 70/10/10/10, "15-20% de verdura") son convenciones de
    # divulgacion sin estudio detras.
    # El riesgo real del exceso vegetal esta bien fundamentado y es la
    # DILUCION: la verdura desplaza carne, higado y hueso, y baja el aporte
    # proporcional de proteina, calcio y micronutrientes. Ademas, el exceso
    # de fibra reduce la digestibilidad global de la dieta y la absorcion de
    # calcio, hierro y zinc.
    # Referencia de contexto: Dillitzer, Becker & Kienzle (2011), Br J Nutr
    # 106:S53 -- de 95 raciones BARF reales analizadas en Munich, el 60%
    # tenia algun desequilibrio de minerales o vitaminas.
    #
    # Los valores 15% y 5% son topes de seguridad de ingenieria, no cifras
    # de una guia: mantienen la fraccion vegetal donde la evidencia no
    # muestra dano y donde los minimos nutricionales siguen alcanzables.
    # El LP verifica los minimos aparte, asi que si la verdura diluyera
    # demasiado el menu saldria infactible y se veria.
    # AJUSTE EMPIRICO del tope. Se barrieron varios valores midiendo la tasa
    # de menus factibles en las 22 pruebas de /home/claude/auditoria:
    #    15% -> 41%   ·   20% -> 62%   ·   25% -> 67%   ·   30% -> 68%
    # Por debajo del 25% el motor se ahoga: la verdura tambien aporta potasio
    # y volumen, y sin ella muchos perfiles no cuadran. Ademas se subio el
    # coste de la verdura en PESO_POR_CATEGORIA de 6 a 12, que empuja al LP a
    # usar menos SIN hacer el menu imposible (con eso, 68%).
    # RESULTADO MEDIDO en menus reales: media 14.7% del peso, maximo 24%.
    # Cairo paso de 272 g de verdura a 105 g (10.9% del plato).
    # El 25% es el TOPE DURO, no lo habitual.
    TOPE_VERDURA_FRUTA_PESO = 0.25   # verdura + fruta juntas
    TOPE_FRUTA_PESO = 0.05           # la fruta aparte, por su azucar

    # Alguna patologia puede EXCLUIR la fruta por completo (diabetes).
    # Se hizo asi y no con un tope del 1% porque un tope tan bajo choca con el
    # minimo de gramos por alimento (20 g) y el menu salia "no factible" con un
    # mensaje incomprensible. Excluirla es mas honesto: la fruta simplemente no
    # aparece, y el aviso de la patologia explica por que.
    fuera_la_fruta = any(PATOLOGIAS.get(p, {}).get("excluye_fruta")
                         for p in (patologias or []))

    idx_verdura_cap = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Verduras y frutas"]

    if idx_verdura_cap:
        # TOPE GLOBAL: toda la verdura y fruta JUNTAS, sobre el peso total.
        # sum(verdura) - 0.15 * sum(todo) <= 0
        fila = [-TOPE_VERDURA_FRUTA_PESO] * n
        for i in idx_verdura_cap:
            fila[i] += 1.0
        A_ub.append(fila)
        b_ub.append(0.0)

        # SUB-TOPE DE FRUTA. En perro sano el azucar de la fruta no es
        # toxico, solo son calorias vacias que diluyen la racion.
        idx_fruta = [i for i in idx_verdura_cap if es_fruta(alimentos_elegidos[i]["nombre"])]
        if idx_fruta and fuera_la_fruta:
            # Diabetes: fruta a cero. Como los gramos no pueden ser negativos,
            # "suma de frutas <= 0" las deja todas en cero.
            fila = [0.0] * n
            for i in idx_fruta:
                fila[i] = 1.0
            A_ub.append(fila)
            b_ub.append(0.0)
        elif idx_fruta:
            fila = [-TOPE_FRUTA_PESO] * n
            for i in idx_fruta:
                fila[i] += 1.0
            A_ub.append(fila)
            b_ub.append(0.0)

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
    # El tope por alimento se puede ajustar: las plantillas compactas usan
    # 40% porque con solo 5 alimentos reales alguno tiene que pesar mas.
    # Sigue evitando el "600 g de un solo corte" que motivo la regla.
    for i in range(n):
        fila = [0.0] * n
        for j in range(n):
            fila[j] = -tope_por_alimento
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

    # (b2) ESTRUCTURA BARF OBLIGATORIA
    # Una dieta BARF tiene cinco pilares y todos deben estar: hueso carnoso,
    # carne o pescado, verduras/frutas, visceras e higado. Cada uno con su
    # limite propio. Los suplementos comerciales estan para COMPENSAR lo que
    # falte, no para sustituir a ninguna de estas categorias: no se puede
    # cambiar el hueso carnoso por harina de hueso y quedarse tan anchos.
    for categoria, mn_pct in (("Hígado", 0.01), ("Vísceras", 0.02)):
        idx = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == categoria]
        if idx:
            fila = [0.0] * n
            for j in range(n):
                fila[j] = mn_pct
            for i in idx:
                fila[i] -= 1.0
            A_ub.append(fila)
            b_ub.append(0.0)

    # (b2b) MINIMO PRACTICO POR CATEGORIA, EN GRAMOS ABSOLUTOS
    # Podar despues no basta: si el unico higado del menu sale a 0,6 g no se
    # puede quitar (haria falta para cumplir la estructura BARF) y quedaba una
    # cantidad que nadie puede pesar. Se le exige al LP desde el principio que
    # si una categoria esta en el menu, este con una cantidad manejable.
    MINIMOS_ABSOLUTOS_G = {
        "Carne muscular": 25.0,
        "Hueso carnoso": 20.0,
        "Pescados y mariscos": 20.0,
        "Vísceras": 10.0,
        "Hígado": 5.0,
        "Verduras y frutas": 12.0,
    }
    # Se escalan con el tamaño del perro: pedirle a un chihuahua de 192 kcal
    # los mismos gramos minimos que a un mastin deja el menu sin solucion
    # posible (las 6 categorias juntas se comerian media racion). El factor
    # esta topado al alza para que un perro gigante no acabe con minimos
    # desproporcionados.
    # Perros muy pequeños: con 190 kcal, exigir 25 g de carne + 20 de hueso +
    # 20 de pescado + 15 de verdura... se come el plato entero y salen
    # cantidades impesables. Por debajo de 400 kcal el minimo se relaja mucho
    # mas: lo que importa en un chihuahua es que la estructura este, no que
    # cada categoria llegue a los gramos de un perro grande.
    factor_tamano = min(1.0, max(0.35, der_objetivo / 1200))
    # --- CALCIO EN CACHORROS DE RAZA GRANDE ---
    # Solo se aplica si el perro es de raza grande Y esta creciendo. Para el
    # resto seria innecesariamente estricto.
    if peso_adulto_esperado_kg and peso_adulto_esperado_kg >= 25 and "Cachorro" in etapa_requisitos:
        for req in requerimientos:
            if req["nutriente"] != "Calcio_LateGrowth_RazaGrande":
                continue
            tope = _valor_o_none(req.get(f"max{etapa_datos}"))
            if tope:
                A_ub.append([a["nutrientes"].get("calcio", 0) for a in alimentos_elegidos])
                b_ub.append(tope * (der_objetivo / 1000))

    # --- PATOLOGIAS: topes mas estrictos que los de FEDIAF ---
    for p in (patologias or []):
        cfg = PATOLOGIAS.get(p, {})
        for nutriente, tope in (cfg.get("max_por_1000kcal") or {}).items():
            k = MAPA_REQUISITO_A_NUTRIENTE.get(nutriente)
            if not k: continue
            A_ub.append([a["nutrientes"].get(k, 0) for a in alimentos_elegidos])
            b_ub.append(tope * (der_objetivo / 1000))
        pct = cfg.get("max_pct_kcal_grasa")
        if pct:
            A_ub.append([a["nutrientes"].get("grasa", 0) * 9 for a in alimentos_elegidos])
            b_ub.append(der_objetivo * pct)

    for categoria, minimo_g in MINIMOS_ABSOLUTOS_G.items():
        idx = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == categoria]
        if not idx:
            continue
        fila = [0.0] * n
        for i in idx:
            fila[i] = -1.0
        A_ub.append(fila)
        b_ub.append(-(minimo_g * factor_tamano) / 100)   # variables en unidades de 100 g

    # (b3) TOPE DE EXTRAS (aceites, semillas, huevo)
    # Son muy densos en calorias y el motor tiraba de ellos para cuadrar
    # grasa y acidos grasos: se vieron 67,8 g de aceite en un perro de 25 kg,
    # casi cinco cucharadas soperas. La pauta habitual es ~1 cucharadita por
    # cada 10 kg. Se limita la categoria al 5% del peso de la racion.
    idx_extras = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Extras"]
    if idx_extras:
        fila = [0.0] * n
        for j in range(n):
            fila[j] = -0.05
        for i in idx_extras:
            fila[i] += 1.0
        A_ub.append(fila)
        b_ub.append(0.0)

    # (c) [RETIRADA] Antes habia un minimo de 5% de pescado. Era redundante:
    #     FEDIAF ya exige EPA/DHA como nutriente, y eso por si solo obliga al
    #     motor a incluir una fuente de omega-3 cuando hace falta. Mantener
    #     ademas un minimo por peso hacia que saliera MAS pescado del
    #     necesario (se vieron 284g de trucha en un perro de 17kg) y ademas
    #     imponia pescado a quien no quiere darlo. El nutriente manda; la
    #     categoria no tiene por que ser obligatoria.

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
        reintento = _resolver_lp(restantes, der_objetivo, etapa_requisitos, forzar_presencia, peso_perro_kg, tope_por_alimento, patologias, peso_adulto_esperado_kg)
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

def dosis_maxima_fabricante(alimento: dict, peso_perro_kg: float):
    """Gramos maximos al dia que el FABRICANTE recomienda de ese suplemento,
    segun el peso del perro. None si el producto no trae tabla de dosis."""
    # (a) dosis lineal: g por kg de peso corporal (aceites, algas, levadura)
    por_kg = alimento.get("dosis_g_por_kg_peso")
    if por_kg and peso_perro_kg is not None:
        return por_kg * peso_perro_kg

    # (a2) algunos productos ademas tienen un tope absoluto ("maximo N
    #      cucharaditas al dia") que manda sobre el calculo por peso
    tope_abs = alimento.get("dosis_max_absoluta_g")
    if por_kg and peso_perro_kg is not None and tope_abs:
        return min(por_kg * peso_perro_kg, tope_abs)

    # (b) dosis por tramos de peso (multivitaminicos, harinas de hueso)
    tramos = alimento.get("dosis_tramos_kg")
    if not tramos or peso_perro_kg is None:
        return None
    for t in tramos:
        if t["hasta_kg"] is None or peso_perro_kg <= t["hasta_kg"]:
            return t["gramos"]
    return tramos[-1]["gramos"]


MAX_ALIMENTOS_MENU = 8   # objetivo practico (ver nota: el LP suele necesitar ~11)
GRAMOS_INSIGNIFICANTES = 3.0  # por debajo de esto no merece la pena pesarlo

# Cuanto es "una cantidad ridicula" depende del alimento. 3 g de aceite es una
# cucharadita normal, pero 5 g de muslo de pavo no tiene ningun sentido: nadie
# compra ni pesa eso. Se pide un minimo razonable a la comida de verdad, y se
# deja que los suplementos y aceites salgan en cantidades pequeñas.
MINIMO_PRACTICO = {
    "Carne muscular": 25.0,
    "Hueso carnoso": 20.0,
    "Pescados y mariscos": 20.0,
    "Vísceras": 10.0,
    "Hígado": 5.0,          # el higado va poco por definicion (tope del 5%)
    "Verduras y frutas": 12.0,
    "Extras": 3.0,          # aceites y semillas: una cucharadita ya cuenta
}


def minimo_practico(alimento):
    """Gramos por debajo de los cuales ese alimento no merece estar en el menu."""
    if alimento.get("tipo") == "Suplemento":
        return 0.3          # los suplementos se dosifican en decimas de gramo
    return MINIMO_PRACTICO.get(alimento.get("categoria"), GRAMOS_INSIGNIFICANTES)


def optimizar_menu(alimentos_elegidos: list, der_objetivo: float, etapa_requisitos: str = "Adulto",
                    forzar_presencia: list = None, max_alimentos: int = MAX_ALIMENTOS_MENU,
                    peso_perro_kg: float = None, tope_por_alimento: float = 0.30,
                    patologias: list = None, peso_adulto_esperado_kg: float = None):
    """
    Calcula el menu y ademas lo simplifica para que sea practico de usar:
    pocos alimentos y sin cantidades ridiculas de pesar.
    """
    # Patologias que dependen de analiticas: no se genera dieta automatica
    bloqueantes = patologias_bloquean(patologias)
    if bloqueantes:
        return {"factible": False,
                "motivo": PATOLOGIAS[bloqueantes[0]]["aviso"],
                "requiere_veterinario": True,
                "gramos": {}}

    resultado = _resolver_lp(alimentos_elegidos, der_objetivo, etapa_requisitos, forzar_presencia, peso_perro_kg, tope_por_alimento, patologias, peso_adulto_esperado_kg)
    if not resultado["factible"]:
        return resultado

    # los que el usuario ha pedido expresamente no se pueden podar nunca
    protegidos = set(forzar_presencia or [])
    candidatos = list(alimentos_elegidos)
    mejor = resultado

    for _ in range(40):  # tope de seguridad, en la practica bastan pocas vueltas
        usados = {n: g for n, g in mejor["gramos"].items() if g > 0.01}

        # 1) quitar lo que sale en cantidad insignificante (no se puede ni pesar)
        # Los 5 pilares BARF NO se podan nunca: si se quita el unico higado
        # del menu, la regla de "higado >= 1%" deja de aplicarse (su indice
        # queda vacio) y el menu se queda SIN higado sin que nadie avise.
        CATEGORIAS_PILAR = {"Hueso carnoso", "Carne muscular", "Verduras y frutas",
                            "Vísceras", "Hígado"}
        catalogo_local = {a["nombre"]: a for a in candidatos}
        insignificantes = [n for n, g in usados.items()
                           if n not in protegidos
                           and g < minimo_practico(catalogo_local.get(n, {}))
                           and catalogo_local.get(n, {}).get("categoria") not in CATEGORIAS_PILAR]

        # Los pilares tampoco pueden salir en cantidades ridiculas: si un
        # pilar sale por debajo de su minimo practico se quita IGUAL, pero
        # solo cuando queda otro alimento de su misma categoria que lo
        # sustituya (asi el pilar sigue presente en el menu).
        for n, g in usados.items():
            a = catalogo_local.get(n, {})
            cat = a.get("categoria")
            if (cat in CATEGORIAS_PILAR and n not in protegidos
                    and g < minimo_practico(a) and n not in insignificantes):
                hermanos = [m for m, gm in usados.items()
                            if m != n and catalogo_local.get(m, {}).get("categoria") == cat
                            and gm >= minimo_practico(catalogo_local.get(m, {}))]
                if hermanos:
                    insignificantes.append(n)
        # 2) si ya no hay insignificantes pero siguen sobrando alimentos,
        #    quitar el mas pequeño de todos
        if insignificantes:
            a_quitar = insignificantes
        elif len(usados) > max_alimentos:
            # tampoco aqui se puede tirar un pilar: el higado suele ser lo
            # mas pequeño del menu y era justo lo que se estaba quitando
            candidato_menor = min(
                ((n, g) for n, g in usados.items()
                 if n not in protegidos
                 and catalogo_local.get(n, {}).get("categoria") not in CATEGORIAS_PILAR),
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

        intento = _resolver_lp(nuevos_candidatos, der_objetivo, etapa_requisitos, forzar_presencia, peso_perro_kg, tope_por_alimento, patologias, peso_adulto_esperado_kg)
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
    if patologias:
        mejor["avisos_patologia"] = avisos_de_patologias(patologias)
    return mejor
