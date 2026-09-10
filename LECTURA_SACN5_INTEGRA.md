# SACN5, LEÍDO ENTERO — capítulo a capítulo

**Qué es esto.** El registro de la relectura íntegra de *Small Animal Clinical
Nutrition, 5ª edición*: cada capítulo de la primera línea a la última, y lo que
sale de cada uno. Su hermano `LECTURA_SACN5.md` registra la lectura anterior, la
de las tablas; `sacn5_tablas.json` es el inventario de las 474 tablas y
`lecturas_sacn5.json` el contador de las frases.

**Por qué existe, y por qué no bastaba con lo que ya había.** El 10 de septiembre
de 2026, viendo cómo se estaban resolviendo los elementos capítulo a capítulo,
Elena escribió:

> «por favor no puedes leer todo sin hacer cossd raras de seleccionar frases y
> cosas asi? simplemente leer como si fueses un opositoe estudiando»

Y el fallo era mío y de bulto: **el filtro nutricional de `leer_sacn5.py` es para
CONTAR y lo estaba usando para DECIDIR QUÉ LEO.** Un elemento resuelto significa
«esta frase la he mirado», no «este capítulo lo he leído». Y como el filtro
descarta **33.207 de las 36.206 frases del libro**, resolver los 2.999 elementos
enteros habría dejado **el 92 % del texto sin abrir** — con el contador en verde y
diciendo «SACN5 leído».

Se comprobó en el sitio: al releer entero el cap.36 aparecieron los estadios
ACC/AHA y la frase «from Class I to Class III or IV following a salty meal», y el
filtro no había sacado ninguna de las dos.

**Cómo se comprueba que esto es verdad.** Cada capítulo leído entero deja su
`lectura_integra` en `lecturas_sacn5.json` con **el número de líneas de su `.txt`**,
y `leer_sacn5.py` lo rehace contra el fichero: si el texto se vuelve a extraer y
cambia de tamaño, la declaración queda vieja y la batería falla — que es lo
correcto, porque lo que se leyó ya no es lo que hay. El recuento de capítulos
leídos enteros se compara **exacto** en el BLOQUE 81, igual que el de frases
pendientes: sube solo cuando alguien lee un capítulo y lo sube en el mismo commit.

**Qué NO es esto.** No es una lista de cambios al motor. Aquí se apunta todo y no
se aplica nada — es el método que se fijó el 10 de septiembre después de que leer
un párrafo, aplicarlo y descubrir en el siguiente que estaba mal pasara dos veces.
Lo que haya que aplicar se decide al final, con los números delante, y las
decisiones clínicas las toma Elena.

---
### cap.1 — Small Animal Clinical Nutrition: An Iterative Process (1.881 lineas, LEIDO ENTERO)

Capitulo de metodo, no de cifras de requisito. Pero trae CUATRO cosas que el motor
usa y que hay que cruzar:

1. **La densidad de referencia del perro es 3,5 kcal EM/g de MATERIA SECA, no 4,0.**
   Cita literal (Box 1-2): «recommended nutrient values for canine and feline foods
   are based on an energy density of 3.5 and 4.0 kcal ME/g (14.64 and 16.74 kJ ME/g)
   of food dry matter, respectively». El 4,0 es el del GATO. Y el libro insiste en
   que comparar sin igualar densidades no vale: Table 6 del mismo Box es «How to
   convert to the same energy density», con el multiplicador
   `densidad_del_alimento / densidad_del_requisito`.
   ⚠️ HAY QUE CRUZARLO con la densidad que usa `auditar_conversiones.py` para pasar
   de % MS a por 1000 kcal, y con `_KCAL_POR_KG_MS_69` de la bateria.

2. **Los multiplicadores del DER del perro** (Box 1-6, Tabla 1), literal:
   RER = 70(BWkg)^0.75, o 30(BWkg)+70 «if the animal weighs between 2 and 45 kg».
   Mantenimiento 1,0-1,8 x RER · castrado 1,6 · entero 1,8 · inactivo/propenso 1,2-1,4 ·
   perdida de peso 1,0 · cuidados criticos 1,0 · ganancia 1,2-1,8 al peso ideal.
   Trabajo: ligero 1,6-2,0 · moderado 2,0-5,0 · duro 5,0-11,0.
   Gestacion: «First 42 days: feed as an intact adult. Last 21 days: use 3 x RER.»
   Lactacion 4-8 x RER, con tabla por numero de cachorros (1 → 3,0 · 2 → 3,5 ·
   3-4 → 4,0 · 5-6 → 5,0 · 7-8 → 5,5 · 9 → ≥6,0).
   Crecimiento: «3 x RER from weaning until four months of age. At four months of age
   energy intake should be reduced to 2 x RER until the puppy reaches adult size.»
   ⚠️ HAY QUE CRUZARLO con `der.py` y con `src/der.js` de canislab-web.

3. **El techo de calcio del cachorro grande lleva una condicion de densidad que no
   teniamos apuntada.** Caso 1-1, literal: «Calcium levels in foods intended for large-
   and giant-breed growth should not exceed 1.2% DM in foods that provide <3.8 kcal
   ME/g (<15.90 kJ) (Chapter 33)». O sea: el 1,2 % MS es a densidad <3,8, y el propio
   caso lo reescala a 1,32 % para un alimento de 4 kcal/g. Nosotros aplicamos 2750 mg
   /1000 kcal por el 1,1 % de Fascetti cap.10.

4. **Los valores «Atwater modificados» que usa el libro**: proteina 3,5 · grasa 8,5 ·
   hidratos digestibles 3,5 kcal EM/g, para perro y gato (Box 1-6, Tabla 2). Los
   generales, cuando se conoce la digestibilidad, son 4,4 · 9,4 · 4,15 x digestibilidad.

5. **La transicion de dieta** (Tabla 1-1): corta 7 dias (75/50/25/0 en cuatro tramos),
   larga 10 dias en perro y 4 semanas en gato. Cruzar con `transicion.py`.

### cap.2 — Evidence-Based Clinical Nutrition (603 lineas, LEIDO ENTERO)

NADA QUE APLICAR: capitulo de metodo. Ni una cifra de nutriente.
Lo unico reutilizable es la **Tabla 2-1, los cuatro grados de evidencia** que el
propio libro se aplica: 1 = ensayo clinico aleatorizado y controlado en la especie
diana con enfermedad natural · 2 = igual pero en laboratorio · 3 = sin
aleatorizacion, cohortes, casos-control, series de casos, modelos · 4 = opinion de
experto, libros de texto, estudios en otras especies, justificacion fisiopatologica.
Util para `PARA_EL_NUTRICIONISTA.md`: cuando una cifra nuestra sale de SACN5 sin
ensayo detras, es grado 4 por su propio criterio.

### cap.3 — Health Literacy and Client Compliance (1.292 lineas, LEIDO ENTERO)

NADA NUTRICIONAL. Ni una cifra de nutriente. Pero DOS cosas de PRODUCTO que valen
para Rawku y que apuntan al mismo sitio (`PENDIENTE_PRODUCTO.md`):

· **El 55 % de los duenos que dan una dieta terapeutica le anaden ADEMAS otras
  comidas o premios**, y el motivo que citan es «they didn't know not to» (estudio
  AAHA 2003). Un menu calculado al miligramo se lo carga un premio diario, y el
  motor hoy no lo dice en ninguna parte.
· **El cumplimiento de la dieta terapeutica es del 19 % en perro y 18 % en gato**,
  y lo que mas lo sube no es el precio (solo el 4 % la rechaza por dinero) sino el
  seguimiento: instrucciones por escrito, recordatorios y una llamada de repaso.
  Elena decide si Rawku hace algo con esto; aqui solo queda apuntado.

Y el nivel de lectura: «the average reading skills of U.S. adults are between the
8th and 9th grade levels». Es el argumento de por que los mensajes de error del
motor estan escritos como estan.

### cap.4 — Nutrigenomics and Nutrigenetics (542 lineas, LEIDO ENTERO)

NADA QUE APLICAR. Ni una cifra de requisito: es un capitulo de tecnologia
(transcriptomica, proteomica, metabolomica) y del estado de los genomas canino y
felino. Lo unico que roza al motor es una frase de contexto de SACN5 cap.4: habla de
«large- and giant-breed puppies with genetic variation that responds to diet» para
prevenir la enfermedad ortopedica del desarrollo — la misma poblacion del techo de
calcio del cachorro grande, sin cifra nueva.

### cap.5 — Macronutrients (6.819 lineas, LEIDO ENTERO)

El capitulo mas cargado de todo lo leido hasta ahora. Doce cosas.

**1. EL LIBRO SE CONTRADICE CONSIGO MISMO EN LOS MULTIPLICADORES DEL DER.**
La Tabla 5-2 Parte 2 (cap.5) y el Box 1-6 Tabla 1 (cap.1) son la MISMA tabla con
numeros DISTINTOS:

| | cap.1 Box 1-6 | cap.5 Tabla 5-2 |
|---|---|---|
| Inactivo/propenso a obesidad | 1,2-1,4 x RER | **1,4** x RER |
| Ganancia de peso | 1,2-1,8 | **1,2-1,4** |
| Trabajo ligero | 1,6-2,0 | **2** |
| Trabajo moderado | 2,0-5,0 | **3** |
| Trabajo duro | 5,0-11,0 | **4-8** |

Coinciden en lo demas (castrado 1,6 · entero 1,8 · perdida 1,0 · gestacion 3 x RER
los ultimos 21 dias · lactacion 4-8 con la tabla por cachorros · crecimiento 3 x RER
hasta los 4 meses y 2 x RER despues). ⚠️ O sea que **citar «SACN5 dice que el
trabajo duro es X» sin decir QUE TABLA es citar mal**. Si alguna cifra del repo o
de `PARA_EL_NUTRICIONISTA.md` sale de aqui, tiene que decir cual de las dos.
Y el texto corrido del cap.5 respalda la version del cap.5: «This requirement
increases to 2 x RER for dogs doing light work, 3 x RER for dogs doing moderate
work and 4 to 8 x RER for dogs doing heavy work».

**2. El escalon de los 4 meses del cachorro, literal y en las dos tablas**:
«Daily energy intake for growing puppies should be 3 x RER from weaning until four
months of age. At four months of age energy intake should be reduced to 2 x RER
until the puppy reaches adult size». Cruzar con `der.js` y con la frase de
`PARA_EL_NUTRICIONISTA.md` que ya fallo una vez por decir «<14 semanas».

**3. El senior**: «dogs over seven years of age required 10 to 20% less energy than
those three to seven years of age» y «because MER declines by approximately 15 to
20% and energy digestibility remains constant, senior dogs should be offered foods
providing a 15 to 20% caloric reduction». Con la excepcion escrita: «physical
activity in a senior dog may offset the age-associated reduction in MER».

**4. El frio** (Tabla 5-3): fuera, en frio, «dogs may need 10 to 90% more calories».
Perros de pelo corto +95 % de 25 °C a 7,6 °C; de pelo largo +59,5 %. Zona
termoneutra 15-20 °C pelo largo, 20-25 °C pelo corto, 10-15 °C perros de trineo.
El motor no pregunta por el clima. Es decision de producto, no mia.

**5. ⚠️ LO MAS IMPORTANTE PARA UNA DIETA BARF: EL LIBRO PONE UN SUELO DE PROTEINA
PARA LA DIETA SIN ALMIDON, Y ES UNA CIFRA.**
Tres frases seguidas, todas literales:
· «foods fed to growing animals and those with high-energy needs should contain at
  least 20% carbohydrates» (crecimiento, gestacion, lactacion).
· «Extensive research in dogs indicates that a **starch-free food containing at
  least 33% of ME from protein** is necessary to supply needed glucose precursors
  (Kienzle et al, 1985).»
· «Overall, a minimum of 23% carbohydrate is recommended in foods for gestating and
  lactating bitches.»
Y el experimento: perras prenadas con dieta sin hidratos y **26 % de la EM como
proteina** desarrollaron hipoglucemia la semana antes del parto, menos nacidos
vivos, letargo y peor cuidado de la camada; con **51 % de EM como proteina** y sin
almidon, igual que con almidon.
Una racion BARF **no lleva almidon**, asi que la cifra que le aplica es la de
en medio: **≥33 % de la EM como proteina**. A 3,5 kcal/g de proteina eso son
**94,3 g/1000 kcal**. ⚠️ CRUZAR con `requisitos_condicionales.json`: el condicional
de gestacion y lactacion ya existe y sale del NRC; esto es una SEGUNDA fuente que
da un numero, y hay que ver si el que aplicamos queda por encima o por debajo.

**6. El TECHO de proteina del adulto sano, literal**: «dog foods for adult
maintenance should not exceed 30% DM protein». Confirma el hallazgo S-28 (que yo
habia dicho mal al principio diciendo que el libro no ponia techo). Los minimos que
cita: NRC 8 % MS adulto y 18 % crecimiento con proteina de altisima calidad; AAFCO
18 % adulto y 22 % crecimiento con ingredientes normales.

**7. LA TABLA 5-16 ES UNA CLASE DE REQUISITO QUE EL MOTOR NO TIENE: el EQUILIBRIO
entre aminoacidos, no su minimo.** «Ideal amino acid profiles (relative to lysine)»,
para PERRO: lisina 1,00 · metionina+cistina 0,64 · triptofano 0,22 · treonina 0,67 ·
arginina 0,71 · isoleucina 0,57 · valina 0,75 · leucina 1,00 · histidina 0,29 ·
fenilalanina+tirosina 1,00. Es exactamente la forma del `ratios` que se estreno el
10 de septiembre con el Ca:P, pero con diez pares a la vez. Nosotros comprobamos
los doce minimos y ni un cociente. **No propongo aplicarla** —el propio libro dice
que el concepto viene del cerdo y se extrapolo— pero tiene que estar escrita.

**8. Linoleico**: «A concentration of 1% of the food DM as linoleic acid is a safe
and effective concentration for dogs». (Gato: ≥0,5 % MS linoleico y ≥0,02 %
araquidonico.)

**9. ⚠️ EL RATIO OMEGA-6:OMEGA-3 — EL LIBRO DICE QUE NO SE SABE.** Literal: «At
this time there are no conclusive data proving the optimal level or relationship of
omega-3 fatty acids to omega-6 fatty acids for any species at any specific
lifestage. The optimal relationship will likely depend on many individual parameters
and differ depending on individual physiologic function». Esto va DIRECTO a
`REVISION_NUTRICIONISTA.md`, donde el ratio omega-6:omega-3 es uno de los tres
puntos que «siguen sin estar». SACN5 no lo pide: dice que no hay datos. Es el mismo
lado que el NRC 2006 («is not helpful»), que ya esta escrito en
`requisitos_condicionales.json`. Dos fuentes de tres.

**10. Un techo medido de omega-3**: «Healthy adult dogs fed 7% of the food DM as
omega-3 fatty acids from fish oil, over a period of two months, showed no problems
with activated partial thromboplastin time, prothrombin time, buccal mucosal
bleeding time clotting or platelet aggregation». Util para el pendiente del omega-3
del cancer y de la artrosis, que estan en `limites_escritos_que_el_solver_no_aplica`
justamente porque no se sabia si cabian.

**11. Taurina**: «There is no evidence that taurine is an essential amino acid for
dogs; however, research indicates that it may be conditionally essential», y el dato
que importa: «feeding a high-fat food (24% DM) significantly reduced plasma taurine
concentrations». Cruzar con el BLOQUE 69, que ya mide la taurina de los menus.

**12. Agua y grasa minima**: SACN5 cap.5 dice que «the daily water requirement of
dogs and cats, expressed in ml/day, is roughly equivalent to the daily energy
requirement (DER) in kcal/day», y que el consumo total ronda **2,5 veces la materia
seca** comida («about 2.5 times the amount of dry matter (DM) consumed as food»). Y hace falta **1-2 % de grasa en el alimento**, de cualquier tipo,
solo para que se absorban las vitaminas A, D, E y K.

**13. ⚠️ Y UNA CORRECCION A UN COMENTARIO DEL REPO.** `auditar_conversiones.py`
dice hoy que el 3,5 kcal/g del Box 1-2 «es un ejemplo trabajado con un alimento
concreto, no la densidad de las tablas». **Eso no es lo que dice el Box 1-2.** Su
frase es general: «recommended nutrient values for canine and feline foods are based
on an energy density of 3.5 and 4.0 kcal ME/g (14.64 and 16.74 kJ ME/g) of food dry
matter, respectively» — 3,5 el PERRO y 4,0 el GATO —, y su Tabla 6 vuelve a usarlo:
«The requirement for potassium is 0.6% DM basis in an adult dog food that provides
3.5 kcal (14.64 kJ)/g».
La CONCLUSION del repo sigue siendo la buena (se convierte con 4,0, porque la Tabla
13-3 declara «Concentrations presume an energy density of 4.0 kcal/g» y sus propias
filas cuadran), pero **el motivo escrito es falso** y el proximo que lo lea se lo va
a creer. El motivo bueno es otro: el 3,5 del Box 1-2 es la densidad de los PERFILES
DE NUTRIENTES de AAFCO/NRC que ese recuadro esta explicando, y las tablas de
factores nutricionales clave del propio SACN5 —que son las que cita
`patologias.json`— declaran la suya, que es 4,0. Hay que reescribir ese parrafo.

### cap.6 — Micronutrients: Minerals and Vitamins (4.216 lineas, LEIDO ENTERO)

Es el capitulo de referencia de los 22 micronutrientes, y lo que trae que no
teniamos escrito son **los TECHOS**, que es justo la clase de cifra que decide si
un menu sale. Todos por kg de MATERIA SECA.

**Los techos del PERRO, uno por uno, con quien los pone:**

| Nutriente | AAFCO 2007 | NRC 2006 |
|---|---|---|
| Vitamina A | 250.000 UI/kg MS | 50.000 UI (15.000 RE) en crecimiento y gestacion/lactacion · 213.333 UI (64.000 RE) en adulto |
| Vitamina D | 5.000 UI/kg MS | 3.200 UI (80 µg colecalciferol)/kg MS |
| Vitamina E | 1.000 UI/kg MS | — |
| Yodo | 50 mg/kg | **4 mg/kg** |
| Selenio | 2 mg/kg | — |
| Cobre | 250 mg/kg MS | ninguno |
| Hierro | 3.000 mg/kg | — |
| Sodio | — | **1,5 % MS** (adulto), y por encima del 2 % «reduced food intake, negative potassium balance and vomiting» |
| Zinc · manganeso · folato · biotina · B12 · colina · K | ninguno | ninguno |

⚠️ **El del yodo hay que cruzarlo YA**: NRC pone el limite superior seguro en
**4 mg/kg MS**, que a 4,0 kcal/g son **1000 µg/1000 kcal**, y el motor aplica
**1275**. Si esa cuenta es la buena, nuestro tope esta un 27 % por encima del de
NRC. Puede que la respuesta sea que aplicamos el de FEDIAF y no el de NRC —hay que
mirarlo—, pero no puede quedarse sin mirar.

**Las densidades, declaradas y distintas segun quien publique la cifra** (esto
cierra el asunto del 3,5 contra 4,0 que quedo mal explicado en
`auditar_conversiones.py`, ver cap.5 punto 13):
· «For dogs, this calcium requirement is based on an energy density of 3.5 kcal/g
  metabolizable energy (ME), whereas an energy density of 4.0 kcal/g ME is assumed
  for cats (AAFCO, 2007)» → **los perfiles de AAFCO del perro van a 3,5**.
· «The NRC (2006) recommended allowance for adult dogs and growing puppies after
  weaning is 0.40 and 0.59% DM calcium (**both based on foods containing 4,000
  kcal/kg**)» → **el NRC va a 4,0**.
· «for large- and giant-breed puppies at risk for developmental orthopedic disease,
  the recommendation is 0.7 to 1.2% DM calcium (**based on foods containing 3,800
  kcal/kg**)» → **y esta va a 3,8**.
⚠️ O sea: **cada cifra trae su propia densidad y hay que mirarla cifra a cifra**.
La del cachorro de raza grande —que es de donde sale nuestro techo de calcio de
2750 mg/1000 kcal— la declara a **3,8**, no a 4,0. A 3,8 el 1,1 % de MS son
**2895** y el 1,2 % son **3158**. Hay que abrir `recomendaciones_libro.json` y ver
que densidad declara su bloque `conversion` para esa fila.

**Otras siete cosas:**

1. **El ratio Ca:P ideal**: «The "ideal" calcium-phosphorus ratio recommended for
   animals with simple stomachs is generally considered to be between 1:1 and 2:1»,
   con el matiz de que sube el fosforo si viene de fitato (plantas) y baja el ratio
   ideal en dietas de carne. Coincide con lo que aplicamos.
2. **El cloruro no tiene estudio propio**: «In the absence of studies establishing
   chloride requirements for dogs or cats, the DM recommendation for chloride is
   **1.5 times that of sodium**». Nuestro catalogo declara cloro; conviene saber que
   el requisito es un multiplo del sodio y no una medida.
3. **Vitamina E y PUFA, la cifra que NO cuadra con la que usamos**: «Various
   researchers have recommended **up to 60 mg of α-tocopherol per g of PUFA**;
   however, **there is no consensus among experts about the quantitation of this
   relationship**». Nosotros medimos contra la relacion clasica de **0,6 mg/g** y
   salimos holgados. Son dos ordenes de magnitud de diferencia. No propongo
   cambiarlo —el propio libro dice que no hay consenso— pero la frase de
   `condicionales.py` que dice que vamos holgados tiene que citar cual de las dos.
4. **Las tiaminasas, con cifras** (Tabla 6-6, mg de tiamina destruida por 100 g de
   pescado y hora): almeja **2.640** · bonito listado **1.000** · atun rabil y pargo
   **265** · dorado 120 · macabi 35 · aguja **0**. «Cooking destroys thiaminases».
   Cruzar con el tope de tiaminasa de `seguridad.py`.
5. **La colina se puede sustituir por metionina**: «Methionine can completely
   replace choline as a methyl donor». La cifra que da es del GATO (si la metionina
   pasa del 0,62 % MS, 3,75 partes de metionina sustituyen a 1 de colina); del perro
   no da numero. Es exactamente la forma de un requisito condicional.
6. **Los datos de vitaminas de las tablas hay que descontarlos**: «To account for
   potential errors, references recommend that analytical values in databases be
   **discounted by 10 to 25%**». Va directo a `DATOS_QUE_FALTAN.md` y al catalogo:
   nuestros valores de vitaminas salen de BEDCA/CIQUAL/USDA sin descuento ninguno.
7. **Toxicidad de la B6 en perro, medida**: mas de **200 mg de piridoxina HCl/kg de
   peso y dia** produjo perdida bilateral de mielina y de axones. Y la vitamina A del
   Caso 6-5: un gato con higado de vaca a diario, vitamina A serica en 315 µg/dl
   contra 20-80 normales, con espondilosis cervical. El higado es lo que mas se
   repite en un BARF.

### cap.7 — Antioxidants (607 lineas, LEIDO ENTERO)

Capitulo corto y con cifras. Cinco cosas.

1. **⚠️ UNA CUARTA DENSIDAD, Y ES LA DE LA VITAMINA E.** El requisito del NRC se
   publica «based on a food containing 0.1 ppm selenium, not more than 1% linoleic
   acid and **3,670 kcal metabolizable energy/kg DM**». O sea que ya van cuatro
   densidades distintas en el mismo libro segun quien publique la cifra: AAFCO
   perro 3,5 · NRC calcio 4,0 · calcio del cachorro grande 3,8 · vitamina E 3,67.
   **La densidad se mira cifra a cifra o la conversion sale mal.**
2. **El techo de la vitamina E**: «There are no published toxicity data for vitamin
   E in dogs; however, concentrations exceeding 2,000 IU/kg DM of food have been fed
   for 17 weeks without observable negative reactions». Y el que se propone:
   «a level of 1,000 IU/kg DM of food, or 45 IU/kg of body weight, has been
   suggested (NRC, 2006)». Coincide con el maximo de AAFCO del cap.6.
3. **El selenio antioxidante, que es MAS del triple del requisito**: «Studies
   indicate antioxidant protective ranges for selenium would be approximately **0.50
   to 1.3 mg selenium/kg food DM** for dogs and cats», con el requisito del perro
   adulto en **0,10 mg/kg** y la recomendacion del NRC en 0,35. Es el hallazgo S-11,
   confirmado aqui por segunda vez y en el mismo rango. Y el techo: «AAFCO (2007)
   suggests a safe upper limit of 2 mg selenium/kg diet for dogs».
   ⚠️ Ese rango entero cabe por debajo del techo, asi que **no es una eleccion
   entre seguridad y beneficio**: es una decision clinica sobre si el motor apunta
   al requisito o al rango protector. La toma Elena.
4. **La frase que resume el capitulo y que vale para el motor entero**: «In the case
   of all of these antioxidants, effective levels necessary to reduce disease risk
   are much higher than levels needed to merely prevent nutritional deficiency». El
   motor formula contra el segundo numero, no contra el primero, y eso esta bien
   dicho — pero conviene que este escrito.
5. **Dos margenes medidos**: la dosis letal 50 intravenosa de vitamina C es «greater
   than 500 mg/kg/day and 2,000 mg/kg/day for cats and dogs»; y el betacaroteno en
   beagles a 50-250 mg/kg/dia dio decoloracion del pelo y vacuolizacion hepatica
   «at all dose levels» pero «no consistent findings of toxicity were found».

### cap.8 — Commercial Pet Foods (3.431 lineas, LEIDO ENTERO)

Capitulo de industria: formas del alimento, marketing, ingredientes, extrusion,
enlatado y control de calidad. Casi todo queda fuera de un motor de BARF, pero trae
**seis cosas que si nos tocan**, y la primera hay que escribirla aunque no guste.

1. **⚠️ EL LIBRO HABLA DE NOSOTROS, Y MAL.** Box 8-5, «Myth No. 9», literal:
   «"BARF" diets (Bones and Raw Foods) better meet the archetypical needs of dogs
   that cannot digest grains commonly used in commercial pet foods.» y la respuesta:
   «FACT: The BARF philosophy appears to be a decision primarily driven by emotion.
   Currently there are no published peer-reviewed clinical papers or scientific
   support for BARF diets (Chapter 11).»
   Queda apuntado tal cual. Es un libro de 2010 escrito en gran parte por gente de
   Hill's, y hay que leerlo con eso delante — pero **la afirmacion que hace es
   comprobable y no se puede tapar**: en 2010 no habia ensayos clinicos revisados
   por pares del BARF. El cap.11 es el que lo desarrolla y lo leere entero cuando
   llegue. Que la fuente que usamos para poner limites diga esto de la dieta que
   calculamos es exactamente la clase de cosa que tiene que estar escrita en
   `PARA_EL_NUTRICIONISTA.md`, no escondida.

2. **La regla del 10 % para premios y sobras**, literal: «As a generalization,
   dietary balance is maintained when less than 10% of the daily intake consists of
   table scraps or treats and the remainder is a prepared food that is complete and
   balanced». Y el uso indebido, que incluye «up to 20% of the daily energy
   requirement is provided by treats used for dental benefits». Junto con el 55 %
   del cap.3 que anade comida por su cuenta, es el mismo pendiente de producto.

3. **Las proteinas que mas reacciones adversas causan, con reparto** (revision de
   15 estudios, 278 perros): «beef, dairy products and wheat represented 69% of
   reported cases; lamb, chicken egg, chicken and soy represented an additional 25%
   of the cases». Va a `exclusiones.py` y a la pantalla de alergias: la vaca y el
   trigo encabezan la lista, no el pollo.

4. **⚠️ UNA TABLA PARA CONTRASTAR EL CATALOGO SIN SALIR DEL LIBRO.** La Tabla 8-7
   da la proteina «as fed» de los ingredientes humedos, que son justo los nuestros:
   higado (cerdo, vaca, pavo, cordero) 17-22 % · subproductos carnicos (pulmon, bazo,
   riñon) 15-20 % · vaca (canal) 18-22 % · **pollo (entero, carcasas, cuellos)
   10-12 %** · pescado de rio 12-15 % · pescado de mar 20-27 %. Es una comprobacion
   de orden de magnitud independiente de BEDCA/CIQUAL/USDA. La de la carcasa de
   pollo llama la atencion por lo baja.

5. **La oxidacion la catalizan el hierro, el cobre, la luz y el calor**, y destruye
   «fat and fat-soluble vitamins». En un BARF congelado no hay extrusion ni
   esterilizado —las perdidas de vitaminas que mide el Box 8-8 (tiamina 52 % en el
   enlatado, piridoxina 89 % en el humedo de perro, vitamina C 100 %) **no nos
   aplican**— pero la oxidacion del aceite de pescado si, y ahi es donde el catalogo
   pone EPA y DHA.

6. **Que el alimento seco limpie los dientes es una generalizacion, no un hecho**:
   «An epidemiologic study of progressive periodontitis in poodles found no
   correlation between food form and disease progression». Util cuando alguien
   pregunte si el BARF perjudica los dientes por no ser croqueta.

### cap.9 — Pet Food Labels (1.743 lineas, LEIDO ENTERO)

Capitulo de etiquetado y de quien regula que, en EE.UU., Canada y Europa. Casi
todo queda fuera, pero trae **el antepasado directo de un fichero nuestro** y dos
matices de conversion.

1. **⚠️ LA LEGISLACION EUROPEA DE ALIMENTOS DIETETICOS, QUE ES DE DONDE VIENE
   `limites_legales_ue_2020_354.json`.** SACN5 la describe en su version de 1995:
   Directiva 93/74/CE del Consejo y Directivas 94/39/CE y 95/9/CE de la Comision,
   con la Tabla 9-11, que son las **17 indicaciones permitidas** — insuficiencia
   renal cronica, disolucion de estruvita, reduccion de recidiva de estruvita,
   urato, oxalato, cistina, intolerancias, trastornos de absorcion agudos,
   maldigestion, insuficiencia cardiaca, diabetes, insuficiencia hepatica,
   hiperlipidemia, reduccion de cobre en el higado, dermatosis y caida de pelo,
   exceso de peso y restauracion nutricional. **Es exactamente la lista de nuestros
   20 objetivos**, quince años antes. Y la frase que importa:
   «The legislation considers most indications for nutritional management as
   "temporary situations" making it mandatory to publish a defined length of use on
   the labels.»
   COMPROBADO EN EL MISMO SITIO: nuestro fichero ya lleva `tiempo_recomendado` en
   cada entrada («inicialmente hasta 6 meses» en la renal). No hay hueco aqui, pero
   **el motor no le dice nada al usuario sobre la duracion** — eso sigue abierto.

2. **La declaracion de energia esta PROHIBIDA en la etiqueta europea**, salvo en
   los dieteticos de obesidad y convalecencia: «Energy declaration is forbidden in
   the EU except for some veterinary dietetic pet foods». Explica por que una
   etiqueta europea no trae kcal y por que el reglamento convierte por **kg de
   pienso al 12 % de humedad** en vez de por 1000 kcal — que es el divisor 3,52 que
   usa nuestro fichero.

3. **La analitica europea es TIPICA y la americana es GARANTIZADA, y no significan
   lo mismo**: en EE.UU. los porcentajes «generally indicate the "worst case" levels
   for these nutrients in the food and do not reflect the exact or typical amounts»;
   en Europa se declara la media. Importa si alguna vez se contrasta una ficha del
   catalogo contra una etiqueta.

4. **Y una cifra que vale para el catalogo**: en EE.UU. «the maximum moisture
   content in all pet foods should not exceed 78%», salvo que se etiquete como
   estofado, salsa, caldo o sustituto de leche. Nada que aplicar; queda apuntado.

**Nada nutricional que aplicar.** No hay ni un requisito ni un techo nuevo.

### cap.10 — Making Pet Foods at Home (2.066 lineas, LEIDO ENTERO)

**El capitulo del libro que habla de lo que hacemos.** Es una racion casera
formulada; nosotros formulamos raciones caseras. Todo lo de aqui hay que leerlo dos
veces: parte coincide con el motor, parte lo contradice de frente, y las dos cosas
tienen que estar escritas.

**LO QUE COINCIDE Y NOS DA LA RAZON**

1. **Por que existe un motor como el nuestro, con cifra**: «In one survey, 90% of
   the homemade elimination foods prescribed by 116 veterinarians in North America
   were not nutritionally adequate for adult canine or feline maintenance
   (Roudebush and Cowell, 1992)». Noventa por ciento, y prescritas por veterinarios.
2. **El fallo tipico de la racion casera es EXACTAMENTE el que vigila el motor**:
   «many formulations contain excessive protein, but are deficient in calories,
   calcium, vitamins and microminerals. Commonly used meat and carbohydrate sources
   contain more phosphorus than calcium; therefore, homemade foods may have inverse
   calcium to phosphorus ratios as high as 1:10.» El Ca:P invertido 1:10 es el
   primer numero que comprueba `_garantizar_verificado`.
3. **Y el segundo fallo tipico es de PRODUCTO, no de calculo**: «The second most
   common error made by pet owners who cook for their pets is to eliminate the
   vitamin-mineral supplement because of its inconvenience, expense or a failure to
   understand its importance. Foods made from recipes that were once crudely
   balanced become grossly unbalanced when owners eliminate supplements.» El Caso
   10-4 es eso mismo con nombre y apellidos: un springer que a los seis meses llega
   con dolor de espalda y debilidad porque el dueño dejo de dar **una pastilla de
   0,5 g de carbonato calcico al dia** por incomoda. El motor da el gramaje de los
   suplementos y no dice en ninguna parte lo que pasa si se saltan.
4. **No se puede formular una racion casera completa sin suplementos inorganicos**:
   «it is not possible to formulate a complete and balanced homemade food without
   using inorganic supplements». Es la regla 4 de `CLAUDE.md` —suplementos y extras
   siempre libres— dicha por la fuente.
5. **El yodo, con cifra que va directa al catalogo**: «It is difficult to meet the
   iodine requirement without using the iodized form (400 µg of iodine/6 g [1 tsp]
   sodium chloride)». ⚠️ HAY QUE MIRAR la ficha de la sal del catalogo: si declara
   sal sin yodar, el yodo de los menus sale de otro sitio y hay que saber de cual.
6. **El higado arregla los aminoacidos, con dosis**: «Providing some liver in the
   meat portion is recommended once a week or no more than half of the meat portion
   regularly. Liver corrects most potential amino acid deficiencies in homemade
   foods for dogs and cats.» El techo del «no mas de la mitad de la carne» es un
   limite de FORMA que nosotros ponemos por margenes de categoria.
7. **Y una frase que vale para el catalogo entero**: «Skeletal muscle protein from
   different animal species has very similar amino acid profiles. The protein
   content of various mammalian and avian skeletal muscle tissues is generally
   equivalent on a water-free basis. Thus, there is no great advantage to feeding
   one meat source over another.» Es el argumento de por que faltan 16 aminogramas
   y el motor sigue en pie: los musculares se parecen entre si.

**LO QUE NOS CONTRADICE, Y HAY QUE ESCRIBIRLO**

8. **⚠️ LA PROPORCION QUE RECOMIENDA SACN5 ES LA INVERSA DE LA BARF.** Literal:
   «The carbohydrate source to protein source ratio should be at least 1:1 to 2:1
   for cat foods and 2:1 to 3:1 for dog foods» y «The final food should contain 25
   to 30% cooked meat for dogs, (one part meat to two or three parts
   carbohydrate…)». O sea: **dos o tres partes de cereal cocido por una de carne**,
   con la carne al 25-30 % del peso. Una racion BARF va justo al reves. El libro no
   da un argumento nutricional para esa proporcion: la razon que sale de su propio
   cap.5 es la del glucogeno —hidratos para los precursores de glucosa—, y ahi
   **si** da la alternativa para la dieta sin almidon (≥33 % de la EM como
   proteina). Esto no es una cifra que aplicar: es una discrepancia de fondo entre
   la fuente y el producto, y va a `PARA_EL_NUTRICIONISTA.md`.
9. **⚠️ EL LIBRO DESACONSEJA LA CARNE CRUDA, DOS VECES.** «Some owners and breeders
   encourage the use of uncooked meat, liver and eggs in their homemade pet food
   recipes. This practice can be dangerous because uncooked animal ingredients can
   harbor pathogenic bacteria that normally would be killed during cooking (Chapter
   11).» Y la instruccion: «Animal ingredients (meat and eggs) should be cooked for
   at least 10 minutes at 82°C (180°F)». Con el cap.11 pendiente de leer, que es el
   que lo desarrolla.
10. **Y la conclusion del capitulo**: «in general, homemade formulas won't be as
    effective as commercially prepared veterinary therapeutic foods» y
    «Veterinarians should always: 1) offer to have a homemade recipe evaluated by a
    nutritionist and 2) recommend the feeding of a consistent complete and balanced
    commercial product as often as possible.»

**LAS CIFRAS SUELTAS QUE SIRVEN**

· **Conservacion**, que el motor no dice en ninguna parte: lotes de tres a siete
  dias en nevera **a 0-4 °C** en recipiente hermetico, o congelado **a -20 °C**;
  «highly susceptible to bacterial and fungal growth when left at room temperatures
  for more than a few hours»; y hay que mirar cada dia color y olor.
· **El suplemento vitaminico NO se cocina ni se guarda con la comida**: «Vitamins
  may be destroyed by heat or oxidation. The vitamin-mineral supplement should be
  kept separate from the food, and administered just before, during or after a
  meal».
· **Mezclarlo todo con batidora**, «to prevent the animal from picking out single
  food items» — si el perro elige, el menu verde deja de serlo.
· **Composicion de los suplementos de calcio**: carbonato calcico **40 % de calcio
  y menos del 1 % de fosforo**; harina de hueso y fosfato dicalcico **~27 % de
  calcio y 16 % de fosforo (2:1)**. Contrastar con las fichas del catalogo.
· **Grasa minima anadida cuando la carne es magra**: al menos **2 % del peso de la
  formula en perro** y 5 % en gato.
· **Humedad de una racion casera: ~70 %**, mas parecida a la humeda que a la seca.
· **Revision**: dos o tres visitas al veterinario al año y revision nutricional dos
  veces al año; a los seis meses de dieta casera exclusiva, historial de tres a
  cinco dias. Y los tejidos que primero avisan: piel, pelo, cristalino y retina.
· **Proteinas y carbohidratos NOVEDOSOS para dieta de eliminacion** (Norteamerica,
  2010): caza (venado, bisonte, alce), conejo, avestruz y pato; y patata, cebada y
  guisante. Y la prevalencia: la reaccion adversa a la comida es «roughly estimated
  at 1% of all hospital cases, or 10 to 20% of cases with allergic dermatoses
  presented to specialists».
· **Vegano**: puede quedarse corto en «arginine, lysine, methionine, tryptophan,
  taurine, iron, calcium, zinc, vitamin A and some B vitamins».

### cap.11 — Food Safety (2.108 lineas, LEIDO ENTERO)

**El capitulo que el cap.8 prometia, y va contra la dieta cruda de frente.** Tiene
una seccion entera titulada «RAW INGREDIENT DIETS». Lo copio con sus cifras porque
esto no se puede resumir a favor ni en contra: es la fuente que usamos para poner
limites diciendo lo que dice de la dieta que calculamos, y **tiene que estar en
`PARA_EL_NUTRICIONISTA.md` con estas mismas palabras**.

**LOS ARGUMENTOS DEL LIBRO, UNO A UNO**

1. **Contra el argumento evolutivo**: «No compelling scientific evidence based on
   evolution supports statements that dogs should eat uncooked food as did wild
   canids. Claims that dogs are carnivores, rather than omnivores, are likely due to
   confusion of taxonomy (Carnivora) with feeding behavior (carnivore).»
2. **Contra el argumento del pelo**: «The high fat content (>50%) of raw food diets
   compared to that found in most dry kibble (<30%) often can account for owners'
   reports of improvement in the appearance of their pet's coat».
3. **⚠️ Contra el argumento de los dientes, y con una cifra que va justo contra el
   hueso carnoso**: «The incidence of periodontitis and fractured teeth, however,
   increased with age in 67 dogs eating raw animal carcasses with bones in a dental
   health study (Robinson and Gorrel, 1997).»
4. **Sobre el equilibrio**: «None of the homemade and commercially available raw
   food diets analyzed were appropriate for long-term feeding (Freeman and Michel,
   2001, 2001a)». Y: «To date, no scientific evidence exists that demonstrates raw
   food diets provide additional or exceptionally unique nutrients that cannot be
   obtained from cooked food.»
5. **Las cifras de contaminacion, que son las que mas pesan**: de 25 dietas crudas
   comerciales, «64% were positive for E. coli and 20% were positive for Salmonella
   spp. In addition, 20% were contaminated with Clostridium perfringens». Y de las
   caseras: «Salmonella spp. were isolated from 80% of the raw meat and bone diets
   sampled and in 30% of the stool samples from dogs consuming those diets». En
   galgos de carreras, «45% of the meat samples were contaminated with salmonellae».
6. **⚠️ Y LA QUE MAS NOS TOCA, PORQUE LA GENTE LO HACE CON RAWKU: CONGELAR NO
   ESTERILIZA.** «Neither freezing raw meat before feeding nor purchasing
   freeze-dried commercial foods eliminates pathogens; freezing and freeze-drying are
   ineffective means for killing bacteria. In fact, both methods are used for
   long-term preservation of valuable stock bacterial cultures in laboratories.»
7. **Contra el argumento del pH gastrico**: «Advocates of feeding raw meat, bone and
   eggs claim that pathogenic organisms in raw meat do not affect dogs and cats due
   to the lower stomach pH and shorter GI transit times in these species. Stomach pH
   and GI transit times are in fact similar among people, dogs and cats and do not
   lower the risk to pets.»
8. **El riesgo es de la CASA, no solo del perro**: perros infectados excretan
   Salmonella, Campylobacter o Yersinia «yet remain clinically normal», y esta
   documentada la transmision al hogar. El libro pone en la lista de precaucion
   extra a mayores, inmunodeprimidos, quimioterapia, antiinflamatorios y **niños que
   gatean**.
9. **Y la obligacion que le pone al profesional**: «Veterinarians recommending
   commercial or homemade foods containing raw meat or eggs have an **ethical
   responsibility to fully inform pet owners of the increased potential risk** of
   foodborne pathogens not only to the pet but the entire household». Si Rawku va a
   ser firmado por veterinarios (`VETERINARIOS.md`), esta frase es parte del diseño
   de la pauta, no una nota al pie.
10. **La escala de riesgo del propio libro**, de menos a mas: enlatado regulado ·
    seco regulado · semihumedo regulado · **casero fresco individual** · seco
    comercial local · comida de perrera producida en masa · basura y carroña. La
    dieta casera esta en el medio, no al final.
11. Y la Tabla 11-5 dice literalmente **«Avoid frozen raw diets»** y **«Cook all
    home-prepared foods at 82°C (180°F) for at least 10 minutes»**.

**COMO SE LEE ESTO SIN TRAGARLO NI TIRARLO**

· Es un libro de 2010, editado en gran parte por gente de Hill's, que fabrica
  precisamente la alternativa. Eso hay que decirlo y no cambia ni una cifra: el 64 %
  de E. coli y el 80 % de Salmonella son medidas, y las medidas se comprueban en la
  fuente original, no se descartan por quien las cita.
· **Nada de esto es un requisito nutricional.** No hay ni un mínimo ni un techo que
  aplicar. Es riesgo microbiologico, que es una dimension que el motor **no modela
  en absoluto**, y no puede modelar: no tiene forma de saber como manipula la carne
  quien la compra.
· Lo que si puede hacer el producto, y hoy no hace: **decirlo**. Higiene, cadena de
  frio (0-4 °C, tres a siete dias; -20 °C congelado, cap.10), utensilios propios,
  descongelar en nevera y no a temperatura ambiente («When large blocks of frozen
  meat are thawed at room temperature, the outermost surface of the meat can reach
  unacceptably high temperatures before the center has thawed»), y el aviso al hogar
  con inmunodeprimidos o niños pequeños. **Es decision de Elena**, y va a
  `PENDIENTE_PRODUCTO.md`.

**LO DEMAS DEL CAPITULO, que si trae cifras y algunas ya estan en el motor**

· **Cebolla**: signos con **5-10 g/kg de peso** de cebolla cruda, cocinada o
  deshidratada; **30 g/kg tres dias seguidos** produjo anemia grave, cuerpos de Heinz
  y hemoglobinuria en todos los perros, uno murio el dia 5. **Ajo**: «foods
  containing garlic should not be fed to dogs». Cruza con el anexo 7.7 de FEDIAF que
  ya vigila el BLOQUE 82.
· **Chocolate**: dosis toxica de teobromina «greater than 200 mg/kg», pero un
  springer murio con **92 mg/kg**; chocolate negro de reposteria **450 mg/onza**;
  cacao en polvo 1-3 % de teobromina. Y «Theobromine is eliminated very slowly in
  dogs», lo que acumula con dosis pequeñas repetidas — que es lo que dice
  `seguridad.py`.
· **Uva y pasa**: SACN5 cap.11 describe fallo renal agudo por cantidades variables,
  «as little as 0.41 oz./kg in one case», y añade que **«given the lack of a
  dose-response relationship, no clear toxic principle has been identified»**. Es
  exactamente el argumento por el que en el BLOQUE 82 no hay cantidad segura.
· **Aflatoxina**: perro y gato estan «among the species most sensitive», con DL50 de
  **0,5 a 1,0 mg/kg**; el limite de accion de la FDA en alimento para mascotas son
  **20 ppb**; y «Aflatoxins are heat stable and not destroyed by boiling,
  autoclaving or food manufacturing methods». Un BARF de carne no lleva cereal, que
  es donde vive.
· **Histamina en pescado**: por debajo de 5-6 ppm es normal, a 20 ppm el deterioro
  ya se nota, y a **500 ppm** es el limite de accion de la FDA. Perro y gato toleran
  **2.500 ppm**. Relevante para el pescado azul del catalogo.
· **Metales medidos en alimento comercial**: plomo 0,88-1,26 ppm, cadmio 0,22-0,80,
  arsenico 0,37, zinc 122 ppm. No toxicos, pero es el orden de magnitud del que
  hablamos cuando se dice «contaminantes».
· **Salmon crudo**: la enfermedad del salmon, *Neorickettsia helminthoeca*, por
  ingerir salmon crudo con el trematodo *Nanophyetus salmincola*; sin tratamiento a
  tiempo, «mortality can reach 50 to 90%». El catalogo tiene salmon.
