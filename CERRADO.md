# Lo que está cerrado

**Cerrado** no quiere decir «terminado» ni «bueno». Quiere decir una cosa muy
concreta: **que dejó de ser una pregunta abierta, y que reabrirlo tiene que ser
un acto consciente y no un descuido.**

Este archivo existe porque hasta el 8 de septiembre de 2026 no había forma de
saber si algo estaba cerrado. Cada sesión volvía a preguntarse lo mismo, y eso —
no la falta de trabajo — es lo que tenía el proyecto dando vueltas.

---

## Las seis condiciones

Vienen de `PROMPT_CIERRE_RAWKU_2.md` y hay que cumplir **las seis a la vez**:

| | Condición |
|---|---|
| 1 | Vive en el repo |
| 2 | Tiene fuente |
| 3 | Tiene ficha de permisos |
| 4 | Tiene un test automático que falla si se rompe |
| 5 | Está escrito como decisión, con fecha y motivo |
| 6 | No deja preguntas sin dueño |

**Cinco de seis no es cerrado.** Si falta una, está abierto, y aquí se dice cuál.

## Cuándo se puede reabrir

Solo por una de estas cuatro razones. Ninguna otra vale — y «no me acordaba»,
«un menú no salía» o «me pareció que estaba mal» no están en la lista:

1. **El nutricionista lo dice.**
2. **Aparece una fuente citable que lo contradice.** Citable: publicada,
   localizable y leída, no recordada.
3. **Un test o un caso real demuestra que está mal.**
4. **Cambia el alcance del producto.**

Al reabrir algo, se escribe **por cuál de las cuatro** y se actualiza aquí.

---

## ⚠️ REABIERTO OTRA VEZ · Los límites de patología

**Cerrado el 8 de septiembre de 2026 por la mañana. Reabierto esa misma tarde,
vuelto a cerrar por la noche, y REABIERTO EL 9 DE SEPTIEMBRE**, por la misma
razón 3 y por el mismo motivo de fondo que la primera vez: **el conjunto**.

### Por qué se reabre, con el número delante

Elena lo dijo así: *«no puedes decir que está cerrado si no te has leído el libro
completo, porque ese libro habla de patologías»*. Tiene razón, y medirlo lo deja
sin discusión:

| | |
|---|---|
| Tablas «Key nutritional factors» en SACN5 | **91** |
| Citadas en este repo | **32** |
| Sin citar | **59** |

De esas 59: **38** son comparativas de piensos comerciales contra la
recomendación (no traen requisito, esas sí son saltables), **10** son solo de
gato, y **11 son tablas de requisito canino o mixto que nadie ha mirado**.
Listadas una a una en `VERIFICACION_FILA_A_FILA.md` §quinta pasada.

**Y hay 26 capítulos de los 70 sin una sola cita en el repo.** El barrido de
agosto se hizo sobre tablas; la lección del 8 de septiembre fue que un barrido de
tablas no encuentra lo que la fuente dice en prosa —así salieron la arginina que
sube con la proteína, el ratio linoleico:linolénico y la proteína de la
lactancia—, y esa lección **todavía no se ha aplicado al libro entero**.

### Qué hace falta para volver a cerrarlo

Leer SACN5 **completo**, no sus tablas. Y antes, terminar FEDIAF: quedan el
glosario, la introducción, la guía 3.1, alimento complementario y **tres anexos
que sí tocan lo que hace el motor** — condición corporal (7.1), taurina (7.3) y
reacción adversa al alimento (7.6).

### ✅ LAS DOS COSAS ESTÁN HECHAS AL CERRAR EL 9 DE SEPTIEMBRE. LA DECISIÓN ES DE ELENA

Se dice con los números delante, y sin redondear a favor:

| | Estado |
|---|---|
| **FEDIAF 2025** | **Leída entera**, anexos incluidos. Los tres que faltaban dieron cosecha: del 7.1 salió la Tabla VII-2 y el BCS 9, que era el 40 % y son más del 45 |
| **Las 11 tablas caninas sin mirar** | **Leídas las once**, con su reparto escrito arriba: 1 aplicada, 1 sin nutrientes, 2 que no aplican y 7 de patologías que no ofrecemos |
| **Los 26 capítulos sin una sola cita** | **Leídos los 21 caninos, enteros.** Quedan 5 sin citar y los cinco son de otra especie: 22, 23 y 24 (gata y gatitos), 46 (tracto urinario felino) y 70 (pequeños mamíferos) |

Lo que la lectura completa encontró **fuera de las tablas**, que es la razón por
la que se exigió: el BCS 9 de FEDIAF, la arginina que sube con la proteína, el
ratio linoleico:linolénico, el +10 % de los aminoácidos, el techo de calcio del
cachorro de raza grande, el bromuro y el cloro del perro epiléptico, el mitotano
con comida, el ritmo de adelgazamiento y la excreción de patógenos. **Ninguna de
esas nueve estaba en una tabla de «Key nutritional factors».**

⚠️ **Y la parte que NO se cierra sola.** Los cinco capítulos que quedan son
felinos o de otra especie **según su título**, y este documento existe
precisamente porque «según parece» no vale. La diferencia con el error de agosto
es que allí se suponía que un barrido de tablas cubría la prosa —que es una
suposición sobre el CONTENIDO— y aquí lo que se afirma está en la portada del
capítulo. Aun así: **la decisión de dar esto por cerrado es de Elena**, no del
asistente, y por la razón 1 de las cuatro.

Hasta que ella lo diga, lo que sigue siendo cierto es esto y solo esto: **las
cifras que hay son las de su fuente, moverlas salta en rojo, y ya no queda
material canino sin leer del que puedan salir más**.

---

### El registro de la primera reapertura, que sigue valiendo

### Por qué se reabrió, dicho sin adornos

El cierre se declaró sobre **21 tablas de SACN5 leídas fila a fila**, y esa cifra
era falsa sin que nadie pudiera saberlo: el barrido que las encontró recortaba su
propia salida con `sed -n '20,60p'` para que cupiera en pantalla. **Hay 89 tablas
«Key nutritional factors», no 40.** Faltaban tres de patología canina —30-5
(cáncer), 31-3 (reacciones adversas al alimento) y 32-6 (dermatosis
inflamatorias)— y una de ellas era de una patología que el motor no ofrecía.

No lo encontró una revisión: apareció leyendo el capítulo 30 entero por otra
cosa. **La condición 2 («tiene fuente») se estaba cumpliendo cifra a cifra y
fallando en el conjunto**: cada número tenía la suya, y faltaban números.

La condición que hay que añadirle a un barrido para poder cerrarlo con él:
**comparar lo revisado contra el total, y que el total se cuente, no se suponga.**

**Alcance del cierre nuevo: las 73 cifras numéricas de las 47 patologías de
`patologias.json`** — 41 topes y 32 suelos, más 2 límites escritos con la
etiqueta de que el solver **no** los aplica (el Ca:P de los urolitos de calcio y
el omega-3 del cáncer).

| | Cómo se cumple |
|---|---|
| 1 · Vive en el repo | `patologias.json` |
| 2 · Tiene fuente | **73/73 con fuente citada y motivo escrito**, y el barrido de las 89 tablas repetido entero y contado (`VERIFICACION_FILA_A_FILA.md` §cuarta pasada). Veinticuatro tablas de SACN5 leídas literal, más Merck, el consenso ACVIM 2019, Cavanaugh 2020, Center 2026, Purina, Today's Veterinary Practice 2025 y el Reglamento (UE) 2020/354. **No queda ninguna fuente sin abrir** |
| 3 · Ficha de permisos | `motor/permisos.py`. **Se deriva, no se escribe**: quién lo ve, quién lo mueve, entre qué y qué, y qué pasa al moverlo |
| 4 · Test que falla | **BLOQUE 55** (cada cifra contra su fuente, la conversión recalculada, y que el solver la aplique) y **BLOQUE 56** (que la ficha siga derivándose). Los dos probados con el fallo puesto |
| 5 · Decisión con fecha | `DECISIONES.md` D-12 y D-13; el detalle por patología en `PATOLOGIAS.md` |
| 6 · Sin preguntas sin dueño | Lo que queda abierto está en `PATOLOGIAS.md` §5 con dueño, y en `PREGUNTAS_ABIERTAS.md` |

### Qué protege exactamente

Que **nadie pueda mover un número en silencio**. Si alguien cambia una cifra,
borra un tope, añade uno sin fuente o se equivoca en la conversión, la batería se
pone roja y dice qué y contra qué está discrepando.

Y ya ha funcionado: el 8 de septiembre el BLOQUE 13 cazó los cuatro números que
se cambiaron, el 38 cazó una fila nueva en la tabla de FEDIAF, el 12 cazó un
sello mal puesto y `auditar_patologias` cazó un tope que caía bajo el mínimo de
crecimiento. Ninguno se coló.

### Lo que NO significa

- **No significa que los números sean los mejores.** Significa que son los de su
  fuente, y que cambiarlos exige traer otra.
- **No es un candado.** No hay nada que impida editar `patologias.json`. Lo que
  hay es que romperlo salta en rojo, que es lo máximo que da la herramienta — y
  probablemente mejor: un candado se salta y una prueba en rojo se ve.
- **No cubre las patologías que no ofrecemos.** Siete con cifras publicadas se
  añadieron ese día —seis por la mañana y `reaccion_adversa_alimento` por la
  tarde, con la tabla que se había perdido—; las que la fuente declara y seguimos
  sin ofrecer están en `PATOLOGIAS.md` §3-bis y en `VERIFICACION_FILA_A_FILA.md`
  §cuarta pasada con el motivo de cada una, y **añadir una es decisión de
  producto**, no de fuentes.
- **Y no significa que SACN5 esté leído entero — por eso esto está REABIERTO
  desde el 9 de septiembre.** Ver arriba: 32 de las 91 tablas citadas, 11 tablas
  de requisito canino sin mirar, y 26 capítulos de 70 sin una sola cita.
- **No cubre lo que el motor no sabe expresar.** La Tabla 30-5 pide un ratio
  omega-6:omega-3 ≈ 1:1 y un techo de carbohidrato (NFE); el motor solo conoce
  un ratio, el calcio:fósforo, y no calcula el NFE. Está escrito en el aviso de
  la patología y en `PENDIENTE_NUTRICION.md`, no aplicado.

---

## CERRADO · Los techos del libro para el perro sano

**Fecha de cierre: 8 de septiembre de 2026, noche.** Ver `DECISIONES.md` **D-15**.
**Ampliado el 9 de septiembre** con los de crecimiento: ver `DECISIONES.md`
**D-16**.

Las **cuatro cifras** de adulto de `recomendaciones_libro.json` —fósforo y
sodio, en adulto y en senior— más las **ocho de crecimiento** del 9 de
septiembre: calcio y fósforo, en las dos etapas de cachorro y en las dos
columnas de la Tabla 17-1 de SACN5 (según el cachorro vaya a pesar más o menos
de 25 kg de adulto). Son la tercera clase de límite del motor y no existían la
mañana del 8.

| | Cómo se cumple |
|---|---|
| 1 · Vive en el repo | `recomendaciones_libro.json`, con `motor/recomendaciones.py` de cargador |
| 2 · Tiene fuente | 12/12, con la cita literal (SACN5 Tablas 13-3, 14-2, 17-1 y 33-5, y Fascetti cap.10 para el 1,1 % del calcio) y la conversión escrita |
| 3 · Ficha de permisos | ⚠️ **no la tiene todavía.** `permisos.py` deriva de `patologias.json` y estas cifras no son de una patología |
| 4 · Test que falla | **BLOQUE 57** para las cifras (la conversión rehecha desde el %MS, que el solver las aplique, que el filtro final las vea sin ninguna patología marcada, y que el techo del adulto no se cuele en crecimiento) y **BLOQUE 62** para el cachorro de raza grande de punta a punta. Los dos probados con el fallo puesto: se infla el hueso de un menú bueno y tiene que saltar |
| 5 · Decisión con fecha | `DECISIONES.md` D-15 (adulto, con las medidas de los cuatro pesos) y D-16 (crecimiento, con los 20 cachorros de raza grande medidos) |
| 6 · Sin preguntas sin dueño | Queda una, escrita: el **suelo** de sodio de esas tablas no se aplica. `PARA_EL_NUTRICIONISTA.md` PREGUNTA 22 |

**Así que esto está en cinco de seis**, y lo que falta es la condición 3.

---

## CERRADO · El DER

**Fecha de cierre: 8 de septiembre de 2026.** Ver `DECISIONES.md` **D-11**.

Verificado contra FEDIAF 2025, Tablas VII-7 y VII-8b, leyendo el PDF. Tres
cambios: fuera el tope de ×6 RER en lactancia (no es de FEDIAF y recortaba hasta
un tercio), dentro las dos razas con cifra propia (Gran Danés y Terranova), y el
crecimiento pasa a la regla de SACN5 por edad.

| | |
|---|---|
| 4 · Test | **BLOQUE 54**, contra FEDIAF VII-7/VII-8b y SACN5 5-2, más el contrato de `der_casos.json` (100 casos, el mismo fichero en los dos repos) |
| 3 · Ficha de permisos | ⚠️ **no la tiene.** El DER no es un límite de patología y `permisos.py` hoy no lo cubre |

**Así que el DER está en cinco de seis.** Se dice, no se disimula.

---

## CERRADO · La conversión de cada cifra de patología (10 de septiembre de 2026)

Las 88 cifras numéricas de `patologias.json` vienen de tablas que las publican en
**% de materia seca**, y el motor trabaja **por 1000 kcal**. Esa conversión
estaba hecha una vez y **contada en prosa** dentro del campo `por_que`.

| | Dónde se cumple |
|---|---|
| 1 · Vive en el repo | El bloque `conversion` de cada cifra, en `patologias.json` |
| 2 · Tiene fuente | Cada bloque lleva la **cita literal de la fila** (tabla, nota al pie y extremo del rango que se usa) |
| 3 · Ficha de permisos | La de la propia patología, sin cambios: esto no mueve ningún límite, describe de dónde salió |
| 4 · Test que falla si se rompe | **BLOQUE 72**, que rehace la cuenta de las 88. Una cifra sin bloque `conversion` también falla |
| 5 · Decisión escrita, con fecha y motivo | `HECHO.md`, 9-10 de septiembre, con el caso que lo motivó |
| 6 · Sin preguntas sin dueño | La única que quedaba —¿3,5 o 4,0 kcal/g?— está **resuelta con la fuente**, no aplazada |

**La densidad es 4,0 y está probado, no supuesto — y hubo que probarlo porque
SACN5 se contradice consigo mismo.** Su Box 1-2 dice, literal: «recommended
nutrient values for canine and feline foods are based on an energy density of
**3.5 and 4.0** kcal ME/g of food dry matter, **respectively**» — o sea 3,5 para
el perro. Pero sus tablas caninas usan 4,0, y lo dicen tres veces:

- la nota al pie de la **Tabla 13-3** («Concentrations presume an energy density
  of 4.0 kcal/g»), única de las 24 que cita el fichero que declara densidad;
- el **cap.34**, que convierte la glucosamina «in a food with an energy density
  of 4 kcal/g DM»;
- y el **cap.15**, que da la misma cantidad en dos unidades —«approximately 20 %
  of the energy from carbohydrate … translates to about 23 % DM carbohydrate»— y
  esa equivalencia sale **22,9 % a densidad 4,0** y 20,0 % a 3,5. Es la
  comprobación que no depende de ninguna nota ni de ningún número nuestro.

Una nota al pie manda sobre las filas que lleva debajo. Y a 4,0 las cifras del
motor se reproducen desde las filas de sus tablas: 84 de 88 exactas y 4 con un
ajuste declarado.

⚠️ **Y se cerró desmintiendo lo que se había escrito antes.** Quedaba anotado que
SACN5 declara 3,5 kcal/g y que por tanto 68 cifras estaban un 14 % apretadas de
más. Era falso. Es un cierre por la razón 3 de la lista de arriba —un test
demuestra que está mal—, aplicada a la nota, no al motor.

## CERRADO · El suelo de DHA de crecimiento y reproducción (10 de septiembre)

| | Dónde se cumple |
|---|---|
| 1 · Vive en el repo | `requisitos_condicionales.json`, regla `dha_en_crecimiento_y_reproduccion` |
| 2 · Tiene fuente | SACN5 Tablas **15-5, 17-1 (sus dos columnas) y 33-5**, y el texto de los caps. 15 y 33 que las deriva, citando NRC 2006 |
| 3 · Ficha de permisos | No aplica: es un mínimo de etapa, no un límite de patología |
| 4 · Test que falla si se rompe | **BLOQUE 73**: la cifra en las cinco etapas y en ninguna más, y seis menús resueltos en vivo que lo cumplen |
| 5 · Decisión escrita | `HECHO.md` y `PARA_EL_NUTRICIONISTA.md` §5, con la medida previa |
| 6 · Sin preguntas sin dueño | Ninguna: la fuente da la cifra, la derivación y la etapa |

**Medido antes de aplicarlo**: 0 de 10 menús por debajo, el más justo a 1,47
veces el suelo, el DHA entre el 57 % y el 75 % del EPA+DHA. No cambia ni un menú
de hoy, y ese es el motivo de ponerlo ahora y no cuando muerda.

---

## CERRADO · El ratio que pide una patología (10 de septiembre)

| | Dónde se cumple |
|---|---|
| 1 · Vive en el repo | Bloque `ratios` de `patologias.json`; `ratios_de_patologias()` en `motor/motor_completo.py`, que llaman el solver **y** `_tope_patologia_roto` |
| 2 · Tiene fuente | SACN5 **Tabla 40-5** (oxalato cálcico) y **Tabla 41-6** (fosfato cálcico), las dos con la misma frase: «maintain a normal Ca:P ratio (1.1:1 to 2:1)» |
| 3 · Ficha de permisos | `GET /patologias` sirve cada ratio con el límite de FEDIAF del mismo par al lado y su `margen_pct`: el 1,1 aprieta un 10 % sobre el 1,0 de FEDIAF en adulto |
| 4 · Test que falla si se rompe | **BLOQUE 75**, y probado con el fallo puesto por partida doble: se parte el calcio del catálogo y se exige que el filtro final lo cace, y desconectando el ratio del solver el bloque se cae. Además `auditar_patologias.py` rechaza una celda de `ratios` inerte, y `auditar_conversiones.py` (BLOQUE 72) rehace sus cuatro cifras |
| 5 · Decisión escrita | `HECHO.md` del 10 de septiembre y `PARA_EL_NUTRICIONISTA.md` §8, con las dos medidas |
| 6 · Sin preguntas sin dueño | Ninguna sobre el Ca:P: la fuente da los dos extremos y los dos caben. La que queda —el omega-6:omega-3— es **de otra cifra**, está en PREGUNTA 40 y tiene dueño |

**Y este no es de los que se ponen porque falte la regla.** Medido antes de
aplicarlo, en cinco perros adultos por la vía de la API: el de 30 kg con oxalato
salía con Ca:P **1,06** —por debajo del 1,1 de su fuente— **y salía en verde**,
porque el semáforo mide el Ca:P contra el 1,0-2,0 de FEDIAF, que es el rango de
un perro **sano**. Medido después: los diez menús siguen verdes y el más justo
cae clavado en 1,10.

⚠️ **Lo que este cierre NO cierra**: el ratio **omega-6:omega-3** sigue sin
aplicarse, y ahora se sabe exactamente por qué. No falta motor —el mecanismo es
genérico y admite cualquier par—: falta el número. Sus fuentes van de **<1:1**
(artrosis, Tabla 34-2) a **7:1** (renal, Tabla 37-9), un factor siete entre dos
enfermedades que un mismo perro puede tener a la vez, y el NRC 2006 dice del
ratio de totales que «is not helpful». Sigue en
`limites_escritos_que_el_solver_no_aplica`, que es dónde va lo que está escrito y
no se aplica.

---

## ABIERTO · Lo que no está cerrado, y por qué

| | Qué falta |
|---|---|
| **El catálogo** | 163 fichas, 7.407 celdas, y **solo 34 con campo `fuente`**. La composición de 129 fichas no tiene procedencia escrita. Es el bloque grande |
| **La humedad** | No está en ninguna ficha. De ella depende toda conversión desde porcentaje de materia seca. `PARA_EL_NUTRICIONISTA.md` §10.0 |
| **Los siete márgenes interpretados** | Donde la fuente da un solo número y el otro extremo lo pusimos nosotros. `PREGUNTAS_ABIERTAS.md` P-02 |
| **Qué ve el dueño** | `visible_para` es lo único de la ficha que no se deriva, porque es criterio de producto. Hoy está puesto con un reparto por defecto que hay que revisar |
| **El techo del Reglamento europeo en el rango** | La ficha deriva el rango de FEDIAF. Donde el Reglamento (UE) 2020/354 pone un techo adicional —renal 1420, cardíaco 739— está escrito en el `por_que` pero no entra en `rango_permitido` |
| **El BCS ideal: ¿punto 5 o rango 4-5?** | Tensión DENTRO de FEDIAF: la §7.1.1 no distingue dirección y la §7.1.3 dice «the ideal BCS should therefore be between 4/9 and 5/9». Hoy un perro en BCS 4 recibe un **8,2 % más de kcal**. Medido por BCS en `PENDIENTE_DECISIONES.md` §4 |
| **La forma química de las vitaminas y los minerales** | Las tablas de conversión están en el repo (`fediaf_conversiones_vitaminas.json` y `sacn5_fuentes_de_minerales.json`) y **ninguna ficha declara en qué forma viene cada nutriente**. Con el peor factor, el ácido pantoténico caería bajo el mínimo de FEDIAF. `DATOS_QUE_FALTAN.md` |
| **El frío** | SACN5 Tabla 5-3 da las cifras (+95 % en pelo corto), y la ficha no pregunta dónde duerme el perro. Falta la pregunta, no el número |

---

## Cómo se añade algo a este archivo

No se añade porque parezca terminado. Se añade cuando **las seis condiciones se
cumplen y se puede señalar dónde se cumple cada una**, como en las tablas de
arriba. Si una no se cumple, va en ABIERTO con lo que falta.
