# -*- coding: utf-8 -*-
"""
LAS RAZAS QUE OFRECE LA FICHA — carga `razas.json` y nada mas.

⚠️ POR QUE EXISTE ESTE ARCHIVO (11 de septiembre de 2026)

Elena: «esto tiene que ser para TODO, razas, tamaño, etapa, actividad,
preguntas para las patologias de veterinarios, todo».

Hasta hoy las 255 razas vivian SOLO en `src/App.jsx` del repo de la app: 255
filas escritas dentro del JavaScript, sin nadie que las mirara. El motor no
las tenia, asi que no podia comprobar ni lo mas basico -- que el tamaño que
manda la app sea uno de los seis que conoce el catalogo, o que las tres listas
de razas de `der.py` (las dos con cifra propia de FEDIAF y las dos de mas y
menos gasto) escriban los nombres EXACTAMENTE como los escribe la app. Un
nombre con una tilde distinta y el Gran Danes deja de recibir sus 200
kcal/kg^0,75 en silencio, con el menu saliendo verde igual.

Aqui no hay ni una cifra, igual que en `patologias.py`: los numeros viven en el
JSON para que se puedan auditar.
"""
import json
import os

_RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "razas.json")


def cargar_crudo(ruta=None):
    """El JSON entero, con su `_meta`. Lo usa la auditoria."""
    with open(ruta or _RUTA, encoding="utf-8") as f:
        return json.load(f)


_DATOS = cargar_crudo()

# La lista tal cual, ordenada por nombre. Cada fila:
#   {"nombre", "tamano", "pesoMin", "pesoMax", "pesoMedio"}
RAZAS = _DATOS["razas"]

# Por nombre, para no recorrer 255 filas cada vez.
POR_NOMBRE = {r["nombre"]: r for r in RAZAS}

# Los seis tamaños, en orden de menor a mayor. Son los mismos seis con los que
# `catalogo_menus.json` indexa sus menus precalculados (`{tamano}_{etapa}`), y
# eso no es casualidad: si la app mandara un septimo, la clave no existiria y
# la vista previa se quedaria sin menu sin decir por que.
TAMANOS = list(_DATOS["_meta"]["tamanos"])


def raza(nombre):
    """La fila de esa raza, o None. El nombre tiene que ser EXACTO."""
    return POR_NOMBRE.get(nombre)
