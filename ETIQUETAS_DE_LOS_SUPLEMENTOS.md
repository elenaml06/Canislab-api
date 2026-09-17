# Las etiquetas de los suplementos, una a una

*(15 de septiembre de 2026.)* Elena:

> «me gustaría que revisaras todos los suplementos también, todas las etiquetas,
> ¿vale? Igual que hemos hecho con el catálogo, que lo hagas con las etiquetas.
> Eh, menos el **Pets Purest**, que te la pasé yo. Todos los demás tienes que
> comprobar las etiquetas, ¿vale?»

Y al hacerlo, un aviso suyo que resultó ser la mitad del trabajo:

> «Ten en cuenta las unidades eh! Todas tienen que estar en las mismas unidades
> que lo que usamos nosotros»

**62 celdas cambiadas en 12 fichas.** Este documento dice de dónde sale cada
una. Los números viven en `alimentos_v3_final.json` con su procedencia en
`composicion_fuente`; esto es su lectura, no una segunda copia — si discrepan,
manda el JSON. Lo vigila el **BLOQUE 116**.

---

## No es una lista de despistes: es UN patrón, y ya estaba escrito en el repo

**La etiqueta declara la SAL o el ÉSTER de la vitamina, y el catálogo anotó ese
número como si fuera la vitamina.**

Es exactamente la trampa que el repo ya tenía escrita para los minerales
—`sacn5_fuentes_de_minerales.json`, «óxido de zinc 100 mg son 72 mg de zinc»— y
para la que **ya existía la tabla de conversión auditada contra el PDF**:
`fediaf_conversiones_vitaminas.json`, la Tabla VII-14 de FEDIAF, transcrita el 9
de septiembre y rehecha por `auditar_transcripcion_fediaf.py`.

O sea: la fuente estaba, la conversión estaba escrita, la tabla estaba auditada,
y **nadie la había aplicado a los suplementos**. Es la lección de
`auditar_conversiones.py` en su forma más pura — *una frase no se ejecuta* —,
solo que aquí ni siquiera era una frase: era una tabla sin nadie que la usara.

⚠️ Y `DATOS_QUE_FALTAN.md` decía que «ninguna ficha dice en qué forma química
viene cada vitamina del grupo B». **Las etiquetas SÍ lo dicen**, y la de astoral
lo dice con el **número E** de cada aditivo: 3a700, 3a821, 3a831, 3a841.

---

## Las cuatro formas que tiene un número de parecer bueno y no serlo

### 1 · El peso de la SAL, anotado como si fuera la vitamina

| Forma de la etiqueta | Factor (FEDIAF VII-14) | Fichas |
|---|---|---|
| Cloruro de colina | **×0,75** (ion colina) | 7 |
| D-pantotenato cálcico | **×0,92** | 7 |
| Clorhidrato de piridoxina | **×0,82** | 3 |
| Mononitrato de tiamina | **×0,81** | 2 |

Ejemplo: «Cloruro di colina 55.000 mg/kg» del V-INTEGRA Adulto son **4.125 mg de
colina** por 100 g, no 5.500.

### 2 · La unidad de la celda: el folato, mil veces por debajo

El folato va en **µg** (`UNIDADES.md`) y las etiquetas lo dan en **mg/kg**.

| Ficha | Etiqueta | Decía | Es |
|---|---|---|---|
| napfcheck Novomineral proLEBER | «Folsäure: 20 mg» /kg | 2 | **2000 µg** |
| V-INTEGRA Perro Adulto | «Acido folico 10 mg» /kg | 1 | **1000 µg** |
| V-INTEGRA Senior | «acido folico 10 mg» /kg | 1,0 | **1000 µg** |
| V-INTEGRA Renal | «Acido folico 9,8 mg» /kg | 0,98 | **980 µg** |
| V-INTEGRA Epato | «acido folico 9,8 mg» /kg | 1,6 | **980 µg** |
| V-INTEGRA Cachorro | «Acido folico 6,8 mg» /kg | 0,68 | **680 µg** |

### 3 · La ACTIVIDAD frente al PESO: la vitamina E

La celda del catálogo está en **mg de d-α-tocoferol**, y eso no es una elección
de estilo: el mínimo que aplica el motor (6,968 mg/1000 kcal en adulto) es la
cifra que FEDIAF publica **en UI** (10,40) dividida por 1,49. Está escrito en la
`nota_auditoria` de `Vitamina_E` de `requerimientos_v2_final.json`.

| Ficha | Etiqueta | Decía | Es |
|---|---|---|---|
| Homemadekun | «Vitamina E – 6 250 UI/kg» | 625 | **419,5 mg** |
| astoral MultiVital BARF | «rrr-alpha-Tocopherylacetat (3a700) 5000 mg/kg» | 500 | **456,4 mg** |
| NEKTON Dog Easy-BARF | «2.000 mg Vitamin E» /kg, **sin forma química** | 200 | **134,2 mg** ⚠️ |
| napfcheck proLEBER | «Vitamin E natürlichen Ursprungs: 6.000 mg» /kg | 600 | **600 mg** ✅ |

⚠️ **El de NEKTON lleva un SUPUESTO y va escrito como tal**: la etiqueta no dice
la forma, así que se toma el aditivo autorizado que se declara así (3a700,
all-rac-α-tocoferil acetato, 1 mg = 1 UI). Si el fabricante confirma otra forma,
la cifra cambia.

✅ **Y el de napfcheck NO se toca**, que es la otra mitad de la regla: «natürlichen
Ursprungs» es el **peso** del d-α-tocoferol natural, o sea ya nuestra unidad.
Convertirlo habría sido el mismo error al revés.

### 4 · La que más pesa, y no es de vitaminas: **la energía a cero**

**`AniForte Beef Blood Powder` declaraba 92 g de proteína y 0 kcal.**

La energía es el **DIVISOR** de los 43 requisitos, que van todos por 1000 kcal.
Una ficha con 92 % de proteína y 0 kcal le metía al motor proteína en el
numerador y nada en el denominador: cualquier menú que la llevara salía con más
proteína por 1000 kcal de la que de verdad tiene.

Ocho fichas publican su proteína y su grasa brutas y tenían la energía a 0. Se
rehace con **FEDIAF §7.2.2.2 b)** (`kcal ME = 4 × %proteína + 9 × %grasa + 4 ×
%NFE`):

| Ficha | kcal/100 g |
|---|---|
| AniForte Beef Blood Powder | **371,6** |
| astoral MultiVital BARF | 129,3 |
| Homemadekun | 90,8 |
| Nutratop Vitamínico-Mineral 7:1 | 78,8 |
| V-INTEGRA Epato | 51,4 |
| V-INTEGRA Senior · Renal | 51,0 |
| V-INTEGRA Perro Adulto | 46,6 |
| NEKTON Dog Easy-BARF | 39,6 |
| V-INTEGRA Cachorro | 38,6 |

⚠️ **El NFE se cuenta como 0 y va declarado**: estas etiquetas no publican la
humedad de la que habría que despejarlo. Contar menos energía aprieta las
concentraciones, que es el lado del que **no** se entrega un menú de más.

Las cuatro que se quedan a 0 lo están con motivo: las dos cáscaras de huevo y el
yoduro potásico no tienen proteína ni grasa, y ni `napfcheck` ni el alga las
publican.

---

## La vitamina E de las V-INTEGRA era un CONSERVANTE

Las cinco fichas de la gama llevaban vitamina E y **ninguna de las cinco
etiquetas la declara como aditivo NUTRICIONAL**. Lo que declaran es una línea de
**aditivos tecnológicos**:

> «Antiossidanti 2.772,2 mg (di cui estratti di origine naturale ricchi in
> tocoferolo 2.380 mg)»

Y el número de la ficha era ese partido por diez, exacto, en las cinco: Adulto
2.380 → 238 · Cachorro 2.206 → 220,6 · Senior 6.700 → 670 · Epato 6.000 → 600 ·
Renal 6.700 → 670. Es el conservante del propio polvo, no un aporte.

⚠️ **Importaba justo ahora**: el suelo de vitamina E del perro sano se acababa de
encender. Medido antes de tocarlo, **entre el 14 % y el 82 %** de la vitamina E
de un menú salía de ese número. Con él a cero, los menús de adulto, sénior y toy
llegan a **114-167 mg/1000 kcal** contra un suelo de 67,1, porque el solver se va
a las dos fichas de vitamina E suelta que entraron ese mismo día. **El suelo no
dependía del conservante.**

---

## Lo que las etiquetas traían y la ficha tenía como hueco

Seis fichas declaran **taurina** —hasta 40.000 mg/kg— y una además **L-carnitina**,
y las tenían en `sin_dato`. No son requisitos de FEDIAF para el perro, pero **sí
son el suelo de `dcm_taurina_respondedora`** (taurina ≥ 250 y L-carnitina ≥ 50
mg/1000 kcal): un hueco ahí puede dejar sin menú a esa patología teniendo la
fuente dentro del bote.

| Ficha | Taurina | L-carnitina |
|---|---|---|
| V-INTEGRA Senior · Epato · Renal | 4000 | — |
| V-INTEGRA Cachorro | 3996 | — |
| napfcheck proLEBER | 3000 | **3500** |
| V-INTEGRA Perro Adulto | 2500 | — |

Y la **fibra bruta**, que tres etiquetas publican y ninguna ficha tenía:
Homemadekun 1,44 % · astoral 1,3 % · NEKTON 4,6 % · Nutratop 4,20 % · alga 8,0 %.

---

## El yodo del alga no tiene UN número, y eso es el hallazgo

`AniForte Seaweed Meal` es la única fuente de yodo natural del catálogo, y el
yodo es uno de los **cinco topes crónicos** (regla 2).

| Dónde | Yodo declarado |
|---|---|
| fuetternundfit.de | 339 mg/kg |
| **aniforte.de, en alemán** | **600 mg/kg** |
| fressnapf.de | 760 mg/kg *(lo que llevaba la ficha)* |
| **aniforte.de, en inglés** | **790 mg/kg** |

**Un factor 2,3 entre la más baja y la más alta, y dos de ellas son la página del
propio fabricante.** No es un descuido de nadie: es lo que el repo ya tiene
escrito en la ficha del yoduro potásico — el yodo del *Ascophyllum* varía hasta
**100 veces** entre lotes (Aakre et al. 2021, *Food & Nutrition Research* 65:7584).

Se toma **la más alta, 790 mg/kg**, y es una decisión con dirección: sobreestimar
lo que lleva el alga hace que el solver meta **menos gramos**, que es el lado
seguro contra el techo. Es además coherente con el margen del 50 % que
`seguridad.tope_de_yodo` ya deja cuando el menú lleva kelp, puesto el 14 de
septiembre por esto mismo.

⚠️ **Y sus cuatro minerales se van a hueco.** La ficha llevaba calcio 1,2 %,
magnesio 0,8 %, sodio 3,6 % y cloruro 5,54 %, de una hoja cuya **ceniza bruta es
19,47 %**. La etiqueta del fabricante —en los dos idiomas— dice «Rohasche 11,12 %,
Rohfaser 8,0 %, Restfeuchte 12,33 %» y **no publica ninguno de los tres**: una
ceniza del 11,12 % no puede contener el 10,1 % de minerales que sumaban esas
cuatro cifras. Las dos hojas no describen el mismo producto, y manda la del
fabricante (mandato 5). Se dejan en hueco y no en cero, por lo de siempre. Medido
antes de quitarlas: a la dosis de la etiqueta aportaban **72 mg de sodio al día**
en un perro de 20 kg, o sea nada.

---

## Tres cifras del V-INTEGRA Epato que su propia etiqueta contradice

No una: **tres**. Calcio 17.300 contra «calcio 16,1 %», proteína 4,2 contra
«proteina grezza 7,0 %» y grasa 0,2 contra «oli e grassi grezzi 2,6 %».

Que la ficha **sí** es de ese producto lo prueban las otras ocho cifras de esas
mismas dos líneas, que coinciden exactas: magnesio 1,3 %, sodio 1,2 %, fósforo
6,9 %, la **ausencia de potasio** (que solo le pasa al Epato de toda la gama),
cobre 30 mg/kg, zinc 5.550 mg/kg, yodo 45 mg/kg y B12 1,50 mg/kg. Son cifras mal
copiadas, no otra formulación. Tres fuentes dicen lo mismo: shop.vetekipp.it (el
fabricante), ziliottigroup.it y farmaciacavalieri.it.

---

## Una contradicción interna en las dos levaduras

Las dos fichas decían **a la vez** dos cosas incompatibles: la nota afirmaba «NO
lleva B12 (solo si está fortificada)» y el mismo párrafo daba «B12 0,34» de
CIQUAL 11009, **con la clave `vitB12` metida además en `sin_dato`**. O sea: un
valor puesto, usado por el solver, y declarado hueco al mismo tiempo —
`datos_incompletos` lo contaba como que falta mientras `valor_nutriente()`
devolvía 0,34.

Manda CIQUAL 11009, que es de donde sale **todo** el bloque B de esas fichas: se
queda el 0,34 y sale de `sin_dato`. La frase que sobraba era la de «no lleva».

⚠️ Y hay que saber lo que ese bloque B **no** es: no sale de la etiqueta de GRAU
ni de la de PAWS & PATCH —ninguna de las dos publica vitaminas—, sale de CIQUAL,
que es por lo que las dos fichas llevan las mismas siete cifras. Lo que sí es de
cada etiqueta son los minerales, y por eso difieren.

---

## Las dos levaduras y el polvo de sangre: lo que la etiqueta publicaba y nadie había leído

Las tres tenían la **energía heredada** —un número sin derivación— y huecos que su
propia etiqueta cierra.

| Ficha | Lo que la etiqueta dice y la ficha no tenía | Energía |
|---|---|---|
| **GRAU Levadura de cerveza** | «Fettgehalt 2,7 %» · «Rohfaser 1,0 %» · «Feuchte 7,0 %» (+ «Rohasche 8,0 %», «Stärke 6,2 %») | 350 heredado → **349,5 rehecho**: el NFE se despeja (35,3) y sale casi el mismo número, que queda **confirmado en vez de heredado** |
| **PAWS & PATCH Levadura de cerveza** | «Rohfett 3,3 %» | 350 heredado → **330,1** |
| **AniForte Beef Blood Powder** | «Rohfaser 0,5 %» · «Restfeuchte 6 %» | **371,6**, y ahora sin estimar nada: con la humedad puesta el NFE sale **negativo** (−2,9), o sea 0 |

⚠️ **Dos cifras de la PAWS & PATCH no son cifras, son COTAS**, y se tratan como la
marca `< X` de CIQUAL que `UNIDADES.md` ya describe:

- «Rohfaser **< 0,3 %**» → **hueco declarado**. Copiar el 1,0 % de la GRAU sería
  describir este producto con la medida de otra marca. En hueco, el motor cuenta 0
  contra un mínimo y el percentil 90 de su familia contra un máximo: conservador
  en las dos direcciones.
- «Feuchtigkeit **<14 %**» → se toma el extremo **alto**, porque es el que deja
  **menos materia seca**, y menos materia seca **aprieta** los siete techos legales
  de la UE, que van sobre ella. Mismo argumento que la cota por composición de los
  cinco aceites.

✅ **Y el polvo de sangre CONFIRMA una decisión vieja en vez de desdecirla.** El 27 de
agosto se vaciaron su cobre y su cinc porque los 3,3 g/kg que declaraba no cabían en
su propio presupuesto de cenizas. La etiqueta releída ahora dice «Rohasche 4 %»:
exactamente el presupuesto con el que no cuadran.

Con esto los huecos de humedad del catálogo pasan de **18 a 9**.

---

## Lo que se miró y está BIEN, que también cuenta

- **Los tres aceites de salmón**: su `linoleico` (14 a 16,1 g) parece alto al
  lado del salmón de USDA, y **no es un fallo**: cada ficha lleva escrito desde
  el 27 de agosto que ahí va el **omega-6 total** de la etiqueta, con el
  argumento de que en el n-6 de un aceite de pescado el linoleico domina de
  verdad (el araquidónico es un 0,5-1 %) — mientras que en el n-3 no, que es por
  lo que el `linolenico` sí se vació. La decisión está tomada, escrita y es
  coherente en las cuatro fichas de aceite.
- **Los minerales de todas las fichas revisadas** cuadran celda a celda con su
  etiqueta: hierro, cobre, zinc, manganeso, yodo y selenio de las cinco
  V-INTEGRA, de napfcheck, de astoral, de NEKTON y de Homemadekun.
- **Las vitaminas A y D**, convertidas de UI con los factores de la Tabla VII-14
  (0,3 µg/UI y 0,025 µg/UI): las nueve fichas que las declaran cuadran.
- **El Pets Purest no se ha tocado**, por petición expresa.

---

## Lo que queda abierto

| | Qué falta | Por qué no lo cierro yo |
|---|---|---|
| **NEKTON, vitamina E** | Que el fabricante diga la forma química | Hoy hay un supuesto escrito. Si dice «d-α-tocoferol», la cifra sube de 134,2 a 200 |
| **Aminogramas de los suplementos** | Ninguna etiqueta los publica | `DATOS_QUE_FALTAN.md`: no los rellena el asistente |
| **Formas químicas del grupo B donde la etiqueta calla** | NEKTON B1, Homemadekun B1/B6, V-INTEGRA B1/B2/B6 | Inventar la forma es inventar la cifra |
| **`napfcheck` y el alga: proteína, grasa y energía** | Sus etiquetas no las publican | Se quedan a 0 declarado |
| **`NaturGreen Psyllium Bio`** | Su etiqueta no se ha podido abrir (la página del fabricante da 404) | Es la única de las 25 que queda sin releer. Su fibra y su dosis ya venían con procedencia escrita |
| **`V-INTEGRA Renal Met`** | Es el único producto de España que arregla el hueco de metionina que señaló Cris, y lleva **DL**-metionina donde ella pidió **L** | **P-43**: es clínica (Cris) y de producto (Elena) |
