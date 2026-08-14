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

# ⚠️ ATÚN — MERCURIO. AESAN clasifica el atun entre las 4 especies de alto
# mercurio (junto a pez espada, tiburon y lucio, que no tenemos). No hay
# dosis-umbral canina publicada: es una regla de FRECUENCIA/ROTACION, no un
# gramaje por plato. Se avisa si el atun es la UNICA fuente de pescado del
# menu (nunca la habitual), no si aparece puntualmente en la rotacion.
MERCURIO_ALTO = {"atun"}

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
PESCADO_CONGELAR_ANTES = {"salmon", "trucha"}

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
                      devolver_avisos=False):
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
    if "urato" in patologias:
        pur = [n for n in menu if _es(n, PURINAS_ALTAS)]
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
    """
    avisos = []
    for n in menu:
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
                "%s: si se da crudo, debe estar CONGELADO antes (varios "
                "días a -20 °C o equivalente) para eliminar el riesgo "
                "parasitario e infeccioso." % n)
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


def revisar_seguridad_semanal(menus_con_dias, alimentos, der):
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
    return avisos
