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
fósforo ✅ · **Ca:P 1,1-2:1 ✅** *(aplicado el 10-sep)* · sodio ✅ · magnesio ✅ ·
evitar vitamina C ❌ ·
pH urinario 7,1-7,5 ➖

### 41-6 · Fosfato cálcico
Agua ➖ · proteína ✅ · calcio 0,4-0,7 % ➖ *(mismo criterio que el oxalato)* ·
fósforo ✅ · **Ca:P 1,1-2:1 ✅** *(aplicado el 10-sep)* · sodio ✅ · magnesio ✅ ·
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

## Resumen (de la TERCERA pasada — ver más abajo la cuarta)

> ⚠️ **Esta lista de ocho puntos ya no es lo que queda: es lo que quedaba el
> 8 de septiembre por la mañana.** Los puntos 2, 3, 4, 5 y 8 se aplicaron ese
> mismo día (commit «Aplicar la tercera pasada»), el 5 con la vitamina E
> corregida de 100 a 67,1 mg porque la tabla la da en UI. Siguen abiertos el
> 1 (nivel de obesidad), el 6 (exclusiones de la flatulencia) y el 7
> (cloruro = 1,5 × sodio). Se deja escrita tal cual porque es el registro de
> lo que encontró la tercera pasada, no un índice de pendientes.

**Ninguna cifra aplicada está mal.** Lo que había era **incompleto**, y en dos
casos —la pancreatitis y la obesidad— **incoherente**: tablas que gradúan de las
que tomábamos una fila suelta.

Lo que falta, por lo que pesa:

1. **Coherencia de nivel en obesidad** (¿adelgazar o mantener?). Es una decisión
   de producto: la app sabe si el objetivo es bajar peso.
2. **Omega-3 total en artrosis y en disfunción cognitiva** (8,75 y 2,5 g). Dos
   fuentes independientes lo piden en artrosis. Necesita clave nueva en el `MAPA`.
3. ~~**Ca:P 1,1-2:1 en los dos urolitos de calcio.** El motor ya sabe de ratios.~~
   ✅ **APLICADO EL 10 DE SEPTIEMBRE.** Lo que faltaba no era saber de ratios: era
   que una **patología** pudiera pedir el suyo. Ahora hay un bloque `ratios` en
   `patologias.json` que admite cualquier par de nutrientes, y lo aplican el
   solver y `_tope_patologia_roto` llamando a la misma función. **Y no era
   cosmético**: medido antes de aplicarlo, el perro de 30 kg con oxalato salía con
   Ca:P **1,06** y salía **en verde**, porque el semáforo mide contra el 1,0-2,0
   de FEDIAF, que es el rango de un perro sano. BLOQUE 75.
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

---

# CUARTA PASADA · el barrido estaba cortado (8 de septiembre)

## Lo que pasó

Este documento decía «las 21 tablas, una por una». Eran las 21 tablas **que yo
había visto**, y no son las que hay.

El barrido original se hizo así:

```bash
grep -h "Key nutritional factors" *.txt | sed -n '20,60p'
```

Ese `sed` está ahí para que la salida cupiera en pantalla. Recorta a 40 líneas.
**Hay 89 tablas «Key nutritional factors» en SACN5**, así que casi la mitad no
llegó a leerse nunca, y el documento afirmaba una cobertura que no tenía.

No se descubrió revisando: se descubrió por casualidad, leyendo el capítulo 30
entero para buscar otra cosa y encontrando en él una tabla con cinco cifras que
aquí no estaba. El barrido se ha repetido sin cortar:

```bash
grep -ho "Table [0-9]\+-[0-9]\+\. *Key nutritional factors[^.]*" *.txt | sort -u | wc -l
# 89
```

**La lección no es «leer mejor»: es que un barrido cuyo resultado no se compara
contra el total no es un barrido, es una muestra.**

## Las 89, clasificadas

De las 89, la mayoría no son recomendaciones:

| Cuántas | Qué son | Qué se hace |
|---|---|---|
| 34 | «…in selected commercial veterinary therapeutic foods» | Comparativas de piensos comerciales, no recomendaciones. No aplican |
| 13 | Gatos (20-3, 21-2, 22-1, 24-1, 27-6, 29-12, 46-12, 46-13, y las columnas felinas) | No es esta especie |
| 8 | Etapas de vida del perro SANO (13-3, 14-2, 15-5, 16-4, 17-1, 18-9, 25-5, 33-5) | Aquí manda FEDIAF, no un libro de texto. Ver más abajo |
| 21 | Patologías caninas **que ya estaban verificadas** | Son las de la tercera pasada |
| 3 | Patologías caninas **que se habían perdido** | 30-5, 31-3, 32-6. Aplicadas hoy |
| 10 | Patologías caninas que el motor no ofrece (oral, gastritis, motilidad gástrica, gastroenteritis aguda, intestino corto, periodontal…) | Cuadros agudos o quirúrgicos, o que no se tratan con la composición de la ración |

## Las tres que faltaban

### 30-5 · Cáncer

La patología `cancer_soporte` existía y **no aplicaba ni una cifra**. La tabla da
cinco. Aplicadas tres:

- **Grasa ≥ 62,5 g/1000 kcal** («25 to 40% of DM»). Es la **única patología del
  motor que pide MÁS grasa, no menos**.
- **Proteína ≥ 75 g** («30 to 45% of DM», «in excess of adult requirements»).
- **Arginina ≥ 5 g** («>2% DM»), más de tres veces el mínimo de FEDIAF (1,51).

La cuarta, **omega-3 ≥ 12,5 g** («>5% DM»), **está escrita y NO se aplica: no
cabe**. Medido con las otras tres puestas, perro de 22 kg:

```
suelo 10,0  -> menú en el peldaño 0
suelo 11,5  -> menú en el peldaño 5
suelo 12,0  -> SIN MENÚ EN NINGÚN PELDAÑO
suelo 12,5  -> SIN MENÚ EN NINGÚN PELDAÑO
```

El techo de este catálogo está entre 11,5 y 12,0. El motivo es del catálogo, no
de la nutrición: la fuente más concentrada es el aceite de linaza (62,5
g/1000 kcal) y para llegar a 12,5 habría que meter ~20 % de las kcal del día en
aceite. La propia Tabla 30-6 de SACN5 enseña que **sí** se alcanza en un pienso
(Hill's n/d, el de los ensayos de Ogilvie en linfoma: 7,29 % MS). Lo que falta es
una fuente concentrada de EPA+DHA en el catálogo.

Y hay una segunda lectura que no se decide aquí: los 12,5 salen del puente
`%MS × 2,5`, que supone 4000 kcal/kg de materia seca. Una ración de cáncer es la
más grasa del motor y su densidad ronda los 4400 — con esa densidad el mismo
«>5 % MS» son **11,4 g, y 11,4 sí cabe**. O sea que puede que el límite no sea
inalcanzable sino mal convertido. Es exactamente el trabajo de humedad que queda
pendiente.

La quinta, **omega-6:omega-3 ≈ 1:1**, el motor no la sabe expresar: solo conoce
un ratio, el calcio:fósforo. Y el techo de carbohidrato («NFE ≤25 % DM») tampoco,
aunque una ración BARF queda muy por debajo por construcción. Las dos quedan
escritas en el aviso de la patología y en `PENDIENTE_NUTRICION.md`.

### 32-6 · Dermatosis inflamatorias (la atópica)

El capítulo 32 tiene **dos** tablas y yo había leído una. La 32-1 (que ya se
aplicaba) es la de dermatosis por **déficit** de nutrientes; la 32-6 es la de
dermatosis **inflamatorias**, que es la atopia.

- **Omega-3 total ≥ 0,875 g/1000 kcal** («0.35 to 1.8% dry matter»). Sale en el
  peldaño 0, sin soltar nada.

La misma fila da también «50 to 300 mg total omega-3/kg body weight/day», que es
como se pauta un **suplemento**, no como se formula una ración. No se modela:
son dos unidades distintas y mezclarlas sería inventar.

### 31-3 · Reacciones adversas al alimento → **patología nueva**

Esta tabla es de una indicación que el motor **no ofrecía como patología**. Se ha
creado `reaccion_adversa_alimento`, la número 47.

- **Omega-3 total ≥ 0,875 g** (el mismo rango que la 32-6, y la fuente dice por
  qué: «Based on levels… recommended for use in the management of inflammatory
  skin diseases (Chapter 32)»).
- **Fósforo ≤ 2000 mg** y **sodio ≤ 1000 mg** («0.4 to 0.8% DM» y «0.2 to 0.4%
  DM»), **solo en adulto**.
- **Atún y caballa fuera del menú** («Avoid foods that contain certain fish
  ingredients [e.g., tuna, mackerel, skipjack, bonito]»), por aminas
  vasoactivas. Puesto en el catálogo con `restricciones_patologia`, el mismo
  mecanismo por el que el plátano no entra en un menú de diabetes. El bonito y
  el listado no están en el catálogo.
- **Proteína ≤ 55 g escrita y NO aplicada**, y el motivo es el paréntesis de la
  fuente: «(dermatologic cases only)». El motor no sabe si la reacción de este
  perro sale por la piel o por el intestino, y la misma página dice que en el
  segundo caso hace falta **más** proteína, no menos. Medido de todas formas
  —con el techo puesto **sí** hay menú, peldaño 0, verde—, para que quede claro
  que no se deja fuera porque no quepa.

**`solo_en_adulto` no lo decidí yo: lo cazó `auditar_patologias.py`** al
aplicarlo. El techo de fósforo (2000) cae por debajo del mínimo de FEDIAF de un
cachorro joven (2250), así que no sería un tope sino una prescripción. Y la
fuente ya lo decía: sus cifras son «for apparently healthy **adult** dogs».

## Dos cosas más que salieron de leer los capítulos SIN tabla

### La epilepsia no tiene tabla, pero el capítulo 28 la nombra

Y las dos veces importan: (1) un subgrupo de epilépticos idiopáticos —muchos
schnauzer miniatura— tiene hipertrigliceridemia, y «in some dogs, dietary therapy
has successfully reduced blood triglyceride levels and **eliminated seizures**
without concomitant use of anticonvulsant drugs»; (2) el fenobarbital a largo
plazo puede subir el colesterol. Lo primero es formulable **hoy**: es la
hiperlipidemia, que ya está en la lista. Puesto como aviso de la epilepsia.

### El aviso de crecimiento de la artrosis decía algo que no es

Ponía que «los suelos de omega-3 y vitamina E sí se aplican igual» en un
cachorro. **Es falso.** `topes_de_patologias()` no separa suelos de topes: con
`solo_en_adulto` y un perro que crece, se salta la patología **entera**. Lo
escribí yo el mismo día que puse los suelos, describiendo lo que me parecía
razonable en vez de lo que hace el código.

Se corrige **el texto** y no el código: separar suelos de topes en crecimiento
(¿le doy a un cachorro con displasia el refuerzo de omega-3?) es una decisión
clínica. Queda en `PENDIENTE_DECISIONES.md`.

## Un fallo del solver que destapó todo esto

Con los suelos del cáncer puestos, el motor construía un menú y el filtro final
lo tiraba. La causa:

- El solver exigía los suelos por patología sobre las **kcal pedidas** (`der`).
- `_tope_patologia_roto` los mide sobre las **kcal reales** del menú, que es lo
  correcto: un suelo es una concentración igual que un techo.

Un menú puede salir hasta un 3 % **por encima** del DER. Medido: 1172 kcal contra
1138 pedidas, 72,2 g de grasa → 63,4 g/1000 kcal contra las pedidas (cumple) y
**61,6 contra las reales (no cumple)**.

Es el mismo fallo del 21 de agosto —el fósforo renal a 1426 con el tope en
1400— visto desde el otro lado. Los **techos** tienen su fila relativa desde
entonces; los **suelos** no la tenían, porque no existían hasta el 7 de
septiembre y se añadieron copiando solo la mitad absoluta. Arreglado con
`patologia_suelo_relativo` en `motor_completo.py`.

## Y un agujero de diseño: los avisos que no llegaban a nadie

`patologias.py` solo dejaba pasar cuatro claves de `avisos`: `general`,
`crecimiento`, `profesional` y `profesional_crecimiento`. **Cualquier otra se
cargaba del JSON y se quedaba dentro**, sin llegar al menú ni a
`GET /patologias`. Texto escrito con su fuente que no leía nadie, y sin que
saltara nada.

Se descubrió al escribir la Tabla 31-3, que tiene tres avisos que no son «el
general» —una o dos proteínas y novel, el omega-3 que confunde la fase de
diagnóstico, y por qué se van el atún y la caballa—. Los tres se habrían perdido.
Ahora hay `avisos_extra`, ordenados por su clave para que el mismo archivo dé
siempre los mismos avisos en el mismo orden.

## Lo que se ha revisado y NO se aplica, con el motivo

- **Tabla 33-5** (crecimiento de razas grandes y gigantes) pide calcio
  0,8-1,2 % MS = 2000-3000 mg/1000 kcal. **FEDIAF permite hasta 4500** en
  `CachorroCrecimiento`. Es un libro de texto apretando por encima del
  regulador en un perro **sano**, no en una patología, y el motor ya aplica la
  nota b de FEDIAF (2500 de mínimo reforzado en raza grande). Apuntado, no
  aplicado.
- **Tabla 47-4** (prevención de enfermedad periodontal) pide vitamina E ≥400
  UI/kg MS. Es la **quinta** tabla que pide esa misma cifra, y esta vez para un
  perro sano. La periodontal no es una patología del motor: se trata con
  textura y cepillado, no con la composición.
- **Tablas 49-2, 52-2, 54-2, 56-2, 59-1** (enfermedad oral, gastritis,
  motilidad gástrica, gastroenteritis aguda, intestino corto): cuadros agudos o
  quirúrgicos. Lo que piden es densidad energética, textura y frecuencia de
  tomas, no una composición distinta.
- **Tablas 13-3 y 14-2** (perro adulto joven y maduro sanos) piden fósforo
  0,4-0,8 % y 0,3-0,7 % MS = 1000-2000 y 750-1750 mg/1000 kcal. **Una ración
  BARF normal ronda los 4000.** ⚠️ Aquí ponía «aquí manda FEDIAF, que no pone
  máximo de fósforo», y era falso: **FEDIAF sí lo pone en adulto, 4,00 g/1000
  kcal** (Tabla III-3b, nota h). Corregido el 9 de septiembre. Lo que pasa es que
  la ración BARF sale **pegada a ese máximo** y el libro recomienda la mitad, que
  es justo la razón por la que el techo de SACN5 se aplicó la noche del 8 (ver
  `DECISIONES.md` D-15). Es la pregunta grande que abrió este barrido, porque
  es de donde salen los topes de fósforo y sodio de la artrosis (34-2) y de la
  reacción adversa (31-3): las dos tablas repiten la cifra del perro sano por
  la comorbilidad de su población. Ver `PENDIENTE_NUTRICION.md`.

---

## Quinta pasada (9 de septiembre de 2026) · contar el barrido contra el total, esta vez de verdad

La §cuarta pasada dejó escrita la lección: *«un barrido cuyo resultado no se
compara contra el total no es un barrido, es una muestra»*. Ese día se corrigió
el número de tablas (89, no 40) y se recuperaron tres. **Lo que no se hizo fue
volver a contar.** Se hace hoy, y sale peor de lo que parecía.

### El recuento

| | |
|---|---|
| Tablas «Key nutritional factors» en SACN5 (contadas sobre el texto completo) | **91** |
| Citadas en `Canislab-api` | **32** |
| Sin citar | **59** |

Y las 59, clasificadas por lo que son —no por lo que parecen—:

| | Cuántas | Qué son |
|---|---|---|
| Comparativas de producto | **38** | «Key nutritional factors **in selected commercial veterinary therapeutic foods**… compared to recommended levels». No traen requisito: comparan piensos del mercado contra la recomendación, que ya tenemos. Son saltables |
| Solo de gato | **10** | 20-3, 21-2, 22-1, 24-1, 27-5, 27-6, 46-12, 46-13, 68-7 y la de gatitos |
| **Requisito canino o mixto SIN MIRAR** | **11** | Abajo, una a una |

### Las once

| Tabla | De qué |
|---|---|
| **16-4** | Cachorros lactantes — la composición de la leche de la perra |
| **18-9** | **Perros de trabajo y deporte.** No es una patología: es una etapa/actividad que la app ya pregunta |
| **25-5** | Alimentos líquidos o batidos comerciales, perro y gato (cuidados críticos) |
| **49-2** | Enfermedades orales |
| **50-3** | Trastornos de la deglución por lesión obstructiva |
| **50-4** | Esofagitis y reflujo gastroesofágico |
| **52-2** | Gastritis y úlcera gastroduodenal |
| **54-2** | Motilidad y vaciamiento gástrico |
| **56-2** | Gastroenteritis o enteritis aguda |
| **59-1** | Síndrome de intestino corto |
| **62-1** | **Colitis** |

Casi todas son del bloque digestivo, que es justo donde el motor **sí** ofrece
patología (`enteropatia_cronica`, con la Tabla 57-1) y donde por lo tanto es más
fácil que falte una vecina.

### ✅ CERRADAS LAS ONCE, EL MISMO DÍA

Leídas las once. El resultado, que es más ordenado de lo que parecía:

| | Cuántas | |
|---|---|---|
| Aplicada | **1** | 18-9, la vitamina E del perro de trabajo |
| Sin ningún nutriente | **1** | 49-2: agua, densidad energética y textura |
| No aplican a Rawku | **2** | 16-4 (leche de la perra) y 25-5 (alimentos líquidos enterales) |
| Familia digestiva, con núcleo común | **5** | 52-2, 54-2, 56-2, 59-1, 62-1 |
| Esofágicas | **2** | 50-3 y 50-4 |

Las siete últimas son **patologías que no ofrecemos**, y añadirlas es decisión de
producto, no de fuentes. Están transcritas y convertidas en
`HALLAZGOS_LECTURA_FUENTES.md`, con su núcleo común identificado —tres suelos de
electrolitos que se repiten en cuatro de las cinco tablas digestivas— para que la
decisión se pueda tomar con los números delante y de una vez, no tabla a tabla.

**Lo que sigue abierto es el recuento grande**: 26 capítulos de 70 sin una sola
cita, de los que van leídos enteros el 7, el 45, el 49, el 51 y el 61, más los
bloques que hacían falta del 18, el 50, el 52, el 54, el 56, el 59 y el 62.

⚠️ **Actualizado el 9 de septiembre por la tarde: van cuatro más, enteros** — el
**38** (urolitiasis canina), el **47** (enfermedad periodontal), el **48**
(introducción a las digestivas y del páncreas exocrino) y el **55** (introducción
al intestino delgado). O sea **nueve de los 26** leídos completos, y con ellos se
cierran los tres temas caninos que la lista nombraba aparte: urolitiasis general,
enfermedad periodontal y la entrada del bloque digestivo.

Lo que trajeron, y ninguna de las cuatro cosas estaba en una tabla que hubiéramos
mirado:
- El **8,79 % de 350.803 urolitos son compuestos** (Tabla 38-8), que refuerza una
  nota que ya estaba escrita y le pone el porqué mecánico.
- La **Tabla 47-4 repite el fósforo 0,4-0,8 % y el sodio 0,2-0,4 %** de la 13-3
  —los dos techos que el motor aplica al adulto sano— y da el motivo que la 13-3
  no daba: prevención renal y de hipertensión en el perro sin nada.
- **La escala de digestibilidad** (recuadro 48-3), que responde a una pregunta
  que estaba abierta desde ayer.
- Y **la cautela del libro sobre el hueso**: 67 foxhounds con carcasas crudas,
  todos con enfermedad periodontal y muchas fracturas dentales, y «no reliable,
  published studies showing dental benefits derived from bone chewing». Se
  comprobó que la app **no promete** ese beneficio; la cita está ahora en
  `seguridad.py`.

⚠️ **Y una segunda tanda, la misma tarde: el 26 (parenteral), el 4
(nutrigenómica) y los tres digestivos que solo estaban leídos por sus tablas —
el 54, el 56 y el 59 — enteros.** De los tres digestivos las tres tablas se
confirman, y el 56 trae en prosa **el párrafo que más nos toca de todo el
libro**: que el perro que come crudo **excreta** patógenos a mucha mayor tasa
que el que come cocinado (Weese y Armstrong, 2006). No es el riesgo del perro,
que ya estaba escrito en `inmunosupresion`: es el de quien vive con él. La app no
lo dice en ninguna parte y está apuntado en `PENDIENTE_PRODUCTO.md`.

### El recuento, rehecho a máquina esta tarde

Contando otra vez como la primera vez —buscando cada capítulo del 1 al 70 en
todos los `.md`, `.json` y `.py` del repo— **quedan 5 capítulos sin una sola
cita**, de los 26 que había esta mañana, y **los cinco son de otra especie**:

| Capítulo | Tema |
|---|---|
| 22, 23, 24 | Gata reproductora, gatitos lactantes, gatitos en crecimiento |
| 46 | Tracto urinario inferior felino |
| 70 | Pequeños mamíferos de compañía |

⚠️ **O sea que lo canino de SACN5 está leído entero.** El último fue el **25**
(cuidados críticos y alimentación enteral asistida), el hermano del 26 —sonda en
vez de vena—, y se leyó precisamente porque la suposición de que «casi seguro no
trae nada» es la que la §cuarta pasada dice que no vale. Menos mal: trae **el
ritmo al que un perro puede adelgazar** (1-4 % del peso a la semana, típicamente
1-2 %, Laflamme 1993), que no estaba en el repo y que es lo único que permite
comprobar desde casa si «adelgazamiento dirigido» está funcionando.

### Y 26 capítulos de 70 sin una sola cita

Contado igual: buscando cada capítulo en todos los `.md` y `.json` del repo.
Siete son felinos o de otras especies. Los caninos que quedan son antioxidantes,
urolitiasis general, urolitos compuestos caninos, enfermedad periodontal y el
bloque digestivo entero.

### La consecuencia, que es la que importa

**`CERRADO.md` reabre los límites de patología.** No porque haya una cifra mal
—las que hay siguen siendo las de su fuente y la batería lo vigila—, sino porque
«cerrado» no puede significar «cerrado sobre lo que casualmente hemos leído».

Y la lección se apila sobre la de la cuarta pasada, un escalón más arriba: no
basta con contar el barrido contra el total **de tablas**. El 8 de septiembre se
vio que las tablas no lo dicen todo —la arginina que sube con la proteína, el
ratio linoleico:linolénico y la proteína de la lactancia estaban en prosa, no en
filas—, así que **el total contra el que hay que contar es el libro, no su índice
de tablas**.
