# Datos que faltan en el catálogo


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

Generado por `auditar_catalogo.py`. **Esto no lo rellena el asistente.**

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

## Testículos de cordero  ·  _Vísceras_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| araquidonico | mg | |
| calcio | mg | |
| cloruro | mg | |
| cobre | mg | |
| colina | mg | |
| dha | g | |
| epa | g | |
| fibra | g | |
| folato | µg | |
| fosforo | mg | |
| grasa | g | |
| hierro | mg | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |
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
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |
| zinc | mg | |

## Timo de ternera  ·  _Vísceras_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| calcio | mg | |
| cloruro | mg | |
| cobre | mg | |
| colina | mg | |
| dha | g | |
| epa | g | |
| fibra | g | |
| folato | µg | |
| fosforo | mg | |
| hierro | mg | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |
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

## Sonrisa de Diez Kelp  ·  _Yodo_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| calcio | mg | |
| cloruro | mg | |
| colina | mg | |
| folato | µg | |
| fosforo | mg | |
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

## Cerebro de ternera  ·  _Vísceras_

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

## GRAU Harina de Hueso  ·  _Calcio_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| cobre | mg | |
| colina | mg | |
| folato | µg | |
| hierro | mg | |
| magnesio | mg | |
| manganeso | mg | |
| niacina | mg | |
| potasio | mg | |
| riboflavina | mg | |
| selenio | µg | |
| tiamina | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |
| zinc | mg | |

## LUPO NATURAL BARF Huesos en polvo  ·  _Calcio_

| Nutriente | Unidad | Valor |
|---|---|---|
| acidoPantotenico | mg | |
| cobre | mg | |
| colina | mg | |
| folato | µg | |
| hierro | mg | |
| magnesio | mg | |
| manganeso | mg | |
| niacina | mg | |
| potasio | mg | |
| riboflavina | mg | |
| selenio | µg | |
| tiamina | mg | |
| vitA | µg | |
| vitB12 | µg | |
| vitB6 | mg | |
| vitD | µg | |
| vitE | mg | |
| yodo | µg | |
| zinc | mg | |

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

## Pets Purest Aceite de Salmón  ·  _Omega-3_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| grasa | g | |
| linoleico (omega-6, C18:2) | g | |
| linolenico (omega-3, C18:3) | g | |
| vitA | µg | |
| vitD | µg | |
| vitE | mg | |

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

## Brit Care Aceite de Salmón  ·  _Omega-3_

| Nutriente | Unidad | Valor |
|---|---|---|
| araquidonico | mg | |
| grasa | g | |
| vitA | µg | |
| vitD | µg | |
| vitE | mg | |

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
