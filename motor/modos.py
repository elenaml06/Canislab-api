# -*- coding: utf-8 -*-
"""
LOS TRES MODOS Y EL RECALCULO.

La idea clave: con el motor nuevo, los tres modos son EL MISMO ALGORITMO.
Lo unico que cambia es COMO se eligen los alimentos; a partir de ahi,
construir -> verificar -> suplementar es identico.

    automatico    los elegimos nosotros
    personalizar  el usuario elige unos y el resto se completa solo
    aprovechar    se parte de lo que tiene en casa y se completa

Con el LP esto eran tres caminos distintos por el codigo, cada uno con sus
reintentos y sus casos raros, y un fallo habia que arreglarlo tres veces.

EL RECALCULO SE ARREGLA SOLO
----------------------------
Al cambiar un ingrediente NO se vuelve a optimizar nada: se sustituye el
nombre dentro de su categoria y se reconstruye con la MISMA plantilla. La
estructura no se mueve. El fallo de "cambio un ingrediente y me quedan 3"
es imposible aqui, y no porque se haya arreglado: porque estructuralmente
no puede pasar. Cada categoria tiene su hueco reservado desde el principio.
"""
import random
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constructor import PILARES
from exclusiones import filtrar as filtrar_exclusiones

# Cuantos alimentos distintos por categoria. Son los mismos topes que ya
# habia en el frontend: maximo 3 proteinas contando el pescado (2 carnes +
# 1 pescado), 2 huesos, 1 viscera, 1 higado, 2-3 verduras.
# RANGOS, no numeros fijos. El motor decide cuantos poner dentro del rango
# segun lo que le falte por cubrir: si con uno llega, uno; si necesita mas
# variedad para tapar un hueco, coge otro.
#
# El numero fijo era demasiado rigido. Una racion puede ser dos carnes y un
# pescado, o un pescado y una carne, o una sola verdura, o una verdura y una
# fruta. Y en visceras no tiene por que haber una sola: puede haber rinon y
# pulmon. Lo unico que no se mueve es que los PILARES esten presentes.
#
# minimo = lo que hace falta para que el pilar exista
# maximo = donde empieza a ser un menu inmanejable en una cocina de verdad
CUANTOS_MIN = {
    "Carne muscular": 1, "Hueso carnoso": 1, "Pescados y mariscos": 0,
    "Vísceras": 1, "Hígado": 1, "Verduras y frutas": 1,
}
CUANTOS_MAX = {
    "Carne muscular": 3, "Hueso carnoso": 2, "Pescados y mariscos": 2,
    "Vísceras": 2, "Hígado": 1, "Verduras y frutas": 3,
}
# PROTEINA TOTAL: la carne y el pescado son lo mismo nutricionalmente, asi
# que lo que se limita es la suma, no cada uno por su lado. Puede ser 2
# carnes + 1 pescado, o 1 carne + 1 pescado, o 3 carnes y ningun pescado.
MAX_PROTEINAS = 3
CATEGORIAS_PROTEINA = ("Carne muscular", "Pescados y mariscos")

# Compatibilidad: el valor "por defecto" es el minimo mas uno donde ayuda
CUANTOS = {c: min(CUANTOS_MIN[c] + (1 if c in ("Carne muscular", "Verduras y frutas") else 0),
                  CUANTOS_MAX[c]) for c in CUANTOS_MIN}


def _disponibles(alimentos, categoria, excluidos):
    """
    Los alimentos de esa categoria que el usuario NO ha excluido.

    ⚠️ `excluidos` NO se compara por nombre exacto: pasa por
    `exclusiones.filtrar()`, que entiende especies y familias. Antes se
    hacia `n not in excluidos` y excluir "Pollo" dejaba pasar
    "Higado de pollo" y "Cuello de pavo" — un fallo de SEGURIDAD con un
    perro alergico.
    """
    de_la_cat = [n for n, a in alimentos.items() if a.get("categoria") == categoria]
    permitidos, _fuera, _avisos = filtrar_exclusiones(de_la_cat, excluidos)
    return permitidos


def elegir_alimentos(modo, alimentos, semilla=0, excluidos=None,
                     elegidos_usuario=None, en_casa=None, cuantos=None):
    """
    Devuelve {categoria: [nombres]} listo para el motor.

    excluidos:        alergias y lo que el perfil dice evitar. Se respeta SIEMPRE
    elegidos_usuario: {categoria: [nombres]} lo que ha pedido a mano
    en_casa:          [nombres] lo que tiene (modo aprovechar)

    En los tres modos, lo que el usuario elige se RESPETA y solo se completa
    lo que falte hasta el tope de la categoria. Nunca se le quita nada.
    """
    excluidos = set(excluidos or [])
    elegidos_usuario = elegidos_usuario or {}
    en_casa = set(en_casa or [])
    cuantos = cuantos or CUANTOS
    rnd = random.Random(semilla)

    salida = {}
    for cat in PILARES:
        tope = cuantos.get(cat, 1)

        # 1. lo que ha pedido el usuario, tal cual (respetando exclusiones)
        pedidos = [n for n in elegidos_usuario.get(cat, []) if n in alimentos]
        suyos, _f, _a = filtrar_exclusiones(pedidos, excluidos)

        # 2. si es "aprovechar", lo que tiene en casa de esa categoria
        if modo == "aprovechar":
            de_casa = [n for n in _disponibles(alimentos, cat, excluidos)
                       if n in en_casa and n not in suyos]
            suyos += de_casa

        # 3. completar hasta el tope con el resto del catalogo
        faltan = tope - len(suyos)
        if faltan > 0:
            resto = [n for n in _disponibles(alimentos, cat, excluidos) if n not in suyos]
            rnd.shuffle(resto)
            suyos += resto[:faltan]

        if suyos:
            salida[cat] = suyos
    return salida


def cambiar(elegidos, viejo, nuevo, alimentos):
    """
    RECALCULO. Sustituye un alimento por otro DENTRO DE SU CATEGORIA.

    Si el nuevo es de otra categoria se rechaza: cambiar el higado por una
    zanahoria dejaria la racion sin higado, y eso no es un cambio de
    ingrediente, es romper la estructura. Que lo diga en voz alta.
    """
    cat_viejo = next((c for c, l in elegidos.items() if viejo in l), None)
    if cat_viejo is None:
        raise ValueError(f"'{viejo}' no está en el menú.")
    if nuevo not in alimentos:
        raise ValueError(f"'{nuevo}' no está en el catálogo.")
    cat_nuevo = alimentos[nuevo].get("categoria")
    if cat_nuevo != cat_viejo:
        raise ValueError(
            f"'{nuevo}' es de la categoría '{cat_nuevo}' y '{viejo}' es de "
            f"'{cat_viejo}'. Solo se puede cambiar un alimento por otro de su "
            f"misma categoría: si no, la ración se quedaría sin un pilar.")
    salida = {c: list(l) for c, l in elegidos.items()}
    salida[cat_viejo] = [nuevo if n == viejo else n for n in salida[cat_viejo]]
    return salida


def quitar(elegidos, nombre, alimentos):
    """
    Quita un alimento. Si era el ULTIMO de su categoria, se avisa: la racion
    se queda sin ese pilar y hay que decirlo, no taparlo.
    """
    cat = next((c for c, l in elegidos.items() if nombre in l), None)
    if cat is None:
        raise ValueError(f"'{nombre}' no está en el menú.")
    salida = {c: list(l) for c, l in elegidos.items()}
    salida[cat] = [n for n in salida[cat] if n != nombre]
    aviso = None
    if not salida[cat]:
        del salida[cat]
        aviso = (f"Al quitar {nombre} la ración se queda sin {cat.lower()}. "
                 f"Es uno de los pilares, así que la ración queda incompleta "
                 f"a propósito: su parte NO se ha repartido entre las demás.")
    return salida, aviso


def anadir(elegidos, nombre, alimentos, cuantos=None):
    """Anade un alimento a su categoria, respetando el tope de la categoria."""
    if nombre not in alimentos:
        raise ValueError(f"'{nombre}' no está en el catálogo.")
    cat = alimentos[nombre].get("categoria")
    cuantos = cuantos or CUANTOS
    salida = {c: list(l) for c, l in elegidos.items()}
    ya = salida.get(cat, [])
    if nombre in ya:
        return salida, f"{nombre} ya estaba en el menú."
    aviso = None
    tope = cuantos.get(cat)
    if tope and len(ya) >= tope:
        aviso = (f"Ya había {len(ya)} de {cat.lower()} y el tope son {tope}. "
                 f"Se ha quitado {ya[-1]} para hacerle sitio a {nombre}.")
        ya = ya[:-1]
    salida[cat] = ya + [nombre]
    return salida, aviso
