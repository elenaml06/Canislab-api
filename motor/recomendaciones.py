# -*- coding: utf-8 -*-
"""
LOS TECHOS DEL PERRO ADULTO SANO, QUE NO SON DE FEDIAF NI DE UNA PATOLOGÍA.

Hasta el 8 de septiembre de 2026 el motor solo conocía dos clases de límite:
los de **FEDIAF** (los 43 requisitos, que valen para cualquier perro) y los de
**patología** (más estrictos, y solo si esa patología está marcada). Faltaba una
tercera, y se veía en el resultado: SACN5 recomienda que el alimento de
CUALQUIER perro adulto sano no pase de 2000 mg de fósforo por 1000 kcal, y una
ración BARF de este motor salía con ~4000.

Ese número solo entraba por la puerta de atrás, en las dos patologías cuya
tabla lo repite —artrosis (1750) y reacción adversa al alimento (2000)—, que lo
llevan porque su población es de riesgo renal y no porque la enfermedad tenga
que ver con el fósforo. El resultado era incoherente: **el mismo perro pasaba de
4000 a 1750 por marcar «artrosis»**, y un perro sin nada se quedaba en 4000.

⚠️ POR QUÉ ESTO ES UN FICHERO Y NO CUATRO LÍNEAS EN `motor_completo.py`

Es la misma regla que sacó la tabla de patologías de dentro del código el 28 de
agosto: **un número que decide si un menú se entrega tiene que poder
auditarse**, y no se audita lo que está enterrado entre `if`s. Aquí no hay ni
una cifra: están en `recomendaciones_adulto.json`, con su fuente, su cita
literal y el porqué, y las vigila el BLOQUE 57.

⚠️ Y POR QUÉ NO VAN EN NINGUNO DE LOS DOS FICHEROS QUE YA HABÍA

- En `requerimientos_v2_final.json` no, porque ese fichero **es** la Tabla
  III-3b de FEDIAF y `auditar_fediaf.py` comprueba sus 43 filas contra el PDF
  celda a celda. Meter ahí un número de un libro de texto es exactamente cómo se
  coló en agosto una fila «Fibra» con mínimo y máximo inventados.
- En `patologias.json` tampoco, porque esto **no es una patología**: se aplica
  al perro que no tiene ninguna.

CÓMO SE COMBINA CON LO DEMÁS

Igual que un tope de patología: con `min()`, así que solo puede APRETAR. Si el
perro además tiene una patología cuya tabla pide menos fósforo (la renal pide
1200), manda la patología. Nunca al revés.
"""
import json
import os

_RUTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "recomendaciones_adulto.json")

with open(_RUTA, encoding="utf-8") as _f:
    CRUDO = json.load(_f)

POR_ETAPA = CRUDO["por_etapa"]


def topes_de_la_etapa(etapa):
    """Los techos del libro para esta etapa, en la forma que espera el solver.

    Devuelve `{clave_nutriente: valor}`, o `{}` si la etapa no tiene ninguno.

    Las etapas que NO tienen ninguno son las de crecimiento, gestación y
    lactancia, y no es un olvido: SACN5 les da sus propias tablas (17-1 para el
    cachorro, 33-5 para el de raza grande, 15-5 para la reproductora) con otros
    números, y además el mínimo de fósforo de un cachorro joven que exige FEDIAF
    (2250) está POR ENCIMA del techo del adulto (2000). Aplicárselo no sería un
    techo: sería dejarlo sin menú.
    """
    ficha = POR_ETAPA.get(etapa) or {}
    return {clave: t["valor"]
            for clave, t in (ficha.get("topes_por_1000kcal") or {}).items()}


def con_procedencia(etapa):
    """Lo mismo, pero cada techo sabiendo de dónde viene y por qué.

    Para poder decirle a alguien «lo que te está apretando el fósforo no es tu
    perro, es la recomendación del libro para cualquier adulto», que es la
    diferencia entre un límite y una pared.
    """
    ficha = POR_ETAPA.get(etapa) or {}
    fuera = []
    for clave, t in (ficha.get("topes_por_1000kcal") or {}).items():
        fuera.append({"tipo": "tope", "clave": clave, "valor": t["valor"],
                      "patologia": None,
                      "nombre_patologia": "Recomendación para el perro adulto sano",
                      "fuente": t.get("fuente"), "por_que": t.get("por_que")})
    return fuera
