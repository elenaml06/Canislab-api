# Rawku — API del motor nutricional

Backend FastAPI + motor MILP en scipy. Desplegado en Render.
El frontend vive en `elenaml06/canislab-web` (Vercel, rawku.app).

**Empieza por `PENDIENTE.md`**: ahí está lo que queda por hacer, priorizado.

## Qué es esto

Calcula raciones BARF para perros que cumplen los 30 requisitos de FEDIAF
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
   los 30 requisitos + el ratio Ca:P + los límites de seguridad crónica.
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
     que el motor cierra los 30 requisitos.
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
| `motor_completo.py` | **El corazón.** `resolver()` monta el problema MILP y lo resuelve: los 29 nutrientes, el ratio Ca:P y los topes de seguridad como restricciones simultáneas. Aquí viven también `PATOLOGIAS` y `topes_de_patologias()` |
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
| `requerimientos_v2_final.json` | Los requisitos de FEDIAF. **43 filas** desde el 26 de agosto: los 29 nutrientes que el motor verifica, el ratio Ca:P, el calcio de raza grande, y **los 12 aminoácidos esenciales, que están puestos y auditados pero TODAVÍA NO SE VERIFICAN** — ver abajo |
| `requisitos.py` | Cargar la tabla de FEDIAF, resolver la etapa y la dosis máxima que marca el fabricante de cada suplemento. Era `optimizador.py`, 1.124 líneas donde esto convivía con el motor anterior al MILP y con una copia desincronizada de la tabla de patologías. El motor viejo se borró el 26 de agosto; quedan 121 líneas |
| `der.py` | Cálculo de las kcal. ⚠️ Ver «la duplicación que hay que vigilar», abajo |
| `analizador.py` | `/analizar`: la dieta que ya le da el dueño. Comparte `MAPA` con el semáforo a propósito — discreparon una vez por la fibra |
| `especies.py`, `accesibles.py` | Qué especie es cada alimento |
| `transicion.py` | Plan de cambio gradual de dieta |
| `persistencia.py`, `observabilidad.py` | Supabase y Sentry |
| `auditar_catalogo.py` | Huecos y datos raros del catálogo. Lo ejecuta el BLOQUE 19 |
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

### Los 12 aminoácidos: puestos, auditados y sin activar

La Tabla III-3b de FEDIAF pide **41 nutrientes** para el perro y el motor
verifica **29**. Lo que falta son los doce aminoácidos esenciales, que
están en la tabla desde siempre, entre `Protein` y `Fat`. La transcripción
de `auditar_fediaf.py` se los había saltado, así que la auditoría decía que
cubríamos la tabla entera cuando cubríamos siete de cada diez filas.

Desde el 26 de agosto están en `requerimientos_v2_final.json` con sus 48
valores, y la auditoría los comprueba contra el PDF: **232 comprobaciones,
0 discrepancias**, frente a las 161 de antes.

**Pero no están en `verificar.MAPA`, y eso es a propósito**: ninguno de los
166 alimentos del catálogo trae dato de aminoácidos. Medido activando solo
la lisina: **la app deja de dar menús**, porque cada alimento cuenta como
cero y el mínimo se vuelve inalcanzable. Y si algunos sí tuvieran el dato,
sería peor todavía — el motor se iría hacia ellos, y eso es un sesgo que no
se ve.

El día que el catálogo traiga aminoácidos hay que activarlos. Lo vigila el
**BLOQUE 27**, que salta por los dos lados: si alguien borra las filas, y
si alguien las activa antes de que haya datos.

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
decidió el 28 de agosto, en qué orden se construye, y las dos cosas
que si se hacen mal no se arreglan después — que el profesional entre
con su cuenta y nunca con la del dueño, y que una prescripción por
debajo de FEDIAF se verifica igual, contra un juego de requisitos
escrito que viaja con el menú.

### Los datos

**`UNIDADES.md` es lo primero que hay que leer antes de tocar el catálogo**:
en qué unidad va cada uno de los 29 nutrientes, sobre qué base (100 g de
alimento tal cual se da) y las cuatro trampas que se cuelan siempre. La
peor, la primera del documento: `linoleico` es **omega-6** y `linolenico`
es **omega-3**. Se diferencian en una letra, son cosas opuestas, y si se
cargan cambiados no salta nada — los dos son nutrientes válidos con
valores plausibles, y el menú sale verde igual. Lo vigilan el BLOQUE 26,
que ancla el aceite de girasol y el de linaza, y `auditar_catalogo.py`,
que lista los nueve alimentos donde el omega-3 supera al omega-6.

**Los dos campos que dicen qué NO nos creemos.** Un 0 en el catálogo puede
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
etapa los 30 requisitos: un perro de diez años volvía como cachorro.

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
