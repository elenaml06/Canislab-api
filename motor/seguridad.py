# -*- coding: utf-8 -*-
"""
TOPES DE SEGURIDAD — lo que no se puede pasar aunque los números cuadren.

⚠️ HONESTIDAD SOBRE LAS CIFRAS
Los MECANISMOS estan documentados con estudios reales (ver cada bloque).
Los NUMEROS DE CORTE (10%, 5%, 4%, 10%) son CRITERIO DE DESARROLLO nuestro,
salvo el 20% de clara cruda, que es donde se midio dano. Si algun dia hay que
defender esto ante un veterinario, hay que decirlo asi: "el mecanismo esta
publicado, el umbral lo hemos puesto nosotros por prudencia".

Son distintos de los requisitos FEDIAF: aquí no se mira si falta algo, sino
si HAY DEMASIADO de algo que hace daño. Portados del motor viejo, donde
estaban como restricciones del LP.

⚠️ TODOS ESTOS SON DIARIOS. No admiten balance semanal: una tiaminasa no se
"compensa" el jueves, y una dosis tóxica no deja de serlo porque el resto de
la semana se coma poco.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constructor import perfil_nutricional
from exclusiones import _norm, _palabras

# ---------------------------------------------------------------------------
# 1. PESCADO CON TIAMINASA
# ---------------------------------------------------------------------------
# Arenque, caballa, sardina, boqueron y ciprinidos llevan TIAMINASA, una
# enzima que DESTRUYE la vitamina B1 del RESTO de la racion. Actua sobre la
# comida antes de comerla, asi que mezclarlo todo y dejarlo reposar empeora
# el efecto. La coccion la destruye, pero el BARF va crudo.
# FUENTE DEL MECANISMO (solida): Markovich JE, Heinze CR, Freeman LM (2013),
# "Thiamine deficiency in dogs and cats", JAVMA 243(5):649. La enzima y el
# cuadro neurologico estan documentados.
# ⚠️ EL 10% ES CRITERIO NUESTRO, NO DE LA FUENTE. La literatura dice que hay
# riesgo si el pescado tiaminasico es "proporcion sustancial de la dieta",
# sin dar cifra. El 10% es prudencia de desarrollo.
TIAMINASA = {"sardina", "caballa", "arenque", "boqueron", "carpa"}
TOPE_TIAMINASA_KCAL = 0.10

# ---------------------------------------------------------------------------
# 1b. MERCURIO en pescado grande depredador
# ---------------------------------------------------------------------------
# El mercurio se bioacumula: los peces grandes y longevos, al final de la
# cadena trófica, llevan mucho más que los pequeños. Es un riesgo CRÓNICO,
# no de una sola ración -- se va acumulando en el cuerpo del perro con cada
# exposición repetida.
# FUENTE DEL MECANISMO (sólida): Merck Veterinary Manual, "Mercury Toxicosis
# in Animals" -- confirma bioacumulación y curso crónico. Datos de contenido
# real: FDA "Mercury Levels in Commercial Fish and Shellfish" (atún blanco/
# albacora: media 0.35 ppm; atún rojo salvaje ~1.7 ppm; sardina: media 0.013
# ppm, prácticamente despreciable).
# ⚠️ NO EXISTE un límite de seguridad de mercurio específico para perros, ni
# regulatorio ni de un estudio de dosis-respuesta crónico (esto se dice
# explícitamente en Dunham-Cheatham et al., Science of the Total Environment
# 2019;684:276-280). El umbral de aquí se ha extrapolado desde la dosis de
# referencia humana de la EPA (0.1 µg/kg de peso al día) -- es una
# aproximación prudente, NO un límite validado en perros, y así se dice en
# el aviso al usuario.
MERCURIO_ALTO = {"atun"}  # el único pescado grande de riesgo real en este catálogo
TOPE_MERCURIO_KCAL = 0.10       # tope por ración, mismo criterio que tiaminasa
TOPE_MERCURIO_DIAS_SEMANA = 1   # no más de 1 día/semana con presencia significativa

# ---------------------------------------------------------------------------
# 1c. VITAMINA D acumulada de varias fuentes
# ---------------------------------------------------------------------------
# La vitamina D es liposoluble: se almacena en el cuerpo y su exceso no se
# elimina rápido. El riesgo real viene de SUMAR fuentes -- aceite de hígado
# de bacalao, pescado graso, suplementos multivitamínicos y de omega-3 -- no
# de ninguna por separado.
# FUENTE (sólida, con cifra real): Lenox CE & Bauer JE, "Potential adverse
# effects of omega-3 fatty acids in dogs and cats", J Vet Intern Med
# 2013;27:217-226 -- límite superior seguro de 14.6 µg (584 UI) de
# colecalciferol para un perro de 10kg. El escalado correcto por peso es
# METABÓLICO (peso^0.75), no lineal: 2.6 µg/kg^0.75 (comprobado: 2.6 ×
# 10^0.75 = 14.6, coincide exactamente). El NRC (2006) fija además un tope
# de 20 µg (800 UI) por cada 1000 kcal de dieta.
TOPE_VITD_KG075 = 2.6      # µg por kg de peso^0.75 -- Lenox & Bauer 2013
TOPE_VITD_KCAL = 20.0      # µg por 1000 kcal -- NRC 2006

# ---------------------------------------------------------------------------
# 1d. YODO (kelp, suplementos, pescado)
# ---------------------------------------------------------------------------
# El yodo en exceso, dado de forma repetida, puede alterar la función
# tiroidea (mecanismo de Wolff-Chaikoff). El kelp es la fuente más
# problemática: su contenido real de yodo varía muchísimo de un producto a
# otro (hasta 100 veces, de 100 a 10.000 µg por gramo), así que cualquier
# cálculo con kelp tiene bastante incertidumbre real, no solo teórica.
# FUENTE DEL MECANISMO (con caso real documentado): tirotoxicosis por
# exceso de yodo en perros, Veterinary Record 2017; caso similar más
# detallado en Isidori, Corbee & Kooistra, Vet Rec Case Rep 2024;12:e975.
# El NRC (2006) fija el límite superior seguro en 1.400 µg por cada 1000
# kcal de dieta.
# ⚠️ Por la enorme variabilidad del kelp, se aplica un margen de seguridad
# extra del 50% cuando el yodo del menú viene, en parte, de kelp -- para no
# confiar en una cifra de producto que en la práctica puede estar muy lejos
# de la real.
TOPE_YODO_KCAL = 1400.0    # µg por 1000 kcal -- NRC 2006
MARGEN_EXTRA_YODO_KELP = 1.5  # +50% de margen si el yodo viene de kelp

# ---------------------------------------------------------------------------
# 1e. SELENIO (vísceras, pescado, suplementos)
# ---------------------------------------------------------------------------
# El selenio tiene toxicidad tanto AGUDA (sobredosis puntual de suplemento)
# como CRÓNICA (consumo mantenido en niveles moderados durante semanas o
# meses -- la llamada "alkali disease": pérdida de pelo, deformidad de
# uñas/pezuñas, letargia). El riñón es, con diferencia, la fuente más
# concentrada del catálogo.
# FUENTE (sólida, con cifra real): Merck Veterinary Manual, "Selenium
# Toxicosis in Animals" -- límite tolerable máximo de 2 µg por gramo de
# dieta para perros, gatos y peces; confirma explícitamente que la
# toxicosis crónica es real y "usually results from chronic intake of a
# high-selenium diet". El NRC no fijó un límite superior formal para
# perros (JAVMA 2013;243(5):658); se usa como referencia complementaria el
# máximo de AAFCO de 0.57 mg por cada 1000 kcal.
TOPE_SELENIO_G_DIETA = 2.0   # µg de selenio por gramo de dieta -- Merck
TOPE_SELENIO_KCAL = 570.0    # µg por 1000 kcal -- AAFCO (referencia semanal)

# ---------------------------------------------------------------------------
# 2. CLARA DE HUEVO CRUDA SOLA
# ---------------------------------------------------------------------------
# La clara cruda tiene AVIDINA, que se une a la biotina e impide absorberla.
# El riesgo es real SOLO si se da clara sola de forma continuada: la yema es
# rica en biotina y compensa, por eso el huevo ENTERO no se limita.
# FUENTE (medida): Am J Vet Res (1984) — dietas con >=20% de clara cruda
# causaron deficit clinico de biotina (dermatitis, alopecia, hiperqueratosis)
# en semanas, con resolucion al retirarla o suplementar biotina.
# ⚠️ EL 5% ES CRITERIO NUESTRO: margen x4 sobre el 20% donde SI se vio dano.
CLARA_SOLA = {"huevo clara", "clara de huevo"}
TOPE_CLARA_PESO = 0.05

# ---------------------------------------------------------------------------
# 3. OXALATO — solo condicionado a patologia
# ---------------------------------------------------------------------------
# ⚠️ EN PERRO SANO NO HAY DOSIS TOXICA PUBLICADA. Literal de la revision:
# "el oxalato dietetico apenas se ha estudiado en el perro". El panico esta
# mal fundado y el 4% es PRUDENCIA NUESTRA, sin respaldo numerico.
# Lo que SI es recomendacion clinica estandar (VCA Animal Hospitals) es
# evitarlos en perros con antecedente de urolitos de oxalato calcico. Ahi el
# tope es 0 y eso si esta fundado.
# Las hojas de ruibarbo son el mayor riesgo agudo (oxalato muy alto).
OXALATO_ALTO = {"espinaca", "acelga", "ruibarbo", "remolacha"}

# ⚠️ URATO — vísceras metabólicas y marisco/cefalópodos son altos en
# purinas. En perro sano no hay problema (el hígado ya elimina el urato
# via uricasa). Pero en perros con predisposición a urolitos de urato
# (dálmata, shunt hepático) SÍ importa, igual que el oxalato en urolitos
# de calcio. Mismo patrón que OXALATO_ALTO: solo se activa con la
# patología, no en perro sano.
PURINAS_ALTAS = {"higado", "rinon", "calamar", "pulpo", "sepia", "gamba",
                 "langostino", "langostinos"}
# QUITADO el tope en perro sano: no tenia respaldo y ademas la ACELGA es
# nuestra mejor fuente de magnesio (385 mg/100 kcal, el doble que la
# siguiente), justo el nutriente que se atasca. Estabamos cerrandonos la
# solucion por una precaucion inventada.
# ⚠️ SIN TOPE EN PERRO SANO (1.0 = el 100% del plato, o sea nada que topar).
# Habia un 4% y se quito el 4 de agosto por decision de la usuaria. Era
# PRUDENCIA INVENTADA: la revision decia literal que "en perros sanos no hay
# dosis umbral toxica publicada" y que "el oxalato dietetico apenas se ha
# estudiado en el perro".
# Y TENIA UN COSTE REAL: la ACELGA es nuestra mejor fuente de magnesio
# (385 mg/100 kcal, el doble que la siguiente), justo el nutriente que mas
# se atasca. Estabamos bloqueando la solucion con una precaucion inventada.
TOPE_OXALATO_PESO_SANO = 1.0
TOPE_OXALATO_PESO_UROLITOS = 0.0   # con antecedente: fuera

# ---------------------------------------------------------------------------
# 4. VITAMINA A ACUMULADA — el punto ciego de las dietas caseras
# ---------------------------------------------------------------------------
# El higado, el aceite de higado de bacalao y el multivitaminico SE SUMAN.
# Es el riesgo acumulativo mas importante del BARF: cada fuente parece
# razonable por separado y juntas se pasan.
# El maximo FEDIAF ya lo comprueba `verificar()`, pero se anade ademas un
# tope de HIGADO POR PESO porque es la via por la que se dispara.
# ⚠️ EL 10% ES CRITERIO NUESTRO. La convencion BARF es 5% y tampoco tiene
# estudio detras. Lo que SI esta documentado es el mecanismo: el higado es la
# via por la que se dispara la vitamina A, y las fuentes SE SUMAN (higado +
# aceite de higado de bacalao + multivitaminico). El maximo de vitamina A de
# FEDIAF, que si esta verificado, lo comprueba aparte `verificar()`.
TOPE_HIGADO_PESO = 0.10

# ⚠️ EL RIÑÓN COMPARTE MECANISMO CON EL HÍGADO — investigado 4 agosto.
# Cobre (organo metabolico activo, igual que el higado) + CADMIO (se
# acumula preferentemente en rinon e higado; vida media biologica del
# cadmio 7-30 anos) + PURINAS (rinon e higado son los organos con mas
# purinas, ~200-300 mg/100g frente a 50-100 del musculo).
# Mismo tope que el higado por prudencia: son "visceras metabolicas".
VISCERAS_METABOLICAS = {"rinon", "higado"}
TOPE_VISCERAS_METABOLICAS_PESO = 0.10

# ⚠️ NOTA: MERCURIO_ALTO se define arriba (junto al mecanismo completo del
# RfD de la EPA). AESAN clasifica también el atún entre las 4 especies de
# alto mercurio (junto a pez espada, tiburón y lucio, que no tenemos en el
# catálogo) -- dato adicional, misma variable, no se redefine dos veces.

# ⚠️ CEFALOPODOS Y CRUSTACEOS — misma familia que el mejillón (que se
# quito del catalogo). Concentran cadmio y cobre en la GLANDULA DIGESTIVA/
# hepatopancreas, no en el musculo. Como se dan pelados/eviscerados el
# riesgo es menor que el del mejillon (que se come entero), pero no deben
# ser la base diaria. Storelli et al. 2006: hasta 20x mas cadmio en
# hepatopancreas que en carne.
CEFALOPODOS_CRUSTACEOS = {"calamar", "pulpo", "sepia", "gamba", "langostino",
                          "langostinos"}

# ⚠️ SALMON Y TRUCHA CRUDOS — riesgo INFECCIOSO, no nutricional. La
# enfermedad del salmon (Neorickettsia helminthoeca) tiene letalidad ~90%
# sin tratar (endémica del noroeste del Pacifico, pero el riesgo parasitario
# general -anisakis- aplica igual al salmon europeo). Se mitiga CONGELANDO
# antes de dar, no limitando la cantidad.
# ⚠️ CORREGIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO,
# pedido expreso: "verificar lo de la congelación previa". Este conjunto
# solo cubría "salmon" y "trucha" -- 2 de los 15 peces reales del
# catálogo -- así que Sardina, Caballa, Merluza, Bacalao, Lubina,
# Dorada, Atún, Boquerón, Lenguado, Pescadilla, Besugo, Bacaladilla y
# Perca nunca disparaban el aviso de "congelar antes de dar si se da
# crudo", aunque todos ellos pueden darse crudos igual que salmón/
# trucha. Confirmado con fuentes: EFSA y el Reglamento UE 1276/2011
# consideran el riesgo de anisakis (y parásitos similares) un riesgo
# GENÉRICO de todo pescado de mar y agua dulce crudo, no específico de
# unas pocas especies -- la normativa exige congelación para prevenirlo
# en prácticamente cualquier pescado destinado a consumo crudo, no solo
# salmón/trucha. Los cefalópodos/crustáceos (calamar, gamba, langostino,
# pulpo, sepia) se quedan fuera de este conjunto a propósito: la app ya
# indica que esos SIEMPRE se dan cocinados, así que el riesgo se elimina
# por cocción, no por congelación -- no necesitan este aviso concreto.
PESCADO_CONGELAR_ANTES = {
    "salmon", "trucha", "sardina", "caballa", "merluza", "bacalao",
    "lubina", "dorada", "atun", "boqueron", "lenguado", "pescadilla",
    "besugo", "bacaladilla", "perca",
}

# ⚠️ HUESOS DE CARGA (pierna de cordero, huesos de cuello de ternera) SE
# QUITARON DEL CATÁLOGO (4 agosto): riesgo de fractura dental demasiado
# alto para ofrecerlos sin más. HUESO_RIESGO_DENTAL vacio a proposito: si
# algun dia se vuelve a anadir un hueso de carga, hay que decidir entonces
# si entra con aviso o no entra.
HUESO_RIESGO_DENTAL = set()
# Costillas: riesgo distinto (astillado/obstruccion, no fractura), por ser
# hueso estrecho que puede encajarse entre los molares.
HUESO_RIESGO_ASTILLADO = {"costillas de cordero"}

# ⚠️ BORRAJA — ALCALOIDES PIRROLIZIDÍNICOS (PA) HEPATOTÓXICOS. La HOJA (que
# es lo que se da en BARF) contiene PA hepatotoxicos y carcinogenicos
# (amabilina, licopsamina). EFSA fijo niveles maximos y la UK FSA
# recomienda EVITAR las infusiones de hoja. El aceite de semilla de borraja
# casi no lleva PA (es otra parte de la planta), pero como hoja NO se debe
# dar de forma habitual. A diferencia de la tiaminasa o el oxalato, aqui NO
# hay una dosis segura publicada por debajo de la cual esta bien: se
# EXCLUYE, no se topa.
BORRAJA_EXCLUIR = {"borraja"}

# ⚠️ RESTRICCIONES POR PATOLOGIA — investigadas 4 agosto, mismo patron que
# el oxalato/urato: en perro SANO no se tocan, solo se activan si la
# patologia esta declarada. Los datos concretos viven en el propio
# alimento (campo "restricciones_patologia" del catalogo).
# Aqui solo se listan que categorias de patologia hay que comprobar.
PATOLOGIAS_CON_RESTRICCION_ALIMENTO = {"hipotiroidismo", "diabetes", "pancreatitis"}


def _es(nombre, conjunto):
    p = _palabras(nombre)
    n = _norm(nombre)
    return any((t in n) if " " in t else (t in p) for t in conjunto)


def revisar_seguridad(menu, alimentos, der, etapa="Adulto", patologias=None,
                      devolver_avisos=False, peso_perro_kg=None):
    """
    Devuelve lista de problemas de SEGURIDAD. Vacia = todo bien.

    Estos topes son DIARIOS siempre: no admiten balance semanal.
    """
    patologias = set(patologias or [])
    problemas = []
    if not menu:
        return ([], []) if devolver_avisos else []
    total = sum(menu.values()) or 1.0

    def kcal_de(nombres):
        return sum(alimentos[n]["energia"] * menu[n] / 100.0
                   for n in nombres if n in alimentos)

    # 1. tiaminasa
    tia = [n for n in menu if _es(n, TIAMINASA)]
    if tia:
        k = kcal_de(tia)
        if k > der * TOPE_TIAMINASA_KCAL:
            # ⚠️ REFORMULADO (5 agosto, madrugada) — pedido expreso: el
            # mensaje empezaba con "TIAMINASA:" en mayúsculas, sonando a
            # alerta, y no dejaba claro hasta la segunda frase que el
            # problema es SOLO por exceso -- fácil de leer como si el
            # pescado en sí fuera peligroso siempre. Ahora empieza
            # dejando claro que es "en exceso", con el mismo dato real.
            problemas.append(
                "En exceso, %s puede destruir la vitamina B1 (tiamina) del "
                "resto de la ración si se da crudo — pero solo si se pasa de "
                "cierta cantidad. Ahora mismo aporta el %.0f%% de las "
                "calorías del día (el límite seguro es %.0f%%)."
                % (", ".join(tia), k / der * 100, TOPE_TIAMINASA_KCAL * 100))

    # 1b. mercurio en pescado grande
    merc = [n for n in menu if _es(n, MERCURIO_ALTO)]
    if merc:
        k = kcal_de(merc)
        if k > der * TOPE_MERCURIO_KCAL:
            problemas.append(
                "En exceso, %s acumula mercurio en el cuerpo del perro con cada "
                "exposición repetida -- no es un riesgo de una sola vez, es "
                "acumulativo. Ahora mismo aporta el %.0f%% de las calorías del día "
                "(el límite prudente es %.0f%%). Este umbral está extrapolado desde "
                "referencias humanas de la EPA -- no existe un límite validado "
                "específicamente en perros."
                % (", ".join(merc), k / der * 100, TOPE_MERCURIO_KCAL * 100))

    # 1c. vitamina D acumulada de todas las fuentes del menú
    vitd_ug = sum(alimentos.get(n, {}).get("nutrientes", {}).get("vitD", 0) * g / 100.0
                 for n, g in menu.items())
    tope_vitd_por_kcal = TOPE_VITD_KCAL * der / 1000.0
    tope_vitd_activo = tope_vitd_por_kcal
    origen_tope_vitd = "el límite del NRC según sus calorías diarias"
    if peso_perro_kg and peso_perro_kg > 0:
        tope_vitd_por_peso = TOPE_VITD_KG075 * (peso_perro_kg ** 0.75)
        if tope_vitd_por_peso < tope_vitd_activo:
            tope_vitd_activo = tope_vitd_por_peso
            origen_tope_vitd = "el límite según su peso (más estricto que el de calorías en este caso)"
    if vitd_ug > tope_vitd_activo:
        problemas.append(
            "Sumando TODAS las fuentes de este menú (pescado graso, aceite de "
            "hígado de bacalao, suplementos), la vitamina D llega a %.1f µg, por "
            "encima de %s (%.1f µg). La vitamina D se acumula en el cuerpo y su "
            "exceso no se elimina rápido -- revisa si hay más de una fuente "
            "sumando a la vez." % (vitd_ug, origen_tope_vitd, tope_vitd_activo))

    # 1d. yodo (kelp, suplementos, pescado)
    yodo_ug = sum(alimentos.get(n, {}).get("nutrientes", {}).get("yodo", 0) * g / 100.0
                 for n, g in menu.items())
    tope_yodo = TOPE_YODO_KCAL * der / 1000.0
    hay_kelp = any(_es(n, {"kelp", "seaweed", "algas"}) for n in menu)
    if hay_kelp:
        tope_yodo /= MARGEN_EXTRA_YODO_KELP
    if yodo_ug > tope_yodo:
        problemas.append(
            "El yodo de este menú llega a %.0f µg, por encima del límite "
            "prudente (%.0f µg%s). Si la fuente es kelp, ten en cuenta que su "
            "contenido real de yodo puede variar mucho de un producto a otro."
            % (yodo_ug, tope_yodo, " -- con margen extra por incluir kelp" if hay_kelp else ""))

    # 1e. selenio (vísceras, pescado, suplementos)
    selenio_ug = sum(alimentos.get(n, {}).get("nutrientes", {}).get("selenio", 0) * g / 100.0
                     for n, g in menu.items())
    selenio_por_g_dieta = (selenio_ug / total) if total else 0
    if selenio_por_g_dieta > TOPE_SELENIO_G_DIETA:
        problemas.append(
            "El selenio de este menú llega a %.2f µg por gramo de dieta, por "
            "encima del límite tolerable (%.2f µg/g). El riñón es la fuente más "
            "concentrada -- revisa si hay mucha cantidad de vísceras o de "
            "suplemento junto con pescado en el mismo menú."
            % (selenio_por_g_dieta, TOPE_SELENIO_G_DIETA))

    # 2. clara de huevo sola
    claras = [n for n in menu if _es(n, CLARA_SOLA)]
    g_clara = sum(menu[n] for n in claras)
    if g_clara > total * TOPE_CLARA_PESO:
        problemas.append(
            "En cantidad, la clara de huevo cruda y SOLA (sin la yema) puede "
            "bloquear la absorción de biotina — el huevo entero no da este "
            "problema. Ahora mismo son %.0f g, el %.0f%% del plato (el "
            "límite es %.0f%%)."
            % (g_clara, g_clara / total * 100, TOPE_CLARA_PESO * 100))

    # 3. oxalato
    oxal = [n for n in menu if _es(n, OXALATO_ALTO)]
    g_ox = sum(menu[n] for n in oxal)
    tope_ox = TOPE_OXALATO_PESO_UROLITOS if "oxalato" in patologias else TOPE_OXALATO_PESO_SANO
    if tope_ox is not None and g_ox > total * tope_ox:
        if "oxalato" in patologias:
            # este caso SÍ es una restricción real, no "solo en exceso" --
            # se mantiene con ese tono, porque aplica siempre que hay ese
            # antecedente, no depende de la cantidad
            problemas.append(
                "%s no deberían dárselas por el antecedente de urolitos de "
                "oxalato cálcico que tiene — no es una cuestión de "
                "cantidad, mejor evitarlas del todo con esta patología."
                % ", ".join(oxal))
        else:
            problemas.append(
                "En cantidad, %s pueden favorecer los oxalatos. Ahora "
                "mismo son el %.0f%% del plato (el límite es %.0f%%)."
                % (", ".join(oxal), g_ox / total * 100, tope_ox * 100))

    # 4. higado por peso (la via por la que se dispara la vitamina A)
    hig = [n for n in menu if alimentos.get(n, {}).get("categoria") == "Hígado"]
    g_hig = sum(menu[n] for n in hig)
    if g_hig > total * TOPE_HIGADO_PESO:
        problemas.append(
            "En exceso, el hígado puede disparar la vitamina A por encima "
            "de lo seguro. Ahora mismo son %.0f g, el %.0f%% del plato (el "
            "límite es %.0f%%)."
            % (g_hig, g_hig / total * 100, TOPE_HIGADO_PESO * 100))

    # 3b. BORRAJA — se excluye del todo, no se topa por cantidad. A
    # diferencia del resto de reglas de esta funcion, aqui no hay un "% del
    # plato aceptable": la evidencia (EFSA, UK FSA) es de EVITAR, no de
    # limitar. Este SÍ mantiene un tono serio -- no es "en exceso", es
    # "mejor no darla en absoluto", y eso hay que decirlo con claridad,
    # no suavizarlo.
    borr = [n for n in menu if _es(n, BORRAJA_EXCLUIR)]
    if borr:
        problemas.append(
            "%s contiene alcaloides pirrolizidínicos, tóxicos para el "
            "hígado, en la hoja — no se recomienda como verdura habitual, "
            "en ninguna cantidad (EFSA, agencia de seguridad alimentaria "
            "del Reino Unido)." % ", ".join(borr))

    # 3b-bis. RESTRICCIONES POR PATOLOGÍA GUARDADAS EN EL PROPIO ALIMENTO
    # (grelo/nabo en hipotiroidismo, dátil/mango/plátano en diabetes,
    # coco en pancreatitis). Mismo patrón que oxalato/urato: solo se
    # activa si la patología está declarada. Cada motivo ya viene
    # redactado en el propio catálogo, no se toca aquí.
    for n in menu:
        restr = alimentos.get(n, {}).get("restricciones_patologia") or {}
        for pat, motivo in restr.items():
            if pat in patologias:
                problemas.append("%s (%s): %s" % (n, pat.upper(), motivo))

    # 3c. URATO — solo en perros con predisposicion (dalmata, shunt
    # hepatico). Mismo patron que el oxalato: en perro sano no se toca.
    # Restricción real, no "en exceso" -- se mantiene con tono serio.
    #
    # ⚠️ CORREGIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO auditando:
    # PURINAS_ALTAS busca "higado"/"rinon" por PALABRA en el nombre, sin
    # comprobar categoría real -- así que "Aceite de hígado de bacalao"
    # (categoría Extras, un aceite ya procesado) se colaba aquí como si
    # fuera el órgano entero, diciendo que "no debería dársele" a un
    # perro con predisposición a urato, cuando un aceite no tiene la
    # misma carga de purinas que la víscera completa. Ahora se exige
    # además que la categoría real sea una de las relevantes de verdad.
    CATEGORIAS_PURINAS_REALES = {"Hígado", "Vísceras", "Pescados y mariscos"}
    if "urato" in patologias:
        pur = [n for n in menu if _es(n, PURINAS_ALTAS)
              and alimentos.get(n, {}).get("categoria") in CATEGORIAS_PURINAS_REALES]
        if pur:
            problemas.append(
                "%s no deberían dárselas por la predisposición que tiene a "
                "urolitos de urato — no es una cuestión de cantidad, mejor "
                "evitarlas del todo con esta patología." % ", ".join(pur))

    # 4b. RIÑÓN — mismo tope que el hígado, distinto motivo: cobre +
    # CADMIO (se acumula en riñón e hígado, vida media 7-30 años) +
    # PURINAS (2-3x el músculo). Aplica junto con el hígado: si entre los
    # dos pasan del tope, ya es demasiada víscera metabólica en el plato.
    visc_meta = [n for n in menu if _es(n, {"rinon"})]
    g_vm = sum(menu[n] for n in visc_meta)
    if g_vm > total * TOPE_VISCERAS_METABOLICAS_PESO:
        problemas.append(
            "En exceso, el riñón acumula cadmio y tiene más purinas que la "
            "carne muscular. Ahora mismo son %.0f g, el %.0f%% del plato "
            "(el límite es %.0f%%)."
            % (g_vm, g_vm / total * 100, TOPE_VISCERAS_METABOLICAS_PESO * 100))
    g_meta_junto = g_hig + g_vm
    if g_meta_junto > total * TOPE_VISCERAS_METABOLICAS_PESO * 1.5 and hig and visc_meta:
        problemas.append(
            "El hígado y el riñón comparten el mismo mecanismo de "
            "acumulación (cobre/cadmio), así que juntos no deberían sumar "
            "mucho más que el límite de uno solo. Ahora mismo entre los "
            "dos son el %.0f%% del plato."
            % (g_meta_junto / total * 100))

    # 5. fuentes de vitamina A acumuladas — AVISO, no un segundo tope.
    #
    # ⚠️ EL TOPE DE VERDAD SÍ EXISTE: está en el PILAR DE REQUISITOS
    # (requerimientos_v2_final.json → "Vitamina_A" → maxAdulto/maxCachorro
    # = 30.000 µg/1000 kcal) y lo comprueba `verificar()` en verificar.py,
    # igual que cualquier otro nutriente con máximo. No hace falta un
    # segundo tope aquí: sería duplicar la misma regla en dos sitios.
    # Lo que SÍ falta sin este aviso es EXPLICAR por qué se pasó: si el
    # hígado, el aceite de hígado de bacalao y el multivitamínico se suman
    # y el total salta el máximo, `verificar()` lo marcará como "se pasa",
    # pero no dice de dónde viene la suma. Este aviso lo aclara.
    fuentes_a = [n for n in menu
                 if (alimentos.get(n, {}).get("nutrientes", {}).get("vitA") or 0)
                 and (alimentos.get(n, {}).get("categoria") in
                      ("Hígado", "Multivitamínico", "Omega-3", "Extras"))]
    # ⚠️ ESTO ES UN AVISO, NO UN INCUMPLIMIENTO. Que la vitamina A venga de
    # varias fuentes no es malo en sí: lo malo sería pasarse del máximo, y de
    # eso ya se encarga `verificar()`. Se devuelve aparte para que no bloquee
    # un menú que está bien.
    avisos = []
    if len(fuentes_a) >= 3:
        avisos.append(
            "La vitamina A viene de %d fuentes a la vez (%s). Se suman, pero "
            "el total está dentro del máximo."
            % (len(fuentes_a), ", ".join(fuentes_a[:3])))
    if devolver_avisos:
        return problemas, avisos

    return problemas


def avisos_rotacion(menu, alimentos):
    """
    Avisos de FRECUENCIA/MANEJO, no bloqueos. No hay dosis publicada para
    estos, asi que no se puede poner un tope en gramos: lo que hay es una
    recomendacion de no darlos a diario / de prepararlos bien.
    Se devuelven aparte de `revisar_seguridad()` porque no son "problemas
    de este menu", son notas que aplican siempre que aparece el alimento.

    ⚠️ CORREGIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO: estos
    chequeos comparaban el NOMBRE del alimento contra listas de palabras
    (_es), sin comprobar nunca la CATEGORÍA real -- así que cualquier
    SUPLEMENTO cuyo nombre contuviera "salmón" (AniForte Aceite de
    Salmón, Brit Care Aceite de Salmón, etc.) disparaba el aviso de
    "congelar antes de dar" pensado para PESCADO CRUDO, aunque sea un
    aceite ya procesado que nunca necesita congelarse. Ahora cada
    chequeo solo se aplica a alimentos de la categoría real donde tiene
    sentido, no a cualquier nombre que mencione la palabra.
    """
    avisos = []
    for n in menu:
        cat_real = alimentos.get(n, {}).get("categoria")
        if cat_real == "Pescados y mariscos":
            if _es(n, MERCURIO_ALTO):
                avisos.append(
                    "%s: alto en mercurio (AESAN). No debería ser la única "
                    "fuente de pescado ni algo diario — rotarlo con otros "
                    "pescados de bajo mercurio." % n)
            if _es(n, CEFALOPODOS_CRUSTACEOS):
                avisos.append(
                    "%s: acumula cadmio y cobre (misma familia que el "
                    "mejillón). Servir sin cabeza/vísceras y no a diario." % n)
            if _es(n, PESCADO_CONGELAR_ANTES):
                avisos.append(
                    "%s: si se da crudo, debe estar CONGELADO antes -- "
                    "al menos 2 semanas a -18/-20 °C (ESCCAP, la referencia "
                    "europea en parásitos de mascotas) -- para eliminar el "
                    "riesgo parasitario e infeccioso." % n)
        if cat_real == "Hueso carnoso":
            if _es(n, HUESO_RIESGO_DENTAL):
                avisos.append(
                    "%s: hueso de carga, de los más duros. Riesgo de fractura "
                    "dental (carnasial). No apto para perros que muerden con "
                    "fuerza; supervisar siempre." % n)
            if _es(n, HUESO_RIESGO_ASTILLADO):
                avisos.append(
                    "%s: hueso estrecho, riesgo de astillado o de quedar "
                    "encajado entre los molares. Supervisar." % n)
    return avisos


# ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL, muy buena pregunta
# planteada directamente: la tiaminasa se comprobaba SOLO dentro de
# CADA menú por separado (revisar_seguridad recibe un único menú). Si
# se generan varios menús que rotan durante la semana, cada uno podía
# quedarse justo por debajo del límite individual, pero si TODOS ellos
# usan pescado crudo con tiaminasa como proteína principal, el perro
# comería pescado crudo casi todos los días de la semana sin que
# ningún aviso lo detectara -- el riesgo real es acumulativo a lo
# largo de la semana, no solo dentro de un menú aislado.
#
# ⚠️ CORREGIDO en el mismo momento, ANTES de entregarlo — AUTOCRÍTICA:
# la primera versión de esta función calculaba un PROMEDIO PONDERADO
# de kcal de tiaminasa y lo comparaba contra el mismo límite de
# exceso (10%). Pero eso es matemáticamente inútil: si TODOS los menús
# individuales están por debajo del 10%, su promedio ponderado
# TAMBIÉN está por debajo del 10% siempre -- así que ese aviso nunca
# podría dispararse sin que YA se hubiera disparado antes al menos uno
# de los avisos por menú individual. No añadía ningún valor real.
#
# El riesgo real no es "el promedio de exceso semanal", es la
# FRECUENCIA: comer pescado crudo con tiaminasa de forma NO trivial
# (aunque cada ración individual no sea excesiva) casi todos los días
# de la semana, de forma repetida y crónica. Por eso este aviso mide
# en cuántos DÍAS de la rotación (ponderados) el pescado con tiaminasa
# aporta una proporción NO trivial de las kcal (un umbral más bajo que
# el de exceso real) -- y avisa si eso pasa en la gran mayoría de los
# días de la semana, incluso si ningún menú individual llega nunca al
# límite de exceso por sí solo.
UMBRAL_PRESENCIA_TIAMINASA = 0.05   # 5% de las kcal del menú -- "presencia no trivial"
UMBRAL_FRECUENCIA_SEMANAL = 0.80    # si pasa en el 80%+ de los días de la semana, avisar


def revisar_seguridad_semanal(menus_con_dias, alimentos, der, peso_perro_kg=None):
    """
    `menus_con_dias`: lista de (gramos: {nombre: g}, dias: int) -- un
    elemento por cada menú de la rotación semanal, con cuántos días de
    la semana se usa cada uno. Devuelve avisos que solo tienen sentido
    mirando la semana completa, no un menú aislado.
    """
    total_dias = sum(d for _, d in menus_con_dias) or 1
    dias_con_presencia = 0
    fuentes = set()
    for gramos, dias in menus_con_dias:
        kcal_tia_menu = sum(alimentos.get(n, {}).get("energia", 0) * g / 100.0
                            for n, g in gramos.items() if _es(n, TIAMINASA))
        if der and (kcal_tia_menu / der) >= UMBRAL_PRESENCIA_TIAMINASA:
            dias_con_presencia += dias
            fuentes |= {n for n in gramos if _es(n, TIAMINASA)}
    frecuencia = dias_con_presencia / total_dias
    avisos = []
    if frecuencia >= UMBRAL_FRECUENCIA_SEMANAL and fuentes:
        avisos.append(
            "%s aparece en cantidad no trivial en %d de los 7 días de la semana "
            "(según la rotación de menús) — aunque ningún menú individual se pase "
            "del límite de exceso por sí solo, comerlo de forma tan repetida y "
            "crónica es justo el patrón que puede ir destruyendo la vitamina B1 "
            "poco a poco. Conviene que al menos uno de los menús use otra "
            "proteína, para no repetir pescado crudo prácticamente todos los días."
            % (", ".join(sorted(fuentes)), dias_con_presencia))

    # ⚠️ AÑADIDO (5 agosto, madrugada) — pedido expreso, tras investigar a
    # fondo cuatro nutrientes más con este mismo tipo de riesgo crónico:
    # mercurio, vitamina D, yodo y selenio. Mismo patrón que arriba con
    # tiaminasa (frecuencia de presencia no trivial a lo largo de la
    # semana, no un promedio simple contra el mismo límite de exceso --
    # eso sería matemáticamente redundante con el chequeo por menú, tal
    # como se corrigió antes para la tiaminasa). Umbral de "presencia no
    # trivial" puesto en la mitad del límite de exceso por menú, criterio
    # de desarrollo propio, no de ninguna fuente concreta.
    UMBRAL_FRECUENCIA_CRONICOS = 0.80

    def _frecuencia_generica(nombres_o_funcion, tope_kcal_frac, medir_por="kcal"):
        dias_con_presencia_ = 0
        fuentes_ = set()
        for gramos, dias in menus_con_dias:
            if medir_por == "kcal":
                aporte = sum(alimentos.get(n, {}).get("energia", 0) * g / 100.0
                            for n, g in gramos.items() if _es(n, nombres_o_funcion))
                umbral_absoluto = der * tope_kcal_frac * 0.5  # mitad del tope de exceso
                encontrados = {n for n in gramos if _es(n, nombres_o_funcion)}
            else:  # medir_por == "nutriente" -- nombres_o_funcion es el nombre del campo
                aportes_por_alimento = {n: alimentos.get(n, {}).get("nutrientes", {}).get(nombres_o_funcion, 0) * g / 100.0
                                        for n, g in gramos.items()}
                aporte = sum(aportes_por_alimento.values())
                umbral_absoluto = tope_kcal_frac * 0.5  # aquí tope_kcal_frac ya es el valor absoluto del tope
                # ⚠️ CORREGIDO en el mismo momento, probando con datos reales:
                # antes esto marcaba como "fuente" a CUALQUIER alimento con el
                # nutriente > 0, así que el mensaje acababa listando casi
                # todos los ingredientes del menú en vez de señalar la fuente
                # real del problema (el riñón, en el caso de selenio). Ahora
                # solo cuentan los alimentos que aportan al menos un 10% del
                # total de ESE menú -- el mensaje señala lo que de verdad
                # importa, no todo lo que técnicamente contiene algo del
                # nutriente en cantidad insignificante.
                umbral_relevancia = aporte * 0.10 if aporte else 0
                encontrados = {n for n, ap in aportes_por_alimento.items() if ap >= umbral_relevancia and ap > 0}
            if aporte >= umbral_absoluto:
                dias_con_presencia_ += dias
                fuentes_ |= encontrados
        return dias_con_presencia_, fuentes_

    total_dias_ = sum(d for _, d in menus_con_dias) or 1

    # mercurio
    dp, fu = _frecuencia_generica(MERCURIO_ALTO, TOPE_MERCURIO_KCAL, "kcal")
    if fu and (dp / total_dias_) >= UMBRAL_FRECUENCIA_CRONICOS:
        avisos.append(
            "%s aparece de forma no trivial en %d de los 7 días de la semana. "
            "El mercurio se acumula en el cuerpo con exposiciones repetidas -- "
            "aunque cada menú esté dentro del límite por sí solo, conviene que "
            "no aparezca en la mayoría de los días de rotación."
            % (", ".join(sorted(fu)), dp))

    # vitamina D -- tope absoluto en µg (por 1000kcal del DER), usando el
    # umbral más estricto entre kcal y peso si el peso está disponible --
    # mismo criterio que en el chequeo por ración.
    tope_vitd_abs = TOPE_VITD_KCAL * der / 1000.0
    if peso_perro_kg and peso_perro_kg > 0:
        tope_vitd_por_peso = TOPE_VITD_KG075 * (peso_perro_kg ** 0.75)
        tope_vitd_abs = min(tope_vitd_abs, tope_vitd_por_peso)
    dp, fu = _frecuencia_generica("vitD", tope_vitd_abs, "nutriente")
    if fu and (dp / total_dias_) >= UMBRAL_FRECUENCIA_CRONICOS:
        avisos.append(
            "Hay una fuente relevante de vitamina D (%s) en %d de los 7 días de "
            "la semana. Es una vitamina que se acumula en el cuerpo -- revisa "
            "que no se estén sumando varias fuentes (pescado graso, aceite de "
            "hígado de bacalao, suplementos) de forma repetida."
            % (", ".join(sorted(fu)), dp))

    # yodo
    tope_yodo_abs = TOPE_YODO_KCAL * der / 1000.0
    dp, fu = _frecuencia_generica("yodo", tope_yodo_abs, "nutriente")
    if fu and (dp / total_dias_) >= UMBRAL_FRECUENCIA_CRONICOS:
        avisos.append(
            "Hay una fuente relevante de yodo (%s) en %d de los 7 días de la "
            "semana. El exceso de yodo mantenido puede alterar la tiroides -- "
            "si la fuente es kelp, su contenido real varía mucho de un "
            "producto a otro." % (", ".join(sorted(fu)), dp))

    # selenio
    tope_selenio_abs = TOPE_SELENIO_KCAL * der / 1000.0
    dp, fu = _frecuencia_generica("selenio", tope_selenio_abs, "nutriente")
    if fu and (dp / total_dias_) >= UMBRAL_FRECUENCIA_CRONICOS:
        avisos.append(
            "Hay una fuente relevante de selenio (%s) en %d de los 7 días de "
            "la semana -- suele ser vísceras (sobre todo riñón). El exceso "
            "sostenido de selenio, no solo puntual, puede causar problemas "
            "crónicos." % (", ".join(sorted(fu)), dp))

    return avisos
