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
documento desde que se añadió a su lista. Y ya ha servido: el 11 de septiembre
cazó una cita mía del cap.14 en la que había escrito «diabetes mellitus» donde la
fuente pone «type II diabetes mellitus», y al ir a arreglarla apareció que me
había dejado fuera la frase siguiente, que matiza la conclusión entera.

## ESTADO: LEÍDO ENTERO, los 15 capítulos, el 11 de septiembre de 2026

| Capítulo | Qué salió |
|---|---|
| Overview, 1, 2 | contexto; sin cifra que aplicar |
| 3 Energía | la exclusión del hueso de Atwater · confirma el DER del motor |
| 4 Hidratos y fibra | ⚠️ la fibra del catálogo y la de las tablas no son la misma |
| 5 Grasa | dos techos que FEDIAF no tiene: grasa 82,5 y linoleico 16,3 g/1000 kcal |
| 6 Proteína | el techo de lisina, con su mecanismo medido · confirma arginina y taurina |
| 7 Minerales | once de doce minerales **no tienen techo** para el perro; los tres que sí, confirman a FEDIAF |
| 8 Vitaminas | ⚠️ la colina se pasa en los 36 menús · confirma el tope de vitamina D · dos techos de vitamina A |
| 9 Agua | 1 mL por kcal; una ración cruda lo cubre casi solo |
| 10 Laboratorio | leído y descartado con motivo |
| 11 Actividad y ambiente | ⚠️ los topes de seguridad deberían APRETARSE en el perro de trabajo |
| 12 Formulación | pienso; nada transferible |
| 13 Composición de ingredientes | ⚠️ **corrige el hallazgo del hueso**: la Tabla 13-1 sí da EM de un ingrediente con hueso |
| 14 Otros componentes | la glucosamina y la diabetes · confirma la L-carnitina |
| 15 Tablas de requisitos | confirma la densidad de 4.000 kcal/kg con la que el repo convierte todo |

**Cuatro cosas quedan medidas y sin aplicar**, cada una por su motivo escrito: la
unidad de la fibra (no hay factor), la colina (la cifra de la fuente es débil), los
dos techos de grasa y linoleico y los dos de vitamina A (caben, pero hay que medir
con el solver antes), y el apretón de los topes de seguridad en el perro de trabajo
(hay que comprobar que sigue habiendo menú).

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

## cap.5 — Fat and Fatty Acids (líneas 8.497-10.430 la parte canina, LEÍDO ENTERO)

El resto del capítulo (10.430 en adelante) es felino y bibliografía.

### ⚠️ DOS TECHOS QUE FEDIAF NO TIENE, y que este capítulo sí da con cifra

FEDIAF pone **mínimo** de grasa (13,75 g/1000 kcal en adulto) y **ningún
máximo**, en ninguna etapa. NRC sí, y los dos son del perro sano:

> «The safe upper limit (SUL) for total dietary fat is approximately 70 percent ME
> or 82.5 g per 1,000 kcal ME»

> «the SUL for LA is estimated at 16.3 g per 1,000 kcal (13.8 percent ME)» ·
> «Amounts of LA in excess of this amount are not recommended for long-term
> feeding»

**De dónde sale el de la grasa, que no es un número redondo por casualidad**: de
un experimento que *indujo pancreatitis* en perros con unos 92 g/1000 kcal
(Lindsay 1948, 6 % ME de proteína y 78 % ME de grasa), menos un margen del 10 %.
NRC lo dice así de claro: el SUL «is based on a safety margin of about 10 percent
less than the amount reported to have induced pancreatitis».

**MEDIDO sobre los 216 menús del catálogo, antes de proponer nada:**

| | mínimo | mediana | máximo | por encima del SUL |
|---|---|---|---|---|
| Grasa (SUL 82,5) | 44,91 | 61,22 | 76,07 | **0 de 36** |
| Linoleico (SUL 16,3) | 3,20 | 3,53 | 7,23 | **0 de 36** |

O sea que los dos **caben de sobra hoy**. Es exactamente la situación del techo de
sodio del perro sano: un techo que hoy no aprieta a nadie, y que seguirá estando
el día que el catálogo cambie. Y el de la grasa tiene además el contexto que da la
propia fuente: «Many practical diets for healthy dogs will typically contain
between 22 and 60 g per 1,000 kcal ME total fat» — nuestra mediana, 61,2, queda
justo en el borde alto de lo normal, que para una ración cruda es lo esperable.

### Lo que CONFIRMA, sin cambio

· **El ratio linoleico:linolénico que el motor ya aplica**, con sus dos rangos y
  con el motivo de por qué se usa ese y no el omega-6:omega-3 total: «A range for
  this ratio of 2.6 to 26 is presumed safe based on evidence to date» en
  mantenimiento y crecimiento, y «the LA:ALA ratio should range between 2.6 and
  16» en gestación y lactancia. Y el porqué, literal: «The European expert
  committee also specifically concluded that the use of a total n-6:n-3 ratio is
  not helpful».
· **El tope crónico de EPA+DHA del motor (2,8 g/1000 kcal)** es exactamente el
  número de esta página: «establishes an SUL for total n-3 LCPUFAs in dogs of
  approximately 2.4 percent ME (i.e., 2.8 g per 1,000 kcal)». El motor lo aplica
  como **presupuesto semanal**, que es más estricto.

### Lo que NO se aplica, y por qué no

· **La ingesta adecuada de EPA+DHA del adulto, 0,11 g/1000 kcal**: «an AI of
  0.11g per 1,000 kcal of combined EPA and DHA for overall health is
  recommended». Es una **AI**, no un requisito —NRC dice en la misma página que
  «A specific requirement for long-chain n-3 PUFAs (EPA and DHA) in adult dogs
  has not been identified to date»—, y FEDIAF no pone mínimo de EPA+DHA en
  adulto. Queda apuntado con su cifra para decidirlo con el número delante.
· **Las cifras de crecimiento calculadas de la leche de perra** (grasa 8,5 % MS,
  linoleico 1,18 % MS, linolénico 0,07 % MS, DHA ~0,03 % MS, araquidónico
  0,03-0,05 % MS y EPA que «should not exceed more than 0.03 percent DM»). La
  propia fuente avisa de lo que valen: «it must be emphasized that these are, at
  best, only estimates of AI. There are no published studies available to define
  precisely the MR, AI, or RA values for these fatty acids». Y el catálogo no
  separa DHA de EPA en todas las fichas.

## cap.6 — Protein and Amino Acids (líneas 11.543-14.180 hasta la bibliografía, LEÍDO ENTERO)

### ⚠️ LO QUE ESTE CAPÍTULO DICE DEL TECHO DE LISINA, que era la única excepción escrita del motor

El motor **no aplica** el techo de lisina de FEDIAF (7,00 g/1000 kcal, solo en
crecimiento) porque 0 de 12 menús de cachorro caben debajo. Es la única excepción
de todo el motor y llevaba la pregunta abierta. NRC da aquí las dos mitades que
faltaban:

**La cifra.** Para el perro, «The SUL for lysine is >20 and <40 g·kg–1 diet
containing 4.0 kcal ME·g–1», que a 4000 kcal/kg son **5 a 10 g/1000 kcal**. O sea
que el 7,00 de FEDIAF cae **dentro de la banda de incertidumbre de NRC**, y ninguna
de las dos fuentes sabe dónde está el techo de verdad.

**El mecanismo, que es lo que de verdad contesta.** El único daño documentado es un
**antagonismo lisina-arginina**: «40 g excess lysine in the diet caused a growth
depression and classical clinical signs of arginine deficiency» — y eso fue con la
arginina a 4 g/kg, o sea una proporción de **10:1**.

**MEDIDO sobre los 12 menús de cachorro del catálogo:**

| | lisina | arginina | lisina:arginina |
|---|---|---|---|
| el más alto | 11,63 | 8,51 | 1,37 |
| mediana | 9,04 | — | **1,35** |
| el más bajo | 6,07 | — | 1,30 |

**Cinco de los doce pasan de 10 g/1000 kcal**, que es el extremo alto de la banda de
NRC. Pero el ratio lisina:arginina va de **1,30 a 1,39**, cuando el antagonismo que
NRC documenta ocurrió a **10:1**. Y no es casualidad: en una ración BARF la arginina
sube con la proteína igual que la lisina, así que las dos se mueven juntas.

**No cambia la decisión, y la refuerza**: el techo sigue sin aplicarse, y ahora la
razón escrita no es solo «no cabe», sino que **el daño que la fuente describe
necesita una desproporción que nuestros menús no tienen, ni de lejos**. Sigue siendo
pregunta para el nutricionista, con estos números delante.

### Lo que CONFIRMA, por segunda fuente independiente

· **La arginina que sube con la proteína**, que el motor aplica desde la Tabla
  VII-13 de FEDIAF: NRC llega al mismo sitio por su cuenta, «it is recommended that
  0.01 g arginine be added for each gram of crude protein above the requirement».
  **El mismo factor, 0,01, en dos fuentes que no se copian.**
· **El suelo de taurina de la DCM** (250 mg/1000 kcal, que el motor aplica desde
  SACN5 Tabla 36-4): NRC da «about 1,000 mg taurine·kg–1 diet (DM)» para dietas
  bajas en proteína o en aminoácidos azufrados, que a 4,0 kcal/g son **exactamente
  250 mg/1000 kcal**. Otra vez el mismo número por dos caminos.
· **Y por qué el perro sano no lleva suelo de taurina**: «the MR for taurine for
  dogs fed a normal diet is 0». El perro la fabrica de los aminoácidos azufrados;
  el problema aparece con dietas bajas en proteína o con azufrados poco
  disponibles — que es lo contrario de una ración BARF.

### Lo que NO se aplica, y por qué no

· **Casi ningún aminoácido tiene techo para el perro.** NRC repite la misma frase
  en arginina, histidina, isoleucina, leucina, fenilalanina, tirosina, treonina,
  triptófano, valina y taurina: no hay estudios de toxicidad, «so no SUL can be
  established». O sea que el hueco no es nuestro: **no existe el dato**. El único
  con cifra es la metionina, y en su forma sintética: «it would appear that the SUL
  for DL-methionine is well below 47 g·kg–1 diet», que es un límite superior sin
  suelo, no un techo utilizable.
· **La proteína del perro mayor**: «Older dogs appear to require somewhat more crude
  protein to maintain labile protein (so-called protein reserves), perhaps as much
  as 50 percent more». ⚠️ Y **SACN5 dice lo contrario**: su Tabla 14-2 da al perro
  maduro 15-23 % de MS de proteína, cuyo extremo bajo (37,5 g/1000 kcal) queda **por
  debajo** del mínimo de FEDIAF que ya aplicamos (52,10). FEDIAF no tiene tabla de
  sénior, así que aquí no hay una norma que rompa el empate: son dos fuentes en
  desacuerdo y el motor se queda en el mínimo de FEDIAF, que es el más alto de los
  dos suelos. Queda apuntado en `FEDIAF_CONTRA_OTRAS_FUENTES.md`.

### Y una frase que conviene tener presente al mirar cualquier aminoácido

> «in general, dogs appear to be more sensitive to disproportionalities among
> dietary amino acids than cats, especially when fed low-protein diets»

El «especially when fed low-protein diets» es la parte que nos toca al revés: una
ración BARF va sobrada de proteína, que es el lado seguro de esa frase.

## cap.7 — Minerals (líneas 15.283-19.300 la parte canina, LEÍDO ENTERO)

### El resultado más útil del capítulo: los techos que NO existen

NRC va mineral por mineral diciendo si se puede fijar un **safe upper limit** para
el perro. La respuesta, once veces de doce, es que **no hay datos**. Eso no es un
hueco nuestro: es que el dato no existe en la literatura, y conviene tenerlo
escrito para no volver a buscarlo.

| Mineral | Qué dice NRC del techo para el PERRO |
|---|---|
| Calcio | **4,5 g/1000 kcal** en cachorro de raza gigante |
| Fósforo | «There are insufficient data on which to base an SUL for P in dogs» |
| Magnesio | «There are no reported adverse effects of excess consumption of Mg in dogs» |
| Sodio | **~15 g/kg MS** |
| Potasio | «There are no data on which to base a SUL for dietary concentrations or intake of K» |
| Cloruro | no hay estudios de exceso en el perro |
| Hierro | «no recommendations as to a SUL of Fe in dogs can be made» |
| Cobre | «there is no available information on a SUL of dietary Cu in normal dogs» |
| Zinc | «there is insufficient information available on which to base a SUL of dietary Zn for dogs» |
| Manganeso | «There are no reports of toxic effects of excess consumption of Mn in dogs or cats» |
| Selenio | no hay SUL; solo el máximo regulatorio de AAFCO, 2,0 mg/kg MS |
| Yodo | «an absolute figure for a SUL of dietary I cannot be predicted for adult dogs» |

### Y los TRES que sí tienen cifra confirman lo que ya aplica el motor

· **Calcio en crecimiento**: «a safe upper limit (SUL) for Ca in growing
  giant-breed puppies may reasonably be set at a minimum of 4.5 g per 1,000 kcal
  ME». Es **exactamente** el máximo de FEDIAF en crecimiento (4500 mg). Dos
  fuentes, el mismo número. Y el motor aprieta por debajo, a 2750 para el cachorro
  que pasará de 25 kg, por SACN5 y Fascetti.
· **Sodio**: «the SUL of Na for dogs can reasonably be set at approximately 15 g
  Na·kg–1 diet, DM basis», que a 4000 kcal/kg son **3750 mg/1000 kcal**. Otra vez
  el máximo de FEDIAF clavado. Y el motor aprieta a 1000 por el techo del libro.
· **Yodo**: la cifra de la que sale nuestro tope crónico. Los alimentos
  comerciales que Belshaw midió llegaban a **1.275 µg/1000 kcal** y se dieron sin
  problema, mientras que a **1.400** Castillo vio función tiroidea deprimida y
  alteraciones óseas en cachorros. El motor aplica 1275, o sea el más alto que la
  fuente documenta como seguro. Confirmado literal.

### Lo que CONFIRMA de los dos ceros de biodisponibilidad

El fichero `sacn5_fuentes_de_minerales.json` guarda dos fuentes cuyo mineral **se
analiza y no llega al perro**. NRC dice lo mismo, por su cuenta y con otras
palabras: «Iron oxide and carbonate demonstrate negligible bioavailability and
should not be used as dietary sources of Fe» y «cupric oxide is only very slightly
bioavailable and therefore should not be used as a Cu supplement in petfoods». Y
añade el del hígado de cerdo: «there are reports that the Cu present in some animal
liver (e.g., pork liver) may not be bioavailable».

### Un matiz sobre nuestro tope de selenio, que no cambia nada pero conviene saber

El motor aplica **570 µg/1000 kcal**, que es la cifra de AAFCO en base energética.
NRC confirma su origen —«for regulatory purposes, a maximum standard of 2.0 mg
Se·kg–1 has been suggested (AAFCO, 2001)»— pero ese 2,0 mg/kg de materia seca, a
la densidad de **4,0 kcal/g que este repo usa para todo lo demás**, daría **500**,
no 570: el 570 sale de la densidad de 3,5 kcal/g con la que AAFCO publica su
equivalente. No se toca, porque 570 es la cifra que la propia AAFCO publica en la
unidad en la que la aplicamos, y porque medido no cambia nada: el máximo de los
menús reales es 142 µg/1000 kcal, cuatro veces por debajo de los dos. Queda
escrito para que nadie lo «arregle» sin saber de dónde sale cada número.

### Y el mecanismo que explica un pendiente ya abierto

El capítulo 4 dejó apuntado que la fibra le quita hierro al perro. Aquí está el
listado completo de lo que compite: «Intestinal absorption of inorganic Fe is
inversely related to Fe status, to the dietary concentration of Fe, and to the
dietary concentrations of several other nutrients such as Ca, P, Zn, and Cu», y
el calcio baja la absorción del hierro **hemo** también. En una ración BARF, que
va cargada de calcio del hueso, eso juega en contra. No hay cifra que aplicar
—NRC no da factor—, pero es el mismo aviso desde otro lado.

## cap.8 — Vitamins (líneas 20.308-24.470 la parte canina, LEÍDO ENTERO)

### ⚠️ EL HALLAZGO: la COLINA de nuestros menús se pasa del máximo que propone NRC, y en los 36

NRC propone para la colina, tras revisar la tolerancia de los animales al exceso:

> «A presumed safe maximum intake of 2,000 mg choline·kg–1 diet is proposed»

A 4,0 kcal/g son **500 mg/1000 kcal**. **FEDIAF no pone máximo de colina.**

**MEDIDO sobre los 216 menús del catálogo:**

| | máximo | por encima de 500 |
|---|---|---|
| Adulto y sénior | 1.125 mg/1000 kcal | **24 de 24** |
| Cachorro | 1.071 mg/1000 kcal | **12 de 12** |

O sea que **todos** nuestros menús llevan más del doble. Es el primer caso de este
repaso en que una cifra de NRC va en contra de lo que el motor entrega.

**Y por eso NO se aplica como techo, al menos no sin preguntar.** Lo que la propia
fuente dice de ese número lo debilita en tres sitios:

1. Es un **«presumed safe maximum»**, y sale de que McKibbin dio 1.500 y 2.000
   mg/kg de **suplemento** a cachorros sin problema, no de haber encontrado daño.
   Es donde pararon los estudios, no donde empieza la toxicidad.
2. El único trabajo que sí vio anemia (Davis, 1944) lo critica NRC en la misma
   página: no tenía controles y la dieta basal podía ser deficiente en algo.
3. La colina de nuestros menús es **de alimento** (hígado, huevo, vísceras), no
   cloruro de colina añadido, que es la forma con la que se hicieron esos
   estudios.

Y hay una cuarta razón, que es de fondo: «dietary requirements for choline are not
fixed but will respond to other components of the diet that are potential methyl
donors, particularly methionine, and nutrients such as cobalamin and folate». Una
ración BARF va cargada de metionina, y eso mueve la ventana entera.

**La pregunta para el nutricionista**: ¿un menú con 1.100 mg de colina por 1000
kcal, toda de alimento y con metionina de sobra, es un problema, o el 2.000 mg/kg
de NRC no aplica a este caso?

### Lo que CONFIRMA, y es el tope de seguridad más importante del motor

**La vitamina D.** El motor aplica `TOPE_VITD_KCAL = 20`. NRC lo dice con esas
palabras y esa unidad:

> «It is suggested that a dietary concentration of cholecalciferol should not
> exceed 20 μg per 1,000 kcal for growing dogs»

y lo extiende al resto: «In the absence of long-term studies on dogs at maintenance
and pregnant and lactating dogs it is suggested that these upper dietary
concentrations be also applied to these dogs». **Exacto, y de la fuente primaria.**
Y el máximo de FEDIAF (14,1875) es todavía más estricto, que es el que manda: NRC
menciona de paso el equivalente de la recomendación general de 1987, «mammals not
be exposed to diets containing more than 55 μg cholecalciferol·kg–1», que a 4000
kcal/kg son **14 µg/1000 kcal** — prácticamente el mismo número que FEDIAF.

### Dos techos de NRC que caben hoy y que FEDIAF no tiene tan apretados

| | NRC | FEDIAF | Nuestro máximo medido |
|---|---|---|---|
| Vitamina A, cachorro y reproductora | **3.750 µg/1000 kcal** | 30.000 | 3.236 (0 de 12 se pasan) |
| Vitamina A, adulto no reproductor | **16.000 µg/1000 kcal** | 30.000 | 5.052 (0 de 24) |
| Niacina, cachorro | **125 mg/1000 kcal** | sin máximo | 56 (0 de 12) |
| Niacina, adulto | **250 mg/1000 kcal** | sin máximo | 65 (0 de 24) |

El de vitamina A del cachorro es **ocho veces más estricto** que el de FEDIAF, y
nuestro peor menú se queda al **86 %** de él, así que aplicarlo hay que medirlo con
el solver antes, no solo contra el catálogo. El de niacina sobra por cuatro veces.
Literales: «it is suggested that an upper limit of 15,000 μg retinol·kg–1 diet of 4
kcal·g–1 be used for puppies», «For adult non-breeding dogs, it is proposed a safe
upper limit of 64,000 μg retinol·kg–1 diet», «it is suggested that diets for puppies
contain less than 0.5 g nicotinic acid·kg–1 (4 kcal·g–1). Adult dogs may tolerate
concentrations up to 1.0 g·kg–1 diet».

### Y otra vez la lista de techos que NO existen

Para el perro, NRC no puede fijar techo de: **vitamina E** («The data do not allow
for a safe upper limit of vitamin E to be defined» — o sea que el suelo de 67,1 del
libro no choca con nada por arriba), **tiamina** («There are no reports of toxicity
resulting from oral ingestion of thiamin by dogs»), **riboflavina**, **B6**,
**niacina** («The safe upper concentration of niacin in the diet of dogs has not
been defined», pese a la sugerencia práctica de arriba), **B12**, **ácido
pantoténico** («generally regarded as nontoxic»), **folato**, **biotina** y
**vitamina K** (la forma natural, la filoquinona, no ha mostrado toxicidad por
ninguna vía).

## cap.9 — Water y cap.11 — Physical Activity and Environment (LEÍDOS ENTEROS)

### ⚠️ EL HALLAZGO del cap.11: los topes de seguridad del motor NO se aprietan cuando el perro come más

NRC dedica un apartado entero a cómo cambian los requisitos con el ejercicio, y
saca dos reglas prácticas. La primera ya la aplica el motor. **La segunda no, y va
en la dirección peligrosa:**

> «In practical terms, safe upper limits (SULs) expressed relative to DM and ME
> should be decreased eightfold in diets intended for sled dogs running in a cold
> environment and halved in diets for working dogs»

**El razonamiento es aritmética pura**: un tope «por 1000 kcal» deja pasar el doble
de microgramos absolutos a un perro que come el doble. Si lo que hace daño es la
cantidad absoluta —y para la vitamina D, el yodo y el selenio lo es—, el tope por
kcal tiene que bajar en la misma proporción. NRC lo remata en la frase siguiente:
«Safe upper limits expressed relative to body weight will remain the same unless
increased exercise has been shown to modify the requirement».

**Y el motor ya tiene el disparador**: `requisitos_condicionales.json` aplica desde
el 9 de septiembre la vitamina E del perro de trabajo, y la dispara con la **DER
efectiva ≥150 kcal/kg^0,75**, que es el escalón «muy activo» de la Tabla VII-7 de
FEDIAF. La misma puerta serviría para esto, sin campo nuevo en la ficha.

**Qué cambiaría**, con los topes crónicos de `seguridad.py` a la mitad:

| Tope crónico | Hoy | A la mitad | Máximo de FEDIAF | ¿Mordería? |
|---|---|---|---|---|
| Vitamina D | 20 µg | **10** | 14,1875 | **Sí**: pasaría a ser el más estricto |
| Yodo | 1.275 µg | **637,5** | 2.750 | **Sí** |
| Selenio | 570 µg | 285 | 142 | No: el de FEDIAF ya es más estricto |

**No se aplica todavía porque falta medirlo con el solver**, no contra el catálogo:
hay que comprobar que un perro de trabajo sigue teniendo menú con la vitamina D a
10 µg/1000 kcal, y ese es el nutriente que más aprieta cuando entra un
multivitamínico. Queda anotado con la cita y la cuenta.

⚠️ Y un matiz que hay que respetar al aplicarlo: la regla de NRC habla de **SULs**,
no de los máximos de la tabla de FEDIAF. Lo que se apretaría son los topes crónicos
del motor (que salen de NRC, Merck y AAFCO), no las celdas de la Tabla III-3b. Ahí
sigue mandando FEDIAF tal cual.

### Lo que CONFIRMA: el escalado de los mínimos que el motor ya hace

> «the lower limits expressed relative to DM or ME should be increased by 1.5 times
> for diets intended for sedentary animals»

Es exactamente el mecanismo de `minimo_de()` en `verificar.py`, que sube los mínimos
cuando el perro come menos (ecuación 7.2.5 de FEDIAF). NRC llega al mismo sitio por
su cuenta, y da la magnitud: ×1,5 para el sedentario. El motor escala por el
cociente real de DER, que es más fino que un factor fijo.

### El frío, por tercera fuente y ahora con FÓRMULA

`der.py` ya tiene escrito que el frío es un hueco de verdad (FEDIAF: «may need 10 to
90 % more calories»; SACN5 Tabla 5-3, por tipo de pelo). NRC lo mide de otra forma,
y esta sí es una fórmula que se puede aplicar el día que la app pregunte la
temperatura: la temperatura crítica inferior del perro adulto está en **23-25 °C**, y
por debajo la producción de calor sube **unos 5 kcal/kg^0,75 por cada grado**, hasta
**el doble del metabolismo basal a 10 °C**. Y el otro extremo casi no cuesta: por
encima de la crítica superior (30-35 °C) el gasto sube menos de un 10 %.

Sigue sin aplicarse por lo mismo de siempre —**falta la pregunta, no la cifra**—,
pero ahora hay tres fuentes y una de ellas da una recta.

### Agua (cap.9), sin cambio

La regla práctica es **1 mL de agua por kcal de EM al día**. Una ración BARF lleva
un 70-75 % de agua, así que la cubre casi entera por sí sola, que es justo lo que
dice el aviso de estreñimiento del motor. Y el dato que explica por qué el frío no
sube la sed aunque suba las kcal: los perros de trineo en carrera a −10/−35 °C
bebieron 190 mL/kg/día con 440 kcal/kg/día, un cociente de **0,41**, y los perros
quietos del mismo sitio salieron a 0,49.

## caps. 10, 12, 13, 14 y 15 (LEÍDOS ENTEROS)

### 🔴 cap.13 — RETIRADO: la cifra que puse aquí no está en el texto

El 11 de septiembre, al montar el contador de NRC, salió esto: **el capítulo 13
del `.txt` son 177 líneas y contiene solo los TÍTULOS y las NOTAS AL PIE de sus
nueve tablas.** Donde iría el cuerpo de la Tabla 13-1 hay dos números de página
sueltos, «667 668». Esas páginas no se extrajeron.

O sea que lo que escribí aquí —que la Tabla 13-1 trae *«Meal, with bone,
rendered»* con 3,61 kcal/g para el perro, y que eso invertía la dirección del
problema del hueso— **no se puede sostener con el texto que tenemos**. Buscadas
literal en las 43.556 líneas, «Meal, with bone», «with bone, rendered» y
«5-00-388» no aparecen ninguna de las tres.

**Por qué no saltó antes.** `auditar_citas.py` solo comprueba las citas de más de
40 caracteres, y *«Meal, with bone, rendered»* tiene 26. Una cifra atribuida a una
tabla, con su número y su código de ingrediente, sin nada mirándola.

**Lo que queda en pie**, del capítulo 3 y comprobado literal: «The resulting Atwater factors of 4 for
protein, 9 for fat, and 4 kcal·g–1 for carbohydrate (nitrogen-free extract; NFE)
still work amazingly well for ingredients in homemade diets for dogs: meat, offal
(except bones and bone meal), poultry, fish, highly purified starch products, milk
products, and even chocolate».

**Y la conclusión buena:** la dirección del error del hueso sigue sin
establecerse, y no porque NRC diga algo más alto, sino porque **no podemos leer
esa tabla**. Ahora se sabe qué falta exactamente: las páginas 667-668 del PDF.

### cap.15 — Confirma la densidad de referencia con la que este repo convierte TODO

> «The energy density of the diet for both dogs and cats was assumed to be 4,000
> kcal of metabolizable energy (ME) per kg»

Es la densidad con la que el repo hace sus 110 conversiones de %MS a por 1000 kcal,
y con la que las rehace `auditar_conversiones.py`. Que sea el mismo supuesto que
usa la fuente no era obvio y ahora está comprobado.

⚠️ Y trae una tabla que **NRC dice expresamente que no se use para formular**: la
15-1, que enseña cómo cambiaría un requisito por 1000 kcal si dependiera
directamente del peso (−40 % en un perro de 2 kg, +61 % en uno de 100). Su propio
pie lo dice: «The table should not be used to formulate diets». Queda apuntado para
que nadie la aplique creyendo que es una corrección por tamaño.

Y da la **fórmula de energía de crecimiento** que es la de la Tabla 33-8 de SACN5,
la que `HALLAZGOS_SACN5_10SEP.md` midió hasta un 28 % por encima de la curva de
Klein que aplicamos: `ME = 130 × BW^0,75 × 3,2 × [e^(−0,87p) − 0,1]`, con p = peso
actual / peso adulto esperado. Ahora está la fórmula, no solo la tabla.

### cap.10 — Leído y descartado con motivo

*Special Considerations for Laboratory Animals*. Lo único con cifra es que el perro
de laboratorio gasta como un «moderadamente activo» (132 kcal/kg^0,75), y del resto
dice que no hay motivo para cambiar ningún requisito: «no special considerations for
laboratory dogs and cats for nutrients other than energy are recommended». No toca
nada de Rawku.

### cap.14 — Lo que sí toca, y es un aviso clínico

*Other Food Constituents*. La **glucosamina**, que es lo que más se recomienda para
la artrosis: «Studies have indicated that glucosamine may also induce or exacerbate
insulin resistance» y «This suggests a possible contraindication for use in dogs with»
«type II diabetes mellitus or those at risk for the disease (e.g., obese dogs)».

⚠️ Y hay que leer la frase siguiente, que matiza y que casi me dejo fuera: «However,
a recent study failed to demonstrate adverse effects of glucosamine or chondroitin
sulfate on glucose metabolism». O sea que la contraindicación está **sugerida y
discutida**, no establecida.

El motor no lleva glucosamina en el catálogo, así que hoy no aplica. Queda escrito
para el día que alguien proponga una ficha de condroprotector: sería la primera
combinación artrosis + diabetes con un aviso que apoyarse en una fuente.

Y confirma la **L-carnitina** que el motor ya aplica en la DCM: se sintetiza en el
cuerpo y no es esencial, pero «lack of adequate production by individuals of some
breeds of dogs may lead to dilated cardiomyopathy similar to» «that seen in taurine
deficiency in cats» — la frase de la fuente se parte ahí por el número de página —,
nombrando cocker americano, dóberman y bóxer.

### cap.12 — Sin nada que aplicar

*Diet Formulation and Feed Processing*: va de extrusión, enlatado y control de
calidad de pienso. Lo único transferible es la lista de pérdidas de vitaminas en
procesado, que a una ración cruda no le aplica — y esa es justamente una ventaja
suya que conviene no olvidar al comparar cifras de pienso con las nuestras.
