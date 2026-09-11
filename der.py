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

=============================================================================
POR QUÉ NO HAY UN FACTOR DE ENFERMEDAD (verificado 7-sep-2026, no de memoria)
=============================================================================
El método AMERICANO (arriba) multiplica el RER por un factor por
enfermedad/lesión -- 1,1 a 2,3 según la tabla de Remillard & Thatcher 1989,
la misma que cita literal Fascetti & Delaney, Applied Veterinary Clinical
Nutrition 2ª ed. (Wiley-Blackwell, 2024), cap.3 "Determining Energy
Requirements" (Ramsey), verificado contra el libro (no contra un resumen).
Esta app NUNCA ha aplicado nada así, y no es un hueco: es la recomendación
de la propia fuente. Tres citas literales del capítulo:

  "These factors have not been extensively tested in dogs and cats, and use
   of these equations assumes that dogs and cats will have similar
   energetic responses to disease and injury to humans. [...] it seems
   reasonable to target energy requirements for most sick or injured dogs
   and cats initially at RER, followed by adjustments based on individual
   progress."

  "It should rarely be necessary to feed injured or ill cats and dogs above
   the predicted energy requirement for a healthy animal at maintenance."

  "Weight loss is never a goal during treatment and recovery from trauma
   and critical illness."

Ninguna patología de `patologias.json` toca esta fórmula ni recibe un
multiplicador propio: el DER de un perro enfermo se calcula EXACTAMENTE
igual que el de uno sano de su mismo peso/etapa/actividad, y eso es lo
correcto según la fuente, no un descuido. La última cita sí motivó un
cambio real: `main.py` avisa (vía `aviso_si_ademas` en `obesidad`) si se
intenta combinar un objetivo de adelgazamiento con una patología aguda o
crítica (`fracaso_renal_agudo`, `encefalopatia_hepatica`, `cancer_soporte`,
`inmunosupresion`, `pancreatitis`) -- ver PENDIENTE_NUTRICION.md.
"""

import math

# =============================================================================
# ADULTOS — base por actividad (kcal por kg de peso metabólico)
# =============================================================================
# ⚠️ CORREGIDO 6-sep-2026: es la TABLA VII-7 de FEDIAF ("Recommendations for
# DER in relation to activity"), no la VII-6 (esa es solo por EDAD, sin
# actividad -- confirmado literal en fediaf_2025.txt, los 5 valores de aqui
# (95/110/125/150-175) cuadran exactos con esa tabla, no con la VII-6.
# La media MEDIDA en 586 perros de compania (Thes et al. 2015 -- FEDIAF lo
# cita como "Thes M et al. 2015" en su propia bibliografia, no 2014) fue 98,
# o sea justo entre "baja" (95) y "moderada bajo impacto" (110). Encaja.
BASE_ACTIVIDAD = {
    "sedentario":   95,    # baja: menos de 1 h/dia, casi siempre con correa
    "normal":      110,    # moderada 1-3 h/dia, bajo impacto
    "activo":      125,    # moderada 1-3 h/dia, ALTO impacto
    "muy_activo":  150,    # alta 3-6 h/dia (perro de trabajo, pastoreo)
    "trabajo":     175,    # alta, extremo superior del rango de FEDIAF
    # FEDIAF llega a 860-1240 para perros de trineo en frio extremo; eso no
    # lo cubre esta app y tendria que pautarlo un veterinario.
}

# ⚠️ LO QUE LA §7.2.3.5 DE FEDIAF ANADE A ESTA TABLA, Y QUE NO SE APLICA
#     (9 de septiembre de 2026, leyendo esa seccion entera; hasta ese dia
#     estaba sin leer).
#
# La tabla de arriba es la VII-7, o sea la RECOMENDACION PRACTICA de FEDIAF. La
# §7.2.3.5 es su revision de literatura, y trae tres cosas que la tabla no dice.
# Ninguna se aplica, y cada una por un motivo distinto -- escritas aqui para que
# no haya que volver a descubrirlas:
#
# 1. EL FRIO, QUE ES UN HUECO DE VERDAD. Literal: «When kept outside in winter,
#    dogs may need 10 to 90 % MORE CALORIES than during summer». Diez a noventa
#    por ciento. Y esta app NO PREGUNTA DONDE VIVE EL PERRO: un mastin que duerme
#    fuera en enero recibe hoy la misma racion que un perro de piso.
#    ⚠️ Y LA CIFRA EXISTE, aunque no la de FEDIAF: la trae SACN5 cap.5, Tabla 5-3
#    («Influence of low environmental temperatures on daily energy requirement»),
#    por TIPO DE PELO y por salto de temperatura concreto:
#
#        Labrador y beagle ...... +25 %   (12-43)   de 15 C a 8,5 C
#        Gran Danes ............. +22 %             de verano a invierno
#        Perro de pelo CORTO .... +95 %             de 25 C a 7,6 C
#        Perro de pelo LARGO .... +59,5 %           de 25 C a 7,6 C
#        Beagle ................. +70,5 %           de 17 C a -17 C
#        Perro de trineo ........ +61,5 %           de 17 C a -17 C
#
#    Ojo al sentido, que es el contrario del que uno diria de memoria: el de pelo
#    CORTO necesita mas subida que el de pelo largo, porque aisla peor.
#
#    ASI QUE LO QUE FALTA NO ES LA CIFRA: ES LA PREGUNTA. La ficha no sabe donde
#    duerme el perro ni a que temperatura, y sin eso no hay a que fila ir. Anadir
#    esa pregunta es una decision de producto (que se pregunta exactamente, y con
#    que palabras), no de lectura, y por eso no se aplica sola. Esta en
#    PENDIENTE_PRODUCTO.md con las dos citas -- la de FEDIAF y esta -- para que se
#    decida con los numeros delante. Lo que SI se puede decir mientras tanto es lo que ya dice la
#    §7.2.4 de FEDIAF y la app repite: la racion es un punto de partida y se
#    ajusta viendo si el perro engorda o adelgaza.
#
# 2. EL SUELO DE 95 NO ES EL SUELO DE LA LITERATURA. Literal: «Individually housed
#    dogs, with little opportunity to move, may have daily energy requirements
#    (DER) AS LOW AS 70 kcal ME/kg0.75». Nuestro «sedentario» son 95, o sea que a
#    un perro de verdad muy quieto podemos darle hasta un 36 % de mas.
#    NO SE BAJA A PROPOSITO: 95 es lo que FEDIAF RECOMIENDA en su Tabla VII-7, y
#    70 es lo que documenta su revision de literatura para perros enjaulados. Son
#    dos cosas distintas y la que manda es la recomendacion. Ademas el error va
#    del lado que se corrige solo -- el dueño ve que engorda y baja la racion --,
#    y el contrario no. El otro extremo de la misma frase, «over 144 kcal
#    ME/kg0.75» para perros en jauria con mucha interaccion, SI cae dentro de
#    nuestra tabla (entre «activo» y «muy_activo»), asi que ahi no falta nada.
#
# 3. LA TERMOGENESIS DE LA PROPIA COMIDA, que nos toca mas que a un pienso.
#    Literal: «Diet-induced thermogenesis plays a small role; it represents about
#    10 % of the daily energy expenditure in dogs. It INCREASES WITH DIETS RICH IN
#    PROTEIN and is greater in dogs fed FOUR MEALS PER DAY than in dogs fed once
#    daily». Una racion BARF es rica en proteina por construccion y la app
#    reparte en 2-3 tomas, o sea que caemos en el lado alto de las dos.
#    NO SE APLICA porque FEDIAF da el total («about 10 %») y NO da cuanto sube
#    con la proteina ni cuanto con el numero de tomas. Sin esas dos cifras,
#    aplicarlo seria inventarselas.

# Ajustes ADITIVOS, en kcal/kg^0.75. Solo se aplican a adulto y senior.
# ⚠️ EL ESCALON DE EDAD ES EL DE FEDIAF, TABLA VII-6 (9 septiembre 2026).
#
# «Practical recommendations for MER in dogs at different ages»:
#
#     1-2 anos ................ 130 (125-140) kcal ME/kg BW^0,75
#     3-7 anos ................ 110  (95-130)
#     > 7 anos (senior) ....... 95   (80-120)
#
# O sea +20 el joven y -15 el senior sobre la banda de 3-7. Aqui ponia +15 y -7,
# que venian de Thes 2014 (100 kcal/kg^0,75 en jovenes contra 93 en mayores de 7).
#
# ⚠️ CASO REAL: esta tabla SE HABIA LEIDO. El comentario de arriba, del 6 de
# septiembre, dice «no la VII-6 (esa es solo por EDAD, sin actividad -- confirmado
# literal en fediaf_2025.txt)». Se abrio, se confirmo, se clasifico bien y se
# aparto -- y nadie cruzo su escalon de edad contra el que aplicabamos. El -7 era
# un -6,4 %, cuando FEDIAF dice -13,6 % y SACN5 cap.5 dice, aparte, «dogs over
# seven years of age required 10 to 20% less energy» y recomienda «foods providing
# a 15 to 20% caloric reduction». Las dos fuentes coincidian y nosotras ibamos por
# menos de la mitad. Lo unico que lo evita es LEER EL CAPITULO ENTERO y
# anotar lo que se aplica y lo que no, que es la regla desde el 11-sep-2026:
# ver `LECTURAS.md`.
#
# ⚠️ Y CRUZAR EDAD CON ACTIVIDAD ES LO QUE PIDE LA FUENTE, aunque la VII-6 y la
# VII-7 sean alternativas entre si. FEDIAF, justo encima de la VII-6: «some young
# adult dogs may have a sedentary lifestyle and need fewer calories than the
# average shown in table VII-6, whereas older dogs (> 7 years of age) which are
# still playing and running will need more energy than indicated». Lo que no era
# de la fuente era el TAMAÑO del escalon.
AJUSTE_EDAD = {
    "joven":   +20,   # 1 a 2 años  -- FEDIAF VII-6: 130 contra 110
    "adulto":    0,   # 2 a 7 años  -- la banda de referencia, 110
    "senior":   -15,  # > 7 años    -- FEDIAF VII-6: 95 contra 110
}
# La banda de 1-2 anos de la Tabla VII-6. Un perro es "adulto joven" mientras no
# cumpla los dos anos; por debajo del fin de su crecimiento ni siquiera llega aqui,
# porque manda la etapa de cachorro.
ADULTO_JOVEN_HASTA_MESES = 24.0

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

# ⚠️ AÑADIDO (8 septiembre) — LAS DOS RAZAS A LAS QUE FEDIAF LES DA CIFRA
# PROPIA, Y QUE EL MOTOR IGNORABA.
#
# La Tabla VII-7 de FEDIAF 2025, la misma de la que salen los cinco escalones
# de actividad, termina con una seccion "Breed specific differences":
#
#     Great Danes      200 (200 - 250) kcal ME per kg BW^0.75
#     Newfoundlands    105 (80 - 132)
#
# Las dos razas estan en la lista de 136 de la app y no se usaban. MEDIDO
# antes de arreglarlo: un Gran Danes de 67,5 kg marcado como "normal" recibia
# 2590 kcal/dia donde FEDIAF dice 4710. EL 55 %. Un perro asi adelgaza.
#
# Y 200 no es un valor extremo: SACN5 cap.5 dice que las estimaciones de DER
# en perro "range between 95 to 200 kcal ... per (BWkg)0.75 per day", o sea
# que es el extremo alto del rango publicado, no un caso raro.
#
# ⚠️ CÓMO SE APLICA: LA CIFRA DE RAZA VA EN VEZ DEL NIVEL DE ACTIVIDAD.
# No es un suelo sobre el que se aplique la actividad, ni un ajuste que se
# sume. Lo dice la propia guia dos veces (leido entero el 9 de septiembre, al
# cerrar PREGUNTAS_ABIERTAS.md P-11):
#
#   · La frase que presenta la tabla: "Table VII-7 provides examples of daily
#     energy requirements of dogs at different activity levels, FOR SPECIFIC
#     BREEDS and for obese prone adults". Tres clases de fila en paralelo, la
#     misma columna y el mismo coeficiente: la fila de raza es ALTERNATIVA a
#     la de actividad, igual que "obese prone adults <=90" es una alternativa
#     y no un descuento sobre el 95 del sedentario.
#   · Y la seccion 7.2.3.4 "Breed & type", que dice de que esta hecha esa
#     diferencia: "Breed-specific needs probably reflect differences in
#     temperament, RESULTING IN HIGHER OR LOWER ACTIVITY, as well as variation
#     in stature or insulation capacity of skin and hair coat". O sea que la
#     diferencia de raza YA CONTIENE la de actividad: sumar un nivel encima
#     seria contar dos veces lo mismo.
#
# ⚠️ LO UNICO QUE SIGUE SIENDO INTERPRETACION NUESTRA es donde caer DENTRO del
# rango publicado, porque FEDIAF da 200 (200-250) y 105 (80-132) y ninguna
# regla para colocarse. Lo que se hace:
#   · el valor central sustituye a la base de "normal";
#   · el nivel de actividad coloca dentro del rango moviendo lo mismo que
#     movia (su diferencia contra "normal");
#   · y el resultado se RECORTA al rango que publica la propia FEDIAF, para
#     no salirse de la fuente por interpretar de mas.
# Consecuencia: para el Gran Danes "en vez de" y "suelo" acaban coincidiendo,
# porque 200 es a la vez el centro y el extremo bajo de su rango, y ningun
# ajuste a la baja (sedentario, senior) puede pasar de ahi. Para el Terranova
# no coinciden, porque su rango abre a los dos lados: 90 sedentario, 132
# trabajo. Ese es el caso que separa las tres lecturas, y por eso lo fija el
# BLOQUE 54 apartado 2-bis.
RAZAS_CIFRA_FEDIAF = {
    # raza -> (central, minimo, maximo) en kcal/kg^0.75
    "Gran Danés": (200.0, 200.0, 250.0),
    "Terranova":  (105.0,  80.0, 132.0),
}

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
# ⚠️ CORREGIDO 6-sep-2026: esto NO es una tabla de FEDIAF -- se comprobó
# fediaf_2025.txt entero y la Tabla VII-8a/8b de crecimiento SOLO trae la
# curva continua de Klein (arriba), sin ningún escalón 210/175/140. Es la
# convención clínica genérica RER x3.0/2.5/2.0 (la que traía el motor
# ANTES de adoptar Klein, ver CLAUDE.md); se conserva solo como respaldo
# prudente si no hay peso adulto esperado, no como cifra de FEDIAF.
# ⚠️ REESCRITO (8 septiembre) — ERAN TRES ESCALONES Y SOLO SE USABA UNO.
#
# Aqui habia una tabla de tres filas por % del peso adulto (210 / 175 / 140),
# y `_coef_crecimiento` leia SIEMPRE la ultima -- las otras dos eran codigo
# muerto, en los dos repos. O sea que un cachorro de dos meses sin peso adulto
# esperado recibia 140 (= 2 x RER), que es lo que SACN5 da para DESPUES de los
# cuatro meses. Un 33 % menos de lo que le toca.
#
# FEDIAF no cubre este caso: su ecuacion de crecimiento (Tabla VII-8b, la de
# Klein) NECESITA el peso adulto esperado. Donde FEDIAF no llega se tira de
# SACN5, y SACN5 lo dice sin rodeos (Tabla 5-2, parte 2 canina):
#
#     "Daily energy intake for growing puppies should be 3 x RER from weaning
#      until four months of age. At four months of age energy intake should be
#      reduced to 2 x RER until the puppy reaches adult size."
#
# 3 x RER = 210 kcal/kg^0.75  ·  2 x RER = 140. Son DOS escalones y cortan por
# EDAD, no por % del peso adulto -- que era ademas el otro problema de la
# tabla vieja: para aplicar un corte por % del peso adulto hace falta el peso
# adulto, que es justo el dato que no hay cuando se llega aqui.
#
# Sin edad tampoco, se queda en 140, que es el lado prudente.
CRECIMIENTO_SACN5_MESES = 4.0
CRECIMIENTO_ANTES_4M = 210.0   # 3 x RER
CRECIMIENTO_DESDE_4M = 140.0   # 2 x RER

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
# ⚠️ QUITADO EL TOPE DE x6 RER (8 de septiembre). FEDIAF NO PONE NINGUNO.
#
# Aqui habia un `LACTANCIA_TOPE_RER = 6.0` que recortaba la formula, y el
# comentario que lo justificaba decia dos cosas, las dos falsas:
#
# 1. Que la formula de lactancia "viene de una fuente SECUNDARIA y no se ha
#    podido contrastar con el texto original de FEDIAF". SI SE PUEDE, y cuadra
#    letra por letra. FEDIAF 2025, Tabla VII-8b ("Average energy requirements
#    during growth and reproduction in dogs"):
#
#        1 to 4 puppies:  145 x kg BW^0.75 + 24 n x kg BW x L
#        5 to 8 puppies:  145 x kg BW^0.75 + [96 + 12 (n-4)] x kg BW x L
#        n = number of puppies; L = 0.75 sem 1; 0.95 sem 2; 1.1 sem 3; 1.2 sem 4
#
#    Que es exactamente lo que hace `calcular_der`, con los mismos 145, los
#    mismos 24n / 96+12(n-4) y los mismos cuatro factores L.
#
# 2. Que el x6 era "el maximo de la tabla clinica". Leida esa tabla (Small
#    Animal Clinical Nutrition 5a ed., Tabla 5-2, parte 2 canina), el x6 NO es
#    un techo general: es la FILA de camadas de 9 o mas cachorros. Se estaba
#    usando una fila de una tabla indexada por tamaño de camada como si fuera
#    un limite universal.
#
# ⚠️ Y RECORTABA DE VERDAD. Medido el 8 de septiembre, en semana 4:
#     25 kg, 6 cachorros:  FEDIAF 5221 kcal -> recortado a 4696  (-10 %)
#     40 kg, 8 cachorros:  FEDIAF 9218 kcal -> recortado a 6680  (-28 %)
#     60 kg, 8 cachorros:  FEDIAF 13494 kcal -> recortado a 9054 (-33 %)
#
# Una perra de 60 kg con 8 cachorros recibia un tercio menos de lo que dice
# FEDIAF, por un techo que no era de FEDIAF y cuya justificacion escrita era
# incorrecta. Se quita: manda FEDIAF.
#
# Lo que sigue siendo verdad del comentario viejo: la lactancia deberia
# pautarla un veterinario, y hay que recalcular cada semana. Eso es un aviso,
# no un recorte de kcal.

# =============================================================================
# PESO CORPORAL — manda sobre todo lo demás
# =============================================================================
RER_COEF = 70                     # RER = 70 x peso^0.75

# ESCALA DE CONDICION CORPORAL. La app usa 5 niveles; la escala validada
# (Laflamme 1997, contrastada con DEXA) es de 9 puntos.
#
# ⚠️ CORREGIDA (9 septiembre 2026) — LA CORRESPONDENCIA LA PUBLICA FEDIAF Y NO
# ERA LA NUESTRA. Aqui ponia {0:2, 1:4, 2:5, 3:7, 4:9}, que era criterio propio.
# Al leer entera la seccion 7.1 resulta que las Tablas VII-1 y VII-2 traen una
# COLUMNA 2 DE CINCO PUNTOS al lado de la de nueve, y su correspondencia es:
#
#     5 puntos    1     2     3     4     5
#     9 puntos    1     3     5     7     9
#
# En los tres escalones de arriba coincidiamos. En los dos de perro delgado
# eramos MENOS severas: el escalon 0 iba a BCS 2 (-30 %) donde FEDIAF pone BCS 1
# (->=40 %), y el 1 iba a BCS 4 (-10 %) donde pone BCS 3 (-20 %).
#
# MEDIDO, y se mueve menos de lo que parece porque el tope de subida del 20 %
# absorbe casi todo: el escalon 0 se topaba antes y se topa ahora (sin cambio), y
# el UNICO que se mueve es el 1, de x1,111 a x1,20 -- un 8 % mas de racion para
# un perro delgado, que es la direccion correcta.
#
# ⚠️ TIENE QUE SEGUIR SIENDO IDENTICO A `BCS_DESDE_CONDICION` de `src/bcs.js`.
BCS_DESDE_CONDICION = {0: 1, 1: 3, 2: 5, 3: 7, 4: 9}
# Regla practica aceptada: cada punto de BCS por encima de 5 equivale a un
# 10% de exceso de peso corporal (y por debajo, a un 10% de defecto).
#
# ⚠️ Y LA TABLA VII-2 DE FEDIAF LA CONFIRMA EN OCHO PUNTOS DE NUEVE (9 de
# septiembre de 2026). Su columna «% BW below or above BCS 5» da un RANGO por
# punto, y este 10 % lineal es exactamente el extremo bajo de cada uno -- el mas
# conservador -- de BCS 1 a BCS 8. El unico que no cuadra es el 9: FEDIAF dice
# «>45 %» y la recta da 40. Ver el comentario largo de `verificar.py`.
BCS_PCT_POR_PUNTO = 0.10
EXCESO_BCS_9 = 0.45          # FEDIAF 2025, Tabla VII-2, fila «9. Grossly Obese»
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
    # ⚠️ El 9 va aparte: FEDIAF dice «>45 %» y la recta se queda en 40. Tiene que
    # decir lo mismo que `verificar.peso_objetivo_desde_bcs`, que es la copia que
    # sí usa la API -- este modulo solo corre si alguien llama a `/der`. Dos
    # sitios que calculan lo mismo, y por eso el BLOQUE 63 los compara.
    if bcs >= 9:
        desvio = EXCESO_BCS_9
    else:
        desvio = (bcs - 5) * BCS_PCT_POR_PUNTO  # +0.2 si BCS 7, -0.3 si BCS 2
    ideal = peso_actual_kg / (1 + desvio)
    # TOPE DE SEGURIDAD hacia arriba. Un perro muy delgado (BCS 2) daria un
    # objetivo un 43% por encima de su peso actual, y pasar de golpe a esa
    # racion es mala idea: se recupera peso poco a poco, y ademas un perro
    # muy delgado suele estarlo por una ENFERMEDAD, no por comer poco.
    # Se limita la correccion al alza al 20% y se avisa.
    if ideal > peso_actual_kg * 1.20:
        ideal = peso_actual_kg * 1.20
    return round(ideal, 2)


def _coef_crecimiento(peso_actual: float, peso_adulto: float,
                      meses: float = None) -> float:
    """
    Devuelve el coeficiente en kcal/kg^0.75 para un cachorro.
    Con peso adulto conocido usa KLEIN 2019 (curva continua medida en 493
    cachorros de compania), que es la que publica FEDIAF en su Tabla VII-8b.
    Sin el, cae a la regla de SACN5 por edad -- ver el comentario de
    CRECIMIENTO_ANTES_4M.
    """
    if not peso_adulto or peso_adulto <= 0:
        if meses is not None and meses < CRECIMIENTO_SACN5_MESES:
            return CRECIMIENTO_ANTES_4M
        return CRECIMIENTO_DESDE_4M
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
    # ⚠️ LAS DOS RAZAS CON CIFRA PROPIA DE FEDIAF MANDAN SOBRE LA BASE.
    # Ver RAZAS_CIFRA_FEDIAF, arriba, para el porque y para que parte de esto
    # es interpretacion nuestra. El nivel de actividad sigue moviendo lo mismo
    # que movia: se aplica su diferencia contra "normal".
    propia = RAZAS_CIFRA_FEDIAF.get(raza)
    if propia:
        central, minimo, maximo = propia
        k = central + (BASE_ACTIVIDAD[actividad] - BASE_ACTIVIDAD["normal"])
    else:
        k = BASE_ACTIVIDAD[actividad]
    k += AJUSTE_EDAD.get(edad_grupo, 0)
    k += AJUSTE_CONVIVENCIA.get(convivencia, 0)
    if macho_entero:
        k += AJUSTE_MACHO_ENTERO
    if propia:
        # El +-15 de Thes 2014 NO se aplica encima: es un ajuste sobre la media
        # de 586 perros, y estas dos razas ya tienen su propia cifra medida.
        # Y se recorta al rango que publica FEDIAF, para no salirse de la
        # fuente por interpretar de mas.
        return max(minimo, min(maximo, k))
    if raza in RAZAS_MAS_GASTO:
        k += AJUSTE_RAZA
    elif raza in RAZAS_MENOS_GASTO:
        k -= AJUSTE_RAZA
    return k


# =============================================================================
# PESO ADULTO DEDUCIDO DE LA CURVA DE CRECIMIENTO
# =============================================================================
# La media de la raza NO sirve: un American Staffordshire adulto va de 18 a
# 34 kg segun la ficha FCI, y usar la media (26) puede errar 8 kg. Y el peso
# adulto es EL dato que mas mueve las kcal de un cachorro, porque la ecuacion
# de Klein va justo por la relacion peso actual / peso adulto.
#
# El propio perro da mejor informacion que la tabla: si con 5 meses ya pesa
# 18 kg, va camino de mas de 26.
#
# ⚠️ 11 SEP: MANDA FEDIAF, Y HASTA HOY NO SE USABA SU ECUACION.
# La Tabla VII-8a de FEDIAF publica esta misma curva como CINCO ECUACIONES,
# validas «from weaning age (8 weeks) to 1 year», y aqui habia una tabla cuyo
# propio comentario decia que venia de «reproducciones divulgativas» de las
# curvas WALTHAM y NO del texto del estudio. Una fuente publicada gana a una
# reproduccion divulgativa, que es la regla de siempre.
#
# ⚠️ CASO REAL ENCONTRADO, y va en la direccion mala: MEDIDO entre los 2 y los
# 12 meses, en perros pequenos la diferencia iba de -1,5 a +3,2 puntos, pero en
# los grandes la tabla vieja iba SISTEMATICAMENTE POR DEBAJO -- un cachorro de
# mas de 47,5 kg de adulto, a los 6 meses, para FEDIAF va por el 57,0 % de su
# peso adulto y la tabla vieja decia 45,0 %. Menos porcentaje supone un peso
# adulto estimado MAYOR, que en la ecuacion de Klein sube el coeficiente: para
# un cachorro de 30 kg a los 6 meses son 2479 kcal con la tabla vieja contra
# 2271 con la de FEDIAF, un 9 % DE MAS, justo en la poblacion en la que la
# propia FEDIAF avisa de que sobrealimentar «can result in skeletal deformities
# especially in large and giant breeds».
#
# ⚠️ Y ESTA TABLA HAY QUE LEERLA DEL PDF, NO DEL TEXTO EXTRAIDO. Las cinco
# bandas y las cinco ecuaciones salen en dos columnas cruzadas y el orden NO es
# el que parece: la banda >15-27,5 lleva -60,70 y la >27,5-47,5 lleva -56,18, o
# sea que el termino independiente NO es monotono y emparejarlas «de menor a
# mayor» las cruza. Las cinco parejas de abajo estan leidas del PDF por
# coordenadas (pagina 56, y=345 a y=405).
#
# FEDIAF 2025, Tabla VII-8a:
#     % del peso adulto esperado = a x Ln(edad en semanas) - b
CURVA_FEDIAF_VII_8A = (
    #  peso adulto esperado hasta (kg),    a,       b
    (7.0,                                36.92,   43.57),
    (15.0,                               36.86,   48.22),
    (27.5,                               39.88,   60.70),
    (47.5,                               36.96,   56.18),
    (float("inf"),                       36.61,   62.39),
)

# La ecuacion de FEDIAF vale de las 8 semanas al ano, y ella misma lo dice. Por
# encima del ano sigue subiendo y pasa del 100 %, asi que ahi NO se usa: se
# vuelve a la tabla de abajo, que es la unica que tiene el tramo de los 12 a los
# 24 meses (el del gigante, que a los 12 meses todavia no ha terminado).
CURVA_FEDIAF_MESES_MIN = 2.0     # 8 semanas = 1,84 meses; se redondea al primer
CURVA_FEDIAF_MESES_MAX = 12.0    # escalon que la tabla de respaldo ya tenia

SEMANAS_POR_MES = 365.25 / 12.0 / 7.0    # 4,348


def _pct_peso_adulto_fediaf(meses, peso_adulto_estimado):
    """
    % del peso adulto que le toca a esa edad, por la Tabla VII-8a de FEDIAF.

    Devuelve None fuera del rango de validez que la propia FEDIAF declara
    (8 semanas a 1 ano), para que el llamador use el respaldo.
    """
    if meses is None or meses < CURVA_FEDIAF_MESES_MIN or meses > CURVA_FEDIAF_MESES_MAX:
        return None
    for tope, a, b in CURVA_FEDIAF_VII_8A:
        if peso_adulto_estimado <= tope:
            break
    semanas = meses * SEMANAS_POR_MES
    pct = (a * math.log(semanas) - b) / 100.0
    # La ecuacion es un ajuste: a los 12 meses el perro pequeno ya la pasa de
    # 100 %. Nunca puede decir que pesa mas de lo que va a pesar de adulto.
    return min(max(pct, 0.01), 1.0)


# RESPALDO, y solo para lo que FEDIAF no cubre: por debajo de los 2 meses y por
# encima de los 12. Derivado de las curvas de crecimiento tipo WALTHAM (Salt,
# German et al. 2017, PLOS ONE, >6 millones de perros).
# ⚠️ Los porcentajes concretos vienen de reproducciones divulgativas de esas
# curvas, NO del texto del estudio: usar como estimacion, no como dato duro.
CURVA_CRECIMIENTO = {
    # meses: (toy <5kg, pequeno 5-10, mediano 10-25, grande 25-45, gigante >45)
     2: (0.35, 0.30, 0.25, 0.20, 0.15),
     3: (0.50, 0.45, 0.40, 0.32, 0.25),
     4: (0.65, 0.58, 0.52, 0.44, 0.35),
     5: (0.75, 0.68, 0.60, 0.50, 0.40),
     6: (0.80, 0.75, 0.65, 0.55, 0.45),
     7: (0.85, 0.80, 0.72, 0.62, 0.52),
     8: (0.90, 0.85, 0.78, 0.68, 0.58),
     9: (0.94, 0.90, 0.84, 0.74, 0.64),
    10: (0.97, 0.93, 0.88, 0.80, 0.70),
    11: (0.99, 0.96, 0.92, 0.85, 0.75),
    12: (1.00, 0.98, 0.95, 0.89, 0.80),
    15: (1.00, 1.00, 0.99, 0.95, 0.88),
    18: (1.00, 1.00, 1.00, 0.99, 0.94),
    24: (1.00, 1.00, 1.00, 1.00, 1.00),
}


def _columna_tamano(peso_adulto_estimado):
    if peso_adulto_estimado < 5:   return 0
    if peso_adulto_estimado < 10:  return 1
    if peso_adulto_estimado < 25:  return 2
    if peso_adulto_estimado < 45:  return 3
    return 4


def peso_adulto_desde_curva(peso_actual_kg, meses, peso_medio_raza=None,
                            peso_min_raza=None, peso_max_raza=None):
    """
    Estima el peso adulto a partir de lo que el perro pesa AHORA y su edad.

    Se itera porque la columna de la tabla depende del peso adulto, que es
    justo lo que se busca: se parte de la media de la raza (o del propio peso
    actual) y se converge en 2-3 vueltas.

    El resultado se limita al rango de la raza si se conoce: la curva es una
    estimacion y no debe sacar a un perro de lo que su raza puede pesar.
    """
    if not peso_actual_kg or peso_actual_kg <= 0 or not meses:
        return peso_medio_raza
    if meses >= 24:
        return peso_actual_kg          # ya es adulto

    edades = sorted(CURVA_CRECIMIENTO)
    estimado = peso_medio_raza or peso_actual_kg * 2

    for _ in range(4):
        # FEDIAF primero, en el tramo en que FEDIAF dice que vale
        pct = _pct_peso_adulto_fediaf(meses, estimado)
        if pct is None:
            col = _columna_tamano(estimado)
            # interpolar entre las dos edades mas cercanas
            antes = max([e for e in edades if e <= meses], default=edades[0])
            despues = min([e for e in edades if e >= meses], default=edades[-1])
            p1 = CURVA_CRECIMIENTO[antes][col]
            p2 = CURVA_CRECIMIENTO[despues][col]
            if despues == antes:
                pct = p1
            else:
                pct = p1 + (p2 - p1) * (meses - antes) / (despues - antes)
        if pct <= 0:
            return estimado
        nuevo = peso_actual_kg / pct
        if abs(nuevo - estimado) < 0.2:
            estimado = nuevo
            break
        estimado = nuevo

    # no salirse de lo que la raza puede pesar
    if peso_min_raza:  estimado = max(estimado, peso_min_raza)
    if peso_max_raza:  estimado = min(estimado, peso_max_raza)
    return round(estimado, 1)


def calcular_der(peso_actual_kg: float, etapa: str, actividad: str = None,
                 esterilizado: bool = False, peso_adulto_esperado_kg: float = None,
                 peso_ideal_kg: float = None, convivencia: str = "solo",
                 macho_entero: bool = False, raza: str = None,
                 semana_gestacion: int = None, n_cachorros: int = None,
                 semana_lactancia: int = 3,
                 meses: float = None, peso_min_raza: float = None,
                 peso_max_raza: float = None) -> dict:
    """
    etapa: "cachorro_joven" | "cachorro_crecimiento" | "gestante_temprana"
           | "gestante_tardia" | "lactante" | "adulto" | "senior"

    Los parámetros nuevos son TODOS opcionales: sin ellos el cálculo sigue
    funcionando con valores prudentes, así que nada que ya llamaba a esta
    función se rompe.
    """
    if not peso_actual_kg or peso_actual_kg <= 0:
        raise ValueError("El peso tiene que ser mayor que cero")

    # EL PESO ADULTO SE DEDUCE DE SU PROPIA CURVA, no de la media de la raza.
    # La media no sirve: un American Staffordshire adulto va de 18 a 34 kg y
    # la media (26) puede errar 8. Y el peso adulto es EL dato que mas mueve
    # las kcal de un cachorro, porque la ecuacion de Klein va justo por la
    # relacion peso actual / peso adulto.
    # El propio perro informa mejor que la tabla: Cairo con 5 meses y 18 kg
    # apunta a 34 kg, no a 26, y eso son 192 kcal/dia de diferencia.
    # Si no se pasa la edad, se usa el peso de la raza como antes.
    peso_adulto_curva = None
    if meses and peso_actual_kg:
        peso_adulto_curva = peso_adulto_desde_curva(
            peso_actual_kg, meses,
            peso_medio_raza=peso_adulto_esperado_kg,
            peso_min_raza=peso_min_raza, peso_max_raza=peso_max_raza)
        if peso_adulto_curva:
            peso_adulto_esperado_kg = peso_adulto_curva

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
        coef = _coef_crecimiento(peso_actual_kg, peso_adulto_esperado_kg, meses)
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
        # ⚠️ SIN TOPE. Ver el comentario largo de arriba: el x6 que habia aqui
        # no era de FEDIAF y recortaba hasta un 33 %.
        der = coef * peso_calculo ** 0.75 + extra * LACTANCIA_PESO_SEMANA[sem - 1]
    elif etapa in ("adulto", "senior"):
        # ⚠️ EL GRUPO «joven» EXISTIA Y NO SE USABA NUNCA (9 septiembre 2026).
        # `AJUSTE_EDAD` tenia una entrada "joven" desde que se escribio esto, y
        # aqui solo se pasaba "senior" o "adulto": codigo muerto que PARECIA
        # aplicado. Es el mismo fallo que los tres escalones de crecimiento, de
        # los que dos no se leian nunca.
        # FEDIAF VII-6 da 130 kcal/kg^0,75 al perro de 1-2 anos contra 110 al de
        # 3-7: un 18 % mas, y la app sabe la fecha de nacimiento. Ahora se aplica.
        if etapa == "senior":
            grupo = "senior"
        elif meses is not None and meses < ADULTO_JOVEN_HASTA_MESES:
            grupo = "joven"
        else:
            grupo = "adulto"
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
        "peso_adulto_usado": peso_adulto_esperado_kg,
        "peso_adulto_de_la_curva": peso_adulto_curva,
    }
    if aviso_peso:
        resultado["aviso"] = aviso_peso
    if etapa == "lactante":
        resultado["requiere_veterinario"] = True
        resultado["aviso_lactancia"] = (
            "La lactancia es la etapa de mayor demanda de toda la vida de una "
            "perra y la que peor se estima con una fórmula. Este número es "
            "solo un punto de partida: pésala cada semana, ajusta según su "
            "condición corporal, y que lo supervise tu veterinario.")
    return resultado


if __name__ == "__main__":
    print("=== CAIRO: 17 kg ahora, 32 kg de adulto, en crecimiento ===")
    print(calcular_der(17, "cachorro_crecimiento", peso_adulto_esperado_kg=32))
    print("\n=== Cairo de adulto, 32 kg, normal, Amstaff ===")
    print(calcular_der(32, "adulto", "normal", raza="American Staffordshire Terrier"))
    print("\n=== Lactante 25 kg con 6 cachorros, semana 3 ===")
    print(calcular_der(25, "lactante", n_cachorros=6, semana_lactancia=3))
