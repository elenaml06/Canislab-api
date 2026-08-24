# Rawku — lo que queda por hacer

Lista viva. Se actualiza al terminar cada cosa, no al final.
Última revisión: 24 de agosto de 2026.

El orden **no** es por lo que parece más urgente, sino por lo que
desbloquea al resto y por lo que cuesta más caro si sale mal. Cobrar dos
veces a alguien duele más que no tener login con Google.

---

## 0. Decisiones tuyas (no son trabajo de programación)

Estas bloquean cosas de abajo. Ninguna lleva más de unos minutos, pero
las tiene que tomar una persona, no yo.

- [ ] **Límites por patología: confirmar los números.** Medido el 20 de
      agosto: los topes actuales son demasiado permisivos (cobre sale
      clavado en 3.0 con el mínimo en 2.08), pero los valores terapéuticos
      que buscabas (fósforo 1000, cobre 1.2) están **por debajo del mínimo
      de FEDIAF** y harían imposible generar menú a ningún perro renal o
      hepático. Lo más apretado que funciona de verdad:
      | | Hoy | Mín. FEDIAF | Recomendado |
      |---|---|---|---|
      | Fósforo (renal) | 1400 | 1160 | **1200** |
      | Cobre (hepatopatía) | 3.0 | 2.08 | **2.3** |
      | Grasa (pancreatitis) | 25 % | — | **18 %** (con suelo en cachorros) |
      Decidir si se aplican esos tres, o si se prefiere otra cosa.
- [ ] **¿Hace falta estar dada de alta como autónoma para cobrar?**
      Pregunta para la gestoría, antes de rellenar el tipo de negocio en
      Stripe. Bloquea la verificación del negocio.
- [ ] **Revisar los textos legales** cuando estén redactados (ver 3.1).
      El borrador lo puedo escribir yo; el visto bueno no.

---

## 1. Urgente — dinero y salud

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

### 1.2 El tope de patología no se respeta ✅ **Hecho el 24 de agosto**

Lo que decía este punto (fósforo renal a 1426 con el tope en 1400) ya
estaba arreglado el 21 de agosto. Pero al ir a comprobarlo se midieron
**todos** los caminos que entregan un menú, no solo el de generar, y
aparecieron dos cosas peores:

**1. La grasa se pasaba SIEMPRE.** Pancreatitis: tope 25 % de las kcal,
salía 26 %. Diabetes: tope 35 %, salía 36 %. En los cuatro pesos probados.
Ese camino (`max_pct_kcal_grasa`) no había recibido el arreglo del 21:
comparaba contra las kcal PEDIDAS, y el menú puede salir hasta un 3 % por
debajo. Menos kcal con la misma grasa = más porcentaje.

**2. Editar un menú se saltaba los topes DEL TODO**, que es mucho peor:

| Patología | Tope | Salía |
|---|---|---|
| renal · fósforo | 1400 | **3084** (+120 %) |
| hepatopatía · cobre | 3.0 | **4.05** |
| pancreatitis · grasa | 25 % | **47 %** |

`_recalcular_con_motor` no le pasaba las patologías al motor — el mismo
fallo que ya tuvo esa misma función con el presupuesto semanal el 5 de
agosto. El menú se generaba respetando el tope y una sola edición lo
tiraba.

**Y la verificación no lo paraba**, que es lo que lo hacía invisible:
comprueba los 30 requisitos de FEDIAF, que son los de un perro SANO.
3084 mg de fósforo entra dentro del máximo de FEDIAF, así que el semáforo
salía VERDE.

Arreglado en tres capas: la grasa contra las kcal reales, las patologías
pasadas al editar, y **la puerta de verificación comprueba ahora también
los topes por patología** (`_tope_patologia_roto`), para que si mañana
otro camino se olvida de pasarlas, el menú no salga igualmente.

Vigilado en el **BLOQUE 13** de `pruebas_completas.py`: generar, patologías
combinadas, y editar. Medido después: 0 casos por encima del tope.

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

---

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

- [x] **Varios perros por cuenta.** ✅ **Hecho el 21 de agosto** en
      `canislab-web`. Selector de perros en los dos paneles laterales,
      crear y borrar perro, y se recuerda con cuál estabas. Cambiar de
      perro **remonta** la app entera a propósito: perfil, menús y kcal se
      calculan una sola vez al montar, así que sin remontar se quedaban
      mezclados los datos de los dos. Borrar un perro borra también sus
      menús (la tabla `menus` no borra en cascada; si no, quedaban
      huérfanos para siempre). 8 pruebas nuevas en
      `tests/varios-perros.spec.js`.

      De paso: pesar al perro desde *Evolución* decía «✅ Peso
      actualizado» y **no lo guardaba nunca** — `usuario` no existía en
      esa pantalla y reventaba justo antes del guardado. Corregido.
- [x] **Cesta de la compra**, diferenciando de quién es cada cosa. ✅
      **Hecha el 24 de agosto** en `canislab-web`. Sale al final de la
      pestaña «El menú» (no en una pestaña nueva: la decisión era «el
      menú, cómo darlo y ya está») y en la pantalla de varios perros.

      Suma **la semana entera**: cada menú por SUS días. Con un perro no
      existía ninguna lista; con varios existía pero sumaba **solo el
      primer menú de cada uno** — si el segundo menú llevaba un alimento
      distinto, ese alimento no salía en la compra y te ibas a la tienda
      sin él.

      Va por zonas de tienda (carnicería / pescadería / frutería /
      despensa), porque carne, hueso, víscera e hígado son cuatro
      casillas del motor pero un solo mostrador. Y en cantidades de
      comprar, no de báscula: «2,5 kg», no «2478 g».

      El «de quién» solo aparece si hay más de un perro **y** el alimento
      no es de todos: «solo Cairo» en catorce de quince líneas taparía
      justo la que importa.

      La lógica vive en `src/cesta.js`, fuera de App.jsx, porque la usan
      dos pantallas y tener dos copias fue lo que dejó una a medias
      mientras la otra ni existía. 21 pruebas en `tests/cesta.spec.js`.

      **No lleva precios** a propósito: no los tenemos, cambian por
      tienda y semana, y una cifra inventada en una lista de la compra es
      peor que ninguna cifra.
- [x] **Menús parecidos entre perros** de la misma casa. ✅ **Motor hecho el
      21 de agosto**: `POST /menu/varios-perros`, con `modo_conjunto`
      `"parecidos"` o `"distintos"`. Manda el perro con menos margen (más
      restricciones y, a igualdad, ración más pequeña) y los demás se
      amoldan a él: al revés no cabe, forzar los 7 alimentos de un pastor
      alemán en un chihuahua de 3 kg no entra en 137 g de ración. Devuelve
      por perro qué alimentos comparte, cuáles cambian y cuántos cambios
      son. Medido: dos adultos de 24,5 y 8,2 kg salen con **0 cambios**
      (misma compra, distintas cantidades) en 1,1 s. **Ya está en la app**:
      en el generador, con más de un perro, sale «¿Para quién?» con las
      tres opciones, y la pantalla de resultados enseña qué lleva cada uno
      que los demás no y la compra de un día sumando a todos. De momento
      solo en modo automático.

      **Prueba de esfuerzo (21 agosto)**: 40 hogares al azar (2-3 perros,
      pesos de 2 a 45 kg, las 4 etapas, alergias y categorías excluidas),
      **86 menús entregados y 86 verificados en verde** de cero contra los
      30 requisitos de la etapa de cada perro. Ni uno en rojo ni en ámbar,
      ningún hogar sin menú, ningún alérgeno ni categoría excluida colada.
      Peor tiempo de un hogar: 4,2 s.

      Encontró **dos** fallos graves que llevaban meses (ver sección 5).

      Encontró de paso un fallo grave que llevaba meses: **las alergias se
      podían saltar forzando el alimento** — ver sección 5.
- [x] **Menús de varios perros: el recorrido COMPLETO.** ✅ **Hecho el 21
      de agosto** (API #23, web #11). Ya no hay camino aparte: para varios
      perros se pasa por las mismas pantallas. Qué come cada perro por
      separado, automático y personalizar, cuántos menús con su rotación,
      aviso de transición por perro, y «Ver y editar el menú de X» que
      abre el editor de siempre.

- [x] **La pantalla del menú, en dos pestañas.** ✅ **Hecho el 23 de
      agosto** en la misma rama. Era un scroll larguísimo con el plan de
      transición pegado a las tarjetas, la congelación perdida en medio de
      la pila de avisos (y con una X que la escondía para siempre), y cómo
      preparar cada alimento detrás del icono de cubiertos de su fila.
      Ahora: **El menú** (qué le doy, con el lápiz de cada alimento) y
      **Cómo darlo** (transición, congelación y preparación, todo junto).
      No se quitó nada; el icono de cubiertos de cada fila sigue estando.
      `tests/menu-dos-pestanas.spec.js`.

- [x] **Sacar los perros del menú lateral.** ✅ **Hecho el 24 de agosto**
      en `claude/burbuja-de-perfil-y-engranaje`, junto con los ajustes de
      cuenta, que iban en el mismo sitio.

      **La burbuja** va en la cabecera de todas las pantallas: dice de qué
      perro es lo que estás viendo, y al tocarla salen los perros de la
      casa y «añadir otro». Antes había dos caminos y ninguno completo —
      unas pastillas que solo aparecían en la ficha, y una fila plegada
      dentro del panel. Desde «Mis menús», por ejemplo, no se podía
      cambiar de perro sin abrir el panel; lo decía el comentario de una
      de las pruebas, y ahora esa misma prueba comprueba lo contrario.

      **El engranaje**, al lado, lleva a **Ajustes**, con las dos mitades:
      los perros (editar ficha, ir a otro, añadir, borrar) y la cuenta
      (correo, contraseña, cerrar sesión). Sin cuenta enseña «crear una
      cuenta» en vez de «cerrar sesión».

      El selector viejo del panel y las pastillas de la ficha se han
      borrado: tener tres formas de hacer lo mismo era parte del lío.

      Vigilado en `tests/ajustes.spec.js` y en `varios-perros.spec.js`,
      con una prueba que falla si los perros vuelven al panel.

      > Un rótulo por el camino: al meter la burbuja quité el «MENÚ
      > SEMANAL» / «PERFIL» de la cabecera, y dos pruebas viejas lo
      > cazaron. Tenían razón: ese rótulo dice en qué pantalla estás. Han
      > vuelto, en su propia línea, y conviven con la burbuja.

- [x] **Poder usar la app sin cuenta.** ✅ **Hecho el 23 de agosto** en
      `claude/menu-dos-pestanas-y-sin-cuenta`. La primera pantalla ofrece
      «Probar sin crear cuenta»; a partir de ahí la app entera funciona
      contra `localStorage` en vez de Supabase (`src/almacen.js`, que
      decide por dónde van los datos y explica en su cabecera **cuándo se
      da de alta el usuario** y por qué ahí).

      La cuenta se ofrece cuando ya existe algo que perder — debajo del
      primer menú, sin bloquear nada — y al crearla lo del navegador
      **sube solo** (`migrarLocalACuenta`). Sin esa parte, registrarse
      después de una semana de uso habría borrado esa semana en silencio.
      Vigilado campo por campo en `tests/sin-cuenta.spec.js`.

      Queda fuera a propósito: sin cuenta `esPremium` responde que **no**,
      para que el día que el muro se encienda «sin cuenta» no sea un
      agujero por el que colarse.

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
      `CLAUDE.md`). Comprobado el 23 de agosto rama por rama, con
      `git rev-list --count origin/main..origin/<rama>`:

      **En `canislab-web`** — las cuatro primeras tienen **0 commits**
      fuera de `main`, todo su trabajo está fusionado:
      `claude/aviso-composicion-menu`, `claude/ficha-completa`,
      `claude/multi-perro`, `claude/perfil-perro-no-se-guarda`.
      Y `claude/rawku-sentry-login-nav-ro683v`, que **no comparte ni un
      commit con `main`** (historia aparte, subida a mano, parada el 20 de
      agosto): son 1.927 líneas MENOS en `App.jsx` y no tiene ni un
      archivo que `main` no tenga. Nada que rescatar.

      **En `Canislab-api`** — diez con 0 commits fuera de `main`:
      `claude/auditoria-catalogo`, `claude/auditoria-fediaf`,
      `claude/datos-visceras`, `claude/huecos-de-datos`,
      `claude/orden-de-trabajo`, `claude/pendiente-nuevos`,
      `claude/pendientes-y-contexto`, `claude/sentry-backend-integration-5qp2qa`,
      `claude/topes-patologia-exactos`, `claude/una-suscripcion-por-persona`,
      `claude/vitamina-e-coherente`.
      Y `motor`, mismo caso que la de la web: historia separada, parada el
      10 de agosto, 10.500 líneas menos, ningún endpoint ni valor
      nutricional que `main` no tenga. Se revisó a fondo — el único valor
      distinto es la energía del corazón de pollo (149 vs los **148**
      verificados de `main`).

      Se borran desde github.com/elenaml06/<repo>/branches, tocando la
      papelera. Desde el contenedor no se puede: el proxy bloquea el
      borrado de ramas.

- [ ] **Rellenar a mano la fecha de nacimiento de los perros ya guardados.**
      No es programación: las fichas creadas antes del 21 de agosto tienen
      la fecha vacía por el fallo de guardado (ver arriba). Hay que entrar
      en cada perro, ponerla y guardar. Una vez y ya.

- [ ] **Personalizar perro por perro** cuando son varios. Hoy lo que se
      elige se aplica a la casa entera (se le fuerza al perro que manda y
      los demás se amoldan). Elegir alimentos distintos para cada perro es
      otra pantalla, y además pelea con que los menús se parezcan — hay
      que decidir antes qué gana cuando chocan.
- [ ] **Entrar con Google.**
- [ ] **Entrar con huella en el móvil.** Sí es posible: se hace con
      *passkeys* (WebAuthn), que Supabase Auth soporta. No es la huella en
      sí lo que viaja, sino una llave que el móvil guarda y desbloquea con
      ella. Depende de tener antes los ajustes de cuenta.
- [ ] **Apartado de sugerencias.**
- [ ] **Apartado de incidencias** (problemas con el pago y demás).
- [ ] **Límite de 2 cambios de alimento por menú en la versión gratis**,
      con botón de deshacer por cambio y restaurar el menú original.

---

## 5. Nutrición — auditado contra el PDF oficial

**Hecho el 21 de agosto** contra la TABLA III-3b de la *FEDIAF Nutritional
Guidelines 2025* (el PDF oficial, no de memoria). Script reproducible en
`auditar_fediaf.py`.

**161 de 161 comprobaciones cuadran exactas** — mínimos *y* máximos. Se
verificó, para los 30 nutrientes del JSON y en las tres etapas: el valor,
la unidad, y que todo esté por 1000 kcal de energía metabolizable.

Los máximos son la cara de la toxicidad y vienen de dos sitios distintos,
que es donde es fácil equivocarse: los nutricionales están en la III-3b ya
por 1000 kcal, y los legales de la UE **solo** en la III-3a, por 100 g de
materia seca — se pasan multiplicando por 2,5 (FEDIAF usa 4000 kcal/kg MS
de referencia). Ese ×2,5 no es una suposición: cuadra en los dos sitios
donde ambas tablas dan el mismo dato, vitamina A (40.000 × 2,5 = 100.000)
y vitamina D (320 × 2,5 = 800).

También se comprueba lo contrario: que el JSON **no se invente** máximos
donde FEDIAF no da ninguno. La vitamina E es uno de esos casos.

También quedó confirmado el mapeo de columnas, que no era obvio:
- `Adulto` usa la columna **95 kcal/kg^0,75**, la más exigente de las dos
  que da FEDIAF para adultos. Es la decisión conservadora, y es correcta.
- `CachorroJoven` = *Early Growth* (< 14 semanas) y reproducción.
- `CachorroCrecimiento` = *Late Growth* (≥ 14 semanas).

La vitamina E parecía discrepar (6,968 mg frente a 10,40 UI) y **no es un
error**: está convertida a 0,67 mg/UI, que es la equivalencia del
α-tocoferol natural, la forma en que las tablas de composición declaran la
vitamina E de los alimentos. Está documentado en el propio JSON.

### Respuesta a «¿usamos todos los nutrientes de FEDIAF?»

De los 44 de la tabla, el JSON cubre 30. Lo que falta:

- **Los 12 aminoácidos esenciales** (arginina, histidina, isoleucina,
  leucina, lisina, metionina, metionina+cistina, fenilalanina,
  fenilalanina+tirosina, treonina, triptófano, valina).
- Biotina (B7) y vitamina K: **FEDIAF no les pone mínimo** en esta tabla
  (aparecen con «-»), así que aquí no falta nada.

**No se pueden añadir hoy, y el motivo es el catálogo, no el motor:**
ninguno de los 163 alimentos tiene dato de aminoácidos. Añadir el
requisito sin el dato haría que todos contaran como cero y ningún menú
saldría nunca. Para hacerlo haría falta primero conseguir el perfil de
aminoácidos de los 163 alimentos.

Contexto para decidir si merece la pena: una dieta que cubre la proteína
con fuentes animales variadas cubre los aminoácidos esenciales de sobra —
por eso muchas guías prácticas se quedan en la proteína total. El caso
donde importa de verdad es una dieta con poca proteína animal.

### Vitamina E de los suplementos — resuelto el 21 de agosto

No eran UI apuntadas como mg, era más sutil: **eran mg de la forma
sintética**. En la UE los piensos declaran la vitamina E como acetato de
all-rac-α-tocoferilo, mientras que los alimentos traen α-tocoferol natural
y el requisito está en natural. Dos monedas en la misma columna, con los
suplementos contando un 49 % de más.

Confirmado con la etiqueta de NEKTON (160.000 UI de A, 20.000 UI de D3 y
2.000 **mg** de E por kg — las tres cuadran con el catálogo) y con la
equivalencia oficial de la EFSA. Convertidos los 9 multivitamínicos ×0,67.
Comprobado que los menús siguen entre 1,5 y 9 veces el mínimo.

---

## 5-bis. Huecos de datos sin declarar (encontrado el 21 de agosto)

Comprobando si los nutrientes se miden en la base correcta salió esto.
Primero lo bueno: **la base está bien**. 68 de 69 alimentos cárnicos
cuadran al contrastar su energía declarada contra sus macros por Atwater,
y ninguna verdura da un ratio imposible. Nutrientes y calorías están en la
misma base (peso fresco) en todo el catálogo, así que el cálculo «por 1000
kcal» es correcto y el agua no lo distorsiona — que era la duda.

Pero aparecieron tres alimentos con casi todo a cero **sin declararlo**:

| Alimento | Nutrientes a cero | Declarados en `sin_dato` |
|---|---|---|
| Timo de ternera | 28 de 31 | **0** |
| Testículos de cordero | 30 de 31 | **0** |
| Grasa de pollo | 28 de 31 | 6 |

Y el motor **usa el timo de ternera**: salió en 1 de 20 menús de prueba.

El campo `sin_dato` existe justo para distinguir «no lo tiene» de «no lo
sabemos», y la diferencia es asimétrica:
- En los **mínimos**, contar un hueco como cero es conservador: como mucho
  se añade un suplemento que no hacía falta.
- En los **máximos** es peligroso: se puede uno pasar de cobre o de
  vitamina A sin enterarse. Y el timo es una víscera, ricas justo en eso.

**Esto no lo puede decidir el código:** que la grasa de pollo tenga casi
todo a cero es verdad (es grasa pura), y que el timo lo tenga es un hueco.
Distinguirlo hace falta mirar la fuente.

**Hecho el 21 de agosto**, hasta donde se pudo:

- **Timo de ternera**: 16 nutrientes rellenados con la ficha USDA FDC
  170194 (la que la propia entrada ya citaba). La vitamina A sí es un cero
  real según la fuente. Los 12 que USDA no publica quedan en `sin_dato`.
- **Testículos de cordero**: 7 rellenados con la ficha USDA de *Lamb, New
  Zealand, testes, raw*, incluidas proteína y grasa, que estaban a cero
  con 68 kcal declaradas — el motor lo veía como calorías sin macros. Los
  23 restantes, en `sin_dato`.
- **Grasa de pollo**: revisado y **estaba bien**. Sus ceros son reales (la
  grasa fundida no tiene proteína ni minerales) y los huecos que sí tiene
  —ácidos grasos y vitamina E— ya estaban declarados.

Validación: tras rellenarlos, la energía declarada cuadra con los macros
por Atwater (ratio 1,01 y 1,00), lo que confirma que las cifras son
coherentes entre sí.

- [ ] **Contrastar esas cifras con la ficha original de USDA.** Se
      recuperaron de espejos por buscador porque el entorno no tiene
      acceso a `fdc.nal.usda.gov`. Dos valores de los testículos son
      **deducidos, no leídos**, y van marcados como tal: la grasa (del
      balance energético) y el selenio (del 48 % del valor diario que
      publica la fuente, porque no da la cifra absoluta).
- [ ] **El linoleico de la grasa de pollo sigue sin dato**, y esta vez no
      por descuido: USDA no publica un valor diferenciado para ese
      alimento. Importa porque el linoleico **tiene máximo** en cachorros,
      y un hueco contado como cero no lo detectaría.
- [ ] Plantearse que el aviso de datos incompletos no dependa de una lista
      mantenida a mano: un alimento con el 90 % de los valores a cero es
      sospechoso por sí solo, lo declare o no.

## 5-ter. Revisión del catálogo entero (21 de agosto)

Hecha con `auditar_catalogo.py`, que queda en el repo y se puede repetir.
Comprueba cuatro cosas que ninguna prueba del motor puede detectar, porque
el motor cumple perfectamente unos datos incompletos.

**Lo que salió bien:** la energía cuadra con los macros en los 163
alimentos. Cero incoherencias. Todo el catálogo está en la misma base
(peso fresco), que es lo que hace válido el cálculo por 1000 kcal.

**Huecos declarados** (ya aplicado): 10 alimentos tenían nutrientes a cero
sin declarar. Seis pescados con EPA y DHA a cero —incluido el **boquerón**,
que con 6,3 g de grasa es pescado azul y ese cero es falso— y cuatro
vísceras (bazo de vaca, páncreas de vaca, bazo de cordero, cerebro de
ternera). Pasan a `sin_dato` para que salte el aviso de datos incompletos.

- [ ] **Conseguir cifras verificadas de EPA/DHA para esos seis pescados.**
      No se rellenaron a ojo a propósito: los valores que devuelve el
      buscador vienen redondeados y no coinciden entre sí, y un dato
      inventado con cara de dato es peor que un hueco declarado. Contarlos
      como cero solo los infravalora (el omega-3 no tiene máximo), así que
      no es peligroso — pero desaprovecha el pescado y mete aceite que
      quizá no hacía falta.
- [ ] **Completar las cuatro vísceras** con la ficha de su fuente, igual
      que se hizo con el timo y los testículos.

### Decisión pendiente: `Laringe de vacuno`

Está en la categoría **Hueso carnoso** con **66 mg de calcio**. Los huesos
carnosos de verdad traen entre 1.250 y 1.810. No es un error de dato: la
laringe es cartílago, no hueso.

El problema es que cuenta para el 20-60 % de hueso de la ración sin
aportar el calcio que esa proporción da por supuesto. No es peligroso —el
calcio tiene mínimo duro, así que el menú lo cubre igual— pero permite
menús que parecen BARF sin serlo.

- [ ] Decidir: moverla a `Extras`, o quitarla del catálogo.

### Qué alimentos faltan, con evidencia

El cuello de botella medido, contando lo que queda al excluir especies:

| Alergias | Carne | Hueso | **Vísceras** | **Hígado** |
|---|---|---|---|---|
| 0 | 25 | 10 | 10 | 4 |
| 3 | 11 | 6 | **2** | **2** |
| 5 | 6 | 5 | **2** | **2** |

Las vísceras y el hígado son lo que deja a un perro alérgico sin menú — es
exactamente lo que medimos que bloqueaba al adulto con tres alergias. Y la
causa es la variedad de especies, no el número de alimentos:

- **Vísceras**: solo cordero, ternera y vaca. Faltan pollo, pavo, conejo,
  pato y cerdo.
- **Hígado**: solo conejo, cordero, pollo y vaca. Faltan pavo, pato, cerdo.

- [ ] Añadir vísceras e hígados de las especies que faltan. Lo más útil y
      lo más fácil de encontrar en una carnicería: **corazón y molleja de
      pollo y de pavo**, **hígado de pavo, de pato y de cerdo**, **riñón de
      cerdo**. Cada especie nueva en esas dos categorías vale más que diez
      cortes nuevos de carne muscular, que ya va sobrada.

Los pescados (20) no se ven afectados por las alergias a mamíferos, y por
eso la escalera de relajación funciona: casi siempre queda pescado.

## 5-quater. Quién consigue los datos y quién los implementa

**Regla, establecida el 21 de agosto después de saltármela.** El asistente
rellenó el timo de ternera y los testículos de cordero con valores que
había buscado él en espejos de USDA, sin poder abrir la ficha original.
Luego los marcó como «sin verificar», lo cual no arregla nada: el motor
los usa igual, así que un número dudoso pesa lo mismo que uno bueno. Solo
hay dos estados honestos: **verificado, o hueco declarado**. Se revirtió.

| Le toca al asistente | Le toca a una persona |
|---|---|
| Manipular y reestructurar lo que ya está en el JSON | **Conseguir valores de alimentos nuevos** |
| Detectar incoherencias entre alimentos | Sacarlos de BEDCA, CIQUAL o USDA |
| Comparar contra los rangos de FEDIAF | Valores de hueso: **solo Köber et al. 2017** |
| Programar la lógica que usa esos valores | Requisitos por patología: guías clínicas |

Lo que sí puede hacer el asistente con las tablas: la auditoría contra el
PDF de FEDIAF (161/161) es leer la fuente primaria que se le dio, y la
conversión de la vitamina E sale de la tabla de bioequivalencia de la
página 63 de ese mismo PDF — **d-α-tocoferol 1 mg = 1,49 UI**, de donde
1 UI = 0,671 mg. Eso es comparar contra FEDIAF, no inventar datos.

### `DATOS_QUE_FALTAN.md`

Generado por `auditar_catalogo.py`: **63 alimentos y 443 valores** por
conseguir, cada uno con su unidad y una casilla vacía. Está pensado para
llevarlo a BEDCA o CIQUAL y rellenarlo, y entonces sí pasárselo al
asistente para que lo inserte con el formato correcto.

Prioridad, por lo que desbloquea:
1. Los seis pescados con EPA/DHA sin dato — el **boquerón** el primero,
   que es pescado azul contado como si no tuviera omega-3.
2. Las seis vísceras (timo, testículos, bazo de vaca, páncreas de vaca,
   bazo de cordero, cerebro de ternera) — son la categoría que deja sin
   menú a los perros con alergias.

## 6. Deuda técnica y detalles

- [x] **Cantidades no medibles.** ✅ **Hecho el 24 de agosto**, con un
      matiz importante: medido sobre 51 menús (todos los tamaños, etapas,
      patologías y exclusiones), el problema es **más pequeño de lo que
      decía este punto y de dos tipos distintos**.

      **A granel** — salía UNA cantidad por debajo de un gramo en ~300
      alimentos medidos: 0,35 g de sal común. Arreglado en el motor con un
      suelo de 1 g: si va a usar un alimento a granel, que use una
      cantidad que quepa en una báscula, y si no le cuadra, que use otra
      cosa. **No se redondea el resultado**: cambiar los gramos después de
      resolver cambia los nutrientes, y toda la app se sostiene sobre que
      las cifras cuadran de verdad.

      El suelo va **solo en Extras**, y eso también se midió: carnes,
      vísceras y verduras nunca bajaban de ~1,9 g, así que ponerles suelo
      no arregla nada y sí cuesta — con el suelo en todo el catálogo,
      `/menu/varios-perros` pasaba de ~7 s a ~11 s con el presupuesto en
      24 s. En Render eso se puede llevar por delante un menú.

      **En polvo** — 0,15 g de alga, 0,60 g de multivitamínico. A éstos
      **no** se les puede poner suelo: sería obligar a dar de más de un
      suplemento. Se arreglan con el peso del cacito de cada producto, que
      es un DATO y está apuntado en `DATOS_QUE_FALTAN.md`.

      ⚠️ **CORREGIDO EL 24 DE AGOSTO — esto de arriba era falso.** Decía
      que «lo que sostiene la garantía es la restricción del motor, que es
      estructural». No lo era: **la fila del suelo no se añadía nunca**.
      Comparaba `categoria_de[n]` (la CLAVE del diccionario de candidatos)
      con `"Extras"`, y los aceites, la sal y las semillas entran bajo la
      clave `"Suplementos"`. Código muerto desde el primer día. Salió
      porque el BLOQUE 14 falló 1 de cada 20 veces en el caso más apretado:
      0,55 g de aceite de girasol.

      Es la **segunda** vez en ese archivo: el límite de 2 suplementos cayó
      en la misma trampa. Para la categoría de un alimento se usa
      `alimentos[n]["categoria"]`, NUNCA `categoria_de[n]`.

      Y de ahí sale el **BLOQUE 16**, que es lo que de verdad lo vigila:
      `resolver()` apunta, por cada regla, cuántas filas puso y cuántos
      coeficientes llevan, y el bloque exige que ninguna de las 16 reglas
      duras valga cero. Contar filas no bastaba — el fallo del límite de
      suplementos añade la fila **vacía**, y `0 <= 2` se cumple siempre.
      Comprobado con tres sabotajes y los tres se cazan. Si añades una
      restricción a `resolver()`, pásala por `_fila(...)` y apúntala en el
      BLOQUE 16; si no, puede morir en silencio como murieron estas dos.
- [ ] **`aviso_composicion` en la web**: ya se pinta, pero conviene ver
      cómo queda en pantalla con un perro con tres alergias.
- [ ] **El campo `tipo_de_clave_supabase` sale como `[Filtered]`** en
      Sentry: su propio filtro lo censura por llamarse «clave». Renombrarlo
      para que el diagnóstico se vea.
- [ ] **La `HTTPException` genérica del webhook sobra en Sentry**: tapa a
      la que sí explica el motivo. Mandar solo la informativa.
- [ ] **`/perro/{id}/menus` devuelve menús sin verificar** (la tabla no
      guarda etapa ni DER). Hoy no lo usa nadie, pero si se usa, hay que
      pasarlo por `/menu/revalidar` antes de enseñarlo.

---

## Hecho el 20 de agosto

- Sentry en el backend, con avisos por correo.
- Los cinco fallos del webhook de Stripe, que **no había funcionado nunca**.
- Verificación obligatoria contra los 30 requisitos en **todos** los
  caminos, incluido el cambio de etapa (`/menu/revalidar`).
- La escalera de relajación: del 23 % de fallos con alergias al 0 %, sin
  ceder en ningún límite.
- Tope de volumen y porciones que escalan con el tamaño del perro.
- Cobro de prueba completado de punta a punta y premium activado de verdad.
