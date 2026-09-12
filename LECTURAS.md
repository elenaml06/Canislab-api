# Lo que hemos leído, y qué decidimos con cada cosa

⚠️ **Escrito el 11 de septiembre de 2026 de noche, sustituyendo a toda la
maquinaria de contadores de lectura.** Elena, y tenía razón:

> «no sé por qué tienes que leer con un script. lee, y según vayas leyendo vas
> anotando, y luego de lo que hayas anotado dices: ¿esto hay que aplicarlo?
> [...] quiero que leas todo bien, frase a frase, letra a letra, y que anotes
> todo lo interesante y que luego decidamos si se aplica o no se aplica»

**Y es la ley para todos los documentos, no solo para los que faltan.**

## Por qué se fueron los contadores

Había cuatro scripts que partían cada libro en frases, filtraban las que
«parecían nutricionales» y exigían un veredicto por frase. Sonaba a rigor y era
lo contrario, por tres razones medidas:

1. **No encontraban nada.** Los tres hallazgos de verdad de esa noche —la
   tercera cifra de la frase del EPA+DHA, el calcio de Köber diez veces por
   debajo, y la rama estricta del «Or» del Reglamento— **no los encontró ningún
   script**. Los encontré leyendo el texto. Los scripts solo decían dónde no
   había leído.
2. **Cortar en frases pierde la estructura.** Una entrada del Reglamento con dos
   ramas unidas por «Or» no es una frase: es una unidad. Partirla es exactamente
   cómo se perdió la mitad que contestaba la pregunta.
3. **«Cerrado» acabó significando «tiene una nota».** Y eso permitió decir tres
   veces que algo estaba cerrado y que luego saliera algo esperando.

**Lo que NO se fue**, porque sí caza errores: los auditores que **rehacen un
número** contra la fuente. `auditar_citas.py` cazó una cita que el libro no
decía; `auditar_conversiones.py` cazó un ×25; `auditar_kober.py` cazó el ×10 de
las fichas de hueso; `auditar_transcripcion_fediaf.py` rehace las 164 celdas de
la tabla. Esos se quedan y se quedan todos.

## Cómo se lee, a partir de ahora

1. Se lee el documento **entero**, seguido, sin filtro.
2. Se va **anotando aquí** todo lo interesante, con su cita literal.
3. Al terminar, se repasa la lista punto por punto y se decide **una de tres**:
   **aplicado**, **no se aplica porque…**, o **pendiente de decidir**.
4. Lo que quede pendiente de decidir va también a `PREGUNTAS_ABIERTAS.md` con
   dueño.

---

## Estado de las fuentes

| Fuente | Leída | Notas |
|---|---|---|
| FEDIAF | **releída entera con el método nuevo (11-sep)** | Abajo, punto por punto. Salieron 7 cosas que decidir, 2 frases falsas en la documentación y 186 celdas cruzadas por primera vez |
| SACN5 | leída, pero **NO con este método** | 124.310 líneas. Su lectura vieja dejó 22 tablas con hallazgo sin aplicar (abajo) y ese registro se conserva, pero no ha pasado por el repaso punto por punto. Mientras no pase, «leída» aquí significa menos que en la fila de FEDIAF |
| NRC 2006 | leída, pero **NO con este método** | 43.556 líneas. Igual que SACN5: tiene lectura previa y no tiene repaso punto por punto |
| Fascetti & Delaney | sí, los 21 capítulos (11-sep) | 42 notas, abajo |
| Reglamento (UE) 2020/354 | sí | Volcado entero en `limites_legales_ue_2020_354.json` |
| Köber 2017 | sí (11-sep) | Cazó tres fichas con el calcio ×10 bajo |
| WSAVA — dietas crudas y premios | sí (11-sep) | Abajo |
| **Spitze 2003** | **no está en el repo** | Decide la taurina de 89 fichas |
| Ettinger & Feldman | no | Dos tomos |
| Dobenecker / Hofmann | **los dos leídos enteros (12-sep)** | El de 2021 (PLOS ONE, 8 beagles) y el de 2025 (JAPAN, 8 foxhound). Abajo. Sale una cosa que el motor no puede ver y que vale hasta el **39,6 %** del fósforo de un menú: **en qué forma química viene el fósforo de los multivitamínicos**. Y una advertencia sobre nuestra propia protección: subir el ratio Ca:P NO protege de un fosfato soluble |
| TVT Merkblatt 181 | **las DOS ediciones leídas enteras (12-sep)**, la de julio de 2017 y la de mayo de 2025 | Es la hoja de la asociación veterinaria alemana de protección animal **sobre el BARF**, o sea sobre esto. Está en alemán. Abajo. Lo suyo más duro ya estaba aplicado desde el 6 de septiembre (el bloqueo de los cortes con tiroides sale de aquí), y salen dos cifras que el motor no usa: el ratio Ca:P «óptimo» **1,3-1,5** y unas proporciones BARF clásicas distintas de las nuestras |
| Ishii 2025 — purinas | **leído entero (12-sep)** | El único estudio que mide las purinas de la comida de perro por espectrometría de masas, y trae **la regla para convertir sus µmol/Mcal a nuestros mg/1000 kcal**. Confirma el objetivo de urato del motor (sus <630 µmol/Mcal son 82,5-95,8 mg/1000 kcal y tenemos escrito 90) y mide lo lejos que está una ración cruda: **1,5-1,8 veces el pienso más cargado que analizaron** |
| ACVIM (Keene 2019) | **leído entero (12-sep)** | Igual: primero se buscó y luego se leyó. Lo que solo aparece leyendo va marcado abajo | Abajo. Cierra P-10 —el límite del sodio existe y es clínico, no una cifra— y saca un hallazgo nuevo: el motor aplica al cardíaco con renal justo la dieta baja en proteína que el consenso dice que hay que evitar |
| IRIS 2026 | **leída entera (12-sep), los cuatro documentos** | ⚠️ Y en dos vueltas: la primera fue media lectura y medio `grep`, y Elena lo cazó. Lo que salió al leerla de verdad está abajo, marcado | Abajo. Contesta lo del IRIS 4, y la respuesta es que **IRIS no da ni una cifra dietética**: la restricción de proteína del estadio 4 no es suya, y lo único que dice de la proteína ahí es que hay que evitar que falte |
| AAHA 2021 | **leída entera (12-sep)**: texto corrido, las cinco tablas y el cuadro de energía | ⚠️ Sus tablas **no se pueden extraer del PDF** —están dibujadas como trazos vectoriales y la página de la Tabla 8 entera devuelve 194 caracteres—, así que se leyeron renderizando las páginas y están transcritas en `aaha_2021_tablas_transcritas.txt`, con el método escrito en su cabecera. Abajo, punto por punto. Confirma dos cosas que ya aplicamos (la banda de BCS 4-5 y el 10 % de los premios), da la segunda fuente independiente del conflicto cardíaco+renal, y trae tres cosas que el motor no decía |
| Today's Veterinary Practice | **leída entera (12-sep)** | Igual. Y al leerla salió lo de las purinas, que ningún `grep` mío habría buscado | El artículo del oxalato, abajo: aguanta entera, todo lo suyo ya estaba aplicado. ⚠️ El que da el sodio cardíaco por estadio ACVIM sigue **sin estar** en el repo |

---

## ACVIM — Keene et al. 2019, consenso sobre la enfermedad mitral degenerativa · leído entero el 12-sep-2026

440 líneas. Es la fuente que el repo cita para el sodio del cardiópata por
estadio, y se lee entera para cerrar **P-10**: si hay un punto en el que bajar
el sodio de un cardiópata sea malo.

### P-10 queda contestada, y la respuesta no es un número

Estadio D, literal:

> *«In patients with refractory fluid accumulations, attempts should be made to
> further decrease dietary sodium intake **if it can be done without
> compromising appetite or renal function**.»* (Class IIa, LOE: expert opinion)

O sea: **sí hay un límite, y es clínico, no una cifra.** Se baja más mientras no
se estropee el apetito ni la función renal. Eso explica por qué ninguna fuente
da un suelo de sodio: el suelo lo pone el perro, no la tabla.

Y el mínimo de FEDIAF sigue estando debajo de todo (290 mg/1000 kcal a DER 95),
que es lo que el motor ya respeta. Así que **no hay nada que cambiar**: la
pregunta se cierra con «el límite existe y es clínico», y el motor no puede
medir apetito ni creatinina.

### El hallazgo de verdad: una interacción que el motor aplica al revés

Estadio C, entre las recomendaciones dietéticas, con la fuerza más alta del
documento (Class I, LOE: moderate):

> *«Ensure adequate protein intake and **avoid low-protein diets designed to
> treat chronic kidney disease, unless severe concurrent renal failure is
> present**.»*

**MEDIDO HOY**, combinando patologías en el motor:

| Marcado | Techo de proteína | Techo de sodio |
|---|---|---|
| `cardiopatia` sola | ninguno | 738,6 |
| `renal` sola | **62,5** | 750,0 |
| `cardiopatia` + `renal` | **62,5** | 738,6 |
| `cardiopatia_c` + `renal` | **62,5** | 625,0 |
| `cardiopatia_d` + `renal` | **62,5** | 480,0 |

O sea que un perro cardíaco al que además se le marca la renal recibe
exactamente la dieta baja en proteína que el consenso dice que hay que evitar
—y en el caso que nombra, porque nuestra clave `renal` **es** la leve-moderada;
la grave es `renal_avanzada`, que no es formulable.

No es un fallo del mecanismo: los topes se combinan con `min()` y eso es
correcto. Es que **aquí las dos fuentes piden cosas opuestas**, y elegir cuál
cede es criterio clínico. Va a `PREGUNTAS_ABIERTAS.md` como **P-19**, no se
cambia sola.

### Lo que SOLO apareció al leerlo entero

| Lo que dice | Decisión |
|---|---|
| Estadio A: *«**No dietary treatment recommended for any patient**»* (Class I) | **CONFIRMA EL MOTOR con cita**: `cardiopatia_a` no lleva ningún límite, y hasta hoy eso era una decisión sin frase detrás |
| Estadio B1: *«**No drug or dietary treatment is recommended**»* (Class I) | Igual: `cardiopatia_b1` está vacía y ahora se sabe por qué |
| Los cuatro criterios que definen el **B2**: soplo ≥3/6, cociente AI:Ao ≥1,6, diámetro ventricular normalizado (LVIDDN) ≥1,7 y VHS radiográfico >10,5 — y sin ecografía, VLAS ≥3 | **Anotados**, igual que los umbrales de IRIS: son los números con los que un veterinario elige el estadio, y la app pregunta el estadio ACVIM desde agosto sin tenerlos escritos en ninguna parte |
| Los **diez** panelistas declaran haber asesorado a Boehringer Ingelheim (que fabrica el pimobendán) y/o a CEVA e IDEXX | **No cambia nada**, y se anota porque es un documento que recomienda el pimobendán como Class I / evidencia fuerte. Quien lo lea tiene derecho a saberlo |

### Lo demás, punto por punto

| Lo que dice | Decisión |
|---|---|
| El consenso **no da ni una cifra de sodio**: «mild» en B2, «modestly restrict» en C, «further decrease» en D. Comprobado: cero apariciones de «mg/100 kcal» en las 440 líneas | **Confirma que el repo ya lo dice bien.** `patologias.json` escribe que «las CIFRAS por estadio salen de» Cavanaugh (Veterinary Practice News 2020) y que el consenso es el marco. La atribución era correcta |
| *«Modestly restrict sodium intake, taking into consideration sodium from all dietary sources (including dog food, **treats, table food, and foods used to administer medications**)»* | **Ya aplicado**: es la fuente primaria detrás del 57 % de Fascetti cap.18, y por eso la pregunta de los premios incluye la comida con la que se esconde la pastilla |
| Caquexia cardíaca: *«maintenance calorie intake in Stage C should be approximately **60 kcal/kg BW**»* | **PENDIENTE DE DECIDIR.** Es una cifra de energía por kg de peso VIVO, no por peso metabólico, y el motor calcula por kg^0,75. Para un perro de 20 kg son 1200 kcal contra las ~1030 que da la tabla de actividad: la fuente pide **más**, no menos, para que no pierda masa. No se aplica sin decidirlo |
| *«Consider supplementing with omega-3 fatty acids, especially in dogs with decreased appetite, muscle loss, or arrhythmia»* (Class IIa) | **No se aplica**: sin cifra |
| Potasio: suplementar **solo** si hay hipopotasemia; evitar dietas altas si hay hiperpotasemia | **No se aplica**: las dos ramas dependen de una analítica, y el motor no la tiene. Refuerza que la cardiopatía sea `dueno_con_diagnostico` |
| Magnesio: igual, solo si hay hipomagnesemia | Igual |
| Todo lo demás —pimobendán, furosemida, espironolactona, IECA, oxígeno, toracocentesis, nitroprusiato— | **No se aplica**: son fármacos y manejo hospitalario |


---

## Today's Veterinary Practice — Cook & Atiee, oxalato cálcico canino · releída entera el 12-sep-2026

Se lee entera porque es la que podía cerrar **P-11** (si el oxalato necesita un
suelo de fósforo). **No lo cierra: no da ninguna cifra de fósforo.** La única
vez que nombra el fosfato es como inhibidor endógeno —*«This is an inorganic
phosphate found in blood and urine that reduces the crystallization of calcium
salts»*—, que es fisiología, no una recomendación dietética. Así que P-11 sigue
abierta y ahora se sabe que es una tercera fuente que no la contesta.

**Y lo demás ya estaba aplicado, entero y bien.** Es la primera fuente que se
relee con este método y aguanta sin sacar nada:

| Lo que dice | Estado |
|---|---|
| *«Dietary calcium restriction does not appear to mitigate CaOx urolithiasis and is not recommended»* | **Ya aplicado** el 8-sep, y con el conflicto contra SACN5 (que pide restringirlo a 0,4-0,7 % MS) resuelto y escrito en `calcio_no_se_restringe` |
| *«do not recommend feeding a diet with a sodium content >120 mg/100 kcal»* (= 1200 mg/1000 kcal) | **Ya anotado**, y se aplica la más estricta: los 750 de la Tabla 40-5 de SACN5. El margen del profesional (290 a 1200) ya lo tenía escrito |
| Los cuatro altos en oxalato que nombra —cacahuete, tofu, espinaca, boniato— | **Los cuatro están** en `OXALATO_ALTO` de `seguridad.py`, que tiene 20 desde el 8-sep |
| *«High-protein foods should be avoided»* | **No se aplica**: sin cifra. `urolitos_fosfato_calcico` sí tiene techo de proteína, y es del Reglamento |
| El magnesio *«forms soluble complexes with oxalate … decreases the uptake of dietary oxalate»*, o sea protector | ⚠️ **Y el motor le pone un TECHO de 375 mg/1000 kcal**, que viene de la Tabla 40-5 de SACN5. Las dos fuentes no se contradicen del todo —una habla del magnesio urinario y la otra del aporte— pero conviene tenerlo delante: la más reciente dice que el magnesio ayuda |
| Citrato potásico (75 mg/kg cada 12 h), hidroclorotiazida (2 mg/kg cada 12 h) | **No se aplica**: son fármacos |
| *«a canned diet is always preferable to dry food»*, y trucos para que beba más | **No se aplica** como cifra, y la ración de este motor es húmeda por construcción |
| La piridoxina no tiene respaldo en el perro con dieta equilibrada | **Confirma no hacer nada**, que es lo que se hace |

### Lo que SOLO apareció al leerlo entero, y esto sí cambia el motor

| Lo que dice | Decisión |
|---|---|
| *«High urine uric acid levels interfere with endogenous stone inhibitors and appear to promote CaOx urolithiasis»* y *«**Robust purine intake** leads to uric acid generation and supports an acidic urine pH»* | ⚠️ **LAS PURINAS IMPORTAN EN EL OXALATO, y el motor no lo sabía.** Los topes de `oxalato` son vitamina D, sodio, fósforo y magnesio: ninguno toca las purinas, y el catálogo SÍ tiene el dato (`purinas` y `purinas_fuente` en cada ficha). La fuente **no da cifra**, así que no se inventa una: **se aplica como aviso**, que es lo que la fuente respalda. Y no vale reusar el umbral del urato: `urato` no es formulable y no tiene ninguno |
| *«cranberry extract has been shown to increase urinary oxalate … and should not be administered to CaOx stone–forming dogs»* | **Ya cubierto**: el arándano está en `OXALATO_ALTO` desde el 8-sep |
| *«The following guidelines … are likely **not appropriate** for rare patients with hereditary CaOx urolithiasis type 2 (usually bulldogs, mastiffs, bassets, or beagles younger than 3 years)»* | ⚠️ **APLICADO como aviso**: hay un subgrupo, definido por raza y edad, al que TODO el consejo dietético de esta patología no le sirve. El motor no puede saberlo —hace falta el genotipo— pero quien firma sí |
| Razas sobrerrepresentadas: schnauzer miniatura, bichón frisé, yorkshire; y en bóxer y bulldog inglés **más del 90 % de los afectados son machos** | **No se aplica**: es epidemiología, no una cifra de la ración. Las cuatro razas están en `razas.json` |
| pH de orina objetivo **6,5 a 7,5** y densidad <1,020 | **No se aplica**: el motor no mide la orina |
| El **calabacín** bajó la sobresaturación urinaria y subió el pH en un estudio en gatos, *«appears to be harmless»* | ⚠️ **Y el calabacín está en `OXALATO_ALTO`**, o sea excluido, porque la Tabla 40-3 de SACN5 lo marca alto en oxalato. **No se toca** —el estudio es en gatos y SACN5 es la fuente del filtro— pero queda escrito que las dos fuentes no dicen lo mismo de ese alimento |
| Citrato potásico (75 mg/kg/12 h), hidroclorotiazida (2 mg/kg/12 h), vinagre de manzana, piridoxina | **No se aplican**: fármacos y suplementos con evidencia equívoca. La piridoxina la desaconseja la propia fuente en un perro con dieta equilibrada |

**Decisión: se aplican DOS avisos** (las purinas y el subgrupo hereditario tipo 2)
y queda una cosa para mirar con la nutricionista, que es el techo de magnesio: lo pide SACN5 y la fuente de 2025 describe el
magnesio como inhibidor. No es contradicción demostrada y por eso no se toca.


---

## IRIS 2026 — «Guidelines» de la International Renal Interest Society · leída entera el 12-sep-2026

Cuatro documentos, 2.262 líneas en total: estadificación, recomendaciones de
tratamiento para perro, graduación del fracaso renal agudo y la guía de bolsillo.
Leídos los cuatro, seguidos.

**Se lee esta antes que ninguna otra de las que faltaban** porque es la que
contesta lo que preguntó Cris Carles: si en un IRIS 4 hay que bajar la proteína
hasta el 15 %.

### El hallazgo que decide, y es lo que la fuente NO dice

**IRIS 2026 no da ni una sola cifra dietética.** Ni de proteína, ni de fósforo,
ni de sodio, ni de nada. Comprobado buscando en los cuatro documentos: cero
apariciones de «g/1000 kcal», «% DM», «dry matter», «g/Mcal», «mg/kg diet» o
«% of calories». Lo que dice de la dieta, las 33 veces que la nombra, es
siempre la misma frase: *«feed a clinical kidney diet»* o *«dietary phosphate
restriction (i.e., clinical kidney diet therapy)»*.

Lo que sí da son **objetivos en SANGRE**, que es otra cosa:

| Estadio | Fosfato en plasma |
|---|---|
| 1 y 2 | < 1,5 mmol/l (4,6 mg/dl) |
| 3 | < 1,6 mmol/l (5,0 mg/dl) |
| 4 | < 1,9 mmol/l (6,0 mg/dl) |

Y con **suelo**: *«but not less than 0.9 mmol/l; <4.6 mg/dl but >2.7 mg/dl»*. O sea que la
propia IRIS dice que bajar el fosfato **de más** también es malo — en sangre,
no en el plato, pero es la misma forma que la pregunta P-11 sobre el suelo de
fósforo del oxalato.

### Y lo que dice del estadio 4 va en la dirección CONTRARIA

Las «Further recommendations for Stage 4 patients» empiezan así, literal:

> *«1. Intensify efforts to prevent protein / calorie malnutrition. Consider
> feeding tube intervention (such as percutaneous esophagostomy or gastrostomy
> tube).»*

Es la **única** vez que la palabra «protein» aparece en todo el documento fuera
de «urine protein to creatinine ratio». Y no pide restringir: pide **evitar la
desnutrición proteico-calórica**, hasta el punto de poner una sonda.

| | |
|---|---|
| Lo que se preguntó | ¿Hay que bajar la proteína al 15 % en un IRIS 4? |
| Lo que dice IRIS | Nada de restringir. Lo único que dice de la proteína en estadio 4 es que hay que **evitar que le falte** |
| Quién sí da la cifra | No IRIS. El techo de proteína que aplica el motor (62,5 g/1000 kcal) es del **Reglamento (UE) 2020/354**, entrada 10, que es ley |

**Decisión: no se cambia nada del motor, y se corrige una cita.** El techo de
proteína se queda donde está y con la fuente que de verdad lo dice. Lo que hay
que arreglar es que `patologias.json` citaba «IRIS» como una de las fuentes del
techo de FÓSFORO de 1200 mg/1000 kcal, y IRIS no da esa cifra ni ninguna otra
dietética. La cifra no cambia —viene de Freeman 2009, WSAVA y la Tabla 37-9 de
SACN5— pero IRIS deja de figurar como si la respaldara.

⚠️ Es la misma familia de error que las dos columnas del PDF, con otra cara:
`auditar_citas.py` comprueba lo que va **entrecomillado**, y esto era una
atribución de fuente sin comillas. Ahí no llega ningún auditor.

### El sodio: IRIS dice tres veces que no hay evidencia

En los estadios 1, 2 y 3, con la misma frase cada vez:

> *«Dietary sodium (Na) reduction – there is no evidence that lowering dietary
> Na will reduce blood pressure. If dietary Na reduction is attempted, it
> should be accomplished gradually and in combination with pharmacological
> therapy.»*

El motor aprieta el sodio del renal a **750 mg/1000 kcal**, y esa cifra es de la
Tabla 37-9 de SACN5, no de IRIS. **No se toca** —SACN5 manda donde FEDIAF no
llega y es un techo, o sea que solo aprieta— pero queda escrito que la sociedad
que define la enfermedad dice que no hay evidencia de que eso baje la tensión,
y que si se hace, que sea **gradual**. Lo segundo sí es accionable: el motor ya
tiene plan de transición.

### Lo que sí hay que llevarse: las cifras que deciden el estadio

Esto es lo que le faltaba a `preguntas_por_patologia.json` para que la pregunta
del estadio renal tenga umbrales con fuente. Perro:

| | Estadio 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| Creatinina (mg/dl) | < 1,4 | 1,4 - 2,8 | 2,9 - 5,0 | > 5,0 |
| SDMA (µg/dl) | < 18 | 18 - 35 | 36 - 54 | > 54 |

Y los dos subestadios, que son **dos preguntas más**:

| UP/C (perro) | Subestadio |
|---|---|
| < 0,2 | No proteinúrico |
| 0,2 - 0,5 | Proteinuria límite |
| > 0,5 | Proteinúrico |

| Presión sistólica (mmHg) | Subestadio |
|---|---|
| < 140 | Normotenso |
| 140 - 159 | Prehipertenso |
| 160 - 179 | Hipertenso |
| ≥ 180 | Gravemente hipertenso |

**Nuestra pregunta de UP/C ya usa el 0,5**, que coincide. Lo que no teníamos con
fuente son los umbrales de creatinina y SDMA, y son los que deciden si un perro
es `renal` o `renal_avanzada`.

### Lo demás, punto por punto

| Lo que dice | Decisión |
|---|---|
| *«an increased blood creatinine or symmetric dimethylarginine (SDMA) concentration alone is not diagnostic of CKD»* | **Refuerza `quien_formula_cada_patologia.json`**: la renal es `solo_veterinario`, y esto dice por qué — ni siquiera una analítica alta basta para diagnosticarla |
| El galgo (*greyhound*) tiene la creatinina y la SDMA **más altas** siendo sano, y los *sight hounds* la tensión más alta | **PENDIENTE DE DECIDIR, y es medible**: `razas.json` tiene los galgos. Si la app va a preguntar el estadio IRIS, un galgo sano puede salir estadio 2 por su raza |
| Los ligantes de fosfato (30-60 mg/kg/día, hidróxido de aluminio, carbonato cálcico…) | **No se aplica**: es un fármaco, no un alimento. Y el motor no formula fármacos |
| Toda la parte de hipertensión, anemia, acidosis, diálisis y sonda de alimentación | **No se aplica**: es tratamiento clínico |
| El fracaso renal AGUDO tiene su propia graduación (documento aparte) y **no menciona la dieta ni una vez** | **Confirma lo que hace el motor**: `fracaso_renal_agudo` no lleva ningún tope propio |
| *«Response to any treatment … should be monitored at intervals using UP/C»* | **No se aplica**: es seguimiento clínico |

### Lo que SOLO apareció al leerla entera

⚠️ La primera pasada fue media lectura y medio `grep`, y eso no es leer: buscar
encuentra lo que ya sospechas. Estas seis no las habría encontrado ninguna
búsqueda mía, porque no sabía que existían.

| Lo que dice | Decisión |
|---|---|
| Estadio 2: *«If muscle loss is marked, consider staging based on serum SDMA concentration rather than creatinine»* | **Anotado, y es la SEGUNDA fuente que dice lo mismo**: la creatinina depende de la masa muscular, igual que FEDIAF dice que el BCS bajo se confunde con la atrofia (P-17). Dos fuentes independientes avisando de que la pérdida de músculo estropea una medida que usamos |
| La guía de bolsillo: diagnosticar CKD en estadio 1 o 2 temprano pide **dos** hallazgos — SDMA persistente **>14 µg/dL** más uno de {imagen anormal, proteinuria renal, densidad urinaria <1,030 en perro} | ⚠️ **Y el 14 NO es el 18.** El >14 es para DIAGNOSTICAR y el >18 para ESTADIFICAR. Dos números parecidos para dos cosas distintas en el mismo documento: si algún día la app pregunta la SDMA, tiene que decir para qué |
| *«If values are persistently discordant, consider assigning the patient to the higher stage»* | **Anotado**: la regla de desempate entre creatinina y SDMA es ir al estadio MÁS ALTO, que es el lado prudente |
| La graduación del fracaso AGUDO usa creatinina con **umbrales distintos** de la estadificación crónica: I <1,6 · II 1,7-2,5 · III 2,6-5,0 · IV 5,1-10,0 · V >10,0, contra 1,4 / 2,8 / 5,0 de la CKD | ⚠️ **Dos escalas confundibles** con la misma unidad y el mismo analito. Si la ficha pregunta creatinina alguna vez, hay que decir cuál de las dos |
| El documento del fracaso agudo **no menciona la dieta ni una vez** en sus 493 líneas | **Confirma** que `fracaso_renal_agudo` no lleve ningún tope. Ahora está comprobado leyéndolo, no suponiéndolo |
| Estadio 3: si hay acidosis metabólica (bicarbonato <18 mmol/l), suplementar con **bicarbonato SÓDICO** oral hasta 18-24 | **No se aplica** (es un fármaco), pero se anota la tensión: la misma guía que sugiere bajar el sodio manda dar sodio por otra puerta en el estadio 3 |

### Lo que sale de esta lectura

1. **Corregir la fuente del fósforo renal** en `patologias.json`: IRIS no da esa
   cifra. (Se hace ahora.)
2. **Contestar a Cris**: IRIS no pide restringir proteína en el estadio 4; pide
   lo contrario. Quien pone el suelo es el Reglamento europeo.
3. **Los umbrales de estadificación** (creatinina, SDMA, UP/C) ya tienen fuente
   y están escritos en `preguntas_por_patologia.json`, en un bloque
   `umbrales_de_la_fuente` que **no cambia ninguna cifra del motor**: son los
   números con los que un veterinario decide el estadio, y hasta hoy la propia
   nota de esa pregunta decía que no estaban en ninguna parte del repo. (Hecho.)
4. **Pendiente**: el galgo sano puede parecer un renal estadio 2.

---

## FEDIAF 2025 — «Nutritional Guidelines» · releída entera el 11-sep-2026 con el método nuevo

98 páginas, 10.682 líneas. Ya estaba marcada «leída» desde agosto, y por eso se
relee: lo que había era un inventario de tablas y un contador de frases, no una
lectura. Esto es la lectura, seguida, de la primera línea a la última, con la
decisión al lado de cada cosa.

**Lo que ha salido**: 5 cosas nuevas que aplicar o decidir, 1 frase de
`CLAUDE.md` que hay que corregir porque es falsa, y 186 celdas de la tabla de
requisitos cruzadas por primera vez contra la SEGUNDA copia que la propia
FEDIAF publica de ella.

### §1 Glosario

| Lo que dice | Decisión |
|---|---|
| *«Minimum recommended level … it is recommended that the nutrient levels are at or above the levels listed in the tables and do not exceed the nutritional or legal maximum»* | **Ya aplicado**: es el semáforo, las dos direcciones |
| *«Nutritional maximum limit … Levels exceeding the nutritional maximum may still be safe, however, no scientific data are currently known to FEDIAF»* | **No cambia ninguna cifra**, pero cambia cómo se lee un techo. Un máximo (N) no es un daño demostrado: es el final de lo que hay medido. Un máximo (L) es ley. Eso ya lo separa `maximo_origen`, y esta frase es la que lo justifica |
| *«Daily ration. The average total quantity of feeding stuffs, calculated on a moisture content of 12%»* | **Ya aplicado**: es de donde sale el divisor 3,52 con el que se convierten las cifras del Reglamento (UE) 2020/354 |

### §2.2 Alcance — aquí están tres de los hallazgos

| Lo que dice | Decisión |
|---|---|
| *«These guidelines relate to dog and cat foods manufactured from ingredients with normal digestibility (i.e. ≥ 70% DM digestibility; ≥ 80% protein digestibility) and average bioavailability»* | **PENDIENTE DE DECIDIR.** Es la condición de validez de toda la tabla y nunca la hemos mirado: el catálogo **no tiene campo de digestibilidad**. La carne cruda va sobrada; el hueso molido, el cartílago y la laringe de vacuno no está claro que lleguen. Si un menú se apoya mucho en ellos, los mínimos de FEDIAF se están aplicando fuera de su rango de validez |
| *«Pet foods can be adequate and safe when nutrient levels are outside the recommendations in this guide, based on the manufacturer's substantiation of nutritional adequacy and safety»* | **Anotado, no aplicado.** Es la **tercera** frase del repo que dice que se puede salir de FEDIAF con prueba (las otras dos: §3.1.b aquí mismo, y el Reglamento (UE) 2020/354). No cambia la regla de Elena —«los requisitos se respetan SIEMPRE»— pero sí cambia lo que se puede afirmar en el documento que lee el nutricionista |
| *«**Excluded from the FEDIAF's Nutritional Guidelines are pet foods for particular nutritional purposes** and some other specialised foods such as for sporting dogs etc. Therefore specific products may have nutrient levels that are different from those stated in these guidelines»* | **HALLAZGO. FEDIAF se excluye a sí misma de las dietas clínicas.** Una dieta para una patología es exactamente uno de esos alimentos —el Reglamento (UE) 2020/354, que es quien las regula, los define como alimentos *«intended for particular nutritional purposes»*— y FEDIAF dice que sus tablas no los cubren. O sea: «gana FEDIAF» es verdad para el perro SANO, y para el perro enfermo quien pone el suelo es la ley, no FEDIAF. Contesta la pregunta de Cris sobre el IRIS 4 y la que hizo Elena sobre si un veterinario puede bajar de los mínimos. **No cambia el motor** (Elena decidió que los requisitos se respetan siempre) pero **sí hay que escribirlo** en `FEDIAF_CONTRA_OTRAS_FUENTES.md` y en `PARA_EL_NUTRICIONISTA.md`, porque hoy los dos afirman algo más fuerte de lo que la fuente dice |

### §3.1 Guía general

| Lo que dice | Decisión |
|---|---|
| Un alimento completo sin etapa declarada *«should be formulated according to the levels recommended for early growth and reproduction»* | **No se aplica**: el motor siempre sabe la etapa. Se anota porque es la regla del caso peor, y es la que usaríamos si algún día hubiera un menú sin etapa |
| §3.1.b *«If certain nutrient levels are outside the values stated in this guide, manufacturers should be able to prove that the product provides adequate and safe intakes»* | Misma familia que la anterior |
| §3.1.3 *«A legal maximum only applies when the particular trace element or vitamin is **added** to the recipe as an additive … If the nutrient comes exclusively from feed materials, the legal maximum does not apply»* | **Ya anotado el 10-sep y sigue PENDIENTE.** El motor aplica **siempre** el techo legal, que es el lado estricto; en la vitamina D eso son 14,19 µg/1000 kcal cuando el nutricional es 20,0. La razón por la que no se ha cambiado está medida y escrita en el propio JSON: seis nutrientes (hierro, zinc, cobre, yodo, selenio, manganeso) **no tienen máximo nutricional publicado**, así que la lectura literal los dejaría sin ningún techo |
| §3.1.4-3.1.6 validación, repetición de análisis e instrucciones de uso | **No se aplican**: son obligaciones de un fabricante que pone un producto en el mercado |

### §3.2.1 Cómo se leen las tablas

| Lo que dice | Decisión |
|---|---|
| *«Legal maxima in EU legislation are expressed on 12% moisture content and they do not account for energy density. Therefore in these guidelines they are only provided on a dry matter basis»* | **Medido, y hoy es benigno por coincidencia.** Convertimos ×2,5, que supone 4000 kcal/kg de materia seca. Una ración BARF de este motor mide **4040 kcal/kg MS** al 35 % de materia seca: un 1 % de diferencia. Pero el catálogo **no guarda la materia seca de ninguna de sus 163 fichas**, así que eso no se puede recalcular, solo estimar |

### §3.3.1 Sustanciación (perro) — de dónde sale cada número

| Lo que dice | Decisión |
|---|---|
| Proteína adulto: la RA del NRC (25 g/1000 kcal) ajustada por digestibilidad aparente del 80 %, menor ingesta energética y los requisitos del perro viejo | Contexto de la cifra que ya aplicamos |
| *«If formulating below the recommended minimum for total protein it is particularly important to ensure that the amino acid profile meets FEDIAF guidelines for adult maintenance»* | **HALLAZGO, y es el que contesta a Cris.** Es la **cuarta** fuente que contempla formular por debajo del mínimo de proteína, y la única que dice **la condición**: que el perfil de aminoácidos siga cumpliendo. El motor ya verifica los **12 aminoácidos por separado**, así que esa condición se cumple por construcción — no hay nada que construir, hay que **decir** que está cumplida |
| Proteína en reproducción: *«If carbohydrate is absent or at a very low level, the protein requirement is much higher, and may be double»* | **Ya aplicado** (`requisitos_condicionales.json`) |
| Proteína en crecimiento: 25 % MS recién destetados, 20 % MS a partir de las 14 semanas | **Ya en la tabla** |
| Arginina: *«For every gram of crude protein above the stated values, an additional 0.01 g of arginine is required»* | **Ya aplicado.** Y esta lectura rehace la cuenta: el Anexo 7.4 lo enuncia **por cada 1 % de proteína en materia seca** y §3.3.1 **por cada gramo**, que parecen dos reglas distintas. Convertido: 0,01 g/100 g MS = 0,025 g/1000 kcal, y 1 % MS = 2,5 g/1000 kcal → 0,01 g de arginina por gramo de proteína. **Coinciden**; no había error |
| Lisina, techo del cachorro: 2,91 % MS a 4156 kcal/kg = 7,0 g/1000 kcal | **Ya es la única excepción escrita** (`MAXIMOS_NO_APLICADOS`) |
| Metionina-cistina adulto: *«The recommended values are based on a dog food containing a very low taurine content, i.e. <100 mg/kg dry matter … For products containing higher levels of taurine the RA for sulphur amino acids can be **lower** than the values quoted in the table»* | **No se aplica, y el motivo importa.** Bajar un mínimo no es apretar, y gana FEDIAF. Pero explica por qué el mínimo de metionina+cistina que aplicamos es el del **caso peor** (una dieta sin taurina) cuando una ración BARF con carne y corazón lleva taurina de sobra — y por qué a Cris «le sale carente de metionina» al bajar la proteína en el IRIS 4. Refuerza la ficha de **L-metionina** que falta en el catálogo |
| *«Methionine In the case of lamb and rice foods, the methionine level may have to be increased»* | **PENDIENTE DE DECIDIR**: no hay arroz en el catálogo, pero **sí hay cordero**. Sin cifra en la fuente |
| Tirosina: *«For maximisation of black hair colour, the tyrosine content may need to be 1.5 to 2 times higher»* | **No se aplica**: es cosmético, no es un requisito de salud |
| Grasa: *«Fat per se is not essential … Therefore the minimum recommendation for total fat in adult dogs with a MER of 95 kcal/kg BW0.75 has not been adjusted»* | **Ya aplicado**: es justo por esto que la grasa no escala en `minimo_de()` |
| Omega-3 y 6 en crecimiento y reproducción: el DHA y el araquidónico se acumulan en cerebro y retina, y suplementar a la madre con ALA y linoleico *«is an ineffective means of increasing the milk content of DHA and AA»* | **Ya aplicado**: son las filas de EPA+DHA (0,13 g) y araquidónico (75 mg) de crecimiento y reproducción |
| *«Omega-3 fatty acids (Adult dogs) … the current information is insufficient to recommend a specific level of omega-3 fatty acids for adult dogs»* | **Ya anotado**: nuestro mínimo de adulto (0,11 g) es del NRC 2006 y se adopta a propósito, con la nota puesta en el JSON |
| **§3.3.1 «Omega-3 vs. 6 FA (Adult dogs)»**: *«The effects of omega-3 fatty acids depend on the level as well as on the ratio of omega-6 to omega-3 fatty acids. Very high levels of long chain omega-3 fatty acids can decrease cellular immunity, particularly in the presence of a low level of omega-6 fatty acids»* | **HALLAZGO, y es el lipidograma de Cris.** La frase que llevamos repitiendo —«FEDIAF no se moja con el omega-6:omega-3»— **es media verdad**: FEDIAF dice que el ratio importa, dice **en qué dirección está el daño** (omega-3 alto con omega-6 bajo) y no da número. Es la **cuarta** fuente que lo pide y ninguna da cifra para el perro sano. Sigue **pendiente de decidir**, pero ya no por falta de respaldo: por falta de cifra |
| Calcio adulto: *«As the calcium level approaches the stated nutritional maximum, it may be necessary to increase the levels of certain trace elements such as zinc and copper»* | **PENDIENTE DE DECIDIR.** El motor no sube el zinc ni el cobre cuando el calcio se acerca a 6250 mg/1000 kcal. Es medible sobre los 216 menús del catálogo, y no está medido |
| Calcio del cachorro: ≥1 % MS en crecimiento temprano; razas grandes y gigantes siguen con ≥1 % hasta los ~6 meses; pequeñas y medianas pueden bajar a 0,8 % MS y subir el Ca:P a 1,8/1 | **Ya aplicado** (notas a y b de la tabla) |
| Máximo de calcio del cachorro: 1,6 % MS desde las 9 semanas no da efectos; hasta 1,8 % MS en crecimiento tardío en todas las razas *«with the exception of great Danes. This breed may be more susceptible and it is preferable to continue with a food containing a maximum calcium content of 1.6%»* | **No hace falta aplicarlo, y está medido por qué.** FEDIAF nombra **una raza** por su nombre y el motor no la distingue — pero al cachorro de más de 25 kg de adulto ya le aplicamos **2750 mg/1000 kcal**, que son **1,10 % MS**: por debajo tanto del 1,6 como del 1,8. La excepción del Gran Danés queda cubierta por una regla más estricta que ya está puesta |
| Sodio: 45,4 mg/MJ (0,19 g/1000 kcal) es adecuado en todas las etapas; 2 % MS puede dar balance negativo de potasio | Contexto. El mínimo que aplicamos (250-290 mg) es el de la tabla, más alto que el de la sustanciación |
| Fósforo: AAFCO introdujo los máximos nutricionales de Ca (6,25) y P (4,0 g/1000 kcal) en 1992 y *«FEDIAF adopted the same nutritional maximums»*; el exceso de P daña sobre todo con Ca:P ≤0,4:1; Stockman 2017 toleró 7,1 g Ca y 4,5 g P (Ca:P 1,6) durante 40 semanas | **Ya aplicado**, y es la cita que devolvió el techo de 4000 la noche del 8-sep |
| Oligoelementos: la biodisponibilidad baja con calcio alto, con zinc alto (que baja el cobre) y con fitatos | Misma familia que el calcio de arriba. **Pendiente** |
| Cobre: *«Owing to its low availability copper oxide should not be considered as a copper source»* | **Ya aplicado** (9-sep, desde SACN5). FEDIAF es la **segunda** fuente que lo dice |
| Hierro: *«iron from oxide or carbonate salts that are added to the diet should not be considered sources contributing to the minimum nutrient level»* | **Ya aplicado para el óxido** (desde SACN5). **El carbonato es nuevo**: FEDIAF lo iguala al óxido y SACN5 solo hablaba del óxido. Hoy no afecta —no hay ninguna ficha de carbonato de hierro en el catálogo— y queda escrito para el día que alguien proponga una |
| Yodo: FEDIAF **descarta** el máximo bajo de Castillo (0,4 mg/100 g MS) porque los cachorros del estudio estaban sobrealimentados un ~75 % y la comida era deficiente en Ca, P y K, y concluye que *«the existing legal maximum is safe for all dogs»* | **Conflicto confirmado con la cita.** Nuestro tope crónico de yodo son 1275 µg/1000 kcal (NRC 2006 / Belshaw) y el legal de FEDIAF son 2750. Ya está en `FEDIAF_CONTRA_OTRAS_FUENTES.md` como uno de los cinco; ahora tiene la frase literal de FEDIAF al lado |
| Selenio en crecimiento: el requisito medido son 0,21 mg/kg MS y se añade margen por la baja disponibilidad en pienso | Contexto |
| Zinc en crecimiento: 5 mg/100 g MS basta con dieta purificada y *«doubling the minimum recommended level may be considered safe»* | Contexto de la cifra de la tabla |
| Vitamina A: el máximo de FEDIAF es el **80 %** de la dosis que «se acerca a desafiar la homeostasis» y ~45 % del no-adverse-effect de un año; Hathcock dio **tres veces** el máximo de FEDIAF durante diez meses sin efectos | **No cambia nada**, pero es exactamente el tipo de dato que necesita `margen_profesional`: dice cuánto colchón hay por encima del techo |
| Vitamina D: 435 IU/100 g MS afectó la absorción de calcio en cachorros de Gran Danés; **320 IU/100 g MS para gigantes en crecimiento** y **425 para cachorros de raza pequeña**; para las demás etapas, el mismo que el del cachorro | **No se aplica la distinción por tamaño**: el motor pone 320 (nutricional) a todos, y encima aplica el legal (227), que es más bajo todavía. Lado estricto, y con el mismo número para todos |
| Vitamina E: *«An increased level of vitamin E may be required if the intake of PUFA is high, particularly from fish oil»* | **Ya documentado** como `tipo: documentado_sin_cifra` — FEDIAF lo enuncia y no lo cuantifica para el perro |
| Vitaminas B: el mínimo es el AI del NRC, *«based on bioavailable forms coming from a **vitamin premix** at the point of consumption»* | **Refuerza un hueco que ya está abierto.** Los mínimos de las B suponen la forma de un premezclado, y ninguna ficha del catálogo dice en qué forma química vienen sus vitaminas B. Está en `DATOS_QUE_FALTAN.md` |
| Riboflavina: 66,8 µg/kg PV/día con dieta semipurificada → 0,6 mg/100 g MS con un 25 % de margen | Contexto |
| Biotina y vitamina K: *«does not need to be added to the food unless the food contains antimicrobial or **anti-vitamin** compounds»* | **Ya aplicado por las dos puntas.** Las dos filas están fuera de la tabla a propósito, y la condición que FEDIAF pone —que haya antivitaminas— la cubren ya dos topes de `seguridad.py`: la **tiaminasa** del pescado crudo (antitiamina) y la **avidina** de la clara cruda (antibiotina, tope del 20 % del peso, Am J Vet Res 1984). FEDIAF es la segunda fuente de la regla |

### §4 Alimento complementario — y aquí hay una frase de `CLAUDE.md` que es falsa

| Lo que dice | Decisión |
|---|---|
| §4.1 *«The total daily ration should match the recommended allowances and nutritional and legal maximum values listed in the tables for complete pet food»* | **CORRIGE LA DOCUMENTACIÓN.** La regla 3-bis de `CLAUDE.md` dice que **«FEDIAF no dice nada de esto»** sobre los premios. **Sí dice**, y dice justo lo que hacemos: el día **entero** —ración más premios— tiene que cumplir los mínimos. Y dice una cosa más que nosotros no afirmábamos: que los **máximos** también se miden sobre el día entero. El motor no los escala (a propósito: de lo que lleva dentro un premio no sabemos nada), así que seguimos por el lado seguro, pero la frase hay que cambiarla |
| Los premios *«may be given in quantities that impact total energy intake. The feeding instructions should give clear recommendations on how not to overfeed»* | **Ya aplicado**: es la pregunta de los premios |
| La clasificación en tres categorías (a: aportan energía; b: aportan nutrientes; c: para entretener, como los masticables) | **No se aplica**: el motor no clasifica premios, cuenta sus kcal |

### §5 Métodos analíticos y §6 Protocolos de ensayo

| Lo que dice | Decisión |
|---|---|
| La Tabla V-1 con el método de laboratorio de cada nutriente, y los dos protocolos de digestibilidad (indicador y colección cuantitativa) | **No se aplican**: son de laboratorio y de fabricante. Se anotan para que no se vuelvan a «descubrir» dentro de seis meses |
| *«Vitamin D analysis of pet foods containing levels … between 500 and 1000 IU/kg DM is difficult and unreliable. The detection limit for HPLC methods is approximately 3000 to 5000 IU/kg»* | **No se aplica**: es una limitación analítica, no un requisito |

### Anexo 7.1 — Body Condition Score

| Lo que dice | Decisión |
|---|---|
| La Tabla VII-2, con el % de peso por encima o por debajo del BCS 5 en cada uno de los nueve puntos | **Ya aplicado**: es `peso_objetivo_desde_bcs()` |
| *«The ideal BCS should therefore be between 4/9 and 5/9»* y *«dogs should be fed to maintain a body condition score (BCS) between 4 and 5»* | **PENDIENTE DE DECIDIR.** El motor toma `BCS_NEUTRO = 5.0`: un perro en BCS 4 se considera **por debajo** del ideal y se le sube el objetivo. FEDIAF dice dos veces que el ideal es **4 a 5**, no 5. Apoyado en Kealy 2002, el estudio de 14 años con labradores donde la restricción alargó la vida |
| La Tabla VII-3, escala de masa muscular de 4 puntos | **PENDIENTE DE DECIDIR.** No se ofrece en ninguna pantalla. La propia fuente reconoce que la parte baja del BCS *«[is] confounded by muscle atrophy»* — o sea que el motor no sabe distinguir un perro delgado de uno atrofiado, y son dos raciones distintas. Es un dato que un veterinario tiene |

### Anexo 7.2 — Energía

| Lo que dice | Decisión |
|---|---|
| §7.2.2.2 b) La ME de *«products of vegetable or animal origin, in their natural state, fresh or preserved, such as meat, offal, milk products»* se predice con **kcal ME = 4 × %proteína + 9 × %grasa + 4 × %NFE** | **COMPROBADO, y coincide.** Es la ecuación que FEDIAF manda usar para un catálogo como el nuestro, que es carne cruda. Rehecha contra las 140 fichas con energía declarada, sin el término NFE (que el catálogo no guarda): **mediana de desviación 1,3 % en carne muscular, 0,0 % en hueso carnoso, 1,4 % en pescado, 2,7 % en vísceras**. Los únicos por encima del 10 % son los hígados (glucógeno), las semillas, el yogur y la fruta y la verdura — todos con hidratos que el término que falta explicaría. O sea: las kcal del catálogo son las que FEDIAF calcularía. **No hay nada que cambiar, y ahora está medido** |
| Tabla VII-5, energías brutas (proteína 5,7 · grasa 9,4 · NFE+fibra 4,1 kcal/g) | **No se usa**: no calculamos energía bruta |
| Tabla VII-6, MER por edad: 1-2 años **130**, 3-7 años **110**, >7 años **95** kcal/kg^0,75 | **Conflicto ya anotado** (la edad del sénior), en `FEDIAF_CONTRA_OTRAS_FUENTES.md` |
| Tabla VII-7, DER por actividad, con el Gran Danés (200) y el Terranova (105) | **Ya aplicada**, con el hueco de «Obese prone adults ≤ 90» declarado en `niveles_de_actividad.json` |
| **Tabla VII-8a, las cinco ecuaciones de la curva de crecimiento**, válidas de las 8 semanas al año: `% del peso adulto = a·Ln(semanas) − b`, con (a, b) = (36,92 · 43,57) para ≤7 kg, (36,86 · 48,22) para >7-15, (39,88 · 60,70) para >15-27,5, (36,96 · 56,18) para >27,5-47,5 y (36,61 · 62,39) para >47,5 | **HALLAZGO Y PENDIENTE DE DECIDIR — es el más gordo de esta lectura.** El motor estima el peso adulto con `CURVA_CRECIMIENTO` de `der.py`, una tabla cuyo propio comentario dice que viene de *«reproducciones divulgativas»* de las curvas WALTHAM y *«NO del texto del estudio»*. FEDIAF publica **la ecuación exacta**, y no coinciden. **Medido, dentro del rango de validez (2 a 12 meses)**: en perros pequeños la diferencia va de −1,5 a +3,2 puntos, pero en los grandes el motor va **sistemáticamente por debajo** — un cachorro de más de 47,5 kg de adulto, a los 6 meses, para FEDIAF va por el **57,0 %** de su peso adulto y para nosotros por el **45,0 %**, 12 puntos. Y eso **sobrealimenta**: menos % supone un peso adulto estimado mayor, que en la ecuación de Klein sube el coeficiente. Para un cachorro de 30 kg a los 6 meses son **2479 kcal con nuestra tabla contra 2271 con la ecuación de FEDIAF, un 9 % de más** — justo en la población en la que la propia FEDIAF dice que sobrealimentar *«can result in skeletal deformities especially in large and giant breeds»*. ⚠️ **Y hay que leer la tabla del PDF, no del texto extraído**: en el `.txt` las cinco bandas y las cinco ecuaciones salen en dos columnas cruzadas y **el orden no es el que parece** (la banda >15-27,5 lleva −60,70 y la >27,5-47,5 lleva −56,18, que no es monótono). Las cinco parejas de arriba están leídas del PDF por coordenadas |
| Tabla VII-8b, gestación (132 · kg^0,75, y +26 · kg en las últimas 5 semanas) y lactancia (145 · kg^0,75 + el extra por camada y semana) | **Ya aplicadas**, en los dos repos |
| *«puppies should never be fed ad libitum»* | **No se aplica**: no es una cifra, y el motor da una ración |
| Fuera de la zona termoneutra, la MER sube **2-5 kcal por kg^0,75 y por cada grado**; un perro que vive fuera en invierno puede necesitar **10 a 90 % más** | **PENDIENTE DE DECIDIR.** La ficha no pregunta dónde vive el perro ni con qué clima, y esto mueve las kcal más que casi cualquier otra cosa que sí preguntamos. Es la familia del nivel de actividad: un dato que el dueño sabe y el motor no recibe |
| Tabla VII-11, los requisitos por kg de peso metabólico | **Ya aplicada**: es la base de la ecuación de §7.2.5 |
| §7.2.5, `Units/1000 kcal = requisito por kg PM × 1000 / DER por kg PM` | **Ya aplicado**: es `minimo_de()`, y solo hacia arriba |

### Anexos 7.3 a 7.7

| Lo que dice | Decisión |
|---|---|
| 7.3 Taurina: en el perro no es esencial; *«low plasma levels of taurine (< 40 µmol/L) may also predispose to dilated cardiomyopathy»*; los **Terranova** sintetizan menos; *«Feeding certain lamb and rice foods may increase the risk of a low-taurine status»* | **PENDIENTE DE DECIDIR.** Hay cordero en el catálogo y el Terranova está en `razas.json`. La cifra que decide (la taurina de 89 fichas) depende de **Spitze 2003**, que no está en el repo |
| 7.4 Tabla VII-13, arginina por contenido de proteína | **Ya aplicada** |
| 7.5 Tabla VII-14, factores de conversión de cada forma química | **Ya aplicada y auditada** (`fediaf_conversiones_vitaminas.json`, rehecha por `auditar_transcripcion_fediaf.py`) |
| 7.6 Reacción adversa: el prurito es el signo en casi el 100 % de los casos; los alérgenos más citados son leche, vaca, huevo y cereales, y los estudios controlados señalan trigo, soja, **pollo** y maíz | **Ya cubierto** por el aviso de proteína novel de la patología. No hay cifra que aplicar |
| 7.7 Tóxicos, **con sus dosis**: uva 19,6 g/kg PV, pasa 2,8 g/kg PV, teobromina 90-115 mg/kg PV en los casos letales, cacao en polvo ~4 g/kg PV, cebolla fresca 5-10 g/kg PV, ajo 5 g/kg PV (= 1,25 ml de extracto) | **No se aplican las dosis, y a propósito**: el motor **prohíbe el alimento entero**, que es más estricto que cualquier umbral. Se anotan porque son las cifras que habría que usar el día que alguien quiera avisar en vez de prohibir |
| 7.7 *«Wild onions (A. validum & A. Canadense) and wild garlic (A. ursinum) have caused haemolytic anaemia in horses and ruminants (Lee K-W et al. 2000) and are potentially toxic for dogs and cats as well»*, y que el gato es más sensible | **Ya cubierto**: `TOXICOS_FEDIAF_7_7` filtra por palabra |

### Anexo 7.8 — las tablas VII-17a-d, y el cruce que nadie había hecho

FEDIAF publica **dos veces** la misma tabla de requisitos: como Tablas III-3a-c
(por etapa) y como Tablas VII-17a-d (por etapa y por MER). `auditar_fediaf.py` y
`auditar_transcripcion_fediaf.py` comprueban la primera copia contra el PDF.
**La segunda no la miraba nadie**, y una discrepancia entre las dos sería un
error interno de FEDIAF que ningún auditor nuestro podría ver.

Cruzadas ahora, extrayendo las cuatro tablas del `.txt` y comparándolas contra
`requerimientos_v2_final.json` columna por columna:

| | |
|---|---|
| Celdas que coinciden exactas | **186** |
| Diferencias por unidad (calcio, potasio y magnesio en g contra mg; vitamina E en UI contra mg con el ×0,671 de la Tabla VII-14) | 17, todas correctas |
| Diferencias reales | **1**, y está documentada: el mínimo de EPA+DHA en adulto. VII-17c y VII-17d lo dejan en «-» y nosotros ponemos 0,11 g. **Es a propósito**: viene del NRC 2006 y su `nota_auditoria` ya lo dice |
| Filas donde las dos copias dicen «-» para el perro (biotina, vitamina K) | Coinciden |
| Fósforo de adulto (que se cayó una vez): VII-17c min 1,00 / VII-17d min 1,16 / máximo 4,00 (N) en las dos | Coinciden con 1000, 1160 y 4000 |
| Colina: 425 en crecimiento y reproducción, 409 con MER 110, 474 con MER 95 | Coinciden |

**Las dos copias de FEDIAF dicen lo mismo, y las dos dicen lo que aplica el motor.**

### §8 Registro de cambios de FEDIAF

No es normativo, pero sirve de comprobación cruzada de los techos legales, que
son los que cambian con la ley. Los dos que se pueden verificar contra nuestro
JSON **cuadran**: el máximo legal de **zinc** bajó de 28,40 a **22,70** mg/100 g
MS en 2017 (nuestro `maxAdulto` es 56,75 = 22,70 × 2,5) y el de **hierro** de
142,00 a **68,18** en 2020 (el nuestro es 170,45 = 68,18 × 2,5).

---

### Lo que sale de esta lectura, en una lista

**Para aplicar o decidir (7):**

1. **La curva de crecimiento de la Tabla VII-8a.** FEDIAF publica cinco
   ecuaciones y usábamos una tabla divulgativa. Medido: hasta 12 puntos de
   diferencia y ~9 % de kcal de más en el cachorro de raza gigante.
   **APLICADA en `der.py` el mismo día**; queda decidir si se lleva también al
   frontend, donde hoy no hay curva ninguna. Ver P-14.
2. **El BCS ideal es 4-5, no 5.** `BCS_NEUTRO = 5.0`.
3. **La digestibilidad mínima (≥70 % MS, ≥80 % proteína)** es la condición de
   validez de toda la tabla y el catálogo no tiene ese campo.
4. **El zinc y el cobre cuando el calcio se acerca al máximo.** Sin medir.
5. **La escala de masa muscular** (Tabla VII-3), que separa delgado de
   atrofiado.
6. **La temperatura ambiente**, que la ficha no pregunta y vale entre un 10 y
   un 90 % de las kcal.
7. **El cordero y la taurina** (y el Terranova), bloqueado por Spitze 2003.

**Para corregir en la documentación (2):**

8. La regla 3-bis de `CLAUDE.md` dice que **«FEDIAF no dice nada»** de los
   premios. **§4.1 sí dice**, y dice lo mismo que hacemos.
9. `FEDIAF_CONTRA_OTRAS_FUENTES.md` y `PARA_EL_NUTRICIONISTA.md` afirman que
   FEDIAF manda siempre. **§2.2 excluye a las dietas para un propósito
   nutricional particular**, o sea a las patologías.

**Confirmado y medido, sin cambio (3):**

10. Las kcal del catálogo coinciden con la ecuación que FEDIAF manda usar para
    carne cruda (mediana del 1,3 %).
11. Las dos copias que FEDIAF publica de su tabla de requisitos coinciden entre
    sí y con el motor (186 celdas).
12. El techo de calcio del Gran Danés ya está cubierto por una regla más
    estricta que aplicamos (1,10 % MS contra el 1,6 % de FEDIAF).

---

## TVT Merkblatt 181 «BARF» — las dos ediciones · leídas enteras el 12-sep-2026

*Tierärztliche Vereinigung für Tierschutz e.V., Arbeitskreis Hunde und Katzen.*
Julio de 2017 y mayo de 2025. Es la única fuente del repo que trata **este
producto**: una hoja informativa de la asociación veterinaria alemana de
protección animal dedicada entera a la alimentación cruda. Está en alemán, y hasta
hoy solo se había leído su página 5 —de ahí salió el bloqueo de los cortes con
tiroides el 6 de septiembre—. **Las dos ediciones dicen lo mismo en las dos cifras
que importan**, comprobado: el ratio Ca:P y las proporciones clásicas.

⚠️ Y como AAHA, **esta fuente no recomienda lo que hacemos**, y con más contundencia:
«Die Ernährung von Hund und Katze mit einer inadäquaten BARF-Ration ist als
tierschutzrelevant einzustufen» —una ración BARF inadecuada es un asunto de
protección animal—, y «alle Vorteile des „Barfens“ auch durch die Verfütterung
gekochter Rationen erreicht werden» —lo mismo se consigue cocinando—. Va a la
misma pregunta que AAHA, la P-20.

### Lo que ya está aplicado, y esta fuente confirma

| Lo que dice | Decisión |
|---|---|
| «Verfütterung von Schlundfleisch und Hühnerhälsen: daran befindet sich in der Regel noch die Schilddrüse der geschlachteten Tiere, was bei regelmäßiger Verfütterung aufgrund des Gehaltes an Schilddrüsenhormonen zu einer Schilddrüsenüberfunktion (Hyperthyreose) bei Hunden führen kann» | **Ya aplicado** desde el 6 de septiembre: `TIROIDES_EXCLUIR` en `seguridad.py`, bloqueo de nivel A (no lo levanta ni un veterinario). Afecta a cuello de pavo, de pato, de ternera y laringe de vacuno. ⚠️ Y comprobado hoy: el catálogo precalculado ya **no tiene ninguna referencia** a esas cuatro fichas — el comentario del código decía que quedaban 56 y se limpiaron al regenerarlo |
| «Die Verfütterung von Eiklar führt zur Bindung von Biotin, wodurch dieses nicht mehr resorbiert werden kann» y que la clara lleva inhibidores de tripsina | **Ya aplicado**: el tope de clara cruda de `seguridad.py`, con la avidina escrita al lado, y el huevo ENTERO sin topar porque la yema trae biotina |
| «Bei einigen Fischarten führt die rohe Verfütterung zu einem Abbau von Thiamin (Vitamin B1), durch das im Fisch enthaltene, hitzelabile Enzym Thiaminase» | **Ya aplicado**: la tiaminasa es uno de los cinco topes crónicos del solver |
| «Die Verfütterung von Knoblauch und Zwiebeln wird, obwohl für das Tier giftig, gerne und fälschlicherweise zur Verfütterung als „Antiparasitikum“ verwendet» | **Ya aplicado**: `TOXICOS_FEDIAF_7_7` filtra ajo y cebolla por palabra |
| El riesgo bacteriano (Salmonella, Listeria, Campylobacter, E. coli, botulismo, H5N1 en gato), las resistencias a antibióticos y las aminas biógenas | **Ya cubierto** por el aviso de higiene del 10 de septiembre, de WSAVA. Esta fuente añade el H5N1 en pienso crudo congelado comercial y las **aminas biógenas** de la cadena de frío rota, que son nuevas y son de manipulación, no de fórmula |
| Contraindicaciones: renal, hepático, urolitos, animal viejo, inmunodeprimido, cachorro, gestante/lactante | **Ya cubierto en seis de siete**: el motor tiene `renal`, `hepatopatia`, los cuatro urolitos e `inmunosupresion`, y los tres primeros no formulan menú automático o lo formulan con topes. La séptima, la gestante, es distinta: la fuente dice que **no hay estudios** de la flora de la perra preñada con BARF, así que no es un tope, es un hueco de la literatura |

### Lo que NO se aplica, con el motivo

| Lo que dice | Por qué no |
|---|---|
| ⚠️ El ratio calcio:fósforo **«optimal 1,3 – 1,5»**, igual en las dos ediciones | **NO se aplica, y hay que verlo medido antes de decidir.** FEDIAF pide 1,0-2,0 y es lo que aplica el motor. Medido el 12-sep sobre los 216 menús del catálogo: van de **1,00 a 1,74, mediana 1,16**, y solo **25 de 216** caen dentro del 1,3-1,5 que pide TVT — 188 están por debajo de 1,3. O sea que aplicarlo como suelo no es un ajuste: cambia el 87 % de los menús. Es la clase de `recomendaciones_libro.json` (una recomendación al perro sano que cabe dentro de FEDIAF), y va a `PREGUNTAS_ABIERTAS.md` con su medida |
| Las proporciones clásicas del BARF según esta fuente: «„Klassische“ BARF-Rationen bestehen zu ca. 60 - 80 % aus Fleisch, 10 - 30% aus fleischigen Knochen, 10 - 25% aus Gemüse und Obst und etwas Pflanzenöl» | **No se aplica, y es FORMA (regla 3), no nutrición** — pero la diferencia es grande y se dice: nuestra plantilla parte de **50 % de hueso carnoso** con margen 20-60 %, o sea que el punto de partida está **por encima del máximo** que publica esta fuente (30 %), y nuestra verdura va de 2 a 10 % contra su 10-25 %. Nuestra plantilla está documentada como convención de divulgación (Billinghurst 1993) «sin estudio detrás», y se probaron cinco repartos sobre 300 menús cada uno con resultado casi idéntico. Lo que legitima la ración es la verificación contra FEDIAF, no la plantilla. Queda escrito porque es la primera fuente **veterinaria publicada** que da otras proporciones |
| «Beliebte Schlachtabfälle wie Lunge und Euter sind bindegewebsreich und somit schwer verdaulich» | **No se aplica: no hay cifra y el motor no modela digestibilidad** (P-16). El catálogo tiene tres fichas de pulmón (vaca, cordero, ternera) y ninguna de ubre. Se anota porque el pulmón ya estaba marcado en el repo como caso debatido entre carne y víscera, y esta fuente da un motivo distinto para mirarlo |
| El perro digiere el almidón mucho mejor que el lobo, y una dieta sin cereal solo tiene sentido en el poquísimo perro con sensibilidad al gluten; y que el lobo come un 10-21 % de su peso al día contra el 2-3 % del perro, así que con esa ración **no llegan los oligoelementos** sin suplementar | **No se aplica, y a la vez es el argumento de por qué existe este motor**: el suplemento no es opcional y por eso Suplementos y Extras van siempre libres (regla 5). No hay cifra que meter |
| «Das sogenannte BARF-Profil aus einer Blutprobe kann nur sehr bedingt Aufschlüsse über eine Fehlernährung geben», con el ejemplo de que el calcio en sangre sigue normal con fracturas patológicas ya presentes | **No se aplica: no es una cifra de ración.** Pero es de lo más útil que dice para quien firma, porque es el contraargumento a «le hice una analítica y salió bien» |
| Que la ración la calcule un veterinario con la especialidad de nutrición, y que en cachorro, geriátrico o enfermo crónico haya revisión periódica | **No se aplica** como regla del motor. Coincide con `quien_formula_cada_patologia.json`, donde 24 de las 47 son `solo_veterinario` |
| Que no se debería dar crudo si en casa hay personas inmunodeprimidas, ancianas, embarazadas o niños pequeños, ni en perros de terapia ni en protectoras | **No se aplica: es del hogar, no del plato.** El motor no pregunta quién vive en la casa, y no propongo que lo pregunte. Queda escrito |

---

## Ishii CS et al. 2025 — las purinas de la comida de perro, medidas · leído entero el 12-sep-2026

*BMC Veterinary Research 21:626.* Nueve metabolitos de purina medidos por
cromatografía líquida y espectrometría de masas en tres lotes de cada una de 24
dietas comerciales (14 secas, 10 húmedas) de los tres fabricantes grandes. Es la
fuente que el repo tenía apuntada como «Purinas (Malandain/Ishii)» y no había
leído.

| Lo que dice | Decisión |
|---|---|
| ⚠️ **LA REGLA DE CONVERSIÓN, que es lo que más falta hacía**: *«The weight of purines from previous reports can be converted to millimoles by dividing the weight of purine (mg) by the molecular mass of the nuclear bases (131–152 mg/mmol), whereas millimoles can be converted to mg Eq UA by multiplying by the molar mass of UA (168 mg/mmol)»* | **APLICADA para poder comparar**. El motor trabaja en mg/1000 kcal y esta fuente publica en µmol/Mcal; sin esta frase las dos cifras no se pueden mirar juntas, que es exactamente el fallo de unidades que ya costó un error en este repo |
| El umbral de dieta baja en purinas: *«All dry Rx diets, except for one LoPr diet, contained less than 630 μmol of total purines per Mcal ME, previously reported to decrease urinary UA and allantoin concentrations in healthy dogs»* | **CONFIRMA el número que el motor ya tenía escrito.** 630 µmol/Mcal son **82,5-95,8 mg/1000 kcal** con la conversión de arriba, y el `objetivo_terapeutico_por_1000kcal` de `urato` es **90**. Cae dentro de la banda, y viene de una fuente distinta y de un método distinto |
| Las medias por categoría: receta 736 µmol/Mcal (IC 475-1053) contra mantenimiento **2459** (1866-3133); seco 464 contra húmedo **1704**; y el peor grupo, mantenimiento en lata, **3218** | **Sirve para medir lo lejos que estamos.** Ver abajo |
| *«Hypoxanthine was the most abundant purine in most foods»* (30 % de la mediana) y es la que más sube el ácido úrico en orina; *«hypoxanthine has been reported to constitute more than 50% of the purines in animal meats and offal, whereas more than 60% of the purines in vegetables are composed of other purines such as adenine and guanine»* | **No se aplica: el catálogo no separa las purinas por tipo.** Sus valores son el total del USDA/ODS. Se anota porque es la razón por la que «bajar purinas» no es lo mismo en un pienso vegetal que en carne |
| *«Inosine was the predominant purine in frozen stored raw fish»*, y la hipoxantina alta de los piensos se explica porque cocinar por encima de 100 ℃ degrada el IMP y la inosina a hipoxantina | **No se aplica, y es el mayor límite de esta comparación**: sus 24 dietas están **cocinadas** y una ración BARF no. El reparto por tipo de purina de un alimento crudo y congelado no es el de esta tabla |
| Ishii: *«these results suggest that dry food may offer an advantage in preventing urate urolithiasis especially if dry food is moistened before feeding»* | **No se aplica**: no formulamos pienso. Refuerza el aviso que ya tiene `urato`, que manda a dieta terapéutica |
| *«the ratio of total purine (μmol) to protein (g) varied several fold between diets within some categories»*, contra la idea de que las purinas van con la proteína | **Ya recogido** el 12-sep en el aviso de `urato`, con la frase de AAHA. Esta fuente lo **mide**: de 1 a 38 µmol/g en los secos |
| Ishii, sobre su propio método: *«there is no standard method of measuring purine content or quality control to ensure results are comparable among different laboratories»*, y que sus valores salieron un 30 % de los de estudios previos | **Es el aviso de cómo leer todo lo anterior.** Va escrito para que la coincidencia del 90 no se lea como más precisa de lo que es |

### Lo MEDIDO con esto delante, el 12-sep-2026

Sobre los 216 menús del catálogo precalculado, con las purinas de las 163 fichas
(todas las tienen) y la conversión de la propia fuente:

| | mg/1000 kcal | µmol/Mcal (masa molar 131-152) |
|---|---|---|
| menú del catálogo, mínimo | 382 | 2.500-2.900 |
| menú del catálogo, **mediana** | **756** | **5.000-5.800** |
| menú del catálogo, máximo | 1.363 | 9.000-10.400 |
| objetivo de `urato` del motor | 90 | 590-690 |
| umbral de dieta baja en purinas (Ishii) | 82,5-95,8 | < 630 |
| el pienso **más** cargado que midió Ishii (mantenimiento en lata) | 422-489 | 3.218 |

O sea: **la ración BARF mediana lleva entre 1,5 y 1,8 veces las purinas del
pienso comercial más cargado que este estudio encontró**, y entre 8 y 9 veces el
umbral de una dieta baja en purinas. Eso **confirma con una fuente nueva** la
decisión que ya estaba tomada —`urato` no formula menú automático— y ahora tiene
un número comparable contra alimentos reales, no solo contra un objetivo.

⚠️ **Y lo que esta comparación NO demuestra**, porque hay que decirlo: sus 24
dietas están cocinadas y medidas sin hidrólisis ácida (9 metabolitos por
separado), y nuestras fichas traen el total del USDA/ODS, que se mide **tras**
hidrólisis. Los propios autores dicen que sus cifras salieron un 30 % de las de
estudios previos. La comparación vale para el orden de magnitud, que es
aplastante, no para el dígito.

---

## Dobenecker 2021 y Hofmann 2025 — el fósforo según de dónde venga · leídos enteros el 12-sep-2026

Son dos estudios del mismo grupo (Cátedra de Nutrición Animal, LMU Múnich), y
hay que leerlos juntos porque el segundo matiza al primero. El repo los cita 35
veces y no se habían leído.

**Dobenecker B, Reese S, Herbst S (2021), PLOS ONE 16(2):e0246950.** Ocho beagles
sanos, cuatro dietas consecutivas: una control que cubre justo el requisito de
fósforo y tres con **cinco veces** ese fósforo, cambiando solo la fuente —harina
de canal de ave (orgánico), NaH₂PO₄ y KH₂PO₄ (los dos inorgánicos y muy
solubles)—. Sangre a 8 tiempos en 7 horas.

| Lo que dice | Decisión |
|---|---|
| *«Pi (KH2PO4, NaH2PO4) but not organic P caused an increased apparent P digestibility and significantly influenced kinetics of serum FGF23, parathyroid hormone, P, CrossLaps and bonespecific alkaline phosphatase, demonstrating a disrupted calcium (Ca) and P homeostasis with potential harm for renal, cardiovascular and skeletal health»* | **Pendiente de decidir, y bloqueado por un dato.** Ver abajo: el motor no sabe en qué forma química viene el fósforo de sus fichas |
| *«The use of Pi in food can therefore not be considered as safe»* | Es la conclusión del resumen, y va entera porque es la frase que decide lo demás |
| La digestibilidad aparente del fósforo cambia con la fuente: orgánico **22 %** contra control 54 %, NaH₂PO₄ 53 % y KH₂PO₄ 48 % | **No se aplica**: el motor no modela digestibilidad, y eso ya está declarado como hueco (P-16). Se anota porque es la medida de cuánto se separan las dos fuentes: el mismo fósforo en el plato, más del doble absorbido |
| Con los dos fosfatos inorgánicos, el producto calcio×fósforo en suero superó el umbral de 55 mg²/dl² **desde la primera hora** y llegó a 180, y el FGF23 llegó a 1655 pg/ml —*«which is otherwise found in dogs with IRIS stage 3»*— en perros **sanos** | **No se aplica: son cifras de sangre, no de ración.** Van escritas porque son el número contra el que un veterinario mediría si esto le preocupa |
| ⚠️ *«This implies that a mere increase of the Ca/P ratio in a product with considerable amounts of soluble Pi salts does not suffice to protect the user from a high P burden»* | **ESTO SÍ NOS TOCA, y no es una cifra: es un límite de nuestra protección.** El motor se defiende del fósforo con dos cosas, el techo por 1000 kcal y el ratio Ca:P, y la fuente dice que la segunda **no protege** si el fósforo viene de una sal soluble. Subir el ratio de 1,4 a 1,9 no evitó ni la subida del fósforo en suero ni la del producto Ca×P |
| *«given the fact that most dogs receive multiple meals per day, the possibly threatening impact on parameters of P homeostasis might exist permanently»* | **No se aplica**: el motor da la ración del día y no decide en cuántas tomas. Se anota porque es lo que convierte un pico de 7 horas en algo permanente |

**Hofmann C, Dobenecker B, Kienzle E (2025), J Anim Physiol Anim Nutr
109:124-129.** Ocho foxhound cruzados, dos dietas que solo se diferencian en la
solubilidad del calcio y del fósforo del corrector mineral.

| Lo que dice | Decisión |
|---|---|
| ⚠️ **La frontera NO es «orgánico contra inorgánico»: es SOLUBLE contra INSOLUBLE.** En este estudio el fosfato inorgánico insoluble es el **CaHPO₄·2H₂O**, o sea el fosfato dicálcico, y es el del lado bueno: *«CaHPO4*2H2O was used as inorganic P source because of its low solubility»*, con solubilidad **0 %** al minuto y a los 90 minutos | **Cambia la pregunta que hay que hacer.** No vale saber si el fósforo de un suplemento es «inorgánico»: hay que saber **qué sal es**, porque el fosfato dicálcico —que es el vehículo habitual de estos correctores— es el insoluble |
| Digestibilidad aparente del fósforo: **20 %** con la fuente insoluble contra **26 %** con la soluble, y fósforo en orina más alto con la soluble | **No se aplica**: otra vez digestibilidad. La diferencia aquí es mucho menor que en el estudio de 2021, y los propios autores lo explican: el premix soluble perdió solubilidad con el tiempo (98 % al minuto, 43 % a los 90) formando complejos insolubles |
| La digestibilidad del **calcio** no depende de la fuente —salió negativa en los dos grupos— y en el perro el sitio principal de absorción parece ser el intestino grueso | **No se aplica, y es tranquilizador**: el catálogo tiene dos fuentes de calcio y las dos son cáscara de huevo (carbonato). Esta fuente dice que ahí la forma da igual |
| El cloruro cálcico acidifica la orina (pH 5,2-4,9 contra 5,8-5,4) y con pH por debajo de 5 sube la excreción de calcio | **No se aplica**: no hay cloruro cálcico en el catálogo. Se anota porque toca los urolitos, donde el pH urinario decide |

### Lo que sale de los dos, y está BLOQUEADO POR UN DATO

El motor mide el fósforo **total** y el ratio calcio:fósforo. No ve la forma
química, y estas dos fuentes dicen que la forma química decide. Así que la
pregunta es: **¿de dónde sale el fósforo de nuestros menús?**

**MEDIDO el 12-sep-2026 sobre los 216 menús del catálogo precalculado**, repartiendo
el fósforo de cada menú entre sus alimentos:

| | % del fósforo del menú que aporta el multivitamínico |
|---|---|
| mínimo | 0,49 % |
| mediana | **17,34 %** |
| máximo | **39,58 %** |
| menús con 0 % | **ninguno de los 216** |

O sea que **hasta cuatro de cada diez miligramos de fósforo de una ración salen
de un bote**, y de ese fósforo no sabemos la sal. Siete de los diez
multivitamínicos del catálogo declaran fósforo, de 100 a 9.200 mg/100 g, y
ninguna ficha dice en qué forma viene. Es exactamente el mismo hueco que ya está
escrito para las vitaminas del grupo B.

**No se aplica nada, y el motivo es que no se puede sin inventarse el dato.** Si
es fosfato dicálcico, Hofmann dice que es el insoluble y no pasa nada; si es
monosódico o monopotásico, Dobenecker dice que no se puede considerar seguro. Son
conclusiones opuestas para el mismo número del catálogo. Va a
`DATOS_QUE_FALTAN.md` —que no rellena el asistente— y la pregunta a
`PREGUNTAS_ABIERTAS.md` con dueño.

---

## AAHA 2021 — «Nutrition and Weight Management Guidelines for Dogs and Cats» · leída entera el 12-sep-2026

1.547 líneas de texto corrido, más **cinco tablas y un cuadro que el PDF no
suelta**. Es la fuente de la que sale la regla del BCS, y la que el repo cita 59
veces sin haberla leído nunca entera.

⚠️ **LO PRIMERO, PORQUE CAMBIA CÓMO SE CITA ESTA FUENTE.** Sus tablas están
dibujadas como trazos vectoriales, no como texto: `page.get_text()` de la página
164 —que es la Tabla 8 entera, la de los nutrientes de cada enfermedad— devuelve
**194 caracteres**, el título y el pie de página, y `get_images()` devuelve 0. No
es el problema de las dos columnas de SACN5 y FEDIAF, donde el texto estaba y
salía desordenado: aquí **no está**. Se leyeron renderizando cada página a 200
ppp y mirándolas, y la transcripción vive en `aaha_2021_tablas_transcritas.txt`,
en este repo, con su método escrito en la cabecera y con lo que la separa de
`fediaf_tabla_III_3b.txt`: aquella se puede rehacer con un script contra el PDF y
esta **no**. `auditar_citas.py` la indexa, así que una cita de la Tabla 8 se
comprueba contra ella y no cae en «fuente que no está en el repo».

⚠️ **Y HAY UN SEGUNDO DEFECTO, en el texto que SÍ se extrae, y es de la familia
del de las dos columnas.** El PDF devuelve los cuatro signos de desigualdad como
signos de puntuación corrientes: `<` sale **coma**, `>` sale **punto**, `≥` sale
`$` y `≤` sale `#`. Comprobado letra a letra contra la página renderizada a 400
ppp. Importa porque las desigualdades de AAHA son justo donde están sus cifras, y
al corromperse **no parecen rotas**: «A BCS ,4/9 or .5/9» se lee como una
enumeración y «treats and other food items make up #10%» parece una nota al pie.
Las ocho frases afectadas están escritas con sus signos buenos en
`aaha_2021_tablas_transcritas.txt`, y una de ellas trae una **discrepancia de la
propia fuente**: el texto dice «each BCS ≥5/9 is equivalent to being 10%
overweight» y su Tabla 2 pone «-» en el BCS 5 y empieza el 10 % en el 6. Manda la
tabla, que es la que trae los números y la que cuadra con la banda 4-5 — y es la
que aplica el motor.

⚠️ **Y LO SEGUNDO: esta fuente no recomienda lo que hace este producto.** «AAHA
does not advocate or endorse feeding pets any raw or dehydrated nonsterilized
foods, including treats that are of animal origin», y su Tabla 4 pone «Unconventional
diet (e.g., raw meat based, home prepared, vegetarian, vegan)» entre los factores
de riesgo que obligan a una evaluación ampliada. No es una cifra y no cambia
ninguna, pero **queda escrito**: usamos sus números para el BCS y para los
premios, y hay que decir dónde nos contradice. Va a `PREGUNTAS_ABIERTAS.md` con
dueño, porque qué se cuenta de esto en la app es decisión de producto, no mía.
Y como en ACVIM, la fuente declara quién la paga: «These guidelines are supported
by generous educational grants from Hill's Pet Nutrition, Inc., Purina Pro Plan
Veterinary Diets, and Royal Canin».

### Lo que CONFIRMA de lo que ya hace el motor

| Lo que dice | Decisión |
|---|---|
| Tabla 2: BCS 4/9 es «Ideal» y BCS 5/9 sale como «-» (no aplica). De 6 en adelante, 10 % de sobrepeso por punto: 6 → 10 %, 7 → 20 %, 8 → 30 %, 9 → 40 % | **Ya aplicado, y es la fuente exacta**. `BCS_IDEAL_MIN = 4.0` y `PCT_POR_PUNTO_BCS = 0.10` en `motor/verificar.py`. Los dos números salen clavados de esta tabla, que hasta hoy nadie había abierto |
| *«A BCS <4/9 or >5/9, MCS with any degree of loss, and unexplained weight change from the pet's previous assessment should prompt an extended assessment»* | **Ya aplicado**: es la banda 4-5 que se encendió el 12-sep. Segunda frase de la misma fuente que dice lo mismo que su Tabla 2 |
| *«Noncomplete or unbalanced food calories at >10% of a patient's daily caloric intake dilute essential nutrients and provide excess calories»* | **Ya aplicado** (regla 3-bis). Es la **séptima** fuente con el 10 %, y la que mejor dice POR QUÉ: «dilute essential nutrients», que es exactamente lo que hace el motor al escalar los mínimos por DER/(DER − premios) |
| *«Base these calculations on ideal weight»* para el plan de adelgazamiento, y en hospitalizados «base feeding calculations on current weight if ideal or underweight or on ideal BW if overweight or obese» | **Ya aplicado**: es `peso_objetivo_kg` y su regla de que sin ese campo se usa el real (lado seguro) |
| Tabla 8, oxalato cálcico: «Controlled calcium with appropriate calcium to phosphorus ratio» | **Ya aplicado**: es el ratio Ca:P 1,1-2,0 del bloque `ratios` de `oxalato`, del 10-sep. Segunda fuente independiente |
| Tabla 8, hepatopatía por cobre: «Low copper / Added zinc» | **Ya aplicado**: `hepatopatia` tiene techo de cobre 2,4 y **suelo de zinc 50** |
| Tabla 8, obesidad: «High protein / Moderate to high fiber / Low energy density / Increased nutrient to calorie ratio / Moderate to low fat» | **Ya aplicado**: `obesidad` lleva suelo de proteína 62,5 y de fibra 30 y techo de grasa 30 |
| Tabla 8, cistina: «Controlled cystine / Controlled methionine» | **Ya escrito**: `cistina` tiene `nutriente_frontera: metionina_cistina`, y no formula porque eso exige bajar del mínimo de FEDIAF |
| Tabla 8, artrosis: «High EPA/DHA ... Low energy density if overweight/obese» | **Ya aplicado**: el suelo de EPA de la artrosis, de SACN5 Tabla 34-2 |
| Tabla 8, dermatitis: «High n-3 fatty acids · Consider n-6:n-3 ratio» | **Ya escrito, y sin aplicar el ratio**: es la **tercera** fuente que pide el omega-6:omega-3 y ninguna da la cifra para el perro. Sigue en `requisitos_condicionales.json` y en la revisión de Cris |
| Tabla 8, enfermedad renal crónica: «Low phosphorus / ± potassium supplementation / High EPA/DHA», **y ni una palabra de bajar la proteína** | **Coincide con IRIS**: la restricción de proteína no es de la ERC sin más. Ver abajo, que aquí hay un conflicto |

### Lo que el motor NO decía, y se APLICA

| Lo que dice | Qué se hace |
|---|---|
| Tabla 8, encefalopatía hepática: «Low protein / ± B12 supplementation», y en las notas **«Avoid organ meats»** y **«Consider vegetarian protein sources»** | **APLICADO**: aviso nuevo en `encefalopatia_hepatica`. Importa porque una ración BARF lleva vísceras SIEMPRE —son la categoría con la que el motor cierra media tabla de vitaminas— y esta patología no formula, así que lo único que puede hacer el motor es decirlo. Ninguna de las fuentes que ya teníamos lo decía con esas palabras |
| Tabla 8, urato: «Low purines · **Does not necessarily mean low protein**» | **APLICADO al aviso profesional de `urato`, y con su matiz**, porque aquí AAHA y SACN5 **no dicen lo mismo**: la Tabla 39-4 de SACN5, que ya estaba citada en ese mismo aviso, sí pide «Restrict dietary protein to 10 to 18% dry matter». No hace falta resolverlo —esta patología no formula— y van las dos. ⚠️ Y hay que leer la frase de AAHA con cuidado: se cita a menudo como «las purinas están en las vísceras, no en la proteína», y **con este catálogo eso es falso**: quitando hígado y corazón la ración sigue en casi cinco veces el objetivo, porque la mayor parte viene de la **carne muscular**. En un pienso vegetal se pueden separar las dos cosas; en BARF no |
| Tabla 8, oxalato cálcico: «Avoid vitamin C supplementation», «Added water», y en las notas «Aim for USG ≤1.020 (dogs)» | **APLICADO como aviso**. La vitamina C no es requisito de FEDIAF para el perro y el catálogo **no tiene ninguna ficha de vitamina C** (comprobado: no existe la clave), así que hoy no hay nada que topar — pero es la puerta por la que entraría el día que alguien añada un suplemento, y la densidad urinaria es el número contra el que quien firma mide si el plan funciona |

### Lo que sale y NO se aplica, con el motivo

| Lo que dice | Por qué no |
|---|---|
| Cuadro 1, factores caninos sobre el RER (= peso^0,75 × 70): adulto castrado 1,4-1,6 · entero 1,6-1,8 · **inactivo/propenso a obesidad 1,0-1,2** · pérdida de peso 1,0 · gestación 3,0 (últimos 21 días) · lactancia 3,0 a ≥6,0 · crecimiento <4 meses 3,0 y ≥4 meses 2,0 · trabajo ligero 1,6-2,0, moderado 2,0-5,0, intenso 5,0-11,0 | **No se aplica: manda FEDIAF**, que publica su propia Tabla VII-7 y es la que usa el motor. Se anota entero porque el «inactivo/propenso a obesidad» es el **HUECO declarado** de `niveles_de_actividad.json` («Obese prone adults ≤ 90») y ahora tiene una segunda fuente que lo cifra: 1,0-1,2 × 70 = **70-84 kcal/kg^0,75**, coherente con el ≤ 90 de FEDIAF |
| *«Recent data suggest mean caloric intake for weight loss over a 12 wk period is»* 63 ± 10,2 kcal/kg^0,75 en el perro (el ± sale como un «6» al extraer el PDF, así que la cifra va fuera de las comillas) | **No se aplica**: el motor no formula dietas de adelgazamiento por kcal, recibe el DER de fuera. Se anota porque es la cifra medida contra la que se lee un plan de pérdida de peso, y el Cuadro 1 da 70 para lo mismo |
| Tabla 8, nefropatía con pérdida de proteínas: «25-50% protein reduction from current intake · Meet essential amino acid requirements» | **No se puede aplicar como está**: es una reducción **relativa a lo que el perro come hoy**, y el motor no sabe eso. Queda escrito porque `renal_proteinuria` hoy no lleva ninguna cifra, solo avisos, y esta es la única que hay en las fuentes leídas |
| Tabla 8, epilepsia idiopática: «High medium-chain triglycerides» | **No se aplica: no hay cifra**. AAHA no dice cuánto, y el motor no tiene clave de triglicéridos de cadena media. Es el mismo caso que los tres `documentado_sin_cifra` de `requisitos_condicionales.json`. A `PREGUNTAS_ABIERTAS.md` |
| Tabla 8, diabetes: «High soluble and insoluble fiber» y «High protein (unless contraindicated, e.g., proteinuria)» | **La fibra ya está** (suelo 17,5 en `diabetes`). **La proteína no, y no hay cifra**: «high» sin número no se puede escribir en el solver. A `PREGUNTAS_ABIERTAS.md` |
| *«For some large- and giant-breed dogs, skeletal maturity may not be achieved until closer to 15-16 mo»* | **No cambia nada, y va por el lado seguro**: la app termina el crecimiento a los 15 meses en un perro de 25 kg de adulto y a los 20-24 en los de 45-70 kg, o sea **más tarde** que AAHA. Requisitos de crecimiento durante más tiempo es el lado estricto |
| *«there are no specific nutritional requirements set by AAFCO for mature, senior, or geriatric pets»* y que no hay que cambiar de dieta por cumplir años | **No se aplica**: el motor sí distingue sénior, pero por la Tabla VII-6 de FEDIAF, que es energía y no requisitos. Coincide: nuestros 43 requisitos tampoco cambian por ser sénior |
| Riesgos de MCD asociada a dieta: *«Previously identified risk factors include lamb and rice diets, low-protein diets, and high-fiber diets»*, y «the most conservative approach is to avoid feeding grain-free diets or diets high in legumes» | **Lo de las legumbres ya está medido y contestado** en `dcm_asociada_a_dieta`. Lo del **cordero** es nuevo por esta puerta y refuerza la P-18, que está parada porque Spitze 2003 no está en el repo. Lo de «low-protein» y «high-fiber» entra en el conflicto de abajo |
| Todo el bloque de comunicación con el cliente, el equipo de la clínica, el microbioma y los pacientes hospitalizados (unas 700 líneas) | **No se aplica**: no hay ninguna cifra de ración. Se leyó entero y se dice que se leyó |

### El conflicto, que es el mismo de siempre y ahora tiene dos fuentes

La Tabla 8 dice, para las **tres** cardiopatías que lista —enfermedad valvular
degenerativa, miocardiopatía hipertrófica y miocardiopatía dilatada—:
«Controlled sodium / High EPA/DHA / **Avoid low protein**». Y en el texto, entre
los factores de riesgo de la miocardiopatía dilatada asociada a dieta,
«low-protein diets».

El motor, a un perro con `cardiopatia` **y** `renal` a la vez, le aplica el techo
de proteína de la renal: **62,5 g/1000 kcal**. Eso es exactamente «low protein».
Es la P-19, que salió leyendo el consenso ACVIM el mismo día, y ahora la dicen
**dos fuentes independientes**. No la resuelvo yo: cuál de las dos manda en un
perro que tiene las dos cosas es criterio clínico. Está en
`PREGUNTAS_ABIERTAS.md` con dueño.

---

## WSAVA — «Raw Meat Based Diets For Pets» · leído entero el 11-sep-2026

| Lo que dice | Decisión |
|---|---|
| *«Bones ... can result in broken teeth, intestinal or oesophageal obstruction, and constipation»* | **APLICADO**: va en la instrucción de «Hueso carnoso» |
| *«Feeding bones does not reduce the risk of plaque or tooth loss due to periodontitis»* | **APLICADO**: la creencia de que el hueso limpia los dientes es una razón por la que se da BARF, y la fuente dice que no. Aquí el hueso está por el calcio |
| Riesgo bacteriano, y que congelar no mata todas las bacterias | **Ya estaba** (aviso de higiene del 10-sep, de otra fuente) |
| *«Home prepared ... diets may have important nutrient deficiencies and excesses»*, y que en cachorros da problemas esqueléticos | **No se aplica**: es la razón de ser de este motor, no una cifra |
| *«High fat, low fiber diets (raw, but also cooked) may be well tolerated by many pets, but others will show gastrointestinal problems, such as diarrhoea, or even pancreatitis»* | **No se aplica**: el motor no puede saber qué perro. Ya hay plan de transición y topes de pancreatitis |
| *«It is important for the practitioner to know when their patients are fed raw»* | **No se aplica**: es para la consulta |

## WSAVA — «Guide to Treats for Dogs» · leído entero el 11-sep-2026

| Lo que dice | Decisión |
|---|---|
| *«Treats should always make up less than 10% of a dog's daily calorie intake»* | **Ya aplicado**. Es la **sexta** fuente con la misma cifra |
| Define «treat» incluyendo *«foods used to administer medication»* | **APLICADO**: la pregunta de los premios no lo decía. Y Fascetti cap.18 lo mide: el 57 % de los cardiópatas toman la pastilla escondida en comida rica en sodio |
| Lista de tóxicos: macadamia, **xilitol**, alcohol y masa de levadura cruda, cafeína | **APLICADO**: las cuatro faltaban en `TOXICOS_FEDIAF_7_7`. El xilitol lo señalan **dos** fuentes, y su puerta de entrada es un suplemento de fibra, categoría que el catálogo sí tiene |
| *«Treats should never replace a meal»* | **No se aplica**: no hay cifra |
| *«Excessively hard chews ... antlers and hooves ... should be avoided»* | **No se aplica**: no hay ninguno en el catálogo |
| La tabla de kcal de premios por peso | **No se usa**: la extracción del PDF sale corrupta (repite 32 y acaba en 146). Si hiciera falta, hay que releerla del PDF |

---

## Lo leído y NO aplicado, que sigue esperando decisión


Son **64**, y cada una dice por qué.


### Fascetti cap02

- **Recommended amounts of EPA plus DHA use MBW multiplied by factors ranging from 115 to 310 (Table 2.1).**

  

- **Disorder Dosage Idiopathic hyperlipidemia 120 mg/kg0.75 Kidney disease 140 mg/kg0.75 Cardiovascular disorders 115 mg/kg0.75 Osteoa**

  


### Fascetti cap03

- **The NRC uses the following equation to predict MER for kennel dogs or active pet dogs (NRC 2006): Equations using different multip**

  

- **Predicted energy requirements are approximately 2.5 times maintenance requirements at weaning and requirements decrease to approxi**

  

- **At this time, and until parturition, energy requirements will increase by 25% to over 60% depending on the size of the bitch (the**

  

- **Energy requirements during lactation in bitches may be calculated using the following equation (NRC 2006): where: kg BW = body wei**

  


### Fascetti cap04

- **The adequate intake for both sodium and potassium recommended by the NRC for exercising dogs is 1 g/Mcal.**

  

- **One recent study suggested that 1.2 g of sodium/Mcal may be ideal in sled dogs undergoing a 1600 km race (Ermon et al. 2014).**

  


### Fascetti cap07

- **Energy requirements for gestation peak anywhere between 30% and 60% of the pre‐breeding requirements depending upon the litter siz**

  DISCREPANCIA MEDIDA, y gana FEDIAF. «Energy requirements for gestation peak anywhere between 30% and 60% of the pre-breeding requirements.» El motor aplica la formula de FEDIAF (132 kcal/kg^0,75 + 26 kcal/kg de peso vivo desde la semana 5) y eso da +62 % en un perro de 10 kg, +73 % en uno de 25 y +79 % en uno de 40: POR ENCIMA del rango de Fascetti en los tres. Se apunta en FEDIAF_CONTRA_OTRAS_FUENTES.md con las dos cifras. || Y una segunda diferencia en el mismo parrafo: Fascetti dice que la necesidad no sube hasta el ULTIMO TERCIO y FEDIAF la sube desde la semana 5 de 9. Tambien gana FEDIAF, y va en el mismo sitio.

- **The recommendations from that study are that diets for lactation provide at least 10–20% of the energy from digestible carbohydrat**

  HALLAZGO QUE NO SE APLICA, y hay que preguntarlo. «The recommendations from that study are that diets for lactation provide at least 10-20% of the energy from digestible carbohydrates (Kienzle et al. 1985)», porque la lactosa de la leche sale mas alta con algo de hidrato. Una racion BARF lleva ~0 %. NO se aplica por tres razones escritas: (1) el propio parrafo dice que sin hidratos las camadas, los pesos al nacer y la supervivencia fueron COMPARABLES; (2) ni FEDIAF ni NRC ponen requisito de hidratos, y el cap. 8 de este mismo libro dice «Carbohydrates are not required in dogs and cats (NRC 2006)»; (3) el catalogo no tiene ni un cereal, asi que aplicarlo no seria apretar una racion sino cambi

- **The investigators of this study found that older dogs required up to 50% more protein than young dogs to maintain labile protein.**

  LA PROTEINA DEL SENIOR, leida entera y SIN CIFRA QUE APLICAR: el propio parrafo se frena en «neither of these studies provides definitive recommendations for protein requirements in older dogs». Medido sobre menus reales del motor: 105,1 / 95,7 / 101,9 g por 1000 kcal en senior de 8, 20 y 35 kg, o sea 122-134 % de los 78,2 que saldrian del «+50 %» del estudio. No hay riesgo y no hay nada que aplicar. Detalle en LECTURA_FASCETTI.md.

- **A more recent study examined 8‐year‐old pointers fed either 16.5% or 45% protein calories over a two‐year period (Kealy 1999).**

  LA PROTEINA DEL SENIOR, leida entera y SIN CIFRA QUE APLICAR: el propio parrafo se frena en «neither of these studies provides definitive recommendations for protein requirements in older dogs». Medido sobre menus reales del motor: 105,1 / 95,7 / 101,9 g por 1000 kcal en senior de 8, 20 y 35 kg, o sea 122-134 % de los 78,2 que saldrian del «+50 %» del estudio. No hay riesgo y no hay nada que aplicar. Detalle en LECTURA_FASCETTI.md.

- **Even the group consuming a higher percentage of their calories from protein lost 3.5% of their lean body mass.**

  LA PROTEINA DEL SENIOR, leida entera y SIN CIFRA QUE APLICAR: el propio parrafo se frena en «neither of these studies provides definitive recommendations for protein requirements in older dogs». Medido sobre menus reales del motor: 105,1 / 95,7 / 101,9 g por 1000 kcal en senior de 8, 20 y 35 kg, o sea 122-134 % de los 78,2 que saldrian del «+50 %» del estudio. No hay riesgo y no hay nada que aplicar. Detalle en LECTURA_FASCETTI.md.


### Fascetti cap08

- **Assessment while on a Home‐Prepared Diet It is recommended that any animal receiving a home‐prepared diet be checked by a veterina**

  HALLAZGO QUE NOS TOCA DE LLENO Y QUE LA APP NO DICE. «It is recommended that any animal receiving a home-prepared diet be checked by a veterinarian AT LEAST EVERY SIX MONTHS» (cada tres meses o menos si hay una enfermedad de por medio), con peso, condicion corporal y, si procede, analitica. Rawku formula dietas caseras y no dice esto en ninguna parte. || Y el mismo parrafo trae el nombre de un fallo que si podemos vigilar: el «DIET DRIFT», que el dueno vaya sustituyendo ingredientes por su cuenta. Va a PENDIENTE_PRODUCTO.md.


### Fascetti cap09

- **Each increment in BCS is approximately equivalent to 10–15% additional weight due to body fat.**

  EL ESCALON DEL BCS, y el motor esta en el extremo BAJO del rango. «Each increment in BCS is approximately equivalent to 10-15% additional weight due to body fat.» El motor aplica 10 % por punto (`der.BCS_PCT_POR_PUNTO`), que sale de la Tabla VII-2 de FEDIAF. Con 15 % el peso objetivo de un perro con BCS 7 saldria mas bajo y comeria menos; con el 10 % sale mas alto y come un poco mas, o sea que adelgaza mas despacio pero no se queda corto de nutrientes -- los minimos se escalan sobre ese mismo peso. Gana FEDIAF y la diferencia queda escrita con las dos cifras.

- **A score of 4–5 is considered optimal for dogs and reflects a body fat level of 15–20%.**

  «A score of 4-5 is considered optimal for DOGS.» El motor ancla el ideal en BCS 5 (`BCS_NEUTRO`), que es lo que dice la Tabla VII-2 de FEDIAF («% BW below or above BCS 5»). Si el ideal fuera 4, un perro en 5 ya estaria ligeramente por encima y su peso objetivo bajaria un 10 %. Gana FEDIAF; apuntado con las dos cifras.


### Fascetti cap10

- **A large‐breed food for growing dogs with a level of 0.8% calcium (per 4200 ME kcal/kg) has been both calculated and proven to be s**

  EL AUTOR PIDE MENOS CALCIO DEL QUE APLICAMOS, y no se puede aplicar. «A large-breed food for growing dogs with a level of 0.8% calcium (per 4200 ME kcal/kg) has been both calculated and PROVEN to be safe for raising large- and giant-breed pups throughout the growth period (Nap et al. 2000).» 0,8 % por 4200 kcal/kg = 1905 mg/1000 kcal. El motor aplica 2750. Pero el MINIMO de FEDIAF para el cachorro de raza grande en late growth son 2500 (fila `Calcio_LateGrowth_RazaGrande`), asi que 1905 deja al cachorro POR DEBAJO del minimo: gana FEDIAF y la cifra queda escrita. Va a FEDIAF_CONTRA_OTRAS_FUENTES.md como conflicto de los que sacan al perro FUERA de la ventana.

- **As a result, the available diets for companion animals can have a vitamin D content exceeding recommended levels (Table 10.7) (Wei**

  «As a result, the available diets for companion animals can have a vitamin D content EXCEEDING RECOMMENDED LEVELS (Table 10.7).» Es el aviso que acompana a la cifra de `cifra#530`, y en nuestro catalogo el mecanismo es el mismo: la vitamina D de una racion BARF entra por los multivitaminicos y por el aceite de higado de bacalao, que es justo donde se concentra.

- **In general, in foods with a protein content of high biological value, the calcium content should be between 0.8% and 1.0% on a dry**

  La misma discrepancia dicha como rango: «In general, in foods with a protein content of high biological value, the calcium content should be between 0.8% and 1.0% on a dry matter basis (for a food with 4200 ME kcal/kg diet) (Nap et al. 2000).» = 1905 a 2381 mg/1000 kcal. El motor aplica 2750 y el minimo de FEDIAF son 2500: el rango ENTERO queda por debajo del minimo de FEDIAF. Gana FEDIAF. Y ojo al matiz, que es nuestro caso: «a protein content of HIGH BIOLOGICAL VALUE» -- una racion BARF lo es.

- **Taken together, the author recommends the following: restricted feeding of a puppy food with a calcium and vitamin D content not t**

  LA RECOMENDACION FINAL DEL AUTOR, con dos cifras: «restricted feeding of a puppy food with a calcium and vitamin D content not to exceed the percentages demonstrated in controlled studies to result in skeletal problems (i.e. calcium ∼1.0% dm, vitamin D content 12.5–25 μg/kg diet)». El calcio es la discrepancia de arriba. La vitamina D es NUEVA: 12,5-25 ug/kg MS = 500-1000 UI/kg, o sea 3,125 a 6,25 ug/1000 kcal a 4000 kcal/kg. El motor no tiene techo de vitamina D en crecimiento mas alla del maximo LEGAL de FEDIAF (14,19) y del tope cronico por peso metabolico. MEDIDO el 11-sep-2026 sobre los 12 menus de cachorro del catalogo: van de 3,14 a 8,96 ug/1000 kcal, mediana 6,07, y SEIS DE LOS DOCE pasan de 6,25. Cabe dentro de la ventana de FEDIAF, asi que se PUEDE aplicar -- y p

- **In 36 dogs with elbow OA due to ED, a double‐blind efficacy study was performed by feeding an increased omega‐3 content (omega‐3 o**

  SEGUNDA FUENTE para el omega-3 de la artrosis, que el motor tiene ESCRITO Y SIN APLICAR. Estudio doble ciego en 36 perros con artrosis de codo: omega-3 al 4 % y omega-6 al 20 % frente a omega-3 al 0,8 % y omega-6 al 38 %. Subio el LTB5 en plasma y la cojera medida por plataforma de fuerzas NO cambio. O sea que esta fuente sostiene el mecanismo y NO demuestra el efecto clinico, que es precisamente el motivo por el que el omega-3 de la artrosis vive en `limites_escritos_que_el_solver_no_aplica`.

- **A clinical trial including force‐plate analysis performed in two groups of dogs fed either a control food or an EPA‐supplemented d**

  Y el estudio que SI ve efecto: con dieta suplementada con EPA durante 90 dias mejoro el apoyo del peso el 82 % de los perros frente al 31 % de los controles (Schoenherr 2005). Va con el de arriba: las dos medidas juntas son lo que hay que ponerle delante a quien decida si se enciende el omega-3 de la artrosis. No se aplica hoy.


### Fascetti cap11

- **An empirical recommendation is to select diets that contain less than 8% total dietary fiber or less than 5% crude fiber.**

  UN TECHO DE FIBRA QUE EL MOTOR NO TIENE. «An empirical recommendation is to select diets that contain LESS THAN 8% TOTAL DIETARY FIBER or less than 5% crude fiber» en enteropatia cronica. 8 % MS a 4000 kcal/kg = 20 g/1000 kcal. FEDIAF no pone requisito de fibra -- y ojo, que en agosto se colo aqui una fila «Fibra» inventada --, asi que esto solo podria vivir como tope de la patologia `enteropatia_cronica`. MEDIDO sobre los 36 menus del catalogo: mediana 1,2 g/1000 kcal, pero OCHO de los 36 pasan de 20 (hasta 31,1), o sea que el tope SI haria algo. No se aplica en esta pasada: su propia fuente lo llama «empirical recommendation» y la tabla de SACN5 que ya usa esa patologia manda. Se escribe y

- **Although it appears that a “natural” diet protects against, or at least minimizes, the development of calculus, it does little to**

  LO QUE UNA DIETA CRUDA NO HACE, dicho por esta fuente: «Although it appears that a “natural” diet protects against, or at least minimizes, the development of calculus, it does little to protect against the development of periodontitis and tooth loss, in either cats or dogs». Es de los pocos sitios donde el libro habla de la dieta cruda y del sarro. No cambia ninguna cifra del motor, y queda escrito porque la app no promete nada dental y esta fuente marca hasta donde llega.

- **Dietary fat restriction is particularly important in patients diagnosed with lymphangiectasia, with many patients needing restrict**

  ⚠️ EL MISMO «15 %» QUE APLICA EL MOTOR, PERO EN OTRA UNIDAD, Y NO CABE. Fascetti: «Dietary fat restriction is particularly important in patients diagnosed with lymphangiectasia, with many patients needing restriction to less than 15% FAT kJ or kcal» -- el 15 % de la ENERGIA, o sea <=16,7 g/1000 kcal. El motor aplica 37,5 g/1000 kcal a `ple_linfangiectasia`, que sale de la Tabla 58-1 de SACN5, donde el mismo 15 % es de MATERIA SECA. Dos fuentes, el mismo numero, dos unidades, y un factor de 2,2 entre las dos. MEDIDO el 11-sep-2026 preguntandole al solver con 40 s en perros de 10, 20 y 35 kg: con 37,5 sale menu en los tres; con 20,0 y con 16,7 NO SALE EN NINGUNO. Asi que la cifra de Fascetti n

- **Unfortunately, there are few commercial veterinary diets available that contain less than 15% fat kJ or kcal.**

  La otra mitad de la misma frase: «there are FEW COMMERCIAL VETERINARY DIETS available that contain less than 15% fat kJ or kcal». O sea que la propia fuente dice que casi ningun producto del mercado llega a esa cifra. Va con `cifra#700`.


### Fascetti cap12

- **For most of the population eating commercial diets, a diet that has less than 20% fat on an ME basis will be considered low fat, b**

  EL UMBRAL DE «BAJA EN GRASA» DE ESTA FUENTE, en la unidad que importa: «a diet that has LESS THAN 20% FAT ON AN ME BASIS will be considered low fat». 20 % de las kcal = 22,2 g/1000 kcal. El motor aplica a la pancreatitis 37,5 g/1000 kcal (y 25,0 si ademas hay obesidad o hiperlipidemia), que salen de la Tabla 67-3 de SACN5 en % de MATERIA SECA. Es la MISMA confusion de unidades que el 15 % de la linfangiectasia del cap. 11, y otra vez la lectura en kcal es mas estricta. MEDIDO el 11-sep-2026 con el solver y 40 s en 10, 20 y 35 kg: con 20,0 g/1000 kcal no sale menu en ninguno. Se escribe con su medida.


### Fascetti cap13

- **These formulations differ from those prescribed for patients with renal disease in that the hepatic formulas are generally less pr**

  LAS DIETAS HEPATICAS DEL MERCADO VAN POR DEBAJO DEL MINIMO DE FEDIAF. «The hepatic formulas are generally less protein restricted (14-15.5% PROTEIN ON AN ME BASIS) than most renal diets»: 14-15,5 % de las kcal = 35 a 38,75 g/1000 kcal, y el minimo de FEDIAF para el adulto son 52,1. El motor NO PUEDE bajar ahi y no lo hace: formular por debajo de FEDIAF es la fase 4 de `VETERINARIOS.md`, que exige una prescripcion declarada que viaje con el menu, y todavia no existe. Queda escrito con las dos cifras. || Y el resto de la frase describe lo que el motor SI aplica ya a la hepatopatia por cobre: cobre restringido (2,4), cinc alto (suelo 50), sodio controlado (625) y antioxidantes (vitamina E 67,1)


### Fascetti cap14

- **A ratio of 2.6 : 26 of LA : ALA (2.6 : 16 in gestation/lactation) is considered safe in dogs, along with a safe upper limit for LA**

  ⚠️ LA FRASE CON TRES CIFRAS, Y LA QUE DIO NOMBRE AL BLOQUE 96. «A ratio of 2.6 : 26 of LA : ALA (2.6 : 16 in gestation/lactation) is considered safe in dogs, along with a safe upper limit for LA and EPA + DHA of 16.3 and 2.8 g/1000 kcal, respectively (NRC 2006)». APLICADAS DOS: el ratio linoleico:linolénico vive en `requisitos_condicionales.json` y el techo de linoleico de 16,3 en `recomendaciones_libro.json` (medido: no aprieta nunca, los 216 menús van de 3,20 a 10,50). SIN APLICAR LA TERCERA: el techo de EPA+DHA de 2,8, que es la única que SÍ aprieta -- medido, 5 de los 216 menús se pasan y llegan a 3,00, y FEDIAF no pone máximo de EPA+DHA en ninguna etapa, así que el semáforo no puede ver

- **In dogs, a tentative upper limit of 75 IU/kg/day (or 1000–2000 IU/kg diet) has been suggested (NRC 2006).**

  ⚠️ EL TECHO DE VITAMINA E DEL PERRO, Y NO LO TENÍAMOS. «In dogs, a tentative upper limit of 75 IU/kg/day (or 1000-2000 IU/kg diet) has been suggested (NRC 2006)». La segunda forma SÍ es una concentración de la dieta y el motor la sabe usar: 1000 UI/kg MS a 4000 kcal/kg MS son 250 UI/1000 kcal, y a 0,671 mg/UI (FEDIAF Tabla VII-14) salen 167,75 mg/1000 kcal en el extremo estricto (335,5 en el laxo). || FEDIAF NO PONE MÁXIMO DE VITAMINA E EN NINGUNA ETAPA -- las tres columnas están vacías --, así que sería el único techo que tendría. || MEDIDO el 11-sep sobre los 216 menús del catálogo: van de 10,05 a 89,28 mg/1000 kcal con mediana 26,86, o sea CERO por encima del techo estricto. No aprieta ho


### Fascetti cap15

- **The minimal dietary protein requirements of cats and dogs with CKD are not known, but have been presumed to be similar to the mini**

  ⚠️ EL MÍNIMO DE PROTEÍNA DEL NRC, Y ESTÁ A 2,6 VECES DEL DE FEDIAF. Literal: «The minimal dietary protein requirements of cats and dogs with CKD are not known, but have been presumed to be similar to the minimal protein requirements of healthy animals: for cats, 3.97 g/kg BW0.67 or 40 g/Mcal; and for dogs, 2.62 g/kg BW0.75 or 20 g/Mcal (NRC 2006)». || Son 20 g/1000 kcal para el perro. El mínimo de FEDIAF en adulto son 52,1. || IMPORTA PORQUE ES EXACTAMENTE EL NÚMERO QUE BLOQUEA EL IRIS 4: la revisión de Cris Carles pide bajar al 15 % de materia seca (37,5 g/1000 kcal), que está POR DEBAJO de los 52,1 de FEDIAF y POR ENCIMA de los 20 del NRC. || GANA FEDIAF, que es la regla del repo, y además

- **In healthy cats and dogs, dietary sodium intake up to 3.1 g/Mcal in cats and 4.1 g/Mcal in dogs does not affect blood pressure or**

  ⚠️ EL SODIO DEL RENAL NO TIENE EVIDENCIA, Y EL MOTOR LO RESTRINGE. Literal del capítulo: «there is currently no evidence to suggest that lowering dietary sodium will reduce blood pressure in cats or dogs with CKD», y en perro sano «dietary sodium intake up to ... 4.1 g/Mcal in dogs does not affect blood pressure or renal or cardiac functions». El motor aplica al `renal` un techo de sodio de 750 mg/1000 kcal, o sea 0,75 g/Mcal -- cinco veces por debajo de lo que esta fuente dice que ya es inocuo. || NO SE QUITA, y por dos motivos escritos: la propia fuente sigue diciendo en el mismo párrafo que «moderately sodium‐restricted therapeutic diets for the nutritional management of renal disease remain common and recommended»

- **Stage I Stage II Stage III Stage IV Hydration Fresh water at all times Protein modification Dogs: UPC >2 Cats: UPC >0.4 Dogs: UPC**

  ⚠️ LA TABLA 15.2, QUE ES LA QUE PEDÍA CRIS POR ESTADIOS -- Y NO DA NÚMEROS DE PROTEÍNA. La fila «Protein modification» dice, para perro, «UPC >2» en estadio I y «UPC >0.5» en estadio II; en III y IV dice «Appropriate dietary protein reduction to control uremia and hyperphosphatemia», sin cifra. || O sea que el estadiaje que esta fuente da NO es un tope de proteína por estadio: es un CRITERIO ANALÍTICO para decidir cuándo tocarla, y el dato es el UPC. || Y el motor ya lo tiene: `renal_proteinuria` se llama literalmente «Proteinuria renal (UPC > 0,5)», que es el umbral del estadio II de esta tabla. Esa patología NO APLICA NINGUNA CIFRA a propósito, y su aviso explica por qué: el consenso ACVIM


### Fascetti cap16

- **Diets formulated for oxalate prevention in cats and dogs contain phosphorus from 0.3 to 2.1 g/Mcal.**

  ⚠️ EL FÓSFORO DEL OXALATO, Y VA EN DIRECCIÓN CONTRARIA A LO QUE APLICA EL MOTOR. Literal: «Dietary phosphorus should not be restricted with calcium oxalate urolithiasis. Low dietary phosphorus is a risk factor for calcium oxalate urolith formation in cats and dogs». Y da rango: «Diets formulated for oxalate prevention in cats and dogs contain phosphorus from 0.3 to 2.1 g/Mcal. Concentrations from approximately 1.5 to 2.0 g/Mcal have been recommended». || El motor aplica al `oxalato` un TECHO de 1500 mg/1000 kcal (SACN5 Tabla 40-5), o sea 1,5 g/Mcal: justo el extremo BAJO de lo que Fascetti recomienda, y sin ningún suelo debajo -- el mínimo de FEDIAF son 1160, así que sobre el papel el motor 

- **It should be noted that getting exact purine concentration data for some commercial foods can be challenging, and often foods must**

  ⚠️ EL DATO DE PURINAS ES DIFÍCIL DE CONSEGUIR, Y AQUÍ TAMBIÉN. «getting exact purine concentration data for some commercial foods can be challenging, and often foods must be selected based on total dietary protein and the protein-rich food sources (e.g. plant- and egg-based proteins) used as indicators». El catálogo SÍ trae `purinas_bases` y `purinas_fuente` en cada ficha, así que aquí vamos por delante de lo que describe el libro. Se anota porque justifica ese campo y porque dice qué hacer cuando falta: usar la proteína total y el origen de la proteína como indicador.


### Fascetti cap17

- **Most recommendations in the literature suggest feeding a diet that provides 20% of the calories or less from fat on a metabolizabl**

  ⚠️ EL TECHO DE GRASA DE LA HIPERLIPIDEMIA, Y FASCETTI ES MÁS ESTRICTO QUE EL MOTOR. Literal: «Most recommendations in the literature suggest feeding a diet that provides 20% of the calories or less from fat on a metabolizable energy (ME) basis». || 20 % de las kcal, a 9 kcal/g de grasa, son 22,2 g/1000 kcal. El motor aplica a la `hiperlipidemia` un techo de 30 (SACN5 Tabla 28-2), o sea un 27 % de las kcal. || ⚠️ Y HAY UNA CIFRA EN LA MISMA UNIDAD DEL MOTOR QUE VA AL REVÉS, en la línea 247: «Dogs were fed low- or moderate-fat diets (24 or 33 g/1000 kcal, respectively), and cholesterol and triglycerides were satisfactorily controlled in BOTH groups» -- con aceite de pescado. O sea que 33 funci

- **However, in many patients more severe restriction is often indicated, sometimes as low as 10% fat ME or less.**

  La otra mitad de la misma frase: «in many patients more severe restriction is often indicated, sometimes as low as 10% fat ME or less», o sea 11,1 g/1000 kcal. Eso está POR DEBAJO del mínimo de grasa de FEDIAF en adulto (13,75), así que el motor no puede llegar ahí ni con un objetivo del profesional: es la vía firmada de VETERINARIOS.md, la misma frontera que el IRIS 4. Medido el 11-sep en pancreatitis: 20 g/1000 kcal sí sale, 17,5 ya no.

- **Dogs were fed low‐ or moderate‐fat diets (24 or 33 g/1000 kcal, respectively), and cholesterol and triglycerides were satisfactori**

  Ver la línea 232: es la cifra del mismo hallazgo, «24 or 33 g/1000 kcal», en la unidad del motor.


### Fascetti cap18

- **Mild sodium restriction (<100 mg/100 kcal) is recommended, although further research is needed to determine the optimal dose and t**

  ⚠️ EL SUELO QUE NO TENEMOS: HAY UN PUNTO EN EL QUE BAJAR EL SODIO ES MALO. Literal, del apartado felino: «Mild sodium restriction (<100 mg/100 kcal) is recommended», y en la frase siguiente «Severe sodium restriction (<50 mg/100 kcal) is not recommended as this can cause early and prolonged activation of the renin-angiotensin-aldosterone (RAA) system». || Esos 50 mg/100 kcal son 500 mg/1000 kcal, y el motor aplica al estadio ACVIM D un techo de 480 -- por DEBAJO de esa línea. || ⚠️ PERO ES EL PÁRRAFO DEL GATO, y el del perro dice otra cosa: «one study showed that a low-sodium diet (40 mg/100 kcal) reduced cardiac size in dogs with CHF compared to a diet containing 70 mg/100 kcal», o sea que 

- **Severe sodium restriction (<50 mg/100 kcal) is not recommended as this can cause early and prolonged activation of the renin‐angio**

  Es la segunda mitad de la frase de la línea 33, la del <50 mg/100 kcal. Mismo veredicto.

- **Therefore, animals with cardiac disease (at least those receiving diuretics) may have higher dietary B vitamin requirements.**

  ⚠️ «animals with cardiac disease (at least those receiving diuretics) may have higher dietary B vitamin requirements». Es un requisito CONDICIONAL -- sube con el fármaco, no con la dieta -- y la fuente NO da cifra, así que aplicarlo sería inventársela. Es la misma forma que las tres `documentado_sin_cifra` de `requisitos_condicionales.json`. || Y hay un dato del motor que lo tranquiliza: medido, la B6 real de los menús va de tres a doce veces el mínimo de FEDIAF, y una ración BARF con vísceras va sobrada de grupo B. Se apunta por si algún día aparece la cifra.

- **In dogs with ACVIM Stage C, the authors recommend moderate sodium restriction (i.e. <80 mg/100 kcal).**

  ⚠️ LA CIFRA CANINA DEL ESTADIO C, Y EL MOTOR ES MÁS ESTRICTO. «In dogs with ACVIM Stage C, the authors recommend moderate sodium restriction (i.e. <80 mg/100 kcal)», o sea <800 mg/1000 kcal. El motor aplica 625 al `cardiopatia_c`. || No es conflicto: 625 cabe dentro de 800 y los topes solo aprietan. Se apunta porque es la segunda fuente canina que da número para ese estadio, y las dos cifras -- 800 y 625 -- convendría que las viera quien firma.


### SACN5 tabla 14-3

- **Comparison of recommended levels of key nutritional factors for foods for mature adult dogs with levels in selected**

  LEIDA 10-sep-2026. Es una comparativa: una fila «Recommended levels» y debajo la composicion de piensos comerciales para perro maduro. Lo aplicable no esta en la tabla sino en el parrafo que la introduce (cap.14): «foods for mature dogs should contain at least 400 IU vitamin E/kg (DM) (Jewell et al, 2000), at least 100 mg vitamin C/kg (DM) and 0.5 to 1.3 mg selenium/kg (DM)». Ver HALLAZGOS_SACN5_10SEP.md: las tres estan medidas y NINGUNA se aplica todavia.


### SACN5 tabla 18-10

- **Effect of nutrient profile on stamina.***

  Efecto del perfil de nutrientes sobre la resistencia en el PERRO: pasando la grasa de 12,8 a 33,1 % de materia seca el tiempo de carrera sube de 103,7 a 137,6 minutos. Es la cara opuesta del techo de grasa, y toca al perro de trabajo.


### SACN5 tabla 18-6

- **) and a distance of 167 km. Assuming all dogs pull equally, the weight pulled by this dog is 15 kg (total sled weight**

  Coste calorico de correr 1 km segun el peso: 1,77 kcal/kg en un perro de 5 kg y 0,76 en uno de 70. La ficha pregunta por la actividad en escalones y no por la distancia; esta tabla la cuantifica.


### SACN5 tabla 19-4

- **). This lack of adaptability has been noted in other al, 1993, 2001; Gruffydd-Jones et al, 1998). Interestingly, the**

  Composicion del cuerpo entero de la rata, que es la referencia de PRESA ENTERA: 5,7 kcal/g de EM, calcio 1,15 % y fosforo 0,98 % (Ca:P de 1,17), linoleico 9,1 %. Es el patron natural contra el que se puede leer una racion BARF, y el repo no lo tiene escrito.


### SACN5 tabla 19-5

- **Comparison of dietary protein requirements during**

  Proteina de crecimiento frente a mantenimiento en el PERRO, con dos lecturas de la misma fuente: 12 % / 4 % y 18 % / 8 % de materia seca. El motor aplica los minimos de FEDIAF, que son mas altos; queda como contraste para la pregunta de la proteina del senior.


### SACN5 tabla 19-6

- **Comparison of minimal protein and amino acid**

  Proteina y aminoacidos MINIMOS de crecimiento del CACHORRO en % de materia seca: proteina 17,5 · arginina 0,66 · histidina 0,25 · isoleucina 0,50 · leucina 0,82 · lisina 0,70. Comparable celda a celda con la Tabla III-3b de FEDIAF, y nadie lo ha cruzado.


### SACN5 tabla 27-12

- **) but requires a few simple Although the lean body mass of an overweight patient is**

  Metodo del PESO IDEAL para fijar las kcal de adelgazamiento, que es el que usa el motor (las kcal se calculan sobre `peso_objetivo_kg`). Queda escrito para que la eleccion entre los cuatro metodos de este capitulo sea una decision y no un accidente.


### SACN5 tabla 27-13

- **Two alternative methods for estimating resting Table 27-15. Using obese body weight and desired rate of**

  Los numeros del adelgazamiento: el RER tiene que ser el 70-80 % del DER al peso optimo, o el 60-70 % al peso obeso, para perder 1-2 % de peso a la semana. El motor baja las kcal al peso objetivo y no comprueba que caigan en esa ventana.


### SACN5 tabla 29-4

- **Effect of feeding insoluble dietary fiber to dogs and cats with diabetes mellitus.***

  Fibra insoluble en el PERRO diabetico, con cifras: pasando de 1 % a 12 % de fibra de materia seca la glucosa media en sangre baja y la dosis de insulina tambien. Es la unica cifra canina de fibra con resultado medido, y cae justo dentro de la pregunta abierta de que fibra mide el catalogo.


### SACN5 tabla 33-3

- **and ed by the parathyroid gland and the C-cells of the thyroid**

  Composicion del hueso, y trae el numero que el motor necesitaba tener escrito: el calcio y el fosforo de la hidroxiapatita van en un ratio Ca:P de 2,15:1 EN PESO (1,67:1 molar). O sea que una racion con mucho hueso tira el Ca:P hacia arriba por quimica, no por casualidad, y el rango 1,0-2,0 de FEDIAF se come por arriba con el hueso.


### SACN5 tabla 33-6

- **Recommended levels of key nutrients for dogs at risk for developmental orthopedic disease compared to levels in selected**

  LEIDA 10-sep-2026, Y TRAE DOS COSAS. Su fila «Recommended levels» para el cachorro en riesgo de enfermedad ortopedica del desarrollo dice: densidad 3,2-4,1 kcal/g MS · GRASA 8,5-17 % MS · DHA >=0,02 % · calcio 0,8-1,2 % · Ca:P 1,1:1-2:1 con la nota «the lower end of the range is preferred». (1) El techo de GRASA (17 % MS = 42,5 g/1000 kcal) el motor no lo aplica. (2) El Ca:P 1,1-2,0 es el CUARTO sitio de SACN5 donde aparece ese mismo rango, y aqui en CRECIMIENTO: el motor aplica el 1,0-1,6 de FEDIAF para raza grande, o sea que el suelo de la fuente (1,1) es mas estricto. Ver HALLAZGOS_SACN5_10SEP.md.


### SACN5 tabla 33-8

- **) (NRC, 2006). Great Dane puppies are the exception to the previous recom-**

  LEIDA 10-sep-2026. «A method for estimating daily energy requirement (DER) for growth of puppies after weaning», adaptada de NRC 2006. Da el DER del cachorro por FRACCION DEL PESO ADULTO, con siete escalones: 15 % -> x2,5 · 30 % -> x2,1 · 43 % -> x1,9 · 60 % -> x1,6 · 71 % -> x1,4 · 80 % -> x1,3 · 100 % -> x1,0, sobre MER = 130 x BW^0,75. Trae ejemplo trabajado. || HALLAZGO: el motor usa la curva de KLEIN 2019 que publica FEDIAF (Tabla VII-8b), y las dos fuentes NO dan lo mismo: medido, el motor queda entre un 14 % y un 28 % POR DEBAJO de esta tabla, y la diferencia es mayor cuanto mas joven el cachorro. No es un fallo -- FEDIAF manda -- pero es una discrepancia de fuentes de hasta el 28 % e


### SACN5 tabla 34-3

- **Nutrient comparison of control and test foods.***

  El alimento de prueba de la artrosis, con su ratio omega-6:omega-3 de 0,7 frente al 22,8 del control, y omega-3 totales del 3,48 % de materia seca. El repo dice que al ratio omega-6:omega-3 «le falta el numero» (PREGUNTA 40): aqui hay uno, publicado y canino.


### SACN5 tabla 36-10

- **Taurine concentrations (mg/kg dry matter)**

  Taurina de las fuentes naturales en mg/kg de materia seca: musculo de vaca 1.200, de cordero 1.600, de pollo 1.100, bacalao 1.000, raton entero 7.000. El catalogo no tiene el dato de taurina en ninguna de sus 163 fichas, y la taurina es la cifra que decide en la cardiomiopatia dilatada.


### SACN5 tabla 36-9

- **Daily sodium intake for a dog and a cat**

  Ingesta diaria de sodio de un perro de 15 kg que come 935 kcal, alimento por alimento: el cardiaco seco da 159 mg/dia, que son 170 mg/1000 kcal. El motor aplica 739 mg/1000 kcal en la cardiopatia B2, cuatro veces mas. Hay que cruzarlo con la Tabla 36-6 y con el techo legal del Reglamento (UE) 2020/354.


### SACN5 tabla 5-13

- **Small intestinal and total tract crude protein and small intestinal amino acid digestibility of dog foods containing animal protein sources.***

  Digestibilidad de la proteina y de los aminoacidos de alimentos CANINOS con proteina animal. «Beef and bone meal» da 68,3 % de digestibilidad ileal de proteina frente a 80,4 % de «Beef, fresh». Toca de lleno la pregunta abierta del HUESO: el motor cuenta la proteina del hueso como si se digiriera igual que la de la carne.


### SACN5 tabla 5-16

- **Ideal amino acid profiles (relative to lysine) for size each protein must be present. The amino acid in shortest**

  Perfil ideal de aminoacidos relativo a la lisina, con columna de PERRO: metionina+cistina 0,64 · triptofano 0,22 · treonina 0,67 · arginina 0,71 · leucina 1,00 · fenilalanina+tirosina 1,00. El motor exige cada aminoacido por separado contra FEDIAF y no mira el perfil. Es la otra forma de la pregunta del techo de lisina.


### SACN5 tabla 5-21

- **shows the fatty acid compositions of different fat 6 family in fish and shellfish, whereas polyunsaturated fatty**

  Composicion de acidos grasos de las grasas y aceites comerciales, g/100 g: el aceite de pescado da 14,1 de EPA y 11,9 de DHA, el de girasol 62,3 de linoleico y el de soja 7,3 de linolenico. Es dato de contraste para las fichas de aceite del catalogo, que es donde vive `dato_dudoso`.


### SACN5 tabla 5-8

- **). It is not clear what factors in fiber are responsible determine total fiber and is commonly used for measuring**

  Disponibilidad del zinc, el calcio, el hierro y el fosforo segun la FUENTE de fibra, al 5 % de fibra dietetica total. Con pulpa de remolacha el zinc baja al 24 % y el calcio al 44 %. El motor no modela disponibilidad: suma el nutriente de la ficha. Los ingredientes de la tabla son de pienso y no del catalogo, pero el mecanismo es el mismo y se suma a la pregunta abierta de la fibra.


### SACN5 tabla 58-2

- **). MCT are water-soluble, ticularly low fat content (Tams and Twedt, 1981; Erickson,**

  Triglicéridos de cadena media frente a los de cadena larga: los de cadena media se hidrolizan mas rapido y no necesitan quilomicrones. Es el mecanismo detras del techo de grasa de la linfangiectasia, que el motor aplica sin distinguir el tipo de grasa.


### SACN5 tabla 6-5

- **lists normal plasma levels of pantothenic acid in foods and foodstuffs. Thus, hydrolytic**

  Las nueve vitaminas del grupo B con la asignacion de AAFCO y la de NRC PARA EL PERRO, su nivel en sangre normal y la prueba con que se mide. Colina 1.700 mg/kg MS (NRC), que a 4,0 kcal/g son 425 mg/1000 kcal: la misma cifra baja que ya salio de NRC 2006 cap.8 y que los 36 menus del catalogo superan. Y da el nivel en sangre, que es lo que falta para poder contestar la pregunta de las formas quimicas del grupo B.


### SACN5 tabla 8-1

- **) (Kallfelz and Dzanis, 1989). In dogs, aver- tive, less costly and safer approach is to simply exchange the**

  Ingesta diaria REAL de calcio, fosforo, vitamina A y vitamina D de un perro adulto con pienso seco tipico frente a su minimo: calcio 74 mg/kg/dia contra un minimo de 25, fosforo 54 contra 19, vitamina D 11 UI contra 2,3. Casi tres veces el minimo, cuatro en la D. Es la medida de por que existen los techos del libro para el perro sano.
