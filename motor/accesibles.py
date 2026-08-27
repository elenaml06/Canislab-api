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
    "Corazón de pollo", "Corazón de pavo", "Corazón de vaca", "Corazón de cordero",
    "Corazón de conejo",
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
    "Bazo de cordero", 
    "Timo de ternera", "Cerebro de ternera",
    # ⚠️ QUITADO "Testículos de cordero" (27 agosto). Estaba aqui desde el
    # 21 de agosto "con datos USDA reales", y esa frase era la que fallaba:
    # de sus 31 nutrientes, 30 estaban a CERO. Solo tenia la vitamina B12
    # -- 9,89 ug, de las mas altas del catalogo -- y 68 kcal con proteina 0
    # y grasa 0, o sea una fila que se contradice a si misma, porque esa
    # energia no puede salir de ningun sitio.
    # Para el solver era vitamina B12 GRATIS: no costaba nada en ningun
    # otro presupuesto. MEDIDO antes de quitarlo: salia en 2 de cada 24
    # menus automaticos, uno de ellos con 90,5 gramos, y cada uno de esos
    # gramos dejaba la racion corta de todo lo demas con el semaforo en
    # VERDE, porque el semaforo verifica contra estos mismos datos.
    # Ninguna de las dos defensas lo veia: `sin_dato` estaba vacio, asi que
    # no salia en `datos_incompletos`, y la ficha estaba "documentada", asi
    # que la regla de no sobrescribir lo documentado la protegia.
    # Si vuelve algun dia, que vuelva con datos. Lo vigila el BLOQUE 29.
]

# ⚠️ AMPLIADO (21 agosto) — el hígado era el cuello de botella medido por
# auditar_catalogo.py: con 3 alergias solo quedaban 2 hígados disponibles, y
# el hígado es una categoría con mínimo obligatorio, así que quedarse sin
# ninguno deja al perro sin menú. Con pavo y pato pasa de 2 a 4.
HIGADO = ["Hígado de vaca", "Hígado de pollo", "Hígado de pavo", "Hígado de pato",
          "Hígado de conejo", "Hígado de cordero"]

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

# =====================================================================
# ⚠️ REESCRITO (27 agosto): ACCESIBLES YA NO ES UNA LISTA A MANO
# =====================================================================
# Todo lo de arriba son las listas historicas, y se quedan SOLO como
# documentacion de por que cada alimento estaba donde estaba. Ya no las
# lee nadie.
#
# El motivo del cambio esta escrito en la cabecera de este mismo archivo:
# "esta lista se desactualizo una vez (5 agosto): llevaba doce nombres de
# alimentos que ya se habian quitado del catalogo y nadie la habia
# tocado". Mientras la lista de lo que el motor puede usar viva en un
# sitio distinto del catalogo, va a volver a desincronizarse -- y la
# proxima vez tampoco habra nadie mirando.
#
# Ahora la marca vive EN LA FICHA DEL ALIMENTO, en el campo
# `accesible_es`, y ACCESIBLES se construye leyendo el catalogo. No hay
# dos sitios que mantener al dia, y anadir un alimento no puede olvidarse
# de nada: si la ficha no dice `accesible_es`, no es accesible.
#
# Lo vigila el BLOQUE 31.
import json as _json
import os as _os

_RAIZ = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "..")


def _construir_accesibles():
    ruta = _os.path.join(_RAIZ, "alimentos_v3_final.json")
    with open(ruta, encoding="utf-8") as f:
        catalogo = _json.load(f)
    salida = {}
    for a in catalogo:
        if a.get("accesible_es") != "si":
            continue
        # ⚠️ Y ADEMAS `preferente`: una ficha por PRODUCTO REAL, no una por
        # entrada de tabla. Las catorce fichas de carne picada de vacuno
        # (5%, 7%, 9%, 10%, 13%, 15%, 17%, 25%, 30%...) son un producto,
        # no catorce. Metiendolas todas al solver no se gana ni un
        # nutriente: se gana que elija una al azar entre catorce casi
        # iguales, y que el problema sea mas grande sin motivo.
        # Las demas siguen en el catalogo y en Personalizar, para quien
        # quiera justo la del 5%.
        if a.get("preferente") == "no":
            continue
        cat = a.get("categoria")
        # Las categorias de suplemento y los Extras NO van aqui: el solver
        # los mete por su propio camino (ver SUP_CATS en motor_completo).
        # Aqui solo van las categorias de COMIDA que forman la plantilla.
        if cat in ("Carne muscular", "Hueso carnoso", "Pescados y mariscos",
                   "Vísceras", "Hígado", "Verduras y frutas"):
            salida.setdefault(cat, []).append(a["nombre"])
    return salida


ACCESIBLES = _construir_accesibles()


def es_accesible(alimento):
    """Si el motor puede usar este alimento en un menu AUTOMATICO.

    Sirve para las categorias que no pasan por ACCESIBLES -- los Extras y
    los suplementos -- que hasta el 27 de agosto entraban TODOS sin
    filtro. Con 22 Extras daba igual; con 150 ya no: los lacteos y los
    frutos secos que entraron con la carga estan a proposito fuera del
    menu automatico, y sin esto se colarian solos.
    """
    return (alimento or {}).get("accesible_es") == "si"


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
