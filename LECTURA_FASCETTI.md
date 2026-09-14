# Lectura de Fascetti y Delaney, *Applied Veterinary Clinical Nutrition*, 2.ª ed.

**Mismo método que con Ettinger** (ver la cabecera de `LECTURA_ETTINGER.md`): se
lee el capítulo, se apunta lo que dice, y se decide qué sirve. El contador
`leer_fascetti.py` se queda como **red por debajo**, no como la lectura: medido,
de las 18.194 frases del libro el filtro se queda con 657, y de las 17.537 que
tira **1.131 llevan un nutriente y una cifra**.

**Y la regla que costó dos correcciones**: antes de apuntar una discrepancia hay
que mirar **si alguna de las otras fuentes ya decía algo de esto**.

Los capítulos 1 a 6 ya tienen su lectura en `lecturas_fascetti.json` y sus
hallazgos en `HALLAZGOS_FASCETTI.md`.

---

## Cap. 7 — Feeding the Healthy Dog and Cat · LEÍDO

**⚠️ CUARTA fuente para el 10 % de los premios** — ✅ **APLICADO EL 11 DE SEPTIEMBRE** (ver abajo) —, y esta lo dice como
recomendación propia de los autores:

> «The authors recommend that the **energy intake from snacks or treats not
> exceed 10 % of the animal's total daily calories**.»

Van ya **cuatro**: Ettinger cap. 192 (con el mecanismo: la carne suelta
desequilibra el Ca:P, el hígado pasa el máximo de vitamina A), Ettinger cap. 175
(que añade las sobras de mesa y los suplementos), y esta. **La app no lo dice y
no pregunta por los premios.** A estas alturas no es un hallazgo: es una deuda.

**La proteína del sénior, y por qué NO es un problema aunque lo parezca.**

> «The investigators of this study found that older dogs required **up to 50 %
> more protein** than young dogs to maintain labile protein.»

Pero el propio párrafo se frena: «neither of these studies provides **definitive
recommendations** for protein requirements in older dogs». O sea que **no hay
cifra que aplicar**. El motor manda Senior a la columna Adulto de FEDIAF, o sea
52,10 g/1000 kcal.

**Medido, y aquí se acaba la preocupación**:

| Menú sénior | Proteína | % del mínimo | % del «+50 %» (78,2) |
|---|---|---|---|
| 8 kg | 105,1 | 202 % | **134 %** |
| 20 kg | 95,7 | 184 % | 122 % |
| 35 kg | 101,9 | 196 % | 130 % |

Una ración BARF **ya da un 22-34 % por encima** de lo que sugiere ese estudio.
No hay nada que aplicar y no hay riesgo: queda escrito con la medida.

**Y confirma lo que el motor NO hace**: «there is no evidence that protein
restriction is of any benefit to healthy older dogs and cats». No la restringimos.

**Lo demás:** si el BCS pasa de 5, dar un 10 % menos de calorías; si no crece bien
o está delgado, un 10 % más. La leche de vaca y de cabra **no sirve** para
sustituir la de la perra por tener menos grasa, proteína y calorías.

---

## Cap. 8 — Commercial and Home-Prepared Diets · LEÍDO

Refuerza lo del cap. 192 de Ettinger con **otros** estudios: de las dietas caseras
analizadas, **35 caían por debajo de AAFCO** en calcio, fósforo, potasio, zinc,
cobre y vitaminas A y E; y de cinco dietas de eliminación, **las cinco** tenían
nutrientes esenciales por debajo del mínimo. Las dietas caseras de eliminación
nutricionalmente adecuadas solo se recomendaban **el 65 % de las veces en perros**.

La lista de lo que falla vuelve a ser casi la misma que ya mide el documento del
nutricionista, con **potasio** añadido. Comprobado de paso: el potasio también
sale por encima del mínimo en los menús del motor.

«**Carbohydrates are not required in dogs and cats (NRC 2006)**», que es la frase
que sostiene que una ración sin hidratos sea legítima — y que hay que leer junto
al cap. 173 de Ettinger, que **sí** pide hidratos al perro de carreras.

---

## Cap. 9 — Nutritional Management of Body Weight · LEÍDO

**⚠️ TERCERA fuente sobre la energía del perro a dieta, y está con nosotras:**

> «The patient's **resting energy requirement (RER) should be calculated using an
> estimate of its optimal body weight** (RER = 70 × BWkg0.75).»

⚠️ La fórmula va citada **tal cual la escribe el libro**, `BWkg0.75`, que es como
sale del PDF: en el papel el `kg` es un subíndice y el `0.75` un exponente. Aquí
estaba escrita `BW^0,75` —nuestra notación y nuestra coma decimal— **dentro de
las comillas**, y así la cazó el BLOQUE 85: una cita entrecomillada tiene que
decir lo que dice la fuente, y arreglar la tipografía por dentro ya es no
decirlo. Lo nuestro va fuera: es RER = 70 × peso^0,75.

Es lo mismo que dice SACN5 cap. 27 y lo mismo que hace el motor. Con esto el
recuento queda **SACN5 + Fascetti a favor, Ettinger en contra**, y la decisión de
quedarnos como estamos se sostiene sola.

Añade otra forma de plantearlo: «restrict the pet to **60-70 % of the calories it
would normally require to maintain its CURRENT weight**» — ojo, sobre el peso
**actual**, no el ideal, que es una base distinta.

**El ritmo coincide una vez más**: 1-2 % del peso por semana. Y da la aritmética
para estimar cuánto durará: **7.700 kcal por kilo** que haya que perder.

---

## Cap. 10 — Nutritional Management of Orthopedic Diseases (Hazewinkel) · LEÍDO

**Es el capítulo del que ya sale una cifra del motor**: el techo de calcio del
cachorro de raza grande, 1,1 % de materia seca = 2750 mg/1000 kcal. Leído entero,
deja tres cosas más.

**1. Su propio autor pide MENOS calcio, y no cabe.** Ver `HALLAZGOS_FASCETTI.md`
F-7: el rango que recomienda (0,8-1,0 % por 4200 kcal/kg = 1905-2381 mg/1000 kcal)
queda **entero por debajo del mínimo de FEDIAF** para ese mismo perro (2500). Gana
FEDIAF.

**2. Un techo de vitamina D en crecimiento que nadie tenía escrito**: 12,5-25
µg/kg de dieta = 3,125-6,25 µg/1000 kcal. Cabe dentro de FEDIAF, y **6 de los 12
menús de cachorro del catálogo se pasan** (hasta 8,96). No se aplica en esta
pasada: se escribe con su medida y se pregunta (F-8).

**3. La segunda fuente del omega-3 de la artrosis**, que el motor tiene escrito y
sin aplicar — y ahora se ve por qué cuesta decidirlo: un estudio doble ciego en 36
perros con artrosis de codo **no vio diferencia** en la cojera medida por
plataforma de fuerzas, y otro con EPA durante 90 días vio mejorar el apoyo en el
**82 %** contra el **31 %** de los controles.

Lo demás del capítulo son los experimentos con los que se demostró el daño del
exceso —Gran Danés con 3,3 % de calcio, 54.000 UI/kg de vitamina D— y la
fisiología del hueso. Nada de eso es una cifra nueva: son la evidencia detrás del
techo que ya se aplica.

---

## Cap. 11 — Nutritional Management of Gastrointestinal Diseases · LEÍDO

**El hallazgo es de unidades, y es gordo.** El motor aplica a la linfangiectasia
grasa ≤ 37,5 g/1000 kcal, leyendo *«Fat <15 % for dogs and cats»* de la Tabla 58-1
de SACN5, que va en **materia seca**. Este capítulo dice el mismo 15 % **en
kcal**, que son 16,7 g/1000 kcal — un factor de 2,2. Medido con el solver y 30-40
s en perros de 10, 20 y 35 kg: con 37,5 sale menú en los tres, con 20,0 y con 16,7
**no sale en ninguno**. Detalle y tabla en F-9.

Y un **techo de fibra** que el motor no tiene: menos del 8 % de fibra total en
enteropatía crónica = 20 g/1000 kcal. Ocho de los 36 menús del catálogo se
pasarían. No se aplica; se pregunta (F-10).

Mucho del capítulo es humano o felino y va marcado uno a uno.

---

## Cap. 12 — Nutritional Management of Exocrine Pancreatic Diseases · LEÍDO

**Repite la confusión de unidades**: aquí el umbral de «baja en grasa» es *«less
than 20 % fat on an ME basis»*, o sea de las kcal, y medido tampoco cabe.

**Y en la EPI esta fuente es MÁS PERMISIVA que el motor**, lo que confirma que
elegir el extremo alto de la Tabla 66-1 de SACN5 (37,5 g/1000 kcal) fue lo
correcto: aquí se llega a decir que la dieta baja en grasa no hace falta salvo
esteatorrea incontrolable, y que otros autores usan dietas al 34-51 % de las kcal
en grasa.

Vuelve a salir lo de los premios, ahora dentro de una patología.

---

## Cap. 13 — Nutritional Management of Hepatobiliary Diseases · LEÍDO

Casi todo son dosis de fármaco por kg de peso, cifras de analítica o de biopsia, o
hepatología humana y felina. Tres cosas tocan al motor, y las tres **confirman**:

- **Por qué el shunt sin encefalopatía no lleva restricción de proteína.** El
  BLOQUE 90 tenía esa pregunta marcada `no_cambia_ninguna_cifra` —una pregunta
  cuyas respuestas aplican lo mismo—, y resulta que eso es lo correcto. Ahora hay
  fuente.
- **El sodio y el cobre de la hepatopatía ya están puestos** (625 y 2,4 por 1000
  kcal), y el cinc y la vitamina E como suelos.
- **Las dietas hepáticas del mercado van por debajo del mínimo de proteína de
  FEDIAF** (14-15,5 % de las kcal = 35-38,75 g/1000 kcal contra 52,1). El motor no
  puede bajar ahí: eso es la fase 4 de `VETERINARIOS.md`.

