# Traspaso: `margen_del_profesional`

**8 de septiembre.** Escrito a petición expresa para la sesión que va a
extender esto. Va en la rama `claude/veterinary-mode-ui-fixes-s9l5j7`, que
está **parada y sin PR** porque toca `patologias.json`.

La mitad de pantalla está en `canislab-web`, rama
`claude/vet-margen-por-patologia` (commit `4bd3386`), también sin PR. Las dos
mitades van juntas o no van.

---

## 1 · Qué es y de dónde sale

Cada tope y cada suelo de `patologias.json` lleva ahora un bloque:

```json
"margen_del_profesional": {
  "direccion": "bajar" | "subir" | null,
  "hasta": <número o null>,
  "criterio": "qué variable clínica lo mueve, con la fuente",
  "donde_para": "el límite duro y por qué"
}
```

Nació de una crítica concreta: el bloque «qué es inamovible y qué decides
tú» de la ficha clínica decía **lo mismo en las 40 patologías** — «nada de la
patología», y tres líneas fijas, una de ellas el peldaño de BARF, que se
elige en cada menú de todas formas.

**Ningún tope ni suelo cambia de valor.** Esto solo estructura el rango que
ya estaba escrito en prosa dentro del propio `por_que`, verificado contra los
primarios en sesiones anteriores. Lo sirve `GET /patologias` desde el mismo
archivo que aplica el solver, y lo pinta `src/topespatologia.jsx`.

## 2 · Qué NO cubre hoy

Esto es lo primero que hay que entender antes de extenderlo.

- **No es un control: es un texto.** El veterinario LEE hasta dónde podría
  mover el número. No puede moverlo. Nada en el motor acepta un tope por
  paciente. Que se pueda es el paso siguiente, y no está hecho.
- **No cubre las 24 patologías sin topes numéricos.** Ahí el bloque dice
  «esta condición no fija ningún límite numérico», que es verdad pero es lo
  mínimo. Lo que esas patologías sí hacen (excluir fruta, excluir alimentos
  por nombre, bloquear, exigir prescripción por debajo de FEDIAF) vive en
  otros campos (`excluye_fruta`, `nota`, `motivo_no_formulable`,
  `necesita_bajo_fediaf`, `nutriente_frontera`,
  `objetivo_terapeutico_por_1000kcal`) y no está encuadrado en el mismo
  marco.
- **No dice qué ve el TUTOR.** El encargo mayor —marcar en todo lo
  nutricional qué ve el usuario, qué mueve el veterinario y hasta dónde—
  tiene tres ejes y esto cubre uno y medio: qué mueve el profesional y hasta
  dónde. Lo que ve el dueño sigue decidiéndose caso a caso en la pantalla.
- **No hay unidades en el bloque.** `hasta` es un número desnudo; la unidad
  se hereda del tope. Al extenderlo a otros ejes, esto se rompe (ver §5).
- **`direccion: "subir"` en un TOPE significa relajar.** Solo pasa en
  pancreatitis-grasa. Es correcto según la fuente, pero es la línea que más
  fácil se lee mal: no se puede convertir en un control sin decidir antes si
  un veterinario puede relajar un tope de patología, que hoy las reglas 2 y 3
  de `CLAUDE.md` no permiten a nadie.

## 3 · Los 19, uno a uno, y cuáles hay que revisar

«Prosa clara» = el rango estaba escrito con sus dos números en el `por_que`.
**«Interpretado» = lo puse yo y hay que revisarlo.**

| # | Patología · nutriente | `hasta` | Fuente del rango | |
|---|---|---|---|---|
| 1 | renal · fósforo | — (no se mueve) | SACN5 cap. 37, Tabla 37-9 («0.2 to 0.5 %» MS = 500-1250) | prosa clara |
| 2 | renal_avanzada · fósforo | — (no se mueve) | Igual que renal | prosa clara |
| 3 | pancreatitis · proteína | 52,1 | SACN5 cap. 67, Tabla 67-3 («15 to 30 %» MS = 37,5-75) | **interpretado**: el extremo de la fuente es 37,5, que está BAJO el mínimo de FEDIAF (52,10); puse el mínimo de FEDIAF como parada |
| 4 | pancreatitis · grasa | 37,5 | SACN5 cap. 67, Tabla 67-3 | prosa clara — pero ver §5, es el caso de las unidades |
| 5 | oxalato · vitamina D | — (no se mueve) | Máximo LEGAL de FEDIAF, Reglamento (UE) 2017/1492 | prosa clara |
| 6 | hepatopatía · cobre | — | Center 2026 JAVMA; SACN5 cap. 68, Tabla 68-8 (objetivo 1,2-1,25) | **interpretado**: `direccion: "bajar"` con `hasta: null`. El objetivo terapéutico está bajo el mínimo de FEDIAF (2,08), o sea que el margen real es cero sin prescripción. Debería probablemente ser `direccion: null`, como renal |
| 7 | cardiopatía (genérica) · sodio | 480 | ACVIM 2019 (Keene), por estadio | **interpretado**: puse el valor del estadio D como suelo de la entrada genérica. Discutible: la genérica existe justo porque NO se sabe el estadio |
| 8 | cardiopatía_b2 · sodio | 800 | Escala moderna por estadio (800-990) | prosa clara |
| 9 | cardiopatía_c · sodio | 500 | Escala moderna por estadio (500-790) | prosa clara |
| 10 | cardiopatía_d · sodio | 290 | Estadio D: «<500» | **interpretado**: 290 es el mínimo de FEDIAF, no una cifra de la fuente |
| 11 | hiperlipidemia · grasa | 13,75 | SACN5 cap. 28, Tabla 28-2 («<12 %» MS = 30) | **interpretado**: la fuente da UN número, no un rango; 13,75 es el mínimo de FEDIAF |
| 12 | hiperlipidemia · fibra | — (sin techo) | SACN5 cap. 28, «at least 10 % DM» | prosa clara. FEDIAF no pone mínimo ni máximo de fibra, así que «sin techo» es literal — y por eso mismo es el suelo más fácil de subir sin darse cuenta |
| 13 | obesidad · grasa | 28 | SACN5 cap. 27, Tabla 27-4 («≤9 %» MS = 22,5) | **interpretado, y no es nutrición**: 28 es un límite MEDIDO del solver con el catálogo real (22,5 y hasta 27 no dan menú ni en 40 s; 28 sí, 5 de 5). Mezcla una cifra de ingeniería con las de fuente. Merece campo aparte |
| 14 | dcm · taurina | — (sin techo) | SACN5 cap. 36, Tabla 36-4 («≥0,1 %» MS) | prosa clara |
| 15 | dcm · L-carnitina | — (sin techo) | SACN5 cap. 36, Tabla 36-4 («≥0,02 %» MS) | prosa clara |
| 16 | PLE / linfangiectasia · grasa | 13,75 | SACN5 cap. 58, Tabla 58-1 («<15 %» MS = 37,5) | **interpretado**: la fuente no da suelo; 13,75 es el mínimo de FEDIAF |
| 17 | EPI · grasa | 25 | SACN5 cap. 66, Tabla 66-1 («10 to 15 %» MS = 25-37,5) | prosa clara. El mejor ejemplo del concepto: el valor por defecto es el extremo ALTO a propósito, porque el tratamiento son las enzimas |
| 18 | artrosis · EPA+DHA | 2,75 | SACN5 cap. 34, Tabla 34-2 («0.4 to 1.1 %» MS = 1,0-2,75) | prosa clara |
| 19 | dermatosis zinc · zinc | 50 | SACN5 cap. 32, Tabla 32-1 («100 to 200 mg/kg» MS = 25-50) | prosa clara |

**Resumen de lo que hay que revisar: 3, 6, 7, 10, 11, 13, 16.** Siete de
diecinueve. El patrón es casi siempre el mismo: **la fuente da un solo
número y yo puse el mínimo de FEDIAF como la otra punta del rango.** Eso
convierte un límite nutricional general en «hasta dónde puede apretar el
veterinario», y no es lo mismo: FEDIAF es el suelo de un perro sano, no el
suelo terapéutico de esa patología.

## 4 · Topes que no encajan en este marco

Ninguno se quedó sin margen —el BLOQUE 51 lo impide— pero tres no encajan:

- **oxalato · vitamina D** no es un tope de la patología: es el máximo legal
  de FEDIAF reproducido ahí para que se vea. Un marco de «qué mueve el
  veterinario» no debería tratarlo igual que a los demás.
- **hepatopatía · cobre** está puesto para el futuro: hoy la patología
  bloquea, así que el tope no llega a aplicarse nunca.
- **renal_avanzada** duplica el fósforo de `renal` porque **su diferencia
  clínica real es la proteína, y esa no está modelada en absoluto**. No hay
  tope de proteína en renal ni en renal_avanzada, así que las dos entradas se
  comportan igual. Esto no es un problema del margen: es un hueco del motor
  que el margen deja a la vista.

## 5 · La grasa en pancreatitis: en qué unidad está cada cifra

Pedido expreso, y con razón: **las tres cifras no están en la misma unidad.**

| Cifra | Unidad | De dónde sale exactamente |
|---|---|---|
| **20** | **g por 1000 kcal de energía metabolizable** — la misma base que usa `topes_por_1000kcal` | Merck Veterinary Manual, «Pancreatitis in Dogs and Cats», literal: «feeding a low-fat diet (ie, **less than 20 g fat/1,000 kcal**) is crucial for treatment success» |
| **≤15 %** | **materia seca** | SACN5 5ª ed., cap. 67, Tabla 67-3, fila «Fat», entrada «≤15% for non-obese and non-hypertriglyceridemic dogs». La tabla lleva la nota al pie «*Nutrients expressed on a **dry matter basis**» (`canislab-fuentes/sacn5/cap67.txt`, líneas 249-260) |
| **≤10 %** | **materia seca** | Misma tabla, fila «≤10% for obese and/or hypertriglyceridemic dogs» |

Es decir: **una está en g/1000 kcal y las otras dos en % de materia seca.**
No son comparables tal cual.

El puente que usa `patologias.json` es **4000 kcal de EM por kg de materia
seca**, que es la densidad de referencia del repo y **no viene de SACN5**.
Con ese puente: 15 % MS = 150 g/kg MS ÷ 4 = **37,5 g/1000 kcal**, y
10 % MS = **25 g/1000 kcal**.

**Ese puente es el eslabón débil, y es sensible en la dirección que
importa.** Una ración baja en grasa es MENOS densa en energía, no más:

| Densidad supuesta | 15 % MS equivale a |
|---|---|
| 3500 kcal/kg MS | 42,9 g/1000 kcal |
| **4000 kcal/kg MS (el que se usa)** | **37,5 g/1000 kcal** |
| 4500 kcal/kg MS | 33,3 g/1000 kcal |

O sea que si la ración real es menos densa que 4000, las cifras de SACN5
convertidas suben, y 20 queda **aún más estricto**. La conclusión «20 es más
estricto que 25 y que 37,5» se sostiene en la dirección que importa, **pero
los números 25 y 37,5 no son fijos: dependen de una densidad supuesta que no
está en la fuente.**

Y hay una tercera convención en juego, ya presente en el repo: **% de energía
metabolizable**. `diabetes.max_pct_kcal_grasa_si_ademas` vale 0,3 y viene de
Purina, literal «<30 % ME». A 8,5 kcal/g de grasa, para cruzar:

- 20 g/1000 kcal ≈ **17 % de la EM**
- 25 g/1000 kcal ≈ **21 % de la EM**
- 37,5 g/1000 kcal ≈ **32 % de la EM**

**Tres convenciones conviviendo — g/1000 kcal, % MS, % EM — y ninguna
escrita al lado del número.** Si este marco se extiende, lo primero es que
cada cifra lleve su unidad y su base pegadas, no heredadas.

## 6 · `renal + pancreatitis`: qué puede decir hoy el motor

**Solo que no hay solución. No sabe decir qué dos restricciones chocan.**

Medido hoy (DER 1200, 25 kg, adulto, modo automático):

| Caso | ¿Factible? |
|---|---|
| Sin patologías | sí |
| renal sola | sí |
| pancreatitis sola | sí |
| **renal + pancreatitis, 25 s** | **no** |
| **renal + pancreatitis, 120 s** | **no** |

Los 120 s importan: **no es un timeout disfrazado**, es estructural.

Lo que devuelve es el mensaje genérico: «No existe ninguna combinación de
alimentos accesibles que cumpla todos los requisitos para este perro, ni
siquiera soltando las proporciones habituales del BARF. Quita alguna
restricción y vuelve a probar.» Ese texto está escrito para un dueño y a un
veterinario no le sirve: no hay ninguna restricción que él pueda quitar.

Existe `imposible_por_aritmetica`, pero **no cubre este caso**. Salta solo
cuando (`motor/motor_completo.py`, ~línea 900) el mínimo escalado de UN
nutriente supera SU PROPIO máximo de FEDIAF, más dos casos de alimento
forzado. Es un chequeo por nutriente aislado: no puede nombrar un choque
entre dos restricciones distintas.

Para poder nombrarlo haría falta construirlo: HiGHS a través de scipy no
expone un conjunto infactible irreducible, así que la vía realista es
resolver otra vez soltando un tope cada vez y decir cuál lo desbloquea.

**Aviso para quien lo intente, que me costó dos rondas descubrirlo:** ver §7.

## 7 · Lo que sé y no está escrito en ningún fichero

Esto es lo que se pierde si no lo dejo aquí.

### La tabla de patologías está cargada DOS VECES en memoria

`motor.patologias` y `patologias` son **dos módulos distintos** para el mismo
archivo, cada uno con su propio `PATOLOGIAS`:

```
>>> import motor.patologias as A, motor_completo as MC
>>> MC.PATOLOGIAS is A.PATOLOGIAS
False
```

**Hoy tienen exactamente el mismo contenido** (comprobado: 40 claves, JSON
idéntico), así que no hay ningún fallo vivo. Pero:

- El solver usa la copia de `motor_completo` (que viene del módulo suelto
  `patologias`).
- `GET /patologias` usa `motor.patologias.cargar_crudo`.

Es la misma familia de fallo que `CLAUDE.md` describe para la tabla
duplicada del `POST /menu` borrado y para el DER, pero **en memoria en vez de
en disco**, y por eso no la ve ninguna prueba: las dos copias se construyen
del mismo JSON al importar, así que siempre coinciden... hasta que alguien
recargue o mute una.

**Consecuencia práctica inmediata:** mutar `PATOLOGIAS` en memoria para
probar «¿y si el tope fuera otro?» **no hace nada** — mutas la copia que el
solver no usa, y el experimento sale infactible dando la falsa impresión de
que el tope no era el culpable. Me pasó, y el primer resultado que saqué era
un artefacto. Hay que mutar la copia de `motor_completo`, y aun así el
verificador final puede leer de otro sitio: comprobar identidad antes de
creerse nada.

### El navegador de este contenedor no sale a internet, pero node sí

Chromium da `ERR_CONNECTION_RESET` contra rawku.app **incluso pasándole
`--proxy-server` y el CA del entorno**. `node` con `fetch` llega sin
problema. La forma de probar la app DESPLEGADA de verdad es interceptar
**todas** las peticiones en Playwright (`page.route("**/*")`) y resolverlas
desde node, dejando pasar el bundle de Vercel y la API de Render y falseando
solo Supabase con `tests/fake-supabase.js`.

Así se encontraron los dos fallos de navegación del PR #73 de la web, que
**ninguna de las 374 pruebas existentes veía**, porque todas empezaban dando
por hecho que se estaba dentro de una ficha.

**El arnés no está en el repo** — se quedó en el scratchpad de la sesión, que
muere con el contenedor. Si hace falta otra vez, hay que rehacerlo; son unas
80 líneas y lo esencial está descrito arriba.

### En `App.jsx`, el render mira `paso` antes que `fase`

Es la causa raíz recurrente, encontrada ya **tres veces** en distintas
pantallas: un `paso` viejo secuestra el render y los botones del panel
cambian el estado sin que la pantalla se mueva. Sin error, sin nada que
mirar, el botón parece muerto. Cualquier pantalla nueva del modo profesional
tiene el mismo agujero hasta que se compruebe.

### Las dos baterías de Playwright no pueden correr a la vez

Comparten los puertos 5178 y 54321 **y el `__control` del servidor falso**:
dos ejecuciones simultáneas se cambian el estado la una a la otra y salen
fallos que no existen. Me pasó y me costó un diagnóstico falso.

### Las pruebas que exigen verde sobre `resolver()` parpadean

`BLOQUE 1` y `BLOQUE 43` afirman *verde* llamando al solver **directamente**,
cuando el verde lo garantiza `_garantizar_verificado()`, no el solver — y
encima con límite de tiempo. Fallan de vez en cuando en perros pequeños con
un micronutriente rozando el mínimo. Última vez: `BLOQUE1 Adulto 3kg:
semáforo ámbar — Yodo 97`. No es una regresión: es la prueba mal apuntada.

### `renal_avanzada` no se comporta distinto de `renal`

Su diferencia clínica es la proteína y no hay ningún tope de proteína en
ninguna de las dos. Hoy son la misma patología con dos nombres.
