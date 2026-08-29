# Rawku — lo que queda por hacer

Lista viva. Se actualiza al terminar cada cosa, no al final.
Última revisión: 28 de agosto de 2026.

El orden **no** es por lo que parece más urgente, sino por lo que
desbloquea al resto y por lo que cuesta más caro si sale mal. Cobrar dos
veces a alguien duele más que no tener login con Google.

---

## 0. Decisiones tuyas (no son trabajo de programación)

Estas bloquean cosas de abajo. Ninguna lleva más de unos minutos, pero
las tiene que tomar una persona, no yo.

- [ ] **EJECUTAR EL SQL DE LA FASE 0 EN SUPABASE.** Está fusionado y
      desplegado desde el 28 de agosto, pero **el código no puede
      ejecutarlo solo**: crear columnas y disparadores es DDL, y eso no
      pasa por la API de Supabase — necesita el SQL Editor o la contraseña
      de la base de datos. Hasta que se ejecute, nadie es profesional (que
      es lo correcto) y **no se puede probar nada de la fase 1** contra
      Supabase de verdad.

      1. Supabase → SQL Editor → pegar `supabase/migracion-rol-profesional
         .sql` (repo `canislab-web`) → Run. Es idempotente.
      2. Acreditarse a una misma: `update public.profiles set rol =
         'profesional', rol_verificado_en = now() where id = '<tu uuid>';`
         El uuid está en Authentication → Users.
      3. **Y la comprobación que de verdad importa**, que no se puede hacer
         desde el SQL Editor porque allí eres `service_role` y el
         disparador te deja pasar a propósito: entrar en rawku.app con una
         cuenta normal, abrir la consola del navegador y probar a
         ascenderse. **Tiene que dar error.** Si dice ok, el disparador no
         protege nada y no se puede seguir con el resto del plan. El
         comando exacto está al final del archivo .sql.

- [ ] **La lista de las nueve `formulable: false`.** La necesita la fase 4:
      es la que define qué diagnósticos exigen firma de un veterinario,
      porque son los que piden bajar de los mínimos de FEDIAF. **No está en
      ninguno de los dos repositorios** — comprobado el 28 de agosto, cero
      apariciones de `formulable` en `Canislab-api` y en `canislab-web`.
      Viene de otro sitio y hay que traerla aquí antes de construir nada de
      la fase 4.

- [x] ~~**El peso ideal desde el BCS estaba calculado de dos formas.**~~
      **RESUELTO el 29 de agosto, y al revés de como lo escribí el 28.**

      El 28 puse que había que RESTAR el exceso, apoyado en el ejemplo
      trabajado de AAHA («labrador de 45 kg con BCS 8 → aproximadamente
      32 kg»). Estaba mal, y el error era mío por leer una frase sin abrir
      la tabla que tiene al lado: **«30 % overweight» es un 30 % SOBRE EL
      IDEAL**, así que se invierte dividiendo. Tres cosas lo cierran:

      1. La **Tabla 1 de la propia guía** da un tercer método que no
         depende de cómo se lea «overweight» porque sale de la masa magra:
         `[peso × (100 − %grasa)] / 0,8`. Da ×0,7875 en BCS 8. Dividiendo
         sale ×0,7692 —un 2 % de diferencia—; restando, ×0,70, que se sale
         del propio rango del método desde BCS 7.
      2. La **Global Pet Obesity Initiative (2019)**, respaldada por ECVCN,
         WSAVA y ACVIM, define obesidad como «30 % above ideal body
         weight». *Above ideal* no admite dos lecturas.
      3. **El ejemplo de AAHA es el raro de su propio documento**: dos de
         sus tres métodos dan 34-35 kg para ese labrador. Es una errata.

      Así que **`der.py` y `App.jsx` estaban bien desde el principio** y el
      que estaba mal era `verificar.peso_objetivo_desde_bcs`, que ya
      divide. Las kcal de los 85 casos del contrato **no se han movido**.

      Y como no había ni una prueba que tocara esa función —por eso se
      coló—, ahora está el **BLOQUE 37**, que ancla los cuatro puntos
      contra el método de la grasa corporal y, sobre todo, **compara las
      dos cuentas entre sí**: es lo que el contrato del DER no puede hacer.

- [ ] **Tres cambios de producto que salen de lo anterior, y que sí mueven
      las kcal de perros reales.** No los he hecho porque cambian lo que
      come un perro que ya está usando la app, y eso se decide, no se
      cuela en un merge.

      1. **Por debajo de BCS 5 no habría que estimar.** Hoy `der.py` y
         `App.jsx` sí estiman hacia arriba (con un tope del +20 %).
         La Tabla 1 de AAHA **empieza en BCS 4 y no tiene columna de
         «% underweight»**, y AAHA 2021 dice lo contrario de estimar:
         *«base feeding calculations on current weight if ideal or
         underweight»*. Un perro delgado dispara un diagnóstico, no un
         plan de engorde. `verificar.py` ya se comporta así; los otros dos
         no.
      2. **BCS 4 es «Ideal» en esa tabla** (15-19 % de grasa), no
         «delgado». Si la segunda opción de la app dice «un poco delgado»
         y mapea a 4, marcamos como subóptimo un perro que las guías
         consideran ideal.
      3. **El mapeo de las cinco opciones.** Hoy es `{0:2, 1:4, 2:5, 3:7,
         4:9}`: saltos de 2, 1, 2, 2 —no equidistantes, lo que rompe la
         premisa del «10 % por punto»—. El estándar es **1, 3, 5, 7, 9**.

      **Y el problema de fondo no es el mapeo, es quién puntúa.** Los
      dueños subestiman de forma sistemática y el sesgo se concentra justo
      en los perros con sobrepeso: Eastland-Jones 2014 (110 dueños) mide
      un 64 % de errores **incluso con la carta delante**, con
      subestimación en el 89-92 % de ellos y hasta el 85 % en perros con
      sobrepeso. Blanchard 2023: **100 % de desacuerdo dueño-veterinario
      en los perros obesos**. Söder 2023 mide 0,6 puntos de subestimación
      media —pero tras una formación corta los dueños aciertan igual que
      el personal veterinario (60 % → 77 %).

      Los tres errores empujan en la misma dirección: **el dueño
      subestima el BCS → el BCS bajo da un objetivo alto → el objetivo
      alto da más kcal**, a un perro que ya está gordo.

- [ ] **Cuatro fichas que ha señalado la comprobación nueva del cociente.**
      (28 de agosto.) Al añadir el nivel 2 —mirar la columna en vez de la
      fila— salieron cuatro que ninguna comprobación anterior veía. **No son
      errores probados: son fichas que hay que mirar en su fuente.** Yo no
      puedo inventar el valor bueno.

      | ficha | qué sale | cómo de sospechoso |
      |---|---|---|
      | **Pulmón de cordero** | Leu/Ile **2,537**, isoleucina al 3,16 % | Es la firma exacta del pavo contaminado del USDA. El más sospechoso |
      | **Calamar** | valina = isoleucina, 0,680 | Los tres cefalópodos tienen Val = Ile exacto |
      | **Pulpo** | valina = isoleucina, 0,651 | pero **NO son el mismo perfil reescalado** — sus AA/proteína difieren |
      | **Sepia** | valina = isoleucina, 0,709 | así que puede ser real: en cefalópodos Val ≈ Ile. Hay que ver la fuente |

      Los tres cefalópodos pueden ser un redondeo legítimo. El pulmón no lo
      parece.

- [ ] **El máximo de lisina de FEDIAF: ¿sobre qué proteína se mide?**
      (28 de agosto, para el nutricionista.) La Tabla III-3b pone un solo
      máximo a un aminoácido: **lisina 7,00 g/1000 kcal, y solo en
      crecimiento**. Está bien transcrito — `auditar_fediaf.py` lo
      comprueba contra el PDF.

      Al encender los doce aminoácidos se midió qué pasaba con él:
      **0 de 15 menús de cachorro caben debajo**, salen entre 8,79 y
      12,12. No es que se pase alguno raro: es que ninguna ración BARF de
      cachorro cabe. Y el motivo se ve en la ración: esos menús llevan
      unos **134 g de proteína por 1000 kcal, y el mínimo de FEDIAF para
      un cachorro son 50**. Una dieta de carne cruda tiene dos veces y
      media la proteína de referencia, y la lisina va detrás.

      **Mientras tanto ese techo NO se aplica** — es el único máximo de
      FEDIAF que no se aplica en todo el sistema. El mínimo de lisina sí.
      El dato se queda en la tabla: dejar de aplicar un número no es lo
      mismo que decir que FEDIAF no lo pide. Lo vigila el BLOQUE 27 por
      tres lados.

      La pregunta es una sola: **¿el 7,00 se mide sobre la proteína de
      referencia de la tabla, o sobre la del plato?**
      · Si es lo primero, no aplicarlo es correcto y esto se cierra.
      · Si es lo segundo, una dieta BARF de cachorro se pasa de lisina
        **por definición**, y eso es una conversación mucho más grande
        que este apartado.

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
- [ ] **Siete preguntas para Michelle.** Las cinco primeras salieron del
      repaso clínico del 25 de agosto; la sexta y la séptima, del trabajo
      del 28 sobre la parte para veterinarios. Ninguna se puede programar sin criterio
      veterinario, y la sexta ni siquiera se puede preguntar sin ser
      colegiado:

- [ ] **Cinco preguntas de la revisión clínica.** Salieron del repaso del
      25 de agosto y ninguna se puede programar sin criterio veterinario.
      ⚠️ La nutricionista ya no es Michelle: es Chris. Las cinco van en
      `Rawku_para_Chris.pdf` (28 de agosto), repartidas entre las
      preguntas 5, 8 y 9:

      1. **¿Qué mínimo de proteína para un senior?** Hoy la app usa la
         columna de adulto de FEDIAF (52,10 g/1000 kcal). Shmalberg (DACVN)
         sugiere ≥75 g. Es un cambio grande: afectaría a todos los seniors.
      2. **¿Distinguir el estadio ACVIM en cardiopatía (B2/C/D)?** Hoy hay
         un solo valor de sodio (900 mg/1000 kcal), que es el de B2 -- el
         menos restrictivo. Para C harían falta 500-790 y para D menos de
         500, pero la app no pregunta el estadio.
      3. **Cachorro con pancreatitis: ¿solo aviso, o bloquear?** Hoy avisa
         y genera el menú sin bajar la grasa, porque el mínimo de grasa que
         necesita para crecer (21,25 g) es mayor que el tope terapéutico
         (20 g).
      4. **¿El umbral 1,10 para pasar de dieta de bajada a mantenimiento es
         el correcto?** Es donde la ración pega el salto de 263 a 413 kcal.
      5. **¿El 10 % de tiaminasa es adecuado?** Es criterio nuestro, no de
         ninguna fuente.
      6. **¿Qué tiene que decir una pauta firmada, y de qué responde quien
         la firma?** Añadida el 28 de agosto, al decidir que la pauta sale
         con el nombre del veterinario y su número de colegiado (ver
         `VETERINARIOS.md`). Si firma la pauta, si firma haberla revisado,
         qué papel tiene Rawku en medio. **Esta se pregunta en el Colegio
         Oficial de Veterinarios de su provincia**, y la tiene que
         preguntar ella: a un colegio no se puede consultar sin ser
         colegiado. No bloquea construir nada — solo cambia el texto del
         documento —, pero sí bloquea que salga la primera pauta firmada
         de verdad.

      7. **¿Qué hace exactamente AnVet, y cuánto cuesta?** Añadida el 28
         de agosto. AnVet es el software con el que formulan los
         veterinarios salidos del Máster de Alimentación Natural y
         Nutrición Veterinaria Funcional de Biovet — o sea que no lo
         eligieron comparando productos: **les vino con la formación**, que
         es un enganche mucho más fuerte. Lo que hace falta saber, y ella
         probablemente lo tiene o lo conoce del máster: **¿calcula las
         cantidades de cada ingrediente o las teclea el veterinario a
         mano?** (todos los demás que hemos mirado —MyVetDiet, Animal Diet
         Formulator, Pet Diet Designer, BalanceIT— las teclea el usuario),
         qué estándar usa (FEDIAF, NRC o AAFCO), y el precio. De esa
         respuesta depende si el solver de Rawku es una ventaja enorme o
         solo una ventaja.

- [ ] **La app no distingue "hepatopatía por cobre" de otras hepatopatías.**
      Desde el 25 de agosto, marcar hepatopatía BLOQUEA la generación,
      porque la restricción de cobre que hace falta en la hepatopatía por
      acúmulo (1,2 mg/1000 kcal) está por debajo del mínimo que FEDIAF
      exige a cualquier perro (2,08). Eso es correcto para esa hepatopatía
      -- pero la lista de la app tiene una sola opción, así que ahora
      también bloquea a un perro con otra enfermedad hepática que quizá sí
      podría comer un menú normal. Si Chris dice que merece la pena,
      hay que partir la opción en dos. El tope de 2,4 mg ya está puesto en
      el código esperando ese día.

      ⚠️ **Y esto conecta con la parte para veterinarios** (28 de agosto):
      uno de los tres poderes que solo tiene el profesional es justamente
      **levantar un bloqueo asumiendo la responsabilidad** — «formula con
      cobre ≤ 1,2, respondo yo». O sea que partir la opción en dos deja de
      ser la única salida: la otra es que un veterinario acreditado pueda
      desbloquearlo caso a caso. Las dos cosas son compatibles y no se
      estorban.

- [ ] **`EPA_DHA_total` se comprueba solo contra el EPA, sin sumarle el
      DHA.** Encontrado el 25 de agosto. El requisito se llama EPA+DHA y en

- [x] **HECHO (25 agosto). `EPA_DHA_total` ya suma las dos claves.** Se
      resolvió con claves DERIVADAS en `valor_nutriente` — el mismo
      mecanismo que el 28 de agosto sirvió para `metionina_cistina` y
      `fenilalanina_tirosina`. Comprobado: epa 0,5 + dha 0,3 = 0,8. Se
      deja escrito el apunte porque la nota decía «hoy solo puede apuntar
      a una clave», y eso ya no es verdad.

      <s>`EPA_DHA_total` se comprueba solo contra el EPA, sin sumarle el
      DHA.</s> Encontrado el 25 de agosto. El requisito se llama EPA+DHA y en
      `verificar.MAPA` apunta a la clave `epa` a secas, así que el DHA no
      cuenta. Va en la dirección segura (se exige más de lo que se pide) y
      hoy los menús lo cumplen de sobra igual -- medido, 145 mg/1000 kcal
      de EPA solo, contra un mínimo de 110 -- pero el nombre dice una cosa
      y el código comprueba otra, y eso siempre acaba mal. Arreglarlo es
      dejar que un requisito apunte a la SUMA de dos claves; hoy solo puede
      apuntar a una.

- [ ] **Repasar la transcripción de la tabla de FEDIAF.** En
      `auditar_fediaf.py` la tabla III-3b está escrita a mano. La auditoría
      compara el JSON contra ESA transcripción: si un número se tecleó mal
      en los dos sitios igual, cuadra y nadie lo ve. Es leer las columnas
      contra el PDF una vez, y ya queda cerrado. Nació el 25 de agosto,
      cuando apareció una fila (`Fibra`) que no era de FEDIAF y la
      auditoría la daba por buena. Ver el recuadro del apartado 5.

- [ ] **Auditar los valores de los ALIMENTOS.** `requerimientos_v2_final
      .json` tiene auditoría contra el PDF; `alimentos_v3_final.json` no
      tiene ninguna. Un valor mal en la composición de un alimento tuerce
      todos los menús que lo lleven y ninguna prueba lo vería. Las fuentes
      son BEDCA, CIQUAL y USDA, y el hueso solo Köber et al. 2017.

- [ ] **Fibra de la borraja.** De las tres verduras a las que les faltaba
      el dato, ella trajo dos de BEDCA el 25 de agosto y ya están puestas:
      coles de Bruselas 4,3 g/100 g y tomate en puré 2,8 (el tomate fresco
      es otra ficha distinta, 1,1 — el nuestro es el puré). Queda la
      borraja, que además tiene un `0.0` explícito, que es peor que no
      tener el dato: dice «no lleva fibra» y no es verdad.

      El hueco no era inocuo: en la medición del 25 de agosto, uno de cada
      ocho menús salió con «0,00 g de fibra» **porque le tocaron las coles
      de Bruselas**. Una verdura de verdad leída como si no llevara nada.

- [ ] **¿Rawku apunta a algún rango de fibra? — pregunta 7 del PDF de Chris.**
      Ni FEDIAF, ni AAFCO, ni el NRC dan un mínimo: la fibra no es un
      nutriente esencial y no tiene valor de referencia oficial. Así que
      no se puede poner un mínimo duro sin dejar sin menú a perros con
      patologías que limitan verduras o que necesitan fibra baja.

      **Lo que sí sabemos, medido el 25 de agosto.** El mismo perro
      (adulto, 1100 kcal), el mismo botón, ocho veces seguidas:

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

      De 0 a 28 al azar. No es que unos menús sean peores: al motor la
      fibra le da igual, así que entre verduras que cumplen lo mismo elige
      por el ruido que le da variedad. **Enseñar hoy esa cifra sería
      enseñar una moneda al aire, y avisar cuando baje de un umbral sería
      un aviso que salta más de la mitad de las veces, al azar.**

      **Se probó a arreglarlo y no funciona.** Se le puso al motor una
      preferencia por las verduras con fibra (una preferencia, no un
      mínimo). Con un descuento suave: la mediana subió a 1,19 y seguía
      yendo de 0,12 a 22,68. Con uno fuerte: la variedad se hundió de 8
      verduras distintas a 3 (albahaca, frambuesa, arándano) y **seguía**
      yendo de 0,61 a 29,47. El motivo es que la fibra del menú la decide
      un solo ingrediente y cuántos gramos le toquen, y eso lo deciden los
      requisitos, no la fibra. No hay palanca barata. El motor se quedó
      como estaba.

      **Lo que hace falta para poder hacer algo es una decisión de
      nutrición**, no de programación: si Rawku quiere apuntar a un rango
      (el consenso clínico que se citó habla de 10-20 g/1000 kcal como
      «moderado», y de que BARF va por debajo de la comida comercial, ~2,7
      % MS vs ~3,4 %), eso se implementa como un suelo BLANDO en el solver
      -- se intenta llegar, y si no se llega el menú sale igual. Es media
      tarde de trabajo. Pero la cifra tiene que venir de Chris: aquí no
      se inventan datos nutricionales.

      Fuentes que trajo ella: Schmidt et al. (2018) PLOS ONE
      13(8):e0201279; Torres-Henderson C. (2025), *The Role of Dietary
      Fiber in Pet Nutrition*, Today's Veterinary Practice.

- [ ] **¿Hace falta estar dada de alta como autónoma para cobrar?**
      Pregunta para la gestoría, antes de rellenar el tipo de negocio en
      Stripe. Bloquea la verificación del negocio.
- [ ] **Revisar los textos legales** cuando estén redactados (ver 3.1).
      El borrador lo puedo escribir yo; el visto bueno no.

      ⚠️ **SUBIÓ DE PRIORIDAD EL 24 DE AGOSTO: ahora bloquea DOS cosas.**
      No solo Stripe. También **entrar con Google**: para publicar la app,
      Google exige un enlace a la Política de Privacidad y otro a las
      Condiciones del Servicio, y esas páginas no existen. Con eso hecho se
      desbloquean las dos de golpe.

      La parte difícil de una política de privacidad es saber qué datos
      recoge la app de verdad y a dónde van, y eso **sí** se puede sacar
      del código con exactitud: qué se guarda en Supabase, qué se manda a
      la API, qué llega a Sentry cuando hay un error, qué toca Stripe. El
      borrador puede salir de ahí — datos reales, no plantilla — pero es
      un texto legal y necesita revisión de quien sepa antes de publicarse.

---

## 1. Urgente — dinero y salud

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

      ⚠️ **MOVIDA EL 24 DE AGOSTO, pedido expreso**: «no quiero que la
      compra aparezca en el menú, tiene que estar solo en el menú lateral».
      Quitada del menú de un perro y de la pantalla de varios; vive solo en
      el panel, en los **dos** paneles (el ligero y el de dentro del menú —
      se puso solo en el primero y desde la pantalla del menú, que es donde
      más falta hace, no salía).

      Al sacarla del menú apareció un fallo que antes no existía: leyendo
      solo lo GUARDADO, acabas de generar un menú, no le has dado a guardar
      y el panel te enseña la compra del menú **anterior** — números
      correctos, menú equivocado, nada en pantalla que lo delate. Ahora
      manda lo que tienes en pantalla y la pantalla dice de dónde salen los
      números. Y se puede elegir **para cuántos días** (3, 1 semana, 2
      semanas, 1 mes): los menús cubren una semana, así que el resto se
      escala en proporción y se avisa cuando no es una semana.
- [x] **La burbuja de perro y el engranaje, en TODAS las pantallas.** ✅
      **Hecho el 24 de agosto.** Caso real: «la burbuja de perfiles de
      perro y configuración tiene que existir en todas las pantallas, y en
      todas las pantallas del menú lateral no aparecen».

      Cierto: las seis pantallas que abre el panel (Perfil, Evolución, Mis
      menús, Analizar, Por qué Rawku) tienen su **propia cabecera**, seis
      copias, y se quedaron sin ella. Entrabas en Evolución y ya no sabías
      de qué perro estabas viendo la evolución ni podías cambiar sin volver
      atrás. También faltaba en Evolución/Analizar abiertas desde el
      perfil, que es otra llamada distinta a `VistaMenus`.

      La prueba (`tests/burbuja-en-todas.spec.js`) **no mira que exista**:
      la pantalla de debajo sigue en el DOM con la suya y Playwright la
      encuentra igual — quitando la burbuja de las seis cabeceras, la
      primera versión de la prueba seguía pasando. Mira que **funcione**:
      la toca y exige que se abra la hoja de perros. Y una tercera prueba
      exige que el panel no tenga ninguna entrada que la lista no cubra,
      para que la séptima pantalla no se olvide.
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

- [x] **La compra: elegir el menú, los días bien, y marcar lo que ya
      tienes.** Pedido el 24 de agosto después de usarla; hecho el 25.

      1. **Elegir qué menú ver.** Selector arriba de la lista: "Todos
         juntos" o "Menú N · X días".

      2. **Los días.** Era un fallo de concepto, no de cuentas: la cesta
         salía de UNA SEMANA y todo se escalaba por dias/7, pero los menús
         de una semana no duran lo mismo (uno cubre 4 días y otro 3). Sus
         palabras: *«si cocinas para 1 semana uno de 3 días tienes para más
         de dos»*. Ahora son dos preguntas distintas según lo que mires:
         todos juntos → **semanas** (multiplicar una semana por 2 es
         exacto); un menú solo → **tandas de ese menú**, y cada opción dice
         los días de comida que da ("2 tandas · 6 días"). Encima de la
         lista, en grande, los días que cubre lo que estás viendo.

      3. **Casillas para marcar lo comprado**, la línea entera pulsable
         (un cuadradito de 12 px no se acierta de pie en una tienda), y un
         botón de empezar de cero que solo sale si hay algo marcado. Se
         guarda en el navegador a propósito, no en Supabase: es de este
         móvil y de esta compra.

      PR #31 de canislab-web. 8 pruebas nuevas, comprobadas rompiéndolas.

- [ ] **Una versión para dueños y otra para veterinarios.** ⚠️ **DECIDIDO
      el 28 de agosto — el plan entero está en `VETERINARIOS.md`.** Aquí
      queda solo lo que se decidió, para no tener que abrir el otro
      documento para saber por dónde va.

      **EL PRINCIPIO DEL QUE SALE TODO** (28 de agosto): el modo veterinario
      **no puede ser una degradación para el tutor**. La tentación es
      bloquearlo todo hasta que alguien firme, y eso mata el producto — el
      tutor paga y recibe menos que ayer. Es al revés: sin validación la
      app hace todo lo que hace hoy, **más decirte qué haría con el
      diagnóstico y qué dato exacto le falta**. «Con la creatinina y el UPC
      podría formular para IRIS 2» convierte; un muro no.

      De ahí sale el reparto: el tutor siempre puede todo el producto de
      perro sano, meter síntomas y seguimiento (los instrumentos validados
      —CBPI, LOAD, CIBDAI, PVAS— son *owner-reported* por construcción, y
      la frecuencia respiratoria en reposo es la mejor medición domiciliaria
      que hay), ver los 30 requisitos sin nada escondido, pedir dieta para
      un diagnóstico, exportar, y **retirarle el acceso al veterinario y
      apagar el modo terapéutico**: es su perro y sus datos.

      La frontera de lo que exige firma es limpia y no arbitraria: **bajar
      de los mínimos de FEDIAF**, que es exactamente donde deja de ser una
      dieta completa y equilibrada y pasa a ser una prescripción.

      Y lo que más valor tiene de todo el proyecto no es un permiso: es
      **el informe que el tutor imprime y le lleva a su veterinario**
      (diagnóstico, objetivos y de dónde salen, los 30 requisitos, la lista
      de la compra y la curva). Eso invierte la captación — no hay que
      reclutar veterinarios, **los traen los tutores**, uno a uno y con un
      caso delante. Y su miedo a la comida casera está justificado: Larsen
      *et al.* (JAVMA 2012) evaluaron 39 recetas renales publicadas y
      **ninguna** cumplía el NRC. No se le quita convenciéndole; se le quita
      enseñándole los números.

      Se preguntó el 24 de agosto y quedaron cuatro preguntas abiertas que
      no podía contestar un programador. Contestadas:

      · **Una sola app**, un repositorio y un motor, con un modo
        profesional que se enciende según quién entra. No dos productos.
      · **Los pacientes, en dos fases**: primero fichas que crea el propio
        veterinario (el dueño puede no tener ni cuenta), después perros que
        el dueño le comparte por invitación. La tabla `accesos` se hace
        desde el día uno para que quepan las dos.
      · **Sí puede bajar de los mínimos de FEDIAF** — que es lo que hace
        falta en una dieta renal o hepática de verdad — pero declarándolo:
        el menú se sigue verificando entero, contra un juego de requisitos
        escrito que viaja con él, y el semáforo dice «verde con
        excepciones», nunca verde a secas. Los cinco topes de seguridad
        crónica no los levanta nadie.
      · **Todavía no se cobra**: gratis para unos pocos veterinarios y el
        precio se decide con lo que se vea.
      · **Acreditación por número de colegiado y alta a mano.** El rol no
        se enciende solo.
      · **La pauta sale firmada**, con el nombre del veterinario y su
        número de colegiado.

      Y tres cosas que no se preguntaron porque no tienen dos respuestas
      razonables: **el veterinario nunca entra en la cuenta del dueño**
      (entra con la suya y ve al perro por un acceso concedido — si
      suplantara, la base de datos no podría saber quién pautó qué),
      **siempre tiene cuenta**, y **el dueño puede no tenerla**.

      Dos cosas que salieron al mirar el código y que conviene saber antes
      de empezar:

      · **Las fases 1 a 3 casi no tocan esta API.** `verificar()` ya
        devuelve todo lo que quiere un profesional — valor, mínimo, máximo
        y margen de los 29 nutrientes, huecos, `dato_dudoso`, Ca:P, topes
        aplicados. La versión de dueño es el frontend enseñando tres cifras
        de treinta. Lo profesional no hay que calcularlo: hay que dejar de
        taparlo. De aquí solo hace falta un `codigo` estable en cada aviso,
        para que el frontend pueda contarlo de otra manera sin duplicar los
        textos en Python.
      · **La API no autentica nada** (CORS en `*`, ningún `Depends`,
        ningún token; el premium lo tapa el frontend con un `blur`). Da
        igual para las fases 1 a 3, porque los datos los protege la
        seguridad por fila de Supabase. Pero «solo un veterinario
        acreditado puede prescribir» comprobado en el frontend no es una
        regla: cualquiera podría mandar una prescripción con el fósforo a
        300 desde una terminal. **La fase 4 empieza por validar el JWT de
        Supabase en la API**, o no se despliega.

      **La firma es la decisión que más obliga**, y no por lo que hay que
      pintar en el PDF. Un documento firmado tiene que seguir diciendo lo
      mismo dentro de un año, y hoy la tabla `menus` guarda nombre, gramos
      y kcal — ni la etapa, ni el DER, ni las patologías —, que es justo
      por lo que `/perro/{perro_id}/menus` marca lo que devuelve como
      `verificado: False`. Firmar eso no se puede: la ficha del perro
      cambia (el peso objetivo de Lola, 7,0 → 6,2), el catálogo cambia
      (fuera la borraja el 27, fuera cinco suplementos el 26) y el motor
      cambia (el fósforo renal, de 1400 a 1200 el 25). **Firmar obliga a
      congelar**: al firmar se guarda una copia inmutable del menú, de la
      ficha verificada entera, del contexto, de los huecos y de los tres
      sellos con los que se calculó. Y ese trabajo hace falta también para
      la prescripción de la fase 4, así que se hace una vez y va antes que
      las dos.

      Dos consecuencias que conviene no olvidar: **el modo profesional
      (fase 1) deja de ser una mejora y pasa a ser requisito** — quien
      firma tiene que poder ver lo que firma —, y **el sello de lo firmado
      lo calcula la API sobre lo que verificó**, no el frontend sobre lo
      que pintó: si no, habría dos ideas de «lo firmado» y el sello
      cuadraría consigo mismo sin decir nada, que es la misma familia de
      fallo que la duplicación del DER.

      Sigue abierto, y no lo decide un programador: **qué dice el
      documento sobre qué se firma exactamente** — si el vet firma la
      pauta, si firma haberla revisado, qué papel tiene Rawku en medio.
      Conviene preguntarlo antes de que salga la primera pauta firmada de
      verdad. No cambia nada de lo de arriba: solo cambia ese texto.
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

      **QUÉ FALTA, Y NO ES CÓDIGO.** Para publicar la app en Google —
      dejarla en producción, o sea que pueda entrar cualquiera y no solo
      unos correos apuntados a mano — Google **exige** tres cosas en
      *Información de marca*:

      · Página principal de la aplicación
      · Enlace a la **Política de Privacidad**
      · Enlace a las **Condiciones del Servicio**

      Y esas dos páginas **no existen**. Comprobado: no hay nada de eso en
      `canislab-web/src`. Mientras falten, el botón «Publicar app» sale en
      gris con el aviso *«La configuración de OAuth de tu app está
      incompleta»*. No es un fallo: es que falta un dato real.

      Así que esto **depende de los textos legales** (ver 3.1), igual que
      Stripe — que también los pide para cobrar. Los tres van juntos.

      **LO QUE YA ESTÁ HECHO EN GOOGLE CLOUD** (24 agosto), para no
      repetirlo:
      · Cuenta de Google Cloud: ya existía.
      · Proyecto **Rawku** creado.
      · *Información de marca*: nombre de la app y correo de contacto
        puestos y guardados.
      · Tipo de usuario: **Externo**.
      · Estado: **En pruebas**. Falta publicar, por lo de arriba.

      **LO QUE FALTARÍA CUANDO HAYA TEXTOS LEGALES**, en orden:
      1. *Información de marca*: pegar los tres enlaces y añadir
         `rawku.app` en **Dominios autorizados** (si pones la página
         principal, Google obliga a registrar el dominio).
      2. `console.cloud.google.com/auth/audience` → **Publicar app**. No
         hace falta verificación de Google: solo se piden los permisos
         básicos (nombre, correo, foto). La revisión larga es para apps
         que piden Gmail o Drive.
      3. `console.cloud.google.com/auth/clients` → crear cliente OAuth,
         tipo **Aplicación web**. En *URI de redireccionamiento
         autorizados*, EXACTAMENTE:
         `https://kvtkdpgpmrvwmvymyqof.supabase.co/auth/v1/callback`
         (sin barra final). *Orígenes de JavaScript*: vacío — Google no
         habla con rawku.app, habla con Supabase.
      4. Supabase → *Authentication → Providers → Google*: activar y pegar
         el ID de cliente y el secreto.
      5. Supabase → *Authentication → URL Configuration*:
         **Site URL** `https://rawku.app` y en **Redirect URLs**
         `https://rawku.app/**`. **Sin esto no vuelve a la app**: Supabase
         solo obedece el `redirectTo` si la dirección está en esa lista.

      **EL CÓDIGO QUE SE QUITÓ**, para rehacerlo sin pensarlo dos veces
      (está en el historial: rama `claude/la-compra-solo-en-el-panel`, PR
      web #25, deshecho en el siguiente):
      · `supabase.js`: `entrarConGoogle()` con `signInWithOAuth`,
        `redirectTo: window.location.origin + '/'` y
        `queryParams: { prompt: 'select_account' }` — para que ofrezca
        elegir cuenta en vez de entrar con la última usada, que en un móvil
        compartido importa.
      · `auth.jsx`: el botón (con el logo de Google en SVG inline, para no
        depender de una imagen externa), y un `useEffect` que lee
        `error_description` de la URL **y del hash** al volver. Ese
        segundo detalle no es opcional: según el flujo el motivo llega en
        uno o en otro, y mirar solo uno deja la mitad de los casos en
        silencio. Además limpiaba la URL, para que recargar no repitiera
        el error para siempre.
      · `tests/entrar-con-google.spec.js`: 5 pruebas — el botón está donde
        toca y no en «olvidé mi contraseña»; manda a `/auth/v1/authorize`
        con `provider=google` y el `redirect_to` correcto (con esto mal la
        sesión se pierde sin dar ningún error); y el error se lee, en la
        query y en el hash, y no se queda pegado al recargar.

      **MIENTRAS TANTO**, si se quiere probar el circuito entero sin
      publicar: dejarlo en *Prueba* y añadirse como **usuario de prueba**
      (admite hasta 100 correos). Entra quien esté en esa lista y nadie
      más — sirve para comprobar que funciona, no para abrirlo.
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

---

## 5. Nutrición — auditado contra el PDF oficial

> ### ⚠️ LO QUE ESTA AUDITORÍA **NO** COMPRUEBA (25 de agosto)
>
> Se escribe aquí porque el 25 de agosto apareció un fallo que esta
> auditoría tenía delante y no vio, y la pregunta que hizo falta contestar
> fue: *«¿cómo puedo fiarme de que está todo correcto?»*. Merece una
> respuesta escrita, no de palabra.
>
> **Lo que pasó.** En `requerimientos_v2_final.json` había una fila
> `Fibra` (mínimo 4,29 g/1000 kcal, máximo 14,3) **que no está en la tabla
> de FEDIAF**. Lleva ahí desde el primer commit del repositorio (14 de
> agosto), sin nota de fuente. El motor nunca la usó, pero el analizador
> sí: por eso un menú hecho por la propia app salía «le falta fibra». 8 de
> 8 menús verdes se quedaban cortos.
>
> **Por qué la auditoría dijo «161 cuadran, 0 discrepancias».** Porque
> recorría la lista de FEDIAF y comprobaba que cada valor estuviera bien
> puesto en el JSON. Nunca comprobaba lo contrario: que cada fila del JSON
> venga de FEDIAF. Una fila que sobra era invisible. **Ya no**: desde el 25
> de agosto mira los dos sentidos, y el BLOQUE 18 de `pruebas_completas.py`
> la ejecuta y exige 0 discrepancias.
>
> **Lo que sigue sin comprobar nadie**, y hay que saberlo:
>
> 1. **La tabla de FEDIAF de `auditar_fediaf.py` está transcrita a mano**
>    del PDF. Si un número se tecleó mal ahí Y está igual de mal en el
>    JSON, los dos cuadran y nadie se entera. Lo único que lo cierra es
>    que una persona lea las dos columnas contra el PDF una vez.
> 2. **Los valores de los ALIMENTOS (`alimentos_v3_final.json`) no tienen
>    ninguna auditoría.** Los requisitos sí; la composición de cada
>    alimento, no. Un valor mal ahí tuerce todos los menús que lo usen y
>    ninguna prueba lo vería: las pruebas comprueban que el motor cumple
>    los requisitos *con los datos que tiene*.
> 3. **Faltan datos de fibra en 3 verduras** (borraja, coles de Bruselas,
>    tomate en puré). Hoy no afecta a nada porque la fibra no es un
>    requisito, pero el hueco está.
>
> **Qué significa «TODO EN VERDE»**, para no volver a confundirlo: que el
> motor cumple lo que dice el JSON, que ningún menú sale sin verificar, y
> que las reglas del motor existen de verdad. **No** significa que el JSON
> sea correcto. Eso lo dice la auditoría contra el PDF, y solo hasta donde
> llega la transcripción del punto 1.

**Hecho el 21 de agosto** contra la TABLA III-3b de la *FEDIAF Nutritional
Guidelines 2025* (el PDF oficial, no de memoria). Script reproducible en
`auditar_fediaf.py`.

**161 de 161 comprobaciones cuadran exactas** — mínimos *y* máximos. Se
verificó, para los nutrientes del JSON y en las tres etapas: el valor,
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

Generado por `auditar_catalogo.py`: **57 alimentos y 431 valores** por
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
