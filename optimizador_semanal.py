"""
CANISLAB - Optimizador SEMANAL (cuando ya hay rotacion real entre varios menus)

Principio ya acordado: kcal siempre EXACTAS por menu/dia. El resto de los
27 nutrientes se compensan a nivel SEMANAL, sumando entre los distintos
menus de la rotacion (no cada menu individual al 100%).

Este modulo se activa cuando transicion.nivel_indicador_nutrientes() dice
"semana" en vez de "menu" (es decir, cuando ya se ha rotado por todos los
menus elegidos al menos una vez).
"""
import sys
sys.path.insert(0, '.')
from scipy.optimize import linprog
from optimizador import cargar_requerimientos, MAPA_REQUISITO_A_NUTRIENTE, _valor_o_none, PESO_POR_CATEGORIA


def optimizar_semana(menus: list, der_objetivo: float, etapa_requisitos: str = "Adulto"):
    """
    menus: lista de dicts, uno por cada menu de la rotacion:
        {"nombre": "Menú 1", "dias": 3, "alimentos": [lista de alimentos candidatos]}
    der_objetivo: kcal EXACTAS que cada menu individual debe cuadrar cada dia
    etapa_requisitos: sufijo de requerimientos_v2_final.json

    Optimiza TODOS los menus a la vez: cada menu cuadra sus kcal exactas
    por separado, pero los 27 nutrientes se comprueban en el TOTAL SEMANAL
    (cada menu pesado por sus dias de uso esa semana).

    Devuelve dict con "factible", y si lo es, "menus" (gramos por alimento
    de cada menu por separado) + "total_semanal_por_nutriente" para revisar.
    """
    requerimientos = cargar_requerimientos()

    # variables: una x_i por cada (menu, alimento) -- todas juntas en un solo vector
    todas_las_variables = []  # lista de (indice_menu, alimento_dict)
    for idx_menu, menu in enumerate(menus):
        for alimento in menu["alimentos"]:
            todas_las_variables.append((idx_menu, alimento))
    n = len(todas_las_variables)

    c = [PESO_POR_CATEGORIA.get(a["categoria"], 1.0) for (_, a) in todas_las_variables]

    A_eq, b_eq = [], []
    # 1) cada menu individual cuadra sus kcal EXACTAS (una restriccion de igualdad por menu)
    for idx_menu, menu in enumerate(menus):
        fila = [0.0] * n
        for j, (im, a) in enumerate(todas_las_variables):
            if im == idx_menu:
                fila[j] = a["energia"]
        A_eq.append(fila)
        b_eq.append(der_objetivo)

    A_ub, b_ub = [], []
    # 2) cada nutriente se comprueba en el TOTAL SEMANAL: suma de
    #    (dias_del_menu * nutriente_aportado_ese_dia) a lo largo de los 7 dias
    dias_totales = sum(m["dias"] for m in menus)
    for req in requerimientos:
        key = MAPA_REQUISITO_A_NUTRIENTE.get(req["nutriente"])
        if key is None:
            continue
        minimo = _valor_o_none(req.get(f"min{etapa_requisitos}"))
        maximo = _valor_o_none(req.get(f"max{etapa_requisitos}"))

        fila = [0.0] * n
        for j, (im, a) in enumerate(todas_las_variables):
            dias_ese_menu = menus[im]["dias"]
            fila[j] = a["nutrientes"].get(key, 0) * dias_ese_menu

        if minimo is not None and minimo > 0:
            A_ub.append([-v for v in fila])
            b_ub.append(-minimo * dias_totales)
        if maximo is not None and maximo > 0:
            A_ub.append(fila)
            b_ub.append(maximo * dias_totales)

    # MINIMO garantizado de verdura y de visceras a nivel SEMANAL (fibra y
    # variedad de organos a lo largo de la semana completa)
    idx_verduras = [j for j, (im, a) in enumerate(todas_las_variables) if a["categoria"] == "Verduras y frutas"]
    if idx_verduras:
        fila = [0.0] * n
        for j in idx_verduras:
            im = todas_las_variables[j][0]
            fila[j] = -menus[im]["dias"]
        A_ub.append(fila)
        b_ub.append(-0.5 * dias_totales)  # 50g/dia de media a lo largo de toda la semana

    idx_visceras = [j for j, (im, a) in enumerate(todas_las_variables) if a["categoria"] == "Vísceras"]
    if idx_visceras:
        fila = [0.0] * n
        for j in idx_visceras:
            im = todas_las_variables[j][0]
            fila[j] = -menus[im]["dias"]
        A_ub.append(fila)
        b_ub.append(-0.3 * dias_totales)  # 30g/dia de media a lo largo de toda la semana

    # MINIMO pequeño de CADA categoria core EN CADA MENU INDIVIDUAL (no solo
    # a nivel semanal) -- para que ningun menu sea literalmente "dos
    # ingredientes sueltos". No exige que sea completo, solo que tenga un
    # poco de variedad interna. Solo se aplica si esa categoria tiene algun
    # candidato disponible en ese menu concreto.
    CATEGORIAS_CORE_MINIMO = {
        "Carne muscular": 0.10,   # 10g minimo por menu si hay candidato de esa categoria
        "Hueso carnoso": 0.10,
        "Vísceras": 0.05,
        "Hígado": 0.05,
        "Verduras y frutas": 0.10,
    }
    for idx_menu, menu in enumerate(menus):
        for categoria, minimo_g in CATEGORIAS_CORE_MINIMO.items():
            idx_en_este_menu = [
                j for j, (im, a) in enumerate(todas_las_variables)
                if im == idx_menu and a["categoria"] == categoria
            ]
            if idx_en_este_menu:
                fila = [0.0] * n
                for j in idx_en_este_menu:
                    fila[j] = -1.0
                A_ub.append(fila)
                b_ub.append(-minimo_g)

    bounds = [(0, None) for _ in range(n)]
    resultado = linprog(c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds, method="highs")

    if not resultado.success:
        return {
            "factible": False,
            "motivo": (
                "No encontramos una combinación semanal que cumpla todos los nutrientes "
                "sumando los menús de la rotación. Prueba a cambiar algún alimento o añadir "
                "un menú más a la rotación."
            ),
        }

    menus_resultado = [{"nombre": m["nombre"], "dias": m["dias"], "gramos": {}, "kcal_total": 0} for m in menus]
    for (im, a), x in zip(todas_las_variables, resultado.x):
        gramos = round(x * 100, 1)
        if gramos > 0.1:
            menus_resultado[im]["gramos"][a["nombre"]] = gramos
            menus_resultado[im]["kcal_total"] += a["energia"] * gramos / 100

    return {"factible": True, "menus": menus_resultado}


if __name__ == "__main__":
    from especies import cargar_alimentos, filtrar_alimentos_disponibles

    alimentos = cargar_alimentos()
    disponibles = filtrar_alimentos_disponibles(alimentos, {"Pollo", "Pavo"})
    por_nombre = {a["nombre"]: a for a in disponibles}

    def candidatos(nombres):
        return [por_nombre[n] for n in nombres if n in por_nombre]

    # 3 menus reales de Cairo, ya en rotacion (transicion completada)
    menus = [
        {"nombre": "Menú 1", "dias": 3, "alimentos": candidatos([
            "Ternera con grasa", "Cuello de ternera", "Hígado de vaca",
            "Espinaca", "Mejillón", "Aceite de girasol", "Sonrisa de Diez Kelp",
        ])},
        {"nombre": "Menú 2", "dias": 2, "alimentos": candidatos([
            "Conejo", "Costillas de cordero", "Riñón de ternera",
            "Calabaza", "Sardina", "Aceite de girasol",
        ])},
        {"nombre": "Menú 3", "dias": 2, "alimentos": candidatos([
            "Ternera solomillo sin grasa", "Costillas de ternera", "Pulmón de ternera",
            "Zanahoria", "Salmón", "Sonrisa de Diez Kelp",
        ])},
    ]

    print("=== ROTACIÓN SEMANAL DE CAIRO (3 menús, 7 días, ya en rotación real) ===\n")
    resultado = optimizar_semana(menus, der_objetivo=1120, etapa_requisitos="CachorroCrecimiento")

    if resultado["factible"]:
        print("✅ FACTIBLE a nivel semanal\n")
        for m in resultado["menus"]:
            print(f"{m['nombre']} ({m['dias']} días/semana, {m['kcal_total']:.1f}kcal/día):")
            for n, g in sorted(m["gramos"].items(), key=lambda x: -x[1]):
                print(f"   {n}: {g}g")
            print()
    else:
        print("❌ NO FACTIBLE:", resultado["motivo"])
