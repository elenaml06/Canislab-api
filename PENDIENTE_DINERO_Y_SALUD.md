# Dinero y salud — lo urgente, antes de cobrar, lo que mira Stripe

Parte de `PENDIENTE.md` (secciones 1, 2 y 3), separado el 6 de septiembre.

## 1. Urgente — dinero y salud

### 1.0 `/menu/varios-perros` devolvía 1 menú en vez de 3 — ARREGLADO el 7 de septiembre

> **CERRADO.** La aritmética de abajo es correcta y sigue siéndolo, pero le
> faltaba una consecuencia: **esos 12, 6 y 4 segundos son TOPES, no costes.**
> `presupuesto_segundos` es un techo y el solver vuelve en cuanto encuentra
> solución — la propia nota lo dice sin usarlo: «la petición tarda 9-15 s de
> los 24». Lo que fallaba no era el presupuesto, era la DECISIÓN de seguir:
> `hay_tiempo_para_otra_ronda()` preguntaba «¿caben otros 10 s en el peor
> caso?» aunque la ronda anterior hubiera costado 3.
>
> Ahora se mide lo que ha costado de verdad cada ronda y se estima con eso,
> nunca siendo optimista más allá de lo observado (si la máquina va lenta,
> las rondas cuestan más, la estimación sube sola y se corta antes).
> Con el presupuesto apretado a 14 s a propósito, cinco tiradas de cada:
> **antes [2, 1, 1, 1, 2] — nunca llegaba a 3; ahora [3, 3, 2, 3, 3]**. Con
> el presupuesto normal de 24 s, 8 de 8 tiradas dan 3/3 en 7-13 s.
> Lo vigila el BLOQUE 48, que aprieta el presupuesto porque con 24 s en una
> máquina rápida las dos versiones aciertan y no probaría nada.

### 1.0 `/menu/varios-perros` devuelve a veces 1 menú en vez de 3

Encontrado el 27 de agosto **por la batería**, no por la app. La casa de
dos perros (un cachorro joven de 12 kg y una adulta de 24,5 kg) pidiendo
3 menús devolvió **1 menú para cada uno**, sin error y sin aviso.

**Está sin arreglar a propósito**, y esto es lo medido para que quien lo
retome no repita el camino:

- **No es del cambio de `valor_plausible`**: 12 tandas con él y 12 sin él,
  **0 fallos en las dos**, y la versión con él iba más rápida (9,3 s
  contra 10,5).
- **No es el tiempo global**: la petición que falló tardó **10,9 s de los
  30** que tiene antes de que Render corte.
- **NO es la rotación de proteína, y esto está medido, no supuesto.** Era
  mi hipótesis: `especies_usadas` va acumulando las especies de los menús
  anteriores, así que el segundo menú podría quedarse sin candidatos en
  una categoría con mínimo obligatorio. Escribí el arreglo (reintentar sin
  la rotación antes de rendirse, que además sería correcto por la regla 3
  de CLAUDE.md: rotar proteína es forma, no nutrición). Luego lo medí:
  **en 25 tiradas la rotación no deja infactible ni un solo menú 2**. El
  arreglo se retiró.
- **En aislado no reproduce**: 24 tandas más del caso exacto, 0 fallos, y
  0 llamadas internas infactibles instrumentando `_resolver_menu_v2_interno`.
- **28 de agosto, medido otra vez** al preguntarse si lo empeoraba la
  imputación de huecos contra los techos: **también pasa en `origin/main`
  sin ese cambio**. 13 tandas del caso exacto en cada lado, en aislado:
  `main` falló 1 (dio `[1, 1]`) y con el cambio fallaron 2 (`[1, 1]` las
  dos). Los tiempos son iguales — media 11,9 s en `main` contra 11,8 s con
  el cambio —, así que el cambio no lo ralentiza. Con 13 tandas por lado
  no se puede distinguir 1 de 2: lo que sí queda claro es que **no es de
  ese cambio**. Y el número de menús que faltan varía: en la batería
  salieron `[2, 2]`, en aislado siempre `[1, 1]`.

Apareció **dos veces, las dos con la máquina cargada**: una dentro de la
batería completa (después de diez bloques de solver) y otra en una tirada
suelta al principio de todo. Eso apunta al presupuesto de segundos **por
llamada** (`segundos_para`), no al global — y Render va más lento que la
máquina de desarrollo, así que ahí se verá antes.

**Medido y hecho a medias el 28 de agosto.** Reproducido por fin: el
mismo caso, ocho tiradas seguidas, **falla 1 de cada 6** y las demás dan
3/3. O sea que el menú 2 no es imposible — es que a veces esa tirada no
cierra.

Lo que se ha arreglado, y ninguna de las dos cosas relaja nada:

- **Reintentar antes de rendirse.** El motor lleva aleatoriedad a
  propósito (es lo que da variedad), así que la misma petición sale casi
  siempre a la segunda. Ahora reintenta hasta dos veces mientras quede
  tiempo para una ronda entera. Cada intento vuelve a pasar por
  `_garantizar_verificado`, así que no puede colar un menú que no cumpla.
- **Decirlo.** El corte por infactibilidad **no ponía**
  `menus_pedidos_no_dados`: pedías 3, recibías 1, y no había ni una
  palabra. Ahora sí, y el aviso distingue los dos motivos — decir «no
  daba tiempo» cuando lo que pasó es que no había combinación manda a la
  usuaria a esperar en vez de a soltar una restricción. Comprobados los
  dos forzando cada camino.

**Lo que sigue sin arreglar es la causa de fondo, y es el reloj.** La
petición tarda **9-15 s de los 24** que tiene, con seis solves dentro (2
perros x 3 menús). El reintento ayuda cuando el fallo es de aleatoriedad;
cuando se acaba el tiempo, lo único que cambia es que ahora se dice. Y
Render va más lento que la máquina de desarrollo, así que ahí se verá
antes.

**LA ARITMÉTICA, que nadie había hecho, y que lo cierra** (28 de agosto):

```
ronda 0:  primer menú de la base 12 s  +  amoldar al otro perro 4 s  = 16 s
ronda 1:  menú 6 s + amoldar 4 s                                     = 10 s
ronda 2:  otros                                                      = 10 s
                                                   TOTAL 36 s   presupuesto 24
```

Con dos perros y tres menús **no cabe, nunca**. Y hay algo peor: si el
primer menú gasta su rodaja entera (12 s), quedan 8 s y
`hay_tiempo_para_otra_ronda()` pide 10 — así que corta **después de la
primera ronda** y devuelve UNO. Por eso en aislado sale 3/3 (el primer
menú tarda 3-4 s, no 12) y dentro de la batería sale 1/3. Render va más
lento que la máquina de desarrollo, así que allí cae antes.

No es un fallo intermitente: es que el presupuesto y las rodajas no
cuadran entre sí, y solo se nota cuando el primer menú se acerca a su
tope.

**Lo que se exige mientras tanto**: el BLOQUE 11 ya no pide el número
exacto de menús —pedía algo imposible—, pide el contrato que sí existe:
que si salen menos, **venga el aviso** diciendo cuántos y por qué.
Recortar se puede; recortar en silencio, no. El día que se arregle la
capacidad, esa prueba vuelve a exigir el número exacto.

**Por dónde seguir**: no es «por qué falla ese menú» — es que seis solves
no caben con holgura en 24 s. Las salidas razonables son bajar el número
de menús que se piden de una vez, resolverlos en varias peticiones, o
darle a cada solve una rodaja de tiempo explícita en vez de que se la
coman los primeros.

### 1.0-bis Los 0,99 g de salmón — CERRADO el 7 de septiembre

> **CERRADO.** El diagnóstico de abajo («el mínimo por alimento solo se
> aplica a los forzados») dejó de ser cierto el 29 de agosto, cuando el
> suelo se extendió a toda la comida. Lo que quedaba abierto era otra cosa:
> el suelo se recortaba contra el techo del propio alimento
> (`suelo = min(porcion, techos[i])`), y el techo de un Extra sale de la
> **dosis del fabricante** — que en un perro diminuto puede ser de medio
> gramo. Ahí el suelo se quedaba por debajo del gramo, que es exactamente
> lo que esta restricción existe para impedir.
>
> Ahora el suelo nunca baja de 1 g, y no hace falta excluir nada a mano: con
> `gramos_i >= 1 * usa_i` y un techo menor que 1, la única solución posible
> es `usa_i = 0`, o sea que el MILP deja fuera solo al alimento del que no
> cabe ni un gramo. Comprobado que no cuesta menús: 10 de 10 en cinco
> perfiles, incluidos perros de 1 kg. El canario del BLOQUE 14 cubre ahora
> también los perros de 1 y 3 kg, que es donde asomaría.

### 1.0-bis El canario del BLOQUE 14 cantó: 0,99 g de salmón

28 de agosto. Un perro de 1,5 kg con 200 kcal y cuatro especies excluidas
recibió **0,99 g de salmón**, contra el suelo de 1,00 g de «esto se puede
pesar». Es un pelo por debajo, pero el canario está para eso.

**Dónde está el hueco:** el mínimo por alimento
(`MINIMO_POR_CATEGORIA`) solo se aplica a los alimentos **forzados**. Un
alimento que elige el solver por su cuenta solo pasa el filtro de
`> 0.02` g de la salida, así que puede salir en cualquier cantidad. Lo
que normalmente lo evita es que al solver no le compensa usar un alimento
más para poner medio gramo — pero con los doce aminoácidos activados hay
más restricciones que cerrar, y aparecen más de estos rellenos mínimos.

**Ojo con el arreglo fácil**: quitar el alimento de la salida cambia el
perfil del menú, y `_garantizar_verificado()` lo rechazaría con razón.
Redondearlo hacia arriba añade nutriente, que es seguro para un mínimo
pero puede romper un máximo. Lo correcto es un mínimo por alimento en el
solver (semicontinuo, ligado a la binaria que ya existe), no un parche en
la salida.

### 1.1 Nadie debería poder suscribirse dos veces
Encontrado el 20 de agosto probando: se crearon **seis suscripciones
activas para el mismo `user_id`** sin que nada lo impidiera. En producción
eso son seis cobros mensuales a la misma persona.

Hace falta, antes de abrir el cobro:
- Antes de crear el checkout, mirar si esa persona ya tiene una
  suscripción activa; si la tiene, mandarla al portal de cliente en vez de
  crear otra.
- Al cancelar, no poner `plan = free` a ciegas: comprobar si le queda
  alguna otra suscripción viva. Hoy una cancelación de cualquiera de las
  seis dejaría a la persona sin premium teniendo cinco pagadas.

### 1.0-ter El yodo de los perros pequeños — ARREGLADO el 7 de septiembre

> **CERRADO, y era peor de lo que decía esta nota.** El «por dónde seguir»
> de abajo acertaba de pleno: el margen no puede ser un porcentaje porque lo
> que cubre es un error ABSOLUTO. Se hizo tal cual — el suelo se pide ahora
> con el mayor de los dos, el 1,5 % de siempre o medio paso de redondeo
> (0,005 g) de la fuente más concentrada de ese nutriente.
>
> La cuenta con el yodo de un perro de 3 kg: mínimo 300 µg/1000 kcal = 90 µg,
> el 1,5 % son 1,35 µg, pero medio paso del yoduro potásico (800 µg/g) mueve
> 4 µg — tres veces el margen. En un perro de 20 kg ese mismo error es el
> 0,6 % del mínimo y el porcentaje lo cubre de sobra; por eso solo se veía
> en los pequeños. Se coge la fuente más concentrada y no la suma de todas
> porque los redondeos no van todos en la misma dirección.
>
> **Y no era estético.** Medido en 60 menús de perros de 1,5 a 4,5 kg:
>
> | | yodo mínimo | mediana | bajo 102 % | menús caídos |
> |---|---|---|---|---|
> | antes (solo %) | **82 %** | 102 % | 16 de 60 | 3 |
> | ahora | 100 % | 106 % | 2 de 60 | 0 |
>
> El 82 % es un menú que NO CUMPLE saliendo del solver. Lo paraba
> `_garantizar_verificado` —la regla 1 haciendo su trabajo— a costa de dejar
> a la usuaria sin menú. Lo vigila el BLOQUE 49.

### 1.0-ter El yodo de los perros muy pequeños vive al 101 % del mínimo

Apuntado el 28 de agosto. Es el mismo mecanismo que el caso ya conocido del
BLOQUE 1 (Toy CachorroJoven de 1,5 kg), pero **no está exento**: apareció en
`Adulto 3 kg`, y aparecerá en cualquier perfil pequeño.

**Medido**, 10 menús del caso exacto en cada árbol:

| | mín | mediana | por debajo del 105 % |
|---|---|---|---|
| `origin/main` | 101 % | 102 % | 7 de 10 |
| con la imputación de huecos | 101 % | 102 % | 7 de 10 |

O sea que **no lo causa la imputación** —la sospecha razonable era que al
imputar huecos el techo de yodo se alcanzara antes y el solver se pegara al
suelo— y tampoco lo ralentiza. La distribución es la misma.

**La causa es de diseño y está escrita en el propio motor**: el suelo se pide
con un +1,5 % de margen (`lo = mn * der / 1000 * 1.015`), así que el solver
apunta al 101,5 % y ahí se queda. Ese margen se subió de 0,8 a 1,5 % el 5 de
agosto por este mismo motivo, con el cloruro de un Toy. En un perro de 3 kg
las cantidades absolutas son tan pequeñas que el redondeo de los gramos a dos
decimales se come el margen entero.

**Por dónde seguir**: el margen no puede ser un porcentaje fijo, porque lo que
tiene que cubrir es un error ABSOLUTO (el del redondeo), y ese no escala con
el tamaño del perro. Debería ser `max(1,5 %, lo que mueve un paso de redondeo
de la fuente más concentrada de ese nutriente)`. Es un cambio en el corazón
del solver y toca los 30 requisitos a la vez, así que no se hace de pasada.

Consecuencia real mientras tanto: no es un menú inseguro —el sistema nunca
entrega nada que no esté verde— sino un «no disponible» ocasional para perros
muy pequeños.

### 1.1-bis `profiles` es una frontera de autorización y no está en el repo

Apuntado el 28 de agosto, antes de que exista el rol de veterinario, para
no descubrirlo cuando ya esté puesto.

El plan de la fase de cuentas es un campo `rol` (`tutor` | `veterinario`)
en `profiles`, del que colgará el modo clínico — el que puede bajar de los
mínimos de FEDIAF porque lo prescribe un veterinario. **Eso no es un campo
de perfil: es un permiso.** Y el front habla con Supabase con la clave
`anon` más el JWT del usuario, así que PostgREST expone `profiles` para
UPDATE a menos que una política RLS lo impida. Que la pantalla no pinte el
campo no protege nada: es la misma clase de fallo que `guardarPerro`
guardando en silencio — la capa de datos, no la pantalla.

**Y esto no es solo futuro: `plan` ya vive en esa tabla.** Si hoy no hay
política que lo impida, cualquiera con su propia sesión puede ponerse
`plan = 'premium'` sin pagar. Hoy el front solo hace `select` sobre
`profiles`, pero eso es lo que hace el front, no lo que permite la base.

**No se puede comprobar desde el repo, y ese es medio problema**: en
`canislab-web/supabase/` solo hay dos migraciones de columnas
(`migracion-menus-perro-id.sql`, `migracion-peso-objetivo.sql`). Las
políticas RLS viven únicamente en el panel de Supabase, así que **ninguna
prueba del repo las ve y ningún cambio en ellas pasa por revisión**.

Qué hacer, y en este orden:
1. **La prueba antes que la política**: un usuario con rol `tutor`
   intentando `update({rol: 'veterinario'})` sobre su propia fila tiene que
   recibir 403. Y lo mismo con `plan: 'premium'`.
2. Bajar las políticas a un `.sql` versionado, para que se puedan revisar
   y volver a aplicar.
3. Solo entonces, añadir la columna `rol`.

### 1.2 El tope de patología no se respeta ✅ Hecho el 24 de agosto

Se encontró que la grasa por patología se comparaba contra las kcal
pedidas (no las reales) y que editar un menú se saltaba los topes por
patología del todo (fósforo renal llegó a 3084 con tope 1400, y salía
verde porque el semáforo de FEDIAF no ve topes por patología). Arreglado
en tres capas y vigilado por el BLOQUE 13. Detalle completo: `HECHO.md`.

> Ojo, esto es distinto del punto 0 (qué NÚMEROS poner). Aquellos siguen
> pendientes de tu decisión; lo de aquí es que el tope, sea el que sea, se
> cumpla.

### 1.3 Comprobar que la cancelación quita el premium
Dar de alta está probado de punta a punta. Cancelar **no**. Si no funciona,
se regala la app a quien se dé de baja. (Relacionado con 1.1: hay que
probarlo con una sola suscripción activa, si no el resultado engaña.)

---

## 2. Antes de poder cobrar de verdad

- [ ] Verificar el negocio en Stripe (datos, IBAN, NIF) — ver la guía.
- [ ] Crear productos, precios y webhook en la cuenta **real**: los de
      ahora son de la sandbox, y no existen en producción.
- [ ] Quitar `STRIPE_PRUEBA` de Render cuando termine la fase de pruebas.
- [ ] Primer cobro real hecho por ti, con tu tarjeta, y reembolsado.

---

## 3. Lo que Stripe va a mirar en la web

### 3.1 Páginas legales que no existen
Comprobado el 20 de agosto: **no hay política de privacidad, ni términos y
condiciones, ni aviso legal, ni política de reembolso.** De cancelar solo
hay una frase suelta. Es de los motivos más comunes de rechazo en la
verificación, y para un negocio europeo que guarda datos personales
también es exigible por ley.

Los precios sí se ven antes de pagar, y qué vendes se entiende. Eso está.

