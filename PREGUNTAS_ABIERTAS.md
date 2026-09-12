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
| 1 | reducida |
| 2 | reducida |
| 3 | reducida |
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

**⚠️ REDUCIDA el 10 de septiembre: la mitad de código ya está hecha.** Esta ficha
decía «sin esto, `margen_del_profesional` no puede pasar de texto a control». Ha
pasado: las **79 cifras** de `patologias.json` llevan ya su ventana
(`margen_profesional`) con suelo, techo y **la procedencia de cada extremo como
una clave que se resuelve** contra la fuente viva; `GET /patologias` la sirve; y
el **BLOQUE 80** rehace las 79 y exige que la cifra aplicada caiga dentro. El
día que se escribió cazó que el sodio cardíaco (739) estaba medio miligramo por
encima de su propio techo legal (738,6).

**Lo que queda abierto es ahora una sola pregunta, y más estrecha:** dentro de esa
ventana, ¿el veterinario mueve libremente, o hay cifras que no debería tocar
aunque quepan? El motor sabe hoy **dónde están los bordes**; lo que no sabe —y
ninguna fuente contesta— es si el interior es todo suyo. Sigue siendo criterio
del nutricionista, y sigue bloqueando el control de la pantalla, no el dato.

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

### ~~P-04 · El techo de lisina de FEDIAF: ¿sobre qué proteína se mide?~~ ✅ CONTESTADA POR LA FUENTE (10 sep)

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

**⚠️ CERRADA EL 10 DE SEPTIEMBRE, leyendo §3.3.1 de FEDIAF entera** (antes solo
se había leído la fila de la tabla, y la explicación no está en la tabla):

> *«Czarnecki et al. (1985) showed that excess dietary lysine (4.91 % DM [basal
> diet 0.91 % + 4 % from a supplement]) decreases weight gain in puppies but not
> 2.91 % DM (basal diet and 2 % from a supplement).»*
>
> *«It was concluded that the highest no-effect-level of lysine for puppies was
> 2.91 % DM (energy density 4156 kcal/kg or 17.39 MJ/kg). This is equivalent to
> 7.0 g/1000 kcal (1.67 g/MJ) or 2.8 % DM (at 4 kcal/g DM) and this is therefore
> the FEDIAF maximum for puppy growth.»*

⚠️ **La cita estaba mal copiada hasta el 12 de septiembre**, y lo cazó
`auditar_citas.py` al empezar a mirar este fichero: los decimales se habían
pasado a coma española **dentro de las comillas** (4,91 en vez de 4.91), se había
metido una negrita dentro de la cita y dos puntos suspensivos se comían la mitad
de la frase. Ninguna de las tres cosas cambia el número ni la conclusión, y las
tres son exactamente lo que este auditor existe para encontrar.

**No se mide sobre la proteína: es lisina TOTAL de la dieta**, y el daño se vio
**añadiendo lisina libre**, no comiendo más carne. Eso no cambia la decisión —el
techo sigue sin aplicarse porque 0 de 12 menús de cachorro caben debajo— pero la
deja mucho mejor sostenida: nuestros 8-11 g vienen de la proteína del alimento,
que no es lo que el estudio midió. Detalle en `HALLAZGOS_LECTURA_FUENTES.md`
F-17.

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

### P-10 · ¿Hay un punto en el que bajar el sodio de un cardiópata sea malo?

| | |
|---|---|
| **Dueño** | **Cris Carles** (o quien firme la pauta) |
| **Bloquea** | No: hoy el motor entrega menú. Pero si la respuesta es sí, hoy lo entrega **por debajo** de donde la fuente avisa |
| **Abierta desde** | 11 de septiembre de 2026, al cerrar el cap.18 de Fascetti |

Es **la única frase de toda la lectura de las cuatro fuentes que dice que un
tope puede ser demasiado BAJO**. Todo lo demás son techos que aprietan y suelos
que exigen; esto es un techo con fondo.

> «Severe sodium restriction (<50 mg/100 kcal) is not recommended as this can
> cause early and prolonged activation of the renin-angiotensin-aldosterone (RAA)
> system.»
> — Fascetti & Delaney 2ª ed., cap.18

**Los números, todos en mg/1000 kcal:**

| | |
|---|---|
| Línea que la fuente llama «restricción severa, no recomendada» | **500** |
| Lo que el motor aplica al **estadio ACVIM D** | **480** |
| Lo que el motor aplica al **estadio C** | 625 |
| Estudio **canino** del mismo capítulo, con beneficio medido | 400 |
| Lo que recomienda Fascetti para el estadio C canino | <800 |

**Los dos matices que impiden aplicarlo solo**, y por eso es pregunta y no
cambio: la frase del <500 está en el apartado **felino** (miocardiopatía
hipertrófica), y el estudio **canino** que cita el mismo capítulo usó 400 y
redujo el tamaño cardíaco. Nuestro 480 sale del consenso ACVIM 2019, que es
canino y es la fuente de esa patología.

⚠️ **El mecanismo para arreglarlo ya existe y no hay que programar nada**: son
los `suelos_por_1000kcal`, que ya usan 16 patologías y se combinan con `max()`.
Lo único que falta es la cifra.

**La pregunta:** ¿lleva la cardiopatía un suelo de sodio? ¿Y en qué estadios?

---

### P-11 · ¿Lleva el oxalato cálcico un suelo de fósforo?

| | |
|---|---|
| **Dueño** | **Cris Carles** (o quien firme la pauta) |
| **Bloquea** | No |
| **Abierta desde** | 11 de septiembre de 2026, al cerrar el cap.16 de Fascetti |

Dos fuentes que se contradicen, y FEDIAF no entra:

| | Qué dice | mg/1000 kcal |
|---|---|---|
| **SACN5 cap.40, Tabla 40-5** (lo que aplica el motor) | *«Dietary phosphorus should be in the range of 0.3 to 0.6% DM»* | **750-1500** |
| **Fascetti cap.16** | *«Dietary phosphorus should not be restricted... Low dietary phosphorus is a risk factor»*, recomendado *«1.5 to 2.0 g/Mcal»* | **1500-2000** |

Los dos rangos **solo se tocan en 1500**, que es el número que aplica el motor.

⚠️ **Y hay una medida que condiciona la respuesta:** los menús reales salen a
**1498,7 / 1498,6 / 1498,4** (perros de 10, 22 y 30 kg), o sea pegados al techo
pero sin llegar. **Un suelo de 1500 dejaría al oxalato sin menú.** Si la
respuesta es que hace falta suelo, hay que decidir también en qué cifra, y
probablemente subir antes el techo.

**La pregunta:** ¿se queda el fósforo del oxalato solo con techo, o lleva suelo?

### P-14 · FEDIAF publica la curva de crecimiento como ecuación, y el motor usa una copia divulgativa

| | |
|---|---|
| **Dueño** | **Elena** (toca los dos repos y el contrato del DER) |
| **Bloquea** | No, pero sobrealimenta al cachorro de raza grande |
| **Abierta desde** | 11 de septiembre de 2026, releyendo FEDIAF entera |

`der.py` estima el peso adulto de un cachorro con `CURVA_CRECIMIENTO`, una tabla
cuyo propio comentario dice que sale de *«reproducciones divulgativas»* de las
curvas WALTHAM y **no** del texto del estudio. FEDIAF publica la ecuación exacta
en su **Tabla VII-8a**, válida de las 8 semanas al año:

| Peso adulto esperado | % del peso adulto |
|---|---|
| ≤ 7 kg | 36,92 · Ln(semanas) − 43,57 |
| > 7 - 15 kg | 36,86 · Ln(semanas) − 48,22 |
| > 15 - 27,5 kg | 39,88 · Ln(semanas) − 60,70 |
| > 27,5 - 47,5 kg | 36,96 · Ln(semanas) − 56,18 |
| > 47,5 kg | 36,61 · Ln(semanas) − 62,39 |

**Medido, dentro del rango de validez (2 a 12 meses):** en perros pequeños la
diferencia va de −1,5 a +3,2 puntos, pero en los grandes el motor va
**sistemáticamente por debajo**. Un cachorro de más de 47,5 kg de adulto, a los
6 meses, para FEDIAF va por el **57,0 %** y para nosotros por el **45,0 %**.

**Y va en la dirección mala:** menos porcentaje supone un peso adulto estimado
mayor, que en la ecuación de Klein sube el coeficiente. Para un cachorro de
30 kg a los 6 meses son **2479 kcal con nuestra tabla contra 2271 con la de
FEDIAF, un 9 % de más**, justo en la población donde la propia FEDIAF dice que
sobrealimentar *«can result in skeletal deformities especially in large and
giant breeds»*.

**Dos matices antes de tocarlo:**

1. El frontend, que es el que manda, **no tiene esta curva**: si no sabe el peso
   adulto usa los dos escalones de SACN5 por edad. O sea que la Tabla VII-8a no
   solo corregiría `der.py`, **llenaría el hueco que el frontend tapa con otra
   fuente**.
2. ⚠️ **Esta tabla hay que leerla del PDF, no del texto extraído.** Las cinco
   bandas y las cinco ecuaciones salen en dos columnas cruzadas y el orden no es
   el que parece: la banda >15-27,5 lleva −60,70 y la >27,5-47,5 lleva −56,18,
   que **no es monótono**. Las cinco parejas de arriba están leídas del PDF por
   coordenadas.

**APLICADA LA MITAD, el 11 de septiembre**: `der.py` usa ya las cinco
ecuaciones entre los 2 y los 12 meses, y conserva la tabla WALTHAM solo para lo
que FEDIAF no cubre (por debajo de las 8 semanas y por encima del año, donde su
ecuación pasa del 100 %). **No cambia ningún caso del contrato**: los siete
casos de cachorro de `der_casos.json` o traen `pesoAdultoKg` o no traen edad, así
que ninguno ejercía esta curva. Medido después del cambio: el cachorro de 30 kg
a los 6 meses pasa de 2479 a **2142 kcal**. ⚠️ Esa cifra se movió esa misma noche de 2269 a 2142 al quitar la iteración: la Tabla VII-8a es una función a trozos y el bucle tenía **dos puntos fijos** —52,6 kg partiendo del doble del peso y 46,6 partiendo de la media del tamaño, los dos autoconsistentes—, así que `der.py` y la app daban pesos adultos distintos para el mismo perro. Ahora se recorren las cinco bandas y se coge la primera que cae dentro de la suya: determinista, sin semilla, y es la solución más pequeña, que es menos kcal.

**La pregunta que queda, y es la mitad que importa:** ¿se lleva también al
frontend? Allí no hay curva ninguna — si no sabe el peso adulto, `calcularDER`
cae a los dos escalones de SACN5 por edad (3 × RER hasta los 4 meses, 2 × RER
después), que es una fuente distinta y más gruesa. Con la Tabla VII-8a, un
cachorro **mestizo** (los de raza sí traen el peso de `razas.json`) usaría la
ecuación de Klein como todos los demás. Eso **sí** cambia las kcal de usuarios
reales y hay que regenerar `der_casos.json` en los dos repos.

---

### P-15 · FEDIAF dice dos veces que el BCS ideal es 4-5, y el motor toma 5

| | |
|---|---|
| **Dueño** | **Cris Carles** |
| **Bloquea** | No |
| **Abierta desde** | 11 de septiembre de 2026, releyendo FEDIAF entera |

`verificar.BCS_NEUTRO = 5.0`: un perro en BCS 4 se considera **por debajo** del
ideal y se le sube el peso objetivo. FEDIAF lo dice dos veces al revés:

> §7.1.3: *«The ideal BCS should therefore be between 4/9 and 5/9.»*
> §7.2.4.1: *«it is recommended that dogs should be fed to maintain a body
> condition score (BCS) between 4 and 5 on the 9-point BCS.»*

Y no es una opinión suelta: se apoya en Kealy 2002, el estudio de catorce años
con labradores en el que la restricción alargó la vida mediana y retrasó la
enfermedad crónica, con los perros restringidos entre 4/9 y 5/9.

**La pregunta:** ¿el 4/9 es ideal, y entonces no hay que subirle el objetivo, o
se deja el 5 como neutro porque es el lado prudente?

---

### P-16 · La tabla de FEDIAF vale para ingredientes de digestibilidad normal, y no sabemos la nuestra

| | |
|---|---|
| **Dueño** | **una fuente** (BEDCA/CIQUAL/USDA no la publican) y **Cris Carles** |
| **Bloquea** | No |
| **Abierta desde** | 11 de septiembre de 2026, releyendo FEDIAF entera |

§2.2, declarando el alcance: *«These guidelines relate to dog and cat foods
manufactured from ingredients with normal digestibility (i.e. **≥ 70 % DM
digestibility; ≥ 80 % protein digestibility**) and average bioavailability.»*

Es la **condición de validez de toda la tabla** y nunca la hemos mirado: el
catálogo no tiene campo de digestibilidad en ninguna de sus 163 fichas. La carne
cruda va sobrada; el hueso molido, el cartílago y la laringe de vacuno no está
claro que lleguen. Si un menú se apoya mucho en ellos, los mínimos de FEDIAF se
están aplicando fuera de su rango declarado de validez.

**La pregunta:** ¿hace falta el dato por ficha, o basta con un aviso cuando un
menú se apoya por encima de cierto porcentaje en hueso y cartílago?

---

### P-17 · Dos datos que la ficha no pregunta y que mueven la ración

| | |
|---|---|
| **Dueño** | **Elena** (producto) |
| **Bloquea** | No |
| **Abierta desde** | 11 de septiembre de 2026, releyendo FEDIAF entera |

Los dos salen de la misma regla suya: «TODOS LOS DATOS QUE RECOJA LA APP TIENEN
QUE LLEGAR DE ALGUNA MANERA AL MOTOR». Aquí es al revés — son datos que el motor
necesita y la app **no recoge**.

1. **La temperatura a la que vive el perro.** §7.2.4.1: fuera de su zona
   termoneutra la MER sube **2-5 kcal por kg^0,75 y por cada grado**, y
   *«when kept outside in winter, dogs may need 10 to 90 % more calories than
   during summer»*. Es más de lo que mueve el nivel de actividad, que sí
   preguntamos. La zona termoneutra que da FEDIAF: 15-20 °C en perros de pelo
   largo, 20-25 °C en pelo corto, 10-15 °C en el husky de Alaska.
2. **La masa muscular** (Tabla VII-3, escala de 4 puntos). La propia fuente
   reconoce que la parte baja del BCS *«[is] confounded by muscle atrophy»*: el
   motor no sabe distinguir un perro delgado de uno atrofiado, y son dos
   raciones distintas. Es un dato que un veterinario tiene y el dueño no.

**La pregunta:** ¿se preguntan, y en qué pantalla?

---

### P-18 · El cordero, la metionina y la taurina

| | |
|---|---|
| **Dueño** | **Cris Carles**, y una fuente que no está (**Spitze 2003**) |
| **Bloquea** | No |
| **Abierta desde** | 11 de septiembre de 2026, releyendo FEDIAF entera |

Tres frases de FEDIAF que apuntan al mismo sitio y ninguna trae cifra:

- §3.3.1: *«Methionine In the case of lamb and rice foods, the methionine level
  may have to be increased.»* No hay arroz en el catálogo; **cordero sí**.
- §7.3.3: *«Feeding certain lamb and rice foods may increase the risk of a
  low-taurine status, because of lower bioavailability of sulphur-containing
  amino acids and increased faecal losses of taurine.»*
- §7.3.3: los **Terranova** sintetizan menos taurine, y el Terranova está en
  `razas.json`.

Y una cuarta que explica por qué el mínimo que aplicamos es el del caso peor:
*«The recommended values [de metionina-cistina] are based on a dog food
containing a very low taurine content, i.e. <100 mg/kg dry matter.»* Una ración
BARF con carne y corazón lleva taurina de sobra, así que FEDIAF dice que ahí la
RA de aminoácidos azufrados **podría ser menor**. No se baja —gana FEDIAF, y
bajar un mínimo no es apretar— pero es justo la mecánica por la que a Cris «le
sale carente de metionina» al restringir la proteína en el IRIS 4.

**La pregunta:** ¿se avisa cuando un menú se apoya en cordero, o se espera a
tener la taurina medida (Spitze 2003, que decide el dato de 89 fichas)?


### P-19 · El cardíaco con renal recibe la dieta baja en proteína que el consenso ACVIM dice que hay que evitar

| | |
|---|---|
| **Dueño** | **Cris Carles** (es criterio clínico: dos fuentes piden cosas opuestas) |
| **Bloquea** | No, pero afecta a un perro que existe |
| **Abierta desde** | 12 de septiembre de 2026, leyendo entero el consenso ACVIM |

Keene BW et al., ACVIM consensus (JVIM 2019;33:1127-1140), recomendaciones
dietéticas del estadio C, con la fuerza más alta del documento — **Class I, LOE:
moderate**:

> *«Ensure adequate protein intake and **avoid low-protein diets designed to
> treat chronic kidney disease, unless severe concurrent renal failure is
> present**.»*

**MEDIDO en el motor el mismo día**, combinando las dos patologías:

| Marcado | Techo de proteína | Techo de sodio |
|---|---|---|
| `cardiopatia` sola | ninguno | 738,6 |
| `renal` sola | **62,5** | 750,0 |
| `cardiopatia` + `renal` | **62,5** | 738,6 |
| `cardiopatia_c` + `renal` | **62,5** | 625,0 |
| `cardiopatia_d` + `renal` | **62,5** | 480,0 |

O sea que el motor le pone al cardíaco con renal exactamente el techo de
proteína de la dieta renal, que es lo que el consenso dice que hay que evitar.
Y en el caso que la frase nombra: nuestra clave `renal` **es** la leve-moderada
(la grave es `renal_avanzada`, que no es formulable), así que no estamos en la
excepción de «severe concurrent renal failure».

**No es un fallo del mecanismo.** Los topes se combinan con `min()` y eso es lo
correcto y lo que protege en todos los demás cruces. Lo que pasa aquí es que
**las dos fuentes piden cosas opuestas**: el Reglamento (UE) 2020/354 entrada 10
pone el techo de proteína de la dieta renal, y el consenso ACVIM dice que a un
cardíaco no se le ponga salvo fallo renal grave.

Las tres salidas posibles, para que la decisión se tome con ellas delante:

1. **Dejarlo como está.** El techo de proteína es de la ley y la ley gana. El
   perro come menos proteína de la que ACVIM querría.
2. **Que la combinación no aplique el techo de proteína**, y avisar. Sería la
   primera vez que una combinación AFLOJA algo, y eso rompe la regla de que
   combinar solo puede apretar.
3. **Que la combinación no sea formulable** y se diga por qué, como ya pasa con
   renal + pancreatitis.

**La pregunta:** ¿cuál de las tres? Y si es la 2, ¿bajo qué condición exacta,
dado que «severe concurrent renal failure» es justamente lo que separa nuestras
dos claves renales?

⚠️ **SEGUNDA FUENTE, 12 de septiembre, leyendo AAHA 2021 entera.** Ya no es un
consenso contra un reglamento: AAHA lo dice también, y para las **tres**
cardiopatías que lista. Su Tabla 8, bloque «Cardiovascular disease», pone en
«Nutrients of Concern» lo mismo en la enfermedad valvular degenerativa, en la
miocardiopatía hipertrófica y en la dilatada: «Controlled sodium / High EPA/DHA /
**Avoid low protein**». Y en el texto corrido, hablando de la miocardiopatía
dilatada asociada a dieta: «Previously identified risk factors include lamb and
rice diets, **low-protein diets**, and high-fiber diets».

Eso cambia el peso de la pregunta en dos sitios. Primero, la salida 1 («la ley
gana») deja al perro comiendo menos proteína de la que piden **dos** fuentes
clínicas independientes, no una. Y segundo, «high-fiber diets» aparece en la
misma lista de riesgo: la patología `obesidad` lleva un suelo de fibra de 30
g/1000 kcal, así que un cardiópata obeso recibe hoy, a la vez, el suelo de fibra
alto y —si además es renal— el techo de proteína bajo. **Eso no está medido**, y
hay que medirlo antes de contestar.

---


---

### P-20 · AAHA no recomienda dar comida cruda, y esto es una app de comida cruda

| | |
|---|---|
| **Dueño** | **Elena** (es decisión de producto: qué se cuenta y dónde) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo entera AAHA 2021 |

El motor usa números de AAHA 2021 en dos sitios que deciden raciones: la banda
de BCS 4-5 (su Tabla 2, que es de donde salen `BCS_IDEAL_MIN = 4.0` y
`PCT_POR_PUNTO_BCS = 0.10`) y el 10 % de los premios. Y la misma fuente dice:

> *«AAHA does not advocate or endorse feeding pets any raw or dehydrated
> nonsterilized foods, including treats that are of animal origin.»*

Y su Tabla 4 pone «Unconventional diet (e.g., raw meat based, home prepared,
vegetarian, vegan)» entre los factores de riesgo que obligan a una evaluación
nutricional ampliada.

No hay ninguna cifra que cambiar y no propongo cambiar nada del motor. La
pregunta es **qué se hace con esto**, y son tres cosas distintas:

1. ¿Va al documento que lee el nutricionista? Ahí ya está
   `FEDIAF_CONTRA_OTRAS_FUENTES.md` para las discrepancias de cifras, pero esto
   no es una cifra: es la postura de una fuente que sí usamos.
2. ¿Se dice en la app? Hay ya un aviso de higiene de manipulación de carne cruda,
   de WSAVA, del 10 de septiembre. Esto es de otra clase.
3. ¿Cambia algo de cómo se cita AAHA? Mi opinión, y es solo eso: no. Usar la
   tabla de BCS de una guía y no seguir su recomendación de producto es legítimo
   **si se dice**, que es exactamente lo que hace esta ficha.

Nota aparte, del mismo tipo que la que ya lleva ACVIM: la guía declara quién la
paga — «These guidelines are supported by generous educational grants from
Hill's Pet Nutrition, Inc., Purina Pro Plan Veterinary Diets, and Royal Canin».

---

### P-21 · Tres recomendaciones de AAHA que no traen número

| | |
|---|---|
| **Dueño** | **Cris Carles** (las tres necesitan una cifra que la fuente no da) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo entera AAHA 2021 |

La Tabla 8 de AAHA 2021 («Nutrients of Concern for Diseases and Select Specific
Conditions») pide tres cosas que el motor hoy no hace, y **ninguna de las tres
viene con cifra**. Escribirlas en el solver exigiría inventarse el número, que es
lo que no se hace aquí. Van juntas porque la pregunta es la misma.

| Patología | Lo que dice AAHA | Lo que hace el motor hoy | Lo que falta |
|---|---|---|---|
| `epilepsia_idiopatica` | «High medium-chain triglycerides» | Nada: un menú normal con avisos de fármaco | La cifra, y además el motor **no tiene clave** de triglicéridos de cadena media. El catálogo tendría que medirlos |
| `diabetes` | «High protein (unless contraindicated, e.g., proteinuria)» | Suelo de fibra 17,5. **Ningún suelo de proteína** | Cuánta. Y la condición: «unless contraindicated» significa que en un diabético con proteinuria es al revés |
| `renal_proteinuria` | «25-50% protein reduction from current intake · Meet essential amino acid requirements» | Solo avisos, **ninguna cifra** | Es una reducción **relativa a lo que el perro come hoy**, y el motor no sabe eso. O se convierte en un valor absoluto por 1000 kcal, o no es aplicable a este sistema |

La última es la más importante de las tres: `renal_proteinuria` es una patología
que un perro tiene de verdad y hoy no lleva ni un número.

---

### P-22 · Hasta el 40 % del fósforo de un menú sale de un bote, y no sabemos qué sal es

| | |
|---|---|
| **Dueño** | **medible primero (Elena: hacen falta las etiquetas), y después Cris Carles** |
| **Bloquea** | No hoy. Podría bloquear el día que se sepa la respuesta |
| **Abierta desde** | 12 de septiembre de 2026, leyendo enteros Dobenecker 2021 y Hofmann 2025 |

Los dos estudios del grupo de Múnich que el repo cita 35 veces dicen lo mismo
desde dos lados: **el daño del fósforo depende de la sal, no solo de la
cantidad.**

Dobenecker dio a ocho beagles cinco veces su requisito de fósforo cambiando solo
la fuente:

> *«Pi (KH2PO4, NaH2PO4) but not organic P caused an increased apparent P
> digestibility and significantly influenced kinetics of serum FGF23,
> parathyroid hormone, P, CrossLaps and bonespecific alkaline phosphatase,
> demonstrating a disrupted calcium (Ca) and P homeostasis with potential harm
> for renal, cardiovascular and skeletal health.»*

Y Hofmann pone la frontera donde de verdad está, que **no** es orgánico contra
inorgánico: *«CaHPO4*2H2O was used as inorganic P source because of its low
solubility»* — el fosfato dicálcico es inorgánico y es el del lado bueno, 0 % de
solubilidad al minuto y a los 90 minutos.

**MEDIDO el mismo día sobre los 216 menús del catálogo precalculado:**

| | % del fósforo del menú que aporta el multivitamínico |
|---|---|
| mínimo | 0,49 % |
| mediana | **17,34 %** |
| máximo | **39,58 %** |
| menús donde aporta 0 % | **ninguno** |

**Y la protección que uno supondría no protege.** Del mismo estudio: *«This
implies that a mere increase of the Ca/P ratio in a product with considerable
amounts of soluble Pi salts does not suffice to protect the user from a high P
burden»*. El motor se defiende del fósforo con el techo por 1000 kcal y con el
ratio calcio:fósforo, y la fuente dice que el segundo no sirve para esto.

**Por qué no lo he decidido yo.** Hacen falta ocho datos que están en ocho
etiquetas y que no puedo inventar, y según cuál sea la respuesta las dos fuentes
dicen cosas opuestas **para el mismo número del catálogo**. La lista de los ocho
productos está en `DATOS_QUE_FALTAN.md`.

**La pregunta, en dos tiempos:**

1. **Para Elena:** ¿se consiguen las ocho etiquetas? Es leer la línea de
   composición o de aditivos del bote.
2. **Para Cris, cuando estén:** si alguno lleva fosfato monosódico o
   monopotásico, ¿qué se hace? Las salidas que se me ocurren son (a) nada, porque
   la dosis del suplemento es de gramos y estos estudios dan cinco veces el
   requisito; (b) marcar esas fichas y que el motor prefiera las otras; (c)
   sacarlas del catálogo. La (a) necesita un número que no tengo: cuánto fósforo
   soluble llega de verdad al perro con la dosis real, que es mucho menor que la
   del estudio.

---

### P-23 · La TVT pide un ratio calcio:fósforo de 1,3-1,5 y el 87 % de nuestros menús está por debajo

| | |
|---|---|
| **Dueño** | **Cris Carles** (es criterio clínico: FEDIAF deja 1,0-2,0 y esta fuente aprieta dentro) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo enteras las dos ediciones del Merkblatt 181 |

El Merkblatt 181 de la TVT —la hoja de la asociación veterinaria alemana de
protección animal dedicada al BARF— da el ratio calcio:fósforo **«optimal 1,3 –
1,5»**, y lo da **igual en sus dos ediciones**, la de julio de 2017 y la de mayo
de 2025. Lo pone dentro de la lista de riesgos, junto a que un ratio inadecuado
en cachorros puede dejar deformidades esqueléticas permanentes.

El motor aplica el **1,0-2,0 de FEDIAF**. El 1,3-1,5 cabe dentro, así que no es
un conflicto: es una recomendación que aprieta, o sea la clase de
`recomendaciones_libro.json`.

**MEDIDO el mismo día sobre los 216 menús del catálogo precalculado:**

| | Ca:P |
|---|---|
| mínimo | 1,00 |
| **mediana** | **1,16** |
| máximo | 1,74 |
| dentro del 1,3-1,5 de la TVT | **25 de 216** |
| por debajo de 1,3 | **188** |
| por encima de 1,5 | 3 |

O sea que **no es un ajuste fino: aplicarlo como suelo cambiaría el 87 % de los
menús**, y no está medido si con este catálogo siguen saliendo. Es la misma forma
que tuvo el suelo de vitamina E: una cifra de una fuente que cabe en la ventana
de FEDIAF y que al encenderla puede dejar a perros sin menú.

**La pregunta:** ¿se aplica el 1,3 como suelo al perro sano? Y si se aplica, ¿al
cachorro también, que es donde la fuente pone el riesgo grave, o solo ahí? Antes
de encenderlo hay que medir cuántos perros se quedan sin menú, como se hizo con
la vitamina E.

⚠️ Y hay que mirarlo junto al **otro** ratio Ca:P que el motor ya aplica: el
1,1-2,0 que pide `oxalato` desde el 10 de septiembre, de las Tablas 40-5 y 41-6
de SACN5. Son tres fuentes con tres bandas para la misma cosa (1,0-2,0 FEDIAF ·
1,1-2,0 SACN5 en oxalato · 1,3-1,5 TVT en el perro sano), y hoy la más estricta
por abajo sería la de la TVT.


---

## Cerradas

*(Cuando una pregunta se contesta, se mueve aquí con la respuesta, la fecha y
quién la dio — y si de ella sale una decisión, se escribe en `DECISIONES.md`
y se enlaza.)*

Ninguna todavía.
