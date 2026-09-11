# -*- coding: utf-8 -*-
"""NO SE PUEDE APLICAR UNA CIFRA DE UN CAPITULO QUE NO ESTA CERRADO.

⚠️ POR QUE EXISTE (11 de septiembre de 2026, de noche). Elena, despues de que
por enesima vez apareciera algo «que se habia pasado» en un capitulo dado por
leido:

    «no puede ser que te tengas que leer un capitulo 18 veces y que siempre
     sigan saliendo cosas que se te han pasado, que no has apuntado, que no has
     aplicado. [...] lo que quiero es que propongas una solucion que no falle»

Y la solucion no podia ser leer con mas cuidado, porque eso es exactamente lo
que se dijo las veces anteriores. El diagnostico, MEDIDO y no supuesto, es otro:

    El repo ya CONTABA los elementos sin veredicto de cada capitulo
    (`leer_fascetti.py`, `leer_sacn5.py`, `leer_fuente.py`), y el contador
    funcionaba: decia 213 pendientes. Lo que NO habia era nada que impidiera
    APLICAR una cifra sacada de un capitulo con pendientes.

O sea: se leia una FRASE, no un CAPITULO. Y de ahi salen, con la misma forma,
los tres fallos de esta semana:

  · La frase del cap.14 de Fascetti trae TRES cifras -- el ratio LA:ALA, el
    techo de linoleico de 16,3 y el techo de EPA+DHA de 2,8 --, se aplicaron
    DOS y la tercera no la vio nadie hasta releer el capitulo entero. Y la
    tercera es la unica que aprieta: 5 de los 216 menus del catalogo se pasan.
  · El 8 % de fibra del cap.11 se aplico a `enteropatia_cronica` y resulto ser
    del cuadro de GASTROENTERITIS AGUDA, dos parrafos mas arriba. Se retiro el
    mismo dia, al abrir el contexto en vez de la frase.
  · La cita F-6 decia «depending on the size of the litter» y el libro dice
    «of the BITCH». Cambiaba la conclusion.

Los tres son el mismo fallo: coger la frase sin cerrar el capitulo.

LA REGLA QUE IMPONE ESTE AUDITOR, y es una sola:

    Si una cifra que el motor APLICA cita el capitulo N de una fuente,
    ese capitulo tiene que tener CERO elementos sin veredicto.

Lo que garantiza y lo que no. NO garantiza que el veredicto sea el correcto --
eso lo miran `auditar_citas.py` (que la cita diga lo que dice la fuente) y
`auditar_conversiones.py` (que la cuenta se rehaga). Lo que SI garantiza es que
nadie pueda volver a aplicar media frase de un capitulo que no se ha terminado
de leer, que es de donde salieron los tres.

Y fuerza el orden que ya estaba escrito en la cabecera de `LECTURA_SACN5.md` y
que yo me salte con Fascetti: leer el capitulo entero, dar veredicto a todo, y
aplicar solo al final.
"""
import io
import json
import os
import re
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

# Los ficheros donde viven las cifras que el motor APLICA.
FICHEROS_CON_CIFRAS = [
    "patologias.json",
    "recomendaciones_libro.json",
    "requisitos_condicionales.json",
]

# Como se llama cada fuente dentro de una cita, y donde vive su registro de
# lectura. La clave es lo que hay que buscar en el texto.
FUENTES = {
    "Fascetti": {"registro": "lecturas_fascetti.json", "lector": "leer_fascetti"},
    "SACN5": {"registro": "lecturas_sacn5.json", "lector": "leer_sacn5"},
}

# ⚠️ «cap.10» no siempre es del libro que aparece primero en la frase. Hay citas
# que nombran los dos: «Fascetti cap.10, dentro del 0,8-1,2 % de la Tabla 33-5
# de SACN5». Ahi el 33 es de SACN5 y el 10 de Fascetti, y atribuirlos a ojo
# acusaria a Fascetti de tener sin cerrar un capitulo que no es suyo. Se
# resuelve recorriendo la cita de izquierda a derecha y quedandose con el ULTIMO
# libro nombrado antes de cada «cap.N».
_NOMBRE_O_CAP = re.compile(r"(Fascetti|SACN5|FEDIAF|NRC)|cap\.?\s*(\d{1,2})", re.I)
# «el cap.40 DE SACN5»: el libro pegado justo detras del numero manda sobre el
# que venia antes en la frase.
_DE_QUE_LIBRO = re.compile(r"^\s*de\s+(Fascetti|SACN5|FEDIAF|NRC)", re.I)


def _normaliza(nombre):
    n = (nombre or "").strip()
    if n.lower() == "fascetti":
        return "Fascetti"
    if n.upper() == "SACN5":
        return "SACN5"
    return n.upper()


def capitulos_citados(texto):
    """{(fuente, 'capNN')} de una cita, atribuyendo cada capitulo a su libro."""
    salida, libro = set(), None
    for m in _NOMBRE_O_CAP.finditer(texto or ""):
        if m.group(1):
            libro = _normaliza(m.group(1))
        elif m.group(2):
            # ⚠️ Y EN CASTELLANO EL LIBRO VA DETRAS: «el cap.40 de SACN5». La
            # regla de «el ultimo libro nombrado» se lo atribuia a Fascetti, que
            # solo tiene 21 capitulos, y salia un aviso de un capitulo que no
            # existe. Asi que primero se mira si el libro viene DESPUES.
            cola = texto[m.end():m.end() + 30]
            detras = _DE_QUE_LIBRO.search(cola)
            suyo = _normaliza(detras.group(1)) if detras else libro
            if suyo in FUENTES:
                salida.add((suyo, int(m.group(2))))
    return salida


# ⚠️ LOS DOS LIBROS NUMERAN SUS FICHEROS DISTINTO, y darlo por hecho hacia que
# 17 cifras de SACN5 salieran como «capitulo que no aparece en el registro».
# Fascetti va con cero delante (`cap05.txt`) y SACN5 no (`cap5.txt`); y ademas
# SACN5 parte los capitulos largos en trozos (`cap33_1.txt`, `cap37_1.txt`), asi
# que un capitulo citado puede vivir en varios ficheros y los pendientes hay que
# SUMARLOS. Contar solo el primer trozo daria cerrado un capitulo a medio leer,
# que es justo lo que este auditor viene a impedir.
_NUMERO_DE_CAP = re.compile(r"^cap0*(\d{1,2})(?:_\d+)?$")


def _numero(nombre_de_fichero):
    m = _NUMERO_DE_CAP.match(nombre_de_fichero)
    return int(m.group(1)) if m else None


def _recorrer(nodo, camino=()):
    """Cada cifra con su `fuente`/`cita` y donde vive, para poder decirlo."""
    if isinstance(nodo, dict):
        # Una cifra es un dict que trae `valor` y `fuente`. Las escritas y NO
        # aplicadas se saltan a proposito: para eso existe la marca, y exigirle
        # capitulo cerrado a algo que el solver no usa seria pedir trabajo por
        # una cifra que hoy no come ningun perro.
        if "fuente" in nodo and nodo.get("aplicado_por_el_solver") is not False:
            textos = [str(nodo.get("fuente") or "")]
            conv = nodo.get("conversion") or {}
            if isinstance(conv, dict):
                textos.append(str(conv.get("cita") or ""))
            yield ".".join(camino), " || ".join(textos)
        for k, v in nodo.items():
            if k in ("limites_escritos_que_el_solver_no_aplica",):
                continue
            yield from _recorrer(v, camino + (str(k),))
    elif isinstance(nodo, list):
        for i, v in enumerate(nodo):
            yield from _recorrer(v, camino + (str(i),))


def pendientes_por_capitulo(fuente):
    """{'capNN': cuantos elementos siguen sin veredicto} de esa fuente."""
    info = FUENTES[fuente]
    ruta = os.path.join(RAIZ, info["registro"])
    if not os.path.exists(ruta):
        return None, f"no existe {info['registro']}"
    try:
        sys.path.insert(0, RAIZ)
        lector = __import__(info["lector"])
    except Exception as e:                      # pragma: no cover
        return None, f"no se puede importar {info['lector']}: {e}"
    datos = json.load(io.open(ruta, encoding="utf-8"))
    salida = {}
    for archivo in lector.capitulos():
        cap = os.path.basename(archivo).replace(".txt", "")
        n = _numero(cap)
        if n is None:
            continue
        elementos = lector.extraer(archivo)
        ya = set((datos["capitulos"].get(cap) or {}).get("veredictos") or {})
        sin = sum(1 for e in elementos if e not in ya)
        # Se SUMA: un capitulo partido en trozos esta cerrado solo si lo estan
        # todos sus trozos.
        salida[n] = salida.get(n, 0) + sin
    return salida, None


def auditar():
    problemas, avisos = [], []
    pendientes = {}
    for fuente in FUENTES:
        p, err = pendientes_por_capitulo(fuente)
        if err:
            avisos.append(f"{fuente}: {err}")
        pendientes[fuente] = p or {}

    cifras = 0
    capitulos_usados = {}
    for fichero in FICHEROS_CON_CIFRAS:
        ruta = os.path.join(RAIZ, fichero)
        if not os.path.exists(ruta):
            avisos.append(f"no existe {fichero}")
            continue
        datos = json.load(io.open(ruta, encoding="utf-8"))
        for donde, texto in _recorrer(datos):
            cifras += 1
            for fuente, cap in capitulos_citados(texto):
                capitulos_usados.setdefault((fuente, cap), []).append(f"{fichero}:{donde}")

    for (fuente, cap), quienes in sorted(capitulos_usados.items()):
        etiqueta = f"{fuente} cap.{cap}"
        sin = pendientes.get(fuente, {}).get(cap)
        if sin is None:
            avisos.append(f"{etiqueta}: citado por {len(quienes)} cifras y no aparece en el "
                          f"registro de lectura")
        elif sin > 0:
            problemas.append(
                f"{etiqueta}: el motor APLICA {len(quienes)} cifra(s) de este capitulo y le "
                f"quedan {sin} elementos SIN VEREDICTO. Se ha aplicado una frase de un capitulo "
                f"que no esta cerrado, que es de donde salieron los tres fallos de esta semana. "
                f"Primero se cierra el capitulo, despues se aplica. Cifras: "
                f"{', '.join(quienes[:4])}{'...' if len(quienes) > 4 else ''}")

    print(f"  {cifras} cifras aplicadas · {len(capitulos_usados)} capitulos citados · "
          f"{len(problemas)} sin cerrar")
    for a in avisos:
        print(f"  [aviso] {a}")
    for p in problemas:
        print(f"  ❌ {p}")
    print(f"\nDiscrepancias: {len(problemas)}")
    return problemas


if __name__ == "__main__":
    sys.exit(1 if auditar() else 0)
