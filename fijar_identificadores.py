#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FIJAR EL IDENTIFICADOR DE FUENTE DE CADA FICHA DEL CATÁLOGO

POR QUÉ EXISTE (8 de septiembre). El catálogo se ha revisado seis o siete
veces y cada vez se ha vuelto a abrir. La causa no es que los datos estén
mal: es que el catálogo NO ES DIRECCIONABLE. De las 163 fichas, 117 no
tienen ningún identificador de fuente, y las 45 que lo tienen lo llevan
escrito en prosa dentro de `nota_datos` -- «FDC 172343» --, donde ninguna
herramienta puede leerlo.

Sin identificador hay que buscar la ficha por NOMBRE cada vez, y buscar por
nombre falla. Medido el mismo día que se escribió esto: «Atún» devuelve
«Atún en aceite de oliva», «Salmón» devuelve «Queso para untar con salmón»
y «Cardo» devuelve «Anacardo». Como cada búsqueda cuesta y puede salir mal,
cada revisión se permite mirar unas docenas de celdas por un criterio
distinto, y siempre queda un ángulo nuevo por el que volver a entrar.

QUÉ HACE ESTO. Propone, para cada ficha, el identificador de BEDCA, CIQUAL
y USDA que le corresponde, y lo ACEPTA SOLO si la fila candidata coincide
con la nuestra en proteína, grasa y agua. Lo que no llega a ese listón sale
en una lista corta para mirarlo a mano; no se escribe nada dudoso.

⚠️ POR QUÉ PROTEÍNA, GRASA Y AGUA Y NO LA ENERGÍA. USDA y BEDCA publican la
energía en kJ y nosotros en kcal, y una conversión mal hecha convierte una
coincidencia en un descarte. Esos tres van en g por 100 g en las tres
fuentes y en el catálogo: no hay ambigüedad de unidad que valga. Y tres
cifras independientes son una huella: dos alimentos distintos coinciden en
una, casi nunca en tres.

⚠️ EL FALLO QUE ESTO EVITA, con nombre y apellidos: «Timo de ternera» y
«Ris, veau, cru» se llaman lo mismo y tienen 20 g y 3 g de grasa. Aceptar
por nombre es cómo se cargaron 17 celdas de cerebro de VACA en la ficha de
TERNERA. La grasa lo habría cazado.

    python3 fijar_identificadores.py                 # propone y no toca nada
    python3 fijar_identificadores.py --escribir      # escribe solo los SEGUROS

Deja el informe en `identificadores_informe.json` para que la siguiente
sesión no repita el viaje.
"""
import json
import os
import re
import sys

import contrastar_fuentes as cf

RUTA = os.environ.get("CANISLAB_CATALOGO") or os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "alimentos_v3_final.json")
INFORME = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       "identificadores_informe.json")

# Cuánto puede separarse la fila candidata de la nuestra para seguir siendo
# EL MISMO ALIMENTO. No es tolerancia de exactitud -- es de identidad.
# La grasa manda: es la que separa el timo de ternera del de vaca (3 g
# contra 20 g) y la que separa un corte con piel de uno sin ella.
TOLERANCIA = {"proteina": 0.15, "grasa": 0.25, "agua": 0.08,
              "energia": 0.20}
# Por debajo de esto, un porcentaje no dice nada: 0,2 g y 0,4 g de grasa se
# separan un 100 % y son el mismo alimento. Se comparan en absoluto.
SUELO_ABSOLUTO = {"proteina": 1.0, "grasa": 1.0, "agua": 2.0,
                  "energia": 8.0}


def _f(x):
    try:
        return float(str(x).replace(",", "."))
    except (TypeError, ValueError):
        return None


def cuadra(nuestro, suyo, clave):
    """¿Son el mismo alimento en esta magnitud?"""
    a, b = _f(nuestro), _f(suyo)
    if a is None or b is None:
        return None                      # no se puede comparar: no vota
    if abs(a - b) <= SUELO_ABSOLUTO[clave]:
        return True
    if max(a, b) == 0:
        return True
    return abs(a - b) / max(a, b) <= TOLERANCIA[clave]


def ids_en_prosa(ficha):
    """Los identificadores que YA están escritos, pero en prosa.

    ⚠️ No se creen: se devuelven como CANDIDATOS y los verifica el mismo
    listón que a los que salen de una búsqueda. Aquí se coló ya un falso
    positivo -- «CIQUAL 400» era «400 µg de yodo» en la misma frase.
    """
    texto = json.dumps(ficha, ensure_ascii=False)
    fuera = {}
    for fuente, patron in (
            ("usda", r'(?:FDC|FoodData Central|fdcId|fdc_id)\D{0,6}(\d{5,7})'),
            ("bedca", r'BEDCA\D{0,6}(\d{3,5})'),
            ("ciqual", r'CIQUAL\D{0,6}(\d{3,6})')):
        hallado = sorted(set(re.findall(patron, texto)))
        if hallado:
            fuera[fuente] = hallado
    return fuera


# --- cómo se le pregunta a cada fuente por proteína, grasa y agua ----------
def _perfil_usda(fid):
    nombre, vals = cf.usda_ficha(fid)
    return nombre, {"proteina": vals.get("Protein"),
                    "grasa": vals.get("Total lipid (fat)"),
                    "agua": vals.get("Water"),
                    "energia": _usda_kcal(fid)}


def _perfil_bedca(fid):
    nombre, vals = cf.bedca_ficha(fid)
    saca = {}
    for k, (valor, _tipo) in vals.items():
        kk = cf._sin_tildes(k).lower()
        if kk.startswith("proteina"):
            saca["proteina"] = valor
        elif kk.startswith("grasa, total"):
            saca["grasa"] = valor
        elif kk.startswith("agua"):
            saca["agua"] = valor
        elif kk.startswith("energia"):
            saca["energia"] = _kcal_desde(valor, None)
    return nombre, saca


def _perfil_ciqual(fid):
    nombre, vals = cf.ciqual_ficha(fid)
    saca = {}
    for k, valor in vals.items():
        kk = cf._sin_tildes(k).lower()
        if "proteine" in kk and "brute" not in kk:
            saca.setdefault("proteina", valor)
        elif kk.startswith("lipides"):
            saca.setdefault("grasa", valor)
        elif kk.startswith("eau"):
            saca.setdefault("agua", valor)
        elif kk.startswith("energie") and "kcal" in kk:
            saca.setdefault("energia", valor)
        elif kk.startswith("energie") and "energia" not in saca:
            saca["energia"] = _kcal_desde(valor, None)
    return nombre, saca


FUENTES = {"bedca": (cf.bedca_buscar, _perfil_bedca),
           "ciqual": (cf.ciqual_buscar, _perfil_ciqual),
           "usda": (cf.usda_buscar, _perfil_usda)}


# ⚠️ LA HUELLA NUMÉRICA NO BASTA, Y ESTO SE DESCUBRIÓ EN LA PRIMERA PRUEBA.
# Para «Bacalao» la búsqueda devolvió BEDCA 745, «Bacalao AHUMADO», y las
# tres cifras cuadraban: proteína 18,3 contra 18,2, grasa 0,55 contra 1,
# agua 81,2 contra 81,2. Y no es el mismo alimento: ahumar no cambia casi
# nada de esos tres y multiplica el sodio. Cocer tampoco cambia la
# proporción -- cambia el agua, y con ella todo lo demás por 100 g.
#
# Así que un candidato cuyo nombre declara una preparación que el nuestro no
# tiene NO PUEDE SER SEGURO, por bien que cuadren los números.
PREPARACIONES = (
    "ahumad", "cocid", "asad", "frit", "hervid", "guisad", "conserva",
    "en aceite", "escabeche", "salad", "deshidratad", "congelad",
    "rebozad", "empanad", "en salmuera", "curad",
    # ⚠️ AÑADIDAS EL 13 DE SEPTIEMBRE, Y UNA SE COLÓ DE VERDAD. La lista tenía
    # «asad», «frit» y «cocid» y NO TENÍA «horno», así que «Perca, al horno»
    # (BEDCA 831) entró como SEGURO en una ficha de perca CRUDA y se quedó ahí.
    # Hornear pierde agua y concentra todo lo demás por 100 g: por esa fila el
    # barrido de composición acusaba a la vitamina B12 de un error de ×100
    # (nuestro 1 µg contra los 0,01 de la fila horneada; la fila CRUDA de USDA
    # da 1,9). Barrido el resto de las 116 fichas emparejadas con esta lista
    # ampliada: Perca era la única.
    "horno", "plancha", "vapor", "al natural", "enlatad", "almíbar", "almibar",
    "microondas", "gratinad", "marinad", "en su jugo", "precocinad",
    "parrilla", "barbacoa", "pasteurizad", "esterilizad", "liofilizad",
    "en polvo", "concentrad", "triturad", "pelad",
    "cooked", "smoked", "roasted", "fried", "boiled", "braised", "canned",
    "dried", "dehydrated", "frozen", "breaded", "salted", "cured", "baked",
    "grilled", "moist heat", "dry heat", "steamed", "poached", "simmered",
    "toasted", "blanched", "reheated", "rotisserie", "pan-fried",
    "cuit", "fume", "seche", "grille", "roti", "conserve", "appertise",
    "blanchi", "etuve", "poele", "panne", "saumure", "au four",
)

# ⚠️ Y UNA PALABRA QUE PARECE UNA PREPARACIÓN Y NO LO ES, con su caso real.
# «stewing» salía en la lista de arriba hasta el 13 de septiembre, y marcaba
# REVISAR a «Gallina (carne sin hueso)» contra USDA 172400 «Chicken, STEWING,
# meat and skin, raw» -- que cuadra en las tres cifras (17,55/17,3 · 20,33/18,1
# · agua 61,84/61,8). No era un falso negativo del emparejamiento: «chicken,
# stewing» no es pollo guisado, es el TIPO DE AVE (gallina madura, para guisar),
# que es literalmente lo que dice nuestro nombre. Una palabra que en una fuente
# nombra el producto y en otra el método no puede estar en la lista a secas.
NO_SON_PREPARACIONES_AUNQUE_LO_PAREZCAN = {
    "stewing": "«Chicken, stewing» de USDA es el tipo de ave (gallina), no pollo guisado",
}


def preparacion_incompatible(nuestro_nombre, ficha, suyo_nombre):
    """¿El candidato declara una preparación que la ficha nuestra no tiene?"""
    if not suyo_nombre:
        return None
    nuestro = cf._sin_tildes(
        f"{nuestro_nombre} {ficha.get('preparacion') or ''}").lower()
    suyo = cf._sin_tildes(suyo_nombre).lower()
    for p in PREPARACIONES:
        if p in NO_SON_PREPARACIONES_AUNQUE_LO_PAREZCAN:
            continue
        if p in suyo and p not in nuestro:
            return p
    return None


# Un alimento que es casi todo grasa no tiene huella: proteína 0, grasa ~100
# y agua 0 describen a TODOS los aceites del catálogo por igual. Ahí las tres
# cifras no distinguen nada, así que no pueden dar un SEGURO por sí solas.
def sin_huella(ficha):
    nut = ficha.get("nutrientes") or {}
    try:
        return float(nut.get("grasa") or 0) >= 80.0
    except (TypeError, ValueError):
        return False



# ⚠️ LA ENERGÍA, QUE ES LA TERCERA HUELLA Y CASI SE PIERDE. Solo 65 de las
# 163 fichas tienen agua, así que sin una tercera magnitud 52 fichas se
# quedaban en dos votos para siempre. La energía sirve, pero hay que sacarla
# con cuidado: USDA guarda DOS filas de energía -- la 1008 en kcal y la 1062
# en kJ -- con el MISMO nombre, «Energy», así que un diccionario por nombre
# se queda con la que llegue última. Para el bacalao devolvía 343, que son
# los kJ; en kcal son 82. Comparar 343 contra nuestros 82 descarta la fila
# correcta. Se lee por identificador, no por nombre.
USDA_ENERGIA_KCAL = "1008"
KJ_POR_KCAL = 4.184


_KCAL_USDA = None


def _usda_kcal(fid):
    """Las kcal de USDA, indexadas de una vez.

    `food_nutrient.csv` son 2 millones de filas: recorrerlo por cada
    candidato convertía una pasada de 5 minutos en una de horas.
    """
    global _KCAL_USDA
    if _KCAL_USDA is None:
        import csv as _csv
        carpeta, _c, _n = cf._usda_tablas()
        _KCAL_USDA = {}
        with open(os.path.join(carpeta, "food_nutrient.csv"), newline="",
                  encoding="utf-8") as f:
            for r in _csv.DictReader(f):
                if r["nutrient_id"] == USDA_ENERGIA_KCAL:
                    _KCAL_USDA[r["fdc_id"]] = r["amount"]
    return _KCAL_USDA.get(str(fid))


def _kcal_desde(valor_fuente, nuestro_kcal):
    """BEDCA y CIQUAL publican la energía en kJ; nosotros en kcal.

    Se devuelve en kcal. No se adivina la unidad por el número -- se
    convierte siempre, porque las dos publican kJ y punto.
    """
    v = _f(valor_fuente)
    return None if v is None else v / KJ_POR_KCAL


# ⚠️ Y LA TERCERA DEFENSA, QUE CAZÓ EL FALLO QUE YA HABÍAMOS COMETIDO. Para
# «Cerebro de vaca» la huella daba SEGURO con BEDCA 1047, «Sesos de
# TERNERA», y con CIQUAL 40006, «Cervelle, VEAU». Los dos son ternera y la
# ficha es de vaca. Y no es un matiz: el 8 de septiembre hubo que rehacer
# esa ficha entera porque llevaba 17 celdas copiadas del registro de vaca en
# una ficha de ternera. El seso de vaca y el de ternera se parecen en
# proteína, grasa y agua -- por eso la huella no los separa. Lo que los
# separa es la ESPECIE Y LA EDAD, y eso está en el nombre.
#
# Cada grupo es un conjunto de nombres que significan LO MISMO. Dos grupos
# distintos nombrados en los dos nombres = no es el mismo alimento.
ANIMALES = (
    ("vaca", "buey", "bovino", "beef", "boeuf", "ox"),
    ("ternera", "veal", "veau", "vitello"),          # misma especie, otra edad
    ("cerdo", "pork", "porc", "swine", "ham"),
    ("cordero", "lamb", "agneau", "oveja", "mutton", "sheep"),
    ("cabra", "goat", "chevre", "chivo"),
    ("pollo", "chicken", "poulet", "gallina", "hen", "broiler"),
    ("pavo", "turkey", "dinde"),
    ("pato", "duck", "canard"),
    ("conejo", "rabbit", "lapin"),
    ("caballo", "horse", "cheval"),
)


def especie_incompatible(nuestro_nombre, suyo_nombre):
    """¿Los dos nombres apuntan a animales distintos?"""
    if not suyo_nombre:
        return None
    a = cf._sin_tildes(nuestro_nombre).lower()
    b = cf._sin_tildes(suyo_nombre).lower()
    de_a = {i for i, g in enumerate(ANIMALES) if any(x in a for x in g)}
    de_b = {i for i, g in enumerate(ANIMALES) if any(x in b for x in g)}
    if de_a and de_b and not (de_a & de_b):
        return (ANIMALES[sorted(de_a)[0]][0], ANIMALES[sorted(de_b)[0]][0])
    return None


def nuestro_perfil(ficha):
    """Proteína, grasa y agua NUESTRAS, con los huecos declarados fuera.

    Un `sin_dato` no puede votar en la identidad: vale 0 y un 0 falso
    descartaría la fila buena.
    """
    huecos = set(ficha.get("sin_dato") or [])
    nut = ficha.get("nutrientes") or {}
    perfil = {}
    for clave, origen in (("proteina", "proteina"), ("grasa", "grasa")):
        if origen not in huecos:
            perfil[clave] = nut.get(origen)
    if ficha.get("humedad_g_100g") is not None:
        perfil["agua"] = ficha["humedad_g_100g"]
    if ficha.get("energia"):
        perfil["energia"] = ficha["energia"]
    return perfil


def evaluar(ficha, fuente, fid):
    """(veredicto, nombre_en_la_fuente, detalle) para un candidato concreto."""
    _buscar, perfilar = FUENTES[fuente]
    try:
        suyo_nombre, suyo = perfilar(fid)
    except Exception as e:                       # una fuente caída no es un no
        return "ERROR", None, {"error": str(e)[:120]}
    nuestro = nuestro_perfil(ficha)
    detalle, votos = {}, []
    for clave in ("proteina", "grasa", "agua", "energia"):
        if clave not in nuestro or clave not in suyo:
            continue
        ok = cuadra(nuestro[clave], suyo.get(clave), clave)
        if ok is None:
            continue
        detalle[clave] = {"nuestro": nuestro[clave], "suyo": suyo.get(clave),
                          "cuadra": ok}
        votos.append(ok)
    if not votos:
        return "SIN_COMPARAR", suyo_nombre, detalle
    bicho = especie_incompatible(ficha["nombre"], suyo_nombre)
    if bicho:
        detalle["especie_distinta"] = f"nuestro {bicho[0]} contra su {bicho[1]}"
        return "NO", suyo_nombre, detalle
    prep = preparacion_incompatible(ficha["nombre"], ficha, suyo_nombre)
    if prep:
        detalle["preparacion_distinta"] = prep
        # Cuadre perfecto pero preparación distinta: es un candidato que hay
        # que MIRAR, no uno que se acepta ni uno que se descarta.
        return ("REVISAR" if all(votos) else "NO"), suyo_nombre, detalle
    if all(votos) and len(votos) >= 3:
        if sin_huella(ficha):
            detalle["sin_huella"] = "casi todo grasa: las tres cifras no distinguen"
            return "REVISAR", suyo_nombre, detalle
        return "SEGURO", suyo_nombre, detalle
    if all(votos) and len(votos) == 2:
        return "PROBABLE", suyo_nombre, detalle
    if all(votos):
        return "FLOJO", suyo_nombre, detalle
    return "NO", suyo_nombre, detalle


def candidatos(ficha, fuente, buscar_por_nombre=True, tope=4):
    """Los ids a evaluar, del más fiable al menos.

    ⚠️ EL ORDEN IMPORTA Y EL PRIMERO CASI SE PIERDE. `humedad_fdc` ya guarda
    el `fdcId` exacto de 65 fichas, y `humedad_fuente` la descripción
    literal de la fila de USDA -- «Beef, variety meats and by-products,
    liver, raw». Sin usarlos, la búsqueda intentaba «Hígado de vaca» contra
    un índice en inglés y no encontraba nada: 33 alimentos REALES salían
    como «no hay candidato» teniendo su identificador escrito al lado.
    """
    vistos, fuera = set(), []

    def _mete(fid, de_donde):
        if fid and str(fid) not in vistos:
            vistos.add(str(fid))
            fuera.append((str(fid), de_donde))

    if fuente == "usda":
        _mete(ficha.get("humedad_fdc"), "el fdcId de la columna de humedad")
    for fid in ids_en_prosa(ficha).get(fuente, []):
        _mete(fid, "escrito en la ficha")

    if buscar_por_nombre:
        buscar, _p = FUENTES[fuente]
        # La descripción de la fila original es MEJOR consulta que el nombre
        # en español, y para USDA es la única que funciona.
        consultas = [ficha["nombre"]]
        desc = (ficha.get("humedad_fuente") or "").split("·")[-1].strip()
        if desc:
            consultas.insert(0, desc)
        for consulta in consultas:
            try:
                res = buscar(consulta) or []
            except Exception:
                continue
            # ⚠️ SE ORDENAN POR PARECIDO AL NOMBRE, NO SE CORTAN POR ORDEN
            # ALFABÉTICO. Esto costó un alimento entero: «Atún» devuelve siete
            # filas de BEDCA ordenadas alfabéticamente y «Atún, crudo» (2134) es
            # la SEXTA, detrás de cuatro conservas y de «Atún, al horno». Con
            # `tope=4` la fila correcta no llegaba a evaluarse nunca, así que
            # «Atún» se quedó sin un solo identificador teniendo el suyo a dos
            # posiciones del corte. Ordenar por parecido la pone primera.
            for fid, d in sorted(res, key=lambda x: _lejania(consulta, x[1]))[:tope]:
                _mete(fid, f"búsqueda: {d[:60]}")
    return fuera


def _lejania(consulta, candidato):
    """Cuánto se aleja el nombre del candidato del que buscamos.

    Cuenta a favor que estén TODAS las palabras de la consulta, y en contra
    cada palabra que el candidato añade -- que es donde viven «en aceite de
    oliva», «al horno» y «Néctar de». No es una medida fina: solo hace falta
    que la fila buena suba por encima del corte.
    """
    c = set(cf._sin_tildes(consulta).replace(",", " ").split())
    d = set(cf._sin_tildes(candidato).replace(",", " ").split())
    if not c:
        return (9, 9)
    faltan = len(c - d)
    sobran = len(d - c)
    return (faltan, sobran)


def main():
    escribir = "--escribir" in sys.argv
    solo = None
    for i, a in enumerate(sys.argv):
        if a == "--solo" and i + 1 < len(sys.argv):
            solo = sys.argv[i + 1]

    catalogo = json.load(open(RUTA, encoding="utf-8"))
    if solo:
        catalogo = [a for a in catalogo
                    if cf._sin_tildes(solo).lower() in cf._sin_tildes(a["nombre"]).lower()]

    informe, resumen = {}, {"SEGURO": 0, "PROBABLE": 0, "REVISAR": 0, "FLOJO": 0,
                            "NO": 0, "SIN_COMPARAR": 0, "NADA": 0}
    for n, ficha in enumerate(catalogo, 1):
        nombre = ficha["nombre"]
        print(f"[{n:3d}/{len(catalogo)}] {nombre[:44]:44s}", end=" ", flush=True)
        fila = {}
        for fuente in ("bedca", "ciqual", "usda"):
            mejor = None
            for fid, de_donde in candidatos(ficha, fuente):
                veredicto, suyo, detalle = evaluar(ficha, fuente, fid)
                orden = {"SEGURO": 0, "PROBABLE": 1, "REVISAR": 2, "FLOJO": 3,
                         "SIN_COMPARAR": 4, "NO": 5, "ERROR": 6}[veredicto]
                cand = {"id": fid, "veredicto": veredicto, "de_donde": de_donde,
                        "nombre_en_la_fuente": suyo, "detalle": detalle}
                if mejor is None or orden < mejor[0]:
                    mejor = (orden, cand)
                if veredicto == "SEGURO":
                    break
            if mejor:
                fila[fuente] = mejor[1]
        informe[nombre] = fila
        mejores = [v["veredicto"] for v in fila.values()]
        top = min(mejores, key=lambda x: {"SEGURO": 0, "PROBABLE": 1, "REVISAR": 2, "FLOJO": 3,
                                          "SIN_COMPARAR": 4, "NO": 5,
                                          "ERROR": 6}.get(x, 9)) if mejores else "NADA"
        resumen[top] = resumen.get(top, 0) + 1
        print(top)

    json.dump(informe, open(INFORME, "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print()
    print("=" * 66)
    for k, v in resumen.items():
        if v:
            print(f"  {k:14s} {v:3d} fichas")
    print(f"\n  informe completo en {os.path.basename(INFORME)}")

    if escribir:
        # ⚠️ SOLO LOS SEGUROS. Un PROBABLE cuadra en dos de tres y eso es
        # justo lo que hacía «Ris, veau, cru»: proteína y agua parecidas, la
        # grasa a 3 contra 20. Si no vota la grasa, no se escribe.
        d = json.load(open(RUTA, encoding="utf-8"))
        puestos = 0
        for ficha in d:
            fila = informe.get(ficha["nombre"]) or {}
            ids = {f: c["id"] for f, c in fila.items()
                   if c["veredicto"] == "SEGURO"}
            if ids:
                ficha["fuentes_id"] = dict(sorted(ids.items()))
                puestos += 1
        with open(RUTA, "w", encoding="utf-8") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=1)
            fh.write("\n")
        print(f"  escritos `fuentes_id` en {puestos} fichas")
    return 0


if __name__ == "__main__":
    sys.exit(main())
