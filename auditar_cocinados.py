# -*- coding: utf-8 -*-
"""
UNA FICHA COCIDA CONTRA SUS FUENTES, QUE NO ES LO MISMO QUE UNA CRUDA
=====================================================================

POR QUE EXISTE (17 de septiembre de 2026). Elena, al entrar los hidratos:
«pues ve mirando en otras bases de datos con el orden que tenemos de prioridad
tambien si el arroz esta mal. TIENES QUE PASAR TODOS LOS ALIMENTOS BIEN A LA
PRIMERA, PORQUE LUEGO NOS ENCONTRAMOS CON QUE HAS PASADO DATOS MAL, HAS MEZCLADO
COLUMNAS...»

`auditar_composicion.py` compara el catalogo contra la fuente CELDA A CELDA y
eso sigue siendo lo que manda. Lo que no puede hacer es decidir CUAL DE LAS DOS
esta mal cuando no coinciden -- solo dice que discrepan, y por eso tiene 315
discrepancias declaradas y sin tocar, con razon. En un alimento COCIDO hay dos
comprobaciones mas que si pueden decidirlo, y las dos encontraron un fallo real
el dia que se escribieron.

1. LAS TRES FUENTES, NORMALIZADAS A MATERIA SECA
   Un alimento cocido lleva el agua que le eche quien cocina: CIQUAL hierve el
   arroz blanco hasta un 63,9 % de agua y USDA hasta un 68,4 %, asi que sus
   cifras por 100 g NO tienen por que coincidir y compararlas a pelo acusa a
   fuentes que estan bien. En SECO si tienen que coincidir: es el mismo grano.
   Y esa es justo la forma de cazar una COLUMNA MEZCLADA, que es lo que se
   pregunta arriba: la variacion biologica entre dos bases del mismo alimento
   es de un factor 2 como mucho, y leer la columna de al lado da 10, 100 o 1000.

2. CADA FILA COCIDA CONTRA LA FILA CRUDA DE **SU MISMA** BASE
   Aqui la direccion es conocida y eso es lo que permite decidir: en materia
   seca, cocer en agua solo puede CONSERVAR o PERDER. No se crean minerales.
   Asi salio que `bedca:1009` «Arroz integral, hervido» declara 9,8 ug de
   selenio cuando su propia fila cruda (`bedca:904`) da 2 -- 15 veces mas
   despues de hervir --, y que la riboflavina de la quinoa cocida de CIQUAL
   pierde el 90 % contra su cruda porque su medida de B2 en cocido esta en el
   limite de deteccion.

⚠️ Y LA LECCION DEL PROPIO SCRIPT, que puso roja su primera version: LAS FILAS
CRUDAS DE REFERENCIA HAY QUE MIRARLAS. `ciqual:9101` parece la del arroz blanco
crudo y es «Riz blanc ETUVE, cru» -- vaporizado, que mete en el grano el hierro
y las vitaminas del salvado --, y `usda:168878` es la fila COCIDA y ENRIQUECIDA.
Con esas dos, el script acusaba al arroz blanco de perder el 90 % del hierro y
de la niacina, y no era verdad: eran SEIS falsos positivos de trece. Es la
leccion del araquidonico 20:4 otra vez -- «no lo eran, la herramienta lo era».
Por eso `FILA_CRUDA` lleva el NOMBRE de cada fila escrito al lado, y el script
lo comprueba contra lo que devuelve la fuente antes de usarla.

⚠️ Y UNA COSA QUE ESTE SCRIPT **NO** DECIDE, porque no es un fallo: las filas
cocidas de CIQUAL son de alimento hervido en AGUA ABUNDANTE Y ESCURRIDO, y las
de USDA por ABSORCION. Se lee en sus propias cenizas (0,13 g contra 0,41 g en el
arroz blanco) y en que CIQUAL conserva el 43 % del potasio y el 41 % del zinc de
su fila cruda. Las dos son honestas y describen dos platos distintos.

NO LO EJECUTA LA BATERIA: necesita red y se baja los volcados de CIQUAL y USDA,
igual que `contrastar_fuentes.py` y `buscar_humedad.py`. Lo que si ejecuta es el
BLOQUE 127, que rehace la parte DETERMINISTA -- la coherencia interna de cada
ficha -- contra la instantanea congelada.

    python3 auditar_cocinados.py
    python3 auditar_cocinados.py "Quinoa cocida"
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
CATALOGO = os.path.join(RAIZ, "alimentos_v3_final.json")
DECLARACION = os.path.join(RAIZ, "fuentes_de_composicion.json")

# La fila CRUDA de la misma base con la que se compara cada fila cocida.
# ⚠️ EL NOMBRE NO ES DECORACION: es lo unico que delata que la fila de
#    referencia es otro alimento, que es el fallo que tuvo este script.
FILA_CRUDA = {
    ("ciqual", "9104"): ("9100", "Riz blanc, cru"),
    ("usda",   "169757"): ("169756", "Rice, white, long-grain, regular, raw, unenriched"),
    ("bedca",  "1009"): ("904", "Arroz integral, crudo"),
    ("ciqual", "9103"): ("9102", "Riz complet, cru"),
    ("usda",   "169704"): ("169703", "Rice, brown, long-grain, raw (Includes foods for USDA's Food Distribution Program)"),
    ("bedca",  "2404"): ("2403", "Patata, cruda"),
    ("ciqual", "4003"): ("4008", "Pomme de terre, sans peau, crue"),
    ("usda",   "170440"): ("170026", "Potatoes, flesh and skin, raw"),
    ("ciqual", "9313"): ("9311", "Flocon d'avoine"),
    ("usda",   "173905"): ("173904", "Cereals, oats, regular and quick, not fortified, dry"),
    ("ciqual", "9341"): ("9340", "Quinoa, cru"),
    ("usda",   "168917"): ("168874", "Quinoa, uncooked"),
}
AGUA = {"bedca": "agua (humedad)", "ciqual": "Eau (g/100 g)", "usda": "Water"}

# Por debajo de esto la cifra es ruido y su cociente en seco no significa nada:
# el sodio de un cereal va de 4 a 6 mg y la materia seca cae un factor tres al
# cocer, asi que «sube el 262 %» sale siempre y no dice nada.
SUELO_QUE_NO_DICE_NADA = {"sodio": 15.0, "yodo": 5.0, "vitA": 5.0, "vitD": 1.0,
                          "epa": 0.05, "dha": 0.05, "araquidonico": 10.0}


def num(x):
    """El `< X` de CIQUAL y el `-` NO son cifras. El `TR` de BEDCA tampoco."""
    if isinstance(x, tuple):
        x = x[0]
    if x is None:
        return None
    s = str(x).strip().replace(",", ".")
    if not s or s in ("-", "·", "traces") or s.startswith("<"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def main():
    import contrastar_fuentes as cf
    decl = json.load(open(DECLARACION, encoding="utf-8"))
    porn = decl["unidades"]["por_nutriente"]
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))
    quiere = sys.argv[1] if len(sys.argv) > 1 else None

    cache = {}

    def fila(f, i):
        if (f, i) not in cache:
            if f == "bedca":
                n, v = cf.bedca_ficha(i)
                cache[(f, i)] = (n, {k: w[0] for k, w in v.items()})
            elif f == "ciqual":
                cache[(f, i)] = cf.ciqual_ficha(i)
            else:
                cache[(f, i)] = cf.usda_ficha(i)
        return cache[(f, i)]

    cocinadas = [a for a in catalogo
                 if str(a.get("preparacion") or "").strip().lower() not in ("", "crudo")
                 and (a.get("fuentes_id") or {})]
    if quiere:
        cocinadas = [a for a in cocinadas if a["nombre"] == quiere]
    if not cocinadas:
        print("No hay ninguna ficha cocinada con fuentes que mirar.")
        return 1

    problemas = 0
    for ficha in cocinadas:
        nombre = ficha["nombre"]
        ids = ficha["fuentes_id"]
        print(f"\n{'='*92}\n### {nombre}   [{ficha['categoria']}]  {ficha['energia']} kcal · "
              f"agua {ficha.get('humedad_g_100g', '?')}")

        # ── 1 · las tres fuentes en materia seca ──────────────────────────
        ms, filas = {}, {}
        for f, i in sorted(ids.items()):
            try:
                n, v = fila(f, i)
            except Exception as e:
                print(f"    {f}:{i} no se puede leer ({str(e)[:50]})")
                continue
            filas[f] = (i, n, v)
            a = num(v.get(AGUA[f]))
            ms[f] = None if a is None else 100.0 - a
            print(f"    {f}:{i:8s} MS={ms[f]}  «{str(n)[:56]}»")

        for clave, meta in porn.items():
            secos = {}
            for f, (i, n, v) in filas.items():
                col = ((meta.get("por_fuente") or {}).get(f) or {}).get("columna")
                if not col or not ms.get(f):
                    continue
                x = num(v.get(col))
                if x is None:
                    continue
                fac = ((meta.get("por_fuente") or {}).get(f) or {}).get("factor", 1.0)
                secos[f] = x * fac / ms[f] * 100.0
            vivos = [x for x in secos.values() if x > 0]
            if len(vivos) < 2:
                continue
            r = max(vivos) / min(vivos)
            if r > 2.5:
                print(f"    [fuentes] {clave:18s} " +
                      " · ".join(f"{f}={secos[f]:.4g}" for f in secos) +
                      f"  por 100 g MS -> {r:.0f}x")

        # ── 2 · cada fila cocida contra la cruda de SU base ───────────────
        proc = ficha.get("composicion_fuente") or {}
        # ⚠️ UNA FICHA QUE SE PESA EN CRUDO NO TIENE NADA QUE COMPARAR AQUI, y
        #    confundirlo seria acusarla de algo que hace bien. El Boniato, la
        #    Berenjena y el Esparrago verde hay que DARLOS cocidos y su
        #    composicion sale, a proposito y declarado, de la fila CRUDA de la
        #    fuente -- por eso su `se_pesa` dice «en crudo». Su fila de origen ya
        #    ES la cruda: compararla consigo misma no dice nada.
        if "crudo" in str(ficha.get("se_pesa") or "").lower():
            print(f"    [cruda] se pesa EN CRUDO con composición de la fila cruda: no hay "
                  f"conversión cocida que comprobar (lo vigila el BLOQUE 123)")
            continue
        for f, (i, n, v) in filas.items():
            ref = FILA_CRUDA.get((f, i))
            if not ref:
                print(f"    [cruda] {f}:{i} sin fila cruda de referencia declarada — no se compara")
                continue
            idr, nombre_esperado = ref
            try:
                n1, v1 = fila(f, idr)
            except Exception:
                continue
            # ⚠️ LA COMPROBACION QUE ESTE SCRIPT NO TENIA Y LE COSTO SEIS
            #    FALSOS POSITIVOS: que la fila de referencia sea la que se cree.
            if str(n1).strip().lower() != nombre_esperado.strip().lower():
                print(f"    [cruda] ⚠️ {f}:{idr} dice llamarse «{n1}» y aquí está declarada como "
                      f"«{nombre_esperado}». NO se compara: una referencia equivocada acusa a "
                      f"datos buenos.")
                problemas += 1
                continue
            a1, a2 = num(v1.get(AGUA[f])), num(v.get(AGUA[f]))
            if a1 is None or a2 is None:
                continue
            for clave, meta in porn.items():
                if not proc.get(clave, "").startswith(f"{f}:{i}"):
                    continue          # solo las celdas que de verdad TOMAMOS de aquí
                col = ((meta.get("por_fuente") or {}).get(f) or {}).get("columna")
                if not col:
                    continue
                x1, x2 = num(v1.get(col)), num(v.get(col))
                if x1 is None or x2 is None or not x1:
                    continue
                if x2 < SUELO_QUE_NO_DICE_NADA.get(clave, 0.0):
                    continue
                s1, s2 = x1 / (100 - a1) * 100, x2 / (100 - a2) * 100
                r = s2 / s1
                if r > 2.0:
                    print(f"    [cruda] {clave:18s} {f}:{i}  {s1:.4g} -> {s2:.4g} /100 g MS = "
                          f"{r*100:.0f} %  <== SUBE AL COCER, y eso no se puede")
                    problemas += 1
                elif r < 0.25:
                    print(f"    [cruda] {clave:18s} {f}:{i}  {s1:.4g} -> {s2:.4g} /100 g MS = "
                          f"{r*100:.0f} %  <== pierde el {100-r*100:.0f} %")
                    problemas += 1
    print(f"\n{len(cocinadas)} fichas cocinadas miradas · {problemas} cosas que mirar a mano")
    return 0


if __name__ == "__main__":
    sys.exit(main())
