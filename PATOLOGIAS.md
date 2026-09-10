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

## 0-pre · Qué significa aquí «verificado», y qué NO significaba

**Leer esto antes que nada.**

Las dos primeras pasadas de este documento comprobaron que **el número que aplica
el motor coincide con el de su fuente**. Eso es cierto y sigue siéndolo: las 57
cifras están comprobadas contra el texto literal.

**Pero eso no es lo mismo que haber recogido todo lo que la fuente dice**, y aquí
se llamó «verificado» a lo primero.

Lo destapó una pregunta de Elena sobre la pancreatitis: la Tabla 67-3 tiene **dos**
filas de grasa —≤15 % para el perro no obeso y ≤10 % para el obeso o
hipertrigliceridémico— y este documento citaba una diciendo «verificado literal».
No se escapó una tabla: se escapó media fila de la tabla que se estaba mirando.

Por eso hay una **tercera pasada**, en `VERIFICACION_FILA_A_FILA.md`: se leen
**todas** las filas de las 21 tablas y se dice qué se hace con cada una. Encontró
dos incoherencias más del mismo tipo —la obesidad mezclando los dos niveles de su
tabla, la artrosis aplicando 2 de 7 filas— y una lista de ocho cosas que faltan.

**Conclusión que hay que tener presente al leer lo que sigue:** ninguna cifra
aplicada está mal. Lo que estaba era **incompleto**, y en dos casos incoherente.
Son problemas distintos y el segundo no lo caza ningún test, porque un test
compara lo que hay contra lo que se declaró — no contra lo que la fuente dice
además.

---

## 0-ter · Dos errores propios en este documento, y qué se hizo para que no se repitan

**Encontrados el 8 de septiembre, segunda tanda, recalculando las 50 conversiones
del documento en vez de releerlas.**

| Dónde | Escrito | Correcto |
|---|---|---|
| Lisina en obesidad (§2.9) | 42,5 g/1000 kcal | **4,25** |
| Fenilalanina+tirosina en dermatosis (§2.13, §3.1) | 32,5 g/1000 kcal | **3,25** |

Los dos son el mismo fallo: multiplicar un porcentaje pequeño **por 25 en vez de
por 2,5**. Un factor 10.

**Ninguno llegó al motor**, porque eran cifras aún sin aplicar. Pero eso fue
suerte, no protección: se encontraron porque volví a mirar, y «volver a mirar» no
es un mecanismo. Un documento que dice estar verificado y contiene un factor 10 no
está cerrado.

**Lo que se cambió para que no dependa de que alguien multiplique bien:** cada
cifra del BLOQUE 55 lleva ahora, además del número y la cita, **el valor de la
fuente y su unidad de origen** (`pct_ms`, `mgkg_ms` o `directo`). El test rehace
la multiplicación y falla si no cuadra. Probado con los dos errores reales
reintroducidos: los caza los dos.

Las 23 cifras que sí están aplicadas en el motor tenían todas la conversión
correcta. Y hay una discrepancia que **no** es un error: el fósforo renal está en
1200 y el techo del rango de la fuente es 1250 — es una elección deliberada dentro
del rango, y por eso su origen va marcado como `directo` con el motivo escrito.

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

## 0-quater · Segunda tanda del 8 de septiembre: los huecos y seis patologías nuevas

**El motor pasa de 40 a 46 patologías, de 21 topes a 36 y de 9 suelos a 21.**
Todo verificado contra su fuente, con la conversión recalculada por el BLOQUE 55,
y todo medido: **cada una da menú verde en el peldaño estricto**.

### Los huecos rellenados

| Patología | Añadido | Cita | Medido |
|---|---|---|---|
| `renal` | potasio ≤ **2000** · proteína ≤ **62,5** | Tabla 37-9 «0.4 to 0.8%» · Reg. UE entrada 10 | potasio 1783 · proteína 62,4 |
| `obesidad` | fibra ≥ **30** · lisina ≥ **4,25** · L-carnitina ≥ **75** | Tabla 27-4 | fibra 30,4 · lisina 13,7 · carnitina 350 |
| `artrosis` | L-carnitina ≥ **75** | Tabla 34-2 | 121 |
| `enteropatia_cronica` | potasio ≤ **2750** | Tabla 57-1 «0.8 to 1.1%» | 2720 |
| `disfuncion_cognitiva` | vitamina E ≥ **187,5** | Tabla 35-3 «≥750 mg/kg» | 189,4 — **peldaño 5**, ver abajo |
| `dermatosis_zinc` y `dermatitis_atopica` | Phe+Tyr ≥ **3,25** | Tabla 32-1 «>1.3% DM» | zinc 26,6 · Phe+Tyr 8,0 |
| `cistina` | sodio ≤ **750** | Tabla 42-1 | (sigue no formulable) |
| `hepatopatia` | zinc ≥ **50** · hierro ≥ **20** · sodio ≤ **625** · taurina ≥ **250** | Tabla 68-8 | (sigue bloqueada) |

Tres cosas que salen de aquí y merecen leerse:

- **La proteína renal viene del Reglamento europeo, no de SACN5.** La restricción
  terapéutica de verdad (Tabla 37-9, «14 to 20%» = 35-50 g) está bajo el mínimo de
  FEDIAF y sigue necesitando firma. Los 62,5 del Reglamento sí caben, y **muerden**:
  una ración sin ajustar va por 130-150.
- **La lisina en obesidad es el único aminoácido concreto** que pide alguna de las
  quince tablas verificadas. Y es la cifra que escribí mal (42,5 en vez de 4,25).
- **El zinc en hepatopatía tiene 6,75 mg de margen hasta el techo legal** de FEDIAF
  (50 frente a 56,75). Es el límite más estrecho de todo el motor.

**Y una excepción medida:** la **disfunción cognitiva** es la única de todas que
**no resuelve en el peldaño estricto** — sale en el 5. Tiene sentido: 187,5 mg de
vitamina E por 1000 kcal son **27 veces** el mínimo de un perro sano, y con comida
sola no se llega; hace falta suplemento, y el peldaño 0 solo deja dos. Sale verde
con 189,4. Se acepta y **se dice**: un menú de disfunción cognitiva llevará más
suplementos y más vísceras de lo normal. Bajar el suelo para que saliera en el
estricto sería apartarse de la fuente.

### La estruvita pasa de bloqueada a formulable

Estaba en `formulable: false` con el motivo «dependen del pH urinario y de
analíticas que la app no puede ver» — cierto, **y escondía que la fuente da tres
cifras perfectamente formulables para la PREVENCIÓN**: magnesio ≤250, fósforo
≤1500, proteína ≤62,5 (Tabla 43-3). Las tres por encima del mínimo de FEDIAF.

**La disolución no se modela y se dice por qué**: pide magnesio <50, fósforo ≤250
y proteína ≤20 g, los tres muy por debajo de los mínimos. Eso es prescripción. Se
abre la prevención de recurrencia, no la disolución de un cálculo ya formado.

### Las seis patologías nuevas

| Nueva | Aplica | Medido |
|---|---|---|
| **Urolitos de fosfato cálcico** | fósforo ≤1500 · magnesio ≤375 · sodio ≤750 · proteína ≤62,5 | verde: 1229 · 226 · 500 · 62,4 |
| **Urolitos de sílice** | — (no formulable) | su único eje es proteína 25-45 g, bajo el mínimo de FEDIAF |
| **Estreñimiento crónico** | fibra ≥17,5 | verde: 27,6 |
| **Flatulencia excesiva** | proteína ≤75 · fibra ≤12,5 | verde: 72,1 · 0,2 |
| **SIBO** | grasa ≤37,5 | verde: 37,5 |
| **Intestino irritable** | fibra ≥20 | verde: 23,8 |

Y la estruvita abierta, medida: verde en peldaño estricto con magnesio 217,5, fósforo 1202,7 y proteína 61,2.

Con el fosfato cálcico **se completa la familia de urolitos**: ya están los cinco.
Y el propio capítulo 41 dice que sus recomendaciones son *«the same as for
prevention of recurrence of calcium oxalate uroliths»*, así que comparte casi todo
con el oxalato que ya estaba.

**Dos cosas que conviene saber de las nuevas:**

- **La flatulencia es de los topes que más mueven el menú de todo el motor.** Pide
  proteína ≤75 y una ración sin ajustar va por 130-150: casi el doble.
- **Flatulencia y estreñimiento son incompatibles entre sí**, y a propósito: una
  pide fibra ≤12,5 y la otra ≥17,5. Lo mismo con hiperlipidemia (≥25). No es un
  fallo — son dos objetivos clínicos opuestos, y el motor lo dirá nombrando los dos
  límites.

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

### 1.2 · El oxalato cálcico ✅ ARREGLADO — y la afirmación de partida era medio falsa

**Lo que decía este apartado el 8 de septiembre por la mañana:** «el oxalato no
ajusta nada; su único tope es la vitamina D, que ya es el máximo legal general».

**Media verdad, y hay que corregirla:** no aplicaba ningún tope **numérico**, eso
sí era cierto. Pero **sí excluía alimentos altos en ácido oxálico desde el 5 de
agosto** (`OXALATO_ALTO` en `motor/seguridad.py`), y esa exclusión nació de un
caso real idéntico al que yo describí: *«con oxalato cálcico avisa que no debería
dársele espinaca, y la mete en el menú de todas formas»*. Verlo antes de escribir
me habría ahorrado la afirmación.

**Lo que sí estaba mal, y ya está arreglado:**

| | Antes | Ahora | Fuente |
|---|---|---|---|
| Sodio | — | **≤ 750** mg | Tabla 40-5: *«Dietary sodium should be <0.3% DM»* |
| Fósforo | — | **≤ 1500** mg | Tabla 40-5: *«in the range of 0.3 to 0.6% DM»*, se aplica el techo |
| Magnesio | — | **≤ 375** mg | Tabla 40-5: *«in the range of 0.04 to 0.15% DM»*, se aplica el techo |
| Alimentos excluidos | 4 en la lista, **2 en el catálogo** | **20 en la lista, 16 en el catálogo** | Tabla 40-3, solo las marcadas (H) |
| Calcio | no se baja | **no se baja, y ahora se sabe por qué** | ver abajo |

Los suelos de los rangos (fósforo 750, magnesio 100) **no se aplican**: los dos
caen por debajo del mínimo de FEDIAF (1160 y 200), o sea que el requisito general
ya es más exigente que el suelo de la fuente.

**Medido en cinco pesos (5, 8, 22, 40 y 60 kg): verde en el peldaño estricto los
cinco**, con sodio 423-571, fósforo 1420-1499 y magnesio 202-225.

**El oxalato pasa a `solo_en_adulto`.** Lo cazó `auditar_patologias.py` en el
acto: 1500 mg de fósforo está **por debajo** del mínimo de FEDIAF en crecimiento
(2250 en CachorroJoven, 1750 en CachorroCrecimiento), así que en un cachorro no
sería un tope sino una prescripción. Clínicamente encaja — el oxalato cálcico es
enfermedad de perro adulto y maduro — y se suelta en crecimiento con su aviso,
nunca en silencio.

#### El conflicto del calcio, resuelto y verificado

Era el punto más incómodo de todo el documento: había un conflicto de fuentes
declarado y resuelto **a favor de una fuente que nadie había abierto**. Ya está
abierta.

- **SACN5 (2010), Tabla 40-5:** *«Restrict dietary calcium to 0.4 to 0.7% DM»*.
- **Cook A, Atiee GF, *Today's Veterinary Practice*, 10 de diciembre de 2025**
  (los dos DACVIM), literal: *«**Dietary calcium restriction does not appear to
  mitigate CaOx urolithiasis and is not recommended.**»*, citando a Carr et al.,
  J Vet Intern Med, marzo de 2020.

El mecanismo es el que ya estaba escrito: el calcio del intestino secuestra el
oxalato de la comida, y bajarlo **aumenta** la absorción de oxalato libre. Se
sigue la fuente de 2025. **El motor no baja el calcio, que es lo que ya hacía;
lo que cambia es que ahora se sabe por qué.**

La misma fuente da además un techo de sodio propio — *«avoid diets exceeding 120
mg/100 kcal»* = 1200 mg/1000 kcal — más laxo que el de SACN5. Se aplica el
estricto.

#### La lista de alimentos: de 4 a 20, y de dónde sale cada uno

La lista vivía en `seguridad.py` con cuatro entradas de conocimiento general
—espinaca, acelga, ruibarbo, remolacha— de las cuales **solo dos existen en el
catálogo**. La Tabla 40-3 de SACN5 tiene la lista de verdad y **la gradúa**:
`(H)` = *«high; avoid feeding»*, `(M)` = *«moderate; feed in limited amounts»*.

Se excluyen **solo las (H)**, que son las que la fuente manda evitar. En el
catálogo son 16: apio, berenjena, boniato, calabacín, espinaca, judía verde,
pepino, pimiento rojo, albaricoque, arándano, frambuesa, fresa, mandarina,
manzana, aceite de cacahuete, más la acelga que se conserva por criterio clínico.
Quedan **30 de las 45** fichas de «Verduras y frutas».

**Las (M) no se excluyen a propósito**, y una conviene conocerla: la **sardina**
es *«Sardines (M)»*, la única de la lista que no es verdura ni fruta. Las demás
(M) del catálogo son brócoli, espárrago, lechuga, pera, piña, tomate, zanahoria
y naranja.

Y la lista sigue viviendo **en un solo sitio**. Se llegó a escribir una segunda
copia en `patologias.json` y se retiró antes de commitear: sería exactamente cómo
se desincronizó la tabla de patologías del `POST /menu`.

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

### 1.4-bis · Los dos límites que se aplicaron el 8 y se retiraron el 9

**Añadido el 9 de septiembre de 2026, y es una rectificación, no un hallazgo
nuevo.** Los dos se aplicaron el 8 tras verificar su tabla, cada uno se midió
por separado y cada uno resolvía. Puestos a la vez con el resto del motor, los
dos dejaban **sin menú a perros de verdad** — que es peor que no haberlos
aplicado. Los dos pasan a `limites_escritos_que_el_solver_no_aplica`, con su
cita y su medida, igual que el omega-3 del cáncer.

| Límite | Lo que pide la fuente | Lo que da este catálogo | Qué pasaba |
|---|---|---|---|
| Disfunción cognitiva, **vitamina E** (Tabla 35-3) | ≥187,5 mg/1000 kcal | hasta ~180 con el fósforo por debajo de 2.000 | **SIN MENU a 8, 22 y 40 kg** — la patología entera dejaba de formular |
| Artrosis, **omega-3 totales** (Tabla 34-2) | ≥8,75 g/1000 kcal | ~6,5 fiable; 8,12 a veces | **SIN MENU de 25 kg en adelante** — el labrador con artrosis se quedaba sin menú y el yorkshire no |

**El de la vitamina E choca con otra cifra del MISMO libro**: el techo de
fósforo del perro adulto sano (2.000 mg/1000 kcal). Para llegar a 187,5 mg de
vitamina E hay que cargar de verdura y de hígado, y eso sube el fósforo.

**El del omega-3 no choca con nada: es que no hay catálogo.** La fuente más
concentrada es el aceite de linaza, y detrás la semilla de lino y el aceite de
hígado de bacalao; la carne no aporta prácticamente nada. Es el mismo motivo
por el que el 12,5 del cáncer tampoco cabe, y por eso el arreglo no es bajar el
número: es traer una fuente concentrada de EPA+DHA al catálogo.

**Lo que sí se sigue aplicando de las dos tablas**: en disfunción cognitiva, el
omega-3 ≥2,5 (peldaño estricto); en artrosis, EPA ≥1,0, L-carnitina ≥75,
vitamina E ≥67,1, fósforo ≤1.750 y sodio ≤1.000.

**Y lo que vigila que no vuelva a pasar**: el BLOQUE 61 de la batería recorre
las 39 patologías formulables y exige que cada una dé menú verde para el perro
de referencia. Hasta hoy nada comprobaba que «formulable» fuera verdad.

### 1.4 · Tres de los cuatro sodios cardíacos superan el techo legal europeo

Reglamento (UE) 2020/354, entrada 24: sodio ≤ 2,6 g/kg = **738,6 mg/1000 kcal**.
El motor: 900 (genérica), 900 (B2), 790 (C), 480 (D). Las tres primeras están
por encima.

No es una infracción nuestra —no vendemos pienso— pero sí significa que un menú
nuestro «para cardiópata» puede llevar más sodio del que Europa admite para
llamarse dieta cardíaca. Ver `DECISIONES.md` D-12.

### 1.5 · ~~La pancreatitis usa Merck cuando la regla adoptada manda SACN5~~ ✅ ARREGLADO

**Aplica hoy:** grasa ≤ **37,5** g/1000 kcal, y **25** si además está marcada
obesidad o hiperlipidemia. **Lo que decía esta línea hasta el 10 de septiembre:**
«grasa ≤ 20 g/1000 kcal» — la cifra de antes del arreglo, tres párrafos por
encima de la frase «Aplicado el 8 de septiembre: 20 → 37,5» que lo desmiente.
Un apartado que se arregla y conserva su cabecera de «esto está mal» miente en
la primera línea, que es la única que mucha gente lee.
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

**Y por qué NO se usa el 20 de Merck, aunque venga en la unidad correcta.** Es la
objeción más fuerte que tiene esta decisión y merece estar escrita: los 20 de
Merck vienen ya en **g/1000 kcal**, la unidad del motor, así que son **inmunes al
puente de 4000 kcal/kg de materia seca**. Los 37,5 no: salen de convertir «≤15 %
MS» y dependen de esa asunción. La fuente que se descartó estaba en mejor unidad
que la que se adoptó.

Se mantiene SACN5 por tres razones, en orden de peso:

1. **No sería una decisión sobre la pancreatitis, sería sobre el método.** Adoptar
   «prefiero la fuente que ya viene en g/1000 kcal» afectaría a casi todas las
   cifras del motor, porque casi todas salen de SACN5 en porcentaje de materia
   seca. Cambiaría la regla de fuentes por una regla de unidades.
2. **La unidad no dice nada de la calidad.** Merck es un manual terciario:
   resume literatura, no mide, y **no cita estudio** para esta cifra. (Cuidado con
   una confusión fácil: el «Sanderson et al. 2001, 20 g/1000 kcal» que aparece en
   `VETERINARIOS.md` es de **proteína**, no de grasa. Coincidencia numérica.)
3. **SACN5 gradúa y Merck no** — ver justo abajo, que es lo que esta objeción
   acabó destapando.

Y medido, la asunción juega a favor: el menú de pancreatitis tiene una densidad
estimada de **3674 kcal/kg MS**, no 4000, así que «≤15 % MS» equivaldría a **40,8**
y aplicamos **37,5**. Somos más estrictos que la fuente, y es autocorrectivo: al
apretar la grasa baja la densidad y la cuenta se vuelve más conservadora.

#### El hueco que destapó: no aplicábamos la graduación

La Tabla 67-3 dice **dos** cosas y el motor aplicaba una:

> *«Fat ≤15% for non-obese and non-hypertriglyceridemic dogs»* → **37,5**
> *«≤10% for obese and/or hypertriglyceridemic dogs»* → **25**

**El perro obeso o hipertrigliceridémico recibía el tope del perro delgado** — y
es el de más riesgo, porque la hipertrigliceridemia **causa** pancreatitis, no
solo la acompaña. Antes de hoy se quedaba en 30, el tope de `obesidad`, cuando la
fuente pide 25.

Arreglado el 8 de septiembre. Hubo que **crear el mecanismo**: existía el
condicional para el % de kcal de grasa (`max_pct_kcal_grasa_si_ademas`) pero no
para un tope absoluto; ahora existe `topes_por_1000kcal_si_ademas`, con la misma
forma y la misma regla — se combina con `min()`, así que solo puede apretar.

| Combinación | Grasa aplicada |
|---|---|
| pancreatitis sola | 37,5 |
| **pancreatitis + obesidad** | **25** |
| **pancreatitis + hiperlipidemia** | **25** |
| obesidad sola | 30 |


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

- **Aplica:** grasa ≤ **37,5** g —y **25** si además está marcada obesidad o
  hiperlipidemia— y proteína ≤ **75** g/1000 kcal.
  ⚠️ **Corregido el 10 de septiembre:** esta ficha decía «grasa ≤ 20 g», que era
  la cifra de Merck de antes del 8 de septiembre. El motor lleva desde entonces
  aplicando las dos de SACN5 Tabla 67-3 (*«Fat ≤15 % for non-obese and
  non-hypertriglyceridemic dogs»* y *«≤10 % for obese and/or hypertriglyceridemic
  dogs»*), y ni el §1.5 de este documento ni el aviso que lee el usuario se
  habían actualizado. Es justo por esto que el margen del profesional dejó de
  vivir en prosa: ahora está en el bloque `margen_profesional` de cada cifra y lo
  rehace el BLOQUE 80.
- **Fuente de la grasa:** SACN5 Tabla 67-3 (ver §1.5; Merck queda como
  referencia más estricta, no como el valor aplicado). **De la proteína:** SACN5 Tabla 67-3,
  *«Protein 15 to 30% for dogs»* → 37,5-75 g; usamos el extremo alto.
  El motivo está en el propio texto y no es obvio: *«Free amino acids (i.e.,
  phenylalanine, tryptophan and valine) in the duodenum are a strong stimulus for
  pancreatic secretion, in fact, more so than fat»* — el exceso de proteína
  estimula el páncreas **más que la grasa**.
- **Techo duro:** grasa, mínimo FEDIAF **13,75**; proteína, mínimo FEDIAF
  **52,1**. Ni FEDIAF ni el Reglamento 2020/354 cubren la pancreatitis, así que
  **no hay techo legal por arriba**: el margen hacia arriba solo lo acota el
  criterio.
- **Margen del profesional:** grasa **13,75 → sin techo legal**; proteína
  **52,1 → 75**. Es la ventana que sirve hoy `GET /patologias`, rehecha contra la
  fuente viva por `auditar_margen_profesional.py`.
- ⚠️ **Frontera física medida:** por debajo de ~26-28 g de grasa no hay menú con
  el catálogo real. Los 20 de Merck estaban **por debajo** de esa frontera, y es
  la otra mitad del motivo por el que se cambiaron.

### 2.4 · Cálculos de oxalato cálcico · `oxalato`

Ver §1.2. **Aplica** (actualizado el 9 de septiembre): vitamina D ≤ **8,75 µg**,
fósforo ≤1500, sodio ≤750 y magnesio ≤375, todos por 1000 kcal.

- **La vitamina D bajó de 14,1875 a 8,75 el 9 de septiembre.** El 14,1875 era el
  máximo **legal** de FEDIAF para cualquier perro, o sea que esta patología no
  tenía tope propio de vitamina D: tenía el de todo el mundo escrito en su ficha,
  que parece un límite y no lo es. La cifra nueva es de Fascetti cap.16, literal:
  *«Diets with vitamin D between 250 and 350 IU/Mcal should suffice»* = 6,25-8,75
  µg/1000 kcal, y se aplica el extremo alto, que es el techo.
- **Medido antes de aplicarlo:** cinco perros (3, 8, 20, 30 y 55 kg) con oxalato
  marcado dan menú en el peldaño **estricto**, con 4,08-5,72 µg reales — por
  debajo incluso del extremo bajo del rango de la fuente.
- **Techo duro:** por arriba sigue estando el legal (14,1875), que nadie mueve.
  Por abajo, el mínimo de FEDIAF (3,975 en adulto).
- **Margen del profesional:** **3,975 → 14,1875**, y el motor se queda en 8,75.

**Y cuatro cosas que la fuente dice y el motor NO aplica**, escritas en
`patologias.json` bajo `limites_escritos_que_el_solver_no_aplica` y con pregunta
abierta en `PARA_EL_NUTRICIONISTA.md` §11-bis: la **proteína** (10-18 % MS, que
cae entera por debajo del mínimo de FEDIAF), el **suelo** de fósforo (750) y el
de magnesio (100), que no aplican porque los mínimos de FEDIAF ya son más altos,
el **conflicto de fuentes del fósforo** (Fascetti dice que NO se restrinja y que
el fósforo bajo es factor de riesgo), el **debate del sodio** (la misma fuente
dice que el sodio bajo aumenta el riesgo) y el **ácido ascórbico**, que es una
regla sobre ingredientes y no un número.

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
- **La metionina (9 de septiembre): no hay techo que poner.** El NRC avisaba con
  un experimento de dosis (Merino 1975: 1 g/kg cada 4 h dio signos de coma
  hepático en perros con shunt portocava), pero **SACN5 cap.68 dice que esa vía
  no importa** — *«these compounds do not play an important role in the
  pathogenesis of HE»* — y que lo que hay que hacer es *«do not administer…
  **methionine-containing products**»*. Es una **exclusión de suplementos**, no
  un límite por nutriente. Hoy no hay nada que excluir (el catálogo no tiene
  ficha de L-metionina); el día que entre, esta patología tiene que excluirla, y
  está escrito en `patologias.json`.

### 2.6 · Cardiopatía · `cardiopatia`, `_b1`, `_b2`, `_c`, `_d`, `_a`

- **Aplica:** sodio ≤ **738,6** (genérica y B2), **625** (C), **480** (D). B1 y A
  sin tope, a propósito.
- **Fuente real:** Cavanaugh SM, Veterinary Practice News, 6-jul-2020 (ver §1.1).
  ACVIM 2019 **no da cifras**. SACN5 Tabla 36-4 sí, pero con otra clasificación
  (ISACHC, no ACVIM): *«Class Ia = 0.15 to 0.25%»* = 375-625 mg y
  *«Class Ib, II and III = 0.08 to 0.15%»* = 200-375 mg. **No son intercambiables
  grado a grado**, y por eso no se sustituyeron.
- **Techo duro:** por abajo, mínimo FEDIAF **290 mg**. Por arriba, Reglamento
  2020/354 entrada 24, **738,6 mg**.
- **Margen del profesional:** **290 → 738,6**. Tres de nuestras cuatro cifras están
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
  *«Lysine ≥1.7%»* = **≥4,25 g**; *«L-carnitine ≥300 ppm»* = **≥75 mg**;
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
  *«Phenylalanine + tyrosine >1.3% DM»* = **>3,25 g**, y *«Avoid excess copper
  (copper <200 mg/kg food DM)»*. También avisa de que *«Higher levels of zinc are
  required in foods with calcium >1.5% DM»* — o sea que en una ración BARF con
  mucho hueso, 25 mg puede no bastar. Eso no lo mira nadie.

### 2.14 · Diabetes mellitus · `diabetes`

- **Aplica:** excluye fruta, y grasa ≤30 % de las kcal **solo si además** hay
  pancreatitis o hipertrigliceridemia (fuente: Purina Institute — **no
  verificada** contra el documento original, ver §4).
- **Fuente principal, verificada:** SACN5 Tabla 29-3, perros:
  *«Fiber 7 to 18%»* = **17,5-45 g**; *«Fat <25%»* = **<62,5 g**;
  *«Protein 15 to 35%»* = 37,5-87,5 g; *«Provide foods with no more than … 55% digestible carbohydrate»*; *«Avoid simple sugars»*.
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

1. ~~La estruvita de prevención es formulable y está bloqueada.~~ ✅ **Abierta el
   8 de septiembre.** Sus tres cifras están por encima del mínimo de FEDIAF, y el
   Reglamento (entradas 17 y 18) coincide: magnesio ≤511 mg, más laxo que los 250
   de SACN5 que se aplican.
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

De las 40 patologías de entonces, 21 no aplicaban ningún número (hoy son 47 y 18). **No es lo mismo «la fuente no
da número» que «no hemos mirado».** Separado:

### 3.1 · Tienen tabla en SACN5 y NO la usamos

| Patología | Tabla | Lo que pide, verificado | Convertido |
|---|---|---|---|
| **`enteropatia_cronica`** | 57-1 (IBD) | *«Potassium 0.8 to 1.1%»* · *«Fat 12 to 15% for dogs»* (muy digestible) · *«Protein ≥25% for dogs»* · *«Crude fiber ≤5%»* o *«7 to 15%»* según enfoque | K **2000-2750 mg (con techo)** · grasa 30-37,5 · proteína ≥62,5 · fibra ≤12,5 o 17,5-37,5 |
| **`disfuncion_cognitiva`** | 35-3 | *«Vitamin E ≥750 mg/kg»* · *«Vitamin C ≥150 mg/kg»* · *«Selenium 0.5 to 1.3 mg/kg»* · *«L-carnitine ≥100 mg/kg»* · *«Total omegas-3 >1%»* · *«1% of each of five vegetable and fruit ingredients»* | vitE **≥187,5 mg** · vitC ≥37,5 · Se 0,125-0,325 · carnitina ≥25 · **ω-3 ≥2,5 g** |
| **`dermatitis_atopica`** | 32-1 | Las mismas de dermatosis: linoleico >1,0 % MS, fenilalanina+tirosina >1,3 % MS, digestibilidad MS >80 % | linoleico **>2,5 g** · Phe+Tyr **>3,25 g** |

**Los tres son implementables hoy** y ninguno baja del mínimo de FEDIAF. La
enteropatía crónica es la más llamativa: es una de las patologías más marcadas y
el motor no le ajusta nada.

### 3.2 · No tienen tabla de factores nutricionales clave en SACN5

Comprobado con un barrido de las tablas «Key nutritional factors» de la obra
⚠️ **que estaba cortado: eran unas 40 de las 89 que hay. Ver §0-quinquies**
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

## 3-bis · ¿Nos falta alguna patología? Barrido completo de las fuentes

**Hecho el 8 de septiembre**, a partir de un barrido de las tablas «Key nutritional factors» —
⚠️ **incompleto: unas 40 de 89, ver §0-quinquies** —
de SACN5 (barrido automático sobre los 70 capítulos) y las 20 entradas caninas del
Reglamento (UE) 2020/354.

### Las que SÍ tenemos

De las tablas caninas de SACN5, el motor cubre: obesidad (27-4), hiperlipidemia
(28-2), diabetes (29-3), dermatosis (32-1), dermatitis inflamatorias (32-6),
artrosis (34-2), disfunción cognitiva (35-3), cardiovascular (36-4), renal (37-9),
urato/purina (39-4), oxalato (40-5), cistina (42-1), estruvita (43-3), IBD (57-1),
colitis (62-1, dentro de `enteropatia_cronica`), PLE (58-1), EPI (66-1),
pancreatitis (67-3) y hepatobiliar (68-8). **Diecinueve.**

### Las que la fuente declara y el motor NO ofrece

| Tabla | Patología | Cifras que da | ¿Encaja en Rawku? |
|---|---|---|---|
| **41-6** | **Urolitos de fosfato cálcico** | proteína 10-25 % · Ca 0,4-0,7 % · P 0,3-0,6 % · **Ca:P 1,1-2:1** · Na <0,3 % · Mg 0,06-0,15 % · vit. D 500-1500 UI/kg | **Sí.** Es el quinto tipo de urolito y tenemos los otros cuatro |
| **44-1** | **Urolitos de sílice** | proteína 10-18 % MS · pH 7,1-7,7 · evitar corn gluten feed, cáscara de arroz y de soja | **Sí**, aunque los ingredientes que evita no existen en BARF |
| **64-2** | **Estreñimiento crónico** | **fibra ≥7 % MS = ≥17,5 g** · agua >75 % | **Sí.** Crónico, doméstico, y la fibra es directamente aplicable |
| **65-1** | **Flatulencia excesiva** | proteína ≤30 % = **≤75 g** · **fibra ≤5 % = ≤12,5 g** · evitar legumbres, lácteos, crucíferas, cebolla, frutos secos y fructosa | **Sí.** Es el motivo de consulta más común que no cubrimos |
| **60-1** | **Sobrecrecimiento bacteriano (SIBO)** | grasa 12-15 % = **30-37,5 g** · densidad 3,5-4 kcal/g MS | **Sí.** Y es complicación frecuente de la EPI, que sí tenemos |
| **63-3** | **Síndrome de intestino irritable** | fibra soluble 1-5 % · mixta 5-10 % · insoluble 10-15 % · **cruda ≥8 % = ≥20 g** | **Sí** |
| **59-1** | Síndrome de intestino corto | — | Postquirúrgico, hospitalario |
| **56-2** | Gastroenteritis aguda | sodio 0,3-0,5 % | Aguda, días. Es la entrada 21 del Reglamento |
| 50-3 · 50-4 | Deglución · esofagitis y reflujo | — | Hospitalario / dudoso |
| 52-2 | Gastritis y úlcera gastroduodenal | — | Dudoso |
| 54-2 | Motilidad y vaciado gástrico | — | Dudoso |
| 47-4 · 49-2 | Periodontal · enfermedades orales | — | No es cuestión de ración |

**Seis patologías con cifras aplicables que el motor no ofrece**, más otras siete
de contexto agudo u hospitalario que probablemente no deban estar.

Y del Reglamento europeo faltan tres purposes: **convalecencia (15)**, diarrea
aguda (21) y apoyo en estrés (30).

### Lo que esto NO es

No es una lista de deberes. **Añadir una patología es una decisión de producto**,
no de fuentes: la flatulencia tiene cifras y fuente, y aun así puede no querer
ofrecerse. Lo que sí era necesario era **saber que existen**, porque hasta hoy la
pregunta «¿nos falta alguna?» no tenía respuesta en ninguna parte.

Las tres que yo pondría primero, por este orden: **fosfato cálcico** (completa la
familia de urolitos, y sus cifras son casi las mismas que las del oxalato que ya
están aplicadas), **estreñimiento** (una sola cifra, la fibra) y **SIBO** (una
sola cifra, la grasa, y es complicación de una patología que ya tenemos).

---

## 4 · Las fuentes: todas abiertas ✅

**Estado al cierre del 8 de septiembre: no queda ninguna fuente de patología sin
verificar contra el documento original.** Eran cuatro.

| Número | Fuente | Estado |
|---|---|---|
| Grasa ≤37,5 en pancreatitis | SACN5 Tabla 67-3 | ✅ literal |
| Grasa ≤20 (la que se retiró) | Merck Veterinary Manual | ✅ literal: *«less than 20 g fat/1,000 kcal»*, cifra única, sin distinguir aguda de crónica |
| Sodio cardíaco | «ACVIM 2019 (Keene)» | ✅ abierto — **y no contiene las cifras**. La fuente real es Cavanaugh 2020 (§1.1) |
| **Cobre ≤2,4** | **Center SA et al., JAVMA 264(2), 2026** | ✅ **abierto**. El límite tolerable es **0,24 mg Cu/100 kcal = 2,40 mg/1000 kcal**, exactamente nuestro número, y el rango de dieta restringida del estudio es **1,50-2,40** |
| **Grasa <30 % ME en diabetes** | **Purina Institute** | ✅ **verificado** — y sale un matiz nuevo, abajo |
| **No bajar el calcio en oxalato** | **Cook & Atiee, Today's Veterinary Practice, 10-dic-2025** | ✅ **abierto**: *«Dietary calcium restriction does not appear to mitigate CaOx urolithiasis and is not recommended»* (§1.2) |

### Lo que apareció al abrirlas

**El cobre queda triplemente acotado.** Center 2026 da 2,40 como tolerable;
SACN5 Tabla 68-8 da 1,25 como objetivo terapéutico; el Reglamento (UE) 2020/354
pone el techo legal en 2,50. Nuestro 2,40 cae justo bajo el techo legal y justo
en el tolerable del estudio. El dato que lo motiva: **35 de 91 perros (38 %)**
con dieta comercial normal tenían rodanina positiva, y 20 (22 %) superaban el
límite de referencia de 400 µg/g de hígado seco.

**Y en la diabetes hay una excepción que el motor no aplica.** La frase de Purina
completa es: *«Dietary fat restriction (<30% of metabolizable energy) is
recommended for diabetic dogs with concurrent chronic pancreatitis or persistent
hypertriglyceridemia, **except for diabetic dogs in thin body condition**»*.

Esa última coma no estaba recogida. Un perro diabético **delgado** con
pancreatitis no debería llevar la restricción de grasa, y hoy se la lleva. La app
conoce la condición corporal, así que es implementable. Queda anotado; no se
cambia sin decidirlo.

La misma fuente da además la equivalencia *«<12 percent on a dry matter basis»*,
que es **exactamente** el tope de grasa de la hiperlipidemia de SACN5 (Tabla
28-2). Dos fuentes independientes llegan al mismo número por caminos distintos.

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
| oxalato | vitamina D 250-350 UI/Mcal (Fascetti, aplicado 9-sep) · fósforo 750-1500 · Ca:P 1,1-2:1 · sodio <750 · magnesio 100-375 · proteína 10-18 % MS · excluir oxálico y vitamina C |
| obesidad | ~~**proteína ≥62,5**~~ ✅ · fibra 30-62,5 · lisina ≥4,25 · L-carnitina ≥75 |
| artrosis | ~~L-carnitina ≥75~~ ✅ · omega-3 totales ≥8,75 → **escrito y NO aplicado** (ver §1.4-bis) |
| ~~PLE~~ | ~~**proteína ≥62,5** · fibra ≤12,5~~ ✅ |
| ~~EPI~~ | ~~fibra ≤12,5~~ ✅ |
| ~~diabetes~~ | ~~**fibra ≥17,5**~~ ✅ |
| enteropatía crónica | ~~grasa ≤37,5 · proteína ≥62,5~~ ✅ · potasio 2000-2750 · fibra |
| disfunción cognitiva | ~~omega-3 ≥2,5~~ ✅ · vitamina E ≥187,5 → **escrito y NO aplicado** (ver §1.4-bis) |
| dermatosis y atopia | ~~linoleico >2,5~~ (descartado: más laxo que FEDIAF) · fenilalanina+tirosina >3,25 |
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

**Verificar (fuentes sin abrir):** ✅ **ninguna.** Las cuatro se abrieron el 8 de
septiembre — ver §4.

**Lo que queda abierto, en una lista** *(⚠️ escrita por la mañana; los puntos 3
y 5 se cerraron ese mismo día — ver §0-quinquies al final)*:

1. **El oxalato en crecimiento.** Pasa a `solo_en_adulto` porque su tope de
   fósforo cae bajo el mínimo de un cachorro. Se suelta con aviso, que es lo
   correcto, pero un cachorro con oxalato no recibe ningún ajuste.
2. **La excepción del perro diabético delgado** (§4). Implementable: la app
   conoce la condición corporal.
3. **Seis patologías con cifras que la fuente declara y no ofrecemos** (§3-bis):
   fosfato cálcico, sílice, estreñimiento, flatulencia, SIBO e intestino
   irritable. Es decisión de producto, no de fuentes.
4. **Los siete «márgenes interpretados»** de `PREGUNTAS_ABIERTAS.md` P-02, donde
   la fuente da un solo número y el otro extremo lo pusimos nosotros.
5. **La ficha de permisos**, condición 3 de las seis del cierre. No existe.
6. **La humedad del catálogo** (`PARA_EL_NUTRICIONISTA.md` §10.0), de la que
   depende toda conversión desde porcentaje de materia seca.


---

# 0-quinquies · CUARTA PASADA (8 de septiembre, tarde)

**Este documento decía «las 21 tablas de SACN5 verificadas fila a fila». Eran
las 21 que yo había visto, y no son las que hay.**

El barrido que las encontró recortaba su propia salida con `sed -n '20,60p'`
para que cupiera en pantalla. **Hay 89 tablas «Key nutritional factors» en
SACN5.** Faltaban tres de patología canina, y una de ellas era de una patología
que el motor no ofrecía. No lo encontró una revisión: apareció leyendo el
capítulo 30 entero por otra cosa.

El relato completo, con la clasificación de las 89 y lo que se aplicó de cada
tabla, está en **`VERIFICACION_FILA_A_FILA.md` §cuarta pasada**. Aquí, el
resumen y lo que cambia en este documento.

## Lo que se aplicó

| Tabla | Patología | Qué |
|---|---|---|
| 30-5 | `cancer_soporte` (no aplicaba **nada**) | grasa ≥62,5 · proteína ≥75 · arginina ≥5. Y omega-3 ≥12,5 **escrito y no aplicado: medido, no cabe** |
| 32-6 | `dermatitis_atopica` | omega-3 total ≥0,875 |
| 31-3 | **`reaccion_adversa_alimento`, patología nueva (la 47)** | omega-3 ≥0,875 · fósforo ≤2000 · sodio ≤1000 (solo en adulto) · **atún y caballa fuera del menú** · proteína ≤55 escrita y no aplicada («dermatologic cases only») |

Más un aviso con fuente en `epilepsia_idiopatica`: SACN5 cap.28 documenta un
subgrupo —muchos schnauzer miniatura— con hipertrigliceridemia en el que *«dietary
therapy has successfully reduced blood triglyceride levels and eliminated
seizures without concomitant use of anticonvulsant drugs»*. Eso **sí** se
formula hoy: es la hiperlipidemia, que ya está en la lista.

## Y tres cosas que no son cifras

**1 · Un fallo del solver.** Los suelos por patología se exigían sobre las kcal
**pedidas** y `_tope_patologia_roto` los mide sobre las **reales**. Un menú puede
salir un 3 % por encima del DER, así que un suelo podía cumplirse para el solver
y no para el filtro final: medido, 61,6 g de grasa contra un suelo de 62,5, y el
cáncer sin menú en ningún peldaño por eso y solo por eso. Es el fallo del 21 de
agosto (el fósforo renal a 1426 con el tope en 1400) visto desde el otro lado.
Arreglado con `patologia_suelo_relativo`.

**2 · Un agujero de diseño en los avisos.** `patologias.py` solo dejaba pasar
cuatro claves de `avisos`; **cualquier otra se cargaba del JSON y no llegaba a
ningún sitio.** Texto escrito con su fuente que no leía nadie. Ahora hay
`avisos_extra`.

**3 · Un aviso mío que decía algo falso.** El de crecimiento de la artrosis
afirmaba que «los suelos de omega-3 y vitamina E sí se aplican igual» en un
cachorro. No se aplican: con `solo_en_adulto` se salta la patología **entera**.
Lo escribí describiendo lo que me parecía razonable en vez de lo que hace el
código. Corregido el texto; separar suelos de topes en crecimiento es decisión
clínica y está en `PENDIENTE_DECISIONES.md`.

## Lo que esta cuarta pasada deja abierto

1. **El fósforo del perro sano.** Los topes de fósforo y sodio de la artrosis
   (34-2) y de la reacción adversa (31-3) **son los del perro adulto sano**
   (13-3 y 14-2), repetidos por la comorbilidad de su población. Una ración BARF
   ronda los 4000 mg/1000 kcal y FEDIAF no pone máximo, así que el mismo perro
   pasa de 4000 a 1750 por marcar «artrosis». Tres salidas posibles, ninguna
   evidente: `PENDIENTE_NUTRICION.md` §14.3.
2. **Un concentrado de EPA+DHA en el catálogo.** Sin él, el omega-3 del cáncer
   no llega. Va en `DATOS_QUE_FALTAN.md`.
3. **El ratio omega-6:omega-3 y el NFE** (Tabla 30-5), que el motor no sabe
   expresar. El ratio se arregla con el mismo trabajo que el Ca:P por patología.
4. **La proteína de la reacción adversa**, que depende de si el perro reacciona
   por la piel o por el intestino — un dato que la ficha no pregunta.
