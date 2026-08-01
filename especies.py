"""
CANISLAB - Motor de especies
Extrae la especie real de un alimento a partir de su nombre, y permite
excluir una especie cruzando TODAS las categorias donde aparezca.

Regla de extraccion (misma logica ya usada en el frontend para agrupar):
- Si el nombre contiene " de X", la especie es X (ej. "Cuello de pollo" -> Pollo)
- Si no, la especie es la primera palabra (ej. "Pavo pechuga con piel" -> Pavo)
"""
import json


def especie_de(nombre: str) -> str:
    if " de " in nombre:
        resto = nombre.split(" de ", 1)[1]
        return resto.split(" ")[0].capitalize()
    return nombre.split(" ")[0]


def cargar_alimentos(path="/tmp/alimentos_v3_final.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def especies_excluidas_a_alimentos(alimentos: list, especies_excluidas: set) -> set:
    """
    Dado un conjunto de especies excluidas (ej. {"Pollo", "Pavo"}),
    devuelve el conjunto de NOMBRES DE ALIMENTO que hay que excluir,
    buscando en TODAS las categorias, no solo en la categoria donde
    el usuario marco la exclusion originalmente.

    Este es el fix del bug: antes, excluir "Pollo" en Carne muscular
    no afectaba a "Cuello de pollo" en Hueso carnoso. Con esta funcion,
    se excluye en TODAS las categorias a la vez.
    """
    especies_excluidas_norm = {e.strip().lower() for e in especies_excluidas}
    excluidos = set()
    for a in alimentos:
        esp = especie_de(a["nombre"]).lower()
        if esp in especies_excluidas_norm:
            excluidos.add(a["nombre"])
    return excluidos


def filtrar_alimentos_disponibles(alimentos: list, especies_excluidas: set, nombres_excluidos_directos: set = None):
    """
    Devuelve la lista de alimentos que SI se pueden usar, tras aplicar:
    1) exclusion por especie completa (cruzando categorias)
    2) exclusion de alimentos concretos marcados uno a uno (ej. "Todo: Pollo"
       ya viene resuelto como especie, pero si el usuario excluyo un corte
       muy concreto sin marcar "toda la especie", tambien se respeta)
    """
    nombres_excluidos_directos = nombres_excluidos_directos or set()
    excluidos_por_especie = especies_excluidas_a_alimentos(alimentos, especies_excluidas)
    todos_excluidos = excluidos_por_especie | nombres_excluidos_directos
    return [a for a in alimentos if a["nombre"] not in todos_excluidos]


if __name__ == "__main__":
    alimentos = cargar_alimentos()

    # --- TEST: reproducir el bug encontrado por el usuario ---
    print("=== TEST: excluir 'Pollo' debe afectar a TODAS las categorias ===")
    excluidos = especies_excluidas_a_alimentos(alimentos, {"Pollo"})
    for nombre in sorted(excluidos):
        cat = next(a["categoria"] for a in alimentos if a["nombre"] == nombre)
        print(f"  EXCLUIDO: {nombre}  (categoria: {cat})")

    categorias_afectadas = {next(a["categoria"] for a in alimentos if a["nombre"] == n) for n in excluidos}
    print(f"\nCategorias afectadas por excluir 'Pollo': {categorias_afectadas}")
    assert len(categorias_afectadas) > 1, "FALLO: deberia afectar a mas de una categoria"
    print("OK: la exclusion cruza categorias correctamente\n")

    # --- Caso real de Cairo: alergia a pollo Y pavo ---
    print("=== CASO REAL CAIRO: alergia a Pollo y Pavo ===")
    excluidos_cairo = especies_excluidas_a_alimentos(alimentos, {"Pollo", "Pavo"})
    print(f"Total alimentos excluidos: {len(excluidos_cairo)}")
    for nombre in sorted(excluidos_cairo):
        cat = next(a["categoria"] for a in alimentos if a["nombre"] == nombre)
        print(f"  - {nombre} ({cat})")

    disponibles = filtrar_alimentos_disponibles(alimentos, {"Pollo", "Pavo"})
    print(f"\nAlimentos disponibles tras excluir Pollo+Pavo: {len(disponibles)} de {len(alimentos)}")
