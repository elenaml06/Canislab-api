# -*- coding: utf-8 -*-
"""
CANISLAB — LEER UNA FUENTE SIN DEJARSE NADA

⚠️ POR QUÉ EXISTE (9 de septiembre de 2026). Elena, después de que una lectura
«completa» de FEDIAF dejara fuera siete cosas, y de que el inventario que se hizo
para arreglarlo dejara fuera otras cuatro:

    «esto no puede pasar en ninguna lectura, por favor.... no sé cómo tienes que
     hacerlo pero apáñatelas para que esto no pase Nunca»

Y el arreglo no puede ser «tener más cuidado», porque eso es exactamente lo que
falló las tres veces. Tiene que ser mecánico.

LA IDEA. «Leída» deja de significar «he pasado los ojos por encima» y pasa a
significar **que ninguna afirmación accionable de esa sección se ha quedado sin
veredicto**. Y quién decide qué es accionable no es el lector: es un extractor.

QUÉ EXTRAE, y por qué estas dos cosas:

1. **Cifras con unidad.** Todo número seguido de g, mg, µg, IU, kcal, kJ, %, ppm...
   Es donde viven los límites. Se nos escapó así el escalón de edad de la Tabla
   VII-6: la tabla se leyó y sus tres números no se cruzaron con los nuestros.

2. **Frases normativas.** Las que llevan «only applies», «does not apply»,
   «should», «must», «unless», «may be required», «can be lower»... Es donde viven
   las REGLAS, que muchas veces no tienen número. Así se nos escapó lo más gordo
   de todo: que el máximo legal solo aplica si el nutriente se añade como aditivo
   (§3.1.3). Un extractor de cifras solo no lo habría cazado, porque no lleva
   ninguna.

CÓMO SE USA

    python3 leer_fuente.py --extraer FEDIAF 3.1     # saca lo que hay que clasificar
    python3 leer_fuente.py --auditar                # falla si algo se quedó sin veredicto

Los veredictos viven en `lecturas_fuentes.json`. Una sección declarada leída con
un solo elemento sin veredicto hace fallar la auditoría, y con ella el BLOQUE 68.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
LECTURAS = os.path.join(RAIZ, "lecturas_fuentes.json")

FUENTES = {
    "FEDIAF": [
        os.path.join(RAIZ, "..", "canislab-fuentes", "FEDIAF", "fediaf_2025.txt"),
    ],
}

# ⚠️ AÑADIDO EL 10 DE SEPTIEMBRE — LA COBERTURA, QUE ERA LA MITAD QUE FALTABA.
#
# Este módulo comprobaba que **lo declarado** tuviera veredicto, y eso pasaba en
# verde con 11 secciones que cubrían el 34 % del documento. O sea: se podía decir
# «FEDIAF leído entero» con dos tercios del texto sin mirar, y la auditoría daba
# la razón. Elena, esta mañana: «anoche me dijiste que de FEDIAF TODO LEÍDO BIEN
# CON TABLAS Y TEXTO, hoy dices que no. ¿Qué está fallando?».
#
# Lo que fallaba es que **una auditoría que solo mira lo declarado premia
# declarar poco**. Ahora una fuente puede declararse COMPLETA, y entonces la
# union de los rangos de sus secciones tiene que ser el 100 % de sus lineas. Sin
# eso, «leída entera» seguiria siendo una afirmacion mia.
COMPLETAS = {"FEDIAF"}

_UNID = r"(?:µg|ug|mg|kg|g|IU|UI|kcal|kJ|MJ|%|ppm)"
_CIFRA = re.compile(rf"(?<![\w.])(\d[\d.,]*)\s*({_UNID})(?![\w])")
# ⚠️ Y AQUI ESTABA EL AGUJERO DE VERDAD, HASTA EL 10 DE SEPTIEMBRE POR LA TARDE.
#
# Esta lista de palabras NO decidia que frases son importantes: decidia cuales
# EXISTIAN. Lo que no llevaba una de ellas no se extraia, asi que no necesitaba
# veredicto, asi que no aparecia como pendiente -- y la auditoria informaba de
# «532 de 532 elementos con veredicto», que suena a documento entero y era
# «532 de los que la lista supo ver».
#
# CASO REAL, y es el que zanja el asunto de los maximos legales. El registro de
# cambios de 2012 (linea 9116) dice:
#
#     «As a general principle it was agreed that no nutritional maximum level
#      WILL BE STATED in the Guidelines for nutrients for which no data on
#      potential adverse effects are available.»
#
# Esa frase es el motivo por el que los seis oligoelementos no tienen maximo
# nutricional -- o sea, la razon por la que el techo legal es el UNICO techo que
# tienen. Lleva «will be stated», que no estaba en la lista, asi que para el
# contador no existia. Medido el mismo dia: de las 1.764 frases del documento la
# lista marcaba 151, y de las 1.613 restantes habia 34 con forma de norma, entre
# ellas «The nutritional maximum (N) is the highest level that is not supposed to
# cause any harmful effect» y «If the product is designed for a specific life
# stage, then the label must clearly state this».
#
# Elena, al verlo: «lee al pie de la letra todo». Asi que ya no filtra nadie: se
# extraen TODAS las frases y todas piden veredicto. La lista se queda, pero solo
# para ORDENAR la cola de pendientes -- las que huelen a norma primero --, que es
# una ayuda para trabajar y no una puerta que deja cosas fuera.
_SENALES = (r"only applies|does not apply|should not|should be|must be|may be required|may need|"
            r"unless|is recommended|recommends|can be lower|can be higher|has to be|needs to be|"
            r"is not to be|shall|it is necessary|may result|may still be safe|does not need|"
            r"do not need|is preferable|it is advisable|are safe|is adequate|will be|was agreed|"
            r"is not supposed|must clearly|is required|are required|is not to|not be taken")
_HUELE_A_NORMA = re.compile(_SENALES, re.I)

# Cortar por frases sin destrozar los numeros ni las abreviaturas. Un `[^.]*\.`
# a secas parte «2.5» en dos y deja 5.459 trozos donde hay 1.764 frases, y un
# recuento inflado con basura es tan poco auditable como uno recortado.
_ABREV = {"e.g", "i.e", "al", "cf", "vs", "approx", "fig", "tab", "no", "dr", "prof",
          "mr", "mrs", "st", "etc", "ca", "resp", "vol", "ed", "eds", "inc", "ltd",
          "co", "jr", "sr", "u.s", "pp", "p", "min", "max", "wt", "sect", "chap"}
_CORTE = re.compile(r"(?<!\d)\.(?!\d)\s+(?=[A-Z0-9\u00ab\"'(])")
_ULTIMA_PALABRA = re.compile(r"([A-Za-z.]+)$")


def _frases(texto):
    """Todas las frases del texto, sin filtrar por contenido."""
    trozos, ini = [], 0
    for m in _CORTE.finditer(texto):
        pal = _ULTIMA_PALABRA.search(texto[ini:m.start()])
        if pal and pal.group(1).lower().rstrip(".") in _ABREV:
            continue                      # «e.g. Table III» no es fin de frase
        t = texto[ini:m.end(0)].strip()
        if t:
            trozos.append(t)
        ini = m.end(0)
    resto = texto[ini:].strip()
    if resto:
        trozos.append(resto)
    return trozos


def _texto(fuente):
    for r in FUENTES.get(fuente, []):
        if os.path.exists(r):
            return open(r, encoding="utf-8", errors="ignore").read().split("\n")
    return None


# ⚠️ Y LA CLAVE LLEVA LA LINEA, DESDE EL 10 DE SEPTIEMBRE POR LA TARDE.
#
# Hasta ahora la clave era solo el texto, asi que **un elemento que aparece dos
# veces en la misma seccion tenia UN solo veredicto**. Suena inofensivo y es
# justo como se cometio el error de hoy:
#
#   La cifra «22,73 µg» sale dos veces en la seccion 3.2.3: una en la tabla
#   FELINA y otra en la NOTA d, que marca la fila de selenio del PERRO. Con una
#   sola clave, el veredicto que se escribio fue «celda de la tabla felina, el
#   motor solo formula para perro» -- verdadero para una de las dos apariciones
#   y FALSO para la que importa. Y la que importa es un techo 2,5 veces mas
#   estricto sobre el selenio anadido (F-28).
#
# Elena, al enterarse: «no me vale que haya cosas que descartes porque si...
# tenemos que asegurarnos de que, de una sola pasada, cuando algo queda leido y
# cerrado esta leido de verdad».
#
# Asi que cada APARICION es un elemento. Medido: 2.015 claves de texto eran
# 2.369 apariciones -- 354 escondidas detras del veredicto de otra.
def _clave(tipo, valor, linea=None):
    """Id de una APARICION concreta: tipo, linea del texto original y contenido."""
    v = " ".join(str(valor).split())
    return f"{tipo}@{linea}:{v[:110]}" if linea is not None else f"{tipo}:{v[:110]}"


def _plano_con_lineas(lineas, a, b):
    """El texto de la seccion en una linea, y donde empieza cada linea original."""
    trozos, marcas, pos = [], [], 0
    for i in range(a, b + 1):
        t = " ".join(lineas[i - 1].split())
        if not t:
            continue
        if trozos:
            pos += 1                      # el espacio que las une
        marcas.append((pos, i))
        trozos.append(t)
        pos += len(t)
    return " ".join(trozos), marcas


def _linea_de(marcas, off):
    linea = marcas[0][1] if marcas else None
    for p, i in marcas:
        if p > off:
            break
        linea = i
    return linea


def extraer(fuente, seccion, a, b):
    lineas = _texto(fuente)
    if lineas is None:
        raise SystemExit(f"no encuentro el texto de {fuente}")
    plano, marcas = _plano_con_lineas(lineas, a, b)
    items = {}

    def _mete(tipo, texto, off):
        # ⚠️ Y SI DOS APARICIONES CAEN EN LA MISMA LINEA, se numeran. Sin esto
        # quedaban 7 pares compartiendo veredicto -- pocas, pero es exactamente
        # el fallo que se esta arreglando, solo que mas dificil de ver.
        base = _clave(tipo, texto, _linea_de(marcas, off))
        k, n = base, 1
        while k in items:
            n += 1
            k = f"{base}#{n}"
        items[k] = None

    for m in _CIFRA.finditer(plano):
        _mete("cifra", f"{m.group(1)} {m.group(2)}", m.start())
    off = 0
    for fr in _frases(plano):
        i = plano.find(fr, off)
        if i < 0:
            i = off
        _mete("frase", fr, i)
        off = i + len(fr)
    return items


# Un veredicto que dice «esto es del gato», y las palabras con las que la fuente
# lo diria de verdad.
_GATO_PALABRA = re.compile(r"felin|gato", re.I)
_AMBOS = re.compile(r"perros?\s+y\s+gatos?|gatos?\s+y\s+perros?|perro\s+y\s+gato", re.I)
_DESCARTE = re.compile(r"no_aplicable|no aplicable|no aplica|no se aplica|se descarta|"
                       r"solo formula para perro|solo perro|no nos aplica", re.I)
_GATO_TEXTO = re.compile(r"\bcats?\b|\bfeline\b|\bkitten", re.I)


def _cargar():
    if os.path.exists(LECTURAS):
        return json.load(open(LECTURAS, encoding="utf-8"))
    return {"_meta": {}, "lecturas": {}}


def auditar():
    datos = _cargar()
    fallos = []
    total = clasificados = 0
    # ⚠️ LAS FUENTES NO ESTAN EN GITHUB ACTIONS, Y ESO NO PUEDE SALIR NI ROJO NI
    # VERDE A SECAS (10 de septiembre). `canislab-fuentes` es otro repositorio y
    # la bateria de la CI no lo clona, asi que alli el extractor no encuentra el
    # texto. Antes eso pasaba en silencio: se imprimia una linea «no está el
    # texto» y la auditoria salia en verde SIN HABER MIRADO NADA -- que es la
    # misma trampa de declarar poco, un piso mas abajo.
    #
    # Y con el recuento de pendientes puesto se volvio rojo, tambien en falso:
    # sin texto salen 0 elementos, 0 no es 269 y la bateria acusaba de haber
    # perdido veredictos.
    #
    # Ninguna de las dos vale. Ahora se dice EXPRESAMENTE que no se ha podido
    # auditar y no se compara nada -- una comprobacion que no se ha hecho tiene
    # que decir que no se ha hecho.
    sin_texto = set()
    for clave, ficha in sorted(datos.get("lecturas", {}).items()):
        fuente, seccion = clave.split("/", 1)
        a, b = ficha["rango"]
        try:
            items = extraer(fuente, seccion, a, b)
        except SystemExit:
            sin_texto.add(fuente)
            continue
        veredictos = ficha.get("veredictos", {})
        for it in items:
            total += 1
            if veredictos.get(it):
                clasificados += 1
        # ⚠️ UN VEREDICTO QUE DESCARTA POR CATEGORIA TIENE QUE PODER
        # COMPROBARSE (10 de septiembre). El error del dia fue descartar la
        # cifra «22,73 µg» como «celda de la tabla FELINA» cuando era la nota d,
        # que marca la fila de selenio del PERRO. Elena: «no me vale que haya
        # cosas que descartes porque si».
        #
        # Asi que si un veredicto dice que algo es del GATO, el texto tiene que
        # decirlo: o el propio elemento, o su linea en la fuente, nombran al
        # gato. Si no lo nombran, el veredicto tiene que explicar por que lo
        # sabe -- y para eso lleva la marca `felino_por:`, que obliga a
        # escribirlo en vez de suponerlo.
        _lineas_f = _texto(fuente) or []
        for k, txt in veredictos.items():
            # «perros y gatos» nombra a los dos: no es un descarte por especie.
            _txt = _AMBOS.sub(" ", txt)
            if not (_GATO_PALABRA.search(_txt) and _DESCARTE.search(_txt)):
                continue
            if "felino_por:" in txt:
                continue
            cuerpo = k.split(":", 1)[1] if ":" in k else k
            n_lin = None
            m_lin = re.search(r"@(\d+)", k.split(":", 1)[0])
            if m_lin:
                n_lin = int(m_lin.group(1))
            alrededor = cuerpo
            if n_lin and 0 < n_lin <= len(_lineas_f):
                alrededor += " " + " ".join(_lineas_f[max(0, n_lin - 3):n_lin + 2])
            if not _GATO_TEXTO.search(alrededor):
                fallos.append(
                    f"{clave}: el veredicto de «{cuerpo[:60]}» lo descarta por FELINO y ni el "
                    f"elemento ni su linea ({n_lin}) nombran al gato. Asi se descarto la nota d "
                    f"del selenio. Si de verdad es felino, escribe `felino_por:` con como se sabe")

        sobra = [k for k in veredictos if k not in items]
        for k in sobra:
            fallos.append(f"{clave}: el veredicto «{k[:70]}» ya no corresponde a nada del texto. "
                          f"O cambió el rango de líneas o cambió la fuente")
    # ── Y LA COBERTURA, para las fuentes declaradas completas ────────────
    for fuente in sorted(COMPLETAS):
        lineas = _texto(fuente)
        if lineas is None:
            sin_texto.add(fuente)
            continue
        cubierto = set()
        for clave, ficha in datos.get("lecturas", {}).items():
            if not clave.startswith(fuente + "/"):
                continue
            a, b = ficha["rango"]
            cubierto |= set(range(a, b + 1))
        n = len(lineas)
        sin = sorted(x for x in range(1, n + 1) if x not in cubierto)
        pct = 100.0 * len(cubierto) / n if n else 0.0
        print(f"  {fuente}: {len(cubierto)}/{n} líneas del texto desglosadas ({pct:.1f} %)")
        if sin:
            tramos, ini = [], sin[0]
            for i, x in enumerate(sin):
                if i + 1 == len(sin) or sin[i + 1] != x + 1:
                    tramos.append((ini, x))
                    if i + 1 < len(sin):
                        ini = sin[i + 1]
            fallos.append(
                f"{fuente} está declarada LEÍDA ENTERA y {len(sin)} de sus {n} líneas no "
                f"están en ninguna sección desglosada. Tramos sin mirar: {tramos[:6]}. "
                f"Una auditoría que solo mira lo declarado premia declarar poco, que es "
                f"exactamente como se pudo decir «FEDIAF leído entero» con el 66 % del "
                f"texto fuera")

    # ── Y EL NUMERO DE PENDIENTES, EXACTO ────────────────────────────────
    #
    # ⚠️ NO se falla por cada elemento sin veredicto, y el motivo importa. Con
    # el fallo por elemento, la unica forma de tener la bateria en verde era
    # declarar pocas secciones -- que es EXACTAMENTE como se pudo decir «FEDIAF
    # leido entero» con el 66 % del texto fuera. Ahora se declara el documento
    # ENTERO y lo que se cuenta es cuanto queda; ese numero se compara EXACTO,
    # como el BLOQUE 78 con las tablas de SACN5, asi que solo baja cuando
    # alguien resuelve elementos y lo baja en el mismo commit.
    for f in sorted(sin_texto):
        print(f"  ⚠️ {f}: NO ESTA EL TEXTO de la fuente, asi que este control NO SE HA HECHO. "
              f"Clona `canislab-fuentes` al lado de este repo para que mire de verdad.")
    pendientes = total - clasificados
    decl = (datos.get("_meta") or {}).get("pendientes_declarados")
    if sin_texto:
        print(f"  {len(datos.get('lecturas', {}))} secciones declaradas · sin comprobar")
        return fallos
    if decl is not None and pendientes != decl:
        fallos.append(
            f"quedan {pendientes} elementos sin veredicto y el fichero declara {decl}. "
            f"Este numero solo baja cuando alguien lee y resuelve, y lo baja en el mismo "
            f"commit; si ha subido, es que ha cambiado el texto de la fuente o el extractor")
    print(f"  {len(datos.get('lecturas', {}))} secciones leídas · "
          f"{clasificados}/{total} elementos con veredicto · {pendientes} pendientes")
    return fallos


def pendientes(seccion=None):
    """Los elementos sin veredicto, los que huelen a norma primero."""
    datos = _cargar()
    for clave, ficha in sorted(datos.get("lecturas", {}).items()):
        if seccion and clave != seccion and not clave.endswith("/" + seccion):
            continue
        fuente, sec = clave.split("/", 1)
        a, b = ficha["rango"]
        items = extraer(fuente, sec, a, b)
        ver = ficha.get("veredictos", {})
        faltan = [k for k in items if not ver.get(k)]
        if not faltan:
            continue
        faltan.sort(key=lambda k: (0 if _HUELE_A_NORMA.search(k) else 1, k))
        print(f"\n## {clave} ({len(faltan)} sin veredicto)")
        for k in faltan:
            print(k)


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--pendientes":
        pendientes(sys.argv[2] if len(sys.argv) > 2 else None)
        sys.exit(0)
    if len(sys.argv) > 1 and sys.argv[1] == "--extraer":
        fuente, seccion = sys.argv[2], sys.argv[3]
        a, b = int(sys.argv[4]), int(sys.argv[5])
        for k in extraer(fuente, seccion, a, b):
            print(k)
        sys.exit(0)
    fs = auditar()
    if fs:
        print(f"\n❌ {len(fs)} elementos sin clasificar:")
        for f in fs[:40]:
            print("  -", f)
        if len(fs) > 40:
            print(f"  ... y {len(fs)-40} más")
        sys.exit(1)
    print("Discrepancias: 0")
    sys.exit(0)
