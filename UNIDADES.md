# Unidades del catálogo de alimentos

**Todo va por 100 g de alimento tal cual se da**: fresco, no materia seca,
y crudo salvo que el alimento sea un producto ya procesado.

Este documento existe porque un número correcto sobre la base equivocada
no da ningún error. Pasó de verdad con el selenio: el tope estaba escrito
con la cifra buena de la fuente, pero aplicado sobre peso fresco cuando la
fuente lo da en materia seca, y dejaba pasar entre tres y cuatro veces el
límite real sin que saltara nada.

---

## Los dos ácidos grasos que se llaman casi igual

Esta es la confusión más fácil de cometer y la más cara, así que va la
primera.

| Nombre | Clave | Qué es | Unidad |
|---|---|---|---|
| **Linoleico** | `linoleico` | **omega-6**, C18:2 n-6 | g |
| **Alfa-linolénico** | `linolenico` | **omega-3**, C18:3 n-3 | g |

Se diferencian en una letra y son cosas opuestas. Se ve solo mirando dos
aceites del catálogo, por 100 g:

| | `linoleico` (ω-6) | `linolenico` (ω-3) |
|---|---|---|
| Aceite de girasol | **57,53 g** | 1,6 g |
| Aceite de linaza | 15,69 g | **55,47 g** |

Si se cambiaran el uno por el otro al cargar datos, el motor creería que
equilibra el omega-3 con un aceite que no lo tiene, y el menú saldría
verde igualmente: los dos son nutrientes válidos con valores plausibles.
Por eso el BLOQUE 26 de las pruebas ancla esos dos aceites, y
`auditar_catalogo.py` lista los alimentos donde el omega-3 supera al
omega-6 — que son pocos y conocidos.

**Y un tercer omega-3 que no es ninguno de los dos:** el EPA y el DHA del
pescado son de cadena larga y van en `epa` y `dha`, cada uno por su lado.
El perro convierte muy poco linolénico en EPA/DHA, así que no son
intercambiables. Si tu tabla los da como «C20:5 n-3» y «C22:6 n-3», esos
son.

---

## Los 29 nutrientes

| Nutriente | Clave | Unidad |
|---|---|---|
| Proteína | `proteina` | g |
| Grasa | `grasa` | g |
| Linoleico (ω-6) | `linoleico` | g |
| Alfa-linolénico (ω-3) | `linolenico` | g |
| Araquidónico | `araquidonico` | **mg** |
| EPA | `epa` | **g** |
| DHA | `dha` | **g** |
| Calcio | `calcio` | mg |
| Fósforo | `fosforo` | mg |
| Potasio | `potasio` | mg |
| Sodio | `sodio` | mg |
| Cloruro | `cloruro` | mg |
| Magnesio | `magnesio` | mg |
| Hierro | `hierro` | mg |
| Cobre | `cobre` | mg |
| Manganeso | `manganeso` | mg |
| Zinc | `zinc` | mg |
| Yodo | `yodo` | **µg** |
| Selenio | `selenio` | **µg** |
| Vitamina A | `vitA` | **µg** |
| Vitamina D | `vitD` | **µg** |
| Vitamina E | `vitE` | mg |
| Tiamina (B1) | `tiamina` | mg |
| Riboflavina (B2) | `riboflavina` | mg |
| Niacina (B3) | `niacina` | mg |
| Ácido pantoténico (B5) | `acidoPantotenico` | mg |
| Vitamina B6 | `vitB6` | mg |
| Folato (B9) | `folato` | **µg** |
| Vitamina B12 | `vitB12` | **µg** |
| Colina | `colina` | mg |

Y dos campos más que no son requisitos de FEDIAF:

| Campo | Clave | Unidad |
|---|---|---|
| Energía | `energia` | **kcal** por 100 g |
| Fibra | `fibra` | g |

La fibra se guarda pero **no se verifica**: ni FEDIAF, ni AAFCO, ni el NRC
fijan un mínimo para perros. Ver la sección de fibra del documento de
consultoría.

---

## Las trampas, en orden de frecuencia

**EPA y DHA van en GRAMOS, no en miligramos.** Es la que más se cuela,
porque casi todas las tablas los dan en mg. La sardina lleva
`epa: 0.254`, que son 254 mg.

**Vitaminas A y D en microgramos, no en UI.** Si la fuente da UI:
vitamina A ÷ 3,33 y vitamina D ÷ 40.

**El araquidónico va en mg** aunque los demás ácidos grasos vayan en
gramos. No es un descuido: es como lo da FEDIAF.

**Yodo, selenio, folato y B12 en microgramos.** El resto de minerales y
vitaminas, en mg.

**La energía tiene que cuadrar con los macros.** `proteína × 4 + grasa × 9`
tiene que parecerse a las kcal declaradas. Si no cuadra, casi siempre es
que la fuente estaba en materia seca o que la ficha mezcla dos alimentos
distintos — le pasó a la dorada de BEDCA, cuyos componentes suman 106 g
por cada 100 g. `auditar_catalogo.py` lo comprueba.

---

## Si un valor no lo tienes

**No lo pongas a cero.** Un cero significa «este alimento no lo tiene», y
el motor se lo cree: para los mínimos es conservador — como mucho añade un
suplemento que no hacía falta — pero **para los máximos es peligroso**,
porque podríamos pasarnos de cobre o de selenio sin enterarnos.

Déjalo vacío y que se declare en `sin_dato`, que es la lista de huecos
conocidos. Los que faltan hoy están en `DATOS_QUE_FALTAN.md`, uno a uno.

**Y no lo dejes fuera del diccionario, que es peor.** Un hueco puede
esconderse de tres maneras, y las tres acaban valiendo 0 para el motor:

| Cómo está guardado | ¿Se ve? |
|---|---|
| 0 y declarado en `sin_dato` | **sí** — es lo que queremos |
| 0 y sin declarar | a medias: la auditoría solo los cazaba en bloque |
| **la clave ni siquiera está** | **no se ve de ninguna forma** |

La tercera es la mala. `valor_nutriente()` devuelve 0 igual que en los
otros dos casos, pero **no hay ningún cero que encontrar**, así que ni la
auditoría ni `datos_incompletos` pueden decir nada. El 27 de agosto
afectaba a cuatro alimentos y 67 celdas, y no eran alimentos raros:
`Pollo pechuga sin piel` y `Pollo muslo sin piel` —de los más usados del
catálogo— y un `Hígado de cordero` al que le faltaba el **fósforo**.
`Corazón de conejo` tenía 21 de sus 31 nutrientes así.

Lo vigila el BLOQUE 29, que exige que las 31 claves estén en todas las
fichas.

**El cero de un tejido animal casi nunca es un cero.** El criterio, que no
necesita ninguna fuente: *un cero solo es creíble si algún alimento de esa
familia puede tenerlo de verdad*. Un tejido no tiene nunca potasio,
fósforo, magnesio, sodio, cloruro, hierro, cinc ni proteína a cero; un
alimento animal no tiene la B12 a cero; y una fila animal con energía pero
sin proteína ni grasa **se contradice a sí misma**, porque ahí no hay
hidratos que expliquen las kcal (en la fruta sí, y por eso la regla es solo
para lo animal).

Eso último no es teórico. `Testículos de cordero` tenía 30 de sus 31
nutrientes a cero, 68 kcal con proteína 0 y grasa 0, y una vitamina B12 de
las más altas del catálogo. Para el solver era **B12 gratis**: no costaba
nada en ningún otro presupuesto. Salía en 2 de cada 24 menús automáticos,
uno con 90,5 g, y cada gramo dejaba la ración corta de todo lo demás **con
el semáforo en verde**, porque el semáforo verifica contra esos mismos
datos. Se quitó del catálogo el 27 de agosto.

---

## El cloruro no es una medida: es el sodio × 1,542

Antes de tocar esa columna hay que saber qué es. En **114 de los alimentos
que tienen los dos valores, `cloruro` = `sodio` × 1,542 exacto** — la razón
entre los pesos atómicos del cloro y del sodio. La columna no es un
análisis: es el sodio reescrito **suponiendo que todo el sodio del alimento
viene de sal común**.

En tejido animal la suposición se sostiene a medias. **En vegetales es
sistemáticamente falsa**, porque el cloruro de la planta va sobre todo con
potasio, no con sodio. CIQUAL, que sí lo analiza (nutriente `Chlorure`,
código 10170), da 61 mg para el champiñón donde la derivación da 7,7, y
45 para los canónigos donde da 6,2: factores de 6 a 8 veces.

Se deja así por ahora, porque cambiar la columna entera es una decisión y
no un arreglo. Pero **no rellenes un hueco de cloruro con sodio × 1,54**:
sería cambiar un cero honesto por un número inventado con mejor cara.
`auditar_catalogo.py` lo avisa en cada ejecución para que no se olvide.

---

## Si el valor está pero no te lo crees: `dato_dudoso`

`sin_dato` resuelve la mitad del problema. Marca los huecos, y los huecos
son peligrosos por el lado del máximo. Pero **un valor declarado y erróneo
no dejaba rastro en ninguna parte**, y ese es el que hace daño: tiene la
forma de un dato bueno, así que pasa cualquier validación de formato.

El 27 de agosto aparecieron tres a la vez, los tres de etiquetas reales:

- el **omega-3 total** de cuatro aceites de salmón guardado en
  `linolenico`, que es solo el ALA — así que el EPA y el DHA se contaban
  dos veces, una en su columna y otra dentro del ALA;
- el **fósforo** de las dos harinas de hueso, que da un Ca:P de 1,28
  cuando la hidroxiapatita da 2,15 por estequiometría;
- el **cobre** del polvo de sangre, 150 veces por encima de lo que tiene
  la sangre bovina desecada.

Ninguno de los tres lo habría visto `sin_dato`, y los tres entraron por lo
mismo: **el nombre de la columna se parecía al de la etiqueta lo bastante
como para que nadie mirara**. Es el mismo error que el `linoleico` contra
el `linolenico` de arriba.

Los que se pueden arreglar, se arreglan. Los que no —porque el valor es el
de la etiqueta y el real no está publicado en ninguna parte— van en
**`dato_dudoso`**, y la marca lleva tres cosas, no una:

```json
"dato_dudoso": {
  "cobre": {
    "motivo":   "por qué no nos lo creemos",
    "resolver": "qué habría que hacer para cerrarlo, y a quién llamar",
    "desde":    "2026-08-27"
  }
}
```

`verificar()` lo devuelve en `datos_dudosos` junto al menú, igual que hace
con los huecos, y `auditar_catalogo.py` los lista **de la marca más vieja a
la más nueva, con los días al lado**.

**Por qué `resolver` y `desde`, y por qué no una fecha de caducidad.** La
diferencia entre un aviso conocido y un dato dudoso es de quién es la
pelota: el primero es un juicio cerrado («lo miramos y está bien»), el
segundo es un juicio abierto con una acción de fuera pegada —llamar a
AniForte, llamar a GRAU, partir la ficha del sésamo—. Ninguna ejecución de
la batería va a hacer que AniForte coja el teléfono, así que lo que hay que
hacer visible no es «¿se ha vuelto a verificar?» sino «¿sigue alguien
intentando cerrarlo?».

Se pensó en que las marcas caducaran a los 30 días y se descartó: un rojo
que salta por el calendario es un rojo que nadie ha provocado, y lo que se
aprende de él es a silenciarlo — subir la fecha sin mirar es el mismo gesto
de no revisar, con un paso más de burocracia. Es el fallo del BLOQUE 19
otra vez: el aviso de los cuatro aceites sonó en **cada** ejecución durante
un mes y nadie preguntó por qué. Un aviso que suena solo no arregla nada.
Sin umbral, sin rojo y sin fecha que subir: solo la lista, que se vuelve
incómoda de leer sola.

### `valor_plausible`: cuando la marca además trabaja

Una marca que solo anota no defiende de nada. Cuando de un valor dudoso
conocemos un **valor plausible publicado**, se pone al lado y el motor
**mide el mismo menú dos veces**: el **máximo** sobre el valor declarado y
el **mínimo** sobre el plausible.

El motivo es el de las cotas: *un valor no puede ser conservador en las dos
direcciones a la vez*. Un cobre inflado protege contra el techo y
desprotege contra el suelo, porque el motor cree cubierto lo que no está.

```json
"valor_plausible": {
  "cobre": {"valor": 0.85, "banda": [0.2, 5.5], "fuente": "Feedipedia node 221 / AFZ…"}
}
```

Dos reglas, y las dos las comprueba el BLOQUE 28:

1. **La `fuente` es obligatoria.** Este es el primer número del catálogo
   que no es una medida y que aun así decide si un menú pasa. Todo esto
   está construido sobre que cada número sabe de dónde viene; este no puede
   ser la excepción. Quien lea `0.85` a secas dentro de seis meses lo
   tratará como un dato.
2. **Nunca asciende a la columna del valor.** El día que el fabricante
   conteste entra lo que diga el fabricante y el plausible se borra. Si
   alguien lo «promociona» porque llevaba un año funcionando, una cuenta de
   servilleta se habrá convertido en el dato oficial del catálogo.

Y ojo con la dirección: un plausible **demasiado alto ablanda la prueba del
suelo**, que es para lo único que sirve. Uno bajo la hace más dura, que es
el error inofensivo. Por eso el cinc bajó de 3,5 a 2,3 en cuanto tuvo tabla
detrás.

---

## Los doce aminoácidos: g por 100 g, como la proteína

| Clave | | Clave | |
|---|---|---|---|
| `arginina` | g | `cistina` | g |
| `histidina` | g | `fenilalanina` | g |
| `isoleucina` | g | `tirosina` | g |
| `leucina` | g | `treonina` | g |
| `lisina` | g | `triptofano` | g |
| `metionina` | g | `valina` | g |

Misma unidad y misma base que `proteina`, porque **son una fracción de
ella**. Eso da la comprobación de coherencia más útil que tiene el
catálogo: la suma de los doce cae entre el **25 % y el 85 %** de la
proteína en cualquier alimento con proteína de verdad. Fuera de esa banda,
o la unidad está mal o el aminograma viene de una ficha con otra proteína.

FEDIAF los pide por 1000 kcal, no por 100 g — la conversión la hace el
motor, igual que con los otros 28. En la tabla son trece filas y no doce:
la metionina y la cistina van cada una por su lado **y además juntas**
(`Metionina_cistina`), y lo mismo la fenilalanina y la tirosina. Son
requisitos distintos, no una repetición.

**Un aminograma no se copia de otra ficha: se transfiere por gramo de
proteína.** Se coge el perfil de la ficha parecida, se divide por SU
proteína y se multiplica por la NUESTRA. Copiarlo tal cual mete el error
de las dos proteínas a la vez.

**Y un cero con proteína delante no es un valor, es un hueco.** Un aceite
con 0 g de proteína tiene 0 de lisina de verdad; una fresa con 0,7 g de
proteína y once aminoácidos a cero, no — son celdas que la fuente no
traía. Salió la fresa exactamente así, con solo el triptófano puesto. Los
huecos van a `sin_dato`, como todos.

Los doce están en la tabla de FEDIAF y **no se verifican todavía**: falta
el aminograma del hueso carnoso entero y de la mayoría de los pescados, y
sin dato cuentan como cero, o sea que el motor los evitaría. Ver la
sección de CLAUDE.md y el BLOQUE 27, que dice la condición exacta para
encenderlos.
