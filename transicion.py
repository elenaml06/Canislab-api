"""
CANISLAB - Logica de transicion (punto 3 del plan de backend)

Guarda la fecha real de inicio de la transicion y calcula, comparando
contra la fecha de hoy, en que dia/semana esta el perro. Decide:
  - el % de BARF vs dieta anterior segun el tramo (25/50/75/100)
  - que menu esta activo esa semana (si hay varios menus elegidos)
  - cuando pasar el indicador de nutrientes de "por menu" a "por semana"
"""
from datetime import date, timedelta

TRAMOS = [
    {"dias_desde": 0, "dias_hasta": 3, "barf_pct": 25},
    {"dias_desde": 3, "dias_hasta": 6, "barf_pct": 50},
    {"dias_desde": 6, "dias_hasta": 9, "barf_pct": 75},
    {"dias_desde": 9, "dias_hasta": None, "barf_pct": 100},
]


def dias_desde_inicio(fecha_inicio: date, fecha_hoy: date = None) -> int:
    fecha_hoy = fecha_hoy or date.today()
    return (fecha_hoy - fecha_inicio).days


def calcular_tramo_transicion(fecha_inicio: date, fecha_hoy: date = None) -> dict:
    dias = dias_desde_inicio(fecha_inicio, fecha_hoy)
    if dias < 0:
        raise ValueError("La fecha de hoy es anterior a la fecha de inicio")

    for tramo in TRAMOS:
        if tramo["dias_hasta"] is None or dias < tramo["dias_hasta"]:
            return {
                "dia_actual": dias + 1,  # dia 1, no dia 0
                "barf_pct": tramo["barf_pct"],
                "dieta_anterior_pct": 100 - tramo["barf_pct"],
                "transicion_completa": tramo["barf_pct"] == 100,
            }


def semana_actual(fecha_inicio: date, fecha_hoy: date = None) -> int:
    """Semana 1, 2, 3... desde que empezo la transicion (para saber que
    menu toca desbloquear, si hay varios elegidos)."""
    dias = dias_desde_inicio(fecha_inicio, fecha_hoy)
    return (dias // 7) + 1


def menu_activo_y_bloqueados(fecha_inicio: date, num_menus_elegidos: int, fecha_hoy: date = None) -> dict:
    """
    Devuelve que menu esta activo esta semana y cuales siguen bloqueados,
    solo relevante mientras dura la transicion (ver punto 3 del plan:
    un solo menu, sustitucion completa semana a semana, no mezclados).
    """
    semana = semana_actual(fecha_inicio, fecha_hoy)
    menu_activo_idx = min(semana, num_menus_elegidos)  # 1-indexado, tope en el ultimo elegido
    return {
        "semana_actual": semana,
        "menu_activo": menu_activo_idx,
        "menus_bloqueados": [i for i in range(1, num_menus_elegidos + 1) if i != menu_activo_idx],
        "rotacion_completa": semana > num_menus_elegidos,  # ya se probaron todos, ahora rota de verdad
    }


def nivel_indicador_nutrientes(fecha_inicio: date, num_menus_elegidos: int, fecha_hoy: date = None) -> str:
    """
    Decide si el indicador '27/27 OK' se muestra POR MENU o POR SEMANA
    (principio ya acordado: por menu durante transicion con 1 solo activo,
    por semana cuando ya hay rotacion real entre varios menus).
    """
    info = menu_activo_y_bloqueados(fecha_inicio, num_menus_elegidos, fecha_hoy)
    return "semana" if info["rotacion_completa"] else "menu"


if __name__ == "__main__":
    inicio = date(2026, 7, 25)  # ejemplo: empezo hace una semana

    print("=== Cairo empezo la transicion el 25 de julio, con 3 menus elegidos ===\n")
    for offset in [0, 2, 3, 5, 6, 8, 9, 15, 22, 29]:
        hoy = inicio + timedelta(days=offset)
        tramo = calcular_tramo_transicion(inicio, hoy)
        menus = menu_activo_y_bloqueados(inicio, 3, hoy)
        nivel = nivel_indicador_nutrientes(inicio, 3, hoy)
        print(f"Dia {tramo['dia_actual']:3d} ({hoy}): {tramo['barf_pct']}% BARF"
              f" | Menu activo: {menus['menu_activo']}"
              f" | Bloqueados: {menus['menus_bloqueados']}"
              f" | Indicador nutrientes: {nivel}")
