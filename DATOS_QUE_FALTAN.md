# Datos que faltan en el catálogo

> ⚠️ **LIMPIADO EL 8 DE SEPTIEMBRE, y hay que saber por qué se ensució.**
> Este archivo dice de sí mismo que lo genera `auditar_catalogo.py`, y **no
> es verdad: ningún código lo escribe.** Se generó una vez y desde entonces
> se mantiene a mano, así que el 27 de agosto -- cuando cinco suplementos y
> los testículos de cordero salieron del catálogo por no cuadrar sus datos
> -- sus secciones se quedaron aquí pidiendo valores de alimentos que ya no
> existen. Eran seis: `Testículos de cordero`, `Sonrisa de Diez Kelp`, `GRAU Harina de Hueso`, `LUPO NATURAL BARF Huesos en polvo`, `Pets Purest Aceite de Salmón`, `Brit Care Aceite de Salmón`.
>
> Pedir datos de un alimento retirado no es solo ruido: manda a una persona
> a buscar en BEDCA o en la ficha del fabricante un número que, aunque lo
> encuentre, no se puede usar. El de **Pets Purest Aceite de Salmón** era el
> peor de los seis, porque salió justo por eso -- sus porcentajes de EPA/DHA
> solo aparecen en fichas de marketing del fabricante, y era el más denso de
> los cinco aceites, así que era el que el solver prefería.
>
> Comprobado el mismo día que de esos seis **no queda ni una referencia** en
> los cuatro archivos de datos (`alimentos_v3_final.json`,
> `catalogo_menus.json`, `requerimientos_v2_final.json`, `der_casos.json`).
> Lo único que los nombra es el BLOQUE 30 de `pruebas_completas.py`, y ahí
> es a propósito: vigila que no vuelvan.



## Peso del cacito de los suplementos en polvo

**Añadido el 24 de agosto.** Midiendo las cantidades no medibles salieron
dosis como **0,15 g de AniForte Seaweed Meal** o **0,60 g de V-INTEGRA**.
Nadie pesa eso, y a estos NO se les puede poner un suelo en el motor:
obligarles a llegar a un gramo sería obligar a dar de más de un
suplemento, que es justo lo que no se puede hacer.

Se arregla con un dato que no tenemos: **cuánto pesa el cacito (o el
comprimido) de cada producto**. Con eso, la app puede decir «un cuarto de
cacito» en vez de «0,15 g», igual que ya hace con los comprimidos
(`formatearComprimidos` en `App.jsx`).

Es un dato de cada fabricante: viene en la etiqueta del bote. No lo busca
Code — se rellena cuando lo tengáis, y la línea aparece sola.

| Producto | Peso del cacito |
|---|---|
| AniForte Seaweed Meal | |
| V-INTEGRA Perro Adulto | |
| Homemadekun (multivitamínico completo) | |
| napfcheck Novomineral proLEBER | |
| NEKTON Dog Easy-BARF (multivitamínico) | |
| Cáscara de huevo PAWS & PATCH | |

Los huecos los ENCUENTRA `auditar_catalogo.py`, pero **este archivo no lo
escribe ningún código**: se mantiene a mano, y por eso pudo quedarse
pidiendo datos de seis alimentos retirados (ver el aviso de arriba). Hoy
son **53 alimentos y 330 valores**. **Esto no lo rellena el asistente.**

Cada valor tiene que venir de una fuente verificada por una persona:

| Para qué | Fuente |
|---|---|
| Alimentos (España) | **BEDCA** — bedca.net |
| Alimentos (Francia, más completa en algunos) | **CIQUAL** — ciqual.anses.fr |
| Alimentos (referencia internacional) | **USDA FoodData Central** — fdc.nal.usda.gov |
| Huesos carnosos | **Köber et al. 2017**, el único estudio con datos reales de hueso en BARF |
| Requisitos por patología | Guías clínicas veterinarias (IRIS, ACVIM, Merck) |

Todos los valores van **por 100 g de alimento tal cual se da** (fresco, no
materia seca), en la unidad que indica cada columna. La energía tiene que
cuadrar con los macros: si no, es que la fuente estaba en materia seca.

**Antes de rellenar nada, mira `UNIDADES.md`**: están las unidades de los
29 nutrientes y las cuatro trampas que se cuelan siempre. En concreto, EPA
y DHA van en gramos aunque las tablas los den en miligramos, y `linoleico`
(omega-6) y `linolenico` (omega-3) se diferencian en una letra y son cosas
opuestas.

---

## Timo de ternera  ·  _Vísceras_

**Recortado el 7 de septiembre**: comprobado contra `alimentos_v3_final.json`,
esta ficha ya trae 23 de los 28 nutrientes de esta lista (incluida la
fibra, en 0 — un timo no tiene fibra de verdad, no es un hueco). Solo
quedan estos 5, que la propia ficha marca `sin_dato`:

| Nutriente | Unidad | Valor |
|---|---|---|
| cloruro | mg | |
| colina | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |

## NaturGreen Psyllium Bio  ·  _Fibra_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| calcio | mg | |
| cloruro | mg | |
| cobre | mg | |
| colina | mg | |
| folato | µg | |
| fosforo | mg | |
| hierro | mg | |
| magnesio | mg | |
| manganeso | mg | |
| niacina | mg | |
| potasio | mg | |
| riboflavina | mg | |
| selenio | µg | |
| sodio | mg | |
| tiamina | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |
| zinc | mg | |

## Cáscara de huevo PAWS & PATCH  ·  _Calcio_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| cloruro | mg | |
| cobre | mg | |
| colina | mg | |
| folato | µg | |
| hierro | mg | |
| magnesio | mg | |
| manganeso | mg | |
| niacina | mg | |
| potasio | mg | |
| proteina | g | |
| riboflavina | mg | |
| selenio | µg | |
| sodio | mg | |
| tiamina | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |
| zinc | mg | |

## Cáscara de huevo casera (en polvo)  ·  _Calcio_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| cloruro | mg | |
| cobre | mg | |
| colina | mg | |
| folato | µg | |
| hierro | mg | |
| magnesio | mg | |
| manganeso | mg | |
| niacina | mg | |
| potasio | mg | |
| proteina | g | |
| riboflavina | mg | |
| selenio | µg | |
| sodio | mg | |
| tiamina | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |
| zinc | mg | |

## Nutratop Vitamínico-Mineral 7:1  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| calcio | mg | |
| fosforo | mg | |
| sodio | mg | |
| cloruro | mg | |
| potasio | mg | |
| magnesio | mg | |
| hierro | mg | |
| cobre | mg | |
| zinc | mg | |
| manganeso | mg | |
| selenio | µg | |
| vitA | µg | |
| vitD | µg | |
| vitE | mg | |
| tiamina | mg | |
| riboflavina | mg | |
| vitB6 | mg | |
| vitB12 | µg | |
| niacina | mg | |
| acidoPantotenico | mg | |
| folato | µg | |
| colina | mg | |

## Cerebro de vaca  ·  _Vísceras_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| araquidonico | mg | |
| cloruro | mg | |
| cobre | mg | |
| colina | mg | |
| dha | g | |
| epa | g | |
| fibra | g | |
| folato | µg | |
| fosforo | mg | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |
| magnesio | mg | |
| manganeso | mg | |
| niacina | mg | |
| riboflavina | mg | |
| tiamina | mg | |
| vitA | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |

## Bazo de cordero  ·  _Vísceras_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| araquidonico | mg | |
| calcio | mg | |
| cloruro | mg | |
| colina | mg | |
| dha | g | |
| epa | g | |
| fibra | g | |
| folato | µg | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |
| manganeso | mg | |
| niacina | mg | |
| riboflavina | mg | |
| tiamina | mg | |
| vitA | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |

## AniForte Seaweed Meal  ·  _Yodo_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| cobre | mg | |
| colina | mg | |
| folato | µg | |
| fosforo | mg | |
| hierro | mg | |
| manganeso | mg | |
| niacina | mg | |
| potasio | mg | |
| proteina | g | |
| riboflavina | mg | |
| selenio | µg | |
| tiamina | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| zinc | mg | |

## Páncreas de vaca  ·  _Vísceras_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| cloruro | mg | |
| colina | mg | |
| dha | g | |
| epa | g | |
| fibra | g | |
| folato | µg | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |
| selenio | µg | |
| vitA | µg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |
| zinc | mg | |

## AniForte Beef Blood Powder  ·  _Hierro_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| colina | mg | |
| folato | µg | |
| manganeso | mg | |
| niacina | mg | |
| riboflavina | mg | |
| selenio | µg | |
| tiamina | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |

## Bazo de vaca  ·  _Vísceras_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| cloruro | mg | |
| colina | mg | |
| dha | g | |
| epa | g | |
| fibra | g | |
| folato | µg | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |
| vitA | µg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |

## PAWS & PATCH Levadura de cerveza  ·  _Vitamina B_

| Nutriente | Unidad | Valor |
|---|---|---|
| calcio | mg | |
| cloruro | mg | |
| colina | mg | |
| fosforo | mg | |
| magnesio | mg | |
| manganeso | mg | |
| sodio | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |

## GRAU Levadura de cerveza  ·  _Vitamina B_

| Nutriente | Unidad | Valor |
|---|---|---|
| colina | mg | |
| manganeso | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |

## Aceite de Salmón Natural Greatness  ·  _Omega-3_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| grasa | g | |
| linoleico (omega-6, C18:2) | g | |
| vitA | µg | |
| vitD | µg | |
| vitE | mg | |

## astoral MultiVital BARF  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| colina | mg | |
| folato | µg | |
| niacina | mg | |
| selenio | µg | |
| vitA | µg | |
| vitD | µg | |

## Sal común (cloruro sódico)  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |
| hierro | mg | |
| manganeso | mg | |
| selenio | µg | |
| zinc | mg | |
| yodo | µg | |

## Oleum Canis Aceite de Salmón  ·  _Omega-3_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| grasa | g | |
| vitA | µg | |
| vitD | µg | |
| vitE | mg | |

## AniForte Aceite de Salmón  ·  _Omega-3_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| grasa | g | |
| vitA | µg | |
| vitD | µg | |
| vitE | mg | |

## Ternera solomillo sin grasa  ·  _Carne muscular_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| dha | g | |
| epa | g | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |

## Ternera con grasa  ·  _Carne muscular_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| dha | g | |
| epa | g | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |

## Lomo de ternera con grasa  ·  _Carne muscular_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| dha | g | |
| epa | g | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |

## Pecho de ternera con hueso  ·  _Hueso carnoso_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| dha | g | |
| epa | g | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |

## Cuello de ternera  ·  _Hueso carnoso_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| dha | g | |
| epa | g | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |

## Laringe de vacuno  ·  _Hueso carnoso_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| dha | g | |
| epa | g | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |

## NEKTON Dog Easy-BARF (multivitamínico)  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| cloruro | mg | |
| magnesio | mg | |
| potasio | mg | |
| selenio | µg | |

## Homemadekun (multivitamínico completo)  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| cloruro | mg | |
| magnesio | mg | |

## V-INTEGRA Epato  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| cloruro | mg | |
| potasio | mg | |

## Pollo pechuga con piel  ·  _Carne muscular_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Calabaza  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Manzana  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Pera  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Fresa  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Sandía  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Melón  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Pollo con piel (sin hueso)  ·  _Carne muscular_

| Nutriente | Unidad | Valor |
|---|---|---|
| calcio | mg | |

## Yogur griego  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |

## Huevo de codorniz  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |
| araquidonico | mg | |

## Huevo de gallina entero  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |
| araquidonico | mg | |

## Huevo de pato  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |
| araquidonico | mg | |

## Huevo de pato entero  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |
| araquidonico | mg | |

## Semilla de lino  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |

## Pipa de calabaza  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |

## Pipa de girasol  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |

## Semilla de sésamo  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| cobre | mg | |

## Canónigos  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Mandarina  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## Piña  ·  _Verduras y frutas_

| Nutriente | Unidad | Valor |
|---|---|---|
| selenio | µg | |

## V-INTEGRA Perro Adulto  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| cloruro | mg | |

## V-INTEGRA Cachorro  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| cloruro | mg | |

## V-INTEGRA Senior  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| cloruro | mg | |

## V-INTEGRA Renal  ·  _Multivitamínico_

| Nutriente | Unidad | Valor |
|---|---|---|
| cloruro | mg | |

## Huevo yema  ·  _Extras_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |

## Hígado de cordero  ·  _Hígado_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |

---

## Los cuatro del cociente (28 de agosto)

**No son huecos: son valores declarados que hay que comprobar en su fuente.**
Los saca la comprobación de nivel 2 —mirar la columna en vez de la fila— que se
añadió ese día a `auditar_catalogo.py`. Ninguna comprobación anterior los veía.

| alimento | qué sale | qué habría que mirar |
|---|---|---|
| **Pulmón de cordero** | Leu/Ile **2,537**, isoleucina al 3,16 % de la proteína | Es la firma exacta del pavo contaminado del USDA (Leu/Ile 2,42-2,52 cuando el resto del catálogo va de 1,16 a 1,98). **El más sospechoso de los cuatro.** De dónde salió su aminograma |
| **Calamar** | valina = isoleucina, 0,680 | Los tres cefalópodos tienen Val = Ile **exacto**. Comprobado que **NO** son el mismo perfil reescalado —sus AA/proteína difieren— así que puede ser real: en cefalópodos la valina se parece mucho a la isoleucina. Hace falta ver la fuente de cada uno |
| **Pulpo** | valina = isoleucina, 0,651 | ídem |
| **Sepia** | valina = isoleucina, 0,709 | ídem |

**Por qué esta comprobación pilla lo que las otras no.** Todas las demás
preguntan «¿este número es posible?» dentro de una fila, y eso caza el valor
**imposible**. No caza el valor **imputado**, porque quien lo imputa lo hace con
proporciones internamente coherentes: el pavo del USDA cuadraba consigo mismo
perfectamente y solo fallaba contra el resto del mundo. Un cociente entre dos
aminoácidos de la misma fila, en cambio, **no se mueve al reescalar por la
proteína del destino**, así que sobrevive a la transferencia y la delata.

---

## La vitamina A: hace falta saber qué son esos microgramos, ficha por ficha

**Añadido el 9 de septiembre de 2026, leyendo el capítulo 8 del NRC entero.**

El campo `vitA` de las 163 fichas está en microgramos, pero **no está escrito de
qué**: puede ser retinol preformado, equivalentes de retinol a 6:1, o RAE a
12:1. Y contrastado con USDA, **el catálogo mezcla al menos dos convenios**:

| Alimento | Nuestra ficha | USDA RAE (12:1) | β-caroteno ÷ 6 | Parece |
|---|---|---|---|---|
| Zanahoria | 1.346 | 835 | 1.381 | equivalentes 6:1 |
| Boniato | 667 | 709 | 1.418 | RAE |
| Rúcula | 596 | 119 | 237 | **ninguno de los dos** |

**Por qué esto es un dato que falta y no un cálculo que se pueda hacer.** El NRC
dice literalmente que para el perro **el factor de conversión del β-caroteno no
está definido**, así que no se puede recalcular una cosa desde la otra. Hay que
ir a la fuente y sacar los dos números por separado, igual que se hace con `epa`
y `dha`.

**Lo que hay que conseguir**, para las **11 fichas vegetales con vitamina A por
encima de 100 µg/100 g** (zanahoria, grelo, boniato, rúcula, espinaca,
canónigos, albahaca, tomate en puré, acelga, col rizada, mandarina) y para las
fichas animales que aportan retinol (hígados, riñones, huevo, mantequilla,
aceites de hígado, suplementos):

- `vitA_retinol` — µg de retinol preformado por 100 g
- `vitA_betacaroteno` — µg de β-caroteno por 100 g

En BEDCA los dos campos existen por separado («Retinol» y «Carotenos totales» o
«β-caroteno»); en CIQUAL también («Rétinol» y «Beta-carotène»); en USDA son
«Retinol», «Carotene, beta» y «Vitamin A, RAE». **El orden de `Bases.md` sigue
mandando**: BEDCA primero.

**Por qué corre prisa, con la medida hecha.** En los 216 menús precalculados el
**83 %** de la vitamina A viene de vegetal, y **103 de los 216 no llegarían al
mínimo de FEDIAF si el caroteno no contara**. El peor declara 11.191 µg y solo
29 son retinol. Detalle: `HALLAZGOS_LECTURA_FUENTES.md` §N-19.

**Esto no lo rellena el asistente**, como todo lo de este archivo.

---

## Ácido oxálico: una columna que no existe y que ahora tiene cifra objetivo (9 de septiembre de 2026)

**Qué hacemos hoy.** En la patología `oxalato` (urolitos de oxalato cálcico) el
motor excluye los alimentos altos en ácido oxálico con una **lista escrita a
mano**: `OXALATO_ALTO`, en `motor/seguridad.py`. Funciona, pero es una lista: se
desincroniza en cuanto entra una ficha nueva al catálogo, y no sabe de
cantidades — un alimento está dentro o fuera.

**Qué dice la fuente.** Fascetti & Delaney 2ª ed., cap.16, leído entero el 9 de
septiembre:

> *«Dietary oxalic acid concentrations should be reduced to the lowest possible
> concentration in cases of calcium oxalate urolithiasis. **Suggested dietary
> concentration is <20 mg oxalic acid/100 g of food (dry matter basis) or about
> <40-45 mg oxalic acid/Mcal.**»*

Y dice también **dónde está**: *«Most pet food ingredients are low in oxalic acid,
**with the exception of vegetables, legumes, and several vegetable-based
fermentable fibers** (e.g. beet pulp and soybean fiber).»* O sea que en nuestro
catálogo el problema está concentrado en las 45 fichas de «Verduras y frutas».

**Qué falta**, y es un dato, así que **no lo rellena el asistente**:

- una clave `acido_oxalico` (mg/100 g de alimento tal cual, como todo lo demás —
  ver `UNIDADES.md`) en las fichas donde la haya, empezando por las 45 verduras;
- con su fuente por ficha, como el resto del catálogo.

**Qué se gana cuando esté.** Que el oxalato deje de ser una lista de nombres y
pase a ser un **techo por nutriente**, que es como se aplican todos los demás
límites del motor: auditable, con cifra, y sin desincronizarse al añadir un
alimento. El objetivo son **<45 mg/1000 kcal**.

**Dónde buscarlo.** Ni BEDCA ni CIQUAL ni USDA publican ácido oxálico de forma
sistemática (no es uno de los 41 nutrientes del perfil). Hay tablas específicas
en la literatura de urolitiasis humana. Es el mismo caso que las purinas, que ya
viven en el catálogo con su `purinas_fuente` propia: **la procedencia vive en la
ficha, no en una lista central**.

---

## El retinol y el β-caroteno, por separado (9 de septiembre de 2026)

**Por qué hace falta, en una línea:** hoy cada ficha trae una sola columna
`vitA` en µg, y **no está escrito qué son esos microgramos**. Pueden ser retinol
solo, equivalentes de retinol europeos (β-caroteno ÷ 6) o RAE americanos
(÷ 12), y contrastando contra USDA se ve que **las fichas mezclan los tres**:
zanahoria 1.346 (= ÷ 6), boniato 667 (= RAE), rúcula 596 (que no es ni lo uno
ni lo otro).

**Y ahora sabemos contra qué hay que compararlo.** FEDIAF 2025, Tabla VII-14
(«Conversion factors – Vitamin source to activity»), fila literal:

> Provitamin A (β-carotene) **(dogs)** — 1.0 mg = **833 IU**

Con el retinol a 0,3 µg = 1 IU en la misma tabla, eso son **1 mg de β-caroteno
= 250 µg de equivalentes de retinol**: un factor de **4 a 1**. Más generoso que
el 6:1 europeo y que el 12:1 americano.

O sea que **una ficha calculada con ÷ 6 declara un 33 % menos** de lo que FEDIAF
le contaría a un perro, y una con RAE, **un 67 % menos**. Y el NRC 2006 confirma
la parte cualitativa: *«only dogs have the ability to use carotenoid precursors
of vitamin A»*.

**Qué falta**, y es un dato, así que **no lo rellena el asistente**:

- `retinol` (µg/100 g de alimento tal cual): el retinol preformado, que es lo
  que traen vísceras, huevo, lácteos y suplementos;
- `betacaroteno` (µg/100 g): lo que traen verduras y frutas;
- con su fuente por ficha, como el resto del catálogo. USDA los publica los dos
  por separado (`Retinol` y `Carotene, beta`); BEDCA también.

**Qué se gana cuando estén.** Que `vitA` se calcule como
`retinol + β-caroteno / 4` con el factor de la propia FEDIAF, en vez de heredar
el convenio de la base de datos de la que salió cada ficha. Hoy **el 83 % de la
vitamina A de los 216 menús precalculados viene de verduras y frutas** —o sea de
caroteno— y **103 de los 216 no llegarían al mínimo si el caroteno no contara**:
es la columna que más depende de un convenio que no está escrito.

**Y una cosa que sí se puede decir ya:** contra el TECHO esto va del lado
seguro. La toxicidad de la vitamina A es del **retinol preformado**, no del
β-caroteno, así que un menú cuya vitamina A venga de zanahoria no se acerca al
máximo aunque el número lo parezca. Eso es información que la ficha verificada
debería dar y hoy no da.

---

## La digestibilidad, que no está en ninguna base de composición (9 de septiembre de 2026)

**Pregunta de Elena: «¿hay alguna fuente donde se pueda sacar la digestibilidad
de los alimentos?».** La respuesta corta es **no, no para un alimento crudo,
ficha a ficha**. La larga es lo que sí hay.

### Por qué hace falta

FEDIAF **§2.2 «Scope»** dice que toda su tabla vale para alimentos *«with normal
digestibility (i.e. ≥70 % DM digestibility; **≥80 % protein digestibility**)»*, y
**§3.2.1** dice qué hacer si no se puede garantizar: subir los aminoácidos
esenciales un 10 % como mínimo. Como no la tenemos, desde el 9 de septiembre
**se aplica ese +10 %** — o sea que la falta de este dato ya está costando
margen.

Y aparece cuatro veces más el mismo día: SACN5 Tabla 18-9 pide **>80 % de
digestibilidad de materia seca** al perro de trabajo, y la Tabla 62-1 (colitis)
distingue *«highly digestible: ≥87 % for protein»* de *«fiber-enhanced: ≥80 %»*.

### Lo que NO la tiene

**Ninguna de las tres bases de composición.** BEDCA, CIQUAL y USDA dan lo que hay
*en* el alimento, no lo que el perro absorbe. No es un hueco de esas bases: es
otra magnitud, y se mide con perros, no con un espectrofotómetro.

### Lo que sí hay, y de dónde sale cada cosa

1. **El supuesto general, para calcular kcal.** SACN5 cap.5: el método de Atwater
   modificado *«assume an average apparent digestibility of **80 % for protein,
   90 % for crude fat and 84 % for carbohydrate**»*, y los alimentos comerciales
   típicos *«range in digestibility from 75 to 85 %»*.

   ⚠️ **Y trae un aviso que nos toca de lleno**: ese método *«**overestimates the
   ME content of foods high in fiber or ash**»*. Una ración BARF lleva entre un
   20 y un 60 % de hueso carnoso, que es ceniza. Si las kcal de las fichas salen
   de Atwater, **están sobreestimadas** para los alimentos con hueso — y las
   kcal son el denominador de los 43 requisitos. Está sin comprobar de dónde
   viene el campo `energia` de cada ficha.

2. **Para los minerales del hueso, sí hay medidas concretas.** Köber 2017 —que ya
   está en el repo de fuentes— dice literal: *«Ca and P from bones were shown to
   have a **lower apparent digestibility in dogs** than other mineral sources»*,
   citando a **Siedler & Dobenecker (2015), ESVCN Proceedings p.128**. Y
   **Hofmann, Dobenecker y Kienzle (2025)**, que también está en el repo de
   fuentes y **no se ha usado nunca**, trae las cifras en su Tabla 3.

3. **La escala con la que se lee un coeficiente** (SACN5 cap.48, recuadro 48-3,
   leído entero el 9 de septiembre). *«**Highly digestible** has generally been
   reserved for products with protein digestibility **≥87 %** and fat and
   carbohydrate digestibilities **≥90 %**»*, y la comida comercial media va en
   *«**78 a 81 %**, **77 a 85 %** y **69 a 79 %** for crude protein, crude fat
   and carbohydrate»*.

   Sirve para situar el +10 %: la comida comercial corriente **no llega** al
   umbral de «alta digestibilidad», y una ración cruda casera no está ni por
   encima ni por debajo — está **sin medir**, que es el supuesto exacto que
   FEDIAF cubre con ese factor.

4. **Cómo se mide de verdad.** FEDIAF sección 6 da los dos protocolos completos
   (método del indicador con óxido de cromo, y colección cuantitativa total).
   Hacen falta perros, seis o más, y varios días de recogida de heces. No es algo
   que se saque de una tabla.

### Qué falta, entonces

- **Dos campos por ficha**, `digestibilidad_ms` y `digestibilidad_proteina`, con
  su fuente — igual que `purinas_fuente` o `fuente_epa_dha`. **No los rellena el
  asistente.**
- Y como no van a existir para 163 fichas, la alternativa realista es **una
  cifra por familia** (músculo crudo, hueso carnoso, víscera, vegetal) sacada de
  la literatura de dietas crudas, que hoy **no está en el repo de fuentes**: los
  trabajos del grupo de Illinois (Beloshapka, Kerr, Swanson) son los que la
  publican.

**Mientras tanto, la decisión tomada es la conservadora**: no se supone nada, se
aplica el +10 % que FEDIAF manda aplicar cuando no se puede garantizar.

---

## La lactosa del «Yogur griego» (9 de septiembre de 2026)

**Un dato, una ficha.** SACN5 cap.55, recuadro 55-3, da un umbral con cifra para
el perro: *«dogs developed diarrhea while consuming more than **1 g of lactose/kg
body weight**»*. El catálogo tiene un lácteo —«Yogur griego», en Extras— y **no
tiene el campo**: la lactosa no es uno de los 41 nutrientes.

**Dónde está**: BEDCA y USDA publican lactosa en los yogures. USDA la trae como
`Lactose` en su ficha de *Yogurt, Greek, plain*; BEDCA, en la ficha del yogur
natural. El orden de `Bases.md` manda: BEDCA primero.

**Qué hacer con él cuando esté**: la decisión (tope duro o aviso) y la cuenta ya
hecha están en `PENDIENTE_NUTRICION.md`. Aquí solo falta el número, con su
fuente y su fecha, como cualquier otro. **No lo rellena el asistente.**

Medido el 9 de septiembre: **0 de los 216 menús del catálogo usan el yogur**, así
que el hueco no está afectando a nadie hoy.

## La forma química de las vitaminas del grupo B, ficha por ficha (9 de septiembre de 2026)

Sale de leer entera la **§7.5 de FEDIAF** y su **Tabla VII-14**, que hasta ese
día estaba marcada «pendiente». Es la hermana de las dos secciones de arriba
sobre la vitamina A: **la misma pregunta, para otros seis nutrientes.**

**Qué dice la fuente.** Una etiqueta puede declarar el peso de la SAL o del
ÉSTER, no el de la vitamina, y la Tabla VII-14 da la equivalencia:

| Fuente declarada | 1 mg de fuente = |
|---|---|
| Mononitrato de tiamina | 0,81 mg de B1 |
| Clorhidrato de tiamina | 0,79 mg de B1 |
| D-pantotenato cálcico | 0,92 mg de ácido pantoténico |
| **DL-pantotenato cálcico** | **0,41 – 0,52 mg** |
| Clorhidrato de piridoxina | 0,82 mg de B6 |
| Cloruro de colina (ion colina) | 0,75 mg de colina |

**Qué falta.** Ninguna de las 11 fichas de multivitamínico dice en qué forma
química viene cada vitamina. Sin eso no se puede saber si el número que
copiamos de la etiqueta es actividad o peso de aditivo.

**Y está medido, que es lo que decide si esto importa.** Sobre menús resueltos
en vivo el 9 de septiembre, suponiendo el peor factor de la tabla para cada uno:

| Nutriente | Peor factor | Peor menú, veces el mínimo de FEDIAF | ¿Aguantaría? |
|---|---|---|---|
| Ácido pantoténico | ×0,41 | 1,96 | **No: se quedaría en 0,80 del mínimo** |
| Tiamina | ×0,79 | 1,29 | Sí, por muy poco (1,02) |
| Colina | ×0,75 | 1,40 | Sí |
| Vitamina B6 | ×0,82 | 3,58 | Sí, sobrado |

O sea: **uno de los cuatro caería por debajo del mínimo de FEDIAF con el menú
saliendo verde**, y otro aguanta por un 2 %. No es una duda teórica.

**Lo que sí está comprobado ya**, y por eso no está aquí: las seis conversiones
de UI a microgramos que declaran tres fichas (napfcheck proLEBER y los dos
V-INTEGRA, vitamina A y D3 cada uno) usan exactamente los factores de la
Tabla VII-14 y salen bien. Lo rehace el **BLOQUE 70** en cada batería, desde la nota de cada ficha.

**Cómo se rellena.** Etiqueta a etiqueta, buscando en la lista de aditivos la
forma exacta (el número E/3a suele venir al lado). Si la etiqueta declara
«Vitamina B5 (ácido pantoténico)» el número ya es actividad y no hay que tocar
nada; si declara «D-pantotenato cálcico», hay que multiplicar. **No lo rellena
el asistente.**

---

## La humedad de cada ficha, que decide siete techos de seguridad (10 de septiembre de 2026)

**Qué falta:** el **agua** (o la materia seca) de cada uno de los alimentos del
catálogo, en g/100 g tal cual se da. Y con ella, idealmente, las **cenizas**.

### Por qué hace falta, y por qué ya no es un hueco de ficha cualquiera

Hasta hoy la humedad era «estaría bien tenerla». Leyendo **§3.2.1 de FEDIAF al
pie de la letra** pasa a ser el dato que decide **siete techos**:

> *«Legal maxima in EU legislation are expressed on 12% moisture content and
> **they do not account for energy density**. Therefore in these guidelines they
> are **only provided on a dry matter basis**.»*

> *«These conversions assume an energy density of 16.7 kJ (4.0 kcal) ME/g DM.
> **For foods with energy densities different from this value, the
> recommendations should be corrected for energy density.**»*

Los máximos **legales** —cobre, yodo, hierro, manganeso, selenio, zinc y
vitamina D— FEDIAF los publica **solo en materia seca**. El motor los aplica
**por 1000 kcal**, convertidos con el ×2,5 de la Tabla III-2, que supone
**4,0 kcal ME por gramo de materia seca**. Si la ración no está en 4,0, la propia
FEDIAF pide corregir.

Y estos siete son precisamente los que **no tienen máximo nutricional**: el legal
es el único techo que tienen.

### Cuánto está en juego

Selenio, techo legal 56,80 µg/100 g MS:

| Densidad real (kcal ME/g MS) | Techo por 1000 kcal |
|---|---|
| 3,5 | 162,3 |
| **4,0** (el supuesto) | **142,0** |
| 4,5 | 126,2 |
| 5,0 | 113,6 |

Una ración BARF tira en las dos direcciones a la vez: el hueso (20-60 %) es casi
todo mineral y suma materia seca casi sin calorías, y la grasa suma calorías casi
sin materia seca. **No se puede saber ni el signo del error** sin el dato.

### Lo que sí hay

Las tres bases lo publican: BEDCA da el agua como nutriente, CIQUAL trae
`Eau (g/100 g)` y USDA `Water`. **No es un hueco de las bases: es una columna que
el catálogo nunca cargó.** Va por el orden de `Bases.md`, ficha a ficha, y **no
lo rellena el asistente**.

Detalle y la medida de sensibilidad: **F-27** en `HALLAZGOS_LECTURA_FUENTES.md`.

### Y una tercera consecuencia, que es la más grave

Con la humedad y las cenizas se puede calcular el **NFE** y con él aplicar la
ecuación de cuatro pasos del Anexo 7.2 de FEDIAF, que es como se calcula de
verdad la energía metabolizable de un alimento. Sin ellas, **el campo `energia`
de cada ficha no se puede comprobar contra nada** — y las kcal son el
denominador de los 43 requisitos. Ver **F-29**.

---

## La forma química del selenio de cada suplemento (10 de septiembre de 2026)

**Qué falta:** para cada alimento del catálogo de categoría suplemento que
declare selenio, **en qué forma viene**: orgánica (levadura de selenio,
selenometionina) o inorgánica (selenito sódico, selenato sódico). Está en la
etiqueta del bote.

### Por qué hace falta

La **nota d** de las tablas de FEDIAF pone un **segundo techo**, y solo para la
forma orgánica:

> *«For organic selenium a maximum supplementation level of **22.73 µg organic
> Se/100 g DM** applies.»*

Son **56,8 µg/1000 kcal** de lo **añadido**, contra los **142** que aplicamos al
**total**. El 40 %.

**Medido:** un `CachorroJoven` de 6 kg recibió en uno de sus menús **63,0
µg/1000 kcal de selenio procedente de suplementos** — por encima del techo de la
nota d **si ese selenio fuera orgánico**. No lo sabemos.

Es el mismo patrón que la forma química de las vitaminas del grupo B: el dato
vive en la etiqueta, no en ninguna base de composición, y sin él no se puede ni
aplicar el techo ni descartarlo.

Detalle y la medida completa: **F-28** en `HALLAZGOS_LECTURA_FUENTES.md`.

## La energía del hueso carnoso crudo (11 de septiembre de 2026)

**Qué falta**: una energía metabolizable **medida** del hueso carnoso crudo, o la
digestibilidad de su proteína. Cualquiera de las dos vale.

**Por qué hace falta.** Las nueve fichas de «Hueso carnoso» calculan su `energia`
como 4×proteína + 9×grasa, que son los factores de Atwater, y NRC 2006 cap.3
excluye el hueso de esos factores con esas palabras: *«meat, offal (except bones
and bone meal), poultry, fish…»*. Ese campo no es decorativo: es la fila de
energía del MILP y el divisor con el que se calculan **todos** los límites del
motor, que van «por 1000 kcal».

**Cuánto pesa, ya medido** (no hace falta remedirlo): el factor en duda es el de
la proteína, que aporta el **13,1 %** de las kcal del menú mediano (7,8 a 30,2 %
sobre los 216 del catálogo). Aunque el colágeno se digiriera al 60 % en vez del
90 % que Atwater supone, las kcal bajarían un 2,6-10,1 %. Es un error de un
dígito por ciento, en la dirección de **infravalorar** la concentración del menú.

**Dónde se ha buscado y no está**:

· **Köber 2017**, que es la fuente de los macros de estas nueve fichas
  (comprobado celda a celda): da materia seca, proteína bruta, grasa bruta,
  cenizas, calcio y fósforo. **No da energía.**
· 🔴 **RETIRADO 11-sep-2026**: aquí se dijo que la Tabla 13-1 de NRC trae *«Meal, with bone, rendered»* con 3,61 kcal/g y que eso invertía la dirección del problema. **Es falso.** El cuerpo de esa tabla NO está en el `.txt` de NRC (el capítulo 13 son 177 líneas con solo títulos y notas al pie; donde iría la tabla hay dos números de página, «667 668»), y las tres cadenas «Meal, with bone», «with bone, rendered» y «5-00-388» no aparecen en las 43.556 líneas. Lo encontró el contador de NRC al montarlo. Detalle y qué queda en pie: `PENDIENTE_NUTRICION.md`.
· **NRC 2006, el libro entero**: «collagen» sale en el metabolismo de la vitamina
  C, en la lisina, en el sodio y en una frase sobre el triptófano, y **en ninguna
  con un coeficiente de digestibilidad**.

**Lo que NO se hace mientras tanto**: poner un factor estimado. Un 0,75 o un 0,60
porque suenan razonables sería un número con forma de dato bueno que nadie puede
rehacer, que es exactamente lo que este repo tiene prohibido.

**Y si aparece la cifra**: corregir la energía de las nueve fichas cambia todos
los menús del catálogo y el DER efectivo de todas las raciones, así que hay que
regenerar con `regenerar_catalogo.py`. Detalle completo y la tabla de
sensibilidad: `PENDIENTE_NUTRICION.md`.

## Un suplemento de vitamina E suelto (11 de septiembre de 2026)

**Qué falta**: una ficha de catálogo de un producto que sea **solo vitamina E**
(α-tocoferol), con su etiqueta real, su dosis de fabricante y su forma química.

**Por qué hace falta, medido.** SACN5 pide **≥400 UI de vitamina E por kg de materia
seca** —67,1 mg/1000 kcal— en cinco capítulos distintos, y el motor ya lo exige en
cuatro patologías (renal, hepatopatía, obesidad y artrosis). Al aplicarlo también al
perro **sano**, la batería dio **seis fallos**: el toy de 1,5 kg se queda sin menú,
el adulto de 20 kg con ocho especies excluidas también, y en varios perros el motor
mete alimentos que nadie pidió sin avisar.

**La causa no es la cifra, es el catálogo.** Las únicas fuentes que llegan a 67,1
mg/1000 kcal son los **nueve multivitamínicos** (200 a 670 mg/100 g y 0 kcal), y el
motor solo deja meter **dos suplementos** por menú. Lo siguiente es el aceite de
girasol, con 63 mg/1000 kcal, que además está limitado por las proporciones de BARF.
Para un perro de 1,5 kg con 200 kcal, llegar a 13,4 mg de vitamina E total sin gastar
las dos plazas de suplemento en ello es lo que no sale.

**Qué se desbloquea con esa ficha**: que el suelo del perro sano deje de costar
menús. Está **ENCENDIDO** desde el 11 de septiembre por decisión de Elena, y con la
batería en rojo mientras siga así: el perro con ocho especies fuera se queda sin menú
(adulto, cachorro y toy), y al toy de 1,5 kg le cuesta tanto que el solver no lo saca
en 1 s ni en 20 intentos. Las otras 15 combinaciones de alergias y exclusiones siguen
saliendo, y al toy lo salva la escalera por la vía de la API. Y de paso deja de
depender de un multivitamínico completo el cumplir una recomendación de un solo
nutriente.

### ⚠️ Y HAY UNA SEGUNDA COSA QUE FALTA, MEDIDA EL 11 DE SEPTIEMBRE: LA FORMA DE LA QUE YA HAY

Los 67,1 mg salen de convertir los 400 UI con el factor del **d-α-tocoferol natural**
(1,49 UI/mg → 1 UI = 0,671 mg), que es **el más permisivo de los siete** de la Tabla
VII-14 de FEDIAF. Con el sintético (dl-α-tocoferil acetato, 1 UI = 1 mg) el mismo
requisito serían **100 mg/1000 kcal**, un 49 % más alto. Y Fascetti cap.6 lo confirma
por su lado: «40 IU vitamin D3 = 1 ug cholecalciferol; **1 IU vitamin E = 1 mg
all-rac-alpha-tocopheryl acetate**».

Medido ese día: en el catálogo **solo dos alimentos llevan vitamina E declarada** —
Homemadekun (625 mg/100 g) y NEKTON Dog Easy-BARF (200) — y **ninguno de los dos dice
qué forma es**. O sea que la cifra que hoy deja a un perro sin menú descansa en una
suposición sobre un dato que no está en ninguna ficha, y la suposición va al lado
**menos** exigente. Si resultara ser el acetato, el suelo real sería más alto, no más
bajo.

Es el mismo patrón que la forma química de las vitaminas del grupo B y la del selenio:
el dato vive en la etiqueta del fabricante y no en el catálogo. **No lo rellena el
asistente.**

**Lo que hace falta de la etiqueta**, igual que con cualquier otra ficha: miligramos
de vitamina E por 100 g, **qué forma química** (d-α-tocoferol natural, dl-α-tocoferol
o el acetato — cambian el factor de UI a mg, FEDIAF Tabla VII-14), y la dosis máxima
que marca el fabricante. **No lo rellena el asistente.**

---

## ⚠️ NO es un dato que falte: por qué el cerdo NO entra en el catálogo (11 de septiembre de 2026)

Esto va aquí porque es donde alguien mirará el día que proponga añadirlo, y
porque **es la decisión contraria a las demás de este documento**: no falta un
dato, sobra una idea.

**Hoy el catálogo no tiene ninguna ficha de cerdo**, y hay **dos motivos de
fuente** para que siga así:

**1. El cobre del hígado de cerdo no llega al perro.** SACN5 cap. 6: su
disponibilidad es esencialmente cero, mientras que los de vaca, cordero y pavo
—tres de los seis hígados del catálogo— la misma fuente los nombra como *«highly
available»*. Una ficha de hígado de cerdo declararía cobre que el perro no
absorbe, y eso **no lo caza el semáforo**: es un valor con forma de dato bueno.

**2. Y el que de verdad cierra la puerta: la pseudorrabia.** Ettinger, Feldman y
Côté, 8.ª ed., cap. sobre pseudorrabia (enfermedad de Aujeszky):

> «La pseudorrabia es una enfermedad de los perros **poco frecuente pero
> mortal** […] Se cree que la mayoría de los casos en perros son el resultado de
> la **ingestión de carne de cerdo cruda infectada**.»

El perro es huésped final y **la enfermedad es mortal**. Este motor calcula
raciones **crudas**. Meter cerdo sería ofrecer, en crudo, el alimento cuya vía de
contagio principal es exactamente esa.

**Qué haría falta para reabrirlo** (las cuatro razones de `CERRADO.md`): una
fuente que diga que el riesgo es despreciable con carne de origen controlado, o
que el producto se ofrezca **cocinado**, que es otro motor. Mientras tanto, no es
un hueco: es una exclusión con dos fuentes.

⚠️ **Y el corolario para la app, que es lo que más se confunde**: el aviso sobre
la ración cruda **no puede ser «cuidado con el cerdo»**, que es lo que la gente
cree. Los casos de salmonelosis que documenta Ettinger cap. 192 son de **vacuno**,
y el catálogo está lleno de los reservorios clásicos: 10 fichas de pollo, 10 de
ternera, 8 de pavo, 7 de vaca. El aviso tiene que ser sobre el manejo de **lo que
sí le estamos dando**.
