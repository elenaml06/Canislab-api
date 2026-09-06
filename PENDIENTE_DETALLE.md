# Detalle de puntos pendientes (sacado de PENDIENTE.md)

Esto no se lee solo: se abre cuando se retoma justo el punto que describe. Son
pendientes de verdad —a diferencia de `HECHO.md`, que es lo ya resuelto—, pero llevan
detrás una investigación o un código que no hace falta releer cada vez que se abre
`PENDIENTE.md` para ver qué queda. Separado el 6 de septiembre por el mismo motivo que
`HISTORIA_TECNICA.md`: `PENDIENTE.md` se lee al empezar casi cualquier sesión.

## Entrar con Google — el código que se quitó y los pasos de Google Cloud

Contexto en `PENDIENTE.md`: hecho y deshecho el 24 de agosto, bloqueado por los textos
legales (política de privacidad y condiciones de servicio, que Google exige para publicar
la app). Esto es el detalle para retomarlo sin pensarlo dos veces.

**Lo que ya está hecho en Google Cloud** (24 agosto):
- Cuenta de Google Cloud: ya existía.
- Proyecto **Rawku** creado.
- *Información de marca*: nombre de la app y correo de contacto puestos y guardados.
- Tipo de usuario: **Externo**.
- Estado: **En pruebas**. Falta publicar, por lo de los textos legales.

**Lo que faltaría cuando haya textos legales**, en orden:
1. *Información de marca*: pegar los tres enlaces (página principal, política de
   privacidad, condiciones del servicio) y añadir `rawku.app` en **Dominios
   autorizados** (si pones la página principal, Google obliga a registrar el dominio).
2. `console.cloud.google.com/auth/audience` → **Publicar app**. No hace falta
   verificación de Google: solo se piden los permisos básicos (nombre, correo, foto). La
   revisión larga es para apps que piden Gmail o Drive.
3. `console.cloud.google.com/auth/clients` → crear cliente OAuth, tipo **Aplicación
   web**. En *URI de redireccionamiento autorizados*, EXACTAMENTE:
   `https://kvtkdpgpmrvwmvymyqof.supabase.co/auth/v1/callback` (sin barra final).
   *Orígenes de JavaScript*: vacío — Google no habla con rawku.app, habla con Supabase.
4. Supabase → *Authentication → Providers → Google*: activar y pegar el ID de cliente y
   el secreto.
5. Supabase → *Authentication → URL Configuration*: **Site URL** `https://rawku.app` y
   en **Redirect URLs** `https://rawku.app/**`. **Sin esto no vuelve a la app**: Supabase
   solo obedece el `redirectTo` si la dirección está en esa lista.

**El código que se quitó**, para rehacerlo sin pensarlo dos veces (está en el historial:
rama `claude/la-compra-solo-en-el-panel`, PR web #25, deshecho en el siguiente):
- `supabase.js`: `entrarConGoogle()` con `signInWithOAuth`,
  `redirectTo: window.location.origin + '/'` y
  `queryParams: { prompt: 'select_account' }` — para que ofrezca elegir cuenta en vez
  de entrar con la última usada, que en un móvil compartido importa.
- `auth.jsx`: el botón (con el logo de Google en SVG inline, para no depender de una
  imagen externa), y un `useEffect` que lee `error_description` de la URL **y del
  hash** al volver. Ese segundo detalle no es opcional: según el flujo el motivo llega
  en uno o en otro, y mirar solo uno deja la mitad de los casos en silencio. Además
  limpiaba la URL, para que recargar no repitiera el error para siempre.
- `tests/entrar-con-google.spec.js`: 5 pruebas — el botón está donde toca y no en
  «olvidé mi contraseña»; manda a `/auth/v1/authorize` con `provider=google` y el
  `redirect_to` correcto (con esto mal la sesión se pierde sin dar ningún error); y el
  error se lee, en la query y en el hash, y no se queda pegado al recargar.

**Mientras tanto**, si se quiere probar el circuito entero sin publicar: dejarlo en
*Prueba* y añadirse como **usuario de prueba** (admite hasta 100 correos). Entra quien
esté en esa lista y nadie más — sirve para comprobar que funciona, no para abrirlo.

## Borrar las ramas viejas — auditoría rama por rama (23 de agosto)

Contexto en `PENDIENTE.md`: no es programación, no corre prisa, pero cuanto más se
acumulen peor (ver «Cómo se trabaja con git aquí» en `CLAUDE.md`). Comprobado con
`git rev-list --count origin/main..origin/<rama>`:

**En `canislab-web`** — las cuatro primeras tienen **0 commits** fuera de `main`, todo
su trabajo está fusionado: `claude/aviso-composicion-menu`, `claude/ficha-completa`,
`claude/multi-perro`, `claude/perfil-perro-no-se-guarda`.
Y `claude/rawku-sentry-login-nav-ro683v`, que **no comparte ni un commit con `main`**
(historia aparte, subida a mano, parada el 20 de agosto): son 1.927 líneas MENOS en
`App.jsx` y no tiene ni un archivo que `main` no tenga. Nada que rescatar.

**En `Canislab-api`** — diez con 0 commits fuera de `main`: `claude/auditoria-catalogo`,
`claude/auditoria-fediaf`, `claude/datos-visceras`, `claude/huecos-de-datos`,
`claude/orden-de-trabajo`, `claude/pendiente-nuevos`, `claude/pendientes-y-contexto`,
`claude/sentry-backend-integration-5qp2qa`, `claude/topes-patologia-exactos`,
`claude/una-suscripcion-por-persona`, `claude/vitamina-e-coherente`.
Y `motor`, mismo caso que la de la web: historia separada, parada el 10 de agosto,
10.500 líneas menos, ningún endpoint ni valor nutricional que `main` no tenga. Se
revisó a fondo — el único valor distinto es la energía del corazón de pollo (149 vs
los **148** verificados de `main`).

Se borran desde github.com/elenaml06/\<repo\>/branches, tocando la papelera. Desde el
contenedor no se puede: el proxy bloquea el borrado de ramas.

## BCS: por qué el dueño subestima, con las cifras (28 de agosto)

Contexto en `PENDIENTE.md`: los tres cambios de producto sobre la estimación por debajo
de BCS 5. El problema de fondo no es el mapeo de las cinco opciones, es quién puntúa:

Los dueños subestiman de forma sistemática y el sesgo se concentra justo en los perros
con sobrepeso: **Eastland-Jones 2014** (110 dueños) mide un 64 % de errores **incluso
con la carta delante**, con subestimación en el 89-92 % de ellos y hasta el 85 % en
perros con sobrepeso. **Blanchard 2023**: 100 % de desacuerdo dueño-veterinario en los
perros obesos. **Söder 2023** mide 0,6 puntos de subestimación media — pero tras una
formación corta los dueños aciertan igual que el personal veterinario (60 % → 77 %).

Los tres errores empujan en la misma dirección: el dueño subestima el BCS → el BCS bajo
da un objetivo alto → el objetivo alto da más kcal, a un perro que ya está gordo.

## Fibra: el experimento que no funcionó (25 de agosto)

Contexto en `PENDIENTE.md`: no hay mínimo de fibra porque ni FEDIAF, ni AAFCO, ni el NRC
dan uno. Esto es la medición completa de por qué enseñar la cifra hoy sería engañoso, y
por qué intentar arreglarlo con una preferencia no funcionó.

**Medido el 25 de agosto.** El mismo perro (adulto, 1100 kcal), el mismo botón, ocho
veces seguidas:

| verdura que le tocó | g fibra / 1000 kcal |
|---|---|
| Albahaca | 28,40 |
| Albahaca | 15,19 |
| Albahaca | 12,66 |
| Plátano | 2,28 |
| Acelga | 0,32 |
| Espárrago verde | 0,20 |
| Canónigos | 0,14 |
| Coles de Bruselas | 0,00 — faltaba el dato; ya puesto, 4,3 g/100 g |

De 0 a 28 al azar. No es que unos menús sean peores: al motor la fibra le da igual, así
que entre verduras que cumplen lo mismo elige por el ruido que le da variedad. Enseñar
hoy esa cifra sería enseñar una moneda al aire, y avisar cuando baje de un umbral sería
un aviso que salta más de la mitad de las veces, al azar.

**Se probó a arreglarlo y no funciona.** Se le puso al motor una preferencia por las
verduras con fibra (una preferencia, no un mínimo). Con un descuento suave: la mediana
subió a 1,19 y seguía yendo de 0,12 a 22,68. Con uno fuerte: la variedad se hundió de 8
verduras distintas a 3 (albahaca, frambuesa, arándano) y **seguía** yendo de 0,61 a
29,47. El motivo es que la fibra del menú la decide un solo ingrediente y cuántos
gramos le toquen, y eso lo deciden los requisitos, no la fibra. No hay palanca barata.
El motor se quedó como estaba.

Fuentes que trajo Cris: Schmidt et al. (2018) PLOS ONE 13(8):e0201279;
Torres-Henderson C. (2025), *The Role of Dietary Fiber in Pet Nutrition*, Today's
Veterinary Practice.
