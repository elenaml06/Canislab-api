# -*- coding: utf-8 -*-
"""
Audita el catálogo de alimentos por dentro, sin fuentes externas.

Existe porque el 21 de agosto, revisando si los nutrientes se medían en la
base correcta, aparecieron seis alimentos con huecos de datos que nadie
había declarado -- incluido un pescado azul con el omega-3 a cero y una
víscera con el 90% de su composición sin dato. Ninguna prueba del motor
podía detectarlo: el motor cumplía perfectamente unos datos incompletos.

Las cuatro comprobaciones que hace, y por qué cada una:

1. COHERENCIA ENERGETICA. Contrasta la energía declarada de cada alimento
   contra sus macros por Atwater. Si los nutrientes vinieran en materia
   seca y las kcal en fresco (o al revés), el ratio se dispararía. Es la
   forma de comprobar que todo el catálogo está en la misma base, que es
   lo que hace válido el cálculo "por 1000 kcal".

2. HUECOS SIN DECLARAR. Un cero puede significar "no lo tiene" o "no lo
   sabemos", y la diferencia es asimétrica: en los mínimos, contar un
   hueco como cero es conservador; en los MAXIMOS deja pasar un exceso sin
   detectarlo. El campo sin_dato existe para distinguirlos, y esto avisa
   de los alimentos donde no se ha usado.

3. PLAUSIBILIDAD POR CATEGORIA. Un hígado sin vitamina A, un hueso sin
   calcio o una carne con calcio de hueso son errores que ningún test
   numérico pilla, porque cada valor por separado es válido.

4. CUELLOS DE BOTELLA. Cuántos alimentos quedan por categoría al excluir
   especies. Es lo que decide si un perro con alergias se queda sin menú.

    python3 auditar_catalogo.py
"""
import json, collections, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "motor"))
RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alimentos_v3_final.json")
al = json.load(open(RUTA, encoding="utf-8"))
def nut(a, k): return (a.get("nutrientes") or {}).get(k, 0) or 0
def es_grasa(a): return nut(a, "grasa") > 80          # aceites: sus ceros son reales
SUPLEMENTOS = ("Multivitamínico", "Vitamina B", "Hierro", "Calcio", "Yodo", "Fibra", "Omega-3")

avisos = []

# ── 1. coherencia energética ──────────────────────────────────────────
for a in al:
    e = a.get("energia", 0)
    if not e: continue
    calc = 4 * nut(a, "proteina") + 9 * nut(a, "grasa")
    if calc > e * 1.15:
        avisos.append(("BASE", a["nombre"],
                       f"los macros dan {calc:.0f} kcal pero declara {e} "
                       f"(ratio {calc/e:.2f}) — ¿nutrientes en seco y kcal en fresco?"))

# ── 2. huecos sin declarar ────────────────────────────────────────────
for a in al:
    n = a.get("nutrientes") or {}
    if not n or es_grasa(a) or a.get("categoria") in SUPLEMENTOS: continue
    sd = set(a.get("sin_dato") or [])
    sin_declarar = [k for k, v in n.items() if not v and k not in sd]
    if len(sin_declarar) >= 10:
        avisos.append(("HUECOS", a["nombre"],
                       f"{len(sin_declarar)} nutrientes a cero sin declarar en sin_dato: "
                       + ", ".join(sin_declarar[:8]) + ("…" if len(sin_declarar) > 8 else "")))

# ── 3. plausibilidad por categoría ────────────────────────────────────
for a in al:
    c, nombre = a.get("categoria"), a["nombre"]
    sd = set(a.get("sin_dato") or [])
    if c == "Hígado" and nut(a, "vitA") < 1000 and "vitA" not in sd:
        avisos.append(("RARO", nombre, f"hígado con vitA={nut(a,'vitA')} (rondan 5.000-20.000 µg)"))
    if c == "Hueso carnoso" and nut(a, "calcio") < 400:
        avisos.append(("RARO", nombre, f"en 'Hueso carnoso' con calcio={nut(a,'calcio'):.0f} mg — "
                                       f"los huesos de verdad traen 1.250-1.810. ¿Es hueso o cartílago?"))
    if c == "Carne muscular" and nut(a, "calcio") > 300:
        avisos.append(("RARO", nombre, f"carne muscular con calcio={nut(a,'calcio'):.0f} mg — ¿lleva hueso?"))
    if c == "Pescados y mariscos" and not nut(a, "epa") and not nut(a, "dha") and "epa" not in sd:
        avisos.append(("RARO", nombre, "pescado con EPA y DHA a cero sin declarar"))

# ── 4. cuellos de botella ─────────────────────────────────────────────
from motor_completo import especie_de
CLAVE = ("Carne muscular", "Hueso carnoso", "Vísceras", "Hígado")
print("CUELLOS DE BOTELLA — cuántos alimentos quedan al excluir especies")
print("(las categorías con mínimo obligatorio son las que dejan sin menú)")
for excl in ([], ["Pollo"], ["Pollo", "Ternera"], ["Pollo", "Ternera", "Cordero"],
             ["Pollo", "Ternera", "Cordero", "Cerdo", "Pavo"]):
    quedan = {c: len([a for a in al if a.get("categoria") == c
                      and especie_de(a["nombre"]) not in excl]) for c in CLAVE}
    critico = [c for c, n in quedan.items() if n <= 2]
    print("   %d alergias: %s%s" % (len(excl),
          "  ".join(f"{c.split()[0]}={n}" for c, n in quedan.items()),
          "   <<< al límite: " + ", ".join(critico) if critico else ""))

# ── 5. datos sin verificar contra su fuente original ──────────────────
# Lo mas importante de un dato de nutricion no es el numero: es de donde
# sale. Un valor recuperado de un espejo puede estar bien, pero nadie lo
# ha comprobado, y eso tiene que poder LISTARSE en cualquier momento en
# vez de vivir enterrado en una nota que nadie relee.
sin_verificar = [a for a in al if (a.get("procedencia") or {}).get("verificado_contra_original") is False]
if sin_verificar:
    print()
    print("DATOS SIN VERIFICAR CONTRA SU FUENTE ORIGINAL")
    for a in sin_verificar:
        p = a["procedencia"]
        print("   %-26s nivel=%-9s %s" % (a["nombre"][:26], p.get("nivel"), p.get("fuente_declarada","")))
        for x in p.get("deducidos", []):
            print("      DEDUCIDO, no leido: %s" % x)

print()
print("═" * 74)
print("AVISOS: %d" % len(avisos))
for tipo, nombre, det in avisos:
    print("  [%-6s] %-34s %s" % (tipo, nombre[:34], det))
sys.exit(1 if any(t == "BASE" for t, _, _ in avisos) else 0)
