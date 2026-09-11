# Hallazgos de Fascetti & Delaney, «Applied Veterinary Clinical Nutrition», 2ª ed.

Lo que sale de leer el libro entero, capítulo a capítulo, con el contador de
`leer_fascetti.py` delante. El registro de qué capítulo está leído y con qué
veredicto vive en `lecturas_fascetti.json`; aquí solo va **lo que dice algo del
motor**, con su medida.

La regla de siempre: **si una fuente contradice a FEDIAF, gana FEDIAF**. Casi
nada de lo de aquí contradice: aprieta dentro de la ventana, o llena un hueco
donde FEDIAF no pone cifra.

---

## F-1. La Tabla 2.1: el omega-3 terapéutico, dosificado por peso metabólico

**Dónde.** Cap.2 «Basic Nutrition Overview», Tabla 2.1, «Daily long-chain
omega-3 fatty acid doses (in mg of combined EPA plus DHA) calculated on a
metabolic body weight basis for adult dogs», adaptada de Bauer (2011).

| Trastorno | Dosis |
|---|---|
| Hiperlipidemia idiopática | 120 mg/kg^0,75 |
| Enfermedad renal | 140 mg/kg^0,75 |
| Trastornos cardiovasculares | 115 mg/kg^0,75 |
| **Artrosis** | **310 mg/kg^0,75** |
| Inflamatorio/inmune (atopia, EII) | 125 mg/kg^0,75 |
| NRC *recommended allowance* | 30 mg/kg^0,75 |
| **NRC *safe upper limit*** | **370 mg/kg^0,75** |

**Por qué importa, y son tres cosas distintas.**

**1. Es una segunda fuente independiente de lo que el motor ya aplica.** Hoy los
suelos de omega-3 salen de SACN5 y van en **g por 1000 kcal**; esta tabla va en
**mg por kg^0,75 y día**. Convertidas a nuestra base —y la conversión **no
depende del peso**, solo del nivel de energía, porque los dos usan el mismo
exponente:

| | a 95 kcal/kg^0,75 | a 110 | a 130 |
|---|---|---|---|
| Renal | 1,47 | **1,27** | 1,08 |
| Artrosis | 3,26 | **2,82** | 2,38 |
| Inflamatorio/atopia | 1,32 | **1,14** | 0,96 |
| Cardiovascular | 1,21 | **1,05** | 0,88 |
| NRC safe upper limit | 3,89 | **3,36** | 2,85 |

*(g de EPA+DHA por 1000 kcal)*

**2. Y en dos patologías pide MÁS que lo que aplicamos.** Nuestro suelo de renal
es **1,0 g/1000 kcal de omega-3 TOTAL** y esta tabla pide **1,27 de EPA+DHA**,
que es un subconjunto: o sea estrictamente más. Igual en dermatitis atópica,
**0,875 total** contra **1,14 de EPA+DHA**. No es un conflicto con FEDIAF
—FEDIAF no pone requisito de omega-3 al adulto—, así que cabría apretarlo. **Es
decisión clínica y va al nutricionista.**

**3. Trae un TECHO que el motor no tiene por ninguna parte.** El *safe upper
limit* del NRC, **370 mg/kg^0,75 = 3,36 g EPA+DHA/1000 kcal** a 110. El libro
dice que sus dosis «are below the canine safe upper limit (NRC 2006a)». Hoy el
motor no tiene ningún máximo de omega-3, y tiene escritos sin aplicar un 8,75
para la artrosis y un 12,5 para el cáncer —los dos de SACN5 y los dos de
omega-3 **total**, no de EPA+DHA—, así que la comparación no es directa. Pero
la pregunta que abre sí lo es: **¿cuánto omega-3 es demasiado?** No está
contestada en ningún sitio del repo.

⚠️ **La trampa al leer esta tabla**: una dosis por kg^0,75 **no es una
concentración fija por 1000 kcal**. El mismo perro con más actividad come más
kcal y recibe la misma dosis, o sea **menos concentración**. Un perro de trabajo
a 130 kcal/kg^0,75 sale un 18 % por debajo del mismo perro a 110. Las dos bases
no son intercambiables y pasarlas de una a otra exige fijar el nivel de energía
y decirlo.

---

## F-2. El contador tiene un punto ciego, y está justo en los ratios

**Cómo salió.** Leyendo el cap.2 apareció esta frase:

> «For example, a ratio of LA : ALA of 3 : 1 to 5 : 1 will typically accomplish
> this goal (Dunbar et al. 2010).»

Es una **recomendación con cifra** sobre el ratio linoleico:linolénico, que es
justo uno de los límites que el motor aplica (2,6-26 en adulto, de NRC 2006), y
toca el ratio omega-6:omega-3 que la nutricionista señaló como ausente. **El
contador no la ve.** Comprobado frase a frase:

| Prueba del filtro | Resultado |
|---|---|
| ¿nombra un nutriente? | **no** — los nombra por abreviatura, `LA` y `ALA` |
| ¿tiene cifra con unidad? | **no** — «3 : 1» es una cifra **sin unidad** |
| ¿huele a recomendación? | no |

Y no es una frase suelta. Medido sobre el libro entero: **7 frases descartadas**
llevan un ratio y una abreviatura de ácido graso, y están repartidas por los
capítulos 2, 10 y 14.

**Lo que costaría cerrarlo, medido en los dos libros.** Contar un **ratio como
cifra** —que es lo coherente, porque el motor ya trata los ratios como una clase
de límite: el Ca:P, el linoleico:linolénico y el bloque `ratios` de
`patologias.json`—:

| | Hoy | Contando ratios | Y además las abreviaturas |
|---|---|---|---|
| Fascetti | 657 | **686** | 688 |
| SACN5 | 2.999 | **3.197** | 3.201 |

⚠️ **Y esto es lo incómodo, y hay que decirlo:** SACN5 figura hoy con **0
pendientes**. Eso es verdad **para el filtro tal como está escrito**, y deja de
serlo si el filtro cuenta los ratios: serían **198 frases nuevas sin veredicto**.
O sea que «SACN5 cerrado» significa hoy «cerrado bajo esta definición de elemento
nutricional», no «cerrado en absoluto».

**No se toca el filtro sin decidirlo**, porque es el mismo para los tres libros a
propósito —un filtro, una definición— y moverlo mueve los tres recuentos y pone
en rojo los BLOQUES 78 y 81 hasta que las 229 frases nuevas tengan veredicto. La
decisión es de Elena. **Lo que no se puede hacer es dejarlo sin escribir.**

---

## F-3. Lo que confirma, que también cuenta

- **La densidad de conversión.** «The nutrient profile on a dry matter basis
  presumes a specific energy density (i.e. 4000 kcal ME/kg food for AAFCO)»
  (cap.2). Es exactamente la densidad con la que `auditar_conversiones.py` rehace
  las 94 cifras de patología, las 14 del libro y las 4 condicionales.
- **La suma metionina+cistina.** «directly including cysteine in the diet
  decreases by up to 50% the amount of methionine needed» (cap.2). El motor trata
  `metionina_cistina` como una suma calculada, no como dos claves sueltas.
- **Los huecos de USDA.** «certain nutrients of interest such as taurine,
  chloride, iodine, and vitamin D are typically or often not available […] this
  can also be true of choline» (cap.2). Es palabra por palabra lo que dice
  `Bases.md` de por qué ninguna de las tres bases tiene los 41 nutrientes, y por
  qué casi todos los huecos del catálogo están donde ninguna llegaba.
- **La vitamina K con mucho pescado.** «The recommendations for vitamin K are
  higher if the product has a high fish content» (cap.2). Ya está escrita en
  `requisitos_condicionales.json` como `documentado_sin_cifra`, y Fascetti
  tampoco da número: confirma que dejarla inerte es lo correcto.
- **El ratio de omega-3 totales no sirve.** «a ratio calculated using all major
  types of omega-3 (i.e. ALA, EPA, and DHA) is not metabolically equivalent to
  one where only EPA and DHA is used» (cap.2). Es el fundamento de lo que NRC
  2006 dice más seco («is not helpful») y de por qué el motor aplica el
  linoleico:linolénico y **no** un omega-6:omega-3 total.


---

## F-4. El sodio del perro que trabaja choca con nuestro techo del perro sano

**Dónde.** Cap.4 «Nutritional and Energy Requirements for Performance», sección de
hidratación y electrolitos:

> «The adequate intake for both sodium and potassium recommended by the NRC for
> exercising dogs is 1 g/Mcal. One recent study suggested that 1.2 g of
> sodium/Mcal may be ideal in sled dogs undergoing a 1600 km race (Ermon et al.
> 2014).»

**Qué significa en nuestra unidad.** 1 g/Mcal son **1000 mg por 1000 kcal**. Y
ese número es, exactamente, el **techo de sodio que el motor aplica a cualquier
adulto sano** desde el 8 de septiembre, que sale de la Tabla 13-3 de SACN5 y vive
en `recomendaciones_libro.json`.

| | mg de sodio/1000 kcal |
|---|---|
| Techo del motor, perro adulto sano | **1000** |
| Ingesta adecuada del NRC, perro que hace ejercicio | **1000** |
| Sugerido para perro de trineo en 1600 km (Ermon 2014) | **1200** |
| Máximo de FEDIAF, adulto | 3750 |

**Por qué importa.** No hay conflicto con FEDIAF: los tres números caben de sobra
bajo su máximo. El conflicto es con **una recomendación nuestra**, y cae justo
sobre el perro que el motor **ya sabe distinguir** — el nivel de actividad viaja
suelto desde el 11 de septiembre y aprieta los topes crónicos por peso
metabólico, que es lo que vigila el BLOQUE 86.

Dicho de otra forma: un perro de trineo formulado con el techo del adulto sano
recibe **menos sodio del que su fuente considera ideal**, y la ingesta adecuada
del perro que hace ejercicio se queda **pegada al techo, sin un miligramo de
margen**.

⚠️ **Y el techo no es caprichoso**, que es lo que complica la decisión. Su
`por_que` dice de dónde sale y para qué: la Tabla 47-4 del mismo SACN5 lo repite
y añade el motivo — *«Phosphorus and sodium are considered key nutritional
factors for apparently healthy adult dogs and cats for purposes of ameliorating
or slowing the progression of subclinical kidney disease and/or hypertension»*.
O sea que es prevención renal y cardiovascular para el perro sin nada
diagnosticado. Levantarlo para el perro de trabajo no es aflojar un número
suelto: es decidir que en ese perro pesa más el electrolito que la prevención.

**Eso es criterio clínico y no lo decide el motor.** Queda escrito con las dos
cifras, que es la regla.

---

## F-5. Tres fuentes y tres curvas para la energía del cachorro

Cap.3: *«Predicted energy requirements are approximately 2.5 times maintenance
requirements at weaning»*. No es la curva de Klein que publica FEDIAF y que el
motor aplica, y tampoco es la Tabla 33-8 de SACN5, que ya está anotada como
hallazgo por ir hasta un **28 % por encima** de Klein.

Son **tres fuentes publicadas y tres curvas** para las kcal de un animal en
crecimiento, que es donde una cifra de más o de menos se paga en hueso. Manda
FEDIAF, y la discrepancia se apunta con sus números.

---

## F-6. Dos cifras de reproducción que la ficha no puede usar

Cap.3 da la subida de energía en **gestación** (*«energy requirements will
increase by 25% to over 60% depending on the size of the litter»*) y la ecuación
del NRC para la **lactancia**, que depende del **número de cachorros** y de la
semana.

Las dos dependen del tamaño de la camada, y **la ficha no pregunta cuántos
cachorros hay**. No es que el motor decida ignorarlo: es un dato que la app no
recoge, así que la cifra no tiene por dónde entrar. Va a la lista de preguntas
que faltan, con su fuente al lado para cuando se decida preguntarlo.
