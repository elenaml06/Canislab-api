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
}
