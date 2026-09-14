# -*- coding: utf-8 -*-
"""LAS DIEZ FICHAS DE HUESO, REHECHAS CONTRA LA TABLA 1 DE KÖBER 2017.

⚠️ POR QUE EXISTE, y es un fallo real encontrado el 11 de septiembre de 2026 de
noche, al leer entera una fuente que llevaba desde agosto «verificada»:

    Tres fichas del catalogo tenian el calcio y el fosforo DIEZ VECES POR
    DEBAJO de lo que midio el estudio. La peor, «Pecho de ternera con hueso»,
    estaba en 93 de los 216 menus del catalogo, y con el valor real de la
    fuente 55 de esos menus SE PASAN del maximo de calcio de FEDIAF -- el peor,
    un cachorro en crecimiento con 9408 mg/1000 kcal contra un maximo de 4500.
    El semaforo los daba verdes porque medía el numero equivocado.

Y las dos razones por las que sobrevivio meses, que son las que este auditor
viene a tapar:

  1. LA TABLA MEZCLA DOS SISTEMAS DE UNIDADES Y SU CABECERA SOLO DECLARA UNO.
     Dice «(g/kg wet weight)», y es verdad del calcio y del fosforo; pero la
     materia seca, la proteina, la grasa y las cenizas van en POR CIENTO. Una
     materia seca de «48.0» leida como g/kg serian un 4,8 %, que es absurdo
     para un hueso. Con dos unidades en una tabla, un factor 10 tiene donde
     esconderse.
  2. EL RATIO Ca:P SOBREVIVE AL ERROR. 427/199 da 2,15 exactamente igual que
     4270/1990. La comprobacion que se hizo en su dia fue precisamente esa --
     «ratio Ca:P real 2,15, coincide con el 2,1:1 que da el propio estudio» --
     y no podia ver nada. Una comprobacion de PROPORCION no caza un error de
     ESCALA.

Es la misma familia que `auditar_transcripcion_fediaf.py`: entre la fuente y el
catalogo hay un paso a mano, y lo que no se rehace no se audita.

⚠️ Y UNA FICHA NO SALE DE UNA FILA SINO DE DOS, a proposito: «Carcasa de pollo»
es la media 50/50 de «Chicken carcass» y «Chicken dorsum», porque en Espana
carcasa y espinazo de pollo son la misma pieza de compra y el estudio las midio
por separado. Va declarado abajo con su motivo, para que promediar no pueda ser
una forma de tapar un numero que no cuadra.
"""
import io
import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
CATALOGO = os.path.join(RAIZ, "alimentos_v3_final.json")

# ── LA TABLA 1, TRANSCRITA TAL CUAL DEL TEXTO DE LA FUENTE ─────────────────
#
# Köber N, Schmitt S, Kienzle E, Dobenecker B (2017), «Bones and gristle as a
# source of calcium in BARF-rations», 21st ESVCN Congress, Cirencester.
#
# Orden de las columnas, como las imprime el estudio:
#   Ca [g/kg fresco] · P [g/kg fresco] · DM [%] · CP [%] · CF [%] · CA [%]
#
# ⚠️ LAS QUINCE FILAS, no solo las diez que usa el catalogo. Las cinco que
# sobran se dejan porque el dia que alguien anada una ficha de esternon de
# vacuno o de pierna de cordero, su cifra ya esta aqui y el auditor la caza.
TABLA_1 = {
    "Calf neck bones":     (73.1, 33.8, 48.0, 20.3,  7.5, 19.7),
    "Calf breastbone":     (42.7, 19.9, 57.3, 18.8, 30.1, 11.9),
    "Cattle breastbone":   (35.1, 16.8, 46.9, 17.9, 14.7, 10.3),
    "Lamb leg":            (27.1, 15.5, 49.6, 22.9, 17.6,  9.3),
    "Chicken dorsum":      (18.2, 10.5, 42.2, 16.2, 18.9,  5.0),
    "Rabbit carcass":      (18.1, 10.1, 34.3, 18.7,  9.3,  6.0),
    "Lamb rips":           (16.9, 10.1, 36.9, 19.7, 11.9,  5.6),
    "Duck carcass":        (16.4,  8.9, 39.1, 15.4, 18.7,  4.9),
    "Turkey neck":         (16.1,  8.4, 31.2, 19.6,  6.0,  5.3),
    "Chicken carcass":     (14.7,  8.3, 43.2, 16.4, 20.0,  4.6),
    "Duck neck":           (12.5,  6.8, 46.2, 12.2, 30.0,  3.5),
    "Rabbit dorsum":       ( 8.6,  5.6, 32.4, 22.9,  6.1,  3.4),
    "Cattle larynges":     ( 6.6,  4.4, 42.2, 21.1, 17.7,  2.9),
    "Cattle scapula":      ( 0.8,  1.0, 38.2, 26.8,  8.1,  1.6),
    "Cattle gristle mix":  ( 0.4,  1.2, 35.4, 19.0, 16.6,  0.8),
}

# Que ficha del catalogo sale de que fila (o de que par de filas).
DE_DONDE_SALE = {
    "Cuello de ternera":          ["Calf neck bones"],
    "Pecho de ternera con hueso": ["Calf breastbone"],
    "Costillas de cordero":       ["Lamb rips"],
    "Espinazo de conejo":         ["Rabbit dorsum"],
    "Carcasa de conejo":          ["Rabbit carcass"],
    "Carcasa de pato":            ["Duck carcass"],
    "Cuello de pato":             ["Duck neck"],
    "Cuello de pavo":             ["Turkey neck"],
    "Laringe de vacuno":          ["Cattle larynges"],
    # ⚠️ DOS FILAS, Y ESTA ESCRITO POR QUE: en Espana «carcasa» y «espinazo» de
    # pollo son la MISMA pieza de compra y el estudio las midio por separado
    # (carcasa Ca 14,7 · espinazo Ca 18,2, un 24 % de diferencia). Se promedian
    # 50/50 para reflejar lo que se compra. Antes habia dos entradas para lo
    # mismo y usar solo «carcasa» infravaloraba el calcio real un 24 %.
    "Carcasa de pollo":           ["Chicken carcass", "Chicken dorsum"],
}

# g/kg de peso fresco -> mg por 100 g, que es la base del catalogo.
A_MG_POR_100G = 100.0


def auditar():
    problemas = []
    if not os.path.exists(CATALOGO):
        print("  ❌ no está alimentos_v3_final.json")
        print("\nDiscrepancias: 1")
        return ["falta el catalogo"]
    crudo = json.load(io.open(CATALOGO, encoding="utf-8"))
    fichas = crudo if isinstance(crudo, dict) else {a["nombre"]: a for a in crudo}

    for nombre, filas in sorted(DE_DONDE_SALE.items()):
        ficha = fichas.get(nombre)
        if ficha is None:
            problemas.append(f"«{nombre}» ha desaparecido del catalogo y salia de la Tabla 1 de "
                             f"Köber ({', '.join(filas)})")
            continue
        if "ber" not in str(ficha.get("fuente") or ""):
            problemas.append(f"«{nombre}» ya no cita a Köber en su `fuente`. O cambio la fuente "
                             f"-- y entonces hay que volver a mirar sus cifras -- o se borro la "
                             f"procedencia")
        nut = ficha.get("nutrientes") or {}
        # La media de las filas de las que sale, columna a columna.
        n = len(filas)
        esperado = [sum(TABLA_1[f][i] for f in filas) / n for i in range(6)]
        for clave, i, factor, unidad in (("calcio", 0, A_MG_POR_100G, "mg/100 g"),
                                         ("fosforo", 1, A_MG_POR_100G, "mg/100 g"),
                                         ("proteina", 3, 1.0, "g/100 g"),
                                         ("grasa", 4, 1.0, "g/100 g")):
            esp = esperado[i] * factor
            real = nut.get(clave)
            if real is None:
                problemas.append(f"«{nombre}» no tiene {clave} y la Tabla 1 la mide")
                continue
            if abs(real - esp) > 0.5:
                extra = ""
                # ⚠️ Se DICE si el error es un factor de diez, porque es el que
                # ya paso y el que la tabla esconde con sus dos unidades.
                if esp and abs(real * 10 - esp) < 0.5:
                    extra = "  ⚠️ ES UN FACTOR 10: el valor esta diez veces POR DEBAJO"
                elif esp and abs(real / 10 - esp) < 0.5:
                    extra = "  ⚠️ ES UN FACTOR 10: el valor esta diez veces POR ENCIMA"
                problemas.append(
                    f"«{nombre}» tiene {clave} = {real} {unidad} y la Tabla 1 de Köber da "
                    f"{esp:.1f} (fila{'s' if n > 1 else ''} {', '.join(filas)}).{extra}")

    print(f"  {len(DE_DONDE_SALE)} fichas del catalogo · {len(TABLA_1)} filas de la Tabla 1 · "
          f"4 columnas rehechas por ficha")
    for p in problemas:
        print(f"  ❌ {p}")
    print(f"\nDiscrepancias: {len(problemas)}")
    return problemas


if __name__ == "__main__":
    sys.exit(1 if auditar() else 0)
