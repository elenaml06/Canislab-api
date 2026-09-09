# -*- coding: utf-8 -*-
"""
CANISLAB — Auditoría: NINGUNA TABLA DE FEDIAF SIN VEREDICTO

⚠️ POR QUÉ EXISTE (9 de septiembre de 2026).

Elena preguntó cómo podía ser que no usáramos la Tabla VII-6 de FEDIAF si se
había leído FEDIAF entero. La respuesta estaba escrita en `der.py`, fechada el 6
de septiembre:

    # ⚠️ CORREGIDO 6-sep-2026: es la TABLA VII-7 de FEDIAF (...), no la VII-6
    # (esa es solo por EDAD, sin actividad -- confirmado literal en fediaf_2025.txt

O sea que la tabla SE LEYÓ, se confirmó literal en el PDF, se clasificó bien y se
apartó. Lo que nadie hizo fue cruzar su escalón de edad contra el que aplicábamos
—que venía de otro estudio y era la mitad—. Y ese mismo día, con la tabla de al
lado (la VII-7), había pasado lo mismo con sus dos filas de raza.

**El fallo no es de lectura. Es de no dejar constancia.** «Me lo he leído» no se
puede comprobar; esto sí.

QUÉ HACE. Recorre el texto de FEDIAF, encuentra cada «Table X-n» que aparezca
como encabezado, y exige que TODAS estén en `fediaf_tablas.json` con un veredicto.
Una tabla nueva en una edición futura, o una que nadie clasificó, sale por aquí.

Y al revés: una tabla en el JSON que ya no está en el PDF también se dice, porque
significa que FEDIAF la ha quitado o renumerado y hay que mirar qué pasó con lo
que colgaba de ella.

LO QUE NO HACE. No comprueba las CIFRAS -- de eso va `auditar_fediaf.py`. Aquí
solo se vigila que nadie pueda pasar por delante de una tabla sin decir qué hace
con ella.
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
# El texto de FEDIAF vive en el repo de fuentes, que no siempre está al lado.
RUTAS_FEDIAF = [
    os.path.join(RAIZ, "..", "canislab-fuentes", "FEDIAF", "fediaf_2025.txt"),
    os.path.join(RAIZ, "fuentes", "FEDIAF", "fediaf_2025.txt"),
]

# Tablas que el extractor de texto ve como encabezado pero que son referencias
# dentro de un párrafo, no tablas de verdad. Se listan a mano para no inventar
# veredictos de cosas que no existen.
NO_SON_TABLAS = set()


def _texto_fediaf():
    for r in RUTAS_FEDIAF:
        if os.path.exists(r):
            return open(r, encoding="utf-8", errors="ignore").read()
    return None


def auditar():
    fallos = []
    inventario = json.load(open(os.path.join(RAIZ, "fediaf_tablas.json"), encoding="utf-8"))
    tablas = inventario["tablas"]
    validos = set(inventario["_meta"]["veredictos"])

    for nombre, ficha in sorted(tablas.items()):
        v = ficha.get("veredicto")
        if v not in validos:
            fallos.append(f"la tabla {nombre} tiene el veredicto «{v}», que no es ninguno de {sorted(validos)}")
        # Todo lo que no sea «aplicada» o «felina» tiene que explicarse.
        if v in ("no_aplicable", "alternativa_declarada", "pendiente") and not ficha.get("por_que"):
            fallos.append(f"la tabla {nombre} es «{v}» y no dice POR QUÉ. Un veredicto sin motivo "
                          f"es lo mismo que no tenerlo: dentro de seis meses nadie sabrá si se "
                          f"miró de verdad")
        if v == "aplicada" and not ficha.get("donde"):
            fallos.append(f"la tabla {nombre} dice «aplicada» y no dice DÓNDE. Sin eso no se puede "
                          f"comprobar que siga aplicándose")

    texto = _texto_fediaf()
    if texto is None:
        print("  (no está el texto de FEDIAF: se audita solo el inventario)")
    else:
        encontradas = set()
        for m in re.finditer(r"Table\s+((?:III|VII|VI|IV|V|II|I)-\d+[a-d]?)\b", texto):
            encontradas.add(m.group(1))
        # ⚠️ Y LAS REFERENCIAS AGRUPADAS, que es como FEDIAF nombra las familias:
        # «Tables III-3a,b,c», «Tables VII-17 a-d». Sin esto, la III-3b -- que es LA
        # tabla del motor -- parecia no existir en el PDF, porque solo aparece
        # escrita entera en la fila de la III-3a.
        for m in re.finditer(r"Tables?\s+((?:III|VII|VI|IV|V|II|I))-(\d+)\s*([a-d])\s*[-–]\s*([a-d])", texto):
            pre, num, a, b = m.groups()
            for c in "abcd":
                if a <= c <= b:
                    encontradas.add(f"{pre}-{num}{c}")
        for m in re.finditer(r"Tables?\s+((?:III|VII|VI|IV|V|II|I))-(\d+)((?:\s*[a-d]\s*,)+\s*[a-d])", texto):
            pre, num, letras = m.groups()
            for c in re.findall(r"[a-d]", letras):
                encontradas.add(f"{pre}-{num}{c}")
        encontradas -= NO_SON_TABLAS
        # Una referencia SIN letra («Tables VII-6 - VII-8») nombra a la familia, no a
        # una tabla: se da por cubierta si el inventario tiene cualquiera de sus
        # miembros con letra.
        bases = {re.sub(r"[a-d]$", "", t) for t in tablas}
        for t in sorted(encontradas):
            if t in tablas:
                continue
            if not t[-1].isalpha() and t in bases:
                continue
            if t not in tablas:
                fallos.append(f"FEDIAF trae una «Table {t}» que NO está en fediaf_tablas.json. "
                              f"Alguien tiene que decir qué hace el motor con ella, aunque sea "
                              f"«no_aplicable»: es exactamente lo que pasó con la VII-6")
        for t in sorted(tablas):
            if t not in encontradas:
                fallos.append(f"fediaf_tablas.json trae la «Table {t}» y el PDF de FEDIAF ya no la "
                              f"tiene. O se ha renumerado o se ha quitado: hay que mirar qué pasa "
                              f"con lo que colgaba de ella")

    pendientes = [k for k, v in tablas.items() if v["veredicto"] == "pendiente"]
    print(f"  {len(tablas)} tablas inventariadas, {len(pendientes)} pendientes: {sorted(pendientes)}")
    return fallos


if __name__ == "__main__":
    fs = auditar()
    if fs:
        print(f"\n❌ {len(fs)} problemas:")
        for f in fs:
            print("  -", f)
        sys.exit(1)
    print("Discrepancias: 0")
    sys.exit(0)
