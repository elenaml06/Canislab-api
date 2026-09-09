# PREGUNTAS ABIERTAS — lo que no sabemos, y quién lo puede contestar

Abierto el 8 de septiembre de 2026.

Una auditoría que hace preguntas necesita una vía para que alguien las
conteste, o se acumulan hasta que dejan de leerse. **Aquí cada pregunta lleva
dueño**: quién puede contestarla, no quién la hizo.

**Ninguna pregunta se queda en un comentario del código.** Si la encuentras
ahí, tráela aquí.

---

## Cómo se lee

- **Dueño** — quién puede contestar: **Elena** (producto, alcance, negocio) ·
  **el nutricionista** (criterio clínico) · **una fuente** (se contesta
  leyendo, no opinando) · **medible** (se contesta midiéndolo, y entonces no
  es una pregunta: es trabajo).
- **¿Bloquea?** — si algo no puede cerrarse mientras esto siga abierto.
- **Abierta desde** — la fecha en que se supo, no la de hoy.

**Lo que NO va aquí:** el trabajo pendiente. Eso vive en `PENDIENTE.md` y sus
cuatro ficheros. Aquí solo lo que **no se puede resolver programando**.
Cuando un punto de `PENDIENTE_DECISIONES.md` es de verdad una pregunta para
alguien de fuera, se apunta aquí con un puntero, no se copia.

---

## El registro de preguntas: dónde vive cada una

⚠️ **AÑADIDO EL 9 DE SEPTIEMBRE, y por un fallo repetido.** Las preguntas vivían
en **tres** ficheros con tres numeraciones y tres formas de marcar el cierre, y
ninguno comprobaba a los otros. Resultado: preguntas resueltas y aplicadas en el
motor que seguían abiertas en el documento que va a revisión. El techo de yodo se
bajó de 1400 a 1275 y la pregunta se cerró en dos de los tres sitios; en el
tercero seguía marcada «bloqueante, la que más nos preocupa» y afirmando que el
techo del motor «es el nivel al que la fuente documenta daño». Ya no lo era.

**La regla, desde hoy:**

| Fichero | Qué es | Numeración |
|---|---|---|
| `PREGUNTAS_ABIERTAS.md` (este) | **El registro.** Toda pregunta viva figura aquí, con dueño | `P-nn` para las propias · el índice de abajo para las del documento de revisión |
| `PARA_EL_NUTRICIONISTA.md` | El documento de revisión. Las preguntas van **en su contexto**, que es como se contestan | `PREGUNTA n`, indexadas aquí abajo |
| `PREGUNTAS_PARA_ELENA.md` | **Histórico** de la sesión del 8-9 de septiembre. No se le añaden preguntas nuevas | `§ n` |

**Nada se borra al cerrarse.** Se tacha, se dice con qué fuente se cerró y se deja.
Una pregunta borrada se vuelve a hacer dentro de seis meses, y entonces no hay
manera de saber que ya se había contestado.

**Y tres estados, no dos:** `abierta` · `reducida` (la fuente contestó una parte y
lo que queda es más estrecho) · `cerrada`. La mayoría de lo que se cierra leyendo
pasa por «reducida» antes: la fuente casi nunca contesta la pregunta entera.

### Índice de `PARA_EL_NUTRICIONISTA.md`

Lo vigila el **BLOQUE 66**: si una pregunta aparece o desaparece del documento, o
cambia de estado, y este índice no se actualiza, la batería lo dice. Sin eso,
«acordarse» es la única garantía, y ya se ha visto lo que vale.

| Pregunta | Estado |
|---|---|
| 1 | abierta |
| 2 | abierta |
| 3 | abierta |
| 4 | abierta |
| 5 | abierta |
| 6 | abierta |
| 7 | abierta |
| 8 | abierta |
| 9 | abierta |
| 10 | reducida |
| 11 | reducida |
| 12 | reducida |
| 13 | abierta |
| 14 | abierta |
| 15 | reducida |
| 16 | cerrada |
| 17 | reducida |
| 18 | cerrada |
| 19 | abierta |
| 19-bis | cerrada |
| 19-ter | abierta |
| 20 | abierta |
| 21 | abierta |
| 21-bis | abierta |
| 21-quater | abierta |
| 22 | abierta |
| 23 | abierta |
| 24 | abierta |
| 25 | abierta |
| 26 | abierta |
| 27 | abierta |
| 28 | abierta |
| 29 | abierta |
| 30 | abierta |
| 31 | abierta |
| 32 | abierta |
| 33 | abierta |
| 34 | reducida |
| 36 | abierta |
| 37 | abierta |
| 38 | abierta |
| 35 | retirada — se cerró y se sacó del documento el 9 de septiembre |

---

## Bloqueantes

### ~~P-01 · La grasa en pancreatitis: ¿20 o el rango de SACN5?~~ ✅ CERRADA

| | |
|---|---|
| **Resuelta** | **8 de septiembre de 2026**, aplicando la regla de fuentes del propio proyecto |
| **Decisión** | **37,5 g/1000 kcal** (SACN5 Tabla 67-3, «Fat ≤15% for non-obese and non-hypertriglyceridemic dogs»). Merck (20) queda como referencia más estricta, no como el valor aplicado |
| **Por qué** | Manda FEDIAF; donde FEDIAF no llega, SACN5. Ni FEDIAF ni el Reglamento (UE) 2020/354 cubren la pancreatitis — la entrada 19 del Reglamento es la insuficiencia pancreática **exocrina**, que es otra cosa, y no pone cifra de grasa. Luego manda SACN5, y Merck es fuente terciaria |
| **Y resolvió el caso** | `renal` + `pancreatitis` vuelve a dar menú: verde, peldaño 5, grasa 37,5 y fósforo 1198,8. No había incompatibilidad clínica entre las dos patologías; había un número que no era el de la fuente que manda |
| **Hallazgo al medirlo** | Los **dos** topes de la pancreatitis son incompatibles entre sí en peldaño estricto, y ya lo eran con los 20: con proteína ≤75 hace falta grasa ≈78, y con grasa ≤37,5 hace falta proteína ≈148. Son 600 de las 1000 kcal entre las dos y las otras 400 tendrían que venir de carbohidrato. Lo salva el último peldaño de la escalera, que suelta el techo del 10 % de verdura — y que está puesto ahí precisamente por un caso de pancreatitis |
| **Dónde** | `PATOLOGIAS.md` §1.5, `CERRADO.md` |

**Lo que sabemos, medido.** Hoy el tope es **20 g/1000 kcal**, y sale del
Merck Veterinary Manual, literal: *«feeding a low-fat diet (ie, less than 20 g
fat/1,000 kcal) is crucial for treatment success»*. La otra fuente del mismo
campo, **SACN5 5ª ed. cap. 67, Tabla 67-3**, da **≤15 % de materia seca** para
perros no obesos y no hipertrigliceridémicos, y **≤10 %** para los que sí. Con
el puente de 4000 kcal/kg MS que usa el repo, eso son **37,5** y **25**.

**Y la elección entre las dos fuentes decide si un perro come.** Medido el 8
de septiembre (adulto 25 kg, DER 1200, los seis peldaños de la escalera):

| Tope de grasa | `renal` + `pancreatitis` |
|---|---|
| 20 (Merck, el de hoy) | **no sale menú** |
| 25 (SACN5, 10 % MS) | no sale menú |
| 37,5 (SACN5, 15 % MS) | **sale menú** |

**Las preguntas:**

1. ¿El objetivo de grasa en pancreatitis canina es un número o un rango? La
   nutricionista ya dijo que **ha tenido que bajarlo mucho en ciertos casos y
   que depende del caso** — si eso es la respuesta, esto deja de ser pregunta
   y pasa a ser trabajo: se implementa como rango con palanca del veterinario
   y el 20 se queda como valor por defecto.
2. Si es un rango, **¿cuáles son sus dos extremos, y qué variable clínica
   mueve dentro de él?** (triglicéridos, episodio agudo vs. crónico, obesidad
   concurrente).
3. **¿Qué se hace mientras tanto con un perro renal y pancreático?** Hoy no
   recibe menú y el mensaje que lee es el genérico de «quita alguna
   restricción», que a un veterinario no le sirve porque no hay ninguna que él
   pueda quitar.

**El puente que hay debajo, y que también hay que revisar:** convertir «% de
materia seca» a «g/1000 kcal» se hace suponiendo **4000 kcal de EM por kg de
materia seca**. Ese número **no viene de SACN5**: es la densidad de referencia
del repo. Y es sensible en la dirección que importa — una ración baja en grasa
es *menos* densa, no más:

| Densidad supuesta | 15 % MS equivale a |
|---|---|
| 3500 kcal/kg MS | 42,9 g/1000 kcal |
| **4000 (el que se usa)** | **37,5** |
| 4500 kcal/kg MS | 33,3 |

Ver también `PENDIENTE_DECISIONES.md` → «Límites por patología: confirmar los
números (fósforo, cobre, grasa)», que es la misma pregunta apuntada antes sin
la medida.

---

### P-02 · Los siete márgenes «interpretados» del veterinario

| | |
|---|---|
| **Dueño** | **El nutricionista** |
| **Bloquea** | Sí: son la mitad de la ficha de permisos, y si están mal el veterinario tiene una palanca que no debería |
| **Abierta desde** | 8 de septiembre de 2026 |

La rama `claude/veterinary-mode-ui-fixes-s9l5j7` estructura, para los 19 topes
y suelos de `patologias.json`, hasta dónde podría moverlos un profesional.
**Doce salen de un rango escrito en la fuente. Siete los puso la sesión**, y
hay un patrón en los siete: **la fuente da un solo número, y se usó el mínimo
de FEDIAF como la otra punta del rango.**

Eso no es lo mismo: **FEDIAF es el suelo de un perro sano, no el suelo
terapéutico de esa patología.**

| # | Patología · nutriente | `hasta` | Por qué hay que revisarlo |
|---|---|---|---|
| 3 | pancreatitis · proteína | 52,1 | El extremo de SACN5 (37,5) está BAJO el mínimo de FEDIAF; se puso el mínimo de FEDIAF como parada |
| 6 | hepatopatía · cobre | `null` | El objetivo terapéutico (1,2) está bajo el mínimo de FEDIAF (2,08): el margen real es cero sin prescripción. Probablemente debería ser `direccion: null`, como renal |
| 7 | cardiopatía genérica · sodio | 480 | Se puso el valor del estadio D. Discutible: la entrada genérica existe justo porque NO se sabe el estadio |
| 10 | cardiopatía D · sodio | 290 | 290 es el mínimo de FEDIAF, no una cifra de la fuente |
| 11 | hiperlipidemia · grasa | 13,75 | La fuente da UN número; 13,75 es el mínimo de FEDIAF |
| 13 | obesidad · grasa | 28 | **No es nutrición: es ingeniería.** 28 es un límite MEDIDO del solver con el catálogo real (22,5 y hasta 27 no dan menú ni en 40 s; 28 sí, 5 de 5). Mezcla una cifra de máquina con las de fuente y merece campo aparte |
| 16 | PLE / linfangiectasia · grasa | 13,75 | La fuente no da suelo; 13,75 es el mínimo de FEDIAF |

**Las preguntas:** ¿en cada uno de los siete, cuál es el suelo terapéutico
real, y qué lo mueve? Y en el 13, ¿tiene sentido que un límite del solver
viaje en el mismo campo que un límite clínico, o hay que separarlos?

**No verificado por mí:** los doce «de prosa clara». Sí verificado: que la
rama **no cambia ni un valor** de los 19 topes ni de los 40 `formulable`.

---

### P-03 · ¿Un veterinario puede RELAJAR un tope de patología?

| | |
|---|---|
| **Dueño** | **Elena** (es alcance de producto) **con el nutricionista** |
| **Bloquea** | Sí: sin esto, `margen_del_profesional` no puede pasar de texto a control |
| **Abierta desde** | 8 de septiembre de 2026 |

Uno de los 19 márgenes tiene `direccion: "subir"` **sobre un tope** —
pancreatitis · grasa. Subir un tope es **relajarlo**. Es correcto según la
fuente, pero es la línea que más fácil se lee mal, y **hoy las reglas 2 y 3
del `CLAUDE.md` no se lo permiten a nadie**.

**Las preguntas:**

1. ¿Un veterinario acreditado puede relajar un tope de patología, o solo
   apretarlo?
2. Si puede, ¿eso sigue siendo «una dieta completa» o pasa a ser una
   **prescripción**, con constancia de quién la firma? (`VETERINARIOS.md` ya
   dice que una prescripción por debajo de FEDIAF se verifica igual, contra un
   juego de requisitos escrito que viaja con el menú. La pregunta es si esto
   es ese caso.)
3. ¿Qué se registra al moverlo? La ficha pide: quién, cuándo, a qué valor,
   sobre qué dato de entrada, y **si el cambio saca la ración de lo que es una
   dieta completa**.

**Lo que se buscó y lo que se encontró (8 de septiembre, tarde).** Se fue a
buscar documentación veterinaria que dijera de qué límites se puede salir un
profesional y de cuáles no. La respuesta existe y está guardada
(`canislab-fuentes/Reglamento_UE_2020_354/`), pero **contesta una pregunta
distinta de la que hacía falta, y conviene no confundirlas**:

- **Sí contesta quién y por qué vía.** El Reglamento (UE) 2020/354 fija, para
  20 objetivos clínicos caninos, una característica nutricional esencial con su
  cifra y su duración, y le da al veterinario un papel explícito: decidir
  **empezar** y decidir **prolongar** (*«before use and before extending the
  period of use»*). Ver `DECISIONES.md` D-12.
- **No contesta hasta dónde.** No hay, por patología y por nutriente, un rango
  con un extremo movible. Hay **un techo (o un suelo) por objetivo**, y punto.
  Lo que la norma pone como rango es **el tiempo**, no la cifra. El único
  porcentaje del texto (±15 %, parte A punto 2) es **tolerancia analítica de
  fabricación**, no margen clínico.
- **Y pone un límite a la relajación** que hoy no está escrito en el motor
  —nota al pie (11)—: los mínimos de FEDIAF para los ácidos grasos esenciales
  hay que cumplirlos **aunque** se esté aplicando un techo terapéutico.

O sea: **esta pregunta sigue abierta tal cual**, y el margen por nutriente sigue
saliendo solo de las tablas de *key nutritional factors* de SACN5, que es donde
una fuente escribe un rango a propósito. Lo que ha cambiado es que ahora se sabe
que **no hay una fuente normativa que dé ese rango**, así que la respuesta tendrá
que ser criterio del nutricionista, declarado como tal.

---

### P-10 · Un tope nuestro recorta hasta un tercio la fórmula de lactancia de FEDIAF

| | |
|---|---|
| **Dueño** | **El nutricionista**, y **Elena** para decidir si la lactancia debe ser automática |
| **Bloquea** | Sí para una perra grande con camada grande |
| **Abierta desde** | 8 de septiembre de 2026 |

⚠️ **Corrige una versión anterior de esta entrada**, que decía que el motor
daba de más comparado con SACN5. Al leer FEDIAF entero resultó lo contrario:
**la fórmula del motor ES la de FEDIAF, exacta**, y lo que sobra es un techo
nuestro que la recorta.

**FEDIAF 2025, Tabla VII-8b, literal:**

> *1 to 4 puppies: 145 × kg BW^0.75 + 24 n × kg BW × L*
> *5 to 8 puppies: 145 × kg BW^0.75 + [96 + 12 (n−4)] × kg BW × L*
> *L = 0.75 in week 1; 0.95 in week 2; 1.1 in week 3 and 1.2 in week 4*

El motor implementa eso letra por letra. **Lo que no es de FEDIAF es
`LACTANCIA_TOPE_RER = 6.0`**: FEDIAF no pone ningún techo. El nuestro sale de
SACN5 Tabla 5-2, donde el ×6 **no es un techo general: es la fila de camadas
de ≥9 cachorros**.

Medido en semana 4:

| Perra | Cachorros | FEDIAF | Le damos | |
|---|---|---|---|---|
| 25 kg | 6 | 5221 kcal | 4696 | **−10 %** |
| 40 kg | 8 | 9218 kcal | 6680 | **−28 %** |
| 60 kg | 8 | 13 494 kcal | 9054 | **−33 %** |

⚠️ **Y el comentario del código decía que esta parte venía de una fuente
secundaria «que no se ha podido contrastar con el texto original de FEDIAF».**
Sí se puede, y cuadra. Ese comentario es lo que hizo que nadie volviera a
mirarlo, y además se usó para justificar el recorte. Ya está corregido en
`der.py`.

**Las preguntas:** ¿se quita el tope y se sigue a FEDIAF? Si se mantiene algún
techo, ¿cuál y con qué respaldo? ¿O la app no debería dar menú automático en
lactancia?

**No aplicado a propósito:** el DER manda desde el front y hay un contrato de
100 casos compartido entre los dos repos; cambiar la ración de una perra
lactante no lo decide una sesión sola.

---

### ~~P-11 · FEDIAF da cifras para dos razas que la app tiene y el motor ignora~~ ✅ CERRADA

| | |
|---|---|
| **Resuelta** | **9 de septiembre de 2026**, leyendo la Tabla VII-7 con su frase de entrada y la sección 7.2.3.4 de la misma guía |
| **Decisión** | Las dos cifras se adoptan, y son **EN VEZ** del nivel de actividad. No son un suelo sobre el que se suma la actividad, ni un ajuste que se añada |
| **Ya estaba aplicado** | Sí, desde el 8 de septiembre, en `der.py` y en `src/der.js` (`RAZAS_CIFRA_FEDIAF`). Lo que faltaba era la lectura que dice que esa forma de aplicarlo es la correcta |
| **Dónde** | `PARA_EL_NUTRICIONISTA.md` §1.1, `HISTORIA_TECNICA.md` (duplicación del DER) |

**La primera prueba: la propia tabla.** La frase que la presenta, literal:

> *«Table VII-7 provides examples of daily energy requirements of dogs at
> different activity levels, for specific breeds and for obese prone adults.
> It is a good alternative to table VII-6 to estimate the energy requirements
> of adult dogs.»*

Son **tres clases de ejemplo en paralelo** —niveles de actividad, razas
concretas, y el perro con tendencia a la obesidad—, todas en la **misma
columna**, `kcal ME per kg BW^0,75`, y todas dando un valor del mismo
coeficiente. Una fila de raza es una **alternativa** a una fila de actividad,
igual que `Obese prone adults ≤ 90` es una alternativa y no un descuento que
se reste al 95 del sedentario. Sumarlas sería sumar dos veces la misma
columna.

**La segunda, y es la que lo cierra:** FEDIAF explica de qué está hecha la
diferencia de raza, sección **7.2.3.4 «Breed & type»**, literal:

> *«Breed-specific needs probably reflect differences in temperament,
> resulting in higher or lower activity, as well as variation in stature or
> insulation capacity of skin and hair coat.»*

O sea que la diferencia de raza **ya contiene** la diferencia de actividad.
Aplicar encima un nivel de actividad sería contar dos veces lo mismo, y por
eso «suelo sobre el que se aplica» no era una lectura posible: el 200 no está
midiendo un gran danés parado, está midiendo gran daneses.

**Lo único que FEDIAF no resuelve es dónde caer dentro del rango publicado.**
Da `200 (200-250)` y `105 (80-132)` y ninguna regla para colocarse. El motor
coloca por actividad —la diferencia contra «normal»— y **recorta al rango de
FEDIAF**, que es lo que mantiene cada resultado dentro de lo que publica la
fuente. Eso sigue siendo interpretación nuestra, y está declarada. Medido hoy
en los dos repos, que dan lo mismo:

| Gran Danés 67,5 kg | coef | kcal/día |
|---|---|---|
| sedentario | 200 (recortado) | 4710 |
| normal | 200 | 4710 |
| activo | 215 | 5063 |
| muy activo | 240 | 5652 |
| trabajo | 250 (recortado) | 5887 |
| senior, normal | 200 (recortado) | 4710 |

**Consecuencia práctica para el gran danés: «en vez de» y «suelo» coinciden.**
Como 200 es a la vez el valor central y el extremo bajo del rango, ningún
ajuste a la baja —sedentario, senior— puede bajar de ahí. Para el terranova
no coinciden, porque su rango abre hacia los dos lados: sedentario da 90 y
trabajo 132.

---

### ~~P-12 · El escalón intermedio de crecimiento (2,5 × RER) no tiene fuente~~ ✅ CERRADA

| | |
|---|---|
| **Resuelta** | **8 de septiembre de 2026**, aplicando la única fuente que da cifra |
| **Decisión** | Fuera el escalón intermedio, y el corte pasa a ser por **edad**: **210** (3 × RER) antes de los 4 meses, **140** (2 × RER) desde los 4 meses |
| **Alcance** | Solo el camino de respaldo: cuando **no** se conoce el peso adulto esperado. Conociéndolo manda la curva continua de Klein 2019 |
| **Dónde** | `der.py` y `src/der.js` (`CRECIMIENTO_SACN5_MESES`, `CRECIMIENTO_ANTES_4M`, `CRECIMIENTO_DESDE_4M`), contrato de 100 casos |

Había **210 / 175 / 140** por tramos del 50 % y el 80 % del peso adulto. Dos
de los tres números tienen fuente y el de en medio no. SACN5 Tabla 5-2,
parte 2, literal:

> *«Daily energy intake for growing puppies should be 3 x RER from weaning
> until four months of age. At four months of age energy intake should be
> reduced to 2 x RER until the puppy reaches adult size.»*

3 × RER = **210** ✓ · 2 × RER = **140** ✓ · **2,5 × RER = 175: no está en
ninguna parte**, y el criterio de corte tampoco coincidía — SACN5 corta por
**edad** y el motor cortaba por **% del peso adulto**, que en este camino ni
se conoce.

**Y había un segundo fallo debajo, que es el que dolía.** El código leía
**siempre el último** escalón, en los dos repos: un cachorro de dos meses sin
peso adulto esperado recibía **140**, que es lo que SACN5 da para **después**
de los cuatro meses. El escalón sin fuente no solo sobraba: tapaba que los
otros dos no se estaban usando.

---

### P-13 · A ≤ RER, AAHA recomienda dieta terapéutica — y Rawku no lo es

| | |
|---|---|
| **Dueño** | **El nutricionista**, y **Elena** para el alcance |
| **Bloquea** | No, pero afecta a todos los perros con sobrepeso |
| **Abierta desde** | 8 de septiembre de 2026 |

A un perro con sobrepeso el motor le da exactamente el **RER de su peso
ideal** (1,0 × RER). Está bien apoyado: coincide con SACN5 Tabla 5-2 («Weight
loss = 1.0 x RER») y es **más estricto** que el «obese prone ≤ 90» de FEDIAF
VII-7.

Pero AAHA 2021 dice, literal: *«Therapeutic weight loss diets are recommended
for patients undergoing significant calorie restriction (less than or equal to
RER) for weight loss.»* A ese nivel de kcal, **la ventana entre los mínimos
escalados y los máximos se estrecha** (es el mismo mecanismo que hace que el
selenio se cruce en DER 45,2).

**Y hay algo más, que conviene decir en voz alta:** la Tabla 4 de AAHA 2021
(«Nutritional Screening: Risk Factors») lista literalmente *«Unconventional
diet (e.g., **raw meat based, home prepared**, vegetarian, vegan)»* entre los
factores de riesgo que justifican una evaluación nutricional extendida. Eso es
exactamente lo que produce Rawku.

**Las preguntas:** ¿es aceptable adelgazar a 1,0 × RER con una ración BARF, o
hay que ser menos agresivo (1,2 × RER) para que quepan los nutrientes? ¿Y qué
debería decirle la app al dueño sobre lo de AAHA?

---

## No bloqueantes

### P-04 · El techo de lisina de FEDIAF: ¿sobre qué proteína se mide?

| | |
|---|---|
| **Dueño** | **El nutricionista** |
| **Bloquea** | No — hay decisión provisional escrita (`DECISIONES.md` D-03) |
| **Abierta desde** | 28 de agosto de 2026 |

El techo (7,00 g/1000 kcal, solo en crecimiento) no se aplica porque **0 de 15
menús de cachorro caben debajo**: la lisina va detrás de la proteína y una
ración BARF de cachorro lleva ~134 g/1000 kcal contra un mínimo de 50.
Aplicarlo dejaría a todos los cachorros sin menú.

**La pregunta:** ¿ese techo está pensado para una dieta con la proteína
ajustada al mínimo, y por eso no es transferible a una ración cruda? ¿O
estamos midiendo algo distinto de lo que él mide? Es el único máximo de FEDIAF
que no aplicamos, y un revisor externo va a preguntar por él el primer día.

Ya estaba apuntada en `PENDIENTE_DECISIONES.md`. Aquí solo con dueño y fecha.

---

### P-05 · El mínimo de EPA+DHA de adulto no es de FEDIAF

| | |
|---|---|
| **Dueño** | **El nutricionista** |
| **Bloquea** | No |
| **Abierta desde** | 26 de agosto de 2026 |

FEDIAF 2025 solo exige EPA+DHA en crecimiento y reproducción (0,13 g), y para
adulto dice literalmente que *«the current information is insufficient to
recommend a specific level of omega-3 fatty acids for adult dogs»*. Nuestro
mínimo de adulto (0,11 g = 110 mg/1000 kcal) **viene del NRC 2006 y lo
adoptamos a propósito** por su relevancia clínica documentada.

Es, por tanto, **criterio nuestro**, no un requisito. Está escrito en el
`nota_auditoria` de la fila, pero no marcado como criterio en ninguna parte
legible por un revisor.

**La pregunta:** ¿se mantiene, se sube, se baja, o se retira y se deja como
recomendación en vez de como mínimo duro?

---

### P-06 · Los umbrales de seguridad crónica son criterio nuestro. ¿Cuáles cambian?

| | |
|---|---|
| **Dueño** | **El nutricionista** |
| **Bloquea** | No, pero es de lo primero que va a mirar |
| **Abierta desde** | 5 de agosto de 2026 |

La cabecera de `motor/seguridad.py` lo dice sin adornos: *«los MECANISMOS
están documentados con estudios reales; los NÚMEROS DE CORTE (10 %, 5 %, 4 %,
10 %) son CRITERIO DE DESARROLLO nuestro, salvo el 20 % de clara cruda, que es
donde se midió daño»*.

Concretamente:

| Umbral | Valor | Qué lo respalda |
|---|---|---|
| Tiaminasa | 10 % de las kcal del día | El mecanismo (Markovich 2013, JAVMA). **La cifra, no**: la literatura dice «proporción sustancial de la dieta», sin número |
| Mercurio | 10 % de las kcal del día | Extrapolado de la dosis de referencia humana de la EPA. **No existe límite canino**, y así se dice en Dunham-Cheatham 2019 |
| Hígado | 10 % del peso | Criterio |
| Vísceras metabólicas | 10 % del peso | Criterio |
| Clara cruda | 5 % del peso | **El único con daño medido** (20 %) |
| Oxalato | 100 % del peso en sano, 0 con antecedente | Criterio |

**Las preguntas:** ¿alguno de estos seis está mal puesto, en un sentido o en
el otro? ¿Y alguno debería depender del caso —o sea, ser un rango con palanca
del veterinario— en vez de una constante?

---

### P-07 · Las 13 condiciones clínicas sin perfil

| | |
|---|---|
| **Dueño** | **Elena** (alcance) primero, **el nutricionista** después |
| **Bloquea** | No |
| **Abierta desde** | 5 de septiembre de 2026 |

`canislab-fuentes/TRABAJO_RAWKU/entregas/AUDITORIA_PATOLOGIAS.md` lista 13
condiciones estudiadas sin perfil en `patologias.json`: estreñimiento,
megaesófago, enfermedad periodontal, gastroenteritis aguda, SIBO, intestino
corto, flatulencia, hipotiroidismo, urolitiasis por sílice, realimentación
tras anorexia, hipertensión sistémica, acidosis tubular renal y gastritis
aguda.

⚠️ **Antes de usar esa lista hay que arreglar su premisa.** Dice auditar «las
47 patologías que carga `patologias.json`»; **el motor tiene 40**, y la lista
de 47 es la del borrador `TRABAJO_RAWKU/code/patologias.json`, marcado «NADA
DE ESTO ESTA VERIFICADO», que se borró dos días después (`DECISIONES.md`
D-07). **Y al menos un punto es falso por eso:** el 8 dice que el
hipotiroidismo «nunca llegó al motor», y `hipotiroidismo` **sí está** en
`patologias.json`, con restricción por alimento (grelo y nabo, por la
progoitrina) y sin tope numérico.

**Las preguntas:** ¿cuáles de las 13 quiere Rawku cubrir? Y de las que sí:
¿tienen objetivo nutricional formulable, o son de las que bloquean?

---

### P-08 · Se borró la lista viva de preguntas para la nutricionista

| | |
|---|---|
| **Dueño** | **Elena** (tiene el PDF que se le envió a Cris el 29 de agosto y su respuesta) |
| **Bloquea** | No, pero se pierde si nadie lo recupera |
| **Abierta desde** | 7 de septiembre de 2026 |

El `PREGUNTAS_NUTRICIONISTA.md` del borrador de `canislab-fuentes` está
marcado **«SUPERADO — 3 de septiembre»**, y remite a `datos_motor.json →
huecos_para_nutricionista` y a `MOTOR.md §6` como la lista vigente. **Los
tres se borraron el 7 de septiembre**, en la limpieza de `TRABAJO_RAWKU`, y
con buen motivo (`DECISIONES.md` D-07).

O sea que **la lista vigente de preguntas para la nutricionista, y la
respuesta que ella ya dio y que cambió tres de ellas, no están hoy en ningún
repo.** Están en el PDF del 29 de agosto y en la respuesta de Cris.

**La pregunta / la petición:** ¿se puede recuperar ese contenido de la rama
`add-sacn5-58-capitulos` (que aún existe) o del PDF, para traerlo a este
fichero antes de que la rama se borre?

Ver también `PENDIENTE_DECISIONES.md` → «Siete preguntas para Cris».

---

### P-09 · ¿Dónde deben vivir las fuentes?

| | |
|---|---|
| **Dueño** | **Elena** |
| **Bloquea** | No |
| **Abierta desde** | 8 de septiembre de 2026 |

**Los números, medidos hoy:** `canislab-fuentes` ocupa **553 MB** en disco, de
los que `sacn5/` son **293 MB** (70 PDFs) y su `.git` pesa **246 MB**. Los 70
`.txt` extraídos con `pdftotext -layout` ocupan **7,1 MB entre todos**, y las
tablas sobreviven a la extracción (comprobado en la Tabla 6-1 del cap. 6). En
la documentación se cita el `.txt` seis veces y el `.pdf` dos.

**Las cuatro opciones, con su coste:**

| | Qué se gana | Qué cuesta |
|---|---|---|
| **(a) Dejarlo** | 0 de trabajo, 0 de riesgo | Cada clon se lleva 246 MB, siempre |
| **(b) `git lfs migrate`** | El clon baja a ~22 MB | **Reescribe el historial entero**, exige `force-push`, y **el carril anónimo de git de estas sesiones no sirve objetos LFS**: una sesión de Claude Code se bajaría los PDFs como punteros vacíos |
| **(c) `git filter-repo` y los PDFs fuera de git** | Máximo ahorro, repo limpio | Mismo coste que (b), **más** que los PDFs dejan de estar versionados: si se pierde la copia, se perdió. Son la copia legal |
| **(d) Repo aparte** | — | Dos repos que mantener, y **no arregla nada solo**: el historial seguiría cargando los 246 MB |

**Recomendación: (a), por ahora.** Es lo único de toda la limpieza que es
irreversible, y el problema que resuelve es incomodidad, no corrección.
**Lo que sí conviene decidir ya es no meter más PDFs grandes sin pensarlo**,
porque el coste de arreglarlo sube con cada uno.

**Y la parte que sí es una respuesta, no una opción:** las fuentes **no pueden
depender de que sigan en un ordenador**. Ya están en `canislab-fuentes` y ahí
deben quedarse. Para FEDIAF el PDF **sí hace falta** (2,6 MB) por el riesgo de
columnas pegadas en las tablas III-3a/III-3b; para SACN5, el `.txt` basta y el
PDF es respaldo.

---

## Cerradas

*(Cuando una pregunta se contesta, se mueve aquí con la respuesta, la fecha y
quién la dio — y si de ella sale una decisión, se escribe en `DECISIONES.md`
y se enlaza.)*

Ninguna todavía.
