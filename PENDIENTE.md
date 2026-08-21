# Rawku — lo que queda por hacer

Lista viva. Se actualiza al terminar cada cosa, no al final.
Última revisión: 20 de agosto de 2026.

El orden **no** es por lo que parece más urgente, sino por lo que
desbloquea al resto y por lo que cuesta más caro si sale mal. Cobrar dos
veces a alguien duele más que no tener login con Google.

---

## 0. Decisiones tuyas (no son trabajo de programación)

Estas bloquean cosas de abajo. Ninguna lleva más de unos minutos, pero
las tiene que tomar una persona, no yo.

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
- [ ] **¿Hace falta estar dada de alta como autónoma para cobrar?**
      Pregunta para la gestoría, antes de rellenar el tipo de negocio en
      Stripe. Bloquea la verificación del negocio.
- [ ] **Revisar los textos legales** cuando estén redactados (ver 3.1).
      El borrador lo puedo escribir yo; el visto bueno no.

---

## 1. Urgente — dinero y salud

### 1.1 Nadie debería poder suscribirse dos veces
Encontrado el 20 de agosto probando: se crearon **seis suscripciones
activas para el mismo `user_id`** sin que nada lo impidiera. En producción
eso son seis cobros mensuales a la misma persona.

Hace falta, antes de abrir el cobro:
- Antes de crear el checkout, mirar si esa persona ya tiene una
  suscripción activa; si la tiene, mandarla al portal de cliente en vez de
  crear otra.
- Al cancelar, no poner `plan = free` a ciegas: comprobar si le queda
  alguna otra suscripción viva. Hoy una cancelación de cualquiera de las
  seis dejaría a la persona sin premium teniendo cinco pagadas.

### 1.2 El tope de patología no se respeta
Con el límite renal en 1400, el motor devuelve fósforo a **1426**. La
restricción existe pero no se cumple: probablemente por la tolerancia del
solver (`mip_rel_gap`) y el redondeo final. En un perro renal, pasarse del
tope es justo lo que no puede pasar.

### 1.3 Comprobar que la cancelación quita el premium
Dar de alta está probado de punta a punta. Cancelar **no**. Si no funciona,
se regala la app a quien se dé de baja. (Relacionado con 1.1: hay que
probarlo con una sola suscripción activa, si no el resultado engaña.)

---

## 2. Antes de poder cobrar de verdad

- [ ] Verificar el negocio en Stripe (datos, IBAN, NIF) — ver la guía.
- [ ] Crear productos, precios y webhook en la cuenta **real**: los de
      ahora son de la sandbox, y no existen en producción.
- [ ] Quitar `STRIPE_PRUEBA` de Render cuando termine la fase de pruebas.
- [ ] Primer cobro real hecho por ti, con tu tarjeta, y reembolsado.

---

## 3. Lo que Stripe va a mirar en la web

### 3.1 Páginas legales que no existen
Comprobado el 20 de agosto: **no hay política de privacidad, ni términos y
condiciones, ni aviso legal, ni política de reembolso.** De cancelar solo
hay una frase suelta. Es de los motivos más comunes de rechazo en la
verificación, y para un negocio europeo que guarda datos personales
también es exigible por ley.

Los precios sí se ven antes de pagar, y qué vendes se entiende. Eso está.

---

## 4. Producto — funcionalidades nuevas

Ordenadas por dependencia: multi-perro va primero porque la cesta y los
menús comparados no tienen sentido sin él.

- [ ] **Varios perros por cuenta.** La base ya está preparada (los menús se
      guardan con `perro_id`, no con `user_id`), pero la app solo maneja uno.
- [ ] **Cesta de la compra**, diferenciando de quién es cada cosa
      («para Cairo» / «para Nala» / «para los dos»). Solo aparece la
      distinción si hay más de un perro.
- [ ] **Menús parecidos entre perros** de la misma casa, para no tener que
      comprar y porcionar el doble de cosas.
- [ ] **Ajustes de cuenta** (no del perro): cambiar contraseña, correo,
      método de pago, darse de baja.
- [ ] **Entrar con Google.**
- [ ] **Entrar con huella en el móvil.** Sí es posible: se hace con
      *passkeys* (WebAuthn), que Supabase Auth soporta. No es la huella en
      sí lo que viaja, sino una llave que el móvil guarda y desbloquea con
      ella. Depende de tener antes los ajustes de cuenta.
- [ ] **Apartado de sugerencias.**
- [ ] **Apartado de incidencias** (problemas con el pago y demás).
- [ ] **Límite de 2 cambios de alimento por menú en la versión gratis**,
      con botón de deshacer por cambio y restaurar el menú original.

---

## 5. Nutrición — auditado contra el PDF oficial

**Hecho el 21 de agosto** contra la TABLA III-3b de la *FEDIAF Nutritional
Guidelines 2025* (el PDF oficial, no de memoria). Script reproducible en
`auditar_fediaf.py`.

**84 de 84 comprobaciones cuadran exactas.** Se verificó, para los 30
nutrientes del JSON y en las tres etapas: el valor, la unidad, y que todo
esté por 1000 kcal de energía metabolizable.

También quedó confirmado el mapeo de columnas, que no era obvio:
- `Adulto` usa la columna **95 kcal/kg^0,75**, la más exigente de las dos
  que da FEDIAF para adultos. Es la decisión conservadora, y es correcta.
- `CachorroJoven` = *Early Growth* (< 14 semanas) y reproducción.
- `CachorroCrecimiento` = *Late Growth* (≥ 14 semanas).

La vitamina E parecía discrepar (6,968 mg frente a 10,40 UI) y **no es un
error**: está convertida a 0,67 mg/UI, que es la equivalencia del
α-tocoferol natural, la forma en que las tablas de composición declaran la
vitamina E de los alimentos. Está documentado en el propio JSON.

### Respuesta a «¿usamos todos los nutrientes de FEDIAF?»

De los 44 de la tabla, el JSON cubre 30. Lo que falta:

- **Los 12 aminoácidos esenciales** (arginina, histidina, isoleucina,
  leucina, lisina, metionina, metionina+cistina, fenilalanina,
  fenilalanina+tirosina, treonina, triptófano, valina).
- Biotina (B7) y vitamina K: **FEDIAF no les pone mínimo** en esta tabla
  (aparecen con «-»), así que aquí no falta nada.

**No se pueden añadir hoy, y el motivo es el catálogo, no el motor:**
ninguno de los 163 alimentos tiene dato de aminoácidos. Añadir el
requisito sin el dato haría que todos contaran como cero y ningún menú
saldría nunca. Para hacerlo haría falta primero conseguir el perfil de
aminoácidos de los 163 alimentos.

Contexto para decidir si merece la pena: una dieta que cubre la proteína
con fuentes animales variadas cubre los aminoácidos esenciales de sobra —
por eso muchas guías prácticas se quedan en la proteína total. El caso
donde importa de verdad es una dieta con poca proteína animal.

- [ ] **Vitamina E de los suplementos: ¿UI o mg?** Los multivitamínicos
      del catálogo llevan valores de 200 a 670, y los fabricantes suelen
      declarar la vitamina E en UI. Si son UI contadas como mg naturales,
      están sobrevaloradas un 49 %. Medido: aun en el peor caso los menús
      aportan de 1,5 a 7 veces el mínimo, así que **hoy nadie se queda
      corto** — pero conviene confirmarlo etiqueta en mano.

---

## 6. Deuda técnica y detalles

- [ ] **Cantidades no medibles.** Salen ingredientes de 0,15 g de sal y
      hasta 0,04 g de kelp en casos con muchas restricciones. Nadie pesa
      eso en casa. Decidir si se redondea o se muestra como «una pizca».
- [ ] **`aviso_composicion` en la web**: ya se pinta, pero conviene ver
      cómo queda en pantalla con un perro con tres alergias.
- [ ] **El campo `tipo_de_clave_supabase` sale como `[Filtered]`** en
      Sentry: su propio filtro lo censura por llamarse «clave». Renombrarlo
      para que el diagnóstico se vea.
- [ ] **La `HTTPException` genérica del webhook sobra en Sentry**: tapa a
      la que sí explica el motivo. Mandar solo la informativa.
- [ ] **`/perro/{id}/menus` devuelve menús sin verificar** (la tabla no
      guarda etapa ni DER). Hoy no lo usa nadie, pero si se usa, hay que
      pasarlo por `/menu/revalidar` antes de enseñarlo.

---

## Hecho el 20 de agosto

- Sentry en el backend, con avisos por correo.
- Los cinco fallos del webhook de Stripe, que **no había funcionado nunca**.
- Verificación obligatoria contra los 30 requisitos en **todos** los
  caminos, incluido el cambio de etapa (`/menu/revalidar`).
- La escalera de relajación: del 23 % de fallos con alergias al 0 %, sin
  ceder en ningún límite.
- Tope de volumen y porciones que escalan con el tamaño del perro.
- Cobro de prueba completado de punta a punta y premium activado de verdad.
