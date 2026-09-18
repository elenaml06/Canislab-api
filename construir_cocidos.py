#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Las fichas COCIDAS del catálogo, construidas desde las fuentes.

⚠️ POR QUÉ EXISTE (18 de septiembre de 2026). El modo cocinado salió con ONCE
fichas escritas a mano contra los 105 alimentos accesibles del catálogo crudo.
Elena: «hay que mirar TODOS los alimentos, porque las verduras, toda la
proteína, el pollo, todo eso se va a dar distinto. Tienes que tener un catálogo
de alimentos igual de rico que el que tenemos ahora, pero para alimentos
cocinados». Once fichas no son un catálogo: son una muestra.

⚠️ Y NO ESCRIBE NI UNA CIFRA DE NUTRIENTE. Eso es a propósito y es la parte
importante: este script solo decide QUÉ FILA de qué fuente describe el mismo
alimento cocinado, y deja la ficha con su `fuentes_id` apuntando ahí. Los
números los pone `auditar_composicion.py --instantanea` y `--cerrar`, que es la
maquinaria que ya está auditada y que deja la procedencia celda a celda. Un
segundo rellenador sería una segunda forma de equivocarse.

LAS TRES REGLAS PARA ELEGIR LA FILA, y las tres nacen de un fallo medido:

1. **El ancla.** La fila cruda que YA está verificada manda: la cocida tiene que
   llevar todas sus palabras identificativas, y se compara contra el ancla DE SU
   PROPIA FUENTE. Sin esto el barrido proponía «Tapioca» para el apio, sepia
   para el bacalao, ciervo para el conejo y foie gras para el hígado de pato.

2. **La composición.** El nombre no basta: «Foie, canard» está dentro de «Foie
   GRAS, canard», y ahí la grasa pasa de 16 a 82 g por 100 g de materia seca.
   Se compara proteína y grasa POR MATERIA SECA contra la ficha cruda, con
   suelos —en una verdura la grasa va de 0,175 a 0,8 g, así que dos décimas
   disparan un 60 %— y con el guardia de imposibilidad aritmética, que es el que
   cazó el pulpo hervido de BEDCA (14,3 g de proteína y grasa dentro de 13,1 de
   materia seca).

3. **Si falla, se baja a la siguiente**, no se deja al alimento sin ficha. Así
   la gallina pasó de una fila con «giblets and neck» a la limpia y la judía
   verde de los 6,79 g de grasa de BEDCA a la de USDA.

⚠️ LO QUE **NO** SE HACE, y es una decisión medida: no se «corrige» una fila de
horno para fingir que es hervida. Medido sobre el mismo pez cocinado de varias
formas y por 100 g de materia seca, lo que decide la ración —proteína y por
tanto las kcal— apenas se mueve (bacalao 92,11 al vapor contra 92,92 al horno,
un 1 %); lo que cambia de verdad es el AGUA, y el agua la publica la fuente. Así
que donde solo hay fila de horno o de plancha, la ficha se construye con ESA
fila y **dice cómo se cocina ese alimento** — la sardina a la plancha y el pavo
al horno, que además es lo que hace la gente. Cero cifras inventadas.
"""
import collections
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CATALOGO = os.path.join(AQUI, "alimentos_v3_final.json")
PROPUESTA = os.path.join(AQUI, "cocidos_propuesta.json")

# ⚠️ LA FRUTA NO SE COCINA, y es lo único de esta lista que se escribe a mano.
# Elena, 18 de septiembre: «aunque la fruta no se cocina, o sea que la fruta...
# nada, la fruta, olvídalo. Pues para la verdura también». En modo cocinado la
# fruta se queda CRUDA tal cual, que es lo que ya permite el modo para lo
# vegetal. No se deriva del catálogo porque no hay ningún campo que diga si algo
# es fruta -- y una lista escrita a mano con su motivo es mejor que una
# derivación que adivina.
FRUTA = {
    "Albaricoque", "Arándano", "Coco fresco", "Dátil", "Frambuesa", "Fresa",
    "Mandarina", "Mango", "Manzana", "Melón", "Naranja", "Pera", "Piña",
    "Plátano", "Sandía",
}

# Cómo se dice «cocido» de cada cosa. El femenino no se adivina bien por la
# terminación —«la carne», «el filete»— así que las excepciones van escritas.
FEMENINO = {"Gallina", "Molleja", "Lengua", "Ternera", "Trucha", "Sepia",
            "Merluza", "Caballa", "Sardina", "Acelga", "Espinaca", "Coliflor",
            "Calabaza", "Zanahoria", "Judía", "Col", "Coles", "Alcachofa",
            "Perca", "Acelga", "Berenjena", "Calabaza"}


def nombre_cocido(nombre):
    """«Pollo muslo sin piel» -> «Pollo muslo sin piel cocido»."""
    primera = nombre.split()[0].strip("(,")
    return f"{nombre} {'cocida' if primera in FEMENINO else 'cocido'}"


def main():
    if not os.path.exists(PROPUESTA):
        print(f"Falta {os.path.basename(PROPUESTA)}. Se genera con buscar_cocidos.py.")
        return 2
    prop = json.load(open(PROPUESTA, encoding="utf-8"))
    catalogo = json.load(open(CATALOGO, encoding="utf-8"),
                         object_pairs_hook=collections.OrderedDict)
    por_nombre = {f["nombre"]: f for f in catalogo}

    nuevas, saltadas = [], []
    for nombre, d in sorted(prop.get("elegidas", {}).items()):
        cruda = por_nombre.get(nombre)
        if cruda is None:
            saltadas.append((nombre, "ya no está en el catálogo"))
            continue
        if nombre in FRUTA:
            saltadas.append((nombre, "es fruta: no se cocina"))
            continue
        nuevo = nombre_cocido(nombre)
        if nuevo in por_nombre:
            saltadas.append((nombre, "ya existe su ficha cocida"))
            continue

        ficha = collections.OrderedDict()
        ficha["nombre"] = nuevo
        ficha["categoria"] = cruda["categoria"]
        if cruda.get("especie"):
            ficha["especie"] = cruda["especie"]
        ficha["preparacion"] = "cocido"
        ficha["fuentes_id"] = collections.OrderedDict(
            sorted((fu, str(i)) for fu, i in d["ids"].items()))
        # ⚠️ LA FICHA NACE CON TODAS SUS CELDAS DECLARADAS COMO HUECO, y ésa es
        # la forma de usar `auditar_composicion.py --cerrar` sin escribir un
        # segundo rellenador. Ese script CORRIGE un catálogo, no crea fichas de
        # cero: su condición es `if clave not in nut: continue`, y es un guardia
        # deliberado —rellenar claves que nadie ha declarado sería inventar la
        # forma de la ficha—. Así que aquí se declara la forma, con las MISMAS
        # claves que tiene su ficha cruda hermana, y se dice que todas están
        # vacías. Él las va cerrando una a una con su procedencia, y las que
        # ninguna fuente publique se quedan en hueco DECLARADO, que es la
        # verdad.
        ficha["nutrientes"] = collections.OrderedDict(
            (clave, 0) for clave in (cruda.get("nutrientes") or {}))
        ficha["sin_dato"] = sorted(cruda.get("nutrientes") or {})
        # ⚠️ LA BASE SE DECLARA, que es lo que permite rehacerla contra la fila
        # de la fuente -- y lo que separa a estas fichas del Boniato, que se da
        # cocido y se pesa CRUDO porque su composición sale de la fila cruda.
        ficha["se_pesa"] = "ya cocido"
        ficha["se_pesa_por_que"] = (
            f"Su composición sale de una fila de alimento YA COCINADO "
            f"({d['fuente']}:{d['id']} «{d['fila']}»), así que los gramos del menú son "
            f"de producto cocinado.")
        ficha["aviso_al_comprar"] = (
            f"Se compra CRUDO y se da COCIDO: {d['como']}, sin sal. "
            f"⚠️ Los gramos del menú son de producto YA COCIDO — pésalo DESPUÉS de "
            f"cocinarlo, no antes.")
        # ⚠️ LAS CONDICIONES LEGALES SE HEREDAN ENTERAS. El `Cerebro de ternera`
        # solo vale de animal de menos de 12 meses (Reglamento CE 999/2001,
        # material especificado de riesgo), y cocinarlo NO cambia eso. Una ficha
        # cocida que perdiera la condición afirmaría que vale cualquier encéfalo
        # de bovino. Lo vigila el BLOQUE 51.
        if "LEY" in (cruda.get("nota_datos") or "") or "LEGAL" in (cruda.get("nota_datos") or ""):
            ficha["nota_datos"] = cruda["nota_datos"]
            ficha["aviso_al_comprar"] = (
                (cruda.get("aviso_al_comprar") or "") + " || " + ficha["aviso_al_comprar"]).strip(" |")
        nuevas.append(ficha)

    print(f"  fichas cocidas nuevas: {len(nuevas)}")
    for n, por in saltadas:
        print(f"    saltada · {n}: {por}")
    if "--escribir" not in sys.argv:
        print("\n  (en seco: no se ha escrito nada. Con --escribir se añaden al catálogo)")
        for f in nuevas:
            print(f"    {f['nombre']:38} {f['fuentes_id']}")
        return 0

    catalogo.extend(nuevas)
    with open(CATALOGO, "w", encoding="utf-8") as fh:
        json.dump(catalogo, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"\n  catálogo: {len(catalogo)} fichas")
    print("  AHORA: auditar_composicion.py --instantanea  y luego  --cerrar")
    return 0


if __name__ == "__main__":
    sys.exit(main())
