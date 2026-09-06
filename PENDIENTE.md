# Rawku — lo que queda por hacer (índice)

Lista viva. Se actualiza al terminar cada cosa, no al final.
Última revisión: 6 de septiembre de 2026.

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
- [ ] La app no distingue hepatopatía por cobre de otras hepatopatías
- [ ] Repasar la transcripción de la tabla de FEDIAF en `auditar_fediaf.py`
- [ ] Auditar los valores de los ALIMENTOS (`alimentos_v3_final.json` no tiene auditoría, a diferencia de los requisitos)
- [ ] Fibra de la borraja (falta el dato, hoy tiene un `0.0` que no es real)
- [ ] ¿Rawku apunta a algún rango de fibra? — decisión de nutrición, no de código
- [ ] ¿Hace falta estar dada de alta como autónoma para cobrar? (pregunta a la gestoría)
- [ ] Revisar los textos legales cuando estén redactados — bloquea Stripe y Google

## `PENDIENTE_DINERO_Y_SALUD.md` — lo urgente, antes de cobrar, lo que mira Stripe

- [ ] `/menu/varios-perros` devuelve a veces 1 menú en vez de 3 (presupuesto de tiempo, no cabe con 2 perros y 3 menús)
- [ ] El canario del BLOQUE 14 cantó: 0,99 g de salmón (falta un mínimo por alimento semicontinuo en el solver)
- [ ] Nadie debería poder suscribirse dos veces
- [ ] El yodo de los perros muy pequeños vive al 101 % del mínimo (el margen de redondeo no escala)
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
- [ ] `/perro/{id}/menus` devuelve menús sin verificar

## `PENDIENTE_NUTRICION.md` — auditado contra el PDF oficial

- [ ] Contrastar con la ficha original de USDA (testículos de cordero: grasa y selenio son deducidos, no leídos)
- [ ] El linoleico de la grasa de pollo sigue sin dato (y tiene máximo en cachorros)
- [ ] Plantearse que el aviso de datos incompletos no dependa de una lista mantenida a mano
- [ ] Conseguir cifras verificadas de EPA/DHA para seis pescados (incluido el boquerón)
- [ ] Completar las cuatro vísceras sin dato (bazo de vaca, páncreas de vaca, bazo de cordero, cerebro de ternera)
- [ ] Decisión pendiente: `Laringe de vacuno` — ¿mover a Extras o quitar del catálogo?
- [ ] Añadir vísceras e hígados de las especies que faltan (pollo, pavo, pato, cerdo)
