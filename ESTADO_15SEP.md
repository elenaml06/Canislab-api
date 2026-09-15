# Dónde vamos, qué falta — 15 de septiembre de 2026

Escrito porque Elena lo pidió con estas palabras: «hoy hemos hecho un montón de
cosas y me da la sensación de que hemos dejado otro montón a medias. Necesito
saber bien cómo vamos, por dónde vamos, qué falta».

Tiene razón: **la batería está en ROJO con 25 fallos**, así que nada de esto se
puede entregar todavía. Esto es el mapa honesto.

---

## 1 · Lo que está HECHO y empujado a `cerrar-nutricion-15sep`

| Commit | Qué |
|---|---|
| `014393a` | **Las etiquetas de los 25 suplementos**: 62 celdas corregidas en 12 fichas, `ETIQUETAS_DE_LOS_SUPLEMENTOS.md`, BLOQUE **116** (7 formas de fallo), BLOQUE **118** (3 formas), `CERRADO.md` corregido, P-43 |
| `c817f97` | **Catálogo de menús regenerado** (214 de 216) y arreglo de `regenerar_catalogo.py` |
| `4417fef` | **P-44**: la medicación la mete quien la receta |
| `e9255f2` | BLOQUES **9**, **85** y **100** arreglados |

---

## 2 · Lo que BLOQUEA la entrega: 25 fallos de batería

Ordenados por si sé ya la causa o no.

### Causa conocida — esperan una decisión de Elena

| Bloques | Qué pasa |
|---|---|
| **57** ×4 · **9** · **43** ×5 · **49** | **El suelo de vitamina E del perro sano está ENCENDIDO** y el BLOQUE 57 exige que esté apagado. Su propio texto lo avisa: «si se ha vuelto a encender, este bloque tiene que saberlo en el MISMO commit — y entonces los BLOQUES 9 y 43 se ponen rojos, que es lo que cuesta y está medido» |

⚠️ **Y hay algo que no estaba medido cuando se encendió**: el suelo se encendió
esta mañana con la medida «los menús llegan a 114-167 mg/1000 kcal», y esa medida
se hizo **con las cifras de vitamina E infladas** que las etiquetas corrigieron
después. Remedido con los datos buenos: los menús salen a **67,7 contra un suelo
de 67,1**, o sea un margen del **0,9 %**.

### Causa conocida — son míos o de la rama, y sé cómo se arreglan

| Bloques | Qué pasa |
|---|---|
| **104** ×5 | **212 celdas no se rehacen** contra `fuentes_instantanea.json` (el mensaje corta a 5). En `main` son **0**. De ellas **132 son de la rama** —los 12 aminoácidos de 11 verduras que dicen venir de USDA y cuya fila no se congeló— y **80 son de etiqueta**, mías: ahí congelar mi propia transcripción sería el fichero contra sí mismo, y su guardián correcto es el BLOQUE 116 |
| **19** | El aminograma del **tomate en puré**: 0,92 g de aminoácidos sobre 4,50 g de proteína = 20 %, fuera de la banda 25-85 %. También de la rama |
| **107** | Cinco textos de `main.py` escriben a mano cuántos requisitos comprueba el motor |

### Causa por investigar

| Bloques | Qué dice |
|---|---|
| **11** ×3 | La **rotación de proteína** no está haciendo nada: los 3 menús de un mismo perro repiten proteína dos veces seguidas |
| **14** | «No se encuentra la lista de categorías exentas del suelo» |
| **76** | La API **reintenta un peldaño ya declarado infactible** 9 veces de 17 — justo lo que se arregló hoy, así que el arreglo puede estar incompleto |
| **101** ×2 | **Cairo** (cachorro de raza grande con premios) se queda **sin menú**, y el techo que sube no se aplica |
| **113** | Quitándole al solver la fila de materia seca, el menú **sigue** cumpliendo los siete techos legales: o el guardia no muerde, o hay que remedirlo |

---

## 3 · Lo que Elena ha pedido hoy y NO está hecho

| | Estado |
|---|---|
| **Un solo suplemento por defecto**, dos solo si es imposible | **medido, sin construir**. Con 1 sale **1 de 6**; con 2, **6 de 6** — y en 5 de los 6 el segundo bote es **la vitamina E** |
| **La medicación la mete el veterinario** (P-44) | escrita y con luz verde, **sin construir** |
| **La ficha que solo vea un veterinario** | **no existe el mecanismo**: `GET /alimentos` sirve las 164 fichas sin mirar quién pregunta, y `/menu/anadir` aceptaría el nombre aunque la pantalla no lo enseñara |
| **Unificar el factor de la vitamina E** | hay **tres** (0,67 · 0,671 · 1/1,49) para la misma conversión |
| El mensaje cuando alguien excluye los suplementos | dice «no existe combinación», sin decir **qué** falta |
| Probar el arreglo de `regenerar_catalogo.py` | sin probar: probarlo reescribe el catálogo |

---

## 4 · Las decisiones que son de Elena y de Cris

1. **El suelo de vitamina E del perro sano: ¿encendido o apagado?** Es la misma
   decisión que «un solo suplemento», y decide 11 de los 25 fallos.
2. **P-43**: para qué sirve la metionina y para qué no (acidificar la orina se
   busca en la estruvita y es lo contrario en oxalato y urato). Clínico → Cris.
3. **P-38**: los 122 límites que vienen de una tabla en % de materia seca y se
   convirtieron suponiendo 4,0 kcal/g cuando la medida real es 5,20.
