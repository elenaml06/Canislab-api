# -*- coding: utf-8 -*-
"""
Compara requerimientos_v2_final.json contra la TABLA III-3b de FEDIAF 2025
(Nutritional Guidelines, pagina 16): "Recommended nutrient levels for
complete dog food -- Unit per 1000 kcal of metabolisable energy".

Existe porque los requisitos son el cimiento de todo: si un valor o una
unidad esta mal, TODOS los menus estan mal, y ninguna cantidad de tests
del motor lo detectaria -- estarian comprobando que se cumple bien un
requisito equivocado.

Comprueba tres cosas a la vez: el valor, la unidad (con su conversion), y
que la columna de FEDIAF que se usa para cada etapa sea la que toca:
  Adulto              -> Adult, MER 95 kcal/kg^0.75 (la mas exigente)
  CachorroJoven       -> Early Growth (< 14 semanas) y reproduccion
  CachorroCrecimiento -> Late Growth (>= 14 semanas)

Ejecutar tras cualquier cambio en requerimientos_v2_final.json:
    python3 auditar_fediaf.py
"""
import json
import os

# Transcrito de la TABLA III-3b (FEDIAF 2025, pag. 16 del PDF).
# Unidades POR 1000 kcal EM, tal cual las da la tabla.
# (adulto95, adulto110, crecimiento_temprano, crecimiento_tardio, unidad_fediaf)
FEDIAF = {
 "Protein":            (52.10, 45.00, 62.50, 50.00, "g"),
 "Fat":                (13.75, 13.75, 21.25, 21.25, "g"),
 "Linoleic":           ( 3.82,  3.27,  3.25,  3.25, "g"),
 "Arachidonic":        ( None,  None, 75.00, 75.00, "mg"),
 "ALA":                ( None,  None,  0.20,  0.20, "g"),
 "EPA_DHA":            ( None,  None,  0.13,  0.13, "g"),
 "Calcium":            ( 1.45,  1.25,  2.50,  2.00, "g"),
 "Phosphorus":         ( 1.16,  1.00,  2.25,  1.75, "g"),
 "Potassium":          ( 1.45,  1.25,  1.10,  1.10, "g"),
 "Sodium":             ( 0.29,  0.25,  0.55,  0.55, "g"),
 "Chloride":           ( 0.43,  0.38,  0.83,  0.83, "g"),
 "Magnesium":          ( 0.20,  0.18,  0.10,  0.10, "g"),
 "Copper":             ( 2.08,  1.80,  2.75,  2.75, "mg"),
 "Iodine":             ( 0.30,  0.26,  0.38,  0.38, "mg"),
 "Iron":               (10.40,  9.00, 22.00, 22.00, "mg"),
 "Manganese":          ( 1.67,  1.44,  1.40,  1.40, "mg"),
 "Selenium_wet":       (67.50, 57.50,100.00,100.00, "µg"),
 "Zinc":               (20.80, 18.00, 25.00, 25.00, "mg"),
 "VitaminA":           ( 1754,  1515,  1250,  1250, "IU"),
 "VitaminD":           (159.00,138.00,138.00,125.00,"IU"),
 "VitaminE":           (10.40,  9.00, 12.50, 12.50, "IU"),
 "B1_Thiamine":        ( 0.62,  0.54,  0.45,  0.45, "mg"),
 "B2_Riboflavin":      ( 1.74,  1.50,  1.05,  1.05, "mg"),
 "B5_Pantothenic":     ( 4.11,  3.55,  3.00,  3.00, "mg"),
 "B6_Pyridoxine":      ( 0.42,  0.36,  0.30,  0.30, "mg"),
 "B12":                ( 9.68,  8.36,  7.00,  7.00, "µg"),
 "B3_Niacin":          ( 4.74,  4.09,  3.40,  3.40, "mg"),
 "B9_Folic":           (74.70, 64.50, 54.00, 54.00, "µg"),
 "Choline":            (474.00,409.00,425.00,425.00,"mg"),
}
# Como se llama cada uno en el JSON, y el factor para pasar de la unidad
# de FEDIAF a la del JSON.
EQUIV = {
 "Proteína_total":     ("Protein",        1.0),      # g -> g
 "Grasa_total":        ("Fat",            1.0),
 "Linoleico":          ("Linoleic",       1.0),
 "Araquidónico":       ("Arachidonic",    1.0),      # mg -> mg
 "Linolénico":         ("ALA",            1.0),
 "EPA_DHA_total":      ("EPA_DHA",        1.0),
 "Calcio":             ("Calcium",     1000.0),      # g -> mg
 "Fósforo":            ("Phosphorus",  1000.0),
 "Potasio":            ("Potassium",   1000.0),
 "Sodio":              ("Sodium",      1000.0),
 "Cloruro":            ("Chloride",    1000.0),
 "Magnesio":           ("Magnesium",   1000.0),
 "Cobre":              ("Copper",         1.0),      # mg -> mg
 "Yodo":               ("Iodine",      1000.0),      # mg -> µg
 "Hierro":             ("Iron",           1.0),
 "Manganeso":          ("Manganese",      1.0),
 "Selenio":            ("Selenium_wet",   1.0),      # µg -> µg
 "Zinc":               ("Zinc",           1.0),
 "Vitamina_A":         ("VitaminA",     0.3),        # IU -> µg retinol (1 UI = 0.3 µg)
 "Vitamina_D":         ("VitaminD",     0.025),      # IU -> µg (1 UI = 0.025 µg)
 # 0.67 y no 1.0: 1 UI = 1 mg SOLO para el acetato sintetico de los
 # suplementos. La vitamina E de los ALIMENTOS es alfa-tocoferol natural,
 # que son 0.67 mg/UI, y asi es como la declaran las tablas de composicion.
 # Convertir a 1.0 daria un requisito un 49% mas alto de la cuenta.
 "Vitamina_E":         ("VitaminE",      0.67),     # IU -> mg alfa-tocoferol natural
 "Tiamina":            ("B1_Thiamine",    1.0),
 "Riboflavina":        ("B2_Riboflavin",  1.0),
 "Acido_pantotenico":  ("B5_Pantothenic", 1.0),
 "Vitamina_B6":        ("B6_Pyridoxine",  1.0),
 "Vitamina_B12":       ("B12",            1.0),
 "Niacina":            ("B3_Niacin",      1.0),
 "Folato":             ("B9_Folic",       1.0),
 "Colina":             ("Choline",        1.0),
}
CAMPOS = [("minAdulto", 0, "Adulto"),
          ("minCachorroJoven", 2, "CachorroJoven (Early Growth)"),
          ("minCachorroCrecimiento", 3, "CachorroCrecimiento (Late Growth)")]

# ⚠️ Ruta relativa al PROPIO archivo (25 agosto): aquí había una ruta
# absoluta a un ordenador concreto, así que esta auditoría solo se podía
# ejecutar en esa máquina. En cualquier otra reventaba antes de comprobar
# nada -- y una auditoría que no se puede ejecutar no auditó nunca.
_AQUI = os.path.dirname(os.path.abspath(__file__))
req = {r["nutriente"]: r
       for r in json.load(open(os.path.join(_AQUI, "requerimientos_v2_final.json"),
                               encoding="utf-8"))}
def num(v):
    if v in (None, "", "-"): return None
    try: return float(str(v).replace(",", "."))
    except ValueError: return None

problemas, ok_n = [], 0
print("%-22s %-28s %10s %10s" % ("NUTRIENTE", "ETAPA", "JSON", "FEDIAF"))
print("─"*76)
for nombre_json, (clave, factor) in EQUIV.items():
    r = req.get(nombre_json)
    if not r:
        problemas.append(("FALTA", nombre_json, "no está en el JSON")); continue
    for campo, col, etiqueta in CAMPOS:
        esperado = FEDIAF[clave][col]
        if esperado is None: continue
        esperado = esperado * factor
        actual = num(r.get(campo))
        if actual is None:
            problemas.append(("SIN VALOR", nombre_json, f"{etiqueta}: el JSON no trae {campo}"))
            continue
        # tolerancia del 1% por redondeos de la propia tabla
        if abs(actual - esperado) > max(esperado * 0.01, 1e-9):
            problemas.append(("NO COINCIDE", nombre_json,
                              f"{etiqueta}: JSON={actual:g} vs FEDIAF={esperado:g} "
                              f"({r.get('unidad')})"))
            print("%-22s %-28s %10g %10g  <<<" % (nombre_json, etiqueta, actual, esperado))
        else:
            ok_n += 1


# ══════════════════════════════════════════════════════════════════════
# MAXIMOS — la cara de la toxicidad
#
# Vienen de dos sitios distintos, y por eso es facil equivocarse:
#   · Los "(N)" nutricionales estan en la III-3b, ya por 1000 kcal.
#   · Los "(L)" legales de la UE SOLO se dan en la III-3a, por 100 g de
#     materia seca. Se pasan a por-1000-kcal multiplicando por 2.5,
#     porque FEDIAF usa 4000 kcal/kg MS como densidad de referencia
#     (100 g MS = 400 kcal, y 1000/400 = 2.5).
# El x2.5 no es una suposicion: cuadra en dos sitios donde las dos tablas
# dan el mismo dato -- vitamina A (40 000 x 2.5 = 100 000) y vitamina D
# (320 x 2.5 = 800), que es justo lo que pone la III-3b.
# ══════════════════════════════════════════════════════════════════════
MAXIMOS = {
 "Calcio":     {"Adulto": 6250, "CachorroJoven": 4000, "CachorroCrecimiento": 4500},
 "Fósforo":    {"Adulto": 4000},
 "Cobre":      {"todas": 2.80 * 2.5},
 "Yodo":       {"todas": 1.10 * 2.5 * 1000},
 "Hierro":     {"todas": 68.18 * 2.5},
 "Manganeso":  {"todas": 17.00 * 2.5},
 "Selenio":    {"todas": 56.80 * 2.5},
 "Zinc":       {"todas": 22.70 * 2.5},
 "Vitamina_A": {"todas": 100000 * 0.3},
 "Vitamina_D": {"todas": 800.0 * 0.025},
 # OJO: la III-3b lo etiqueta "Early Growth:", asi que este maximo es
 # SOLO de crecimiento temprano. No ponerlo tambien en el tardio.
 "Linoleico":  {"CachorroJoven": 16.25},
}
# Nutrientes que NO tienen maximo en FEDIAF: que el JSON ponga "-" es lo
# correcto, y ponerle un numero seria inventarselo. La vitamina E es uno.
SIN_MAXIMO = ("Proteína_total", "Grasa_total", "Vitamina_E", "Tiamina",
              "Riboflavina", "Acido_pantotenico", "Vitamina_B6", "Vitamina_B12",
              "Niacina", "Folato", "Colina", "Potasio", "Magnesio",
              "Linolénico", "EPA_DHA_total", "Araquidónico")

for nut, topes in MAXIMOS.items():
    r = req.get(nut)
    if not r:
        problemas.append(("FALTA", nut, "no está en el JSON")); continue
    for etapa in ("Adulto", "CachorroJoven", "CachorroCrecimiento"):
        esperado = topes.get(etapa, topes.get("todas"))
        if esperado is None: continue
        actual = num(r.get("max" + etapa))
        if actual is None:
            problemas.append(("SIN MÁXIMO", nut,
                              f"{etapa}: el JSON no lo pone y FEDIAF da {esperado:g}"))
        elif abs(actual - esperado) > max(esperado * 0.01, 1e-9):
            problemas.append(("MÁXIMO NO COINCIDE", nut,
                              f"{etapa}: JSON={actual:g} vs FEDIAF={esperado:g}"))
        else:
            ok_n += 1

# ─── VALORES PUESTOS A PROPÓSITO QUE **NO** SON DE FEDIAF ────────────────────
#
# ⚠️ AÑADIDO (25 agosto). FEDIAF no cubre todo, y a veces se adopta un valor
# de otra fuente a conciencia. Eso es legítimo -- lo que no puede pasar es
# que quede indistinguible de un valor de la tabla, porque entonces nadie
# sabe de dónde salió. Es literalmente lo que pasó con la fila "Fibra":
# estaba ahí desde el primer día, sin fuente, y acabó diciéndole a una
# usuaria que a un menú hecho por la propia app le faltaba algo.
#
# Cada entrada lleva su fuente. Salen en el informe como "PUESTO A PROPÓSITO",
# aparte de las discrepancias, para que se vean sin ensuciar el recuento.
FUERA_DE_FEDIAF = {
    ("EPA_DHA_total", "minAdulto"):
        "NRC 2006. FEDIAF solo exige EPA+DHA en crecimiento y reproducción; "
        "para adulto no da mínimo. Se adopta por relevancia clínica "
        "(inflamación, articulaciones, corazón, piel). Decidido el 25/08/2026.",
    ("EPA_DHA_total", "maxAdulto"):
        "Lenox & Bauer, JVIM 2013 (27:217-226). FEDIAF no da máximo de "
        "EPA+DHA para ninguna etapa. Decidido el 25/08/2026.",
}

a_proposito = []
for (_nut, _campo), _razon in FUERA_DE_FEDIAF.items():
    _fila = req.get(_nut)
    _v = num(_fila.get(_campo)) if _fila else None
    if _v is None:
        problemas.append(("FALTA EL VALOR ADOPTADO", _nut,
                          f"{_campo} está declarado en FUERA_DE_FEDIAF pero el JSON no lo trae. "
                          f"O se puso y se ha borrado, o sobra esta entrada."))
    else:
        a_proposito.append((_nut, _campo, _v, _razon))

for nut in SIN_MAXIMO:
    r = req.get(nut)
    if not r: continue
    for etapa in ("Adulto", "CachorroJoven", "CachorroCrecimiento"):
        if (nut, "max" + etapa) in FUERA_DE_FEDIAF:
            continue     # adoptado a propósito y con fuente, ver arriba
        if num(r.get("max" + etapa)) is not None:
            problemas.append(("MÁXIMO INVENTADO", nut,
                              f"{etapa}: el JSON pone un máximo y FEDIAF no da ninguno"))
        else:
            ok_n += 1

# ─── Y AL REVÉS: ¿SOBRA ALGUNA FILA EN EL JSON? ─────────────────────────────
#
# ⚠️ AÑADIDO (25 agosto) — CASO REAL ENCONTRADO. Esta auditoría comprobaba
# que cada valor de FEDIAF estuviera bien puesto en el JSON. Nunca comprobó
# lo contrario: que cada fila del JSON venga de FEDIAF. Con 161
# comprobaciones cuadrando y 0 discrepancias, en el JSON había una fila
# "Fibra" (4,29 g mínimo, 14,3 máximo) QUE NO ESTÁ EN LA TABLA DE FEDIAF, y
# esta auditoría la daba por buena sin mirarla, porque solo recorría su
# propia lista.
#
# El motor nunca la usó (no estaba en verificar.MAPA), pero el ANALIZADOR
# sí: le dijo a una usuaria que a un menú hecho por la propia app le faltaba
# fibra. 8 de 8 menús verdes salían cortos.
#
# Una fila que sobra es tan peligrosa como un valor mal puesto: en el
# momento en que alguien la enchufa a un mapa, pasa a decidir menús. Y una
# auditoría que solo mira en una dirección deja creer que está todo
# comprobado.
NO_SON_NUTRIENTES_DE_LA_TABLA = {
    # Sí sale de FEDIAF, pero es una RELACIÓN, no una fila de nutriente.
    "Relacion_Ca_P",
    # Caso especial derivado: el calcio de cachorros de raza grande en
    # crecimiento tardío. No es una fila propia de la tabla III-3b; el motor
    # lo aplica aparte, solo si el peso adulto esperado es >= 25 kg.
    "Calcio_LateGrowth_RazaGrande",
}
_cubiertos = set(EQUIV) | set(MAXIMOS) | set(SIN_MAXIMO) | NO_SON_NUTRIENTES_DE_LA_TABLA
for _n in req:
    if _n in _cubiertos:
        continue
    problemas.append(("NO ESTÁ EN FEDIAF", _n,
                      "hay una fila en el JSON que esta auditoría no compara contra "
                      "ninguna fila de la tabla III-3b. O falta añadirla aquí con su "
                      "valor de FEDIAF, o no es un requisito y no puede acabar en "
                      "ningún mapa de requisitos (es lo que pasó con 'Fibra')"))

if a_proposito:
    print()
    print("PUESTOS A PROPÓSITO (no son de la tabla de FEDIAF):")
    for _nut, _campo, _v, _razon in a_proposito:
        print("  %s · %s = %g" % (_nut, _campo, _v))
        print("      %s" % _razon)

print()
print("Comprobaciones que cuadran: %d" % ok_n)
print("Discrepancias: %d" % len(problemas))
for tipo, nut, det in problemas:
    print("  [%s] %s — %s" % (tipo, nut, det))
