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

**Qué se hace con esto.** Nada todavía, y por la regla de siempre: **manda
FEDIAF**, y la Tabla VII-7 es de FEDIAF. Pero esto no es un matiz: **las kcal
deciden todo lo demás**, porque los 43 requisitos se miden por 1000 kcal. Una
diferencia del 62 % en el perro pequeño mueve la ración entera.

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
