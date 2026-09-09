# SACN5 — LECTURA ÍNTEGRA, CAPÍTULO A CAPÍTULO

> **Método, y por qué es este.** Elena, 9 de septiembre de noche:
>
> «PRIMERO LEE TODO Y APUNTA TODO Y CUANDO YA TENGAS CLARO TODO LO QUE TIENES
>  QUE HACER CUANDO TERMINES LA LECTURA APLICAS PORQUE SI NO ESTAS APLICANDO
>  COSAS QUE LUEGO TIENES QUE CAMBIAR 10 VECES»
>
> Y el caso que lo provocó, el mismo día: leí el Box 1-2, vi «3,5 kcal/g»,
> anuncié que las 68 cifras de patología estaban mal convertidas y que las iba a
> corregir tabla por tabla — y dos comprobaciones después resultó que la única
> tabla de SACN5 que declara densidad dice **4,0**, o sea que estaban bien. Un
> párrafo leído y aplicado antes de leer el siguiente.
>
> **Así que aquí NO se aplica nada.** Este fichero es solo el cuaderno: se lee
> el capítulo entero — texto Y tablas —, se apunta todo lo accionable, y la
> aplicación va después, de una vez, cuando la lectura esté cerrada.

## Estado de la lectura

| Capítulos | Estado |
|---|---|
| 1-4 | leídos en la sesión anterior; hallazgos abajo, y uno de ellos CORREGIDO |
| 5-70 | pendientes de esta noche |

---

## ⚠️ CORRECCIÓN AL HALLAZGO DEL CAP. 1 (la densidad de conversión)

**Lo que quedó escrito antes, y es FALSO:** «SACN5 declara 3,5 kcal/g de materia
seca (Box 1-2 y cap.13), así que las 68 cifras de patología convertidas con 4,0
están un 14 % apretadas de más».

**Lo comprobado, mecánicamente, sobre las 24 tablas de SACN5 que cita
`patologias.json`:**

- Se buscó en las 24 la nota al pie que declara densidad. **Solo UNA la declara**:
  la Tabla 13-3, y dice literal «*Dry matter basis. Concentrations presume an
  energy density of **4.0 kcal/g**. Levels should be corrected for foods with
  higher energy densities.»
- Las otras 23 dicen únicamente «Nutrients expressed on a dry matter basis», sin
  densidad.
- **Comprobado además contra sus propias filas**: la Tabla 13-3 da fósforo
  0,4-0,8 % MS y sodio 0,2-0,4 % MS. A 4,0 kcal/g eso es 2000 y 1000 mg/1000
  kcal, que son **exactamente** las dos cifras que aplica el motor. A 3,5 darían
  2286 y 1143, que no son las nuestras.
- El **3,5 del Box 1-2** aparece en un ejemplo trabajado con un alimento
  concreto; y en el propio capítulo 13, en el MISMO párrafo, el fósforo se
  deriva «at an energy density of 3.5 kcal/g DM» mientras el sodio dice «this
  allowance is for foods with an energy density of **4 kcal/g** (NRC, 2006)».
  O sea: la densidad es de cada derivación, no del libro.

**Conclusión: el ×2,5 estaba bien y no hay 68 cifras que reescalar.** Lo que sí
hace falta es que eso deje de depender de que alguien lo lea: cada cifra tiene
que llevar su conversión como DATO (valor de la fuente + unidad + densidad +
cita) y una auditoría que la rehaga. Eso es `auditar_conversiones.py`, escrito
esta noche y pendiente de rellenar sus 92 bloques — **en la fase de aplicar, no
ahora**.

**Queda una pregunta abierta y con datos, para Elena:** la Tabla 27-4 (obesidad)
recomienda en una de sus propias filas «Foods for weight loss should contain
≤3,4 kcal ME/g» de materia seca. No dice que sus otras filas estén expresadas a
esa densidad — no lo dice ninguna tabla salvo la 13-3 —, pero si lo estuvieran,
sus cifras subirían un 18 %. Es la única de las 24 donde la tabla propone una
densidad distinta de 4,0 para el propio alimento. Se apunta, no se decide.

---

## Hallazgos por capítulo

### CAP. 5 — Nutrientes y energía

**⚠️ TABLA 5-3 — LA CIFRA DEL FRÍO, QUE FEDIAF DEJA COMO RANGO DE 1 A 9.**
«Influence of low environmental temperatures on daily energy requirement (DER)»,
literal:

| Raza | Aumento del DER (%) | Temp. baja | Temp. normal |
|---|---|---|---|
| Labrador retriever y beagle | 25 (12-43) | 8,5 °C | 15 °C |
| Gran Danés | 22 | Invierno | Verano |
| **Perros de pelo CORTO** | **95** | 7,6 °C | 25 °C |
| **Perros de pelo LARGO** | **59,5** | 7,6 °C | 25 °C |
| Beagle | 70,5 | −17 °C | 17 °C |
| Perro de trineo de Alaska | 61,5 | −17 °C | 17 °C |

Fuentes que cita: Blaza 1982, Zentek y Meyer 1992, Meyer 1990.

**Qué cambia esto respecto a lo que quedó escrito de FEDIAF §7.2.3.5.** Allí el
pendiente decía «no hay UNA cifra, hay un rango de 10 a 90 %, así que es
decisión». **Con esta tabla sí hay cifras**, y por tipo de pelo y por salto de
temperatura concreto — que es justo lo que hacía falta. El pendiente cambia de
«falta la cifra» a **«falta la pregunta en la ficha»**: la app no sabe si el
perro duerme fuera ni a qué temperatura. Y ojo al sentido, que es el contrario
del que uno diría de memoria: **el de pelo corto necesita más subida (95 %) que
el de pelo largo (59,5 %)**, porque aísla peor.

APLICAR: no todavía — necesita una pregunta nueva en la ficha, que es producto.
Lo que sí cambia YA es el texto del pendiente, que hoy afirma que no hay cifra.

**Tabla 5-2 — DER de lactación por número de cachorros.** 3,0 × RER con 1
cachorro; 3,5 con 2; 4,0 con 3-4; 5,0 con 5-6; 5,5 con 7-8; ≥6,0 con ≥9. Y
crecimiento: 3 × RER del destete a los 4 meses, 2 × RER de ahí al tamaño adulto.
COMPROBAR en la fase de aplicar si `der.py`/`src/der.js` usan el número de
cachorros o un factor fijo.

**Frases con cifra, del texto y no de las tablas:**
- Senior: «senior dogs should be offered foods providing a **15 to 20 % caloric
  reduction**» (Kienzle y Rainbird 1991, Finke 1994, Harper 1998). Nuestro
  escalón senior es −15 sobre 110 = **−13,6 %**, o sea justo por debajo del
  extremo bajo del rango. Coincide con FEDIAF VII-6 (95 contra 110). No es un
  error, pero conviene tenerlo escrito: las dos fuentes dan lo mismo y nosotros
  vamos un pelo por debajo.
- AAFCO vía SACN5: «canine foods … should contain **at least 22 % DM protein for
  growth, and 18 % DM protein for adult maintenance**». A 4,0 kcal/g son 55 y 45
  g/1000 kcal; los mínimos de FEDIAF que aplicamos (62,5 y 52,1) son MÁS altos.
  Nada que cambiar.

### CAP. 6 — Minerales: DOS hallazgos duros, y son de datos del catálogo

**1. EL ÓXIDO DE HIERRO NO SE ABSORBE, Y ANALÍTICAMENTE PARECE HIERRO.** Literal:

> «Typical iron sources include ferrous sulfate, ferric chloride, ferrous
> fumarate, ferrous carbonate and iron oxide. **The iron in iron oxide, however,
> is not biologically available.** Iron oxide is often added to pet foods to
> impart a “meaty red” color … **Analytically, a pet food containing iron oxide
> will appear to be high in iron, but may not be high in available iron.** … (e.g.,
> 0.04 % DM iron oxide in a moist food contributes 933 mg iron/kg of food).»

**2. EL ÓXIDO DE COBRE TIENE DISPONIBILIDAD CERO — Y EL HÍGADO DE CERDO TAMBIÉN.**
Literal:

> «Results showed that **copper availability was essentially zero from copper
> oxide and pork liver.** Beef, sheep and turkey liver, however, were highly
> available sources of copper. **AAFCO (2007) has recommended that pet food
> companies discontinue the use of copper oxide as a copper source**…»

⚠️ Lo del **hígado de cerdo** no es una nota de fabricación: es una ficha de
catálogo. COMPROBAR en la fase de aplicar si existe y qué cobre declara.

**3. Y LA TABLA QUE FALTABA PARA LOS MINERALES**, hermana de la Tabla VII-14 de
FEDIAF (que es solo de vitaminas): el capítulo trae el **% de mineral elemental
de cada sal**. Las que nos tocan por ser fuentes típicas de multivitamínico:

| Mineral | Fuente | % elemental |
|---|---|---|
| Calcio | carbonato cálcico 39 · citrato 24 · sulfato 23 · cloruro 35 | |
| Ca y P | harina de hueso **24 Ca / 12,6 P** · fosfato dicálcico 18-24 Ca / 18,5 P | |
| Magnesio | óxido 54 · sulfato 9 | |
| Potasio | citrato 36 · cloruro 50 · sulfato 42 | |
| Hierro | sulfato ferroso 33 (mono) / 20 (hepta) · fumarato 32,9 · carbonato 48,2 · **óxido férrico 69,9 (NO disponible)** | |
| Cobre | carbonato 57,5 · cloruro 37,3 · hidróxido 65,1 · **óxido 79,9 (disponibilidad CERO)** · sulfato 25,4 | |
| Manganeso | carbonato 47,8 · óxido 77,4 · sulfato 22,7-32,5 | |
| Zinc | carbonato 56 · cloruro 48 · óxido 72 · sulfato 22,7-36,4 | |
| Yodo | yodato cálcico 65,1 · yoduro potásico 76,4 · yoduro cuproso 66,6 | |
| Selenio | selenito sódico 45,6 · selenato sódico 41,8 | |

Fuente: adaptada del NRC 1986; nota del propio libro: «Actual mineral levels in
technical grade sources may vary».

APLICAR (fase de aplicar): esta tabla va al lado de la VII-14 en
`fediaf_conversiones_vitaminas.json` — o mejor, ese fichero pasa a llamarse algo
que cubra las dos, porque el problema es el mismo: **la etiqueta declara la sal y
el catálogo anota la cifra como si fuera el elemento**. Y con dos avisos de
disponibilidad, no solo de conversión: óxido de hierro y óxido de cobre son
números que existen en la etiqueta y NO llegan al perro.

### CAPS. 7, 8, 9 — sin nada que aplicar
Antioxidantes (7), fabricación y mercado (8), etiquetado (9). El 9 trae las
reglas de porcentaje de las etiquetas europeas («With rabbit: at least 4 % of
the named species», «Beef dinner: at least 26 %»), que son de rotulación
comercial y no tocan el motor. Del 7 no sale ni una frase normativa con cifra.

### CAP. 10 — Comida casera (nuestro capítulo) — UNA cifra aplicable

**EL 10 % DE LOS EXTRAS, y es la cifra que le falta al panel «Esto es todo lo que
come».** Literal:

> «The occasional feeding of table foods **should not be of concern for healthy
> pets unless the food composes more than 10 % of the daily dry matter intake**
> (Lewis et al, 1987).»

Ese panel se justificó con el 55 % del cap.3 (cuánto de la dieta puede llegar a
ser «lo de fuera» en la práctica). Esto da el **umbral**: por encima del 10 % de
la materia seca diaria, lo de fuera deja de ser inocuo. Es un número que se le
puede decir al dueño y hoy no se le dice.

**Lo demás del capítulo no toca el motor**: las tablas 10-2 a 10-8 son recetas
caseras COCINADAS con arroz/pasta como fuente de energía, o sea otra estructura
de ración; y el caso del 30 % de carne y el 10 % de grasa es de un GATO. Nota de
contexto útil: «veterinary supplements contribute between 0 and 300 % of the
vitamin-mineral requirements», que es por qué el motor tiene `dosis_max` por
ficha.

⚠️ El «1,1 % de MS de calcio para prevenir panosteitis» que cita `CLAUDE.md` como
«Fascetti cap.10» **no está en este capítulo**: es del libro de Fascetti, otra
fuente. No hay contradicción, pero conviene no confundirlos al citar.

### CAPS. 11 y 12 — nada que aplicar
Seguridad alimentaria y toxicología (11) y la relación con el cliente (12). Del
11, lo único con cifra es de manejo doméstico: «Spoilage bacteria require at
least 30 % moisture for growth whereas molds require 5 to 15 %», y los tiempos de
refrigeración «usually three to five days», que no contradicen nada de lo que
dice la app.

### CAP. 15 — Reproducción. EL CAPÍTULO MÁS CARGADO HASTA AHORA

Rawku ofrece gestación y lactancia, y este capítulo tiene **tres cosas
cuantificadas que el motor no aplica** más un refuerzo de una que sí.

**A. LA DIETA SIN HIDRATOS EN LA PERRA PREÑADA — TRES CIFRAS, Y NOSOTROS
APLICAMOS UNA.** Una ración BARF es exactamente «a carbohydrate-free food».
Literal:

> «Feeding a **carbohydrate-free food** to pregnant bitches **increases the risk
> of hypoglycemia and ketosis** during late pregnancy. Furthermore, the lactose
> concentration in the milk may **decrease by 40 %** during peak lactation.»
>
> Box 15-1: «If a carbohydrate-free food is fed, gluconeogenic precursors such as
> **protein should be increased by at least 50 %** when energy requirements are
> moderate and **may have to be doubled** if the energy requirement of the dam is
> high.»
>
> «If no carbohydrate is given, protein intake must almost be doubled; the food
> must provide **at least 12 to 13 g digestible protein/BWkg^0,75**»
>
> «In a study in which a food that had about **50 % DM protein** was fed, no
> problems with hypoglycemia or ketosis resulted and puppies were born healthy
> (Blaza et al, 1989).»

O sea tres cuantificaciones independientes del MISMO ajuste: (a) +50 % o ×2 sobre
el requisito, (b) un absoluto de 12-13 g de proteína digestible por kg^0,75, y
(c) un 50 % de MS de proteína que funcionó en un estudio = **125 g/1000 kcal** a
4,0 kcal/g.

COMPROBAR al aplicar: qué cifra usa hoy `proteina_en_reproduccion_sin_hidratos`
(viene de FEDIAF/NRC) y si cae dentro o por debajo de estas tres. **La (b) es
distinta en naturaleza** — va por peso metabólico, no por concentración — y sería
la primera regla de ese tipo en el motor.

Y el número que cierra el círculo: «Providing approximately **20 % of the energy
from carbohydrate** … translates to about **23 % DM carbohydrate**» — o sea que
la fuente convierte 20 % de la energía en 23 % de MS, que **solo cuadra a ~4,0
kcal/g** (0,20 × 1000 / 4 = 50 g/1000 kcal = 20 % de MS a 4,0… con hidratos a 3,5
kcal/g de ME sale 23 %). Es otra confirmación indirecta de la densidad de
referencia.

**B. EL DHA TIENE QUE SER AL MENOS EL 40 % DEL EPA+DHA — Y ESO NO SE APLICA.**
Literal:

> «Foods for late gestation and peak lactation should contain the minimum
> recommended allowance of DHA plus EPA of **at least 0.05 % (DM)** (NRC, 2006).
> Therefore, **DHA needs to be at least 40 % of the total DHA plus EPA, or
> 0.02 % DM**.»

El EPA+DHA ≥0,05 % MS = 0,125 g/1000 kcal, que es **exactamente** lo que ya pide
FEDIAF para crecimiento y reproducción. Pero **el reparto no lo pide nadie en el
motor**: hoy da igual que los 0,125 g sean todo EPA. La cifra existe y es
0,02 % MS = **0,05 g de DHA por 1000 kcal**, y el catálogo tiene la clave `dha`.
Es una regla condicional nueva (un nutriente que depende de otro), con cifra.

**C. LA TABLA 15-5 (KNF de perras reproductoras), columna gestación/lactancia,
base MS.** Convertida a por-1000-kcal a 4,0:

| Factor | Fuente (%MS) | Por 1000 kcal |
|---|---|---|
| Densidad energética | ≥4,0 kcal ME/g | (es la densidad, no un nutriente) |
| Proteína bruta | 25-35 | 62,5-87,5 g |
| Grasa bruta | ≥20 | ≥50 g |
| DHA | ≥0,02 | ≥0,05 g |
| Hidratos digestibles | ≥23 | (no aplicable a BARF; ver A) |
| Calcio | 1,0-1,7 | 2500-4250 mg |
| Fósforo | 0,7-1,3 | 1750-3250 mg |
| Ca:P | 1:1-2:1 | 1,0-2,0 |

⚠️ Y el aviso que la acompaña, que es de seguridad y no de nutrición:
> «**excessive calcium intake during pregnancy may decrease activity of the
> parathyroid glands and predispose the bitch to eclampsia during lactation**…
> **Calcium supplementation is not recommended during gestation or lactation**»

COMPROBAR al aplicar: FEDIAF da calcio máx 1,60 % MS en crecimiento/reproducción
(=4000 mg) y Ca:P máx 1,6:1, o sea que **FEDIAF ya es más estricto que SACN5 en
las dos**. Lo que NO tenemos es el aviso de la eclampsia, que es texto y va al
dueño.

**D. Lactancia de raza grande**: «Foods for lactating large-breed dogs should
provide **at least 18 % DM fat and 4.0 to 5.0 kcal ME/g DM**» y «foods containing
**25 to 35 % DM crude protein and 1.0 to 1.6 % DM calcium** are adequate».

**E. Energía de gestación y lactancia — DOS fórmulas que hay que cruzar con
`der.py`.**
- Tabla 15-6, gestación: semanas 1-4 = DER; semana 5 = DER + **18 kcal/kg PV**;
  semanas 6-8 = DER + **36 kcal/kg PV**; semana 9 = DER + **18**. Y «During
  gestation DER is estimated as **1,9 × RER** (132 kcal ME/kg^0,75)».
- Tabla 15-7, lactancia, método 1: `ME = DER + (PVkg × [24n + 12m] × L)`, con
  **DER de la perra lactante = 145 × kg^0,75**, factores de semana L = 0,75 /
  0,95 / 1,1 / 1,2 (semanas 1 a 4), **n = nº de cachorros si son 1-4** y **m = si
  son 5-8** (m = 0 con menos de cinco).
- Tabla 5-2 da la versión rápida: 3,0 × RER con 1 cachorro … ≥6,0 × RER con ≥9.

COMPROBAR al aplicar: si `der.py` y `src/der.js` usan el **número de cachorros y
la semana de lactancia**, o un factor fijo. Si es fijo, aquí hay una diferencia
que puede ser grande — entre 3,0 y 6,0 × RER hay el doble de comida.

**F. Peso de la perra**: «After parturition, bitches should weigh about **5 to
10 % more than their pre-breeding weight**» y «Retention of more than 10 % above
pre-breeding weight» es lo indeseable.

### CAP. 17 — Crecimiento. Dos cosas nuevas

**A. EL DHA TAMBIÉN EN CRECIMIENTO.** La Tabla 17-1 pide **DHA ≥0,02 % MS en
las DOS columnas** (cachorro de <25 kg y de >25 kg de adulto), igual que la 15-5
de reproducción. O sea que el mínimo de DHA — **0,05 g/1000 kcal a 4,0** — vale
para crecimiento Y reproducción, y el motor no lo aplica en ninguna de las dos.
Refuerza el hallazgo B del cap.15: no es una cifra suelta de un capítulo, es la
misma en dos.

Resto de la 17-1, ya aplicado o más flojo que lo nuestro: proteína 22-32 % MS
(55-80 g/1000 kcal), grasa ≥10-25 %, densidad 3,5-4,5 kcal/g, y el calcio y el
fósforo con sus dos columnas por peso adulto (>25 kg), que son los techos que
entraron el 9 de septiembre.

**B. LA ENERGÍA DE CRECIMIENTO VA POR FRACCIÓN DE PESO ADULTO, NO POR EDAD.**
Tabla 17-2, literal:

| Tramo | × RER | kcal/kg^0,75 |
|---|---|---|
| Del destete al 50 % del peso adulto | 3 | 210 |
| Del 50 al 80 % del peso adulto | 2,5 | 175 |
| ≥80 % del peso adulto | 1,8-2,0 | 125-140 |

Y el Gran Danés otra vez aparte: «Great Dane puppies **may need 25 % more energy
during the first two months after weaning = 250 kcal/BWkg^0,75**», y «may not
grow when daily energy intake is less than 175 kcal ME/BWkg^0,75».

⚠️ **Esto NO es lo que aplica el motor.** El respaldo de crecimiento de `der.py`
usa la regla del **cap.5** (3 × RER hasta los 4 meses, 2 × RER después), que es
por EDAD y tiene dos escalones. La del cap.17 es por FRACCIÓN DE PESO ADULTO y
tiene tres. Las dos son de SACN5 y no se contradicen — dicen lo mismo con
variables distintas —, pero la del capítulo de crecimiento es más fina y la app
**ya pregunta el peso adulto estimado**, así que la tiene disponible.
COMPROBAR y decidir al aplicar; no es un error, es una versión mejor de lo mismo.

### CAP. 18 — Perro de trabajo. Tabla 18-9 leída entera

| Factor | Sprint | Intermedia baja | Intermedia alta | Resistencia |
|---|---|---|---|---|
| Densidad (kcal ME/g MS) | 3,5-4,0 | 4,0-5,0 | 4,5-5,5 | >6,0 |
| Grasa (%MS) | 8-10 | 15-30 | 25-40 | >50 |
| Proteína (%MS) | 22-28 | 22-32 | 22-32 | 28-34 |
| Hidratos NFE (%MS) | 55-65 | 30-55 | 30-35 | <15 |
| Digestibilidad MS | >80 % | >80 % | >80 % | >80 % |
| **Vitamina E** | **≥500 UI/kg MS** | ≥500 | ≥500 | ≥500 |
| Vitamina C | 150-250 mg/kg MS | igual | igual | igual |
| Selenio | 0,5-1,3 mg/kg MS | igual | igual | igual |

- La **vitamina E ≥500 UI/kg MS** es la misma en las cuatro columnas = **125
  UI/1000 kcal**. COMPROBAR contra lo que aplica hoy
  `antioxidantes_del_perro_de_trabajo`.
- El **selenio 0,5-1,3 mg/kg MS** es el CUARTO sitio donde aparece ese rango
  (con la 35-3, la 18-9 y el cap.7), y sigue saliéndose por arriba del máximo
  legal de FEDIAF. Ya está escrito como pregunta.
- La **vitamina C** no la pide FEDIAF (el perro la sintetiza) y ya está decidido
  que no se aplica.
- Y una frase del texto que corrobora el 10 % del cap.10: «each snack should
  compose **no more than 10 % of the normal daily food amount**».
- Contexto útil contra un mito: «The idea that athletic dogs require markedly
  more protein than nonworking dogs is **inaccurate**… the need for protein and
  other nutrients increases only slightly with increasing workload». Lo que sube
  es la ENERGÍA. Eso es exactamente lo que hace `BASE_ACTIVIDAD`.

### CAPS. 16, 19-24 — felinos y neonatos: nada que aplicar
El 16 (cachorros lactantes) y el 23 son de neonatos, que la app no cubre. El 19
al 24 son **todos de gato** (comprobado en la primera línea de cada uno:
«Feeding Young Adult Cats», «…Mature Adult Cats», «…Reproducing Cats»,
«…Nursing and Orphaned Kittens», «…Growing Kittens»). Copiar una cifra de ahí
sería el error de especie que ya está documentado con el selenio del cap.3 de
FEDIAF. Del 19 solo se retiene una corroboración: «table foods and treats fed at
**less than 10 % of the total daily intake** should be safe» — el mismo 10 % del
cap.10 y del cap.18, ahora en tres capítulos distintos.

### CAPS. 25 y 26 — alimentación asistida y parenteral: no aplicable
Sondas, jeringa y nutrición parenteral. La app no hace nada de eso. Dos cifras
que sí sirven de contraste y no cambian nada:
- «most pet foods … should contain **at least 146 mg arginine/100 kcal for adult
  dogs**» = 1,46 g/1000 kcal. El mínimo de FEDIAF que aplicamos es **1,51**, o
  sea que vamos por encima.
- «initially feeding patients at RER, or at least 60 % of RER … is a rational and
  safe recommendation» — es realimentación hospitalaria, no una ración de casa.

### CAP. 27 — Obesidad. Tabla 27-4 entera (columna PERRO)

| Factor | Pérdida de peso | Evitar recuperarlo | Por 1000 kcal (a 4,0) |
|---|---|---|---|
| Densidad energética | ≤3,4 kcal ME/g MS | igual | — |
| Grasa | ≤9 % | ≤14 % | 22,5 / 35 g |
| Fibra | 12-25 % | 10-20 % | 30-62,5 g |
| Proteína | ≥25 % | ≥18 % | ≥62,5 g |
| Lisina | ≥1,7 % | — | ≥4,25 g |
| Hidratos | ≤40 % | ≤55 % | (no aplica a BARF) |
| L-carnitina | ≥300 ppm | igual | ≥75 mg |
| Vitamina E | ≥400 UI/kg | igual | ≥100 UI = **67,1 mg** de tocoferol natural |
| Vitamina C | ≥100 mg/kg | igual | ≥25 mg |
| Selenio | 0,5-1,3 mg/kg | igual | 125-325 µg |
| **Sodio** | **0,2-0,4 %** | igual | **500-1000 mg** |
| **Fósforo** | **0,4-0,8 %** | igual | **1000-2000 mg** |

**Lo que ya cuadra:** L-carnitina 75 ✓, lisina 4,25 ✓, proteína 62,5 ✓, fibra 30
✓, vitamina E 67,1 ✓ (400 UI × 0,671 ÷ 4).

**El sodio y el fósforo de esta tabla NO están en la entrada de obesidad — y no
hace falta que estén:** son **exactamente los mismos números** que la Tabla 13-3
del perro adulto sano (P 0,4-0,8 %, Na 0,2-0,4 %), que ya se aplican a TODO perro
desde el 8 de septiembre vía `recomendaciones_libro.json` (2000 y 1000). O sea
que el perro obeso ya los recibe. Merece quedar escrito para que nadie los
«descubra» otra vez.

**La grasa sí discrepa, y a propósito:** la fuente dice ≤9 % MS = **22,5**
g/1000 kcal y el motor aplica **30**. Está declarado como criterio nuestro en la
propia ficha. Al aplicar habrá que marcarlo `ajustado_a_proposito`.

**⚠️ Y LA DENSIDAD, que es la única tabla de las 24 que propone una distinta de
4,0:** «Foods for weight loss … should contain **≤3,4 kcal ME/g**». No dice que
sus otras filas estén expresadas a esa densidad — ninguna tabla lo dice salvo la
13-3, que dice 4,0 —, pero si lo estuvieran, sus cifras subirían un 18 %. Queda
como pregunta con datos, no como cambio.

### CAP. 33 — Crecimiento de raza grande. Tabla 33-5 entera

| Factor | Recomendación | Por 1000 kcal (a 4,0) |
|---|---|---|
| Densidad energética | 3,2-4,1 kcal/g | — |
| Grasa | 8,5-17 % MS | 21,25-42,5 g |
| **DHA** | **>0,02 % MS** | **>0,05 g** |
| Calcio | 0,8-1,2 % MS | 2000-3000 mg |
| Fósforo | «basado en el calcio, para mantener el ratio» | — |
| Ca:P | 1,1:1 a 2:1 («el extremo bajo es el preferido») | — |
| Suplementos | «None recommended if a commercial food is fed» | — |

Nota al pie: «*Dry matter basis» — **sin densidad declarada**, como las otras 22.
Y el asterisco del DHA dice para qué es: «***For improved learning».

- **El 2750 mg/1000 kcal de calcio que aplicamos = 1,1 % MS a 4,0**, que cae
  dentro del 0,8-1,2 % de esta tabla y es el número de Fascetti. ✓
- **Confirmada la contradicción que ya estaba apuntada en `CLAUDE.md`**: la Ca:P
  de la 17-1 es 1,5:1 y la de la 33-5 es **2:1**, para la misma población. Aquí
  además dice cuál prefiere: «the lower end of range is preferred».
- Zinc: «Canine growth foods should contain **100 mg/kg DM zinc** (NRC, 2006)» =
  25 mg/1000 kcal, que es **exactamente** el mínimo de FEDIAF en crecimiento. ✓
- «free-choice feeding is not recommended for large- and giant-breed puppies
  until they have reached skeletal maturity (**about 12 months of age or at least
  80 to 90 % of adult weight**)» — es manejo, no nutriente, y la app ya da la
  ración medida en gramos, que es lo contrario de ad libitum.

### ⚠️⚠️ EL HALLAZGO QUE SE REPITE EN CUATRO SITIOS: EL DHA

El mínimo de **DHA ≥0,02 % MS = 0,05 g/1000 kcal** aparece, con la misma cifra:

1. **Tabla 15-5** — reproducción (gestación/lactancia).
2. **Tabla 17-1** — crecimiento, en **las dos** columnas de peso adulto.
3. **Tabla 33-5** — crecimiento de raza grande y gigante.
4. Y el texto del **cap.15** y del **cap.33** lo derivan igual: «the minimum
   recommended allowance of DHA plus EPA of at least 0,05 % (DM) (NRC, 2006).
   Therefore, **DHA needs to be at least 40 % of the total DHA plus EPA, or
   0,02 % DM**».

**El motor pide EPA+DHA ≥0,125 g/1000 kcal (FEDIAF) y NO pide reparto.** Hoy un
menú de cachorro o de perra gestante cumple con los 0,125 g siendo todo EPA, y
saldría verde. La cifra existe, es canina, está en cuatro sitios y se deriva de
una fuente que ya usamos (NRC 2006). **Es el candidato más claro de todo lo
leído hasta ahora a convertirse en regla del motor.**

### CAP. 34 — Artrosis. Tabla 34-2 entera, y DOS filas que no tenemos

| Factor | Fuente | Nuestro valor | ¿Cuadra? |
|---|---|---|---|
| Omega-3 totales | 3,5-4,0 % MS | 8,75 (escrito, no aplicado) | ✓ = 3,5 % |
| EPA | 0,4-1,1 % MS | 1,0 | ✓ = 0,4 % |
| Omega-6:omega-3 | <1:1 | 1,0 (escrito, no aplicado) | ✓ |
| L-carnitina | ≥300 mg/kg MS | 75 | ✓ |
| **Glucosamina HCl** | **≤0,10 % MS** | — | **no existe la columna** |
| **Condroitín sulfato** | **≤0,08 % MS** | — | **no existe la columna** |
| Vitamina E | ≥400 UI/kg MS | 67,1 mg | ✓ (400 × 0,671 ÷ 4) |
| Vitamina C | ≥100 mg/kg MS | — | no se aplica (el perro la sintetiza) |
| Selenio | 0,5-1,3 mg/kg MS | 125 (escrito, no aplicado) | ✓ |
| Fósforo | 0,3-0,7 % MS | 1750 | ✓ = 0,7 % |
| Sodio | 0,2-0,4 % MS | 1000 | ✓ = 0,4 % |

**La glucosamina y el condroitín son MÁXIMOS, no suelos**, y el texto los da
también por peso: «glucosamine HCl and chondroitin sulfate should not exceed
**15 mg and 12 mg/kg body weight/day**, respectively». El catálogo no tiene esas
columnas y ningún alimento las aporta, así que hoy no hay nada que topar — pero
si algún día entra un condroprotector al catálogo, el techo ya está localizado.

⚠️ **Y AQUÍ ESTÁ LA SEGUNDA TABLA QUE DECLARA LA DENSIDAD**, y dice 4,0: «in a
food with an **energy density of 4 kcal/g DM**, glucosamine HCl and chondroitin
sulfate should not exceed [0,10 y 0,08 %]». O sea que cuando SACN5 necesita
convertir entre %MS y mg/kg de peso, usa 4,0. Junto con la nota de la Tabla 13-3
son **dos declaraciones explícitas de 4,0 y ninguna de 3,5** para este uso.

Nota de manejo: «The daily intake of the therapeutic osteoarthritis food should
be based on **80 % of the DER for an ideal body weight** and fed for
approximately one month» — es una pauta de adelgazamiento del artrósico, no un
nutriente.

### CAP. 35 — Disfunción cognitiva. Confirmada fila a fila
Vitamina E ≥750 **mg**/kg MS (=187,5 ✓, y ojo: aquí es mg y en las otras cuatro
tablas es UI, que es justo por lo que los dos valores del motor son distintos),
vitamina C ≥150 mg/kg, selenio 0,5-1,3 mg/kg, omega-3 totales >1 %, L-carnitina
y ácido α-lipoico, y una fila que no es un nutriente: «**Fruits and vegetables:
1 % of each of five vegetable and fruit ingredients**». Esa última es de
variedad, no de cifra, y una ración BARF con su categoría de verduras ya la
cumple de sobra.

### CAP. 36 — Cardiopatía. Tres cosas de TEXTO que el motor no puede dar
1. **El agua.** «**Distilled water or water with less than 150 ppm sodium**
   should be considered for patients with advanced CHF in whom more strictly
   limited sodium intake is desirable.» La app baja el sodio de la COMIDA y no
   dice nada del agua. Es un aviso, no un nutriente.
2. **La L-carnitina terapéutica.** «dogs … **40 kg are most often affected and
   should receive 2 g of L-carnitine mixed with food three times daily**» — seis
   gramos al día, que es una dosis y no una concentración. Va como aviso, igual
   que la taurina de la miocardiopatía.
3. **El potasio con diuréticos.** «Patients receiving diuretic therapy should
   receive adequate amounts of potassium.» El motor tiene techo de potasio en
   renal y **suelo** ninguno en cardiopatía; el aviso es lo que corresponde.

### CAP. 37 — Renal. Tabla 37-9 entera, y todo cuadra
Proteína 14-20 % · Fósforo 0,2-0,5 % · Sodio ≤0,3 % · Cloruro 1,5 × sodio ·
Potasio 0,4-0,8 % · **Omega-3 0,4-2,5 %** · **Omega-6:omega-3 de 1:1 a 7:1** ·
Vitamina E ≥400 UI/kg (perro) · Vitamina C ≥100 mg/kg (perro).

Todos nuestros números salen de ahí: 1200 (P), 750 (Na), 1125 (Cl), 2000 (K),
1,0 (omega-3), 7,0 (ratio), 67,1 (vitE). **La proteína es la excepción y hay que
mirarla al aplicar**: la fuente dice 14-20 % MS = 35-50 g/1000 kcal y el motor
topa en **62,5**, más flojo — porque 50 cae POR DEBAJO del mínimo de FEDIAF para
adulto (52,1) y ahí ya no es un tope, es una dieta de prescripción.

Y una cifra clínica que sirve de aviso y no de límite: «nutritional management
should be considered by **stage 2 CKD** and is clearly indicated when **serum
creatinine exceeds 2 mg/dl (179 µmol/l)**».

### LAS NUEVE TABLAS DE RECOMENDACIÓN CANINA QUE NO TIENEN PATOLOGÍA EN EL MOTOR

Barrido completo: de las **121 tablas «Key nutritional factors»** de SACN5 (476
tablas en total, contadas sin cortar la salida — la lección de
`VERIFICACION_FILA_A_FILA.md`), las que son **recomendación canina** están todas
mapeadas contra `patologias.json` menos estas nueve. Aquí van leídas enteras,
para que la decisión de ofrecerlas o no se tome con los números delante.

**Tabla 50-3 — disfagia por lesión obstructiva o motilidad aberrante**
Densidad ≥4,5 kcal/g · Grasa **≥25 %** MS · Proteína ≥25 % MS.

**Tabla 50-4 — esofagitis / reflujo gastroesofágico**
Densidad ≥4 kcal/g · Grasa **≤15 %** MS · Proteína ≥25 % MS.
⚠️ Las dos esofágicas piden **lo contrario** en grasa (≥25 % vs ≤15 %), y el
texto dice por qué: «High dietary fat delays gastric emptying and reduces lower
esophageal sphincter pressure, which promotes reflux». No se pueden ofrecer como
una sola «patología esofágica».

**Tabla 52-2 — gastritis y úlcera gastroduodenal**
Potasio 0,8-1,1 % · Cloruro 0,5-1,3 % · Sodio 0,3-0,5 % · Proteína ≤30 % (vía
«highly digestible») o 16-26 % (vía dieta de eliminación, una o dos fuentes).

**Tabla 53-2 — dilatación-vólvulo gástrico**
«**The only key nutritional factor**» es el **tamaño del bocado**: «>30 mm was
protective against GDV in giant-breed dogs». Ni un nutriente. Es exactamente lo
que ya dice el aviso de `riesgo_gdv`, así que **esta tabla está cerrada y no
falta nada**.

**Tabla 54-2 — trastornos de motilidad y vaciado gástrico**
Densidad 4,0-4,5 · Potasio 0,8-1,1 % · Cloruro 0,5-1,3 % · Sodio 0,3-0,5 % ·
Grasa **≤15 %** · Fibra bruta ≤5 %, evitando fibras gelificantes (pectinas y
gomas) · Forma: húmeda.

**Tabla 56-2 — gastroenteritis / enteritis aguda**
Sodio 0,3-0,5 % · Cloruro 0,5-1,3 % · Potasio 0,8-1,1 % · Grasa 12-15 % (alta
digestibilidad) u 8-12 % (con fibra) · Fibra ≤5 % o 7-15 % según enfoque.

**Tabla 59-1 — síndrome de intestino corto**
Grasa 12-15 % · Fibra ≤5 % (soluble o mixta) · **Hidratos: sin lactosa** ·
Digestibilidad ≥87 % proteína y ≥90 % grasa.

**Tabla 62-1 — colitis (diarrea de intestino grueso)**
Proteína adulto 15-30 %, cachorro 22-32 % · Grasa 8-15 % · Digestibilidad ≥87/90 %.

**Tabla 47-4 — enfermedad periodontal**
Vitamina E ≥400 UI/kg · Vitamina C ≥100 mg/kg · Selenio 0,5-1,3 mg/kg ·
**Fósforo 0,4-0,8 %** · **Sodio 0,2-0,4 %**.
⚠️ **Esta no aporta ningún número nuevo**: el fósforo y el sodio son EXACTAMENTE
los del perro adulto sano (Tabla 13-3), que ya aplicamos a todo perro. Y el único
factor propio es la textura con sello VOHC, que es de pienso seco. **Cerrada.**

**PATRÓN QUE SE REPITE Y QUE CONVIENE VER JUNTO:** las tres tablas digestivas
altas (52-2, 54-2, 56-2) piden el MISMO núcleo de electrolitos — potasio
0,8-1,1 %, cloruro 0,5-1,3 %, **sodio 0,3-0,5 %** — y ese sodio va **hacia
arriba** (750-1250 mg/1000 kcal), no hacia abajo: es reposición de pérdidas por
vómito y diarrea. Es la dirección CONTRARIA a la del renal y la cardiopatía. Si
algún día se ofrecen, ojo con combinarlas.

## ⚠️⚠️ HALLAZGO GRANDE — LA TABLA 32-1 DA EL UMBRAL QUE FEDIAF NO DA

Esta tarde se escribió en `requisitos_condicionales.json` la regla
`zinc_y_cobre_cuando_el_calcio_esta_alto`, con este motivo textual: *«FEDIAF no
da NI UN FACTOR — ni cuánto sube el requisito ni **a partir de qué nivel de
calcio empieza**»*.

**SACN5 da el punto de partida.** Tabla 32-1, fila Zinc, literal:

> «Avoid excess calcium — **Higher levels of zinc are required in foods with
> calcium >1.5 % DM**»

A 4,0 kcal/g eso son **3750 mg de calcio por 1000 kcal**. O sea que la condición
que FEDIAF enuncia sin cuantificar («as the calcium level **approaches** the
stated nutritional maximum») tiene un umbral publicado, y encima por debajo del
máximo de FEDIAF (6250): la advertencia empieza al **60 % del techo**, no
pegada a él.

Lo que SIGUE sin existir es el **factor**: cuánto zinc hay que subir. Ninguna de
las dos fuentes lo dice. Así que la regla sigue siendo `documentado_sin_cifra`
para el requisito — pero **el umbral que decía que no existía sí existe**, y el
BLOQUE 69 que se escribió esta tarde vigila el 90 % de 6250 (5625) cuando el
número que la literatura señala es **3750**. Al aplicar hay que bajarlo, y con
su cita.

⚠️ Y esto es exactamente por qué Elena tiene razón con el método: esa regla se
escribió y se dejó cerrada («no hay umbral») cuatro horas antes de leer el
capítulo que lo trae.

### CAP. 32 — Dermatosis. Tabla 32-1 entera

| Factor | Perro adulto | Por 1000 kcal (a 4,0) |
|---|---|---|
| Proteína | 25-30 % MS | 62,5-75 g |
| Grasa | 10-15 % MS | 25-37,5 g |
| Fenilalanina + tirosina | >1,3 % MS | >3,25 g ✓ lo aplicamos |
| Digestibilidad MS | >80 % | — |
| **Linoleico** | **>1,0 % MS** | >2,5 g (FEDIAF ya pide 3,83: vamos por encima) |
| Zinc | 100-200 mg/kg MS | 25-50 mg ✓ aplicamos 25 |
| Cobre (techo) | <200 mg/kg MS | <50 mg (el techo legal, 7,0, es MUY inferior) |
| **Calcio (disparador)** | **>1,5 % MS pide más zinc** | **>3750 mg** |
| Crecimiento/lactancia | Proteína 30-35 %, grasa 15-30 % | 75-87,5 / 37,5-75 g |

Y un aviso que es de manejo y no de cifra: «**Zinc supplementation (Do not give
with food)**», con dosis: sulfato de zinc 10 mg/kg/día vía oral, zinc-metionina
2 mg/kg/día. Es dosis terapéutica, no concentración de la ración.

### CAPS. 28-31 — confirmaciones, sin nada nuevo
- **28 (hiperlipidemia)**: «Restrict dietary fat (**<12 % DM**)» ✓ nuestro 30, y
  «fiber levels of **at least 10 % DM** are recommended for dogs» ✓ nuestro 25.
- **29 (diabetes)**: fibra 7-18 % ✓ nuestro 17,5. El resto de ese capítulo es
  hipertiroidismo FELINO.
- **30 (cáncer)**: «omega-3 (**>5 % DM**)» ✓ 12,5, «arginine DM levels **>2 %**»
  ✓ 5,0, grasa 25-40 % ✓ 62,5, proteína perro 30-45 % ✓ 75, e hidratos «no more
  than 25 % DM», que no aplica a BARF.
- **31 (reacción adversa)**: proteína dermatológica **16-22 % MS** ✓ nuestro
  límite escrito de 55 (=22 %), lactosa «up to **1 g de lactosa/kg** de peso al
  día», digestibilidad proteica ≥87 %, y el criterio de respuesta: «watch for a
  marked (**at least 50 %**) decrease in the pruritus».

### CAPS. 38, 45, 48, 49, 51, 55, 61, 69 — sin nada que aplicar
Diagnóstico de urolitos (38), un caso clínico (45), fibra (48), introducción a
las enfermedades orales (49, 51), introducción al intestino delgado (55) y al
grueso (61), y el capítulo de fármacos y nutrientes (69). Ninguno trae una cifra
canina que el motor pueda aplicar; el 48 solo aporta un contexto útil sobre la
fibra: «little or no effect on gastric emptying, mineral absorption or colonic
microflora **unless fed in high concentrations (>20 % DM)**».

### CAP. 70 — animales exóticos. No aplicable
Hurones, conejos y cobayas. Nada de perro.

### CAP. 68 — Hepatobiliar. Confirmaciones y DOS cosas nuevas
Confirmado: cobre «<**5 mg/kg** DM» (=1,25) ✓, zinc «more than **200 mg/kg** DM»
(=50) ✓, vitamina E «at least **400 IU/kg** DM» para perro (=67,1) ✓, taurina
≥0,1 % (=250) ✓, cobre hepático normal «**400 µg/g dry weight** or less» ✓, y
**la grasa NO se restringe**: «There appears to be **no reason for routinely
restricting dietary fat** in dogs and cats with liver disease» — que es
justamente lo que hace el motor (no tiene tope de grasa en hepatopatía).

Nuevo, y no lo aplicamos:
- **Fibra: «Total dietary fiber levels should be between 3 and 8 % and be
  primarily soluble fiber»** = 7,5-20 g/1000 kcal.
- **Hidratos: «Providing at least 30 to 50 % of dietary calories in the form of
  easily digested, complex digestible carbohydrate»** — otra vez el problema
  estructural de una ración sin hidratos, como en reproducción.
- Y el aminograma: «hepatic disease can be improved by feeding a protein with an
  amino acid composition **high in BCAA and low in AAA**» (ramificados altos,
  aromáticos bajos). El catálogo tiene los doce aminoácidos, así que esto SÍ se
  podría medir — pero la fuente no da cifra de ratio.

### CAPS. 39-44, 46, 57, 58, 63-67 — todo cuadra, con dos matices

Los urolitos (39 urato, 40 oxalato, 41 fosfato cálcico, 42 cistina, 43 estruvita,
44 sílice) y los digestivos (57 EII, 58 PLE, 63 SII, 64 estreñimiento, 65
flatulencia, 66 IPE, 67 pancreatitis) confirman **fila a fila** los números que
ya aplica el motor. El 46 es de gato.

Dos matices que hay que mirar al aplicar:

1. **La vitamina D del oxalato y la del fosfato cálcico salen de dos frases
   distintas del mismo capítulo y no coinciden.** El texto del cap.40 dice
   «restrict vitamin D in foods to **between 500 to 1,500 IU/kg DM**» (= 125-375
   UI/1000 kcal = 3,125-9,375 µg) y también «Diets with vitamin D **between 250
   and 350 IU/Mcal** should suffice» (= 8,75 µg). El motor usa **8,75** en
   `oxalato` (la más estricta) y **9,375** en `urolitos_fosfato_calcico` (la del
   1500 UI/kg). No es un error — son dos frases de la fuente — pero conviene que
   quede escrito por qué dos patologías hermanas llevan cifras distintas.

2. **La pancreatitis del perro obeso es ≤10 % MS, no ≤15 %.** Literal: «Obese and
   hypertriglyceridemic patients recovering from pancreatitis should receive
   low-fat foods (**≤10** and ≤15 % DM for dog and cat foods, respectively)». Los
   ≤10 % del perro = **25 g/1000 kcal**, que es exactamente el
   `topes_por_1000kcal_si_ademas` que ya existe. ✓ Confirmado.

---

# LO QUE HAY QUE APLICAR (lista cerrada tras leer los 70 capítulos)

Ordenado por lo que cambia un menú, no por capítulo.

## 1. CIFRAS QUE EL MOTOR PUEDE APLICAR YA

**1.1 · El DHA mínimo en crecimiento y reproducción: 0,05 g/1000 kcal.**
Cuatro sitios (Tablas 15-5, 17-1 en sus dos columnas, 33-5, y el texto de los
caps. 15 y 33), misma cifra: **DHA ≥0,02 % MS**, derivada como «DHA needs to be
at least 40 % of the total DHA plus EPA». Hoy el motor pide EPA+DHA ≥0,125 g y
no pide reparto: un menú que lo cumpla todo con EPA sale verde. El catálogo
tiene la clave `dha`. **Es el candidato más sólido de toda la lectura.**

**1.2 · Bajar el umbral de calcio del BLOQUE 69 de 5625 a 3750 mg/1000 kcal.**
La Tabla 32-1 da el disparador que FEDIAF no da: «Higher levels of zinc are
required in foods with **calcium >1,5 % DM**». El bloque escrito esta tarde
vigila el 90 % del máximo de FEDIAF, que es una cifra inventada por mí; hay que
sustituirla por la de la fuente, con su cita.

**1.3 · Corregir el pendiente del frío.** Hoy `PENDIENTE_PRODUCTO.md` y `der.py`
dicen que FEDIAF «no da UNA cifra, da un rango de 1 a 9». **La Tabla 5-3 de
SACN5 sí las da**, por tipo de pelo y por salto de temperatura (pelo corto +95 %,
pelo largo +59,5 % de 25 °C a 7,6 °C; Labrador y beagle +25 % de 15 a 8,5 °C;
Gran Danés +22 % de verano a invierno). Sigue haciendo falta la pregunta en la
ficha — eso es producto — pero el texto que afirma que no hay cifra es falso y
hay que arreglarlo.

## 2. LAS 92 CONVERSIONES, COMO DATO Y NO COMO PROSA

`auditar_conversiones.py` ya está escrito y falla con las 92. Hay que rellenar
cada bloque `conversion` con el valor literal de la fuente, su unidad, la
densidad y la cita. **La densidad es 4,0 en todas**, y ahora está probado y no
supuesto:
- Es la única densidad que declara una tabla de SACN5 (13-3: «Concentrations
  presume an energy density of 4.0 kcal/g»);
- Es la que usa el cap.34 para convertir la glucosamina entre %MS y mg/kg de peso;
- Es la que hace cuadrar «20 % de la energía en hidratos = 23 % de MS» del cap.15;
- Y reproduce EXACTAMENTE las cifras del motor desde las filas de sus tablas.
La única excepción declarada distinta es el **3,8 kcal/g del cap.33 vía Caso
1-1** para el calcio del cachorro grande, que hay que tratar aparte.

## 3. AVISOS (texto, no cifras) QUE LA FUENTE DA Y LA APP NO DICE

- **Eclampsia por exceso de calcio en la gestante** (cap.15): «excessive calcium
  intake during pregnancy may … predispose the bitch to eclampsia during
  lactation» y «Calcium supplementation is **not** recommended during gestation
  or lactation».
- **Agua con menos de 150 ppm de sodio** en insuficiencia cardíaca avanzada (cap.36).
- **L-carnitina terapéutica en cardiopatía**: 2 g tres veces al día en perros de
  ~40 kg (cap.36).
- **Potasio con diuréticos** (cap.36).
- **El zinc terapéutico no se da con la comida** (cap.32).
- **Cuándo empieza la dieta renal**: estadio 2, o creatinina >2 mg/dl (cap.37).
- **El 10 % de los extras** (caps. 10, 18 y 19, tres veces): por encima del 10 %
  de la materia seca diaria, lo de fuera deja de ser inocuo.

## 4. DATOS DEL CATÁLOGO QUE HAY QUE MIRAR (no rellena el asistente)

- **Óxido de hierro: hierro que se analiza y no se absorbe** (cap.6).
- **Óxido de cobre: disponibilidad cero, y AAFCO pide dejar de usarlo** (cap.6).
- **Hígado de cerdo: cobre con disponibilidad esencialmente cero** (cap.6).
  ⚠️ Esto último es una FICHA, no una nota de fabricación. Comprobar si existe.
- La tabla de **% de mineral elemental de cada sal** del cap.6, hermana de la
  VII-14 de FEDIAF.

## 5. DECISIONES DE ELENA (con los números ya delante)

- **¿Se pregunta dónde vive el perro?** Si sí, la Tabla 5-3 da las cifras.
- **Las nueve tablas de recomendación canina sin patología en el motor**: siete
  digestivas/esofágicas con sus números arriba; la 53-2 (vólvulo) y la 47-4
  (periodontal) están CERRADAS y no hace falta nada.
- **La densidad de la Tabla 27-4** (obesidad), única que propone ≤3,4 kcal/g para
  el propio alimento: si sus filas se leyeran a esa densidad, sus cifras subirían
  un 18 %. La fuente no lo dice; se deja en 4,0 y se apunta.
---

## COMPROBACIONES CRUZADAS HECHAS DURANTE LA LECTURA (sin tocar nada)

**1. El suelo de proteína de la perra gestante, 125 g/1000 kcal, queda
CORROBORADO por una fuente distinta y por otro camino.** Se aplicó el 8 de
septiembre desde FEDIAF («If carbohydrate is absent … the protein requirement is
much higher, and may be double»). SACN5 cap.15 llega al mismo sitio con un
experimento: «In a study in which a food that had about **50 % DM protein** was
fed, no problems with hypoglycemia or ketosis resulted and puppies were born
healthy (Blaza et al, 1989)». **50 % de MS a 4,0 kcal/g son exactamente 125
g/1000 kcal.** Dos fuentes, dos razonamientos, el mismo número.

**2. La vitamina E del perro de trabajo (83,9 mg/1000 kcal) cuadra con la Tabla
18-9 leída entera**: «≥500 IU vitamin E/kg food (DM)» en las cuatro columnas de
actividad. 500 ÷ 4 = 125 UI/1000 kcal, × 0,671 mg/UI = 83,9. ✓

**3. El hígado de cerdo NO está en el catálogo — ni ninguna ficha de cerdo.**
Comprobado: las seis fichas de hígado son de vaca, conejo, pollo, cordero, pavo
y pato. Así que el hallazgo del cap.6 («copper availability was essentially zero
from copper oxide **and pork liver**») no nos afecta hoy. Y la otra mitad de esa
frase nos favorece: «**Beef, sheep and turkey liver** … were highly available
sources of copper» — vaca, cordero y pavo, tres de nuestras seis. Queda escrito
para el día que alguien proponga añadir hígado de cerdo: su cobre no cuenta.

