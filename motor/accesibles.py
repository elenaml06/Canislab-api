# -*- coding: utf-8 -*-
"""
ALIMENTOS FÁCILES DE ENCONTRAR EN ESPAÑA.

POR QUÉ EXISTE
--------------
El motor tenía todo el catálogo pero Claude le pasaba a mano una lista corta
("menú de pollo y ternera") y luego se extrañaba de que no usara pescado.
No era el motor descartando nada: es que nunca se le ofreció.

Ahora se le da TODO lo que se encuentra en un súper, una carnicería o una
pescadería normales, y él elige. Fuera queda lo que existe en el catálogo
pero no se compra fácil, o lo que se quitó del catálogo por seguridad o
por datos malos.

⚠️ ESTA LISTA SE DESACTUALIZÓ UNA VEZ (5 agosto): llevaba doce nombres de
alimentos que ya se habían quitado del catálogo por completo (huesos de
carga, cardo, berro, kiwi, tomate con datos de conserva...) y nadie la
había tocado desde entonces. `densidad.py` los seguía ofreciendo como
candidatos aunque no existieran de verdad. Se limpió a mano contra el
catálogo real y hay que MANTENERLA AL DÍA cada vez que se quite o añada
algo del catálogo — si no, este archivo vuelve a mentir.

Esto NO es una regla nutricional: es de sentido común de compra. Si un
menú necesita algo que no se encuentra fácil, no se va a preparar.
"""

CARNE = [
    "Pollo con piel (sin hueso)", "Pollo muslo con piel", "Pollo pechuga con piel",
    "Pollo muslo sin piel", "Pollo pechuga sin piel", "Pollo ala con piel (sin hueso)",
    "Pavo pechuga sin piel", "Pavo pechuga con piel", "Pavo muslo con piel", "Pavo",
    "Ternera solomillo sin grasa", "Lomo de ternera con grasa", "Ternera con grasa",
    "Conejo", "Pato (carne sin hueso)", "Gallina (carne sin hueso)",
    "Corazón de pollo", "Corazón de vaca", "Corazón de cordero", "Corazón de conejo",
    # ⚠️ AÑADIDO (5 agosto, madrugada): "Molleja de pollo" y "Molleja de
    # pavo" estaban en Vísceras -- corregido a Carne muscular, igual que
    # el corazón. En alimentación cruda, lo que separa víscera de carne
    # no es "es tejido muscular o es un órgano" (por ahí caímos en el
    # error), es si SEGREGA algo o no: la molleja tritura mecánicamente,
    # no segrega, así que va con la carne muscular -- igual que el
    # corazón, que bombea pero tampoco segrega.
    "Molleja de pollo", "Molleja de pavo",
    # ⚠️ AÑADIDO (5 agosto, madrugada) — segunda pasada, confirmado con
    # varias guías de raw feeding: la lengua TAMPOCO segrega, así que
    # también va con la carne muscular, no con las vísceras. Estaba mal
    # puesta igual que la molleja y el corazón.
    #
    # ⚠️ EL PULMÓN NO SE MUEVE (tercera pasada, mismo momento): a
    # diferencia de corazón/molleja/lengua, donde todas las fuentes
    # coinciden sin excepción, el pulmón es un caso genuinamente
    # debatido en la comunidad de alimentación cruda -- se deja en
    # Vísceras (abajo) por prudencia, sin consenso claro para moverlo.
    "Lengua de ternera", "Lengua de buey", "Lengua de cordero",
]

# Solo huesos que se piden sin problema en una carnicería normal.
# Pierna de cordero con hueso y Huesos de cuello de ternera se QUITARON del
# catálogo (riesgo de fractura dental, huesos de carga). Pecho de vacuno y
# Pecho de ternera con hueso también se quitaron (difíciles de conseguir).
HUESO = [
    "Carcasa de pollo", "Cuello de pavo", "Cuello de pato", "Carcasa de pato",
    "Costillas de cordero", "Carcasa de conejo",
    # ⚠️ AÑADIDO (5 agosto, noche): los dos con respaldo real del estudio
    # de Köber et al. 2017 (ESVCN) que la usuaria ya había pasado antes.
    # "Espinazo de conejo" ya tenía ficha completa pero nunca había
    # llegado a esta lista curada -- solo se podía usar a mano.
    "Espinazo de conejo", "Pecho de ternera con hueso",
    # ⚠️ AÑADIDO (5 agosto, noche) — segunda pasada por la tabla completa
    # del mismo estudio: "Cuello de ternera" es la fila que faltaba y
    # SÍ es segura (ratio Ca:P normal) Y fácil de conseguir.
    # "Escápula de vacuno" y "cartílago de vacuno" quedan fuera a
    # propósito: el propio estudio dice que su ratio Ca:P está invertido
    # y no son una buena fuente de calcio. "Pierna de cordero con hueso"
    # también queda fuera: ya se había excluido antes por riesgo de
    # fractura dental (hueso de carga), es una decisión de seguridad
    # tomada antes, no una falta de datos.
    "Cuello de ternera",
    # ⚠️ QUITADO (5 agosto, madrugada): "Laringe de vacuno" tenía datos
    # científicos reales, pero NO es un alimento que se consiga en una
    # carnicería normal -- es una pieza muy especializada, típicamente
    # solo en mataderos, no a la venta al público. El criterio de esta
    # lista es "fácil/seguro de encontrar", no solo "con buenos datos".
    # Se queda en el catálogo completo por si alguien la busca a mano
    # explícitamente (avisando de la dificultad), pero el automático ya
    # no la sugiere. Además, ya sabíamos que su calcio es demasiado
    # bajo (66mg/100g) para sostener Hueso carnoso ella sola.
]

PESCADO = [
    # ⚠️ CORREGIDO (5 agosto): se quitaron Sepia, Pulpo, Gamba roja,
    # Langostinos y Calamar. La propia app ya avisaba de esto en
    # INSTRUCCIONES_POR_CATEGORIA ("los mariscos, SIEMPRE cocinados"), pero
    # el motor los seguía eligiendo igual, sin distinguir pescado
    # (que sí puede darse crudo si se congela antes) de marisco/cefalópodo
    # (que necesita cocinarse siempre). La usuaria no quiere ningún
    # alimento en el menú que obligue a cocinar antes de dar.
    "Salmón", "Sardina", "Caballa", "Merluza", "Bacalao", "Lubina", "Dorada",
    "Trucha", "Atún", "Boquerón", "Lenguado", "Pescadilla", "Besugo",
    "Bacaladilla", "Perca",
]

VISCERAS = [
    "Riñón de ternera", "Riñón de cordero",
    # ⚠️ CORREGIDO (5 agosto, madrugada) — el pulmón vuelve aquí: a
    # diferencia de lengua/molleja/corazón (donde todas las fuentes
    # coinciden sin excepción), el pulmón es un caso genuinamente
    # debatido en la comunidad de alimentación cruda -- se deja por
    # prudencia, sin consenso claro para moverlo a Carne muscular.
    "Pulmón de ternera", "Pulmón de cordero",
    # ⚠️ AMPLIADO (5 agosto, madrugada) — investigación verificada con
    # múltiples fuentes cruzadas (USDA principalmente). "Bazo de
    # ternera" y "Páncreas de ternera" se renombraron a "de vaca": sus
    # datos originales eran de animal adulto (hierro muy alto, 44.5mg
    # -- propio de vaca, no de ternera lechal), no de ternera joven.
    # Confirmado que NO existen datos fiables de bazo/páncreas de
    # pollo, pavo ni conejo -- no se han añadido esas especies. En su
    # lugar, bazo/páncreas de cerdo y cordero, y timo/cerebro/
    # testículos (con datos USDA reales, cruzados con más de una
    # fuente cada uno) dan variedad real sin inventar ninguna cifra.
    "Bazo de vaca", "Páncreas de vaca",
    "Bazo de cerdo", "Bazo de cordero", "Páncreas de cerdo",
    "Timo de ternera", "Cerebro de ternera", "Testículos de cordero",
]

HIGADO = ["Hígado de vaca", "Hígado de pollo", "Hígado de conejo", "Hígado de cordero"]

# Berro se QUITÓ del catálogo (tóxico, clasificación ASPCA). Kiwi se quitó
# (riesgo mecánico + oxalato en semilla). Cardo se quitó (difícil de
# encontrar). Tomate (puré) se quitó (el dato tenía sodio/cloruro de
# conserva con sal, no de tomate fresco). Puerro no existe en el catálogo.
# Brócoli y Col lombarda ya están fusionados con sus duplicados.
# ⚠️ Dátil, Endibia y Grelo se QUITARON de aquí (5 agosto): más difíciles de
# encontrar que el resto. Pero SIGUEN en el catálogo entero: si el usuario
# los pide expresamente, se pueden usar igual. Solo no entran por defecto
# cuando el motor elige solo.
VERDURA = [
    "Zanahoria", "Calabaza", "Calabacín", "Judía verde", "Brócoli", "Acelga",
    "Espinaca", "Coliflor", "Coles de Bruselas", "Col rizada", "Col lombarda",
    "Repollo", "Pimiento rojo", "Pepino", "Lechuga", "Canónigos",
    "Rucula", "Apio", "Espárrago verde", "Alcachofa", "Berenjena", "Champiñón",
    "Nabo pelado", "Rábano", "Boniato", "Albahaca",
    "Manzana", "Pera", "Plátano", "Fresa", "Sandía", "Melón",
    "Naranja", "Mandarina", "Piña", "Mango", "Frambuesa", "Arándano",
    "Albaricoque",
]

ACCESIBLES = {
    "Carne muscular": CARNE,
    "Hueso carnoso": HUESO,
    "Pescados y mariscos": PESCADO,
    "Vísceras": VISCERAS,
    "Hígado": HIGADO,
    "Verduras y frutas": VERDURA,
}


def disponibles(alimentos, excluidos=None):
    """Lo accesible que además existe en el catálogo y no está excluido."""
    from exclusiones import filtrar
    salida = {}
    for cat, lista in ACCESIBLES.items():
        hay = [n for n in lista if n in alimentos]
        if excluidos:
            hay, _f, _a = filtrar(hay, excluidos)
        if hay:
            salida[cat] = hay
    return salida
