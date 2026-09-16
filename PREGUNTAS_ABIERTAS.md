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
secundaria *que no se ha podido contrastar con el texto original de FEDIAF*.**
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

### P-35 · ¿Hay un punto en el que bajar el sodio de un cardiópata sea malo?

> ⚠️ **ERA UNA SEGUNDA «P-10», y estuvo así días sin que saltara nada** (renumerada el 12 de
> septiembre de 2026). Había dos preguntas distintas con el mismo número: el tope que recorta la
> fórmula de lactancia y ésta. En un registro cuya razón de existir es que ninguna pregunta se
> pierda, un número repetido tapa una de las dos: quien busque la P-10 encuentra la primera y se
> va. Y el BLOQUE 66, que vigila este fichero, comparaba el ÍNDICE contra
> `PARA_EL_NUTRICIONISTA.md` -- o sea la numeración `PREGUNTA n` --, y a la numeración PROPIA del
> registro, las `P-nn`, no la miraba nadie. Desde hoy sí: ver el BLOQUE 66.

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

### P-41 · ¿Lleva el oxalato cálcico un suelo de fósforo?

⚠️ **ERA LA P-11 Y SE RENUMERA A P-41 el 15 de septiembre**, por lo mismo que la
P-40 de abajo: había **dos preguntas con el número 11**, ésta y «FEDIAF da cifras
para dos razas que la app tiene y el motor ignora», que está CERRADA. Se renumera
la abierta y no la cerrada a propósito: una pregunta cerrada es historia y se
cita desde `HECHO.md`, mientras que la abierta es la que se va a volver a leer.
Las referencias de `der.py` y `LECTURAS.md` van cambiadas en el mismo commit.

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

**REDUCIDA el 13 de septiembre, y la reduce el propio motor.** La pregunta estaba
mal planteada por mi parte: **el oxalato YA lleva suelo de fósforo**. No el de
SACN5 —los 750 de la Tabla 40-5 están escritos y no se aplican porque no pueden
cambiar nada— sino el de FEDIAF, que es **1160 mg/1000 kcal** y es más alto.
Comprobado: el motor aplica hoy techo 1500 y suelo 1160, o sea una ventana de
340 mg.

Así que lo que queda no es «¿lleva suelo?» sino una sola cosa: **¿hay que subir
ese suelo de 1160 al 1500-2000 de Fascetti?** Y ahí sigue mandando la medida de
arriba: los menús salen a 1498,x, así que **cualquier suelo por encima de 1160
empieza a apretar y uno de 1500 deja al oxalato sin menú**. Si la respuesta es
que sí, hay que subir el techo antes, y eso ya no es una cifra: es elegir entre
SACN5 y Fascetti, que es exactamente lo que decide un clínico. **Dueño: Cris
Carles.**

### ~~P-14 · FEDIAF publica la curva de crecimiento como ecuación, y el motor usa una copia divulgativa~~ · **CERRADA el 13 de septiembre**

| | |
|---|---|
| **Dueño** | — |
| **Bloquea** | No |
| **Abierta desde** | 11 de septiembre de 2026, releyendo FEDIAF entera · **cerrada el 13** |
| **Qué la cerró** | La mitad que faltaba —llevar la Tabla VII-8a al frontend— **ya estaba hecha** desde el 12 de septiembre, cuando se quitó el recorte por raza: `src/der.js` tiene las cinco ecuaciones en `CURVA_FEDIAF_VII_8A` y las usa para el cachorro mestizo sin peso adulto, exactamente como pedía esta pregunta. Estaba resuelta en el motor y abierta en el registro: **una pregunta zombi**, que es justo lo que este fichero existe para impedir. Comprobado el 13 de septiembre en los dos repos, y el contrato del DER —146 casos, uno de ellos con peso adulto Y edad a la vez, que es el que ejerce la curva en los dos lados— sale verde en los dos |

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

### ~~P-15 · FEDIAF dice dos veces que el BCS ideal es 4-5, y el motor toma 5~~ · **CERRADA el 13 de septiembre**

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

**CERRADA el 13 de septiembre, y la contestó la propia FEDIAF.** Se aplicó el 12:
`BCS_IDEAL_MIN = 4` en los tres sitios a la vez —`verificar.py`, `der.py` y
`src/bcs.js`—, así que dentro de la banda 4-5 el peso no se corrige y por debajo
del 4 el destino es el 4 y no el 5. Antes, a un perro en BCS 4 se le subía el
peso objetivo un 11 % contra lo que dice su propia guía dos veces. Estaba
aplicado y la pregunta seguía abierta: **otra zombi**. Comprobado el 13 de
septiembre en los tres ficheros.

⚠️ Y el mismo día esa banda ganó un segundo uso que no tenía: es la que decide
el ±10 % por condición corporal de un CACHORRO (P-37). O sea que este número, que
parecía cosmético, ahora mueve las kcal de un cachorro en las dos direcciones.

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

⚠️ **AMPLIADA EL 12 DE SEPTIEMBRE, leyendo el cap.178 de Ettinger (Debra Zoran), que
trae la primera cifra concreta de todo el repo para esto.** Dice que un alimento de
mantenimiento corriente tiene una digestibilidad de proteína e hidratos de entre el
*«70 y el 85 %»* de materia seca, y que las dietas médicas digestivas *«idealmente
deben tener una digestibilidad de CHO y proteínas de al menos un 88 % de MS»*.

O sea que entre una dieta corriente y una entérica hay hasta **18 puntos**, y el
motor **no ve ninguno de los dos**: suma los nutrientes que declara cada ficha como
si llegaran enteros al perro. Y el umbral de validez de FEDIAF (≥70 % MS, ≥80 %
proteína) cae **dentro** de la banda del alimento corriente, no por encima: no es un
listón lejano, es la mitad baja de lo normal.

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

⚠️ **TERCERA FUENTE, Y LA PRIMERA QUE PONE UNA CIFRA** (12 de septiembre, leyendo
el capítulo 183 de Ettinger, de Lisa Freeman y John Rush, que es el de nutrición
cardíaca):

> *«La restricción de proteínas debe evitarse en perros y gatos con enfermedades
> cardiacas porque estos pacientes están predispuestos a la pérdida de masa
> muscular corporal. Las dietas bajas en proteínas, incluso si están diseñadas
> como dietas cardiacas, dietas diseñadas para enfermedades renales y «dietas
> sénior», no se recomiendan a menos que exista una disfunción renal grave. De lo
> contrario, se recomienda un alimento nutricionalmente equilibrado de buena
> calidad que proporcione al menos los niveles mínimos de proteína canina (4,5
> g/100 kcal)»*

Dice lo mismo que el consenso ACVIM, **con la misma excepción** («a menos que
exista una disfunción renal grave» = «unless severe concurrent renal failure is
present»), y añade el número que faltaba: **al menos 4,5 g/100 kcal = 45 g/1000
kcal**, el mínimo de la AAFCO.

**Y con ese número, el techo del motor queda por encima de las tres fronteras que
nombran las fuentes:**

| | g/1000 kcal | % de las kcal |
|---|---|---|
| Suelo que nombra Freeman (mínimo AAFCO) | 45 | 18 % |
| Mínimo de FEDIAF, perro adulto | 52,1 | 21 % |
| Frontera de «restricción» del cap.175 del mismo libro | 50 | 20 % |
| **Techo del renal que aplica el motor** | **62,5** | **25 %** |

Eso **estrecha la pregunta y no la cierra**. Las tres fuentes siguen diciendo
«evitar dietas bajas en proteína» y un techo sigue siendo un techo — pero ya no se
puede afirmar que el motor le ponga al cardíaco una **dieta baja en proteína**,
porque por el número que da la única fuente que da uno, no lo es. La pregunta que
queda es más fina: **¿basta con estar por encima de 45, o el problema es tener un
techo puesto por una enfermedad que este perro quizá no tiene en grado grave?**

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

⚠️ **Y el 12 de septiembre por la tarde entró la QUINTA fuente, que es la que más
pesa de las cinco, porque es la agencia reguladora.** Ettinger cap.192 (Perea y
Delaney, el capítulo dedicado a las dietas caseras, vegetarianas y crudas) cita la
postura de la FDA estadounidense: *«La FDA no aboga por una dieta cruda de carne, de
aves de corral o mariscos en mascotas, pero está intensificando sus esfuerzos para
minimizar el riesgo que estos alimentos puedan representar para la salud animal y
humana porque entendemos que algunas personas prefieren alimentar a sus mascotas con
este tipo de dietas»*.

Y es el único de los cinco que dice **qué se rompe exactamente**. De cinco dietas
crudas analizadas (dos comerciales y tres caseras), *«todas tenían nutrientes
esenciales por debajo de los niveles mínimos recomendados por la AAFCO»*, y de las
tres caseras, *«tenían proporciones mal equilibradas de calcio y fósforo (Ca, P), dos
tenían niveles excesivos de vitamina D y una tenía niveles excesivos de vitamina E»*.

**Eso cambia el tono de la respuesta, y conviene verlo.** Las tres cosas que esa
fuente encuentra rotas en las dietas crudas caseras son exactamente tres de las que
el motor comprueba de cero en cada menú: el ratio Ca:P es una restricción dura del
solver, la vitamina D es uno de los cinco topes de seguridad crónica, y la vitamina E
no tiene máximo en FEDIAF pero sí se mide. O sea que lo que estas cinco fuentes
desaconsejan es **el crudo formulado a ojo**, que es justo lo que este motor existe
para no hacer. La misma frase de la FDA reconoce que hay gente que va a dar crudo
igual y que lo que procede entonces es reducir el riesgo. Sigue siendo una decisión
de producto y no la tomo yo, pero la pregunta ya no es «¿cómo lo contamos?» sino
«¿lo contamos con los tres números al lado?».

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
| `disfuncion_cognitiva` | Ettinger cap.175 pide también triglicéridos de cadena media: «se propone que los cuerpos cetónicos obtenidos del metabolismo de los MCT proporcionan fuentes alternativas de energía para el cerebro envejecido» | Suelo de vitamina E | Otra vez la dosis. Son ya **dos** patologías del motor —esta y la epilepsia— a las que **dos** fuentes distintas les piden MCT sin decir cuánto, y el catálogo no los mide |

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

### ~~P-23 · La TVT pide un ratio calcio:fósforo de 1,3-1,5 y el 87 % de nuestros menús está por debajo~~ ✅ CERRADA

| | |
|---|---|
| **Resuelta** | **12 de septiembre de 2026**, por Elena, con la regla de fuentes del propio proyecto |
| **Decisión** | **No se aplica.** El motor sigue con el **1,0-2,0 de FEDIAF** |
| **Sus palabras** | *«El ratio Ca:P viene de fediaf, ya sabes como va el orden de fuentes que mandan»* |
| **Por qué** | El ratio calcio:fósforo **es un REQUISITO**, y los requisitos los fija FEDIAF: 1,0-2,0. El 1,3-1,5 de la TVT no es un tope clínico sobre un perro enfermo — es **otra banda para el perro que no tiene nada**, con suelo y techo propios, o sea un requisito rival de una fuente que va detrás. Cuando dos fuentes dan el requisito del mismo perro sano, no se elige la más estricta: se aplica la que manda |
| **El alcance, dicho por ella** | *«Lo que te decia del ratio me referia al requerimiento, si alguna patologia necesita algo distinto es otra cosa»*. Acotado el mismo día, porque yo había cerrado con esta regla también la P-30, que es de una patología. Esa está **reabierta** |
| **Lo que NO cambia** | El **1,1-2,0 del `oxalato`** sigue aplicado, y con esto ya no necesita defensa: es una patología pidiendo lo suyo, que es «otra cosa» |
| **Dónde** | `LECTURAS.md` (TVT), `FEDIAF_CONTRA_OTRAS_FUENTES.md` §4 |

⚠️ **La línea que separa esto de los otros dos Ca:P del repo.** Desde fuera se
parecen y no lo son:

| | TVT, perro sano | SACN5, oxalato | Bartges, renal |
|---|---|---|---|
| Banda | 1,3-**1,5** | 1,1-**2,0** | 1,1-**1,3** |
| A quién | al perro que **no tiene nada** | a una **patología marcada** | a una **patología marcada** |
| Qué es | un **requisito** rival del de FEDIAF | un límite clínico | un límite clínico |
| Estado | **no se aplica** (esta pregunta) | **aplicado** | **no aplicado, y sigue abierto** (P-30) |

La distinción es la que puso Elena: la regla es sobre **el requisito**, y lo que
pida una patología «es otra cosa». Los dos de la derecha se deciden como cualquier
otro límite de patología, uno por uno y con quien sabe de esto. Lo que sigue debajo
es la medida que se hizo antes de cerrar esta, y se deja entera.


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

### P-24 · El motor podría decir si la ración acidifica la orina, y no lo dice

| | |
|---|---|
| **Dueño** | **Elena** (es una capacidad nueva del producto) **y una fuente que falta** |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo entero el extracto de Stürmer 2005 |

El motor tiene cuatro patologías de urolito —`estruvita`, `urato`, `oxalato` y
`cistina`— y las cuatro dicen lo mismo: **el pH de la orina decide, y el motor no
lo ve**. Tres de ellas ni siquiera formulan menú automático por eso.

Pero el pH urinario no es un misterio: depende en buena parte del balance
catión-anión de la ración, y la fórmula está publicada (Krohn 1993, que es la que
usa Stürmer y una variante de la que usa Hofmann 2025):

> *«KAB [mmol/kg TS] = 49,9\*Ca + 82,3\*Mg + 43,5\*Na + 25,6\*K – 59\*P – 13\*(Met+Cys) – 28,2\*Cl»*

**El motor tiene los siete datos.** Calcio, magnesio, sodio, potasio, fósforo,
metionina+cistina y cloruro están en las 163 fichas del catálogo, sin un solo
hueco (comprobado).

**MEDIDO el 12-sep-2026 sobre los 216 menús del catálogo:**

| | KAB (mmol por 1000 kcal) |
|---|---|
| mínimo | −22 |
| mediana | 14 |
| máximo | 132 |
| menús con KAB negativa (ración **acidificante**) | **40 de 216** |

O sea que uno de cada cinco menús empuja la orina hacia ácida, que es lo que
quiere la estruvita y lo que **no** quieren el urato ni la cistina, y hoy el menú
sale igual y no lo dice nadie.

⚠️ **ACTUALIZADO EL MISMO DÍA, y la actualización cambia el bloqueo.** Escribí
aquí que la ecuación del perro «no está en el repo». **Sí está**: la recoge la tesis de Heer
2017, que se leyó unas horas después, en su Tabla 1 y en su texto. Es de Behnsen
1992 y dice:

> *«BEHNSEN (1992) stellte in ihren Studien einen deutlichen Zusammenhang
> zwischen der KAB im Futter und dem Urin-pH her (pH = 6,92 + 0,0073 * KAB; r =
> 0,96***; n = 12). Die KABs variierten hier von -349 mmol/kg TS bis 437
> mmol/kg TS und produzierten Harn-pH-Werte von 5,94 ± 0,55 bis 7,78 ± 0,05.»*

**Y esa ecuación, tal como está publicada, no puede ser.** La frase da la recta y
el rango de los datos a la vez, y no encajan:

| | KAB | pH según la ecuación | pH que se midió |
|---|---|---|---|
| extremo ácido | −349 | **4,37** | 5,94 ± 0,55 |
| extremo alcalino | +437 | **10,11** | 7,78 ± 0,05 |

Una recta con r = 0,96 no predice un recorrido de 5,7 unidades sobre datos que
recorren 1,84. La pendiente que sale de los dos extremos publicados es **0,0023**,
un tercio de la impresa, y ese número sí encaja con las demás especies de la
misma tabla (gato 0,0021 y 0,0023; cerdo 0,0031) y con la **Figura 4** de la
propia tesis, donde la nube del perro va de pH ~5,5 a ~7,6 y ninguna especie pasa
de 9. Comprobado contra el PDF: no es un fallo de extracción, está impreso así.

Aplicada tal cual a nuestros 216 menús daría pH urinarios de 6,29 a **10,77**, y
un pH urinario de 10,8 no existe.

**Así que el bloqueo ya no es «falta la ecuación», es «la que hay no se
sostiene».** No voy a poner una pendiente que he calculado yo de dos extremos.
Hace falta Behnsen 1992 —la tesis de Hannover— o alguna otra fuente con la
ecuación del perro.

**Lo que SÍ se puede decir sin ninguna ecuación es el signo**, y eso no depende
de ninguna pendiente: 40 de los 216 menús tienen balance negativo, o sea
acidifican.

**La pregunta, en dos:**

1. **Para Elena:** ¿vale la pena decir la dirección? Sería un dato más en el menú,
   solo con las patologías de urolito marcadas, del tipo «esta ración empuja la
   orina hacia ácida» — útil para la estruvita, contraproducente para el urato.
2. **Y si vale:** ¿se consigue Behnsen 1992, o alguna otra fuente con la
   ecuación del perro? Con ella esto deja de ser una dirección y pasa a ser un
   número. Y si se consigue, lo primero que hay que mirar es si su pendiente es
   la 0,0073 que imprime Heer o la 0,0023 que sale de sus propios datos.

---

### P-25 · El motor entrega las kcal como un número exacto, y dos fuentes dicen que la banda real es de ±30 %

| | |
|---|---|
| **Dueño** | **Elena** (qué se enseña y a quién) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo enteros los 18 documentos de la WSAVA |

Las guías de evaluación nutricional de la WSAVA (JSAP 2011), hablando de cómo
estimar las necesidades energéticas:

> *«energy requirements can vary by 50% in either direction for cats, and by 30%
> in either direction for dogs»*

Y sus preguntas frecuentes lo repiten para el dueño: *«individual dogs or cats
can vary up to 50% above or below these starting points»*.

El motor recibe un DER y formula contra él. La app calcula ese DER y enseña un
número: «1.955 kcal». No dice en ninguna parte que ese número tiene una banda de
±30 % en el perro, y esa banda es **más ancha que la diferencia entre dos niveles
de actividad** de la Tabla VII-7 de FEDIAF (95 a 175 kcal/kg^0,75 es un factor de
1,84 entre los extremos; ±30 % sobre un mismo nivel ya es un factor de 1,86).

Esto no es un fallo: ninguna fuente da otra cosa, y el motor no puede formular
contra un rango. Es una cuestión de **qué se dice**.

**La pregunta, en tres:**

1. ¿Se dice, y dónde? Mi propuesta sería el registro de veterinario de
   `GET /vocabulario`, junto a los cinco niveles de actividad, donde ya va la
   cifra de FEDIAF de cada uno.
2. ¿Se le dice también al dueño? Ahí no tengo opinión: «entre 1.370 y 2.540
   kcal» puede ser más honesto y menos útil que «1.955 y ajusta según el peso»,
   que es justo lo que recomiendan las mismas guías (revisar peso y condición
   corporal cada dos semanas al principio).
3. ¿Va a `PARA_EL_NUTRICIONISTA.md`? Ahí sí creo que sí, porque quien revisa el
   motor tiene que saber contra qué incertidumbre se está comparando todo lo
   demás.

---

### P-26 · Los estándares de la FCI no dan el peso de la mayoría de las razas

| | |
|---|---|
| **Dueño** | **Elena** (decide si se sigue por esta vía o por otra) |
| **Bloquea** | No. Pero `razas.json` sigue sin fuente, y de ahí salen las kcal, la etapa y el techo de calcio del cachorro de raza grande |
| **Abierta desde** | 12 de septiembre de 2026, leyendo los estándares descargados |

`razas.json` lleva escrito en su `_meta` que **sus 255 pesos adultos no tienen
fuente publicada**. El 11 de septiembre se empezó a resolver bajando los
estándares oficiales de la FCI, que son públicos y gratis. El plan era el
correcto y está a medias:

- Descargados: **33 estándares de 255 razas**.
- El lector que el LÉEME de esa carpeta dice que debe vivir en el repo de la API
  (`leer_estandares_fci.py`) **no existe**.

**Y medido hoy sobre esos 33, la vía no da lo que se esperaba:**

| | |
|---|---|
| estándares con un peso en kg | **9** |
| estándares sin peso en kg | **24** |

Un estándar de raza describe la **altura a la cruz**, que es lo que se mide en un
concurso. El peso lo dan solo algunas razas. El del pointer inglés tiene el
apartado «SIZE AND WEIGHT» y dentro solo pone la altura; igual el airedale
terrier, el setter inglés, el bull terrier o el bobtail.

O sea que bajar los 222 que faltan daría fuente a **algo más de una cuarta parte**
de las razas, y el resto seguiría igual que hoy. Convertir altura en peso no vale:
no hay una conversión publicada para el perro, y sería inventar el número, que es
justo lo que `razas.json` declara que no hace.

**La pregunta, en dos:**

1. ¿Se terminan de bajar los 222 que faltan aun sabiendo que solo cubren una
   cuarta parte? Mi opinión: sí, porque una cuarta parte con fuente es mejor que
   ninguna, y el fichero puede decir cuáles la tienen y cuáles no — que es más
   honesto que la frase de hoy, que dice que no la tiene ninguna.
2. ¿De dónde salen los otros tres cuartos? Aquí no tengo propuesta buena. Las
   cuatro fuentes del motor no traen tabla de peso por raza, y las que circulan
   son de clubes y de webs divulgativas.

⚠️ **Y una cosa de proceso**: esto llevaba un día hecho a medias y no estaba
escrito en ninguna parte de este repo. La descarga vive en el otro repo y el
lector que tenía que auditarla aquí no llegó a existir. Si nadie lo lee, en un
mes alguien vuelve a empezar.

---

### P-27 · Un metaanálisis de Ettinger calcula las kcal con otro exponente, y el desacuerdo va en las dos direcciones

| | |
|---|---|
| **Dueño** | **Cris Carles** (es criterio: dos fuentes con dos formas de escalar) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo la sección de nutrición de Ettinger |

El capítulo 172 del tratado de Ettinger, Feldman y Côté —*Nutrición de perros
adultos sanos*, escrito por **Martha G. Cline**, que es la primera autora de las
guías AAHA 2021 que ya usamos— publica las ecuaciones de energía de un
**metaanálisis**, y no usan el exponente 0,75:

| | Fórmula |
|---|---|
| Mantenimiento, todos los perros | 81,5 × PC^0,93 |
| Mantenimiento, **solo perros domésticos** | **62 × PC^0,97** |

> *«El metaanálisis del REM de perros adultos demostró un REM promedio de 142,8 ±
> 55,3 kcal/kg de PC0,75/día, con una ecuación alométrica estimada de 81,5 kcal/kg
> de PC0,93/día»*

> *«La ecuación recomendada para determinar el REM de los perros de compañía es
> 62,5 kcal/kg de PC0,97/día»*

⚠️ Dos avisos antes de discutirlo. **El texto dice 62,5 y su propio cuadro dice
62**, en el mismo capítulo. Y como el exponente no es el mismo, **las dos curvas se
cruzan**: no hay «un porcentaje» de diferencia.

**MEDIDO el 12-sep**, la ecuación de perro doméstico contra lo que aplica el motor
a un perro de actividad normal (110 × PC^0,75, Tabla VII-7 de FEDIAF):

| Peso | Ettinger | Motor | Diferencia |
|---|---|---|---|
| 3 kg | 180 kcal | 251 kcal | **−28,2 %** |
| 10 kg | 579 | 619 | −6,5 % |
| 30 kg | 1.680 | 1.410 | **+19,1 %** |
| 60 kg | 3.290 | 2.371 | **+38,7 %** |

O sea que con el exponente 0,97 el perro grande necesitaría **un 39 % más** y el
toy **un 28 % menos** de lo que el motor le da hoy. No es un desacuerdo de nivel:
es de forma.

**Por qué no lo cambio.** Manda FEDIAF, que publica su tabla en kcal/kg^0,75, y
además el propio capítulo avisa de que *«Existe una gran variación en el intervalo
de predicción del REM; por lo tanto, las fórmulas deben usarse solo como punto de
partida»* — su ± 55,3 sobre 142,8 es un 39 %, la misma banda que abre la P-25. Con
esa incertidumbre, las dos curvas caben una dentro de la otra en casi todo el
rango.

**La pregunta:** ¿hay que decirlo en el documento que va a revisión, y hay que
mirar con lupa los dos extremos —el toy y el gigante—, que es donde las dos
fuentes más se separan y donde además el motor ya tiene problemas conocidos (al
toy le cuesta salir menú, y el gigante es el que más lejos está de la curva de
crecimiento)?

---

### P-28 · Al cardíaco y al renal con sobrepeso el motor les quita kcal, y esta fuente dice que ese sobrepeso puede protegerles

| | |
|---|---|
| **Dueño** | **Cris Carles** (es criterio clínico puro) |
| **Bloquea** | No da error, y por eso preocupa |
| **Abierta desde** | 12 de septiembre de 2026, leyendo el capítulo 177 de Ettinger |

El capítulo 177 del tratado de Ettinger —*Caquexia y sarcopenia*, de **Lisa M.
Freeman**, que es también la autora del capítulo de nutrición cardíaca— dice:

> *«El objetivo del BCS en un perro o gato sano es de 4-5 sobre 9 en la escala de
> BCS de 9 puntos. Sin embargo, en ciertas enfermedades (p. ej., ICC, ERC), puede
> ser beneficioso un BCS ligeramente más alto (es decir, un BCS de 6-7/9), aunque
> se requiere más investigación para hacer recomendaciones concretas. A pesar de
> ello, se ha de evitar la obesidad (BCS >7/9) en animales con estas
> enfermedades.»*

Es la **paradoja de la obesidad**, y el capítulo la explica: en insuficiencia
cardíaca y en enfermedad renal crónica lo que mata es la **caquexia**, la pérdida
de masa magra, y *«La mayor reserva de MMC en la obesidad proporciona una mayor
reserva durante el estado catabólico»*. El capítulo 176 lo respalda con datos:
*«Los perros con insuficiencia cardiaca que aumentaron de peso tuvieron una
supervivencia significativamente más larga que aquellos cuyo peso se mantuvo
estable o disminuyó»*, y en renal *«los perros con bajo peso tenían un tiempo de
supervivencia significativamente más corto»*.

**Qué hace el motor hoy.** `peso_objetivo_desde_bcs()` en `motor/verificar.py`
**no recibe las patologías**: aplica la regla del perro sano a cualquier perro. Un
BCS por encima de 5 baja el peso de referencia, y el DER se calcula sobre ese peso.

**MEDIDO el 12-sep** con la función del motor:

| BCS | Peso objetivo de un perro de 30 kg | kcal respecto a su peso real |
|---|---|---|
| 5 | 30,00 kg | 100 % |
| 6 | 27,27 kg | **93,1 %** |
| 7 | 25,00 kg | **87,2 %** |

O sea que a un cardíaco o a un renal con BCS 7 el motor le da **un 12,8 % menos de
kcal** que si se calculara sobre su peso real — en dos enfermedades donde esta
fuente dice que ese BCS «puede ser beneficioso» y donde el peligro documentado es
adelgazar.

**Por qué no lo toco.** Son tres decisiones clínicas encadenadas y ninguna es mía:
si la banda ideal cambia con la patología, cuáles (la fuente nombra insuficiencia
cardíaca congestiva y enfermedad renal crónica, no «cardiopatía» y «renal» sin
más), y qué se hace con el «se requiere más investigación para hacer
recomendaciones concretas» que la propia fuente añade.

⚠️ **Y EL CAPÍTULO 183 DEL MISMO LIBRO DA LA FORMA EXACTA DE LA RESPUESTA**, leído
el mismo día. Lisa Freeman lo escribe distinguiendo el estadio:

> *«Los autores apuntan a un BCS de 4-5/9 para animales sanos y aquellos con
> enfermedad cardiaca asintomática, y un BCS de 6-7/9 para aquellos con ICC. Un
> BCS por encima de 7/9 puede tener efectos perjudiciales, por lo que se debe
> evitar la obesidad, aunque los autores generalmente no intentarán iniciar un
> plan de pérdida de peso en perros o gatos después de la aparición de la ICC»*

O sea que **no es «con cardiopatía, otra banda»**: es la cardiopatía
**asintomática** con la banda de siempre (4-5) y la **insuficiencia cardíaca
congestiva** con la otra (6-7). Y el motor **ya tiene esa distinción hecha**: son
sus cinco claves por estadio ACVIM —`cardiopatia_a`, `b1` y `b2` son la
asintomática, y `cardiopatia_c` y `d` la ICC— y **la app ya pregunta el estadio**.
Si se decide aplicarlo, no hay que preguntar nada nuevo.

**La pregunta, entonces, es más concreta de lo que estaba:**

1. Con `cardiopatia_c` o `cardiopatia_d` marcadas, ¿el motor debe dejar de bajar el
   peso de referencia mientras el BCS esté entre 6 y 7, y seguir bajándolo a partir
   de 8?
2. Y en el renal, ¿con cuál de las dos claves —`renal` o `renal_avanzada`—, dado
   que la fuente habla de «ERC» sin estadificar y el motor sí estadifica?
3. ¿Se le dice a quien firma? Mi opinión: sí, y con la frase de la fuente, porque
   es exactamente el tipo de decisión que un dueño no puede tomar solo.

⚠️ Es la misma familia que la P-19: el motor aplica al enfermo la regla del perro
sano y **sale verde**, porque el semáforo mira el menú y no el peso con el que se
calculó.

---

### P-29 · Tres fuentes piden omega-3 al cardíaco y el motor no le pone ninguno

| | |
|---|---|
| **Dueño** | **Cris Carles** (la dosis viene por kg de peso y condicionada a un dato clínico) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo el capítulo 183 de Ettinger |

Las cinco claves de cardiopatía del motor —`cardiopatia` y los cuatro estadios
ACVIM— **solo llevan un techo de sodio**. Ningún suelo. Y tres fuentes piden
omega-3:

- **AAHA 2021**, Tabla 8: «High EPA/DHA» en las tres cardiopatías que lista.
- **Ettinger cap.183** (Freeman y Rush): *«Los autores recomiendan una dosis de EPA
  de 40 mg/kg y de 25 mg/kg para el DHA en perros y gatos con una ingesta
  reducida/alterada de alimentos o caquexia»*, y *«la ingesta de ácidos grasos n-3
  se ha asociado con una mayor supervivencia en perros con ICC»*.
- **El mismo capítulo**, sobre el mecanismo: la suplementación con aceite de
  pescado *«puede disminuir la producción de citocinas en perros con ICC y mejorar
  la caquexia»*.

**MEDIDO el 12-sep**, pasando la dosis de Freeman a la unidad del motor:

| Perro | kcal/día aprox. | EPA+DHA que sale |
|---|---|---|
| 10 kg | 619 | **1,05 g/1000 kcal** |
| 30 kg | 1.410 | **1,38 g/1000 kcal** |

Para comparar: el mínimo general de EPA+DHA del motor es **0,11 g/1000 kcal**, y el
suelo de EPA que la artrosis ya aplica es **1,0 g/1000 kcal**. La cifra está en el
mismo orden que un suelo que el motor sabe aplicar hoy.

**Por qué no lo pongo yo.** Dos cosas, y las dos son de las que este repo no
decide solo:

1. **La dosis está dada por kg de peso corporal, no por 1000 kcal.** Convertirla
   exige fijar las kcal del perro, y las kcal son justo lo que el motor recibe de
   fuera. Las dos cifras de la tabla de arriba salen de suponer una actividad
   normal; con otra actividad, el mismo perro da otro número.
2. **La fuente la condiciona**: *«en perros y gatos con una ingesta
   reducida/alterada de alimentos o caquexia»*. Eso es un dato clínico —apetito y
   masa muscular— que la ficha **no pregunta** (es la P-17).

⚠️ **AMPLIADA LA MISMA TARDE, leyendo el cap.182 (Richard Hill), que quita la mitad
del problema.** La objeción 1 —que la dosis venga por kg y no por 1000 kcal— deja de
ser un obstáculo, porque ese capítulo da la conversión hecha **y dice que la buena es
la nuestra**:

> *«la recomendación estándar para perros es de 0,22 g de aceite de pescado que
> contiene 66 mg de EPA + DHA/kg de PC/día. Esto es equivalente a aproximadamente 1
> mg de EPA + DHA/kcal de EM, asumiendo que un perro de 10 kg consume
> aproximadamente 120 kcal/kg0,75 diariamente»*

Y, en la misma página: *«La dosificación basada en la EM es preferible a la
dosificación por PC, que proporciona una cantidad desproporcionada de EPA y DHA en
perros de razas grandes»*.

**1 mg/kcal son 1.000 mg/1000 kcal**, que es exactamente el orden de las dos cifras
medidas arriba (1,05 y 1,38 g/1000 kcal) y del suelo de EPA que la artrosis ya
aplica. Tres cálculos por tres caminos distintos y el mismo número.

Queda en pie la objeción 2, que es la que de verdad decide: la fuente cardíaca
condiciona la dosis a un dato clínico que la ficha no pregunta.

**La pregunta:** ¿se le pone un suelo de EPA+DHA a la cardiopatía? Y si sí, ¿a
todas las claves o solo a los estadios C y D, que son la ICC de la que habla la
fuente? La cifra ya no es un problema: **1.000 mg/1000 kcal**, que es lo que dice
el cap.182 en la unidad del motor.

---

### P-30 · El renal pide un ratio calcio:fósforo de 1,1-1,3 y el motor tiene el mecanismo hecho sin usar

| | |
|---|---|
| **Dueño** | **Cris Carles** (es una restricción clínica nueva sobre una patología formulable) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo el capítulo 184 de Ettinger |

⚠️ **CERRADA Y REABIERTA EL MISMO DÍA, y el motivo hay que leerlo porque separa dos
cosas que se parecen.** Por la tarde la cerré junto con la P-23, aplicando a las dos
la frase de Elena *«El ratio Ca:P viene de fediaf, ya sabes como va el orden de
fuentes que mandan»*. Me pasé de alcance, y ella lo acotó en el acto:

> *«Lo que te decia del ratio me referia al requerimiento, si alguna patologia
> necesita algo distinto es otra cosa»*

O sea que la regla es sobre **el REQUISITO**, que es el del perro sano y lo fija
FEDIAF en 1,0-2,0. La **P-23 sigue cerrada**: el 1,3-1,5 de la TVT es otra banda
para el perro que no tiene nada, o sea un requisito rival. Esta **no**: el 1,1-1,3
de Bartges es de una PATOLOGÍA, y una patología pidiendo su propio límite es
exactamente lo que hacen los otros 79 del motor. Vuelve a estar abierta, y se
decide como cualquier otro límite de patología: con su fuente, su conversión, su
medida y la firma de quien sabe de esto.


El capítulo 184 del tratado de Ettinger —*Manejo nutricional de las afecciones
renales*, de **Joseph W. Bartges**— da las dos cifras del fósforo renal en la misma
frase:

> *«El contenido de fósforo en la dieta para el manejo de la ERC debe ser del
> 0,2-0,5 % (en base a materia seca) mientras se mantiene una relación de Ca:P de
> 1,1-1,3:1»*

**La primera mitad ya está aplicada y cuadra.** El 0,2-0,5 % de materia seca son
**500 a 1.250 mg/1000 kcal** a la densidad de 4.000 kcal/kg MS con la que convierte
todo el repo, y el techo de fósforo que el motor aplica al renal es **1.200**:
dentro de la banda, en su extremo alto.

**La segunda mitad no está aplicada, y el motor tiene el mecanismo hecho.** El
bloque `ratios` de `patologias.json` existe desde el 10 de septiembre precisamente
para esto —una patología que pide su propio cociente entre dos nutrientes— y se
estrenó con el Ca:P de 1,1-2,0 del oxalato. `renal` no tiene ninguno.

**MEDIDO el 12-sep** sobre los 216 menús del catálogo precalculado:

| Ca:P | Menús |
|---|---|
| dentro de **1,1-1,3** | **130** |
| por debajo de 1,1 | 58 |
| por encima de 1,3 | 28 |

O sea que **seis de cada diez menús ya cumplirían**, que es una situación muy
distinta de la del ratio de la TVT (P-23), donde solo 25 de 216 caían dentro. Aquí
la banda es estrecha por arriba y por abajo, así que apretar los dos lados a la vez
puede dejar sin menú a perros concretos: eso hay que medirlo con el solver antes de
encenderlo, como se hizo con la vitamina E.

⚠️ **Y hay que mirarlo junto a los otros tres Ca:P que ya conviven en el repo**, que
son cuatro bandas para la misma cosa:

| Fuente | Banda | Estado |
|---|---|---|
| FEDIAF, perro sano | 1,0-2,0 | **aplicada** |
| SACN5, urolitos de calcio | 1,1-2,0 | **aplicada** en `oxalato` |
| Bartges, enfermedad renal crónica | **1,1-1,3** | **no aplicada** — es de una PATOLOGÍA, así que sigue abierta (esta pregunta) |
| TVT, perro sano | 1,3-1,5 | **no se aplica** — el requisito del perro sano lo fija FEDIAF (P-23, cerrada el 12-sep) |

**La pregunta:** ¿se le pone a `renal` el ratio 1,1-1,3? Y antes de eso, la que
hace falta para contestarla: ¿se mide con el solver cuántos perros se quedan sin
menú al apretar la banda por los dos lados, como se hizo con el suelo de vitamina
E?

---

### P-31 · La dieta que trata la cistinuria puede causar la miocardiopatía que el motor sabe prevenir

| | |
|---|---|
| **Dueño** | **Cris Carles** |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo el capítulo 185 de Ettinger |

El capítulo 185 —*Manejo nutricional de la enfermedad del tracto urinario
inferior*, de Yann Queau y Vincent C. Biourge— cierra su apartado de cistina así:

> *«En perros con cistinuria se han visto deficiencias de carnitina y de taurina, y
> se recomienda la taurina y la carnitina para prevenir la cardiomiopatía dilatada,
> especialmente si el animal está siendo alimentado con una dieta restringida en su
> precursor, la metionina»*

Es un enlace directo entre dos patologías que el motor ya tiene:

- `cistina` lleva hoy un **techo de sodio y nada más**. Su tratamiento real es
  bajar la metionina y la cistina **por debajo del mínimo de FEDIAF**, que el motor
  no hace y por eso no formula menú automático.
- `dcm_taurina_respondedora` ya aplica **suelos de taurina (250 mg/1000 kcal) y de
  L-carnitina (50)**, de la Tabla 36-4 de SACN5.

O sea que el motor **tiene las dos cifras** y no las cruza. Y el cruce importa
justo donde el motor se retira: la ración que trata la cistinuria es la que crea el
riesgo.

**La pregunta:** cuando un profesional formule para `cistina` por la vía firmada
—que es la única que puede bajar de FEDIAF—, ¿deben entrar automáticamente los
suelos de taurina y L-carnitina? ¿Y debe decirlo el aviso de `cistina` aunque hoy
esa patología no genere menú, para que quien la marque sepa que la dieta que va a
pautar tiene ese efecto?


---

### P-32 · Ettinger aprieta la grasa por debajo de SACN5 en tres patologías digestivas, y una de sus cifras no cabe

| | |
|---|---|
| **Dueño** | **Cris Carles** (es elegir entre dos fuentes clínicas para el mismo perro) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo enteros los capítulos 178 y 182 de Ettinger |

Los capítulos **178** (Debra Zoran, enteropatías) y **182** (Richard Hill,
hiperlipidemia) dan techos de grasa **más bajos** que los que el motor aplica hoy, y
los tres techos de hoy salen de SACN5:

| Patología | Techo de hoy | De dónde sale | Lo que pide Ettinger |
|---|---|---|---|
| `enteropatia_cronica` | 37,5 g/1000 kcal | SACN5 Tabla 57-1, «Fat 12 to 15% for dogs» | *«6-15 % de MS en perros o <3 g de grasa/100 kcal»* = **30** |
| `ple_linfangiectasia` | 37,5 | SACN5 Tabla 58-1, «Fat <15%» | con albúmina <1,5 g/dl, *«concentraciones de grasa <3 g/100 kcal o <10 % de MS»* = **30** o **25** |
| `hiperlipidemia` | 30 | SACN5 Tabla 28-2, 12 % MS | *«<25 g de grasa/Mcal en alimentos para perros»*, y en los casos que no responden, *«menos de 18 g de grasa/Mcal»* = **25** y **18** |

⚠️ **Y esto no es nuevo: es la tercera cifra de una discrepancia que ya estaba
abierta.** `FEDIAF_CONTRA_OTRAS_FUENTES.md` §1 tiene desde el 10 de septiembre el
caso de la grasa en linfangiectasia, donde SACN5 (37,5, en materia seca) y Fascetti
(16,7, en kcal) se llevan un factor de 2,2 por culpa de **qué unidad lleva el
«15 %»**. Ettinger cae **en medio** de las dos y —esto es lo que aporta— da la cifra
**en las dos unidades a la vez**, así que ya no es una pelea de unidades: es una
pelea de números.

**MEDIDO el 12-sep**, con el solver, 30 s por peldaño, adultos de 3, 10, 22 y 40 kg,
recorriendo la escalera entera como hace la API. La celda dice **en qué peldaño sale
el menú** (0 = estricto, 5 = el último):

| | 3 kg | 10 kg | 22 kg | 40 kg |
|---|---|---|---|---|
| `enteropatia_cronica` 37,5 (**hoy**) | 2 | 1 | **0** | **0** |
| `enteropatia_cronica` 30 | 2 | 2 | 2 | 2 |
| `enteropatia_cronica` 25 | **5** | **5** | **5** | **5** |
| `ple_linfangiectasia` 37,5 (**hoy**) | 2 | 1 | **0** | **0** |
| `ple_linfangiectasia` 30 | 2 | 2 | 2 | 2 |
| `ple_linfangiectasia` 25 | 2 | 2 | 2 | 2 |
| `hiperlipidemia` 30 (**hoy**) | 2 | 2 | 2 | 2 |
| `hiperlipidemia` 25 | **5** | 3 | 3 | 4 |
| `hiperlipidemia` **18** | **sin menú** | **sin menú** | **sin menú** | **sin menú** |

**Lo que sale de la medida, y es distinto para cada una:**

1. **Los 30 de la enteropatía y de la linfangiectasia caben sin drama**: el menú
   sigue saliendo en los cuatro pesos, en el peldaño 2. Cuesta uno o dos peldaños de
   forma, que es exactamente lo que la regla 3 autoriza y lo que el motor dice.
2. **Los 25 no son iguales en las dos**: la linfangiectasia los aguanta en el
   peldaño 2 y la enteropatía se va al 5, el último. La diferencia no es la grasa:
   es que `enteropatia_cronica` lleva **además** un techo de potasio (2.750) que la
   otra no tiene.
3. **Los 18 de la hiperlipidemia NO CABEN con este catálogo**, en ningún peldaño ni
   en ningún peso. Y eso es un dato sobre el catálogo, no sobre la cifra: 18 g de
   grasa por 1000 kcal es una ración casi sin grasa, y la fuente misma la describe
   como una dieta casera formulada para los casos que no responden a nada.

**La pregunta, que son tres:** ¿se bajan los dos techos de 37,5 a 30, que es lo que
cuesta un peldaño? ¿Se baja el de la hiperlipidemia de 30 a 25, que cuesta tres?
¿Y los 25 de la linfangiectasia se ponen como **tope condicional** —igual que la
pancreatitis tiene el suyo— cuando el veterinario declare albúmina <1,5 g/dl, que es
la condición exacta con la que la fuente lo pide? Los 18 no se proponen: no caben, y
está medido.

---

### P-33 · El suelo de fibra de la diabetes está en una unidad y el número que decide está en otra

| | |
|---|---|
| **Dueño** | **Cris Carles** (es elegir cifra clínica) **y una fuente que no existe** (el factor entre las dos fibras) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo entero el capítulo 181 de Ettinger |

`diabetes` aplica un **suelo de fibra de 17,5 g/1000 kcal**, que sale de convertir el
extremo bajo de la Tabla 29-3 de SACN5 («Fiber 7 to 18%» de materia seca). El
capítulo 181 de Ettinger (Jennifer Larsen) da el número para lo mismo y **en otra
unidad**:

> *«si se elige una dieta rica en fibra, parece que la concentración de esta debe
> exceder los 55 g de FDT/Mcal, ya sea de una fuente de fibra insoluble o de una
> mixta, para que proporcione un efecto beneficioso»*

Y antes, describiendo el estudio que lo mide:

> *«no se observó beneficio alguno en perros con DM alimentados con dietas que
> contenían 18-20 g de FDT/Mcal cuando se compararon con dietas moderadamente bajas
> en fibra con 14 g de FDT/Mcal»*

⚠️ **FDT es fibra dietética TOTAL, que es exactamente lo que trae el campo `fibra`
del catálogo** — BEDCA, CIQUAL y USDA publican fibra total. La cifra de SACN5 está
en **fibra BRUTA**, que es otra cosa: el aviso de unidad lleva escrito en la ficha de
`ple_linfangiectasia` desde el 11 de septiembre, con la frase del NRC 2006 («The
crude fiber method accounts for only 5 to 20 percent of the total fiber in a food»),
y nadie había puesto las dos cifras una al lado de la otra.

Puestas: **el motor exige 17,5 g de fibra total y esta fuente mide 18-20 g de fibra
total y lo llama «ningún beneficio»**. No es que el número esté mal convertido; es
que el número convertido cae en la banda que el estudio usó como control.

Y Ettinger añade una tercera fuente al mismo agujero, el cap.190 (Amy Farcas), que
dice que ni siquiera la fibra «total» es total: su método *«no mide el componente de
FDBPM»*, las fibras de bajo peso molecular.

**MEDIDO el 12-sep**, mismo montaje que la P-32 (solver, 30 s por peldaño, escalera
entera, adultos de 3, 10, 22 y 40 kg). La celda es el peldaño en el que sale el menú:

| Suelo de fibra | 3 kg | 10 kg | 22 kg | 40 kg |
|---|---|---|---|---|
| **17,5 (hoy)** | **0** | **0** | **0** | **0** |
| 35 | 2 | **0** | **0** | **0** |
| 45 | 2 | 2 | 2 | 3 |
| **55 (Ettinger)** | **5** | **5** | **5** | **5** |

O sea: **los 55 caben, en los cuatro pesos, pero solo en el último peldaño** — el
que suelta el techo del 10 % de verdura. Tiene sentido y es lo que hay que mirar
antes de decidir: llegar a 55 g de fibra por 1000 kcal significa un menú con mucha
más verdura de la que el criterio BARF de este motor considera normal. **Eso es
FORMA, no nutrición**, así que la regla 3 lo permite y el menú lo diría — pero
convertiría *todos* los menús de diabetes en menús del último peldaño, y eso es una
decisión de producto además de clínica.

**La pregunta:** ¿se sube el suelo de fibra de la diabetes? Y si sí, ¿hasta 55, que
es lo que la fuente mide como umbral de beneficio y sale en el peldaño 5, o hasta
45, que sale en el 2-3? Antes de eso hay una pregunta para la fuente que nadie ha
podido contestar todavía: **cuántos gramos de fibra total son 7 g de fibra bruta**,
que es el número que convertiría la cifra de SACN5 a la unidad del catálogo. La
Tabla 5-9 de SACN5 dice que la proporción va del 0 % al 82 % según el ingrediente,
así que ese factor único **no existe**.

---

### P-34 · El menú que el motor entrega no sirve para la fase de DIAGNÓSTICO de una alergia, y ahora lo dice

| | |
|---|---|
| **Dueño** | **Elena** (es producto: si hace falta un modo distinto) **y Cris Carles** (si ese modo es defendible) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, leyendo entero el capítulo 186 de Ettinger |

El capítulo 186 (Manon Paradis) prohíbe durante la dieta de eliminación
exactamente lo que este motor mete **siempre**:

> *«No se deben administrar otras fuentes de alimento (no se permiten premios,
> huesos, sobras de la mesa, juguetes para masticar con saborizantes; glucosamina,
> vitaminas, ácidos grasos esenciales omega-3, antiparasitarios con sabor oral,
> pasta de dientes con sabor»*

Y, por si quedaba duda:

> *«Por lo general, no se recomienda agregar suplementos (p. ej., ácidos grasos
> esenciales [AGE], vitaminas, minerales) durante la prueba de eliminación, ya que
> esta prueba tiene un tiempo limitado en el cual debe realizarse»*

La regla 5 de `CLAUDE.md` deja **Suplementos y Extras siempre libres** —aceites,
semillas, huevo, sal— porque son la herramienta con la que el solver cierra los 43
requisitos. Un menú de `reaccion_adversa_alimento` lleva, casi siempre, aceite de
salmón: o sea justo lo que la fuente dice que confunde la prueba. Eso ya estaba a
medias en el aviso `fase_de_diagnostico`, que habla **solo** del omega-3 porque es
lo que dice SACN5; esta fuente extiende la lista a todo.

**Lo que se ha hecho el 12-sep**: se dice, en el aviso nuevo
`lo_que_la_prueba_no_puede_llevar`, con las dos citas, con la frase de la propia
fuente de que una dieta de prueba *«aunque incompletas y desequilibradas, se pueden
utilizar de forma segura para la fase de diagnóstico»* en un adulto sano, y con las
dos duraciones (8-10 semanas si hay síntomas de piel, 2-4 si solo son digestivos).
Lo vigila el BLOQUE 64.

**Lo que NO se ha hecho, y es la pregunta.** El motor **no puede** formular sin
suplementos: sin ellos no cierra los 43 requisitos, y entregar un menú que no cumple
choca de frente con la regla 1, que es la que no se toca. Así que las opciones son
dos y las dos son decisión de producto:

1. **Dejarlo como está**: el motor entrega el menú de comer y el aviso explica que
   la fase de prueba es otra cosa y la lleva el veterinario.
2. **Un modo «prueba de eliminación»** que formule sin Suplementos ni Extras,
   entregue el menú **marcado como incompleto**, con la duración máxima escrita y
   sin semáforo verde — porque no lo estaría. Eso sería la primera vez que este
   motor entrega algo que no cumple FEDIAF, y por eso no lo hago solo. Tendría que
   ir por la vía firmada de `VETERINARIOS.md`, como cualquier otra prescripción por
   debajo del suelo.

**La pregunta:** ¿se construye ese modo, y por la vía firmada? Y si no, ¿basta con
el aviso?


### P-37b · Al cachorro de raza grande con premios se le cae el techo de calcio del libro: ¿es eso lo que queremos, o hay que topar los premios?

**Abierta el 13 de septiembre de 2026. Dueña: Elena (decisión clínica).**

Encontrada en PRODUCCIÓN, con su propio perro. Cairo, American Staffordshire,
cachorro de casi 7 meses, 20 kg, que pesará unos 31 de adulto: **no salía ningún
menú en cuanto se declaraban premios.**

**Lo que pasa, y las dos cifras son correctas:**

| | mg/1000 kcal | De dónde |
|---|---|---|
| Suelo de calcio | **2500** | FEDIAF, Tabla III-3b **nota b**: cachorro que pasará de 15 kg de adulto |
| Techo de calcio | **2750** | SACN5 Tabla 17-1, columna del que pasará de **25 kg**, y Fascetti cap.10 («in order to prevent panosteitis») |

Entre los dos hay un **10 %** de sitio, y los premios se lo comen: la ración se
formula con las kcal que quedan y se le sigue exigiendo el día entero de
nutrientes (regla 3-bis), así que **el suelo sube y el techo no**.

| Premios | Suelo escalado | ¿Cabe bajo 2750? |
|---|---|---|
| ninguno | 2500 | sí |
| 5 % | 2632 | sí, justo |
| **9,1 %** | **2750** | **el punto exacto donde deja de caber** |
| 10 % (lo que RECOMIENDA la fuente) | 2778 | no |
| 20 % | 3125 | no |

**Lo aplicado, que NO es una decisión nueva:** manda FEDIAF y el techo del libro
cede, que es la regla ya escrita en `topes_de_la_etapa` desde el 8 de septiembre
—la que salva al perro a dieta— y la regla general del repo: si una fuente
contradice a FEDIAF, gana FEDIAF. El suelo es un REQUISITO y el techo una
RECOMENDACIÓN. El máximo duro de FEDIAF (4500) sigue puesto, el menú se verifica
igual, y el menú **dice** que el techo ha cedido
(`techos_del_libro_que_no_se_aplican`).

**LO QUE HAY QUE DECIDIR, Y NO LO DECIDE EL MOTOR.** Medido sobre el menú que
sale: con premios al 10 % el calcio se queda en **2824 mg/1000 kcal** — dentro
del 4500 de FEDIAF y un 2,7 % por encima del 2750 que las dos fuentes caninas
recomiendan justo para este perro y justo por la panosteitis. O sea que el
arreglo devuelve el menú y **paga un precio en el nutriente donde más pesa**,
aunque el precio es ahora el mínimo que la aritmética permite (la primera
versión, con el techo desapareciendo del todo, pagaba 3746).

Las dos salidas:

1. **La de hoy**: el techo **sube hasta el suelo** y se queda pegado a él, sale
   menú, y se dice a cuánto ha subido. El calcio de Cairo se queda en **2824**
   —a un 2,7 % del consejo del libro— en vez de los 3746 de la primera versión.
   La holgura con la que sube (2 %) es **nuestra** y va medida; y como es
   nuestra, si con ella no saliera menú el motor la suelta y reintenta.
2. **Topar los premios al 9 % en el cachorro de raza grande** y decírselo al
   dueño, para que las dos cifras quepan. ⚠️ Eso es cambiar lo que el dueño ha
   declarado que come su perro, y el motor no sabe si de verdad come menos
   premios o si lo que pasa es que la ración se le queda corta. Es criterio
   clínico.

Y hay una tercera que NO vale y queda escrita para no volver a proponerla:
**bajar el techo del libro a la vez que el suelo** no se puede, porque entonces
la ventana es un punto y no hay menú; y **dejar el techo puesto** es lo que
dejaba a Cairo sin comida.

Lo vigila el BLOQUE 101, con el fallo puesto de tres formas.

### P-36 · El rango de peso de la raza ACOTA el peso adulto que se le estima a un cachorro, y para 65 razas ese rango es ahora el del estándar de concurso

| | |
|---|---|
| **Dueño** | **Elena** (es producto: qué significa el rango que se le enseña al dueño) **y Cris Carles** (si acotar así es defendible) |
| **Bloquea** | No |
| **Abierta desde** | 12 de septiembre de 2026, por la noche, al aplicar los estándares de la FCI |

`pesoAdultoDesdeCurva` usa `pesoMin`/`pesoMax` de la raza para **acotar** el peso
adulto que la curva de crecimiento le proyecta a un cachorro. Hasta hoy esos dos
números no tenían fuente publicada; desde hoy, 65 razas los tienen —el estándar
oficial de la FCI— y 20 de ellas han cambiado de cifra.

Y ahí hay una pregunta que no es de dato sino de qué significa el número. **El
estándar de la FCI es el peso al que debe estar un ejemplar de CONCURSO**, no la
horquilla de lo que pesa un perro de esa raza que vive en un piso. Son dos cosas
distintas y el motor las usa como si fueran una:

- Donde la FCI da un rango de verdad, aplicarlo es lo correcto y además suele
  ensanchar (el Kuvasz gana 10 kg de techo, y con el techo viejo a un macho se le
  proyectaba de menos).
- Pero donde da **un peso por sexo** —el Setter Gordon, «en los machos debe ser de
  29,5 kg»— convertirlo en rango dejaría la horquilla en 25,5-29,5 y un Gordon de
  33 kg, que existe, quedaría acotado a 29,5. Por eso **no se ha aplicado**: de un
  punto no se inventa una horquilla alrededor. Esas filas se quedan con su cifra
  vieja, sin fuente, y lo dicen en su `ojo`.

**La pregunta tiene dos mitades.** (1) ¿El rango que acota tiene que ser el del
estándar, o el rango real de la población, que ninguna de las cuatro fuentes del
motor publica? (2) Y la de antes, que Elena ya planteó ese mismo día: *«¿y si solo
metemos las razas y el peso estimado adulto se calcula con el resto de datos?»* —
o sea quitar el acotado y dejar que decida la curva de FEDIAF, que es la que sí
tiene fuente. Si se quita, esta tabla deja de decidir kcal y pasa a ser solo lo
que se le enseña al dueño, y las dos mitades de la pregunta se caen solas.

**Lo que NO cambia mientras tanto:** el menú sale verificado igual. Esto mueve las
kcal que se le piden a un cachorro, no si el menú cumple.

---

### ⚠️ CONTESTADA LA MISMA NOCHE, y la segunda mitad está aplicada

**Elena, 12 de septiembre de 2026:** *«Pues si esto es lo correcto hazlo sí»*.

Antes de tocar nada se miró **cómo lo hacen los demás**, que es lo que convirtió
esto de una opinión en una decisión con respaldo:

| Quién | Cómo saca el peso adulto de un cachorro |
|---|---|
| Curvas de **WALTHAM** (50.000 perros; son las que publica Royal Canin para veterinarios) | Diez gráficas por **sexo** y por **banda** de peso adulto. El peso adulto sale de la trayectoria del propio cachorro. El estándar de raza se usa solo para ELEGIR la banda: *«the weight of the parents ... or via the breed standard»* |
| **MyVetDiet** (software español de raciones) | Tiene tabla de más de 180 razas y la llama **«pesos indicativos»**. En cachorro, *«cálculo automático del peso adulto del cachorro»* con la curva del animal |
| **Pet Diet Designer** | No usa la raza: pide *«current and full grown weights»*, los escribe la persona |
| Calculadoras de consumo de «¿cuánto va a pesar mi cachorro?» | Sí usan tabla por raza, y son las menos rigurosas (±10-20 %) |

O sea que **nadie usa el rango de la raza para acotar el número**, y nosotros sí.

**MEDIDO antes de quitarlo**, sobre las 270 razas a 4, 6 y 9 meses: el recorte
movía el peso adulto en **47 de 1620** casos, con **3,0 % de mediana** de kcal y
**6,9 % el peor**. Y lo que importa no es el tamaño sino la dirección: casi todos
son cachorros que apuntan por debajo del mínimo de su raza, y ahí el recorte les
**sube** las kcal. Al Mastín Español de 9 meses le añadía **152 kcal al día**, y es
un cachorro de raza gigante, justo donde FEDIAF avisa de deformidades
esqueléticas por sobrealimentar.

**Aplicado el 12 de septiembre por la noche**, en los dos repos: fuera las dos
líneas y fuera los parámetros, que no se quedan aceptándose sin hacer nada. La
tabla de razas sigue sirviendo para el peso de respaldo cuando no hay edad ni
peso con los que calcular, y para lo que se le enseña al dueño. Lo vigilan el
apartado 9 del BLOQUE 96 y `tests/der-contrato.spec.js`, los dos comprobados con
el recorte devuelto.

**LO QUE SIGUE ABIERTO es la otra mitad: el SEXO.** La tabla de MyVetDiet da
«pesos indicativos diferenciados para machos y hembras», y la FCI publica machos
y hembras por separado en **la mitad** de sus estándares —el Kuvasz son 48-62 en
machos y 37-50 en hembras, y nosotros guardamos 37-62 para los dos—. La ficha ya
pregunta el sexo. Con el recorte fuera esto ya no decide kcal, así que ha dejado
de ser urgente, pero sí decide lo que se le enseña al dueño y la banda que le
tocaría. **Dueño: Elena.**


### ~~P-37 · La condición corporal de un cachorro no mueve NADA~~ · **REDUCIDA el mismo día: la fuente SÍ da la cifra**

| | |
|---|---|
| **Dueño** | **Cris Carles**, y solo para lo que queda: si el ±10 % de escalón basta o hay que graduarlo |
| **Bloquea** | No |
| **Abierta desde** | 13 de septiembre de 2026 · **reducida ese mismo día** |
| **Qué la redujo** | SACN5 cap.17, **Tabla 17-5, paso 5** — la buscamos en las demás fuentes y estaba en el mismo capítulo que ya habíamos leído: «This amount is only an estimate and is intended to be used as a starting point. The puppy's body condition should be monitored regularly (at least every two weeks) and **the amount fed should be increased or decreased by 10%**, depending on body condition score». El cap.27 repite la regla para mantenimiento: «increase or decrease the amount in 10% increments» |
| **Qué se aplicó** | `ajuste_por_condicion_en_crecimiento` en `der.py` y `ajustePorCondicionEnCrecimiento` en `src/der.js`: **×1,1 por debajo de la banda ideal de FEDIAF (4-5), ×1,0 dentro, ×0,9 por encima**, y sin BCS no se toca nada. La app manda el BCS en `calcularDER`. Cinco casos nuevos en `der_casos.json`, en los dos repos |
| **Qué queda** | Que un cachorro en BCS 6 y uno en BCS 9 reciban el MISMO −10 %. Es lo que dice la fuente —la regla es de escalón, no proporcional, y lo que cierra la diferencia es repetirla cada dos semanas— pero conviene que lo confirme quien firma |

`der.py` aplica la corrección por peso ideal solo `if not en_crecimiento`. O sea
que en un cachorro el BCS **no hace absolutamente nada**. Medido, el mismo
cachorro de 20 kg a los 7 meses:

| | BCS 3 | BCS 5 | BCS 7 |
|---|---|---|---|
| Cachorro | 1439 kcal | 1439 kcal | 1439 kcal |
| El mismo perro, adulto | 1431 | 1040 | **578** |

Y SACN5 cap.17 dice lo contrario de lo que hacemos, con todas las letras:

> «All puppies should have their body condition evaluated and reassessed at
> least every two weeks to allow for adjustments in amounts fed and, thus,
> growth rates»

> «regularly assessing body condition provides more immediate feedback about
> optimal nutritional status than using body weights based on estimated adult
> size»

La frase anterior a esa segunda llama al camino que sí usamos —estimar el peso
adulto— «a markedly less effective option».

⚠️ **Y lo que NO se puede hacer es aplicarlo por mi cuenta**, porque el capítulo
dice *que se reevalúe y se ajuste* y no dice **cuánto**. Eso es un bucle
clínico, no una ecuación, y ponerle un factor inventado sería exactamente lo que
`auditar_conversiones.py` existe para impedir. La regla del propio capítulo
—3 × RER hasta el 50 % del peso adulto, 2,5 × después, 1,8-2 × al llegar al
80 %— tampoco sirve de salida: **también necesita el peso adulto**, o sea que es
la misma dependencia con otra forma, y encima en tres escalones donde nosotros
tenemos una curva continua medida en 493 cachorros (Klein 2019, la que publica
FEDIAF en su Tabla VII-8b).

**La pregunta es**: ¿cuánto se corrige la ración de un cachorro por cada punto de
BCS por encima o por debajo de 5, y a partir de qué edad? En adulto se corrige
dividiendo por el exceso medido (Tabla VII-2 de FEDIAF), y esa tabla es de perro
adulto: no hay base para aplicársela a un cachorro, que está creciendo.


### ~~P-40 · No se guarda ni una pesada~~ · **HECHA el mismo día, y falta ejecutar el SQL**

⚠️ **ERA LA P-38 Y SE RENUMERA A P-40 el 15 de septiembre**, porque había **dos
preguntas con el número 38**: ésta y la de la densidad energética. Es el mismo
fallo que los dos BLOQUE 98 del 13 de septiembre y la lección es la misma: **un
número es la única forma que tiene el repo de decir de qué se está hablando**, y
dos con el mismo número es una referencia rota que no da ningún error. Se
renumera ÉSTA y no la otra por el mismo criterio que se usó con los bloques: la
de la densidad está citada desde `CLAUDE.md`, `PENDIENTE.md`, `LECTURAS.md`, el
sello de `main.py` y cuatro sitios de `pruebas_completas.py`, y ésta desde dos.
Las dos referencias que había —`PENDIENTE_NUTRICION.md` §22 y `der.py`— van
cambiadas en el mismo commit.

| | |
|---|---|
| **Dueño** | **Elena**, y solo para una cosa: ejecutar `supabase/migracion-pesos.sql` en el SQL Editor |
| **Bloquea** | No |
| **Abierta desde** | 13 de septiembre de 2026 · **hecha ese mismo día** |
| **Qué se hizo** | La tabla `pesos` con su RLS y **una pesada por perro y día**; `apuntarPesada` / `getPesadas`; lo mismo **sin cuenta** en `almacen.js`, porque ese es el camino por defecto y las semanas que más importan son las de un cachorro; que suban al crear la cuenta (`migrarLocalACuenta`), que es donde se perdían en silencio el peso objetivo y el nivel de premios; y `pesoRealDelMes()`, que pone cada pesada en **el mes que tenía el perro** y no en el del calendario. Tres pruebas en `tests/historial-de-pesadas.spec.js`, las tres comprobadas con el fallo puesto |
| **Si no se ejecuta el SQL** | La app NO se rompe: `apuntarPesada` avisa por consola y devuelve `null`. Perder una pesada es molesto; no poder guardar la ficha es que la app no sirve — la misma decisión que ya había con las columnas nuevas |
| **Lo que abre** | Con dos o más pesadas se puede estimar el peso adulto de la **trayectoria del propio cachorro**, que es lo que hacen WALTHAM y MyVetDiet. Eso cerraría el tramo de 12 a 24 meses sin depender de las 185 razas sin fuente. Hoy el tramo lo tapa el suelo de la Tabla VII-8a, que es un parche bueno pero un parche |

Elena, ese día: *«como aún así se va a pesar al perro, cada dos semanas se va a
ir actualizando»*. La mitad de eso ya pasa y la otra mitad no.

- ✅ Al cambiar el peso, la estimación **se rehace**: la curva usa el peso de
  hoy, así que cada pesada corrige el peso adulto proyectado.
- ❌ Pero **no se guarda ninguna pesada**. `pesoActual` se sobrescribe.
- ❌ La pantalla «Evolución y crecimiento» dibuja la curva esperada y **un solo
  punto real**, el de hoy (`real: i + 1 === edad.totalMeses ? pesoActual : null`),
  aunque lleves un año pesándolo. Promete una serie que no existe.
- ❌ Y hay una tabla `historial_peso` con su `registrar_peso` en
  `persistencia.py` **que no la llama nadie** y que no existe en Supabase.

**Por qué importa más que una pantalla bonita**: con dos o más pesadas se puede
estimar el peso adulto de la **trayectoria del propio cachorro**, que es lo que
hacen las curvas de WALTHAM (50.000 perros) y lo que hace MyVetDiet. Eso cerraría
de golpe los dos huecos que hoy tapa la tabla de razas —el cachorro sin fecha de
nacimiento y el tramo de 12 a 24 meses, donde **202 de las 270 razas (75 %)
siguen creciendo** y la ecuación de FEDIAF ya no vale— sin depender de las 185
razas que no tienen fuente.

**Lo que hace falta decidir**: si se crea la tabla en Supabase, cada cuánto se le
pide al dueño que pese, y si las pesadas viajan al motor (hoy el peso adulto lo
calcula la app y el motor solo lo recibe, que es la duplicación declarada del
DER).


### P-38 · Una ración de este motor va a 5,20 kcal/g de materia seca, y los 135 límites que vienen de una tabla en % de materia seca se convirtieron suponiendo 4,0 — **REDUCIDA el 15 de septiembre: los siete límites LEGALES ya están aplicados**

⚠️ **LO PRIMERO QUE HAY QUE SABER AL ABRIR ESTA PREGUNTA (15 de septiembre de
2026).** Elena, leyendo la medida: «pues corrige por densidad no??», y después
«haz lo que diga FEDIAF tal como lo diga FEDIAF, **pero comprueba bien en la
fuente antes de hacer nada**». Al comprobarlo, la pregunta se parte en dos y una
de las dos mitades **deja de ser una pregunta**, porque la fuente ya la contesta.

**Lo que FEDIAF dice, y son DOS cosas distintas que yo había mezclado**:

| | Lo que dice §3.2.1 | Cuántos |
|---|---|---|
| **Los máximos LEGALES de la UE** | *«Legal maxima in EU legislation are expressed on 12% moisture content and **they do not account for energy density**. Therefore in these guidelines **they are only provided on a dry matter basis**.»* | **7** — cobre, yodo, hierro, manganeso, selenio, zinc y el (L) de la vitamina D |
| **Todo lo demás** (los mínimos, y los seis máximos nutricionales) | FEDIAF **los imprime por 1000 kcal** en su Tabla III-3b, y el motor usa **ese** número | el resto |

Y se ve **en la propia tabla**: la celda de máximo de esos siete está **VACÍA**
en la III-3b, solo pone «(L)». **No hay número por 1000 kcal que usar** — el que
aplicaba el motor lo habíamos hecho nosotros con el ×2,5 de la Tabla III-2, que
es justo la conversión de la que la nota al pie dice *«These conversions assume
an energy density of 16.7 kJ (4.0 kcal) ME/g DM. For foods with energy densities
different from this value, the recommendations should be corrected for energy
density»*.

**✅ APLICADO EL 15 DE SEPTIEMBRE**, en la forma que no supone ninguna densidad:
el límite entra en el MILP como restricción lineal sobre la materia seca del
propio menú —`Σ nut·g ≤ L_ms · Σ MS·g`—, y el semáforo hace la misma cuenta.
Medido: **10 de 10 perros de referencia con menú verde**, con el hueco de humedad
contado como agua entera (el lado que más aprieta), y el selenio pegado al 100 %
del techo nuevo. ⚠️ Y **212 de los 216 menús precalculados se pasaban** de un
límite legal (selenio 206, cobre 101, vitamina D 28, zinc 1): el catálogo se
regeneró entero. Lo vigila el **BLOQUE 113**.

⚠️ **Y LO QUE **NO** SE TOCA, que es la mitad que casi me llevo por delante**:
los **mínimos**. Mi primera lectura decía que corregir por densidad los bajaría
un 23 % y que eso era «lo que dice la fuente al pie de la letra». **Es falso**:
FEDIAF publica los mínimos por 1000 kcal en la Tabla III-3b, anclados a la
ingesta diaria (*«Recommended minimum values are based on an average daily energy
intake of either 95 kcal/kg0.75 (398 kJ/kg0.75) or 110 kcal/kg0.75 (460 kJ/
kg0.75) for dogs»*), y el motor usa esos
números. No hay ninguna conversión nuestra que corregir ahí. Lo mismo los seis
máximos nutricionales que sí vienen impresos por 1000 kcal — calcio 6,25/4,00/
4,50 · fósforo 4,00 · vitamina A 100 000 · vitamina D (N) 800 · lisina 7,00 ·
linoleico 16,25 —, comprobados celda a celda contra `fediaf_tabla_III_3b.txt`.

**LO QUE SIGUE ABIERTO**, y es lo de abajo: los **122 límites que NO son de
FEDIAF** —las 94 cifras de `patologias.json`, las 24 de
`recomendaciones_libro.json` y las 4 de `requisitos_condicionales.json`—, que
vienen de tablas de SACN5 y Fascetti en % de materia seca y se convirtieron con
el mismo ×2,5. Ahí la fuente **no** dice que haya que corregir, y sus tablas
están escritas para un **pienso**, donde 4,0 kcal/g MS es la densidad de verdad.
Medido: corrigiéndolos también, **3 de 11 perros pierden el menú**, y los que
aprietan son el fósforo y el sodio del libro. Y sigue abierta la otra mitad: que
SACN5 recomienda una densidad de 3,5-4,5 kcal/g MS y ninguno de nuestros menús
la cumple.

Lo de abajo se conserva tal como se escribió el 14 de septiembre, porque la
medida de la densidad y el recuento de las 135 siguen siendo buenos — lo que
cambia es qué parte de ellos era una pregunta.

### P-38-bis · lo escrito el 14 de septiembre (la medida sigue valiendo; el alcance no)

| | |
|---|---|
| **Dueño** | **Cris Carles** (es nutrición: si el consejo de una fuente es una concentración en el alimento o una cantidad por energía) **y Elena** (porque decide cuántos perros se quedan sin menú) |
| **Bloquea** | **No.** Y hay que decirlo con cuidado, porque la primera versión de esta ficha ponía que sí: una cifra nueva en % de materia seca entra hoy con el mismo 23 % de holgura que las otras 135, y **eso no es motivo para dejarla fuera** — dejarla fuera es no tener límite ninguno, que es peor. Lo que sí es obligatorio es que declare su `densidad_kcal_por_g_MS: 4.0` como las demás, para que el día que esto se decida se muevan TODAS a la vez y ninguna se quede con el supuesto viejo escondido |
| **Abierta desde** | 14 de septiembre de 2026, al cerrar la humedad del catálogo |

**Lo que dice la fuente**, en la misma página en la que publica la tabla de
conversión que usa este repo:

> «These conversions assume an energy density of 16.7 kJ (4.0 kcal) ME/g DM. For
> foods with energy densities different from this value, the recommendations
> should be corrected for energy density.»
> — FEDIAF 2025, §3.2.1, Tabla III-2

Y encima de esa misma frase, sobre los límites legales:

> «Legal maxima in EU legislation are expressed on 12% moisture content and they
> do not account for energy density. Therefore in these guidelines they are only
> provided on a dry matter basis.»

**Lo que hace el motor hoy**: convierte con el ×2,5 de esa tabla, que es
exactamente `10 / 4,0`. Lo hacen **135 cifras**: las 94 de `patologias.json`, las
24 de `recomendaciones_libro.json`, las 4 de `requisitos_condicionales.json` —las
tres declaran `densidad_kcal_por_g_MS: 4.0`— y **los 13 máximos de FEDIAF que la
Tabla III-3b no da por 1000 kcal**, porque los publica solo en base materia seca:

| | |
|---|---|
| **Límites legales de la UE** | vitamina D · hierro · yodo · selenio · zinc · cobre · manganeso |
| Máximos nutricionales | calcio · fósforo · vitamina A · linoleico · lisina |

**Lo que estaba sin medir, y ya no**: hasta el 14 de septiembre no se podía ni
comprobar el supuesto, porque sin la humedad de cada alimento no hay materia
seca. Con las 144 fichas cerradas, una ración de este motor va a

> **5,20 kcal por gramo de materia seca** (de 4,05 a 6,18 en los 216 menús del
> catálogo), no a 4,0.

⚠️ Y la banda no depende de lo que falta: los 18 alimentos sin humedad —los
suplementos en polvo, mandato 5, cuya etiqueta no la declara— pesan una mediana
de **7,4 g sobre 730 g de ración**, así que contarlos como agua en vez de como
materia seca mueve la mediana menos de dos décimas. La medida se sostiene con el hueco
dentro, que es lo que hay que poder afirmar antes de usarla.

Y el motivo no es un fallo de datos: una ración BARF es proteína y grasa **sin
almidón, sin fibra y sin ceniza de relleno**, y esas tres son justo lo que baja la
densidad de un pienso. La carne fresca va de 4,4 a 6, los aceites a 8,9 y la
verdura a 3.

**O sea que las 135 van un ~23 % flojas.** Los techos permiten un 23 % más de lo
que la fuente quiere decir, y los suelos exigen un 23 % más de lo que pide.

**Lo que cuesta, medido** (14 de septiembre, sobre los 216 menús del catálogo y
sobre el solver):

| | |
|---|---|
| Celdas hoy en VERDE que se pasarían de un **máximo de FEDIAF** corregido | **515** (lisina 143 —que es la excepción ya escrita y no cuenta—, **selenio 155, calcio 116, cobre 92, vitamina D 9**) |
| Celdas hoy en verde que se pasarían de un **techo del libro** corregido | **219** (fósforo 127, calcio 47, vitamina D 43, sodio 2) |
| ¿Sigue habiendo menú con los 13 máximos apretados un 23 %? | **8 de 8** perros de referencia (adulto 3, 20 y 40 kg; cachorro joven 10; crecimiento 18; sénior 22; lactante 22; gestante 20) |
| ⚠️ Pero un factor fijo NO basta | los menús que salen con el factor apretado son a su vez **más densos** (4,90 a 5,87 kcal/g MS), así que el factor que de verdad les tocaría va de ×0,68 a ×0,82. Un número fijo se queda corto en unos perros y se pasa en otros — por eso la forma correcta es la del punto 2, que no usa ningún factor |

⚠️ **Y NO ES SOLO LA CONVERSIÓN: SACN5 RECOMIENDA UNA DENSIDAD, Y NO LA
CUMPLIMOS.** Encontrado el mismo día leyendo su capítulo 13:

> «Active young adult dogs should be fed a food with an energy density range of
> **3.5 to 4.5 kcal/g dry matter (DM)**. The energy density range of foods for
> inactive/obese prone dogs should be lower (**3.0 to 3.5 kcal/g DM**).»
> — SACN5 5.ª ed., cap.13 «Feeding Young Adult Dogs»

Medido sobre los 216 menús: **3 caen dentro de la banda del perro activo, 213
están por encima, y ninguno dentro de la del perro inactivo o propenso a
engordar.** Eso ya no es un supuesto de conversión: es una recomendación sobre
el alimento que el motor no cumple, y de una fuente distinta.

⚠️ Pero **decir que esto es un fallo sería pasarse**, y por eso es una pregunta:
esa banda está escrita para un pienso, donde la densidad decide el VOLUMEN que
el perro come y por tanto si se queda saciado. Una ración BARF es agua y
proteína, y su volumen por caloría no se parece al de un pienso. Si la banda
aplica o no a una dieta cruda lo dice un clínico, no una cuenta — y es
exactamente la misma pregunta que la de arriba, vista por el otro lado.

**Lo que hay que decidir, y son tres cosas:**

1. **Si se aplica.** La fuente lo dice y la regla del repo es que si lo dice el
   manual se aplica. Aprieta, que es el lado seguro, y **cabe**: 8 de 8.
2. **Cómo.** El factor no es una constante: depende de la densidad del menú, que
   no se sabe hasta resolverlo. Pero **no hace falta ningún factor**: un límite en
   % de materia seca es **lineal en los gramos** —`Σ nutrienteᵢ·gᵢ ≤ (L/100)·Σ
   materia_secaᵢ·gᵢ`—, así que se puede escribir tal cual en el MILP y el supuesto
   de los 4,0 desaparece del motor en vez de corregirse. El sitio es
   `verificar.maximo_de()`, que ya es «EL ÚNICO SITIO» por el que leen el máximo
   el solver, el semáforo, el analizador y `suplementar()`.
3. **Qué pasa donde el techo corregido cae por debajo de un suelo de FEDIAF.** Ya
   pasa: el techo del fósforo del sénior (1750) corregido da **1149**, y el mínimo
   de FEDIAF del adulto es **1160**. Manda FEDIAF y el techo se cae —eso ya está
   escrito y es la regla 3-ter— pero hay que decir cuántos son.

⚠️ **Y lo que NO se ha hecho a propósito**: bajar ninguna cifra. Ninguna de las
135 se toca. Lo que está en cuestión es la conversión, no el número de la fuente.

⚠️ **MEDIDO EL 15 DE SEPTIEMBRE, Y CAMBIA LA RESPUESTA AL PUNTO 2: HECHO BIEN,
NO CABE.** El 14 se midió con un **factor fijo** del 23 % y salían **8 de 8**
perros con menú. Pero un factor fijo no es la corrección: la corrección es la del
punto 2 —el límite escrito sobre la materia seca del propio menú—, y eso es un
**punto fijo**, porque apretar el límite cambia el menú y el menú cambia su
densidad. Iterando hasta ese punto fijo sobre once perros de referencia:

| | |
|---|---|
| Perros que **pierden el menú** | **3 de 11** — adulto 3 kg, sénior 22 kg y cachorro joven 10 kg |
| El factor que de verdad les toca | **0,728 · 0,678 · 0,696** — más apretado que el 0,77 del factor fijo, que es por lo que aquel salía 8 de 8 |

**Y lo que aprieta NO es FEDIAF: son los techos del LIBRO.** Soltando **un solo**
límite corregido y dejando los demás apretados:

| Perro | Vuelve a salir soltando |
|---|---|
| Adulto 3 kg | **fósforo** *o* **sodio** (los dos, techos de SACN5 Tabla 13-3) |
| Cachorro joven 10 kg | **fósforo** (techo de SACN5 Tabla 17-1) |
| Sénior 22 kg | ninguno solo — hacen falta varios |

Eso importa **más que el recuento**, porque cambia de qué clase de límite estamos
hablando. Ninguno de los 13 máximos de FEDIAF —los siete legales de la UE entre
ellos— es el que deja al perro sin comer: el que aprieta es una **recomendación de
un libro de texto**, que es justo la clase que ya cede cuando choca (regla 3-ter
de `CLAUDE.md`: *un techo del LIBRO cede ante un suelo de FEDIAF, y se dice*).

Así que la decisión de Elena no es «¿corregimos o no?» sino **«¿los techos del
libro se corrigen también, o se quedan con su conversión de 4,0?»**, y hay
argumento para lo segundo: esos techos se leyeron de una tabla escrita para un
**pienso**, donde 4,0 kcal/g MS es la densidad de verdad — corregirlos es
aplicarles una densidad que su propia tabla no contempla. Los máximos de FEDIAF
no tienen esa salida: su nota dice expresamente que hay que corregir.

**No se ha aplicado nada.** Está medido y escrito, que es la regla.

Lo vigila el **BLOQUE 111**, que mide la densidad real en cada batería y falla si
se mueve — para que el día que cambie no se siga citando un 23 % que ya no existe.


### P-39 · Las diez piezas con hueso ponen el 29 % de las kcal de un menú, y su energía está calculada con unos factores que NRC dice expresamente que no valen para el hueso

| | |
|---|---|
| **Dueño** | **Cris Carles** (es nutrición: qué digestibilidad tiene el colágeno del hueso en el perro) |
| **Bloquea** | No, pero mueve el divisor de los 43 requisitos |
| **Abierta desde** | 14 de septiembre de 2026, midiendo la humedad |

**Lo que dice la fuente**, y la excepción va entre paréntesis en su propia frase:

> «The resulting Atwater factors of 4 for protein, 9 for fat, and 4 kcal·g⁻¹ for
> carbohydrate (nitrogen-free extract; NFE) still work amazingly well for
> ingredients in homemade diets for dogs: meat, offal **(except bones and bone
> meal)**, poultry, fish, highly purified starch products, milk products, and
> even chocolate.»
> — NRC 2006, cap.3

Y dice de dónde sale ese 4: *«Atwater factors include a digestibility of 98
percent for carbohydrate, 96 percent for fat, and **90 percent for protein**»*.
La proteína del hueso es **colágeno**, y ahí es donde el supuesto se cae.

**Lo que hace el motor hoy**: las diez fichas con hueso llevan su energía
calculada con Atwater exacto. Comprobado rehaciendo la cuenta en las diez —
`4 × proteína + 9 × grasa` da **el número de la ficha al decimal** en las diez.
No hay término de hidratos, y eso está bien: la Tabla 1 de Köber mide materia
seca, proteína, grasa y cenizas, y las tres últimas suman la primera (en el
cuello de ternera, 20,3 + 7,5 + 19,7 = 47,5 contra 48,0 de materia seca). La
ceniza es mineral, no da kcal y Atwater no la cuenta, así que **el error no está
ahí**: está en la digestibilidad.

**Lo que expone, medido sobre los 216 menús del catálogo:**

| | |
|---|---|
| Menús con alguna pieza con hueso | **213 de 216** |
| kcal que ponen esas piezas | **mediana 29,0 %**, máximo **48,0 %** |
| Si su energía estuviera un 10 % alta, el DER del menú se desvía | mediana 2,9 % · peor 4,8 % |
| Si estuviera un 20 % alta | mediana 5,8 % · peor 9,6 % |
| Si estuviera un 30 % alta | mediana 8,7 % · peor 14,4 % |

**Y la dirección importa**: si la energía del hueso está sobreestimada, el menú
entrega MENOS kcal de las que dice, así que el perro come de menos **y** todo
nutriente por 1000 kcal reales va más concentrado de lo que el semáforo mide.
Es decir, aprieta contra los MÁXIMOS — la misma dirección que la P-38, y por eso
las dos se leen juntas.

**Lo que NO se puede hacer, y por eso esto es una pregunta y no un arreglo**:
NRC dice que Atwater no vale para el hueso y **no da ningún factor alternativo**;
tampoco lo dan FEDIAF, SACN5 ni Fascetti, ni Köber mide energía. Poner un número
sería inventarlo, que es exactamente lo que este repo no hace — la misma regla
que deja inertes los tres `documentado_sin_cifra` de
`requisitos_condicionales.json`.

**Lo que hace falta**: una digestibilidad de la proteína del hueso en el perro,
o una medida de energía metabolizable de estas piezas. Con eso el arreglo es de
una línea por ficha.

⚠️ **BUSCADO A FONDO EL 15 DE SEPTIEMBRE, ABRIENDO LAS CUATRO FUENTES, y sigue
sin haber número — pero la búsqueda deja tres cosas que no estaban escritas.**

**1 · NRC dice dónde está el dato, y no es ninguna de nuestras fuentes.** En el
mismo capítulo 3, dos párrafos antes de la frase que excluye el hueso:

> «For diets that consist of usual ingredients, data on digestibility of
> nutrients or ME from tabular values may be used (**see Meyer and Zentek,
> 2001**). […] While this approach does not take into account interactions among
> nutrients and effects of processing, it has been used successfully for
> **homemade** and semi-purified experimental diets (Kienzle, 1995).»

O sea que NRC **sí** considera resuelto el problema para una dieta casera — pero
remitiendo a una tabla de EM por ingrediente que está en *Meyer & Zentek,
Ernährung des Hundes* (2001), que no está en el repo. **Ése es el documento que
cierra esta pregunta**, y hasta ahora no sabíamos ni que existía.

**2 · Y la otra ecuación de NRC tampoco sirve, comprobado.** Su Tabla 3-1 trae
una segunda vía —la de los alimentos preparados: GE por bomba calorimétrica o
`5,7×proteína + 9,4×grasa + 4,1×(NFE+fibra)`, y una digestibilidad energética
que sale de `91,2 − 1,43 × %fibra bruta`—. **No vale para el hueso**: esa
digestibilidad se predice desde la FIBRA BRUTA, y un hueso no tiene. Queda
descartada, que es mejor que dejarla como posibilidad sin mirar.

**3 · Fascetti da el MECANISMO y dice que el crudo es el peor caso.** Cap.11,
literal:

> «some protein sources have inherently low digestibility due to antinutritional
> factors (e.g. legumes) or **dimensional features such as numerous cross-links
> (e.g. collagen)**. In those cases, **processing methods such as heating are
> necessary to improve digestibility**.»

La proteína del hueso y del cartílago **es** colágeno, y una ración BARF va
cruda. O sea que no solo es menos digestible que el 90 % que supone Atwater:
está en el extremo en el que la fuente dice que haría falta cocinarla para
subirla. Eso confirma la DIRECCIÓN del error —la energía del hueso está
sobreestimada— sin dar la magnitud.

**Y lo que se ha comprobado que NO existe**: FEDIAF solo da un método *in vivo*
(§6.1.2, prueba de alimentación con seis perros y recogida de heces y orina), y
**Köber 2017 no mide energía** — su Tabla 1 trae materia seca, proteína bruta,
grasa bruta, cenizas, calcio y fósforo, y nada más. Las cuatro fuentes del repo
están miradas y ninguna tiene el número.


### P-42 · A un perro RENAL se le ha quitado el suelo de vitamina E, y la causa es que en el catálogo no hay vitamina E suelta

| | |
|---|---|
| **Dueño** | **Cris Carles** (es clínica: si el antioxidante de la Tabla 37-9 se puede quedar fuera mientras no haya ficha) y **Elena** (es dato: conseguir la ficha) |
| **Estado** | **abierta** — aplicado el apagado el 15 de septiembre de 2026, con la cifra escrita y medida |

**Qué dice la fuente.** SACN5 5ª ed., Tabla 37-9 «Key nutritional factors for
dogs and cats with chronic kidney disease», fila «Antioxidants … ≥400 IU vitamin
E/kg of food for dogs». Convertido con el factor del d-α-tocoferol natural de la
Tabla VII-14 de FEDIAF (1 UI = 0,671 mg) y la densidad de 4,0 kcal/g MS: **67,1
mg/1000 kcal**. Es **la misma cifra** que piden otras tres tablas del mismo libro
—artrosis (34-2), obesidad (27-4) y hepatobiliar (68-8)— y el techo del perro
sano de los capítulos 13 y 14.

**Qué ha pasado.** El BLOQUE 61 se puso rojo: la `renal`, marcada `formulable:
true`, dejó de dar menú **a ningún peso**. La causa no es la cifra, es de
**datos**, y ya estaba escrita dos veces en el repo: **en el catálogo no hay un
suplemento de vitamina E suelto**, solo los nueve multivitamínicos. Llegar a 67,1
obliga a meter **dos**, y dos ya no caben debajo de los **siete máximos LEGALES
de la UE**, que desde el 15 de septiembre van sobre **materia seca**, que es la
única forma en que FEDIAF los publica (§3.2.1).

**La medida, sobre el perro de referencia del BLOQUE 61** (adulto de 20 kg, DER
950):

| | |
|---|---|
| Con el suelo puesto | **sin menú en ninguno de los ocho peldaños** |
| Sin el suelo | menú en `proporcion_minima_y_un_suplemento_mas` |
| Vitamina E de ese menú | **34,5 mg/1000 kcal** (la mitad de lo que pide SACN5) |
| Zinc de ese menú | **99,0 % de su techo LEGAL** |
| Selenio | 93,5 % |

O sea: **no hay sitio para el segundo multivitamínico**. Subir la vitamina E se
paga en zinc, y el zinc es **ley**, no una recomendación.

**Lo que se ha hecho, que es el procedimiento y no una decisión clínica**: la
cifra **no se ha bajado**. Se ha movido a
`limites_escritos_que_el_solver_no_aplica` de `patologias.json` con esta medida,
con su cita literal y con su conversión intactas, que es lo que este repo hace
con un número de la fuente que no cabe.

⚠️ **Las otras tres la siguen aplicando, y eso está medido una por una**:
artrosis, obesidad y hepatopatía salen con **dos multivitamínicos**, bajando de
peldaño. Que tres la apliquen y una no **no es incoherencia**: es que en las tres
cabe y en la cuarta no. Uniformar bajando la cifra sería inventársela; uniformar
quitándola de las cuatro sería tirar un límite que sí cabe.

**Lo que hay que decidir:**

1. **Cris** — ¿es aceptable que un perro renal se quede sin ese antioxidante
   mientras no haya ficha? ¿O la renal debería dejar de ser `formulable` hasta
   entonces, que es la otra salida que el propio BLOQUE 61 nombra?
2. **Elena** — conseguir la **ficha de un suplemento de vitamina E suelto**
   (`DATOS_QUE_FALTAN.md`). Es el mismo dato que desbloquea el suelo del perro
   sano, apagado desde el 11 de septiembre por lo mismo. El día que entre, se
   vuelve a poner `aplicado_por_el_solver: true` y **la batería tiene que salir
   verde**: esa es la comprobación de que el problema era el catálogo y no la
   cifra.

⚠️ **Y la trampa del factor, que sigue viva**: los 67,1 salen del d-α-tocoferol
**natural**, que es el más permisivo de los siete de la Tabla VII-14. Si la ficha
que entre es de **acetato sintético**, el mismo requisito son **100 mg/1000
kcal**, no 67,1.


---

### P-43 · El único producto que arregla el hueco de metionina que señaló Cris lleva **DL**-metionina, y ella pidió **L**

| | |
|---|---|
| **Dueño** | **Cris Carles** (es clínica: si la forma DL vale) y **Elena** (es de producto: si se mete esa ficha) |
| **Estado** | **abierta** — encontrado el 15 de septiembre de 2026 al revisar las etiquetas de los suplementos |

**De dónde viene.** `REVISION_NUTRICIONISTA.md` §3: «Empieza a salir carente de
metionina, que se tiene que suplementar como **L-metionina**». Está marcado ❌ y
es el tercero de los tres puntos suyos que siguen sin cubrir. El motor **sí**
verifica la metionina (está en `verificar.MAPA` desde el 28 de agosto, con su
mínimo y el de metionina+cistina), así que **detecta** la carencia; lo que no
hay es **con qué arreglarla**.

**Lo que se ha encontrado.** **`V-INTEGRA Renal Met`**, del mismo fabricante que
las cinco fichas de esa gama que ya están en el catálogo, **se vende en España**
(viralataspetshop.es) y su etiqueta está publicada entera. Declara, entre sus
aditivos nutricionales por kg:

> «DL-metionina: 58.200 mg»

y lo confirma su propio bloque analítico: «Metionina 5,8 %». Son **5.820 mg de
metionina por 100 g**, que es un orden de magnitud por encima de cualquier otra
cosa del catálogo. El resto de su etiqueta es el hermano del `V-INTEGRA Renal`
que ya tenemos, con el fósforo a 0 %: ácido fólico 9,6 mg/kg, cloruro de colina
49.000, taurina 39.200, yodo 44, calcio 14,8 %, proteína bruta 10,2 %, grasa 2,5 %,
humedad 1,8 %.

**Por qué no lo meto yo y ya está.** Por dos cosas, y las dos son de quien firma:

1. **DL no es L.** La D-metionina se convierte a L en el perro, pero **no gratis
   ni del todo**, y NRC 2006 (cap. «Methionine · Dogs») dice que **da la
   eficiencia de utilización de la DL respecto a la L precisamente porque no es
   1:1**. Contar los 5.820 enteros sería darlo por resuelto; contar la mitad
   sería inventarme un factor. Y la dirección del error importa: la metionina
   tiene **mínimo y no máximo**, así que contar de más deja al perro corto sin
   que el semáforo lo vea.
2. **Y NRC avisa de toxicidad, de la DL en concreto.** «Biourge et al. (2002)
   reported methionine toxicosis in six hunting dogs fed a single meal of about
   300 g of a normal diet containing 47 g DL-methionine·kg–1» —ataxia,
   desorientación, temblores, vómitos, y convulsiones en el cachorro de 6 meses—
   y concluye: «it would appear that the **SUL for DL-methionine is well below
   47 g·kg–1** diet containing 4 kcal ME·g–1». Del mismo párrafo sale lo otro:
   «If they used L-methionine, **D-methionine would appear to be considerably
   more toxic than the L-form**».

**Lo que hace falta para cerrarla**, y es poco: que Cris diga **(a)** si la
DL-metionina le vale para lo que ella pedía, y **(b)** con qué factor se cuenta
la mitad D. Con eso la ficha entra en una tarde, con su dosis máxima de etiqueta
y su tope, como cualquier otra. Mientras tanto **no se mete**, porque una ficha
de metionina con el número mal contado es peor que no tenerla: el motor daría la
carencia por arreglada.

**Y hay una alternativa que también es de producto**: la DL-metionina de grado
pienso al 99 % existe suelta y barata, pero se vende **a granel de 25 kg** y sin
etiqueta de producto para mascota. Que eso sea o no aceptable es decisión de
Elena, no mía.

---

### ⚠️ ACTUALIZADA EL MISMO DÍA: Elena pasa DOS productos, y uno resuelve la mitad de la pregunta

Elena: «¿Y estas? **VETFOOD L-Methiocid** … **napfcheck Vet-MET**».

**Las dos son L-metionina, no DL.** O sea que la mitad clínica de esta pregunta
—«¿vale la forma DL?»— **deja de hacer falta**: hay producto con la forma que
pidió Cris. Pero solo una de las dos se puede meter hoy:

| | Qué declara | ¿Entra? |
|---|---|---|
| **napfcheck Vet-MET** | «L-Methionin: **600.000 mg**» por kg = **60 g/100 g**. Es POLVO, así que la cifra entra directa. Analíticos completos (proteína 40,4 % · grasa 2,1 % · fibra bruta 15,2 % · ceniza 1,8 %) y dosis (hasta 2 g al día por cada 5 kg de peso). Y es **la misma marca** del `napfcheck Novomineral proLEBER` que ya está en el catálogo | **Sí** |
| **VETFOOD L-Methiocid** | «L-metionina (500 mg/2 kapsułki)» = 250 mg por cápsula, y analíticos por 100 g (proteína 59,8 % · fibra 1,4 % · grasa 3,8 % · ceniza 2,7 % · **azufre 7,6 %** · almidón 14,1 %) | **No**, y por un dato concreto: **no publica lo que pesa la cápsula**, así que 250 mg/cápsula no se puede pasar a mg/100 g. El azufre solo da una **cota**: la L-metionina es 21,49 % de azufre por fórmula, así que 7,6 / 0,2149 ≤ **35,4 g/100 g** — y encima esa cota es floja porque el hidrolizado de ave que lleva dentro también aporta azufre. Una cota no es una cifra |

**Lo medido, que es lo que hace falta para decidir:**

| | |
|---|---|
| Mínimo de FEDIAF, metionina adulto | **1,16 g/1000 kcal** → un perro de 20 kg a 950 kcal necesita **1,10 g/día** |
| Lo que hace falta de `napfcheck Vet-MET` para cubrirlo | **1,8 g de producto** |
| El alimento del catálogo con más metionina | langostino, 0,709 g/100 g — harían falta **155 g** |
| **Dosis MÁXIMA de la etiqueta** para ese mismo perro | **8 g/día = 4,8 g de metionina**, o sea **4,4 veces el requisito del día entero** |

### ⚠️ Y AQUÍ ESTÁ LO QUE SIGUE ABIERTO, QUE YA NO ES LA FORMA SINO EL TECHO

**Estos productos no son correctores de una carencia: son ACIDIFICANTES
URINARIOS.** El propio napfcheck lo dice —«Methionin Ergänzung zur *Ansäuerung
des Urins*»— y su dosis se ajusta **midiendo el pH de la orina**. El VETFOOD
igual: struvita, una cápsula cada 12 h, hasta 6 meses.

Eso deja **dos** cosas que decide Cris y no yo:

1. **¿Hasta dónde puede subir la metionina en un perro sano?** Porque **FEDIAF no
   pone máximo** —la celda de `maxAdulto` está vacía—, así que si el solver se
   fuera al tope del fabricante **el semáforo no lo pararía**. Y NRC 2006 avisa
   justo de eso: «*Biourge et al. (2002) reported methionine toxicosis in six
   hunting dogs*» —ataxia, temblores, vómitos y convulsiones en el cachorro de 6
   meses— y concluye que «*it would appear that the SUL for DL-methionine is well
   below 47 g·kg–1 diet containing 4 kcal ME·g–1*».
2. **¿En qué patologías NO debe entrar nunca?** Acidificar la orina es lo que se
   busca en la **estruvita** y es **lo contrario** de lo que le conviene a un
   perro con **oxalato** o con **urato**. Hoy el catálogo no tiene forma de decir
   «este alimento sí para esta patología y no para aquella», así que meterlo sin
   contestar esto es dejar que el motor se lo pueda dar a cualquiera.

### ⚠️ Y AL MEDIRLO, LA PREGUNTA CAMBIA DE SITIO: EL MOTOR NO SE QUEDA CORTO DE METIONINA

Antes de meter una ficha había que comprobar lo que esta pregunta llevaba
dándose por hecho desde que la escribió Cris. **Medido sobre los 214 menús del
catálogo**, contra el mínimo de FEDIAF de cada etapa:

| | El más justo | Mediana | Por debajo del mínimo |
|---|---|---|---|
| **Metionina** | **157 %** (Gigante_Adulto/Salmón) | 319 % | **0 de 214** |
| **Metionina + cistina** | **126 %** (Pequeño_Adulto/Ternera) | 238 % | **0 de 214** |

O sea: **ningún menú de este motor sale carente de metionina, y el más justo va
un 26 % por encima del mínimo.** Y no es casualidad ni suerte: la metionina y la
suma metionina+cistina son **dos de los 43 requisitos** que el MILP impone como
restricción dura desde el 28 de agosto, así que un menú corto **no se entrega**.

**Lo que dijo Cris sigue siendo verdad de lo que ella ve** —formulando a mano, una
ración casera se queda corta de metionina con facilidad— pero **no es verdad de
este motor**, y esa diferencia es justo la que había que medir antes de meter un
producto.

**Consecuencia, y es la que ordena el resto:** la ficha de L-metionina **no hace
falta para cubrir el requisito**. Hace falta para otra cosa distinta y legítima —
que un veterinario pueda **acidificar la orina** de un perro con estruvita—, y eso
la manda al **formulador del profesional**, no al automático.

⚠️ Y meterla en el automático sería activamente malo: el solver no la necesita, así
que si la usara sería **porque le sale barata en nutrición por gramo**, que es
exactamente el fallo de la albahaca del 14 de septiembre. Un acidificante urinario
no se le da a un perro sano porque salga eficiente.

### ✅ Y ELENA LO CIERRA EL MISMO DÍA, CON UN CRITERIO MÁS FUERTE QUE EL MÍO

> «Hombre, pero **la dosis de eso la tiene que pautar un veterinario**, ¿no? No
> lo tendría que calcular el motor… O sea, eso es algo que un veterinario receta
> al perro, y que el veterinario tiene que tener acceso a ello **para ponerlo
> dentro del menú y ver cómo cuadran los nutrientes**, pero ya está. Él es el que
> pauta cuánto tiene que tomar.»

Eso es más estricto que lo que yo había escrito, y con razón. Yo proponía «solo
formulador, con el tope del fabricante» — pero **un tope del fabricante sigue
siendo el solver eligiendo los gramos**. Lo que dice Elena es que la cantidad **no
es del motor en absoluto**: la pone quien firma, y el motor solo la cuenta para
cuadrar el resto de la ración alrededor.

**Y eso NO hay que construirlo: ya está.** `POST /formular/autocompletar` acepta
`gramos_por_alimento`, los respeta con 0,5 g de margen, y —lo que lo hace servir—
**si no puede respetarlos NO entrega el menú**: devuelve `factible: false` con
`gramos_fijos_movidos` y la alternativa aparte, porque desde el 29 de agosto está
escrito que «*si se han movido, no es un sí*». O sea que la promesa «tus gramos no
se tocan» se cumple o se dice.

**Lo que hace falta, entonces, es solo esto:**

| | |
|---|---|
| Que la ficha exista en el catálogo, con su etiqueta | para que el veterinario pueda escribirla y el motor sepa qué lleva dentro |
| Que **NO** entre en `accesibles.py` | que es la lista blanca del automático. Lo que no está ahí, el solver no lo usa nunca por su cuenta — es el mecanismo que ya deja fuera a los nueve aceites, a los huevos y al cerebro de ternera |

Con las dos cosas, el techo de seguridad **deja de ser una pregunta del motor**:
el solver nunca elige esa cantidad, así que no hay nada que topar. Queda como lo
que es —una dosis clínica— y quien la pone es quien puede medir el pH de la orina.

**Lo único que sigue abierto para Cris** es lo segundo del bloque anterior, y es
de aviso y no de cifra: que la ficha diga **para qué es y para qué no** —acidificar
la orina se busca en la estruvita y es lo contrario de lo que conviene en oxalato
y en urato—, porque el formulador se lo enseña a un profesional pero la ficha es
donde vive ese dato.

---

### P-44 · La medicación no es comida: la mete quien la receta, no nosotros

| | |
|---|---|
| **Dueño** | **Elena** (es de producto y la propuesta es suya) y **Cris Carles** (qué se le pide a quien firma) |
| **Estado** | **abierta** — propuesta el 15 de septiembre de 2026, sin construir |

**De dónde sale.** Al decidir dónde meter la L-metionina, Elena:

> «igual no debería estar en un catálogo de alimentos, que realmente es una
> medicación… Igual en vez de meter nosotros medicaciones —porque igual luego
> ellos eligen otra marca y la composición es distinta— **que ellos puedan meter
> la medicación que van a usar, meter los datos de la medicación para que el
> motor lo pueda calcular si quieren. Y si no, simplemente poner que han pautado
> esa medicación** y si no meten los datos, no sé si eso tiene sentido…»

**Sí lo tiene, y por una razón que no es de comodidad: nuestro catálogo es de
COMIDA.** Cada ficha lleva su procedencia y la rehace un auditor contra su
fuente. Una ficha de fármaco no puede cumplir eso, porque **el fármaco que
recete el veterinario no es el que hayamos elegido nosotros**: el `napfcheck
Vet-MET` (60 g de L-metionina por 100 g, en polvo) y el `VETFOOD L-Methiocid`
(250 mg por cápsula) son el mismo principio activo con composiciones que no se
parecen. Poner una ficha sería **elegirle la marca a quien firma** y, peor,
contar en su ración una composición que no es la que ha recetado.

### Lo que YA existe en el motor y encaja, que es medio camino

| | |
|---|---|
| **Cinco avisos que nombran un fármaco concreto** | `mitotano_con_comida`, `bromuro_y_cloro`, `potasio_con_diureticos`, `analitica_de_taurina`, `carnitina_dosis_terapeutica`. Dos empiezan literalmente con «**ES UN AVISO DE FÁRMACO, NO UN TOPE**» |
| **Gramos fijados por el profesional** | `POST /formular/autocompletar` acepta `gramos_por_alimento`, los respeta con 0,5 g y, si no puede, **no entrega el menú** |
| **Lo que se come fuera de la ración ya se cuenta** | regla 3-bis: `kcal_de_premios`. Un jarabe o una pasta llevan kcal, y el mecanismo de descontarlas del DER está hecho |
| **`dato_dudoso`** | el sitio del repo para un valor declarado que no se ha podido verificar. `verificar()` lo devuelve junto al menú |

**Y dos huecos reales que esto llenaría:**

1. ⚠️ **El aviso del bromuro sale hoy a quien no le toca.** `bromuro_y_cloro`
   dispara **porque está marcada `epilepsia_idiopatica`**, no porque nadie haya
   dicho que el perro toma bromuro. O sea que se le suelta a todo epiléptico,
   lo tome o no. Y al revés es peor: el bromuro compite con el **cloruro de la
   dieta**, así que en el perro que sí lo toma el cloruro de la ración pasa a ser
   una cifra que hay que vigilar — y el motor no tiene forma de saber que ese
   perro es ese.
2. **La pauta firmada no guarda la medicación.** `PeticionFirmar` tiene
   `paciente` y un `indicaciones` de texto libre, y nada estructurado. Pero
   `VETERINARIOS.md` dice que la pauta se guarda **congelada entera** porque un
   documento firmado tiene que seguir diciendo lo mismo dentro de un año: si el
   fármaco interactúa con la dieta, **pertenece a ese documento**.

### Lo que yo añadiría, y es lo que la propuesta no dice todavía

**(a) No son «con datos / sin datos»: son DOS preguntas independientes.**

| | Qué decide | Ejemplo |
|---|---|---|
| **¿Aporta nutrientes o kcal?** | si hay que contarlo en la ración o la ración sale mal calculada | la L-metionina, un aceite, un suplemento de zinc |
| **¿Interactúa con la dieta?** | si hay que avisar y/o vigilar un nutriente | el bromuro con el cloruro · el mitotano con la comida · los diuréticos con el potasio |

Eso contesta el «no sé si eso tiene sentido» del final: **declarar el fármaco SIN
datos no es inútil**, porque activa la segunda columna entera, que es justo la
que el motor ya sabe hacer y hoy dispara a ciegas.

**(b) Un dato tecleado no tiene auditor, y eso hay que decirlo en el documento.**
Si quien firma escribe la composición y se equivoca en un ×1000 —que es
**literalmente** lo que se encontró el mismo día en seis fichas de suplemento con
la etiqueta publicada delante— el motor se lo cree y **el menú sale verde**. El
catálogo tiene ocho auditores contra eso; un número escrito en el momento no
tiene ninguno. Así que lo que entre por aquí va marcado como **declarado por el
profesional y no verificado**, y eso tiene que salir **en la pauta firmada**:
quien firma tiene derecho a ver que ese número lo puso él y no una fuente.

**(c) El límite, que no se puede cruzar:** el motor **no opina sobre la dosis del
fármaco**. Cuenta lo que aporta a la ración y avisa de lo que ya sabe. Nada más.

**(d) Y esto reclasifica la metionina** (P-43): deja de ser una ficha del catálogo
y pasa a ser **el primer caso de uso de esta puerta**. Lo cual resuelve además lo
de la marca sin tener que elegir ninguna.

⚠️ **Lo que NO desaparece**: la puerta por rol sigue haciendo falta el día que
haya en el catálogo cualquier ficha que el dueño no deba ver, porque hoy
`GET /alimentos` sirve las 164 fichas **sin mirar quién pregunta** y
`/menu/anadir` aceptaría el nombre aunque la pantalla no lo enseñara. Esconder
sin cerrar la puerta es decorado — la lección de `/stripe/portal`.

---

### P-45 · El suelo de vitamina E del perro SANO: ¿67,1 mg/1000 kcal, o el mínimo de FEDIAF?

| | |
|---|---|
| **Dueño** | **Adrián (Ecocan)** — es criterio clínico. Elena, 15 de septiembre: «lo dejamos como pregunta para el nutricionista, que en este caso va a ser Adrián, Ecocan» |
| **¿Bloquea?** | No. El motor aplica el mínimo de FEDIAF, que es el requisito, y se cumple siempre |
| **Abierta desde** | 15 de septiembre de 2026 |
| **Estado** | **abierta** — la cifra está escrita y apagada en `recomendaciones_libro.json`, con sus medidas |

**La pregunta, en una línea:** al perro adulto y sénior **sin ninguna patología**,
¿se le exige la vitamina E del **requisito** (~7 mg/1000 kcal) o la que el libro
recomienda **«for improved antioxidant performance»** (67,1 mg/1000 kcal, casi
diez veces)?

### Las cuatro cifras, y que las tres primeras coinciden

| Fuente | Qué es | mg/1000 kcal |
|---|---|---|
| **FEDIAF 2025**, Tabla III-3b (10,40 UI) | requisito, y es lo que el motor aplica | **6,968** |
| **NRC 2006**, *recommended allowance* | requisito | **7,5** |
| **AAFCO**, mínimo del perfil (50 UI/kg MS) | requisito legal EE. UU. | ~**8,4** |
| **SACN5 5ª ed.**, Tabla 13-3 (≥400 UI/kg MS) | **recomendación** del libro | **67,1** |

Las tres referencias de requisito se parecen entre sí. La cuarta está un orden de
magnitud por encima **y no dice ser un requisito** — el propio capítulo 13 lo
separa: *«The requirement for vitamin E for foods (DM) for adult dogs is 30 mg/kg
(NRC, 2006)»*, y los 400 UI son *«for improved antioxidant performance»*.

### ⚠️ Lo que se leyó del estudio original, que es lo que hace falta para decidir

SACN5 apoya ese 400 en un solo trabajo y lo cita sin dar el detalle. Leído
entero: **Jewell DE, Toll PW, Wedekind KJ, Zicker SC, «Effect of increasing
dietary antioxidants on concentrations of vitamin E and total alkenals in serum
of dogs and cats», *Vet Ther* 2000;1(4):264-72 (PMID 19757574)**. Literal:

> «The total analyzed dietary vitamin E levels for the canine treatment groups
> were **293, 445, and 598 IU vitamin E/kg of food, as fed**.»

> «The **thresholds for significant reduction of serum alkenal concentrations**
> in dogs and cats **were 445 and 540 IU vitamin E/kg of food**, respectively,
> on an as-fed basis.»

Tres cosas que cambian cómo se lee el 400, y las tres son para Adrián:

1. **El 400 de la tabla no es el número del estudio.** El efecto se demostró a
   **445 UI/kg tal cual** —en pienso seco, ~494 UI/kg MS, o sea ~83 mg/1000
   kcal— y el grupo de **293 no dio efecto significativo**. Nuestro 67,1 (=400
   UI/kg MS) queda **por debajo de la única dosis que funcionó** y muy por
   encima del requisito. Está en tierra de nadie.
2. **Lo medido es un biomarcador en suero** —alcanales, o sea peroxidación
   lipídica—, no un resultado clínico. 40 perros adultos sanos, 6 semanas.
3. **Era un estudio de pienso SECO** (Hill's). Una ración BARF fresca no es el
   mismo escenario oxidativo. Y por la relación clásica vitamina E:PUFA vamos
   holgados: **min 0,79 · mediana 4,82 · máx 44,01 UI/g, y 0 de 214 menús por
   debajo** del 0,6 UI/g que recomienda AAFCO (nota *h* de su Apéndice A,
   comprobada contra el documento: *«It is recommended that the ratio of IU of
   vitamin E to grams of polyunsaturated fatty acids (PUFA) be > 0.6:1»*).

### Lo que cuesta aplicarlo, medido

No es que no quepa: **cabe**. Desde el 15 de septiembre hay en el catálogo dos
fichas de vitamina E suelta (aceite de germen de trigo de Beaphar y vitamina E
líquida de MARNYS), y con ellas los perros de referencia sacan menú. Lo que
cuesta es de **producto**:

| Con el suelo encendido, peldaño `estricto` (**un solo bote**) | |
|---|---|
| toy 3 kg · mini 10 kg · mediano 22 kg · grande 40 kg · sénior 8 kg · sénior 28 kg | **0 de 6 sacan menú** |
| Los 6, permitiendo el segundo bote | menú, y el segundo bote es **siempre** una vitamina E suelta |
| cachorro 10 kg · cachorro 25 kg | menú con un bote — pero solo porque este suelo está escrito únicamente en Adulto y Sénior |

**Y con un bote no se puede, por las etiquetas:** ningún multivitamínico del
catálogo aporta 67,1 dentro de la dosis que marca su fabricante. El mejor,
Homemadekun, da 45,7 mg a un perro de 10 kg; el napfcheck 18,0; los seis
V-INTEGRA y el Nutratop llevan **0** desde que se les quitó el conservante (ver
`ETIQUETAS_DE_LOS_SUPLEMENTOS.md`).

Seguridad: ninguna en juego. El techo seguro son 1000-2000 UI/kg MS (NRC, vía
Fascetti cap.14) y el motor aplica **167,75 mg/1000 kcal** — el suelo está 2,5
veces por debajo.

### Por qué está apagado hoy, y qué se descartó

Elena, el 15 de septiembre, leyendo el aviso que tendría que ver el dueño si el
suelo cediera y se dijera:

> «no tiene sentido que un usuario vea ese mensaje, porque no tiene ni puta idea
> de qué le estás hablando»

Se descartó, entonces, la salida que estaba propuesta: que el **suelo** del libro
cediera y se dijera, como ya ceden los **techos** del libro ante un suelo de
FEDIAF (`techos_del_libro_que_no_se_aplican`). Técnicamente se puede; lo que no
se puede es el texto — el canal del dueño no admite «la vitamina E se quedó en 35
en vez de 67», que es la regla COMIDA-NO-NUTRIENTES del 14 de septiembre. Y
decírselo solo al profesional dejaría al dueño con dos botes sin saber por qué.

**Lo que se hace mientras tanto:** el suelo queda `aplicado_por_el_solver: false`
en Adulto y Sénior, con la cifra, la fuente, la conversión y todas las medidas
intactas, y con la maquinaria viva — el **BLOQUE 57** lo enciende a mano y exige
que el solver y el filtro final lo apliquen. El día que Adrián conteste se pone a
`true` y ya está.

### Lo que hay que preguntarle exactamente

1. Para un perro **sano**, adulto o sénior, con una ración **fresca** tipo BARF:
   ¿tiene sentido clínico exigir ~10 veces el requisito de vitamina E, sabiendo
   que el número sale de un biomarcador en pienso seco y que el propio estudio no
   vio efecto por debajo de 445 UI/kg?
2. Si la respuesta es que sí: ¿**67,1** (el 400 de la tabla) o **~83** (el 494
   UI/kg MS que es el umbral real del estudio)? Aplicar el 400 es aplicar una
   cifra que el estudio no demostró.
3. ¿Cambia la respuesta según el **PUFA** de la ración? FEDIAF dice en su §3.3
   que la vitamina E sube con los PUFA y **no da cifra para el perro** — está
   escrito como `documentado_sin_cifra` en `requisitos_condicionales.json`. Si
   Adrián da una regla (por ejemplo la de AAFCO, +0,6 UI por gramo de PUFA por
   encima de 83 g/kg), eso sustituiría a un suelo plano y sería **mejor**, porque
   ataría la cifra a la ración de cada perro en vez de a una media.
4. Y la de al lado: **P-42**, el mismo nutriente en el perro **renal**, hoy en
   `limites_escritos_que_el_solver_no_aplica`. Son la misma pregunta con dos
   poblaciones, y conviene que las conteste la misma persona.

**Dónde está todo:** `recomendaciones_libro.json` →
`por_etapa.Adulto.suelos_por_1000kcal.vitE` (y `Senior`), con el `por_que`
entero. Lo vigila el **BLOQUE 57**.

### ⚠️ LA PRUEBA QUE IBA A CONTESTAR ESTO YA SE HA HECHO, Y SALIÓ QUE NO (16 de septiembre de 2026)

`CLAUDE.md` dice hoy, en dos sitios:

> «El día que entre en el catálogo una ficha de vitamina E suelta se vuelve a
> poner a `true` y la batería tiene que salir verde: **esa es la comprobación de
> que el problema era el catálogo y no la cifra**.»

**Esa comprobación ya se puede dar por hecha, y el resultado es el contrario.**
Las dos fichas de vitamina E suelta (`MARNYS VITAHELP Vitamina E liquida` y
`Beaphar Aceite de Germen de Trigo`) entraron el 15 de septiembre, están dentro,
y con el suelo encendido:

| | |
|---|---|
| Suelo encendido, **un solo bote** | **0 de 6** adultos y séniors — infactible **DEMOSTRADO**, no por reloj |
| Suelo encendido, **dos botes** | 6 de 6 verde, a 70,2 mg/1000 kcal |

Y con la ficha nueva metida a mano para probar (`napfcheck Vitamin Complete`,
550 mg de d-α-tocoferol por 100 g) **no cambia nada**: sigue siendo 0 de 6 con un
bote, y con dos el solver sigue eligiendo la MARNYS.

**La causa es aritmética, no de catálogo.** Para llegar a 67,1 mg/1000 kcal en
una ración de 1100 kcal hacen falta 73,8 mg de vitamina E, y eso son:

| Multivitamínico | vitE mg/100 g | gramos que harían falta |
|---|---|---|
| napfcheck Novomineral proLEBER | 600 | **12,3 g/día** |
| astoral MultiVital BARF | 456,4 | 16,2 g/día |
| Homemadekun | 419,5 | 17,6 g/día |
| NEKTON Dog Easy-BARF | 134,2 | 55,0 g/día |
| Las seis V-INTEGRA y el Nutratop | **0** | imposible |

Y **la dosis que declara la etiqueta de cualquiera de ellos es 1-4 g al día**.
O sea que **ninguna premezcla puede llevar ese suelo a su dosis declarada**,
exista o no exista el producto. **El segundo bote es ESTRUCTURAL.**

**Eso cambia la pregunta que se le hace a Adrián**: ya no es «¿falta un
producto?» sino **«¿vale la pena un segundo bote por una recomendación que no es
un requisito?»**. Y el coste de producto sigue siendo el medido el 15: con el
suelo puesto, **0 de 6** adultos y séniors sacan menú con un solo bote.

---

### P-47 · El catálogo no tiene ficha de zinc, cobre, selenio ni manganeso

| | |
|---|---|
| **Dueño** | **Elena** (es de catálogo y de compra) |
| **¿Bloquea?** | No, pero explica tres cosas a la vez |
| **Abierta desde** | 16 de septiembre de 2026 |

Hay ficha suelta de **Calcio** (2), **Hierro** (1), **Yodo** (2), **Vitamina B**
(2), **Vitamina E** (2), **Omega-3** (4) y **Fibra** (1). De **zinc, cobre,
selenio y manganeso, ninguna**.

O sea que **la única forma que tiene el motor de meter zinc es un
multivitamínico**, y todos traen calcio. Medido sobre nueve productos —los diez
del catálogo más `cdVet Fit-BARF MicroMineral`, `napfcheck Novomineral Balance`,
`Sensitiv`, `BARF Complete` y `Dibaq Sense`— **ninguno baja del 15 % de calcio**,
y siete están entre el 15 y el 21 %. No es casualidad: **existen para dietas
caseras SIN hueso**, donde el calcio lo tiene que poner el bote. Este motor
formula CON hueso, así que ese calcio es lastre.

⚠️ Y el motor tiene la patología **`dermatosis_por_zinc`**, cuyo propio aviso
dice «zinc por boca», **sin ninguna ficha de zinc en el catálogo**.

**Candidato español encontrado y SIN MEDIR**: `Dermovital Zinc` (Stangest,
España), comprimido de 1,3 g con **25 mg de zinc** (quelato de aminoácidos) y
12,5 µg de selenio, **sin calcio declarado**. Lleva además aceite de borraja y
de pescado (EPA 10,8 · DHA 7,2 mg por comprimido) y complejo B, así que no es
zinc puro: es un suplemento de piel.

---

### P-48 · Solo entran productos que se vendan en España

| | |
|---|---|
| **Quién lo decidió** | **Elena**, 16 de septiembre de 2026: «solo pueden ser cosas que se vendan en España, ¿vale? Ya sea en Amazon o en cualquier otra tienda» |
| **Estado** | **cerrada** — es una regla, no una pregunta. Se escribe aquí porque no estaba escrita en ningún sitio |

Ya era como funcionaba el catálogo de hecho (el yoduro potásico declara
«ostrovit.es, envío España») pero no estaba dicho.

**Primer descartado por esta regla:** `napfcheck Vitamin Complete`. Su tienda
(vetbiom.com) tiene la web traducida al español, pero **su propia página de
envíos** lista cinco zonas —Alemania/Austria, Benelux, Polonia/Chequia, Francia
y Dinamarca— y dice «We currently only ship to the countries listed above».
**España no está.**

---

### P-46 · La rotación de proteína no llega al cachorro, y hacerla dura cambia los menús de todos

| | |
|---|---|
| **Dueño** | **Elena** — es de producto: rotar tiene un precio y hay que decidir si se paga |
| **¿Bloquea?** | No. Es variedad, no nutrición: el menú que sale está verde y cumple los 43 requisitos |
| **Abierta desde** | 15 de septiembre de 2026 |

**Qué pasa.** Pidiendo tres menús seguidos para el mismo perro, el adulto cambia
de proteína y el cachorro **no**: repite pollo las tres veces.

| perro | las tres proteínas |
|---|---|
| cachorro joven 12 kg | Pollo · Pollo · Pollo |
| cachorro tardío 15 kg | Pollo · Pollo · Pollo |
| cachorro tardío 6 kg | Pollo · Pollo · Pollo |
| adulto 24,5 kg | Gallina · Ternera · Gallina |
| adulto 8,2 kg | Gallina · Ternera · Gallina |

**Y no es ninguna de las tres explicaciones fáciles**, las tres medidas el mismo
día:

1. **No es que no pueda.** Excluyendo pollo y gallina de verdad, los tres
   cachorros sacan menú (ternera, pavo), 3 de 3. El menú alternativo existe.
2. **No es la cifra de la penalización.** `PENALIZACION_DE_ROTACION` está en 6,0
   (medida ese día: con 2,0 repetían 3 de 6 casas de adultos, con 4,0 ninguna).
   Subida a 12, 20 y 40 el cachorro **sigue repitiendo** — a 40 cambia uno de
   tres. Y 40 estaría por encima de los **12,0** de `PENALIZACION_DE_ENCARGO`,
   que es la línea que no se cruza: repetir proteína es un defecto de variedad,
   no encontrar el alimento es no comer.
3. **No es el margen de optimalidad del solver.** Apretando `mip_rel_gap` de
   0,30 a 0,02 sigue repitiendo.

**La causa, entonces:** la rotación vive en el **objetivo**, y para un cachorro
el menú con pollo es tanto mejor que la preferencia no lo voltea. En
crecimiento los mínimos son más altos y la ventana más estrecha, y la carcasa de
pollo es la forma barata de cerrar el calcio.

### La salida, y por qué no la decide el asistente

Hacer la rotación **dura con plan B**: prohibir como principal la especie del
menú anterior y, si no hay menú, soltarlo y **decirlo**. Es exactamente el
mecanismo que ya tiene el techo del libro (`resolver()` prueba apretado y suelta
si sale infactible), y ya está medido que el menú sin pollo existe, así que
nadie se quedaría sin comer.

**Lo que hay que decidir es el precio**, y es tuyo:

- ¿Prefieres que un cachorro coma pollo tres semanas seguidas, o un menú
  posiblemente **más caro y con más ingredientes**?
- La rotación dura afectaría **también a los adultos**, que hoy ya rotan: les
  quitaría la opción de volver a una proteína buena al tercer menú (hoy hacen
  Gallina → Ternera → Gallina, que es rotación real y perfectamente razonable).
- Y hay un caso donde repetir es lo correcto: un perro con muchas alergias puede
  tener **una sola** proteína viable. Ahí el plan B tendría que soltar y decirlo,
  no dejarle sin menú.

**Mientras tanto** el BLOQUE 11 exige que **el adulto rote** —eso sí está
garantizado, 6 de 6 casas medidas— e **imprime** el caso del cachorro con su
medida en vez de acusar al motor de tener «el mecanismo apagado», que es falso:
el mecanismo está puesto y la especie a evitar le llega al solver.

---

## Cerradas

*(Cuando una pregunta se contesta, se mueve aquí con la respuesta, la fecha y
quién la dio — y si de ella sale una decisión, se escribe en `DECISIONES.md`
y se enlaza.)*

Ninguna todavía.
