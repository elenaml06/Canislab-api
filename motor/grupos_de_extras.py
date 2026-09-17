# -*- coding: utf-8 -*-
"""El grupo al que pertenece cada Extra (Aceite, Semillas, Huevo, Sal...).

⚠️ AQUÍ NO HAY NINGUNA LISTA (15 de septiembre de 2026). Se lee
`grupo_de_cada_extra` de `alimentos_como_se_presentan.json`, que es EL MISMO
fichero con el que la app pinta los extras agrupados. Escribir aquí una segunda
copia sería la quinta vez que este repo tropieza con lo mismo: dos listas del
mismo conjunto se desincronizan, y la que está en el sitio equivocado no da
error -- se queda parada y la pantalla se ve perfecta.
"""
import json
import os

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RUTA = os.path.join(os.path.dirname(_AQUI), "alimentos_como_se_presentan.json")

try:
    with open(_RUTA, encoding="utf-8") as _f:
        GRUPO_DE_CADA_EXTRA = json.load(_f).get("grupo_de_cada_extra") or {}
except OSError:
    GRUPO_DE_CADA_EXTRA = {}


def grupo_de_extra(nombre):
    """«Aceite», «Semillas», «Huevo»… o None si ese alimento no es un Extra."""
    return GRUPO_DE_CADA_EXTRA.get(nombre)
