# Rawku — lo que queda por hacer (índice)

Lista viva. Se actualiza al terminar cada cosa, no al final.
Última revisión: 11 de septiembre de 2026.

**Desde el 6 de septiembre esto es solo el índice.** Cada punto vive en uno
de cuatro archivos, por tema — ábrelos según lo que toque la tarea, no
todos de golpe: `PENDIENTE_DECISIONES.md`, `PENDIENTE_DINERO_Y_SALUD.md`,
`PENDIENTE_PRODUCTO.md`, `PENDIENTE_NUTRICION.md`. Lo ya resuelto está en
`HECHO.md`; la investigación o el código detrás de un pendiente que no hace
falta releer cada vez, en `PENDIENTE_DETALLE.md`.

**Hay un repositorio nuevo, `elenaml06/canislab-fuentes`**, con las fuentes
nutricionales (FEDIAF, NRC, y todo lo que Cowork ha escrito a partir de
libros con copyright que no se guardan en ningún repo). Empieza por su
`ESTADO_Y_PROXIMOS_PASOS.md` si esta sesión toca nutrición, patologías o
el catálogo.

El orden **no** es por lo que parece más urgente, sino por lo que
desbloquea al resto y por lo que cuesta más caro si sale mal. Cobrar dos
veces a alguien duele más que no tener login con Google.

---

## `PENDIENTE_DECISIONES.md` — decisiones tuyas, no son trabajo de programación

Bloquean cosas de abajo. Ninguna lleva más de unos minutos, pero las tiene
que tomar una persona, no yo.

- [ ] ⚠️ **Cuatro decisiones de la app contra el motor** (10 sep, `FRONTEND_VS_MOTOR.md`): si se pregunta el estadio ACVIM al marcar «Cardiopatía» y a quién —hoy un perro en estadio C recibe el tope del B2—, si `urolitos_fosfato_calcico` entra en la lista del dueño, si se parte la casilla conflacionada de cálculos en cuatro, y si se ofrece `raza_predispuesta_cobre`
- [ ] ⚠️ **Cinco cifras caninas de SACN5 que el motor no aplica** (10 sep, `HALLAZGOS_SACN5_10SEP.md`), las cuatro medidas en vivo: la **vitamina E** del perro sano (SACN5 pide 67,1 mg/1000 kcal en cinco capítulos y los menús dan 13-20, **0 de 10 llegan**); la **vitamina C** ≥25 mg/1000 kcal, que pediría un dato nuevo en 163 fichas; el **selenio** 125-325, cuyo extremo alto **se pasa del máximo de FEDIAF**; la **grasa del cachorro de raza grande**, que SACN5 recomienda en 8,5-17 % MS y una ración cruda da 23-29 % (**0 de 6 caben**); y la **energía del cachorro**, donde la Tabla 33-8 (NRC 2006) va hasta un **28 % por encima** de la curva de Klein que publica FEDIAF y que aplicamos —no es un fallo, manda FEDIAF, pero son dos fuentes publicadas que difieren en un animal en crecimiento—
- [ ] 🔴 **RELEER TODA CITA ANTERIOR AL 10 DE SEPTIEMBRE** (`HALLAZGOS_LECTURA_FUENTES.md`, último apartado). El texto de FEDIAF y de SACN5 se había extraído pegando las **dos columnas** de cada página: el **49,3 %** de las líneas de FEDIAF y el **37,5 %** de las de SACN5. Ya está rehecho y el BLOQUE 81 lo vigila, pero **toda cita entrecomillada sacada de esos ficheros puede decir algo que la fuente no dice**. Toca `PARA_EL_NUTRICIONISTA.md`, `PATOLOGIAS.md`, `LECTURA_SACN5.md` y los campos `fuente`/`por_que` de `patologias.json`
- [x] ~~FEDIAF, leído entero y bien~~ — HECHO 10 sep. El **100 %** de las 10.683 líneas desglosado y **532 de 532** cifras y frases con veredicto. Salieron ocho cosas: `HALLAZGOS_LECTURA_FUENTES.md` F-15 a F-22
- [ ] **SACN5, el texto: 3.140 elementos nutricionales sin veredicto.** Lo clava el BLOQUE 81, exacto: solo baja cuando alguien lee y lo baja en el mismo commit
- [ ] ⚠️ **En GitHub Actions no están las fuentes, y cinco controles no se ejecutan allí.** `canislab-fuentes` es otro repositorio y el workflow no lo clona, así que los BLOQUES 18-bis, 67, 68, 77, 78 y 81 dicen «no está el texto» y **no comprueban nada**. Hasta el 10 de septiembre eso salía en verde sin decirlo; ahora al menos lo dice. Arreglarlo es un `actions/checkout` extra del repo de fuentes con un token — **decisión de Elena**, porque toca dar acceso a un repositorio privado desde la CI. Bastaría con los `.txt` (unos 5 MB); los PDF de SACN5 son 293 MB y no hacen falta
- [ ] ⚠️ **La HUMEDAD de cada ficha, y ahora se sabe para qué** (`HALLAZGOS_LECTURA_FUENTES.md` F-16). FEDIAF dice literal que la conversión desde %MS **asume 4,0 kcal/g de materia seca** y que «should be corrected for energy density» si es otra — y que los máximos **legales** ni siquiera dependen de la energía. Es el puente que usan las 92 cifras de patología, las 12 del libro y todas las de SACN5, y **sin la humedad no se puede ni medir cuánto nos desviamos**
- [ ] ⚠️ **Ocho preguntas que la ficha no hace y sin las cuales el tope de una patología se elige mal** (10 sep, `PENDIENTE_PRODUCTO.md`): derivadas de la fuente de cada patología, no opinadas. De las **24 que solo puede marcar un veterinario**, la app le ofrece **once al dueño con menú automático** sin preguntarle el dato — la pancreatitis sin los triglicéridos recibe 37,5 g de grasa donde su fuente pide 25, y sale **en verde**
- [x] ~~Estipular qué puede variar un veterinario y hasta qué techo~~ — RESUELTO 10 sep. Las **79 cifras** de patología llevan su ventana (`margen_profesional`) con la procedencia de cada extremo, `GET /patologias` la sirve y el BLOQUE 80 la rehace. ⚠️ Y sale una pregunta nueva, porque el Reglamento (UE) 2020/354 **no da rango por nutriente**: dentro de esa ventana, ¿el veterinario mueve libremente, o hay cifras que no debería tocar aunque quepan? Eso no lo contesta ninguna fuente y va a `PREGUNTAS_ABIERTAS.md`
- [ ] Ejecutar el SQL de la fase 0 en Supabase (rol profesional)
- [ ] La lista de las nueve `formulable: false` (la necesita la fase 4)
- [ ] ⚠️ **Un perro en BCS 4 recibe hoy un 8 % más de comida, y FEDIAF §7.1.3 dice que «the ideal BCS should therefore be between 4/9 and 5/9»** — o sea que ya está en su peso. Encontrado con `radiografia.py` el 10 sep, con la tabla de efecto por BCS medida. Es tensión DENTRO de FEDIAF (§7.1.1 no distingue dirección, §7.1.3 da el rango) y toca a todo perro marcado «delgado»
- [ ] Tres cambios de producto sobre la estimación por BCS por debajo de 5
- [ ] Cuatro fichas de aminoácidos que hay que mirar en su fuente
- [ ] El máximo de lisina de FEDIAF: ¿sobre qué proteína se mide? (para el nutricionista)
- [ ] Límites por patología: confirmar los números (fósforo, cobre, grasa)
- [ ] Siete preguntas para Cris (proteína senior, estadio ACVIM, pancreatitis en cachorro, umbral 1,10, tiaminasa, qué firma un veterinario, qué hace AnVet)
- [x] La app no distingue hepatopatía por cobre de otras hepatopatías — RESUELTO 7 sep (`raza_predispuesta_cobre`)
- [x] Repasar la transcripción de la tabla de FEDIAF en `auditar_fediaf.py` — HECHO 10 sep, y **mecánico, no a ojo**: `fediaf_tabla_III_3b.txt` es la tabla tal cual sale del PDF y `auditar_transcripcion_fediaf.py` rehace sus **164 celdas** contra la transcripción a mano. Las 164 cuadran. Las cuatro filas que no se transcriben van declaradas con su motivo. BLOQUE 77, probado con el fallo puesto (un valor, una unidad, una fila borrada y el propio texto de la fuente editado)
- [ ] **Tres decisiones que dejó leer SACN5 entera** (10 sep): si se pregunta dónde duerme el perro (la Tabla 5-3 da las cifras del frío, pelo corto +95 %), con qué densidad se leen las cifras de obesidad (la 27-4 es la única que propone ≤3,4 kcal/g), y si la energía del cachorro pasa a ir por fracción de peso adulto (Tabla 17-2, tres escalones) en vez de por edad
- [x] Auditar los valores de los ALIMENTOS — RESUELTO 7 sep: la auditoría ya existía (`auditar_catalogo.py`), se ejecutó de verdad y se investigaron sus 20 avisos. Ver `PENDIENTE_DECISIONES.md`
- [x] Fibra de la borraja — CERRADO 7 sep: el alimento ya no existe en el catálogo, no es un hueco de dato
- [ ] `renal + pancreatitis` no da menú en ningún tamaño — decisión de nutrición: qué tope cede, y qué se le dice mientras (BLOQUE 50)
- [x] El fósforo del perro sano — APLICADO 8 sep: 2000 en adulto, 1750 en senior, medido y en el peldaño 0 (`DECISIONES.md` D-15)
- [~] Al toy de 1,5 kg le cuesta sacar menú con el techo de fósforo — **al dueño ya no le pasa** (0 sin menú de 20 por la vía de la API, con 24 s y con 3 s; lo arregló el reparto de tiempo del 8 sep) — ⚠️ **la causa escrita era falsa y está corregida el 10 sep**: no hay ningún «sorteo de alimentos» (de `modos.py` el motor solo usa un diccionario; el MILP ve todos los candidatos), y el ruido va en el OBJETIVO, que no puede volver infactible nada. Es el `time_limit`: 11 de 30 sin menú a 1 s, 6 a 5 s, **0 a 30 s**. Lo que queda es el coste de tiempo, no un menú perdido (`PENDIENTE_NUTRICION.md` §14.4)
- [ ] El techo de Ca:P del cachorro de raza grande: SACN5 Tabla 17-1 dice 1,5 y aplicamos el 1,6 de FEDIAF. Hoy no cambiaría ni un menú (los reales van de 1,03 a 1,29), y el propio libro se contradice — la 33-5 dice 2,0. Necesita mecanismo de ratio en `recomendaciones_libro.json` — el de PATOLOGÍA ya existe desde el 10 sep (bloque `ratios`, BLOQUE 75), así que lo que falta es el mismo en el fichero del libro (`PENDIENTE_NUTRICION.md`, último punto)
- [ ] En crecimiento, ¿los suelos de una patología también se caen con el tope?
- [ ] La proteína de la reacción adversa: la fuente la limita solo en casos dermatológicos y la ficha no lo pregunta
- [ ] ¿Rawku apunta a algún rango de fibra? — decisión de nutrición, no de código (nota: hiperlipidemia ya tiene suelo real, 7 sep — ver `PENDIENTE_NUTRICION.md` §10)
- [ ] ¿Hace falta estar dada de alta como autónoma para cobrar? (pregunta a la gestoría)
- [ ] Revisar los textos legales cuando estén redactados — bloquea Stripe y Google

## `PENDIENTE_DINERO_Y_SALUD.md` — lo urgente, antes de cobrar, lo que mira Stripe

- [x] `/menu/varios-perros` devolvía 1 menú en vez de 3 — ARREGLADO 7 sep: decidía si seguir con el TOPE de cada rodaja (peor caso 10 s) en vez de con lo que había costado de verdad la ronda anterior. Ahora se mide. Con el presupuesto apretado a 14 s: antes [2,1,1,1,2], ahora [3,3,2,3,3]. BLOQUE 48
- [x] Los 0,99 g de salmón — CERRADO 7 sep: el suelo de «esto se puede pesar» se recortaba contra el techo del propio alimento (`min(porcion, techos[i])`) y podía quedarse por debajo del gramo. Ahora nunca baja de 1 g y el MILP deja fuera solo al alimento del que no cabe ni un gramo
- [ ] Nadie debería poder suscribirse dos veces
- [x] El yodo de los perros pequeños — ARREGLADO 7 sep, y era peor de lo apuntado: el margen del suelo era un 1,5 % fijo cuando lo que tiene que cubrir es el error ABSOLUTO del redondeo. Medido en 60 menús de perros de 1,5-4,5 kg: antes el yodo bajaba al 82 % y 3 menús se caían; ahora mínimo 100 % y ninguno. BLOQUE 49
- [ ] `profiles` es una frontera de autorización y no está en el repo (RLS sin versionar)
- [ ] Comprobar que la cancelación quita el premium
- [ ] Verificar el negocio en Stripe, crear productos/precios/webhook reales, quitar `STRIPE_PRUEBA`, primer cobro real
- [ ] Páginas legales que no existen (privacidad, condiciones, reembolso)

## `PENDIENTE_PRODUCTO.md` — funcionalidades nuevas y deuda técnica

- [ ] 🔴 **El aviso del estreñimiento crónico cuenta media verdad** (11 sep, cap.64): dice que la comida cruda juega a favor por el agua —cierto— y no nombra el hueso. El capítulo dice DOS VECES que las dietas de hueso y carne cruda causan estreñimiento y obstipación «due to the large contribution bones make to such foods», y la regla de forma del motor pide 20-60 % de hueso. Es el aviso que recibe justo el perro que consulta por eso
- [ ] **El hueso, cuarto daño documentado** (11 sep, cap.50): **46 de 60 cuerpos extraños esofágicos** retirados a perros eran hueso. Se suma a las fracturas dentales, los patógenos y la diarrea aguda
- [ ] **El páncreas CRUDO es tratamiento de la EPI y no está en el catálogo** (11 sep, cap.66): la fuente lo recomienda con dosis (30-90 g) y es de las poquísimas cosas del libro que SOLO puede hacer una dieta cruda. Ninguna de las 163 fichas es páncreas. Son dos decisiones: si entra la ficha, y si el aviso lo nombra aunque no entre
- [x] **Los tres ficheros de cifras, con su conversión rehecha** — HECHO 10 sep. Los doce techos del libro y los cuatro requisitos condicionales (donde están **las dos conversiones a la vez**: la vitamina E del perro de trabajo, «≥500 IU/kg MS» a mg de tocoferol natural, que es el fallo del 8 sep exacto). En cada batería se rehacen 92 + 12 + 4. Detalle: `recomendaciones_libro.json` tenía la cuenta contada en prosa dentro de `por_que`, igual que tenían las 88 de patología antes del ×25. Ahora `auditar_conversiones.py` las rehace (12 de 12 exactas) y el BLOQUE 72 las mira. Deciden el techo de calcio del cachorro de raza grande y el **único** techo de fósforo que hay en crecimiento
- [x] **El perro pequeño con patología ya no se queda sin menú por el reloj** — HECHO 10 sep: la API reintentaba hasta dos veces cada peldaño que HiGHS ya había demostrado imposible (status 2), y reintentar eso no puede cambiar nada porque el ruido del motor va en el OBJETIVO. Chihuahua de 3 kg con renal: **23,6 s y 16 llamadas → 9,3 s y 6**, mismo menú y mismo peldaño; y dos cruces del BLOQUE 50 pasan a dar menú. BLOQUE 76 y `HECHO.md`
- [ ] **¿Se borra lo muerto de `motor/modos.py`?** Son 190 líneas de las que el motor usa **un diccionario** (`CUANTOS_MAX`): `elegir_alimentos`, `cambiar`, `quitar` y `anadir` no los llama nadie. No es urgente, pero código muerto que parece vivo ya costó un diagnóstico equivocado el 10 sep (`HECHO.md`)
- [x] **El ratio que pide una patología** — HECHO 10 sep: el Ca:P de 1,1-2,0 de las Tablas 40-5 y 41-6 llevaba dos días escrito con `aplicado_por_el_solver: false`, y **no era cosmético**: el perro de 30 kg con oxalato salía con 1,06 y en verde, porque el semáforo mide contra el 1,0-2,0 de FEDIAF, que es el rango de un perro sano. El mecanismo es genérico, así que al **omega-6:omega-3 ya no le falta motor: le falta el número** (PREGUNTA 40). BLOQUE 75 y `HECHO.md`
- [x] **Los `avisos_extra` de patología, PINTADOS** — HECHO 10 sep. Eran ocho y ya son **veinte**; la API los mandaba con cada menú desde el 29 de agosto y `respuestaApiAMenu` no los recogía, así que se perdían. Ahora salen dentro del panel de «lo tiene que aprobar tu veterinario». Y al ir a pintarlos se vio que **dos mentían**: el aviso de cardiopatía B2 decía 900 mg/1000 kcal de sodio y el motor aplica 739, y el de estadio C decía 790 y aplica 625. BLOQUE 74 y `tests/avisos-de-patologia.spec.js`
- [~] **La higiene de la casa, DICHA** — HECHO 10 sep: panel «Higiene en casa» junto al de Congelación. El perro que come crudo excreta más bacterias aunque esté sano (SACN5 cap.56), y eso protege a las personas, no a él. Queda pendiente la otra mitad: preguntar si en casa hay alguien de riesgo, que es una casilla y cambia lo que hay que decir
- [ ] Sugerir patologías por raza: ahora hay **tres** tablas de fuente, incluida la de urolitos, cuyas seis patologías el motor ya tiene
- [ ] **¿Duerme fuera?** FEDIAF §7.2.3.5 cuantifica el invierno: **10 a 90 % más de calorías**, y 2-5 kcal/kg^0,75 por cada grado bajo la zona termoneutra. La ficha no pregunta dónde vive el perro, así que hoy un mastín en el patio en enero recibe lo mismo que un perro de piso. Y **la cifra existe**: SACN5 Tabla 5-3 la da por tipo de pelo y salto de temperatura (pelo corto +95 %, pelo largo +59,5 %, Labrador +25 %, Gran Danés +22 %). Lo que falta es **la pregunta en la ficha**, que es decisión de producto
- [ ] **La masa muscular (Tabla VII-3 de FEDIAF), que no es el BCS.** La salvedad ya está puesta el 9 sep (`salvedadDelBcs`, avisa en la parte baja de la escala); la escala entera es una pantalla de palpación y falta. Importa en la ficha del veterinario: un perro puede estar obeso y sarcopénico a la vez
- [~] Ajustes de cuenta: falta método de pago (portal Stripe) y darse de baja de verdad
- [ ] Volver a encender el muro de pago cuando toque (`VITE_PAYWALL`, dos pruebas paradas a propósito)
- [ ] Los 34 pesos de referencia que faltan en «cómo preparar» (verduras y frutas)
- [ ] Borrar las ramas viejas — ⚠️ **RECUENTO CORREGIDO 8 sep**: la auditoría del 23 de agosto era buena pero está caducada. Hoy hay **11 ramas vivas y 6 nunca se miraron** (22 commits fuera de `main`), y **cuatro de ellas suenan a trabajo nutricional**. Solo 5 son borrables, comprobadas con `--is-ancestor`. Lista real y comandos: `TRASPASO.md` §1
- [ ] Rellenar a mano la fecha de nacimiento de los perros guardados antes del 21 de agosto
- [ ] Una versión para dueños y otra para veterinarios — decidido, plan completo en `VETERINARIOS.md`
- [ ] Personalizar perro por perro cuando son varios
- [ ] Entrar con Google — hecho y deshecho, bloqueado por los textos legales
- [ ] Entrar con huella en el móvil (passkeys, API experimental)
- [ ] Apartado de sugerencias
- [ ] Apartado de incidencias
- [ ] Límite de 2 cambios de alimento por menú en la versión gratis
- [ ] `aviso_composicion` en la web: ver cómo queda con tres alergias
- [ ] `tipo_de_clave_supabase` sale como `[Filtered]` en Sentry (renombrar)
- [ ] La `HTTPException` genérica del webhook sobra en Sentry
- [x] `/perro/{id}/menus` — ARREGLADO 7 sep, era el único agujero en la regla 1: la tabla no guardaba la etapa ni el DER, así que el menú no se podía verificar NI EN PRINCIPIO. Ahora se guarda el contexto con el menú y se verifica al leerlo. BLOQUE 47

## `PENDIENTE_NUTRICION.md` — auditado contra el PDF oficial

- [ ] ⚠️ **El TECHO de hierro de la hepatopatía** (11 sep, caps.50-70 de SACN5): la Tabla 68-8 da un rango, «80 to 140 mg/kg», y el motor aplica solo el suelo (20 mg/1000 kcal). El extremo alto tiene mecanismo escrito —el hierro se acumula en el hígado y cataliza la peroxidación— y para el potasio de la enteropatía se tomó la decisión CONTRARIA, aplicando el techo. **Medido: el techo de 35 lo cruzan 3 de los 216 menús (1,4 %), los tres de crecimiento o gestación**; en adulto, ninguno
- [ ] **La dosis de omega-3 de la enteropatía crónica** (11 sep): 175 mg/kg/día, rango 50-300. Es del TEXTO del cap.57 y no de su tabla, que es por lo que no la encontró el trabajo de transcribir tablas. La propia fuente dice que no hay ensayo en perro, así que su sitio es `limites_escritos_que_el_solver_no_aplica` — y hoy no está escrita en ninguna parte
- [ ] **La B12 le falta al aviso de la insuficiencia pancreática** (11 sep): el de `enteropatia_cronica` sí la lleva; la EPI tiene la cifra más alta de las dos (82 % de los perros) y no la menciona
- [ ] **La forma química de las vitaminas B, ficha por ficha** (Tabla VII-14 de FEDIAF). Medido: con el peor factor de la tabla el ácido pantoténico caería POR DEBAJO del mínimo de FEDIAF con el menú en verde, y la tiamina aguanta por un 2 %. Las conversiones de UI sí están comprobadas (BLOQUE 70)
- [ ] **La lactosa del «Yogur griego»**: SACN5 da el umbral (1 g/kg de peso) y el catálogo no tiene el dato. 0 de 216 menús lo usan hoy, pero Extras va siempre libre
- [x] Contrastar con la ficha original de USDA — RESUELTO 7 sep: testículos de cordero ya no existe en el catálogo, timo de ternera ya cita FDC 170194 directo, y el acceso a USDA (`DEMO_KEY`) sí funciona (usado para el linoleico de abajo)
- [x] El linoleico de la grasa de pollo — RESUELTO 7 sep: 19,5 g/100g, USDA FDC 173564
- [x] El aviso de datos incompletos ya no depende de una lista a mano — RESUELTO 7 sep: `[SOSPECHOSO]` en `auditar_catalogo.py` compara cada alimento con los demás de su categoría (BLOQUE 46). Encontró 11 huecos el mismo día
- [ ] Enganchar (o no) ese detector al aviso que ve la usuaria — decisión abierta, hoy acierta 9 de 13
- [x] EPA/DHA de los seis pescados — ya estaban cerrados desde el 25 ago; el punto llevaba describiendo trabajo hecho (verificado 7 sep)
- [x] Las cuatro vísceras sin dato — COMPLETADAS 7 sep con la ficha de su fuente (BEDCA 1047 el cerebro; USDA 169454/169452/174364 las otras tres, que coincidían celda a celda)
- [x] Las dos «discrepancias» del cerebro — RESUELTAS 7 sep, y NO eran errores: calcio 43 y selenio 21,3 son exactos de cerebro de VACA (USDA 168622) y se comparaban contra cerebro de ternera. La ficha se llamaba «de ternera» con datos de vaca, igual que pasó con el bazo y el páncreas: renombrada a `Cerebro de vaca` y rehecha entera desde su fuente real. El araquidónico del pavo también se retiró: era un fallo de mi herramienta (USDA publica dos filas de 20:4 y el catálogo usa la buena)
- [x] Decisión pendiente: `Laringe de vacuno` — RESUELTO 7 sep: movida a `Extras`
- [x] Vísceras de ave — NO EXISTEN en BEDCA, CIQUAL ni USDA (comprobado 7 sep): de pollo/pavo/pato/oca/conejo solo hay hígado, corazón y molleja, y los tres últimos ya están (en Carne muscular, porque no segregan)
- [ ] ⚠️ DECISIÓN: `Timo de ternera` y `Pulmón de ternera` tampoco son de ternera (11/11 y 10/11 celdas coinciden con las fichas de VACA de USDA). Y no es cosmético: el timo de vaca tiene 20,35 g de grasa y 236 kcal, el de ternera 3,07 y 101 — quien compre mollejas de ternera da algo muy distinto de lo que el menú calculó. O se renombran (como el bazo y el páncreas en agosto) o se cambian los datos a los de ternera. Detalle en `PENDIENTE_NUTRICION.md`
- [ ] Buscado 8 sep si hay ESTUDIOS con vísceras de ave: lo mejor es Seong et al. 2015 (Food Sci. Anim. Resour. 35(2):179-188), ocho despojos de pollo con proximal, 10 minerales, 6 vitaminas, 17 aminoácidos y grasos — pero NO trae bazo, páncreas, riñón ni timo, y le faltan vitD, vitE, B12, folato, colina y yodo (dos de ellos, topes de seguridad). Lo único aprovechable sería el PULMÓN de pollo, y entraría con seis huecos. Decisión, no dato
- [ ] Vísceras solo tiene DOS especies (bovino y ovino) y es pilar obligatorio: un perro alérgico a las dos se queda sin ninguna. Es decisión de producto (admitir cerdo, o decirlo claro), no un dato que falte
- [x] Taurina y L-carnitina — RESUELTO 7 sep: dato en las 159 fichas y suelo activado en `dcm_taurina_respondedora` (250/50 mg/1000kcal, SACN5 cap.36)
