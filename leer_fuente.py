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
_SENALES = (r"only applies|does not apply|should not|should be|must be|may be required|may need|"
            r"unless|is recommended|recommends|can be lower|can be higher|has to be|needs to be|"
            r"is not to be|shall|it is necessary|may result|may still be safe|does not need|"
            r"do not need|is preferable|it is advisable|are safe|is adequate")
_FRASE = re.compile(r"[^.]*?(?:" + _SENALES + r")[^.]*\.", re.I)


def _texto(fuente):
    for r in FUENTES.get(fuente, []):
        if os.path.exists(r):
            return open(r, encoding="utf-8", errors="ignore").read().split("\n")
    return None


def _clave(tipo, valor):
    """Id estable y corto de un elemento, para que el JSON no dependa de espacios."""
    v = " ".join(str(valor).split())
    return f"{tipo}:{v[:110]}"


def extraer(fuente, seccion, a, b):
    lineas = _texto(fuente)
    if lineas is None:
        raise SystemExit(f"no encuentro el texto de {fuente}")
    plano = " ".join(" ".join(lineas[a - 1:b]).split())
    items = {}
    for n, u in _CIFRA.findall(plano):
        items[_clave("cifra", f"{n} {u}")] = None
    for m in _FRASE.finditer(plano):
        items[_clave("frase", m.group(0))] = None
    return items


def _cargar():
    if os.path.exists(LECTURAS):
        return json.load(open(LECTURAS, encoding="utf-8"))
    return {"_meta": {}, "lecturas": {}}


def auditar():
    datos = _cargar()
    fallos = []
    total = clasificados = 0
    for clave, ficha in sorted(datos.get("lecturas", {}).items()):
        fuente, seccion = clave.split("/", 1)
        a, b = ficha["rango"]
        try:
            items = extraer(fuente, seccion, a, b)
        except SystemExit:
            print(f"  ({fuente}: no está el texto, no se puede auditar {seccion})")
            continue
        veredictos = ficha.get("veredictos", {})
        for it in items:
            total += 1
            if veredictos.get(it):
                clasificados += 1
        sobra = [k for k in veredictos if k not in items]
        for k in sobra:
            fallos.append(f"{clave}: el veredicto «{k[:70]}» ya no corresponde a nada del texto. "
                          f"O cambió el rango de líneas o cambió la fuente")
    # ── Y LA COBERTURA, para las fuentes declaradas completas ────────────
    for fuente in sorted(COMPLETAS):
        lineas = _texto(fuente)
        if lineas is None:
            print(f"  ({fuente}: no está el texto, no se puede medir la cobertura)")
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
    pendientes = total - clasificados
    decl = (datos.get("_meta") or {}).get("pendientes_declarados")
    if decl is not None and pendientes != decl:
        fallos.append(
            f"quedan {pendientes} elementos sin veredicto y el fichero declara {decl}. "
            f"Este numero solo baja cuando alguien lee y resuelve, y lo baja en el mismo "
            f"commit; si ha subido, es que ha cambiado el texto de la fuente o el extractor")
    print(f"  {len(datos.get('lecturas', {}))} secciones leídas · "
          f"{clasificados}/{total} elementos con veredicto · {pendientes} pendientes")
    return fallos


if __name__ == "__main__":
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
