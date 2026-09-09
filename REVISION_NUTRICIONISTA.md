# La revisión de Cris Carles, punto por punto

**Escrito el 8 de septiembre de 2026**, comprobando cada punto contra el repo
del día, no contra lo que recordábamos. Cris escribió su valoración **antes** de
las cuatro pasadas de verificación de patologías de ese día, así que parte de lo
que señaló ya no es cierto — y parte sigue siéndolo entera.

> «Me gusta la idea de un software que quite trabajo mecánico, pero creo que a la
> parte de patologías le falta trabajo.»

Tenía razón. Este documento dice **en qué ya no**, **en qué a medias** y **en qué
sigue teniéndola**, con lo que hay que hacer en cada caso.

---

## 1 · «Los criterios para patologías no modifican los % de macros en la mayoría de los casos, solo tienen en cuenta determinados micros»

### ✅ CUBIERTO

Era cierto cuando lo escribió. Hoy **15 de las 47 patologías tocan macros**:

| Patología | Proteína | Grasa | Fibra |
|---|---|---|---|
| renal | ≤62,5 | | |
| pancreatitis | ≤75 | ≤37,5 (**≤25** si además hay obesidad o hiperlipidemia) | |
| obesidad | ≥62,5 | ≤30 | ≥30 |
| hiperlipidemia | | ≤30 | ≥25 |
| PLE / linfangiectasia | ≥62,5 | ≤37,5 | ≤12,5 |
| EPI | | ≤37,5 | ≤12,5 |
| enteropatía crónica | ≥62,5 | ≤37,5 | |
| SIBO | | ≤37,5 | |
| cáncer | **≥75** | **≥62,5** | |
| estruvita | ≤62,5 | | |
| fosfato cálcico | ≤62,5 | | |
| diabetes | | ≤30 % de las kcal si además pancreatitis o hipertrigliceridemia | ≥17,5 |
| estreñimiento | | | ≥17,5 |
| flatulencia | ≤75 | | ≤12,5 |
| intestino irritable | | | ≥20 |

Todas con la cita literal de su fuente, la conversión escrita y el margen que le
queda al profesional contra el límite de FEDIAF. Se sirven en `GET /patologias`.

---

## 2 · «Un renal IRIS 2 ya requiere restricción proteica moderada, y en un IRIS 4 hay que bajarla hasta el 15 % o más»

### 🟡 A MEDIAS — sabemos dónde está la frontera, pero no formulamos por debajo

Hay dos niveles:

- **`renal`** — proteína ≤62,5 g/1000 kcal. Es la restricción moderada.
- **`renal_avanzada`** (equivalente a IRIS 3-4) — marcada **`formulable: false`**,
  con `nutriente_frontera: proteina` y `objetivo_terapeutico_por_1000kcal: 42,5`.

El 15 % de materia seca que dice Cris son **37,5 g/1000 kcal**, y el mínimo de
FEDIAF son **52,1**. O sea: el motor **sabe** que ahí hay que bajar y **sabe** que
eso cruza FEDIAF, y por eso no lo formula solo. Lo que falta es la parte firmada
—el rol profesional que puede prescribir por debajo del mínimo con un juego de
requisitos propio que viaja con el menú—, que está diseñada (`VETERINARIOS.md`) y
no construida.

**Lo que NO tenemos es el estadiaje fino de IRIS** (1, 2, 3, 4 por separado):
tenemos dos escalones donde ella maneja cuatro.

---

## 3 · «Empieza a salir carente de metionina, que se tiene que suplementar como L-metionina»

### ❌ NO CUBIERTO — y es un hueco de catálogo concreto

La **metionina sí se verifica**: está en `verificar.MAPA` desde el 28 de agosto,
con su mínimo de FEDIAF y también el de metionina+cistina, que es una suma que
calcula `valor_nutriente`. Así que el motor **detectaría** la carencia.

Lo que no hay es **con qué arreglarla**: no existe ninguna ficha de L-metionina
en el catálogo. Buscado por nombre — no está.

**Qué hace falta:** una ficha de L-metionina con su etiqueta real (mg por 100 g y
dosis máxima del fabricante), como las demás fichas de suplemento. Va a
`DATOS_QUE_FALTAN.md`.

---

## 4 · «Pancreatitis: si has puesto grasa por debajo del 20 %, yo la he bajado hasta el 8-10 % según las analíticas»

### 🟡 A MEDIAS — los dos niveles de la fuente están; el suyo es prescripción

El motor aplica **los dos niveles literales de la Tabla 67-3 de SACN5**:

- ≤15 % de materia seca = **37,5 g/1000 kcal** en el perro no obeso ni
  hipertrigliceridémico,
- ≤10 % = **25 g** si además hay obesidad o hipertrigliceridemia.

(Hasta el 8 de septiembre había un solo nivel, y encima el más estricto de los
tres: 20 g, de Merck. Se corrigió por la regla de fuentes del repo — SACN5 manda
sobre Merck.)

El **8 %** al que ella baja son **20 g/1000 kcal**: por debajo de lo que da la
fuente para cualquier perro, y eso es **una prescripción individual**, no un tope
general. Es exactamente el caso de uso de la pantalla del punto 5.

---

## 5 · «Decidir dónde dejas la proteína y cuánto subes los carbos es una decisión individual»

### ❌ NO CUBIERTO — diseñado y medido, no construido

Es su petición de fondo, y es la buena.

**Lo que ya funciona (medido, no supuesto):** el solver es un MILP y cada
nutriente es una fila con su mínimo y su máximo, así que **pedir un objetivo es
exactamente eso**, y el mecanismo ya es genérico. Perro adulto de 22 kg, catálogo
real:

| Lo que se pide | Resultado |
|---|---|
| grasa ≤45 / 40 / 37,5 / 35 / 30 / 28 | menú **verde** en las seis, y la grasa sale clavada |
| grasa ≤25 | sin menú |
| fósforo ≤1200 **y** sodio ≤739 | verde, 1165,2 y 453,0 |
| «solo pavo, conejo y sardina» + grasa ≤40 | verde, grasa 40,0, y de carne solo entra conejo |

**Lo que falta:** la pantalla donde pedirlo, el rol profesional que lo firma, y
que el objetivo pedido y no cumplido haga que el menú **no salga** (regla 1) en
vez de salir verde porque el semáforo solo mira FEDIAF. Está todo escrito en
`PLAN_OBJETIVOS_PROFESIONAL.md`.

---

## 6 · «Me falta el lipidograma, porque la relación omega-6:omega-3 es crucial en muchas patologías»

### ❌ NO CUBIERTO — no existe en el motor

Buscado: no hay ni una línea de ratio omega-6:omega-3 en ningún sitio.

**Y no es solo ella quien lo pide.** La Tabla 30-5 de SACN5 (cáncer) pide
literalmente *«an omega-6:omega-3 fatty acid ratio approximating 1:1»*, y al
aplicarla el 8 de septiembre hubo que dejarlo escrito como «el motor no sabe
expresarlo».

**Lo que sí hay** desde ese día es la clave `omega3_total` (linolénico + EPA +
DHA), con suelo real en artrosis (8,75 g/1000 kcal), disfunción cognitiva (2,5),
dermatitis atópica (0,875) y reacción adversa al alimento (0,875). Es la mitad de
la cuenta: el numerador está, el ratio no.

**Es implementable y no es caro:** un ratio entre dos sumas de nutrientes es
lineal igual que el calcio:fósforo, que el motor ya aplica. Lo que falta es la
forma de que una patología —o un profesional— pida el suyo. Es el mismo trabajo
que arreglaría el `ratio_ca_p` de los urolitos de calcio, que también está
escrito y sin aplicar.

### ⚠️ ACTUALIZADO EL 9 DE SEPTIEMBRE: ahora hay TRES fuentes y NO dicen lo mismo

Y por eso esto ya no es un «implementarlo y ya», sino una decisión con nombre:

| Fuente | Qué dice del ratio |
|---|---|
| Cris Carles | La relación omega-6:omega-3 es crucial en muchas patologías |
| **SACN5 Tabla 30-5** (cáncer) | *«an omega-6:omega-3 fatty acid ratio approximating 1:1»* |
| **SACN5 cap.25** (cuidados críticos) | **5:1 a 1:1**, «depending on patient assessment», y añade que **no está estandarizado** |
| **NRC 2006, cap.5** | Del ratio de **totales**: *«is not helpful»*. Recomienda en su lugar el **linoleico:linolénico** |

**Y esa última ya está aplicada.** Desde el 9 de septiembre el motor exige el
**ratio linoleico:linolénico** —2,6-26 en adulto y crecimiento, 2,6-16 en
gestación y lactancia— vía `requisitos_condicionales.json`, que es exactamente lo
que el NRC recomienda **en lugar** del de totales.

O sea que la mitad de lo que Cris pedía **sí está**, con otra forma y con la
fuente que dice por qué esa forma y no la otra. Lo que sigue sin estar es el
ratio de **totales**, y ahora la pregunta no es «¿se puede?» sino «¿debe?». Va
como **PREGUNTA 40** en `PARA_EL_NUTRICIONISTA.md`, con las tres fuentes en la
mano.

**Y tiene razón en lo de FEDIAF**: no se moja. Da mínimo de linoleico, y de
EPA+DHA solo en crecimiento y reproducción; en adulto, nada. Por eso el motor
adoptó el mínimo de EPA+DHA de NRC 2006 para adulto (0,11 g), decidido el 25 de
agosto y anotado como excepción en `auditar_fediaf.py`.

---

## Resumen

| | Punto | Estado |
|---|---|---|
| 1 | Macros por patología | ✅ cubierto — 15 de 47 patologías |
| 2 | Estadiaje renal e IRIS 4 | 🟡 dos escalones de cuatro; la frontera está marcada, no se formula por debajo |
| 3 | L-metionina | ❌ se verifica, pero no hay ficha en el catálogo |
| 4 | Pancreatitis al 8-10 % | 🟡 los dos niveles de la fuente están; el suyo es prescripción |
| 5 | Objetivos de macros individuales | ❌ diseñado y medido, sin pantalla ni firma |
| 6 | Ratio omega-6:omega-3 | ❌ no existe |

**Lo que hay que hacer, por orden de lo que desbloquea:**

1. **El ratio omega-6:omega-3.** Es lineal, el motor ya sabe de ratios, y lo
   piden dos fuentes independientes (Cris y la Tabla 30-5). El mismo trabajo
   arregla el Ca:P por patología.
2. **La pantalla de objetivos por nutriente y el rol que firma.** Es lo que
   convierte «tres escalones de renal» en «el estadio que tú digas», y lo que
   permite el 8 % de grasa de una pancreatitis aguda.
3. **La ficha de L-metionina** en el catálogo. Es un dato, no código.
4. **El estadiaje de IRIS** más fino, que depende de 2.
