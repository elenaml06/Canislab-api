# -*- coding: utf-8 -*-
"""
CANISLAB — EL CONTADOR DE NRC 2006, «Nutrient Requirements of Dogs and Cats».

⚠️ POR QUE EXISTE (11 de septiembre de 2026). Elena, al contarle yo que NRC
estaba «leido entero» y que lo que faltaba era el contador:

    «lo del NRC que dices que esta leido, pero sin contador, tiene que estar el
     contador, vale? Para todo tiene que haber un contador y tienes que
     asegurarte de que lo has leido bien y que luego el contador lo verifica»

Tiene razon, y es la leccion de este repo entera: **«leido» sin contador es solo
mi palabra.** Ya paso tres veces el mismo dia con FEDIAF, y otra con SACN5, y las
dos veces la afirmacion era sincera y falsa a la vez. `LECTURA_NRC2006.md`
registra la lectura de los 15 capitulos; esto es lo que permite COMPROBARLA.

COMO SE PARTE EN CAPITULOS. El PDF de NRC viene en un solo .txt de 43.556 lineas.
El corte se hace en el patron del libro -- una linea con solo el numero, una
linea en blanco y el titulo en Title Case -- y se declara la linea de inicio de
cada uno, para que si el texto se vuelve a extraer y cambia, salte. El indice y
los dos apendices (desde la linea del «Index») NO se cuentan: son listas de
paginas, no texto nutricional.

EL FILTRO ES EL DE SACN5, importado, no copiado. Un filtro, una definicion: dos
filtros parecidos en dos ficheros son dos filtros que se separan, y entonces
«elemento nutricional» significa una cosa en un libro y otra en el de al lado.

    python3 leer_nrc2006.py
"""
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
from leer_sacn5 import extraer_de_texto  # noqa: E402

LECTURAS = os.path.join(RAIZ, "lecturas_nrc2006.json")
RUTAS = [os.environ.get("RUTA_NRC2006") or "",
         os.path.join(RAIZ, "..", "canislab-fuentes", "NRC2006", "nrc2006.txt"),
         os.path.join(RAIZ, "fuentes", "NRC2006", "nrc2006.txt")]

# El titulo de cada capitulo, para que el fichero de lecturas se lea solo.
TITULOS = {
    1: "Comparative Digestive Physiology of Dogs and Cats",
    2: "Feeding Behavior of Dogs and Cats",
    3: "Energy",
    4: "Carbohydrates and Fiber",
    5: "Fat and Fatty Acids",
    6: "Protein and Amino Acids",
    7: "Minerals",
    8: "Vitamins",
    9: "Water",
    10: "Special Considerations for Laboratory Animals",
    11: "Physical Activity and Environment",
    12: "Diet Formulation and Feed Processing",
    13: "Nutrient Composition of Ingredients",
    14: "Other Food Constituents",
    15: "Nutrient Requirements and Dietary Nutrient Concentrations",
}
_CAB = re.compile(r"^\s*(\d{1,2})\s*$")


def ruta():
    for r in RUTAS:
        if r and os.path.isfile(r):
            return r
    return None


def capitulos():
    """{n: (titulo, texto)} partiendo el .txt por las cabeceras del libro."""
    r = ruta()
    if not r:
        return {}
    lineas = open(r, encoding="utf-8", errors="ignore").read().splitlines()
    # El indice y los apendices no son texto nutricional: son listas de paginas.
    fin_cuerpo = len(lineas)
    for i, l in enumerate(lineas):
        if i > 34000 and l.strip() == "Index":
            fin_cuerpo = i
            break
    inicios = {}
    for i in range(900, fin_cuerpo - 3):
        m = _CAB.fullmatch(lineas[i] or "")
        if not m:
            continue
        n = int(m.group(1))
        if n not in TITULOS or n in inicios:
            continue
        if lineas[i + 1].strip() or not lineas[i + 2].strip():
            continue
        t = lineas[i + 2].strip()
        if re.match(r"^[A-Z][A-Za-z]", t) and len(t) < 60 and not t.isupper():
            inicios[n] = i
    orden = sorted(inicios.items(), key=lambda kv: kv[1])
    fuera = {}
    for j, (n, ini) in enumerate(orden):
        fin = orden[j + 1][1] if j + 1 < len(orden) else fin_cuerpo
        fuera[n] = (TITULOS[n], "\n".join(lineas[ini:fin]), ini, fin - ini)
    return fuera


def _cargar():
    if os.path.exists(LECTURAS):
        return json.load(open(LECTURAS, encoding="utf-8"))
    return {"_meta": {}, "capitulos": {}}


def auditar():
    datos = _cargar()
    fallos = []
    caps = capitulos()
    if not caps:
        print("  (no está el texto de NRC 2006: no se puede contar)")
        return fallos
    if sorted(caps) != sorted(TITULOS):
        fallos.append(f"NRC2006: se han encontrado los capítulos {sorted(caps)} y el libro tiene "
                      f"{sorted(TITULOS)}. O cambió el texto o cambió el cortador, y en los dos "
                      f"casos lo que se leyó ya no es lo que hay")
    total = con_veredicto = descartadas = leidos = 0
    for n in sorted(caps):
        titulo, texto, ini, nlineas = caps[n]
        items, _desc = extraer_de_texto(texto, con_descartadas=True)
        descartadas += _desc
        clave = f"cap{n}"
        ficha = (datos.get("capitulos") or {}).get(clave) or {}
        ver = ficha.get("veredictos") or {}
        total += len(items)
        con_veredicto += sum(1 for k in items if ver.get(k))
        sobra = [k for k in ver if k not in items]
        if sobra:
            fallos.append(f"NRC2006/{clave}: {len(sobra)} veredictos ya no corresponden a nada "
                          f"del texto ({sobra[0][:70]}...). O cambió el filtro o cambió el texto")
        li = ficha.get("lectura_integra") or {}
        if li:
            if li.get("lineas") != nlineas:
                fallos.append(f"NRC2006/{clave}: la lectura íntegra declara {li.get('lineas')} "
                              f"líneas y el capítulo tiene {nlineas}. O se declaró mal o el texto "
                              f"se ha vuelto a extraer -- y entonces hay que releerlo")
            else:
                leidos += 1
    pend = total - con_veredicto
    print(f"  {len(caps)} capítulos · {total} elementos nutricionales · "
          f"{con_veredicto} con veredicto · {pend} pendientes")
    print(f"  {descartadas} frases descartadas por el filtro nutricional "
          f"(de {total + descartadas} frases del libro)")
    print(f"  {leidos} de {len(caps)} capítulos LEÍDOS ENTEROS")
    m = datos.get("_meta") or {}
    for clave, vivo, etq in (("total_declarado", total, "elementos"),
                             ("pendientes_declarados", pend, "pendientes"),
                             ("descartadas_declaradas", descartadas, "descartadas"),
                             ("capitulos_leidos_declarados", leidos, "capítulos leídos")):
        decl = m.get(clave)
        if decl is not None and decl != vivo:
            fallos.append(f"NRC2006: hay {vivo} {etq} y el fichero declara {decl}. Este número se "
                          f"mueve SOLO cuando alguien lee, y en el mismo commit")
    return fallos


if __name__ == "__main__":
    f = auditar()
    print("-" * 60)
    if f:
        print(f"\n{len(f)} PROBLEMAS:\n")
        for x in f[:30]:
            print("  -", x)
        sys.exit(1)
    print("\nDiscrepancias: 0")
