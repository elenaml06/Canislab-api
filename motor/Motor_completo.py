# -*- coding: utf-8 -*-
"""
EL MOTOR DE VERDAD — una sola pregunta, no miles de intentos con nombres fijos.

POR QUÉ ESTE ARCHIVO EXISTE
-----------------------------
Toda la noche del 4→5 de agosto se probó: elegir a mano, elegir por
densidad con una sola pasada, comparar unas pocas combinaciones,
enumerar miles de combinaciones con nombres fijos ("menú de pollo",
"menú de pollo y sardina"...). La usuaria lo dijo claro:
    "no pruebes con menú de pollo... que saques menús viables, y si el
     menú es de cordero con pollo, pues cordero con pollo, con lo que
     salga"
Fijar la carne y el hueso de antemano y luego probar variantes alrededor
es la pregunta equivocada. La pregunta correcta es UNA SOLA:
    "de TODOS los alimentos disponibles, ¿cuál es la mejor combinación
     posible — qué alimentos Y cuánto de cada uno — que cumple los 30
     requisitos con máximo 2 suplementos?"

Eso es un problema de PROGRAMACIÓN LINEAL ENTERA MIXTA (MILP): unas
variables son continuas (cuántos gramos) y otras son binarias (¿se usa
este alimento sí/no?), porque hay que LIMITAR CUÁNTOS alimentos distintos
se usan por categoría (máx. 3 carnes, máx. 2 suplementos...), y eso no
se puede expresar solo con gramos.

`scipy.optimize.milp` lo resuelve de forma EXACTA: si existe una
combinación que funciona, la encuentra. Si no existe, lo dice con
certeza matemática, no porque no se haya probado lo suficiente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from verificar import MAPA, _num, EQUIVALENCIA


def resolver(der, etapa, alimentos, req, peso_perro_kg, dosis_maxima_fn,
            excluidos=None, margenes_categoria=None, cuantos_max=None,
            max_suplementos=2, tolerancia_kcal=0.03,
            forzar=None, preferir=None):
    """
    UNA sola llamada. Decide QUÉ alimentos usar Y cuántos gramos de cada
    uno, de entre TODOS los accesibles, a la vez.

    `forzar`: lista de nombres que SÍ O SÍ tienen que entrar en la ración
    (con gramos > 0). Es el modo PERSONALIZAR: el usuario elige alimentos
    concretos y el motor calcula el resto alrededor de esa elección. Si
    forzar algo hace que no exista solución, se devuelve (False, None) —
    igual que antes, una respuesta exacta, no una aproximación.

    `preferir`: lista de nombres que el motor debe usar CON PREFERENCIA
    sobre otros si hay varias soluciones igual de válidas — no obliga a
    que entren, solo hace que el "coste" de usarlos sea menor. Es el modo
    APROVECHAR: lo que el usuario ya tiene en casa gana la partida frente
    a alimentos que tendría que comprar, PERO SOLO si con eso sigue
    cumpliendo los 30 requisitos — si no llega, el motor añade lo que
    haga falta igualmente, avisando (eso se ve en qué más aparece en la
    ración final).

    Devuelve (factible: bool, gramos: {nombre: g} o None).
    """
    from accesibles import ACCESIBLES
    from exclusiones import filtrar

    if cuantos_max is None:
        from modos import CUANTOS_MAX as cuantos_max

    # ⚠️ AÑADIDO 5 agosto: "Extras" (aceites, huevos, semillas) NO estaba
    # en esta lista, así que ni siquiera entraban como candidatos — el
    # linoleico dependía solo de lo que aportara la carne, sin poder usar
    # aceite de girasol. Ahora entra, y junto con los suplementos
    # comerciales queda topado al 5% del peso (decisión de la usuaria).
    SUP_CATS = ("Multivitamínico", "Omega-3", "Yodo", "Fibra", "Calcio",
               "Hierro", "Vitamina B", "Extras")

    # Candidatos: TODOS los accesibles de cada categoría de comida, y
    # TODOS los suplementos del catálogo (no solo unos pocos elegidos).
    candidatos_por_cat = {}
    for cat, lista in ACCESIBLES.items():
        disp = [n for n in lista if n in alimentos]
        if excluidos:
            disp, _f, _a = filtrar(disp, excluidos)
        candidatos_por_cat[cat] = disp
    candidatos_por_cat["Suplementos"] = [a["nombre"] for a in alimentos.values()
                                        if a.get("categoria") in SUP_CATS]

    nombres = []
    categoria_de = {}
    for cat, lista in candidatos_por_cat.items():
        for n in lista:
            if n not in nombres:
                nombres.append(n)
                categoria_de[n] = cat
    n_var = len(nombres)
    # variables: [gramos_0..gramos_N-1, usa_0..usa_N-1] — la mitad continuas,
    # la mitad binarias (0/1), unidas por: gramos_i <= usa_i * TECHO_i
    idx = {n: i for i, n in enumerate(nombres)}

    et = EQUIVALENCIA.get(etapa, etapa)
    A_rows, lb_rows, ub_rows = [], [], []

    def fila_vacia():
        return [0.0] * (2 * n_var)

    # TECHOS por variable (para la vinculación gramos<=usa*techo)
    techos = []
    for n in nombres:
        a = alimentos[n]
        if categoria_de[n] == "Suplementos":
            t = dosis_maxima_fn(a, peso_perro_kg)
            techos.append(t if t else 5.0)
        else:
            kcal100 = a.get("energia", 0) or 1.0
            techos.append((der * 0.55) / kcal100 * 100.0)  # ningún alimento >55% del día

    # 1. kcal totales = DER (con tolerancia)
    fila = fila_vacia()
    for n in nombres:
        fila[idx[n]] = alimentos[n].get("energia", 0) / 100.0
    A_rows.append(fila); lb_rows.append(der * (1 - tolerancia_kcal)); ub_rows.append(der * (1 + tolerancia_kcal))

    # 2. mínimos y máximos de FEDIAF
    for nombre_req, clave in MAPA.items():
        r = req.get(nombre_req)
        if not r:
            continue
        mn = _num(r.get(f"min{et}"))
        mx = _num(r.get(f"max{et}")) or _num(r.get("maxAdulto"))
        fila = fila_vacia()
        aporta_algo = False
        for n in nombres:
            v = (_num(alimentos[n].get("nutrientes", {}).get(clave)) or 0.0) / 100.0
            if v:
                fila[idx[n]] = v; aporta_algo = True
        if not aporta_algo:
            continue
        lo = mn * der / 1000.0 if mn is not None else -np.inf
        hi = mx * der / 1000.0 if mx is not None else np.inf
        A_rows.append(fila); lb_rows.append(lo); ub_rows.append(hi)

    # 2b. RATIO Ca:P — se me olvidó la primera vez. Calcio y fósforo por
    # separado no bastan: la RELACIÓN entre ambos es su propio requisito,
    # y es lineal (Ca >= ratio_min * P  y  Ca <= ratio_max * P), así que
    # se puede meter igual que cualquier otra restricción.
    r_ratio = req.get("Relacion_Ca_P")
    if r_ratio:
        rmin = _num(r_ratio.get(f"min{et}"))
        rmax = _num(r_ratio.get(f"max{et}"))
        fila_ca = fila_vacia(); fila_p = fila_vacia()
        for n in nombres:
            ca = (_num(alimentos[n].get("nutrientes", {}).get("calcio")) or 0.0) / 100.0
            p = (_num(alimentos[n].get("nutrientes", {}).get("fosforo")) or 0.0) / 100.0
            fila_ca[idx[n]] = ca
            fila_p[idx[n]] = p
        if rmin is not None:
            fila = [fila_ca[j] - rmin * fila_p[j] for j in range(2 * n_var)]
            A_rows.append(fila); lb_rows.append(0.0); ub_rows.append(np.inf)
        if rmax is not None:
            fila = [fila_ca[j] - rmax * fila_p[j] for j in range(2 * n_var)]
            A_rows.append(fila); lb_rows.append(-np.inf); ub_rows.append(0.0)

    # 3. margen por peso de cada categoría de COMIDA (no suplementos)
    if margenes_categoria:
        fila_total = fila_vacia()
        for n in nombres:
            if categoria_de[n] != "Suplementos":
                fila_total[idx[n]] = 1.0
        for cat, (mnp, mxp) in margenes_categoria.items():
            miembros = [n for n in nombres if categoria_de[n] == cat]
            if not miembros:
                continue
            fila_cat = fila_vacia()
            for n in miembros:
                fila_cat[idx[n]] = 1.0
            fila_rel_max = [fila_cat[j] - mxp * fila_total[j] for j in range(2 * n_var)]
            A_rows.append(fila_rel_max); lb_rows.append(-np.inf); ub_rows.append(0.0)
            fila_rel_min = [-fila_cat[j] + mnp * fila_total[j] for j in range(2 * n_var)]
            A_rows.append(fila_rel_min); lb_rows.append(-np.inf); ub_rows.append(0.0)

    # 4. VINCULACIÓN gramos <= usa * techo (y gramos >= 0, ya en bounds)
    for n in nombres:
        i = idx[n]
        fila = fila_vacia()
        fila[i] = 1.0
        fila[n_var + i] = -techos[i]
        A_rows.append(fila); lb_rows.append(-np.inf); ub_rows.append(0.0)

    # 5. CUÁNTOS ALIMENTOS DISTINTOS por categoría (máx.)
    for cat, tope in cuantos_max.items():
        miembros = [n for n in nombres if categoria_de[n] == cat]
        if not miembros:
            continue
        fila = fila_vacia()
        for n in miembros:
            fila[n_var + idx[n]] = 1.0
        A_rows.append(fila); lb_rows.append(0); ub_rows.append(tope)

    # 6. MÁXIMO DE SUPLEMENTOS (solo los COMERCIALES cuentan para el
    # límite de "2" — los aceites/huevos de Extras no son "un suplemento"
    # en el sentido de producto de marca, cuentan aparte en el peso)
    SUP_COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                       "Calcio", "Hierro", "Vitamina B")
    fila = fila_vacia()
    for n in nombres:
        if categoria_de[n] in SUP_COMERCIALES:
            fila[n_var + idx[n]] = 1.0
    A_rows.append(fila); lb_rows.append(0); ub_rows.append(max_suplementos)

    # 6b. EXTRAS + SUPLEMENTOS JUNTOS, MÁXIMO 5% DEL PESO (decisión de la
    # usuaria 5 agosto: "los extras, suplementos también entrando dentro
    # de extras, no pueden superar un cinco por ciento").
    fila_total_con_sup = fila_vacia()
    for n in nombres:
        fila_total_con_sup[idx[n]] = 1.0
    fila_extras = fila_vacia()
    for n in nombres:
        if categoria_de[n] == "Suplementos":
            fila_extras[idx[n]] = 1.0
    fila_5pc = [fila_extras[j] - 0.05 * fila_total_con_sup[j] for j in range(2 * n_var)]
    A_rows.append(fila_5pc); lb_rows.append(-np.inf); ub_rows.append(0.0)

    constraints = LinearConstraint(np.array(A_rows), np.array(lb_rows), np.array(ub_rows))
    integrality = np.array([0] * n_var + [1] * n_var)   # 0=continua, 1=entera(binaria)
    bounds = Bounds(lb=[0.0] * n_var + [0] * n_var, ub=[np.inf] * n_var + [1] * n_var)

    # FORZAR: el alimento tiene que estar sí o sí (usa_i >= 1, o sea = 1)
    if forzar:
        for n in forzar:
            if n not in idx:
                continue  # no es un candidato válido; se ignora sin romper
            i = idx[n]
            bounds.lb[n_var + i] = 1

    # objetivo: minimizar cuántos alimentos distintos se usan en total
    # (ración simple, no 20 ingredientes), PERO con coste menor para los
    # que el usuario quiere aprovechar — así el resolver los prefiere
    # cuando dos soluciones son igual de válidas, sin obligarlos.
    coste_binaria = [1.0] * n_var
    if preferir:
        for n in preferir:
            if n in idx:
                coste_binaria[idx[n]] = 0.1   # mucho más barato usarlo
    c = np.array([0.0] * n_var + coste_binaria)

    res = milp(c, constraints=constraints, integrality=integrality, bounds=bounds)

    if res.success:
        x = res.x[:n_var]
        gramos = {n: round(x[idx[n]], 2) for n in nombres if x[idx[n]] > 0.5}
        return True, gramos
    return False, None
