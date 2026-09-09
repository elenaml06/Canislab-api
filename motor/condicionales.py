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
- `recomendaciones_libro.json` son los techos de SACN5 para el adulto sano.
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


def factor_sobre_el_minimo(nombre_requisito, etapa):
    """El factor por el que hay que multiplicar el mínimo de FEDIAF, o 1.0.

    ⚠️ HOY SOLO HAY UNO, Y NO ES UN CAPRICHO DE FEDIAF: es la condición sobre la
    que cuelga toda su tabla. §2.2 «Scope» dice que la guía vale para alimentos
    «with normal digestibility (i.e. ≥70 % DM digestibility; ≥80 % protein
    digestibility)», y §3.2.1 dice qué hacer cuando eso no se puede garantizar:
    subir los aminoácidos esenciales «by a minimum of 10 %».

    **No podemos garantizarlo.** El catálogo no tiene columna de digestibilidad,
    y una ración BARF lleva entre un 20 y un 60 % de hueso carnoso, que es lo
    menos digestible del plato. No es que salgamos por debajo: es que no lo
    sabemos, y la regla está escrita justo para ese caso.

    Vive aquí y no en `verificar.py` por lo mismo que el resto de este módulo:
    la cifra va en el JSON, con su cita, y el código solo la lee. Lo llama
    `minimo_de()`, que es el ÚNICO sitio que escala mínimos — así el solver y el
    semáforo lo reciben por la misma puerta y no pueden discrepar.
    """
    factor = 1.0
    for regla in REGLAS.values():
        if regla.get("tipo") != "factor_sobre_el_minimo":
            continue
        if nombre_requisito not in (regla.get("nutrientes") or []):
            continue
        if etapa not in (regla.get("aplica_a_etapas") or []):
            continue
        factor = max(factor, float(regla["valor"]))
    return factor


def suelo_relativo_de(etapa, clave_nutriente, valor_del_que_depende):
    """El suelo de `clave_nutriente` cuando depende de otro nutriente del MISMO menú.

    Hoy solo hay uno —la arginina según la proteína, Tabla VII-13 de FEDIAF—
    pero la forma es general: `ancla + coeficiente × (lo_que_hay − ancla_del_otro)`,
    y nunca por debajo del ancla.

    `valor_del_que_depende` va en las mismas unidades que todo lo demás: por
    1000 kcal. Devuelve `None` si no hay regla para esa etapa y ese nutriente,
    para que quien llama no tenga que saber si existe.

    ⚠️ NO compone con el mínimo de FEDIAF: eso lo hace quien llama, con un
    `max()`. Aquí solo se responde «¿qué pide esta regla?», que es lo que
    permite que el solver y el semáforo hagan la misma cuenta sin copiarla.
    """
    for regla in REGLAS.values():
        if regla.get("tipo") != "suelo_relativo":
            continue
        if regla["nutriente"] != clave_nutriente:
            continue
        ancla = (regla.get("anclas_por_etapa") or {}).get(etapa)
        if not ancla:
            continue
        extra = max(0.0, float(valor_del_que_depende) - float(ancla["proteina"]
                                                             if regla["depende_de"] == "proteina"
                                                             else ancla[regla["depende_de"]]))
        return float(ancla["nutriente"]) + float(regla["coeficiente"]) * extra
    return None


def suelos_relativos_de_la_etapa(etapa):
    """Las reglas de suelo relativo que aplican a esta etapa, en crudo.

    Las necesita el SOLVER, que no puede llamar a `suelo_relativo_de` porque
    todavía no sabe cuánta proteína va a tener el menú: tiene que meter la
    regla como una fila lineal y dejar que la resuelva el propio LP.
    """
    fuera = []
    for clave_regla, regla in sorted(REGLAS.items()):
        if regla.get("tipo") != "suelo_relativo":
            continue
        ancla = (regla.get("anclas_por_etapa") or {}).get(etapa)
        if not ancla:
            continue
        fuera.append({
            "clave_regla": clave_regla,
            "nutriente": regla["nutriente"],
            "depende_de": regla["depende_de"],
            "coeficiente": float(regla["coeficiente"]),
            "ancla_nutriente": float(ancla["nutriente"]),
            "ancla_depende_de": float(ancla[regla["depende_de"]]),
            "nombre": regla.get("nombre", clave_regla),
            "fuente": regla.get("fuente"),
        })
    return fuera


def ratios_de_la_etapa(etapa):
    """Las relaciones entre dos nutrientes que hay que respetar en esta etapa.

    Mismo patrón que el ratio Ca:P, que ya vive en `requerimientos_v2_final.json`
    porque **ese** sí es una fila de la Tabla III-3b de FEDIAF. Este no lo es
    —es del NRC—, así que vive aquí. Ver el `por_que` de la regla.
    """
    fuera = []
    for clave_regla, regla in sorted(REGLAS.items()):
        if regla.get("tipo") != "ratio":
            continue
        rango = (regla.get("rangos_por_etapa") or {}).get(etapa)
        if not rango:
            continue
        fuera.append({
            "clave_regla": clave_regla,
            "numerador": regla["numerador"],
            "denominador": regla["denominador"],
            "min": rango.get("min"),
            "max": rango.get("max"),
            "nombre": regla.get("nombre", clave_regla),
            "fuente": regla.get("fuente"),
            "por_que": regla.get("por_que"),
        })
    return fuera
