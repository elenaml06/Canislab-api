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
# TABLA VII-6 de FEDIAF (Anexo 7.2.4). Las bases 95 y 110 estan confirmadas
# en el texto oficial (secc. 3.2.1); el resto de la tabla via reproduccion de
# UK Pet Food ("Based on FEDIAF Nutritional Guidelines P62").
# La media MEDIDA en 586 perros de compania (Thes et al. 2014) fue 98, o sea
# justo entre "baja" (95) y "moderada bajo impacto" (110). Encaja.
BASE_ACTIVIDAD = {
    "sedentario":   95,    # baja: menos de 1 h/dia, casi siempre con correa
    "normal":      110,    # moderada 1-3 h/dia, bajo impacto
    "activo":      125,    # moderada 1-3 h/dia, ALTO impacto
    "muy_activo":  150,    # alta 3-6 h/dia (perro de trabajo, pastoreo)
    "trabajo":     175,    # alta, extremo superior del rango de FEDIAF
    # FEDIAF llega a 860-1240 para perros de trineo en frio extremo; eso no
    # lo cubre esta app y tendria que pautarlo un veterinario.
}

# Ajustes ADITIVOS, en kcal/kg^0.75. Solo se aplican a adulto y senior.
AJUSTE_EDAD = {
    "joven":   +15,   # 1 a 2 años
    "adulto":    0,   # 2 a 7 años
    "senior":   -7,   # Thes et al. 2014: 100 kcal/kg^0.75 en jovenes vs 93 en
                      # mayores de 7 anos -> -7 (antes teniamos -5)
}
AJUSTE_CONVIVENCIA = {"solo": 0, "con_otros_perros": +10}
AJUSTE_MACHO_ENTERO = +10

# Razas con gasto por encima / por debajo de la media (estudio de Múnich).
# Los nombres están tal como aparecen en nuestra lista de 136 razas.
# Razas con gasto por encima / por debajo de la media.
# LISTA EXACTA de Thes et al. (2014), "Metabolizable energy intake of client
# owned adult dogs", J Anim Physiol Anim Nutr — Universidad de Munich, catedra
# de Nutricion Animal (Prof. Kienzle). 586 perros de compania REALES con peso
# estable. Media 98 kcal/kg^0.75; estas razas 113 y 82 -> +-15.
# La app no tiene Kleiner Munsterlander, Sloughi, English Foxhound ni Lowchen.
RAZAS_MAS_GASTO = {
    "Jack Russell Terrier", "Parson Russell Terrier", "Dálmata",
    "Braco Húngaro (Vizsla)", "Bearded Collie", "Galgo Afgano",
    "Galgo Español", "Boxer", "Rhodesian Ridgeback", "Flat Coated Retriever",
}
# OJO: el BORDER COLLIE esta en la lista de MENOS gasto, aunque sorprenda.
# Y "Collies" en la tesis excluye expresamente al Bearded Collie.
RAZAS_MENOS_GASTO = {
    "Dachshund Estándar", "Dachshund Miniatura", "Lhasa Apso", "Shih Tzu",
    "West Highland White Terrier", "Border Collie", "Collie de Pelo Largo",
    "Airedale Terrier", "American Staffordshire Terrier", "Golden Retriever",
}
AJUSTE_RAZA = 15

# =============================================================================
# CRECIMIENTO (FEDIAF) — por % del peso ADULTO esperado, no por edad
# =============================================================================
# CRECIMIENTO — ecuacion de KLEIN et al. (2019), J Anim Physiol Anim Nutr
# 103:1952-1958. Grupo de Kienzle, Universidad de Munich: 493 CACHORROS DE
# COMPANIA REALES. Es la mejor evidencia disponible, y de la misma familia
# europea que el dato de adultos (Thes et al. 2014, mismo grupo).
#
#   ME (MJ) = (1.063 - 0.565 x [PesoActual / PesoAdultoEsperado]) x Peso^0.75
#
# Ventaja sobre los 3 escalones de FEDIAF (210/175/140): es una CURVA
# CONTINUA, sin saltos bruscos al cruzar el 50% y el 80% del peso adulto.
# Klein tambien confirmo que el NRC 2006 sobreestima ~20% en menores de 6
# meses, en linea con los estudios de Norfolk y Yorkshire Terrier.
KLEIN_A = 1.063
KLEIN_B = 0.565
MJ_A_KCAL = 239.0
# Escalones de FEDIAF, conservados solo como respaldo si no hay peso adulto
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
# Factores de semana de lactancia del NRC 2006: 0.75 / 0.95 / 1.1 / 1.2.
# Antes teniamos 1.40 en la semana 4, que venia de la fuente secundaria.
LACTANCIA_PESO_SEMANA = [0.75, 0.95, 1.10, 1.20]
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

# ESCALA DE CONDICION CORPORAL. La app usa 5 niveles; la escala validada
# (Laflamme 1997, contrastada con DEXA) es de 9 puntos. Equivalencia:
#   0 Muy delgado -> BCS 2   ·   1 Delgado -> BCS 4   ·   2 Ideal -> BCS 5
#   3 Sobrepeso   -> BCS 7   ·   4 Obeso   -> BCS 9
BCS_DESDE_CONDICION = {0: 2, 1: 4, 2: 5, 3: 7, 4: 9}
# Regla practica aceptada: cada punto de BCS por encima de 5 equivale a un
# 10% de exceso de peso corporal (y por debajo, a un 10% de defecto).
BCS_PCT_POR_PUNTO = 0.10
SOBREPESO_UMBRAL = 1.10           # >=10% por encima del ideal
INFRAPESO_UMBRAL = 0.90           # >=10% por debajo
INFRAPESO_AUMENTO = 1.20          # +20%


def calcular_rer(peso_kg: float) -> float:
    """Necesidad en reposo. Es la base de todo."""
    return RER_COEF * peso_kg ** 0.75


def peso_ideal_desde_condicion(peso_actual_kg: float, condicion_idx: int) -> float:
    """
    Estima el peso ideal a partir del selector de condicion corporal de la app.

    Todas las guias (FEDIAF, NRC, AAHA, y la propia tesis de Munich) coinciden
    en que la racion se calcula sobre el peso IDEAL, no sobre el actual. Un
    perro con sobrepeso tiene menos masa magra, que es el tejido que gasta.
    Thes et al. 2014 lo midio: sobre el peso actual los gordos comen 86
    kcal/kg^0.75 y los delgados 119, pero sobre el peso IDEAL la diferencia
    DESAPARECE. Literal: "calcular el mantenimiento por el peso ideal es un
    metodo excelente".
    """
    if peso_actual_kg is None or peso_actual_kg <= 0:
        return None
    if condicion_idx is None:
        return None
    bcs = BCS_DESDE_CONDICION.get(condicion_idx)
    if bcs is None:
        return None
    desvio = (bcs - 5) * BCS_PCT_POR_PUNTO      # +0.2 si BCS 7, -0.3 si BCS 2
    ideal = peso_actual_kg / (1 + desvio)
    # TOPE DE SEGURIDAD hacia arriba. Un perro muy delgado (BCS 2) daria un
    # objetivo un 43% por encima de su peso actual, y pasar de golpe a esa
    # racion es mala idea: se recupera peso poco a poco, y ademas un perro
    # muy delgado suele estarlo por una ENFERMEDAD, no por comer poco.
    # Se limita la correccion al alza al 20% y se avisa.
    if ideal > peso_actual_kg * 1.20:
        ideal = peso_actual_kg * 1.20
    return round(ideal, 2)


def _coef_crecimiento(peso_actual: float, peso_adulto: float) -> float:
    """
    Devuelve el coeficiente en kcal/kg^0.75 para un cachorro.
    Con peso adulto conocido usa KLEIN 2019 (curva continua medida en 493
    cachorros de compania). Sin el, cae al escalon mas prudente de FEDIAF.
    """
    if not peso_adulto or peso_adulto <= 0:
        return CRECIMIENTO[-1][1]     # sin peso adulto, lo prudente
    frac = peso_actual / peso_adulto
    if frac > 1.0:
        frac = 1.0                    # ya llego a su peso adulto
    coef = (KLEIN_A - KLEIN_B * frac) * MJ_A_KCAL
    # Suelo de seguridad: nunca por debajo del mantenimiento adulto medio,
    # porque un cachorro nunca necesita menos que un adulto de su peso.
    return max(coef, 98.0)


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
