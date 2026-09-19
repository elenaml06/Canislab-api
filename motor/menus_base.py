# -*- coding: utf-8 -*-
"""Los menús de ARRANQUE por patología. Los datos están en
`menus_base_patologias.json`; esto solo los carga y elige cuál sirve.

⚠️ QUÉ ES ESTO Y QUÉ NO ES, porque se parece al catálogo y no es lo mismo.

`catalogo_menus.json` guarda GRAMOS, y por eso su vía rápida los **reescala**
por las kcal del perro y los entrega sin resolver nada. Eso no puede llevar
patologías ni premios: el día entero de nutrientes en menos kilocalorías no sale
de multiplicar por un factor, lo decide el MILP.

Aquí se guarda una **LISTA DE ALIMENTOS, sin gramos**. Con ella se RESTRINGE el
catálogo que ve el solver, y **el solver vuelve a decidir todos los gramos** para
ese perro, con SUS kcal, SUS premios, SU peso y SUS topes. Lo único que se ahorra
es la parte cara, que es elegir QUÉ alimentos entre 105 accesibles.

⚠️ RESTRINGIR NO ES FORZAR, Y ESA DISTINCIÓN COSTÓ UNA VUELTA ENTERA. La vía del
catálogo fijo (5 de agosto) usa `forzar`: todos esos alimentos tienen que salir
con gramos > 0. Aquí eso no vale, porque la lista es de OTRO perro y obligar a
que sus diez alimentos entren en la ración de éste es durísimo. Medido, con
`forzar` el arranque de la renal cocinada no llegaba a verde en NINGÚN peldaño y
solo costaba tiempo (22,9 s por la búsqueda libre contra 29,5 s pasando antes por
el atajo); RESTRINGIENDO sale en 0,1 s.

LA MEDIDA, por la API y con la tabla puesta y quitada (19 de septiembre de 2026):

    adulto renal COCINADO ..... 23,8 s  ->  0,1 s   y en MEJOR peldaño
    adulto con artrosis .......  6,8 s  ->  0,1 s
    adulto con obesidad .......  4,5 s  ->  0,1 s
    toy 1,5 kg con artrosis ... 19,1 s  -> 13,7 s   el atajo NO entra
    Cairo con premios al 10 % . 15,1 s  -> 11,0 s   el atajo NO entra

⚠️ LAS DOS ÚLTIMAS FILAS MANDAN EN EL DISEÑO: hay perros para los que la lista de
otro perro no vale. El arranque es un ATAJO, no una respuesta. Si no llega a
verde se tira y se resuelve de cero, igual que hace la vía del catálogo desde el
5 de agosto -- y medido, eso no cuesta tiempo.

⚠️ Y NO LLEVA SELLO en `/verificar`, a propósito y por el mismo motivo que el
catálogo de menús: de aquí no sale ningún gramo. Si este fichero se corrompiera,
lo peor que puede pasar es que el solver arranque de una lista mala y no llegue
a verde -- y entonces se cae a la búsqueda libre. Lo que entrega el motor lo
sigue verificando `_garantizar_verificado()` de cero, como todo.
"""
import json
import os

_RUTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "menus_base_patologias.json")

if os.path.exists(_RUTA):
    with open(_RUTA, encoding="utf-8") as _f:
        _DATOS = json.load(_f)
else:                                   # sin fichero no hay atajo, y ya está
    _DATOS = {"menus": {}, "sin_menu": {}}

MENUS = _DATOS.get("menus") or {}
SIN_MENU = _DATOS.get("sin_menu") or {}
META = _DATOS.get("_meta") or {}

# Cómo se escribe «sin proteína forzada» en la clave. Tiene que ser la misma
# palabra que usa `generar_menus_base.py`: son las dos puntas de lo mismo.
LIBRE = "libre"


def arranques_de(patologias, modo):
    """Las listas de arranque para ese perro, en el orden en que probarlas.

    Devuelve [(proteina, [alimentos], peldano)]. El arranque `libre` va primero
    porque es el que sale en el peldaño más alto: forzar una proteína es en sí
    una restricción.

    ⚠️ RECORRE LAS PATOLOGÍAS EN ORDEN y junta lo que haya de cada una. Un perro
    con dos patologías no tiene arranque propio -- se generan de una en una --,
    y eso no es un problema: la lista es un PUNTO DE PARTIDA, y el menú que
    salga se comprueba contra TODAS sus patologías antes de entregarse.
    """
    m = (modo or "crudo").strip().lower()
    fuera = []
    for p in (patologias or []):
        for clave, ent in MENUS.items():
            pat, modo_ent, proteina = clave.split("|", 2)
            if pat != p or modo_ent != m:
                continue
            fuera.append((proteina, list(ent.get("alimentos") or []),
                          ent.get("peldano")))
    # El libre primero, y dentro de cada grupo el orden del fichero (alfabético
    # por clave), que es determinista: dos peticiones iguales prueban lo mismo.
    fuera.sort(key=lambda x: 0 if x[0] == LIBRE else 1)
    return fuera


# ─── Y EL ARRANQUE DEL PERRO SIN PATOLOGÍA, QUE YA EXISTÍA A MEDIAS ──────────
#
# ⚠️ CASO REAL, CONTADO POR ELENA (19 de septiembre de 2026). Cairo, su cachorro
# de casi 22 kg, no sacaba menú **con premios**: medido contra el motor
# desplegado, 90,8 · 104,4 · 143,0 s y «el cálculo está tardando más de lo
# normal», tres de tres.
#
# `main.py` tiene desde el 5 de agosto una vía que hace EXACTAMENTE lo que hace
# falta: coger los alimentos del menú del catálogo de ese tamaño y etapa y
# forzarlos como base, dejando que el solver decida los gramos. Esa vía **sí**
# sabe de premios -- le pasa `kcal_de_premios` desde el 11 de septiembre -- y
# estaba apagada en cuanto había uno, porque comparte el `elif` con la OTRA vía,
# la que reescala un menú enlatado por un factor. Y esa otra sí que no puede
# llevar premios: el día entero de nutrientes en menos kilocalorías no sale de
# multiplicar, lo decide el MILP.
#
# O sea que un gate escrito para la vía de al lado estaba apagando la única que
# podía resolver el caso de Cairo. Aquí se sirven esas listas para que la vía
# del arranque las use también cuando hay premios.
#
# ⚠️ SE DEVUELVEN LISTAS, NUNCA GRAMOS. De este módulo no sale un solo gramo:
# los del catálogo son de otro perro.
def arranques_del_catalogo(tamano, etapa, modo, al=None):
    """Las listas de arranque del catálogo fijo para ese tamaño y etapa.

    Primero la del menú base y después las de sus variantes, que traen cinco
    proteínas -- o sea que aquí también hay «varios menús y no uno solo».
    Devuelve [(proteina, [alimentos], peldano)], con `LIBRE` para la base.
    """
    if not tamano or not etapa:
        return []
    from catalogo_menus import CATALOGO, CATALOGO_VARIANTES, vale_en_este_modo
    clave = f"{tamano}_{etapa}"
    fuera = []
    ent = CATALOGO.get(clave)
    if ent and ent.get("gramos") and vale_en_este_modo(ent["gramos"], modo, al):
        fuera.append((LIBRE, sorted(ent["gramos"]), ent.get("peldano")))
    for var in (CATALOGO_VARIANTES.get(clave) or []):
        g = var.get("gramos")
        if g and vale_en_este_modo(g, modo, al):
            fuera.append((var.get("proteina") or LIBRE, sorted(g), var.get("peldano")))
    return fuera
