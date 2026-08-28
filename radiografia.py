# -*- coding: utf-8 -*-
"""
RADIOGRAFÍA — qué números ENTRAN al motor, para poder compararlos entre ramas.

Por qué existe (28 de agosto). La batería contesta «¿este menú cumple?».
No contesta «¿este menú se ha hecho con los números del perro que pediste?».
Y esa es justo la familia de fallos que se nos ha escapado dos veces:

  · una línea sacaba el peso de donde no debía  → el menú salía VERDE
  · el DER estaba duplicado y daba otro número  → el menú salía VERDE

Los dos pasaron una batería en verde, porque el semáforo comprueba el menú
CONTRA las kcal que le dieron: si las kcal ya venían mal, el menú cuadra
perfectamente con un perro que no es el tuyo. Un fallo así no se ve en el
resultado, solo se ve en la ENTRADA.

Esto imprime la entrada. Se corre en `main` y en la rama, y se comparan los
dos archivos con `diff`. Cada línea que cambie tiene que tener un motivo que
alguien pueda decir en voz alta. La que no lo tenga es un fallo.

    python3 radiografia.py > /tmp/rama.txt
    git stash && python3 radiografia.py > /tmp/main.txt && git stash pop
    diff /tmp/main.txt /tmp/rama.txt

No sustituye a la batería: la batería dice si está bien, esto dice si ha
cambiado. Hacen falta las dos.
"""
import sys, json
sys.path.insert(0, '.')
sys.path.insert(0, './motor')

from fastapi.testclient import TestClient
import main as app_main
# Los imports son tolerantes A PROPÓSITO: este archivo tiene que poder correr
# TAMBIÉN en `main`, que es contra lo que se compara. Si exigiera las funciones
# nuevas, solo se podría correr en la rama -- y una radiografía de un solo lado
# no compara nada.
try:
    from verificar import minimo_de, maximo_de
except ImportError:                       # `main`: aún no existen
    def minimo_de(fila, nombre, etapa, der_efectiva=None):
        return fila.get(f"min{etapa}")
    def maximo_de(fila, nombre, etapa):
        # El `or maxAdulto` NO es invento: es lo que `main` ya hacía en los
        # cinco sitios que leían un máximo. Sin él, la comparación inventaría
        # diferencias donde no las hay -- y una radiografía que miente sobre
        # lo que ha cambiado es peor que no tenerla.
        return fila.get(f"max{etapa}") or fila.get("maxAdulto")
from constructor import cargar

cli = TestClient(app_main.app)
al, req = cargar()

# Los nutrientes que se miran. No son todos a propósito: son los que se mueven
# por motivos distintos -- uno que escala, uno que no (grasa), uno con techo
# legal que puede cruzarse (selenio), el que aprieta primero (cloruro), y los
# dos que estrenamos hoy (metionina y lisina).
NUTRIENTES = ["Proteína_total", "Grasa_total", "Calcio", "Fósforo", "Selenio",
              "Cloruro", "Metionina", "Lisina", "Vitamina_D", "Relacion_Ca_P",
              "Calcio_LateGrowth_RazaGrande"]

# ── los perros ────────────────────────────────────────────────────────────
# Uno por cada forma en que el peso o las kcal pueden salir de un sitio
# distinto. Si un cambio mueve la casilla de "peso" o "der_efectiva" de
# alguno de estos, es exactamente el fallo que buscamos.
PERROS = [
    # (nombre, kcal, etapa, peso, peso_adulto, peso_objetivo, bcs, patologías)
    ("adulto normal 22 kg",            1630, "Adulto",               22,   None, None, None, []),
    ("adulto 22 kg con BCS 5",         1630, "Adulto",               22,   None, None, 5,    []),
    ("adulto pequeño 5 kg",             530, "Adulto",                5,   None, None, None, []),
    ("adulto gigante 60 kg",           3400, "Adulto",               60,   None, None, None, []),
    ("senior 28 kg",                   1720, "Senior",               28,   None, None, None, []),
    ("cachorro 12 kg (adulto 30)",     1900, "CachorroCrecimiento",  12,   30,   None, None, []),
    ("cachorro 12 kg (SIN peso adulto)",1900,"CachorroCrecimiento",  12,   None, None, None, []),
    ("cachorro joven 6 kg",            1000, "CachorroJoven",         6,   None, None, None, []),
    ("gestante tardía 15 kg",          1800, "GestanteTardia",       15,   None, None, None, []),
    ("lactante 28 kg",                 3600, "Lactante",             28,   None, None, None, []),
    # los tres peldaños del peso de referencia, el mismo perro por tres vías
    ("bajada · objetivo DECLARADO",     900, "Adulto",               30,   None, 25,   None, []),
    ("bajada · objetivo por BCS 7",     900, "Adulto",               30,   None, None, 7,    []),
    ("bajada · SIN objetivo ni BCS",    900, "Adulto",               30,   None, None, None, []),
    ("bajada · BCS 9 (fuera de AAHA)",  900, "Adulto",               30,   None, None, 9,    []),
    ("bajada · BCS 4 (por debajo de 5)",900, "Adulto",               30,   None, None, 4,    []),
    # patologías: los topes se miden sobre las kcal REALES, no las pedidas
    ("renal 22 kg",                    1630, "Adulto",               22,   None, None, None, ["Renal"]),
    ("hepatopatía 22 kg",              1630, "Adulto",               22,   None, None, None, ["Hepatopatia"]),
    ("pancreatitis 22 kg",             1630, "Adulto",               22,   None, None, None, ["Pancreatitis"]),
]


def linea(k, v):
    print(f"  {k:<22} {v}")


print("=" * 72)
print("EL PESO. De dónde sale y qué DER efectiva produce.")
print("=" * 72)
print("La casilla 'procedencia' es la que caza el fallo de 'lo sacaba de")
print("donde no debía': dice el peldaño, no solo el número.\n")

for (nombre, kcal, etapa, peso, peso_ad, peso_obj, bcs, pat) in PERROS:
    cuerpo = {
        "nombres_alimentos": [],
        "der_objetivo": kcal,
        "etapa_requisitos": etapa,
        "peso_perro_kg": peso,
        "peso_adulto_esperado_kg": peso_ad,
        "peso_objetivo_kg": peso_obj,
        "bcs": bcs,
        "patologias": pat,
        "modo": "automatico",
    }
    print(f"· {nombre}")
    try:
        r = cli.post("/menu/v2", json=cuerpo)
        d = r.json() if r.status_code == 200 else {}
    except Exception as e:
        print(f"  ERROR de llamada: {e}\n")
        continue

    pref = d.get("peso_de_referencia")
    if pref is None:
        linea("peso usado (kg)", "(la respuesta no lo dice)")
        linea("procedencia", "(la respuesta no lo dice)")
        linea("der_efectiva", "(la respuesta no lo dice)")
        pref = {}
    else:
        linea("peso usado (kg)", pref.get("kg"))
        linea("procedencia", pref.get("procedencia"))
        linea("der_efectiva", pref.get("der_efectiva"))

    # los mínimos que ESE peso produce, que es lo que de verdad entra al solver
    de = pref.get("der_efectiva")
    for nutr in NUTRIENTES:
        fila = req.get(nutr)
        if not fila:
            continue
        mn = minimo_de(fila, nutr, etapa, de)
        mx = maximo_de(fila, nutr, etapa)
        linea(f"mín {nutr}", f"{mn}" + (f"   (máx {mx})" if mx is not None else ""))
    print()

print("=" * 72)
print("Fin. Compara este archivo con el de `main`. Cada diferencia, un motivo.")
print("=" * 72)
