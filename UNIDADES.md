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
`dato_dudoso`, un diccionario `{"nutriente": "por qué no nos lo creemos"}`.
`verificar()` lo devuelve en `datos_dudosos` junto al menú, igual que hace
con los huecos, y `auditar_catalogo.py` los lista. Lo vigila el BLOQUE 28.
