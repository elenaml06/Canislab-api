# -*- coding: utf-8 -*-
"""
CUÁNTOS ALIMENTOS DISTINTOS CABEN POR CATEGORÍA.

⚠️ ESTE FICHERO ERA 182 LÍNEAS Y HOY SON LAS QUE SE USAN (14 de septiembre de
2026). De todo lo que había aquí, el motor usaba UNA COSA: el diccionario
`CUANTOS_MAX`, que lee `motor_completo.resolver()`. Lo demás
--`elegir_alimentos`, `cambiar`, `quitar`, `anadir`, `_disponibles`,
`CUANTOS_MIN`, `CUANTOS`, `MAX_PROTEINAS`, `CATEGORIAS_PROTEINA`-- no lo
llamaba nadie: los tres endpoints de edición tienen su propia implementación en
`main.py`.

POR QUÉ SE BORRA, QUE NO ES POR LIMPIEZA. Código muerto que parece vivo ya
costó un diagnóstico equivocado: durante días un pendiente culpó a
`elegir_alimentos` de que al toy de 1,5 kg le costara sacar menú --«el sorteo de
candidatos»-- y resultó que aquí no hay ningún sorteo, que `resolver()` ve todos
los alimentos accesibles y elige el MILP, y que la causa era el `time_limit`.
Una función que no se ejecuta no se puede depurar, pero sí se puede leer y
creer, que es peor.

El docstring que había describía «los tres modos son el mismo algoritmo» y el
recálculo al cambiar un ingrediente. Eso sigue siendo verdad del motor, pero no
lo hace este fichero: lo hacen `resolver()` y los endpoints de `main.py`.

QUÉ SON ESTOS NÚMEROS. El máximo de alimentos distintos que el MILP puede meter
de cada categoría: donde empieza a ser un menú inmanejable en una cocina de
verdad. La carne y el pescado son lo mismo nutricionalmente, así que los dos
juntos pueden llegar a cinco fichas distintas; el hígado va solo, porque dos
hígados distintos no aportan variedad y sí complican la compra.
"""

CUANTOS_MAX = {
    "Carne muscular": 3,
    "Hueso carnoso": 2,
    "Pescados y mariscos": 2,
    "Vísceras": 2,
    "Hígado": 1,
    "Verduras y frutas": 3,
    # Uno solo: dos cereales distintos en el mismo plato no aportan variedad
    # nutricional y sí complican la compra y la cocción, que es el mismo
    # argumento por el que el hígado va a 1.
    "Cereales y tubérculos": 1,
    # ⚠️ UN SOLO MULTIVITAMÍNICO (15 de septiembre de 2026). Elena, sobre el
    # menú de su perro en Personalizar: «me ha metido 3 suplementos... tiene
    # que intentar 1 o 2».
    #
    # Medido contra la API DESPLEGADA con su perfil exacto (American
    # Staffordshire de 7 meses, 20 kg, pollo + carcasa + hígado + zanahoria),
    # 20 peticiones seguidas con los cuatro niveles de premios: **20 de 20 dan
    # exactamente 2 suplementos, y los DOS son multivitamínicos** -- «astoral
    # MultiVital BARF» y «V-INTEGRA Cachorro».
    #
    # O sea que el tope de 2 se cumplía; lo que no había es nada que impidiera
    # que los dos fueran del mismo tipo. Dos multivitamínicos en el mismo
    # cuenco es redundante, y para quien lo lee parece un error aunque el menú
    # esté verde -- que es el mismo argumento de «la comida se tiene que poder
    # comprar» del 14 de septiembre.
    #
    # El motor sigue pudiendo meter DOS suplementos: lo que no puede es que los
    # dos sean multivitamínicos. Si hace falta un segundo, será de otra cosa
    # (omega-3, calcio, yodo), que es justo lo que aporta algo.
    #
    # ⚠️ MEDIDO ANTES DE PONERLO, y sobre once perros de 1,5 a 40 kg en las seis
    # etapas, con y sin Personalizar: **no cuesta ni un menú** -- los mismos 10
    # de 11 que salían siguen saliendo (el que falta es el toy de 1,5 kg, que
    # necesita la escalera y esta medida no la recorre). Los dos casos que
    # sacaban dos multivitamínicos pasan a uno, y de paso el perro de 3 kg baja
    # de dos aceites a uno.
    "Multivitamínico": 1,
    # ⚠️ Y UNO DE VITAMINA E (15 de septiembre de 2026). Dos botes distintos de
    # lo mismo en el mismo cuenco no es comida, igual que con el multivitamínico.
    # Se suelta en la escalera por el mismo sitio y por el mismo motivo: es
    # FORMA, y la forma no puede dejar a un perro sin comer.
    "Vitamina E": 1,
}


# ⚠️ Y LOS EXTRAS, POR GRUPO -- PORQUE «EXTRAS» SON 23 COSAS QUE NO SE PARECEN
#    EN NADA (15 de septiembre de 2026).
#
# `CUANTOS_MAX` es por CATEGORÍA del catálogo, y los 23 extras comparten una
# sola: aceites, grasas, huevos, semillas, sal, cartílago y yogur, todos
# «Extras». Toparlos juntos no sirve -- un menú con sal + un aceite + una
# semilla son tres extras y está bien; tres ACEITES son tres extras y no es
# comida.
#
# CASO REAL, reproducido contra la API desplegada con el perfil del perro de
# Elena (American Staffordshire de 7 meses, 20 kg, en Personalizar):
#
#     aceite de oliva virgen extra · aceite de girasol · aceite de sésamo
#     semilla de lino · semilla de sésamo · sal
#
# Tres aceites distintos y dos semillas en el mismo cuenco. El MILP optimiza
# nutrición por gramo y nadie le había dicho que eso no es una ración -- el
# mismo argumento de «la comida del menú se tiene que poder comprar» del 14 de
# septiembre, visto por el otro lado.
#
# ⚠️ EL AGRUPAMIENTO NO SE INVENTA AQUÍ: sale de `grupo_de_cada_extra` de
# `alimentos_como_se_presentan.json`, que es el MISMO con el que la app los
# pinta. Una segunda lista se desincronizaría, que es la lección de siempre.
CUANTOS_MAX_POR_GRUPO_DE_EXTRA = 1
