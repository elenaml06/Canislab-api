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
