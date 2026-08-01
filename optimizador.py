"""
CANISLAB - Optimizador matematico de menus (punto 1 y 6 del plan de backend)

Dado: DER objetivo, una lista de alimentos elegidos (uno por categoria, tipico
de modo Automatico), y las tablas de requerimientos FEDIAF, calcula los gramos
exactos de cada alimento para que:
  - Las kcal cuadren EXACTO con el DER (restriccion de igualdad)
  - Todos los nutrientes minimos se cumplan (restriccion >=)
  - Los nutrientes con maximo no se pasen (restriccion <=)
  - Se minimice el total de gramos (dieta lo mas eficiente posible, sin
    "rellenar" con más comida de la necesaria)

Si no existe combinacion posible (punto 6 del plan), lo detecta y devuelve
un mensaje claro en vez de fallar en silencio.
"""
import json
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
    "Vísceras": 1.5,
    "Hígado": 2.5,
    "Pescados y mariscos": 3.0,
    "Verduras y frutas": 6.0,
    "Extras": 5.0,
    "Suplementos comerciales": 8.0,
}


def optimizar_menu(alimentos_elegidos: list, der_objetivo: float, etapa_requisitos: str = "Adulto"):
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

    for req in requerimientos:
        nutriente_key = MAPA_REQUISITO_A_NUTRIENTE.get(req["nutriente"])
        if nutriente_key is None:
            continue  # ratio Ca:P y casos especiales se tratan aparte

        minimo = _valor_o_none(req.get(f"min{etapa_requisitos}"))
        maximo = _valor_o_none(req.get(f"max{etapa_requisitos}"))

        valores = [a["nutrientes"].get(nutriente_key, 0) for a in alimentos_elegidos]

        if minimo is not None and minimo > 0:
            # -sum(valor_i * x_i) <= -minimo  ==  sum(valor_i * x_i) >= minimo
            A_ub.append([-v for v in valores])
            b_ub.append(-minimo)
            detalles_restricciones.append(f"min {req['nutriente']} >= {minimo}{req['unidad']}")

        if maximo is not None and maximo > 0:
            A_ub.append(valores)
            b_ub.append(maximo)
            detalles_restricciones.append(f"max {req['nutriente']} <= {maximo}{req['unidad']}")

    # MINIMO garantizado de verdura y de visceras (no solo higado) -- no es
    # una regla de porcentaje artificial, es una garantia razonada de que la
    # dieta tenga fibra vegetal (transito intestinal) y variedad de organos
    # (nutrientes que el listado de 27 no recoge del todo), aunque los 27
    # nutrientes trackeados ya se puedan cumplir sin ellos matematicamente.
    idx_verduras = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Verduras y frutas"]
    if idx_verduras:
        fila = [0.0] * n
        for i in idx_verduras:
            fila[i] = -1.0  # -suma(x_i) <= -minimo_en_unidades_100g
        A_ub.append(fila)
        b_ub.append(-0.5)  # minimo 50g de verdura/fruta en total

    idx_visceras_no_higado = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Vísceras"]
    if idx_visceras_no_higado:
        fila = [0.0] * n
        for i in idx_visceras_no_higado:
            fila[i] = -1.0
        A_ub.append(fila)
        b_ub.append(-0.3)  # minimo 30g de visceras (corazon/riñon/pulmon...) en total

    # MISMA LOGICA para Carne muscular: sin esto, si otro alimento (ej. un
    # hueso con mucho calcio) resuelve todo por si solo, la carne muscular
    # se queda casi a cero -- razonable poner un minimo real de presencia
    idx_carne = [i for i, a in enumerate(alimentos_elegidos) if a["categoria"] == "Carne muscular"]
    if idx_carne:
        fila = [0.0] * n
        for i in idx_carne:
            fila[i] = -1.0
        A_ub.append(fila)
        b_ub.append(-1.5)  # minimo 150g de carne muscular en total

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
    for a, x in zip(alimentos_elegidos, resultado.x):
        gramos = round(x * 100, 1)  # x esta en unidades de 100g
        if gramos > 0.1:
            gramos_por_alimento[a["nombre"]] = gramos
            kcal_total += a["energia"] * gramos / 100
            total_gramos += gramos

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
