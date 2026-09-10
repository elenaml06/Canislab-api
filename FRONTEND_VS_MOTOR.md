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
