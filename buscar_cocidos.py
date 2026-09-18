#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Qué fila COCIDA EN AGUA existe, para cada alimento del catálogo.

⚠️ POR QUÉ EXISTE (18 de septiembre de 2026). Elena, al ver que el modo
cocinado tenía once fichas contra 105 accesibles: «hay que mirar TODOS los
alimentos, porque las verduras, toda la proteína, el pollo, todo eso se va a
dar distinto. Tienes que tener un catálogo de alimentos igual de rico que el
que tenemos ahora, pero para alimentos cocinados».

Y por una segunda frase suya, que es la que lo hace una herramienta y no una
búsqueda a mano: «no me creo que no haya fichas de estos alimentos hervidos o
al vapor en otras bases de datos. En muchos sitios simplemente pone cocinado».
Tenía razón: yo había dicho que el salmón solo existía al horno mirando la
INSTANTÁNEA CONGELADA, que solo contiene las filas que ya había elegido yo.
Nunca busqué. Buscando de verdad, CIQUAL tiene «Saumon, cuit à la vapeur» con
59 columnas contra las 32 de la fila que usé, y tapa las cuatro celdas que yo
había bajado a USDA.

⚠️ EL ORDEN DE PREFERENCIA NO ES EL DEL MANDATO, y esto es lo que hay que
entender antes de tocarlo. El mandato (BEDCA → Köber → CIQUAL → USDA) decide de
QUIÉN te fías cuando dos fuentes dan cifras distintas del MISMO alimento. Aquí
se decide otra cosa: cuál de las filas de una fuente es EL MISMO ALIMENTO que
nuestra ficha. Una trucha al horno y una trucha al vapor no son la misma comida
por 100 g -- medido: la de horno tiene un 25 % más de materia seca --, así que
una fila de horno de la fuente que manda vale MENOS que una fila hervida de la
siguiente. Primero se elige la fila, y entre las filas válidas manda el mandato.

NO ESCRIBE NADA. Solo dice qué hay.
"""
import json
import sys
import contrastar_fuentes as cf

# ⚠️ CALOR HÚMEDO contra CALOR SECO, y la diferencia no es de matiz: hervir o
# vaporizar deja el agua dentro, hornear o freír la saca. El alimento por 100 g
# es otro. Estas son las palabras con las que cada fuente dice lo primero.
HUMEDO = (
    "bouilli", "cuit à l'eau", "cuit a l'eau", "vapeur", "hervid", "cocid",
    "boiled", "steamed", "simmered", "braised", "poached", "moist heat",
    "stewed", "blanchi", "blanched",
    # ⚠️ «à l'étouffée» es cocer en el propio vapor con la olla tapada, o sea
    # calor HÚMEDO, y faltaba: sin ella la MERLUZA se quedaba sin ficha cocida
    # teniendo «Merlu, cuit à l'étouffée» en CIQUAL. Una palabra que falta en esta
    # lista no da error: deja al alimento fuera del catálogo y no lo dice nadie.
    "etouffee", "étouffée", "etuvee", "étuvée", "papillote",
)
# «cuit, sans précision» de CIQUAL y «cooked» a secas de USDA: la fuente no dice
# el método. CIQUAL lo llama «aliment moyen» -- es su media entre métodos --, así
# que sirve y va en su propia casilla, ni mejor ni peor que el calor húmedo.
GENERICO = ("sans précision", "sans precision", "aliment moyen")
# Calor SECO sin grasa añadida: el horno, la plancha, la parrilla. Cambia el
# agua y poco más, así que sirve cuando no hay nada mejor — diciendo cómo se
# cocina ese alimento.
SECO = ("rôti", "roti", "au four", "four", "grillé", "grille",
        "roasted", "baked", "broiled", "dry heat", "grilled",
        "horno", "plancha", "microondas", "micro-ondes")
# ⚠️ Y FREÍR NO ES UN MÉTODO DE COCCIÓN MÁS: es añadir aceite. Una fila frita
# describe otro alimento —la grasa sube por lo que se le echa, no por lo que
# tiene— y además a un perro no se le da comida frita. La primera versión lo
# metía en el calor seco y el barrido propuso «Boquerón, FRITO» como ficha del
# boquerón. Va con lo que está fuera del todo, no con lo aceptable a falta de algo
# mejor.
FRITO = ("frit", "fried", "poêlé", "poele", "rebozad", "breaded", "panne",
         "empanad", "beignet", "tempura")
# Lo que NO es cocinar: conserva, salazón, ahumado, seco.
FUERA = FRITO + ("fumé", "fume", "smoked", "salé", "sale", "salted", "conserve",
         "canned", "appertisé", "appertise", "séché", "seche", "dried",
         "saumure", "marinad", "ahumad", "salad", "crudo", "cru", "crue",
         "raw", "congel", "frozen", "rebozad", "breaded", "préemballé",
         "preemballe", "sandwich", "pizza", "tarte", "rillettes", "carpaccio",
         "oeufs", "huile", "nuggets", "kippered", "fermented", "lox")


def _clase(nombre):
    n = cf._sin_tildes(nombre).lower()
    if any(cf._sin_tildes(w).lower() in n for w in FUERA):
        return None
    if any(cf._sin_tildes(w).lower() in n for w in HUMEDO):
        return "humedo"
    if any(cf._sin_tildes(w).lower() in n for w in GENERICO):
        return "generico"
    if any(cf._sin_tildes(w).lower() in n for w in SECO):
        return "seco"
    return None


def _num(v):
    t = str(v).strip()
    if not t or t == "-" or t.startswith("<"):
        return None
    try:
        return float(t.replace(",", "."))
    except ValueError:
        return None


# La hoja de CIQUAL se indexa UNA vez: `ciqual_ficha` recorre sus 3.185 filas
# enteras por cada candidato, y con 105 alimentos eso no termina.
_IDX_CIQUAL = None


def _indice_ciqual():
    global _IDX_CIQUAL
    if _IDX_CIQUAL is None:
        h = cf._ciqual_hoja()
        if h is None:
            _IDX_CIQUAL = {}
            return _IDX_CIQUAL
        cols = [h.cell_value(0, c) for c in range(h.ncols)]
        _IDX_CIQUAL = {}
        for r in range(1, h.nrows):
            cod = str(h.cell_value(r, 6)).split('.')[0]
            _IDX_CIQUAL[cod] = (h.cell_value(r, 7),
                                {cols[c]: h.cell_value(r, c)
                                 for c in range(9, h.ncols)})
    return _IDX_CIQUAL


_CACHE_BEDCA = {}


def _mide_bedca(fid):
    """BEDCA también se mide, y es el mandato 1.

    ⚠️ Sin esto, cinco fichas —calabaza, col lombarda, corazón de vaca, judía
    verde y pulpo— salían «no medible» y no se podía comprobar si la fila cocida
    es el mismo alimento. Dejar sin medir la fuente que MANDA es justo al revés.
    """
    if str(fid) in _CACHE_BEDCA:
        return _CACHE_BEDCA[str(fid)]
    import auditar_composicion as ac
    nom, vals = ac._bedca_crudo(cf, str(fid))
    con = sum(1 for v in vals.values() if _num(v[0]) is not None)
    agua = None
    for k, v in vals.items():
        if cf._sin_tildes(k).lower().startswith("agua"):
            agua = _num(v[0])
            break
    _CACHE_BEDCA[str(fid)] = (nom, con, agua)
    return nom, con, agua


_CACHE_USDA = {}


def _mide_ciqual(cod):
    nom, f = _indice_ciqual().get(str(cod), ('', {}))
    con = sum(1 for v in f.values() if _num(v) is not None)
    agua = next((_num(v) for k, v in f.items() if k.startswith("Eau")), None)
    return nom, con, agua


def _mide_usda(fid):
    if str(fid) in _CACHE_USDA:
        return _CACHE_USDA[str(fid)]
    nom, vals = cf.usda_ficha(fid)
    con = sum(1 for v in vals.values() if _num(v) is not None)
    agua = next((_num(v) for k, v in vals.items() if k.lower() == "water"), None)
    _CACHE_USDA[str(fid)] = (nom, con, agua)
    return nom, con, agua


# ─── QUE LA FILA COCIDA SEA EL MISMO ALIMENTO QUE LA CRUDA ────────────────
#
# ⚠️ ESTO NACE DE UN DESASTRE MEDIDO, no de prudencia. La primera versión
# buscaba con la PRIMERA PALABRA del nombre de la fila cruda, y el barrido de los
# 105 alimentos proponía esto:
#
#     Apio            -> «Tapioca, hervida»
#     Bacalao         -> «Mollusks, CUTTLEFISH, cooked» (sepia)
#     Caballa         -> «Mollusks, cuttlefish»
#     Conejo          -> «Game meat, DEER»
#     Coco fresco     -> «Haricot coco, bouilli» (una alubia)
#     Gallina         -> «HUEVO de gallina, hervido»
#     Bazo de vaca    -> «Beef, LIVER, cooked»
#     Hígado de pato  -> «FOIE GRAS, canard, bloc»
#     Col lombarda    -> «Brocoli»
#
# Es el «pollo / repollo» que el repo ya tiene escrito, a escala de catálogo. Y
# con «Foie, lapin, cru» partido por la coma queda «Foie», que casa con
# cualquier hígado del mundo y con el foie gras.
#
# LA REGLA: la fila cruda que ya está verificada es el ANCLA. Su nombre, quitadas
# las palabras de preparación y las vacías, da los tokens que identifican al
# alimento — «cabillaud», o «foie»+«lapin» —, y la fila cocida tiene que
# llevarlos TODOS. No es parecido: es contención.
_VACIAS = {
    "de", "del", "la", "le", "les", "el", "los", "las", "y", "o", "ou", "et",
    "and", "with", "without", "sans", "sin", "con", "au", "aux", "a", "al",
    "en", "the", "of", "all", "mixed", "species", "classes", "total", "only",
    "separable", "lean", "fat", "trimmed", "includes", "foods", "for", "usda",
    "food", "distribution", "program", "may", "have", "been", "previously",
    "drained", "salt", "sal", "aliment", "moyen", "sans", "precision",
    "type", "variety", "meats", "by-products", "products", "flesh", "parte",
    "comestible", "fresco", "fresca", "crudo", "cruda", "cru", "crue", "raw",
    # ⚠️ LOS CALIFICATIVOS DE CRÍA NO PUEDEN SER OBLIGATORIOS. La fila cruda del
    # salmón en CIQUAL se llama «Saumon, cru, ÉLEVAGE» y la cocida buena «Saumon,
    # cuit à la vapeur», sin esa palabra: exigirla dejaba al salmón con «Salmón,
    # plancha» de BEDCA (29 columnas) en vez de la de vapor (59). Que criado y
    # salvaje no son lo mismo es verdad —en el salmón cambia la grasa— pero eso
    # lo mira la comprobación de COMPOSICIÓN, que es donde se puede medir, no una
    # regla de nombres que solo sabe si la palabra está o no está.
    "elevage", "sauvage", "farmed", "wild", "domesticated", "domestique",
    "imported", "importe", "composite", "cuts", "retail", "parts", "young",
    "broilers", "fryers", "broiler", "fryer", "commun", "ou",
}


def _tokens(nombre):
    """Las palabras que IDENTIFICAN el alimento en el nombre de una fila."""
    t = cf._sin_tildes(nombre).lower()
    for c in ",;()/\\-\"'":
        t = t.replace(c, " ")
    fuera = set(_VACIAS)
    for grupo in (HUMEDO, GENERICO, SECO, FUERA):
        for w in grupo:
            for parte in cf._sin_tildes(w).lower().split():
                fuera.add(parte)
    return {p for p in t.split() if len(p) >= 3 and p not in fuera and not p.isdigit()}


def es_el_mismo_alimento(nombre_crudo, nombre_cocido):
    """¿La fila cocida habla del mismo alimento que la cruda ya verificada?"""
    anc = _tokens(nombre_crudo)
    if not anc:
        return False
    return anc <= _tokens(nombre_cocido)


def candidatos(consulta, medir_max=6):
    """Todas las filas COCIDAS de las tres fuentes para esta consulta.

    ⚠️ SE CLASIFICA ANTES DE MEDIR, y no es una optimización cualquiera: sin
    esto el barrido no termina. `usda_buscar("chicken")` devuelve **394 filas** y
    leer los nutrientes de una cuesta ~1 s, porque hay que buscarla en un volcado
    de dos millones de líneas. Medirlas todas son seis minutos por alimento.
    Clasificar por el NOMBRE es gratis, así que primero se tira lo que no es
    comida cocida en agua y solo se miden las `medir_max` mejores de cada fuente.
    """
    out = []
    for fuente, buscar, medir in (
            ("bedca", cf.bedca_buscar, _mide_bedca),
            ("ciqual", cf.ciqual_buscar, _mide_ciqual),
            ("usda", cf.usda_buscar, _mide_usda)):
        try:
            filas = buscar(consulta)
        except Exception as e:                       # una fuente caída no para el resto
            out.append((fuente, None, f"error: {e}", None, None, None))
            continue
        clasificadas = []
        for ident, nombre in filas:
            cl = _clase(nombre)
            if cl:
                clasificadas.append((cl, str(ident), nombre))
        orden = {"humedo": 0, "generico": 1, "seco": 2}
        clasificadas.sort(key=lambda x: orden.get(x[0], 9))
        for k, (cl, ident, nombre) in enumerate(clasificadas):
            con = agua = None
            if medir and k < medir_max:
                try:
                    _, con, agua = medir(ident)
                except Exception:
                    pass
            out.append((fuente, ident, nombre, cl, con, agua))
    orden = {"humedo": 0, "generico": 1, "seco": 2}
    out.sort(key=lambda x: (orden.get(x[3], 9), -(x[4] or 0)))
    return out


def main():
    consultas = sys.argv[1:]
    if not consultas:
        print(__doc__)
        return
    for q in consultas:
        print("=" * 78)
        print(q)
        hay = False
        for fuente, ident, nombre, cl, con, agua in candidatos(q):
            hay = True
            print(f"  [{cl or '?':8}] {fuente:6} {str(ident):>8}  {nombre[:56]:58}"
                  f" celdas={con if con is not None else '?':>4} agua={agua}")
        if not hay:
            print("  (ninguna fila cocida en las tres fuentes)")


if __name__ == "__main__":
    main()
