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
   Y desde el 8 de septiembre hay una **tercera clase de techo**: los que el
   libro recomienda al perro **sano**, que se aplican **sin que haya ninguna
   patología marcada**, viven en `recomendaciones_libro.json` y se comprueban
   en el mismo sitio y con el mismo `min()` que los de patología. En adulto son
   dos (fósforo 2000 y sodio 1000 por 1000 kcal; 1750 el fósforo en senior).
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
| `recomendaciones.py` | Lee `recomendaciones_libro.json`: **los techos que el libro recomienda al perro SANO**, por etapa. Es la tercera clase de límite del motor, y no existía hasta el 8 de septiembre: los de FEDIAF valen para cualquier perro, los de patología solo si está marcada, y estos valen para el perro que **no tiene nada**. Se combinan con `min()` como los de patología: solo pueden apretar. Empezó con dos cifras de adulto (fósforo y sodio) y el 9 de septiembre entraron las de **crecimiento** — calcio y fósforo, con **dos columnas** según el cachorro vaya a pesar más o menos de 25 kg de adulto |
| `patologias.py` | Lee `patologias.json` y lo pasa a la forma que espera el solver. **Aquí no hay ni una cifra**: hasta el 28 de agosto la tabla eran 200 líneas de `dict` dentro de `motor_completo.py`, mezclando números, motivo clínico, textos y lógica de crecimiento. Se sacó por lo mismo que el catálogo y la tabla de FEDIAF: un número que decide si un menú se entrega tiene que poder auditarse, y no se audita lo que está enterrado entre `if`s |
| `catalogo_menus.py` | Carga los menús precalculados de la vista previa. Los datos están en `catalogo_menus.json`, en la raíz con los demás: aquí solo quedan 55 líneas de código |

### La API (raíz)

| Archivo | Qué hace |
|---|---|
| `main.py` | FastAPI: todos los endpoints, el presupuesto semanal de seguridad crónica y `_garantizar_verificado()`, por donde pasa **todo** menú antes de salir |
| `requerimientos_v2_final.json` | Los requisitos de FEDIAF. **43 filas, y desde el 28 de agosto se verifican las 43**: los 41 nutrientes de la Tabla III-3b (los 12 aminoácidos incluidos), el ratio Ca:P y el calcio de raza grande. Con **una** excepción escrita y probada: el techo de lisina — ver abajo |
| `requisitos.py` | Cargar la tabla de FEDIAF, resolver la etapa y la dosis máxima que marca el fabricante de cada suplemento. Era `optimizador.py`, 1.124 líneas donde esto convivía con el motor anterior al MILP y con una copia desincronizada de la tabla de patologías. El motor viejo se borró el 26 de agosto; quedan 121 líneas |
| `der.py` | Cálculo de las kcal. ⚠️ Ver «la duplicación que hay que vigilar (DER)», abajo |
| `analizador.py` | `/analizar`: la dieta que ya le da el dueño. Comparte `MAPA` con el semáforo a propósito — discreparon una vez por la fibra |
| `especies.py`, `accesibles.py` | Qué especie es cada alimento |
| `transicion.py` | Plan de cambio gradual de dieta |
| `persistencia.py`, `observabilidad.py` | Supabase y Sentry |
| `pruebas_completas.py` | **La batería.** Los 77 bloques, ~25 min. Es lo que se ejecuta entero antes de entregar cualquier cambio (ver «Cómo se prueba») |
| `auditar_patologias.py` | Cada cifra de `patologias.json` contra `requerimientos_v2_final.json`: que ninguna patología formulable tenga un tope por debajo del mínimo de FEDIAF, y que la clave del nutriente exista en el `MAPA`. Lo ejecuta el BLOQUE 32 |
| `radiografia.py` | Imprime los números que **ENTRAN** al motor, para comparar `main` con una rama a golpe de `diff`. No lo ejecuta la batería: se corre a mano. Existe porque el semáforo comprueba el menú contra las kcal que le dieron — si las kcal ya venían mal, el menú sale VERDE para un perro que no es el tuyo, y eso solo se ve en la entrada |
| `auditar_catalogo.py` | Huecos y datos raros del catálogo, y quién se queda sin aminograma. Lo ejecuta el BLOQUE 19 |
| `regenerar_catalogo.py` | Rehace los 36 menús de la vista previa y sus 180 variantes. **Está en el repo por un fallo real**: el 8 de septiembre se regeneró el catálogo con una copia de este script que vivía en un scratchpad y que llamaba al motor **sin `margenes_categoria`** — el motor formula sin proporciones BARF, y salieron menús de **25,8 kg de comida al día con un 91 % de verdura y sin hueso**, los 216 **en verde**, porque lo que se había apagado no era la nutrición sino la FORMA, y la forma no la mira el semáforo. No llegó a `main`. Desde el 9 de septiembre el script vive aquí, hace la misma llamada que la API, y **el BLOQUE 25 comprueba las proporciones de los 216 menús** |
| `auditar_fediaf.py` | Cada valor del JSON contra la tabla de FEDIAF. Lo ejecuta el BLOQUE 18. ⚠️ Su tabla de FEDIAF está **transcrita a mano dentro del propio archivo**, y quien la audita a ella es el de abajo |
| `auditar_transcripcion_fediaf.py` + `fediaf_tabla_III_3b.txt` | **Quién audita al auditor** (10 de septiembre). La cadena era: PDF → transcripción a mano dentro de `auditar_fediaf.py` → `requerimientos_v2_final.json`. El segundo tramo estaba vigilado desde el 25 de agosto y el primero no, que es el que decide todo: con un valor mal transcrito el JSON «cuadra», la batería sale verde y **todos** los menús cumplen bien un requisito equivocado — y el motor no tiene el PDF, así que no puede cazarlo. Ya pasó, y no con un dígito: la transcripción se había saltado **los doce aminoácidos enteros**. El `.txt` es la Tabla III-3b tal cual sale del PDF, sin tocar una palabra, y el script **rehace las 164 celdas**. Las cuatro filas que no se transcriben (selenio seco, biotina, vitamina K y el ratio Ca/P) van declaradas una a una con su motivo, para que saltarse una no pueda volver a ser invisible. Lo ejecuta el BLOQUE 77 |
| `auditar_conversiones.py` | **Que la conversión de cada cifra se rehaga en vez de creerse.** Las 88 cifras de `patologias.json` vienen de tablas publicadas en **% de materia seca** y el motor trabaja **por 1000 kcal**. Esa conversión estaba hecha una vez y **contada en prosa** dentro del campo `por_que`, y una frase no se ejecuta: el 8 de septiembre una se escribió ×25 en vez de ×2,5 —10 veces el valor bueno, con forma de dato bueno— y lo único que la cazó fue que alguien la leyó. Ahora cada cifra lleva un bloque `conversion` con el valor literal de la fuente, su unidad, la densidad de referencia y la cita, y este script **rehace la cuenta**. Una cifra sin ese bloque falla igual: lo que no se puede rehacer no se puede auditar. **Desde el 10 de septiembre también rehace las 12 cifras de `recomendaciones_libro.json`**, que estaban en el mismo estado del que veníamos —la conversión contada en prosa dentro de `por_que`— y que deciden cosas gordas: el techo de calcio del cachorro de raza grande, y el único techo de fósforo que hay en crecimiento. Lo ejecuta el BLOQUE 72 |
| `leer_fuente.py` + `lecturas_fuentes.json` | **Que una lectura no se deje nada.** «Leída» dejó de significar «he pasado los ojos» el 9 de septiembre, después de que la misma cosa fallara **tres veces el mismo día**: se leyó FEDIAF entero y se escaparon dos filas de raza y un escalón de edad; se hizo un inventario de tablas para arreglarlo y se escaparon siete cosas que estaban en el texto; se amplió a secciones y cuatro decían «aplicada» sin estar leídas — y al leerlas salió la más gorda de todas, que el máximo **legal** de FEDIAF solo aplica si el nutriente se **añade como aditivo**. El arreglo no podía ser tener más cuidado. `leer_fuente.py` extrae de cada sección **todas** sus cifras con unidad y **todas** sus frases normativas, y `lecturas_fuentes.json` tiene que dar veredicto a cada una. Las frases importan tanto como las cifras: la regla del máximo legal no lleva ni un número. Lo ejecuta el BLOQUE 68, que además exige que lo que `fediaf_tablas.json` declare «leído» tenga aquí su desglose |
| `auditar_fediaf_tablas.py` | **Que ninguna tabla de FEDIAF se quede sin veredicto.** Recorre el PDF, encuentra cada «Table X-n» y exige que esté en `fediaf_tablas.json` diciendo qué hace el motor con ella. Nació el 9 de septiembre de una pregunta de Elena: cómo podía ser que no usáramos la Tabla VII-6 si se había leído FEDIAF entero. La respuesta estaba en un comentario de `der.py` de tres días antes — la tabla **se leyó**, se confirmó literal, se clasificó bien y se apartó, sin que nadie cruzara su escalón de edad contra el que aplicábamos, que era la mitad. Lo mismo había pasado con las dos filas de raza de la tabla de al lado. El fallo no es de lectura: es que «me lo he leído» no se puede comprobar y un inventario sí. Lo ejecuta el BLOQUE 67 |
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


### Endpoints: cuáles usa la app y cuáles no

Los que llama el frontend hoy: `/menu/v2`, `/menu/semana`,
`/menu/varios-perros`, `/menu/anadir`, `/menu/cambiar`, `/menu/quitar`,
`/menu/revalidar`, `/analizar`, `/alimentos`, `/formular/*`, `/pauta/*`,
`/patologias`, `/relajacion`, y los de Stripe.

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
ve la batería.
`/perro/{perro_id}/menus` **era el único agujero de la regla 1** hasta el 7
de septiembre, y no por descuido: la tabla `menus` guardaba nombre, gramos
y kcal, así que un menú guardado no se podía verificar ni en principio.
Ahora `guardar_menu` escribe el contexto (etapa, DER, pesos, patologías)
junto al menú y el endpoint lo verifica al leerlo — o dice que no puede,
si es una fila anterior a ese cambio. Lo vigila el BLOQUE 47.

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
nadie. Se vigilan por separado contra `der_casos.json` (124 casos, **el
mismo archivo en los dos repos**): BLOQUE 23 aquí, `der-contrato.spec.js`
allí. Si tocas la fórmula de un lado, regenera esperados y copia
`der_casos.json` a los dos repos — los dos commits, o ninguno. Detalle
completo: `HISTORIA_TECNICA.md`.

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

En la raíz, los ocho: `alimentos_v3_final.json` (el catálogo),
`requerimientos_v2_final.json` (la tabla de FEDIAF), `catalogo_menus.json`
(los 36 menús precalculados de la vista previa y sus 180 variantes),
`der_casos.json` (el contrato del DER, ver arriba),
`recomendaciones_libro.json` (los techos del libro para el perro sano),
`requisitos_condicionales.json` (los requisitos que dependen de la propia
dieta), `fediaf_conversiones_vitaminas.json` (la Tabla VII-14: cuántos
microgramos de cada fuente hacen una UI) y `sacn5_fuentes_de_minerales.json` (su
hermana para los minerales, del capítulo 6 de SACN5).

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

## Cómo se prueba

```bash
python3 pruebas_completas.py     # ~25 min, tiene que salir TODO EN VERDE
```

Los 77 bloques tardan unos **25 minutos** (1.458 s en la última medida; el
«~10 min» que ponía aquí se quedó corto en cuanto los bloques 50 a 61
empezaron a resolver menús de verdad, y el «~2 min» de antes llevaba meses
caducado). No necesita red ni claves de verdad: se fabrica
su propio Stripe y su propio Supabase de mentira, así que corre igual en
cualquier máquina y sin conexión.

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
