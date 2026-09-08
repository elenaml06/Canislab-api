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

## REABIERTO Y VUELTO A CERRAR · Los límites de patología

**Cerrado el 8 de septiembre de 2026 por la mañana. REABIERTO esa misma tarde,
por la razón 3 («un test o un caso real demuestra que está mal»), y vuelto a
cerrar por la noche.**

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
- **No cubre lo que el motor no sabe expresar.** La Tabla 30-5 pide un ratio
  omega-6:omega-3 ≈ 1:1 y un techo de carbohidrato (NFE); el motor solo conoce
  un ratio, el calcio:fósforo, y no calcula el NFE. Está escrito en el aviso de
  la patología y en `PENDIENTE_NUTRICION.md`, no aplicado.

---

## CERRADO · Los techos del perro adulto sano

**Fecha de cierre: 8 de septiembre de 2026, noche.** Ver `DECISIONES.md` **D-15**.

Las **cuatro cifras** de `recomendaciones_adulto.json`: fósforo y sodio, en
adulto y en senior. Son la tercera clase de límite del motor y no existían por
la mañana.

| | Cómo se cumple |
|---|---|
| 1 · Vive en el repo | `recomendaciones_adulto.json`, con `motor/recomendaciones.py` de cargador |
| 2 · Tiene fuente | 4/4, con la cita literal de SACN5 Tabla 13-3 y 14-2 y la conversión escrita |
| 3 · Ficha de permisos | ⚠️ **no la tiene todavía.** `permisos.py` deriva de `patologias.json` y estas cifras no son de una patología |
| 4 · Test que falla | **BLOQUE 57**, y comprueba las cuatro cosas que pueden romperse: la conversión rehecha desde el %MS, que el solver lo aplique, que el filtro final lo vea sin ninguna patología marcada, y que NO se aplique en crecimiento. Probado con el fallo puesto (se cuadruplica el hueso y tiene que saltar) |
| 5 · Decisión con fecha | `DECISIONES.md` D-15, con las medidas de los cuatro pesos |
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

## ABIERTO · Lo que no está cerrado, y por qué

| | Qué falta |
|---|---|
| **El catálogo** | 163 fichas, 7.407 celdas, y **solo 34 con campo `fuente`**. La composición de 129 fichas no tiene procedencia escrita. Es el bloque grande |
| **La humedad** | No está en ninguna ficha. De ella depende toda conversión desde porcentaje de materia seca. `PARA_EL_NUTRICIONISTA.md` §10.0 |
| **Los siete márgenes interpretados** | Donde la fuente da un solo número y el otro extremo lo pusimos nosotros. `PREGUNTAS_ABIERTAS.md` P-02 |
| **Qué ve el dueño** | `visible_para` es lo único de la ficha que no se deriva, porque es criterio de producto. Hoy está puesto con un reparto por defecto que hay que revisar |
| **El techo del Reglamento europeo en el rango** | La ficha deriva el rango de FEDIAF. Donde el Reglamento (UE) 2020/354 pone un techo adicional —renal 1420, cardíaco 739— está escrito en el `por_que` pero no entra en `rango_permitido` |

---

## Cómo se añade algo a este archivo

No se añade porque parezca terminado. Se añade cuando **las seis condiciones se
cumplen y se puede señalar dónde se cumple cada una**, como en las tablas de
arriba. Si una no se cumple, va en ABIERTO con lo que falta.
