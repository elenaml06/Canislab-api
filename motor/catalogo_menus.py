# -*- coding: utf-8 -*-
"""
CATÁLOGO DE MENÚS FIJOS — 36 combinaciones, 6 tamaños × 6 etapas, más 180
variantes. Los datos están en `catalogo_menus.json`; esto solo los carga.

Generado el 5 de agosto con motor_completo.py, verificado uno a uno contra
los 30 requisitos de FEDIAF. Los 36 salen en verde.

CÓMO SE ELIGIÓ EL PESO DE CADA CACHORRO
------------------------------------------
Un cachorro no tiene un peso fijo -- va cambiando. Se usó un punto
representativo de cada etapa, con la misma curva de Klein que ya está
verificada en der.py:
  - CachorroJoven: peso a los 2 meses
  - CachorroCrecimiento: peso a la mitad de su periodo de crecimiento
Gestante y lactante usan el peso adulto de cada tamaño. Lactante asume
una camada de 4 cachorros (lo más común, se ajusta a mano si hace falta).

CÓMO USAR ESTO
----------------
CATALOGO["Mediano_CachorroCrecimiento"] -> {"gramos": {...}, "der": 1303, ...}

Esto es un PUNTO DE PARTIDA, no sustituye al motor en vivo: sirve para
arrancar rápido o como respaldo si el motor no responde, pero un perro
concreto (peso exacto, alergias, patologías) sigue necesitando pasar por
motor_completo.resolver() para un menú hecho a su medida.

⚠️ POR QUÉ LOS DATOS ESTÁN EN UN JSON (26 agosto). Este archivo eran 3.081
líneas, y 3.050 de ellas eran datos: gramos de alimentos, escritos como un
diccionario de Python dentro de la carpeta `motor/`, que es donde vive la
LÓGICA. Buscar una función en el motor obligaba a pasar por encima de un
listado de menús, y cualquier diff que los tocara enterraba el cambio real.

Ahora los datos van donde van los demás datos -- junto a
`alimentos_v3_final.json` y `requerimientos_v2_final.json`, en la raíz -- y
aquí queda solo lo que es código. Ni un gramo ha cambiado: se volcó el
diccionario tal cual y se comprobó que lo que carga es idéntico.

⚠️ Y NO LLEVA SELLO en /verificar, a diferencia de los otros dos JSON, a
propósito: si estos menús se corrompieran, `_garantizar_verificado()` los
rechazaría igual que a cualquier otro menú antes de entregarlos. El
BLOQUE 8 lo comprueba con /catalogo.
"""
import json
import os

_RUTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "catalogo_menus.json")

with open(_RUTA, encoding="utf-8") as _f:
    _DATOS = json.load(_f)

CATALOGO = _DATOS["CATALOGO"]
CATALOGO_VARIANTES = _DATOS["CATALOGO_VARIANTES"]


# ─── ⚠️ EL CATÁLOGO ES CRUDO, Y HAY QUE PREGUNTÁRSELO ANTES DE SERVIRLO ──────
#
# CASO REAL, EN PRODUCCIÓN (19 de septiembre de 2026). Pidiendo un menú
# COCINADO, `/menu/v2` devolvía en 0,1 s un menú de fichas CRUDAS -- con
# `Carcasa de pollo` dentro, que es hueso carnoso -- y la respuesta decía
# `modo_de_preparacion: "cocinado"`.
#
# El hueso COCIDO astilla. En modo cocinado no es «una proporción que cede»:
# es una exclusión DURA, como una alergia, y así lo dice el propio
# `GET /vocabulario`. O sea que el atajo estaba sirviendo un plato peligroso,
# rápido y en verde.
#
# La causa es la de siempre en este repo: este catálogo se generó el 5 de
# agosto, el modo cocinado entró el 18 de septiembre, y nadie volvió a mirar
# los atajos. Es la misma familia que ya está escrita en `motor_completo`
# —«si un camino nuevo llama al motor, tiene que pasarle `patologias`»— con la
# diferencia de que aquí el olvido no se ve en ninguna cifra: el semáforo
# comprueba nutrientes, no de qué modo son las fichas.
#
# ⚠️ SE PREGUNTA POR LOS ALIMENTOS, NO POR UNA ETIQUETA. Podría ponerse aquí
# un `MODO_DEL_CATALOGO = "crudo"`, y sería una frase más que se queda
# parada: el día que se regeneren los menús para cocinado habría que acordarse
# de cambiarla. Mirar las fichas es un HECHO sobre el menú, y sigue siendo
# verdad se regenere lo que se regenere.
def vale_en_este_modo(gramos, modo, al=None):
    """¿Se puede servir este menú ya calculado para ese modo de preparación?

    `gramos` es {nombre: g}. `modo` es "crudo" o "cocinado" (None = crudo, que
    es lo que hace el resto del motor). `al` es el catálogo ya cargado: quien
    llama a esto desde `main` lo tiene a mano, y pedirlo otra vez sería cargarlo
    por cada menú.
    """
    if not gramos:
        return False
    from accesibles import vale_en
    if al is None:
        from main import cargar_v2      # importado aquí para no ciclar
        al, _ = cargar_v2()
    m = modo or "crudo"
    for nombre in gramos:
        ficha = al.get(nombre)
        # Un alimento que ya no está en el catálogo no se puede juzgar: se
        # descarta el atajo y se resuelve de verdad, que es el lado seguro.
        if not ficha or not vale_en(ficha, m):
            return False
    return True
