# -*- coding: utf-8 -*-
"""
CANISLAB — LA CONVERSIÓN DE CADA CIFRA, REHECHA Y NO CREÍDA

⚠️ POR QUÉ EXISTE (9 de septiembre de 2026, de noche). Elena:

    «lo de sacn5 de la corrección de densidad, tienes que hacer algún tipo de
     escrito o algo para que no sea manual y para que si hay algún valor que no
     esté bien hecho que lo cace»

QUÉ PASABA. Las 92 cifras de `patologias.json` vienen casi todas de una tabla
que las publica en **% de materia seca**, y el motor trabaja **por 1000 kcal**.
La conversión estaba hecha una vez y **contada en prosa**, dentro del campo
`por_que` de cada cifra: «%MS x 2,5 = g/1000 kcal a la densidad de referencia de
4000 kcal EM/kg MS». Eso tiene dos problemas y los dos han mordido ya:

  1. **Una frase no se ejecuta.** El 8 de septiembre una de esas conversiones se
     escribió como x25 en vez de x2,5 — la fenilalanina+tirosina de la dermatitis
     atópica, 32,5 en lugar de 3,25 — y lo único que la cazó fue que alguien la
     leyó. Diez veces el valor bueno, con forma de dato bueno.

  2. **La densidad no es la misma en todas las fuentes**, y elegirla mal desplaza
     la cifra un 14 % sin que nada chirríe. Pasó al revés: se dedujo que SACN5
     usaba 3,5 kcal/g (Box 1-2) y que por tanto las 68 cifras que vienen de ese
     libro estaban un 14 % apretadas de más. **Es falso**, y este script es lo
     que lo demuestra sin que haya que fiarse de nadie: de las 24 tablas de SACN5
     que cita `patologias.json`, **una sola declara densidad**, la 13-3, y dice
     literalmente «Concentrations presume an energy density of 4.0 kcal/g». Sus
     propias filas lo confirman: fósforo 0,8 % MS -> 2000 mg/1000 kcal, sodio
     0,4 % -> 1000, que son exactamente las dos cifras que aplica el motor. El
     3,5 del Box 1-2 es un ejemplo trabajado con un alimento concreto, no la
     densidad de las tablas.

CÓMO FUNCIONA. Cada cifra lleva un bloque `conversion` con TRES datos y una
cita, y este script **rehace la cuenta** y la compara con el valor que aplica el
solver:

    "conversion": {
      "valor_en_la_fuente": 0.8,
      "unidad_en_la_fuente": "%MS",
      "densidad_kcal_por_g_MS": 4.0,
      "cita": "Tabla 13-3, nota al pie: «Concentrations presume an energy
               density of 4.0 kcal/g»"
    }

Y una cifra SIN ese bloque también falla. Ese es el punto: lo que no se puede
rehacer no se puede auditar, y una tabla de números que deciden si un menú se
entrega no puede tener celdas que nadie sepa de dónde salen.

    python3 auditar_conversiones.py
"""
import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

# Los bloques de `patologias.json` que llevan cifras que el motor aplica (o que
# están escritas para no aplicarse, que también hay que poder auditar).
BLOQUES = ("topes_por_1000kcal", "suelos_por_1000kcal",
           "topes_por_1000kcal_si_ademas", "suelos_por_1000kcal_si_ademas",
           "limites_escritos_que_el_solver_no_aplica")

# Cómo se pasa cada unidad de fuente a «por 1000 kcal».
#
# La aritmética, que es una sola: un nutriente al X % de materia seca son X x 10
# gramos por kg de MS; y 1 kg de MS son 1000 x densidad kcal. O sea que por 1000
# kcal hay (X x 10) / densidad gramos. En miligramos, mil veces más.
#
# NO se convierte con la densidad del ALIMENTO sino con la que declara la
# FUENTE, y esa distinción es el corazón del asunto: la cifra por 1000 kcal es
# la invariante. Lo trabaja el propio SACN5 en su Caso 1-1 («dividing the food
# energy density by the requirement energy density»).
#
# ⚠️ Y EL SEGUNDO FACTOR, que es donde se falló de verdad. Algunas fuentes dan el
# nutriente en una unidad que NO es la del catálogo: la vitamina E en UI cuando
# nosotros medimos mg de tocoferol natural, la vitamina D en UI cuando medimos
# µg. Esa segunda conversión va en `factor_a_la_unidad_del_motor`, con su propia
# cita, porque el 8 de septiembre se escribió el suelo de vitamina E de la
# artrosis tratando las UI como si fueran mg — 100 en vez de 67,1 — y lo que lo
# cazó no fue ninguna comprobación: fue que la artrosis dejó de dar menú.
def _convertir(valor, unidad, densidad, factor=1.0):
    u = (unidad or "").strip()
    valor = valor * factor
    if u == "%MS":                 # gramos por 1000 kcal
        return valor * 10.0 / densidad
    if u == "%MS->mg":             # el nutriente va en mg en el MAPA
        return valor * 10000.0 / densidad
    if u == "mg/kg MS":
        return valor / densidad
    if u == "g/kg MS":
        return valor * 1000.0 / densidad
    if u == "UI/kg MS":
        return valor / densidad
    if u == "mg/100 kcal":
        return valor * 10.0
    if u == "g/100 kcal":
        return valor * 10.0
    if u == "mg/kg MS->ug":       # el catálogo mide µg (selenio, vitamina D)
        return valor * 1000.0 / densidad
    if u == "g/kg al 12% humedad":
        # Los máximos LEGALES del Reglamento (UE) van sobre pienso completo al
        # 12 % de humedad, no sobre materia seca. Se pasa a MS dividiendo por
        # 0,88 y desde ahí es un g/kg MS normal.
        return (valor / 0.88) * 1000.0 / densidad
    if u == "por 1000 kcal":       # la fuente ya la da en la unidad del motor
        return valor
    if u == "adimensional":        # un ratio no se convierte
        return valor
    if u == "derivado de otro limite":
        return valor
    return None


def auditar():
    tabla = json.load(open(os.path.join(RAIZ, "patologias.json"), encoding="utf-8"))["patologias"]
    fallos = []
    revisadas = comprobadas = sin_bloque = 0
    for pat, ficha in sorted(tabla.items()):
        for bloque in BLOQUES:
            celdas = ficha.get(bloque) or {}
            if not isinstance(celdas, dict):
                continue
            for nut, celda in sorted(celdas.items()):
                # Una celda con `valor: null` es un limite ESCRITO sin cifra -- el
                # ácido ascórbico del oxalato, la metionina de la hepatopatía --, o
                # sea prosa. No hay conversión que rehacer porque no hay número.
                if not isinstance(celda, dict) or celda.get("valor") is None:
                    continue
                revisadas += 1
                conv = celda.get("conversion")
                donde = f"{pat}/{bloque}/{nut}"
                if not conv:
                    sin_bloque += 1
                    fallos.append(
                        f"{donde}: no dice de qué cifra de la fuente sale. Sin `conversion` "
                        f"(valor_en_la_fuente + unidad_en_la_fuente + densidad_kcal_por_g_MS + "
                        f"cita) esta celda no se puede rehacer, y lo que no se puede rehacer no "
                        f"se puede auditar: es exactamente cómo se coló un x25 en vez de un x2,5")
                    continue
                faltan = [c for c in ("valor_en_la_fuente", "unidad_en_la_fuente",
                                      "densidad_kcal_por_g_MS", "cita") if c not in conv]
                # Un factor de unidad sin explicar es medio dato: la cifra sale
                # bien y nadie puede comprobar de dónde salió el multiplicador.
                if conv.get("factor_a_la_unidad_del_motor") and not conv.get("por_que_el_factor"):
                    fallos.append(f"{donde}: lleva `factor_a_la_unidad_del_motor` y no dice de "
                                  f"dónde sale. Ese factor es exactamente donde se falló el 8 de "
                                  f"septiembre con las UI de la vitamina E")
                if faltan:
                    fallos.append(f"{donde}: al bloque `conversion` le faltan {faltan}")
                    continue
                dens = conv["densidad_kcal_por_g_MS"]
                esperado = _convertir(float(conv["valor_en_la_fuente"]),
                                      conv["unidad_en_la_fuente"], float(dens),
                                      float(conv.get("factor_a_la_unidad_del_motor") or 1.0))
                if esperado is None:
                    fallos.append(f"{donde}: unidad de fuente desconocida "
                                  f"«{conv['unidad_en_la_fuente']}». Si es nueva, hay que añadirla "
                                  f"a `_convertir` con su aritmética escrita, no aproximarla")
                    continue
                aplicado = float(celda["valor"])
                # Un margen del 1 % cubre el redondeo con el que se escriben las
                # cifras (2286 por 2285,7). Cualquier cosa mayor es otra cuenta.
                if abs(aplicado - esperado) > max(0.01 * esperado, 1e-9):
                    ajuste = celda.get("ajustado_a_proposito") or conv.get("ajustado_a_proposito")
                    if ajuste:
                        comprobadas += 1
                        continue
                    fallos.append(
                        f"{donde}: el motor aplica {aplicado:g} y la conversión de la fuente da "
                        f"{esperado:.4g} ({conv['valor_en_la_fuente']} {conv['unidad_en_la_fuente']} "
                        f"a {dens} kcal/g MS). Si el número se apartó a propósito, tiene que "
                        f"decirlo `ajustado_a_proposito` con el motivo; si no, uno de los dos "
                        f"está mal")
                    continue
                comprobadas += 1
    print(f"  {revisadas} cifras · {comprobadas} con la conversión rehecha y correcta · "
          f"{sin_bloque} sin declarar de dónde salen")
    return fallos


if __name__ == "__main__":
    fs = auditar()
    if fs:
        print(f"\n❌ {len(fs)} problemas:")
        for f in fs[:60]:
            print("  -", f)
        if len(fs) > 60:
            print(f"  ... y {len(fs)-60} más")
        sys.exit(1)
    print("Discrepancias: 0")
    sys.exit(0)
