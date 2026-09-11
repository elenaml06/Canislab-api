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
_CIFRA = re.compile(rf"(?<![\w.])\d[\d.,]*\s*{_UN}(?![\w])", re.I)
_RECO = re.compile(r"(?:should contain|should be restricted|should be avoided|"
                   r"is recommended|are recommended|recommended (?:level|amount|range|intake)|"
                   r"key nutritional factor|target level|should be fed|should not exceed|"
                   r"should be limited|restrict dietary|avoid dietary)", re.I)
_ES_NUT = re.compile(_NUT, re.I)


def capitulos():
    def clave(f):
        m = re.match(r"cap(\d+)([a-z]?)(?:_(\d+))?\.txt", os.path.basename(f))
        return (int(m.group(1)), m.group(2), int(m.group(3) or 0))
    return sorted(glob.glob(os.path.join(CAPS, "*.txt")), key=clave)


# ⚠️ LOS TRES ARREGLOS DEL 10 DE SEPTIEMBRE POR LA TARDE, Y LOS TRES SALEN DE UN
# FALLO REAL EN FEDIAF, NO DE UNA MEJORA TEORICA.
#
# 1. UNA CLAVE POR APARICION, NO POR TEXTO. En FEDIAF la clave era solo el texto,
#    asi que un elemento que salia dos veces en la misma seccion tenia UN solo
#    veredicto -- y el veredicto escrito valia para una de las dos. Asi se
#    descarto como «celda de la tabla felina» la NOTA d, que es un techo del
#    PERRO 2,5 veces mas estricto sobre el selenio anadido. Aqui, con 70
#    capitulos de un libro de clinica, la misma frase se repite mucho mas.
#
# 2. UN CORTADOR DE FRASES QUE NO PARTA LOS NUMEROS. El `[^.]*` de antes corta
#    «2.5 mg» en dos, asi que media frase se pierde y la otra media entra
#    truncada. Se usa el mismo cortador que FEDIAF.
#
# 3. Y LO QUE EL FILTRO DESCARTA, CONTADO. El filtro nutricional sigue siendo
#    necesario -- SACN5 es un libro de clinica y la mayoria de sus cifras son
#    epidemiologia o dosis de farmaco --, pero HASTA HOY LO QUE DESCARTABA ERA
#    INVISIBLE, que es exactamente el agujero que tenia FEDIAF. Medido el 10 de
#    septiembre: 36.206 frases en el libro, 3.140 dejaba pasar el filtro y
#    33.066 se caian sin que nadie las viera. De esas, 340 tienen forma de NORMA
#    DIETETICA segun un patron INDEPENDIENTE del filtro -- y esas 340 entran
#    ahora en la cuenta, marcadas `olor`, porque son justo donde puede estar
#    escondido un limite que el motor deberia aplicar.
#
# El total de descartadas se imprime siempre, para que el tamaño del punto ciego
# se vea en cada ejecucion en vez de deducirse.
_ABREV = {"e.g", "i.e", "al", "cf", "vs", "approx", "fig", "tab", "no", "dr", "prof",
          "mr", "mrs", "st", "etc", "ca", "resp", "vol", "ed", "eds", "inc", "ltd",
          "co", "jr", "sr", "u.s", "pp", "p", "min", "max", "wt", "sect", "chap"}
_CORTE = re.compile(r"(?<!\d)\.(?!\d)\s+(?=[A-Z0-9\u00ab\"'(])")
_ULTIMA = re.compile(r"([A-Za-z.]+)$")

# Huele a norma dietetica SIN usar las palabras del filtro. Es el control
# independiente: si el filtro se dejara algo importante, esto lo caza.
_OLOR = re.compile(r"\b(?:will be|was agreed|must (?:be|not)|shall|ought to|"
                   r"is (?:not )?(?:advis|indicat|contraindicat)|do(?:es)? not need|"
                   r"no more than|at least|upper limit|maximum (?:of|level|intake)|"
                   r"minimum (?:of|level|intake)|toxicit|deficien|excess)\b", re.I)
_COMIDA = re.compile(r"\b(?:diet|dietary|food|feeding|ration|nutrient|supplement|intake)\b", re.I)


def _frases(texto):
    trozos, ini = [], 0
    for m in _CORTE.finditer(texto):
        pal = _ULTIMA.search(texto[ini:m.start()])
        if pal and pal.group(1).lower().rstrip(".") in _ABREV:
            continue
        t = texto[ini:m.end(0)].strip()
        if t:
            trozos.append(t)
        ini = m.end(0)
    resto = texto[ini:].strip()
    if resto:
        trozos.append(resto)
    return trozos


# El guion de corte de linea del PDF: «sele- nium» es «selenium». Ver el
# comentario largo dentro de `extraer`.
_SIN_GUION = re.compile(r"-\s+")


def _clave(tipo, valor, n=None):
    v = " ".join(str(valor).split())[:130]
    return f"{tipo}#{n}:{v}" if n is not None else f"{tipo}:{v}"


def extraer(ruta, con_descartadas=False):
    """Los elementos NUTRICIONALES de un capítulo, UNA CLAVE POR APARICION."""
    return extraer_de_texto(open(ruta, encoding="utf-8", errors="ignore").read(),
                            con_descartadas=con_descartadas)


def extraer_de_texto(crudo, con_descartadas=False):
    """El mismo filtro, sobre un texto ya cargado.

    ⚠️ SE PARTE EN DOS EL 11 DE SEPTIEMBRE porque NRC 2006 viene en UN SOLO .txt
    de 43.556 líneas y hay que contarlo por capítulos, que se cortan en memoria.
    `leer_nrc2006.py` y `leer_fascetti.py` llaman aquí **a propósito**: un filtro,
    una definición. Dos filtros parecidos en dos ficheros son dos filtros que se
    separan, y entonces «elemento nutricional» significa una cosa en un libro y
    otra en el de al lado, sin que nadie lo vea. Si el filtro cambia, cambian los
    tres recuentos a la vez, que es lo que hace falta para que un número clavado
    signifique algo.
    """
    t = " ".join(crudo.split())
    items, descartadas = {}, 0
    for i, fr in enumerate(_frases(t)):
        # ⚠️ EL FILTRO SE PRUEBA SOBRE LA FRASE SIN EL GUION DE CORTE DE LINEA,
        # Y ESTO NO ES COSMETICO (10 de septiembre, de noche, preguntandolo Elena:
        # «cuando dices leido elemento a elemento estas teniendo cuidado con las
        # columnas para leerlo bien, leyendo cada frase y cada tabla?»).
        #
        # El PDF parte palabras al final de linea, y al juntar el texto queda
        # «sele- nium», «phos- phorus», «vita- min». La lista de nutrientes busca
        # «selenium», asi que NO LO ENCONTRABA y la frase se descartaba entera.
        #
        # Encontrado mirando lo que el filtro tiraba en un capitulo YA LEIDO: de
        # 463 frases descartadas del cap.13, cuatro llevaban cifra con unidad, y
        # una era «the recommended range of sele- nium for adult dog foods is 0.5
        # to 1.3 mg/kg (DM)» -- justo la cifra del hallazgo S-11, tirada por un
        # guion. Medido en todo el libro: **196 frases**.
        #
        # Es la MISMA familia que el fallo de las dos columnas: un artefacto del
        # PDF cambiando en silencio lo que se lee. La CLAVE se sigue construyendo
        # con el texto original -- si no, los veredictos ya escritos perderian su
        # clave --; lo unico que se de-guiona es la copia con la que se decide.
        # ⚠️ Y SE PRUEBA SOBRE LAS DOS FORMAS, no solo sobre la de-guionada.
        # Quitar el guion arregla «sele- nium» y ROMPE «non-nutritional» ->
        # «nonnutritional» y «deficien- cy» -> «deficiency», que es donde
        # enganchaba `_OLOR`. Medido: de-guionando a secas entraban 51 frases
        # nuevas y se CAIAN tres, y una de las tres era el aviso de calcio y zinc
        # que este repo ya cita. Probar las dos formas solo puede ENSANCHAR, que
        # es el lado seguro de un filtro cuyo punto ciego se cuenta.
        _dos = (fr, _SIN_GUION.sub("", fr))
        _hay = lambda _rx: any(_rx.search(_x) for _x in _dos)
        _olor_ok = _hay(_OLOR) and _hay(_COMIDA) and len(fr) > 60
        if not _hay(_ES_NUT):
            # ni siquiera nombra un nutriente: solo entra si huele a norma
            if _olor_ok:
                items[_clave("olor", fr[:150], i)] = None
            else:
                descartadas += 1
            continue
        if _hay(_CIFRA):
            items[_clave("cifra", fr[:150], i)] = None
        elif _hay(_RECO):
            items[_clave("reco", fr[:150], i)] = None
        elif _olor_ok:
            items[_clave("olor", fr[:150], i)] = None
        else:
            descartadas += 1
    return (items, descartadas) if con_descartadas else items


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
    total = con_veredicto = descartadas = 0
    por_cap = {}
    for ruta in capitulos():
        nombre = os.path.basename(ruta)[:-4]
        items, _desc = extraer(ruta, con_descartadas=True)
        descartadas += _desc
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
    # ⚠️ EL PUNTO CIEGO, IMPRESO SIEMPRE (10 septiembre). Lo que el filtro tira
    # era invisible, que es el agujero que tenia FEDIAF: alli «532 de 532» sonaba
    # a documento entero y era «532 de los que la lista supo ver». Aqui el filtro
    # SIGUE HACIENDO FALTA -- SACN5 es un libro de clinica --, pero su tamaño se
    # ve en cada ejecucion y se compara exacto, para que no pueda crecer solo.
    print(f"  {descartadas} frases descartadas por el filtro nutricional "
          f"(de {total + descartadas} frases del libro)")
    desc_decl = (datos.get("_meta") or {}).get("descartadas_declaradas")
    if desc_decl is not None and descartadas != desc_decl:
        fallos.append(
            f"SACN5: el filtro descarta {descartadas} frases y el fichero declara {desc_decl}. "
            f"Si sube, el filtro se ha vuelto mas estrecho y hay material nuevo que nadie ve; "
            f"si baja sin que el total suba, alguien lo ha relajado. Se cambia en el MISMO "
            f"commit y se dice por que")
    if declarado is not None and total != declarado:
        fallos.append(
            f"SACN5: el filtro saca {total} elementos y el fichero declara {declarado}. Si se "
            f"ha tocado el filtro, el número de pendientes baja sin que nadie haya leído nada. "
            f"Se cambia el declarado en el MISMO commit y se dice por qué")
    # ============================================================
    # LA LECTURA INTEGRA, CONTADA APARTE
    # ============================================================
    #
    # ⚠️ POR QUE EXISTE (10 de septiembre, de noche). Elena, despues de ver como
    # se estaban resolviendo los elementos capitulo a capitulo:
    #
    #     «por favor no puedes leer todo sin hacer cossd raras de seleccionar
    #      frases y cosas asi? simplemente leer como si fueses un opositoe
    #      estudiando»
    #
    # Y tenia razon, y el fallo era mio y de bulto: **el filtro es para CONTAR y
    # lo estaba usando para DECIDIR QUE LEO**. Un elemento resuelto significa
    # «esta frase la he mirado», no «este capitulo lo he leido»; y como el filtro
    # tira 33.207 frases de 36.206, resolver los 2.999 elementos del libro entero
    # dejaria **el 92 % del texto sin abrir**. Se comprobo releyendo el cap.36
    # entero justo despues: aparecieron los estadios ACC/AHA y la frase «from
    # Class I to Class III or IV following a salty meal», y el filtro no habia
    # sacado ninguna de las dos.
    #
    # Asi que hay DOS contadores y miden cosas distintas, y por eso van
    # separados: `pendientes_declarados` cuenta FRASES con veredicto y este
    # cuenta CAPITULOS leidos de principio a fin. Un capitulo no cuenta aqui
    # hasta que su `lectura_integra` declara el numero de lineas del .txt, y ese
    # numero se comprueba contra el fichero: si alguien vuelve a extraer el texto
    # y cambia de tamaño, la declaracion queda vieja y esto falla -- que es lo
    # correcto, porque lo que se leyo ya no es lo que hay.
    caps_datos = datos.get("capitulos") or {}
    enteros = []
    for _n in sorted(por_cap):
        _li = ((caps_datos.get(_n) or {}).get("lectura_integra") or {})
        if not _li:
            continue
        _dicho = _li.get("lineas")
        _real = sum(1 for _ in open(os.path.join(CAPS, _n + ".txt"),
                                    encoding="utf-8", errors="ignore"))
        if _dicho != _real:
            fallos.append(
                f"SACN5/{_n}: la lectura integra declara {_dicho} lineas y el .txt tiene "
                f"{_real}. O se declaro mal o el texto se ha vuelto a extraer -- y en ese "
                f"caso lo que se leyo ya no es lo que hay, y hay que releerlo")
            continue
        enteros.append(_n)
    ent_decl = (datos.get("_meta") or {}).get("capitulos_leidos_enteros_declarados")
    print(f"  {len(enteros)} de {len(por_cap)} capitulos LEIDOS ENTEROS "
          f"(no es lo mismo que resolver sus elementos: el filtro tira el "
          f"{100.0 * descartadas / (total + descartadas):.0f} % de las frases)")
    if ent_decl is not None and len(enteros) != ent_decl:
        fallos.append(
            f"SACN5: hay {len(enteros)} capitulos con lectura integra declarada y el fichero "
            f"dice {ent_decl}. Sube SOLO cuando alguien lee un capitulo entero y lo sube en "
            f"el mismo commit")

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
