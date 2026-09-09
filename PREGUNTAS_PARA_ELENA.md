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
