# -*- coding: utf-8 -*-
"""
LEER SACN5 SIN DEJARSE NADA — EL CONTADOR DEL TEXTO, NO SOLO DE LAS TABLAS.

⚠️ POR QUE EXISTE (10 de septiembre de 2026). Elena:

    «te mandé leer SACN5 todo bien con tablas y texto, y ahora resulta que
     tampoco... ¿qué está fallando?»

Lo que fallaba es que **«leído» significaba tres cosas y se usaban como una**:

  1. Sacado del PDF entero, sin perder texto.
  2. Con veredicto para cada tabla Y CADA FRASE.
  3. Aplicado, o descartado con motivo escrito.

De SACN5 el (1) está hecho y ahora está medido: los 70 capítulos extraen su
texto completo. El (2) estaba hecho **solo para las tablas** —eso es
`sacn5_tablas.json`, y su BLOQUE 78 clava las que faltan—, y del TEXTO no había
contador ninguno. Así que «leído entero» era una afirmación mía, y de las
afirmaciones mías ya sabemos lo que valen: la regla del máximo legal de FEDIAF
no lleva ni un número, y por eso ningún inventario de tablas podía verla.

QUE CUENTA ESTE MODULO, y por qué NO todo

SACN5 no es FEDIAF. FEDIAF es normativo de la primera línea a la última: cada
frase es una regla para un alimento. SACN5 es un libro de clínica, y la mayoría
de sus cifras son epidemiología, dosis de fármaco o descripciones de casos.
Contar sus 6.982 cifras y frases enteras sería un número grande y sin señal.

Así que el filtro es **nutricional y está escrito**: una frase entra si lleva
una cifra con unidad **y** nombra un nutriente, o si es una frase de
recomendación dietética («should contain», «key nutritional factor», «target
level», «should not exceed»...) que nombra un nutriente. Ese es el material del
que sale un límite del motor, y son **3.291** elementos.

⚠️ EL FILTRO ES PARTE DE LO AUDITADO. Si alguien lo relaja, el número de
pendientes baja sin que nadie haya leído nada -- que es la misma trampa de
declarar pocas secciones. Por eso el BLOQUE lo compara EXACTO contra
`_meta.total_declarado`, y ese número solo se toca en el mismo commit en que se
cambia el filtro, explicando por qué.
"""
import json
import os
import re
import sys
import glob

RAIZ = os.path.dirname(os.path.abspath(__file__))
CAPS = os.path.join(RAIZ, "..", "canislab-fuentes", "sacn5")
LECTURAS = os.path.join(RAIZ, "lecturas_sacn5.json")

# Los nutrientes y las palabras de composición que hacen que una cifra sea
# nutricional. Es la lista del MAPA del motor más las que SACN5 usa en sus
# tablas de «key nutritional factors».
_NUT = (r"protein|fat\b|calcium|phosphor|sodium|chloride|potassium|magnesium|copper|iron|"
        r"iodine|selenium|zinc|manganese|vitamin|thiamin|riboflavin|niacin|pyridox|folate|"
        r"cobalamin|choline|biotin|pantothen|linoleic|linolenic|arachidonic|EPA|DHA|omega|"
        r"arginine|histidine|isoleucine|leucine|lysine|methionine|cystine|phenylalanine|"
        r"tyrosine|threonine|tryptophan|valine|taurine|carnitine|fiber|fibre|energy|kcal|"
        r"purine|oxalate|water|moisture|ash|carbohydrate|starch|sugar")
_UN = r"(?:µg|ug|mg|kg|g|IU|UI|kcal|kJ|MJ|%|ppm|mEq)"
_CIFRA = re.compile(rf"[^.]*?(?<![\w.])\d[\d.,]*\s*{_UN}(?![\w])[^.]*\.", re.I)
_RECO = re.compile(r"[^.]*?(?:should contain|should be restricted|should be avoided|"
                   r"is recommended|are recommended|recommended (?:level|amount|range|intake)|"
                   r"key nutritional factor|target level|should be fed|should not exceed|"
                   r"should be limited|restrict dietary|avoid dietary)[^.]*\.", re.I)
_ES_NUT = re.compile(_NUT, re.I)


def capitulos():
    def clave(f):
        m = re.match(r"cap(\d+)([a-z]?)(?:_(\d+))?\.txt", os.path.basename(f))
        return (int(m.group(1)), m.group(2), int(m.group(3) or 0))
    return sorted(glob.glob(os.path.join(CAPS, "*.txt")), key=clave)


def _clave(tipo, valor):
    return f"{tipo}:{' '.join(str(valor).split())[:130]}"


def extraer(ruta):
    """Los elementos NUTRICIONALES de un capítulo, sin repetir."""
    t = " ".join(open(ruta, encoding="utf-8", errors="ignore").read().split())
    items = {}
    for m in _CIFRA.finditer(t):
        if _ES_NUT.search(m.group(0)):
            items[_clave("cifra", m.group(0)[:150])] = None
    for m in _RECO.finditer(t):
        if _ES_NUT.search(m.group(0)):
            items[_clave("reco", m.group(0)[:150])] = None
    return items


def _cargar():
    if os.path.exists(LECTURAS):
        return json.load(open(LECTURAS, encoding="utf-8"))
    return {"_meta": {}, "capitulos": {}}


def auditar():
    datos = _cargar()
    fallos = []
    if not os.path.isdir(CAPS):
        print("  (no está el texto de SACN5: no se puede contar)")
        return fallos
    total = con_veredicto = 0
    por_cap = {}
    for ruta in capitulos():
        nombre = os.path.basename(ruta)[:-4]
        items = extraer(ruta)
        ficha = (datos.get("capitulos") or {}).get(nombre) or {}
        ver = ficha.get("veredictos") or {}
        n_ok = sum(1 for k in items if ver.get(k))
        total += len(items)
        con_veredicto += n_ok
        por_cap[nombre] = (len(items), n_ok)
        sobra = [k for k in ver if k not in items]
        if sobra:
            fallos.append(f"SACN5/{nombre}: {len(sobra)} veredictos ya no corresponden a nada "
                          f"del texto ({sobra[0][:70]}...). O cambió el filtro o cambió el texto")
    pend = total - con_veredicto
    declarado = (datos.get("_meta") or {}).get("total_declarado")
    pend_decl = (datos.get("_meta") or {}).get("pendientes_declarados")
    print(f"  {len(por_cap)} capítulos · {total} elementos nutricionales · "
          f"{con_veredicto} con veredicto · {pend} pendientes")
    if declarado is not None and total != declarado:
        fallos.append(
            f"SACN5: el filtro saca {total} elementos y el fichero declara {declarado}. Si se "
            f"ha tocado el filtro, el número de pendientes baja sin que nadie haya leído nada. "
            f"Se cambia el declarado en el MISMO commit y se dice por qué")
    if pend_decl is not None and pend != pend_decl:
        fallos.append(
            f"SACN5: quedan {pend} elementos sin veredicto y el fichero declara {pend_decl}. "
            f"Este número baja SOLO cuando alguien resuelve elementos y lo baja en el mismo "
            f"commit -- exacto, como el BLOQUE 78 con las tablas")
    return fallos


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--extraer":
        for k in extraer(os.path.join(CAPS, sys.argv[2] + ".txt")):
            print(k)
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "--recuento":
        for ruta in capitulos():
            n = os.path.basename(ruta)[:-4]
            print("%-14s %5d" % (n, len(extraer(ruta))))
        sys.exit(0)
    fs = auditar()
    for f in fs:
        print("  ✗", f)
    print("\nDiscrepancias:", len(fs))
    sys.exit(1 if fs else 0)
