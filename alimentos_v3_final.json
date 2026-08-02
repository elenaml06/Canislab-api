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


# Cuantos alimentos de refuerzo se anaden POR CATEGORIA cuando el menu que
# el usuario tiene delante no da de si para cuadrar los nutrientes.
REFUERZO_POR_CATEGORIA = 3


def _ampliar_candidatos(candidatos, alimentos_disponibles, nunca_reañadir=None):
    """Anade alternativas de las MISMAS categorias que ya tiene el menu.

    Al editar, el usuario nos manda solo los 8-10 alimentos que ve en
    pantalla. Con tan pocos el optimizador casi nunca encuentra solucion
    (hacen falta ~11 para cuadrar los 27 nutrientes), asi que devolvia
    "no encontramos combinacion" practicamente siempre. Dandole algunas
    alternativas mas de las mismas categorias tiene margen para recalcular.
    """
    ya = {a["nombre"] for a in candidatos} | set(nunca_reañadir or ())
    categorias = {a["categoria"] for a in candidatos}
    ampliados = list(candidatos)
    for cat in categorias:
        extra = [a for a in alimentos_disponibles
                 if a["categoria"] == cat and a["nombre"] not in ya]
        ampliados.extend(extra[:REFUERZO_POR_CATEGORIA])
    return ampliados


def recalcular_menu(nombres_alimentos_actuales: list, der_objetivo: float,
                     etapa_requisitos: str, especies_excluidas: set = None,
                     forzar_presencia: list = None,
                     peso_perro_kg: float = None,
                     nunca_reañadir: list = None) -> dict:
    """
    Punto de entrada UNICO para cualquier cambio en un menu: anadir
    suplemento, quitar suplemento, cambiar un alimento con el lapiz.
    Se recalcula todo de cero con el optimizador.

    Primero se intenta SOLO con los alimentos que el usuario tiene en el
    menu (asi el resultado es el que espera). Si con esos no hay solucion
    posible, se reintenta anadiendo alternativas de las mismas categorias
    en vez de devolver un error: es mucho mas util que decirle "no se
    puede" cada vez que toca algo.
    """
    alimentos = cargar_alimentos()
    if especies_excluidas:
        alimentos = filtrar_alimentos_disponibles(alimentos, especies_excluidas)
    candidatos = _candidatos_por_nombre(alimentos, nombres_alimentos_actuales)

    r = optimizar_menu(candidatos, der_objetivo, etapa_requisitos,
                       forzar_presencia, peso_perro_kg=peso_perro_kg)
    if r.get("factible"):
        return r

    ampliados = _ampliar_candidatos(candidatos, alimentos, nunca_reañadir)
    r2 = optimizar_menu(ampliados, der_objetivo, etapa_requisitos,
                        forzar_presencia, peso_perro_kg=peso_perro_kg)
    if r2.get("factible"):
        r2["se_ampliaron_alimentos"] = True
        return r2
    return r


def anadir_alimento(menu_actual: list, nuevo_alimento: str, der_objetivo: float,
                     etapa_requisitos: str, especies_excluidas: set = None,
                     peso_perro_kg: float = None) -> dict:
    """Añade un alimento (ej. un suplemento) al menu y recalcula TODO de verdad."""
    nueva_lista = menu_actual + [nuevo_alimento] if nuevo_alimento not in menu_actual else menu_actual
    # si el usuario lo anade a mano, debe salir con gramos reales, no a 0
    return recalcular_menu(nueva_lista, der_objetivo, etapa_requisitos, especies_excluidas,
                            forzar_presencia=[nuevo_alimento], peso_perro_kg=peso_perro_kg)


def quitar_alimento(menu_actual: list, alimento_a_quitar: str, der_objetivo: float,
                     etapa_requisitos: str, especies_excluidas: set = None,
                     peso_perro_kg: float = None) -> dict:
    """Quita un alimento del menu y recalcula TODO de verdad."""
    nueva_lista = [a for a in menu_actual if a != alimento_a_quitar]
    # Si el recalculo no encuentra solucion, amplia candidatos... y podia
    # volver a meter justo lo que el usuario acababa de quitar. Se prohibe
    # explicitamente: si lo has quitado, no vuelve.
    return recalcular_menu(nueva_lista, der_objetivo, etapa_requisitos, especies_excluidas,
                            peso_perro_kg=peso_perro_kg,
                            nunca_reañadir=[alimento_a_quitar])


def cambiar_alimento(menu_actual: list, alimento_viejo: str, alimento_nuevo: str,
                      der_objetivo: float, etapa_requisitos: str, especies_excluidas: set = None,
                      peso_perro_kg: float = None) -> dict:
    """Sustituye un alimento por otro (el lapiz de editar) y recalcula TODO de verdad."""
    nueva_lista = [alimento_nuevo if a == alimento_viejo else a for a in menu_actual]
    # el alimento por el que se cambia debe aparecer de verdad en el menu
    return recalcular_menu(nueva_lista, der_objetivo, etapa_requisitos, especies_excluidas,
                            forzar_presencia=[alimento_nuevo], peso_perro_kg=peso_perro_kg,
                            nunca_reañadir=[alimento_viejo])


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
