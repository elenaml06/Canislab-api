# -*- coding: utf-8 -*-
"""Regenera `catalogo_menus.json`, los 36 menús de la vista previa y sus variantes.

⚠️ POR QUÉ ESTE ARCHIVO ESTÁ EN EL REPO Y NO EN UN SCRATCHPAD, que es donde
estaba: **porque vivir fuera del repo ya causó un fallo de verdad.**

El 8 de septiembre se regeneró el catálogo entero con una copia de este script
que no existía en ningún sitio versionado, y esa copia **llamaba a
`mc.resolver()` sin `margenes_categoria`**. `motor_completo.py` aplica las
proporciones BARF dentro de un `if margenes_categoria:`, así que sin ese
argumento **el motor formula sin proporciones**: nutricionalmente correcto y
prácticamente absurdo. El resultado, medido:

    Toy_Adulto ............  131 g  ->    655 g   (5 % de verdura -> 89 %)
    Gigante_Lactante ...... 6.846 g -> 25.792 g   (25,8 kg de comida al día)
    Pequeño_CachorroCrecimiento .......  2.903 g, 92 % verdura, SIN HUESO

Los 216 salían **VERDES** —cumplen los 43 requisitos— y por eso ni el semáforo
ni `_garantizar_verificado` los rechazaban: lo que se había apagado no era la
nutrición, era la FORMA, y la forma no la mira el semáforo. Es exactamente la
regla 3 del CLAUDE.md leída al revés: la forma se puede relajar *cuando no hay
menú*, y aquí se relajó *sin que nadie lo pidiera y sin decirlo*.

No llegó a `main`. Se arregló el 9 de septiembre: el script se trae aquí, hace
la MISMA llamada que hace la API (`margenes_categoria=MARGENES_V2`,
`max_suplementos=2`, peldaño 0), y **el BLOQUE 25 comprueba desde hoy las
proporciones de cada menú del catálogo**, para que si vuelve a pasar lo diga la
batería y no un ojo.

Uso:

    python3 regenerar_catalogo.py            # los 36 + las 180 variantes
    python3 regenerar_catalogo.py --solo-base

Se conservan la clave, el peso, la etapa y el DER de cada entrada: eso no lo
decide el motor, sale de la curva de Klein y está verificado aparte. Lo que se
rehace son los GRAMOS, y cada uno se comprueba verde antes de guardarlo. Si
alguno no sale, se deja el viejo y se dice cuál.
"""
import io
import json
import os
import sys
import time

_AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_AQUI, "motor"))
sys.path.insert(0, _AQUI)

import motor_completo as mc                      # noqa: E402
import main                                      # noqa: E402
from constructor import cargar, MARGENES as MARGENES_V2   # noqa: E402
from requisitos import dosis_maxima_fabricante   # noqa: E402
from verificar import verificar                  # noqa: E402

RUTA = os.path.join(_AQUI, "catalogo_menus.json")

# Las especies de pescado van restringidas en su categoría, no en la carne.
CAT_DE = {"Salmón": "Pescados y mariscos", "Merluza": "Pescados y mariscos"}

# ⚠️ LA LLAMADA TIENE QUE SER LA MISMA QUE HACE LA API. Si aquí se formula con
# otros argumentos, el catálogo deja de representar lo que el motor entrega, y
# eso no lo caza ninguna prueba de nutrición porque el menú sale verde igual.
LLAMADA_COMO_LA_API = dict(margenes_categoria=MARGENES_V2, max_suplementos=2)


def resolver_uno(al, req, der, etapa, peso, especie=None, proteina=None, segundos=45):
    """Un menú verde para esa ficha, o el mejor que haya salido, o (None, None)."""
    kw = dict(LLAMADA_COMO_LA_API)
    if especie and proteina:
        kw["restringir_especie"] = {especie: proteina}
    t0 = time.time()
    mejor = None
    while time.time() - t0 < segundos:
        ok, g = mc.resolver(der, etapa, al, req, peso, dosis_maxima_fabricante, **kw)
        if not ok:
            continue
        if main._tope_patologia_roto(g, al, [], etapa):
            continue
        v = verificar(g, al, req, der, etapa)
        if v["semaforo"] == "verde":
            return g, v
        mejor = mejor or (g, v)
    return mejor if mejor else (None, None)


def main_regenerar(solo_base=False):
    al, req = cargar()
    d = json.load(io.open(RUTA, encoding="utf-8"))
    cambios, fallos = [], []

    for clave, e in d["CATALOGO"].items():
        g, v = resolver_uno(al, req, e["der"], e["etapa"], e["peso_kg"])
        if g is None or v["semaforo"] != "verde":
            fallos.append(clave)
            print("  %-28s NO SALE -- se deja el viejo" % clave, flush=True)
            continue
        e["gramos"] = g
        e["semaforo"] = v["semaforo"]
        e["correctos"] = v["correctos"]
        e["total"] = v["correctos"] + len(v["faltan"]) + len(v["se_pasa"])
        cambios.append(clave)
        print("  %-28s OK  %2d alimentos, %4.0f g, %d/%d"
              % (clave, len(g), sum(g.values()), e["correctos"], e["total"]), flush=True)

    if not solo_base:
        for clave, lista in d["CATALOGO_VARIANTES"].items():
            ent = d["CATALOGO"][clave]
            for var in lista:
                p = var["proteina"]
                cat = CAT_DE.get(p, "Carne muscular")
                g, v = resolver_uno(al, req, ent["der"], ent["etapa"], ent["peso_kg"], cat, p)
                if g is None or v["semaforo"] != "verde":
                    fallos.append("%s/%s" % (clave, p))
                    print("  %-28s variante %-10s NO -- se deja la vieja"
                          % (clave, p), flush=True)
                    continue
                var["gramos"] = g
                print("  %-28s variante %-10s OK (%2d alimentos, %4.0f g)"
                      % (clave, p, len(g), sum(g.values())), flush=True)

    json.dump(d, io.open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nCATALOGO regenerado: %d de %d" % (len(cambios), len(d["CATALOGO"])), flush=True)
    print("no regenerados (%d): %s" % (len(fallos), fallos), flush=True)
    return fallos


if __name__ == "__main__":
    main_regenerar(solo_base="--solo-base" in sys.argv)
