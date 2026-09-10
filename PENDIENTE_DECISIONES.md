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

- [x] **Cuatro fichas que había señalado la comprobación nueva del cociente.**
      RESUELTO — investigadas contra USDA el 7 de septiembre (ver más abajo,
      «Auditar los valores de los ALIMENTOS»): el pulmón de cordero (Leu/Ile
      2,54) y los tres cefalópodos (valina≈isoleucina) tienen esos cocientes
      de verdad en la fuente primaria USDA, confirmado con `WebSearch`, no
      de memoria. No son una copia mal calibrada como el caso del pavo
      contaminado que motivó la comprobación: son cocientes reales de esas
      especies. Esta entrada se quedó sin marcar después de investigarse;
      corregido aquí el 7 de septiembre al revisar el documento entero
      contra el estado real del código, no contra lo que decía de memoria.

      | ficha | qué salía | resultado |
      |---|---|---|
      | Pulmón de cordero | Leu/Ile 2,537, isoleucina 3,16% | Real, confirmado contra USDA |
      | Calamar / Pulpo / Sepia | valina = isoleucina | Real: en cefalópodos Val≈Ile de verdad |

- [ ] **El máximo de lisina de FEDIAF, reformulada tras leer la fuente
      primaria (7 de septiembre) — la pregunta original estaba mal
      planteada.** (28 de agosto, para el nutricionista.) La Tabla III-3b
      pone un solo máximo a un aminoácido: **lisina 7,00 g/1000 kcal, y
      solo en crecimiento**. Está bien transcrito — `auditar_fediaf.py` lo
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

      **La pregunta original preguntaba mal.** Se planteaba como «¿se mide
      sobre la proteína de la tabla o sobre la del plato?», dando por hecho
      que el 7,00 sale de un ratio lisina/proteína. Leído el propio texto de
      FEDIAF (p.22 del PDF, sección «Lysine»), **no es así**: el número no
      viene de ningún ratio con la proteína. Viene de un único estudio de
      dosis-respuesta con lisina SUPLEMENTADA (Czarnecki et al. 1985): a
      cachorros se les dio una dieta basal (0,91% DM) más lisina cristalina
      añadida hasta 4,91% DM, y el peso bajó; con 2,91% DM (2 puntos de
      suplemento en vez de 4) no bajó. FEDIAF tomó ese 2,91% DM como el
      "no-effect-level" y lo convirtió a energía (a 4156 kcal/kg): **7,0
      g/1000 kcal**. Es un umbral de seguridad absoluto (mg de lisina por
      kcal ingerida), no una proporción con la proteína del plato.

      Esto cambia la pregunta real, y la deja más concreta para el
      nutricionista: el estudio de origen usó lisina **cristalina
      suplementada** (absorción rápida, sin el resto de aminoácidos que la
      acompañan en una proteína entera) — la toxicología de aminoácidos
      libres suplementados suele ser distinta de la del mismo aminoácido
      ligado a proteína intacta, de absorción más lenta y equilibrada.
      **¿Generaliza ese no-effect-level de lisina cristalina a la lisina
      que llega ligada a la carne y el hueso de una ración BARF?** Si no
      generaliza, no aplicar el techo sigue siendo correcto (y por un
      motivo más sólido que el de antes). Si sí generaliza, hay que
      reconsiderar si una ración BARF de cachorro es viable tal cual bajo
      este criterio — pero eso ya no es una duda sobre qué proteína usa la
      fórmula, es una pregunta farmacológica sobre aminoácidos libres vs.
      proteína intacta, y la tiene que responder ella.

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
         (sodio 739/739/625/480 según estadio -- ⚠️ CORREGIDO el 8 de
         septiembre: eran 900/900/790/480 y se atribuían a «ACVIM 2019
         Keene et al.», pero al abrir el consenso resultó que NO da ninguna
         cifra de sodio: es cualitativo en las cuatro etapas. Las cifras son
         de Cavanaugh, Veterinary Practice News 2020, y tres de las cuatro
         superaban el techo legal europeo de 739 mg. Ver `PATOLOGIAS.md`
         §1.1 y §1.4),
         cruzadas además contra SACN5 cap.36 Tabla 36-4 (confirma el patrón,
         no cambia los números -- framework ISACHC distinto del ACVIM). La
         app ya pregunta el estadio (familia "cardiopatia" en
         `VETERINARIOS.md` §12-quinquies). La genérica `cardiopatia` (739,
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

- [x] **Repasar la transcripción de la tabla de FEDIAF — HECHO el 7 de
      septiembre.** En `auditar_fediaf.py` la tabla III-3b está escrita a
      mano. La auditoría compara el JSON contra ESA transcripción: si un
      número se tecleó mal en los dos sitios igual, cuadra y nadie lo ve.
      Se extrajo la Tabla III-3b entera del PDF de nuevo (independiente de
      la transcripción) y se comparó celda a celda, los 41 nutrientes:
      **40 coinciden exactamente**. El único que no —
      `MAXIMOS["Fósforo"] = 4000`— no era un error de transcripción, era
      un número sin fuente que llevaba ahí desde el primer PR del repo
      (`ae7878b`): ni FEDIAF, ni NRC 2006, ni Dobenecker et al. 2021 (el
      estudio más específico sobre toxicidad de fósforo en perros) dan
      ningún máximo. Quitado — ver `HECHO.md`. Nació el 25 de agosto,
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


---

## Lo que dejó abierto la cuarta pasada (8 de septiembre, tarde)

- [x] **El fósforo del perro sano.** ✅ RESUELTO el 8 de septiembre por la
  noche, y no era una decisión tuya: lo dice SACN5 (Tabla 13-3 para el adulto,
  14-2 para el maduro) y se midió que cabe. Aplicado como techo duro, 2000 en
  adulto y 1750 en senior, con el sodio a 1000. Los cuatro pesos probados salen
  en el peldaño 0 y en verde, y el perro de 3 kg pasa de ámbar a verde. Costó
  regenerar los 216 menús precalculados de la vista previa. Ver `DECISIONES.md`
  D-15.

- [ ] **En crecimiento, ¿los suelos de una patología también se caen?** Hoy sí:
  `solo_en_adulto` se salta la patología **entera**, topes y suelos. Para la
  artrosis eso significa que un cachorro con displasia no recibe el refuerzo de
  omega-3 ni el de vitamina E, que no tienen nada de peligroso a esa edad. El
  motivo de que se caigan es el **techo** de fósforo (2000 cae bajo el mínimo de
  un cachorro, 2250), no el suelo. Separar las dos cosas es cinco líneas de
  código; **si se debe hacer es criterio clínico.** El aviso de crecimiento de la
  artrosis, mientras tanto, dice la verdad: no se aplica nada.

- [ ] **La proteína de la reacción adversa al alimento (≤55 g/1000 kcal).** La
  fuente la pide «(dermatologic cases only)» y el motor no sabe si este perro
  reacciona por la piel o por el intestino — y en el segundo caso la misma página
  pide **más** proteína, no menos. Está escrita y **no** aplicada. Se resuelve o
  bien preguntando en la ficha cómo se manifiesta, o bien con la pantalla de
  objetivos por nutriente, donde un profesional la fijaría a mano.

## Lo que dejó abierto leer SACN5 entera (10 de septiembre de 2026)

Tres decisiones, las tres con los números ya delante. **Ninguna es de fuentes:**
la fuente ya dijo lo que dice, y lo que falta es criterio de producto.

### 1 · ¿Se pregunta dónde duerme el perro?

FEDIAF §7.2.3.5 dice que un perro que vive fuera en invierno puede necesitar de
un **10 a un 90 %** más de calorías. Ese rango era la razón por la que esto
estaba parado. **SACN5 Tabla 5-3 da las cifras concretas:**

| Perro | Aumento del DER | De | A |
|---|---|---|---|
| Labrador retriever y beagle | +25 % (12-43) | 15 °C | 8,5 °C |
| Gran Danés | +22 % | verano | invierno |
| Pelo **corto** | **+95 %** | 25 °C | 7,6 °C |
| Pelo **largo** | +59,5 % | 25 °C | 7,6 °C |
| Beagle | +70,5 % | 17 °C | −17 °C |
| Perro de trineo | +61,5 % | 17 °C | −17 °C |

Lo que hay que decidir: **(a)** si se pregunta; **(b)** qué se pregunta
exactamente —¿duerme fuera? ¿a cuántos grados? el tipo de pelo la app podría
deducirlo de la raza—; **(c)** qué se hace con un perro que duerme fuera solo
parte del año. Hoy ese perro recibe la misma ración que uno de piso.

### 2 · La densidad con la que se leen las cifras de obesidad

Todas las tablas de SACN5 se convierten a 4,0 kcal/g de materia seca, y eso está
probado (ver `HECHO.md` del 9-10 de septiembre). **La Tabla 27-4 es la única de
las 24 que propone otra cosa** — pero para el propio alimento, no como base de
conversión: «Foods for weight loss … should contain **≤3,4 kcal ME/g**».

No dice que sus otras filas estén expresadas a esa densidad; ninguna tabla lo
dice salvo la 13-3, que dice 4,0. Pero si lo estuvieran, **sus cifras subirían un
18 %**. Se ha dejado en 4,0 por ser la lectura literal. Es una pregunta para la
nutricionista, no una decisión de código.

### 3 · La energía del cachorro: ¿por edad o por fracción de peso adulto?

SACN5 da la misma regla de dos maneras y el motor usa la del capítulo 5:

| Fuente | Cómo la parte | Escalones |
|---|---|---|
| Cap. 5 (lo que aplica el motor) | por **edad** | 3 × RER hasta los 4 meses, 2 × RER después |
| **Tabla 17-2** (capítulo de crecimiento) | por **fracción del peso adulto** | 3 × RER hasta el 50 %, 2,5 × del 50 al 80 %, 1,8-2,0 × por encima del 80 % |

No se contradicen: dicen lo mismo con variables distintas. Pero la del capítulo
de crecimiento es **más fina** (tres escalones en vez de dos) y **la app ya
pregunta el peso adulto estimado**, así que tiene el dato. Cambiarla movería la
ración de los cachorros que están entre el 50 y el 80 % de su peso adulto.

Y trae aparte al Gran Danés otra vez: «may need **25 % more energy** during the
first two months after weaning = **250 kcal/BWkg^0,75**», y «may not grow when
daily energy intake is less than 175 kcal ME/BWkg^0,75».

### 4 · ⚠️ Un perro en BCS 4 recibe hoy un 8 % más de comida, y FEDIAF dice que BCS 4 ya es ideal

**Encontrado el 10 de septiembre con `radiografia.py`**, comparando lo que ENTRA
al motor contra `main`. Es la clase de fallo que la batería no puede ver: el menú
sale verde porque cuadra con las kcal que le dieron, y lo que cambia es el peso
con el que se calcularon esas kcal.

**Lo que hace el motor hoy** (perro de 30 kg reales, peso que usa para escalar):

| BCS | Peso de referencia | Cambio | Efecto en las kcal |
|---|---|---|---|
| 1, 2, 3 | 36,00 kg | +20,0 % | **+14,7 %** |
| **4** | **33,33 kg** | **+11,1 %** | **+8,2 %** |
| 5 | (no deriva) | — | — |
| 6 | 27,27 kg | −9,1 % | −6,9 % |
| 7 | 25,00 kg | −16,7 % | −12,8 % |
| 8 | 23,08 kg | −23,1 % | −17,9 % |
| 9 | 20,69 kg | −31,0 % | −24,3 % |

**La tensión, y está dentro de FEDIAF, no entre FEDIAF y otra fuente:**

- La **§7.1.1** dice que la energía se calcula sobre el peso óptimo y **no
  distingue dirección**. Es la lectura con la que se aplicó el 9 de septiembre:
  si el perro está por debajo de 5, se deriva hacia arriba.
- La **§7.1.3** dice, literal: *«**The ideal BCS should therefore be between 4/9
  and 5/9**»*, y la **§7.2.4.1** lo repite citando a Kealy 2002 — el estudio de
  los catorce años en labradores, que es justo el que enseña que el perro más
  delgado vive más.

Si el ideal es el **rango 4-5** y no el punto 5, un perro en BCS 4 **ya está en
su peso**, y darle un 8 % más de comida es empujarlo fuera del rango que la
propia fuente asocia con vivir más.

**Qué hay que decidir**, y es de criterio, no de lectura:

1. ¿`BCS_NEUTRO` sigue siendo el **punto 5**, o pasa a ser el **rango 4-5**?
2. Si pasa a ser rango: ¿el BCS 4 deja de derivar peso objetivo (lo más simple),
   o deriva hacia el punto medio del rango?
3. Y lo mismo por arriba: hoy el BCS 6 baja un 6,9 % las kcal. Si el ideal llega
   hasta 5, el 6 sí está por encima y eso se queda como está.

⚠️ **Toca a todo perro marcado como «delgado» en la pantalla del dueño**, porque
el escalón 1 de los cinco del dueño mapea a BCS 3 — y a cualquiera al que un
veterinario le ponga un 4. No es un caso raro.

Las dos citas y la medida están aquí; el cambio, en `main._peso_de_referencia` y
en `verificar.peso_objetivo_desde_bcs`, que son **dos copias** de la misma regla
y tendrían que moverse juntas.
