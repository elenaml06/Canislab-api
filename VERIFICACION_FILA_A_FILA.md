# Las tablas de SACN5, fila a fila

**8 de septiembre de 2026, tercera pasada.**

## Por qué existe este documento

Porque «verificado» significaba menos de lo que parecía.

Las dos primeras pasadas comprobaron que **el número que aplicamos coincide con
el de su fuente**. Eso está bien y sigue siendo cierto. Pero **no es lo mismo que
haber recogido todo lo que la fuente dice**, y yo llamé «verificado» a lo primero.

Lo destapó una pregunta: la Tabla 67-3 de la pancreatitis tiene **dos** filas de
grasa —≤15 % para el perro normal y ≤10 % para el obeso o hipertrigliceridémico—
y yo cité una diciendo «verificado literal». No se me escapó una tabla: se me
escapó media fila de la tabla que estaba mirando.

Si pasó ahí, podía haber pasado en las otras veinte. Así que esta pasada es
distinta: **se leen todas las filas de cada tabla y se dice qué hacemos con cada
una.** Cuatro estados:

| | |
|---|---|
| ✅ | **Aplicada.** Es un límite del motor |
| ➖ | **No aplicable.** Es de gato, es cualitativa, o es un fármaco/suplemento que no se formula |
| ⚠️ | **Más laxa que FEDIAF.** La fuente la pide pero el requisito general ya es más exigente: aplicarla no cambiaría ni un menú |
| ❌ | **No aplicada, y sí cambiaría algo** |

---

## Lo que ha salido

**Tres discrepancias nuevas**, y una es del mismo tipo que la de la pancreatitis:

### 1 · En obesidad estamos mezclando los dos niveles de la tabla

La Tabla 27-4 no da una recomendación: da **dos columnas**, «foods for weight
loss» y «foods for prevention of weight regain». Y nosotros cogemos filas de las
dos:

| Factor | Adelgazamiento | Mantener el peso | Lo que aplicamos |
|---|---|---|---|
| Grasa | ≤9 % → 22,5 | ≤14 % → 35 | **30** — ni uno ni otro |
| Proteína | ≥25 % → 62,5 | ≥18 % → 45 | **62,5** — el de adelgazar |
| Fibra | 12-25 % → 30-62,5 | 10-20 % → 25-50 | **30** — el de adelgazar |
| Lisina | ≥1,7 % → 4,25 | *(no la pide)* | **4,25** — el de adelgazar |

La grasa está declarada y con su motivo medido (22,5 no resuelve con el catálogo
real), así que no es un error escondido. Pero **la incoherencia sí es real**: si
el perro está adelgazando, la grasa debería tender a 22,5; si está manteniendo,
la proteína puede bajar a 45. Estamos aplicando la mitad de cada columna.

**Es la misma clase de fallo que la pancreatitis:** una tabla que gradúa y
nosotros tomando una fila suelta.

### 2 · La artrosis pide siete cosas y aplicamos dos

Tabla 34-2, todas caninas y todas con cifra:

| Fila | Cifra | Por 1000 kcal | |
|---|---|---|---|
| Total omega-3 | 3,5-4,0 % | 8,75-10 g | ❌ |
| Eicosapentaenoic acid | 0,4-1,1 % | 1,0-2,75 g | ✅ |
| Omega-6:omega-3 | <1:1 | ratio | ❌ |
| L-carnitine | ≥300 mg/kg | 75 mg | ✅ |
| Glucosamine HCl | ≤0,10 % | — | ➖ suplemento |
| Chondroitin sulfate | ≤0,08 % | — | ➖ suplemento |
| Vitamin E | ≥400 IU/kg | 100 UI | ❌ |
| Vitamin C | ≥100 mg/kg | 25 mg | ➖ el perro la sintetiza |
| Selenium | 0,5-1,3 mg/kg | 0,125-0,325 mg | ⚠️ |
| Phosphorus** | 0,3-0,7 % | 750-1750 mg | ❌ |
| Sodium** | 0,2-0,4 % | 500-1000 mg | ❌ |

Y la nota `**` dice algo que no es un detalle: *«Dogs with osteoarthritis are
often in age groups at risk for kidney and/or heart disease»*. O sea que el
fósforo y el sodio están ahí **porque el perro artrósico suele ser mayor** — es
una tabla que ya está pensando en la comorbilidad.

El **omega-3 total** es el que más pesa: 8,75 g coincide casi exactamente con lo
que exige el Reglamento (UE) 2020/354 para la misma indicación (≥8,24). Dos
fuentes independientes piden lo mismo y no pedimos ninguna.

### 3 · La disfunción cognitiva pide siete y aplicamos una

| Fila | Cifra | Por 1000 kcal | |
|---|---|---|---|
| Vitamin E | ≥750 mg/kg | 187,5 mg | ✅ |
| Vitamin C | ≥150 mg/kg | 37,5 mg | ➖ el perro la sintetiza |
| Selenium | 0,5-1,3 mg/kg | 0,125-0,325 mg | ⚠️ |
| L-carnitine | 250-750 IU/kg | — | ❌ (y la unidad está rara: «IU» para la carnitina) |
| α-lipoic acid | ≥100 mg/kg | 25 mg | ➖ no está en el catálogo |
| **Total omega-3** | **>1 %** | **2,5 g** | ❌ |
| Frutas y verduras | 1 % de cada uno de cinco | — | ➖ es forma, no nutriente |

---

## Las 21 tablas, una por una

### 27-4 · Obesidad
Densidad ≤3,4 kcal/g ❌ · grasa ✅ *(nivel mezclado, ver arriba)* · fibra ✅ ·
proteína ✅ · lisina ✅ · carbohidrato ≤40 % ➖ *(el motor no modela carbohidrato)* ·
L-carnitina ✅ · vit E ≥400 UI/kg ❌ · vit C ➖ · selenio ⚠️ · sodio 0,2-0,4 % ❌ ·
fósforo 0,4-0,8 % ❌

### 28-2 · Hiperlipidemia
Grasa <12 % ✅ · fibra ≥10 % ✅ · fibratos ➖ *(fármaco)*. **Completa.**

### 29-3 · Diabetes
Agua ➖ · carbohidrato digestible ≤55 % ➖ · evitar azúcares simples ✅ *(excluye
fruta)* · fibra 7-18 % ✅ · grasa <25 % ⚠️ *(62,5 g: más laxo que cualquier menú
nuestro)* · proteína 15-35 % ⚠️ · evitar semihúmedos ➖. **Completa en lo aplicable.**

### 32-1 · Dermatosis y dermatitis
Proteína 25-30 % ❌ · grasa 10-15 % ❌ · Phe+Tyr >1,3 % ✅ · digestibilidad >80 % ➖ ·
linoleico >1,0 % ⚠️ *(FEDIAF ya exige 3,3)* · zinc 100-200 mg/kg ✅ ·
**cobre <200 mg/kg ⚠️** *(el máximo legal de FEDIAF, 7,0 mg, ya es 7 veces más
estricto)* · «higher zinc si calcio >1,5 % MS» ❌ *(y en BARF con hueso el calcio
suele estar ahí)* · suplementos de zinc y retinoides ➖ *(fármacos)*

### 34-2 · Artrosis
Ver arriba. **2 de 7 aplicables.**

### 35-3 · Disfunción cognitiva
Ver arriba. **1 de 4 aplicables.**

### 36-4 · Cardiovascular
Sodio ✅ · cloruro 1,5 × sodio ❌ · taurina ✅ *(en la MCD)* · L-carnitina ✅ *(ídem)* ·
fósforo 0,2-0,7 % ❌ · potasio ≥0,4 % ⚠️ *(FEDIAF exige 1450 > 1000)* ·
magnesio ≥0,06 % ⚠️ *(FEDIAF exige 200 > 150)*

### 37-9 · Renal
Agua ➖ · proteína 14-20 % ➖ *(bajo FEDIAF: prescripción)* · fósforo ✅ · sodio ✅ ·
cloruro 1,5 × sodio ❌ · potasio 0,4-0,8 % ✅ *(el techo)* · omega-3 0,4-2,5 % ❌ ·
vit E ≥400 UI/kg ❌ · vit C ➖

### 40-5 · Oxalato
Agua ➖ · proteína 10-18 % ➖ *(bajo FEDIAF)* · **calcio 0,4-0,7 % ➖ a propósito**
*(fuente más reciente lo contradice)* · evitar alimentos con oxálico ✅ ·
fósforo ✅ · Ca:P 1,1-2:1 ❌ · sodio ✅ · magnesio ✅ · evitar vitamina C ❌ ·
pH urinario 7,1-7,5 ➖

### 41-6 · Fosfato cálcico
Agua ➖ · proteína ✅ · calcio 0,4-0,7 % ➖ *(mismo criterio que el oxalato)* ·
fósforo ✅ · **Ca:P 1,1-2:1 ❌** · sodio ✅ · magnesio ✅ ·
**vitamina D 500-1500 UI/kg ❌** *(= 3,1-9,4 µg/1000 kcal: MÁS estricto que el
máximo legal de 14,19 que aplicamos)* · pH 6,2-6,6 ➖

### 42-1 · Cistina
Agua ➖ · proteína 10-18 % ➖ *(bajo FEDIAF)* · sodio ✅ · pH 7,1-7,7 ➖

### 43-3 · Estruvita
Agua ➖ · proteína ✅ *(prevención)* · fósforo ✅ · magnesio ✅ · pH ➖.
**Completa en lo formulable.** La disolución no se modela, y se dice.

### 44-1 · Sílice
Agua ➖ · proteína 10-18 % ➖ *(bajo FEDIAF: la patología bloquea)* ·
evitar gluten de maíz / cáscaras ➖ *(ingredientes de pienso)* · pH ➖

### 57-1 · Enteropatía crónica
Potasio 0,8-1,1 % ✅ *(techo)* · densidad energética ❌ · grasa ✅ · proteína ✅ ·
fibra cruda ≤5 % o 7-15 % ❌ · digestibilidad ➖

### 58-1 · PLE
Densidad >3,5 kcal/g ❌ · grasa ✅ · proteína ✅ · fibra ✅ · digestibilidad ➖

### 60-1 · SIBO
Digestibilidad ➖ · grasa ✅. **Completa en lo aplicable.**

### 63-3 · Intestino irritable
Fibra soluble / mixta / insoluble / cruda: se aplica la **cruda** ✅, que es la
única que el catálogo sabe medir — y lo dice la propia nota al pie de la tabla

### 64-2 · Estreñimiento
Agua >75 % ➖ *(el BARF lo cumple solo)* · fibra ✅ · digestibilidad ➖ *(gato)* ·
densidad ➖ *(gato)*

### 65-1 · Flatulencia
Digestibilidad ➖ · carbohidrato «rice is preferred» ➖ · proteína ✅ · fibra ✅ ·
**evitar legumbres, lácteos, crucíferas, cebolla, frutos secos, especias y
fructosa ❌** *(son exclusiones de alimento, implementables como el oxalato)*

### 66-1 · EPI
Digestibilidad ➖ · grasa ✅ · fibra ✅. **Completa en lo aplicable.**

### 67-3 · Pancreatitis
Grasa ✅ **en sus dos niveles** desde el 8 de septiembre · proteína ✅.
**Completa.**

### 68-8 · Hepatobiliar
Densidad ≥4,0 kcal/g ❌ · proteína 15-20 % ➖ *(bajo FEDIAF)* · arginina ➖ *(gato)* ·
taurina ✅ · sodio ✅ · cobre ✅ · zinc ✅ · hierro ✅ · vit E ≥400 UI/kg ❌ · vit C ➖

---

## Resumen

**Ninguna cifra aplicada está mal.** Lo que había era **incompleto**, y en dos
casos —la pancreatitis y la obesidad— **incoherente**: tablas que gradúan de las
que tomábamos una fila suelta.

Lo que falta, por lo que pesa:

1. **Coherencia de nivel en obesidad** (¿adelgazar o mantener?). Es una decisión
   de producto: la app sabe si el objetivo es bajar peso.
2. **Omega-3 total en artrosis y en disfunción cognitiva** (8,75 y 2,5 g). Dos
   fuentes independientes lo piden en artrosis. Necesita clave nueva en el `MAPA`.
3. **Ca:P 1,1-2:1 en los dos urolitos de calcio.** El motor ya sabe de ratios.
4. **Vitamina D 3,1-9,4 µg en fosfato cálcico**, más estricta que el máximo legal.
5. **Vitamina E ≥100 UI/1000 kcal** en cuatro tablas distintas (renal, artrosis,
   obesidad, hepatobiliar). Es el factor que más se repite de todos.
6. **Las exclusiones de alimento de la flatulencia**, implementables como las del
   oxalato.
7. **Cloruro = 1,5 × sodio** en renal y cardiopatía.
8. **Fósforo y sodio en artrosis**, que la tabla pide por la comorbilidad del
   perro mayor.

Y una que no es una cifra: **«higher levels of zinc are required in foods with
calcium >1.5 % DM»** (Tabla 32-1). Una ración BARF con hueso suele estar por
encima de ese calcio, así que el suelo de zinc de 25 mg podría quedarse corto
justo en la comida que hacemos nosotros.
