# Lo ya hecho (sacado de PENDIENTE.md)

`PENDIENTE.md` empieza siendo lo primero que se lee en cualquier sesión
(`CLAUDE.md` lo pide así). Con los puntos ya resueltos mezclados entre los
pendientes de verdad, pesaba 81,8 KB y crecía con cada cosa que se
terminaba, no con lo que quedaba por hacer.

Este archivo no se lee solo: se abre cuando hace falta el detalle de algo
que ya se resolvió — por qué se decidió así, qué se midió, qué PR lo trajo.
Nada de esto es agenda; es historial. Se separó el 6 de septiembre.

## El peso ideal desde el BCS estaba calculado de dos formas — resuelto el 29 de agosto

**RESUELTO el 29 de agosto, y al revés de como se escribió el 28.**

El 28 se puso que había que RESTAR el exceso, apoyado en el ejemplo
trabajado de AAHA («labrador de 45 kg con BCS 8 → aproximadamente
32 kg»). Estaba mal, y el error era leer una frase sin abrir
la tabla que tiene al lado: **«30 % overweight» es un 30 % SOBRE EL
IDEAL**, así que se invierte dividiendo. Tres cosas lo cierran:

1. La **Tabla 1 de la propia guía** da un tercer método que no
   depende de cómo se lea «overweight» porque sale de la masa magra:
   `[peso × (100 − %grasa)] / 0,8`. Da ×0,7875 en BCS 8. Dividiendo
   sale ×0,7692 —un 2 % de diferencia—; restando, ×0,70, que se sale
   del propio rango del método desde BCS 7.
2. La **Global Pet Obesity Initiative (2019)**, respaldada por ECVCN,
   WSAVA y ACVIM, define obesidad como «30 % above ideal body
   weight». *Above ideal* no admite dos lecturas.
3. **El ejemplo de AAHA es el raro de su propio documento**: dos de
   sus tres métodos dan 34-35 kg para ese labrador. Es una errata.

Así que **`der.py` y `App.jsx` estaban bien desde el principio** y el
que estaba mal era `verificar.peso_objetivo_desde_bcs`, que ya
divide. Las kcal de los 85 casos del contrato **no se han movido**.

Y como no había ni una prueba que tocara esa función —por eso se
coló—, ahora está el **BLOQUE 37**, que ancla los cuatro puntos
contra el método de la grasa corporal y, sobre todo, **compara las
dos cuentas entre sí**: es lo que el contrato del DER no puede hacer.

## `EPA_DHA_total` ya suma las dos claves — hecho el 25 de agosto

Se resolvió con claves DERIVADAS en `valor_nutriente` — el mismo
mecanismo que el 28 de agosto sirvió para `metionina_cistina` y
`fenilalanina_tirosina`. Comprobado: epa 0,5 + dha 0,3 = 0,8.

El problema original: `EPA_DHA_total` se comprobaba solo contra el EPA,
sin sumarle el DHA. El requisito se llama EPA+DHA y en `verificar.MAPA`
apuntaba a la clave `epa` a secas, así que el DHA no contaba. Iba en la
dirección segura (se exigía más de lo que se pedía) y los menús lo
cumplían de sobra igual — medido, 145 mg/1000 kcal de EPA solo, contra un
mínimo de 110 — pero el nombre decía una cosa y el código comprobaba
otra. Se arregló dejando que un requisito apunte a la SUMA de dos claves.

## El tope de patología no se respeta — hecho el 24 de agosto

Lo que decía este punto (fósforo renal a 1426 con el tope en 1400) ya
estaba arreglado el 21 de agosto. Pero al ir a comprobarlo se midieron
**todos** los caminos que entregan un menú, no solo el de generar, y
aparecieron dos cosas peores:

**1. La grasa se pasaba SIEMPRE.** Pancreatitis: tope 25 % de las kcal,
salía 26 %. Diabetes: tope 35 %, salía 36 %. En los cuatro pesos probados.
Ese camino (`max_pct_kcal_grasa`) no había recibido el arreglo del 21:
comparaba contra las kcal PEDIDAS, y el menú puede salir hasta un 3 % por
debajo. Menos kcal con la misma grasa = más porcentaje.

**2. Editar un menú se saltaba los topes DEL TODO**, que es mucho peor:

| Patología | Tope | Salía |
|---|---|---|
| renal · fósforo | 1400 | **3084** (+120 %) |
| hepatopatía · cobre | 3.0 | **4.05** |
| pancreatitis · grasa | 25 % | **47 %** |

`_recalcular_con_motor` no le pasaba las patologías al motor — el mismo
fallo que ya tuvo esa misma función con el presupuesto semanal el 5 de
agosto. El menú se generaba respetando el tope y una sola edición lo
tiraba.

**Y la verificación no lo paraba**, que es lo que lo hacía invisible:
comprueba los 30 requisitos de FEDIAF, que son los de un perro SANO.
3084 mg de fósforo entra dentro del máximo de FEDIAF, así que el semáforo
salía VERDE.

Arreglado en tres capas: la grasa contra las kcal reales, las patologías
pasadas al editar, y **la puerta de verificación comprueba ahora también
los topes por patología** (`_tope_patologia_roto`), para que si mañana
otro camino se olvida de pasarlas, el menú no salga igualmente.

Vigilado en el **BLOQUE 13** de `pruebas_completas.py`: generar, patologías
combinadas, y editar. Medido después: 0 casos por encima del tope.

> Esto es distinto de la pregunta abierta de qué NÚMEROS poner (sigue en
> `PENDIENTE.md` §0): aquella sigue pendiente de decisión; lo de aquí es
> que el tope, sea el que sea, se cumpla.

## Multi-perro: varios perros por cuenta, cesta, burbuja y sin cuenta — hechos entre el 21 y el 24 de agosto

Ocho piezas de la fase de multi-perro, todas terminadas y desplegadas.

### Varios perros por cuenta — hecho el 21 de agosto

En `canislab-web`. Selector de perros en los dos paneles laterales,
crear y borrar perro, y se recuerda con cuál estabas. Cambiar de
perro **remonta** la app entera a propósito: perfil, menús y kcal se
calculan una sola vez al montar, así que sin remontar se quedaban
mezclados los datos de los dos. Borrar un perro borra también sus
menús (la tabla `menus` no borra en cascada; si no, quedaban
huérfanos para siempre). 8 pruebas nuevas en
`tests/varios-perros.spec.js`.

De paso: pesar al perro desde *Evolución* decía «✅ Peso
actualizado» y **no lo guardaba nunca** — `usuario` no existía en
esa pantalla y reventaba justo antes del guardado. Corregido.

### Cesta de la compra, diferenciando de quién es cada cosa — hecha el 24 de agosto

En `canislab-web`. Sale al final de la
pestaña «El menú» (no en una pestaña nueva: la decisión era «el
menú, cómo darlo y ya está») y en la pantalla de varios perros.

Suma **la semana entera**: cada menú por SUS días. Con un perro no
existía ninguna lista; con varios existía pero sumaba **solo el
primer menú de cada uno** — si el segundo menú llevaba un alimento
distinto, ese alimento no salía en la compra y se iba a la tienda
sin él.

Va por zonas de tienda (carnicería / pescadería / frutería /
despensa), porque carne, hueso, víscera e hígado son cuatro
casillas del motor pero un solo mostrador. Y en cantidades de
comprar, no de báscula: «2,5 kg», no «2478 g».

El «de quién» solo aparece si hay más de un perro **y** el alimento
no es de todos: «solo Cairo» en catorce de quince líneas taparía
justo la que importa.

La lógica vive en `src/cesta.js`, fuera de App.jsx, porque la usan
dos pantallas y tener dos copias fue lo que dejó una a medias
mientras la otra ni existía. 21 pruebas en `tests/cesta.spec.js`.

**No lleva precios** a propósito: no se tienen, cambian por
tienda y semana, y una cifra inventada en una lista de la compra es
peor que ninguna cifra.

⚠️ **MOVIDA EL 24 DE AGOSTO, pedido expreso**: «no quiero que la
compra aparezca en el menú, tiene que estar solo en el menú lateral».
Quitada del menú de un perro y de la pantalla de varios; vive solo en
el panel, en los **dos** paneles (el ligero y el de dentro del menú —
se puso solo en el primero y desde la pantalla del menú, que es donde
más falta hace, no salía).

Al sacarla del menú apareció un fallo que antes no existía: leyendo
solo lo GUARDADO, se acaba de generar un menú, no se ha dado a guardar
y el panel enseña la compra del menú **anterior** — números
correctos, menú equivocado, nada en pantalla que lo delate. Ahora
manda lo que hay en pantalla y la pantalla dice de dónde salen los
números. Y se puede elegir **para cuántos días** (3, 1 semana, 2
semanas, 1 mes): los menús cubren una semana, así que el resto se
escala en proporción y se avisa cuando no es una semana.

### La burbuja de perro y el engranaje, en TODAS las pantallas — hecho el 24 de agosto

Caso real: «la burbuja de perfiles de
perro y configuración tiene que existir en todas las pantallas, y en
todas las pantallas del menú lateral no aparecen».

Cierto: las seis pantallas que abre el panel (Perfil, Evolución, Mis
menús, Analizar, Por qué Rawku) tienen su **propia cabecera**, seis
copias, y se quedaron sin ella. Entrabas en Evolución y ya no sabías
de qué perro estabas viendo la evolución ni podías cambiar sin volver
atrás. También faltaba en Evolución/Analizar abiertas desde el
perfil, que es otra llamada distinta a `VistaMenus`.

La prueba (`tests/burbuja-en-todas.spec.js`) **no mira que exista**:
la pantalla de debajo sigue en el DOM con la suya y Playwright la
encuentra igual — quitando la burbuja de las seis cabeceras, la
primera versión de la prueba seguía pasando. Mira que **funcione**:
la toca y exige que se abra la hoja de perros. Y una tercera prueba
exige que el panel no tenga ninguna entrada que la lista no cubra,
para que la séptima pantalla no se olvide.

### Menús parecidos entre perros de la misma casa — motor hecho el 21 de agosto

`POST /menu/varios-perros`, con `modo_conjunto`
`"parecidos"` o `"distintos"`. Manda el perro con menos margen (más
restricciones y, a igualdad, ración más pequeña) y los demás se
amoldan a él: al revés no cabe, forzar los 7 alimentos de un pastor
alemán en un chihuahua de 3 kg no entra en 137 g de ración. Devuelve
por perro qué alimentos comparte, cuáles cambian y cuántos cambios
son. Medido: dos adultos de 24,5 y 8,2 kg salen con **0 cambios**
(misma compra, distintas cantidades) en 1,1 s. **Ya está en la app**:
en el generador, con más de un perro, sale «¿Para quién?» con las
tres opciones, y la pantalla de resultados enseña qué lleva cada uno
que los demás no y la compra de un día sumando a todos. De momento
solo en modo automático.

**Prueba de esfuerzo (21 agosto)**: 40 hogares al azar (2-3 perros,
pesos de 2 a 45 kg, las 4 etapas, alergias y categorías excluidas),
**86 menús entregados y 86 verificados en verde** de cero contra los
30 requisitos de la etapa de cada perro. Ni uno en rojo ni en ámbar,
ningún hogar sin menú, ningún alérgeno ni categoría excluida colada.
Peor tiempo de un hogar: 4,2 s.

Encontró de paso un fallo grave que llevaba meses: **las alergias se
podían saltar forzando el alimento** — ver `Ya_probado.md`.

### Menús de varios perros: el recorrido COMPLETO — hecho el 21 de agosto

API #23, web #11. Ya no hay camino aparte: para varios
perros se pasa por las mismas pantallas. Qué come cada perro por
separado, automático y personalizar, cuántos menús con su rotación,
aviso de transición por perro, y «Ver y editar el menú de X» que
abre el editor de siempre.

### La pantalla del menú, en dos pestañas — hecho el 23 de agosto

Era un scroll larguísimo con el plan de
transición pegado a las tarjetas, la congelación perdida en medio de
la pila de avisos (y con una X que la escondía para siempre), y cómo
preparar cada alimento detrás del icono de cubiertos de su fila.
Ahora: **El menú** (qué le doy, con el lápiz de cada alimento) y
**Cómo darlo** (transición, congelación y preparación, todo junto).
No se quitó nada; el icono de cubiertos de cada fila sigue estando.
`tests/menu-dos-pestanas.spec.js`.

### Sacar los perros del menú lateral — hecho el 24 de agosto

En `claude/burbuja-de-perfil-y-engranaje`, junto con los ajustes de
cuenta, que iban en el mismo sitio.

**La burbuja** va en la cabecera de todas las pantallas: dice de qué
perro es lo que estás viendo, y al tocarla salen los perros de la
casa y «añadir otro». Antes había dos caminos y ninguno completo —
unas pastillas que solo aparecían en la ficha, y una fila plegada
dentro del panel. Desde «Mis menús», por ejemplo, no se podía
cambiar de perro sin abrir el panel; lo decía el comentario de una
de las pruebas, y ahora esa misma prueba comprueba lo contrario.

**El engranaje**, al lado, lleva a **Ajustes**, con las dos mitades:
los perros (editar ficha, ir a otro, añadir, borrar) y la cuenta
(correo, contraseña, cerrar sesión). Sin cuenta enseña «crear una
cuenta» en vez de «cerrar sesión».

El selector viejo del panel y las pastillas de la ficha se han
borrado: tener tres formas de hacer lo mismo era parte del lío.

Vigilado en `tests/ajustes.spec.js` y en `varios-perros.spec.js`,
con una prueba que falla si los perros vuelven al panel.

> Un rótulo por el camino: al meter la burbuja se quitó el «MENÚ
> SEMANAL» / «PERFIL» de la cabecera, y dos pruebas viejas lo
> cazaron. Tenían razón: ese rótulo dice en qué pantalla estás. Han
> vuelto, en su propia línea, y conviven con la burbuja.

### Poder usar la app sin cuenta — hecho el 23 de agosto

En `claude/menu-dos-pestanas-y-sin-cuenta`. La primera pantalla ofrece
«Probar sin crear cuenta»; a partir de ahí la app entera funciona
contra `localStorage` en vez de Supabase (`src/almacen.js`, que
decide por dónde van los datos y explica en su cabecera **cuándo se
da de alta el usuario** y por qué ahí).

La cuenta se ofrece cuando ya existe algo que perder — debajo del
primer menú, sin bloquear nada — y al crearla lo del navegador
**sube solo** (`migrarLocalACuenta`). Sin esa parte, registrarse
después de una semana de uso habría borrado esa semana en silencio.
Vigilado campo por campo en `tests/sin-cuenta.spec.js`.

Queda fuera a propósito: sin cuenta `esPremium` responde que **no**,
para que el día que el muro se encienda «sin cuenta» no sea un
agujero por el que colarse.

## La compra: elegir el menú, los días bien, y marcar lo que ya tienes — hecho el 25 de agosto

Pedido el 24 de agosto después de usarla; hecho el 25.

1. **Elegir qué menú ver.** Selector arriba de la lista: "Todos
   juntos" o "Menú N · X días".

2. **Los días.** Era un fallo de concepto, no de cuentas: la cesta
   salía de UNA SEMANA y todo se escalaba por dias/7, pero los menús
   de una semana no duran lo mismo (uno cubre 4 días y otro 3). En sus
   palabras: *«si cocinas para 1 semana uno de 3 días tienes para más
   de dos»*. Ahora son dos preguntas distintas según lo que se mire:
   todos juntos → **semanas** (multiplicar una semana por 2 es
   exacto); un menú solo → **tandas de ese menú**, y cada opción dice
   los días de comida que da ("2 tandas · 6 días"). Encima de la
   lista, en grande, los días que cubre lo que se está viendo.

3. **Casillas para marcar lo comprado**, la línea entera pulsable
   (un cuadradito de 12 px no se acierta de pie en una tienda), y un
   botón de empezar de cero que solo sale si hay algo marcado. Se
   guarda en el navegador a propósito, no en Supabase: es de este
   móvil y de esta compra.

PR #31 de canislab-web. 8 pruebas nuevas, comprobadas rompiéndolas.

## Cantidades no medibles — hecho el 24 de agosto

Medido sobre 51 menús (todos los tamaños, etapas,
patologías y exclusiones), el problema era **más pequeño de lo que
parecía y de dos tipos distintos**.

**A granel** — salía UNA cantidad por debajo de un gramo en ~300
alimentos medidos: 0,35 g de sal común. Arreglado en el motor con un
suelo de 1 g: si va a usar un alimento a granel, que use una
cantidad que quepa en una báscula, y si no le cuadra, que use otra
cosa. **No se redondea el resultado**: cambiar los gramos después de
resolver cambia los nutrientes, y toda la app se sostiene sobre que
las cifras cuadran de verdad.

El suelo va **solo en Extras**, y eso también se midió: carnes,
vísceras y verduras nunca bajaban de ~1,9 g, así que ponerles suelo
no arregla nada y sí cuesta — con el suelo en todo el catálogo,
`/menu/varios-perros` pasaba de ~7 s a ~11 s con el presupuesto en
24 s. En Render eso se puede llevar por delante un menú.

**En polvo** — 0,15 g de alga, 0,60 g de multivitamínico. A éstos
**no** se les puede poner suelo: sería obligar a dar de más de un
suplemento. Se arreglan con el peso del cacito de cada producto, que
es un DATO y está apuntado en `DATOS_QUE_FALTAN.md`.

⚠️ **CORREGIDO EL 24 DE AGOSTO — lo de arriba era falso al principio.**
Decía que «lo que sostiene la garantía es la restricción del motor, que
es estructural». No lo era: **la fila del suelo no se añadía nunca**.
Comparaba `categoria_de[n]` (la CLAVE del diccionario de candidatos)
con `"Extras"`, y los aceites, la sal y las semillas entran bajo la
clave `"Suplementos"`. Código muerto desde el primer día. Salió
porque el BLOQUE 14 falló 1 de cada 20 veces en el caso más apretado:
0,55 g de aceite de girasol.

Es la **segunda** vez en ese archivo: el límite de 2 suplementos cayó
en la misma trampa. Para la categoría de un alimento se usa
`alimentos[n]["categoria"]`, NUNCA `categoria_de[n]`.

Y de ahí sale el **BLOQUE 16**, que es lo que de verdad lo vigila:
`resolver()` apunta, por cada regla, cuántas filas puso y cuántos
coeficientes llevan, y el bloque exige que ninguna de las 16 reglas
duras valga cero. Contar filas no bastaba — el fallo del límite de
suplementos añade la fila **vacía**, y `0 <= 2` se cumple siempre.
Comprobado con tres sabotajes y los tres se cazan. Si se añade una
restricción a `resolver()`, hay que pasarla por `_fila(...)` y
apuntarla en el BLOQUE 16; si no, puede morir en silencio como
murieron estas dos.
