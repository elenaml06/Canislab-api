# Lo ya hecho (sacado de PENDIENTE.md)

`PENDIENTE.md` empieza siendo lo primero que se lee en cualquier sesión
(`CLAUDE.md` lo pide así). Con los puntos ya resueltos mezclados entre los
pendientes de verdad, pesaba 81,8 KB y crecía con cada cosa que se
terminaba, no con lo que quedaba por hacer.

Este archivo no se lee solo: se abre cuando hace falta el detalle de algo
que ya se resolvió — por qué se decidió así, qué se midió, qué PR lo trajo.
Nada de esto es agenda; es historial. Se separó el 6 de septiembre.

## Hecho el 20 de agosto

- Sentry en el backend, con avisos por correo.
- Los cinco fallos del webhook de Stripe, que **no había funcionado nunca**.
- Verificación obligatoria contra los 30 requisitos en **todos** los
  caminos, incluido el cambio de etapa (`/menu/revalidar`).
- La escalera de relajación: del 23 % de fallos con alergias al 0 %, sin
  ceder en ningún límite.
- Tope de volumen y porciones que escalan con el tamaño del perro.
- Cobro de prueba completado de punta a punta y premium activado de verdad.

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
> `PENDIENTE_DECISIONES.md`): aquella sigue pendiente de decisión; lo de
> aquí es que el tope, sea el que sea, se cumpla.

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

## El umbral de calcio en cachorros de raza grande estaba en 25kg, FEDIAF dice 15kg — hecho el 7 de septiembre

`RAZA_GRANDE_O_GIGANTE_KG` valía 25 en `motor/motor_completo.py` (la
restricción del solver) y en `main.py`
(`_minimo_calcio_raza_grande_roto()`, el semáforo de verificación final).
La nota "b" de la Tabla III-3b de FEDIAF —leída directamente del PDF
oficial, no de una fuente secundaria— fija el umbral en **15 kg de peso
adulto esperado**, no 25. Cachorros de razas de 15-25 kg en crecimiento
tardío no estaban recibiendo el calcio reforzado que exige FEDIAF. La
cifra de calcio en sí (2500 mg) ya era correcta — solo el peso del corte
estaba mal, copiado de una fuente secundaria (un artículo de Vet Clinics
que cita FEDIAF) nunca contrastada contra el PDF.

Corregido en los dos sitios, que tienen que coincidir siempre por
definición (mismo criterio, misma fila de la tabla).

La corrección hace aflorar un caso límite real que antes no existía
(cachorro de raza grande sin hueso + 3 alergias, ~33% de fallo aislado):
se añadió un reintento por infactibilidad en `_resolver_menu_v2_interno`
(máx. 2 intentos extra), mismo criterio que ya usa `/menu/varios-perros`
("el motor lleva aleatoriedad a propósito, la misma petición sale casi
siempre a la segunda"). Reduce el fallo aislado a ~10-15%.

PR #82. `pruebas_completas.py` entero, TODO EN VERDE.

## Linoleico de "Grasa de pollo" y categoría de "Laringe de vacuno" — hecho el 7 de septiembre

Dos huecos que llevaban desde el 25 de agosto en `PENDIENTE_NUTRICION.md`:

- **Linoleico**: 0 → 19,5 g/100g. USDA FoodData Central FDC 173564 "Fat,
  chicken" (SR Legacy, NDB 4542) — su proteína (0) y grasa (99,8) ya
  coincidían exactas con esta ficha, así que es con altísima probabilidad
  la misma fuente que el resto de la fila. Importaba porque el linoleico
  tiene máximo en cachorros, y un hueco contado como cero no lo detectaría.
- **Laringe de vacuno**: categoría "Hueso carnoso" → "Extras". Bloqueada
  por tejido tiroideo desde el 6 de septiembre (`TIROIDES_EXCLUIR`), nunca
  puede aportar hueso a ningún menú, así que su categoría antigua solo
  servía para disparar dos avisos ya conocidos en `auditar_catalogo.py`
  ("hueso con poco calcio, ¿es cartílago?"). 0 referencias en
  `catalogo_menus.json` (comprobado), no afecta a los menús precalculados.

PR #82 (junto con lo del calcio). `auditar_catalogo.py` limpio de estos
dos avisos.

## Taurina y L-carnitina: dato en las 159 fichas, y suelo activado en `dcm_taurina_respondedora` — hecho el 7 de septiembre

**Parte 1 — el dato (PR #83).** Ninguna ficha del catálogo tenía taurina
ni L-carnitina. Se añadieron las dos claves (mg/100g) a las 159 fichas:
valor real donde hay fuente citable, `sin_dato` donde no — nunca un
número inventado. Fuente principal: Spitze, Wong, Rogers y Fascetti
(2003), *J. Anim. Physiol. Anim. Nutr.* 87:251-262, el estudio más
completo de taurina en ingredientes de dieta animal (carnes, vísceras,
pescados y vegetales, directo o por familia/tejido cercano según
confianza). L-carnitina tiene cobertura más limitada (agregados por
especie de la literatura general). Estadística: taurina 130/159 con
valor real, 29 `sin_dato`; L-carnitina 101/159, 58 `sin_dato`.

Mapeo por nombre revisado ficha a ficha con cuidado explícito de no
confundir familias por coincidencia de texto — comprobado que "Repollo"
no hereda nada de "Pollo": Spitze confirma taurina=0 en todos los
vegetales, y así queda su ficha.

Se corrigió de paso un falso positivo de "HUECOS" en `auditar_catalogo.py`
que las dos claves nuevas introducían en 27 verduras y frutas, mismo
criterio que ya existía para `purinas_fuente`: un cero con fuente escrita
no es un hueco.

**Parte 2 — la activación (mismo día).** La patología
`dcm_taurina_respondedora` ya existía desde la ronda SACN5 del 6-7 de
septiembre, pero solo como aviso: "la taurina no está entre los 41
nutrientes que este motor mide". Y el mecanismo de "suelos por patología"
(el espejo de los topes, para cuando una fuente pide un MÍNIMO más alto
que el de FEDIAF) también existía ya, usado por primera vez en `artrosis`
y `dermatosis_zinc`. Con el dato de la Parte 1 puesto, solo faltaba
conectar las dos piezas:

- `Taurina` y `L_carnitina`, dos filas nuevas en
  `requerimientos_v2_final.json`, mismo patrón que `Fibra`: las seis
  columnas a "-", no exigen ni limitan nada a un perro sano.
- Las dos claves añadidas a `verificar.MAPA`.
- `suelos_por_1000kcal` en `dcm_taurina_respondedora`: taurina ≥250,
  L-carnitina ≥50 mg/1000kcal, SACN5 5ª ed. cap.36 «Cardiovascular
  Disease», Tabla 36-4 (0,1% y 0,02% de materia seca a 4000kcal/kgMS).

Probado contra el solver (adulto 20kg): el menú que sale de verdad lleva
414 mg de taurina y 138 mg de L-carnitina por 1000kcal, muy por encima
del suelo, porque ya incluye corazón e hígado. Verificado también en
`_garantizar_verificado()` (regla 2 del `CLAUDE.md`: los topes/suelos por
patología no son solo del solver), no se quedó en aviso.

De paso, revisando `PENDIENTE_DECISIONES.md` y `PENDIENTE_NUTRICION.md`
contra el estado real del código (no de memoria) para esta sesión,
salieron cuatro cosas que ya estaban resueltas y seguían marcadas como
pendientes: las 4 fichas de aminoácidos sospechosas (pulmón de cordero,
calamar, pulpo, sepia — ya confirmadas reales contra USDA el 7 de
septiembre), el contraste de timo/testículos con USDA (testículos de
cordero ya no existe, timo ya cita FDC 170194 directo, y el acceso a la
API de USDA con `DEMO_KEY` sí funciona — la nota decía lo contrario), y
la lista de hígados que faltan por especie (pavo y pato ya existían,
solo faltaba corregir la lista). Se reformuló también con más precisión
la pregunta pendiente del máximo de lisina, tras leer la metodología
exacta de FEDIAF en el PDF (p.22, sección Lysine): no es un ratio con la
proteína, es un no-effect-level de lisina CRISTALINA suplementada
(Czarnecki et al. 1985) convertido a energía — la pregunta real para el
nutricionista es si eso generaliza a la lisina de una proteína entera.

`pruebas_completas.py` entero, TODO EN VERDE.

## Quitado un máximo de fósforo sin fuente que llevaba desde el primer PR del repo — hecho el 7 de septiembre

Comprobando la Tabla III-3b de FEDIAF entera (los 41 nutrientes) contra
la transcripción de `auditar_fediaf.py`, celda a celda, para cerrar de
verdad el pendiente de "repasar la transcripción" (no solo lecturas
puntuales de una nota concreta), apareció una fila que **no tenía nada
que ver con FEDIAF**: `MAXIMOS["Fósforo"] = {"Adulto": 4000}`, con el
mismo número en `requerimientos_v2_final.json`. Los dos coincidían entre
sí, así que la auditoría nunca lo vería — exactamente el riesgo que se
buscaba con esta revisión.

Investigado a fondo antes de tocar nada, no solo "no lo encontré":
- **FEDIAF** (Tabla III-3a y III-3b): ningún número. Solo la nota "h",
  informativa sobre biodisponibilidad, sin cifra.
- **NRC 2006**: *"There are insufficient data on which to base an SUL
  for P in dogs"* (no hay datos para fijar un límite superior seguro).
- **Dobenecker et al. 2021** (PLOS ONE, el estudio más específico sobre
  toxicidad de fósforo en perros adultos sanos, en `canislab-fuentes`):
  *"More work is needed... no-effect-levels can be defined"* — ni la
  fuente más centrada en el tema da un número.
- **AAFCO/SACN5 cap.6**: solo dan mínimo de fósforo, nunca máximo.

El número llevaba ahí desde el primer PR de historia del repo
(`ae7878b`), antes de que existiera la disciplina de "cada cifra lleva
fuente". Y no era teórico: recortaba de verdad el menú automático
estándar de un adulto de 20kg, que salía justo en el límite (4000,0)
antes de quitarlo.

Quitado: `maxAdulto` pasa a "-" en el JSON, "Fósforo" se mueve de
`MAXIMOS` a `SIN_MAXIMO` en `auditar_fediaf.py`. Comprobado después que
el fósforo real de un menú no se dispara al quitar el techo (sigue en
~3970 mg/1000kcal, porque lo limita lo que dan los alimentos de verdad,
no un número artificial). `auditar_fediaf.py`: 234 comprobaciones
cuadran (subió de 232), 0 discrepancias. `pruebas_completas.py` entero,
TODO EN VERDE.

De paso, la revisión completa de la tabla confirmó que **los otros 40
nutrientes coinciden exactamente** con el PDF — esta fue la única
discrepancia real en todo el documento.

## Vuelve Pets Purest, con una ficha que sí cuadra — hecho el 7 de septiembre

Pets Purest Aceite de Salmón había salido del catálogo el 27 de agosto
(BLOQUE30 de `pruebas_completas.py`) porque su EPA/DHA solo aparecía en
fichas de marketing del fabricante, replicadas por revendedores, sin
ningún análisis propio — y era el más denso de los cinco aceites, así que
el solver lo prefería por delante de opciones mejor documentadas.

La usuaria mandó la foto de la etiqueta física del bote que tiene en casa
("Pets Purest 100% Natural Pure Scottish Salmon Oil", 300ml), con
"Analytical Constituents" y "Nutritional Content" propios — no una ficha
de marketing de un revendedor, sino el dato real del producto. Con eso el
motivo original de la salida deja de aplicar, y por instrucción explícita
se añadió como dato real, no como `dato_dudoso`.

Ficha nueva, "Pets Purest Aceite de Salmón Escocés" (160ª del catálogo),
mismo patrón que los otros dos aceites de salmón: grasa/proteína/fibra de
la propia etiqueta (99 g grasa, no 99,5 — es lo que declara ESTA etiqueta),
EPA y DHA en el extremo bajo de los rangos declarados (7% y 10%, sobre
7-9% y 10-12%) para no sobreestimar, linoleico = omega-6 total (6,6%, ya
que en el omega-6 de un aceite de pescado el ácido linoleico sí domina de
verdad), linolénico en `sin_dato` en vez de estimado por resta (mismo
criterio que sus dos hermanos), vitamina E en `sin_dato` pese a que la
etiqueta menciona "0,5% tocoferoles" — en la lista de INGREDIENTES, no en
el análisis nutricional, mismo criterio ya aplicado a las otras dos
marcas. Sin dosis de fabricante: ni la etiqueta ni la web dan el volumen
de una pulsación en ml.

Actualizado con esto:
- `pruebas_completas.py` BLOQUE28a: la cuenta de aceites en categoría
  Omega-3 pasa de 3 a 4, con el mensaje de fallo explicando por qué.
- `pruebas_completas.py` BLOQUE30: quitada la entrada de Pets Purest del
  diccionario `_FUERA_30` (el propio bloque dice qué hacer en este caso:
  "si vuelve con una ficha que cuadre, quita esta comprobación"), con un
  comentario fechado explicando el porqué en su lugar.
- `main.py`: sello de `alimentos_v3_final.json` actualizado (160 fichas).

De paso, dos correcciones de texto en `patologias.json` que no cambian
ningún número: `raza_predispuesta_cobre` decía que el motor excluye el
hígado (u otros alimentos ricos en cobre) como prevención — comprobado en
el código que ese mecanismo no existe, así que el aviso mentía sobre lo
que hace la app. Corregido para decir la verdad (el menú es normal, sin
exclusión de hígado, y sugerir excluirlo a mano en Personalizar si el
veterinario lo quiere). Y `dcm_asociada_a_dieta`: el aviso no mencionaba
explícitamente el boniato/patata, que la propia fuente FDA cita "en menor
medida" junto a las legumbres — ampliado con el mismo argumento estructural
(nunca son la fuente calórica principal en una ración BARF).

`pruebas_completas.py` entero, TODO EN VERDE (aparte del hueco de tiempo ya
conocido del BLOQUE43 con un perro de juguete de 1,5 kg y 3 s de
presupuesto, que no es de esta ficha: el menú se calcula bien, lo que
falta a veces es el margen para verificarlo, y verificar cuesta 1,6 ms).
