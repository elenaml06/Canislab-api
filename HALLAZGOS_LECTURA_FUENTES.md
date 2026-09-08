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

**Es la más urgente de todo este documento.**

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
