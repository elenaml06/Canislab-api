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

### cap.12 — Introduction to Feeding Normal Dogs (619 lineas, LEIDO ENTERO)

Capitulo corto de contexto: el perro es omnivoro, no carnivoro, y por que.
Tres cosas que sirven.

1. **⚠️ UN LIMITE FISICO QUE EL MOTOR NO TIENE Y PODRIA TENER.** Literal: «On
   average, a medium-sized, adult domestic dog has the capacity to ingest **30 to
   35 g of dry matter per kg body weight per day**», y el estomago «can hold 1 to 9
   liters depending on the breed». Para un perro de 20 kg son **600-700 g de materia
   seca al dia**; a la humedad de un BARF (~70 %, cap.10) eso son unos **2 kg de
   comida fresca**. El motor no comprueba en ninguna parte que la racion QUEPA en el
   perro. Y ya ha hecho falta: el 8 de septiembre una regeneracion del catalogo sin
   `margenes_categoria` saco menus de **25,8 kg de comida al dia** y los 216 salieron
   **en verde**, porque lo que se habia apagado era la forma y la forma no la mira el
   semaforo. Esta cifra es una segunda red, independiente de las proporciones BARF, y
   viene de la fuente. **Es candidata a comprobacion nueva** — decision de Elena.

2. **La Tabla 12-5 es la demostracion numerica de por que existe este motor**: un
   perro de 10 kg alimentado SOLO con carne picada de vaca, en la cantidad que cubre
   sus kcal (482 g), recibe: proteina **341 % del recomendado**, grasa **1.204 %**,
   calcio **5 %**, fosforo 128 %, **ratio Ca:P de 1:20**, cobre 24 %, **yodo 10 %**,
   zinc 70 %. El libro concluye: «This comparison confirms that an all-meat food
   would be unbalanced for dogs». Es el mismo cuadro que sale al analizar una dieta
   casera en `/analizar`.

3. **El perro es omnivoro y el libro lo argumenta con anatomia**: la relacion entre
   longitud del tubo digestivo y longitud del cuerpo es **6:1 en el perro**, 4:1 en
   el gato, 10:1 en el conejo y hasta 20:1 en algunos herbivoros; el intestino
   delgado es el 23 % del volumen digestivo del perro contra el 15 % del gato; y «Dogs
   digest starch effectively via pancreatic enzymes and mucosal disaccharidases».
   Tambien: en la presa, «Viscera are typically consumed; therefore, partially
   digested vegetable material is a normal part of the wolf's diet».

### cap.13 — Feeding Young Adult Dogs: Before Middle Age (1.993 lineas, LEIDO ENTERO)

**El capitulo de referencia del perro adulto sano, y la Tabla 13-3 es LA tabla de la
que sale `recomendaciones_libro.json`.** Confirmado literal al pie de la tabla:
«*Dry matter basis. **Concentrations presume an energy density of 4.0 kcal/g.**
Levels should be corrected for foods with higher energy densities.» — que es
exactamente lo que `auditar_conversiones.py` dice, esta vez leido en su sitio.

**LA TABLA 13-3 ENTERA, en % de materia seca a 4,0 kcal/g** (columna normal /
columna inactivo-propenso a obesidad), con lo que dan por 1000 kcal:

| Factor | Normal | Inactivo | Por 1000 kcal |
|---|---|---|---|
| Densidad energetica (kcal EM/g MS) | 3,5-4,5 | 3,0-3,5 | — |
| Grasa y acidos grasos esenciales | 10-20 % | 7-10 % | 25-50 g |
| Fibra bruta | ≤5 % | ≥10 % | — |
| Proteina | 15-30 % | 15-30 % | 37,5-75 g |
| **Fosforo** | **0,4-0,8 %** | 0,4-0,8 % | **1000-2000 mg** |
| **Sodio** | **0,2-0,4 %** | 0,2-0,4 % | **500-1000 mg** |
| Cloruro | 1,5 x Na | 1,5 x Na | — |
| **Vitamina E** | **≥400 UI/kg** | ≥400 | **≥100 UI** |
| **Vitamina C** | **≥100 mg/kg** | ≥100 | **≥25 mg** |
| **Selenio** | **0,5-1,3 mg/kg** | 0,5-1,3 | **125-325 µg** |
| Textura (sello VOHC) | placa | placa | — |

✅ **Los dos techos de `recomendaciones_libro.json` cuadran clavados**: fosforo
0,8 % MS ÷ 4,0 = **2000 mg/1000 kcal** y sodio 0,4 % ÷ 4,0 = **1000 mg/1000 kcal**.
Son el **tope del rango** de esta tabla, no una cifra suelta. Queda comprobado en
la fuente y no de oidas.

**⚠️ Y TRES FILAS DE ESA MISMA TABLA QUE EL MOTOR NO APLICA**, y que son de la
misma tabla y con la misma autoridad que las dos que si:
· **Vitamina E ≥400 UI/kg MS** = ≥100 UI/1000 kcal. El requisito del NRC son
  **30 mg/kg MS**, o sea que la tabla pide **mas de diez veces el requisito**. El
  texto lo explica: «Research indicates that a level of vitamin E much higher than
  the requirement confers specific biologic benefits», con un estudio de
  biomarcadores que pide 500 UI/kg y otro donde 2.010 UI/kg mejoro la funcion
  inmunitaria en perros mayores durante un año sin problemas de seguridad. El techo
  sugerido: «An upper limit of 1,000 to 2,000 IU/kg food (DM) has been suggested for
  dogs». Es el hallazgo S-12/S-33, ahora con la cifra de la tabla y no solo del texto.
· **Selenio 0,5-1,3 mg/kg MS** = 125-325 µg/1000 kcal, con el requisito minimo en
  **0,10 mg/kg** y el maximo de AAFCO en **2,0 mg/kg**. El rango entero cabe. Es
  S-11.
· **Vitamina C ≥100 mg/kg MS**, aunque el perro la sintetiza — «dogs (and cats) have
  from one-quarter to one-tenth the ability to synthesize vitamin C as other
  mammals». ⚠️ Ojo: el cap.40 nos dice lo contrario para el oxalato calcico («excessive
  quantities of vitamin C should be avoided»), y **ninguna ficha del catalogo declara
  vitamina C**, asi que el motor no podria aplicarlo ni queriendo.

**EL PORQUE DEL TECHO DE FOSFORO, con cifras**: «up to **25%** of the young adult
dog population may already be affected by subclinical kidney disease» y «**22.4%**
of all dogs over five years of age examined at a European veterinary teaching
hospital … had abnormally elevated kidney function tests». Y: «Excess dietary
phosphorus can accelerate progression of chronic renal disease». Es el argumento
entero de por que existe `recomendaciones_libro.json`, en la fuente.

**LA PROTEINA, con tres formas de decirlo y una que va por 100 kcal**:
· minimo teorico «1.7 g metabolizable protein/BWkg^0.75 for an ideal protein»;
· con proteina media (valor biologico ~70), 2,1-2,5 g digestible/BWkg^0.75;
· y el recomendado: «A daily protein intake for adult maintenance of 4.3 to 5.0 g
  digestible protein/BWkg^0.75 (biologic value = 70) or **4.0 to 6.5 g digestible
  protein/100 kcal ME** is recommended» → **40-65 g/1000 kcal**.
⚠️ Un BARF tipico de este motor lleva **~105 g/1000 kcal**. Eso es entre **1,6 y 2,6
veces** el rango recomendado, y por encima del techo del 30 % MS (= 75 g/1000 kcal).
El propio libro dice que el exceso «is not stored as protein, but rather is
deaminated by the liver» y que «foods high in protein also tend to contain high
levels of phosphorus» — que es justo el nutriente al que le pone techo. Los dos
numeros estan unidos y hay que llevarlos juntos a la revision.

**LA GRASA Y LOS OMEGA-3, con dos cifras nuevas**: minimo del NRC **8,5 % MS de
grasa** con al menos **1 % de acido linoleico**; y — esta si es nueva —
«The minimum recommended allowance for dietary **eicosapentaenoic plus
docosahexaenoic acids is 0.044% DM** (NRC, 2006)», que a 4,0 kcal/g son
**110 mg de EPA+DHA por 1000 kcal**. ⚠️ Cruzar con el minimo de `epa_dha` del motor.
Y el matiz sobre el omega-3: «Whether omega-3 fatty acids are essential is less
certain … Nevertheless, a source of dietary omega-3 fatty acids is recommended».

**EL DER POR EDAD (Tabla 13-2)**, que es una tercera version de los multiplicadores
y **no coincide con ninguna de las dos anteriores**:

| Edad | kcal EM/BWkg^0.75 | x RER |
|---|---|---|
| 1-2 años | 120-140 | 1,7-2,0 |
| 3-7 años | 100-130 | 1,4-1,9 |
| >7 años | 80-120 | 1,1-1,7 |

Con la nota al pie: «Most pet dogs are minimally active and have a DER of
approximately **95 kcal/BWkg^0.75 or 1.2 to 1.4 x RER**». Y el Cuadro 13-6 vuelve a
dar los de siempre: castrado 1,6 · entero 1,8 · inactivo 1,2-1,4 · trabajo 2,0-8,0.
Ya van **tres tablas del mismo libro** con multiplicadores distintos (cap.1, cap.5 y
esta). Citar una sin decir cual es citar mal.

**Y LO QUE ANADE SOBRE EL PERRO CONCRETO**:
· **Castrar**: «Obesity occurs twice as often in neutered dogs than in
  reproductively intact dogs», y la causa parece ser mas comida, no menos gasto:
  SACN5 cap.13: «**Neutering does not appear to have a marked impact on the resting
  energy expenditure of female dogs**»; lo que si sube, dice la misma frase, es la
  ingesta.
  El motor ya pregunta por la esterilizacion.
· **Sexo**: «One study showed that female dogs had an average of **16% more body
  fat** than male dogs», y no hay estudios controlados de requisitos por sexo.
· **Raza**: Terranova **~20 % menos** de energia que la media; **gran danes y
  dalmata hasta un 60 % mas**. El motor no pregunta la raza para las kcal.
· **Frio**: hasta un **10-90 % mas** de energia fuera en invierno; temperatura
  critica inferior 15-20 °C en pelo largo, 20-25 °C en pelo corto, 10-15 °C en
  razas articas. Y calor: mas AGUA y poca mas energia — en desierto, «the water
  required for cooling a 15-kg dog may equal **2,5 % of its body mass per hour**».
· **Premios**: «<10% of the total diet on a volume, weight or calorie basis», con
  el ejemplo que duele: **diez premios de hueso al dia le subieron el calcio a un
  pastor aleman de 5 meses un 80 %** por encima de un alimento de cachorro grande, y
  eso «increases the risk of developmental orthopedic disease». El motor calcula el
  calcio del cachorro grande al miligramo y no dice nada de los premios.
· **Revision**: perro sano cada seis a doce meses, y **mas a menudo si come casero**
  — «Because few if any homemade recipes have been tested according to prescribed
  feeding protocols».
· Y el criterio de que va bien: «alert, have an ideal BCS (2.5/5 to 3.5/5) with a
  stable, normal body weight and a healthy coat. Stools should be firm, well formed
  and medium to dark brown.»

### cap.14 — Feeding Mature Adult Dogs: Middle Aged and Older (1.087 lineas, LEIDO ENTERO)

**De aqui sale el 1750 del fosforo senior.** La Tabla 14-2, en % de materia seca:

| Factor | Normal | Inactivo | Por 1000 kcal (a 4,0) |
|---|---|---|---|
| Densidad energetica | 3,0-4,0 | 3,0-3,5 | — |
| Grasa bruta | 10-15 % | 7-10 % | 25-37,5 g |
| Fibra bruta | ≥2 % | ≥10 % | — |
| Proteina | **15-23 %** | 15-23 % | **37,5-57,5 g** |
| **Fosforo** | **0,3-0,7 %** | 0,3-0,7 % | **750-1750 mg** |
| Sodio | 0,15-0,4 % | 0,15-0,4 % | 375-1000 mg |
| Cloruro | 1,5 x Na | 1,5 x Na | — |
| Vitamina E | 400 UI/kg | 400 | 100 UI |
| Vitamina C | ≥100 mg/kg | ≥100 | ≥25 mg |
| Selenio | 0,5-1,3 mg/kg | 0,5-1,3 | 125-325 µg |

✅ **El 1750 cuadra**: 0,7 % MS ÷ 4,0 = 1750 mg/1000 kcal, tope del rango.

⚠️ **PERO HAY UN DETALLE DE AUDITORIA QUE HAY QUE MIRAR**: al pie de la **Tabla
14-2 NO se declara la densidad**. Dice solo «*All foods expressed on a dry matter
basis unless otherwise noted. If the caloric density of the food is different, the
nutrient content in the dry matter must be adapted accordingly (Chapter 1).» —
**«different» de que, no lo dice**. La que declara 4,0 es su hermana, la Tabla 13-3
del adulto joven. O sea que **nuestra conversion del fosforo senior se apoya en la
densidad declarada por OTRA tabla**. La conclusion sigue pareciendo la buena (las
dos tablas son de la misma serie y del mismo capitulo doble), pero **el bloque
`conversion` de `recomendaciones_libro.json` tiene que citar de donde saca el 4,0
para esta fila, y decir que no es del pie de su propia tabla**. Hay que abrirlo.

**Y TRES COSAS NUEVAS QUE EL MOTOR NO TIENE**

1. **⚠️ UN TECHO DE CALCIO PARA EL ADULTO, QUE NO TENIAMOS**: «Foods with **0.4 to
   0.8% DM calcium** are recommended for mature dogs. The **calcium-phosphorus ratio
   should not be less than 1:1**.» El 0,8 % MS son **2000 mg/1000 kcal**. Hoy el
   motor solo pone techo de calcio en crecimiento (4250 / 2750 segun el peso adulto)
   y en adulto se queda con el maximo de FEDIAF. Es exactamente la misma forma que
   el fosforo y el sodio de `recomendaciones_libro.json`: un techo del libro para el
   perro **sano**. **Candidato claro a cuarta cifra de ese fichero** — decision de
   Elena, y hay que medir antes si cabe.
2. **El techo de proteina del maduro baja a 23 % MS** (frente al 30 % del adulto
   joven) = **57,5 g/1000 kcal**. Un BARF de ~105 g/1000 kcal esta a casi el doble.
   El libro lo justifica con estudios: «foods with **18% DM protein** are adequate to
   maintain immunocompetence in older dogs» y «foods with **16 to 20% DM protein**
   are sufficient to maintain nitrogen balance and protein stores in older dogs». Y
   el matiz honesto: «High protein intake has **not** been shown to contribute to the
   development of kidney disease in healthy animals. However, after kidney function
   is impaired, protein may play a role in progression of renal disease» — con el
   estudio de cuatro años en perros con un solo riñon donde 34 % contra 18 % **no
   cambio la funcion renal** pero si aumento la matriz mesangial y la fibrosis.
3. **La unica intervencion nutricional que alarga la vida, con cifra**: «The only
   nutritional modification known to slow aging and increase the lifespan
   consistently in multiple species is caloric restriction. **Reducing caloric intake
   by 20 to 30% of normal**, while meeting essential nutrient needs, slows the aging
   process and reduces the risk for cancer, renal disease, arthritis and
   immune-mediated diseases». Y reconoce que «This level of restriction seems
   difficult to achieve in the long term».

**Lo demas que sirve**
· **Cuando empieza «maduro», con cifra y criterio**: «a food change should be
  considered around the age of **five years for large- and giant-breed dogs** and
  around **seven years for small dogs**», porque se considera mayor al llegar a la
  mitad de su esperanza de vida. Cruzar con como resuelve la etapa `requisitos.py`.
· **La caida del DER con la edad**: «a **12 to 13% decrease** in daily energy
  requirement by around seven years of age», y el punto de partida «1.4 x resting
  energy requirement (100 kcal ME/BWkg^0.75)».
· **Supervivencia por tamaño** (Tabla 14-1): a los 10 años sobrevive el **38 %** de
  los perros pequeños y el **13 %** de los grandes; a los 15, el **7,0 %** y el
  **0,1 %**.
· **Disfuncion cognitiva**: afecta al **28 %** de los perros de 11-12 años y al
  **68 %** de los de 15-16.
· Y la frase que explica por que al mayor se le aprieta el rango por arriba:
  «mature animals may no longer be able to cope with excesses, borderline
  deficiencies or changes in nutrient intake and quality. Therefore, foods for
  mature dogs should meet allowances more rigorously and consistently because of
  lack of reserve capacity».

### cap.15 — Feeding Reproducing Dogs (1.573 lineas, LEIDO ENTERO)

**El capitulo de gestacion y lactancia, y trae la SEGUNDA fuente independiente del
suelo de proteina que el motor ya aplica a la dieta sin hidratos.**

1. **LA DIETA SIN HIDRATOS, CONFIRMADA POR TERCERA VIA.** `requisitos_condicionales.json`
   aplica desde el 8 de septiembre un suelo de **125 g de proteina/1000 kcal** en
   gestacion y lactancia cuando la dieta no lleva hidratos, sacado del «may be
   double» de FEDIAF §3.3.1 sobre los 62,5 de la Tabla III-3b. SACN5 cap.15 lo dice
   con **otras dos formas del mismo numero**, y las dos apuntan al mismo sitio o mas
   arriba:
   · «If no carbohydrate is given, protein intake must almost be doubled; the food
     must provide **at least 12 to 13 g digestible protein/BWkg 0.75**».
   · Y el Box 15-1: «If a carbohydrate-free food is fed, gluconeogenic precursors
     such as protein should be **increased by at least 50 % when energy requirements
     are moderate and may have to be doubled if the energy requirement of the dam is
     high**».
   Y la Tabla 15-1 de SACN5 pone el desenlace en la columna de al lado, con nombre
   propio: la fila «Carbohydrate-free food» tiene enfrente, en la columna
   «Reproductive and health consequences», bajo peso al nacer, mas morbilidad y
   mortalidad neonatal y mas nacidos muertos. (Es una **fila de tabla**, no una frase:
   va descrita y no entrecomillada, porque las celdas de una tabla salen del PDF en
   lineas sueltas y pegarlas seria escribir una frase que el libro no dice.)
   No hay que cambiar nada: el x2
   que aplicamos es el extremo alto de esa horquilla, o sea el lado seguro. Queda
   escrito **porque una cifra con tres fuentes independientes no se vuelve a
   discutir**.

2. **⚠️ EL HUECO REAL DEL CAPITULO: NO HAY NINGUN TECHO EN GESTACION NI EN
   LACTANCIA, Y LA TABLA 15-5 DA CUATRO.** `recomendaciones_libro.json` tiene hoy
   adulto (fosforo y sodio), senior (fosforo) y crecimiento (calcio y fosforo, en
   sus dos columnas). **Gestacion y lactancia no tienen ninguno.** La Tabla 15-5
   («Key nutritional factors for reproducing dogs») da, en materia seca y con la
   densidad de 4,0 kcal/g que el propio capitulo exige («the food should be high in
   energy density (≥4.0 kcal/g)»):
   · **Calcio 1,0-1,7 %** → **2500-4250 mg/1000 kcal**
   · **Fosforo 0,7-1,3 %** → **1750-3250 mg/1000 kcal**
   · **Proteina 25-35 %** → 62,5-87,5 g/1000 kcal
   · **Grasa ≥20 %** → ≥50 g/1000 kcal
   Y el techo de calcio **no es cosmetico, tiene mecanismo clinico escrito**. SACN5 cap.15,
   con la comparacion con la vaca lechera delante: «**excessive calcium intake during
   pregnancy may decrease activity of the parathyroid glands and predispose the bitch
   to eclampsia during lactation**», y por eso se recomienda para casi todas las razas
   un alimento que «**avoids large excesses of calcium (1.0 to 1.7% DM)**».
   El Box 15-2 entero es esa enfermedad, y señala a la dieta casera de carne:
   «**toy breeds tend to receive more meat-based homemade foods, which are low in
   calcium**» — un BARF mal formulado esta en las dos puntas del problema a la vez.
   **Es candidata a cifra nueva en `recomendaciones_libro.json` y es decision de
   Elena**, con la medida por delante: hay que resolver menus de Gestante,
   GestanteTardia y Lactante y ver donde cae hoy el calcio, exactamente como se hizo
   con los techos de adulto y de cachorro.

3. **UNA DISCREPANCIA DENTRO DEL PROPIO CAPITULO, apuntada para no copiarla mal.**
   La Tabla 15-5 pone el ratio Ca:P de gestacion/lactancia en **«1:1-2:1»** y el
   texto de la seccion de calcio dice dos veces **«1.1:1 to 2:1»**. No cambia lo que
   hace el motor (aplicamos el 1,0-2,0 de FEDIAF, que es el mismo techo y un suelo
   mas bajo), pero si alguien cita esta tabla algun dia, **la tabla y el texto no
   dicen lo mismo** y hay que decir cual de los dos se esta citando.

4. **La energia de la gestacion, para cruzar con `der.py` y `der.js`.** Tabla 15-10:
   SACN5 Tabla 15-10: «**Gestation = 1.8 to 2.0 x RER for the first four weeks, then
   2.2 to 3.5 x RER for the last five weeks**» y «**Lactation = 4.0 to 8.0 x RER**»,
   con el pico de lactancia en 2,1 x RER mas un 25 % por cachorro. Y la Tabla 15-6 lo
   da en incremento sobre el DER:
   semana 5 «DER + 18 kcal ME/kg BW», semanas 6-8 «DER + 36», semana 9 «DER + 18».
   El motor no calcula el DER (lo manda el frontend), asi que esto **no es un
   requisito nutricional**, pero es la referencia contra la que se compara si algun
   dia se revisa la curva de reproduccion. Es el mismo tipo de cruce que dejo la
   Tabla 33-8 sin hacer.

5. **Cifras minimas del capitulo que ya cubre FEDIAF o que no aplican**: hierro
   ≥70 mg/kg MS, zinc ≥96, cobre ≥12,4, fenilalanina ≥0,83 % MS, fenilalanina+
   tirosina ≥1,23 % MS (todas «NRC, 2006», para gestacion tardia y pico de
   lactancia). **Y una que si toca el catalogo**: «**Oxides of iron should not be
   used as an iron source because they are poorly available**» y «oxides of copper
   should not be used because they are poorly available» — que es exactamente lo que
   ya vive en `sacn5_fuentes_de_minerales.json` con sus dos ceros, ahora confirmado
   en un segundo capitulo.

6. **El DHA de reproduccion, confirmado literal** en el sitio del que salio:
   «Foods for late gestation and peak lactation should contain the minimum
   recommended allowance of DHA plus eicosapentaenoic acid (EPA) of at least 0.05 %
   (DM) (NRC, 2006). Therefore, DHA needs to be at least 40 % of the total DHA plus
   EPA, or 0.02 % DM». Es la cita que ya lleva `requisitos_condicionales.json`, leida
   ahora en su parrafo entero y no en la fila de la tabla.

7. **El agua**, otra vez y con cifra de trabajo: «Water requirements in ml are
   roughly equal to energy requirements in kcal. A 35-kg bitch nursing a large litter
   may require **five to six liters of water per day** at peak lactation».

### cap.16 — Feeding Nursing and Orphaned Puppies from Birth to Weaning (2.148 lineas, LEIDO ENTERO)

**Casi todo el capitulo esta fuera del alcance del motor** — el lactante mama, no
come raciones —, pero deja tres cosas que si sirven.

1. **LA ARGININA: LA MISMA REGLA QUE APLICAMOS, DICHA EN LA OTRA UNIDAD, Y CUADRA.**
   `requisitos_condicionales.json` aplica «+0,01 g de arginina por cada gramo de
   proteina sobre el requisito» con anclas por etapa, y su campo `por_que` ya explica
   que el 0,01 sale igual en las dos unidades. SACN5 cap.16 lo enuncia **en la unidad
   de %MS**: «For four- to 14-week-old puppies, **0.01 g of arginine should be added
   for every 1 % of crude protein in excess of 22.5 %** (NRC, 2006)». Y ese 22,5 %MS
   es exactamente el ancla que ya usamos para crecimiento temprano y reproduccion
   (22,5 %MS × 2,5 = 56,25 g/1000 kcal). O sea que **la conversion que hicimos el 9
   de septiembre esta confirmada contra una fuente distinta**, no solo contra la
   aritmetica.

2. **La leche de perra como referencia** (Tabla 16-4, en %MS): proteina 33, grasa
   41,8, linoleico 4,9, calcio 1,06, fosforo 0,79, **6,43 kcal/g MS**, digestibilidad
   >95 %. El capitulo hace el ajuste que hay que hacer y que nosotros hacemos todo el
   rato: «Bitch's milk has an energy density of 6.43 kcal/g (DM). **Converting this
   amount of linoleic acid to a 4 kcal/g basis results in a linoleic acid equivalent
   of 3.0 % (DM)**» — o sea que el libro tampoco compara %MS entre alimentos de
   densidades distintas sin convertir. Es la misma cuenta que rehace
   `auditar_conversiones.py`.

3. **Cuando empieza a comer solido**, que es cuando empieza a existir para este
   motor: «Most puppies will start eating solid food **between three and four weeks
   of age**» y «Weaning should be effectively completed **between six and seven weeks
   of age**». Y el alimento del destete, en el mismo capitulo de SACN5: «**contain at
   least 25 to 30 % protein and have an energy content of at least 4.0 kcal (16.7 kJ)
   metabolizable energy/g (dry matter)**».

### cap.17 — Feeding Growing Puppies: Postweaning to Adulthood (910 lineas, LEIDO ENTERO)

**La Tabla 17-1 es la que ya aplica `recomendaciones_libro.json` para el cachorro.
Confirmada literal, celda a celda, y con el texto que la deriva.**

1. **Las dos columnas, confirmadas.** Tabla 17-1, «Recommended levels in food (DM)»,
   «Puppies with an adult BW <25 kg» / «>25 kg»: calcio **0,7-1,7 / 0,7-1,2**,
   fosforo **0,6-1,3 / 0,6-1,1**, Ca:P **1:1-1.8:1 / 1:1-1.5:1**, proteina 22-32 %,
   grasa 10-25 %, DHA ≥0,02 %, densidad 3,5-4,5 kcal/g. Y el texto lo repite fuera de
   la tabla: «Foods for large- and giant-breed puppies should contain **0.7 to 1.2 %
   DM calcium (0.6 to 1.1 % phosphorus)**» y «**Because small- to medium-sized breeds
   are less sensitive to slightly overfeeding or underfeeding calcium**» —la fuente
   mete aqui su cita bibliografica— «**the level of calcium in foods for these puppies
   can range from 0.7 to 1.7% DM, (0.6 to 1.3% phosphorus) without risk**». Los techos que aplicamos hoy (4250 y 3250 al pequeño;
   2750 y 2750 al grande) salen de aqui, con el calcio del grande **apretado al 1,1 %
   por Fascetti cap.10** en vez del 1,2 % de esta tabla, o sea por el lado seguro.

2. **⚠️ UN TECHO DE ESTA TABLA QUE NO APLICAMOS, Y ES EL RATIO.** SACN5 pone el Ca:P
   del cachorro de **mas de 25 kg de adulto en 1,5:1 como maximo**. El motor aplica
   hoy el de FEDIAF: 1,8 en crecimiento tardio y **1,6** cuando el peso adulto llega
   a `RAZA_GRANDE_O_GIGANTE_KG` (15 kg, nota b de la Tabla III-3a). O sea que para un
   cachorro que vaya a pesar mas de 25 kg **damos 1,6 donde la fuente canina dice
   1,5**. Es poco margen y por eso mismo es facil que nadie lo mire. **No se toca
   ahora**: el cap.33 (Tabla 33-5) es el capitulo especifico de raza grande y hay que
   leerlo entero antes de decidir, que es el metodo de este documento. Queda apuntado
   con los dos umbrales al lado, que ya se confundieron una vez: **25 kg es de SACN5
   y 15 kg es de FEDIAF, y deciden cosas distintas**.

3. **Por que hay techo de calcio en el cachorro y no en el adulto**, con el mecanismo
   escrito. SACN5 cap.17: «**intestinal absorption of calcium never decreases below
   approximately 40 %, even if they receive high levels of calcium in foods**», la
   retencion sube con la ingesta, y —dos frases mas abajo, en el mismo parrafo—
   «**Absorption of calcium gradually is more regulated after puppies are about 10
   months old**». Un cachorro no se defiende del exceso; un
   adulto si. Eso es exactamente por que el techo del adulto es una recomendacion y el
   del cachorro cubre un hueco de seguridad.

4. **El minimo de fosforo del cachorro, que es mas bajo de lo que parece**: «The
   phosphorus intake is less critical than the calcium intake, **provided the minimum
   requirements of 0.35 % DM are met** and the calcium-phosphorus ratio is between 1:1
   and 1.8:1». Y mas arriba, en el mismo capitulo de SACN5, se citan cachorros
   criados con exito con «**0.37 to 0.6% DM calcium and 0.33% DM phosphorus**».

5. **La energia del crecimiento** (Tabla 17-2), para el mismo cruce pendiente que la
   Tabla 33-8. Sus tres filas, leidas (es una **tabla**, asi que va descrita y no
   entrecomillada): del destete al 50 % del peso adulto, **3 x RER** = 210 kcal/BWkg^0,75;
   del 50 al 80 %, **2,5 x RER** = 175; a partir del 80 %, **1,8-2,0 x RER** = 125-140.
   Y el Gran Danes en la nota al pie, esa si literal: «**Great Dane puppies may need
   25% more energy during the first two months after weaning = 250 kcal or 1,050
   kJ/BWkg**».

6. **⚠️ UNA ERRATA DE LA FUENTE, apuntada para que nadie la copie.** El capitulo dice
   «The recommended minimum allowance for copper in growing puppies is **1.1 % DM**
   (NRC, 2006)». Eso son 11.000 mg/kg de materia seca, que es absurdo: el NRC pide
   **11 mg/kg MS**. Es un error de unidad del libro, no una cifra a aplicar. Lo apunto
   porque este repo tiene ya un caso de un x10 escrito con forma de dato bueno
   (`auditar_conversiones.py`, 8 de septiembre) y la unica defensa es leerlo y decirlo.

7. **Y una frase que vale para todo el producto**: «**Underfeeding through the growth
   phase is healthier than overfeeding and results in the same mature size**»
   (Tabla 17-3, punto 7).

### cap.18 — Feeding Working and Sporting Dogs (4.061 lineas, LEIDO ENTERO)

**De aqui sale la vitamina E del perro de trabajo que ya aplica
`requisitos_condicionales.json`. Confirmada, y con las otras dos de su fila.**

1. **La Tabla 18-9, confirmada literal en sus cuatro columnas** (sprint · intermedio
   de duracion/frecuencia baja o moderada · intermedio de duracion/frecuencia alta ·
   resistencia). Los tres antioxidantes valen **lo mismo en las cuatro**:
   · **Vitamina E ≥500 IU/kg MS** — la cifra que aplicamos.
   · **Vitamina C 150-250 mg/kg MS**.
   · **Selenio 0,5-1,3 mg/kg MS**.
   Y el texto da el porque de cada una. De la E: «Based on antioxidant biomarker
   studies in non-exercising dogs, for improved antioxidant performance, dog foods
   should contain at least 500 IU/kg of DM vitamin E». Del selenio: «The minimum
   requirement for selenium in foods for dogs is 0.10 mg/kg (DM)… Therefore, for
   increased antioxidant benefits, the recommended range of selenium for dog foods is
   0.5 to 1.3 mg/kg (DM)».

2. **⚠️ Y TRAE EL LIMITE POR ARRIBA, QUE ES LO QUE FALTABA PARA PODER DECIDIR.** El
   capitulo dice explicitamente que pasarse **empeora el rendimiento, con las dos
   medidas. SACN5 cap.18: «**When racing greyhounds were supplemented with high doses
   (1 g/day) of vitamin C, they ran slower**» y «**Racing greyhounds also ran slower
   when supplemented with high doses of vitamin E (1,000 IU/day) but not lower doses
   (100 IU/day)**». Y el mecanismo: «**Single antioxidant supplementation can have a
   pro-oxidant effect**… If co-antioxidants are absent or decreased, the α-tocopherol
   radical can exhibit pro-oxidant activity», y «**High doses of vitamin C and
   selenium may act as pro-oxidants**». O sea que estas tres cifras **no son «cuanto
   mas mejor»**, y si alguna vez se aplican las tres hay que aplicarlas juntas: el
   propio libro dice que «**Multi-nutrient antioxidant supplementation using lower
   doses is a better approach**». Eso responde media pregunta abierta de Elena sobre
   el selenio.
   El techo regulatorio del selenio, para el cruce con `seguridad.py`: «There are no
   data to base a safe upper limit of selenium for dogs or cats, but for regulatory
   purposes, a **maximum standard of 2.0 mg/kg (DM)** has been set for dog foods in
   the United States (AAFCO, 2007)».

3. **⚠️ EL CALCIO DEL PERRO QUE COME CARNE, QUE ES EL NUESTRO.** Box 18-6, literal y
   entero, porque describe una racion BARF sin nombrarla: «Canine athletes fed
   high-fat foods or those whose food is supplemented with meat (as is common with
   greyhounds and sled dogs) **may require additional calcium**. The high level of fat
   in performance foods **enhances the formation of insoluble calcium soaps, thus
   rendering a portion of the ingested calcium unavailable**. Additionally, **red meat
   is rich in phosphorus and nearly devoid of calcium**. Meat supplementation may thus
   require calcium supplementation to maintain a normal calcium content and
   calcium-phosphorus ratio in the diet. **Dietary calcium levels of 1.2 to 2.0 % of a
   food's DM have been successfully fed to working dogs**. Very high-fat foods with
   lower calcium concentrations may be deficient in available calcium. **Excessive
   calcium supplementation may also predispose a dog to zinc deficiency by inhibiting
   absorption of this nutrient**».
   Tres cosas, y ninguna se aplica hoy: (a) el motor cuenta el calcio del menu como si
   estuviera todo disponible, y con mucha grasa **no lo esta**; (b) por eso el rango
   que el libro da al perro de trabajo empieza en **1,2 %MS = 3000 mg/1000 kcal**, muy
   por encima del minimo de FEDIAF; (c) y el aviso de zinc es el mismo que ya vive en
   `requisitos_condicionales.json` como `zinc_y_cobre_cuando_el_calcio_esta_alto`,
   `documentado_sin_cifra` — **sigue sin cifra tambien aqui**, asi que sigue inerte con
   razon. Lo de los jabones calcicos **no es cuantificable con lo que dice el libro**
   («a portion»), asi que tampoco se puede aplicar; queda escrito como lo que es: una
   razon medida para NO apurar el calcio por abajo en un menu muy graso.

4. **El magnesio del galgo**, que es la unica cifra de mineral con nombre propio del
   capitulo, en SACN5 cap.18: «**Foods containing low levels of magnesium (but at levels
   above the minimum Association of American Feed Control Official's allowance)
   resulted in clinical signs of magnesium deficiency in greyhound dogs**» y «**These
   signs were alleviated when foods containing magnesium at 0.12 % of the dry matter
   (DM) were fed**» — 300 mg/1000 kcal. Es un caso de «cumplir el
   minimo no basto», que es el mismo argumento de los techos del libro pero por el
   otro lado. Sin etapa ni poblacion definida mas alla de «galgo de carreras», asi que
   **no es aplicable**; queda apuntado.

5. **El perro de trabajo NO necesita mas proteina de lo que parece, y el libro lo
   dice con numeros**: «The protein requirement for exercise is only **mildly
   increased (5 to 15 %)** regardless of exercise type… **Dietary protein should be at
   least 24 % of kcal**», y para el de resistencia «**16 % of the ME as protein should
   be viewed as an absolute minimum**». El estudio detras: los perros de trineo con
   solo el 16 % de la energia como proteina «suffered significantly more injuries and
   had a significant decline in VO2 max» frente a los del 24, 32 y 40 %. Un BARF va
   muy por encima de todo esto.

6. **Los hidratos, y por que aqui no son un requisito**: «Provided sufficient
   gluconeogenic precursors are available, **dogs have no dietary requirement for
   carbohydrates except during gestation and neonatal development**». Es la frase que
   sostiene que una racion sin hidratos sea legitima en adulto **y que no lo sea en
   gestacion**, que es justo lo que separa el suelo condicional del punto 1 del cap.15.
   Con un matiz medido: «Studies involving sled dogs fed 0 or 17 % of their kcal as
   carbohydrate showed that dogs were **more susceptible to developing "stress"
   diarrhea when fed foods devoid of carbohydrate**».

7. **La grasa por tipo de ejercicio** (Tabla 18-9), por si algun dia hay un modo
   «perro de trabajo»: sprint 8-10 %MS · intermedio bajo 15-30 · intermedio alto 25-40
   · resistencia >50 %MS. Y densidad: 3,5-4,0 · 4,0-5,0 · 4,5-5,5 · >6,0 kcal/g MS.
   Con el aviso de que **la grasa insaturada no es libre**: «>60 % unsaturated fatty
   acids to optimize olfaction» en los dos intermedios, pero «large intakes of
   unsaturated fatty acids may increase the risk of oxidative damage to membrane
   lipids», que es precisamente por que la fila de al lado pide los tres antioxidantes.

8. **Seguridad alimentaria, otra vez y en un capitulo distinto.** SACN5 cap.18, sobre
   el galgo y el perro de trineo alimentados con carne casera de calidad variable:
   «**the safety of these foods should always be evaluated**», «**Some raw meat sources
   contain abundant bacteria and bacterial toxins**» y «**Raw foods may pose a health
   hazard for people who care for these**» — la frase sigue en la pagina siguiente y
   termina «dogs and for the dogs themselves», que va aqui sin comillas porque el salto
   de pagina mete en medio la cabecera del libro. Y el caso 18-1 lo aterriza en una racion que es un BARF
   de galgo. Es el mismo pendiente de producto que dejo el cap.11: **decirlo**.

---

## Los seis capitulos FELINOS (19 a 24), leidos enteros a proposito

**POR QUE SE LEEN SI RAWKU ES DE PERROS.** Porque el repo ya tiene su propia
leccion sobre esto: `sacn5_tablas.json` aparta 44 tablas «felinas» **por su propio
titulo**, y la razon de que ese campo se llame `veredicto_por` es que una vez se
descarto como «celda felina» la nota d del selenio, **que es un techo del PERRO**.
Un capitulo entero titulado «Feeding Normal Cats» no es lo mismo que una celda de
una tabla mixta, pero la unica forma de que «no habia nada del perro aqui» sea
comprobable es haberlo leido. **Y habia**: la Tabla 19-6 del capitulo del gato trae
una columna entera de cachorro de PERRO.

Los seis van declarados en `lecturas_sacn5.json` con su `lectura_integra` como
cualquier otro, porque se han leido igual.

### cap.19 — Introduction to Feeding Normal Cats (1.299 lineas, LEIDO ENTERO)

1. **⚠️ LA TABLA 19-6 ES CANINA A MEDIAS, Y CONFIRMA TRECE MINIMOS DEL MOTOR.** Se
   titula «Comparison of minimal protein and amino acid requirements for growth in
   kittens and puppies» y su segunda columna es **«Recommended allowance for
   puppies», del NRC 2006, en %MS y con la nota al pie «Based on a dietary energy
   content of 4.0 kcal/g dry matter»**. O sea: es una transcripcion INDEPENDIENTE de
   las mismas cifras del NRC que FEDIAF publica en su Tabla III-3b, en un libro
   distinto. Convertida con el ×2,5 de siempre y comparada contra lo que el motor
   aplica hoy en `CachorroCrecimiento` (g/1000 kcal):

   | Aminoacido | SACN5 T19-6 (%MS) | ×2,5 | FEDIAF, aplicado |
   |---|---|---|---|
   | Proteina | 17,5 | 43,75 | **50** |
   | Arginina | 0,66 | 1,65 | **1,84** |
   | Histidina | 0,25 | 0,625 | 0,63 |
   | Isoleucina | 0,50 | 1,25 | 1,25 |
   | Leucina | 0,82 | 2,05 | **2,00** |
   | Lisina | 0,70 | 1,75 | 1,75 |
   | Metionina | 0,26 | 0,65 | 0,65 |
   | Metionina+cistina | 0,53 | 1,325 | 1,33 |
   | Fenilalanina | 0,50 | 1,25 | 1,25 |
   | Fenilalanina+tirosina | 1,00 | 2,50 | 2,50 |
   | Treonina | 0,63 | 1,575 | 1,60 |
   | Triptofano | 0,18 | 0,45 | **0,53** |
   | Valina | 0,56 | 1,40 | 1,40 |

   **Doce de trece cuadran o van por el lado seguro** (FEDIAF pide igual o mas). La
   unica en la que FEDIAF va por DEBAJO es la **leucina**: 2,00 contra 2,05, un
   2,4 %. Es demasiado poco para ser un error de transcripcion de nadie y demasiado
   poco para cambiar un menu, pero queda apuntado porque es lo unico que no cuadra y
   porque **manda FEDIAF**, que es la regla de este repo. Esto no es una fuente
   nueva: es la comprobacion de que la cadena PDF → `auditar_fediaf.py` →
   `requerimientos_v2_final.json` da el mismo numero que dio otro equipo leyendo el
   mismo NRC.

2. **Y la nota al pie de esa tabla dice la regla de la arginina otra vez**, ahora en
   la columna del GATO: «Arginine requirement increases in kittens with increased
   dietary protein; approximately 2 g/kg should be added for each 10 % increase in
   crude protein above the minimum allowance (22.5 %)». En %MS eso es 0,2 puntos de
   arginina por cada 10 de proteina = **0,02 por punto**, o sea **el doble del 0,01
   del perro**. Confirma que el coeficiente que aplicamos es el canino y no el
   felino, que es justo la confusion que podia colarse.

3. **La Tabla 19-5 pone las dos especies una al lado de otra**, y explica de paso por
   que el perro no es un gato: el perro necesita **12 % MS de proteina para crecer y
   4 % para mantenimiento** con proteina ideal (18 y 8 con el minimo del NRC), y el
   gato 29 y 19. La frase: «**The protein requirement for growth in kittens is only
   50 % higher than that of puppies, whereas the protein requirement for feline
   maintenance is twice that of adult dogs**».

4. **La Tabla 19-3 repite el dato anatomico del cap.12**: la relacion intestino
   delgado : longitud del cuerpo es **4:1 en el gato, 6:1 en el perro**, 10:1 en el
   conejo y 14:1 en el cerdo. Y el texto dice del perro: «**dogs can more efficiently
   use a variety of foods, some of which may require more digestion than animal
   tissues**».

5. **El Box 19-3 habla de huesos y de carne cruda, y aunque va de gatos las dos
   frases no llevan especie dentro.** «**Bones with jagged or sharp points are often
   to blame for oral trauma and can become esophageal foreign bodies. Bone feeding is
   also associated with colitis and constipation in small animals**» — «small
   animals» es perro y gato. Y de la carne cruda: «**Raw meat, even when "flash
   frozen," may contain harmful bacteria (e.g., Salmonella spp. and Escherichia coli)
   and parasites**» y «**Unless supplemented with vitamins and minerals, raw meat is
   nutritionally incomplete and can lead to nutritional secondary
   hyperparathyroidism, iodine deficiency or both**». Es el mismo pendiente de
   producto del cap.11 y del cap.18, dicho por tercera vez.

6. **La cebolla, con la cifra del gato para comparar con la del perro**: en el gato
   «**Subsequent studies have demonstrated toxic effects at levels of 2.5 % dry
   matter**». El cap.11 daba 5-10 g/kg de peso para el perro. Dos poblaciones, dos
   formas de medir; ninguna cambia el BLOQUE 82, que no admite cantidad segura.

### cap.20 — Feeding Young Adult Cats (2.053 lineas, LEIDO ENTERO)

**Nada aplicable al motor**, y eso hay que poder afirmarlo: el capitulo entero gira
sobre pH urinario, magnesio y estruvita, que son problemas felinos. Lo unico que
cruza con el perro:

· **El techo de selenio de AAFCO, otra vez, y dicho como prestado**: «There are no
  data on which to base a safe upper limit of selenium for cats, but for regulatory
  purposes, a **maximum of 2 mg/kg DM has been set for dog foods** in the United
  States (AAFCO, 2007)». Son 500 µg/1000 kcal, muy por encima del maximo que aplica
  el motor (142 µg, de FEDIAF). El nuestro es el estricto; no cambia nada.
· **La misma tabla de antioxidantes que el perro de trabajo**, con las mismas cifras
  para el gato adulto (vitamina E ≥500 UI/kg MS, C 100-200 mg/kg, Se 0,5-1,3 mg/kg).
  Que las cuatro columnas del perro de trabajo y la del gato sano den lo mismo dice
  que **ese 500 no es una cifra del ejercicio: es la cifra de «rendimiento
  antioxidante» de este libro**, y viene del mismo estudio (Jewell et al, 2000). Lo
  apunto porque afina el alcance de lo que aplicamos: `requisitos_condicionales.json`
  lo aplica **solo al perro de trabajo**, que es lo conservador.

### cap.21 — Feeding Mature Adult Cats (1.676 lineas, LEIDO ENTERO)

**Nada aplicable.** Una frase que si vale como argumento general, y que es la hermana
felina de la que ya esta apuntada del cap.14: «**Reducing caloric intake by 20 to
30 % of normal, while meeting essential nutrient needs, slows the aging process and
decreases susceptibility to cancer, renal disease, arthritis and immune-mediated
diseases in animal models studied**», seguida de «**This level of caloric restriction
is difficult to achieve in the long term and has not been incorporated into
mainstream nutritional advice**».

### cap.22 — Feeding Reproducing Cats (1.494 lineas, LEIDO ENTERO)

**Nada aplicable**, pero el capitulo es el espejo del 15 y sirve para leer bien aquel:
· El gato **si** tiene un suelo de hidratos en lactancia y por el mismo motivo que la
  perra: «**at least 10 % DM digestible carbohydrate should be included in foods for
  lactating queens**» (el perro, 23 %). Y el mecanismo escrito es el mismo:
  «Digestible carbohydrates spare protein necessary to sustain blood glucose
  concentrations in queens and provide a substrate for lactose during milk
  production».
· El DHA de reproduccion, en su version felina: **≥0,004 %MS** (contra ≥0,02 % del
  perro), derivado igual: «**the minimum recommended allowance of DHA plus
  eicosapentaenoic acid (EPA) is at least 0.01 % DM**» y «**DHA needs to be at least
  40 % of the total DHA plus EPA, or ≥0.004 % DM**». Los dos porcentajes son distintos y
  **la regla del 40 % es la misma**, que es exactamente lo que aplica
  `requisitos_condicionales.json` con la cifra canina.
· Y la eclampsia otra vez, con el mismo mecanismo del Box 15-2: «**High calcium
  intake may down-regulate parathyroid gland secretion and impair normal mobilization
  of calcium from skeletal stores**». Que la misma frase aparezca en el capitulo del
  perro y en el del gato refuerza el hallazgo del cap.15: **el techo de calcio de la
  gestacion no es una preferencia de formulacion, es prevencion de una enfermedad**.

### cap.23 — Feeding Nursing and Orphaned Kittens (1.633 lineas, LEIDO ENTERO)

**Nada aplicable** — el motor no formula para lactantes. La Tabla 23-3 trae la leche
de perra al lado de la de gata para comparar, con las mismas cifras que la 15-3 y la
16-4, y ahi cierra el circulo de los tres capitulos.

### cap.24 — Feeding Growing Kittens: Postweaning (872 lineas, LEIDO ENTERO)

**Nada aplicable**, y una diferencia entre especies que conviene tener escrita para no
mezclarlas nunca: «**Unlike the situation with puppies, calcium excess in kittens is
not associated with developmental orthopedic disease**». O sea que los techos de
calcio del cachorro de la Tabla 17-1 —que el motor SI aplica— son especificamente
caninos y no tienen equivalente felino. Y la contrapartida, que si es comun a las dos
especies y describe una racion BARF mal hecha: «**Calcium deficiency coupled with
phosphorus excess occurs most commonly in kittens fed unsupplemented all-meat
diets**».

---

## Los capítulos de CLÍNICA (25 en adelante)

Aquí empieza la mitad clínica del libro. La regla de lectura no cambia, pero sí
cambia qué se busca: de aquí salen (o no salen) las cifras de `patologias.json`.

### cap.25 — Critical Care Nutrition and Enteral-Assisted Feeding (3.664 lineas, LEIDO ENTERO)

**Casi todo es alimentación por sonda y no toca al motor**, que formula raciones
para un perro que come solo. Lo que sí cruza:

1. **La Tabla 25-5 confirma DOS suelos del motor por una vía distinta.** Está en
   **unidades por 100 kcal**, no en %MS —el propio capítulo explica por qué: «in
   critical care nutrition, nutrient requirements are conventionally expressed on an
   energy rather than on a DM basis»—, así que se compara directo con lo nuestro
   multiplicando por 10:
   · **Arginina ≥146 mg/100 kcal para el perro** = **1,46 g/1000 kcal**. El motor
     aplica 1,51 en adulto (FEDIAF). El nuestro es el estricto.
   · **Proteína 5,0-12,0 g/100 kcal para el perro** = 50-120 g/1000 kcal. Un BARF
     típico va por 105, o sea **dentro del rango del paciente crítico**, cerca del
     techo. No es un límite del perro sano y no se aplica; queda apuntado porque es
     la primera vez que aparece un TECHO de proteína expresado en la unidad del
     motor.
   Y una tercera que **no tiene equivalente en FEDIAF**: **glutamina ≥500 mg/100
   kcal** = 5 g/1000 kcal. La glutamina no es esencial y no está en la Tabla III-3b,
   así que no hay nada que aplicar.

2. **El ratio omega-6:omega-3, cuarta fuente y cuarto rango distinto.** El capítulo:
   «the dietary dose that favors a less inflammatory cascade during a disease process
   is still not standardized across veterinary patients, but is suggested as an
   **omega-6:omega-3 fatty acid ratio ranging between 5:1 to 1:1**, depending on
   patient assessment». Es exactamente lo que dice `CLAUDE.md` de por qué ese ratio
   sigue sin aplicarse: **cada fuente da uno distinto y la elección es clínica**.
   Ahora hay una cuarta cifra y sigue sin haber una sola.

3. **El agua, otra vez y con la misma regla**: «The water requirements in ml for
   normal healthy animals approximate their daily energy requirement (DER) in kcal».

4. **Y una cifra de seguridad que sí es del perro sano**, aunque venga de un capítulo
   de UCI: la capacidad gástrica. «**Gastric capacities for cats and dogs are typically
   5 to 10 ml/kg body weight during initial food reintroduction**» y «**Maximum
   capacities as high as 45 to 90 ml/kg body weight have been measured in cats and
   dogs when fully re-alimented**». Los 45-90 ml/kg son la hermana líquida de los
   **30-35 g de materia seca por kg** del cap.12, y apuntan al mismo hueco: **el
   motor no comprueba en ninguna parte que la ración quepa en el perro**. Sigue
   siendo decisión de Elena.

### cap.26 — Parenteral-Assisted Feeding (2.056 lineas, LEIDO ENTERO)

**Nada aplicable, y hay que poder decirlo.** El capítulo entero va de soluciones
intravenosas: dextrosa al 50 %, lípido al 20 %, aminoácidos al 8,5 %, osmolaridades,
catéteres y compatibilidad de fármacos. No hay ni un requisito de un alimento.
Lo único que roza el catálogo es una advertencia de dosis de traza que el motor ya
cubre por otra vía: «PN solutions containing **2 mg zinc and 0.2 mg copper/100 kcal**
RER approximate the patient's needs» — 20 mg de zinc y 2 de cobre por 1000 kcal, que
está en el orden de los mínimos de FEDIAF y muy por debajo de sus máximos.

### cap.27 — Obesity (5.024 lineas, LEIDO ENTERO)

**El capítulo más largo del libro hasta aquí, y su relación con el motor es indirecta
pero real: Rawku pregunta el `peso_objetivo_kg` y escala los mínimos con él.**

1. **DE DÓNDE SALE UN «PESO OBJETIVO», con la fórmula.** El motor pide ese campo y
   `verificar.minimo_de()` escala con él, pero el repo no dice en ninguna parte cómo
   se calcula. SACN5 lo da entero (Box 27-3, Tabla 3): **«Ideal weight = current
   weight x (100 - percent body fat [%BF]) ÷ 0.80»**, con el %BF estimado de la
   condición corporal — «**%BF changes by roughly 10 % for each change in BCS on a
   5-point scale**», con el 3/5 en 20 %, el 4/5 en 30 % y el 5/5 en 40 % o más. La
   Tabla 27-3 es esa cuenta ya hecha, de 2 a 73 kg. **No es una cifra que el motor
   deba aplicar** —el peso objetivo lo pone quien rellena la ficha—, pero es la
   respuesta a «¿y ese número de dónde lo saco?», y hoy la app no la da. **Decisión
   de producto, de Elena**, y va a `PENDIENTE_PRODUCTO.md`.

2. **La velocidad segura de adelgazar, que el motor YA dice en un aviso.**
   `patologias.json` lleva un aviso suelto de «un perro adelgaza 1-2 % a la semana»
   que vigila el BLOQUE 64. Confirmado literal y con su porqué: «**Studies in people
   indicate that loss of more than 2 % of body weight per week is unhealthy**» y «**A
   greater proportion of lean body mass is lost when more than 2 % of body weight is
   lost per week**». Y el otro extremo, que el aviso no dice: «a rate of loss of at
   least **0.5 % of the initial body weight per week** is needed to maintain owner
   interest and complete the weight-reduction program within a reasonable period».
   El rango del libro para el perro es **1 a 2 % semanal**, con el 0,5 % como suelo
   aceptable.

3. **⚠️ Y LA VITAMINA E OTRA VEZ, QUE ES EL QUINTO SITIO.** `HALLAZGOS_SACN5_10SEP.md`
   ya dice que SACN5 pide cuatro veces la vitamina E que damos al perro sano, en
   cinco capítulos distintos. Este es uno de ellos, con su cifra propia: los alimentos
   de adelgazamiento del perro deben llevar **≥400 UI/kg MS** = 100 UI/1000 kcal =
   **67,1 mg/1000 kcal** al factor 0,671 del tocoferol natural. El mínimo de FEDIAF
   para el adulto son **6,968**. Diez veces. Y la fila de al lado repite el selenio
   **0,5-1,3 mg/kg MS** (125-325 µg/1000 kcal), que se sale por arriba del **máximo
   legal de 142** que aplica el motor — el mismo choque que ya está escrito en
   `requisitos_condicionales.json` para el perro de trabajo y en
   `PARA_EL_NUTRICIONISTA.md` como una sola pregunta.

4. **Las dos cifras del perro sano que SÍ coinciden con lo que ya aplicamos.**
   Tabla 27-4, alimentos de adelgazamiento para perro: **sodio 0,2-0,4 %MS** =
   500-1000 mg/1000 kcal y **fósforo 0,4-0,8 %MS** = 1000-2000 mg/1000 kcal. Los dos
   techos —1000 de sodio y 2000 de fósforo— son **exactamente** los que
   `recomendaciones_libro.json` aplica al adulto sano desde el 8 de septiembre,
   sacados de las Tablas 13-3 y 14-2. Que el capítulo de la obesidad llegue al mismo
   número por su cuenta, y con su propio motivo escrito («because they may be fed
   weight-management foods for extended periods of time, and subclinical renal
   disease is relatively common»), es la confirmación que faltaba.

5. **Lo demás del capítulo NO se puede aplicar a un BARF, y conviene decir por qué**:
   las cifras de adelgazamiento del perro son **fibra 12-25 %MS**, **hidratos ≤40 %**
   y **grasa ≤9 %**. Una ración cruda no lleva ni fibra ni hidratos en esas
   cantidades, y su grasa está muy por encima. El mecanismo que persiguen esas tres
   cifras —diluir calorías y dar saciedad— **no es un requisito nutricional**: es una
   forma de fabricar pienso. Lo que sí es traspasable es el principio, y el libro lo
   dice claro: «**The goal of a weight-management food should be to restrict only
   energy, not other nutrients**» — que es literalmente lo que hace este motor cuando
   se le baja el DER, porque los mínimos escalan hacia arriba.
   Y una que **no se aplica y es interesante**: **lisina ≥1,7 %MS** = 4,25 g/1000 kcal
   en alimentos de adelgazamiento, contra el mínimo de FEDIAF de 1,22 en adulto. El
   motivo es proteger la masa magra, y el libro lo mide: los perros con la lisina
   optimizada perdieron más peso (-2,1 kg contra -1,3) y **ganaron masa magra en vez
   de perderla** (+0,3 kg contra -1,1). Un BARF va muy por encima de 4,25 sin
   proponérselo, así que aplicarlo no cambiaría nada — pero queda medido.
   · **L-carnitina ≥300 ppm MS** (75 mg/1000 kcal) para el perro: no está en FEDIAF,
     no está en el catálogo y no se puede aplicar sin dato.

6. **Y el dato que más pesa para el producto, porque cambia el mensaje y no el
   número**: «**In a lifelong study of two groups of Labrador retriever dogs, the
   treatment group was fed 25 % less than the control group**», y el de control acabo
   con sobrepeso moderado: «**The median lifespan of the leaner group was 13.0 years
   compared to 11.2 years for the moderately overweight dogs**». Y de la artrosis:
   «**the mean age at which 50 % of dogs required long-term treatment for
   osteoarthritis was significantly younger (10.3 years)**» que en los de condicion
   normal, donde fueron 13,3 años.
   Casi dos años de vida y tres de articulaciones sanas, por un sobrepeso **moderado**.

### cap.28 — Disorders of Lipid Metabolism (1.158 lineas, LEIDO ENTERO)

**Este capitulo YA esta aplicado, y el releerlo entero lo confirma sin cambiar
nada.** `patologias.json` lleva desde el 6 y el 7 de septiembre el tope de grasa y el
suelo de fibra de la hiperlipidemia, los dos de aqui:
· **Grasa ≤30 g/1000 kcal**, de «**Restrict dietary fat (<12% dry matter [DM])**»
  (Tabla 28-2) × 2,5. Confirmado literal.
· **Fibra ≥25 g/1000 kcal**, de «**fiber levels of at least 10% DM are recommended
  for dogs**». Confirmado literal, y confirmada tambien la salvedad que el propio
  campo `por_que` del JSON ya recoge: «**no studies have been done in animals to
  evaluate the effects of dietary fiber type or amount on reducing serum triglyceride
  levels**». Es decir, la cifra que aplicamos viene declarada por la fuente como una
  recomendacion practica y no como una dosis-respuesta medida — y eso ya estaba
  escrito.

**Lo que el capitulo dice y nuestro aviso NO dice**, y son dos cosas que un dueño
querria saber:
1. **La dieta no siempre basta, y hay cifra**: «**up to 10 % of dogs with idiopathic
   hyperlipidemia are unresponsive to dietary fat restriction and may require
   pharmacologic supplementation**». Nuestro aviso ya manda al veterinario si no
   baja, pero no dice que a uno de cada diez no le va a bajar por dieta.
2. **Y un aviso de seguridad del otro lado**: «**Patients that lose a significant
   amount of weight (more than 1 % of body weight per week) should receive gradually
   increasing amounts of the recommended food**». Bajar la grasa a 30 g/1000 kcal
   baja la densidad del menu, y si el perro adelgaza mas del 1 % semanal sin quererlo,
   hay que darle mas. Eso no lo dice el aviso de hiperlipidemia. **Candidato a aviso
   nuevo, decision de Elena.**

Y el objetivo clinico, para que quien firma sepa contra que se mide: «**The goals of
dietary therapy are to achieve: 1) a clear serum sample, 2) a total triglyceride
concentration less than 500 mg/dl**».

### cap.29 — Endocrine Disorders (2.705 lineas, LEIDO ENTERO)

**Diabetes, hipertiroidismo felino e hipotiroidismo canino. Aqui SI aparece un hueco,
y esta medido.**

1. **⚠️ DE LA TABLA 29-3 APLICAMOS UNA FILA DE TRES, Y LAS OTRAS DOS NO CUADRAN CON
   UN BARF.** El motor toma de esa tabla el suelo de fibra de la diabetes (17,5
   g/1000 kcal, extremo bajo del «Fiber 7 to 18%»), y el propio JSON dice que se
   añadio al verificar la tabla entera y ver que el motor solo aplicaba una fila de
   ella (son palabras nuestras, no de la fuente). Pero la columna del perro tiene **cinco** filas y solo se aplico una. Las
   dos que faltan, convertidas con el ×2,5 de siempre:
   · **Grasa <25 %MS = <62,5 g/1000 kcal**, sin condiciones. El motor solo aplica un
     tope de grasa en diabetes **si ademas hay pancreatitis o hipertrigliceridemia**
     (30 % de las kcal, de Purina).
   · **Proteina 15-35 %MS = 37,5-87,5 g/1000 kcal**. Es un **TECHO de proteina**, y el
     motor no aplica ninguno en diabetes.
   **MEDIDO EN VIVO, 10 de septiembre**, resolviendo con el motor y el catalogo
   reales, `patologias=["diabetes"]`, adulto, cuatro pesos (5, 12, 22 y 35 kg) y tres
   semillas cada uno, doce menus:

   | | minimo | maximo | techo de la Tabla 29-3 |
   |---|---|---|---|
   | Proteina g/1000 kcal | 92,6 | 111,5 | **87,5** |
   | Grasa g/1000 kcal | 58,4 | 69,9 | **62,5** |

   **Doce de doce se pasan del techo de proteina. Nueve de doce se pasan del de
   grasa.**

   **Y HAY UN ARGUMENTO SERIO PARA NO APLICARLOS, que es justo por lo que esto es
   decision de Elena y no mia.** La columna se titula, en dos lineas, «Dogs (increased-fiber/» + «high-carbohydrate
   food)»: describe **un tipo de alimento** —pienso con fibra y
   cereal— que no es lo que hace este motor. Sus 15-35 %MS de proteina son el rango de
   un alimento cuyo grueso calorico son hidratos; una racion cruda no tiene de donde
   sacar esas calorias mas que de proteina y grasa. Aplicar ese techo a un BARF es la
   misma categoria de error que aplicarle la fibra del 12-25 %MS del capitulo de la
   obesidad. **Pero entonces la fila de fibra que SI aplicamos viene de esa misma
   columna**, y eso es lo que hay que resolver: o la columna vale para nosotros o no
   vale, y hoy vale a medias sin que este escrito por que.
   Lo que la fuente **no** dice en ninguna parte es que 35 %MS sea un maximo de
   seguridad: la unica nota de esa fila es «**Dogs with renal failure should be fed
   protein at the low end of the range**». Va a `PENDIENTE_NUTRICION.md`.

2. **El hipotiroidismo tiene una cifra de energia que el motor no usa porque no
   calcula el DER**, pero que la app si podria: «**energy expenditure, as measured by
   indirect calorimetry, was approximately 15 % lower in hypothyroid dogs, compared
   with healthy dogs**», y vuelve a la normalidad con levotiroxina. Un perro
   hipotiroideo **sin tratar** necesita un 15 % menos de kcal, y hoy Rawku le da las
   mismas que a uno sano. Es exactamente el mismo tipo de cruce pendiente que la
   Tabla 33-8 y la 15-6. **Decision de producto.**

3. **⚠️ Y LA TABLA 29-11 LISTA UN ALIMENTO DEL CATALOGO QUE NO EXCLUIMOS.** Nuestro
   aviso de hipotiroidismo quita el grelo y el nabo y explica por que deja el brocoli,
   la coliflor y las coles. La Tabla 29-11 de SACN5, «Goitrogenic factors in foods and
   the environment», lista once alimentos y entre ellos **«Sweet potatoes»** y
   **«Seaweed»**. **El catalogo tiene BONIATO** (y no tiene algas). Nadie lo ha mirado.
   ⚠️ Con el matiz que hay que decir y que la propia tabla escribe en su pie:
   «**Epidemiologic associations and risk factors**» — son asociaciones, no umbrales
   con dosis. La tabla tampoco da cantidad para ninguno de los once. Asi que **esto no
   es una cifra aplicable**: es una pregunta para el nutricionista, y va a
   `PREGUNTAS_ABIERTAS.md`. Lo que no se puede es no haberlo mirado.

4. **Lo que confirma sin cambiar nada**: el aviso de diabetes dice que lo importante
   es la regularidad y que se quita la fruta. El capitulo lo respalda entero:
   «**Foods and snacks containing simple sugars rapidly increase blood glucose
   concentration and should be avoided for diabetic dogs and cats**», y sobre el
   reparto de las comidas, «**several small meals given at regular intervals
   throughout the day with and following insulin administration result in minimal
   hyperglycemia**».

5. **Todo lo del hipertiroidismo es FELINO** y se dice: «hyperthyroidism is uncommon
   in dogs», y cuando sale en un perro casi siempre es un carcinoma, no la hiperplasia
   del gato. Su Tabla 29-12 no aplica. Lo unico canino de ese bloque es un dato de
   catalogo que conviene tener: el Box 29-3 mide el yodo de los alimentos comerciales
   de EE. UU. y sale que «**I concentrations in U.S. dog foods ranged from 0.8 to
   196.8 mg/kg**» — un factor 250 entre el mas bajo y el mas alto. Es el mismo
   argumento por el que el motor aplica un techo de yodo propio y no se fia de que
   «un alimento completo ya lo trae».

### cap.30 — Cancer (2.146 lineas, LEIDO ENTERO)

**Este capitulo es una CONFIRMACION, no un hallazgo, y eso tambien hay que
escribirlo.** La Tabla 30-5 se leyo entera el 8 de septiembre (fue la que se
habia perdido al cortar el barrido con `sed`, ver `VERIFICACION_FILA_A_FILA.md`
§cuarta pasada) y `patologias.json` ya aplica lo que se puede aplicar de ella y
declara por escrito lo que no. Leido el capitulo completo, **no aparece ni una
cifra canina mas** que la tabla no traiga. Lo que sigue es lo que se ha
comprobado al releerlo.

1. **La Tabla 30-5, releida celda a celda.** No se transcribe entrecomillada
   porque sus etiquetas de fila se parten al extraer el texto y la columna de al
   lado se cuela en medio — pegarlas seria escribir una frase que el libro no
   dice. En prosa, y para el PERRO: carbohidrato digestible (NFE) **≤25 % de
   materia seca** o <20 % de las kcal; grasa **25-40 % MS** o 50-65 % de las
   kcal; omega-3 **>5 % MS**; ratio omega-6:omega-3 **lo mas cerca de 1:1 que se
   pueda**; proteina **30-45 % MS** o 25-40 % de las kcal; arginina **>2 % MS**.
   El texto corrido de SACN5 cap.30 repite las tres primeras con decimal y sin
   forma de tabla: «Currently, recommendations for canine and feline cancer
   patients continue to be focused on foods with increased fat calories (25 to
   40% DM fat)».
   Lo que el motor hace hoy con cada una: grasa **suelo 62,5 g/1000 kcal**
   (el 25 % MS x 2,5) — la unica patologia del motor que pide MAS grasa;
   proteina **suelo 75**; arginina **suelo 5** (el 2 % MS); y el omega-3 de
   12,5 **escrito y no aplicado**, con la medida de por que no cabe en
   `limites_escritos_que_el_solver_no_aplica`. El NFE y el ratio omega-6:omega-3
   van declarados como no modelables en los avisos.

2. **La arginina, con el porque de que sea «>2 %» y no otra cosa.** SACN5 cap.30
   lo dice sin esconderlo: «The minimum effective level of dietary arginine for
   cancer patients is unknown; however, based on work in other species, it is
   thought appropriate to provide more than 2% DM arginine in foods for dogs with
   cancer.» O sea que el 2 % es una extrapolacion declarada, no un ensayo canino.
   El motor lo aplica igual —es un suelo, y por encima del minimo de FEDIAF—,
   pero conviene que quien firme una pauta sepa de donde sale.

3. **⚠️ EL CAPITULO CONFIRMA UNA DECISION DEL MOTOR QUE NADIE HABIA COMPROBADO:
   el cancer NO cambia el DER.** Rawku calcula las kcal igual con cancer marcado
   que sin el, y eso hasta hoy era una omision, no una decision. SACN5 cap.30 la
   respalda con los estudios de calorimetria indirecta: «dogs with cancer and no
   evidence of weight loss do not have energy requirements higher than those of
   apparently healthy dogs without cancer». Lo que si cambia es el perro que **ya
   ha perdido peso**, y ahi el libro no da un factor de enfermedad sino el de
   siempre: en SACN5 cap.30, «the DER factor typically ranges from low activity
   (1.1 to 1.3 x RER) to adult maintenance (1.4 x RER for cats and 1.6 x RER for
   dogs)» — que esta dentro de los escalones de actividad que ya usa el motor.
   Queda como decision escrita: **el cancer no toca el DER, y ahora se sabe por
   que**.

4. **Los cuatro recuadros (30-2 a 30-5) no dan ni una cifra aplicable, y la
   fuente lo dice ella misma.** Aminoacidos, vitaminas, minerales y alimentos
   novedosos ocupan cuatro paginas de mecanismo —glutamina, retinoides, vitamina
   C, vitamina E, selenio, hierro, zinc— y ninguno llega a un numero para el
   perro. La frase que lo cierra, en SACN5 cap.30: «cancer prevention and
   treatment have not been established for pet animals». Importa por contraste:
   la vitamina E del perro sano si tiene cifra en cinco capitulos distintos
   (`HALLAZGOS_SACN5_10SEP.md`) y **aqui no**, asi que el cancer no anade nada al
   caso de la vitamina E. La glutamina aparece otra vez —como en el cap.25— y
   sigue sin estar en la Tabla III-3b de FEDIAF ni en el catalogo: no hay nada
   que aplicar.

5. **Las tres contraindicaciones ya estan puestas y se confirman.** El aviso de
   `cancer_soporte` nombra las tres que trae el capitulo (intolerancia previa a
   la grasa, perro con sobrepeso, insuficiencia renal o hepatica) y la frase de
   cabecera de que un cambio de dieta no esta indicado en todo perro con cancer.
   Releidas las tres en su sitio: dicen lo que el aviso dice.

### cap.31 — Adverse Reactions to Food (2.597 lineas, LEIDO ENTERO)

**La Tabla 31-3 ya estaba aplicada entera** (`reaccion_adversa_alimento`: omega-3
0,875 de suelo, fosforo 2000 y sodio 1000 de techo, la proteina de 55 escrita y
no aplicada por el parentesis «dermatologic cases only», el atun y la caballa
fuera por `restricciones_patologia`). Lo que sigue es lo que **solo aparece en el
texto corrido** y no tiene forma de tabla, que es justo lo que el contador de
`leer_sacn5.py` no puede encontrar.

1. **⚠️ LA REACTIVIDAD CRUZADA, Y UN HUECO MEDIDO EN `exclusiones.py`.** El
   capitulo nombra los alergenos caninos identificados uno a uno, en SACN5
   cap.31: «bovine IgG (cow's milk, beef), ovine IgG (lamb), muscle
   phosphoglucomutase (beef, lamb) and Gly proteins 50 and 75 kD (soy)». Dos de
   esos cruzan lineas que nuestras familias **no** cruzan:
   · la **IgG bovina** es la misma en la leche de vaca y en la carne de vaca;
   · la **fosfoglucomutasa muscular** es la misma en la vaca y en el cordero.
   Y lo repite por el lado de la leche: «Cross reactivity between milk proteins
   from cows, goats and sheep is common.»
   **MEDIDO contra el catalogo de hoy**, con `expandir_exclusiones`:
       marcar «ternera» quita 19 alimentos y **deja dentro** el Yogur griego
       (IgG bovina) y los **7 de cordero** (fosfoglucomutasa)
       marcar «lacteo»  quita 1 (el Yogur griego) y deja los 19 de vaca
   O sea que un perro con alergia a la vaca diagnosticada puede recibir yogur y
   cordero. **NO SE TOCA AQUI**: la regla 4 dice que las alergias no se tocan
   jamas, y ampliar una familia es una decision clinica, no una correccion —
   ampliar de mas quita alimentos utiles a quien no los necesita. Queda como
   **decision de Elena**, con la cita y la medida delante.
   Y lo que el codigo ya hace bien, confirmado por la misma pagina: **no** meter
   el huevo en la familia de las aves (el capitulo los trata como alergenos
   distintos y solo cruza el huevo con «egg proteins of other birds»), y **no**
   agrupar las legumbres, porque el cruce entre ellas «is very rare». Los
   cereales cruzan entre si — «Wheat, rye and barley cross react in allergic
   people, but oat allergens appear to cross react only weakly» — y eso hoy no
   afecta: en el catalogo no hay ni trigo ni cebada ni centeno ni avena.

2. **⚠️ Y AQUI ESTA LA FUENTE QUE LE FALTABA A UNA REGLA DEL MOTOR.** El matiz 2
   de la regla 5 de `CLAUDE.md` dice que Suplementos y Extras van **siempre
   libres**, y hasta hoy eso era criterio nuestro sin respaldo escrito. SACN5
   cap.31 lo dice tal cual, y precisamente en el capitulo de las alergias:
   «Non-flavored vitamin and mineral supplements are not perceived as causes of
   adverse food reactions.» Con la condicion que lo acompana y que conviene leer:
   «Additive-free supplements that do not contain animal or vegetable proteins
   are unlikely to be sources of ingested allergens.» O sea: sin sabor anadido y
   sin proteina dentro. Y de los aceites, lo mismo: «Vegetable oils are not a
   routine source of ingested allergens», con el dato de que los alergicos al
   cacahuete y a la soja toleran su aceite. Nuestro filtro por palabras quita el
   «Aceite de cacahuete» a quien marque cacahuete, o sea que **es mas estricto
   que la fuente** — y se queda asi: la regla 4 solo permite apretar.

3. **La razon de ser de este motor, escrita por la fuente y en su contra.** El
   capitulo revisa las dietas caseras de eliminacion que recomiendan los
   dermatologos: «Most of the homemade foods recommended in the AAVD survey for
   initial management of dogs and cats with suspected food allergy were
   nutritionally inadequate for growth or adult maintenance», y el porque:
   «In general, homemade foods lack a source of calcium, essential fatty acids,
   certain vitamins and other micronutrients and contain excessive levels of
   protein, which are contraindicated in food allergy cases.» Con el numero:
   «Many previously recommended homemade elimination foods have a severe inverse
   calcium-to-phosphorus ratio of 1:10.» Y el plazo: no mas de tres semanas, con
   enfermedad esqueletica en el cachorro en cuatro. **No es una critica a la
   comida casera: es la descripcion exacta del problema que resuelve un
   solver** — cerrar los 43 requisitos a la vez en vez de juntar dos
   ingredientes. Vale para `PARA_EL_NUTRICIONISTA.md` mejor que cualquier frase
   nuestra.

4. **Los plazos de la prueba de eliminacion, que los avisos de hoy no llevan.**
   `reaccion_adversa_alimento` tiene ya el aviso de la reintroduccion (con la
   cita de FEDIAF) y el de que el omega-3 puede confundir la fase de
   diagnostico, pero ninguno dice **cuanto dura**. SACN5 cap.31 lo cuantifica:
   «The patient is then fed a controlled elimination food for six to 12 weeks»
   en piel, dos a cuatro semanas en aparato digestivo, y a la reintroduccion
   «A return of GI signs after challenge with the responsible allergen will
   usually occur within the first three days, but may take as long as seven
   days». **Propuesta apuntada, no aplicada**: son cifras de manejo clinico y
   anadirlas a un aviso es cambiar lo que la app le dice al dueno.

5. **Y una cifra suelta que no obliga a nada hoy**: la lactosa. «One study showed
   that adult dogs were able to use up to 1 g of lactose/kg body weight/day»,
   que el libro traduce a 20-22 ml/kg de leche de vaca o de cabra. El unico
   lacteo del catalogo es el Yogur griego, que lleva poca lactosa y entra en
   cantidades pequenas: no hay tope que poner. Queda escrito por si algun dia
   entra leche.

### cap.32 — Skin and Hair Disorders (2.987 lineas, LEIDO ENTERO)

**Las dos tablas de cifras ya estaban aplicadas**: la 32-1 en `dermatosis_zinc`
(zinc 25 de suelo, fenilalanina+tirosina 3,25) y la 32-6 en `dermatitis_atopica`
(omega-3 0,875, el mismo rango que la Tabla 31-3). Lo que sale de leer el
capitulo entero son **tres cosas que estan en el texto y en los recuadros, no en
las tablas**, y las tres se han medido.

1. **⚠️ EL RECUADRO 32-2 PIDE MAS FENILALANINA+TIROSINA QUE LA TABLA, Y NO ES UNA
   ERRATA.** El motor aplica 3,25 g/1000 kcal, que es el «>1.3% DM» de la Tabla
   32-1. El recuadro «Red Coat Syndrome», en el mismo capitulo, da otra cifra para
   la misma cosa: en SACN5 cap.32, «Dietary phenylalanine plus tyrosine levels
   greater than 2% dry matter or addition of L-tyrosine to the food should provide
   optimal amino acid levels for maximal melanin synthesis in cats and dogs» —
   **2 % MS = 5,0 g/1000 kcal**, un 54 % mas. Las dos cifras no dicen lo mismo: la
   tabla da el suelo para que no falte, y el recuadro el que hace falta para la
   sintesis **maxima** de melanina, que es lo que decide si un pelo negro se
   vuelve rojizo.
   **MEDIDO sobre los 36 menus del catalogo**: van de **5,32 a 11,41 g/1000 kcal**
   (mediana 8,08). **Los 36 pasan las dos cifras**, la de la tabla y la del
   recuadro, sin que haya que aplicar nada. Una racion cruda va sobrada de
   aromaticos porque va sobrada de proteina. Queda escrito: no se aplica **porque
   no hace falta**, no porque no se haya visto.

2. **⚠️ EL CALCIO ESTORBA AL ZINC, Y ESTE MOTOR HACE RACIONES ALTAS EN CALCIO.**
   Es el hallazgo del capitulo y no tiene forma de fila. La Tabla 32-4 lista como
   factor de riesgo de dermatosis por zinc los alimentos con «High mineral levels
   (calcium, phosphorus, magnesium)», el texto lo explica —«Foods high in calcium,
   phosphorus and magnesium adversely affect absorption of zinc» y «high levels of
   minerals such as calcium inhibit the absorption of nutrients such as zinc,
   which are essential for normal, healthy skin»— y la Tabla 32-1 pone el umbral:
   «Higher levels of zinc are required in foods with calcium >1.5% DM», con la
   misma frase para el cobre. Y avisa de quien mas riesgo tiene, que es
   exactamente nuestro caso: «Excessive use of mineral supplements containing
   calcium in large- and giant-breed puppies is common and can inhibit zinc
   absorption».
   **MEDIDO sobre los 36 menus** (calcio en %MS por el puente de siempre, %MS x
   2500 = mg/1000 kcal):
       calcio 0,63 a 1,64 % MS, mediana 1,48
       **17 de 36 por encima del 1,5 % MS** — y los 17 son de crecimiento,
       gestacion o lactancia; **ninguno** de adulto o senior (el mayor, 0,97)
   O sea que el umbral de la fuente lo cruza justo la poblacion que ella misma
   senala. **Y la buena noticia, tambien medida**: en esos 17 menus el zinc va de
   **27,3 a 47,0** mg/1000 kcal —dentro del rango 25-50 que pide la Tabla 32-1
   para el perro— y el cobre de **2,79 a 7,00**, por encima de su 1,25-2,5. O sea
   que **la compensacion que pide la fuente ya esta puesta**, no por diseno sino
   porque una racion cruda con visceras va sobrada de los dos. **No se cambia
   nada**, y ahora se sabe por que — hasta hoy era suerte sin medir.

3. **La dosis de omega-3 en mg por kg de perro, que es otra unidad y cuadra.** La
   Tabla 32-6 y el texto dan la misma recomendacion por dos caminos: «An initial
   dose of 50 to 300 mg of total omega-3 fatty acids/kg body
   weight/day seems to be effective in a large number of studies» y «As a food amount, this dose range translates to approximately
   0.35 to 1.8% total omega-3 fatty acids (DM).» El motor aplica el extremo bajo
   del segundo (0,875 g/1000 kcal) y nunca habia comprobado el primero. **Cuadra**:
   el perro de 10 kg del propio capitulo come 600 kcal, y 0,875 x 0,6 = 525 mg,
   o sea **52,5 mg/kg/dia** — justo por encima del suelo de 50. Es la unica cifra
   del motor que se puede verificar en dos unidades distintas de la misma fuente.

4. **El cobre, tercera confirmacion de algo que ya esta en
   `sacn5_fuentes_de_minerales.json`.** El capitulo repite lo del cap.6: «copper
   from monogastric mammalian liver (pork and rat) and copper oxide is poorly
   available», y del otro lado «Copper availability is relatively high in poultry
   by-product meal, avian liver (chicken and turkey) and ruminant liver (beef and
   sheep)». Los higados del catalogo son de pavo, pollo, vaca y cordero: los
   cuatro de la lista buena. Sigue sin haber ninguno de cerdo.

5. **La vitamina E, SEXTO capitulo que pide 400 UI/kg MS.** En SACN5 cap.32, «vitamin E in foods is
   at least 400 IU/kg of food (DM) for dogs and at least 500 IU/kg of food (DM)
   for cats» — los mismos 67 mg/1000 kcal de los capitulos 1, 7, 27, 34, 35 y 47 que
   ya estan medidos en `HALLAZGOS_SACN5_10SEP.md` §S-12. Sigue sin aplicarse y por
   el mismo motivo: subir un minimo diez veces cambia que alimentos entran en
   todos los menus, y eso lo decide el nutricionista. Lo que este capitulo anade es
   el contexto — la piel es el organo mas expuesto al oxidante — y una dosis
   TERAPEUTICA que no es de alimento y no toca al motor: 200 a 800 UI dos veces al
   dia por boca, para lupus discoide, paniculitis esteril y dermatomiositis.

6. **Y lo que hay que poder decirle al dueno cuando pregunte si el aceite le va a
   arreglar el picor.** SACN5 cap.32 lo mide en 16 ensayos aleatorizados (Tabla
   32-10) y lo resume sin adornos: «up to 50% of dogs with allergic pruritus will
   improve with modification in fatty acid intake, if secondary bacterial and yeast
   infections are controlled». La mitad, y solo si lo demas esta controlado. El
   aviso general de `dermatitis_atopica` no dice ninguna de las dos cosas.
   **Propuesta apuntada, no aplicada.**

### cap.33 — Developmental Orthopedic Disease of Dogs (2.358 lineas, LEIDO ENTERO)

**Es el capitulo del cachorro de raza grande, y el unico del libro que ya estaba
trabajado a fondo antes de esta relectura**: sus elementos tienen veredicto uno a
uno en `lecturas_sacn5.json` y de el salen cuatro hallazgos ya escritos en
`HALLAZGOS_SACN5_10SEP.md` — la escalera de energia de crecimiento (S-17), el
Ca:P de la Tabla 17-1 contra el de la 33-5 (S-18), la proteina del cachorro
(S-19) y el techo de grasa que no es lo que parece (S-25). **Aqui no se repiten.**
Lo que sale de leerlo entero, de la primera linea a la ultima, son **dos cosas
nuevas y dos confirmaciones**, y una de las dos nuevas es una correccion de algo
que este repo tenia escrito y era falso.

1. **⚠️ EL SUELO DEL RATIO Ca:P, QUE NADIE HABIA MIRADO — Y ESTE SI DEJA PASAR
   MENUS REALES.** S-18 discutio el **techo** del ratio (1,5 de la Tabla 17-1
   contra el 1,6/1,8 de FEDIAF que aplicamos). El **suelo** no se miro, y las dos
   tablas coinciden en el: la celda de la Tabla 33-5 dice «1.1:1 to 2:1 (the lower
   end of range is preferred)» y el texto lo repite al hilo del calcio — «When
   calcium intake is set at 0.8 to 1.2% DM of the food, as recommended previously
   for large breeds at risk for DOD, the calcium-phosphorus ratio should be kept
   within physiologic limits (1.1:1 to 2:1)». El motor aplica el suelo de FEDIAF,
   que es **1,0**, y no distingue raza.
   **MEDIDO sobre los 12 menus de cachorro del catalogo**: el ratio va de 1,020 a
   1,385, y **dos caen por debajo de 1,1** — `Grande_CachorroJoven` en **1,020** y
   `Gigante_CachorroJoven` en **1,030**. Los dos son crecimiento temprano de raza
   grande o gigante, que es exactamente la poblacion de este capitulo.
   Y eso lo distingue del techo de 1,6, donde 0 de 32 menus caian en la ventana:
   **aqui el hueco de la regla esta produciendo menus por debajo del suelo de la
   fuente**. **Decision de Elena**, porque subir el suelo a 1,1 solo para el
   cachorro de mas de 25 kg de peso adulto es tocar el solver y hay que medir antes
   si sigue habiendo menu en el peldano 0.

2. **⚠️ CORRECCION: EL DHA POR SEPARADO NO ESTA APLICADO, Y EL REPO DECIA QUE SI.**
   El veredicto de `cifra#308` en `lecturas_sacn5.json` decia «DHA >=0,02 % MS. Ya
   aplicado», y es **falso**: el `MAPA` de `verificar.py` tiene `EPA_DHA_total` (la
   suma) y `EPA` (que existe solo para el suelo de la artrosis), y **no tiene una
   fila de DHA**. Lo que estaba aplicado es la suma, que es otra cosa. Corregido en
   el mismo commit.
   Lo que pide la fuente, literal: «The minimum recommended allowance for DHA plus
   eicosapentaenoic acid (EPA) is 0.05% (DM) with EPA not exceeding 60% of the
   total (NRC, 2006). Thus, DHA needs to be at least 40% of the total DHA plus EPA,
   or 0.02% (DM).» O sea **DHA sola, minimo 0,05 g/1000 kcal y al menos el 40 % de
   la suma**. Aritmeticamente un menu puede cumplir los 0,13 g de EPA+DHA que exige
   FEDIAF en crecimiento **con EPA sola y cero DHA**, y salir verde. Y no es
   intercambiable: el DHA se pide para el desarrollo neural, retiniano y auditivo,
   y «The conversion of short-chain polyunsaturated fatty acids to DHA is an
   inefficient process in puppies».
   **MEDIDO sobre los 12 menus de cachorro**: el DHA va de **0,081 a 1,324**
   g/1000 kcal (los 12 por encima de 0,05) y supone del **54,4 % al 75,0 %** de la
   suma (los 12 por encima del 40 %). O sea que el hueco esta en las reglas y no en
   los menus, y la razon es del catalogo: el omega-3 de aqui viene del pescado, que
   es rico en DHA. **Apuntado, no aplicado** — pero ahora dice la verdad.

3. **La vitamina D: el tope de seguridad cronica del motor sale CLAVADO por otra
   puerta.** `seguridad.py` aplica `TOPE_VITD_KCAL = 20,0 µg/1000 kcal` citando al
   NRC 2006. Este capitulo lo da en la otra unidad: «The safe upper limit is 3,200
   IU/kg (DM) (NRC, 2006).» A 4000 kcal/kg MS son 800 UI/1000 kcal, y a 40 UI por
   µg, **20 µg/1000 kcal**. Exacto, por un camino distinto y en un capitulo
   distinto. Y trae medido lo que pasa al pasarse: 135 veces la dosis recomendada
   en cachorros de gran danes no subio el calcio ni el fosforo en plasma, y aun asi
   produjo osteocondrosis y sindrome de radius curvus.

4. **La proteina alta NO es factor de riesgo, y esto hay que poder decirlo.** Es
   la duda que mas se repite con una racion cruda de cachorro, que lleva ~134 g de
   proteina por 1000 kcal. SACN5 cap.33, literal: «Protein excess has not been
   shown to negatively affect health or skeletal development during growth of Great
   Dane puppies when compared with isoenergetically fed controls». Y el caso
   clinico 33-3 lo cuenta en vivo: el dueno cambio de comida porque el club de
   perros culpo a la proteina, y lo que sobraba era energia y calcio. Confirma que
   el motor hace bien en no poner techo de proteina en crecimiento, y es una frase
   para `PARA_EL_NUTRICIONISTA.md`.

5. **Y una que hay que leer con cuidado antes de copiarla.** El recuadro 33-5 va
   contra los suplementos de calcio y no se anda con rodeos: «Because virtually all
   dog foods contain more calcium than is needed to meet the requirement, the use
   of a calcium supplement certainly is unnecessary.» **Eso vale para un pienso
   completo, no para una racion cruda**, donde el hueso o la cascara de huevo SON
   la fuente de calcio y sin ellos no se cierra el requisito. Lo que si traslada es
   la advertencia de detras, que es de cantidad y no de principio: dos cucharaditas
   de carbonato calcico anadidas a mano **doblan** la ingesta diaria de un
   rottweiler de 15 semanas. En Rawku el calcio lo pone el solver y no el dueno,
   con techo por 1000 kcal y con la dosis maxima del fabricante encima — que es
   justo la proteccion que el capitulo pide.

### cap.34 — Nutritional Management of Osteoarthritis (1.900 lineas, LEIDO ENTERO)

**La Tabla 34-2 ya estaba aplicada casi entera** en `artrosis`: EPA 1,0 de suelo,
L-carnitina 75, vitamina E 67,1, fosforo 1750 y sodio 1000 de techo, y los dos que
no caben —el omega-3 total de 8,75 y el ratio omega-6:omega-3 de <1:1— escritos en
`limites_escritos_que_el_solver_no_aplica`. Leerlo entero saca **un hallazgo nuevo
y medido**, y tres cosas que hay que dejar escritas porque no se pueden aplicar.

1. **⚠️ LA MISMA CIFRA EN LA OTRA UNIDAD NO CUADRA, Y FALLA JUSTO EN EL PERRO
   GRANDE.** El capitulo da su recomendacion de EPA por dos caminos. Por
   concentracion: «a food designed to aid in the management of osteoarthritis in
   dogs should provide levels of total omega-3 fatty acids between 3.5 to 4.0% DM
   and specifically 0.4 to 1.1% DM EPA». Y por **dosis**: «Dogs consuming the
   therapeutic food should receive an average of 50 to 100 mg EPA/kg body
   weight/day.» El motor aplica el extremo bajo del primero — 0,4 % MS x 2,5 =
   **1,0 g/1000 kcal** — y nunca habia comprobado el segundo.
   **No cuadra, y se puede calcular sin resolver nada**: con un suelo por 1000
   kcal, los mg de EPA por kilo de perro al dia son exactamente **DER/peso**, y ese
   cociente **baja con el tamano**. Medido sobre los doce perros de referencia del
   catalogo:
       Toy adulto (3 kg, 251 kcal) ......... **83,7** mg/kg/dia
       Mediano adulto (22 kg, 1117 kcal) ... **50,8**
       Mediano senior (22 kg, 1046 kcal) ... **47,5**  ← por debajo
       Grande senior (32 kg, 1386 kcal) .... **43,3**  ← por debajo
       Gigante senior (55 kg, 2080 kcal) ... **37,8**  ← un 24 % por debajo
   O sea que el suelo que aplicamos cae **por debajo de los 50 mg/kg/dia de la
   fuente en el perro mediano senior y en todos los grandes y gigantes**, que es
   exactamente la poblacion con artrosis. Y la solucion esta dentro del rango de la
   propia tabla: el extremo alto es 1,1 % MS = **2,75 g/1000 kcal**, y con **1,32**
   ya se llega a 50 mg/kg/dia hasta en el gigante senior. **Decision de Elena**,
   porque subir un suelo cambia que alimentos entran; pero la aritmetica no depende
   del solver y por eso se puede afirmar sin medir menus.
   Y por que EPA y no la suma, que ya estaba bien resuelto y este capitulo lo
   explica: «EPA was the only omega-3 fatty acid able to significantly decrease the
   oncostatin M-stimulated loss of aggrecan in the canine cartilage in vitro
   model».

2. **La vitamina C, que la tabla pide y este motor no puede pedir.** Tabla 34-2:
   «for improved antioxidant performance, and in conjunction with levels of vitamin
   E recommended above, foods for adult dogs and cats should contain at least 100
   mg vitamin C/kg DM» = **25 mg/1000 kcal**. No se aplica y **no es una decision
   pendiente**: el perro sintetiza su propia vitamina C, FEDIAF no la pone en la
   Tabla III-3b, y **el catalogo no tiene columna de vitamina C** en ninguna de sus
   163 fichas. Aplicarla exigiria un dato que no existe. Queda escrito para que no
   se «descubra» otra vez dentro de seis meses, que es para lo que sirve este
   documento.

3. **La glucosamina y la condroitina son TECHOS, no suelos, y el motivo no es
   clinico.** La Tabla 34-2 las pone en «≤0.10%» y «≤0.08%», y el texto dice de
   donde salen: no de un ensayo de eficacia, sino de un limite **regulatorio** de
   un estado de EE.UU. — «glucosamine HCl and chondroitin sulfate should not exceed
   0.10 and 0.08% DM, respectively». Ninguna de las dos esta en el catalogo y no
   hay nada que aplicar. Lo que si merece quedar escrito es el aviso del recuadro
   34-1 sobre los suplementos que la gente compra por su cuenta: «26 of 32 (81%)
   commercially available human products contained less than 90% of the chondroitin
   sulfate stated on the label». Ocho de cada diez botes traen menos de lo que
   ponen.

4. **Y una confirmacion de las que no cambian nada pero cierran una duda.** El
   techo de fosforo de 1750 y el de sodio de 1000 que aplicamos en `artrosis`
   llevan en la propia tabla el asterisco que explica que **no son de la artrosis**:
   son los del perro adulto mayor sano, por el riesgo renal y cardiaco de la edad,
   los mismos de los caps.13 y 14. Es la tercera indicacion del libro que repite
   esos dos numeros —con la reaccion adversa (Tabla 31-3) y la obesidad (Tabla
   27-4)—, y las tres coinciden con lo que `recomendaciones_libro.json` aplica al
   perro sano desde el 8 de septiembre. Cuatro tablas, un numero.

### cap.35 — Cognitive Dysfunction in Dogs (1.397 lineas, LEIDO ENTERO)

**Y aqui esta el hallazgo que justifica releer un libro que ya se habia
"leido".** La Tabla 35-3 se trabajo el 9 de septiembre y de sus seis filas el
motor aplica dos y declara tres. Leyendola entera, fila por fila y contra el
texto corrido, **una de las dos que aplica esta cogida de la fila de al lado**.

1. **⚠️ LA L-CARNITINA DE LA DISFUNCION COGNITIVA SALE DE LA FILA DEL ACIDO
   ALFA-LIPOICO. Es un salto de fila, exactamente el fallo que este repo lleva
   dias persiguiendo.** El JSON aplica **25,0 mg/1000 kcal** citando una frase que la fuente NO dice: "L-carnitine
   ... Provide foods with >=100 mg/kg". Va sin comillas angulares a proposito,
   porque no es una cita — es lo que el JSON escribio, y `auditar_citas.py` la
   marcaria como no encontrada, que es justo lo que es. La tabla dice otra cosa. Sus filas, en orden:
       Vitamin E ......... ≥750 mg/kg
       Vitamin C ......... ≥150 mg/kg
       Selenium .......... 0,5 a 1,3 mg/kg
       **L-carnitine ..... 250 a 750 IU/kg**
       **α-lipoic acid ... ≥100 mg/kg**
       Total omega-3 ..... >1 %
   O sea que **los ≥100 mg/kg son del acido alfa-lipoico**, que es otro nutriente
   y no esta en el catalogo. La L-carnitina de esta tabla son **250 a 750**.
   **Y el capitulo lo confirma DOS veces mas**, lo cual quita cualquier duda de
   que sea un artefacto de la extraccion: el texto corrido lo repite en una sola
   frase —«vitamin E = ≥750 mg/kg; vitamin C = ≥150 mg/kg; selenium = 0.5 to 1.3
   mg/kg; L-carnitine = 250 to 750 IU/kg; α-lipoic acid = ≥100 mg/kg»— y la Tabla
   35-4 pone el alimento comercial del ensayo con **299 mg/kg de L-carnitina**,
   que cae dentro de 250-750 y no tendria sentido si el requisito fueran 100.
   **Corregido en el mismo commit**: el suelo pasa de 25,0 a **62,5 mg/1000 kcal**
   (250 mg/kg MS / 4), y el acido alfa-lipoico entra en
   `limites_escritos_que_el_solver_no_aplica` con sus 25 mg/1000 kcal y el motivo
   —no hay columna de acido alfa-lipoico en ninguna de las 163 fichas—.
   ⚠️ **Y hay que decir lo que la fuente escribe mal**: pone «IU/kg» para la
   L-carnitina, y la L-carnitina **no tiene unidades internacionales**. Las otras
   dos apariciones de la cifra en el mismo capitulo la tratan como mg (la Tabla
   35-4 compara esos 250-750 con los 299 **mg/kg** del alimento real), asi que se
   lee como mg/kg de materia seca y **se deja escrito que la fuente pone otra
   unidad**. Lo que no se puede es copiar «IU» y hacer como si se hubiera
   convertido.
   **MEDIDO con el suelo nuevo puesto**: [se rellena con la medida]

2. **Que las otras cinco filas estaban bien, y merece decirlo.** La vitamina E
   (≥750 mg/kg = 187,5 mg/1000 kcal), la vitamina C (≥150 = 37,5) y el selenio
   (0,5-1,3 mg/kg = 125-325 µg) estan las tres escritas y **declaradas como no
   aplicadas**, cada una con su motivo medido: la vitamina E no cabe con el techo
   de fosforo del perro sano puesto, la vitamina C no es un nutriente de FEDIAF ni
   una columna del catalogo, y el selenio se sale por arriba del maximo legal de
   142 µg que aplica el motor. Y el omega-3 total de >1 % MS = 2,5 g/1000 kcal si
   se aplica. Cinco de seis correctas y una cogida de la fila de al lado: por eso
   el metodo no puede ser «tener mas cuidado».

3. **La septima fila, que no es una cifra y por una vez la cumplimos sin
   proponernoslo.** «Fruits and vegetables — 1% of each of five vegetable and
   fruit ingredients», y el texto anade que «No minimum or maximum effective
   levels for fruits and vegetables have been established». Una racion BARF de
   este motor lleva verdura por construccion —esta en las proporciones de partida
   de `constructor.py`—, asi que la fila se cumple por la FORMA y no por un
   limite. No hay nada que aplicar y conviene que quede escrito por que.

4. **Lo que el capitulo dice del DER y del pienso, que no toca al motor pero
   contesta una pregunta.** La disfuncion cognitiva **no cambia las kcal**: el
   capitulo no da ningun factor de energia, y su unica advertencia sobre la
   comida es de PRIORIDAD — «cardiovascular and chronic renal failure may become
   more of a priority than cognitive dysfunction, necessitating reduced levels of
   sodium and phosphorus in the food». Eso es justo lo que hace el motor cuando se
   marcan dos patologias a la vez: el tope mas estricto manda con `min()`. La
   fuente pide explicitamente lo que el solver ya hace por construccion.

5. **Y el plazo, que el aviso de hoy no lleva.** «Improvements in abnormal
   behavior associated with brain aging may be noted within six to 12 weeks after
   making a dietary change. If improvements are not noted with 12 weeks, then it
   is unlikely that nutritional management alone will result in significant
   improvement.» Seis a doce semanas, y a las doce sin mejora la dieta sola no va
   a bastar. **Propuesta apuntada, no aplicada**, como los plazos de la dieta de
   eliminacion del cap.31.

### cap.36 — Cardiovascular Disease (3.027 lineas, LEIDO ENTERO)

**De la Tabla 36-4, que tiene SIETE filas para el perro, el motor aplica tres, y
las tres estan bien.** El sodio por estadio en `cardiopatia*` —con toda la
historia de su atribucion, la correccion del 8 de septiembre y el techo legal
europeo escritos en su celda—, y la taurina (0,1 % MS = 250 mg/1000 kcal) y la
L-carnitina (0,02 % MS = 50) en `dcm_taurina_respondedora`. Leyendo el capitulo
entero, las cuatro filas restantes se resuelven asi:

1. **El potasio y el magnesio: nada que hacer, y por una razon que hay que
   escribir.** La tabla pide para el perro potasio **≥0,4 % MS** (1000 mg/1000
   kcal) y magnesio **≥0,06 % MS** (150). Los dos minimos de FEDIAF que el motor
   ya aplica son **mas altos**: potasio 1450 y magnesio 200. O sea que el
   requisito cardiaco **ya se cumple por el suelo del perro sano**, sin anadir
   nada. No es un hueco: es una fila que no aprieta.
   Y hay un matiz que explica por que el potasio no puede ser una cifra fija de
   todas formas: en el caso 36-2 el propio libro lo resume con las dos
   direcciones a la vez — «ensure adequate potassium intake, if using diuretics;
   avoid excess potassium intake, if using angiotensin-converting enzyme (ACE)
   inhibitor drugs». Depende del farmaco, no del alimento. Eso lo decide un
   clinico y no un solver.

2. **⚠️ EL FOSFORO SI ES UN HUECO.** La misma tabla pide para el perro cardiopata
   **0,2 a 0,7 % MS = 500 a 1750 mg/1000 kcal**, y `cardiopatia*` **no aplica
   ningun techo de fosforo**: un perro con cardiopatia marcada sale con el techo
   del perro adulto sano, que son 2000. El motivo esta escrito en la propia tabla
   —«Dogs with osteoarthritis are often in age groups at risk for kidney and/or
   heart disease», en la 34-2, y aqui «Phosphorus is a nutrient of concern in
   patients with concurrent chronic kidney disease»—, o sea que el numero no es
   del corazon: es del rinon que suele acompanarlo. **1750 es exactamente el
   techo que el motor YA aplica en `artrosis`**, y esa patologia es formulable,
   asi que la cifra cabe con el catalogo. Lo que falta medir es si cabe **junto
   al techo de sodio** de cada estadio, que es lo que aprieta de verdad.
   **MEDIDO**: [pendiente]

3. **El cloruro: la fuente pide un RATIO, y desde el 10 de septiembre el motor
   sabe expresarlo.** La tabla dice «Chloride — Dogs: Class Ia = 1.5 x sodium
   levels», y el texto lo repite: «Recommended chloride levels are typically 1.5
   times sodium levels.» Es un cociente entre dos nutrientes, que es exactamente
   lo que estrenó el bloque `ratios` de `patologias.json` con el Ca:P de los
   urolitos de calcio. **No se aplica**, y la razon para no aplicarlo a la ligera
   esta en el propio capitulo: el cloruro no acompana al sodio por simetria sino
   porque **es el anion el que dispara la renina** — «renin release occurs in
   response to renal tubular chloride concentration» — y por eso las sales de
   sodio sin cloruro no suben la tension igual. O sea que es un limite con
   mecanismo propio y merece decidirse, no copiarse. **Decision de Elena**, con
   la maquinaria ya construida.

4. **Y el dato de producto que este capitulo da y ningun otro**: el agua. «Distilled
   water or water with less than 150 ppm sodium is recommended for patients with
   advanced heart disease and failure». El motor cuenta el sodio del alimento y
   **no cuenta el del agua**, y un perro bebe aproximadamente sus kcal en
   mililitros (cap.25). A 150 ppm eso son ~0,15 mg de sodio por ml: para el perro
   mediano de 1117 kcal, **168 mg/dia**, que sobre un techo de 480 mg/1000 kcal
   en el estadio D no es despreciable. No es una cifra que el motor pueda aplicar
   —no sabe que agua bebe el perro— pero **es un aviso que se le puede dar al
   dueno**, y hoy no se le da. Apuntado.

### cap.37 — Chronic Kidney Disease (4.779 lineas, LEIDO ENTERO)

**Es el capitulo mas largo del libro y el que mas cifras del motor sostiene.** Los
seis numeros renales estan confirmados uno a uno en `HALLAZGOS_SACN5_10SEP.md`
§S-30 contra la Tabla 37-11, y siguen bien. Lo que anade leerlo entero:

1. **HAY DOS TABLAS, NO UNA, Y LA QUE FALTABA TRAE UNA FILA MAS.** S-30 verifico
   contra la **Tabla 37-11**, que es la de alimentos comerciales con su fila
   «Recommended levels». La tabla de factores propiamente dicha es la **37-9**, y
   dice lo mismo con una fila que la 37-11 no lleva: **«Chloride — 1.5 x sodium
   levels in foods for dogs»**. Es el mismo ratio que pide el capitulo cardiaco
   (Tabla 36-4), o sea **dos indicaciones distintas pidiendo el mismo cociente**,
   y ninguna de las dos aplicada. Refuerza que la decision sobre el bloque
   `ratios` merece tomarse.

2. **El ratio omega-6:omega-3, y la contradiccion que el propio libro no ve.** La
   Tabla 37-9 lo da explicito para el rinon: **«Omega-6:omega-3 fatty acid ratio
   of 1:1 to 7:1»**, y el texto lo justifica y luego dice algo que no se sostiene:
   «These recommendations are similar to omega-3 fatty acid content and
   omega-6:omega-3 ratios recommended for dogs and cats with cancer,
   osteoarthritis and inflammatory skin diseases.» **No son similares**: el cancer
   pide «as close to 1:1 as possible» (Tabla 30-5) y la artrosis **<1:1** (Tabla
   34-2), mientras que aqui se admite hasta **7:1** — siete veces mas laxo. Es la
   confirmacion, dentro de una sola fuente, de lo que `CLAUDE.md` dice de por que
   ese ratio sigue sin aplicarse: **no hay un numero, hay un rango por enfermedad
   y lo elige un clinico**. Ahora esta medido cuanto se separan.

3. **El fosforo en la otra unidad, y aqui hay que tener cuidado con lo que se
   afirma.** La Figura 37-8 da las dos ramas de un experimento clasico en mg por
   kilo de perro: alto = 60 a 80 mg/kg/dia, bajo = 15 a 40. **No es una
   recomendacion, son los brazos de un estudio**, y por eso esto no propone
   cambiar nada. Pero conviene tener la conversion hecha: con nuestro techo renal
   de 1200 mg/1000 kcal, los mg por kilo de perro al dia son 1,2 x DER/peso, y eso
   da **100 en el toy de 3 kg, 61 en el mediano de 22 kg y 48 en el gigante de 55**.
   O sea que el mismo techo por concentracion cae en la banda «alta» del
   experimento para el perro pequeno y en la baja para el grande. Es el mismo
   efecto que se midio con el EPA de la artrosis (cap.34): **un limite por 1000
   kcal no es un limite por kilo de perro, y la diferencia va con el tamano**.
   Queda escrito porque aparece ya dos veces y va a volver a aparecer.

4. **La transicion, que este motor SI implementa y aqui tiene un matiz nuevo.**
   `transicion.py` aplica el calendario largo de la Tabla 1-1 (10 dias) con su
   fuente citada, y eso esta bien. El capitulo renal anade que para un enfermo
   renal ese calendario es **el minimo**: «The transition period should be a
   minimum of seven days; however, some patients (especially cats) need a
   transition of three to four weeks or longer.» Y le da un peso que no tiene en
   ningun otro capitulo — un cambio brusco «results in an unhappy owner and a
   patient that will likely not receive the benefits of nutritional management».
   El motor usa 10 dias para todos, con patologia o sin ella. **Apuntado como
   decision de producto**, no aplicado.

5. **Y la frase que deberia estar en la pantalla, porque corrige un malentendido
   que el propio libro identifica.** Del recuadro 37-4: «It may be more
   appropriate to refer to these foods as “formulated to avoid excessive protein”
   or “modified protein foods” instead of being “protein restricted”, which may
   incorrectly be interpreted as protein-deficient by pet owners and health care
   team members.» El motor aplica en renal un suelo de proteina de 62,5 g/1000
   kcal — **por encima** del 14-20 % MS (35-50) que pide la tabla, y eso ya esta
   escrito y razonado —, asi que Rawku esta del lado bueno de este malentendido y
   puede decirlo con la cita delante.

6. **Lo que NO se ha leido de este capitulo, y se dice**: las Tablas 37-11 y 37-12
   son **listados de productos comerciales** —marca a marca, con su densidad
   energetica y sus porcentajes—, y de ellas se ha leido la fila «Recommended
   levels», que es la que manda, y no las celdas de cada pienso. Es la misma
   categoria que `sacn5_tablas.json` aparta por su propio titulo, y aqui se
   declara para que no cuente como leido lo que no lo esta.

### cap.38 — Canine Urolithiasis: Definitions, Pathophysiology and Clinical Manifestations (2.118 lineas, LEIDO ENTERO)

**Nada que aplicar, y hay que poder decirlo con la misma seguridad que cuando si
hay algo.** Es el capitulo definicional de los urolitos: nucleacion,
sobresaturacion, matriz organica, radiodensidad, urohidropropulsion por miccion,
analisis cuantitativo. **No tiene tabla de «Key nutritional factors» ni una sola
cifra de formulacion**; las de cada tipo de calculo estan en los capitulos
siguientes (39 a 43), que son de donde salen las seis patologias de urolitos del
motor.

Lo que si aporta es **el porque de una decision de permisos que ya esta tomada**.
Las seis patologias de calculos —estruvita, oxalato, urato, cistina, silice y
fosfato calcico— estan las seis marcadas `solo_veterinario` en
`quien_formula_cada_patologia.json`, y cinco de ellas declaran «pH urinario» como
el dato clinico que falta. Este capitulo dice que **antes que el pH hace falta
saber de que es la piedra, y que eso solo lo dice un laboratorio**:
· «Microscopic evaluation of urine crystals should not be used as the sole
  criterion to predict the mineral composition of macroliths in patients with
  confirmed urolithiasis»
· «Only quantitative analysis can provide definitive information about the
  mineral composition of the entire urolith.»
Y avisa de que la piedra puede no ser de una sola cosa: «Compound uroliths have
one or more layers of mineral composition (e.g., struvite) different from
minerals identified in the nucleus (e.g., calcium oxalate)», lo que significa que
marcar la patologia equivocada no es un matiz — el capitulo lo lista como una de
las tres causas de que la disolucion no funcione.
**PROPUESTA, NO APLICADA**: que el `que_dato` de esas cinco pase de «pH urinario»
a nombrar tambien el **analisis cuantitativo del calculo**, que es lo que urato
ya declara. Es un campo de documentacion que vigila el BLOQUE 79, no una cifra
del solver, pero cambia lo que la ficha dice que hace falta preguntar y por eso
se deja escrito en vez de hacerlo.

Y una frase que conviene tener a mano cuando alguien pregunte por que el motor no
«cura» piedras: «Urolithiasis should not be viewed as a single disease, but rather
as a sequela of one or more underlying abnormalities.»

### cap.39 — Canine Purine Urolithiasis (2.598 lineas, LEIDO ENTERO)

**La Tabla 39-4 ya estaba aplicada y bien**: `urato` va `formulable: false` con
`nutriente_frontera: purinas`, objetivo 90 mg/1000 kcal, y su aviso profesional
cita literal el «Restrict dietary protein to 10 to 18% dry matter» de esa tabla
como segundo eje independiente que apunta a lo mismo. Nada que corregir. Lo que
sale de leerlo entero es **una comprobacion del catalogo que nadie habia hecho**.

1. **⚠️ LA TABLA 39-3 ES UNA LISTA DE ALIMENTOS, Y SE PUEDE CRUZAR CON EL
   CATALOGO. Al hacerlo, los huecos de datos caen JUSTO en la columna
   equivocada.** La tabla clasifica los alimentos en tres columnas —alimentos que evitar por su alta
   concentracion de purinas, alimentos a usar con moderacion y alimentos de
   concentracion despreciable; los rotulos de columna se parten al extraer el
   texto y por eso van descritos y no entrecomillados— y en la primera nombra,
   entre otros: sesos, mollejas, rinon, higado, corazon, sardinas, caballa, atun,
   salmon, mejillones, gambas, anchoas y «Yeast (baker's and brewer's)».
   **MEDIDO contra las 163 fichas**: 58 de ellas llevan las purinas en `sin_dato`
   —o sea, declaradas como desconocidas, que es lo correcto y no un cero
   disfrazado— y entre esas 58 estan **las dos levaduras de cerveza, el cerebro
   de ternera, el timo de ternera, el pancreas de vaca, la laringe de vacuno y
   los dos pulmones**. Seis de esas ocho estan nombradas por la fuente en la
   columna de «evitar». Y la comparacion interna lo confirma: el **timo de vaca**
   si tiene dato y es **el alimento con mas purinas de todo el catalogo (525
   mg/100 g)**, mientras que el timo de ternera figura como desconocido.
   **NO ES UN FALLO DEL MOTOR** —el catalogo hace lo correcto declarandolo
   `sin_dato` en vez de poner un 0— **pero si tiene una consecuencia que conviene
   escribir**: la medida que sostiene la decision de `urato` (una racion cruda ronda
   los 780 mg de purinas/1000 kcal contra un objetivo de 90, segun su propia
   celda en `patologias.json`) se calcula con
   esas 58 fichas aportando cero. O sea que **es una cota INFERIOR**, y la carga
   real es todavia mayor. La decision de no formular urato automaticamente sale
   **reforzada**, no debilitada, y ahora se sabe por que.
   Apuntado para `DATOS_QUE_FALTAN.md`, donde las purinas hoy solo aparecen
   nombradas de pasada como ejemplo de procedencia en la ficha.

2. **Y una diferencia de metodo a favor del repo, que merece decirse.** La Tabla
   39-3 es **cualitativa** —tres columnas, ni un numero— y sus alimentos son de
   dieta humana. El catalogo lleva las purinas **en mg por 100 g con su
   `purinas_fuente` ficha a ficha** (USDA/ODS-NIH v2.0, Souci-Fachmann-Kraut).
   Cruzadas las dos, el orden coincide donde hay dato: boqueron 411, sardina 345,
   salmon 250, higados 243, rinones 213, caballa 194, corazones 171, atun 157 —
   los ocho en la columna de «evitar» de la fuente. **La clasificacion cualitativa
   de SACN5 y los numeros del catalogo dicen lo mismo**, que es la primera vez
   que se comprueba.

3. **Lo que el capitulo NO da y por eso no se puede aplicar**: un techo de purinas
   en mg. El objetivo de 90 mg/1000 kcal que usa el motor **no sale de aqui** —la
   Tabla 39-4 no lo trae— y el capitulo se limita a decir que los tres primeros
   ingredientes no acuosos sean bajos en purinas. Es un criterio de **etiqueta de
   pienso**, no una cifra formulable, y por eso el motor no puede convertirlo en
   restriccion. Queda escrito para que nadie busque en este capitulo un numero que
   no esta.

### cap.40 — Canine Calcium Oxalate Urolithiasis (1.798 lineas, LEIDO ENTERO)

**La patologia mas trabajada del bloque de urolitos, y se confirma entera.** De la
Tabla 40-5 el motor aplica el sodio (750), el fosforo (1500), el magnesio (375) y
—desde el 10 de septiembre— **el ratio Ca:P de 1,1 a 2,0**, que es el que estreno
el bloque `ratios`; escribe sin aplicar el suelo de fosforo, el de magnesio, la
proteina y el acido ascorbico; y **no baja el calcio a proposito**, con el motivo
de la propia fuente en su aviso. Releido el capitulo entero, esa decision es
exactamente lo que dice: «reducing consumption of calcium may increase the
availability of oxalic acid for intestinal absorption and subsequent urinary
excretion», y el epidemiologico humano que lo respalda. **Bien.**

Lo que sale de leerlo entero son dos comprobaciones de la transcripcion, y las dos
son pequenas:

1. **La Tabla 40-3 esta transcrita a 17 de sus 20 entradas (H), y las tres que
   faltan no existen en el catalogo.** `_OXALATO_TABLA_40_3` en `seguridad.py`
   recoge las marcadas «high; avoid feeding»: apio, berenjena, boniato, calabacin,
   espinaca, judia verde, pepino, pimiento, albaricoque, los tres frutos del bosque,
   mandarina, manzana, cacahuete, soja y tofu. **Faltan tres** que la tabla tambien
   marca (H): la **piel de limon, lima o naranja**, las **nueces pecanas** y el
   **germen de trigo**. **COMPROBADO**: ninguna de las tres esta en las 163 fichas,
   asi que hoy no cambia ningun menu. Se deja escrito porque el dia que se anada
   una, la lista no la va a coger — y porque «17 de 20» y «las 20» no son lo mismo
   aunque den el mismo resultado.
   (Las marcadas (M) se dejaron fuera a proposito y esta razonado: la fuente pide
   para ellas «feed in limited amounts», y el motor no sabe expresar «con
   moderacion» para un alimento concreto. En el catalogo son brocoli, zanahoria,
   lechuga, esparrago, tomate, naranja, pera, pina y sardina.)

2. **El aceite de cacahuete se excluye, y probablemente no hace falta.** La
   exclusion va por palabras, asi que «cacahuete» tumba tambien el **Aceite de
   cacahuete**. El oxalato es hidrosoluble y se queda en la parte acuosa, no en el
   aceite — es el mismo caso que el cap.31 con los aceites vegetales y las
   alergias, donde la fuente dice explicitamente que el alergico al cacahuete
   tolera su aceite. **No se toca**, por lo mismo que alli: apretar de mas es el
   lado seguro y aflojar una exclusion de urolitos no es una decision que tome un
   asistente. Queda medido y escrito.

3. **Y una confirmacion que vale para el documento de revision**: el capitulo dice
   por que el oxalato es el urolito que mas ha crecido —«Calcium oxalate accounted
   for 38% of all canine uroliths submitted to the Minnesota Urolith Center from
   1981 to 2007»— y que la restriccion de proteina que pide (10 a 18 % MS) es la
   misma cifra que pide el capitulo del urato. Dos urolitos distintos, la misma
   frontera, y las dos **por debajo del minimo de FEDIAF** (52,1 g/1000 kcal contra
   los 25-45 de la fuente). Por eso `oxalato` aplica su proteina como escrita y no
   aplicada, y por eso `urato` no es formulable: no es una decision distinta en
   cada sitio, es la misma frontera vista dos veces.

### cap.41 — Canine Calcium Phosphate Urolithiasis (1.094 lineas, LEIDO ENTERO)

De la Tabla 41-6 el motor aplica **cinco de sus ocho filas** —fosforo 1500,
magnesio 375, sodio 750, proteina 62,5 y vitamina D 9,375— mas el ratio Ca:P de
1,1 a 2,0 en el bloque `ratios`. El pH urinario (6,2-6,6) no es modelable. Queda
**una fila**, y es la que da el hallazgo.

1. **⚠️ EL TECHO DE CALCIO NO SE APLICA, Y EL MOTIVO ESCRITO ES EL DE LA
   PATOLOGIA DE AL LADO.** La Tabla 41-6 pide **calcio 0,4 a 0,7 % MS = 1000 a
   1750 mg/1000 kcal**, y el motor no aplica ninguno. El aviso de
   `urolitos_fosfato_calcico` explica por que, con esta frase suya (va sin comillas
   angulares porque es del JSON y no de la fuente): "El calcio NO se baja, igual
   que en el oxalato: bajarlo aumenta la absorcion intestinal de oxalato y no
   ayuda". **Y ese motivo es del oxalato, no de
   aqui.** En un urolito de oxalato calcico el argumento se sostiene y esta
   verificado con una fuente de 2025 que dice literalmente lo contrario que SACN5
   2010; vive en la clave `calcio_no_se_restringe` de `oxalato`, con su cita. Pero
   **esa fuente se titula «Canine Calcium Oxalate Urolithiasis» y no habla de
   fosfato calcico**, y el mecanismo tampoco traslada: aqui la piedra es fosfato,
   no oxalato, asi que «bajar el calcio libera oxalato» no dice nada del problema
   que se quiere evitar. El capitulo 41 pide su cifra por derecho propio y explica
   su propio mecanismo — la hipercalciuria baja la solubilidad del fosfato
   calcico — sin apoyarse en el oxalato para nada.
   **Y hay sitio para aplicarlo**: 1750 mg/1000 kcal contra el minimo de FEDIAF
   para el adulto, que son 1450. La ventana es estrecha —300 mg— pero no esta
   vacia.
   **NO SE CAMBIA AQUI**, porque restringir o no el calcio en un perro con
   urolitos es criterio clinico y no de un asistente. Lo que si hace falta es que
   la decision **exista como decision**: hoy no esta en
   `limites_escritos_que_el_solver_no_aplica`, que es el sitio que audita el
   BLOQUE 55, sino solo en la prosa de un aviso — y con el motivo prestado.
   **Decision de Elena**, con las dos opciones sobre la mesa: aplicar el techo de
   1750, o declararlo escrito y no aplicado con un motivo que sea de este capitulo.

2. **Lo que la fuente dice del fosforo, y que matiza nuestro 1500.** El capitulo
   avisa en los dos sentidos: «Foods with higher levels of phosphorus tend to
   augment hyperphosphaturia», pero tambien «excessive restriction of dietary
   phosphorus may enhance the availability of dietary calcium for intestinal
   absorption. It may also enhance production of 1,25-vitamin D by the kidneys,
   thereby promoting hypercalciuria.» O sea que apretar de mas el fosforo **hace
   dano por el otro lado**. El motor aplica 1500, que es el extremo ALTO del
   0,3-0,6 % MS de la tabla: es el lado correcto de ese aviso, y ahora esta
   escrito por que.

3. **Y la proteina, donde el motor tambien elige el extremo alto y esta vez la
   fuente pide lo contrario.** La tabla da 10 a 25 % MS y el texto anade una
   preferencia que la tabla no lleva: «The recommended range for dietary protein
   is 10 to 25% DM; the lower end of this range is probably better.» El motor
   aplica **62,5**, que es el 25 % — el extremo alto. Y esta bien que lo haga, por
   la razon de siempre: el extremo bajo (25 g/1000 kcal) esta **por debajo del
   minimo de FEDIAF** (52,1) y seria una dieta de prescripcion. Queda escrito que
   la fuente prefiere el otro extremo y que no se puede llegar sin bajar de
   FEDIAF, que es exactamente la frontera que `VETERINARIOS.md` reserva para una
   pauta firmada.

### cap.42 — Canine Cystine Urolithiasis (937 lineas, LEIDO ENTERO)

**La Tabla 42-1 esta aplicada en lo que se puede.** `cistina` va
`formulable: false` con `nutriente_frontera: metionina_cistina`, aplica el sodio
de 750 y su aviso profesional cita literal el «Restrict high quality dietary
protein to 10 to 18% dry matter» de esa tabla. Nada que corregir.

Lo unico que anade el texto corrido y la tabla no lleva es **una lista de
alimentos**: «Besides most meats, other food ingredients high in methionine
include eggs, wheat and peanuts.» De esos tres, el catalogo tiene **huevo** (dos
fichas) y **cacahuete** (su aceite). No cambia nada hoy —esta patologia no
formula menu automatico— pero es la tercera vez en cinco capitulos que una
patologia de urolitos trae su lista de alimentos ademas de sus cifras (Tabla 39-3
para las purinas, 40-3 para el oxalato, y esta), y solo dos de las tres estan
recogidas en el motor. Queda apuntado.

Y una cosa que si importa para el aminograma: el capitulo explica que la
restriccion real es de **metionina**, que es el precursor, no de cistina. El
catalogo tiene las dos columnas desde el 28 de agosto (94 de 159 fichas con
aminograma), asi que el dato existe; lo que no existe es la posibilidad de bajar
de FEDIAF sin firma. Eso ya esta escrito.

### cap.43 — Canine Struvite Urolithiasis (2.503 lineas, LEIDO ENTERO)

**La Tabla 43-3 esta aplicada entera y bien, con sus dos columnas separadas**
—disolucion contra prevencion—, que es el detalle que mas facil habria sido
perder: `estruvita` aplica los tres numeros de PREVENCION (magnesio 250, fosforo
1500, proteina 62,5) y declara en su aviso profesional los de DISOLUCION (fosforo
≤0,1 % MS, proteina ≤8 % MS) como lo que son, muy por debajo del minimo de
FEDIAF. Y el aviso de crecimiento dice por que ahi no se aplica ninguno. Nada que
corregir.

Lo que sale de leerlo entero es **un dato de metodo que toca a `transicion.py`**,
y es el segundo en dos capitulos:
· para disolver estruvita, la transicion es de **cuatro o cinco dias** —«Begin the
  transition by feeding 75% of the current food and 25% of the litholytic food on
  Day 1. On Day 2, feed half of each food. On Day 3, feed 75% as the litholytic
  food. By Day 4 or 5, feed only the litholytic food.»— que es el calendario CORTO
  de la Tabla 1-1;
· para el enfermo renal, el cap.37 pide **siete dias como minimo y a veces tres o
  cuatro semanas**.
El motor aplica **diez dias a todos**, con patologia o sin ella, y su comentario
razona esa eleccion solo contra el cambio de pienso a crudo. **No es un fallo**
—el calendario largo cumple el minimo de las dos indicaciones— pero la fuente
trata la velocidad de transicion como algo que depende de para que es la dieta, y
el motor no. **Apuntado como decision de producto.**

Y una frase de manejo que el motor ya cumple sin haberlo buscado: «Free-choice
feeding is often associated with more persistent aciduria compared to meal
feeding» y, aun asi, la recomendacion es dar **raciones medidas dos o tres veces
al dia** en vez de comida a discrecion. Rawku no sabe dar de comer a discrecion:
formula una racion pesada. Es la tercera vez que el libro pide explicitamente lo
que este motor hace por construccion — con el `food-limited feeding` del cap.33 y
el «restrict only energy» del cap.27.

### cap.44 — Canine Silica Urolithiasis (539 lineas, LEIDO ENTERO)

**Confirmado entero, sin nada nuevo.** La Tabla 44-1 tiene cuatro filas —agua,
proteina 10-18 % MS, silice (evitar gluten de maiz, cascarilla de arroz y de soja)
y pH urinario 7,1-7,7— y `urolitos_silice` las recoge las cuatro: va
`formulable: false` con `nutriente_frontera: proteina` y objetivo 35 g/1000 kcal,
y su aviso profesional ya trae el matiz que mas importa a una racion cruda, que el
capitulo dice literal: «Animal-derived protein ingredients are an unlikely source
of silica. In contrast, some plant-derived protein sources contain larger
quantities of silica.» O sea que el eje de silice de la fuente apunta a
ingredientes que un BARF casi no lleva, y el unico eje que si nos toca —la
proteina— cae entero por debajo del minimo de FEDIAF. Esta bien escrito y bien
decidido.

### cap.45 — Canine Compound Urolithiasis (268 lineas, LEIDO ENTERO)

**Ya se habia leido entero el 9 de septiembre y su regla esta recogida**, en la
clave `nota_urolito_compuesto` de `oxalato`: los urolitos compuestos son el 7 % de
los caninos, el primer ejemplo del capitulo es justo nucleo de oxalato con capa de
estruvita, y la regla de manejo es tratar **el mineral del nucleo y no los de las
capas**. El motor combina `oxalato` + `estruvita` con `min()` sin decir nada, y
eso esta escrito ahi con su medida y su motivo. Releido: **la nota dice lo que el
capitulo dice.** Nada que anadir.

### cap.46 — Feline Lower Urinary Tract Diseases (5.360 lineas, LEIDO ENTERO)

**Capitulo FELINO leido entero a proposito**, por la misma razon que los seis de
la primera mitad: apartarlo por el titulo es exactamente como se descarto una vez
la nota d del selenio, que era del perro. Y ha vuelto a pasar lo mismo — **este
capitulo felino trae la lista de alimentos altos en oxalato mas completa del
libro, y su texto la enuncia para los DOS**.

1. **⚠️ LA TABLA 46-18 CONTRADICE Y AMPLIA A LA 40-3, Y LA FRASE QUE LA
   INTRODUCE DICE «dogs and cats».** El texto, literal: «Excessive intake of
   oxalate is unlikely in dogs and cats eating most commercial foods but it could
   occur in pets receiving excessive amounts of certain human foods as treats.
   Foods that contain relatively high amounts of oxalate (e.g., spinach, carrots,
   liver, sardines) should be avoided in patients with a history of calcium
   oxalate uroliths.» De esos cuatro ejemplos, **el motor solo excluye la
   espinaca**: la zanahoria, el **higado** y la **sardina** no estan en
   `OXALATO_ALTO`.
   **MEDIDO contra el catalogo**, cruzando la columna «Moderate to high oxalate»
   de la Tabla 46-18 con las 163 fichas, salen **catorce alimentos que la tabla
   pone arriba y el motor no excluye**: la sardina, **los seis higados** (vaca,
   pollo, pavo, cordero, conejo, pato) y el aceite de higado de bacalao, la
   zanahoria, la pera, el platano, la naranja, la pina, el grelo y el nabo (los
   dos, «Greens (collards, mustard, turnips)»), el tomate y el sesamo.
   Y al reves, **uno que el motor SI excluye y esta tabla pone en la columna
   BAJA**: el **pepino**, que la Tabla 40-3 marca (H) y la 46-18 clasifica como
   bajo en oxalato. Lo mismo pasa con el esparrago y el brocoli, que la 40-3 marca
   (M) y esta pone abajo.
   **NO SE TOCA NADA, y aqui el motivo es de peso**: el higado es la pieza con la
   que una racion cruda cubre la vitamina A, el cobre y la B12, y quitarlo de un
   menu de oxalato podria dejar la patologia sin menu. Es exactamente la clase de
   decision que **no toma un asistente**. Lo que si hacia falta era ponerla sobre
   la mesa con la medida hecha. **Decision de Elena**, y grande.

2. **⚠️ Y UN HALLAZGO DE METODO QUE VALE PARA TODO EL REPO: esta tabla NO se
   puede leer del `.txt`, y el `.txt` no avisa.** El arreglo del 10 de septiembre
   —`page.get_text()` en vez de conservar la disposicion visual— resolvio las dos
   columnas del **cuerpo del texto**, y por eso las citas de prosa son fiables.
   Pero una **tabla de dos columnas dentro de una columna de texto** sigue
   saliendo entrelazada: en el `.txt`, la Tabla 46-18 aparece con las celdas alternadas
   una linea si y otra no (higado, vaca, sardinas, bacon, jamon, cordero...), que
   leido en fila pone en la misma lista lo
   alto y lo bajo. **Leida asi, la carne de vaca parece alta en oxalato y la
   sardina baja.** La unica forma fiable de leerla es sacar las palabras del PDF
   **con su coordenada x** y separar por posicion — con `pymupdf`, `get_text
   ("words")`, columna alta en x≈134 y columna baja en x≈229. Asi se lee, y asi se
   ha leido. **Esto no estaba escrito en ninguna parte** y es la tercera capa del
   mismo fallo: primero las dos columnas del libro, luego las citas partidas, y
   ahora las tablas de dos columnas dentro de la columna. Apuntado para
   `canislab-fuentes` y para quien vuelva a abrir una tabla.

3. **Lo que confirma sin cambiar nada.** El mecanismo del calcio que sostiene la
   decision de `oxalato` esta aqui otra vez y mas claro que en el cap.40: «if
   dietary calcium is reduced without a concomitant reduction in dietary oxalate,
   intestinal absorption and urinary excretion of oxalate may increase.» Y el
   capitulo trae el aviso de la vitamina C con su medida —en gatos sanos, de 40 a
   193 mg/kg de alimento no cambio la excrecion urinaria de oxalato— y aun asi
   recomienda evitarla. El motor no tiene columna de vitamina C, asi que no aplica
   ni una cosa ni la otra.

4. **Lo felino que no toca al motor, y se dice para cerrarlo.** Todo lo demas del
   capitulo —la cistitis idiopatica felina, los tapones uretrales, la
   uretrostomia perineal, el pH urinario objetivo, los recuadros de manejo de la
   bandeja y del enriquecimiento ambiental, y las Tablas 46-19 a 46-27 de piensos
   comerciales felinos— es de gato y no tiene columna canina. Las cifras de sus
   tablas (magnesio 0,07-0,14 % MS, fosforo 0,5-0,9, calcio 0,6-1,0, proteina
   32-45, sodio 0,3-0,6) son perfiles de alimento **felino** y no se trasladan.

### cap.47 — Periodontal Disease (1.868 lineas, LEIDO ENTERO)

**Este capitulo no da ni una cifra que el motor pueda aplicar de nuevo, y aun asi
es de los que mas le importan a esta app**, porque desmonta una creencia sobre la
que se vende medio BARF.

1. **⚠️ EL RECUADRO 47-6 DICE QUE LA COMIDA NATURAL NO PREVIENE LA ENFERMEDAD
   PERIODONTAL, Y QUE ADEMAS ROMPE DIENTES.** Es el recuadro «Natural Food
   Sources and Periodontal Disease», y su medida es concreta: «One study involved
   67 English foxhounds, one to nine years of age that were routinely fed raw
   carcasses consisting of the bony skeleton, muscle and associated tissues. Oral
   examinations revealed that all dogs had varying signs of periodontal disease as
   well as a high prevalence of tooth fractures.» Y su conclusion: «These findings
   cast skepticism on the long-held view that a natural food source prevents
   development of oral disease, particularly periodontal disease, in dogs and
   cats.»
   **QUE HACE HOY RAWKU**: nada, y eso es lo bueno y lo malo a la vez. **No
   promete beneficio dental en ninguna parte** —comprobado, no hay ni una mencion
   a dientes, sarro o placa en avisos, documentos ni codigo—, asi que **no hay
   nada que corregir**. Pero tampoco avisa del **riesgo de fractura dental** del
   hueso carnoso, que es entre el 20 y el 60 % del peso de una racion de este
   motor, y el dueno tipico llega creyendo lo contrario. El motor si sabe de
   dientes por otro lado: `main.py` deja sin hueso al perro «senior sin dientes» o
   con la mandibula operada. **Propuesta apuntada, no aplicada**: un aviso de
   producto que diga las dos cosas — que el hueso no limpia los dientes y que
   puede romperlos —, con esta cita. Es texto que ve el dueno, asi que **decision
   de Elena**.
   Y para no contarlo torcido, la otra mitad del capitulo: la comida blanda
   **tampoco** es automaticamente peor. La Figura 47-5 compara humedo de marca,
   humedo de supermercado y seco, y «There is no significant difference in
   substrate accumulation among dogs fed the three foods.» Lo que funciona no es
   «duro» sino una textura disenada — «A typical dry food does not possess the
   mechanical characteristics for adequate dental cleansing» — y el propio libro
   dice que llamar dental a un pienso crujiente «is a misrepresentation to pet
   owners». O sea que ni el hueso ni el pienso: lo unico que la fuente respalda es
   un producto con el sello VOHC o un ensayo de grado 1 o 2 detras.

2. **La Tabla 47-4 no anade cifras nuevas, y esa es la noticia.** Sus cinco filas
   caninas son **las mismas de siempre**: vitamina E ≥400 UI/kg MS (el **septimo**
   capitulo que la pide, tras el 1, 7, 27, 32, 34, 35 y 37 — sigue sin aplicarse,
   §S-12), vitamina C ≥100 mg/kg (que el catalogo no tiene), selenio 0,5-1,3 mg/kg
   (que choca con el maximo legal de 142 µg/1000 kcal, §S-11), **fosforo 0,4-0,8 %
   MS = 1000-2000** y **sodio 0,2-0,4 % MS = 500-1000**.
   Esos dos ultimos son, otra vez, los techos del perro adulto sano que
   `recomendaciones_libro.json` aplica desde el 8 de septiembre. **Van ya cinco
   tablas del mismo libro con el mismo par de numeros**: 13-3 y 14-2 (el perro
   sano), 27-4 (obesidad), 31-3 (reaccion adversa), 34-2 (artrosis) y 47-4
   (periodontal). Cinco indicaciones distintas, cinco veces 2000 y 1000. Eso ya no
   es una coincidencia: es **la cifra que el libro considera prudente para
   cualquier perro adulto que va a comer lo mismo durante meses**, que es
   exactamente el caso de Rawku.

### cap.48 — Introduction to Gastrointestinal and Exocrine Pancreatic Diseases (306 lineas, LEIDO ENTERO)

Es el capitulo-indice del bloque digestivo: enumera las diecinueve enfermedades
que vienen despues y describe los **tipos de alimento** que se usan en ellas. No
tiene tabla de factores nutricionales clave ni una cifra por patologia. Lo que si
trae, y sirve de comprobacion cruzada, es **la escala de grasa del perro** en el
recuadro 48-3: alimentos de grasa moderada **12 a 15 % MS** (30 a 37,5 g/1000
kcal), y por encima del **25 % MS** (62,5) alimentos que «Patients with GI or
pancreatic disease may not tolerate».
**Cuadra con lo que el motor aplica**: el techo de grasa de `pancreatitis` son
**37,5 g/1000 kcal**, que es exactamente el extremo alto del rango «moderado» de
esta escala, y viene de la Tabla 67-4 (SACN5 cap.67). Dos capitulos distintos, la
misma frontera. Y el 62,5 que la escala llama «alto» es, curiosamente, el mismo
numero que el cancer pide como **suelo** — la misma cifra es techo en un sitio y
suelo en otro, que es el mejor recordatorio de por que los limites del motor van
por patologia y no por criterio general.
Dos cosas mas que no son cifras y conviene tener: la definicion de «altamente
digestible» que usa el libro —proteina ≥87 %, grasa e hidratos ≥90 %— y que el
propio capitulo avisa de que «All too often, relative terms such as “low” vs.
“high” are used without stating the point of reference.» Eso es exactamente lo
que este repo intenta no hacer.

### cap.49 — Oral Diseases (258 lineas, LEIDO ENTERO)

**Nada aplicable, y por una razon estructural.** Sus dos factores nutricionales
clave son **densidad energetica** (>4,5 kcal/g MS en el perro) y **forma del
alimento** (liquido o papilla), y ninguno de los dos es un nutriente: son
propiedades del producto terminado. El motor formula gramos de alimentos frescos
y **no decide la textura ni la densidad**, asi que no hay nada que aplicar ni que
declarar como no aplicado.
Lo unico que roza a Rawku es la parte de manejo, que el motor ya respeta sin
saberlo: raciones pequenas y varias veces al dia. Y una nota que si vale para el
catalogo el dia que alguien mire la boca del perro: el cap.47 deja al perro sin
hueso cuando es senior sin dientes o tiene la mandibula operada, y este capitulo
anade la lista de lo que mas duele — fracturas de sinfisis mandibular, dientes
desplazados, neoplasia oral — donde esa misma exclusion tendria sentido y hoy no
se ofrece como opcion.

### Dos punteros que faltaban, escritos al cerrar esta tanda

**1. El DHA del cap.33 ya tenia dueno, y hay que decirlo.** La correccion de
`lecturas_sacn5.json` sigue siendo correcta —el veredicto decia «ya aplicado» y
no lo esta—, pero la **decision** de aplicarlo no es nueva: vive en
`LECTURA_SACN5.md` §1.1 desde la primera lectura, que lo senala como el candidato
mas solido de toda ella (sin comillas a proposito: esa frase es nuestra, no de
SACN5, y `auditar_citas.py` solo sabe buscar en la fuente) y ya habia visto que
sale en cuatro sitios (Tablas
15-5, 17-1 en sus dos columnas, 33-5, y el texto de los caps.15 y 33). Lo que
anade esta relectura son **los numeros del catalogo**: DHA de 0,081 a 1,324
g/1000 kcal en los doce menus de cachorro, del 54 al 75 % de la suma. O sea que
el hueco esta en las reglas y no en los menus, y aplicarlo **no romperia nada**.
Esa medida faltaba.

**2. El umbral de calcio del BLOQUE 69 esta aplicado, y esta relectura dice donde
NO se comprueba.** `LECTURA_SACN5.md` §1.2 pedia sustituir el 90 % inventado por
el 1,5 % MS de la Tabla 32-1, y ya esta hecho: `_CA_UMBRAL_ZINC_69 = 3750.0`.
Pero sus seis casos son **adulto y senior** —3, 10, 20 y 40 kg adultos, 10 y 30
senior—, y medido sobre los 36 menus del catalogo **ninguno de adulto o senior
cruza el umbral** (el mayor, 0,97 % MS). Los que lo cruzan son **17, y los 17 son
de crecimiento, gestacion o lactancia**, que es justo la poblacion que ese bloque
no resuelve. La regla sigue siendo `documentado_sin_cifra` y no cambia nada, pero
conviene saber que **el bloque vigila la etapa donde el umbral no se toca**.
Apuntado; ampliar sus casos a crecimiento es una linea, y es decision de quien
mantenga la bateria.

---

## Los capitulos de DIGESTIVO (50 al 67)

Aqui la relectura cambia de tono: **ocho de estos dieciocho capitulos ya tienen
patologia en el motor** —`riesgo_gdv`, `enteropatia_cronica`,
`estrenimiento_cronico`, `flatulencia`, `intestino_irritable`, `sibo`,
`ple_linfangiectasia`, `insuficiencia_pancreatica_exocrina`—, asi que lo que se
busca no es «que dice la fuente» sino **que dice la fuente que el motor no
tenga**. Se comprueba cifra a cifra contra `patologias.json`.

### cap.50 — Pharyngeal and Esophageal Disorders (927 lineas, LEIDO ENTERO)

1. **⚠️ EL HUESO, POR TERCERA VEZ Y CON LA CIFRA MAS DURA DE LAS TRES.** El
   cap.19 hablaba de fracturas dentales y el cap.11 de patogenos; este trae el
   tercer dano y lo mide: «**In a recent retrospective review, 46 of 60 esophageal
   foreign bodies removed from dogs were bones**». Y en la anamnesis, el capitulo
   manda preguntar exactamente por lo que este motor formula: «Owners of pets
   presenting for suspected pharyngeal and esophageal disorders should be asked
   about feeding dental chew treats» y, tras la cita del estudio que va en medio,
   «bones or bone and raw food diets, which can result in esophageal foreign
   bodies». Setenta y siete de cada cien cuerpos
   extranos esofagicos del perro son hueso.
   El motor mete hueso carnoso en **todos** los menus (es la fuente de calcio del
   BARF y la regla de forma pide 20-60 %). No hay nutriente que tocar aqui: es un
   **aviso**, y es el mismo pendiente que ya dejaron el cap.19 y el cap.11.
   Sigue siendo decision de Elena, ahora con tres danos distintos medidos.

2. **Las cifras del capitulo NO se aplican, y conviene decir por que.** Pide
   energia ≥4,5 kcal/g MS y grasa ≥25 %MS para el megaesofago, y grasa ≤15 %MS
   para la esofagitis por reflujo. Son **recomendaciones opuestas entre si** segun
   cual de las dos cosas tenga el perro, no requisitos: el propio capitulo las
   separa en dos tablas (50-3 y 50-4). Ninguna de las dos es una patologia del
   motor, y el motor no formula por consistencia. Queda apuntado y no se aplica.

### cap.51 — Introduction to Gastric Diseases (132 lineas, LEIDO ENTERO)

**Nada que aplicar, y es un capitulo puente**: lista razas predispuestas
(Tabla 51-1) y dosis de farmaco (Tabla 51-2). Su unica frase con forma de
recomendacion es de manejo clinico, no de formulacion: «In most vomiting cases of
less than 48 hours' duration, withholding water for 24 hours and food for 24 to
48 hours generally controls the episode».

### cap.52 — Gastritis and Gastroduodenal Ulceration (931 lineas, LEIDO ENTERO)

**No hay patologia «gastritis» en el motor, y despues de leerlo entero sigo
pensando que no debe haberla** —es un cuadro agudo que se maneja con ayuno,
fluidos y farmacos, no formulando una racion—, pero sus cifras quedan escritas
porque son las mismas que repiten los caps.54 y 56 y porque **si algun dia se
anade, ya estan medidas**: potasio 0,8-1,1 %MS (2000-2750 mg/1000 kcal), cloruro
0,5-1,3 %MS (1250-3250), sodio 0,3-0,5 %MS (750-1250), grasa <15 %MS en el perro,
fibra ≤5 %MS y proteina ≤30 %MS.
⚠️ Y una de ellas **chocaria de frente con lo que el motor ya aplica**: ese suelo
de sodio de 750 vive por debajo del techo de 1000 que
`recomendaciones_libro.json` pone al adulto sano, o sea que caben los dos; pero
el **suelo** de 750 y el techo de 1000 dejan una ventana de nada. Es la misma
forma de choque que ya esta escrita para el selenio del perro de trabajo. No se
aplica nada.

### cap.53 — Gastric Dilatation and GDV (592 lineas, LEIDO ENTERO)

**Cotejado linea a linea contra `riesgo_gdv` en `patologias.json`, y esta
completo**: los nueve factores de riesgo dieteticos, los dos protectores con su
cita literal, y la contradiccion declarada de la grasa (Raghavan 2006 contra
Raghavan 2004, misma poblacion) que es por lo que no se pone tope. Nada que
anadir de cifras.

Dos matices que la ficha no recoge y que son de la Tabla 53-1, apuntados sin
aplicar porque **ninguno de los dos es un nutriente**:
· **Estar delgado es factor de riesgo**: «Lean body condition (body condition
  score ≤2/5)». El motor pregunta la condicion corporal y calcula el peso
  objetivo con ella, asi que el dato ya lo tiene.
· **Ejercicio de mas de dos horas al dia** figura como factor de riesgo por su
  cuenta, aparte del ejercicio postprandial que el aviso si menciona.

### cap.54 — Gastric Motility and Emptying Disorders (576 lineas, LEIDO ENTERO)

**Repite las mismas cifras del cap.52** (los tres electrolitos identicos, grasa
≤15 %MS perro, fibra ≤5 %MS) y anade densidad energetica 4,0-4,5 kcal/g MS. No
hay patologia de vaciado gastrico en el motor y no se propone una. Nada que
aplicar.

### cap.55 — Introduction to Small Intestinal Diseases (412 lineas, LEIDO ENTERO)

1. **⚠️ La Tabla 55-1 pone «Raw meat consumption» en la columna «Dietary» de las
   causas de diarrea aguda de intestino delgado.** Es la **cuarta** fuente del
   libro que senala la carne cruda, despues del cap.11 (las cifras duras: 64 % de
   E. coli y 20 % de Salmonella en dietas crudas comerciales), del cap.19 y del
   cap.56. Aqui no hay cifra: es una entrada de tabla. No cambia nada de lo ya
   escrito, y se apunta para que el recuento sea honesto.

2. **La lactosa, con umbral y sin ficha que lo mida.** El Recuadro 55-3: «In one
   study, dogs developed diarrhea while consuming more than 1 g of lactose/kg body
   weight, an amount equivalent to about 20 ml milk/kg body weight or three-fourths
   cup of milk for a 10-kg dog». Y el motivo: «After weaning age, lactase decreases
   to about 10% of peak activity in dogs». El catalogo tiene lacteos —yogur, queso,
   kefir, leche, que `exclusiones.py` agrupa en su propia familia— y **ninguna ficha
   lleva columna de lactosa**, asi que el motor no puede medir ese umbral ni
   aunque quisiera. Es dato que falta, no codigo: va a `DATOS_QUE_FALTAN.md` y
   **no lo rellena el asistente**.

### cap.56 — Acute Gastroenteritis and Enteritis (1.506 lineas, LEIDO ENTERO)

**El aviso de la carne cruda, otra vez y con las tres frases juntas**:
«Consumption of raw food diets has been associated with bacterial enteritides»;
«Cultures of home-prepared and commercially available raw foods have demonstrated
bacterial pathogens including Salmonella spp., Campylobacter spp., Escherichia
spp. and Yersinia spp.»; y la que mas importa para quien vive con el perro,
«Dogs consuming such foods shed bacterial pathogens at a much higher rate than
those consuming conventionally cooked commercial foods». Las tres apuntan al
mismo pendiente de producto del cap.11, que ya esta escrito. **No hay cifra
nueva**: el cap.11 es el que trae los porcentajes.

Sus cifras de formulacion (grasa 12-15 %MS, fibra ≤5 %MS o 7-15 %MS segun
estrategia, digestibilidad ≥87 % proteina) son del alimento terapeutico de la
fase aguda y **no se aplican**, por lo mismo que las del cap.52.

### cap.57 — Inflammatory Bowel Disease (1.460 lineas, LEIDO ENTERO)

**La Tabla 57-1 esta aplicada entera** en `enteropatia_cronica`: potasio 2750,
grasa 37,5 y proteina 62,5, cada una con su conversion y su margen, y el aviso
lleva la B12 con la pauta. Cotejado fila por fila, no falta ninguna.

**Lo que falta es del TEXTO, y por eso no lo encontro el trabajo de transcribir
tablas**: la dosis de omega-3. «A reasonable starting dose estimated from human
and animal trials is approximately 175 mg (range 50 to 300 mg) omega-3 fatty
acids/kg body weight/day». Para un perro de 22 kg son **3,85 g de omega-3 al
dia**. No esta en `patologias.json` ni en el bloque de limites escritos que el
solver no aplica.
⚠️ Y el propio capitulo dice **por que no se puede aplicar tal cual**: «To date,
there are no published therapeutic trials investigating the efficacy of omega-3
fatty acid supplementation in dogs or cats with IBD» y «there is no well-established effective dose for dogs and
cats». O sea que es exactamente el mismo
caso que el omega-3 del cancer y el de la artrosis, que ya viven en
`limites_escritos_que_el_solver_no_aplica` con su medida. **Su sitio es ese, y hoy
no esta escrito en ninguna parte.** Decision de Elena; lo que si es un hueco de
registro es que no figure.

Dos cosas mas del texto, apuntadas y sin aplicar porque las dos son clinicas y
condicionales: el **zinc** («Supplemental dietary zinc intake should be considered
if dogs and cats with IBD have poor coat quality or dermatitis») y el **magnesio**
(«Hypomagnesemia has been reported to occur in 30% of dogs and cats hospitalized
for GI disorders»). Ninguna de las dos trae cifra dietetica.

### cap.58 — Protein-Losing Enteropathies (765 lineas, LEIDO ENTERO)

**Tabla 58-1 aplicada entera** en `ple_linfangiectasia`: grasa 37,5, fibra 12,5,
proteina 62,5. La cuarta fila, densidad energetica >3,5 kcal/g MS, no es un
nutriente por 1000 kcal y no tiene forma de restriccion del motor.

Del texto, una cosa concreta que el aviso no dice y que si es accionable para
quien cocina: la **clara de huevo cocida** como refuerzo de proteina, con dosis
—«Provide a minimum of one to two cooked large egg whites per 10 kg body weight
as needed to maintain serum albumin levels above 2 g/dl»—. Ojo con la palabra
**cooked**: en una racion cruda la clara va cruda, y eso no es lo que dice la
fuente. Apuntado, no aplicado.

### cap.59 — Short Bowel Syndrome (887 lineas, LEIDO ENTERO)

**Nada que aplicar y hay que poder decirlo**: es un cuadro **posquirurgico** que
el propio capitulo maneja con nutricion parenteral y sondas. No hay patologia
suya en el motor y no se propone una. Su Tabla 59-1 repite grasa 12-15 %MS y
fibra ≤5 %MS, que ya estan por otras patologias, y anade dos cosas que el motor
no puede expresar: «Lactose free» y «Dry foods are preferred».

### cap.60 — Small Intestinal Bacterial Overgrowth (525 lineas, LEIDO ENTERO)

**Tabla 60-1 aplicada**: grasa 37,5 en `sibo`. La otra fila es digestibilidad, que
no es una restriccion del motor. Nada nuevo.

### cap.61 — Introduction to Large Intestinal Diseases (94 lineas, LEIDO ENTERO)

Capitulo puente, tres tablas de causas y razas. **Nada que aplicar.**

### cap.62 — Large Bowel Diarrhea: Colitis (1.273 lineas, LEIDO ENTERO)

La colitis la cubre `enteropatia_cronica`, y su Tabla 62-1 **no aporta ningun
limite mas estricto** que los ya aplicados: grasa 8-15 %MS (mismo techo, 37,5),
potasio 0,8-1,1 (mismo, 2750), fibra ≤5 o ≥7 (los dos enfoques opuestos que ya
estan explicados en el aviso por los que no se pone numero).
Su fila de proteina, «Adult dogs: 15 to 30%», **no es un limite de la colitis**: el
texto la ata a la etapa —«Protein should be provided at levels sufficient for the
appropriate lifestage of colitis patients unless PLE is present»— y remite a los
caps.13 y 20. Ese 30 %MS del adulto sano ya esta apuntado y medido en el cap.13
de esta misma lectura.

### cap.63 — Idiopathic Bowel Syndrome (426 lineas, LEIDO ENTERO)

**Tabla 63-3 aplicada**: fibra 20,0 en `intestino_irritable` (≥8 %MS de fibra
bruta). Lo que la tabla anade y **el motor no sabe expresar** son los tres tipos
—soluble 1-5 %, mixta 5-10 %, insoluble 10-15 %— con su nota: «Any one of the
three types of fiber listed at the recommended levels can be effective, depending
on patient response». El catalogo no clasifica la fibra por tipo, asi que la unica
cifra aplicable es la de fibra bruta, que es justo la que se aplica. Correcto.

Del texto, lo que mas pesa no es nutricional: **el estres es el disparador**, y
«Abnormal personality traits, nervousness or stressors have been identified as
preceding bouts of chronic idiopathic large bowel diarrhea in approximately 40%
of IBS cases».

### cap.64 — Constipation/Obstipation/Megacolon (1.009 lineas, LEIDO ENTERO)

**Tabla 64-2 aplicada**: fibra 17,5 de suelo en `estrenimiento_cronico` (≥7 %MS).

1. **⚠️⚠️ Y AQUI ESTA EL HALLAZGO MAS SERIO DE TODA ESTA TANDA: el aviso del motor
   cuenta media verdad, y la mitad que falta es la del hueso.** El aviso dice hoy
   que la comida cruda juega a favor aqui porque lleva mucha mas agua que un
   pienso (sin comillas: esa frase es nuestra, del propio `patologias.json`, no de
   SACN5). Lo del agua es cierto y esta en la Tabla 64-2 (agua >75 %). Pero el
   capitulo dice **dos veces**, y en dos sitios distintos, lo contrario sobre la
   otra mitad de la racion:
   · «In addition, consumption of bones and raw foods has been associated with
     constipation and obstipation in dogs».
   · «Constipation and obstipation have been reported to occur in dogs consuming
     bones and raw food diets due to the large contribution bones make to such
     foods».
   La causa que nombra la fuente —**la cantidad de hueso**— es exactamente lo que
   este motor pone en todos los menus: la regla de forma pide **20-60 % de hueso
   carnoso**, y es la fuente de calcio del BARF. Un perro que ya consulta por
   estrenimiento cronico recibe hoy un aviso que le dice que su dieta juega a
   favor, sin nombrarle lo unico que la fuente senala como causa.
   **No lo cambio yo**: es texto que va al dueno sobre el producto de Elena, y la
   regla del proyecto es que eso no se decide en silencio. Pero no es una
   preferencia de producto: es una frase del motor que la fuente contradice a
   medias, y va la primera de la lista.
   Es ademas el **cuarto** dano documentado del hueso en esta relectura, con los
   del cap.19 (fracturas dentales), el cap.11 (patogenos) y el cap.50 (46 de 60
   cuerpos extranos esofagicos).

2. **La fibra soluble tiene un techo que el motor no puede ver.** «Such fibers
   should be added at no more than 5% of the total food because soluble fibers can
   significantly reduce the availability of minerals, including zinc, calcium, iron
   and phosphorus». Y la nota de las Tablas 64-3 y 64-4: «Fiber sources should be
   insoluble or mixed. Increased levels of soluble fiber are not recommended». El
   motor sube la **fibra bruta** sin distinguir tipo porque el catalogo no lo trae.
   Queda escrito como limitacion conocida, no como fallo.

3. Y el otro extremo, que si es una contraindicacion clara y que el aviso tampoco
   dice: en el megacolon —estrenimiento sin motilidad ninguna— la fibra **empeora**
   («fiber-enhanced foods and fiber supplements are no longer effective stimulants
   of colonic motility and, worse, can contribute to obstipation»), y la Tabla 64-2
   pide ≤5 %MS. El motor tiene **una sola** patologia de estrenimiento y le sube la
   fibra siempre. Distinguir los dos cuadros es diagnostico veterinario, no de
   ficha; lo que si cabe es decirlo.

### cap.65 — Flatulence (714 lineas, LEIDO ENTERO)

**Tabla 65-1 aplicada** en `flatulencia`: proteina 75 y fibra 12,5, y el aviso
recoge **siete** de las ocho filas de ingredientes (legumbres, lacteos, cruciferas,
cebolla, frutos secos, especias, fruta), diciendo ademas cuales de ellas pueden
estar de verdad en el menu. Cotejado contra el catalogo: las seis cruciferas
existen —brocoli, coles de Bruselas, col lombarda, col rizada, coliflor, repollo—,
asi que el aviso acierta al senalarlas.

**Falta la octava fila, y es la que toca al motor por dentro**: «Vitamin-mineral
supplements — Avoid; unnecessary with most commercial foods». Los suplementos son
precisamente **la herramienta con la que este motor cierra los 43 requisitos**, y
van siempre libres por diseno. ⚠️ Pero leida entera, la fila **no se puede
trasladar**, y el motivo esta escrito en ella misma: «unnecessary **with most
commercial foods**». Un pienso completo ya lleva los micronutrientes dentro y el
suplemento sobra; una racion cruda **no los lleva**, y ahi el suplemento es lo que
la hace completa. Que no se aplique esta bien; que no este escrito por que, no.

### cap.66 — Exocrine Pancreatic Insufficiency (832 lineas, LEIDO ENTERO)

**Tabla 66-1 aplicada**: grasa 37,5 y fibra 12,5 en
`insuficiencia_pancreatica_exocrina`. Nada que corregir en las cifras.

Y dos cosas del texto que **no estan en el aviso** y que las dos son de este
producto en concreto:

1. **El pancreas CRUDO es tratamiento, y lo dice la fuente con dosis.** «If
   available, raw bovine, porcine or ovine pancreas can be effective» y «Dogs
   should receive 30 to 90 g (1 to 3 oz.) of freshly thawed, chopped pancreas».
   Ademas: «Raw pancreas can be frozen in individual doses for several months
   without losing enzyme activity», y cuando el polvo de enzimas irrita la boca
   —efecto adverso que el capitulo describe— la salida que da es esa misma: «If
   not, feeding raw pancreas should be considered». **El catalogo no tiene ninguna
   ficha de pancreas** (comprobado sobre las 163). Es de las poquisimas veces en
   toda la lectura en que la fuente recomienda algo que **solo** puede hacer una
   dieta cruda, y hoy Rawku no lo ofrece ni lo menciona. Decision de Elena, de
   producto y de catalogo.

2. **La B12, que en la EPI es mas frecuente que en la enteropatia cronica.**
   «Reports have identified cobalamin deficiency in 82% of dogs» y, tras la cita
   del estudio que va en medio, «60% of cats» con EPI, y «Cobalamin deficiency has been associated with poor outcomes in
   canine EPI». El aviso de `enteropatia_cronica` **si** lleva la advertencia de la
   B12 con su pauta; el de la EPI **no**, teniendo la cifra mas alta de las dos.

### cap.67 — Acute and Chronic Pancreatitis (1.097 lineas, LEIDO ENTERO)

**Tabla 67-3 aplicada entera, las dos filas y la condicion**: proteina 75 y grasa
37,5, que baja a 25 con el perro obeso o hipertrigliceridemico. Y el `por_que` de
la proteina recoge el mecanismo del texto —los aminoacidos libres estimulan la
secrecion pancreatica mas que la grasa—, que es lo que hace que ese techo **si**
sea de la pancreatitis y no de la etapa, al reves que el del cap.62.

Del texto, tres cifras que **no son limites y conviene tener escritas**:
· El umbral de riesgo va **por debajo** del techo de tratamiento: «Feeding a
  high-fat (>20% dry matter [DM]) food, treat or human food has often been
  associated with the onset of acute pancreatitis». 20 %MS son 50 g/1000 kcal, y
  el techo que aplicamos es 37,5. Vamos por dentro.
· El dato clinico que decide la condicion: «Serum triglyceride levels (>900
  mg/dl) increase the risk of pancreatitis in dogs» — que es justo la pregunta que
  `quien_formula_cada_patologia.json` dice que la app no hace.
· Y una que juega **a favor** de una racion cruda, apuntada sin exagerarla:
  el experimento historico se hizo con dieta alta en grasa **y baja en proteina**
  —«feeding high-fat, low-protein foods was associated with the development of
  pancreatitis and hepatic lipidic changes in dogs»—, que no es el perfil de un
  BARF. No es una exculpacion: el mismo capitulo dice que la proteina alta estimula
  la secrecion pancreatica por otra via.

### cap.68 — Hepatobiliary Disease (3.611 lineas, LEIDO ENTERO)

**El capitulo mas largo de la mitad clinica, y el que mejor sale del cotejo.** La
Tabla 68-8 tiene diez filas para el perro y el motor aplica seis en `hepatopatia`
—cobre 2,4, sodio 625, zinc 50, hierro 20, taurina 250, vitamina E 67,1—, y las
cuatro que faltan **estan todas explicadas en algun sitio del repo menos una**:

· **Densidad energetica ≥4,0 kcal/g MS**: no es un nutriente por 1000 kcal y no
  tiene forma de restriccion del motor.
· **Proteina 15-20 %MS** (37,5-50 g/1000 kcal), y 10-15 %MS con encefalopatia
  (25-37,5): las dos caen **por debajo del minimo de FEDIAF** (52,1), asi que no
  se modelan como tope — y no se han perdido: viven en `shunt_sin_encefalopatia` y
  en `encefalopatia_hepatica`, las dos declaradas **no formulables** con
  `necesita_bajo_fediaf`, `nutriente_frontera` y `objetivo_terapeutico_por_1000kcal`,
  y con la cita literal en su aviso profesional. Es exactamente como debe hacerse.
· **Vitamina C ≥100 mg/kg MS** (25 mg/1000 kcal): **no se puede aplicar y hay dos
  motivos, no uno.** El primero es de datos: la vitamina C no esta en el `MAPA` de
  `verificar.py` ni existe como columna en ninguna de las 163 fichas, porque FEDIAF
  no le pone requisito al perro —que la sintetiza—. El segundo es de la propia
  fuente, y es mas interesante: el capitulo se **contradice a proposito** segun el
  subgrupo. La Tabla 68-8 la pide, y su texto avisa de que «supplementation with
  excessive amounts of vitamin C may be deleterious in patients with increased
  hepatic copper or iron concentrations»; y el caso clinico del Bedlington lo dice
  ya sin matices: «this practice is not recommended because vitamin C promotes
  increased oxidative damage in the presence of high copper concentrations». O sea
  que en la hepatopatia **por cobre**, que es justo la que el motor topa, la fila
  de la tabla esta desaconsejada por el mismo capitulo.

· **⚠️ Y LA QUE SI ES UN HUECO: el TECHO de hierro.** La tabla dice «Iron (mg/kg)
  80 to 140», un **rango**, y el motor toma solo el extremo bajo como suelo (20
  mg/1000 kcal), con el `por_que` escrito: «Se usa el extremo bajo (20)». Pero el
  extremo alto **no es el borde de un rango cualquiera: es un techo con mecanismo
  escrito**, y el capitulo lo desarrolla en su propia seccion: «Iron is a potent
  catalyst of oxidative processes (Fenton reaction) and iron-associated hepatic
  injury may involve lipid peroxidation of membranes and damage to organelles»;
  «Foods for dogs with chronic hepatitis and those with secondary hemosiderosis
  documented by evaluation of liver biopsy specimens should avoid excessive iron
  levels»; y la frase que fija el rango entero: «Iron levels of 80 to 140 mg/kg DM
  meet the dietary allowance without providing excessive intake. This range is
  recommended for patients with liver disease». Remata con «Injectable or oral
  supplements containing iron should be avoided in these patients».
  Es el mismo tipo de decision que ya se tomo **al reves** para el potasio de la
  enteropatia cronica: alli la Tabla 57-1 daba «0.8 to 1.1%» y se aplico el
  **techo**, con el motivo escrito de que el riesgo es el exceso. Aqui el riesgo
  que la fuente describe tambien es el exceso —acumulacion hepatica de hierro— y se
  aplico el suelo.

  **MEDIDO antes de proponer nada**, sobre los 216 menus del catalogo regenerado
  (216 de 216, sin resolver nada nuevo: se recalcula el hierro de cada menu
  guardado con `valor_nutriente` y se divide por su DER):

  | | mg de hierro / 1000 kcal |
  |---|---|
  | minimo | 18,4 |
  | mediana | 25,6 |
  | maximo | 37,4 |
  | por encima del techo de 35 | **3 de 216 (1,4 %)** |

  Los tres que se pasan son `Gigante_GestanteTardia` (37,4),
  `Mini_CachorroCrecimiento#3` (36,8) y `Toy_CachorroJoven` (35,4) — **los tres de
  crecimiento o gestacion**, que es donde el minimo de hierro sube. En adulto no se
  pasa ninguno. O sea que el techo **cabe holgado** en la poblacion que de verdad
  formula esta patologia, y `hepatopatia` es ademas `formulable: false` y
  `formulable_por_profesional: true`, asi que solo entra por la puerta del
  veterinario.
  El maximo de FEDIAF es 170,45, muy por encima; el suelo de FEDIAF, 10,4. La
  ventana que quedaria seria **20-35**, y el margen profesional iria de 10,4 a 35.
  **No lo aplico**: es una cifra que decide si sale menu y la regla del proyecto es
  que eso no se cambia en silencio. Queda medido y con la comparacion contra el
  criterio que ya se uso para el potasio.

**Lo demas del capitulo confirma lo que el motor ya hace, y conviene decirlo:**

1. **El cobre esta triplemente corroborado y el `por_que` ya lo recoge entero.** La
   Tabla 68-8 pide «Copper ≤5 mg/kg» de MS = 1,25 mg/1000 kcal, mas estricto que
   los 2,4 del motor — pero 1,25 esta **por debajo del minimo de FEDIAF** (2,08),
   asi que seria prescripcion, y eso ya esta escrito en la ficha con su margen
   profesional (2,08-2,40) y el techo legal del Reglamento (UE) 2020/354 en 2,50.
   Nada que cambiar.
2. **La Tabla 68-9 es la lista de alimentos ricos en cobre y da de lleno en un
   BARF**: «Foods with very high copper content», y debajo, en filas propias, «Liver» y
   «Shellfish»; en el escalon siguiente, corazon, rinon, legumbres, setas, frutos secos y musculo. El caso
   clinico lo lleva a la practica: los caseros «should exclude liver, shellfish,
   organ meats and cereals because of their high copper content» y «Vitamin-mineral
   supplements that do not contain a copper source are recommended». El motor **no
   excluye alimentos por patologia** —solo pone topes de nutrientes—, y eso ya esta
   escrito y corregido a proposito en el aviso de `raza_predispuesta_cobre` desde el
   7 de septiembre. El tope numerico de cobre hace el mismo trabajo por otra via.
3. **El zinc de 200 mg/kg MS tiene respaldo de seguridad explicito**, que es lo que
   faltaba saber para dejarlo tranquilo: «This inclusion level is approximately
   three times the minimum recommended allowance for foods for healthy dogs and
   cats (60 and 74 mg/kg DM, respectively) (NRC, 2006), but is probably safe», con
   el estudio de dosis muy superiores sin efectos.
4. **Y una cosa de manejo que el motor no dice y la fuente si**, apuntada porque es
   la misma familia que el reparto en varias tomas del volvulo: «Multiple daily
   feedings rather than one or two large meals may benefit patients with hepato-
   biliary disease», con su motivo (menos acidos grasos libres, mejor digestibilidad
   y menos sustrato de una vez para la fermentacion colonica).

### cap.69 — Effects of Food on Pharmacokinetics (1.787 lineas, LEIDO ENTERO)

**El capitulo mejor aprovechado de todo el libro, y no queda nada por sacar de
su parte gorda.** El caso 69-1 —el teckel con bromuro potasico— ya esta entero
en el aviso `bromuro_y_cloro` de `epilepsia_idiopatica`: el caso, el mecanismo
literal, las dos comidas con su porcentaje de cloro, **la medida sobre los 216
menus del catalogo** y —lo que mas cuesta ver— que **el riesgo va al reves** en una
racion cruda, hacia la toxicidad por bromuro y no hacia la crisis. Y tambien esta
Maguire (2000) con las tres vidas medias del fenobarbital. Releido entero, no hay
nada de eso que corregir.

Tres cosas mas del capitulo, y las tres son pequenas:

1. **El techo de yodo del motor gana un segundo mecanismo, independiente del que
   ya tenia.** `seguridad.py` topa el yodo por seguridad cronica (1275); este
   capitulo anade la via contraria a la que uno espera: «Excessive dietary intake
   of iodine can lead to a paradoxical “iodine toxicosis goiter” through what is
   referred to as the “Wolff-Chaikoff effect.”» — o sea que el exceso de yodo
   produce **deficit** de hormona tiroidea, no exceso. No cambia la cifra; refuerza
   por que hay cifra.

2. **La tiramina y los inhibidores de la MAO, que es un aviso posible y hay que
   contarlo con su matiz.** El cap.69 lista, entre los factores no nutritivos que
   estorban a un farmaco, «tyramine in chicken livers and aged cheeses, which
   confound the action of monoamine oxidase inhibitors». Y el cap.35 dice cual es
   el farmaco del perro: «Selegiline is licensed for treatment of cognitive
   dysfunction in dogs in North America» y «Selegiline is a selective and irre-
   versible inhibitor of MOA-B in dogs». El catalogo lleva higado de pollo y queso,
   y `disfuncion_cognitiva` es una patologia del motor.
   ⚠️ **Pero el enlace no lo cierra la fuente y no voy a cerrarlo yo**: la reaccion
   clasica de la tiramina es con los inhibidores **no selectivos** o de MAO-A, y la
   selegilina a dosis terapeutica es selectiva de MAO-B. SACN5 nombra las dos cosas
   en dos capitulos distintos y **no las junta en ninguna parte**. Queda apuntado
   como pregunta para el clinico, no como aviso.

3. **La interaccion de la selegilina que SI dice el cap.35 con todas las letras, y
   que hoy no esta en el aviso de `disfuncion_cognitiva`**: «Although selegiline can
   be used concurrently with most veterinary therapeutic foods and supplements, it
   should not be combined with narcotics, antidepressants or monoamine oxidase
   inhibitors. Therefore, it should probably not be used with supplements containing
   tryptophan, St. John's wort or Ginkgo biloba».
   **Comprobado contra el catalogo: hoy es inerte.** Ninguna de las 163 fichas es un
   suplemento de triptofano, de hiperico ni de ginkgo — las categorias de suplemento
   del motor son multivitaminico, omega-3, calcio, hierro, yodo, vitamina B y fibra.
   O sea que el motor **no puede** meter ninguno de los tres. Se apunta por lo mismo
   que se apuntan los `documentado_sin_cifra`: para que el dia que alguien proponga
   una ficha de triptofano —que es un aminoacido del `MAPA`, asi que no seria raro—
   esta frase ya este escrita y no haya que redescubrirla.

### cap.70 — Feeding Small Pet Mammals (2.585 lineas, LEIDO ENTERO)

**El ultimo capitulo del libro, y no toca al perro en nada.** Va de hurones,
conejos y roedores: cobayas, chinchillas, hamsters, jerbos, ratas y ratones. Lo
leo entero de todas formas y **por el motivo de siempre**, que es la leccion del
cap.46: apartar un capitulo por su titulo es como se descarto una vez la nota d
del selenio, que era del perro. Aqui el barrido sale limpio de verdad — las dos
unicas veces que aparece la palabra «dog» en 2.585 lineas son «ferrets fed low-quality cat or dog food have a much higher incidence of
struvite urolithiasis» y
la descripcion anatomica de los dientes de un conejo, donde «Canine teeth are
absent».

Las cifras del capitulo son de otras especies y **ninguna se traslada**: proteina
30-35 %MS y grasa 15-20 %MS del huron (que es carnivoro estricto, como el gato),
la vitamina C del cobaya —que es de las poquisimas especies que no la sintetiza,
al reves que el perro—, el calcio del conejo, que **se excreta por la orina en vez
de por la bilis** y por eso le da urolitiasis donde a otros no.
Una sola cosa **rima** con algo del perro sin ser aplicable, y se apunta como
curiosidad y no como hallazgo: el limite de higado del huron por la vitamina A
—«no more than 30 g of liver should be added per 800 kcal»— es la misma
preocupacion que en el perro resuelve, por otra via y con otro numero, el maximo
de vitamina A de FEDIAF que el motor ya aplica.

---

## Fin de la relectura integra de SACN5

Con el cap.70 quedan **los setenta capitulos leidos enteros**, de la primera linea
a la ultima, y apuntado capitulo por capitulo en este documento. Lo que sale de
los veinte ultimos (50 al 70) esta arriba; el resumen de lo que hay que **decidir**
—que no es lo mismo que lo que hay que leer— sigue viviendo en
`HALLAZGOS_SACN5_10SEP.md` y en los pendientes por tema.
