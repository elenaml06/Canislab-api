# Lo que salió de dar veredicto a las 286 tablas que faltaban

**Escrito el 11 de septiembre de 2026.** Su hermano mayor es
`HALLAZGOS_SACN5_10SEP.md`, que trae los tres primeros hallazgos (la vitamina E
del perro sano, la energía del cachorro y la grasa del cachorro de raza grande).
Aquí están los **19 que aparecieron al leer las 286 tablas que seguían sin
veredicto**, y con ellos `sacn5_tablas.json` queda en **0 pendientes de 474**.

> **Por qué había 286 sin veredicto si el libro estaba leído entero.** Porque son
> dos preguntas distintas y solo una se puede comprobar. `LECTURA_SACN5_INTEGRA.md`
> decía verdad: los 70 capítulos, de la primera línea a la última. El inventario
> preguntaba otra cosa: **¿alguien ha escrito qué hace el motor con ESTA tabla?**
> Eso es lo que faltaba, y es lo que impide que «me lo he leído» tape un hueco.
> Elena lo dijo corto: «como que sacn cinco a medias? Me dijiste que ya estaba».

> **Ninguno de los 19 se aplica hoy**, y es a propósito: el método del 10 de
> septiembre es leer todo, apuntar todo y aplicar solo al final, con los números
> delante. Los que son decisión clínica los toma Elena.

---

## El resumen, antes del detalle

| | Tablas |
|---|---|
| Leídas y sin nada que aplicar | 206 |
| Felinas | 25 |
| Listados de productos o de fármacos | 13 |
| Con rastro en el repo que el inventario no veía | 22 |
| **Aplicada entera** (la 6-2 **es** `sacn5_fuentes_de_minerales.json`) | 1 |
| **Con hallazgo** | **19** |

Las 206 **no se apartaron por el título**: se abrió el cuerpo de cada una en el
`.txt` de su capítulo, y el motivo va por familias que dicen *por qué* no aplica.
El campo `veredicto_por` lo deja escrito tabla a tabla.

---

## 1 · El hueso, por dos sitios distintos

Los dos tocan la pregunta que quedó abierta el mismo día en `PENDIENTE_NUTRICION.md`.

**Tabla 33-3 — la química.** El hueso no tiene un Ca:P cualquiera: lo tiene fijo,
porque es hidroxiapatita. Literal: «Ca-P ratio 1.67:1 on a molar basis. Ratio is
2.15:1 on a weight basis». O sea que **2,15:1 en peso**, y el rango de FEDIAF para
la ración entera es 1,0-2,0. Una ración con mucho hueso empuja el Ca:P hacia
arriba por química, no por casualidad, y el techo de FEDIAF se come por arriba.

**Tabla 5-13 — la digestibilidad.** Es una tabla de alimentos **caninos**, y
compara «Beef and bone meal» con «Beef, fresh»: la digestibilidad ileal de la
proteína es **68,3 %** en el primero y **80,4 %** en el segundo. El motor cuenta
la proteína del hueso como si se digiriera igual que la de la carne, que es
exactamente la duda que dejó NRC 2006 cap.3 al excluir el hueso de sus factores
de Atwater. No la cierra —son harinas, no hueso carnoso crudo— pero es la primera
cifra canina que apunta en una dirección.

## 2 · La presa entera, que es el patrón natural y no estaba escrito

**Tabla 19-4**, composición del cuerpo entero de la rata: **5,7 kcal/g** de EM,
**calcio 1,15 %**, **fósforo 0,98 %** (un Ca:P de **1,17**), linoleico 9,1 %.
Es contra lo que se puede leer una ración BARF, y el repo no lo tenía.

## 3 · Las nueve vitaminas del grupo B del perro, con su nivel en sangre

**Tabla 6-5.** Da la asignación de AAFCO **y** la de NRC **para el perro**, el
nivel normal en sangre y la prueba con que se mide cada una. La colina de NRC son
**1.700 mg/kg MS**, que a 4,0 kcal/g son **425 mg/1000 kcal**: la misma cifra baja
que ya salió de NRC 2006 cap.8 y que los 36 menús del catálogo superan.
Y es lo que faltaba para poder **contestar** la pregunta de las formas químicas
del grupo B, que hoy vive en `DATOS_QUE_FALTAN.md` sin forma de comprobarse.

## 4 · Los aminoácidos, por dos caminos

**Tabla 5-16**, perfil ideal relativo a la lisina, columna de **perro**:
metionina+cistina 0,64 · triptófano 0,22 · treonina 0,67 · arginina 0,71 ·
leucina 1,00 · fenilalanina+tirosina 1,00. El motor exige cada aminoácido por
separado contra FEDIAF y **no mira el perfil**. Es la otra forma de la pregunta
del techo de lisina, que hoy es el único máximo no aplicado.

**Tabla 19-6**, mínimos de crecimiento del **cachorro** en % de materia seca:
proteína 17,5 · arginina 0,66 · histidina 0,25 · isoleucina 0,50 · leucina 0,82 ·
lisina 0,70. Comparable celda a celda con la Tabla III-3b de FEDIAF, y nadie lo
ha cruzado. **Tabla 19-5** pone al lado el contraste de mantenimiento.

## 5 · El sodio cardíaco, que puede estar cuatro veces alto

**Tabla 36-9** da la ingesta diaria de sodio de un perro de 15 kg que come
935 kcal, alimento por alimento. El cardíaco seco le da **159 mg/día**, que son
**170 mg/1000 kcal**. El motor aplica **739 mg/1000 kcal** en la cardiopatía B2,
que es **más de cuatro veces**. No es una contradicción automática —739 sale de
su propia tabla y el techo legal del Reglamento (UE) 2020/354 está en 738,6— pero
son dos cifras de la misma fuente que no se parecen, y hay que cruzarlas.

## 6 · El ratio omega-6:omega-3, que el repo decía que no tenía número

`REVISION_NUTRICIONISTA.md` lo pone entre las tres cosas que siguen sin estar, y
`PENDIENTE_PRODUCTO.md` dice que «al omega-6:omega-3 ya no le falta motor: le
falta el número». **Tabla 34-3** trae uno, publicado y canino: el alimento de
prueba de la artrosis va a **0,7** de omega-6:omega-3 frente a **22,8** del
control, con omega-3 totales al 3,48 % de materia seca. No es un requisito de
perro sano —es el alimento de un ensayo— pero es un número real de una fuente que
ya usamos, y la pregunta 40 se puede reformular con él delante.

## 7 · La taurina, que no está en ninguna de las 163 fichas

**Tabla 36-10**, en mg/kg de materia seca: músculo de vaca 1.200, de cordero
1.600, de pollo 1.100, bacalao 1.000, y **ratón entero 7.000**. La taurina es la
cifra que decide en la cardiomiopatía dilatada, y el catálogo no la tiene en
ninguna ficha. Va a `DATOS_QUE_FALTAN.md`.

## 8 · La fibra, otra vez, y ahora con una cifra canina

**Tabla 29-4** es la única cifra canina de fibra **con resultado medido**: en
perros diabéticos, subiendo la fibra insoluble baja la glucosa media en sangre y
la dosis de insulina. Cae justo dentro de la pregunta abierta de qué fibra mide
el catálogo (bruta contra dietética total).
Y **Tabla 5-8** añade el otro lado: la fuente de fibra **cambia la disponibilidad
del mineral**. Con pulpa de remolacha al 5 % de fibra dietética total, el zinc
disponible baja al **24 %** y el calcio al **44 %**. El motor no modela
disponibilidad: suma el nutriente de la ficha y ya.

## 9 · El perro de trabajo, que ya tenía un pendiente y ahora tiene dos cifras más

**Tabla 18-10**: subiendo la grasa de **12,8 a 33,1 %** de materia seca, el tiempo
de carrera pasa de **103,7 a 137,6 minutos**. Es la cara opuesta del techo de
grasa de NRC (82,5 g/1000 kcal), y las dos apuntan al mismo perro.
**Tabla 18-6** cuantifica el gasto: correr 1 km cuesta **1,77 kcal/kg** en un
perro de 5 kg y **0,76** en uno de 70. La ficha pregunta por escalones de
actividad y no por distancia.

## 10 · El adelgazamiento tiene una ventana, y el motor no la comprueba

**Tabla 27-13**: el RER tiene que quedar en el **70-80 % del DER** al peso óptimo,
o el **60-70 %** al peso obeso, para perder 1-2 % de peso a la semana. El motor
baja las kcal al peso objetivo —que es el método de la **Tabla 27-12**, y esa
elección ahora está escrita— pero no comprueba que el resultado caiga dentro de
esa ventana.

## 11 · Tres de referencia, que no cambian un menú pero cierran un hueco de dato

- **Tabla 8-1** mide lo que de verdad come un perro adulto con pienso seco frente
  a su mínimo: calcio **74 mg/kg/día** contra un mínimo de **25**, fósforo 54
  contra 19, vitamina D 11 UI contra 2,3. Es la medida de por qué existen los
  techos del libro para el perro sano.
- **Tabla 5-21** da la composición de ácidos grasos de los aceites: el de pescado
  **14,1 de EPA y 11,9 de DHA**, el de girasol 62,3 de linoleico, el de soja 7,3
  de linolénico. Es dato de contraste para las fichas de aceite del catálogo, que
  es donde vive `dato_dudoso`.
- **Tabla 58-2** explica por qué el tipo de grasa importa en la linfangiectasia:
  los triglicéridos de cadena media se hidrolizan más rápido y no necesitan
  quilomicrones. El motor aplica el techo de grasa sin distinguir el tipo.

---

## Lo que hay que hacer con esto

Ninguno es un cambio de código de hoy. Cuatro son **dato que falta** (taurina,
formas químicas del grupo B, energía del hueso crudo, qué fibra mide cada ficha)
y el resto son **preguntas para el nutricionista**. Los 19 están en
`sacn5_tablas.json` con `veredicto: leida_con_hallazgo`, y el BLOQUE 78 clava el
recuento en **22** —los 3 del día 10 más estos 19— exacto y por separado del de
pendientes: el número que baja al trabajar no puede tapar al que sube al
encontrar algo.
