# NRC 2006, leído entero — registro capítulo a capítulo

`Nutrient Requirements of Dogs and Cats`, National Research Council, 2006.
43.556 líneas, 15 capítulos. Texto limpio: 28 líneas de 22.276 largas con hueco
de cuatro o más espacios (0,1 %), o sea que **no tiene el problema de las dos
columnas** que tenían SACN5 y FEDIAF.

**Por qué se lee.** Es la fuente de la que deriva FEDIAF, el repo ya la cita en
varios sitios —el ratio linoleico:linolénico de `requisitos_condicionales.json`,
los mínimos de taurina, las alusiones de `patologias.json`— y **no tenía registro
de lectura**. Mismo método que con SACN5: leer entero, apuntar todo, aplicar solo
al final.

**Método.** Cada cita entrecomillada de más de 40 caracteres se comprueba
literal contra `NRC2006/nrc2006.txt` con `auditar_citas.py`, que audita este
documento desde que se añadió a su lista.

---

## Overview (líneas 1.095-1.290, LEÍDO ENTERO)

El Overview no es prosa de cortesía: **define las cuatro clases de cifra del
libro y fija la asunción que usa todo este motor**.

1. **⚠️ LOS 4.000 kcal/kg DE MATERIA SECA SON DE AQUÍ, Y NRC LOS LLAMA ASUNCIÓN.**
   Literal: «The energy density of the diet for both dogs and cats was assumed to
   be 4,000 kilocalories (kcal) of metabolizable energy (ME) per kilogram (kg)».
   Ese es **exactamente** el puente que usan las 94 cifras de `patologias.json`,
   las 12 de `recomendaciones_libro.json` y todas las de SACN5 para pasar de
   «% de materia seca» a «por 1000 kcal». El repo ya lo tenía escrito desde
   FEDIAF (`HALLAZGOS_LECTURA_FUENTES.md` F-16); esto lo confirma **río arriba**,
   en la fuente de la que FEDIAF deriva. No cambia ninguna cifra: confirma que la
   asunción es de las fuentes y no nuestra.

2. **Y NRC avisa de la consecuencia, que es la que más importa aquí.** Literal:
   «Unfortunately, requirements expressed relative to DM change with the energy
   density of the diet, and, in some instances, requirements expressed relative to
   ME may change with body weight (BW)».
   La segunda mitad habla de **la unidad en la que trabaja este motor**: por 1000
   kcal. El motor ya sabe de esto por un lado —`minimo_de()` escala los mínimos
   hacia arriba cuando el perro come menos, por la ecuación 7.2.5 de FEDIAF— y
   NRC dice que la ilustración está en la introducción a las tablas del cap.15.
   **Queda apuntado para leerlo allí**, que es donde hay que comprobarlo, no aquí.

3. **Las cuatro clases de cifra, que no son intercambiables y el repo mezcla en
   una sola palabra.** NRC las define una a una:
   · **Minimal Requirement** — «the minimal concentration or amount of a
     bioavailable nutrient that will support a defined physiological state».
   · **Adequate Intake** — «the concentration in the diet or amount required by
     the animal of a nutrient that is presumed to sustain a given life stage when
     no Minimal Requirement has been demonstrated».
   · **Recommended Allowance** — «the concentration or amount of a nutrient in a
     diet formulated to support a given physiological state», y añade que «is
     based on the Minimal Requirement and, where applicable, includes a
     bioavailability factor».
   · **Safe Upper Limit** — «the maximal concentration or amount of a nutrient
     that has not been associated with adverse effects».
   ⚠️ Esto importa para el día que se cite NRC: **un «mínimo» de NRC puede ser
   tres cosas distintas**, y la que lleva factor de biodisponibilidad es la
   tercera. No se aplica nada todavía; se apunta para no volver a citar «NRC dice
   X» sin decir cuál de las cuatro.

4. **Los perros de referencia detrás de cada «por 1000 kcal».** «Requirements for
   adult dogs at maintenance are based on a 15-kg adult dog that consumes 1,000
   kcal of ME per day» y «Requirements for growth of puppies are based on a 5.5-kg
   puppy that consumes 1,000 kcal of ME per day». Para gestación y lactancia, «a
   22-kg bitch with eight puppies in peak lactation consuming 5,000 kcal of ME per
   day». Son los animales concretos con los que se calibraron las tablas.

5. **Y un aviso de edición que hay que comprobar antes de citar una cifra del
   cap.15**: el propio libro dice que esta versión corrige a la anterior —«Some
   values, particularly in Chapter 15, have been revised or deleted based on the
   availability of new information or to correct errors in calculation»— y que
   «This final version of the report, therefore, supersedes the data contained in
   the prepublication». El `.txt` del repo **sí lleva ese aviso**, o sea que es la
   versión final y no la prepublicación. Comprobado al leerlo, no supuesto.

## cap.1 — Comparative Digestive Physiology of Dogs and Cats (líneas 1.291-2.270, LEÍDO ENTERO)

**Capítulo de referencia, y no hay nada que aplicar.** Es anatomía y fisiología
comparada: compartimentos digestivos, hormonas y medida de la digestibilidad. El
propio libro dice que es nuevo en esta edición y que no cita fuentes originales
en su primera sección. Tres cosas se apuntan porque tocan preguntas que ya están
abiertas en el repo:

1. **El perro pequeño tiene proporcionalmente MÁS intestino, y es un tercer dato
   sobre la pregunta de si la ración cabe en el perro.** Literal: «The weight of
   the empty intestinal tract in small breeds is 6 to 7 percent of their body
   weight, and it decreases to 3 to 4 percent in large and giant breed dogs».
   Se suma a los 30-35 g de materia seca por kg del cap.12 de SACN5 y a los 45-90
   ml/kg de capacidad gástrica del cap.25. **El motor no comprueba en ninguna
   parte que la ración quepa**, y esa pregunta sigue abierta; lo que añade NRC es
   que el margen no es igual en todos los tamaños, y va en la dirección buena para
   el perro pequeño, que es justo el que más volumen come por kilo.

2. **La taurina y la bilis, que es el mecanismo detrás del suelo que el motor ya
   aplica.** «More than 99 percent of bile acids normally are conjugated with
   taurine to form taurocholic acid, taurodeoxycholic acid, and
   taurochenodeoxycholic acid in both dogs and cats» — en el perro **también**,
   no solo en el gato. Y el capítulo señala que el procesado térmico afecta al
   estado de taurina, por aumentar lo que llega al intestino grueso. Una ración
   cruda no lleva ese procesado. No es una cifra: es contexto del suelo de
   taurina que ya está puesto en `dcm_taurina_respondedora`.

3. **Ni el perro ni el gato tienen amilasa salival**: «Like many species, dogs and
   cats lack the α-amylase enzyme that would initiate the process of starch
   digestion». Y la amilasa pancreática del cachorro es mucho más baja que la del
   adulto. No toca al motor —una ración cruda apenas lleva almidón— pero es el
   dato que hay debajo de las recomendaciones de hidratos de otras fuentes.

**Nada de este capítulo entra en el motor.**

## cap.2 — Feeding Behavior of Dogs and Cats (líneas 2.687-3.300, LEÍDO ENTERO)

Capítulo de comportamiento. Tres cosas cruzan con el motor, y **dos confirman
cosas que el repo ya dice**:

1. **El agua de la comida, que es justo la mitad buena del aviso del
   estreñimiento.** Escribí ayer en ese aviso que la comida cruda juega a favor
   porque lleva más agua, citando a SACN5. NRC lo dice más fuerte y con cifra:
   «both dogs and cats are able to maintain water balance when fed meat or fish
   containing 67-73 percent water, without drinking any water». Y marca el
   límite: ni el gato aguanta con carne desecada al 61 % de humedad. **Segunda
   fuente independiente para esa frase.** No cambia nada; la respalda.

2. **⚠️ NRC dice que un perro adulto normal está bien con UNA toma al día, y eso
   parecía chocar con lo que el motor recomienda.** Literal: «normal adult dogs
   will maintain optimal health if fed only one meal a day», y para el cachorro
   «growing puppies should be fed either free-choice or two or three times a
   day».
   **Comprobado en el motor, y NO hay choque**: el consejo de repartir en 2-3
   tomas vive **solo** en el aviso de `riesgo_gdv`, no en ningún aviso general.
   O sea que el motor le dice «reparte» al perro con riesgo de vólvulo —que es lo
   que pide SACN5 cap.53— y no se lo dice al resto, que es lo que pide NRC. Las
   dos fuentes conviven porque hablan de poblaciones distintas. **Queda escrito
   para que nadie lo "arregle" por error metiendo el consejo en el aviso
   general.**

3. **Lo que un perro elige comer cuando puede elegir**, que no es un requisito
   pero da contexto a la pregunta de si un BARF lleva demasiada proteína: los
   perros, como las ratas, «will choose about 25-30 percent of their calories as
   protein». Una ración de este motor ronda los 105 g/1000 kcal, o sea un 42 % de
   las calorías. **No se aplica nada**: elegir no es requerir, y el propio
   capítulo dice que la elección la mandan la palatabilidad y el aprendizaje. Se
   apunta porque es un tercer número en esa conversación, junto al 30 % MS del
   cap.13 de SACN5 y al 23 % del maduro.

## cap.3 — Energy (líneas 3.301-4.640, LEÍDO ENTERO)

### ⚠️ EL HALLAZGO: el motor calcula las kcal del hueso con unos factores que esta fuente excluye para el hueso, con esas palabras

NRC explica de dónde salen los factores de Atwater (4 kcal/g proteína, 9 grasa,
4 hidratos) y **para qué alimentos valen**, nombrando la excepción:

> «The resulting Atwater factors of 4 for protein, 9 for fat, and 4 kcal·g–1 for
> carbohydrate (nitrogen-free extract; NFE) still work amazingly well for
> ingredients in homemade diets for dogs: meat, offal (except bones and bone
> meal), poultry, fish, highly purified starch products, milk products, and even
> chocolate»

«**except bones and bone meal**». Y la Tabla 3-1 repite la frontera en su columna
«Application», reservando la ecuación de Atwater para el alimento sin procesar o
de consumo humano —carne, despojos, lácteos y fuentes de almidón cocinadas—.
(Sin comillas a propósito: esa celda de la tabla sale con sus dos columnas
entrelazadas en el `.txt`, así que no hay una frase contigua que citar.)

**COMPROBADO EN EL CATÁLOGO, no supuesto.** Las nueve fichas de «Hueso carnoso»
tienen su `energia` **exactamente igual** a 4×proteína + 9×grasa, hasta el
decimal, y sus propias notas lo dicen: «Energia calculada de sus macros».

| Ficha | energía del catálogo | 4×prot + 9×grasa |
|---|---|---|
| Carcasa de pollo | 240,2 | 240,2 |
| Cuello de pavo | 132,4 | 132,4 |
| Cuello de pato | 318,8 | 318,8 |
| Carcasa de conejo | 158,5 | 158,5 |
| Costillas de cordero | 185,9 | 185,9 |
| Carcasa de pato | 229,9 | 229,9 |

**Por qué importa y no es cosmético**: el hueso carnoso es el 20-60 % de cada
ración por la regla de forma, y **todos** los límites del motor —los 43 de
FEDIAF, los cinco de seguridad crónica, los del libro y los 75 de patología— van
«por 1000 kcal». Las kcal son el denominador de todo. Si el denominador del hueso
está mal, todo el menú parece más o menos concentrado de lo que está.

**Lo que NO puedo decir todavía, y no lo voy a decir**: ni el tamaño ni la
dirección del error. Köber 2017 —la fuente de estas fichas, comprobada: sus
macros coinciden— **no da energía**: solo materia seca, proteína bruta, grasa
bruta, cenizas, calcio y fósforo. O sea que en el repo **no hay una energía
medida del hueso con la que comparar**. Lo que sí se sabe es por dónde mirar: los
factores de Atwater llevan dentro una digestibilidad supuesta —NRC la explicita,
«Atwater factors include a digestibility of 98 percent for carbohydrate, 96
percent for fat, and 90 percent for protein»— y la proteína del hueso es sobre
todo colágeno. Si el colágeno no se digiere al 90 %, la energía real es **menor**
que la calculada. **Eso hay que comprobarlo en el cap.6 de NRC**, que es el de
proteína, y ahí lo miraré. No antes.

⚠️ Y un matiz que juega a favor del motor: NRC **recomienda** Atwater justo para
lo que hace Rawku — «For dogs, Atwater factors are still recommended for use for
table food if no other data are available». La excepción del hueso es una
excepción dentro de una recomendación que por lo demás encaja.

### Lo que CONFIRMA el DER del motor, río arriba de FEDIAF

NRC da 132 kcal × BW^0,75 para perros de perrera jóvenes y activos, y dice que el
perro de casa está por debajo: «Pet dogs without opportunity and stimulus to
exercise need between 10 and 20 percent less energy than experimental dogs». El
suelo que cita, medido por calorimetría en perros de dueño, ronda «90 kcal·kg
BW–0.75».

El motor aplica la tabla de FEDIAF: 95 sedentario, **110 normal**, 125, 150-175.
Ese 110 es exactamente 132 menos un 17 %, o sea **dentro de la banda que NRC
describe para el perro de compañía**. No hay nada que cambiar: es una
confirmación desde la fuente de la que deriva FEDIAF.

NRC da además una ecuación lineal «de cabecera» para 8-20 kg: energía en
kilocalorías «= 358 + 39 × BW». Queda apuntada como contraste disponible para
`der_casos.json`, no como sustituta.

### La capacidad de comer, cuarta cifra y la más precisa hasta ahora

La pregunta de si la ración cabe en el perro lleva abierta desde el cap.12 de
SACN5 (30-35 g de materia seca por kg) y el cap.25 (45-90 ml/kg de capacidad
gástrica). NRC añade dos datos, y los dos dicen que **el margen depende del
tamaño**:

· «The weight of the empty intestinal tract in small breeds is 6 to 7 percent of
  their body weight, and it decreases to 3 to 4 percent in large and giant breed
  dogs» (cap.1).
· Y en lactancia, que es cuando más come: «Small- and medium-sized breeds can
  increase their dry matter intake during lactation to around 4.5 percent of
  their body weight; some individuals may even reach an intake of up to 9 percent
  of body weight», mientras que los daneses «do not eat more dry matter than
  2.5-3.2 percent of their body weight even if they suckle a large litter».

El motor **no comprueba en ninguna parte que la ración quepa**, y en lactancia de
raza gigante es donde más apretaría. Sigue siendo una pregunta abierta, ahora con
cifras por tamaño.

### Y dos confirmaciones más, sin cambio

· **La condición corporal**: «It is recommended to keep BCS (system with 9
  scores) within the range of 4 to 5 in dogs», que es el mismo corte de la AAHA
  2021 que el repo ya tiene verificado.
· **Sobrealimentar de energía basta para romper el esqueleto del cachorro grande,
  aunque todo lo demás esté bien**: «Feeding too much energy in combination with
  a well-balanced intake of all other nutrients will induce growth disorders in
  predisposed breeds such as Great Danes». Es el argumento de fondo de los techos
  de calcio y fósforo de crecimiento que el motor ya aplica, dicho desde la
  energía.

## cap.4 — Carbohydrates and Fiber (líneas 5.146-7.400, LEÍDO ENTERO)

### ⚠️ EL HALLAZGO: el motor compara fibra de una clase contra límites de otra

Ocho patologías del motor ponen un suelo o un techo de **fibra**. Las ocho cifras
salen de tablas de SACN5. Las ocho se comparan contra el campo `fibra` del
catálogo. Y **no son la misma fibra**.

**La mitad de la fuente.** Las tablas de SACN5 están en **fibra bruta** (*crude
fiber*), que es la que declaran las etiquetas de pienso. Tres lo dicen con esas
palabras en la propia fila —«Crude fiber ≤5%» en la 58-1, «Crude fiber ≥8%» en la
63-3, «≥7% crude fiber» en la 64-2— y el pie de la 63-3 explica por qué las demás
también lo son:

> «Crude fiber is the only fiber value readily available for pet foods»

El capítulo 5 de SACN5 dice de dónde viene esa costumbre —«regulations require
that the maximum amount of crude fiber be listed on the label of all pet foods»—
y lo que vale ese número: «Because the crude fiber analysis underestimates
fermentable fiber, it does not accurately represent the total fiber in a pet
food».

**La otra mitad, la del catálogo.** El campo `fibra` es **fibra dietética total**,
que es lo que publican BEDCA, CIQUAL y USDA. No es deducción: dos fichas lo dicen
literal en su propia `nota_datos` —«BEDCA, "Coles de Bruselas" — fibra dietética
total 4,3 g/100 g» y la misma frase en el puré de tomate—, y el propio SACN5
explica que ese es el método del **otro** lado: «This analysis is used to
determine total fiber and is commonly used for measuring fiber content of human
foods». El catálogo de Rawku se construye justo de bases de alimentación humana.

**Cuánto separa a las dos.** NRC lo cuantifica en una frase:

> «The crude fiber method accounts for only 5 to 20 percent of the total fiber in
> a food and, as such, underestimates the true DF concentration»

Y la Tabla 5-9 de SACN5 lo enseña ingrediente a ingrediente, con las dos columnas
al lado. La proporción no es una constante: va del **0 %** al **82 %**, y el 0 no
es un caso raro, es el de toda la fibra soluble.

| Ingrediente | Fibra bruta (%) | Fibra dietética total (%) | Bruta / total |
|---|---|---|---|
| Pectina de manzana | 0 | 95 | 0 % |
| Goma guar | 0 | 81 | 0 % |
| Goma arábiga | 0 | 91 | 0 % |
| Pulpa de cítrico | 12 | 77 | 16 % |
| Salvado de maíz | 19 | 90 | 21 % |
| Pulpa de remolacha | 20 | 66 | 30 % |
| Fibra de guisante | 30 | 92 | 33 % |
| Cáscara de cacahuete | 57 | 76 | 75 % |
| Celulosa | 80 | 98 | 82 % |

(La fila «Rice bran 44 / 13» de esa misma tabla sale con la bruta por encima de
la total, que es imposible. No se usa: o es una errata del libro o es el texto a
dos columnas otra vez.)

**En qué dirección falla cada límite.** Como la bruta siempre es menor o igual
que la total, comparar un valor de total contra un umbral de bruta falla en los
dos sentidos según el límite sea suelo o techo, y solo uno de los dos es el lado
seguro:

· Los **cinco suelos** (obesidad 30, hiperlipidemia 25, intestino irritable 20,
  estreñimiento 17,5, diabetes 17,5 g/1000 kcal) se dan por cumplidos con una
  fibra bruta real muy por debajo de la que pide la fuente. El motor cree que
  entrega el 7-12 % de MS que pide la tabla y entrega una fracción.
· Los **tres techos** (flatulencia, insuficiencia pancreática exocrina y
  linfangiectasia, los tres 12,5 g/1000 kcal) rechazan menús cuya fibra bruta
  real está holgadamente por debajo del techo. Aquí el error aprieta de más, que
  es el lado seguro, pero estrecha sin motivo la ventana de un perro enfermo.

**MEDIDO, no supuesto.** Pidiendo a la API un menú para el perro de referencia
(20 kg, DER 950, adulto) con cada una de las ocho patologías marcadas:

| Patología | Límite | Fibra total entregada | En % MS | Fibra BRUTA real (al 5-20 %) | Lo que pide la fuente |
|---|---|---|---|---|---|
| Obesidad | suelo 30 | 45,35 | 18,14 % | 0,91 a 3,63 % | 12 % |
| Hiperlipidemia | suelo 25 | 38,88 | 15,55 % | 0,78 a 3,11 % | 10 % |
| Estreñimiento | suelo 17,5 | 26,73 | 10,69 % | 0,53 a 2,14 % | 7 % |
| Diabetes | suelo 17,5 | 25,89 | 10,35 % | 0,52 a 2,07 % | 7 % |
| Intestino irritable | suelo 20 | 20,02 | 8,01 % | 0,40 a 1,60 % | 8 % |
| Flatulencia | techo 12,5 | 0,43 | 0,17 % | 0,01 a 0,03 % | ≤5 % |
| Insuf. pancreática exocrina | techo 12,5 | 2,54 | 1,02 % | 0,05 a 0,20 % | ≤5 % |
| Linfangiectasia (PLE) | techo 12,5 | 2,13 | 0,85 % | 0,04 a 0,17 % | ≤5 % |

Lo que dice esta tabla, en una línea: **ninguno de los cinco suelos se cumple en
la unidad de su propia fuente**, ni siquiera en el extremo más favorable del rango
de NRC. Y **los tres techos no aprietan a nadie**: una ración BARF sale con 0,2-1 %
de fibra bruta de MS, o sea diez veces por debajo del techo, así que ahí el error
de unidad no le quita menús a ningún perro. **El problema son los suelos.**

**Y el propio NRC dice que esto ya se ha medido, justo en la diabetes.** Al
revisar por qué la fibra bruta no predecía la glucemia en perros:

> «No relationship was found between crude fiber content of the diet and blood
> glucose or insulin»

> «This was attributed to the inability of the crude fiber analysis to recover
> soluble dietary fibers, which can play a key role in mediating postprandial
> hyperglycemia»

O sea: la unidad en la que está escrito nuestro suelo de diabetes es
precisamente la que la fuente dice que no sirve para lo que ese suelo quiere
conseguir.

**Lo que NO se toca, y por qué.** No hay factor de conversión que aplicar. NRC da
un rango de **cuatro veces** (5 a 20 %) y la tabla de SACN5 enseña que dentro de
ese rango el valor depende del ingrediente, con el 0 para la fibra soluble —que
es justo la del psyllium del catálogo—. Y la Tabla 63-3 sí ofrece las filas en
términos de fibra dietética (soluble 1-5 %, mixta 5-10 %, insoluble 10-15 %),
pero elegir cuál es la del perro es explícitamente clínico: «Any one of the three
types of fiber listed at the recommended levels can be effective, depending on
patient response». Inventarse un factor o elegir una fila sería poner un número
que parece bueno. Queda escrito, medido, y con la pregunta hecha en
`PENDIENTE_NUTRICION.md`.

⚠️ Y una frase de `patologias.json` que era **falsa** y se corrige con esto: el
`por_que` de `intestino_irritable` decía que se usaba la fila de fibra bruta
«porque es la unica que el catalogo sabe medir». Es al revés. Esa nota al pie de
SACN5 habla de **piensos**, cuya etiqueta solo declara la bruta; el catálogo de
Rawku es el único de los dos que **sí** tiene el valor de fibra dietética total.

### Lo que confirma, sin cambio

· **La proteína de gestación y lactancia sin hidratos**, que el motor ya aplica
  desde `requisitos_condicionales.json`, con el experimento entero: Kienzle 1985,
  dieta sin hidratos, «in bitches fed the low-protein, carbohydrate-free diet (20
  percent of calories from protein), a reduction in birth weight (30 to 40
  percent) and an increase in perinatal mortality rate (75 percent) were
  observed». Y la conclusión en las palabras de NRC: «although pregnant and
  lactating bitches do not require a dietary source of carbohydrate, they have
  increased protein requirements when fed a carbohydrate-free diet».
· **El ritmo de adelgazamiento** que dice el aviso de obesidad del motor: NRC lo
  pone en «0.5 to 2 percent of initial body weight per week». El aviso dice 1-2 %,
  dentro de la banda.

### Lo que NO se aplica, y por qué no

· **La fibra insoluble en gestación y lactancia**: «supplementing a bitch's diet
  with insoluble fiber during the latter phases of pregnancy and during lactation
  should be avoided since it will decrease the energy density of the diet». No es
  una cifra, y el motor no separa fibra soluble de insoluble. Importa el día que
  una perra gestante lleve además obesidad o estreñimiento marcados, que son las
  dos patologías que empujan fibra hacia arriba.
· **La fibra le quita hierro al perro**: perfundiendo intestino de perro sano con
  hierro más psyllium, «they exhibited reduced (P < 0.05) iron uptake (32.0
  μg·h–1) as compared to iron alone (71.9 μg·h–1)», y con pectina, 28,5. Es menos
  de la mitad. No hay dosis-respuesta que convertir en un límite, y el hierro del
  motor ya lleva su mínimo de FEDIAF, pero queda apuntado porque el catálogo tiene
  psyllium y cinco patologías empujan la fibra hacia arriba.
· **El mecanismo escrito en el `por_que` de la obesidad** —«La fibra da saciedad
  con pocas kcal»— lo desmiente NRC para la fibra insoluble: «indicating that
  mechanical satiation is not a mechanism by which insoluble fiber decreases food
  intake», y remata «Fiber content is not central to a low-calorie diet; rather,
  caloric intake of the animal per unit of time» es lo que decide. No cambia la
  cifra, que es de SACN5 y sigue en pie; cambia el motivo que tenemos escrito.
· **La edad a la que un perro es geriátrico, que NRC parte por tamaño**:
  «Generally, giant- and large-breed animals are considered geriatric at 5 years
  of age, whereas medium- or small-breed dogs and all cats are not considered
  geriatric until 7 or more years of age». El motor usa **7 años para todos**. Es
  la misma forma que las dos filas de raza de FEDIAF, pero aquí NRC está
  definiendo una palabra, no publicando un requisito, y el escalón de energía que
  el motor aplica es el de la Tabla VII-6 de FEDIAF, que es otra fuente y otra
  cosa. Queda apuntado, sin tocar nada: lo que sí cambiaría por tamaño es el techo
  de fósforo del sénior (1750 contra 2000), y esa cifra es del libro, no de NRC.
