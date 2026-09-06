# Historia técnica

Este documento no se lee solo: se abre cuando se trabaja justo en la parte
del motor que describe. `CLAUDE.md` deja un resumen de dos líneas de cada
tema con un puntero aquí — esto es el detalle completo, con las medidas y
el porqué, que antes vivía en `CLAUDE.md` y se cargaba en cada sesión sin
falta.

Se separó el 6 de septiembre porque `CLAUDE.md` había llegado a 485 líneas
y se carga entero y automáticamente en cualquier sesión, hable o no de
aminoácidos, del DER o del selenio. Mover esto aquí no borra nada: solo
deja de ser gratis-obligatorio y pasa a bajo demanda.

## Los 12 aminoácidos: encendidos el 28 de agosto, con una excepción

La Tabla III-3b de FEDIAF pide **41 nutrientes** para el perro. Desde el 28
de agosto el motor los verifica **los 41**, y con el ratio Ca:P y el calcio
de raza grande son **las 43 filas de la tabla, completas**.

Los doce aminoácidos esenciales estuvieron dos días puestos en la tabla y
apagados en el motor, y merece la pena saber por qué, porque el motivo
cambió de forma por el camino:

**Al principio**, ninguna ficha traía aminoácidos — y no es que faltara el
dato, es que **las doce claves no existían en el diccionario**, la tercera
forma que tiene un hueco de esconderse. Activando solo la lisina, la app
dejaba de dar menús: cada alimento cuenta como cero y el mínimo se vuelve
inalcanzable. Un fallo ruidoso.

**Con 49 fichas cargadas** el fallo cambió de forma y dejó de verse. Un
alimento sin aminograma no cuenta como «no lo sé»: cuenta como **cero**.
Ya no bloqueaba: **desplazaba**. El motor se habría ido lejos del hueso
carnoso (10 de 10 sin dato entonces) y el menú habría salido **verde**,
porque el semáforo mide el mismo cero.

**Se encienden con 94 fichas** porque las tres cosas que hacían falta están
medidas, no supuestas:

- De un menú real, solo el **1,0 %** de la proteína viene de alimentos sin
  aminograma. Nueve de los diez huesos carnosos ya lo tienen.
- El aminoácido más justo se queda en **×2,12** de su mínimo (la metionina);
  el resto entre ×2,26 y ×5,02. Una ración de carne va sobrada.
- Con ellos puestos salen **20 de 20** menús, el hueso sigue en los 20 y su
  mediana sube de 207 a 216 g. En 51 casos con patologías y alergias, la
  mediana de resolver son **2,1 s** y lo peor 4,8 — lejos de los 30 de Render.

Que casi nunca aprieten no los hace inútiles: existen para el menú que **no**
es el de todos los días — una dieta muy restringida, una patología que
aprieta, un menú editado a la baja. Ahí es donde un aminoácido se queda
corto, y hasta el 28 de agosto nada lo habría visto.

**`metionina_cistina` y `fenilalanina_tirosina` no son claves de los
alimentos**: son sumas que calcula `valor_nutriente`, como `epa_dha`. FEDIAF
pide los cuatro requisitos —el aminoácido solo y la suma con su pareja—
porque la cistina se fabrica a partir de la metionina y la tirosina a partir
de la fenilalanina, así que la pareja ahorra al esencial.

### La excepción: el techo de lisina no se aplica

FEDIAF pone **un solo máximo a un aminoácido**: lisina 7,00 g/1000 kcal, y
solo en crecimiento. Está bien transcrito. Y medido, **0 de 15 menús de
cachorro caben debajo** — salen entre 8,79 y 12,12. No es que se pase alguno
raro: es que ninguna ración BARF de cachorro cabe, porque lleva unos 134 g
de proteína por 1000 kcal contra un mínimo de 50, y la lisina va detrás de
la proteína.

Aplicarlo dejaría a todos los cachorros sin menú. No aplicarlo es dejar de
comprobar un máximo de FEDIAF. Las dos cosas son malas, así que **no se
decide a escondidas**: la excepción vive en `verificar.MAXIMOS_NO_APLICADOS`
—una sola lista, que leen el solver y el semáforo por `maximo_de()`, para que
no puedan discrepar—, está escrita con la medición al lado, y la pregunta
para el nutricionista está en `PENDIENTE.md` §0: **¿el 7,00 se mide sobre la
proteína de la tabla o sobre la del plato?**

El **mínimo** de lisina sí se aplica. Lo único que se quita es el techo, y
el dato se queda en la tabla: dejar de aplicar un número no es lo mismo que
decir que FEDIAF no lo pide.

### Lo que vigila el BLOQUE 27

Que las filas sigan en la tabla con sus valores. Que los doce sigan en
`MAPA` —sacarlos vuelve a dejar la tabla cubierta a 30 de 43 y en verde—.
Que las dos sumas sumen de verdad. Que la proteína que viene de alimentos
sin aminograma no pase del **5 %** de un menú real (era el 1,0 %) — medido
sobre el plato y no contando fichas, porque lo que importa no es cuántos
alimentos no lo tienen, sino cuánto pesan. Que no se pierdan los 94
aminogramas. Y las tres del techo de lisina: que siga siendo el único
máximo no aplicado, que el mínimo apriete, y que la fila no se borre.

**Faltan 16 aminogramas**, y once son suplementos: solo los desbloquea una
etiqueta. La laringe de vacuno se deja vacía **a propósito** — es cartílago,
y el colágeno no tiene triptófano ni cistina; pasarle el aminograma del
músculo lo inventaría entero. `auditar_catalogo.py` lista quién los tiene y
quién no, por categoría — el total no dice nada, la categoría sí.

**Y una trampa de unidades que casi entra**: el segundo envío de aminogramas
traía el **triptófano en miligramos** y los otros once en gramos. Cargado tal
cual, el triptófano habría salido mil veces más alto y su mínimo no habría
apretado nunca, en silencio. Lo cazó la comprobación de coherencia: los doce
son una **fracción de la proteína**, así que su suma tiene que caer entre el
25 % y el 85 % de ella. Con el triptófano en mg se salían las 45 filas; en
gramos, ninguna. **Esa comprobación se corre antes de cargar cualquier
aminograma.**

## Los mínimos suben cuando el perro come menos

Es la ecuación de la propia FEDIAF, apartado 7.2.5, p. 60, leída del PDF:

> *«a systematic adjustment applied to all essential nutrients is needed
> **when fed below** the NRC standard assumption»*

Un perro necesita los mismos miligramos de zinc coma lo que coma. Si está a
dieta y esos miligramos tienen que caber en menos calorías, el mínimo **por
1000 kcal** sube. Hasta el 28 de agosto no subía: un perro adelgazando
recibía la misma densidad de nutrientes que uno normal, justo cuando menos
margen tiene. A la ración de bajada media (DER 63, medida por AAHA 2021) la
proteína mínima pasa de 52,10 a 78,6 g/1000 kcal.

**Solo hacia arriba, y esa es la decisión que hay que entender.** La ecuación
va en los dos sentidos, y aplicada tal cual bajaría el mínimo del perro
normal de 52,10 a 45,00 (la columna de 110) — medido, cinco de ocho perfiles
reales bajarían. Pero el «below» de FEDIAF es respecto a **130**, no a 110:
las columnas de 110 y 95 ya son las dos un ajuste hacia arriba desde la base
del NRC, no un techo y un suelo. **No hay una línea en las 98 páginas que
autorice bajar un mínimo porque el perro coma más**, y bajarlo sería relajar
nutrición. Así que el publicado es el suelo.

`minimo_de()` en `verificar.py` es el **único** sitio que sabe escalar, igual
que `maximo_de()` es el único que sabe de máximos. Lo leen el solver y el
semáforo: si cada uno escalara por su cuenta, el motor podría construir un
menú que el semáforo rechazara.

Tres cosas que no se escalan, y ninguna por olvido:

- **La grasa.** FEDIAF publica 13,75 g/1000 kcal en las dos columnas. Si se
  escalara, las kcal dejarían de cerrar.
- **El EPA+DHA, el linolénico y el araquidónico.** La ecuación presupone que
  existe un requerimiento diario absoluto, y FEDIAF pone «-» en adulto porque
  no lo hay: no se puede subir la densidad para cubrir algo que no existe. La
  protección real ahí escala sola — la **vitamina E** sí tiene mínimo de
  adulto y sube un 76 % de DER 110 a 56, mientras el aporte de PUFA por
  caloría se queda igual.
- **Crecimiento, gestación y lactancia.** Las dos columnas de la ecuación son
  de mantenimiento; para esas etapas FEDIAF publica otras y no está
  verificado que valga.

### La ventana se cierra: el cruce del selenio

**Los máximos NO escalan.** Un máximo de FEDIAF es un límite de
*concentración en el alimento* — la tabla III-3a los da en base materia seca
y marca los de la UE con «(L)» — y una concentración no depende de cuánto
coma el perro. Pero el mínimo sí sube. **La ventana entre los dos se cierra
según bajan las kcal.**

El primero en cruzarse es el **selenio en dieta húmeda**, que es la que
aplica a una ración BARF: mínimo 67,5 µg/1000 kcal a DER 95 y máximo legal de
la UE 142,0. Se cruzan en **DER 45,2**, y está medido de punta a punta — a
DER 49 sale menú y a DER 45 ya no. A la ración de bajada de AAHA (80 % del
RER, DER 56) la ventana es de solo **×1,24**.

Por debajo del cruce el problema es **infactible por aritmética**: no hay
comida, ni combinación, ni restricción que quitar que lo arregle. Por eso el
motor devuelve `imposible_por_aritmetica` con el nutriente y los dos números,
en vez del «quita alguna restricción y vuelve a probar» de siempre — que ahí
manda a la usuaria a un callejón sin salida. Es un modo de fallo **distinto**
del de los que aprietan primero (cloruro, folato, magnesio, linoleico), que
no tienen máximo y se arreglan añadiendo comida.

Lo vigila el **BLOQUE 34**: los dos anclajes contra el PDF, que nunca baje,
que sí suba, la grasa exenta, que no se escale en cachorro, que los máximos
no se muevan con el DER, que no aparezca un cruce nuevo sin avisar, y que a
DER 45 el mensaje sea el bueno y a DER 49 siga saliendo menú.

**El peso de referencia es el OBJETIVO**, no el real: en un perro con
sobrepeso las kcal ya se calculan sobre el ideal, así que la densidad tiene
que medirse sobre el mismo peso. Viaja en `peso_objetivo_kg` desde la app —
si no llega, se usa el real y se escala un poco de más, que es el lado
seguro. Sin ese campo el escalado queda **puesto y apagado**, así que lo
vigila `tests/peso-objetivo-en-cada-peticion.spec.js` en `canislab-web`.

## La duplicación que hay que vigilar (DER)

**El DER está calculado dos veces**: en `der.py` (Python, este repo) y en
`calcularDER()` de `App.jsx` (JavaScript, `canislab-web`). Las dos tienen
la misma fórmula, los mismos coeficientes por actividad y edad, las mismas
listas de razas de más y menos gasto, el mismo `+10` por macho entero y por
convivir con otros perros.

Y **la que manda es la del frontend**: la app calcula el DER y lo envía en
`der_objetivo`, así que `der.py` solo se ejecuta si alguien llama a `/der`,
que no llama nadie.

Comprobado el 26 de agosto con 16 perfiles (adulto, senior, cachorro,
gestante, lactante, bajada y subida de peso, razas de los dos grupos):
**coinciden en los 16**. Pero nada lo vigila. El día que se toque una y no
la otra, el usuario verá unas kcal y el motor cumplirá los requisitos sobre
otras, y no dará ningún error — que es exactamente la familia de fallos
descrita en «Fallos que no puede encontrar la usuaria» en `CLAUDE.md`.

**Cómo se vigila desde el 26 de agosto**: `der_casos.json`, 85 casos con
sus kcal, **el mismo archivo en los dos repos**. Cada lado comprueba su
implementación contra esos números sin necesitar al otro — el BLOQUE 23
aquí, `tests/der-contrato.spec.js` allí. Si tocas la fórmula de un lado, la
prueba de ese lado se cae en el acto.

Si el cambio es a propósito: se regeneran los esperados y **se copia
`der_casos.json` a los dos repos**. Los dos commits, o ninguno.

En el frontend la fórmula ya no está enterrada en `App.jsx`: vive en
`src/der.js`, que es lógica pura y no importa React.

## Los datos: cómo se encontraron las trampas

**`linoleico` es omega-6 y `linolenico` es omega-3.** Se diferencian en una
letra, son cosas opuestas, y si se cargan cambiados no salta nada — los dos
son nutrientes válidos con valores plausibles, y el menú sale verde igual.
Lo vigilan el BLOQUE 26, que ancla el aceite de girasol y el de linaza, y
`auditar_catalogo.py`, que lista los nueve alimentos donde el omega-3 supera
al omega-6.

**Los dos campos que dicen qué NO nos creemos.** Un 0 en el catálogo puede
ser «no lo tiene» o «no lo sabemos», y eso lo separa `sin_dato`. Pero faltaba
la otra mitad: **un valor declarado y erróneo no dejaba rastro en ninguna
parte**, y es el que hace daño, porque tiene la forma de un dato bueno y
pasa cualquier validación de formato. El 27 de agosto salieron tres a la
vez, los tres de etiquetas reales: el **omega-3 total** de cuatro aceites
de salmón metido en `linolenico` —que es solo el ALA, así que el EPA y el
DHA se contaban dos veces—, el **fósforo** de las dos harinas de hueso, con
un Ca:P de 1,28 cuando la hidroxiapatita da 2,15 por estequiometría, y el
**cobre** del polvo de sangre, 150 veces por encima de lo que tiene la
sangre desecada. Los tres entraron por lo mismo: el nombre de la columna se
parecía al de la etiqueta lo bastante como para que nadie mirara. Lo que se
puede arreglar se arregla; lo que no —porque el valor es el de la etiqueta
y el real no está publicado— va en **`dato_dudoso`**, que `verificar()`
devuelve junto al menú igual que los huecos. Lo vigila el BLOQUE 28.
