# -*- coding: utf-8 -*-
"""
LOS REQUISITOS QUE NO SON UN NÚMERO FIJO.

Hasta el 8 de septiembre de 2026 el motor daba por hecho que un requisito es una
celda: nutriente, etapa, número. Y casi siempre lo es. Pero hay otros escritos
así:

    «The requirement for α-linolenic acid **varies depending upon linoleic acid
     content of the diet**»                                        (NRC 2006)

    «The recommendation for protein **assumes the diet contains some
     carbohydrate**… If carbohydrate is absent… the protein requirement is much
     higher, and may be double»                                    (FEDIAF 2025)

    «The arginine requirement **increases with increased protein content**»
                                                                   (FEDIAF 2025)

**Ninguno de esos tiene forma de fila**, así que ninguno lo encontró el trabajo de
transcribir tablas celda a celda — que estaba bien hecho y no sirvió para esto.
Aparecieron leyendo el texto entero, y de ahí sale este módulo.

⚠️ POR QUÉ ESTO ES UN FICHERO Y NO UN `if`

La misma regla de siempre: **un número que decide si un menú se entrega tiene que
poder auditarse.** Las cifras están en `requisitos_condicionales.json`, con la
cita literal de su fuente, el porqué y la medida que se hizo antes de aplicarlas.
Aquí no hay ni una.

⚠️ Y POR QUÉ NO VAN EN LOS FICHEROS QUE YA HABÍA

- `requerimientos_v2_final.json` **es** la Tabla III-3b de FEDIAF, y
  `auditar_fediaf.py` la compara con el PDF celda a celda. Un valor que depende
  de la dieta no es una celda de esa tabla.
- `patologias.json` es por enfermedad, y esto le pasa a un perro **sano**.
- `recomendaciones_adulto.json` son los techos de SACN5 para el adulto sano.
  Esto son **suelos**, y de otra fuente.

Cada uno de los cuatro dice una cosa distinta, y mezclarlos es cómo se
desincronizan.
"""
import json
import os

_RUTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "requisitos_condicionales.json")

with open(_RUTA, encoding="utf-8") as _f:
    CRUDO = json.load(_f)

REGLAS = CRUDO["reglas"]


def suelos_de_la_etapa(etapa):
    """Los suelos condicionales que aplican a esta etapa, `{clave: valor}`.

    De momento solo hay uno —la proteína de gestación y lactancia— y se aplica
    **siempre** en esas etapas, sin mirar los hidratos de la ración. No es un
    atajo: una ración BARF es carne, hueso, víscera y como mucho un 10 % de
    verdura, así que es «carbohydrate absent or at a very low level» por
    construcción. El catálogo ni siquiera tiene clave de hidratos, y ponerla
    para deducir algo que ya sabemos sería inventar precisión.

    Si algún día el motor formulara con cereal, esta función es donde habría que
    mirarlo de verdad.
    """
    fuera = {}
    for regla in REGLAS.values():
        if regla.get("tipo") != "suelo":
            continue
        if etapa not in (regla.get("aplica_a_etapas") or []):
            continue
        clave = regla["nutriente"]
        fuera[clave] = max(fuera.get(clave, 0.0), regla["valor"])
    return fuera


def con_procedencia(etapa):
    """Los mismos, sabiendo de dónde vienen, para poder decirlo.

    Un límite que aprieta y no se puede nombrar es una pared: quien lo choca no
    sabe contra qué. Lo usa el diagnóstico de «¿qué me está bloqueando?».
    """
    fuera = []
    for clave_regla, regla in sorted(REGLAS.items()):
        if regla.get("tipo") != "suelo":
            continue
        if etapa not in (regla.get("aplica_a_etapas") or []):
            continue
        fuera.append({"tipo": "suelo", "clave": regla["nutriente"],
                      "valor": regla["valor"], "patologia": None,
                      "nombre_patologia": regla.get("nombre", clave_regla),
                      "fuente": regla.get("fuente"), "por_que": regla.get("por_que")})
    return fuera
