"""
CANISLAB - Calculo de DER (Daily Energy Requirement)

POR QUE UN SOLO MULTIPLICADOR Y NO "ETAPA x ACTIVIDAD"
------------------------------------------------------
El Excel original cruzaba dos factores (uno de etapa y otro de actividad) y
los multiplicaba. Se cambio a un unico factor por situacion porque asi es
como lo presentan las fuentes: FEDIAF (Anexo 7.2.4, "Practical
recommendations for daily energy intake by dogs and cats in different
physiological states") y NRC dan UN factor sobre el RER para cada situacion,
no dos que se multipliquen.

La razon de fondo es que el factor de cada etapa YA INCLUYE la actividad
tipica de esa etapa:
  - Un cachorro de 5 meses no es "sedentario" ni "activo" en el sentido
    adulto: el 2.0 ya contempla que juega y ademas esta creciendo. Cruzarlo
    con 1.2 o 1.8 daria 2.4-3.6, sin respaldo en ninguna fuente.
  - Lo mismo con gestacion y lactancia: el coste metabolico domina sobre la
    actividad, que ademas baja en esas fases.

Donde SI se usa la actividad es donde toca: en ADULTO y SENIOR, el
multiplicador ES el de actividad. Asi que en la practica si hay dos ejes,
solo que no se multiplican entre si: la etapa decide QUE tabla se usa, y
dentro de adulto/senior la actividad decide el valor.

TODOS los multiplicadores se aplican sobre el RER (70 x peso^0.75).
"""

# TODOS estos multiplicadores se aplican sobre el RER (70 x peso^0.75).
#
# CORREGIDO en la auditoria nutricional del 2 de agosto: gestacion y
# lactancia estaban MAL. Con los valores anteriores una perra en gestacion
# tardia (1.5) recibia MENOS calorias que un adulto normal (1.6), y una
# lactante (2.5) apenas mas. Es justo al reves: son las dos situaciones de
# mayor demanda energetica de la vida del perro. Una lactante mal alimentada
# pierde condicion corporal muy rapido y los cachorros crecen peor.
#
# Referencias: FEDIAF y NRC expresan gestacion y lactancia como multiplos
# del MANTENIMIENTO, no del RER:
#   - gestacion primeras 5-6 semanas ~ mantenimiento
#   - gestacion ultimo tercio        ~ mantenimiento x 1.25-1.5
#   - lactancia (pico)               ~ mantenimiento x 2-4 segun camada
# Tomando mantenimiento = RER x 1.6, sobre RER quedan:
MULTIPLICADOR_FIJO = {
    "cachorro_joven": 3.0,        # <4 meses (coincide con FEDIAF)
    "cachorro_crecimiento": 2.0,  # 4 meses en adelante (coincide con FEDIAF)
    "gestante_temprana": 1.6,     # = mantenimiento
    "gestante_tardia": 2.2,       # = mantenimiento x 1.4
    "lactante": 3.2,              # = mantenimiento x 2 (valor PRUDENTE:
                                  # el pico real llega a x4 con camadas
                                  # grandes -- pendiente ajustarlo por
                                  # numero de cachorros y semana)
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
