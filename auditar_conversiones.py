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
           # ⚠️ `ratios` ENTRA AQUI EL 10 DE SEPTIEMBRE, el dia que se aplico.
           # Un ratio es adimensional y no hay conversion que rehacer, asi que
           # parece que no pinta nada en una auditoria de conversiones. Pinta:
           # lo que este script comprueba de verdad es que CADA cifra que decide
           # si un menu sale diga de que numero de la fuente sale. Dejar fuera
           # las que "no se convierten" es como se cuelan: la celda existe, no
           # la mira nadie, y el menu sale verde igual.
           "ratios",
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


# ⚠️ AÑADIDO (10 septiembre) — LOS TECHOS DEL LIBRO PARA EL PERRO SANO.
#
# `recomendaciones_libro.json` es la TERCERA clase de límite del motor -- ni
# FEDIAF ni patología: lo que el libro recomienda al perro que no tiene nada --
# y sus doce cifras salen todas de un porcentaje de materia seca, exactamente
# igual que las de patología. Y estaban en el mismo estado del que veníamos: la
# conversión hecha una vez y CONTADA EN PROSA dentro de `por_que` («%MS x 2500 =
# mg/1000 kcal»). Una frase no se ejecuta, y ahí es donde se coló un x25 en vez
# de un x2,5 el 8 de septiembre.
#
# Deciden cosas gordas: el techo de calcio del cachorro de raza grande (2750) es
# un 39 % más bajo que el máximo de FEDIAF, y el de fósforo en crecimiento
# (3250 / 2750) es el ÚNICO que hay, porque FEDIAF deja esas dos celdas vacías.
def auditar_recomendaciones():
    ruta = os.path.join(RAIZ, "recomendaciones_libro.json")
    tabla = json.load(open(ruta, encoding="utf-8"))["por_etapa"]
    fallos, revisadas, comprobadas, sin_bloque = [], 0, 0, 0

    def recorrer(nodo, ruta_txt):
        nonlocal revisadas, comprobadas, sin_bloque
        if not isinstance(nodo, dict):
            return
        if isinstance(nodo.get("valor"), (int, float)):
            revisadas += 1
            conv = nodo.get("conversion")
            if not conv:
                sin_bloque += 1
                fallos.append(
                    f"{ruta_txt}: no dice de qué cifra de la fuente sale. Sin `conversion` no "
                    f"se puede rehacer, y lo que no se puede rehacer no se puede auditar -- "
                    f"que es exactamente cómo se coló un x25 en vez de un x2,5")
                return
            faltan = [c for c in ("valor_en_la_fuente", "unidad_en_la_fuente",
                                  "densidad_kcal_por_g_MS", "cita") if c not in conv]
            if faltan:
                fallos.append(f"{ruta_txt}: al bloque `conversion` le faltan {faltan}")
                return
            esperado = _convertir(float(conv["valor_en_la_fuente"]),
                                  conv["unidad_en_la_fuente"],
                                  float(conv["densidad_kcal_por_g_MS"]),
                                  float(conv.get("factor_a_la_unidad_del_motor") or 1.0))
            if esperado is None:
                fallos.append(f"{ruta_txt}: unidad de fuente desconocida "
                              f"«{conv['unidad_en_la_fuente']}»")
                return
            aplicado = float(nodo["valor"])
            if abs(aplicado - esperado) > max(0.01 * esperado, 1e-9):
                if nodo.get("ajustado_a_proposito") or conv.get("ajustado_a_proposito"):
                    comprobadas += 1
                    return
                fallos.append(
                    f"{ruta_txt}: el motor aplica {aplicado:g} y la conversión de la fuente da "
                    f"{esperado:.4g} ({conv['valor_en_la_fuente']} "
                    f"{conv['unidad_en_la_fuente']} a {conv['densidad_kcal_por_g_MS']} kcal/g "
                    f"MS). Uno de los dos está mal")
                return
            comprobadas += 1
            return
        for clave, hijo in nodo.items():
            recorrer(hijo, f"{ruta_txt}/{clave}")

    for etapa, ficha in sorted(tabla.items()):
        recorrer(ficha, etapa)
    print(f"  {revisadas} techos del libro · {comprobadas} con la conversión rehecha y "
          f"correcta · {sin_bloque} sin declarar de dónde salen")
    return fallos


# ⚠️ AÑADIDO (10 septiembre) — LOS REQUISITOS QUE DEPENDEN DE LA PROPIA DIETA.
#
# `requisitos_condicionales.json` es el tercer sitio con cifras sacadas de una
# fuente, y dos de ellas llevan las DOS conversiones -- la de densidad y la de
# unidad --, que es donde se falla de verdad: la vitamina E del perro de trabajo
# sale de «>=500 IU/kg (DM)» de SACN5 y hay que pasarla a mg de tocoferol
# NATURAL. Tratar esas UI como si fueran mg es exactamente el fallo del 8 de
# septiembre con la vitamina E de la artrosis (100 en vez de 67,1), y lo que lo
# cazó no fue ninguna comprobación: fue que la artrosis dejó de dar menú.
#
# Las reglas cuyo número NO es un `valor` suelto -- el ratio linoleico:
# linolénico, que es un rango por etapa, y las anclas de arginina, que son una
# tabla entera de FEDIAF -- van declaradas abajo con su motivo, para que
# saltarse una no pueda pasar en silencio.
SIN_CONVERSION_CONDICIONALES = {
    "arginina_segun_proteina": (
        "Sus números no son un `valor`: son las anclas por etapa de la Tabla VII-13 de "
        "FEDIAF, que ya vienen POR 1000 KCAL en la unidad del motor. No hay conversión "
        "que rehacer; lo que hay que comprobar es la aritmética de la recta, y eso lo "
        "hace el BLOQUE 60."),
    "ratio_linoleico_linolenico": (
        "Es un rango por etapa y adimensional (2,6-26 y 2,6-16, NRC 2006 cap.5). No hay "
        "unidad que convertir. Lo comprueba el BLOQUE 60."),
    "zinc_y_cobre_cuando_el_calcio_esta_alto": (
        "El umbral de calcio que lleva dentro (3750 mg/1000 kcal, Tabla 32-1 de SACN5) "
        "no es el valor de la regla: la regla es `documentado_sin_cifra` y no la aplica "
        "el solver. Lo mide en vivo el BLOQUE 69."),
}


def auditar_condicionales():
    ruta = os.path.join(RAIZ, "requisitos_condicionales.json")
    reglas = json.load(open(ruta, encoding="utf-8"))["reglas"]
    fallos, revisadas, comprobadas = [], 0, 0
    for clave, regla in sorted(reglas.items()):
        if not isinstance(regla.get("valor"), (int, float)):
            continue
        if clave in SIN_CONVERSION_CONDICIONALES:
            continue
        revisadas += 1
        conv = regla.get("conversion")
        if not conv:
            fallos.append(
                f"{clave}: tiene un valor ({regla['valor']}) y no dice de qué cifra de la "
                f"fuente sale. O lleva `conversion`, o va declarada en "
                f"SIN_CONVERSION_CONDICIONALES con el motivo")
            continue
        faltan = [c for c in ("valor_en_la_fuente", "unidad_en_la_fuente",
                              "densidad_kcal_por_g_MS", "cita") if c not in conv]
        if conv.get("factor_a_la_unidad_del_motor") and not conv.get("por_que_el_factor"):
            fallos.append(f"{clave}: lleva `factor_a_la_unidad_del_motor` y no dice de dónde "
                          f"sale. Ese factor es donde se falló el 8 de septiembre con las UI "
                          f"de la vitamina E")
        if faltan:
            fallos.append(f"{clave}: al bloque `conversion` le faltan {faltan}")
            continue
        esperado = _convertir(float(conv["valor_en_la_fuente"]), conv["unidad_en_la_fuente"],
                              float(conv["densidad_kcal_por_g_MS"]),
                              float(conv.get("factor_a_la_unidad_del_motor") or 1.0))
        if esperado is None:
            fallos.append(f"{clave}: unidad de fuente desconocida "
                          f"«{conv['unidad_en_la_fuente']}»")
            continue
        aplicado = float(regla["valor"])
        if abs(aplicado - esperado) > max(0.01 * esperado, 1e-9):
            if regla.get("ajustado_a_proposito") or conv.get("ajustado_a_proposito"):
                comprobadas += 1
                continue
            fallos.append(
                f"{clave}: el motor aplica {aplicado:g} y la conversión de la fuente da "
                f"{esperado:.4g} ({conv['valor_en_la_fuente']} {conv['unidad_en_la_fuente']} a "
                f"{conv['densidad_kcal_por_g_MS']} kcal/g MS). Uno de los dos está mal")
            continue
        comprobadas += 1

    # Y una declaración caducada tiene que salir: si la regla ya no existe, la
    # excusa tampoco vale.
    for clave in sorted(SIN_CONVERSION_CONDICIONALES):
        if clave not in reglas:
            fallos.append(f"{clave} está en SIN_CONVERSION_CONDICIONALES y ya no es una regla "
                          f"de `requisitos_condicionales.json`. Una excepción caducada es una "
                          f"alarma apagada")
    print(f"  {revisadas} requisitos condicionales · {comprobadas} con la conversión rehecha y "
          f"correcta · {len(SIN_CONVERSION_CONDICIONALES)} declarados sin conversión")
    return fallos


if __name__ == "__main__":
    fs = auditar() + auditar_recomendaciones() + auditar_condicionales()
    if fs:
        print(f"\n❌ {len(fs)} problemas:")
        for f in fs[:60]:
            print("  -", f)
        if len(fs) > 60:
            print(f"  ... y {len(fs)-60} más")
        sys.exit(1)
    print("Discrepancias: 0")
    sys.exit(0)
