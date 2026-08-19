# -*- coding: utf-8 -*-
"""
EL MOTOR DE VERDAD — una sola pregunta, no miles de intentos con nombres fijos.

POR QUÉ ESTE ARCHIVO EXISTE
-----------------------------
Toda la noche del 4→5 de agosto se probó: elegir a mano, elegir por
densidad con una sola pasada, comparar unas pocas combinaciones,
enumerar miles de combinaciones con nombres fijos ("menú de pollo",
"menú de pollo y sardina"...). La usuaria lo dijo claro:
    "no pruebes con menú de pollo... que saques menús viables, y si el
     menú es de cordero con pollo, pues cordero con pollo, con lo que
     salga"
Fijar la carne y el hueso de antemano y luego probar variantes alrededor
es la pregunta equivocada. La pregunta correcta es UNA SOLA:
    "de TODOS los alimentos disponibles, ¿cuál es la mejor combinación
     posible — qué alimentos Y cuánto de cada uno — que cumple los 30
     requisitos con máximo 2 suplementos?"

Eso es un problema de PROGRAMACIÓN LINEAL ENTERA MIXTA (MILP): unas
variables son continuas (cuántos gramos) y otras son binarias (¿se usa
este alimento sí/no?), porque hay que LIMITAR CUÁNTOS alimentos distintos
se usan por categoría (máx. 3 carnes, máx. 2 suplementos...), y eso no
se puede expresar solo con gramos.

`scipy.optimize.milp` lo resuelve de forma EXACTA: si existe una
combinación que funciona, la encuentra. Si no existe, lo dice con
certeza matemática, no porque no se haya probado lo suficiente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from verificar import MAPA, _num, EQUIVALENCIA

# ⚠️ AÑADIDO (5 agosto, noche): copia local de especie_de() (la misma
# lógica que ya usan especies.py y el frontend) -- se define aquí en
# vez de importarla desde la carpeta raíz, para no depender de cómo
# esté configurado el path de imports en el despliegue real.
def especie_de(nombre: str) -> str:
    if " de " in nombre:
        resto = nombre.split(" de ", 1)[1]
        return resto.split(" ")[0].capitalize()
    return nombre.split(" ")[0]

# ⚠️ AÑADIDO (5 agosto, noche): esta tabla YA EXISTÍA en optimizador.py
# (el LP viejo) -- se acordó con la usuaria el 1 de agosto y nunca se
# portó al motor nuevo. Por eso las patologías no hacían nada: la app
# seguía preguntando y mandando el dato, pero resolver() lo ignoraba.
# Se porta tal cual, sin cambiar ningún valor.
PATOLOGIAS = {
    "renal": {"max_por_1000kcal": {"fosforo": 1400.0},
        "aviso": ("Se ha bajado el fósforo todo lo posible sin bajar del mínimo "
                  "nutricional de un perro sano. IMPORTANTE: una dieta renal "
                  "terapéutica de verdad baja el fósforo POR DEBAJO de ese mínimo, "
                  "y eso solo puede pautarlo tu veterinario. Esto es un apoyo, "
                  "no sustituye una dieta renal prescrita.")},
    "pancreatitis": {"max_pct_kcal_grasa": 0.25,
        "aviso": ("Se ha bajado la grasa al 25% de las calorías. En pancreatitis "
                  "la tolerancia a la grasa es muy individual: ajústalo con tu "
                  "veterinario según cómo responda.")},
    "oxalato": {"max_por_1000kcal": {"vitD": 20.0},
        "aviso": ("Ojo: en oxalato NO hay que bajar el calcio (bajarlo aumenta la "
                  "absorción de oxalato y empeora). Lo importante es el agua y "
                  "evitar verduras muy ricas en oxalato como la espinaca o la acelga.")},
    "hepatopatia": {"max_por_1000kcal": {"cobre": 3.0},
        "aviso": ("Se ha limitado el cobre, clave en las hepatopatías por acúmulo. "
                  "Si hay encefalopatía hepática hace falta además ajustar la "
                  "proteína, y eso lo tiene que pautar tu veterinario.")},
    "cardiopatia": {"max_por_1000kcal": {"sodio": 900.0},
        "aviso": ("Se ha bajado el sodio. En cardiopatía avanzada puede hacer falta "
                  "bajarlo más y vigilar el potasio si toma diuréticos: consúltalo.")},
    "diabetes": {"max_pct_kcal_grasa": 0.35, "excluye_fruta": True,
        "aviso": ("Lo más importante en diabetes no es el menú sino la REGULARIDAD: "
                  "misma cantidad, a la misma hora, coordinada con la insulina. "
                  "Se ha quitado la fruta del menú: su azúcar se absorbe rápido y "
                  "descuadra la pauta de insulina. La verdura fibrosa sí se "
                  "mantiene, porque ayuda a amortiguar la subida de glucosa.")},
    "hipotiroidismo": {
        "aviso": ("No se cambia la composición. Pero evita darle cuello de rumiante "
                  "grande de forma repetida: puede llevar restos de tejido tiroideo "
                  "y alterar los valores de la analítica.")},
    "estruvita": {"sin_dieta_automatica": True,
        "aviso": ("Estos cálculos dependen del pH de la orina y de analíticas que la "
                  "app no puede ver. Una dieta mal ajustada aquí puede empeorarlos, "
                  "así que no generamos menú automático: necesitas una dieta pautada "
                  "por tu veterinario.")},
    # ⚠️ CONECTADO (5 agosto, madrugada) — CASO REAL ENCONTRADO, pedido
    # expreso: "urato" no tenía sin_dieta_automatica, así que el sistema
    # intentaba generar un menú excluyendo hígado y las vísceras/pescado
    # con purinas altas -- y con el catálogo actual, esa combinación es
    # matemáticamente imposible de verdad (confirmado probándolo
    # directamente con el solver, no es un bug de código): el hígado
    # aporta la mayoría de la vitamina A disponible, y sin él ni sin
    # riñón no queda margen real para cumplir el resto de los 30
    # requisitos a la vez. Antes esto se traducía en "no hay ninguna
    # combinación posible" sin explicación -- ahora se bloquea con el
    # mismo mensaje claro que estruvita, en vez de fallar en silencio.
    # "cistina" tiene el mismo mecanismo clínico (predisposición a
    # urolitos que requiere analíticas y control veterinario) y nunca
    # había llegado a añadirse a este diccionario en absoluto.
    "urato": {"sin_dieta_automatica": True,
        "aviso": ("La predisposición a urolitos de urato (dálmata, shunt hepático) "
                  "necesita restringir tanto las purinas que, con alimentos frescos "
                  "normales, no queda margen real para cubrir el resto de nutrientes "
                  "a la vez -- por eso no generamos menú automático aquí: esto "
                  "necesita una dieta pautada por tu veterinario, a menudo con "
                  "pienso terapéutico específico.")},
    "cistina": {"sin_dieta_automatica": True,
        "aviso": ("Igual que con estruvita, esto depende del pH de la orina y de "
                  "analíticas que la app no puede ver -- no generamos menú "
                  "automático: necesitas una dieta pautada por tu veterinario.")},
    # ⚠️ AÑADIDO (5 agosto, madrugada) — pedido expreso: antes, si el
    # perro tenía una patología que no está en esta lista, no había
    # ninguna forma de decirlo -- la persona se quedaba con la duda de
    # si su caso necesitaba también adaptar la dieta. Igual que
    # estruvita, esto BLOQUEA de verdad la generación automática (no es
    # solo un aviso visual en el frontend que se pudiera saltar) --
    # porque no hay ninguna regla nutricional conocida en este sistema
    # para una condición sin especificar, así que fingir haberla
    # ajustado sería peor que no generar nada.
    "otra": {"sin_dieta_automatica": True,
        "aviso": ("Esta condición no está entre las que este sistema sabe ajustar "
                  "automáticamente todavía, así que no generamos un menú que podría "
                  "no estar realmente adaptado a lo que necesita: mejor que un "
                  "veterinario valore su caso en concreto y paute la dieta.")},
}

FRUTAS = {"Manzana", "Pera", "Plátano", "Fresa", "Sandía", "Melón", "Naranja",
         "Mandarina", "Piña", "Mango", "Frambuesa", "Arándano", "Albaricoque", "Dátil"}


def patologias_bloquean(patologias):
    """Las que impiden generar dieta automática (dependen de analíticas)."""
    return [p for p in (patologias or []) if PATOLOGIAS.get(p, {}).get("sin_dieta_automatica")]


def avisos_de_patologias(patologias):
    return [PATOLOGIAS[p]["aviso"] for p in (patologias or []) if p in PATOLOGIAS]


def resolver(der, etapa, alimentos, req, peso_perro_kg, dosis_maxima_fn,
            excluidos=None, margenes_categoria=None, cuantos_max=None,
            max_suplementos=2, tolerancia_kcal=0.03,
            forzar=None, preferir=None, patologias=None, semilla_aleatoria=None,
            time_limit=15, restringir_especie=None, peso_adulto_esperado_kg=None,
            evitar_especies=None, restringir_a_elegidos=None, categorias_excluidas=None,
            presupuesto_semanal_restante=None):
    """
    UNA sola llamada. Decide QUÉ alimentos usar Y cuántos gramos de cada
    uno, de entre TODOS los accesibles, a la vez.

    `forzar`: lista de nombres que SÍ O SÍ tienen que entrar en la ración
    (con gramos > 0). Es el modo PERSONALIZAR: el usuario elige alimentos
    concretos y el motor calcula el resto alrededor de esa elección. Si
    forzar algo hace que no exista solución, se devuelve (False, None) —
    igual que antes, una respuesta exacta, no una aproximación.

    `preferir`: lista de nombres que el motor debe usar CON PREFERENCIA
    sobre otros si hay varias soluciones igual de válidas — no obliga a
    que entren, solo hace que el "coste" de usarlos sea menor. Es el modo
    APROVECHAR: lo que el usuario ya tiene en casa gana la partida frente
    a alimentos que tendría que comprar, PERO SOLO si con eso sigue
    cumpliendo los 30 requisitos — si no llega, el motor añade lo que
    haga falta igualmente, avisando (eso se ve en qué más aparece en la
    ración final).

    `restringir_a_elegidos`: {categoría: [nombres]} — ⚠️ AÑADIDO (5
    agosto, madrugada), PEDIDO EXPRESO: en Personalizar, si el usuario
    elige 1-2 carnes concretas, antes el motor podía añadir OTRA carne
    más sin que hiciera falta, solo porque "le convenía" para cuadrar
    algo. Con esto, la categoría (típicamente Carne muscular, Pescados y
    mariscos, Hueso carnoso) queda restringida a SOLO los nombres dados
    -- ninguna otra especie de esa categoría entra, aunque sí se sigue
    decidiendo libremente CUÁNTOS gramos de cada una. Si con eso no hay
    solución viable, quien llama a resolver() debe reintentar sin esta
    restricción (igual que ya hace forzar cuando no hay solución) --
    aquí solo se aplica el filtro, la lógica de "inténtalo así primero,
    si no se puede afloja" vive en quien llama, no aquí dentro.

    `presupuesto_semanal_restante`: {clave_nutriente: tope_diario_efectivo}
    — ⚠️ AÑADIDO (5 agosto, madrugada), CAMBIO DE ARQUITECTURA PEDIDO
    EXPRESAMENTE: los topes de seguridad crónica (tiaminasa, mercurio,
    vitD, yodo, selenio) tienen un límite SEMANAL real, no solo por
    ración -- pero cada menú de una rotación se genera en una llamada
    aparte, sin memoria de lo que ya "gastaron" los menús anteriores de
    esa misma semana. Quien orquesta la generación de varios menús
    (main.py) calcula, ANTES de pedir este menú, cuánto presupuesto
    semanal queda tras los menús ya generados, lo reparte entre los
    días que faltan, y pasa aquí el tope diario EFECTIVO resultante --
    más estricto que el tope normal por ración. Aquí dentro solo se usa
    ese valor en vez del de por defecto si viene informado (nunca al
    revés: nunca se afloja un tope, solo se puede endurecer). Así, por
    diseño, es matemáticamente imposible que la suma de una semana
    entera supere el límite seguro, sin depender de que nadie revise un
    aviso después.

    Devuelve (factible: bool, gramos: {nombre: g} o None).
    """
    from accesibles import ACCESIBLES
    from exclusiones import filtrar

    if cuantos_max is None:
        from modos import CUANTOS_MAX as cuantos_max

    # ⚠️ AÑADIDO 5 agosto: "Extras" (aceites, huevos, semillas) NO estaba
    # en esta lista, así que ni siquiera entraban como candidatos — el
    # linoleico dependía solo de lo que aportara la carne, sin poder usar
    # aceite de girasol. Ahora entra, y junto con los suplementos
    # comerciales queda topado al 5% del peso (decisión de la usuaria).
    SUP_CATS = ("Multivitamínico", "Omega-3", "Yodo", "Fibra", "Calcio",
               "Hierro", "Vitamina B", "Extras")

    # Candidatos: TODOS los accesibles de cada categoría de comida, y
    # TODOS los suplementos del catálogo (no solo unos pocos elegidos).
    #
    # ⚠️ REESCRITO (5 agosto, noche) — DECISIÓN DE DISEÑO IMPORTANTE,
    # pedida expresamente por la usuaria: ACCESIBLES es la lista de "lo
    # fácil/seguro de encontrar" que usa el AUTOMÁTICO para no sugerir
    # cosas raras -- pero eso NUNCA debe impedir que el usuario, a mano,
    # use CUALQUIER cosa del catálogo entero si la elige explícitamente
    # (personalizar, o "todo el/la X"). Antes, si algo no estaba en
    # ACCESIBLES, era imposible usarlo aunque el usuario lo pidiera
    # expresamente -- fallaba siempre, sin explicación. Ahora, si el
    # usuario fuerza un alimento concreto o pide "todo el/la X" y eso no
    # está en la lista curada, se añade igualmente desde el catálogo
    # completo, siempre que exista de verdad y sea de esa categoría.
    candidatos_por_cat = {}
    for cat, lista in ACCESIBLES.items():
        disp = [n for n in lista if n in alimentos]
        if excluidos:
            disp, _f, _a = filtrar(disp, excluidos)

        # elección explícita del usuario (personalizar): si forzó un
        # alimento de ESTA categoría que no estaba en la lista curada,
        # se añade igual, tomándolo del catálogo completo
        if forzar:
            for n in forzar:
                if n in alimentos and alimentos[n].get("categoria") == cat and n not in disp:
                    disp.append(n)

        # "Todo el/la especie": si tras filtrar por la especie pedida no
        # queda NINGÚN candidato curado, se busca en el catálogo entero
        # cualquier alimento de esa categoría+especie, en vez de dejar
        # la categoría vacía (que antes hacía fallar todo el menú).
        if restringir_especie and cat in restringir_especie:
            especie_pedida = restringir_especie[cat].strip().lower()
            disp_curados = [n for n in disp if especie_de(n).strip().lower() == especie_pedida]
            if not disp_curados:
                disp_curados = [n for n, a in alimentos.items()
                                if a.get("categoria") == cat
                                and especie_de(n).strip().lower() == especie_pedida]
            disp = disp_curados

        # ⚠️ AÑADIDO (5 agosto, madrugada) — ver docstring de
        # restringir_a_elegidos arriba. Se aplica DESPUÉS de todo lo
        # anterior: si esta categoría tiene una lista de "solo estos",
        # se descarta cualquier otro candidato de la categoría, sean
        # cuales sean -- solo quedan los nombres pedidos (comprobando
        # que existan de verdad y sean de esta categoría, tomándolos
        # del catálogo completo si no estaban en la lista curada).
        if restringir_a_elegidos and cat in restringir_a_elegidos:
            pedidos = [n for n in restringir_a_elegidos[cat]
                      if n in alimentos and alimentos[n].get("categoria") == cat]
            if pedidos:
                disp = pedidos

        # ⚠️ AÑADIDO (5 agosto, madrugada) — PEDIDO EXPRESO: perros que
        # no pueden masticar hueso carnoso con normalidad (senior,
        # dientes en mal estado, etc.) necesitan poder excluir esa
        # categoría ENTERA de la ración -- no elegir una especie
        # concreta, sino no usar NINGÚN hueso carnoso. Se aplica el
        # ÚLTIMO, después de cualquier otra restricción, y GANA sobre
        # todas ellas: si la categoría está excluida, se vacía sin
        # excepción, aunque forzar/restringir_a_elegidos hubiera puesto
        # algo ahí (nunca debería pasar en la práctica -- el frontend no
        # debe dejar elegir a mano una categoría que se acaba de excluir
        # -- pero por seguridad, la exclusión gana siempre).
        if categorias_excluidas and cat in categorias_excluidas:
            disp = []

        # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO,
        # pedido expreso: con oxalato cálcico, el aviso decía "no
        # debería dársele espinaca" pero la espinaca aparecía en el
        # menú de todas formas -- toda una categoría de restricciones
        # de patología (oxalato, urato, borraja, restricciones propias
        # de cada alimento) solo vivían como aviso de texto, nunca como
        # algo que el solver respetara al elegir. Se aplica AQUÍ, con
        # la MISMA prioridad final que categorias_excluidas (después de
        # forzar/restringir_a_elegidos, ganando sobre ellos) -- la
        # seguridad nunca debe poder saltarse ni siquiera si alguien
        # intenta forzar a mano un alimento prohibido por patología.
        #
        # ⚠️ CORREGIDO en el mismo momento -- CASO REAL ENCONTRADO
        # probando "urato": la primera versión de esto ponía TECHO=0
        # más abajo en vez de quitar el alimento de aquí -- pero dejarlo
        # presente como variable del LP (aunque con techo 0) podía
        # "gastar" el cupo de restricciones como "máximo 1 víscera"
        # (cuantos_max) sin aportar nada real, dejando sin cupo a una
        # víscera de verdad y volviendo el problema matemáticamente
        # infactible sin motivo real. Quitarlos aquí, del catálogo de
        # candidatos, evita que puedan "gastar" cupo de ninguna
        # restricción, sea la que sea.
        from seguridad import OXALATO_ALTO, PURINAS_ALTAS, BORRAJA_EXCLUIR, _es as _es_patologia
        if "oxalato" in (patologias or []):
            disp = [n for n in disp if not _es_patologia(n, OXALATO_ALTO)]
        if "urato" in (patologias or []) and cat in ("Hígado", "Vísceras", "Pescados y mariscos"):
            disp = [n for n in disp if not _es_patologia(n, PURINAS_ALTAS)]
        disp = [n for n in disp if not _es_patologia(n, BORRAJA_EXCLUIR)]
        disp = [n for n in disp
               if not any(pat in (patologias or [])
                         for pat in (alimentos.get(n, {}).get("restricciones_patologia") or {}))]

        candidatos_por_cat[cat] = disp
    candidatos_por_cat["Suplementos"] = [a["nombre"] for a in alimentos.values()
                                        if a.get("categoria") in SUP_CATS]

    # ⚠️ REESCRITO (5 agosto, mañana): antes solo se EXCLUÍA "V-INTEGRA
    # Perro Adulto" fuera de esa etapa, sin ofrecer ninguna alternativa
    # -- así que un cachorro se quedaba sin ningún V-INTEGRA disponible
    # (el motor tenía que buscarse la vida con otra marca). Ahora que
    # existen las 5 variantes reales del fabricante (Cachorro, Adulto,
    # Senior, Epato, Renal, con datos de la ficha oficial), se filtra la
    # lista para que SOLO esté disponible la variante correcta según la
    # etapa y la patología del perro -- nunca las demás, aunque
    # matemáticamente "cuadraran": cada una está formulada para una
    # necesidad concreta (más calcio en cachorro, cobre restringido en
    # hepatopatía, fósforo a cero en renal...), y mezclar no tiene sentido.
    TODAS_LAS_VINTEGRA = {"V-INTEGRA Cachorro", "V-INTEGRA Perro Adulto",
                          "V-INTEGRA Senior", "V-INTEGRA Epato", "V-INTEGRA Renal"}
    if patologias and "hepatopatia" in patologias:
        correcta = "V-INTEGRA Epato"
    elif patologias and "renal" in patologias:
        correcta = "V-INTEGRA Renal"
    elif etapa in ("CachorroJoven", "CachorroCrecimiento", "Gestante",
                   "GestanteTemprana", "GestanteTardia", "Lactante"):
        correcta = "V-INTEGRA Cachorro"  # misma exigencia nutricional que un cachorro
    elif etapa == "Senior":
        correcta = "V-INTEGRA Senior"
    else:
        correcta = "V-INTEGRA Perro Adulto"
    candidatos_por_cat["Suplementos"] = [
        n for n in candidatos_por_cat["Suplementos"]
        if n not in TODAS_LAS_VINTEGRA or n == correcta
    ]

    nombres = []
    categoria_de = {}
    for cat, lista in candidatos_por_cat.items():
        for n in lista:
            if n not in nombres:
                nombres.append(n)
                categoria_de[n] = cat
    n_var = len(nombres)
    # variables: [gramos_0..gramos_N-1, usa_0..usa_N-1] — la mitad continuas,
    # la mitad binarias (0/1), unidas por: gramos_i <= usa_i * TECHO_i
    idx = {n: i for i, n in enumerate(nombres)}

    et = EQUIVALENCIA.get(etapa, etapa)
    A_rows, lb_rows, ub_rows = [], [], []

    def fila_vacia():
        return [0.0] * (2 * n_var)

    # TECHOS por variable (para la vinculación gramos<=usa*techo)
    # ⚠️ AÑADIDO (5 agosto): diabetes quita la fruta del todo. Poniendo su
    # techo a 0, la vinculación gramos<=usa*techo obliga gramos=0 siempre,
    # sin tocar el resto de la formulación.
    excluye_fruta = any(PATOLOGIAS.get(p, {}).get("excluye_fruta") for p in (patologias or []))
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO,
    # pedido expreso: "con oxalato cálcico avisa que no debería dársele
    # espinaca, y la mete en el menú de todas formas". Causa real: había
    # TODA una categoría de restricciones de patología (oxalato, urato,
    # borraja, y las restricciones propias de cada alimento como grelo/
    # nabo en hipotiroidismo) que solo vivían como AVISO de texto en
    # seguridad.py, sin ninguna exclusión real dentro del solver -- a
    # diferencia de los topes numéricos (fósforo, sodio, grasa%) que sí
    # eran restricciones duras. El solver podía meter espinaca sin nada
    # que se lo impidiera, y el aviso posterior decía "esto no debería
    # estar aquí" sobre un menú que él mismo ya había generado. Ahora se
    # excluyen con el MISMO mecanismo que ya usaba la fruta en diabetes
    # (techo a 0): oxalato con antecedente de urolitos, urato con
    # predisposición, borraja siempre (toxicidad real, no depende de
    # patología), y las restricciones propias de cada alimento en el
    # catálogo (grelo/nabo, dátil/mango/plátano, coco...).
    from seguridad import OXALATO_ALTO, PURINAS_ALTAS, BORRAJA_EXCLUIR, _es as _es_patologia
    excluye_oxalato = "oxalato" in (patologias or [])
    excluye_urato = "urato" in (patologias or [])
    CATEGORIAS_PURINAS_REALES = {"Hígado", "Vísceras", "Pescados y mariscos"}
    techos = []
    for n in nombres:
        a = alimentos[n]
        if excluye_fruta and n in FRUTAS:
            techos.append(0.0)
            continue
        if excluye_oxalato and _es_patologia(n, OXALATO_ALTO):
            techos.append(0.0)
            continue
        if excluye_urato and _es_patologia(n, PURINAS_ALTAS) and a.get("categoria") in CATEGORIAS_PURINAS_REALES:
            techos.append(0.0)
            continue
        if _es_patologia(n, BORRAJA_EXCLUIR):
            techos.append(0.0)
            continue
        restr_propia = a.get("restricciones_patologia") or {}
        if any(pat in (patologias or []) for pat in restr_propia):
            techos.append(0.0)
            continue
        if categoria_de[n] == "Suplementos":
            t = dosis_maxima_fn(a, peso_perro_kg)
            techos.append(t if t else 5.0)
        else:
            kcal100 = a.get("energia", 0) or 1.0
            techos.append((der * 0.55) / kcal100 * 100.0)  # ningún alimento >55% del día

    # 1. kcal totales = DER (con tolerancia)
    fila = fila_vacia()
    for n in nombres:
        fila[idx[n]] = alimentos[n].get("energia", 0) / 100.0
    A_rows.append(fila); lb_rows.append(der * (1 - tolerancia_kcal)); ub_rows.append(der * (1 + tolerancia_kcal))

    # ⚠️ AÑADIDO (5 agosto): topes mas estrictos por patologia. Si una
    # patologia baja el maximo de un nutriente y ese maximo es MAS
    # RESTRICTIVO que el de FEDIAF, gana el de la patologia (el min de
    # los dos). Nunca al reves: una patologia no puede RELAJAR un tope.
    topes_patologia = {}
    for p in (patologias or []):
        info = PATOLOGIAS.get(p, {})
        for clave, valor in info.get("max_por_1000kcal", {}).items():
            actual = topes_patologia.get(clave)
            topes_patologia[clave] = valor if actual is None else min(actual, valor)

    # ⚠️ AÑADIDO (5 agosto, noche) — CONECTADO: "Calcio_LateGrowth_RazaGrande"
    # ya existía en los datos, con nota de auditoría explícita diciendo que
    # el motor nunca lo usaba porque no estaba en su MAPA. Fuente: 4.5g/1000kcal
    # como techo de calcio en cachorros de razas grandes/gigantes es la cifra
    # que cita la literatura veterinaria (Vet Clinics: Small Animal Practice,
    # citando FEDIAF) -- coincide con el techo genérico que YA aplicábamos a
    # TODOS los cachorros. Lo que de verdad falta para raza grande/gigante es
    # un MÍNIMO más alto (2500 en vez de 2000): necesitan una ingesta más
    # consistente, no tienen margen para quedarse cortas. Solo se activa para
    # razas grande/gigante (peso adulto esperado >= 25kg) Y en crecimiento --
    # nunca para razas pequeñas, donde este mínimo más alto no aplica.
    minimos_reforzados = {}
    RAZA_GRANDE_O_GIGANTE_KG = 25
    if (peso_adulto_esperado_kg and peso_adulto_esperado_kg >= RAZA_GRANDE_O_GIGANTE_KG
            and etapa in ("CachorroJoven", "CachorroCrecimiento")):
        r_grande = req.get("Calcio_LateGrowth_RazaGrande")
        if r_grande:
            mn_grande = _num(r_grande.get(f"min{et}"))
            if mn_grande:
                minimos_reforzados["calcio"] = mn_grande

    # 2. mínimos y máximos de FEDIAF
    #
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CAMBIO DE ARQUITECTURA PEDIDO
    # EXPRESAMENTE: hasta ahora, los topes de seguridad crónica
    # (mercurio, vitamina D, yodo, selenio) SOLO se comprobaban DESPUÉS
    # de generar el menú, como un aviso de texto -- el usuario podía
    # ignorarlo, y el sistema seguía dejando pasar la dieta igual. Se
    # pidió explícitamente que estos límites nunca puedan superarse,
    # ni con aviso ni sin él: la responsabilidad es del sistema, no del
    # usuario. Para vitamina D y yodo, algunos de nuestros umbrales de
    # seguridad crónica (NRC 2006) son MÁS ESTRICTOS que el máximo
    # nutricional/legal de FEDIAF -- así que aquí se usa siempre el más
    # estricto de los dos como techo REAL del solver, no solo el de
    # FEDIAF. Ver seguridad.py para el porqué de cada cifra.
    from seguridad import TOPE_VITD_KCAL, TOPE_VITD_KG075, TOPE_YODO_KCAL, TOPE_SELENIO_G_DIETA
    # ⚠️ CORREGIDO (5 agosto, madrugada) — BUG REAL Y GRAVE ENCONTRADO,
    # pedido expreso: "si edito un menú, ¿sigue teniendo en cuenta los
    # límites semanales?" -- investigando eso se encontró un bug de
    # unidades MUCHO más amplio, presente en TODO el sistema (no solo
    # al editar). MAPA (usado más abajo para construir cada restricción
    # con "hi = mx * der / 1000.0") espera que "mx" sea una TASA "por
    # 1000kcal" -- pero "tope_vitd_activo" se calculaba AQUÍ ya
    # convertido a un valor ABSOLUTO (TOPE_VITD_KCAL * der / 1000.0),
    # y luego se mezclaba, vía min(), con el máximo FEDIAF (que SÍ es
    # una tasa) y con presupuesto_semanal_restante (también absoluto) --
    # tres magnitudes de unidades distintas comparadas como si fueran
    # la misma cosa. El resultado ganador de esos min() volvía a pasar
    # por "* der / 1000.0" en el bucle de más abajo, aplicando la
    # conversión de tasa a absoluto una SEGUNDA vez cuando el valor ya
    # era absoluto -- confirmado con un caso real: un tope real de 18µg
    # se convertía en un tope efectivo de 21.6µg (18 * der/1000 = 18*1.2),
    # una violación del 20% que solo aparecía cuando el solver se veía
    # empujado cerca de ese límite (de ahí que fuera intermitente, no
    # siempre). Ahora TODO se mantiene como tasa "por 1000kcal" hasta el
    # final del bucle, y solo se convierte a absoluto una única vez, ahí.
    tope_vitd_activo = TOPE_VITD_KCAL
    # ⚠️ CORREGIDO en el mismo momento, CASO REAL ENCONTRADO en producción
    # (segunda vez que se pedía este arreglo): la Fase 1 original solo
    # llevaba el tope por kcal de vitamina D como restricción dura --
    # NUNCA se calculaba ni comparaba el tope por peso (kg^0.75), que sí
    # se compara correctamente en el aviso de revisar_seguridad() (solo
    # avisa, no bloquea). Un cachorro/lactante pequeño puede tener un
    # tope por peso mucho más estricto que el de kcal (confirmado con
    # datos reales: 3.5µg por peso frente a 12.9µg por kcal para un Toy
    # Lactante de 1.5kg) -- así que el solver dejaba pasar menús que
    # violaban el límite real sin que nada lo impidiera, porque nunca
    # llegó a comparar contra el tope correcto. TOPE_CRONICO_KCAL usa
    # ahora siempre el más estricto de los dos, igual que ya hacía
    # revisar_seguridad() -- MAPA guarda "vitD" en kcal por 1000, así
    # que el de peso se convierte a esa misma unidad antes de comparar.
    if peso_perro_kg and peso_perro_kg > 0 and der:
        tope_vitd_por_peso_absoluto = TOPE_VITD_KG075 * (peso_perro_kg ** 0.75)
        tope_vitd_por_peso_en_kcal = tope_vitd_por_peso_absoluto / der * 1000.0
        tope_vitd_activo = min(tope_vitd_activo, tope_vitd_por_peso_en_kcal)
    # ⚠️ AÑADIDO en el mismo momento -- CASO REAL: probando el arreglo de
    # arriba, el solver se pegaba EXACTO al límite (matemáticamente
    # correcto con precisión completa), pero el redondeo de gramos a 2
    # decimales para enseñarlos podía empujar el valor final ligerísimamente
    # por encima del tope real -- mismo mecanismo que ya se documentó para
    # los mínimos (con su margen del 0.8%), pero nunca se había aplicado a
    # los máximos. Con márgenes de seguridad tan estrechos como estos
    # (algunos casos dejan muy poco margen entre el mínimo de FEDIAF y el
    # tope de seguridad crónica), ese redondeo puede marcar la diferencia
    # entre pasar o no pasar el límite real. Margen del 1% SOLO en estos 5
    # puntos concretos, no en el resto de los 30 requisitos de FEDIAF.
    MARGEN_REDONDEO_SEGURIDAD = 0.99
    tope_vitd_activo *= MARGEN_REDONDEO_SEGURIDAD
    TOPE_CRONICO_KCAL = {"vitD": tope_vitd_activo, "yodo": TOPE_YODO_KCAL * MARGEN_REDONDEO_SEGURIDAD}
    if presupuesto_semanal_restante and der:
        # presupuesto_semanal_restante llega en valores ABSOLUTOS (µg
        # totales para el día) desde main.py -- se convierte aquí a la
        # misma tasa "por 1000kcal" que usa TOPE_CRONICO_KCAL, antes de
        # comparar con min(). La conversión a absoluto real ocurre una
        # única vez, más abajo en el bucle de MAPA (hi = mx * der / 1000).
        for clave_nut, tope_efectivo_absoluto in presupuesto_semanal_restante.items():
            if clave_nut in TOPE_CRONICO_KCAL:
                tope_efectivo_tasa = tope_efectivo_absoluto / der * 1000.0
                # nunca se afloja -- solo se usa si es MÁS estricto que el normal
                TOPE_CRONICO_KCAL[clave_nut] = min(TOPE_CRONICO_KCAL[clave_nut], tope_efectivo_tasa)
    for nombre_req, clave in MAPA.items():
        r = req.get(nombre_req)
        if not r:
            continue
        mn = _num(r.get(f"min{et}"))
        if clave in minimos_reforzados:
            mn = minimos_reforzados[clave] if mn is None else max(mn, minimos_reforzados[clave])
        mx = _num(r.get(f"max{et}")) or _num(r.get("maxAdulto"))
        if clave in topes_patologia:
            mx = topes_patologia[clave] if mx is None else min(mx, topes_patologia[clave])
        if clave in TOPE_CRONICO_KCAL:
            tope_cronico = TOPE_CRONICO_KCAL[clave]
            mx = tope_cronico if mx is None else min(mx, tope_cronico)
        fila = fila_vacia()
        aporta_algo = False
        for n in nombres:
            v = (_num(alimentos[n].get("nutrientes", {}).get(clave)) or 0.0) / 100.0
            if v:
                fila[idx[n]] = v; aporta_algo = True
        if not aporta_algo:
            continue
        # ⚠️ AÑADIDO (5 agosto): +1.5% de margen sobre el mínimo exacto.
        # Encontrado probando la aleatoriedad de arriba: el programa podía
        # resolver EXACTO al límite (matemáticamente correcto con toda su
        # precisión), pero al redondear los gramos a 2 decimales para
        # enseñarlos, ese redondeo empujaba el nutriente justo por debajo
        # del mínimo -- pasando de "cumple" a "no cumple" solo por el
        # redondeo, no por un fallo real de la solución. Con este margen,
        # el redondeo ya no puede tirarlo por debajo.
        # ⚠️ SUBIDO de 0.8% a 1.5% (5 agosto, madrugada) — CASO REAL: el
        # cloruro en un Toy CachorroJoven de 1.5kg tenía 156.36mg vs el
        # mínimo de 157.50mg -- diferencia de 1.14mg, equivalente a 0.002g
        # de sal (60.700mg cloruro/100g). El solver resolvía pidiendo 158.76mg
        # (0.8% sobre el mínimo) pero el redondeo a 2 decimales bajaba el
        # resultado 2.40mg por debajo de lo que el solver exigió. Con 1.5%
        # el solver pide 159.97mg, dejando un colchón real de 2.47mg por
        # encima del mínimo FEDIAF incluso después del redondeo.
        lo = mn * der / 1000.0 * 1.015 if mn is not None else -np.inf
        hi = mx * der / 1000.0 if mx is not None else np.inf
        A_rows.append(fila); lb_rows.append(lo); ub_rows.append(hi)

    # ⚠️ AÑADIDO (5 agosto, madrugada) — SELENIO POR GRAMO DE DIETA
    # (Merck Veterinary Manual: 2 µg/g de dieta, límite tolerable
    # máximo) -- esta cifra viene en una unidad DISTINTA a la de
    # FEDIAF (µg por gramo de comida, no µg por 1000 kcal), así que no
    # se puede simplemente comparar y quedarse con la más estricta como
    # arriba. Pero SÍ se puede expresar como restricción lineal
    # directa: suma(selenio_i * gramos_i) <= 2.0 * suma(gramos_i), que
    # reordenado es suma((selenio_i/100 - 2.0) * gramos_i) <= 0 -- una
    # fila más para el mismo sistema de restricciones del solver, con
    # límite superior 0, sin cambiar cómo funciona el resto.
    fila_selenio_g = fila_vacia()
    aporta_selenio = False
    tope_selenio_efectivo = TOPE_SELENIO_G_DIETA * MARGEN_REDONDEO_SEGURIDAD
    if presupuesto_semanal_restante and "selenio_g_dieta" in presupuesto_semanal_restante:
        tope_selenio_efectivo = min(tope_selenio_efectivo, presupuesto_semanal_restante["selenio_g_dieta"] * MARGEN_REDONDEO_SEGURIDAD)
    for n in nombres:
        v_selenio = (_num(alimentos[n].get("nutrientes", {}).get("selenio")) or 0.0) / 100.0
        if v_selenio:
            fila_selenio_g[idx[n]] = v_selenio - tope_selenio_efectivo
            aporta_selenio = True
    if aporta_selenio:
        A_rows.append(fila_selenio_g); lb_rows.append(-np.inf); ub_rows.append(0.0)

    # ⚠️ AÑADIDO (5 agosto, madrugada) — TIAMINASA Y MERCURIO como
    # restricciones duras. Estos dos no son nutrientes numéricos con
    # dato por alimento -- son SETS de especies concretas (sardina/
    # caballa/arenque/boquerón/carpa para tiaminasa; atún para
    # mercurio), así que se restringe directamente la fracción de kcal
    # del día que pueden aportar ENTRE TODOS los alimentos de cada set,
    # igual que la restricción de kcal totales de arriba pero limitada
    # a ese subconjunto. Antes esto se comprobaba DESPUÉS de generar el
    # menú (revisar_seguridad) y solo avisaba -- ahora, si forzar algo
    # llevaría a superar el tope, el solver directamente no encuentra
    # solución, en vez de generarla y avisar después.
    from seguridad import TIAMINASA, MERCURIO_ALTO, TOPE_TIAMINASA_KCAL, TOPE_MERCURIO_KCAL, _es
    for clave_presupuesto, nombre_set, tope_frac in (
        ("tiaminasa", TIAMINASA, TOPE_TIAMINASA_KCAL),
        ("mercurio", MERCURIO_ALTO, TOPE_MERCURIO_KCAL),
    ):
        tope_frac_efectivo = tope_frac * MARGEN_REDONDEO_SEGURIDAD
        if presupuesto_semanal_restante and clave_presupuesto in presupuesto_semanal_restante:
            # aquí el presupuesto llega ya como fracción de kcal (0-1), igual que tope_frac
            tope_frac_efectivo = min(tope_frac_efectivo, presupuesto_semanal_restante[clave_presupuesto] * MARGEN_REDONDEO_SEGURIDAD)
        fila_set = fila_vacia()
        aporta_set = False
        for n in nombres:
            if _es(n, nombre_set):
                fila_set[idx[n]] = alimentos[n].get("energia", 0) / 100.0
                aporta_set = True
        if aporta_set:
            A_rows.append(fila_set); lb_rows.append(-np.inf); ub_rows.append(tope_frac_efectivo * der)

    # 2b. RATIO Ca:P — se me olvidó la primera vez. Calcio y fósforo por
    # separado no bastan: la RELACIÓN entre ambos es su propio requisito,
    # y es lineal (Ca >= ratio_min * P  y  Ca <= ratio_max * P), así que
    # se puede meter igual que cualquier otra restricción.
    r_ratio = req.get("Relacion_Ca_P")
    if r_ratio:
        rmin = _num(r_ratio.get(f"min{et}"))
        rmax = _num(r_ratio.get(f"max{et}"))
        fila_ca = fila_vacia(); fila_p = fila_vacia()
        for n in nombres:
            ca = (_num(alimentos[n].get("nutrientes", {}).get("calcio")) or 0.0) / 100.0
            p = (_num(alimentos[n].get("nutrientes", {}).get("fosforo")) or 0.0) / 100.0
            fila_ca[idx[n]] = ca
            fila_p[idx[n]] = p
        if rmin is not None:
            fila = [fila_ca[j] - rmin * fila_p[j] for j in range(2 * n_var)]
            A_rows.append(fila); lb_rows.append(0.0); ub_rows.append(np.inf)
        if rmax is not None:
            fila = [fila_ca[j] - rmax * fila_p[j] for j in range(2 * n_var)]
            A_rows.append(fila); lb_rows.append(-np.inf); ub_rows.append(0.0)

    # 3. margen por peso de cada categoría de COMIDA (no suplementos)
    if margenes_categoria:
        # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO: las
        # exclusiones de patología recién añadidas arriba (oxalato,
        # urato, restricciones por alimento) pueden dejar una categoría
        # ENTERA vacía como efecto secundario -- por ejemplo, "urato"
        # excluye TODOS los alimentos de Hígado del catálogo (los 4/4
        # tienen purinas altas), pero Hígado sigue teniendo su mínimo
        # obligatorio del 3% del peso, matemáticamente imposible de
        # cumplir si no queda ningún candidato. A diferencia de
        # categorias_excluidas (donde el usuario pide excluir la
        # categoría a propósito), aquí nadie pidió vaciar "Hígado" --
        # es una consecuencia de excluir por seguridad los alimentos
        # concretos. Se detecta automáticamente qué categorías han
        # quedado sin ningún candidato disponible (techo>0 en ninguno
        # de sus miembros) y se tratan con el MISMO mecanismo que una
        # exclusión explícita: su mínimo se ignora, en vez de dejar el
        # problema matemáticamente irresoluble.
        categorias_con_candidato = {categoria_de[n] for n in nombres if techos[idx[n]] > 0}
        categorias_vaciadas_efectivo = {
            cat for cat in margenes_categoria
            if any(categoria_de[n] == cat for n in nombres) and cat not in categorias_con_candidato
        }
        categorias_excluidas_efectivo = set(categorias_excluidas or []) | categorias_vaciadas_efectivo
        # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO
        # completando la exclusión de categoría entera: quitar "Hueso
        # carnoso" (mínimo 20%, máximo 60% del peso) deja un hueco que
        # las demás categorías, con sus máximos actuales, no pueden
        # cubrir matemáticamente -- sumando los máximos del resto
        # (Carne 60% + Verdura 10% + Vísceras 12% + Hígado 6% + un 5%
        # de suplementos aparte) no se llega al 100% del peso del
        # menú, así que el problema era irresoluble aunque el mínimo
        # de Hueso carnoso ya se hubiera puesto a 0. Cuando se excluye
        # esta categoría a propósito, se sube el máximo de Carne
        # muscular (pescado incluido) para que pueda absorber ese
        # hueco -- es la categoría más natural para compensarlo, ya
        # que el hueso carnoso también aporta principalmente proteína
        # y grasa, no un nutriente exclusivo suyo.
        if "Hueso carnoso" in categorias_excluidas_efectivo:
            margenes_categoria = dict(margenes_categoria)
            mn_carne, mx_carne = margenes_categoria.get("Carne muscular", (0.10, 0.60))
            _mn_hueso, mx_hueso = margenes_categoria.get("Hueso carnoso", (0.20, 0.60))
            # ⚠️ CORREGIDO en el mismo momento -- probado con el motor
            # real: sumar una cifra fija (+0.20) no bastaba, seguía
            # siendo matemáticamente imposible llegar al 100% del peso.
            # El cálculo correcto es sumar el HUECO REAL que deja el
            # hueso (su máximo habitual), con 0.95 como techo -- no 1.0
            # exacto, para dejar algo de margen a las categorías con
            # mínimo obligatorio (verduras, vísceras, hígado).
            margenes_categoria["Carne muscular"] = (mn_carne, min(0.95, mx_carne + mx_hueso))
        fila_total = fila_vacia()
        for n in nombres:
            if categoria_de[n] != "Suplementos":
                fila_total[idx[n]] = 1.0
        for cat, (mnp, mxp) in margenes_categoria.items():
            miembros = [n for n in nombres if categoria_de[n] == cat]
            if not miembros:
                # ⚠️ CORREGIDO (5 agosto, noche) — FALLO GRAVE ENCONTRADO
                # por la usuaria: esto antes hacía "continue", saltándose
                # la restricción ENTERA en silencio si esta categoría se
                # quedaba sin ningún candidato disponible (por ejemplo,
                # tras aplicar exclusiones). Eso significaba que si
                # "Hueso carnoso" se quedaba sin candidatos, el mínimo del
                # 20% dejaba de exigirse del todo -- y el motor podía
                # devolver un menú SIN NINGÚN HUESO, marcado como
                # "factible" y "verde" (los 30 nutrientes no dicen nada
                # de los márgenes de categoría, así que verificar() no lo
                # pillaba). Si el mínimo de esta categoría es mayor que
                # cero y no hay NINGÚN candidato para cumplirlo, es
                # matemáticamente imposible cumplirlo -- así que ahora se
                # declara NO FACTIBLE de forma explícita y ruidosa, en
                # vez de fingir que no pasa nada.
                #
                # ⚠️ CORREGIDO (5 agosto, madrugada) — EXCEPCIÓN EXPLÍCITA
                # E INTENCIONAL: la protección de arriba es correcta para
                # el caso ACCIDENTAL (una combinación de exclusiones
                # individuales deja la categoría vacía sin que nadie lo
                # pidiera a propósito). Pero si la categoría está en
                # categorias_excluidas -- exclusión EXPLÍCITA de la
                # categoría entera, pedida a propósito (ver el bloque más
                # arriba que vacía "disp" para esta categoría) -- vaciarla
                # es justo lo que se pidió, así que el mínimo debe
                # ignorarse en ESTE caso concreto, no fallar.
                if mnp and mnp > 0 and not (categorias_excluidas_efectivo and cat in categorias_excluidas_efectivo):
                    return False, None
                continue
            fila_cat = fila_vacia()
            for n in miembros:
                fila_cat[idx[n]] = 1.0
            # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO: el
            # redondeo de cada alimento a 2 decimales al construir el
            # resultado final (más abajo) puede desplazar el peso total
            # de una categoría unas centésimas de gramo respecto a lo
            # que el LP calculó internamente con precisión completa --
            # normalmente inofensivo, pero si el LP resuelve JUSTO en el
            # límite del margen (p.ej. exactamente 20.000% cuando el
            # mínimo es 20%), ese redondeo posterior puede empujarlo a
            # 19.98% y salir fuera de rango pese a que el LP lo resolvió
            # bien. Mismo principio que el +0.8% que ya se aplica a los
            # mínimos de nutrientes: se pide un pelín más del mínimo y
            # un pelín menos del máximo, para que quede colchón real.
            mnp_con_margen = mnp * 1.01 if mnp else mnp
            mxp_con_margen = mxp * 0.99 if mxp else mxp
            fila_rel_max = [fila_cat[j] - mxp_con_margen * fila_total[j] for j in range(2 * n_var)]
            A_rows.append(fila_rel_max); lb_rows.append(-np.inf); ub_rows.append(0.0)
            fila_rel_min = [-fila_cat[j] + mnp_con_margen * fila_total[j] for j in range(2 * n_var)]
            A_rows.append(fila_rel_min); lb_rows.append(-np.inf); ub_rows.append(0.0)

    # ⚠️ AÑADIDO (5 agosto): grasa como % de las kcal (pancreatitis,
    # diabetes) -- restricción propia, no cabe en el bucle de arriba
    # porque compara contra las kcal totales, no contra un mínimo/máximo
    # por 1000kcal. grasa (g) x 9 kcal/g <= pct x der
    pct_grasa_max = None
    for p in (patologias or []):
        v = PATOLOGIAS.get(p, {}).get("max_pct_kcal_grasa")
        if v is not None:
            pct_grasa_max = v if pct_grasa_max is None else min(pct_grasa_max, v)
    if pct_grasa_max is not None:
        fila = fila_vacia()
        for n in nombres:
            g = (_num(alimentos[n].get("nutrientes", {}).get("grasa")) or 0.0) / 100.0
            fila[idx[n]] = g * 9.0
        A_rows.append(fila); lb_rows.append(-np.inf); ub_rows.append(pct_grasa_max * der)

    # 4. VINCULACIÓN gramos <= usa * techo (y gramos >= 0, ya en bounds)
    for n in nombres:
        i = idx[n]
        fila = fila_vacia()
        fila[i] = 1.0
        fila[n_var + i] = -techos[i]
        A_rows.append(fila); lb_rows.append(-np.inf); ub_rows.append(0.0)

    # 5. CUÁNTOS ALIMENTOS DISTINTOS por categoría (máx.)
    for cat, tope in cuantos_max.items():
        miembros = [n for n in nombres if categoria_de[n] == cat]
        if not miembros:
            continue
        fila = fila_vacia()
        for n in miembros:
            fila[n_var + idx[n]] = 1.0
        A_rows.append(fila); lb_rows.append(0); ub_rows.append(tope)

    # 6. MÁXIMO DE SUPLEMENTOS (solo los COMERCIALES cuentan para el
    # límite de "2" — los aceites/huevos de Extras no son "un suplemento"
    # en el sentido de producto de marca, cuentan aparte en el peso)
    SUP_COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                       "Calcio", "Hierro", "Vitamina B")
    # ⚠️ CORREGIDO (5 agosto, tarde) — FALLO GRAVE ENCONTRADO por la
    # batería de pruebas: esto comparaba categoria_de[n] (que vale
    # literalmente el texto genérico "Suplementos" para CUALQUIER
    # suplemento, es la clave del diccionario de candidatos, no la
    # categoría real del alimento) contra SUP_COMERCIALES (que tiene
    # categorías específicas como "Multivitamínico"). La condición NUNCA
    # era cierta, así que esta fila de restricción se quedaba a CEROS —
    # "0 ≤ 2" siempre, sin importar cuántos suplementos hubiera de
    # verdad. El límite de 2 llevaba SIN aplicarse matemáticamente desde
    # que se creó este archivo, no solo desde hoy: dependía por completo
    # de que el objetivo (minimizar alimentos) tendiera a pocos por
    # casualidad, sin ninguna garantía dura detrás. Ahora se consulta la
    # categoría REAL del alimento en el catálogo, no la clave genérica.
    fila = fila_vacia()
    for n in nombres:
        if alimentos[n].get("categoria") in SUP_COMERCIALES:
            fila[n_var + idx[n]] = 1.0
    A_rows.append(fila); lb_rows.append(0); ub_rows.append(max_suplementos)

    # 6b. EXTRAS + SUPLEMENTOS JUNTOS, MÁXIMO 5% DEL PESO (decisión de la
    # usuaria 5 agosto: "los extras, suplementos también entrando dentro
    # de extras, no pueden superar un cinco por ciento").
    fila_total_con_sup = fila_vacia()
    for n in nombres:
        fila_total_con_sup[idx[n]] = 1.0
    fila_extras = fila_vacia()
    for n in nombres:
        if categoria_de[n] == "Suplementos":
            fila_extras[idx[n]] = 1.0
    fila_5pc = [fila_extras[j] - 0.05 * fila_total_con_sup[j] for j in range(2 * n_var)]
    A_rows.append(fila_5pc); lb_rows.append(-np.inf); ub_rows.append(0.0)

    constraints = LinearConstraint(np.array(A_rows), np.array(lb_rows), np.array(ub_rows))
    integrality = np.array([0] * n_var + [1] * n_var)   # 0=continua, 1=entera(binaria)
    bounds = Bounds(lb=[0.0] * n_var + [0] * n_var, ub=[np.inf] * n_var + [1] * n_var)

    # FORZAR: el alimento tiene que estar sí o sí (usa_i >= 1, o sea = 1)
    # ⚠️ CORREGIDO (5 agosto, mañana) — CASO REAL: la usuaria forzó "Pollo
    # muslo con piel" Y "Carcasa de pollo", y la carcasa desapareció del
    # menú final aunque la restricción "forzar" se cumplía matemáticamente.
    # La causa: forzar solo fijaba la variable BINARIA (usa=1), pero no
    # exigía una cantidad de gramos mínima -- así que el resolver podía
    # cumplir "se usa" con una cantidad ridícula (1-2 gramos), y entonces
    # desaparecía del resultado aunque "estuviera forzado".
    #
    # ⚠️ SEGUNDO FALLO ENCONTRADO Y CORREGIDO EN EL MISMO MOMENTO: el
    # primer intento de arreglo usaba "3% de las kcal del día" como
    # mínimo -- pero para un alimento con MUY pocas kcal por 100g (una
    # verdura, una hierba), eso se traduce en una cantidad de PESO
    # enorme (207 g de albahaca, en este caso real), que rompía el
    # margen máximo de peso de su categoría (Verduras y frutas: 10%).
    # Mezclaba kcal y peso sin darse cuenta -- el mismo tipo de error que
    # ya habíamos visto antes con el reescalado del catálogo. Ahora el
    # mínimo es un peso pequeño y FIJO (10 g), sin relación con las kcal
    # del alimento: suficiente para que sea una porción real y visible,
    # nunca tan grande como para poder romper ningún margen.
    #
    # ⚠️ AMPLIADO (5 agosto, madrugada) — CASO REAL: con ese mínimo
    # único de 10 g, cuando se fuerzan VARIOS alimentos de Carne
    # muscular a la vez (el mecanismo de "preservar todo al editar"
    # hace esto a menudo), el resolver podía repartir la carne entre
    # todos ellos dándole a cada uno justo esos 10 g -- técnicamente
    # "presentes", pero una cantidad ridícula que no representa una
    # porción real. 10 g de sal o de un extra es razonable; 10 g de
    # carne muscular no lo es. Ahora el mínimo depende de la categoría:
    # más alto para las proteínas de verdad (carne, pescado, hueso),
    # bajo para lo que sí suele darse en cantidades pequeñas (vísceras,
    # hígado, por su propio límite de dosis) o en extras/suplementos.
    MINIMO_POR_CATEGORIA = {
        "Carne muscular": 40.0,
        "Pescados y mariscos": 40.0,
        "Hueso carnoso": 25.0,
        "Verduras y frutas": 15.0,
    }
    if forzar:
        for n in forzar:
            if n not in idx:
                continue  # no es un candidato válido; se ignora sin romper
            i = idx[n]
            minimo = MINIMO_POR_CATEGORIA.get(categoria_de.get(n), 10.0)
            bounds.lb[n_var + i] = 1
            bounds.lb[i] = min(minimo, techos[i])

    # objetivo: minimizar cuántos alimentos distintos se usan en total
    # (ración simple, no 20 ingredientes), PERO con coste menor para los
    # que el usuario quiere aprovechar — así el resolver los prefiere
    # cuando dos soluciones son igual de válidas, sin obligarlos.
    #
    # ⚠️ AÑADIDO (5 agosto): el motor era determinista -- mismos datos,
    # mismo menú, siempre. Bien para fiabilidad, mal para variedad: pedir
    # el menú de un mismo perro dos veces daba idéntico resultado, y con
    # varios menús a la vez, sin rotar, salía siempre el mismo. Se añade
    # un ruido aleatorio PEQUEÑO al coste de cada alimento (no a las
    # restricciones nutricionales, esas no se tocan) para que, cuando hay
    # varias combinaciones igual de válidas, el motor no elija siempre la
    # misma. Con una semilla, se puede repetir el mismo resultado a
    # propósito (para depurar); sin ella, cada llamada es distinta.
    coste_binaria = [1.0] * n_var
    if preferir:
        for n in preferir:
            if n in idx:
                coste_binaria[idx[n]] = 0.1   # mucho más barato usarlo
    if semilla_aleatoria is not False:
        rng = np.random.RandomState(semilla_aleatoria)  # None = aleatorio de verdad cada vez
        for i in range(n_var):
            coste_binaria[i] += rng.uniform(0.0, 0.4)
        # ⚠️ AÑADIDO (5 agosto, mediodía) — CASO REAL: el pescado salía
        # SIEMPRE en la práctica (8/8 en la prueba), no "casi siempre"
        # como se pensaba. Su ventaja real en EPA/DHA es tan grande que
        # el ruido pequeño de arriba nunca bastaba para que ganara otra
        # cosa. La mitad de las veces (al azar), se penaliza un poco el
        # pescado en el objetivo -- así, cuando SÍ hay una alternativa
        # nutricionalmente válida sin pescado, el resolver la prefiere en
        # esa mitad de los casos. Nunca afecta a si el menú es correcto:
        # solo influye en qué alimento igual de válido se elige.
        if rng.random() < 0.5:
            for n in nombres:
                if categoria_de[n] == "Pescados y mariscos":
                    coste_binaria[idx[n]] += 1.5
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL: la rotación de
    # proteína entre varios menús automáticos EXCLUÍA por completo la
    # especie del menú anterior (especies_excluidas). Eso es una
    # restricción DURA e invisible para el usuario -- él nunca pidió
    # evitar esa especie, es una decisión interna para dar variedad. Si
    # esa especie resultaba ser la única forma razonable de cerrar los
    # 30 requisitos con este perro concreto, la exclusión dura podía
    # volver el problema mucho más difícil o directamente imposible, y
    # el usuario veía "no existe combinación" sin haber pedido nada raro.
    # Ahora, igual que con el pescado, solo se PENALIZA en el objetivo
    # -- el motor la evita si puede, pero nunca puede fallar por esto.
    if evitar_especies:
        evitar_lower = {e.strip().lower() for e in evitar_especies}
        for n in nombres:
            if categoria_de[n] in ("Carne muscular", "Pescados y mariscos", "Hueso carnoso",
                                   "Vísceras", "Hígado"):
                if especie_de(n).strip().lower() in evitar_lower:
                    coste_binaria[idx[n]] += 2.0
    c = np.array([0.0] * n_var + coste_binaria)

    # ⚠️ AÑADIDO (5 agosto, noche) — CASO REAL ENCONTRADO: cachorro pequeño
    # + alergia al pollo tardaba 72-75 segundos, siempre, de forma
    # constante. La causa: milp() sin límites intentaba DEMOSTRAR que la
    # solución encontrada era la óptima exacta (mínimo número de alimentos
    # distintos posible), no solo encontrar UNA que funcione. Esa prueba
    # de optimalidad exacta es la parte cara del problema, no encontrar
    # una solución valida. El objetivo (menos alimentos distintos) es un
    # capricho de presentación, no un requisito nutricional: conformarse
    # con estar cerca del óptimo (1%) es indistinguible para el usuario y
    # muchísimo más rápido.
    #
    # ⚠️ SUBIDO (5 agosto, madrugada) — CASO REAL: restringir a una sola
    # especie (personalizar, "todo el/la X") es un problema genuinamente
    # más difícil, y en el servidor real (más lento que este entorno de
    # pruebas) cada intento individual puede tardar mucho más -- dejando
    # sitio para MENOS reintentos dentro del mismo presupuesto de 18s.
    # Subido de 0.15 a 0.30: acepta una solución un poco menos "óptima"
    # en cuanto a minimizar cuántos alimentos distintos usa (un capricho
    # de presentación, no nutricional), a cambio de que cada intento
    # tarde bastante menos -- así caben más reintentos en el mismo
    # tiempo, sin tocar en absoluto la corrección nutricional, que sigue
    # siendo exacta (el gap no afecta a ninguna restricción, solo a la
    # prueba de que el objetivo es el mínimo posible).
    res = milp(c, constraints=constraints, integrality=integrality, bounds=bounds,
              options={"time_limit": time_limit, "mip_rel_gap": 0.30})

    if res.success:
        x = res.x[:n_var]
        # ⚠️ CORREGIDO (5 agosto, mañana): el umbral de 0.5g podía borrar
        # del resultado un aporte PEQUEÑO PERO REAL y necesario -- por
        # ejemplo, el yoduro potásico funciona en dosis de fracciones de
        # gramo. Si el LP decidía que 0.3g de yoduro cerraban el yodo,
        # ese 0.3g desaparecía del diccionario final por el filtro,
        # dejando el yodo sin cerrar en el menú que de verdad se enseña,
        # aunque el LP internamente SÍ lo había resuelto bien. Bajado a
        # 0.02g -- bajo el umbral de lo que se puede pesar en casa, pero
        # sin perder aportes reales de suplementos muy concentrados.
        gramos = {n: round(x[idx[n]], 2) for n in nombres if x[idx[n]] > 0.02}

        # ⚠️ AÑADIDO (5 agosto, madrugada) — RED DE SEGURIDAD FINAL: caso
        # real de la usuaria, un menú de solo 4 alimentos (carne, víscera,
        # hígado, suplemento) SIN hueso ni verdura, aceptado como válido.
        # No se ha conseguido reproducir la causa exacta pese a más de 40
        # intentos dirigidos -- puede ser una imprecisión numérica del
        # propio solver en combinación con pesos muy desiguales entre
        # alimentos. En vez de seguir cazando la causa exacta, esto
        # comprueba el RESULTADO REAL (los gramos que se van a enseñar,
        # no la restricción teórica) antes de devolverlo: si a una
        # categoría con mínimo obligatorio le falta representación de
        # verdad, se rechaza aquí, pase lo que pase por dentro del LP.
        if margenes_categoria:
            for cat, (mnp, _mxp) in margenes_categoria.items():
                if not mnp or mnp <= 0:
                    continue
                # ⚠️ CORREGIDO (5 agosto, madrugada) — mismo motivo que la
                # excepción de arriba: si esta categoría se excluyó a
                # propósito (categorias_excluidas), no tiene sentido
                # exigirle representación aquí tampoco -- esta red de
                # seguridad final debe respetar la misma excepción, o
                # anula por su cuenta lo que ya se permitió arriba.
                if categorias_excluidas_efectivo and cat in categorias_excluidas_efectivo:
                    continue
                if not any(alimentos[n].get("categoria") == cat for n in gramos):
                    return False, None

        return True, gramos
    return False, None
