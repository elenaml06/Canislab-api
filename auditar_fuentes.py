# -*- coding: utf-8 -*-
"""NINGUNA FUENTE DECIDE UNA CIFRA SIN ESTAR DECLARADA.

⚠️ POR QUE EXISTE (11 de septiembre de 2026, de noche). Elena, despues de que
se cerrara Fascetti: «tienes que seguir leyendo todo lo que no este cerrado
fuente a fuente».

Al medirlo salio que la pregunta estaba mal planteada por mi parte, y el numero
lo dice solo: el repo tenia contador para CUATRO fuentes -- FEDIAF, SACN5, NRC
2006 y Fascetti -- y hay ONCE MAS que deciden cifras que el motor aplica y no
tenian ninguno. O sea que «cerrado fuente a fuente» era verdad de cuatro y
nadie podia ver que de las otras once no se sabia nada.

Y lo peor no es el numero, es la forma: casi todas esas once se buscaron para
CONFIRMAR UNA CIFRA que ya teniamos -- abrir el PDF, encontrar el numero,
cerrarlo --, que es exactamente leer una FRASE y no un DOCUMENTO. Es el fallo
que costo los ocho ultimos capitulos de Fascetti, con otro disfraz.

LO QUE HACE ESTE AUDITOR, y son tres cosas:

  1. MIDE EN VIVO que fuentes cita cada cifra de los ficheros de datos del
     motor. No lee una lista escrita: cuenta las citas de verdad.
  2. Exige que cada fuente que aparezca este DECLARADA en
     `fuentes_del_motor.json` con su estado. Una fuente nueva que entre por la
     puerta de atras -- alguien anade una ficha citando un articulo -- hace
     fallar esto el mismo dia.
  3. Y al reves: una fuente declarada que ya no cita nadie se dice tambien,
     porque un inventario con filas muertas deja de leerse.

LO QUE **NO** HACE, escrito para que nadie lo lea como mas de lo que es: NO
dice que las once esten leidas. Dice que estan DECLARADAS y con que estado. El
estado `verificada_la_cifra` es un rojo suave y significa literalmente «se
confirmo el numero, no se leyo el documento». Subirlas a `leida_entera` es
trabajo de lectura, no de codigo, y es lo que queda.
"""
import io
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
INVENTARIO = os.path.join(RAIZ, "fuentes_del_motor.json")

# Los ficheros de datos donde vive una cifra con su procedencia escrita.
FICHEROS = [
    "patologias.json", "recomendaciones_libro.json", "requisitos_condicionales.json",
    "requerimientos_v2_final.json", "alimentos_v3_final.json",
    "limites_legales_ue_2020_354.json", "fediaf_conversiones_vitaminas.json",
    "sacn5_fuentes_de_minerales.json",
]

# Los campos donde una ficha dice de donde sale lo que dice. Son varios porque
# el catalogo separa la procedencia por nutriente (la taurina de un alimento no
# sale de la misma fuente que su calcio), que es el patron de `purinas_fuente`.
CAMPOS = ("fuente", "purinas_fuente", "taurina_fuente", "lcarnitina_fuente",
          "fuente_epa_dha")

# Como se reconoce cada fuente dentro de una cita. ⚠️ Son expresiones y no
# nombres exactos porque una misma fuente se escribe de varias formas en el
# repo («Kober» y «Köber», «SACN5» y «Small Animal Clinical Nutrition»), y
# exigir una sola grafia dejaria fuera citas de verdad.
COMO_SE_LLAMAN = {
    "FEDIAF": r"FEDIAF",
    "SACN5": r"SACN5|Small Animal Clinical Nutrition",
    "NRC2006": r"\bNRC\b",
    "Fascetti": r"Fascetti",
    "Spitze_2003": r"Spitze",
    "Kober_2017": r"K(ö|o)ber",
    "Dobenecker_Hofmann": r"Dobenecker|Hofmann",
    "Today_s_Veterinary_Practice": r"Veterinary Practice",
    "Reglamento_UE_2020_354": r"2020/354|Reglamento \(UE\)",
    "ACVIM": r"ACVIM",
    "IRIS": r"\bIRIS\b",
    "WSAVA": r"WSAVA",
    "Ettinger": r"Ettinger",
    "Merck": r"Merck",
    "Purina": r"Purina",
}

ESTADOS = {"leida_entera", "verificada_la_cifra", "no_esta_en_el_repo", "inventariada"}


def citas_vivas():
    """{fuente: cuantas cifras la citan}, contado de los ficheros de verdad."""
    patron = re.compile(
        r'"(?:' + "|".join(CAMPOS) + r')"\s*:\s*"([^"]{5,900})"')
    cuenta = {}
    for fichero in FICHEROS:
        ruta = os.path.join(RAIZ, fichero)
        if not os.path.exists(ruta):
            continue
        texto = io.open(ruta, encoding="utf-8").read()
        for m in patron.finditer(texto):
            cita = m.group(1)
            for nombre, rx in COMO_SE_LLAMAN.items():
                if re.search(rx, cita, re.I):
                    cuenta[nombre] = cuenta.get(nombre, 0) + 1
    return cuenta


def auditar():
    problemas = []
    if not os.path.exists(INVENTARIO):
        print("  ❌ falta fuentes_del_motor.json")
        print("\nDiscrepancias: 1")
        return ["falta el inventario"]
    inv = json.load(io.open(INVENTARIO, encoding="utf-8"))["fuentes"]
    vivas = citas_vivas()

    for nombre, cuantas in sorted(vivas.items(), key=lambda x: -x[1]):
        if nombre not in inv:
            problemas.append(
                f"«{nombre}» decide {cuantas} cifra(s) que el motor aplica y NO esta declarada "
                f"en fuentes_del_motor.json. Una fuente que entra por la puerta de atras es una "
                f"cifra de la que nadie sabe si se ha leido")
            continue
        estado = inv[nombre].get("estado")
        if estado not in ESTADOS:
            problemas.append(f"«{nombre}» declara el estado «{estado}», que no es ninguno de "
                             f"{sorted(ESTADOS)}")
        # ⚠️ El recuento declarado se compara EXACTO cuando esta escrito. Si
        # alguien anade diez fichas citando una fuente, el numero se mueve y hay
        # que volver a mirarla -- que es justo lo que se quiere.
        decl = inv[nombre].get("citas_vivas")
        if decl is not None and decl != cuantas:
            problemas.append(f"«{nombre}» declara {decl} citas y hay {cuantas}. O han entrado "
                             f"cifras nuevas de esa fuente, o han salido: en los dos casos hay "
                             f"que volver a mirarla")

    for nombre, ficha in sorted(inv.items()):
        if nombre not in vivas and ficha.get("citas_vivas"):
            problemas.append(f"«{nombre}» esta declarada con {ficha['citas_vivas']} citas y hoy "
                             f"no la cita ninguna cifra. Un inventario con filas muertas deja "
                             f"de leerse")

    por_estado = {}
    for ficha in inv.values():
        por_estado[ficha.get("estado")] = por_estado.get(ficha.get("estado"), 0) + 1
    print(f"  {len(inv)} fuentes declaradas · {sum(vivas.values())} citas vivas · "
          + " · ".join(f"{v} {k}" for k, v in sorted(por_estado.items())))
    for nombre, cuantas in sorted(vivas.items(), key=lambda x: -x[1]):
        estado = (inv.get(nombre) or {}).get("estado", "SIN DECLARAR")
        marca = "  " if estado in ("leida_entera", "inventariada") else "⚠️"
        print(f"   {marca} {nombre:28} {cuantas:4} citas   {estado}")
    for p in problemas:
        print(f"  ❌ {p}")
    print(f"\nDiscrepancias: {len(problemas)}")
    return problemas


if __name__ == "__main__":
    sys.exit(1 if auditar() else 0)
