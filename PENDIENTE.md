# Rawku — lo que queda por hacer (índice)

Lista viva. Se actualiza al terminar cada cosa, no al final.
Última revisión: 7 de septiembre de 2026.

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

- [ ] Ejecutar el SQL de la fase 0 en Supabase (rol profesional)
- [ ] La lista de las nueve `formulable: false` (la necesita la fase 4)
- [ ] Tres cambios de producto sobre la estimación por BCS por debajo de 5
- [ ] Cuatro fichas de aminoácidos que hay que mirar en su fuente
- [ ] El máximo de lisina de FEDIAF: ¿sobre qué proteína se mide? (para el nutricionista)
- [ ] Límites por patología: confirmar los números (fósforo, cobre, grasa)
- [ ] Siete preguntas para Cris (proteína senior, estadio ACVIM, pancreatitis en cachorro, umbral 1,10, tiaminasa, qué firma un veterinario, qué hace AnVet)
- [x] La app no distingue hepatopatía por cobre de otras hepatopatías — RESUELTO 7 sep (`raza_predispuesta_cobre`)
- [ ] Repasar la transcripción de la tabla de FEDIAF en `auditar_fediaf.py`
- [x] Auditar los valores de los ALIMENTOS — RESUELTO 7 sep: la auditoría ya existía (`auditar_catalogo.py`), se ejecutó de verdad y se investigaron sus 20 avisos. Ver `PENDIENTE_DECISIONES.md`
- [x] Fibra de la borraja — CERRADO 7 sep: el alimento ya no existe en el catálogo, no es un hueco de dato
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

- [~] Ajustes de cuenta: falta método de pago (portal Stripe) y darse de baja de verdad
- [ ] Volver a encender el muro de pago cuando toque (`VITE_PAYWALL`, dos pruebas paradas a propósito)
- [ ] Los 34 pesos de referencia que faltan en «cómo preparar» (verduras y frutas)
- [ ] Borrar las ramas viejas de los dos repos (15 ya comprobadas, nada que rescatar)
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
