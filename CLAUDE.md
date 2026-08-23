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
