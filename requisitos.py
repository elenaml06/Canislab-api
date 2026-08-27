"""
REQUISITOS: cargar la tabla de FEDIAF, resolver la etapa y la dosis
maxima que marca el fabricante de cada suplemento.

⚠️ DE DONDE SALE ESTE ARCHIVO (26 agosto). Era `optimizador.py`, 1.124
lineas donde convivian DOS COSAS que no tienen nada que ver:

  · `optimizar_menu()` y `_resolver_lp()`: el motor ANTERIOR al MILP,
    con su propia tabla de patologias y su propio mapa de requisitos.
    Solo lo usaba el endpoint /menu, que el frontend no llama.
  · Estas cuatro utilidades, que si usan el motor vivo y el analizador.

Estaban en el mismo archivo, asi que desde fuera no habia forma de saber
cual era cual -- y la copia vieja de la tabla de patologias llevaba
semanas desincronizada de la de verdad: fosforo renal a 1.400 en vez de
1.200, cobre en hepatopatia a 3,0 en vez de 2,4 y sin bloquear, grasa en
pancreatitis al 25% de las kcal en vez de 20 g/1000 kcal, diabetes
bajando la grasa siempre en vez de solo con pancreatitis, y urato,
cistinuria y "otra" sin existir, o sea sin bloquear nada.

No causaba menus malos porque `_garantizar_verificado()` los comprobaba
otra vez contra las tablas de verdad antes de entregarlos -- pero tener
dos tablas clinicas y que la segunda mienta es justo lo que este
proyecto no se puede permitir. El motor viejo y sus copias se han
borrado; la unica tabla de patologias es la de `motor/motor_completo.py`
y el unico mapa de requisitos es `verificar.MAPA`.
"""
import json


def cargar_requerimientos(path="requerimientos_v2_final.json"):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# =====================================================================
# EQUIVALENCIA DE ETAPAS (segun como las agrupa FEDIAF)
# =====================================================================
# La app ofrece 6 etapas pero requerimientos_v2_final.json solo tiene
# columnas para 3. No es un hueco que haya que rellenar inventando datos:
# FEDIAF NO define tablas separadas para gestacion, lactancia ni senior.
#   - Gestacion y lactancia: FEDIAF las agrupa junto al crecimiento en una
#     unica categoria "Growth and Reproduction" (AAFCO hace lo mismo). Se
#     entiende bien: en los tres casos el animal esta construyendo tejido
#     nuevo y necesita el mismo perfil reforzado.
#   - Senior: FEDIAF no le da tabla propia; usa la de adulto. La unica
#     particularidad documentada es subir la proteina para cubrir a los
#     perros mayores (FEDIAF eleva la RA de 40 a 45 g/1000kcal por este
#     motivo), lo que se aplica abajo con SENIOR_PROTEINA_MINIMA.
EQUIVALENCIA_ETAPAS = {
    "Gestante": "CachorroCrecimiento",   # Growth and Reproduction
    "Lactante": "CachorroCrecimiento",   # Growth and Reproduction
    "Senior": "Adulto",                  # sin tabla propia en FEDIAF
}
# FEDIAF sube la proteina recomendada para perros mayores (40 -> 45
# g/1000kcal). Si nuestro valor de adulto ya es mas alto, se respeta el
# nuestro y esto no hace nada.
SENIOR_PROTEINA_MINIMA = 45.0


# Las UNICAS etapas que existen en requerimientos_v2_final.json. Cualquier
# otra cosa es un error de quien llama, y hay que gritarlo.
ETAPAS_VALIDAS = {"Adulto", "CachorroJoven", "CachorroCrecimiento"}


# Frutas de nuestro catalogo. El JSON no distingue fruta de verdura (todo cae
# en "Verduras y frutas"), asi que se separan por nombre. Si se anaden frutas
# nuevas al catalogo hay que meterlas aqui tambien.

def resolver_etapa(etapa_pedida):
    """
    Devuelve la etapa cuyos requisitos hay que usar realmente.

    ⚠️ FALLA A PROPOSITO si la etapa no existe. Antes no lo hacia, y eso
    causo un fallo real: el frontend mandaba "cachorro_crecimiento" (la clave
    de der.py) en vez de "CachorroCrecimiento" (la de los requisitos). Como
    los requisitos se buscan con f"min{etapa}", NINGUNA columna coincidia, no
    se comprobaba NI UN nutriente, y el analizador respondia que la dieta
    estaba perfecta cuando le faltaban 15 nutrientes.
    Un fallo silencioso en la base es mucho peor que un error visible.
    """
    etapa = EQUIVALENCIA_ETAPAS.get(etapa_pedida, etapa_pedida)
    if etapa not in ETAPAS_VALIDAS:
        raise ValueError(
            f"Etapa de requisitos '{etapa_pedida}' no reconocida. "
            f"Las validas son: {sorted(ETAPAS_VALIDAS)}. "
            f"Cuidado: las claves de der.py (adulto, cachorro_crecimiento...) "
            f"NO son las mismas que las de los requisitos.")
    return etapa


def _valor_o_none(v):
    if v is None or v == "-" or v == "":
        return None
    return float(v)



def dosis_maxima_fabricante(alimento: dict, peso_perro_kg: float):
    """Gramos maximos al dia que el FABRICANTE recomienda de ese suplemento,
    segun el peso del perro. None si el producto no trae tabla de dosis."""
    # (a) dosis lineal: g por kg de peso corporal (aceites, algas, levadura)
    por_kg = alimento.get("dosis_g_por_kg_peso")
    if por_kg and peso_perro_kg is not None:
        return por_kg * peso_perro_kg

    # (a2) algunos productos ademas tienen un tope absoluto ("maximo N
    #      cucharaditas al dia") que manda sobre el calculo por peso
    tope_abs = alimento.get("dosis_max_absoluta_g")
    if por_kg and peso_perro_kg is not None and tope_abs:
        return min(por_kg * peso_perro_kg, tope_abs)

    # (b) dosis por tramos de peso (multivitaminicos, harinas de hueso)
    tramos = alimento.get("dosis_tramos_kg")
    if not tramos or peso_perro_kg is None:
        return None
    for t in tramos:
        if t["hasta_kg"] is None or peso_perro_kg <= t["hasta_kg"]:
            return t["gramos"]
    return tramos[-1]["gramos"]

