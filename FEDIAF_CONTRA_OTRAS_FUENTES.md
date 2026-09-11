# Dónde las fuentes no dicen lo mismo, y qué aplica el motor

**Escrito el 11 de septiembre de 2026**, a petición de Elena, para que vaya en el
documento que lee el nutricionista.

## La regla, en una línea

**Si otra fuente contradice a FEDIAF, gana FEDIAF.** Pero la discrepancia se
apunta, con las dos cifras y con la que aplicamos, porque quien firma una pauta
tiene derecho a saber que existe.

## Y una distinción que hace falta antes de leer la lista

«Contradecir a FEDIAF» **no** es lo mismo que «pedir otra cosa que FEDIAF». Casi
todas las cifras de este motor que no son de FEDIAF **caben dentro** de FEDIAF:
aprietan el mínimo hacia arriba o el máximo hacia abajo, sin salirse de la
ventana. Eso no es un conflicto y se aplica sin más — es lo que hacen los topes
de patología, los del libro y los condicionales, todos con `min()` y `max()`, que
solo pueden apretar.

Hay conflicto **solo** cuando la otra fuente sacaría al perro **fuera** de la
ventana de FEDIAF. Ahí es donde manda FEDIAF, y de eso va la primera tabla.

---

## 1 · Conflictos de verdad: la otra fuente se sale de FEDIAF y NO se aplica

| Nutriente | Dice FEDIAF | Dice la otra fuente | Qué aplica el motor |
|---|---|---|---|
| **Selenio** | máximo **142 µg/1000 kcal** (Tabla III-3b) | SACN5 caps. 13, 14 y 47 recomiendan **0,5-1,3 mg/kg MS = 125-325 µg/1000 kcal** | **El máximo de FEDIAF, 142.** El 56 % superior del rango del libro queda fuera |
| **Ratio Ca:P del cachorro de raza grande** | techo **1,6** (nota b de la Tabla III-3b) | SACN5 da **1,5** en una de sus tablas de crecimiento | **El 1,6 de FEDIAF.** Detalle y la contradicción interna del propio libro: `HALLAZGOS_SACN5_10SEP.md` §S-5 |
| **Energía del cachorro** | curva de Klein (Tabla VII-7) | SACN5 Tabla 33-8, tomada de NRC 2006, llega hasta un **28 % por encima** | **La de FEDIAF.** Es la más conservadora: dar de más a un cachorro de raza grande es exactamente lo que causa enfermedad ortopédica del desarrollo |
| **Edad a la que un perro es sénior** | escalón de la Tabla VII-6, **7 años** para todos | NRC 2006 cap.4: *«Generally, giant- and large-breed animals are considered geriatric at 5 years of age, whereas medium- or small-breed dogs and all cats are not considered geriatric until 7 or more years of age»* | **Los 7 años de FEDIAF.** Y hay un matiz: NRC ahí está **definiendo una palabra**, no publicando un requisito, mientras que el escalón que el motor aplica es una tabla de energía |
| **Yodo** | máximo **2750 µg/1000 kcal** | SACN5 le atribuye al NRC un límite que **el propio NRC dice que no se puede fijar** | **El tope crónico del motor, 1275 µg/1000 kcal**, que es más estricto que los dos. Detalle: `HALLAZGOS_SACN5_10SEP.md` §S-7 |
| **Calcio del cachorro de raza grande** | mínimo **2500** mg/1000 kcal (fila `Calcio_LateGrowth_RazaGrande`, nota b) | Fascetti cap. 10, escrito por Hazewinkel, que es quien hizo los experimentos: **0,8-1,0 % de materia seca por 4200 kcal/kg = 1905-2381 mg/1000 kcal**, y su recomendación final es ~1,0 % | **El techo de 2750 que ya aplica el motor** (1,1 % MS, del mismo capítulo). El rango que recomienda su autor queda **entero por debajo del mínimo de FEDIAF**, así que aplicarlo dejaría al cachorro corto de calcio. Detalle y las cuatro cifras: `HALLAZGOS_FASCETTI.md` §F-7 |
| **Grasa en linfangiectasia** | mínimo **13,75** g/1000 kcal, sin máximo | El mismo «15 %» en **dos unidades**: SACN5 Tabla 58-1 lo da en **materia seca** (= 37,5 g/1000 kcal) y Fascetti cap. 11 en **kcal** (= 16,7). Un factor de 2,2 | **Los 37,5 de SACN5.** Medido con el solver y 40 s en perros de 10, 20 y 35 kg: con 16,7 y con 20,0 **no sale menú en ninguno**. Lo que hay que decidir antes que el número es **qué unidad lleva el 15 %**. Detalle: `HALLAZGOS_FASCETTI.md` §F-9 |
| **Proteína en hepatopatía** | mínimo **52,1** g/1000 kcal en adulto | Fascetti cap. 13: las dietas hepáticas del mercado llevan **14-15,5 % de las kcal en proteína = 35-38,75 g/1000 kcal** | **El mínimo de FEDIAF.** Formular por debajo del mínimo es la fase 4 de `VETERINARIOS.md` y exige una prescripción declarada que viaje con el menú; todavía no existe |

### Y un caso al revés: FEDIAF dice algo que no cabe

| Nutriente | Dice FEDIAF | Qué pasa | Qué aplica el motor |
|---|---|---|---|
| **Techo de lisina en crecimiento** | **7,00 g/1000 kcal** | **0 de 12 menús de cachorro caben debajo** (van de 8,24 a 11,48, mediana 9,03). La lisina va detrás de la proteína, y una ración BARF de cachorro lleva ~134 g/1000 kcal contra un mínimo de 50 | **No se aplica**, y es la **única** excepción escrita de todo el motor. Vive en `verificar.MAXIMOS_NO_APLICADOS`, con la pregunta abierta. El **mínimo** de lisina sí se aplica |

---

## 2 · Lo que otra fuente aprieta DENTRO de FEDIAF, y sí se aplica

Esto no es conflicto. Son cifras de un libro o de una guía clínica que caen
dentro de la ventana de FEDIAF y la estrechan.

| Nutriente | Ventana de FEDIAF | Lo que aprieta | De dónde sale |
|---|---|---|---|
| **Fósforo, adulto sano** | 1160 a **4000** mg/1000 kcal | techo **2000** | SACN5 Tablas 13-3 y 47-4. El libro recomienda **la mitad** del máximo de FEDIAF, y una ración BARF salía pegada a ese máximo |
| **Fósforo, sénior sano** | igual | techo **1750** | SACN5 Tabla 14-2 |
| **Sodio, adulto y sénior** | 290 a 3750 | techo **1000** | SACN5 Tablas 13-3, 14-2 y 47-4 |
| **Calcio y fósforo del cachorro** | calcio 2000-4500; el fósforo **en crecimiento** no tiene máximo en FEDIAF (en adulto sí: 4,00 g/1000 kcal) | 4250/3250 (adulto <25 kg) y **2750/2750** (>25 kg) | SACN5 Tabla 17-1 (dos columnas) y Fascetti cap.10. El techo de fósforo **de crecimiento** es el único que tiene un cachorro: las dos celdas de máximo de esa fila de FEDIAF están vacías |
| **Vitamina E, adulto y sénior sanos** | mínimo 6,968 mg, **sin máximo** | suelo **67,1 mg/1000 kcal** — ⚠️ **escrito y HOY APAGADO** | SACN5 Tablas 13-3 y 14-2, ≥400 UI/kg MS, dicho en **cinco capítulos**. Se encendió y se apagó el mismo 11 de septiembre: encendido deja sin menú a los tres perros con ocho especies fuera y pone roja la batería. La cifra **no se ha bajado**; está escrita con su medida y se pregunta. Ver la regla 2 de `CLAUDE.md` |
| **Vitamina D, yodo, selenio, mercurio, tiaminasa** | los máximos de la Tabla III-3b | los cinco topes crónicos de `seguridad.py`, todos más estrictos | NRC 2006 y la literatura citada en cada línea del fichero |
| **Los 75 límites de patología** | la ventana de FEDIAF de cada nutriente | siempre dentro | `patologias.json`, cifra a cifra con su fuente. `auditar_patologias.py` comprueba que **ninguna** patología formulable tenga un tope por debajo del mínimo de FEDIAF |
| **Proteína de gestación y lactancia** | el mínimo de la Tabla III-3b | sube, porque FEDIAF lo calcula suponiendo hidratos que una ración BARF no lleva | NRC 2006 (Kienzle 1985): con la dieta sin hidratos y la proteína baja, la mortalidad perinatal subió un **75 %** |
| **Arginina** | Tabla III-3b | sube con la proteína, por la **propia** Tabla VII-13 de FEDIAF | Es FEDIAF contra FEDIAF, y se aplica la más estricta de las dos |

---

## 3 · Donde FEDIAF no dice nada, y por eso manda la otra fuente

| Tema | FEDIAF | Lo que hay |
|---|---|---|
| **Fibra** | no da ni mínimo ni máximo para perros | ocho patologías con suelo o techo, todas de tablas de SACN5. ⚠️ **Y están en una unidad distinta de la del catálogo** — ver `PENDIENTE_NUTRICION.md`, apartado de la fibra |
| **Taurina y L-carnitina** | no son requisito para el perro (sí la taurina para el gato) | suelos reales en `dcm_taurina_respondedora`, de SACN5 Tabla 36-4 |
| **Vitamina K** | no la publica para el perro | el NRC sí, y el catálogo **no la tiene en ninguna ficha**. Pendiente de dato, no de código |
| **Ratio linoleico:linolénico** | lo enuncia y no lo cuantifica | 2,6-26 en adulto y crecimiento, de NRC 2006 cap.5, **aplicado**. NRC dice además que el ratio omega-6:omega-3 totales *«is not helpful»* |
| **Máximo de vitamina E** | ninguno en ninguna etapa | SACN5 cap.13 recoge que *«An upper limit of 1,000 to 2,000 IU/kg food (DM) has been suggested for dogs»* (AAFCO 1985, NRC 1985). **Escrito y no aplicado**: es un rango sugerido, no un máximo, y los menús con el suelo nuevo salen en 68-79 mg/1000 kcal, muy por debajo del extremo bajo (167,75 mg) |
| **Energía del hueso carnoso** | no se pronuncia | NRC excluye el hueso de los factores de Atwater, que es lo que usa el catálogo. Medido: el error está acotado en un dígito por ciento y no hay cifra que aplicar. `PENDIENTE_NUTRICION.md` |

---

## 4 · Lo que esta lista NO es

**No es todo lo que dicen las fuentes.** Es donde hay **desacuerdo** o donde
FEDIAF calla. Lo que las fuentes confirman sin discrepar —que es la mayor
parte— está en `LECTURA_SACN5_INTEGRA.md`, `LECTURA_NRC2006.md` y
`HALLAZGOS_SACN5_10SEP.md`, capítulo a capítulo.

**No decide nada de clínica.** Cada fila dice qué aplica el motor hoy y por qué.
Las que están abiertas viven en `PREGUNTAS_ABIERTAS.md` con su estado.
