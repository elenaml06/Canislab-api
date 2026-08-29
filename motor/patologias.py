# -*- coding: utf-8 -*-
"""
LOS TOPES POR PATOLOGÍA, QUE AHORA SON DATOS.

Hasta el 28 de agosto esta tabla era un `dict` de 200 líneas dentro de
`motor_completo.py`, mezclando cuatro cosas que no se parecen: los números,
el motivo clínico de cada número, los textos que lee el usuario y la lógica
de qué pasa en crecimiento.

Se saca por lo mismo que se sacaron los menús del catálogo y la tabla de
FEDIAF: **un número que decide si un menú se entrega tiene que poder
auditarse**, y no se puede auditar lo que está enterrado entre `if`s. La
tabla de FEDIAF tiene `auditar_fediaf.py` desde el 25 de agosto y por eso
sabemos que sus 43 filas cuadran con el PDF. Esta no tenía nada.

⚠️ LO QUE VIGILA `auditar_patologias.py` (BLOQUE 32), y por qué cada cosa:

  1. Cada cifra con su FUENTE y su POR QUÉ. Es la regla del catálogo entero.
  2. Ninguna patología FORMULABLE puede tener un tope por debajo del mínimo
     de FEDIAF. Si lo tiene, no es un tope: es una dieta de prescripción, y
     entonces va con `formulable: false`. Medido: de las 47 patologías que
     propuso la revisión clínica, SIETE cifras estaban por debajo del
     mínimo -- fósforo 800 en IRIS 3, cobre 1,8 en hepatopatía, proteína 35.
     No eran errores: eran dietas terapéuticas mezcladas con topes normales
     en el mismo campo, y así no se distinguen.
  3. Que la clave del nutriente EXISTA en el MAPA del verificador. Es el
     fallo de la fibra otra vez: una fila que el motor no mira nunca porque
     su clave no está en el mapa, y nadie se entera porque el menú sale
     verde igual.
  4. Que soltar un tope en crecimiento venga SIEMPRE con su aviso. Regla 5
     del CLAUDE.md: se puede bajar de peldaño, pero se dice.

El motor sigue viendo exactamente la misma forma de diccionario que antes:
este módulo la reconstruye al cargar, así que `topes_de_patologias()`,
`patologias_bloquean()` y `avisos_de_patologias()` no se han tocado.
"""
import json, os

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RUTA = os.path.join(_AQUI, "..", "patologias.json")


def cargar_crudo(ruta=None):
    """El JSON tal cual, con fuentes y motivos. Lo usa la auditoría."""
    with open(ruta or _RUTA, encoding="utf-8") as f:
        return json.load(f)


def _a_forma_del_motor(crudo):
    """Reconstruye el dict que el solver espera, sin metadatos.

    La forma del motor es la que era: valores desnudos. Los metadatos
    (fuente, por_que, motivo_no_formulable) no llegan aquí a propósito --
    el solver no tiene nada que hacer con ellos y mezclarlos volvería a
    poner la documentación dentro del cálculo, que es de lo que veníamos.
    """
    salida = {}
    for clave, p in crudo["patologias"].items():
        e = {}
        topes = {n: t["valor"] for n, t in (p.get("topes_por_1000kcal") or {}).items()}
        if topes:
            e["max_por_1000kcal"] = topes
        cond = p.get("max_pct_kcal_grasa_si_ademas")
        if cond:
            e["max_pct_kcal_grasa_si_ademas"] = (cond["valor"], tuple(cond["requiere"]))
        for campo in ("solo_en_adulto", "en_crecimiento", "excluye_fruta",
                      "sin_dieta_automatica",
                      # ⚠️ LO DEL VETERINARIO (29 agosto). `formulable_por_
                      # profesional` dice si a un profesional acreditado se le
                      # formula; `necesita_bajo_fediaf` dice si para TRATAR de
                      # verdad haría falta bajar de un mínimo de FEDIAF, que es
                      # la frontera que exige firma (ver VETERINARIOS.md).
                      "formulable_por_profesional", "necesita_bajo_fediaf",
                      "nutriente_frontera", "objetivo_terapeutico_por_1000kcal"):
            if campo in p:
                e[campo] = p[campo]
        avisos = p.get("avisos") or {}
        if avisos.get("general"):
            e["aviso"] = avisos["general"]
        if avisos.get("crecimiento"):
            e["aviso_crecimiento"] = avisos["crecimiento"]
        if avisos.get("profesional"):
            e["aviso_profesional"] = avisos["profesional"]
        if avisos.get("profesional_crecimiento"):
            e["aviso_profesional_crecimiento"] = avisos["profesional_crecimiento"]
        salida[clave] = e
    return salida


CRUDO = cargar_crudo()
PATOLOGIAS = _a_forma_del_motor(CRUDO)
