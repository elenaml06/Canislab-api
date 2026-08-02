"""
CANISLAB - Recalculo real al tocar cosas (punto 4 del plan de backend)

Cuando el usuario anade/quita un suplemento, o edita un alimento con el
lapiz, esto vuelve a llamar al optimizador de verdad con la lista de
alimentos actualizada -- no una simulacion aproximada como hacia el
frontend hasta ahora (que solo reajustaba gramos a ojo).
"""
import sys
sys.path.insert(0, '.')
from especies import cargar_alimentos, filtrar_alimentos_disponibles
from optimizador import optimizar_menu


def _candidatos_por_nombre(alimentos, nombres):
    por_nombre = {a["nombre"]: a for a in alimentos}
    return [por_nombre[n] for n in nombres if n in por_nombre]


def recalcular_menu(nombres_alimentos_actuales: list, der_objetivo: float,
                     etapa_requisitos: str, especies_excluidas: set = None,
                     forzar_presencia: list = None) -> dict:
    """
    Punto de entrada UNICO para cualquier cambio en un menu: anadir
    suplemento, quitar suplemento, cambiar un alimento con el lapiz.
    Siempre se le pasa la lista COMPLETA de alimentos que debe tener el
    menu tras el cambio, y se recalcula todo de cero con el optimizador.
    """
    alimentos = cargar_alimentos()
    if especies_excluidas:
        alimentos = filtrar_alimentos_disponibles(alimentos, especies_excluidas)
    candidatos = _candidatos_por_nombre(alimentos, nombres_alimentos_actuales)
    return optimizar_menu(candidatos, der_objetivo, etapa_requisitos, forzar_presencia)


def anadir_alimento(menu_actual: list, nuevo_alimento: str, der_objetivo: float,
                     etapa_requisitos: str, especies_excluidas: set = None) -> dict:
    """Añade un alimento (ej. un suplemento) al menu y recalcula TODO de verdad."""
    nueva_lista = menu_actual + [nuevo_alimento] if nuevo_alimento not in menu_actual else menu_actual
    # si el usuario lo anade a mano, debe salir con gramos reales, no a 0
    return recalcular_menu(nueva_lista, der_objetivo, etapa_requisitos, especies_excluidas,
                            forzar_presencia=[nuevo_alimento])


def quitar_alimento(menu_actual: list, alimento_a_quitar: str, der_objetivo: float,
                     etapa_requisitos: str, especies_excluidas: set = None) -> dict:
    """Quita un alimento del menu y recalcula TODO de verdad."""
    nueva_lista = [a for a in menu_actual if a != alimento_a_quitar]
    return recalcular_menu(nueva_lista, der_objetivo, etapa_requisitos, especies_excluidas)


def cambiar_alimento(menu_actual: list, alimento_viejo: str, alimento_nuevo: str,
                      der_objetivo: float, etapa_requisitos: str, especies_excluidas: set = None) -> dict:
    """Sustituye un alimento por otro (el lapiz de editar) y recalcula TODO de verdad."""
    nueva_lista = [alimento_nuevo if a == alimento_viejo else a for a in menu_actual]
    # el alimento por el que se cambia debe aparecer de verdad en el menu
    return recalcular_menu(nueva_lista, der_objetivo, etapa_requisitos, especies_excluidas,
                            forzar_presencia=[alimento_nuevo])


if __name__ == "__main__":
    # Menu base real de Cairo (el que ya validamos: 800g, completo y variado)
    menu_cairo = [
        "Ternera con grasa", "Cuello de ternera", "Riñón de ternera",
        "Pulmón de ternera", "Hígado de vaca", "Mejillón",
        "Espinaca", "Aceite de girasol", "Sonrisa de Diez Kelp",
    ]
    der = 1120
    etapa = "CachorroCrecimiento"
    excluidas = {"Pollo", "Pavo"}

    print("=== MENU BASE DE CAIRO ===")
    base = recalcular_menu(menu_cairo, der, etapa, excluidas)
    if base["factible"]:
        print(f"{base['total_gramos']}g, {base['kcal_total']}kcal")
        for n, g in sorted(base["gramos"].items(), key=lambda x: -x[1]):
            print(f"  {n}: {g}g")
    else:
        print("NO FACTIBLE:", base["motivo"])

    print("\n=== EL USUARIO AÑADE UN SUPLEMENTO DE CALCIO (GRAU Harina de Hueso) ===")
    con_calcio = anadir_alimento(menu_cairo, "GRAU Harina de Hueso", der, etapa, excluidas)
    if con_calcio["factible"]:
        print(f"{con_calcio['total_gramos']}g, {con_calcio['kcal_total']}kcal")
        for n, g in sorted(con_calcio["gramos"].items(), key=lambda x: -x[1]):
            print(f"  {n}: {g}g")
    else:
        print("NO FACTIBLE:", con_calcio["motivo"])

    print("\n=== EL USUARIO QUITA EL MEJILLÓN CON EL LÁPIZ, LO CAMBIA POR SALMÓN ===")
    cambiado = cambiar_alimento(menu_cairo, "Mejillón", "Salmón", der, etapa, excluidas)
    if cambiado["factible"]:
        print(f"{cambiado['total_gramos']}g, {cambiado['kcal_total']}kcal")
        for n, g in sorted(cambiado["gramos"].items(), key=lambda x: -x[1]):
            print(f"  {n}: {g}g")
    else:
        print("NO FACTIBLE:", cambiado["motivo"])
        print("(esperado: Salmón por si solo no cubre suficiente Yodo -> ejemplo real de punto 6)")
