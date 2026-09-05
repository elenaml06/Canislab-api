# Rawku — API del motor nutricional

Backend FastAPI + motor MILP en scipy. Desplegado en Render.
El frontend vive en `elenaml06/canislab-web` (Vercel, rawku.app).

**Empieza por `PENDIENTE.md`**: ahí está lo que queda por hacer, priorizado.

## Qué es esto

Calcula raciones BARF para perros que cumplen los 43 requisitos de FEDIAF
de forma exacta (no aproximada), con programación lineal entera mixta.
Decide qué alimentos usar y cuánto de cada uno a la vez.

Quien lo usa no es un veterinario: es alguien que quiere alimentar bien a
su perro. Por eso los mensajes de error explican qué pasa y qué hacer, no
qué falló por dentro.

## Lo que no se puede romper

Estas reglas están puestas a propósito y con motivo. Si un cambio choca
con alguna, casi siempre el error está en el cambio.

1. **Ningún menú sale sin verificar.** Todo camino que devuelva un menú
   pasa por `_garantizar_verificado()`, que lo comprueba de cero contra
   los 41 nutrientes + el ratio Ca:P + el calcio de raza grande + los
   límites de seguridad crónica.
   Si no está verde, **no se entrega**. Preferimos no dar menú a dar uno
   que no cumple. El BLOQUE 8 de las pruebas lo vigila.
2. **Los límites de seguridad crónica** (vitamina D, yodo, selenio,
   mercurio, tiaminasa) son restricciones duras dentro del solver, no
   avisos posteriores. Un aviso se puede ignorar; esto no.
   Lo mismo vale para **los topes por patología** (fósforo en renal, cobre
   en hepatopatía, grasa en pancreatitis…): son más estrictos que FEDIAF y
   se miden sobre las **kcal reales** del menú, no sobre las pedidas — el
   menú puede salir un 3 % por debajo, y menos kcal con el mismo nutriente
   es más concentración. Se comprueban **también** en
   `_garantizar_verificado`, porque el semáforo de FEDIAF no los ve: son
   los requisitos de un perro SANO, y un renal con 3084 mg de fósforo
   salía verde. Si un camino nuevo llama al motor, tiene que pasarle
   `patologias` — se olvidó una vez en la edición y una sola edición
   tiraba el tope.
3. **Lo que se puede relajar es la FORMA, nunca la nutrición.** Cuando no
   existe menú, se sueltan las proporciones de BARF (hueso 20-60 %, etc.),
   que son criterio nuestro y no de FEDIAF. Nunca los requisitos ni la
   seguridad. Ver `_escalera_de_relajacion()`.
4. **Las alergias y las categorías excluidas a mano no se tocan jamás.**
   Pueden ser médicas.
5. **Lo que eliges a mano se respeta, con un perro o con cinco.** Si la
   pantalla de Personalizar te deja elegir en una categoría, el motor no
   mete nada más de esa categoría. La lista de las que se respetan es
   `CATEGORIAS_QUE_ELIGE_EL_USUARIO` en `main.py`, y **tiene que coincidir
   con `CATEGORIAS` de `App.jsx`** — el día que dejen de coincidir, elegir
   en las que sobran no hará nada y nadie se enterará, porque el menú sale
   verde igual. Ya pasó: durante tres semanas se respetaban tres de las
   seis, y 15 de cada 36 menús personalizados metían algo que nadie pidió,
   callando.
   Dos matices que no son excepciones:
   · Una categoría que **no tocas** se queda en automático. No elegir
     pescado no es prohibir el pescado; para eso están las alergias.
   · Suplementos y Extras (sal, aceites, semillas, huevo) van siempre
     libres: no se eligen en ninguna pantalla y son la herramienta con la
     que el motor cierra los 43 requisitos.
   Y si con lo elegido no hay menú posible, se baja de peldaño y **se
   dice** — nunca se cambia en silencio. Eso incluye la pantalla de varios
   perros, que tenía esos avisos puestos a `null` a mano.

## El mapa: qué es cada archivo

Escrito el 26 de agosto porque no existía y hacía falta. Con 10.000 líneas
de Python repartidas en dos carpetas, «¿dónde toco esto?» se respondía
leyendo hasta encontrarlo, y hay dos motores en el repo — uno vivo y uno
jubilado — que desde fuera se parecen mucho.

### El motor de verdad (`motor/`)

| Archivo | Qué hace |
|---|---|
| `motor_completo.py` | **El corazón.** `resolver()` monta el problema MILP y lo resuelve: los 41 nutrientes (los 12 aminoácidos entre ellos desde el 28 de agosto), el ratio Ca:P y los topes de seguridad como restricciones simultáneas. Aquí viven también `PATOLOGIAS` y `topes_de_patologias()` |
| `verificar.py` | El semáforo. `MAPA` es **la** lista de requisitos, la única, compartida con el solver y con el analizador. Y `suplementar()`, que cierra huecos |
| `seguridad.py` | Los cinco topes crónicos y los avisos. Cada cifra con su fuente escrita al lado |
| `constructor.py` | Proporciones BARF de partida y `valor_nutriente()` (las claves derivadas, como `epa_dha`) |
| `exclusiones.py` | Alergias por palabras y familias de especie. Excluir «pollo» quita también «gallina» |
| `accesibles.py`, `modos.py` | Qué alimentos entran según el modo (automático / personalizar / aprovechar) |
| `catalogo_menus.py` | Carga los menús precalculados de la vista previa. Los datos están en `catalogo_menus.json`, en la raíz con los demás: aquí solo quedan 55 líneas de código |

### La API (raíz)

| Archivo | Qué hace |
|---|---|
| `main.py` | FastAPI: todos los endpoints, el presupuesto semanal de seguridad crónica y `_garantizar_verificado()`, por donde pasa **todo** menú antes de salir |
| `requerimientos_v2_final.json` | Los requisitos de FEDIAF. **43 filas, y desde el 28 de agosto se verifican las 43**: los 41 nutrientes de la Tabla III-3b (los 12 aminoácidos incluidos), el ratio Ca:P y el calcio de raza grande. Con **una** excepción escrita y probada: el techo de lisina — ver abajo |
| `requisitos.py` | Cargar la tabla de FEDIAF, resolver la etapa y la dosis máxima que marca el fabricante de cada suplemento. Era `optimizador.py`, 1.124 líneas donde esto convivía con el motor anterior al MILP y con una copia desincronizada de la tabla de patologías. El motor viejo se borró el 26 de agosto; quedan 121 líneas |
| `der.py` | Cálculo de las kcal. ⚠️ Ver «la duplicación que hay que vigilar», abajo |
| `analizador.py` | `/analizar`: la dieta que ya le da el dueño. Comparte `MAPA` con el semáforo a propósito — discreparon una vez por la fibra |
| `especies.py`, `accesibles.py` | Qué especie es cada alimento |
| `transicion.py` | Plan de cambio gradual de dieta |
| `persistencia.py`, `observabilidad.py` | Supabase y Sentry |
| `auditar_catalogo.py` | Huecos y datos raros del catálogo, y quién se queda sin aminograma. Lo ejecuta el BLOQUE 19 |
| `auditar_fediaf.py` | Cada valor del JSON contra la tabla de FEDIAF. Lo ejecuta el BLOQUE 18 |

### Endpoints: cuáles usa la app y cuáles no

Los que llama el frontend hoy: `/menu/v2`, `/menu/semana`,
`/menu/varios-perros`, `/menu/anadir`, `/menu/cambiar`, `/menu/quitar`,
`/menu/revalidar`, `/analizar`, `/alimentos`, y los de Stripe.

**Los que nadie llama pero siguen expuestos**: `/catalogo/{tamano}/{etapa}`,
`/der`, `/transicion` y `/perro/{perro_id}/menus`. Se dejan a propósito: no
duplican nada, son funciones que existen y que la app puede volver a usar.
Pero nadie los prueba usando la app, así que si algo se rompe ahí solo lo
ve la batería.

`POST /menu` **ya no existe** (26 de agosto). Era el motor anterior al MILP
y arrastraba su propia tabla de patologías, desincronizada de la buena:
fósforo renal a 1.400 en vez de 1.200, cobre en hepatopatía a 3,0 y sin
bloquear, grasa en pancreatitis al 25 % de las kcal, diabetes bajando la
grasa siempre, y urato, cistinuria y «otra» sin existir. No llegó a dar
menús malos porque `_garantizar_verificado()` los habría rechazado — que es
otra forma de decir que ese camino construía menús que el filtro final iba
a tirar. El BLOQUE 24 vigila que no vuelva.

### Los 12 aminoácidos: encendidos el 28 de agosto, con una excepción

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

#### La excepción: el techo de lisina no se aplica

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

#### Lo que vigila el BLOQUE 27

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

### Los mínimos suben cuando el perro come menos

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

#### La ventana se cierra: el cruce del selenio

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

### La duplicación que hay que vigilar

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
descrita en «Fallos que no puede encontrar la usuaria».

**Cómo se vigila desde el 26 de agosto**: `der_casos.json`, 85 casos con
sus kcal, **el mismo archivo en los dos repos**. Cada lado comprueba su
implementación contra esos números sin necesitar al otro — el BLOQUE 23
aquí, `tests/der-contrato.spec.js` allí. Si tocas la fórmula de un lado, la
prueba de ese lado se cae en el acto.

Si el cambio es a propósito: se regeneran los esperados y **se copia
`der_casos.json` a los dos repos**. Los dos commits, o ninguno.

En el frontend la fórmula ya no está enterrada en `App.jsx`: vive en
`src/der.js`, que es lógica pura y no importa React.

### Los documentos

`CLAUDE.md` (esto) es la entrada. `PENDIENTE.md` es lo que queda, ordenado
por prioridad. `DATOS_QUE_FALTAN.md` son los valores del catálogo que hay
que conseguir de BEDCA/CIQUAL/USDA, uno a uno — **no los rellena el
asistente**. `Bases.md` y `Ya_probado.md` son de las primeras sesiones:
decisiones cerradas y callejones sin salida ya recorridos, léelos antes de
proponer un cambio grande. `CAMBIOS_DE_DATOS_REVERTIDOS.md` explica por qué
se deshicieron unos cambios de datos del 21 de agosto.
`VETERINARIOS.md` es el plan de la parte para veterinarios: qué se
decidió el 28 de agosto, en qué orden se construye, y las tres cosas
que si se hacen mal no se arreglan después — que el profesional entre
con su cuenta y nunca con la del dueño; que una prescripción por debajo
de FEDIAF se verifique igual, contra un juego de requisitos escrito que
viaja con el menú; y que la pauta, que sale firmada con nombre y número
de colegiado, se guarde congelada entera — menú, ficha verificada,
contexto, huecos y sellos —, porque la ficha del perro, el catálogo y el
motor cambian, y un documento firmado tiene que seguir diciendo lo mismo
dentro de un año.

### Los datos

**`UNIDADES.md` es lo primero que hay que leer antes de tocar el catálogo**:
en qué unidad va cada uno de los 41 nutrientes, sobre qué base (100 g de
alimento tal cual se da) y las cuatro trampas que se cuelan siempre. La
peor, la primera del documento: `linoleico` es **omega-6** y `linolenico`
es **omega-3**. Se diferencian en una letra, son cosas opuestas, y si se
cargan cambiados no salta nada — los dos son nutrientes válidos con
valores plausibles, y el menú sale verde igual. Lo vigilan el BLOQUE 26,
que ancla el aceite de girasol y el de linaza, y `auditar_catalogo.py`,
que lista los nueve alimentos donde el omega-3 supera al omega-6.

**Los TRES campos que dicen qué NO nos creemos.** Un 0 en el catálogo puede
ser «no lo tiene» o «no lo sabemos», y eso lo separa `sin_dato`. Pero falta
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

Y **el tercero es `trazas`** (3 de septiembre), que es el 0 que sí lo es
pero no es un «no tiene». BEDCA distingue tres cosas —0, trazas y n.d.— y
el catálogo solo sabía escribir dos, así que once pescados y el pollo con
piel declaraban un cero redondo de vitamina A o D donde la fuente dice
«trazas». Numéricamente no cambia nada, y eso es lo correcto: contra un
mínimo el cero es el lado conservador, y contra un techo una traza está
por definición por debajo del límite de cuantificación. Lo que cambia es
que deja de ser un cero **falso** —un «no tiene» que nadie comprobó—, que
es la familia entera de fallos contra la que van los otros dos campos.
El peligro no es el número: es que alguien las barra a `sin_dato`, y
entonces el motor las imputa al percentil 90 de su familia contra los
techos, que para la vitamina D de un pescado es un disparate en la otra
dirección. Por eso el **BLOQUE 44** exige que las dos listas sean
disjuntas y que el valor siga siendo cero.

En la raíz, los cuatro: `alimentos_v3_final.json` (el catálogo),
`requerimientos_v2_final.json` (la tabla de FEDIAF), `catalogo_menus.json`
(los 36 menús precalculados de la vista previa y sus 180 variantes) y
`der_casos.json` (el contrato del DER, ver arriba).

Los dos primeros llevan **sello** en `/verificar`: si cambian sin que se
actualice el hash en `main.py`, la API lo dice. Los otros dos no, y es a
propósito — un menú del catálogo corrupto lo rechaza
`_garantizar_verificado()` igual que cualquier otro, y el contrato del DER
se comprueba entero en cada batería.

## Lo que Rawku NO puede afirmar

Escrito el 5 de septiembre, y va aquí y no en `PENDIENTE.md` porque no es
una tarea: es una frase que no se puede escribir nunca, y el sitio donde
alguien la buscaría es éste.

**Que el hueso limpia los dientes o previene la enfermedad periodontal.**
Es la creencia más extendida sobre la comida cruda y no se sostiene. SACN5
cap. 47, literal:

> *«Many of the recommendations made about the effect of food texture on
> oral health are unsubstantiated and several have turned out to be untrue
> when exposed to rigorous study, **including "natural foods"**.»*

El libro nombra la comida «natural» entre las creencias sobre textura que
**no resistieron** el estudio riguroso. Se puede decir que la comida blanda
acumula más placa —eso sí está—, pero de ahí no se sigue lo contrario.

Hoy **la app no lo afirma en ningún sitio**, comprobado. Esta sección existe
para que siga sin afirmarlo: es exactamente el tipo de frase que se cuela
sola cuando alguien escribe la pantalla de marketing.

Y lo que sí se puede decir del hueso, porque es canino, publicado y es un
número: **de cada diez cuerpos extraños que hay que sacar del esófago de un
perro, ocho son hueso** (Rousseau et al. 2007, 46 de 60, citado en SACN5
cap. 50a). Eso lo avisa `avisos_rotacion()` para cada hueso carnoso del
menú, y lo vigila el BLOQUE 48.

## Cómo se prueba

```bash
python3 pruebas_completas.py     # ~2 min, tiene que salir TODO EN VERDE
```

Se ejecuta **entero** antes de entregar cualquier cambio, no solo el
trozo que parece afectado. Existe porque antes cada arreglo se probaba
solo con el caso que había fallado, y eso dejaba romperse otros diez sin
que nadie se enterara hasta que los encontraba la usuaria.

Un test que pasa con el fallo puesto no sirve: al añadir uno, comprueba
que falla si reintroduces el problema.

## Comprobar qué hay desplegado

`https://canislab-api.onrender.com/verificar` dice, sin necesidad de
terminal: si los datos llegaron intactos, **qué versión de `main.py` está
corriendo** (`sello_main_py_actual`, comparable con el hash del archivo en
`main`), si Sentry está activo, y en qué modo están Stripe y Supabase.

Nació porque Render servía versiones viejas sin avisar y no había forma de
saberlo desde el móvil.

## Cómo está escrito el código

Los comentarios cuentan **por qué** existe algo, no qué hace la línea.
Muchos empiezan con `⚠️ CASO REAL ENCONTRADO` y describen el fallo
concreto que los provocó: «forzar aceite de hígado de bacalao en
generación daba 0 g pero en edición daba 5 g». Eso no es verbosidad — es
lo que permite que alguien que llegue en seis meses entienda por qué una
línea rara no se puede quitar.

Mantén ese estilo. Y en español, como el resto.

## Cómo se trabaja con git aquí

Esto está escrito porque el 21 de agosto se lió: once ramas sueltas, una
rama creada desde un `main` viejo (perdiendo un arreglo que ya estaba
fusionado), y cuatro tandas de trabajo terminadas y sin desplegar sin
avisar a nadie. Nada de eso fue un accidente inevitable.

1. **Antes de empezar CUALQUIER cosa**, siempre:
   `git fetch origin main && git checkout -B <rama> origin/main`.
   Nunca ramificar de una rama vieja ni de lo que hubiera en el disco: si
   la anterior ya se fusionó, esa copia local está caducada.
2. **Una rama por cambio**, con nombre que diga qué es. Nada de reutilizar
   una rama cuyo PR ya está fusionado — se empieza otra desde `main`.
3. **Al terminar: PR y decirlo.** Trabajo en una rama no está entregado.
   Vercel y Render despliegan de `main`; mientras no llegue ahí, no
   existe para quien usa la app. Hay que decir explícitamente si algo se
   queda sin fusionar y por qué.
4. **Tras fusionar, borrar la rama.** En Ajustes del repo →
   *Automatically delete head branches* lo hace GitHub solo.
5. **Comprobar que llegó.** La API se comprueba en `/verificar`
   (`sello_main_py_actual` = los primeros 16 hex del SHA-256 de
   `main.py`). La app, con la marca de build del panel lateral.

## Fallos que no puede encontrar la usuaria

Hay una familia de fallos que no dan error, no se ven en pantalla y solo
aparecen usando la app días después. El caso que los define: `guardarPerro`
leía siete campos con nombres que en la app no existen
(`perfil.fechaNacimiento` cuando se llama `dia`/`mesIdx`/`anio`…), así que
la fecha de nacimiento, la esterilización, la actividad y el tamaño se
guardaban vacíos **en silencio**. Y de la fecha sale la etapa, y de la
etapa los 43 requisitos: un perro de diez años volvía como cachorro.

Contra eso hay tres cosas, y las tres hay que mantenerlas:

- `tests/ficha-ida-y-vuelta.spec.js` (en `canislab-web`) recorre los
  campos de la ficha que afectan a la comida y exige que cada uno valga
  lo mismo después de guardar y volver a cargar. **Si añades un campo a
  la ficha, añádelo ahí.**
- `tests/sin-cuenta.spec.js` hace lo mismo en el otro sitio donde la
  ficha cambia de manos: al pasar de usar la app sin cuenta a crear una,
  cuando lo guardado en el navegador sube a Supabase. Misma lista de
  campos, mismo motivo. **Si añades un campo a la ficha, va también
  aquí** — si no, se pierde justo en ese salto y en silencio.
- Comprobar siempre lo GUARDADO, no lo que enseña la pantalla. La ficha
  se pinta del estado local: puede verse perfecta y estar guardada vacía.
  Una prueba que mire la pantalla aprueba este fallo.

## Variables de entorno

| Variable | Para qué |
|---|---|
| `SENTRY_DSN` | Captura de errores. Sin ella la API funciona igual, sin avisar |
| `STRIPE_SECRET_KEY` | Cobros. `sk_test_` en sandbox, `sk_live_` en real |
| `STRIPE_WEBHOOK_SECRET` | Verifica que los eventos vienen de Stripe |
| `STRIPE_PRICE_MENSUAL` / `_ANUAL` | Precios de prueba. Sin ellas, los de producción |
| `SUPABASE_URL` / `SUPABASE_SERVICE_KEY` | Activar el premium. Hace falta la **secreta**, no la pública |
| `STRIPE_PRUEBA` / `SENTRY_PRUEBA` | Endpoints de prueba. Se borran al terminar |

## Trampas conocidas

- **Las claves nuevas de Supabase (`sb_secret_…`) no son JWT**: no pueden
  ir en `Authorization: Bearer` o Supabase devuelve 403 aunque sean
  correctas. Solo en `apikey`.
- **`service_role` se salta la seguridad por fila, pero no los permisos de
  tabla.** Si una tabla se creó a mano, hace falta
  `GRANT SELECT, UPDATE ON public.<tabla> TO service_role;`.
- **Stripe quitó `current_period_end` del objeto Subscription** en la
  versión Basil: ahora vive en `items.data[]`.
- **Un `StripeObject` no es un dict**: no admite `.get()`.
- **Render duerme el servicio** tras ~15 min sin tráfico. Lo mantiene
  despierto un GitHub Action cada 10 minutos.
