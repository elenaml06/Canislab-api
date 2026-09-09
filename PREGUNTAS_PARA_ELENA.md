# Preguntas que han salido trabajando de noche

**Sesión del 8-9 de septiembre de 2026.** Cada una lleva lo que hace falta para
contestarla sin releer nada: qué se ha encontrado, qué se ha medido, y qué
pasaría con cada respuesta. Las que he podido decidir con la fuente en la mano
NO están aquí — están hechas.

---

## 1 · El techo de yodo: cuánto margen le dejamos a una tiroides

**Qué había.** `motor/seguridad.py` tenía el techo de yodo en **1.400 µg/1000
kcal**, con un comentario que decía «el NRC fija el límite superior seguro en
1.400».

**Qué dice de verdad el NRC.** Que a 1.400 µg/1000 kcal se vio **tiroides
deprimida y alteraciones óseas en cachorros** (Castillo 2001a), y que **no puede
fijar un límite superior seguro**. O sea que teníamos el techo puesto justo en la
dosis que hace daño.

**Qué he hecho.** Bajarlo a **1.275 µg/1000 kcal**, que es lo más alto que la
propia fuente documenta como comido sin problemas (piensos comerciales medidos
por Belshaw 1975, rango 400-1.275). No es una cifra mía: sale del NRC.

**Qué he medido antes de tocarlo.** Sobre los 216 menús precalculados: el peor va
a **1.038**, la mediana a **418**, y **ninguno** pasa de 1.275. O sea que el
cambio no quita ni un menú.

**Lo que te pregunto.** 1.275 está a un 9 % de la cifra que hizo daño, y esa cifra
es de **cachorros**, que son el grupo sensible; nuestro techo se aplica igual a
todos. Como el peor menú real va a 1.038, habría sitio para bajarlo bastante más
sin coste ninguno. ¿Lo dejamos en 1.275, o se lo pasas al nutricionista para que
diga un número con más margen? La referencia del propio NRC para perro adulto es
**220 µg/1000 kcal**, o sea que incluso 1.000 seguirían siendo casi cinco veces
la dosis recomendada.

---

## 2 · La metionina en hepatopatía: el NRC avisa de algo que no tenemos

**Lo que dice el NRC, literal:** *«Oral administration of about 1 g
methionine·kg BW⁻¹ every 4 hours for 24 hours caused **no acute clinical signs in
normal dogs** but caused **severe clinical signs similar to hepatic coma in dogs
with portacaval shunts**»* (Merino 1975).

**Qué tenemos.** `patologias.json` no tiene **ningún** tope de metionina en
hepatopatía. Tiene el del cobre, que es el clásico, pero no este.

**Por qué no lo he aplicado yo.** Porque la cifra del NRC es una **dosis por kilo
de peso administrada cada cuatro horas**, no una concentración de dieta.
Convertirla a µg/1000 kcal sería inventarme el número, que es exactamente lo que
`CERRADO.md` prohíbe. Y además nuestra «hepatopatía» es genérica: un shunt
portosistémico no es lo mismo que una hepatitis.

**Lo que hace falta.** Que el nutricionista (o un internista) diga si en
hepatopatía hay que topar la metionina, y con qué cifra y sobre qué base. Si la
respuesta es que sí, el motor puede aplicarlo: la clave `metionina` ya está en
las 163 fichas del catálogo desde el 28 de agosto.

---

## 3 · La fibra y el hierro en las cuatro patologías con suelo de fibra

**Lo que dice el NRC:** con pectina o psyllium en el intestino, la captación de
hierro baja de 71,9 a 28,5 µg/h — **menos de la mitad**. Es la misma advertencia
de la nota g de FEDIAF, pero con número.

**A quién le toca.** Tenemos suelos de fibra en cuatro patologías:
hiperlipidemia ≥25, obesidad ≥30, intestino irritable ≥20, estreñimiento ≥17,5
(g/1000 kcal). En esos cuatro menús el hierro de la ficha se absorbe peor de lo
que dice el número.

**Por qué no lo arreglo yo.** El efecto depende del **tipo** de fibra, y el
catálogo tiene un solo campo `fibra` sin distinguir soluble de insoluble. No hay
factor que aplicar sin inventármelo.

**Lo que te pregunto.** ¿Merece la pena que el menú avise («este menú lleva mucha
fibra; el hierro se absorbe peor») o que en esas cuatro patologías el suelo de
hierro suba un porcentaje que diga el nutricionista? Es una pregunta suya, no mía.

---

## 4 · La vitamina A: la mitad de los menús no llegan al mínimo sin contar caroteno

**Es la más importante de las cuatro.** Y no la buscaba: salió leyendo el
capítulo de vitaminas del NRC entero.

**El problema.** La vitamina A de una zanahoria y la de un hígado **no son el
mismo nutriente**. La del hígado es retinol; la de la zanahoria es β-caroteno,
que el cuerpo tiene que convertir. Hay un factor de conversión, y **el NRC dice
que para el perro no está definido**: *«a retinol equivalency has not been
defined»*. En humanos son 21 µg de caroteno por 1 de retinol. El convenio
europeo (BEDCA) usa 6 a 1. El americano (USDA/RAE), 12 a 1.

**Lo medido, sobre los 216 menús precalculados:**

```
% de la vitamina A que viene de verduras y frutas ..... mediana 83 %
menús que NO llegarían al mínimo de FEDIAF sin contar
el caroteno ........................................... 103 de 216
el peor (Grande_Lactante): declara 11.191 µg,
        de retinol de verdad ..........................        29
```

Veintinueve microgramos de retinol en el menú de una perra lactante, y sale
verde.

**Y las fichas mezclan convenios.** Contra USDA: la zanahoria es caroteno÷6, el
boniato es RAE, y la rúcula no es ni una cosa ni la otra. `UNIDADES.md` no decía
nada de esto (ya lo dice: lo he añadido con la medida).

**Lo que NO he tocado.** Ni un valor del catálogo: eso es dato, y los datos no
los relleno yo. Ni ningún factor de conversión: el NRC dice que no existe para el
perro, y ponerlo sería inventármelo.

**Lo que te pregunto, y hay tres decisiones distintas ahí dentro:**

1. **¿Qué convenio queremos?** Lo natural sería «retinol y caroteno separados»,
   como ya hacemos con `epa` y `dha`: dos campos en vez de uno. Eso es trabajo de
   datos (hay que ir a la fuente ficha por ficha) y va en `DATOS_QUE_FALTAN.md`.
2. **¿Qué factor le ponemos al caroteno para el perro?** Esto es pregunta para
   el nutricionista, no para mí, y no tiene respuesta buena en la literatura: el
   NRC dice que no está definida.
3. **Mientras tanto, ¿el menú debería DECIRLO?** Yo puedo hacer que la ficha
   verificada informe de cuánta de la vitamina A es retinol preformado, igual que
   ya informa de los huecos y de los `dato_dudoso`. Eso es información, no una
   decisión clínica, y lo haría sin problema si me dices que sí. Es lo único de
   los tres que se puede hacer esta semana.

**Lo tranquilizador, para que no cunda el pánico:** por arriba no hay problema.
El techo de vitamina A que aplicamos (30.000 µg/1000 kcal, FEDIAF) se aplica a
esa misma suma mezclada, o sea que aprieta **de más** — y el NRC dice que *«los
carotenoides tienen una toxicidad baja para el perro»*, así que la zanahoria no
puede dar hipervitaminosis A. El problema es solo el suelo.

---

## 5 · El ratio omega-6:omega-3 — que es justo lo que preguntó Cris, y las dos fuentes no dicen lo mismo

**Esta la contesta un clínico, no yo.** Y la traigo porque es literalmente el
punto de Cris.

**SACN5 lo pide, con números, en tres de nuestras patologías:**

| Patología | Lo que pide la tabla |
|---|---|
| Renal (Tabla 37-9) | omega-6:omega-3 de **1:1 a 7:1** |
| Artrosis (Tabla 34-2) | **< 1:1** |
| Cáncer (Tabla 30-5) | «as close to **1:1** as possible» |

**El NRC dice que ese ratio no sirve.** Literal, capítulo 5: *«The European
expert committee also specifically concluded that the use of a **total n-6:n-3
ratio is not helpful**»*, porque mezcla ácidos grasos de potencia muy distinta
(los de cadena larga son mucho más potentes que sus precursores de 18 carbonos).
Lo que el NRC recomienda en su lugar es el ratio **linoleico:linolénico**, que
**ya lo he aplicado** en todas las etapas (2,6-26 en adulto, 2,6-16 en gestación
y lactancia): eso sí es un requisito del perro sano y la fuente lo da como tal.

**Mi lectura, para que la contrastes con quien sepa:** no es que una de las dos
esté equivocada. El NRC habla de **requisitos de un perro sano**; SACN5 da un
**objetivo terapéutico** en un perro enfermo, donde lo que se busca es un efecto
antiinflamatorio y la literatura clínica lo escribe con el ratio total. Si eso
es así, la respuesta correcta sería aplicar los dos: el LA:ALA del NRC siempre
(hecho), y el ratio total de SACN5 **solo dentro de las patologías que lo
piden**.

**Lo que costaría, medido** sobre los 216 menús precalculados: el cociente
omega-6/omega-3 tiene mediana 4,68 y máximo 28,34, y **52 de los 216 pasan de
7**. O sea que aplicarlo en renal cambiaría uno de cada cuatro menús, y el <1:1
de artrosis es mucho más exigente todavía (habría que meter bastante pescado
azul o aceite de lino).

**Lo que he hecho mientras tanto:** dejarlo escrito en `patologias.json` dentro
de `limites_escritos_que_el_solver_no_aplica`, con la cita, la medida y el
motivo — el mismo sitio donde ya vivía el omega-3 del cáncer. Así está en el
repo, se puede auditar, y `GET /patologias` lo sirve al profesional para que lo
vea aunque el motor no lo aplique.

**Lo que sí he aplicado de la misma tabla renal**, porque ahí las fuentes no se
contradicen y son filas normales: el **cloruro ≤ 1.125 mg/1000 kcal** (la tabla
dice «1,5 × el sodio» y nuestro sodio renal son 750) y el **suelo de omega-3
totales de 1,0 g/1000 kcal**. Probado: cuatro perros renales de 5, 20, 25 y
40 kg salen verdes con las dos puestas.

---

## 6 · La vitamina E de la disfunción cognitiva: dos números del MISMO libro que no caben juntos

**Esto es una rectificación de algo que hice yo anoche, y prefiero contarlo
entero.**

**Qué hice el 8.** Leyendo la Tabla 35-3 de SACN5 (disfunción cognitiva) vi que
el motor no aplicaba nada de esa tabla teniendo tabla propia, y apliqué sus dos
factores con respaldo de ensayo clínico:

- vitamina E **≥ 187,5 mg/1000 kcal** («Provide foods with ≥750 mg/kg» de
  materia seca ÷ 4)
- omega-3 totales **≥ 2,5 g/1000 kcal**

Medí que resolvía —salía en el peldaño 5, con 189,4 mg, verde— y lo dejé puesto.

**Qué se me escapó.** Ese mismo día, en **otra pasada**, se puso el techo de
fósforo del perro adulto sano (2.000 mg/1000 kcal, también de SACN5,
`recomendaciones_adulto.json`). Cada cifra la medí por separado y cada una cabía.
**Juntas no.** Para llegar a 187,5 mg de vitamina E el motor tiene que cargar de
verdura y de hígado, y eso sube el fósforo por encima de 2.000.

**El resultado, medido hoy sobre el camino real de la API, todos los peldaños:**

```
disfunción cognitiva,  8 kg .... SIN MENU
disfunción cognitiva, 22 kg .... SIN MENU
disfunción cognitiva, 40 kg .... SIN MENU
```

Una patología marcada «formulable» que no formulaba nada, a ningún peso. **En
`main` sí daba menú.** O sea que mi cambio la dejó peor que como estaba.

**Dónde está el techo de verdad**, bisecando el suelo con el techo de fósforo
puesto (perro de 22 kg, DER 1.000):

```
vitE ≥ 120 ....... menú en el peldaño ESTRICTO   (real 125,5;  fósforo 1.998)
vitE ≥ 150 ....... menú en el peldaño 5          (real 156,9;  fósforo 1.998)
vitE ≥ 175 ....... menú en el peldaño 5          (real 177,7;  fósforo 1.998)
vitE ≥ 185 ....... SIN MENU EN NINGÚN PELDAÑO
vitE ≥ 187,5 ..... SIN MENU EN NINGÚN PELDAÑO   ← lo que pide la fuente
```

Este catálogo llega a **~180 mg/1000 kcal** sin pasarse de fósforo. La fuente
pide 187,5: **se queda fuera por un 5 %**. Y si se suelta el techo de fósforo, el
menú que sale lleva 4.000 mg de fósforo —el doble de la recomendación— y **403 g
de albahaca** para un perro de 22 kg. Eso no es un menú: es el solver
exprimiendo la columna de la vitamina E.

**Qué he hecho.** Mover la vitamina E a
`limites_escritos_que_el_solver_no_aplica`, con la cita, la medida y el motivo —
el mismo sitio y el mismo trato que ya tenía el omega-3 del cáncer, que no cabe
por lo mismo. Sigue en el repo, se puede auditar y `GET /patologias` se la sirve
al profesional. **El suelo de omega-3 (2,5) sí se sigue aplicando**, y resuelve
en el peldaño estricto: la patología no se queda sin nada.

**Lo que te pregunto, y son dos cosas distintas:**

1. **Cuando dos cifras del mismo libro chocan, ¿cuál manda?** Aquí chocan «la
   recomendación para cualquier adulto sano» (fósforo ≤2.000) y «la tabla de la
   enfermedad que tiene este perro» (vitamina E ≥187,5). Yo he preferido dejar
   el techo de fósforo, que es el protector y general, y aparcar el suelo, que
   es el agresivo y específico. Pero es una decisión clínica y no me
   corresponde. Si el criterio es el contrario, el cambio es de una línea.
2. **¿Puede estar mal la conversión, y no el número?** Los 187,5 salen del
   puente de siempre (%MS × 2,5, que supone 4.000 kcal EM/kg de materia seca).
   Una ración BARF es más densa. A **4.400 kcal/kg MS**, el MISMO «≥750 mg/kg
   MS» de la fuente son **170,5 mg/1000 kcal — y eso SÍ cabe** (medido: 175
   resuelve). Es exactamente la misma duda que ya está escrita para el omega-3
   del cáncer. Si el nutricionista dice que la densidad de referencia correcta
   para nuestras raciones es 4.400 y no 4.000, **varios límites de patología
   dejan de ser inalcanzables de golpe** y hay que recalcularlos todos. Es la
   pregunta que más cosas mueve de todo lo que llevo esta noche.

**Y lo que he añadido para que esto no se repita:** el **BLOQUE 61** de la
batería recorre las **39 patologías formulables** y exige que cada una dé menú
verde para el perro de referencia. Es la comprobación más tonta que faltaba —
*que lo que decimos que se puede formular se pueda formular*— y es la única que
caza este fallo, porque el semáforo no lo ve: no había menú que mirar.

---

## 7 · El omega-3 de la artrosis: el labrador se quedaba sin menú y el yorkshire no

**Misma noche, mismo tipo de fallo que el §6, y esta vez sin choque entre
fuentes: simplemente el catálogo no llega.**

**Qué apliqué el 8.** La Tabla 34-2 de SACN5 pide para artrosis **omega-3
totales ≥8,75 g/1000 kcal** (3,5 % de materia seca), y el **Reglamento (UE)
2020/354, entrada 27** pide ≥8,24 para la misma indicación. Dos fuentes
independientes, casi el mismo número, y el motor no pedía ninguna. Lo puse.

**Qué se me escapó.** Lo medí en un perro. Medido hoy en varios:

```
suelo 3,00 .... 20 kg OK | 30 kg OK | 55 kg OK
suelo 5,00 .... 20 kg OK | 30 kg OK | 55 kg OK
suelo 6,50 .... 20 kg OK | 30 kg OK | 55 kg OK   (los tres bordan el suelo: 6,60)
suelo 8,00 .... 20 kg OK | 30 kg SIN MENU | 55 kg OK
suelo 8,75 .... 20 kg OK | 25, 30, 40 y 55 kg SIN MENU     ← lo que pide la fuente
```

El techo fiable de este catálogo está en **~6,5** y la fuente pide **8,75**: se
queda fuera por un 26 %. Y lo peor no es que falle: es **cómo** falla. A 8,75 no
falla siempre ni nunca, **falla según el peso** — el labrador con artrosis, que
es el paciente más típico que vas a tener, se quedaba sin menú, y el yorkshire
no. Un fallo así en producción parece un error aleatorio de la app.

**Qué he hecho.** Lo mismo que con la vitamina E del §6 y que con el omega-3 del
cáncer: moverlo a `limites_escritos_que_el_solver_no_aplica`, con las dos citas y
la medida entera. **Los otros cinco límites de artrosis se siguen aplicando**:
EPA ≥1,0 (que es el de la misma tabla con respaldo de ensayo clínico),
L-carnitina ≥75, vitamina E ≥67,1, fósforo ≤1.750 y sodio ≤1.000. Quitando solo
ese suelo, artrosis vuelve a resolver en el peldaño **estricto** a 30 y a 55 kg.

**Y aquí la conversión NO salva el número**, a diferencia del §6: incluso a 4.400
kcal/kg MS el mismo «3,5 % MS» son 7,95 g/1000 kcal, que sigue por encima de lo
que cabe.

**Lo que te pregunto, y es una decisión de producto más que clínica:** el arreglo
de verdad no es tocar el límite, es **traer al catálogo una fuente concentrada de
EPA+DHA**. Hoy lo más concentrado que hay es el aceite de linaza (62,5 g/1000
kcal), y detrás la semilla de lino (40,2) y el aceite de hígado de bacalao
(22,3); los aceites de salmón van de 7,8 a 19,1 y la carne no aporta
prácticamente nada. Con un aceite de pescado concentrado en el catálogo, **este
límite y el del cáncer (12,5) dejarían de ser inalcanzables los dos a la vez**.
¿Quieres que busque cuál, con ficha y fuente, para que lo valides? Es trabajo de
datos, y los datos no los relleno yo — pero sí puedo traerte los candidatos con
su composición declarada y su fabricante.

**Y un añadido de después**, leyendo el capítulo 10 de Fascetti & Delaney
entero, que **respalda la decisión por un camino que no esperaba**. Fascetti
cuenta el experimento del que sale ese 3,5-4 % de SACN5, literal:

> *«In 36 dogs with elbow OA due to ED, a double-blind efficacy study was
> performed by feeding an increased omega-3 content (**omega-3 of 4%** and
> omega-6 of 20%) versus a high omega-6 content (omega-3 of 0.8% and omega-6 of
> 38%). The dogs that consumed the high concentrations of omega-3 fatty acids
> had significant increases in plasma LTB5 concentrations, **although lameness
> scored by ground reaction force analysis did not differ between the
> groups**»* (Hazewinkel et al. 1998).

El 4 % movió el marcador bioquímico y **no movió la cojera medida con placa de
fuerza**. Y la misma página trae el contraste con lo que sí aplicamos:

> *«A clinical trial including force-plate analysis performed in two groups of
> dogs fed either a control food or an **EPA-supplemented** diet for a 90-day
> period revealed that 31% of the controls and **82% of the EPA-supplemented
> group improved their weight bearing**»* (Schoenherr 2005).

O sea que de esa tabla, lo que tiene efecto clínico **medido** es el EPA —que el
motor exige y cumple— y no el omega-3 total. Eso no cambia **por qué** se retira
(no cabe), pero sí **cuánto se pierde** al retirarlo: bastante menos de lo que
parecía.

---

## 9 · La grasa de la pancreatitis: dos manuales, dos definiciones, y nuestra regla de fuentes no cubre este caso

**No he tocado nada.** Esto es para que lo decidas tú, porque el 8 de septiembre
ya se cambió una vez y volver a cambiarlo esta noche sin que lo sepas sería ir y
venir sobre el mismo número.

**Qué pasó el 8.** El tope de grasa en pancreatitis estaba en **20 g/1000 kcal**,
tomado del Merck Veterinary Manual. Se subió a **37,5** aplicando la regla de
fuentes del proyecto: manda FEDIAF; donde FEDIAF no llega, manda SACN5. FEDIAF no
cubre la pancreatitis, SACN5 sí (Tabla 67-3: «Fat ≤15 % DM»), y 15 % de materia
seca son 37,5 g/1000 kcal. Se hizo bien y está escrito.

**Qué he encontrado leyendo Fascetti & Delaney entero.** Que su capítulo 12
define «baja en grasa» de otra forma y con otro número:

> *«For most of the population eating commercial diets, **a diet that has less
> than 20% fat on an ME basis will be considered low fat**.»*

Las cuatro cifras, puestas en las mismas unidades para poder mirarlas juntas:

| Fuente | Lo que dice | g/1000 kcal | % de las kcal |
|---|---|---|---|
| **SACN5 Tabla 67-3** (lo que aplicamos) | «Fat ≤15 % MS» | **37,5** | ≈34 % |
| SACN5, si es obeso o hipertrigliceridémico (también aplicado) | «≤10 % MS» | 25,0 | ≈22 % |
| Merck (lo que había antes) | «less than 20 g fat/1,000 kcal» | 20,0 | ≈18 % |
| **Fascetti cap.12** | «low fat» = <20 % ME | ≈22 | <20 % |

**Fascetti y Merck coinciden casi exactamente**, y los dos son bastante más
estrictos que el 37,5 que aplicamos. Con la definición de Fascetti, **nuestro
menú de pancreatitis no cuenta como dieta baja en grasa**.

**Y para ser justa con la otra cara, que también está en el mismo capítulo:** hay
autores que recomiendan **no restringir** la grasa (34-51 % ME) si no hay
hiperlipidemia; un estudio de 10 perros sanos con 16 % vs 38 % ME no vio
diferencias en enzimas pancreáticas; y un retrospectivo de 34 perros con
pancreatitis aguda vio *una tendencia* a menos intolerancia con dieta baja en
grasa que **no llegó a ser significativa**. O sea que la literatura va de «da
igual» a «menos del 20 % de las kcal», y nosotros estamos en medio.

**Lo único que zanja algo** es la frase con la que el capítulo cierra el
apartado: *«**If energy needs can be met, the use of a low-fat diet has no
drawbacks and is recommended** until more information is available»*. El único
argumento en contra de bajar la grasa es que la dieta se vuelve poco densa y el
perro no llega a sus kcal — y **eso a nosotros no nos pasa**, porque el menú se
formula a medida y las kcal se cumplen siempre por construcción.

**Lo que te pregunto, y son dos cosas:**

1. **¿Bajamos el tope de pancreatitis a ~22 g/1000 kcal (20 % de las kcal)?**
   Si la respuesta es sí, lo mido primero: hay que ver si sale menú en el peldaño
   estricto a varios pesos antes de aplicarlo, que es la lección de esta misma
   noche. Yo no lo hago sin que me lo digas porque es criterio clínico.
2. **Y la pregunta de fondo, que vale para todo el motor:** nuestra regla de
   fuentes dice «manda FEDIAF; donde no llega, SACN5». **No dice qué hacer cuando
   dos manuales de referencia no coinciden** — y ya me ha pasado tres veces esta
   noche (el ratio omega-6:omega-3 del renal, el sodio del renal, y esto).
   Propuestas, para que elijas una y la escribamos en `CERRADO.md` de una vez:
   - **(a)** manda siempre SACN5, y lo demás se anota como contraste;
   - **(b)** manda la más estricta de las dos, salvo que deje sin menú;
   - **(c)** cuando discrepan, no se aplica ninguna y se escribe en
     `limites_escritos_que_el_solver_no_aplica` hasta que lo vea un clínico.
   Yo recomendaría **(b)** para los TECHOS (equivocarse por debajo de un techo no
   hace daño) y **(c)** para los SUELOS (un suelo que no cabe deja al perro sin
   menú, que es lo que ha pasado hoy dos veces).

---

## 8 · ⚠️ EL CALCIO DE LOS CACHORROS DE RAZA GRANDE — la más importante de todas, y está medida y lista

**Si solo lees una, que sea esta.** Es la única de la noche que toca a un perro
en el que equivocarse **no se arregla después**, y la respuesta se puede aplicar
en cinco minutos porque ya está medida.

### Lo que hacemos hoy

FEDIAF da para el crecimiento una ventana de calcio: mínimo 2.000 (2.500 en raza
grande tardía) y **máximo 4.500 mg/1000 kcal = 1,80 % de materia seca**. El motor
cumple los dos. Pero como una ración con hueso va sobrada de calcio, **el solver
se pega al techo**. Medido sobre los 12 menús de crecimiento del catálogo:

```
Grande_CachorroCrecimiento ....... 4.500 mg/1000 kcal = 1,80 % MS  ← EL TOPE EXACTO
Gigante_CachorroCrecimiento ...... 4.500                 1,80 %     ← EL TOPE EXACTO
Toy_CachorroCrecimiento .......... 4.500                 1,80 %
mediana de los 12 ................ 3.920                 1,57 %
11 de los 12 pasan de 1,1 % MS
```

### Lo que dice el capítulo de ortopedia de Fascetti & Delaney

Lo firma **Herman Hazewinkel**, que es el autor de casi todos los estudios de
calcio en cachorro que citan luego FEDIAF y SACN5. O sea que no es «otra fuente»:
es la fuente de las otras. Dice, dos veces:

> *«In order to prevent panosteitis, a diet designed for young dogs of large
> breeds with a **calcium content no greater than 1.1% dm** should be fed during
> the growth period, starting at partial weaning.»*
>
> *«In general… **the calcium content should be between 0.8% and 1.0% on a dry
> matter basis** (for a food with 4200 ME kcal/kg diet).»*

Y remata con una frase dirigida exactamente a lo que vendemos: *«The occurrence
of these dietary orthopedic diseases **is increasing since the feeding of BARF and
homemade diets has become more popular**.»*

La escala, para ver dónde estamos:

| Calcio (% MS) | Qué se vio en el estudio |
|---|---|
| 0,55 % (gran danés) | fracturas patológicas |
| **0,8-1,0 %** | **lo que recomienda la fuente** |
| 1,1 % | el control sano de todos esos estudios; el techo que da para prevenir panosteítis |
| **1,80 %** | **donde formulamos nosotros (= el máximo de FEDIAF)** |
| 3,3 % (gran danés) | osteocondrosis severa, radius curvus, wobbler |
| 3,3 % solo 3 semanas en el destete | panosteítis en **todos**, meses después, con la comida ya normalizada |

### Lo que he medido, que es lo que hace que esta pregunta se pueda contestar

Bajando el techo de calcio del crecimiento y pidiendo menú por el camino real de
la API, cuatro cachorros distintos:

```
techo 4.500 (1,80 % MS, hoy) ... los 4 salen, en el peldaño ESTRICTO, a 1,36-1,70 % MS
techo 2.750 (1,10 % MS) ........ LOS 4 SALEN, en el peldaño ESTRICTO, a 1,01-1,10 % MS
techo 2.500 (1,00 % MS) ........ 3 de 4 SIN MENU
techo 2.000 (0,80 % MS) ........ los 4 SIN MENU
```

(labrador de 15 kg a los 4 meses, gran danés de 25 kg a los 4 meses, mestizo de
6 kg a los 3 meses, yorkshire de 1,5 kg a los 4 meses.)

**El 1,1 % de Fascetti es exactamente lo más estricto que este catálogo aguanta**,
y aguanta sin bajar ni un peldaño. Un 0,1 % más abajo y se cae todo. Que la
recomendación de la fuente coincida al decimal con el límite de lo formulable es
la mejor señal de que el número es el bueno.

Y por qué 2.000 no puede ser, que también sale de la medida: a esas kcal **el
mínimo de calcio de FEDIAF para cachorro joven (2.500) queda POR ENCIMA del techo
(2.000)** — no es que no haya combinación, es que no puede haberla.

### Lo que te pregunto

**¿Bajamos el techo de calcio del crecimiento de 4.500 a 2.750 mg/1000 kcal
(1,80 % → 1,10 % de materia seca)?**

- **A favor**: es más estricto que FEDIAF, así que sigue siendo legal y correcto;
  la fuente es el autor de los estudios en los que se basan las demás; está
  medido y **no cuesta ni un menú ni un peldaño**; y el margen de error del
  calcio del hueso es mayor que el de los demás nutrientes del catálogo (la
  disponibilidad del calcio del hueso molido **no está medida en la literatura**,
  ver `PENDIENTE_NUTRICION.md`), lo que es un argumento más para no vivir pegados
  al techo.
- **En contra**: cambia **todos** los menús de cachorro del producto y obliga a
  regenerar los 12 menús de crecimiento del catálogo. Y no es lo que dice FEDIAF,
  que es nuestra fuente primaria.
- **Alternativa más pequeña**, si prefieres tocar poco: aplicarlo **solo a la raza
  grande**, que es donde la fuente lo dice literalmente y donde está el daño. El
  motor ya distingue esa fila (`Calcio_LateGrowth_RazaGrande`, la nota b de
  FEDIAF), así que es un cambio de una cifra.

**No lo he aplicado yo** porque cambia el producto entero para una población
concreta y eso es criterio clínico. Pero si me dices que sí, es una línea y una
regeneración del catálogo, y la batería lo comprueba.

---

## 10 · Cinco cifras más que las fuentes dan y el motor no aplica

Las junto aquí para que estén en un sitio. **Ninguna la he aplicado.** Cada una
lleva lo que costaría y en qué dirección se equivoca si nos quedamos como
estamos.

### 10.1 · La vitamina D del oxalato: la fuente da la mitad de nuestro techo

Fascetti cap.16: *«Diets with vitamin D between **250 and 350 IU/Mcal** should
suffice»* = **6,25-8,75 µg/1000 kcal**. Nuestro tope en `oxalato` es **14,1875**,
que es el máximo LEGAL de cualquier perro — o sea que hoy **no aplicamos ningún
tope específico de vitamina D para el oxalato**, aplicamos el de todo el mundo.
Es la única de las cuatro cifras del oxalato donde el cambio va en el lado seguro
(bajar un techo). Habría que medir si sale menú antes de aplicarlo.

### 10.2 · El fósforo del oxalato: la fuente dice que NO se restrinja

Fascetti cap.16, literal: *«**Dietary phosphorus should not be restricted with
calcium oxalate urolithiasis. Low dietary phosphorus is a risk factor** for
calcium oxalate urolith formation in cats and dogs»*, y recomienda **1,5-2,0
g/Mcal**. Nuestro tope es **1.500 mg/1000 kcal**, o sea que aplicamos como
**máximo** lo que la fuente da como **mínimo** aconsejable. SACN5 dice otra cosa.
Aquí equivocarse por abajo **no es el lado seguro**, porque el fósforo bajo es
factor de riesgo de la propia enfermedad. Subir un techo es aflojar, y eso no lo
hago yo.

### 10.3 · El sodio del oxalato: el debate está abierto y bajo puede ser peor

Misma fuente: *«the **low** dietary sodium concentrations… **increase** the risk…
diets that contain **high** dietary sodium concentrations **decrease** the
risk»*, y *«recommended concentrations… **is debated**, as diets containing as low
as 0,4 g/Mcal and as high as 3,5 g/Mcal are available commercially»*. Nuestro tope
son 0,75 g/Mcal. Lo dejo como está y lo dejo escrito.

### 10.4 · El zinc y el linoleico de la piel: la dosis con ensayo es 4× la nuestra

Fascetti cap.14, citando a NRC 2006: *«The combination of **zinc (100 mg/1000
kcal) and linoleic acid (15 g/1000 kcal)** produced statistically significant
improvements in coat gloss and decreased TEWL over a nine-week period in dogs»*.
Nuestro suelo de zinc en `dermatosis_zinc` es **25**. Y van juntas: *«EFA
deficiency impairs zinc absorption»*, así que subir el zinc sin el linoleico
puede no servir. El linoleico de 15 g/1000 kcal es **cinco veces** el mínimo de
FEDIAF y no sé si cabe: habría que medirlo.

### 10.5 · El ácido oxálico: hay cifra objetivo y no tenemos el dato

Fascetti cap.16: *«Suggested dietary concentration is **<20 mg oxalic acid/100 g
of food (dry matter basis) or about <40-45 mg oxalic acid/Mcal**»*. Nosotros
excluimos alimentos altos en oxálico **por una lista** (`OXALATO_ALTO`), no por
una cifra, porque el catálogo **no tiene columna de ácido oxálico**. Ahora esa
columna tiene un objetivo numérico. Va a `DATOS_QUE_FALTAN.md` — y los datos no
los relleno yo.
