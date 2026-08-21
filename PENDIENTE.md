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

**161 de 161 comprobaciones cuadran exactas** — mínimos *y* máximos. Se
verificó, para los 30 nutrientes del JSON y en las tres etapas: el valor,
la unidad, y que todo esté por 1000 kcal de energía metabolizable.

Los máximos son la cara de la toxicidad y vienen de dos sitios distintos,
que es donde es fácil equivocarse: los nutricionales están en la III-3b ya
por 1000 kcal, y los legales de la UE **solo** en la III-3a, por 100 g de
materia seca — se pasan multiplicando por 2,5 (FEDIAF usa 4000 kcal/kg MS
de referencia). Ese ×2,5 no es una suposición: cuadra en los dos sitios
donde ambas tablas dan el mismo dato, vitamina A (40.000 × 2,5 = 100.000)
y vitamina D (320 × 2,5 = 800).

También se comprueba lo contrario: que el JSON **no se invente** máximos
donde FEDIAF no da ninguno. La vitamina E es uno de esos casos.

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

### Vitamina E de los suplementos — resuelto el 21 de agosto

No eran UI apuntadas como mg, era más sutil: **eran mg de la forma
sintética**. En la UE los piensos declaran la vitamina E como acetato de
all-rac-α-tocoferilo, mientras que los alimentos traen α-tocoferol natural
y el requisito está en natural. Dos monedas en la misma columna, con los
suplementos contando un 49 % de más.

Confirmado con la etiqueta de NEKTON (160.000 UI de A, 20.000 UI de D3 y
2.000 **mg** de E por kg — las tres cuadran con el catálogo) y con la
equivalencia oficial de la EFSA. Convertidos los 9 multivitamínicos ×0,67.
Comprobado que los menús siguen entre 1,5 y 9 veces el mínimo.

---

## 5-bis. Huecos de datos sin declarar (encontrado el 21 de agosto)

Comprobando si los nutrientes se miden en la base correcta salió esto.
Primero lo bueno: **la base está bien**. 68 de 69 alimentos cárnicos
cuadran al contrastar su energía declarada contra sus macros por Atwater,
y ninguna verdura da un ratio imposible. Nutrientes y calorías están en la
misma base (peso fresco) en todo el catálogo, así que el cálculo «por 1000
kcal» es correcto y el agua no lo distorsiona — que era la duda.

Pero aparecieron tres alimentos con casi todo a cero **sin declararlo**:

| Alimento | Nutrientes a cero | Declarados en `sin_dato` |
|---|---|---|
| Timo de ternera | 28 de 31 | **0** |
| Testículos de cordero | 30 de 31 | **0** |
| Grasa de pollo | 28 de 31 | 6 |

Y el motor **usa el timo de ternera**: salió en 1 de 20 menús de prueba.

El campo `sin_dato` existe justo para distinguir «no lo tiene» de «no lo
sabemos», y la diferencia es asimétrica:
- En los **mínimos**, contar un hueco como cero es conservador: como mucho
  se añade un suplemento que no hacía falta.
- En los **máximos** es peligroso: se puede uno pasar de cobre o de
  vitamina A sin enterarse. Y el timo es una víscera, ricas justo en eso.

**Esto no lo puede decidir el código:** que la grasa de pollo tenga casi
todo a cero es verdad (es grasa pura), y que el timo lo tenga es un hueco.
Distinguirlo hace falta mirar la fuente.

- [ ] Revisar esos tres alimentos y, para cada nutriente a cero, decidir
      si es un cero real o un hueco. Los huecos, a `sin_dato`.
- [ ] Mientras tanto, decidir si el timo y los testículos se quedan en el
      catálogo. Con el 90 % de su composición desconocida, cualquier menú
      que los use tiene sus máximos sin comprobar de verdad.
- [ ] Plantearse que el aviso de datos incompletos no dependa de una lista
      mantenida a mano: un alimento con el 90 % de los valores a cero es
      sospechoso por sí solo, lo declare o no.

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
