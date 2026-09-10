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

⚠️ **MEDIDO EL 9 DE SEPTIEMBRE, Y NO SALEN 4000.** Se estimó la materia seca de
cada alimento como proteína + grasa + fibra + cenizas —las cenizas a partir del
calcio, porque el mineral del hueso es hidroxiapatita y el calcio es su ~39 %— y
se pesó por los gramos de los 216 menús del catálogo:

| | kcal por kg de materia seca |
|---|---|
| Mínimo | 4157 |
| **Mediana** | **5159** |
| Máximo | 6365 |
| Menús por debajo de 4000 | **0 de 216** |

**La mediana está un 29 % por encima del puente.** Y tiene sentido físico: los
4000 son la cifra de un pienso, que lleva hidratos a 4 kcal/g y bastante ceniza y
fibra; una ración cruda no lleva hidratos y sí grasa a 9 kcal/g.

⚠️ **CORREGIDO EL 9 DE SEPTIEMBRE, Y AQUÍ PONÍA LO CONTRARIO.** Esta sección
decía que, por ser nuestra ración más densa, los techos convertidos desde % de
materia seca quedaban «un 29 % más flojos» y los suelos «un 29 % más estrictos».
**Es falso, y la medida de arriba no tiene la culpa: la culpa era de la deducción.**

El capítulo 1 de SACN5 dice lo contrario, y dos veces:

> «Animals require less food to meet their energy requirements when foods with
> higher energy densities are fed. Under these circumstances, **the concentrations
> of the other nutrients in the food need to be increased proportionately**, to
> ensure the animal receives the minimum amount of all nutrients needed in a
> smaller amount of food.»

Y la simétrica, que es la que vale para los techos:

> «When foods with lower energy densities are fed... **the nutrient levels need to
> be decreased proportionately**, so that the animal would not receive toxic levels
> of nutrients in a larger amount of food.»

O sea que el porcentaje sobre materia seca **sube o baja con la densidad del
alimento a propósito**, justo para que la cantidad **por caloría** se mantenga. La
cantidad por 1000 kcal es la invariante, y es la unidad en la que trabaja el motor.
**Por eso la conversión sí vale para una ración cruda**: lo que no vale es coger el
porcentaje y aplicarlo tal cual.

El **Caso 1-1** del mismo capítulo lo resuelve con números: un techo de 1,2 % a 3,6
kcal/g son 3,33 g/1000 kcal, y su versión corregida a 4,0 kcal/g —1,32 %— son 3,30.
El mismo número.

### ⚠️ LO QUE SÍ ESTÁ MAL, Y ES OTRA COSA: la densidad de referencia

La conversión no se hace con la densidad de nuestra ración, sino con **la que
declara la fuente**. Y ahí depende de quién sea el número:

| De quién es el número | Densidad de referencia | Multiplicador |
|---|---|---|
| **FEDIAF** (Tablas III-3b y VII-17) | **4 kcal/g MS** | ×2,5 |
| **NRC** (recommended allowances) | **4 kcal/g MS** | ×2,5 |
| **SACN5**, sus tablas de «key nutritional factors» | **4 kcal/g MS** | ×2,5 |
| **SACN5 cap.33** (calcio del cachorro grande, vía Caso 1-1) | **3,8 kcal/g MS** | ×2,63 |

### ⚠️ CORREGIDO EL 10 DE SEPTIEMBRE: SACN5 SE CONTRADICE CONSIGO MISMO, Y GANA EL 4,0

Aquí ponía que SACN5 usa **3,5** para el perro, que por tanto usábamos el
multiplicador del gato y que **68 de las 74 cifras clínicas** estaban un 14 %
apretadas de más, con una tabla de cuánto había que aflojar cada una. **Era
falso**, y lo era en la dirección peligrosa: proponía relajar 68 límites clínicos.

**Lo que sí dice el Box 1-2**, literal y entero:

> «For example, **recommended nutrient values for canine and feline foods are
> based on an energy density of 3.5 and 4.0 kcal ME/g** (14.64 and 16.74 kJ ME/g)
> **of food dry matter, respectively**.»

O sea que el método declara 3,5 para el perro. **Pero sus propias tablas caninas
no lo usan**, y lo dicen tres veces:

1. **La nota al pie de la Tabla 13-3** —de la que salen nuestros techos del perro
   sano— dice: *«Dry matter basis. **Concentrations presume an energy density of
   4.0 kcal/g**. Levels should be corrected for foods with higher energy
   densities.»* Es la **única** de las 24 tablas que cita `patologias.json` que
   declara densidad, y dice 4,0.
2. **El cap.34** convierte la glucosamina así: *«**in a food with an energy
   density of 4 kcal/g DM**, glucosamine HCl and chondroitin sulfate should not
   exceed 0,10 y 0,08 %»*.
3. **Y el cap.15 lo demuestra sin que haya que fiarse de ninguna nota**, porque da
   la misma cantidad en dos unidades: *«Providing approximately **20 % of the
   energy from carbohydrate** … translates to about **23 % DM carbohydrate**»*.
   Esa equivalencia solo sale a 4,0:

   | Densidad supuesta | El 20 % de la energía, en % de MS |
   |---|---|
   | 3,5 kcal/g | 20,0 % |
   | 3,8 kcal/g | 21,7 % |
   | **4,0 kcal/g** | **22,9 % ≈ 23 %** ✅ |

   (Con los 3,5 kcal/g de Atwater modificado para el hidrato. Es la comprobación
   que no depende de ningún número nuestro.)

**Conclusión: el ×2,5 estaba bien y no hay 68 cifras que aflojar.** El 3,5 del
Box 1-2 es lo que el libro dice de su método; el 4,0 es lo que hacen sus tablas,
y una nota al pie manda sobre las filas que lleva debajo.

Y desde el 10 de septiembre esto **no depende de que alguien lo lea**: cada una
de las 88 cifras lleva su conversión como dato —valor literal de la fuente,
unidad, densidad y cita— y `auditar_conversiones.py` **rehace la cuenta** en cada
batería (BLOQUE 72). 84 de las 88 se reproducen exactas desde las filas de sus
tablas; las otras 4 llevan `ajustado_a_proposito` con el motivo.

> **PREGUNTA 1 — reducida el 10 de septiembre por segunda vez, y lo que queda
> es una contradicción de la fuente, no una duda nuestra.**
> Nació preguntando si el puente había que hacerlo «a la densidad real de la
> ración»: no, la densidad de la ración no entra. Siguió preguntando si había que
> corregir 68 cifras de 4,0 a 3,5: tampoco, y eso está resuelto arriba con la
> propia aritmética del libro.
>
> **Lo que queda, y es tuyo porque es criterio y no lectura:**
>
> 1. **El Box 1-2 dice 3,5 para el perro y las tablas caninas usan 4,0.** Nosotras
>    aplicamos el 4,0 de las tablas, porque una nota al pie manda sobre las filas
>    que lleva debajo y porque el cap.15 lo confirma con su propia equivalencia.
>    **¿Estás de acuerdo con esa lectura?** Si el 3,5 fuera lo que vale, 68 límites
>    clínicos se aflojarían un 14 %.
> 2. **El cap.33 declara 3,8** para el calcio del cachorro de raza grande, vía el
>    Caso 1-1. O sea que al menos una tabla tiene densidad propia distinta.
>    **¿Hay que ir tabla por tabla buscando la suya**, o basta con la de la 13-3
>    salvo que el capítulo diga otra cosa? Hoy hacemos lo segundo, y las 88
>    conversiones están escritas como dato para que se pueda auditar cuál usa cada
>    una.

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

> **PREGUNTA 2 — replanteada el 9 de septiembre.** La correspondencia que
> proponíamos aquí (`(L)` y SUL = tope duro · «key nutritional factor» con rango =
> rango clínico · lo demás = criterio nuestro) **era nuestra, y ya no hace falta
> inventarla**: la Tabla 2-1 de SACN5 da una escala publicada (ver PREGUNTA 3). Lo
> que sí sigue haciendo falta es cruzar las dos cosas, porque miden cosas
> distintas: el grado de evidencia dice **cuánto te fías del número**, y el origen
> legal o nutricional dice **si se puede pasar**. Un límite legal de grado 4 sigue
> siendo intocable, y una recomendación de grado 1 sigue siendo una recomendación.
> **Lo que queda**: ¿el cruce correcto es «lo legal no se toca nunca, lo demás se
> mueve según el grado», o hay casos donde eso no funciona?

> **PREGUNTA 3 — reducida el 9 de septiembre. Estaba en SACN5, en el capítulo 2.**
> No es «qué se puede mover», pero sí la clasificación que falta para poder
> discutirlo, y es explícita, publicada, veterinaria y de nutrición clínica: la
> **Tabla 2-1, «Guidelines for quality of evidence that can be used for veterinary
> clinical nutrition»**, adaptada del U.S. Preventive Services Task Force por
> Roudebush et al. 2004, y que **usa el propio SACN5** para calificar sus
> recomendaciones. Cuatro grados, literal:
>
> · **1** — ensayo aleatorizado y controlado, **en la especie diana y con la
>   enfermedad desarrollada de forma natural**.
> · **2** — ensayo aleatorizado y controlado **en laboratorio**, misma especie,
>   enfermedad natural.
> · **3** — estudio clínico bien diseñado **sin aleatorizar**; cohortes o casos y
>   controles; **modelos o simulaciones** de la enfermedad en la especie diana;
>   series de casos; resultados espectaculares de estudios no controlados.
> · **4** — opinión basada en experiencia clínica (libros de texto, monografías,
>   ponencias); estudios descriptivos; **estudios en otras especies**;
>   justificación fisiopatológica; informes de comités de expertos.
>
> Con esa escala, cada una de las 74 cifras clínicas se puede etiquetar **sin
> inventar nada**, derivándolo de la fuente que ya lleva escrita. Ejemplos que
> salen solos: nuestro techo de **mercurio es grado 4** («studies conducted in
> other species» — es una dosis humana); la **tiaminasa, grado 4**
> («pathophysiologic justification»); los techos del perro sano, grado 4 (informe
> de comité o libro de texto); la proteína y la fibra de obesidad, **grado 2**,
> porque el cap.27 cita ensayos controlados de restricción energética en perro.
>
> **Lo que sigue siendo tuyo, y es más estrecho**: ¿un grado 4 debería poder
> moverlo un colegiado y un grado 1 no? ¿O el grado dice cuánto te fías del
> número, y quién lo toca es otra cosa?

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
| Ajuste joven (1-2 años) | **+20** | FEDIAF 2025, **Tabla VII-6** («Practical recommendations for MER in dogs at different ages»): 130 kcal/kg^0,75 de 1 a 2 años contra 110 de 3 a 7 |
| Ajuste senior (>7 años) | **−15** | Íd., Tabla VII-6: 95 kcal/kg^0,75 en >7 años contra 110. Y SACN5 cap.5 dice lo mismo por otro lado: «senior dogs should be offered foods providing a 15 to 20 % caloric reduction» |
| Convive con otros perros | +10 | Íd. |
| Macho entero | +10 | Íd. |
| Ajuste por raza | ±15 | Thes et al. 2014, Universidad de Múnich, 586 perros de compañía reales. Media 98; las razas de la lista, 113 y 82 |

**Estado: los cinco escalones de actividad, VERIFICADOS** el 8 de septiembre
contra la Tabla VII-7 de FEDIAF 2025 («Recommendations for DER in relation to
activity»): 95 · 110 · 125 · 150-175, exactos. Y hay un contrato de **124 casos**
con sus kcal esperadas, que se comprueba en cada batería.

⚠️ **El escalón de edad cambió el 9 de septiembre y hay que decirlo**, porque la
versión anterior de este documento daba +15/−7 (Thes et al. 2014). Al inventariar
las tablas de FEDIAF apareció que la **Tabla VII-6** publica el escalón de edad
—130 / 110 / 95 kcal/kg^0,75 para 1-2 años, 3-7 años y >7 años— y que **no se
estaba usando**: nuestro −7 era un −6,4 % cuando FEDIAF dice −13,6 % y SACN5
cap.5 dice «15 to 20 %». Y había algo peor: el grupo «joven» era **código
muerto**, no se pasaba nunca ni desde el servidor ni desde la app, así que un
perro de año y medio recibía lo mismo que uno de cinco. Los 24 casos nuevos del
contrato del DER (de 100 a 124) son justo los que fijan ese escalón.

**Y esa misma tabla trae dos filas más que el motor no usaba. Ya las usa.**

| Fila de FEDIAF VII-7 | Qué dice | Qué hace el motor |
|---|---|---|
| **Great Danes** | **200 (200-250) kcal/kg^0,75** | La aplica desde el 8 de septiembre |
| **Newfoundlands** | **105 (80-132)** | Íd. |
| Obese prone adults | ≤ 90 | Usa RER del peso ideal (70), **más estricto** — ver §1.4 |

Las dos razas están en la lista de 136 de la app y no se usaban. Lo que
costaba, medido:

| Perro | FEDIAF, específico de su raza | Motor antes, en «normal» (110) | Le dábamos |
|---|---|---|---|
| Gran Danés 67,5 kg | **4710 kcal/día** | 2590 kcal/día | **el 55 %** |
| Terranova 56,5 kg | 2164 kcal/día | 2267 kcal/día | el 105 % |

Un gran danés se quedaba **2100 kcal/día corto** si su dueño marcaba «normal».
Y los 200 no son un valor extremo: SACN5 cap. 5 dice que las estimaciones de
DER en perro *«range between 95 to 200 kcal … per (BWkg)0.75 per day»*.

**¿En vez del nivel de actividad, o el suelo sobre el que se aplica? EN VEZ
DE, y lo dice la propia guía dos veces.** Primero la frase que presenta la
tabla:

> *«Table VII-7 provides examples of daily energy requirements of dogs at
> different activity levels, for specific breeds and for obese prone adults.»*

Tres clases de ejemplo en paralelo, la misma columna y el mismo coeficiente:
una fila de raza es una alternativa a una fila de actividad, igual que
`Obese prone adults ≤ 90` es una alternativa y no un descuento sobre el 95.
Y después la sección **7.2.3.4 «Breed & type»**, que dice de qué está hecha
esa diferencia:

> *«Breed-specific needs probably reflect differences in temperament,
> resulting in higher or lower activity, as well as variation in stature or
> insulation capacity of skin and hair coat.»*

La diferencia de raza **ya contiene** la de actividad. Sumar un nivel de
actividad encima sería contarla dos veces.

**Lo único que FEDIAF no resuelve es dónde caer dentro del rango que publica.**
Da `200 (200-250)` y `105 (80-132)` y ninguna regla para colocarse dentro. El
motor coloca por actividad —su diferencia contra «normal»— y recorta al rango
de FEDIAF, de forma que ningún resultado sale de lo que publica la fuente.
Esa parte es interpretación nuestra, y se declara:

| Gran Danés 67,5 kg | coef | kcal/día |
|---|---|---|
| sedentario | 200 (recortado) | 4710 |
| normal | 200 | 4710 |
| activo | 215 | 5063 |
| muy activo | 240 | 5652 |
| trabajo | 250 (recortado) | 5887 |
| senior, normal | 200 (recortado) | 4710 |

Para el gran danés «en vez de» y «suelo» acaban coincidiendo, porque 200 es a
la vez el valor central y el extremo bajo de su rango: ningún ajuste a la baja
puede bajar de ahí. Para el terranova no coinciden — su rango abre hacia los
dos lados, y va de 90 (sedentario) a 132 (trabajo).

El ajuste por raza de Thes 2014 (±15 kcal/kg^0,75) **no se aplica encima** de
estas dos: ya tienen cifra propia medida.

**Lo que hay que saber:** el DER se calcula **en dos sitios** (servidor y
app), y manda el de la app. Es una duplicación conocida, y por eso existe el
contrato de 124 casos: los dos lados se comprueban contra el mismo fichero.

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

> **La segunda mitad de esta pregunta la contesta FEDIAF** (9 de septiembre): su
> propia fila para esa descripción es *«High activity (3-6 h/day) (working dogs, e.g.
> sheep dogs) — 150-175»*, y 175 es su extremo alto. Los 210 son 3,0 × RER de la
> escala **paralela** de SACN5: son dos marcos distintos y mezclarlos cuenta dos veces
> lo mismo. Manda FEDIAF. *(Y por encima FEDIAF solo tiene «High activity under
> extreme conditions (racing sled dogs 168 km/d in extreme cold) — 860-1240», que esta
> app no cubre y tendría que pautar un veterinario.)*

> **PREGUNTA 5.** Los cinco escalones de actividad los elige el DUEÑO en la
> app, describiendo a su perro. ¿Hay alguna forma mejor de preguntarlo, o algún
> escalón que sobre o falte?

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

**Si no se conoce el peso adulto esperado** se cae a un camino de respaldo,
que hasta el 8 de septiembre eran tres escalones —**210 / 175 / 140**
kcal/kg^0,75 por tramos del 50 % y el 80 % del peso adulto— y ahora son dos,
cortados por edad. FEDIAF no cubre este caso: su ecuación de crecimiento
necesita el peso adulto. La única fuente con cifra es SACN5 Tabla 5-2, parte 2
(canina), literal:

> *«Daily energy intake for growing puppies should be 3 x RER from weaning
> until four months of age. At four months of age energy intake should be
> reduced to 2 x RER until the puppy reaches adult size.»*

3 × RER = **210** ✓ · 2 × RER = **140** ✓ · **2,5 × RER = 175 no estaba en
ninguna parte**: lo habíamos puesto nosotras. Y el criterio de corte tampoco
coincidía — SACN5 corta **por edad** y el motor cortaba **por % del peso
adulto**, que en este camino ni se conoce. Se aplicó la fuente: **210 antes de
los 4 meses, 140 desde los 4 meses**.

⚠️ **Debajo había un segundo fallo, y es el que dolía.** El código leía
**siempre el último** escalón, en los dos repos: un cachorro de dos meses sin
peso adulto esperado recibía **140**, que es lo que SACN5 da para *después* de
los cuatro meses. El escalón sin fuente no solo sobraba: tapaba que los otros
dos no se estaban usando.

> **PREGUNTA 6.** ¿Klein 2019 te parece la referencia correcta para
> crecimiento en una app de consumo? ¿Y el respaldo de SACN5 (210 antes de los
> 4 meses, 140 después) cuando no se sabe el peso adulto, o preferirías que la
> app exigiera ese dato?

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

> **PREGUNTA 9.** En un perro con BCS 9 aplicamos el **45 %** de exceso que da
> la Tabla VII-2 de FEDIAF («>45 %»), y sigue siendo una **cota inferior**: la
> escala satura ahí y Broome et al. (2023) ven perros que superan la descripción
> del 9. ¿Se acepta la cota inferior como está, o en ese extremo preferirías que
> no diéramos estimación y pidiéramos el peso objetivo al veterinario?

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

**El senior tiene tres cosas propias**, aunque comparta la tabla de requisitos
del adulto:

| | Valor | Fuente |
|---|---|---|
| Proteína mínima | 45 g/1000 kcal si el valor de adulto fuera menor | FEDIAF. Hoy no cambia nada: nuestro mínimo de adulto ya es 52,10 |
| Techo de fósforo | **1750** mg/1000 kcal | SACN5 Tabla 14-2 (el adulto joven tiene 2000) |
| Techo de sodio | **1000** mg/1000 kcal | SACN5 Tabla 14-2 |

> **PREGUNTA 10 — contestada en parte el 9 de septiembre, leyendo la Tabla 14-2
> entera.** «Key nutritional factors for foods for mature dogs» da, literal, tres
> antioxidantes con cifra: **Vitamin E 400 IU/kg · Vitamin C ≥100 mg/kg · Selenium
> 0.5 to 1.3 mg/kg** de materia seca. Convertidos (÷4): **67,1 mg · 25 mg · 125-325
> µg por 1000 kcal**. Ninguno se aplica hoy al senior. Los mismos 400 UI de vitamina E
> ya se aplican a la obesidad, así que la cifra no es nueva en el motor.
> **Y contesta la otra mitad en contra**: la proteína **no** sube. Su rango es
> *«Protein (%) 15-23»* = 37,5-57,5 g/1000 kcal, y el extremo bajo queda **por debajo**
> del mínimo de FEDIAF (52,10) que ya aplicamos.
> ⚠️ El extremo alto del selenio (325 µg) **supera el máximo legal de FEDIAF**
> (142 µg), así que ese rango no se puede aplicar entero: mandaría el legal.
> Lo que queda por decidir es tuyo: **¿se aplican los tres al senior, sabiendo que
> son de una tabla de alimentos comerciales, o alguno sobra en una ración cruda?**

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

> **PREGUNTA 11 — reducida el 9 de septiembre, leyendo la nota c entera.** Dice,
> literal: *«Scientific data show that sodium levels up to 1.5 % DM (3.75 g/1000
> kcal) and chloride levels up to 2.35 % DM (5.87 g/1000 kcal) are safe for healthy
> dogs. **Higher levels may still be safe, but no scientific data are available.»*
> O sea que la nota **no es un máximo**: es hasta dónde llegan los datos, y la propia
> frase dice que por encima puede seguir siendo seguro. Tratarlo como techo duro es
> más estricto que la fuente, y consta. Lo que queda es la decisión de producto:
> **¿se mantiene el lado estricto, o pasa a aviso?** Con el dato al lado: en adulto
> no llega a morder nunca, porque el techo de sodio del perro sano (1000 mg) está
> muy por debajo de esos 3750.

**Nutrientes sin máximo en FEDIAF, y el motor no les pone ninguno:** proteína,
grasa, vitamina E, las vitaminas del grupo B, colina, potasio, magnesio,
linolénico, EPA+DHA, araquidónico y los 12 aminoácidos (salvo el techo de
lisina).

**El fósforo sí lo tiene, y por partida doble.** El máximo de FEDIAF en adulto
es **4,00 g/1000 kcal** (Tabla III-3b, fila «Adult: 4.00 (N)», nota h, y el
texto de la sección 3.3.1: *«AAFCO introduced a nutritional maximum for both Ca
(6.25 g/1000 kcal) and P (4 g/1000 kcal)… FEDIAF adopted the same nutritional
maximums»*). En **crecimiento** las dos columnas de máximo están vacías, así que
ahí FEDIAF no pone ninguno.

Y por debajo de ese máximo legal actúa el techo del libro para el perro **sano**:
**2000 mg/1000 kcal** en adulto (SACN5 Tabla 13-3) y **1750** en maduro
(Tabla 14-2). Es la mitad del de FEDIAF, y es el que aprieta de verdad: una
ración cruda de este motor sale pegada a los 4000 sin él.

> **PREGUNTA 12 — reducida el 9 de septiembre, leyendo Dobenecker 2021 entero.**
> El estudio contesta la pregunta tal y como estaba formulada: **sí, la forma importa,
> y lo demuestra con el fósforo total igualado entre los brazos.** Mismos perros,
> cuatro dietas, todas a **1,7 % MS de fósforo (cinco veces la RDA)**, cambiando solo
> la fuente: fosfato inorgánico (NaH2PO4, KH2PO4) contra fósforo orgánico (harina de
> ave como única fuente). Resultado literal:
> *«Pi (KH2PO4, NaH2PO4) **but not organic P** caused an increased apparent P
> digestibility and significantly influenced kinetics of serum FGF23, parathyroid
> hormone, P, CrossLaps and bone-specific alkaline phosphatase»*, y la conclusión:
> *«**The use of Pi in food can therefore not be considered as safe.**»*
> El brazo orgánico, a ≈4250 mg/1000 kcal —por encima del máximo de FEDIAF— no alteró
> la homeostasis. Nuestra ración no lleva ni un fosfato añadido: es hueso e
> hidroxiapatita y carne.
> **Lo que el estudio no contesta, y es lo que queda**: si por eso se suelta el techo
> del libro. SACN5 lo recomienda sobre fósforo TOTAL y por otra línea de evidencia.
> La pregunta pasa a ser mucho más estrecha: **sabiendo que el daño documentado es del
> fosfato inorgánico y que aquí no hay ninguno, ¿se mantienen los 2000 o se sube hasta
> el máximo de FEDIAF (4000)?**
>
> *(Lo que decía antes, y sigue en pie como contexto:)* El techo del perro sano son
> **2000 mg/1000 kcal**, del libro,
> no de FEDIAF. ¿Es el número correcto para una ración cruda, o en un alimento
> húmedo y sin fosfatos añadidos el fósforo del hueso se comporta distinto? Lo
> preguntamos porque **NRC 2006** dice que no hay datos para fijar un límite
> toxicológico (*«There are insufficient data on which to base an SUL for P in
> dogs»*) y **Dobenecker et al. 2021** (*PLOS ONE*) distingue fosfato
> **inorgánico añadido** de fósforo **orgánico** de la matriz del alimento, que
> es el que lleva el hueso carnoso.

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
| **DHA solo** | **— en adulto; 0,05 g en crecimiento y reproducción** | **SACN5 (Tablas 15-5, 17-1 y 33-5) — nuevo el 10 de septiembre** |

### ⚠️ EL DHA SE PIDE APARTE DESDE EL 10 DE SEPTIEMBRE, Y ANTES NO

Hasta ese día el motor exigía **EPA+DHA como una sola cifra** y no pedía reparto,
que es lo que hace la Tabla III-3b de FEDIAF. O sea que un menú de cachorro o de
perra gestante podía cumplir los 0,125 g **enteros con EPA**, con cero DHA, y
salir verde.

SACN5 lo pide separado, y con la misma cifra en **cuatro sitios** — Tabla 15-5
(reproducción), Tabla 17-1 (crecimiento, en **sus dos columnas** de peso adulto),
Tabla 33-5 (crecimiento de raza grande) y el texto de los capítulos 15 y 33, que
lo derivan así:

> «Foods for late gestation and peak lactation should contain the minimum
> recommended allowance of DHA plus eicosapentaenoic acid (EPA) of at least
> 0,05 % (DM) (NRC, 2006). Therefore, **DHA needs to be at least 40 % of the
> total DHA plus EPA, or 0,02 % DM**.»

0,02 % de materia seca a 4,0 kcal/g son **0,05 g/1000 kcal**. Y el DHA no es
intercambiable con el EPA aquí: la Tabla 33-5 dice para qué es —«***For improved
learning»— y el capítulo 15 añade que «milk concentrations of DHA parallel
dietary intake», o sea que lo que no lleva la ración no llega al cachorro.

**Medido ANTES de aplicarlo**, sobre diez menús resueltos en vivo (tres de
CachorroJoven, tres de CachorroCrecimiento, uno de Gestante, uno de
GestanteTardia y dos de Lactante): **ninguno bajaba de 0,05**, el más justo iba a
1,47 veces el suelo, y el DHA salía entre el **57 % y el 75 %** del EPA+DHA. O
sea que **no cambia ni un menú de hoy** — y ese es justamente el motivo de
ponerlo ahora y no cuando muerda.

**No se aplica en adulto**, a propósito: ninguna de las tres tablas es de adulto,
y FEDIAF no pone requerimiento absoluto de EPA+DHA en adulto. Pasarlo de una
etapa a otra sería inventarse la cifra.

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

> **PREGUNTA 15 — reducida el 9 de septiembre, leyendo el NRC entero en ese punto.**
> El NRC lo llama **adequate intake**, no requisito, y lo dice con todas las letras:
> *«A specific requirement for long-chain n-3 PUFAs (EPA and DHA) in adult dogs has
> not been identified to date. ... However, an AI of 0.11 g per 1,000 kcal of
> combined EPA and DHA for overall health is recommended based on studies in other
> species including humans, and pet food usage data. ... small variations in amounts
> of both of these n-3 LCPUFAs are acceptable until more data become available.»*
> O sea que la fuente ni lo exige ni lo cuantifica como mínimo, y tolera variación.
> Aplicarlo como requisito duro es más estricto que la fuente. La decisión que queda
> es tuya y es más estrecha: **¿requisito duro, o recomendación que se dice y no
> bloquea?**

> **~~PREGUNTA 16~~ — CERRADA el 9 de septiembre. El promedio semanal es la lectura
> estricta, no la laxa.** El SUL sale de perros **alimentados con esas dietas durante
> 12 semanas** — *«impaired cellular immunity when dogs were fed diets containing
> 3.13 percent ME n-3 LCPUFAs ... for 12 weeks (Wander et al., 1997)»* — y se contrasta
> con la ingesta poblacional groenlandesa a largo plazo. Es una **concentración de la
> dieta sostenida durante semanas**, así que promediar 7 días es exigir más, no menos.
> ⚠️ **Lo que sí conviene saber**: el SUL del NRC es de n-3 LCPUFA **totales** y
> nosotras lo aplicamos a **EPA+DHA**, que deja fuera el DPA presente en muchas
> fuentes naturales. Por ese lado somos permisivas, y queda declarado.

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

> **PREGUNTA 17 — reducida el 9 de septiembre, leyendo la nota b entera.** Dice,
> literal: *«For puppies of breeds with adult body weight over 15 kg, until the age
> of about 6 months. Only after that time, calcium **can be** reduced to 0.8 % DM
> (2 g/1000 kcal or 0.48 g/MJ) and the calcium-phosphorus ratio **can be** increased
> to 1.8/1.»* O sea que la fuente no obliga a relajar a los 6 meses: **lo permite**.
> Mantenerlo toda la fase no contradice la nota, es declinar un permiso. Lo que
> queda por decidir es solo si merece la pena declinarlo, y esa parte sí es tuya:
> **¿hay motivo clínico para soltar el refuerzo a los 6 meses, o el lado estricto es
> preferible?**

**El umbral de «raza grande» es **15 kg de peso adulto esperado**, que es lo que
dicen las notas a y b de la Tabla III-3b.** No confundirlo con los 25 kg de SACN5,
que deciden otra cosa (§7-bis).

> **~~PREGUNTA 18~~ — CERRADA el 9 de septiembre. Sí hay matiz, y es del gran danés,
> no de «los gigantes».** FEDIAF lo dice en el texto de calcio, literal:
> *«During later growth up to 1.8 % DM can be fed to all breed dogs including giant
> breeds **with the exception of great Danes**. This breed may be more susceptible
> and it is preferable to continue with a food containing a maximum calcium content
> of 1.6%.»*
> 1,6 % MS = **4000** mg/1000 kcal contra los **4500** del resto. Y no hace falta
> implementarlo aparte: el techo del libro para un cachorro de más de 25 kg de adulto
> esperado, aplicado desde el 9 de septiembre, son **2750** — por debajo de los dos.
> El matiz del gran danés ya está cubierto, y por abajo.

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
| **Yodo** | **1275** µg/1000 kcal (+50 % de margen si viene de kelp) | NRC 2006, Belshaw 1975 | De fuente |
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
| Yodo | **1275** µg/1000 kcal | 2750 µg (legal) | ✅ este sí manda |

**Esto no deja a ningún perro desprotegido** —lo que protege es el máximo
legal de FEDIAF, que es más estricto— pero **la documentación dice que
protegen y no protegen**. Si mañana alguien tocara un máximo de FEDIAF
pensando que «ya está el tope crónico debajo», no hay nada debajo.

*(Para la vitamina D esto ya estaba escrito en el `nota_auditoria` de su fila
desde el 6 de septiembre. Para el selenio, no.)*

**El de yodo bajó de 1400 a 1275 el 9 de septiembre**, y de paso se contestó la
pregunta que llevaba abierta: *«1275 está a un 9 % de la cifra que hizo daño, y
esa cifra es de cachorros; ¿bajamos más?»*. La contesta FEDIAF 2025 §3.3.1,
apartado «Iodine», hablando del mismo estudio del que sale nuestro número:

> *«From studies by Castillo et al. (2001a, b) low nutritional maximum for
> iodine in dogs (0.4 mg/100 g DM) was recommended. However in these studies
> puppies were significantly overfed (approx. 75 % above energy requirement)
> which resulted in a substantially increased intake of iodine. Furthermore the
> food was deficient in a number of key nutrients, e.g. Ca, P and K, and
> therefore inappropriate for puppies. Consequently, these results are
> irrelevant for normal commercial nutritionally balanced foods, and the
> existing legal maximum is safe for all dogs.»*

O sea que el organismo que fija los requisitos ya evaluó ese estudio, explica
por qué no aplica a una dieta equilibrada, y declara seguro el máximo legal
entero (2750). Nuestro 1275 es **2,2 veces más estricto** que eso y no cuesta
ni un menú: el peor de los 216 va a 1038. Se queda donde está, y ahora consta
por qué.

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

> **~~PREGUNTA 19-bis~~ — CERRADA el 9 de septiembre, y la contesta FEDIAF.**
> Era: el techo de yodo estaba en **1400**, que es justo el nivel al que Castillo
> 2001a documenta tiroides deprimida y alteraciones óseas en cachorros. Se bajó a
> **1275**, que es lo más alto que la propia fuente documenta comido sin problemas
> (piensos medidos por Belshaw 1975, rango 400-1275), y quedaba la pregunta de si
> había que bajar más. **No hace falta**: FEDIAF 2025 §3.3.1, apartado «Iodine»,
> evalúa ese mismo estudio y lo descarta —
> *«...puppies were significantly overfed (approx. 75 % above energy requirement)...
> the food was deficient in a number of key nutrients, e.g. Ca, P and K, and
> therefore inappropriate for puppies. Consequently, these results are irrelevant
> for normal commercial nutritionally balanced foods, and the existing legal maximum
> is safe for all dogs.»*
> O sea que el organismo que fija los requisitos declara seguro el máximo legal
> entero (2750). Nuestro 1275 es **2,2 veces más estricto** que eso y no cuesta ni un
> menú: el peor de los 216 va a 1038. Se queda. Lo vigilan los BLOQUES 59 y 65.

**Medido el 9 de septiembre, y el «siempre» tiene una excepción:**

| Tope nuestro | Máximo de FEDIAF | ¿Quién manda? |
|---|---|---|
| Selenio 570 µg/1000 kcal | 142 µg/1000 kcal | FEDIAF. El nuestro **nunca actúa** |
| Vitamina D 20 µg/1000 kcal | 14,1875 µg/1000 kcal | FEDIAF. Tampoco actúa nunca |
| Vitamina D 2,6 µg/kg^0,75 | 1,35 · 1,56 · 1,77 · 2,13 · 2,48 µg/kg^0,75, según el nivel de actividad | FEDIAF en los cinco niveles |

Los dos se cruzan en **183 kcal/kg^0,75**, y hay un perro por encima: el **gran
danés**, al que FEDIAF le da 200. Ahí el que protege es el nuestro (2,60 contra
2,84).

> **PREGUNTA 19-ter.** El de selenio y el de vitamina D por kcal **no actúan
> nunca**: ¿se quitan y se deja escrito que quien protege es FEDIAF, o se quedan
> como segunda red por si FEDIAF cambia? El de vitamina D **por peso metabólico**
> sí actúa —en el gran danés y en cualquier perro por encima de 183
> kcal/kg^0,75—, así que ese se queda en cualquier caso.


> **PREGUNTA 19 (bloque entero).** De los seis umbrales marcados como
> criterio nuestro, ¿alguno está mal puesto, en un sentido o en el otro? Y
> sobre todo: **¿alguno debería depender del caso** —o sea, ser un rango con
> palanca del veterinario— en vez de ser una constante igual para todos?

> **PREGUNTA 20.** El del mercurio nos preocupa especialmente: es una
> extrapolación desde una dosis de referencia **humana**, y la fuente dice
> expresamente que no hay límite canino. ¿Lo dejamos, lo cambiamos, o lo
> convertimos en aviso?

---

## 7-bis · Los techos del perro SANO

**Es la tercera clase de límite del motor, y hasta el 8 de septiembre no
existía.** Los de FEDIAF valen para cualquier perro. Los de patología, solo si
esa patología está marcada. Estos valen para el perro que **no tiene nada**:

| Etapa | Techo | Fuente |
|---|---|---|
| Adulto | Fósforo ≤ **2000** mg/1000 kcal · sodio ≤ **1000** | SACN5 Tabla 13-3, *«Phosphorus (%) 0.4 to 0.8»*, *«Sodium (%) 0.2 to 0.4»* |
| Senior | Fósforo ≤ **1750** · sodio ≤ **1000** | SACN5 Tabla 14-2, *«Phosphorus (%) 0.3 to 0.7»*, *«Sodium (%) 0.15 to 0.4»* |
| Crecimiento, hasta 25 kg de adulto esperado | Calcio ≤ **4250** · fósforo ≤ **3250** | SACN5 Tabla 17-1, columna *«Puppies with an adult BW <25 kg»* |
| Crecimiento, **más de 25 kg** de adulto esperado | Calcio ≤ **2750** · fósforo ≤ **2750** | SACN5 Tablas 17-1 (segunda columna) y 33-5 · Fascetti cap.10 |
| Gestación y lactancia | — | No hay |

**Los cuatro de crecimiento son del 9 de septiembre** y se aplican a las dos
etapas de cachorro. Existen porque hasta ese día un cachorro de raza grande
recibía **4500 mg de calcio** (1,80 % de materia seca), que es el máximo de
FEDIAF y un **64 % por encima** de lo que dicen las dos fuentes caninas que
hablan de esto; y porque **FEDIAF no pone máximo de fósforo en crecimiento** —
las dos columnas de máximo de esa fila están vacías. El calcio del grande queda
apretado al 1,1 % de materia seca que pide Fascetti cap.10 *«in order to prevent
panosteitis»*, dentro del 0,8-1,2 % de las Tablas 17-1 y 33-5.

⚠️ **Ojo con los dos umbrales, que no son el mismo.** Los **25 kg** de SACN5
(cap.33: *«large- and giant-breed puppies (>25 kg adult weight)»*) parten la
Tabla 17-1 en dos columnas y deciden estos techos. Los **15 kg** de la nota b de
FEDIAF deciden otra cosa: el mínimo de calcio reforzado y el techo del ratio
Ca:P. Dos fuentes, dos poblaciones, dos números.

### Por qué hacían falta

**FEDIAF SÍ pone máximo de fósforo en adulto: 4,00 g/1000 kcal.** Está en la
Tabla III-3b («Adult: 4.00 (N)», nota h) y en el texto de la sección 3.3.1:
*«AAFCO introduced a nutritional maximum for both Ca (6.25 g/1000 kcal) and P
(4 g/1000 kcal)… FEDIAF adopted the same nutritional maximums for both Ca and
P»*. Se borró por error el 7 de septiembre y **se devolvió la noche del 8**
(ver la nota de auditoría de esa fila en `requerimientos_v2_final.json`).
En **crecimiento** sí que no hay ninguno: las dos columnas están vacías.

Lo que pasa es que **una ración BARF de este motor salía pegada a ese máximo**
—medido, 3.933 a 4.115 mg/1000 kcal, y un menú del catálogo llegó a 4.124, por
encima— y SACN5 recomienda **la mitad** para cualquier perro adulto sano. El
techo del libro no existe porque falte el de FEDIAF: existe porque el de FEDIAF
es un máximo de seguridad y este es lo que el libro recomienda de verdad.

Y el matiz que sí sigue en pie: el NRC 2006 dice que **no hay datos para fijar
un SUL toxicológico** en perros, y Dobenecker et al. 2021 (*PLOS ONE*) que
todavía no se puede definir un no-effect-level. Eso es otra cosa que el máximo
NUTRICIONAL de FEDIAF, que sí existe.

Y ese número **ya estaba entrando en el motor, pero por la puerta de atrás**: en
las dos patologías cuya tabla lo repite —artrosis (1750, Tabla 34-2) y reacción
adversa al alimento (2000, Tabla 31-3)—, que lo llevan porque su población es de
riesgo renal, no porque la enfermedad tenga que ver con el fósforo. El resultado
era incoherente: **el mismo perro pasaba de 4000 a 1750 por marcar «artrosis»**.

### Medido antes de aplicarlo

Un techo así solo se puede aplicar si cabe, y eso se mide, no se supone. Perro
adulto sano, sin alergias, solver a 15 s:

| Peso | Sin techo | Con el techo |
|---|---|---|
| 3 kg | P=4007, **ámbar** | P=1889, peldaño 0, **verde** |
| 10 kg | P=4013, verde | P=1962, peldaño 0, verde |
| 22 kg | P=3813, verde | P=1586, peldaño 0, verde |
| 40 kg | P=3811, verde | P=1524, peldaño 0, verde |

Los cuatro en el **peldaño 0** —sin soltar ni una proporción de BARF— y los
cuatro verdes. El de 3 kg, que sin techo salía ámbar, sale verde con él.

Lo que sí costó: **207 de los 216 menús precalculados de la vista previa**
estaban por encima (mediana 3149). Se regeneró el catálogo entero.

### El techo del ADULTO no se aplica en crecimiento, y no es un olvido

El mínimo de fósforo que FEDIAF exige a un **cachorro joven** son **2250**, por
encima del techo del adulto (2000). Aplicárselo no sería un techo: sería dejarlo
sin menú. Lo que el crecimiento tiene son **sus propios techos**, los de la
Tabla 17-1 de arriba, que están por encima de ese mínimo.

> **PREGUNTA 28.** El sodio de estas dos tablas tiene también un
> **suelo** (0,2 % MS = 500 mg en adulto, 0,15 % = 375 en maduro) que **no** se
> aplica: se ha entendido que lo que la tabla quiere es no pasarse, y que un
> suelo de sodio por encima del mínimo de FEDIAF (290) en un perro sano no lo
> pide nadie. Si eso es leerlo mal, es una línea de cambio.

## 8 · Las patologías: 47 perfiles, 74 límites numéricos y 4 ratios

Los topes por patología **son más estrictos que FEDIAF** y se miden sobre las
**kcal reales del menú**, no las pedidas — el menú puede salir un 3 % por
debajo, y menos kcal con el mismo nutriente es más concentración. **Los suelos
también** (desde el 8 de septiembre por la tarde: hasta entonces el solver los
exigía sobre las kcal pedidas y el filtro final los medía sobre las reales, así
que un menú un 3 % por encima del DER cumplía para uno y no para el otro).

**Regla que se comprueba automáticamente:** ninguna patología formulable
puede tener un tope **por debajo** del mínimo de FEDIAF. Si lo tiene, eso ya
no es un tope: es una dieta de prescripción, y va marcada como no formulable
automáticamente.

### ⚠️ Y DESDE EL 10 DE SEPTIEMBRE UNA PATOLOGÍA PUEDE PEDIR SU PROPIO RATIO

**Son 4, y son dos veces el mismo:** el Ca:P de **1,1 a 2,0** que piden la Tabla
40-5 (oxalato cálcico) y la 41-6 (fosfato cálcico), las dos con la misma frase
—*«maintain a normal Ca:P ratio (1.1:1 to 2:1)»*—. Cada extremo cuenta como un
límite porque el suelo y el techo del mismo par bloquean por separado.

Estaban escritos desde el 8 de septiembre y **no se aplicaban**, y no por
descuido: el motor sabe de ratios Ca:P desde el principio —los aplica desde
FEDIAF y desde la nota b de raza grande— pero no había forma de que una
**patología** pidiera el suyo, así que la celda vivía con
`aplicado_por_el_solver: false` para no perder el número.

**Y no era cosmético.** Medido antes de aplicarlo, por la vía de la API y en
cinco perros adultos, el de 30 kg con oxalato salía con Ca:P **1,06** —por debajo
del 1,1 de la fuente— **y salía en verde**: el semáforo mide el Ca:P contra el
rango de FEDIAF, que en adulto es 1,0-2,0, y los requisitos de FEDIAF son los de
un perro **sano**. Es el mismo agujero del renal con 3084 mg de fósforo, esta vez
en un cociente.

Medido después: los cinco perros de cada patología siguen dando menú verde, y el
más justo sale clavado en 1,10. El **techo** (2,0) coincide con el de FEDIAF en
adulto, así que por arriba no cambia nada; se escribe igual porque es lo que dice
la fuente. Lo vigila el **BLOQUE 75**, que además lo prueba con el fallo puesto.

El mecanismo es **genérico**: admite cualquier par de nutrientes, porque un
cociente entre dos sumas es lineal igual que el Ca:P. Eso es lo que hacía falta
para el **omega-6:omega-3**, que **sigue sin aplicarse** —ver PREGUNTA 40— porque
ahí lo que falta no es maquinaria sino una decisión: las fuentes van de <1:1
(artrosis) a 7:1 (renal) y el NRC dice que ese ratio «is not helpful».

> **⚠️ Esta sección se rehízo entera el 8 de septiembre de 2026.** La versión
> anterior decía «40 perfiles, 19 límites» y traía los números de antes de las
> cuatro pasadas de verificación de ese día. Ninguna de sus cifras era falsa
> cuando se escribió; varias habían dejado de serlo. Se sustituye por la tabla
> completa, generada del propio `patologias.json` para que no pueda volver a
> desincronizarse a mano.

### 8.1 · Los 73, verificados uno a uno contra su capítulo

**Verificado el 8 de septiembre abriendo cada capítulo de SACN5 y leyendo la
tabla citada, fila a fila y no solo la fila del nutriente que ya teníamos.** El
motivo clínico completo de cada cifra —con la cita literal, la conversión y el
margen que le queda al profesional— está en `patologias.json` y se sirve en
`GET /patologias`; aquí va el resumen.

«Convertido» = el valor de la fuente pasado a g o mg por 1000 kcal con el puente
de 4000 kcal/kg MS (§0.1). **El BLOQUE 55 de la batería rehace esa conversión
desde el número de la fuente y compara**, así que ninguna de estas cifras puede
moverse sin que salte.

| Patología | Nutriente | | Valor | Mín. FEDIAF adulto | Máx. FEDIAF adulto | Fuente |
|---|---|---|---|---|---|---|
| Artrosis / osteoartritis | fosforo | ≤ | **1750.0 mg** | 1160 | sin máximo | SACN5 cap.34, Tabla 34-2 |
| Artrosis / osteoartritis | sodio | ≤ | **1000.0 mg** | 290 | 3750 | SACN5 cap.34, Tabla 34-2 |
| Artrosis / osteoartritis | epa | ≥ | **1.0 g** | — | sin máximo | SACN5 cap.34 «Nutritional Management of Osteoarthritis», Tabla 34-2 |
| Artrosis / osteoartritis | lcarnitina | ≥ | **75.0 mg** | — | sin máximo | SACN5 cap.34, Tabla 34-2 |
| Artrosis / osteoartritis | omega3_total | ≥ | **8.75 g** | — | sin máximo | SACN5 cap.34, Tabla 34-2; y Reglamento (UE) 2020/354, entrada 27 |
| Artrosis / osteoartritis | vitE | ≥ | **67.1 mg** | 6.968 | sin máximo | SACN5 Tabla 34-2 |
| Soporte nutricional oncológico (incluye caquexia/sarcopenia asociada) | arginina | ≥ | **5.0 g** | 1.51 | sin máximo | SACN5 cap.30 «Cancer», Tabla 30-5 |
| Soporte nutricional oncológico (incluye caquexia/sarcopenia asociada) | grasa | ≥ | **62.5 g** | 13.75 | sin máximo | SACN5 cap.30 «Cancer», Tabla 30-5 |
| Soporte nutricional oncológico (incluye caquexia/sarcopenia asociada) | proteina | ≥ | **75.0 g** | 52.1 | sin máximo | SACN5 cap.30 «Cancer», Tabla 30-5 |
| Cardiopatía | sodio | ≤ | **739.0 mg** | 290 | 3750 | Cavanaugh SM (DACVIM cardiologia), «Understanding nutrition in dogs with degenerative mitral valve disease», Veterinary Practice News, 6-jul-2020 — las CIFRAS por estadio salen de aqui. El consenso ACVIM 2019 (Keene BW et al., JVIM 2019;33:1127-1140) es el marco clinico, pero NO da cifras. Techo legal: Reglamento (UE) 2020/354, entrada 24 |
| Cardiopatía, estadio ACVIM B2 (remodelado, sin síntomas) | sodio | ≤ | **739.0 mg** | 290 | 3750 | Keene BW et al., ACVIM consensus, JVIM 2019;33:1127-1140; rango numérico de Veterinary Practice News, escala moderna por estadio |
| Cardiopatía, estadio ACVIM C (insuficiencia cardíaca, actual o pasada) | sodio | ≤ | **625.0 mg** | 290 | 3750 | Keene BW et al., ACVIM consensus, JVIM 2019;33:1127-1140; rango numérico de Veterinary Practice News, escala moderna por estadio |
| Cardiopatía, estadio ACVIM D (insuficiencia cardíaca refractaria) | sodio | ≤ | **480.0 mg** | 290 | 3750 | Keene BW et al., ACVIM consensus, JVIM 2019;33:1127-1140; rango numérico de Veterinary Practice News, escala moderna por estadio |
| Urolitos de cistina | sodio | ≤ | **750.0 mg** | 290 | 3750 | SACN5 cap.42 «Canine cystine urolith dissolution and prevention», Tabla 42-1 |
| Miocardiopatía dilatada respondedora a taurina | lcarnitina | ≥ | **50.0 mg** | — | sin máximo | SACN5 5ª ed., cap.36 «Cardiovascular Disease», Tabla 36-4, verificado 7-sep-2026 |
| Miocardiopatía dilatada respondedora a taurina | taurina | ≥ | **250.0 mg** | — | sin máximo | SACN5 5ª ed., cap.36 «Cardiovascular Disease», Tabla 36-4, verificado 7-sep-2026 |
| Dermatitis atópica | fenilalanina_tirosina | ≥ | **3.25 g** | 2.58 | sin máximo | SACN5 cap.32 «Skin and Hair Disorders», Tabla 32-1 |
| Dermatitis atópica | omega3_total | ≥ | **0.875 g** | — | sin máximo | SACN5 cap.32, Tabla 32-6 |
| Dermatosis zinc-sensible (razas nórdicas, defecto de absorción) | fenilalanina_tirosina | ≥ | **3.25 g** | 2.58 | sin máximo | SACN5 cap.32 «Skin and Hair Disorders», Tabla 32-1 |
| Dermatosis zinc-sensible (razas nórdicas, defecto de absorción) | zinc | ≥ | **25.0 mg** | 20.8 | 56.75 | SACN5 5ª ed., cap.32 «Skin and Hair Disorders», Tabla 32-1, verificado 7-sep-2026 |
| Diabetes mellitus | fibra | ≥ | **17.5 g** | — | sin máximo | SACN5 cap.29 «Diabetes Mellitus», Tabla 29-3 |
| Disfunción cognitiva canina | omega3_total | ≥ | **2.5 g** | — | sin máximo | SACN5 cap.35, Tabla 35-3 |
| Disfunción cognitiva canina | vitE | ≥ | **187.5 mg** | 6.968 | sin máximo | SACN5 cap.35 «Brain aging and cognitive dysfunction», Tabla 35-3 |
| Enteropatía crónica / colitis (incluye enfermedad inflamatoria intestinal) | grasa | ≤ | **37.5 g** | 13.75 | sin máximo | SACN5 cap.57 «Inflammatory Bowel Disease», Tabla 57-1 |
| Enteropatía crónica / colitis (incluye enfermedad inflamatoria intestinal) | potasio | ≤ | **2750.0 mg** | 1450 | sin máximo | SACN5 cap.57 «Inflammatory Bowel Disease», Tabla 57-1 |
| Enteropatía crónica / colitis (incluye enfermedad inflamatoria intestinal) | proteina | ≥ | **62.5 g** | 52.1 | sin máximo | SACN5 cap.57, Tabla 57-1 |
| Estreñimiento crónico | fibra | ≥ | **17.5 g** | — | sin máximo | SACN5 cap.64 «Chronic constipation/obstipation», Tabla 64-2 |
| Cálculos de estruvita | fosforo | ≤ | **1500.0 mg** | 1160 | sin máximo | SACN5 cap.43 «Canine struvite urolithiasis», Tabla 43-3 |
| Cálculos de estruvita | magnesio | ≤ | **250.0 mg** | 200 | sin máximo | SACN5 cap.43 «Canine struvite urolithiasis», Tabla 43-3 |
| Cálculos de estruvita | proteina | ≤ | **62.5 g** | 52.1 | sin máximo | SACN5 cap.43 «Canine struvite urolithiasis», Tabla 43-3 |
| Flatulencia excesiva (gases) | fibra | ≤ | **12.5 g** | — | sin máximo | SACN5 cap.65 «Excessive flatulence», Tabla 65-1 |
| Flatulencia excesiva (gases) | proteina | ≤ | **75.0 g** | 52.1 | sin máximo | SACN5 cap.65 «Excessive flatulence», Tabla 65-1 |
| Hepatopatía por acúmulo de cobre | cobre | ≤ | **2.4 mg** | 2.08 | 7 | Center SA et al., «Lower risk for liver copper accumulation in dogs fed copper-restricted diets versus those fed copper-replete diets», JAVMA 264(2), 2026 (doi javma.25.05.0295). VERIFICADO 8-sep-2026. Confirmado ademas contra SACN5 cap.68, Tabla 68-8, y contra el Reglamento (UE) 2020/354, entrada 28 |
| Hepatopatía por acúmulo de cobre | sodio | ≤ | **625.0 mg** | 290 | 3750 | SACN5 cap.68 «Hepatobiliary Disease», Tabla 68-8 |
| Hepatopatía por acúmulo de cobre | hierro | ≥ | **20.0 mg** | 10.4 | 170.45 | SACN5 cap.68 «Hepatobiliary Disease», Tabla 68-8 |
| Hepatopatía por acúmulo de cobre | taurina | ≥ | **250.0 mg** | — | sin máximo | SACN5 cap.68 «Hepatobiliary Disease», Tabla 68-8 |
| Hepatopatía por acúmulo de cobre | vitE | ≥ | **67.1 mg** | 6.968 | sin máximo | SACN5 Tabla 68-8 |
| Hepatopatía por acúmulo de cobre | zinc | ≥ | **50.0 mg** | 20.8 | 56.75 | SACN5 cap.68 «Hepatobiliary Disease», Tabla 68-8 |
| Hiperlipidemia (triglicéridos o colesterol altos) | grasa | ≤ | **30.0 g** | 13.75 | sin máximo | SACN5 5ª ed., cap.28 «Disorders of Lipid Metabolism», Tabla 28-2, verificado 6-sep-2026 |
| Hiperlipidemia (triglicéridos o colesterol altos) | fibra | ≥ | **25.0 g** | — | sin máximo | SACN5 5ª ed., cap.28 «Disorders of Lipid Metabolism», sección «Key Nutritional Factors · Fiber», verificado 7-sep-2026 |
| Insuficiencia pancreática exocrina (EPI) | fibra | ≤ | **12.5 g** | — | sin máximo | SACN5 cap.66 «Exocrine Pancreatic Insufficiency», Tabla 66-1 |
| Insuficiencia pancreática exocrina (EPI) | grasa | ≤ | **37.5 g** | 13.75 | sin máximo | SACN5 5ª ed., cap.66 «Exocrine Pancreatic Insufficiency», Tabla 66-1, verificado 6-sep-2026 |
| Síndrome de intestino irritable | fibra | ≥ | **20.0 g** | — | sin máximo | SACN5 cap.63 «Idiopathic bowel syndrome», Tabla 63-3 |
| Obesidad / sobrepeso, adelgazamiento dirigido | grasa | ≤ | **30.0 g** | 13.75 | sin máximo | SACN5 5ª ed., cap.27 «Obesity», Tabla 27-4, verificado 6-sep-2026 |
| Obesidad / sobrepeso, adelgazamiento dirigido | fibra | ≥ | **30.0 g** | — | sin máximo | SACN5 cap.27 «Obesity», Tabla 27-4 |
| Obesidad / sobrepeso, adelgazamiento dirigido | lcarnitina | ≥ | **75.0 mg** | — | sin máximo | SACN5 cap.27 «Obesity», Tabla 27-4 |
| Obesidad / sobrepeso, adelgazamiento dirigido | lisina | ≥ | **4.25 g** | 1.22 | sin máximo | SACN5 cap.27 «Obesity», Tabla 27-4 |
| Obesidad / sobrepeso, adelgazamiento dirigido | proteina | ≥ | **62.5 g** | 52.1 | sin máximo | SACN5 cap.27 «Obesity», Tabla 27-4 |
| Obesidad / sobrepeso, adelgazamiento dirigido | vitE | ≥ | **67.1 mg** | 6.968 | sin máximo | SACN5 Tabla 27-4 |
| Cálculos de oxalato cálcico | fosforo | ≤ | **1500.0 mg** | 1160 | sin máximo | SACN5 cap.40 «Canine Calcium Oxalate Urolithiasis», Tabla 40-5 |
| Cálculos de oxalato cálcico | magnesio | ≤ | **375.0 mg** | 200 | sin máximo | SACN5 cap.40 «Canine Calcium Oxalate Urolithiasis», Tabla 40-5 |
| Cálculos de oxalato cálcico | sodio | ≤ | **750.0 mg** | 290 | 3750 | SACN5 cap.40 «Canine Calcium Oxalate Urolithiasis», Tabla 40-5; contrastado con Cook A, Atiee GF, «Understanding and Addressing Canine Calcium Oxalate Urolithiasis», Today's Veterinary Practice, 10-dic-2025 |
| Cálculos de oxalato cálcico | vitD | ≤ | **14.1875 µg** | 3.975 | 14.1875 | Máximo LEGAL de FEDIAF 2025 (Tabla III-3a, Reglamento (UE) 2017/1492), no el nutricional |
| Pancreatitis | grasa | ≤ | **37.5 g** | 13.75 | sin máximo | SACN5 cap. 67 «Pancreatitis», Tabla 67-3. Merck Veterinary Manual («less than 20 g fat/1,000 kcal») queda como referencia mas estricta, no como el valor aplicado |
| Pancreatitis | proteina | ≤ | **75.0 g** | 52.1 | sin máximo | SACN5 5ª ed., cap. 67 «Pancreatitis», Tabla 67-3, verificado 6-sep-2026 contra el texto |
| Enteropatía pierde-proteínas / linfangiectasia intestinal | fibra | ≤ | **12.5 g** | — | sin máximo | SACN5 cap.58, Tabla 58-1 |
| Enteropatía pierde-proteínas / linfangiectasia intestinal | grasa | ≤ | **37.5 g** | 13.75 | sin máximo | SACN5 5ª ed., cap.58 «Protein-Losing Enteropathies», Tabla 58-1, verificado 6-sep-2026 |
| Enteropatía pierde-proteínas / linfangiectasia intestinal | proteina | ≥ | **62.5 g** | 52.1 | sin máximo | SACN5 cap.58 «Protein-Losing Enteropathies», Tabla 58-1 |
| Reacción adversa al alimento (alergia o intolerancia alimentaria diagnosticada) | fosforo | ≤ | **2000.0 mg** | 1160 | sin máximo | SACN5 cap.31 «Adverse Reactions to Food», Tabla 31-3 |
| Reacción adversa al alimento (alergia o intolerancia alimentaria diagnosticada) | sodio | ≤ | **1000.0 mg** | 290 | 3750 | SACN5 cap.31 «Adverse Reactions to Food», Tabla 31-3 |
| Reacción adversa al alimento (alergia o intolerancia alimentaria diagnosticada) | omega3_total | ≥ | **0.875 g** | — | sin máximo | SACN5 cap.31 «Adverse Reactions to Food», Tabla 31-3 |
| Insuficiencia renal crónica | fosforo | ≤ | **1200.0 mg** | 1160 | sin máximo | Freeman LM, dvm360 2009; WSAVA; IRIS. Confirmado 6-sep-2026 contra SACN5 5ª ed., cap.37 «Chronic Kidney Disease», Tabla 37-9 |
| Insuficiencia renal crónica | potasio | ≤ | **2000.0 mg** | 1450 | sin máximo | SACN5 cap.37 «Chronic Kidney Disease», Tabla 37-9 |
| Insuficiencia renal crónica | proteina | ≤ | **62.5 g** | 52.1 | sin máximo | Reglamento (UE) 2020/354, Anexo parte B, entrada 10 |
| Insuficiencia renal crónica | sodio | ≤ | **750.0 mg** | 290 | 3750 | SACN5 cap.37 «Chronic Kidney Disease», Tabla 37-9 |
| Insuficiencia renal crónica | vitE | ≥ | **67.1 mg** | 6.968 | sin máximo | SACN5 Tabla 37-9 |
| Insuficiencia renal crónica, moderada-grave (equivalente a IRIS 3-4) | fosforo | ≤ | **1200.0 mg** | 1160 | sin máximo | Igual que renal (Freeman LM, dvm360 2009; WSAVA; IRIS; SACN5 cap.37 Tabla 37-9) |
| Sobrecrecimiento bacteriano en el intestino delgado (SIBO) | grasa | ≤ | **37.5 g** | 13.75 | sin máximo | SACN5 cap.60 «Small intestinal bacterial overgrowth», Tabla 60-1 |
| Urolitos de fosfato cálcico | fosforo | ≤ | **1500.0 mg** | 1160 | sin máximo | SACN5 cap.41 «Canine Calcium Phosphate Urolithiasis», Tabla 41-6 |
| Urolitos de fosfato cálcico | magnesio | ≤ | **375.0 mg** | 200 | sin máximo | SACN5 cap.41 «Canine Calcium Phosphate Urolithiasis», Tabla 41-6 |
| Urolitos de fosfato cálcico | proteina | ≤ | **62.5 g** | 52.1 | sin máximo | SACN5 cap.41 «Canine Calcium Phosphate Urolithiasis», Tabla 41-6 |
| Urolitos de fosfato cálcico | sodio | ≤ | **750.0 mg** | 290 | 3750 | SACN5 cap.41 «Canine Calcium Phosphate Urolithiasis», Tabla 41-6 |
| Urolitos de fosfato cálcico | vitD | ≤ | **9.375 µg** | 3.975 | 14.1875 | SACN5 cap.41, Tabla 41-6 |

**Además, dos cifras escritas con la etiqueta de que el solver NO las aplica**,
porque escribirlas sin decirlo parecería un límite y no lo son:

| Patología | Qué pide la fuente | Por qué no se aplica |
|---|---|---|
| Oxalato y fosfato cálcico · **Ca:P 1,1-2:1** | SACN5 40-5 y 41-6: *«maintain a normal Ca:P ratio (1.1:1 to 2:1)»* | El motor sabe de ratios Ca:P (los aplica desde FEDIAF y desde la nota b de raza grande) pero no tiene forma de que una **patología** pida el suyo. Falta motor, no fuente |
| Cáncer · **omega-3 ≥ 12,5 g** | SACN5 30-5: *«>5% DM»* | **No cabe en este catálogo.** Medido: con los otros tres suelos del cáncer puestos, 11,5 sale en el peldaño 5 y 12,0 no sale en ninguno. La fuente más concentrada es el aceite de linaza (62,5 g/1000 kcal) y haría falta ~20 % de las kcal del día en aceite. Falta un concentrado de EPA+DHA en el catálogo |

### 8.1-bis · Los tres que discrepaban, y en qué quedaron

La versión anterior de este documento marcaba **cuatro** discrepancias con
SACN5 y dejaba una pregunta bloqueante (la 21-bis). El 8 de septiembre se
resolvieron tres de las cuatro **aplicando la fuente**, que es lo que se pidió:

**1 · Pancreatitis · grasa: era 20, ahora 37,5 — y 25 si además hay obesidad o
hiperlipidemia.** El 20 venía de Merck (*«less than 20 g fat/1,000 kcal»*) y la
Tabla 67-3 de SACN5 **gradúa** la grasa en dos niveles: *«≤15% for non-obese and
non-hypertriglyceridemic dogs»* = 37,5 y *«≤10% for obese and/or
hypertriglyceridemic dogs»* = 25. El motor aplicaba un solo nivel y encima el más
estricto de los tres, así que el perro **obeso** con pancreatitis —el de más
riesgo— recibía de hecho el tope de `obesidad` (30), más laxo que los 25 que pide
la fuente para él. Ahora hay un mecanismo de tope condicional
(`topes_por_1000kcal_si_ademas`) y los dos niveles están puestos. **Efecto
lateral medido:** `renal + pancreatitis` pasó de no dar menú nunca a darlo en
verde (fósforo 1198,8, grasa 37,5). El choque no era clínico: era un número que
no venía de la fuente que manda.

**2 · Cardiopatía · sodio: era 900/900/790/480, ahora 739/739/625/480.** Las
cifras por estadio salen de Cavanaugh 2020 (DACVIM cardiología); el consenso
ACVIM 2019 es el marco clínico pero **no da cifras**, que es justo lo que había
que comprobar. Sigue habiendo distancia con las clases de SACN5 36-4
(0,15-0,25 % MS en Ia = 375-625), pero son dos escalas distintas y la que usa la
app es la de estadios ACVIM.

**3 · Hepatopatía · cobre: sigue en 2,4 donde SACN5 dice 1,25.** Dos fuentes que
no dicen lo mismo: SACN5 cap. 68 Tabla 68-8 da **≤5 mg/kg MS** (*«less than 5 ppm
DM copper»*) = 1,25 mg/1000 kcal; Center et al. 2026 (*JAVMA* 264(2):171-180) da
0,24 mg/100 kcal = 2,4. Se usa la más nueva. **No tiene efecto práctico** —la
hepatopatía bloquea la formulación automática antes de llegar al tope— pero el
número está ahí y la elección la hicimos nosotras.

**4 · Obesidad · grasa: sigue en 30 donde SACN5 27-4 dice 22,5.** Está declarado
en el propio dato y con la medida al lado: 22,5 —y hasta 27— **no dan menú** con
el catálogo real ni en 40 s de reintentos, porque una comida de verdad, sin
premezcla vitamínica sintética, no puede bajar tanto la grasa y seguir llegando a
los mínimos de ácidos grasos esenciales con las kcal que quedan. El 30 se apoya
en la otra fila de la misma tabla: *«Foods for prevention of weight regain should
contain ≤14%»* = 35. **Es honesto, pero es un límite de máquina vestido de límite
clínico.**

> **PREGUNTA 21-bis (sigue abierta, y ahora son dos).** Las dos donde elegimos
> nosotras sin que nadie lo firme:
> 1. **Cobre en hepatopatía**: ¿Center 2026 (2,4) o SACN5 (1,25)?
> 2. **Obesidad**: el 30 es lo que la máquina puede hacer, no lo que dice la
>    fuente. ¿Se acepta y se declara como «lo mejor alcanzable con comida
>    real», o hay que decirle al dueño que para adelgazar de verdad hace falta
>    otra cosa?
>
*El fósforo del perro sano ya no es una pregunta: el techo del libro
—2000 mg/1000 kcal en adulto (SACN5 Tabla 13-3) y 1750 en maduro (14-2)— se
aplica a todos los adultos, por debajo del máximo de FEDIAF (4,00 g). Lo que
queda de aquello es la PREGUNTA 12, sobre si 2000 es el número correcto para una
ración cruda.*

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
   (FEDIAF manda; donde FEDIAF no llega, SACN5) el número tiene que ser el de
   SACN5 (37,5 g no obeso / 25 g obeso) y no los 20 g de Merck. **Aplicado el 8 de
   septiembre**: el motor topa hoy en 37,5. Ver §8.2.

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

**De los seis puntos que tenía esta pregunta, cuatro ya están cerrados por el
propio motor y no hace falta contestarlos:** el sodio cardíaco se bajó a **739**,
el techo de proteína renal está en **62,5**, la estruvita es formulable y su
magnesio está en **250** (más estricto que los 511 que se preguntaban), y el
suelo de omega-3 totales de la artrosis **no cabe** con el catálogo real y por eso
vive declarado en `limites_escritos_que_el_solver_no_aplica`, con su medida.

> **PREGUNTA 21-quater.** Quedan dos, y las dos son tuyas:
> 1. **Urato y cistina: ¿la vía de «proteína ≤220 g/1000 kcal + fuentes
>    seleccionadas» es viable con comida real**, o la carga de purinas o de
>    cistina la tumba igual? Hoy las dos están bloqueadas: medido con nuestro
>    catálogo, una ración cruda va de **687 a 922 mg de purinas/1000 kcal**, y no
>    por las vísceras — la mayor parte es carne muscular.
> 2. **Convalecencia (suelo de proteína 71 g/1000 kcal): ¿es una etapa que
>    debería existir?** Es el único de los tres objetivos legales que faltan que
>    parece nuestro.

### 8.1-ter · Lo que las mismas tablas piden y el motor NO aplica

> **⚠️ Esta lista se escribió en la TERCERA pasada y se ha quedado corta por los
> dos lados.** Varias de sus filas se aplicaron ese mismo día (los omega-3
> totales de artrosis y disfunción cognitiva, la vitamina E de cuatro tablas, el
> fósforo y el sodio de la artrosis, la vitamina D del fosfato cálcico). Y
> faltaban tres tablas enteras, que se encontraron en la cuarta pasada. Lo que
> **hoy** sigue sin aplicarse, con su motivo, está en
> `VERIFICACION_FILA_A_FILA.md` §cuarta pasada.

Al leer las tablas enteras —no solo la fila del nutriente que ya teníamos—
aparecieron factores que el motor no implementaba. **La mayoría ya están puestos**,
y esto es lo que queda:

| Tabla | Factor | Lo que dice | Convertido | Estado |
|---|---|---|---|---|
| SACN5 27-4 (obesidad) | Proteína | *«≥25%»* | ≥62,5 g/1000 kcal | ✅ aplicado 8-sep |
| SACN5 27-4 | Fibra | *«12 to 25%»* | 30-62,5 g/1000 kcal | ✅ aplicado (suelo 30) |
| SACN5 27-4 | Lisina | *«≥1.7%»* | ≥4,25 g/1000 kcal | ✅ aplicado |
| SACN5 27-4 | L-carnitina | *«≥300 ppm»* | ≥75 mg/1000 kcal | ✅ aplicado |
| SACN5 27-4 | Vitamina E | *«≥400 IU/kg»* | ≥67,1 mg/1000 kcal | ✅ aplicado |
| SACN5 27-4 | Grasa | *«Foods for weight loss should contain ≤9%»* | ≤22,5 g/1000 kcal | ⚠️ el motor topa en **30**, más flojo que la fuente — ver PREGUNTA 23 |
| SACN5 27-4 | Densidad energética | *«≤3.4 kcal ME/g»* MS | no transferible | ❌ es otra base: una ración cruda va a ~5,2 kcal/g de MS |
| SACN5 36-4 (cardiopatía) | **Taurina** | *«Dogs: ≥0.1%»* | **≥250 mg/1000 kcal** | ❌ no aplicado |
| SACN5 36-4 | **L-carnitina** | *«Dogs: ≥0.02%»* | **≥50 mg/1000 kcal** | ❌ no aplicado |
| SACN5 36-4 | **Fósforo** | *«Dogs: 0.2 to 0.7%»* | **500-1750 mg/1000 kcal** | ❌ no aplicado |
| SACN5 36-4 | Cloruro | *«1.5 x sodium levels»* | ligado al sodio | ❌ no aplicado |

*(El potasio y el magnesio cardíacos de esa misma tabla —≥0,4 % y ≥0,06 % MS— sí
quedan cubiertos: los mínimos de FEDIAF, 1450 mg y 200 mg/1000 kcal, son 0,58 % y
0,08 % MS, por encima de los dos.)*

**Lo que falta es de cardiopatía, y es trabajo, no pregunta**: la fuente da la
cifra. Se aplica midiendo antes, y solo se pregunta lo que no quepa.

> **PREGUNTA 29.** De la Tabla 36-4, la **taurina** es la única con matiz: FEDIAF no
> se la exige al perro porque la sintetiza, y SACN5 la pide en cardiopatía. ¿El suelo
> de 250 mg/1000 kcal vale para **cualquier** cardiopatía, o solo para la
> miocardiopatía dilatada, que es donde la respuesta está documentada?

### 8.2 · La grasa en pancreatitis — RESUELTO el 8 de septiembre

> **⚠️ Esta sección describe un problema que ya no existe, y se deja porque el
> razonamiento sigue siendo el bueno.** Se resolvió aplicando la fuente que
> manda: la grasa de la pancreatitis pasó de 20 a **37,5**, y a **25** si además
> hay obesidad o hiperlipidemia marcadas (Tabla 67-3, que gradúa en dos
> niveles). Lo que sigue vigente es el diagnóstico: era una constante que
> debería ser un rango. Ver §8.1-bis.

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

El motor aplica **37,5**, y **25** si además hay obesidad o hiperlipidemia
marcadas. Con eso el perro renal con pancreatitis sí recibe menú.

*Esto ya no es una pregunta. Lo que queda de aquí es la **PREGUNTA 21**, que es
otra cosa: si ese 37,5 es un número o un rango, y qué variable clínica lo mueve.*

### 8.5 · Las patologías sin límite numérico

> **⚠️ Actualizado el 8 de septiembre: son 47 perfiles, no 40, y las que no
> fijan ningún número ya no son 24.** El recuento exacto y por patología se lee
> de `GET /patologias`, que es el que no puede desincronizarse; aquí se deja el
> criterio, que no ha cambiado.

De las 47, **dieciocho no fijan ningún número**. Lo que sí hacen es excluir
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

> **PREGUNTA 30.**
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

## 11-bis · Lo que las fuentes dicen y el motor NO aplica (9 de septiembre)

Todas estas están **escritas en el repo con su fuente y su motivo**
(`patologias.json`, bloque `limites_escritos_que_el_solver_no_aplica`, y el
BLOQUE 55 de la batería vigila que sigan sin aplicarse). Ninguna se ha aplicado
en silencio y ninguna se ha tirado a la basura. Lo que falta es la decisión
clínica.

### 11-bis.1 · Oxalato: el fósforo, y las dos fuentes dicen lo contrario

Hoy el motor le pone al oxalato un **techo de fósforo de 1500 mg/1000 kcal**,
de SACN5 Tabla 40-5 (*«Dietary phosphorus should be in the range of 0.3 to 0.6%
DM»*).

Fascetti & Delaney cap.16 dice literalmente lo contrario: *«Dietary phosphorus
should not be restricted with calcium oxalate urolithiasis. **Low dietary
phosphorus is a risk factor** for calcium oxalate urolith formation in cats and
dogs»*, y recomienda **1,5-2,0 g/Mcal** — o sea que lo que una fuente da como
máximo aconsejable la otra lo da como **mínimo**.

> **PREGUNTA 31.** ¿Se restringe el fósforo en el oxalato cálcico canino, o no?
> Si no, ¿quitamos el techo o lo subimos a 2000? Equivocarse por abajo aquí
> **no es el lado seguro**, porque el fósforo bajo es factor de riesgo de la
> propia enfermedad, y por eso no lo hemos tocado nosotras.

### 11-bis.2 · Oxalato: el sodio, y la propia fuente dice que el debate está abierto

Hoy: techo de **750 mg/1000 kcal** (SACN5 Tabla 40-5, *«Dietary sodium should be
<0.3% DM»*).

Fascetti cap.16 apunta al revés: *«the **low** dietary sodium concentrations…
**increase** the risk… diets that contain **high** dietary sodium concentrations
**decrease** the risk»*, y a la vez reconoce que *«recommended concentrations…
**is debated**, as diets containing as low as 0,4 g/Mcal and as high as 3,5
g/Mcal are available commercially»*.

> **PREGUNTA 32.** Con un rango de mercado de casi diez veces, ¿qué techo (o
> qué suelo) de sodio tiene sentido en un perro con oxalato?

### 11-bis.3 · Oxalato: la proteína, que cae entera por debajo de FEDIAF

SACN5 Tabla 40-5: *«Restrict dietary protein to **10 to 18% dry matter**»* =
25-45 g/1000 kcal. El **mínimo** de FEDIAF para el adulto son **52,1**, así que
el techo entero de la fuente está por debajo del suelo del perro sano: no existe
ningún número que cumpla las dos cosas. Y una ración BARF real de este motor
ronda los **105 g/1000 kcal**, más del doble del techo de la tabla.

> **PREGUNTA 33.** ¿Es esta una de las que solo puede pautar un colegiado (la
> «fase 4»: una prescripción declarada, por debajo de FEDIAF, que viaja con el
> menú y contra la que se verifica)? ¿O el objetivo realista en una ración
> cruda es simplemente «no pasarse», y entonces cuál es el número?

### 11-bis.4 · Dermatosis por zinc: la dosis del ensayo está por encima del máximo legal

Fascetti cap.14, citando a NRC 2006: *«The combination of **zinc (100 mg/1000
kcal) and linoleic acid (15 g/1000 kcal)** produced statistically significant
improvements in coat gloss and decreased TEWL over a nine-week period in dogs»*.
Y van juntas a propósito: la misma fuente dice que *«EFA deficiency impairs zinc
absorption»*.

Nuestro suelo de zinc es **25** (SACN5 Tabla 32-1, extremo bajo). Medido: con el
zinc en 100 **no sale menú a ningún peso**; con 60, 75 y 90 tampoco, ni bajando
la escalera entera. Zinc 50 solo sí sale, y linoleico 15 solo también; lo que no
existe es la combinación, que es justo lo que la fuente probó.

Y hay un motivo que no es del catálogo: **100 mg/1000 kcal está por encima del
máximo LEGAL de la UE** (22,70 mg/100 g MS = 56,75 mg/1000 kcal). Esa dosis no
se puede vender en un alimento completo en Europa.

> **PREGUNTA 34 — replanteada el 9 de septiembre, leyendo el cap.14 de Fascetti
> entero. La fuente dice que la pregunta está mal hecha: no pide más zinc en la
> DIETA, pide un suplemento.** Literal:
> *«Therapy requires zinc supplementation with a recommended dosage of **2–3 mg/kg/
> body weight (BW) of elemental zinc** in the form of zinc sulfate, zinc gluconate,
> or zinc methionine (White et al. 2001). Zinc oxide should not be used as it is not
> very bioavailable.»*
> Y sobre el síndrome I, que es el de las razas nórdicas de nuestra ficha:
> *«Skin lesions develop **despite adequate consumption of diets with sufficient
> bioavailable zinc**»*, porque *«these dogs have a genetic defect in the intestinal
> absorption or the metabolism of zinc»*.
> Puesto en nuestras unidades se ve por qué chocaba con el techo legal: un perro de
> 20 kg necesita **40-60 mg de zinc elemental al día**, que con un DER de ~1000 kcal
> son 40-60 mg/1000 kcal **además** de la dieta, y el techo legal es 56,75 mg/1000
> kcal en total. El suplemento terapéutico solo ya se lo come entero. No es que el
> catálogo se quede corto: **es que esto no se hace con comida**.
> Y la segunda mitad la contesta también: el linoleico no actúa por su cuenta, es
> coadyuvante — *«EFA deficiency impairs zinc absorption, and supplementation with
> EFAs appears to enhance zinc absorption... the clinical signs of zinc deficiency can
> be partially reversed by supplementing with EFA»*, con el mecanismo escrito (la
> delta-6-desaturasa necesita zinc como cofactor).
> **Lo que queda es de producto**: esta patología debería decir «necesita un
> suplemento de zinc pautado, no un menú con más zinc», que es lo que dice la fuente.
>
> *(La pregunta como estaba:)* Con el techo legal en 56,75, ¿cuánto zinc tiene sentido
> pedirle a esta patología? ¿Y el linoleico de 15 g/1000 kcal (cinco veces el
> mínimo de FEDIAF) aporta algo por sí solo, sin el zinc?

### 11-bis.5 · El ratio omega-6:omega-3, que es lo que preguntó Cris

SACN5 lo da para cuatro patologías, y el cap.37 lo dice explícitamente: *«These
recommendations are similar to omega-3 fatty acid content and omega-6:omega-3
ratios recommended for dogs and cats with cancer, osteoarthritis and
inflammatory skin diseases»*.

| patología | ratio que pide SACN5 | dónde |
|---|---|---|
| Enfermedad renal crónica | 1:1 a 7:1 | cap.37 |
| Cáncer | «approximating 1:1» / «as close to 1:1 as possible» | cap.30 |
| Artrosis | **menos de 1:1** | cap.34 |
| Reacción adversa al alimento | *«currently unknown»* | cap.31 |

Y **para el perro sano no hay ninguno en ninguna fuente que tengamos.** El NRC
2006 cap.5 dice literalmente que el ratio de totales *«is not helpful»* porque
mezcla ácidos grasos de potencia muy distinta, y recomienda en su lugar el ratio
**linoleico:linolénico**, que el motor sí aplica desde el 9 de septiembre (2,6-26
en adulto y crecimiento, 2,6-16 en gestación y lactancia).

*Esto es la mitad de la **PREGUNTA 40**, donde está la pregunta entera con las
tres fuentes juntas. Lo que hay que añadir aquí es la consecuencia práctica: el
ratio de totales se cumple metiendo aceite de pescado, y el aceite de un menú de
este motor ya llega a **25,3 g** en el peor caso.*

### 11-bis.6 · Y una que ya estaba, y sigue igual

El **selenio de la disfunción cognitiva** (SACN5 Tabla 35-3, 0,5-1,3 mg/kg MS =
125-325 µg/1000 kcal). El rango empieza 12 µg por debajo del máximo de FEDIAF
(142) y termina en 325, **dos veces y media** ese máximo. Medido: con el suelo en
125 salen los cinco perros de prueba, pero su selenio real queda entre el **88 %
y el 98 % del máximo de FEDIAF**, y el selenio es uno de los cinco límites de
toxicidad crónica del motor. **No se aplica**: un techo existe para no vivir en
él.

> **PREGUNTA 36.** ¿Merece la pena acercar el selenio al techo de FEDIAF en esta
> patología, o el margen de 3 µg es demasiado poco para un nutriente con
> toxicidad crónica documentada?

---

## 11-ter · El urolito compuesto: dos patologías marcadas y la fuente dice que se trata una

**SACN5 cap.45** («Canine Compound Urolithiasis»), leído entero el 9 de
septiembre. Los urolitos compuestos —núcleo de un mineral con capas de otro— son
el **7 %** de los urolitos caninos analizados en Minnesota, y el primer ejemplo
que pone el capítulo es *«a nucleus of 100 % calcium oxalate monohydrate
surrounded by a shell of 80 % magnesium ammonium phosphate»* — o sea oxalato por
dentro y estruvita por fuera.

Y la regla de manejo, literal:

> *«it seems logical to recommend management protocols designed primarily to
> minimize recurrence of minerals composing the **nucleus** (rather than those in
> shells) of compound uroliths»*

**Qué hace hoy el motor:** si se marcan `oxalato` y `estruvita` a la vez, combina
los dos juegos de límites con `min()` y no dice nada. Las otras tres parejas de
urolitos sí se paran, pero **por casualidad**: `urato` y `cistina` están marcadas
«sin dieta automática» porque necesitan bajar de FEDIAF, no porque sean
incompatibles con nada.

**Por qué no lo he bloqueado yo:** cuál es el núcleo sale del **análisis de la
piedra**, que la app no tiene y no puede deducir. Bloquear dejaría sin menú a
quien marcó dos casillas sin tener un urolito compuesto.

> **PREGUNTA 37.** Con dos tipos de urolito marcados, ¿qué debe hacer la app?
> Tres opciones: (a) preguntar por el análisis y aplicar solo el del núcleo,
> (b) bloquear y mandar al veterinario, o (c) seguir combinando y avisar. La (a)
> es la que dice la fuente, y necesita un dato que hoy no pedimos.
> **PREGUNTA 38.** ¿Hay más parejas de patologías cuyos límites no deban
> combinarse? El motor hoy combina siempre con `min()`, que es lo seguro para un
> techo pero puede no ser lo correcto clínicamente.

---

## 11-quater · Lo que salió de leer los últimos capítulos de SACN5 (9 de septiembre, tarde)

Con esto queda **leído entero todo lo canino de SACN5**: de los 70 capítulos, los
5 que siguen sin citarse en el repo son felinos o de otras especies (22, 23, 24,
46 y 70). Estas son las preguntas que salieron y que **no puede decidir el
asistente**.

### PREGUNTA 39 — El omega-3 tiene dos caras y las dos están escritas. ¿Dónde está el techo?

**Lo que pide una parte del libro.** Las tablas de **cáncer** y de **artrosis**
piden omega-3 en cantidades que el catálogo real no alcanza. Las dos están en
`limites_escritos_que_el_solver_no_aplica` de `patologias.json`, con su medida.

**Lo que dice otra parte, cap.25, y no lo teníamos:**

> *«Chronic suppression of the inflammatory and/or immune response by feeding
> high levels of omega-3 fatty acids should be done cautiously and **is not
> warranted in disease states in which a fully competent immune system is
> essential for survival and recovery**.»*

Con dos medidas: ratones prealimentados con el **40 % de las calorías como aceite
de pescado** tenían comprometida la resistencia a la infección (Chang et al,
1992), y gatos sanos con **omega-6:omega-3 de 1,3:1** durante ocho semanas tenían
la **función plaquetaria significativamente disminuida** (Saker et al, 1998).

**Lo que hemos podido contestar nosotras, buscándolo:** no hay cifra canina. Las
dos medidas que da el capítulo son de otras especies —ratones al 40 % de las
calorías y gatos a 1,3:1— y el único número aplicable al perro que existe en el
repo es el **SUL de EPA+DHA del NRC 2006: 2,8 g/1000 kcal**, que el motor ya
aplica como promedio semanal.

**La pregunta**: ¿vale ese SUL como techo de omega-3, o hace falta uno de omega-3
totales? Y si hace falta: si existe un techo, la respuesta a por qué los suelos de
cáncer y artrosis no caben deja de ser «el catálogo no llega» y pasa a ser «no
habría que llegar».

### PREGUNTA 40 — El ratio omega-6:omega-3: dos fuentes que no dicen lo mismo

Es la primera de las tres que Cris echó de menos en `REVISION_NUTRICIONISTA.md`, y
ahora hay material para decidirla:

| Fuente | Qué dice |
|---|---|
| **NRC 2006, cap.5** | Del ratio de **totales**: *«is not helpful»*, porque mezcla ácidos grasos de potencia muy distinta. Recomienda en su lugar el **linoleico:linolénico** |
| **SACN5**, cuatro patologías | Renal 1:1 a 7:1 (cap.37) · cáncer «as close to 1:1 as possible» (cap.30) · artrosis menos de 1:1 (cap.34) · reacción adversa «currently unknown» (cap.31) |
| **SACN5 cap.25** | **5:1 a 1:1** «depending on patient assessment», y añade que **no está estandarizado** |
| **Lo que hace el motor hoy** | Aplica el **linoleico:linolénico** (2,6-26 en adulto y crecimiento, 2,6-16 en gestación y lactancia), que es lo que dice el NRC. El de totales **no existe** |

**Para el perro sano no hay ratio en ninguna fuente que tengamos.** Todos los de
arriba son de patología.

**La pregunta**: ¿se queda así? Nuestra lectura es que sí —el de totales lo
desaconseja la fuente primaria, y el rango del cap.25 es para el paciente crítico
y sin estandarizar— pero es una decisión clínica, no aritmética, y quien firma
tiene que poder decir por qué el ratio que le pidieron no está. Si la respuesta es
que sí se aplica en esas cuatro patologías, hay que contar con que se cumple
metiendo aceite de pescado, y el aceite de un menú de este motor ya llega a
**25,3 g** en el peor caso.

### PREGUNTA 41 — La lactosa: hay umbral, hay lácteo y no hay dato

**El umbral, con cifra** (SACN5 cap.55, recuadro 55-3): *«dogs developed diarrhea
while consuming more than **1 g of lactose/kg body weight**»*. Y el cap.59 pide
las dietas de intestino corto **«lactose free»**.

**Lo que hay**: un lácteo en el catálogo, «Yogur griego», en Extras. **0 de los
216 menús del catálogo lo usan** hoy, pero Extras va siempre libre, así que un
menú personalizado sí puede meterlo.

**Lo que falta**: la lactosa no es uno de los 41 nutrientes, así que el motor no
sabe cuánta lleva. Con 4 g/100 g el tope saldría en **25 g de yogur por kg de
peso** — 75 g para un perro de 3 kg.

**La pregunta**: cuando el dato esté, ¿esto es un **tope de seguridad** (como el
mercurio del atún, que también se mide por peso del perro) o solo un **aviso**?
El mercurio se acumula y una diarrea no; el criterio es tuyo.

### PREGUNTA 42 — Los avisos de fármaco: ¿faltan más?

De leer entero el cap.69 («Effects of Food on Pharmacokinetics») han entrado dos
avisos nuevos, y los dos describen algo que pasa **por culpa del cambio de dieta
que hace esta app**:

- **Bromuro potásico** (epilepsia): bromo y cloro compiten por la reabsorción
  tubular renal. Una ración de este motor lleva **la mitad de cloro** que la
  comida que mantenía estable al perro del caso 69-1 (mediana 826 mg/1000 kcal =
  0,33 % MS, contra 0,65 %). Menos cloro es **más bromo en sangre**: el riesgo va
  hacia la toxicidad, no hacia la crisis.
- **Mitotano** (Cushing): en ayunas la absorción cae de 13,0 a **0,4 mg/l**. La
  pastilla va con la comida.

**Lo que hemos podido contestar nosotras:** en el capítulo entero, esos **dos son
los únicos con cifra canina**. Hay un tercero con dirección pero sin número —el
fenobarbital, cuya vida media se acorta al restringir proteína o grasa— y está
recogido en el mismo aviso. Del resto, el capítulo da el mecanismo general
(proteína alta acelera el metabolismo hepático de muchos fármacos) y todos los
números son de personas o de rata.

**La pregunta**: ¿hay más fármacos frecuentes en el perro cuya pauta cambie al
pasar a una ración cruda, alta en proteína y sin cereales? Es una pregunta de
consulta, no de bibliografía: lo que se ve en la práctica.

---

## 11-quinquies · Lo que salió de leer FEDIAF y SACN5 **enteras** (10 de septiembre)

Las dos fuentes se habían leído «enteras» varias veces y cada vez aparecía algo
más. Esta vez se hizo con método: extraer mecánicamente de cada sección **todas**
sus cifras con unidad y **todas** sus frases normativas, y dar veredicto a cada
una (`leer_fuente.py`); y contar las tablas sin cortar la salida — **476 tablas**
en SACN5, **121** de «Key nutritional factors».

**Lo que cambia el motor** (los tres, con su medida):

| Qué | De dónde | Efecto medido |
|---|---|---|
| Suelo de **DHA** en crecimiento y reproducción, 0,05 g/1000 kcal | SACN5 Tablas 15-5, 17-1 y 33-5 | 0 de 10 menús por debajo. No cambia ninguno hoy |
| **Histamina**: aviso en atún, caballa, sardina y boquerón | FEDIAF §7.6.2.4 | Aviso, no tope: la genera la mala conservación y es termorresistente |
| **Uva y pasa**, prohibidas | FEDIAF §7.7.1 | Faltaba la sección entera. 2,8 g de pasas/kg de peso |

**Lo que se corrigió porque era falso:**

- Se había escrito que SACN5 declara **3,5 kcal/g** de materia seca y que por
  tanto 68 cifras de patología estaban un 14 % apretadas de más. **No.** De las
  24 tablas que cita el motor, **una sola declara densidad** —la 13-3— y dice
  **4,0**. Las 88 cifras se reproducen desde las filas de sus tablas a 4,0, y
  ahora eso lo **rehace una auditoría** en cada batería en vez de creerse una
  frase escrita en un comentario.
- El aviso de **cardiopatía B2** decía al dueño «sodio bajado a 900 mg/1000 kcal»
  y el motor aplica **739**; el de **estadio C** decía 790 y aplica **625**. Los
  topes bajaron el 8 de septiembre y los avisos se quedaron.

**Lo que la fuente cuantifica y sigue SIN aplicarse, porque falta una pregunta
en la ficha y no un número:**

- **El frío.** SACN5 Tabla 5-3 da el aumento del DER por tipo de pelo: **+95 %**
  en pelo corto y **+59,5 %** en pelo largo al pasar de 25 °C a 7,6 °C; +25 % en
  labrador y beagle; +22 % en gran danés. La app no pregunta dónde duerme el
  perro. **PREGUNTA para vosotras: ¿se pregunta, y con qué palabras?**
- **La masa muscular.** FEDIAF Tabla VII-3, escala de 0 a 3 por palpación. Se ha
  aplicado la **salvedad** —en la parte baja del BCS el peso objetivo puede
  quedarse corto porque lo que falta puede ser músculo— pero no la escala.

**Y el umbral que FEDIAF no da y SACN5 sí:** FEDIAF dice que «as the calcium
level approaches the stated nutritional maximum, it may be necessary to increase
the levels of certain trace elements such as **zinc and copper**» y **no dice
desde cuándo**. La Tabla 32-1 de SACN5 lo publica: **calcio >1,5 % MS**, o sea
3750 mg/1000 kcal — el **60 %** del máximo de FEDIAF, no el 90 %. Lo que sigue
sin existir en ninguna de las dos es **cuánto** hay que subir el zinc.

**Las nueve tablas de recomendación canina que el motor no ofrece** están leídas
enteras y con sus números en `PENDIENTE_PRODUCTO.md`. Dos de las nueve resultan
estar **cerradas**: la 53-2 (vólvulo), cuyo único factor nutricional es el tamaño
del bocado —ya está en el aviso—, y la 47-4 (periodontal), cuyas cifras de
fósforo y sodio son **las mismas** que las del perro adulto sano que ya
aplicamos.

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
