# -*- coding: utf-8 -*-
"""
CANISLAB — Auditoría: NINGUNA TABLA DE SACN5 SIN VEREDICTO

⚠️ POR QUÉ EXISTE (10 de septiembre de 2026). Elena, esa mañana:

    «sacn5 leido completo significa leido de verdad con todas sus tablas, todos
     sus párrafos y todo bien extraido? no quiero que pase como pasó con FEDIAF
     que estaba "todo leido" y luego resulta que seguian saliendo cosas que
     habias ignorado»

FEDIAF tiene desde el 9 de septiembre `auditar_fediaf_tablas.py`, que exige un
veredicto escrito para cada una de sus tablas, y `leer_fuente.py`, que exige uno
para cada cifra y cada frase normativa de cada sección. SACN5 no tenía **nada**:
había un cuaderno de lectura (`LECTURA_SACN5.md`) y ningún sitio donde
comprobar que no se hubiera saltado nada.

Y ya pasó una vez, y está escrito: `VERIFICACION_FILA_A_FILA.md` §cuarta pasada
cuenta que un barrido de las tablas de SACN5 **se cortó su propia salida con
`sed`**, así que de las que hay solo se revisaron unas 40, y faltaban tres de
patología canina. Un barrido cuyo resultado no se compara contra el total no es
un barrido, es una muestra.

QUÉ HACE. Recorre los 70 textos de capítulo, encuentra cada «Table X-n» y exige
que TODAS estén en `sacn5_tablas.json` con un veredicto. Una tabla sin veredicto
sale por aquí. Y al revés: una del JSON que ya no aparece en el texto también se
dice, porque significa que el extractor cambió y hay que mirar qué pasó con lo
que colgaba de ella.

LO QUE NO HACE, Y HAY QUE DECIRLO CLARO. No lee las tablas: solo comprueba que
ninguna se quede sin que alguien diga qué hace el motor con ella. Un veredicto
`pendiente` es un veredicto honesto -- «nadie lo ha mirado» -- y por eso se
cuentan aparte y el BLOQUE 78 no deja que crezcan.

    python3 auditar_sacn5_tablas.py
"""
import glob
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
# Los textos viven en el repo de fuentes, que no siempre está al lado (en la CI
# no está). Cuando no está, este script lo DICE y no finge haber auditado.
RUTAS_SACN5 = [
    os.environ.get("RUTA_SACN5") or "",
    os.path.join(RAIZ, "..", "canislab-fuentes", "sacn5"),
    os.path.join(RAIZ, "fuentes", "sacn5"),
]

VEREDICTOS = ("aplicada", "citada_en_el_repo", "leida_y_no_aplica", "leida_con_hallazgo",
              "felina", "lista_de_productos", "pendiente")


def carpeta_de_textos():
    for r in RUTAS_SACN5:
        if r and os.path.isdir(r) and glob.glob(os.path.join(r, "cap*.txt")):
            return r
    return None


def tablas_del_texto(carpeta):
    """{«X-n»: [capítulos donde aparece]} leyendo los 70 ficheros."""
    fuera = {}
    for f in sorted(glob.glob(os.path.join(carpeta, "cap*.txt"))):
        m0 = re.match(r"cap(\d+[a-z]?)", os.path.basename(f))
        cap = m0.group(1) if m0 else os.path.basename(f)
        texto = open(f, encoding="utf-8", errors="replace").read()
        for m in re.finditer(r"Table\s+(\d+)-(\d+)", texto):
            fuera.setdefault(f"{m.group(1)}-{m.group(2)}", set()).add(cap)
    return {k: sorted(v) for k, v in fuera.items()}


def auditar():
    inventario = json.load(open(os.path.join(RAIZ, "sacn5_tablas.json"),
                                encoding="utf-8"))["tablas"]
    problemas = []

    # 1. Los veredictos son de la lista, y ninguno se queda mudo.
    for clave, ficha in sorted(inventario.items()):
        v = ficha.get("veredicto")
        if v not in VEREDICTOS:
            problemas.append(f"Tabla {clave}: veredicto «{v}», que no es ninguno de "
                             f"{VEREDICTOS}")
        if v in ("leida_y_no_aplica", "aplicada", "felina", "lista_de_productos") and not (
                ficha.get("nota") or "").strip():
            problemas.append(f"Tabla {clave}: dice «{v}» y no dice POR QUÉ. Un veredicto sin "
                             f"motivo no se puede revisar: es una firma en blanco")

    carpeta = carpeta_de_textos()
    if carpeta is None:
        print(f"  {len(inventario)} tablas en el inventario · "
              f"{sum(1 for f in inventario.values() if f['veredicto'] == 'pendiente')} pendientes")
        print("  (no está el texto de SACN5: no se puede cruzar contra la fuente)")
        return problemas, len(inventario), False

    # 2. Ninguna tabla del libro se queda fuera del inventario.
    en_el_texto = tablas_del_texto(carpeta)
    for clave in sorted(en_el_texto):
        if clave not in inventario:
            problemas.append(
                f"Tabla {clave} (cap. {', '.join(en_el_texto[clave])}) está en SACN5 y NO en "
                f"`sacn5_tablas.json`. Nadie ha dicho qué hace el motor con ella, y eso es "
                f"exactamente lo que este fichero existe para impedir")
    # 3. Y ninguna del inventario ha desaparecido del libro.
    for clave in sorted(inventario):
        if clave not in en_el_texto:
            problemas.append(
                f"Tabla {clave} está en el inventario y ya no aparece en el texto de SACN5. O el "
                f"extractor ha cambiado o la referencia era falsa: hay que mirar qué colgaba de ella")
    return problemas, len(inventario), True


if __name__ == "__main__":
    fallos, n, cruzado = auditar()
    inv = json.load(open(os.path.join(RAIZ, "sacn5_tablas.json"), encoding="utf-8"))["tablas"]
    from collections import Counter
    cuenta = Counter(f["veredicto"] for f in inv.values())
    if cruzado:
        print(f"  {n} tablas de SACN5 · " + " · ".join(
            f"{cuenta[v]} {v}" for v in VEREDICTOS if cuenta[v]))
    print("-" * 60)
    if fallos:
        print(f"\n{len(fallos)} PROBLEMAS:\n")
        for f in fallos[:40]:
            print("  -", f)
        if len(fallos) > 40:
            print(f"  ... y {len(fallos) - 40} más")
        sys.exit(1)
    print("\nNinguna tabla de SACN5 se queda sin veredicto.")
