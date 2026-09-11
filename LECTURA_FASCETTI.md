# Fascetti & Delaney, «Applied Veterinary Clinical Nutrition», 2ª ed — leído

**Qué es esto.** El registro de la lectura íntegra de Fascetti, capítulo a
capítulo. Sus hermanos son `LECTURA_SACN5_INTEGRA.md` y `LECTURA_NRC2006.md`.
El contador de frases es `leer_fascetti.py` + `lecturas_fascetti.json`.

**Por qué existe.** Fascetti estaba **extraído y no leído**. Sus 21 capítulos
llevaban semanas en el repo de fuentes, el motor le cita cuatro veces —el 1,1 %
de calcio del cachorro de raza grande sale de su capítulo 10— y **no había
ningún sitio donde comprobar que se hubiera leído**. Exactamente el agujero que
tenían FEDIAF antes del 9 de septiembre y SACN5 antes del 10.

Elena, 11 de septiembre de 2026: «termina de leer todas las fuentes, y por leer
me refiero a todos los pasos que tienes de verificar las tablas, verificar los
párrafos que no se mezclen, leer toda la información y sacar toda la información
bien, y apuntar y aplicar todo lo necesario».

**El texto está limpio.** 0 de 5.675 líneas largas con las dos columnas pegadas,
medido por el BLOQUE 81. No tiene el problema que tenían SACN5 y FEDIAF.

**Método.** Se apunta todo y no se aplica nada hasta el final, con los números
delante. Las decisiones clínicas las toma Elena.

---

### cap.1 — Integration of Nutrition into Clinical Practice (52 líneas, LEÍDO ENTERO)

Capítulo de método: la valoración nutricional como quinta constante vital y cómo
encaja en la consulta. No trae cifras de requisito.

### cap.2 — Basic Nutrition Overview (320 líneas, LEÍDO ENTERO)

Tres cosas que cruzan con el motor:

1. **Los factores de Atwater, y de dónde sale cada uno.** Literal: «For pet
   foods, the energy conversion factors that are used are referred to as
   modified Atwater factors: 3.5, 8.5, and 3.5 kcal/g for protein, fat and
   carbohydrate, respectively. These values are slightly lower than those used
   for human foods (i.e. 4 kcal/g for protein, 9 kcal/g for fat, and 4 kcal/g
   for carbohydrate) due to the typically lower digestibility of pet food
   (assumed average apparent digestibility for protein is 80%, 90% for fat, and
   84% for carbohydrate)».
   ⚠️ **Toca de lleno la duda del hueso.** El catálogo usa 4/9/4, los humanos, y
   la diferencia entre una serie y otra **es exactamente la digestibilidad**. O
   sea que la pregunta abierta —si la proteína del hueso se digiere como la de
   la carne— es la misma pregunta que decide qué factor toca.

2. **La cisteína ahorra metionina y la tirosina ahorra fenilalanina.** Literal:
   «directly including cysteine in the diet decreases by up to 50% the amount of
   methionine needed in the diets of both dogs and cats». El motor ya suma
   `metionina_cistina` y `fenilalanina_tirosina` como pares, que es la forma
   correcta. Confirmación, no cambio.

3. **La D-lisina no sirve y la D-metionina sí, hasta la mitad.** Literal:
   «D‐lysine cannot be used by dogs and cats the way L‐lysine can be. However,
   D‐methionine can be used to meet up to 50% of the methionine requirement».
   Importa para la ficha de L-metionina que falta en el catálogo
   (`REVISION_NUTRICIONISTA.md`): si algún día entra, la forma química decide.

### cap.3 — Determining Energy Requirements (466 líneas, LEÍDO ENTERO)

1. **Atwater clásico (4/9/4) vale para comida muy digestible.** Literal: «The
   Atwater equation was developed over 100 years ago to predict the energy
   content of human diets (Atwater 1902). It is still used in human nutrition,
   and it provides a reasonable estimate for the ME value of human foods fed to
   dogs (and possibly cats). The Atwater equation may also be appropriate for
   highly digestible commercial pet foods». Y más abajo: «the Atwater equation
   may be more appropriate for diets with high energy values and high
   digestibility».
   ⚠️ **Esto respalda al catálogo**: una ración de carne fresca cruda es comida
   muy digestible, y ahí el 4/9/4 es el factor que la fuente recomienda. La duda
   del hueso sigue siendo la duda del hueso, no del resto de la ración.

2. **La ecuación de energía de NRC para el perro, entera y con su fibra.**
   Literal: «Step 1: GE (kcal) = (5.7 × g protein) + (9.4 × g fat) + [4.1 × (g
   nitrogen‐free extract + g fiber)] Step 2: % energy digestibility = 91.2 –
   (1.43 × % crude fiber in dry matter) Step 3: DE (kcal) = GE × (% energy
   digestibility/100) Step 4: ME (kcal) = DE – (1.04 × g protein)».
   Es la que FEDIAF manda usar en Europa y la que ya está apuntada por quedarse
   corta con fibra por encima del 8 % de materia seca. Aquí está completa, y se
   puede **rehacer sobre una ficha de hueso** para contrastar con el 4/9/4.

3. **Las cifras de digestibilidad que hay detrás.** GE de referencia: 9,4 grasa,
   5,65 proteína, 4,15 hidratos. Digestibilidad: 0,90 grasa, 0,80 proteína, 0,85
   hidratos, **0 fibra bruta**. Y la corrección urinaria de la proteína, 1,25
   kcal/g en perro. De ahí salen los 3,5 y 8,5 del pienso.

4. **Ceniza estimada**: 2,5 % en húmedo y 8 % en seco. Útil para la cuenta de la
   materia seca mientras no haya humedad en las fichas.

### cap.4 — Nutritional and Energy Requirements for Performance (157 líneas, LEÍDO ENTERO)

El capítulo del perro de trabajo, y es el que más toca al motor de los cuatro.

1. ⚠️ **SEGUNDA FUENTE PARA APRETAR LOS OLIGOELEMENTOS EN EL PERRO DE TRABAJO.**
   NRC 2006 dice que los topes de seguridad se parten por la mitad; Fascetti lo
   dice con palabras y por el mismo motivo. Literal: «there is a potential for
   excess intake of calcium and trace minerals by dogs that take in large amounts
   of food because of their very high energy requirements. The amount of trace
   minerals in the diet of dogs undertaking large amounts of exercise should be
   kept close to the minimum requirement and should probably not be increased as
   the amount of fat is increased in the diet, but this is an unstudied area in
   dogs».
   Dos fuentes independientes, misma conclusión, y el motor ya tiene el
   disparador (actividad alta). Sigue sin aplicarse: ver `PENDIENTE_NUTRICION.md`.

2. **Tabla 4.2, y sus cifras ya vienen en las unidades del motor** (g/Mcal es
   g/1000 kcal). Perro de resistencia: proteína 90, grasa 59, hidratos 0, sodio
   1 g, potasio 1 g, calcio 3 g, fósforo 3 g. Perro de velocidad: proteína 60,
   grasa 36, hidratos 105.
   ⚠️ **Y el fósforo choca con lo que aplicamos.** 3 g/1000 kcal son 3000 mg, y
   el techo del libro para el adulto sano que el motor aplica son **2000**. O sea
   que a un perro de trabajo le estamos poniendo un techo un 33 % por debajo de
   lo que su propia fuente llama ingesta adecuada. El motor no distingue: aplica
   el techo del perro sano a cualquier adulto.

3. **Tercera fuente para la vitamina E que sube con los PUFA.** Literal:
   «Requirements for antioxidant vitamins also increase with the amount of
   dietary fat and with the amount of polyunsaturated fatty acids in all diets».
   Sigue sin cifra para el perro, igual que en FEDIAF y en NRC.

4. **Segunda fuente para la B6 que sube con la proteína**: «requirements for
   vitamin B6 (pyridoxine) tend to vary with protein intake». Tampoco da número.

5. **Nada de bebidas isotónicas**: «Commercial sports drinks sold for human
   athletes should not be offered to exercising dogs». Es material de aviso.

6. **El agua sí escala**: de 0,5 ml/kcal en frío a 0,6-1,2 a temperatura normal y
   1,8 en el perro obeso, y hay que ofrecer el doble de la media.
