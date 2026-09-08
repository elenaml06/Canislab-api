# Rawku — API del motor nutricional

Backend FastAPI + motor MILP en scipy. Desplegado en Render.
El frontend vive en `elenaml06/canislab-web` (Vercel, rawku.app).

**Empieza por `PENDIENTE.md`**: es el índice de lo que queda por hacer,
priorizado. Desde el 6 de septiembre es solo eso — un índice de una línea
por punto — y cada punto vive en uno de cuatro archivos por tema
(`PENDIENTE_DECISIONES.md`, `PENDIENTE_DINERO_Y_SALUD.md`,
`PENDIENTE_PRODUCTO.md`, `PENDIENTE_NUTRICION.md`). Abre solo el que toque
la tarea, no los cuatro de golpe.

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
| `der.py` | Cálculo de las kcal. ⚠️ Ver «la duplicación que hay que vigilar (DER)», abajo |
| `analizador.py` | `/analizar`: la dieta que ya le da el dueño. Comparte `MAPA` con el semáforo a propósito — discreparon una vez por la fibra |
| `especies.py`, `accesibles.py` | Qué especie es cada alimento |
| `transicion.py` | Plan de cambio gradual de dieta |
| `persistencia.py`, `observabilidad.py` | Supabase y Sentry |
| `auditar_catalogo.py` | Huecos y datos raros del catálogo, y quién se queda sin aminograma. Lo ejecuta el BLOQUE 19 |
| `auditar_fediaf.py` | Cada valor del JSON contra la tabla de FEDIAF. Lo ejecuta el BLOQUE 18 |
| `contrastar_fuentes.py` | Una ficha del catálogo contra **BEDCA, CIQUAL y USDA a la vez**, en el orden de `Bases.md`. **No lo ejecuta la batería** (necesita red y se baja 10 MB): es la herramienta de quien va a mirar una ficha. Trae dentro cómo se lee cada fuente — el XML de BEDCA hay que reconstruirlo de su `query.js`, y con la lista de atributos recortada devuelve el cuerpo vacío sin dar error |

### Endpoints: cuáles usa la app y cuáles no

Los que llama el frontend hoy: `/menu/v2`, `/menu/semana`,
`/menu/varios-perros`, `/menu/anadir`, `/menu/cambiar`, `/menu/quitar`,
`/menu/revalidar`, `/analizar`, `/alimentos`, `/formular/*`, `/pauta/*`,
`/patologias`, `/relajacion`, y los de Stripe.

`GET /patologias` (7 de septiembre) sirve la tabla de `patologias.json` con
los topes, su fuente, su motivo y **el margen contra el límite de FEDIAF del
mismo nutriente** — renal aprieta el fósforo a 1200 con el mínimo en 1160:
un 3,4 % de sitio. Existe para que quien firma una pauta pueda leer el
número que decide si sale menú, y **para que ese número no se copie a la
app**: sería la tercera copia de la misma tabla, que es exactamente cómo se
desincronizó la del `POST /menu`. Lo vigila el BLOQUE 44, cifra a cifra
contra el archivo que aplica el solver.

`GET /relajacion` (8 de septiembre) sirve los peldaños de la escalera con su
nombre y qué suelta cada uno, y `/menu/v2` y `/formular/autocompletar`
aceptan `peldano`. **Con un peldaño elegido no se baja solo**: bajar sería
cambiarle la decisión a quien la ha tomado, que es lo contrario de por qué se
puede elegir. Un peldaño mueve las proporciones de BARF y cuántos suplementos
caben — la FORMA, regla 3 — y **nunca** los 43 requisitos, el ratio Ca:P ni
los topes de seguridad y de patología: eso lo vigila el BLOQUE 45, que además
comprueba que la lista servida es la que recorre `_escalera_de_relajacion` y
no una copia. Y el menú dice ahora **siempre** en qué peldaño salió, no solo
cuando hubo que bajar: «no dice nada» y «estricto» se leían igual, y quien
firma necesita poder afirmar lo segundo.

**Los que nadie llama pero siguen expuestos**: `/catalogo/{tamano}/{etapa}`,
`/der`, `/transicion` y `/perro/{perro_id}/menus`. Se dejan a propósito: no
duplican nada, son funciones que existen y que la app puede volver a usar.
Pero nadie los prueba usando la app, así que si algo se rompe ahí solo lo
ve la batería.
`/perro/{perro_id}/menus` **era el único agujero de la regla 1** hasta el 7
de septiembre, y no por descuido: la tabla `menus` guardaba nombre, gramos
y kcal, así que un menú guardado no se podía verificar ni en principio.
Ahora `guardar_menu` escribe el contexto (etapa, DER, pesos, patologías)
junto al menú y el endpoint lo verifica al leerlo — o dice que no puede,
si es una fila anterior a ese cambio. Lo vigila el BLOQUE 47.

`POST /menu` **ya no existe** (26 de agosto). Era el motor anterior al MILP
y arrastraba su propia tabla de patologías, desincronizada de la buena:
fósforo renal a 1.400 en vez de 1.200, cobre en hepatopatía a 3,0 y sin
bloquear, grasa en pancreatitis al 25 % de las kcal, diabetes bajando la
grasa siempre, y urato, cistinuria y «otra» sin existir. No llegó a dar
menús malos porque `_garantizar_verificado()` los habría rechazado — que es
otra forma de decir que ese camino construía menús que el filtro final iba
a tirar. El BLOQUE 24 vigila que no vuelva.

### Los 12 aminoácidos y el techo de lisina

Los 41 nutrientes de FEDIAF (Tabla III-3b) se verifican los 41 desde el 28
de agosto, incluidos los 12 aminoácidos esenciales — con el Ca:P y el calcio
de raza grande son las 43 filas completas. `metionina_cistina` y
`fenilalanina_tirosina` no son claves de los alimentos: son sumas que
calcula `valor_nutriente`, como `epa_dha`.

**Una excepción escrita y probada**: el techo de lisina (7,00 g/1000 kcal,
solo en crecimiento) no se aplica — 0 de 15 menús de cachorro caben debajo,
porque la lisina va detrás de la proteína y una ración BARF de cachorro
lleva ~134 g/1000kcal contra un mínimo de 50. Aplicarlo dejaría a todos los
cachorros sin menú. La excepción vive en `verificar.MAXIMOS_NO_APLICADOS`
—única lista, leída por solver y semáforo vía `maximo_de()`—, con la
pregunta pendiente para el nutricionista en `PENDIENTE_DECISIONES.md`. El **mínimo**
de lisina sí se aplica; solo se quita el techo.

Lo vigila el BLOQUE 27: que los doce sigan en `MAPA`, que las dos sumas
sumen de verdad, que la proteína sin aminograma no pase del 5 % de un menú
real, y que el techo de lisina siga siendo el único máximo no aplicado.
Faltan 16 aminogramas (once suplementos, y la laringe de vacuno vacía a
propósito por ser cartílago). Detalle completo, las medidas y la trampa de
unidades del triptófano: `HISTORIA_TECNICA.md`.

### Los mínimos escalan hacia arriba, nunca hacia abajo

`minimo_de()` en `verificar.py` es el único sitio que escala los mínimos
cuando el perro come menos (ecuación de FEDIAF 7.2.5) — y `maximo_de()` el
único que sabe de máximos. Solo hacia arriba: no hay base en FEDIAF para
bajar el mínimo de un perro que come más. No escalan la grasa, el
EPA+DHA/linolénico/araquidónico (no hay requerimiento absoluto en adulto), ni
crecimiento/gestación/lactancia.

**Los máximos no escalan nunca** —son concentración, no cantidad— así que la
ventana entre mínimo y máximo se cierra según bajan las kcal. En dieta
húmeda el selenio se cruza en DER 45,2: por debajo el motor devuelve
`imposible_por_aritmetica` (nutriente + los dos números) en vez del «quita
una restricción» de siempre, porque ahí no hay combinación que lo arregle.
Lo vigila el BLOQUE 34.

El peso de referencia para escalar es `peso_objetivo_kg`, no el real — sin
ese campo se usa el real y se escala de más (lado seguro); lo vigila
`tests/peso-objetivo-en-cada-peticion.spec.js` en `canislab-web`. Detalle
completo y las medidas: `HISTORIA_TECNICA.md`.

### La duplicación que hay que vigilar (DER)

El DER se calcula dos veces: `der.py` aquí y `calcularDER()`/`src/der.js` en
`canislab-web` — y **manda el del frontend**, que se envía en
`der_objetivo`; `der.py` solo corre si alguien llama a `/der`, que no llama
nadie. Se vigilan por separado contra `der_casos.json` (85 casos, **el
mismo archivo en los dos repos**): BLOQUE 23 aquí, `der-contrato.spec.js`
allí. Si tocas la fórmula de un lado, regenera esperados y copia
`der_casos.json` a los dos repos — los dos commits, o ninguno. Detalle
completo: `HISTORIA_TECNICA.md`.

### Los documentos

`CLAUDE.md` (esto) es la entrada. `HISTORIA_TECNICA.md` tiene el detalle
completo — medidas, cifras, el porqué — de los temas que aquí solo llevan
un resumen de dos líneas: los aminoácidos, el escalado de mínimos y
máximos, la duplicación del DER, los datos dudosos. Ábrelo solo cuando la
tarea toque justo esa parte del motor. `PENDIENTE.md` es el índice de lo
que queda, ordenado por prioridad — desde el 6 de septiembre, solo el
índice: cada punto vive en `PENDIENTE_DECISIONES.md`,
`PENDIENTE_DINERO_Y_SALUD.md`, `PENDIENTE_PRODUCTO.md` o
`PENDIENTE_NUTRICION.md` según el tema, y se abre solo el que toque la
tarea. Lo ya resuelto vive en `HECHO.md`, y la investigación o el código
detrás de un pendiente que no hace falta releer cada vez, en
`PENDIENTE_DETALLE.md` (el bloque de veterinarios señala directamente a
`VETERINARIOS.md`, que ya lo tenía completo) — los dos con resumen de una
línea y puntero en su sitio, para no recargar lo que se lee al empezar
cualquier sesión. `DATOS_QUE_FALTAN.md` son los valores del catálogo
que hay que conseguir de BEDCA/CIQUAL/USDA, uno a uno — **no los rellena el
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
peor: `linoleico` es **omega-6** y `linolenico` es **omega-3** — se
diferencian en una letra, son cosas opuestas, y si se cargan cambiados no
salta nada, el menú sale verde igual. Lo vigilan el BLOQUE 26 y
`auditar_catalogo.py` (los nueve alimentos donde el omega-3 supera al
omega-6).

**Los TRES campos que dicen qué sabemos de cada 0.** Un 0 puede ser «no lo
tiene» o «no lo sabemos» — eso lo separa `sin_dato`. Un valor declarado y
erróneo (tiene forma de dato bueno y pasa cualquier validación de formato)
va en **`dato_dudoso`**, que `verificar()` devuelve junto al menú igual que
los huecos. Lo vigila el BLOQUE 28. Los tres casos reales que lo motivaron
(omega-3 de salmón, fósforo de harina de hueso, cobre de polvo de sangre):
`HISTORIA_TECNICA.md`.
El tercero es **`cero_verificado`** (7 de septiembre): un 0 al que alguien
fue a la fuente, comprobó que es real, y dejó escrito cuál y cuándo. Existe
porque el aviso `[SOSPECHOSO]` de `auditar_catalogo.py` deduce los ceros
raros del propio catálogo —si el 90 % de los DEMÁS de su categoría tienen
ese nutriente y este no, se dice— y sin una forma de contestarle volvería a
preguntar lo mismo cada vez, que es como una auditoría deja de leerse. Es el
mismo patrón que `purinas_fuente` o `fuente_epa_dha`: la procedencia vive en
la ficha, no en una lista central. Lo vigila el BLOQUE 46, que no se
conforma con verlo salir limpio — vacía la tiamina de un hígado en una copia
del catálogo y exige que la auditoría lo encuentre.

**Y las tres bases de datos no son intercambiables.** El orden lo fija
`Bases.md`: BEDCA (primaria) → Köber 2017 para el hueso → CIQUAL → USDA. No
es preferencia, es que **ninguna tiene los 41 nutrientes**: BEDCA trae yodo
pero ni un aminoácido, USDA trae los 12 aminoácidos y la colina pero no
publica yodo, CIQUAL trae todos los ácidos grasos pero tampoco aminoácidos.
Casi todos los huecos del catálogo están justo donde ninguna llegaba — no
son fallos de copia: donde una ficha entera sale del mismo registro de USDA,
coinciden 153 de 156 celdas. Y BEDCA distingue «midieron 0» (`value_type`
`AR`) de «no hay cifra» (`TR` con la celda vacía), distinción que se pierde
al volcarla a un CSV y que convierte huecos en ceros mudos. Detalle y las
medidas: `PENDIENTE_NUTRICION.md` §5-quater.

En la raíz, los cuatro: `alimentos_v3_final.json` (el catálogo),
`requerimientos_v2_final.json` (la tabla de FEDIAF), `catalogo_menus.json`
(los 36 menús precalculados de la vista previa y sus 180 variantes) y
`der_casos.json` (el contrato del DER, ver arriba).

Los dos primeros llevan **sello** en `/verificar`: si cambian sin que se
actualice el hash en `main.py`, la API lo dice. Los otros dos no, y es a
propósito — un menú del catálogo corrupto lo rechaza
`_garantizar_verificado()` igual que cualquier otro, y el contrato del DER
se comprueba entero en cada batería.

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
