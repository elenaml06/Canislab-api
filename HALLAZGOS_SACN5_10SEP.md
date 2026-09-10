# Lo que salió de leer SACN5 con inventario, el 10 de septiembre

**Escrito el 10 de septiembre de 2026**, después de montar `sacn5_tablas.json` y
empezar a darle veredicto a las 474 tablas del libro.

> **Por qué este fichero y no una línea más en `LECTURA_SACN5.md`.** Aquel es el
> cuaderno de la lectura de la noche del 9. Esto es lo que aparece **al hacer la
> lectura comprobable**: cifras caninas que el motor no aplica, cada una con su
> cita literal y su medida en vivo. Ninguna se aplica todavía, y **eso es a
> propósito**: las cuatro cambian menús de verdad y las cuatro son una decisión
> clínica, no una lectura.

---

## 1 · La vitamina E del perro sano: SACN5 pide **cuatro veces** lo que damos

Y no lo dice en un sitio, lo dice en **cinco capítulos**, todos citando el mismo
estudio de biomarcadores (Jewell et al, 2000):

| Capítulo | Población | Literal |
|---|---|---|
| 13 | adulto joven | «A prudent recommendation is that foods for young adult dogs should contain **at least 400 IU vitamin E/kg (DM)**» |
| 13 | (el estudio) | «One antioxidant biomarker study in dogs indicated that for improved antioxidant performance, dog foods should contain **at least 500 IU vitamin E/kg (DM)**» |
| 14 | maduro / senior | «foods for mature dogs should contain **at least 400 IU vitamin E/kg (DM)**» |
| 34 | artrosis | «foods for osteoarthritis should contain **at least 400 IU/kg DM** (dog foods)» |
| 37 | renal crónico | «**≥400 IU vitamin E/kg** of food for dogs» |
| 47 | salud oral | «foods for oral health should contain **at least 400 IU/kg dry matter (DM)** (dog foods)» |

400 UI/kg MS ÷ 4,0 kcal/g × 0,671 mg/UI = **67,1 mg/1000 kcal**.

**Lo que aplica el motor hoy**: el mínimo de FEDIAF para adulto, **6,968
mg/1000 kcal**. Y el suelo de 67,1 solo en dos patologías —artrosis y perro de
trabajo (500 UI/kg = 83,9)—, que salieron de este mismo número por otra puerta.

**Medido en vivo el 10 de septiembre**, resolviendo diez menús con el motor y el
catálogo reales (adulto y senior, de 3 a 40 kg):

```
vitamina E real ....... 13,3 a 19,7 mg/1000 kcal, mediana 16,7
llegan a 67,1 ......... 0 de 10
```

O sea que el perro sano recibe **la cuarta parte** de lo que su fuente
recomienda, y aplicarlo obligaría a meter un suplemento de vitamina E en
**todos** los menús.

> **DECISIÓN.** No es un requisito: SACN5 lo llama «for improved antioxidant
> performance», y FEDIAF no pone máximo de vitamina E, así que aritméticamente
> cabe. Pero cambia todos los menús y mete un suplemento nuevo. ¿Se aplica al
> perro sano, se aplica solo al senior (cap.14), o se queda escrito?

### 1.1 · Y con ella van dos más, del mismo párrafo

- **Vitamina C ≥100 mg/kg MS** = 25 mg/1000 kcal (caps. 13, 14 y 47). El perro
  **sintetiza** vitamina C y FEDIAF no le pone requisito; el catálogo no la
  lleva como nutriente. Aplicarla pediría un dato nuevo en 163 fichas.
- **Selenio 0,5-1,3 mg/kg MS** = **125-325 µg/1000 kcal** (caps. 13, 14 y 47).
  ⚠️ **El extremo alto se pasa del máximo de FEDIAF**, que son 142 µg/1000 kcal.
  Y el bajo (125) deja una ventana del 12 % contra ese máximo. El techo crónico
  del motor (570) coincide con el «maximum standard of 2.0 mg/kg (DM)» que el
  propio SACN5 da para uso regulatorio, así que ahí no hay conflicto — el
  conflicto es con FEDIAF.

---

## 2 · La grasa del cachorro de raza grande: una ración cruda se sale por mucho

**Tabla 33-6**, fila «Recommended levels», para el cachorro **en riesgo de
enfermedad ortopédica del desarrollo**:

| | Recomendado |
|---|---|
| Densidad energética | 3,2-4,1 kcal/g MS |
| **Grasa** | **8,5-17 % MS** |
| DHA | ≥0,02 % *(aplicado desde el 9 de septiembre)* |
| Calcio | 0,8-1,2 % *(aplicado: 2750 mg/1000 kcal)* |
| **Ca:P** | **1,1:1 – 2:1**, «the lower end of the range is preferred» |

17 % MS = **42,5 g/1000 kcal**. **Medido en vivo**, seis menús de cachorro de
raza grande (10, 15 y 25 kg, las dos etapas de crecimiento):

```
grasa real ............ 57,2 a 71,1 g/1000 kcal, mediana 62,6
caben bajo 42,5 ....... 0 de 6
```

Son **23-29 % de materia seca** contra el 8,5-17 % que recomienda la tabla. No
es un ajuste: es que una ración cruda de carne, hueso y víscera es
intrínsecamente más grasa que un pienso de crecimiento.

> **DECISIÓN.** Esto no se puede aplicar sin cambiar qué es una ración BARF de
> cachorro. Lo que sí se puede es **decirlo**: un aviso en el menú del cachorro
> de raza grande diciendo que la fuente recomienda una grasa más baja de la que
> tiene una ración cruda, y que quien vigila el crecimiento es el veterinario.

### 2.1 · Y el Ca:P 1,1 aparece por cuarta vez, ahora en crecimiento

El rango **1,1:1 – 2:1** es el mismo que piden las Tablas 40-5 (oxalato) y 41-6
(fosfato cálcico), que el motor **ya aplica** desde esta madrugada. La 33-6 lo
pide además para el **cachorro de raza grande**, con la nota de que se prefiere
el extremo bajo.

El motor aplica ahí el **1,0-1,6 de FEDIAF** (nota b). O sea que el suelo de la
fuente (1,1) es **más estricto** que el nuestro (1,0).

**Medido**: los 16 menús de raza grande del BLOQUE 53 van de 1,03 a 1,29, así
que **hay al menos uno por debajo de 1,1**. Aplicarlo cambiaría menús.

> **DECISIÓN**, y se junta con la que ya estaba abierta en `PENDIENTE.md` sobre
> el techo de Ca:P del cachorro de raza grande: ahora hay **tres** tablas de
> SACN5 hablando de lo mismo con tres rangos distintos —17-1 dice 1-1,5 para el
> grande; 33-5 dice 1,1-2,0; 33-6 dice 1,1-2,0 con el bajo preferido— y FEDIAF
> dice 1,0-1,6.

---

## 3 · La energía del cachorro: dos fuentes y hasta un **28 %** de diferencia

**Tabla 33-8**, «A method for estimating daily energy requirement (DER) for
growth of puppies after weaning», adaptada de NRC 2006. Da el DER por
**fracción del peso adulto**, no por edad, con siete escalones sobre
MER = 130 × BW^0,75:

| % del peso adulto | 15 | 30 | 43 | 60 | 71 | 80 | 100 |
|---|---|---|---|---|---|---|---|
| **factor sobre MER** | 2,5 | 2,1 | 1,9 | 1,6 | 1,4 | 1,3 | 1,0 |

Y trae ejemplo trabajado: cachorro de 5,25 kg con 35 kg de adulto esperado →
15 % → MER = 130 × 3,47 = 450 → **DER = 1.127 kcal/día**.

**Lo que aplica el motor** cuando se sabe el peso adulto —que es siempre que se
puede hablar de «% del peso adulto»— es la curva continua de **Klein 2019**, que
es la que **publica FEDIAF** en su Tabla VII-8b, medida en 493 cachorros de
compañía. Los dos números, calculados el 10 de septiembre:

| Cachorro | SACN5 33-8 | Motor (Klein/FEDIAF) | Diferencia |
|---|---|---|---|
| 5,25 kg (15 % de 35) | 1.127 | 811 | **−28 %** |
| 9 kg (15 % de 60) | 1.689 | 1.215 | **−28 %** |
| 3 kg (30 % de 10) | 622 | 487 | −22 % |
| 15 kg (47 % de 32) | 1.815 | 1.454 | −20 % |
| 25 kg (56 % de 45) | 2.440 | 2.002 | −18 % |
| 20 kg (80 % de 25) | 1.598 | 1.381 | −14 % |

**Esto no es un fallo**: la regla del repo es que manda FEDIAF, y la curva de
Klein es la que FEDIAF publica. Pero son dos fuentes publicadas que difieren
hasta un **28 % en un animal en crecimiento**, y la diferencia es mayor cuanto
más joven es el cachorro — que es justo cuando más cara sale.

Y el cap.33 añade una cosa más: el **gran danés es la excepción**, «may require
**20 % more**» que las demás razas grandes y gigantes.

> **DECISIÓN**, y se junta con la que ya estaba abierta en `PENDIENTE.md` sobre
> si la energía del cachorro pasa a ir por fracción de peso adulto (Tabla 17-2,
> tres escalones): la 33-8 da **siete** escalones y un ejemplo trabajado. ¿Se
> queda Klein, se avisa de la horquilla, o se sube al cachorro de raza grande?

---

## 4 · Lo que confirma, que también cuenta

- **Tabla 17-4** y su párrafo: calcio 0,7-1,7 % MS en cachorro pequeño-mediano y
  0,7-1,2 % en raza grande, y «foods with a calcium content of **1.1% DM**» como
  nivel de referencia. Es exactamente el 1,1 % de Fascetti que el motor aplica
  como techo del cachorro de raza grande. **Nada nuevo, y eso es una buena
  noticia**: dos fuentes independientes y el mismo número.
- **Cap.33**: «Canine growth foods should contain **100 mg/kg DM zinc** (NRC,
  2006)». El motor aplica el mínimo de FEDIAF, 25 mg/1000 kcal, que a 4,0 kcal/g
  son exactamente **100 mg/kg MS**. El mismo número por dos caminos.
- **Cap.15**: «Food should provide at least **10 to 20 %** … [digestible] … carbohydrate to support normal milk lactose production» en la lactante. Una
  ración BARF no lleva hidratos, y por eso el motor **dobla la proteína** en
  gestación y lactancia desde el 8 de septiembre. Esta frase es la otra mitad de
  ese mismo hallazgo, y no se puede aplicar: no vamos a meter cereal.

---

## 5 · Dónde queda cada una

Las tres tablas con hallazgo (**14-3**, **33-6** y **33-8**) están marcadas
`leida_con_hallazgo` en `sacn5_tablas.json`, y el **BLOQUE 78 cuenta esa
etiqueta aparte y exacto**: no se mezclan con las 286 que nadie ha mirado, para
que el número que baja al trabajar no tape al que sube al encontrar algo.

---

## Segunda tanda (10 de septiembre, tarde) — leyendo con el contador arreglado

Los tres primeros salen de las Tablas **17-1** y **33-5**, que son las dos de las
que el motor ya aplica el calcio y el fósforo del cachorro. O sea: teníamos esas
tablas abiertas y aplicamos **unas filas sí y otras no**.

### S-4 · El techo de grasa del cachorro de raza grande, y no cabe ninguno

**Tabla 33-5**, «Key nutritional factors for foods … for large- and giant-breed puppies», en materia seca:

| Factor | Recomendado |
|---|---|
| Densidad energética | 3,2-4,1 kcal/g |
| **Grasa** | **8,5-17 %** |
| DHA | ≥0,02 % |
| Calcio | 0,8-1,2 % |
| Ca:P | 1,1:1-2:1 (se prefiere el extremo bajo) |

El **calcio** de esa tabla ya se aplica. La **grasa** no. Medido sobre los 12
menús de cachorro del catálogo:

| | |
|---|---|
| Grasa real | **46,0 a 76,1 g/1000 kcal** (mediana 62,0) |
| Techo de la 33-5 convertido a 4,0 kcal/g | 42,5 → **lo pasan 12 de 12** |
| Convertido al extremo bajo de su propia tabla (3,2) | 53,1 → lo pasan **8 de 12** |

O sea que **ni uno solo cabe**, y por bastante. Es exactamente la forma del techo
de lisina: una cifra pensada para pienso, que en una ración cruda no entra
porque la grasa viene con la carne. **No se aplica**, se escribe con su medida y
se pregunta — que es lo que dice `PATOLOGIAS.md` §1.4-bis para este caso.

**El DHA de la misma tabla sí se cumple**, y conviene decirlo: 0,081 a 1,322
g/1000 kcal contra un mínimo de 0,050. **0 de 12 por debajo.**

### S-5 · Dos tablas del mismo libro no dicen lo mismo del Ca:P del cachorro grande

| Fuente | Ca:P para el cachorro de raza grande |
|---|---|
| SACN5 **Tabla 17-1**, columna «adult BW >25 kg» | **1:1 – 1,5:1** |
| SACN5 **Tabla 33-5** y su texto | **1,1:1 – 2:1**, «the lower end of the range is preferred» |
| FEDIAF nota b (umbral 15 kg) — **lo que aplica el motor** | **≤1,6** |

Nuestro 1,6 cae **entre las dos**. Aplicar el 1,5 de la 17-1 sería seguir una
tabla y contradecir la otra del mismo libro, así que **no se toca**: es una
pregunta para el nutricionista, no una decisión de refactor.

Y hay una tercera cosa que las dos sí dicen igual, y que el motor ya cumple: *«el
valor absoluto del calcio importa más que el ratio en el perro joven»*. El caso
que lo demuestra está en el capítulo 33: cachorros de gran danés con **Ca:P 1,1:1
—perfecto— pero 3,3 % de calcio** desarrollaron más enfermedad ortopédica que los
controles con 1,1 %.

### S-6 · La densidad de referencia no es 4,0 en ninguna de las dos tablas

Las cinco cifras que el motor toma de estas tablas se convierten con **4,0 kcal
por gramo de materia seca**. Las tablas dicen otra cosa:

- **Tabla 17-1**: energía «3,5-4,5 kcal/g». Es un **rango**, no un punto.
- **Tabla 33-5**: «3,2-4,1 kcal/g».
- Y el capítulo 6, para la recomendación de 0,7-1,2 % de calcio del cachorro
  grande: *«based on foods containing **3,800 kcal/kg**»*.

Convertir 1,1 % de materia seca da **2750** mg/1000 kcal a 4,0 y **2895** a 3,8.
**Aplicamos 2750**, o sea el lado estricto — no hay ninguna cifra mal, pero la
densidad declarada en `recomendaciones_libro.json` no es la que dice la fuente, y
eso es lo que audita `auditar_conversiones.py`. Es la misma familia que **F-27**
en FEDIAF, y se cierra con el mismo dato: la **humedad** del catálogo.

### S-7 · SACN5 le atribuye al NRC un límite de yodo que el NRC dice que **no se puede fijar**

Leyendo el capítulo 6 (minerales) aparece esto, literal:

> *«Current AAFCO (2007) guidelines set a maximum safe level for iodine for dogs
> at 50 mg/kg, whereas **NRC (2006) recommends 4 mg/kg as a safe upper limit**.»*

Cuatro mg/kg de materia seca son **1.000 µg/1000 kcal** (a 4,0 kcal/g), o sea
**por debajo de los 1.275 que aplica el motor**. Parecía un techo más estricto de
una fuente que ya usamos, y el motor lo debería aplicar.

**Fui al NRC 2006, que está en el repo de fuentes, y dice lo contrario.**
Capítulo 8, epígrafe «Safe Upper Limit of Iodine for Dogs», entero:

> *«Belshaw et al. (1975) measured I concentrations in several commercial brands
> of dog food. The results corresponded to concentrations ranging, at a minimum,
> from 400 to 1,275 μg I per 1,000 kcal ME … Apparently these foods were fed
> without any clinical abnormalities … Castillo et al. (2001a) reported
> evidence of depressed thyroid gland function … in puppies fed diets containing
> an estimated maximum I content of 1,400 μg I per 1,000 kcal ME … **Based on
> this information an absolute figure for a SUL of dietary I cannot be predicted
> for adult dogs.**»*

Y su tabla resumen lo confirma: la fila de yodo trae **la ingesta adecuada y la
recomendación, y la columna de «Safe Upper Limit» vacía**.

**O sea que el 4 mg/kg no está en el NRC.** Es una atribución de SACN5 que su
fuente primaria no sostiene.

**Qué se hace: nada, y ese es el resultado.** El techo se queda en 1.275, que es
el número que el NRC sí documenta como comido sin problemas y por debajo de donde
se vio el daño. Lo que cambia es que ahora está comprobado contra la fuente
primaria en vez de contra quien la cita.

⚠️ **Y la lección vale para todo lo que venga de SACN5**: es un libro de texto que
cita, y una cifra suya atribuida a otra fuente **no es esa fuente**. Cuando el
repo tenga el original —NRC 2006, FEDIAF, el Reglamento— la cifra se comprueba
contra el original. Aquí ha hecho falta a la primera.

### S-8 · La vitamina K: FEDIAF no la publica, el NRC sí, y nosotros no la tenemos en ninguna parte

Capítulo 6, epígrafe «Vitamin K», literal:

> *«AAFCO (2007) does not have a recommended allowance for vitamin K for dogs,
> but recommends 0.1 mg/kg DM for cats… **For dogs, the recommended allowance of
> vitamin K is 1.64 mg/kg DM for growth, 1.63 mg/kg DM for maintenance and
> 1.6 mg/kg DM for gestation and lactation.**»* (la cifra es del NRC 2006, que la
> fuente atribuye en la frase de antes)

**Lo que hay hoy en el motor: nada.** La vitamina K no está en los 43 requisitos
—es una de las cuatro filas de FEDIAF que no se transcriben— y **tampoco está en
el catálogo**: ninguna ficha declara vitamina K.

Y la razón por la que no se transcribió está escrita y es buena. FEDIAF §3.3.1:

> *«Vitamin K does not need to be added unless diet contains antimicrobial or
> anti-vitamin compounds.»*

**Pero con la cifra del NRC delante, el hueco cambia de naturaleza.** Deja de ser
«FEDIAF dice que no hace falta» y pasa a ser «FEDIAF dice que no hace falta
añadirla, el NRC publica cuánta hace falta, y nosotros **no podemos ni mirarlo**
porque no tenemos la columna».

Y hay un tercer hilo que apunta al mismo sitio: FEDIAF avisa de que **la vitamina
K sube en dietas con mucho pescado** (§3.3.2, con la cifra sólo para el gato), y
el motor mete pescado para cerrar el EPA+DHA.

**No se aplica nada** —sin columna en el catálogo no hay nada que verificar— y
queda como dos cosas separadas: un **dato que falta** (la vitamina K ficha por
ficha, que no rellena el asistente) y una **pregunta para el nutricionista**: si
la ración es cruda y sin antimicrobianos, ¿basta con el criterio de FEDIAF, o
conviene medirla porque lleva pescado?

### S-9 · La ración sin hidratos en la gestación: tres estudios, y nuestro número cae donde debe

Es la comprobación que un nutricionista pediría primero, porque una ración BARF
**no lleva almidón** y la gestación es donde eso más pesa. El capítulo 5 de SACN5
trae los tres trabajos, y hasta hoy sólo teníamos la frase de FEDIAF.

**Lo que teníamos.** FEDIAF §3.3.1: *«The recommendation for protein assumes the
diet contains some carbohydrate… If carbohydrate is absent or at a very low
level, the protein requirement is much higher, and may be double.»* De ahí sale
el suelo de **125 g de proteína/1000 kcal** que el motor aplica en gestación y
lactancia.

**Lo que dice SACN5, con las tres cifras:**

| Estudio | Dieta | Resultado |
|---|---|---|
| Romsos 1981 | **sin hidratos**, 26 % de la energía como proteína | hipoglucemia la semana antes del parto, **menos cachorros vivos**, letargo, peor cuidado de la camada |
| Kienzle 1985 | — | *«a starch-free food containing **at least 33 % of ME from protein** is necessary to supply needed glucose precursors»* |
| Blaza 1989 | **sin almidón**, **51 %** de la energía como proteína | **rindió igual** que la dieta con almidón |

**Dónde cae nuestro número.** 125 g/1000 kcal son **43,8 %** de la energía con el
factor de Atwater modificado (3,5 kcal/g) y **50 %** con 4,0. Es decir:

- muy por encima del **33 %** que Kienzle marca como necesario,
- y pegado al **51 %** con el que Blaza no vio diferencia,
- y a años luz del **26 %** con el que Romsos vio morir cachorros.

**Es una confirmación independiente**, y por un camino distinto: FEDIAF lo dijo
como «puede ser el doble» y SACN5 lo dice como «al menos el 33 % de la energía».
Los dos llevan al mismo sitio.

**Y una cifra que no se aplica, a propósito.** El mismo párrafo cierra con:

> *«Overall, a minimum of **23 % carbohydrate** is recommended in foods for
> gestating and lactating bitches.»*

Una ración cruda no puede cumplirlo. **No se aplica**, y no por descuido: la
propia fuente dice cuál es la alternativa —subir la proteína— y es exactamente lo
que hace el motor, con el número por encima del umbral que ella misma marca.

Queda escrito porque es la primera pregunta que va a hacer quien revise, y ahora
la respuesta tiene tres estudios detrás en vez de una frase.

### S-10 · Ninguna dieta renal de las que alargan la vida cabe dentro de FEDIAF

El capítulo 37 (enfermedad renal crónica) trae la composición de **los alimentos
renales terapéuticos de los estudios de supervivencia**, que son los que
demostraron alargar la vida del perro. Puestos al lado del mínimo de FEDIAF para
un perro **sano**:

| | Fósforo (mg/1000 kcal) | Proteína (g/1000 kcal) |
|---|---|---|
| **Mínimo de FEDIAF, perro adulto** | **1160** | **52,1** |
| Tope renal que aplica el motor | ≤1200 | — |
| Estudio de restricción de fósforo | **1100** | 42,5 |
| Estudio 2 (supervivencia) | **700** | 35 |
| Estudio 1 (supervivencia) | **675 – 1050** | 55 – 60 |
| Rango recomendado por SACN5 para el perro con ERC | — | **35 – 50** |
| Un pienso renal del capítulo | — | **20,5** |

**Todas están por debajo del mínimo de FEDIAF.** Las de fósforo y, salvo una, las
de proteína. Y el rango que el propio libro recomienda —*«14 to 20 % DM protein
for dogs»*— cae **entero** por debajo de los 52,1 g/1000 kcal del perro sano.

**Esto no es un fallo del motor: es la medida exacta de por qué existe la fase 4
de `VETERINARIOS.md`.** El tope renal del motor (1200) deja **40 mg** de sitio
sobre el mínimo de FEDIAF, un 3,4 %. Con eso se puede apretar un poco; no se
puede formular la dieta que alargó la vida en esos estudios. Por eso
`renal_avanzada` está bloqueada, y ahora se sabe **cuánto** hay que bajar de
FEDIAF para tratar de verdad: entre un 5 y un 42 % en fósforo.

**Y dos cosas más del mismo capítulo:**

- **El estadio IRIS está tabulado con su creatinina**, y es el dato que decide el
  techo de fósforo. La app **no lo pregunta** y sigue ofreciendo `renal` al dueño
  con menú automático — uno de los once casos de `FRONTEND_VS_MOTOR.md`.
- **La creatinina no se sale de su rango hasta que la función renal ya ha caído
  mucho**, así que un perro puede tener enfermedad renal con la analítica normal.
  Es el argumento de fondo de que esta patología sea `solo_veterinario`.

Y una a favor del formato, que también hay que decirla: en enfermedad renal **se
prefieren los alimentos húmedos**, y una ración cruda lo es.

---

## Tercera tanda (10 de septiembre, noche) — el capítulo 13 entero: el adulto joven

**Los 88 elementos del capítulo tienen veredicto**, uno a uno, en
`lecturas_sacn5.json`. Es el capítulo que describe **la población central de este
motor**: el perro adulto sano. De ahí salen seis cosas, y **dos de ellas
confirman números que ya aplicamos** — que es el resultado que más tranquiliza y
el que menos se cuenta.

### S-11 · ⚠️ El selenio: lo que recomienda SACN5 EMPIEZA en el máximo de FEDIAF y lo dobla

> *«For improved antioxidant performance, foods for mature dogs should contain at
> least 400 IU vitamin E/kg (DM) (Jewell et al, 2000), at least 100 mg vitamin
> C/kg (DM) and **0.5 to 1.3 mg selenium/kg (DM)**.»* (Tabla 13-4 y el texto)

A 4,0 kcal/g de materia seca eso son **125 a 325 µg/1000 kcal**.

| | µg/1000 kcal |
|---|---|
| Mínimo de FEDIAF, que aplicamos | 67,5 |
| **Máximo de FEDIAF, que aplicamos como restricción dura** | **142** |
| Rango que recomienda SACN5 | **125 – 325** |
| Nuestros 12 menús de adulto y senior | 85,5 – 141,3 |

O sea que **el 56 % superior del rango de SACN5 está por encima de un techo que
el motor no deja pasar**, y nuestros menús ya viven pegados a ese techo: el más
alto está en 141,3 con el máximo en 142.

**No se cambia nada, y esa es la decisión.** Un máximo de FEDIAF es un máximo, y
el propio SACN5 lo dice tres párrafos más abajo: *«There are no data to base a
safe upper limit of selenium for dogs, but for regulatory purposes, a maximum
standard of 2.0 mg/kg (DM) has been set for dog foods in the U.S. (AAFCO,
2007)»*. Recomendar 325 sin poder decir dónde está el techo no es motivo para
subir el nuestro. Queda escrito para que nadie lo redescubra y para que el
nutricionista lo vea.

### S-12 · La vitamina E: quinto capítulo que lo dice, y ahora con la medida del menú

> *«**at least 400 IU vitamin E/kg (DM)**»*, y el estudio de biomarcadores
> *«at least 500 IU vitamin E/kg (DM)»*, y la recomendación prudente repetida
> *«foods for young adult dogs should contain at least 400 IU vitamin E/kg (DM)»*.

400 UI/kg MS = 100 UI/1000 kcal = **67 mg/1000 kcal** de tocoferol natural.

| | mg/1000 kcal |
|---|---|
| Mínimo de FEDIAF, que aplicamos | 6,968 |
| Requisito del NRC 2006 que cita el propio capítulo | 7,5 |
| **Lo que recomienda SACN5** | **67** |
| Nuestros 12 menús | 13,6 – 71,4 (mediana **27,4**) |

**Once de los doce están por debajo.** Y hay un detalle que no esperaba: los
**senior** van muy por encima de los **adultos** (36 a 71 contra 13 a 18), o sea
que el motor ya llega a la cifra del libro cuando la etapa aprieta y no cuando
no. FEDIAF **no pone máximo** de vitamina E en adulto, así que subir esto no
choca con nada — y el propio capítulo trae el techo que faltaría: *«An upper
limit of 1,000 to 2,000 IU/kg food (DM) has been suggested for dogs»*, que son
167 a 335 mg/1000 kcal, muy por encima de donde estamos.

Es la misma cifra que ya salió en los capítulos 1, 7, 34, 35 y 47. **Sigue sin
aplicarse**, y la razón sigue siendo la misma: subir un mínimo diez veces cambia
qué alimentos entran en todos los menús, y eso lo decide el nutricionista.

### S-13 · Grasa y proteína: nuestros menús están por encima del rango del libro, los dos

| | Rango de SACN5 (% MS) | Por 1000 kcal | Nuestros 12 menús |
|---|---|---|---|
| Grasa | 10 – 20 | 25 – 50 g | **61,2 – 69,7** |
| Proteína bruta | 15 – 30 | 37,5 – 75 g | **81,7 – 102,4** |

**Los doce, por encima, en los dos.** FEDIAF no pone máximo ni de grasa ni de
proteína en el adulto, y es la naturaleza de una ración de carne cruda.

⚠️ **CORREGIDO la misma noche, al completar el capítulo 5:** «no incumple nada»
era falso. **SACN5 sí pone un techo de proteína al adulto sano** —«should not
exceed 30% DM protein», o sea 75 g/1000 kcal— y los doce menús se lo saltan. Lo
que pasa es que el argumento de la fuente es de **coste**, no de daño, y viene en
un párrafo que discute la premisa misma de una ración cruda. Detalle, con el
párrafo entero: **S-28**. Pero el capítulo ata explícitamente la proteína alta a dos cosas:

> *«In addition to any potential aggravating effects excess dietary protein may
> have on subclinical kidney disease, **foods high in protein also tend to
> contain high levels of phosphorus**.»*

> *«**up to 25% of the young adult dog population may already be affected by
> subclinical kidney disease**»*

**La palanca concreta de esas dos frases ya está aplicada**: el techo de fósforo
del perro sano, 2000 mg/1000 kcal, que vive en `recomendaciones_libro.json` desde
el 8 de septiembre. Y sobre la proteína en sí, el propio libro dice que el asunto
*«has yet to be resolved»*. Va como pregunta al nutricionista, no como número.

⚠️ ~~Y una cifra suelta que conviene tener vista: el **mínimo** de grasa que
recomienda SACN5 es **8,5 % MS = 21,25 g/1000 kcal**, y el mínimo de FEDIAF que
aplicamos es **13,75** — un 35 % más bajo. No cambia ningún menú (vamos por 61 a
70), pero es una fuente pidiendo más que FEDIAF en un suelo.~~

**TACHADO el mismo día, al leer el capítulo 17: eso era una errata del capítulo
13.** El cap. 17 dice, citando al mismo NRC 2006, que el 8,5 % MS es el mínimo del
**CRECIMIENTO** y que el del adulto es **5,5 % MS = 13,75 g/1000 kcal**, que es
exactamente el mínimo de FEDIAF que aplicamos. No hay ninguna fuente pidiendo más
que FEDIAF aquí: hay una frase del libro que copió sobre el adulto la cifra del
cachorro. Detalle en **S-20**.

### S-14 · ✅ El escalón de edad, confirmado por cuarta vez

La Tabla 13-2 del capítulo:

| Edad | kcal/BWkg^0,75 | Lo que aplicamos (Tabla VII-6 de FEDIAF) |
|---|---|---|
| 1-2 años | 120 – 140 | **130** |
| 3-7 años | 100 – 130 | **110** |
| >7 años | 80 – 120 | **95** |

Los tres caen dentro de los tres rangos. Y la nota al pie de la tabla dice
*«Most pet dogs are minimally active and have a DER of approximately 95
kcal/BWkg 0.75 or 1.2 to 1.4 x RER»*, que es nuestro escalón bajo de actividad.

### S-15 · ⚠️ El Terranova: dos fuentes, dos números, y seguimos al menos estricto

> *«**Newfoundland dogs have energy requirements about 20% less than average**
> (Kienzle and Rainbird, 1991), whereas **Great Danes and Dalmatians may have
> energy requirements up to 60% higher than average**»*

| | Media | Terranova | Gran Danés |
|---|---|---|---|
| SACN5 cap.13 | 110 | **≈88** (−20 %) | hasta 176 (+60 %) |
| FEDIAF Tabla VII-7, que es lo que aplicamos | 110 | **105** (−4,5 %) | **200** (+82 %) |

En el Gran Danés FEDIAF es **más generosa** que SACN5 y aplicamos la de FEDIAF.
En el **Terranova** aplicamos **un 19 % más de lo que dice SACN5** — y en una
raza gigante, dar de más no es el lado seguro. Las dos fuentes citan al mismo
grupo (Kienzle y Rainbird), así que no es que una sea vieja.

**Y el DALMATA no tiene fila en FEDIAF**, así que hoy recibe el factor genérico
aunque SACN5 lo nombre junto al Gran Danés. Va como pregunta.

### S-16 · La fibra: la única cifra que el libro da, y dos menús se pasan

> *«It is difficult to determine the optimal concentration of crude fiber in a
> complete food for dogs; however, **up to 5% DM seems adequate**.»*

5 % MS = **≤12,5 g/1000 kcal**. Medido sobre los doce menús de adulto y senior:
diez van por debajo de 2,3, y **dos están en 21,3 y 26,1**.

No se aplica: la propia frase dice que es difícil de determinar, FEDIAF **no da
ni mínimo ni máximo** de fibra, y nuestra fila `Fibra` existe precisamente sin
números para eso. Queda escrito con la medida delante, que es lo que faltaba para
poder decidirlo.

### Y lo que el capítulo NO cambia, dicho para no volver a mirarlo

- **RER = 70 × BWkg^0,75** — es exactamente `der.py`.
- **Los mínimos de fósforo (0,3 % MS), sodio (0,08 % MS), proteína (10 % MS) y
  selenio (0,10 mg/kg MS)** que cita del NRC son todos **más flojos** que los de
  FEDIAF que ya aplicamos. Manda el nuestro.
- **La densidad energética 3,5-4,5 kcal/g MS** no se puede comprobar: nuestro
  catálogo no declara humedad. Es el hueco de la humedad, ya abierto y con dueño.
- **Los premios** (un puñado puede ser el 40 % del DER de un perro pequeño; un
  premio dental con 426 mg de calcio) son producto, no motor: la app no los
  pregunta y el catálogo no los tiene.
- **La vitamina C ≥100 mg/kg MS** no es un requisito (el perro la sintetiza y
  FEDIAF no le da fila) y **ninguna ficha del catálogo la declara**. Queda como
  dato que falta, no como límite.

---

## Cuarta tanda (10 de septiembre, noche) — el capítulo 17 entero: el crecimiento

Los 51 elementos con veredicto. Es el capítulo del que ya salieron los dos techos
de calcio y fósforo del cachorro el 9 de septiembre — y al leerlo entero aparece
**lo que se dejó de esa misma tabla**.

### S-18 · ⚠️ De la Tabla 17-1 se cogieron DOS columnas y se dejó la tercera

La Tabla 17-1 tiene tres filas de mineral, cada una con **dos columnas** según el
cachorro vaya a pesar más o menos de 25 kg de adulto:

| | <25 kg adulto | >25 kg adulto | Qué aplica el motor |
|---|---|---|---|
| Calcio | 0,7–1,7 % MS | 0,7–1,2 % MS | **4250** y **2750** ✅ |
| Fósforo | 0,6–1,3 % MS | 0,6–1,1 % MS | **3250** y **2750** ✅ |
| **Ca:P** | **1:1–1,8:1** | **1:1–1,5:1** | **1,6 / 1,8 de FEDIAF, sin distinguir raza** ❌ |

Las dos primeras filas se aplicaron el 9 de septiembre. **La tercera no**, y es la
misma tabla, la misma fuente y la misma población. El motor pone el techo del
ratio por **etapa** (1,6 en cachorro joven, 1,8 en crecimiento) y **no mira el
peso adulto esperado**, así que un cachorro de raza grande puede salir en 1,7 con
el semáforo en verde cuando su propia tabla lo topa en **1,5**.

Es exactamente el fallo que este repo lleva días persiguiendo: **leer la fila que
ya tenías y no la tabla entera.**

⚠️ **MATIZADO el mismo día, al leer el capítulo 33: el libro da DOS rangos de
Ca:P para esta misma población y no coinciden.** La **Tabla 33-5**, que es la
específica de la enfermedad ortopédica del desarrollo, dice **1,1:1 a 2:1** *«(the
lower end of range is preferred)»*, y el texto lo repite: *«the calcium-phosphorus
ratio should be kept within physiologic limits (1.1:1 to 2:1)»*. O sea que en el
**techo** la 33-5 es **más floja** que nuestro 1,6/1,8 de FEDIAF, y en el **suelo**
es **más estricta** (1,1 contra 1,0).

Así que aplicar el 1,5 de la Tabla 17-1 sería quedarse con la más estricta de dos
tablas del mismo libro que no dicen lo mismo. **Eso lo decide el nutricionista, no
yo.** Lo que sí queda medido y firme es que ningún menú del catálogo llega a 1,5,
así que la decisión no está forzada por lo que el motor pueda o no pueda hacer.

Y el capítulo 33 explica **por qué el techo tiene que ser una cifra de calcio y no
solo un ratio**: *«Great Dane puppies raised on food with a calcium to phosphorus
ratio of 1.1:1 but with an excessive absolute amount of calcium (3.3% DM
calcium:3.0% DM phosphorus) developed more severe signs of DOD than did control
dogs»*. Un ratio correcto no protege de un calcio absoluto alto.

**Medido, y cabe con margen.** Los doce menús de cachorro del catálogo:

| | Ca:P |
|---|---|
| Gigante crecimiento / joven | 1,38 · 1,03 |
| Grande crecimiento / joven | 1,23 · 1,02 |
| Los ocho de razas menores | 1,15 – 1,31 |

**Ninguno llega a 1,5**, y el más alto de raza grande está en 1,38. O sea que
aplicarlo hoy no quitaría ni un menú.

No se aplica **en esta pasada** a propósito: es la regla de `LECTURA_SACN5.md`
—leer todo, apuntar todo, aplicar al final— y estrenar una clase de límite nueva
(un ratio en `recomendaciones_libro.json`, que hoy solo guarda techos por
nutriente) a mitad de una lectura es cómo se falló el 8 de septiembre.

### S-17 · ⚠️ SACN5 da DOS escaleras de energía de crecimiento distintas, y usamos la más floja

| | Escalones | Corta por |
|---|---|---|
| Caps. 1 y 5, Tabla 5-2 | **3 × RER** → **2 × RER** | **edad** (4 meses) |
| **Cap. 17, Tabla 17-2** | **3 × → 2,5 × → 1,8-2,0 ×** | **% del peso adulto** (50 %, 80 %) |

`der.py` usa la primera **como respaldo**, y solo cuando no hay peso adulto
esperado (con él manda la curva continua de Klein, que es la de FEDIAF). Pero en
esa banda las dos no dicen lo mismo:

| Cachorro entre el 50 % y el 80 % de su peso adulto | kcal/BWkg^0,75 |
|---|---|
| Lo que da nuestro respaldo (2 × RER, desde los 4 meses) | **140** |
| Lo que da la Tabla 17-2 (2,5 × RER) | **175** |

**Un 20 % menos.** Y el capítulo avisa de lo que pasa por debajo de esa cifra:
*«Young Great Dane puppies may not grow when daily energy intake is less than
175 kcal (735 kJ) metabolizable energy (ME)/BWkg 0.75 (2.5 x RER)»*.

Al Gran Danés no le afecta —tiene fila propia en FEDIAF (200) y esa es la que se
aplica—, pero a cualquier otro cachorro sin peso adulto esperado, sí. El
comentario de `der.py` ya llama a los tres escalones *«la convención clínica
genérica»* y se quedó con los dos por edad; ahora está medido lo que cuesta.

### S-20 · ⚠️ El libro se contradice consigo mismo en el mínimo de grasa del ADULTO

Dos capítulos, la misma cifra, la misma cita al NRC 2006, dos números:

> **cap. 13** — *«The minimum recommended allowance for dietary fat in foods for
> normal, healthy adult dogs is 8.5%, with at least 1% of the food as linoleic
> acid (DM) (NRC, 2006).»*

> **cap. 17** — *«The minimum recommended allowance of dietary fat for growth
> (8.5% DM) is much less than that needed for nursing, but more than is needed
> for adult maintenance (5.5% DM) (NRC, 2006).»*

**La buena es la del capítulo 17.** 5,5 % MS = **13,75 g/1000 kcal**, que es
exactamente el mínimo de grasa de FEDIAF que aplica el motor. El capítulo 13
copió sobre el adulto la cifra del **crecimiento**.

⚠️ Esto **corrige lo que escribí en S-13**, donde di por buena la cifra del
cap. 13 y anoté que era «una fuente pidiendo más que FEDIAF en un suelo». No lo
es: FEDIAF y SACN5 dicen lo mismo, y quien se equivoca es una frase del libro.

### S-19 · La proteína del cachorro, y la duda que el capítulo SÍ cierra

Rango recomendado **22-32 % MS = 55-80 g/1000 kcal**, y una ración BARF de
cachorro ronda los **134**. Por encima otra vez, como en el adulto.

Pero aquí el capítulo contesta la pregunta que importa, y la contesta a favor:

> *«it has been shown that foods containing 23 to 31% crude protein (6.4 to 8.8
> g/100 kcal ME) do not have a deleterious effect on skeletal development»*

O sea que **lo que deforma el hueso del cachorro de raza grande no es la
proteína**: es el calcio y la energía. Que es exactamente lo que el motor limita
en crecimiento, y exactamente lo que no limita.

### S-21 · Los hidratos que una ración cruda no lleva

> *«It has been suggested that foods contain about **20% digestible carbohydrate
> until puppies are four months of age** to ensure optimal health.»*

Y lo repite en las respuestas del capítulo: *«puppies appear to do better if
growth-type foods contain more than 20% complex carbohydrate DM»*. Una ración de
carne cruda no lleva prácticamente ninguno.

No hay número que aplicar —el propio libro dice *«no specific level of digestible
(soluble) carbohydrates exists for growing puppies»*— pero es de la **misma
familia** que el requisito condicional de proteína de gestación y lactancia que
el motor sí aplica: FEDIAF calcula suponiendo que la dieta lleva hidratos, y ésta
no. Va como pregunta para el nutricionista.

### Y una errata del libro, localizada exactamente

> *«The recommended minimum allowance for copper in growing puppies is **1.1% DM**
> (NRC, 2006).»*

Un 1,1 % de materia seca de cobre serían **27.500 mg/1000 kcal**. La cifra real
del NRC es **11 mg/kg MS = 2,75 mg/1000 kcal**, que es *exactamente* el mínimo de
FEDIAF que aplicamos. El libro escribió «1.1 % DM» donde iba «11 mg/kg DM». No se
toma nada de ahí, y queda escrito para que nadie lo tome mañana.

### Lo que confirma, que también cuenta

- **DHA+EPA ≥0,05 % MS y el EPA no más del 60 %**, así que el DHA ≥0,02 % MS. Es
  la fuente del suelo de DHA de crecimiento, ya aplicado y cerrado.
- **El fósforo del cachorro grande, 1,1 % MS = 2750**, y el calcio 1,2 % = 3000
  donde aplicamos **2750** por Fascetti. Coherente.
- **El umbral son 25 kg de peso adulto**, dicho otra vez y con el método al lado
  (*«Estimate adult body weight… >25 kg adult weight, use large-/giant-breed
  recommendation»*). No es el de 15 kg de la nota b de FEDIAF.
- **Por qué el techo de calcio es una restricción y no un aviso**: entre los dos y
  los seis meses la absorción intestinal de calcio **no baja del 40 %** por mucho
  que se le dé. El cachorro no se autorregula.
- **El BCS del cachorro es un rango**, 2,5/5 a 3,5/5. Tercera fuente que da rango
  donde nosotros usamos un punto — la pregunta ya está abierta en `CERRADO.md`.

---

## Quinta tanda (10 de septiembre, noche) — el capítulo 15 entero: gestación y lactancia

Los 79 elementos con veredicto. Este capítulo **contesta una pregunta que el
propio código tenía escrita como pendiente** y confirma dos cifras del DER.

### S-22 · ⚠️ La tabla que `recomendaciones.py` decía que faltaba por transcribir es la 15-4, y está aquí

`motor/recomendaciones.py` lo dice en su propia documentación:

> *«Las etapas que NO tienen ninguno son gestación y lactancia: SACN5 les da su
> propia tabla (la 15-5 de la reproductora) que todavía no se ha transcrito. Que
> devuelvan `{}` es el lado seguro y no un olvido silencioso.»*

**Es la Tabla 15-4**, y el capítulo la repite dos veces más en el texto. Para
gestación y lactancia:

| Factor | Rango en la fuente | Por 1000 kcal |
|---|---|---|
| Densidad energética | ≥4,0 kcal ME/g MS | (no comprobable sin humedad) |
| Proteína bruta | 25–35 % MS | 62,5 – 87,5 g |
| Grasa bruta | ≥20 % MS | ≥50 g |
| DHA | ≥0,02 % MS | ya aplicado |
| **Hidratos digestibles** | **≥23 % MS** | ver S-24 |
| **Calcio** | **1,0–1,7 % MS** | **2500 – 4250 mg** |
| **Fósforo** | **0,7–1,3 % MS** | **1750 – 3250 mg** |
| Ca:P | 1:1–2:1 | |

Los dos techos que faltan —**calcio 4250 y fósforo 3250**— resultan ser **los
mismos números** que el motor ya aplica al cachorro de menos de 25 kg. Así que
transcribir esta tabla no inventaría una cifra nueva: rellenaría un hueco
declarado con un número que el motor ya sabe manejar.

⚠️ Dos avisos antes de aplicarlo, que es por lo que no se aplica en esta pasada:

- **El capítulo se contradice en dos sitios menores.** El techo de calcio es
  **1,7 % MS** en la Tabla 15-4 y en el texto, y **1,6 %** en las respuestas del
  caso clínico. Y el suelo del ratio Ca:P es **1:1** en la tabla y **1,1:1** en el
  texto. Si se aplica, se toma el más estricto de cada par.
- **No está medido.** El catálogo precalculado no tiene menús de gestación ni de
  lactancia, así que no sé si esos techos caben. Hay que medirlo antes, como se
  hizo con los del cachorro.

Y el argumento clínico de por qué importa lo da el propio capítulo, en el recuadro
de la eclampsia: *«Prevention of eclampsia starts during pregnancy by feeding a
balanced food, without excess calcium and with a balanced calcium-phosphorus
ratio.»*

### S-23 · La forma del extra de gestación: FEDIAF lo da plano y SACN5 en escalón

| Semana de gestación | SACN5, Tabla 15-6 | FEDIAF, que es lo que aplica `der.py` |
|---|---|---|
| 1–4 | DER | DER |
| 5 | DER + **18** kcal/kg PV | DER + **26** |
| 6–8 | DER + **36** kcal/kg PV | DER + **26** |
| 9 | DER + **18** kcal/kg PV | DER + **26** |

En las **tres semanas de máximo crecimiento fetal** (6 a 8) damos **26 donde
SACN5 da 36**: un 28 % menos. En las semanas 5 y 9 damos de más. El promedio de
SACN5 sobre las cinco semanas es 28,8, muy cerca del 26 plano de FEDIAF, así que
sobre el total de la gestación la diferencia casi se cancela — pero no se
reparte igual.

**FEDIAF manda y no se cambia.** Queda escrito con los dos números al lado,
porque «damos menos en la semana 7» es la clase de cosa que nadie encuentra si no
está apuntada.

### S-24 · Los hidratos de la reproductora: cuatro cifras de la misma fuente, y nuestro suelo aguanta

Es el bloque más importante del capítulo para este motor, porque **una ración
cruda no lleva hidratos digestibles y esta etapa los pide como factor clave**.

La razón fisiológica: *«more than 50% of the energy for fetal development is
supplied by glucose… bitches have a high metabolic requirement for glucose during
the last weeks of gestation»*.

Y el capítulo cuantifica **cuatro veces**:

| | Lo que dice | Por 1000 kcal |
|---|---|---|
| Con hidratos | *«Foods for gestation should contain at least 23% DM digestible carbohydrate»* | — |
| Sin hidratos (1) | *«protein intake must almost be doubled; the food must provide at least 12 to 13 g digestible protein/BWkg 0.75»* | **91 – 98 g digestible** |
| Sin hidratos (2) | *«gluconeogenic precursors such as protein should be increased by at least 50%… and may have to be doubled»* | **94 – 175 g** sobre el rango 62,5-87,5 |
| Estudio | *«a food that had about 50% DM protein was fed, no problems with hypoglycemia or ketosis resulted and puppies were born healthy»* | **125 g** |

**Nuestro suelo condicional es 125 g/1000 kcal de proteína bruta**, y viene del
NRC. Cae por encima de las dos cuantificaciones y **exactamente** sobre el estudio
que probó ese nivel sin daño. Es la mejor confirmación posible: el número que
aplicamos tiene un ensayo detrás que lo alimentó y salió bien.

Lo que sigue sin resolver no es la proteína, es el hidrato en sí: el capítulo lo
pone como **factor nutricional clave** de la perra lactante (*«water, energy,
protein, carbohydrate, fat, calcium, phosphorus and food digestibility»*) para
sostener la lactosa de la leche, y ahí la proteína no sustituye a nada. Va como
pregunta, junto con la misma cuestión en el cachorro (**S-21**).

### Lo que confirma, y son dos cifras del DER

- **Gestación: 132 kcal ME/BWkg^0,75 (1,9 × RER)** — es exactamente
  `GESTACION_BASE` de `der.py`. El capítulo lo dice dos veces.
- **Lactancia: 145 × BWkg^0,75 sin contar la leche** — es exactamente
  `LACTANCIA_BASE`, y la fórmula de la Tabla 15-7 con `n`, `m` y el factor de
  semana es la que aplicamos (el método 1; el método 2 del libro no distingue
  semana de lactancia y no lo usamos).
- **DHA+EPA ≥0,05 % MS y el DHA ≥40 % del total** — el suelo de DHA, ya aplicado.
- **Grasa ≥20 % MS = 50 g/1000 kcal** para gestación tardía, lactantes con menos
  de cuatro cachorros y perras gigantes: una ración BARF va por 61 a 70 y lo
  cumple sin añadir nada.
- Y los mínimos del NRC que cita (hierro 70 mg/kg MS, zinc 96, fenilalanina
  0,83 %) son **más flojos** que los de FEDIAF que aplicamos. El único que va por
  encima es el **cobre, 12,4 mg/kg MS = 3,1** contra nuestro 2,75 — diferencia
  pequeña, del NRC y no de FEDIAF.

---

## Sexta tanda (10 de septiembre, noche) — el capítulo 33 entero: el cachorro de raza grande

Los 90 elementos con veredicto. Es el capítulo del que sale el umbral de los 25 kg,
y trae **el hallazgo más duro de toda la lectura de esta noche**.

### S-26 · ⚠️⚠️ El techo de vitamina A del motor es OCHO VECES el límite seguro del NRC para cachorros y reproductoras

> *«The safe upper limit of vitamin A is **15,000 µg/kg DM** (NRC, 2006).»*

A 4,0 kcal/g de materia seca eso son **3.750 µg/1000 kcal**. Y el NRC lo publica
así en su propia tabla, en esa misma unidad, así que no hay conversión que
discutir.

**Comprobado en el NRC original, porque la cifra tiene DOS valores y SACN5 solo
cita uno** (el del capítulo del cachorro):

> *«it is suggested that an upper limit of **15,000 μg retinol·kg⁻¹ diet of 4
> kcal·g⁻¹ be used for puppies**. For adult non-breeding dogs, it is proposed a
> safe upper limit of **64,000 μg retinol·kg⁻¹ diet** (4 kcal·g⁻¹) be adopted.»*
> … *«the level proposed for puppies (15,000 μg retinol·kg⁻¹ diet of 4 kcal·g⁻¹)
> is also suggested for breeding bitches.»*

| | µg/1000 kcal |
|---|---|
| **Techo del motor** (FEDIAF, «100 000 (N)» UI × 0,3 µg/UI) | **30.000** |
| Límite seguro del NRC, adulto no reproductor | 16.000 |
| **Límite seguro del NRC, cachorro y reproductora** | **3.750** |
| Mínimo de FEDIAF, que aplicamos | 375 |

**Ocho veces** para el cachorro y la perra preñada. Casi el doble para el adulto.

**Y no es teórico. Medido sobre los 36 menús precalculados:**

| | µg/1000 kcal |
|---|---|
| Mediana de los 36 | 2.098 |
| **Mediano_Lactante** | **5.052** — un 35 % por encima del límite del NRC |
| Grande_CachorroJoven | 3.334 — al 89 % del límite |
| Toy_Adulto y Mini_Adulto | 5.029 y 3.660 — muy por debajo del límite del adulto (16.000) |

O sea: **un menú de perra lactante del catálogo está por encima del límite seguro
que el NRC propone para reproductoras, y el semáforo lo da verde** porque mide
contra los 30.000 de FEDIAF.

Esto no es una recomendación del libro: es un **límite de seguridad**, la misma
familia que los cinco topes crónicos de `seguridad.py` (vitamina D, yodo, selenio,
mercurio, tiaminasa). Y viene con el mecanismo al lado, en el mismo capítulo: la
vitamina D a 135 veces la dosis recomendada **no movió el calcio ni el fósforo en
plasma** y aun así causó osteocondrosis y radius curvus. Con el hígado, que es la
fuente de vitamina A de una ración BARF, la analítica puede salir normal.

**No se aplica esta noche**, por la regla de leer todo antes de aplicar y porque
un tope nuevo de esta clase hay que medirlo en los 216 menús y no en 36. Pero es
el primero de la lista cuando se cierre la lectura.

### S-25 · El techo de grasa del cachorro de raza grande, y por qué NO es lo que parece

La Tabla 33-5 pone la grasa en **8,5 a 17 % MS** = 21,25 a 42,5 g/1000 kcal.
Nuestros cuatro menús de cachorro de raza grande y gigante:

| | g/1000 kcal |
|---|---|
| Gigante crecimiento | **73,8** |
| Gigante joven | 46,6 |
| Grande crecimiento | 64,6 |
| Grande joven | 52,4 |

Los cuatro por encima, y el gigante un **74 %** por encima. Pero el propio
capítulo desactiva la lectura fácil, dos veces:

> El capítulo lo dice de sus propios límites superiores: *«…dietary fat in foods
> intended for large- and giant-breed puppies **have not been established** but a
> dietary fat level of 17% is acceptable **as long as the puppies are fed properly
> (food-limited feeding)**.»* (la frase empieza al otro lado de la Tabla 33-5, que
> se cuela en medio al extraer el texto)

> *«when large-breed puppies were fed a very low energy density food… free choice
> vs. a food of higher energy density and increased fat…, the puppies eating the
> low energy density food **had less body fat but not slower growth**»*

O sea que el 17 % **no es un límite establecido**: es un nivel aceptable *si se
limita la cantidad*, y limitar la cantidad es exactamente lo que hace este motor —
formula para un DER, no da comida a discreción. Lo que hay que controlar es la
**energía**, no la grasa. Queda escrito con la medida, y con el porqué de no
aplicarlo.

### S-27 · Hasta cuándo es «cachorro» un perro de raza grande: 18 meses

> *«A balanced, high quality food especially designed for fast growing, large- and
> giant-breed dogs, characterized by a relatively low calcium content, should be
> fed **until 18 months of age**.»*

Y en otro sitio: *«free-choice feeding is not recommended for large- and
giant-breed puppies until they have reached skeletal maturity (**about 12 months
of age or at least 80 to 90% of adult weight**)»*.

Es un dato de **etapa**, no de nutriente, y decide qué columna de requisitos
recibe el perro. Hay que cruzarlo con dónde corta hoy la ficha, y eso toca los dos
repos. Va como pregunta.

### Lo que confirma, y esta vez son cinco números exactos

El capítulo cita al NRC 2006 para cinco mínimos, y **cinco de cinco coinciden con
lo que aplica el motor**:

| | SACN5 cap. 33 | Por 1000 kcal | Mínimo de FEDIAF que aplicamos |
|---|---|---|---|
| Cobre | 11 mg/kg MS | 2,75 | **2,75** ✅ |
| Zinc | 100 mg/kg MS | 25 | **25** ✅ |
| Manganeso | 1,4 mg/1000 kcal | 1,4 | **1,4** ✅ |
| Vitamina A | 1.515 µg/kg MS | 379 | **375** ✅ |
| Vitamina D | 550 UI/kg MS | 3,44 µg | **3,45** ✅ |

Y el del cobre **cierra la errata del capítulo 17**: allí ponía «1.1 % DM» y aquí
está el número bueno, 11 mg/kg MS, dicho sin ambigüedad.

**Y el umbral de los 25 kg, literal y con los tres orígenes del exceso:**

> *«Specific factors that are currently thought to increase the risk of DOD in
> young dogs include: 1) belonging to a large or giant breed (genetics) (**>25 kg
> adult weight**), 2) free-choice feeding… and 3) excessive intake of calcium and
> vitamin D **from food, treats and supplements**.»*

Tres orígenes, y el motor controla dos: la comida y los suplementos (por la dosis
máxima de fabricante). Los premios no los ve nadie.

**Y una frase que explica por qué todos los límites de este motor van por 1000
kcal y no por porcentaje:** cambiar a un alimento de menor densidad con el
*mismo* porcentaje de calcio hace que el cachorro coma **más** calcio, porque come
más gramos para las mismas kilocalorías. El capítulo lo cuantifica con un
rottweiler de 15 semanas: 5,4 g de calcio contra 6,7 g, sin que el porcentaje de
la etiqueta cambie.

---

## Séptima tanda (10 de septiembre, noche) — el capítulo 5, ya completo

Al capítulo 5 le faltaban **62 elementos** de la primera pasada. Ya están los 158.
Y entre los que faltaban está el techo que corrige lo que escribí en **S-13**.

### S-28 · ⚠️ SACN5 SÍ pone techo de proteína al adulto sano — y hay que leer el párrafo entero antes de tocar nada

> *«Thus, dog foods for adult maintenance **should not exceed 30% DM protein**.»*

30 % MS = **75 g/1000 kcal**. Los doce menús de adulto y senior del catálogo van
de **81,7 a 102,4**: los doce por encima, el peor un 37 % por encima.

⚠️ Esto **corrige S-13**, donde escribí que «FEDIAF no pone máximo de proteína en
adulto, así que no se incumple nada». Lo primero sigue siendo verdad; lo segundo
no: **SACN5 sí lo pone**, y es del perro sano, que es la clase de
`recomendaciones_libro.json`.

**Y aquí está la parte que decide qué hacer, que es el párrafo entero:**

> *«Excess protein adds unnecessary cost to foods. Excess protein is used for
> energy. As an energy source, protein is no better than digestible carbohydrate;
> however, protein is a more expensive energy source… **There are no nutritional
> reasons that support providing excessive amounts of dietary protein.** After the
> protein/amino acid requirements are met, additional protein provides no
> additional benefits. Thus, dog foods for adult maintenance should not exceed 30%
> DM protein.»*

El argumento de la fuente es **el coste y la ausencia de beneficio**, no el daño.
Y el párrafo que va justo antes dice esto:

> *«…the myth that dogs are carnivores and that meat-based, high-protein foods are
> more natural and thus better than lower protein foods that contain both animal
> and plant sources of protein.»*

O sea que este techo sale de un capítulo que discute **la premisa misma de una
ración de carne cruda**, y lo hace por economía de un pienso comercial. **No es un
límite de seguridad.**

Frente a eso, la vía que sí es de salud está en el capítulo 13 y **ya está
aplicada**: la proteína alta arrastra fósforo alto, y el techo de fósforo del
perro sano (2000 mg/1000 kcal) lleva puesto desde el 8 de septiembre.

**Decisión: no se aplica, y se pregunta.** Aplicar 75 g/1000 kcal cambiaría los
doce menús de adulto por un argumento de coste de pienso. Es exactamente el tipo
de cosa que no decido yo.

### Lo demás del capítulo, que es respaldo y un par de avisos

- **La fibra otra vez en <5 % MS** para el perro sano (*«a small amount of fiber
  (<5%)… is recommended in foods for healthy pets»*), que es el mismo ≤12,5
  g/1000 kcal de S-16, dicho desde otro capítulo.
- **Los ácidos grasos de cadena corta dan menos del 5 % de la energía del perro**,
  frente al 75 % del rumiante. Descarta contar la fermentación de la fibra como
  energía.
- **Un techo de omega-3 que la fuente demuestra que no hace falta**: perros
  adultos sanos con **7 % MS de omega-3** de aceite de pescado durante dos meses,
  sin problemas de coagulación ni de agregación plaquetaria. 7 % MS son 17,5
  g/1000 kcal, muy por encima de cualquier suelo que aplique el motor.
- **Y un dato que suma al aviso de taurina que ya damos al profesional**: un
  alimento alto en grasa (**24 % MS**) baja la taurina en plasma de forma
  significativa. Nuestros menús de adulto van por 61-70 g/1000 kcal, que es mucho
  más del 24 % MS.
- **Por qué el motor verifica los doce aminoácidos y no solo la proteína**, dicho
  por la fuente: *«animals do not have a requirement for protein per se but have
  an amino acid requirement»*.
- **Y una trampa para el día que alguien proponga aceite de cártamo**: va de ~80 %
  de linoleico a ~80 % de oleico **según la variedad**. Una ficha sacada de la
  fuente equivocada estaría completamente mal, y no hay cártamo en el catálogo.

---

## Octava tanda (10 de septiembre, noche) — el capítulo 6, ya completo

Los 39 que faltaban. Son en su mayoría **casos clínicos y cifras felinas**, y por
eso no cambian nada — pero dejan tres cosas escritas que sí valían la pena.

### Tres mínimos más del NRC, y los tres son más flojos que el nuestro

| | NRC 2006, perro | Por 1000 kcal | Mínimo de FEDIAF que aplicamos |
|---|---|---|---|
| Ácido pantoténico | 15 mg/kg MS | 3,75 | **4,11** ✅ |
| Vitamina B12 | 35 µg/kg MS | 8,75 | **9,68** ✅ |
| Colina | 1.700 mg/kg MS | 425 | **474** ✅ |

En los tres manda el de FEDIAF. Y las cifras de AAFCO que cita el mismo capítulo
(B12 5,5 y colina 300) son todavía más flojas.

### S-29 · La tercera regla «sube con la dieta» y tampoco trae número

> *«**Excess dietary protein and/or high-fat foods increase the choline
> requirement.**»*

Es exactamente la misma forma que las dos que ya viven en
`requisitos_condicionales.json` marcadas `documentado_sin_cifra`: **la vitamina E
sube con los PUFA** y **la B6 sube con la proteína**. Esta es la tercera —**la
colina sube con la proteína y con la grasa**— y una ración BARF es alta en las
dos. Tampoco tiene cifra, así que tampoco se puede aplicar; queda escrita para
que se pueda auditar y para no volver a descubrirla.

### Y un hueco que resulta que NO se puede cerrar

> *«**neither AAFCO (2007) nor NRC (2006) has recommended a maximum or safe upper
> limit for dietary choline for dogs and cats**»*

El motor no tiene techo de colina **porque no existe**, no por olvido. Escrito
para no volver a buscarlo.

### El mismo mecanismo de S-26, con hígado de por medio

Un gato con vitamina A en suero de **315 µg/dl** (normal 20 a 80) por
**suplementación diaria de hígado**. Es felino, y el gato es mucho más sensible,
así que **no se traslada al perro**. Pero el mecanismo es el mismo que el techo de
vitamina A de **S-26** y la fuente en el catálogo es la misma: el hígado.

Y para situar el tope crónico de selenio: la dosis letal mínima **inyectada** en
el perro es 2,0 mg/kg de peso vivo. Es vía intramuscular y no se traslada a una
dieta, pero explica por qué el selenio es uno de los cinco topes duros.
