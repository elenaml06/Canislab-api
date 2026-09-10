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
TIAMINASA = {
    "sardina", "caballa", "arenque", "boqueron", "carpa",
    # ⚠️ AÑADIDO (5 agosto, madrugada) — investigación exhaustiva con
    # fuentes primarias (NRC 1983 Tabla 22, Hilker & Peter 1966/1968,
    # Tang & Hilker 1970): el atún (amarillo y listado) está confirmado
    # tiaminasa-positivo según el NRC, la referencia nutricional de mayor
    # rango. Las gambas/camarones y langostinos también contienen
    # tiaminasa (Fujita 1954, múltiples fuentes de acuariofilia y
    # nutrición animal). El "SIEMPRE cocinados" para mariscos es solo
    # texto informativo en el frontend -- el motor no tiene concepto de
    # "crudo vs cocinado", así que no puede garantizar que el usuario
    # los cocine de verdad; lo más consistente es que activen la misma
    # restricción del 10% que el pescado, cubriendo el caso de que
    # alguien los dé crudos. Solo se añaden los que existen de verdad
    # en el catálogo (confirmado antes de editar): atun, gamba, langostino.
    "atun", "gamba", "langostino",
}
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
# Tope por ración, mismo criterio que la tiaminasa. FUENTE: NRC 2006 fija un
# nivel tolerable de ingesta de mercurio TOTAL; esto es la transposición
# prudencial de ese nivel al porcentaje calórico del día. Es la única forma
# de la restricción que tiene base aplicable en perros.
#
# ⚠️ QUITADO (25 agosto, revisión clínica): aquí había además un
# `TOPE_MERCURIO_DIAS_SEMANA = 1`. Se quita por dos motivos, y los dos
# importan:
#
#   1. NO LO USABA NADIE. Estaba declarado y ninguna línea del repositorio lo
#      leía -- comprobado. O sea que la app decía tener una regla de "máximo
#      un día a la semana" que no se aplicaba en ningún sitio. Peor que no
#      tenerla: aparecía escrita en la documentación para la nutricionista
#      como si fuera una restricción real.
#   2. NO TIENE BASE EN PERROS. No existe estudio canino ni guía veterinaria
#      que fije una frecuencia semanal de pescado con mercurio. Ese "≤1
#      día/semana" es una transposición directa de las recomendaciones de
#      FDA/EFSA para embarazadas y niños pequeños, que son grupos de especial
#      sensibilidad al metilmercurio por su efecto neurotóxico sobre un
#      sistema nervioso EN DESARROLLO. Un perro adulto no es ese caso.
#
# Lo que sí queda es el 10% de las kcal del día, que es lo que se sostiene.
#
# Restricción por CONCENTRACIÓN calórica diaria, no por frecuencia. El único
# número de referencia que existe es el MTL de la FDA para mercurio en dieta
# canina, 0,27 mg/kg de materia seca -- y viene extrapolado de Charbonneau et
# al. 1976, que era en GATOS. Es un límite de concentración, no de cuántos
# días a la semana.
TOPE_MERCURIO_KCAL = 0.10

# ⚠️ AÑADIDO (26 agosto) — EPA+DHA, EL LÍMITE CRÓNICO.
#
# 2800 mg/1000 kcal. FUENTE: NRC 2006, recogido en Lenox & Bauer, JVIM
# 2013;27:217-226 (DOI 10.1111/jvim.12033). Es un SUL -- Safe Upper Limit --
# o sea una concentración de la DIETA HABITUAL, no el tope de un plato.
#
# Está aquí y NO como máximo en requerimientos_v2_final.json a propósito, y
# el motivo se midió: puesto como máximo por menú, 19 de los 20 pescados del
# catálogo lo pasan ELLOS SOLOS (de 2527 mg/1000 kcal el pulpo a ~11.000 el
# boquerón), porque el pescado tiene mucho omega-3 y muy pocas calorías. Un
# día entero eliminó el pescado azul de la app: los menús con pescado bajaron
# de 13 de cada 24 a 4.
#
# Se aplica sobre el PROMEDIO de la rotación semanal, por el mismo mecanismo
# de presupuesto que vitD y yodo (ver _presupuesto_semanal_inicial en
# main.py). Un día de pescado azul a la semana es exactamente lo que la
# fuente permite; siete no.
#
# FEDIAF 2025 no establece máximo de EPA+DHA: la columna Maximum de la Tabla
# III-3b está vacía.
TOPE_EPA_DHA_SEMANAL_KCAL = 2.8   # g por 1000 kcal, promedio de la semana

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
#
# ⚠️⚠️ CORREGIDO EL 9 DE SEPTIEMBRE DE 2026, Y EL ERROR ERA SERIO.
#
# Aquí ponía 1.400 µg/1000 kcal, y el comentario decía: «El NRC (2006) fija
# el límite superior seguro en 1.400 µg por cada 1000 kcal de dieta».
#
# **EL NRC DICE LO CONTRARIO.** Literal, cap.8, «Safe Upper Limit of Iodine
# for Dogs»:
#
#   «Castillo et al. (2001a) reported evidence of DEPRESSED THYROID GLAND
#    FUNCTION, evidenced by reduced plasma concentrations of thyroid hormones
#    AND BONE ABNORMALITIES, IN PUPPIES FED DIETS CONTAINING an estimated
#    maximum I content of 1,400 μg I per 1,000 kcal ME, providing an
#    estimated 250 μg I·kg BW-1·d-1. Based on this information AN ABSOLUTE
#    FIGURE FOR A SUL OF DIETARY I CANNOT BE PREDICTED for adult dogs.»
#
# O sea que los 1.400 son **la concentración a la que se observó el daño**, y
# el NRC dice expresamente que **no puede fijar un límite superior seguro**.
# Teníamos el techo puesto justo en la dosis que hace daño. Un techo ahí no
# es un techo.
#
# Es la misma familia de fallo que el máximo de fósforo borrado el 7 de
# septiembre: leer una línea de una fuente y aplicarla al revés.
#
# EL NUEVO NÚMERO SALE DE LA MISMA PÁGINA, no de mi criterio. El NRC cita a
# Belshaw (1975), que midió el yodo de varias marcas comerciales de pienso:
#
#   «The results corresponded to concentrations ranging, at a minimum, from
#    400 to 1,275 μg I per 1,000 kcal ME … APPARENTLY THESE FOODS WERE FED
#    WITHOUT ANY CLINICAL ABNORMALITIES in dogs consuming them.»
#
# Así que 1.275 es lo más alto que la fuente documenta como comido sin
# problemas, y por debajo de donde se vio el daño.
#
# ⚠️ MEDIDO ANTES DE BAJARLO, sobre los 216 menús del catálogo precalculado:
#       peor menú ......... 1.038 µg/1000 kcal
#       mediana ...........   418
#       por encima de 1.275 ...... 0 de 216
#       por encima de 1.000 ...... 2 de 216
# O sea que el cambio NO quita ni un menú: solo saca el techo del sitio donde
# hay daño documentado.
#
# ⚠️ LA PREGUNTA QUE HABÍA ABIERTA AQUÍ (PREGUNTAS_PARA_ELENA.md §1) LA
# CONTESTA FEDIAF, Y NO LA HABÍAMOS MIRADO (9 de septiembre).
#
# Era: «1.275 está a un 9 % de la cifra que hizo daño, y esa cifra es de
# CACHORROS; ¿bajamos más?». La respuesta está en FEDIAF 2025, sección 3.3.1,
# apartado «Iodine», y habla justo del estudio del que sale nuestro número.
# Literal:
#
#   «From studies by Castillo et al. (2001a, b) low nutritional maximum for
#    iodine in dogs (0.4 mg/100 g DM) was recommended. However in these studies
#    PUPPIES WERE SIGNIFICANTLY OVERFED (approx. 75 % above energy requirement)
#    which resulted in a substantially increased intake of iodine. Furthermore
#    the food was DEFICIENT IN A NUMBER OF KEY NUTRIENTS, e.g. Ca, P and K, and
#    therefore inappropriate for puppies. Consequently, THESE RESULTS ARE
#    IRRELEVANT for normal commercial nutritionally balanced foods, and THE
#    EXISTING LEGAL MAXIMUM IS SAFE FOR ALL DOGS.»
#
# O sea que el organismo que fija los requisitos ya evaluó ese estudio, explica
# por qué no aplica a una dieta equilibrada, y declara seguro el máximo legal
# entero: 2.750 µg/1000 kcal (Tabla III-3a, 1,10 mg/100 g MS x 2,5).
#
# NO SE CAMBIA NADA, y ahora se sabe por qué: nuestro 1.275 es **2,2 veces más
# estricto** que lo que FEDIAF considera seguro, y no cuesta ni un menú (el peor
# real va a 1.038). Bajarlo más tampoco haría falta -- no hay daño documentado
# en este rango para una dieta equilibrada --, y subirlo hasta el legal sería
# soltar un margen que hoy sale gratis. Se queda donde está, a propósito.
#
# La referencia del propio NRC para perro adulto son 220 µg/1000 kcal, así que
# incluso este techo es casi seis veces la recomendación.
#
# ⚠️ Por la enorme variabilidad del kelp, se aplica un margen de seguridad
# extra del 50% cuando el yodo del menú viene, en parte, de kelp -- para no
# confiar en una cifra de producto que en la práctica puede estar muy lejos
# de la real.
TOPE_YODO_KCAL = 1275.0    # µg por 1000 kcal -- NRC 2006, Belshaw 1975
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
# perros (JAVMA 2013;243(5):658).
#
# ⚠️ CORREGIDO (26 agosto) — LA BASE DE CÁLCULO ESTABA MAL, y es el tipo
# de error que no da ningún fallo: el tope se aplicaba como 2 µg por
# gramo de dieta sobre el PESO FRESCO. Los 2 mg/kg de Merck son en BASE
# MATERIA SECA. Una ración BARF lleva un 70-75% de agua, así que sobre
# fresco ese mismo límite son ~0,5-0,6 µg/g: aplicándolo sobre el peso
# tal cual se sirve, el tope real quedaba entre tres y cuatro veces más
# alto de lo que dice la fuente. Ningún menú salía marcado, y el número
# escrito en el código era el correcto -- lo que estaba mal era sobre qué
# se multiplicaba.
#
# Se pasa a la cifra de AAFCO, 570 µg por cada 1000 kcal, que es ESE
# MISMO límite de Merck ya convertido a base energética. La energía no
# depende del agua que lleve la ración, así que no hay ambigüedad de base
# de cálculo posible: es la forma correcta de expresarlo para una dieta
# cruda. Un solo tope, y en la unidad que no se puede malinterpretar.
#
# Se quita TOPE_SELENIO_G_DIETA en vez de dejarlo desconectado: una
# constante que parece un límite y no lo es es peor que no tenerla.
#
# FUENTES:
#   · Merck Veterinary Manual, "Selenium Toxicosis in Animals": 2 mg/kg
#     de dieta EN BASE MATERIA SECA.
#   · AAFCO: 0,57 mg por cada 1000 kcal -- el equivalente energético.
#   · Zentrichová V et al. (2021), Animals 11(2):418 (PMID 33562028):
#     revisión sistemática del selenio en el perro. No hay casos de
#     intoxicación natural documentados, pero las dietas CRUDAS tienen
#     una biodisponibilidad de selenio mucho más alta (~91%) que las
#     procesadas (47-79%) -- o sea que en BARF el mismo número de
#     microgramos llega más entero, y aflojar la base de cálculo es
#     justo lo contrario de lo que pide este alimento.
#
# MEDIDO en 18 menús de seis perfiles (adulto de 5, 20 y 40 kg, cachorro
# en crecimiento, renal y cardiopatía): el máximo fue 142 µg/1000 kcal,
# cuatro veces por debajo de los 570. El tope correcto no deja sin menú a
# nadie.
TOPE_SELENIO_KCAL = 570.0    # µg por 1000 kcal -- AAFCO (= 2 mg/kg MS de Merck)

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
# ⚠️ AMPLIADA (8 septiembre) — LA LISTA ERA DE CUATRO Y LA FUENTE MARCA
# CATORCE QUE TENEMOS. Hasta hoy esto eran "espinaca, acelga, ruibarbo,
# remolacha": conocimiento general, sin una tabla detrás, y de esas cuatro
# solo dos existen en el catálogo (ruibarbo y remolacha no están).
#
# SACN5 5ª ed., cap.40, Tabla 40-3 «Selected human foods to limit or avoid
# feeding to dogs with calcium oxalate uroliths», columna «Moderate/high-
# oxalate foods», tiene la lista de verdad y la gradúa: (H) = «high; avoid
# feeding», (M) = «moderate; feed in limited amounts». Se excluyen SOLO las
# (H), que es lo que la fuente manda evitar. Verificado literal el 8-sep-2026.
#
# Las (M) NO se excluyen a propósito, y una de ellas conviene conocerla: la
# SARDINA es «Sardines (M)», la única de la lista que no es verdura ni fruta.
# Las otras (M) del catálogo son brócoli, espárrago, lechuga, pera, piña,
# tomate, zanahoria y naranja.
#
# La ACELGA y el RUIBARBO se quedan aunque NO estén en la Tabla 40-3: son
# los dos casos clásicos de oxalato alto y estaban aquí antes con criterio
# clínico general. Se marcan como tales para que se sepa cuáles vienen de la
# tabla y cuáles no -- que es justo lo que faltaba en la versión de cuatro.
#
# ⚠️ Y ESTO ES LO ÚNICO que excluye alimentos por oxalato. Cuando el 8 de
# septiembre se escribió que «el oxalato no ajusta nada», era verdad solo a
# medias: no aplicaba ningún tope NUMÉRICO (sodio, fósforo, magnesio se
# añadieron ese día), pero la exclusión de alimentos sí existía desde el 5 de
# agosto. Ver PATOLOGIAS.md §1.2.
_OXALATO_TABLA_40_3 = {
    # Verduras marcadas (H) en la Tabla 40-3
    "apio",           # Celery (H)
    "berenjena",      # Eggplant (H)
    "boniato",        # Sweet potatoes (H)
    "calabacin",      # Summer squash (H)
    "espinaca",       # Spinach (H)
    "judia verde",    # Green beans (H)
    "pepino",         # Cucumber (H)
    "pimiento",       # Green peppers (H)
    # Frutas marcadas (H)
    "albaricoque",    # Apricots (H)
    "arandano",       # Most berries (H)
    "frambuesa",      # Most berries (H)
    "fresa",          # Most berries (H)
    "mandarina",      # Tangerine (H)
    "manzana",        # Apples (H)
    # Frutos secos marcados (H)
    "cacahuete",      # Peanuts (H)
    "soja",           # Soybeans (H)
    "tofu",           # Tofu (H)
}
_OXALATO_CRITERIO_CLINICO = {
    # No están en la Tabla 40-3, pero son los dos casos clásicos y estaban
    # aquí desde antes. Se conservan; queda escrito que no vienen de la tabla.
    "acelga",
    "ruibarbo",
    "remolacha",
}
OXALATO_ALTO = _OXALATO_TABLA_40_3 | _OXALATO_CRITERIO_CLINICO

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

# ⚠️ LA HISTAMINA DEL PESCADO MAL CONSERVADO (9 de septiembre de 2026, leyendo
#     ENTERA la §7.6 de FEDIAF, que hasta ese día estaba sin leer).
#
# FEDIAF §7.6.2.4, literal, en el apartado que se titula «All individuals
# susceptible if sufficient quantity eaten»:
#
#   «Pharmacologic reaction — Adverse reaction to a food as result of a
#    naturally derived or added chemical producing a drug-like or
#    pharmacological effect in the host such as methylxanthines in chocolate
#    or **pseudo-allergic reactions caused by high histamine levels in not
#    well-preserved scombroid fish (e.g. tuna)**»
#
# POR QUÉ ESTO ES NUESTRO Y NO DE OTRO. Servimos pescado CRUDO, y cuatro de las
# especies del catálogo son de las que forman histamina: Atún y Caballa
# (Scombridae), Sardina (Clupeidae) y Boquerón (Engraulidae). No es una lista
# nuestra: son tres de las seis familias que nombra el Reglamento (CE) 2073/2005
# al fijar el límite de histamina «productos de la pesca de especies de peces
# asociadas a un alto contenido de histidina».
#
# Y POR QUÉ NO ES LO MISMO QUE LO QUE YA HABÍA, que es la pregunta que hay que
# hacerse antes de añadir un aviso más:
#   · El tope de MERCURIO (atún) es un metal que se acumula. Otro mecanismo.
#   · El aviso de aminas vasoactivas de `reaccion_adversa_alimento` (SACN5
#     cap.31) sale SOLO si esa patología está marcada, y habla de bajar el
#     umbral de un perro YA sensible.
#   · Esto es de FEDIAF, va en el apartado «TODOS los individuos son
#     susceptibles si comen cantidad suficiente», y no depende de que el perro
#     tenga nada: depende de cómo se haya conservado el pescado. Un perro sano
#     con una caballa que rompió la cadena de frío tiene el mismo problema.
#
# LO QUE NO SE HACE, y es a propósito: no se topa la cantidad ni se saca el
# pescado del catálogo. La histamina no la genera el pez, la genera la mala
# conservación, y es TERMORRESISTENTE — cocinar y congelar no la destruyen una
# vez formada, así que un tope en gramos no arregla nada y un pescado bien
# conservado no tiene ningún problema. Lo que hay que decir es cuándo se forma.
PESCADO_HISTAMINA = {"atun", "caballa", "sardina", "boqueron"}

# ⚠️ Y LA CIFRA QUE FALTABA AQUÍ, DE SACN5 cap.50 (9 de septiembre de 2026).
#
# Estas dos listas son POR CORTE: dicen qué hueso concreto tiene qué riesgo. Lo
# que no había era la magnitud del riesgo general de dar hueso, y existe
# publicada. SACN5 cap.50, literal, citando a Rousseau et al. (2007):
#
#   «In a recent retrospective review, **46 of 60 esophageal foreign bodies
#    removed from dogs were bones»
#
# Cuarenta y seis de sesenta. No es un argumento contra el hueso carnoso —una
# ración BARF lleva entre un 20 y un 60 % y es su fuente de calcio— pero sí es
# el número que hay que tener delante al decidir qué cortes se ofrecen y con qué
# aviso, y al contestar a un dueño que pregunta si es peligroso. La respuesta
# honesta no es «no», es «el hueso es la primera causa de cuerpo extraño
# esofágico en el perro, y por eso estos dos conjuntos existen».
#
# ⚠️ Y EL SEGUNDO NÚMERO, DE SACN5 cap.47 (mismo día, leído entero).
#
# El capítulo de enfermedad periodontal trae el recuadro 47-6, «Natural Food
# Sources and Periodontal Disease», con el estudio de **67 foxhounds ingleses**
# de uno a nueve años alimentados de rutina con carcasas crudas —esqueleto,
# músculo y tejidos asociados—: «Oral examinations revealed that **all dogs had
# varying signs of periodontal disease as well as a high prevalence of tooth
# fractures**».
#
# Y el caso 47-1 va directo al argumento del hueso carnoso crudo: «there are **no
# reliable, published studies showing dental benefits derived from bone
# chewing** … anecdotal reports suggest the health concerns presented with cooked
# bones **also occur commonly with raw, meaty bones** … The safety and efficacy of
# feeding bones, regardless of type, remain undetermined».
#
# LO QUE ESTO CAMBIA AQUÍ: nada del motor, y a propósito. El hueso carnoso está
# en el catálogo porque es la fuente de calcio de una ración BARF, no por los
# dientes, y este capítulo no toca esa razón. Lo que desmonta es un beneficio que
# Rawku **nunca ha prometido**: se comprobó `instrucciones.js` de `canislab-web`
# entero el 9 de septiembre y no hay ni una afirmación dental — lo que dice del
# hueso carnoso es crudo siempre, entero o en trozos grandes, que lo roa y no lo
# trague, supervisado, y esperar a las 14 semanas para los duros.
#
# Se escribe aquí para que la cautela esté CITADA y para que, si algún día se
# escribe en la app que el hueso limpia los dientes, alguien encuentre esto
# antes.
#
# El mismo capítulo trae la otra mitad, que es la que hace que el riesgo importe
# poco o mucho según el corte: los cuerpos extraños esofágicos son de los que se
# tragan enteros. Un hueso que el perro roe y muele no es el mismo problema que
# uno que le cabe en la garganta de una pieza.

# ⚠️ BORRAJA — ALCALOIDES PIRROLIZIDÍNICOS (PA) HEPATOTÓXICOS. La HOJA (que
# es lo que se da en BARF) contiene PA hepatotoxicos y carcinogenicos
# (amabilina, licopsamina). EFSA fijo niveles maximos y la UK FSA
# recomienda EVITAR las infusiones de hoja. El aceite de semilla de borraja
# casi no lleva PA (es otra parte de la planta), pero como hoja NO se debe
# dar de forma habitual. A diferencia de la tiaminasa o el oxalato, aqui NO
# hay una dosis segura publicada por debajo de la cual esta bien: se
# EXCLUYE, no se topa.
# ⚠️ Y DESDE EL 27 DE AGOSTO YA NO ESTA EN EL CATALOGO. Esta exclusion se
# escribio en agosto y hacia la mitad del trabajo: sacaba la borraja del
# menu AUTOMATICO, y por eso no salia en ninguno de los 30 menus que se
# midieron. Pero el alimento seguia en `alimentos_v3_final.json`, o sea en
# `/alimentos`, o sea en el selector de Personalizar -- donde cualquiera
# podia elegirla a mano y el motor la aceptaba sin rechistar.
# Excluir de lo automatico y dejar en el selector es media exclusion, y
# para un hepatotoxico acumulativo sin dosis segura publicada media
# exclusion no vale.
#
# Ademas su ficha traia 13 ug de vitamina D, que es IMPOSIBLE: ninguna
# planta sintetiza colecalciferol. Era el unico vegetal del catalogo con
# vitamina D, y con mas que cualquier pescado. Lo que eso significa se ve
# mejor mirando lo que estuvo a punto de pasar: se estaba disenando un
# suelo de vitamina D "que un 30% venga de la comida y no del suplemento",
# y 13 g de borraja lo satisfacian ENTEROS. Una restriccion nueva habria
# entrado en verde sin obligar a nada, desactivada por una sola fila.
#
# Este conjunto se queda por si alguien la vuelve a meter: la exclusion
# tiene que seguir funcionando aunque el alimento reaparezca.
BORRAJA_EXCLUIR = {"borraja"}

# ⚠️ TEJIDO TIROIDEO — HIPERTIROIDISMO EXOGENO (6 septiembre). El cuello y
# la garganta de un animal de abasto suelen llevar la glandula tiroides
# pegada si no se retira a proposito, y con uso REGULAR (no una vez) esa
# hormona tiroidea puede darle al perro una tirotoxicosis exogena.
# FUENTE, literal, confirmada en el PDF (no en el .txt extraido):
# TVT Merkblatt 181 BARF, Mai 2025 (Tierarztliche Vereinigung fur
# Tierschutz e.V.), pagina 5: "Verfutterung von Schlundfleisch und
# Huhnerhalsen: daran befindet sich in der Regel noch die Schilddruse der
# geschlachteten Tiere, was bei regelmassiger Verfutterung aufgrund des
# Gehaltes an Schilddrusenhormonen zu einer Schilddrusenuberfunktion
# (Hyperthyreose) bei Hunden fuhren kann." Identico en la edicion de Juli
# 2017 -- comprobado linea a linea, no cambio nada entre las dos.
# Cuatro fichas del catalogo caen en esta zona anatomica: Cuello de pavo,
# Cuello de pato y Cuello de ternera (las tres en la lista automatica de
# huesos -- HUESO en accesibles.py -- asi que hoy se ofrecen a CUALQUIER
# perro sin que nadie las pida) y Laringe de vacuno (fuera del automatico
# por otro motivo -dificil de encontrar, poco calcio- pero elegible a mano
# en Personalizar). Es un bloqueo de nivel A: no lo levanta ni un
# veterinario, igual que la borraja.
# No se borran del catalogo en esta pasada porque `catalogo_menus.json`
# (los menus precalculados de la vista previa) tiene 56 referencias a
# estos cuatro nombres -- borrarlos de golpe dejaria huerfanas esas filas.
# `_garantizar_verificado()` las rechazaria igual (esta exclusion tambien
# se aplica ahi, ver mas abajo), asi que no es inseguro, pero regenerar
# ese catalogo es su propio trabajo, no colarlo aqui. Igual que con la
# borraja: la exclusion va primero, en codigo; el catalogo se limpia
# despues, aparte.
TIROIDES_EXCLUIR = {"cuello", "laringe", "traquea", "esofago", "garganta"}

# ⚠️ LOS ALIMENTOS HUMANOS QUE FEDIAF DECLARA TOXICOS (10 septiembre de 2026).
#
# Salen del ANEXO 7.7 de FEDIAF, «Risks of some human foods regularly given to
# pets», leido entero hoy. Hasta hoy ese anexo no estaba en ninguna parte del
# repo, y el motivo por el que no se noto es el peor posible: **hoy no hay
# ninguno en el catalogo** -- comprobado sobre las 163 fichas --, asi que la
# ausencia de la lista no daba error, no daba aviso y no cambiaba ningun menu.
#
# Es exactamente el patron del oxido de cobre y del oxido de hierro: una regla
# de la fuente que hoy no muerde y que el dia que muerda ya no habra nadie
# mirando. El coste de escribirla es cero y el de no escribirla es una ficha de
# uva o de cebolla entrando sin que salte nada.
#
# LAS CIFRAS, literales del anexo:
#
#   · Uva y pasa: «The lowest intake that has so far been reported to cause
#     poisoning is around 2.8 g of raisins per kg bodyweight (BW) and 19.6 g of
#     grapes per kg BW; one dog became ill after only eating 10 to 12 grapes».
#     Y ademas: «The severity of the illness does not seem to be dose-related»
#     -- o sea que no hay una dosis segura de la que fiarse. Solo el perro se ve
#     afectado; el extracto de uva no, tiene que comerse la fruta.
#   · Chocolate y cacao: el toxico es la teobromina, «particularly toxic to
#     dogs, because its elimination is very slow», vida media ~17,5 h y
#     recirculacion enterohepatica -- «repeated intakes of smaller (non-toxic)
#     quantities may still cause intoxication». Tampoco hay dosis segura por
#     acumulacion.
#   · Cebolla, ajo y el resto del genero Allium: el anexo los nombra en su
#     entrada («raisins, grapes, onions, garlic and chocolate»).
#
# NO SE PONE UNA DOSIS MAXIMA A PROPOSITO. La propia fuente dice de los dos
# primeros que la gravedad no depende de la dosis y que dosis pequenas repetidas
# intoxican igual. Un tope numerico aqui seria inventarse una seguridad que la
# fuente niega: van fuera, en cualquier cantidad, como la borraja y el tiroides.
TOXICOS_FEDIAF_7_7 = {
    "uva", "uvas", "pasa", "pasas", "sultana", "chocolate", "cacao",
    "cebolla", "cebolleta", "ajo", "puerro", "chalota", "cebollino",
}

# ⚠️ RESTRICCIONES POR PATOLOGIA — investigadas 4 agosto, mismo patron que
# el oxalato/urato: en perro SANO no se tocan, solo se activan si la
# patologia esta declarada. Los datos concretos viven en el propio
# alimento (campo "restricciones_patologia" del catalogo).
# Aqui solo se listan que categorias de patologia hay que comprobar.
# ─── VALORES CONFIRMADOS EN LA REVISIÓN CLÍNICA DEL 25 DE AGOSTO ────────────
#
# Estos NO cambiaron de número. Se dejan escritos con su fuente porque
# "revisado y correcto" y "nadie lo ha mirado nunca" se parecen demasiado
# mirando el código, y la diferencia importa cuando alguien vuelva dentro de
# seis meses a decidir si un tope se puede aflojar.
#
#   Tiaminasa, máx 10% de las kcal
#       Correcto y conservador. NO hay umbral oficial: la literatura
#       (Kritikos 2017) habla de riesgo cuando el pescado tiaminásico es
#       "proporción sustancial de la dieta", sin dar cifra. El 10% es
#       criterio nuestro -- ver el comentario de TIAMINASA más arriba.
#
#   Vitamina D crónica, ≤20 µg/1000 kcal
#       Correcto y conservador. NRC 2006 / Lenox & Bauer 2013.
#
#   Yodo crónico, ≤1400 µg/1000 kcal
#       Correcto y conservador A PROPÓSITO: el NRC da ~2750 µg. Se usa un
#       umbral bastante más bajo por decisión nuestra.
#
#   Selenio crónico, ≤570 µg/1000 kcal
#       Correcto. Es el valor de AAFCO. Merck da 2 µg/g de dieta, que sale
#       ≈500 µg/1000 kcal -- las dos referencias no coinciden exactamente y
#       se usa la de AAFCO. Queda anotada la discrepancia.
#
#   Mercurio (atún), máx 10% de las kcal y ≤1 día/semana
#       Correcto y prudencial. NO existe estudio dosis-respuesta en perro:
#       el criterio es la bioacumulación, no una cifra medida.
#
#   Calcio de cachorro de raza grande, 2500-4500 mg/1000 kcal
#       Correcto. Hazewinkel; Dobenecker et al. 2006 (JAPN).
#
#   Corte de etapa cachorro: 14 SEMANAS
#       Correcto -- y es el de FEDIAF, literal: sus tablas de requisitos
#       titulan las dos columnas «Early Growth (< 14 weeks)» y «Late Growth
#       (>= 14 weeks)». Aquí ponía «4 meses» (unas 17 semanas) y se defendía
#       como margen conservador deliberado, que es otra forma de decir que nos
#       inventábamos un umbral existiendo el de la fuente. Cambiado el 9 de
#       septiembre en `canislab-web/src/der.js`, que es donde se decide la
#       etapa; lo vigila `tests/der-contrato.spec.js`.
#
#   Ratio Ca:P — adulto 1,0-2,0 · crecimiento tardío 1,0-1,8
#       Correctos. FEDIAF.
#
#   EPA+DHA en crecimiento, ≥130 mg/1000 kcal
#       Correcto. FEDIAF 2025. (El de ADULTO no es de FEDIAF: ver la
#       nota_auditoria de esa fila en requerimientos_v2_final.json.)

PATOLOGIAS_CON_RESTRICCION_ALIMENTO = {"hipotiroidismo", "diabetes", "pancreatitis"}


def _es(nombre, conjunto):
    p = _palabras(nombre)
    n = _norm(nombre)
    return any((t in n) if " " in t else (t in p) for t in conjunto)


def revisar_seguridad(menu, alimentos, der, etapa="Adulto", patologias=None,
                      devolver_avisos=False, peso_perro_kg=None, requerimientos=None):
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
    tope_selenio = TOPE_SELENIO_KCAL * der / 1000.0
    if der and selenio_ug > tope_selenio:
        problemas.append(
            "El selenio de este menú llega a %.0f µg, por encima del límite "
            "tolerable (%.0f µg). El riñón es la fuente más concentrada -- revisa "
            "si hay mucha cantidad de vísceras o de suplemento junto con pescado "
            "en el mismo menú."
            % (selenio_ug, tope_selenio))

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

    # 3b-ter. TEJIDO TIROIDEO — cuello, garganta y laringe pueden traer la
    # tiroides del animal pegada. TVT Merkblatt 181 (mayo 2025): con uso
    # regular, riesgo de hipertiroidismo exógeno. Bloqueo de nivel A, igual
    # que la borraja: no se topa por cantidad, se excluye del todo.
    tox = [n for n in menu if _es(n, TOXICOS_FEDIAF_7_7)]
    if tox:
        problemas.append(
            "%s está en la lista de alimentos humanos con toxicidad documentada "
            "en el perro (FEDIAF, anexo 7.7). No hay una cantidad segura: la "
            "propia fuente dice que en la uva y la pasa la gravedad no depende "
            "de la dosis, y que en el chocolate dosis pequeñas repetidas "
            "intoxican igual por acumulación. Fuera de la ración."
            % ", ".join(tox))

    tir = [n for n in menu if _es(n, TIROIDES_EXCLUIR)]
    if tir:
        problemas.append(
            "%s puede llevar la glándula tiroides del animal pegada — con "
            "uso regular puede causar hipertiroidismo exógeno en el perro. "
            "No se recomienda en ninguna cantidad habitual (TVT Merkblatt "
            "181, mayo 2025)." % ", ".join(tir))

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

    # ⚠️ DOS AVISOS DE FEDIAF QUE ESTABAN LEIDOS Y NO SE DECIAN (10 septiembre).
    #
    # Los dos salen de leer FEDIAF 2025 entera, y los dos son AVISO y no cifra
    # a proposito: la fuente describe el riesgo y NO da un numero, asi que
    # ponerle un tope seria inventarselo -- y callarse tampoco vale, porque el
    # motor construye justo las raciones donde el riesgo aparece.

    # 1. CORDERO Y TAURINA (Anexo 7.3.3, «Dog»). «Feeding certain LAMB and rice
    #    foods MAY INCREASE THE RISK OF A LOW-TAURINE STATUS, because of lower
    #    bioavailability of sulphur-containing amino acids and increased faecal
    #    losses of taurine». Y en la misma pagina: «some breeds seem to be more
    #    sensitive... particularly NEWFOUNDLAND DOGS, in which the rate of
    #    taurine synthesis is decreased».
    #    La taurina NO esta entre los 43 requisitos porque el perro sano la
    #    sintetiza de metionina y cisteina -- lo dice la propia FEDIAF --, asi
    #    que un menu de cordero sale VERDE y nadie ve el riesgo. El objetivo que
    #    da la fuente es de analitica (>40 µmol/L en plasma), no de receta.
    cordero = [n for n in menu if _es(n, {"cordero", "ovino", "oveja", "borrego"})]
    if cordero:
        avisos.append(
            "Este menú lleva cordero (%s). FEDIAF (anexo 7.3.3) relaciona las "
            "dietas de cordero con un riesgo mayor de taurina baja, porque sus "
            "aminoácidos azufrados se aprovechan peor. El perro sano fabrica su "
            "propia taurina y no hace falta añadirla, pero hay razas que la "
            "sintetizan peor —FEDIAF nombra al Terranova— y en ellas conviene "
            "que el veterinario mire la taurina en sangre. No es un problema "
            "del menú: es algo que preguntar si el perro es de esas razas."
            % ", ".join(cordero))

    # 2. LA HISTAMINA DEL PESCADO ESCOMBROIDE YA ESTABA, Y AQUI LA PUSE
    #    DUPLICADA (10 septiembre, y lo cazo la propia prueba de extremo a
    #    extremo). Leyendo §1.1 de FEDIAF -- la definicion de «pharmacologic
    #    reaction», que nombra la histamina del escombroide mal conservado --
    #    escribi un aviso nuevo, y resulta que el mismo pasaje de FEDIAF ya
    #    estaba aplicado desde antes en `avisos_rotacion()`, con mejor
    #    redaccion y con el razonamiento escrito de por que no es lo mismo que
    #    el mercurio ni que las aminas vasoactivas de la reaccion adversa.
    #
    #    Se quita el mio. Dos avisos diciendo lo mismo es peor que uno: «un
    #    aviso que sale siempre deja de leerse», que es la regla con la que se
    #    decidio no meter mas ruido en esa lista.
    #
    #    Lo que si faltaba, y era el fallo de verdad, es que ESTA LISTA no
    #    salia de la API: `main._seguridad_completa` llamaba a esta funcion sin
    #    `devolver_avisos=True`, asi que todo lo de aqui abajo se construia y se
    #    tiraba. Arreglado alli.

    # 3. EL CALCIO CERCA DE SU TECHO SE LLEVA POR DELANTE EL ZINC Y EL COBRE
    #    (10 septiembre). FEDIAF lo dice DOS VECES y las dos sin cifra:
    #
    #      §3.3.1, «Calcium (Adult dogs)»: «As the calcium level approaches the
    #      stated nutritional maximum, IT MAY BE NECESSARY TO INCREASE the
    #      levels of certain trace elements such as ZINC and COPPER.»
    #
    #      nota g de las tablas: «The bioavailability of minerals should be
    #      carefully considered in diet formulas where the concentration of
    #      these nutrients is close to the recommended amounts.»
    #
    #    Y SACN5 cap.6 SI le pone numero al punto donde empieza: «as calcium
    #    levels increased FROM 1.0 TO 1.5 %, zinc usage (as measured by changes
    #    in plasma zinc) decreased» en cachorros, y de 1,2 a 3,2 % baja la
    #    retencion de zinc segun la forma quimica del zinc.
    #
    #    NOS TOCA DE LLENO: una racion BARF cierra el calcio con hueso, asi que
    #    va alta por construccion.
    #
    #    LO QUE NO SE HACE, y es a proposito: no se sube el minimo de zinc ni el
    #    de cobre. Ninguna de las dos fuentes dice CUANTO, y subir un minimo a
    #    ojo es inventarse la cifra -- ademas de que el zinc tiene techo legal y
    #    apretarlo por abajo cierra la ventana. Lo que se hace es DECIRLO,
    #    cuando de verdad esta cerca: a partir del 85 % de su maximo.
    # ⚠️ El maximo se PIDE, no se carga aqui: la tabla de FEDIAF se lee en un
    # solo sitio y quien llama ya la tiene. Si no lo pasan, no se avisa -- antes
    # callarse que inventarse el techo.
    _max_ca = None
    if requerimientos:
        from verificar import maximo_de as _max_de_ca
        _fila_ca = requerimientos.get("Calcio")
        if _fila_ca:
            _max_ca = _max_de_ca(_fila_ca, "Calcio", etapa)
    if _max_ca and der:
        _ca = sum((alimentos.get(n, {}).get("nutrientes", {}).get("calcio") or 0) * g / 100.0
                  for n, g in menu.items())
        _ca_1000 = _ca / der * 1000.0
        if _ca_1000 >= _max_ca * 0.85:
            avisos.append(
                "El calcio de esta ración va al %.0f %% de su máximo (%.0f de %.0f mg por "
                "1000 kcal). No se pasa, pero FEDIAF avisa de que con el calcio alto puede "
                "hacer falta más zinc y más cobre, porque se absorben peor. Es normal en una "
                "ración con hueso; si el perro es de los que se le nota en la piel o el pelo, "
                "es algo que comentar con el veterinario."
                % (100.0 * _ca_1000 / _max_ca, _ca_1000, _max_ca))

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
            if _es(n, PESCADO_HISTAMINA):
                avisos.append(
                    "%s: es de las especies que acumulan histamina si se rompe "
                    "la cadena de frío. Compralo bien frío y dalo el mismo día "
                    "que lo descongeles; si huele fuerte o pica en la lengua, "
                    "tíralo. La histamina no se va ni congelando ni cocinando "
                    "una vez formada, y puede dar una reacción parecida a una "
                    "alergia en cualquier perro, no solo en uno alérgico "
                    "(FEDIAF 2025, §7.6.2.4)." % n)
            # ⚠️ QUITADO (5 agosto, madrugada) — pedido expreso: este aviso
            # ("congelar antes de dar") era redundante con la instrucción
            # general de la categoría "Pescados y mariscos" en el
            # frontend, que ya cubre la duración de congelación (2
            # semanas) para cualquier pescado -- no hace falta repetirlo
            # aquí, alimento por alimento, además. PESCADO_CONGELAR_ANTES
            # se deja definido por si algún día hace falta en otro sitio,
            # simplemente ya no dispara este aviso concreto.
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
