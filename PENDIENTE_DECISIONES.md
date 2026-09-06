# Decisiones tuyas (no son trabajo de programación)

Parte de `PENDIENTE.md`, separado el 6 de septiembre para que abrirlo no
cueste nada en sesiones que no tocan una decisión pendiente. Sigue siendo
lo primero que bloquea al resto — el índice de `PENDIENTE.md` señala aquí
para cada punto.

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

- [x] **El peso ideal desde el BCS estaba calculado de dos formas.**
      RESUELTO el 29 de agosto: `verificar.peso_objetivo_desde_bcs` estaba
      mal (restaba en vez de dividir), `der.py`/`App.jsx` estaban bien.
      Vigilado por el BLOQUE 37. Detalle completo: `HECHO.md`.

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

      **Y el problema de fondo no es el mapeo, es quién puntúa**: el dueño
      subestima el BCS de forma sistemática, más cuanto más gordo está el
      perro, y eso empuja a más kcal justo al que ya está gordo. Las
      cifras (Eastland-Jones 2014, Blanchard 2023, Söder 2023):
      `PENDIENTE_DETALLE.md`.

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
      ⚠️ La nutricionista ya no es Michelle: es Cris. Las cinco van en
      `Rawku_para_Cris.pdf` (28 de agosto), repartidas entre las
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
      podría comer un menú normal. Si Cris dice que merece la pena,
      hay que partir la opción en dos. El tope de 2,4 mg ya está puesto en
      el código esperando ese día.

      ⚠️ **Y esto conecta con la parte para veterinarios** (28 de agosto):
      uno de los tres poderes que solo tiene el profesional es justamente
      **levantar un bloqueo asumiendo la responsabilidad** — «formula con
      cobre ≤ 1,2, respondo yo». O sea que partir la opción en dos deja de
      ser la única salida: la otra es que un veterinario acreditado pueda
      desbloquearlo caso a caso. Las dos cosas son compatibles y no se
      estorban.

- [x] **`EPA_DHA_total` ya suma las dos claves.** Hecho el 25 de agosto,
      con claves derivadas en `valor_nutriente`. Detalle completo: `HECHO.md`.

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

- [ ] **¿Rawku apunta a algún rango de fibra? — pregunta 7 del PDF de Cris.**
      Ni FEDIAF, ni AAFCO, ni el NRC dan un mínimo: la fibra no es un
      nutriente esencial y no tiene valor de referencia oficial. Así que
      no se puede poner un mínimo duro sin dejar sin menú a perros con
      patologías que limitan verduras o que necesitan fibra baja.

      **Medido el 25 de agosto**: el mismo perro, el mismo botón, ocho
      veces seguidas, da de 0,00 a 28,40 g/1000 kcal al azar — al motor la
      fibra le da igual, así que entre verduras que cumplen lo mismo elige
      por el ruido que le da variedad. **Enseñar hoy esa cifra sería
      enseñar una moneda al aire.** Se probó a corregirlo con una
      preferencia en el motor y no funcionó: seguía yendo de 0,12 a 29,47
      según la fuerza del ajuste. La tabla completa y la medición del
      intento fallido: `PENDIENTE_DETALLE.md`.

      **Lo que hace falta para poder hacer algo es una decisión de
      nutrición**, no de programación: si Rawku quiere apuntar a un rango
      (el consenso clínico que se citó habla de 10-20 g/1000 kcal como
      «moderado», y de que BARF va por debajo de la comida comercial, ~2,7
      % MS vs ~3,4 %), eso se implementa como un suelo BLANDO en el solver
      -- se intenta llegar, y si no se llega el menú sale igual. Es media
      tarde de trabajo. Pero la cifra tiene que venir de Cris: aquí no
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

