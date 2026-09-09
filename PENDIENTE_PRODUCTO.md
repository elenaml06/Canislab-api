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


---

## 7. Dos cosas que dice Fascetti y que son de producto, no de nutrición

Escritas el 9 de septiembre de 2026 leyendo Fascetti & Delaney 2ª ed. entera.
Ninguna de las dos cambia un número del motor: las dos cambian **si el menú
sirve de algo una vez que sale de la pantalla**.

### 7.1 · El «diet drift»: a los pocos años, solo el 13 % sigue la receta

Fascetti, cap.15, literal:

> *«owners are likely to substitute or delete some ingredients or supplements,
> unbalancing the diet in a process referred to as **“diet drift”**… only **13%
> of dog owners** that were provided a homemade diet recommendation at a
> veterinary teaching hospital were strictly adhering to the recipe a few years
> later (Johnson et al. 2016).»*

**Trece por ciento**, y eso en pacientes de un hospital universitario, que son
los más motivados que hay. Nuestro producto es exactamente una receta casera:
todo el trabajo de cumplir los 43 requisitos vale cero si a los seis meses el
dueño ha quitado el suplemento porque se acabó y no lo ha repuesto.

Lo que se puede hacer, y no está hecho:

- **Avisar de qué se rompe si quitas algo.** El motor ya sabe decirlo: quitar un
  alimento y revalidar es `/menu/quitar` + `_garantizar_verificado()`. Falta que
  la app lo ofrezca como pregunta normal («se me ha acabado el aceite de salmón,
  ¿qué hago?») en vez de como una operación de edición.
- **Distinguir lo que se puede sustituir de lo que no.** Hoy todos los alimentos
  de un menú parecen igual de opcionales en pantalla. La verdura no lo es igual
  que el suplemento que cierra el yodo.
- **Recordar la reposición de suplementos**, que son los que se acaban y los que
  más pesan en el semáforo.

#### ⚠️ Y SACN5 lo mide por el otro lado, con más números (9 de septiembre)

Leyendo entero el **cap.3** de SACN5 —alfabetización sanitaria y cumplimiento—
aparecen las cifras del **AAHA Compliance Study**, que es el estudio más grande
que hay de esto en veterinaria. Lo que dicen, y va todo en la misma dirección
que el 13 % de Fascetti:

> «**55%** of pet owners who fed a therapeutic food also supplemented the
> recommended food with other foods or treats. **The primary reason cited by
> clients was that they didn't know not to.**»

| Dato | Cifra |
|---|---|
| Cumplimiento de dieta terapéutica, perro | **19 %** |
| Ídem contando todos los que se beneficiarían | **5-7 %** |
| Dueños que quieren instrucciones habladas **y** escritas | casi **80 %** |
| Dueños que agradecerían **varios recordatorios** | **65 %** |
| Dueños que querrían una llamada si van con retraso | **72 %** |
| Dueños que abandonaron la dieta **por precio** | **4 %** |
| Veterinarios que creen que la barrera es el precio | **60 %** |

**Tres consecuencias, y las tres son de producto:**

1. **El aviso de «no le añadas nada» es lo primero que hay que decir, no una
   nota al pie.** Aplicado el 9 de septiembre: `canislab-web` pinta un recuadro
   propio, el primero de «Cómo darlo», y lo vigila `menu-dos-pestanas.spec.js`
   comprobando también que va POR ENCIMA del de congelación — el mismo capítulo
   mide que el dueño recuerda «as little as half» de lo que se le cuenta, así
   que lo que va al final no se lee.
2. **Los recordatorios son la única palanca con evidencia.** En el estudio, el
   servicio con más cumplimiento (vacunas, 87 %) es el único para el que
   prácticamente todas las clínicas mandan recordatorio, y el 65 % de los dueños
   los pide. Eso respalda directamente el tercer punto de arriba —recordar la
   reposición de suplementos— y le pone número.
3. **El precio no es la barrera, aunque lo parezca.** Solo el 4 % abandonó por
   coste y el 60 % de los veterinarios cree que es el motivo principal. Si algún
   día se recorta una funcionalidad «porque la gente no va a pagar», este es el
   dato que dice que el problema estaba en otro sitio.

Y el capítulo trae además la medida que justifica los dibujos: el recuerdo de
instrucciones habladas pasa de **14 % a 85 %** cuando van con pictogramas (Houts
et al. 1998, p<0,0001). Eso es de la §7.2 de aquí abajo, que va justo de eso.

### 7.2 · El dueño puntúa mal la condición corporal, y de ahí sale TODO

Fascetti, cap.9, dos medidas:

> *«A study involving 201 dogs found that while the expert scored **79% of the
> dogs as overweight or obese, only 28% of the caregivers** scored their dogs
> above ideal (Singh et al. 2002).»*
>
> *«approximately 28% of the canine and feline patients were scored as
> overweight or obese, but **only 2% had weight recorded as an issue** (Lund et
> al. 1999).»*

Por qué nos importa más que a un pienso: del BCS sale el **peso objetivo**, del
peso objetivo sale el **DER**, y del DER salen **los 43 mínimos escalados**
(`minimo_de()`). Un BCS mal puesto no da error en ningún sitio: da un menú
verde para un perro que no es el tuyo. Es la familia de fallos de la sección
«Fallos que no puede encontrar la usuaria» del `CLAUDE.md`, y `radiografia.py`
existe justo para verlo por dentro.

Lo que se puede hacer:

- **Enseñar las ilustraciones de las nueve categorías** (Purina, las que
  reproduce Fascetti en las Figuras 9.1 y 9.2), no solo el número. La validación
  del sistema de 9 puntos es *con* la descripción y el dibujo, no con la cifra
  sola.
- **Preguntar por palpación, no por aspecto**: la escala se aplica tocando las
  costillas, y esa es la pregunta que distingue un 5 de un 7.
- **Y contrastar**: si el dueño dice 5 y el peso declarado está muy por encima
  del estándar de la raza, decirlo. Hoy no se dice nada.

### 7.3 · Lo que la fuente dice del crudo, y que la app no dice

Fascetti & Delaney 2ª ed., cap.8, leído entero el 9 de septiembre de 2026. Es el
capítulo que habla de BARF por su nombre, y trae cosas incómodas que **usamos
como fuente para otros números**, así que no se pueden citar solo cuando
convienen:

> *«**There is no documented evidence that feeding raw meat has any health or
> nutritional advantages over cooked foods.** The FDA **does not advocate the
> feeding of raw meat**, poultry, or seafood to pets.»*
>
> *«while many animals never become ill…, they **still pose a risk to humans and
> other animals through environmental shedding**… **Those greatest at risk are
> the very young and old, in addition to the immunocompromised.**»*
>
> *«**simple routine washing may not be enough** to eliminate potential
> food-borne pathogens in the animal companion's food bowl and environment.»*
>
> *«The use of raw bones (compared to cooked) **may reduce the risk of
> splintering and tooth fractures, but sharp fragments can still occur** and
> puncture the mucosa.»*

**Ninguna de las cuatro se puede meter en el solver**: no son números. Las
cuatro son información que quien usa la app no tiene y que le afecta a ella y a
quien viva en su casa. Dos cosas concretas, y **las dos las decides tú, no yo**,
porque son de tono de producto:

1. **Una sección de manipulación segura**, dicha una vez y bien: tabla y cuchillo
   aparte, lavar el comedero con algo más que agua, y el aviso explícito de que
   en una casa con bebés, personas mayores o alguien inmunodeprimido **el riesgo
   no es del perro, es de las personas**.
2. **El hueso**: ya avisamos de lo que no se puede pesar (BLOQUE 14), pero no del
   riesgo de fragmento. El propio texto reconoce que el crudo es mejor que el
   cocido en esto — es la única ventaja documentada que le concede, y decirlo así
   es más creíble que no decir nada.

Y la parte que juega a nuestro favor, que también hay que decir: de 200 recetas
caseras publicadas, **190 tenían al menos un nutriente esencial por debajo** del
mínimo de NRC o AAFCO y 167 tenían varios; de las cinco dietas crudas analizadas
(dos comerciales y tres caseras), **las cinco** tenían nutrientes por debajo del
mínimo, y las caseras además vitamina D y E altas y el Ca:P mal. **Eso es
exactamente lo que este motor comprueba en cada menú antes de entregarlo.** El
argumento de venta no es «BARF es mejor»: es «este BARF está calculado y
verificado, y el 95 % de las recetas que hay por ahí no lo están».

---

## Siete patologías digestivas y esofágicas que la fuente declara y no ofrecemos (9 de septiembre de 2026)

**Decisión de producto, no de fuentes** (`CERRADO.md`: «añadir una patología es
decisión de producto»). Salen de leer enteros los capítulos de SACN5 que no
tenían ni una cita en el repo, y **están todas transcritas y convertidas** en
`HALLAZGOS_LECTURA_FUENTES.md`. Lo que falta es decidir si se ofrecen.

### Las cinco digestivas comparten un núcleo, así que son una decisión y no cinco

Gastritis y úlcera (52-2), motilidad gástrica (54-2), gastroenteritis aguda
(56-2), intestino corto (59-1) y colitis (62-1). Cuatro de las cinco piden los
mismos tres **suelos** de electrolitos, y SACN5 lo dice explícitamente: por
encima de los mínimos del perro sano.

| | Por 1000 kcal | Mínimo de FEDIAF |
|---|---|---|
| Potasio | 2000-2750 mg | 1450 |
| Cloruro | 1250-3250 mg | 430 |
| Sodio | 750-1250 mg | 290 |

Más grasa ≤37,5 g/1000 kcal y fibra ≤12,5 g (enfoque muy digestible) o ≥17,5 g
(enfoque enriquecido en fibra).

**Lo que hay que decidir:** si se ofrecen como cinco patologías separadas, como
una sola («apoyo digestivo») con variantes, o ninguna. Y quién las marca: son
diagnósticos, no observaciones del dueño.

### Las dos esofágicas van en direcciones opuestas

Disfagia obstructiva (50-3) pide grasa **≥62,5 g**/1000 kcal; esofagitis y
reflujo (50-4) la pide **≤37,5 g**. La fuente explica el porqué: la grasa alta
retrasa el vaciamiento gástrico y baja la presión del esfínter esofágico, o sea
favorece el reflujo. Las dos suben la proteína a ≥62,5 g, y también con motivo:
la proteína sube la presión de ese esfínter.

**Ninguna de las dos se puede marcar sin diagnóstico.**

---

## Sugerir patologías por raza (9 de septiembre de 2026)

Los capítulos 49, 51 y 61 de SACN5 traen **tablas de trastornos asociados a
raza**, y la app ya sabe la raza (la usa para el DER).

| Trastorno | Razas |
|---|---|
| Dilatación-vólvulo gástrico | basset hound, dóberman, setter gordon, gran danés, setter irlandés, san bernardo, weimaraner |
| Colitis ulcerativa | bóxer, bulldog francés |
| Gastroenteritis hemorrágica | teckel, schnauzer miniatura, caniche toy |
| Neoplasia oral | cocker, pastor alemán, braco alemán de pelo corto, golden retriever, weimaraner |

Rawku **ya tiene `riesgo_gdv`** con un aviso muy completo, pero **lo tiene que
marcar el dueño**, y el dueño de un gran danés no tiene por qué saber que existe.

**Lo que se propone:** que la app lo **sugiera** —nunca que lo marque sola— a las
razas que la fuente nombra. «Tu raza está en la lista de riesgo de X: ¿lo
marcamos?». Es un cambio de pantalla, no de motor.

### ⚠️ Y AHORA HAY DOS TABLAS MÁS, DE PATOLOGÍAS QUE EL MOTOR YA APLICA

Añadidas el mismo día, de leer enteros los capítulos 38 y 55.

**Tabla 38-11** (urolitos) es la más valiosa de las tres, porque **las seis
patologías de urolito ya existen en `patologias.json`** — aquí no hay que
construir nada nuevo en el motor, solo la pregunta:

| Piedra | Razas | Sexo | Edad típica |
|---|---|---|---|
| Estruvita | schnauzer miniatura, caniche miniatura, bichón frisé, cocker spaniel | hembras (>80 %) | 2-9 años |
| Oxalato cálcico | schnauzer miniatura y estándar, lhasa apso, yorkshire, caniche miniatura, shih tzu, bichón frisé | machos (>70 %) | 5-12 años |
| Urato | **dálmata**, bulldog inglés, schnauzer miniatura, yorkshire, shih tzu | machos (>90 %) | 1-5 años |
| Fosfato cálcico | yorkshire, schnauzer miniatura, shih tzu | machos (>55 %) | <1 año y 6-10 |
| Cistina | bulldog inglés, teckel, basset hound, terranova | machos (>98 %) | 1-7 años |
| Sílice | pastor alemán, golden retriever, labrador, schnauzer miniatura, cavalier | machos (95 %) | 3-10 años |

**Tabla 55-3** (intestino delgado): gastroenteritis eosinofílica (pastor alemán,
setter irlandés), enteritis linfoplasmocítica (pastor alemán, shar-pei,
soft-coated wheaten terrier), sobrecrecimiento bacteriano (pastor alemán,
beagle), linfangiectasia (yorkshire, golden, teckel, basenji), enteropatía
sensible al trigo (setter irlandés).

**Y la app tiene además el sexo y la edad**, que estas tablas también dan. Una
sugerencia que cruza raza, sexo y edad acierta mucho más que una que solo mira la
raza: el dálmata macho joven es el 90 % de los uratos.

⚠️ **El límite sigue siendo el mismo, y es lo importante**: una predisposición de
raza **no es un diagnóstico**. Marcarla sola sería decidir por criterio clínico
sin que nadie lo haya pedido, y eso no lo hace ni el motor ni la app. Se sugiere
la pregunta, la marca la persona.

Detalle y citas literales: `HALLAZGOS_LECTURA_FUENTES.md`, capítulos 38 y 55.

---

## ⚠️ Los ocho `avisos_extra` de patología no los pinta nadie (9 de septiembre de 2026)

**Medido hoy**, contando el JSON y buscando en el front:

| | |
|---|---|
| Avisos `avisos_extra` en `patologias.json` | **8**, en 4 patologías |
| Sitios de `canislab-web` que los pintan | **0** |

Los ocho son: `epilepsia_idiopatica` (hipertrigliceridemia, y el nuevo
`bromuro_y_cloro`), `cushing` (`mitotano_con_comida`), `cancer_soporte` (dos) y
`reaccion_adversa_alimento` (tres: una o dos proteínas, fase de diagnóstico,
aminas vasoactivas).

**La API sí los sirve**, y por dos caminos: `patologias.py` los mete en la
respuesta del menú y `GET /patologias` los sirve al elegir la patología, que es
lo que se construyó el 8 de septiembre justamente para que quien firma una pauta
los leyera antes de decidir. Lo que no existe es el sitio donde se ven.

Lo que el dueño ve hoy con cualquier patología marcada es **un solo aviso
genérico**: «Este menú TIENE que aprobarlo tu veterinario … enséñale este menú
antes de empezar». Es correcto y no basta: los ocho dicen cosas que ese texto no
dice.

**Por qué esto importa más desde hoy.** Los dos avisos nuevos son de FÁRMACO, y
los dos describen algo que pasa **por culpa del cambio de dieta que hace esta
app**:

- Un perro con bromuro potásico que pasa a esta ración baja su carga de cloro a
  la mitad, y el bromo sérico sube. Hay que medirlo.
- Un perro con mitotano tiene que tomar la pastilla **con** la comida: en ayunas
  la absorción cae de 13,0 a 0,4 mg/l.

Un aviso que vive en un JSON y no llega a ninguna pantalla es, para quien usa la
app, un aviso que no existe. Es la misma familia que el `null` puesto a mano en
la pantalla de varios perros, y la misma que el fallo de `guardarPerro`: nada da
error, nada se ve, y solo aparece usándolo.

**Lo que hace falta**, y es de pantalla, no de motor:
1. Que `VistaMenus` pinte `avisos_extra` debajo del aviso genérico de patología,
   uno por línea.
2. Que la pantalla de elegir patologías pinte los de `GET /patologias` **antes**
   de marcar, que es cuando se decide.
3. Un test como los de `ficha-ida-y-vuelta`: marcar una patología que tenga
   `avisos_extra` y exigir que su texto esté en pantalla. Sin él vuelve a
   perderse en el siguiente refactor.

Fuente de los dos nuevos: SACN5 5ª ed., cap.69, casos 69-1 y 69-2. Detalle en
`HALLAZGOS_LECTURA_FUENTES.md`.

---

## La app no dice que un perro que come crudo EXCRETA más patógenos (9 de septiembre de 2026)

**De leer entero el capítulo 56 de SACN5.** Literal: *«**Dogs consuming such
foods shed bacterial pathogens at a much higher rate than those consuming
conventionally cooked commercial foods**» (Weese and Armstrong, 2006)*, y los
patógenos cultivados en comida cruda casera y comercial: *Salmonella*,
*Campylobacter*, *Escherichia*, *Yersinia* (Weese, 2006; Strohmeyer et al, 2006).

**Lo que Rawku dice hoy, comprobado:**

| Dónde | Qué dice |
|---|---|
| `instrucciones.js` (panel de Congelación) | Tiempos: una semana, dos el pescado, tres días descongelado |
| `instrucciones.js` (Pescados y mariscos) | Qué va crudo y qué cocinado, y por qué |
| `patologias.json` → `inmunosupresion` | El riesgo de patógenos **para el perro** con las defensas bajas |

O sea: **manipulación del alimento, sí; higiene de la casa, en ninguna parte**.
Y son dos cosas distintas. Congelar bien protege al perro de los parásitos; no
impide que el perro excrete salmonela y que la toque un niño de dos años.

**Lo que se propone**, y es de texto, no de motor:
1. Una línea en el panel que ya existe: lavarse las manos después de dar de
   comer y de recoger las heces, limpiar el cuenco y la superficie, y no dejar
   que el perro lama la cara a nadie del grupo sensible justo después de comer.
2. **Y un aviso propio si en casa hay alguien de riesgo** — niños pequeños,
   embarazadas, mayores, personas inmunodeprimidas. La app no pregunta eso hoy.
   Es una pregunta de una casilla y cambia lo que hay que decir.

⚠️ **Esto no es un argumento contra el crudo ni cambia ningún menú.** Es
información que la fuente da, que quien elige alimentar así tiene derecho a
tener, y que hoy no está.

Cita completa y contexto: `HALLAZGOS_LECTURA_FUENTES.md`, capítulo 56.
