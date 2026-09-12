# Dónde las fuentes no dicen lo mismo, y qué aplica el motor

**Escrito el 11 de septiembre de 2026**, a petición de Elena, para que vaya en el
documento que lee el nutricionista.

## La regla, en una línea

**Si otra fuente contradice a FEDIAF, gana FEDIAF.** Pero la discrepancia se
apunta, con las dos cifras y con la que aplicamos, porque quien firma una pauta
tiene derecho a saber que existe.

## Y una distinción que hace falta antes de leer la lista

«Contradecir a FEDIAF» **no** es lo mismo que «pedir otra cosa que FEDIAF». Casi
todas las cifras de este motor que no son de FEDIAF **caben dentro** de FEDIAF:
aprietan el mínimo hacia arriba o el máximo hacia abajo, sin salirse de la
ventana. Eso no es un conflicto y se aplica sin más — es lo que hacen los topes
de patología, los del libro y los condicionales, todos con `min()` y `max()`, que
solo pueden apretar.

Hay conflicto **solo** cuando la otra fuente sacaría al perro **fuera** de la
ventana de FEDIAF. Ahí es donde manda FEDIAF, y de eso va la primera tabla.

## Y un límite de la regla que pone la propia FEDIAF (11 de septiembre, releyéndola entera)

«Gana FEDIAF» es verdad **para el perro sano**, y hay que decirlo así porque
FEDIAF **se excluye a sí misma** del otro caso. Su §2.2, al declarar el alcance:

> *«Excluded from the FEDIAF's Nutritional Guidelines are pet foods for
> particular nutritional purposes and some other specialised foods such as for
> sporting dogs etc. Therefore specific products may have nutrient levels that
> are different from those stated in these guidelines.»*

Una dieta para una patología es exactamente uno de esos alimentos: el
Reglamento (UE) 2020/354, que es quien las regula, las define como alimentos
*«intended for particular nutritional purposes»*. O sea que en una dieta clínica **quien pone el suelo es la ley, no
FEDIAF**, y la ley sí permite bajar de algunos mínimos de FEDIAF para objetivos
concretos (urato 36,9 y cistina 45,5 g/1000 kcal de proteína, con cuatro
condiciones escritas; están en `limites_legales_ue_2020_354.json`).

Y no es la única frase de FEDIAF en esa dirección. Hay **tres** más, y la
tercera trae la condición:

- §2.2: *«Pet foods can be adequate and safe when nutrient levels are outside
  the recommendations in this guide, based on the manufacturer's substantiation
  of nutritional adequacy and safety.»*
- §3.1.b: *«If certain nutrient levels are outside the values stated in this
  guide, manufacturers should be able to prove that the product provides
  adequate and safe intakes of all required nutrients.»*
- §3.3.1, proteína: *«If formulating below the recommended minimum for total
  protein it is particularly important to ensure that the amino acid profile
  meets FEDIAF guidelines for adult maintenance.»* — que es justo lo que pide
  Cris Carles para el IRIS 4, y la condición **ya se cumple** en este motor:
  los 12 aminoácidos esenciales se verifican uno a uno desde el 28 de agosto.

**Qué cambia esto en el motor: nada.** Elena lo decidió y la decisión sigue:
*los requisitos se respetan SIEMPRE, eso no se negocia*. Lo que cambia es lo
que se puede **afirmar**: hasta hoy este documento decía que FEDIAF manda en
todos los casos, y la propia FEDIAF dice que en las dietas clínicas no. Quien
firma una pauta tiene derecho a saberlo, que es la razón de ser de este fichero.

---

## 1 · Conflictos de verdad: la otra fuente se sale de FEDIAF y NO se aplica

| Nutriente | Dice FEDIAF | Dice la otra fuente | Qué aplica el motor |
|---|---|---|---|
| **Selenio** | máximo **142 µg/1000 kcal** (Tabla III-3b) | SACN5 caps. 13, 14 y 47 recomiendan **0,5-1,3 mg/kg MS = 125-325 µg/1000 kcal** | **El máximo de FEDIAF, 142.** El 56 % superior del rango del libro queda fuera |
| **Ratio Ca:P del cachorro de raza grande** | techo **1,6** (nota b de la Tabla III-3b) | SACN5 da **1,5** en una de sus tablas de crecimiento | **El 1,6 de FEDIAF.** Detalle y la contradicción interna del propio libro: `HALLAZGOS_SACN5_10SEP.md` §S-5 |
| **Energía del cachorro** | curva de Klein (Tabla VII-7) | SACN5 Tabla 33-8, tomada de NRC 2006, llega hasta un **28 % por encima** | **La de FEDIAF.** Es la más conservadora: dar de más a un cachorro de raza grande es exactamente lo que causa enfermedad ortopédica del desarrollo |
| **Edad a la que un perro es sénior** | escalón de la Tabla VII-6, **7 años** para todos | NRC 2006 cap.4: *«Generally, giant- and large-breed animals are considered geriatric at 5 years of age, whereas medium- or small-breed dogs and all cats are not considered geriatric until 7 or more years of age»* | **Los 7 años de FEDIAF.** Y hay un matiz: NRC ahí está **definiendo una palabra**, no publicando un requisito, mientras que el escalón que el motor aplica es una tabla de energía |
| **Yodo** | máximo **2750 µg/1000 kcal** | SACN5 le atribuye al NRC un límite que **el propio NRC dice que no se puede fijar** | **El tope crónico del motor, 1275 µg/1000 kcal**, que es más estricto que los dos. Detalle: `HALLAZGOS_SACN5_10SEP.md` §S-7 |
| **Calcio del cachorro de raza grande** | mínimo **2500** mg/1000 kcal (fila `Calcio_LateGrowth_RazaGrande`, nota b) | Fascetti cap. 10, escrito por Hazewinkel, que es quien hizo los experimentos: **0,8-1,0 % de materia seca por 4200 kcal/kg = 1905-2381 mg/1000 kcal**, y su recomendación final es ~1,0 % | **El techo de 2750 que ya aplica el motor** (1,1 % MS, del mismo capítulo). El rango que recomienda su autor queda **entero por debajo del mínimo de FEDIAF**, así que aplicarlo dejaría al cachorro corto de calcio. Detalle y las cuatro cifras: `HALLAZGOS_FASCETTI.md` §F-7 |
| **Grasa en linfangiectasia** | mínimo **13,75** g/1000 kcal, sin máximo | El mismo «15 %» en **dos unidades**: SACN5 Tabla 58-1 lo da en **materia seca** (= 37,5 g/1000 kcal) y Fascetti cap. 11 en **kcal** (= 16,7). Un factor de 2,2 | **Los 37,5 de SACN5.** Medido con el solver y 40 s en perros de 10, 20 y 35 kg: con 16,7 y con 20,0 **no sale menú en ninguno**. Lo que hay que decidir antes que el número es **qué unidad lleva el 15 %**. Detalle: `HALLAZGOS_FASCETTI.md` §F-9 |
| **Proteína en hepatopatía** | mínimo **52,1** g/1000 kcal en adulto | Fascetti cap. 13: las dietas hepáticas del mercado llevan **14-15,5 % de las kcal en proteína = 35-38,75 g/1000 kcal** | **El mínimo de FEDIAF.** Formular por debajo del mínimo es la fase 4 de `VETERINARIOS.md` y exige una prescripción declarada que viaje con el menú; todavía no existe |

### Y un caso al revés: FEDIAF dice algo que no cabe

| Nutriente | Dice FEDIAF | Qué pasa | Qué aplica el motor |
|---|---|---|---|
| **Techo de lisina en crecimiento** | **7,00 g/1000 kcal** | **0 de 12 menús de cachorro caben debajo** (van de 8,24 a 11,48, mediana 9,03). La lisina va detrás de la proteína, y una ración BARF de cachorro lleva ~134 g/1000 kcal contra un mínimo de 50 | **No se aplica**, y es la **única** excepción escrita de todo el motor. Vive en `verificar.MAXIMOS_NO_APLICADOS`, con la pregunta abierta. El **mínimo** de lisina sí se aplica |

---

## 1-bis · El REQUISITO de calcio:fósforo lo fija FEDIAF; lo que pida una patología es otra cosa

Escrito el **12 de septiembre de 2026**, decidido por Elena en dos mensajes del
mismo día. El primero:

> *«El ratio Ca:P viene de fediaf, ya sabes como va el orden de fuentes que
> mandan»*

Y el segundo, acotando el alcance —porque yo había aplicado el primero de más y
había cerrado con él también la pregunta del renal:

> *«Lo que te decia del ratio me referia al requerimiento, si alguna patologia
> necesita algo distinto es otra cosa»*

O sea que la regla es sobre **el requisito**: el del perro que no tiene nada, que
es el que FEDIAF publica. Una patología que pida su propio cociente se decide como
cualquier otro de sus 79 límites — con su fuente, su conversión y su medida.

Hacía falta una entrada propia porque el Ca:P es **la cifra del repo que más
fuentes vuelven a dar**: cinco bandas distintas para lo mismo, y dos de ellas
caben enteras dentro de la de FEDIAF, así que no saltaban como conflicto.

| Fuente | Banda | Qué le hace a la ventana de FEDIAF | Estado |
|---|---|---|---|
| **FEDIAF**, perro sano (Tabla III-3b) | **1,0-2,0** | es la ventana | **aplicada** |
| **FEDIAF**, cachorro de raza grande (nota b) | techo **1,6** | la aprieta **FEDIAF a sí misma** | **aplicada** |
| SACN5 Tablas 40-5 y 41-6, urolitos de calcio | 1,1-**2,0** | sube el suelo a 1,1 y **deja el techo de FEDIAF intacto** | **aplicada** en `oxalato` |
| Bartges (Ettinger cap.184), enfermedad renal crónica | 1,1-**1,3** | sube el suelo **y baja el techo** | **no aplicada, y la pregunta sigue abierta** — es de una patología, o sea «otra cosa». P-30 |
| TVT Merkblatt 181, perro sano | 1,3-**1,5** | sube el suelo **y baja el techo** | **no se aplica** — es un requisito rival del de FEDIAF. P-23, cerrada |

**La línea que las separa es a QUIÉN se lo piden.** El de la TVT habla del perro
**que no tiene nada**, que es exactamente de quien habla FEDIAF: es un requisito
rival, y ahí manda FEDIAF y se acabó. Los del oxalato y del renal los pide una
**patología marcada**, que es la regla 2 del proyecto y la misma forma que tienen
los otros 79 límites: uno está aplicado y el otro está por decidir, cada uno por
su cuenta.

Y en el renal hay un dato que conviene tener delante al decidirlo, y es de la
propia frase de Bartges: su otra mitad —el fósforo al 0,2-0,5 % de materia seca—
**ya está aplicada**, con el techo de 1.200 mg/1000 kcal. El fósforo es el
denominador del cociente, así que el motor ya aprieta ese ratio por un lado.

---

## 2 · Lo que otra fuente aprieta DENTRO de FEDIAF, y sí se aplica

Esto no es conflicto. Son cifras de un libro o de una guía clínica que caen
dentro de la ventana de FEDIAF y la estrechan.

| Nutriente | Ventana de FEDIAF | Lo que aprieta | De dónde sale |
|---|---|---|---|
| **Fósforo, adulto sano** | 1160 a **4000** mg/1000 kcal | techo **2000** | SACN5 Tablas 13-3 y 47-4. El libro recomienda **la mitad** del máximo de FEDIAF, y una ración BARF salía pegada a ese máximo |
| **Fósforo, sénior sano** | igual | techo **1750** | SACN5 Tabla 14-2 |
| **Sodio, adulto y sénior** | 290 a 3750 | techo **1000** | SACN5 Tablas 13-3, 14-2 y 47-4 |
| **Calcio y fósforo del cachorro** | calcio 2000-4500; el fósforo **en crecimiento** no tiene máximo en FEDIAF (en adulto sí: 4,00 g/1000 kcal) | 4250/3250 (adulto <25 kg) y **2750/2750** (>25 kg) | SACN5 Tabla 17-1 (dos columnas) y Fascetti cap.10. El techo de fósforo **de crecimiento** es el único que tiene un cachorro: las dos celdas de máximo de esa fila de FEDIAF están vacías |
| **Vitamina E, adulto y sénior sanos** | mínimo 6,968 mg, **sin máximo** | suelo **67,1 mg/1000 kcal** — ⚠️ **escrito y HOY APAGADO** | SACN5 Tablas 13-3 y 14-2, ≥400 UI/kg MS, dicho en **cinco capítulos**. Se encendió y se apagó el mismo 11 de septiembre: encendido deja sin menú a los tres perros con ocho especies fuera y pone roja la batería. La cifra **no se ha bajado**; está escrita con su medida y se pregunta. Ver la regla 2 de `CLAUDE.md` |
| **Vitamina D, yodo, selenio, mercurio, tiaminasa** | los máximos de la Tabla III-3b | los cinco topes crónicos de `seguridad.py`, todos más estrictos | NRC 2006 y la literatura citada en cada línea del fichero |
| **Los 75 límites de patología** | la ventana de FEDIAF de cada nutriente | siempre dentro | `patologias.json`, cifra a cifra con su fuente. `auditar_patologias.py` comprueba que **ninguna** patología formulable tenga un tope por debajo del mínimo de FEDIAF |
| **Proteína de gestación y lactancia** | el mínimo de la Tabla III-3b | sube, porque FEDIAF lo calcula suponiendo hidratos que una ración BARF no lleva | NRC 2006 (Kienzle 1985): con la dieta sin hidratos y la proteína baja, la mortalidad perinatal subió un **75 %** |
| **Arginina** | Tabla III-3b | sube con la proteína, por la **propia** Tabla VII-13 de FEDIAF | Es FEDIAF contra FEDIAF, y se aplica la más estricta de las dos |

---

## 3 · Donde FEDIAF no dice nada, y por eso manda la otra fuente

| Tema | FEDIAF | Lo que hay |
|---|---|---|
| **Fibra** | no da ni mínimo ni máximo para perros | ocho patologías con suelo o techo, todas de tablas de SACN5. ⚠️ **Y están en una unidad distinta de la del catálogo** — ver `PENDIENTE_NUTRICION.md`, apartado de la fibra |
| **Taurina y L-carnitina** | no son requisito para el perro (sí la taurina para el gato) | suelos reales en `dcm_taurina_respondedora`, de SACN5 Tabla 36-4 |
| **Vitamina K** | no la publica para el perro | el NRC sí, y el catálogo **no la tiene en ninguna ficha**. Pendiente de dato, no de código |
| **Ratio linoleico:linolénico** | lo enuncia y no lo cuantifica | 2,6-26 en adulto y crecimiento, de NRC 2006 cap.5, **aplicado**. NRC dice además que el ratio omega-6:omega-3 totales *«is not helpful»* |
| **Máximo de vitamina E** | ninguno en ninguna etapa | **APLICADO el 11-sep-2026 por la noche: 167,75 mg/1000 kcal**, el extremo estricto. ⚠️ **Y lo que lo desbloqueó fue la SEGUNDA fuente**: SACN5 cap.13 ya recogía *«An upper limit of 1,000 to 2,000 IU/kg food (DM) has been suggested for dogs»* (AAFCO 1985, NRC 1985) y se había dejado sin aplicar por ser «un rango sugerido»; al cerrar el cap.14 de Fascetti apareció la misma horquilla citando **NRC 2006**, o sea la edición vigente. Dos fuentes independientes y la misma cifra deja de ser una sugerencia suelta. Medido antes de aplicarlo: los 216 menús del catálogo van de 10,05 a 89,28 mg/1000 kcal, **0 por encima** |
| **Máximo de EPA+DHA** | ninguno en ninguna etapa | **APLICADO el 11-sep-2026 por la noche: 2,8 g/1000 kcal** (Fascetti cap.14 citando NRC 2006, y la fuente lo repite por peso metabólico: *«<370 mg × BW(kg)0.75»*). ⚠️ Es el único de los tres techos de esa frase que **sí aprieta**: medido antes de aplicarlo, **5 de los 216 menús** se pasaban, hasta 3,00. Obligó a regenerar el catálogo |
| **Mínimo de proteína del perro** | 52,1 g/1000 kcal en adulto | **NRC 2006 dice 20** (*«2.62 g/kg BW0.75 or 20 g/Mcal»*, citado por Fascetti cap.15). ⚠️ **Gana FEDIAF y el motor no baja de 52,1**, y además las dos cifras no miden lo mismo: la del NRC es un requerimiento mínimo suponiendo biodisponibilidad del 100 % y la de FEDIAF una recomendación para una dieta completa. Se apunta porque **es el número que bloquea el IRIS 4** que pide la revisión de Cris (15 % MS = 37,5 g/1000 kcal, entre los dos). Bajar el mínimo general NO es la solución: la solución es la vía firmada de `VETERINARIOS.md`, donde una prescripción por debajo de FEDIAF viaja con su propio juego de requisitos |
| **Energía del hueso carnoso** | no se pronuncia | NRC excluye el hueso de los factores de Atwater, que es lo que usa el catálogo. Medido: el error está acotado en un dígito por ciento y no hay cifra que aplicar. `PENDIENTE_NUTRICION.md` |
| **Triglicéridos de cadena media en la epilepsia** | no dice nada | AAHA 2021 Tabla 8 pide «High medium-chain triglycerides» y **no da cifra**. El motor no tiene clave para medirlos. No se aplica: P-21 |
| **Proteína del diabético** | 52,1 g/1000 kcal de mínimo general, nada específico | AAHA 2021 Tabla 8 pide «High protein (unless contraindicated, e.g., proteinuria)» y **no da cifra**. `diabetes` lleva solo el suelo de fibra. No se aplica: P-21 |
| **Proteína de la nefropatía con pérdida de proteínas** | nada | AAHA 2021 Tabla 8 da «25-50% protein reduction from current intake», que es **relativo a lo que el perro come hoy** y el motor no lo sabe. `renal_proteinuria` sigue sin ninguna cifra. P-21 |

---

## 3-quater · Ettinger cap.185 contra SACN5, en el oxalato — y es sobre una patología que el motor SÍ formula

⚠️ Añadido el 12 de septiembre. FEDIAF no entra aquí: no da topes por patología.
Son **dos fuentes clínicas que apuntan en direcciones contrarias** sobre los mismos
tres nutrientes.

| | Lo que dice | Lo que hace el motor |
|---|---|---|
| **SACN5**, Tablas 40-5 y 41-6 | Recomendaciones de formulación para el perro que ya forma cálculos de oxalato: bajar sodio, fósforo y magnesio | **Aplicado**: techos de 750, 1.500 y 375 mg/1000 kcal en `oxalato` |
| **Ettinger cap.185** (Queau y Biourge) | *«En perros alimentados con dietas secas y húmedas, el riesgo de urolitiasis por CaOx fue mayor para perros que consumieron dietas con los niveles más bajos de proteína, sodio, potasio, calcio, fósforo y magnesio»*. Y usa el sodio **a propósito** para provocar diuresis, por encima de **2,5 g/1000 kcal** | — |

O sea que el motor **baja** tres de los seis nutrientes que la segunda fuente asocia
a **más** riesgo en el perro, y su cifra de sodio para diuresis es más de **tres
veces** nuestro techo.

**No se cambia nada, y por qué**: lo de SACN5 son recomendaciones de formulación
para el perro enfermo y lo de Ettinger es un estudio epidemiológico retrospectivo
sobre dietas comerciales — dos clases de dato distintas. Y el propio capítulo lo
relativiza: *«Se conoce poco sobre el papel que desempeñan los precursores
dietéticos en la fisiopatología del CaOx»*.

Pero queda escrito, porque es **la primera vez que dos fuentes del repo se
contradicen sobre una patología que el motor sí formula**, y quien firme una pauta
de oxalato tiene derecho a saberlo.

---

## 3-bis-bis · TVT Merkblatt 181, leído entero el 12 de septiembre

Es la única fuente del repo que trata **este producto**. Da dos cifras que el
motor no usa, y las dos son de FORMA o de recomendación, no de requisito:

| Tema | FEDIAF | TVT | Qué hace el motor |
|---|---|---|---|
| **Ratio calcio:fósforo** | 1,0-2,0 | «optimal 1,3 – 1,5», igual en 2017 y en 2025 | **El de FEDIAF**, y desde el 12 de septiembre eso está **decidido, no pendiente**: el ratio Ca:P lo fija FEDIAF. Medido: de 216 menús del catálogo, **188 están por debajo de 1,3**. P-23 cerrada. Ver §1-bis |
| **Proporciones clásicas del BARF** | no se pronuncia (no es nutrición) | 60-80 % carne · 10-30 % hueso carnoso · 10-25 % verdura y fruta | La plantilla del motor parte de **50 % de hueso** (margen 20-60 %) y 10 % de verdura (margen 2-10 %), o sea por encima del máximo de hueso y por debajo del mínimo de verdura que publica esta fuente. Es FORMA (regla 3) y lo que legitima la ración es la verificación contra FEDIAF, no la plantilla — pero es la primera fuente **veterinaria publicada** que da otras proporciones, y queda escrito |

---

## 3-ter · AAHA 2021, leída entera el 12 de septiembre

Es la fuente de la que salen la banda de BCS 4-5 y el 10 % de los premios, y se
había citado 59 veces sin leerla. Al leerla entera aparecen tres cosas de esta
lista.

**Una donde manda FEDIAF y AAHA cabe dentro.** Su Cuadro 1 da los factores
caninos sobre el RER (peso^0,75 × 70): adulto castrado 1,4-1,6, entero 1,6-1,8,
inactivo/propenso a obesidad 1,0-1,2, crecimiento 3,0 antes de los 4 meses y 2,0
después. El motor usa la Tabla VII-7 de FEDIAF y no cambia — pero la fila
«inactivo/propenso a obesidad» da 70-84 kcal/kg^0,75, que **cabe dentro** del
«Obese prone adults ≤ 90» de FEDIAF y lo confirma. Ese nivel sigue siendo el
HUECO declarado de `niveles_de_actividad.json`, ahora con dos fuentes y no una.

**Una donde AAHA es MENOS estricta que nosotros, y nos quedamos como estamos.**
«For some large- and giant-breed dogs, skeletal maturity may not be achieved
until closer to 15-16 mo». La app termina el crecimiento a los 15 meses con 25 kg
de adulto y a los 20-24 meses con 45-70 kg, o sea más tarde. Más tiempo con
requisitos de crecimiento es el lado estricto y ahí se queda.

**Y una que es conflicto de verdad, y ya estaba abierta.** Su Tabla 8 pide «Avoid
low protein» en las **tres** cardiopatías que lista, y el motor aplica al
cardíaco con renal el techo de proteína de 62,5 g/1000 kcal que viene del
Reglamento (UE) 2020/354. Es la P-19, que salió del consenso ACVIM el mismo día:
ahora son **dos fuentes clínicas independientes** contra una entrada de la ley.
No se resuelve aquí — es criterio clínico y tiene dueño.

⚠️ **Y una cosa que no es una cifra y va escrita igual**: AAHA no recomienda dar
comida cruda («AAHA does not advocate or endorse feeding pets any raw or
dehydrated nonsterilized foods, including treats that are of animal origin»), y
su Tabla 4 pone la dieta cruda entre los factores de riesgo que obligan a una
evaluación ampliada. Usamos sus números y no seguimos su recomendación de
producto. Eso es legítimo **si se dice**, y se dice: P-20.

---

## 3-bis · Donde discrepan dos fuentes ENTRE SÍ, y FEDIAF no entra

⚠️ Apartado añadido el 11 de septiembre de 2026, al cerrar los capítulos de
Fascetti. Hasta entonces esta lista solo miraba «FEDIAF contra otra fuente», y
hay un caso que no cabía en ninguna de las tres secciones: **dos fuentes que se
contradicen en un nutriente que FEDIAF no restringe para esa patología**. Ahí no
hay regla que aplicar —FEDIAF no se pronuncia— y la elección es de criterio, así
que tiene que estar escrita.

### El fósforo del oxalato cálcico

| | Qué dice | En la unidad del motor |
|---|---|---|
| **SACN5 cap.40, Tabla 40-5** (lo que aplica el motor) | *«Dietary phosphorus should be in the range of 0.3 to 0.6% DM»* | **750 a 1500** mg/1000 kcal |
| **Fascetti cap.16** | *«Dietary phosphorus should not be restricted with calcium oxalate urolithiasis. Low dietary phosphorus is a risk factor for calcium oxalate urolith formation»*, y recomienda *«approximately 1.5 to 2.0 g/Mcal»* | **1500 a 2000** mg/1000 kcal |
| Mínimo de FEDIAF en adulto | — | 1160 |

**Los dos rangos solo se tocan en un punto, y es 1500** — que es exactamente el
número que aplica el motor, tomando el techo de SACN5. No hay ninguna otra cifra
que las dos fuentes acepten.

**Medido el 11-sep, tres perros adultos por la API en peldaño estricto:** los
menús salen a 1498,7 / 1498,6 / 1498,4 mg/1000 kcal, o sea **pegados al techo**.
Una ración BARF va sobrada de fósforo y el solver sube hasta donde le dejan.

⚠️ **Y por eso no se le pone un suelo de 1500, aunque sea lo que pide Fascetti:**
el motor solo llega a 1498,7, así que ese suelo dejaría al oxalato **sin menú**.
Lo que hoy evita el problema es una propiedad del catálogo, no una garantía.
Decisión clínica pendiente, en `PREGUNTAS_ABIERTAS.md`.

### Y una forma de límite que el motor tiene y esta patología no usa

Fascetti cap.18 trae la única frase de toda la lectura que dice que **un tope
puede ser demasiado BAJO**: *«Severe sodium restriction (<50 mg/100 kcal) is not
recommended as this can cause early and prolonged activation of the
renin-angiotensin-aldosterone (RAA) system»*. Son 500 mg/1000 kcal, y el motor
aplica **480** al estadio ACVIM D.

El mecanismo para expresar eso **existe**: son los `suelos_por_1000kcal`, que ya
usan 16 patologías. Lo que no hay es la cifra, y no se pone sola por dos motivos:
la frase es del párrafo **felino**, y el estudio **canino** del mismo capítulo
usó 400 mg/1000 kcal con beneficio medido. Decisión clínica, en
`PREGUNTAS_ABIERTAS.md`.

### La grasa de tres patologías digestivas: Ettinger aprieta por debajo de SACN5

⚠️ Añadido el 12 de septiembre, al leer entera la sección XI de Ettinger. Es el
mismo caso que el fósforo del oxalato —dos fuentes clínicas y FEDIAF sin
pronunciarse, porque su único límite de grasa es un **mínimo** de 13,75— y toca
tres patologías a la vez.

| Patología | Lo que aplica el motor | De dónde sale | Lo que pide Ettinger |
|---|---|---|---|
| `enteropatia_cronica` | 37,5 g/1000 kcal | SACN5 Tabla 57-1 | cap.178: *«6-15 % de MS en perros o <3 g de grasa/100 kcal»* = **30** |
| `ple_linfangiectasia` | 37,5 | SACN5 Tabla 58-1 | cap.178, con albúmina <1,5 g/dl: *«concentraciones de grasa <3 g/100 kcal o <10 % de MS»* = **30** o **25** |
| `hiperlipidemia` | 30 | SACN5 Tabla 28-2 | cap.182: *«<25 g de grasa/Mcal en alimentos para perros»*, y en los rebeldes *«menos de 18 g de grasa/Mcal»* = **25** y **18** |

**Y aporta algo que ninguna de las otras dos tenía: la cifra en las DOS unidades a
la vez.** El caso de la linfangiectasia llevaba desde el 10 de septiembre en §1 de
esta lista como una pelea de unidades —SACN5 daba el «15 %» en materia seca (37,5)
y Fascetti el mismo «15 %» en kcal (16,7), un factor de 2,2—. Ettinger escribe las
dos («6-15 % de MS **o** <3 g/100 kcal»), cae en medio, y convierte la pregunta en
una de números y no de unidades.

Medido con el solver, escalera entera, adultos de 3, 10, 22 y 40 kg: los **30**
caben en los cuatro pesos (peldaño 2), los **25** también salvo en la enteropatía,
que se va al último peldaño por su techo de potasio, y los **18** de la
hiperlipidemia **no salen en ningún peldaño ni en ningún peso**. Las tres tablas
completas y la decisión pendiente, en `PREGUNTAS_ABIERTAS.md` P-32.

### La fibra de la diabetes: no es discrepancia de cifra, es de UNIDAD

El motor exige un suelo de **17,5 g/1000 kcal**, convertido del «7 % de materia
seca» de la Tabla 29-3 de SACN5, que está en **fibra bruta**. El cap.181 de
Ettinger da el umbral de beneficio en **fibra dietética total**, que es la unidad
del catálogo: *«la concentración de esta debe exceder los 55 g de FDT/Mcal»*, y
mide que con *«18-20 g de FDT/Mcal»* no hubo beneficio ninguno.

No es que una fuente pida más que la otra: es que **el número del motor está en la
unidad equivocada** y nadie tiene el factor para pasarlo (la Tabla 5-9 de SACN5 lo
mide entre el 0 % y el 82 % según el ingrediente). Detalle, medida y pregunta:
`PREGUNTAS_ABIERTAS.md` P-33.

---

---

## 4 · Lo que esta lista NO es

**No es todo lo que dicen las fuentes.** Es donde hay **desacuerdo** o donde
FEDIAF calla. Lo que las fuentes confirman sin discrepar —que es la mayor
parte— está en `LECTURA_SACN5_INTEGRA.md`, `LECTURA_NRC2006.md` y
`HALLAZGOS_SACN5_10SEP.md`, capítulo a capítulo.

**No decide nada de clínica.** Cada fila dice qué aplica el motor hoy y por qué.
Las que están abiertas viven en `PREGUNTAS_ABIERTAS.md` con su estado.
