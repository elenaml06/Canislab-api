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

- [x] **Límites por patología: confirmar los números.** ⚠️ **ESTA TABLA ESTABA
      DESACTUALIZADA (comprobado el 6 de septiembre contra
      `motor_completo.PATOLOGIAS` en producción)** — decía "Hoy" con los
      valores del 20 de agosto y el código ya se había movido:
      | | Decía aquí | **En producción hoy** | Mín. FEDIAF | Recomendado (20 ago) |
      |---|---|---|---|---|
      | Fósforo (renal) | 1400 | **1200 — YA APLICADO** | 1160 | 1200 |
      | Cobre (hepatopatía) | 3.0 | **2.4** — intermedio, a propósito: ver abajo | 2.08 | 2.3 |
      | Grasa (pancreatitis) | 25 % | **20 %** — el punto de partida de las dietas comerciales bajas en grasa | — | 18 % |

      **Fósforo renal: cerrado**, coincide con lo recomendado.

      **Cobre hepatopatía: la opción ya se partió en dos (7 de
      septiembre).** `hepatopatia` (diagnóstico confirmado por biopsia o
      analítica de cobre) sigue bloqueando -- el terapéutico real (1,2) está
      bajo el mínimo FEDIAF y eso no cambia por mucho que se parta la
      opción. Lo que sí cambió: se añadió `raza_predispuesta_cobre` (Bedlington,
      Westie, Labrador, Dálmata... predispuestos SIN diagnóstico confirmado),
      que SÍ formula un menú normal evitando los alimentos más cargados de
      cobre, sin bajar del mínimo. La app (`canislab-web`) ya pregunta cuál
      de las dos aplica -- ver `VETERINARIOS.md` §12-quinquies, familia
      "hepatopatia". El 2,4 mg de la entrada `hepatopatia` se queda igual
      (es correcto que sea el intermedio, no el terapéutico: la patología
      bloquea de todas formas). Sigue sin resolverse si además se ajusta a
      2,3 -- pero ya no urge, porque ahora hay una opción intermedia real
      (raza_predispuesta_cobre) para el caso que antes forzaba a elegir
      entre bloquear a todos o no bloquear a nadie.

      **Pancreatitis grasa: cerrado (6 de septiembre).** Cruzado contra
      SACN5 5ª ed., cap.67, Tabla 67-3: el rango general es ≤15% de materia
      seca (~37,5 g/1000kcal) y para el paciente obeso o hipertrigliceridémico
      baja a ≤10% (~25 g/1000kcal) -- los 20 g/1000kcal ya puestos (Merck)
      caen DENTRO de los dos rangos, incluido el más estricto. No hace falta
      bajar más: 20 ya es más restrictivo que lo que pide la fuente para el
      caso general, y casi tan restrictivo como el caso obeso/hipertrigli.
      Detalle: `PENDIENTE_NUTRICION.md` §10.
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
      2. **¿Distinguir el estadio ACVIM en cardiopatía (B2/C/D)? RESUELTO
         (6-7 de septiembre).** Se añadieron `cardiopatia_a/_b1/_b2/_c/_d`
         (sodio 900/900/790/480 según estadio, ACVIM 2019 Keene et al.),
         cruzadas además contra SACN5 cap.36 Tabla 36-4 (confirma el patrón,
         no cambia los números -- framework ISACHC distinto del ACVIM). La
         app ya pregunta el estadio (familia "cardiopatia" en
         `VETERINARIOS.md` §12-quinquies). La genérica `cardiopatia` (900,
         sin estadio) se queda para quien no lo sepa.
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

- [x] **La app no distingue "hepatopatía por cobre" de otras hepatopatías.**
      RESUELTO el 7 de septiembre: `raza_predispuesta_cobre` (formulable,
      sin diagnóstico confirmado) se añadió junto a `hepatopatia` (bloqueada,
      diagnóstico confirmado), con familia de subtipo en la app -- ver arriba
      y `VETERINARIOS.md` §12-quinquies. El poder del veterinario de
      "levantar un bloqueo asumiendo la responsabilidad" sigue existiendo
      igual para `hepatopatia` (`formulable_por_profesional: true`); las
      dos cosas siguen siendo compatibles, como ya se prevía aquí.

- [x] **`EPA_DHA_total` ya suma las dos claves.** Hecho el 25 de agosto,
      con claves derivadas en `valor_nutriente`. Detalle completo: `HECHO.md`.

- [ ] **Repasar la transcripción de la tabla de FEDIAF.** En
      `auditar_fediaf.py` la tabla III-3b está escrita a mano. La auditoría
      compara el JSON contra ESA transcripción: si un número se tecleó mal
      en los dos sitios igual, cuadra y nadie lo ve. Es leer las columnas
      contra el PDF una vez, y ya queda cerrado. Nació el 25 de agosto,
      cuando apareció una fila (`Fibra`) que no era de FEDIAF y la
      auditoría la daba por buena. Ver el recuadro del apartado 5.

- [x] **Auditar los valores de los ALIMENTOS.** RESUELTO — parte ya
      existía y no se sabía, parte se hizo el 7 de septiembre. Esta nota
      llevaba desde el 25 de agosto diciendo que `alimentos_v3_final.json`
      "no tiene ninguna auditoría", y era falso desde el 21 de agosto:
      `auditar_catalogo.py` existe, es exhaustivo (coherencia
      energía/macros, huecos sin declarar, omega-6 vs omega-3, ácidos
      grasos que no caben en la grasa total, `dato_dudoso`, ceros
      biológicamente imposibles por categoría, aminograma coherente —
      Leu/Ile, His/Val=Ile, triptófano%—, linaje de las purinas,
      consistencia órgano-categoría) y lo ejecuta el BLOQUE 19 de
      `pruebas_completas.py`. Nadie había vuelto a tachar esta línea
      después de construirla.

      Lo que sí se hizo el 7 de septiembre, ejecutando esa auditoría de
      verdad e investigando cada aviso activo en vez de darla por hecha:
      **2 falsos positivos corregidos** en el propio auditor, verificados
      contra USDA (`WebSearch`, no de memoria) — el pulmón de cordero
      (Leu/Ile 2,54) y calamar/pulpo/sepia (valina≈isoleucina) tienen esos
      cocientes de verdad en la fuente primaria, no son una copia mal
      calibrada como el caso del pavo; y **4 fichas de vísceras** (Bazo de
      vaca, Páncreas de vaca, Bazo de cordero, Cerebro de ternera) con
      `sin_dato` incompleto: su propia `nota_datos` ya decía qué minerales
      o vitaminas "se dejan en 0" por no tener dato fiable, pero el campo
      estructurado no los llevaba, así que contra un máximo contaban como
      cero MEDIDO en vez de hueco. Ningún valor numérico cambia. Detalle
      completo en el commit y en los comentarios de `auditar_catalogo.py`.

      Lo que sigue sin auditoría automática, y hay que decirlo: los
      valores en sí (que 78 kcal sea la cifra correcta de la dorada, y no
      solo que sea *consistente*) siguen viniendo de comparar contra BEDCA/
      CIQUAL/USDA a mano, caso a caso, cuando algo llama la atención. Una
      auditoría no puede saber si un número está bien sin la fuente
      primaria al lado — solo puede cazar cuándo un número no puede estar
      bien pase lo que pase (imposible, incoherente consigo mismo, o
      copiado de otra fila). Eso es justo lo que hace.

- [x] **Fibra de la borraja.** CERRADO el 7 de septiembre, aunque no como
      se pensaba el 25 de agosto: la borraja no está a medio rellenar, es
      que **ya no está en el catálogo entero** — se retiró en algún punto
      posterior (el BLOQUE 31 de `pruebas_completas.py` vigila justo eso:
      "la borraja, fuera del catálogo entero"). No es un hueco de dato: es
      un alimento que ya no existe, así que no hay nada que rellenar. Las
      otras dos sí están confirmadas: coles de Bruselas 4,3 g/100 g y
      tomate en puré 2,8 (159 de 159 fichas del catálogo traen ya la clave
      `fibra` — ver `PENDIENTE_NUTRICION.md` §5).

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

