# Producto — funcionalidades nuevas y deuda técnica

Parte de `PENDIENTE.md` (secciones 4 y 6), separado el 6 de septiembre.

## 4. Producto — funcionalidades nuevas

Ordenadas por dependencia: multi-perro va primero porque la cesta y los
menús comparados no tienen sentido sin él.

> ⚠️ **21 de agosto, encontrado probando en producción:** la ficha del
> perro **no se guardaba entera**. `guardarPerro` leía siete campos que en
> la app no existen con ese nombre (`perfil.fechaNacimiento`,
> `perfil.castrado`, `perfil.actividad`…), así que la fecha de nacimiento,
> la esterilización, la actividad y el tamaño se guardaban vacíos, en
> silencio. Al releer, la fecha caía al valor por defecto — el mismo para
> todos los perros de la cuenta, que parece «me ha copiado la del otro».
> De la fecha sale la ETAPA y de la etapa los 30 requisitos: un perro de
> diez años volvía como cachorro. Corregido (PR web #9).
>
> **Queda por hacer a mano:** las fichas ya guardadas siguen con la fecha
> vacía. Hay que entrar en cada perro, poner su fecha de nacimiento y
> guardar, una vez.

- [x] **Multi-perro: ocho piezas hechas entre el 21 y el 24 de agosto.**
      Varios perros por cuenta, cesta de la compra por zonas de tienda y
      sin precios, burbuja de perro + engranaje en todas las pantallas,
      menús parecidos entre perros (`modo_conjunto`), el recorrido
      completo de varios perros por las mismas pantallas, la pantalla del
      menú en dos pestañas, sacar los perros del menú lateral a la
      burbuja/Ajustes, y poder usar la app sin cuenta (`localStorage` +
      migración al crear cuenta). Todas probadas y desplegadas. Detalle
      completo de cada una, con las cifras y los PR: `HECHO.md`.

- [~] **Ajustes de cuenta** (no del perro). **Hecho a medias el 24 de
      agosto**, en el engranaje: **correo** y **contraseña** ya se pueden
      cambiar desde dentro de la app. Antes no había ninguna forma: para
      cambiar la contraseña había que cerrar sesión, pedir el enlace de
      «olvidé mi contraseña» y abrir el correo.

      Ojo con el correo: Supabase manda un enlace de confirmación al
      correo NUEVO y hasta que se abre, la cuenta sigue con el viejo. La
      pantalla lo dice, porque si no parece que no ha funcionado.

      Quedan dos, y las dos por el mismo motivo:
      - **Método de pago** — es el portal de cliente de Stripe, que está
        apagado.
      - **Darse de baja** — borrar la cuenta de verdad necesita la clave
        de administrador de Supabase, o sea el backend, no la app. Y hay
        que decidir antes qué pasa con sus menús y con una suscripción
        viva.

- [ ] **Volver a encender el muro de pago cuando toque.** Está apagado
      desde el 22 de agosto para poder probar la app entera sin candados
      (web #14). No se tocó nada de Stripe: se enciende con la variable
      **`VITE_PAYWALL`** en Vercel (`on` = el de verdad con Stripe,
      `demo` = se ve y se activa sin pagar) y redesplegar. Sin tocar
      código.

      ⚠️ **Antes de encenderlo hay que reactivar dos pruebas que están
      paradas a propósito** (el motivo está escrito dentro de cada una):
      «el muro de pago nunca encierra» en `secciones-desde-perfil.spec.js`
      y «con cuenta gratis, pedir más de un menú ofrece Premium» en
      `varios-perros.spec.js`. Vigilan que el candado no deje a la usuaria
      encerrada sin poder salir sin pagar, y que la pantalla de varios
      perros no sea un agujero para saltárselo. Las dos son fallos reales
      que ya pasaron.

- [ ] **Los 34 pesos de referencia que faltan** en «cómo preparar». Cada
      alimento puede llevar una frase del tipo «una zanahoria mediana pesa
      unos 60 g», para hacerse una idea de cuánto es sin báscula. La tienen
      43 de los 77; les falta a **todas las verduras y frutas**: acelga,
      albahaca, alcachofa, apio, arándano, berenjena, boniato, borraja,
      brócoli, calabacín, calabaza, canónigos, cardo, champiñón, col
      lombarda, col rizada, coles de Bruselas, coliflor, endibia, espinaca,
      espárrago verde, frambuesa, fresa, grelo, judía verde, lechuga, nabo
      pelado, pepino, plátano, repollo, rúcula, rábano, tomate y zanahoria.

      Es un DATO, no código: cuando existan, se meten en `COMO_DAR_ALIMENTO`
      (campo `pieza`) y la línea aparece sola. Mientras no estén, no se
      pinta nada — antes se pintaba «undefined» (web #13).

- [ ] **Borrar las ramas viejas de los dos repos.** No es programación y
      no corre prisa, pero cuanto más se acumulen peor: el 21 de agosto se
      lió justo por esto (ver «Cómo se trabaja con git aquí» en
      `CLAUDE.md`).

      ⚠️ **RECUENTO CORREGIDO (8 de septiembre).** Aquí ponía «comprobado el
      23 de agosto rama por rama —15 ramas entre los dos repos, ninguna
      tiene nada que rescatar». **Aquella auditoría no estaba equivocada:
      está caducada y su alcance se lee mal.** Sus conclusiones siguen
      siendo ciertas para las 15 ramas que miró — pero once de aquellas ya
      no existen, y hoy hay **11 ramas vivas de las que SEIS son posteriores
      a esa auditoría y nunca se han mirado**, con **22 commits que no están
      en `main`**.

      Leído hoy, este punto decía «las ramas que hay están comprobadas,
      bórralas», y eso no es cierto. Un documento que manda borrar y cuya
      lista no cubre lo que hay es peor que no tenerlo, porque quien lo lee
      no tiene motivo para desconfiar.

      **Borrables (5, todas en `canislab-web`)** — las cinco son antepasadas
      de `main`, o sea que no contienen ni una línea que `main` no tenga:
      `aviso-composicion-menu`, `ficha-completa`, `multi-perro`,
      `perfil-perro-no-se-guarda`, `rawku-sentry-login-nav-ro683v`.

      **NO borrables (6), y ⚠️ CUATRO SUENAN A TRABAJO NUTRICIONAL:**
      `el-corazon-de-ternera-es-musculo` (API, 4 comm., **nutrición**),
      `nutrition-audit-data-validation-bihto9` (API, 11 comm., **nutrición**),
      `calcio-raza-grande-contrato` (web, 3 comm., **nutrición**),
      `laringe-y-trazas` (web, 2 comm., **nutrición**),
      `de-punta-a-punta-con-la-api-real` (web, 1 comm.),
      `la-ficha-clinica-pinta-los-que-cumplen` (web, 1 comm.).
      **Las cuatro de nutrición las tiene que mirar quien esté cerrando esa
      parte, no una sesión de limpieza.**

      La comprobación buena es
      `git merge-base --is-ancestor origin/claude/<rama> origin/main`.
      **`git cherry` NO vale** (compara por `patch-id` y da falsos
      positivos con los merges en squash: marcó como «no fusionada» una
      rama cuyos ficheros SÍ están en `main`). Detalle completo, con los
      títulos de los 22 commits: `TRASPASO.md` §1 y §2.

      Se borran desde github.com/elenaml06/<repo>/branches, tocando la
      papelera. Desde el contenedor no se puede (comprobado otra vez el 8 de
      septiembre, ahora lo para el clasificador de permisos).

- [ ] **Rellenar a mano la fecha de nacimiento de los perros ya guardados.**
      No es programación: las fichas creadas antes del 21 de agosto tienen
      la fecha vacía por el fallo de guardado (ver arriba). Hay que entrar
      en cada perro, ponerla y guardar. Una vez y ya.

- [x] **La compra: elegir el menú, los días bien, y marcar lo que ya
      tienes.** Pedido el 24 de agosto, hecho el 25: selector de qué menú
      ver, los días calculados por tandas (no por semana fija), y casillas
      para marcar lo comprado. PR #31 de `canislab-web`. Detalle completo:
      `HECHO.md`.

- [ ] **Una versión para dueños y otra para veterinarios.** ⚠️ **DECIDIDO
      el 28 de agosto — el plan entero, completo, está en `VETERINARIOS.md`**
      (el principio de que no degrada al tutor: su §2; el reparto de
      permisos: su §1 y §3; el formulador del veterinario: su §7; los
      pacientes en dos fases: su §9; la prescripción de la fase 4: su §10;
      la firma, que es la decisión que más obliga porque un documento
      firmado tiene que seguir diciendo lo mismo dentro de un año: su §11).
      Este punto en `PENDIENTE.md` es solo el marcador de que sigue por
      construir — para el contenido, `VETERINARIOS.md` es lo que manda, no
      esto.
- [ ] **Personalizar perro por perro** cuando son varios. Hoy lo que se
      elige se aplica a la casa entera (se le fuerza al perro que manda y
      los demás se amoldan). Elegir alimentos distintos para cada perro es
      otra pantalla, y además pelea con que los menús se parezcan — hay
      que decidir antes qué gana cuando chocan.
- [ ] **Entrar con Google.** ⚠️ **HECHO Y DESHECHO el 24 de agosto.** El
      código funcionaba y estaba probado (5 pruebas), pero se retiró porque
      **no se puede activar todavía**, y media función en producción es
      peor que ninguna: un botón que devuelve `Unsupported provider` es un
      botón roto.

      **QUÉ FALTA, Y NO ES CÓDIGO.** Google exige, para publicar la app,
      un enlace a la Política de Privacidad y otro a las Condiciones del
      Servicio en *Información de marca* — y esas páginas no existen
      todavía. Así que esto **depende de los textos legales** (ver 3.1),
      igual que Stripe. Los dos van juntos.

      Lo que ya está configurado en Google Cloud, los pasos exactos para
      cuando existan los textos legales, y el código completo que se quitó
      (para rehacerlo sin pensarlo dos veces): `PENDIENTE_DETALLE.md`.
- [ ] **Entrar con huella en el móvil.** Se hace con *passkeys* (WebAuthn).

      ⚠️ **CORREGIDO EL 24 DE AGOSTO — antes ponía aquí «que Supabase Auth
      soporta», a secas, y es verdad a medias.** Comprobado en la librería
      instalada (`@supabase/auth-js` 2.112.3): `signInWithPasskey` existe,
      pero la propia librería lo frena — *«the passkey API is experimental
      and disabled by default»* — y hay que activarlo a mano al crear el
      cliente. Además, ENTRAR con la llave está, pero **registrarla** no
      aparece entre los factores (`enroll` solo admite `totp` y `phone`),
      así que crear la llave la primera vez no está claro que se pueda con
      esta versión.

      Por eso va después de Google: Google es API estable y ahorra el paso
      donde más gente abandona; la huella es API experimental sobre una
      cuenta que ya tiene que existir, o sea comodidad para quien ya se
      registró — justo quien menos problema tiene.
- [ ] **Apartado de sugerencias.**
- [ ] **Apartado de incidencias** (problemas con el pago y demás).
- [ ] **Límite de 2 cambios de alimento por menú en la versión gratis**,
      con botón de deshacer por cambio y restaurar el menú original.


## 6. Deuda técnica y detalles

- [x] **Cantidades no medibles.** Hecho el 24 de agosto: suelo de 1 g en
      alimentos a granel de Extras (categoría real, no la clave del
      diccionario — ese fue el bug de fondo), sin redondear el resultado.
      Vigilado por el BLOQUE 16. Queda pendiente el peso del cacito de los
      productos en polvo (alga, multivitamínico) — eso sí es un DATO, ver
      `DATOS_QUE_FALTAN.md`. Detalle completo: `HECHO.md`.
- [ ] **`aviso_composicion` en la web**: ya se pinta, pero conviene ver
      cómo queda en pantalla con un perro con tres alergias.
- [ ] **El campo `tipo_de_clave_supabase` sale como `[Filtered]`** en
      Sentry: su propio filtro lo censura por llamarse «clave». Renombrarlo
      para que el diagnóstico se vea.
- [ ] **La `HTTPException` genérica del webhook sobra en Sentry**: tapa a
      la que sí explica el motivo. Mandar solo la informativa.
- [x] **`/perro/{id}/menus` devolvía menús sin verificar — ARREGLADO el 7
      de septiembre.** Era el único agujero en la regla 1 del `CLAUDE.md`
      («ningún menú sale sin verificar»), y el paréntesis de esta nota decía
      por qué no se había tapado antes: *la tabla no guarda etapa ni DER*.
      No faltaba código, faltaba el DATO — sin saber contra qué verificar, un
      menú guardado no se podía comprobar ni en principio.
      Ahora `guardar_menu` escribe el contexto JUNTO al menú (etapa, DER,
      pesos, patologías, en una columna `contexto` nueva, con migración para
      las bases que ya existían) y el endpoint lo pasa por
      `_garantizar_verificado()` al leerlo. Tres desenlaces y los tres se
      dicen: `verificado: true` con su ficha; `verificado: false` con el
      motivo **y sin los gramos** (un menú rechazado no se entrega); y
      `verificado: null` para las filas anteriores a este cambio, que no se
      pueden verificar contra nada y siguen necesitando `/menu/revalidar`.
      Lo vigila el BLOQUE 47, que planta medio kilo de pollo sin hueso y
      exige que vuelva rechazado.

