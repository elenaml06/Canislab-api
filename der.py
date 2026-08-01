"""
CANISLAB - Calculo de DER (Daily Energy Requirement)
Implementa la tabla de multiplicadores acordada en esta sesion (un solo
multiplicador combinado por situacion, NO etapa x actividad cruzados).
"""

MULTIPLICADOR_FIJO = {
    "cachorro_joven": 3.0,       # <4 meses
    "cachorro_crecimiento": 2.0,  # 4 meses en adelante, en crecimiento
    "gestante_temprana": 1.0,
    "gestante_tardia": 1.5,
    "lactante": 2.5,
}

MULTIPLICADOR_ADULTO = {
    "sedentario": 1.2,
    "normal": 1.6,
    "activo": 1.8,
    "muy_activo": 2.0,
    "trabajo": 3.0,
}

MULTIPLICADOR_SENIOR = {
    "sedentario": 1.0,
    "normal": 1.2,
    "activo": 1.4,
}

FACTOR_ESTERILIZADO = 0.889


def calcular_rer(peso_actual_kg: float) -> float:
    """RER = 70 * peso^0.75 (formula estandar, kcal/dia)."""
    return 70 * (peso_actual_kg ** 0.75)


def calcular_der(peso_actual_kg: float, etapa: str, actividad: str = None, esterilizado: bool = False) -> dict:
    """
    etapa: "cachorro_joven" | "cachorro_crecimiento" | "gestante_temprana"
           | "gestante_tardia" | "lactante" | "adulto" | "senior"
    actividad: solo se usa si etapa es "adulto" o "senior"
    """
    rer = calcular_rer(peso_actual_kg)

    if etapa in MULTIPLICADOR_FIJO:
        multiplicador = MULTIPLICADOR_FIJO[etapa]
    elif etapa == "adulto":
        if actividad not in MULTIPLICADOR_ADULTO:
            raise ValueError(f"Actividad '{actividad}' no valida para adulto")
        multiplicador = MULTIPLICADOR_ADULTO[actividad]
    elif etapa == "senior":
        if actividad not in MULTIPLICADOR_SENIOR:
            raise ValueError(f"Actividad '{actividad}' no valida para senior")
        multiplicador = MULTIPLICADOR_SENIOR[actividad]
    else:
        raise ValueError(f"Etapa '{etapa}' no reconocida")

    if esterilizado:
        multiplicador *= FACTOR_ESTERILIZADO

    der = rer * multiplicador
    return {
        "rer": round(rer, 1),
        "multiplicador_aplicado": round(multiplicador, 3),
        "der": round(der, 1),
    }


if __name__ == "__main__":
    # Caso real: Cairo, 16kg actual, cachorro en crecimiento
    resultado = calcular_der(peso_actual_kg=16, etapa="cachorro_crecimiento")
    print("=== CAIRO (16kg, cachorro en crecimiento) ===")
    print(resultado)
    assert abs(resultado["der"] - 1120) < 50, f"DER inesperado: {resultado['der']} (se esperaba ~1120)"
    print("OK: coincide con el DER ya usado en el proyecto (~1120 kcal)\n")

    # Caso adulto activo esterilizado, 30kg
    resultado2 = calcular_der(peso_actual_kg=30, etapa="adulto", actividad="activo", esterilizado=True)
    print("=== Adulto 30kg, activo, esterilizado ===")
    print(resultado2)
