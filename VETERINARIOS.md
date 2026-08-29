# Rawku para veterinarios — el plan

Escrito el 28 de agosto de 2026, a partir de la pregunta que estaba
abierta en `PENDIENTE.md` desde el 24: *«¿una versión para dueños y otra
para veterinarios?»*. Ese apartado listaba cuatro preguntas que había que
contestar **antes** de escribir código. Ya están contestadas, y están
abajo. Este documento es lo que sale de ellas.

No es una lista de tareas: es el orden en que se puede construir sin
tirar nada de lo hecho, y las tres o cuatro cosas que si se hacen mal no
se arreglan después.

---

## 1. Lo que se decidió, y ya no se discute

| Pregunta | Decisión |
|---|---|
| ¿Una app o dos productos? | **Una app, un repositorio, un motor.** Con un modo profesional que se enciende según quién entra |
| ¿Cómo llega el vet a un perro que no es suyo? | **Las dos formas, en dos fases**: primero pacientes que crea él, después perros que le comparte el dueño. El modelo de datos se hace desde el día uno para que quepan las dos |
| ¿Puede bajar de los mínimos de FEDIAF? | **Sí, declarándolo.** Ver el apartado 10, que es el difícil |
| ¿Quién paga? | **Nadie todavía.** Se abre gratis a unos pocos veterinarios y el precio se decide con lo que se vea |
| ¿Cómo se acredita? | **Número de colegiado y alta a mano.** El modo profesional no se enciende solo |
| ¿Firma el veterinario la pauta? | **Sí, con su nombre y su número de colegiado.** Ver el apartado 11, que es el que más cosas obliga |

Y tres que no se preguntaron porque no tienen dos respuestas razonables:

**El veterinario NUNCA entra en la cuenta del dueño.** Ni «entrar como»,
ni suplantar, ni una contraseña compartida. Entra con **su** cuenta y ve
al perro porque tiene un acceso concedido. La diferencia no es de estilo:
suplantando, la base de datos no puede saber quién generó cada menú —
todo queda a nombre del dueño. Y la primera vez que alguien pregunte
«¿esta pauta la hice yo o la hizo la app?», no habrá forma de saberlo.
Todo lo demás de este documento depende de esto.

**El veterinario siempre tiene cuenta.** Sin cuenta no hay a quién
atribuir una pauta, ni a quién cobrarle el día que se cobre, ni forma de
que sus pacientes sigan ahí mañana. Y no cuesta trabajo: es el mismo
registro que ya existe más un campo.

**El dueño puede no tener cuenta.** En la fase 2, el vet crea la ficha de
un paciente cuyo dueño no ha abierto la app en su vida. Ese es el caso
real de una consulta, y si se exige que el dueño se registre primero, la
función no se usa.

---

## 2. El principio del que sale todo: el modo veterinario no puede ser una degradación para el tutor

Añadido el 28 de agosto, y va antes que el reparto de permisos porque es de
donde sale el reparto.

**La tentación es bloquearlo todo hasta que alguien firme, y eso mata el
producto**: el tutor paga y recibe menos que ayer. La regla es la contraria:
**sin validación la app hace todo lo que hace hoy, más decirte qué haría con
el diagnóstico y qué dato exacto le falta.**

> «Con la creatinina y el UPC podría formular para IRIS 2.»

Eso convierte. Un muro no. Y de paso es la frase que hace que el tutor vaya
al veterinario, que es justo lo que queremos.

### Lo que el tutor puede hacer siempre, haya veterinario o no

- **Todo el producto de perro sano, sin recortes.**
- **Meter síntomas y seguimiento.** Y esto no es una concesión que se le
  hace: **los instrumentos validados están diseñados para que los rellene
  el dueño**. El CBPI, el LOAD, el CIBDAI y el PVAS son *owner-reported*
  por construcción, y la frecuencia respiratoria en reposo es la medición
  domiciliaria con mejor evidencia que existe. Quitárselos al tutor sería
  usarlos al revés de como fueron diseñados.
- **Ver el menú entero y los 30 requisitos**, sin nada escondido detrás del
  veterinario.
- **Pedir una dieta para un diagnóstico.**
- **Exportar el histórico.**
- **Retirar el acceso del veterinario y desactivar el modo terapéutico.**
  Ésta se olvida siempre y es la que más importa: **es su perro y sus
  datos**. Un diagnóstico validado no puede dejar al tutor encerrado fuera
  de su propia cuenta.

### Lo que sí exige diagnóstico validado

**Que el motor aplique restricciones por debajo de los mínimos de FEDIAF.**

Ahí está la frontera, y es limpia y no arbitraria: **es exactamente donde
deja de ser una dieta completa y equilibrada y pasa a ser una
prescripción.** No hay que discutir caso por caso qué se bloquea y qué no
— lo dice el propio estándar.

Son las nueve marcadas `formulable: false`. ⚠️ **Esa lista no está en
ninguno de los dos repositorios** (comprobado el 28 de agosto: cero
apariciones de `formulable` en `Canislab-api` y en `canislab-web`). Viene de
otro sitio y hay que traerla aquí antes de construir la fase 4, porque es
la que define qué necesita firma.

Y con ella, **todo lo que necesite un valor de laboratorio que el tutor no
puede producir**: estadio IRIS, tipo de cálculo, calcemia, triglicéridos.

### Lo que solo puede el veterinario

- **Validar el diagnóstico.**
- **Elegir dentro del rango clínico cuando lo hay.** Fósforo 0,8 o 1,2 en
  IRIS 3 es **juicio clínico, no cálculo**, y por eso no lo puede decidir
  el motor ni un valor por defecto.
- **Levantar un bloqueo asumiendo la responsabilidad.** Hoy la hepatopatía
  **bloquea la generación entera** (`patologias_bloquean()`), porque el
  cobre que hace falta en la hepatopatía por acúmulo está por debajo del
  mínimo de FEDIAF. Un veterinario tiene que poder decir «formula con cobre
  ≤ 1,2, respondo yo».
- **Tener una lista de pacientes.**

### Lo que importa más que el reparto de permisos: el informe para la consulta

**La acción más valiosa del tutor en modo veterinario no es usar la app: es
llevarle a su veterinario un documento.**

Una página imprimible con:

- el diagnóstico,
- **los objetivos usados y de dónde salen**,
- los 30 requisitos verificados,
- la lista de la compra,
- y la curva de evolución.

Eso es lo que hace que un veterinario diga que sí a una dieta casera —algo
que por defecto le da pánico, **y con razón**: Larsen *et al.* (JAVMA,
2012) evaluaron 39 recetas caseras publicadas para perros con enfermedad
renal crónica y **ninguna** cumplía las recomendaciones del NRC
([PubMed 22332622](https://pubmed.ncbi.nlm.nih.gov/22332622/)). El miedo
del veterinario a la comida casera está justificado por los datos, así que
no se le quita convenciéndole: se le quita enseñándole los números.

**Y esto invierte el problema de captación.** No hay que reclutar
veterinarios: **los traen los tutores**. Uno a uno, con un caso concreto
delante, que es la única forma en que un veterinario prueba una
herramienta de verdad. Si el tutor llega a la consulta con eso, el
veterinario valida dentro de la app porque ya está el 90 % hecho.

Comparado con el importador de pacientes del apartado 9, esto vale
muchísimo más y cuesta menos.

### La pantalla de validación: qué firma exactamente

Va a doler si se hace mal, así que queda escrito:

**La pantalla en la que el veterinario valida tiene que enseñarle las
cifras concretas que está firmando.** Fósforo 800 mg/1000 kcal, proteína
35 g/1000 kcal, **y que las dos están por debajo del mínimo de FEDIAF, y
por qué**.

**Nunca «modo renal activado».** Si firma a ciegas es una trampa para él y
un problema para nosotros.

Y de paso es lo que hace el producto defendible: **el veterinario ve
exactamente lo mismo que el motor**. No un resumen, no una etiqueta: los
mismos números contra los que se va a verificar el menú.

---

## 3. Lo que no cambia, entre por donde entre

Las cinco reglas de `CLAUDE.md` siguen enteras, y una en concreto hay que
leerla dos veces antes de tocar nada de la fase 4:

- **Ningún menú sale sin verificar.** Todo pasa por
  `_garantizar_verificado()`, también los del veterinario. Un menú
  prescrito no es un menú sin comprobar: es un menú comprobado contra
  otra cosa, y esa otra cosa tiene que estar escrita.
- **Los cinco topes de seguridad crónica** — vitamina D, yodo, selenio,
  mercurio y tiaminasa — **no los levanta nadie**. Ni un veterinario, ni
  con firma. No son criterio nutricional discutible: son el margen entre
  una dieta y una intoxicación acumulada, y están puestos con su fuente
  al lado en `motor/seguridad.py`.
- **Las alergias y las exclusiones a mano no se tocan jamás.** Un vet
  puede añadirlas; quitarlas, no.
- **Lo que se relaja es la forma, nunca la nutrición.** La escalera de
  relajación suelta proporciones BARF, que son criterio nuestro. Sigue
  igual.

---

## 4. Por qué esto es un proyecto de app, y casi no de motor

El motor ya es profesional. `verificar()` devuelve hoy, para cada uno de
los 29 nutrientes: el valor del menú por 1000 kcal, el mínimo y el máximo
de FEDIAF para esa etapa, si cumple, los huecos de datos del catálogo
(`sin_dato`) y los valores que no nos creemos (`dato_dudoso`). Devuelve
el ratio Ca:P, el semáforo, los avisos de seguridad y los topes por
patología que se aplicaron.

**Nada de eso hay que calcularlo: hay que dejar de taparlo.** La versión
«para dueños» no es un motor más pequeño, es el frontend enseñando tres
cifras de las treinta. La versión profesional es la misma respuesta,
pintada entera.

Eso cambia el tamaño del proyecto: las fases 0 a 3 son casi todas
**Supabase y `canislab-web`**. De esta API hacen falta solo dos cosas
pequeñas, las dos de la fase 1: un `codigo` estable en cada aviso
(apartado 6) y que devuelva el sello de lo verificado (apartado 11).
Las que sí tocan el motor son **la congelación de lo firmado y la
prescripción**, y en ese orden — ver el final del apartado 11.

---

## 5. Fase 0 — el rol

Lo más pequeño que ya sirve para algo.

**Supabase**, tres columnas en `profiles`:

```sql
ALTER TABLE public.profiles
  ADD COLUMN IF NOT EXISTS rol TEXT NOT NULL DEFAULT 'tutor',
  ADD COLUMN IF NOT EXISTS num_colegiado TEXT,
  ADD COLUMN IF NOT EXISTS rol_verificado_en TIMESTAMPTZ;
```

`rol` es `'tutor'` o `'profesional'`. Y la regla que hace que signifique
algo: **el modo profesional se enciende solo si `rol = 'profesional'` Y
`rol_verificado_en` no está vacío.** Pedir el número de colegiado sin
mirarlo no acredita nada; lo que acredita es que alguien lo aprobó.

Quien se registra puede *pedir* el rol (deja su número); encenderlo es un
`UPDATE` a mano hasta que haya suficientes vets como para que compense
automatizarlo.

**Importante para la seguridad por fila**: `rol` no puede ser editable
por su propio dueño, o cualquiera se asciende con una llamada desde la
consola del navegador. La política de `UPDATE` sobre `profiles` tiene que
excluir esas tres columnas — igual que ya pasa con `plan`, que solo lo
escribe el webhook de Stripe con la clave secreta.

---

## 6. Fase 1 — el modo profesional: ver más, no poder más

Misma app, mismos límites, más números a la vista. Es la fase que más
valor da por lo poco que cuesta, porque el dato ya viaja.

Y desde que se decidió que la pauta sale firmada, **esta fase no es una
mejora: es requisito**. Quien firma tiene que poder ver lo que firma
(apartado 11).

Lo que se enseña de más:

- La tabla entera de los 29 nutrientes con valor, mínimo, máximo y
  margen. Hoy el dueño ve «cumple 30 de 30»; el profesional quiere ver
  cuál va justo.
- Los huecos del catálogo (`sin_dato`) y los `dato_dudoso` del menú, con
  su nombre. Un profesional tiene derecho a saber sobre qué datos se
  construyó lo que va a firmar.
- **Qué peldaño de la escalera de relajación se usó**, y poder elegirlo.
  Hoy se baja solo y se avisa; un profesional quiere decidir si prefiere
  otro reparto antes que soltar la proporción de hueso.
- El ratio Ca:P y los topes de patología aplicados, con su número.

Y una cosa que no es «enseñar más» y que es la que más trabajo lleva:

### Generar el menú: el modo manual es la puerta de entrada

Escrito el 28 de agosto, después de mirar cómo trabajan de verdad los
programas que ya usan los veterinarios (AnVet, MyVetDiet, Animal Diet
Formulator, Pet Diet Designer, BalanceIT).

**Cómo lo hacen todos, sin excepción**: el veterinario elige los alimentos
y **teclea los gramos a mano**, viendo columnas de nutrientes con el % del
requisito, y va corrigiendo por tanteo hasta que cuadran. Es una hoja de
cálculo con buena cara. La propia literatura lo dice sin adornos: llegar a
todos los niveles de todos los nutrientes es muy difícil, y hace falta
saber de nutrición clínica **y de hojas de cálculo**.

**Ninguno decide qué alimentos Y cuánto de cada uno a la vez.** Eso es lo
que hace el MILP de este repo, y es la única ventaja que no se copia
rápido.

**Pero eso no significa quitarles el tanteo.** La gente prefiere lo malo
conocido, y un profesional no va a confiar el primer día en una caja que
le escupe una dieta hecha. Así que el modo profesional tiene los dos, y en
este orden:

**1. Modo manual — lo malo conocido.** El vet elige alimentos y pone
gramos, y la ficha se recalcula delante de él. Es lo que ya sabe hacer, sin
aprender nada.

Y esto **ya está construido**: es `/analizar`, que recibe gramos por
alimento y devuelve la ficha entera contra FEDIAF, compartiendo `MAPA` con
el semáforo. Hoy se vende como «analiza la dieta que ya le das al perro»,
pero mecánicamente es un formulador manual. Lo que falta no es cálculo, es
pantalla: añadir y quitar alimentos y mover gramos viendo la ficha
moverse, en vez de un formulario de una sola tirada.

**2. El botón que convierte — «termínamelo».** El vet coloca lo que quiere
para ese paciente, se atasca (siempre se atascan: es la parte difícil), y
el motor **respeta lo que él puso y cierra el resto**. Ése es el momento en
el que descubre que el automático no es una caja negra que le quita el
criterio, sino que le ahorra el tanteo.

Es la misma palanca de **anclar y recalcular**, y por eso las dos cosas no
son dos productos: el manual es la puerta y el botón es la conversión.

**3. El automático de siempre**, para cuando ya se fía.

### El límite del modo manual, y por qué juega a favor

Un menú montado a mano que no cumpla **se puede ver en rojo**: eso ya lo
hace `/analizar` sin romper la regla 1, porque devuelve un análisis y no un
menú. Lo que no se puede es **entregarlo ni firmarlo como pauta**.

Su hoja de cálculo les deja imprimir con una columna en rojo. Ésta no. Para
alguien que va a firmar con su número de colegiado, eso no es una
limitación: es el motivo para usarla.

### «Cómo darlo» es pautable

Las instrucciones salen automáticas, como ahora, pero el veterinario puede
**cambiarlas para ese paciente**: un caso concreto puede necesitar otra
cosa. Se guarda con la pauta —y si está firmada, congelado con ella
(apartado 11)—, no como un texto global.

### Los textos hablan a la persona equivocada

Los avisos del motor están escritos para quien no es veterinario, a
propósito y bien. El problema es que **rematan en «coméntalo con tu
veterinario»** — `motor/verificar.py:449` y `:460`,
`motor/exclusiones.py:113`, los avisos de `PATOLOGIAS` en
`motor/motor_completo.py`. Dicho a un veterinario, eso no es un aviso:
es ruido, y de los que hacen que se deje de leer el resto.

**Cómo NO hacerlo**: duplicar cada texto en Python con una versión para
cada público. Son decenas de cadenas construidas con f-strings dentro de
la lógica; duplicarlas es garantizar que un día se corrija una y no la
otra, y nadie lo verá porque las dos son frases correctas.

**Cómo sí**: cada aviso lleva un `codigo` estable (`"calcio_al_maximo"`,
`"tiaminasa_10pct"`, `"renal_fosforo_al_minimo"`) junto al texto que ya
tiene. El motor sigue devolviendo su frase de siempre, que es la del
dueño, y el frontend en modo profesional decide si la sustituye por otra
o la enseña tal cual. **La cifra y la condición viven en un solo sitio
—el motor—; lo que cambia es a quién se le cuenta.** Añadir el código es
un cambio pequeño y mecánico en esta API, y es lo único que la fase 1
necesita de aquí.

---

## 7. El formulador del veterinario: su pantalla, no la nuestra con más botones

Dictado el 29 de agosto, y corrige algo que el resto del plan daba por
hecho. Hasta aquí decía «modo profesional = las mismas pantallas enseñando
más». Para el MENÚ eso no vale:

> «Ellos no tienen que tener automático / personalizar. Ellos tienen su
> propio modo de crear el menú, que es esta manera en la que ellos van
> poniendo alimentos, y según van seleccionando van viendo todos los
> nutrientes por categorías —proteínas, aminoácidos, vitaminas— **en tiempo
> real**, cuando vayan cambiando gramos.»

Eso no es una variante de «Personalizar»: es **otra pantalla**. Y es
exactamente cómo funcionan AnVet, MyVetDiet, Animal Diet Formulator y Pet
Diet Designer (apartado 6). La diferencia de Rawku no es quitarles esa
pantalla — es que **el botón de terminar existe**.

### Cómo es

Una tabla que se rellena a mano, con los nutrientes vivos al lado:

| | |
|---|---|
| **Los gramos los pone el veterinario** | No el motor. Escribe «pechuga de pavo 300 g» y ve qué pasa |
| **Los gramos TOTALES también** | Decide la ración completa, y el motor trabaja dentro de ella |
| **Los nutrientes, en vivo** | Agrupados: energía y macros, minerales, vitaminas, aminoácidos, ácidos grasos. Cada uno con su valor, su mínimo, su máximo y el margen |
| **Se recalcula a cada cambio** | Cambiar 300 por 280 mueve la tabla entera delante de sus ojos |
| **Excluir una categoría entera** | Además de alimentos sueltos. «Este perro no come hueso» es una frase, no una lista |
| **Autocompletar** | El botón. Ver abajo |

### El botón de autocompletar, que es la conversión

> «Que él tenga un botón que pueda pulsar y que se complete solo con lo que
> falta, y que luego también pueda modificar cosas de lo que le ha rellenado
> automáticamente.»

Ése es el momento en el que un veterinario deja de usar su hoja de cálculo.
Y lo que hace que funcione es que **lo autocompletado se pueda tocar
después**: si al pulsar el botón queda un menú intocable, no es una
herramienta, es una caja negra — y vuelve a AnVet.

Mecánicamente **ya existe**: es `forzar` en `resolver()`. Lo que el
veterinario ha escrito entra forzado y el motor cierra el resto. Lo que
falta es la pantalla, y **que lo autocompletado se distinga de lo suyo**
para poder editarlo sin miedo a deshacer su criterio.

### Lo que hay que decidir antes de construirlo

**¿Qué manda si los gramos totales que fija el veterinario no dan para
cumplir?** Es la pregunta de verdad y no tiene respuesta obvia:

- Cumplir los requisitos y **pasarse** de los gramos que pidió.
- Respetar los gramos y **entregar un menú que no cumple** — choca de
  frente con la regla 1: ningún menú sale sin verificar.
- O **decirlo y que elija**: «con 450 g no llegas al calcio; hacen falta
  520, o bajamos el objetivo de kcal».

La tercera es la única que no rompe nada, pero hay que diseñarla.

### La condición corporal: «rellenito» no es lenguaje de consulta

> «Cuando te pone la condición física, la forma del perro, no debería ser
> ideal / rellenito / muy gordito. Para un veterinario es mejor el BCS.»

Hoy la ficha usa cinco caritas con nombres de andar por casa. Están bien
para un dueño y **son ridículas en una consulta**. Un profesional trabaja
con el **BCS de 9 puntos** (WSAVA), que además es lo que aparece en la
historia clínica.

Y esto no es solo el rótulo: **de la condición sale el peso objetivo, y del
peso objetivo salen las kcal**. Si el vet marca «BCS 7/9» y el tutor ve
«rellenito», los dos tienen que estar mirando **el mismo número por
debajo**: la escala profesional y la de casa son la misma cosa con dos
nombres, no dos cálculos.

⚠️ Y ahí hay una trampa ya medida en este proyecto: el peso objetivo se
fija al marcar la condición y **no se recalcula al pesar al perro** — si se
recalculara, bajaría con él y la dieta no terminaría nunca (Lola: 7,0 kg →
263 kcal, 6,2 → 240). Lo que cambie en modo profesional tiene que
respetarlo.

---

## 8. El mapa de pantallas: qué ve cada uno

Escrito el 28 de agosto, al preguntarse en voz alta si «la app tendría que
ser totalmente distinta por dentro». La respuesta corta es que no —mismo
motor, mismas pantallas, mismos datos—, pero la pregunta destapó un hueco
de verdad: el plan decía «se ve más, no se puede más» y **no decía qué
pantallas**. Sin esto no se puede empezar la fase 1.

Las pantallas son las que hay hoy en `App.jsx`, no unas inventadas.

### Las que existen hoy

| Pantalla | Tutor | Veterinario | Qué cambia |
|---|---|---|---|
| **Onboarding**, 6 pasos (nombre y sexo · raza o tamaño · fecha de nacimiento · peso y condición · actividad y esterilización · alergias y patologías) | Sí | Sí, **pero es otro**: es dar de alta a un paciente, no a «tu perro». Mismos 6 datos, otro tono, y dos campos más: nombre y contacto del tutor | Ver abajo |
| **Generar el menú** | Automático o personalizar | **Tres, y en este orden**: manual (elige alimentos y pone gramos, como en AnVet), «termínamelo» (ancla lo suyo y el motor cierra el resto) y el automático | El manual y el botón son nuevos — ver el apartado 6 |
| Pestaña **«El menú»** | Sí | Sí | El vet ve además la tabla de los 29 nutrientes con margen, el Ca:P, los topes aplicados, los huecos y el peldaño de relajación usado |
| Pestaña **«Cómo darlo»** | Sí | Sí — es lo que le da al tutor, y **lo puede pautar**: cambiar el texto para ese paciente | Cambia de destinatario y se vuelve editable |
| **Mis menús** | Sí | Sí, del paciente que tenga abierto | Nada |
| **Perfil del perro** | Sí | Sí | Nada |
| **Evolución y crecimiento** | Sí (premium) | Sí — es seguimiento clínico, justo lo suyo | Nada |
| **Analizar la dieta actual** | Sí (premium) | Sí, y es de lo más útil que hay para una consulta | Nada |
| **La compra** (la cesta) | Sí | **No.** El vet no hace la compra de un perro que no es suyo | Se quita del menú lateral |
| **Transición** | Sí | La **pauta**, no la sigue | Se queda, cambia de destinatario |
| **Varios perros de una casa** | Sí | **No.** Un vet no tiene «una casa con cinco perros»: tiene pacientes, que es otra cosa | Lo sustituye la lista de pacientes |
| **Suscripción / premium** | Sí | No, mientras no se cobre | — |

### Las que sólo existen en modo veterinario

Éstas hay que construirlas: hoy no hay nada parecido.

| Pantalla | Para qué | Fase |
|---|---|---|
| **Lista de pacientes** | Su pantalla de entrada. Buscar, abrir, dar de alta. Es lo que en modo tutor es «la casa» | 2 |
| **Alta de paciente** | El onboarding, con los datos del tutor y sin el tono de «tu perro» | 2 |
| **Acreditación** | Donde pide el rol: su número de colegiado. En Ajustes | 0-1 |
| **Ficha clínica del menú** | Los 29 nutrientes, el Ca:P, los topes, los huecos. Puede ser una pestaña más junto a «El menú» y «Cómo darlo» | 1 |
| **Prescripción** | Fijar un tope o un mínimo para ese paciente | 4 |
| **Firmar la pauta** | El botón, la vista previa de lo que se firma, y el PDF | 4 |
| **Pautas firmadas del paciente** | El historial. Documentos, no un menú que se pisa | 4 |
| **Validación del diagnóstico** | Donde el vet ve **las cifras exactas** que va a firmar y las valida. Nunca «modo renal activado» (apartado 2) | 4 |

### Las que sólo existen en modo tutor

**La compra** y **la suscripción**. Nada más: todo lo demás o vale para los
dos, o cambia de destinatario sin desaparecer.

Y una que hay que construir, la más valiosa de todas y no está en ninguna
de las dos listas de arriba: **el informe para la consulta** (apartado 2).
Lo genera el tutor, sin veterinario y sin validar nada, y es lo que lleva
impreso a su cita. Es la pantalla que trae veterinarios.

Que la lista sea tan corta es la prueba de que esto es un modo y no dos
productos. Si hubiera doce pantallas exclusivas de cada lado, la decisión
del apartado 1 estaría mal tomada.

### El onboarding es el que más cambia, y hay que tener cuidado

Es la pantalla más delicada del cambio, por dos motivos que ya han hecho
daño en este proyecto:

1. **Son los datos de los que sale todo.** De la fecha de nacimiento sale
   la etapa, y de la etapa los 30 requisitos. El fallo de `guardarPerro`
   —siete campos leídos con nombres que no existían, guardados vacíos en
   silencio, un perro de diez años volviendo como cachorro— salió de tocar
   justo esto. Si el alta de paciente es un formulario nuevo, **es un
   segundo camino hacia la misma tabla**, y hay que probarlo con la misma
   vara: los campos van también a `ficha-ida-y-vuelta.spec.js` y a
   `sin-cuenta.spec.js`, y se comprueba lo GUARDADO, nunca la pantalla.
2. **Lo más barato es que sea el mismo formulario con otro tono**, no otro
   formulario. Dos formularios contra la misma tabla se separan solos, y
   cuando se separen no dará error: el menú saldrá verde igual.

### Las tres que faltaban, decididas el 28 de agosto

**1. El veterinario no ve «La compra».** No hace la compra de un perro que
no es suyo. Sale del menú lateral en modo profesional y ya está.

**2. Hay un interruptor de modo, y el veterinario con perro tiene la app
entera.** Una cuenta, un login, dos modos: en modo tutor es un usuario
normal con su perro, su cesta y su suscripción; en modo profesional ve a
sus pacientes. El interruptor cambia la VISTA, nunca la cuenta.

Y esto destapa algo que no estaba previsto y que hay que resolver en la
fase 2, no después: **el perro del veterinario no puede salir en su lista
de pacientes**, ni un paciente en su lista de perros. Los dos tienen
`perros.user_id` = él, así que la columna no los distingue.

Lo distingue la tabla `accesos` del apartado 9, sin añadir nada:

- **Un paciente tiene fila en `accesos`** (`origen` =
  `'creado_por_el_profesional'`).
- **Su perro no tiene ninguna.**

O sea que la lista de pacientes son los perros CON fila y la de perros
propios los que no la tienen. Ésta es la razón de más peso para crear
`accesos` ya en la fase 2 aunque para los pacientes propios parezca
redundante: sin ella, el interruptor de modo no tiene con qué separar las
dos listas, y lo que sale es el perro del veterinario metido entre sus
pacientes.

**3. El premium viaja con el perro, no con la persona.** Si un tutor con
premium le comparte su perro (fase 3), el veterinario ve las pantallas de
pago **de ese perro** — las paga su tutor y es suyo. Y no se extiende: sus
otros pacientes siguen como estén.

Lo que eso cambia en el código es una pregunta. Hoy `esPremium(userId)`
pregunta por la PERSONA, y la lista del menú lateral de `App.jsx` marca dos
entradas con `isPremium: true` («Evolución y crecimiento» y «Analizar la
dieta actual»). Pasa a preguntarse **por el perro**: ¿está cubierto este
perro, por quien sea? Es un cambio pequeño y además es mejor así — hoy, un
tutor premium que deja de pagar pierde el acceso a los perros de una casa
que quizá pagaba otro.

**Cuidado con el orden**: hasta que exista la fase 3 no hay ningún perro
compartido, así que «cubierto por su tutor» y «cubierto por su dueño» son
lo mismo. La pregunta hay que cambiarla igualmente **en la fase 3**, no
antes ni después: antes es cambiar algo que funciona sin ningún caso que lo
necesite, y después es descubrir que el vet ve borrosa la pantalla de un
perro que está pagado.

## 9. Fases 2 y 3 — los pacientes

Se decidió hacer las dos formas en dos fases. Que se pueda es cuestión de
diseñar la tabla ahora, no después.

### La tabla que hace que las dos quepan

`perros.user_id` sigue significando lo mismo que hoy: **de quién es la
ficha**. Para un paciente que crea el vet, es el vet. Nada de lo que ya
funciona se entera de este cambio, y esa es la gracia.

Encima, una tabla que responde a una sola pregunta — *¿puede esta cuenta
ver este perro?*:

```sql
CREATE TABLE public.accesos (
  id           uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  perro_id     uuid NOT NULL REFERENCES public.perros(id) ON DELETE CASCADE,
  profesional  uuid NOT NULL REFERENCES auth.users(id),
  origen       TEXT NOT NULL,   -- 'creado_por_el_profesional' | 'invitado_por_el_tutor'
  estado       TEXT NOT NULL DEFAULT 'activo',   -- 'activo' | 'revocado'
  creado_en    timestamptz NOT NULL DEFAULT now(),
  revocado_en  timestamptz,
  UNIQUE (perro_id, profesional)
);
```

**En la fase 2** el vet crea la ficha y se le pone una fila con
`origen = 'creado_por_el_profesional'`. Parece redundante —es su propio
perro, `user_id` ya lo dice— y hace dos cosas que no se ven a primera
vista. Una: que la fase 3 sea añadir filas en vez de reescribir el acceso,
**un solo camino para «¿puede verlo?» desde el primer día**. Y dos, que es
la que obliga: **es lo único que separa a un paciente del perro del propio
veterinario**. Los dos tienen `user_id` = él; lo que los distingue es que
el paciente tiene fila aquí y su perro no. Sin eso, el interruptor de modo
del apartado 8 le mete su perro entre los pacientes.

**En la fase 3** el dueño invita por correo y, al aceptarse, entra una
fila con `origen = 'invitado_por_el_tutor'`. Nada más cambia.

Las políticas de `perros` y `menus` pasan a ser, en lectura:

```sql
user_id = auth.uid()
OR EXISTS (SELECT 1 FROM public.accesos a
           WHERE a.perro_id = perros.id
             AND a.profesional = auth.uid()
             AND a.estado = 'activo')
```

Se revoca poniendo `estado = 'revocado'`, no borrando la fila: quién tuvo
acceso y hasta cuándo es exactamente el dato que hará falta el día que
alguien pregunte. Y **el dueño tiene que poder revocar en un toque, y
verlo**: un acceso concedido que no se ve ni se puede quitar es un acceso
que nadie recuerda haber dado.

### Quién generó cada menú

Una columna más, `menus.creado_por uuid`, y se rellena siempre con
`auth.uid()`. Es lo que la suplantación habría hecho imposible: sin ella,
un menú del vet y uno que el dueño se hizo un domingo son la misma fila.

### Lo que el vet ve de un paciente

Los datos del perro que afectan a la comida, que son los que ya hay. **No
la cuenta del dueño**: ni su correo, ni sus otros perros, ni su
facturación. El acceso es a un perro, nunca a una persona.

---

## 10. Fase 4 — la prescripción, que es la difícil

Esta es la que justifica el proyecto entero, y la que puede romper lo que
protege la regla 1.

### El problema, hoy

Una dieta renal terapéutica de verdad baja el fósforo **por debajo del
mínimo que FEDIAF exige a un perro sano**. Y una hepatopatía por acúmulo
de cobre necesita 1,2 mg/1000 kcal cuando el mínimo de FEDIAF es 2,08.
Como el motor no puede bajar de ahí, hoy pasa esto:

- **renal** se queda en 1200 mg de fósforo, que es lo más apretado
  posible sin romper el mínimo, con un aviso que dice honestamente que
  eso *no* es una dieta renal prescrita.
- **hepatopatía bloquea** desde el 25 de agosto: no da menú.

Las dos cosas son correctas **para un dueño**. Un veterinario colegiado
es precisamente la persona que sí puede pautar por debajo de FEDIAF, y si
la app no se lo deja, lo hará en una hoja de cálculo.

### La forma que respeta la regla 1

La regla no dice «todo menú cumple FEDIAF». Dice **ningún menú sale sin
verificar**. Se mantiene entera así:

Un menú prescrito se verifica **de cero y entero**, igual que cualquier
otro, contra un **juego de requisitos declarado**. Lo que cambia no es si
se comprueba: es contra qué. Y ese «contra qué» viaja con el menú, se
enseña en pantalla y se guarda con él.

Una prescripción es un objeto pequeño y explícito:

```
prescripcion = {
  "fosforo": {"min": 900, "max": 900},
  "motivo": "ERC estadio 3",
  "firmada_por": "<uuid del profesional>",
  "colegiado": "...",
  "fecha": "2026-09-01"
}
```

Y hay **una sola función** que resuelve los requisitos de un paciente:

```
requisitos_del_paciente(etapa, patologias, prescripcion)
    -> (minimos, maximos, topes, excepciones)
```

Esto no es preferencia de estilo. En este repo ya ha pasado dos veces que
dos sitios leyeran la misma tabla por su cuenta y dijeran cosas distintas
— el analizador y el semáforo con la fibra, y la tabla de patologías
duplicada del motor anterior al MILP, con el fósforo renal a 1400 en un
lado y a 1200 en el otro. **El solver, `_tope_patologia_roto()` y
`_garantizar_verificado()` tienen que llamar los tres a esta función**, o
el menú se construirá contra unos números y se comprobará contra otros.

Reglas de lo que una prescripción puede hacer:

- **Puede bajar un mínimo de FEDIAF** para un nutriente nombrado.
- **Puede apretar un máximo** por debajo del tope de patología.
- **No puede aflojar ningún máximo** por encima de FEDIAF.
- **No puede tocar los cinco topes de seguridad crónica.** Ni uno.
- El semáforo de un menú prescrito **nunca dice «verde» a secas**: dice
  *verde con excepciones*, y las lista. Un verde limpio significa «cumple
  los requisitos de un perro sano», y esto no lo cumple a propósito.

### El agujero que hay que tapar antes: la API no tiene puerta

**Hoy esta API no autentica nada.** `CORS` está en `*`, no hay ningún
`Depends`, ningún token, ninguna cabecera. Cualquiera puede llamar a
`/menu/v2` desde una terminal. El premium tampoco se comprueba aquí: lo
tapa el frontend con `PremiumGate`, que es un `blur` de CSS.

Para las fases 0 a 3 eso da igual —el acceso a los datos lo protege la
seguridad por fila de Supabase, no la API—. **Para la fase 4 no**: «solo
un veterinario acreditado puede prescribir» comprobado en el frontend no
es una regla, es una sugerencia. Cualquiera podría mandar una
`prescripcion` con el fósforo a 300 y la API la aplicaría.

Así que la fase 4 empieza por lo aburrido: **la API tiene que validar el
JWT de Supabase** y mirar ella misma que `rol = 'profesional'` y
`rol_verificado_en` no está vacío, antes de aceptar una prescripción. No
hace falta autenticar todos los endpoints —los demás no dan acceso a
datos de nadie—, solo el camino que levanta un mínimo. Pero sin eso, la
fase 4 no se despliega.

---

## 11. La firma

Decidido el 28 de agosto: **la pauta sale firmada, con el nombre del
veterinario y su número de colegiado.**

Es la decisión que más obliga de todas, y no por lo que hay que pintar en
el PDF —eso son dos líneas—, sino por lo que un documento firmado tiene
que poder hacer un año después. Todo lo de este apartado sale de ahí.

### Lo que se firma es un documento, no «el menú»

Hoy la tabla `menus` guarda nombre, gramos y kcal. Nada más. Eso ya está
señalado en `/perro/{perro_id}/menus`, en `main.py`: **un menú guardado no
se puede verificar, ni siquiera en principio, porque falta contra qué**
—no está la etapa, ni el DER, ni las patologías con las que se calculó—.
Por eso ese endpoint marca lo que devuelve como `verificado: False`.

Firmar eso no se puede. Un documento firmado tiene que seguir diciendo lo
mismo dentro de un año, y hoy nada de esto se queda quieto:

- **La ficha del perro cambia.** Caso real de este repo, el del peso
  objetivo: Lola pesaba 7,0 kg y luego 6,2. Si el vet firmó a 7,0, el
  documento firmado dice 7,0 para siempre — aunque la ficha ya diga otra
  cosa.
- **El catálogo cambia.** También ha pasado, dos veces en una semana:
  fuera la borraja el 27 de agosto, fuera cinco suplementos el 26. Un menú
  firmado que llevara borraja no se puede regenerar hoy: saldría otro.
- **El motor cambia.** El tope de fósforo en renal pasó de 1400 a 1200 el
  25 de agosto. El mismo menú, verificado antes y después, no da lo mismo.

Así que **firmar obliga a congelar**. Al firmar se guarda una copia
completa e inmutable de lo que se firmó:

```
pautas_firmadas
  id                 uuid
  perro_id           uuid
  profesional        uuid          -- quién firma
  nombre_firmante    text          -- copiados AQUÍ, no leídos de profiles:
  num_colegiado      text          -- si mañana cambia su ficha, lo firmado no cambia
  firmada_en         timestamptz
  menu               jsonb         -- los gramos
  ficha_verificada   jsonb         -- la respuesta ENTERA de verificar(): los 29
                                   -- nutrientes con su valor, mínimo, máximo y
                                   -- margen, el Ca:P, el semáforo, los avisos
  contexto           jsonb         -- etapa, DER, peso, patologías, prescripción,
                                   -- peldaño de relajación usado, exclusiones
  huecos             jsonb         -- sin_dato y dato_dudoso de este menú
  sellos             jsonb         -- el del catálogo, el de la tabla FEDIAF y el
                                   -- de main.py con los que se calculó
  sello              text          -- ver abajo
```

Lo de copiar el nombre y el número en vez de apuntar a `profiles` no es
redundancia: es que un documento firmado no puede cambiar porque su autor
edite su perfil.

Y los tres sellos son los que ya existen: `/verificar` sella hoy
`alimentos_v3_final.json`, `requerimientos_v2_final.json` y `main.py`.
Guardarlos con la pauta es lo que permite responder «¿con qué datos se
calculó esto?» sin adivinar.

### El sello lo calcula la API, no el frontend

Un sello sobre lo firmado —SHA-256 de la copia canónica, truncado a 16
hex, **igual que el de `/verificar`**— para poder comprobar que el PDF que
alguien enseña es el que se firmó.

**Lo calcula la API, sobre lo que acaba de verificar**, y lo devuelve con
el menú. No el frontend sobre lo que pintó en pantalla. Si lo calculara el
frontend, habría dos ideas de «lo firmado» —la del motor y la de la
pantalla— y el día que se separen, el sello seguirá cuadrando consigo
mismo y no dirá nada. Es la misma familia de fallo que la duplicación del
DER que ya vigila `der_casos.json`.

### Firmar es un acto: hay que pulsar

El modo profesional **no firma solo**. Si firmara por el hecho de estar
encendido, el vet acabaría con veinte pautas firmadas de las que hizo
probando. Hasta que se pulsa «Firmar la pauta» es un borrador, y se ve que
lo es.

### No se firma a ciegas

Dos cosas que dejan de ser opcionales en cuanto hay firma:

- **La fase 1 pasa a ser requisito, no mejora.** Un profesional que firma
  responde de lo que firma, así que tiene que poder ver los 29 nutrientes
  con su margen antes de pulsar. Firmar una pantalla que dice «cumple 30
  de 30» y nada más es firmar a ciegas.
- **Los huecos van en el documento**, no solo en pantalla. Si el menú se
  calculó con alimentos a los que les falta un dato (`sin_dato`) o con
  alguno de los valores que no nos creemos (`dato_dudoso`), eso sale
  impreso en la pauta firmada. Es incómodo y es exactamente por eso: lo
  contrario es firmar sobre datos incompletos sin que conste en ninguna
  parte.

### Una pauta firmada no se edita

Se firma otra. La anterior queda, con su fecha. El historial de pautas de
un paciente es una lista de documentos, no un documento que se va
pisando — que es, además, la única forma de poder mirar atrás y ver qué se
le pautó y cuándo.

Por lo mismo, **revocar el acceso no borra lo firmado**: si el dueño
quita el acceso al veterinario, el vet deja de ver al perro, pero las
pautas que firmó siguen existiendo para los dos. Un documento firmado no
se puede hacer desaparecer retirando un permiso.

### Esto reordena el plan

Congelar el menú entero con su contexto hace falta **para la firma y para
la prescripción de la fase 4** — una prescripción hay que guardarla con el
menú o no se puede defender tampoco. Es el mismo trabajo, se hace una vez,
y va **antes** que las dos.

### Lo que sigue sin ser mío

Un veterinario colegiado que firma una pauta calculada por un software
responde de ella. Qué dice exactamente el documento sobre qué firma —si
firma la pauta, si firma haberla revisado, qué papel tiene Rawku en
medio— es una cuestión de responsabilidad profesional, y hay que
preguntarla **antes** de que salga la primera pauta firmada de verdad.

**Dónde se pregunta**: en el **Colegio Oficial de Veterinarios** — el
colegio profesional de la provincia. En España un veterinario tiene que
estar colegiado, y el colegio es quien contesta de qué responde un
colegiado al firmar una pauta calculada por un software, y qué tiene que
decir el documento.

**Quién pregunta**: un veterinario, no nosotros. No se puede consultar a
un colegio sin ser colegiado. Aquí ese papel lo hace **Michelle**, que ya
es el criterio clínico del proyecto (ver las preguntas que tiene
pendientes en `PENDIENTE.md`) y que además será quien firme la primera
pauta. Va como una pregunta más de esa lista.

Lo de arriba se puede construir igual mientras tanto: no cambia según lo
que diga ese texto, solo cambia el texto.

## 12. Cómo se prueba

`pruebas_completas.py` entero, como siempre. Y bloques nuevos, cada uno
comprobado rompiéndolo:

- Una prescripción **no puede** aflojar ninguno de los cinco topes de
  seguridad crónica. Se intenta, y no se aplica.
- Una prescripción **no puede** subir un máximo por encima de FEDIAF.
- Un menú prescrito **sigue pasando** `_garantizar_verificado()` contra
  su juego declarado, y su semáforo **no** sale «verde» a secas.
- El solver y `_tope_patologia_roto()` resuelven los mismos números para
  el mismo paciente: se comparan las dos salidas de
  `requisitos_del_paciente()`. Es el bloque que evita que se repita lo de
  la fibra.
- Sin `rol = 'profesional'` verificado, una `prescripcion` se rechaza con
  401, no se ignora en silencio. **Ignorarla en silencio sería peor que
  aplicarla**: el vet vería un menú que cree prescrito y no lo es.
- El sello de una pauta firmada **cambia** si se le toca un solo gramo, y
  **no cambia** si se guarda el mismo contenido con otro formato. Es la
  misma comprobación que ya hay para los sellos de los JSON en
  `/verificar`, y por el mismo motivo: un sello que salta por el formato
  se acaba ignorando, y entonces no vigila nada.
- Una pauta firmada **sigue diciendo lo mismo** después de cambiar la
  ficha del perro y después de tocar el catálogo. Es la prueba que
  justifica la tabla entera: si se cae, es que algo se está leyendo en
  vivo en vez de la copia congelada.
- Firmar **guarda el nombre y el número de colegiado**, y cambiar después
  el perfil del veterinario no altera lo ya firmado.

Y tres que vigilan el principio del apartado 2, que es el que más fácil se
rompe sin querer, porque se rompe **quitando** cosas:

- **Sin diagnóstico validado, la app hace todo lo que hace hoy.** Un tutor
  sin veterinario genera su menú, ve los 30 requisitos, mete seguimiento y
  exporta, igual que antes de que existiera nada de esto. Si esta prueba
  cae, el modo veterinario se ha convertido en una degradación y no se
  entrega.
- **El tutor puede retirar el acceso del veterinario y apagar el modo
  terapéutico**, y después sigue viendo su perro, su menú y su histórico.
  Nadie se queda encerrado fuera de su propia cuenta.
- **La pantalla de validación enseña las cifras**, no una etiqueta: el
  valor, el mínimo de FEDIAF y la diferencia, para cada nutriente que la
  prescripción baja. Se comprueba rompiéndola: si se sustituye por un
  «modo renal activado», la prueba tiene que caer.

En `canislab-web`, y esto no es opcional (ver «Fallos que no puede
encontrar la usuaria» en `CLAUDE.md`): los campos nuevos de la ficha van
**también** a `tests/ficha-ida-y-vuelta.spec.js` y a
`tests/sin-cuenta.spec.js`. Si no, se pierden al guardar o al pasar de
sin cuenta a con cuenta, y en silencio.

---

## 13. Lo que sigue abierto — y no lo decide un programador

- **Qué dice el documento sobre qué se firma exactamente** — ver el final
  del apartado 11. Es lo único que queda de la firma que no se resuelve
  escribiendo código, y conviene preguntarlo antes de la primera pauta de
  verdad. Lo demás ya está decidido: se firma, con nombre y número de
  colegiado.
- **El precio**, cuando haya vets usándolo.
- **Los menús NO firmados, si el dueño revoca el acceso.** Los firmados ya
  está decidido: quedan (apartado 11). Los borradores que el vet generó y
  no llegó a firmar, no — ¿desaparecen de su lista o los conserva?
- **Cachorro renal, gestante con pancreatitis**: hoy se bloquean porque
  el mínimo para crecer choca con el tope terapéutico. Con prescripción
  eso deja de ser un muro, y hay que decidir si se abre — es exactamente
  el caso donde más falta hace un profesional y donde más daño hace un
  número mal puesto.
