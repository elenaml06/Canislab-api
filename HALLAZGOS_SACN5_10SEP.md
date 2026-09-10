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
| 47 | salud oral | «foods for oral health should contain **at least 400 IU/kg dry matter** (dog foods)» |

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
> without any clinical abnormalities. […] Castillo et al. (2001a) reported
> evidence of depressed thyroid gland function … in puppies fed diets containing
> an estimated maximum I content of 1,400 μg I per 1,000 kcal ME. **Based on this
> information an absolute figure for a SUL of dietary I cannot be predicted for
> adult dogs.**»*

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
> 1.6 mg/kg DM for gestation** (NRC 2006).»*

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
