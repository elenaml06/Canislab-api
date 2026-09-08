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

## CERRADO · Los límites de patología

**Fecha de cierre: 8 de septiembre de 2026.**
**Alcance: las 57 cifras numéricas de las 46 patologías de `patologias.json`** —
36 topes y 21 suelos.

| | Cómo se cumple |
|---|---|
| 1 · Vive en el repo | `patologias.json` |
| 2 · Tiene fuente | **57/57 con fuente citada y motivo escrito.** Quince tablas de SACN5 leídas literal, más Merck, el consenso ACVIM 2019, Cavanaugh 2020, Center 2026, Purina, Today's Veterinary Practice 2025 y el Reglamento (UE) 2020/354. **No queda ninguna fuente sin abrir** |
| 3 · Ficha de permisos | `motor/permisos.py`. **Se deriva, no se escribe**: quién lo ve, quién lo mueve, entre qué y qué, y qué pasa al moverlo. 57 fichas |
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
- **No cubre las patologías que no ofrecemos.** Seis con cifras publicadas se
  añadieron ese día; las que la fuente declara y seguimos sin ofrecer están en
  `PATOLOGIAS.md` §3-bis, y **añadir una es decisión de producto**, no de fuentes.

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
