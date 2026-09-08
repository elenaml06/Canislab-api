# TRASPASO — sesión del 8 de septiembre

Rama: `claude/nutricion-pendiente-vuoobq`. Dos commits, **sin PR y sin
fusionar**. Escrito al pararme para que nadie tenga que deducir nada de los
mensajes de commit.

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
(`contrastar_fuentes.py`, que imprime el `value_type`). Las **14 celdas son
`TR` con la celda VACÍA**. En el esquema de BEDCA:

| código | significa |
|---|---|
| `AR` / `BE` + un número | es una **medida**, aunque el número sea 0 |
| `LZ` + un 0 | cero **lógico**: por composición no puede tener |
| `TR` + **celda vacía** | **NO HAY CIFRA**. Es un hueco |

Comprobado en Merluza (2347), Bacaladilla (2136), Lenguado (2341), Lubina
(2344), Calamar (2320), Pulpo (2471), Sepia (2635) y Merluza congelada (825).

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
- **Las 69 diferencias de `Cerebro de ternera`**: `main` tiene la ficha
  rehecha desde USDA 168622 tras el lío vaca/ternera. La rama tiene la
  versión vieja.
- **Borrar los tres cuellos y la laringe del catálogo**: `main` los conserva
  y los **bloquea en el solver** por tejido tiroideo, que es mejor — el
  alimento sigue existiendo y el motivo queda escrito.

### 🔁 Ya estaba en `main` por otro camino (no hace falta rescatarlo)

Comprobado una a una: las 103 correcciones del catálogo (albahaca fósforo
56, hígado de pollo vitA 3296 y cobre 0,492, dorada grasa 1 y vitD 1,5), el
techo legal de la vitamina D y el bloqueo de tejido tiroideo. Llegaron por
los PR #76 y #80.

**Conclusión: esa rama ya no tiene nada que rescatar.** Se puede borrar.

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
