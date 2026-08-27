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

# ── 2b. OMEGA-6 CONTRA OMEGA-3: los dos que se llaman casi igual ──────
#
# `linoleico` es omega-6 (C18:2) y `linolenico` es omega-3 (C18:3). Se
# diferencian en una letra y son cosas opuestas. Si alguien los cambia al
# cargar una tabla, NADA salta: los dos son nutrientes validos y los dos
# valores son plausibles, asi que el menu sale verde igual y el motor cree
# que equilibra el omega-3 con un aceite que no lo tiene.
#
# En la comida de verdad el omega-6 casi siempre gana, porque el omega-3
# de cadena corta esta concentrado en muy pocos alimentos. Que el omega-3
# supere al omega-6 no es un error -- pasa en el lino, en los aceites de
# salmon y en algun pescado magro -- pero es raro, y una lista corta se
# puede repasar a ojo. Si un dia esa lista se llena, es que se han
# invertido las columnas.
for a in al:
    n = a.get("nutrientes") or {}
    w6, w3 = n.get("linoleico") or 0, n.get("linolenico") or 0
    if w3 > w6 and (w6 or w3):
        avisos.append(("OMEGA", a["nombre"],
                       f"omega-3 ({w3} g) por encima del omega-6 ({w6} g). Es posible, pero "
                       f"revisa que no esten cambiados: linoleico=omega-6, linolenico=omega-3"))

# ── 2c. LOS GRASOS TIENEN QUE CABER DENTRO DE LA GRASA ────────────────
#
# El linoleico, el linolenico, el EPA y el DHA son PARTES de la grasa
# total, asi que sumados no pueden pasarse de ella. Es una ley fisica, no
# un criterio: si se pasan, el dato esta mal.
#
# Esto existe por la trampa de las unidades, que es la que mas se cuela:
# casi todas las tablas de composicion dan el EPA y el DHA en MILIGRAMOS y
# nosotros los guardamos en GRAMOS. Cargar la sardina con epa=254 en vez
# de 0.254 pondria 930 g de acidos grasos dentro de 7,5 g de grasa --
# imposible, y hasta ahora nada lo miraba. El menu habria salido verde: el
# EPA+DHA es un nutriente con minimo, y pasarse de largo no lo rompe.
#
# El araquidonico va en mg a proposito (asi lo da FEDIAF), por eso se
# divide entre 1000 antes de sumarlo.
#
# Margen del 5%: los valores vienen de fuentes distintas y de analisis
# distintos, asi que un pelo por encima no es un error de carga.
for a in al:
    n = a.get("nutrientes") or {}
    grasa = n.get("grasa") or 0
    if not grasa:
        continue
    suma = sum(n.get(k) or 0 for k in ("linoleico", "linolenico", "epa", "dha"))
    suma += (n.get("araquidonico") or 0) / 1000.0
    if suma > grasa * 1.05 and suma - grasa > 0.05:
        avisos.append(("GRASOS", a["nombre"],
                       f"los acidos grasos suman {suma:.2f} g y la grasa total es {grasa} g. "
                       f"No caben. Lo mas probable: EPA/DHA cargados en mg en vez de g"))

# ── 2d. DATO DUDOSO: el valor que SI esta y no nos lo creemos ─────────
#
# `sin_dato` marca los HUECOS, y los huecos son peligrosos por el lado del
# maximo. Pero un valor DECLARADO Y ERRONEO no dejaba rastro en ninguna
# parte, y es peor: tiene la forma de un dato bueno, asi que pasa cualquier
# validacion de formato.
#
# ⚠️ CASO REAL (27 agosto): tres a la vez, los tres de etiquetas reales.
# El omega-3 TOTAL de cuatro aceites de salmon guardado en `linolenico`
# (que es solo el ALA: el EPA y el DHA se contaban dos veces); el fosforo
# de las dos harinas de hueso, con un Ca:P de 1,28 cuando la hidroxiapatita
# da 2,15 por estequiometria; y el cobre del polvo de sangre, 150 veces por
# encima de lo que tiene la sangre desecada. Los tres pasaban las cuatro
# comprobaciones de arriba. Entraron por columnas cuyo nombre se parece al
# de la etiqueta lo bastante como para que nadie mire.
#
# Los que se pudieron arreglar, se arreglaron. Los que no —porque el valor
# es el de la etiqueta y el real no esta publicado— llevan `dato_dudoso`,
# y esto los lista para que nadie los olvide.
for a in al:
    for k, motivo in (a.get("dato_dudoso") or {}).items():
        valor = (a.get("nutrientes") or {}).get(k)
        avisos.append(("DUDOSO", a["nombre"],
                       f"{k}={valor} declarado pero no creible. {motivo[:150]}"))

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
# ⚠️ DOS ESPACIOS ENTRE EL NOMBRE Y EL DETALLE, Y EL NOMBRE SIN CORTAR.
# CASO REAL (26 agosto): esto era "%-34s %s" con nombre[:34], y el BLOQUE
# 19 lee cada línea con una expresión que separa el nombre del detalle por
# DOS espacios seguidos. Con un nombre de 34 caracteres justos, el relleno
# no añadía nada y solo quedaba el espacio del formato: el aviso de
# "Aceite de Salmón Natural Greatness" se leía mal, y el BLOQUE 19 decía
# que ese hueco había desaparecido cuando seguía ahí. Hay cinco alimentos
# con nombres de 34 o más -- y el corte a 34 además perdía el final de los
# de 38, así que dos alimentos distintos podían leerse como el mismo.
for tipo, nombre, det in avisos:
    print("  [%-6s] %-34s  %s" % (tipo, nombre, det))
sys.exit(1 if any(t == "BASE" for t, _, _ in avisos) else 0)
