# Las patologías, una por una

**8 de septiembre de 2026.** Escrito verificando cada cifra contra su fuente
original, no contra lo que decía el repo. Para cada patología: qué aplica el
motor, la **cita literal** de la fuente, el **techo duro** que nadie puede pasar
y de dónde sale, y **qué margen le queda al profesional**.

Sustituye a leer `patologias.json` a pelo. Los números siguen viviendo allí —
este documento no es una segunda copia, es su lectura. Si un número de aquí no
coincide con el JSON, manda el JSON y este documento está caducado.

---

## 0 · Cómo se lee

Cada ficha lleva cuatro cosas, y las cuatro importan:

- **Aplica** — lo que el motor hace hoy, con el número exacto.
- **Fuente** — la cita literal, con su conversión a por-1000-kcal. Todas las
  tablas de SACN5 llevan la nota «*Nutrients expressed on a dry matter basis*»,
  así que la conversión es **× 2,5** (a la densidad de referencia de 4000 kcal
  EM/kg de materia seca). Está comprobada nota al pie por nota al pie.
- **Techo duro** — el límite que **nadie** mueve, y por qué es duro. Tres
  orígenes posibles:
  · **Legal** — máximo `(L)` de FEDIAF, Reglamento (UE) 2017/1492 sobre
    aditivos. No lo mueve ni un veterinario.
  · **Seguridad crónica** — los cinco topes del motor (vitamina D, yodo,
    selenio, mercurio, tiaminasa).
  · **Mínimo de FEDIAF** — se puede cruzar, pero al cruzarlo el resultado deja
    de ser un menú y pasa a ser una **prescripción firmada** (`necesita_bajo_fediaf`).
- **Margen** — entre qué y qué puede moverse el profesional, según la regla
  adoptada en `DECISIONES.md` D-13: **por defecto puede mover cualquier valor de
  patología, en cualquier dirección**, salvo lo marcado como legal o de
  seguridad.

Y una quinta línea cuando aplica: **⚠️ Lo que la fuente pide y NO aplicamos.**
Esa línea aparece en 13 de las 19 patologías con cifras, y es el hallazgo más
grande de esta revisión.

---

## 0-bis · Lo aplicado el 8 de septiembre

Este documento se escribió como diagnóstico y **los cambios ya están hechos**. Lo
que sigue describe el estado tras aplicarlos; donde algo se corrigió, se dice qué
había antes, porque el error es parte de lo que hay que poder auditar.

**Cuatro correcciones:**

| | Antes | Ahora | Medido |
|---|---|---|---|
| Sodio cardíaco (genérica y B2) | 900 | **739** | verde, sodio real 501 y 485 |
| Sodio cardíaco (C) | 790 | **625** | verde, 499 |
| Grasa en pancreatitis | 20 | **37,5** | verde en peldaño 5; **renal+pancreatitis vuelve a dar menú** |
| Suelo de artrosis | sobre `epa_dha` | sobre **`epa`** | verde, EPA real 1,2 |

Más la atribución de fuente de la cardiopatía genérica, que citaba a ACVIM unas
cifras que ACVIM no da.

**Siete factores nuevos**, todos de la tabla de la propia patología y todos por
encima del mínimo de FEDIAF (ninguno necesita prescripción). Medidos por el camino
real: **los siete resuelven en el peldaño estricto, sin bajar ni un escalón**.

| Patología | Factor añadido | Menú medido |
|---|---|---|
| `renal` | sodio ≤ **750** | verde, sodio 466 (22 kg) · 547 (8 kg) |
| `diabetes` | fibra ≥ **17,5** | verde, fibra 27,7 |
| `obesidad` | proteína ≥ **62,5** | verde, proteína 159,8 (22 kg) · 170,0 (8 kg) |
| `ple_linfangiectasia` | proteína ≥ **62,5** · fibra ≤ **12,5** | verde, 144,9 y 2,2 (22 kg) · 144,3 y 2,5 (40 kg) |
| `insuficiencia_pancreatica_exocrina` | fibra ≤ **12,5** | verde, fibra 0,6 |
| `enteropatia_cronica` | grasa ≤ **37,5** · proteína ≥ **62,5** | verde, 37,5 y 148,8 — **antes no aplicaba nada** |

**Uno que se decidió NO añadir**, y el motivo importa: el ácido linoleico de la
Tabla 32-1 (dermatosis y atopia, *«Dogs: Linoleic acid >1.0% DM»* = 2,5 g/1000
kcal). El **mínimo de FEDIAF para un adulto ya es 3,3**, o sea más exigente. Un
suelo de 2,5 se combina con `max()` contra el de FEDIAF y no cambiaría ni un menú:
sería un número en el JSON que no hace nada, y eso es exactamente lo que hace que
una tabla deje de leerse. Queda escrito aquí y no en los datos.

**Lo que sigue pendiente** está en §5.

---

## 1 · Lo que está MAL y hay que arreglar

Cinco cosas. Ninguna es un número inventado; son atribuciones, unidades y
criterios.

### 1.1 · La cardiopatía genérica atribuye a ACVIM unas cifras que ACVIM no da

`patologias.json`, entrada `cardiopatia`, dice literalmente:

> «ACVIM da el sodio por estadio: B2 80-99 mg/100 kcal, C 50-79, D <50»

**Verificado contra el consenso original** (Keene BW, Atkins CE, Bonagura JD et
al., *ACVIM consensus guidelines for the diagnosis and treatment of myxomatous
mitral valve disease in dogs*, J Vet Intern Med 2019;33:1127-1140): **el
consenso no da ni una sola cifra de sodio, en ninguna etapa.** Es cualitativo
de principio a fin:

| Etapa | Lo que dice ACVIM 2019, literal |
|---|---|
| B1 | sin recomendación dietética |
| B2 | *«mild dietary sodium restriction and provision of a highly palatable diet with adequate protein and calories»* |
| C | *«Modestly restrict sodium intake, taking into consideration sodium from all dietary sources… and avoid any processed or other salted foods»* |
| D | *«attempts should be made to further decrease dietary sodium intake if it can be done without compromising appetite or renal function»* |

Las cifras 80-99 / 50-79 / <50 mg/100 kcal salen de otro sitio: **Cavanaugh SM,
DVM MS DACVIM (cardiología), «Understanding nutrition in dogs with degenerative
mitral valve disease», Veterinary Practice News, 6 de julio de 2020**, que las
presenta como su lectura práctica del consenso y cita a Keene como fuente.

Es una fuente legítima —una diplomada del ACVIM en cardiología, publicada— pero
**es opinión de experta en una revista profesional, no un consenso ni un libro
de texto revisado por pares**. Es el eslabón más débil de toda la cadena de
fuentes del motor, y sostiene **cuatro números**.

Lo que hay que corregir es la atribución, no el número: las entradas por estadio
(`cardiopatia_b2/_c/_d`) ya lo dicen bien; la genérica, no.

### 1.2 · El oxalato cálcico no ajusta nada

`oxalato` es formulable y su **único** tope es la vitamina D a 14,1875 µg… que
es el **máximo legal de FEDIAF que ya se aplica a cualquier perro**. Su propio
`por_que` lo admite: *«No es un tope propio de la patología»*.

O sea: se marca oxalato, sale menú, sale verde, y **no se le ha ajustado nada**.

La Tabla 40-5 de SACN5 pide siete cosas, verificadas literalmente:

| Factor | Cita literal | Por 1000 kcal |
|---|---|---|
| Proteína | *«Restrict dietary protein to 10 to 18% dry matter»* | 25-45 g — **bajo el mínimo de FEDIAF (52,1)** |
| Calcio | *«Restrict dietary calcium to 0.4 to 0.7% DM»* | 1000-1750 mg |
| Fósforo | *«Dietary phosphorus should be in the range of 0.3 to 0.6% DM»* | 750-1500 mg |
| Ca:P | *«maintain a normal Ca:P ratio (1.1:1 to 2:1)»* | ratio |
| Sodio | *«Dietary sodium should be <0.3% DM»* | <750 mg |
| Magnesio | *«in the range of 0.04 to 0.15% DM»* | 100-375 mg (**con techo**) |
| Vitamina C | *«Avoid pet foods, supplements or human foods that contain ascorbic acid»* | exclusión de alimento |
| Oxálico | *«Avoid foods high in oxalic acid (Table 40-3)»* | exclusión de alimento |

De estas ocho, **cinco son implementables hoy** sin bajar de FEDIAF: fósforo,
Ca:P, sodio, magnesio y las dos exclusiones. La del calcio es la que tiene el
conflicto de fuentes ya documentado (SACN5 dice bajarlo, Today's Veterinary
Practice 2025 citando a Carr 2020 dice que bajarlo empeora el problema) y se
mantiene sin tocar, que es la posición conservadora.

### 1.3 · La artrosis mide el nutriente equivocado

**Aplica:** suelo de `epa_dha` ≥ 1,0 g/1000 kcal.
**La fuente** (SACN5 Tabla 34-2) dice: *«Eicosapentaenoic acid 0.4 to 1.1%»* —
**EPA sola**, no EPA+DHA.

Exigir que la **suma** llegue a 1,0 es más laxo que exigir que **el EPA** llegue
a 1,0: un menú con 0,3 de EPA y 0,7 de DHA pasa nuestro filtro y no cumple la
fuente. No es un número mal copiado; es el nutriente equivocado.

Y la misma tabla pide dos cosas más que no miramos: **omega-3 totales 3,5-4,0 %
MS = 8,75-10 g/1000 kcal** y **L-carnitina ≥300 mg/kg MS = 75 mg/1000 kcal**. El
suelo de omega-3 totales coincide casi exactamente con el que exige el
Reglamento (UE) 2020/354 para la misma indicación (≥8,24), o sea que dos fuentes
independientes piden lo mismo y nosotros no pedimos ninguna.

### 1.4 · Tres de los cuatro sodios cardíacos superan el techo legal europeo

Reglamento (UE) 2020/354, entrada 24: sodio ≤ 2,6 g/kg = **738,6 mg/1000 kcal**.
El motor: 900 (genérica), 900 (B2), 790 (C), 480 (D). Las tres primeras están
por encima.

No es una infracción nuestra —no vendemos pienso— pero sí significa que un menú
nuestro «para cardiópata» puede llevar más sodio del que Europa admite para
llamarse dieta cardíaca. Ver `DECISIONES.md` D-12.

### 1.5 · La pancreatitis usa Merck cuando la regla adoptada manda SACN5

**Aplica:** grasa ≤ 20 g/1000 kcal.
**Fuente:** Merck Veterinary Manual, verificado literal el 8 de septiembre:
*«In dogs, feeding a low-fat diet (ie, less than 20 g fat/1,000 kcal) is crucial
for treatment success»* y *«In dogs, a ration with less than 20 g fat/1,000 kcal
should be chosen»*. Es **una cifra única, no un rango**, y **no distingue aguda
de crónica**.

Pero la regla de este proyecto es: manda FEDIAF; donde FEDIAF no llega, SACN5.
FEDIAF no cubre la pancreatitis. **SACN5 sí** (Tabla 67-3, verificada):
*«≤15% for non-obese and non-hypertriglyceridemic dogs»* = **37,5 g/1000 kcal**,
y *«≤10% for obese and/or hypertriglyceridemic dogs»* = **25 g**.

**Aplicado el 8 de septiembre: 20 → 37,5.**

⚠️ **Y midiendo el cambio salió algo más gordo, que no tiene que ver con el
número: los dos topes de esta patología son incompatibles entre sí**, y ya lo
eran con los 20 anteriores. Medido en peldaño estricto, adulto de 22 kg:

| | Resultado |
|---|---|
| proteína ≤75, grasa ≤45 · 50 · 55 · 60 · 65 | **ninguno da menú** |
| grasa ≤37,5, proteína ≤90 · 105 · 120 · 135 | **ninguno da menú** |
| proteína ≤75 con la grasa suelta | sale, con grasa **77,6** |
| grasa ≤37,5 con la proteína suelta | sale, con proteína **148,2** |

Es aritmética de energía: 37,5 g de grasa más 75 g de proteína son unas **600 de
las 1000 kcal**, y las otras 400 tendrían que venir de carbohidrato — que una
ración cruda apenas tiene. La dieta de pancreatitis que describe SACN5 (45 % de
la materia seca entre proteína y grasa, el resto carbohidrato) **es un pienso, no
un BARF**.

**No hay que bloquear la patología: la escalera ya lo resuelve, y estaba puesta
para esto.** Medido por el camino real (recorriendo `_escalera_de_relajacion`):

| Perro | Resultado |
|---|---|
| Adulto 8 kg | verde en el **peldaño 5**, grasa 37,5 · proteína 73,2 |
| Adulto 22 kg | verde en el **peldaño 5**, grasa 37,5 · proteína 74,8 |
| Adulto 35 kg | verde en el **peldaño 5**, grasa 25,8 · proteína 74,9 |

El peldaño 5 es `tope_maximo_de_visceras_higado_y_verdura`, que suelta el techo
del 10 % de «Verduras y frutas» — y su comentario en `main.py` lo puso ahí
**exactamente por un caso de pancreatitis**. O sea que la pancreatitis **siempre**
cae al último peldaño, y por la regla 5 eso se le dice a quien pide el menú.

Consecuencia práctica que hay que escribir en la pantalla: un menú de pancreatitis
lleva mucha más verdura de la que lleva un BARF normal. No es un fallo — es lo que
pide la fuente.

**Y el cambio resuelve el caso que motivó todo el diagnóstico de choque.** Medido
por el camino real:

| Combinación | Antes (grasa ≤20) | Ahora (grasa ≤37,5) |
|---|---|---|
| **renal + pancreatitis** | sin menú en ningún tamaño | **verde**, peldaño 5, grasa 37,5 · fósforo 1198,8 |
| obesidad + pancreatitis | — | **verde**, peldaño 5, grasa 27,4 (manda el 30 de obesidad) |

El choque que se diagnosticó era **renal fósforo ≤1200 contra pancreatitis grasa
≤20**. Con la grasa en el valor que pide la fuente, el choque desaparece: no había
una incompatibilidad clínica entre las dos patologías, había un número que no era
el de la fuente que manda.

---

## 2 · Las 19 con cifra, una por una

Los mínimos de FEDIAF que se citan como techo de apretado son los de un adulto a
DER 95 (proteína 52,1 g · grasa 13,75 g · fósforo 1160 mg · sodio 290 mg · cobre
2,08 mg · zinc 20,8 mg · EPA+DHA 0,11 g por 1000 kcal). **Escalan hacia arriba
cuando el perro come menos** (`minimo_de()`, ecuación FEDIAF 7.2.5), así que en
un perro pequeño el margen de apretado es más corto que el que sale aquí.

### 2.1 · Insuficiencia renal crónica · `renal`

- **Aplica:** fósforo ≤ **1200** mg/1000 kcal. Solo en adulto; en crecimiento bloquea.
- **Fuente:** SACN5 cap. 37, Tabla 37-9, verificada literal: *«Phosphorus 0.2 to
  0.5% in foods for dogs»* → **500-1250 mg/1000 kcal**. Los 1200 caen dentro, en
  el extremo menos restrictivo.
- **Techo duro:** por abajo, el **mínimo de FEDIAF, 1160 mg**. Bajar de ahí es
  prescripción. Por arriba, el Reglamento (UE) 2020/354 entrada 10 pone
  **1420 mg** para poder llamarse dieta renal.
- **Margen del profesional:** **1160 → 1420**. Son 260 mg de ancho, un 22 %. El
  motor vive en 1200, casi pegado al suelo.
- ⚠️ **Lo que la fuente pide y NO aplicamos:** la misma Tabla 37-9 pide además
  **sodio ≤0,3 % MS = ≤750 mg**, **potasio 0,4-0,8 % = 1000-2000 mg** (con
  techo), **omega-3 0,4-2,5 % = 1,0-6,25 g** y **vitamina E ≥400 UI/kg**. De
  esos, el sodio es el que más pesa clínicamente y no lo tocamos. Y el
  Reglamento 2020/354 añade un techo de **proteína ≤62,5 g**, que está por
  encima del mínimo de FEDIAF y por tanto **no necesita firma** — hoy no existe.

### 2.2 · Insuficiencia renal moderada-grave · `renal_avanzada`

- **Aplica:** fósforo ≤ 1200 (idéntico a `renal`). No formulable.
- **Por qué no formulable:** su objetivo real es la **proteína**, 35-50 g/1000
  kcal (Tabla 37-9: *«Protein 14 to 20% in foods for dogs»*), y eso está bajo el
  mínimo de FEDIAF (52,1).
- ⚠️ **El problema:** como el fósforo es el mismo y la proteína no está modelada,
  `renal` y `renal_avanzada` **se comportan exactamente igual** en el solver. La
  distinción clínica no existe dentro del motor.

### 2.3 · Pancreatitis · `pancreatitis`

- **Aplica:** grasa ≤ **20** g y proteína ≤ **75** g/1000 kcal.
- **Fuente de la grasa:** Merck (ver §1.5). **De la proteína:** SACN5 Tabla 67-3,
  *«Protein 15 to 30% for dogs»* → 37,5-75 g; usamos el extremo alto.
  El motivo está en el propio texto y no es obvio: *«Free amino acids (i.e.,
  phenylalanine, tryptophan and valine) in the duodenum are a strong stimulus for
  pancreatic secretion, in fact, more so than fat»* — el exceso de proteína
  estimula el páncreas **más que la grasa**.
- **Techo duro:** grasa, mínimo FEDIAF **13,75**; proteína, mínimo FEDIAF
  **52,1**. Ni FEDIAF ni el Reglamento 2020/354 cubren la pancreatitis, así que
  **no hay techo legal por arriba**: el margen hacia arriba solo lo acota el
  criterio.
- **Margen del profesional:** grasa **13,75 → sin techo legal** (SACN5 pone
  25 o 37,5 según el perro); proteína **52,1 → 75**.
- ⚠️ **Frontera física medida:** por debajo de ~26-28 g de grasa no hay menú con
  el catálogo real. El valor actual (20) está por debajo de esa frontera.

### 2.4 · Cálculos de oxalato cálcico · `oxalato`

Ver §1.2. **Aplica** solo vitamina D ≤14,1875 µg, que es el máximo legal general.
**Techo duro:** ése, y es **legal** — no lo mueve nadie.
**Margen del profesional:** ninguno sobre lo que hay hoy, porque lo que hay hoy
es un límite legal. Todo lo específico de la patología está sin implementar.

### 2.5 · Hepatopatía por acúmulo de cobre · `hepatopatia`

- **Aplica:** cobre ≤ **2,4** mg/1000 kcal. **No formulable** (bloquea).
- **Fuente:** Center SA et al., JAVMA 264(2):171-180, 2026 (límite tolerable
  0,24 mg/100 kcal). **Triplemente corroborado**: SACN5 Tabla 68-8 da
  *«Copper ≤5 mg/kg»* MS = **1,25 mg/1000 kcal**, y el Reglamento (UE) 2020/354
  entrada 28 pone **≤8,8 mg/kg = 2,50 mg/1000 kcal**. Los 2,4 del motor quedan
  justo por debajo del techo legal europeo.
- **Techo duro:** por arriba, **2,50 legal europeo**. Por abajo, el **mínimo de
  FEDIAF 2,08**, y el objetivo terapéutico real (1,2) está **por debajo** de él:
  por eso bloquea.
- **Margen del profesional:** **2,08 → 2,50**. Estrechísimo, 0,42 mg. Por debajo
  de 2,08 es prescripción.
- ⚠️ La misma Tabla 68-8 pide además **proteína 15-20 % MS = 37,5-50 g** (también
  bajo FEDIAF), **taurina ≥0,1 % = 250 mg**, **zinc >200 mg/kg = >50 mg**,
  **hierro 80-140 mg/kg = 20-35 mg** y **sodio 0,08-0,25 % = 200-625 mg**. La
  hepatopatía real está bajo el suelo nutricional en **dos** ejes, no en uno.

### 2.6 · Cardiopatía · `cardiopatia`, `_b1`, `_b2`, `_c`, `_d`, `_a`

- **Aplica:** sodio ≤ **900** (genérica y B2), **790** (C), **480** (D). B1 y A
  sin tope, a propósito.
- **Fuente real:** Cavanaugh SM, Veterinary Practice News, 6-jul-2020 (ver §1.1).
  ACVIM 2019 **no da cifras**. SACN5 Tabla 36-4 sí, pero con otra clasificación
  (ISACHC, no ACVIM): *«Class Ia = 0.15 to 0.25%»* = 375-625 mg y
  *«Class Ib, II and III = 0.08 to 0.15%»* = 200-375 mg. **No son intercambiables
  grado a grado**, y por eso no se sustituyeron.
- **Techo duro:** por abajo, mínimo FEDIAF **290 mg**. Por arriba, Reglamento
  2020/354 entrada 24, **738,6 mg**.
- **Margen del profesional:** **290 → 739**. Tres de nuestras cuatro cifras están
  fuera de ese margen por arriba.
- ⚠️ **Lo que la fuente primaria pide y no aplicamos**, todo verificado en
  ACVIM 2019: en estadio C, *«maintenance calorie intake… should be approximately
  60 kcal/kg BW»* — **una fórmula de DER propia de la insuficiencia cardíaca**,
  que el motor no usa; *«Ensure adequate protein intake and avoid low-protein
  diets designed to treat chronic kidney disease, unless severe concurrent renal
  failure is present»* — una instrucción explícita para **cardiopatía + renal**
  que el motor no conoce; y *«Consider supplementing with omega-3 fatty acids»*
  desde estadio C. Cavanaugh añade **proteína mínimo 5 g/100 kcal, objetivo 6-10**
  = suelo de **50** y objetivo **60-100 g/1000 kcal**.

### 2.7 · Miocardiopatía dilatada respondedora a taurina · `dcm_taurina_respondedora`

- **Aplica:** suelos de **taurina ≥250** y **L-carnitina ≥50** mg/1000 kcal.
- **Fuente:** SACN5 Tabla 36-4, verificada: *«Taurine — Dogs: ≥0.1%»* = 250 mg;
  *«L-Carnitine — Dogs: ≥0.02%»* = 50 mg. Ambas correctas.
- **Techo duro:** ninguno. Ni FEDIAF ni el Reglamento fijan taurina ni carnitina
  en el perro. Es de los pocos sitios donde **no hay techo de ningún tipo**.
- **Margen del profesional:** hacia arriba, libre. Hacia abajo, hasta 0 (no hay
  requisito de FEDIAF que proteger).
- **Cobertura del catálogo, medida:** taurina con dato en **62 de 163** fichas
  (71 declaradas a 0, 61 sin dato); L-carnitina en **35 de 163**. Los valores más
  altos: calamar/pulpo/sepia 356, atún 284, caballa 207, pato 178, lengua 175.
  El suelo es alcanzable, pero **descansa sobre un catálogo con el 37 % de
  cobertura**.

### 2.8 · Hiperlipidemia · `hiperlipidemia`

- **Aplica:** grasa ≤ **30** g, fibra ≥ **25** g/1000 kcal.
- **Fuente:** SACN5 Tabla 28-2, verificada literal: *«Restrict dietary fat (<12%
  dry matter [DM])»* = <30 g; *«Increase dietary fiber: Dogs: ≥10% DM»* = ≥25 g.
  Las dos exactas.
- **Techo duro:** grasa, mínimo FEDIAF **13,75**. Fibra: **FEDIAF no pone ni
  mínimo ni máximo**, así que el suelo de fibra no tiene techo de ningún tipo —
  es el valor más fácil de subir sin que salte nada.
- **Margen del profesional:** grasa **13,75 → 35,7** (el techo legal europeo de
  la entrada 22, base 3500 kcal); fibra **0 → sin techo**.
- **Honestidad de la fuente:** el propio capítulo dice *«no studies have been
  done in animals to evaluate the effects of dietary fiber type or amount on
  reducing serum triglyceride levels»*. El 10 % es práctica clínica, no
  dosis-respuesta.

### 2.9 · Obesidad / adelgazamiento · `obesidad`

- **Aplica:** grasa ≤ **30** g/1000 kcal.
- **Fuente:** SACN5 Tabla 27-4, verificada: *«Foods for weight loss should
  contain ≤9%»* = **22,5 g**. **El motor NO usa la cifra de la fuente**: usa 30,
  porque 22,5 —y hasta 27— no dan menú con el catálogo real. La propia tabla da
  *«Foods for prevention of weight regain should contain ≤14%»* = 35 g, así que
  los 30 caen en la franja de mantenimiento, no en la de adelgazamiento.
- **Techo duro:** mínimo FEDIAF **13,75**, inalcanzable en la práctica.
- **Margen del profesional:** **~28 → 35**. Por debajo de 28 el solver no
  resuelve: es una frontera **del catálogo**, no de la nutrición, y hay que
  decirlo como tal.
- ⚠️ **Lo que la fuente pide y NO aplicamos, y aquí duele:** *«Protein — Foods
  for weight loss should contain ≥25%»* = **≥62,5 g** (subir la proteína
  mientras se recortan kcal es lo que protege la masa magra, y el motor solo
  aplica el mínimo de FEDIAF, 52,1); *«Fiber — 12 to 25%»* = **30-62,5 g**;
  *«Lysine ≥1.7%»* = **≥42,5 g**; *«L-carnitine ≥300 ppm»* = **≥75 mg**;
  sodio 0,2-0,4 % = 500-1000 mg; fósforo 0,4-0,8 % = 1000-2000 mg.
  **Seis factores, y aplicamos uno.**

### 2.10 · Enteropatía pierde-proteínas / linfangiectasia · `ple_linfangiectasia`

- **Aplica:** grasa ≤ **37,5** g/1000 kcal.
- **Fuente:** SACN5 Tabla 58-1, verificada: *«Fat <15% for dogs and cats»* =
  37,5 g. Exacta. Motivo: la grasa de cadena larga sobrecarga los linfáticos.
- **Techo duro:** mínimo FEDIAF **13,75**.
- **Margen del profesional:** **13,75 → sin techo legal** (la entrada 20 del
  Reglamento no pone cifra de grasa).
- ⚠️ **Lo que falta, y es contradictorio con lo que hacemos:** la misma tabla
  pide **proteína ≥25 % MS = ≥62,5 g** — en una enfermedad que **pierde
  proteína**, y nosotros no ponemos suelo ninguno — y **fibra cruda ≤5 % =
  ≤12,5 g**. Además el Reglamento entrada 20 pide suelos de **sodio ≥511** y
  **potasio ≥1420 mg**.

### 2.11 · Insuficiencia pancreática exocrina · `insuficiencia_pancreatica_exocrina`

- **Aplica:** grasa ≤ **37,5** g/1000 kcal.
- **Fuente:** SACN5 Tabla 66-1, verificada: *«Fat 10 to 15% for dogs»* = 25-37,5.
  Usamos el extremo **alto** a propósito, y el texto lo respalda: *«feeding a
  highly digestible food in conjunction with pancreatic enzyme supplementation is
  more effective than simply decreasing the fat content»*. El tratamiento son las
  enzimas; la grasa es apoyo.
- **Techo duro:** mínimo FEDIAF 13,75. Sin techo legal (entrada 19 del
  Reglamento no pone cifra de nutriente, solo digestibilidad).
- **Margen del profesional:** **25 → 37,5** dentro de la fuente; por debajo de 25
  ya es más estricto que lo publicado.
- ⚠️ **Falta:** *«Fiber ≤5% DM, lower is better»* = **≤12,5 g**.

### 2.12 · Artrosis · `artrosis`

Ver §1.3. **Aplica** EPA+DHA ≥1,0 cuando la fuente pide **EPA** ≥1,0.
**Techo duro:** ninguno por arriba (FEDIAF no pone máximo de EPA+DHA en adulto);
por abajo, el mínimo general de EPA+DHA, **0,11 g**.
**Margen del profesional:** **0,11 → 2,75** (el extremo alto de la Tabla 34-2,
*«0.4 to 1.1%»*).

### 2.13 · Dermatosis zinc-sensible · `dermatosis_zinc`

- **Aplica:** zinc ≥ **25** mg/1000 kcal.
- **Fuente:** SACN5 Tabla 32-1, verificada: *«Zinc — Dogs: 100 to 200 mg/kg food
  DM»* = **25-50 mg**. Usamos el extremo bajo.
- **Techo duro:** **el máximo LEGAL de zinc de FEDIAF**. Este es el caso más
  claro de todos: el margen hacia arriba lo corta la ley, no el criterio.
- **Margen del profesional:** **25 → 50**, y ahí para de golpe.
- ⚠️ **Falta:** la misma tabla pide *«Linoleic acid >1.0% DM»* = **>2,5 g**,
  *«Phenylalanine + tyrosine >1.3% DM»* = **>32,5 g**, y *«Avoid excess copper
  (copper <200 mg/kg food DM)»*. También avisa de que *«Higher levels of zinc are
  required in foods with calcium >1.5% DM»* — o sea que en una ración BARF con
  mucho hueso, 25 mg puede no bastar. Eso no lo mira nadie.

### 2.14 · Diabetes mellitus · `diabetes`

- **Aplica:** excluye fruta, y grasa ≤30 % de las kcal **solo si además** hay
  pancreatitis o hipertrigliceridemia (fuente: Purina Institute — **no
  verificada** contra el documento original, ver §4).
- **Fuente principal, verificada:** SACN5 Tabla 29-3, perros:
  *«Fiber 7 to 18%»* = **17,5-45 g**; *«Fat <25%»* = **<62,5 g**;
  *«Protein 15 to 35%»* = 37,5-87,5 g; *«Provide foods with no more than 55%
  digestible carbohydrate»*; *«Avoid simple sugars»*.
- ⚠️ **El pilar del tratamiento es la fibra y no la aplicamos.** El suelo de
  17,5 g es implementable y hoy no existe. La exclusión de fruta cubre «avoid
  simple sugars» a medias. El Reglamento entrada 12 añade **azúcares totales
  ≤17,6 g**.

### 2.15 · Los cuatro urolitos · `estruvita`, `urato`, `cistina`, y el oxalato

Los cuatro están hoy en **no formulable**, con el motivo «depende del pH urinario
y de analíticas que la app no puede ver». Eso es cierto **y a la vez esconde que
las fuentes dan cifras formulables**:

| | Cita literal (SACN5) | Por 1000 kcal | ¿Bajo FEDIAF? |
|---|---|---|---|
| **Estruvita, prevención** | *«restrict dietary protein to <25% DM»* · *«phosphorus to <0.6% DM»* · *«magnesium to 0.04 to 0.1% DM»* (Tabla 43-3) | proteína <62,5 · fósforo <1500 · **magnesio 100-250** | **No** — los tres son formulables |
| **Estruvita, disolución** | *«protein to ≤8%»* · *«phosphorus ≤0.1%»* · *«magnesium <0.02%»* | 20 · 250 · <50 | Sí, muy por debajo |
| **Cistina** | *«Restrict high quality dietary protein to 10 to 18% DM»* · *«Restrict sodium to less than 0.3% DM»* (Tabla 42-1) | proteína 25-45 · **sodio <750** | La proteína sí; **el sodio no** |
| **Urato** | objetivo de purinas 90 mg/1000 kcal; medido en nuestro catálogo: **687-922** | — | Sí |

Dos cosas de aquí:

1. **La estruvita de prevención es formulable y está bloqueada.** Sus tres
   cifras están por encima del mínimo de FEDIAF. Y el Reglamento (entradas 17 y
   18) coincide: magnesio ≤511 mg.
2. **La cistina la atacamos por el nutriente equivocado.** Nuestro
   `nutriente_frontera` es `metionina_cistina`; la fuente restringe **proteína
   total y sodio**, y el Reglamento (entrada 14) también va por proteína. El
   sodio <750 es formulable hoy.

### 2.16 · Hipotiroidismo · `hipotiroidismo`

- **Aplica:** nada numérico. Restricción por alimento (grelo y nabo, *Brassica
  rapa*, ricos en progoitrina).
- **Nota del propio JSON, correcta:** *«No existe umbral canino publicado de
  crucíferas»*. Verificado: no hay tabla de factores clave para hipotiroidismo en
  SACN5.
- **Es la única patología del motor sin ningún límite numérico y con razón
  documentada.**

---

## 3 · Las 21 sin cifra: cuáles tienen fuente y cuáles no

De las 40 patologías, 21 no aplican ningún número. **No es lo mismo «la fuente no
da número» que «no hemos mirado».** Separado:

### 3.1 · Tienen tabla en SACN5 y NO la usamos

| Patología | Tabla | Lo que pide, verificado | Convertido |
|---|---|---|---|
| **`enteropatia_cronica`** | 57-1 (IBD) | *«Potassium 0.8 to 1.1%»* · *«Fat 12 to 15% for dogs»* (muy digestible) · *«Protein ≥25% for dogs»* · *«Crude fiber ≤5%»* o *«7 to 15%»* según enfoque | K **2000-2750 mg (con techo)** · grasa 30-37,5 · proteína ≥62,5 · fibra ≤12,5 o 17,5-37,5 |
| **`disfuncion_cognitiva`** | 35-3 | *«Vitamin E ≥750 mg/kg»* · *«Vitamin C ≥150 mg/kg»* · *«Selenium 0.5 to 1.3 mg/kg»* · *«L-carnitine ≥100 mg/kg»* · *«Total omegas-3 >1%»* · *«1% of each of five vegetable and fruit ingredients»* | vitE **≥187,5 mg** · vitC ≥37,5 · Se 0,125-0,325 · carnitina ≥25 · **ω-3 ≥2,5 g** |
| **`dermatitis_atopica`** | 32-1 | Las mismas de dermatosis: linoleico >1,0 % MS, fenilalanina+tirosina >1,3 % MS, digestibilidad MS >80 % | linoleico **>2,5 g** · Phe+Tyr **>32,5 g** |

**Los tres son implementables hoy** y ninguno baja del mínimo de FEDIAF. La
enteropatía crónica es la más llamativa: es una de las patologías más marcadas y
el motor no le ajusta nada.

### 3.2 · No tienen tabla de factores nutricionales clave en SACN5

Comprobado con un barrido de las 70 tablas «Key nutritional factors» de la obra
completa: **no existe** tabla para `epilepsia_idiopatica`, `cushing`, `addison`,
`mielopatia_degenerativa`, `riesgo_gdv`, `hipotiroidismo`,
`raza_predispuesta_cobre`, `dcm_asociada_a_dieta`, `renal_proteinuria`,
`fracaso_renal_agudo`, `cancer_soporte`, `inmunosupresion`, `cardiopatia_a`,
`cardiopatia_b1`, `otra`.

Que no haya tabla **no significa que no haya nada que decir** —varias tienen
texto clínico en sus capítulos— pero sí significa que no hay una cifra publicada
en el formato que usa el motor, y que ponerle una sería inventarla.

Tres de estas merecen mirada aparte y **quedan pendientes**:
`cancer_soporte`, `fracaso_renal_agudo` y `renal_proteinuria`.

---

## 4 · Fuentes que sostienen números vivos y NO están verificadas

Cuatro. Se dicen para que nadie las dé por buenas sin abrirlas:

| Número del motor | Fuente citada | Estado |
|---|---|---|
| grasa ≤20 en pancreatitis | Merck Veterinary Manual | ✅ **verificado literal** el 8-sep-2026 |
| sodio 900/900/790/480 | «ACVIM 2019 (Keene)» | ⚠️ **atribución incorrecta** — ACVIM no da cifras. La fuente real es Cavanaugh, Veterinary Practice News, 2020 (✅ verificada) |
| cobre ≤2,4 | Center SA et al., JAVMA 2026 | ⚠️ el artículo no se ha abierto, pero el número queda **triplemente acotado** por SACN5 (1,25) y el Reglamento UE (2,50) |
| grasa <30 % ME en diabetes | Purina Institute | ❌ **sin verificar** |
| no bajar el calcio en oxalato | Today's Veterinary Practice 2025, citando Carr 2020 | ❌ **sin verificar**, y **contradice a SACN5 Tabla 40-5**, que sí manda bajarlo |

La última es la más incómoda: hay un **conflicto de fuentes declarado** y
resuelto a favor de la más reciente, pero la más reciente no se ha leído.
Operativamente da igual hoy (el motor no toca el calcio, que es la posición
conservadora), pero la decisión está tomada sobre una fuente sin abrir.

---

## 5 · Resumen: qué hay que hacer

**Arreglar (son errores):** ✅ **los cuatro, hechos el 8 de septiembre.** Ver §0-bis.

1. ~~Atribución de fuente del sodio cardíaco~~ ✅
2. ~~Suelo de artrosis de `epa_dha` a `epa`~~ ✅
3. ~~La grasa en pancreatitis~~ ✅ → 37,5 (SACN5). Y resolvió renal+pancreatitis.
4. ~~El sodio cardíaco frente al techo legal europeo~~ ✅ → 739 / 739 / 625 / 480.

**Sigue roto y NO se ha tocado:** el **oxalato cálcico** (§1.2). Es el único de
los cinco que queda, y es el más laborioso: son cinco factores más dos exclusiones
de alimento (ácido oxálico y vitamina C), y una de las dos necesita una lista de
alimentos ricos en oxalato que hoy no existe en el catálogo.

**Implementar (no bajan de FEDIAF, no necesitan firma):**

| Patología | Qué añadir |
|---|---|
| ~~renal~~ | ~~sodio ≤750~~ ✅ · potasio 1000-2000 · **proteína ≤62,5** |
| oxalato | fósforo 750-1500 · Ca:P 1,1-2:1 · sodio <750 · magnesio 100-375 · excluir oxálico y vitamina C |
| obesidad | ~~**proteína ≥62,5**~~ ✅ · fibra 30-62,5 · lisina ≥42,5 · L-carnitina ≥75 |
| artrosis | omega-3 totales ≥8,75 · L-carnitina ≥75 |
| ~~PLE~~ | ~~**proteína ≥62,5** · fibra ≤12,5~~ ✅ |
| ~~EPI~~ | ~~fibra ≤12,5~~ ✅ |
| ~~diabetes~~ | ~~**fibra ≥17,5**~~ ✅ |
| enteropatía crónica | ~~grasa ≤37,5 · proteína ≥62,5~~ ✅ · potasio 2000-2750 · fibra |
| disfunción cognitiva | vitamina E ≥187,5 · omega-3 ≥2,5 |
| dermatosis y atopia | ~~linoleico >2,5~~ (descartado: más laxo que FEDIAF) · fenilalanina+tirosina >32,5 |
| estruvita (prevención) | magnesio 100-250 · fósforo <1500 · proteína <62,5, **y pasarla a formulable** |
| cistina | sodio <750 |
| hepatopatía | zinc >50 · hierro 20-35 · sodio 200-625 · taurina ≥250 |
| cardiopatía C | proteína ≥50 |

Eran **catorce patologías**. Tras la tanda del 8 de septiembre quedan **ocho** con
al menos un factor de su propia fuente sin aplicar. Ninguno requiere prescripción.

Los que quedan y por qué no se hicieron ya: los tres de artrosis y obesidad
(omega-3 totales, lisina, L-carnitina) **necesitan claves nuevas en el `MAPA`**
como la que se añadió para el EPA; los de oxalato y estruvita necesitan además
decidir si esas patologías pasan a formulables; y el de cardiopatía C (proteína
≥50) es más laxo que el mínimo de FEDIAF (52,1), así que no cambiaría nada — mismo
caso que el linoleico.

**Verificar (fuentes sin abrir):** Purina Institute (diabetes), Today's
Veterinary Practice 2025 / Carr 2020 (calcio en oxalato), Center 2026 (cobre).
