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


# ⚠️ LOS MENÚS DE LA VISTA PREVIA SE HACEN CON LO BARATO Y LO ACCESIBLE
# (13 de septiembre de 2026). Elena: «usa ingredientes que sean fáciles de
# encontrar y baratos [...] lo que quiero es algo variado, barato y accesible».
#
# ⚠️ Y ESTO NO ES SOLO LA VISTA PREVIA, que es lo que hace que importe: los menús
# de `CATALOGO_VARIANTES` son la VÍA RÁPIDA de `/menu/v2` -- se reescalan a las
# kcal del perro y se entregan como menú de verdad. Así que lo que entre aquí es
# lo que come mucha gente, no una foto de catálogo.
#
# DOS EJES, y mezclarlos daría lo contrario de lo que se pide (ver el `_meta` de
# `donde_se_compra_cada_alimento.json`): un multivitamínico se pide por internet
# y no es caro; una gamba roja está en cualquier supermercado y sí lo es.
#
#   · `premium`: fuera. Son 20 y los que de verdad mueven el catálogo son cuatro
#     -- timo de vaca, solomillo de ternera, salmón y lomo con grasa.
#   · `no_se_vende`: fuera, y no es precio: el cerebro de vaca es material
#     especificado de riesgo (Reg. (CE) 999/2001 anexo V).
#   · `especializada`: fuera SOLO en las categorías de comida. Los suplementos se
#     piden por internet por definición y son la herramienta con la que el motor
#     cierra los 43 requisitos -- quitarlos sería romper la regla 5.
#
# LO QUE NO SE TOCA: ningún requisito. Esto elige qué alimentos VE el solver, no
# qué tiene que cumplir. Si con los accesibles no sale menú, el menú no sale y se
# ve aquí -- que es mejor que entregar uno de gamba roja.
CATEGORIAS_DE_COMIDA = ("Carne muscular", "Pescados y mariscos", "Hueso carnoso",
                        "Vísceras", "Hígado", "Verduras y frutas")


def solo_lo_accesible(al):
    """El catálogo sin lo premium ni lo que no se puede comprar (ni dar).

    Devuelve (alimentos, cuántos se han quitado). Si el fichero no está, no se
    filtra nada y se dice: un regenerado silencioso con el filtro caído daría un
    catálogo distinto sin que nadie lo notara.
    """
    import json as _j, os as _o
    ruta = _o.path.join(_o.path.dirname(_o.path.abspath(__file__)),
                        "donde_se_compra_cada_alimento.json")
    if not _o.path.exists(ruta):
        print("⚠️  no está `donde_se_compra_cada_alimento.json`: NO se filtra nada")
        return al, 0
    with open(ruta, encoding="utf-8") as f:
        d = _j.load(f)
    ficha = d["por_alimento"]
    fuera = []
    for n, a in list(al.items()):
        x = ficha.get(n)
        if not x:
            continue          # sin ficha no se decide nada; lo caza el BLOQUE 100
        if x["donde"] == "no_se_vende":
            fuera.append(n)
        elif a.get("categoria") in CATEGORIAS_DE_COMIDA and (
                x["precio_orientativo"] == "premium" or x["donde"] == "especializada"):
            fuera.append(n)
    return {n: a for n, a in al.items() if n not in fuera}, len(fuera)


def peso_adulto_de(d, tamano):
    """El peso ADULTO de ese tamaño, leído del propio catálogo.

    ⚠️ NO ES EL `peso_kg` DE LA ENTRADA, y confundirlos es justo el fallo que
    esto evita (9 septiembre): el `peso_kg` de un cachorro es lo que pesa HOY
    (a los 2 meses, o a mitad del crecimiento), y lo que decide el techo de
    calcio de SACN5 es lo que va a pesar de ADULTO. Un gran danés de 12 kg a
    los dos meses es un cachorro de raza gigante, no un perro mediano.

    Se lee de la entrada `<tamaño>_Adulto` del mismo fichero en vez de
    escribirse aquí a mano, para que no haya una segunda copia de los seis
    pesos que se pueda desincronizar de la primera.
    """
    ent = d["CATALOGO"].get("%s_Adulto" % tamano)
    return (ent or {}).get("peso_kg")


# ⚠️ CUÁNTO TIEMPO SE LE DA AL SOLVER POR MENÚ. 45 s era el valor fijo hasta el
# 13 de septiembre, y ese día se quedó corto de verdad: al quitar del catálogo un
# manganeso de 0,6 mg que NO TENÍA FUENTE EN NINGUNA PARTE (ver el sello de
# `main.py`), seis variantes de conejo dejaron de cubrir el mínimo de manganeso
# —la peor al 47 %— porque ese número falso era el que lo cubría. Con 45 s el
# solver no encontraba sustituto y el script «dejaba la vieja», que es justo el
# fallo de abajo. Se deja configurable para poder reintentar los que no salen sin
# rehacer los 216.
SEGUNDOS_POR_MENU = int(os.environ.get("CANISLAB_SEGUNDOS_POR_MENU") or 45)


def resolver_uno(al, req, der, etapa, peso, especie=None, proteina=None,
                 segundos=None, peso_adulto=None):
    """Un menú verde para esa ficha, o el mejor que haya salido, o (None, None)."""
    if segundos is None:
        segundos = SEGUNDOS_POR_MENU
    kw = dict(LLAMADA_COMO_LA_API)
    kw["peso_adulto_esperado_kg"] = peso_adulto
    if especie and proteina:
        kw["restringir_especie"] = {especie: proteina}
    # ⚠️ LA ESCALERA, Y ESTE SCRIPT NO LA USABA. Hasta el 13 de septiembre aquí
    # solo se probaba el PRIMER peldaño (`margenes_categoria=MARGENES_V2`), que es
    # la primera llamada de la API pero NO es lo que la API entrega: `/menu/v2`
    # envuelve esa llamada en `_escalera_de_relajacion()` y baja de peldaño
    # cuando no hay menú, diciéndolo.
    #
    # CASO REAL ENCONTRADO EL 13 DE SEPTIEMBRE. Nueve variantes de CONEJO no se
    # regeneraban y el script decía «NO SALE -- se deja el viejo», que se lee como
    # «necesita más tiempo». No lo era: con 45 s no salían, con 300 s tampoco, y
    # preguntándole al solver directamente son INFACTIBLES en el primer peldaño y
    # salen VERDES EN UN SEGUNDO sin las proporciones BARF. O sea que lo que
    # bloqueaba era la FORMA, que es justo lo que la regla 3 del CLAUDE.md
    # autoriza a soltar: «lo que se puede relajar es la FORMA, nunca la
    # nutrición». El catálogo precalculado estaba negando menús que la API sí
    # entrega.
    #
    # Se guarda EN QUÉ PELDAÑO salió cada uno, porque bajar sin decirlo es lo
    # único que la regla 3 prohíbe.
    escalones = main._escalera_de_relajacion()
    t0 = time.time()
    mejor = None
    for margenes_p, supl_p, clave_p in escalones:
        kw["margenes_categoria"] = margenes_p
        kw["max_suplementos"] = supl_p
        while time.time() - t0 < segundos:
            ok, g = mc.resolver(der, etapa, al, req, peso, dosis_maxima_fabricante, **kw)
            if not ok:
                break          # ese peldaño es infactible: se baja, no se insiste
        # ⚠️ CON EL PESO ADULTO TAMBIÉN AQUÍ (9 septiembre). Sin él, el filtro
        # mediría el calcio de un cachorro de raza gigante contra el techo del
        # cachorro pequeño (4250 en vez de 2750) y daría por bueno un menú que
        # la API va a rechazar en cuanto el usuario diga qué perro tiene.
            if main._tope_patologia_roto(g, al, [], etapa,
                                         peso_adulto_esperado_kg=peso_adulto):
                continue
            # ⚠️ CONTRA LAS KCAL REALES DEL MENÚ, NO CONTRA LAS PEDIDAS (12 de
            # septiembre, por la noche). Aquí ponía `der` y es el fallo que este
            # repo ya tiene escrito dos veces: el menú que devuelve el solver no
            # trae exactamente las kcal que se le piden -- medido, de +1,6 % a
            # +3,0 % --, y TODOS los mínimos son por 1000 kcal. Con un 3 % de
            # kcal de más, la concentración baja un 3 % y el nutriente que iba
            # al 99 % se cae por debajo del mínimo. Así se guardaron menús que
            # salían VERDES contra las kcal pedidas y ÁMBAR contra las suyas:
            # 41 de 216, casi todos por linoleico, manganeso, cloruro o yodo.
            # Es la regla 2 de CLAUDE.md -- los límites se miden sobre las kcal
            # reales -- y la misma que aplica `_garantizar_verificado`, que es
            # justo por lo que estos menús no llegaban al perro: la vía rápida
            # los verificaba otra vez y los tiraba. Peso muerto.
            #
            # ⚠️ Y VA DENTRO DE LA ESCALERA (13 de septiembre, al fusionar). Las
            # dos ramas tocaron estas líneas a la vez: una metió la escalera de
            # peldaños y la otra las kcal reales. Hacen falta LAS DOS, y ponerlo
            # fuera del bucle habría medido el último peldaño con las kcal del
            # primero.
            der_real = sum(al[n]["energia"] * gr / 100.0 for n, gr in g.items() if n in al)
            v = verificar(g, al, req, der_real or der, etapa)
            # ⚠️ EL NOMBRE DEL PRIMER PELDAÑO NO ES `None`. La escalera lo da como
            # None, y `main.py` lo traduce a `PELDANO_ESTRICTO` antes de
            # responder, justo por esto: «"no dice nada" y "estricto" se leen
            # igual», y quien firma necesita poder afirmar lo segundo. Se usa la
            # misma constante, no una cadena escrita aquí.
            nombre_p = clave_p or main.PELDANO_ESTRICTO
            if v["semaforo"] == "verde":
                return g, v, nombre_p
            mejor = mejor or (g, v, nombre_p)
    return mejor if mejor else (None, None, None)


def main_regenerar(solo_base=False, solo=None):
    al, req = cargar()
    # ⚠️ EL SOLVER SOLO VE LO ACCESIBLE. Ver `solo_lo_accesible`: esto elige qué
    # alimentos entran, no qué requisitos hay que cumplir. El filtro final y los
    # 43 requisitos son exactamente los mismos.
    al, _fuera = solo_lo_accesible(al)
    print(f"catálogo para la vista previa: {len(al)} alimentos ({_fuera} fuera "
          f"por premium, por tienda especializada o por no poderse dar)")
    d = json.load(io.open(RUTA, encoding="utf-8"))
    cambios, fallos = [], []

    def _toca(texto):
        return solo is None or solo.lower() in texto.lower()

    for clave, e in d["CATALOGO"].items():
        if not _toca(clave):
            continue
        g, v, peldano = resolver_uno(al, req, e["der"], e["etapa"], e["peso_kg"],
                                     peso_adulto=peso_adulto_de(d, e["tamano"]))
        if g is None or v["semaforo"] != "verde":
            fallos.append(clave)
            print("  %-28s NO SALE -- se deja el viejo" % clave, flush=True)
            continue
        e["gramos"] = g
        e["peldano"] = peldano
        e["semaforo"] = v["semaforo"]
        e["correctos"] = v["correctos"]
        e["total"] = v["correctos"] + len(v["faltan"]) + len(v["se_pasa"])
        cambios.append(clave)
        print("  %-28s OK  %2d alimentos, %4.0f g, %d/%d%s"
              % (clave, len(g), sum(g.values()), e["correctos"], e["total"],
                 "" if peldano == main.PELDANO_ESTRICTO else "  [peldano %s]" % peldano), flush=True)

    if not solo_base:
        for clave, lista in d["CATALOGO_VARIANTES"].items():
            ent = d["CATALOGO"][clave]
            for var in lista:
                p = var["proteina"]
                if not _toca("%s/%s" % (clave, p)):
                    continue
                cat = CAT_DE.get(p, "Carne muscular")
                g, v, peldano = resolver_uno(al, req, ent["der"], ent["etapa"],
                                             ent["peso_kg"], cat, p,
                                             peso_adulto=peso_adulto_de(d, ent["tamano"]))
                if g is None or v["semaforo"] != "verde":
                    fallos.append("%s/%s" % (clave, p))
                    print("  %-28s variante %-10s NO -- se deja la vieja"
                          % (clave, p), flush=True)
                    continue
                var["gramos"] = g
                var["peldano"] = peldano
                print("  %-28s variante %-10s OK (%2d alimentos, %4.0f g)%s"
                      % (clave, p, len(g), sum(g.values()),
                         "" if peldano == main.PELDANO_ESTRICTO else "  [peldano %s]" % peldano),
                      flush=True)

    json.dump(d, io.open(RUTA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\nCATALOGO regenerado: %d de %d" % (len(cambios), len(d["CATALOGO"])), flush=True)
    print("no regenerados (%d): %s" % (len(fallos), fallos), flush=True)

    # ⚠️ Y AHORA SE COMPRUEBA LO QUE QUEDA EN EL FICHERO, REGENERADO O NO.
    #
    # CASO REAL ENCONTRADO EL 13 DE SEPTIEMBRE. Este script decía «NO -- se deja
    # la vieja» y se quedaba tan ancho, y eso es un agujero: el menú viejo se
    # calculó con los valores VIEJOS del catálogo, así que si el catálogo ha
    # cambiado puede haber dejado de cumplir. Pasó con seis variantes de conejo
    # —46/48 y 47/48, todas por el manganeso— y el script las dejó dentro sin
    # decir que estaban rojas: imprimía «se deja la vieja», que suena a «no pasa
    # nada». Lo que no se comprueba no se sabe, y aquí lo que no se comprobaba era
    # justo lo que no se había tocado.
    #
    # No se borran solas: un menú rojo en el fichero es un fallo que hay que ver y
    # arreglar resolviéndolo con más tiempo, no tapándolo.
    rojos = []
    for clave, e in d["CATALOGO"].items():
        v = verificar(e["gramos"], al, req, e["der"], e["etapa"])
        if v["semaforo"] != "verde":
            rojos.append("%s (%d/%d)" % (clave, v["correctos"],
                                         v["correctos"] + len(v["faltan"]) + len(v["se_pasa"])))
        for var in d["CATALOGO_VARIANTES"].get(clave, []):
            v = verificar(var["gramos"], al, req, e["der"], e["etapa"])
            if v["semaforo"] != "verde":
                falta = ", ".join("%s al %d%%" % (f["nutriente"], f.get("cubre_pct", 0))
                                  for f in v["faltan"]) or "se pasa de algún máximo"
                rojos.append("%s/%s (%d/%d: %s)"
                             % (clave, var["proteina"], v["correctos"],
                                v["correctos"] + len(v["faltan"]) + len(v["se_pasa"]), falta))
    if rojos:
        print("\n⚠️ ATENCION: %d MENUS DEL FICHERO NO ESTAN VERDES contra el catalogo "
              "actual. Son los que no se han podido regenerar y se han quedado con su "
              "version vieja, calculada con datos que ya no son los de ahora. NO se "
              "entregan asi -- hay que reintentarlos con mas tiempo "
              "(CANISLAB_SEGUNDOS_POR_MENU):" % len(rojos), flush=True)
        for r in rojos:
            print("     - %s" % r, flush=True)
    else:
        print("\nLos %d menus del fichero estan VERDES contra el catalogo actual."
              % (len(d["CATALOGO"]) + sum(len(x) for x in d["CATALOGO_VARIANTES"].values())),
              flush=True)
    return fallos + rojos


if __name__ == "__main__":
    # `--solo <texto>` reintenta solo las fichas cuyo nombre contiene ese texto,
    # para no rehacer los 216 cuando lo que falta son seis. Va con
    # CANISLAB_SEGUNDOS_POR_MENU para darles mas tiempo.
    _solo = None
    for _i, _a in enumerate(sys.argv):
        if _a == "--solo" and _i + 1 < len(sys.argv):
            _solo = sys.argv[_i + 1]
    sys.exit(1 if main_regenerar(solo_base="--solo-base" in sys.argv, solo=_solo) else 0)
