# Rawku — el motor nutricional, para revisión

**8 de septiembre de 2026.** Escrito para que un nutricionista veterinario
pueda revisar el motor entero sin leer código y sin fiarse de nuestra palabra.

No es un resumen de lo que funciona: es el estado real. Cada apartado dice
**qué hace hoy el motor**, **de dónde sale cada número**, **en qué estado
está** y **qué duda queda abierta**. Donde no sabemos algo, lo dice. Donde
hemos decidido algo sin fuente, lo dice también y lo marca.

---

## 0 · Qué es esto y qué se pide

**Qué es Rawku.** Una app que calcula raciones BARF (comida cruda) para
perros. No propone una receta y comprueba si cumple: **resuelve un problema
de programación lineal entera mixta** que decide a la vez qué alimentos usar
y cuántos gramos de cada uno, con los requisitos nutricionales como
restricciones simultáneas. Si no existe ninguna combinación que los cumpla
todos, **no entrega menú**.

**Quién lo usa.** Un dueño, no un veterinario. Hay además un modo profesional
para veterinarios acreditados, que puede formular casos que al dueño se le
bloquean y firmar la pauta con su número de colegiado.

**Qué se pide de esta revisión.** Tres cosas, y la tercera es la que más
falta hace:

1. **Que los números estén bien.** Cada uno lleva su fuente citada abajo.
2. **Que las decisiones que hemos tomado nosotras sin fuente estén
   señaladas** y sean defendibles, o se cambien.
3. **Que cada límite quede clasificado en una de tres cajas** (§0.2). Hoy el
   motor trata igual un límite legal y un objetivo terapéutico que depende
   del caso, y eso significa que **el software está tomando decisiones
   clínicas que nadie ha firmado**.

### 0.1 · Cómo está expresado todo

**Todos los requisitos y límites del motor van en unidades por 1000 kcal de
energía metabolizable.** Es la base de la Tabla III-3b de FEDIAF, y se usa
en todo el motor sin excepción.

Cuando una fuente da el valor en **% de materia seca**, se convierte con
**4000 kcal EM/kg MS** (= 400 kcal/100 g MS). **Ese puente no es nuestro**:

- NRC 2006, al presentar sus tablas: *«The energy density of the diet for
  both dogs and cats was assumed to be 4,000 kilocalories (kcal) of
  metabolizable energy (ME) per kilogram (kg).»*
- FEDIAF 2025 usa la misma densidad, y por eso sus tablas III-3a (por 100 g
  MS) y III-3b (por 1000 kcal) se convierten exactamente con ×2,5.

**Pero es un supuesto, y en dietas bajas en grasa es optimista.** Una ración
baja en grasa es *menos* densa en energía, no más, así que al convertir un
«≤15 % MS» a g/1000 kcal el resultado sube:

| Densidad real | «15 % MS» equivale a |
|---|---|
| 3500 kcal/kg MS | 42,9 g/1000 kcal |
| **4000 (el supuesto)** | **37,5** |
| 4500 kcal/kg MS | 33,3 |

Y hay una **tercera convención** en circulación, el **% de energía
metabolizable**, que usa por ejemplo el objetivo de grasa en diabetes
(Purina, «<30 % ME»). A 8,5 kcal/g de grasa: 20 g/1000 kcal ≈ 17 % EM;
25 ≈ 21 % EM; 37,5 ≈ 32 % EM.

> **PREGUNTA 1.** ¿Es aceptable convertir con 4000 kcal/kg MS en una ración
> BARF, que es húmeda y bastante menos densa que un pienso? Si no lo es,
> ¿qué densidad usarías, o preferirías que los objetivos se expresaran
> directamente en % de EM?

### 0.2 · Las tres cajas: lo que se te pide clasificar

Este es el encargo principal. Cada límite del motor tiene que caer en una de
estas tres, y hoy **ninguno lo lleva escrito**:

| Caja | Qué es | Quién lo puede mover |
|---|---|---|
| **Tope duro** | Límite legal, o valor verificado contra fuente primaria como máximo de seguridad | **Nadie** |
| **Rango clínico** | La fuente da un rango a propósito, porque depende del caso, del estadio y de la analítica | El veterinario, dentro del rango, con el dato de entrada que lo justifique |
| **Criterio nuestro** | Lo pusimos porque resolvía un problema observado, sin fuente veterinaria detrás | Es legítimo, pero va declarado como criterio, no disfrazado de ciencia |

**Y las fuentes ya hacen esa distinción, aunque nosotros no la habíamos
recogido.** Comprobado leyendo los documentos originales:

- **FEDIAF** marca cada máximo con **`(L) = EU legal limit`** o
  **`(N) = nutritional`**. Un `(L)` es ley (Reglamento (UE) 2017/1492); un
  `(N)` es el máximo para poder llamarse «alimento completo».
- **NRC 2006** define cuatro niveles y los nombra: *Minimal Requirement*,
  *Adequate Intake*, *Recommended Allowance*, y **Safe Upper Limit** —
  *«the maximal concentration or amount of a nutrient that has not been
  associated with adverse effects»*. El SUL es el tope duro.
- **Small Animal Clinical Nutrition, 5ª ed. (SACN5)** llama a lo suyo
  literalmente **«key nutritional factors and their TARGET LEVELS»**, y en
  el capítulo 1 enumera **siete cosas que mueven ese objetivo**: *«1) the
  patient's lifestage and physiologic state, 2) environmental conditions…,
  3) the nature of any disease or injury, 4) the known nutrient losses…,
  5) the interactions of medications and nutrients…, 6) the known capacity
  of the body to store certain nutrients and 7) the interrelationships of
  various nutrients»*. Y avisa: *«AAFCO allowances for pet food nutrient
  profiles are not necessarily optimal»*.

O sea: **cuando SACN5 escribe un rango («0.2 to 0.5 %»), el rango es la
respuesta, no una imprecisión.** Eso encaja exactamente con la caja
«rango clínico».

> **PREGUNTA 2.** ¿Te vale esta correspondencia — `(L)` y SUL = tope duro ·
> «key nutritional factor» con rango = rango clínico · lo demás = criterio
> nuestro — como regla general para clasificar los 19 límites del §8? ¿O hay
> casos donde no funciona?

> **PREGUNTA 3.** ¿Conoces algún documento veterinario que trate
> explícitamente **qué límites son rígidos y cuáles quedan a criterio
> profesional**? Hemos buscado en FEDIAF 2025, NRC 2006 y SACN5 y lo más
> cercano es lo de arriba, que es implícito. Si existe algo explícito
> (ECVCN, WSAVA, AAHA), es lo que nos falta.

---

## 1 · La energía: cuántas kcal al día

Es lo primero que se calcula y de lo que cuelga todo lo demás: **los
requisitos van por 1000 kcal**, así que si las kcal están mal, todos los
nutrientes están mal aunque cada uno cuadre.

### 1.1 · Adulto y senior

```
RER  = 70 × peso^0,75
DER  = (base por actividad + ajustes) × peso^0,75
```

| Componente | Valor | Fuente |
|---|---|---|
| Coeficiente RER | 70 × kg^0,75 | Convención universal (FEDIAF, NRC, SACN5) |
| Sedentario | 95 kcal/kg^0,75 | FEDIAF 2025, Tabla VII-7 («Recommendations for DER in relation to activity») |
| Normal | 110 | Íd. (moderada 1-3 h/día, bajo impacto) |
| Activo | 125 | Íd. (moderada, alto impacto) |
| Muy activo | 150 | Íd. (alta, 3-6 h/día) |
| Trabajo | 175 | Íd., extremo superior del rango |
| Ajuste joven (1-2 años) | +15 | Thes et al. 2014, *J Anim Physiol Anim Nutr* |
| Ajuste senior (>7 años) | −7 | Íd.: 100 kcal/kg^0,75 en jóvenes vs. 93 en >7 años |
| Convive con otros perros | +10 | Íd. |
| Macho entero | +10 | Íd. |
| Ajuste por raza | ±15 | Thes et al. 2014, Universidad de Múnich, 586 perros de compañía reales. Media 98; las razas de la lista, 113 y 82 |

**Estado: los cinco escalones de actividad, VERIFICADOS** el 8 de septiembre
contra la Tabla VII-7 de FEDIAF 2025 («Recommendations for DER in relation to
activity»): 95 · 110 · 125 · 150-175, exactos. Y hay un contrato de **85
casos** con sus kcal esperadas, que se comprueba en cada batería.

⚠️ **PERO ESA MISMA TABLA TRAE DOS FILAS QUE EL MOTOR NO USA, Y UNA DUELE.**
Verificado leyendo la tabla entera, no solo la parte que ya estaba citada:

| Fila de FEDIAF VII-7 | Qué dice | Qué hace el motor |
|---|---|---|
| **Great Danes** | **200 (200-250) kcal/kg^0,75** | Nada. Su máximo es 175 («trabajo») |
| **Newfoundlands** | **105 (80-132)** | Nada |
| Obese prone adults | ≤ 90 | Usa RER del peso ideal (70), **más estricto** — ver §1.4 |

**Las dos razas están en la lista de la app.** Medido:

| Perro | FEDIAF, específico de su raza | Motor en «normal» (110) | Le damos |
|---|---|---|---|
| Gran Danés 67,5 kg | **4710 kcal/día** | 2590 kcal/día | **el 55 %** |
| Terranova 56,5 kg | 2164 kcal/día | 2267 kcal/día | el 105 % |

El Gran Danés se queda **2100 kcal/día corto** si su dueño marca «normal».
Y no es una cifra rara: SACN5 cap. 5 dice que las estimaciones de DER en
perro *«range between 95 to 200 kcal … per (BWkg)0.75 per day»*, o sea que
200 es el extremo alto del rango publicado, no un valor extremo.

El ajuste por raza que sí tiene el motor (±15 kcal/kg^0,75, Thes 2014) **no
incluye a ninguna de las dos**.

> **PREGUNTA 4-bis (bloqueante).** ¿Adoptamos las cifras de FEDIAF para Gran
> Danés y Terranova? Y si sí: ¿esos 200 kcal/kg^0,75 son **en vez** del nivel
> de actividad, o el suelo sobre el que se aplica? La tabla los pone bajo
> «DER in relation to activity» pero sin cruzarlos con los cinco niveles.

**Lo que hay que saber:** el DER se calcula **en dos sitios** (servidor y
app), y manda el de la app. Es una duplicación conocida, y por eso existe el
contrato de 85 casos: los dos lados se comprueban contra el mismo fichero.

> **PREGUNTA 4.** El ajuste por raza (±15 kcal/kg^0,75) sale de un solo
> estudio de 586 perros y son 20 razas concretas. ¿Lo mantendrías, o es
> demasiada precisión para el tamaño de la evidencia?

**Contraste con el segundo marco.** SACN5 Tabla 5-2 expresa el DER como
múltiplos de RER en vez de kcal/kg^0,75. Convertido (× RER × 70), los dos
marcos casi coinciden:

| SACN5 | × RER | = kcal/kg^0,75 | Motor |
|---|---|---|---|
| Inactive / obese prone | 1,4 | 98 | sedentario **95** |
| Neutered adult | 1,6 | 112 | normal **110** |
| Intact adult | 1,8 | 126 | activo **125** (y macho entero: 110 + 10 = 120) |
| Light work | 2,0 | 140 | muy activo **150** |
| Moderate work | 3,0 | 210 | trabajo **175** |
| Weight loss | 1,0 | 70 | RER del peso ideal, **70** ✓ |

Los tres primeros cuadran casi exactos. Los de trabajo, el motor se queda
**por debajo** de SACN5 (175 contra 210 en trabajo moderado).

> **PREGUNTA 5.** Los cinco escalones de actividad los elige el DUEÑO en la
> app, describiendo a su perro. ¿Hay alguna forma mejor de preguntarlo, o
> algún escalón que sobre o falte? Y en concreto: ¿el escalón «trabajo» (175)
> debería llegar a los 210 de «moderate work» de SACN5?

### 1.2 · Crecimiento

Ecuación continua de **Klein et al. (2019)**, *J Anim Physiol Anim Nutr*
103:1952-1958 (grupo de Kienzle, Múnich, 493 cachorros de compañía reales):

```
EM (MJ) = (1,063 − 0,565 × [peso actual / peso adulto esperado]) × peso^0,75
```

✅ **Verificado el 8 de septiembre: esta ecuación ES la de FEDIAF.** Su Tabla
VII-8b la da como `[254.1 − 135.0 × (actual/expected)] × kg^0.75` kcal, que es
la de Klein convertida de MJ (×239) — idéntica — y cita a Klein 2019 como
fuente. O sea que el motor no eligió «Klein en vez de FEDIAF»: usa la de
FEDIAF, que es la de Klein.

Se eligió frente a los escalones clásicos (RER ×3,0 / ×2,5 / ×2,0) porque es
una curva continua, sin saltos al cruzar el 50 % y el 80 % del peso adulto.
Klein también documenta que el NRC 2006 sobreestima ~20 % en menores de 6
meses.

**Si no se conoce el peso adulto esperado**, se cae a los escalones
210/175/140 kcal/kg^0,75. No están en FEDIAF (se comprobó el PDF entero el 6
de septiembre).

⚠️ **VERIFICADO EL 8 DE SEPTIEMBRE: DOS DE LOS TRES SÍ TIENEN FUENTE, Y EL
DE EN MEDIO NO.** SACN5 Tabla 5-2, parte 2 (canina), literal:

> *«Daily energy intake for growing puppies should be 3 x RER from weaning
> until four months of age. At four months of age energy intake should be
> reduced to 2 x RER until the puppy reaches adult size.»*

3 × RER = **210** ✓ · 2 × RER = **140** ✓ · **2,5 × RER = 175 no está en
ninguna parte**: lo pusimos nosotras.

**Y el criterio de corte tampoco es el mismo:** SACN5 corta **por edad** (4
meses); el motor corta **por % del peso adulto** (50 % y 80 %).

> **PREGUNTA 6-bis.** ¿El escalón intermedio de 2,5 × RER tiene sentido
> clínico, o hay que quedarse con los dos de SACN5? ¿Y cortar por edad o por
> % del peso adulto?

> **PREGUNTA 6.** ¿Klein 2019 te parece la referencia correcta para
> crecimiento en una app de consumo? ¿Y el respaldo 210/175/140 cuando no se
> sabe el peso adulto, o preferirías que la app exigiera ese dato?

### 1.3 · Gestación y lactancia

| | Valor | Fuente |
|---|---|---|
| Gestación, primeras 4 semanas | 132 × kg^0,75 | **FEDIAF 2025, Tabla VII-8b** ✅ verificado |
| Gestación, últimas 5 semanas | 132 × kg^0,75 + 26 × kg | **FEDIAF VII-8b** ✅ verificado |
| Lactancia, 1-4 cachorros | 145 × kg^0,75 + 24n × kg × L | **FEDIAF VII-8b** ✅ verificado, letra por letra |
| Lactancia, 5-8 cachorros | 145 × kg^0,75 + [96+12(n−4)] × kg × L | **FEDIAF VII-8b** ✅ verificado |
| L, factor de semana | 0,75 · 0,95 · 1,10 · 1,20 | **FEDIAF VII-8b** ✅ verificado |
| **Tope de ×6 RER** | — | ⚠️ **NUESTRO. FEDIAF no pone ninguno** |

**Verificado el 8 de septiembre contra la Tabla VII-8b de FEDIAF 2025**
(«Average energy requirements during growth and reproduction in dogs»),
literal:

> *1 to 4 puppies: **145 × kg BW^0.75 + 24 n × kg BW × L***
> *5 to 8 puppies: **145 × kg BW^0.75 + [96 + 12 (n−4)] × kg BW × L***
> *n = number of puppies; L = 0.75 in week 1 of lactation; 0.95 in week 2;
> 1.1 in week 3 and 1.2 in week 4*

**Es exactamente lo que hace el motor.** El comentario del código decía que
esta parte venía «de una fuente secundaria que no se ha podido contrastar con
el texto original de FEDIAF» y que era «la parte menos verificada de todo el
DER». **No era cierto**, y ese comentario es lo que hizo que nadie volviera a
mirarlo — y además se usó para justificar un recorte. Corregido.

⚠️ **LO QUE SÍ ES NUESTRO ES EL TOPE DE ×6 RER, Y RECORTA DE VERDAD.** FEDIAF
no pone ningún techo a esa fórmula. El nuestro sale de SACN5 Tabla 5-2, donde
el ×6 **no es un techo general: es la fila de camadas de ≥9 cachorros**. Se
está usando una fila de una tabla indexada por tamaño de camada como si fuera
un límite universal. Medido en semana 4:

| Perra | Cachorros | FEDIAF | Le damos | |
|---|---|---|---|---|
| 25 kg | 6 | 5221 kcal | 4696 | **−10 %** |
| 40 kg | 8 | 9218 kcal | 6680 | **−28 %** |
| 60 kg | 8 | 13 494 kcal | 9054 | **−33 %** |

Una perra de 60 kg con 8 cachorros recibe **un tercio menos** de lo que dice
FEDIAF.

> **PREGUNTA 7.**
> 1. ¿Se quita el tope de ×6 y se sigue a FEDIAF sin más? Es lo que dice la
>    fuente, pero la fórmula escala con el peso vivo y en perras gigantes se
>    va a cifras muy altas.
> 2. Si se mantiene algún techo, **¿cuál, y con qué respaldo?**
> 3. O, por encima de todo: **¿debería la app no dar menú automático en
>    lactancia** y mandar al veterinario? Es la etapa que más se mueve semana
>    a semana y la que peor tolera un error.

### 1.4 · Cómo se decide el peso de referencia

El peso con el que se calculan las kcal **y con el que se escalan los
mínimos** (§3.3) sale de esta escalera, en este orden:

1. **Peso objetivo** si el dueño lo ha puesto.
2. **Peso ideal estimado desde la condición corporal**, si la ha marcado.
3. **Peso real**, si no hay nada mejor.

**El peso ideal desde el BCS se DIVIDE, no se resta:**

```
peso ideal = peso actual / (1 + 0,10 × (BCS − 5))
```

Esto estuvo mal un día y el motivo importa: «30 % overweight» significa un
30 % **por encima del ideal**, no un 30 % del peso de hoy.

- AAHA 2014, Tabla 1: el tercer método —`[peso × (100 − %grasa)] / 0,8`— no
  depende de cómo se lea «overweight» y da ×0,7875 en BCS 8. Dividiendo sale
  ×0,7692 (2 % de diferencia); restando, ×0,70, que se sale del propio rango
  del método de la grasa ya desde BCS 7.
- Global Pet Obesity Initiative 2019 (Ward, German y Churchill; respaldada
  por ECVCN, WSAVA y ACVIM) define obesidad como «30 % above ideal body
  weight» y la equipara a 8/9.

**Dos límites deliberados:**

- **Por debajo de BCS 5 no se estima.** La Tabla 1 de AAHA empieza en BCS 4 y
  no tiene columna de «% underweight», y AAHA 2021 dice lo contrario de
  estimar: *«base feeding calculations on current weight if ideal or
  underweight»*. En un perro delgado el peso de referencia es el suyo.
- **En BCS 9 la cifra (40 %) es un techo, no una medida.** Broome et al.
  2023 (*Sci Rep* 13:22958) observan con DXA perros que *«exceed the
  description for score 9»*, y Bjornvad 2011 no encuentra diferencia de grasa
  entre 8 y 9. Se estima igual, pero se devuelve marcado como cota inferior.

**El adelgazamiento, VERIFICADO por dos fuentes.** A un perro con sobrepeso
el motor le da exactamente el **RER de su peso ideal** (70 × ideal^0,75), o
sea **1,0 × RER**. Coincide con SACN5 Tabla 5-2 («Weight loss = 1.0 x RER») y
es **más estricto** que el «obese prone ≤ 90» de FEDIAF VII-7.

⚠️ **Pero AAHA 2021 dice algo sobre ese nivel que hay que leer:** *«Therapeutic
weight loss diets are recommended for patients undergoing significant calorie
restriction (less than or equal to RER) for weight loss.»* O sea: a ≤ RER,
AAHA recomienda una dieta **terapéutica** — y Rawku no lo es. Ahí es donde la
ventana entre mínimos y máximos se estrecha (§3.3).

⚠️ **Y AAHA 2021 clasifica lo que hace Rawku como factor de riesgo
nutricional.** Su Tabla 4 («Nutritional Screening: Risk Factors») lista
literalmente *«Unconventional diet (e.g., raw meat based, home prepared,
vegetarian, vegan)»* entre los factores que justifican una evaluación
nutricional extendida. No es motivo para no hacerlo; sí para decirlo.

**La escala que ve el dueño es de 5 niveles**, no de 9. La equivalencia es:
0 Muy delgado → BCS 2 · 1 Delgado → BCS 4 · 2 Ideal → BCS 5 · 3 Sobrepeso →
BCS 7 · 4 Obeso → BCS 9.

> **PREGUNTA 8.** ¿La escala de 5 niveles con esa equivalencia te parece
> aceptable, sabiendo que la rellena un dueño mirando a su perro? La
> alternativa es enseñarle la de 9 puntos de Laflamme con dibujos.

> **PREGUNTA 9.** En un perro con BCS 9 damos una estimación que sabemos que
> se queda corta (y por tanto **da menos kcal de las que tocarían para
> adelgazar bien**). ¿Preferirías que no diéramos ninguna y pidiéramos el
> peso objetivo al veterinario?

---

## 2 · La etapa vital

Solo existen tres juegos de requisitos, porque FEDIAF solo publica tres:

| Etapa que elige el dueño | Requisitos que se aplican | Por qué |
|---|---|---|
| Adulto | Adulto | — |
| Senior | Adulto | FEDIAF no le da tabla propia |
| Cachorro <14 semanas | Early Growth | — |
| Cachorro ≥14 semanas | Late Growth | — |
| Gestante | Growth and Reproduction | FEDIAF agrupa gestación y lactancia con crecimiento |
| Lactante | Growth and Reproduction | Íd. |

**Senior lleva un único ajuste**: la proteína mínima sube a **45 g/1000 kcal**
si el valor de adulto fuera menor. FEDIAF eleva la recomendación de 40 a 45
por este motivo. (En la práctica nuestro mínimo de adulto ya es 52,10, así
que hoy no cambia nada.)

> **PREGUNTA 10.** ¿Un senior necesita algo más que subir la proteína?
> ¿Fósforo, sodio, algún antioxidante? Hoy come exactamente como un adulto.

---

## 3 · Los requisitos: FEDIAF 2025, Tabla III-3b

### 3.1 · Qué se verifica

**Los 41 nutrientes de la Tabla III-3b, más el ratio Ca:P, más el calcio de
raza grande: 43 comprobaciones.** Los 12 aminoácidos esenciales incluidos.

Verificado el 8 de septiembre **contra el PDF oficial, renderizando las
páginas como imagen** (no contra el texto extraído, que puede pegar
columnas): **248 comprobaciones, 0 discrepancias.** Se comprueban el valor,
la unidad con su conversión, y que la columna usada sea la de la etapa.

Las conversiones de unidad que aplica el motor, todas comprobadas:

| Nutriente | FEDIAF | Motor | Factor |
|---|---|---|---|
| Vitamina A | UI | µg retinol | ×0,3 |
| Vitamina D | UI | µg | ×0,025 |
| Vitamina E | UI | mg | ×0,67 (α-tocoferol natural, no el acetato sintético) |
| Calcio, fósforo, potasio, sodio, cloruro, magnesio | g | mg | ×1000 |
| Yodo | mg | µg | ×1000 |

**Se usa siempre la columna de adulto más exigente (MER 95 kcal/kg^0,75), no
la de 110.**

### 3.2 · Los máximos, y de dónde sale cada uno

| Nutriente | Máximo (por 1000 kcal) | Origen | Caja |
|---|---|---|---|
| Cobre | 7,00 mg | FEDIAF III-3a, 2,80 **(L)** × 2,5 | **Legal** |
| Yodo | 2750 µg | 1,10 **(L)** × 2,5 | **Legal** |
| Hierro | 170,45 mg | 68,18 **(L)** × 2,5 | **Legal** |
| Manganeso | 42,5 mg | 17,00 **(L)** × 2,5 | **Legal** |
| Selenio | 142,0 µg | 56,80 **(L)** × 2,5 | **Legal** |
| Zinc | 56,75 mg | 22,70 **(L)** × 2,5 | **Legal** |
| Vitamina A | 30 000 µg | 100 000 UI **(N)** × 0,3 | Nutricional |
| **Vitamina D** | **14,1875 µg** | 227 **(L)** × 2,5 × 0,025 | **Legal** — ver abajo |
| Calcio | 6250 mg adulto · 4000 cachorro joven · 4500 crecimiento | III-3b **(N)** | Nutricional |
| Linoleico | 16,25 g, **solo crecimiento temprano** | III-3b **(N)** | Nutricional |
| Lisina | 7,00 g, **solo crecimiento** | III-3b **(N)** | Nutricional — **no se aplica**, §4 |
| Sodio | 3750 mg | **Nota c** de la tabla | Ver abajo |
| Cloruro | 5870 mg | **Nota c** | Ver abajo |

**La vitamina D es el único nutriente con dos máximos** en la III-3a: 227,00
**(L)** y 320,00 **(N)**. Se aplica el legal, que es más estricto. Por eso el
tope es 14,1875 µg y no los 20 µg que saldrían del nutricional.

⚠️ **Sodio y cloruro no tienen máximo en la tabla: tienen una nota.** Literal
de la nota c: *«Scientific data show that sodium levels up to 1.5 % DM
(3.75 g/1000 kcal…) and chloride levels up to 2.35 % DM (5.87 g/1000 kcal…)
are safe for healthy dogs. **Higher levels may still be safe, but no
scientific data are available.**»* O sea: FEDIAF no lo llama máximo. **Usarlo
como techo duro es criterio nuestro**, del lado prudente.

> **PREGUNTA 11.** ¿Está bien tratar el «hasta aquí hay datos» de la nota c
> como un techo que impide entregar el menú? ¿O debería ser un aviso?

**Nutrientes sin máximo en FEDIAF, y el motor no les pone ninguno:** proteína,
grasa, vitamina E, las vitaminas del grupo B, colina, potasio, magnesio,
**fósforo**, linolénico, EPA+DHA, araquidónico y los 12 aminoácidos (salvo el
techo de lisina).

⚠️ **El fósforo llevaba un máximo de 4000 mg desde el primer día del
proyecto, sin fuente, y se quitó el 7 de septiembre.** No lo da FEDIAF (solo
la nota h, informativa y sin cifra), ni NRC 2006 (*«There are insufficient
data on which to base an SUL for P in dogs»*), ni Dobenecker et al. 2021
(*PLOS ONE*, el estudio más centrado en toxicidad de fósforo en perros
adultos sanos: *«no-effect-levels can be defined»* — todavía ninguno).
Recortaba menús reales contra un límite sin origen.

> **PREGUNTA 12 (importante).** El fósforo **no tiene techo** en el motor
> para un perro sano. Un menú BARF va sobrado de fósforo. ¿Es aceptable, o
> pondrías un techo aunque las tres fuentes se abstengan? Si pondrías uno,
> ¿cuál y con qué respaldo?

### 3.3 · Los mínimos se escalan cuando el perro come poco

FEDIAF publica los mínimos de adulto en **dos columnas**, para un MER de 95 y
de 110 kcal/kg^0,75. Un perro que come menos kcal necesita más concentración
de cada nutriente para llegar a la misma cantidad absoluta. El motor
interpola/extrapola entre esas dos columnas (ecuación 7.2.5 de FEDIAF) y se
queda con **el mayor de los dos anclajes escalados** — en magnesio y cloruro
gana el de 110, en selenio y calcio el de 95.

**Reglas, y las tres son deliberadas:**

- **Solo hacia arriba.** No hay base en FEDIAF para bajar el mínimo de un
  perro que come más.
- **Solo en adulto.** Para crecimiento, gestación y lactancia FEDIAF publica
  otras columnas y la ecuación no está verificada ahí.
- **La grasa está exenta**: FEDIAF publica 13,75 g en las dos columnas.
  Escalarla haría que las kcal dejaran de cerrar.
- **Los máximos no escalan nunca** — son concentración, no cantidad.

**Consecuencia que hay que conocer:** la ventana entre mínimo y máximo **se
cierra según bajan las kcal**. En dieta húmeda el **selenio se cruza en DER
45,2 kcal/día**: por debajo de eso, el mínimo escalado supera el máximo legal
y no existe ninguna ración posible. El motor lo detecta y lo dice con nombre
y números, en vez de dar el «quita alguna restricción» de siempre.

> **PREGUNTA 13.** Ese cruce afecta a perros muy pequeños (unos 1,5-2 kg con
> poca actividad). Hoy se les dice que no se puede. ¿Es la respuesta
> correcta, o hay alguna salida clínica que no estamos viendo?

---

## 4 · Los aminoácidos, y la única excepción del motor

Los 12 esenciales de la Tabla III-3b se verifican los 12.
`metionina+cistina` y `fenilalanina+tirosina` se calculan como suma.

**La única excepción escrita de todo el motor: el techo de lisina no se
aplica.**

- FEDIAF pone un máximo de **7,00 g/1000 kcal, solo en crecimiento**.
- **0 de 15 menús de cachorro caben debajo.** La lisina va detrás de la
  proteína, y una ración BARF de cachorro lleva ~134 g de proteína/1000 kcal
  contra un mínimo de 50.
- Aplicarlo dejaría **a todos los cachorros sin menú**.
- El **mínimo** de lisina sí se aplica. Solo se quita el techo.

> **PREGUNTA 14 (la que más falta hace de este apartado).** El techo de
> lisina, ¿está pensado para una dieta con la proteína ajustada al mínimo, y
> por eso no es transferible a una ración cruda? ¿O estamos midiendo algo
> distinto de lo que él mide? Es el único máximo de FEDIAF que no aplicamos.

**Huecos de datos:** faltan **16 aminogramas** en el catálogo (once
suplementos comerciales, más la laringe de vacuno, que va vacía a propósito
por ser cartílago). El motor vigila que **la proteína sin aminograma no pase
del 5 % de un menú real**.

---

## 5 · Los ácidos grasos

| | Mínimo adulto | Fuente |
|---|---|---|
| Linoleico (ω-6) | 3,82 g | FEDIAF |
| Linolénico (ω-3) | — (solo crecimiento: 0,20 g) | FEDIAF |
| Araquidónico | — (solo crecimiento: 75 mg) | FEDIAF |
| **EPA + DHA** | **0,11 g** | **NRC 2006 — NO es de FEDIAF** |

⚠️ **El mínimo de EPA+DHA de adulto es criterio nuestro.** FEDIAF 2025 solo
lo exige en crecimiento y reproducción (0,13 g) y para adulto dice literalmente
que *«the current information is insufficient to recommend a specific level of
omega-3 fatty acids for adult dogs»*. Los 110 mg/1000 kcal vienen del NRC 2006
y se adoptaron a propósito por relevancia clínica documentada.

**El máximo de EPA+DHA no se aplica por menú, sino al promedio de la semana.**
FEDIAF deja la columna vacía. Los 2800 mg de Lenox & Bauer (*JVIM*
2013;27:217-226) son el **SUL del NRC 2006**, o sea una concentración de la
**dieta habitual crónica**, no el tope de un plato. Puesto por menú, **18 de
los 20 pescados del catálogo lo pasan ellos solos** (del pulpo, 2527, al
boquerón, ~11 000), porque el pescado tiene mucho omega-3 y pocas calorías:
un día entero borró el pescado azul de la app, de 13 menús con pescado de
cada 24 a 4. Ahora vive donde dice la fuente: en el promedio de la rotación
semanal.

**Trampa de datos que vigilamos:** `linoleico` es **omega-6** y `linolenico`
es **omega-3**. Se diferencian en una letra, son cosas opuestas, y si se
cargan cambiados **no salta nada**: el menú sale verde igual. Hay una prueba
dedicada, y una auditoría que señala los nueve alimentos donde el omega-3
supera al omega-6.

> **PREGUNTA 15.** ¿Mantenemos el mínimo de EPA+DHA de adulto del NRC, lo
> subimos, lo bajamos, o lo convertimos en recomendación en vez de requisito
> duro?

> **PREGUNTA 16.** ¿El SUL de 2800 mg aplicado al **promedio semanal** es la
> lectura correcta de «concentración de la dieta habitual»? ¿O el promedio
> debería ser de más días?

---

## 6 · El ratio Ca:P y el calcio del cachorro de raza grande

**El ratio Ca:P se comprueba como una restricción propia**, no como
consecuencia del calcio y el fósforo por separado: se puede tener los dos
bien y el ratio mal.

| Etapa | Mínimo | Máximo | Fuente |
|---|---|---|---|
| Adulto | 1/1 | **2/1** | FEDIAF III-3b |
| Cachorro <14 sem | 1/1 | **1,6/1** | Íd. |
| Cachorro ≥14 sem, **raza pequeña** (<15 kg adulto) | 1/1 | **1,8/1** | Íd., nota **a** |
| Cachorro ≥14 sem, **raza grande** (>15 kg adulto) | 1/1 | **1,6/1** | Íd., nota **b** |

⚠️ **La fila de raza grande se añadió el 8 de septiembre y antes no
existía.** La nota b manda **dos** cosas y solo estaba puesta una. Literal:

> *«For puppies of breeds with adult body weight over 15 kg, until the age of
> about 6 months. Only after that time, calcium can be reduced to 0.8 % DM
> (2 g/1000 kcal or 0.48 g/MJ) **and the calcium-phosphorus ratio can be
> increased to 1.8/1**.»*

El mínimo de calcio reforzado (**2500 mg/1000 kcal** en vez de 2000) estaba
desde agosto. El techo del ratio (1,6 en vez de 1,8) no estaba en ningún
sitio. **Y las dos mitades tiran en sentidos opuestos**: subir el calcio
empuja el ratio hacia arriba, así que aplicar solo una deja al perro justo
del lado malo.

**Medido antes de corregirlo: 0 de 32 menús de cachorro de raza grande caían
entre 1,6 y 1,8** (el peor, 1,49). El agujero era real en las reglas y no
estaba dando menús malos. Se cerró igual.

**Los dos valores se aplican a toda la fase de crecimiento**, no solo hasta
los 6 meses: el motor no distingue esa sub-fase, y quedarse con el valor más
exigente es el lado seguro.

> **PREGUNTA 17.** ¿Es correcto aplicar el requisito reforzado de raza grande
> a **toda** la fase de crecimiento tardío, en vez de solo hasta los ~6 meses
> como dice la nota b? Es más estricto que la fuente, a propósito.

> **PREGUNTA 18.** El umbral de «raza grande» es **15 kg de peso adulto
> esperado**, que es lo que dicen las notas a y b. ¿Hay algún matiz por raza
> (gigantes vs. grandes) que deberíamos recoger?

---

## 7 · Los topes de seguridad crónica y las reglas por alimento

**Son restricciones duras dentro del solver, no avisos posteriores.** Un
aviso se puede ignorar; esto no.

Y aquí está la parte más honesta del motor, escrita en su propia cabecera:
**los mecanismos están documentados con estudios reales; los números de corte
los pusimos nosotras.**

| Regla | Umbral | Mecanismo (fuente sólida) | El número |
|---|---|---|---|
| **Tiaminasa** (sardina, caballa, arenque, boquerón, carpa, atún, gamba, langostino) | ≤10 % de las kcal del día | Markovich, Heinze & Freeman 2013, *JAVMA* 243(5):649 | ⚠️ **Nuestro.** La literatura dice «proporción sustancial de la dieta», sin cifra |
| **Mercurio** (atún) | ≤10 % de las kcal del día | Merck Vet Manual; datos FDA de contenido real | ⚠️ **Nuestro**, extrapolado de la dosis de referencia humana de la EPA. **No existe límite canino**: lo dice Dunham-Cheatham et al. 2019, *Sci Total Environ* 684:276-280 |
| **Vitamina D** | 2,6 µg/kg^0,75 y 20 µg/1000 kcal | Lenox & Bauer 2013; NRC 2006 | De fuente |
| **Yodo** | 1400 µg/1000 kcal (+50 % de margen si viene de kelp) | NRC 2006 | De fuente |
| **Selenio** | 570 µg/1000 kcal | AAFCO (= 2 mg/kg MS de Merck) | De fuente |
| **EPA+DHA semanal** | 2,8 g/1000 kcal de promedio | NRC 2006 vía Lenox & Bauer | De fuente |
| **Clara de huevo cruda** | ≤5 % del peso | Avidina/biotina | ⚠️ **El ÚNICO con daño medido** (al 20 %) |
| **Hígado** | ≤10 % del peso | Vitamina A | ⚠️ Nuestro |
| **Vísceras metabólicas** (hígado + riñón) | ≤10 % del peso | — | ⚠️ Nuestro |
| **Oxalato** (espinaca, acelga, ruibarbo, remolacha) | libre en sano · **0 con antecedente** | — | ⚠️ Nuestro |
| **Tejido tiroideo** (cuellos, laringe, tráquea, esófago, garganta) | **excluido** | Tirotoxicosis alimentaria | De fuente |
| **Borraja** | excluida | — | De fuente |

**Todos son diarios y no admiten balance semanal**, salvo el de EPA+DHA: una
tiaminasa no se «compensa» el jueves.

### 7.1 · Verificado el 8 de septiembre: tres de los cinco no pueden activarse nunca

Los cinco «topes de seguridad crónica» son, según la regla 2 del `CLAUDE.md`,
restricciones duras dentro del solver. **Puestos en la misma unidad que el
máximo de FEDIAF que el motor ya aplica, tres de ellos están por encima**, así
que no pueden morder jamás:

| Tope crónico | Valor | Máximo de FEDIAF ya aplicado | |
|---|---|---|---|
| Vitamina D (por kcal) | 20 µg/1000 kcal | **14,19 µg** (legal) | ❌ **nunca se activa** |
| Vitamina D (por peso metabólico) | 2,6 µg/kg^0,75 ≈ 23,2 µg/1000 kcal | **14,19 µg** | ❌ **nunca se activa** |
| Selenio | 570 µg/1000 kcal | **142 µg** (legal) | ❌ **nunca se activa** (4× más permisivo) |
| Yodo | 1400 µg/1000 kcal | 2750 µg (legal) | ✅ este sí manda |

**Esto no deja a ningún perro desprotegido** —lo que protege es el máximo
legal de FEDIAF, que es más estricto— pero **la documentación dice que
protegen y no protegen**. Si mañana alguien tocara un máximo de FEDIAF
pensando que «ya está el tope crónico debajo», no hay nada debajo.

*(Para la vitamina D esto ya estaba escrito en el `nota_auditoria` de su fila
desde el 6 de septiembre. Para el selenio, no.)*

### 7.2 · Y dos cifras están mal atribuidas al NRC

**El yodo, que es el único de los tres que sí actúa, usa como techo el nivel
en el que se midió DAÑO.** NRC 2006, literal:

> *«Castillo et al. (2001a) reported **evidence of depressed thyroid gland
> function**, evidenced by reduced plasma concentrations of thyroid hormones
> and **bone abnormalities**, in puppies fed diets containing an estimated
> maximum I content of **1,400 μg I per 1,000 kcal ME**… Based on this
> information **an absolute figure for a SUL of dietary I cannot be predicted
> for adult dogs**.»*

O sea: **el NRC no da un SUL de yodo**, dice expresamente que no se puede
predecir, y los 1400 son el nivel al que unos cachorros mostraron función
tiroidea deprimida y alteraciones óseas. **El motor usa ese mismo número como
techo**, citando «NRC 2006».

**El selenio también.** NRC 2006, literal:

> *«**no data are available on an acceptable SUL for dietary Se in dogs**
> although for regulatory purposes, a maximum standard of **2.0 mg Se·kg–1**
> has been suggested (AAFCO, 2001).»*

2,0 mg/kg a 4000 kcal/kg son **500 µg/1000 kcal**, no los 570 que tiene el
motor. (Da igual en la práctica, porque el legal de 142 manda de todos modos.)

> **PREGUNTA 19-bis (bloqueante, y es la que más nos preocupa de todo el
> apartado 7).** El techo de yodo del motor **es el nivel al que la fuente
> documenta daño en cachorros**. Un techo de seguridad debería estar por
> debajo de eso, con su factor de seguridad. **¿Qué cifra ponemos?** Y como el
> NRC dice que no se puede predecir un SUL: ¿nos quedamos con el límite legal
> de FEDIAF (2750), que es todavía más alto, o ponemos un criterio nuestro
> declarado y más bajo?

> **PREGUNTA 19-ter.** ¿Merece la pena mantener los topes de vitamina D y
> selenio de `seguridad.py`, sabiendo que el límite legal de FEDIAF es
> siempre más estricto y que nunca llegan a actuar? La alternativa es
> quitarlos y dejar escrito que quien protege es FEDIAF.


> **PREGUNTA 19 (bloque entero).** De los seis umbrales marcados como
> criterio nuestro, ¿alguno está mal puesto, en un sentido o en el otro? Y
> sobre todo: **¿alguno debería depender del caso** —o sea, ser un rango con
> palanca del veterinario— en vez de ser una constante igual para todos?

> **PREGUNTA 20.** El del mercurio nos preocupa especialmente: es una
> extrapolación desde una dosis de referencia **humana**, y la fuente dice
> expresamente que no hay límite canino. ¿Lo dejamos, lo cambiamos, o lo
> convertimos en aviso?

---

## 8 · Las patologías: 40 perfiles, 19 límites numéricos

Los topes por patología **son más estrictos que FEDIAF** y se miden sobre las
**kcal reales del menú**, no las pedidas — el menú puede salir un 3 % por
debajo, y menos kcal con el mismo nutriente es más concentración.

**Regla que se comprueba automáticamente:** ninguna patología formulable
puede tener un tope **por debajo** del mínimo de FEDIAF. Si lo tiene, eso ya
no es un tope: es una dieta de prescripción, y va marcada como no formulable
automáticamente.

### 8.1 · Los 19, verificados uno a uno contra su capítulo

**Verificado el 8 de septiembre abriendo cada capítulo de SACN5 y leyendo la
tabla citada.** «Convertido» = el valor de la fuente pasado a g o mg por 1000
kcal con el puente de 4000 kcal/kg MS (§0.1).

| Patología · nutriente | Motor | Lo que dice la fuente | Convertido | |
|---|---|---|---|---|
| renal · fósforo | ≤ 1200 mg | SACN5 37-9: *«Phosphorus 0.2 to 0.5% in foods for dogs»* | 500-1250 | ✅ dentro, extremo alto |
| renal avanzada · fósforo | ≤ 1200 mg | Íd. | 500-1250 | ✅ |
| pancreatitis · proteína | ≤ 75 g | SACN5 67-3: *«Protein 15 to 30% for dogs»* | 37,5-75 | ✅ extremo alto |
| **pancreatitis · grasa** | **≤ 20 g** | Merck: *«less than 20 g fat/1,000 kcal»*. SACN5 67-3: *«≤15%»* no obeso, *«≤10%»* obeso | 37,5 / 25 | ⚠️ **más estricto que las dos cifras de SACN5** |
| oxalato · vitamina D | ≤ 14,19 µg | FEDIAF III-3a, 227 **(L)** legal | 14,19 | ✅ exacto |
| **hepatopatía · cobre** | **≤ 2,4 mg** | Center 2026 JAVMA. **SACN5 68-8: *«Copper ≤5 mg/kg»* MS**, y en el texto *«less than 5 ppm DM»* | **1,25** | ⚠️ **el doble de permisivo que SACN5** |
| **cardiopatía (genérica)** | **≤ 900 mg Na** | ACVIM 2019. **SACN5 36-4: perros, Class Ia 0,15-0,25 % MS; Ib/II/III 0,08-0,15 %** | **375-625 / 200-375** | ⚠️ **1,4× más permisivo que el techo de SACN5** |
| cardiopatía B2 | ≤ 900 mg Na | Íd. | Íd. | ⚠️ íd. |
| cardiopatía C | ≤ 790 mg Na | Íd. | Íd. | ⚠️ íd. |
| cardiopatía D | ≤ 480 mg Na | Íd. | Íd. | ✅ dentro de Class Ia |
| hiperlipidemia · grasa | ≤ 30 g | SACN5 28: *«Restrict dietary fat (<12% dry [matter])»* | 30 | ✅ **exacto** |
| hiperlipidemia · fibra | ≥ 25 g | SACN5 28: *«Dogs: ≥10% DM»* | 25 | ✅ **exacto** |
| **obesidad · grasa** | **≤ 30 g** | SACN5 27-4: *«Foods for weight loss should contain ≤9%»* | **22,5** | ⚠️ **más permisivo — declarado y medido, ver abajo** |
| MCD · taurina | ≥ 250 mg | SACN5 36-4: *«Dogs: ≥0.1%»* | 250 | ✅ **exacto** |
| MCD · L-carnitina | ≥ 50 mg | SACN5 36-4: *«Dogs: ≥0.02%»* | 50 | ✅ **exacto** |
| PLE · grasa | ≤ 37,5 g | SACN5 58: *«<15% for dogs and cats»* | 37,5 | ✅ **exacto** |
| EPI · grasa | ≤ 37,5 g | SACN5 66-1: *«Fat 10 to 15% for dogs»* | 25-37,5 | ✅ extremo alto |
| artrosis · EPA+DHA | ≥ 1,0 g | SACN5 34-2: *«0.4 to 1.1% DM»* | 1,0-2,75 | ✅ extremo bajo |
| dermatosis zinc · zinc | ≥ 25 mg | SACN5 32-1: *«Dogs: 100 to 200 mg/kg food DM»* | 25-50 | ✅ extremo bajo |

**Resultado: 13 de 19 caen exactos o dentro del rango de su fuente.** Cuatro
discrepan y dos de esos cuatro son la misma familia (cardiopatía).

### 8.1-bis · Los cuatro que discrepan, y por qué

**1 · Obesidad · grasa: 30 donde SACN5 dice 22,5.** Está **declarado en el
propio dato** y con la medida al lado: 22,5 —y hasta 27— **no dan menú** con
el catálogo real ni en 40 s de reintentos, porque una comida de verdad, sin
premezcla vitamínica sintética, no puede bajar tanto la grasa y seguir
llegando a los mínimos de ácidos grasos esenciales y micronutrientes con las
kcal que quedan. El 30 se apoya en la otra fila de la misma Tabla 27-4:
*«Foods for prevention of weight regain should contain ≤14%»* = 35, así que
30 queda dentro de esa franja. **Es honesto, pero es un límite de máquina
vestido de límite clínico.**

**2 · Hepatopatía · cobre: 2,4 donde SACN5 dice 1,25.** Dos fuentes que no
dicen lo mismo: SACN5 cap. 68 Tabla 68-8 da **≤5 mg/kg MS** (y el texto
insiste: *«a low-copper (<5 mg/kg, dry matter) veterinary…»*, *«less than 5
ppm DM copper»*), que son 1,25 mg/1000 kcal; Center et al. 2026 (*JAVMA*
264(2):171-180) da 0,24 mg/100 kcal = 2,4. **Se usa la más nueva.** Hoy no
tiene efecto práctico —la hepatopatía bloquea la formulación automática antes
de llegar al tope— pero el número está ahí.

**3 y 4 · Cardiopatía · sodio.** También dos fuentes que no coinciden.
SACN5 36-4 da, para perro, **0,15-0,25 % MS** en clase Ia (375-625
mg/1000 kcal) y **0,08-0,15 %** en Ib/II/III (200-375). Nuestros topes —900
en la genérica y en B2, 790 en C, 480 en D— **están por encima del techo de
SACN5 en los tres primeros**; solo el de estadio D cae dentro. La fuente que
usamos es el consenso ACVIM 2019, veinte años más nuevo y específico de
cardiología, que trabaja con una escala por estadios distinta de las clases
de SACN5.

> **PREGUNTA 21-bis (bloqueante).** En los tres casos de arriba tenemos dos
> fuentes que no dicen lo mismo, y hemos elegido una sin que nadie lo firme:
> 1. **Cobre en hepatopatía**: ¿Center 2026 (2,4) o SACN5 (1,25)?
> 2. **Sodio en cardiopatía**: ¿ACVIM 2019 por estadios, o las clases de
>    SACN5, que son bastante más estrictas? Es el que más perros toca.
> 3. **Obesidad**: el 30 es lo que la máquina puede hacer, no lo que dice la
>    fuente. ¿Se acepta y se declara como «lo mejor alcanzable con comida
>    real», o hay que decirle al dueño que para adelgazar de verdad hace
>    falta otra cosa?

### 8.1-quater · Y contra el reglamento europeo de alimentos dietéticos

**Encontrado el 8 de septiembre, y es la pieza que faltaba.** FEDIAF dice en su
propio alcance que sus recomendaciones son las del **alimento completo para un
animal sano**, y que *«excluded from the FEDIAF's Nutritional Guidelines are
pet foods for particular nutritional purposes»*. Esa categoría tiene su propia
ley: el **Reglamento (UE) 2020/354**, cuyo Anexo B da, para cada motivo
clínico, **la característica nutricional esencial con su cifra, el tiempo
recomendado de uso y la advertencia veterinaria**.

Es decir: **existe una lista legal europea de en qué casos un alimento puede
salirse de FEDIAF, con qué número y durante cuánto.** Ver `DECISIONES.md`
D-12.

**La fuente está guardada** en `canislab-fuentes/Reglamento_UE_2020_354/`:
el PDF oficial del Diario Oficial en castellano y en inglés, el texto extraído,
y una `LECTURA.md` con las 20 entradas caninas entrada por entrada.

**Cómo se convierten sus cifras — y no es cosa nuestra, lo manda la norma.**
Van por kg de pienso completo al 12 % de humedad, y su nota al pie (2) dice:
*«based on a diet with a dry matter energy density of 4000 kcal Metabolisable
Energy/kg calculated using the equation described in the FEDIAF Nutritional
Guidelines… **the values shall be adapted if the energy density deviates**»*.
0,88 kg MS × 4000 kcal = 3520 kcal/kg de pienso → **valor ÷ 3,52**. Con una
trampa: la nota **(12)** cambia la base a 3500 kcal/kg MS (**÷ 3,08**) y en la
lista canina la usa **solo la entrada 22, hiperlipidemia**.

*(Corrección: la primera versión de esta tabla aplicó 3,52 también a la grasa y
dio 31,25 g. La cifra correcta es **35,7 g**. La conclusión no cambia.)*

**Las 20 entradas caninas, y qué hace el motor con cada una.** «—» = la norma no
pone cifra, solo una propiedad cualitativa.

| Nº | Objetivo del Reg. 2020/354 (perro) | Cifra legal | Por 1000 kcal | El motor | |
|---|---|---|---|---|---|
| 10 | Renal · fósforo | ≤ 5 g/kg | 1420 mg | 1200 | ✅ más estricto |
| 10 | **Renal · proteína cruda** | **≤ 220 g/kg** | **62,5 g** | **no existe** | ❌ **falta** |
| 11 | Oxalato · calcio y vit. D bajos, orina alcalina | — | — | vitD 14,19 µg | ⚠️ la ley no da cifra |
| 12 | **Diabetes · azúcares totales** | **≤ 62 g/kg** | **17,6 g** | no existe | ⚠️ una ración cruda casi no los lleva |
| 13 | Intolerancias · fuentes limitadas/hidrolizadas | — | — | exclusiones y alergias | ✅ cualitativo, cubierto |
| 14 | **Cistina · proteína** | ≤ 160 g/kg · o · ≤ 220 | **45,5 g** · o · **62,5 g** | bloquea | ⚠️ la vía B no baja de FEDIAF |
| 15 | **Convalecencia · proteína (suelo)** | ≥ 250 g/kg | **71,0 g** | **no existe la etapa** | ❌ **falta** |
| 16 | Urato · proteína (vía A) | ≤ 130 g/kg | 36,9 g | bloquea | ✅ 36,9 < 52,1: es prescripción |
| 16 | **Urato · proteína (vía B)** | ≤ 220 g/kg + fuentes bajas en purinas | **62,5 g** | bloquea | ⚠️ **esta vía NO baja de FEDIAF** |
| 17-18 | **Estruvita · magnesio** | ≤ 1,8 g/kg | **511 mg** | no existe | ❌ **falta** |
| 19 | Maldigestión / IPE · digestibilidad | — | — | grasa ≤ 37,5 g | ⚠️ la ley no pone cifra de grasa |
| 20 | **Absorción intestinal · Na y K (suelos)** | ≥ 1,8 y ≥ 5 g/kg | **511 y 1420 mg** | grasa ≤ 37,5 g | ⚠️ palanca distinta |
| 21 | Diarrea aguda | (pienso complementario) | — | **no existe** | ❌ fuera de alcance hoy |
| 22 | Hiperlipidemia · grasa | ≤ 110 g/kg **(base 3500)** | **35,7 g** | 30 | ✅ más estricto |
| 23 | **Hepática · proteína cruda** | ≤ 279 g/kg | **79,3 g** | no existe | ❌ **falta** |
| 24 | **Cardíaca · sodio** | **≤ 2,6 g/kg** | **739 mg** | 900 · 900 · 790 · 480 | ❌ **tres por encima** |
| 25 | Adelgazamiento · densidad energética | < 3060 kcal/kg | (densidad) | grasa ≤ 30 g | ⚠️ palanca distinta |
| 26 | **Dermatosis · LA y EPA+DHA (suelos)** | LA ≥ 12,3 + EPA+DHA ≥ 2,9 g/kg · o · LA ≥ 18,5 + EPA+DHA ≥ 0,39 | **3,49 + 0,82 g** · o · **5,26 + 0,111 g** | zinc ≥ 25 mg | ❌ **falta** |
| 27 | **Artrosis · omega-3 totales y EPA** | ω-3 ≥ 29 g/kg **y** EPA ≥ 3,3 g/kg | **8,24 g** y **0,94 g** | EPA+DHA ≥ 1,0 g | ⚠️ el EPA encaja; **el ω-3 total, no** |
| 28 | Cobre en hígado | ≤ 8,8 mg/kg | 2,50 mg | 2,40 | ✅ más estricto |
| 30 | Estrés · caseína hidrolizada | 1-3 g/kg | (aditivo) | **no existe** | ❌ fuera de alcance hoy |

**Cobertura: 17 de los 20 objetivos caninos** tienen una patología equivalente en
el motor. Los tres que faltan son **convalecencia (15)**, **diarrea aguda (21)** y
**estrés (30)**; los dos últimos son discutiblemente producto y no motor, pero el
primero no.

**Siete cosas que salen de aquí:**

1. **El cobre hepático queda resuelto a favor de lo que ya teníamos.** Center
   2026 daba 2,4 y SACN5 1,25; el reglamento europeo permite hasta 2,50. Los
   2,4 del motor son legales y más estrictos.
2. **El sodio cardíaco no.** Ahora hay tres cifras: SACN5 200-625, el
   reglamento **739**, y las nuestras 900/900/790/480. Las tres primeras
   nuestras están por encima del techo legal-dietético europeo.
3. **Faltan dos techos de proteína que son perfectamente implementables**:
   renal 62,5 y hepática 79,3 g/1000 kcal. Los dos quedan **por encima** del
   mínimo de FEDIAF (52,1), o sea que **no hacen falta prescripción ni firma**
   — y una ración BARF sin ajustar va por ~130, así que morderían de verdad.
4. **El urato tiene una segunda vía legal que no exige bajar de FEDIAF**
   (≤220 g/kg con fuentes seleccionadas = 62,5). Hoy lo bloqueamos entero
   porque la carga de purinas de una ración cruda está muy por encima de
   cualquier objetivo; pero el reglamento ataca el problema por la proteína y
   la selección de fuentes, no por las purinas. Lo mismo vale para la
   **cistina** (entrada 14, ≤220 g/kg con fuentes bajas en cistina).
5. **La artrosis se queda corta por el lado que no miramos.** El motor pide
   EPA+DHA ≥ 1,0 g/1000 kcal, y la ley pide EPA ≥ 0,94 — encaja — **pero además
   pide omega-3 totales ≥ 8,24 g**, que no comprobamos en absoluto.
6. **La estruvita tiene una cifra legal implementable y no la usamos**: magnesio
   ≤ 511 mg/1000 kcal. Hoy la patología está en «no formulable» sin ningún tope.
7. **La pancreatitis no está en el reglamento.** Ni en FEDIAF. La entrada 19
   cubre la insuficiencia pancreática **exocrina**, que es otra cosa, y no pone
   cifra de grasa. O sea: **para la pancreatitis no hay número oficial de
   ninguna de las dos referencias normativas**, y por la regla adoptada
   (FEDIAF manda; donde FEDIAF no llega, SACN5) el número tendría que ser el de
   SACN5 (37,5 g no obeso / 25 g obeso), no los 20 g de Merck que aplica hoy el
   motor. Ver §8.2, que es donde esto se decide.

**Y dos frases del reglamento que respaldan reglas que el motor ya tenía**, y que
conviene que veas porque son las que sostienen todo lo demás:

- **Un techo terapéutico no autoriza a bajar de los mínimos de FEDIAF** — nota al
  pie (11): *«The minimum recommendations according to the FEDIAF Nutritional
  Guidelines for all essential fatty acids shall be met in the daily ration.»*
- **Con dos patologías se cumplen los dos topes** — parte A, punto 7: *«it shall
  comply with each respective entry in Part B»*. No se promedian ni se elige el
  menos malo: por eso renal + pancreatitis, cuando no caben juntos, **dice qué
  dos límites chocan** en vez de aflojar uno.

**Lo que el reglamento NO contesta, dicho con precisión** porque es fácil citarlo
de más: **no da, por patología y por nutriente, un rango con un extremo que tú
puedas mover.** Da una sola característica esencial por objetivo — casi siempre un
techo, a veces un suelo — y te asigna un papel distinto y explícito, el de decidir
**empezar** y decidir **prolongar**: *«It is recommended that advice from a
veterinarian be sought before use and before extending the period of use»*. Lo que
la norma pone como rango es **el tiempo**, no la cifra. El único porcentaje del
texto, el ±15 % de la parte A punto 2, es **tolerancia analítica de fabricación**,
no margen clínico. Así que la pregunta de hasta dónde se puede mover cada número
sigue siendo tuya, y sigue siendo la PREGUNTA 22.

> **PREGUNTA 21-quater (bloqueante).**
> 1. **Sodio cardíaco: ¿nos bajamos a los 739 del reglamento europeo?** Es más
>    estricto que lo nuestro en tres de las cuatro entradas.
> 2. **¿Añadimos los techos de proteína de renal (62,5) y hepática (79,3)?**
>    No requieren firma y hoy no existen.
> 3. **Urato y cistina: ¿la vía de «proteína ≤220 + fuentes seleccionadas» es
>    viable con comida real**, o la carga de purinas / cistina la tumba igual?
> 4. **Artrosis: ¿añadimos el suelo de omega-3 totales (8,24 g/1000 kcal)?**
>    Hoy solo comprobamos EPA+DHA ≥ 1,0 y ese lado sí encaja.
> 5. **Estruvita: ¿añadimos el techo de magnesio (511 mg/1000 kcal)** y la
>    pasamos a formulable, o sigue bloqueada?
> 6. **Convalecencia (suelo de proteína 71 g/1000 kcal): ¿es una etapa que
>    debería existir?** Es el único de los tres objetivos legales que faltan
>    que parece nuestro.

### 8.1-ter · Lo que las mismas tablas piden y el motor NO aplica

Al leer las tablas enteras —no solo la fila del nutriente que ya teníamos—
aparecen factores que el motor no implementa:

| Tabla | Factor que falta | Lo que dice | Convertido |
|---|---|---|---|
| SACN5 27-4 (obesidad) | **Fibra** | *«Foods for weight loss should contain 12 to 25%»* | 30-62,5 g/1000 kcal |
| SACN5 27-4 (obesidad) | **Proteína** | *«…should contain ≥25%»* | ≥62,5 g/1000 kcal |
| SACN5 27-4 (obesidad) | Densidad energética | *«≤3.4 kcal ME/g»* MS | otra base |
| SACN5 36-4 (cardiopatía) | **Fósforo** | *«Dogs: 0.2 to 0.7%»* | 500-1750 mg/1000 kcal |
| SACN5 36-4 (cardiopatía) | Cloruro | *«1.5 x sodium levels»* | ligado al sodio |

Dos de ellos importan de verdad: **la proteína en el adelgazamiento** (subir
la proteína mientras se recortan kcal es lo que protege la masa magra, y el
motor solo aplica el mínimo de FEDIAF, 52,1, por debajo de los 62,5 de SACN5)
y **la fibra**, que es la que da saciedad.

*(El potasio y el magnesio cardíacos de esa misma tabla —≥0,4 % y ≥0,06 % MS—
sí quedan cubiertos: los mínimos de FEDIAF, 1450 mg y 200 mg/1000 kcal, son
0,58 % y 0,08 % MS, por encima de los dos.)*

> **PREGUNTA 21-ter.** ¿Cuáles de estos cinco hay que añadir? La proteína en
> obesidad es la que más nos preocupa.

### 8.2 · El caso que más falta hace resolver: la grasa en pancreatitis

**Es el ejemplo de manual de una constante que debería ser un rango, y no es
teórico: es lo que deja sin comer a un perro.**

Tres cifras conviven, y las tres tienen fuente:

| Cifra | Unidad original | Fuente, literal |
|---|---|---|
| **20 g/1000 kcal** | ya en g/1000 kcal | Merck Vet Manual: *«feeding a low-fat diet (ie, **less than 20 g fat/1,000 kcal**) is crucial for treatment success»* |
| **≤15 % MS** = 37,5 g/1000 kcal | materia seca | SACN5 cap.67 Tabla 67-3: *«≤15% for non-obese and non-hypertriglyceridemic dogs»* |
| **≤10 % MS** = 25 g/1000 kcal | materia seca | Íd.: *«≤10% for obese and/or hypertriglyceridemic dogs»* |

**El motor aplica 20, que es más estricto que las dos cifras de SACN5.** Y eso
tiene una consecuencia medida el 8 de septiembre (adulto 25 kg, DER 1200,
recorriendo los seis peldaños de relajación de la forma de la ración):

| | ¿Sale menú? |
|---|---|
| `renal` sola | **sí** |
| `pancreatitis` sola | **sí** |
| **`renal` + `pancreatitis`** | **NO**, en ninguno de los seis peldaños |
| … soltando solo el fósforo renal (1200) | **sí** |
| … soltando solo la grasa de pancreatitis (20) | **sí** |
| … con la grasa a 25 (SACN5, perro obeso) | no |
| … con la grasa a **37,5** (SACN5, perro no obeso) | **sí** |

No es un problema de tiempo de cálculo: el solver lo declara imposible en
0,1 segundos. **Los dos límites que chocan son el fósforo renal ≤1200 y la
grasa de pancreatitis ≤20**, y el motor ya lo dice con esas palabras desde el
8 de septiembre, en vez del «quita alguna restricción» de antes.

Fíjate en lo que significa: **elegir Merck en vez de SACN5 es lo que deja sin
menú a un perro renal con pancreatitis.** Eso es una decisión clínica, y hoy
la toma el software.

> **PREGUNTA 21 (la más importante de todo el documento).**
> 1. ¿El objetivo de grasa en pancreatitis canina es **un número o un
>    rango**? Si depende del caso —episodio agudo vs. crónico, triglicéridos,
>    obesidad concurrente— dinos **qué variable lo mueve y entre qué y qué**,
>    y lo implementamos como rango con palanca del veterinario, con el 20
>    como punto de partida.
> 2. Y mientras tanto: **¿qué se le dice a un perro renal con pancreatitis?**
>    Hoy no recibe menú.

### 8.3 · Los siete límites que interpretamos nosotras

Hay un trabajo empezado (sin fusionar todavía) que estructura, para cada uno
de los 19, **hasta dónde podría moverlo un profesional**. De los 19, **doce
salen de un rango escrito en la fuente**. Los otros **siete los pusimos
nosotras**, y hay un patrón: *la fuente da un solo número y usamos el mínimo
de FEDIAF como la otra punta*. **Eso no es lo mismo**: FEDIAF es el suelo de
un perro sano, no el suelo terapéutico de esa patología.

| Patología · nutriente | Hasta dónde dejaríamos bajar | Por qué hay que revisarlo |
|---|---|---|
| pancreatitis · proteína | 52,1 | El extremo de SACN5 (37,5) está **bajo** el mínimo de FEDIAF; pusimos el de FEDIAF como parada |
| hepatopatía · cobre | sin parada | El objetivo terapéutico (1,2) está bajo el mínimo de FEDIAF (2,08): el margen real es cero sin prescripción |
| cardiopatía genérica · sodio | 480 | Pusimos el valor del estadio D. La entrada genérica existe justo porque **no** se sabe el estadio |
| cardiopatía D · sodio | 290 | Es el mínimo de FEDIAF, no una cifra de la fuente |
| hiperlipidemia · grasa | 13,75 | La fuente da un número, no un rango; 13,75 es el mínimo de FEDIAF |
| **obesidad · grasa** | **28** | ⚠️ **No es nutrición: es ingeniería.** Es un límite **medido** de nuestro solver con el catálogo real (22,5 y hasta 27 no dan menú ni en 40 s; 28 sí, 5 de 5) |
| PLE · grasa | 13,75 | La fuente no da suelo; 13,75 es el mínimo de FEDIAF |

> **PREGUNTA 22.** En cada uno de estos siete: **¿cuál es el suelo
> terapéutico real, y qué variable clínica lo mueve?**

> **PREGUNTA 23.** El de obesidad mezcla una cifra de máquina con las de
> fuente. ¿Te parece que un límite así debería existir siquiera, o el motor
> debería decir «no puedo bajar de aquí con este catálogo» y separarlo del
> objetivo clínico?

### 8.4 · Dos cosas que sabemos que están mal modeladas

⚠️ **`renal_avanzada` se comporta exactamente igual que `renal`.** Su
diferencia clínica real es **la proteína**, y no hay ningún tope de proteína
en ninguna de las dos: las dos entradas aplican el mismo fósforo (1200) y
nada más. Hoy son la misma patología con dos nombres.

⚠️ **La hepatopatía tiene tope de cobre, pero bloquea antes de llegar a
aplicarlo.** El objetivo terapéutico (1,2 mg/1000 kcal) está por debajo del
mínimo de FEDIAF (2,08): la dieta que trata está por debajo de la que
alimenta. Por eso no se genera menú automático.

> **PREGUNTA 24.** ¿Qué debería hacer `renal_avanzada` de distinto? Si es
> bajar la proteína por debajo de FEDIAF, eso es prescripción y solo lo firma
> un veterinario — pero entonces la entrada debería decir eso y no fingir que
> aprieta el fósforo un poco más.

### 8.4-bis · Cobertura contra la lista legal europea

El Anexo B del Reglamento (UE) 2020/354 tiene **20 objetivos nutricionales
particulares para perro** (entradas 10 a 28 y la 30; la 29 no es canina). El
motor cubre **17**.

*(Corrección del 8 de septiembre, tarde: la primera cuenta decía 19 objetivos y
dos que faltaban. Al leer el PDF oficial entrada por entrada son **20**, y los
que faltan son **tres** — se había pasado por alto la 21, diarrea aguda.)*

**Los tres que faltan:**

| Nº | Objetivo legal | Característica esencial que pide | Por 1000 kcal |
|---|---|---|---|
| 15 | **Restablecimiento nutricional, convalecencia** | Ingredientes muy digestibles · energía **≥3520 kcal/kg** · proteína bruta **≥250 g/kg** | proteína ≥ **71 g** |
| 21 | **Trastornos agudos de la absorción intestinal** (diarrea aguda) | Na ≥1,8 %, K ≥0,6 %, carbohidratos digestibles ≥32 %, **1-7 días** | pienso **complementario**, no ración completa |
| 30 | **Apoyo en situaciones de estrés** | Caseína bovina hidrolizada por tripsina, **1-3 g/kg** | 0,28-0,85 g |

La 21 es la menos nuestra de las tres: la norma la define como pienso
**complementario** para 1-7 días, no como la ración completa de un perro.

El primero es un **suelo** de proteína y de densidad energética para un perro
que sale de una enfermedad o una cirugía — justo lo contrario de casi todo lo
demás, que son techos. El motor no tiene ninguna entrada para eso.

**Y catorce perfiles del motor no corresponden a ningún objetivo legal**:
addison, cushing, cáncer, disfunción cognitiva, epilepsia, fracaso renal
agudo, hipotiroidismo, inmunosupresión, mielopatía degenerativa, las dos
miocardiopatías dilatadas, pancreatitis, riesgo de dilatación-vólvulo, y
«otra». **Eso no es un fallo**: la lista legal es de **alimentos dietéticos
comerciales**, no un catálogo de enfermedades. Pero sí dice dónde no hay
número europeo al que agarrarse.

⚠️ **Y ahí está el caso de la pancreatitis, que es el que deja sin comer a un
perro.** Aplicando la regla que usa este proyecto —FEDIAF primero; donde
FEDIAF no llega, SACN5— resulta que:

- **FEDIAF** no dice nada de pancreatitis.
- **El Reglamento 2020/354 tampoco**: no hay objetivo dietético «pancreatitis»
  en la lista.
- Luego **manda SACN5**: ≤15 % MS (no obeso, no hipertrigliceridémico) =
  **37,5 g/1000 kcal**, y ≤10 % MS (obeso o hipertrigliceridémico) = **25**.

Hoy el motor usa **20**, de Merck, que no es ninguna de las dos. Y **medido:
con 37,5 el perro renal con pancreatitis SÍ recibe menú.**

> **PREGUNTA 21-quinquies.** Siguiendo la propia regla del proyecto, el tope
> de grasa en pancreatitis debería ser el de SACN5 —37,5 en el perro normal,
> 25 en el obeso o hipertrigliceridémico— y no los 20 de Merck. Eso además
> resuelve el caso `renal + pancreatitis`. **Pero relaja un tope de patología,
> y eso no lo decide el software.** ¿Se cambia?

### 8.5 · Las 24 patologías sin límite numérico

De las 40, **24 no fijan ningún número**. Lo que sí hacen es excluir
alimentos, excluir fruta, bloquear la formulación automática, o exigir una
prescripción por debajo de FEDIAF. Ejemplos: hipotiroidismo (excluye grelo y
nabo por progoitrina, sin umbral canino publicado), diabetes (excluye fruta;
y si además hay pancreatitis o hipertrigliceridemia, tope de grasa al 30 % de
las kcal, Purina Institute), urato (objetivo de purinas 90 mg/1000 kcal, pero
bloquea porque una ración cruda está en 687-922).

**Y hay 13 condiciones estudiadas que no tienen perfil ninguno**:
estreñimiento y obstipación, megaesófago/disfagia/esofagitis, enfermedad
periodontal, gastroenteritis aguda, SIBO, síndrome de intestino corto,
flatulencia excesiva, urolitiasis por sílice, realimentación tras anorexia,
hipertensión sistémica, acidosis tubular renal, hiperoxaluria primaria y
gastritis aguda.

> **PREGUNTA 25.** De esas 13, ¿cuáles merecen perfil en una app de ración
> cruda para dueños? ¿Y de las que sí: tienen objetivo nutricional
> formulable, o son de las que hay que bloquear?

---

## 9 · La forma de la ración, que NO es nutrición

Esto es criterio nuestro **declarado**, y es importante que se lea como tal.

Proporciones de partida (% del peso de la ración): hueso carnoso 20-60 %,
carne muscular 10-60 %, verduras y frutas 2-10 %, vísceras 2-12 %, hígado
2-6 %.

**Cuando no existe menú posible, se sueltan estas proporciones —nunca los
requisitos ni la seguridad—** bajando por una escalera de seis peldaños, y
**se dice siempre en qué peldaño salió**. Un veterinario puede además
**elegir el peldaño**, y entonces no se baja solo: bajar sería cambiarle la
decisión a quien la ha tomado.

El último peldaño suelta el techo de vísceras, hígado y verdura, pero **nunca
el mínimo de carne y hueso**: sin eso el motor monta una ración de hígado,
verdura y suplementos que cumple los 43 requisitos en el papel y no es comida
para un perro.

> **PREGUNTA 26.** ¿Las proporciones de partida te parecen razonables como
> punto de arranque? No son de FEDIAF: son criterio de BARF.

---

## 10 · Los datos: de dónde sale la composición de cada alimento

**163 fichas, 7407 casillas de nutriente.**

**El orden de fuentes es fijo y está escrito:** BEDCA (primaria) → Köber 2017
para el hueso → CIQUAL → USDA. No es preferencia: **ninguna tiene los 41
nutrientes**. BEDCA trae yodo pero ni un aminoácido; USDA trae los 12
aminoácidos y la colina pero no publica yodo; CIQUAL trae todos los ácidos
grasos pero tampoco aminoácidos.

### 10.0 · La humedad, que no está — y de la que dependen casi todas las cifras de patología

**Esto es lo primero que hay que mirar de este apartado, y salió el 8 de
septiembre al verificar la pancreatitis.**

Casi todas las cifras clínicas que aplica el motor vienen de tablas que las dan
en **porcentaje de materia seca**: SACN5 las expresa así en las quince tablas que
se han verificado, y el Reglamento europeo las da por kg de pienso al 12 % de
humedad. El motor, en cambio, trabaja en **gramos por 1000 kcal**, porque es la
única unidad que no depende de cuánta agua lleve la comida.

El puente entre las dos es **multiplicar por 2,5**, y ese 2,5 sale de asumir una
densidad de **4000 kcal metabolizables por kg de materia seca**. Es la referencia
de FEDIAF, la de NRC 2006, y **la que impone la propia ley**: el Reglamento (UE)
2020/354, en su nota al pie (2), dice literalmente *«based on a diet with a dry
matter energy density of 4000 kcal Metabolisable Energy/kg… **the values shall be
adapted if the energy density deviates**»*.

**«Shall be adapted».** La ley obliga a adaptar los valores si la densidad se
desvía. Y una ración de comida cruda no tiene por qué tener 4000.

**El problema: no podemos comprobarlo.** Las 163 fichas del catálogo **no llevan
humedad**. Ninguna. Así que no se puede calcular la materia seca de un menú, y por
tanto no se puede saber su densidad energética real. La conversión ×2,5 es una
asunción que hoy **no es verificable con nuestros propios datos**.

**Lo que sí se ha podido hacer es estimarla**, deduciendo el carbohidrato por
diferencia (Atwater modificado) y la ceniza del calcio y el fósforo. Con ese
método, sobre menús reales de un adulto de 22 kg:

| Menú | Densidad estimada | Qué significa para un «≤15 % MS» |
|---|---|---|
| Perro sano, sin patología | **4420** kcal/kg MS | equivaldría a 33,9 g/1000 kcal |
| Pancreatitis (grasa ≤37,5) | **3674** | equivaldría a **40,8** |
| Obesidad (grasa ≤30) | **3886** | equivaldría a 38,6 |

Tres cosas de aquí:

1. **El error es del orden del ±10 %**, no de un factor. La conversión aguanta.
2. **Y en las patologías es conservador.** Un menú con la grasa topada tiene
   *menos* densidad que la referencia, así que el número que aplicamos (37,5) es
   más estricto que el que saldría con la densidad real (40,8). El sesgo trabaja
   a favor de la seguridad, no en contra — y es autocorrectivo: cuanto más se
   aprieta la grasa, más baja la densidad y más conservadora se vuelve la cuenta.
3. **Pero es una estimación, no una medida.** Y afecta a **todas** las cifras de
   patología a la vez, no solo a la grasa.

> **PREGUNTA 30-bis.**
> 1. ¿Te parece aceptable el puente de 4000 kcal/kg MS para una ración cruda, o
>    hay que medir la humedad antes de seguir usando cifras convertidas desde
>    porcentaje de materia seca?
> 2. Si hay que medirla: ¿vale la humedad publicada de las bases de datos
>    (BEDCA/CIQUAL/USDA) para un alimento que se sirve crudo y entero, o el
>    despiece y el goteo la cambian lo bastante como para que haya que medirla?
> 3. ¿Hay algún nutriente donde este ±10 % sí sea determinante y haya que
>    tratarlo aparte?

**Estado:** dato que falta, identificado y cuantificado, sin resolver. Existe un
`HUMEDAD_CATALOGO.csv` en el material de trabajo con 66 humedades documentadas y
93 pendientes con su motivo, que nunca llegó al catálogo.

### 10.1 · Los tres estados de un 0

Esto es de lo que más orgullosas estamos y conviene que lo mires:

| Estado | Qué significa |
|---|---|
| valor | Un dato |
| **`sin_dato`** | No lo sabemos. **No cuenta como 0**: contra un techo se imputa al percentil 90 de su familia |
| **`cero_verificado`** | Un 0 al que alguien fue a la fuente, comprobó que es real, y dejó escrito cuál y cuándo |
| **`dato_dudoso`** | Un valor declarado que creemos erróneo. Tiene forma de dato bueno y pasa cualquier validación de formato |

**Un hueco no es un cero.** Contra un mínimo, un cero es conservador; contra
un máximo es peligroso, porque aprueba lo que no sabemos. **1362 casillas
están declaradas `sin_dato`.**

### 10.2 · Estado real de la procedencia

⚠️ **Solo 34 de las 163 fichas llevan hoy un identificador de fuente.** Las
demás lo llevan en prosa o no lo llevan. Hay trabajo hecho (sin fusionar) que
sube eso a 99 fichas con identificador y añade la columna de humedad con
procedencia en 65.

**El contraste exhaustivo de las 7407 casillas contra su fila de origen NO
está hecho.** Es lo siguiente.

> **PREGUNTA 27.** ¿Hay algún nutriente donde te fíes más de una base que del
> orden que usamos? En concreto, ¿el hueso de Köber 2017 te parece la
> referencia correcta para el calcio del hueso carnoso?

---

## 11 · Qué NO hace el motor

Para que la revisión no dé por hecho lo que no hay:

- **No decide cuándo hay que ir al veterinario.** Bloquea la formulación
  automática en las condiciones que lo requieren, y lo dice.
- **No trata ninguna enfermedad.** Aplica límites; no es una dieta
  terapéutica.
- **No ajusta por analítica.** No hay ningún sitio donde entre un valor de
  laboratorio.
- **No modela el estadio de la enfermedad** salvo en cardiopatía (ACVIM A-D)
  y renal (base / moderada-grave, y esta última hoy no se comporta distinto).
- **No distingue crudo de cocinado.** Por eso los mariscos activan la misma
  restricción de tiaminasa que el pescado.
- **No tiene concepto de fase dentro del crecimiento** (los ~6 meses de la
  nota b de FEDIAF).
- **No permite mover ningún límite, ni siquiera al veterinario.** Hoy solo
  puede *leer* hasta dónde podría moverlo. Que se pueda mover de verdad es el
  paso siguiente, y por eso hace falta la clasificación del §0.2.

---

## 12 · Cómo contestar

No hace falta contestarlo todo ni en orden. Si solo hay tiempo para tres:

1. **La 21** — la grasa en pancreatitis. Es la que hoy deja a un perro sin
   comer.
2. **La 2 y la 3** — la clasificación en tres cajas. Es lo que permite que un
   veterinario mueva lo que es suyo sin que el software decida por él.
3. **La 19** — los seis umbrales de seguridad que pusimos nosotras.

Para cada respuesta nos sirve: **el número o el rango, la variable clínica
que lo mueve si es rango, y la referencia**. Si la respuesta es «depende del
caso», eso ya es una respuesta completa y la implementamos como rango.

Si algo de este documento no coincide con lo que sabes, **dilo con el dato
que lo desmiente**: hemos preferido escribir lo que hay, incluidos los
huecos, antes que un resumen que quede bien.
