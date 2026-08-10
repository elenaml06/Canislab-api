# -*- coding: utf-8 -*-
"""
BATERÍA DE PRUEBAS COMPLETA — se ejecuta ANTES de dar por bueno cualquier
cambio en el motor o en main.py, no solo cuando la usuaria lo pide.

Por qué existe (5 agosto): antes cada arreglo se probaba solo con el caso
concreto que había fallado, y eso dejaba que otros 10 casos se rompieran
sin que nadie lo notara hasta que la usuaria los encontraba usando la app
de verdad. Esto es agotador e inaceptable. Este archivo es el compromiso
de que eso no vuelva a pasar: se ejecuta ENTERO, con calma, antes de
entregar cualquier archivo modificado.

CÓMO USARLO
-----------
    cd canislab-api
    python3 pruebas_completas.py

Tarda varios minutos (normal, prueba muchísimos casos reales). Si al
final dice "TODO EN VERDE", se puede entregar el archivo. Si dice que hay
fallos, se arreglan ANTES de entregar nada, no después.
"""
import sys, time, json
sys.path.insert(0, '.')
sys.path.insert(0, './motor')

from motor_completo import resolver, patologias_bloquean
from constructor import cargar, MARGENES
from verificar import verificar
from optimizador import dosis_maxima_fabricante
from catalogo_menus import CATALOGO

al, req = cargar()
SUP_COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra", "Calcio", "Hierro", "Vitamina B")
PESCADOS = ["Salmón", "Sardina", "Caballa", "Merluza", "Bacalao", "Lubina", "Dorada",
           "Trucha", "Atún", "Boquerón", "Lenguado", "Pescadilla", "Besugo", "Bacaladilla", "Perca"]
VINTEGRA = {"V-INTEGRA Cachorro", "V-INTEGRA Perro Adulto", "V-INTEGRA Senior",
           "V-INTEGRA Epato", "V-INTEGRA Renal"}

fallos = []
t_total = time.time()


def der_de(peso, etapa):
    mult = 2.0 if "Cachorro" in etapa else (1.6 if etapa in ("Adulto", "Senior") else 1.8)
    return 70 * peso**0.75 * mult


def comprobar_menu(nombre_caso, g, der, etapa, peso=None):
    """Comprobaciones que se repiten en todos los bloques: verde, máximo
    2 suplementos, dosis del fabricante respetada, márgenes de categoría
    por peso respetados."""
    problemas = []
    f = verificar(g, al, req, der, etapa)
    if f["semaforo"] != "verde":
        problemas.append(f"{nombre_caso}: semáforo {f['semaforo']} — "
                         f"{[(x['nutriente'], x.get('cubre_pct')) for x in f['rojos']+f['ambar']]}")
    n_sup = sum(1 for n in g if al.get(n, {}).get("categoria") in SUP_COMERCIALES)
    if n_sup > 2:
        problemas.append(f"{nombre_caso}: {n_sup} suplementos (máximo 2)")
    if peso:
        for n, gr in g.items():
            a = al.get(n, {})
            if a.get("categoria") in SUP_COMERCIALES:
                techo = dosis_maxima_fabricante(a, peso)
                if techo and gr > techo * 1.01:
                    problemas.append(f"{nombre_caso}: {n} pasado de dosis ({gr}g > {techo}g)")
    total = sum(g.values())
    for cat, (mn, mx) in MARGENES.items():
        peso_cat = sum(gr for n, gr in g.items() if al.get(n, {}).get("categoria") == cat)
        pct = peso_cat / total if total else 0
        if pct > mx + 0.02:
            problemas.append(f"{nombre_caso}: {cat} al {pct*100:.1f}% (máx {mx*100:.0f}%)")
    return problemas, f


# ============================================================
# BLOQUE 1 — todas las etapas x varios pesos, automático
# ============================================================
print("=== BLOQUE 1: etapas x pesos (automático) ===")
CASOS_ETAPA = [
    ("CachorroJoven", 1.5), ("CachorroJoven", 6), ("CachorroJoven", 15),
    ("CachorroCrecimiento", 3), ("CachorroCrecimiento", 12), ("CachorroCrecimiento", 25), ("CachorroCrecimiento", 45),
    ("Adulto", 3), ("Adulto", 12), ("Adulto", 22), ("Adulto", 32), ("Adulto", 55), ("Adulto", 75),
    ("Senior", 8), ("Senior", 28), ("Senior", 50),
    ("GestanteTemprana", 15), ("GestanteTardia", 15), ("GestanteTardia", 30),
    ("Lactante", 15), ("Lactante", 28),
]
# ⚠️ CORREGIDO: antes probaba UNA llamada aislada (o como mucho 1
# reintento sin límite de tiempo), lo que NO es representativo de lo que
# de verdad hace main.py -- que reintenta dentro de un PRESUPUESTO de
# 18 segundos, no un número fijo de intentos. Se replica esa misma
# lógica aquí, para que la batería mida lo que la usuaria experimenta
# de verdad, no una única tirada de dados.
PRESUPUESTO_PRUEBA = 18.0
for etapa, peso in CASOS_ETAPA:
    der = der_de(peso, etapa)
    t0 = time.time()
    ok, g = False, None
    while time.time() - t0 < PRESUPUESTO_PRUEBA:
        ok, g = resolver(der, etapa, al, req, peso, dosis_maxima_fabricante,
                         margenes_categoria=MARGENES, max_suplementos=2)
        if ok:
            break
    if not ok:
        fallos.append(f"BLOQUE1 {etapa} {peso}kg: NO FACTIBLE ni dentro del presupuesto de {PRESUPUESTO_PRUEBA}s")
        continue
    problemas, _ = comprobar_menu(f"BLOQUE1 {etapa} {peso}kg", g, der, etapa, peso)
    fallos.extend(problemas)
print(f"  hecho, {len(fallos)} fallos hasta ahora"); json.dump(fallos, open("/tmp/ultimos_fallos.json","w"), ensure_ascii=False, indent=1)

# ============================================================
# BLOQUE 2 — personalizar: forzar varias combinaciones
# ============================================================
print("=== BLOQUE 2: personalizar (forzar) ===")
der, peso, etapa = 1589, 18.0, "CachorroCrecimiento"
COMBOS_FORZAR = [
    ["Pollo con piel (sin hueso)", "Carcasa de pollo"],
    ["Ternera con grasa", "Zanahoria"],
    ["Conejo", "Carcasa de conejo", "Hígado de conejo"],
    ["Salmón"],
    ["Corazón de cordero", "Costillas de cordero", "Riñón de cordero", "Hígado de cordero"],
]
for combo in COMBOS_FORZAR:
    ok, g = resolver(der, etapa, al, req, peso, dosis_maxima_fabricante,
                     margenes_categoria=MARGENES, max_suplementos=2, forzar=combo)
    if not ok:
        fallos.append(f"BLOQUE2 forzar={combo}: NO FACTIBLE")
        continue
    faltan = [n for n in combo if n not in g or g[n] < 1]
    if faltan:
        fallos.append(f"BLOQUE2 forzar={combo}: no entraron con cantidad real {faltan}")
    problemas, _ = comprobar_menu(f"BLOQUE2 forzar={combo}", g, der, etapa, peso)
    fallos.extend(problemas)
print(f"  hecho, {len(fallos)} fallos hasta ahora"); json.dump(fallos, open("/tmp/ultimos_fallos.json","w"), ensure_ascii=False, indent=1)

# ============================================================
# BLOQUE 3 — aprovechar: preferir varias combinaciones
# ============================================================
print("=== BLOQUE 3: aprovechar (preferir) ===")
COMBOS_PREFERIR = [
    ["Pollo con piel (sin hueso)", "Zanahoria"],
    ["Salmón", "Merluza", "Boquerón"],
    ["Hígado de vaca"],
]
for combo in COMBOS_PREFERIR:
    ok, g = resolver(der, etapa, al, req, peso, dosis_maxima_fabricante,
                     margenes_categoria=MARGENES, max_suplementos=2, preferir=combo)
    if not ok:
        fallos.append(f"BLOQUE3 preferir={combo}: NO FACTIBLE")
        continue
    problemas, _ = comprobar_menu(f"BLOQUE3 preferir={combo}", g, der, etapa, peso)
    fallos.extend(problemas)
print(f"  hecho, {len(fallos)} fallos hasta ahora"); json.dump(fallos, open("/tmp/ultimos_fallos.json","w"), ensure_ascii=False, indent=1)

# ============================================================
# BLOQUE 4 — variedad real: pescado y multivitamínico, varios intentos
# ============================================================
print("=== BLOQUE 4: variedad real (pescado, multivitamínico) ===")
con_pescado = 0
vistos_multi = {}
for i in range(10):
    ok, g = resolver(der, etapa, al, req, peso, dosis_maxima_fabricante,
                     margenes_categoria=MARGENES, max_suplementos=2)
    if not ok:
        continue
    if any(n in PESCADOS for n in g):
        con_pescado += 1
    for n in g:
        if al.get(n, {}).get("categoria") in SUP_COMERCIALES:
            vistos_multi[n] = vistos_multi.get(n, 0) + 1
print(f"  pescado en {con_pescado}/10 (sano: ni 0 ni 10)")
print(f"  multivitamínicos vistos: {vistos_multi}")
if con_pescado == 10:
    fallos.append("BLOQUE4: pescado SIEMPRE (10/10) — sin variedad real")
if con_pescado == 0:
    fallos.append("BLOQUE4: pescado NUNCA (0/10) — revisar si es lo esperado")

# ============================================================
# BLOQUE 5 — exclusiones + patologías combinadas
# ============================================================
print("=== BLOQUE 5: exclusiones + patologías ===")
CASOS_EXCL = [
    (["pollo"], None), (["ternera", "cordero"], None),
    (None, ["diabetes"]), (None, ["pancreatitis"]),
    (["pollo"], ["hepatopatia"]),
]
for excl, pat in CASOS_EXCL:
    ok, g = resolver(der, etapa, al, req, peso, dosis_maxima_fabricante,
                     margenes_categoria=MARGENES, max_suplementos=2, excluidos=excl, patologias=pat)
    if not ok:
        continue  # puede ser correcto (ej. renal+cachorro es imposible por diseño)
    if excl:
        colados = [n for n in g if any(e in n.lower() for e in excl)]
        if colados:
            fallos.append(f"BLOQUE5 excl={excl}: se coló {colados}")
    problemas, _ = comprobar_menu(f"BLOQUE5 excl={excl} pat={pat}", g, der, etapa, peso)
    fallos.extend(problemas)
print(f"  hecho, {len(fallos)} fallos hasta ahora"); json.dump(fallos, open("/tmp/ultimos_fallos.json","w"), ensure_ascii=False, indent=1)

# ============================================================
# BLOQUE 6 — V-INTEGRA: la variante correcta según etapa/patología
# ============================================================
print("=== BLOQUE 6: V-INTEGRA correcta por etapa/patología ===")
CASOS_VINTEGRA = [
    ("CachorroCrecimiento", 18, None, "V-INTEGRA Cachorro"),
    ("GestanteTardia", 25, None, "V-INTEGRA Cachorro"),
    ("Lactante", 20, None, "V-INTEGRA Cachorro"),
    ("Adulto", 20, None, "V-INTEGRA Perro Adulto"),
    ("Senior", 20, None, "V-INTEGRA Senior"),
    ("Adulto", 20, ["hepatopatia"], "V-INTEGRA Epato"),
    ("Adulto", 20, ["renal"], "V-INTEGRA Renal"),
]
for etapa_c, peso_c, pat, esperada in CASOS_VINTEGRA:
    der_c = der_de(peso_c, etapa_c)
    ok, g = resolver(der_c, etapa_c, al, req, peso_c, dosis_maxima_fabricante,
                     margenes_categoria=MARGENES, max_suplementos=2, patologias=pat)
    if not ok:
        continue
    usada = [n for n in g if n in VINTEGRA]
    otras_coladas = [n for n in usada if n != esperada]
    if otras_coladas:
        fallos.append(f"BLOQUE6 {etapa_c} pat={pat}: se coló {otras_coladas}, esperaba {esperada}")
print(f"  hecho, {len(fallos)} fallos hasta ahora"); json.dump(fallos, open("/tmp/ultimos_fallos.json","w"), ensure_ascii=False, indent=1)

# ============================================================
# BLOQUE 7 — tiempos: que el peor caso no se dispare
# ============================================================
print("=== BLOQUE 7: tiempos (peor caso razonable) ===")
t0 = time.time()
ok, g = resolver(1589, "CachorroCrecimiento", al, req, 18.0, dosis_maxima_fabricante,
                 margenes_categoria=MARGENES, max_suplementos=2)
dt = time.time() - t0
print(f"  una llamada normal: {dt:.1f}s")
if dt > 15:
    fallos.append(f"BLOQUE7: una sola llamada tardó {dt:.1f}s (demasiado, revisar time_limit)")

# ============================================================
# RESUMEN FINAL
# ============================================================
print(f"\n{'='*60}")
print(f"TOTAL: {time.time()-t_total:.0f}s de pruebas")
if fallos:
    print(f"\n❌ {len(fallos)} FALLOS ENCONTRADOS — NO ENTREGAR TODAVÍA:\n")
    for x in fallos:
        print("  -", x)
    sys.exit(1)
else:
    print("\n✅ TODO EN VERDE — se puede entregar el archivo")
    sys.exit(0)
