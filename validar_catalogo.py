# -*- coding: utf-8 -*-
"""
VALIDACIÓN FÍSICA DEL CATÁLOGO.

Encuentra los 6 errores de esta sesión: una pieza "con piel/hueso/grasa"
NUNCA puede tener menos grasa o menos kcal que su equivalente "sin". Y un
alimento con tejido animal no puede declarar 0 mg de un mineral que todo
tejido lleva.

Ejecutar tras cualquier cambio al catalogo:  python3 validar_catalogo.py
"""
import json, itertools, sys

al = json.load(open('alimentos_v3_final.json', encoding='utf-8'))
nombre = {a["nombre"]: a for a in al}
problemas = []

# 1. pares "con X" / "sin X": con debe tener >= grasa y >= kcal que sin
PARES = [("con piel", "sin piel"), ("con hueso", "sin hueso"),
         ("con grasa", "sin grasa")]
for con_txt, sin_txt in PARES:
    for n, a in nombre.items():
        low = n.lower()
        if con_txt not in low:
            continue
        base = low.replace(con_txt, sin_txt)
        par = next((n2 for n2 in nombre if n2.lower() == base), None)
        if not par:
            continue
        b = nombre[par]
        g1 = float(a["nutrientes"].get("grasa") or 0)
        g2 = float(b["nutrientes"].get("grasa") or 0)
        e1, e2 = a.get("energia", 0), b.get("energia", 0)
        if g1 < g2:
            problemas.append(f"'{n}' ({g1}g grasa) < '{par}' ({g2}g) — imposible")
        if e1 < e2:
            problemas.append(f"'{n}' ({e1} kcal) < '{par}' ({e2}) — imposible")

# 2. tejido animal con un mineral estructural en 0
CARNE_CATS = {"Carne muscular", "Hueso carnoso", "Vísceras", "Hígado",
             "Pescados y mariscos"}
SIEMPRE_PRESENTE = ["calcio", "fosforo", "potasio", "sodio"]
for a in al:
    if a.get("categoria") not in CARNE_CATS or a.get("dato_no_fiable"):
        continue
    for k in SIEMPRE_PRESENTE:
        if k in a.get("sin_dato", []):
            continue
        v = a["nutrientes"].get(k)
        if v is not None and float(v) == 0:
            problemas.append(f"'{a['nombre']}': {k}=0, imposible en tejido animal")

if problemas:
    print(f"❌ {len(problemas)} PROBLEMAS FÍSICOS ENCONTRADOS:")
    for p in problemas:
        print("   " + p)
    sys.exit(1)
else:
    print("✅ Sin incoherencias físicas: ningún 'con X' pesa menos que su 'sin X',")
    print("   y ningún tejido animal declara 0 en un mineral estructural.")
