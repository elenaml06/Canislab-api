# Lo que el motor sabe hacer y la app no ofrece

**Escrito el 10 de septiembre de 2026**, midiéndolo contra el repo del día y
levantando la app de verdad contra la API de verdad
(`playwright.real.config.js`), no contra lo que recordábamos.

> **Por qué existe.** Elena, el 10 de septiembre: *«todo lo que has hecho en
> backend tiene que poder ser efectivo y servir para algo en el frontend»*. Y
> tiene un precedente que lo justifica solo: los `avisos_patologia` llevaban
> desde el **29 de agosto** viajando con cada menú y la app los tiraba, sin que
> nada saltara. Veinte avisos de doce patologías, escritos con su fuente, que no
> leía nadie.
>
> Esto es el barrido completo de ese mismo tipo de hueco, en las dos
> direcciones: qué patologías conoce el motor y la app no ofrece, y qué campos
> devuelve la API que la app no lee.

---

## 1 · Diez patologías que el motor tiene y la app no ofrece a nadie

> ### ⚠️ RESUELTO EL 11 DE SEPTIEMBRE DE 2026 — y lo que sigue es el registro
>
> Medido ese día: la app ofrece **las 47 patologías del motor, ni una más ni una
> menos**. Las diez de la tabla de abajo tienen casilla, las cinco de la
> cardiopatía dentro de la pregunta del estadio ACVIM. Lo clava
> `tests/vocabulario.spec.js` en `canislab-web`, **en las dos direcciones**: una
> patología del motor sin casilla, y una clave que la app manda y el motor no
> conoce (ésa se tira sin decir nada y el menú sale verde igual).
>
> Y hay una regla nueva encima, de Elena el mismo día: «un dueño, obviamente, no
> puede marcar casillas de veterinario, ni siquiera le deberían salir». De las 37
> casillas que veía el dueño, **quince eran `solo_veterinario`** y ya no le
> salen. La lista no se opina: sale de la cita de la fuente de cada patología, en
> `quien_formula_cada_patologia.json`.
>
> El texto original se deja intacto, porque es el registro de lo que se midió el
> 10 de septiembre.


Ni al dueño ni al veterinario: **no están en la lista `PATOLOGIAS` de
`App.jsx`**, así que no hay casilla que marcar. **Siete de las diez** son
`formulable: true`, o sea que el motor les daría menú hoy mismo.

| Clave | Formulable | Qué aplica el motor | Por qué importa |
|---|---|---|---|
| `cardiopatia_a` | sí | nada (solo aviso) | El consenso ACVIM **no recomienda** dieta en estadio A, y decirlo es la información |
| `cardiopatia_b1` | sí | nada (solo aviso) | Igual: «no drug or dietary treatment is recommended» |
| `cardiopatia_b2` | sí | sodio ≤ **739** | Es lo que la app aplica hoy a *cualquier* cardiópata |
| `cardiopatia_c` | sí | sodio ≤ **625** | Un perro en C recibe hoy 739 |
| `cardiopatia_d` | sí | sodio ≤ **480** | Un perro en D recibe hoy 739 |
| `raza_predispuesta_cobre` | sí | nada (avisos) | Se creó el 7 de septiembre justo para separar «raza predispuesta» de «hepatopatía diagnosticada» |
| `urolitos_fosfato_calcico` | sí | fósforo ≤1500 · magnesio ≤375 · sodio ≤750 · proteína ≤62,5 · vitD ≤9,375 · **Ca:P 1,1-2,0** | Cinco topes y el ratio nuevo del 10 de septiembre, y no llega a nadie |
| `encefalopatia_hepatica` | no | — | Bloqueada a propósito |
| `renal_avanzada` | no | fósforo ≤1200 | Bloqueada: para tratar de verdad hay que bajar de FEDIAF |
| `urolitos_silice` | no | — | Bloqueada por lo mismo |

### 1.1 · El caso de la cardiopatía, que es el que más pesa

La app tiene **una** casilla, «Cardiopatía», y manda la clave genérica
`cardiopatia`, que aplica **sodio ≤ 739**. Ese número es el del **estadio B2**.
El motor tiene los cinco estadios de la escala ACVIM y cada uno su cifra:

| Estadio ACVIM | Sodio que pide la fuente | Lo que recibe hoy |
|---|---|---|
| A (predispuesto, sin enfermedad) | **ninguna restricción** | 739 |
| B1 (soplo, sin remodelado) | **ninguna restricción** | 739 |
| B2 (remodelado, sin síntomas) | 739 | 739 ✅ |
| C (insuficiencia cardíaca) | **625** | 739 |
| D (refractaria) | **480** | 739 |

O sea que **dos estadios reciben un tope que su fuente no pide** y **dos reciben
uno más flojo del que pide**. La app no puede arreglarlo por su cuenta: le falta
la pregunta. Es exactamente el caso que planteó Elena — «si el techo cambia en
función de una analítica o un estadio, hay que preguntarlo».

---

## 2 · Campos que la API devuelve y la app no lee

Medido con la app real hablando con la API real. De los que puede devolver
`/menu/v2`, estos **no aparecen ni una vez** en `src/`:

| Campo | Qué lleva dentro | Qué se pierde |
|---|---|---|
| `choque_de_patologias` | Qué dos límites chocan, de qué patología viene cada uno, su valor, su fuente y su porqué | Cuando dos patologías no tienen menú juntas, el veterinario ve «no se puede» y no **cuál** cede |
| `se_intento_relajando` | Los peldaños que se probaron antes de rendirse | Lo mismo: no se sabe cuánto se intentó |
| `imposible_por_aritmetica` | Que no hay combinación posible **y quitar restricciones no arregla nada** | Se le dice «quita alguna restricción» a alguien que puede quitarlas todas y seguirá sin salir |
| `se_relajo` | La lista de lo que se soltó | El peldaño se pinta, pero no **qué** se soltó |
| `peso_de_referencia` | Sobre qué peso se escalaron los mínimos, y de dónde salió | Es el dato que separa un menú del perro de un menú de otro perro |
| `formulado_como_profesional` | Si el menú salió por la puerta del veterinario | — |
| `peldano_lo_eligio_el_profesional` | Si el peldaño lo eligió él o lo bajó el motor | Un profesional que firma necesita poder afirmar cuál de las dos |

**Y dos de `GET /patologias` que ya se arreglaron el 10 de septiembre**, porque
eran el mismo hueco un piso más arriba: la ficha del veterinario los recibía y
no los pintaba.

| Campo | Qué llevaba dentro | ✅ |
|---|---|---|
| `margen_profesional` | La ventana de cada cifra: suelo, techo y **de dónde sale cada extremo**. Sin él, «fósforo ≤ 1200» no dice si se puede tocar ni hasta dónde | Se pinta, con las dos frases que no dicen lo mismo: bajar del suelo se puede y se firma, pasar del techo legal no lo puede hacer nadie |
| `topes_si_ademas` | El segundo escalón: la grasa de la pancreatitis baja de 37,5 a 25 si además hay obesidad o hipertrigliceridemia | Se pinta, diciendo con qué se activa. Antes se veía 37,5 y parecía el único número |

---

## 3 · Las preguntas que faltan en la ficha

Barrido de `patologias.json`: **24 de las 47** llevan dentro, en su fuente o en
su aviso, una referencia a un estadio, una fase o un valor de analítica. De
esas, el motor ya resuelve unas cuantas partiéndolas en patologías distintas
(los cinco estadios de cardiopatía, los tres escalones renales), que es la forma
correcta — el problema es que la app no las ofrece.

Las que quedan sin forma de preguntarse:

| Patología | De qué depende | Qué habría que preguntar |
|---|---|---|
| `reaccion_adversa_alimento` | La fuente limita la proteína **«dermatologic cases only»** | ¿Reacciona por la piel o por el intestino? En el segundo caso la misma página pide **más** proteína |
| `estruvita` (la casilla conflacionada) | Hoy una sola casilla manda `estruvita` aunque el perro tenga urato o cistina | Cuál de los cuatro tipos de cálculo |
| `pancreatitis` | El tope de grasa baja de 37,5 a 25 **si además** hay obesidad o hipertrigliceridemia | Ya se resuelve marcando la otra patología; falta decirlo en la pantalla |
| `renal` | El estadio IRIS decide si la dieta renal está indicada («by stage 2… clearly indicated when serum creatinine exceeds 2 mg/dl») | El estadio, o al menos la creatinina |

---

## 4 · Lo que hay que decidir (Elena)

1. **Los cinco estadios de cardiopatía en la app**: ¿se pregunta el estadio
   ACVIM al marcar «Cardiopatía»? Si sí, ¿al dueño también, o solo al
   veterinario? Hoy un perro en estadio C recibe el tope del B2.
2. **`urolitos_fosfato_calcico`**: es formulable y no se ofrece. ¿Entra en la
   lista del dueño, como el oxalato, o solo en la del veterinario?
3. **La casilla conflacionada de cálculos**: ¿se parte en cuatro (estruvita,
   oxalato, urato, cistina) o se deja como está y solo la ve partida el
   veterinario?
4. **`raza_predispuesta_cobre`**: no aplica ninguna cifra, solo avisos. ¿Se
   ofrece igual? El aviso ES la información — y se creó el 7 de septiembre justo
   para separar «raza predispuesta» de «hepatopatía diagnosticada».

---

## 4-bis · Quién puede marcar cada patología, derivado de su fuente

**No es una decisión de producto y por eso no está en la lista de arriba.**
Elena lo dijo el 10 de septiembre: «si hay algo que necesita análisis o que
necesita lo que sea, no lo puede formular a alguien que no sea un veterinario,
y las preguntas que hay que hacer son las que sean necesarias para estipular
los valores correctos». Las dos cosas se **deducen** de la fuente de cada
patología, así que se derivaron una a una, con la cita literal que lo
condiciona, en `quien_formula_cada_patologia.json`.

La regla es una sola: **si la fuente condiciona su cifra a un estadio, a una
fase o a un valor de analítica, entonces hace falta preguntarlo — y quien
contesta esa pregunta es quien tiene el informe.** De ahí salen las dos cosas a
la vez, y de ahí sale el reparto:

| Quién | Cuántas | Qué significa |
|---|---|---|
| `solo_veterinario` | 24 | Para elegir la cifra correcta hace falta un dato que solo está en un informe clínico |
| `dueno_con_diagnostico` | 18 | Hace falta que un veterinario la haya diagnosticado, pero la cifra es una sola |
| `dueno` | 5 | La puede marcar quien vive con el perro |

**Y lo que la app hace hoy:** de las 24 `solo_veterinario`, **once** se le
ofrecen al dueño con menú automático sin que nadie le pregunte el dato del que
depende la cifra — `renal`, `renal_proteinuria`, `pancreatitis`, `oxalato`,
`estruvita`, `cardiopatia`, `dcm_taurina_respondedora`, `diabetes`,
`hiperlipidemia`, `reaccion_adversa_alimento` y `epilepsia_idiopatica`. El caso
más claro es la pancreatitis: su fuente baja la grasa de 37,5 a 25 si hay
hipertrigliceridemia, la app no pregunta los triglicéridos, y el perro que
necesita 25 recibe 37,5 **en verde** — porque el semáforo mide contra FEDIAF,
que es el perro sano.

Las once están declaradas con su pregunta en
`SIN_LA_PREGUNTA_QUE_DECIDE_LA_CIFRA`, dentro de
`tests/patologias-app-y-motor.spec.js`. **Esa lista solo puede encoger**: se
quita una entrada el día que la app pregunte de verdad su dato, y hay una
segunda prueba que falla si una excepción caduca.

---

## 5 · Y esto ya no se puede volver a colar

`tests/patologias-app-y-motor.spec.js` (en `canislab-web`) tiene desde el 10 de
septiembre las **dos direcciones**:

- «app → motor», que ya estaba: la app no ofrece patologías que el motor no
  conoce.
- «motor → app», que faltaba: **toda patología `formulable` del motor tiene que
  poder marcarse en la app**, o estar declarada con su motivo en
  `NO_LAS_OFRECE_LA_APP_TODAVIA`. Esa lista **solo puede encoger**: hay una
  tercera prueba que falla si una excepción caduca, o sea si la app empieza a
  ofrecer algo que sigue declarado ahí.

⚠️ Y esa lista ya cazó un error de este mismo documento: la primera versión
decía **once** patologías y **ocho** formulables. Eran **diez** y **siete**:
`dcm_asociada_a_dieta` sí está en la app, y la primera cuenta la perdió porque
el patrón con el que se leyó `App.jsx` exigía los tres campos en un orden
concreto. La prueba usa el patrón bueno y lo dijo a la primera. Es la diferencia
entre contar a ojo y contar con algo que se ejecuta.

---

## 6 · El barrido completo: qué dato escribe la app por su cuenta

**Escrito el 12 de septiembre de 2026.** Elena:

> «COMPRUEBA TODO PARA QUE NINGUN DATO LO MANDE LA APP, TODO TIENE QUE VENIR
> DEL MOTOR»

Barrido de **todas** las constantes de módulo de `canislab-web/src` (los ocho
ficheros de lógica y los tres de pantalla), una por una. La regla para
clasificar es la cadena de siempre: **FUENTE manda → MOTOR la implementa → APP
la ofrece**. Un respaldo no cuenta como copia si la verdad llega del motor y
está comprobado que la app la lee; una lista que la app usa **siempre** sí.

### 6.1 · Lo que ya llega del motor

Razas · tamaños y su rango de peso · etiquetas de condición corporal del dueño ·
niveles de actividad en sus dos registros · la pregunta de premios y sus cuatro
respuestas · las familias de patología (qué pregunta, qué respuestas y a qué
clave lleva cada una) · quién puede marcar cada patología · los grupos de
categorías del catálogo · las seis cifras del BCS que deciden el peso objetivo ·
los 46 nutrientes a los que un profesional puede ponerle un objetivo · **y desde
hoy las 47 patologías con sus dos etiquetas y sus nueve aparatos**.

### 6.2 · Lo que sigue escribiéndolo la app, medido

| Dónde | Qué es | Lo que se ha medido hoy |
|---|---|---|
| `App.jsx` `CATEGORIAS_ALIMENTO` | El catálogo entero, agrupado por categoría y especie | **163 alimentos en el motor, 162 escritos aquí.** Falta «Pets Purest Aceite de Salmón Escocés». Y no es un respaldo: `categoriasDisponibles` se calcula **siempre** de esta tabla (`filtrarCategoriasPorEspecies(CATEGORIAS_ALIMENTO, …)`), así que la pantalla de Personalizar del dueño **nunca** lee `/alimentos`. El formulador del veterinario sí lo lee |
| `App.jsx` `MENUS_EJEMPLO` | Los menús de relleno de la vista previa | **Seis de sus quince alimentos no existen en el catálogo** («Pechuga de pavo sin piel», «Costillas de ternera», «Alitas de pollo» y tres pares «X + Y»). Y el motor tiene los suyos: los 36 menús precalculados de `catalogo_menus.json`, que sirve `/catalogo/{tamano}/{etapa}` — uno de los endpoints que **no llama nadie** |
| `App.jsx` `PESO_ADULTO_POR_TAMANO` | 3 · 6 · 12 · 22 · 32 · 55 kg | De aquí salen las kcal y la etapa de un mestizo. El motor publica el rango real por tamaño en `/vocabulario` (`tamanos.rango_observado_kg`), calculado sobre las 255 razas; estas seis cifras se escribieron a mano. Es la misma forma de fallo que dejó **cuatro de los seis rangos caducados** hasta el 11 de septiembre |
| `bcs.js` `ESCALA_BCS` y `BCS_DESDE_CONDICION` | Los nueve descriptores y los cinco escalones del dueño | El motor sirve los dos (`condicion_corporal.puntos` y `escalones_del_dueno`), pero **sus descriptores clínicos son más pobres que los de la app** («BCS 1/9 — Emaciado» contra «Caquéctico · Costillas, lumbares y pelvis visibles a distancia…»). Aquí la salida NO es que la app lea lo de hoy: es **subir los descriptores buenos al motor** y que la app los lea. Hacerlo al revés empeoraría la pantalla, que es exactamente lo que la regla no quiere |
| `nutrientes.js` `GRUPOS` | Cómo se agrupan los 41 nutrientes en la ficha | El motor no lo tiene. Es el mismo caso que los aparatos de patología, que hoy se han subido: la agrupación es presentación, pero decide qué ve quien lee una ficha. Falla al lado seguro (lo que no esté cae en «Otros» y se ve), así que no esconde nada |
| `topespatologia.jsx` `NOMBRE_NUTRIENTE` | 31 nombres de nutriente para la pantalla de topes | Segunda copia de los nombres que `/vocabulario` ya sirve con los 46 nutrientes del formulador |
| `App.jsx` `ETAPA_A_SUFIJO_API` y `ETAPA_LABEL` | Las cuatro etapas de la app y su nombre | El motor sirve `etapas.con_tabla_propia` y sus equivalencias. La correspondencia con las claves internas de la app es suya, pero **que las cuatro existan** lo decide el motor |
| `supabase.js` `ACTIVIDAD_POR_INDICE` | `baja · media · alta · muy_alta · trabajo` | No es dato del motor: es cómo lo **guarda la base**, y los tres primeros no se pueden renombrar sin romper las fichas guardadas. Lo que sí tiene que cuadrar es **cuántos hay**, y eso ya lo compara `tests/vocabulario.spec.js` contra `der.BASE_ACTIVIDAD` |
| `der.js` entero | La fórmula del DER | **Duplicación puesta a propósito**, con su contrato en `der_casos.json`, el mismo fichero en los dos repos (BLOQUE 23 aquí, `der-contrato.spec.js` allí). No se toca sin regenerar los dos. Ver `CLAUDE.md`, «la duplicación que hay que vigilar» |
| `cesta.js` `ZONAS`, `instrucciones.js` | Cómo se ordena la compra y cómo se manipula cada alimento | No son datos del motor: son de manejo y de tienda. Se quedan |

### 6.3 · El orden en que hay que arreglarlo

1. **El catálogo de Personalizar**, porque es el único de la lista que ya está
   desincronizado y que decide qué come el perro.
2. **`MENUS_EJEMPLO`**, porque enseña alimentos que no existen.
3. **`PESO_ADULTO_POR_TAMANO`**, porque de ahí salen kcal.
4. Los descriptores del BCS — **subiéndolos al motor**, no bajando la app.
5. Los grupos de nutrientes y los nombres de nutriente, que son presentación.
