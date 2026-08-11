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
    # varias guías de raw feeding: la lengua y el pulmón TAMPOCO
    # segregan, así que también van con la carne muscular, no con las
    # vísceras. Estaban mal puestos igual que la molleja y el corazón.
    "Lengua de ternera", "Lengua de buey", "Lengua de cordero",
    "Pulmón de ternera", "Pulmón de cordero",
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
    # del mismo estudio: "Cuello de ternera" y "Laringe de vacuno" son
    # las dos filas que faltaban y SÍ son seguras (ratio Ca:P normal).
    # "Escápula de vacuno" y "cartílago de vacuno" quedan fuera a
    # propósito: el propio estudio dice que su ratio Ca:P está invertido
    # y no son una buena fuente de calcio. "Pierna de cordero con hueso"
    # también queda fuera: ya se había excluido antes por riesgo de
    # fractura dental (hueso de carga), es una decisión de seguridad
    # tomada antes, no una falta de datos.
    "Cuello de ternera", "Laringe de vacuno",
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
    # ⚠️ AVISO IMPORTANTE (5 agosto, madrugada): tras mover lengua y
    # pulmón a Carne muscular (misma razón que la molleja y el corazón:
    # no segregan), esta categoría se queda SOLO con riñón -- no
    # tenemos datos de bazo, páncreas, testículos ni cerebro (las
    # otras vísceras secretoras reales) para ampliarla. Consecuencia
    # real: si alguien excluye a la vez "Ternera" y "Cordero" (dos
    # alergias comunes), Vísceras se queda sin ningún candidato, y la
    # red de seguridad ya puesta hará que el sistema diga claramente
    # que no puede (en vez de mentir con un menú sin víscera, que es
    # lo que hacía antes de esa red). Es correcto, pero más frágil que
    # antes. Si se consiguen datos fiables de bazo o páncreas, esto
    # mejoraría mucho.
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
