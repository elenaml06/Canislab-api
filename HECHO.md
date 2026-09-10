# Lo ya hecho (sacado de PENDIENTE.md)

`PENDIENTE.md` empieza siendo lo primero que se lee en cualquier sesión
(`CLAUDE.md` lo pide así). Con los puntos ya resueltos mezclados entre los
pendientes de verdad, pesaba 81,8 KB y crecía con cada cosa que se
terminaba, no con lo que quedaba por hacer.

Este archivo no se lee solo: se abre cuando hace falta el detalle de algo
que ya se resolvió — por qué se decidió así, qué se midió, qué PR lo trajo.
Nada de esto es agenda; es historial. Se separó el 6 de septiembre.

## Hecho el 20 de agosto

- Sentry en el backend, con avisos por correo.
- Los cinco fallos del webhook de Stripe, que **no había funcionado nunca**.
- Verificación obligatoria contra los 30 requisitos en **todos** los
  caminos, incluido el cambio de etapa (`/menu/revalidar`).
- La escalera de relajación: del 23 % de fallos con alergias al 0 %, sin
  ceder en ningún límite.
- Tope de volumen y porciones que escalan con el tamaño del perro.
- Cobro de prueba completado de punta a punta y premium activado de verdad.

## Leyendo SACN5 entero: lo aplicado de los capítulos 1, 2 y 3 — 9 de septiembre de 2026

Encargo: leer los capítulos **enteros**, no las tablas. La primera tanda ya
demuestra por qué, porque el método de conversión vive en el capítulo 1 y las
cifras están en el 13, el 27, el 33, el 37 y el 40 — con las tablas solas la
conversión parece obvia y no lo es.

**Aplicado:**

- **La transición de dieta tiene fuente**, y figuraba como «criterio nuestro,
  declarado». Es literalmente el calendario **largo del perro** de la Tabla 1-1
  (75/25 los días 1-3, 50/50 los 4-6, 25/75 los 7-9, 100 % el día 10), que es
  exactamente lo que hace `transicion.py`. Y el largo es el que la fuente
  recomienda «for situations in which the food change is known to be
  significant», que es lo que es pasar de pienso a ración cruda.
- **«Esto es todo lo que come» pasa a ser lo primero de «Cómo darlo».** El cap.3
  cita el AAHA Compliance Study: «55% of pet owners who fed a therapeutic food
  also supplemented the recommended food with other foods or treats. The primary
  reason cited by clients was that **they didn't know not to**». Más de la mitad
  rompe la dieta calculada sin saberlo. Lo vigila `menu-dos-pestanas.spec.js`, y
  comprueba también que va **por encima** del aviso de congelación, porque el
  mismo capítulo mide que el dueño recuerda «as little as half» de lo que se le
  dice. Probado con el fallo puesto: quitando el título, se cae.
- **Las PREGUNTAS 2 y 3 se reducen con la Tabla 2-1**, «Guidelines for quality of
  evidence that can be used for veterinary clinical nutrition» (Roudebush et al.
  2004, adaptada del U.S. Preventive Services Task Force). Cuatro grados, y la
  usa el propio SACN5. La pregunta era «¿existe algo explícito?»: existe, y con
  ella cada una de las 74 cifras clínicas se puede etiquetar sin inventar nada.
  Nuestro techo de mercurio es grado 4 con las palabras de la propia tabla
  («studies conducted in other species»).

**Anotado y NO aplicado, porque mueve 68 cifras y hay que verificarlo tabla a
tabla**: la densidad de referencia para convertir desde «% de materia seca» es la
que declara la fuente, y para alimento **canino** SACN5 usa **3,5 kcal/g**, no
4,0. Lo dice el Box 1-2 y lo repite el cap.13 dentro de su propio párrafo. Las
cifras de FEDIAF y las del NRC sí van a 4,0 —comprobado en la propia tabla de
FEDIAF—, así que no es un error global: es un error solo en lo que viene de
SACN5. Detalle, ejemplos y el método trabajado del Caso 1-1, en el cuaderno de
lectura.

⚠️ **Y de paso corrige algo que estaba escrito y era falso**: que un techo
convertido desde % de materia seca queda «un 29 % más flojo» en una ración cruda
por ser más densa. No. El porcentaje sube o baja **con** la densidad del alimento
a propósito, para que la cantidad por caloría se mantenga; el Caso 1-1 lo resuelve
con números. La densidad de nuestra ración no entra en la conversión, y por eso la
conversión sí vale para comida cruda.

## El corte de cachorro joven pasa de 4 meses a las 14 semanas de FEDIAF — resuelto el 9 de septiembre de 2026

Estaba escrito en tres sitios como **diferencia declarada con FEDIAF, al lado
estricto**: FEDIAF corta *Early Growth* en las **14 semanas** y nosotras
cortábamos en los **4 meses**, unas 17. Tres semanas de más con los requisitos
de cachorro joven, que son los más altos —calcio 2500 contra 2000, fósforo 2250
contra 1750, proteína 62,5 contra 50—, así que el margen pedía más y no menos.

**Eso no lo convierte en defendible.** El umbral lo pone la fuente: FEDIAF 2025
titula las dos columnas de sus tablas de requisitos *«Early Growth (< 14
weeks)»* y *«Late Growth (≥ 14 weeks)»*. Un margen conservador inventado
existiendo el número de la fuente sigue siendo un número inventado, y encima
`PARA_EL_NUTRICIONISTA.md` §2 ya decía «<14 semanas» — o sea que el documento
que va a revisión describía una cosa y el código hacía otra.

**Cambiado donde se decide la etapa**, que es `canislab-web/src/der.js`: el
corte va ahora en **días** (`EARLY_GROWTH_DIAS = 98`) y no en meses, porque 14
semanas caen a mitad del cuarto mes y con meses enteros no se puede expresar.
`calcularEdad` pasa a devolver `totalDias`, calculado sobre el calendario y no
multiplicando meses por 30.

⚠️ **Y el respaldo va al lado estricto a propósito.** Si falta `totalDias` —una
ficha guardada antes de que el campo existiera—, comparar contra `undefined`
daría siempre false y mandaría a un cachorro de dos meses a *Late Growth*, que
pide **menos**. Se cae al corte viejo de 4 meses en su lugar: un fallo de datos
no puede bajar requisitos. Es la familia de fallos de `ficha-ida-y-vuelta`.

Lo vigila `tests/der-contrato.spec.js` con tres pruebas: que la constante sean
98 días, que el día 97 sea todavía cachorro joven y el 98 ya no (los dos lados
del corte, no solo uno), y el respaldo sin `totalDias`. Probado con el fallo
puesto: subiendo la constante a 120 se caen dos.

**No toca el otro «4 meses» del motor**, que es el de SACN5 —3 × RER hasta los
cuatro meses, 2 × RER después— en el respaldo del DER cuando no se conoce el
peso adulto. Ese sí es la cifra de su fuente.

## Las dos filas de raza del DER: la fuente dice EN VEZ DE, no suelo — resuelto el 9 de septiembre de 2026

Quedaba abierto desde el 8 de septiembre, cuando se adoptaron las dos cifras de
la Tabla VII-7 de FEDIAF (`Great Danes 200 (200-250)`, `Newfoundlands 105
(80-132)`): **¿esos 200 van en vez del nivel de actividad, o son el suelo sobre
el que se aplica?** Se anotó como interpretación nuestra porque la tabla no
cruza las filas de raza con los cinco niveles.

**Estaba contestado en la guía, y en dos sitios.** La frase que presenta la
tabla — *«examples of daily energy requirements of dogs at different activity
levels, for specific breeds and for obese prone adults»* — pone las tres clases
de fila en paralelo, en la misma columna y con el mismo coeficiente: una fila de
raza es alternativa a una de actividad, igual que `obese prone adults ≤ 90` lo
es y no un descuento sobre el 95 del sedentario. Y la sección **7.2.3.4 «Breed
& type»** dice de qué está hecha esa diferencia: *«Breed-specific needs probably
reflect differences in temperament, resulting in higher or lower activity, as
well as variation in stature or insulation capacity of skin and hair coat.»* La
diferencia de raza **ya contiene** la de actividad; sumarle un nivel encima
sería contarla dos veces.

**El motor ya lo hacía así**, en los dos repos. Lo que faltaba era la lectura
que lo respalda, y una guardia que separase las tres lecturas posibles: las
comprobaciones que había no lo hacían — «Gran Danés en normal = 200» lo cumplen
igual la lectura buena y la de «suelo», y el recorte al rango tapa la de
«sumar». El **BLOQUE 54, apartado 2-bis** fija siete casos, y el terranova es el
que las separa porque su rango abre a los dos lados. Probado con el fallo puesto
por los dos lados: con `max(105, base)` fallan 4 casos, con `200 + base` fallan
5.

**Lo único que sigue siendo nuestro** es dónde caer dentro del rango publicado,
porque FEDIAF da el rango y ninguna regla para colocarse. Se coloca por
actividad y se recorta al rango, así que ningún resultado sale de la fuente.
Para el gran danés «en vez de» y «suelo» acaban coincidiendo, porque 200 es a la
vez el centro y el extremo bajo de su rango.

Cerradas con esto `PREGUNTAS_ABIERTAS.md` **P-11** y **P-12** (esta última, el
escalón de crecimiento de 2,5 × RER, ya estaba aplicada desde el 8 y el
documento seguía describiendo el estado viejo). Y de paso, el contrato del DER
decía **85 casos** en nueve documentos y en tres ficheros de código cuando hace
tiempo que son **100**.

## El BCS 9 pasa del 40 % al 45 %, en las TRES copias — resuelto el 9 de septiembre de 2026

**Aplicado el mismo día en los dos repos.** La Tabla VII-2 del Anexo
7.1 de FEDIAF da la columna «% BW below or above BCS 5» del perro, y puesta al
lado de nuestra regla del 10 % por punto:

| BCS | FEDIAF | Rawku |
|---|---|---|
| 1 | −≥40 % | −40 ✓ |
| 2 | −30 a 40 % | −30 ✓ |
| 3 | −20 a 30 % | −20 ✓ |
| 4 | −10 a 15 % | −10 ✓ |
| 5 | 0 % | 0 ✓ |
| 6 | +10 a 15 % | +10 ✓ |
| 7 | +20 a 30 % | +20 ✓ |
| 8 | +30 a 45 % | +30 ✓ |
| **9** | **>45 %** | **+40 ✗** |

O sea que la recta del 10 % lineal **es el extremo bajo de cada rango de
FEDIAF** —el más conservador— en ocho puntos de nueve. En el noveno la escala
deja de ser lineal.

**Cambiado en la API**, en las dos copias que había aquí
(`verificar.peso_objetivo_desde_bcs` y `der.peso_ideal_desde_condicion`), y con
el BLOQUE 63 comparándolas para que no vuelvan a separarse.

**Y la tercera copia, en `canislab-web`**: no estaba en `src/der.js` sino en
`src/bcs.js`, en `pesoIdealDesdeBcs`, que es la única de ese repo y la que
**MANDA** — el DER que viaja en `der_objetivo` sale de ahí, no de `der.py`. Es
decir que el número que de verdad decide las kcal del día era justo el que
faltaba por cambiar. Un perro de 20 kg con BCS 9 tenía dos pesos objetivo según
quién lo calculara: 14,29 kg en el frontend y 13,79 en la API — medio kilo, y
hacia arriba, o sea más kcal para el perro que peor lo lleva.

Lo vigila `tests/bcs.spec.js`, con el test de la Tabla VII-2 fila a fila (el
mismo que el BLOQUE 63 de aquí) y con uno que falla si el 9 vuelve a la recta.
Comprobado con el fallo puesto: cuatro de los ocho tests se caen.

**Y hay un efecto que hay que decir**: el escalón «Obeso» de la pantalla del
dueño ES un BCS 9, así que este cambio mueve el peso objetivo de fichas ya
guardadas sin que nadie las toque. Se acepta porque el 40 % no tenía fuente y el
45 % la tiene, y porque va al lado seguro (menos kcal para un perro obeso). El
test que exigía que la escala nueva diera EXACTAMENTE lo mismo que la vieja se
ha partido en dos: sigue exigiéndolo en los escalones 0 a 3, y en el 4 exige el
número nuevo y que sea menor que el viejo.

**Lo que NO hace falta:** regenerar `der_casos.json`. Ninguno de sus 100 casos
usa `condicion_idx`, así que el contrato del DER no se mueve. Comprobado.

**Y una cosa más que se cerró de paso:** por debajo de BCS 5 la API **ya estima**
peso objetivo, hacia arriba y topado al +20 %. Antes `verificar.py` devolvía
`None` (apoyándose en AAHA, que no tiene esas filas) mientras `der.py` sí
estimaba: dos reglas del mismo repo que discrepaban justo ahí. FEDIAF tiene las
cuatro filas y su §7.1.1 dice que la energía se calcula sobre el peso óptimo sin
distinguir dirección.

---

## El peso ideal desde el BCS estaba calculado de dos formas — resuelto el 29 de agosto

**RESUELTO el 29 de agosto, y al revés de como se escribió el 28.**

El 28 se puso que había que RESTAR el exceso, apoyado en el ejemplo
trabajado de AAHA («labrador de 45 kg con BCS 8 → aproximadamente
32 kg»). Estaba mal, y el error era leer una frase sin abrir
la tabla que tiene al lado: **«30 % overweight» es un 30 % SOBRE EL
IDEAL**, así que se invierte dividiendo. Tres cosas lo cierran:

1. La **Tabla 1 de la propia guía** da un tercer método que no
   depende de cómo se lea «overweight» porque sale de la masa magra:
   `[peso × (100 − %grasa)] / 0,8`. Da ×0,7875 en BCS 8. Dividiendo
   sale ×0,7692 —un 2 % de diferencia—; restando, ×0,70, que se sale
   del propio rango del método desde BCS 7.
2. La **Global Pet Obesity Initiative (2019)**, respaldada por ECVCN,
   WSAVA y ACVIM, define obesidad como «30 % above ideal body
   weight». *Above ideal* no admite dos lecturas.
3. **El ejemplo de AAHA es el raro de su propio documento**: dos de
   sus tres métodos dan 34-35 kg para ese labrador. Es una errata.

Así que **`der.py` y `App.jsx` estaban bien desde el principio** y el
que estaba mal era `verificar.peso_objetivo_desde_bcs`, que ya
divide. las kcal de los casos del contrato **no se han movido**.

Y como no había ni una prueba que tocara esa función —por eso se
coló—, ahora está el **BLOQUE 37**, que ancla los cuatro puntos
contra el método de la grasa corporal y, sobre todo, **compara las
dos cuentas entre sí**: es lo que el contrato del DER no puede hacer.

## `EPA_DHA_total` ya suma las dos claves — hecho el 25 de agosto

Se resolvió con claves DERIVADAS en `valor_nutriente` — el mismo
mecanismo que el 28 de agosto sirvió para `metionina_cistina` y
`fenilalanina_tirosina`. Comprobado: epa 0,5 + dha 0,3 = 0,8.

El problema original: `EPA_DHA_total` se comprobaba solo contra el EPA,
sin sumarle el DHA. El requisito se llama EPA+DHA y en `verificar.MAPA`
apuntaba a la clave `epa` a secas, así que el DHA no contaba. Iba en la
dirección segura (se exigía más de lo que se pedía) y los menús lo
cumplían de sobra igual — medido, 145 mg/1000 kcal de EPA solo, contra un
mínimo de 110 — pero el nombre decía una cosa y el código comprobaba
otra. Se arregló dejando que un requisito apunte a la SUMA de dos claves.

## El tope de patología no se respeta — hecho el 24 de agosto

Lo que decía este punto (fósforo renal a 1426 con el tope en 1400) ya
estaba arreglado el 21 de agosto. Pero al ir a comprobarlo se midieron
**todos** los caminos que entregan un menú, no solo el de generar, y
aparecieron dos cosas peores:

**1. La grasa se pasaba SIEMPRE.** Pancreatitis: tope 25 % de las kcal,
salía 26 %. Diabetes: tope 35 %, salía 36 %. En los cuatro pesos probados.
Ese camino (`max_pct_kcal_grasa`) no había recibido el arreglo del 21:
comparaba contra las kcal PEDIDAS, y el menú puede salir hasta un 3 % por
debajo. Menos kcal con la misma grasa = más porcentaje.

**2. Editar un menú se saltaba los topes DEL TODO**, que es mucho peor:

| Patología | Tope | Salía |
|---|---|---|
| renal · fósforo | 1400 | **3084** (+120 %) |
| hepatopatía · cobre | 3.0 | **4.05** |
| pancreatitis · grasa | 25 % | **47 %** |

`_recalcular_con_motor` no le pasaba las patologías al motor — el mismo
fallo que ya tuvo esa misma función con el presupuesto semanal el 5 de
agosto. El menú se generaba respetando el tope y una sola edición lo
tiraba.

**Y la verificación no lo paraba**, que es lo que lo hacía invisible:
comprueba los 30 requisitos de FEDIAF, que son los de un perro SANO.
3084 mg de fósforo entra dentro del máximo de FEDIAF, así que el semáforo
salía VERDE.

Arreglado en tres capas: la grasa contra las kcal reales, las patologías
pasadas al editar, y **la puerta de verificación comprueba ahora también
los topes por patología** (`_tope_patologia_roto`), para que si mañana
otro camino se olvida de pasarlas, el menú no salga igualmente.

Vigilado en el **BLOQUE 13** de `pruebas_completas.py`: generar, patologías
combinadas, y editar. Medido después: 0 casos por encima del tope.

> Esto es distinto de la pregunta abierta de qué NÚMEROS poner (sigue en
> `PENDIENTE_DECISIONES.md`): aquella sigue pendiente de decisión; lo de
> aquí es que el tope, sea el que sea, se cumpla.

## Multi-perro: varios perros por cuenta, cesta, burbuja y sin cuenta — hechos entre el 21 y el 24 de agosto

Ocho piezas de la fase de multi-perro, todas terminadas y desplegadas.

### Varios perros por cuenta — hecho el 21 de agosto

En `canislab-web`. Selector de perros en los dos paneles laterales,
crear y borrar perro, y se recuerda con cuál estabas. Cambiar de
perro **remonta** la app entera a propósito: perfil, menús y kcal se
calculan una sola vez al montar, así que sin remontar se quedaban
mezclados los datos de los dos. Borrar un perro borra también sus
menús (la tabla `menus` no borra en cascada; si no, quedaban
huérfanos para siempre). 8 pruebas nuevas en
`tests/varios-perros.spec.js`.

De paso: pesar al perro desde *Evolución* decía «✅ Peso
actualizado» y **no lo guardaba nunca** — `usuario` no existía en
esa pantalla y reventaba justo antes del guardado. Corregido.

### Cesta de la compra, diferenciando de quién es cada cosa — hecha el 24 de agosto

En `canislab-web`. Sale al final de la
pestaña «El menú» (no en una pestaña nueva: la decisión era «el
menú, cómo darlo y ya está») y en la pantalla de varios perros.

Suma **la semana entera**: cada menú por SUS días. Con un perro no
existía ninguna lista; con varios existía pero sumaba **solo el
primer menú de cada uno** — si el segundo menú llevaba un alimento
distinto, ese alimento no salía en la compra y se iba a la tienda
sin él.

Va por zonas de tienda (carnicería / pescadería / frutería /
despensa), porque carne, hueso, víscera e hígado son cuatro
casillas del motor pero un solo mostrador. Y en cantidades de
comprar, no de báscula: «2,5 kg», no «2478 g».

El «de quién» solo aparece si hay más de un perro **y** el alimento
no es de todos: «solo Cairo» en catorce de quince líneas taparía
justo la que importa.

La lógica vive en `src/cesta.js`, fuera de App.jsx, porque la usan
dos pantallas y tener dos copias fue lo que dejó una a medias
mientras la otra ni existía. 21 pruebas en `tests/cesta.spec.js`.

**No lleva precios** a propósito: no se tienen, cambian por
tienda y semana, y una cifra inventada en una lista de la compra es
peor que ninguna cifra.

⚠️ **MOVIDA EL 24 DE AGOSTO, pedido expreso**: «no quiero que la
compra aparezca en el menú, tiene que estar solo en el menú lateral».
Quitada del menú de un perro y de la pantalla de varios; vive solo en
el panel, en los **dos** paneles (el ligero y el de dentro del menú —
se puso solo en el primero y desde la pantalla del menú, que es donde
más falta hace, no salía).

Al sacarla del menú apareció un fallo que antes no existía: leyendo
solo lo GUARDADO, se acaba de generar un menú, no se ha dado a guardar
y el panel enseña la compra del menú **anterior** — números
correctos, menú equivocado, nada en pantalla que lo delate. Ahora
manda lo que hay en pantalla y la pantalla dice de dónde salen los
números. Y se puede elegir **para cuántos días** (3, 1 semana, 2
semanas, 1 mes): los menús cubren una semana, así que el resto se
escala en proporción y se avisa cuando no es una semana.

### La burbuja de perro y el engranaje, en TODAS las pantallas — hecho el 24 de agosto

Caso real: «la burbuja de perfiles de
perro y configuración tiene que existir en todas las pantallas, y en
todas las pantallas del menú lateral no aparecen».

Cierto: las seis pantallas que abre el panel (Perfil, Evolución, Mis
menús, Analizar, Por qué Rawku) tienen su **propia cabecera**, seis
copias, y se quedaron sin ella. Entrabas en Evolución y ya no sabías
de qué perro estabas viendo la evolución ni podías cambiar sin volver
atrás. También faltaba en Evolución/Analizar abiertas desde el
perfil, que es otra llamada distinta a `VistaMenus`.

La prueba (`tests/burbuja-en-todas.spec.js`) **no mira que exista**:
la pantalla de debajo sigue en el DOM con la suya y Playwright la
encuentra igual — quitando la burbuja de las seis cabeceras, la
primera versión de la prueba seguía pasando. Mira que **funcione**:
la toca y exige que se abra la hoja de perros. Y una tercera prueba
exige que el panel no tenga ninguna entrada que la lista no cubra,
para que la séptima pantalla no se olvide.

### Menús parecidos entre perros de la misma casa — motor hecho el 21 de agosto

`POST /menu/varios-perros`, con `modo_conjunto`
`"parecidos"` o `"distintos"`. Manda el perro con menos margen (más
restricciones y, a igualdad, ración más pequeña) y los demás se
amoldan a él: al revés no cabe, forzar los 7 alimentos de un pastor
alemán en un chihuahua de 3 kg no entra en 137 g de ración. Devuelve
por perro qué alimentos comparte, cuáles cambian y cuántos cambios
son. Medido: dos adultos de 24,5 y 8,2 kg salen con **0 cambios**
(misma compra, distintas cantidades) en 1,1 s. **Ya está en la app**:
en el generador, con más de un perro, sale «¿Para quién?» con las
tres opciones, y la pantalla de resultados enseña qué lleva cada uno
que los demás no y la compra de un día sumando a todos. De momento
solo en modo automático.

**Prueba de esfuerzo (21 agosto)**: 40 hogares al azar (2-3 perros,
pesos de 2 a 45 kg, las 4 etapas, alergias y categorías excluidas),
**86 menús entregados y 86 verificados en verde** de cero contra los
30 requisitos de la etapa de cada perro. Ni uno en rojo ni en ámbar,
ningún hogar sin menú, ningún alérgeno ni categoría excluida colada.
Peor tiempo de un hogar: 4,2 s.

Encontró de paso un fallo grave que llevaba meses: **las alergias se
podían saltar forzando el alimento** — ver `Ya_probado.md`.

### Menús de varios perros: el recorrido COMPLETO — hecho el 21 de agosto

API #23, web #11. Ya no hay camino aparte: para varios
perros se pasa por las mismas pantallas. Qué come cada perro por
separado, automático y personalizar, cuántos menús con su rotación,
aviso de transición por perro, y «Ver y editar el menú de X» que
abre el editor de siempre.

### La pantalla del menú, en dos pestañas — hecho el 23 de agosto

Era un scroll larguísimo con el plan de
transición pegado a las tarjetas, la congelación perdida en medio de
la pila de avisos (y con una X que la escondía para siempre), y cómo
preparar cada alimento detrás del icono de cubiertos de su fila.
Ahora: **El menú** (qué le doy, con el lápiz de cada alimento) y
**Cómo darlo** (transición, congelación y preparación, todo junto).
No se quitó nada; el icono de cubiertos de cada fila sigue estando.
`tests/menu-dos-pestanas.spec.js`.

### Sacar los perros del menú lateral — hecho el 24 de agosto

En `claude/burbuja-de-perfil-y-engranaje`, junto con los ajustes de
cuenta, que iban en el mismo sitio.

**La burbuja** va en la cabecera de todas las pantallas: dice de qué
perro es lo que estás viendo, y al tocarla salen los perros de la
casa y «añadir otro». Antes había dos caminos y ninguno completo —
unas pastillas que solo aparecían en la ficha, y una fila plegada
dentro del panel. Desde «Mis menús», por ejemplo, no se podía
cambiar de perro sin abrir el panel; lo decía el comentario de una
de las pruebas, y ahora esa misma prueba comprueba lo contrario.

**El engranaje**, al lado, lleva a **Ajustes**, con las dos mitades:
los perros (editar ficha, ir a otro, añadir, borrar) y la cuenta
(correo, contraseña, cerrar sesión). Sin cuenta enseña «crear una
cuenta» en vez de «cerrar sesión».

El selector viejo del panel y las pastillas de la ficha se han
borrado: tener tres formas de hacer lo mismo era parte del lío.

Vigilado en `tests/ajustes.spec.js` y en `varios-perros.spec.js`,
con una prueba que falla si los perros vuelven al panel.

> Un rótulo por el camino: al meter la burbuja se quitó el «MENÚ
> SEMANAL» / «PERFIL» de la cabecera, y dos pruebas viejas lo
> cazaron. Tenían razón: ese rótulo dice en qué pantalla estás. Han
> vuelto, en su propia línea, y conviven con la burbuja.

### Poder usar la app sin cuenta — hecho el 23 de agosto

En `claude/menu-dos-pestanas-y-sin-cuenta`. La primera pantalla ofrece
«Probar sin crear cuenta»; a partir de ahí la app entera funciona
contra `localStorage` en vez de Supabase (`src/almacen.js`, que
decide por dónde van los datos y explica en su cabecera **cuándo se
da de alta el usuario** y por qué ahí).

La cuenta se ofrece cuando ya existe algo que perder — debajo del
primer menú, sin bloquear nada — y al crearla lo del navegador
**sube solo** (`migrarLocalACuenta`). Sin esa parte, registrarse
después de una semana de uso habría borrado esa semana en silencio.
Vigilado campo por campo en `tests/sin-cuenta.spec.js`.

Queda fuera a propósito: sin cuenta `esPremium` responde que **no**,
para que el día que el muro se encienda «sin cuenta» no sea un
agujero por el que colarse.

## La compra: elegir el menú, los días bien, y marcar lo que ya tienes — hecho el 25 de agosto

Pedido el 24 de agosto después de usarla; hecho el 25.

1. **Elegir qué menú ver.** Selector arriba de la lista: "Todos
   juntos" o "Menú N · X días".

2. **Los días.** Era un fallo de concepto, no de cuentas: la cesta
   salía de UNA SEMANA y todo se escalaba por dias/7, pero los menús
   de una semana no duran lo mismo (uno cubre 4 días y otro 3). En sus
   palabras: *«si cocinas para 1 semana uno de 3 días tienes para más
   de dos»*. Ahora son dos preguntas distintas según lo que se mire:
   todos juntos → **semanas** (multiplicar una semana por 2 es
   exacto); un menú solo → **tandas de ese menú**, y cada opción dice
   los días de comida que da ("2 tandas · 6 días"). Encima de la
   lista, en grande, los días que cubre lo que se está viendo.

3. **Casillas para marcar lo comprado**, la línea entera pulsable
   (un cuadradito de 12 px no se acierta de pie en una tienda), y un
   botón de empezar de cero que solo sale si hay algo marcado. Se
   guarda en el navegador a propósito, no en Supabase: es de este
   móvil y de esta compra.

PR #31 de canislab-web. 8 pruebas nuevas, comprobadas rompiéndolas.

## Cantidades no medibles — hecho el 24 de agosto

Medido sobre 51 menús (todos los tamaños, etapas,
patologías y exclusiones), el problema era **más pequeño de lo que
parecía y de dos tipos distintos**.

**A granel** — salía UNA cantidad por debajo de un gramo en ~300
alimentos medidos: 0,35 g de sal común. Arreglado en el motor con un
suelo de 1 g: si va a usar un alimento a granel, que use una
cantidad que quepa en una báscula, y si no le cuadra, que use otra
cosa. **No se redondea el resultado**: cambiar los gramos después de
resolver cambia los nutrientes, y toda la app se sostiene sobre que
las cifras cuadran de verdad.

El suelo va **solo en Extras**, y eso también se midió: carnes,
vísceras y verduras nunca bajaban de ~1,9 g, así que ponerles suelo
no arregla nada y sí cuesta — con el suelo en todo el catálogo,
`/menu/varios-perros` pasaba de ~7 s a ~11 s con el presupuesto en
24 s. En Render eso se puede llevar por delante un menú.

**En polvo** — 0,15 g de alga, 0,60 g de multivitamínico. A éstos
**no** se les puede poner suelo: sería obligar a dar de más de un
suplemento. Se arreglan con el peso del cacito de cada producto, que
es un DATO y está apuntado en `DATOS_QUE_FALTAN.md`.

⚠️ **CORREGIDO EL 24 DE AGOSTO — lo de arriba era falso al principio.**
Decía que «lo que sostiene la garantía es la restricción del motor, que
es estructural». No lo era: **la fila del suelo no se añadía nunca**.
Comparaba `categoria_de[n]` (la CLAVE del diccionario de candidatos)
con `"Extras"`, y los aceites, la sal y las semillas entran bajo la
clave `"Suplementos"`. Código muerto desde el primer día. Salió
porque el BLOQUE 14 falló 1 de cada 20 veces en el caso más apretado:
0,55 g de aceite de girasol.

Es la **segunda** vez en ese archivo: el límite de 2 suplementos cayó
en la misma trampa. Para la categoría de un alimento se usa
`alimentos[n]["categoria"]`, NUNCA `categoria_de[n]`.

Y de ahí sale el **BLOQUE 16**, que es lo que de verdad lo vigila:
`resolver()` apunta, por cada regla, cuántas filas puso y cuántos
coeficientes llevan, y el bloque exige que ninguna de las 16 reglas
duras valga cero. Contar filas no bastaba — el fallo del límite de
suplementos añade la fila **vacía**, y `0 <= 2` se cumple siempre.
Comprobado con tres sabotajes y los tres se cazan. Si se añade una
restricción a `resolver()`, hay que pasarla por `_fila(...)` y
apuntarla en el BLOQUE 16; si no, puede morir en silencio como
murieron estas dos.

## El umbral de calcio en cachorros de raza grande estaba en 25kg, FEDIAF dice 15kg — hecho el 7 de septiembre

`RAZA_GRANDE_O_GIGANTE_KG` valía 25 en `motor/motor_completo.py` (la
restricción del solver) y en `main.py`
(`_minimo_calcio_raza_grande_roto()`, el semáforo de verificación final).
La nota "b" de la Tabla III-3b de FEDIAF —leída directamente del PDF
oficial, no de una fuente secundaria— fija el umbral en **15 kg de peso
adulto esperado**, no 25. Cachorros de razas de 15-25 kg en crecimiento
tardío no estaban recibiendo el calcio reforzado que exige FEDIAF. La
cifra de calcio en sí (2500 mg) ya era correcta — solo el peso del corte
estaba mal, copiado de una fuente secundaria (un artículo de Vet Clinics
que cita FEDIAF) nunca contrastada contra el PDF.

Corregido en los dos sitios, que tienen que coincidir siempre por
definición (mismo criterio, misma fila de la tabla).

La corrección hace aflorar un caso límite real que antes no existía
(cachorro de raza grande sin hueso + 3 alergias, ~33% de fallo aislado):
se añadió un reintento por infactibilidad en `_resolver_menu_v2_interno`
(máx. 2 intentos extra), mismo criterio que ya usa `/menu/varios-perros`
("el motor lleva aleatoriedad a propósito, la misma petición sale casi
siempre a la segunda"). Reduce el fallo aislado a ~10-15%.

PR #82. `pruebas_completas.py` entero, TODO EN VERDE.

## Linoleico de "Grasa de pollo" y categoría de "Laringe de vacuno" — hecho el 7 de septiembre

Dos huecos que llevaban desde el 25 de agosto en `PENDIENTE_NUTRICION.md`:

- **Linoleico**: 0 → 19,5 g/100g. USDA FoodData Central FDC 173564 "Fat,
  chicken" (SR Legacy, NDB 4542) — su proteína (0) y grasa (99,8) ya
  coincidían exactas con esta ficha, así que es con altísima probabilidad
  la misma fuente que el resto de la fila. Importaba porque el linoleico
  tiene máximo en cachorros, y un hueco contado como cero no lo detectaría.
- **Laringe de vacuno**: categoría "Hueso carnoso" → "Extras". Bloqueada
  por tejido tiroideo desde el 6 de septiembre (`TIROIDES_EXCLUIR`), nunca
  puede aportar hueso a ningún menú, así que su categoría antigua solo
  servía para disparar dos avisos ya conocidos en `auditar_catalogo.py`
  ("hueso con poco calcio, ¿es cartílago?"). 0 referencias en
  `catalogo_menus.json` (comprobado), no afecta a los menús precalculados.

PR #82 (junto con lo del calcio). `auditar_catalogo.py` limpio de estos
dos avisos.

## Taurina y L-carnitina: dato en las 159 fichas, y suelo activado en `dcm_taurina_respondedora` — hecho el 7 de septiembre

**Parte 1 — el dato (PR #83).** Ninguna ficha del catálogo tenía taurina
ni L-carnitina. Se añadieron las dos claves (mg/100g) a las 159 fichas:
valor real donde hay fuente citable, `sin_dato` donde no — nunca un
número inventado. Fuente principal: Spitze, Wong, Rogers y Fascetti
(2003), *J. Anim. Physiol. Anim. Nutr.* 87:251-262, el estudio más
completo de taurina en ingredientes de dieta animal (carnes, vísceras,
pescados y vegetales, directo o por familia/tejido cercano según
confianza). L-carnitina tiene cobertura más limitada (agregados por
especie de la literatura general). Estadística: taurina 130/159 con
valor real, 29 `sin_dato`; L-carnitina 101/159, 58 `sin_dato`.

Mapeo por nombre revisado ficha a ficha con cuidado explícito de no
confundir familias por coincidencia de texto — comprobado que "Repollo"
no hereda nada de "Pollo": Spitze confirma taurina=0 en todos los
vegetales, y así queda su ficha.

Se corrigió de paso un falso positivo de "HUECOS" en `auditar_catalogo.py`
que las dos claves nuevas introducían en 27 verduras y frutas, mismo
criterio que ya existía para `purinas_fuente`: un cero con fuente escrita
no es un hueco.

**Parte 2 — la activación (mismo día).** La patología
`dcm_taurina_respondedora` ya existía desde la ronda SACN5 del 6-7 de
septiembre, pero solo como aviso: "la taurina no está entre los 41
nutrientes que este motor mide". Y el mecanismo de "suelos por patología"
(el espejo de los topes, para cuando una fuente pide un MÍNIMO más alto
que el de FEDIAF) también existía ya, usado por primera vez en `artrosis`
y `dermatosis_zinc`. Con el dato de la Parte 1 puesto, solo faltaba
conectar las dos piezas:

- `Taurina` y `L_carnitina`, dos filas nuevas en
  `requerimientos_v2_final.json`, mismo patrón que `Fibra`: las seis
  columnas a "-", no exigen ni limitan nada a un perro sano.
- Las dos claves añadidas a `verificar.MAPA`.
- `suelos_por_1000kcal` en `dcm_taurina_respondedora`: taurina ≥250,
  L-carnitina ≥50 mg/1000kcal, SACN5 5ª ed. cap.36 «Cardiovascular
  Disease», Tabla 36-4 (0,1% y 0,02% de materia seca a 4000kcal/kgMS).

Probado contra el solver (adulto 20kg): el menú que sale de verdad lleva
414 mg de taurina y 138 mg de L-carnitina por 1000kcal, muy por encima
del suelo, porque ya incluye corazón e hígado. Verificado también en
`_garantizar_verificado()` (regla 2 del `CLAUDE.md`: los topes/suelos por
patología no son solo del solver), no se quedó en aviso.

De paso, revisando `PENDIENTE_DECISIONES.md` y `PENDIENTE_NUTRICION.md`
contra el estado real del código (no de memoria) para esta sesión,
salieron cuatro cosas que ya estaban resueltas y seguían marcadas como
pendientes: las 4 fichas de aminoácidos sospechosas (pulmón de cordero,
calamar, pulpo, sepia — ya confirmadas reales contra USDA el 7 de
septiembre), el contraste de timo/testículos con USDA (testículos de
cordero ya no existe, timo ya cita FDC 170194 directo, y el acceso a la
API de USDA con `DEMO_KEY` sí funciona — la nota decía lo contrario), y
la lista de hígados que faltan por especie (pavo y pato ya existían,
solo faltaba corregir la lista). Se reformuló también con más precisión
la pregunta pendiente del máximo de lisina, tras leer la metodología
exacta de FEDIAF en el PDF (p.22, sección Lysine): no es un ratio con la
proteína, es un no-effect-level de lisina CRISTALINA suplementada
(Czarnecki et al. 1985) convertido a energía — la pregunta real para el
nutricionista es si eso generaliza a la lisina de una proteína entera.

`pruebas_completas.py` entero, TODO EN VERDE.

## Quitado un máximo de fósforo sin fuente que llevaba desde el primer PR del repo — hecho el 7 de septiembre

Comprobando la Tabla III-3b de FEDIAF entera (los 41 nutrientes) contra
la transcripción de `auditar_fediaf.py`, celda a celda, para cerrar de
verdad el pendiente de "repasar la transcripción" (no solo lecturas
puntuales de una nota concreta), apareció una fila que **no tenía nada
que ver con FEDIAF**: `MAXIMOS["Fósforo"] = {"Adulto": 4000}`, con el
mismo número en `requerimientos_v2_final.json`. Los dos coincidían entre
sí, así que la auditoría nunca lo vería — exactamente el riesgo que se
buscaba con esta revisión.

Investigado a fondo antes de tocar nada, no solo "no lo encontré":
- **FEDIAF** (Tabla III-3a y III-3b): ningún número. Solo la nota "h",
  informativa sobre biodisponibilidad, sin cifra.
- **NRC 2006**: *"There are insufficient data on which to base an SUL
  for P in dogs"* (no hay datos para fijar un límite superior seguro).
- **Dobenecker et al. 2021** (PLOS ONE, el estudio más específico sobre
  toxicidad de fósforo en perros adultos sanos, en `canislab-fuentes`):
  *"More work is needed... no-effect-levels can be defined"* — ni la
  fuente más centrada en el tema da un número.
- **AAFCO/SACN5 cap.6**: solo dan mínimo de fósforo, nunca máximo.

El número llevaba ahí desde el primer PR de historia del repo
(`ae7878b`), antes de que existiera la disciplina de "cada cifra lleva
fuente". Y no era teórico: recortaba de verdad el menú automático
estándar de un adulto de 20kg, que salía justo en el límite (4000,0)
antes de quitarlo.

Quitado: `maxAdulto` pasa a "-" en el JSON, "Fósforo" se mueve de
`MAXIMOS` a `SIN_MAXIMO` en `auditar_fediaf.py`. Comprobado después que
el fósforo real de un menú no se dispara al quitar el techo (sigue en
~3970 mg/1000kcal, porque lo limita lo que dan los alimentos de verdad,
no un número artificial). `auditar_fediaf.py`: 234 comprobaciones
cuadran (subió de 232), 0 discrepancias. `pruebas_completas.py` entero,
TODO EN VERDE.

De paso, la revisión completa de la tabla confirmó que **los otros 40
nutrientes coinciden exactamente** con el PDF — esta fue la única
discrepancia real en todo el documento.


## Siete cosas del modo veterinario, usándolo de verdad — hecho el 7 de septiembre

Encontradas por la usuaria entrando con la cuenta acreditada. Ninguna daba
error, ninguna salía en un log: todas se ven usando la app. Lo que las une es
que el modo veterinario se construyó encima de la app del tutor apagando
trozos, y donde no se apagó ninguno, al veterinario le habla la app del dueño.

1. **«Todavía no tienes ninguno» con treinta pacientes.** La puerta del
   veterinario se pintaba con `!yaTienePerroGuardado`, que no significa «no
   tiene pacientes» sino «ahora mismo no hay ningún perro montado» — y dar de
   alta a uno desmonta el perro a propósito. Ahora cuenta los pacientes
   guardados.
2. **Los pacientes colgaban de la burbuja de perros.** La hoja desplegable
   responde «¿de cuál de tus perros estás?», que con tres perros de una casa
   se contesta de un vistazo y con cincuenta pacientes es un muro. Ahora la
   burbuja es una miga de pan que lleva a una **pantalla de Pacientes** con
   buscador por nombre, tutor y raza — que es como trabajan Nutrimenta,
   VetMenu y MyVetDiet: la casa del profesional es el fichero, y un paciente
   es un sitio en el que entras y del que sales.
3. **«Mis menús» salía vacío.** Se pedía solo por `creado_por`, una columna
   creada el 28 de agosto que no rellenaba nadie hasta el 29: todo lo
   anterior valía NULL. Ahora se piden también por los perros que son sus
   pacientes y se juntan las dos vías.
4. **El menú de un paciente se leía como el de un tutor**, con el «Este menú
   TIENE que aprobarlo tu veterinario» incluido — dicho a quien lo va a
   firmar con su número de colegiado. Fuera, y en su sitio el tope que la
   patología le ha impuesto al motor. El semáforo dice lo mismo en registro
   clínico, y la cabecera lleva el caso entero (raza, peso objetivo, BCS,
   etapa, kcal, patologías) sin salir a buscarlo.
5. **Marcar una patología no decía nada.** Ahora `GET /patologias` sirve el
   tope, la fuente, el motivo y **el margen contra el mínimo de FEDIAF**, y
   dice también qué NO se puede levantar desde la app. Los números no se
   copian a la app a propósito: sería la tercera copia de la tabla. BLOQUE 44.
6. **«Analizar la dieta actual» fuera del panel profesional.** Es la
   herramienta del dueño. «Evolución y crecimiento» se queda: la curva de
   peso entre consultas es seguimiento del paciente.
7. **Los avisos de seguridad bajan al final en modo profesional.** El aviso
   está bien calculado; lo que estaba mal es dónde. A un tutor hay que
   pararle antes de que dé de comer algo; un veterinario formula primero y
   revisa las notas después, junto al menú que puede editar.

Y uno que salió al arreglarlos: apagando el modo estando en la lista de
Pacientes, `fase` se quedaba en una pantalla que en modo tutor ya no se
pinta, y la app se quedaba en blanco sin error.

Once pruebas nuevas en `tests/veterinario-pantallas.spec.js` (canislab-web) y
el BLOQUE 44 en la API. Todas comprobadas reintroduciendo el fallo.


## La fase 1 del modo veterinario, entera — hecho el 8 de septiembre

Las dos que quedaban de `VETERINARIOS.md` §6, pedidas seguidas.

### Elegir el peldaño de la escalera de relajación

Estaba escrito desde el 28 de agosto: «qué peldaño se usó, Y PODER
ELEGIRLO. Hoy se baja solo y se avisa; un profesional quiere decidir si
prefiere otro reparto antes que soltar la proporción de hueso».

Y en el formulador era peor de lo que parecía: **`autocompletar` no recorría
la escalera nunca**. Formulaba con las proporciones completas y, si no salía,
decía que no — o sea que un veterinario tenía MENOS margen que un tutor, al
que el motor sí le baja de peldaño solo. La pancreatitis de 25 kg, que es el
caso que motivó el último peldaño, no salía para él de ninguna manera.

`GET /relajacion` sirve los peldaños con su nombre y qué suelta cada uno,
leídos de `_escalera_de_relajacion` y no copiados. `/menu/v2` y
`/formular/autocompletar` aceptan `peldano`, y **con uno elegido no se baja
solo**: bajar sería cambiarle la decisión a quien la ha tomado. Cuando no
sale, se dice en qué peldaño no sale y cuántos quedan por debajo — «no se
puede» a secas no dice si queda algo que probar.

Un peldaño mueve las proporciones de BARF y cuántos suplementos caben, que es
criterio nuestro. Los 43 requisitos, el ratio Ca:P y los topes de seguridad y
de patología son idénticos en todos, y el BLOQUE 45 lo comprueba sobre el
menú del último peldaño.

### La pauta en papel, con el logo de la clínica

Es el final del trabajo, y hasta hoy no existía: se formulaba aquí y se
copiaban los gramos a mano en la plantilla de la clínica. En Nutrimenta,
VetMenu y MyVetDiet el informe con la marca de quien firma es el producto.

Tres decisiones que van escritas porque tienen precio:

- **Se imprime el DOCUMENTO firmado, no la pantalla.** La ficha del perro
  cambia, el catálogo cambia y el motor cambia; un papel firmado tiene que
  seguir diciendo lo mismo dentro de un año. Si la vista leyera el estado de
  la app, imprimiría hoy una cosa y en marzo otra, las dos con la misma firma
  debajo.
- **El PDF lo hace el navegador** (`window.print()` → «Guardar como PDF»).
  jsPDF o html2canvas serían 300 KB para hacer peor lo que el navegador ya
  hace bien, y además imprime de verdad en la impresora de la consulta.
- **El logo va como `data:` URI en `profiles`, no en Storage.** Un logo en
  Storage se puede borrar, y entonces una pauta firmada dejaría de poder
  imprimirse igual. Se redimensiona a 320 px de ancho antes de guardarlo
  (20-40 KB) y se rechaza lo que pase de 200 KB. El razonamiento entero está
  en `supabase/migracion-clinica.sql`.

Los datos de la clínica NO viajan dentro del documento firmado: el logo no es
parte de lo que se verificó, así que puede cambiar sin invalidar el sello.

Ocho pruebas nuevas en `tests/pauta-en-papel-y-peldanos.spec.js` y el BLOQUE
45 en la API, todas comprobadas reintroduciendo el fallo.

⚠️ **Falta ejecutar `supabase/migracion-clinica.sql`** en Supabase. Sin ella
todo lo demás funciona y el bloque de la clínica lo dice al guardar, en vez
de fingir que ha guardado.

## Vuelve Pets Purest, con una ficha que sí cuadra — hecho el 7 de septiembre

Pets Purest Aceite de Salmón había salido del catálogo el 27 de agosto
(BLOQUE30 de `pruebas_completas.py`) porque su EPA/DHA solo aparecía en
fichas de marketing del fabricante, replicadas por revendedores, sin
ningún análisis propio — y era el más denso de los cinco aceites, así que
el solver lo prefería por delante de opciones mejor documentadas.

La usuaria mandó la foto de la etiqueta física del bote que tiene en casa
("Pets Purest 100% Natural Pure Scottish Salmon Oil", 300ml), con
"Analytical Constituents" y "Nutritional Content" propios — no una ficha
de marketing de un revendedor, sino el dato real del producto. Con eso el
motivo original de la salida deja de aplicar, y por instrucción explícita
se añadió como dato real, no como `dato_dudoso`.

Ficha nueva, "Pets Purest Aceite de Salmón Escocés" (160ª del catálogo),
mismo patrón que los otros dos aceites de salmón: grasa/proteína/fibra de
la propia etiqueta (99 g grasa, no 99,5 — es lo que declara ESTA etiqueta),
EPA y DHA en el extremo bajo de los rangos declarados (7% y 10%, sobre
7-9% y 10-12%) para no sobreestimar, linoleico = omega-6 total (6,6%, ya
que en el omega-6 de un aceite de pescado el ácido linoleico sí domina de
verdad), linolénico en `sin_dato` en vez de estimado por resta (mismo
criterio que sus dos hermanos), vitamina E en `sin_dato` pese a que la
etiqueta menciona "0,5% tocoferoles" — en la lista de INGREDIENTES, no en
el análisis nutricional, mismo criterio ya aplicado a las otras dos
marcas. Sin dosis de fabricante: ni la etiqueta ni la web dan el volumen
de una pulsación en ml.

Actualizado con esto:
- `pruebas_completas.py` BLOQUE28a: la cuenta de aceites en categoría
  Omega-3 pasa de 3 a 4, con el mensaje de fallo explicando por qué.
- `pruebas_completas.py` BLOQUE30: quitada la entrada de Pets Purest del
  diccionario `_FUERA_30` (el propio bloque dice qué hacer en este caso:
  "si vuelve con una ficha que cuadre, quita esta comprobación"), con un
  comentario fechado explicando el porqué en su lugar.
- `main.py`: sello de `alimentos_v3_final.json` actualizado (160 fichas).

De paso, dos correcciones de texto en `patologias.json` que no cambian
ningún número: `raza_predispuesta_cobre` decía que el motor excluye el
hígado (u otros alimentos ricos en cobre) como prevención — comprobado en
el código que ese mecanismo no existe, así que el aviso mentía sobre lo
que hace la app. Corregido para decir la verdad (el menú es normal, sin
exclusión de hígado, y sugerir excluirlo a mano en Personalizar si el
veterinario lo quiere). Y `dcm_asociada_a_dieta`: el aviso no mencionaba
explícitamente el boniato/patata, que la propia fuente FDA cita "en menor
medida" junto a las legumbres — ampliado con el mismo argumento estructural
(nunca son la fuente calórica principal en una ración BARF).

`pruebas_completas.py` entero, TODO EN VERDE (aparte del hueco de tiempo ya
conocido del BLOQUE43 con un perro de juguete de 1,5 kg y 3 s de
presupuesto, que no es de esta ficha: el menú se calcula bien, lo que
falta a veces es el margen para verificarlo, y verificar cuesta 1,6 ms).

## De la ficha del paciente a formular, sin escalones — hecho el 8 de septiembre

Cambio en `canislab-web`. Encontrado ABRIENDO LA APP y mirando las
pantallas, no leyendo el código — que es la única forma de encontrar esto.

**Lo que se veía.** Al abrir un paciente, y otra vez al guardar su ficha,
salía la pantalla «Perfil» del TUTOR: el perro rosa, «Nala necesita 1211
kilocalorías al día», «pésalo cada 2-3 semanas y ajusta si lo ves más
delgado o más gordo» y «Borrar a Nala de mi cuenta». Una pantalla entera
que repite lo que el veterinario acaba de rellenar, para que su único botón
útil sea «Todo bien, ir al generador de menús →». Pedido expreso: «eso
debería estar ahí simplemente en esa pantalla, y que la siguiente pantalla
sea directamente ir al generador de menús».

**Y detrás había dos fallos que no dan error:**

1. **La ficha secuestraba la navegación.** Con ella abierta `paso` valía 1,
   y el render mira `paso` antes que `fase`: pulsar «Menús» o «Pacientes» en
   el panel cambiaba la fase de verdad y la pantalla no se movía. Botón
   muerto, sin aviso. Es el mismo fallo que ya está escrito en
   `navegarDesdeElPanel` («navegabas bien y no lo veías»), otra vez.
2. **La ficha llevaba el contador del asistente del dueño**: «/ 6» con seis
   rayitas apagadas, prometiendo cinco pantallas que no existen.

**La raíz de los tres es la misma**: en modo profesional `paso` no puede
decidir qué se pinta. La ficha clínica ES toda la fase `"onboarding"`, en
una pantalla, y cualquier otra fase manda. Los seis `if (paso === N)` del
asistente llevan ahora `!enModoProfesional` delante, para que un `paso`
heredado no vuelva a secuestrar nada.

**Lo que hubo que traerse antes de quitar esa pantalla**, porque vivía solo
ahí: las **kcal/día** (el número del que cuelga todo, ahora en la cabecera
de la ficha y moviéndose mientras se teclea el peso o el BCS) y el aviso de
que **la pauta guardada se le ha quedado corta**, que es lo único
clínicamente urgente que tenía.

Queda: `Pacientes → paciente → Ficha (todo, editable, con las kcal) →
[Guardar y formular la ración →] → Formulador`. El botón reutiliza
`irAlGeneradorDeMenus`, que es quien sabe guardar con la etapa — guardar por
otro camino dejaba al perro con la etapa vieja, y de la etapa salen los 43
requisitos.

Seis pruebas en `tests/vet-de-la-ficha-a-formular.spec.js`, cinco de ellas
comprobadas reintroduciendo el fallo (la sexta es la del tutor, que tiene
que seguir pasando y pasa). Y `ayudas.js` tiene ahora `esperarElPaciente`
aparte de `esperarLaFicha`: son dos pantallas de llegada distintas, y una
espera que aceptara cualquiera de las dos daría por buena justamente la
regresión que esto arregla.


## Al veterinario no le habla la app del dueño (segunda pasada) — hecho el 8 de septiembre

Cuatro cosas seguidas, después de mirar las capturas del recorrido.

### 1. Fuera los muros de tutor

> «Obviamente a un veterinario no le tiene que saltar ningún tipo de aviso de
> "necesitas una dieta pautada por tu veterinario". Eso es absurdo.»

Lo era, y **no era un problema de tono**: guardar la ficha de un paciente con
hepatopatía, shunt o cálculos urinarios le mandaba a la pantalla del dueño —
«Esto lo tiene que pautar tu veterinario»— al veterinario que lo estaba
pautando. Y el motor **ya le formula esas ocho** desde el 29 de agosto
(`formulable_por_profesional`, BLOQUE 39), así que la pantalla era más
restrictiva que el propio motor: el muro solo servía para mandarle a hacerlo
en una hoja de cálculo, donde no lo verifica nadie.

Los avisos de seguridad tampoco le saltan ya: bajan a **«Cómo darlo»**, que
es el texto que él corrige y que acaba impreso en la pauta. Los límites duros
siguen dentro del cálculo; lo que se enseña ahí es criterio por encima de
ellos.

### 2. Y en su lugar, qué es inamovible y qué decide él

> «Que le diga las recomendaciones, lo que puede tocar y lo que no. Lo
> inamovible y lo que puede tocar, y él tiene que tener visibilidad de todo
> eso.»

`QueCambiaLaPatologia` pasa de una frase corrida al final a **dos listas
enfrentadas** —«No se toca» / «Lo decides tú»— más un bloque de
**recomendación clínica** con el objetivo terapéutico de la literatura (que
suele estar por debajo de lo que el motor puede hacer, y ese tramo lo pauta
él), el `aviso_profesional` y las notas.

### 3. La lista de patologías, por aparato

> «Me parece un peñazo, es enorme. No me gusta que más de la mitad de la
> página sea una lista de patologías hacia abajo.»

Eran 27 casillas seguidas en medio de la ficha. Ahora son nueve cabeceras
plegadas (`APARATOS` en `App.jsx`) con un buscador encima; un aparato con
algo marcado se abre solo y lo cuenta, porque lo que el paciente **tiene** no
puede esconderse detrás de un clic. Los grupos se construyen a partir de
`PATOLOGIAS`, no se escriben aparte: una patología nueva cae en «Otras» en
vez de desaparecer de la pantalla en silencio.

«Hígado» pasó a llamarse **«Hepático y biliar»**: en esa misma ficha hay una
categoría de alimento llamada «Hígado», y dos botones iguales en la misma
pantalla se confunden — lo vio primero una prueba, pero le pasaría igual a
quien use un lector de pantalla.

### 4. La burbuja seguía siendo una mascota

> «En tus capturas puedo ver perfectamente que en el icono de arriba a la
> derecha sigue apareciendo Nala.»

Cierto. El 7 se le cambió a dónde lleva —a la lista de pacientes— y se quedó
con el mismo círculo con la inicial y el mismo nombre del perro que en la app
del dueño. Ahora es una miga de pan de verdad: **«‹ Pacientes»**. De quién es
la ficha lo dice la ficha, en su línea de caso.

### Y una que salió buscando: la app no mandaba el token

`_es_profesional_acreditado(token)` existe en la API desde el 29 de agosto, y
de él cuelga que se le formulen al veterinario las patologías que al tutor se
le bloquean y que reciba los avisos profesionales. **La app no mandaba el
token nunca**, así que la API veía siempre a un tutor: todo ese camino
existía, parecía hecho y no lo recorría nadie. Se manda ahora, y solo en modo
profesional. Se manda el TOKEN y no un `modo_profesional: true` porque un
booleano lo escribe cualquiera desde la consola del navegador.

### BLOQUE 50: perros de verdad, patologías mezcladas

> «Tienes que meterte bien y comprobar que haces pruebas con todo tipo de
> perfiles de perros con todo tipo de patologías mezclándolas entre sí.»

Cinco perfiles (3, 12, 30, 55 y 20 kg) × doce cruces de patologías elegidos
porque **aprietan nutrientes distintos y por eso pueden pelearse**: renal y
pancreatitis (fósforo *y* grasa), renal y cardiopatía (dos minerales),
pancreatitis e hiperlipidemia (grasa por arriba, fibra por abajo)… De cada
cruce se comprueba que si sale menú está verde, que **ningún tope queda roto
medido sobre las kcal reales**, que con dos patologías manda la más estricta
de cada nutriente, y que si no sale se dice por qué. 127 s, 60 combinaciones.

**Lo que encontró, y es una decisión de nutrición, no de código:**
`renal + pancreatitis` **no da menú en ninguno de los cinco tamaños**. Es
coherente —fósforo ≤ 1200 con el mínimo de FEDIAF en 1160, grasa ≤ 20 y
proteína ≤ 75 a la vez dejan una ventana que el catálogo no alcanza— pero el
mensaje que recibe el veterinario es el del tutor: «quita alguna restricción
y vuelve a probar». No puede: son las dos enfermedades que tiene el perro.
Queda apuntado en `PENDIENTE_NUTRICION.md`.

---

## 9 de septiembre de 2026 (noche) — FEDIAF leída ENTERA, y lo que faltaba aplicado

Elena, tras la tercera vez que una lectura «completa» dejó cosas fuera:

> «TODO SE LEE AL PIE DE LA LETRA Y SE VA APUNTANDO TODO PARA APLICAR LO
> NECESARIO.» · «todo lo que falta de fediaf aplicalo»

El inventario `fediaf_tablas.json` decía «aplicada» de tres secciones que
**nadie se había leído enteras**, y «pendiente» de otras cuatro. Se han leído
las siete y ha salido esto.

### Lo que se ha aplicado

**La histamina del pescado mal conservado** (§7.6.2.4), que no estaba en
ningún sitio del repo. FEDIAF la nombra literalmente: «pseudo-allergic
reactions caused by high histamine levels in **not well-preserved scombroid
fish (e.g. tuna)**», y lo hace en el apartado titulado «All individuals
susceptible if sufficient quantity eaten» — o sea que no depende de que el
perro tenga nada. Servimos pescado crudo y cuatro especies del catálogo
forman histamina: Atún y Caballa (Scombridae), Sardina (Clupeidae) y
Boquerón (Engraulidae), tres de las seis familias que nombra el Reglamento
(CE) 2073/2005. Va como aviso y no como tope porque la histamina la genera la
mala conservación, no el pez, y es **termorresistente**: no se va ni
congelando ni cocinando, así que limitar los gramos no arreglaría nada.

**La uva y la pasa**, que faltaban en la lista de prohibidos. Estaban los
Allium y el chocolate — las §§7.7.2 y 7.7.3 — y faltaba la §7.7.1 entera. Con
sus dosis: 2,8 g de pasas o 19,6 g de uva por kg de peso, «a large dog of
40 kg may need to eat only 120 g». Y el tóxico **sigue sin identificarse**
(«Analysis for a variety of substances has proved negative»), así que no hay
forma de acotarlo por análisis. La uva es una **fruta**, o sea la categoría
del catálogo por donde habría entrado sin que chirriara nada.

**Las dos cifras en sangre de la taurina del perro** (§7.3.3): >40 µmol/L en
plasma y >200 µmol/L en sangre entera. El aviso de miocardiopatía dilatada
mandaba a hacer una analítica **sin decir contra qué se lee**. Y con ellas,
que el **Terranova** sintetiza taurina más despacio (Backus 2006), que es un
riesgo de raza y no de dieta.

**La confirmación por reintroducción** (§7.6.4): «Ideally this should be
confirmed by a challenge (reintroduction of the suspected component)». Es la
mitad del diagnóstico que casi nadie hace, y sin ella se le quita de por vida
un alimento a un perro al que puede no hacerle nada.

**La Tabla VII-14 entera**, en `fediaf_conversiones_vitaminas.json`, y el
**BLOQUE 70** rehaciendo con ella las seis conversiones de UI que declaran
tres fichas del catálogo. Las seis salen bien; lo que no había era forma de
saberlo. Convertir la vitamina D con el factor de la A multiplica por doce el
aporte de un multivitamínico y el semáforo no dice nada.

**La ecuación de energía que de verdad nos toca** (§7.2.2.2 b). FEDIAF tiene
tres formas de calcular la ME y dedica un apartado a «products of vegetable
or animal origin, **in their natural state**, fresh or preserved, such as
meat, offal», que es exactamente este catálogo: `4 × %proteína + 9 × %grasa +
4 × %NFE`. Medido: la mediana del catálogo sale a **1,014 veces** esa
ecuación y 70 de 73 fichas animales caen dentro del ±10 %. Ya la seguía. Lo
que no había era comprobación — y las kcal son el **denominador de las 43
filas del semáforo**, así que un error ahí desplaza todas las
concentraciones y ninguna prueba lo ve, porque todas usan el mismo
denominador. **BLOQUE 71.** Los hígados que se pasan quedan explicados por el
tercer término (NFE, o sea glucógeno) que el catálogo no tiene como columna.

**La salvedad del extremo bajo del BCS** (§7.1.3 + Tabla VII-3): «scores at
the lower end of the BCS are **confounded by muscle atrophy**». El BCS 9 ya
llevaba la suya («la escala se satura») y faltaba la otra mitad. Ahora las dos
salen de la misma función, `salvedadDelBcs()`, porque escritas a mano en las
dos pantallas que pintan el peso objetivo acabarían diciendo cosas distintas.

### Lo que NO se ha aplicado, y por qué

**El invierno** (§7.2.3.5): «When kept outside in winter, dogs may need **10
to 90 % more calories**». Es un hueco real —la ficha no pregunta dónde vive
el perro— pero no hay *una* cifra, hay un rango de 1 a 9. Es decisión.
`PENDIENTE_PRODUCTO.md`.

**El suelo de 70 kcal/kg^0,75** de perros enjaulados: es su revisión de
literatura, no su recomendación. La Tabla VII-7 dice 95 y es la que manda.

**La termogénesis de la comida**: da el total («about 10 %») y no cuánto sube
con la proteína ni con el número de tomas. Aplicarlo sería inventarse dos
cifras.

**La forma química de las vitaminas B**: es dato, no código. Medido con el
peor factor de la Tabla VII-14, el **ácido pantoténico caería por debajo del
mínimo de FEDIAF con el menú en verde**, y la tiamina aguanta por un 2 %.
`DATOS_QUE_FALTAN.md`, etiqueta por etiqueta, y **no lo rellena el asistente**.

### Y una corrección de método, que es lo que más vale

Las tres condicionales nuevas de la §3.3.1 se habían escrito con su medida
**contra `catalogo_menus.json`**: «hoy 0 de 216 menús llevan clara de huevo».
Elena: *«pero no tiene que estar en base a los menus del catalogo, porque eso
puede cambiar..»*.

Tiene razón, y es exactamente el fallo que este repo lleva persiguiendo desde
agosto: una frase medida una vez se queda escrita en un fichero de datos, el
catálogo se regenera, la frase deja de ser verdad **y no la desmiente nadie**.
Así que la medida no se guarda: **se rehace**. El **BLOQUE 69** resuelve menús
de verdad en cada batería y falla cuando la conclusión que sostiene cada regla
se da la vuelta. En el JSON se queda solo lo que no depende de ningún menú: la
aritmética de las tablas.

### Un test que no podía fallar

En el BLOQUE 50, la comprobación de «con dos patologías manda la más
estricta» llamaba a `valor_nutriente(al[n], …)` — la ficha entera donde la
función espera el diccionario de nutrientes. Devolvía 0 para todo, así que la
comprobación **no podía fallar ni con el fallo puesto**. Arreglada, y
comprobados los otros ocho sitios que llaman a esa función: era el único.

---

## 9-10 de septiembre de 2026 (noche) — SACN5 leída ENTERA, los 70 capítulos

Elena, después de que yo anunciara una corrección de densidad y la desmintiera
dos comprobaciones después:

> «PRIMERO LEE TODO Y APUNTA TODO Y CUANDO YA TENGAS CLARO TODO LO QUE TIENES QUE
>  HACER CUANDO TERMINES LA LECTURA APLICAS PORQUE SI NO ESTAS APLICANDO COSAS
>  QUE LUEGO TIENES QUE CAMBIAR 10 VECES»

Así que esta vez: leer los 70 capítulos enteros —texto **y** tablas—, apuntar
todo sin tocar nada, y aplicar al final de una vez. El barrido contó **476
tablas** y **121 «Key nutritional factors»**, sin cortar la salida (la lección de
`VERIFICACION_FILA_A_FILA.md`).

### La corrección que motivó todo, resuelta al revés de lo que yo dije

Quedaba escrito que SACN5 declara **3,5 kcal/g** de materia seca y que por tanto
las 68 cifras de patología convertidas con 4,0 estaban un 14 % apretadas de más.
**Es falso.** De las 24 tablas de SACN5 que cita `patologias.json`, **una sola
declara densidad** —la 13-3— y dice «Concentrations presume an energy density of
**4.0 kcal/g**». El 3,5 del Box 1-2 es un ejemplo trabajado con un alimento
concreto; en el mismo párrafo del cap.13 el fósforo se deriva a 3,5 y el sodio
dice «this allowance is for foods with an energy density of **4 kcal/g**».

Y ahora está **probado y no supuesto**: las 88 cifras del motor se reproducen
desde las filas de sus tablas a 4,0 —fósforo 0,8 % MS → 2000, sodio 0,4 % →
1000—, 84 exactas y 4 con un ajuste declarado.

### Lo que se aplica

**Las 88 conversiones, como dato y no como prosa.** Cada cifra de
`patologias.json` lleva ahora un bloque `conversion` con el valor literal de la
fuente, su unidad, la densidad y la cita, y `auditar_conversiones.py` **rehace la
cuenta** (BLOQUE 72). Una cifra sin ese bloque falla igual. Existe porque el 8 de
septiembre una conversión se escribió ×25 en vez de ×2,5 y lo único que la cazó
fue que alguien la leyó.

**El suelo de DHA de crecimiento y reproducción: 0,05 g/1000 kcal.** Aparece con
la misma cifra en cuatro sitios (Tablas 15-5, 17-1 en sus dos columnas y 33-5,
más el texto de los caps. 15 y 33): «DHA needs to be at least 40 % of the total
DHA plus EPA, or 0,02 % DM». El motor pedía EPA+DHA ≥0,125 g y **no pedía
reparto**, así que un menú de cachorro podía cumplirlo entero con EPA y salir
verde. Medido antes de aplicarlo: 0 de 10 menús por debajo, el más justo a 1,47
veces el suelo, el DHA entre el 57 % y el 75 % del total. No aprieta nada hoy —
que es el motivo de ponerlo hoy. BLOQUE 73.

**El umbral de calcio del BLOQUE 69, corregido de 5625 a 3750.** Esa tarde escribí
«FEDIAF no da a partir de qué nivel de calcio empieza» y usé el 90 % del máximo,
que me inventé. La Tabla 32-1 de SACN5 lo publica: «Higher levels of zinc are
required in foods with **calcium >1,5 % DM**» = 3750 mg/1000 kcal, el 60 % del
máximo y no el 90 %. El factor sigue sin existir en ninguna fuente.

**La cifra del frío, que decíamos que no existía.** `der.py` y
`PENDIENTE_PRODUCTO.md` afirmaban que no hay una cifra sino un rango de 1 a 9.
Eso es verdad de FEDIAF y falso del conjunto: la **Tabla 5-3** la da por tipo de
pelo y salto de temperatura (pelo corto **+95 %**, pelo largo +59,5 %, Labrador
+25 %, Gran Danés +22 %). Lo que falta no es la cifra: es la pregunta en la ficha.

**`sacn5_fuentes_de_minerales.json`**, la hermana de la Tabla VII-14 para
minerales, con el % elemental de cada sal y —lo que la de vitaminas no tiene—
**dos ceros**: el óxido de hierro («not biologically available», se añade como
colorante y hace que el alimento *parezca* alto en hierro) y el óxido de cobre
(«essentially zero»; AAFCO pidió dejar de usarlo). Y el hígado de cerdo, que
también es cero — no nos afecta porque no hay ninguna ficha de cerdo, y los de
vaca, cordero y pavo la fuente los llama «highly available».

**Seis avisos** que la fuente da y la app no decía: el agua con menos de 150 ppm
de sodio en la insuficiencia cardíaca avanzada; la dosis terapéutica de
L-carnitina (2 g tres veces al día); el potasio con diuréticos; que el zinc oral
**no se da con la comida**; y cuándo empieza la dieta renal (estadio 2, o
creatinina >2 mg/dl).

### Lo que NO se aplica, y por qué

Las **nueve tablas de recomendación canina sin patología en el motor** quedan
leídas enteras y con sus números en `PENDIENTE_PRODUCTO.md`, para que la decisión
se tome con ellos delante. Dos de las nueve están **cerradas**: la 53-2 (vólvulo)
porque su único factor es el tamaño del bocado, que ya está en el aviso de
`riesgo_gdv`; y la 47-4 (periodontal) porque sus cifras de fósforo y sodio son
**exactamente** las del perro adulto sano, que ya se aplican a todos.

### Dos confirmaciones que valen tanto como un hallazgo

El suelo de proteína de la perra gestante (125 g/1000 kcal) se aplicó desde
FEDIAF («may be double»). SACN5 llega al mismo número por un experimento: «a food
that had about **50 % DM protein** … no problems with hypoglycemia or ketosis»
(Blaza 1989). 50 % de MS a 4,0 son exactamente 125. Y la vitamina E del perro de
trabajo (83,9) cuadra con la Tabla 18-9 leída entera: ≥500 UI/kg MS en las cuatro
columnas de actividad.

### Y dos guardias que dejaron de vigilar al cambiar lo que vigilaban

La batería los cazó a los dos, que es exactamente lo que tenían que hacer:

- **BLOQUE 58** comprobaba que las etapas de crecimiento no tuvieran *ningún*
  suelo condicional, como forma de asegurar que el de proteína de reproducción no
  se escapara. Funcionó mientras hubo un solo suelo; en cuanto entró el de DHA,
  CachorroJoven «ganó un suelo de reproducción» que no era de reproducción. Ahora
  mira **la proteína**, que es de lo que habla la frase de FEDIAF.
- **BLOQUE 65** ancla 25 cifras del documento de revisión contra el motor vivo, y
  una de ellas buscaba «el ajuste senior de **Thes 2014**». Al pasar el escalón
  de edad a la Tabla VII-6 de FEDIAF, el documento dejó de decir Thes y el ancla
  dejó de encontrar su frase — y el propio bloque lo dice: «o se reescribió la
  frase (y hay que actualizar el patrón aquí) o se borró el dato». Era lo
  primero. De paso se ancló también el ajuste **joven**, que no lo estaba y era
  el que había sido código muerto.

---

## 10 de septiembre de 2026 — Los avisos de patología llegan por fin a la pantalla, y dos de ellos mentían

Era el punto que encabezaba `PENDIENTE_PRODUCTO.md` con ⚠️, y esta misma noche
lo había hecho más grande yo: los `avisos_extra` eran ocho y pasaron a ser
**veinte** al aplicar FEDIAF y SACN5.

**Lo que pasaba.** La API manda `avisos_patologia` con **cada** menú desde el 29
de agosto — los monta `avisos_de_patologias` en el motor — y `respuestaApiAMenu`
recoge campo por campo lo que le interesa de la respuesta. Ese campo no estaba en
la lista, así que se perdían ahí mismo, **dos líneas por debajo del comentario
que cuenta que eso ya había pasado antes con `problemas_seguridad`**.

Y no son avisos de relleno. Dicen justo lo que el motor no puede hacer solo: que
a un perro con bromuro potásico hay que medirle el bromo en sangre **después** de
cambiarle la dieta —y el cambio de dieta lo hace esta app—, que el mitotano se
absorbe treinta veces mejor con comida que en ayunas, que el zinc oral **no** se
da con la comida, contra qué número se lee una analítica de taurina.

Ahora salen dentro del panel que ya aparece exactamente cuando hay patología, el
de «Este menú TIENE que aprobarlo tu veterinario». Van ahí y no en un panel
propio a propósito: un aviso más entre los avisos se lee, un panel más se cierra.

### Y al ir a pintarlos se vio que dos mentían

`cardiopatia_b2` le decía al dueño «Sodio bajado a una restricción moderada
(estadio B2, **900 mg/1000 kcal**)» y el motor aplica **739**. `cardiopatia_c`
decía **790** y aplica **625**. Los dos topes se bajaron el 8 de septiembre
—porque el rango clínico entero se salía del techo legal europeo— y los avisos se
quedaron con el número viejo.

Es la peor versión del fallo: no falta información, la que hay es **falsa**, y
además en la dirección que tranquiliza. Un veterinario que lea «bajado a 900»
cree que la dieta está menos restringida de lo que está. Llevaban dos días así, y
lo único que los habría encontrado era ir a leerlos — que es justo lo que nadie
hacía, porque no se pintaban.

### Y diez avisos llevaban contabilidad del repo dentro

Diez empezaban con «⚠️ AÑADIDO 9-sep-2026, DE LEER ENTERO EL CAP.25 DE SACN5…».
Eso es de `por_que` y de este fichero. El dueño de un perro con Cushing no
necesita saber qué día leímos el capítulo 69. Los 87 avisos están limpios.

**BLOQUE 74** vigila las dos cosas: que ningún aviso afirme «<nutriente> bajado a
N por 1000 kcal» con un número que el motor no aplica, y que ninguno lleve
fechas ni marcas de trabajo interno. Comprobado que falla con el fallo puesto:
devolviendo el 790 a la cardiopatía C, salta.

### Y la higiene de la casa, que la app no decía en ninguna parte

El mismo día, la otra mitad del capítulo 56 de SACN5: «Dogs consuming such foods
**shed bacterial pathogens at a much higher rate** than those consuming
conventionally cooked commercial foods» (Weese y Armstrong, 2006), con
*Salmonella*, *Campylobacter*, *Escherichia* y *Yersinia* cultivadas en comida
cruda casera y comercial.

Rawku decía cómo manipular el ALIMENTO —congelar una semana, dos el pescado, tres
días descongelado— y **nada** de la higiene de la casa. Son dos cosas distintas:
congelar bien protege al perro de los parásitos, y no impide que el perro excrete
salmonela y que la toque un niño de dos años.

Ahora hay un panel «Higiene en casa» pegado al de Congelación, en la pestaña
«Cómo darlo». Nombra además a los grupos sensibles —bebés, embarazadas, mayores,
defensas bajas— para que quien esté en esa situación se dé por aludido sin que la
app se lo tenga que preguntar. Preguntarlo de verdad sigue pendiente: es una
casilla en la ficha y cambia lo que hay que decir.

No es un argumento contra el crudo ni cambia ningún menú. Es información que la
fuente da y que quien elige alimentar así tiene derecho a tener.

### Y la radiografía, corrida por primera vez contra `main`

`radiografia.py` existe desde el 28 de agosto para contestar la pregunta que la
batería no contesta: no «¿este menú cumple?» sino «¿este menú se ha hecho con los
números del perro que pediste?». Se corre en `main` y en la rama y se comparan
los dos archivos. **No se había corrido en esta rama.**

De 301 líneas, cambian 128, y todas menos dos tienen un motivo que se puede decir
en voz alta:

- **`(máx 4000.0)`** aparece en el fósforo de todas las etapas de adulto: es el
  máximo de FEDIAF que se borró por error el 7 de septiembre y volvió el 8.
- **Metionina 1,16 → 1,276 y lisina 1,22 → 1,342**, y así los doce aminoácidos:
  es exactamente ×1,1, el factor de digestibilidad de la §3.2.1 de FEDIAF.
- **BCS 9: peso de referencia 21,429 → 20,69 kg** en un perro de 30: es el
  EXCESO_BCS_9 pasando del 40 % al 45 % que dice la Tabla VII-2.

Las dos que no: un perro en **BCS 4** pasa de no tener peso objetivo a tener
33,33 kg sobre 30 reales, o sea **un 8,2 % más de kcal**. Eso salió del cambio
del 9 de septiembre —derivar hacia arriba por debajo de 5— y **choca con la
§7.1.3 de FEDIAF**, que dice que el BCS ideal es el **rango 4-5**. Medido,
escrito con las dos citas y puesto como decisión en `PENDIENTE_DECISIONES.md`
§4: no se cambia sola porque toca la ración de todo perro marcado «delgado».

## 10 de septiembre de 2026 — Una patología puede pedir su propio ratio, y el primero que lo usa cambiaba menús de verdad

**El punto 1 de lo que pedía la revisión de Cris Carles**, hecho por el otro
extremo del que parecía.

`REVISION_NUTRICIONISTA.md` cerraba con una lista ordenada por lo que desbloquea,
y arriba del todo estaba el ratio omega-6:omega-3, con esta nota: «es el mismo
trabajo que arreglaría el `ratio_ca_p` de los urolitos de calcio, que también
está escrito y sin aplicar». Se ha hecho ese trabajo. El omega-6:omega-3 **sigue
sin aplicarse** —y no por falta de motor, ver abajo—, pero el Ca:P sí.

### Qué faltaba, exactamente

No era saber de ratios. El motor monta restricciones de ratio desde el principio:
el Ca:P de FEDIAF y el techo de 1,6 de la nota b para el cachorro de raza grande
son dos filas lineales dentro del MILP. Lo que no había era **la forma de que una
PATOLOGÍA pidiera el suyo**.

Así que cuando la tercera pasada del 8 de septiembre leyó enteras la Tabla 40-5
(oxalato cálcico) y la 41-6 (fosfato cálcico) y encontró en las dos la misma
frase —«maintain a normal Ca:P ratio (1.1:1 to 2:1)»—, la cifra se escribió con
su fuente y con `aplicado_por_el_solver: false`, que es lo correcto: un límite
que parece un límite y no hace nada es peor que no escribirlo.

### Y no era cosmético

Medido **antes** de aplicarlo, por la vía de la API y en el peldaño estricto, en
cinco perros adultos (3, 10, 20, 30 y 40 kg):

| Patología | Ca:P de los cinco menús |
|---|---|
| oxalato | 1,11 · 1,40 · 1,30 · **1,06** · 1,49 |
| urolitos de fosfato cálcico | 1,61 · 1,60 · 1,81 · 1,68 · 1,90 |

El perro de 30 kg con oxalato salía con **1,06** —por debajo del 1,1 que pide su
fuente— **y salía en verde**. El semáforo comprueba el Ca:P contra el rango de
FEDIAF, que en adulto es 1,0-2,0, y **los requisitos de FEDIAF son los de un
perro sano**. Es el agujero del renal con 3084 mg de fósforo otra vez, esta vez
dentro de un cociente.

Medido **después**: los diez menús siguen saliendo, verdes, y el más justo cae
clavado en **1,10** — o sea que la restricción está atada y activa, no de adorno.
El techo (2,0) coincide con el de FEDIAF en adulto, así que por arriba no cambia
nada hoy; se escribe igual porque es lo que dice la fuente y porque el límite de
FEDIAF puede moverse.

### Cómo está hecho

- **`patologias.json`**: bloque `ratios`, con `numerador`, `denominador`,
  `sentido` y su `conversion` como cualquier otra cifra. En `ratios` **solo va lo
  que se aplica**; lo escrito y no aplicado sigue en
  `limites_escritos_que_el_solver_no_aplica`, y `auditar_patologias.py` rechaza
  una celda que diga lo contrario.
- **`ratios_de_patologias()`** en `motor_completo.py`, y **el solver y
  `_tope_patologia_roto` la llaman a ella**, no cada uno a su manera. Es la
  lección del 8 de septiembre: cuando cada uno aplicaba los suelos por su cuenta,
  el motor construía menús enteros para que el filtro final los tirara.
- **Genérico a propósito**: admite cualquier par de nutrientes y se lee con
  `valor_nutriente`, así que una clave compuesta (`omega6_total`, `epa_dha`) entra
  igual el día que haga falta.
- **`GET /patologias`** sirve los ratios con el límite de FEDIAF del mismo par al
  lado, igual que hace con los topes: sin el número de enfrente, «1,1» no dice si
  aprieta o es un adorno. Aprieta un 10 %.
- **El diagnóstico de choques** los sabe nombrar y soltar. Un ratio no se dice
  como un tope —no va «por cada 1000 kcal» y su clave no es un nutriente—, así que
  tiene su propia frase; sin ella salía «exige como mucho 1,1 de
  calcio:fosforo:min por cada 1000 kcal», mal en las tres cosas.
- **BLOQUE 75**, y probado con el fallo puesto: se parte por la mitad el calcio de
  todo el catálogo y se exige que el filtro final lo cace. Desconectando el ratio
  del solver, el bloque se cae.

### Lo que esto NO decide

El **omega-6:omega-3 sigue sin aplicarse**, y ahora es más claro por qué: no
faltaba motor, falta el número. Las fuentes van de **<1:1** (artrosis, Tabla 34-2)
a **7:1** (renal, Tabla 37-9) —un factor siete entre dos enfermedades que un mismo
perro puede tener a la vez— y el NRC 2006 dice del ratio de totales que «is not
helpful». Es PREGUNTA 40 en `PARA_EL_NUTRICIONISTA.md` y la decide quien firma.

## 10 de septiembre de 2026 — Un pendiente llevaba dos días culpando a una función que no interviene

`PENDIENTE_NUTRICION.md` §14.4 decía, sobre el toy de 1,5 kg al que le cuesta
sacar menú desde que existe el techo de fósforo:

> *«`elegir_alimentos` sortea candidatos por categoría sin saber qué límites hay
> puestos»*

y de ahí salía un plan: **sesgar el sorteo hacia los huesos de mejor Ca:P**. Ese
plan habría sido trabajo tirado, porque arregla una función que no está en el
camino.

### Los dos hechos

1. **`elegir_alimentos` no lo llama nadie.** De todo `motor/modos.py` —190
   líneas— el motor importa **una sola cosa**: el diccionario `CUANTOS_MAX`
   (`motor_completo.py:531`). Ni `elegir_alimentos`, ni `cambiar`, ni `quitar`,
   ni `anadir`: los endpoints `/menu/cambiar`, `/menu/quitar` y `/menu/anadir`
   tienen su propia implementación en `main.py`, y la batería tampoco los usa.
   **No hay sorteo de candidatos**: `resolver()` recibe todos los accesibles de
   cada categoría y elige el MILP.
2. **Lo aleatorio va en el objetivo, y un objetivo no vuelve infactible nada.**
   El ruido son 0 a 0,4 sobre el coste de usar cada alimento, más la penalización
   del pescado la mitad de las veces. Cambia por dónde busca HiGHS, o sea cuánto
   TARDA.

### La medida que lo cierra

Mismo toy, mismas 30 semillas, subiendo el reloj:

| `time_limit` | Sin menú de 30 |
|---|---|
| 1 s | 11 |
| 5 s | 6 |
| **30 s** | **0** |

Con 30 segundos no falla ninguna, así que **las 30 son factibles**: lo que
faltaba era tiempo para encontrar la primera solución entera. Y no es una
solución ya encontrada que se tire —eso se arregló el 29 de agosto—: en un
segundo HiGHS no llega a tener ninguna.

### Y al dueño ya no le llega

Medido por la vía de la API, que es la que usa la app, 20 peticiones:

| Presupuesto | Sin menú | Peldaño |
|---|---|---|
| 24 s (lo normal) | **0 de 20** | los 20 estrictos |
| 3 s (Render lento) | **0 de 20** | 7 estrictos, 13 un peldaño abajo, **y lo dice** |

Lo arregló el reparto de tiempo del 8 de septiembre: `tiempo_de_un_intento()`
impide que una llamada se lleve más del 40 % del presupuesto, así que siempre
queda para bajar de peldaño, y con cuatro huecos de suplemento entra la cáscara
de huevo (Ca:P de 370:1) y el techo deja de apretar. **El diagnóstico correcto
llevaba desde ese día escrito en el docstring de esa función.** Lo que no se
actualizó fueron los tres sitios que contaban la versión vieja.

### Corregido en cuatro sitios, y por qué importa

`PENDIENTE_NUTRICION.md` §14.4, `DECISIONES.md` D-15, el comentario del BLOQUE 43
—que afirmaba «es un sorteo que de verdad no tiene solución»— y la tabla de
medidas de `HALLAZGOS_LECTURA_FUENTES.md`. Más una línea en `CLAUDE.md` diciendo
qué se usa de verdad de `modos.py`, porque **código muerto que parece vivo** es
exactamente lo que mandó a este punto a diagnosticar la función equivocada.

Queda una pregunta pequeña, de limpieza y no de nutrición: si se borra lo muerto
de `modos.py`. No se ha tocado: borrar código no es urgente y el mapa ya avisa.

## 10 de septiembre de 2026 — El perro pequeño con patología se quedaba sin menú por reintentar diez veces lo imposible

Encontrado tirando del hilo anterior: si el ruido del solver va en el
**objetivo**, y un objetivo no puede volver infactible un problema factible,
entonces **reintentar un problema que HiGHS ha demostrado imposible no puede
salir bien nunca**. Y la API lo hacía.

### El caso

Chihuahua de 3 kg, DER 260, `renal`. Por la vía de la API: **21-24 segundos y
dieciséis llamadas al solver**, y a veces se acababa el presupuesto y contestaba
«El cálculo está tardando más de lo normal».

La escalera son seis peldaños. Medidos uno a uno con tres semillas cada uno:

| Peldaño | Estado de HiGHS | Tiempo |
|---|---|---|
| 0 a 4 | **status 2** (infactible **demostrado**), las tres semillas | 0,2 a 2,8 s |
| 5 | status 0, menú verde, las tres semillas | 1,9 a 2,2 s |

O sea que **la escalera entera cuesta 7,2 segundos**. Las otras diez llamadas
eran reintentos de peldaños ya demostrados imposibles.

### De dónde venía el bucle, y por qué tenía razón a medias

`_intentar_generacion` reintenta hasta dos veces cuando la primera llamada sale
infactible, y el motivo escrito es bueno: *«el motor lleva aleatoriedad a
propósito… la misma petición sale casi siempre a la segunda»*. Eso es **cierto
cuando se acabó el reloj** —status 1, HiGHS no llegó a encontrar la primera
solución entera, y otra semilla llega antes— y **falso cuando la infactibilidad
está demostrada**.

Quien llamaba no podía distinguirlos: `resolver()` devolvía `(False, None)` en
los dos casos.

### El arreglo

`resolver()` acepta `estado_del_solver`, un diccionario que rellena quien llama
—como `diagnostico`, pero **sin coste**: aquel cuenta filas y coeficientes en
cada `_fila()` y esto tiene que poder pedirse en cada llamada de producción—. Ahí
va el `status` de HiGHS y un `infactible_demostrado`. El bucle de reintentos lo
mira y para.

Se mira **solo el status 2**. Si el solver devolvió una solución que rechazó la
red de seguridad de las categorías (status 0 con `ok` falso), reintentar sigue
sirviendo, y se sigue reintentando.

### Lo que cambia, medido

| | Antes | Después |
|---|---|---|
| Chihuahua 3 kg + renal | 23,6 s · 16 llamadas | **9,3 s · 6 llamadas** |
| Peldaño y menú | el mismo | el mismo |
| Cruces sin menú (los 60 del BLOQUE 50) | 7 | **5** |

Los dos que pasan a dar menú son **chihuahua + renal** y **chihuahua +
renal+cardiopatía C**, que antes se quedaban sin menú *por falta de tiempo*, no
por falta de solución. Los cinco que siguen sin darlo son todos
`renal+pancreatitis`, que es infactible de verdad —comprobado a 60 s en el último
peldaño— y es una decisión de nutrición abierta.

Y esto importa más en producción que aquí: Render va 6-10 veces más lento y el
presupuesto son 24 segundos.

### El test

**BLOQUE 76**, probado con el fallo puesto (quitando la condición vuelve a hacer
16 llamadas y 9 repeticiones, y el bloque se cae). No cuenta llamadas totales a
propósito —eso dependería de lo rápido que vaya la máquina—: afirma la **regla**,
que es que no se repita un peldaño que ya salió demostrado imposible.

## 10 de septiembre de 2026 — Quién audita al auditor: la transcripción de FEDIAF ya se rehace sola

Estaba en `PENDIENTE.md` como *«Repasar la transcripción de la tabla de FEDIAF en
`auditar_fediaf.py`»*, y repasarla a ojo no habría servido: lo que hacía falta era
que no hubiera que repasarla.

### El hueco

La cadena que sostiene los 43 requisitos era:

```
PDF de FEDIAF  --(a mano, una vez)-->  auditar_fediaf.FEDIAF
               --(BLOQUE 18)-->        requerimientos_v2_final.json
```

El segundo tramo estaba vigilado desde el 25 de agosto. **El primero no**, y es
el que decide todo: con un valor mal transcrito, `auditar_fediaf` dice que el
JSON cuadra, la batería sale verde, y **todos los menús cumplen bien un requisito
equivocado**. El motor no tiene el PDF: no puede cazarlo por construcción.

Y no es hipotético. Esa transcripción **se había saltado los doce aminoácidos
enteros**, que estaban en la Tabla III-3b desde siempre entre «Protein» y «Fat»:
el motor decía cubrir «todo FEDIAF» con 29 de los 41 nutrientes que la tabla
pide. Lo encontró contar filas a mano el 26 de agosto, no una prueba.

### Lo que se ha hecho

`fediaf_tabla_III_3b.txt` es **la tabla tal cual sale del PDF** — sin tocar una
palabra, con su cabecera de página y su pie de notas —, y
`auditar_transcripcion_fediaf.py` la lee, saca sus filas y **rehace las 164
celdas** (41 nutrientes × 4 columnas de mínimo) contra la transcripción a mano.
Las 164 cuadran.

Es el mismo patrón que `auditar_conversiones.py` con las 92 cifras de patología y
que `leer_fuente.py` con las secciones de texto: **lo que no se puede rehacer no
se puede auditar**.

Detalles que costaron:

- El PDF escribe los miles con un espacio fino, así que «1 754» hay que pegarlo
  antes de partir por espacios o la vitamina A pasa a valer **1**.
- El calcio es la única fila partida en tres líneas, y no por capricho de
  maquetación: su celda de Late Growth tiene **dos** valores, 2.00ᵃ (raza
  pequeña) y 2.50ᵇ (raza grande, la nota b). El motor aplica el 2,00 genérico y
  el 2,50 reforzado va aparte, en `Calcio_LateGrowth_RazaGrande`.
- La transcripción se lee con `ast` en vez de importar el módulo, porque
  `auditar_fediaf.py` **revienta** si le falta una fila — y una fila que falta es
  justo uno de los fallos que esto tiene que poder contar en vez de morirse.

### Y ninguna fila se queda fuera sin decir por qué

Las cuatro que no se transcriben van declaradas una a una:

| Fila | Por qué no está |
|---|---|
| **Selenio (dietas secas)** | Rawku formula ración cruda, o sea húmeda. Y la húmeda es **más alta** en adulto (67,50 contra 55,00), así que además es el lado exigente |
| **Biotina (B7)** | FEDIAF no da cifra: las cuatro columnas son «-» |
| **Vitamina K** | Igual. FEDIAF la nombra en su §3.3 (más K con mucho pescado) y no la cuantifica para el perro: vive en `requisitos_condicionales.json` como `documentado_sin_cifra` |
| **Ratio Ca/P** | No es un nutriente de cuatro columnas: es un mínimo único (1/1) y cuatro máximos por etapa. Vive en el JSON como `Relacion_Ca_P` y lo vigila el BLOQUE 53 |

Sin esa lista, saltarse otros doce aminoácidos volvería a ser invisible.

### El test

**BLOQUE 77**, probado con el fallo puesto cuatro veces: un valor cambiado
(treonina 2,03 → 2,30), una unidad cambiada (valina g → mg), una fila borrada
(triptófano) y **el propio texto de la fuente editado**. Los cuatro se cazan. El
último importa tanto como los otros tres: si alguien retoca el `.txt` para que
cuadre, deja de ser una fuente y pasa a ser una tercera copia de la misma tabla.

## 10 de septiembre de 2026 — Los doce techos del libro también se rehacen ahora, en vez de creerse

Mismo hilo que lo anterior, un fichero más allá. `auditar_conversiones.py` nació
el 9 de septiembre porque las 88 cifras de `patologias.json` tenían su conversión
**contada en prosa** dentro de `por_que` — y una frase no se ejecuta: así se
escribió un ×25 en vez de un ×2,5, diez veces el valor bueno y con forma de dato
bueno.

`recomendaciones_libro.json` estaba exactamente igual y no lo miraba nadie.

### Qué son y por qué importan

Son la **tercera clase de límite** del motor: ni FEDIAF ni patología, sino lo que
el libro recomienda al perro que **no tiene nada**. Doce cifras, y todas salen de
un porcentaje de materia seca de una tabla de SACN5, con la cuenta escrita a mano
en la nota («%MS × 2500 = mg/1000 kcal»).

No son decorativas:

- El techo de calcio del **cachorro de raza grande** son 2750 mg/1000 kcal, un
  **39 % por debajo** del máximo de FEDIAF (4500 en crecimiento tardío). Sale de
  Fascetti cap.10, «no greater than 1.1% dm», *«in order to prevent
  panosteitis»*.
- El techo de **fósforo en crecimiento** (3250 en raza pequeña, 2750 en grande)
  es el **único que existe**: FEDIAF deja esas dos celdas de su tabla vacías.

Un error de conversión ahí no lo caza nada: el semáforo mira los requisitos de
FEDIAF y el menú sale verde igual.

### Lo hecho

Cada una de las doce lleva ya su bloque `conversion` —valor literal de la fuente,
unidad, densidad y cita con la tabla y la columna— y `auditar_conversiones.py`
**rehace la cuenta**. Las doce cuadran exactas (0,8 · 0,4 · 0,7 · 0,4 · 1,7 · 1,3
· 1,1 · 1,1 % de materia seca × 2500). El BLOQUE 72 lo ejecuta y además exige que
sus densidades sean las mismas 4,0 que las de patología.

Probado con el fallo puesto dos veces: cambiando el techo de fósforo del adulto a
2200 y borrando el bloque `conversion` del sodio del senior. Los dos se cazan.

## 10 de septiembre de 2026 — Y los requisitos condicionales, que son donde están las dos conversiones a la vez

Tercer y último fichero con cifras sacadas de una fuente.
`requisitos_condicionales.json` tenía cuatro números aplicados y ninguno decía,
como dato, de qué cifra de la fuente salía: la cuenta estaba en prosa dentro de
`por_que`, igual que estaban las 88 de patología antes del ×25 y los doce techos
del libro esta misma noche.

Y aquí importa más, porque **dos de los cuatro llevan las dos conversiones**: la
de densidad y la de unidad.

| Regla | Valor | De dónde sale |
|---|---|---|
| Vitamina E del perro de trabajo | 83,9 mg/1000 kcal | «≥500 IU vitamin E/kg food (DM)» (SACN5 Tabla 18-9) ÷ 4,0 kcal/g × **0,671 mg/UI** de tocoferol natural |
| DHA en crecimiento y reproducción | 0,05 g/1000 kcal | «0.02 % DM» (SACN5 caps. 15 y 33) ÷ 4,0 |
| Proteína de gestación y lactancia | 125 g/1000 kcal | 62,50 de la Tabla III-3b **×2**, por «and may be double» de FEDIAF §3.3.1 |
| Aminoácidos sin digestibilidad garantizada | ×1,1 | Factor de FEDIAF §3.2.1; adimensional, no hay unidad que cambiar |

El de la vitamina E es **literalmente el fallo del 8 de septiembre**: entonces se
escribió el suelo de vitamina E de la artrosis tratando las UI como si fueran mg
—100 en vez de 67,1— y lo que lo cazó no fue ninguna comprobación, fue que la
artrosis dejó de dar menú. Probado con el fallo puesto: quitando el factor de
unidad, el auditor dice que el motor aplica 83,9 y la fuente da 125.

Las tres reglas cuyo número no es un `valor` suelto —el ratio
linoleico:linolénico, que es un rango por etapa; las anclas de arginina, que son
una tabla entera de FEDIAF ya por 1000 kcal; y el umbral de calcio del zinc, que
está en una regla que el solver no aplica— van declaradas con su motivo, y el
auditor **falla si una declaración se queda caducada**: si la regla desaparece,
la excusa tampoco vale.

Con esto los tres ficheros de cifras del motor se rehacen en cada batería: **92
de patología · 12 del libro · 4 condicionales**.
