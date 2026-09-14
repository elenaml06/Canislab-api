# Rawku — API del motor nutricional

Backend FastAPI + motor MILP en scipy. Desplegado en Render.
El frontend vive en `elenaml06/canislab-web` (Vercel, rawku.app).

**Empieza por `PENDIENTE.md`**: es el índice de lo que queda por hacer,
priorizado. Desde el 6 de septiembre es solo eso — un índice de una línea
por punto — y cada punto vive en uno de cuatro archivos por tema
(`PENDIENTE_DECISIONES.md`, `PENDIENTE_DINERO_Y_SALUD.md`,
`PENDIENTE_PRODUCTO.md`, `PENDIENTE_NUTRICION.md`). Abre solo el que toque
la tarea, no los cuatro de golpe.

## Qué es esto

Calcula raciones BARF para perros que cumplen los 43 requisitos de FEDIAF
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
   los 41 nutrientes + el ratio Ca:P + el calcio de raza grande + los
   límites de seguridad crónica.
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
   Y hay una **cuarta forma de límite desde el 10 de septiembre**: el **ratio
   entre dos nutrientes que pide una patología**, en el bloque `ratios` de
   `patologias.json`. Se estrenó con el Ca:P de 1,1-2,0 que piden las Tablas 40-5
   y 41-6 de SACN5 para los dos urolitos de calcio, que llevaba dos días escrito
   con `aplicado_por_el_solver: false` porque el motor sabía de ratios Ca:P —los
   aplica desde FEDIAF y desde la nota b— y **no tenía forma de que una PATOLOGÍA
   pidiera el suyo**. Y no era cosmético: el perro de 30 kg con oxalato salía con
   Ca:P **1,06** y salía **en verde**, porque el semáforo mide contra el 1,0-2,0
   de FEDIAF, que es el rango de un perro SANO. Es genérico —admite cualquier par
   de nutrientes— porque el omega-6:omega-3 necesita exactamente lo mismo, aunque
   ese siga **sin aplicarse**: sus fuentes van de <1:1 a 7:1 según la enfermedad y
   eso lo decide un clínico. Lo vigila el BLOQUE 75, con el fallo puesto.
   Y desde el 8 de septiembre hay una **tercera clase de límite**: los que el
   libro recomienda al perro **sano**, que se aplican **sin que haya ninguna
   patología marcada**, viven en `recomendaciones_libro.json` y se comprueban
   en el mismo sitio y con el mismo `min()` que los de patología. Desde el 11 de
   septiembre esa clase tiene **las dos mitades**: también suelos, con `max()`.
   Y ahí vale la regla de siempre: **si una fuente contradice a FEDIAF, gana
   FEDIAF**, así que un suelo del libro que se pasara de un máximo de FEDIAF se
   cae y se dice. ⚠️ **Hoy no hay ningún suelo encendido, y el único escrito
   lleva DOS decisiones del mismo día.** Es la vitamina E del perro sano (67,1
   mg/1000 kcal). Por la mañana del 11 de septiembre Elena lo encendió con la
   regla correcta —«la norma es la norma»: si la fuente lo dice, se aplica— y por
   la tarde lo apagó para poder entregar: «apágalo y fusiona todo, ya
   preguntaremos lo de la vitamina E». Lo segundo es el **orden**, no la norma:
   con el suelo encendido la batería sale roja en los BLOQUES 9 y 43, nada se
   entrega en rojo, y este suelo estaba reteniendo 150 commits que no tienen nada
   que ver con él. Lo que cuesta está **medido** y hay que leerlo antes de tocar
   nada:

   | | Con el suelo | Sin el suelo |
   |---|---|---|
   | Perro con **ocho especies fuera** (adulto 20 kg, cachorro 10 kg y toy 3 kg) | **sin menú los tres** | con menú los tres |
   | Las otras 15 combinaciones de alergias y exclusiones del BLOQUE 9 | con menú | con menú |
   | Toy de 1,5 kg **por la API**, con la escalera y el presupuesto de verdad | 10 de 10 con menú (7 en peldaño estricto) | — |
   | Toy de 1,5 kg **preguntando al solver con 1 s** (lo que aprieta el BLOQUE 43) | 20 de 20 sin menú | 12 de 20 sin menú |

   O sea: a quien usa la app solo le falta el menú si excluye ocho especies; el
   toy lo salva la escalera. La causa está medida y es de DATOS: **en el catálogo
   no hay un suplemento de vitamina E suelto**, solo los nueve multivitamínicos, y
   el motor deja meter dos. **La cifra NO se ha bajado** — se queda escrita con su
   fuente, su conversión y su medida, y se pregunta, que es la regla. El día que
   entre en el catálogo una ficha de vitamina E suelta se vuelve a poner a `true`
   y la batería tiene que salir verde: esa es la comprobación de que el problema
   era el catálogo y no la cifra. Está en `PENDIENTE_DECISIONES.md`, y el BLOQUE
   57 vigila las dos mitades — que siga apagado y que el `por_que` siga contando
   las dos decisiones. En adulto son
   Existen porque una ración BARF de este motor salía **pegada al máximo de
   FEDIAF** (~4000 mg/1000 kcal, y un menú del catálogo llegó a 4124, por
   encima), y el libro recomienda **la mitad** para cualquier perro adulto
   sano. ⚠️ Ojo con una frase que estuvo mal escrita aquí hasta el 9 de
   septiembre: **FEDIAF SÍ pone máximo de fósforo en adulto, 4,00 g/1000 kcal**
   (Tabla III-3b, «Adult: 4.00 (N)», nota h, y el texto de la sección 3.3.1).
   Se borró por error el 7 de septiembre y se devolvió la noche del 8. Un
   máximo de seguridad y una recomendación no son lo mismo, y este techo es lo
   segundo. Y ese número solo entraba antes por la puerta de atrás, en las dos
   patologías cuya tabla lo repite: el mismo perro pasaba de 4000 a 1750 por
   marcar «artrosis». Medido antes de aplicarlo: cabe en
   el peldaño 0 y en verde en 3, 10, 22 y 40 kg. **El techo del adulto no se
   aplica en crecimiento** — el mínimo de un cachorro joven (2250) está por
   encima del techo del adulto.
   **En crecimiento hay otros dos, y son del 9 de septiembre**: el calcio y el
   fósforo de la Tabla 17-1 de SACN5, que tiene **dos columnas** según el
   cachorro vaya a pesar más o menos de **25 kg de adulto** (cap.33: «large-
   and giant-breed puppies (>25 kg adult weight)»). Al pequeño, calcio 4250 y
   fósforo 3250; al grande, **2750 los dos** — el calcio apretado al 1,1 % de
   materia seca que pide Fascetti cap.10 «in order to prevent panosteitis»,
   dentro del 0,8-1,2 % de las Tablas 17-1 y 33-5. Existen porque hasta ese día
   un cachorro de raza grande recibía **4500 mg de calcio** (1,80 % MS), que es
   el máximo de FEDIAF y un **64 % por encima** de lo que dicen las dos fuentes
   caninas que hablan de esto; y porque **FEDIAF no pone máximo de fósforo en
   crecimiento** — las dos columnas de máximo de esa fila están vacías, y ahí
   el hueco sí es total: el adulto tiene el 4,00 de FEDIAF y el cachorro no
   tenía ninguno. Ojo con los dos umbrales: los
   **25 kg** de SACN5 no son los **15 kg** de la nota b de FEDIAF
   (`RAZA_GRANDE_O_GIGANTE_KG`), que decide otra cosa — el mínimo de calcio
   reforzado y el techo del ratio Ca:P. Dos fuentes, dos poblaciones, dos
   números. Lo vigilan los BLOQUES 57 y 62.
3. **Lo que se puede relajar es la FORMA, nunca la nutrición.** Cuando no
   existe menú, se sueltan las proporciones de BARF (hueso 20-60 %, etc.),
   que son criterio nuestro y no de FEDIAF. Nunca los requisitos ni la
   seguridad. Ver `_escalera_de_relajacion()`.
3-ter. **Un techo del LIBRO cede ante un suelo de FEDIAF, y se dice** (13 de
   septiembre). No es nuevo —`topes_de_la_etapa` lo hace desde el 8 de
   septiembre, y es lo que salva al perro a dieta— pero hasta hoy comparaba
   contra un suelo que NO es el que aplica el solver, y eso dejó a un perro de
   verdad sin comer. **CASO REAL, EN PRODUCCIÓN**: Cairo, el cachorro de Elena,
   American Staffordshire de casi 7 meses que pesará 31 kg de adulto, **no
   sacaba ningún menú en cuanto se declaraban premios**. Se cruzaban dos cifras
   de calcio y las dos son correctas: el **suelo 2500** de la nota b de FEDIAF
   (cachorro que pasará de 15 kg) contra el **techo 2750** de la Tabla 17-1 de
   SACN5 (el que pasará de 25 kg). Entre los dos hay un 10 % de sitio y los
   premios se lo comen, porque **suben el suelo y no el techo** (regla 3-bis).
   El suelo contra el que se mide un techo tiene que ser **el que de verdad se
   aplica** —`recomendaciones.suelo_que_de_verdad_se_aplica`: la fila escalada,
   MÁS la nota b, MÁS los premios—, y eso vale para el solver y para
   `_tope_patologia_roto` a la vez, con el MISMO `factor_premios`, o el filtro
   final tira menús que el solver construyó bien. Y el techo que cede **se
   dice**, en `techos_del_libro_que_no_se_aplican` del propio menú: la función
   que los contaba existía desde el 8 de septiembre con el comentario «el techo
   se cae, no en silencio» y **no la llamaba nadie**.
   ⚠️ **Y el techo no desaparece: SUBE hasta el suelo** (misma noche, y lo pidió
   Elena leyendo el arreglo: «pero a ver, ¿y no se puede dar un menú que cumpla
   el techo? seguro que sí»). Cumplirlo no se puede —el suelo está por encima,
   es aritmética— pero **quedarse pegado a él sí**, y la primera versión no lo
   hacía: el techo desaparecía y el menú se iba a 3746 cuando con 2778 le
   bastaba. La holgura con la que sube es `HOLGURA_DEL_TECHO_QUE_SUBE` = 1,02 y
   es **NUESTRA**, no de ninguna fuente: medido sobre tres cachorros de raza
   grande y dos niveles de premios, con 1,005 salen **0 de 6** y con 1,02 salen
   **6 de 6**. Y como es nuestra, **no puede dejar a un perro sin comer**:
   `resolver` prueba con el techo apretado y, si no sale menú, lo suelta y
   reintenta una vez — que es el comportamiento ya probado de antes. El calcio
   de Cairo pasa de 3746 a **2824**, o sea 922 mg menos al día y a un 2,7 % del
   consejo del libro en vez de a un 36 %. ⚠️ Y **el filtro final NO exige ese
   techo subido**: es un número nuestro, y rechazar un menú por pasarse de algo
   que nos hemos inventado sería darle rango de requisito — además de tirar
   justo los menús que el plan B existe para poder dar. Lo que cuesta está medido
   y **está sin decidir** en `PREGUNTAS_ABIERTAS.md` P-37b: con premios al 10 %
   ese cachorro sale con 3746 mg de calcio, dentro del máximo duro de FEDIAF
   (4500) y por encima del 2750 que las dos fuentes caninas piden justo para
   prevenir la panosteitis. Lo vigila el BLOQUE 101.
3-bis. **Lo que el perro come fuera de la ración se cuenta, no se ignora**
   (11 de septiembre). Los premios, las sobras de la mesa y los suplementos
   que da el dueño por su cuenta llegan por `kcal_de_premios` (el número) o
   `premios_nivel` (la respuesta elegida), y el motor **formula la ración con
   las kcal que quedan y le sigue exigiendo EL DÍA ENTERO de nutrientes**. No
   es simetría: de lo que lleva dentro un premio no sabemos nada, así que
   contar con él para cubrir un requisito sería darlo por cubierto sin
   saberlo. En números, los mínimos por 1000 kcal de la ración suben por
   DER/(DER − premios) y los máximos NO, que es exactamente la «dilución de
   nutrientes» que describe la fuente. **Cuidado con las dos medidas de kcal
   que conviven desde aquí**: `der` es el día entero y decide CUÁNTO
   nutriente hace falta; `der_racion` son las kcal de la ración y es contra lo
   que se escribe cada fila del solver. Escalar el suelo y usar `der` sería
   contarlo dos veces. Lo piden cuatro fuentes con la misma cifra —no más del
   10 % del día— y **FEDIAF lo dice también**, en su §4.1, que hasta el 11 de
   septiembre aquí ponía que no decía nada: «The total daily ration should
   match the recommended allowances and nutritional and legal maximum values
   listed in the tables for complete pet food». O sea que el día ENTERO
   —ración más premios— tiene que cumplir, que es exactamente lo que hace el
   motor. Y dice una cosa más que nosotros no afirmábamos: que **los máximos
   también se miden sobre el día entero**. El motor no los escala a propósito,
   porque de lo que lleva dentro un premio no sabemos nada, así que sigue por
   el lado seguro — pero eso es una decisión nuestra, no un hueco de FEDIAF. La
   pregunta y sus cuatro respuestas las sirve `GET /vocabulario` con los dos
   registros, y **de las cuatro cifras solo el 10 % es de la fuente**: el 5 %
   y el 20 % son nuestros y van marcados como tales. Lo vigilan los BLOQUES
   88, 87 y 95. ⚠️ **La ficha todavía no hace la pregunta**, y eso está
   declarado en `lo_que_la_ficha_todavia_no_pregunta` de
   `datos_de_la_ficha.json`.
4. **Las alergias y las categorías excluidas a mano no se tocan jamás.**
   Pueden ser médicas.
5. **Lo que eliges a mano se respeta, con un perro o con cinco.** Si la
   pantalla de Personalizar te deja elegir en una categoría, el motor no
   mete nada más de esa categoría. La lista de las que se respetan es
   `CATEGORIAS_QUE_ELIGE_EL_USUARIO` en `main.py`, y **tiene que coincidir
   con `CATEGORIAS` de `App.jsx`** — el día que dejen de coincidir, elegir
   en las que sobran no hará nada y nadie se enterará, porque el menú sale
   verde igual. Ya pasó: durante tres semanas se respetaban tres de las
   seis, y 15 de cada 36 menús personalizados metían algo que nadie pidió,
   callando.
   Dos matices que no son excepciones:
   · Una categoría que **no tocas** se queda en automático. No elegir
     pescado no es prohibir el pescado; para eso están las alergias.
   · Suplementos y Extras (sal, aceites, semillas, huevo) van siempre
     libres: no se eligen en ninguna pantalla y son la herramienta con la
     que el motor cierra los 43 requisitos.
   Y si con lo elegido no hay menú posible, se baja de peldaño y **se
   dice** — nunca se cambia en silencio. Eso incluye la pantalla de varios
   perros, que tenía esos avisos puestos a `null` a mano.

6. **NADA VIVE SOLO EN LA APP.** Ninguna lista que la app enseñe puede
   decidirse en la app: se pide al motor, y lo que vive en `App.jsx` es un
   **respaldo** para cuando Render duerme. Elena, 12 de septiembre: «NADA VIVA
   SOLO EN LA APP, TIENE QUE LLAMAR A COSAS QUE VIVAN EN EL MOTOR PARA QUE
   CUANDO SE CAMBIE ALGO SE APLIQUE Y LA APP LO PILLE DIRECTO. PARA TODO».
   La cadena es **FUENTE manda → MOTOR la implementa → APP la ofrece**.

   ⚠️ **Esta regla ya estaba dicha y se seguía rompiendo, y por eso ahora se
   ejecuta**: una frase no se ejecuta, que es la lección de
   `auditar_conversiones.py`. Cinco veces el mismo fallo en dos semanas — las
   seis categorías de Personalizar, los cinco niveles de actividad, las 47
   patologías, las 255 razas y los 163 alimentos — y las cinco se descubrieron
   **por casualidad**, porque una lista copiada a mano no da error: se queda
   parada y la pantalla se ve perfecta. El caso que la cerró: el aceite de
   salmón Pets Purest entró al catálogo el 7 de septiembre con la foto de su
   etiqueta, el motor lo usa en 23 de los 216 menús precalculados, y en la app
   no aparecía. Medido: la lista de la app tenía **exactamente** los mismos
   alimentos que el motor menos ese.

   El inventario es `lo_que_la_app_pinta.json`: **25 listas** (eran 14 el 12 de
   septiembre; las once que faltaban entraron el 13), cada una con su
   endpoint, el camino dentro de la respuesta, el fichero del motor donde vive
   el dato y el nombre de su constante de respaldo. Se vigila por **las dos
   puntas, y hacen falta las dos** — una lista puede estar declarada y no
   servirse, o servirse y no estar declarada: el **BLOQUE 99** exige que el
   endpoint declarado sirva esa lista de verdad y no vacía, y
   `tests/la-ley-del-motor.spec.js` en `canislab-web` exige que toda constante
   `*_RESPALDO` de `src/` esté declarada. Una lista nueva escrita a mano falla
   al escribirla, que es el único momento en que se puede cazar.

   Y una tercera cosa que ninguna de las dos puede ver: **que la app USE lo que
   lee**. Eso es de cada prueba, y la forma de hacerlo es sembrar nombres
   **inventados**, porque con los de verdad «la app lo ha leído del motor» y
   «la app está pintando su respaldo» se ven exactamente igual.

## El mapa: qué es cada archivo

Escrito el 26 de agosto porque no existía y hacía falta. Con 10.000 líneas
de Python repartidas en dos carpetas, «¿dónde toco esto?» se respondía
leyendo hasta encontrarlo, y hay dos motores en el repo — uno vivo y uno
jubilado — que desde fuera se parecen mucho.

### El motor de verdad (`motor/`)

| Archivo | Qué hace |
|---|---|
| `motor_completo.py` | **El corazón.** `resolver()` monta el problema MILP y lo resuelve: los 41 nutrientes (los 12 aminoácidos entre ellos desde el 28 de agosto), el ratio Ca:P y los topes de seguridad como restricciones simultáneas. Aquí vive `topes_de_patologias()`, que resuelve los topes para una etapa y una combinación de patologías — pero **la tabla ya no está aquí**: se importa de `patologias.py`. Y desde el 10 de septiembre `ratios_de_patologias()`, su hermana para los cocientes: una patología puede pedir su propio ratio entre dos nutrientes (bloque `ratios`), y se combina con el mismo criterio que todo lo demás — el suelo con `max()`, el techo con `min()`, o sea que solo puede apretar |
| `verificar.py` | El semáforo. `MAPA` es **la** lista de requisitos, la única, compartida con el solver y con el analizador. Y `suplementar()`, que cierra huecos |
| `seguridad.py` | Los cinco topes crónicos y los avisos. Cada cifra con su fuente escrita al lado |
| `constructor.py` | Proporciones BARF de partida y `valor_nutriente()` (las claves derivadas, como `epa_dha`) |
| `exclusiones.py` | Alergias por palabras y familias de especie. Excluir «pollo» quita también «gallina» |
| `accesibles.py`, `modos.py` | Qué alimentos entran según el modo (automático / personalizar / aprovechar). ⚠️ **De `modos.py` el motor usa UNA sola cosa**, el diccionario `CUANTOS_MAX`: `elegir_alimentos`, `cambiar`, `quitar` y `anadir` no los llama nadie —los tres endpoints tienen su propia implementación en `main.py`— y **no hay ningún sorteo de candidatos**: `resolver()` ve todos los accesibles y elige el MILP. Está escrito aquí porque el 10 de septiembre un pendiente llevaba días culpando a `elegir_alimentos` de que al toy de 1,5 kg le costara sacar menú, y la causa era el `time_limit` |
| `condicionales.py` | Lee `requisitos_condicionales.json`: **los requisitos que NO son un número fijo porque dependen de la propia dieta**. Son **seis** desde el 9 de septiembre: **tres que se aplican** y **tres escritas sin cifra**, porque FEDIAF las enuncia y no las cuantifica para el perro. (1) La proteína de **gestación y lactancia**, que FEDIAF calcula suponiendo que la dieta lleva hidratos — y una ración BARF no lleva; NRC trae el experimento: con la dieta sin hidratos y la proteína baja, la **mortalidad perinatal subió un 75 %**. (2) La **arginina que sube con la proteína**: FEDIAF publica una tabla entera para esto (Anexo 7.4 y Tabla VII-13, «+0,01 g de arginina por cada gramo de proteína sobre el requisito, en todas las etapas») y no la aplicábamos — con los 105 g/1000 kcal de proteína que lleva un BARF típico, la tabla pide 1,90 g de arginina y el motor exigía 1,51. (3) El **ratio linoleico:linolénico**, 2,6-26 en adulto y crecimiento y 2,6-16 en gestación y lactancia (NRC 2006 cap.5) — que es lo que el NRC recomienda **en lugar** del ratio omega-6:omega-3 totales, del que dice literalmente que «is not helpful». Ninguno de los tres tiene forma de fila, así que ninguno lo encontró el trabajo de transcribir tablas. || Y las **tres que NO se aplican**, con `tipo: documentado_sin_cifra`: la **vitamina E sube con los PUFA**, la **B6 sube con la proteína** y la **K en dietas con mucho pescado**. Las tres las nombra FEDIAF en su sección 3.3 y de las tres da número solo para el GATO o para ninguno, así que aplicarlas sería inventarse la cifra. Están escritas para que se puedan auditar y para no volver a «descubrirlas» dentro de seis meses; el BLOQUE 60 vigila que sigan inertes. Medido: por la relación clásica de vitamina E:PUFA (≥0,6 mg/g) vamos holgados —0 de 216 menús por debajo, el peor a 1,53— y la B6 real va de tres a doce veces el mínimo de FEDIAF. **El solver y el semáforo llaman a las mismas funciones de este módulo**, y eso no es elegancia: es la lección del 8 de septiembre, cuando cada uno aplicaba los suelos de patología a su manera y el motor construía menús enteros para que el filtro final los tirara |
| `recomendaciones.py` | Lee `recomendaciones_libro.json`: **lo que el libro recomienda al perro SANO**, por etapa. Es la tercera clase de límite del motor, y no existía hasta el 8 de septiembre: los de FEDIAF valen para cualquier perro, los de patología solo si está marcada, y estos valen para el perro que **no tiene nada**. Empezó con dos techos de adulto (fósforo y sodio) y el 9 de septiembre entraron los de **crecimiento** — calcio y fósforo, con **dos columnas** según el cachorro vaya a pesar más o menos de 25 kg de adulto. ⚠️ **Y el 11 de septiembre dejó de ser solo de techos**: guarda también **suelos**, con `max()`, porque una recomendación del libro que fuera un mínimo no tenía dónde vivir. El único escrito es la **vitamina E** del perro sano, que SACN5 pide en ≥400 UI/kg MS (67,1 mg/1000 kcal) en **cinco capítulos** y que el motor exige a cuatro PATOLOGÍAS y no al perro sin nada. **Está ESCRITA y APAGADA** (`aplicado_por_el_solver: false`), y lleva **dos decisiones de Elena del mismo día**: encenderla por la mañana («la norma es la norma») y apagarla por la tarde («apágalo y fusiona todo, ya preguntaremos lo de la vitamina E»). Lo segundo es el ORDEN y no la norma: encendida pone roja la batería en los BLOQUES 9 y 43, y estaba reteniendo 150 commits que no tienen nada que ver con ella. Lo que cuesta: los tres perros con ocho especies fuera se quedan sin ninguno, y al toy de 1,5 kg le cuesta tanto que el solver no lo saca en 1 s ni en 20 intentos (sin el suelo, 12 de 20). Por la API, con la escalera, el toy sí sale 10 de 10. Las medidas completas están arriba, en la regla 2. La causa es de DATOS: **no hay un suplemento de vitamina E suelto en el catálogo**, solo los nueve multivitamínicos y el motor deja meter dos. La cifra NO se baja — se queda escrita con su medida y se pregunta. ⚠️ Y **tres de los seis fallos que dio al encenderla no eran suyos**: el motor metía comida que nadie pidió sin avisar en la pantalla de varios perros, y eso era un fallo de verdad (el perro que se amolda heredaba el menú del primero y no su aviso), arreglado el 11 de septiembre. **Y aquí manda FEDIAF**: si un suelo del libro se pasara del máximo de FEDIAF, el suelo se cae. El BLOQUE 57 vigila las dos cosas: que siga apagada con su motivo escrito, y que la maquinaria funcione (la enciende a mano y exige que solver y filtro final la apliquen) |
| `patologias.py` | Lee `patologias.json` y lo pasa a la forma que espera el solver. **Aquí no hay ni una cifra**: hasta el 28 de agosto la tabla eran 200 líneas de `dict` dentro de `motor_completo.py`, mezclando números, motivo clínico, textos y lógica de crecimiento. Se sacó por lo mismo que el catálogo y la tabla de FEDIAF: un número que decide si un menú se entrega tiene que poder auditarse, y no se audita lo que está enterrado entre `if`s |
| `catalogo_menus.py` | Carga los menús precalculados de la vista previa. Los datos están en `catalogo_menus.json`, en la raíz con los demás: aquí solo quedan 55 líneas de código |

### La API (raíz)

| Archivo | Qué hace |
|---|---|
| `main.py` | FastAPI: todos los endpoints, el presupuesto semanal de seguridad crónica y `_garantizar_verificado()`, por donde pasa **todo** menú antes de salir |
| `requerimientos_v2_final.json` | Los requisitos de FEDIAF. **43 filas, y desde el 28 de agosto se verifican las 43**: los 41 nutrientes de la Tabla III-3b (los 12 aminoácidos incluidos), el ratio Ca:P y el calcio de raza grande. Con **una** excepción escrita y probada: el techo de lisina — ver abajo |
| `requisitos.py` | Cargar la tabla de FEDIAF, resolver la etapa y la dosis máxima que marca el fabricante de cada suplemento. Era `optimizador.py`, 1.124 líneas donde esto convivía con el motor anterior al MILP y con una copia desincronizada de la tabla de patologías. El motor viejo se borró el 26 de agosto; quedan 121 líneas |
| `der.py` | Cálculo de las kcal. ⚠️ Ver «la duplicación que hay que vigilar (DER)», abajo |
| `analizador.py` | `/analizar`: la dieta que ya le da el dueño. Comparte `MAPA` con el semáforo a propósito — discreparon una vez por la fibra. ⚠️ **Y volvieron a discrepar el 11 de septiembre, en la etapa**: es el único que llama a `requisitos.resolver_etapa`, que mandaba gestación y lactancia a `CachorroCrecimiento` (Late Growth) mientras `verificar.EQUIVALENCIA` las mandaba a `CachorroJoven`. La buena es la segunda: la cabecera de la Tabla III-3b dice literal «Early Growth (< 14 weeks) **& Reproduction**». O sea que la dieta de una perra preñada se comparaba contra requisitos hasta un **38 %** más bajos (leucina 3,23 → 2,00, fósforo 2250 → 1750, proteína 62,5 → 50) y salía **en verde**. Dos tablas para lo mismo, en dos módulos, y ninguna comprobaba a la otra. Lo vigila ahora el BLOQUE 89, clave a clave |
| `especies.py`, `accesibles.py` | Qué especie es cada alimento |
| `transicion.py` | Plan de cambio gradual de dieta |
| `persistencia.py`, `observabilidad.py` | Supabase y Sentry |
| `pruebas_completas.py` | **La batería.** Los 100 bloques, ~40 min. Es lo que se ejecuta entero antes de entregar cualquier cambio (ver «Cómo se prueba») |
| `datos_de_la_ficha.json` | **Los 21 campos que la ficha pregunta, y CÓMO llega cada uno al motor** (11 de septiembre). Nació de una frase de Elena: «TODOS LOS DATOS QUE RECOJA LA APP TIENEN QUE LLEGAR DE ALGUNA MANERA AL MOTOR, SI NO SON DATOS INUTILES Y CUANDO SE PIDEN ES SIEMPRE POR ALGO». Y tiene un caso que lo justifica solo, del mismo día: la ficha pregunta la **actividad** desde siempre, la app la usaba para calcular las kcal y mandaba solo el número — el motor veía 1955 kcal y no sabía si era un galgo de sofá o un perro de trineo, que es justo lo que decide si se le aprietan los topes crónicos por peso metabólico. Hay tres formas de llegar: `campo` (viaja suelto), `dentro_de` (va cocinado dentro de un número que sí viaja, y entonces **hay que escribir qué se pierde por ir así**) y `no_hace_falta` (con su motivo, que tiene que ser un motivo y no una excusa). Lo vigila el BLOQUE 87. ⚠️ Eran 20 y faltaba `raza`: la lista se copió a mano de `tests/ficha-ida-y-vuelta.spec.js`… donde `raza` tampoco estaba, porque su perro de ejemplo era un mestizo y `null` vuelve como `null` aunque se pierda. Dos inventarios copiados a mano, el mismo hueco en los dos |
| `niveles_de_actividad.json` | **La Tabla VII-7 de FEDIAF fila por fila**, con lo que hace el motor y lo que ofrece la app (11 de septiembre). Cinco filas emparejadas, una **partida por nosotros** (el rango «High activity 150-175» es UNA fila de la fuente y el motor la parte en dos niveles), una fuera a propósito (los perros de trineo, 860-1240) y un **HUECO** declarado: «Obese prone adults ≤ 90» no está ni en el motor ni en la app. Lo vigila el BLOQUE 88 |
| `preguntas_por_patologia.json` | **Qué pregunta decide la cifra de cada patología, qué respuestas tiene, y a qué clave del motor lleva cada una** (11 de septiembre). Nació de una frase de Elena: «tendrá que haber preguntas para cada patología preguntando resultados de analíticas o lo que sea para que pueda coger según la respuesta los límites para cada estadio o cada caso». ⚠️ **Y lo primero que hay que saber al abrirlo es que la mitad ya estaba hecha**: la cardiopatía tiene **cinco claves con cinco techos de sodio** (`cardiopatia_c` 625, `cardiopatia_d` 480) y la app **ya pregunta el estadio ACVIM**. Cuatro de las diez están `aplicada`. Aquí no hay ni un número escrito: se **derivan** de `patologias.json`, y donde el motor no tiene una clave por respuesta se dice en vez de inventarla. Cinco estados, y el que importa es **`no_cambia_ninguna_cifra`**: una pregunta cuyas respuestas aplican exactamente lo mismo no decide nada — se le pide un dato clínico a quien firma y da igual lo que conteste. Hoy le pasa a `shunt_sin_encefalopatia`. Lo vigila el BLOQUE 90, que además exige que **cada `requiere` de un tope condicional apunte a una patología que exista**: el de la diabetes decía `hipertrigliceridemia`, que no es ninguna de las 47, así que ese techo **no se aplicaba nunca** por esa puerta — el solver lo resuelve con `any(otra in lista ...)` y un nombre que nadie puede marcar no entra jamás, con el menú saliendo verde igual. ⚠️ **Y desde la noche del 11 comprueba las 19 respuestas, no solo las cinco de la cardiopatía**: cifra a cifra, techos con `min()` y suelos con `max()`, contra lo que devuelve `topes_de_patologias` — que es la función que llama el solver. Son 28 cifras, y de 14 de ellas nadie comprobaba que contestar una cosa u otra cambiara nada. Y las dos direcciones: un tope que el solver aplica y la respuesta no dice es una restricción que quien firma no ve, y que puede dejar al perro sin menú sin que se sepa por qué. ⚠️ **La lista la lee ahora la app de `GET /vocabulario`** y no de su propia `FAMILIAS_PATOLOGIA`, que queda de respaldo — y `segura` se deriva del `_no_formulable` que dice el motor, que era el riesgo escrito en `App.jsx` desde agosto. Lo vigila `tests/puerta-veterinario.spec.js` sembrando un estadio **inventado** |
| `patologias_como_se_presentan.json` | **Cómo se le ENSEÑA cada patología a quien la marca: en qué aparato va y cómo se llama sin jerga** (12 de septiembre). Nació de una frase de Elena: «COMPRUEBA TODO PARA QUE NINGUN DATO LO MANDE LA APP, TODO TIENE QUE VENIR DEL MOTOR». Hasta ese día las 47 etiquetas y los nueve grupos por aparato vivían dentro de `src/App.jsx`, escritos a mano — la misma forma de fallo que las seis categorías de Personalizar y que los cinco niveles de actividad contra los tres de la base de datos: una patología nueva en `patologias.json` no aparecía en ninguna pantalla y no saltaba nada. ⚠️ **Aquí no hay ni un número, y casi nada es nuevo**: el nombre técnico es el `nombre` de `patologias.json` (y es el registro del veterinario), el `formulable` también, quién puede marcarla sale de `quien_formula_cada_patologia.json` y el aviso es el `avisos.general` que ya sirve `GET /patologias`. Lo único que no existía en ningún sitio son dos cosas: **cómo se le dice al dueño** y **en qué aparato va**. `GET /vocabulario` lo sirve todo junto en `patologias.lista` y `patologias.por_aparato`, y **las doce que no llevan casilla propia se DERIVAN**, no se escriben: son las respuestas de las familias que sustituyen a su cabecera (los cinco estadios ACVIM, la renal avanzada, los cuatro urolitos que no son estruvita, la predisposición al cobre y la encefalopatía) — ponerles casilla sería la misma patología dos veces en la misma pantalla. Lo vigila el BLOQUE 105 (era el 98, luego el 102, y hubo DOS con cada número: ver su cabecera), y `tests/patologias-del-motor.spec.js` en `canislab-web` sembrando etiquetas **inventadas**, porque con las de verdad «la app lo ha leído» y «la app pinta su respaldo» se ven igual |
| `razas.json` + `razas.py` | **Las 270 razas que ofrece la ficha**, con su tamaño y su rango de peso adulto (11 de septiembre). Hasta ese día vivían **solo en `src/App.jsx`** del repo de la app: 255 filas dentro del JavaScript, sin nadie que las mirara. El motor no las tenía, así que no podía comprobar ni lo más básico — que el tamaño que manda la app sea uno de los **seis** con los que `catalogo_menus.json` indexa sus menús, o que las tres listas de razas de `der.py` escriban los nombres **exactamente** como los escribe la app. ⚠️ Eso último es lo que más calla: `der.py` reconoce al Gran Danés y al Terranova **por su nombre literal** para darles su cifra propia de FEDIAF (200 y 105 kcal/kg^0,75, que van EN VEZ del nivel de actividad), y una tilde distinta y esa cifra no se aplica nunca, sin error y con el menú en verde. Ya pasó en el otro repo: el Supabase de mentira sembraba «Pastor alemán» con a minúscula, que no existe en la lista, así que durante meses todas las pruebas que usaban ese perro corrieron contra un mestizo con nombre de raza. ⚠️ **Estas cifras NO TENÍAN fuente publicada** —ninguna de las cuatro fuentes del motor trae una tabla de peso por raza—, y el 12 de septiembre la ganaron **85 de las 270**: **20** del BOE (Real Decreto 558/2001, los prototipos de las razas españolas, que es LEY) y **65** del estándar oficial de la **FCI**, que es el único documento que dice raza por raza lo que pesa. Las otras 185 siguen sin ella y eso sigue escrito en su `_meta` y en `DATOS_QUE_FALTAN.md`. ⚠️ **Y lo que hay que saber antes de tocar una de esas cifras es que no todo estándar da un RANGO**: «Mínimo, 40 kg para las hembras» y «Hembras: 40 – 50 kg» tienen los mismos dígitos y no dicen lo mismo, así que cada fila lleva su `forma_de_la_fci` (rango · punto · punto_sexo · minimos · maximo · solo_machos) y **solo el rango sustituye a nuestra cifra** — de un punto no se inventa una horquilla alrededor, que es por lo que el Setter Gordon sigue en 20-36 aunque la FCI diga 29,5 en machos. ⚠️ **Y ese rango YA NO ACOTA las kcal** (12 de septiembre, noche). Hasta esa noche recortaba el peso adulto que la curva le proyecta a un cachorro, y de ahí salen sus kcal. Se quitó tras mirar cómo lo hacen los demás: las curvas de **WALTHAM** —las que publica Royal Canin para veterinarios— sacan el peso adulto de la trayectoria del propio cachorro y usan el estándar de raza **solo para elegir la banda**, y **MyVetDiet**, con tabla de más de 180 razas, la llama «pesos indicativos». Medido antes de tocarlo: el recorte movía 47 de 1620 casos, mediana 3,0 % de kcal y 6,9 % el peor, y casi siempre **hacia arriba** en cachorros que apuntan por debajo del mínimo de su raza — al Mastín Español de 9 meses le añadía 152 kcal al día, y es un cachorro de raza gigante, justo donde FEDIAF avisa de deformidades esqueléticas por sobrealimentar. Hoy la tabla sirve para el peso de **respaldo** cuando no hay edad ni peso con los que calcular, y para lo que se le **enseña** al dueño. Lo vigilan el apartado 9 del BLOQUE 96 y `tests/der-contrato.spec.js`. Lo que sigue abierto es el **sexo**: la FCI da machos y hembras por separado en la mitad de sus estándares y aquí se guardan juntos (P-36). Y el BLOQUE 89 **rehace cada peso contra su cita** |
| `alimentos_como_se_presentan.json` + `lo_que_la_app_pinta.json` | **La regla 6, con sus dos ficheros** (12 de septiembre, noche). El primero dice **cómo se le ENSEÑA el catálogo a quien lo mira**: las ocho pantallas, qué categoría del motor va en cada una y cómo se agrupa por dentro. Aquí **no hay ni un alimento** — salen de `alimentos_v3_final.json`, y el segundo nivel se DERIVA: la especie que el motor ya usa para las alergias en las seis categorías de comida, la propia categoría en los suplementos, y solo los 23 Extras llevan su grupo escrito porque «Huevo» o «Semillas» no se pueden sacar de ningún sitio. ⚠️ `GET /alimentos` mandaba `especie: null` en los 163 porque leía una clave que las fichas no tienen; el motor SÍ la sabe. El segundo fichero es **el inventario de la ley**: las **25** listas que la app pinta, con su endpoint y su respaldo — eran 14 ese día; las once que faltaban se trajeron el 13 de septiembre, y las **tres** que quedan declaradas como «faltan por traer» son a propósito: `ACTIVIDAD_KEY`, `BASE_ACTIVIDAD` y `CURVA_FEDIAF_VII_8A` son la parte de actividad y de curva del CÁLCULO DEL DER, que se hace en la app porque hacerlo en el motor sería una llamada de red por cada tecla, y es la duplicación ya declarada de `der_casos.json`. Lo vigilan el BLOQUE 99 y `tests/la-ley-del-motor.spec.js`, comprobado con una lista sin declarar |\n| `nutrientes_como_se_presentan.json` + `bcs_tabla_VII_1.json` | **Las dos listas de la app que quedaban por traer, y las dos venían de la misma forma de fallo** (13 de septiembre). La primera dice **cómo se AGRUPAN los nutrientes al leer una ficha** y en qué orden: aquí no hay ni una cifra, solo en qué grupo va cada fila. Vivía en `GRUPOS` de `src/nutrientes.js` con **42** nutrientes escritos a mano, y el motor sirve **46** más **dos relaciones** (Ca:P y linoleico:linolénico), o sea 48 filas posibles — las seis que faltaban (Fibra, Taurina, L-carnitina, EPA, omega-3 totales y la relación linoleico:linolénico) caían en el cajón **«Otros»**. Y ese cajón está puesto a propósito —se prefiere un grupo feo a un nutriente escondido—, que es justo por lo que no se enteró nadie: «Otros» se ve, no da error, y ahí llevaban esas seis desde que existe la ficha. **Un cajón de paso que se vuelve permanente deja de avisar.** || La segunda es **la Tabla VII-1 de FEDIAF**: cómo se RECONOCE cada punto de condición corporal, mirando y palpando. ⚠️ **No es la VII-2**, que ya estaba en el motor: aquella dice CUÁNTO se desvía del peso ideal cada punto —de ahí salen las kcal— y esta dice **qué número escribe quien está delante del perro**, que es el que entra en esa cuenta. Vivía en `ESCALA_BCS` de `src/bcs.js`, escrita a mano y **sin fuente**, siendo una paráfrasis de una tabla que FEDIAF publica entera. Trae las dos mitades: la frase **literal** de FEDIAF en inglés —las 26 las comprueba `auditar_citas.py` contra el texto del PDF— y nuestra traducción para la pantalla, marcada como nuestra. ⚠️ Y el 8 y el 9 **no tienen «abdomen»**: FEDIAF cambia esa casilla por «general», y va declarado para que nadie lo rellene «por simetría». Los vigila el BLOQUE 99 |
| `auditar_patologias.py` | Cada cifra de `patologias.json` contra `requerimientos_v2_final.json`: que ninguna patología formulable tenga un tope por debajo del mínimo de FEDIAF, y que la clave del nutriente exista en el `MAPA`. Lo ejecuta el BLOQUE 32 |
| `quien_formula_cada_patologia.json` | **Quién puede marcar cada una de las 47, y qué falta preguntar** (10 de septiembre). No es una opinión de producto: cada línea sale de la **cita de la propia fuente de esa patología**. Si su tabla condiciona la cifra a un dato clínico —el estadio IRIS que decide el techo de fósforo, los triglicéridos que bajan la grasa de 37,5 a 25, la taurina en sangre—, entonces **no la puede marcar quien no tiene ese dato**, y la pregunta que falta en la ficha es la que hace falta para elegir el número. Salen **24 `solo_veterinario`**, 18 `dueno_con_diagnostico`, 5 `dueno` y **8 preguntas que la app no hace**. Lo vigila el BLOQUE 79, que además exige que una patología declarada sin dato clínico no tenga marcadores de analítica en su propio JSON — y cazó tres contradicciones mías nada más escribirlo |
| `limites_legales_ue_2020_354.json` + `auditar_margen_profesional.py` | **Hasta dónde puede mover un veterinario cada cifra, y hasta dónde no** (10 de septiembre). La respuesta ya estaba escrita y ese era el problema: en **prosa**, dentro del campo `por_que` de cada cifra («Margen del profesional: 13,75 a 37,5») y en el §2 de `PATOLOGIAS.md`. Una frase no se ejecuta — la lección de `auditar_conversiones.py` otra vez —, y las dos que había ya estaban caducadas: la de la pancreatitis citaba el margen de antes del tope condicional, y **el sodio cardíaco aplicaba 739 con su propia celda citando el techo LEGAL en 738,6**. Ahora cada una de las **79 cifras** lleva un bloque `margen_profesional` con su suelo, su techo y **de dónde sale cada uno** —una clave de procedencia, no un número copiado: `minimo_fediaf:Fósforo`, `legal_ue:24_cardiaca:sodio`, `seguridad:TOPE_VITD_KCAL`, `sin_techo`—, y el auditor **rehace las 79 ventanas** contra la fuente viva. El JSON nuevo son **las 20 entradas caninas del Reglamento (UE) 2020/354**, que es la única fuente del repo que es **ley** y por tanto la única que pone un techo del que no se sale nadie. ⚠️ Y hay que citarlo con cuidado: el Reglamento **no da un rango de maniobra por nutriente** —da un techo o un suelo por objetivo—, y su ±15 % es **tolerancia analítica de etiquetado**, no margen clínico. Lo ejecuta el BLOQUE 80, que además exige que `GET /patologias` sirva las 79 ventanas |
| `auditar_citas.py` | **Que cada cita entrecomillada diga lo que dice la fuente** (10 de septiembre). Nació del fallo de las dos columnas: FEDIAF y SACN5 se habían extraído del PDF conservando la disposición visual, y los dos libros van a dos columnas, así que el **49,3 %** de las líneas de FEDIAF y el **37,5 %** de las de SACN5 pegaban la línea de la izquierda con la de la derecha. Durante días se pudo citar de buena fe, entre comillas, una frase que **la fuente no dice**. Saca las **783 citas de más de 40 caracteres** de cuatro documentos y seis ficheros de datos, y busca cada una **literal** en los 98 textos de fuente del repo de al lado, normalizando lo que es nuestro y no de la fuente (negritas, el `>` de cita, los ocho guiones de Unicode, los superíndices, el separador de miles). Hoy: **759 encontradas literales** y **24 que citan una fuente que no está en el repo** (Merck, el consenso ACVIM, IRIS en PDF, Purina) y por tanto **no se pueden comprobar aquí, y se dice**. Los tres recuentos van **clavados y comparados exacto** — no solo el de las que hay que mirar: con uno solo, una cita mal copiada podía esconderse cambiando de casilla, y **pasó** (46 citas vivían en «no dice de dónde sale», y 15 eran la misma frase de FEDIAF copiada mal en 14 filas de `requerimientos_v2_final.json`, con una condición borrada). ⚠️ Y «no encontrada» **nunca significó falsa**: las 31 que quedaban se abrieron una a una contra el libro y las 31 estaban ahí — lo que fallaba era cómo se habían copiado (una abreviatura metida dentro de las comillas, un punto fuera de ellas, un «12 a 15» donde el libro pone «12 to 15», una cita del estudio que era de la frase de al lado). ⚠️ **AMPLIADO EL 12 DE SEPTIEMBRE, y encontró seis citas mal copiadas el mismo día.** Hasta entonces no miraba `LECTURAS.md` ni `PREGUNTAS_ABIERTAS.md`, que son los dos ficheros donde **más** se cita literal — el método es leer y anotar la frase de la fuente al lado — y que habían nacido después de esta lista. Al meterlos salieron seis: una abreviatura metida dentro de las comillas («blood creatinine or SDMA» donde IRIS escribe «symmetric dimethylarginine (SDMA)»), una condición borrada por una elipsis («but not less than 0.9 mmol/l; > 2.7 mg/dl», que se comía el «<4.6 mg/dl but»), dos con mis mayúsculas dentro de la cita, una cortada a media palabra, y los decimales de FEDIAF pasados a coma española dentro de las comillas. Ninguna cambiaba una cifra del motor y las seis son exactamente lo que este auditor existe para encontrar. || Y ahora indexa también **los textos de fuente que viven en ESTE repo**, no solo en el de al lado, porque las tablas de AAHA 2021 **no se pueden extraer de su PDF**: están dibujadas como trazos vectoriales y la página de la Tabla 8 entera devuelve 194 caracteres. Ver `aaha_2021_tablas_transcritas.txt`, y **los .xml**, porque Hofmann 2025 —uno de los dos estudios con los que el repo justifica lo del fósforo— vive solo como XML de PubMed Central y sus citas no se podían comprobar. || Y **tres fallos del propio auditor**, los tres del mismo día y los tres de la misma familia —dar por incomprobable algo que sí se podía comprobar—: el **guion blando** (U+00AD), que el PDF de Ishii trae 100 veces y que hace que la misma palabra no sea la misma cadena; que **«purina» casaba dentro de «purinas» y de «purine»**, así que cualquier frase sobre purinas se atribuía a la marca Purina y se iba a la casilla de las que no se pueden mirar; y que una clave de dos palabras no casaba si el Markdown la partía con un salto de línea. || ⚠️ **Y el cuarto, que estaba anotado y sin decidir**: este auditor solo miraba las citas **en inglés**, con el motivo escrito de que «las fuentes están todas en inglés». Dejó de ser verdad el día que entró **Ettinger & Feldman**, que son 255.458 líneas **en español**, y su propio LÉEME lo dejó apuntado «para decidirlo». Desde el 12 de septiembre una cita en español se audita **si su párrafo nombra una fuente que está en español**. La regla es estrecha a propósito: auditar toda cita española cuyo párrafo nombre cualquier fuente acusaría, una detrás de otra, a las frases de Elena y a nuestra propia prosa entrecomillada, y una auditoría que acusa a quien no ha hecho nada se deja de mirar. Comprobado con el fallo puesto: una cita inventada de Ettinger salta. || ⚠️ **Y ESA REGLA, TAL CUAL SE ESTRENÓ, NO AUDITABA CASI NADA** (12 de septiembre, por la tarde). Esa misma tarde entraron ~100 citas nuevas de Ettinger y el recuento subió **en una**. Tres motivos, los tres de la misma forma —mirar demasiado cerca—: (1) **el párrafo de una fila de tabla es la tabla**, que empieza en «| Lo que dice | Qué hacemos |» y no nombra a nadie, y el método de lectura escribe los hallazgos en tablas; ahora se mira además el **título Markdown** más cercano. (2) Y hay que mirar **dos** títulos, no uno: el cercano es el capítulo («### cap.178, Debra Zoran…») y quien nombra la fuente es el `##` de arriba. Con solo el cercano se auditaban 3 de 50. (3) Y se preguntaba si la **primera** fuente que aparece está en español, cuando `_quien_dice` devuelve una sola y **un párrafo que compara dos fuentes nombra a las dos**: la P-32 enfrenta a SACN5 con Ettinger, salía «sacn5», y sus ocho citas de Ettinger no se miraban — que es justo la clase de párrafo donde más importa. Con las tres arregladas se pasa de **1.648 a 1.795 citas auditadas**, y aparecieron **siete mal copiadas** el mismo día: dos que eran **prosa mía** entrecomillada como si fuera de la fuente, una que era **nuestro propio campo `por_que`**, un «en general» donde el libro pone «por lo general», una cita empezada a media frase que se comía un paréntesis («el 95 %)»), y dos fallos del auditor —el `[...]` que `_norm` borraba antes de poder usarlo como separador, y el orden de esa alternancia—. Comprobado otra vez con el fallo puesto, ahora dentro de una tabla. || ⚠️ **Y un efecto de esa regla que hay que conocer: dentro de un apartado de Ettinger, una frase de Elena entre comillas angulares sale acusada** — claro que no aparece en el libro, no es de un libro. La salida NO es añadir «si cerca pone Elena, no se mira»: probado y **medido, eso se salta 26 citas**, y entre ellas hay de SACN5 y de FEDIAF de verdad, porque el párrafo que recoge una frase suya suele traer al lado la cita de la fuente de la que están hablando. Silenciar una cita de fuente es peor que acusar una frase de Elena. La salida es la barata: **sus palabras no van entre « » dentro de un apartado de una fuente en español**; van donde ya viven, en `PREGUNTAS_ABIERTAS.md` y en `HECHO.md`, y desde el apartado se apunta ahí. Lo ejecuta el BLOQUE 85 |
| `radiografia.py` | Imprime los números que **ENTRAN** al motor, para comparar `main` con una rama a golpe de `diff`. No lo ejecuta la batería: se corre a mano. Existe porque el semáforo comprueba el menú contra las kcal que le dieron — si las kcal ya venían mal, el menú sale VERDE para un perro que no es el tuyo, y eso solo se ve en la entrada |
| `auditar_catalogo.py` | Huecos y datos raros del catálogo, y quién se queda sin aminograma. Lo ejecuta el BLOQUE 19 |
| `regenerar_catalogo.py` | Rehace los 36 menús de la vista previa y sus 180 variantes. **Está en el repo por un fallo real**: el 8 de septiembre se regeneró el catálogo con una copia de este script que vivía en un scratchpad y que llamaba al motor **sin `margenes_categoria`** — el motor formula sin proporciones BARF, y salieron menús de **25,8 kg de comida al día con un 91 % de verdura y sin hueso**, los 216 **en verde**, porque lo que se había apagado no era la nutrición sino la FORMA, y la forma no la mira el semáforo. No llegó a `main`. Desde el 9 de septiembre el script vive aquí, hace la misma llamada que la API, y **el BLOQUE 25 comprueba las proporciones de los 216 menús** |
| `auditar_fediaf.py` | Cada valor del JSON contra la tabla de FEDIAF. Lo ejecuta el BLOQUE 18. ⚠️ Su tabla de FEDIAF está **transcrita a mano dentro del propio archivo**, y quien la audita a ella es el de abajo |
| `auditar_transcripcion_fediaf.py` + `fediaf_tabla_III_3b.txt` + `fediaf_tabla_VII_14.txt` | **Quién audita al auditor** (10 de septiembre). La cadena era: PDF → transcripción a mano dentro de `auditar_fediaf.py` → `requerimientos_v2_final.json`. El segundo tramo estaba vigilado desde el 25 de agosto y el primero no, que es el que decide todo: con un valor mal transcrito el JSON «cuadra», la batería sale verde y **todos** los menús cumplen bien un requisito equivocado — y el motor no tiene el PDF, así que no puede cazarlo. Ya pasó, y no con un dígito: la transcripción se había saltado **los doce aminoácidos enteros**. El `.txt` es la Tabla III-3b tal cual sale del PDF, sin tocar una palabra, y el script **rehace las 164 celdas**. Las cuatro filas que no se transcriben (selenio seco, biotina, vitamina K y el ratio Ca/P) van declaradas una a una con su motivo, para que saltarse una no pueda volver a ser invisible. **Y lo mismo con la Tabla VII-14**, la de las formas químicas: sus 27 factores se rehacen contra el texto del PDF, porque `fediaf_conversiones_vitaminas.json` existe precisamente para que nadie convierta la vitamina D con el factor de la A —×12 el aporte, y el semáforo callado— y ese fichero tampoco puede creerse a sí mismo. Lo ejecuta el BLOQUE 77 |
| `aaha_2021_tablas_transcritas.txt` | **Las tablas de AAHA 2021, que su PDF no suelta** (12 de septiembre). AAHA es la fuente de la que salen la banda de BCS 4-5 y el 10 % de los premios, y el repo la citaba 59 veces sin haberla leído entera. Al leerla aparecen **dos defectos del PDF**, y los dos callan. (1) Sus tablas están dibujadas como **trazos vectoriales**: `get_text()` de la página de la Tabla 8 —la que empareja cada enfermedad con sus nutrientes, o sea la hermana de `patologias.json`— devuelve **194 caracteres**, el título y el pie, y `get_images()` devuelve 0. No es el problema de las dos columnas de SACN5: ahí el texto estaba y salía desordenado; aquí **no está**. (2) En el texto que sí se extrae, los cuatro signos de desigualdad salen como puntuación corriente: `<` sale coma, `>` sale punto, `≥` sale `$` y `≤` sale `#`. Eso es peor que un hueco porque **no parece roto**: «A BCS ,4/9 or .5/9» se lee como una enumeración. ⚠️ Este fichero es una **transcripción a mano**, leída de las páginas renderizadas a 200 ppp, y eso lo separa de `fediaf_tabla_III_3b.txt`: aquella la rehace un script contra el PDF y **esta no se puede rehacer**. Va escrito en su cabecera, no en un comentario. `auditar_citas.py` lo indexa, así que una cita de la Tabla 8 se comprueba contra él |
| `fci_estandares_peso.txt` | **El apartado TAMAÑO Y PESO de los 65 estándares de la FCI que cita `razas.json`** (12 de septiembre, por la noche). Está para que `auditar_citas.py` compruebe que cada cita dice lo que dice la fuente y para que el BLOQUE 89 pueda REHACER cada peso contra ella. Sale de los PDF públicos de fci.be con `page.get_text()`, así que **sí se puede rehacer** — eso lo separa de `aaha_2021_tablas_transcritas.txt`, que es a mano y no. ⚠️ Se solapa a medias con `canislab-fuentes/FCI/`, que existe desde el 11 de septiembre con su `bajar_estandares.py` y 31 estándares enteros: ahí es donde tienen que acabar los 270, y aquí vive solo el apartado de peso de los que citamos, porque la sesión que lo escribió no podía empujar al repo de fuentes y un texto que se queda en una máquina no audita nada mañana |
| `auditar_conversiones.py` | **Que la conversión de cada cifra se rehaga en vez de creerse.** Las 88 cifras de `patologias.json` vienen de tablas publicadas en **% de materia seca** y el motor trabaja **por 1000 kcal**. Esa conversión estaba hecha una vez y **contada en prosa** dentro del campo `por_que`, y una frase no se ejecuta: el 8 de septiembre una se escribió ×25 en vez de ×2,5 —10 veces el valor bueno, con forma de dato bueno— y lo único que la cazó fue que alguien la leyó. Ahora cada cifra lleva un bloque `conversion` con el valor literal de la fuente, su unidad, la densidad de referencia y la cita, y este script **rehace la cuenta**. Una cifra sin ese bloque falla igual: lo que no se puede rehacer no se puede auditar. **Desde el 10 de septiembre rehace también los otros dos ficheros con cifras de una fuente**: las 12 de `recomendaciones_libro.json` —que estaban igual, con la conversión contada en prosa, y deciden el techo de calcio del cachorro de raza grande y el único techo de fósforo que hay en crecimiento— y las 4 de `requisitos_condicionales.json`, donde están **las dos conversiones a la vez**: la vitamina E del perro de trabajo sale de «≥500 IU/kg MS» y hay que pasarla además a mg de tocoferol natural, que es exactamente donde se falló el 8 de septiembre. Lo ejecuta el BLOQUE 72 |
| `LECTURAS.md` | **Lo que hemos leído de cada fuente, y qué decidimos con cada cosa.** Sustituye a toda la maquinaria de contar lecturas que hubo entre el 9 y el 11 de septiembre —`leer_fuente.py`, `leer_sacn5.py`, `leer_nrc2006.py`, `leer_fascetti.py`, sus cuatro `lecturas_*.json`, los dos inventarios de tablas y tres auditores—, borrada por una frase de Elena: «no sé por qué tienes que leer con un script. Lee, y según vayas leyendo vas anotando, y luego de lo que hayas anotado dices: vale, ¿esto hay que aplicarlo?». Los contadores decían «0 pendientes» y seguían saliendo cosas, porque contaban **frases con nota**, no cosas decididas. ⚠️ **El método es ahora la ley para todos los documentos**: se lee entero y seguido, se anota aquí todo lo interesante con su cita literal, y al terminar se repasa punto por punto decidiendo una de tres — **aplicado**, **no se aplica porque…** o **pendiente de decidir** —, y lo que quede pendiente va a `PREGUNTAS_ABIERTAS.md` con dueño |
| `canislab-fuentes/sacn5/extraer_texto.py` | ⚠️ **Y esto es lo que estaba fallando de verdad.** Los `.txt` de SACN5 y de FEDIAF se habían extraído **conservando la disposición visual**, y los dos libros van a **dos columnas**: cada línea pegaba la de la izquierda con la de la derecha. **El 37,5 % de las líneas de SACN5 y el 49,3 % de las de FEDIAF.** O sea que la mitad de lo que se leía eran frases que la fuente **no dice** —«Linoleic and α-linolenic acids are considered / DM fat should be restricted to between 7 to 10 %» son dos párrafos distintos—, y **cualquier cita sacada de ahí puede ser falsa**. Eso explica cómo «leído entero» podía ser verdad en esfuerzo y falso en resultado. Rehecho con `page.get_text()`, que sí lee las columnas en orden: quedan 2 líneas de 123.191. ⚠️ **Y por eso hay tablas que NO se pueden leer del `.txt`**: la VII-8a de FEDIAF, la de la curva de crecimiento, saca sus cinco bandas y sus cinco ecuaciones en dos columnas cruzadas y el emparejamiento que parece natural las cruza. Esa se leyó del PDF por coordenadas, y el BLOQUE 96 vigila que no se vuelva a cruzar |
| `fuentes_de_composicion.json` | **La prioridad de las fuentes del catálogo, con número de mandato, y la unidad en que publica cada una cada nutriente** (13 de septiembre). Nació de una petición de Elena: «coge cada fuente que tenemos y según la importancia de la fuente les pones número de prioridad o mandato». El orden existía y estaba en dos sitios donde no se puede auditar: en **prosa** en `Bases.md` y **cableado** en una tupla de `contrastar_fuentes.py` (`next(x for x in (b, c, u) ...)`). Son **1 BEDCA · 2 Köber 2017 (solo el calcio y el fósforo del hueso) · 3 CIQUAL · 4 USDA · 5 la etiqueta del fabricante**, cada uno con su porqué escrito. ⚠️ Y el orden **se volvió a justificar** el mismo día, porque Elena empujó («igual CIQUAL y la otra que empieza por F valen más que USDA»): se confirma, pero los motivos escritos eran otros. BEDCA es **la que MENOS nutrientes publica** de las europeas (~40 de 968 alimentos, contra 65 de CIQUAL y 105 de Frida) — no manda por completa, manda por **ser la española** y por ser **la única que distingue un hueco de un cero** (`value_type`: `TR` con la celda vacía = no hay cifra). Trae además el **mandato por nutriente**, que es donde el orden general no se puede aplicar a ciegas: el yodo no puede venir de USDA porque no lo publica, los 12 aminoácidos y la colina SOLO los publica USDA, y el cloruro solo CIQUAL. Y dos **conflictos de convenio declarados y sin resolver**: la vitamina A (tres convenios del β-caroteno y ninguno es el 4:1 que FEDIAF define para el perro) y la niacina (BEDCA da equivalentes, USDA preformada) |
| `auditar_composicion.py` + `fuentes_instantanea.json` | **El catálogo contra sus fuentes, celda a celda** (13 de septiembre). Entre una base de composición y el catálogo había un paso **a mano que nadie rehacía**, que es la misma forma de fallo que `auditar_transcripcion_fediaf.py` y `auditar_kober.py`. Lo que había mira otras cosas: `auditar_catalogo.py` compara el catálogo consigo mismo y nunca sale a la fuente, `fijar_identificadores.py` solo mira cuatro cifras, y `contrastar_fuentes.py` mira **una** ficha a mano — nadie la había pasado por las 163. El `.json` es la **instantánea congelada** de lo que publica cada fuente, en **su** unidad, con la **descripción literal de la fila**: eso último no es decoración, es lo único que delata un emparejamiento malo, porque un identificador a secas no dice si «pollo» trajo «Repollo». Con ella la batería puede comprobarlo **sin red**. Tiene tres modos: barrer, `--instantanea` y `--cerrar` (el único que escribe). Lo vigila el **BLOQUE 104** — nació como 100, pasó a 101 y acabó en 104, y las dos veces por lo mismo: dos ramas creando el mismo número el mismo día, y las dos con razón en su lado. ⚠️ Es la tercera vez que pasa (antes fue el 98), así que la lección ya no es «renumerar»: es que **un número de bloque es la única forma que tiene el repo de decir quién vigila qué**, y dos con el mismo número es una referencia rota que no da ningún error |
| `contrastar_fuentes.py` | Una ficha del catálogo contra **BEDCA, CIQUAL y USDA a la vez**, en el orden de `Bases.md`. **No lo ejecuta la batería** (necesita red y se baja 10 MB): es la herramienta de quien va a mirar una ficha. Trae dentro cómo se lee cada fuente — el XML de BEDCA hay que reconstruirlo de su `query.js`, y con la lista de atributos recortada devuelve el cuerpo vacío sin dar error |

**Y una patología marcada `formulable: true` tiene que formular de verdad.**
Suena a perogrullada y fue un fallo real del 8 de septiembre: se aplicaron dos
cifras de SACN5 en pasadas distintas —la vitamina E de la disfunción cognitiva y
el techo de fósforo del adulto sano—, cada una medida sola y cada una viable
sola, y **juntas dejaban esa patología sin menú a cualquier peso**. El semáforo no
puede cazarlo por construcción: no hay menú que mirar. Lo vigila desde el 9 el
**BLOQUE 61**, que recorre las 39 formulables y exige menú verde para el perro de
referencia. Cuando una cifra de la fuente no cabe, no se baja: se mueve a
`limites_escritos_que_el_solver_no_aplica` con su medida —donde ya están el
omega-3 del cáncer y el de la artrosis— y se pregunta. Detalle: `PATOLOGIAS.md`
§1.4-bis.


### El catálogo, en orden alfabético — y por qué eso es una regla y no estilo

*(13 de septiembre de 2026, noche.)* Elena, mirando Personalizar: «**han
desaparecido cosas del catálogo… por ejemplo la zanahoria no está**», y un
minuto después: «**ah calla si está, solo q no está por orden alfabético**».

**El fallo no dejaba nada fuera y aun así hizo exactamente el mismo daño que
dejarlo fuera**, y por eso está aquí y no en una lista de retoques: quien lo vio
dio por hecho que el alimento ya no existía. Un alimento que no se encuentra es
un alimento que no se elige. Y **ninguna de las comprobaciones que ya había
podía verlo**: el BLOQUE 99 y `catalogo-app-y-motor.spec.js` cuentan alimentos y
comparan conjuntos, y no faltaba ninguno.

Los nombres **de dentro** de cada grupo ya se ordenaban desde siempre; lo que
salía en el orden en que aparece en el catálogo eran **los grupos y las
categorías**. En «Verduras y frutas»: Calabaza · Calabacín · Zanahoria · Judía ·
Brócoli. Se ordenan ahora las tres cosas, en las **dos** formas que sirve `GET
/alimentos` —`pantallas` (lo que ve el dueño en Personalizar) y `por_categoria`
(lo que lee el formulador del veterinario)—, y en la app también el **respaldo**,
que no pasa por el motor y es justo donde una lista escrita a mano se desordena
en cuanto alguien añade una línea al final.

⚠️ **Se ordena SIN TILDES y sin mayúsculas, y eso no es cosmético**: con el orden
de códigos de carácter todo lo que lleva tilde se va **detrás de la Z** —la «Ñ»
incluida—, así que «Riñón» acabaría después de «Zanahoria» y «Acelga» y «Ácido»
quedarían separados por veinte filas. Es la **misma regla con la que se busca**
(`sinTildes` en `src/texto.js`, `_sin_tildes_para_ordenar` en `main.py`), y tiene
que serlo: se ordena para que quien busca encuentre. Lo vigilan el BLOQUE 99 —con
el fallo puesto, ocho rojos— y `tests/catalogo-en-orden.spec.js`, que llama a la
**misma** función que pinta (`arbolOrdenado`, en `texto.js` y no en `App.jsx`
para que se pueda probar sin levantar la app).

### Endpoints: cuáles usa la app y cuáles no

Los que llama el frontend hoy: `/menu/v2`, `/menu/semana`,
`/menu/varios-perros`, `/menu/anadir`, `/menu/cambiar`, `/menu/quitar`,
`/menu/revalidar`, `/analizar`, `/alimentos`, `/formular/*`, `/pauta/*`,
`/patologias`, `/relajacion`, `/vocabulario`, y los de Stripe.

`GET /patologias` (7 de septiembre) sirve la tabla de `patologias.json` con
los topes, su fuente, su motivo y **el margen contra el límite de FEDIAF del
mismo nutriente** — renal aprieta el fósforo a 1200 con el mínimo en 1160:
un 3,4 % de sitio. Existe para que quien firma una pauta pueda leer el
número que decide si sale menú, y **para que ese número no se copie a la
app**: sería la tercera copia de la misma tabla, que es exactamente cómo se
desincronizó la del `POST /menu`. Lo vigila el BLOQUE 44, cifra a cifra
contra el archivo que aplica el solver.
Y sirve también los **avisos sueltos** de cada patología —los que no son
«general», «crecimiento», «profesional» ni «profesional_crecimiento»—, que son
ocho y dicen justo lo que el motor NO puede hacer solo: que al perro con bromuro
potásico hay que medirle el bromo en sangre después de cambiarle la dieta, que el
mitotano va con comida, que la reacción adversa necesita una o dos proteínas y
novel, que un perro adelgaza 1-2 % a la semana. Son texto, así que el BLOQUE 44
no los miraba: los vigila el **BLOQUE 64** (9 de septiembre), que exige que
lleguen **por las dos puertas** —`GET /patologias` y la tabla que lee el solver—
y que sigan llevando su cifra dentro. Un aviso truncado parece que está y no dice
el número.

⚠️ **Y desde el 13 de septiembre (noche) esos avisos tienen los DOS REGISTROS,
como todo lo demás.** Lo pidió Elena viendo uno en su pantalla: «los avisos al
usuario son muy técnicos y nombran fuentes. **FUERA**». Y era literal — el aviso
de la artrosis empezaba «SACN5 5ª ed., cap.34 …, Tabla 34-2», y el del
estreñimiento traía tres frases en inglés entre comillas. Medido antes de
tocarlo: **24 de los 54 avisos principales y 23 de los 25 sueltos** nombraban una
fuente, una tabla, un capítulo o una unidad del motor. La regla no cambia —
`dueno` sin jerga y con algo que hacer, `veterinario` con la palabra de la fuente
— y **lo que se le quita al dueño no se borra, se mueve**: el texto técnico se
queda entero con su clave de siempre y es el que sirve `GET /patologias` y el que
sale en modo profesional. || La forma: `avisos.dueno` y `avisos.dueno_crecimiento`
para el aviso principal, y el prefijo **`dueno_`** para los sueltos
(`dueno_mitotano_con_comida` al lado de `mitotano_con_comida`). Es **opcional a
propósito**: hay avisos que ya estaban escritos sin jerga y duplicarlos sería dos
textos que mantener para decir lo mismo, así que lo que se vigila **no es que el
campo exista sino que el texto SERVIDO esté limpio** — el BLOQUE 107 mira el
aviso que sale (`dueno` si lo hay, `general` si no) por las dos puertas que lo
enseñan, `avisos_patologia` dentro del menú y `GET /vocabulario` al marcarla, que
es la única que ven las ocho patologías que no formulan. || ⚠️ Y **hay dos formas
de que esto se vuelva en contra, y las dos están vigiladas**: que las claves
nuevas caigan en `avisos_extra` —que sale por el canal del dueño—, con lo que el
dueño leería las dos versiones seguidas; y que el registro llano acabe **encima**
del técnico, que no es limpiar sino perder la cita, y saldría verde porque el
canal del dueño estaría impecable. Por eso el bloque ancla cuatro avisos técnicos
(renal, artrosis, disfunción cognitiva y obesidad) y exige que sigan nombrando su
fuente. || Y **el `not es_profesional` de `avisos_de_patologias` no sobra** aunque
esa función ya haga `continue` con esa condición: los dos `continue` solo
disparan si la patología TIENE aviso de profesional, y **30 de las 47 no lo
tienen** — sin esa guarda, a un veterinario que formula una de esas 30 se le
serviría el texto llano.

⚠️ **Y LOS AVISOS DE SEGURIDAD LLEVABAN LA MISMA FUENTE DENTRO, y a esos no
llegaba el barrido.** Son los 16 de `revisar_seguridad` y `avisos_rotacion`
—la tiaminasa, el mercurio, la vitamina D, el yodo, el selenio, la histamina,
el tejido tiroideo, los huesos— y **dependen de qué alimento lleve el menú**:
el de la histamina solo sale con sardina, caballa, atún o boquerón. O sea que
pedir cinco menús y mirar lo que traigan es una **muestra, no un barrido**, y
cuatro se escaparon: «(FEDIAF 2025, §7.6.2.4)» en el de la histamina, «el
límite del NRC según sus calorías diarias» en el de la vitamina D —que además
estaba mal escrito, «por encima de **el** límite»—, «(TVT Merkblatt 181, mayo
2025)» en el del tejido tiroideo y «referencias humanas de la EPA» en el del
mercurio. La forma de barrerlos todos es **no pedir menús**: se le pasa a la
función un menú sintético con **el catálogo entero**, que dispara a la vez cada
aviso que depende de un alimento (336 avisos). Las cuatro fuentes se mueven a
`avisos_profesional`, y para eso la lista del profesional de `revisar_seguridad`
**nace ahora al principio de la función y no 240 líneas más abajo** — antes no
existía todavía cuando se escribían esos tres avisos, que es por lo que llevaban
la cita dentro. ⚠️ **«AESAN» se queda, y es una decisión**: es la agencia
española de seguridad alimentaria y su consejo sobre el mercurio en el pescado
está escrito para el público general. Lo que Elena mandó fuera es la referencia
que no se puede consultar, no el nombre de un organismo público.

⚠️ **Lo que NO se ha encontrado, y se dice**: Elena describió además «un aviso de
que el máximo era el 10 y que llevaba un 11 — eso no debería ser un aviso,
debería ser un menú en rojo». Barridos `/menu/v2`, `/menu/semana`,
`/menu/cambiar`, `/menu/anadir`, `/menu/revalidar` y `/catalogo/*` con toy,
adulto, gigante, cachorro y lactante, **ningún menú entregado trae un aviso de
«te has pasado del límite»**, y está comprobado por qué: `_garantizar_verificado`
llama a `_menu_precalculado_es_seguro`, que aplica **los mismos cinco topes con
las mismas constantes** que el aviso, así que un menú que se pase no se entrega
—se reformula o se rechaza—. Medido sobre un menú real: con 80 g de sardina
(10,2 % de las kcal) el filtro ya dice que no, y `/menu/revalidar` devuelve el
menú rehecho con 52 g. El candidato más parecido a lo que describe es el aviso
de la **tiaminasa**, que dice literalmente «el límite seguro es 10 %», pero solo
puede salir por `/analizar`, donde avisar **es** lo correcto porque no hay menú
que rechazar. Queda en `PENDIENTE_PRODUCTO.md` a la espera de la captura.

`GET /vocabulario` (11 de septiembre) sirve **todo lo que el motor enumera**,
para que la app lo lea en vez de copiárselo: los cinco niveles de actividad con
su cifra de FEDIAF, las 255 razas, los seis tamaños, las etapas, los nueve
puntos de BCS, las patologías, las categorías, los peldaños y **los 46
nutrientes a los que un profesional puede ponerle un objetivo** Y desde ese mismo
día **la pregunta de los premios con sus cuatro respuestas** —la única de las
listas que trae además CÓMO se pregunta, en los dos registros, porque es una
pregunta que la ficha todavía no hace y la app tiene que poder montarla entera
leyendo de aquí. De sus cuatro cifras **solo el 10 % es de la fuente**; el 5 %
y el 20 % son nuestros y su etiqueta de veterinario lo dice. Existe por una
frase de Elena: «si el motor dice que hay dieciocho niveles de actividad, la app
tiene que tener 18 niveles de actividad porque si no no sirve de nada, y así con
todo». La cadena es **FUENTE manda → MOTOR la implementa → APP la ofrece**,
nunca al revés — y eso último hay que decirlo porque yo lo hice al revés una vez
ese mismo día: amplié la base de datos de la app para que cupieran los cinco
niveles que la app ya ofrecía, en vez de preguntar primero cuántos tiene la
fuente.
Cada cosa se sirve con **dos registros**: `dueno` (sin jerga, con un ejemplo de
lo que se ve o se toca) y `veterinario` (la palabra de la fuente, con su tabla y
sus horas). Los dos viven en el motor a propósito: si la técnica viviera copiada
en la app, el día que el motor añada un nivel la app se queda con su lista vieja
y el usuario elige algo que el motor no sabe recibir. Lo vigilan los BLOQUES 88
y 89 aquí, y `tests/vocabulario.spec.js` en `canislab-web` — que además no se
conforma con ver la palabra correcta en pantalla: siembra palabras **inventadas**,
porque «la app lo ha leído del motor» y «la app está pintando su respaldo» se ven
exactamente igual, y una prueba con las palabras de verdad pasaría en verde con
la petición entera comentada.
⚠️ **Lo que NO se puede servir por aquí son las cifras que ya viajan dentro del
menú** — los topes de patología van por `GET /patologias` y los peldaños por
`GET /relajacion`. Tres sitios y una sola copia de cada cosa.

**Los objetivos que pone el profesional** (11 de septiembre) van en
`objetivos_del_profesional` de `POST /formular/*`: `{nutriente: {"min": x,
"max": y}}`, en la unidad del motor (g o mg por 1000 kcal), que es la misma en
la que ya lee todos los demás límites. Nacieron de un pedido de Elena — «el
veterinario debe poder decidir en qué porcentaje quiere dejar la grasa, la
proteína, lo que sea… y no solo para patologías» — y de la regla que los limita,
suya también: «**los requisitos se respetan SIEMPRE, eso no se negocia**».
Así que **solo pueden apretar**: entran por el mismo cajón que los topes y
suelos de patología y con el mismo `min()`/`max()`, y antes de llegar al solver
`_objetivos_dentro_de_fediaf` los recorta contra FEDIAF. Un techo del
profesional por encima del máximo de FEDIAF no hace nada; un suelo suyo por
debajo del mínimo se sube al de FEDIAF; y un techo **por debajo del mínimo** no
se intenta siquiera, porque no es apretar una ración sino dejarla incompleta.
⚠️ **Y la lista de nutrientes que se ofrecen la sirve `GET /vocabulario`, no la
app** (11 de septiembre, por la noche). La pantalla del formulador tenía **ocho**
escritos a mano dentro de `formulador.jsx` y el motor acepta los **46** que
verifica: la clave viaja tal cual y `_objetivos_dentro_de_fediaf` la busca en
`verificar.MAPA`. O sea que los otros 38 no faltaban por el motor — faltaban
porque la lista la decidía la app, que es el fallo de las categorías y el de los
niveles de actividad otra vez. Se sirven con su **unidad dentro del título del
veterinario**, porque quien escriba 2 creyendo que son gramos cuando son
miligramos aprieta mil veces de más. Los ocho se quedan de **respaldo** para
cuando Render duerme, y que el respaldo no esté tapando la petición lo comprueba
`tests/formulador.spec.js` sembrando **nombres inventados**. Lo vigila el BLOQUE
88, que además exige que cada nutriente servido se pueda usar **de verdad**: uno
servido y descartado por el motor sería un objetivo que el profesional escribe,
que no hace nada, y que no aparece en ningún recorte.
⚠️ **Todo recorte se dice** en `objetivos_ajustados`, salga o no salga el menú:
aplicar el número de FEDIAF en lugar del suyo en silencio dejaría al profesional
firmando algo que no es lo que escribió. Lo vigila el BLOQUE 91, y su prueba más
importante es la cuarta: un perro renal con un techo de fósforo de 3000 puesto
por el profesional tiene que seguir saliendo a 1200 **y seguir saliendo** — si
deja de salir, es que el objetivo flojo llegó al solver y lo paró el filtro
final, que es taparlo y no evitarlo.

**Y la semana del profesional tiene presupuesto, como la del dueño** (11 de
septiembre). El generador del tutor reparte el presupuesto semanal de seguridad
crónica entre los siete días desde el 25 de agosto: `/menu/semana` genera la
semana entera en UNA llamada para que el servidor pueda ir restando y pasarlo a
`resolver()` como restricción DURA. El formulador del veterinario no lo hacía, así
que cada ración se formulaba como si fuera la semana entera y **quien firma tenía
menos protección que el tutor** justo en los cinco topes que son crónicos. Ahora
`/formular/autocompletar` acepta `raciones_ya_puestas` (las que ya ha decidido,
con sus días) y `dias_de_esta_racion`, y **la resta la hace el servidor**: el
profesional construye sus raciones de una en una y no puede mandarlas todas de
golpe, pero dejarle la cuenta a la app sería volver al aviso que se puede ignorar.
Medido: con seis días de una ración de 6844 µg de yodo al día contra un
presupuesto de 8106, la del séptimo no sale; desconectando el presupuesto del
solver sale con 524 µg como si nada. Lo vigila el BLOQUE 92.

`GET /relajacion` (8 de septiembre) sirve los peldaños de la escalera con su
nombre y qué suelta cada uno, y `/menu/v2` y `/formular/autocompletar`
aceptan `peldano`. **Con un peldaño elegido no se baja solo**: bajar sería
cambiarle la decisión a quien la ha tomado, que es lo contrario de por qué se
puede elegir. Un peldaño mueve las proporciones de BARF y cuántos suplementos
caben — la FORMA, regla 3 — y **nunca** los 43 requisitos, el ratio Ca:P ni
los topes de seguridad y de patología: eso lo vigila el BLOQUE 45, que además
comprueba que la lista servida es la que recorre `_escalera_de_relajacion` y
no una copia. Y el menú dice ahora **siempre** en qué peldaño salió, no solo
cuando hubo que bajar: «no dice nada» y «estricto» se leían igual, y quien
firma necesita poder afirmar lo segundo.

**Los que nadie llama pero siguen expuestos**: `/catalogo/{tamano}/{etapa}`,
`/der`, `/transicion` y `/perro/{perro_id}/menus`. Se dejan a propósito: no
duplican nada, son funciones que existen y que la app puede volver a usar.
Pero nadie los prueba usando la app, así que si algo se rompe ahí solo lo
ve la batería. **Y se rompen de verdad**: `/der` llevaba desde el 28 de
agosto devolviendo 500 en TODAS las llamadas — se le pasaba un
`peso_objetivo_kg=` que `calcular_der()` no tiene — y no lo vio nadie en
dos semanas, porque la app calcula el DER por su cuenta y el BLOQUE 23
prueba la función por dentro, nunca la puerta. Arreglado el 11 de
septiembre, y ahora el BLOQUE 93 llama al endpoint.
`/perro/{perro_id}/menus` **era el único agujero de la regla 1** hasta el 7
de septiembre, y no por descuido: la tabla `menus` guardaba nombre, gramos
y kcal, así que un menú guardado no se podía verificar ni en principio.
Ahora `guardar_menu` escribe el contexto (etapa, DER, pesos, patologías)
junto al menú y el endpoint lo verifica al leerlo — o dice que no puede,
si es una fila anterior a ese cambio. Lo vigila el BLOQUE 47.
**Y desde el 11 de septiembre pide credencial**: era un GET con el id del
perro en la dirección y nada más, y los ids van 1, 2, 3 — contarlos hacia
arriba enseñaba el historial de comida de los perros de todo el mundo. La
regla 1 mira que el MENÚ cumpla, no que sea tuyo; eso son dos preguntas.

### Las puertas: quién puede pedir qué

Escrito el 11 de septiembre, porque hasta ese día no había ninguna y los
92 bloques de la batería vigilaban qué SALE, nunca quién PIDE. Seis
agujeros, ninguno de ellos daba error ni se veía en pantalla, y los cuatro
primeros llegaban a datos de otra persona. Lo vigila entero el BLOQUE 93.

1. **La consulta a Stripe se montaba con un f-string.** Una comilla simple
   dentro del `user_id` — que llega en el cuerpo de `/stripe/checkout`, que
   no autentica a nadie — la convertía en la consulta que quisiera quien
   llamara, y devolvía las suscripciones de otra gente. Ahora ese campo
   pasa por `_user_id_limpio()`, y sin id válido **no se hace la consulta**.
2. **`/stripe/portal` abría el portal del `stripe_customer_id` que le
   mandaran.** Un identificador no es una credencial, que es exactamente lo
   que ya estaba escrito el 29 de agosto en `_es_profesional_acreditado` y
   este endpoint no seguía. Ahora pide el token de sesión y el cliente sale
   de la suscripción de ESE uid. `/stripe/checkout` tampoco devuelve ya una
   URL de portal: sabiendo el uid de otro — un UUID, que no es secreto —
   daba la puerta a su facturación.
3. **El token de sesión se iba entero a Sentry.** `observabilidad.py`
   comparaba nombres de clave EXACTOS, su lista decía `token`, y el campo
   se llama `token_usuario`. Ahora se compara por trozo y además se tacha
   por FORMA (`_JWT`, y los prefijos `sb_secret_` / `sk_live_` / `whsec_`),
   porque Sentry adjunta las variables locales y ahí el token viaja dentro
   de un texto donde ninguna limpieza por nombre puede verlo.
4. **El sello de una pauta firmada era un SHA-256 sin clave**, o sea una
   receta pública: se cambiaba el menú y el número de colegiado, se
   recalculaba, y `/pauta/comprobar` decía «es exactamente el que se
   firmó». Ahora es HMAC con `SELLO_SECRETO`, **y sin esa variable no se
   firma** (503). `/pauta/comprobar` sigue reconociendo los sellos
   anteriores, pero los llama por su nombre y dice que hay que volver a
   firmar.
5. **El CORS estaba en `*`** con el comentario «en produccion, poner aqui
   el dominio real» puesto desde el primer día. Hoy no daba acceso a la
   cuenta de nadie — para eso hace falta el token —, pero deja de ser
   inofensivo en cuanto un endpoint se fíe de una cookie, y ese día nadie
   iba a volver aquí.
6. **`/der` cogía el índice de actividad sin mirarlo.** Un `-1` no
   revienta: en Python cuenta desde el final y elige «trabajo», el que más
   kcal da. De ese DER salen las kcal del menú y el semáforo verifica
   CONTRA ESE DER, así que sale verde — es la familia de fallo de
   `radiografia.py`.

**Lo que sigue sin puerta, y es a propósito**: `/menu/v2`, `/analizar`,
`/alimentos` y los demás del motor. No dan acceso a datos de nadie: se les
manda un perro y devuelven un menú. Y el premium lo sigue tapando el
frontend, que es un `blur` de CSS. Ver `VETERINARIOS.md` §10 para lo que
queda y por qué la fase 4 no se despliega sin ello.

`POST /menu` **ya no existe** (26 de agosto). Era el motor anterior al MILP
y arrastraba su propia tabla de patologías, desincronizada de la buena:
fósforo renal a 1.400 en vez de 1.200, cobre en hepatopatía a 3,0 y sin
bloquear, grasa en pancreatitis al 25 % de las kcal, diabetes bajando la
grasa siempre, y urato, cistinuria y «otra» sin existir. No llegó a dar
menús malos porque `_garantizar_verificado()` los habría rechazado — que es
otra forma de decir que ese camino construía menús que el filtro final iba
a tirar. El BLOQUE 24 vigila que no vuelva.

### Los 12 aminoácidos y el techo de lisina

Los 41 nutrientes de FEDIAF (Tabla III-3b) se verifican los 41 desde el 28
de agosto, incluidos los 12 aminoácidos esenciales — con el Ca:P y el calcio
de raza grande son las 43 filas completas. `metionina_cistina` y
`fenilalanina_tirosina` no son claves de los alimentos: son sumas que
calcula `valor_nutriente`, como `epa_dha`.

**Una excepción escrita y probada**: el techo de lisina (7,00 g/1000 kcal,
solo en crecimiento) no se aplica — **0 de 12 menús de cachorro caben debajo**
(remedido el 9 de septiembre sobre el catálogo regenerado: van de 8,24 a 11,48,
mediana 9,03), porque la lisina va detrás de la proteína y una ración BARF de
cachorro lleva ~134 g/1000kcal contra un mínimo de 50. Aplicarlo dejaría a todos los
cachorros sin menú. La excepción vive en `verificar.MAXIMOS_NO_APLICADOS`
—única lista, leída por solver y semáforo vía `maximo_de()`—, con la
pregunta pendiente para el nutricionista en `PENDIENTE_DECISIONES.md`. El **mínimo**
de lisina sí se aplica; solo se quita el techo.

Lo vigila el BLOQUE 27: que los doce sigan en `MAPA`, que las dos sumas
sumen de verdad, que la proteína sin aminograma no pase del 5 % de un menú
real, y que el techo de lisina siga siendo el único máximo no aplicado.
Faltan 16 aminogramas (once suplementos, y la laringe de vacuno vacía a
propósito por ser cartílago). Detalle completo, las medidas y la trampa de
unidades del triptófano: `HISTORIA_TECNICA.md`.

### Los mínimos escalan hacia arriba, nunca hacia abajo

`minimo_de()` en `verificar.py` es el único sitio que escala los mínimos
cuando el perro come menos (ecuación de FEDIAF 7.2.5) — y `maximo_de()` el
único que sabe de máximos. Solo hacia arriba: no hay base en FEDIAF para
bajar el mínimo de un perro que come más. No escalan la grasa, el
EPA+DHA/linolénico/araquidónico (no hay requerimiento absoluto en adulto), ni
crecimiento/gestación/lactancia.

**Los máximos no escalan nunca** —son concentración, no cantidad— así que la
ventana entre mínimo y máximo se cierra según bajan las kcal. En dieta
húmeda el selenio se cruza en DER 45,2: por debajo el motor devuelve
`imposible_por_aritmetica` (nutriente + los dos números) en vez del «quita
una restricción» de siempre, porque ahí no hay combinación que lo arregle.
Lo vigila el BLOQUE 34.

El peso de referencia para escalar es `peso_objetivo_kg`, no el real — sin
ese campo se usa el real y se escala de más (lado seguro); lo vigila
`tests/peso-objetivo-en-cada-peticion.spec.js` en `canislab-web`. Detalle
completo y las medidas: `HISTORIA_TECNICA.md`.

### La duplicación que hay que vigilar (DER)

El DER se calcula dos veces: `der.py` aquí y `calcularDER()`/`src/der.js` en
`canislab-web` — y **manda el del frontend**, que se envía en
`der_objetivo`; `der.py` solo corre si alguien llama a `/der`, que no llama
nadie. Se vigilan por separado contra `der_casos.json` (137 casos, **el
mismo archivo en los dos repos**): BLOQUE 23 aquí, `der-contrato.spec.js`
allí. Si tocas la fórmula de un lado, regenera esperados y copia
`der_casos.json` a los dos repos — los dos commits, o ninguno. Detalle
completo: `HISTORIA_TECNICA.md`.

⚠️ **Y el peso adulto de un cachorro ya NO se recorta al rango de su raza**
(12 de septiembre, noche): lo decide su propia trayectoria. El porqué, la medida
y las dos guardas están en `der.peso_adulto_desde_curva` y en la P-36.

⚠️ **Y hay un trozo que NO está duplicado, que es peor**: la estimación del
peso adulto de un cachorro a partir de su edad. Aquí vive en
`peso_adulto_desde_curva()`, y el frontend **no la tiene** — si no sabe el peso
adulto cae a los dos escalones de SACN5 por edad. Desde el 11 de septiembre
esta parte usa la **Tabla VII-8a de FEDIAF**, que publica la curva como cinco
ecuaciones por banda de peso adulto; antes usaba una tabla sacada de
reproducciones divulgativas de las curvas WALTHAM, y en el cachorro de raza
gigante iba **12 puntos por debajo**, o sea **~9 % de kcal de más** (2479
contra 2142 en un cachorro de 30 kg a los 6 meses) justo donde FEDIAF avisa de
deformidades esqueléticas por sobrealimentar. **Ningún caso de `der_casos.json`
la ejercía**, así que el contrato no cambió. Lo vigila el BLOQUE 96, incluido
el emparejamiento banda↔ecuación, que es lo que el texto a dos columnas del PDF
cruza. Si se lleva también al frontend, ahí sí hay que regenerar el contrato en
los dos repos: está en `PREGUNTAS_ABIERTAS.md` P-14.

### Los documentos

`CLAUDE.md` (esto) es la entrada. `HISTORIA_TECNICA.md` tiene el detalle
completo — medidas, cifras, el porqué — de los temas que aquí solo llevan
un resumen de dos líneas: los aminoácidos, el escalado de mínimos y
máximos, la duplicación del DER, los datos dudosos. Ábrelo solo cuando la
tarea toque justo esa parte del motor. `PENDIENTE.md` es el índice de lo
que queda, ordenado por prioridad — desde el 6 de septiembre, solo el
índice: cada punto vive en `PENDIENTE_DECISIONES.md`,
`PENDIENTE_DINERO_Y_SALUD.md`, `PENDIENTE_PRODUCTO.md` o
`PENDIENTE_NUTRICION.md` según el tema, y se abre solo el que toque la
tarea. Lo ya resuelto vive en `HECHO.md`, y la investigación o el código
detrás de un pendiente que no hace falta releer cada vez, en
`PENDIENTE_DETALLE.md` (el bloque de veterinarios señala directamente a
`VETERINARIOS.md`, que ya lo tenía completo) — los dos con resumen de una
línea y puntero en su sitio, para no recargar lo que se lee al empezar
cualquier sesión. `CERRADO.md` (8 de septiembre) dice **qué está cerrado y qué no**, y por qué.
Cerrado no es «terminado»: es que cumple **las seis condiciones a la vez** (vive
en el repo · tiene fuente · tiene ficha de permisos · tiene un test que falla si
se rompe · está escrito como decisión con fecha · no deja preguntas sin dueño), y
que reabrirlo solo vale por una de cuatro razones escritas. Cinco de seis no es
cerrado, y ahí se dice cuál falta. Ábrelo antes de tocar un número que venga de
una fuente.
`PATOLOGIAS.md` (8 de septiembre) es la lista de las 47 patologías una por
una: qué aplica el motor, la **cita literal** de la fuente con su conversión, el
**techo duro** que nadie puede pasar y de dónde sale (legal, seguridad crónica o
mínimo de FEDIAF), y **qué margen le queda al profesional**. Se escribió
verificando cada cifra contra su fuente original, y encontró cinco errores y
catorce patologías con factores de su propia fuente sin aplicar. Ábrelo antes de
tocar `patologias.json`: los números siguen viviendo allí y este documento es su
lectura, no una segunda copia — si discrepan, manda el JSON.
Las **474 tablas de SACN5** se inventariaron el 10 de septiembre en `sacn5_tablas.json` y el fichero se **borró el 11** con el resto de contadores: 64 tenían rastro en el repo, 44 eran felinas, 75 eran listados de productos, 208 estaban leídas sin nada que aplicar, **22 leídas CON hallazgo** y 1 aplicada entera (la 6-2 **es** `sacn5_fuentes_de_minerales.json`). Lo que importaba de ese inventario **no se ha perdido**: las 22 con hallazgo están migradas una a una a `LECTURAS.md`, y las medidas completas siguen en `HALLAZGOS_SACN5_10SEP.md` y `HALLAZGOS_SACN5_11SEP.md` (los 19 de las tablas más los 9 del texto). Los dos más gordos: SACN5 pide **cuatro veces** la vitamina E que damos al perro sano —en cinco capítulos distintos— y su tabla de energía del cachorro (33-8, de NRC 2006) va hasta un **28 % por encima** de la curva de Klein que publica FEDIAF y que aplicamos.
`LECTURA_SACN5.md` (10 de septiembre) es el **registro de la lectura íntegra de
SACN5**, capítulo a capítulo, texto y tablas. Existe porque una lectura que no
deja rastro no se puede comprobar ni continuar: dice de cada capítulo qué se
aplicó, qué no y **por qué no**, y trae leídas enteras las **nueve tablas de
recomendación canina que el motor no ofrece**, para que esa decisión se tome con
los números delante. Su cabecera explica el método —leer todo, apuntar todo, y
aplicar solo al final— y el fallo que lo motivó: leer un párrafo, aplicarlo, y
descubrir en el siguiente que estaba mal. Ábrelo antes de volver a abrir SACN5.

`VERIFICACION_FILA_A_FILA.md` es el registro de las cuatro pasadas de
verificación de ese día, y su §cuarta pasada trae la lección que más cuesta:
**el barrido de las tablas de SACN5 se hizo cortando su propia salida con
`sed`, así que de las 89 tablas que hay solo se revisaron unas 40** y faltaban
tres de patología canina. Un barrido cuyo resultado no se compara contra el
total no es un barrido, es una muestra.
`PARA_EL_NUTRICIONISTA.md` es **el documento que se entrega para revisión**:
qué hace hoy el motor en cada punto, de qué fuente sale cada número, y qué
queda sin decidir. Se escribe a mano y el motor cambia debajo, así que se
desincroniza sin que se vea — pasó dos veces el 9 de septiembre, y en
direcciones opuestas: decía que el motor «no usa» las dos filas de raza de
FEDIAF cuando ya las usaba, y decía «<14 semanas» para Early Growth cuando el
código cortaba a los 4 meses. Por eso lo vigila el **BLOQUE 65**, que ancla
25 cifras del documento contra el valor **vivo** que aplica el motor: los
escalones de actividad, las dos razas, el respaldo de crecimiento, los topes
de seguridad crónica, los techos del perro sano, los dos umbrales de raza
grande y el recuento de patologías y de sus límites. No revisa la prosa, solo
números — que es donde están las decisiones —, y si un ancla deja de encontrar
su frase también falla, porque un ancla que ya no vigila nada no avisa a nadie.
`PREGUNTAS_ABIERTAS.md` es **el registro de preguntas**, y desde el 9 de
septiembre dice también dónde vive cada una. Vivían en tres ficheros con tres
numeraciones y tres formas de marcar el cierre, sin que ninguno comprobara a los
otros, y eso dejaba **preguntas zombi**: resueltas y aplicadas en el motor, y
todavía abiertas en el documento que va a revisión. El techo de yodo bajó de 1400
a 1275 y la pregunta siguió marcada «bloqueante, la que más nos preocupa» en
`PARA_EL_NUTRICIONISTA.md`, afirmando algo del motor que ya era falso. Ahora este
fichero lleva el **índice** de las preguntas del documento de revisión con su
estado —`abierta` · `reducida` · `cerrada` · `retirada`, cuatro y no dos, porque
la fuente casi nunca contesta la pregunta entera— y el **BLOQUE 66** exige que
índice y documento digan lo mismo. Nada se borra al cerrarse: se tacha con la
fuente que lo cerró, porque una pregunta borrada se vuelve a hacer.
`FEDIAF_CONTRA_OTRAS_FUENTES.md` (11 de septiembre) es **dónde las fuentes no
dicen lo mismo, y qué aplica el motor**. La regla es una sola: **si otra fuente
contradice a FEDIAF, gana FEDIAF** — pero la discrepancia se apunta con las dos
cifras, porque quien firma una pauta tiene derecho a saberla. Trae la distinción
que hace falta para leerlo: casi todo lo que el motor aplica y no es de FEDIAF
**cabe dentro** de FEDIAF (aprieta con `min()` o con `max()`) y eso no es
conflicto; hay conflicto solo cuando la otra fuente sacaría al perro **fuera** de
la ventana, y hoy son cinco casos (selenio, Ca:P del cachorro grande, energía de
crecimiento, edad del sénior y yodo). Va al documento que lee el nutricionista.

`REVISION_NUTRICIONISTA.md` es la valoración que hizo Cris Carles del motor,
punto por punto contra el repo: qué de lo que señaló ya está cubierto, qué a
medias y qué sigue sin estar. Los tres que siguen sin estar son el **ratio
omega-6:omega-3** (que no existe, y lo piden dos fuentes independientes), la
**pantalla de objetivos por nutriente** con el rol que la firma, y la **ficha de
L-metionina** en el catálogo. Ábrelo antes de decidir qué se construye después.
`DATOS_QUE_FALTAN.md` son los valores del catálogo
que hay que conseguir de BEDCA/CIQUAL/USDA, uno a uno — **no los rellena el
asistente**. `Bases.md` y `Ya_probado.md` son de las primeras sesiones:
decisiones cerradas y callejones sin salida ya recorridos, léelos antes de
proponer un cambio grande. `CAMBIOS_DE_DATOS_REVERTIDOS.md` explica por qué
se deshicieron unos cambios de datos del 21 de agosto.
`VETERINARIOS.md` es el plan de la parte para veterinarios: qué se
decidió el 28 de agosto, en qué orden se construye, y las tres cosas
que si se hacen mal no se arreglan después — que el profesional entre
con su cuenta y nunca con la del dueño; que una prescripción por debajo
de FEDIAF se verifique igual, contra un juego de requisitos escrito que
viaja con el menú; y que la pauta, que sale firmada con nombre y número
de colegiado, se guarde congelada entera — menú, ficha verificada,
contexto, huecos y sellos —, porque la ficha del perro, el catálogo y el
motor cambian, y un documento firmado tiene que seguir diciendo lo mismo
dentro de un año.

### Los datos

**`UNIDADES.md` es lo primero que hay que leer antes de tocar el catálogo**:
en qué unidad va cada uno de los 41 nutrientes, sobre qué base (100 g de
alimento tal cual se da) y las cuatro trampas que se cuelan siempre. La
peor: `linoleico` es **omega-6** y `linolenico` es **omega-3** — se
diferencian en una letra, son cosas opuestas, y si se cargan cambiados no
salta nada, el menú sale verde igual. Lo vigilan el BLOQUE 26 y
`auditar_catalogo.py` (los nueve alimentos donde el omega-3 supera al
omega-6).

**Los TRES campos que dicen qué sabemos de cada 0.** Un 0 puede ser «no lo
tiene» o «no lo sabemos» — eso lo separa `sin_dato`. Un valor declarado y
erróneo (tiene forma de dato bueno y pasa cualquier validación de formato)
va en **`dato_dudoso`**, que `verificar()` devuelve junto al menú igual que
los huecos. Lo vigila el BLOQUE 28. Los tres casos reales que lo motivaron
(omega-3 de salmón, fósforo de harina de hueso, cobre de polvo de sangre):
`HISTORIA_TECNICA.md`.
El tercero es **`cero_verificado`** (7 de septiembre): un 0 al que alguien
fue a la fuente, comprobó que es real, y dejó escrito cuál y cuándo. Existe
porque el aviso `[SOSPECHOSO]` de `auditar_catalogo.py` deduce los ceros
raros del propio catálogo —si el 90 % de los DEMÁS de su categoría tienen
ese nutriente y este no, se dice— y sin una forma de contestarle volvería a
preguntar lo mismo cada vez, que es como una auditoría deja de leerse. Es el
mismo patrón que `purinas_fuente` o `fuente_epa_dha`: la procedencia vive en
la ficha, no en una lista central. Lo vigila el BLOQUE 46, que no se
conforma con verlo salir limpio — vacía la tiamina de un hígado en una copia
del catálogo y exige que la auditoría lo encuentre.

**Y las tres bases de datos no son intercambiables.** El orden lo fija
`Bases.md`: BEDCA (primaria) → Köber 2017 para el hueso → CIQUAL → USDA. No
es preferencia, es que **ninguna tiene los 41 nutrientes**: BEDCA trae yodo
pero ni un aminoácido, USDA trae los 12 aminoácidos y la colina pero no
publica yodo, CIQUAL trae todos los ácidos grasos pero tampoco aminoácidos.
Casi todos los huecos del catálogo están justo donde ninguna llegaba — no
son fallos de copia: donde una ficha entera sale del mismo registro de USDA,
coinciden 153 de 156 celdas. Y BEDCA distingue «midieron 0» (`value_type`
`AR`) de «no hay cifra» (`TR` con la celda vacía), distinción que se pierde
al volcarla a un CSV y que convierte huecos en ceros mudos. Detalle y las
medidas: `PENDIENTE_NUTRICION.md` §5-quater.

**Y desde el 13 de septiembre el orden de esas bases es un NÚMERO, no una frase, y
el catálogo se ha comprobado contra ellas celda a celda por primera vez.**
Lo pidió Elena: «coge todos los alimentos del catálogo y los buscas por orden en
esas listas, si no aparece en la que manda número 1 la buscas en la 2 y así… y
compruebas que todos los datos están bien, anotas los fallos y cambias lo que
haya que cambiar», con dos avisos que son las dos reglas de este trabajo: **«ten
cuidado con errores de poner pollo y que te salga repollo»** y **«UN HUECO NO ES
UN CERO. SOLO UN CERO ES UN CERO»**.

El orden vive en `fuentes_de_composicion.json` y el barrido en
`auditar_composicion.py`. Lo que salió, medido:

| | |
|---|---|
| Celdas que cuadran con su fuente | **3.157** |
| Celdas que reciben la **cifra** de la fuente que manda | **312**, en 46 fichas |
| Ceros que pasan de **mudos** a declarados con su fila de origen | **418** (`cero_verificado` pasa de 8 celdas a 426) |
| Ceros que la fuente declara **sin cifra** y pasan a `sin_dato` | **65** |
| Fichas emparejadas con su fila exacta | **128 de 163** (las 35 restantes son 22 suplementos, mandato 5, y 10 huesos, mandato 2: no tienen fila en ninguna base) |
| Discrepancias que **no se tocan** | **253** — dos fuentes honestas que no dicen lo mismo, y cuál vale es un juicio, no una cuenta |

**Lo que más pesa de esos 312 son los ácidos grasos de la carne, el huevo y la
verdura, que estaban a CERO y sin declarar**: el muslo de pollo declaraba 0 g de
linoleico y USDA da 3,05, y el linoleico es un requisito de FEDIAF **con mínimo**.
Un cero ahí no es un hueco inofensivo: el motor se lo cree y va a buscar el
linoleico a los aceites.

**Los aminoácidos y los ácidos grasos NO se copian: se transfieren por gramo.**
Es la regla que ya estaba escrita en `UNIDADES.md` para el aminograma («se divide
por SU proteína y se multiplica por la NUESTRA; copiarlo tal cual mete el error de
las dos proteínas a la vez») y desde el 13 de septiembre se aplica igual a los
ácidos grasos, por gramo de **grasa**, con el mismo argumento sin cambiar una
palabra: un ácido graso es una fracción de la grasa, no una cantidad
independiente.

### Los cinco fallos de datos que encontró, y los dos de las herramientas

1. **El manganeso 0,6 que no existe en ninguna fuente**, repetido en **ocho
   fichas** de especies distintas (Pavo, Pavo muslo, Pavo pechuga, Pato, Cuello
   de pavo, Cuello de pato, Carcasa de pato, Canónigos). BEDCA **no publica
   manganeso** —su tabla no tiene esa columna—, USDA da 0,022 en el muslo de pavo
   y 0,019 en el pato, y la Tabla 1 de Köber no lo mide. Un mismo número en ocho
   fichas no es una medida: es un valor que se propagó. Y no era inofensivo por el
   lado que parece — 0,6 es unas **treinta veces** el valor real del ave, así que
   el motor creía el manganeso cubierto cuando no lo estaba. Donde hay fuente se
   pone la cifra de la fuente; donde no la hay pasa a **hueco declarado**, porque
   un número que no se puede sostener no es un dato.
2. **Cuatro valores de albahaca SECA en la ficha de albahaca FRESCA**, y es la
   tercera vez que esta ficha cae en lo mismo: el 4 de agosto se le corrigió la
   energía (7,7 veces alta, venía de `Spices, basil, dried`) y el 6 de septiembre
   otros siete valores. Se quedaron dentro `fibra: 40,5` · `vitB6: 2,32` ·
   `vitE: 7,48` · `niacina: 6,95`, que son del orden de la seca; la fresca
   (FDC 172232, la fila que la propia ficha declara) da 1,6 · 0,155 · 0,8 · 0,902.
   La prueba de que la ficha sí es la fresca está en las otras cinco columnas, que
   coinciden exactas. **40,5 g de fibra por 100 g en una hierba fresca es el 40 %
   de su peso**, y la fibra es suelo o techo en ocho patologías.
3. **El agua del timo de ternera era la del timo de VACA** (67,8 en vez de 79,16),
   con el `humedad_fdc` apuntando a FDC 170194, que es la fila de la **otra**
   ficha del catálogo. Esto **cierra una pregunta que ya estaba escrita** en su
   propia `humedad_nota` («verificar si el nombre o la fuente es lo que hay que
   cambiar»): la respuesta es la fuente del agua, porque su energía, proteína y
   grasa coinciden exactas con la fila de ternera. Es el fallo «Timo de ternera
   contra Ris de veau» que el repo tenía avisado, colado por la única columna sin
   huella.
4. **El manganeso de la pechuga de pavo, 0,6 contra 0,006**, un factor 100 contra
   la fila que la propia ficha ya citaba. Se escapó de la revisión del 6 de
   septiembre, que corrigió ocho campos de esa misma ficha contra esa misma fila
   y no miró el manganeso.
5. **Una ficha sin ninguna procedencia**: `Hígado de conejo` no lleva `fuente` ni
   `nota_datos`, y su `sin_dato` solo declara taurina y L-carnitina — o sea que
   sus otros 44 nutrientes se presentan como medidas y no se puede saber de dónde
   salió ni uno. Ninguna de las cuatro fuentes publica hígado de conejo
   (comprobado en las tres). **No se toca ninguna cifra**: lo que falta no es un
   número, es saber de dónde viene, y eso no lo rellena el asistente.

Y los dos de las herramientas, que son peores porque acusan a datos que están
bien — la lección del araquidónico 20:4 otra vez, «no lo eran, la herramienta lo
era»:

6. **`contrastar_fuentes.py` leía la energía de USDA en kJ.** USDA guarda **dos**
   filas llamadas `Energy`, la 1008 en kcal y la 1062 en kJ, y un diccionario por
   nombre se queda con la última. Para el bacalao devolvía **343** y lo comparaba
   contra nuestros 83 kcal: «discrepa −76 %» en **toda** ficha con identificador
   de USDA. `fijar_identificadores.py` ya lo sabía y lo esquivaba por su cuenta;
   aquí no se arregló nunca. Y la energía es el **divisor** de los 43 requisitos,
   que van todos por 1000 kcal: leerla mal los desplaza los 43 a la vez.
7. **El cloruro estaba declarado como «no lo tiene nadie» y CIQUAL lo publica.**
   Estaba en `NO_LO_TIENE_NADIE` y sin entrada en el mapa, así que un hueco de
   cloruro **no se podía cerrar nunca** con la herramienta — mientras
   `UNIDADES.md` decía en otra sección que «CIQUAL, que sí lo analiza, da 61 mg
   para el champiñón donde la derivación da 7,7». Dos sitios del repo afirmando lo
   contrario, y mandaba el código.

### Y un fallo que cometió este mismo barrido, con su guardia puesto

Merece estar aquí porque es la trampa de las unidades en su forma más fina, y la
cazó la comprobación de coherencia que ya estaba escrita en `UNIDADES.md`.

Al rellenar el aminograma de la **zanahoria** desde USDA 170393 «Carrots, raw», los
doce aminoácidos sumaban **0,89 g sobre una proteína de 0,8 g** — el **111 %** de
la proteína, cuando los doce *son* una fracción de ella. El escalado por gramo de
proteína no lo salvó por un detalle del suelo: la transferencia se salta cuando la
proteína baja de 1 g, y la zanahoria tiene 0,8. Y aunque se hubiera aplicado no
bastaba, porque **la incoherencia viene de la propia fila**: USDA da 0,93 g de
proteína y 0,89 g de aminoácidos, o sea el 96 % de SU proteína.

De las doce fichas a las que el barrido puso aminograma, **solo la zanahoria se
salía**; las otras once caen entre 0,31 y 0,61. Queda en hueco, y el guardia que lo
impide dice la regla entera: **un aminograma se escribe ENTERO o no se escribe**,
porque celda a celda no hay forma de ver que la suma se pase.

⚠️ **Y son DOS reglas, no una** — mezclarlas acusa a fichas correctas, que es el
otro error que hubo que deshacer el mismo día:

| Regla | Cuándo vale |
|---|---|
| La suma de las partes **no puede pasar del total** | **Siempre.** Es una imposibilidad aritmética, no un criterio |
| La banda del **25-85 %** de `UNIDADES.md` | Solo donde hay **proteína de verdad** (≥ 1 g). La manzana tiene 0,3 g y 0,073 g de aminoácidos — el 24,3 %, y no tiene nada mal: con cifras así el cociente no significa nada |

La misma comprobación encontró **dos incoherencias preexistentes** que no venían de
este trabajo y que no se tocan, porque arreglarlas es decidir cuál de los dos
números se cambia: la **dorada** declara 1 g de grasa y 1,97 g de ácidos grasos
—imposible—, y eso además dice cuál es el sospechoso, porque su fila de BEDCA da
7,22 g de grasa y con 7,22 los 1,97 encajan; y la **lubina** se pasa un 4,6 %, que
es poco y puede ser redondeo. Las dos van declaradas con su medida en
`fracciones_que_superan_su_total` de `fuentes_de_composicion.json`.

### Y dos emparejamientos malos, que son el «pollo / repollo» de verdad

- **`Perca` apuntaba a BEDCA 831, «Perca, AL HORNO»**, en una ficha **cruda**.
  Hornear pierde agua y concentra todo lo demás por 100 g, así que esa fila
  describe otro alimento. Se colaba porque el guardia de preparaciones de
  `fijar_identificadores.py` tiene «asad», «frit» y «cocid» y **no tenía
  «horno»**. Por esa fila el barrido acusaba a su vitamina B12 de un error de
  ×100 (1 µg nuestro contra los 0,01 de la fila horneada; la fila cruda de USDA
  da 1,9). Barridas las 128 fichas emparejadas con la lista ampliada: Perca era
  la única.
- **`Pato` tenía identificador de USDA y sus cifras son exactas de BEDCA 976.**
  El índice apuntaba a una fila de la que no salen sus números, y por eso el
  barrido acusaba a su vitamina D de un ×10.

**Y tres trampas de nombre, medidas, que hay que conocer antes de buscar nada:**

| Lo que pasa | El caso |
|---|---|
| **BEDCA pliega la ñ en n** | Buscar **«Piña»** devuelve **«Espinaca»**, porque la consulta se vuelve `pina` y eso está dentro de es**pina**ca |
| **USDA casa la consulta dentro de otra palabra** | Buscar **«Lard»** (manteca) devuelve **«Collards»** y cinco filas de «Frybread made with lard». La fila buena es la que **empieza** por la consulta |
| **BEDCA escribe los nombres con coma** | **«Espárrago verde»** da **0 resultados**: su fila se llama «Espárrago, verde» |

**Y una cuarta que costó un alimento entero**: el emparejador se quedaba con los
**4 primeros candidatos por orden ALFABÉTICO**. «Atún» devuelve siete filas de
BEDCA y «Atún, crudo» es la **sexta**, detrás de cuatro conservas y de «Atún, al
horno», así que no llegaba a evaluarse nunca y «Atún» se quedó **sin un solo
identificador** teniendo el suyo a dos posiciones del corte. Ahora se ordenan por
parecido al nombre.

**Una palabra que parece una preparación y no lo es**, con su caso: «stewing»
estaba en la lista de preparaciones y marcaba como sospechoso el emparejamiento de
`Gallina (carne sin hueso)` con `Chicken, STEWING, meat and skin, raw` — y
«chicken, stewing» no es pollo guisado, es **el tipo de ave** (gallina madura),
que es literalmente lo que dice nuestro nombre.

**El cero de una fuente tampoco se obedece a ciegas.** BEDCA publica
`calcio = 0` como **medida** (`value_type` AR) para el pollo entero con piel, y un
tejido animal con 0 mg de calcio no existe. Con la primera versión del relleno esa
ficha pasaba de 10 mg a 0 obedeciendo a la fuente. Ahora no se obedece: se dice. El
criterio es el que ya tiene `UNIDADES.md` («un cero solo es creíble si algún
alimento de esa familia puede tenerlo de verdad»), y hay que leerlo con cuidado
porque habla de **tejido**: una manteca o una grasa de pollo **sí** tienen 0 de
proteína y 0 de minerales de verdad, y la primera versión de esta regla las acusaba
— doce celdas de trece eran falsos positivos.

⚠️ **Y una base europea que está evaluada y NO aplicada, con su medida, porque la
decisión es de Elena**: **Frida** (Dinamarca, DTU), versión 6.1 de mayo de 2026,
CC BY 4.0. A favor: ~105 componentes, la más completa de EuroFIR, **mide los
aminoácidos de todo alimento con proteína desde 2018** —que es lo único por lo que
USDA es hoy imprescindible—, es europea, está viva (USDA SR Legacy está congelada
en 2018) y trae la referencia de cada valor. En contra: es danesa, tiene menos de
la mitad de alimentos que CIQUAL, y **no se ha podido abrir**: su volcado lo sirve
un S3 del DTU en el puerto 9000, que no sale de este entorno. Está escrita entera
en `candidatas_declaradas` de `fuentes_de_composicion.json` para que no haya que
volver a descubrirla.

### El cerebro de vaca: lo primero que sale del catálogo por LEY y no por nutrición

*(13 de septiembre.)* Todo lo demás de este documento son decisiones nutricionales
o de dato. Esta no: es el **Reglamento (CE) 999/2001** y el **1069/2009**, y por eso
no admite matices del tipo «con carne de origen controlado».

La cadena, comprobada contra la versión **CONSOLIDADA** en EUR-Lex
(`eli/reg/2001/999/2024-01-01`) y **no** contra el texto original de 2001 — que
decía **seis** meses y el vigente dice **doce**, que era justo la trampa:

1. **999/2001, anexo V**: «the skull excluding the mandible and including the brain
   and eyes, and the spinal cord of animals **aged over 12 months**» es material
   especificado de riesgo.
2. **1069/2009, art. 8**: «Category 1 material shall comprise […] (i) **specified
   risk material**».
3. **1069/2009, art. 35**: la comida para mascotas sale de **categoría 3**, y su
   apartado (iii) para el **petfood crudo** —que es lo que calcula este motor—
   remite también a categoría 3.

**`Cerebro de vaca` fuera del catálogo** (una vaca pasa de 12 meses por
definición). **`Cerebro de ternera` se queda**, porque la ternera española se
sacrifica por debajo del año, **con la condición de edad escrita en su propia
ficha**. Medido antes de sacarla: aparecía en **0 de los 216** menús.

⚠️ **Y estar fuera del automático no bastaba.** Las dos ya lo estaban desde el 7 y
el 8 de septiembre por otro motivo (su DHA las hacía ganar siempre y los sesos no
se piden en una carnicería normal), y eso es una cuestión distinta: lo que está
fuera del automático **se puede seguir eligiendo a mano**, y lo ilegal no.

**Los otros tres candidatos se miraron y ninguno está afectado, cada uno por su
motivo** — que no es el mismo, y por eso hay que leer la norma entera: el `Cuello
de ternera` porque el umbral de la **columna** son **30 meses** y además la norma
excluye expresamente las apófisis espinosas y transversas de las cervicales; el
`Pecho de ternera con hueso` porque costillar y esternón no son columna ni médula;
y las `Costillas de cordero` porque para **ovino** la norma cubre solo cráneo,
encéfalo, ojos y médula — **no** la columna vertebral. ⚠️ Eso sí deja una puerta:
el día que alguien proponga **sesos de cordero**, la norma los alcanza, y su umbral
no es solo la edad sino «o que tenga un incisivo permanente», que es un dato que el
catálogo no puede saber.

Lo vigila el **BLOQUE 51**: falla si vuelve la ficha (con cualquiera de sus
nombres, médula espinal incluida) y falla si la de ternera pierde su condición de
edad — sin ella, la ficha afirma que vale cualquier encéfalo de bovino. Comprobado
con el fallo puesto de las tres formas. Detalle y citas: `DATOS_QUE_FALTAN.md`.

⚠️ **Y sacar la ficha NO bastaba: la empeoraba.** Lo vio Elena el mismo día, y la
frase describe el fallo entero:

> «a lo mejor la persona que vaya a comprar al supermercado pide cerebro de ternera
> y dice: no tengo, pero tengo de vaca. Y problema.»

Antes estaban **las dos** en la lista y la diferencia se veía. Ahora solo aparece
«de ternera», y quien la lea **no tiene forma de saber que la otra no vale**. Y la
sustitución pasa en el mostrador, donde el motor no está: lo único que puede hacer
es **decirlo donde se lee**.

De ahí sale el campo **`aviso_al_comprar`**, que sale por **las dos puertas** —la
misma forma que el BLOQUE 64 con los avisos de patología, y por el mismo motivo:

| Puerta | Cuándo se lee | Por qué hace falta |
|---|---|---|
| `problemas_seguridad` | con el menú ya hecho | es el canal que la app **ya pinta en los ocho caminos** (generar, semana, varios perros, editar, revalidar), así que **no hay que tocar la app** |
| `GET /alimentos` | **antes**, al elegir el alimento a mano | sin ella, quien lo elige a mano no lee nada hasta el final |

Con solo la primera, el camino de «elegir a mano» no avisa; con solo la segunda,
quien deja elegir al motor no lo lee nunca. Lo vigila el BLOQUE 51 con el fallo
puesto de cuatro formas, y exige además que **una ficha con una condición LEGAL en
su `nota_datos` tenga aviso**: una condición que solo vive en una nota técnica no
la lee quien va a la carnicería, que es justo donde ocurre la sustitución que la
condición existe para evitar.

### ⚠️ Y una medida de la vitamina A que estaba mal en cinco sitios

*(13 de septiembre.)* El repo afirmaba, en `UNIDADES.md`, `HALLAZGOS_LECTURA_FUENTES.md`,
`PREGUNTAS_PARA_ELENA.md`, `DATOS_QUE_FALTAN.md` y `fuentes_de_composicion.json`,
que **«el 83 % de la vitamina A de los 216 menús viene de verdura y fruta»**, que
**«103 de los 216 no llegarían al mínimo si el caroteno no contara»** y que el peor
menú «declara 11.191 µg y solo 29 son retinol». **Las tres cifras eran falsas.**

| | Decía | **Es** |
|---|---|---|
| Verdura y fruta | 83 % | **6,5 %** |
| Hígado | — | **77,9 %** (el de vaca él solo, 49,5 %) |
| Multivitamínico | — | **12,7 %** |
| Menús bajo el mínimo sin caroteno | 103 de 216 | **0 de 216** |
| El menú con más vitamina A | lactancia, 11.191 µg, 29 de retinol | **`Pequeño_Lactante#4`, 5.155 µg/1000 kcal, el 80,5 % puesto por el hígado de vaca** |

**El fallo, y se reproduce**: el método contaba **la vitamina A del hígado como si
fuera caroteno**, y la del hígado es retinol puro. Poniendo a cero la vitamina A
del hígado **y** de los multivitamínicos salen mediana 74 % y **máximo 100 %**, y
el documento decía «mediana 83 %, máximo 100 %» — ese 100 % es la huella, porque
bien contado ningún menú pasa del 35 %. Lo delataba además su propia frase: en un
menú con 5.500 µg de hígado dentro, «solo 29 son retinol» solo sale si el hígado
está en el lado equivocado.

**Y la dirección del riesgo también estaba al revés**: contar de menos el caroteno
**no es el lado seguro** — es seguro contra el mínimo y **peligroso contra el
máximo**, porque la vitamina A es de los pocos nutrientes con techo. Lo que permite
estar tranquilos es **la medida, no el argumento**: el menú más alto va a 5.155
µg/1000 kcal contra un techo de **30.000 en todas las etapas**, o sea el **17 %**;
0 de 216 pasan del máximo y 0 caen bajo el mínimo.

⚠️ **Y LA PRIMERA VERSIÓN DE ESTA CORRECCIÓN TAMBIÉN ESTABA MAL, que es la lección
que más vale de todo esto.** Decía que el máximo era **10.000 µg/1000 kcal (33 %)**
y lo justificaba con un menú concreto —`Grande_CachorroJoven#2`, «76,87 g de hígado
de pato y 466 g de boniato»— que **no existe en `main` ni existía ya en la propia
rama**. El motivo: la medida cambió de `alimentos_v3_final.json` para comprobar que
no dependía del catálogo, **y no cambió `catalogo_menus.json`**, que es el que de
verdad la mueve — regenerar los menús reparte los gramos de otra forma. La cazó la
otra lectura al ir a buscar ese menú y no encontrarlo. **Son DOS ficheros y hay que
decir contra cuál se mide**, y lo que se escriba tiene que salir del catálogo
FUSIONADO.

Consecuencia para el plan: **aplicar el convenio 4:1 de FEDIAF sigue siendo lo
correcto** —la regla es que gana FEDIAF— pero **deja de correr prisa**, porque lo
que la hacía urgente era el «103 de 216». El método para rehacer la medida está
escrito en `UNIDADES.md`, para que no haya que fiarse de esta tampoco.

### La vitamina D, y el cero mudo que sostenía un verde

Es lo que más pesa de todo el barrido, y no por el número de celdas (nueve) sino
por lo que enseña: **un verde de la batería se estaba apoyando en un dato que
ninguna fuente dice**.

**La ficha `Pescadilla` declaraba 0 µg de vitamina D.** BEDCA da `TR` con la celda
vacía —o sea NO HAY CIFRA— en sus **tres** filas de merluza (2347 fresca, 825
congelada, 1174 pescadilla), y CIQUAL, que sí la mide, da **2,15 µg** a
`Merlu, cru`. Era un cero mudo. Y era **lo único** que sostenía el menú del adulto
de 20 kg con ocho especies excluidas del BLOQUE 9: barrido de esa cifra contra el
endpoint, sale menú con **0,0** y no sale con 1,0 · 2,15 · 3 · 4 · 5 · 6 · 8.

Y al medirlo se ve que **no era cuestión de cuál es la cifra buena, sino
aritmética**. Con las ocho especies fuera quedan 108 alimentos accesibles, casi
todos pescado, y el tope crónico son **20 µg/1000 kcal** (NRC 2006, restricción
DURA por la regla 2). **17 de los accesibles pasan ese tope ellos solos**, y no
solo el pescado azul: la merluza, con 2,15 µg y 65 kcal por 100 g, sale a **33
µg/1000 kcal**. Un pescado blanco tiene muy pocas kcal, así que cualquier vitamina
D se le convierte en una concentración alta. O sea que una ración hecha casi solo
de pescado se pasa de vitamina D de verdad, y no dar menú es la regla 1
funcionando. El BLOQUE 9 lleva ahora la medida escrita y ya no exige ese menú —
sigue exigiendo lo único que dijo que comprobaba: que si no lo da, **lo diga**.

**Nueve celdas se cerraron bajando por la cadena de mandato**, que es literalmente
lo que pidió Elena («si no aparece en la que manda número 1 la buscas en la 2 y
así»). BEDCA tiene la columna de vitamina D y casi nunca la mide: `TR` en diez de
los veinte pescados y en seis carnes magras.

| Ficha | Cifra | De dónde |
|---|---|---|
| Merluza | 2,15 | ciqual 26044 «Merlu, cru» |
| Bacalao | 1,41 | ciqual 26043 «Cabillaud, cru» |
| Lubina | 5,59 | ciqual 26072 «Bar commun ou loup, cru, sans précision» — y USDA 175142 da **5,6** por su cuenta |
| Lenguado | 0,75 | ciqual 26058 «Sole, crue» |
| Pulpo | 0,5 | ciqual 10018 «Poulpe, cru» |
| Calamar | 0,36 | ciqual 10001 «Calmar ou calamar ou encornet, cru» |
| Sepia | 0 | ciqual 10016 «Seiche, crue» |
| Aceite de girasol | 0 | usda 171025, bajando al mandato 4 |
| Aceite de cacahuete (vit. **A**) | 0 | usda 171410 |

**Y los dos aceites eran los dos peores, porque su hueco se imputaba a nivel de
huevo**: el aceite de girasol recibía **5 µg de vitamina D** (lo que declara el
huevo de pato) y el de cacahuete **591 µg de retinol** (lo que declara la yema).
Los dos son aceites de semilla refinados. Es el mismo fallo que el de la proteína
de los aceites, y lo bonito es que **BEDCA lo dice ella misma, cruzado**: declara
`LZ` (cero lógico) la vitamina A del de girasol y `LZ` la vitamina D del de
cacahuete — a cada uno le mide una y a la otra le pone `TR`.
⚠️ La vitamina A tiene **conflicto de convenio declarado** y aquí **no muerde**: un
`RAE` de 0 obliga a retinol 0 **y** β-caroteno 0, así que es cero en los cuatro
convenios.

**Tres marcas que NO son un número**, y hay que conocer las tres antes de cerrar
una celda: el `TR` de BEDCA con la celda vacía, el `-` de CIQUAL (no disponible) y
el **`< X` de CIQUAL** (límite de detección). La tercera es la traicionera porque
parece casi una cifra: `Huile de tournesol` da «< 0,25», y por eso ese aceite hubo
que cerrarlo bajando hasta USDA.

**Y tres se quedan en hueco a propósito**, porque ninguna fuente publica su
especie: `Bacaladilla` (*Micromesistius poutassou*; el `Merlan` de CIQUAL es
*Merlangius merlangus*, **otra especie**), `Gamba roja` (*Aristeus antennatus*;
CIQUAL da «< 0,2» y la única fila de USDA con cifra es la de «may contain
additives to retain moisture», que es otro producto) y `Pescadilla` (ninguna de
las cuatro publica vitamina D de merluza **congelada**, comprobado contra BEDCA
fila a fila). Están en `DATOS_QUE_FALTAN.md`.

⚠️ **Y el BLOQUE 51 sigue cerrando la trampa del `TR`, que es otra cosa.** Que
BEDCA no mida no convierte la celda en incerrable para siempre: manda a la
siguiente fuente. Lo que sigue prohibido es leer el `TR` como «trazas» y escribir
un cero, porque eso produce una celda **con valor y sin procedencia** —o con
procedencia `bedca`, que es imposible porque esa celda está vacía—, y el bloque
falla en los dos casos. Comprobado con el fallo puesto de las dos formas.

### Y las vísceras, que no se habían barrido

Nace de una pregunta de Elena —«¿has comprobado el valor de todas las vísceras? El
hígado de todos, y luego buscar si en alguna fuente se dan datos de vísceras de pollo
y pavo»— y de otra que vale como regla: si dejar un hueco a propósito no es peligroso.

**La segunda primero, porque la respuesta es la que hay que tener en la cabeza: un
hueco NO cuenta como cero.** Contra un MÁXIMO el motor le mete el percentil 90 de su
familia, y contra un MÍNIMO cuenta 0 — o sea que es conservador en las dos
direcciones. Medido en los tres pescados que se quedaron sin cifra: el hueco les
cuenta 8 µg/100 g, nivel de salmón, que son **104 · 89 · 146 µg/1000 kcal** contra un
tope de **20**. El motor los trata como si fueran salmón. **El peligroso es el cero
mudo**, que afirma «no lo tiene» y **afloja** el techo.

**Y en las vísceras había siete ceros mudos, y los siete aflojaban un tope crónico.**
Pasan a hueco declarado:

| Ficha | Celda | Qué dice cada fuente |
|---|---|---|
| **Riñón de cordero** | vitamina D | BEDCA 1063 `TR` · USDA sin cifra · CIQUAL «-». **Tres fuentes, ninguna la mide** — y que la ficha bebió de BEDCA lo prueba su vitamina E, 0,43, clavada |
| **Pulmón de vaca** y **Pulmón de cordero** | vit. E y **yodo** | la fila de BEDCA no trae esas columnas · USDA **no publica yodo de nada** · CIQUAL no tiene ninguna fila de pulmón |
| **Bazo de cordero** | **yodo** | BEDCA no tiene ninguna fila de bazo · USDA no publica yodo · CIQUAL no tiene bazo |
| **Hígado de conejo** | vitamina D | y no era un cero: era un **1,2 copiado del hígado de VACA**, la cifra de BEDCA 1053 clavada |

Tres de los siete son **yodo**, que es uno de los cinco topes crónicos.

**Por qué estaba invisible, y aquí hay que ser exacto porque mi primera lectura fue más
amplia de lo que los datos sostienen**: el barrido lee `fuentes_id`, y faltaban **dos**
—no cinco—. Los tres corazones (vaca 2265, cordero 966, pollo 970) ya tenían su id de
BEDCA y su vitamina D ya se comparaba contra ella. Los que callaban eran el **hígado de
vaca** (solo declaraba USDA, y de ahí sale su vitamina D pero NO su vitamina A) y el
**pulmón de cordero** (USDA no publica vitamina D del pulmón, así que sus 12 µg no se
comparaban con nada).

**Lo que se cerró con cifra:** el **timo de ternera**, vitamina D = **0,25** de
`ciqual:40304` «Ris, veau, cru» — ris de veau *es* el timo de ternera, BEDCA no tiene
ninguna fila de timo y USDA 172542 no publica la suya. Y **la procedencia del hígado de
conejo**, que era **la única ficha del catálogo sin ninguna**: sale de `ciqual:40110`
«Foie, lapin, cru», con proteína, grasa y la vitamina A (4530) exactas. Eso cierra el
fallo nº5 del barrido del mismo día.

**La discrepancia que hay que decidir, no conseguir**: el **hígado de vaca** declara
**10250 µg de vitamina A** y **es la cifra de BEDCA** (`BE`); USDA, en la fila que la
ficha declaraba como única fuente, da **4968** — 2,06×. ⚠️ Y el conflicto de convenio
del β-caroteno **no lo explica**: un hígado no tiene caroteno, su vitamina A es retinol
puro, y con retinol puro los cuatro convenios dan el mismo número. CIQUAL no desempata
(6350). Importa porque el hígado entra en casi todo menú, es de donde sale casi toda la
vitamina A de la ración, y la vitamina A tiene **máximo en FEDIAF**. No se toca la
cifra —manda BEDCA— pero ahora la ficha declara también su id.

**Dos fichas con cifras de otra especie, que NO se tocan** porque renombrar es decisión
de producto. Son la cuarta y la quinta de una familia con tres casos ya cerrados (bazo,
páncreas y pulmón «de ternera»):
- el **`Riñón de ternera` es un riñón de BUEY** (identidad exacta de `ciqual:40402`, y
  su vitamina D 1,05 es la de esa fila clavada; su vitamina A, 204, no sale de ninguna
  de las cuatro filas candidatas y sigue sin explicar);
- el **`Pulmón de vaca` lleva la vitamina D del pulmón de TERNERA**, y esto **cierra
  una pregunta que esa ficha llevaba escrita desde el 8 de septiembre** («o se sembró
  de la fila de la especie equivocada, o es casualidad»): no es casualidad, `bedca:2300`
  da 11 y 14, las nuestras exactas, y USDA no publica vitamina D del pulmón. Y el
  catálogo tiene aparte un `Pulmón de ternera` cuya vitamina D es un hueco.

**Vísceras de pollo y pavo, contestado: las seis fichas de ave están bien.** USDA
publica hígado, molleja, corazón y despojos de los dos, CIQUAL añade corazón, molleja e
hígado de pollo y corazón e hígado de pavo, y BEDCA tiene corazón e hígado de pollo.
**Del pollo la vitamina D solo la mide el hígado.** Las seis cuadran: hígado de pollo 0
= USDA · hígado de pavo 1,3 = USDA · corazón de pavo 0,4 = USDA **y** CIQUAL · molleja
de pavo 0,5 = USDA · corazón de pollo 0,2 = BEDCA 970 · molleja de pollo en hueco, que
es correcto porque su fila (USDA 171456) no la mide.

⚠️ **Y de aquí sale un campo nuevo, `hueco_verificado`, gemelo de `cero_verificado`.**
`sin_dato` era una **lista pelada**, así que «hemos mirado las tres fuentes y ninguna
mide esta celda» y «nadie ha mirado nunca» se veían **exactamente igual** — y para
contestar si el hueco es peligroso hay que poder leer lo primero. El BLOQUE 100 exige
que el campo no pueda mentir, en cinco formas: su clave está en `sin_dato`, su valor es
0, **no** está también en `cero_verificado` (una celda no puede ser a la vez «la fuente
mide 0» y «ninguna fuente la mide»), no tiene `composicion_fuente`, y su motivo dice de
verdad qué se miró. Comprobado con las cinco reintroducidas.

⚠️ **Y una palabra más que parece una preparación y no lo es**, que puso roja la batería
el mismo día: «Oil, peanut, **salad or cooking**» de USDA dice **para qué se vende** el
aceite refinado, no que esté cocinado — la fila declara 99,9 g de grasa y 0 de agua, que
es aceite crudo. Vive con «stewing» en `NO_SON_PREPARACIONES_AUNQUE_LO_PAREZCAN`.

En la raíz, los nueve: `alimentos_v3_final.json` (el catálogo),
`requerimientos_v2_final.json` (la tabla de FEDIAF), `catalogo_menus.json`
(los 36 menús precalculados de la vista previa y sus 180 variantes),
`der_casos.json` (el contrato del DER, ver arriba),
`recomendaciones_libro.json` (los techos del libro para el perro sano),
`requisitos_condicionales.json` (los requisitos que dependen de la propia
dieta), `fediaf_conversiones_vitaminas.json` (la Tabla VII-14: cuántos
microgramos de cada fuente hacen una UI) y `sacn5_fuentes_de_minerales.json` (su
hermana para los minerales, del capítulo 6 de SACN5) y `razas.json` (las 255
razas que ofrece la ficha, con su tamaño y su rango de peso adulto).

**El noveno es del 11 de septiembre y no trae ni un número nuevo: trae 255
números que ya existían y vivían donde nadie podía mirarlos.** Es la tabla de
razas, que estaba dentro de `src/App.jsx`. Se mueve tal cual, sin tocar una
cifra, por lo mismo que se movieron el catálogo y la tabla de patologías: un
número que decide si un menú se entrega tiene que poder auditarse. Y aquí
decide tres — el peso adulto esperado (y de ahí las kcal y la etapa), el techo
de calcio del cachorro de raza grande, y si a ese perro le toca la cifra de
energía propia que FEDIAF le da a dos razas. ⚠️ **No tiene fuente publicada**, y
eso está escrito en su `_meta`: ninguna de las cuatro fuentes del motor trae
una tabla de peso por raza.

**El octavo es de la noche del 9 de septiembre y trae algo que la tabla de
vitaminas no tiene: dos ceros.** El problema de base es el mismo —la etiqueta
declara la **sal** y el catálogo anota el número como si fuera el elemento, así
que «óxido de zinc 100 mg» son 72 mg de zinc—, pero SACN5 añade dos fuentes cuyo
mineral **se analiza y no llega al perro**: el **óxido de hierro** («the iron in
iron oxide is not biologically available»; se añade como colorante rojo, y «a pet
food containing iron oxide will appear to be high in iron») y el **óxido de
cobre** («copper availability was essentially zero»; AAFCO pidió dejar de
usarlo). Eso no es un factor de conversión, es un cero. Y una tercera cosa que sí
es un alimento: el **hígado de cerdo** también tiene cobre con disponibilidad
cero, mientras que los de **vaca, cordero y pavo** —tres de los seis del
catálogo— la fuente los nombra como «highly available». Hoy no afecta: no hay
ninguna ficha de cerdo. Queda escrito para el día que alguien proponga añadirla.

**El séptimo es del 9 de septiembre por la noche y existe por un hueco
concreto.** Tres fichas del catálogo llevan la vitamina A y la D convertidas
de UI a microgramos, y la conversión estaba *hecha y escrita* en el campo
`nota_datos` de cada ficha sin comprobarse contra nada. Es el peor sitio para
un error, porque tiene forma de dato bueno: convertir la vitamina D con el
factor de la A (0,3 en vez de 0,025) multiplica por **doce** el aporte de un
multivitamínico y el semáforo no dice nada. El **BLOQUE 70** rehace las seis
conversiones desde la nota de cada ficha; las seis salen bien, y una séptima
ya no puede entrar sin comprobarse. Lo que sigue sin resolverse es dato y no
código: ninguna ficha dice en qué **forma química** viene cada vitamina del
grupo B, y con el peor factor de la tabla el ácido pantoténico caería por
debajo del mínimo de FEDIAF con el menú en verde. Está en
`DATOS_QUE_FALTAN.md` y **no lo rellena el asistente**.

**El quinto es del 8 de septiembre y merece una línea de por qué está solo.**
No cabía en ninguno de los otros dos sin romper lo que significan: en
`requerimientos_v2_final.json` no, porque ese fichero **es** la Tabla III-3b de
FEDIAF y `auditar_fediaf.py` comprueba sus 43 filas contra el PDF celda a celda
—meter ahí un número de un libro de texto es exactamente cómo se coló en agosto
una fila «Fibra» con mínimo y máximo inventados—; y en `patologias.json` tampoco,
porque esto **no es una patología**: se aplica al perro que no tiene ninguna.

Los dos primeros llevan **sello** en `/verificar`: si cambian sin que se
actualice el hash en `main.py`, la API lo dice. Los otros dos no, y es a
propósito — un menú del catálogo corrupto lo rechaza
`_garantizar_verificado()` igual que cualquier otro, y el contrato del DER
se comprueba entero en cada batería.

## «Cerrado» son DOS números, no uno — y desde el 11 de septiembre ninguno lo cuenta un script

Escrito el 11 de septiembre de 2026 de noche, porque hasta ese día era uno y
por eso se pudo decir tres veces que algo estaba cerrado y que luego saliera
algo esperando. Elena: «me dices que algo está cerrado y siempre sale algo que
demuestra que no lo está, y eso no puede ser».

**El primero: cada elemento de la fuente tiene VEREDICTO.** Eso lo contaban
cuatro scripts (`leer_fuente.py`, `leer_sacn5.py`, `leer_nrc2006.py`,
`leer_fascetti.py`) y los cuatro decían **cero pendientes** — y seguían saliendo
cosas. El punto ciego estaba declarado dentro del propio auditor: tres de los
cuatro registros guardaban el veredicto como **texto libre**, así que su «0
pendientes» significaba «0 sin nota», no «0 sin decidir». Un contador que
cuenta frases con nota no cuenta lecturas.

**El segundo: cuántas cosas hemos leído, hemos decidido NO aplicar, y siguen
esperando.** Ese número, el 11 de septiembre, era **92**.

⚠️ **Los cuatro scripts, sus cuatro JSON, los dos inventarios de tablas y los
tres auditores que los vigilaban están BORRADOS** (`leer_*.py`,
`lecturas_*.json`, `sacn5_tablas.json`, `fediaf_tablas.json`,
`auditar_sacn5_tablas.py`, `auditar_fediaf_tablas.py`,
`auditar_pendiente_de_aplicar.py`, `auditar_fuente_cerrada.py`,
`auditar_fuentes.py`, `fuentes_del_motor.json`), con los ocho bloques que los
ejecutaban. Elena, al ver que el problema no se arreglaba añadiendo contadores:

> «todos los scripts de mierda que hayas hecho fuera no los quiero. quiero que
> leas todo bien, frase a frase, letra a letra, y que anotes todo lo
> interesante y que luego decidamos si se aplica o no se aplica»

**Lo que hay en su lugar es `LECTURAS.md`**, y el método que describe es la ley
para todos los documentos: leer entero y seguido, anotar según se lee con la
cita literal, y al terminar repasar punto por punto decidiendo **aplicado**, **no
se aplica porque…** o **pendiente de decidir**. Lo que quede pendiente va a
`PREGUNTAS_ABIERTAS.md` con dueño. Los hallazgos que se quedan escritos y sin
aplicar siguen viviendo donde ya vivían y ahí sí los cuenta la batería:
`limites_escritos_que_el_solver_no_aplica` de `patologias.json`, los
`documentado_sin_cifra` de `requisitos_condicionales.json` y los apagados de
`recomendaciones_libro.json`.

**Lo que SÍ se queda son los auditores que rehacen un NÚMERO contra la fuente**,
que es otra cosa y sigue siendo la única forma de que una cifra no mienta:
`auditar_fediaf.py`, `auditar_transcripcion_fediaf.py`, `auditar_conversiones.py`,
`auditar_citas.py`, `auditar_patologias.py`, `auditar_margen_profesional.py`,
`auditar_catalogo.py` y `auditar_kober.py`.

## Antes de fusionar: la app DE VERDAD contra el motor DE VERDAD

**Escrito el 13 de septiembre de 2026, y lo pidió Elena el día que producción
estuvo rota sin que nada saltara:**

> «a partir de ahora cuando hagas PR y fusiones tienes que hacer pruebas para
> todo tipo de etapas y todo tipo de perros con todo tipo de patologías en la
> app real con las cuentas de prueba, en veterinario y usuario, para ver si
> falla algo»

⚠️ **Y el motivo está medido: ese día había 101 bloques del motor en verde y 550
pruebas de la app en verde, y la app no daba UN SOLO MENÚ.** Cairo, el cachorro
de Elena, se quedaba sin comer y ninguna de las dos baterías podía verlo.

**Por qué ninguna de las dos lo ve, y es estructural:**

| | Qué prueba | Qué NO puede ver |
|---|---|---|
| `pruebas_completas.py` | el motor, por dentro y por sus endpoints | lo que la app le MANDA de verdad |
| `tests/*.spec.js` de `canislab-web` | la app, contra un motor **de mentira** que siempre devuelve menú | que el motor de verdad diga que no |

Las dos juntas dejan un hueco del tamaño exacto del fallo: **una petición que la
app manda bien y el motor contesta «no hay menú» por un motivo real.** Eso no es
un fallo de nadie de los dos y solo se ve juntándolos.

**Lo que hay que ejecutar antes de fusionar** es `tests/motor-de-verdad.spec.js`
en `canislab-web`: levanta la app y la deja hablar con la API **desplegada**, y
recorre la matriz de etapas × tamaños × premios × patologías, en los dos roles.
No sustituye a nada: se suma.

⚠️ **La mitad de la CUENTA sigue siendo de mentira**, y va declarado: el
Supabase real necesita una credencial que no vive en el repo. Lo que se prueba
de verdad es el motor, que es donde estaba el fallo. El día que se ponga la
credencial como secreto de GitHub, esa mitad también.

## Cómo se prueba

```bash
python3 pruebas_completas.py     # ~40 min, tiene que salir TODO EN VERDE
```

Los **100 bloques** tardan unos **40 minutos** (2.387 s en la última medida; el
«~25 min» que ponía aquí se quedó corto igual que antes se quedó corto el
«~10 min», y antes el «~2 min»: cada vez que un bloque nuevo resuelve menús de
verdad, esta cifra sube. Si vuelve a bajar sin motivo, es que algo no se está
ejecutando). No necesita red ni claves de verdad: se fabrica
su propio Stripe y su propio Supabase de mentira, así que corre igual en
cualquier máquina y sin conexión.

⚠️ **Y el 13 de septiembre había DOS bloques con el número 98**: el de las fichas
de hueso contra Köber y el de las patologías que enumera el motor. Un número de
bloque es la única forma que tiene el repo de decir quién vigila qué —«lo vigila el
BLOQUE 98» señalaba a dos sitios distintos, en `CLAUDE.md` para las patologías y en
`main.py` para el hueso—, así que dos con el mismo número es una referencia rota
que no da ningún error. El de las patologías pasa a ser el **99** (se renumera ese
porque el otro está citado dentro del sello del catálogo en `main.py`), y el nuevo
del catálogo contra sus fuentes es el **100**.

**Desde el 8 de septiembre la ejecuta también GitHub Actions** en cada
pull request y en cada empujón a `main` (`.github/workflows/bateria.yml`).
Eso no sustituye a ejecutarla antes de abrir el PR — te lo cuenta diez
minutos después, no antes —, pero cierra el hueco de que un rojo se cuele
por olvido: en el historial hay un commit que se llama literalmente «WIP:
la carga puesta, con la batería en rojo (13 fallos)».

Se ejecuta **entero** antes de entregar cualquier cambio, no solo el
trozo que parece afectado. Existe porque antes cada arreglo se probaba
solo con el caso que había fallado, y eso dejaba romperse otros diez sin
que nadie se enterara hasta que los encontraba la usuaria.

Un test que pasa con el fallo puesto no sirve: al añadir uno, comprueba
que falla si reintroduces el problema.

**Y un test que falla cuando el motor ACIERTA es peor todavía**, porque enseña
a desconfiar de la batería — y una batería de la que se desconfía se mira por
encima. Pasó dos veces la noche del 9 al 10 de septiembre, con la misma forma
las dos: **una prueba que da por hecha una propiedad incidental del menú que
devuelve el solver**.

- El BLOQUE 58 sumaba **40 g fijos** de aceite a un menú de lactancia para
  empujar la proteína por debajo de su suelo. Una ejecución devolvió un menú
  con tanta proteína que 40 g solo la bajaron a 127,0 — por encima del suelo
  de 125 —, el filtro calló con razón y el test concluyó que no comprobaba
  nada. Ahora la dosis **se calcula** para cruzar el suelo con margen.
- El BLOQUE 60 exigía que en el menú resuelto la Tabla VII-13 pidiera más
  arginina que la III-3b. Otra ejecución devolvió 74 g de proteína — por
  debajo del cruce, que está en torno a 82 —, donde manda la III-3b y **eso es
  lo correcto**. Ahora la aritmética se comprueba aparte, a una proteína fija
  y representativa, y del menú real solo se exige el invariante: que se aplique
  **la más estricta** de las dos.

- El BLOQUE 75 pedía el menú a `/menu/v2` y exigía que saliera. **Rojo en
  GitHub Actions y verde aquí**: allí el presupuesto son 24 s para la escalera
  entera y la máquina va varias veces más lenta, así que el perro de 3 kg se
  quedaba sin menú **por reloj** — y el bloque lo acusaba de que «la cifra de la
  fuente no cabe». Reescrito el mismo día para preguntárselo al solver con
  tiempo suficiente; que el menú **entregado** cumpla se comprueba aparte, sobre
  los que la API sí devuelve. El reloj es del BLOQUE 43.
- Y en el segundo intento seguía mal, por otra cosa: exigía el menú **en el
  peldaño estricto**. Medido, el perro de 3 kg con fosfato cálcico sale
  infactible demostrado en los peldaños 0, 1 y 2 y da menú en el 3 — **igual con
  el límite nuevo y sin él**, o sea que no lo causaba el cambio: es la ventana
  estrecha del perro pequeño, y bajar de peldaño diciéndolo es la regla 3. Ahora
  recorre la escalera, como hace el motor.

- El BLOQUE 57 buscaba en el menú un alimento de categoría «Hueso carnoso» y lo
  **cuadruplicaba**, para exigir que el filtro final cazara el exceso de fósforo.
  Dos suposiciones sobre el menú, y las dos falsas. **Que haya hueso**: medido
  sobre seis menús de adulto de 22 kg, en **cuatro no había ninguno**, así que el
  `if` no entraba y el bloque **no comprobaba nada, en silencio** — un test que
  se salta solo es peor que no tenerlo, porque sale verde igual. Y **que ×4 el
  hueso sea ×4 el fósforo por 1000 kcal**: no lo es, el hueso también trae kcal,
  así que lo que sube es un cociente. En el menú donde sí había hueso el ×4 lo
  dejó en 2372 —cruzó por poco— y en GitHub Actions no cruzó: **rojo allí y verde
  aquí**, acusando al filtro de no mirar el techo del perro sano cuando el filtro
  tenía razón. Ahora no se toca el menú: se le **añade** el alimento de más
  fósforo por kcal **del catálogo**, en la cantidad que **se calcula** para
  cruzar el techo. Ocho de ocho menús cruzan, y con el techo desconectado del
  filtro el bloque falla.

La regla que sale de ahí: **el menú que devuelve el solver cambia entre
ejecuciones**, así que una prueba solo puede afirmar de él lo que sea verdad de
CUALQUIER menú válido (que esté verde, que respete sus topes, que aplique el
límite más estricto). Todo lo que dependa de una cifra concreta del menú, o se
calcula a partir de ese menú, o se comprueba aparte con números fijos.

Y dos hermanas suyas, del 10 de septiembre, que valen igual: **una prueba no
puede afirmar en qué peldaño sale un menú** (bajar es legítimo y se dice), ni
**depender de lo rápida que sea la máquina** — si lo que se quiere afirmar es
que un límite cabe, se le pregunta al solver con tiempo, no a un endpoint con
presupuesto. Un rojo que solo sale en la CI no es un rojo de la CI: es una
prueba que estaba midiendo el reloj sin querer.

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
etapa los 43 requisitos: un perro de diez años volvía como cachorro.

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
| `SELLO_SECRETO` | La clave con la que se sellan las pautas firmadas. **Sin ella `/pauta/firmar` devuelve 503 a propósito**: un sello sin clave lo recalcula cualquiera y no prueba quién firmó. `/verificar` dice si está puesta |

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
- **El bytecode cacheado puede mentirle a la batería.** La invalidación de `.pyc`
  de CPython compara la fecha del fuente con la guardada en el `.pyc` **con
  resolución de un segundo**. Si tocas un `.py` dentro del mismo segundo en que
  Python escribió su `.pyc`, Python sigue sirviendo el viejo. Pasó el 9 de
  septiembre: `seguridad.py` decía 1275 en el disco y la batería informaba de
  1400, dos veces, 50 minutos buscando un fallo que no existía. Es la peor clase
  de fallo posible aquí — la batería **afirma algo del motor que el código no
  dice** —, y un verde así taparía un cambio real. Desde entonces la batería borra
  todos los `__pycache__` antes de importar nada. Si algún día una cifra del motor
  y la del fichero no cuadran, esto es lo primero que hay que mirar.
- **Render duerme el servicio** tras ~15 min sin tráfico. Lo mantiene
  despierto un GitHub Action cada 10 minutos.
