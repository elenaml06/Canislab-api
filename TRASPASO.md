# Traspaso — dos sesiones del 8 de septiembre de 2026

⚠️ **Este fichero tiene DOS documentos, y no es un error.** El 8 de septiembre
trabajaron dos sesiones en paralelo sin saber la una de la otra, y las dos
escribieron su traspaso con este mismo nombre. Al fusionarlas el 11 de
septiembre no se descarta ninguno: cada uno cuenta lo que hizo su rama, y
borrar uno sería tirar el único sitio donde está escrito por qué se hizo así.

1. **Sesión de limpieza y orden** — abajo, la primera.
2. **Sesión del catálogo direccionable** (`fuentes_id` y los huecos declarados)
   — la segunda.

---

# Traspaso — sesión de limpieza y orden (8 de septiembre de 2026)

Escrito al parar, a petición expresa, porque el inventario del proyecto lo
está haciendo otra sesión y esto no puede quedarse solo en el historial de
un chat.

**Lo primero, porque es lo único con riesgo:** hay un documento del repo que
lleva a borrar ramas que tienen trabajo dentro. Corregido abajo, y en
`PENDIENTE.md` / `PENDIENTE_PRODUCTO.md` / `PENDIENTE_DETALLE.md`.

**Qué NO se ha tocado en esta sesión:** nada nutricional. Ni
`requerimientos_v2_final.json`, ni `alimentos_v3_final.json`, ni
`patologias.json`, ni `der.py`/`der.js`, ni los topes de seguridad, ni el
`MAPA` del verificador, ni `_garantizar_verificado`. Ni un valor, ni una
coma.

---

## 1 · Las ramas: qué dice el repo, qué es verdad, y con qué se comprobó

### El problema

`PENDIENTE.md` decía: *«Borrar las ramas viejas de los dos repos (15 ya
comprobadas, nada que rescatar)»*. Leído hoy, eso dice «las ramas que hay
están comprobadas, bórralas». Y no es así.

**La auditoría del 23 de agosto no está equivocada: está caducada, y su
alcance está mal contado.** Comprobó 15 ramas concretas y sus conclusiones
siguen siendo ciertas para esas 15. Pero de aquellas 15, **once ya no
existen** (se borraron) y hoy hay **once ramas vivas, de las cuales seis son
posteriores a esa auditoría y nunca se miraron**. Entre las seis suman **22
commits que no están en `main`**.

Un documento que manda borrar y cuya lista no cubre lo que hay es más
peligroso que no tener documento, porque el que lo lee no tiene motivo para
desconfiar.

### Cómo se comprueba de verdad

```bash
git fetch origin main claude/<rama> --depth=200
git merge-base --is-ancestor origin/claude/<rama> origin/main && echo DENTRO || echo FUERA
git rev-list --count origin/claude/<rama> ^origin/main     # cuántos commits únicos
```

**`--is-ancestor` es la prueba buena.** Dice si el tip de la rama está
contenido en `main`: si lo está, la rama no tiene literalmente nada propio y
borrarla no puede perder nada.

⚠️ **`git cherry` NO sirve aquí, y lo comprobé.** Compara por `patch-id`, y
un commit fusionado con *squash* o retocado después cambia de `patch-id`.
Marcó `claude/de-punta-a-punta-con-la-api-real` como «no está en main»
cuando `playwright.real.config.js` y `tests/de-punta-a-punta.spec.js` **sí
están** en `main` hoy. Si alguien usa `cherry` para decidir, va a conservar
ramas muertas — o peor, a creer que una comprobación se hizo.

Tampoco sirve `git diff origin/main <rama> --stat`: estas ramas están tan
atrás que el diff sale dominado por lo que `main` ha añadido después (una da
«10.777 borrados», que es `main` avanzando, no la rama aportando).

### La lista real, a 8 de septiembre de 2026

**`Canislab-api` — 2 ramas, las DOS con trabajo fuera de `main`:**

| Rama | Commits fuera | ¿Suena a nutrición? |
|---|---|---|
| `claude/el-corazon-de-ternera-es-musculo` | 4 | **SÍ** |
| `claude/nutrition-audit-data-validation-bihto9` | 11 | **SÍ** |

**`canislab-web` — 9 ramas: 5 dentro de `main`, 4 fuera:**

| Rama | ¿Dentro de `main`? | Commits fuera | ¿Suena a nutrición? |
|---|---|---|---|
| `claude/aviso-composicion-menu` | ✅ dentro | 0 | no |
| `claude/ficha-completa` | ✅ dentro | 0 | no |
| `claude/multi-perro` | ✅ dentro | 0 | no |
| `claude/perfil-perro-no-se-guarda` | ✅ dentro | 0 | no |
| `claude/rawku-sentry-login-nav-ro683v` | ✅ dentro | 0 | no |
| `claude/calcio-raza-grande-contrato` | ❌ fuera | 3 | **SÍ** |
| `claude/laringe-y-trazas` | ❌ fuera | 2 | **SÍ** |
| `claude/de-punta-a-punta-con-la-api-real` | ❌ fuera | 1 | no |
| `claude/la-ficha-clinica-pinta-los-que-cumplen` | ❌ fuera | 1 | no |

### ⚠️ CUATRO DE LAS QUE ESTÁN FUERA SUENAN A TRABAJO NUTRICIONAL

Lo digo explícitamente porque hay una sesión cerrando justo eso, y porque
ninguna de las cuatro se ha abierto ni leído en esta sesión — solo se han
leído los títulos de sus commits.

**`claude/el-corazon-de-ternera-es-musculo`** (API, 4 commits)
```
6d2e450 El corazón de ternera es músculo, no víscera
562419a BLOQUE 19 y BLOQUE 4: dos listas mas que se habian quedado viejas
fad7535 La carga, con los 13 fallos de la bateria arreglados
36ac2b5 WIP: la carga puesta, con la bateria en rojo (13 fallos)
```
Cambia de categoría un alimento del catálogo. Y su commit base es un **WIP
con la batería en rojo**: si alguien la fusiona sin mirar, entra ese estado.

**`claude/nutrition-audit-data-validation-bihto9`** (API, 11 commits)
```
01d11d4 Apuntar qué del paquete aplicado NO está verificado contra su fuente
94bb1ee La batería, en verde: los 48 bloques, 559 s
204f4c3 El riesgo del hueso que de verdad ocurre, y la frase que no se puede escribir
bf1f0ad La batería, en verde: los 47 bloques, 590 s
5f31b60 La columna de humedad, las legumbres con patata, y el suelo de vitamina E
884a887 La batería, en verde: los 46 bloques, 593 s
a219321 Las legumbres de grano en cardiopatía, y la energía del hueso declarada
5bdbdec Lo que no tiene procedencia, fuera: dorada, yodos, cobres y hueso
06bcbbd El techo legal de la vitamina D, el tejido tiroideo, y la vía rápida que no miraba las exclusiones
65b7bf4 Conectar `trazas` de punta a punta, y el sésamo vuelve a estar marcado
38971dc Las 103 correcciones del catálogo, la laringe fuera y el tercer estado de un cero
```
Esta es la más pesada: habla de 103 correcciones del catálogo, humedad, el
techo de la vitamina D, el suelo de vitamina E, y de retirar valores sin
procedencia. **Parte de esto parece estar ya en `main`** (el tercer estado
de un cero, `cero_verificado`, existe; la laringe ya está en Extras), pero
parte quizá no. Nadie ha comparado a fondo.

**`claude/calcio-raza-grande-contrato`** (web, 3 commits) — «La app deja de
ofrecer siete alimentos que el motor ya no tiene», más la instrucción de la
borraja. Toca la lista de alimentos de la app.

**`claude/laringe-y-trazas`** (web, 2 commits) — la laringe fuera del
selector, los tres cuellos, y las trazas en la ficha clínica.

**Recomendación: que estas cuatro las mire quien esté cerrando la parte
nutricional, antes que nadie borre nada.** No es trabajo de limpieza.

---

## 2 · Las 5 ramas que iba a borrar, y con qué concluí que eran seguras

Iba a borrar **solo** estas cinco, todas en `canislab-web`:

```
claude/aviso-composicion-menu
claude/ficha-completa
claude/multi-perro
claude/perfil-perro-no-se-guarda
claude/rawku-sentry-login-nav-ro683v
```

**La comprobación, una por una:**

```bash
git fetch -q origin claude/<rama> --depth=200
git merge-base --is-ancestor FETCH_HEAD origin/main   # salió 0 en las cinco
```

Salir 0 en `--is-ancestor` significa que el tip de la rama **es un
antepasado de `main`**: cada commit suyo ya está en `main`, la rama no
contiene ni una línea que `main` no tenga. No es «parece fusionada», es
«matemáticamente no hay nada dentro». Lo confirmé además con
`git rev-list --count FETCH_HEAD ^origin/main`, que dio **0** en las cinco.

Las cinco coinciden exactamente con las cinco de `canislab-web` que ya
declaraba segura la auditoría del 23 de agosto. Esa parte del documento sí
era correcta.

**No se borró ninguna.** Lo intenté, el clasificador de permisos denegó el
`git push origin --delete`, y acto seguido llegó la instrucción de no tocar
ramas. Siguen las once vivas. (Nota de paso: `PENDIENTE_DETALLE.md` dice que
«desde el contenedor no se puede: el proxy bloquea el borrado de ramas» —
sigue siendo cierto hoy, por otra vía.)

---

## 3 · Los 286 MB de PDFs de `canislab-fuentes`: opciones y coste

### Los números

- `canislab-fuentes` pesa **308 MB**; `sacn5/` son **293 MB** de eso (95 %).
- Son **70 PDFs** (los capítulos de *Small Animal Clinical Nutrition*, 5ª
  ed.) más sus **70 `.txt`** extraídos con `pdftotext -layout`, que ocupan
  **7,1 MB entre todos**.
- El `.git` del repo pesa **246 MB**. Ese es el coste real: se paga en cada
  clon, siempre, aunque solo quieras leer un `.txt`.
- En la documentación se cita el `.txt` **6 veces** y el `.pdf` **2**.

### Lo que comprobé sobre la calidad del `.txt`

Esto es lo que decide si el PDF es imprescindible o es respaldo. **Las
tablas sobreviven a la extracción.** La `Table 6-1` de `cap6.txt` sale con
las cuatro columnas alineadas y legibles, y el texto a dos columnas del
cuerpo se interpola correctamente. `pdftotext -layout` está haciendo bien su
trabajo aquí.

Con eso, el PDF de SACN5 es **respaldo para comprobar una tabla dudosa a
ojo**, no la herramienta de trabajo diaria. (Ojo: para FEDIAF el README dice
lo contrario y con razón — ahí el PDF sí hace falta por el riesgo de
columnas pegadas en las tablas III-3a/III-3b. Eso son 2,6 MB, no 293.)

### Las cuatro opciones reales

**(a) Dejarlo como está.**
Coste: 0 de trabajo. Cada clon se lleva 246 MB. En este contenedor tardó
minutos. Riesgo: ninguno.

**(b) `git lfs migrate import --include="sacn5/*.pdf"`.**
El clon baja a **~22 MB**. Coste: **reescribe el historial entero** — todos
los SHA cambian —, exige `force-push` a `main`, y cualquier clon local
existente hay que rehacerlo. Y un aviso concreto que he verificado en esta
sesión: **el carril anónimo de git de estas sesiones no sirve objetos LFS**,
así que una sesión de Claude Code que clone el repo se bajaría los PDFs como
punteros vacíos. Los `.txt` seguirían llegando bien.

**(c) `git filter-repo` (o BFG) para sacarlos del historial, y guardar los
PDFs fuera de git** (disco, Drive).
Máximo ahorro y el repo queda limpio de verdad. Mismo coste de reescritura y
`force-push` que (b), **más** que los PDFs dejan de estar versionados: si se
pierde la copia, se perdió. Son la copia legal de la usuaria.

**(d) Un repo aparte, `canislab-fuentes-pdf`.**
Coste: dos repos que mantener y dos sitios donde buscar. Y no arregla nada
por sí solo: el historial de `canislab-fuentes` seguiría cargando los 246 MB
salvo que además se reescriba.

### Mi recomendación

**(a), por ahora.** Es lo único de toda esta limpieza que es irreversible, y
el problema que resuelve es incomodidad, no correción. Un archivo documental
que se clona de vez en cuando puede permitirse pesar. Si algún día molesta
de verdad, **(b)** con los ojos abiertos sobre lo de LFS.

Lo que sí conviene decidir pronto es **no meter más PDFs grandes sin
pensarlo**, porque el coste de arreglarlo sube con cada uno.

---

## 4 · Por qué partir `main.py` DESPUÉS del CI y no antes

`main.py` tiene **4.875 líneas** y 67 funciones, y se pueden sacar dos
bloques enteros sin cambiar comportamiento: Stripe + Supabase (~600 líneas)
y las garantías de seguridad (~800). Quedaría en torno a 3.400.

**No lo he hecho, y el orden importa por tres motivos:**

**1. El corte no arregla nada; solo hace el fichero navegable.** Busqué
duplicación de verdad en `main.py` (bloques de 8 líneas repetidos): hay
**tres**, y los tres son legítimos — son los reintentos de
`_escalera_de_relajacion`. O sea que las 4.875 líneas son contenido, no
copia-pega. Un cambio que no arregla nada nunca debe ser el que entra sin
red de seguridad.

**2. Lo que se movería incluye `_garantizar_verificado`, que ES la regla 1.**
Por ahí pasa todo menú antes de salir. Mover eso a otro fichero es
exactamente el código que no se toca sin que algo automático lo compruebe.

**3. Hoy la única prueba de que el corte es neutro es ejecutar la batería
entera a mano.** Tarda ~10 minutos (959 s medidos en este contenedor de 4
CPU; 559-593 s en la máquina de la usuaria) y depende de acordarse. En el
historial hay un commit llamado literalmente *«WIP: la carga puesta, con la
bateria en rojo (13 fallos)»* — en rojo sí se empuja.

Con el workflow ya puesto (`.github/workflows/bateria.yml`, en la rama
`claude/audit-api-sources-web-gk95ir`), el PR del corte se demuestra solo, y
si rompe algo el fallo queda pegado al PR en vez de aparecer tres días
después. El CI cuesta 10 minutos de espera; el corte sin CI cuesta un fallo
silencioso en el camino que garantiza que ningún menú sale sin verificar.

**En resumen: el CI primero porque el corte de `main.py` es justo el cambio
que necesita el CI para ser seguro, y no al revés.**

---

## 5 · Lo que sé y no está escrito en ningún fichero de ningún repo

Esto es lo que se perdería si esta sesión desaparece. Va aunque parezca
menor: casi todo es una medida o una trampa concreta.

### Sobre la batería y el CI

- **La batería no necesita red ni claves de verdad.** Se fabrica su propio
  Stripe (`STRIPE_WEBHOOK_SECRET` inventado) y su propio Supabase
  (`https://supabase.dementira`) dentro del BLOQUE 10, y los borra al
  terminar. Por eso se puede meter en CI sin configurar un solo secreto.
  Esto no estaba escrito en ninguna parte y es la razón de que el workflow
  sea posible.
- **`pruebas_completas.py` termina con `sys.exit(1)` si hay fallos.** Sin
  eso el workflow saldría verde siempre. Comprobado.
- **Cuánto tarda de verdad:** 959 s en este contenedor (4 CPU), 559/590/593 s
  según los propios commits de la usuaria. El `CLAUDE.md` decía «~2 min»
  desde hacía meses. Ya está corregido.
- **El único bloque que puede fallar por la máquina y no por el código es el
  BLOQUE 7**, que exige que una llamada al solver no pase de 15 s. Medido
  aquí: **3,3 s**. Hay 4,5× de margen. Si algún día empieza a fallar solo en
  CI, el arreglo es mirar el `time_limit`, no subir el número.
- **La suite de la web da 374 pasadas y 2 saltadas en ~5,2 min.** Las 2
  saltadas son las del muro de pago (`VITE_PAYWALL` en `off`), lo que
  coincide con lo que dice `PENDIENTE_PRODUCTO.md`.

### Sobre el código, cosas que sorprenden

- **Ni `main.py` ni `App.jsx` tenían duplicación real.** Busqué bloques
  repetidos en los dos: 3 en cada uno, y todos legítimos. La intuición de
  «un fichero de 11.798 líneas estará lleno de copia-pega» es falsa aquí. El
  problema era navegabilidad, no redundancia — y eso cambia qué arreglo
  tiene sentido.
- **`RawkuOnboardingInterna` (en `App.jsx`) son 6.653 líneas con 86
  `useState` y SIETE pantallas dentro** (`onboarding`, `generador`, `casa`,
  `misMenus`, `pacientes`, `pautas`, `seccion`). La parte de veterinario
  está entre las líneas relativas ~3.462 y ~5.832 de esa función, marcada
  con comentarios de bloque: `LA PUERTA DEL VETERINARIO`, `LA FICHA DEL
  PACIENTE`, `EL HISTORIAL DE PAUTAS FIRMADAS`, `LA LISTA DE PACIENTES`. Ese
  es el mapa para quien la parta: **no son componentes, es JSX en línea
  compartiendo ese estado**, así que sacarlas obliga a levantar estado. No
  es mover código.
- **Los `import` de `App.jsx` NO están todos arriba.** Llegan hasta la línea
  92 y están intercalados con código (un bloque de `localStorage` y el
  `ErrorBoundary`). Cualquier herramienta que suponga «los imports están en
  las primeras 40 líneas» se rompe — me pasó al partirlo.

### La trampa que más cara puede salir

- **Al analizar código JS línea a línea, hay que limpiar las CADENAS ANTES
  que los COMENTARIOS.** Al revés, un `https://…` dentro de una cadena se
  lee como comentario `//` y se come el resto de la línea, con su llave de
  cierre incluida. Eso hizo que `Fuentes()` (que cita URLs) pareciera llegar
  hasta el final del fichero.
  **Esto no es teórico para este proyecto:** hay CUATRO pruebas que analizan
  el código fuente en vez de la pantalla (`peso-adulto-en-cada-peticion`,
  `peso-objetivo-en-cada-peticion`, `catalogo-app-y-motor`,
  `un-solo-alimento`). Cualquiera que se toque tiene esta trampa delante.

### Sobre las pruebas que leen el código

- Esas cuatro pruebas hacían `readFileSync("../src/App.jsx")` y buscaban
  marcas de texto. Ahora pasan por `tests/fuente.js`, que lee **todo
  `src/`** — porque al partir `App.jsx`, `llamarRecalculo` se fue a
  `vistamenus.jsx` y `CATEGORIAS_ALIMENTO` a `catalogoapp.jsx`, y las cuatro
  se habrían quedado buscando donde ya no hay nada.
- **`tests/catalogo-app-y-motor.spec.js` nunca se había ejecutado de verdad
  en ningún sitio automático.** Tenía un `test.skip(!fs.existsSync(...))` que
  la daba por buena si el repo del motor no estaba al lado, y **no había
  ningún CI en el repo de la web**. Es la prueba que pilló que un hígado de
  pato salía como «Extra» con la instrucción de los aceites. Corregido: ahora
  falla y dice qué clonar.
- Verifiqué las dos pruebas con el fallo puesto a mano, como manda el
  `CLAUDE.md`: quitarle `"Gallina"` al catálogo de la app la caza, y quitar
  `peso_adulto_esperado_kg` de `llamarRecalculo` (que ahora vive en otro
  fichero) también.

### Sobre los repos y los datos

- **`der_casos.json` es idéntico en los dos repos hoy.** md5
  `92506f87725fbfa084de25701ab0e8d8`. El contrato del DER está sincronizado.
- **La regla 5 se cumple hoy.** `CATEGORIAS_QUE_ELIGE_EL_USUARIO`
  (`main.py:1649`) y las seis claves de `CATEGORIAS_ALIMENTO` (ahora en
  `src/catalogoapp.jsx`) coinciden: Carne muscular, Pescados y mariscos,
  Hueso carnoso, Vísceras, Hígado, Verduras y frutas.
- **El grafo de los 15 documentos del repo de la API no tiene ni un
  huérfano**: todos están citados desde otro. Es de las cosas que están
  mejor de lo que parecen desde fuera.
- **`radiografia.py` tiene CERO importaciones en todo el repo** y no está
  muerto: es la herramienta que compara las ENTRADAS del motor entre ramas.
  Faltaba en el mapa de `CLAUDE.md` — ya está puesto —, y es el candidato
  número uno a que alguien lo borre por parecer basura.
- **Ninguno de los tres repos ejecutaba sus pruebas en CI.** El único
  workflow que existía era el ping que mantiene despierto a Render.
- **`canislab-web` no tiene `CLAUDE.md`.** Tiene un README de 320 líneas, al
  que le he añadido el mapa de módulos, pero no hay un documento de entrada
  equivalente al de la API.

### Un detalle menor del corte de `App.jsx`

- Al mover los bloques me llevé también los comentarios pegados justo
  encima. Uno de ellos es huérfano: un `⚠️ QUITADO (5 agosto) —
  POOL_CANDIDATOS…` que hablaba de código ya borrado y que estaba entre
  `especieDe` y `formatearGramos`. Ha acabado en `src/formato.js`. No rompe
  nada, pero si alguien lo busca, está ahí.

---

## 6 · Dónde está cada cosa

Tres ramas, **ninguna fusionada, ningún PR abierto, ninguna rama borrada**:

| Repo | Rama | Qué lleva |
|---|---|---|
| `Canislab-api` | `claude/audit-api-sources-web-gk95ir` | Mapa de `CLAUDE.md` al día + `.github/workflows/bateria.yml` + este `TRASPASO.md` + las tres correcciones de las ramas |
| `canislab-web` | `claude/limpieza-web-appjsx-ci` | `App.jsx` 11.799 → 7.498 (8 módulos), la prueba que se saltaba sola, `herramientas/`, `.github/workflows/pruebas.yml`, mapa en el README |
| `canislab-fuentes` | `claude/limpieza-fuentes` | Un solo `INVENTARIO_FUENTES.md` + `.gitignore` |

**Comprobado antes de empujar cada una:** la batería entera en verde (50
bloques, 959 s, 0 fallos) para la API; lint + build + 374 pruebas para la
web, idéntico a antes del corte.

---

# TRASPASO — sesión del 8 de septiembre

Rama: `claude/nutricion-pendiente-vuoobq`. **Sin PR y sin fusionar.** Dos
commits de código (`9bc0a8d`, `c6af011`) y los de este archivo. Escrito al
pararme para que nadie tenga que deducir nada de los mensajes de commit.

---

## 0. Estado de los dos commits: los dos VERIFICADOS

| commit | qué es | batería |
|---|---|---|
| `9bc0a8d` | 95 casillas a hueco declarado + columna de humedad | ✅ verde · 51 bloques · 821 s |
| `c6af011` | `fuentes_id` en 99 fichas + `fijar_identificadores.py` | ✅ verde · 51 bloques · **857 s** |

⚠️ **Corregido el mismo día.** Este apartado decía que `c6af011` no estaba
verificado, porque la ejecución de la batería se interrumpió al parar la
sesión. **Terminó después**, en segundo plano, y salió en verde. Se
comprobaron las tres cosas antes de cambiar esta línea, porque un «ya está
verificado» equivocado es peor que el aviso:

- la ejecución arrancó **después** de añadir la guarda de especie al BLOQUE
  51, y el `pruebas_completas.py` de `c6af011` la lleva;
- el árbol de trabajo no cambió entre lanzarla y hacer el commit, así que
  corrió contra ese contenido exacto;
- y el sello declarado en el `main.py` de `c6af011` cuadra con su propio
  `alimentos_v3_final.json` — si no, un bloque habría fallado.

**Aun así sigue sin fusionarse**: no hay PR y no se pidió ninguno.

⚠️ **Y una trampa que casi cuela**: la batería se lanzó como
`python3 pruebas_completas.py | tail -30`, y el código de salida de una
tubería es el del **último** comando. Salió 0 con la batería en rojo o en
verde por igual. **El código de salida de una tubería no dice nada**: hay
que leer la línea «TODO EN VERDE» de la salida.

---

## 1. DECISIÓN CERRADA: el `TR` de BEDCA NO significa «trazas»

**Esto es lo que no puede volver a abrirse.** Es una comprobación hecha
contra la fuente, no una opinión, y si no queda escrita como decisión
alguien reabrirá la rama dentro de un mes y la deshará.

### Qué se rechazó

La rama `claude/nutrition-audit-data-validation-bihto9` (3-6 de septiembre,
nunca fusionada) creaba un campo **`trazas`** con 14 celdas de vitamina A y
D en diez pescados, y **las sacaba de `sin_dato`**. El argumento escrito era
razonable: «una traza es un dato publicado, no un hueco».

### Contra qué fuente se comprobó, y qué dijo

Se le pidieron las fichas al servicio de BEDCA una a una el 8 de septiembre
(`contrastar_fuentes.py`, que imprime el `value_type`). **13 de las 14
celdas son `TR` con la celda VACÍA**, y ninguna es `AR` con un 0. En el
esquema de BEDCA:

| código | significa |
|---|---|
| `AR` / `BE` + un número | es una **medida**, aunque el número sea 0 |
| `LZ` + un 0 | cero **lógico**: por composición no puede tener |
| `TR` + **celda vacía** | **NO HAY CIFRA**. Es un hueco |

Comprobado ficha a ficha: Merluza (2347), Bacalao (2302, «Bacalao, crudo»),
Bacaladilla (2136), Lenguado (2341), Lubina (2344), Calamar (2320), Pulpo
(2471), Sepia (2635), Gamba roja (817, «Gamba roja, cruda») y, de refuerzo,
Merluza congelada (825). Las 13 celdas de esas nueve fichas: `TR` vacío.

**La que falta es una sola y conviene decir cuál:** la vitamina D de «Pollo
con piel (sin hueso)». Esa ficha **no tiene registro identificado en BEDCA**
—es una de las 26 pendientes del apartado 14 de `PENDIENTE_NUTRICION.md`—,
así que no hay fila contra la que comprobarla. Sigue en `sin_dato` en
`main`, que es lo conservador.

**Y una corroboración que vale más que las trece:** «Gamba, hervida» (2337)
da vitamina D = **0 con `AR`**, o sea un cero MEDIDO, mientras que «Gamba
roja, cruda» (817) da `TR` vacío. BEDCA distingue las dos cosas de verdad, y
esa es exactamente la distinción que el campo `trazas` borraba.

**La prueba de que el campo era exactamente eso y no otra cosa:** donde la
rama **no** marcaba traza —la vitamina A de calamar, pulpo y sepia— BEDCA
**sí** publica cifra con `AR`: 63, 70 y 2. El campo `trazas` calcaba celda
por celda las `TR`. No era una lectura parcial: era la lectura del código.

### Qué habría pasado si se aplica

Catorce huecos correctamente declarados se habrían convertido en **ceros
medidos falsos**. Y eso no es cosmético: un `sin_dato` no cuenta como cero
contra un techo —se imputa al percentil 90 de su familia, ver
`constructor.valor_para_maximo`—, mientras que un cero medido sí defiende.
El resultado habría sido **aflojar el techo crónico de la vitamina D** en
diez pescados, que es uno de los cinco topes duros de la regla 2 del
`CLAUDE.md`.

`main` ya las tenía bien, en `sin_dato`. **No se rescató, y no se rescata.**
Lo vigila el BLOQUE 51, que además falla si vuelve a aparecer el campo
`trazas` en el catálogo.

---

## 2. Qué se rescató de esa rama y qué se descartó A PROPÓSITO

Para que nadie la vuelva a abrir entera. **La rama salió del `main` del 2 de
septiembre**, y `main` ha cambiado mucho desde entonces: aplicarla tal cual
—o hacer cherry-pick— **borra trabajo posterior verificado**.

### ✅ Rescatado (en `9bc0a8d`)

- **86 casillas** donde el mismo número se repite entre fichas distintas: 21
  cobres con solo cuatro valores en todo el grupo, y 70 celdas en seis
  huesos carnosos donde conejo, pato, pollo y cordero declaran la misma
  vitamina A, la misma D y la misma riboflavina siendo especies distintas.
  Pasan a `sin_dato`. Comprobado antes: **BEDCA no publica cobre** para
  besugo, lubina, pulpo, calamar, trucha, lenguado ni pescadilla — la celda
  no existe en la respuesta.
- **La columna de humedad** con procedencia en 65 fichas
  (`humedad_g_100g`, `humedad_fuente`, `humedad_fdc`).

### ❌ Descartado a propósito

- **El campo `trazas`** — apartado 1. No se toca.
- **46 casillas de las 132 que la rama vacía**: son valores que se
  contrastaron **después** del 2 de septiembre contra BEDCA/CIQUAL/USDA. El
  EPA, el DHA y los **400 µg de yodo del aceite de hígado de bacalao** están
  entre ellos, y el yodo es un tope crónico. Aplicar la rama los borra.
- **Las 69 diferencias del cerebro.** Ojo, que es fácil contarlo al revés:
  la rama tiene **una sola** ficha, «Cerebro de ternera», y lleva dentro los
  números de la **vaca** (proteína 10,86 · grasa 10,3 · calcio 43, que son
  clavados los de USDA 168622, *Beef brain*). `main` la partió en dos, y hoy
  cada una tiene los suyos, comprobado: `Cerebro de vaca` = 10,86 / 10,3 /
  43 (USDA 168622) y `Cerebro de ternera` = 10,4 / 8,6 / 12, que es USDA
  174351, *Veal brain* (10,32 / 8,21 / 10). Aplicar la rama devuelve los
  números de vaca a la ficha de ternera.
- **Borrar los tres cuellos y la laringe del catálogo**: `main` los conserva
  y los **bloquea en el solver** por tejido tiroideo, que es mejor — el
  alimento sigue existiendo y el motivo queda escrito.

### 🔁 Ya estaba en `main` por otro camino (no hace falta rescatarlo)

Comprobado una a una: las 103 correcciones del catálogo (albahaca fósforo
56, hígado de pollo vitA 3296 y cobre 0,492, dorada grasa 1 y vitD 1,5), el
techo legal de la vitamina D y el bloqueo de tejido tiroideo. Llegaron por
los PR #76 y #80.

### Hasta dónde llegó esta revisión, para que nadie herede una certeza falsa

**Lo que sí se auditó entero:** su `alimentos_v3_final.json`, casilla por
casilla contra el de `main` (las 210 diferencias, clasificadas una a una), y
lo que su `main.py` hacía con `trazas`.

**Lo que NO se leyó línea a línea:** su `pruebas_completas.py` (+529 líneas)
y su `motor/seguridad.py` (+176). Se comprobó que **el trabajo grande de
esos dos archivos ya está en `main`** —el techo legal de la vitamina D y el
bloqueo de tejido tiroideo, por el PR #76— pero no que no quede ninguna
prueba suelta que mereciera la pena.

Así que la conclusión honesta es: **del catálogo no queda nada que
rescatar**, y del código queda por mirar un rato de pruebas. Si alguien la
borra, eso es lo que se pierde.

---

## 3. Lo que sé y no está escrito en ningún fichero del repo

Esto es lo que se pierde cuando termina la sesión.

### 3.1 El repositorio se clona en SUPERFICIAL, y eso hace mentir a git

`git merge-base` decía «no merge base» en nueve ramas y `git rev-list`
contaba 380-400 commits sin fusionar. **Era mentira**: faltaba la historia.
Con `git fetch --unshallow` esas mismas ramas resultaron tener **cero
commits propios** — su PR se había fusionado entero.

Quien audite ramas sin hacer `--unshallow` primero concluirá que hay diez
ramas con cientos de commits perdidos y no las borrará nunca.

### 3.2 Los nombres reales de los componentes en BEDCA

Perdí una comprobación entera por esto y estuve a punto de vaciar diez
yodos correctos:

- El yodo se llama **`ioduro`**. Buscar «yodo» devuelve vacío, y de ahí sale
  la conclusión falsa de que BEDCA no publica yodo para las verduras. **Sí
  lo publica**: `ioduro` = 1 con `AR` en acelga, alcachofa, arándano,
  calabacín, calabaza, coliflor y dátil, confirmado en los siete.
- La vitamina A es `Vitamina A equivalentes de retinol de actividades de
  retinos y carotenoides`.
- La grasa es `grasa, total (lipidos totales)` y el agua `agua (humedad)`.

### 3.3 Las tres fuentes publican la energía en kJ, y USDA la publica dos veces

USDA tiene **dos filas de energía con el mismo nombre**: `nutrient_id` 1008
en kcal y 1062 en kJ. Un diccionario indexado por nombre se queda con la que
llegue última. Para el bacalao devuelve **343**, que son los kJ; en kcal son
82. Comparar 343 contra nuestros 82 descarta la fila correcta.

BEDCA y CIQUAL publican solo kJ: hay que dividir entre 4,184.

### 3.4 `usda_ficha()` recorre 2 millones de filas en cada llamada

`food_nutrient.csv` se lee entero y linealmente. Llamarlo por candidato
convierte una pasada de 5 minutos en uno de horas. Hay que indexar una vez
(lo hace `fijar_identificadores.py`, no `contrastar_fuentes.py`).

### 3.5 Qué constantes de familia son CORRECTAS — comprobado, no repetir el viaje

El detector nuevo de `auditar_catalogo.py` señala cifras repetidas en 6+
fichas de una categoría. **Fui a la fuente en las cuatro más grandes:**

| aviso | veredicto | por qué |
|---|---|---|
| colina 65 en 17 pescados | ✅ **correcto** | USDA da 65 al eglefino, calamar, lenguado, perca, pulpo y trucha, y 65,2 al bacalao |
| zinc 0,1 en 14 verduras | ✅ **correcto** | BEDCA lo da con `AR` individual: manzana, pepino, alcachofa |
| yodo 1 en 10 verduras | ✅ **correcto** | `ioduro`=1 con `AR`, confirmado en siete por separado |
| manganeso 0,035 en 8 pescados blancos | ❌ **inventado** | 0,035 es el valor del **calamar** en USDA. A sus especies USDA les da 0,011 (eglefino), 0,014 (lenguado), 0,015 (lubina) y 0,7 (perca) |

Solo el manganeso se corrigió (a `sin_dato`, sin mapear a ojo). Y la colina
de la lubina, 65 → 60,80: USDA da 60,8 al *sea bass*.

**Y el detector no puede ser una prueba de pase/fallo:** disparaba 87 veces
sobre el catálogo ya arreglado. La L-carnitina de siete carnes vale 10,0
porque Spitze 2003 la publica así para todas. Por eso vive en la auditoría
como aviso y no en la batería.

### 3.6 Las medidas del cambio de las 86 casillas

Se midió antes de entregarlo y no está en ningún sitio salvo el mensaje del
commit: ninguna familia baja de los 3 donantes de `MINIMO_FAMILIA`, los 16
cobres de pescado **suben** de 0,08 a 0,41 imputado, y **cero fichas
empeoran** — ninguna que ya fuera hueco se queda con un percentil más bajo.
El cambio es monótonamente más conservador.

### 3.7 Por qué la identificación automática necesita TRES guardas

Las tres salieron de fallos reales de la primera pasada, no de teoría:

1. **Preparación.** Para «Bacalao» la búsqueda devolvió BEDCA 745, *Bacalao
   **ahumado***, y las tres cifras cuadraban: proteína 18,3 contra 18,2,
   grasa 0,55 contra 1, agua 81,2 contra 81,2. Ahumar no cambia casi nada de
   esos tres y multiplica el sodio. Con la guarda puesta encontró el bueno:
   BEDCA 2302, *Bacalao, crudo*.
2. **Especie.** Para `Cerebro de vaca` la huella daba SEGURO con BEDCA 1047
   (*Sesos de **ternera***) y CIQUAL 40006 (*Cervelle, **veau***). **Es
   exactamente el error que hubo que deshacer este mismo día** rehaciendo la
   ficha entera. Vaca y ternera se parecen en proteína, grasa y agua: la
   huella numérica no los separa nunca. Solo el nombre.
3. **Sin huella.** Un alimento que es casi todo grasa no tiene huella:
   proteína 0, grasa ~100 y agua 0 describen a **todos** los aceites por
   igual. Ahí la máquina no puede demostrar nada y no debe intentarlo.

### 3.8 La dorada se delata sola

`fijar_identificadores.py` la rechaza con las tres magnitudes comparables,
**sin que nadie le haya dicho que es sospechosa**. Confirma por un camino
independiente lo que ya sabíamos: su fila de BEDCA mezcla dos peces. Está
marcada `dato_no_fiable`.

### 3.9 Cosas del entorno que cuestan media hora cada una

- **Borrar ramas remotas está prohibido** en esta sesión: `git push --delete`
  devuelve `HTTP 403` del proxy. Empujar sí funciona. El servidor MCP de
  GitHub tampoco tiene herramienta para borrar ramas. Lo tiene que hacer una
  persona desde la web.
- **`pkill -f pruebas_completas.py` se mata a sí mismo** si el script que lo
  ejecuta contiene esa cadena en su texto. Y **`pgrep -f` casa con la propia
  línea de comandos**, así que devuelve PID fantasma.
- **El catálogo se escribe con `indent=1`, `ensure_ascii=False` y salto
  final.** Con `indent=2` el diff pasa de 240 a 24.402 líneas.
- **El sello es de JSON canónico, no de los bytes**:
  `sha256(json.dumps(d, sort_keys=True, ensure_ascii=True))[:16]`.
- La batería entera tarda **~820 s** con 51 bloques.

### 3.10 Estado de las otras ramas y de Supabase

- **`claude/el-corazon-de-ternera-es-musculo`** — 318 alimentos nuevos, y
  **las 318 sin aminograma** (lisina = 0). Es del 27 de agosto, un día antes
  de que se encendieran los 12 aminoácidos: hoy reventaría el BLOQUE 27.
  Nunca tuvo PR y no hay una línea en la documentación diciendo por qué se
  quedó fuera. No se descartó: se olvidó.
- **`motor`** — la subida del 10 de agosto de los ocho archivos del motor en
  la raíz. Todos están en `motor/` y más grandes. No tiene nada que
  rescatar; quedó sin borrar porque no lleva el prefijo `claude/`.
- **Supabase: las nueve migraciones están aplicadas.** Y ojo con la consulta
  de comprobación: `creado_por` va en **`public.menus`**, no en
  `public.perros` — solo `tutor_nombre` y `tutor_contacto` van en `perros`.
  Una consulta que busque las tres en `perros` da «2 de 3» y parece que
  falta una migración que no falta.

---

## 4. Lo que estaba haciendo cuando paré

Dando identificador de fuente a las fichas del catálogo, para que el
contraste deje de ser un descubrimiento y pase a ser un `diff`: con el
identificador fijado se pueden comparar las **7.407 casillas** contra su
fila de origen en cada pasada, y lo que no cuadre sale con nombre y número.

99 fichas ya lo tienen. 38 no deben tenerlo (16 suplementos de marca con
datos de etiqueta, la sal, el yoduro potásico y 9 huesos carnosos, que vienen
de Köber 2017). **Quedan 26 para mirar a ojo**, listadas una a una con su
motivo en `PENDIENTE_NUTRICION.md` apartado 14.

El paso siguiente, que no llegué a hacer, era el contraste exhaustivo de las
7.407 casillas.
