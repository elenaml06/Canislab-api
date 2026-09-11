# -*- coding: utf-8 -*-
"""
CANISLAB — EL CONTADOR DE FASCETTI & DELANEY, «Applied Veterinary Clinical
Nutrition», 2ª ed.

⚠️ POR QUE EXISTE (11 de septiembre de 2026). Elena: «termina de leer todas las
fuentes, y por leer me refiero a todos los pasos que tienes de verificar las
tablas, verificar los párrafos que no se mezclen, leer toda la información y
sacar toda la información bien, y apuntar y aplicar todo lo necesario».

Fascetti estaba EXTRAIDO y NO LEIDO. Sus 21 capitulos llevaban semanas en el repo
de fuentes, se le citaba en cuatro sitios del motor (el 1,1 % de calcio del
cachorro de raza grande sale de su cap.10) y **no habia ningun sitio donde se
pudiera comprobar que se hubiera leido**. Exactamente el agujero que tenian
FEDIAF antes del 9 de septiembre y SACN5 antes del 10.

QUE CUENTA, Y POR QUE EL MISMO FILTRO QUE SACN5. Se importa `extraer` de
`leer_sacn5.py` a proposito: **un filtro, una definicion**. Dos filtros parecidos
en dos ficheros son dos filtros que se separan, y entonces «elemento
nutricional» significa una cosa en un libro y otra en el de al lado, sin que
nadie lo vea. Si el filtro cambia, cambia para los dos y los dos recuentos se
mueven a la vez, que es justo lo que hace falta para que un numero clavado
signifique algo.

LOS DOS CONTADORES, que no miden lo mismo:
  · `pendientes_declarados`  — FRASES del filtro nutricional sin veredicto.
  · `capitulos_leidos_declarados` — CAPITULOS leidos de principio a fin.
Hacen falta los dos porque el filtro descarta el 96 % de las frases del libro:
resolver los 657 elementos dejaria 17.537 frases sin abrir.

    python3 leer_fascetti.py
"""
import glob
import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
from leer_sacn5 import extraer  # noqa: E402  — un filtro, una definicion

LECTURAS = os.path.join(RAIZ, "lecturas_fascetti.json")
RUTAS = [os.environ.get("RUTA_FASCETTI") or "",
         os.path.join(RAIZ, "..", "canislab-fuentes", "fascetti"),
         os.path.join(RAIZ, "fuentes", "fascetti")]


def carpeta():
    for r in RUTAS:
        if r and os.path.isdir(r) and glob.glob(os.path.join(r, "cap*.txt")):
            return r
    return None


def capitulos():
    c = carpeta()
    return sorted(glob.glob(os.path.join(c, "cap*.txt"))) if c else []


def _cargar():
    if os.path.exists(LECTURAS):
        return json.load(open(LECTURAS, encoding="utf-8"))
    return {"_meta": {}, "capitulos": {}}


def auditar():
    datos = _cargar()
    fallos = []
    if not capitulos():
        print("  (no está el texto de Fascetti: no se puede contar)")
        return fallos
    total = con_veredicto = descartadas = 0
    leidos = 0
    for ruta in capitulos():
        nombre = os.path.basename(ruta)[:-4]
        items, _desc = extraer(ruta, con_descartadas=True)
        descartadas += _desc
        ficha = (datos.get("capitulos") or {}).get(nombre) or {}
        ver = ficha.get("veredictos") or {}
        total += len(items)
        con_veredicto += sum(1 for k in items if ver.get(k))
        sobra = [k for k in ver if k not in items]
        if sobra:
            fallos.append(f"Fascetti/{nombre}: {len(sobra)} veredictos ya no corresponden a nada "
                          f"del texto ({sobra[0][:70]}...). O cambió el filtro o cambió el texto")
        # ⚠️ «Leido entero» se declara con el NUMERO DE LINEAS del .txt y se
        # rehace aqui: si el texto se vuelve a extraer y cambia de tamaño, lo que
        # se leyo ya no es lo que hay. Es la misma regla que en SACN5.
        li = ficha.get("lectura_integra") or {}
        if li:
            n = sum(1 for _ in open(ruta, encoding="utf-8", errors="ignore"))
            if li.get("lineas") != n:
                fallos.append(f"Fascetti/{nombre}: la lectura íntegra declara {li.get('lineas')} "
                              f"líneas y el .txt tiene {n}. O se declaró mal o el texto se ha "
                              f"vuelto a extraer -- y entonces hay que releerlo")
            else:
                leidos += 1
    pend = total - con_veredicto
    print(f"  {len(capitulos())} capítulos · {total} elementos nutricionales · "
          f"{con_veredicto} con veredicto · {pend} pendientes")
    print(f"  {descartadas} frases descartadas por el filtro nutricional "
          f"(de {total + descartadas} frases del libro)")
    print(f"  {leidos} de {len(capitulos())} capítulos LEÍDOS ENTEROS")
    m = datos.get("_meta") or {}
    for clave, vivo, etq in (("total_declarado", total, "elementos"),
                             ("pendientes_declarados", pend, "pendientes"),
                             ("descartadas_declaradas", descartadas, "descartadas"),
                             ("capitulos_leidos_declarados", leidos, "capítulos leídos")):
        decl = m.get(clave)
        if decl is not None and decl != vivo:
            fallos.append(f"Fascetti: hay {vivo} {etq} y el fichero declara {decl}. Este número "
                          f"se mueve SOLO cuando alguien lee, y en el mismo commit")
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
