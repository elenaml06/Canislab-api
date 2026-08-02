"""
CANISLAB - Plantillas base validadas

POR QUE EXISTE ESTO
El motor sabe generar menus desde cero, pero cada tirada es una combinacion
nueva que nadie ha revisado, y eso hace que de vez en cuando salga algo raro
(se vieron 262 g de trucha en un perro de 17 kg). Los formuladores
profesionales trabajan al reves: una receta fija, validada una vez, que se
repite. Eso es mas seguro pero aburre al perro y no aprovecha la variedad.

Aqui se hace el hibrido que acordamos: un conjunto pequeño de plantillas
que YA se han comprobado que funcionan, entre las que se rota, y que el
motor escala en gramos al perro concreto. Asi hay variedad y a la vez cada
menu viene de una receta conocida.

Cada plantilla define QUE alimentos lleva. Los GRAMOS los sigue calculando
el optimizador con todas sus restricciones de seguridad, asi que la
plantilla nunca puede saltarselas: si una plantilla no cuadra para un perro
concreto, se descarta y se prueba la siguiente.
"""

# Cada plantilla es una lista de alimentos. Se han elegido buscando que
# entre todas haya variedad de especie (por rotacion) y que cada una tenga
# lo necesario: proteina, fuente de calcio, omega-3, verdura y el premix.
# --- COMPACTAS: la estructura BARF completa, con los alimentos justos ---
# Llevan los cinco pilares (hueso carnoso, carne/pescado, verdura, visceras,
# higado) porque esa estructura no es negociable, mas 2 suplementos que
# COMPENSAN lo que la comida no cubre (omega-3 y micronutrientes).
# Se apoyan en los suplementos comerciales para cubrir calcio (harina de
# hueso), omega-3 (aceite de salmon) y micronutrientes (multivitaminico),
# igual que hacen los formuladores profesionales. Comprobado que 7 es el
# minimo posible: con menos hay que meter cantidades que rompen algun
# limite de seguridad (con 6 salian 449 g de acelga, muy por encima del
# tope de oxalatos).
COMPACTAS = [
    {
        "id": "compacta-conejo",
        "nombre": "Sencilla de conejo",
        "descripcion": "Estructura BARF completa con carne blanca de conejo.",
        "compacta": True,
        "alimentos": [
            "Conejo", "Corazón de vaca",
            "Carcasa de conejo",
            "Riñón de ternera", "Hígado de conejo",
            "Caballa", "Calabaza", "Judía verde",
            "AniForte Aceite de Salmón",
            "Homemadekun (multivitamínico completo)",
        ],
    },
]

PLANTILLAS = COMPACTAS + [
    {
        "id": "ternera-sardina",
        "nombre": "Ternera y sardina",
        "descripcion": "Base de ternera con sardina como fuente de omega-3.",
        "alimentos": [
            "Ternera con grasa", "Corazón de vaca", "Ternera solomillo sin grasa",
            "Pecho de ternera con hueso", "Costillas de ternera", "Rabo de toro",
            "Riñón de ternera", "Pulmón de ternera", "Hígado de vaca",
            "Sardina", "Merluza",
            "Calabaza", "Zanahoria", "Judía verde",
            "Aceite de girasol",
            "Homemadekun (multivitamínico completo)",
        ],
    },
    {
        "id": "conejo-caballa",
        "nombre": "Conejo y caballa",
        "descripcion": "Carne blanca de conejo, suave de digerir.",
        "alimentos": [
            "Conejo", "Corazón de cordero", "Ternera solomillo sin grasa",
            "Carcasa de conejo", "Costillas de cordero", "Patas de conejo",
            "Riñón de cordero", "Pulmón de cordero", "Hígado de conejo",
            "Caballa", "Merluza",
            "Calabacín", "Judía verde", "Zanahoria",
            "Aceite de girasol",
            "Homemadekun (multivitamínico completo)",
        ],
    },
    {
        "id": "cordero-salmon",
        "nombre": "Cordero y salmón",
        "descripcion": "Cordero con salmón, alta en omega-3.",
        "alimentos": [
            "Corazón de cordero", "Ternera solomillo sin grasa", "Ternera con grasa",
            "Costillas de cordero", "Espinazo de cordero", "Cuello de cordero",
            "Riñón de cordero", "Pulmón de cordero", "Hígado de vaca",
            "Salmón", "Merluza",
            "Zanahoria", "Brócoli", "Calabaza",
            "Aceite de girasol",
            "Homemadekun (multivitamínico completo)",
        ],
    },
    {
        "id": "pollo-trucha",
        "nombre": "Pollo y trucha",
        "descripcion": "Base de pollo, la opción más económica.",
        "alimentos": [
            "Pollo muslo con piel", "Pollo pechuga con piel",
            "Carcasa de pollo", "Cuello de pollo",
            "Riñón de ternera", "Hígado de pollo",
            "Trucha",
            "Calabaza", "Manzana",
            "Aceite de girasol",
            "Homemadekun (multivitamínico completo)",
        ],
    },
    {
        "id": "pavo-boqueron",
        "nombre": "Pavo y boquerón",
        "descripcion": "Pavo magro con boquerón.",
        "alimentos": [
            "Pavo pechuga sin piel", "Corazón de vaca",
            "Cuello de pavo", "Ala de pavo",
            "Pulmón de ternera", "Hígado de vaca",
            "Boquerón",
            "Calabacín", "Pera",
            "Aceite de girasol",
            "Homemadekun (multivitamínico completo)",
        ],
    },
    {
        "id": "ternera-merluza",
        "nombre": "Ternera y merluza",
        "descripcion": "Ternera con pescado blanco, baja en grasa.",
        "alimentos": [
            "Ternera solomillo sin grasa", "Lomo de ternera con grasa",
            "Costillas de ternera", "Rabo de toro",
            "Lengua de ternera", "Hígado de vaca",
            "Merluza", "Sardina",
            "Judía verde", "Zanahoria",
            "Aceite de girasol",
            "Homemadekun (multivitamínico completo)",
        ],
    },
    {
        "id": "mixta-conejo-ternera",
        "nombre": "Conejo y ternera",
        "descripcion": "Mezcla de dos especies, buena para rotar.",
        "alimentos": [
            "Conejo", "Ternera con grasa", "Corazón de vaca",
            "Pecho de ternera con hueso", "Carcasa de conejo", "Costillas de ternera",
            "Riñón de ternera", "Pulmón de ternera", "Hígado de conejo",
            "Caballa", "Merluza",
            "Calabaza", "Brócoli", "Zanahoria",
            "Aceite de girasol",
            "Homemadekun (multivitamínico completo)",
        ],
    },
]


def plantillas_compatibles(especies_excluidas: set, catalogo: dict, solo_compactas: bool = False):
    """Plantillas que no llevan ninguna especie excluida y cuyos alimentos
    existen todos en la base. Devuelve la lista filtrada."""
    especies_excluidas = especies_excluidas or set()
    validas = []
    for p in PLANTILLAS:
        if solo_compactas and not p.get("compacta"):
            continue
        alimentos = [catalogo.get(n) for n in p["alimentos"]]
        if any(a is None for a in alimentos):
            continue  # la plantilla nombra algo que ya no esta en la base
        if any(a.get("especie") in especies_excluidas for a in alimentos):
            continue  # el perro es alergico a algo de esta plantilla
        validas.append(p)
    return validas
