# Lo que aparece al leer las fuentes ENTERAS, no buscando filas de tabla

**Empezado el 8 de septiembre de 2026, por la noche.**

## Por qué existe este documento

Cris Carles señaló tres cosas por encima, en un correo que ni siquiera era la
revisión que le encargamos. De las tres, **una no la teníamos en absoluto** (el
ratio omega-6:omega-3), otra a medias y otra sin la pieza que hace falta (la
L-metionina). Y la pregunta de Elena fue la correcta:

> «Si ella nos ha dicho esas pequeñas cosas por encima, seguro que hay muchas más
> que hemos pasado por alto también. Hay que encontrar la fuente de dónde vienen
> estas cosas.»

**El fallo no fue leer poco: fue leer buscando lo que esperábamos encontrar.**
Hemos transcrito tablas fila a fila y auditado celda a celda — y esas auditorías
son buenas y siguen valiendo. Lo que no hemos leído es **el texto**: los anexos,
las notas al pie, y las frases del tipo «el requisito de X depende del contenido
de Y». Un requisito que no tiene forma de fila no lo encuentra un barrido de
filas.

Este documento recoge lo que va apareciendo al leer las fuentes **enteras**.

---

## FEDIAF 2025

### F-1 · El requisito de ARGININA sube con la proteína, y nosotros lo tenemos fijo

**Tabla VII-13**, y el texto que la acompaña:

> *«The arginine requirement **increases with increased protein content** owing to
> its role as an intermediate in the urea cycle. The NRC 2006 advises an extra
> 0.01 g arginine for every 1 % increase in protein (% DM) above the recommended
> allowance for all life stages in dogs.»*

La tabla da la arginina para cada nivel de proteína, de 18 % a 55 % de materia
seca. Nosotros tenemos **un solo número** (`minAdulto: 1.51`), que corresponde a
la fila del 25-30 % de proteína.

**Y una ración BARF de este motor sale al 38-43 % de proteína en materia seca.**
En esas filas FEDIAF pide 0,72-0,79 g/100 g MS = **1,80-1,98 g/1000 kcal**.

**MEDIDO** (adulto sano, menú real del motor):

| Peso | Proteína | % MS | Arginina que pide FEDIAF | Arginina real | |
|---|---|---|---|---|---|
| 3 kg | 96,3 g | 38,5 | 1,72 | 5,12 | cumple |
| 10 kg | 105,1 g | 42,0 | 1,85 | 3,81 | cumple |
| 22 kg | 107,4 g | 43,0 | 1,85 | 4,24 | cumple |
| 40 kg | 100,9 g | 40,4 | 1,85 | 3,97 | cumple |

**Hoy no aprieta**: la carne es rica en arginina y sobra por el doble. Pero
**sobra por suerte, no por diseño** — y en crecimiento la tabla pide más (0,94-1,02
g/100 g MS al 45 % de proteína = 2,35-2,55 g/1000 kcal, contra nuestro 2,04 fijo).
Hay que implementarlo: es un requisito de FEDIAF y lo tenemos plano.

### F-2 · La TAURINA del perro, el anexo 7.3.3, que enlaza tres cosas que teníamos sueltas

> *«Low plasma or low whole-blood taurine levels may be seen in dogs fed
> non-supplemented **very low protein diets**, or foods that are **low in
> sulphur-containing amino acids** or with poor availability of the
> sulphur-containing amino acids… Feeding certain **lamb and rice** foods may
> increase the risk… In dogs, low plasma levels of taurine (< 40 µmol/L) may also
> predispose to **dilated cardiomyopathy**… particularly **Newfoundland dogs**, in
> which the rate of taurine synthesis is decreased. The addition of taurine to such
> foods **or increasing the intake of the precursors of taurine (methionine and
> cysteine)** can prevent such a decrease.»*

Esto une, en un solo párrafo de la fuente que manda:

1. **La dieta baja en proteína** — que es exactamente lo que pide una renal, y lo
   que Cris dijo que nos faltaba.
2. **La metionina y la cistina** como precursoras — que es la L-metionina que
   Cris dice que hay que suplementar, y de la que **no tenemos ficha en el
   catálogo**.
3. **La miocardiopatía dilatada** — que ya está en la lista de patologías.
4. **Una raza concreta, el Terranova** — y la app **ya conoce la raza**: el
   Gran Danés y el Terranova tienen su propia cifra de DER desde el 8 de
   septiembre.

**Nada de esto está conectado hoy.** Un Terranova con una renal (dieta baja en
proteína) es un caso de riesgo de taurina que FEDIAF describe literalmente, y el
motor no dice ni una palabra.

### F-3 · El máximo LEGAL solo aplica si el nutriente se AÑADE como aditivo

**Sección 3.1.3**, y es un matiz que cambia el sentido de lo que aplicamos:

> *«A legal maximum only applies **when the particular trace element or vitamin is
> added to the recipe as an additive**, but relates to the "total" amount present in
> the finished product… **If the nutrient comes exclusively from feed materials, the
> legal maximum does not apply**, instead the nutritional maximum… should be taken
> into account.»*

El 6 de septiembre pusimos la vitamina D al máximo **legal** (227 UI = 14,1875
µg/1000 kcal) en vez del **nutricional** (320 UI = 20 µg), por ser más estricto.
Según esta frase, el legal solo aplica **si hay un suplemento que añada vitamina D**
— cosa que pasa en casi todos nuestros menús, porque llevan multivitamínico. Pero
en una ración de comida fresca sin suplemento de vitamina D, el que aplica es el
nutricional.

**No es peligroso**: estamos siendo más estrictos de lo que la norma exige, que es
el lado bueno. Pero el motivo escrito en el repo no es el correcto, y aprieta
menús que no haría falta apretar.

### F-4 · Los alérgenos que FEDIAF nombra, y el paso de provocación

**Sección 7.6.4**, para la patología `reaccion_adversa_alimento` que se creó hoy:

> *«**Milk, beef, eggs, cereals and dairy products** are mentioned most often whereas
> more controlled studies mentioned **wheat, soy, chicken and maize** as the most
> important allergens.»*
>
> *«Adverse reactions to food are only diagnosed through the elimination of the food
> component (eviction diet)… **Ideally this should be confirmed by a challenge
> (reintroduction of the suspected component)** after clinical signs have
> disappeared.»*

Es una segunda fuente independiente de la lista de SACN5 (que daba ternera,
lácteos y trigo) y **añade pollo, soja y maíz**. Y el paso de **provocación**, que
nuestro aviso de la fase de diagnóstico no menciona.

### F-5 · Lo que FEDIAF dice del ratio omega-6:omega-3 — y por qué el número no es suyo

> *«The effects of omega-3 fatty acids depend on the level as well as on **the ratio
> of omega-6 to omega-3 fatty acids**. Very high levels of long chain omega-3 fatty
> acids can decrease cellular immunity, particularly in the presence of a low level
> of omega-6 fatty acids.»*
>
> *«…the current information is insufficient to recommend a specific level of
> omega-3 fatty acids for adult dogs.»*

O sea: FEDIAF dice que el ratio importa **y que no pone número**. Exactamente lo
que dijo Cris. El número está en NRC 2006 — ver N-1.

---

### ⛔ F-9 · EL PEOR: habíamos BORRADO el máximo de fósforo de FEDIAF

**Esto no es un hueco: es un requisito real que quitamos, y lo quitamos por
escrito diciendo que no existía.**

El 7 de septiembre se borró el `maxAdulto = 4000` del fósforo, y se escribió en
`auditar_fediaf.py`:

> *«Ni FEDIAF (Tabla III-3a/III-3b: **solo la nota "h", informativa, sin cifra**)
> ni NRC 2006 ni Dobenecker et al. 2021 dan un maximo.»*

**La parte de NRC y Dobenecker es cierta.** Ellos hablan del **SUL
toxicológico**, que efectivamente no existe. **La de FEDIAF es falsa**, y está en
el documento **dos veces**:

1. **Tabla III-3b**, columna de máximos, junto a la nota h: **`Adult: 4.00 (N)`**.
   Y en la III-3a el mismo valor como `Adult: 1.60 (N)` g/100 g MS, que por 2,5
   son 4,00.
2. **Texto de la sección 3.3.1**, literal:
   > *«AAFCO introduced a nutritional maximum for both Ca (6.25 g/1000 kcal) and
   > **P (4 g/1000 kcal)** in 1992 out of concern for the risk of nutrient excess.
   > **FEDIAF adopted the same nutritional maximums for both Ca and P.**»*

**Son dos cosas distintas y se mezclaron**: el SUL toxicológico (no existe) y el
máximo NUTRICIONAL de FEDIAF (sí existe).

#### Por qué se coló, que es lo que hay que recordar

En el texto extraído del PDF, **la columna de máximos cae visualmente sobre la
fila ANTERIOR**. Leyendo hacia abajo se ve esto:

```
                                   Adult:        6.25 (N)
Calcium*     g  1.45  1.25  2.50   Early growth: 4.00 (N)
                                   Late growth:  4.50 (N)
                                   Adult:        4.00 (N)
Phosphorus*  g  1.16  1.00  2.25   h
```

El calcio parece tener **cuatro** máximos y el fósforo **ninguno**. El calcio
tiene tres —6,25 adulto, 4,00 crecimiento temprano, 4,50 tardío, que son
exactamente los que ya teníamos— y **el cuarto es del fósforo**. Se caza
contando los máximos de cada fila contra los que ya están en el JSON, no leyendo
hacia abajo.

#### Qué consecuencia tuvo de verdad

**Entre el 7 y el 8 de septiembre el motor no tuvo NINGÚN techo de fósforo en
adulto.** Los menús salían a ~4000 mg/1000 kcal, y el catálogo precalculado
llegó a tener uno con **4124 — por encima del máximo de FEDIAF**.

Hoy queda tapado porque el techo de SACN5 (2000) es más estricto, pero **no
siempre**: cuando el perro come poco y ese techo cede ante el mínimo escalado
(ver D-15), el de FEDIAF vuelve a ser el único que queda. Devolverlo no es
cosmético.

#### Arreglado

`maxAdulto: 4000` devuelto con la cita, `auditar_fediaf.py` corregido, y **el
auditor gana una comprobación que no tenía**: que una etapa sin máximo en FEDIAF
lleve `-` en el JSON. Antes ni la miraba — el mismo agujero por el que esto pudo
pasar un día entero. Probado con el fallo puesto.

Solo hay máximo en **adulto**: en crecimiento FEDIAF no da ninguno para el
fósforo (el `1.80` de la III-3a que parecía suyo es el «Late growth» del
**calcio**, 4,50 g/1000 kcal).

---

## NRC 2006

### N-1 · El ratio linoleico:linolénico, con número, y es un requisito CONDICIONAL

> *«This is one instance in which the ratio of LA to ALA should be considered. **A
> range for this ratio of 2.6 to 26 is presumed safe** based on evidence to date. It
> includes a margin of safety of approximately 10 percent at both extremes.»*

Y en las notas al pie de sus tres tablas de requisitos, literal:

> *«The requirement for α-linolenic acid **varies depending upon linoleic acid
> content of the diet**. The ratio of linoleic acid to α-linolenic acid should be
> between **2.6 and 26**»* (mantenimiento)
> *«…between **2.6 and 16**»* (crecimiento, y gestación/lactancia)

**El requisito de omega-3 de NRC no es un número: es un ratio contra el omega-6
que tenga la dieta.** Nosotros tratamos el linolénico como un mínimo suelto y nos
hemos comido la mitad de la frase.

**Por qué se nos pasó**: es una nota al pie, no una fila. Leímos las tablas
buscando mínimos y máximos por nutriente.

### N-2 · El ratio vitamina E : AGPI — encontrado antes, pero la medida está caducada

> *«A ratio of at least **0.6 mg of tocopherol per gram of PUFA** in the diet should
> be maintained.»* Y: *«High-PUFA diets, especially those containing **fish oils
> subject to peroxidation**, may require four or more times this level.»*

Este **sí** se había encontrado (7 de septiembre, `PENDIENTE_NUTRICION.md` §12) y
se midió: el peor ratio de ~30 menús era 1,19, por encima de 0,6, así que no
apretaba y no se implementó.

Esa medida era de ANTES de los suelos de omega-3 del 8 de septiembre, así que
**se ha vuelto a medir** con ellos puestos — subir los AGPI sin subir la vitamina
E es justo lo que esta frase avisa:

| Caso | vitE mg | AGPI g | ratio | NRC ≥ 0,6 |
|---|---|---|---|---|
| sano 22 kg | 21,3 | 10,8 | **1,98** | sí |
| sano 3 kg | 4,9 | 2,2 | 2,20 | sí |
| artrosis 22 kg | 77,5 | 15,3 | 5,08 | sí |
| cáncer 22 kg | 93,4 | 6,3 | 14,77 | sí |
| dermatitis atópica 22 kg | 102,6 | 10,9 | 9,40 | sí |
| disfunción cognitiva 22 kg | 216,5 | 8,7 | 24,91 | sí |
| cachorro 10 kg | 83,8 | 6,4 | 13,09 | sí |

**Peor ratio: 1,98, más del triple del mínimo.** Los suelos de omega-3 no lo han
roto — al contrario: las patologías que piden omega-3 piden también vitamina E, y
salen mucho mejor que el perro sano. Sigue sin apretar, y sigue sin implementarse.

⚠️ **Y la primera versión de esta medida estaba MAL, con el ratio en 0,02**: sumé
el araquidónico como si fuera gramos y va en **miligramos**. Es literalmente la
trampa que avisa `UNIDADES.md` en su línea 166. Se dice porque el número malo
llegó a escribirse antes de mirarlo dos veces.


### F-6 · La nota g: la biodisponibilidad en dietas ALTAS EN FIBRA

> *«**The bioavailability of minerals should be carefully considered in diet
> formulas where the concentration of these nutrients is close to the recommended
> amounts.** For example, in **high fiber diets** and in formulas where plant based
> raw materials rich in phytate are used as the main source of phosphorus.»*

Nos toca de lleno y no lo decimos en ningún sitio. El motor pone **suelos de
fibra** en cuatro patologías —hiperlipidemia ≥25, obesidad ≥30, intestino
irritable ≥20, estreñimiento ≥17,5 g/1000 kcal— y el solver, por definición,
resuelve **pegado al mínimo** de los minerales: es un problema de optimización que
busca el menú más pequeño que cumple.

O sea: en esas cuatro patologías estamos exactamente en el caso que la nota
describe —fibra alta **y** minerales al borde del mínimo— y no hay ni un aviso.
No es que la cifra esté mal: es que FEDIAF avisa de que en ese escenario la cifra
puede no llegar a absorberse, y eso el dueño no lo lee en ninguna parte.

### F-7 · Las notas f y h: el fósforo INORGÁNICO no es el mismo fósforo

> *(h, perros)* *«**High intake of inorganic phosphorus compounds** affects the
> calcium and phosphorus homeostasis in dogs (Siedler S 2018, Dobenecker B et al.
> 2021).»*
> *(f, gatos)* *«High intake of **highly bioavailable inorganic phosphorus
> compounds (Pi; such as sodium dihydrogen phosphate)**, ≥1.5 g/1000 kcal ME can
> affect indicators of kidney function.»*

**Esto matiza el techo de fósforo que se aplicó el mismo día.** La preocupación de
la literatura es el fósforo **inorgánico añadido** —fosfatos de aditivo, muy
biodisponibles—, no el fósforo del hueso, que va como fosfato cálcico y se absorbe
bastante peor. Una ración BARF con 4000 mg de fósforo de hueso **no es lo mismo**
que un pienso con 4000 mg de los que una parte son fosfatos añadidos.

No invalida el techo de SACN5 (2000 mg), que está puesto sobre el fósforo total y
es lo que dice su tabla. Pero es lo primero que diría un nutricionista al verlo, y
tiene que estar escrito. **Y abre una pregunta real**: ¿tiene sentido el mismo
techo para el fósforo del hueso que para el de un aditivo? La fuente distingue; el
motor no.

### F-8 · Los valores de adulto de FEDIAF ya llevan un +20 % sobre NRC

> *«Unless indicated with an * and substantiated hereafter, the values recommended
> for adult dogs are the levels recommended by NRC 2006 **increased by 20 %** to
> compensate for the lower energy requirement of household dogs.»*

No es un fallo nuestro, pero **hay que saberlo para no sumar dos veces el mismo
margen**: cuando comparemos una cifra de NRC con una de FEDIAF, la de FEDIAF ya
lleva ese 20 % dentro. Y explica por qué la arginina de FEDIAF (0,60 g/100 g MS)
es más alta que la que sale de la Tabla VII-13 para el 21 % de proteína (~0,55).


---

## Más de FEDIAF, sección 3.3 (la que explica cada nutriente con asterisco)

### F-10 · La METIONINA+CISTINA que pide FEDIAF supone un alimento BAJO en taurina

> *«The recommended values are based on a dog food containing a **very low taurine
> content, i.e. <100 mg/kg dry matter**. For products containing higher levels of
> taurine **the RA for sulphur amino acids can be lower** than the values quoted in
> the table.»*

O sea que el mínimo de metionina+cistina que aplicamos está calculado para un
alimento casi sin taurina — y una ración BARF de carne lleva taurina de verdad
(el catálogo tiene el dato desde el 7 de septiembre). No es un peligro: es que
estamos siendo **más estrictos de lo necesario**, sin saberlo.

### F-11 · La METIONINA hay que SUBIRLA en dietas de cordero

> *«**In the case of lamb and rice foods, the methionine level may have to be
> increased.** For further information see taurine section ANNEX 7.3.»*

El catálogo tiene cordero. Un menú de cordero debería llevar más metionina, y el
motor no lo sabe. Es la misma frase del anexo 7.3.3 vista desde el otro lado.

### F-12 · Por debajo del mínimo de proteína, el perfil de aminoácidos es LO que importa

> *«**If formulating below the recommended minimum for total protein it is
> particularly important to ensure that the amino acid profile meets FEDIAF
> guidelines** for adult maintenance.»*

Es exactamente el caso que describió Cris (la renal IRIS 4) y la regla que tiene
que gobernar el modo veterinario: bajar la proteína **no** autoriza a bajar los
aminoácidos. Hoy no formulamos por debajo del mínimo, así que no hace daño — pero
es la regla que hay que tener escrita antes de construir esa parte.

### ⚠️ F-13 · La proteína de GESTACIÓN y LACTANCIA supone que hay HIDRATOS

> *«The recommendation for protein assumes the diet contains **some
> carbohydrate** to decrease the risk of hypoglycaemia in the bitch and neonatal
> mortality. **If carbohydrate is absent or at a very low level, the protein
> requirement is much higher, and may be double**.»*

**Una ración BARF es prácticamente sin hidratos.** Carne, hueso, víscera y un
10 % de verdura. Según esta frase, en gestación y lactancia el requisito de
proteína **puede ser el doble** del que aplicamos (62,5 g/1000 kcal → 125).

**MEDIDO** en menús reales del motor:

| Etapa | Proteína | % MS |
|---|---|---|
| Gestante 22 kg | **123,9 g** | 49,6 |
| Lactante 22 kg | **124,2 g** | 49,7 |
| Gestante tardía 22 kg | 119,2 g | 47,7 |
| Adulto 22 kg (referencia) | 101,7 g | 40,7 |

**Cumplimos, y por los pelos: 123,9 contra 125.** Pero **cumplimos por
casualidad, no por regla**: un menú de gestación que saliera con 70 g de proteína
pasaría nuestro semáforo (mínimo 62,5) y estaría a la mitad de lo que FEDIAF dice
que hace falta sin hidratos. Y es el caso donde equivocarse cuesta más caro:
hipoglucemia de la madre y mortalidad neonatal.

**Era la más urgente de todo este documento. ✅ APLICADA la misma noche.**

#### Y NRC trae el experimento, con las cifras

Buscando de dónde sale la frase de FEDIAF apareció el estudio, en NRC 2006
cap. 5, «Effects on Reproductive Performance»:

> *«Kienzle et al. (1985) fed carbohydrate-free diets with different
> concentrations of protein to pregnant and lactating bitches. In bitches fed the
> **high-protein, carbohydrate-free diet (42 percent of calories from protein)**,
> litter size, birth weight, and puppy survival rate were **comparable** to those
> when bitches were fed a carbohydrate-containing control diet. In contrast, in
> bitches fed the **low-protein, carbohydrate-free diet (20 percent of calories
> from protein)**, a reduction in **birth weight (30 to 40 percent)** and an
> increase in **perinatal mortality rate (75 percent)** were observed.»*

**No es una recomendación teórica: es mortalidad neonatal medida.**

#### Qué se ha aplicado

**Suelo de proteína de 125 g/1000 kcal** en gestante, gestante tardía y
lactante. Vive en `requisitos_condicionales.json` con
`motor/condicionales.py` de cargador, y lo vigila el **BLOQUE 58**.

El número es la lectura **más estricta** de las dos que dan las fuentes: el
«doble» de FEDIAF sobre el mínimo de reproducción (62,5) son 125; los «42 % de
las kcal» de Kienzle son 105 g a 4 kcal/g o 120 a 3,5, los dos por debajo.

**MEDIDO antes de aplicarlo**, los nueve casos (5, 22 y 40 kg × las tres
etapas): **los nueve en el peldaño 0 y en verde**, con la proteína real entre
125,1 y 152,6. **No cuesta ni un peldaño.**

### F-14 · Calcio alto → hay que SUBIR el zinc y el cobre

> *«**As the calcium level approaches the stated nutritional maximum, it may be
> necessary to increase the levels of certain trace elements such as zinc and
> copper.**»*
>
> *(General, oligoelementos)* *«the bioavailability of trace elements is reduced by
> a high content of certain minerals (e.g. calcium), the level of other trace
> elements (e.g. **high zinc decreases copper absorption**) and sources of phytic
> acid.»*

**Segunda fuente independiente**: SACN5 Tabla 32-1 ya decía *«higher levels of
zinc are required in foods with calcium >1.5 % DM»*, y quedó apuntado sin aplicar
en `VERIFICACION_FILA_A_FILA.md`. Ahora lo dice también FEDIAF. **Y una ración
BARF es de hueso: el calcio va alto por construcción.**

### F-15 · Fuentes de mineral que NO cuentan para el mínimo

> *«Owing to its low availability **copper oxide should not be considered a copper
> source**.»*
> *«Because of very poor availability, **iron from oxide or carbonate salts** that
> are added to the diet **should not be considered sources contributing to the
> minimum nutrient level**.»*

Hay que mirar si algún suplemento del catálogo declara cobre como óxido o hierro
como óxido/carbonato: si lo hace, ese aporte **no cuenta** para el mínimo y el
motor lo está contando.

### F-16 · El zinc: doblar el mínimo «puede considerarse seguro»

> *«Considering potential factors present in practical pet foods that could
> decrease zinc availability, **doubling the minimum recommended level may be
> considered safe**.»*

No es una obligación, pero es la respuesta de FEDIAF al problema del calcio alto
del F-14, y encaja con la dermatosis zinc-sensible que ya tenemos.


---

## Resto de FEDIAF (leído el 8 de septiembre por la noche)

### F-17 · La vitamina E depende de los AGPI — y lo dice FEDIAF, no solo NRC

> *«**Vitamin E requirements depend on the intake of polyunsaturated fatty acids
> (PUFA)** and the presence of other antioxidants. An increased level of vitamin E
> may be required **if the intake of PUFA is high, particularly from fish oil**.»*

**Segunda fuente independiente** de lo mismo que dice NRC con su 0,6 mg de
tocoferol por gramo de AGPI (N-2). Y nombra el aceite de pescado, que es
exactamente lo que suben nuestros suelos de omega-3. Medido y por ahora cumple
(peor ratio 1,98), pero ya no es «una frase suelta de NRC»: lo piden las dos.

### F-18 · El máximo de vitamina D distingue el tamaño de la raza

> *«320 IU per 100 g DM should be the nutritional maximum for **growing giant
> breed** dogs… 425 IU/100 g DM can be considered a safe nutritional maximum for
> **small breed** puppies. Since there is no information on maximum safe intakes
> for adult dogs and breeding bitches, FEDIAF recommends the same nutritional
> maximum for other life stages as those indicated for puppies.»*

No nos afecta hoy porque aplicamos el máximo **legal** (227 UI), más estricto que
los dos. Pero conviene saber que el nutricional distingue raza gigante de raza
pequeña, y que el de adulto es prestado del de cachorro por falta de datos.

### F-19 · La biotina y la vitamina K NO tienen mínimo, y por qué

> *«For healthy dogs **biotin does not need to be added** to the food **unless the
> food contains antimicrobial or anti-vitamin compounds**.»* Y lo mismo para la
> vitamina K.

En la Tabla III-3b las dos llevan «-» en todas las columnas, así que **que no
estén en el `MAPA` es correcto**, no un olvido. Comprobado.

Y la excepción que nombra —«anti-vitamin compounds»— es la **avidina de la clara
de huevo cruda**, que es un caso muy nuestro: **ya está cubierto**
(`seguridad.py`, tope del 5 % del peso para la clara cruda, con el daño medido al
20 % citado en `PARA_EL_NUTRICIONISTA.md`).

### F-20 · Comprobado: no falta ninguna FILA de la tabla de FEDIAF

Contadas una contra otra: **42 filas con valor en la Tabla III-3b y 42 en nuestro
JSON.** Las otras 6 de nuestro fichero son añadidos documentados y con «-» en
todas las columnas (fibra, taurina, L-carnitina, EPA, omega-3 total y el calcio
de raza grande). **Ninguna fila de FEDIAF se ha quedado fuera.**

Importaba comprobarlo porque una fila que falta entera **es invisible** para un
auditor que recorre nuestras propias filas.

### F-21 · La ecuación de escalado es literalmente la nuestra

> *«Units/1000 kcal = Nutrient requirement per day (Units/kg metabolic BW) × 1000
> ÷ DER (kcal/kg metabolic BW)»* (§7.2.5)

Es exactamente lo que hace `minimo_de()`. ✓ Y el texto añade el porqué: *«the
energy needs may be satisfied before the requirements of protein, minerals or
vitamins are met»*.

### F-22 · Los cambios de 2025 y de 2024 son cosméticos

Sección 8, leída: lo de 2025 vs 2024 son encabezados de tabla y símbolos
matemáticos. Lo de 2024 vs 2021 añade *«Table VII-8b: Added n-4 to equation»* y
actualiza la nota (f). **No arrastramos nada de una edición vieja.**

### Lo que queda de FEDIAF sin leer, y por qué no corre prisa

§7.1 (condición corporal), §7.7 (riesgos de alimentos humanos — comprobado que
**ninguno** de los que nombra está en nuestro catálogo), §4 (alimento
complementario), §5 y §6 (métodos analíticos y protocolos de prueba de
digestibilidad). Ninguna contiene requisitos de nutrientes.


---

## Lo que salió de leer NRC sobre aminoácidos, y una afirmación nuestra que ya no es cierta

### N-3 · El antagonismo lisina-arginina: el techo de lisina no es toxicidad, es antagonismo

NRC 2006, capítulo de aminoácidos, «Amino Acid Imbalances and Antagonisms»:

> *«**A lysine-arginine antagonism has been reported in growing dogs by Czarnecki
> et al. (1985)** (i.e., 40 g lysine·kg⁻¹ added to a basal diet somewhat limiting
> in arginine caused a decrease in weight gain **that was largely corrected by the
> addition of 4 g arginine·kg⁻¹ diet**).»*

Y en la misma página, otros dos que también nos tocan:

> *«…when 4 g lysine·kg⁻¹ was added to a low-protein basal diet, apparently
> limiting in sulfur amino acids, **weight gain was depressed 28 percent and was
> restored by the further addition of 3 g DL-methionine**.»*
> *«…in puppies the addition of 2.2 g cystine·kg⁻¹ to a diet severely limiting in
> methionine caused a decrease in weight gain and **necrotic skin lesions on the
> pads of the front feet**, which were corrected rapidly when methionine was
> added.»*

**Czarnecki et al. 1985 es EL MISMO estudio que FEDIAF cita para el máximo de
lisina** (*«excess dietary lysine (4.91 % DM) decreases weight gain in puppies but
not 2.91 % DM»*). O sea que **el techo de lisina no es un límite de toxicidad: es
un límite de antagonismo, y solo muerde cuando la arginina va justa.** Eso no
estaba escrito en ningún sitio nuestro, y cambia cómo hay que leer la excepción.

### ⛔ N-4 · La justificación escrita de la excepción de la lisina ya no es cierta

`CLAUDE.md` dice, y lo repite `PARA_EL_NUTRICIONISTA.md`:

> *«el techo de lisina (7,00 g/1000 kcal, solo en crecimiento) no se aplica —
> **0 de 15 menús de cachorro caben debajo**»*

**MEDIDO hoy, 15 menús de cachorro (7 de CachorroJoven y 8 de
CachorroCrecimiento, de 2 a 60 kg): 13 de 15 caben debajo.** Solo dos se pasan
(8,61 y 8,02), y la cifra **baila mucho entre sorteos** — el mismo perro da 5,12
en un intento y 10,23 en otro, porque depende de qué alimentos salgan.

**La excepción sigue estando bien puesta** (hay menús que se pasan, y aplicar el
techo dejaría a esos sin menú). **Lo que ya no vale es el motivo escrito.**

### ⛔ N-5 · Y no podemos afirmar ninguna de las dos cosas, porque no vemos la lisina

En los menús de cachorro, **entre el 17 y el 41 % de la proteína del plato viene
de alimentos sin dato de lisina**. Y el culpable es casi siempre **uno solo**:
`V-INTEGRA Cachorro`, un suplemento que declara proteína y no trae aminograma.
(De las 66 fichas sin lisina, **ninguna es carne, hueso, víscera, hígado ni
pescado**: son 34 verduras, 10 extras y 22 suplementos.)

Contar un hueco como 0 es el **lado seguro para un mínimo** —se exige de más— pero
es el **lado malo para un techo**: el menú parece cumplir porque no hemos mirado.
Así que el «13 de 15 caben» de arriba es, él mismo, poco de fiar.

**Y el BLOQUE 27 no lo caza**, porque su guardia de «la proteína sin aminograma no
pasa del 5 %» se mide sobre **un único menú de ADULTO de 25 kg**. Nunca ha mirado
un cachorro — que es justo donde el hueco es del 17-41 % y donde los aminoácidos
más aprietan.

**El arreglo es un DATO, no código**: el aminograma de `V-INTEGRA Cachorro` (y
probablemente el de las otras cuatro variantes de V-INTEGRA). Va a
`DATOS_QUE_FALTAN.md`. Y el BLOQUE 27 tiene que medir su guardia también en
crecimiento.


---

# ⛔ AVISO SOBRE LAS MEDIDAS DE ESTE DOCUMENTO (8 de septiembre, noche)

**Varias de las medidas de arriba están hechas sobre menús que la app nunca
produciría, y hay que rehacerlas.**

## El fallo

`motor_completo.resolver()` aplica las proporciones de BARF **solo si se las
pasas**:

```python
if margenes_categoria:        # línea 1501
```

Sin ese argumento **no hay ni suelo ni techo de categoría**, y el solver es libre
de montar cualquier cosa que cumpla los números. Lo que monta, medido:

```
CachorroCrecimiento 22 kg:  Dorada 503 g · ALCACHOFA 2.566 g · Carcasa 165 g
CachorroJoven 10 kg:        Pollo 259 g · RÚCULA 1.089 g
```

**2,5 kg de alcachofa al día**, el 79 % del plato en verdura, con el tope real en
el 10 %. Eso no es un menú: es una solución matemática del problema sin la forma
de una ración.

## Qué medidas se salvan y cuáles no

**Se salvan** — usaron `_escalera_de_relajacion()`, que sí pasa las proporciones,
y son justo las que han decidido algo:

| Medida | Dónde |
|---|---|
| El techo de fósforo cabe en el peldaño 0 (3, 10, 22, 40 kg) | D-15 |
| La proteína de reproducción a 125 cabe en los nueve casos | F-13 |
| El omega-3 del cáncer: 11,5 sí, 12,0 no | 30-5 |
| El toy de 1,5 kg: 12 sorteos sin menú de 30 | §14.4 |

**No valen, y hay que rehacerlas:**

- La arginina de los menús reales (decía 3,8-5,1 contra un requisito de 1,85) → **F-1**
- El ratio vitamina E : AGPI (decía 1,98 en el peor caso) → **N-2**
- La lisina de los cachorros (decía 13 de 15 bajo el techo) → **N-4**
- La proteína de gestación y lactancia de la PRIMERA medida (123,9 y 124,2) →
  **F-13**. La segunda, la que decidió el número, sí es buena.

## Lo que hay que aprender

Es el mismo error que el del barrido cortado y el del araquidónico en gramos:
**una medida mal hecha da un número, y un número parece un hecho.** Las tres veces
lo que faltó fue comprobar que la herramienta estaba midiendo lo que yo creía.

A partir de aquí, **ninguna medida de este documento vale sin decir con qué
proporciones se hizo**.


---

## NRC 2006, minerales: lo que dice del fitato y por qué nos toca poco

### N-6 · El problema del fitato con el zinc es de dietas VEGETALES, y una ración BARF no lo es

> *«**Most animal products and seafood are relatively free of constituents that
> interfere with Zn absorption**, and, as mentioned previously, **amino acids
> derived from meat digestion may actually improve the absorption of Zn**.
> Vegetable products are more likely to contain chemicals that interfere with Zn
> absorption, the most notable of these being **phytate**; phytate is present in
> many plant sources including cereals such as corn, wheat, and rice and oilseed
> meals such as **soy, peanut, and sesame**, which may contain 1.5 percent or more
> phytate. Dietary phytate has long been known to reduce the absorption of Zn, and
> **this effect is exacerbated by high concentrations of dietary Ca**.»*

Es la contrapartida buena de F-14 y F-16: FEDIAF avisa de que con el calcio alto
hay que subir el zinc, y NRC explica **por qué** —el fitato— y añade que **en una
dieta de carne ese mecanismo apenas existe**. Una ración BARF es carne, hueso y
víscera; no lleva cereal ni harina de oleaginosa.

**Comprobado en el catálogo**, porque la fuente nombra el sésamo: los **aceites**
de sésamo, girasol, cacahuete y linaza traen **cero calcio y cero zinc** —el
fitato se queda en la torta, no pasa al aceite—. Las que sí podrían aportarlo son
las tres **semillas** (sésamo 975 mg de calcio y 7,75 de zinc, lino, pipa de
girasol), y van como «Extras» en cantidades pequeñas.

**Conclusión: no es una alarma, es un matiz que había que comprobar en vez de
suponer.** Queda escrito para que la próxima vez que alguien lea F-14 no se
asuste de más.

### N-7 · Otras dos que conviene tener anotadas

> *«Ca availability **decreases during the growth period and also with increasing
> dietary Ca concentration**»* — o sea que el calcio alto se absorbe peor, lo que
> juega a favor del margen que ya tenemos.
> *«…with **high dietary Ca significantly reducing absorption of P**»* — el calcio
> alto baja la absorción del fósforo, que es otro matiz a favor en la discusión
> del techo de fósforo (F-7).

---

## NRC 2006, capítulo 4 (hidratos y fibra) y capítulo 5 (grasa y ácidos grasos)

Leídos enteros la noche del 8 al 9 de septiembre. El capítulo 4 es casi todo
pienso extrusionado y sirve de poco a una ración cruda; el capítulo 5 es **lo
más importante que ha salido en toda la lectura**, porque es justo lo que la
nutricionista señaló por encima —«falta el lipidograma, falta el ratio
omega-6:omega-3»— y aquí está la fuente, con cifras.

### N-8 · La proteína de la reproducción sin hidratos: la fuente exacta

Ya estaba aplicada (`requisitos_condicionales.json`), pero conviene dejar
escrito de dónde sale el número, porque el capítulo 4 lo trae con las dos
mitades del experimento:

> *«Kienzle et al. (1985) fed carbohydrate-free diets with different
> concentrations of protein to pregnant and lactating bitches. In bitches fed
> the **high-protein, carbohydrate-free diet (42 percent of calories from
> protein)**, litter size, birth weight, and puppy survival rate were comparable
> to those when bitches were fed a carbohydrate-containing control diet. In
> contrast, in bitches fed the **low-protein, carbohydrate-free diet (20 percent
> of calories from protein)**, a reduction in birth weight (30 to 40 percent) and
> an **increase in perinatal mortality rate (75 percent)** were observed.»*

Y Romsos 1981, con el 26 % de las calorías en proteína y sin hidratos: 63 % de
cachorros vivos al nacer contra el 96 % del control, y **35 % vivos a los tres
días contra el 93 %**. Las bitches sin hidratos entraron en cetosis con glucemias
de 15-20 mg/dL la semana antes del parto.

O sea que el umbral está **entre el 26 % y el 42 % de las calorías**. Nuestro
suelo de 125 g/1000 kcal es el **43,75 %** de las kcal (a 3,5 kcal/g, el Atwater
modificado del pienso) o el 50 % (a 4 kcal/g): por encima del 42 % que sí
funcionó. Está del lado seguro y ahora se sabe por qué.

### N-9 · «El ratio omega-6:omega-3» que pide la nutricionista: el NRC dice que ESE ratio no sirve, y da otro

Esto hay que leerlo entero antes de aplicar nada, porque es una trampa:

> *«The European expert committee also specifically concluded that **the use of a
> total n-6:n-3 ratio is not helpful** (de Deckere et al., 1998). The British
> Nutrition Foundation Task Force on Fatty Acids (BNF) has stated that attempts
> to explain data based on the total n-6:n-3 ratio **may be distorted**.»*

El motivo está escrito justo antes: unos estudios calculan el ratio sumando
**todos** los omega-6 y **todos** los omega-3 (derivados de cadena larga
incluidos) y otros solo los de 18 carbonos (LA y ALA), y **no son
equivalentes**, porque «the long-chain metabolites are known to be more potent as
substrates for eicosanoid production than their parent fatty acids».

Lo que el NRC sí recomienda es el ratio **LA:ALA** —linoleico partido por
linolénico, los dos de 18 carbonos—, y da rangos por etapa:

| Etapa | Rango LA:ALA | Cita |
|---|---|---|
| Adulto mantenimiento | **2,6 – 26** | *«A range for this ratio of 2.6 to 26 is presumed safe based on evidence to date. It includes a margin of safety of approximately 10 percent at both extremes.»* |
| Gestación y lactancia | **2,6 – 16** | *«Because of competition between LA and ALA for metabolism, the LA:ALA ratio should range between 2.6 and 16. This range is not as wide as that for maintenance, thereby helping ensure the availability of 18-carbon n-3 ALA for subsequent elongation.»* |
| Crecimiento | **≈ 16,3**, «less than 17» | *«the RAs are 1.3 percent DM for LA and 0.08 percent DM for ALA with an LA:ALA ratio of 16.3»* |

Y el porqué del suelo de 2,6 y del techo de 26 es metabólico, no arbitrario:
*«high cellular LA will affect ALA conversion to a greater extent than high ALA
at lower LA content»*. El linoleico y el linolénico compiten por la misma
Δ6-desaturasa.

**Esto no está aplicado.** El motor exige el mínimo de linoleico (3,82 g/1000
kcal en adulto, FEDIAF) y el de linolénico solo en crecimiento (0,20 g), pero
**no mira la relación entre los dos en ninguna etapa**. Es exactamente la clase
de cosa que sale verde y está mal.

### N-10 · Tres techos del NRC para el perro adulto que no tenemos

FEDIAF deja las tres columnas de máximo vacías. El NRC no.

| Qué | Cifra | De dónde sale |
|---|---|---|
| **Grasa total, SUL** | **82,5 g/1000 kcal** (≈70 % ME) | *«Another study, noted earlier, **induced pancreatitis** in dogs using approximately 92 g per 1,000 kcal ME (Lindsay et al., 1948). Thus, the SUL for total fat is based on a safety margin of about 10 percent less than the amount reported to have induced pancreatitis»*. Y a ~95 g/1000 kcal se indujo **hipertensión y obesidad** (Rochhini 1987). |
| **Linoleico, SUL** | **16,3 g/1000 kcal** (13,8 % ME) | *«the SUL for LA is estimated at 16.3 g per 1,000 kcal (13.8 percent ME) … Amounts of LA in excess of this amount are not recommended for long-term feeding.»* |
| **Omega-3 de cadena larga (EPA+DPA+DHA), SUL** | **2,8 g/1000 kcal** (2,4 % ME) | Inmunidad celular deprimida a 3,13 % ME durante 12 semanas (Wander 1997), menos un 10 % de margen. |

Dos cosas que merecen subrayarse:

1. El **16,3 del NRC para adulto** y el **16,25 de FEDIAF para crecimiento
   temprano** son, a efectos prácticos, el mismo número desde dos sitios
   distintos. Que dos fuentes independientes caigan en el mismo sitio es la
   mejor señal que se puede pedir de que el techo es real.
2. El **2,8 de omega-3 de cadena larga ya lo tenemos**, y en el sitio correcto:
   en el promedio semanal de `/menu/semana`, no plato a plato. La nota de
   auditoría de `EPA_DHA_total` en `requerimientos_v2_final.json` ya explica por
   qué (18 de los 20 pescados del catálogo pasan de 2.800 ellos solos). Nada que
   cambiar ahí — pero conviene saber que el NRC lo llama SUL de **la suma de los
   tres**, DPA incluido, y nosotros sumamos solo EPA+DHA. Va del lado seguro,
   porque sumar menos con el mismo techo aprieta menos; queda apuntado.

### N-11 · Lo poco que el capítulo 4 le dice a una ración cruda

- **Lactosa**: *«Adult dogs … tolerate lactose at approximately 3 g·kg BW⁻¹·d⁻¹»*
  y Burger 1993, *«dogs tolerate lactose at concentrations of 5 percent or less
  of total energy»*. El único lácteo del catálogo es el **yogur griego**, con
  ~3,5 g de lactosa por 100 g. **Medido: sale en 0 de los 216 menús
  precalculados.** Para llegar al 5 % de la energía haría falta que el yogur
  fuera casi la mitad de las calorías del menú. No es un riesgo, pero queda la
  cifra escrita por si algún día entra otro lácteo.
- **La fibra baja la absorción del hierro**: *«iron + pectin reduced (P < 0.05)
  iron uptake (28.5 μg·h⁻¹) as compared to iron alone (71.9 μg·h⁻¹)»*. Es la
  misma advertencia de la nota g de FEDIAF, con el número. Nos toca porque
  tenemos **suelos de fibra en cuatro patologías** (hiperlipidemia ≥25,
  obesidad ≥30, intestino irritable ≥20, estreñimiento ≥17,5): en esos cuatro
  casos el hierro del menú se absorbe peor de lo que dice la ficha. No hay cifra
  que aplicar —el efecto depende del tipo de fibra—, pero es una pregunta
  legítima para el nutricionista.
- **Fibra insoluble en gestación tardía y lactancia: evitarla.** *«supplementing
  a bitch's diet with insoluble fiber during the latter phases of pregnancy and
  during lactation should be avoided since it will decrease the energy density
  of the diet»*. No tenemos ningún suelo de fibra en esas etapas, así que no
  chocamos con ello; pero si alguna vez se añade uno, esto lo prohíbe.

---

## NRC 2006, capítulo 6 (proteína y aminoácidos)

Leído entero. Es el capítulo que contesta a **dos** cosas: la pregunta que
llevamos abierta desde el 28 de agosto sobre el techo de lisina, y la petición
de la nutricionista sobre la metionina.

### N-12 · La arginina tiene que subir con la proteína, y ahora hay fórmula

> *«Since both of the above groups have shown that increasing dietary nitrogen
> increases the severity of clinical signs when a low-arginine or arginine-free
> diet is fed, **it is recommended that 0.01 g arginine be added for each gram of
> crude protein above the requirement**.»* (perro, crecimiento)

Y el mismo mecanismo, medido en el gato con una regresión (r² = 0,99):
`arginina g/kg = 0,02 × proteína g/kg + 4,0`. En el perro el coeficiente es la
mitad, 0,01.

**Lo que significa para una ración BARF, con números.** El requisito de proteína
del NRC para un cachorro de 4-14 semanas es 180 g/kg de dieta a 4 kcal/g, o sea
**45 g/1000 kcal**. Un menú BARF de cachorro lleva **~134 g/1000 kcal** (medido,
ver §aminoácidos de `HISTORIA_TECNICA.md`). El exceso son ~89 g/1000 kcal, que a
0,01 g de arginina por gramo pide **+0,89 g de arginina/1000 kcal** sobre el
mínimo. El mínimo del NRC en esa etapa es 1,575 g/1000 kcal (6,3 g/kg ÷ 4), así
que el requisito real de ese menú sería **≈ 2,47 g/1000 kcal**, no 1,575.

Esto **no está aplicado**, y es el mismo patrón que la proteína de gestación sin
hidratos: un requisito que depende de otro nutriente del mismo menú, no una cifra
fija de tabla. Va en `requisitos_condicionales.json`.

### N-13 · El techo de lisina: por fin el mecanismo, y por fin un número

Llevamos desde el 28 de agosto con el techo de lisina de FEDIAF (7,00 g/1000 kcal
en crecimiento) **no aplicado**, en `verificar.MAXIMOS_NO_APLICADOS`, con la
pregunta abierta para el nutricionista y sin saber por qué existe ese techo. El
NRC lo explica:

> *«A **lysine-arginine antagonism** was reported by Czarnecki et al. (1985) in
> growing English pointer puppies. They found that, although 10 or 20 g of extra
> free lysine per kilogram of diet had no effect, **40 g excess lysine** in the
> diet caused a growth depression and classical clinical signs of **arginine
> deficiency** (emesis, increased plasma ammonia, and orotic aciduria) **when the
> diet contained 4 g arginine·kg⁻¹**. **An additional 4 g arginine prevented the
> clinical signs** and improved weight gain. … The SUL for lysine is **>20 and
> <40 g·kg⁻¹ diet** containing 4.0 kcal ME·g⁻¹.»*

Tres cosas que cambian la conversación:

1. **El SUL del NRC en nuestras unidades es «más de 5 y menos de 10 g/1000
   kcal»** (÷4). El techo de FEDIAF, 7,00, cae **justo en medio de esa horquilla**.
   O sea que el 7,00 no es un número inventado: es el punto medio del único
   experimento que existe.
2. **El daño no es de la lisina: es de la arginina que se queda corta.** Lo que
   enfermó a los cachorros fue una deficiencia de arginina inducida, con 4 g de
   arginina por kilo de dieta —**1 g/1000 kcal**, que está *por debajo* del
   mínimo de FEDIAF en adulto (1,51)—. Con arginina suficiente, los signos no
   aparecieron.
3. Por eso N-12 y N-13 **son el mismo hallazgo visto por los dos lados**: el
   techo de lisina y el suelo de arginina que sube con la proteína son la misma
   restricción. Si la arginina acompaña, la lisina alta no es el problema.

**Falta medir** —y es lo primero que hay que hacer con el motor libre— el
cociente lisina:arginina de los menús de cachorro reales, con
`margenes_categoria=MARGENES_V2` (ver el aviso de más arriba sobre las medidas
sin proporciones). El caso que enfermó a los perros de Czarnecki iba a ~11,8:1
de lisina a arginina; la carne ronda 1,4:1. Si la medida confirma esa distancia,
la excepción del techo de lisina deja de ser una decisión pendiente y pasa a ser
una decisión **justificada**, y la pregunta al nutricionista cambia de «¿lo
aplicamos?» a «¿confirmas que con este cociente no hay antagonismo?».

### N-14 · Los otros tres antagonismos de aminoácidos del perro, y por qué no nos tocan

El NRC cierra el capítulo con esto, y merece leerse entero porque es
tranquilizador **por el motivo correcto**:

> *«…in general, **dogs appear to be more sensitive to disproportionalities among
> dietary amino acids than cats, especially when fed low-protein diets**.»*

Los cuatro antagonismos documentados en el perro son todos **sobre dietas bajas
en proteína o limitantes en el aminoácido contrario**:

| Antagonismo | Qué pasó | Con qué se corrigió |
|---|---|---|
| Lisina → arginina | +40 g lisina/kg con 4 g arginina/kg: emesis, hiperamoniemia, aciduria orótica | +4 g arginina/kg |
| Lisina → metionina | +4 g lisina/kg en dieta baja en azufrados: −28 % de crecimiento | +3 g DL-metionina/kg |
| Metionina → lisina | +1,5 g metionina/kg en dieta limitante en lisina: −37 % de crecimiento | +1,3 g lisina/kg |
| Cistina → metionina | +2,2 g cistina/kg con metionina a 1,1 g/kg: lesiones necróticas en almohadillas | más metionina |

Una ración BARF **no está en ninguna de esas condiciones**: es carne, hueso y
víscera, con la proteína dos y tres veces por encima del requisito y con los
aminoácidos en la proporción del músculo. La lección no es «no pasa nada», es
que **el riesgo de los aminoácidos en el perro vive en las dietas pobres, no en
las ricas** — y eso es exactamente lo contrario de lo que uno supondría al ver
un techo en una tabla.

### N-15 · La metionina: la nutricionista tenía razón, y hay una advertencia que no teníamos

Cris Carles nombró la **L-metionina** en el contexto renal. El NRC trae dos cosas
sobre metionina en el perro que no estaban en el repo:

**Primera, la buena, y sostiene lo que ella dijo:**

> *«Over a period of two decades (Stekol, 1935; Miller, 1944; Allison, 1947,
> 1956), it was shown in both growing and adult dogs that **methionine (either the
> L- or the DL-form) had a unique effect in reducing nitrogen loss and maintaining
> serum albumin when dogs were fed a low-protein or a protein-free diet**.»*

Es justo el escenario de un renal restringido: proteína baja, y la metionina
protege la albúmina y reduce la pérdida de nitrógeno. Y en el perro, además:
*«Daily supplements of methionine, without changing the diet, results in an
increase in plasma taurine concentration»* — o sea que también cubre el riesgo de
taurina de una dieta baja en proteína, que es como salió la miocardiopatía
dilatada de los Newfoundland.

**Segunda, la que nos faltaba, y es una advertencia de seguridad:**

> *«Oral administration of about 1 g methionine·kg BW⁻¹ every 4 hours for 24
> hours caused **no acute clinical signs in normal dogs** but caused **severe
> clinical signs similar to hepatic coma in dogs with portacaval shunts**
> (Merino et al., 1975).»*

Y un caso real de intoxicación por error de formulación: seis perros de caza con
una sola comida de ~300 g de un pienso con 47 g de DL-metionina/kg — ataxia,
desorientación, temblores, vómitos, y el más joven con convulsiones. *«the SUL
for DL-methionine is well below 47 g·kg⁻¹ diet»* (= muy por debajo de 11,75
g/1000 kcal).

**Lo que esto abre, y no lo decido yo**: hoy `patologias.json` no tiene ningún
tope de metionina en **hepatopatía**, y el NRC dice que en un perro con shunt
portosistémico la metionina que un perro sano tolera sin inmutarse provoca
signos de coma hepático. No lo aplico porque la cifra del NRC es una **dosis por
kilo de peso administrada cada 4 horas**, no una concentración de dieta, y
convertir una cosa en la otra sería inventarme el número — que es exactamente lo
que `CERRADO.md` prohíbe. Va a `PREGUNTAS_PARA_ELENA.md` para el nutricionista.

### N-16 · Requisitos del NRC para el perro adulto, para tener con qué comparar

Ninguno se aplica (manda FEDIAF), pero conviene tenerlos escritos porque son la
segunda fuente:

| | NRC (MR adulto, ÷4 desde g/kg a 4 kcal/g) | FEDIAF (mínimo adulto) |
|---|---|---|
| Proteína bruta | 80 g/kg = **20 g/1000 kcal** (RA 100 g/kg = 25) | 52,1 g/1000 kcal |
| Azufrados totales (met+cis) | 5,2 g/kg = **1,30 g/1000 kcal** | 1,63 g/1000 kcal |
| Metionina | 2,6 g/kg = **0,65 g/1000 kcal** | 0,82 g/1000 kcal |
| Arginina | 2,8 g/kg = **0,70 g/1000 kcal** | 1,51 g/1000 kcal |

FEDIAF es más exigente en las cuatro. No hay ninguna fila donde el NRC pida más
que FEDIAF en el adulto sano, así que **el semáforo no se queda corto por este
lado**. Eso era lo que había que comprobar.

---

## NRC 2006, capítulo 7 (minerales)

### ⚠️ N-17 · EL PEOR HALLAZGO DE LA NOCHE: nuestro techo de yodo es EXACTAMENTE la dosis que hizo daño

`motor/seguridad.py` línea 163:

```python
TOPE_YODO_KCAL = 1400.0    # µg por 1000 kcal -- NRC 2006
```

y el comentario de encima dice: *«El NRC (2006) fija el límite superior seguro
en 1.400 µg por cada 1000 kcal de dieta.»*

**Eso no es lo que dice el NRC.** Lo que dice, literal, es lo contrario:

> *«Castillo et al. (2001a) reported evidence of **depressed thyroid gland
> function**, evidenced by reduced plasma concentrations of thyroid hormones **and
> bone abnormalities, in puppies fed diets containing an estimated maximum I
> content of 1,400 μg I per 1,000 kcal ME**, providing an estimated 250 μg I·kg
> BW⁻¹·d⁻¹. **Based on this information an absolute figure for a SUL of dietary I
> cannot be predicted for adult dogs.**»*

O sea: **1.400 es la concentración a la que se observó el daño** —tiroides
deprimida y alteraciones óseas en cachorros—, y el NRC dice **expresamente que
no puede fijar un límite superior seguro**. Nosotros lo copiamos como si fuera
el límite seguro y lo pusimos de techo. Un techo puesto justo en la dosis que
hace daño no es un techo.

Es la misma familia de fallo que el máximo de fósforo borrado el 7 de
septiembre: leer una línea de una fuente y aplicarla al revés de lo que dice.
Y es peor que aquel, porque aquel dejaba un menú sin techo y este pone el techo
en el sitio equivocado con un comentario que afirma una fuente que no dice eso.

**Lo que la fuente sí da, y sirve de anclaje:**

| Cifra | Qué es |
|---|---|
| 220 µg/1000 kcal | La dosis recomendada (RA) del NRC para perro adulto |
| **400 – 1.275 µg/1000 kcal** | El rango de piensos comerciales que Belshaw (1975) midió y que *«apparently these foods were fed without any clinical abnormalities»* |
| 1.400 µg/1000 kcal | **Donde se vio el daño** (Castillo 2001a, cachorros) |
| 2.750 µg/1000 kcal | El máximo LEGAL de FEDIAF (Tabla III-3a, 1,10 mg/100 g MS × 2,5) — más flojo que el nuestro, así que no ata |

**Medido antes de tocar nada**, sobre los 216 menús del catálogo precalculado:

```
peor menú ............ 1.038 µg/1000 kcal
mediana .............. 418
menús por encima de 1.275 ....... 0 de 216
menús por encima de 1.000 ....... 2 de 216
```

Así que bajar el techo de 1.400 a **1.275** —el punto más alto que la fuente
documenta como comido sin problemas— **no quita ni un menú** y saca el techo del
sitio donde hay daño documentado. Se aplica.

Lo que **no** decido yo, y va a `PREGUNTAS_PARA_ELENA.md`: si 1.275 es
suficiente margen. Está a un 9 % de la cifra que hizo daño, y esa cifra es de
**cachorros**, que son el grupo sensible, mientras que nuestro techo se aplica a
todos por igual. El peor menú real va a 1.038, o sea que habría sitio para
bajarlo bastante más sin coste. Pero elegir cuánto margen se le deja a una
tiroides es criterio clínico, y ahí no me meto.

### N-18 · Lo demás del capítulo 7, que sí cuadra

Tres coincidencias que conviene tener escritas, porque son la segunda fuente
diciendo lo mismo que ya aplicamos:

- **Calcio, techo de crecimiento.** NRC: *«a safe upper limit (SUL) for Ca in
  growing giant-breed puppies may reasonably be set at a minimum of 4.5 g per
  1,000 kcal ME»*. Nuestro `Calcio_LateGrowth_RazaGrande` tiene **4.500 mg**.
  Mismo número desde otra fuente. Y hay un dato más fino que no teníamos: Slater
  (1992) encontró que dar a cachorros de raza grande dietas con **≥3,6 g/1000
  kcal** se asociaba a más riesgo de osteocondritis — por debajo del techo, o sea
  que el margen real es más estrecho de lo que parece.
- **Fósforo: el NRC NO tiene techo.** *«There are insufficient data on which to
  base an SUL for P in dogs.»* Eso deja al techo del perro adulto sano (2.000
  mg/1000 kcal, SACN5 Tabla 13-3) como **la única cifra con fuente que existe**
  para esa pregunta — lo cual refuerza haberlo puesto, y explica por qué FEDIAF
  se queda en el 4.000 nutricional de AAFCO.
- **Sodio: el techo del NRC es 15 g/kg MS** = 3.750 mg/1000 kcal, muy por encima
  del nuestro (1.000 mg, SACN5). No hay conflicto: el nuestro es el estricto.

Y una cuarta que ya estaba anotada en N-7 pero ahora con el número: **el calcio
alto baja la absorción del fósforo**, y el efecto *«is most evident at Ca:P
ratios greater than 2:1»* — que es justo donde FEDIAF pone su techo de Ca:P en
adulto (2/1). Otra convergencia.

---

## NRC 2006, capítulo 8 (vitaminas) — y la trampa de la vitamina A

### ⚠️ N-19 · La mitad de nuestros menús no llegarían al mínimo de vitamina A sin contar caroteno, y en ningún sitio se dice

Esto **no lo buscaba**. Salió leyendo el capítulo 8 del NRC, que empieza
explicando algo que damos por sabido y no lo está:

> *«In nature, **all of the vitamin A ingested by animals originates from
> carotenoids** synthesized by plants… **1 IU of vitamin A is equivalent to 0.344
> μg of pure all-trans retinyl acetate (0.3 μg all-trans retinol)**… In humans, **21
> μg of β-carotene is required to provide 1 RE**… Even though **dogs appear to
> utilize β-carotene from carrots efficiently** (Turner, 1933; Bradfield and Smith,
> 1938), **a retinol equivalency has not been defined**.»*

O sea: **la vitamina A de una zanahoria y la de un hígado no son el mismo
nutriente**, hay un factor de conversión entre ellas, y **para el perro ese
factor no está definido**. En humanos son 21 a 1 desde el alimento; el convenio
europeo clásico usa 6 a 1; el americano moderno (RAE) usa 12 a 1.

**Medido en los 216 menús del catálogo precalculado**, separando la vitamina A
que viene de la categoría «Verduras y frutas» (todo caroteno, cero retinol) de
la que viene de vísceras, carne y suplementos:

```
% de la vitamina A que viene de vegetal .... mediana 83 %, máximo 100 %

menús que NO llegarían al mínimo de FEDIAF (526,2 µg/1000 kcal)
si no se cuenta el caroteno ................ 103 de 216   (48 %)

el peor:  Grande_Lactante   11.191 µg totales,
                            de los cuales retinol de verdad: 29
```

**Veintinueve microgramos de retinol en el menú de una perra lactante**, y el
semáforo lo da verde porque suma los 11.191. Si el factor real del perro fuera
el humano (21:1 en vez del 6:1 que traen las fichas), ese menú tendría que
dividir el caroteno por 3,5 y se quedaría muy corto.

**Y las fichas no siguen un solo convenio.** Comparadas con USDA:

| Alimento | Nuestra ficha | USDA RAE (12:1) | β-caroteno ÷ 6 |
|---|---|---|---|
| Zanahoria | 1.346 | 835 | 1.381 ← nuestro valor es este |
| Boniato | 667 | 709 ← nuestro valor es este | 1.418 |
| Rúcula | 596 | 119 | 237 ← **ninguno de los dos** |

O sea que la columna `vitA` del catálogo mezcla al menos dos convenios
distintos, y en algún caso ninguno de los dos.

**Y `UNIDADES.md` no lo dice.** El archivo que existe justo para que esto no
pase trae una sola línea —«Vitamina A · `vitA` · µg»— y una regla de conversión
desde UI. No dice si esos microgramos son **retinol**, **equivalentes de retinol
a 6:1** o **RAE a 12:1**, ni menciona los carotenoides. Es exactamente el mismo
tipo de agujero que el `linoleico`/`linolenico`, y con la misma propiedad: **no
salta nada, el menú sale verde igual**.

**Lo que NO he hecho, a propósito.** No he tocado ni un valor del catálogo:
rellenar datos no es mi trabajo (regla escrita desde la primera sesión). Y no he
puesto ningún factor de conversión, porque el NRC dice literalmente que para el
perro **no está definido** — inventarme uno sería justo lo que `CERRADO.md`
prohíbe.

**Lo que sí he hecho:** medirlo, escribirlo aquí, avisarlo en `UNIDADES.md`,
abrir la pregunta en `PREGUNTAS_PARA_ELENA.md` y apuntar el trabajo de datos en
`DATOS_QUE_FALTAN.md`.

### N-20 · Los techos de vitamina A del NRC, y por qué el nuestro no es el que aprieta

| | NRC 2006 (µg retinol/1000 kcal) | Lo nuestro (FEDIAF) |
|---|---|---|
| Cachorro | **3.750** (15.000 µg/kg de dieta a 4 kcal/g) | 30.000 |
| Hembra reproductora | **3.750** | 30.000 |
| Adulto no reproductor | **16.000** (64.000 µg/kg) | 30.000 |

El techo de FEDIAF es **ocho veces** el que el NRC sugiere para un cachorro. Y
medido, **116 de 216** de nuestros menús pasan de 3.750 y **4** pasan incluso de
16.000, mientras que **ninguno** pasa de 30.000: o sea que más de la mitad de
los menús viven justo en ese hueco entre las dos fuentes.

**Antes de asustarse hay que leer las dos mitades**, y es importante:

1. El 3.750 del NRC **no sale de ningún experimento con cachorros**. Sale de
   *«The NRC (1987) proposed a presumed maximal safe level … of 10 times the
   requirement … Because carnivores appear to have a higher tolerance … **it is
   suggested that** an upper limit of 15,000 μg retinol·kg⁻¹ diet … be used for
   puppies»*. Es precaución, no daño observado.
2. El daño observado en el perro está **muchísimo más arriba**: Cho (1975) dio
   90.000 µg de retinol **por kilo de peso y día** —que en un cachorro de 6 kg
   comiendo 800 kcal son unos **675.000 µg/1000 kcal**, veintinueve veces
   nuestro peor menú—. Y Cline (1997) dio a perros adultos **67.500 µg/1000
   kcal durante un año** sin encontrar ningún cambio en el hueso.
3. Y el 73 % de la vitamina A de nuestro peor menú de cachorro **es caroteno de
   zanahoria**, y *«dietary carotenoids are assumed to have **a low toxicity for
   dogs**»*: el caroteno no da hipervitaminosis A. Contarlo contra un techo es
   ir del lado seguro.

**Conclusión: por el techo no hay problema, y el motivo es interesante** — el
techo se aplica a una suma que mezcla retinol y caroteno, y eso aprieta de más,
que es el lado bueno. El problema está en el **suelo**, que es N-19: la misma
mezcla, mirada desde abajo, afloja de más. Es el mismo dato leído por sus dos
extremos, y solo uno de los dos es peligroso.

---

## Lo que queda MEDIDO y listo para aplicar (noche del 8 al 9)

Tres cosas del NRC que no están en el motor, con la medida hecha **antes** de
tocar nada, para saber si cuestan menús o no.

### N-21 · El ratio linoleico:linolénico — 15 de 216 menús se salen, uno a 109:1

La regla es N-9: **2,6 a 26 en adulto**, **2,6 a 16 en gestación y lactancia**,
≈16 en crecimiento. Medido sobre los 216 menús precalculados:

```
ratio LA:ALA .......... mínimo 0,50   mediana 7,79   máximo 109,14

por debajo de 2,6 ..........  1 de 216
por encima de 26 ........... 15 de 216
por encima de 16 ........... 67 de 216
```

El peor, un menú de senior de raza mini: **1,53 g de linoleico contra 0,014 g de
linolénico**. Ciento nueve a uno, cuando el techo es veintiséis.

**Y se entiende por qué pasa.** FEDIAF **no da mínimo de linolénico en adulto**
(la fila lleva «-»), así que en un menú de adulto no hay nada que impida al
omega-3 caer a cero mientras el omega-6 sube. La restricción de FEDIAF es solo
un suelo de linoleico (3,82 g/1000 kcal); no hay techo, y no hay ninguna
relación entre los dos. Es el mismo agujero que tenía el ratio Ca:P antes de
ponerlo, y por el mismo motivo: **una relación entre dos nutrientes no cabe en
una tabla de números fijos**, así que un barrido de tablas no la encuentra.

Es lineal (`LA − 26·ALA ≤ 0` y `2,6·ALA − LA ≤ 0`), así que entra en el solver
exactamente igual que el Ca:P, que ya está.

**Esta sí cuesta menús**, a diferencia del yodo: quince de doscientos dieciséis
tendrían que cambiar. Es lo que tiene tapar un agujero real.

### N-22 · La arginina que sube con la proteína

La regla es N-12: **+0,01 g de arginina por cada gramo de proteína bruta por
encima del requisito** (perro, NRC 2006 cap.6). También es lineal:

    arginina − 0,01 × proteína  ≥  arginina_minima − 0,01 × proteina_requerida

Pendiente de medir con el motor libre (la batería estaba corriendo), porque
medirlo bien exige `margenes_categoria=MARGENES_V2` — ver el aviso de más
arriba sobre las medidas hechas sin proporciones BARF.

### N-23 · Y una comprobación que sale bien, escrita para no repetirla

**La vitamina K y el pescado.** El NRC trae un caso feo: gatos con dietas
comerciales de salmón y atún **muriendo de hemorragias**, con 60 µg de vitamina
K/kg de dieta, y recuperándose con vitamina K1 (Strieker 1996). Como el BARF
puede llevar bastante pescado, había que mirarlo.

**No nos aplica, y la fuente lo dice explícitamente.** FEDIAF 2025 pone el aviso
del pescado **solo en la sección del gato** (§3.3.2): *«there is some indication
that canned pet food for cats being high in fish may increase the risk of
prolonged coagulation times»*. En la sección del perro (§3.3.1) dice solo:
*«Vitamin K does not need to be added unless diet contains antimicrobial or
anti-vitamin compounds»*. Y el NRC, en el capítulo del perro: *«Many commercial
dog foods do not contain supplemental vitamin K, and **there is a lack of reports
of dogs fed these diets having prolonged clotting times**»*. Los dos casos
publicados son de gato.

**La tiaminasa, en cambio, sí, y nuestra lista cuadra.** El NRC dice: *«Carp and
saltwater herring contain thiaminases, but **perch**, catfish, butterfish, and
spots apparently **do not**»*, y *«Both thiaminase I and thiaminase II are
inactivated by cooking»* — que es justo por qué al BARF le importa y al pienso
no. Nuestra lista (`motor/seguridad.py`) lleva sardina, caballa, arenque,
boquerón, carpa, atún, gamba y langostino, y **no** lleva la perca, que sí está
en el catálogo. Coincide con la fuente en las dos direcciones.

**Y el techo de vitamina D está bien puesto y bien atribuido**, al contrario que
el del yodo: *«It is suggested that a dietary concentration of cholecalciferol
should not exceed **20 μg per 1,000 kcal** for growing dogs»* — que es
exactamente `TOPE_VITD_KCAL = 20.0`. Y el límite legal de FEDIAF que aplicamos
además (14,1875 µg) coincide casi al decimal con la otra recomendación del mismo
párrafo: *«mammals not be exposed to diets containing more than 55 μg
cholecalciferol·kg⁻¹ … equivalent to **14 μg** cholecalciferol per 1,000 kcal»*.

### N-24 · Un número del NRC que parece un techo y NO hay que aplicar: la colina

Lo escribo porque es el reverso de N-17, y la lección es la contraria: **no todo
lo que la fuente llama límite lo es**, y leer solo la frase del límite lleva a
romper el motor.

El NRC dice: *«A presumed safe maximum intake of **2,000 mg choline·kg⁻¹ diet**
is proposed»* — que a 4 kcal/g son **500 mg/1000 kcal**.

**Medido: 213 de nuestros 216 menús lo pasan**, con una mediana de 878 y un
máximo de 2.052. Aplicarlo dejaría al motor casi sin menús.

**Y no hay que aplicarlo**, por tres cosas que están en el mismo párrafo:

1. **El mínimo de FEDIAF para el perro adulto son 474 mg/1000 kcal.** Un «techo»
   un 5 % por encima del suelo obligatorio no es un techo: es un número que no
   deja ventana. Cuando eso pasa, casi siempre el número no es lo que parece.
2. **El NRC desmonta él mismo el único estudio de daño.** Davis (1944) vio
   anemia, y el NRC anota: *«No control dogs given only this diet were used in
   either study, and … injections of a liver extract or the feeding of a stomach
   preparation restored red cell numbers, **suggesting that the basal diet may
   have been deficient in an essential nutrient(s)**»*.
3. **Y lo que sí se probó salió bien**: *«McKibbin et al. (1944) supplemented the
   diet of growing puppies with 1,500 mg choline chloride·kg⁻¹ and **reported no
   problems**»*, y luego 2.000 mg/kg igual. O sea que los 2.000 son **lo más alto
   que alguien probó**, no la dosis a la que algo pasó.

**La regla que sale de aquí, y vale para todo el documento:** un «safe upper
limit» del NRC puede ser tres cosas distintas —daño observado menos un margen
(la grasa: 92 → 82,5), lo más alto probado sin incidentes (la colina), o una
extrapolación de «diez veces el requisito» (la vitamina A del cachorro)—, y el
NRC lo dice cada vez. **Hay que leer cuál de las tres es antes de aplicarlo**, y
es exactamente lo que no se hizo con el yodo (N-17), donde se aplicó como techo
seguro una cifra que era daño observado.

---

## SACN5 capítulo 37 (enfermedad renal crónica), leído entero — y aquí está lo de Cris

Este es **el capítulo del que salen las cosas que dijo la nutricionista**, y
leerlo entero encuentra que de su tabla de nutrientes clave aplicamos cuatro
filas de ocho.

### N-25 · La Tabla 37-9 completa, y lo que falta de ella

Literal, columna de perro (todo sobre materia seca; conversión ×2,5 a
g/1000 kcal, la misma que usa el resto del repo):

| Fila de la tabla | Lo que dice (perro) | En g/mg por 1000 kcal | ¿Lo aplicamos? |
|---|---|---|---|
| Proteína | 14 – 20 % MS | 35 – 50 g | **sí**, pero a 62,5 (ver abajo) |
| Fósforo | 0,2 – 0,5 % MS | 500 – 1.250 mg | **sí**, 1.200 |
| Sodio | ≤ 0,3 % MS | ≤ 750 mg | **sí**, 750 |
| Potasio | 0,4 – 0,8 % MS | 1.000 – 2.000 mg | **sí** el techo (2.000); el suelo **ya lo cubre FEDIAF**, que pide 1.450 |
| **Cloruro** | **1,5 × el sodio** | **≤ 1.125 mg** con nuestro tope de sodio | **NO** |
| **Omega-3 totales** | **0,4 – 2,5 % MS** | **1,0 – 6,25 g** | **NO** |
| **Ratio omega-6 : omega-3** | **de 1:1 a 7:1** | — | **NO** |
| Vitamina E | ≥ 400 UI/kg de alimento | ≥ 67,1 mg | **sí**, 67,1 |
| Vitamina C | ≥ 100 mg/kg de alimento | ≥ 25 mg | **no se puede**: el perro la sintetiza, FEDIAF no la pide y el catálogo no tiene la clave |

**Medido, sobre los 216 menús precalculados** (que son de perro sano, así que no
es que estén mal — es para saber si estas restricciones morderían):

```
cloruro / sodio ....... mediana 1,27   máximo 2,63    por encima de 1,5:  24 de 216
omega-3 totales ....... mediana 1,28   mínimo 0,15    por debajo de 1,0:  73 de 216
omega-6 / omega-3 ..... mediana 4,68   máximo 28,34   por encima de 7:    52 de 216
```

O sea: **las tres muerden**. No son filas decorativas.

### N-26 · Los dos matices que hay que leer antes de aplicar nada de esto

**Primero, la proteína.** La tabla pide 14-20 % MS = **35-50 g/1000 kcal**, y el
mínimo de FEDIAF para el perro adulto sano son **52,1**. O sea que **el rango
entero de la tabla cae por debajo del mínimo de FEDIAF**: no es formulable sin
bajar de FEDIAF, que es justo lo que `necesita_bajo_fediaf` marca. Nuestro
62,5 no es la tabla: es lo más bajo que se puede pedir sin romper el suelo, con
margen. Esto ya estaba bien resuelto y documentado; lo escribo para que quien
lea la tabla no piense que el motor se quedó corto.

**Segundo, y es la respuesta a Cris sobre el ratio omega-6:omega-3: las dos
fuentes se contradicen, y hay que decirlo.**

- **SACN5, Tabla 37-9**, para el renal: *«Omega-6:omega-3 fatty acid ratio of
  **1:1 to 7:1**»*. Un objetivo clínico, con números, para una patología
  concreta.
- **NRC 2006, cap.5**: *«The European expert committee also specifically
  concluded that the use of a **total n-6:n-3 ratio is not helpful**»*, y
  recomienda en su lugar el ratio **LA:ALA** (N-9).

No es que una de las dos esté equivocada. Es que **hablan de cosas distintas**:
el NRC habla del perro **sano** y de fijar requisitos generales, donde el ratio
total mezcla ácidos grasos de potencia muy distinta; SACN5 habla de un objetivo
**terapéutico** en un perro **enfermo**, donde lo que se busca es un efecto
antiinflamatorio concreto y el ratio total es la forma en que la literatura
clínica lo escribe.

**La lectura que propongo, y que no aplico solo:** el ratio **LA:ALA** del NRC
como requisito del perro sano en todas las etapas (N-21, N-9), y el ratio
**total omega-6:omega-3** de SACN5 **solo dentro de las patologías que lo
piden**, como un tope más de `patologias.json`, con su cita. Son dos reglas
distintas en dos sitios distintos, que es exactamente como está montado el resto
(FEDIAF en un fichero, SACN5 en otro, condicionales en un tercero).

Va a `PREGUNTAS_PARA_ELENA.md` §5, porque «qué ratio se le pide a un perro
renal» es criterio clínico y no mío.
