# -*- coding: utf-8 -*-
"""Rehace `menus_base_patologias.json`: los menús de arranque por patología.

⚠️ POR QUÉ EXISTE. Lo pidió Elena el 19 de septiembre de 2026, después de ver
que un menú con patología podía tardar más de un minuto:

    «no te puedes tirar más de 20 o 30 segundos esperando a ver un menú en la
     pantalla»

y, sobre cómo tenían que ser:

    «que sean varios menús, o sea, no solo uno, porque entonces todos los perros
     con eso, con esa patología van a comer exactamente lo mismo. Entonces haz
     unos cuantos menús que se puedan adaptar luego los gramos [...] Por si uno
     elige, oye, lo quiero de conejo, oye, lo quiero de cordero»

y:

    «tienes que tener en cuenta que esto tiene que ser para los dos tipos de
     comida, para barf y para cocinada»

⚠️ LO QUE SE GUARDA ES UNA LISTA DE ALIMENTOS, NO UNOS GRAMOS, y esa es la
diferencia con `catalogo_menus.json`. Un menú enlatado se reescala por las kcal
del perro y por eso no puede llevar patologías ni premios -- el día entero de
nutrientes en menos calorías no sale de un factor, lo decide el MILP. Aquí no se
reescala nada: la lista entra como `forzar` y **el solver vuelve a decidir todos
los gramos** para ESE perro, con SUS kcal, SUS premios y SUS topes. Lo único que
se ahorra es la parte cara, que es elegir QUÉ alimentos entre 105.

LA MEDIDA QUE LO JUSTIFICA (19 de septiembre, con el catálogo de verdad y por
la escalera entera, exigiendo verde en los dos lados):

    toy 1,5 kg ................ 21,6 s  ->  0,02 s   (x885)
    Cairo con premios al max ...  6,0 s  ->  0,03 s   (x191)
    adulto con artrosis ....... 14,9 s  ->  0,09 s   (x158)
    adulto renal COCINADO ......  7,7 s  ->  0,29 s   (x27)
    adulto con obesidad ........  2,5 s  ->  0,13 s   (x20)
    toy 1,5 kg CON PREMIOS .... 22,7 s  ->  NO SALE

⚠️ LA ÚLTIMA FILA ES LA IMPORTANTE, y por eso la búsqueda libre se queda: hay
perros para los que la lista de otro perro no vale. El arranque es un ATAJO, no
una respuesta -- si no llega a verde, se tira y se resuelve de cero, que es
exactamente lo que ya hace la vía del catálogo desde el 5 de agosto.

Uso:

    python3 generar_menus_base.py                  # las 39 x 2 modos x 8 arranques
    python3 generar_menus_base.py --seguir         # solo lo que falta
    python3 generar_menus_base.py --solo artrosis  # una patología
    CANISLAB_PROCESOS=3 python3 generar_menus_base.py --seguir
    CANISLAB_SEGUNDOS_POR_BASE=90 python3 generar_menus_base.py

⚠️ SE GUARDA EN CADA CELDA, no al terminar: son 624 y la primera versión perdió
entero lo que llevaba cuando hubo que parar el proceso. Con `--seguir` se
retoma justo donde se dejó.
"""
import json
import os
import sys
import time

_AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_AQUI, "motor"))
sys.path.insert(0, _AQUI)

import motor_completo as mc                      # noqa: E402
import main                                      # noqa: E402
from constructor import MARGENES as MARGENES_V2  # noqa: E402
from requisitos import dosis_maxima_fabricante   # noqa: E402
from verificar import verificar                  # noqa: E402

RUTA = os.path.join(_AQUI, "menus_base_patologias.json")

# ⚠️ LAS MISMAS CINCO QUE YA OFRECE `CATALOGO_VARIANTES`, MÁS DOS. Las cinco de
# agosto son Pollo, Ternera, Conejo, Salmón y Merluza; Elena nombró el cordero
# («oye, lo quiero de cordero») y el pavo entra con él porque es la otra ave
# barata del catálogo. No se inventan: las siete existen como especie.
# ⚠️ Y LA PRIMERA ES `None`, QUE NO ES UNA PROTEÍNA: es el arranque SIN forzar
# ninguna, y es el que se usa cuando el dueño no ha pedido una en concreto --
# o sea, casi siempre. Importa porque forzar la proteína es en sí una
# restricción: medido con la artrosis, el arranque libre sale en un peldaño más
# alto que cualquiera de los siete forzados. Se guarda con la clave `libre`.
PROTEINAS = (None, "Pollo", "Ternera", "Conejo", "Cordero", "Pavo", "Salmón", "Merluza")

# Cómo se escribe `None` en la clave del JSON.
LIBRE = "libre"

# El pescado se restringe en SU categoría, no en la carne. Igual que en
# `regenerar_catalogo.py`, y por el mismo motivo.
CAT_DE = {"Salmón": "Pescados y mariscos", "Merluza": "Pescados y mariscos"}

MODOS = ("crudo", "cocinado")

# ⚠️ EL PERRO DE REFERENCIA ES EL DEL BLOQUE 61, y no es un capricho: 20 kg y
# DER 950 es el perro medio del catálogo y el que ya usan los bloques 8, 50 y
# 61 para decir si una patología formula. Si una lista no sale para ESE perro,
# no hay arranque que guardar.
PESO_REF, DER_REF, ETAPA_REF = 20.0, 950.0, "Adulto"

SEGUNDOS_POR_BASE = int(os.environ.get("CANISLAB_SEGUNDOS_POR_BASE") or 60)


def _resolver_por_la_escalera(al, req, patologia, modo, proteina, segundos):
    """La lista de alimentos de un menú VERDE, y en qué peldaño salió.

    ⚠️ POR LA ESCALERA Y EXIGIENDO VERDE, que son las dos cosas que este repo
    ya tiene escritas y que la primera versión de la medida se saltó: el solver
    puede devolver factible un menú que el semáforo deja en ámbar (los mínimos
    se miden contra las kcal REALES, que no son las pedidas), y quedarse con él
    sería guardar como arranque una lista que el filtro final va a tirar.
    """
    # ⚠️ «NO SALE» Y «NO ME HA DADO TIEMPO» NO SON LO MISMO, Y BAJO CARGA LO
    # SEGUNDO SE DISFRAZA DE LO PRIMERO. Pasó generando estas 624: con dos
    # procesos a la vez, `artrosis|crudo|Salmón` y `artrosis|crudo|Merluza`
    # salieron «sin menú» a los 60 s, y solas salen en 9,8 y 7,1 s. O sea que la
    # máquina cargada estaba BORRANDO arranques buenos del fichero, en silencio
    # y con forma de dato honesto -- que es la peor clase de error de datos que
    # hay en este repo.
    #
    # Así que se devuelve también si se acabó el reloj, y el que llama lo
    # escribe. Un «sin menú» que dice «infactible DEMOSTRADO en 1 s» se puede
    # creer; uno que dice «se acabó el reloj» hay que repetirlo.
    se_acabo_el_reloj = False
    kw = dict(patologias=[patologia], modo_de_preparacion=modo)
    if proteina:
        kw["restringir_especie"] = {CAT_DE.get(proteina, "Carne muscular"): proteina}
    t0 = time.time()
    for margenes, supl, clave in main._escalera_de_relajacion(
            patologias=[patologia], etapa=ETAPA_REF):
        if time.time() - t0 >= segundos:
            se_acabo_el_reloj = True
            break
        while time.time() - t0 < segundos:
            ok, g = mc.resolver(DER_REF, ETAPA_REF, al, req, PESO_REF,
                                dosis_maxima_fabricante,
                                margenes_categoria=margenes, max_suplementos=supl,
                                time_limit=min(20, segundos), **kw)
            if not ok or not g:
                break                      # ese peldaño es infactible: se baja
            if verificar(g, al, req, DER_REF, ETAPA_REF)["semaforo"] != "verde":
                continue                   # el solver reintenta con otra semilla
            # ⚠️ Y QUE NO ROMPA SU PROPIO TOPE, medido sobre las kcal REALES.
            # El semáforo no lo ve: son los requisitos de un perro SANO (regla 2).
            if main._tope_patologia_roto(g, al, [patologia], ETAPA_REF):
                continue
            return sorted(g), clave, time.time() - t0, False
    return None, None, time.time() - t0, se_acabo_el_reloj


def _una_celda(args):
    """Una celda, para poder repartirlas entre procesos.

    ⚠️ CARGA EL CATÁLOGO DENTRO. Pasarlo por el `Pool` obligaría a serializar
    163 fichas por celda, y son 624 celdas.
    """
    patologia, modo, proteina, segundos = args
    import main as _m                      # ya importado; aquí es barato
    al, req = _m.cargar_v2()
    lista, peldano, t, sin_reloj = _resolver_por_la_escalera(
        al, req, patologia, modo, proteina, segundos)
    return patologia, modo, proteina, lista, peldano, t, sin_reloj


def _guardar(menus, sin_menu):
    """⚠️ SE GUARDA EN CADA CELDA, NO AL FINAL. La primera versión de esto
    escribía el JSON una sola vez, al terminar: siete horas de trabajo que se
    perdían enteras si algo cortaba el proceso. Y algo lo cortó."""
    salida = {
        "_meta": {
            "que_es": ("Menús de ARRANQUE por patología: la LISTA de alimentos de un "
                       "menú verde, sin gramos. Entra como `forzar` en el solver, que "
                       "vuelve a decidir todos los gramos para el perro de verdad."),
            "no_es": ("No es un menú que se sirva. No se reescala nada, y no se entrega "
                      "sin pasar por `_garantizar_verificado`, como cualquier otro."),
            "perro_de_referencia": {"peso_kg": PESO_REF, "der": DER_REF, "etapa": ETAPA_REF},
            "proteinas": [p or LIBRE for p in PROTEINAS],
            "modos": list(MODOS),
            "se_rehace_con": "python3 generar_menus_base.py",
        },
        "menus": dict(sorted(menus.items())),
        "sin_menu": dict(sorted(sin_menu.items())),
    }
    tmp = RUTA + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(salida, f, ensure_ascii=False, indent=1)
        f.write("\n")
    os.replace(tmp, RUTA)          # o entero o el de antes, nunca a medias


def main_():
    solo = None
    if "--solo" in sys.argv:
        solo = sys.argv[sys.argv.index("--solo") + 1]
    # ⚠️ `--seguir` NO REHACE lo que ya está. Con 624 celdas y minutos por
    # celda, volver a calcular lo que ya salió es tirar horas.
    seguir = "--seguir" in sys.argv
    procesos = int(os.environ.get("CANISLAB_PROCESOS") or 1)

    tabla = json.loads(open(os.path.join(_AQUI, "patologias.json"),
                            encoding="utf-8").read())["patologias"]
    formulables = sorted(k for k, v in tabla.items() if v.get("formulable"))
    if solo:
        formulables = [k for k in formulables if k == solo]

    viejo = {}
    if os.path.exists(RUTA):
        viejo = json.load(open(RUTA, encoding="utf-8"))
    menus = dict(viejo.get("menus") or {})
    sin_menu = dict(viejo.get("sin_menu") or {})

    pendientes = []
    for patologia in formulables:
        for modo in MODOS:
            for proteina in PROTEINAS:
                clave = f"{patologia}|{modo}|{proteina or LIBRE}"
                if seguir and (clave in menus or clave in sin_menu):
                    continue
                pendientes.append((patologia, modo, proteina, SEGUNDOS_POR_BASE))

    print(f"{len(pendientes)} celdas por hacer, {procesos} proceso(s), "
          f"{SEGUNDOS_POR_BASE}s por celda", flush=True)
    t_total = time.time()
    hechas = 0

    def _anotar(res):
        nonlocal hechas
        patologia, modo, proteina, lista, peldano, t, sin_reloj = res
        clave = f"{patologia}|{modo}|{proteina or LIBRE}"
        if lista is None:
            # ⚠️ NO ES UN FALLO, Y SE ESCRIBE. Una proteína forzada puede ser
            # infactible de verdad -- le pasa ya a nueve variantes del catálogo.
            # Lo que no vale es que no se sepa.
            menus.pop(clave, None)
            porque = ("SE ACABÓ EL RELOJ, no está demostrado que no exista: "
                      "hay que repetirlo con más tiempo o sin la máquina cargada"
                      if sin_reloj else
                      "infactible DEMOSTRADO en los peldaños que se probaron")
            sin_menu[clave] = (f"no sale menú verde para el perro de referencia "
                               f"({PESO_REF:.0f} kg, DER {DER_REF:.0f}, {ETAPA_REF}) "
                               f"en {t:.0f} s por la escalera entera — {porque}")
            print(f"  {clave:52} --  sin menú ({t:.0f}s"
                  f"{', RELOJ' if sin_reloj else ''})", flush=True)
        else:
            sin_menu.pop(clave, None)
            menus[clave] = {"alimentos": lista, "peldano": peldano or main.PELDANO_ESTRICTO}
            print(f"  {clave:52} OK  {len(lista):2d} alim · {t:5.1f}s · "
                  f"{peldano or 'estricto'}", flush=True)
        hechas += 1
        _guardar(menus, sin_menu)

    if procesos > 1:
        import multiprocessing as mp
        with mp.Pool(procesos) as pool:
            for res in pool.imap_unordered(_una_celda, pendientes):
                _anotar(res)
    else:
        for args in pendientes:
            _anotar(_una_celda(args))

    print(f"\n{len(menus)} arranques · {len(sin_menu)} sin menú · "
          f"{hechas} hechas en {time.time() - t_total:.0f}s -> {RUTA}")


if __name__ == "__main__":
    main_()
