# -*- coding: utf-8 -*-
"""
CANISLAB — Cálculo del DER (necesidad energética diaria) — MÉTODO EUROPEO

=============================================================================
FUENTES  (verificadas el 2 agosto 2026, no citadas de memoria)
=============================================================================
· CRECIMIENTO, GESTACIÓN y LACTANCIA -> FEDIAF.
· ADULTOS -> tesis de la Universidad de Múnich (Thes_Cindy_Melanie,
  edoc.ub.uni-muenchen.de/17585): estudio retrospectivo del consumo
  energético REAL de 586 perros de compañía privados europeos.
Ambas recogidas y aplicadas en la calculadora alemana "Hannes Sein
Futterrechner" (dr.ueke.de), que declara sus fuentes explícitamente.

=============================================================================
CÓMO FUNCIONA — y en qué se diferencia del método americano
=============================================================================
El método AMERICANO hace:   DER = RER x UN factor multiplicativo.
El método EUROPEO hace:     DER = (base + modificadores) x peso^0.75
                            con los modificadores SUMÁNDOSE en kcal/kg^0.75.

Por eso aquí no hay "multiplicadores" que se puedan apilar por error: hay
un COEFICIENTE en kcal por kg de peso metabólico, y unos ajustes que se le
suman o restan.

=============================================================================
¿SE USA LA ACTIVIDAD EN CACHORROS?  NO. Y la fuente lo dice literal:
=============================================================================
  "Für Hunde im Wachstum und Reproduktion ist dies unerheblich, denn sie
   brauchen generell mehr Energie, um zusätzliche Körpermasse zu produzieren."
  (Para perros en crecimiento y reproducción esto es IRRELEVANTE, porque
   necesitan más energía en general para producir masa corporal.)

Lo repite para la actividad, la convivencia, la edad Y la raza: los cuatro
ajustes se apagan en cachorros, gestantes y lactantes. En esas etapas manda
el crecimiento o la lactancia, no cuánto pasea.

=============================================================================
QUÉ CAMBIÓ RESPECTO A LA VERSIÓN ANTERIOR (y por qué)
=============================================================================
1. CRECIMIENTO: antes eran 2 tramos fijos por EDAD (3.0 y 2.0 x RER). Ahora
   son 3 tramos por % DEL PESO ADULTO esperado, que es como lo hace FEDIAF.
   El x2.0 fijo equivalía al tramo "desde el 80%" y se aplicaba desde los 4
   meses: se quedaba MUY corto a mitad de crecimiento.
2. GESTACIÓN: fórmula real de FEDIAF, aditiva. La anterior (x2.2) daba menos
   de lo debido.
3. LACTANCIA: depende del NÚMERO DE CACHORROS y de la SEMANA. El x3.2 fijo
   solo valía para camadas de 1-2.
4. ESTERILIZACIÓN: el dato europeo dice que NO cambia el gasto (la fuente lo
   marca con un "(!)"). Se conserva el parámetro por compatibilidad pero ya
   no reduce nada. Lo que sí sube el gasto es ser MACHO ENTERO (+10).
5. SOBREPESO: si el perro está >=10% por encima de su peso ideal, el gasto
   se baja al RER puro (70) y eso MANDA sobre todo lo demás.

Todo se calcula sobre el PESO IDEAL cuando se conoce, no sobre el actual.
"""

# =============================================================================
# ADULTOS — base por actividad (kcal por kg de peso metabólico)
# =============================================================================
BASE_ACTIVIDAD = {
    "sedentario":   88,    # hasta 1 h de actividad al día
    "normal":       98,    # hasta 2,5 h
    "activo":      110,    # interpolado entre 98 y 120
    "muy_activo":  120,    # más de 2,5 h
    "trabajo":     150,    # deporte de resistencia o trabajo real:
                           # fuera del rango del estudio, se mantiene el
                           # valor alto que ya usaba el proyecto (~2.1 x RER)
}

# Ajustes ADITIVOS, en kcal/kg^0.75. Solo se aplican a adulto y senior.
AJUSTE_EDAD = {
    "joven":   +15,   # 1 a 2 años
    "adulto":    0,   # 2 a 7 años
    "senior":   -5,   # más de 7 años
}
AJUSTE_CONVIVENCIA = {"solo": 0, "con_otros_perros": +10}
AJUSTE_MACHO_ENTERO = +10

# Razas con gasto por encima / por debajo de la media (estudio de Múnich).
# Los nombres están tal como aparecen en nuestra lista de 136 razas.
RAZAS_MAS_GASTO = {
    "Jack Russell Terrier", "Parson Russell Terrier", "Dálmata",
    "Braco Húngaro (Vizsla)", "Bearded Collie", "Greyhound", "Whippet",
    "Galgo Español", "Galgo Afgano", "Boxer", "Rhodesian Ridgeback",
    "Flat Coated Retriever",
}
RAZAS_MENOS_GASTO = {
    "Dachshund Estándar", "Dachshund Miniatura", "Bichón Maltés",
    "Bichón Habanero", "Bichón Frisé", "West Highland White Terrier",
    "Collie de Pelo Largo", "Shetland Sheepdog", "Airedale Terrier",
    "American Staffordshire Terrier", "Golden Retriever",
}
AJUSTE_RAZA = 15

# =============================================================================
# CRECIMIENTO (FEDIAF) — por % del peso ADULTO esperado, no por edad
# =============================================================================
CRECIMIENTO = [
    (0.50, 210),   # hasta el 50% del peso final   (= RER x 3.0)
    (0.80, 175),   # del 50 al 80%                 (= RER x 2.5)
    (None, 140),   # del 80% en adelante           (= RER x 2.0)
]

# =============================================================================
# GESTACIÓN y LACTANCIA (FEDIAF)
# =============================================================================
GESTACION_BASE = 132              # kcal/kg^0.75, toda la gestación
GESTACION_EXTRA_DESDE_SEM5 = 26   # + kcal por kg de PESO VIVO desde la sem. 5
LACTANCIA_BASE = 145              # kcal/kg^0.75
# El extra de lactancia se pondera por semana: sube hasta el pico y baja
LACTANCIA_PESO_SEMANA = [0.75, 0.95, 1.10, 1.40]
# TOPE DE SEGURIDAD. El termino extra de la lactancia escala con el PESO VIVO
# (24 x n x peso), asi que en perros grandes se dispara muy por encima de lo
# que da la tabla clinica (Small Animal Clinical Nutrition), cuyo maximo es
# x6 del RER incluso con camadas de 9 o mas cachorros. Como la formula de
# lactancia viene de una fuente SECUNDARIA y no se ha podido contrastar con
# el texto original de FEDIAF, se limita al maximo de la tabla clinica.
# Es la parte menos verificada de todo el DER: la lactancia SIEMPRE deberia
# pautarla un veterinario, y ademas hay que recalcular cada semana.
LACTANCIA_TOPE_RER = 6.0

# =============================================================================
# PESO CORPORAL — manda sobre todo lo demás
# =============================================================================
RER_COEF = 70                     # RER = 70 x peso^0.75
SOBREPESO_UMBRAL = 1.10           # >=10% por encima del ideal
INFRAPESO_UMBRAL = 0.90           # >=10% por debajo
INFRAPESO_AUMENTO = 1.20          # +20%


def calcular_rer(peso_kg: float) -> float:
    """Necesidad en reposo. Es la base de todo."""
    return RER_COEF * peso_kg ** 0.75


def _coef_crecimiento(peso_actual: float, peso_adulto: float) -> float:
    if not peso_adulto or peso_adulto <= 0:
        return CRECIMIENTO[-1][1]     # sin peso adulto, lo prudente
    frac = peso_actual / peso_adulto
    for limite, kcal in CRECIMIENTO:
        if limite is None or frac <= limite:
            return kcal
    return CRECIMIENTO[-1][1]


def _coef_adulto(actividad, edad_grupo, convivencia, macho_entero, raza):
    if actividad not in BASE_ACTIVIDAD:
        raise ValueError(f"Actividad '{actividad}' no reconocida")
    k = BASE_ACTIVIDAD[actividad]
    k += AJUSTE_EDAD.get(edad_grupo, 0)
    k += AJUSTE_CONVIVENCIA.get(convivencia, 0)
    if macho_entero:
        k += AJUSTE_MACHO_ENTERO
    if raza in RAZAS_MAS_GASTO:
        k += AJUSTE_RAZA
    elif raza in RAZAS_MENOS_GASTO:
        k -= AJUSTE_RAZA
    return k


def calcular_der(peso_actual_kg: float, etapa: str, actividad: str = None,
                 esterilizado: bool = False, peso_adulto_esperado_kg: float = None,
                 peso_ideal_kg: float = None, convivencia: str = "solo",
                 macho_entero: bool = False, raza: str = None,
                 semana_gestacion: int = None, n_cachorros: int = None,
                 semana_lactancia: int = 3) -> dict:
    """
    etapa: "cachorro_joven" | "cachorro_crecimiento" | "gestante_temprana"
           | "gestante_tardia" | "lactante" | "adulto" | "senior"

    Los parámetros nuevos son TODOS opcionales: sin ellos el cálculo sigue
    funcionando con valores prudentes, así que nada que ya llamaba a esta
    función se rompe.
    """
    if not peso_actual_kg or peso_actual_kg <= 0:
        raise ValueError("El peso tiene que ser mayor que cero")

    # El cálculo se hace sobre el peso IDEAL si se conoce (en adultos).
    en_crecimiento = etapa in ("cachorro_joven", "cachorro_crecimiento")
    peso_calculo = peso_actual_kg
    aviso_peso = None
    if peso_ideal_kg and peso_ideal_kg > 0 and not en_crecimiento:
        ratio = peso_actual_kg / peso_ideal_kg
        if ratio >= SOBREPESO_UMBRAL:
            # Sobrepeso: manda sobre todo. Se baja al RER del peso IDEAL.
            der = RER_COEF * peso_ideal_kg ** 0.75
            return {
                "rer": round(calcular_rer(peso_ideal_kg), 1),
                "coeficiente_kcal_kg075": RER_COEF,
                "multiplicador_aplicado": 1.0,
                "der": round(der, 1),
                "metodo": "europeo",
                "aviso": (f"Está un {(ratio-1)*100:.0f}% por encima de su peso ideal. "
                          f"La ración se ha bajado a su necesidad en reposo y conviene "
                          f"aumentar el ejercicio. Pésalo cada mes."),
            }
        peso_calculo = peso_ideal_kg
        if ratio <= INFRAPESO_UMBRAL:
            aviso_peso = (f"Está un {(1-ratio)*100:.0f}% por debajo de su peso ideal: "
                          f"se ha subido la ración un 20%. Pésalo cada mes.")

    rer = calcular_rer(peso_calculo)

    # --- coeficiente según la etapa ---
    if en_crecimiento:
        coef = _coef_crecimiento(peso_actual_kg, peso_adulto_esperado_kg)
        der = coef * peso_actual_kg ** 0.75
    elif etapa in ("gestante_temprana", "gestante_tardia"):
        coef = GESTACION_BASE
        der = coef * peso_calculo ** 0.75
        tardia = etapa == "gestante_tardia" or (semana_gestacion or 0) >= 5
        if tardia:
            der += GESTACION_EXTRA_DESDE_SEM5 * peso_calculo
    elif etapa == "lactante":
        coef = LACTANCIA_BASE
        n = n_cachorros if n_cachorros and n_cachorros > 0 else 4
        # OJO: la fuente alemana escribe "(96 + 12 x nº cachorros)", pero eso
        # da un SALTO imposible entre 4 y 5 cachorros (de 96 a 156). La forma
        # del NRC es 96 + 12x(n-4), que sí es continua: con 4 cachorros
        # 24x4 = 96, y 96 + 12x0 = 96. Se usa la continua.
        extra = (24 * n * peso_calculo) if n <= 4 else ((96 + 12 * (n - 4)) * peso_calculo)
        sem = min(max(semana_lactancia or 3, 1), 4)
        der = coef * peso_calculo ** 0.75 + extra * LACTANCIA_PESO_SEMANA[sem - 1]
        tope = LACTANCIA_TOPE_RER * calcular_rer(peso_calculo)
        topada = der > tope
        if topada:
            der = tope
    elif etapa in ("adulto", "senior"):
        grupo = "senior" if etapa == "senior" else "adulto"
        coef = _coef_adulto(actividad or "normal", grupo, convivencia,
                            macho_entero, raza)
        der = coef * peso_calculo ** 0.75
    else:
        raise ValueError(f"Etapa '{etapa}' no reconocida")

    if aviso_peso:
        der *= INFRAPESO_AUMENTO

    resultado = {
        "rer": round(rer, 1),
        "coeficiente_kcal_kg075": round(coef, 1),
        "multiplicador_aplicado": round(der / rer, 3),   # informativo
        "der": round(der, 1),
        "metodo": "europeo",
    }
    if aviso_peso:
        resultado["aviso"] = aviso_peso
    if etapa == "lactante":
        resultado["requiere_veterinario"] = True
        resultado["aviso_lactancia"] = (
            "La lactancia es la etapa de mayor demanda de toda la vida de una "
            "perra y la que peor se estima con una fórmula. Este número es "
            "solo un punto de partida: pésala cada semana, ajusta según su "
            "condición corporal, y que lo supervise tu veterinario."
            + (" (Se ha aplicado el tope de seguridad.)" if locals().get("topada") else ""))
    return resultado


if __name__ == "__main__":
    print("=== CAIRO: 17 kg ahora, 32 kg de adulto, en crecimiento ===")
    print(calcular_der(17, "cachorro_crecimiento", peso_adulto_esperado_kg=32))
    print("\n=== Cairo de adulto, 32 kg, normal, Amstaff ===")
    print(calcular_der(32, "adulto", "normal", raza="American Staffordshire Terrier"))
    print("\n=== Lactante 25 kg con 6 cachorros, semana 3 ===")
    print(calcular_der(25, "lactante", n_cachorros=6, semana_lactancia=3))
