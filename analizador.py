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
#
# ⚠️ AMPLIADO (5 agosto, madrugada) — pedido expreso: faltaban 14 de los
# 30 nutrientes reales sin ninguna explicación de origen -- si a alguien
# le salía "Fósforo, cubre el 60%" sin más, se quedaba sin saber qué
# hacer con eso. Completado con los 30 nutrientes reales del sistema.
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
    "Acido_pantotenico": "carne y vísceras en general, sobre todo hígado",
    "Araquidónico": "grasa animal, sobre todo de pollo y huevo — el perro, a diferencia de otros mamíferos, no lo fabrica bien por sí solo",
    "Cloruro": "sal común, o carne y hueso en cantidad normal",
    "Fibra": "verduras y fruta, o un suplemento específico de fibra",
    "Fósforo": "hueso carnoso, carne y pescado — normalmente sube solo si sube la proteína",
    "Grasa_total": "carne con piel o con grasa, y aceites",
    "Magnesio": "pescado, vísceras y verduras de hoja",
    "Niacina": "carne, pescado e hígado",
    "Potasio": "carne, pescado y verduras",
    "Proteína_total": "carne muscular, pescado y vísceras",
    "Riboflavina": "hígado, carne y huevo",
    "Sodio": "sal común, o carne y hueso en cantidad normal",
    "Tiamina": "carne y vísceras en general",
    "Vitamina_B6": "carne, pescado e hígado",
}

# Nutrientes cuyo exceso preocupa de verdad, con el motivo en cristiano.
#
# ⚠️ AMPLIADO (5 agosto, madrugada) — mismo motivo que DE_DONDE_VIENE:
# faltaban 9 de los 14 nutrientes que sí tienen un máximo real en el
# sistema, así que podían aparecer en "sobran" sin ninguna explicación
# de por qué importa. Selenio usa los datos ya investigados a fondo en
# otra ronda (Merck Veterinary Manual).
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
    "Cloruro": ("Junto con el sodio, en exceso mantenido puede cargar la "
                "presión arterial y el riñón."),
    "Cobre": ("Se acumula en el hígado. Hay razas con predisposición genética "
              "a la toxicidad por cobre (por ejemplo el Bedlington Terrier), "
              "donde el margen de seguridad es mucho más estrecho."),
    "Fibra": ("En exceso reduce la digestibilidad del resto de la dieta, y "
              "suele notarse en heces blandas o gases."),
    "Hierro": ("El cuerpo regula bien su absorción por dieta normal, así que "
               "el exceso real es raro salvo por sobredosis de suplemento -- "
               "en ese caso, sí puede dañar el hígado."),
    "Linoleico": ("Un exceso de omega-6 respecto al omega-3 puede favorecer "
                  "procesos inflamatorios en el cuerpo."),
    "Manganeso": ("El exceso mantenido puede afectar al sistema nervioso, "
                  "aunque es poco frecuente que llegue a ese nivel solo con "
                  "dieta normal."),
    "Selenio": ("El exceso mantenido en el tiempo (no solo una dosis puntual "
                "alta) puede causar pérdida de pelo, deformidad de uñas y "
                "letargia -- lo que se conoce como toxicosis crónica por "
                "selenio."),
    "Sodio": ("Junto con el cloruro, en exceso mantenido puede cargar la "
              "presión arterial y el riñón."),
    "Zinc": ("El zinc por dieta normal es de los minerales menos tóxicos que "
             "hay -- el riesgo real de intoxicación por zinc en perros viene "
             "casi siempre de ingerir objetos metálicos (monedas, juguetes), "
             "no de la comida."),
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
    # Casos que reventaban: sin alimentos (respuesta incoherente) y con
    # der_objetivo 0 (division por cero al calcular el % de energia).
    if not gramos_por_alimento:
        return {"factible": False,
                "veredicto": "No has indicado ningún alimento todavía.",
                "faltan": [], "se_pasa": [], "correctos": 0,
                "reparto_categorias": {}, "peso_total_g": 0}
    if not der_objetivo or der_objetivo <= 0:
        return {"factible": False,
                "veredicto": "Falta saber cuántas calorías necesita el perro para poder analizar la dieta.",
                "faltan": [], "se_pasa": [], "correctos": 0,
                "reparto_categorias": {}, "peso_total_g": 0}

    catalogo = {a["nombre"]: a for a in cargar_alimentos()}

    desconocidos = [n for n in gramos_por_alimento if n not in catalogo]
    if desconocidos:
        # Misma forma de respuesta que el resto: si cambia segun el caso, el
        # frontend no sabe leerla y se queda en blanco sin decir por que.
        return {"factible": False, "ok": False,
                "veredicto": "No tenemos datos de: " + ", ".join(desconocidos),
                "motivo": "No tenemos datos de: " + ", ".join(desconocidos),
                "faltan": [], "se_pasa": [], "correctos": 0,
                "reparto_categorias": {}, "peso_total_g": 0}
    if not gramos_por_alimento:
        return {"factible": False, "ok": False,
                "veredicto": "No has añadido ningún alimento todavía.",
                "motivo": "No has añadido ningún alimento todavía.",
                "faltan": [], "se_pasa": [], "correctos": 0,
                "reparto_categorias": {}, "peso_total_g": 0}

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
        msg = (f"Todavía no tenemos los requisitos de la etapa "
               f"'{etapa_requisitos}', así que no podemos analizar.")
        return {"factible": False, "ok": False, "veredicto": msg, "motivo": msg,
                "faltan": [], "se_pasa": [], "correctos": 0,
                "reparto_categorias": {}, "peso_total_g": 0}

    escala = der_objetivo / 1000
    # ⚠️ CORREGIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO, pedido
    # expreso: "siguen apareciendo repetidos algunos nutrientes cuando
    # dice lo que falta". Causa real: "Calcio" y
    # "Calcio_LateGrowth_RazaGrande" son DOS requisitos distintos en el
    # JSON de requerimientos, pero AMBOS mapean al mismo nutriente real
    # ("calcio") -- es intencional en el MOTOR de generación (una
    # segunda restricción, más estricta, para razas grandes en
    # crecimiento), pero en el analizador esto hacía que el mismo dato
    # de calcio se comparara dos veces contra dos límites distintos,
    # apareciendo como "Calcio" Y "Calcio LateGrowth RazaGrande" a la
    # vez en el resultado -- el mismo nutriente, dos veces, con
    # etiquetas distintas. Ahora se agrupan PRIMERO por el nutriente
    # real al que mapean, consolidando en una sola entrada con la
    # restricción más estricta de todas las que apliquen (el mínimo
    # más alto, el máximo más bajo) -- que es, de hecho, lo que
    # "Calcio_LateGrowth_RazaGrande" quiere decir conceptualmente: una
    # restricción adicional que se SUMA, no un nutriente aparte.
    por_nutriente = {}
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
        acumulado = por_nutriente.setdefault(clave, {
            "nombre_mostrado": req["nutriente"], "unidad": req["unidad"],
            "minimo": None, "maximo": None,
        })
        # el mínimo más ALTO manda (la restricción más exigente hacia abajo)
        if minimo is not None and (acumulado["minimo"] is None or minimo > acumulado["minimo"]):
            acumulado["minimo"] = minimo
        # el máximo más BAJO manda (la restricción más exigente hacia arriba)
        if maximo is not None and (acumulado["maximo"] is None or maximo < acumulado["maximo"]):
            acumulado["maximo"] = maximo

    faltan, sobran, correctos = [], [], []
    for clave, datos in por_nutriente.items():
        minimo, maximo = datos["minimo"], datos["maximo"]
        valor = totales.get(clave, 0)
        mn = minimo * escala if minimo is not None else None
        mx = maximo * escala if maximo is not None else None
        nombre_para_buscar = datos["nombre_mostrado"]
        # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL, pedido expreso:
        # "linoleico me sale repetido" -- no era un dato duplicado (solo
        # hay una entrada real de Linoleico en el sistema), era que
        # "Linoleico" y "Linolénico" se parecen tanto en el nombre que
        # se leían como si fueran el mismo nutriente dos veces. Son dos
        # cosas genuinamente distintas (omega-6 y omega-3), así que se
        # aclara directamente en el nombre que se muestra, no solo en
        # el texto pequeño de abajo -- así se distingue de un vistazo.
        nombre_mostrado_final = nombre_para_buscar.replace("_", " ")
        if nombre_para_buscar == "Linoleico":
            nombre_mostrado_final = "Linoleico (omega-6)"
        elif nombre_para_buscar == "Linolénico":
            nombre_mostrado_final = "Linolénico (omega-3)"
        base = {
            "nutriente": nombre_mostrado_final,
            "unidad": datos["unidad"],
            "tiene": round(valor, 2),
            "minimo": round(mn, 2) if mn is not None else None,
            "maximo": round(mx, 2) if mx is not None else None,
        }
        if mn is not None and valor < mn:
            base["cubre_pct"] = round(valor / mn * 100)
            base["de_donde"] = DE_DONDE_VIENE.get(nombre_para_buscar)
            faltan.append(base)
        elif mx is not None and valor > mx:
            base["del_maximo_pct"] = round(valor / mx * 100)
            base["por_que_importa"] = POR_QUE_IMPORTA_PASARSE.get(nombre_para_buscar)
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
