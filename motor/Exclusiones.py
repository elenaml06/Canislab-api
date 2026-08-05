# -*- coding: utf-8 -*-
"""
EXCLUSIONES — lo que el usuario NO quiere en la ración.

Cubre alergias, intolerancias, manías del perro, lo que no encuentra en su
tienda y lo que simplemente no le da la gana usar. Todo se trata igual: si
el usuario lo excluye, no aparece.

EL FALLO QUE ARREGLA (real, detectado el 3 agosto)
--------------------------------------------------
La exclusión funcionaba por NOMBRE EXACTO. Cairo es alergico al pollo y al
pavo; se excluia "Pollo" y "Pavo", y el motor seguia metiendo:
    "Pollo con piel (sin hueso)"   "Carcasa de pollo"   "Higado de pollo"
    "Cuello de pavo"               "Pavo muslo con piel"
porque ninguno se llama exactamente "Pollo" ni "Pavo".
Es un fallo de SEGURIDAD: un perro alergico habria comido justo lo que le
sienta mal.

COMO FUNCIONA AHORA
-------------------
Se compara por PALABRAS, no por cadena exacta, y sin tildes ni mayusculas:
  · "pollo"            -> quita todo lo que lleve "pollo" en el nombre
  · "Higado de pollo"  -> quita solo ese
  · "ternera"          -> quita solo la ternera, NO "Ternero"... (ver abajo)

Ademas se conocen las FAMILIAS: excluir "pollo" quita tambien "gallina",
porque es la misma especie (Gallus gallus) y un perro alergico al pollo
reacciona igual. Esto NO es opcional: Olivry et al. (2017, BMC Vet Res
13:251) midieron que los perros con IgE anti-pollo reaccionan tambien a
PATO y PAVO en el ~97% de los casos.
"""
import unicodedata

# Especies que se comportan como una sola a efectos de alergia.
# La clave es lo que escribe el usuario; los valores, lo que hay que quitar.
FAMILIAS_ALERGIA = {
    # OJO: el HUEVO no entra aqui. La alergia al huevo es a sus proteinas
    # (ovoalbumina, ovomucoide) y es INDEPENDIENTE de la alergia a la carne
    # de pollo. Mueller & Olivry (2016, BMC Vet Res 12:9) los listan como
    # alergenos distintos. Excluir el huevo al decir "pollo" seria quitar un
    # alimento util sin motivo. Quien sea alergico al huevo, que escriba
    # "huevo".
    "pollo":   ["pollo", "gallina", "gallo"],
    "gallina": ["pollo", "gallina", "gallo"],
    "pavo":    ["pavo"],
    "pato":    ["pato"],
    "ternera": ["ternera", "vaca", "buey", "toro", "vacuno", "res"],
    "vaca":    ["ternera", "vaca", "buey", "toro", "vacuno", "res"],
    "buey":    ["ternera", "vaca", "buey", "toro", "vacuno", "res"],
    "cordero": ["cordero", "oveja", "borrego"],
    "cerdo":   ["cerdo", "porcino", "cochino"],
    "conejo":  ["conejo"],
    "caballo": ["caballo", "equino"],
    "pescado": ["pescado", "salmón", "salmon", "sardina", "caballa", "merluza",
                "atún", "atun", "trucha", "boquerón", "boqueron", "arenque",
                "lubina", "dorada", "bacalao", "rape", "sepia", "pulpo",
                "mejillón", "mejillon", "gamba", "langostino"],
    "huevo":   ["huevo"],
    "lácteo":  ["yogur", "queso", "leche", "kéfir", "kefir"],
    "lacteo":  ["yogur", "queso", "leche", "kéfir", "kefir"],
}

# Aves emparentadas: quien es alergico a una suele serlo a las demas.
# Olivry 2017: ~97% de reactividad cruzada pollo <-> pato <-> pavo.
AVES = ["pollo", "gallina", "gallo", "pavo", "pato", "codorniz", "oca", "ganso"]


def _palabras(s):
    """las palabras del nombre, normalizadas y sin signos"""
    n = _norm(s)
    for ch in "(),.;:/-":
        n = n.replace(ch, " ")
    return set(n.split())


def _norm(s):
    """minusculas y sin tildes, para comparar sin sorpresas"""
    s = unicodedata.normalize("NFD", str(s))
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return s.lower().strip()


def expandir_exclusiones(lo_que_dijo, avisar_aves=True):
    """
    Convierte lo que escribe el usuario en la lista de terminos a buscar.

    lo_que_dijo: lista de textos ("pollo", "Hígado de pollo", "ternera"...)
    Devuelve (terminos, avisos)
    """
    terminos, avisos = set(), []
    for bruto in (lo_que_dijo or []):
        t = _norm(bruto)
        if not t:
            continue
        terminos.add(t)
        # si es una familia conocida, añadir todos sus miembros
        familia = FAMILIAS_ALERGIA.get(t)
        if familia:
            for m in familia:
                terminos.add(_norm(m))
            otros = [m for m in familia if _norm(m) != t]
            if otros:
                avisos.append(
                    f"Al excluir «{bruto}» se quitan también {', '.join(otros)}: "
                    f"es la misma especie o muy cercana.")
        # aviso de reactividad cruzada entre aves
        if avisar_aves and t in AVES:
            otras = [a for a in AVES if a != t and a not in terminos]
            if otras:
                avisos.append(
                    f"Ojo: los perros alérgicos a un ave suelen reaccionar también "
                    f"a las demás ({', '.join(otras[:3])}...). Si es una alergia "
                    f"diagnosticada, coméntalo con tu veterinario antes de usarlas.")
    return terminos, avisos


def esta_excluido(nombre_alimento, terminos):
    """
    True si este alimento cae en alguna exclusion.

    ⚠️ SE COMPARA POR PALABRAS COMPLETAS, no por subcadena. Buscando "pollo"
    dentro del texto se excluia el REPOLLO, que es una col. El mismo fallo
    habria quitado "empanada" al excluir "pan".
    Se admite que el termino sea una palabra suelta del nombre, o varias
    palabras seguidas ("higado de pollo").
    """
    palabras = _palabras(nombre_alimento)
    n = _norm(nombre_alimento)

    # EL HUEVO SE EXCLUYE SOLO SI SE PIDE EXPRESAMENTE.
    # "Huevo de gallina entero" lleva la palabra "gallina", asi que al
    # excluir el pollo se iba tambien el huevo. Son alergenos DISTINTOS
    # (Mueller & Olivry 2016): la alergia al huevo es a la ovoalbumina y la
    # ovomucoide, no a la carne. Quitarlo sin motivo es perder un alimento
    # util y barato.
    es_huevo = "huevo" in palabras or "huevos" in palabras
    if es_huevo and not any(t.startswith("huevo") for t in terminos):
        return False

    for t in terminos:
        if not t:
            continue
        if " " in t:                       # termino de varias palabras
            if t in n:
                return True
        elif t in palabras:                # palabra completa
            return True
    return False


def filtrar(alimentos, lo_que_dijo, avisar_aves=True):
    """
    Devuelve (nombres_permitidos, nombres_quitados, avisos).
    `alimentos` puede ser un dict {nombre: datos} o una lista de nombres.
    """
    nombres = list(alimentos.keys()) if isinstance(alimentos, dict) else list(alimentos)
    terminos, avisos = expandir_exclusiones(lo_que_dijo, avisar_aves)
    permitidos, quitados = [], []
    for n in nombres:
        (quitados if esta_excluido(n, terminos) else permitidos).append(n)
    return permitidos, quitados, avisos
