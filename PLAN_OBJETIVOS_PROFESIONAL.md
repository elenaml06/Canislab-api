# Objetivos por nutriente: qué hace falta para que un profesional pueda pedirlos

**8 de septiembre de 2026.** La idea: que además de elegir alimentos y gramos, un
profesional pueda decir *«quiero la grasa aquí, la proteína aquí, el yodo aquí —
y respeta mis alimentos en lo posible»*, y que el motor calcule el resto.

Este documento dice **qué ya funciona** (medido, no supuesto), **qué falta** y
**en qué orden**.

---

## 1 · Lo que YA funciona hoy, medido

El solver es un MILP: cada nutriente es una fila de la matriz con su mínimo y su
máximo. Poner un objetivo **es exactamente eso**, y el mecanismo ya existe y es
genérico — `topes_patologia` y `suelos_patologia` son diccionarios
`{clave: valor}` que se combinan con `min()` y `max()` contra los de FEDIAF
dentro del bucle que recorre los 44 requisitos del `MAPA`.

Medido el 8 de septiembre, perro adulto de 22 kg, catálogo real:

| Lo que se pide | Resultado |
|---|---|
| grasa ≤45 / 40 / 37,5 / 35 / 30 / 28 | menú **verde** en los seis, y la grasa sale clavada: 45,0 · 40,0 · 37,5 · 35,0 · 30,0 · 28,0 |
| grasa ≤25 | **sin menú** |
| sodio ≤739 | verde, sodio 496,8 |
| fósforo ≤1200 **y** sodio ≤739 | verde, 1165,2 y 453,0 |
| «solo pavo, conejo y sardina» + grasa ≤40 | verde, grasa 40,0, y de carne **solo entra conejo** |
| «solo pavo, conejo y sardina» + fósforo ≤1200 | verde, 1198,8, y de carne solo pavo |

Y la salvaguarda aguanta sola: pedí a propósito **cobre ≤200 mg/1000 kcal**, unas
siete veces el máximo legal. El menú salió con **2,32**. El `min()` contra el
máximo de FEDIAF hace que **un objetivo solo pueda apretar, nunca aflojar**. Eso
no hay que construirlo.

La restricción por alimentos (`restringir_a_elegidos`) también existe ya: es lo
que usa la pantalla de Personalizar.

**Dos datos de producto que salen de la medición:**

- **La frontera práctica de la grasa está entre 25 y 28 g/1000 kcal.** Por debajo
  no hay comida real que lo consiga. La pantalla debería saberlo y avisar antes
  de que alguien pulse y espere.
- **El motor empuja hasta el límite**: pidiendo «≤40» devuelve 40,0, no 35. Si lo
  que se quiere es *un objetivo* y no *un techo*, hay que poder dar mínimo **y**
  máximo.

---

## 2 · Lo que falta, por capas

### Capa 1 · La puerta de entrada (API)

Hoy los objetivos solo entran leyendo `patologias.json`. `resolver()` ya acepta
lo que hace falta por dentro, pero **no hay forma de pasárselo desde fuera**.

Contrato propuesto para `/menu/v2` y `/formular/autocompletar`:

```json
"objetivos": {
  "grasa":    {"max": 40, "unidad": "g_por_1000kcal"},
  "proteina": {"min": 90, "max": 110, "unidad": "g_por_1000kcal"},
  "fibra":    {"min": 10, "unidad": "pct_materia_seca"}
}
```

- Claves: las **44 del `MAPA`** (todos los nutrientes de FEDIAF, los 12
  aminoácidos incluidos, más `taurina`, `lcarnitina`, `fibra` y las dos sumas).
  Cualquier otra clave se rechaza con error, no se ignora en silencio.
- `min` y `max` opcionales por separado. Los dos a la vez = banda.
- **Nunca igualdad exacta.** Pedir «grasa = 30» casi siempre no tiene solución;
  se pide una banda y se explica por qué.

### Capa 2 · Las unidades, en un solo sitio

Un profesional piensa en **% de materia seca** o en **% de las kcal**; el motor
en **g por 1000 kcal**. Hay que aceptar las tres y convertir **en una sola
función**, o volvemos a tener el mismo número calculado de dos formas — que es el
fallo de la fibra otra vez, y el de la duplicación del DER.

```
pct_materia_seca → × 25   (a la densidad de referencia de 4000 kcal EM/kg MS)
pct_kcal_grasa   → × 1000 / 9   (Atwater)
g_por_1000kcal   → tal cual
```

⚠️ **La conversión desde % de materia seca asume 4000 kcal/kg MS y una ración
BARF no lo cumple.** Es la misma trampa que documenta `DECISIONES.md` D-12 sobre
el Reglamento europeo. Cuando el profesional pida en % MS, la pantalla tiene que
enseñarle el valor convertido **antes** de resolver, para que vea sobre qué se
está pidiendo de verdad.

### Capa 3 · La verificación — sin esto, lo demás no vale nada

**Es lo primero que hay que cerrar.** Hoy, si el profesional pide grasa ≤30 y el
menú sale con 45, **el menú saldría verde**: el semáforo comprueba los requisitos
de FEDIAF, y un objetivo pedido a mano no es de FEDIAF.

Es literalmente el mismo fallo que ya documenta el `CLAUDE.md` con los topes de
patología («el semáforo de FEDIAF no los ve: son los requisitos de un perro SANO,
y un renal con 3084 mg de fósforo salía verde»).

Los objetivos manuales tienen que comprobarse en `_garantizar_verificado()`,
igual que los topes de patología, y **el menú no sale si no se cumplen**.

### Capa 4 · Decir por qué no, cuando no hay menú

Ya existe el mecanismo: `diagnosticar_choque_de_patologias()` suelta un límite
cada vez y ve cuál desbloquea. Hay que engancharlo a los objetivos manuales.

Dos respuestas distintas, y las dos hacen falta:

- **«Tu grasa ≤25 choca con el mínimo de ácido linoleico.»** Dos restricciones
  que no caben juntas.
- **«Con los alimentos que has elegido no se llega al yodo: faltan X µg. Esto lo
  arreglaría.»** Falta un aporte, no sobra una restricción.

La segunda es, en mi opinión, la funcionalidad más valiosa de todo el plan: a un
profesional le sirve más un diagnóstico que un menú.

### Capa 5 · La pantalla

Vive **del lado del profesional**, no del dueño. El eje es **el rol, no el
diagnóstico**: un dueño no sabría qué poner y un número mal puesto es peor que
ninguno; y atarlo a la patología haría que alguien marque una patología falsa
para desbloquear la herramienta.

Lo que tiene que enseñar por cada nutriente, y esto es exactamente lo que aporta
`PATOLOGIAS.md`:

- el **valor por defecto** que aplica el motor,
- el **rango de la fuente**, con la cita,
- el **techo duro** y de dónde sale (legal · seguridad · mínimo de FEDIAF),
- y si el valor pedido **cruza el mínimo de FEDIAF**, avisar de que eso convierte
  el menú en **prescripción firmada**.

### Capa 6 · «Respeta mis alimentos en lo posible»

Hoy `restringir_a_elegidos` es **duro**: solo esos, y si no hay solución, falla.
Lo que hace falta además es **blando**: *estos primero, añade lo mínimo
imprescindible, y di qué añadiste y por qué*.

Es implementable —se penaliza en la función objetivo lo que no se eligió— pero
**toca la función objetivo, no la matriz**, que es más delicado que todo lo
anterior. Va el último a propósito.

---

## 3 · El orden, y por qué

| | Qué | Por qué ahí |
|---|---|---|
| 1 | Objetivos en la API + **comprobación en `_garantizar_verificado`** | Sin la comprobación, todo lo demás es cosmética: el motor diría que sí y entregaría un menú que no cumple |
| 2 | Diagnóstico de qué choca y qué falta | Barato (el mecanismo existe) y es la mitad del valor |
| 3 | Unidades y conversión en un solo sitio | Hace falta antes de que lo use una persona, no antes de que funcione |
| 4 | La pantalla del profesional | Se alimenta de `PATOLOGIAS.md` |
| 5 | El modo blando | El más difícil y el que menos duele si tarda |

---

## 4 · Los riesgos, dichos claro

1. **Un objetivo mal puesto puede tumbar algo que nadie estaba mirando.** Grasa
   ≤20 arrastra el ácido linoleico. El motor tiene que **negarse con
   explicación**, nunca obedecer a medias.
2. **La regla 1 no se toca.** Ningún menú sale sin verificar, y ahora hay un
   juego de requisitos más que verificar.
3. **El registro no es opcional** (D-13): quién, cuándo, de qué valor a qué
   valor. Un menú que salió porque alguien movió un número tiene que poder
   explicarse dentro de un año.
4. **Los límites legales y de seguridad se aplican solos** por la aritmética del
   `min()`/`max()` — pero eso hay que **probarlo con un test**, no confiarlo. Lo
   medí una vez (cobre ≤200 → 2,32) y esa medición tiene que volverse un bloque
   de la batería, o el día que alguien cambie el orden de las combinaciones se
   romperá en silencio.
