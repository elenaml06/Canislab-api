# ESTADO — dónde está Rawku hoy

**Foto tomada el 8 de septiembre de 2026, 11:07–12:00 UTC**, contra los tres
repos (`Canislab-api`, `canislab-web`, `canislab-fuentes`) y contra la API
desplegada. **Es una foto de algo que se mueve**: hay cuatro sesiones más
trabajando ahora mismo en ramas sin fusionar. Lo que puede caducar por eso
está marcado ⏳ y listado entero en §6.

Esto y `DECISIONES.md` son lo primero que se lee al abrir cualquier sesión,
antes de tocar nada. **Lo mantiene una sola sesión** (la que cierra); las
demás lo leen y proponen cambios, no lo reescriben en paralelo.

---

## 0 · Cómo se lee esto

**Los dos niveles.** El nivel 1 es la nutrición: qué come el perro y por qué.
Se cierra y se congela. El nivel 2 es el producto (app de tutor y de
veterinario, front y back): sigue abierto. **El nivel 2 consume el nivel 1;
nunca lo reimplementa, lo copia ni lo corrige por su cuenta.**

**Cerrado quiere decir las seis a la vez** (`DECISIONES.md` §0): vive en el
repo · lleva fuente · lleva ficha de permisos · lo protege un test que falla
si se rompe · está escrito como decisión con fecha y motivo · no deja
preguntas sin dueño.

Por eso las tablas de abajo llevan **una columna por condición** en vez de un
sello: hoy casi nada falla por la nutrición y casi todo falla por la ficha de
permisos, y eso se lee mejor separado.

| Marca | Qué significa |
|---|---|
| **cerrado** | Las seis condiciones |
| **en curso** | Funciona y está probado, pero le falta al menos una de las seis |
| **roto** | Hay algo mal hoy, medido |
| **no empezado** | No existe |
| ⏳ | Puede quedar obsoleto por trabajo de otra sesión (§6) |

**La ficha de permisos** (los ocho campos: `tipo`, `fuente`, `visible_para`,
`modificable_por`, `rango_permitido`, `requiere`, `defecto`, `al_moverlo`)
**no existe todavía en ninguna parte del nivel 1**. Lo más cerca está
`margen_del_profesional`, en una rama sin fusionar, que cubre 2,5 de los 8
campos para 19 cifras. Por eso ninguna línea de la tabla del nivel 1 dice
«cerrado». No es pesimismo: es la condición 3.

---

## 1 · NIVEL 1 — la nutrición

Leyenda de las columnas: **Rp** = vive en el repo · **Fu** = lleva fuente
comprobable · **Fi** = ficha de permisos · **Te** = test que falla si se rompe ·
**De** = escrito como decisión.

### 1.1 · Los requisitos de FEDIAF

| Qué | Dónde | Rp | Fu | Fi | Te | De | Estado |
|---|---|---|---|---|---|---|---|
| Tabla de requisitos, 46 filas | `requerimientos_v2_final.json` | ✅ | ⚠️ 31/46 llevan `nota_auditoria` en prosa; 15 no llevan nada | ❌ | ✅ BLOQUE 18 (`auditar_fediaf.py`), sello en `/verificar` | ⚠️ en `CLAUDE.md`, no como decisión | **en curso** |
| Los 41 nutrientes + Ca:P + calcio raza grande se verifican | `motor/verificar.py` (`MAPA`, 44 entradas) | ✅ | ✅ | ❌ | ✅ BLOQUE 27 | ✅ | **en curso** (falta ficha) |
| El techo de lisina no se aplica | `verificar.MAXIMOS_NO_APLICADOS` | ✅ | ✅ | ❌ | ✅ BLOQUE 27 | ✅ `DECISIONES.md` D-03 | **en curso** (falta ficha) |
| Los mínimos escalan solo hacia arriba; los máximos no escalan | `verificar.minimo_de()` / `maximo_de()` | ✅ | ✅ FEDIAF 7.2.5 | ❌ | ✅ BLOQUE 34 | ✅ `DECISIONES.md` D-04 | **en curso** (falta ficha) |

**Medido hoy:** el fichero tiene **46 filas**, no 43. Las 43 de las que habla
`CLAUDE.md` son los requisitos de FEDIAF que se verifican (41 nutrientes +
Ca:P + calcio de raza grande); las otras tres —`Fibra`, `Taurina`,
`L_carnitina`— están en el fichero porque las usan los objetivos por
patología, y no son requisitos de FEDIAF. **La frase de `CLAUDE.md` no es
falsa, pero cuenta filas de un fichero que tiene otras tres.** Corregirlo es
una línea (§5, F-01).

### 1.2 · El catálogo de alimentos

| Qué | Dónde | Rp | Fu | Fi | Te | De | Estado |
|---|---|---|---|---|---|---|---|
| 163 fichas · 7.407 casillas de nutriente | `alimentos_v3_final.json` | ✅ | ❌ **34/163 fichas llevan campo `fuente`** | ❌ | ✅ BLOQUE 12, 19, 26, 28, 29, 46 + sello | ⚠️ parcial | **en curso** |
| Los tres estados de un 0 (`sin_dato`, `dato_dudoso`, `cero_verificado`) | mismas fichas | ✅ | ✅ | ❌ | ✅ BLOQUE 28, 29, 46 | ✅ | **en curso** (falta ficha) |
| 1.362 casillas declaradas `sin_dato` (143/163 fichas lo usan) | mismas fichas | ✅ | — | ❌ | ✅ BLOQUE 29, 35 | ✅ | **en curso** |
| Identificador de fuente por ficha (`fuentes_id`) ⏳ | **rama `claude/nutricion-pendiente-vuoobq`**, 99/163 fichas | ❌ **fuera de `main`** | ✅ | ❌ | ✅ BLOQUE 51 (en la rama) | ❌ | **en curso, sin fusionar** |
| Columna de humedad con procedencia ⏳ | misma rama, 65 fichas | ❌ fuera de `main` | ✅ USDA | ❌ | ✅ | ❌ | **en curso, sin fusionar** |
| Contraste exhaustivo de las 7.407 casillas contra su fila de origen | — | ❌ | — | ❌ | ❌ | ❌ | **no empezado** |

**El dato duro:** hoy, en `main`, **129 de las 163 fichas no tienen campo de
procedencia**, y las que la tienen la llevan en prosa (`nota_datos`, 105
fichas), lo que obliga a buscar por nombre en cada revisión. Buscar por
nombre ya falló una vez (el lío vaca/ternera del cerebro). El trabajo que lo
arregla existe y está fuera de `main`.

### 1.3 · Los topes de seguridad crónica y las reglas por alimento

⚠️ **Verificados contra NRC 2006 el 8 de septiembre, y salen tres cosas**
(detalle en `PARA_EL_NUTRICIONISTA.md` §7.1 y §7.2):

| Tope | Qué se encontró |
|---|---|
| Vitamina D (20 µg y 2,6 µg/kg^0,75) | **No puede activarse**: el máximo legal de FEDIAF (14,19) es más estricto. Ya estaba dicho para la vitamina D en su `nota_auditoria` |
| Selenio (570 µg) | **No puede activarse**: el legal de FEDIAF (142) es 4× más estricto. Y el NRC dice *«no data are available on an acceptable SUL»*; el de AAFCO son 500, no 570 |
| **Yodo (1400 µg)** | **Sí actúa, y es el nivel al que el NRC documenta DAÑO** en cachorros. El NRC dice expresamente que **no se puede predecir un SUL** de yodo |
| Tiaminasa, mercurio, hígado, vísceras, clara, oxalato | Sin cambios: ya estaban **declarados como criterio nuestro** en la cabecera del propio fichero |

| Qué | Dónde | Rp | Fu | Fi | Te | De | Estado |
|---|---|---|---|---|---|---|---|
| Los 5 topes crónicos (vit. D, yodo, selenio, mercurio, tiaminasa) | `motor/seguridad.py`, **como constantes de código** | ✅ | ✅ cada cifra con su fuente al lado, en comentario | ❌ | ✅ BLOQUE 21, 22 + duros en el solver | ⚠️ en comentarios | **en curso** |
| ~12 reglas más por alimento (oxalato, purinas, hígado 10 %, vísceras 10 %, clara 5 %, borraja, tejido tiroideo, congelación, astillado) | `motor/seguridad.py` | ✅ | ✅ prosa | ❌ | ✅ BLOQUE 30, 31, 33 | ⚠️ en comentarios | **en curso** |
| Los umbrales de corte son criterio nuestro y está dicho | cabecera de `seguridad.py` | ✅ | ✅ lo declara literalmente | ❌ | — | ⚠️ en comentario | **en curso** |

**Lo importante de esta sección:** toda esta capa es **código, no dato**. No
se puede servir por la API, no puede llevar ficha de permisos, y el front no
puede preguntarle nada. Es la parte del nivel 1 más lejos de poder pasar al
nivel 2 tal como está.

### 1.4 · Las patologías

| Qué | Dónde | Rp | Fu | Fi | Te | De | Estado |
|---|---|---|---|---|---|---|---|
| 40 perfiles · 14 topes · 5 suelos · 6 objetivos terapéuticos | `patologias.json` | ✅ | ✅ **19/19 topes y suelos llevan `fuente` y `por_que`** | ❌ | ✅ BLOQUE 13, 32, 36, 44, 50 (`auditar_patologias.py`) | ⚠️ en `por_que` | **en curso** |
| **Los 19, verificados uno a uno contra su capítulo de SACN5** (8 sep) | — | — | **13 de 19 exactos o dentro del rango de su fuente**; 4 discrepan; 2 dependen de fuentes que no tenemos en local (Merck, ACVIM 2019, Center 2026) | ❌ | — | ⚠️ | **en curso** |
| `GET /patologias` sirve la tabla desde el mismo archivo que aplica el solver | `main.py` | ✅ | ✅ | ❌ | ✅ BLOQUE 44, cifra a cifra | ✅ | **en curso** (falta ficha) |
| Ningún tope formulable por debajo del mínimo de FEDIAF | `auditar_patologias.py` | ✅ | ✅ | — | ✅ BLOQUE 32/36 — **ejecutado hoy: «todo cuadra»** | ✅ | **cerrado salvo ficha** |
| `margen_del_profesional`: hasta dónde puede mover cada cifra un veterinario ⏳ | **rama `claude/veterinary-mode-ui-fixes-s9l5j7`**, 19/19 cifras | ❌ **fuera de `main`** | ✅ | ⚠️ **2,5 de los 8 campos** | ✅ BLOQUE 51 (en la rama) | ❌ | **en curso, sin fusionar** |
| La tabla de patologías está cargada **dos veces en memoria** | `motor.patologias` y el módulo suelto `patologias` | ✅ | — | — | ❌ **ningún test lo ve** | ❌ | **roto (latente)** |

**Verificado hoy, no de memoria:**
- `auditar_patologias.py` ejecutado: **47 patologías, 41 topes, 32 suelos** (por la tarde, tras la cuarta pasada; por la mañana eran 46/36/21), «todo
  cuadra» (8 de septiembre, tarde). Eran 40/14/5 esa misma mañana: la ronda de
  verificación contra las fuentes añadió seis patologías y rellenó los factores
  que las tablas pedían y no se aplicaban. Ver `PATOLOGIAS.md` §0-bis y §0-quater.
- La rama del veterinario **no cambia ni un valor**: comparadas las 19 cifras
  y los 40 `formulable` entre `main` y la rama, **0 diferencias**. Solo añade
  el bloque `margen_del_profesional`. Su afirmación es cierta.
- La doble carga en memoria es real:
  `motor.patologias.PATOLOGIAS is motor_completo.PATOLOGIAS` → **False**; el
  módulo suelto `patologias` sí es el mismo objeto que usa el solver. Hoy los
  dos tienen el mismo contenido, así que no hay fallo vivo — pero es la misma
  familia del `POST /menu` borrado, y **ningún test lo vigila**.

### 1.5 · La energía (DER)

✅ **CERRADO el 8 de septiembre** — `DECISIONES.md` D-11. Verificado contra
FEDIAF 2025 (Tablas VII-7 y VII-8b) y SACN5 (Tabla 5-2), aplicada la regla
«FEDIAF manda; donde FEDIAF no llega, SACN5», y protegido por el BLOQUE 54 y
por el contrato de 100 casos idéntico en los dos repos.

⚠️ **Lo que se encontró al verificarlo, y ya está aplicado:**
Hasta ese día el DER solo estaba comprobado contra su propio contrato de 85
casos — que garantiza que los dos repos calculan lo mismo, **no que lo que
calculan sea lo que dice la fuente**. Al abrir FEDIAF VII-7, SACN5 Tabla 5-2 y
AAHA 2021:

| Qué | Resultado |
|---|---|
| Los 5 escalones de actividad (95/110/125/150/175) | ✅ **exactos** contra FEDIAF VII-7 |
| El adelgazamiento a 1,0 × RER del peso ideal | ✅ coincide con SACN5, más estricto que FEDIAF |
| La ecuación de crecimiento (Klein) | ✅ **es la de FEDIAF VII-8b**, idéntica |
| Gestación (132 · 132+26×kg) | ✅ **FEDIAF VII-8b**, exacta |
| La fórmula de lactancia | ✅ **FEDIAF VII-8b**, letra por letra, con sus factores L |
| **El tope de ×6 RER en lactancia** | ✅ **QUITADO**: no era de FEDIAF y recortaba hasta un −33 % |
| Los 3 escalones de crecimiento de respaldo | ✅ **SUSTITUIDOS** por la regla de SACN5 (3×RER hasta los 4 meses, 2×RER después). Dos de los tres eran código muerto |
| Gran Danés y Terranova | ✅ **ADOPTADOS** de FEDIAF VII-7 (200 y 105). Un Gran Danés pasa de 2590 a 4710 kcal |

Detalle y medidas: `PREGUNTAS_ABIERTAS.md` P-10 a P-13, y
`PARA_EL_NUTRICIONISTA.md` §1.

| Qué | Dónde | Rp | Fu | Fi | Te | De | Estado |
|---|---|---|---|---|---|---|---|
| El DER se calcula en dos sitios y manda el del front | `der.py` + `canislab-web/src/der.js` | ✅ | ✅ | ❌ | ✅ contrato de 100 casos: BLOQUE 23 aquí, `der-contrato.spec.js` allí | ✅ `CLAUDE.md` | **en curso** |
| Los escalones de actividad | `der.BASE_ACTIVIDAD` | ✅ | ✅ **FEDIAF VII-7, verificado** | ❌ | ✅ | ⚠️ | **en curso** |
| La fórmula de lactancia, sin tope | `der.LACTANCIA_*` | ✅ | ✅ **FEDIAF VII-8b** | ❌ | ✅ BLOQUE 54 | ✅ D-11 | **cerrado salvo ficha** |
| Las dos razas con cifra de FEDIAF | `der.RAZAS_CIFRA_FEDIAF` | ✅ | ✅ **FEDIAF VII-7** | ❌ | ✅ BLOQUE 54 + contrato | ✅ D-11 | **cerrado salvo ficha** |
| El respaldo de crecimiento | `der.CRECIMIENTO_*` | ✅ | ✅ **SACN5 5-2** | ❌ | ✅ BLOQUE 54 + `der-contrato` | ✅ D-11 | **cerrado salvo ficha** |
| **Las razas con cifra propia de FEDIAF** | — | ❌ **no existe** | ✅ FEDIAF VII-7 | ❌ | ❌ | ❌ | **no empezado** |
| El contrato está sincronizado entre los dos repos | `der_casos.json` | ✅ | — | — | ✅ | ✅ | **verificado hoy: md5 `92506f87…` idéntico en los dos repos** |
| El peso objetivo desde el BCS se **divide**, no se resta | `verificar.peso_objetivo_desde_bcs` | ✅ | ✅ AAHA 2014/2021 + GPOI 2019 | ❌ | ✅ BLOQUE 37 | ✅ `DECISIONES.md` D-05 | **en curso** (falta ficha) |

### 1.6 · La garantía de que ningún menú sale sin verificar

| Qué | Dónde | Rp | Fu | Fi | Te | De | Estado |
|---|---|---|---|---|---|---|---|
| `_garantizar_verificado()` en todo camino que devuelve menú | `main.py` | ✅ | ✅ regla 1 | — | ✅ **BLOQUE 8**, y BLOQUE 47 para los menús guardados | ✅ `CLAUDE.md` | **cerrado salvo ficha** |
| Los topes por patología se comprueban también ahí, sobre kcal reales | `main.py` | ✅ | ✅ | ❌ | ✅ BLOQUE 13 | ✅ | **en curso** |
| La escalera de relajación suelta la FORMA, nunca la nutrición | `main._escalera_de_relajacion` | ✅ | ✅ regla 3 | ❌ | ✅ BLOQUE 9, 45 | ✅ | **en curso** |

### 1.7 · Lo que está roto o falta, medido hoy

| Qué | Estado | Medida |
|---|---|---|
| **La batería NO sale en verde hoy sobre `main` sin tocar** | **roto (prueba mal diseñada)** | Ver §1.9. 1 fallo de 50 bloques, 1.232 s. Es el BLOQUE 4, y no es la nutrición. **Arreglado el 8 de septiembre** fijando la semilla |
| ~~El tope de lactancia y las razas de FEDIAF~~ | **cerrado 8 sep** | `DECISIONES.md` D-11 |
| ~~4 de los 19 límites de patología discrepan de SACN5~~ | **resuelto 8 sep** | El sodio cardíaco baja a 739/739/**625**/480 y ya no discrepa. El cobre (2,4) queda triplemente acotado: Center 2026 lo da como tolerable, SACN5 pide 1,25 como objetivo y la ley pone el techo en 2,50. La grasa de obesidad (30 frente a los 22,5 de la fuente) sigue declarada y con su motivo medido: 22,5 no resuelve con el catálogo real |
| ~~La cardiopatía genérica atribuye a ACVIM cifras que ACVIM no da~~ | **arreglado 8 sep** | Verificado contra Keene 2019: el consenso es cualitativo en las 4 etapas, sin una sola cifra. Los 80-99/50-79/<50 mg/100 kcal son de Cavanaugh, Veterinary Practice News 2020. `PATOLOGIAS.md` §1.1 |
| ~~El oxalato cálcico no ajusta nada~~ | **arreglado 8 sep** | Y la afirmación era medio falsa: no aplicaba ningún tope NUMÉRICO, pero sí excluía alimentos altos en oxalato desde agosto. Ahora aplica sodio ≤750, fósforo ≤1500 y magnesio ≤375, y la lista de alimentos pasa de 4 entradas a 20 (Tabla 40-3, solo las marcadas «avoid»). `PATOLOGIAS.md` §1.2 |
| ~~La artrosis mide el nutriente equivocado~~ | **arreglado 8 sep** | El suelo pasa de `epa_dha` a `epa`, con clave nueva en el `MAPA` y fila propia en la tabla de FEDIAF (patrón de Fibra/Taurina/L-carnitina). `PATOLOGIAS.md` §1.3 |
| ~~14 patologías tienen factores de su propia fuente sin aplicar~~ | **hecho 8 sep** | Aplicados los de renal, obesidad, artrosis, enteropatía crónica, disfunción cognitiva, dermatosis, atopia, cistina y hepatopatía, y la estruvita pasa a formulable. Lo que queda, en `PATOLOGIAS.md` §5 |
| ~~El sodio cardíaco está por encima del techo legal europeo~~ | **arreglado 8 sep** | Bajado a **739 · 739 · 625 · 480**. El 625 del estadio C es el único número que admiten las tres fuentes a la vez (techo de SACN5 Class Ia, dentro del rango de Cavanaugh para C, y bajo el techo legal). Fuente en `canislab-fuentes/Reglamento_UE_2020_354/` |
| **Falta un techo de proteína que NO necesita prescripción** | **medio hecho 8 sep** | El renal (62,5, Reg. 2020/354 entrada 10) ya está aplicado. Queda el hepático (79,3, entrada 23), que no se aplicó porque `hepatopatia` sigue bloqueada por el cobre |
| **3 de los 5 topes de seguridad crónica no pueden activarse nunca** | **roto (documentación)** | El máximo legal de FEDIAF es más estricto en vitamina D (×2) y selenio (×4). No deja a nadie desprotegido, pero la regla 2 del `CLAUDE.md` dice que protegen |
| **El techo de yodo es el nivel al que el NRC documenta DAÑO** | **roto** | NRC 2006: a 1400 µg/1000 kcal hubo función tiroidea deprimida y alteraciones óseas en cachorros, y dice que **no se puede predecir un SUL**. El motor usa 1400 como techo. §7.2 |
| Faltan 3 de los 20 objetivos legales europeos | **no empezado** | Convalecencia (proteína ≥71 g/1000 kcal), diarrea aguda y apoyo en estrés. §8.4-bis |
| **5 factores de las tablas de SACN5 que el motor no aplica** | **no empezado** | proteína y fibra en obesidad, fósforo y cloruro en cardiopatía. §8.1-ter |
| **Un cachorro de raza grande sin hueso carnoso se queda sin menú ~1 de cada 4 veces** | **roto** | Medido: 11/15 con menú. No lo causa el techo de Ca:P nuevo (sin él, 9/15). Es el mínimo de calcio reforzado, que sin hueso hay que cerrar solo con suplementos |
| **`renal` + `pancreatitis` no da menú, y el motor no sabe decir por qué** | **roto** | Ver §1.8. Confirmado y, además, **diagnosticado**: chocan el fósforo renal (1200) y la grasa de pancreatitis (20) |
| La ficha de permisos de los ocho campos | **no empezado** | 0 de 8 campos en `main`; 2,5 de 8 en una rama, solo para 19 cifras de patología |
| La clasificación en las tres cajas (tope duro / rango clínico / criterio nuestro) | **no empezado** | No existe como dato en ninguna parte |
| Las cifras del nivel 1 no llevan su unidad y su base pegadas | **roto (latente)** | Conviven tres convenciones: g/1000 kcal, % de materia seca, % de energía metabolizable. Ninguna escrita junto al número |
| `renal_avanzada` no se comporta distinto de `renal` | **roto** | Su diferencia clínica es la proteína y no hay tope de proteína en ninguna de las dos. Verificado: las dos tienen exactamente `fosforo: 1200` y nada más |
| BLOQUE 1 y BLOQUE 43 afirman «verde» llamando al solver, no a `_garantizar_verificado` | **roto (prueba mal apuntada)** | Parpadean en perros pequeños. Reportado por la sesión del veterinario; no reproducido por mí |
| 13 condiciones clínicas estudiadas sin perfil en `patologias.json` | **no empezado** | `canislab-fuentes/TRABAJO_RAWKU/entregas/AUDITORIA_PATOLOGIAS.md`. ⚠️ Ese documento tiene un fallo de premisa: ver §5, F-02 |

### 1.8 · `renal` + `pancreatitis`: qué choca exactamente

Esto lo pedía el anexo del encargo y **se puede contestar**. Medido hoy,
adulto de 25 kg, DER 1200, modo automático, `time_limit` 60 s:

| Caso | ¿Sale menú? |
|---|---|
| `renal` sola, último peldaño | **sí** (6 alimentos, 2,2 s) |
| `pancreatitis` sola, último peldaño | **sí** (6 alimentos, 1,6 s) |
| `renal` + `pancreatitis`, **los seis peldaños de la escalera** | **no**, los seis |
| … quitando el tope de fósforo renal (1200) | **sí** (7 alimentos, 0,3 s) |
| … quitando el tope de grasa de pancreatitis (20) | **sí** (5 alimentos, 1,1 s) |
| … quitando el tope de proteína de pancreatitis (75) | no |
| … con la grasa de pancreatitis a **25** (SACN5 10 % MS) | no |
| … con la grasa de pancreatitis a **37,5** (SACN5 15 % MS) | **sí** (7 alimentos, 2,2 s) |
| … con el fósforo renal a 1250 (extremo alto de SACN5) | no |

**Las dos restricciones que chocan son el fósforo renal ≤ 1200 y la grasa de
pancreatitis ≤ 20.** Soltando cualquiera de las dos, sale menú. No es un
timeout disfrazado: el solver declara infactible en 0,1 s, o sea que lo
detecta la presolución.

**Y la infactibilidad la creamos nosotras, en parte.** El 20 de grasa sale de
Merck («less than 20 g fat/1,000 kcal»), que es una fuente legítima; pero la
otra fuente del mismo campo, SACN5 cap. 67 Tabla 67-3, da ≤15 % de materia
seca, que con el puente de 4000 kcal/kg MS que usa el repo son **37,5** — y a
37,5 el menú sale. O sea: **la elección entre dos fuentes válidas es lo que
deja sin menú a un perro renal con pancreatitis.** Eso no es un fallo de
programación: es exactamente la decisión clínica que la sección 3 del encargo
llama «rango clínico», y la nutricionista ya dijo que la grasa en
pancreatitis depende del caso. Va a `PREGUNTAS_ABIERTAS.md` P-03 con dueño.

⚠️ **Corrección a lo que dice el `TRASPASO.md` de la rama del veterinario:**
ahí se afirma que el motor «solo sabe decir que no hay solución». Es cierto
para el usuario —el mensaje que sale es el genérico—, pero **el motor sí
puede localizar el choque**: soltar un tope cada vez y ver cuál desbloquea
funciona, tarda 2 segundos, y lo acabo de hacer. Lo que falta es exponerlo,
no averiguar si se puede.

### 1.9 · La batería sobre `main`: 1 fallo, y es la prueba, no el motor

**Ejecutada entera hoy sobre `main` sin tocar nada**, 50 bloques, **1.232 s**:

```
❌ 1 FALLOS ENCONTRADOS — NO ENTREGAR TODAVÍA:
  - BLOQUE4: pescado NUNCA (0/10) — revisar si es lo esperado
```

**Qué es.** El BLOQUE 4 resuelve diez menús seguidos para un cachorro de 18 kg
y **exige que el pescado salga en unos sí y en otros no** (ni 0/10 ni 10/10).
El solver es aleatorio a propósito (`RandomState(None)`), así que es una
afirmación estadística con n = 10 y **sin semilla**.

**Medido después, con la máquina libre:** seis tandas de diez, 6/10, 4/10,
3/10, 5/10, 3/10 y 3/10 — **ninguna infactible**, tasa base ~40 %. Con eso,
0/10 tiene una probabilidad de 0,6¹⁰ ≈ **0,6 % por ejecución**, y hoy salió.
Una medida independiente de 40 tiradas dio 24/40.

**Conclusión, y hay que separarla en dos:**

1. **No hay regresión nutricional.** Los diez menús de la ejecución fallida
   fueron factibles (se ve en la propia salida: `V-INTEGRA Cachorro` aparece
   10 veces), y el pescado sale con normalidad al repetir. Lo que hicieron fue
   cubrir el omega-3 con aceite de salmón —que es un suplemento, no un
   pescado— en las diez.
2. **Sí hay un problema de prueba, y no es el único.** El BLOQUE 4 puede
   ponerse rojo sin que nada esté mal, ~1 de cada 170 ejecuciones. Es la misma
   familia que los BLOQUE 1 y 43, que afirman «verde» llamando al solver en
   vez de a `_garantizar_verificado()` y con límite de tiempo. **Una batería
   que se pone roja sola enseña a ignorar el rojo**, que es justo lo contrario
   de para lo que existe. Arreglo probable: fijar semilla, o afirmar sobre 30
   tiradas en vez de 10, o contar el aceite de salmón como fuente de omega-3.

⚠️ **Consecuencia para todo lo demás de este documento:** cuando aquí se dice
que una rama «declara batería en verde», eso significa que su sesión la vio en
verde una vez. **No lo he reejecutado en las ramas.**

### 1.10 · Dos trampas de método (para quien repita estas medidas)

**1 · `resolver()` devuelve una tupla `(ok, menu)`, no el menú.** Un
`if resolver(...)` sale siempre verdadero, y `len()` sobre el resultado da 2
independientemente de todo. Yo mismo saqué un resultado falso así antes de
mirar la firma. Si una medida sobre el solver da «siempre factible, 2
alimentos», es esto.

**2 · Lanzar la batería con `nohup ... &` devuelve 0 al instante**, y ese 0 no
dice nada: es del arranque, no de la batería. Es primo del que ya está
apuntado en otra sesión (`python3 pruebas_completas.py | tail -30` devuelve el
código de salida de `tail`). **La única señal buena es leer la última línea de
la salida**: o «TODO EN VERDE» o «N FALLOS ENCONTRADOS».

---

## 2 · NIVEL 2 — el producto

Abierto a propósito. Aquí solo se apunta lo que hace falta para saber que no
pisa el nivel 1.

| Qué | Dónde | Estado |
|---|---|---|
| App de tutor (generador, casa, mis menús) | `canislab-web/src/App.jsx` | **en curso** |
| Modo veterinario (puerta, pacientes, ficha clínica, formulador, pautas) | `App.jsx` líneas ~3.462–5.832 + `formulador.jsx`, `fichaclinica.jsx`, `pautaimprimible.jsx` | **en curso** |
| El rol profesional se verifica **en el servidor**, no en el front | `main._es_profesional_acreditado()` | ✅ **cerrado en lo que importa** |
| Cobros (Stripe) | `main.py` + `suscripcion.jsx` | **en curso** — desplegado hoy en **modo prueba** (`/verificar` dice `"modo":"prueba"`) |
| Persistencia (Supabase) | `persistencia.py` + `supabase.js` | **en curso** — 9 migraciones aplicadas |
| CI de pruebas | **no existe en ninguno de los tres repos** | **no empezado** ⏳ hay uno escrito en la rama `claude/audit-api-sources-web-gk95ir` |

**Lo bueno, verificado:** `main.py` **no acepta** un `modo_profesional` que
venga del cliente, y lo dice en cuatro sitios distintos del código. El
permiso lo resuelve el servidor leyendo `rol` + `rol_verificado_en` de
Supabase. Ése es el patrón que pide la sección 8 del encargo, y ya está
puesto para el permiso más importante que hay.

---

## 3 · Dónde el nivel 2 pisa el nivel 1

Cuatro sitios, todos verificados hoy.

### 3.1 · La lista de patologías está duplicada en el front, sin ningún test

`canislab-web/src/App.jsx` tiene una constante `PATOLOGIAS` con **32 entradas
y un campo `segura`**, que es el `formulable` del backend. El propio
comentario del código lo admite: *«cualquier cambio de `formulable` en
patologias.json tiene que reflejarse aquí también»*.

**Medido hoy:** las 32 claves existen todas en el backend, y **los 32
`segura` coinciden con los 32 `formulable`**. Hoy no hay divergencia.

**Y no hay nada que la impida mañana.** Ningún test de ninguno de los dos
repos compara las dos listas. `tests/fake-supabase.js` tiene además una
**tercera copia** de esos valores, escrita a mano. Es literalmente el fallo
que describe la regla 5 de `CLAUDE.md` —tres semanas respetando tres de seis
categorías, en silencio, con el menú saliendo verde igual— y el que mató al
`POST /menu`. **Es una decisión clínica (¿se le genera menú automático a este
perro?) tomada en la interfaz.**

### 3.2 · El front sigue dando una regla de seguridad que el motor borró

`canislab-web/src/instrucciones.js:32` dice al usuario: *«Si usas atún u otro
pescado grande, **no más de 1 vez por semana**»*.

Esa regla era `TOPE_MERCURIO_DIAS_SEMANA = 1` y **se borró del motor el 25 de
agosto**, con dos motivos escritos en `motor/seguridad.py`: no la usaba
ninguna línea del repositorio, y **no tiene base en perros** (es una
transposición de las recomendaciones de FDA/EFSA para embarazadas y niños).
Lo que quedó es el 10 % de las kcal del día, que sí se aplica.

O sea: **el nivel 1 retiró una regla por no tener base, y el nivel 2 se la
sigue diciendo al dueño.** Es un número clínico escrito en la interfaz, y es
además el caso exacto que la sección 8 llama «alguien arregla un número en el
front y nadie se entera» — solo que al revés.

### 3.3 · El catálogo de alimentos está duplicado en el front

`App.jsx` lleva su propia lista de alimentos por categoría. La compara con el
motor `tests/catalogo-app-y-motor.spec.js` — pero esa prueba **solo corre si
los dos repos están clonados uno al lado del otro**, y **no hay CI en
`canislab-web`**, así que en la práctica no corre nunca de forma automática.
Ya estuvo días en rojo sin que se viera (siete alimentos que el motor había
retirado seguían ofreciéndose en la app).

### 3.4 · El DER se calcula dos veces

Conocido y documentado en `CLAUDE.md`. **Es el único de los cuatro que está
bien defendido**: contrato de 100 casos, probado en los dos repos, y
`der_casos.json` verificado hoy como idéntico (md5 `92506f87725fbfa084de25701ab0e8d8`).
Se deja aquí como referencia de cómo deberían estar los otros tres.

---

## 4 · Ramas, PRs y despliegue

**Comprobado con `git merge-base --is-ancestor`**, que es la prueba buena:
dice si el tip de la rama está contenido en `main`. `git cherry` **no sirve**
(compara por `patch-id`, y un commit fusionado con squash cambia de
`patch-id`), y `git diff --stat` tampoco (sale dominado por lo que `main`
añadió después).

### 4.1 · `Canislab-api` — 5 ramas, las 5 fuera de `main`. Ningún PR abierto

| Rama | Commit | Fuera | ¿Verificada? | Qué hace falta |
|---|---|---|---|---|
| `claude/audit-api-sources-web-gk95ir` | `3cd21a2` | 2 | ✅ batería en verde declarada (50 bloques, 959 s) — **no reejecutada por mí** | Decidir si entra. Trae el CI y el mapa de `CLAUDE.md` al día |
| `claude/nutricion-pendiente-vuoobq` | `e562501` | 4 | ✅ los dos commits de datos declarados verdes (51 bloques, 821 s y 857 s) — **no reejecutados por mí** | **Nivel 1.** Es la procedencia del catálogo. Revisar y fusionar |
| `claude/veterinary-mode-ui-fixes-s9l5j7` | `5b66061` | 2 | ⚠️ **no declara batería.** Verificado por mí que no cambia ningún valor | **Nivel 1.** Es la ficha de permisos empezada. 7 de sus 19 márgenes están «interpretados» y hay que revisarlos |
| `claude/nutrition-audit-data-validation-bihto9` | `01d11d4` | 11 (56 detrás) | — | **Nada que rescatar.** Ver `DECISIONES.md` D-01 y D-02. Se puede borrar |
| `claude/el-corazon-de-ternera-es-musculo` | `6d2e450` | 4 (79 detrás) | ❌ su commit base es un **WIP con la batería en rojo (13 fallos)** | **No fusionar.** Ver `DECISIONES.md` D-06 |

### 4.2 · `canislab-web` — 13 ramas: 5 dentro de `main`, 8 fuera

| Rama | Fuera | Nivel | Nota |
|---|---|---|---|
| `claude/aviso-composicion-menu` | 0 | — | **Dentro de `main`.** Borrable sin perder nada |
| `claude/ficha-completa` | 0 | — | Dentro de `main`. Borrable |
| `claude/multi-perro` | 0 | — | Dentro de `main`. Borrable |
| `claude/perfil-perro-no-se-guarda` | 0 | — | Dentro de `main`. Borrable |
| `claude/rawku-sentry-login-nav-ro683v` | 0 | — | Dentro de `main`. Borrable |
| `claude/calcio-raza-grande-contrato` | 3 | **1** | Toca la lista de alimentos de la app. Sin leer |
| `claude/laringe-y-trazas` | 2 | **1** | Laringe fuera del selector y trazas en la ficha. Sin leer. ⚠️ «trazas» es el nombre del campo que **se rechazó** (D-01): comprobar que no es lo mismo |
| `claude/de-punta-a-punta-con-la-api-real` | 1 | 2 | Sin leer |
| `claude/la-ficha-clinica-pinta-los-que-cumplen` | 1 | 2 | Sin leer |
| `claude/limpieza-web-appjsx-ci` ⏳ | 1 | 2 | Sesión viva: parte `App.jsx` 11.798 → 7.498 y añade CI |
| `claude/vet-margen-por-patologia` ⏳ | 2 | 2 | Sesión viva: **la mitad de pantalla de `margen_del_profesional`. Va con la rama de la API o no va** |
| `claude/veterinario-arranque-y-rueda` ⏳ | 1 | 2 | **Sesión viva que nadie mencionó.** Arranque del veterinario y rueda de ajustes. Nivel 2 puro, sin nutrición |

### 4.3 · `canislab-fuentes` — 3 ramas, 2 fuera de `main`

| Rama | Fuera | Nota |
|---|---|---|
| `claude/limpieza-fuentes` ⏳ | 1 | Sesión viva: `INVENTARIO_FUENTES.md` + `.gitignore` |
| `add-sacn5-58-capitulos` | 4 (1 detrás) | **No fusionar.** Es la línea anterior a la limpieza del 7-sep. Ver `DECISIONES.md` D-07 |

### 4.4 · Lo desplegado

**`main` es lo que corre.** Verificado hoy contra
`https://canislab-api.onrender.com/verificar`:

- `sello_main_py_actual` = `f12ad1c8876174ae` = SHA-256 del `main.py` de `main`. **Coinciden.**
- Los tres sellos de datos correctos, 163 alimentos cargados.
- Sentry activo. **Stripe en modo prueba con precios de sandbox.**
- Arrancado a las 11:16:01 UTC del 8 de septiembre.

### 4.5 · El documento que manda borrar ramas sin haberlas comprobado

`PENDIENTE.md:62` dice hoy, en `main`: *«Borrar las ramas viejas de los dos
repos (15 ya comprobadas, nada que rescatar)»*, y `PENDIENTE_PRODUCTO.md:82`
lo repite. **Es falso hoy**: de aquellas 15 de la auditoría del 23 de agosto,
once ya no existen, y de las 18 ramas vivas que hay ahora entre los tres
repos **13 están fuera de `main`** y varias llevan trabajo de nivel 1.

La corrección está escrita en la rama `claude/audit-api-sources-web-gk95ir`,
sin fusionar. **Mientras no entre, el documento sigue diciendo en `main` que
se pueden borrar.** Es lo más urgente de esta lista porque es lo único que
puede destruir trabajo.

---

## 5 · Documentos que afirman cosas que no son

*(Numerados `F-` de «falla el documento», para no confundirlos con las `P-` de
`PREGUNTAS_ABIERTAS.md`.)*

| # | Documento | Qué dice | Qué es verdad |
|---|---|---|---|
| **F-01** | `CLAUDE.md` | «`requerimientos_v2_final.json`, 43 filas» | El fichero tiene **46**. Las 43 son los requisitos verificados; las otras 3 (`Fibra`, `Taurina`, `L_carnitina`) están para las patologías |
| **F-02** | `canislab-fuentes/TRABAJO_RAWKU/entregas/AUDITORIA_PATOLOGIAS.md` (5-sep) | «las 47 patologías que carga `patologias.json`» y, en su punto 8, que el hipotiroidismo «nunca llegó al motor» | El motor tiene **40** perfiles, e **`hipotiroidismo` existe** —con restricción por alimento (grelo y nabo) y sin tope numérico—. La auditoría se hizo contra el borrador `TRABAJO_RAWKU/code/patologias.json` (47 perfiles, marcado «NADA DE ESTO ESTA VERIFICADO»), que se borró dos días después. **Su lista de 13 huecos puede seguir siendo útil, pero está medida contra el fichero equivocado y al menos un punto es falso** |
| **F-03** | `PENDIENTE.md` / `PENDIENTE_PRODUCTO.md` | «15 ramas ya comprobadas, nada que rescatar» | §4.5 |
| **F-04** | `CLAUDE.md` | «`python3 pruebas_completas.py` — ~2 min» | Medido por otra sesión: 559–959 s según la máquina. Corregido en una rama sin fusionar |

---

## 6 · Qué de esta foto caduca, y por qué

Hay **cuatro sesiones más trabajando ahora mismo**, todas paradas con su
rama sin fusionar:

1. `claude/audit-api-sources-web-gk95ir` (API) + `claude/limpieza-web-appjsx-ci` (web) + `claude/limpieza-fuentes` (fuentes) — **la misma sesión**, limpieza y CI.
2. `claude/nutricion-pendiente-vuoobq` (API) — **nivel 1**, procedencia del catálogo.
3. `claude/veterinary-mode-ui-fixes-s9l5j7` (API) + `claude/vet-margen-por-patologia` (web) — **nivel 1**, márgenes por patología.
4. `claude/veterinario-arranque-y-rueda` (web) — nivel 2, nadie la mencionó.

**Dos de las cuatro están tocando el nivel 1**, y las dos tocan cosas
distintas (una el catálogo, otra las patologías), así que **no se pisan entre
sí**. Ninguna toca `requerimientos_v2_final.json` ni `seguridad.py`.

**Caduca si esas ramas se fusionan:** §1.2 entera (el catálogo cambia de
1.213 líneas), §1.4 (la fila de `margen_del_profesional` pasaría a `main`),
§4 entera, §5 F-03 y F-04.

**No caduca:** §1.7 y §1.8 (el choque renal+pancreatitis no lo toca nadie),
§3 entera (los cuatro sitios donde el nivel 2 pisa el nivel 1: ninguna sesión
está en eso), §1.3 (`seguridad.py` no lo toca nadie).

---

## 7 · Qué se hace al terminar cualquier trabajo

- Actualizar este fichero.
- Si se ha cerrado algo del nivel 1: escribirlo en `DECISIONES.md` con su
  ficha y su test.
- Si queda una pregunta: a `PREGUNTAS_ABIERTAS.md` con dueño. **Nunca en un
  comentario del código.**
- Una rama por tarea, PR pequeño, fusionar, borrar. Una rama vieja es una
  decisión perdida esperando a repetirse.

### Cómo se relaciona esto con `PENDIENTE.md`

No lo sustituye, y conviene no acabar con dos listas que dicen lo mismo:

- **`ESTADO.md`** (esto) — **dónde estamos**: qué existe, en qué estado, con
  qué medida. Se lee para saber si algo ya está hecho.
- **`PENDIENTE.md` y sus cuatro ficheros** — **qué falta**, priorizado. Se lee
  para saber qué hacer a continuación.
- **`DECISIONES.md`** — **qué no se vuelve a discutir**.
- **`PREGUNTAS_ABIERTAS.md`** — **qué no sabemos y quién lo puede contestar**.

Cuando un punto de `PENDIENTE.md` se cierra, la decisión va a
`DECISIONES.md` y la línea de aquí cambia de estado. `HECHO.md` sigue siendo
el histórico narrado.
