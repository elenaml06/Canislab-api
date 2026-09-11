# Lectura de Ettinger, Feldman y Côté — *Tratado de Medicina Interna Veterinaria*, 8.ª ed.

**El método, y por qué este y no otro.** Se lee el capítulo entero, se apunta lo
que dice, y se decide qué sirve y qué no. Nada de filtros: un filtro decide de
antemano qué cuenta, y lo que cae fuera es invisible por definición. Medido el 11
de septiembre sobre Fascetti, que sí tiene contador: de sus 18.194 frases el
filtro se queda con 657, y de las 17.537 que tira **3.605 nombran algo
nutricional y 1.131 llevan además una cifra**. Casi el doble de las que se
miraron.

**Dónde está el libro.** `canislab-fuentes/Ettinger_Feldman/`, los dos tomos con
su texto extraído. 360 capítulos, del 1 al 360, sin un hueco. Está **en español**:
es la traducción de Grupo Asís (2021) de la 8.ª edición de Elsevier.

**⚠️ Y LA REGLA QUE COSTÓ DOS CORRECCIONES EL MISMO DÍA.** Al leer una fuente
nueva **no basta con comparar contra el motor**: hay que preguntarse **si alguna
de las otras ya decía algo de esto**. Sin eso, una discrepancia entre dos libros
del mismo nivel se apunta como si fuera un fallo nuestro. Pasó dos veces el 11 de
septiembre —con la energía del perro a dieta (SACN5 dice lo que hace el motor) y
con el exponente de la energía de mantenimiento (NRC usa el mismo 0,75 que
nosotras)— y las dos las cazó Elena, no yo. El sitio donde mirar primero es
`FEDIAF_CONTRA_OTRAS_FUENTES.md`.

**Por dónde se va.** Los capítulos **170 a 194** del tomo 1 son una sección
entera de nutrición, y es por donde se empieza. Después, los de patología que
deciden algo que el motor ya aplica.

---

## Cap. 170 — Evaluación nutricional (Kathryn E. Michel) · LEÍDO ENTERO

**Qué dice.** Cómo se valora el estado nutricional de un paciente: reseña,
condición corporal, historial dietético y seguimiento.

**Lo que sirve, y son tres cosas:**

**1. Confirma de dónde sale nuestro BCS de nueve puntos.** La figura 170.1 se
acredita al «conjunto de herramientas del Comité de Nutrición Global
proporcionado por cortesía de la Asociación Mundial de Veterinaria de Pequeños
Animales» y a Laflamme 1997. El motor lo atribuye a WSAVA y ahora esa
atribución se puede abrir dentro del repo.

**2. Segunda fuente independiente para el hueco de la masa muscular.** Dice, y
es una frase que vale la pena tener entera:

> «los sistemas de puntuación […] pueden clasificar de forma errónea a algunos
> pacientes desnutridos. […] el proceso de evaluación de la condición corporal
> debe incluir no solo la evaluación básica de la silueta corporal y del tejido
> adiposo como una reserva de energía, sino también una evaluación aparte de la
> masa muscular (es decir, una puntuación de la condición muscular)»

Y el motivo, que es el que no estaba escrito en el repo: **no existe reserva de
proteína endógena**. «Aunque el propósito del tejido adiposo es servir como
reserva de energía, no existe una reserva análoga de proteína endógena. Debido a
que todas las proteínas endógenas cumplen alguna función, el catabolismo continuo
eventualmente tendrá consecuencias perjudiciales.» Eso es exactamente el pendiente
de `PENDIENTE.md` («la masa muscular, que no es el BCS»), ahora con dos fuentes
y con su porqué.

**3. ⚠️ Y el hallazgo de verdad: lo que la ficha NO pregunta.** El cuadro 170.1
enumera lo que un historial dietético tiene que recoger. Comparado con los 21
campos de `datos_de_la_ficha.json`, la app **no pregunta casi nada de esto**:

| El cuadro 170.1 pide | ¿Lo pregunta la app? |
|---|---|
| Golosinas comerciales (marca, tamaño, frecuencia) | **no** |
| Comida casera o sobras | **no** |
| Golosinas para masticar (cuero crudo, orejas de cerdo) | **no** |
| Suplementos dietéticos que ya toma | **no** |
| **Alimento usado para darle la medicación** | **no** |
| Acceso a la basura y capacidad de rebuscar | **no** |
| Quién más vive en casa o le da de comer | **no** |

Esto es el reverso exacto de la regla de Elena («todo dato que recoja la app
tiene que llegar al motor»): son datos que **la fuente dice que hacen falta y la
app no recoge**. Y no es cosmético para este motor: el menú se calcula al gramo
sobre unas kcal, y un perro al que le dan dos golosinas y las sobras de la cena
no está comiendo esa ración. La más fina es la de la medicación, porque el que
la da ni la cuenta como comida.

---

## Cap. 172 — Nutrición de perros adultos sanos (Martha G. Cline) · LEÍDO ENTERO

**Qué dice.** El perro como omnívoro, sus requerimientos energéticos y los de
nutrientes en la edad adulta temprana (1 a 7 años).

**⚠️ EL HALLAZGO: la energía de mantenimiento va con OTRO EXPONENTE.** El cuadro
172.1 da las fórmulas, y no usan el 0,75 que aplica el motor:

> RE de mantenimiento (todos los perros): **81,5 × (PC en kg)^0,93**
> RE de mantenimiento (solo perros domésticos): **62 × (PC en kg)^0,97**

Y el metaanálisis del que salen: «REM promedio de **142,8 ± 55,3 kcal/kg de
PC^0,75/día**, con una ecuación alométrica estimada de 81,5 kcal/kg de PC^0,93».

El motor aplica la Tabla VII-7 de FEDIAF, que va en **kcal por kg^0,75** — 110
para el adulto de actividad moderada. Con exponentes distintos las dos escalas no
se cruzan en paralelo: **coinciden por el medio y se separan en los extremos**, y
además cambian de signo. Medido:

| Peso | Motor (110·kg^0,75) | Ettinger (62·kg^0,97) | Diferencia |
|---|---|---|---|
| 1,5 kg | 149 | 92 | **+62 %** |
| 3 kg | 251 | 180 | +39 % |
| 10 kg | 619 | 579 | +7 % |
| 20 kg | 1.040 | 1.133 | −8 % |
| 40 kg | 1.750 | 2.220 | −21 % |
| 80 kg | 2.942 | 4.349 | **−32 %** |

O sea: al perro **toy** le damos un 62 % más kcal de las que dice esta fuente, y
al **gigante** un 32 % menos. El cruce está sobre los 12 kg.

**⚠️ CORREGIDO, POR EL MISMO MOTIVO QUE EL CAP. 176.** Escrito así parecía que el
exponente de Ettinger era «el bueno» y el nuestro el raro. **No es eso**, y basta
mirar las otras fuentes que ya están leídas:

| Fuente | Qué usa |
|---|---|
| **NRC 2006** | *«Average maintenance requirements **130 kcal × kg BW^0,75**»* — exponente **0,75** |
| **FEDIAF**, Tabla VII-7 | 95 a 175 kcal/kg^**0,75** según actividad — exponente **0,75** |
| **Ettinger** cap. 172 | un **metaanálisis posterior**: 81,5 × kg^0,93 y 62 × kg^0,97 |

O sea que **dos de las tres usan 0,75**, y lo de Ettinger es un trabajo más
reciente que ese capítulo recoge, no el consenso. La divergencia sigue siendo
real y sigue mereciendo estar apuntada —las kcal deciden todo lo demás, porque
los 43 requisitos se miden por 1000 kcal— pero es **una fuente contra dos**, no
al revés.

Y un detalle que sale de paso: el **130 del NRC** es bastante más alto que el
**110** de FEDIAF para actividad moderada, y es **exactamente** el umbral en el
que el motor cruza al perro de trabajo. Otra coincidencia que conviene tener
apuntada.

**Qué se hace.** Nada: se queda el 0,75 de FEDIAF, y la discrepancia va al
documento del nutricionista con las tres cifras.

Y hay que leerlo con cuidado, que es lo que impide sacar la conclusión fácil: el
110 es un **escalón de actividad** de FEDIAF y el 62·kg^0,97 es la **media de un
metaanálisis** de perros de compañía, así que no son la misma magnitud. Lo que sí
es comparable, y es lo que importa, es **la forma**: el exponente. Con 0,75 la
curva sube más despacio que con 0,97, y eso no depende del coeficiente.

Va a `FEDIAF_CONTRA_OTRAS_FUENTES.md` con las dos cifras, que es lo que se hace
cuando dos fuentes publicadas no dicen lo mismo. Y se junta con lo que ya había
abierto sobre la energía del **cachorro**, donde ya van tres curvas distintas
(Klein en FEDIAF, la Tabla 33-8 de SACN5 un 28 % por encima, y el «2,5 veces
mantenimiento al destete» de Fascetti).

**Lo demás del capítulo, leído y sin nada que aplicar:** que el perro es omnívoro
y no carnívoro estricto (sintetiza taurina, araquidónico y vitamina A de sus
precursores, pero **no sintetiza vitamina D** y **conjuga los ácidos biliares con
taurina** obligatoriamente), y que está adaptado al almidón por tres genes
(AMY2B, MGAM, SGLT1) con variación entre razas. Nada de eso cambia una cifra del
motor, pero la de la vitamina D explica por qué es un tope crónico y no un
requisito cualquiera.

### Cap. 172, segunda parte — macronutrientes, minerales y vitaminas

**⚠️ La biodisponibilidad de los minerales de origen vegetal.** Dice, literal:

> «La biodisponibilidad de calcio, fósforo y magnesio de origen vegetal es
> significativamente menor que la que se encuentra en las sales minerales o en
> los huesos y **debe reducirse en un 50 %**. Además, la biodisponibilidad del
> cobre y del cinc de origen vegetal también está comprometida. Por el
> contrario, el sodio, el potasio y el cloruro se añaden con mayor facilidad y no
> es necesario realizar modificaciones.»

Esto toca al motor de lleno, porque el motor **suma el calcio de todos los
alimentos por igual**: si la mitad del que viene de verdura no llega al perro,
un menú estaría contando calcio que no existe.

**Medido antes de alarmarse**, sobre menús resueltos de verdad, qué porcentaje de
cada mineral viene de categorías vegetales:

| Perro | Calcio | Fósforo | Magnesio |
|---|---|---|---|
| toy 3 kg | 6,3 % | 2,1 % | 16,0 % |
| adulto 10 kg | 2,6 % | 1,6 % | 20,6 % |
| adulto 22 kg | 0,2 % | 0,7 % | 1,4 % |
| adulto 40 kg | 0,6 % | 0,8 % | 2,5 % |
| cachorro 10 kg | 0,1 % | 0,2 % | 3,2 % |

**Y la conclusión es tranquilizadora, por el motivo que el propio libro da.** La
frase exime expresamente «las sales minerales o **los huesos**», y en una ración
BARF el calcio viene justo de ahí: del hueso carnoso y de los suplementos. Aplicar
el −50 % al trozo vegetal movería el calcio como mucho un **3,2 %** y el fósforo
un **1,1 %**. El único que se nota es el **magnesio**, hasta un **10 %** en el
perro pequeño y mediano.

**Qué se hace.** No se cambia nada hoy: el efecto en calcio y fósforo está por
debajo del ruido, y el magnesio va holgado. Queda escrito con su medida, porque el
día que alguien proponga una ración con más verdura —o una vegetariana, que el
cap. 192 discute— esta corrección **sí** haría falta y entonces no hay que volver
a descubrirla.

**Lo demás, leído y anotado:**

- **Proteína.** El NRC pone el mínimo del adulto en **20 g/1000 kcal** y lo
  recomendado en **25**; AAFCO en **51,4**. El motor aplica el mínimo de FEDIAF,
  **52,10**, o sea la escala de AAFCO y no la del NRC. La diferencia no es un
  desacuerdo sobre el perro: AAFCO parte del NRC y le suma el margen por
  digestibilidad y biodisponibilidad del procesado industrial. Anotado porque
  explica por qué nuestro mínimo dobla al del NRC, que es una pregunta que
  cualquiera se hace al comparar las dos tablas.
- **Linoleico.** «Los perros necesitan alrededor del **1-2 % de las calorías
  totales** como ácido linoleico para prevenir los signos clínicos derivados de su
  deficiencia.» Es otra base distinta de la nuestra (g/1000 kcal), y cae por
  debajo de lo que ya exige FEDIAF.
- **Grasa.** Las bandas de las dietas comerciales, en % de EM: baja <25, moderada
  25-35, alta >35, muy baja <20. Sirve para leer las cifras de patología que
  vienen en % de EM, no para aplicar nada.
- **Fibra.** «Los perros no precisan requerimientos nutricionales específicos de
  carbohidratos o fibra.» Confirma por qué la fila «Fibra» de
  `requerimientos_v2_final.json` está con los seis campos a «-» y solo existe para
  que una patología pueda ponerle un suelo.

---

## Cap. 192 — Dietas no convencionales: caseras, vegetarianas y crudas · LEÍDO ENTERO
### (Sally C. Perea y Sean J. Delaney)

**Este es EL capítulo.** Habla literalmente de lo que hace Rawku, y hay que
leerlo entero y sin filtrarlo, porque en su mayor parte es una **crítica** de las
dietas caseras y crudas. Eso no lo invalida: lo hace más útil, porque describe
con precisión el modo de fallo que este motor existe para evitar.

### Lo que dice de las dietas caseras, y es duro

Los estudios que cita, con sus números:

| Estudio | Qué encontró |
|---|---|
| 85 dietas caseras publicadas (49 mantenimiento, 36 crecimiento) | **86 %** con minerales inadecuados · **62 %** con vitaminas · **55 %** con proteína o aminoácidos |
| 5 dietas crudas (2 comerciales, 3 caseras) | **todas** con algún nutriente esencial por debajo del mínimo de AAFCO. Las 3 caseras con Ca:P mal equilibrado, 2 con exceso de vitamina D y 1 con exceso de vitamina E |
| 200 recetas de libros, manuales y webs | **95 %** con al menos un nutriente esencial fuera de NRC/AAFCO · **83,5 %** con varios · **92 %** con instrucciones vagas · **89,5 %** sin instrucciones de cómo darlo |

Y nombra **cuáles fallan más**: «cinc, colina, cobre, EPA+DHA, Ca, vitamina D y
vitamina E». Nueve de esas 200 recetas **pasaban el límite máximo seguro de
vitamina D** y seis el de EPA+DHA.

### ⚠️ El motor contra esa lista, medido

Es la prueba que este capítulo pide a gritos: si esas siete son las que fallan,
¿qué hace el nuestro? Medido sobre menús resueltos de verdad, en % del mínimo de
FEDIAF **ya escalado**:

| Perro | cinc | colina | cobre | EPA+DHA | calcio | vit D | vit E |
|---|---|---|---|---|---|---|---|
| toy 3 kg | 108 % | 173 % | 107 % | 641 % | 181 % | 327 % | 165 % |
| adulto 10 kg | 106 % | 132 % | 150 % | 680 % | 142 % | 112 % | 214 % |
| adulto 22 kg | 135 % | 136 % | 126 % | 586 % | 126 % | 105 % | 282 % |
| adulto 40 kg | 125 % | 147 % | 104 % | 179 % | 167 % | 103 % | 250 % |
| cachorro 10 kg | 149 % | 180 % | 126 % | 101 % | 174 % | 177 % | 872 % |

**Las siete por encima del mínimo en los cinco menús.** El peor caso de cada una
va del 101 % (EPA+DHA en el cachorro) al 165 % (vitamina E). Que varias vayan
justas no es un defecto: el solver minimiza, así que se para donde el requisito
se cumple.

⚠️ **Y por eso importa que el motor mire también los MÁXIMOS.** Dos de los tres
excesos que el capítulo denuncia —vitamina D y EPA+DHA— son justamente topes
crónicos duros del solver, no avisos. El tercero, el Ca:P mal equilibrado, es una
restricción simultánea desde el primer día.

### Lo que sí se aplica, o se tiene que aplicar

**1. El 10 % de los alimentos desequilibrados.** Cifra literal y directa:

> «Los alimentos y premios desequilibrados no se deben proporcionar en más de un
> **10 % de la ingesta calórica diaria total**. Cuando se agregan alimentos
> desequilibrados a una dieta completa y equilibrada, se produce una dilución de
> nutrientes, y los nutrientes esenciales pueden quedar por debajo de los
> requerimientos mínimos.»

Y el mecanismo, con dos ejemplos que son exactamente los nuestros: **la carne
suelta desequilibra el Ca:P** porque lleva mucho fósforo, y **el hígado puede
pasar el máximo de vitamina A**. La app no dice esto en ninguna parte, y es
justo lo que hace un dueño que sigue el menú al gramo y luego da premios. **Esto
hay que decirlo**, y se junta con el hallazgo del cap. 170: la ficha tampoco
pregunta qué premios le da.

**2. La proteína, al menos un tercio del volumen.** «En general, las proteínas
han de constituir al menos un tercio del volumen de la dieta.» Es una proporción
de una fuente publicada, que es lo que a las nuestras les falta (regla 3: las
proporciones de BARF son criterio nuestro). **Medido: nuestros menús van del 88,5
al 93,5 % del peso en fuentes de proteína**, o sea muy por encima. Se cumple con
margen enorme, pero ahora la cifra tiene una fuente detrás.

**3. La harina de huesos, y por qué nuestro calcio no es esa.**

> «La harina de huesos generalmente se consigue con facilidad, pero **se ha
> dejado de usar debido a la preocupación por la contaminación por plomo**.»

El catálogo **no la tiene**: nuestras dos fichas de calcio son **cáscara de
huevo**, que es carbonato cálcico, una de las formas que el propio capítulo
acepta («carbonato de Ca, citrato de Ca o una combinación de Ca y P como CaP
dibásico o tribásico»). Queda escrito para que nadie la proponga sin saber esto.

**4. La sal yodada, y los sustitutos que no llevan yodo.** «Las sales se pueden
usar en dietas caseras para proporcionar sodio, cloruro, potasio y yoduro,
incluida la sal yodada común. **Los sustitutos de la sal (mezclas de cloruro de
potasio) no proporcionan yodo.**» El catálogo tiene sal y dos fichas de yodo;
esto confirma la elección y avisa del sustituto.

**5. La colina y la metionina.** «Los niveles de metionina en la dieta por encima
de los requerimientos necesarios pueden servir para satisfacer una parte del
requerimiento de colina. Sin embargo, debido a que la metionina es un aminoácido
limitante, especialmente en dietas bajas en proteínas, **generalmente se
recomienda la suplementación de colina**.» El motor exige las dos por separado,
que es lo conservador. Y enlaza con el pendiente de la ficha de L-metionina que
la nutricionista pidió.

**6. ⚠️ Y la que explica el hueco de la vitamina E suelta:**

> «Debido a que la suplementación de una mayor cantidad de vitaminas y minerales
> puede provocar el **exceso de otros nutrientes** más allá de los límites
> seguros, puede ser necesario **suplementar de forma separada** los nutrientes
> limitantes claves.»

Es exactamente el problema del suelo de vitamina E: para llegar a 67,1 mg hay que
meter más multivitamínico, y eso arrastra todo lo demás hacia sus topes. La
fuente dice que la salida es un suplemento **suelto**, que es justo lo que falta
en el catálogo. Ya no es una intuición nuestra: está escrito.

### Lo que dice del CRUDO, y hay que decirlo entero

El capítulo no recomienda el crudo. Nombra tres riesgos —bacterias patógenas,
contaminación ambiental y obstrucción por huesos— y trae los casos: dos gatos con
salmonelosis por carne cruda de vacuno, uno muerto; y un brote en un criadero de
galgos donde **S. enterica salió en 88 de 133 muestras**, el 93 % de las fecales
y el **75 % de la carne cruda**, y también del suelo, los comederos, el fregadero
y las moscas. Cita la postura de la FDA: «La FDA no aboga por una dieta cruda de
carne, de aves de corral o mariscos en mascotas».

Y señala el riesgo para las personas: las mascotas que no enferman **excretan el
patógeno igual**, con más riesgo para niños, mayores e inmunodeprimidos.

**Qué se hace con esto.** No cambia ni una cifra del motor, porque no es
nutrición: es manipulación. Pero **es información que quien usa la app tiene
derecho a tener**, y hoy no se la damos. Va a `PENDIENTE_PRODUCTO.md` como
decisión de Elena, no mía: qué se le cuenta al dueño sobre el riesgo bacteriano y
sobre el manejo, y con qué palabras.

### Cap. 192 — coda: la salmonela NO es lo del cerdo

Pregunta de Elena: «¿lo de la salmonela viene del cerdo? Nosotros no tenemos
nada de cerdo». Comprobado en el texto, y no:

- **Los casos del capítulo son de VACUNO.** Los dos gatos («una dieta cruda a
  base de carne de vacuno», uno muerto) y el brote del criadero de galgos, con
  el serotipo en el **75 %** de las muestras de carne cruda. La postura de la FDA
  que cita habla de «carne, aves de corral o mariscos».
- **Y el catálogo está lleno de los reservorios clásicos**: 10 fichas de pollo,
  10 de ternera, 8 de pavo, 7 de vaca.

**Lo que SÍ es del cerdo está en otro capítulo y es peor.** La enfermedad de
Aujeszky o pseudorrabia: *«poco frecuente pero mortal […] Se cree que la mayoría
de los casos en perros son el resultado de la ingestión de carne de cerdo cruda
infectada»*.

**Consecuencia para nosotros, y son dos:**

1. **No tener cerdo está bien, ahora por dos motivos de fuente**: el cobre del
   hígado de cerdo con disponibilidad cero (SACN5 cap.6) y esto, que es mortal.
   Va a `DATOS_QUE_FALTAN.md` para el día que alguien proponga una ficha.
2. ⚠️ **El aviso al usuario no puede ser «cuidado con el cerdo»**, que es lo que
   la gente cree. Tiene que ser sobre el manejo del **pollo y la ternera** que sí
   le estamos dando.

---

## Cap. 171 — Nutrición neonatal y pediátrica · LEÍDO ENTERO

**⚠️ CUARTA curva para la energía del cachorro.** «Los requerimientos energéticos
[…] para cachorros se pueden estimar en **3 veces el requerimiento de energía en
reposo** (RER; 70 × PC^0,75) desde el destete hasta los 4 meses de edad y en **2 ×
RER** para el resto del periodo de crecimiento.»

Medido contra lo que aplica el motor (curva de Klein, vía FEDIAF):

| Peso | Edad | Adulto esperado | Motor | Ettinger | Diferencia |
|---|---|---|---|---|---|
| 3 kg | 3 m | 5 kg | 441 | 479 | −8 % |
| 10 kg | 3 m | 30 kg | 1.185 | 1.181 | **0 %** |
| 10 kg | 8 m | 15 kg | 835 | 787 | +6 % |
| 25 kg | 8 m | 35 kg | 1.815 | 1.565 | +16 % |
| **30 kg** | **5 m** | **60 kg** | **2.564** | **1.795** | **+43 %** |

Coincide bien en el cachorro pequeño y joven, y **se separa justo en el cachorro
grande en pleno crecimiento**, que es la población donde el exceso de energía hace
daño de verdad. Ya van **cuatro fuentes y cuatro curvas**: Klein (FEDIAF, la que
aplicamos), SACN5 Tabla 33-8 (hasta un 28 % por encima de Klein), Fascetti («2,5
veces mantenimiento al destete») y esta.

**Y el propio capítulo dice por qué importa**: «Los excesos de nutrientes con
efectos en el desarrollo esquelético (**calcio, vitamina D, vitamina A**) se
pueden observar en mascotas en crecimiento alimentadas con una dieta comercial
suplementada con calcio u otras vitaminas/minerales.» Los tres tienen tope en el
motor; el del calcio del cachorro de raza grande es de SACN5 y Fascetti.

**Lo demás, leído:**
- «Las deficiencias y los excesos de nutrientes […] pueden observarse con dietas
  caseras mal formuladas (o crudas); por lo tanto, **no son la mejor opción para
  los animales en crecimiento y deben evitarse**.» Es la postura del libro sobre
  formular en crecimiento, y va con lo del cap. 192.
- La dieta de **lactancia** necesita **≥4 kcal EM por gramo de materia seca**, y
  las de cachorro de raza grande **no valen** para reproducción por ser menos
  densas.
- EPA y DHA preformados de aceites marinos son más eficientes que su precursor:
  «la capacidad de perros y gatos para biotransformarlo es limitada». Confirma por
  qué el motor exige EPA+DHA y no linolénico a secas en crecimiento.

---

## Cap. 173 — Manejo nutricional del perro deportista · LEÍDO ENTERO

**Confirma dos cifras del motor, y las dos importan:**

- **«Los perros domésticos activos precisan […] aproximadamente 130 × (peso
  corporal metabólico en kg)^0,75.»** Es **exactamente** el umbral en el que el
  motor cruza al perro de trabajo y le apreta los topes crónicos por peso
  metabólico (BLOQUE 86). Ahora esa cifra tiene una segunda fuente.
- **Los perros de trineo «consumen aproximadamente 1.000 kcal/kg^0,75 al día»**
  (un perro de 25 kg, unas 10.000 kcal/día). `niveles_de_actividad.json` declara
  la fila de FEDIAF de los perros de trineo (860-1240) como **fuera a propósito**,
  y esta cifra cae dentro. La decisión de dejarlos fuera se sostiene.
- Los **galgos**, 150-160 kcal/kg^0,75, caen dentro del escalón más alto que sí
  ofrece el motor.

**⚠️ Y un conflicto real con la ración cruda, que hay que decir:**

> «debe encontrarse **carbohidrato digerible en la dieta al menos en un 50 % de
> la energía metabolizable (EM)** para su uso en perros de carreras y entre el 15
> y el 30 %» para el resto.

**Una ración BARF de este motor no lleva prácticamente hidratos.** Para el perro
de carreras esto no es un matiz: la fuente dice que la mitad de su energía debería
venir de algo que nosotros no le damos. No es un límite nutricional que se pueda
apretar — es que el motor **no formula para ese perro**. Va a
`PENDIENTE_PRODUCTO.md`: hay que decidir si se avisa, o si el perro de carreras
queda declarado fuera del alcance como ya lo está el de trineo.

**La proteína del perro de competición**, para tener la banda:
- Trineo: «aproximadamente el **30 % de la EM** diaria (**70-80 g de
  proteína/Mcal**) […] de origen animal altamente digestibles».
- Carreras: **24 % de la EM o superior** es la recomendación general.
- Los perros de detección de olores rindieron bien con solo **18 % de EM**.

Encaja con la Tabla 4.2 de Fascetti (90 g/Mcal aeróbico de larga distancia, 60
anaeróbico corto) y queda **por debajo** de lo que ya da un BARF de este motor
(~105 g/1000 kcal), así que no aprieta nada.

**La grasa**: «en torno al **55-70 % de EM** en forma de grasa» para resistencia,
y hay que introducirla **gradualmente, 8-12 semanas antes** de la competición.
Eso último es manejo, no formulación, pero es lo que un dueño necesitaría saber.

---

## Cap. 176 — Obesidad · LEÍDO ENTERO

**Confirma el BCS.** «Cada punto arriba o abajo representa una ganancia o pérdida
de peso de aproximadamente un **10-15 %**», sobre la escala de 9 validada con DXA.
El motor aplica un **45 %** de exceso al BCS 9 (cuatro puntos sobre el 5), que cae
dentro del 40-60 % que sale de esa regla. Y define obeso como **15-20 % por
encima del peso óptimo**.

**⚠️ Y una divergencia real en el adelgazamiento, que es clínica.**

> «Generalmente es de alrededor del **80 % del requerimiento de energía en reposo
> (RER), basado en el peso ideal** de la mascota, con controles cada 2-4 semanas.
> Algunos estudios recomiendan mayores restricciones en el RER (**60 %**).»
> RER = 70 × (peso ideal en kg)^0,75

Medido contra lo que da el motor cuando se le pasa el peso ideal:

| Peso real | Peso ideal | Motor | 80 % RER | 60 % RER | Motor vs 80 % |
|---|---|---|---|---|---|
| 20 kg | 15 kg | 534 | 427 | 320 | **+25 %** |
| 35 kg | 25 kg | 783 | 626 | 470 | +25 % |
| 45 kg | 30 kg | 897 | 718 | 538 | +25 % |

El motor da **el RER entero del peso ideal**; esta fuente pide el **80 %**.

⚠️ **CORREGIDO EL MISMO DÍA, y la corrección la provocó Elena** («pero SACN5
también hablaba de eso»). Escrito así, esto parecía que dábamos de más que la
literatura. **No es eso: son DOS FUENTES CLÍNICAS QUE NO COINCIDEN**, y la
nuestra es la de SACN5. Su cap. 27 dice, literal:

> «Determine RER for ideal weight (also from Table 27-3, immediately below ideal
> weight) **= initial estimated daily energy intake**.»

O sea **exactamente lo que hace el motor**. Y añade el marco: «RER should provide
approximately 70 to 80 % of DER for optimal weight or 60 to 70 % of DER for obese
weight».

Los tres números, sobre el peso ideal:

| | kcal/kg^0,75 |
|---|---|
| FEDIAF, «Obese prone adults **≤ 90**» (Tabla VII-7) — es un **techo** | ≤ 90 |
| **SACN5 cap. 27 y el motor** | **70** (el RER entero) |
| Ettinger cap. 176 | 56 (el 80 % del RER) |

**Y por eso la regla de la jerarquía no decide aquí.** FEDIAF pone un techo y
estamos por debajo, así que no hay conflicto con ella; el desacuerdo es entre dos
libros de clínica del mismo nivel. Se queda como está —con SACN5, que es la fuente
de la que sale casi todo lo demás del motor— y **va al nutricionista como
discrepancia, no como error**.

**El ritmo de pérdida coincide en las tres**: SACN5 pide 1-2 % del peso inicial
por semana, con el 0,5 % como mínimo y el 2 % como máximo, y Ettinger 0,5-2 %. El
aviso del motor dice 1-2 %.

**Y el ritmo, que casi coincide.** «La pérdida de peso debe progresar lentamente
(**0,5-2 % por semana**)». El aviso del motor dice **1-2 % a la semana**, o sea
una banda más estrecha dentro de la suya. La fuente admite bajar hasta el 0,5 %.

**Lo demás, leído:** dieta alta en proteína y baja en hidratos porque la tasa de
utilización energética de la proteína (77 %) es menor que la de la grasa (94 %);
la fibra, sin acuerdo universal sobre su eficacia; y la L-carnitina, que el motor
ya tiene como clave y solo aplica como suelo de patología.

---

## Caps. 175, 177, 179, 180, 183, 184 y 185 · LEÍDOS

Leídos en bloque, apuntando solo lo que toca al motor. Cada cifra comparada
contra lo que aplicamos **y contra las otras fuentes**, que es la regla de arriba.

### Cap. 175 — Geriátricos sanos
- **Repite el 10 % de los premios**, y lo define mejor que el cap. 192: «se
  recomienda que un **máximo del 10 % de las calorías diarias** se destinen a
  alimentos poco nutritivos (como **premios, sobras de la mesa, suplementos**)».
  Segunda fuente para el mismo pendiente.
- Sénior: el último **25 %** de la esperanza de vida de su raza. Nuestro corte es
  por edad absoluta (>7 años). Apuntado; ya está en la lista de discrepancias.
- **No restringir proteína al sénior sano**: «menos del 20 y 30 % de calorías
  proteicas» solo si hay enfermedad renal. El motor **no** restringe proteína al
  sénior. Confirma.

### Cap. 177 — Caquexia y sarcopenia
Sin cifras que aplicar. Confirma por tercera vez el hueco de la **masa muscular**:
la pérdida de masa magra se da en más del 50 % de los perros con insuficiencia
cardíaca congestiva y el peso puede **subir** enmascarándola.

### Cap. 179 — Enfermedad pancreática
- **Grasa en pancreatitis: «menos de un 15 % […] en base a MS»** para perro. Al
  convertir con la densidad de siempre: 15 × 2,5 = **37,5 g/1000 kcal**, que es
  **exactamente** lo que aplica el motor desde SACN5 Tabla 67-3. Dos fuentes, el
  mismo número.
- ⚠️ **Y contradice lo que mucha gente cree sobre la IPE**: «Anteriormente se
  recomendaba la restricción de grasas en la dieta para el [tratamiento de la
  IPE]», y los estudios que cita comparan dietas con 51 %, 40,8 %, 30 % y 22 % de
  grasa sobre EM **sin encontrar beneficio en restringir**. Comprobado: el motor
  **no** restringe grasa en la insuficiencia pancreática exocrina. Correcto.

### Cap. 180 — Enfermedad hepática
- **⚠️ Cobre, y aquí sí manda FEDIAF.** «Las dietas restringidas en Cu pueden
  contener **tan solo 3 ppm de Cu en base a materia seca**» = **0,75 mg/1000
  kcal**. Pero el **mínimo de FEDIAF para el adulto son 2,08**, así que esa cifra
  **no la puede alcanzar una ración completa**: bajar ahí deja al perro
  deficiente. El motor aplica **2,4**, que es lo más apretado que cabe sobre el
  mínimo, con un 15 % de sitio. **Caso de manual de la regla: la fuente clínica
  pide menos que el mínimo nutricional y gana FEDIAF.**
- **No restringir proteína a todos**: «la restricción de proteínas […] no se
  recomienda para todos, ni incluso [en la mayoría]». El motor no la restringe en
  hepatopatía salvo encefalopatía. Confirma.

### Cap. 183 — Enfermedad cardíaca
- **«La restricción de proteínas debe evitarse en perros y gatos con»**
  cardiopatía, y las dietas renales o sénior «no se recomiendan a menos que exista
  una disfunción renal grave». Comprobado: el motor **solo** toca el sodio en
  cardiopatía. Confirma.
- **El sodio de las dietas comerciales va «entre 33 y 412 mg/100 kcal»** = 330 a
  4.120 mg/1000 kcal. Los tres topes del motor (738,6 en B2, 625 en C, 480 en D)
  caen dentro de la mitad baja. Sin conflicto.
- **L-carnitina 50-100 mg/kg**, que es dosis por perro y no concentración.
- Magnesio de las dietas bajas en sodio: 10-50 mg/100 kcal, con mínimo AAFCO de
  11 mg/100 kcal.

### Cap. 184 — Enfermedad renal
- Sodio: llama «baja» a una dieta de **1,0 g/Mcal** (= 1.000 mg/1000 kcal) y
  «alta» a **3,1**. El motor no topa sodio en renal, solo fósforo. Apuntado.
- Grasa hasta el **30 % en base a MS**; las de aceite de pescado al 15 %.
- **El cloruro de K no se recomienda** por palatabilidad.
- ⚠️ **Y avisa contra restringir sodio a lo bruto**: en gatos con ERC inducida «la
  restricción de Na se asoció con hipopotasemia». Va contra la idea intuitiva.

### Cap. 185 — Tracto urinario inferior
- Las dietas secas comerciales que estudia llevan **sodio por encima de 2,5
  g/1000 kcal**, y hasta 2,9.
- **El sodio alto aumenta la excreción urinaria de calcio**, que es lo que importa
  en el oxalato cálcico.
- Acidificantes y alcalinizantes nombrados uno a uno (metionina, sulfato de calcio
  o sodio, cloruro de calcio o amonio · carbonato de calcio o sodio).
