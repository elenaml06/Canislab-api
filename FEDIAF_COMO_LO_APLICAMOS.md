# FEDIAF, frase a frase: qué hace el motor con cada una, y quién lo vigila

*(15 de septiembre de 2026.)* Nace de una pregunta de Elena, y la pregunta es
justa:

> «¿estás seguro de que estamos aplicando todo tal como lo marca FEDIAF? Porque
> más de una vez has dicho, ay, es que FEDIAF decía esto y lo estamos aplicando
> de esta otra manera. Y en teoría FEDIAF ya estaba cerrado. Entonces, si hoy,
> cuando ya lleva cerrado cinco días, salen cosas, es que ya no me fío de nada.»

**La respuesta honesta es que hay DOS cosas y solo una estaba garantizada.**

| | Qué es | Quién lo garantiza |
|---|---|---|
| **Los NÚMEROS** | las 164 celdas de la Tabla III-3b y los 27 factores de la VII-14 | `auditar_transcripcion_fediaf.py`, que los **rehace desde el texto del PDF** en cada batería (BLOQUE 77). No se han copiado a mano sin comprobar ni una vez |
| **LA LETRA DE AL LADO** | en qué unidad va cada número, a quién se le aplica, y las notas al pie | **hasta hoy, nadie.** Se leyó a mano y se anotó en `LECTURAS.md` — y *leído* no es *comprobado* |

**Todo lo que ha aparecido estos días sale de la segunda fila**, no de la
primera. El caso del lunes lo enseña entero: los siete máximos legales estaban
**bien transcritos**; lo que fallaba era la frase de al lado, §3.2.1, que dice
que esos siete *«are only provided on a dry matter basis»*.

⚠️ **Y una cosa que hay que decir porque cambia el diagnóstico: eso NO era un
descubrimiento del lunes.** Estaba escrito en `LECTURAS.md` desde el **11 de
septiembre**, con su cita y su medida, como *pendiente de decidir* (la **P-38**).
Lo que pasó el lunes no fue que apareciera un fallo nuevo: fue que **se aplicó
una decisión que llevaba cuatro días escrita y esperando**. Son dos cosas muy
distintas y conviene no confundirlas.

**Qué significa «cerrado» aquí, que es donde estaba la trampa.** Nunca quiso
decir «aplicado entero». Los contadores que decían «0 pendientes» contaban
**frases con nota**, no decisiones — está escrito en `CLAUDE.md` y fue una frase
de Elena la que los mandó fuera. FEDIAF está **leída entera**, de la primera
línea a la última, con **71 frases con veredicto** en la sección de `LECTURAS.md`.
De esas, **15 siguen abiertas**, y están todas abajo con dueño.

---

## 1 · Lo que el motor aplica, y quién lo vigila

Solo las frases que **deciden un número**. Las de contexto, las que son
obligaciones de un fabricante y las que no tienen cifra están en `LECTURAS.md`
con su veredicto.

| § de FEDIAF | Lo que dice | Qué hace el motor | Quién lo vigila |
|---|---|---|---|
| §1 · glosario | los niveles deben estar **al o por encima** del mínimo y **no pasar** del máximo nutricional ni del legal | es el semáforo, en las dos direcciones | BLOQUE 8, BLOQUE 18 |
| §3.1.3 | el máximo **legal** es obligatorio y se reporta **solo en base materia seca** | los siete (Cu, Fe, I, Mn, Se, Zn, vit. D) entran en el solver y en el semáforo como restricción lineal sobre la materia seca del propio menú | **BLOQUE 113** |
| §3.2.1 | los **mínimos** van por 1000 kcal, anclados a 95 o 110 kcal/kg^0,75 | el motor usa **esos** números, sin convertir nada | **BLOQUE 113** (la mitad que casi se cambia por error) |
| §3.2.1 | *«If the protein digestibility of ≥ 80% cannot be guaranteed, it is recommended to increase the essential amino acid levels by a minimum of 10%»* | aplicado: `aminoacidos_si_no_se_garantiza_la_digestibilidad` | BLOQUE 60, BLOQUE 72 |
| §3.2.2 · nota a | mínimo de calcio reforzado en crecimiento | aplicado | BLOQUE 18, BLOQUE 62 |
| §3.2.2 · nota b | el cachorro que pasará de **15 kg**: calcio 2500 y techo del ratio Ca:P 1,6 | aplicado, y con su umbral propio (`RAZA_GRANDE_O_GIGANTE_KG`), que **no** es el de 25 kg de SACN5 | BLOQUE 57, BLOQUE 62 |
| §3.3.1 · proteína en reproducción | *«If carbohydrate is absent or at a very low level, the protein requirement is much higher, and may be double»* | aplicado: 125 g/1000 kcal en gestación y lactancia | BLOQUE 58, BLOQUE 60 |
| §3.3.1 · arginina | *«For every gram of crude protein above the stated values, an additional 0.01 g of arginine is required»* | aplicado, y la cuenta rehecha contra el Anexo 7.4 | BLOQUE 60 |
| §3.3.1 · lisina | techo de 7,00 g/1000 kcal en crecimiento | **NO se aplica**, y es la **única** excepción escrita: 0 de 12 menús de cachorro caben debajo | BLOQUE 27 |
| §3.3.1 · grasa | *«Fat per se is not essential»* | por eso la grasa **no escala** en `minimo_de()` | BLOQUE 34 |
| §3.3.1 · fósforo adulto | máximo nutricional 4,00 g/1000 kcal | aplicado | BLOQUE 18, BLOQUE 57 |
| §3.3.1 · cobre y hierro | el óxido de cobre y el óxido/carbonato de hierro **no cuentan** como fuente | aplicado | BLOQUE 70 |
| §4.1 | *«The total daily ration should match the recommended allowances and nutritional and legal maximum values»* | los premios **no** eximen: la ración se formula con las kcal que quedan y se le exige el día entero | BLOQUE 88, BLOQUE 95 |
| §7.1 · Tabla VII-2 | el % de desviación del peso ideal por cada punto de BCS | aplicado: `peso_objetivo_desde_bcs()` | BLOQUE 96 |
| §7.1 · Tabla VII-1 | cómo se RECONOCE cada punto de BCS | servido al dueño y al veterinario, con la frase literal | BLOQUE 99 |
| §7.2.2.2 b) | la ecuación de ME para ingredientes **frescos o crudos** | comprobada, y coincide con la del motor | BLOQUE 23 |
| §7.2 · Tabla VII-7 | DER por nivel de actividad, con el Gran Danés y el Terranova por su nombre | aplicada, con el hueco de «Obese prone adults ≤ 90» declarado | BLOQUE 88 |
| §7.2 · Tabla VII-8a | las cinco ecuaciones de la curva de crecimiento | aplicadas, incluido el emparejamiento banda↔ecuación que el PDF a dos columnas cruza | BLOQUE 96 |
| §7.2 · Tabla VII-8b | gestación y lactancia | aplicadas, en los dos repos | BLOQUE 23 |
| §7.2.5 | `Units/1000 kcal = requisito por kg PM × 1000 / DER por kg PM` | aplicado, y **solo hacia arriba**: no hay base para bajar el mínimo de un perro que come más | BLOQUE 34 |
| §7.4 · Tabla VII-13 | arginina por contenido de proteína | aplicada | BLOQUE 60 |
| §7.5 · Tabla VII-14 | factores de conversión de cada forma química de vitamina | aplicada **y rehecha desde el PDF** | BLOQUE 70, BLOQUE 77 |
| §7.7 | tóxicos con sus dosis | el motor **prohíbe el alimento entero**, que es más estricto que la dosis | BLOQUE 51 |
| Anexo 7.8 · VII-17a-d | la **segunda copia** que FEDIAF publica de la misma tabla | cruzadas las 186 celdas: 186 coinciden, 17 difieren solo en unidad y **1** de verdad (el EPA+DHA de adulto), documentada | BLOQUE 18 |

---

## 2 · Lo que sigue ABIERTO, con dueño

Ninguna de estas cambia hoy una cifra del motor sin que alguien lo decida. Están
todas en `LECTURAS.md` con su cita literal.

| § | La frase | Qué falta | Dueño |
|---|---|---|---|
| §2.2 | *«ingredients with normal digestibility (i.e. ≥ 70% DM digestibility; ≥ 80% protein digestibility)»* | es la **condición de validez de toda la tabla** y el catálogo no tiene campo de digestibilidad | Cris (P-16) |
| §2.2 | FEDIAF **se excluye a sí misma** de los alimentos para fines nutricionales particulares | «gana FEDIAF» es verdad para el perro SANO; para el enfermo quien pone el suelo es la ley | Cris |
| §3.1.3 | el máximo legal **solo aplica si el nutriente se AÑADE como aditivo** | el motor lo aplica **siempre** —el lado estricto— porque seis de los siete **no tienen máximo nutricional publicado** y la lectura literal los dejaría sin ningún techo. ⚠️ Desde el 15 de septiembre eso **cuesta**: dos variantes del catálogo y el suelo de vitamina E de la renal | Cris + Elena |
| §3.2.1 | *«the recommendations should be corrected for energy density»* | los otros **122** límites en % de materia seca, los que **no** son de FEDIAF | **P-38** |
| §3.3.1 | *«If formulating below the recommended minimum for total protein … ensure that the amino acid profile meets FEDIAF guidelines»* | el motor ya verifica los 12 aminoácidos, o sea que la condición se cumple por construcción; falta **decirlo** | Cris |
| §3.3.1 | *«Methionine In the case of lamb and rice foods, the methionine level may have to be increased»* | hay cordero en el catálogo y la fuente **no da cifra** | Cris |
| §3.3.1 | el ratio **omega-6:omega-3**: FEDIAF dice que importa y en qué dirección está el daño, y **no da número** | cuarta fuente que lo pide sin cifra | Cris (P-40) |
| §3.3.1 | *«As the calcium level approaches the stated nutritional maximum, it may be necessary to increase the levels of certain trace elements»* | el motor no sube zinc ni cobre con el calcio alto | Cris |
| §3.3.1 | yodo: FEDIAF **descarta** el máximo bajo de Castillo | conflicto confirmado con nuestro tope crónico de 1275 µg | Cris |
| §7.1.3 | *«The ideal BCS should therefore be between 4/9 and 5/9»* | el motor toma `BCS_NEUTRO = 5`, así que a un perro en BCS 4 —que **ya está en su banda ideal**— le da un 8 % más de comida | Elena + Cris |
| §7.1 | Tabla VII-3, escala de masa muscular de 4 puntos | no se ofrece en ninguna pantalla | Elena |
| §7.2 | fuera de la zona termoneutra la MER sube **2-5 kcal/kg^0,75 por grado** | la ficha no pregunta dónde vive el perro | Elena |
| §7.3 | taurina: *«low plasma levels of taurine (< 40 µmol/L) may also predispose to dilated cardiomyopathy»*, con el cordero y el Terranova nombrados | hay cordero en el catálogo y el Terranova en `razas.json` | Cris |
| Tabla VII-6 | MER por edad, >7 años 95 kcal/kg^0,75 | conflicto ya anotado con la edad del sénior | Cris |
| §7.2 · VII-8a | la curva de crecimiento **solo está en el motor** | el frontend no la tiene y cae a los dos escalones de SACN5 | **P-14** |

---

## 3 · Lo que este documento NO garantiza, y hay que decirlo

Una tabla que dice «vigilado por el BLOQUE n» **no comprueba que ese bloque
compruebe lo que dice**. Lo que el **BLOQUE 116** sí exige, y es lo que se puede
exigir mecánicamente:

1. que **cada bloque que se nombra aquí exista** de verdad en la batería — una
   referencia a un bloque que no está es la misma referencia rota que tuvieron
   los dos BLOQUES 98;
2. que **cada frase citada entre comillas sea literal**, contra el texto del PDF
   (`auditar_citas.py`, BLOQUE 85);
3. que el recuento de abiertas de aquí **sea el mismo** que el de `LECTURAS.md`.

Lo que **no** se puede comprobar con un script es que el veredicto sea el
correcto. Para eso está la lectura, y por eso la lectura se deja escrita con la
cita al lado: para que otra persona pueda discrepar de ella.
