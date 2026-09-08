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
