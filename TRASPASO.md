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
