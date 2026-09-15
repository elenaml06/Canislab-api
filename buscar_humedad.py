# -*- coding: utf-8 -*-
"""
LA HUMEDAD DE CADA FICHA, CONTRA SUS FUENTES.

POR QUÉ HACE FALTA, y no es curiosidad: **FEDIAF dice que la conversión desde
% de materia seca ASUME 4,0 kcal/g de materia seca**, y que los valores «should
be corrected for energy density» si es otra. Ese es el puente que usan las 92
cifras de patología de `patologias.json`, las 12 de `recomendaciones_libro.json`
y todas las que salen de SACN5 — o sea, casi todos los límites del motor que no
son de la Tabla III-3b.

Sin la humedad de cada alimento **no se puede ni medir cuánto nos desviamos de
ese 4,0**, porque la materia seca de una ración es
`suma(gramos × (100 − humedad) / 100)` y sin humedad no hay materia seca.

⚠️ LA REGLA ES LA MISMA QUE EN EL BARRIDO DE COMPOSICIÓN DEL 13 DE SEPTIEMBRE, y
las dos frases que la resumen son de Elena: «**ten cuidado con errores de poner
pollo y que te salga repollo**» y «**UN HUECO NO ES UN CERO. SOLO UN CERO ES UN
CERO**».

Por eso aquí NO se busca por nombre: se usa el `fuentes_id` que la ficha YA
declara — el identificador con el que se cerró su composición celda a celda —, y
se baja por la cadena de mandato de `fuentes_de_composicion.json` (BEDCA →
CIQUAL → USDA). Si esa fila no publica el agua, se baja a la siguiente; si
ninguna la publica, la celda se queda como **hueco declarado** diciendo qué se
miró, que es lo que hace `hueco_verificado` con las demás.

⚠️ Y LAS TRES MARCAS QUE NO SON UN NÚMERO, que ya están escritas en `CLAUDE.md`:
el `TR` de BEDCA con la celda vacía (no hay cifra), el `-` de CIQUAL (no
disponible) y el **`< X` de CIQUAL** (límite de detección), que es la traicionera
porque parece casi una cifra.

    python3 buscar_humedad.py            # dice qué encontraría, sin escribir
    python3 buscar_humedad.py --cerrar   # lo escribe en el catálogo
    python3 buscar_humedad.py --instantanea   # congela el agua en fuentes_instantanea.json

⚠️ NO LO EJECUTA LA BATERÍA: necesita red y se baja el volcado de USDA (6 MB) y
la tabla de CIQUAL (3,6 MB). Lo que sí ejecuta la batería es la comprobación
contra `fuentes_instantanea.json`, que es la copia congelada y no necesita red.
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "motor"))

import contrastar_fuentes as CF  # noqa: E402

CATALOGO = os.path.join(RAIZ, "alimentos_v3_final.json")
INSTANTANEA = os.path.join(RAIZ, "fuentes_instantanea.json")

# El orden de mandato, leído del fichero que lo declara. No se escribe aquí:
# sería la segunda copia del orden, que es justo lo que `fuentes_de_composicion`
# existe para impedir.
with open(os.path.join(RAIZ, "fuentes_de_composicion.json"), encoding="utf-8") as _f:
    _FUENTES = json.load(_f)


def _orden_de_mandato():
    fuentes = _FUENTES.get("fuentes") or _FUENTES.get("orden") or {}
    if isinstance(fuentes, dict):
        pares = [(v.get("mandato", 99), k) for k, v in fuentes.items()
                 if isinstance(v, dict)]
    else:
        pares = [(v.get("mandato", 99), v.get("clave")) for v in fuentes]
    orden = [k for _, k in sorted(pares) if k in ("bedca", "ciqual", "usda")]
    return orden or ["bedca", "ciqual", "usda"]


ORDEN = _orden_de_mandato()


def _agua_bedca(fid):
    """(valor, fila, marca) o (None, fila, marca) si esa fila no publica el agua."""
    nombre, vals = CF.bedca_ficha(str(fid))
    for clave, (valor, tipo) in vals.items():
        if "agua" in clave.lower() or "water" in clave.lower():
            # ⚠️ `TR` con la celda vacía es «no hay cifra», no «trazas». Leerlo
            # como cero produce una celda con valor y sin procedencia.
            if not str(valor).strip():
                return None, nombre, f"bedca {tipo} sin cifra"
            return float(str(valor).replace(",", ".")), nombre, f"bedca {tipo}"
    return None, nombre, "bedca no publica el agua en esa fila"


def _agua_ciqual(cid):
    # ⚠️ CIQUAL PUBLICA SUS COLUMNAS EN FRANCÉS, y la primera versión de esta
    # función buscaba «water»: no encontraba nada y declaraba HUECO una celda
    # que la fuente SÍ publica. Es la familia de fallo que el repo ya tiene
    # escrita para `auditar_citas.py` — dar por incomprobable algo que se puede
    # comprobar —, y aquí era peor porque el hueco se escribe en la ficha.
    # El agua es «Eau (g/100 g)». Se ancla al principio de la columna para que
    # no case dentro de otro nombre.
    nombre, vals = CF.ciqual_ficha(str(cid))
    for clave, valor in vals.items():
        _c = str(clave).strip().lower()
        if _c.startswith("eau") or _c.startswith("water"):
            crudo = str(valor).strip()
            if not crudo or crudo == "-":
                return None, nombre, "ciqual sin dato"
            if crudo.startswith("<"):
                # límite de detección: parece una cifra y no lo es
                return None, nombre, f"ciqual límite de detección ({crudo})"
            return float(crudo.replace(",", ".")), nombre, "ciqual"
    return None, nombre, "ciqual no trae la columna"


def _agua_usda(fdc):
    nombre, vals = CF.usda_ficha(str(fdc))
    for clave, valor in vals.items():
        if str(clave).strip().lower() == "water":
            crudo = str(valor).strip()
            if not crudo:
                return None, nombre, "usda sin cifra"
            return float(crudo), nombre, "usda"
    return None, nombre, "usda no publica el agua en esa fila"


_LECTOR = {"bedca": _agua_bedca, "ciqual": _agua_ciqual, "usda": _agua_usda}


def agua_de(ficha):
    """Baja por la cadena de mandato hasta encontrar el agua. Devuelve
    (valor, fuente, id, fila, lo_que_se_miro)."""
    ids = ficha.get("fuentes_id") or {}
    mirado = []
    for fuente in ORDEN:
        fid = ids.get(fuente)
        if not fid:
            continue
        try:
            valor, fila, marca = _LECTOR[fuente](fid)
        except Exception as e:                        # red, fila que no existe…
            mirado.append(f"{fuente}:{fid} error ({type(e).__name__})")
            continue
        mirado.append(f"{fuente}:{fid} {marca}")
        if valor is not None:
            return valor, fuente, fid, fila, mirado
    return None, None, None, None, mirado


# ── LOS QUE NO TIENEN FILA EN NINGUNA BASE ─────────────────────────────────
#
# 33 fichas no tienen `fuentes_id` y no por descuido: son 22 suplementos
# (mandato 5, la etiqueta del fabricante) y 11 piezas con hueso o cartílago,
# y NINGUNA de las tres bases de composición tiene una fila para ellas. Eso no
# las deja sin respuesta: hay tres caminos, y los tres se escriben.

# 1. EL HUESO SALE DE KÖBER, QUE SÍ LO MIDIÓ. Su Tabla 1 publica `DM [%]` para
#    las quince piezas, y la humedad es 100 − DM. Es la MISMA tabla y el MISMO
#    emparejamiento con el que ya salen el calcio y el fósforo de estas fichas,
#    así que no se inventa nada: se lee una columna más de la fila que la ficha
#    ya declara. ⚠️ Eso AMPLÍA el mandato 2, que decía «solo el calcio y el
#    fósforo del hueso», y la ampliación va escrita en
#    `fuentes_de_composicion.json` — un mandato que se estira en silencio es un
#    número sin procedencia.
import auditar_kober as KOBER  # noqa: E402

# 2. UN ACEITE NO TIENE SITIO PARA EL AGUA, y es aritmética, no criterio: con
#    99 o 99,5 g de grasa por cada 100 g queda medio gramo para TODO lo demás,
#    agua incluida. Es el mismo argumento que ya está escrito y aceptado en la
#    ficha del aceite de oliva desde el 13 de septiembre para su zinc. Se
#    escribe 0 y se dice que es una COTA por composición y no una cifra de la
#    fuente.
GRASA_QUE_NO_DEJA_SITIO = 99.0

# 3. UNA FICHA QUE YA ES UN PROXY DECLARADO hereda la humedad por el mismo
#    camino por el que heredó todo lo demás. Hoy es una.
PROXY = {
    "Corazón de conejo": ("Corazón de cordero",
                          "la ficha entera es un PROXY declarado desde agosto "
                          "(«sin dato USDA/CIQUAL de conejo. Estimado a partir de corazon "
                          "de cordero»), así que la humedad viaja por el mismo camino que "
                          "su energía, su proteína y su grasa. No es una medida de conejo."),
}

# 4. LO QUE QUEDA SON POLVOS Y COMPRIMIDOS, y su etiqueta NO declara humedad.
#    Se quedan en hueco DICIENDO qué se miró, que es la diferencia entre «no
#    hay dato» y «nadie ha mirado».


def _sin_fila(ficha, catalogo):
    """Los tres caminos de arriba, en orden. Devuelve (valor, porqué) o
    (None, lo_que_se_miró)."""
    nombre = ficha["nombre"]

    filas = KOBER.DE_DONDE_SALE.get(nombre)
    if filas:
        # columna 2 de la Tabla 1 = DM [%]. Si sale de dos filas, la misma
        # media 50/50 con la que ya se calculan su calcio y su fósforo.
        dm = sum(KOBER.TABLA_1[f][2] for f in filas) / len(filas)
        return 100.0 - dm, (
            "Köber 2017, Tabla 1, columna «DM [%]» de "
            + " + ".join(f"«{f}»" for f in filas)
            + f" = {dm:.2f} % de materia seca, o sea {100.0 - dm:.2f} g de agua por 100 g. "
            "Es la MISMA fila de la que ya salen el calcio y el fósforo de esta ficha. "
            "Ninguna de las tres bases de composición tiene una fila para esta pieza.")

    grasa = (ficha.get("nutrientes") or {}).get("grasa") or 0
    if grasa >= GRASA_QUE_NO_DEJA_SITIO:
        return 0.0, (
            f"COTA POR COMPOSICIÓN, no una cifra de la fuente: la ficha declara {grasa} g de "
            f"grasa por cada 100 g, así que quedan {100 - grasa:g} g para TODO lo demás, agua "
            "incluida. Es el mismo argumento ya escrito y aceptado en la ficha del aceite de "
            "oliva el 13 de septiembre para su zinc. Su etiqueta (mandato 5) no declara humedad "
            "y ninguna base de composición tiene una fila para este producto.")

    if nombre in PROXY:
        de, porque = PROXY[nombre]
        otra = next((f for f in catalogo if f["nombre"] == de), None)
        if otra and otra.get("humedad_g_100g") is not None:
            return otra["humedad_g_100g"], (
                f"PROXY de «{de}» ({otra['humedad_g_100g']} g): " + porque)

    return None, ("no tiene fila en BEDCA, CIQUAL ni USDA (es " + str(ficha.get("categoria"))
                  + ", mandato 5: la etiqueta del fabricante), y la etiqueta no declara "
                    "humedad. Köber 2017 tampoco la mide: su Tabla 1 es de hueso y cartílago.")


def main():
    escribir = "--cerrar" in sys.argv
    congelar = "--instantanea" in sys.argv
    with open(CATALOGO, encoding="utf-8") as f:
        al = json.load(f)

    instant = {}
    if congelar and os.path.exists(INSTANTANEA):
        with open(INSTANTANEA, encoding="utf-8") as f:
            instant = json.load(f)

    cerradas, huecos, sin_id, ya = [], [], [], 0
    for ficha in al:
        if ficha.get("humedad_g_100g") is not None:
            ya += 1
            continue
        if not ficha.get("fuentes_id"):
            valor, porque = _sin_fila(ficha, al)
            if valor is None:
                sin_id.append((ficha["nombre"], porque))
                if escribir:
                    ficha["humedad_hueco"] = "14-sep-2026, buscar_humedad.py: " + porque
                continue
            cerradas.append((ficha["nombre"], valor, "—", "—", porque[:60]))
            if escribir:
                ficha["humedad_g_100g"] = round(valor, 2)
                ficha["humedad_fuente"] = porque
                ficha.pop("humedad_hueco", None)
            continue
        valor, fuente, fid, fila, mirado = agua_de(ficha)
        if valor is None:
            huecos.append((ficha["nombre"], mirado))
            if escribir:
                # ⚠️ NO va en `hueco_verificado`: ese campo es para NUTRIENTES y
                # el BLOQUE 104 exige que su clave esté en `sin_dato` y valga 0
                # dentro de `nutrientes`. La humedad no es un nutriente ni vive
                # ahí, así que meterla dentro pondría roja la batería diciendo
                # una verdad sobre otra cosa. Tiene su propio campo, con lo
                # mismo que exige aquél: qué fuentes se miraron y qué dijo cada una.
                ficha["humedad_hueco"] = (
                    "14-sep-2026, buscar_humedad.py: " + " · ".join(mirado))
            continue
        cerradas.append((ficha["nombre"], valor, fuente, fid, fila))
        if escribir:
            ficha["humedad_g_100g"] = round(valor, 2)
            ficha["humedad_fuente"] = f"{fuente}:{fid} · {fila}"
            # si en una pasada anterior se declaró hueco, deja de serlo
            ficha.pop("humedad_hueco", None)
        if congelar:
            entrada = instant.setdefault("alimentos", {}).setdefault(ficha["nombre"], {})
            entrada.setdefault(fuente, {}).setdefault("celdas", {})["humedad"] = {
                "valor": str(valor), "columna": "agua", "unidad": "G", "value_type": None}
            entrada[fuente].setdefault("id", str(fid))
            entrada[fuente].setdefault("fila", fila)

    print(f"  fichas con humedad de antes: {ya}")
    print(f"  CERRADAS con su fuente:      {len(cerradas)}")
    print(f"  huecos declarados:           {len(huecos)}")
    print(f"  sin fila en ninguna base, HUECO: {len(sin_id)}")
    for n, v, fu, fid, fila in cerradas[:200]:
        print(f"     {v:6.2f} g  {n:36s} {fu}:{fid}  «{fila}»")
    for n, m in huecos:
        print(f"     HUECO   {n:36s} {' · '.join(m)}")
    for n, m in sin_id:
        print(f"     HUECO   {n:36s} {m[:70]}")

    if escribir:
        with open(CATALOGO, "w", encoding="utf-8") as f:
            json.dump(al, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("  catálogo escrito")
    if congelar:
        with open(INSTANTANEA, "w", encoding="utf-8") as f:
            json.dump(instant, f, ensure_ascii=False, indent=1)
            f.write("\n")
        print("  instantánea escrita")
    return 0


if __name__ == "__main__":
    sys.exit(main())
