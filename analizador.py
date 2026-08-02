"""
CANISLAB - Analizador de dietas (modo verificador)

El usuario mete lo que YA le esta dando a su perro (alimentos y gramos) y
esto le dice que cumple, que no, y por que. Es el modo que usan los
verificadores profesionales (Diet Check Munich de la LMU, Raw Fed & Nerdy):
el humano propone y el software audita.

NO calcula gramos: los recibe. Solo diagnostica.
"""
from especies import cargar_alimentos
from optimizador import (
    cargar_requerimientos, MAPA_REQUISITO_A_NUTRIENTE, _valor_o_none,
    resolver_etapa, SENIOR_PROTEINA_MINIMA,
)

# Cuando un nutriente se queda corto, decir DE DONDE suele venir ayuda mas
# que el nombre del nutriente a secas.
DE_DONDE_VIENE = {
    "Yodo": "algas/kelp o un multivitamínico completo",
    "Vitamina_E": "aceites vegetales (girasol, oliva) o un multivitamínico",
    "Linoleico": "aceites vegetales, sobre todo el de girasol",
    "Linolénico": "semilla o aceite de lino, y pescado azul",
    "Zinc": "vísceras, carne roja o un multivitamínico",
    "Cobre": "hígado y un multivitamínico",
    "Manganeso": "un multivitamínico (los alimentos frescos aportan poco)",
    "Vitamina_D": "pescado azul, huevo o un multivitamínico",
    "Vitamina_A": "hígado",
    "Calcio": "hueso carnoso o un suplemento de calcio",
    "Hierro": "hígado, vísceras y carne roja",
    "Selenio": "pescado y vísceras",
    "EPA_DHA_total": "pescado azul o aceite de pescado",
    "Colina": "huevo e hígado",
    "Folato": "hígado y verduras de hoja",
    "Vitamina_B12": "vísceras y carne",
}

# Nutrientes cuyo exceso preocupa de verdad, con el motivo en cristiano.
POR_QUE_IMPORTA_PASARSE = {
    "Calcio": ("En un cachorro en crecimiento el exceso de calcio se asocia a "
               "problemas de desarrollo del esqueleto. El perro adulto lo excreta, "
               "pero el cachorro no sabe regularlo."),
    "Vitamina_A": ("Se acumula en el hígado. Un exceso mantenido puede dañar "
                   "hígado, huesos y articulaciones."),
    "Vitamina_D": ("Se acumula en el cuerpo y tarda meses en eliminarse. "
                   "El exceso afecta al riñón y al calcio en sangre."),
    "Yodo": ("El exceso mantenido puede alterar la tiroides."),
    "Fósforo": ("Un exceso mantenido carga el riñón, sobre todo si el perro "
                "ya tiene la función renal tocada."),
}

ETAPAS_CRECIMIENTO = {"CachorroJoven", "CachorroCrecimiento", "Gestante", "Lactante"}


def analizar_dieta(gramos_por_alimento: dict, der_objetivo: float,
                   etapa_requisitos: str = "Adulto"):
    """
    gramos_por_alimento: {"Carcasa de pollo": 680, "Pollo muslo": 400, ...}
    der_objetivo: kcal que ese perro necesita al dia
    etapa_requisitos: Adulto / CachorroJoven / CachorroCrecimiento /
                      Gestante / Lactante / Senior
    """
    catalogo = {a["nombre"]: a for a in cargar_alimentos()}

    desconocidos = [n for n in gramos_por_alimento if n not in catalogo]
    if desconocidos:
        return {
            "ok": False,
            "motivo": "No tenemos datos de: " + ", ".join(desconocidos),
        }
    if not gramos_por_alimento:
        return {"ok": False, "motivo": "No has añadido ningún alimento todavía."}

    # --- sumar lo que aporta la dieta tal cual la da el usuario ---
    totales, kcal, peso_total = {}, 0.0, 0.0
    por_categoria = {}
    for nombre, g in gramos_por_alimento.items():
        a = catalogo[nombre]
        g = float(g)
        if g <= 0:
            continue
        peso_total += g
        kcal += a["energia"] * g / 100
        por_categoria[a["categoria"]] = por_categoria.get(a["categoria"], 0) + g
        for k, v in a["nutrientes"].items():
            totales[k] = totales.get(k, 0) + v * g / 100

    etapa_datos = resolver_etapa(etapa_requisitos)
    requisitos = cargar_requerimientos()

    # sin requisitos para esa etapa no se puede auditar nada
    hay = sum(1 for r in requisitos
              if MAPA_REQUISITO_A_NUTRIENTE.get(r["nutriente"])
              and _valor_o_none(r.get(f"min{etapa_datos}")) is not None)
    if hay == 0:
        return {"ok": False,
                "motivo": f"Todavía no tenemos los requisitos de la etapa "
                          f"'{etapa_requisitos}', así que no podemos analizar."}

    escala = der_objetivo / 1000
    faltan, sobran, correctos = [], [], []
    for req in requisitos:
        clave = MAPA_REQUISITO_A_NUTRIENTE.get(req["nutriente"])
        if not clave:
            continue
        minimo = _valor_o_none(req.get(f"min{etapa_datos}"))
        maximo = _valor_o_none(req.get(f"max{etapa_datos}"))
        if etapa_requisitos == "Senior" and req["nutriente"] == "Proteína_total":
            if minimo is None or minimo < SENIOR_PROTEINA_MINIMA:
                minimo = SENIOR_PROTEINA_MINIMA
        if minimo is None and maximo is None:
            continue
        valor = totales.get(clave, 0)
        mn = minimo * escala if minimo is not None else None
        mx = maximo * escala if maximo is not None else None
        base = {
            "nutriente": req["nutriente"].replace("_", " "),
            "unidad": req["unidad"],
            "tiene": round(valor, 2),
            "minimo": round(mn, 2) if mn is not None else None,
            "maximo": round(mx, 2) if mx is not None else None,
        }
        if mn is not None and valor < mn:
            base["cubre_pct"] = round(valor / mn * 100)
            base["de_donde"] = DE_DONDE_VIENE.get(req["nutriente"])
            faltan.append(base)
        elif mx is not None and valor > mx:
            base["del_maximo_pct"] = round(valor / mx * 100)
            base["por_que_importa"] = POR_QUE_IMPORTA_PASARSE.get(req["nutriente"])
            sobran.append(base)
        else:
            correctos.append(base)

    faltan.sort(key=lambda x: x["cubre_pct"])
    sobran.sort(key=lambda x: -x["del_maximo_pct"])

    # --- energia ---
    desvio = (kcal - der_objetivo) / der_objetivo * 100 if der_objetivo else 0
    if abs(desvio) <= 10:
        energia_txt = "La cantidad de comida encaja con lo que necesita."
    elif desvio > 0:
        energia_txt = (f"Le estás dando un {abs(desvio):.0f}% más de energía de la "
                       f"que necesita. Mantenido en el tiempo lleva a sobrepeso"
                       + (", y en un cachorro además hace que crezca más rápido de lo conveniente."
                          if etapa_requisitos in ETAPAS_CRECIMIENTO else "."))
    else:
        energia_txt = (f"Le estás dando un {abs(desvio):.0f}% menos de energía de la "
                       f"que necesita.")

    # --- proporciones por categoria, informativas ---
    reparto = [
        {"categoria": c, "gramos": round(g, 1),
         "pct": round(g / peso_total * 100) if peso_total else 0}
        for c, g in sorted(por_categoria.items(), key=lambda x: -x[1])
    ]

    # --- ratio calcio:fosforo ---
    ca, fo = totales.get("calcio", 0), totales.get("fosforo", 0)
    ratio = round(ca / fo, 2) if fo else None
    ratio_ok = ratio is not None and 1.0 <= ratio <= 1.8

    # --- veredicto en una linea ---
    if not faltan and not sobran and abs(desvio) <= 10:
        veredicto = "Esta dieta cubre todo lo que hemos podido comprobar."
    elif sobran and any(s["nutriente"] in ("Calcio", "Vitamina A", "Vitamina D")
                        for s in sobran) and etapa_requisitos in ETAPAS_CRECIMIENTO:
        veredicto = ("Hay un exceso que conviene corregir pronto, porque en "
                     "crecimiento es cuando más importa.")
    elif len(faltan) >= 5:
        veredicto = ("A esta dieta le faltan varias cosas que los alimentos frescos "
                     "por sí solos no suelen cubrir.")
    elif faltan or sobran:
        veredicto = "La dieta está bien encaminada, pero hay cosas que ajustar."
    else:
        veredicto = "La dieta cumple los nutrientes; solo hay que ajustar la cantidad."

    return {
        "ok": True,
        "veredicto": veredicto,
        "energia": {
            "aporta_kcal": round(kcal),
            "necesita_kcal": round(der_objetivo),
            "desvio_pct": round(desvio),
            "texto": energia_txt,
        },
        "peso_total_g": round(peso_total, 1),
        "reparto": reparto,
        "calcio_fosforo": {"ratio": ratio, "correcto": ratio_ok,
                           "referencia": "entre 1:1 y 1.8:1"},
        "faltan": faltan,
        "sobran": sobran,
        "correctos": len(correctos),
        "total_comprobados": len(faltan) + len(sobran) + len(correctos),
        "aviso": ("Este análisis es orientativo y se basa en nuestras tablas de "
                  "composición. No sustituye la valoración de un veterinario."),
    }
