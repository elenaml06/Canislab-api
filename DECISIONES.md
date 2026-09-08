# DECISIONES — lo que no se vuelve a discutir

Las decisiones **cerradas** del nivel 1 (la nutrición), con fecha, qué se
decidió, la fuente y el motivo. Se lee al empezar cualquier sesión, junto con
`ESTADO.md`, **antes de tocar nada**. Si lo que ibas a hacer ya está aquí, no
se hace.

Abierto el 8 de septiembre de 2026, porque no existía y por eso las cosas
dadas por hechas volvían a salir cada pocas semanas.

---

## 0 · Qué es «cerrado», y cuándo se puede reabrir

Algo del nivel 1 está cerrado cuando cumple **las seis condiciones a la vez**:

1. **Vive en el repo, versionado.** No en una conversación, no en un informe,
   no en un fichero suelto en un ordenador.
2. **Lleva su fuente**, de forma que alguien pueda ir a comprobarla.
3. **Lleva su ficha de permisos completa** —`tipo`, `fuente`, `visible_para`,
   `modificable_por`, `rango_permitido`, `requiere`, `defecto`,
   `al_moverlo`— o la parte que falte está declarada como pregunta abierta.
4. **Hay un test automático que falla si se rompe.** «Lo comprobé» no cierra
   nada.
5. **Está escrito como decisión**, con fecha y motivo.
6. **No deja preguntas colgando sin dueño.**

### Se reabre solo si

- Lo dice el nutricionista.
- Aparece una fuente que lo contradice **y se puede citar**.
- Un test o un caso real demuestra que está mal.
- Cambia el alcance del producto y la decisión deja de aplicar.

**Nada más.** Que a alguien —a la usuaria incluida, o a una sesión nueva— le
parezca dudoso **no es motivo**. Si te asalta la duda sobre algo de aquí,
apúntalo en `PREGUNTAS_ABIERTAS.md` con dueño; no reabras el trabajo. Cuando
algo se reabra, queda constancia de la decisión anterior, del motivo y de
quién lo pide.

### Sobre la condición 3 (la ficha de permisos)

**Ninguna decisión de este fichero la cumple todavía**, porque la ficha de
permisos no existe aún en ninguna parte del nivel 1 (`ESTADO.md` §1). Están
aquí igualmente y la razón importa: **son decisiones sobre qué es verdad, no
sobre quién puede moverlo.** Un dato que se comprobó contra su fuente y salió
falso no deja de ser falso porque nadie haya escrito todavía quién podría
tocarlo. Lo que la ficha les falta va apuntado en cada una, y cerrar esa
columna es la fase 1.

### Las tres cajas

Cada decisión numérica dice en cuál cae, porque es lo que le permite a un
revisor externo saber qué está mirando:

- **Tope duro** — límite legal o valor verificado contra fuente primaria. No
  se mueve.
- **Rango clínico** — la fuente da un rango a propósito, porque depende del
  caso, del estadio y de la analítica. Se implementa como rango con palanca
  del veterinario, **nunca como constante**.
- **Criterio nuestro** — lo pusimos porque resolvía un problema real
  observado, sin fuente veterinaria detrás. Es legítimo, pero va **declarado
  como criterio**, no disfrazado de ciencia.
## D-01 · El `TR` de BEDCA NO significa «trazas». El campo `trazas` se rechaza

**Fecha:** 8 de septiembre de 2026.
**Caja:** no aplica — es una decisión sobre lectura de fuente, no un valor.
**Estado:** cerrado salvo ficha (no le corresponde ficha: no es un valor movible).

**Qué se decidió.** La rama `claude/nutrition-audit-data-validation-bihto9`
(3–6 de septiembre, nunca fusionada) creaba un campo **`trazas`** con 14
celdas de vitamina A y D en diez pescados, y **las sacaba de `sin_dato`**. El
argumento escrito era razonable: «una traza es un dato publicado, no un
hueco». **Se rechaza. No se rescata, y no se vuelve a proponer.**

**La fuente y qué dice.** El esquema de BEDCA:

| código | significa |
|---|---|
| `AR` / `BE` + un número | es una **medida**, aunque el número sea 0 |
| `LZ` + un 0 | cero **lógico**: por composición no puede tenerlo |
| `TR` + **celda vacía** | **NO HAY CIFRA.** Es un hueco |

**Comprobado dos veces, por dos sesiones distintas, contra el servicio de
BEDCA en directo** (`contrastar_fuentes.bedca_ficha`, que imprime el
`value_type`). La segunda comprobación es del 8 de septiembre y estos son los
ocho identificadores, tal como respondió el servicio:

| id | ficha | Vitamina A | Vitamina D |
|---|---|---|---|
| 2347 | Merluza fresca | `('', 'TR')` | `('', 'TR')` |
| 2136 | Bacaladilla | `('', 'TR')` | `('', 'TR')` |
| 2341 | Lenguado | `('', 'TR')` | `('', 'TR')` |
| 2344 | Lubina | `('', 'TR')` | `('', 'TR')` |
| 825 | Merluza, congelada, cruda | `('', 'TR')` | `('', 'TR')` |
| 2320 | Calamar, asado | **`('63', 'AR')`** | `('', 'TR')` |
| 2471 | Pulpo | **`('70', 'AR')`** | `('', 'TR')` |
| 2635 | Sepia | **`('2', 'AR')`** | `('', 'TR')` |

**La prueba de que el campo era exactamente eso y no otra cosa** está en las
tres últimas filas: **donde la rama NO marcaba traza —la vitamina A de
calamar, pulpo y sepia— BEDCA sí publica cifra con `AR`: 63, 70 y 2.** El
campo `trazas` calcaba celda por celda las `TR`. No era una lectura parcial de
la fuente: era la lectura del código de ausencia.

**Qué habría pasado si se aplica.** Catorce huecos correctamente declarados se
habrían convertido en **ceros medidos falsos**. Y eso no es cosmético: un
`sin_dato` **no cuenta como cero contra un techo** —se imputa al percentil 90
de su familia, `constructor.valor_para_maximo`—, mientras que un cero medido
sí defiende. El resultado habría sido **aflojar el techo crónico de la
vitamina D** en diez pescados, que es uno de los cinco topes duros de la
regla 2 de `CLAUDE.md`. Un hueco no es un cero: contra un mínimo el cero es
conservador, contra un máximo es peligroso, porque aprueba lo que no sabemos.

`main` ya las tenía bien, en `sin_dato`.

**Test que lo protege:** BLOQUE 51 de `pruebas_completas.py`, que falla si
vuelve a aparecer el campo `trazas` en el catálogo. ⚠️ **Ese bloque vive hoy
en la rama `claude/nutricion-pendiente-vuoobq`, sin fusionar.** Mientras no
entre, esta decisión cumple cinco de las seis condiciones, no las seis.

**Nota al margen, sin efecto sobre la decisión:** el id 2320 es «Calamar,
**asado**», no crudo. No cambia nada aquí —lo que se comprueba es el código de
ausencia, no la cifra—, pero conviene saberlo si alguien usa esa ficha para
otra cosa.

---

## D-02 · La rama `nutrition-audit-data-validation-bihto9` no tiene nada que rescatar

**Fecha:** 8 de septiembre de 2026.
**Estado:** cerrado (decisión de proceso; no lleva ficha ni test).

**Por qué se escribe.** Una rama descartada **necesita una decisión escrita
que diga por qué, o vuelve**: otra sesión la abrirá, verá trabajo
aparentemente pendiente y deshará una comprobación ya hecha.

**Contexto.** La rama salió del `main` del 2 de septiembre. `main` ha cambiado
mucho desde entonces: aplicarla tal cual —o hacer cherry-pick— **borra trabajo
posterior verificado**. Hoy está 11 commits por delante y **56 por detrás**.

**Qué se rescató**, ya aplicado en la rama `claude/nutricion-pendiente-vuoobq`:

- **86 casillas** donde el mismo número se repite entre fichas distintas: 21
  cobres con solo cuatro valores en todo el grupo, y 70 celdas en seis huesos
  carnosos donde conejo, pato, pollo y cordero declaran la misma vitamina A,
  la misma D y la misma riboflavina siendo especies distintas. Pasan a
  `sin_dato`. Comprobado antes: BEDCA **no publica cobre** para besugo,
  lubina, pulpo, calamar, trucha, lenguado ni pescadilla.
- **La columna de humedad** con procedencia, en 65 fichas.

**Qué se descartó a propósito, y no se vuelve a mirar:**

1. **El campo `trazas`** — D-01.
2. **46 de las 132 casillas que la rama vacía**: son valores contrastados
   **después** del 2 de septiembre contra BEDCA/CIQUAL/USDA. El EPA, el DHA y
   los **400 µg de yodo del aceite de hígado de bacalao** están entre ellos, y
   **el yodo es un tope crónico**. Aplicar la rama los borra.
3. **Las 69 diferencias de `Cerebro de ternera`**: `main` tiene la ficha
   rehecha desde USDA 168622 tras el lío vaca/ternera. La rama tiene la
   versión vieja.
4. **Borrar los tres cuellos y la laringe del catálogo**: `main` los conserva
   y los **bloquea en el solver** por tejido tiroideo
   (`seguridad.TIROIDES_EXCLUIR`), que es mejor — el alimento sigue existiendo
   y el motivo queda escrito.

**Lo que ya estaba en `main` por otro camino** (PR #76 y #80), comprobado una a
una: las 103 correcciones del catálogo (albahaca fósforo 56, hígado de pollo
vitA 3296 y cobre 0,492, dorada grasa 1 y vitD 1,5), el techo legal de la
vitamina D y el bloqueo de tejido tiroideo.

**Conclusión: la rama se puede borrar.**

**No verificado por mí:** el detalle casilla a casilla de los cuatro puntos
descartados. Lo verificó la sesión de `claude/nutricion-pendiente-vuoobq` el 8
de septiembre y lo dejó escrito en su `TRASPASO.md`. Yo he confirmado los
hechos estructurales: la rama existe, está 11 delante y 56 detrás, y su
catálogo difiere de `main` en 1.213 líneas.

---

## D-03 · El techo de lisina no se aplica. El mínimo sí

**Fecha:** 28 de agosto de 2026 (recogida aquí el 8 de septiembre).
**Caja:** **criterio nuestro**, declarado como tal.
**Estado:** cerrado salvo ficha.

**Qué se decidió.** El techo de lisina de FEDIAF (7,00 g/1000 kcal, solo en
crecimiento) **no se aplica**. El mínimo sí.

**El motivo, medido:** 0 de 15 menús de cachorro caben debajo, porque la
lisina va detrás de la proteína y una ración BARF de cachorro lleva ~134
g/1000 kcal contra un mínimo de 50. Aplicarlo dejaría a **todos** los
cachorros sin menú.

**Dónde vive:** `verificar.MAXIMOS_NO_APLICADOS = {"Lisina"}`, lista única
leída por el solver y por el semáforo vía `maximo_de()`.

**Test:** BLOQUE 27 comprueba, entre otras cosas, que **es el único máximo no
aplicado**.

**Lo que le falta para las seis:** la ficha, y **no está cerrada la pregunta
de fondo** — sigue abierta en `PREGUNTAS_ABIERTAS.md` P-04 con el
nutricionista como dueño. Es un criterio nuestro declarado, no una decisión
nutricional cerrada.

---

## D-04 · Los mínimos escalan hacia arriba y nunca hacia abajo. Los máximos no escalan

**Fecha:** anterior al 26 de agosto de 2026 (recogida aquí el 8 de septiembre).
**Caja:** **tope duro** (la ecuación es de FEDIAF).
**Estado:** cerrado salvo ficha.

**Qué se decidió.** `minimo_de()` en `verificar.py` es el único sitio que
escala los mínimos cuando el perro come menos (ecuación de FEDIAF 7.2.5), y
`maximo_de()` el único que sabe de máximos. **Solo hacia arriba**: no hay base
en FEDIAF para bajar el mínimo de un perro que come más.

**No escalan** la grasa (FEDIAF publica 13,75 g/1000 kcal en las dos columnas;
escalarla haría que las kcal dejaran de cerrar), el
EPA+DHA/linolénico/araquidónico (no hay requerimiento absoluto en adulto), ni
crecimiento/gestación/lactancia (la ecuación no está verificada ahí).

**Los máximos no escalan nunca** — son concentración, no cantidad.

**La consecuencia, que es lo que hay que saber:** la ventana entre mínimo y
máximo **se cierra según bajan las kcal**. En dieta húmeda el selenio se cruza
en DER 45,2: por debajo el motor devuelve `imposible_por_aritmetica` (el
nutriente y los dos números) en vez del «quita una restricción» de siempre,
porque ahí no hay combinación que lo arregle.

**El peso de referencia para escalar es `peso_objetivo_kg`, no el real.** Sin
ese campo se usa el real y se escala de más, que es el lado seguro.

**Tests:** BLOQUE 34 aquí; `tests/peso-objetivo-en-cada-peticion.spec.js` en
`canislab-web`.

---

## D-05 · El peso objetivo desde el BCS se DIVIDE, no se resta

**Fecha:** 29 de agosto de 2026 (recogida aquí el 8 de septiembre).
**Caja:** **tope duro** (valor verificado contra fuente primaria).
**Estado:** cerrado salvo ficha.

**Qué se decidió.** `peso_ideal = peso_actual / (1 + 0,10 × (BCS − 5))`.

**El error que se corrigió no fue un número mal copiado: fue leer una frase de
un ejemplo sin abrir la tabla que tiene al lado.** «30 % overweight» significa
un 30 % **por encima del ideal**, no un 30 % del peso de hoy, y eso se
invierte dividiendo:

    actual = 1,30 × ideal    →  ideal = actual / 1,30 = 34,6 kg
    restar el 30 % del actual →  45 × 0,70            = 31,5 kg   MAL

**Las tres comprobaciones que lo cierran**, ninguna de interpretación:

1. La **Tabla 1 de la propia guía AAHA** da el % de sobrepeso por punto de BCS
   y el % de grasa. Su tercer método, `[peso × (100 − %grasa)] / 0,8`, no
   depende de cómo se lea «overweight» porque sale de la masa magra: da ×0,7875
   en BCS 8. Dividiendo sale ×0,7692, un 2 % de diferencia. Restando sale
   ×0,70, que se sale del propio rango del método de la grasa ya desde BCS 7.
2. La **Global Pet Obesity Initiative** (2019, Ward, German y Churchill,
   respaldada por ECVCN, WSAVA y ACVIM) define la obesidad como «30 % above
   ideal body weight» y dice que equivale a 8/9. «Above ideal» no admite dos
   lecturas.
3. **El ejemplo de AAHA es el raro de su propio documento:** dos de sus tres
   métodos dan 34-35 kg para ese labrador y el ejemplo escribe 32. Es una
   errata aritmética en la guía.

**Los dos límites, y son deliberados:**

- **Por debajo de BCS 5 no se estima.** La Tabla 1 empieza en BCS 4, no hay
  columna de «% underweight», y AAHA 2021 manda lo contrario de estimar: «base
  feeding calculations on current weight if ideal or underweight».
- **En BCS 9 la cifra es un techo, no una medida.** Broome et al. (2023, Sci
  Rep 13:22958) observan con DXA perros que «exceed the description for score
  9», y Bjornvad 2011 no encuentra diferencia de grasa entre 8 y 9. Se estima
  igual —una cota inferior es mejor que nada— pero `_peso_de_referencia` lo
  devuelve **con procedencia propia**, para que se vea que lo es.

**Test:** BLOQUE 37. Las kcal de los 85 casos del contrato del DER no se
mueven, porque el que cambió fue `verificar.py` y no `der.py`.

---

## D-06 · La rama `el-corazon-de-ternera-es-musculo` no se fusiona

**Fecha:** 8 de septiembre de 2026.
**Estado:** cerrado (decisión de proceso).

**Qué se decidió.** No se fusiona, y su contenido **no se rescata en bloque**.
Si alguien quiere el cambio que le da nombre —que el corazón de ternera es
músculo y no víscera— se hace **de nuevo**, en una rama desde el `main` de
hoy, como un cambio de una línea del catálogo con su fuente.

**Los tres motivos, medidos hoy:**

1. **Está 79 commits por detrás de `main`.** Su diff contra `main` **borra**
   `VETERINARIOS.md`, `HECHO.md`, `HISTORIA_TECNICA.md`, `patologias.json`,
   `auditar_patologias.py`, `contrastar_fuentes.py` y los cinco
   `PENDIENTE_*.md`. Fusionarla no añade un alimento: revierte semanas.
2. **Su catálogo tiene 477 fichas y las 477 están sin lisina** — es del 27 de
   agosto, un día antes de que se encendieran los 12 aminoácidos. Hoy
   reventaría el BLOQUE 27. (⚠️ Corrijo aquí lo que dice el `TRASPASO.md` de
   `claude/nutricion-pendiente-vuoobq`, que habla de «318 alimentos nuevos y
   las 318 sin aminograma»: **no son las nuevas, son las 477**, porque la rama
   entera es anterior al aminograma. `main` tiene 163 fichas, 69 de ellas sin
   lisina, y la mayoría son verduras, aceites y suplementos.)
3. **Su commit base es un WIP con la batería en rojo**, literalmente: «WIP: la
   carga puesta, con la bateria en rojo (13 fallos)».

**Nunca tuvo PR y no había una línea en ninguna parte diciendo por qué se
quedó fuera.** No se descartó: se olvidó. Esta entrada es para que no vuelva.

---

## D-07 · La rama `add-sacn5-58-capitulos` de `canislab-fuentes` no se fusiona

**Fecha:** 8 de septiembre de 2026 (la decisión de fondo es del 7).
**Estado:** cerrado (decisión de proceso).

**Qué se decidió.** No se fusiona. Es la línea **anterior** a la limpieza del
7 de septiembre, y fusionarla resucita 27 ficheros que se borraron a
conciencia.

**Qué se borró y por qué**, según el propio commit `e0eb90f` de `main`: un
borrador de investigación entero (`datos_motor.json` de 59 secciones, un
`patologias.json` de 47 perfiles marcado **«NADA DE ESTO ESTA VERIFICADO»**,
`CORRECCIONES_CATALOGO.csv`, `MOTOR.md`, `AUTORIDAD.md`, `PATOLOGIAS.md`,
`PREGUNTAS_NUTRICIONISTA.md`, cuatro scripts que dependían de esos datos, y
las carpetas `informes/` y `lecturas/`, resúmenes que su propio autor ya
marcaba «no sirven para citar»). **Nunca se reconcilió con el motor real**, y
su propio README de aviso estaba a su vez caducado: decía «11 patologías en
producción» cuando ya había 40.

**Qué se conservó, porque sí pasó verificación real:**
`HUMEDAD_CATALOGO.csv` (65 fichas de fuente directa USDA), la base de datos de
purinas en `fuentes_datos/`, y el rastro de auditoría de `entregas/`.

**Verificado por mí hoy:** la rama no borra nada de `main`; solo añade los 27
ficheros de la línea vieja. Los capítulos de SACN5 y Fascetti **ya están en
`main`** (70 PDF + 70 `.txt` en `sacn5/`), así que la rama no aporta fuentes.

⚠️ **Con una salvedad que no cierra:** entre lo borrado estaba
`PREGUNTAS_NUTRICIONISTA.md`, y su cabecera dice que la lista vigente vive en
`datos_motor.json → huecos_para_nutricionista` y en `MOTOR.md §6` — **los dos
también borrados**. O sea que **la lista viva de preguntas para la
nutricionista se borró junto con el borrador**. No es motivo para fusionar la
rama (el resto sí había que borrarlo), pero sí para recuperar **ese** contenido
antes de que la rama se borre. Va a `PREGUNTAS_ABIERTAS.md` P-08.

---

## D-08 · El tope de mercurio por días de la semana se eliminó, y no vuelve

**Fecha:** 25 de agosto de 2026 (recogida aquí el 8 de septiembre).
**Caja:** **criterio nuestro retirado**. Lo que queda (10 % de las kcal) es
criterio nuestro declarado.
**Estado:** cerrado salvo ficha — **y con un incumplimiento vivo en el front**.

**Qué se decidió.** Se elimina `TOPE_MERCURIO_DIAS_SEMANA = 1`. Los dos
motivos, y los dos importan:

1. **No lo usaba nadie.** Estaba declarado y ninguna línea del repositorio lo
   leía. La app decía tener una regla de «máximo un día a la semana» que no se
   aplicaba en ningún sitio. Peor que no tenerla: aparecía escrita en la
   documentación para la nutricionista como si fuera una restricción real.
2. **No tiene base en perros.** No existe estudio canino ni guía veterinaria
   que fije una frecuencia semanal de pescado con mercurio. Ese «≤1
   día/semana» es una transposición directa de las recomendaciones de FDA/EFSA
   para **embarazadas y niños pequeños**, grupos de especial sensibilidad al
   metilmercurio por su efecto sobre un sistema nervioso **en desarrollo**. Un
   perro adulto no es ese caso.

**Lo que sí queda:** `TOPE_MERCURIO_KCAL = 0.10`, una restricción por
**concentración calórica diaria**. El único número de referencia que existe es
el MTL de la FDA para mercurio en dieta canina (0,27 mg/kg de materia seca), y
viene extrapolado de Charbonneau et al. 1976, **que era en gatos**. Está dicho
así en el aviso al usuario.

⚠️ **Esta decisión está incumplida hoy en el nivel 2.**
`canislab-web/src/instrucciones.js:32` sigue diciéndole al dueño: «Si usas
atún u otro pescado grande, **no más de 1 vez por semana**». El nivel 1 retiró
la regla por no tener base y el nivel 2 se la sigue dando. Corregirlo es fase
3; está en `ESTADO.md` §3.2.

---

## D-09 · `POST /menu` no vuelve

**Fecha:** 26 de agosto de 2026 (recogida aquí el 8 de septiembre).
**Estado:** cerrado.

**Qué se decidió.** El endpoint `POST /menu` —el motor anterior al MILP— se
borra y no vuelve.

**El motivo:** arrastraba **su propia tabla de patologías, desincronizada de
la buena**: fósforo renal a 1.400 en vez de 1.200, cobre en hepatopatía a 3,0
y sin bloquear, grasa en pancreatitis al 25 % de las kcal, diabetes bajando la
grasa siempre, y urato, cistinuria y «otra» sin existir.

No llegó a dar menús malos porque `_garantizar_verificado()` los habría
rechazado — **que es otra forma de decir que ese camino construía menús que el
filtro final iba a tirar**.

**Test:** BLOQUE 24 vigila que no vuelva, y que no haya tablas clínicas
duplicadas.

⚠️ **La misma familia de fallo está viva hoy en dos sitios**, y esta decisión
es el motivo por el que hay que arreglarlos: la tabla de patologías cargada
dos veces en memoria (`ESTADO.md` §1.4) y la lista `PATOLOGIAS` duplicada en
`App.jsx` con una tercera copia en `tests/fake-supabase.js` (`ESTADO.md` §3.1).
Ninguno de los dos lo ve ningún test.

---

## D-10 · El máximo de EPA+DHA es semanal, no por menú

**Fecha:** 26 de agosto de 2026 (recogida aquí el 8 de septiembre).
**Caja:** **tope duro**, aplicado en la base correcta.
**Estado:** cerrado salvo ficha.

**Qué se decidió.** El máximo de EPA+DHA **se quita de
`requerimientos_v2_final.json`** y vive en el **promedio de la rotación
semanal**, en el presupuesto de `/menu/semana`.

**Los dos motivos:**

1. **FEDIAF 2025 deja la columna Maximum VACÍA para EPA+DHA.** No hay máximo.
2. Los 2.800 mg de Lenox & Bauer (JVIM 2013;27:217-226) son el **SUL del NRC
   2006**, o sea una concentración de la **dieta habitual crónica**, no el tope
   de un plato.

**Y la medida que lo cierra:** puesto como máximo por menú, **18 de los 20
pescados del catálogo lo pasan ellos solos** (solo el bacalao, 1.928, y el
pulpo, 2.527, quedan por debajo; el boquerón llega a ~11.000 mg/1000 kcal),
porque el pescado tiene mucho omega-3 y pocas calorías. El tope por menú
**borraba el pescado azul entero del catálogo**: los menús con pescado bajaron
de 13 de cada 24 a 4.

**Dónde vive:** `seguridad.TOPE_EPA_DHA_SEMANAL_KCAL = 2.8`.
**Test:** BLOQUE 21.

**Nota:** el **mínimo** de EPA+DHA de adulto (0,11 g) tampoco es de FEDIAF
—FEDIAF dice literalmente que «the current information is insufficient to
recommend a specific level of omega-3 fatty acids for adult dogs»—: viene del
NRC 2006 y **se adopta a propósito** por su relevancia clínica documentada.
Eso lo hace **criterio nuestro** y está escrito en el `nota_auditoria` de la
fila. Va a `PREGUNTAS_ABIERTAS.md` P-05 para que el nutricionista lo vea.
## D-11 · El DER, cerrado contra FEDIAF 2025

**Fecha:** 8 de septiembre de 2026.
**Caja:** **tope duro** donde FEDIAF publica cifra; **rango clínico** en nada
(el DER no es un límite: es una estimación de partida).
**Estado:** **cerrado salvo ficha** — vive en el repo, cada cifra con su tabla
citada, protegido por el BLOQUE 54 y por el contrato de 100 casos, escrito
aquí, y sus preguntas están en `PREGUNTAS_ABIERTAS.md` con dueño.

### La regla que decide, y de quién es

**FEDIAF manda. Donde FEDIAF no llega, SACN5.** Es criterio de producto de
Elena, tomado el 8 de septiembre: FEDIAF es la referencia europea y es la que
aplica a quien usa la app. No se vuelve a discutir salvo por la regla de
reapertura del §0.

### Qué se verificó, y contra qué

Hasta hoy el DER solo estaba comprobado contra `der_casos.json`, que garantiza
que los dos repos calculan **lo mismo** — no que lo que calculan sea lo que
dice la fuente. Se abrió el PDF de FEDIAF 2025 (Tablas VII-7 y VII-8b), SACN5
(Tabla 5-2) y AAHA 2021.

**Lo que ya estaba bien, y ahora consta:**

| Qué | Contra | |
|---|---|---|
| Los 5 escalones de actividad: 95 · 110 · 125 · 150 · 175 | **FEDIAF VII-7** | exactos |
| La ecuación de crecimiento `(1,063 − 0,565 × frac) × kg^0,75` MJ | **FEDIAF VII-8b** | **es la de FEDIAF**, que cita a Klein 2019. Su forma en kcal, `[254,1 − 135,0 × frac] × kg^0,75`, es la misma ×239 |
| Gestación: 132 × kg^0,75, y +26 × kg las últimas 5 semanas | **FEDIAF VII-8b** | exacta |
| Lactancia: `145 × kg^0,75 + 24n × kg × L` (1-4) y `+ [96+12(n−4)] × kg × L` (5-8), con L = 0,75 / 0,95 / 1,10 / 1,20 | **FEDIAF VII-8b** | **exacta, letra por letra** |
| Adelgazar: RER del peso ideal (1,0 × RER) | SACN5 Tabla 5-2 («Weight loss = 1.0 x RER») | coincide, y es más estricto que el «obese prone ≤ 90» de FEDIAF |
| RER = 70 × kg^0,75 | Convención universal | — |

### Los tres cambios que se aplican, y por qué

**1 · Se quita el tope de ×6 RER en lactancia.**

FEDIAF (VII-8b) **no pone ningún techo** a esa fórmula. El que había salía de
SACN5 Tabla 5-2, donde el ×6 **no es un techo general: es la fila de camadas
de ≥9 cachorros**. Se estaba usando una fila de una tabla indexada por tamaño
de camada como si fuera un límite universal.

**Y recortaba de verdad.** Medido en semana 4:

| Perra | Cachorros | FEDIAF | Se daba | |
|---|---|---|---|---|
| 25 kg | 6 | 5221 kcal | 4696 | −10 % |
| 40 kg | 8 | 9218 kcal | 6680 | −28 % |
| 60 kg | 8 | 13 494 kcal | 9054 | **−33 %** |

⚠️ **Y el comentario que lo justificaba decía dos cosas falsas**: que la
fórmula venía «de una fuente secundaria que no se ha podido contrastar con el
texto original de FEDIAF» (sí se puede, y cuadra), y que el ×6 era «el máximo
de la tabla clínica» (es una fila, no un máximo). Un comentario que declara no
verificado algo que sí lo está es peor que no tenerlo: nadie vuelve a mirarlo,
y aquí además se usó para justificar el recorte.

**2 · Se adoptan las dos razas con cifra propia de FEDIAF.**

La Tabla VII-7 termina con una sección «Breed specific differences»:
**Great Danes 200 (200-250)** y **Newfoundlands 105 (80-132)** kcal/kg^0,75.
Las dos razas están en la lista de 136 de la app y **el motor no las usaba**.

Medido: un Gran Danés de 67,5 kg marcado como «normal» recibía **2590 kcal
donde FEDIAF dice 4710 — el 55 %**. Un perro así adelgaza.

Y 200 no es un valor extremo: SACN5 cap. 5 dice que las estimaciones de DER en
perro *«range between 95 to 200 kcal … per (BWkg)0.75 per day»*.

⚠️ **Cómo se aplica es interpretación nuestra**, y va declarada: FEDIAF pone
las dos filas dentro de la tabla de actividad, con valor central y rango, pero
sin cruzarlas con los cinco niveles. Se hace así: el valor central sustituye a
la base de «normal», el nivel de actividad sigue moviendo su diferencia contra
«normal», el ±15 de Thes 2014 **no** se suma encima (estas razas ya tienen su
propia cifra medida), y el resultado se recorta al rango que publica FEDIAF.
La pregunta de si eso es lo que FEDIAF quiere decir: `PREGUNTAS_ABIERTAS.md`
P-11.

**3 · El respaldo de crecimiento pasa a la regla de SACN5, por edad.**

Había una tabla de tres escalones por % del peso adulto —210 / 175 / 140— y
**el código leía SIEMPRE el último, en los dos repos**: dos de las tres filas
eran código muerto. O sea que un cachorro de dos meses sin peso adulto
esperado recibía 140 (= 2 × RER), que es lo que corresponde **después** de los
cuatro meses. Un 33 % menos.

FEDIAF no cubre este caso —su ecuación necesita el peso adulto esperado—, así
que manda SACN5 (Tabla 5-2, parte 2 canina), literal: *«Daily energy intake
for growing puppies should be 3 x RER from weaning until four months of age.
At four months of age energy intake should be reduced to 2 x RER until the
puppy reaches adult size.»* Dos escalones, y cortan **por edad**. Sin edad ni
peso adulto se queda en 140, que es el lado prudente.

Y el 175 (2,5 × RER) **no está en FEDIAF ni en SACN5**: era nuestro, y se va.

### Qué protege esto

- **BLOQUE 54**, nuevo: comprueba los cinco escalones contra VII-7, las dos
  razas y su rango, que la fórmula de lactancia siga siendo la de VII-8b, que
  `LACTANCIA_TOPE_RER` no vuelva, que el respaldo de crecimiento sea el de
  SACN5, y la gestación. **Probado con el fallo puesto por tres lados
  distintos**: devolviendo el tope, quitando el Gran Danés y quitando el
  escalón de los 4 meses. Los tres se cazan.
- **`der_casos.json`, de 85 a 100 casos**, con los dos repos idénticos
  (md5 comprobado): se añadieron las dos razas en los cinco niveles, un Boxer
  de control (para que el ±15 de Thes no se contamine), y cuatro casos de
  lactancia sin tope. Cambiaron 5 de los 85 originales, todos de lactancia, y
  todos son los que el tope recortaba.

⚠️ **Lo que el contrato NO puede cubrir, y consta en el propio fichero:** los
casos con `mesesEdad`. `der.py`, al recibir la edad, **deduce** el peso adulto
con `peso_adulto_desde_curva` y pasa a la ecuación de Klein; `der.js` no tiene
esa función (la app deduce el peso adulto por su cuenta y lo pasa ya hecho).
Con la edad, los dos toman caminos distintos **a propósito**, y un caso así no
puede vivir en un contrato compartido. Ese camino se prueba en cada lado por
separado.

### Lo que queda abierto, y no impide cerrar esto

`PREGUNTAS_ABIERTAS.md` P-11 (cómo cruzar las razas con la actividad), P-13
(a ≤ RER, AAHA recomienda dieta terapéutica), y la de si la app debería dar
menú automático en lactancia. Son preguntas **para el nutricionista**, no
huecos de verificación: los números están donde dice la fuente.

---

## D-12 · Cuándo se puede salir de un límite, y quién puede

**Fecha:** 8 de septiembre de 2026.
**Estado:** **cerrado** como marco (es un hecho documentado, no un criterio
nuestro). Lo que cuelga de él —clasificar cada límite— es trabajo, y está en
`ESTADO.md`.

### La pregunta

¿Existe alguna fuente que diga **qué límites son rígidos y cuáles quedan a
criterio profesional**? Hasta hoy lo más cercano era implícito: FEDIAF marca
sus máximos como `(L)` legal o `(N)` nutricional, NRC define el *Safe Upper
Limit*, y SACN5 llama a lo suyo *«key nutritional factors and their target
levels»* y enumera siete cosas que los mueven.

**Sí existe, es explícito, es europeo y es ley.**

### Lo que dice FEDIAF de su propio alcance

Dos frases de su sección de alcance, literales, que hasta hoy no estaban
recogidas en ninguna parte del repo:

> *«Pet foods can be adequate and safe when nutrient levels are **outside the
> recommendations in this guide**, based on the manufacturer's substantiation
> of nutritional adequacy and safety.»*

> *«**Excluded from the FEDIAF's Nutritional Guidelines are pet foods for
> particular nutritional purposes** and some other specialised foods… specific
> products **may have nutrient levels that are different from those stated in
> these guidelines**.»*

Y sobre las dietas de eliminación:

> *«Through veterinarians, special diets… are available for dogs and cats
> suffering of adverse reactions to food; the formulation and the label
> declarations for those foods are **regulated by the specific EU legislation
> on dietetic foods for animals**.»*

O sea: **los requisitos de FEDIAF son los del alimento completo de un animal
sano, y salirse de ellos tiene una vía legal con nombre.**

### La vía: Reglamento (UE) 2020/354

Establece la lista de **objetivos nutricionales particulares** (los llamados
alimentos dietéticos o PARNUT) y deroga la Directiva 2008/38/CE. Su Anexo,
parte B, es una tabla con estas columnas exactas:

> *Entry number · **Particular nutritional purpose** · **Essential nutritional
> characteristics** · Species or category of animal · Labelling declarations ·
> **Recommended length of time** · Other provisions*

Es decir, para cada motivo clínico: **qué se le permite hacer al alimento, con
qué cifra, durante cuánto tiempo, y qué hay que declarar.** Y la frase que
aparece en las entradas caninas:

> *«It is recommended that advice from a veterinarian be sought before use and
> before extending the period of use.»*

### La regla que sale de ahí, y que se adopta

| Nivel | Qué es | ¿Se puede salir? |
|---|---|---|
| **Límite legal `(L)` de FEDIAF** | Ley de la UE sobre aditivos (Reg. 2017/1492): cobre, yodo, hierro, manganeso, selenio, zinc, vitamina D | **NO. Nadie, tampoco el veterinario.** Es ley y aplica también al alimento dietético |
| **Requisito de FEDIAF** (mínimos y máximos `(N)`) | La referencia del **alimento completo para un animal sano** | **SÍ**, por dos vías: la sustanciación del fabricante, o un **objetivo nutricional particular del Reg. 2020/354** — que lleva cifra, duración y consejo veterinario |
| **Objetivo de SACN5** (*key nutritional factor*) | Objetivo terapéutico, con rango a propósito | **SÍ**, criterio clínico dentro del rango que da la fuente |
| **Criterio nuestro** | Sin fuente veterinaria detrás | Se puede cambiar, pero va **declarado como criterio** |

**Y hay una frontera práctica que ya usa el motor y ahora tiene respaldo
legal:** un objetivo terapéutico **por encima** del mínimo de FEDIAF se puede
formular como alimento completo; uno **por debajo** es prescripción y necesita
firma. Eso es exactamente lo que hace `necesita_bajo_fediaf`, y coincide con
cómo el reglamento separa sus dos vías para el urato (≤130 g/kg de proteína,
que cae bajo el mínimo de FEDIAF, frente a ≤220 g/kg con fuentes
seleccionadas, que no).

### El puente de 4000 kcal/kg MS no queda «validado»: lo manda la propia ley

*(Corregido el 8 de septiembre, tarde, al leer el PDF oficial. La primera
redacción de este apartado lo deducía de que la entrada de convalecencia pide
≥3520 kcal = 0,88 × 4000. La deducción era correcta pero innecesaria: **el
reglamento lo dice con todas las letras en su nota al pie (2)**.)*

> *«based on a diet with a dry matter energy density of **4000 kcal Metabolisable
> Energy/kg** calculated using the equation described in the **FEDIAF Nutritional
> Guidelines**… **The values shall be adapted if the energy density deviates from
> the 4000 kcal Metabolisable Energy/kg.**»*

Tres cosas de una sola frase:

1. La densidad de referencia es 4000 kcal EM/kg de materia seca — la misma que
   NRC 2006, la misma que FEDIAF, la misma que usa el repo.
2. La ecuación de energía que manda usar es **la de FEDIAF**, no otra.
3. **«The values shall be adapted»**: adaptar las cifras cuando la densidad se
   desvía no es una licencia que nos tomemos, es una obligación de la norma. Una
   ración BARF no tiene 4000 kcal/kg MS, así que leer el anexo sin convertir
   sería leerlo mal.

```
1 kg de pienso al 12 % de humedad = 0,88 kg MS
0,88 × 4000 = 3520 kcal/kg de pienso   →   por 1000 kcal = valor por kg ÷ 3,52
```

**Trampa, y ya mordió una vez:** la nota al pie **(12)** cambia la base a **3500
kcal/kg MS** → divisor **3,08**. En la lista canina la usa **solo la entrada 22,
hiperlipidemia**. La primera versión de esta comparación aplicó 3,52 a esa fila y
dio «grasa legal 31,25 g/1000 kcal»; **la cifra correcta es 35,7 g**. La
conclusión no cambia (el motor pone 30, más estricto que las dos), pero el número
estaba mal y queda corregido aquí y en `PARA_EL_NUTRICIONISTA.md` §8.1-quater.

### Dos frases más del reglamento que respaldan reglas que ya tenía el motor

**Un techo terapéutico no autoriza a bajar de los mínimos de FEDIAF** — nota al
pie (11), colgada del tope de grasa de la entrada 22:

> *«The minimum recommendations according to the FEDIAF Nutritional Guidelines
> for all essential fatty acids shall be met in the daily ration.»*

Es la **regla 3 de `CLAUDE.md`** —lo que se relaja es la forma, nunca la
nutrición— escrita en el Diario Oficial.

**Con dos patologías se cumplen los dos topes** — parte A, punto 7:

> *«Where a feed intended for particular nutritional purposes is intended to meet
> more than one particular nutritional purpose, **it shall comply with each
> respective entry** in Part B.»*

Respalda dos cosas del motor a la vez: que renal + pancreatitis aplique los dos
topes simultáneamente en vez de promediarlos, y que la respuesta correcta cuando
no caben juntos sea **decir qué dos límites chocan** (BLOQUE 52) en lugar de
aflojar uno por su cuenta.

### El único porcentaje del texto NO es un margen clínico

Parte A, punto 2:

> *«…a technical deviation of **+/- 15 %** shall be permitted.»*

Es la **tolerancia analítica de fabricación** frente a lo que declara la etiqueta,
cuando el anexo IV del Reg. 767/2009 no fija una. Citarlo como «el veterinario
puede subir un 15 %» sería un error, y es un error fácil de cometer porque es el
único número con pinta de margen en toda la norma.

### Dónde vive la fuente

`canislab-fuentes/Reglamento_UE_2020_354/` — PDF oficial del Diario Oficial en
castellano y en inglés, texto extraído, y una `LECTURA.md` con las **20 entradas
caninas** de la parte B, su cifra convertida a por-1000-kcal, y el reparto de qué
contesta y qué no. Descargado del *cellar* de la Oficina de Publicaciones
(`publications.europa.eu/resource/celex/32020R0354`): EUR-Lex por navegador está
detrás de un desafío anti-bot que devuelve 202 con el cuerpo vacío.

### Lo que NO cierra esto

El marco dice **quién puede salirse y por qué vía**. No dice **hasta dónde**
en cada caso concreto: eso sigue siendo la ficha de permisos, y sigue
necesitando al nutricionista para los rangos. Ver `PREGUNTAS_ABIERTAS.md`
P-02 y P-03.

Dicho con precisión, porque es fácil citar esta fuente de más: **el reglamento no
da, por patología y por nutriente, un rango con un extremo que el veterinario
pueda mover.** Da, para cada uno de los 20 objetivos caninos, **una sola
característica nutricional esencial** — casi siempre un techo, a veces un suelo —
y le asigna al veterinario un papel distinto y explícito, que es el de decidir
**empezar** y decidir **prolongar**:

> *«It is recommended that advice from a veterinarian be sought **before use and
> before extending the period of use**.»*

Lo que la norma pone como rango es **el tiempo** (parte A punto 6: «indicates a
range within which the nutritional purpose should normally be achieved»), no la
cifra. El margen por nutriente, cuando existe, sigue viniendo de las tablas de
*key nutritional factors and their target levels* de SACN5 — que es donde una
fuente escribe un rango a propósito — y para los siete márgenes interpretados del
motor sigue sin respuesta: P-02.

---

## D-13 · Qué puede mover un profesional, y qué no

**Fecha:** 8 de septiembre de 2026.
**Estado:** **cerrado como criterio de producto.** Lo decide Elena; queda escrito
porque **invierte** el valor por defecto que fijaba `PROMPT_CIERRE_RAWKU_2.md`
(«el valor por defecto de `modificable_por` es **nadie**») para una clase concreta
de dato.

### La regla

> **Por defecto, un profesional acreditado puede mover cualquier valor de
> patología, en la dirección que sea.** Lo que no se mueve es lo marcado como
> legal o de seguridad. Cruzar un requisito de FEDIAF se puede, pero convierte el
> menú en prescripción firmada.

| Clase de número | ¿Se puede mover? |
|---|---|
| **Legal** — máximos `(L)` de FEDIAF (cobre, yodo, hierro, manganeso, selenio, zinc, vitamina D; Reglamento (UE) 2017/1492) y los cinco topes de seguridad crónica | **No.** Tampoco un veterinario: no puede autorizar más cobre del que permite la ley de aditivos |
| **Requisito de FEDIAF** — los mínimos de los 41 nutrientes, el ratio Ca:P | **Sí, pero deja de ser un menú.** El resultado es una prescripción firmada. El motor ya tiene el concepto: `necesita_bajo_fediaf` |
| **Tope o suelo de patología** | **Sí, libremente, en las dos direcciones** |

### Por qué se invierte el valor por defecto

No es laxitud: es fidelidad a la fuente. Verificando las once tablas de SACN5
que sostienen los topes del motor (ver `PATOLOGIAS.md`), **las fuentes casi nunca
dan un número: dan un rango.** «≤15 % o ≤10 % según el perro» en pancreatitis,
«10 a 15 %» en EPI, «100 a 200 mg/kg» en zinc, «0,4 a 1,1 %» en EPA. El número
único del motor **lo elegimos nosotros dentro de ese rango**, y en al menos un
caso —la grasa en obesidad, 30 en vez de los 22,5 de la fuente— por razones de
ingeniería, no clínicas: 22,5 no daba menú con el catálogo real.

Fijar el punto y no dejarlo mover es **menos fiel a la fuente** que dejarlo mover.

Y hay un argumento clínico que apunta igual: **apretar no es automáticamente el
lado seguro.** Está escrito en el `por_que` de `cardiopatia_c`: una restricción
severa de sodio puede activar el eje renina-angiotensina-aldosterona y empeorar
el pronóstico. Si ni siquiera «más estricto» es siempre mejor, no tenemos por qué
ser nosotros quienes fijemos el punto.

### Dos condiciones que no son burocracia

1. **Queda registrado**: quién, cuándo, de qué valor a qué valor, y sobre qué dato
   de entrada. Es lo que ya pedía la ficha de permisos.
2. **El menú se sigue verificando igual**, contra el juego de requisitos que
   resulte. **La regla 1 de `CLAUDE.md` no se toca**: ningún menú sale sin
   verificar, y un objetivo pedido por el profesional y no cumplido tiene que
   hacer que el menú **no salga** — no que salga verde porque el semáforo solo
   mira FEDIAF.

### Un matiz que hay que decir bien, o se cita de más

«Dentro de los márgenes legales» **no existe para la mayoría de patologías**. El
Reglamento (UE) 2020/354 pone cifra a 14 de sus 20 entradas caninas, y hay
patologías centrales que **no están en la lista**: la pancreatitis, la primera. Ahí
el único acotamiento real son los mínimos de FEDIAF y los topes de seguridad. Es
un margen ancho, y saberlo forma parte de usarlo bien.

### Qué queda abierto

**Hasta dónde** debería moverse cada valor sigue siendo criterio del nutricionista,
y ahora se sabe que **no hay fuente normativa que dé ese rango** (D-12). Los siete
márgenes «interpretados» de `PREGUNTAS_ABIERTAS.md` P-02 siguen sin respuesta, y
P-03 se cierra parcialmente: **quién** puede, sí; **hasta dónde**, no.
