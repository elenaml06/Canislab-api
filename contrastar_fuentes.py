# -*- coding: utf-8 -*-
"""
CONTRASTAR EL CATÁLOGO CONTRA SUS FUENTES — BEDCA, CIQUAL y USDA
================================================================

POR QUÉ EXISTE
--------------
El 7 de septiembre se cerraron 52 celdas del catálogo yendo a las fuentes.
Lo caro de aquel día no fueron los datos: fue averiguar CÓMO se leen.

  · BEDCA no tiene API documentada. Su buscador manda un XML a
    `procquery.php`, y ese XML hay que reconstruirlo leyendo el `query.js`
    del propio sitio. Con la lista de atributos recortada el servicio
    devuelve un cuerpo VACÍO en vez de un error, así que hay que mandar
    exactamente la misma lista de 57 campos que manda su `foodresponse1.xsl`.
  · CIQUAL no tiene consulta por alimento: se baja la tabla 2020 entera en
    un `.xls` y se busca en local.
  · USDA sí tiene API, pero la `DEMO_KEY` está limitada y contesta
    OVER_RATE_LIMIT casi siempre. El volcado oficial de SR Legacy son 6 MB
    y no tiene límite ninguno.

Todo eso está aquí para no volver a descubrirlo.

NO LO EJECUTA LA BATERÍA, y es a propósito: necesita red y se baja 10 MB.
`pruebas_completas.py` no puede depender de que tres servidores externos
estén levantados. Lo que sí vigila la batería es el catálogo consigo mismo
(`auditar_catalogo.py`, BLOQUES 19 y 44). Esto es la herramienta de la
persona que va a mirar una ficha.

CÓMO SE USA
-----------
    python3 contrastar_fuentes.py "Cerebro de vaca"
    python3 contrastar_fuentes.py "Cerebro de vaca" --bedca 1047 --ciqual 40006 --usda 174351
    python3 contrastar_fuentes.py --buscar "sesos"

Sin identificadores solo busca por nombre y te dice los candidatos; el
emparejamiento NO se automatiza a propósito, porque "Timo de ternera" y
"Ris, veau, cru" se llaman igual y son productos distintos (3 g de grasa
frente a 20). Eso lo mira una persona.

EL ORDEN DE LAS FUENTES ES EL DE `Bases.md`
-------------------------------------------
BEDCA (primaria) → Köber 2017 para el hueso → CIQUAL → USDA. No es una
preferencia estética: es que NINGUNA tiene los 41 nutrientes.

    | Fuente | Yodo | Grasos uno a uno | Aminoácidos | Colina |
    |--------|------|------------------|-------------|--------|
    | BEDCA  | SÍ   | según la ficha   | NO          | NO     |
    | CIQUAL | sí   | SÍ, todas        | NO          | no     |
    | USDA   | NO   | sí               | SÍ, los 12  | SÍ     |

Por eso casi todos los huecos del catálogo están justo donde ninguna
llegaba — no son fallos de copia. Ver `UNIDADES.md`.

LA TRAMPA DE BEDCA QUE HAY QUE MIRAR SIEMPRE
--------------------------------------------
Cada celda de BEDCA lleva un `value_type`:

    AR / BE  + un número  →  es una MEDIDA (aunque el número sea 0)
    LZ       + un 0       →  cero LÓGICO: por composición no puede tener
    TR       + celda vacía →  NO HAY CIFRA. Esto es un HUECO, no un cero

Al volcar BEDCA a una tabla el `TR` vacío se convierte en 0 y ya nadie sabe
que no era una medida. Seis de los huecos cerrados el 7 de septiembre eran
exactamente eso. Por eso esta herramienta IMPRIME EL value_type y no solo
el número: sin él no se puede distinguir un cero de un hueco.
"""
import argparse
import json
import os
import sys
import unicodedata
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

BASE = os.path.dirname(os.path.abspath(__file__))
CATALOGO = os.path.join(BASE, "alimentos_v3_final.json")
# Los volcados pesan 10 MB y no van al repositorio: se bajan una vez y se
# quedan en una carpeta ignorada.
CACHE = os.path.join(BASE, ".fuentes_cache")

URL_BEDCA = "https://www.bedca.net/bdpub/procquery.php"
URL_CIQUAL = ("https://ciqual.anses.fr/cms/sites/default/files/inline-files/"
              "Table%20Ciqual%202020_FR_2020%2007%2007.xls")
URL_USDA = ("https://fdc.nal.usda.gov/fdc-datasets/"
            "FoodData_Central_sr_legacy_food_csv_2018-04.zip")


def _sin_tildes(t):
    t = unicodedata.normalize("NFD", str(t).lower())
    return "".join(c for c in t if unicodedata.category(c) != "Mn")


def _bajar(url, destino):
    if os.path.exists(destino):
        return destino
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    print(f"  bajando {os.path.basename(destino)}...", file=sys.stderr)
    urllib.request.urlretrieve(url, destino)
    return destino


# =============================================================================
# BEDCA — la fuente primaria
# =============================================================================
# ⚠️ ESTA LISTA DE ATRIBUTOS NO SE PUEDE RECORTAR. Es la misma que manda
# `foodresponse1.xsl` del propio BEDCA. Con una lista más corta el servicio
# responde 200 con el cuerpo VACÍO -- no un error, nada -- y se pierde media
# hora buscando el fallo en el sitio equivocado.
_SEL_BEDCA_2 = [
    "f_id", "f_ori_name", "f_eng_name", "sci_name", "langual", "foodexcode",
    "mainlevelcode", "codlevel1", "namelevel1", "codsublevel", "codlevel2",
    "namelevel2", "f_des_esp", "f_des_ing", "photo", "edible_portion",
    "f_origen", "c_id", "c_ori_name", "c_eng_name", "eur_name",
    "componentgroup_id", "glos_esp", "glos_ing", "cg_descripcion",
    "cg_description", "best_location", "v_unit", "moex", "stdv", "min", "max",
    "v_n", "u_id", "u_descripcion", "u_description", "value_type",
    "vt_descripcion", "vt_description", "mu_id", "mu_descripcion",
    "mu_description", "ref_id", "citation", "at_descripcion", "at_description",
    "pt_descripcion", "pt_description", "method_id", "mt_descripcion",
    "mt_description", "m_descripcion", "m_description", "m_nom_esp",
    "m_nom_ing", "mhd_descripcion", "mhd_description",
]


def _bedca_post(xml):
    req = urllib.request.Request(URL_BEDCA, data=xml.encode("utf-8"),
                                 headers={"Content-Type": "text/xml"})
    with urllib.request.urlopen(req, timeout=120) as r:
        return r.read().decode("utf-8", "replace")


def bedca_buscar(texto):
    xml = ('<?xml version="1.0" encoding="utf-8"?><foodquery><type level="1"/>'
           '<selection><atribute name="f_id"/><atribute name="f_ori_name"/>'
           '<atribute name="f_eng_name"/><atribute name="f_origen"/></selection>'
           '<condition><cond1><atribute1 name="f_ori_name"/></cond1>'
           f'<relation type="LIKE"/><cond3>{texto}</cond3></condition>'
           '<condition><cond1><atribute1 name="f_origen"/></cond1>'
           '<relation type="EQUAL"/><cond3>BEDCA</cond3></condition>'
           '<order ordtype="ASC"><atribute3 name="f_ori_name"/></order></foodquery>')
    raiz = ET.fromstring(_bedca_post(xml))
    return [((f.findtext("f_id") or "").strip(), (f.findtext("f_ori_name") or "").strip())
            for f in raiz.iter("food")]


def bedca_ficha(f_id):
    sel = "".join(f'<atribute name="{a}"/>' for a in _SEL_BEDCA_2)
    xml = ('<?xml version="1.0" encoding="utf-8"?><foodquery><type level="2"/>'
           f'<selection>{sel}</selection>'
           '<condition><cond1><atribute1 name="f_id"/></cond1>'
           f'<relation type="EQUAL"/><cond3>{f_id}</cond3></condition>'
           '<condition><cond1><atribute1 name="publico"/></cond1>'
           '<relation type="EQUAL"/><cond3>1</cond3></condition>'
           '<order ordtype="ASC"><atribute3 name="componentgroup_id"/></order>'
           '</foodquery>')
    raiz = ET.fromstring(_bedca_post(xml))
    vals = {}
    for c in raiz.iter("foodvalue"):
        comp = (c.findtext("c_ori_name") or "").strip()
        if comp:
            vals[comp] = ((c.findtext("best_location") or "").strip(),
                          (c.findtext("value_type") or "").strip())
    return (raiz.findtext(".//f_ori_name") or "").strip(), vals


# =============================================================================
# CIQUAL — la tabla 2020 entera, en local
# =============================================================================
_CIQUAL = None


def _ciqual_hoja():
    global _CIQUAL
    if _CIQUAL is None:
        try:
            import xlrd
        except ImportError:
            print("Falta `xlrd` para leer el .xls de CIQUAL: pip install xlrd",
                  file=sys.stderr)
            return None
        ruta = _bajar(URL_CIQUAL, os.path.join(CACHE, "ciqual2020.xls"))
        _CIQUAL = xlrd.open_workbook(ruta).sheet_by_index(0)
    return _CIQUAL


def ciqual_buscar(texto):
    h = _ciqual_hoja()
    if h is None:
        return []
    t = _sin_tildes(texto)
    return [(str(h.cell_value(r, 6)).split(".")[0], h.cell_value(r, 7))
            for r in range(1, h.nrows) if t in _sin_tildes(h.cell_value(r, 7))]


def ciqual_ficha(codigo):
    h = _ciqual_hoja()
    if h is None:
        return "", {}
    cols = [h.cell_value(0, c) for c in range(h.ncols)]
    for r in range(1, h.nrows):
        if str(h.cell_value(r, 6)).split(".")[0] == str(codigo):
            return h.cell_value(r, 7), {cols[c]: h.cell_value(r, c)
                                        for c in range(9, h.ncols)}
    return "", {}


# =============================================================================
# USDA — el volcado oficial de SR Legacy, en local
# =============================================================================
# ⚠️ NO se usa la API: la `DEMO_KEY` contesta OVER_RATE_LIMIT casi siempre,
# porque el límite es por IP y aquí se sale por un proxy compartido. El
# volcado son 6 MB, es la MISMA fuente primaria y no tiene límite ninguno.
_USDA = None


def _usda_tablas():
    global _USDA
    if _USDA is None:
        import csv
        ruta = _bajar(URL_USDA, os.path.join(CACHE, "sr_legacy.zip"))
        carpeta = os.path.join(CACHE, "sr_legacy")
        if not os.path.isdir(carpeta):
            with zipfile.ZipFile(ruta) as z:
                z.extractall(carpeta)
        raiz = next(os.path.join(dp, "food.csv") for dp, _, fn in os.walk(carpeta)
                    if "food.csv" in fn)
        d = os.path.dirname(raiz)
        with open(raiz, newline="", encoding="utf-8") as f:
            comidas = {r["fdc_id"]: r["description"] for r in csv.DictReader(f)}
        with open(os.path.join(d, "nutrient.csv"), newline="", encoding="utf-8") as f:
            nutrientes = {r["id"]: r["name"] for r in csv.DictReader(f)}
        _USDA = (d, comidas, nutrientes)
    return _USDA


def usda_buscar(texto):
    _, comidas, _ = _usda_tablas()
    t = _sin_tildes(texto)
    return sorted((i, d) for i, d in comidas.items() if t in _sin_tildes(d))


# ⚠️ USDA TIENE DOS FILAS LLAMADAS «Energy» Y NO SON LA MISMA UNIDAD: la 1008
# en kcal y la 1062 en kJ. Un diccionario por nombre se queda con la que llegue
# última, que es la de kJ.
#
# ESTO ERA UN FALLO DE ESTA HERRAMIENTA, encontrado el 13 de septiembre al
# barrer el catálogo entero: para el bacalao `usda_ficha` devolvía 343 -- los kJ
# -- y `contrastar` lo comparaba contra nuestros 83 kcal, o sea «⚠ discrepa
# -76 %» en TODA ficha con identificador de USDA. `fijar_identificadores.py` ya
# lo sabía y tenía su propio `_usda_kcal` para esquivarlo; aquí no se arregló
# nunca, así que la herramienta que existe para comparar comparaba mal la única
# columna que desplaza las otras 43 a la vez (todos los requisitos van por 1000
# kcal). Es la lección del araquidónico 20:4 otra vez: el dato no era el error,
# la herramienta lo era.
USDA_ENERGIA_KCAL = "1008"


def usda_ficha(fdc_id):
    import csv
    d, comidas, nutrientes = _usda_tablas()
    vals = {}
    with open(os.path.join(d, "food_nutrient.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["fdc_id"] == str(fdc_id):
                nombre = nutrientes.get(r["nutrient_id"], "?")
                if nombre == "Energy":
                    # solo la fila en kcal; la de kJ se ignora a propósito
                    if r["nutrient_id"] != USDA_ENERGIA_KCAL:
                        continue
                # el valor a secas, como CIQUAL: el `value_type` es cosa de BEDCA
                vals[nombre] = r["amount"]
    return comidas.get(str(fdc_id), ""), vals


# =============================================================================
# EL MAPA DE FUENTES — una sola tabla para las tres, en las unidades de
# UNIDADES.md.
#
# ⚠️ SE LLAMA `MAPA_FUENTES` Y NO `MAPA` A PROPÓSITO. `MAPA` es el nombre de
# LA lista de requisitos de FEDIAF, que vive solo en `verificar.py` y la
# comparten el solver, el semáforo y el analizador. El BLOQUE 24 vigila que
# no haya dos, porque ya hubo dos y no coincidían -- por ahí se coló la fibra
# como requisito inexistente y ocho de ocho menús verdes salían "le falta
# fibra". Esto de aquí es otra cosa (nombres de nutrientes en tres bases de
# datos externas) y no puede llamarse igual ni de lejos.
# =============================================================================
# clave del catálogo -> (nombres en BEDCA, en CIQUAL, en USDA, factor)
# El factor convierte de la unidad de la fuente a la del catálogo. Solo hace
# falta en el araquidónico (las tres lo dan en g, el catálogo lo guarda en mg)
# y en la energía de BEDCA (kJ).
MAPA_FUENTES = {
 "proteina":        (["proteina, total"], ["Protéines, N x 6.25 (g/100 g)"], ["Protein"], 1),
 "grasa":           (["grasa, total (lipidos totales)"], ["Lipides (g/100 g)"], ["Total lipid (fat)"], 1),
 "fibra":           (["fibra, dietetica total"], ["Fibres alimentaires (g/100 g)"], ["Fiber, total dietary"], 1),
 "linoleico":       (["ácido graso 18:2 n-6 cis,cis (ácido linoleico)", "ácido graso 18:2"],
                     ["AG 18:2 9c,12c (n-6), linoléique (g/100 g)"],
                     ["PUFA 18:2 n-6 c,c", "PUFA 18:2"], 1),
 "linolenico":      (["ácido graso 18:3 n-3 cis,cis,cis (ácido linolénico)", "ácido graso 18:3"],
                     ["AG 18:3 c9,c12,c15 (n-3), alpha-linolénique (g/100 g)"],
                     ["PUFA 18:3 n-3 c,c,c (ALA)", "PUFA 18:3"], 1),
 "araquidonico":    (["ácido graso 20:4 n-6  (ácido araquidónico)",
                      "ácido graso 20:4 n-6 (ácido araquidónico)", "ácido graso 20:4"],
                     ["AG 20:4 5c,8c,11c,14c (n-6), arachidonique (g/100 g)"],
                     # ⚠️ `PUFA 20:4` PRIMERO, Y NO `PUFA 20:4 n-6`. USDA
                     # publica las dos filas y NO son coherentes entre sí en
                     # las fichas de ave: el corazón de pavo (FDC 171484) da
                     # 20:4 = 0,205 g y 20:4 n-6 = 0,009 g, veintitrés veces
                     # menos. En tejido animal casi todo el 20:4 ES el n-6,
                     # así que la fila pequeña es la anómala -- y el resto
                     # del catálogo lo confirma: hígado de vaca 289 mg,
                     # hígado de pollo 326, molleja de pollo 86 (donde USDA
                     # ni siquiera trae la fila n-6). El catálogo usa `20:4`
                     # en todas sus fichas, así que la comparación tiene que
                     # usar la misma.
                     # Se descubrió al revés: con `20:4 n-6` primero, esta
                     # herramienta señaló tres fichas de pavo como "20 veces
                     # el valor de USDA" y llegaron a apuntarse como error de
                     # dato. No lo eran. La herramienta lo era.
                     ["PUFA 20:4", "PUFA 20:4 n-6"], 1000),
 "epa":             (["ácido graso 20:5 n-3 (ácido eicosapentaenóico)",
                      "ácido graso 20:5 (ácido eicosapentaenóico)", "ácido graso 20:5"],
                     ["AG 20:5 5c,8c,11c,14c,17c (n-3) EPA (g/100 g)"],
                     ["PUFA 20:5 n-3 (EPA)"], 1),
 "dha":             (["ácido graso 22:6 n-3 (ácido docosahexaenóico)",
                      "ácido graso 22:6 (ácido docosahexaenóico)", "ácido graso 22:6"],
                     ["AG 22:6 4c,7c,10c,13c,16c,19c (n-3) DHA (g/100 g)"],
                     ["PUFA 22:6 n-3 (DHA)"], 1),
 "calcio":          (["calcio"], ["Calcium (mg/100 g)"], ["Calcium, Ca"], 1),
 "fosforo":         (["fósforo"], ["Phosphore (mg/100 g)"], ["Phosphorus, P"], 1),
 "potasio":         (["potasio"], ["Potassium (mg/100 g)"], ["Potassium, K"], 1),
 "sodio":           (["sodio"], ["Sodium (mg/100 g)"], ["Sodium, Na"], 1),
 "magnesio":        (["magnesio"], ["Magnésium (mg/100 g)"], ["Magnesium, Mg"], 1),
 "hierro":          (["hierro, total"], ["Fer (mg/100 g)"], ["Iron, Fe"], 1),
 "cobre":           (["cobre"], ["Cuivre (mg/100 g)"], ["Copper, Cu"], 1),
 "manganeso":       (["manganeso"], ["Manganèse (mg/100 g)"], ["Manganese, Mn"], 1),
 "zinc":            (["zinc (cinc)"], ["Zinc (mg/100 g)"], ["Zinc, Zn"], 1),
 # ⚠️ USDA NO PUBLICA YODO. Si una ficha lo necesita, o sale de BEDCA/CIQUAL
 # o se queda en `sin_dato` -- y el yodo es uno de los cinco topes duros de
 # seguridad crónica, así que un 0 inventado aquí es peligroso de verdad.
 "yodo":            (["ioduro"], ["Iode (µg/100 g)"], [], 1),
 "selenio":         (["selenio, total"], ["Sélénium (µg/100 g)"], ["Selenium, Se"], 1),
 "vitA":            (["Vitamina A equivalentes de retinol de actividades de retinos y carotenoides"],
                     ["Rétinol (µg/100 g)"], ["Vitamin A, RAE"], 1),
 "vitD":            (["Vitamina D"], ["Vitamine D (µg/100 g)"], ["Vitamin D (D2 + D3)"], 1),
 "vitE":            (["Viamina E equivalentes de alfa tocoferol de actividades de vitámeros E"],
                     ["Vitamine E (mg/100 g)"], ["Vitamin E (alpha-tocopherol)"], 1),
 "tiamina":         (["tiamina"], ["Vitamine B1 ou Thiamine (mg/100 g)"], ["Thiamin"], 1),
 "riboflavina":     (["riboflavina"], ["Vitamine B2 ou Riboflavine (mg/100 g)"], ["Riboflavin"], 1),
 "niacina":         (["equivalentes de niacina, totales"],
                     ["Vitamine B3 ou PP ou Niacine (mg/100 g)"], ["Niacin"], 1),
 "acidoPantotenico":(["ácido pantoténico (vitamina B5)"],
                     ["Vitamine B5 ou Acide pantothénique (mg/100 g)"], ["Pantothenic acid"], 1),
 "vitB6":           (["Vitamina B-6, Total"], ["Vitamine B6 (mg/100 g)"], ["Vitamin B-6"], 1),
 "folato":          (["folato, total"], ["Vitamine B9 ou Folates totaux (µg/100 g)"], ["Folate, total"], 1),
 "vitB12":          (["Vitamina B-12"], ["Vitamine B12 (µg/100 g)"], ["Vitamin B-12"], 1),
 # Colina y los doce aminoácidos: SOLO USDA.
 "colina":          ([], [], ["Choline, total"], 1),
 "arginina":        ([], [], ["Arginine"], 1),
 "histidina":       ([], [], ["Histidine"], 1),
 "isoleucina":      ([], [], ["Isoleucine"], 1),
 "leucina":         ([], [], ["Leucine"], 1),
 "lisina":          ([], [], ["Lysine"], 1),
 "metionina":       ([], [], ["Methionine"], 1),
 "cistina":         ([], [], ["Cystine"], 1),
 "fenilalanina":    ([], [], ["Phenylalanine"], 1),
 "tirosina":        ([], [], ["Tyrosine"], 1),
 "treonina":        ([], [], ["Threonine"], 1),
 "triptofano":      ([], [], ["Tryptophan"], 1),
 "valina":          ([], [], ["Valine"], 1),
 # ⚠️ LA ENERGÍA ES LA COLUMNA CON MÁS TRAMPA DE UNIDAD DEL FICHERO, y por eso
 # es la única con un factor POR FUENTE en vez de uno solo:
 #   · BEDCA la publica SOLO en kJ (437,1 kJ para la pechuga de pollo) -> /4,184
 #   · CIQUAL publica cuatro columnas: kJ y kcal, por dos métodos. Se usa la del
 #     Reglamento UE 1169/2011 en kcal, que es la que nos aplica.
 #   · USDA tiene DOS filas «Energy» -- 1008 kcal y 1062 kJ --; `usda_ficha` ya
 #     devuelve solo la de kcal, así que aquí el factor es 1.
 # Y no es cosmético: la energía es el DIVISOR de los 43 requisitos, que van
 # todos por 1000 kcal. Leerla mal los desplaza los 43 a la vez.
 "energia":         (["energía, total"], ["Energie, Règlement UE N° 1169/2011 (kcal/100 g)"],
                     ["Energy"], 1),
 # ⚠️ EL CLORURO SÍ LO PUBLICA ALGUIEN, y hasta el 13 de septiembre este fichero
 # decía que no: estaba en `NO_LO_TIENE_NADIE` y sin entrada aquí, así que un
 # hueco de cloruro NO SE PODÍA CERRAR NUNCA con esta herramienta. CIQUAL lo
 # analiza («Chlorure», código 10170) y `UNIDADES.md` ya lo decía en otra
 # sección: «CIQUAL, que sí lo analiza, da 61 mg para el champiñón donde la
 # derivación da 7,7». Dos sitios del repo afirmando lo contrario, y mandaba el
 # código. BEDCA y USDA no lo publican.
 # ⚠️ Que ahora se PUEDA leer no autoriza a rellenar: en 114 fichas la columna
 # `cloruro` no es una medida, es `sodio` × 1,542, y cambiarla entera es una
 # decisión y no un arreglo. Ver `UNIDADES.md`.
 "cloruro":         ([], ["Chlorure (mg/100 g)"], [], 1),
}
# Ninguna de las tres publica esto. Si falta, falta.
# ⚠️ EL CLORURO SALIÓ DE AQUÍ EL 13 DE SEPTIEMBRE: CIQUAL sí lo publica. Ver el
# comentario de `cloruro` en MAPA_FUENTES.
NO_LO_TIENE_NADIE = ("taurina", "lcarnitina", "purinas")


def _num(x):
    if x is None:
        return None
    s = str(x).strip().replace(",", ".")
    if s in ("", "-") or s.startswith("<"):
        return None      # "< 0,08" es un tope, no una medida: no se usa como cifra
    try:
        return float(s)
    except ValueError:
        return None


def _sacar(vals, nombres, factor, con_tipo=False):
    for n in nombres:
        if n in vals:
            bruto = vals[n]
            v = _num(bruto[0] if con_tipo else bruto)
            if v is not None:
                return v * factor, (bruto[1] if con_tipo else "")
    return None, ""


def contrastar(nombre, b_id=None, c_id=None, u_id=None):
    cat = json.load(open(CATALOGO, encoding="utf-8"))
    ficha = next((a for a in cat if a["nombre"] == nombre), None)
    if ficha is None:
        print(f"«{nombre}» no está en el catálogo."); return 1
    huecos = set(ficha.get("sin_dato") or [])
    ciertos = set(ficha.get("cero_verificado") or {})
    dudosos = set(ficha.get("dato_dudoso") or {})
    nut = dict(ficha["nutrientes"], energia=ficha["energia"])

    nb, vb = bedca_ficha(b_id) if b_id else ("(no consultada)", {})
    nc, vc = ciqual_ficha(c_id) if c_id else ("(no consultada)", {})
    nu, vu = usda_ficha(u_id) if u_id else ("(no consultada)", {})

    print(f"### {ficha['nombre']}  [{ficha['categoria']}]")
    print(f"  BEDCA  {b_id or '-':>8}  {nb}")
    print(f"  CIQUAL {c_id or '-':>8}  {nc}")
    print(f"  USDA   {u_id or '-':>8}  {nu}\n")
    print(f"{'nutriente':18s}{'catálogo':>11s}{'BEDCA':>13s}{'CIQUAL':>11s}{'USDA':>11s}   estado")
    print("-" * 96)

    for k in MAPA_FUENTES:
        if k not in nut:
            continue
        cv = nut[k]
        nb_, nc_, nu_, fac = MAPA_FUENTES[k]
        b, tipo = _sacar(vb, nb_, fac, con_tipo=True)
        c, _ = _sacar(vc, nc_, fac)
        u, _ = _sacar(vu, nu_, fac)
        # BEDCA publica la energía en kJ y el catálogo en kcal
        if k == "energia" and b is not None:
            b = b / 4.184
        # el primero de las tres que tenga cifra, en el orden de Bases.md
        mejor = next((x for x in (b, c, u) if x is not None), None)
        f = lambda v: "·" if v is None else f"{v:,.4g}"
        bedca_txt = f(b) + (f" {tipo}" if tipo else "")
        if k in huecos:
            est = "HUECO -> hay cifra, se puede cerrar" if mejor is not None else "HUECO -> ninguna lo publica"
        elif k in ciertos:
            est = "cero ya verificado"
        elif k in dudosos:
            est = "ya marcado dato_dudoso"
        elif mejor is None:
            est = ""
        elif cv == 0 and mejor > 0:
            est = f"⚠ CERO MUDO (la fuente da {mejor:,.4g})"
        elif abs(cv - mejor) / max(abs(cv), abs(mejor), 1e-9) > 0.20:
            est = f"⚠ discrepa {100*(cv-mejor)/max(abs(mejor),1e-9):+.0f}% — corregir NO es rellenar"
        else:
            est = "ok"
        print(f"{k:18s}{f(cv):>11s}{bedca_txt:>13s}{f(c):>11s}{f(u):>11s}   {est}")

    ciegos = sorted((huecos | {k for k, v in nut.items() if not v}) & set(NO_LO_TIENE_NADIE))
    if ciegos:
        print(f"\nNinguna de las tres publica: {', '.join(ciegos)}")
    print("\nEn BEDCA: AR/BE = medida (aunque valga 0) · LZ = cero lógico · "
          "TR con la celda vacía = NO HAY CIFRA, o sea un hueco.")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    p.add_argument("nombre", nargs="?", help="nombre exacto del alimento en el catálogo")
    p.add_argument("--buscar", help="busca ese texto en las tres fuentes y sale")
    p.add_argument("--bedca"); p.add_argument("--ciqual"); p.add_argument("--usda")
    a = p.parse_args()

    if a.buscar:
        for etiqueta, fn in (("BEDCA", bedca_buscar), ("CIQUAL", ciqual_buscar),
                             ("USDA", usda_buscar)):
            print(f"--- {etiqueta}")
            try:
                for i, d in fn(a.buscar)[:12]:
                    print(f"   {i:10s} {d}")
            except Exception as e:                      # una fuente caída no tumba las otras
                print(f"   (no se pudo consultar: {e})")
        return 0
    if not a.nombre:
        p.print_help(); return 2
    if not (a.bedca or a.ciqual or a.usda):
        print("Sin identificadores no hay nada que contrastar. Búscalos primero:\n"
              f'    python3 contrastar_fuentes.py --buscar "{a.nombre.split()[0].lower()}"\n'
              "y comprueba que el candidato es EL MISMO alimento (energía, proteína y grasa)\n"
              "antes de usarlo: «Timo de ternera» y «Ris, veau, cru» se llaman igual y\n"
              "tienen 20 g y 3 g de grasa.")
        return 2
    return contrastar(a.nombre, a.bedca, a.ciqual, a.usda)


if __name__ == "__main__":
    sys.exit(main())
