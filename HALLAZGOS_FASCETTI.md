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
- **Los huecos de USDA.** «However, certain nutrients of interest such as
  taurine, chloride, iodine, and vitamin D are typically or often not available»
  (cap.2) — y el mismo párrafo añade que lo que parezca una carencia puede ser
  falta de dato, y que a la colina le pasa igual. Es palabra por palabra lo que dice
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

## F-6. Una cifra de reproducción que la ficha no puede usar (corregida el 11-sep por la tarde)

Cap.3 da la subida de energía en **gestación** y la ecuación del NRC para la
**lactancia**, que depende del **número de cachorros** y de la semana. La
lactancia es la que la ficha no puede alimentar: **no pregunta cuántos cachorros
hay**. No es que el motor decida ignorarlo — es un dato que la app no recoge, así
que la cifra no tiene por dónde entrar. Va a la lista de preguntas que faltan.

⚠️ **Y aquí había una cita mal copiada, que cazó `auditar_citas.py` el mismo día
al meter este fichero en su lista.** Decía *«depending on the size of the
litter»* y el libro dice:

> «At this time, and until parturition, energy requirements will increase by 25%
> to over 60% depending on the size of the **bitch** (the percentage increase in
> energy requirements during pregnancy tends to be greater for large-breed
> bitches).»

O sea **del tamaño de la PERRA, no de la camada** — y eso cambia la conclusión:
para la gestación el dato que hace falta es el peso, que la ficha sí pregunta.
Lo que sigue sin poder entrar es la ecuación de lactancia. Es exactamente el
fallo que este auditor existe para cazar, y estuvo escrito unas horas.

---

# Segunda tanda — capítulos 7 a 13 (11 de septiembre de 2026, tarde)

Los capítulos 7, 8 y 9 estaban **leídos en `LECTURA_FASCETTI.md` y sin un solo
veredicto en `lecturas_fascetti.json`**, que es exactamente el agujero que ese
fichero existe para cerrar: «leído» en un documento que nadie puede ejecutar.
Ahora están los tres, más el 10, 11, 12 y 13. Quedan del 14 al 21.

## F-7. ⚠️ El autor del capítulo del hueso pide MENOS calcio del que damos, y no se puede aplicar

El techo de calcio del cachorro de raza grande del motor —**2750 mg/1000 kcal**,
el 1,1 % de materia seca— sale de este mismo capítulo 10, escrito por Hazewinkel,
que es quien hizo los experimentos. Leído entero, el capítulo dice **dos cosas
más**, y las dos piden **menos**:

> «A large-breed food for growing dogs with a level of **0.8 % calcium** (per
> 4200 ME kcal/kg) has been both calculated and **proven to be safe** for raising
> large- and giant-breed pups throughout the growth period (Nap et al. 2000).»

> «In general, in foods with a protein content of **high biological value**, the
> calcium content should be **between 0.8 % and 1.0 %** on a dry matter basis
> (for a food with 4200 ME kcal/kg diet).»

Y la recomendación final del autor: **calcio ~1,0 % MS**.

| | % MS | Por 1000 kcal |
|---|---|---|
| Lo que aplica el motor (1,1 % a 4000 kcal/kg) | 1,1 | **2750** |
| Fascetti, extremo bajo (0,8 % a 4200 kcal/kg) | 0,8 | 1905 |
| Fascetti, extremo alto (1,0 % a 4200 kcal/kg) | 1,0 | 2381 |
| **Mínimo de FEDIAF, cachorro de raza grande** | | **2500** |

**El rango entero de Fascetti queda por debajo del mínimo de FEDIAF.** Aplicarlo
dejaría al cachorro corto de calcio, así que **gana FEDIAF** y la cifra se apunta
con sus dos números. Es uno de los pocos conflictos que sacan al perro **fuera**
de la ventana de FEDIAF, y por eso va a `FEDIAF_CONTRA_OTRAS_FUENTES.md`.

Ojo al matiz, que es el nuestro: *«a protein content of high biological value»*.
Una ración BARF lo es.

## F-8. ⚠️ Un techo de vitamina D en crecimiento que nadie tenía escrito

La recomendación final del mismo autor lleva **dos** cifras, y la segunda es
nueva:

> «Taken together, the author recommends the following: restricted feeding of a
> puppy food with a calcium and vitamin D content not to exceed the percentages
> demonstrated in controlled studies to result in skeletal problems (i.e. calcium
> ∼1.0% dm, **vitamin D content 12.5–25 μg/kg diet**), maintaining an optimal body
> condition during growth, and activity adapted to the vulnerability of the
> skeleton.»  *(Fascetti cap. 10)*

12,5–25 µg/kg MS = 500–1000 UI/kg = **3,125 a 6,25 µg/1000 kcal** a 4000 kcal/kg.
Hoy el motor solo tiene ahí el **máximo LEGAL de FEDIAF (14,19)** y el tope
crónico por peso metabólico. **Medido sobre los 12 menús de cachorro del
catálogo**:

| | µg/1000 kcal |
|---|---|
| El más bajo (Mini_CachorroCrecimiento) | 3,14 |
| Mediana | 6,07 |
| El más alto (Grande_CachorroCrecimiento) | **8,96** |
| **Se pasan de 6,25** | **6 de 12** |

**Cabe dentro de la ventana de FEDIAF**, así que se *podría* aplicar — y por eso
no se aplica en silencio. El mecanismo está en el mismo capítulo y es serio: los
perros criados con exceso de vitamina D desarrollaron osteocondrosis y radius
curvus **sin signos de intoxicación clásica** y sin que se moviera el calcio en
plasma. Pero el propio capítulo avisa de lo contrario:

> «A true safe upper limit for vitamin D intake, supported by clear scientific
> evidence for reproduction/growth and for adult maintenance, **is not currently
> known in dogs** (Wedner and Verbrugghe 2016).»  *(Fascetti cap. 10)*

O sea que lo que da no es un límite de seguridad demostrado: es la concentración
que recomienda para un pienso de cachorro. Es la diferencia entre las dos clases
de límite que el motor ya separa — `seguridad.py` frente a
`recomendaciones_libro.json` —, y por eso iría a la segunda. **Se pregunta.**

## F-9. ⚠️ El mismo «15 %» en dos unidades, y un factor de 2,2 entre las dos

El motor aplica a la linfangiectasia **grasa ≤ 37,5 g/1000 kcal**, leyendo la
Tabla 58-1 de SACN5: *«Fat <15 % for dogs and cats»*, en **materia seca**.
Fascetti cap. 11 dice el mismo 15 % **en kcal**:

> «Dietary fat restriction is particularly important in patients diagnosed with
> lymphangiectasia, with many patients needing restriction to **less than 15 %
> fat kJ or kcal**.»

15 % de las kcal = **16,7 g/1000 kcal**. Y el cap. 12 repite la jugada con el
umbral de «baja en grasa»: *«less than 20 % fat on an ME basis»* = 22,2.

**Medido el mismo día, preguntándole al solver con 40 s** (no a un endpoint con
presupuesto, que es la lección del BLOQUE 43):

| Tope de grasa | 10 kg | 20 kg | 35 kg |
|---|---|---|---|
| 37,5 g/1000 kcal (lo que aplica el motor) | sale | sale | sale |
| 20,0 | **no** | **no** | **no** |
| 16,7 (el 15 % de las kcal) | **no** | **no** | **no** |

### Por qué no entra, medido peldaño a peldaño (11 de septiembre, tarde)

Elena: *«mira a ver por qué no entra»*. La respuesta es que **no lo impide la
nutrición: lo impide la forma de una ración BARF**. Bisecando el techo de grasa
con el solver a 30 s, perro adulto de 20 kg y 1100 kcal:

| Dónde se pregunta | Grasa mínima alcanzable |
|---|---|
| Peldaño 0, estricto | **34,9** g/1000 kcal |
| Peldaño 1, sin mínimo de vísceras/hígado/verdura | 34,9 |
| Peldaño 2, sin ningún mínimo de categoría | 23,6 |
| Peldaño 3, con un suplemento más | 23,1 |
| Peldaño 4, con dos suplementos más | 23,1 |
| Peldaño 5, el último, sin tope de secundarias | **18,1** |
| Fuera de la escalera, sin ninguna proporción de BARF | **14,1** |
| **Lo que pide Fascetti (15 % de las kcal)** | **16,7** |
| Mínimo de grasa de FEDIAF | 13,75 |

Lo que esto dice, en orden:

1. **El 16,7 queda por debajo del último peldaño de la escalera** (18,1), así que
   por los caminos que el motor recorre hoy no se alcanza nunca. No es que el
   solver no lo encuentre: es que no existe dentro de esas proporciones.
2. **Nutricionalmente sí existe**, a 14,1 — justo por encima del mínimo de grasa
   de FEDIAF (13,75). Lo que se agota ahí son la propia grasa y el **linoleico**
   (3,82 contra un mínimo de 3,82), que es omega-6 y viene *dentro* de la grasa.
3. **Pero el menú que lo consigue no es comida para un perro**: 1.592 g de
   frambuesa, 601 g de judía verde y 441 g de dorada. Es el solver sin ninguna
   proporción, que es justo lo que el 9 de septiembre produjo raciones de 25 kg
   con un 91 % de verdura, todas verdes.
4. **Y en el último peldaño, lo que baja la grasa es el boniato**: 560 g de los
   1.018 g del menú. Es decir, el motor llega a 18,1 metiendo el único hidrato
   que tiene a mano — que es exactamente lo que hace una dieta veterinaria baja
   en grasa, y lo que una ración BARF no tiene.

O sea: la cifra de Fascetti describe **un producto que no es esto**. Con este
catálogo, para bajar la grasa hay que sustituir calorías de grasa por calorías
de hidrato, y el catálogo tiene un hidrato (boniato) topado por las proporciones
de BARF. No es una limitación del solver ni del reloj.

⚠️ Y lo que hay que decidir primero sigue sin ser el número: es **qué unidad
lleva el 15 %**. Dos fuentes buenas, la misma cifra, dos unidades. Si la
respuesta es «en kcal», entonces **esta patología no se puede formular con este
catálogo** y hay que decirlo en vez de dar un menú que incumple su propia
fuente.

## F-10. Un techo de fibra en enteropatía crónica que el motor no tiene

> «An empirical recommendation is to select diets that contain **less than 8 %
> total dietary fiber** or less than 5 % crude fiber.»

8 % MS = **20 g/1000 kcal**. FEDIAF no pone requisito de fibra —y cuidado, que en
agosto se coló aquí una fila «Fibra» con mínimo y máximo inventados—, así que
esto solo podría vivir como tope de `enteropatia_cronica`. **Medido sobre los 36
menús del catálogo**: mediana 1,2 g/1000 kcal, pero **8 de los 36 pasan de 20**,
hasta 31,1. O sea que el tope **sí haría algo**. No se aplica en esta pasada: su
propia fuente lo llama *«empirical recommendation»* y la tabla de SACN5 que ya usa
esa patología manda. Se pregunta.

## F-11. Lo que SÍ confirma, que también cuenta

- **El 10 % de los premios sale SEIS veces** entre este libro y Ettinger, y el
  cap. 9 añade el matiz que faltaba: es el 10 % de la ingesta **objetivo**, no de
  lo que come hoy. El motor lo calcula sobre `der_objetivo`, que ya va sobre el
  peso objetivo. Aplicado el 11 de septiembre.
- **La proteína sin hidratos en gestación y lactancia**: *«although pregnant and
  lactating bitches do not require a dietary source of carbohydrate, they have an
  increased protein requirement when a carbohydrate-free diet is fed»*. Es
  exactamente el requisito condicional que el motor ya aplica, y ahora tiene una
  fuente más.
- **El shunt sin encefalopatía no lleva restricción de proteína**: *«dietary
  protein should not be restricted in animals with PSSs that are not
  encephalopathic»*. El BLOQUE 90 tenía esa pregunta marcada como
  `no_cambia_ninguna_cifra` —una pregunta cuyas respuestas aplican lo mismo— y
  resulta que **eso es lo correcto**. Ahora hay fuente.
- **La EPI**: esta fuente es **más permisiva** que el motor (*«a low-fat diet is
  not necessary unless steatorrhea is uncontrollable»*, y otros autores llegan al
  34-51 % de las kcal). El motor aplica 37,5 igualmente, que es el extremo alto de
  la Tabla 66-1 de SACN5. Un tope que la fuente considera innecesario no hace
  daño: solo aprieta.
- **Las dietas hepáticas del mercado van por debajo del mínimo de FEDIAF**
  (14-15,5 % de las kcal en proteína = 35-38,75 g/1000 kcal contra los 52,1 de
  FEDIAF). El motor no puede bajar ahí, y eso es la fase 4 de `VETERINARIOS.md`.
- **La segunda fuente del omega-3 de la artrosis**, con sus dos estudios midiendo
  en direcciones distintas: uno no vio diferencia en la cojera medida por
  plataforma de fuerzas, y el otro vio mejorar el apoyo en el 82 % contra el 31 %
  de los controles. Sigue sin aplicarse, y ahora se sabe por qué cuesta decidirlo.
- **Una dieta casera hay que revisarla con un veterinario al menos cada seis
  meses** (cada tres si hay enfermedad). La app no lo dice en ninguna parte.

## F-12. Dos discrepancias medidas de energía en reproducción, y gana FEDIAF

| | Fascetti cap. 7 | El motor (FEDIAF) |
|---|---|---|
| Pico de gestación | +30 a 60 % sobre lo de antes de cruzar | **+62 % (10 kg), +73 % (25), +79 % (40)** |
| Cuándo sube | el último tercio | desde la semana 5 de 9 |
| Pico de lactancia | 2 a 4 veces el mantenimiento | 2,17-2,53 con dos cachorros · 3,45-4,34 con seis · **4,5-4,9 con ocho** |

Las tres van por encima del rango de Fascetti en los perros grandes. Gana FEDIAF
—es la fuente de la fórmula— y en lactancia, además, quedarse corto es el riesgo
de verdad. Apuntado con las dos cifras.


## F-13. El techo de EPA+DHA del NRC, que sale de la misma frase que el linoleico que sí aplicamos

Capítulo 14, leído entero el 11 de septiembre de 2026. La frase:

> «A ratio of 2.6 : 26 of LA : ALA (2.6 : 16 in gestation/lactation) is
> considered safe in dogs, along with a safe upper limit for LA and EPA + DHA of
> 16.3 and 2.8 g/1000 kcal, respectively (NRC 2006).»

De esa frase el motor aplica **dos de sus tres cifras** y no la tercera:

| Cifra | Estado | Qué pasa hoy |
|---|---|---|
| Ratio LA:ALA 2,6-26 (2,6-16 en reproducción) | ✅ aplicado, `requisitos_condicionales.json` | — |
| Techo de LA 16,3 g/1000 kcal | ✅ aplicado el 11-sep, `recomendaciones_libro.json` | **no aprieta nunca**: medido sobre los 216 menús del catálogo, van de 3,20 a 10,50 |
| **Techo de EPA+DHA 2,8 g/1000 kcal** | ❌ **NO aplicado** | **sí aprieta** |

**Y no es teórico. Medido el 11-sep sobre los 216 menús del catálogo:**

| | EPA+DHA por 1000 kcal |
|---|---|
| mínimo | 0,11 |
| mediana | 0,46 |
| máximo | **3,00** |
| **por encima de 2,8** | **5 de 216** |

Los cinco: `Toy_Adulto#3` (3,00), `Mini_Adulto#1` (2,92), `Mediano_Adulto#1`
(2,91), `Pequeño_Senior#1` (2,83), `Gigante_Senior#1` (2,81).

⚠️ **Y FEDIAF no pone máximo de EPA+DHA en ninguna etapa** — las tres columnas de
máximo de esa fila están vacías —, así que el semáforo no puede verlo: es la
familia de siempre, un menú por encima de lo que la fuente llama límite superior
seguro sale **en verde**, porque el semáforo mide los requisitos de un perro
SANO y ahí no hay techo que medir.

**Lo que cuesta aplicarlo, y por qué no se aplicó en la misma pasada que el
linoleico:** el techo del libro se comprueba también en `_garantizar_verificado`,
así que encenderlo deja **esos cinco menús precalculados sin poder entregarse**
hasta regenerar el catálogo con `regenerar_catalogo.py`. No es que la cifra no
quepa —bajar EPA+DHA es quitar pescado, y la mediana está seis veces por debajo
del techo—: es que hay que rehacer los 216 y volver a pasar la batería entera.
Queda escrito con su medida, que es la regla, y es lo siguiente que toca de aquí.

## F-14. El techo de vitamina E del perro, que no teníamos porque FEDIAF no lo pone

Capítulo 14, última línea del bloque de vitamina E. Salió al **cerrar** el
capítulo, no al leerlo por encima: es el hallazgo que justifica el BLOQUE 96.

> «In dogs, a tentative upper limit of 75 IU/kg/day (or 1000–2000 IU/kg diet)
> has been suggested (NRC 2006).»

La primera forma va por kilo de perro y el motor no la sabe usar. **La segunda
sí es una concentración de la dieta**, que es justo la forma del motor:

| | |
|---|---|
| 1000 UI/kg MS, a 4000 kcal EM/kg MS | 250 UI/1000 kcal |
| × 0,671 mg/UI (FEDIAF Tabla VII-14, d-alfa-tocoferol) | **167,75 mg/1000 kcal** |
| extremo laxo (2000 UI/kg MS) | 335,5 mg/1000 kcal |

⚠️ **FEDIAF no pone máximo de vitamina E en ninguna etapa** — las tres columnas
de máximo de esa fila están vacías —, así que este sería el único techo que
tendría el nutriente.

**Medido sobre los 216 menús del catálogo:**

| | vitamina E por 1000 kcal |
|---|---|
| mínimo | 10,05 |
| mediana | 26,86 |
| máximo | 89,28 |
| **por encima del techo estricto (167,75)** | **0 de 216** |

No aprieta hoy. Se apunta igual porque lo que lo tapa es una propiedad del
catálogo de hoy y no una garantía — el mismo motivo por el que se aplicó el Ca:P
del fosfato cálcico aunque ninguno de los cinco menús lo cruzara.

**Y da el dato que le faltaba a la decisión de Elena sobre el SUELO de vitamina
E**, la que se encendió por la mañana y se apagó por la tarde del 11 de
septiembre: el suelo de SACN5 (67,1 mg/1000 kcal) y este techo (167,75) dejan una
ventana de **2,5 veces**, así que el suelo que está escrito y apagado **no choca
con el límite superior seguro** de la otra fuente. Lo que lo hacía caro es otra
cosa, y también está medido: **189 de los 216 menús están por debajo de ese
suelo**, porque en el catálogo no hay un suplemento de vitamina E suelto.

## F-15. El fósforo del oxalato: las dos fuentes van en direcciones contrarias

Capítulo 16, y salió al **cerrarlo**. El motor le aplicaba a este capítulo una
cifra (la vitamina D del oxalato) sin que ninguno de sus 36 elementos tuviera
veredicto — es el segundo caso que cazó el BLOQUE 96.

> «Dietary phosphorus **should not be restricted** with calcium oxalate
> urolithiasis. **Low dietary phosphorus is a risk factor** for calcium oxalate
> urolith formation in cats and dogs.»
>
> «Diets formulated for oxalate prevention in cats and dogs contain phosphorus
> from 0.3 to 2.1 g/Mcal. Concentrations from approximately **1.5 to 2.0
> g/Mcal** have been recommended.»

Y el motor le aplica al oxalato un **techo** de 1500 mg/1000 kcal, de la Tabla
40-5 de SACN5. O sea 1,5 g/Mcal: el extremo **bajo** de lo que Fascetti
recomienda, y **sin ningún suelo debajo**. El mínimo de FEDIAF son 1160, así que
sobre el papel el motor podía entregar un menú de oxalato entre 1160 y 1500, que
es justo donde Fascetti dice que está el riesgo de formar la piedra que se
intenta prevenir.

**Medido el 11-sep, tres perros adultos por la API en peldaño estricto:**

| Peso | Fósforo por 1000 kcal | Magnesio |
|---|---|---|
| 10 kg | 1498,7 | 206,6 |
| 22 kg | 1498,6 | 206,7 |
| 30 kg | 1498,4 | 214,6 |

Los tres salen **pegados al techo**: una ración BARF va sobrada de fósforo y el
solver sube hasta donde le dejan. En la práctica el menú cae en el número que
las dos fuentes comparten.

⚠️ **Y por eso NO se pone un suelo, aunque parezca lo obvio.** Los dos números
son 1500 por los dos lados y el motor solo llega a 1498,7: un suelo de 1500
dejaría al oxalato **sin menú**. Lo que hoy salva la situación es una propiedad
del catálogo, no una garantía — el mismo argumento que llevó a aplicar el Ca:P
del fosfato cálcico aunque ninguno de los cinco menús lo cruzara, pero aquí con
el signo cambiado. Es decisión clínica.

**El magnesio, en cambio, sí coincide.** Fascetti sugiere «from 0.08 to 0.10 %
dry matter or approximately 200 mg magnesium/Mcal» y avisa de que no se restrinja
mucho; el motor aplica techo de 375 y el mínimo de FEDIAF son 200, así que la
ventana es 200-375 y los tres menús salen en 206-215. Dentro y en la zona que la
fuente llama prudente.

**Dos huecos de DATO que deja el capítulo:**

- **Hidroxiprolina** (`<4,4 g/Mcal` en dietas de prevención de oxalato). No es
  ninguno de los 41 nutrientes de FEDIAF ni una clave de ninguna ficha, así que
  el catálogo no lo tiene. Importa porque está sobre todo en **hueso y colágeno**,
  que es lo que más lleva una ración BARF. La cifra es de gato; el día que haya
  dato canino, esto es aplicable. Va a `DATOS_QUE_FALTAN.md`.
- **Purinas**: el libro dice que el dato exacto «can be challenging» de conseguir
  y que a menudo hay que usar la proteína total como indicador. Aquí vamos por
  delante: cada ficha del catálogo trae `purinas_bases` y `purinas_fuente`.
