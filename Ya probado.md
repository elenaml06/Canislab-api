# YA PROBADO — lo que se intentó y NO funcionó

**Extraído de las 14 sesiones (31 julio – 2 agosto).**

Este archivo existe porque cada sesión nueva empieza sin saber qué se
descartó. Sin esto, se vuelven a proponer cosas ya probadas, y desde fuera
parece que damos vueltas — porque las damos.

> **REGLA: leer esto ANTES de proponer cualquier cambio en el motor.**
> Si lo que vas a proponer está aquí, no lo propongas: di que ya se probó
> y por qué falló.

---

## ❌ DESCARTADO — no volver a proponerlo

| Qué se intentó | Por qué se descartó | Sesión |
|---|---|---|
| **Solver de Excel** para optimizar la ración | Demasiado manual, el usuario no quiere pasos a mano. Hoja OPTIMIZADOR eliminada | 31 jul |
| **Replit** para alojar el backend | Reconstruye el código desde cero por su cuenta | 1 ago |
| **Poda iterativa** de alimentos en el LP | *"La poda no está reduciendo casi nada — sigue en 11-13"*. Se dejó el motor como estaba. **⚠️ OJO: el código de poda SIGUE en `optimizar_menu` (bucle de 40 vueltas)** — revisar si aporta algo o es peso muerto | 2 ago (s7) |
| **Ratio fijo BARF** (80/10/10 y similares) como regla dura | Folclore de divulgación sin respaldo. Descartado **dos veces** | 2 ago (s8) |
| **Doblar la dosis de suplemento** para cubrir huecos | *"Doblar la dosis no mejora, EMPEORA"*. Linolénico, cloruro y magnesio no se arreglan con más suplemento | 2 ago (s8) |
| **Mejillón y pulpo** como candidatos habituales | Descartados por datos poco fiables | 2 ago |
| **Yogur griego** entre los candidatos | 150 mg calcio/100g, distorsionaba el cálculo | 2 ago |
| **Prohibición dura de crucíferas** | Bajo respaldo; el efecto goitrogénico requiere dosis muy altas | 2 ago (s8) |

## 🔄 REVERTIDO — se cambió y hubo que deshacerlo

| Cambio | Por qué se revirtió | Sesión |
|---|---|---|
| **Corazón → categoría Vísceras** | Es músculo de verdad, no víscera glandular. Daba menús con 303 g de corazón. **Revertido a Carne muscular** | 1-2 ago |
| **Valores de ternera "corregidos"** | Los originales YA eran correctos. Se "corrigieron" sin comprobar y hubo que volver atrás | 2 ago (s7) |
| **Valores de vitaminas de FEDIAF "corregidos"** | Se compararon UI contra µg. Los originales eran correctos | 2 ago |
| **Desplegable de selección manual** | Se cambió y se volvió al desplegable normal con formato condicional | 31 jul |

## ⚠️ PROBLEMAS QUE YA APARECIERON ANTES (y han vuelto)

| Problema | Cuándo salió | Estado |
|---|---|---|
| **El hígado sale a cero o casi** | Sesión 8: *"if liver is still coming out as zero… removing small liver amounts below the 0.1g threshold"* | **VOLVIÓ el 2 ago**: 11 g en un menú de 1094 g. Causa: el mínimo estaba en 1%. Subido a 3% |
| **Recálculo deja pocos ingredientes** | El usuario dice que ya pasó y se corrigió | **VOLVIÓ el 2 ago**. NO reproducido en pruebas (8 cambios distintos dan 10-12 ingredientes) |
| **Volver a pasar por todos los pasos tras editar el perfil** | Sesiones 3, 4 y app-design | Limitación conocida, nunca resuelta |

## 🧱 LÍMITES REALES DEL MOTOR (no son fallos, son la herramienta)

- **`scipy.linprog` es LP, no MILP**: se puede exigir "carne ≥25 g EN TOTAL", pero NO "cada carne, o 0 o ≥25 g". Por eso salen cantidades pequeñas raras (~5% de las líneas)
- **El LP minimiza coste → cada categoría se va a su MÍNIMO.** Esto significa que **los mínimos SON la receta**. Si un mínimo está mal puesto, el menú sale mal y nadie se entera
- **Cada restricción nueva baja la factibilidad.** Medido el 2 ago: 73% → 68% (tope verdura) → 62% (mínimo hígado). Estamos peleando contra el optimizador
- **Renal y pancreatitis: 0/3 menús factibles.** Comprobado que ya era así antes del cambio de verdura. Son restricciones inherentemente duras
- **Sin red en el contenedor**: no se puede instalar fastapi ni arrancar la app de verdad. Solo verificación estática

## 🕳️ HUECOS CONOCIDOS Y NO TAPADOS

- **139 de 153 alimentos NO tienen anotada la fuente.** Los valores parecen correctos (el chivato nombre/calcio da 0 casos), pero no son trazables
- **No existe ninguna prueba del RECÁLCULO.** `a1` prueba generar, `a3` edición, `b3` endpoints — pero nada comprueba que tras cambiar un ingrediente sigan estando los 5 pilares. **Por eso ese fallo puede volver indefinidamente**
- **Nadie comprueba el reparto por categorías** de los menús generados. Por eso el hígado al 1% pasó desapercibido tanto tiempo
- **No hay campo de carbohidratos** en los alimentos. No es un error, pero invalida cualquier prueba de coherencia energía↔macros
- Carcasa de conejo: 1800 mg calcio vs 650 de Segal. Sin resolver
- ~33 alimentos sin mapear a BEDCA

## 📌 TRAMPAS EN LAS QUE YA SE CAYÓ (metodología)

- **Citar una fuente de memoria en vez de abrirla.** Pasó con FEDIAF: se "corrigieron" valores correctos
- **Escribir una prueba mal y creerse el resultado.** Pasó el 2 ago: una prueba dijo "51 alimentos con error"; el error estaba en la prueba (no hay campo de carbohidratos)
- **Una regla de categoría con índice vacío se desactiva EN SILENCIO.** Si se poda el único hígado, la regla "hígado ≥ X%" deja de aplicarse
- **Un fallo silencioso es peor que un error visible.** El analizador decía "dieta perfecta" con 15 nutrientes faltando, porque la clave de etapa llegaba mal escrita
