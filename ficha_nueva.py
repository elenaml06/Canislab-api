# -*- coding: utf-8 -*-
"""Las tres fuentes de un alimento que TODAVIA NO esta en el catalogo.

`contrastar_fuentes.py` compara una ficha contra sus fuentes; esto es el paso
de antes: no hay ficha que comparar. Reusa SUS lectores y SU tabla de mapeo a
proposito -- una segunda forma de leer las mismas bases seria el mismo
nutriente calculado de dos formas, que es el fallo de la fibra otra vez.

  python3 ficha_nueva.py "Arroz blanco cocido" --bedca 2661 --ciqual 9104 --usda 169757
"""
import sys, json, argparse
sys.path.insert(0, "/home/user/Canislab-api")
from contrastar_fuentes import (MAPA_FUENTES, _sacar, bedca_ficha, ciqual_ficha,
                                usda_ficha)

# El orden de mandato vive en el repo, no aqui.
MANDATO = json.load(open("/home/user/Canislab-api/fuentes_de_composicion.json",
                         encoding="utf-8"))

p = argparse.ArgumentParser()
p.add_argument("nombre")
p.add_argument("--bedca"); p.add_argument("--ciqual"); p.add_argument("--usda")
a = p.parse_args()

nb, vb = bedca_ficha(a.bedca) if a.bedca else ("(no consultada)", {})
nc, vc = ciqual_ficha(a.ciqual) if a.ciqual else ("(no consultada)", {})
nu, vu = usda_ficha(a.usda) if a.usda else ("(no consultada)", {})

print(f"### {a.nombre}")
print(f"  1 BEDCA  {a.bedca or '-':>8}  {nb}")
print(f"  3 CIQUAL {a.ciqual or '-':>8}  {nc}")
print(f"  4 USDA   {a.usda or '-':>8}  {nu}\n")
print(f"{'nutriente':20s}{'BEDCA':>12s}{'CIQUAL':>12s}{'USDA':>12s}   se queda")
print("-" * 80)

ficha, fuente_de, huecos = {}, {}, []
CLAVES = list(MAPA_FUENTES) + ["energia"]
for k in CLAVES:
    if k == "energia":
        nb_, nc_, nu_, fac = (["energia, total"],
                              ["Energie, Règlement UE N° 1169/2011 (kcal/100 g)"],
                              ["Energy"], 1)
    else:
        nb_, nc_, nu_, fac = MAPA_FUENTES[k]
    b, tipo = _sacar(vb, nb_, fac, con_tipo=True)
    c, _ = _sacar(vc, nc_, fac)
    u, _ = _sacar(vu, nu_, fac)
    if k == "energia" and b is not None:
        b = b / 4.184          # BEDCA publica en kJ
    # ⚠️ el `TR` de BEDCA con la celda vacia NO es un cero: es que no hay cifra
    if b is not None and tipo == "TR":
        b = None
    quien = None
    for cand, etiq in ((b, f"bedca:{a.bedca}"), (c, f"ciqual:{a.ciqual}"),
                       (u, f"usda:{a.usda}")):
        if cand is not None:
            ficha[k] = round(cand, 6); quien = etiq; break
    f = lambda v: "·" if v is None else f"{v:,.5g}"
    if quien is None:
        huecos.append(k)
    else:
        fuente_de[k] = quien
    print(f"{k:20s}{f(b):>12s}{f(c):>12s}{f(u):>12s}   {quien or 'HUECO'}")

print(f"\nhuecos ({len(huecos)}): {huecos}")
print("\n--- ficha en bruto ---")
print(json.dumps({"nutrientes": ficha, "composicion_fuente": fuente_de,
                  "sin_dato": huecos}, ensure_ascii=False, indent=1))
