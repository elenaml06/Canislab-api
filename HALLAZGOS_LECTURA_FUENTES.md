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
| El toy de 1,5 kg: 12 semillas sin menú de 30 a 1 s de solver — ⚠️ y **0 de 30 a 30 s**, o sea que era el reloj y no el «sorteo» (corregido el 10 sep) | §14.4 |

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

---

## ⚠️ Y UN FALLO NUESTRO, ENCONTRADO POR CASUALIDAD AL MEDIR OTRA COSA

### N-27 · El catálogo de la vista previa se regeneró SIN las proporciones BARF

**No salió de leer una fuente.** Salió mirando de dónde venía la vitamina A del
peor menú de cachorro (N-19) y viendo esto en la lista de ingredientes:

```
Zanahoria .......  620,3 g
Nabo pelado ..... 1405,7 g      ← en un menú de 493 kcal para un cachorro mini
```

Un menú de 1,6 kg para un cachorro de raza mini. Eso no es una ración BARF.

**Medido, la rama contra `main`:**

| Menú | En `main` | En la rama | Verdura |
|---|---|---|---|
| Toy_Adulto | 131 g | **655 g** | 5 % → **89 %** |
| Pequeño_CachorroCrecimiento | 586 g | **2.903 g** | 10 % → **92 %**, y **sin nada de hueso** |
| Gigante_Lactante | 6.846 g | **25.792 g** | 10 % → **91 %** |

**Veinticinco kilos y ocho gramos de comida al día.**

**La causa, en una línea:** el 8 de septiembre el catálogo se regeneró con un
script que vivía en un scratchpad —fuera del repo— y que llamaba a
`mc.resolver()` **sin `margenes_categoria`**. `motor_completo.py` aplica las
proporciones BARF dentro de un `if margenes_categoria:`, así que sin ese
argumento el motor formula **sin proporciones**.

**Y los 216 salían VERDES.** Cumplen los 43 requisitos, así que ni el semáforo
ni `_garantizar_verificado` tenían nada que objetar. Lo que se había apagado no
era la nutrición: era **la FORMA**. Y la forma no la mira el semáforo — por
diseño, porque la regla 3 del `CLAUDE.md` dice que la forma es lo único que se
puede relajar. Lo que la regla 3 **no** dice es que se pueda relajar sola, sin
que nadie lo pida y sin decirlo, que es exactamente lo que pasó.

**No llegó a `main`**: se quedó en la rama. Pero habría llegado, porque nada lo
miraba.

**Las tres cosas que se han arreglado, y las tres importan por separado:**

1. **El script está en el repo**, como `regenerar_catalogo.py`, y hace la misma
   llamada que hace la API. La lección es la de siempre en este proyecto y ya
   estaba escrita para los datos: *si vive solo en tu ordenador, se pierde* —
   resulta que también vale para **la herramienta que produce un dato**.
2. **El BLOQUE 25 comprueba desde hoy las proporciones** de cada uno de los 216
   menús contra `constructor.MARGENES`, que es la misma tabla que usa el motor.
   Es la única comprobación que lo caza, porque por nutrientes es indetectable.
3. **El catálogo se ha regenerado bien**, con las proporciones puestas. Los
   tamaños vuelven a ser de comida: Toy_Adulto en 166 g, no en 655.

**Y la lección general, que es la que más vale:** *estaba todo verde* no
significa *estaba bien*. El semáforo comprueba los 43 requisitos y **solo** los
43 requisitos. Cualquier otra cosa que se rompa —la forma, las cantidades, la
procedencia de un dato— sale verde igual, y hace falta una prueba distinta para
cada una. Es el mismo argumento que hay detrás de `dato_dudoso`, de
`cero_verificado` y del sello de los datos: **cada cosa que puede romperse en
silencio necesita su propio testigo**.

---

## ⚠️ EL FALLO DE LA NOCHE DEL 8 AL 9: DOS CIFRAS DEL MISMO LIBRO QUE NO CABEN JUNTAS

**Y no lo encontró leer una fuente: lo encontró comprobar que lo que decimos
que se puede formular se pueda formular.**

Esa noche se aplicaron, en pasadas distintas y con horas de diferencia:

- **Tabla 35-3 de SACN5** (disfunción cognitiva): vitamina E **≥ 187,5
  mg/1000 kcal** («Provide foods with ≥750 mg/kg» de materia seca ÷ 4).
- **`recomendaciones_libro.json`** (SACN5, perro adulto sano): fósforo
  **≤ 2.000 mg/1000 kcal**.

Cada una se midió por separado, y **cada una cabía por separado**. Juntas no:
para llegar a 187,5 mg de vitamina E el motor tiene que cargar de verdura y de
hígado, y eso sube el fósforo por encima de 2.000.

**Resultado, medido sobre el camino real de la API y todos los peldaños:**

```
disfunción cognitiva,  8 kg .... SIN MENU
disfunción cognitiva, 22 kg .... SIN MENU
disfunción cognitiva, 40 kg .... SIN MENU
```

Una patología marcada `formulable: true` que **no formulaba nada, a ningún
peso** — y que en `main` sí daba menú. El cambio la dejó peor que como estaba.

**Dónde está el techo de verdad** (bisecando el suelo con el techo de fósforo
puesto, perro de 22 kg y DER 1.000):

```
vitE ≥ 120 ..... peldaño ESTRICTO   (real 125,5;  fósforo 1.998)
vitE ≥ 150 ..... peldaño 5          (real 156,9;  fósforo 1.998)
vitE ≥ 175 ..... peldaño 5          (real 177,7;  fósforo 1.998)
vitE ≥ 185 ..... SIN MENU
vitE ≥ 187,5 ... SIN MENU          ← lo que pide la fuente
```

El catálogo llega a ~180 y la fuente pide 187,5: **se queda fuera por un 5 %**.
Sin el techo de fósforo el menú que sale lleva 4.000 mg de fósforo y **403 g de
albahaca** para un perro de 22 kg — el solver exprimiendo la columna de la
vitamina E, no una ración.

**Qué se ha hecho.** La vitamina E pasa a
`limites_escritos_que_el_solver_no_aplica`, con la cita, la medida y el motivo:
el mismo trato que ya tenía el omega-3 del cáncer, que no cabe por lo mismo. El
suelo de omega-3 (2,5 g/1000 kcal) de esa misma tabla **se sigue aplicando** y
resuelve en el peldaño estricto.

### Las tres lecciones, y ninguna es «leer mejor»

1. **Medir una cifra sola no dice nada sobre el conjunto.** Las dos se midieron
   bien; lo que faltó fue volver a medir la primera después de poner la
   segunda. En un motor de restricciones, **cada limite nuevo invalida todas
   las medidas anteriores**, no solo las del mismo nutriente.
2. **El semáforo no puede cazar esto, por construcción.** No hay menú que
   mirar. `_garantizar_verificado()` es el filtro que impide entregar un menú
   malo; no existe nada que impida **no entregar ninguno**. Son dos fallos
   opuestos y hasta hoy solo teníamos testigo para uno.
3. **Faltaba la comprobación más tonta de todas.** El BLOQUE 50 prueba doce
   cruces de patologías elegidos a mano, y la disfunción cognitiva no estaba en
   ninguno. El BLOQUE 36 audita las cifras de una en una, que es aritmética y
   no ve un cruce entre **dos nutrientes distintos**. Desde hoy el **BLOQUE 61**
   recorre las 39 patologías formulables y exige que cada una dé menú verde
   para el perro de referencia. Tarda ~110 s y es la única prueba del repo que
   vigila la frase *«esta patología se puede formular»*.

Y la lección general es la misma que dejó el catálogo regenerado sin
proporciones, vista por el otro lado: **estaba todo verde** no significa que
esté bien, y **no hay menú** tampoco salta solo. Cada cosa que puede romperse
en silencio necesita su propio testigo — incluido el silencio de no dar nada.

---

## Fascetti & Delaney 2ª ed., capítulo 10 (enfermedades ortopédicas), leído entero

Lo escribe **Herman Hazewinkel**, que es el autor de casi todos los estudios que
cita — y de los que SACN5 y FEDIAF citan a su vez cuando hablan del calcio del
cachorro de raza grande. O sea que no es una fuente más: es la fuente de las
otras.

### F-1 · ⚠️ EL CALCIO DE NUESTROS CACHORROS DE RAZA GRANDE VA AL TOPE DE FEDIAF, Y ESTA FUENTE PIDE LA MITAD

**Es lo más serio que ha salido de este capítulo, y toca a la población donde
equivocarse no se arregla después.**

Lo que dice Fascetti, literal, dos veces y en dos sitios distintos:

> *«In order to prevent panosteitis, a diet designed for young dogs of large
> breeds with a **calcium content no greater than 1.1% dm** should be fed during
> the growth period, starting at partial weaning.»*

> *«In general, in foods with a protein content of high biological value, **the
> calcium content should be between 0.8% and 1.0% on a dry matter basis** (for a
> food with 4200 ME kcal/kg diet) (Nap et al. 2000).»*

Y remata con una frase que va dirigida exactamente a lo que hacemos nosotros:

> *«The occurrence of these dietary orthopedic diseases **is increasing since the
> feeding of BARF and homemade diets has become more popular**.»*

**Lo que aplica el motor hoy:** el máximo de FEDIAF, 4.500 mg/1000 kcal =
**1,8 % MS**. Es decir, **el 64 % por encima del techo que da esta fuente** para
esa misma población, y el 125 % por encima del 0,8 % que llama «probado seguro».

**Y no es teórico: nuestros menús se pegan al techo.** Medido sobre los 12 menús
de crecimiento del catálogo precalculado:

```
Grande_CachorroCrecimiento ....... 4.500 mg/1000 kcal  = 1,80 % MS  ← EL TOPE EXACTO
Gigante_CachorroCrecimiento ...... 4.500                 1,80 %      ← EL TOPE EXACTO
Toy_CachorroCrecimiento .......... 4.500                 1,80 %
Pequeño_CachorroCrecimiento ...... 4.426                 1,77 %
Grande_CachorroJoven ............. 3.987                 1,59 %
Mini_CachorroCrecimiento ......... 3.956                 1,58 %
Gigante_CachorroJoven ............ 3.884                 1,55 %
...
Mediano_CachorroJoven ............ 2.551                 1,02 %   ← el único por debajo de 1,1 %
mediana .......................... 3.920                 1,57 %
11 de los 12 pasan de 1,1 % MS
```

Los tres que salen clavados en 4.500 no es casualidad: es el solver empujando
contra el techo, porque una ración con hueso va sobrada de calcio y el techo es
lo único que la frena. **Si mañana FEDIAF subiera el techo, subiríamos con él.**

**Por qué pasa, y por qué no es un fallo del motor:** FEDIAF da para el
crecimiento un mínimo de 2.000 (2.500 en raza grande tardía) y un máximo de
4.500. Los dos son requisitos y los dos se cumplen. Lo que dice Hazewinkel es
que **el sitio correcto dentro de esa ventana está pegado al mínimo, no al
máximo**, y eso el motor no lo sabe: el solver no tiene motivo para preferir un
extremo de una ventana legal.

**Los otros números del mismo capítulo, para tener la escala:**

| Calcio (% MS) en el cachorro | Qué se vio |
|---|---|
| 0,05 % (poodle miniatura) | fracturas patológicas |
| 0,55 % (gran danés) | fracturas patológicas |
| **0,8-1,0 %** | **lo que recomienda la fuente** |
| 1,1 % | el control sano de todos esos estudios; techo que da para prevenir panosteítis |
| **1,8 %** | **donde formulamos nosotros (= el máximo de FEDIAF)** |
| 3,3 % (gran danés) | osteocondrosis severa, radius curvus, wobbler |
| 3,3 % solo de la 3ª a la 6ª semana | panosteítis en TODOS, con la comida ya normalizada después |

Ese último es el que más asusta: **tres semanas de exceso en el destete y la
lesión aparece meses después**, con la dieta ya corregida.

Y por peso vivo, del mismo capítulo: *«at 2 months of age, 260-830 mg Ca/kg
BW/d appears to be safe for skeletal growth; decreasing to 210-540 mg Ca/kg BW/d
at 5 months of age»*.

**Qué NO he hecho.** Bajar el techo yo. Apretar el calcio del cachorro por
debajo de lo que permite FEDIAF cambia todos los menús de crecimiento del
producto y es exactamente «una decisión que depende de criterio clínico».
Va como pregunta a `PREGUNTAS_PARA_ELENA.md` §8, con la medida de si cabe.

### F-2 · El techo de vitamina D que aplicamos, contrastado con la dosis que hizo daño

La Tabla 10.5 del mismo capítulo da la dosis-respuesta en gran danés:

```
1,14 µg vitamina D/100 g MS ..... osificación endocondral NORMAL
  10 µg/100 g MS ................ osteocondrosis LEVE
 135 µg/100 g MS ................ osteocondrosis SEVERA
```

Los 10 µg/100 g MS son 100 µg/kg MS = **25 µg/1000 kcal** con el puente de
siempre. **Nuestro techo son 14,1875 µg/1000 kcal** (el legal, Reglamento (UE)
2017/1492, que es más estricto que el nutricional de FEDIAF). O sea que estamos
al **57 % de la dosis más baja a la que se documenta lesión**, un factor de
seguridad de 1,76.

No cambia nada —el límite legal manda y ya lo aplicamos— pero conviene tenerlo
escrito: **el margen no es enorme**, y el propio capítulo avisa de que *«a true
safe upper limit for vitamin D intake… is not currently known in dogs»*, que es
la misma frase que el NRC usa para el yodo.

### F-3 · Lo que confirma, sin cambiar nada

- **El EPA de la artrosis tiene respaldo clínico y el omega-3 total no.** Ver
  el detalle en `patologias.json` y en `PREGUNTAS_PARA_ELENA.md` §7: el ensayo
  del 4 % de omega-3 (Hazewinkel 1998) movió el marcador bioquímico y **no** la
  cojera medida con placa de fuerza; el del EPA (Schoenherr 2005) mejoró el
  apoyo en el 82 % frente al 31 % del control.
- **La proteína alta no daña el esqueleto del cachorro.** Gran daneses con 29 %
  de las kcal en proteína: ninguna diferencia en crecimiento, metabolismo del
  calcio ni desarrollo esquelético (Nap et al. 1993b). Es la respuesta a un
  miedo clásico de quien da BARF a un cachorro de raza grande, y nuestras
  raciones van muy por encima de eso.
- **El perro no sintetiza vitamina D en la piel**, así que toda la que hay viene
  de la comida — que es por lo que el techo importa más que en humanos.

---

## Fascetti & Delaney 2ª ed., capítulo 15 (enfermedad renal), leído entero

Lo firman **Yann Queau y Denise Elliott**. Es la otra mitad de lo que ya
teníamos por SACN5 cap.37 y por IRIS, y sirve sobre todo para **contrastar**:
donde los dos libros coinciden, el número está firme; donde no, hay que decirlo.

### F-4 · Lo que CONFIRMA lo que ya aplicamos

**El fósforo, con la cifra de supervivencia detrás.** Literal:

> *«In one study of dogs with surgically induced reduced renal function, dogs
> fed a **low‐phosphorus diet (0.44% dm)** for 24 months had a **75% survival**
> versus a **33% survival** in dogs fed a **high‐phosphorus diet (1.44% dm)**
> (Finco et al. 1992b). Renal function also deteriorated more rapidly in the
> high‐phosphorus group.»*

0,44 % MS = **1.100 mg/1000 kcal** con el puente de siempre. **Nuestro tope
renal son 1.200**, o sea prácticamente la dieta del brazo que sobrevivió. Es la
primera vez que ese número aparece con un desenlace duro (supervivencia a 24
meses) y no solo como recomendación de tabla.

**El omega-3, y por qué el suelo que puse ayer va en la dirección correcta:**

> *«Supplementation with menhaden fish oil **lowered glomerular capillary
> pressure, reduced proteinuria, and slowed progressive decline in the GFR**
> (Brown et al. 1998).»* Y del otro lado: *«**Omega-6 fatty acids appeared to be
> detrimental** to renal disease… supplementation with omega-6 PUFA… was
> associated with **increased glomerular capillary pressure, glomerular
> enlargement**, and increased eicosanoid excretion rates (Brown et al. 2000).»*

Y una precisión que importa a un catálogo como el nuestro, donde el aceite de
linaza es la fuente de omega-3 más concentrada que hay: *«one study suggests
that the provision of dietary long-chain omega-3 fatty acids **from marine
sources** versus dietary shorter-chain omega-3 fatty acids **from plant
sources** is also important in the dog (Waldron et al. 2012)»*. O sea que **el
lino no sustituye al pescado** para esto: nuestro suelo renal es de omega-3
totales (linolénico + EPA + DHA) y el motor puede cumplirlo con lino solo.
Apuntado, sin cambiar nada: separar el suelo en «totales» y «de cadena larga»
es decisión clínica.

### F-5 · ⚠️ Donde los dos libros NO dicen lo mismo: el sodio del renal

**SACN5 (Tabla 37-9) pide sodio ≤0,3 % MS**, que es de donde sale nuestro tope
renal de **750 mg/1000 kcal** — y de ahí el cloruro de 1.125 que puse ayer,
porque la misma tabla lo escribe como «1,5 × el sodio». **Fascetti dice que eso
no tiene evidencia.** Literal:

> *«There have not been any published studies to demonstrate that dietary sodium
> restriction will alleviate hypertension or slow disease progression.»*
>
> *«In healthy cats and dogs, dietary sodium intake **up to… 4.1 g/Mcal in
> dogs** does not affect blood pressure or renal or cardiac functions.»*
>
> *«**there is currently no evidence to suggest that lowering dietary sodium will
> reduce blood pressure** in cats or dogs with CKD.»*

Y añade que en el gato la restricción de sodio **activó el sistema
renina-angiotensina-aldosterona y bajó el potasio** sin tocar la presión
(Buranakarl et al. 2004). O sea que no es solo inútil: puede tener coste.

**4,1 g/Mcal son 4.100 mg/1000 kcal: cinco veces y media nuestro tope.**

**Qué he hecho: nada, y a propósito.** Nuestro tope es el más estricto de los
dos y está muy por encima del mínimo de FEDIAF, así que **no puede hacer daño**
y no deja a nadie sin menú (medido ayer: los cuatro renales salen con 436-470 mg
de cloruro contra un techo de 1.125). Pero el propio Fascetti reconoce que las
dietas renales del mercado siguen siendo moderadamente bajas en sodio
(«remain common and recommended»), así que estamos donde está el mercado.
Queda escrito para que quien firme una pauta sepa que ese número es
**convención, no evidencia**.

### F-6 · Y una frase que vale por un capítulo entero, sobre lo que hacemos

> *«In one report evaluating 28 and 39 recipes advocated for cats and dogs with
> kidney disease, respectively, assumptions on ingredient and/or supplement type
> were required for every recipe, and their analysis with computer software
> revealed that **no recipe met all National Research Council nutrient
> recommended allowances** for adult animals (Larsen et al. 2012). Deficiencies
> were common for essential amino acids, trace minerals, or some vitamins.»*

**Sesenta y siete recetas caseras para perro y gato renal, y ninguna cumplía.**
Los huecos que enumera —aminoácidos esenciales, oligoelementos y vitaminas— son
exactamente las tres cosas que este motor comprueba de cero en cada menú desde
el 28 de agosto, cuando entraron los 12 aminoácidos. Es la mejor descripción que
he leído de por qué existe la regla 1 del `CLAUDE.md`.

Y el aviso que va con ella, que también nos toca: *«owners are likely to
substitute or delete some ingredients or supplements, unbalancing the diet in a
process referred to as **“diet drift”**… only **13% of dog owners** that were
provided a homemade diet recommendation at a veterinary teaching hospital were
strictly adhering to the recipe a few years later (Johnson et al. 2016)»*.
Trece por ciento. Es un argumento de producto, no de nutrición, y va a
`PENDIENTE_PRODUCTO.md`: el menú se cumple si es fácil de cumplir.

---

## Fascetti & Delaney 2ª ed., capítulo 9 (manejo del peso), leído entero

### F-7 · La frase que justifica, palabra por palabra, el escalado de mínimos

> *«**Maintenance foods in general are likely not fortified enough in essential
> nutrients to be safely used for the caloric restriction necessary for active
> weight loss.**»*

Es exactamente lo que hace `minimo_de()` en `verificar.py` con la ecuación 7.2.5
de FEDIAF: cuando el perro come menos, el mínimo por 1000 kcal **sube**, porque
lo que necesita no baja con las calorías. Un alimento normal no está formulado
para eso; el nuestro se reformula para cada perro, que es la única forma de que
la restricción calórica no se cobre un micronutriente. Lo vigila el BLOQUE 34.

Y con ella la otra mitad, que es la que sostiene el suelo de proteína en
obesidad: *«increasing dietary protein may help preserve lean body mass during
weight loss in both dogs and cats»*.

### F-8 · La cifra de restricción calórica, que NO es la misma base que la nuestra

Fascetti da dos, y hay que leer bien la base de cada una:

> *«weight reduction may be achieved simply by **restricting the current calorie
> intake by 20-40%**»* — es decir, sobre lo que el perro come HOY.
>
> *«Typically the recommendation is to restrict the pet to **60-70% of the
> calories it would normally require to maintain its current weight**»* — es
> decir, sobre el **MER** del peso ACTUAL.
>
> *«The patient's resting energy requirement (RER) should be calculated using an
> estimate of its **optimal body weight** (RER = 70 × BWkg^0,75).»*

**Nosotros calculamos el DER sobre el peso OBJETIVO** (ver «el peso de
referencia para escalar es `peso_objetivo_kg`» en `CLAUDE.md`), que es la
tercera de las tres y la que recomienda AAHA. No hay contradicción —Fascetti
también usa el peso óptimo para el RER— pero **las dos primeras cifras se
expresan sobre el peso actual y la nuestra sobre el objetivo**, así que no son
comparables sin convertir. Queda escrito porque es justo el tipo de cifra que
alguien copia de un libro a un campo sin mirar la base, y `der_casos.json` es el
contrato que lo sujeta. No cambio nada: el DER lo manda el frontend y su fuente
es AAHA 2021, ya verificada.

### F-9 · Ritmo de pérdida y L-carnitina: uno se confirma y el otro se enfría

- **El ritmo**: *«the target weight loss rate of **1-2% of body weight/week**»*.
  Coincide con lo que ya decimos.
- **La L-carnitina**, que aplicamos como suelo en obesidad y en artrosis (75
  mg/1000 kcal, de SACN5), aquí sale mucho más floja: *«May increase the rate of
  weight loss while promoting retention of lean body mass… **Effects are modest
  and inconsistent**»*. No es motivo para quitarla —es un suelo, no un techo, y
  no cuesta menú— pero sí para no venderla como más de lo que es en el texto que
  lee el dueño.
- Y una que **no** tenemos y tampoco vamos a poner: el cromo. *«no companion
  animal study to date has shown any benefit from supplementation»*.

### F-10 · Y el dato que explica por qué la app pregunta el BCS y no se fía de la foto

> *«A study involving 201 dogs found that while the expert scored **79% of the
> dogs as overweight or obese, only 28% of the caregivers** scored their dogs
> above ideal.»*

Y del lado del veterinario: *«approximately 28% of the canine and feline
patients were scored as overweight or obese, but **only 2% had weight recorded
as an issue**»*. Es un argumento de producto y va a `PENDIENTE_PRODUCTO.md`: si
el dueño se equivoca al puntuar, el peso objetivo sale mal, y de ahí sale el DER
y de ahí los 43 requisitos escalados. Es la misma cadena que el `radiografia.py`
vigila por dentro, vista desde fuera.

---

## Fascetti & Delaney 2ª ed., capítulo 12 (páncreas exocrino), leído entero

### F-11 · La grasa de la pancreatitis: tres fuentes y tres definiciones de «baja en grasa»

Primero, un aviso del propio capítulo que vale para todo el motor:

> *«The use of generalized terms like “low-fat” or “high-fat” is confusing
> because **there is no established definition** of what a “standard” or
> “typical” dietary fat concentration is… Ideally, **percentage of ME is the
> ideal way to compare different foods**, since it allows for comparison between
> foods with varying amounts of moisture, fiber, and ash.»*

Y da la referencia práctica: *«For most of the population eating commercial
diets, **a diet that has less than 20% fat on an ME basis will be considered low
fat**»*.

**Dónde nos deja eso.** Nuestro tope de pancreatitis son **37,5 g/1000 kcal**
(SACN5 Tabla 67-3, «Fat ≤15 % DM»). En porcentaje de las kcal eso es
**≈33-34 % ME** — o sea que, con la definición de Fascetti, **nuestro menú de
pancreatitis no es una dieta baja en grasa**: está justo en el borde de lo que
él llama sin restringir.

Las tres cifras, en la misma unidad, para poder compararlas de una vez:

| Fuente | Lo que dice | g/1000 kcal | % ME |
|---|---|---|---|
| SACN5 Tabla 67-3, perro no obeso | «Fat ≤15 % DM» | **37,5** ← el que aplicamos | ≈34 % |
| SACN5 Tabla 67-3, obeso o hipertrigliceridémico | «≤10 % DM» | **25,0** ← también aplicado, graduado | ≈22 % |
| Merck Veterinary Manual | «less than 20 g fat/1,000 kcal» | 20,0 | ≈18 % |
| Fascetti cap.12 | «low fat» = <20 % ME | ≈22 | <20 % |

**Fascetti y Merck coinciden casi exactamente** (≈18-20 % ME), y los dos son
bastante más estrictos que el valor que aplicamos. Nuestro tramo graduado (25
g para el obeso o hipertrigliceridémico, puesto el 8 de septiembre) sí cae en
esa zona.

**Y la otra cara, que también está en el capítulo y que hay que decir entera:**

> *«Some authors have recommended using **highly digestible diets not restricted
> in fat (34-51% ME)** unless there is evidence of hyperlipidemia (Jensen and
> Chan 2014).»* Y un estudio de 10 perros sanos con 16 % vs 38 % ME de grasa
> *«did not find any differences in blood PLI, TLI, or gastrin concentrations»*.
> Y un retrospectivo de 34 perros con pancreatitis aguda: *«a **trend** toward
> fewer episodes of gastrointestinal intolerance in dogs fed low-fat diets, but
> **this did not reach significance**»*.

O sea que la literatura va de «no hace falta restringir» a «menos de 20 % ME», y
nosotros estamos en medio. La conclusión del propio capítulo es la única frase
que zanja algo: *«**If energy needs can be met, the use of a low-fat diet has no
drawbacks and is recommended** until more information is available»* — y en un
menú BARF formulado a medida las kcal se cubren siempre, así que el argumento
de la densidad energética, que es el único en contra, no nos aplica.

**No lo he cambiado.** El 8 de septiembre se subió de 20 a 37,5 con una regla
escrita (manda FEDIAF; donde no llega, SACN5) y una medida, y cambiarlo otra vez
esta noche sería ir y venir. Pero la regla de fuentes no contemplaba el caso de
**dos manuales que no dicen lo mismo**, y este es. Va a
`PREGUNTAS_PARA_ELENA.md` §9.

### F-12 · La EPI: lo que ya teníamos escrito era exactamente lo que dice esta fuente

El tope de grasa de la EPI (37,5, el extremo ALTO del rango de SACN5) se puso
con este motivo escrito: *«el propio texto dice que restringir la grasa NO es lo
prioritario si hay reemplazo enzimático adecuado -- es un apoyo, no el
tratamiento»*. Fascetti lo dice más fuerte todavía:

> *«current information indicates that **a low-fat diet is not necessary unless
> steatorrhea is uncontrollable**, at least initially.»*
>
> *«The most important finding of these studies was that **response to fat
> restriction varied greatly from dog to dog**: some animals responded favorably,
> others were not affected, **others were negatively affected**.»*
>
> *«There are studies in experimentally induced EPI in dogs that suggest that
> **fat restriction actually worsens lipase activity**, since fat and protein
> protect lipase during aboral intestinal transit.»*

Es una confirmación en toda regla de una decisión que ya estaba tomada por el
motivo correcto, y de que el aviso de la EPI («el tratamiento son las enzimas y
este menú no lo sustituye») es lo primero que hay que leer.

Y un aviso que sí nos toca por ser BARF: *«raw pancreas can also be used;
however, it **still carries the same risks associated with feeding any raw
animal product**, including the potential for zoonotic diseases»*. El páncreas
crudo circula como remedio casero para la EPI. No está en el catálogo y no debe
estarlo sin decir esto.

### F-13 · Y la lección de unidades, que es la de siempre

Este capítulo mide la grasa en **% de las kcal (ME)**; SACN5 la mide en **% de
materia seca**; Merck en **g/1000 kcal**; y la etiqueta de un pienso en **% tal
cual**. Son cuatro números distintos para la misma dieta y solo uno de ellos es
comparable entre alimentos. `UNIDADES.md` ya avisa de la trampa para el
catálogo; esta es la misma trampa un piso más arriba, en los LÍMITES.

---

## Fascetti & Delaney 2ª ed., capítulo 8 (dietas comerciales y caseras), leído entero

**Es el capítulo que habla de nosotros.** No de «una dieta casera» en abstracto:
del BARF, por su nombre, y de lo que sale mal cuando se hace sin cuentas. Hay
que leerlo entero y sin filtrar, porque la mitad de lo que dice es incómoda y la
otra mitad es exactamente el argumento de por qué existe este motor.

### F-14 · Las cifras de lo que pasa cuando una dieta casera no se calcula

> *«Overall, **most (190/200 [95%]) recipes resulted in at least 1 essential
> nutrient at concentrations that did not meet NRC or AAFCO guidelines**, and
> many (**167 [83.5%]) recipes had multiple deficiencies**… Only 3 recipes
> provided all essential nutrients in concentrations meeting or exceeding the
> NRC RA… **all 5 of these recipes were written by veterinarians**.»*

Doscientas recetas. **Nueve** cumplían el mínimo de AAFCO, y **ocho de esas nueve
las había escrito un veterinario**. Y en el capítulo 15 la misma medida sobre
recetas renales: 67 recetas, **ninguna** cumplía.

Y en crudo específicamente:

> *«One study evaluated the nutritional adequacy of **five raw food diets**. Two
> were commercial products, the remaining three home-prepared. **All five diets
> had essential nutrients that were analyzed to be below AAFCO minimum
> recommendations**… The home-prepared diets had **excessive concentrations of
> vitamins D and E**, as well as **inappropriate calcium to phosphorus
> ratios**.»*

Los tres fallos que enumera —vitamina D alta, vitamina E alta, Ca:P mal— son
tres de las cosas que este motor comprueba en cada menú: la D tiene techo legal
duro, la E tiene mínimo y el Ca:P es una de las 43 filas. No es casualidad: son
los fallos típicos de una ración de carne con hueso y suplementos, que es lo que
formulamos.

**Esto es el argumento entero de la regla 1 del `CLAUDE.md`**, escrito por
alguien de fuera: *ningún menú sale sin verificar*. Lo que separa nuestra ración
de las 190 que fallaban no es la receta: es que la nuestra se comprueba de cero
contra los 43 requisitos antes de entregarla, y si no está verde no se entrega.

### F-15 · ⚠️ «La disponibilidad del calcio del hueso molido es DESCONOCIDA»

Literal, y es la frase que más nos toca de todo el capítulo:

> *«Grinding bones may help reduce the risk of trauma and obstruction, but **the
> availability of the calcium from these sources is unknown**.»*

Nuestro catálogo cuenta el calcio del hueso carnoso como calcio disponible, con
las cifras de **Köber 2017** (que es el abstract del ESVCN con Ca, P y Ca:P de 15
huesos y cartílagos, y es la fuente que `Bases.md` fija justo para esto). Köber
da el CONTENIDO; esta frase dice que la **absorción** no está medida.

**No cambia ningún número** —no hay factor que aplicar sin inventarlo, que es
justo lo que `CERRADO.md` prohíbe— pero sí cambia lo que se puede AFIRMAR. Y hay
un matiz que juega a nuestro favor y conviene tenerlo escrito: el capítulo 10
(Hazewinkel) mide absorción real de calcio en cachorros con trazador ⁴⁵Ca y dice
que **la fuente casi no importa**: *«The source of calcium – **bone meal, fresh
bones**, or dairy products – **does not make a lot of difference**; it is the
amount of calcium eaten and absorbed that counts»*. O sea que las dos frases no
se contradicen del todo: la primera dice que no está cuantificado para hueso
molido, la segunda que en la práctica se comporta como las demás fuentes.

Queda anotado en `PENDIENTE_NUTRICION.md` como lo que es: **una incertidumbre
conocida sobre un dato que decide menús**, no un error.

### F-16 · Lo que dice del crudo, entero y sin recortar

Es lo más duro del capítulo y hay que copiarlo tal cual, porque recortarlo sería
elegir la parte que nos gusta:

> *«**There is no documented evidence that feeding raw meat has any health or
> nutritional advantages over cooked foods.** The US Food and Drug Administration
> (FDA) **does not advocate the feeding of raw meat**, poultry, or seafood to
> pets (FDA 2007).»*
>
> *«while many animals never become ill while consuming raw food diets, they
> **still pose a risk to humans and other animals through environmental
> shedding**… Individuals preparing raw diets are also at risk by handling
> contaminated meat and egg products. **Those greatest at risk are the very young
> and old, in addition to the immunocompromised.**»*
>
> *«It has been shown that **simple routine washing may not be enough** to
> eliminate potential food-borne pathogens in the animal companion's food bowl
> and environment.»*
>
> Y sobre el hueso: *«The use of raw bones (compared to cooked) **may reduce the
> risk of splintering and tooth fractures, but sharp fragments can still occur**
> and puncture the mucosa at any point along the gastrointestinal route.»*

**Qué hacemos con esto.** No es un número: no hay nada que aplicar en el solver.
Pero es información que quien usa la app **no tiene** y que le afecta a ella y a
quien viva en su casa. Dos cosas concretas, las dos de producto y ninguna
decidida por mí:

1. **Manipulación segura**, dicho una vez y bien: tabla y cuchillo aparte, lavado
   del comedero con algo más que agua, y el aviso explícito de que en una casa
   con bebés, personas mayores o alguien inmunodeprimido el riesgo no es del
   perro, es de ellos.
2. **El hueso**: ya avisamos de lo que no se puede pesar (BLOQUE 14), pero no del
   riesgo de fragmento. El propio texto reconoce que el crudo es mejor que el
   cocido en esto, que es la única ventaja documentada que le concede.

Va a `PENDIENTE_PRODUCTO.md`. Y con una regla de honestidad que creo que es la
correcta: **si la fuente que usamos para justificar los números dice esto, la app
no puede citarla solo cuando conviene.**

---

## Fascetti & Delaney 2ª ed., capítulo 13 (hígado y vías biliares), leído entero

### F-17 · La estrategia del cobre es la nuestra, contada por el otro lado

Fascetti describe la dieta hepática comercial así:

> *«the hepatic diets are **restricted in dietary copper**, have **increased
> concentrations of dietary zinc** and B vitamins, are **controlled in sodium**,
> and are fortified with antioxidants.»*

Es exactamente lo que aplica nuestra `hepatopatia`: cobre ≤2,4 · zinc ≥50 ·
sodio ≤625 · vitamina E ≥67,1 (más hierro ≥20 y taurina ≥250). Cuatro de cuatro,
y la vitamina E además con su motivo aquí escrito: *«Vitamin E may be beneficial
for the management of patients with copper-associated liver damage because of
its antioxidant effects that protect against lipid peroxidation»*.

Y la razón de que el zinc suba a la vez que el cobre baja, que no estaba escrita
en nuestro JSON: *«**zinc ions induce the synthesis of metallothionein, which
binds copper tightly, rendering it unabsorbable**»*. No es que el hígado enfermo
necesite más zinc: es que el zinc **bloquea la absorción del cobre**. Vale la
pena tenerlo escrito porque explica por qué los dos números van juntos y por qué
subir uno sin bajar el otro no sirve.

### F-18 · La lista de alimentos ricos en cobre, y por qué NO hace falta ponerla

> *«Homemade diets should **exclude liver, nuts, shellfish, mushrooms, and organ
> meats** that are all high in copper content (Center 1996b).»*

Es una instrucción operativa y sería tentador implementarla: el motor ya sabe
excluir alimentos por patología (lo hace con el oxalato y con el urato). **Pero
sería redundante y peor.** Nuestro tope de cobre (2,4 mg/1000 kcal) hace lo mismo
por el camino correcto: no prohíbe el hígado, prohíbe **pasarse de cobre**, y deja
que el solver decida si cabe una pizca de hígado o ninguna. Una exclusión por
nombre de alimento es más burda y se desincroniza cuando entra una ficha nueva
al catálogo.

Lo que sí conviene: que el aviso de `hepatopatia` **nombre esos cinco** para
quien además come fuera del menú. La regla de la comida es una cosa; el premio
de la tarde es otra.

Y una precisión útil para `raza_predispuesta_cobre`, cuyo aviso ya dice (bien) que
tener la raza no es tener la enfermedad: Fascetti confirma que **la dieta sola
funciona en poco más de la mitad**: *«hepatic copper concentrations could be
normalized in one study with dietary intervention alone in **15 out of 28**
subclinical Labrador retrievers… However, some study individuals **continued to
accumulate copper despite being fed a low-copper and high-zinc diet**»* — y por
eso el seguimiento es con biopsia, no con el menú.

### F-19 · La proteína hepática: confirma que necesita firma

> *«the hepatic formulas are generally **less protein restricted (14-15.5%
> protein on an ME basis)** than most renal diets»*

14-15,5 % de las kcal en proteína son **≈35-39 g/1000 kcal**, es decir **por
debajo del mínimo de FEDIAF para adulto (52,1)**. Es lo que ya dice nuestro
`necesita_bajo_fediaf` para las hepatopatías con encefalopatía y para el shunt: no
se puede formular por la puerta normal, hace falta prescripción. Segunda fuente
que da el mismo rango.

Y el matiz clínico que va con ello, que también teníamos: *«Dietary protein should
**not** be restricted… **unless** the cat is showing signs of encephalopathy»*.
Restringir proteína en una hepatopatía sin signos neurológicos no es lo indicado —
que es exactamente por qué en el motor `hepatopatia`, `shunt_sin_encefalopatia` y
`encefalopatia_hepatica` son **tres entradas distintas** con tres objetivos
distintos, y no una sola.

---

## Fascetti & Delaney 2ª ed., capítulo 18 (cardiovascular), leído entero

### F-20 · La escalera de sodio del corazón: la fuente da el número de la etapa C y confirma la nuestra

> *«one study showed that **a low-sodium diet (40 mg/100 kcal) reduced cardiac
> size** in dogs with CHF compared to a diet containing 70 mg/100 kcal (Rush et
> al. 2000). **In dogs with ACVIM Stage C, the authors recommend moderate sodium
> restriction (i.e. <80 mg/100 kcal).**»*

En nuestras unidades: el estudio comparó **400 vs 700 mg/1000 kcal** y la
recomendación de etapa C es **<800 mg/1000 kcal**. Nuestra escalera:

```
cardiopatia (genérica) ..... 739   (tope legal del Reg. (UE) 2020/354)
cardiopatia_a .............. sin tope
cardiopatia_b1 ............. sin tope
cardiopatia_b2 ............. 739
cardiopatia_c .............. 625   ← la fuente pide <800: cumplimos con margen
cardiopatia_d .............. 480   ← cerca de los 400 del estudio de Rush
```

**Las cinco encajan**, y las dos primeras encajan *por no tener tope*, que es lo
importante: Fascetti avisa expresamente de lo contrario a lo que uno haría por
instinto —

> *«**severe sodium restriction in animals with early heart disease could
> theoretically be detrimental** by early and excessive activation of the RAA
> system.»*

O sea que **no poner tope en A y B1 no es un olvido: es lo correcto**, y ahora
está escrito con su fuente. Lo que sí pide en esas etapas es *«mild sodium
restriction and the maintenance of an optimal body condition score»*, y lo
segundo ya lo cubre el DER sobre peso objetivo.

### F-21 · La DCM asociada a dieta, medida por fin en vez de argumentada

Nuestra entrada `dcm_asociada_a_dieta` no aplica ningún tope y explicaba por qué
con un argumento estructural: *legumbres y boniato nunca son la fuente principal
de kcal en un menú BARF*. Era una afirmación **sin número**. Ya lo tiene:

```
boniato en los 36 menús base ............. 0 de 36
boniato en las 180 variantes ............. 2 de 180, y el peor aporta el 6,3 % de las kcal
legumbres en el catálogo entero .......... 0 de 163 fichas
   (ni guisante, ni lenteja, ni garbanzo, ni judía, ni soja)
```

El patrón que describe la FDA —legumbres o patata **sustituyendo al cereal** como
fuente principal de energía— no es que sea improbable aquí: **no puede darse**,
porque no hay cereal que sustituir y porque los ingredientes implicados o no
están en el catálogo o no llegan al 7 % de las kcal.

Y dos cosas del capítulo que sí cambian lo que hay que **decir**:

> *«This secondary form of DCM is unique because of the **improvement in various
> echocardiographic variables and longer survival times after diet change**,
> whereas dogs with primary DCM typically have limited echocardiographic
> improvement and shorter survival times.»*

El cambio de dieta **es** el tratamiento — por eso esta patología existe en el
motor aunque no aplique ni un tope.

> *«Except in one study of golden retrievers, **plasma and whole blood taurine
> deficiency have been uncommon** in affected dogs.»*

**No es un problema de taurina** y no se arregla suplementándola, que es lo que
mucha gente hace por su cuenta. Y el mecanismo sigue sin conocerse: un estudio de
«foodomics» encontró más de 100 compuestos que diferían entre las dietas
implicadas y las tradicionales, con el guisante como el ingrediente que más los
explicaba.

### F-22 · Taurina y L-carnitina en el perro, con la matización que faltaba

> *«While taurine is an essential nutrient for cats…, **dogs are thought to be
> able to synthesize adequate amounts of taurine endogenously, so it is not
> classified as an essential nutrient for dogs**. Dog breeds at high risk for DCM
> (e.g. Doberman pinschers, boxers) typically do not have taurine deficiency.»*

Coherente con que la taurina sea en nuestro motor una fila **sin referencia** de
FEDIAF (como la fibra y el EPA) y con que solo aparezca como suelo donde una
fuente clínica lo pide: `dcm_taurina_respondedora` y `hepatopatia`.

Y de la L-carnitina, la misma prudencia que ya salía en el capítulo 9: *«**the
supporting data are not yet robust enough** to make firm recommendations for most
of these nutrients»*. Es un suelo barato y sin riesgo, pero no hay que venderlo
como más de lo que es.

---

## Fascetti & Delaney 2ª ed., capítulos 17 (endocrino) y 19 (oncología), leídos enteros

### F-23 · La fibra de la diabetes: nuestro suelo es el más bajo de todos los estudiados

El capítulo 17 repasa seis estudios de fibra en perro diabético. Las cantidades
que usaron, convertidas a nuestras unidades:

```
Nelson 1998 ..... 11 % vs 23 % de fibra total sobre materia seca  =  27,5 vs 57,5 g/1000 kcal
un estudio de 12 perros estables ....... «total fiber 50 g/1000 kcal», 90 % insoluble
Blaxter 1990 .... 20 g de salvado de trigo o de goma guar añadidos a la lata
NUESTRO SUELO EN DIABETES ..............  17,5 g/1000 kcal   (SACN5)
```

O sea que **el suelo que aplicamos está por debajo de todo lo que se ha
estudiado**. No está mal —es un SUELO, y el motor puede subir de ahí— pero
conviene saber que no es una dosis terapéutica: es el mínimo por debajo del cual
no dejamos bajar.

Y la conclusión honesta del propio capítulo, que hay que citar entera para no
vender más de lo que hay: *«Research examining the efficacy of fiber
supplementation in diabetes **has raised a number of questions, perhaps more than
it has answered**. Most controlled studies support that increasing amounts of
**insoluble** fiber may reduce the postprandial glycemic curve»*. **Insoluble** —
y nuestro catálogo tiene un solo campo `fibra` que no distingue soluble de
insoluble, que es exactamente la misma limitación que ya está anotada en
`PREGUNTAS_PARA_ELENA.md` §3 para el hierro. Es la segunda vez que la misma
carencia del catálogo aparece por otro camino.

Y el cromo, otra vez: *«no companion animal study to date has shown any
benefit»*. No lo tenemos y no hay que ponerlo.

### F-24 · El cáncer: los dos suelos que aplicamos son exactamente los de la fuente

> *«providing protein at **30-35% of total calories** will achieve this goal in
> most animals»* → a 4 kcal/g son **75-87,5 g/1000 kcal**. Nuestro suelo de
> proteína en `cancer_soporte` es **75,0**: el extremo bajo exacto.
>
> *«Most cats and dogs can tolerate as much as **60-65% of their total energy
> requirement as fat**»* → nuestro suelo de grasa (62,5 g/1000 kcal) son **≈56 %
> de las kcal**, dentro de lo tolerable y por debajo del techo que da la fuente.

Dos fuentes independientes (SACN5 Tabla 30-5 y este capítulo) dando el mismo par
de números. Eso es lo más cerca de «cerrado» que puede estar una cifra clínica.

Y el matiz que faltaba, sobre el estudio del que sale todo esto: *«Although a
high-fat ration appeared to normalize carbohydrate metabolism and prolong
survival times **in a subset of dogs with lymphoma** in one study, this diet was
also enriched with **other nutrients including n-3 fatty acids and arginine**
(Ogilvie et al. 2000)»* — o sea que el ensayo no separa la grasa del omega-3 ni
de la arginina, y por eso las tres cifras de la Tabla 30-5 van juntas. Es
coherente con que apliquemos las tres (grasa, proteína, arginina) y con que la
cuarta (omega-3 ≥12,5) se quede escrita sin aplicar porque no cabe.

### F-25 · ⚠️ Y el aviso que SÍ falta en nuestra entrada de cáncer

> *«it is also important to recognize that **a high-fat, high-protein diet is
> contraindicated in many cats and dogs with cancer**. Animals with a history of
> dietary fat intolerance should continue to have their dietary fat intake
> restricted… High-fat diets also make it more difficult to maintain optimal body
> condition in the substantial proportion of animals with cancer that are
> **overweight or obese**. Switching to a high-protein diet for a cat or dog with
> cancer that **also has concurrent and significant renal or hepatic
> insufficiency may precipitate clinical decompensation that is difficult to
> reverse**.»*

Nuestro `cancer_soporte` empuja la grasa y la proteína hacia ARRIBA. Los tres
casos en que eso está contraindicado —intolerancia a la grasa, sobrepeso, y
insuficiencia renal o hepática concurrente— son tres cruces que el motor **ya
resuelve por aritmética**: si además marcas `pancreatitis`, `obesidad`, `renal` o
`hepatopatia`, sus topes chocan con estos suelos y el BLOQUE 52 hace que se diga
cuáles. Lo que falta no es lógica: es que **el aviso de cáncer lo diga en
palabras**, porque quien marca solo «cáncer» en un perro que además está gordo no
recibe hoy ninguna advertencia.

Es información, no una decisión clínica, así que lo añado al aviso. Y también
esto, que es lo primero del capítulo: *«**A change in diet is not automatically
indicated in every cat or dog with cancer.** Each animal must be carefully and
individually evaluated, and those that are already maintaining good body
condition on a high-quality complete and balanced food… may remain on this ration
until there is an objective reason to change»*.

---

## Fascetti & Delaney 2ª ed., capítulo 16 (tracto urinario inferior), leído entero

**⚠️ Es el capítulo que más contradice lo que aplicamos hoy**, y hay que leerlo
entero antes de tocar nada, porque tres de nuestros cuatro topes de `oxalato`
apuntan en la dirección que esta fuente desaconseja.

### F-26 · El fósforo del oxalato: la fuente dice expresamente que NO se restrinja

> *«**Dietary phosphorus should not be restricted with calcium oxalate
> urolithiasis. Low dietary phosphorus is a risk factor for calcium oxalate
> urolith formation in cats and dogs** (Lekcharoensuk et al. 2000a,b, 2001,
> 2002). Reduction in dietary phosphorus may be associated with activation of
> vitamin D, which in turn promotes intestinal calcium absorption and
> hypercalciuria.»*
>
> *«Diets formulated for oxalate prevention in cats and dogs contain phosphorus
> from 0.3 to 2.1 g/Mcal. **Concentrations from approximately 1.5 to 2.0 g/Mcal
> have been recommended** (Kirk et al. 2003).»*

**Nuestro tope de `oxalato` es fósforo ≤1.500 mg/1000 kcal = 1,5 g/Mcal**, es
decir **el extremo BAJO exacto de lo recomendado** — y como es un TECHO, el
solver formula pegado a él o por debajo. Es decir: aplicamos como límite
superior lo que la fuente da como límite **inferior** de lo aconsejable.

No digo que esté mal: nuestro número sale de SACN5 y hay dos manuales que no
coinciden, igual que con la grasa de la pancreatitis. Pero **la dirección del
error importa**: aquí equivocarse por abajo no es el lado seguro, porque la
propia fuente dice que el fósforo bajo **es un factor de riesgo de la
enfermedad que estamos tratando**.

### F-27 · El sodio del oxalato: la fuente dice que el debate está abierto y que bajo puede ser peor

> *«Epidemiologic evidence suggests that **the low dietary sodium concentrations
> in cat and dog foods increase the risk** for calcium oxalate urolithiasis and
> that **diets that contain high dietary sodium concentrations decrease the
> risk**.»*
>
> *«**recommended concentrations of sodium in foods for cats and dogs predisposed
> to calcium oxalate formation is debated**, as diets containing as low as **0.4
> g/Mcal** sodium and as high as **3.5 g/Mcal** sodium are available
> commercially.»*

**Nuestro tope es 750 mg/1000 kcal = 0,75 g/Mcal**: dentro del rango comercial,
pero en su cuarto inferior. El mecanismo que da la fuente para el sodio alto es
la dilución de la orina — *«high dietary sodium chloride promotes urine dilution
in cats and dogs, and while calcium excretion increased in dogs in this study,
**the overall urinary calcium concentration decreased**, as did relative
supersaturation for calcium oxalate (Queau et al. 2020)»* — y la alternativa que
propone si el sodio alto preocupa es *«the use of a **high-moisture diet** is
generally recommended»*. Una ración BARF es de por sí una dieta de humedad alta,
así que por ese lado ya estamos donde hay que estar.

### F-28 · El magnesio: coincidimos, y por poco

> *«Studies in cats associate **low dietary magnesium with calcium oxalate
> risk**… it appears logical that **magnesium should not be highly restricted**…
> **Prudent concentrations of dietary magnesium have been suggested from 0.08 to
> 0.10 % dry matter or approximately 200 mg magnesium/Mcal**.»*

Nuestro tope de magnesio en oxalato es **375 mg/1000 kcal**, o sea **por encima**
de los 200 que sugiere la fuente: no restringe de más. Aquí no hay conflicto.

### F-29 · ⚠️ La vitamina D del oxalato: la fuente da un número, y es la MITAD del nuestro

> *«Excessive concentrations of vitamin D (which promotes intestinal absorption
> of calcium)… should be avoided. **Diets with vitamin D between 250 and 350
> IU/Mcal should suffice.**»*

250-350 UI/Mcal son **6,25-8,75 µg/1000 kcal** (1 µg = 40 UI). **Nuestro tope de
vitamina D en oxalato es 14,1875**, que es el máximo LEGAL para cualquier perro
(Reglamento (UE) 2017/1492) — o sea que en la práctica **no estamos aplicando
ningún tope específico de oxalato**: estamos aplicando el techo que ya tiene
cualquier menú.

Esta es la única de las cuatro donde el cambio iría en el **lado seguro** (bajar
un techo) y donde la fuente da una cifra concreta. Antes de aplicarla hay que
medir si sale menú, que es la lección de esta misma noche. Queda propuesto en
`PREGUNTAS_PARA_ELENA.md` §10.

### F-30 · Y tres cosas más del mismo capítulo que sí podemos usar ya

- **La proteína alta PROTEGE**, al revés que en humanos: *«a case-controlled,
  retrospective study showed that **higher protein concentration in cat and dog
  foods appeared protective against calcium oxalate uroliths**»*. Una ración BARF
  va a 130 g/1000 kcal. A favor nuestro.
- **El ácido oxálico tiene una cifra**: *«Suggested dietary concentration is **<20
  mg oxalic acid/100 g of food (dry matter basis) or about <40-45 mg oxalic
  acid/Mcal**»*. Nosotros excluimos alimentos altos en oxálico por una LISTA
  (`OXALATO_ALTO` en `seguridad.py`), no por una cifra, porque **el catálogo no
  tiene columna de ácido oxálico**. Es un dato que falta y ahora tiene número
  objetivo: va a `DATOS_QUE_FALTAN.md`.
- **Las dietas acidificantes son un factor de riesgo mayor** y el objetivo de pH
  urinario sugerido es ~7,5: *«feeding an acidifying diet or administering urinary
  acidifiers to cats and dogs at risk for calcium oxalate is **contraindicated**»*.
  El repo de fuentes ya tiene la maquinaria del KAB (balance ácido-base) y la
  ecuación de Behnsen, **sin aplicar a producción**. Este es el primer uso
  clínico concreto que le he encontrado: no es un adorno, es el factor que la
  fuente pone por delante de todos los demás en el oxalato.

---

## Fascetti & Delaney 2ª ed., capítulo 14 (piel), leído entero

### F-31 · El zinc del pelo y la piel: la dosis estudiada es CUATRO VECES nuestro suelo

> *«The combination of **zinc (100 mg/1000 kcal) and linoleic acid (15 g/1000
> kcal)** produced **statistically significant improvements in coat gloss and
> decreased TEWL** over a nine-week period in dogs (Marsh et al. 2000; NRC
> 2006).»*

Nuestro suelo de zinc en `dermatosis_zinc` es **25 mg/1000 kcal** (SACN5). La
combinación con evidencia medida es **100 de zinc + 15 g de linoleico**, y las
dos van juntas — el propio capítulo explica por qué: *«**EFA deficiency impairs
zinc absorption**»*. O sea que subir el zinc sin subir el linoleico puede no
servir de nada.

Es la primera cifra que encuentro con un ensayo controlado detrás para la piel, y
el NRC la recoge. **No la aplico**: subir un suelo cambia todos los menús de esa
patología, el linoleico de 15 g/1000 kcal es más de cinco veces el mínimo de
FEDIAF (2,8) y no sé si cabe. Va a `PREGUNTAS_PARA_ELENA.md` §10 con la propuesta
de medirlo.

Y el aviso que va con ello, del mismo capítulo: la dermatosis que responde al
zinc **se trata con zinc oral (2-3 mg/kg de peso vivo)**, no con la dieta, y
*«**zinc oxide should not be used as it is not very bioavailable**»* — que es
exactamente el tipo de detalle que decide si un suplemento del catálogo sirve o
no sirve.

### F-32 · La dieta de eliminación: lo que hay que decirle a quien la hace

Nada de esto es un número del motor, y todo es lo que hace que una dieta de
eliminación funcione o no:

> *«**There is no such thing as a “hypoallergenic diet.”**»*
>
> *«in order to diagnose CAFR in more than 90% of dogs and cats, an elimination
> diet trial should last for a **minimum of 8 weeks**, but **10-12 weeks (or
> more)** may be required.»*
>
> *«**up to 75% in one survey** of dogs will still have **instances of food
> indiscretions** during a trial, including provision of treats by the pet owner
> (dental chews, rawhides, jerky) or access to unmonitored food sources.»*
>
> *«**B vitamins (especially thiamin) can be very quickly depleted and should be
> supplemented even in the short term.**»*
>
> *«food-allergic dogs will react to the **flavored heartworm preventive**… with
> increased pruritus and increased serum IgE within days.»*
>
> *«Sometimes it is necessary to **place all animals in a house on the same
> diet** to ensure an effective trial.»*

Las seis son producto, no motor, y las seis explican por qué una dieta de
eliminación «falla» cuando en realidad no se ha hecho. La pantalla de varios
perros que ya existe hace fácil lo de la última. Va a `PENDIENTE_PRODUCTO.md`.

---

## Fascetti & Delaney 2ª ed., capítulo 11 (aparato digestivo), leído entero

### F-33 · La grasa del intestino: otra vez el 20 % de las kcal

Igual que en pancreatitis (§F-11), la referencia práctica que da esta fuente para
el aparato digestivo es **el 20 % de las kcal**, no un % de materia seca:

> *«**Low fat.** No fat-titration studies have been performed to guide firm
> recommendations. However, a pragmatic recommendation especially to promote gut
> motility would be to choose the lowest fat content available. **An almost
> arbitrary cutoff of 20% of metabolizable energy (ME) could be made.**»*
>
> *«**Dietary fiber content.** …An empirical recommendation is to select diets
> that contain **less than 8% total dietary fiber or less than 5% crude fiber**.»*

Y es honesto sobre lo que vale: *«an almost arbitrary cutoff»*. Nuestro tope de
grasa en `enteropatia_cronica` (37,5 g/1000 kcal ≈ 34 % de las kcal) está por
encima de esa referencia, exactamente igual que el de pancreatitis. Es la misma
pregunta y va en el mismo sitio: `PREGUNTAS_PARA_ELENA.md` §9.

El 8 % de fibra total sobre materia seca son **20 g/1000 kcal**, que es justo el
SUELO que aplicamos en `intestino_irritable` (SACN5 Tabla 63-3, «Crude fiber
≥8 %»). Ojo: **una fuente da ese 8 % como TECHO de fibra total y la otra como
SUELO de fibra bruta**, y son dos medidas distintas de la fibra. No es una
contradicción —fibra bruta y fibra dietética total no son lo mismo, y la bruta es
siempre menor— pero es exactamente el tipo de cruce que hay que mirar dos veces.
Nuestro catálogo mide una sola `fibra`, así que no puede distinguirlas: mismo
hueco que ya está anotado en `PREGUNTAS_PARA_ELENA.md` §3.

### F-34 · Lo que se agota en una enteropatía crónica, y que el menú no puede reponer

El capítulo enumera los déficits que aparecen en la enteropatía crónica: **B12 y
folato**, **zinc**, **magnesio**, **hierro** y **vitamina K**. Dos cosas
importantes para nosotros:

1. **La B12 no se repone con la dieta en este caso.** La fuente da la pauta y es
   inyectable o a dosis altas por boca: *«Dogs and cats are typically supplemented
   with B12 at a dose of **250 μg (cats) or 500 μg (dogs) per dose, subcutaneously
   or intramuscularly, weekly for 4-5 weeks**»*. Eso no es un menú: es una
   prescripción. Nuestro aviso de `enteropatia_cronica` debería decirlo, porque un
   dueño que ve el menú «completo y equilibrado» puede pensar que ya está cubierto
   — y el propio capítulo dice que *«la respuesta al tratamiento puede ser limitada
   hasta que se corrige»*.
2. **El zinc sí tiene efecto medido**: *«In a study of CD patients with increased
   intestinal permeability, daily oral zinc supplementation **improved symptoms and
   normalized the permeability in 80% of cases**»*. Es humano (enfermedad de
   Crohn), así que no se convierte en un suelo, pero explica por qué el zinc
   aparece en tantas tablas.

### F-35 · Y la mejor noticia del capítulo para lo que hacemos

> *«dietary therapy can be **extremely successful even as the sole therapy** in
> some cases… In a report of 13 dogs with lymphocytic-plasmacytic colitis,
> **clinical signs resolved in all 13** with the introduction of an elimination
> diet… **hydrolyzed and elimination diets were equally successful**.»*

Y algo que cambia el consejo que se le da al dueño: *«Interestingly, **31 of 39
dogs showed no recurrence of clinical signs when switched back to their original
diet**»*. O sea que en la enteropatía que responde a la comida, la dieta de
eliminación puede no ser para siempre. Eso es lo contrario de lo que se suele
contar, y es información que quien paga un menú a medida merece tener.

---

## Fascetti & Delaney 2ª ed., capítulo 2 (nutrición básica), leído entero

### F-36 · La frase que valida los TRES campos de `sin_dato`, `dato_dudoso` y `cero_verificado`

Es la mejor confirmación de una decisión de diseño que he encontrado en toda la
noche, y viene de un capítulo introductorio:

> *«These programs rely heavily on reference databases like that of the USDA…
> However, **certain nutrients of interest such as taurine, chloride, iodine, and
> vitamin D are typically or often not available. Therefore, “deficiencies” in
> these nutrients suggested by computer analysis when compared to reported
> nutrient requirements for dogs and cats may be the result of a LACK OF
> AVAILABLE DATA RATHER THAN A REAL DEFICIENCY** (this can also be true of
> choline, which is not routinely reported by USDA).»*

Es literalmente el problema que resuelven los tres campos del catálogo: un 0 que
puede ser «no lo tiene» o «no lo sabemos», y que sin separarlos se convierte en
un hueco mudo. Y **nombra los mismos nutrientes**: yodo y colina son justo dos de
los huecos que `Bases.md` explica (BEDCA trae yodo pero ni un aminoácido; USDA
trae los aminoácidos y la colina pero no publica yodo).

O sea que el problema no es del catálogo de Rawku: **es de las bases de datos**, y
lo tiene cualquiera que formule con ellas. La diferencia es que nosotros lo
decimos por ficha en vez de dejar que salga como una deficiencia falsa.

### F-37 · Y la que valida el escalado de mínimos, por si quedaba duda

> *«The NRC also uses an additional unit not used by AAFCO: **amount per kilogram
> body weight raised to the three-quarter power** (i.e. amt/kg BW^0.75), which is
> more analogous to the “dosing” of medications… **when a very low energy intake
> is expected or suggested, this third method may be used.**»*

Es exactamente la ecuación 7.2.5 de FEDIAF que aplica `minimo_de()`, y el caso de
uso que da —**consumo de energía muy bajo**— es el perro a dieta, que es el que
casi se queda sin menú cuando se puso el techo de fósforo del adulto sano (ver
`motor/recomendaciones.py`). Dos fuentes, el mismo mecanismo, el mismo motivo.

### F-38 · La dosis terapéutica de omega-3 por peso metabólico, y que encaja con la nuestra

> *«Recommended amounts of EPA plus DHA use MBW multiplied by **factors ranging
> from 115 to 310**… These recommendations are intended as a starting point for
> therapy under veterinary supervision and are **below the canine safe upper
> limit**.»* (mg de EPA+DHA al día, MBW = kg^0,75; Bauer 2011.)

Para un perro de 20 kg (kg^0,75 = 9,46) eso son **1.088 a 2.932 mg de EPA+DHA al
día**. Con un DER de 1.000 kcal, **1,09 a 2,93 g/1000 kcal**. Nuestro suelo de
EPA en artrosis (1,0 g/1000 kcal) cae justo en el borde bajo de esa horquilla, y
el de omega-3 totales del renal (1,0) también. Tercera fuente independiente que
apunta al mismo sitio.

Y el aviso que la acompaña, que es el que hay que tener presente cuando alguien
lee la etiqueta de un aceite de salmón: *«omega-3 dosages indicated on **product
labels** are those suggested for **health maintenance of normal animals**… These
amounts may be sufficient to help alleviate low-level inflammatory states»* — o
sea que la dosis de la etiqueta **no es la dosis terapéutica**, y la diferencia
es de dos a tres veces.

---

## Fascetti & Delaney 2ª ed., capítulo 3 (requisitos de energía) — ⚠️ LA FUENTE QUE FIGURABA COMO PENDIENTE, Y YA NO LO ESTÁ

`LECTURAS_PENDIENTES.md` del repo de fuentes tenía **una sola entrada viva** en
prioridad 1, y era esta:

> *«Fascetti & Delaney 2ª ed., capítulo 3 ("Determining Energy Requirements") —
> Vía Perlego, con la suscripción de la usuaria, **requiere su cuenta, no es
> accesible por red pública** — Los factores energéticos citados en §3.6 y §3.8
> del inventario.»*

**El capítulo está descargado en el repo** (`fascetti/cap03.txt`, con su
cabecera `URL: https://ereader.perlego.com`). Leído entero el 9 de septiembre.
Estos son sus números, que es lo que se pedía verificar:

### F-39 · Los coeficientes, en la misma unidad que usamos nosotros

**Tabla 3.1** (perro adulto, kcal/día, todos sobre kg de peso vivo^0,75):

```
RER  (energía en reposo) .................  70 × kg^0,75
MER  perro activo de compañía o de perrera  130 × kg^0,75
MER  adulto joven activo .................. 140 × kg^0,75
MER  perro inactivo .......................  95 × kg^0,75
MER  perro mayor activo ................... 105 × kg^0,75
```

**Y los factores del método americano** (Box 3.1, perro):

```
adulto castrado ......... 1,6 × RER      pérdida de peso .... 1,0 × RER
adulto entero ........... 1,8 × RER      cuidados críticos .. 1,0 × RER
inactivo / propenso ..... 1,2-1,4 × RER  ganar peso ......... 1,2-1,8 × RER
trabajo ligero .......... 1,6-2,0 × RER
trabajo moderado ........ 2,0-5,0 × RER
trabajo duro ............ 5,0-11,0 × RER
```

### F-40 · Cómo encajan con lo nuestro, y la única discrepancia que importa

`der.py` (y `src/der.js` en la app, que es el que manda) usa el **método europeo**
de FEDIAF: un coeficiente por nivel de actividad, multiplicado por kg^0,75. Los
nuestros y los suyos, uno al lado del otro:

| | nuestro (FEDIAF) | Fascetti (Tabla 3.1) |
|---|---|---|
| perro sedentario / inactivo | **95** | **95** ← coinciden exactamente |
| perro normal | 110 | 130 («active pet dog») |
| perro activo | 125 | 140 («active young adult») |
| perro mayor | — (se usa el de su actividad) | 105 |

El **95 del perro inactivo es idéntico**, que es la mejor señal de que las dos
escalas hablan de lo mismo. Los otros dos son más altos en la americana, y eso ya
está explicado dentro de `der.py`: las dos escuelas no son intercambiables y el
proyecto eligió la europea a propósito (FEDIAF es la fuente primaria). **No hay
nada que cambiar**; lo que había que hacer era poder afirmarlo, y ahora se puede.

**⚠️ La discrepancia que sí hay que mirar es la pérdida de peso**, y son tres
cifras distintas de tres sitios:

```
Fascetti cap.3 (Box 3.1) ..... pérdida de peso = 1,0 × RER
Fascetti cap.9 ............... restringir al 60-70 % del MER del peso ACTUAL
AAHA 2021 (lo que usamos) .... 0,8 × RER sobre el peso OBJETIVO
```

No se contradicen del todo —cada una se expresa sobre una base distinta, y
`HALLAZGOS §F-8` ya lo desmenuza— pero **son tres bases distintas para el mismo
número**, y es exactamente el tipo de cifra que alguien copia de un libro a un
campo sin mirar sobre qué se calcula. Lo que nos protege de eso es
`der_casos.json`: 100 casos con su esperado, el mismo archivo en los dos repos, y
dos pruebas que lo vigilan (BLOQUE 23 aquí, `der-contrato.spec.js` allí).

### F-41 · Y la frase con la que empieza el capítulo, que conviene tener escrita

> *«It should be stressed that **predicted energy requirements should be viewed
> as an “educated guess”** at the animal's true energy requirement. These
> equations should be used as a tool to provide **a starting point** for selecting
> the amount of food to give an animal, and **adjustments should be made based on
> any observed changes in body weight**.»*

Lo dice el autor del capítulo que da las ecuaciones. Todo el motor cuelga del
DER —de él salen los gramos y contra él se escalan los 43 mínimos—, así que
merece estar dicho en la app con estas palabras: el número de partida es una
estimación, y lo que manda es el peso del perro dentro de un mes.

---

## Fascetti & Delaney: los capítulos restantes (1, 4, 5, 6, 20 y 21), leídos

Los seis se han leído enteros. Cuatro no tocan nada del motor y hay que decirlo
igual, para que quede constancia de que se leyeron y no de que se saltaron:

- **Cap.1 (integrar la nutrición en la clínica)** y **cap.5 (regulación de
  alimentos y suplementos)** son de gestión de clínica y de derecho **de Estados
  Unidos** (FFDCA, DSHEA, AAFCO, NASC). Nuestro marco es europeo —Reglamento (UE)
  2020/354 y FEDIAF—, que ya está leído y aplicado. Lo único trasladable del
  cap.5: *«a product represented to be a vitamin or mineral supplement **must
  provide guarantees for each and every added vitamin and/or mineral**»*, que es
  la razón por la que las fichas de suplemento del catálogo declaran valor a
  valor y no un «complejo vitamínico» genérico.
- **Cap.20 (nutrición enteral y sondas)** y **cap.21 (nutrición parenteral)** son
  el perro hospitalizado que no come. El motor no formula para sonda y no debe:
  una ración BARF no pasa por una sonda. No hay nada que aplicar.

Los otros dos sí dejan algo:

### F-42 · Cap.4: el rango real del perro de compañía es de 1 a 4

Tabla 4.1, gasto energético medido en perros libres, en **kcal ME/kg^0,75**:

```
metabolismo basal ..................  76 (48-114)
perro de COMPAÑÍA .................. (50-200)   ← el rango entero
perros de laboratorio con carrera .. 130 (80-170)
galgos de carreras ................. 140 (120-160)
perros de caza ..................... 240 (200-280)
perros de trineo en carrera larga .. 1050 (860-1240)
```

Nuestros coeficientes de actividad (95 sedentario · 110 normal · 125 activo ·
150-175 muy activo) caen todos dentro del rango del perro de compañía. Pero el
dato que importa es **la anchura**: entre el perro de compañía menos activo y el
más activo hay un factor de **cuatro**. Eso es lo que hay detrás de la frase del
cap.3 —el DER es «an educated guess»— y es el mejor argumento para que la app
insista en pesar al perro al mes y ajustar.

### F-43 · Cap.6: el ejemplo que explica por qué TODO el motor va por 1000 kcal

El Box 6.1 pone el caso con números, y es exactamente la trampa que
`UNIDADES.md` avisa, un piso más arriba:

> Alimento A: 3.000 kcal/kg, 10 % humedad, **1,0 % de calcio**.
> Alimento B: 4.750 kcal/kg, 10 % humedad, **1,1 % de calcio**.
>
> Mirando la materia seca, B parece tener más calcio. Por energía, **el perro que
> come B ingiere un 30 % MENOS de calcio**, porque necesita mucha menos cantidad
> de alimento para cubrir sus kcal.

*«This means that the patient eating the second food will consume 30% less
calcium… If the practitioner had just looked at the information on a dry matter
basis, they would have thought that the patient was getting **less** calcium.»*

Es la justificación, escrita por otro, de que **los 43 requisitos, los topes de
patología, los de seguridad y los condicionales vayan todos por 1000 kcal** y de
que el puente `%MS × 2,5` lleve siempre escrito el supuesto de 4000 kcal/kg de
materia seca. Un número de nutriente sin su base energética no significa nada, y
este ejemplo lo demuestra al revés de lo que uno esperaría.

---

# RESUMEN DE LA LECTURA DE FASCETTI & DELANEY (9 de septiembre de 2026)

**Los 21 capítulos, enteros.** Lo que ha salido, ordenado por lo que hay que
hacer con ello:

**Un cambio grande, medido y sin aplicar** (necesita tu decisión):
- **§F-1 / PREGUNTAS §8** — el calcio de los cachorros de raza grande. Formulamos
  a 1,80 % MS (el techo de FEDIAF) y la fuente pide **≤1,1 %**. Medido: a 1,1 %
  **salen los cuatro cachorros de prueba en el peldaño estricto**, y a 1,0 % ya no
  sale ninguno. Es la más importante de la noche.

**Cuatro cifras más de fuente que no aplicamos** (PREGUNTAS §10): la vitamina D
del oxalato (la fuente da la mitad de nuestro techo), el fósforo del oxalato (la
fuente dice que NO se restrinja y nosotros lo restringimos), el sodio del oxalato
(debate abierto) y el zinc+linoleico de la piel (la dosis con ensayo es 4× la
nuestra).

**Una contradicción entre manuales, sin resolver** (PREGUNTAS §9): la grasa de la
pancreatitis y del intestino — SACN5 da 37,5 g/1000 kcal, Fascetti y Merck dan
≈20-22. Y con ella, la pregunta de fondo: **qué manda cuando dos manuales no
coinciden**, que la regla de fuentes del proyecto no cubre.

**Seis confirmaciones de cosas que ya hacíamos** (§F-4, F-12, F-17, F-19, F-20,
F-24, F-36, F-37, F-39): el fósforo renal con su cifra de supervivencia, la
estrategia del cobre, la escalera de sodio cardíaca, los dos suelos del cáncer,
el escalado de mínimos, los tres campos de procedencia de los datos, y los
coeficientes de energía.

**Una medida que faltaba y ya está** (§F-21): la DCM asociada a dieta. El
argumento estructural que sostenía esa entrada era una afirmación sin número;
ahora son 2 de 216 menús con boniato, 6,3 % de las kcal en el peor, y cero
legumbres en las 163 fichas.

**Una fuente que figuraba como pendiente y ya no lo está** (§F-39): el capítulo 3
de Fascetti, el único que quedaba vivo en `LECTURAS_PENDIENTES.md`.

**Y tres cosas de producto** (`PENDIENTE_PRODUCTO.md` §7): el «diet drift» (a los
pocos años solo el 13 % sigue la receta), que el dueño puntúa mal la condición
corporal, y lo que la fuente dice del crudo — que hay que decir entero, porque la
citamos para lo demás.

---

## ⚠️ UN FALLO DEL MOTOR, ENCONTRADO POR LA BATERÍA A LAS TANTAS: el solver resolvía un problema y entregaba otro

**No viene de leer ninguna fuente. Lo cazó el BLOQUE 49**, y explica DOS fallos
que parecían distintos.

### El síntoma

```
BLOQUE49: 1 menú sale del solver con el YODO al 96 % del mínimo  (perro de 4,5 kg, DER 400)
BLOQUE49: 3 de 20 menús de perros pequeños no salen o no están verdes
BLOQUE61: «oxalato» está marcada formulable y NO da menú para el perro de referencia
```

Los tres son el mismo fallo.

### La causa

La línea que recoge la solución del MILP es, desde el 5 de agosto:

```python
gramos = {n: round(x[idx[n]], 2) for n in nombres if x[idx[n]] > 0.02}
```

El umbral está **bien puesto**: 18 mg no los pesa nadie, y ese mismo día se bajó
de 0,5 g a 0,02 porque el yoduro potásico funciona en fracciones de gramo. Lo que
estaba mal es que **el solver no lo sabía**. Podía poner **0,0185 g** de una
fuente concentrada, darse por satisfecho, y la entrega tiraba ese aporte.

Con **76.000 µg de yodo/100 g** (harina de algas) o **80.000** (yoduro potásico),
0,0185 g son **14 µg**. En un perro de 4,5 kg el mínimo de yodo son 120 µg: ese
descarte silencioso se lleva el **12 % del requisito**. En un perro de 30 kg el
mismo descarte absoluto es el 1,7 % y no se nota — por eso solo salía en los
pequeños, que es exactamente el mismo disfraz con el que se presentaba el
problema del redondeo, y por eso se confundían.

**Y explica también el de oxalato**, que parecía otra cosa: al tirar unos gramos,
el menú entregado tiene **menos kcal** que el que resolvió el solver, y menos
kcal con el mismo nutriente es **más concentración**. Un techo de patología que
cabía por poco deja de caber, `_garantizar_verificado` lo rechaza (regla 1
funcionando) y la usuaria se queda sin menú. Es la misma aritmética que ya está
escrita en la regla 2 del `CLAUDE.md` —los topes se miden sobre las kcal REALES—
vista desde el otro lado.

### El arreglo

Que el solver tenga **prohibido usar menos de lo que sobrevive a la entrega**:

```
SUELO_ENTREGABLE_G = 0.03      (nuevo, en el bloque de suelos)
UMBRAL_DE_ENTREGA_G = 0.02     (el de siempre, ahora con nombre)
```

Los suplementos siguen exentos del suelo de 1 g —no se pesan, se dosifican— pero
no del de 0,03. Y los dos números **solo valen juntos**: el BLOQUE 49 los lee del
código y falla si alguien invierte la pareja.

**Medido, los mismos 20 menús de perros de 1,5 a 4,5 kg:**

```
                    menús caídos   yodo mínimo   mediana
antes                    3             96 %       112 %
después                  0            107 %       117 %
```

Y `oxalato`, que fallaba, sale ahora **6 de 6 veces en el peldaño estricto**.

### La lección, que es la de siempre pero por un sitio nuevo

Los dos números —el que usa el solver y el que usa la entrega— describían la
misma frontera y **no se hablaban**. Es la familia de la tabla de patologías
duplicada, la de la fibra entre el motor y el analizador, y la del denominador
del BLOQUE 25 que también se ha arreglado esta noche: **dos sitios que calculan
lo mismo acaban discrepando siempre**. La única defensa que funciona es que uno
lea al otro, o que una prueba los compare.

Y una segunda: **el fallo llevaba puesto desde el 5 de agosto** y la batería lo
tocaba desde el 28 pensando que era otra cosa (el redondeo). Lo que lo separó no
fue leer el código: fue que el BLOQUE 61 —la comprobación nueva, la de «cada
patología formulable formula de verdad»— fallara **al mismo tiempo** y por lo
que parecía otro motivo. Dos síntomas distintos de la misma causa se reconocen
antes que uno solo.

---

## ⚠️ Y UN SEGUNDO FALLO DEL MOTOR, DE LA MISMA FAMILIA: el techo se comprobaba con un número y se medía con otro

Lo cazó el **BLOQUE 61**, el testigo nuevo, y solo porque falla **una vez de cada
siete** — con una sola tirada la prueba pasa y el fallo parece un fantasma.

### El síntoma

```
BLOQUE61: «oxalato» está marcada formulable y NO da menú para el perro de referencia
   motivo: «El menú que salía se pasa de los límites de la patología de este perro»
```

Medido con 20 semillas: **3 de 20 menús de oxalato salían con la vitamina D a
14,6 contra su tope de 14,2** y `_garantizar_verificado` los tiraba. La regla 1
funcionando — y la usuaria sin menú, una vez de cada siete, sin patrón visible.

### La causa

El motor pone **dos filas** por cada techo, y con motivo (está escrito ahí desde
el 21 de agosto): una **absoluta**, sobre las kcal pedidas, y otra **relativa**,
sobre las kcal reales — porque el menú puede salir un 3 % por debajo y menos
kcal con el mismo nutriente es más concentración.

Las dos filas usaban **vectores distintos**:

```
fila absoluta ..... fila_techo  = el valor declarado CON EL HUECO IMPUTADO a su familia
fila relativa ..... valor_nutriente()  = el valor DECLARADO a secas
```

Y `_tope_patologia_roto` —el filtro que decide si el menú se entrega— mide como
la **absoluta**, imputando. En el menú que fallaba, la vitamina D **declarada**
era 8,4 µg/1000 kcal y la **imputada** 14,6: varios alimentos tenían el dato
vacío. El solver comprobaba su techo contra 8,4, lo daba por bueno, y el filtro
lo medía contra 14,6 y lo tiraba.

**No es un caso raro de la vitamina D.** Le pasa a **cualquier tope de patología
cuyo nutriente tenga huecos en el catálogo**, que son casi todos. Que solo se
viera en el oxalato es porque su techo de vitamina D es el más apretado que hay
(14,1875, el máximo legal) y porque la vitamina D es de los nutrientes con más
huecos.

### El arreglo, y por qué es una línea

La fila relativa se construye ahora **a partir de la absoluta** en vez de repetir
la cuenta:

```python
v_nut = fila_techo[idx[n]]      # ya es valor/100, con el hueco imputado
```

**Medido:** oxalato pasa de **3 de 20** menús con el tope roto a **0 de 20**.

Y lo vigila el BLOQUE 13 con una comprobación nueva que prueba **doce semillas**
por combinación de patologías (oxalato, renal, hepatopatía, y renal+cardiopatía),
porque con una sola tirada este fallo se esconde.

### Tres veces la misma familia en una noche

```
· el denominador del BLOQUE 25 ..... la prueba sumaba cinco categorías y el motor seis
· SUELO_ENTREGABLE_G .............. el solver planificaba 0,0185 g y la entrega los tiraba
· fila_techo vs valor_nutriente ... el solver comprobaba declarado y el filtro imputado
```

Los tres son **dos sitios que calculan lo mismo de dos maneras**, que es
exactamente lo que ya había pasado con la tabla de patologías duplicada del
`POST /menu`, con la fibra entre el motor y el analizador, y con los suelos de
patología el 8 de septiembre. No es mala suerte: es la forma que tiene este
motor de romperse. **La única defensa que funciona es que uno lea al otro** — que
es lo que se ha hecho en los tres — o que una prueba los compare.

Y una segunda lección, sobre las pruebas: los tres fallos se han encontrado en
la misma noche porque el **BLOQUE 61** empezó a fallar. Ninguno de los tres se
manifestaba como un número raro; los tres se manifestaban como **«no hay menú»**,
que hasta hoy no lo miraba nadie.

---

## ⚠️ APLICADO EL 9 DE SEPTIEMBRE: EL TECHO DE CALCIO DEL CACHORRO DE RAZA GRANDE

Era el hallazgo más urgente de toda la lectura de fuentes, y aquí está aplicado
con la medida al lado.

### Lo que decía el motor hasta hoy

Un cachorro de raza grande recibía el calcio que le permite FEDIAF, y nada más.
Medido por la vía de la API, en el peldaño estricto, antes de tocar nada:

| perro | calcio mg/1000 kcal | % materia seca |
|---|---|---|
| labrador (32 kg de adulto), 15 kg, DER 1300 | 4489 | 1,80 % |
| gran danés (55 kg), 25 kg, DER 2000 | 4500 | 1,80 % |
| gran danés temprano (55 kg), 12 kg, DER 1400 | 3750 | 1,50 % |
| pastor alemán (35 kg), 18 kg, DER 1500 | 4054 | 1,62 % |

Los cuatro **en verde**, porque 4500 es exactamente el máximo de FEDIAF para
crecimiento tardío. El semáforo no tenía nada que decir.

### Lo que dicen las fuentes

Las dos que hablan de esto, y las dos son caninas y específicas:

- **SACN5 cap.17, Tabla 17-1** («Key nutritional factors for foods for growing
  puppies») parte sus columnas en 25 kg de peso adulto esperado, y a la de
  «>25 kg» le da **«Calcium (%) 0.8-1.2»** y **«Phosphorus (%) 0.6-1.1»**. La
  columna de «<25 kg» dice 0,7-1,7 y 0,6-1,3.
- **SACN5 cap.33, Tabla 33-5** («Key nutritional factors for foods for growth
  (postweaning) of large- and giant-breed puppies») repite **«Calcium 0.8 to
  1.2 %»**, y el propio capítulo define la población: *«To help prevent DOD in
  large- and giant-breed puppies (>25 kg adult weight)»*.
- **Fascetti & Delaney cap.10** aprieta el techo, literal: *«In order to prevent
  panosteitis, a diet designed for young dogs of large breeds with a calcium
  content no greater than 1.1% dm should be fed during the growth period,
  starting at partial weaning»*.

Se aplica **1,1 %**, que es el más estricto de los dos y cae dentro del rango
del otro: 1,1 × 2500 = **2750 mg/1000 kcal**. O sea que el motor estaba dando
un **64 % más de calcio** del que recomiendan sus propias fuentes al perro al
que más le importa.

Y no es un número feo en una ficha. El cachorro de raza grande **no regula su
absorción de calcio como el adulto**; el exceso da enfermedad ortopédica del
desarrollo. SACN5 cap.33 trae la Figura 33-6: dos hermanos de camada de gran
danés, uno alimentado con 1,1 % de calcio y otro con 3,3 %, y el segundo con
crecimiento pobre y deformidad angular de los miembros.

### El fósforo del cachorro no tenía techo NINGUNO

Al transcribir la Tabla 17-1 salió lo segundo: **FEDIAF no da máximo de fósforo
en crecimiento**. Las columnas `maxCachorroJoven` y `maxCachorroCrecimiento` de
esa fila están vacías, y está comprobado contra el PDF (la nota de auditoría de
esa fila lo cuenta: el máximo de adulto, 4000, se llegó a borrar por error el 7
de septiembre y se devolvió el 8).

**Y aquí el hueco es de verdad, a diferencia del adulto**, que es un matiz que
conviene no perder: el adulto **sí tiene máximo de FEDIAF** (4,00 g/1000 kcal), y
lo que se le añadió el 8 de septiembre fue la **recomendación del libro**, que es
la mitad. El cachorro no tenía **ninguno de los dos**. La Tabla 17-1 es el único
número canino con fuente que existe
para taparlo: **3250** al cachorro de menos de 25 kg de adulto, **2750** al de
más.

### Dos umbrales de «raza grande», y no son el mismo número

- **15 kg** (`RAZA_GRANDE_O_GIGANTE_KG`) es el corte de las notas a y b de la
  Tabla III-3b de FEDIAF: decide el mínimo de calcio reforzado (2500) y el
  techo del ratio Ca:P (1,6).
- **25 kg** es el corte de SACN5 para la enfermedad ortopédica del desarrollo.

Dos fuentes, dos poblaciones, dos números. Unificarlos sería inventarse uno de
los dos, así que cada uno vive donde vive su fuente y hay un comentario en
`motor/recomendaciones.py` para que nadie los «arregle».

### Medido después de aplicarlo

Veinte cachorros de raza grande y gigante (Grande 32 kg y Gigante 55 kg de
adulto, crecimiento temprano y tardío) por cinco configuraciones cada uno (sin
exclusiones, sin pollo, sin hueso carnoso, sin pescado ni cerdo, sin vacuno):

    SIN MENÚ ............ 0 de 20
    peldaño ............. estricto los 20 (sin soltar ni una proporción de BARF)
    calcio .............. 2463 a 2748 (1,0 a 1,1 % MS), techo 2750
    fósforo ............. 1839 a 2708, techo 2750

Y ocho cachorros más, mezclando tamaños, para ver la otra columna: el beagle
(18 kg de adulto) sale a 4187 de calcio y **3247 de fósforo**, contra su techo
de 3250. O sea que el techo del cachorro pequeño también aprieta de verdad: no
es una fila decorativa.

### Y un tercer fallo del motor, destapado por esto

Los dos primeros fallos de esta familia están más arriba en este documento. Este
es el tercero en dos días, y es literalmente el mismo: **dos sitios que calculan
lo mismo de dos maneras**.

El mínimo de calcio reforzado de la raza grande (2500) lo exigía el solver
contra las **kcal pedidas**, y lo comprobaba `_minimo_calcio_raza_grande_roto`
contra las **kcal reales** del menú. Como la tolerancia permite salirse un 3 %,
un menú de 2400 kcal pedidas que sale a 2472 reales con 6000 mg de calcio da
2500 por un lado y 2427 por el otro.

Antes de hoy no se notaba porque el calcio de una dieta con hueso iba sobradísimo
(2618-4500 medido el 7 de septiembre) y nunca se apoyaba en su suelo. En cuanto
el techo del libro lo baja a 2750, la ventana pasa a ser del 10 % y un desalineo
del 3 % deja de ser teoría: **2 de cada 20 cachorros de raza grande se quedaban
sin menú**, con el mensaje «se queda corto de calcio para un cachorro de raza
grande» — el solver construyendo un menú que el filtro final tiraba.

Arreglado igual que los otros dos: el suelo tiene ahora su fila relativa sobre
las kcal reales, la misma que ya tenían los suelos de patología. Después del
arreglo, 20 de 20.

### Y una cosa más, que también estaba mal y no daba error

`regenerar_catalogo.py` **no le pasaba al motor el peso adulto esperado**, así
que regeneraba los 216 menús del catálogo midiendo el calcio de un cachorro de
gran danés contra el techo del yorkshire. Es exactamente el fallo que el propio
docstring de ese archivo cuenta que ya pasó una vez con `margenes_categoria`. El
peso adulto de cada tamaño se lee ahora del propio catálogo (la entrada
`<tamaño>_Adulto`) en vez de escribirse a mano, para que no haya una segunda
copia de esos seis números.

---

## LO QUE SALIÓ DE VOLVER A LAS FUENTES CON LAS PREGUNTAS EN LA MANO (9 de septiembre)

Elena lo dijo así: *«las que no se pueden resolver con documentación, busca otra
documentación que las pueda resolver, que ya hemos visto más de una vez que no
has mirado bien»*. Tenía razón. **Cuatro de las preguntas abiertas tenían la
respuesta escrita en una fuente que ya estaba en el repo.**

### 1 · El factor del β-caroteno para el perro SÍ está definido, y lo da FEDIAF

Yo había escrito que no existía, apoyándome solo en el NRC 2006 (*«a retinol
equivalency has not been defined»*). **FEDIAF 2025, Tabla VII-14**, trae la fila
con nombre y apellidos:

> Provitamin A (β-carotene) **(dogs)** — 1.0 mg = **833 IU**

Con el retinol a 0,3 µg = 1 IU en la misma tabla, eso son **1 mg de β-caroteno =
250 µg de equivalentes de retinol**: factor **4 a 1**, más generoso que el 6:1
europeo y el 12:1 americano.

Las dos frases conviven —el NRC habla de que no hay estudio de equivalencia,
FEDIAF publica un factor reglamentario— pero la conclusión cambia entera: **ya no
es una pregunta de criterio, es un dato que falta.** Las fichas están calculadas
con factores ajenos, así que una con ÷6 declara un 33 % menos de lo que FEDIAF le
contaría al perro, y una con RAE, un 67 % menos. Hacen falta dos columnas,
`retinol` y `betacaroteno`. Escrito en `UNIDADES.md` y `DATOS_QUE_FALTAN.md`.

### 2 · El techo de yodo: FEDIAF ya evaluó el estudio del que sale nuestro número

La pregunta era si bajar el techo de 1.275 µg/1000 kcal, porque está a un 9 % de
la dosis que hizo daño en el estudio de Castillo 2001. **FEDIAF 2025 §3.3.1
«Iodine» habla de ese estudio exacto:**

> *«…in these studies **puppies were significantly overfed** (approx. 75 % above
> energy requirement)… the food was **deficient in a number of key nutrients**,
> e.g. Ca, P and K… Consequently, **these results are irrelevant** for normal
> commercial nutritionally balanced foods, and **the existing legal maximum is
> safe for all dogs**.»*

El máximo legal son 2.750. Nuestro 1.275 es **2,2 veces más estricto** que lo que
FEDIAF considera seguro y no cuesta ni un menú. **No se toca**, y ahora hay un
motivo escrito en vez de una pregunta abierta.

### 3 · La metionina en hepatopatía: no hay techo que poner, hay una exclusión

El NRC contaba el experimento de Merino 1975 (1 g/kg cada 4 h provocó signos de
coma hepático en perros con shunt portocava). **SACN5 cap.68 dice dos cosas que
cambian la pregunta:** que esa vía *«does not play an important role in the
pathogenesis of HE»* porque los métodos antiguos la sobrevaloraron, y que lo que
hay que hacer es *«do not administer… **methionine-containing products**»*.

O sea: **una regla de exclusión de suplementos, no un límite por nutriente.** Hoy
no hay nada que excluir porque el catálogo no tiene ficha de L-metionina; el día
que entre, `hepatopatia` tiene que excluirla, y está escrito.

### 4 · El ratio omega-6:omega-3, que es lo que preguntó Cris

**Para el perro sano no existe en ninguna fuente que tengamos**, y el NRC 2006
dice literalmente que el ratio de totales *«is not helpful»*, recomendando en su
lugar el **linoleico:linolénico** — que el motor ya aplica desde hoy.

**Para las patologías sí existe**, y SACN5 lo dice en cuatro sitios:

| patología | ratio | dónde |
|---|---|---|
| Enfermedad renal crónica | 1:1 a 7:1 | cap.37 |
| Cáncer | «approximating 1:1» | cap.30 |
| Artrosis | **menos de 1:1** | cap.34 |
| Reacción adversa al alimento | *«currently unknown»* | cap.31 |

Los tres primeros quedan escritos en `patologias.json` como
`limites_escritos_que_el_solver_no_aplica`, con el mismo motivo que ya tenía el
de la renal: dos fuentes que se contradicen, y eso lo decide un clínico. El
cuarto es un no-número de la propia fuente, que también se escribe.

### 5 · La grasa en pancreatitis son DOS cifras — y ya estaban las dos puestas

SACN5 cap.67, literal: *«Obese and hypertriglyceridemic patients recovering from
pancreatitis should receive low-fat foods (**≤10** … % DM for dog…). Other
patients can be fed moderate-fat foods (**≤15** … % DM for dog…)»*. Para el
perro: **25 g/1000 kcal** si es obeso o hipertrigliceridémico, **37,5** si no.

Lo apunté como hallazgo y **estaba equivocado**: el 8 de septiembre ya se
implementó, incluido el mecanismo que hacía falta
(`topes_por_1000kcal_si_ademas`, que condiciona un tope a que otra patología
esté marcada). Está en `PATOLOGIAS.md` §1.5 con su tabla:

| combinación | grasa aplicada |
|---|---|
| pancreatitis sola | 37,5 |
| pancreatitis + obesidad | **25** |
| pancreatitis + hiperlipidemia | **25** |
| obesidad sola | 30 |

**Lo dejo escrito porque el error es la lección**: llegué a poner la cifra en
`limites_escritos_que_el_solver_no_aplica` diciendo «el motor no tiene ese
mecanismo», y lo tiene desde ayer. Miré `topes_por_1000kcal` y `suelos_…` y no
`topes_por_1000kcal_si_ademas`. Un hallazgo que no se contrasta contra lo que ya
hay no es un hallazgo: es trabajo repetido, y del que ensucia el JSON.

### 6 · Y el changelog de FEDIAF, leído entero (2011 → 2025)

Los trece apartados de «Adaptations in the Nutritional Guidelines», que era lo
que quedaba pendiente de FEDIAF. **No hay nada que aplicar**, y eso también es un
resultado: nuestra tabla ya recoge los cambios que importan. Comprobado uno a
uno contra `requerimientos_v2_final.json`:

| cambio del changelog | lo que tenemos |
|---|---|
| 2013: se borra el máximo NUTRICIONAL de zinc | tenemos 56,75, que es el **legal** |
| 2016: se borran los máximos nutricionales de sodio y cloruro para perro, y se sustituyen por una nota de niveles seguros | tenemos 3.750 y 5.870, que salen de esa nota (1,5 % y 2,35 % MS) |
| 2016: potasio de crecimiento tardío corregido a 1,10 g/1000 kcal | tenemos 1.100 mg |
| 2017: máximo legal de zinc a 22,70 mg/100 g MS | 22,70 ÷ 4 × 10 = **56,75** ✓ |
| 2018: colina de crecimiento temprano de 209 a 170 mg/100 g MS | tenemos **425** = 1.700 ÷ 4 ✓ |
| 2019: máximo legal de hierro a 68,18 mg/100 g MS | tenemos **170,45** = 68,18 × 10 ÷ 4 ✓ |
| 2025 vs 2024 | **solo editorial**: encabezados de tablas, símbolos matemáticos y espacios |

Y las secciones 5 y 6 de FEDIAF, que también estaban sin leer, son **métodos
analíticos** (referencias AOAC/USP por nutriente) y **protocolos de ensayo de
digestibilidad**. No fijan ningún requisito. Lo único aprovechable: FEDIAF
distingue **fibra dietética total, insoluble y soluble** como tres analitos con
método propio, así que «soluble vs insoluble» no es un concepto vago — es una
columna que no tenemos.

---

## FEDIAF 2025, LEÍDA ENTERA (9 de septiembre) — y lo gordo estaba en un recuadro, no en una tabla

Elena: *«cuando te digo que te los leas me refiero a que te los leas completos.
No me vale que cojas las tablas y listo, porque hemos visto que haciendo eso hay
errores»*. Esto es el resultado de hacerlo. Nueve hallazgos, y el primero cambia
doce mínimos.

### 1 · Los aminoácidos esenciales van un 10 % por encima, y no lo aplicábamos

**§3.2.1 «How to read the tables»**, en el recuadro que hay al lado de la tabla
de conversiones, literal:

> *«For commercial dog and cat foods it is recommended that the nutrient levels
> are at or above the levels listed in the tables and do not exceed the
> nutritional or legal maximum. **If the protein digestibility of ≥80 %
> (mentioned under 2.2. Scope) cannot be guaranteed, it is recommended to
> increase the essential amino acid levels by a minimum of 10 %.**»*

Y **§2.2 «Scope»** dice de qué cuelga toda la guía:

> *«These guidelines relate to dog and cat foods manufactured from ingredients
> with **normal digestibility (i.e. ≥70 % DM digestibility; ≥80 % protein
> digestibility)** and average bioavailability.»*

**No podemos garantizar ese 80 %.** El catálogo no tiene columna de
digestibilidad —ni una— así que no es que salgamos por debajo: es que no lo
sabemos, y la regla está escrita justo para ese caso. Y hay motivo para no darlo
por hecho: una ración BARF lleva entre un 20 y un 60 % de hueso carnoso, con
colágeno y tejido conectivo, que es lo menos digestible del plato.

**Medido, dos veces.** Primero, cuánto margen tienen hoy los doce sobre su
mínimo, en los 36 menús base del catálogo:

| aminoácido | peor menú | percentil 10 | mediana |
|---|---|---|---|
| Lisina | 358 % | 385 % | 503 % |
| Arginina | 263 % | 312 % | 372 % |
| Histidina | 246 % | 279 % | 376 % |
| Isoleucina | 234 % | 290 % | 360 % |
| Leucina | 228 % | 248 % | 314 % |
| Valina | 209 % | 254 % | 366 % |
| Treonina | 204 % | 217 % | 264 % |
| Fenilalanina+tirosina | 202 % | 237 % | 287 % |
| Fenilalanina | 180 % | 221 % | 306 % |
| Triptófano | 143 % | 168 % | 229 % |
| Metionina | 137 % | 189 % | 319 % |
| **Metionina+cistina** | **112 %** | **149 %** | 240 % |

Once de los doce sobran. **Uno va justo**, y es metionina+cistina.

Segundo, con el +10 % puesto y por la vía de la API: doce perfiles (toy, mini,
mediano, grande, gigante, senior, cachorro temprano y tardío, lactante, y adulto
sin pollo, sin vacuno y sin pescado) dan menú **los doce, en el peldaño
estricto**.

**Y hay una segunda razón para que sea justo ese el que va apretado**, en otra
parte del mismo documento — ver el hallazgo 6.

### 2 · El máximo LEGAL solo se aplica si el nutriente se añade como aditivo

**§3.1.3**, literal:

> *«**A legal maximum only applies when the particular trace element or vitamin
> is added to the recipe as an additive**, but relates to the "total" amount
> present in the finished product… **If the nutrient comes exclusively from feed
> materials, the legal maximum does not apply**, instead the nutritional
> maximum, when included in the relevant tables, should be taken into account.»*

Nosotros aplicamos **siempre** el legal, para el zinc (56,75), el yodo (2750),
el hierro (170,45), el selenio (142), el cobre (7,0), el manganeso (42,5) y la
vitamina D (14,1875). En un menú **sin suplementos** esos nutrientes vienen solo
de materia prima y el legal no aplicaría.

**No se cambia nada**, y ahora hay un motivo escrito: el legal suele ser más
estricto que el nutricional (vitamina D: 227 legal contra 320 nutricional), así
que aplicarlo siempre es el lado seguro. Lo que sí importa es no volver a
escribir «está por encima del máximo legal» sin el matiz.

### 3 · La definición de «máximo nutricional», que es la que faltaba

**§1.1 Glosario**: *«Nutritional maximum limit is the maximum level of a
nutrient in a complete pet food that, **based on scientific data, has not been
associated with adverse effects** in healthy dogs and cats. **Levels exceeding
the nutritional maximum may still be safe**, however, no scientific data are
currently known to FEDIAF.»*

Es exactamente la distinción que hoy hizo falta con el fósforo: un máximo
nutricional no es un techo toxicológico, es «hasta aquí hay datos». Y explica por
qué FEDIAF puede decir del yodo que *«the existing legal maximum is safe for all
dogs»* después de descartar el estudio de Castillo.

### 4 · El BCS ideal del perro es 4/9 a 5/9, y en BCS 9 FEDIAF dice más del 45 %

**Anexo 7.1**, literal: *«**The ideal BCS should therefore be between 4/9 and
5/9**»*, con grasa corporal óptima **15-25 %** en perro (Kealy 2002, el estudio
de 14 años con labradores).

Y la **Tabla VII-2** da los rangos por punto, que es lo que usamos para derivar
el peso objetivo desde el BCS:

| BCS | % de peso sobre el ideal (FEDIAF) | lo que aplica Rawku |
|---|---|---|
| 6 | +10 a 15 % | +10 % |
| 7 | +20 a 30 % | +20 % |
| 8 | +30 a **45** % | +30 % |
| 9 | **>45 %** | 40 % |

Coincidimos con el **extremo bajo** del rango en 6, 7 y 8 — o sea que estimamos
**menos exceso**, y el peso objetivo sale más alto y con él más kcal. Y en BCS 9
FEDIAF dice **más del 45 %** y nosotros aplicamos 40.

Eso confirma con fuente primaria lo que ya estaba escrito en `verificar.py` a
partir de Broome et al. (2023): en BCS 9 nuestra estimación es una **cota
inferior**. **Y FEDIAF también da filas por DEBAJO de 5**, que AAHA no tiene
(BCS 4 = −10 a 15 %, 3 = −20 a 30 %, 2 = −30 a 40 %, 1 = −≥40 %).

No se toca todavía porque el peso objetivo alimenta el DER, que se calcula en
los dos repos y tiene contrato compartido (`der_casos.json`). Va a
`PENDIENTE_NUTRICION.md` con la medida.

### 5 · La ración diaria TOTAL incluye los premios

**§4.1**: *«The total daily ration should match the recommended allowances and
nutritional and legal maximum values listed in the tables for complete pet
food.»* Rawku no modela premios ni snacks. Es un hueco de producto, no de motor.

### 6 · Taurina: no es esencial en el perro, pero el mecanismo apunta a met+cis

**Anexo 7.3**, sobre el perro: sintetiza taurina de los aminoácidos azufrados,
así que **no es esencial**. Pero:

> *«low plasma levels of taurine (<40 µmol/L) **may also predispose to dilated
> cardiomyopathy**… low plasma or low whole-blood taurine levels may be seen in
> dogs fed non-supplemented very low protein diets, **or foods that are low in
> sulphur-containing amino acids or with poor availability of the
> sulphur-containing amino acids**»*

Y la intervención que nombra: *«The addition of taurine to such foods **or
increasing the intake of the precursors (methionine and cysteine)** can prevent
such a decrease»*. Razas más sensibles: **Terranova**, con la tasa de síntesis
disminuida (Backus 2006) — y es una de las dos razas con cifra propia de DER.

**Dos partes distintas de la misma guía apuntando al mismo nutriente**: §3.2.1
dice que subamos los aminoácidos esenciales porque no garantizamos la
digestibilidad, y el anexo 7.3 dice que el azufrado poco disponible es
precisamente el que lleva a cardiomiopatía dilatada. Y metionina+cistina es el
que menos margen tiene del catálogo. Conecta con `dcm_asociada_a_dieta`, que hoy
solo tiene avisos.

### 7 · Reacción adversa al alimento: el diagnóstico es la dieta de eliminación

**Anexo 7.6**: el signo predominante es el **prurito, en casi el 100 % de los
casos**; solo el 10-15 % dan signos digestivos. Y *«adverse reactions to food are
**only diagnosed through the elimination of the food component** (eviction
diet)»*, idealmente confirmado por reintroducción.

Los alérgenos más citados son leche, vacuno, huevo, cereales y lácteos; los
estudios controlados nombran trigo, soja, **pollo** y maíz — con el matiz de que
puede ser simplemente lo que más se come. **Casi cualquier proteína intacta puede
causarla.**

Rawku ya tiene la herramienta (exclusiones por palabra y por familia de especie).
Lo que no tiene es un **modo dieta de eliminación**: una o como mucho dos fuentes
de proteína novedosas, que es lo que pide SACN5 cap.31. Va a producto.

### 8 · Anexo 7.7: los alimentos humanos, con cifras

| | Dosis más baja documentada |
|---|---|
| Pasas | **2,8 g/kg de peso vivo** |
| Uvas | 19,6 g/kg |
| Cebolla fresca | **5-10 g/kg** |
| Ajo | 5 g/kg (extracto equivalente, 7 días) |
| Teobromina | letal a 90-115 mg/kg; LD50 250-500 |

*«Even a large dog of 40 kg may need to eat only 120 g to be at risk»* (pasas), y
*«the severity of the illness does not seem to be dose-related»*.

**Ninguno está en el catálogo** — comprobado, cero coincidencias con uva, pasa,
cebolla, ajo, puerro, cebollino, chalota, chocolate y cacao. Lo que no hay es
nada que impida meterlos mañana.

### 9 · El changelog 2011→2025, y las secciones 5 y 6

Ya contadas más arriba: el changelog no deja nada que aplicar y nuestra tabla
recoge los seis cambios que importan; las secciones 5 y 6 son métodos analíticos
y protocolos de digestibilidad. Lo único aprovechable de ahí: FEDIAF distingue
**fibra total, insoluble y soluble** como tres analitos con método propio, así
que «soluble vs insoluble» no es un concepto vago, es una columna que no
tenemos — y hace falta para la pregunta de la fibra y el hierro.

---

## SACN5 · empieza la lectura por capítulos ENTEROS (9 de septiembre)

No por tablas. El recuento de la §quinta pasada de `VERIFICACION_FILA_A_FILA.md`
dice por qué: 32 de 91 tablas citadas y 26 capítulos de 70 sin una sola cita, y
la lección del 8 de septiembre es que las tablas no traen lo que la fuente dice
en prosa.

### Capítulo 7 · Antioxidantes — leído entero

Es uno de los 26 sin citar, y trae **cinco cosas**, dos de ellas con cifra.

#### 7.1 · La vitamina E no tiene máximo en FEDIAF, y aquí hay uno sugerido

Literal: *«There are no published toxicity data for vitamin E in dogs; however,
concentrations exceeding 2,000 IU/kg DM of food have been fed for 17 weeks
without observable negative reactions. Although an upper limit of toxicity has
not been documented, **a level of 1,000 IU/kg DM of food, or 45 IU/kg of body
weight, has been suggested (NRC, 2006)**»*.

1.000 UI/kg MS ÷ 4 = 250 UI/1000 kcal, y × 0,671 = **167,75 mg/1000 kcal**.

**FEDIAF no da máximo de vitamina E** (está en la lista `SIN_MAXIMO` de
`auditar_fediaf.py`), así que hoy el motor no le pone ninguno. Es la misma forma
que el fósforo del adulto: un nutriente sin techo y una fuente que sí sugiere
uno.

**Y corrobora algo de ayer**: el suelo de vitamina E de la disfunción cognitiva
que hubo que apartar por no caber eran **187,5 mg/1000 kcal** — o sea que estaba
**por encima del nivel que el NRC sugiere como límite superior**. Apartarlo no
fue solo aritmética del catálogo.

#### 7.2 · El selenio: el rango protector es el mismo de la Tabla 35-3

*«Studies indicate antioxidant protective ranges for selenium would be
approximately **0.50 to 1.3 mg selenium/kg food DM** for dogs and cats»* — que es
exactamente el rango de la Tabla 35-3 (125-325 µg/1000 kcal) que la disfunción
cognitiva pide y que no aplicamos.

Y el techo: *«**AAFCO (2007) suggests a safe upper limit of 2 mg selenium/kg diet
for dogs**»* = **500 µg/1000 kcal**, o sea **3,5 veces el máximo legal de FEDIAF**
(142) que aplicamos nosotros. No cambia nada —manda el legal— pero sitúa la
decisión: no aplicar el suelo de 125 no es por miedo a la toxicidad, es porque
obliga a vivir pegado a un techo legal, y eso sigue valiendo.

#### 7.3 · El β-caroteno del perro, corroborado por la vía del plasma

*«β-carotene can serve as a precursor to vitamin A in dogs, but not cats»*, y el
dato que lo cuantifica: a la misma dosis, el gato alcanza en plasma
**concentraciones 50 veces mayores** que el perro, *«indicating that most of the
β-carotene administered to dogs is probably converted to vitamin A rather than
absorbed directly»*.

O sea que el perro es un convertidor eficiente, que es justo lo que dice el
factor 4:1 de FEDIAF Tabla VII-14 encontrado hoy. Dos fuentes independientes.

#### 7.4 · De dónde sale el mínimo de vitamina E, y por qué es condicional

*«NRC recommends that dogs receive 22 IU vitamin E per kg/food DM (**based on a
food containing 0.1 ppm selenium, not more than 1 % linoleic acid** and 3,670
kcal ME/kg DM)»*.

Esto le pone **cifra a la condición** de la regla `vitamina_e_segun_pufa` que
tenemos escrita como `documentado_sin_cifra`: el mínimo publicado supone **no más
de un 1 % de ácido linoleico en materia seca**. Una ración BARF pasa de ahí de
sobra. No cambia nada hoy —está medido que vamos holgados, 0 de 216 menús por
debajo de la relación clásica 0,6 mg/g y el peor a 1,53— pero la regla deja de
ser «FEDIAF lo nombra y no lo cuantifica»: hay un ancla.

#### 7.5 · Y dos avisos sueltos que no cambian el motor

- **Vitamina C y oxalato**: en personas, 2.000 mg/día suben la excreción urinaria
  de oxalato; en gatos, hasta 193 mg/kg MS no aumentó el riesgo. Es el respaldo
  de la fila «Ascorbic acid» de la Tabla 40-5 que hoy no podemos aplicar por
  falta de datos de etiqueta.
- **Vitamina C y galgos**: *«oral vitamin C supplementation at 1 g/day may slow
  racing times in greyhounds»*. No es nuestro caso, pero desmonta la idea de que
  suplementar antioxidantes siempre suma.

### Capítulo 62 · Colitis — la Tabla 62-1, que era una de las once sin mirar

**No es una patología que ofrezcamos** (tenemos `enteropatia_cronica`, con la
Tabla 57-1), y añadirla es decisión de producto, no de fuentes. Se transcribe
aquí para que la decisión se pueda tomar con la tabla delante.

Tabla 62-1, columna perro, convertida a por 1000 kcal (× 2,5 en gramos, × 2500
en mg):

| Factor | La fuente | Por 1000 kcal |
|---|---|---|
| Proteína, adulto | 15-30 % MS | 37,5-75 g |
| Proteína, cachorro | 22-32 % MS | 55-80 g |
| Grasa | 8-15 % MS | 20-37,5 g |
| Fibra, alimento muy digestible | ≤5 % MS | ≤12,5 g |
| Fibra, alimento enriquecido | ≥7 % MS | ≥17,5 g |
| Sodio | 0,3-0,5 % MS | 750-1250 mg |
| Cloruro | 0,5-1,3 % MS | 1250-3250 mg |
| Potasio | 0,8-1,1 % MS | 2000-2750 mg |

Dos cosas que saltan a la vista:

- **El suelo de proteína (37,5) está por debajo del mínimo de FEDIAF (52,1)**,
  igual que en el oxalato. Otra que solo podría pautar un colegiado.
- **El techo de proteína (75) es exactamente el mismo que aplicamos en
  pancreatitis**, y el de grasa (37,5) también. Las dos tablas coinciden sin
  haberlo buscado.

Y por tercera vez en el mismo día, la **digestibilidad**: *«Highly digestible
foods: **≥87 % for protein** and ≥90 % for fat»*, *«Fiber-enhanced foods: ≥80 %
for protein»*. Aparece en FEDIAF §2.2, en FEDIAF §3.2.1 y aquí. Es una columna
que el catálogo no tiene y de la que cuelgan cosas.

### Capítulo 18 · Perros de trabajo y de deporte — leído entero

Otro de los 26 sin citar, y **el que más cambia el motor para un perro SANO**.

#### El hallazgo: al perro que trabaja le faltaba doce veces la vitamina E

Tabla 18-9, fila «Antioxidants / Vitamin E», **en las cuatro columnas de
actividad** —sprint, intermedia baja, intermedia alta y resistencia—:

> *«≥500 IU vitamin E/kg food (DM)»*

500 ÷ 4 = 125 UI/1000 kcal, y × 0,671 (tocoferol natural, conversión de la Tabla
VII-14 de FEDIAF) = **83,9 mg/1000 kcal**.

El mínimo de FEDIAF para el adulto son **6,968**. O sea que el perro de trabajo
necesita **doce veces** eso. Y medido sobre los 36 menús del catálogo:

```
vitamina E real ..... de 13,4 a 89,0 mg/1000 kcal, mediana 25,1
llegan a 83,9 ....... 3 de 36
```

Un perro de pastoreo estaba recibiendo **un tercio** de lo que su fuente pide, y
salía **verde**, porque el semáforo mide contra el mínimo del perro de
mantenimiento.

#### Y no hacía falta ningún campo nuevo

**La DER efectiva en kcal por kg^0,75 ES el nivel de actividad.** `der.py` y la
Tabla VII-7 de FEDIAF usan los mismos cinco escalones, y el motor ya calcula esa
cifra para escalar los mínimos:

| DER efectiva | `der.py` lo llama | |
|---|---|---|
| 95 | sedentario | |
| 110 | normal | |
| 125 | activo | |
| **150** | **muy activo** | *«perro de trabajo, pastoreo»* |
| **175** | **trabajo** | |

Así que el suelo se dispara desde 150 sin pedirle al frontend un campo más que
podría desincronizarse — que es exactamente la lección del DER.

**Medido antes de aplicarlo:** diez perros de trabajo (8, 15, 25, 35 y 55 kg, a
150 y a 175 kcal/kg^0,75) dan menú **los diez en el peldaño estricto**, con la
vitamina E real entre 82,7 y 87,8. Y no choca con ningún techo: FEDIAF no da
máximo de vitamina E, y el único escrito —el que sugiere el NRC vía cap.7,
167,75 mg/1000 kcal— es el doble.

**Dónde está la línea, y qué es interpretación nuestra:** la Tabla 18-1 lista las
actividades, y en «intermediate» incluye *«exercise with people (running,
bicycling)»*, que podría ser también nuestro «activo» (125). Se aplica desde 150
porque cubre a los perros que la fuente nombra sin discusión —pastoreo, policía,
rescate, caza, trineo— y no le pone un suelo nuevo a un perro que la fuente no
cubre claramente. Bajarlo a 125 es decisión de nutrición.

#### Las otras dos filas de la misma tabla, escritas y sin aplicar

- **Vitamina C, 150-250 mg/kg MS** = 37,5-62,5 mg/1000 kcal. **No se aplica**: el
  perro la sintetiza y **FEDIAF no le pone requisito ninguno** — no hay fila de
  vitamina C en la Tabla III-3b. Y el cap.7 avisa de que suplementar no siempre
  suma: *«oral vitamin C supplementation at 1 g/day may slow racing times in
  greyhounds»*.
- **Selenio, 0,5-1,3 mg/kg MS** = 125-325 µg/1000 kcal. **No se aplica**: el rango
  se sale por arriba del máximo legal de FEDIAF (142). Es la **tercera vez** que
  aparece este mismo rango —Tabla 35-3, cap.7 y aquí—, así que la pregunta para
  el nutricionista es una sola.

#### Y lo que dice FEDIAF de esta población, que cierra el círculo

**§2.2 «Scope»**: *«Excluded from the FEDIAF's Nutritional Guidelines are pet
foods for particular nutritional purposes and **some other specialised foods such
as for sporting dogs**»*. O sea que para estos perros la propia FEDIAF dice que
su tabla no basta. SACN5 es la que la completa.

#### El resto de la Tabla 18-9, para cuando toque

| Factor | Sprint | Intermedia baja | Intermedia alta | Resistencia |
|---|---|---|---|---|
| Grasa (% MS) | 8-10 | 15-30 | 25-40 | >50 |
| Proteína (% MS) | 22-28 | 22-32 | 22-32 | 28-34 |
| Densidad (kcal/g MS) | 3,5-4,0 | 4,0-5,0 | 4,5-5,5 | >6,0 |
| Digestibilidad MS | >80 % | >80 % | >80 % | >80 % |
| Ácidos grasos insaturados | — | >60 % | >60 % | — |

La fila de insaturados lleva su porqué escrito: *«to optimize olfaction»* — es
para los perros de detección. Y la digestibilidad **>80 % de materia seca** en
las cuatro columnas, que es más de lo que FEDIAF supone (≥70 %) y la **cuarta
vez** que la digestibilidad aparece hoy.

### Capítulo 45 · Urolitos compuestos — leído entero (es corto)

Uno de los 26 sin citar. Trae **una regla de manejo** que el motor no cumple.

Los urolitos compuestos —núcleo de un mineral, capas de otro— son el **7 %** de
los urolitos caninos analizados en Minnesota, y el primer ejemplo del capítulo es
*«a nucleus of 100 % calcium oxalate monohydrate surrounded by a shell of 80 %
magnesium ammonium phosphate»*: oxalato dentro, estruvita fuera.

Y la regla: *«management protocols designed primarily to minimize recurrence of
minerals composing the **nucleus** (rather than those in shells)»*.

**El motor combina `oxalato` + `estruvita` con `min()` y no dice nada.** Las otras
tres parejas de urolitos sí se paran, pero por casualidad: `urato` y `cistina`
están marcadas «sin dieta automática» porque necesitan bajar de FEDIAF, no porque
sean incompatibles. No existe ningún mecanismo de **parejas incompatibles**: el
motor solo sabe bloquear patologías sueltas.

Escrito en `patologias.json` (`nota_urolito_compuesto`, en las dos) y como
PREGUNTA 37 y 38 en `PARA_EL_NUTRICIONISTA.md`. No se bloquea porque cuál es el
núcleo sale del análisis de la piedra, un dato que la app no pide.

### Capítulos 51 y 61 · Las dos introducciones del aparato digestivo — leídas enteras

Cortas las dos, y de las 26 sin citar. **No traen números**, traen listas — que
es justo lo que un barrido de tablas de «key nutritional factors» no recoge,
porque no son esas tablas.

**Tabla 51-1, trastornos gástricos por raza.** Dilatación-vólvulo gástrico:
basset hound, dóberman, setter gordon, **gran danés**, setter irlandés, san
bernardo, weimaraner. Estenosis pilórica: boston terrier, bóxer, gato siamés.

**Tabla 61-3, trastornos colónicos por raza.** Flatulencia: braquicéfalos.
Gastroenteritis hemorrágica: teckel, schnauzer miniatura, caniche toy. Síndrome
de intestino irritable: razas de trabajo y toy. Colitis ulcerativa: **bóxer y
bulldog francés**.

**Lo que esto abre, y no es motor:** Rawku ya tiene `riesgo_gdv` con un aviso muy
completo —comprobado antes de escribir esto, para no descubrir otra vez algo que
ya está— pero **el dueño tiene que marcarlo**. La app sabe la raza (la usa para
el DER). Podría **sugerirlo** a las siete razas que la fuente nombra, en vez de
esperar a que alguien lo sepa. Lo mismo con la colitis ulcerativa del bóxer.

Es decisión de producto y va a `PENDIENTE_PRODUCTO.md`, no al motor.

### Capítulo 49 · Enfermedades orales — leído entero

La Tabla 49-2 era una de las once «sin mirar», y al leerla resulta que **no pide
ni un nutriente**. Sus tres factores son:

| Factor | Lo que pide |
|---|---|
| Agua | mantener el equilibrio, oral o parenteral |
| Densidad energética | **>4,5 kcal/g de materia seca** en perro |
| Forma del alimento | líquido o papilla, que se aceptan mejor |

Es una tabla de **forma**, no de nutrición: densidad energética y textura. El
motor no modela ninguna de las dos, y para esta indicación la fuente **no pide un
perfil distinto de nutrientes**. Así que «enfermedad oral» no sería una patología
del motor, sería un consejo — y eso **baja de once a diez** las tablas de
requisito canino que de verdad faltan por mirar.

El manejo que sí es accionable: **varias comidas pequeñas al día**, y enjuagar la
boca con agua después de cada una para que no se queden restos pegados a las
lesiones.

**Tabla 49-1, razas**: paladar hendido en braquicéfalos; épulides en bóxer;
gingivitis y estomatitis en maltés y husky siberiano; neoplasia oral en cocker,
pastor alemán, braco alemán de pelo corto, golden retriever y weimaraner.

Y un dato nutricional suelto que conviene no perder: *«Oral congenital anomalies
such as cleft palate… may have nutritional causes (e.g., **copper deficiency in
pregnant queens**)»*. Es en gata, no en perra, así que no se aplica — pero es la
primera vez que aparece un déficit de cobre en gestación con consecuencia
malformativa, y nuestro mínimo de cobre no distingue etapa reproductora.

### Las once tablas «sin mirar»: cerradas las once (9 de septiembre)

La §quinta pasada de `VERIFICACION_FILA_A_FILA.md` dejó once tablas de requisito
canino o mixto sin leer. Leídas las once, **el resultado es mejor de lo que
parecía y más ordenado**:

| Tabla | Qué es | Qué pasa con ella |
|---|---|---|
| **18-9** | Perro de trabajo y deporte | **APLICADA**: vitamina E ≥83,9 mg/1000 kcal |
| **49-2** | Enfermedades orales | **No pide ni un nutriente**: agua, densidad y textura |
| **16-4** | Cachorros lactantes | **No aplica**: es la composición de la leche de la perra, el patrón para criar huérfanos. No formulamos leche |
| **25-5** | Alimentos líquidos para nutrición enteral | **No aplica**: osmolaridad 250-400 mOsm/l y 1 kcal/ml. No formulamos líquidos |
| **52-2** | Gastritis y úlcera gastroduodenal | familia digestiva, abajo |
| **54-2** | Motilidad y vaciamiento gástrico | familia digestiva |
| **56-2** | Gastroenteritis aguda | familia digestiva |
| **59-1** | Síndrome de intestino corto | familia digestiva |
| **62-1** | Colitis | familia digestiva |
| **50-3** | Disfagia por lesión obstructiva | esofágicas, abajo |
| **50-4** | Esofagitis y reflujo | esofágicas |

#### La familia digestiva: cinco tablas y UN núcleo común

Las cinco piden lo mismo en lo esencial, y **son suelos, no techos** — cap.52 lo
dice literal: *«Foods for patients with acute gastroenteritis should contain
levels of potassium, chloride and sodium **above the minimum allowances for
normal dogs and cats**»*.

| | La fuente (% MS) | Por 1000 kcal | Mínimo de FEDIAF |
|---|---|---|---|
| Potasio | 0,8-1,1 | **2000-2750 mg** | 1450 |
| Cloruro | 0,5-1,3 | **1250-3250 mg** | 430 |
| Sodio | 0,3-0,5 | **750-1250 mg** | 290 |

Y alrededor: grasa ≤15 % MS (≤37,5 g/1000 kcal) en perro, fibra ≤5 % MS
(≤12,5 g) en el enfoque «muy digestible» o 7-15 % en el enriquecido, densidad
4,0-4,5 kcal/g MS, y digestibilidad ≥87 % proteína y ≥90 % grasa.

Dos avisos concretos de la 54-2 que no son números: **evitar fibras
gelificantes** (pectinas y gomas: arábiga, guar, carragenato, psyllium, xantana,
garrofín, ghatti, tragacanto) en trastornos de motilidad, y servir la comida
**entre 21 y 38 °C**, porque la comida fría retrasa el vaciamiento gástrico.

Y una que va al revés de todo lo demás, en el intestino corto (59-1): ahí se
prefiere el **alimento seco**, porque vacía el estómago más despacio.

**Ninguna de las cinco es una patología que ofrezcamos.** Añadirlas es decisión
de producto, no de fuentes (`CERRADO.md`), y va a `PENDIENTE_PRODUCTO.md`.

#### Las dos esofágicas

| | Disfagia obstructiva (50-3) | Esofagitis y reflujo (50-4) |
|---|---|---|
| Densidad | ≥4,5 kcal/g MS | ≥4 kcal/g MS |
| Grasa | **≥25 % MS** (≥62,5 g) | **≤15 % MS** (≤37,5 g) |
| Proteína | ≥25 % MS (≥62,5 g) | ≥25 % MS |

Van en direcciones opuestas en la grasa, y el capítulo explica por qué: *«High
dietary fat delays gastric emptying and reduces lower esophageal sphincter
pressure, which promotes reflux»*. Y la proteína sube a propósito, porque
*«protein stimulates an increase in gastroesophageal sphincter pressure»*.

#### Y la cifra del hueso, que es la que más nos toca

Del mismo cap.50, citando a Rousseau et al. (2007):

> *«In a recent retrospective review, **46 of 60 esophageal foreign bodies
> removed from dogs were bones**»*

Cuarenta y seis de sesenta. **No es un argumento contra el hueso carnoso** —una
ración BARF lleva entre un 20 y un 60 % y es su fuente de calcio— pero es el
número que hay que tener delante al decidir qué cortes se ofrecen, y al
contestarle a un dueño que pregunta si es peligroso. Escrito en `seguridad.py`,
al lado de las dos listas de riesgo por corte que ya había.

### Capítulo 1 · «An Iterative Process» — leído entero, y trae un matiz al cambio de hoy

Es el primer capítulo del libro y uno de los 26 sin citar. No tiene tabla de
factores nutricionales, así que ningún barrido de tablas lo habría abierto
nunca. Trae tres cosas.

#### 1 · Confirma el BCS ideal 4-5/9, por una vía independiente

Literal: *«A BCS of **2.5/5 to 3/5** is probably ideal for most mature dogs and
cats for optimal health and resultant longevity. Thus, overall, **an ideal BCS is
a range of numbers rather than simply a "3/5"**»*.

En escala de nueve, 2,5/5 es 4/9 y 3/5 es 5/9. **Es exactamente lo que dice
FEDIAF** en su §7.1.3 («The ideal BCS should therefore be between 4/9 and 5/9»).
Dos fuentes independientes, el mismo rango.

#### 2 · ⚠️ Y UN MATIZ AL CAMBIO DE HOY, que conviene tener escrito

La misma frase sigue: *«a BCS of **2/5 to 2.5/5 may be desirable for a racing
greyhound**»* — o sea **3 a 4 sobre 9 para un perro de carreras**.

Hoy se ha cambiado la API para que **estime peso objetivo también por debajo de
BCS 5**, siguiendo la Tabla VII-2 de FEDIAF. Para un galgo de competición en BCS
4 eso significa proponerle un peso objetivo un 10 % mayor: **engordarlo**.

No se toca nada por ahora, y el motivo es que el efecto real es pequeño y va del
lado seguro: ese peso objetivo NO cambia las kcal en la app —las calcula el
frontend— sino el peso de referencia con el que se **escalan los mínimos** de
FEDIAF, y un peso de referencia mayor escala los mínimos **hacia arriba**, que es
más conservador. Pero queda escrito, porque el día que el peso objetivo alimente
las kcal, un galgo de carreras en BCS 4 no está delgado: está en su sitio.

Y la app ya sabe distinguirlo: tiene el nivel de actividad, y el «trabajo» (175
kcal/kg^0,75) es justo esa población.

#### 3 · La malnutrición incluye los excesos, y el ejemplo es el de hoy

Box 1-1, literal: *«Another example of malnutrition due to unbalanced nutrition
is **developmental orthopedic disease seen in rapidly growing large- and
giant-breed puppies as a result of excessive calcium and energy intake**»*.

Es el tercer sitio del libro que dice lo mismo —caps. 10 de Fascetti, 33 y ahora
el 1— y es exactamente el techo de calcio que se aplicó esta mañana. En el
**primer capítulo**, en un recuadro, sin tabla.

#### Y dos apuntes de método

- **Repetibilidad del BCS**: entre observadores coincide el **80-90 %** de las
  veces, y correlaciona 0,9 con la composición corporal medida. O sea que el
  dato de entrada del que cuelga el peso objetivo tiene ese margen, y ninguna
  cifra que salga de él puede ser más precisa que eso.
- *«Intakes of **treats and nutritional supplements** should be recorded»* — los
  premios, otra vez. Es la tercera fuente que los nombra (FEDIAF §4.1 y SACN5
  cap.17) y Rawku sigue sin modelarlos.

---

### Capítulo 38 · Urolitiasis canina: definiciones, fisiopatología y manifestaciones clínicas — leído entero

Es uno de los 26 sin citar. Es un capítulo **de diagnóstico**, no de dietas: la
dieta de cada tipo de piedra vive en los capítulos 39 a 45, que ya están leídos.
Aun así deja cuatro cosas.

#### 38.1 · Cuántas piedras hay de cada tipo, sobre 350.803 urolitos

Tabla 38-8, Minnesota Urolith Center, 1981-2007. Es el censo, y ordena por dónde
merece la pena mirar:

| Tipo | % |
|---|---|
| Estruvita (fosfato amónico magnésico) | 42,53 |
| Oxalato cálcico | 38,01 |
| **Compuestos** (núcleo de un mineral, capas de otro) | **8,79** |
| Purinas (urato amónico, urato sódico, ácido úrico, xantina) | 6,39 |
| Mixtos | 2,32 |
| Cistina | 0,97 |
| Fosfato cálcico | 0,51 |
| Sílice | 0,40 |

Las seis patologías de urolito que tiene el motor —`estruvita`, `oxalato`,
`urato`, `cistina`, `urolitos_fosfato_calcico` y `urolitos_silice`— cubren el
**88,8 %** del censo. Lo que queda fuera son los compuestos y los mixtos, que no
son un séptimo tipo sino **combinaciones de los seis**.

#### 38.2 · Y el 8,79 % refuerza la nota del urolito compuesto, que ya estaba escrita

`patologias.json` lleva desde ayer `nota_urolito_compuesto` en `oxalato` y en
`estruvita`, con el 7 % que da el capítulo 45. Aquí el mismo libro, con la serie
entera y más larga, da **8,79 % de 350.803**. O sea que **casi una piedra de cada
once es compuesta**, y que marcar dos casillas de urolito a la vez no es un caso
de laboratorio.

El capítulo 38 añade el **porqué mecánico**, que el 45 daba como regla de manejo:
*«Veterinarians have encountered difficulty in dissolving uroliths composed
primarily of struvite with an outer shell composed primarily of calcium apatite.
Difficulty will also be encountered in attempting to induce complete dissolution
of a urolith with a nucleus of calcium oxalate, calcium phosphate, ammonium urate
or silica and a shell of struvite **because the solubility characteristics of
this combination of minerals are dissimilar**»*. Tratar los dos a la vez no es
que sea redundante: es que las dos dietas piden orinas incompatibles.

La nota se actualiza con esta cifra. Sigue sin bloquearse, por lo mismo que ya
está escrito allí: cuál es el núcleo sale del análisis de la piedra, y la app no
lo tiene.

#### 38.3 · La raza y el sexo predicen el tipo de piedra — Tabla 38-11

Es la tabla que le falta al punto de **sugerencias por raza** que está apuntado
en `PENDIENTE_PRODUCTO.md`, y es una fuente de verdad, no una lista de internet:

| Piedra | Razas | Sexo | Edad típica |
|---|---|---|---|
| Estruvita | schnauzer miniatura, caniche miniatura, bichón frisé, cocker spaniel | hembras (>80 %) | 2-9 años |
| Oxalato cálcico | schnauzer miniatura y estándar, lhasa apso, yorkshire, caniche miniatura, shih tzu, bichón frisé | machos (>70 %) | 5-12 años |
| Urato | **dálmata**, bulldog inglés, schnauzer miniatura, yorkshire, shih tzu | machos (>90 %) | 1-5 años |
| Fosfato cálcico | yorkshire, schnauzer miniatura, shih tzu | machos (>55 %) | <1 año y 6-10 |
| Cistina | bulldog inglés, teckel, basset hound, terranova | machos (>98 %) | 1-7 años |
| Sílice | pastor alemán, golden retriever, labrador, schnauzer miniatura, cavalier | machos (95 %) | 3-10 años |

⚠️ **No se aplica nada de esto, y no por olvido.** Una predisposición de raza no
es un diagnóstico: proponerle una dieta de urato a un dálmata sano sería decidir
por criterio clínico sin que nadie lo haya marcado, y eso no lo hace el motor.
Lo que sí puede hacer, y es lo que está apuntado, es **sugerir la pregunta**.

Y el schnauzer miniatura sale en **cinco de las seis filas**.

#### 38.4 · Un aviso de método sobre la hipercalciuria, por si algún día se mide

*«Dogs that absorb excessive amounts of calcium from their food and subsequently
excrete large quantities of calcium in their urine have **intestinal
hypercalciuria**. Hypercalciuria primarily occurs during food consumption; normal
or lower quantities of urine calcium are excreted when food is withheld»*. O sea
que en el perro de oxalato la vía dietética es real y medible, y se distingue de
la hipercalcemia por análisis en ayunas. No cambia nada hoy: el motor ya aprieta
el calcio en `oxalato`. Queda escrito porque explica **por qué** ese tope es
dietético y no un parche.

---

### Capítulo 48 · Introducción a las enfermedades digestivas y del páncreas exocrino — leído entero

Otro de los 26 sin citar. Es corto y es el índice de los capítulos 49 a 67, pero
trae en un recuadro (el 48-3) **la cifra que Elena preguntó ayer** y una
corroboración del tope de grasa de la pancreatitis.

#### 48.1 · ⚠️ LA DIGESTIBILIDAD, CON NÚMEROS — y responde a la pregunta de ayer

Elena preguntó si hay alguna fuente de la que sacar la digestibilidad de los
alimentos. `DATOS_QUE_FALTAN.md` quedó con la pregunta abierta. Aquí no está el
dato por alimento, pero sí **la escala con la que se lee**, literal:

- *«**highly digestible** has generally been reserved for products with protein
  digestibility **≥87 %** and fat and carbohydrate digestibilities **≥90 %**»*.
- *«The **average** digestibility coefficients for popular commercial foods are
  **78 a 81 %**, **77 a 85 %** y **69 a 79 %** for crude protein, crude fat and
  carbohydrate, respectively»*.
- *«Average fat digestibility in commercial dog food is approximately **90 %**»*.

⚠️ **Y esto sostiene el +10 % de los aminoácidos que se aplicó anoche.** FEDIAF
manda subir un 10 % los mínimos de aminoácidos cuando **no se garantiza la
digestibilidad** de la dieta. Hasta ahora ese factor se aplicaba porque FEDIAF lo
dice; con esta tabla se puede además situar: la comida comercial media va en
**78-81 %** de digestibilidad proteica, y «alta digestibilidad» empieza en **87 %**.
Una ración cruda casera no tiene ensayo de digestibilidad de ningún tipo, así que
no está ni en una casilla ni en la otra: está sin medir, que es exactamente el
supuesto que FEDIAF cubre con el +10 %.

**Lo que sigue faltando** es el coeficiente por alimento, y este capítulo no lo
trae. Queda como estaba en `DATOS_QUE_FALTAN.md`.

#### 48.2 · El tope de grasa de la pancreatitis, corroborado desde otro capítulo

El motor aplica **37,5 g/1000 kcal** en `pancreatitis`, que salen del ≤15 % MS de
la Tabla 67-3. El capítulo 48 dice lo mismo desde el lado general, sin hablar de
pancreatitis: *«Patients with GI or pancreatic disease may not tolerate high-fat
foods (**>25 % DM**) … Foods containing **moderate amounts of fat (12 a 15 % DM
for dogs)** are generally tolerated and have sufficient caloric density for most
patients»*.

Nuestro 37,5 **es** el 15 % MS, o sea el extremo alto de lo que este capítulo
llama tolerado. Dos capítulos independientes del mismo libro y el mismo número.

Y trae el aviso que explica por qué no se baja más: *«foods containing **less
than 10 % DM fat need to be fed in larger volumes** to meet the patient's caloric
requirement. **Some patients may not tolerate this volume of food**»*. Que es,
dicho por la fuente, la frontera física que la medida del 8 de septiembre
encontró con el catálogo: por debajo de 25 g no salía menú.

#### 48.3 · La fibra en enfermedad digestiva, y por qué no cambia nada aquí

*«It is unusual for GI foods to contain crude fiber levels greater than **5 % DM**
because fiber reduces dry matter digestibility and decreases pancreatic enzymatic
activity in vitro»*, y por el otro lado la fibra insoluble es lo primero para la
diarrea de intestino grueso: *«increasing the insoluble fiber content of the food
resolves or modulates most cases of colitis»*.

**No se aplica**: la fibra no es uno de los 43 requisitos de FEDIAF —la fila
«Fibra» con mínimo y máximo inventados es justo la que se coló en agosto y se
quitó— y el motor no la restringe ni la exige. Queda escrito porque las siete
patologías digestivas que están apuntadas en `PENDIENTE_PRODUCTO.md` van a
necesitar exactamente este eje, y este es el capítulo que lo define.

#### 48.4 · Gluten y gliadina: existe en el perro y no nos toca

*«An analogous condition, termed **wheat-sensitive enteropathy**, has been
identified in **Irish setter** dogs»*, por la gliadina de trigo, cebada, centeno,
trigo sarraceno y avena; no la hay en arroz ni maíz.

**No aplica al motor**: el catálogo de Rawku no tiene cereales. Se escribe para
que no se «descubra» dentro de seis meses y para que quede claro que la ausencia
es del catálogo, no un olvido.

#### 48.5 · Y una regla de método que vale para toda la app

*«All too often, relative terms such as "low" vs. "high" are used **without
stating the point of reference**»*. Es la misma norma que ya sigue el proyecto al
escribir cada tope con su cifra y su base (`UNIDADES.md`), dicha por la fuente.

---

### Capítulo 55 · Introducción a las enfermedades del intestino delgado — leído entero

Corto, casi todo fisiopatología de la diarrea, y trae **tres cosas que tocan a
Rawku**, dos de ellas con cifra.

#### 55.1 · ⚠️ «Raw meat consumption» está en la lista de causas de diarrea aguda

Tabla 55-1, columna «Dietary», literal y en este orden: *«Dietary indiscretion ·
Foreign bodies · Garbage toxicity · **Raw meat consumption**»*, y en la columna
de al lado los agentes: *Bacillus, Campylobacter, Clostridium, Escherichia coli,
Salmonella, Staphylococcus, Yersinia*.

Es el libro de referencia poniendo **la comida cruda** —lo que hace este
producto— en su lista de causas, para el perro sano y no solo para el
inmunodeprimido, que es donde `patologias.json` lo tenía escrito hasta hoy.

**Y no deja un hueco: corrobora lo que la app ya hace.** El panel de
«Congelación» de `instrucciones.js` en `canislab-web` ya da los tiempos (una
semana, dos el pescado, tres días una vez descongelado) y la ficha de pescados y
mariscos ya dice qué va crudo y qué cocinado. Esta es la fuente que sostiene ese
panel, y hasta hoy no estaba citada en ningún sitio.

#### 55.2 · La lactosa tiene un número, y hay un lácteo en el catálogo

Recuadro 55-3, literal: *«In one study, **dogs developed diarrhea while consuming
more than 1 g of lactose/kg body weight**, an amount equivalent to about 20 ml
milk/kg body weight or three-fourths cup of milk for a 10-kg dog»*. Y el
mecanismo: el perro adulto tiene poca lactasa, la lactosa sin hidrolizar llega al
colon y arrastra agua.

**En el catálogo hay un lácteo**: «Yogur griego», en Extras.

**Medido hoy sobre el catálogo regenerado: 0 de los 216 menús lo usan.** O sea
que hoy no aprieta a nadie. Pero Extras va **siempre libre** (regla 5 del
`CLAUDE.md`: es una de las herramientas con las que el motor cierra los 43
requisitos), así que un menú personalizado sí puede meterlo, y no hay nada que lo
tope por este motivo.

⚠️ **No se aplica, y por una razón concreta**: la lactosa **no es uno de los 41
nutrientes** del catálogo, así que el motor no sabe cuánta lleva el yogur. Poner
el dato es rellenar el catálogo, y eso no lo hace el asistente. Va a
`PENDIENTE_NUTRICION.md` con la cifra y la cuenta hecha.

#### 55.3 · Más razas asociadas, y una que ya conocíamos

Tabla 55-3, «Breed-associated small intestinal disorders» — la segunda tabla de
raza del día, después de la 38-11 de los urolitos:

| Trastorno | Razas |
|---|---|
| Gastroenteritis eosinofílica | pastor alemán, setter irlandés |
| Gastroenteritis hemorrágica | teckel, caniche miniatura, schnauzer miniatura |
| Enteritis linfoplasmocítica | pastor alemán, shar-pei, soft-coated wheaten terrier |
| Sobrecrecimiento bacteriano | pastor alemán, beagle |
| Linfangiectasia | yorkshire, golden retriever, teckel, basenji |
| Enteropatía sensible al trigo | setter irlandés |

Mismo criterio que con la 38-11: **no se aplica nada**. Una predisposición de
raza no es un diagnóstico.

Y la enteropatía por gliadina vuelve a salir (recuadro 55-2), con el detalle de
que el perro afectado da síntomas **antes de los seis meses** y que la gliadina
no está en arroz, maíz ni patata. Sigue sin tocarnos: el catálogo no tiene
cereales.

---

### Capítulo 47 · Enfermedad periodontal — leído entero

Otro de los 26 sin citar, y **el que más toca a Rawku de los cuatro de hoy**. Es
un capítulo de perro y gato, con dos tablas de cifras y un recuadro que habla
directamente de la dieta cruda.

#### 47.1 · ⚠️ LO QUE DICE DE LOS HUESOS CARNOSOS, Y HAY QUE LEERLO ENTERO

El recuadro 47-6 se titula «Natural Food Sources and Periodontal Disease» y trae
**el estudio de los 67 foxhounds ingleses**, de uno a nueve años, alimentados de
rutina con carcasas crudas —esqueleto, músculo y tejidos asociados—: *«Oral
examinations revealed that **all dogs had varying signs of periodontal disease as
well as a high prevalence of tooth fractures**»*.

Y el caso 47-1, respuesta 2, va directo al argumento del «hueso carnoso crudo»:

> *«there are **no reliable, published studies showing dental benefits derived
> from bone chewing** … Current theory proposes that uncooked bones are not as
> hard as cooked bones and do not fracture teeth …; however, **anecdotal reports
> suggest the health concerns presented with cooked bones also occur commonly
> with raw, meaty bones** … The **safety and efficacy of feeding bones, regardless
> of type, remain undetermined**. Veterinarians should be cautious about
> recommending bones for dental benefits.»*

**Lo primero que se hizo con esto fue comprobar qué dice la app**, porque una
afirmación falsa en la pantalla sería lo grave. **No la hay**: `instrucciones.js`
en `canislab-web` no promete beneficio dental en ninguna parte. Lo que dice del
hueso carnoso es lo contrario —crudo siempre, entero o en trozos grandes, que lo
roa y no lo trague, supervisado, esperar a las 14 semanas para los duros— y la
app tiene además la vía del senior sin dientes, que puede quitar la categoría
entera.

O sea que Rawku **no vende el argumento que la fuente desmonta**. Lo que sí hace
falta es que esa cautela esté citada: el aviso de `seguridad.py`
(`HUESO_RIESGO_ASTILLADO`) tenía la cifra de Rousseau 2007 y no esta.

⚠️ **Y una cosa que NO se cambia sola**: el hueso carnoso está en el motor porque
es la fuente de calcio de una ración BARF, no por los dientes. Este capítulo no
toca esa razón. Lo que quita es un beneficio que nunca prometimos.

#### 47.2 · ⚠️ EL FÓSFORO 2000 Y EL SODIO 1000 TIENEN UNA SEGUNDA FUENTE, Y ES ESTE CAPÍTULO

Los dos techos de `recomendaciones_libro.json` para el adulto sano salen de la
Tabla 13-3 (cap.13, «Feeding Young Adult Dogs»). La Tabla 47-4 de este capítulo,
escrita por otros autores y para otra cosa, da **exactamente los mismos rangos**:

| | Tabla 13-3 (cap.13) | Tabla 47-4 (cap.47) | Lo que aplicamos |
|---|---|---|---|
| Fósforo | 0,4-0,8 % MS | 0,4-0,8 % MS | techo 2000 mg/1000 kcal |
| Sodio | 0,2-0,4 % MS | 0,2-0,4 % MS | techo 1000 mg/1000 kcal |

Y el texto dice **por qué** están ahí, que es lo que faltaba: *«Phosphorus and
sodium are considered key nutritional factors for apparently healthy adult dogs
and cats for purposes of **ameliorating or slowing the progression of subclinical
kidney disease and/or hypertension**»*. O sea que no son un capricho del capítulo
del adulto joven: son una medida de prevención renal y cardiovascular para el
perro **que no tiene nada diagnosticado**, que es exactamente la clase de límite
que `recomendaciones_libro.json` existe para guardar.

Dos capítulos independientes, los mismos dos números, y ahora con el motivo
escrito.

#### 47.3 · Tres cifras más de la Tabla 47-4, ninguna aplicable hoy

| Nutriente | Tabla 47-4 (perro) | En nuestras unidades |
|---|---|---|
| Vitamina E | ≥400 UI/kg MS | ≥67,1 mg/1000 kcal |
| Vitamina C | ≥100 mg/kg MS | ≥25 mg/1000 kcal |
| Selenio | 0,5-1,3 mg/kg MS | 125-325 µg/1000 kcal |

- La **vitamina E**: el mínimo de FEDIAF en adulto ya está por encima de esa
  cifra en el menú real, así que no aprieta. Y el techo sugerido por el NRC que
  salió del cap.7 (167,75 mg/1000 kcal) sigue siendo el número relevante.
- La **vitamina C** no es uno de los 43 requisitos: el perro la sintetiza y
  FEDIAF no le pone requisito. Aquí es un antioxidante «para mejor rendimiento»,
  no un requerimiento. **No se aplica.**
- El **selenio**: es el **tercer sitio del libro** con el mismo rango (cap.7,
  Tabla 35-3 y ahora la 47-4). Y sigue chocando con lo mismo: 125 µg de suelo
  contra un máximo legal de FEDIAF de 142. No cambia nada.

#### 47.4 · Y dos frases sobre la comida casera, que son la razón de ser de esto

*«Improperly formulated **homemade foods** are more likely to be **deficient in
calcium**»* y *«Adequate vitamin content can be a problem in improperly
formulated homemade foods»*, con la lista de lo que se ve en la boca cuando
faltan: vitamina A (gingivitis marginal, reabsorción de hueso alveolar), complejo
B (inflamación gingival, necrosis epitelial), vitamina D (encía, ligamento
periodontal, hueso alveolar).

Es lo que hace este motor, dicho por la fuente y con las consecuencias
enumeradas. Y añade una que no teníamos escrita: *«Experiments in dogs have
demonstrated **resorption of alveolar bone** following consumption of a food with
a **low ratio of calcium to phosphorus**»* — el ratio Ca:P, que el motor ya
verifica como una de las 43 filas, tiene aquí su consecuencia clínica concreta.

#### 47.5 · Los premios, por cuarta vez

*«Generally, feeding excessive amounts (**>10 % of the total food intake** on a
volume or calorie basis) of any treat is not recommended»*. Es la cuarta fuente
que los nombra (FEDIAF §4.1, SACN5 cap.17, SACN5 cap.1 y ahora el 47), y la
primera que da **una cifra**. Rawku sigue sin modelarlos. Va a
`PENDIENTE_PRODUCTO.md`.

---

### Capítulo 69 · Efectos de la comida sobre la farmacocinética — leído entero

⚠️ **El de más consecuencias directas de todos los que van leídos hoy**, y no
porque cambie un número del motor: no cambia ninguno. Cambia lo que hay que
DECIR. Rawku cambia la dieta de un perro, y este capítulo es el que explica qué
le pasa a la medicación cuando la dieta cambia.

#### 69.1 · ⚠️ EL BROMURO Y EL CLORO: un perro epiléptico con crisis por cambiar de comida

Caso 69-1, y es un perro real. Teckel de 11 años con epilepsia idiopática,
controlada con bromuro potásico, **dos meses sin crisis** y bromo sérico en
1.100 mg/l. Le cambian la comida a una dieta disolvente de estruvita —más sal— y
**dos semanas después tiene un racimo de cinco crisis en 36 horas**. El bromo
sérico había caído a **410 mg/l**, muy por debajo del rango terapéutico
(1.000-2.000), sin que nadie tocara la dosis.

El mecanismo, literal: *«Bromide and chloride **compete for renal tubular
reabsorption**. An increase in chloride load … will markedly increase urinary
excretion of bromide in several species, **including dogs**»*.

Las dos comidas del caso, en cloro sobre materia seca: la buena **0,65 %**, la
que dio el problema **2,41 %**.

**Medido hoy sobre los 216 menús del catálogo regenerado:**

| | mg/1000 kcal | % materia seca |
|---|---|---|
| mínimo | 424 | 0,17 |
| mediana | 826 | 0,33 |
| máximo | 2.973 | 1,19 |

O sea que la mediana de una ración de este motor es **la mitad de cloro** que la
comida que mantenía estable a ese perro, y el máximo se queda por debajo de la
que le provocó las crisis.

⚠️ **Y por eso el riesgo va AL REVÉS que en el caso.** Menos cloro es menos bromo
excretado, o sea bromo sérico **que sube**. Un perro que viene de un pienso y
pasa a esta ración puede irse hacia la **toxicidad por bromuro** (sedación,
ataxia), no hacia la crisis. Es la misma competencia leída en la otra dirección,
y es la que nos toca a nosotros.

**Aplicado**: `epilepsia_idiopatica` gana el aviso `bromuro_y_cloro` en
`patologias.json`, con el caso, el mecanismo, las dos cifras del libro y las tres
nuestras. No es un tope: el menú no cambia, y bajar o subir el cloro no sería más
seguro — sería otro cambio. Lo que corresponde es que el veterinario **mida el
bromo sérico** después del cambio de dieta, que es literalmente lo que dice el
caso.

#### 69.2 · Y el fenobarbital, con 27 beagles

Maguire et al. (2000), en el mismo capítulo: 27 beagles adultos, farmacocinética
del fenobarbital antes y dos meses después de cambiarles la comida. Restringir
**proteína** o **grasa** acortó la vida media:

| Comida | Vida media (h) |
|---|---|
| mantenimiento | 32,9 ± 5,2 |
| renal (baja en proteína) | 25,9 ± 6,1 |
| adelgazamiento (baja en grasa) | 24,0 ± 4,7 |

Conclusión de los autores, literal: *«**phenobarbital dosage should be
reevaluated if a dog's diet, body weight or body composition changes during
treatment**»*.

Una ración BARF es **alta** en proteína, así que el cambio va en la dirección
contraria a la dieta renal del estudio — y sigue siendo un cambio. El aviso lo
recoge junto al del bromuro, porque el perro epiléptico suele llevar uno de los
dos fármacos, o los dos.

#### 69.3 · El mitotano del Cushing: treinta veces más con comida que en ayunas

Caso 69-2, Tabla 1, concentración plasmática máxima en el perro:

| Cómo se da | mg/l |
|---|---|
| Comprimidos **en ayunas** | 0,4 |
| Comprimidos **con comida** | 13,0 |
| Comprimidos molidos en aceite con comida | 15,4 |

*«Mitotane is soluble in fat but poorly soluble in water»*, y la consecuencia
clínica: *«**Failure to administer the drug with food may contribute to the
apparent "resistance"** to the effects of the drug seen in some dogs with
hyperadrenocorticism»*. Un perro que no responde puede no ser resistente: puede
ser un perro al que le dan la pastilla en ayunas.

**Aplicado**: `cushing` gana el aviso `mitotano_con_comida`, con la tabla y con
la cosa que el dueño sí puede vigilar — *«the owners should observe the dog's
appetite closely before administering the daily mitotane dose»*, porque perder el
apetito es el primer signo de toxicidad. Tampoco cambia el menú: una ración de
este motor lleva grasa de sobra.

#### 69.4 · La tiaminasa del pescado crudo, otra vez y desde otro sitio

*«thiamin to replace that lost to **thiaminase activity in raw fish**»*, en la
lista de suplementaciones indicadas para contrarrestar efectos de fármacos y
dietas. Es uno de **los cinco topes de seguridad crónica** que el motor ya aplica
como restricción dura dentro del solver. No cambia nada; es la enésima fuente que
lo dice, y esta desde el capítulo de farmacocinética.

#### 69.5 · Lo demás, medido y sin efecto

- **Proteína alta y metabolismo hepático de fármacos**: *«High-protein (44 vs. 10 %
  of kcal) … foods enhance the hepatic metabolism and excretion of many different
  drugs»*. Una ración BARF está en el extremo alto. Es el mecanismo general
  detrás de lo del fenobarbital, y no hay cifra canina para nada más.
- **Proteína y gentamicina**: subir la proteína en el perro de 9,4 a 27,3 % MS
  **aumenta** la eliminación de gentamicina y **reduce** su nefrotoxicidad. Va a
  favor.
- **Calcio y magnesio de la dieta** reducen la acumulación tubular renal de
  aminoglucósidos: también a favor.
- **Obesidad**: cambia el volumen de distribución de los fármacos lipófilos y de
  los polares en direcciones opuestas, y *«must be considered whenever a
  patient's body weight changes markedly»*. Rawku ya calcula sobre el peso
  objetivo, no el real.
- **Pomelo, hipérico, tiramina de quesos curados, metilxantinas**: nada de eso
  está en el catálogo.

---

### Capítulo 4 · Nutrigenómica y nutrigenética — leído entero

Otro de los 26 sin citar, y hay que decirlo claro: **no trae ni una cifra
aplicable**. Es un capítulo de método —transcriptómica, proteómica,
metabolómica—, con el estado del genoma canino (2,4 Gb, ~19.300 genes, secuenciado
de un bóxer hembra) y más de 450 enfermedades genéticas descritas en el perro.

Lo único que toca a algo nuestro es una frase de pasada que **corrobora por cuarta
vez** el techo de calcio del cachorro de raza grande: *«large- and giant-breed
puppies with genetic variation that responds to diet for the **prevention of
developmental orthopedic disease**»*. Los otros tres sitios son Fascetti cap.10 y
SACN5 caps. 1 y 33.

Se deja escrito que está leído entero y que no hay nada más, para que nadie tenga
que volver.

---

### Capítulo 26 · Alimentación parenteral asistida — leído entero

De los que quedaban sin cita, y hay que decirlo sin adornos: **es nutrición
intravenosa de hospital**. Bolsas de tres en uno, catéteres yugulares y
periféricos, osmolaridades, compatibilidad de fármacos con el complejo B. Nada de
eso es una ración BARF en casa.

Se deja escrito que está leído entero para que nadie tenga que volver, y con las
dos únicas cosas que se pueden leer fuera del hospital:

- **El síndrome de realimentación.** Caso 26-3: un gato que llevaba sin comer,
  al que se le pasó de por debajo del gasto en reposo a un 40 % por encima entre
  la vía intravenosa y la sonda, y a las 24 horas tenía potasio 2,7 y fósforo
  1,2. La regla del libro: *«All patients fed with PN, enteral nutrition or both
  should initially be fed at RER»* — al gasto en REPOSO, no por encima, y sin
  «factores de enfermedad». **No aplica a Rawku**: un perro que lleva tres días
  sin comer no está pidiendo una ración BARF, está en el veterinario. Queda
  escrito porque es el único sitio del libro donde alimentar de MÁS es el daño.
- Las soluciones de aminoácidos *«contain all the essential amino acids for dogs
  and cats, **except taurine**»*. La taurina no es uno de los 43 de FEDIAF para
  el perro. Sin efecto.

---

### Capítulos 54, 56 y 59 · La familia digestiva, ahora enteros

Los tres estaban leídos **solo por sus tablas** (54-2, 56-2 y 59-1), que ya
están transcritas en la §cuarta pasada de `VERIFICACION_FILA_A_FILA.md`. Leerlos
enteros confirma las tres tablas y añade **una cosa importante y dos menores**.

#### ⚠️ 56.1 · EL PÁRRAFO DE LA COMIDA CRUDA, Y ESTE SÍ NOS TOCA

Capítulo 56 («Acute Gastroenteritis and Enteritis»), sección de factores de
riesgo, literal:

> *«Consumption of **raw food diets** has been associated with bacterial
> enteritides (Chengappa et al, 1993; Stone et al, 1993; Morley et al, 2006).
> Cultures of **home-prepared** and commercially available raw foods have
> demonstrated bacterial pathogens including Salmonella spp., Campylobacter
> spp., Escherichia spp. and Yersinia spp. (Weese, 2006; Strohmeyer et al, 2006).
> **Dogs consuming such foods SHED bacterial pathogens at a much higher rate than
> those consuming conventionally cooked commercial foods** (Weese and Armstrong,
> 2006).»*

Y antes: *«Feeding uncooked meat in homemade foods and racing greyhound rations
is linked to bacterial enteritis … Incorporation of raw poultry in foods has been
linked to campylobacteriosis and salmonellosis»*.

**Lo que esto añade a lo que ya había.** `patologias.json` tiene el riesgo
escrito en `inmunosupresion`, y está bien escrito, pero habla del **perro**: un
sistema inmune débil aguanta peor un patógeno. Este párrafo dice otra cosa: que
**el perro que come crudo EXCRETA más patógenos**, o sea que el riesgo no es solo
suyo, es de quien vive con él — niños pequeños, embarazadas, mayores,
inmunodeprimidos de la casa.

Rawku **no dice eso en ninguna parte**. Lo que hay en `instrucciones.js` de
`canislab-web` son los tiempos de congelación y qué va crudo y qué cocinado, que
es manipulación del alimento, no higiene de la casa. Va a
`PENDIENTE_PRODUCTO.md`, y el aviso de `inmunosupresion` gana la parte que le
faltaba.

#### 59.1 · «Lactose free», y es la segunda vez hoy

La Tabla 59-1 (síndrome de intestino corto) lleva una fila que no es un número:
**`Carbohydrate: Lactose free`**, porque *«extensive small bowel resection
results in loss of lactase and other brush border disaccharidases»*.

Es la **segunda fuente del día** que señala la lactosa, después del umbral de
**1 g/kg de peso** del recuadro 55-3. El catálogo tiene un lácteo y no tiene el
dato. Ya está apuntado en `PENDIENTE_NUTRICION.md` y en `DATOS_QUE_FALTAN.md`;
esto solo lo refuerza.

#### 54.1 · Lo que la Tabla 54-2 no dice, y son cosas de manejo

- El estómago del perro se vacía en **6-8 horas** tras una comida media (4-6 en
  el gato).
- **La comida fría retrasa el vaciado**: ofrecerla entre **21 y 38 °C**. ⚠️ Ojo,
  porque `instrucciones.js` recomienda dar el cuello de pollo **semicongelado** a
  los perros tragones, para que lo roan en vez de tragárselo. Las dos cosas son
  ciertas y no chocan —una es para un perro con un trastorno de vaciado gástrico
  y la otra para evitar un atragantamiento en un perro sano— pero conviene que
  esté escrito el día que se ofrezcan menús para esos trastornos.
- **Las comidas grandes se vacían más despacio**: al menos tres al día.
- **Las fibras gelificantes** (pectinas y gomas: arábiga, guar, carragenato,
  psyllium, xantana, garrofín, ghatti, tragacanto) retrasan el vaciado y hay que
  evitarlas. Ninguna está en el catálogo de Rawku.
- La grasa en el duodeno libera colecistoquinina y retrasa el vaciado: es el
  mecanismo detrás del ≤15 % MS de grasa de la tabla.
- Razas: braquicéfalos (estenosis pilórica congénita) y lhasa apso, maltés, shih
  tzu y pequinés (gastropatía pilórica hipertrófica crónica). Tercera tabla de
  raza del día; mismo criterio que las otras dos, no se aplica sola.

---

### Capítulo 25 · Nutrición de cuidados críticos y alimentación enteral asistida — leído entero

El último de los caninos que quedaban sin cita. Como el 26, es de hospital
—sondas nasoesofágicas, de esofagostomía, de gastrostomía, de yeyunostomía— y
**casi todo él no aplica**. Pero, a diferencia del 26, trae **tres cosas que sí**,
y una de ellas es un número que el dueño puede medir en casa.

#### ⚠️ 25.1 · CUÁNTO PUEDE ADELGAZAR UN PERRO A LA SEMANA, Y NO ESTABA EN NINGÚN SITIO

Literal, sección «History and Physical Examination»:

> *«Pets on a designated weight-loss program can safely lose **1 to 4%, more
> typically 1 to 2%, of their body weight per week** (Laflamme, 1993).»*

Y la frase de al lado, que es la que evita el susto:

> *«a weight change of **10 to 15% within several days is most likely a hydration
> problem** and should be corrected first with medical or fluid management.»*

**Comprobado hoy: la cifra no estaba en el repo.** `obesidad` en `patologias.json`
tenía el tope de grasa (30 g/1000 kcal, de la Tabla 27-4) y el aviso de que se
adelgaza bajando kcal sobre el peso objetivo, pero **ningún ritmo**. Sin ritmo,
«adelgazamiento dirigido» no tiene forma de comprobarse desde casa: la báscula
sube o baja y nadie sabe si eso está bien.

Aplicado como aviso `ritmo_de_perdida_de_peso`, con la cuenta hecha: un perro de
30 kg pierde bien entre 300 y 600 g a la semana, como mucho 1,2 kg; uno de 5 kg,
entre 50 y 100 g. No cambia el menú.

#### 25.2 · El omega-3 también tiene un lado malo, y es la otra cara de dos pendientes

`patologias.json` lleva dos entradas en
`limites_escritos_que_el_solver_no_aplica` porque el omega-3 que piden las tablas
de **cáncer** y de **artrosis** no cabe con el catálogo real. Este capítulo dice
lo contrario desde el otro extremo, y con cifras:

> *«chronic suppression of the inflammatory and/or immune response by feeding
> high levels of omega-3 fatty acids should be done cautiously and **is not
> warranted in disease states in which a fully competent immune system is
> essential for survival and recovery**.»*

- Ratones prealimentados dos a cuatro semanas con **40 % de las calorías como
  aceite de pescado** tenían **comprometida la resistencia** a una enfermedad
  infecciosa (Chang et al, 1992).
- Gatos sanos con una dieta de **omega-6:omega-3 de 1,3:1** durante ocho semanas
  tuvieron la **función plaquetaria significativamente disminuida** (Saker et al,
  1998).

Y la frase de cierre: *«As with many other nutrients, **excessive levels of
omega-3 fatty acids can be detrimental**»*.

**Lo que esto cambia**: nada del motor, y mejora una pregunta. Que esos dos
suelos de omega-3 no quepan deja de ser solo un problema del catálogo — la propia
fuente dice que pasarse tiene coste. Va a la pregunta del nutricionista, no a un
tope.

#### 25.3 · Y el ratio omega-6:omega-3, que es una de las tres cosas que Cris echó de menos

`REVISION_NUTRICIONISTA.md` lista el **ratio omega-6:omega-3** como una de las
tres que siguen sin estar. Este capítulo trae una cifra, y hay que leerla con
cuidado:

> *«The dietary dose that favors a less inflammatory cascade during a disease
> process **is still not standardized across veterinary patients**, but is
> suggested as an **omega-6:omega-3 fatty acid ratio ranging between 5:1 to
> 1:1**, depending on patient assessment.»*

⚠️ **No se aplica, y por tres motivos que conviene tener escritos:**
1. Es para el **paciente crítico** en un proceso inflamatorio, no para el perro
   sano que usa esta app.
2. La propia fuente dice que **no está estandarizado**.
3. El **NRC 2006** dice del ratio de omega-6:omega-3 **totales** que *«is not
   helpful»*, y recomienda en su lugar el **linoleico:linolénico**, que es
   justamente el que el motor **sí aplica** desde ayer (2,6-26 en adulto y
   crecimiento, 2,6-16 en gestación y lactancia), vía
   `requisitos_condicionales.json`.

O sea que la pregunta de Cris tiene ahora **dos respuestas escritas y en
tensión**: una fuente que da un rango para el enfermo crítico y otra que dice que
el ratio total no sirve. Eso es exactamente lo que hay que ponerle delante al
nutricionista, en vez de elegir por él.

#### 25.4 · Lo demás, leído y sin efecto

- **Tabla 25-5**, factores clave para alimentación enteral: osmolaridad 250-400
  mOsm/l, densidad 1-2 kcal/ml, hidratos 2-4 g/100 kcal, proteína 5-12 g/100 kcal
  en el perro, arginina ≥146 mg/100 kcal, glutamina ≥500 mg/100 kcal, grasa 5-7,5
  g/100 kcal. Son cifras **por 100 kcal de comida líquida por sonda**. No hay
  ninguna ración masticable detrás.
- **El síndrome de realimentación** otra vez (recuadro 25-3), con la misma regla
  que el cap.26: no pasar del gasto en reposo al realimentar. No aplica.
- *«Patients fed **homemade foods**, table foods, vegetarian or single item foods
  are at greater risk for developing subclinical nutritional imbalances»* — la
  razón de ser de este motor, dicha una vez más.
- Los **potes de comida de bebé** llevan *«only 10 % of the calcium required by
  dogs and cats»* y a veces polvo de cebolla. No están en el catálogo.

---

## FEDIAF · el 66 % del texto que nunca había pasado por el extractor (10 de septiembre)

**Elena, esta mañana:** *«anoche me dijiste que de FEDIAF TODO LEÍDO BIEN CON
TABLAS Y TEXTO, hoy dices que no. ¿Qué está fallando?»*

La pregunta es la buena, y la respuesta se puede medir. **«Leído» ha significado
tres cosas distintas** y las he usado como si fueran una:

| | Qué significa | Cómo estaba FEDIAF |
|---|---|---|
| 1 | Sacado del PDF entero, sin perder texto | ✅ sí |
| 2 | Con veredicto para cada tabla **y cada frase** | tablas sí (34/34); **texto solo el 34 %** |
| 3 | Aplicado, o descartado con motivo escrito | lo que salía del 2 |

Las 11 secciones que tenían desglose cubrían **1.790 de las 5.305 líneas** del
documento. El otro 66 % nunca había pasado por `leer_fuente.py`. Y ahí es
exactamente donde estaba lo que seguía apareciendo después de cada «ya está
leído»: **la regla del máximo legal no lleva ni un número**, así que un
inventario de tablas no puede verla.

**Hoy son 21 secciones, el 100 % de las líneas y 498 de 498 elementos con
veredicto.** Lo vigila el BLOQUE 68.

### F-11 · El tope de suplementación del selenio ORGÁNICO, que no estaba en ninguna parte

Nota **d** de las tablas III-3a/b/c y VII-17a-d, literal del PDF (página 21):

> *«For organic selenium a maximum supplementation level of **22.73 µg organic
> Se/100 g DM** (0.20 mg organic Se/kg complete feed with a moisture content of
> 12 %) applies.»*

Puesto en la unidad del motor: 22,73 µg/100 g MS = 227,3 µg/kg MS, y a 4000
kcal/kg MS son **56,8 µg/1000 kcal**. El tope de selenio que aplica el motor son
**570 µg/1000 kcal** (AAFCO, `seguridad.py`), o sea **diez veces más alto**.

**No son el mismo límite y hay que decirlo bien:** el de FEDIAF acota el selenio
**orgánico que se AÑADE** —selenometionina, levadura selenizada—, no el selenio
total del alimento, que es lo que mide el motor. Un menú de carne y vísceras
lleva su selenio de la matriz, no añadido.

**Pero no estaba escrito en ninguna parte del repo**, y decide algo el día que
entre al catálogo un suplemento con selenio orgánico declarado. Queda anotado, y
lo que falta es dato y no código: ninguna ficha dice en qué **forma química**
viene su selenio, que es el mismo hueco de las vitaminas del grupo B
(`DATOS_QUE_FALTAN.md`).

### F-12 · El hierro inerte no cuenta contra el máximo legal

De la sección **3.3.1**, la del PERRO —el registro de cambios lo confirma: *«b. 3.3.1.
Following sentence was added under header “iron”»*—, y son **dos** cosas en la misma
frase:

> *«Because of very poor availability, iron from oxide or carbonate salts that
> are added to the diet **should not be considered sources** contributing to the
> minimum nutrient content. In addition, **the amount of inert iron is not to be
> taken into consideration for the calculation of the total iron content of the
> feed for EU legal maximum**.»*

La primera mitad ya la teníamos por SACN5 (`sacn5_fuentes_de_minerales.json`, 9
de septiembre): el óxido de hierro no cuenta como fuente. **La segunda es nueva:
tampoco cuenta contra el techo.** Hoy no cambia ningún menú —no hay ninguna
ficha con óxido ni carbonato de hierro— y queda escrito para el día que alguien
proponga añadir una. Y el óxido de cobre lo dice FEDIAF con las mismas palabras
que SACN5: dos fuentes independientes, misma conclusión.

### F-13 · El registro de cambios por año confirma cuatro números del motor

La sección 8 es el changelog de FEDIAF desde 2011, y sirve para lo contrario de
lo habitual: **verificar que aplicamos la versión vigente y no una anterior.**

| Lo que dice el changelog | Lo que aplica el motor | |
|---|---|---|
| Máximo legal de **zinc**: de 28,40 a **22,70** mg/100 g MS | 56,75 mg/1000 kcal (= 22,70 × 10 ÷ 4) | ✅ |
| Máximo legal de **hierro**: de 142,00 a **68,18** mg/100 g MS | 170,45 mg/1000 kcal (= 68,18 × 10 ÷ 4) | ✅ |
| Tabla VII-14, **piridoxina**: de 0,89 a **0,82** mg | 0,82 en `fediaf_conversiones_vitaminas.json` | ✅ |
| Los máximos nutricionales de **calcio (6,25 g)** y **fósforo (4 g)** por 1000 kcal son de **AAFCO 1992**, «out of concern for the risk of nutrient excess» | 6250 y 4000 mg | ✅ |

Ninguna de las cifras **viejas** está en el repo. Y la última fila contesta de
paso una pregunta que llevaba semanas abierta: **de dónde sale el máximo de
fósforo del adulto** y por qué el cachorro no tiene ninguno.

### F-14 · Un estudio que respalda el calcio del cachorro, y va muy por encima del nuestro

De la sección 3.3.1, y **releído sobre el texto bueno**, porque la primera
versión de este apartado lo contaba mal:

> *«While the current **SUL of Ca and P for adult dogs is extrapolated from
> puppies**, the work of Stockman J et al. (2017) demonstrated these values being
> appropriate. In this study a diet providing **7,1 g/1000 kcal of total Ca and
> 4,5 g/1000 kcal of total P (Ca:P 1,6:1)** was well tolerated over a period of
> 40 weeks, with no adverse effects noted.»*

Dice dos cosas, y la primera no la sabíamos: **el límite superior seguro de
calcio y fósforo del perro ADULTO está extrapolado del cachorro**, no medido en
adultos. Stockman 2017 es el trabajo que lo respalda a posteriori, con un
alimento que llevaba **por encima** de los máximos publicados (7,1 contra 6,25
de calcio; 4,5 contra 4 de fósforo) y no hizo daño en 40 semanas.

Para el motor no cambia ningún número —seguimos aplicando 6250 y 4000, que es lo
que publica FEDIAF—, pero sí cambia lo que se puede afirmar de ellos: **no son
una frontera medida en el animal al que se aplican.**

### Y lo que NO ha aparecido, que también es un resultado

De los 256 elementos nuevos, la gran mayoría son de tres sitios donde no había
nada que aplicar, y ahora está escrito por qué:

- **§3.3.2**, la sustanciación del **gato** (45 cifras). Se leyó igual porque
  varias de sus frases hablan de las dos especies, y de ahí salieron F-12 y la
  confirmación del óxido de cobre.
- **§5 y §6**, los métodos analíticos y el **protocolo del ensayo de
  digestibilidad** (24 cifras): cuántos perros, cuántos días de recogida, en qué
  se conserva la orina. Es lo que hace un fabricante para validar un pienso. El
  motor no hace ensayos: usa la ecuación predictiva de §7.2, que sí estaba
  desglosada.
- **§9**, las referencias.


---

## ⚠️ Y LO QUE HAY QUE RELEER: todas las citas sacadas de los `.txt` viejos

Lo de arriba se escribió el 10 de septiembre por la mañana, sobre el texto
extraído **conservando la disposición visual**. Ese mismo día, por la tarde, se
descubrió que ese texto pegaba las **dos columnas** de cada página: el **49,3 %**
de las líneas de FEDIAF y el **37,5 %** de las de SACN5.

**Las cuatro de hoy (F-11 a F-14) se han vuelto a comprobar contra el texto
bueno**, y una de ellas —F-14— decía algo distinto de lo que dice la fuente: se
ha corregido. F-12 estaba en la sección del gato y en realidad está en la del
perro.

Lo que queda pendiente y no es opcional: **releer contra el texto bueno toda
cita de este documento anterior al 10 de septiembre**, y las de
`PARA_EL_NUTRICIONISTA.md`, `PATOLOGIAS.md` y `LECTURA_SACN5.md`. Una cita
sacada de un texto con las columnas pegadas puede decir algo que la fuente no
dice, y esa es la peor clase de error que puede tener este repo: tiene forma de
dato bueno y lleva comillas.

---

## FEDIAF, LEÍDO ENTERO Y BIEN — las 532 celdas y frases, con veredicto (10 de septiembre)

Segunda pasada, ya sobre el texto con las columnas en orden. **El 100 % de las
10.683 líneas está en una sección desglosada y las 532 cifras y frases tienen
veredicto.** Lo vigila el BLOQUE 68, que además exige que la unión de las
secciones sea el documento entero — sin eso, una auditoría que solo mira lo
declarado premia declarar poco, que es como se pudo decir «FEDIAF leído entero»
con dos tercios fuera.

Lo que sigue es lo que apareció y no estaba en el repo.

### F-15 · El anexo 7.7 entero: los alimentos humanos tóxicos ✅ APLICADO

FEDIAF dedica un anexo a **uva, pasa, chocolate, cebolla y ajo**, con las dosis:

> *«The lowest intake that has so far been reported to cause poisoning is around
> **2,8 g of raisins per kg bodyweight** and **19,6 g of grapes per kg BW**; one
> dog became ill after only eating 10 to 12 grapes… **The severity of the illness
> does not seem to be dose-related**.»*

Y del chocolate: la teobromina tiene una vida media de 17,5 h y recirculación
enterohepática, así que *«repeated intakes of smaller (non-toxic) quantities may
still cause intoxication»*.

**No estaba en ninguna parte del repo.** Y el motivo por el que no se notó es el
peor posible: **hoy no hay ninguno en el catálogo** —comprobado sobre las 163
fichas—, así que su ausencia no daba error, no daba aviso y no cambiaba ningún
menú. Es el patrón del óxido de cobre otra vez: una regla que hoy no muerde y
que el día que muerda ya no habrá nadie mirando.

**Aplicado:** `TOXICOS_FEDIAF_7_7` en `seguridad.py`, filtrado en el solver
junto a la borraja y el tejido tiroideo, con aviso propio, y **BLOQUE 82** que
comprueba las tres puertas. Sin tope numérico a propósito: la propia fuente dice
que la gravedad no depende de la dosis y que dosis pequeñas repetidas intoxican
igual. Poner un número aquí sería inventarse una seguridad que la fuente niega.

### F-16 · El puente de 4 kcal/g de materia seca es una asunción, y FEDIAF manda corregirla

Dos frases de §3.2.1, y las dos tocan a **todo** el repo:

> *«These conversions assume an energy density of 16,7 kJ (4,0 kcal) ME/g DM.
> **For foods with energy densities different from this value, the
> recommendations should be corrected for energy density.**»*

> *«Legal maxima in EU legislation are expressed on 12 % moisture content and
> **they do not account for energy density**. Therefore in these guidelines they
> are only provided on a dry matter basis.»*

El ×2,5 con el que pasamos **cada** cifra de %MS a por-1000-kcal —las 92 de
patología, las 12 del libro, las de SACN5— sale de asumir 4,0 kcal/g MS. La
fuente dice que hay que corregirlo si la densidad es otra, y una ración cruda,
sin hidratos y con más grasa, no tiene por qué estar en 4,0.

**Y hay una prueba de que FEDIAF sí corrige:** el techo de lisina del cachorro
se convierte con **4156 kcal/kg**, la densidad del estudio del que sale, no con
4000 (ver F-17).

⚠️ **Lo que hace esto especialmente incómodo: no se puede ni medir.** Para saber
la densidad energética en materia seca hace falta la **humedad de cada ficha**, y
no está en ninguna (`CERRADO.md`, sección ABIERTO). Así que este hallazgo no
cambia un número: sube de prioridad el dato que falta, y ahora se sabe
exactamente para qué hace falta.

Para el techo **legal** el efecto tiene signo conocido: si un menú tiene más de
4,0 kcal/g MS, puede llevar más de lo que la ley permite **por kg de alimento**
y aun así pasar nuestro control por 1000 kcal.

### F-17 · El techo de lisina: contesta la pregunta P-04

`PREGUNTAS_ABIERTAS.md` P-04 preguntaba **sobre qué proteína se mide** el techo
de lisina. La respuesta estaba en §3.3.1 y no se mide sobre proteína:

> *«Czarnecki et al. (1985) showed that excess dietary lysine (**4,91 % DM**
> [basal diet 0,91 % + **4 % from a supplement**]) decreases weight gain in
> puppies but not 2,91 % DM… the highest no-effect-level of lysine for puppies
> was **2,91 % DM** (energy density **4156 kcal/kg**). This is equivalent to
> **7,0 g/1000 kcal** or 2,8 % DM (at 4 kcal/g DM) and this is therefore the
> FEDIAF maximum for puppy growth.»*

Es **lisina total de la dieta**, y el daño se vio **añadiendo lisina libre** a
una dieta basal, no comiendo más proteína. Eso importa para nuestra excepción:
el motor no aplica ese techo porque **0 de 12 menús de cachorro caben debajo**
(van de 8,24 a 11,48), y ahora se sabe que esos 8-11 g vienen de la proteína de
la carne, no de un suplemento de lisina cristalina, que es lo que el estudio
midió. **No cambia la decisión, pero la deja mucho mejor sostenida.**

### F-18 · El gran danés tiene su propio techo de calcio

> *«During later growth **up to 1,8 % DM can be fed to all breed dogs including
> giant breeds with the exception of great Danes**. This breed may be more
> susceptible and it is preferable to continue with a food containing a maximum
> calcium content of **1,6 %**.»*

1,6 % MS son 4000 mg/1000 kcal, contra los 4500 que el motor aplica en
crecimiento. **Medido: hoy no cambia ningún menú**, porque el techo del libro
para el cachorro de más de 25 kg de adulto (2750 mg, SACN5 Tabla 17-1 +
Fascetti cap.10) ya es bastante más estricto que 4000, y un gran danés siempre
pasa de 25 kg. Queda escrito porque **está cubierto por accidente**: si algún
día ese techo del libro se moviera, el del gran danés no lo sostendría nadie.

### F-19 · La vitamina D tiene tres máximos según el tamaño de la raza

> *«Studies in Great Dane puppies showed that a dietary vitamin D level of **435
> IU/100 g DM** can affect Ca absorption and may stimulate endochondral
> ossification disturbances. Therefore, **320 IU per 100 g DM** should be the
> nutritional maximum for growing **giant breed** dogs. Based on differences in
> cholecalciferol metabolism between giant breed and small breed puppies, **425
> IU/100 g DM** can be considered a safe nutritional maximum for **small breed**
> puppies. Since there is no information on maximum safe intakes for adult dogs
> and breeding bitches, FEDIAF recommends the **same nutritional maximum for
> other life stages** as those indicated for puppies.»*

Convertido: **20 µg/1000 kcal** en raza gigante y **26,6** en raza pequeña, y
valen también para el adulto. El motor aplica **14,1875** a todos, que es el
máximo **legal**. Y §3.1.3 dice que el legal **solo aplica si el nutriente se
añade como aditivo**: en un menú cuya vitamina D venga solo de hígado, pescado o
aceite de hígado de bacalao —materias primas— el que mandaría es el nutricional.

**Medido sobre los 216 menús del catálogo:** la vitamina D va de 3,17 a 14,19
µg/1000 kcal, mediana 5,71. Solo tres pasan de 13, y **el único que toca el techo
(14,19) lleva un multivitamínico**, que es un aditivo, así que ahí el legal
manda y nuestro número es el correcto.

**No se aplica, y el motivo se escribe:** relajar hasta 26,6 cruzaría nuestro
propio tope de seguridad crónica (20 µg), casi todos los menús llevan
multivitamínico, y ningún menú se está quedando fuera por esto. Ser más estricto
aquí no cuesta nada medible.

### F-20 · Por qué FEDIAF descarta un techo de yodo más bajo

> *«From studies by Castillo et al. (2001a,b) low nutritional maximum for iodine
> in dogs (**0,4 mg/100 g DM**) was recommended. However in these studies puppies
> were significantly **overfed (approx. 75 % above energy requirement)**… the food
> was deficient in a number of key nutrients… Consequently, these results are
> **irrelevant** for normal commercial nutritionally balanced foods, and the
> existing legal maximum is safe for all dogs.»*

0,4 mg/100 g MS son 1000 µg/1000 kcal — **más estricto que nuestro tope crónico
de 1275**. FEDIAF lo descarta con un motivo concreto y comprobable. Es material
directo para la pregunta abierta del yodo: no hay que subir el nuestro, pero sí
hay que saber que la fuente más estricta que existe está desacreditada por la
propia FEDIAF.

### F-21 · Tercera fuente independiente para el ratio omega-6:omega-3

> *«The effects of omega-3 fatty acids depend on the level **as well as on the
> ratio of omega-6 to omega-3 fatty acids**. Very high levels of long chain
> omega-3 fatty acids can decrease cellular immunity, particularly in the
> presence of a low level of omega-6 fatty acids.»*

Cris Carles lo señaló, el NRC 2006 lo menciona (y prefiere el
linoleico:linolénico, que sí aplicamos), y **FEDIAF también lo dice**. Ninguna de
las tres da una cifra para el perro sano. Lo que cambia es el peso de la
pregunta: ya no es «una fuente lo pide», son tres.

### F-22 · La ecuación de energía se queda corta con mucha fibra

> *«In dog foods with **crude fibre content above 8 % in DM** and a high
> percentage of fermentable NSP in the crude fibre fraction the predictive
> equation **can underestimate the energy density**.»*

Toca al **BLOQUE 71**, que compara las kcal de cada ficha del catálogo contra
esa misma ecuación. Un alimento muy fibroso puede salir «alejado de la ecuación»
sin que su dato esté mal. Hoy el bloque no distingue ese caso — y, como F-16, no
se puede comprobar sin la humedad.

### F-23 · La columna de MÁXIMOS no la comprobaba nadie, y ya se rompió una vez

**Pregunta de Elena, 10 de septiembre:** *«aunque el legal sea más bajo debes
dejar anotado el límite nutricional también porque lo legal podría cambiar»*.

Tiene razón, y al ir a hacerlo aparecieron dos cosas peores que la que motivó la
pregunta.

**Primera: hay una razón más fuerte que «la ley podría cambiar».** Es §3.1.3, y
ya estaba escrita en el repo sin que nadie hubiera sacado esta consecuencia:

> *«A legal maximum only applies when the particular trace element or vitamin is
> **added to the recipe as an additive**. If the nutrient comes exclusively from
> feed materials, **the legal maximum does not apply, instead the nutritional
> maximum applies**.»*

O sea que en una ración cruda cuyo cobre, zinc, hierro o vitamina D vengan solo
de la carne y las vísceras, **el techo que gobierna es el nutricional** — y ese
número no estaba en ninguna parte que se pudiera leer.

**Segunda: los maxima no se auditaban.** `auditar_transcripcion_fediaf.py`
rehacía las **cuatro columnas de mínimo** de la Tabla III-3b y **no miraba la de
máximo**. Y en la III-3b los máximos legales **no llevan número**: solo pone
«(L)», porque la §3.2.1 dice que no dependen de la densidad energética y por eso
se dan solo en base materia seca. Así que los siete techos legales que aplica el
motor —cobre 7, yodo 2750, hierro 170,45, manganeso 42,5, selenio 142, zinc
56,75 y vitamina D 14,1875— son **conversiones nuestras de la Tabla III-3a**, y
no había nada que las comparara con el PDF.

⚠️ **Y no es hipotético: ya se rompió.** La nota del sello del 8 de septiembre lo
cuenta con todas las letras — el maximo de fósforo del adulto se quitó el día 7
porque *«en el texto extraído del PDF la columna de máximos cae visualmente sobre
la fila ANTERIOR: leyendo línea a línea, el calcio parece tener cuatro máximos y
el fósforo ninguno»*. Durante un día **el motor no tuvo techo de fósforo en
adulto** y el catálogo llegó a tener un menú con 4124 mg. Era ya el fallo de las
dos columnas pegadas (F-16), visto en una celda y sin encontrarle la causa.

**Lo aplicado:**

- `fediaf_tabla_III_3a.txt`, la página 15 del PDF tal cual.
- Las **13 filas con máximo** llevan ahora `maximo_origen` — legal o nutricional
  — y la cita de cómo sale en la tabla.
- La **vitamina D lleva los dos números**: 14,1875 µg (legal, 227,00 (L)) y
  **20,0 µg (nutricional, 320,00 (N))**. Es el único nutriente del perfil canino
  con los dos publicados y con el legal por debajo.
- `auditar_transcripcion_fediaf.py` **rehace los 18 máximos** desde el texto del
  PDF, con su etiqueta y su conversión — y el factor no es siempre ×2,5: el
  calcio y el fósforo van en g en la tabla y en mg en el motor, el yodo en mg y
  en µg, y las vitaminas A y D en UI. Probado con el fallo puesto seis veces,
  incluida la del 7 de septiembre.

**Y una coincidencia que da confianza:** esos 20,0 µg del máximo nutricional son
exactamente el máximo que FEDIAF da al cachorro de **raza gigante** (320 IU/100 g
MS, §3.3.1, por los estudios en gran danés de Tryfonidou 2002) **y** el tope de
seguridad crónica que el motor ya aplicaba desde NRC 2006. Tres caminos
independientes al mismo número.

### F-24 · Cómo se gestiona el techo legal y el nutricional, medido

**Pregunta de Elena:** *«¿cómo vas a gestionar lo del límite legal y el
nutricional?»*. La respuesta necesitaba una medida antes que una opinión.

**Hay tres procedencias, no dos, y no son lo mismo:**

| | Qué es | Quién lo mueve |
|---|---|---|
| **(L) legal** | Reglamento (UE) 2017/1492 | Nadie… **pero solo aplica si el nutriente se añade como aditivo** (§3.1.3) |
| **(N) nutricional** | Criterio de FEDIAF | Admite lectura profesional |
| **Nota c** (sodio y cloruro) | «El nivel más alto con datos» | No dice que por encima haga daño: dice que **nadie lo ha mirado** |

Esa tercera es fácil de citar mal. Literal: *«Scientific data show that sodium
levels up to 1,5 % DM… are safe for healthy dogs. **Higher levels may still be
safe, but no scientific data are available**»*.

⚠️ **Y aquí la primera versión de este apartado contaba mal, lo cazó Elena.**
Se midió «viene de una ficha de categoría suplemento» y se llamó «va añadido como
aditivo», y **no es lo mismo**. De las 22 fichas que se contaron, **solo 11 son
aditivos**: los diez multivitamínicos y el yoduro potásico en comprimidos. El
alga, la cáscara de huevo, la levadura de cerveza, el aceite de salmón y el polvo
de sangre son **materias primas**, y su mineral es natural, no añadido.

Rehecha la medida con la clasificación buena, **el número apenas cambia** —el
yodo pasa de 91,3 % a 90,8 %— porque el multivitamínico domina el aporte de los
ocho. Pero eso es suerte de qué alimento pesa más, no que la cuenta estuviera
bien.

**La medida que decide la gestión.** Sobre los 216 menús del catálogo, qué parte
de cada nutriente con techo va **añadida como aditivo** (multivitamínico o
yoduro potásico):

| Nutriente | Mediana | Máximo | Menús sin nada añadido |
|---|---|---|---|
| Yodo | 91,3 % | 97,8 % | 0 de 216 |
| Vitamina D | 70,5 % | 100 % | 0 de 216 |
| Zinc | 60,0 % | 82,4 % | 0 de 216 |
| Manganeso | 56,1 % | 93,8 % | 0 de 216 |
| Hierro | 48,2 % | 78,9 % | 0 de 216 |
| Cobre | 40,3 % | 84,4 % | 0 de 216 |
| Vitamina A | 21,8 % | 61,1 % | 0 de 216 |
| Selenio | 13,5 % | 49,9 % | **1** de 216 |

**En 215 de 216 menús los ocho nutrientes llevan parte añadida.** O sea que el
techo legal es **el que corresponde por la §3.1.3** en casi todos los casos, no
una precaución nuestra.

**Cómo se gestiona, entonces:**

1. **El motor sigue aplicando el más bajo, siempre.** Con un motivo medido: en
   215 de 216 el legal es el que toca, y aplicarlo también al que falta es más
   estricto que la norma, nunca menos.
2. **Los dos números se guardan y se sirven**, con su etiqueta, en
   `/formular/estado` → `techos_de_fediaf`. Quien firma ve el número aplicado,
   de dónde sale, y el otro si existe. BLOQUE 83.
3. **Cada fila con máximo dice su procedencia**, y el auditor falla si alguna se
   queda sin ella. Cazó una nada más escribirlo:
   `Calcio_LateGrowth_RazaGrande` no la tenía.
4. **Lo que NO se hace solo, y por qué.** Aplicar la §3.1.3 al pie de la letra
   —el nutricional cuando el nutriente no va añadido— necesitaría un campo por
   ficha que diga **qué nutrientes aporta como aditivo declarado**. Eso es dato,
   no código. Y para los seis oligoelementos sería además peligroso: FEDIAF **no
   publica (N)** para ellos, así que relajar el legal los dejaría **sin ningún
   techo**.

### F-25 · Y el caso «sin multivitamínico» existe, y se pega al techo

La pregunta de Elena tenía una segunda mitad que la primera respuesta no tocaba:
si el legal solo aplica a lo añadido, **¿qué pasa en un menú que no lleve
multivitamínico?**

**Medido: el motor sí saca menú verde sin multivitamínico.** No es hipotético.
Y en tres de esos menús (5, 12 y 35 kg), qué parte del techo legal alcanzan:

| Nutriente | % del techo legal | Techo |
|---|---|---|
| **Selenio** | **97,1 %** | 142 µg |
| Vitamina D | 74,6 % | 14,19 µg |
| Cobre | 55,9 % | 7 mg |
| Yodo | 43,7 % | 2750 µg |
| Zinc | 36,1 % | 56,75 mg |
| Hierro | 12,8 % | 170,45 mg |
| Vitamina A | 7,3 % | 30 000 µg |
| Manganeso | 4,0 % | 42,5 mg |

En ese menú el aporte de los ocho viene **exclusivamente de materias primas**, así
que la lectura literal de §3.1.3 diría que el techo legal **no aplica**. Y para
seis de los ocho FEDIAF **no publica nutricional**: se quedarían **sin ningún
techo de FEDIAF**. Lo único que quedaría debajo son los topes de seguridad
crónica, y son **más laxos**: el del selenio son 570 µg (AAFCO) contra los 142 de
FEDIAF, **cuatro veces más** — y el menú ya está en el 97 % de 142.

**Eso cierra la decisión, y ahora con un argumento y no con una precaución:**
aplicar siempre el legal no es solo lo estricto, es **lo único que deja un techo
justo donde el menú se pega a él**. Las seis filas afectadas llevan ahora escrito
`sin_maximo_nutricional_publicado` con esta medida dentro, y el auditor falla si
una fila con techo legal no dice qué quedaría sin él.


### F-26 · La comprobación de F-24 y F-25 contra el PDF, porque Elena no se fiaba

*«Pero compruébalo bien, yo lo he dicho, pero no estoy segura, tienes que
comprobar bien.»* Bien hecho: al ir al PDF aparecieron **dos frases que no
tenía** y **una tensión dentro del propio documento**.

**1 · §3.1.3 dice dos cosas más de las que yo había citado.**

> *«A legal maximum only applies when the particular trace element or vitamin is
> added to the recipe as an additive, **but relates to the 'total' amount present
> in the finished product (amount coming from the additive plus amount from feed
> materials (ingredients))**.»*

Cuando el techo legal aplica, aplica al **total**, no solo a la parte añadida.
**Es lo que hace el motor**: mide el nutriente entero del menú. No lo había
verificado y resulta que está bien.

> *«…instead the nutritional maximum, **when included in the relevant tables**,
> should be taken into account.»*

FEDIAF admite en su propia frase que el nutricional **puede no estar en las
tablas**. Es exactamente el caso de los seis oligoelementos.

**2 · Y el registro de cambios de 2012 lo zanja, con un principio escrito.**

> *«**As a general principle it was agreed that no nutritional maximum level will
> be stated in the Guidelines for nutrients for which no data on potential
> adverse effects are available.**»*

O sea que la ausencia de (N) para cobre, yodo, hierro, manganeso, selenio y zinc
**no es un hueco de la tabla ni un fallo de transcripción**: es una decisión
declarada, y su motivo es que **no hay datos de efectos adversos**. Eso confirma
F-25 con la fuente en la mano: quitar el techo legal a esos seis no los deja con
un techo más alto, los deja **sin ninguno, y precisamente porque nadie sabe
dónde está el daño**.

**3 · ⚠️ Y hay una tensión dentro del propio documento, que conviene tener
escrita.**

> **⚠️ ESTO ESTABA MAL, y lo corrige F-27 unas líneas más abajo (mismo día, por
> la tarde). No hay ninguna tensión: las dos frases están en el MISMO PÁRRAFO de
> §3.1.3, una detrás de otra. Se escribió así por citar un trozo en vez de leer
> la sección entera. Se deja escrito, no borrado, porque una equivocación
> borrada se vuelve a cometer.**

§3.2.1, leyendo las tablas:

> *«The legal maximum (L) is **mandatory and always applies to all life
> stages**.»*

Y §3.1.3, en la sección que trata específicamente de los máximos:

> *«A legal maximum **only applies when** the particular trace element or vitamin
> is added to the recipe as an additive… If the nutrient comes exclusively from
> feed materials, the legal maximum **does not apply**.»*

La lectura que las reconcilia es que el «always applies to **all life stages**»
de §3.2.1 habla de **etapas vitales** —no varía entre cachorro y adulto—, no de
la procedencia del nutriente. Es la más razonable, y además §3.1.3 es la sección
específica y la detallada.

**Pero no hace falta elegir**, y eso es lo tranquilizador: **aplicar siempre el
legal satisface las dos lecturas a la vez**. Una dice que es obligatorio siempre;
la otra lo condiciona. Cumplir la más estricta cumple las dos.

**4 · Y una tercera confirmación de paso.** El changelog dice también
*«Nutritional maximum for sodium has been deleted and replaced by a footnote»*.
Es la nota c, y confirma que el máximo de sodio y cloruro **no es un (N)**: es
«el nivel más alto con datos», que es como está etiquetado en el JSON desde hoy.


### F-27 · La «tensión» de F-26 no existía, y al ir a mirarlo salió algo peor

Leyendo §3.1.3 **entera y al pie de la letra**, no en la frase que tenía citada.

**1 · Primero, una corrección de lo que escribí esta mañana.** El punto 3 de F-26
decía que había una tensión entre §3.2.1 («the legal maximum is mandatory and
always applies to all life stages») y §3.1.3 («a legal maximum only applies when…
added as an additive»), y proponía una lectura que las reconciliara.

No hay tensión y no hace falta reconciliar nada: **las dos frases están en el
mismo párrafo de §3.1.3**, una detrás de otra. «All life stages» habla de etapas
vitales, no de procedencia. Leer la sección entera lo resuelve solo. Lo que
fallaba era, otra vez, haber citado un trozo en vez de leer el sitio.

**2 · Y en §3.2.1 hay una frase que sí cambia algo, y es de las gordas.**

> *«Legal maxima in EU legislation are expressed on 12% moisture content and
> **they do not account for energy density**. Therefore in these guidelines they
> are **only provided on a dry matter basis**.»*

> *«These conversions assume an energy density of 16.7 kJ (4.0 kcal) ME/g DM.
> **For foods with energy densities different from this value, the
> recommendations should be corrected for energy density.**»*

FEDIAF publica los máximos legales **solo en materia seca, a propósito**, porque
la ley no habla de calorías. El motor los aplica **por 1000 kcal**, convertidos
con el ×2,5 de la Tabla III-2 — que es exactamente la conversión que la segunda
frase condiciona a una densidad de **4,0 kcal ME/g de materia seca**. Y pide
corregirla cuando la densidad es otra.

Una ración BARF de este motor no tiene por qué estar en 4,0: lleva del 20 al 60 %
de hueso, que es casi todo mineral y aporta materia seca con muy pocas calorías,
y por el otro lado grasa, que aporta calorías con poca materia seca. Los dos
efectos van **en direcciones opuestas**, así que ni siquiera se puede decir de
antemano hacia dónde falla.

**Lo que está en juego, medido en sensibilidad** (selenio, cuyo techo legal es
56,80 µg/100 g MS):

| Densidad real (kcal ME/g MS) | Factor 10/E | Techo legal por 1000 kcal |
|---|---|---|
| 3,5 | ×2,86 | 162,3 |
| 3,8 | ×2,63 | 149,5 |
| **4,0** (el que suponemos) | **×2,50** | **142,0** |
| 4,5 | ×2,22 | 126,2 |
| 5,0 | ×2,00 | 113,6 |
| 5,5 | ×1,82 | 103,3 |

O sea que el techo que aplicamos puede estar **un 14 % por debajo** del que toca
o un **25 % por encima**. Y no es un nutriente: son **los siete** con máximo
legal — cobre, yodo, hierro, manganeso, selenio, zinc y vitamina D —, que
además son justo los seis que **no tienen máximo nutricional ninguno** (F-25), o
sea aquellos para los que este es el único techo que existe.

**3 · Y por qué no se puede cerrar hoy.** Para saber la densidad real de un menú
hace falta su materia seca, y **el catálogo no tiene columna de humedad** — ni de
cenizas. Está en `DATOS_QUE_FALTAN.md` desde antes, como un hueco de ficha; hoy
deja de ser eso: **es el dato que decide siete techos de seguridad**. No lo
rellena el asistente.

Mientras tanto no se toca ninguna cifra. Bajar el techo «por si acaso» sería
inventarse la densidad igual que suponerla 4,0, solo que en la otra dirección, y
el ×2,5 al menos es el factor que publica la propia FEDIAF.


### F-28 · La nota d: un segundo techo de selenio, 2,5 veces más estricto, y un veredicto que estaba mal

Leyendo §3.2.3 **al pie de la letra**, que es la sección de las tablas felinas —
y donde, al final, están impresas **las notas a-h, que son comunes a las seis
tablas**.

**1 · Primero, un veredicto mío que era falso — y al buscar sus hermanos salieron
diez más.** La cifra `22,73 µg` estaba clasificada como *«celda de la tabla
FELINA, el motor solo formula para perro»*. No lo es: es la **nota d**, y marca
la fila de **selenio del PERRO** en la Tabla III-3a, que se lee `56.80 (L)d`.
Las notas están impresas debajo de la última tabla felina y por eso se leyeron
como felinas. Seis de las ocho —a, b, c, d, g, h— marcan filas del perro.

Y no era un despiste suelto. Al poner una regla que **exige demostrar** el
descarte por felino, saltaron **once elementos** con la misma etiqueta falsa,
todos dentro del bloque de notas:

| Línea | Qué es de verdad |
|---|---|
| 2931-2932 | **Nota b**: el calcio al que se puede bajar pasados los ~6 meses (0,8 % MS · 2 g/1000 kcal · 0,48 g/MJ) |
| 2934, 2936-2937 | **Nota c**: el cloruro seguro del perro (2,35 % MS · **5,87 g/1000 kcal** · 1,40 g/MJ) — y **5,87 es el número que aplica el motor** |
| 2940-2941 | **Nota d**: el selenio orgánico (22,73 µg/100 g MS · 0,20 mg/kg · la humedad del 12 %) |

O sea que estaban etiquetadas como «no nos aplica» **tres cifras que el motor sí
aplica** y la humedad de referencia del 12 %, que es la misma base de F-27.

**2 · Y lo que dice la nota d es un techo que no aplicamos.**

> *«For organic selenium a maximum supplementation level of **22.73 µg organic
> Se/100 g DM** (0.20 mg organic Se/kg complete feed with a moisture content of
> 12 %) applies.»*

Es un techo **de otra naturaleza** que el de la fila:

| | Qué limita | Cuánto | Por 1000 kcal (×2,5) |
|---|---|---|---|
| Fila III-3a | el **total** de selenio | 56,80 µg/100 g MS | 142,0 |
| **Nota d** | **solo lo suplementado**, y solo en forma **orgánica** | 22,73 µg/100 g MS | **56,8** |

O sea: **el 40 %**. Y la cuenta de la propia nota cuadra — 0,20 mg/kg de pienso
al 12 % de humedad son 0,227 mg/kg de materia seca, que son sus 22,7 µg/100 g.

**3 · Y no es teórico. Medido hoy** sobre menús reales, contando solo lo que
aportan los alimentos de categoría suplemento:

| Perro | Selenio total | **De suplemento** | ¿Cabe en la nota d? |
|---|---|---|---|
| CachorroJoven 6 kg | 139,2 | **63,0** | **NO** (tope 56,8) |
| CachorroJoven 1,5 kg | 142,0 | 39,0 | sí |
| CachorroCrecimiento 12 kg | 140,5 | 26,1 | sí |
| Adulto 22 kg | 139,0 | 9,1 | sí |
| Lactante 15 kg | 141,0 | 22,1 | sí |

El cachorro de 6 kg **se pasa** — en uno de los menús que devolvió el solver, no
en todos, porque el menú cambia entre ejecuciones. Los adultos van holgados: su
selenio viene sobre todo de las vísceras y el pescado, no del bote.

**4 · Por qué no se puede aplicar hoy.** La nota d solo rige si el selenio es
**orgánico** (levadura de selenio, selenometionina) y no si es selenito o
selenato sódico. **Ninguna ficha del catálogo dice en qué forma química viene su
selenio.** Es exactamente el mismo hueco que el de las vitaminas del grupo B, y
aplicar el techo a ciegas sería inventarse el dato — igual que ignorarlo.

Queda en `DATOS_QUE_FALTAN.md`. **No lo rellena el asistente.**


### F-29 · Las kcal de cada ficha no se pueden comprobar contra la ecuación de FEDIAF

Leyendo el **Anexo 7.2** al pie de la letra. FEDIAF publica la ecuación con la
que se calcula la energía metabolizable de un alimento, en cuatro pasos
(NRC 2006a, y es la base de la norma europea EN 16967):

```
1.  GE (kcal) = 5,7 × %proteína bruta + 9,4 × %grasa bruta + 4,1 × (%NFE + %fibra bruta)
2.  digestibilidad energética (perro) = 91,2 − 1,43 × %fibra bruta en MS
3.  DE = GE × digestibilidad / 100
4.  ME (perro) = DE − 1,04 × %proteína bruta
```

Y dice cuál es mejor: *«The equations cited by NRC provide a more accurate
estimate of ME compared to the modified Atwater method in dry pet foods; the
modified Atwater method and the NRC equations provide an equally moderate
accuracy … for wet foods»*.

**El problema es que no la podemos aplicar.** El paso 1 necesita el **NFE**
(extracto libre de nitrógeno), que se obtiene por diferencia:

```
NFE = 100 − agua − proteína − grasa − cenizas − fibra
```

O sea que hace falta **humedad y cenizas**, y el catálogo no tiene ninguna de
las dos. Es el mismo dato que falta en **F-27**, y ésta es su tercera
consecuencia — y la más grave de las tres:

| Consecuencia | Qué decide |
|---|---|
| F-27 | los siete techos **legales**, convertidos con una densidad supuesta |
| F-27 | el techo de calcio y fósforo del cachorro, por la misma conversión |
| **F-29** | **las kcal de cada ficha**, que son el **denominador de los 43 requisitos** |

Si las kcal de una ficha están mal, **todo el menú está mal y el semáforo sale
verde igual**, porque el semáforo mide contra las kcal que le dan.

**Y hay un motivo concreto para sospechar.** SACN5 avisa de que el método de
Atwater modificado *«overestimates the ME content of foods high in fiber or
ash»*. Una ración BARF lleva entre un 20 y un 60 % de **hueso carnoso**, que es
ceniza. Si el campo `energia` de las fichas con hueso sale de Atwater, está
**sobreestimado** — y sobreestimar las kcal significa dar **menos comida** de la
que el perro necesita, y repartir los nutrientes sobre un denominador inflado.

Hoy no se puede ni confirmar ni descartar: **está sin comprobar de dónde viene
el campo `energia` de cada ficha**. Queda en `DATOS_QUE_FALTAN.md` junto a la
humedad, que es lo que desbloquea las dos cosas.


### F-30 · FEDIAF nombra una raza con menos taurina, la app conoce esa raza, y no pasa nada

**Anexo 7.3.3, «Dog»**, leído entero:

> *«In dogs, low plasma levels of taurine (< 40 µmol/L) may also predispose to
> dilated cardiomyopathy. However, **some breeds seem to be more sensitive** to
> develop such side effects, **particularly Newfoundland dogs, in which the rate
> of taurine synthesis is decreased** (Backus RC et al. 2006).»*

Y en la misma página, el otro factor de riesgo:

> *«**Feeding certain lamb and rice foods may increase the risk of a low-taurine
> status**, because of lower bioavailability of sulphur-containing amino acids
> and increased faecal losses of taurine possibly caused by rice bran.»*

**Lo que hace hoy el motor.** Conoce al Terranova: tiene su fila de energía de la
Tabla VII-7 (105 kcal/kg^0,75, rango 80-132) y la app lo ofrece en su lista de
razas. De la taurina, nada — ni un aviso.

Y las dos condiciones se juntan solas: una ración BARF de cordero para un
Terranova es exactamente el perfil que describe FEDIAF, y sale **verde**, porque
la taurina no es esencial para el perro y no está entre los 43 requisitos.

**Lo que se puede hacer y lo que no.** FEDIAF **no da una cifra**: dice que el
alimento debe formularse para mantener reservas adecuadas (>40 µmol/L en plasma,
>200 µmol/L en sangre entera), que es un objetivo de analítica, no de receta. Así
que subir la metionina «un poco» sería inventarse el número — lo mismo que pasa
con el *«in the case of lamb and rice foods, the methionine level may have to be
increased»* de §3.3.1, que es este mismo asunto visto desde el otro lado.

Lo que sí se puede es **decirlo**: el motor ya tiene la patología
`dcm_taurina_respondedora`, y este es el aviso que le falta a la raza. Queda
apuntado como decisión de producto, no como cifra.
