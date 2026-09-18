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
    # ⚠️ Las 54 fichas COCIDAS del 18 de septiembre de 2026, construidas desde las
    # fuentes por `construir_cocidos.py`. Van en la MISMA lista que las crudas: quien
    # decide en qué modo vale cada una es `modos_de`, no esta lista. Y tienen que
    # estar aquí o el motor NO LAS VE — una ficha que no está en su lista no es
    # candidata, el menú sale igual y no lo dice nadie. Ya pasó con las once primeras.
    "Conejo cocido",
    "Corazón de cordero cocido",
    "Corazón de pavo cocido",
    "Corazón de pollo cocido",
    "Corazón de vaca cocido",
    "Gallina (carne sin hueso) cocida",
    "Jarrete de ternera cocido",
    "Lengua de buey cocida",
    "Lengua de cordero cocida",
    "Lengua de ternera cocida",
    "Molleja de pavo cocida",
    "Molleja de pollo cocida",
    "Pato (carne sin hueso) cocido",
    "Pavo muslo con piel cocido",
    "Pavo pechuga con piel cocido",
    "Pavo pechuga sin piel cocido",
    "Pollo ala con piel (sin hueso) cocido",
    "Pollo muslo con piel cocido",
    "Pollo muslo sin piel cocido",
    "Pollo pechuga con piel cocido",
    "Pollo pechuga sin piel cocido",
    "Vaca para guisar cocida",
    # ⚠️ LAS COCINADAS VAN EN LA MISMA LISTA QUE LAS CRUDAS (17 de septiembre de
    # 2026), y quien decide en qué modo vale cada una es `modos_de`, no la
    # pertenencia a esta lista. Meterlas en una lista aparte habría sido una
    # segunda copia del mismo conjunto, que es el fallo que este fichero lleva
    # avisado desde el 5 de agosto.
    #
    # ⚠️ Y AQUÍ SE CAYÓ AL ESTRENAR EL MODO: las once fichas cocinadas entraron
    # al catálogo y NO a esta lista, así que en modo cocinado el solver solo
    # veía verdura y suplementos -- «infactible» en los cuatro perros de prueba,
    # y la causa no era nutrición ni proporciones: era que la comida no estaba
    # ofrecida. Es literalmente lo que avisa la cabecera de este fichero.
    # ⚠️ «Pollo muslo cocido» ESTUVO AQUÍ Y YA NO EXISTE, y va dicho porque el
    # BLOQUE 12 tuvo que cazarlo (18 de septiembre de 2026). Al construir las
    # fichas cocidas nuevas lo sustituyeron DOS más precisas —«Pollo muslo con
    # piel cocido» y «Pollo muslo sin piel cocido», que es como está el
    # catálogo en crudo— y el nombre viejo se quedó en esta lista: el motor lo
    # filtraba en silencio, sin error y con el menú saliendo igual. Un nombre
    # que no existe en una lista curada no da error: deja de haber un alimento.
    "Jarrete de ternera cocido", "Vaca para guisar cocida",
    "Corazón de vaca cocido", "Corazón de pavo cocido",
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
    # ⚠️ SEGUNDA VUELTA, 18 de septiembre de 2026, y las seis vienen de dos frases
    # de Elena: «tienes que meter más pescado» y «veo que no hay nada de cerdo ni
    # de ternera en carne muscular». Cada una entró con su fila CRUDA de la misma
    # fuente como ancla y medida en materia seca; lo que no anclaba se rechazó y
    # está escrito en `cocidos_propuesta.json` (sardina, boquerón, lubina).
    "Cerdo cocido", "Ternera cocida", "Solomillo de vaca cocido",
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
    # ⚠️ Las 54 fichas COCIDAS del 18 de septiembre de 2026, construidas desde las
    # fuentes por `construir_cocidos.py`. Van en la MISMA lista que las crudas: quien
    # decide en qué modo vale cada una es `modos_de`, no esta lista. Y tienen que
    # estar aquí o el motor NO LAS VE — una ficha que no está en su lista no es
    # candidata, el menú sale igual y no lo dice nadie. Ya pasó con las once primeras.
    "Bacalao cocido",
    "Caballa cocida",
    "Calamar cocido",
    "Lenguado cocido",
    "Merluza cocida",
    "Perca cocida",
    "Salmón cocido",
    "Trucha cocida",
    "Bacalao cocido", "Salmón cocido", "Trucha cocida",
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
    # ⚠️ SEGUNDA VUELTA, 18 de septiembre de 2026, y las seis vienen de dos frases
    # de Elena: «tienes que meter más pescado» y «veo que no hay nada de cerdo ni
    # de ternera en carne muscular». Cada una entró con su fila CRUDA de la misma
    # fuente como ancla y medida en materia seca; lo que no anclaba se rechazó y
    # está escrito en `cocidos_propuesta.json` (sardina, boquerón, lubina).
    "Atún claro cocido", "Pulpo cocido", "Dorada cocida",
]

VISCERAS = [
    # ⚠️ Las 54 fichas COCIDAS del 18 de septiembre de 2026, construidas desde las
    # fuentes por `construir_cocidos.py`. Van en la MISMA lista que las crudas: quien
    # decide en qué modo vale cada una es `modos_de`, no esta lista. Y tienen que
    # estar aquí o el motor NO LAS VE — una ficha que no está en su lista no es
    # candidata, el menú sale igual y no lo dice nadie. Ya pasó con las once primeras.
    "Bazo de cordero cocido",
    "Bazo de vaca cocido",
    "Cerebro de ternera cocido",
    "Pulmón de cordero cocido",
    "Pulmón de ternera cocido",
    "Pulmón de vaca cocido",
    "Riñón de cordero cocido",
    "Timo de ternera cocido",
    "Timo de vaca cocido",
    "Riñón de vaca cocido",
    "Riñón de vaca", "Riñón de cordero",
    # ⚠️ CORREGIDO (5 agosto, madrugada) — el pulmón vuelve aquí: a
    # diferencia de lengua/molleja/corazón (donde todas las fuentes
    # coinciden sin excepción), el pulmón es un caso genuinamente
    # debatido en la comunidad de alimentación cruda -- se deja por
    # prudencia, sin consenso claro para moverlo a Carne muscular.
    # ⚠️ PARTIDO EN DOS EL 8 DE SEPTIEMBRE. Había una sola ficha llamada
    # "Pulmón de ternera" cuyos datos NO eran de ternera: coinciden celda a
    # celda con el pulmón de VACA de USDA (FDC 168628) y no con el de
    # ternera (174361). En vez de elegir una especie y perder la otra, se
    # parten: cada una con SUS datos. Y no es un decimal -- el selenio va de
    # 44,3 a 17,2 y el sodio de 198 a 108.
    "Pulmón de vaca", "Pulmón de ternera", "Pulmón de cordero",
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
    # Mismo caso que el pulmón, y aquí la diferencia es enorme: el timo de
    # VACA (FDC 170194, el que llevaba el nombre equivocado) tiene 236 kcal y
    # 20,35 g de grasa, y el de TERNERA (FDC 172542) 101 kcal y 3,07 g. Siete
    # veces menos grasa. Quien compra mollejas en la carnicería compra uno de
    # los dos, así que estaban los dos o el menú mentía.
    "Timo de vaca", "Timo de ternera",
    # ⚠️ Y EL 13 DE SEPTIEMBRE «Cerebro de vaca» SALIÓ DEL CATÁLOGO ENTERO, que
    # es más fuerte que estar fuera del automático, y por un motivo LEGAL y no
    # nutricional: el encéfalo bovino de un animal de más de 12 meses es material
    # especificado de riesgo (Reg. 999/2001, anexo V consolidado), o sea material
    # de categoría 1 (Reg. 1069/2009, art. 8), y la comida para mascotas sale de
    # categoría 3 (art. 35). Una vaca pasa de 12 meses por definición.
    # «Cerebro de ternera» SE QUEDA, porque la ternera española se sacrifica por
    # debajo del año, con la condición escrita en su propia ficha. Lo vigila el
    # BLOQUE 51. Ver `DATOS_QUE_FALTAN.md`.
    # Lo que sigue es la historia de por qué ninguna de las dos entraba YA en el
    # automático, que es una cuestión distinta y sigue valiendo para la de ternera.
    # ⚠️ QUITADO "Cerebro de vaca" (7 septiembre), mismo criterio que la
    # laringe de vacuno: se queda en el catálogo para quien lo elija A MANO,
    # pero el automático ya no lo propone. Y esta vez el motivo se midió.
    #
    # Hasta hoy su ficha tenía el DHA a CERO -- un cero mudo, ni siquiera
    # declarado -- mientras su propia `nota_datos` decía, escrito, "rico en
    # DHA de forma natural". Al ponerle el valor real de BEDCA 1047 (0,36 g
    # /100 g) pasó a ser LA ÚNICA VÍSCERA DEL CATÁLOGO CON DHA, así que
    # cubría dos casillas con un solo alimento -- la de víscera y la de
    # omega-3 -- y ganaba siempre. MEDIDO con 20 menús automáticos idénticos
    # antes y después: el cerebro pasó de 0/20 a 15/20, y a cambio
    # desaparecieron el timo (6/20 -> 0), el riñón de ternera (5/20 -> 0),
    # el pulmón de ternera (4/20 -> 0) y el riñón de cordero (2/20 -> 0).
    # De paso dejaba al pescado fuera: de 30 semillas, solo 2 conservaban el
    # boquerón que el usuario había pedido conservar (lo cazó el BLOQUE 17).
    #
    # El dato es CORRECTO y se queda: el problema no es nutricional, es que
    # los sesos no se piden en una carnicería normal y no pueden ser la
    # víscera por defecto de tres de cada cuatro menús. Igual que la
    # laringe: el criterio de esta lista es "fácil y seguro de encontrar",
    # no solo "con buenos datos".
    #
    # ⚠️ Y VALE PARA LAS DOS (8 septiembre). El 8 se partió la ficha en
    # "Cerebro de vaca" (sus datos, FDC 168622) y "Cerebro de ternera" (los
    # de ternera de verdad, BEDCA 1047 + USDA 174351), porque la que había
    # llevaba nombre de una y datos de la otra. NINGUNA de las dos entra en
    # el automático: la de ternera tiene menos DHA (0,36 frente a 0,851)
    # pero sigue siendo la única víscera que lo trae, así que ganaría igual.
    # Las dos siguen en el catálogo para quien las elija a mano.
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
HIGADO = [
    # ⚠️ Las 54 fichas COCIDAS del 18 de septiembre de 2026, construidas desde las
    # fuentes por `construir_cocidos.py`. Van en la MISMA lista que las crudas: quien
    # decide en qué modo vale cada una es `modos_de`, no esta lista. Y tienen que
    # estar aquí o el motor NO LAS VE — una ficha que no está en su lista no es
    # candidata, el menú sale igual y no lo dice nadie. Ya pasó con las once primeras.
    "Hígado de cordero cocido",
    "Hígado de pavo cocido",
    "Hígado de pollo cocido",
    "Hígado de vaca cocido",
    "Hígado de vaca cocido", "Hígado de pollo cocido","Hígado de vaca", "Hígado de pollo", "Hígado de pavo", "Hígado de pato",
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
    # ⚠️ Las 54 fichas COCIDAS del 18 de septiembre de 2026, construidas desde las
    # fuentes por `construir_cocidos.py`. Van en la MISMA lista que las crudas: quien
    # decide en qué modo vale cada una es `modos_de`, no esta lista. Y tienen que
    # estar aquí o el motor NO LAS VE — una ficha que no está en su lista no es
    # candidata, el menú sale igual y no lo dice nadie. Ya pasó con las once primeras.
    "Acelga cocida",
    "Berenjena",
    "Boniato",
    "Brócoli cocido",
    "Calabacín cocido",
    "Calabaza cocida",
    "Cardo cocido",
    "Champiñón cocido",
    "Col lombarda cocida",
    "Coles de Bruselas cocida",
    "Coliflor cocida",
    "Espinaca cocida",
    "Espárrago verde",
    "Judía verde cocida",
    "Pimiento rojo cocido",
    "Repollo cocido",
    "Zanahoria cocida",
    "Zanahoria", "Calabaza", "Calabacín", "Judía verde", "Brócoli", "Acelga",
    "Espinaca", "Coliflor", "Coles de Bruselas", "Col rizada", "Col lombarda",
    "Repollo", "Pimiento rojo", "Pepino", "Lechuga", "Canónigos",
    "Rucula", "Apio", "Espárrago verde", "Alcachofa", "Berenjena", "Champiñón",
    "Nabo pelado", "Rábano", "Boniato", "Albahaca",
    "Manzana", "Pera", "Plátano", "Fresa", "Sandía", "Melón",
    "Naranja", "Mandarina", "Piña", "Mango", "Frambuesa", "Arándano",
    "Albaricoque",
]

# ⚠️ LOS HIDRATOS, Y POR QUE ES UNA CATEGORIA APARTE Y NO VERDURA (17 de
# septiembre de 2026). Elena: «tenemos que meter los hidratos de carbono en el
# catalogo». Meterlos en «Verduras y frutas» habria sido no meterlos: esa
# categoria tiene el techo en el 10 % del plato desde el 5 de agosto —lo bajo
# la propia Elena al ver 384 g de canonigos— y a una pancreatitis le hacen
# falta 362 de cada 1000 kcal en hidratos por pura aritmetica, con la grasa
# topada en 37,5 g y la proteina en 75.
#
# Los cinco se DAN COCIDOS y se PESAN COCIDOS, que no es lo mismo que el
# Boniato, la Berenjena y el Esparrago verde —esos se dan cocidos y se pesan
# CRUDOS, porque su composicion sale de la fila cruda—. Lo dice cada ficha en
# `se_pesa` y lo vigila el BLOQUE 123.
CEREALES = [
    "Arroz blanco cocido", "Arroz integral cocido", "Patata cocida",
    "Copos de avena cocidos", "Quinoa cocida",
]

ACCESIBLES = {
    "Carne muscular": CARNE,
    "Hueso carnoso": HUESO,
    "Pescados y mariscos": PESCADO,
    "Vísceras": VISCERAS,
    "Hígado": HIGADO,
    "Verduras y frutas": VERDURA,
    "Cereales y tubérculos": CEREALES,
}


# ─── CRUDO O COCINADO ────────────────────────────────────────────────────────
#
# ⚠️ POR QUÉ EXISTE (17 de septiembre de 2026). Elena: «serían dos cosas
# distintas, el usuario tiene que poder elegir, o el veterinario, si quiere
# hacer menú barf o cocinado, y en función [de eso] que le proponga los
# ingredientes correctos para cada caso».
#
# Y `motor/seguridad.py` llevaba escrito desde agosto que el motor «no tiene
# concepto de crudo vs cocinado», con la consecuencia puesta: la gamba y el
# langostino cargan con el tope de la tiaminasa POR SI ACASO, porque no había
# forma de saber si se cocinan de verdad.
#
# ⚠️ QUÉ SIGNIFICA «COCINADO» AQUÍ, Y ES UNA DEFINICIÓN, NO UN DETALLE: que la
# parte ANIMAL va cocida — hervida o al vapor, sin grasa añadida y sin sal. Es
# donde vive toda la diferencia de seguridad (bacterias, parásitos, tiaminasa,
# avidina y el hueso), y es el único grado que Elena eligió: «solo hervido».
# La verdura sigue pudiendo ir cruda y triturada en los dos modos, que es lo
# que hace cualquier dieta casera cocinada. ⚠️ ESO ÚLTIMO ESTÁ SIN CONFIRMAR
# con ella: va escrito aquí y en PREGUNTAS_ABIERTAS.md en vez de decidido en
# silencio.
#
# ⚠️ LA ASIMETRÍA QUE HACE QUE EL HUESO SEA OTRA COSA. Equivocarse en «creo que
# es cocinado y era crudo» quita unos topes y el perro come pescado con
# tiaminasa: malo, y a largo plazo. Equivocarse al revés mete HUESO CARNOSO en
# un menú que se va a cocinar, y el hueso cocido ASTILLA: daño físico
# inmediato. SACN5 cap.50 lo tiene contado -- 46 de 60 cuerpos extraños
# esofágicos retirados a perros eran hueso. Por eso el hueso no es «se evita»
# en cocinado: NO EXISTE, como una alergia (regla 4), y no como una proporción
# que cede (regla 3).
MODO_CRUDO = "crudo"
MODO_COCINADO = "cocinado"
MODOS = (MODO_CRUDO, MODO_COCINADO)

# Las categorías donde la preparación cambia el ALIMENTO y su seguridad.
# Fuera de estas, una ficha vale en los dos modos: un aceite, una cáscara de
# huevo, un bote de vitaminas o una verdura no cambian porque el plato lleve
# la carne cocida.
CATEGORIAS_ANIMALES = ("Carne muscular", "Pescados y mariscos", "Vísceras", "Hígado")


_CRUDAS_DEL_CATALOGO = None


def _tiene_hermana_cruda(ficha):
    """¿Existe en el catálogo la versión CRUDA de esta ficha cocida?

    Se mira por el nombre —«Espinaca cocida» -> «Espinaca»— porque es como se
    construyen: `construir_cocidos.py` le pega el participio al nombre de su
    ficha cruda. Si algún día se nombran de otra forma, esto deja de encontrar
    la hermana y la ficha vuelve a valer en los dos modos, que es el lado del
    que no se pierde comida.
    """
    _cargar_gemelas()
    nombre = str((ficha or {}).get("nombre") or "")
    return " " in nombre and nombre.rsplit(" ", 1)[0] in _CRUDAS_DEL_CATALOGO


_COCIDAS_DE_UNA_CRUDA = None


def _cargar_gemelas():
    """Las dos caras del mismo índice: qué crudas hay, y de cuáles hay cocida."""
    global _CRUDAS_DEL_CATALOGO, _COCIDAS_DE_UNA_CRUDA
    if _CRUDAS_DEL_CATALOGO is not None:
        return
    import json as _json
    import os as _os
    ruta = _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))),
                         "alimentos_v3_final.json")
    try:
        with open(ruta, encoding="utf-8") as fh:
            fichas = _json.load(fh)
    except Exception:
        _CRUDAS_DEL_CATALOGO, _COCIDAS_DE_UNA_CRUDA = set(), set()
        return
    _CRUDAS_DEL_CATALOGO = {f["nombre"] for f in fichas
                            if not str(f.get("preparacion") or "").strip()}
    _COCIDAS_DE_UNA_CRUDA = set()
    for f in fichas:
        if not str(f.get("preparacion") or "").strip():
            continue
        n = str(f.get("nombre") or "")
        if " " in n and n.rsplit(" ", 1)[0] in _CRUDAS_DEL_CATALOGO:
            _COCIDAS_DE_UNA_CRUDA.add(n.rsplit(" ", 1)[0])


def _tiene_hermana_cocida(ficha):
    """¿Existe en el catálogo la versión COCIDA de esta ficha cruda?

    ⚠️ ES LA MITAD QUE FALTABA, y la vio Elena mirando lo que le había contado
    yo (18 de septiembre de 2026): «menú cocinado sin nada crudo animal, has
    dicho. No del todo. O sea, menú cocinado sin nada crudo animal y sin nada
    crudo vegetal, ¿no?».

    Tenía razón. La regla de las categorías animales las hace excluyentes por su
    `preparacion`, y con lo vegetal no pasaba nada: la ZANAHORIA cruda valía en
    los dos modos, así que el automático de un menú cocinado podía poner
    zanahoria cruda teniendo «Zanahoria cocida» al lado. Y eso no es solo feo:
    son dos composiciones distintas del mismo alimento en el mismo plato, y
    quien lo lee no sabe cuál de las dos cosas tiene que hacer.

    La regla que lo cierra es UNA y vale para los dos lados: **si un alimento
    existe en las dos formas, cada ficha va a su modo**. Lo que existe en una
    sola —la lechuga, el pepino, la fruta, el boniato, el arroz— sigue valiendo
    en los dos, que es lo correcto: nadie cuece una lechuga, y el boniato no se
    da crudo ni en BARF.
    """
    _cargar_gemelas()
    return str((ficha or {}).get("nombre") or "") in (_COCIDAS_DE_UNA_CRUDA or set())


def peligro_de_preparacion(ficha, modo):
    """¿Esta ficha en este modo es un PELIGRO, y no solo una incoherencia?

    ⚠️ LA DISTINCIÓN ES LA REGLA 5 (18 de septiembre de 2026), y la pidió Elena
    con dos casos de verdad: «a lo mejor alguien le da BARF a su perro pero le
    apetece meterle huevo porque le encantan las propiedades del huevo, aunque
    vaya cocido» y «a lo mejor alguien que hace comida cocinada le quiere meter
    fruta o verdura sin cocinar, muy triturada».

    Las dos tienen que poder hacerse. Lo que el usuario elige A MANO se respeta
    —eso es la regla 5— y el modo es una restricción del AUTOMÁTICO: decide qué
    propone el motor cuando elige él, no qué se le permite pedir a una persona.
    Es exactamente el mismo criterio con el que los hidratos entran a mano en un
    menú BARF aunque el automático no los proponga.

    Y hay UNA excepción, una sola: el **hueso carnoso en modo cocinado**. Eso no
    es incoherencia, es un peligro — el hueso cocido ASTILLA y puede clavarse o
    hacer un tapón (SACN5 5ª ed., cap. 50: 46 de 60 cuerpos extraños esofágicos
    retirados a perros eran hueso). Un peligro no cede ante una elección, igual
    que no cede una alergia.

    Dar carne cruda dentro de un menú cocinado NO entra aquí: eso es exactamente
    lo que hace una ración BARF, y quien lo pide sabe lo que pide.
    """
    if not modo:
        return False
    return ((ficha or {}).get("categoria") == "Hueso carnoso"
            and modo == MODO_COCINADO)


def modos_de(ficha):
    """En qué modos vale esta ficha. Se DERIVA, no se escribe ficha a ficha.

    Una lista escrita a mano se queda parada el día que entre una ficha nueva,
    y no daría ningún error -- el alimento simplemente no saldría, o saldría
    donde no debe. La derivación son tres reglas:

      · «Hueso carnoso» -> SOLO crudo, siempre. El hueso cocido astilla.
      · categoría animal -> el modo que diga su `preparacion`.
      · vegetal COCIDO que tiene hermana cruda -> solo cocinado (ver abajo).
      · vegetal CRUDO que tiene hermana cocida -> solo crudo (la mitad
        simétrica, del mismo día: si existe en las dos formas, cada ficha va a
        su modo).
      · todo lo demás    -> los dos.

    ⚠️ LA TERCERA SE VIO MIRANDO UN PLATO (18 de septiembre de 2026): en un menú
    CRUDO entraba «Espinaca cocida». Y no todas las fichas cocidas son iguales:

      · Las que se dan SIEMPRE cocidas —el boniato, la berenjena, el espárrago
        verde, la clara de huevo, el arroz— no tienen versión cruda en el
        catálogo porque cruda no se da. Ésas valen en los DOS modos, y en BARF
        llevan meses.
      · Las que son la ALTERNATIVA cocida de una ficha cruda que existe —la
        espinaca cocida frente a la espinaca— son del modo cocinado: en un menú
        crudo ya tienes la cruda, y ofrecer las dos es el mismo alimento dos
        veces con dos composiciones distintas.

    La diferencia se DERIVA —¿tiene hermana cruda en el catálogo?— y no se
    escribe: una lista a mano se quedaría parada la próxima vez que entre una
    ficha cocida, que es lo que este fichero lleva avisado desde agosto.
    """
    cat = (ficha or {}).get("categoria")
    if cat == "Hueso carnoso":
        return (MODO_CRUDO,)
    prep = str((ficha or {}).get("preparacion") or "").strip().lower()
    if cat in CATEGORIAS_ANIMALES:
        return (MODO_COCINADO,) if prep and prep != "crudo" else (MODO_CRUDO,)
    if prep and prep != "crudo" and _tiene_hermana_cruda(ficha):
        return (MODO_COCINADO,)
    # Y LA MITAD SIMÉTRICA: una verdura CRUDA que tiene su gemela cocida es del
    # modo crudo. Ver `_tiene_hermana_cocida` — lo pidió Elena el mismo día.
    if (not prep or prep == "crudo") and _tiene_hermana_cocida(ficha):
        return (MODO_CRUDO,)
    return MODOS


def vale_en(ficha, modo):
    """¿Esta ficha se puede usar en este modo? Sin modo, vale todo."""
    if not modo:
        return True
    return modo in modos_de(ficha)


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


# ─── LO QUE SE COMPRA EN UN SÚPER Y LO QUE HAY QUE ENCARGAR ──────────────────
#
# ⚠️ Elena, 14 de septiembre de 2026: «Costillas de cordero e hígado de pato, y
# seguramente otros, me siguen apareciendo en un menú para Cairo automático...
# Eso no son alimentos ni baratos ni accesibles».
#
# Y no era un menú suelto. MEDIDO sobre los 216 menús precalculados, el motor
# elige sistemáticamente el extremo raro de cada categoría:
#
#   · Espinazo de conejo en 105 de 216 y costillas de cordero en 95 -- mientras
#     cuello de pavo, cuello de pato, carcasa de conejo, pecho y cuello de
#     ternera salen en CERO.
#   · Albahaca en 74 (mediana 58 g por menú, máximo 651 g).
#   · Páncreas de vaca en 52. Lengua de ternera en 35, mediana 470 g, máximo
#     3,4 kg.
#   · Y zanahoria, calabacín, judía verde, brócoli, manzana y pera: cero.
#
# LA CAUSA NO ES UN FALLO DEL SOLVER: el MILP optimiza nutrición por gramo y la
# COMPRA no entra en la cuenta. La albahaca es un concentrado de vitaminas y
# minerales por gramo, así que es la forma barata de cerrar huecos; igual la
# lengua, igual el páncreas, igual el espinazo.
#
# ⚠️ ESTA LISTA NO QUITA NADA: reparte los 105 accesibles en dos, y el motor
# PENALIZA los de encargo en el objetivo. Es la misma forma que ya tienen el
# pescado (+1,5) y la rotación de especie (+2,0). Excluirlos estrecharía el
# problema y dejaría sin menú al perro con alergias o al toy, que es la ventana
# más fina que tiene el motor.
#
# Las cifras viven en `lo_facil_de_comprar.json` -- aquí no hay lista escrita:
# es un número que decide qué come un perro y tiene que poder auditarse, igual
# que el catálogo y la tabla de patologías.
import json as _json_facil
import os as _os_facil

with open(_os_facil.path.join(
        _os_facil.path.dirname(_os_facil.path.dirname(_os_facil.path.abspath(__file__))),
                       "lo_facil_de_comprar.json"), encoding="utf-8") as _f_facil:
    _FACIL = _json_facil.load(_f_facil)

DE_ENCARGO = dict(_FACIL["de_encargo"])
FACILES = list(_FACIL["faciles"])


def es_de_encargo(nombre):
    """¿Este alimento hay que encargarlo en vez de comprarlo en el súper?"""
    return nombre in DE_ENCARGO


def por_que_de_encargo(nombre):
    """El motivo escrito, para poder decírselo a quien va a comprar."""
    return DE_ENCARGO.get(nombre)
