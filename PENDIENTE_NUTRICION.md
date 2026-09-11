# Nutrición — auditado contra el PDF oficial

Parte de `PENDIENTE.md` (secciones 5, 5-bis, 5-ter, 5-quater), separado
el 6 de septiembre. Si esta sesión toca nutrición, patologías o el
catálogo, mira también `canislab-fuentes/ESTADO_Y_PROXIMOS_PASOS.md`.

## 5. Nutrición — auditado contra el PDF oficial

> ### ⚠️ LO QUE ESTA AUDITORÍA **NO** COMPRUEBA (25 de agosto)
>
> Se escribe aquí porque el 25 de agosto apareció un fallo que esta
> auditoría tenía delante y no vio, y la pregunta que hizo falta contestar
> fue: *«¿cómo puedo fiarme de que está todo correcto?»*. Merece una
> respuesta escrita, no de palabra.
>
> **Lo que pasó.** En `requerimientos_v2_final.json` había una fila
> `Fibra` (mínimo 4,29 g/1000 kcal, máximo 14,3) **que no está en la tabla
> de FEDIAF**. Lleva ahí desde el primer commit del repositorio (14 de
> agosto), sin nota de fuente. El motor nunca la usó, pero el analizador
> sí: por eso un menú hecho por la propia app salía «le falta fibra». 8 de
> 8 menús verdes se quedaban cortos.
>
> **Por qué la auditoría dijo «161 cuadran, 0 discrepancias».** Porque
> recorría la lista de FEDIAF y comprobaba que cada valor estuviera bien
> puesto en el JSON. Nunca comprobaba lo contrario: que cada fila del JSON
> venga de FEDIAF. Una fila que sobra era invisible. **Ya no**: desde el 25
> de agosto mira los dos sentidos, y el BLOQUE 18 de `pruebas_completas.py`
> la ejecuta y exige 0 discrepancias.
>
> **Lo que sigue sin comprobar nadie**, y hay que saberlo:
>
> 1. **La tabla de FEDIAF de `auditar_fediaf.py` está transcrita a mano**
>    del PDF. Si un número se tecleó mal ahí Y está igual de mal en el
>    JSON, los dos cuadran y nadie se entera. Lo único que lo cierra es
>    que una persona lea las dos columnas contra el PDF una vez.
> 2. **Los valores de los ALIMENTOS (`alimentos_v3_final.json`) no tienen
>    ninguna auditoría.** Los requisitos sí; la composición de cada
>    alimento, no. Un valor mal ahí tuerce todos los menús que lo usen y
>    ninguna prueba lo vería: las pruebas comprueban que el motor cumple
>    los requisitos *con los datos que tiene*.
> 3. ~~Faltan datos de fibra en 3 verduras (borraja, coles de Bruselas,
>    tomate en puré)~~ **cerrado (7 de septiembre)**: comprobado contra el
>    catálogo actual, `Coles de Bruselas` (4,3 g/100g) y `Tomate (puré)`
>    (2,8 g/100g) ya traen el dato; `Borraja` no existe como ficha en
>    `alimentos_v3_final.json` (no es que le falte fibra, es que no está el
>    alimento). De hecho las 159 fichas del catálogo traen ya la clave
>    `fibra` — solo 3 (las tres formas de huevo) la marcan `sin_dato` en
>    vez de cero confirmado, que es lo correcto para un alimento donde 0
>    es razonable pero no está medido. **El dato del catálogo está
>    completo**; lo que sigue abierto es solo lo de la sección 9/10: la
>    fibra no es una de las 41 filas que mide el motor.
>
>    **Y no es un simple "añadirla al MAPA cuando haya un momento" (7 de
>    septiembre).** `auditar_fediaf.py` tiene, desde el 25 de agosto, una
>    comprobación explícita "¿SOBRA ALGUNA FILA EN EL JSON?" que rechaza
>    cualquier fila de `requerimientos_v2_final.json` que no venga de la
>    tabla III-3b de FEDIAF — y el ejemplo que cita en su propio comentario
>    es literalmente este: *"o no es un requisito y no puede acabar en
>    ningún mapa de requisitos (es lo que pasó con 'Fibra')"*. Y no es solo
>    la auditoría: el bucle que de verdad construye las restricciones del
>    solver (`motor_completo.py`, `for nombre_req, clave in MAPA.items():
>    r = req.get(nombre_req); if not r: continue`) salta cualquier clave
>    sin fila en ese JSON — así que un suelo por patología sobre fibra
>    (para diabetes, hiperlipidemia, colitis) tampoco se aplicaría nunca
>    sin una fila ahí, con el mismo riesgo de origen: convertiría una fila
>    inventada en un requisito que decide menús, en silencio, otra vez.
>    Para desbloquear eso de verdad hace falta una de dos cosas, ninguna de
>    las cuales es "rellenar datos": (a) un objetivo clínico real (no
>    inventado) de un nutricionista veterinario para al menos una de esas
>    tres patologías, documentado como excepción explícita en
>    `NO_SON_NUTRIENTES_DE_LA_TABLA` igual que ya se hace con
>    `Relacion_Ca_P` y `Calcio_LateGrowth_RazaGrande`; o (b) un mecanismo de
>    suelo/tope que no pase por `requerimientos_v2_final.json`, que hoy no
>    existe. Verificado leyendo el código, no de memoria.
>
> **Qué significa «TODO EN VERDE»**, para no volver a confundirlo: que el
> motor cumple lo que dice el JSON, que ningún menú sale sin verificar, y
> que las reglas del motor existen de verdad. **No** significa que el JSON
> sea correcto. Eso lo dice la auditoría contra el PDF, y solo hasta donde
> llega la transcripción del punto 1.

**Hecho el 21 de agosto** contra la TABLA III-3b de la *FEDIAF Nutritional
Guidelines 2025* (el PDF oficial, no de memoria). Script reproducible en
`auditar_fediaf.py`.

**161 de 161 comprobaciones cuadran exactas** — mínimos *y* máximos. Se
verificó, para los nutrientes del JSON y en las tres etapas: el valor,
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

**Hecho el 21 de agosto**, hasta donde se pudo:

- **Timo de ternera**: 16 nutrientes rellenados con la ficha USDA FDC
  170194 (la que la propia entrada ya citaba). La vitamina A sí es un cero
  real según la fuente. Los 12 que USDA no publica quedan en `sin_dato`.
- **Testículos de cordero**: 7 rellenados con la ficha USDA de *Lamb, New
  Zealand, testes, raw*, incluidas proteína y grasa, que estaban a cero
  con 68 kcal declaradas — el motor lo veía como calorías sin macros. Los
  23 restantes, en `sin_dato`.
- **Grasa de pollo**: revisado y **estaba bien**. Sus ceros son reales (la
  grasa fundida no tiene proteína ni minerales) y los huecos que sí tiene
  —ácidos grasos y vitamina E— ya estaban declarados.

Validación: tras rellenarlos, la energía declarada cuadra con los macros
por Atwater (ratio 1,01 y 1,00), lo que confirma que las cifras son
coherentes entre sí.

- [x] **Contrastar esas cifras con la ficha original de USDA — RESUELTO,
      y la premisa había caducado.** «El entorno no tiene acceso a
      fdc.nal.usda.gov» dejó de ser cierto en algún punto posterior a
      escribir esto: `api.nal.usda.gov/fdc/v1` responde con `DEMO_KEY`
      (usado con éxito el 7 de septiembre para el linoleico de "Grasa de
      pollo", FDC 173564). **Testículos de cordero ya no existe en el
      catálogo** (retirado en algún punto posterior a esta nota — no hay
      nada que contrastar). **Timo de ternera** ya cita FDC 170194
      directamente en su `nota_datos` y se corrigió con esa misma ficha el
      6 de septiembre (cobre, -27%) — ya está a la fuente primaria, no a un
      espejo.
- [x] **El linoleico de la grasa de pollo — RESUELTO el 7 de septiembre.**
      19,5 g/100g, USDA FDC 173564 "Fat, chicken" (SR Legacy, NDB 4542):
      su proteína (0) y grasa (99,8) ya coincidían exactas con esta ficha,
      así que es con altísima probabilidad la misma fuente que el resto de
      la fila. Cerrado en `alimentos_v3_final.json`.
- [x] **Que el aviso de datos incompletos no dependa de una lista mantenida
      a mano — HECHO el 7 de septiembre, y encontró once huecos el mismo
      día.** `auditar_catalogo.py` tiene ahora un aviso `[SOSPECHOSO]` que
      no lee ninguna lista: compara cada alimento con **los demás de su
      categoría**. Si el 90 % de sus compañeros tienen un nutriente y él lo
      tiene a cero sin declararlo, se dice. El criterio sale del propio
      catálogo, así que crece solo cuando entra un alimento nuevo.
      El umbral se midió: con 80 % entraban los ceros REALES de la grasa de
      la fruta y con 95 % se escapaban seis huecos de verdad.
      **El denominador son LOS DEMÁS, no todos**, y eso no es un detalle: la
      primera versión metía al propio alimento en la cuenta, así que en una
      categoría pequeña un hueco se tapaba a sí mismo (en «Hígado», que
      tiene 6, vaciar uno deja 5 de 6 = 83 % y ya no llegaba al 90 %). Se
      descubrió porque el BLOQUE 46 planta el fallo a propósito y NO
      saltaba; al arreglarlo apareció un hueco real, el linoleico del hígado
      de cordero. Lo vigila el **BLOQUE 46**, que no se conforma con verlo
      salir limpio: vacía la tiamina de un hígado en una copia del catálogo
      y exige que la auditoría lo encuentre.
      Sale a cero hoy porque los once que levantó están resueltos, y hay una
      salida nueva para no volver a preguntar lo ya contestado:
      **`cero_verificado`**, un campo por ficha donde se escribe que un cero
      se fue a mirar, es real, y con qué fuente — el mismo patrón que ya
      usaban `purinas_fuente`, `taurina_fuente` y `fuente_epa_dha`.
- [ ] El aviso que ve el USUARIO (`datos_incompletos`, en `verificar.py`)
      sigue leyendo solo `sin_dato`. No se enganchó al detector nuevo a
      propósito: el `[SOSPECHOSO]` acierta lo bastante para que una persona
      lo lea una vez, pero no lo bastante para salir en cada menú — de los
      trece que levantó, cuatro eran ceros REALES (la vitamina A del
      champiñón, la coliflor, el coco y el cardo). Un aviso que se equivoca
      una de cada tres veces enseña a la usuaria a ignorarlo, y entonces
      tampoco verá el que sí importa. Queda como decisión abierta.

## 5-ter. Revisión del catálogo entero (21 de agosto)

Hecha con `auditar_catalogo.py`, que queda en el repo y se puede repetir.
Comprueba cuatro cosas que ninguna prueba del motor puede detectar, porque
el motor cumple perfectamente unos datos incompletos.

**Lo que salió bien:** la energía cuadra con los macros en los 163
alimentos. Cero incoherencias. Todo el catálogo está en la misma base
(peso fresco), que es lo que hace válido el cálculo por 1000 kcal.

**Huecos declarados** (ya aplicado): 10 alimentos tenían nutrientes a cero
sin declarar. Seis pescados con EPA y DHA a cero —incluido el **boquerón**,
que con 6,3 g de grasa es pescado azul y ese cero es falso— y cuatro
vísceras (bazo de vaca, páncreas de vaca, bazo de cordero, cerebro de
ternera). Pasan a `sin_dato` para que salte el aviso de datos incompletos.

- [x] **Los seis pescados con EPA/DHA — YA ESTABAN CERRADOS**, y este punto
      llevaba desde el 25 de agosto describiendo un trabajo hecho. Se
      comprobó el 7 de septiembre recorriendo el catálogo entero: **no
      queda ni un solo pescado con `epa` o `dha` en `sin_dato`**. Los seis
      (bacalao, boquerón, gamba roja, langostino, perca, pescadilla) llevan
      su fuente en `nota_datos` y sus cifras ancladas en el BLOQUE 21.
- [x] **Las cuatro vísceras — COMPLETADAS el 7 de septiembre**, con la
      ficha de su fuente, como pedía este punto. Y la fuente se pudo
      identificar con certeza en vez de suponerla: bazo de vaca, páncreas
      de vaca y bazo de cordero coinciden **celda a celda** con USDA FDC
      169454, 169452 y 174364 en todas las que ya tenían valor, así que
      rellenar sus huecos con esa misma ficha es completar la MISMA fuente,
      no cruzar dos. El cerebro de ternera es el único de los cuatro que
      tiene fuente primaria española (BEDCA 1047, "Sesos, de ternera,
      crudos") y de ahí salen sus 17 celdas nuevas.
      Siguen sin dato yodo, vitD, vitE, colina y cloruro de los tres de
      USDA: esa base no los publica, y BEDCA y CIQUAL no tienen bazo ni
      páncreas de ninguna especie.
- [x] **Las dos «discrepancias» del cerebro NO lo eran, y detrás había algo
      peor — RESUELTO el 7 de septiembre.** El calcio (43 mg frente a 10-12)
      y el selenio (21,3 µg frente a 10-11,6) se apuntaron aquí como posibles
      errores de dato. No lo son: **son exactos de USDA FDC 168622, que es
      cerebro de VACA**, y se estaban comparando contra cerebro de TERNERA
      (USDA 174351, BEDCA 1047, CIQUAL 40006), que es otro animal.
      La ficha se llamaba «Cerebro de ternera» y sus datos eran de vaca:
      coincide celda a celda con la ficha de vaca en las nueve que tenían
      valor (proteína 10,86, grasa 10,3, calcio 43, selenio 21,3, hierro
      2,55, potasio 274, zinc 1,02, vitB12 9,51). **Es exactamente lo que ya
      pasó con «Bazo de ternera» y «Páncreas de ternera»**, renombrados a
      «de vaca» el 21 de agosto por la misma razón — al cerebro se le pasó.
      Renombrado a **`Cerebro de vaca`** (0 referencias en
      `catalogo_menus.json`, comprobado).
      **Y la ficha se rehízo entera**, porque ese mismo día yo le había
      rellenado 17 celdas desde BEDCA 1047, que es la ficha de ternera: el
      DHA quedó en 0,36 g cuando el de vaca es **0,851**, y la vitamina A en
      0 cuando son 7 µg. Ahora toda la ficha sale de USDA 168622, una sola
      fuente, y lo que esa ficha no publica (vitD, yodo, colina) vuelve a
      `sin_dato` en vez de llevar cifras de la otra especie.
      **La lección, y es la de este proyecto entera**: una explicación
      plausible para un aviso nuevo no es una comprobación. El aviso `[OMEGA]`
      saltó al rellenar y se le buscó una razón razonable («el cerebro
      concentra omega-3»); lo que decía de verdad es que la ficha que yo
      acababa de rellenar tenía datos de otro animal.

### `Laringe de vacuno` — RESUELTO el 7 de septiembre

Estaba en la categoría **Hueso carnoso** con **66 mg de calcio**. Los
huesos carnosos de verdad traen entre 1.250 y 1.810. No era un error de
dato: la laringe es cartílago, no hueso.

Se decidió moverla a **`Extras`**: bloqueada por tejido tiroideo desde el
6 de septiembre (`TIROIDES_EXCLUIR`), nunca puede aportar hueso a ningún
menú, así que la categoría antigua solo servía para disparar dos avisos
ya conocidos en `auditar_catalogo.py`. 0 referencias en
`catalogo_menus.json` (comprobado), así que no afecta a los menús
precalculados.

### Qué alimentos faltan, con evidencia

El cuello de botella medido, contando lo que queda al excluir especies:

| Alergias | Carne | Hueso | **Vísceras** | **Hígado** |
|---|---|---|---|---|
| 0 | 25 | 10 | 10 | 4 |
| 3 | 11 | 6 | **2** | **2** |
| 5 | 6 | 5 | **2** | **2** |

Las vísceras y el hígado son lo que deja a un perro alérgico sin menú — es
exactamente lo que medimos que bloqueaba al adulto con tres alergias. Y la
causa es la variedad de especies, no el número de alimentos:

- **Vísceras** (categoría "Vísceras", no hígado): **sigue siendo solo
  cordero, ternera y vaca** (bazo, páncreas, cerebro, pulmón, riñón, timo).
  Faltan pollo, pavo, conejo, pato y cerdo enteros — esto no ha cambiado.
- **Hígado**: ⚠️ **CORREGIDO 7 de septiembre — esta lista estaba
  desactualizada.** Ya existen hígado de pollo, pavo, pato, cordero,
  conejo y vaca (verificado contra el catálogo real, no de memoria).
  **Solo falta hígado de cerdo.**

- [x] **Corazón y molleja de pollo y de pavo — YA ESTÁN**, y este punto
      estaba desactualizado igual que lo estuvo el del hígado. Existen los
      cuatro (más corazón de conejo, de cordero y de vaca), solo que en
      **Carne muscular** y no en Vísceras, y eso es a propósito y está
      razonado en `accesibles.py`: el criterio no es "de dónde sale" sino
      **si el órgano SEGREGA algo**. La molleja tritura, el corazón bombea,
      la lengua mueve: ninguno segrega, así que son músculo. Solo el pulmón
      se quedó en Vísceras, y por prudencia, porque ahí las fuentes no
      coinciden.
- [x] **Vísceras secretoras de ave: NO EXISTEN, comprobado el 7 de
      septiembre en las tres bases.** Se buscó una por una en BEDCA, CIQUAL
      y el volcado completo de USDA SR Legacy: de pollo, pavo, pato, oca y
      conejo **solo hay hígado, corazón y molleja**. Ni bazo, ni páncreas,
      ni riñón, ni timo, ni cerebro de ninguna de esas especies, en ninguna
      de las tres. No es un hueco de datos que se pueda llenar buscando
      mejor: esos órganos no se separan ni se venden, así que nadie los ha
      analizado. `accesibles.py` ya lo decía desde el 5 de agosto
      ("Confirmado que NO existen datos fiables de bazo/páncreas de pollo,
      pavo ni conejo") y ahora está verificado contra las tres fuentes.
### Buscado el 8 de septiembre: ¿hay algún estudio con vísceras de ave?

Sí hay literatura, pero **ninguna sirve para hacer una ficha del catálogo**,
y conviene que quede escrito para no volver a buscarlo cada vez.

Lo mejor que existe, con diferencia, es **Seong, Cho, Park, Kang, Park,
Moon & Ba (2015), «Characterization of Chicken By-products by Mean of
Proximate and Nutritional Compositions», *Food Science of Animal Resources*
35(2):179-188, doi 10.5851/kosfa.2015.35.2.179**. Analiza OCHO despojos de
pollo — corazón, **pulmón**, hígado, molleja, ciego, buche, intestino
delgado y duodeno — con proximal, diez minerales (Na, K, Ca, Mg, P, Fe, Zn,
Mn, Cu, Cr), seis vitaminas (A, B1, B2, B3, B5, B6), diecisiete aminoácidos
y el perfil de ácidos grasos.

**Y aun así no cierra el problema**, por dos motivos:

1. **No trae bazo, páncreas, riñón ni timo de ave**, que son justo las
   piezas que faltan. Trae pulmón, que sí sería una víscera nueva de una
   especie nueva — es lo único aprovechable de todo lo que hay publicado.
2. **Le faltan seis de los 41 que mide el motor**: vitamina D, vitamina E,
   B12, folato, colina y yodo. Con esos seis en `sin_dato`, y siendo la
   vitamina D y el yodo dos de los cinco topes duros de seguridad crónica,
   un pulmón de pollo entraría al catálogo ciego justo donde más duele.

El resto de lo publicado es peor: el estudio de metales en órganos de pollo
(Sci. Total Environ. 1999) da once metales y fósforo y **ni una vitamina**;
las vísceras de oca (Kokoszyński et al., *Foods* 2025) son otra vez hígado,
molleja y corazón —que ya tenemos— con proximal y diez minerales, sin
vitaminas, sin aminoácidos y sin ácidos grasos. Y una revisión reciente
(*Edible Offal as a Valuable Source of Nutrients in the Diet*, 2024) lo dice
con todas las letras: la información sobre despojos de ave es la más escasa
de todas.

**Conclusión, y es la misma a la que llegó `accesibles.py` el 5 de agosto
por otro camino**: no es que no se haya buscado bien. Es que esos órganos no
se separan ni se venden, así que nadie los ha analizado con la profundidad
que necesita una ficha. Lo único con recorrido real es **el pulmón de pollo
del estudio coreano**, y aun ese entraría con seis huecos, dos de ellos de
seguridad. Decidir si compensa es una decisión, no un dato que falte.

- [ ] **Queda entonces el problema de verdad, y no se arregla con datos**:
      la categoría Vísceras solo tiene DOS especies —bovino (ternera/vaca,
      que para `exclusiones.py` son la misma) y ovino— y es un pilar
      obligatorio con un mínimo del 2 %. Un perro alérgico a las dos se
      queda sin ninguna, y lo único que puede hacer el motor es bajar un
      peldaño de la escalera de relajación y decirlo. Las salidas son de
      producto, no de catálogo: (a) admitir el cerdo, que sí tiene bazo,
      páncreas, riñón y cerebro publicados en las tres bases —hoy queda
      fuera y además el TVT Merkblatt 181 bloquea el cerdo crudo—, o (b)
      aceptar que con esas dos alergias el menú va sin víscera y decirlo
      claro. Es una decisión, no un dato que falte.
- [ ] ⚠️ **DECISIÓN TUYA: el timo y el pulmón «de ternera» tampoco son de
      ternera, y aquí NO es cosmético.** Encontrado el 7 de septiembre al
      barrer todas las fichas «de ternera» contra las dos fichas de USDA
      (vaca y ternera) después de descubrir lo del cerebro:

      | ficha | coincide con VACA | con TERNERA |
      |---|---|---|
      | `Timo de ternera` | **11 de 11** | 0 de 11 |
      | `Pulmón de ternera` | **10 de 11** | 2 de 11 |
      | `Riñón de ternera` | 1 de 11 | 2 de 11 → se queda como está |
      | `Lengua de ternera` | 0 | 0 → viene de otra fuente, no de USDA |

      **Y la diferencia es enorme, no un decimal.** El timo:

      | | catálogo | vaca (FDC 170194) | ternera (FDC 172542) |
      |---|---|---|---|
      | energía | 236 | **236** | 101 |
      | grasa | 20,35 | **20,35** | 3,07 |
      | proteína | 12,17 | **12,18** | 17,21 |

      Si alguien lee «timo de ternera» y compra mollejas de ternera —que es
      lo que se vende en España— está dando un alimento con **la séptima
      parte de la grasa y menos de la mitad de las calorías** que el menú
      creía. Eso descuadra la ración de verdad, no es una etiqueta.

      **Las dos salidas son válidas y la decisión no es de datos:**
      1. **Renombrar a `Timo de vaca` y `Pulmón de vaca`**, como ya se hizo
         con el bazo y el páncreas en agosto. Los datos se quedan como
         están, que son correctos. Cuesta: 27 + 72 referencias en
         `catalogo_menus.json` (renombrado consistente, los menús siguen
         siendo válidos y `_garantizar_verificado` los revisa igual).
      2. **Dejar el nombre y cambiar los datos** a los de ternera (FDC
         172542 y 174361), porque las mollejas de ternera son lo que la
         gente encuentra en la carnicería. Cuesta: dos fichas rehechas, y
         los menús precalculados que las lleven cambian de perfil.

      La 1 es más fiel al dato; la 2 es más fiel a lo que se compra. No la
      tomo yo.
- [ ] **Hígado de cerdo**: única pieza que falta en esa categoría. Fuera de
      esta ronda a propósito — el 7 de septiembre se decidió no meter nada
      de cerdo.

Los pescados (20) no se ven afectados por las alergias a mamíferos, y por
eso la escalera de relajación funciona: casi siempre queda pescado.

## 5-quater. Quién consigue los datos y quién los implementa

**Regla, establecida el 21 de agosto después de saltármela.** El asistente
rellenó el timo de ternera y los testículos de cordero con valores que
había buscado él en espejos de USDA, sin poder abrir la ficha original.
Luego los marcó como «sin verificar», lo cual no arregla nada: el motor
los usa igual, así que un número dudoso pesa lo mismo que uno bueno. Solo
hay dos estados honestos: **verificado, o hueco declarado**. Se revirtió.

| Le toca al asistente | Le toca a una persona |
|---|---|
| Manipular y reestructurar lo que ya está en el JSON | **Conseguir valores de alimentos nuevos** |
| Detectar incoherencias entre alimentos | Sacarlos de BEDCA, CIQUAL o USDA |
| Comparar contra los rangos de FEDIAF | Valores de hueso: **solo Köber et al. 2017** |
| Programar la lógica que usa esos valores | Requisitos por patología: guías clínicas |

Lo que sí puede hacer el asistente con las tablas: la auditoría contra el
PDF de FEDIAF (161/161) es leer la fuente primaria que se le dio, y la
conversión de la vitamina E sale de la tabla de bioequivalencia de la
página 63 de ese mismo PDF — **d-α-tocoferol 1 mg = 1,49 UI**, de donde
1 UI = 0,671 mg. Eso es comparar contra FEDIAF, no inventar datos.

### La premisa de esa regla caducó, y así queda (7 de septiembre)

Lo que hacía falta que decidiera una persona no era «tocar el catálogo»:
era que el asistente **no podía abrir la ficha original** y tiraba de
buscadores y espejos, que redondean y no coinciden entre sí. Eso ya no es
cierto. Las tres fuentes de `Bases.md` se leen enteras desde una sesión:

| Fuente | Cómo se lee | Qué publica y qué no |
|---|---|---|
| **BEDCA** (primaria) | Su servicio público (`bedca.net/bdpub/procquery.php`, XML) | Macros, minerales **y yodo**. Ácidos grasos uno a uno **solo en algunas fichas**. **Ni un aminoácido, ni colina** |
| **CIQUAL** | La tabla 2020 entera, un `.xls` de 3,6 MB, en local | Macros, minerales, yodo **y todos los ácidos grasos**, ficha por ficha. **Ningún aminoácido** |
| **USDA** | El volcado oficial de SR Legacy, un `.zip` de 6 MB, en local | Todo, **incluidos los 12 aminoácidos y la colina**. **No publica yodo** |

Dos cosas que salieron de leerlas de verdad y que conviene no volver a
aprender:

1. **Ninguna base tiene los 41 nutrientes.** BEDCA tiene yodo pero ni un
   aminoácido; USDA tiene los aminoácidos pero no el yodo; CIQUAL tiene los
   ácidos grasos pero tampoco aminoácidos. Una ficha completa **hay que
   armarla con las tres**, y los huecos del catálogo están, casi todos,
   justo donde ninguna llegaba. No son fallos de copia.
2. **BEDCA distingue «midieron 0» de «no hay cifra», y esa distinción se
   pierde al volcarla a una tabla.** Cada celda lleva un `value_type`: `AR`
   con un 0 es un cero medido; `TR` con la celda vacía es que no hay
   número. Al pasarlo a un CSV el `TR` vacío se convierte en 0 y ya nadie
   sabe que no era una medida. Seis de los huecos cerrados el 7 de
   septiembre (tiamina de la calabaza, vitE de pera, calabacín y nabo…)
   son exactamente eso, y hoy se resuelven mirando el `value_type`.

**Y se midió cuánto de bien está copiado el catálogo, porque la pregunta se
hizo en voz alta.** De las 12 fichas que citan un FDC de USDA que se puede
abrir y confirmar que es el mismo alimento, en las cinco donde la ficha
**entera** sale de ese registro —molleja de pollo, molleja de pavo, hígado
de cordero, timo de ternera, hígado de pato— coinciden **153 de 156 celdas,
el 98,1 %**, y tres de las cinco al decimal. La copia y la conversión de
unidades están bien hechas. De las 52 celdas cerradas ese día, **ninguna
era un número mal copiado: las 52 eran ceros**.

Lo que **no** ha cambiado: un valor que la fuente no publica sigue sin
inventarse, y una discrepancia con un valor YA declarado **no se corrige
sola** — eso es corregir, no rellenar, y lo decide una persona (ver las dos
del cerebro de ternera y el araquidónico del pavo, arriba).

### `DATOS_QUE_FALTAN.md`

⚠️ **CORREGIDO el 8 de septiembre**: aquí ponía «Generado por
`auditar_catalogo.py`: 57 alimentos y 431 valores». Lo primero es falso —
**ningún código escribe ese archivo**, la auditoría encuentra los huecos
pero el documento se mantiene a mano — y por eso lo segundo también se
quedó viejo: seguía pidiendo datos de los seis alimentos que salieron del
catálogo el 27 de agosto (los testículos de cordero, las dos harinas de
hueso, el Kelp, y los aceites de salmón de Pets Purest y Brit Care).
Pedir datos de un alimento retirado manda a una persona a buscar un número
que, aunque lo encuentre, no se puede usar. Limpiado: hoy son
**53 alimentos y 330 valores** por
conseguir, cada uno con su unidad y una casilla vacía. Está pensado para
llevarlo a BEDCA o CIQUAL y rellenarlo, y entonces sí pasárselo al
asistente para que lo inserte con el formato correcto.

Prioridad, por lo que desbloquea:
1. Los seis pescados con EPA/DHA sin dato — el **boquerón** el primero,
   que es pescado azul contado como si no tuviera omega-3.
2. Las seis vísceras (timo, testículos, bazo de vaca, páncreas de vaca,
   bazo de cordero, cerebro de ternera) — son la categoría que deja sin
   menú a los perros con alergias.

## 6. Catálogo corregido contra USDA/BEDCA (6 de septiembre)

**Hecho, con permiso expreso**: 23 fichas, 86 celdas, aplicadas desde
`CORRECCIONES_CATALOGO.csv` (repositorio `canislab-fuentes`) — solo las
filas `CORREGIR` con cifra confirmada contra un FDC de USDA o una ficha de
BEDCA/FEN, nunca las `VERIFICAR` (indicios sin número cerrado). Cada celda
se comprobó contra el valor que ya había en el JSON antes de sustituir:
86/86 coincidieron. Detalle completo en el commit `c69758c`.

Los más graves: Albahaca (7 minerales eran de deshidratada, no fresca —
zinc +619%), Hígado de pollo (cobre +815%, vitA +236%), Semilla de sésamo
(calcio −85%, era sésamo pelado no entero), Dorada (la ficha de BEDCA no
cuadraba consigo misma: agua+proteína+grasa sumaban 106 g/100g), y 5
pechugas/muslos de pollo y pavo con errores de escala en vitamina A.

**Abierto, sin cifra disponible**: al bajar la grasa de la Dorada, su
DHA/EPA — de la misma fuente "de piscifactoría" que la grasa ya corregida,
ya documentado en su propio `nota_datos` desde antes — quedan sumando
1,97 g de ácidos grasos contra 1 g de grasa total. Falta una cifra de EPA/
DHA de dorada SALVAGE para cerrarlo. `auditar_catalogo.py` lo señala con
`[GRASOS]` a propósito, sin silenciarlo (whitelisted en el BLOQUE 19).

El linoleico de la Semilla de sésamo sigue en 0 — es un hueco real (el
sésamo es de los alimentos más ricos en omega-6 que existen), pero
`CORRECCIONES_CATALOGO.csv` no traía cifra para esa celda, así que no se
inventó ninguna.

## 7. Legumbres en cardiopatía — ¿conviene añadirlas al catálogo?

**Pregunta del 6 de septiembre. Respuesta: no, por ahora, y el motivo es
más matizado de lo que parece.**

El borrador de 47 patologías (`canislab-fuentes/TRABAJO_RAWKU/code/
patologias.json`, perfil `dcm_asociada_a_dieta`) ya trae la respuesta
investigada:

> «Causalidad NO establecida; mecanismo abierto (hipótesis actual:
> fosfolipidosis, no taurina). Asociación real y reproducible. La FDA dejó
> de publicar actualizaciones en 2024 sin cerrar el caso. **UNA BARF
> CONVENCIONAL NO ESTÁ IMPLICADA en ningún estudio**: el patrón de riesgo
> es "legumbre sustituyendo al cereal" en pienso seco. Solo aplicar la
> bandera si el motor formula con legumbres como fuente calórica
> principal.»

Y además: «El señalamiento es específico del GUISANTE. La lenteja y la
soja NO están implicadas del mismo modo (Quilliam 2023).»

**Por qué no añadirlas de todas formas, ya que el riesgo parece acotado**:
1. La causalidad sigue sin establecerse — es una asociación epidemiológica
   con mecanismo abierto, en una enfermedad potencialmente mortal (DCM).
2. El patrón de riesgo (legumbre reemplazando al cereal como fuente
   calórica principal) es estructuralmente un problema de **pienso seco**:
   una ración BARF nunca sustituye cereal por legumbre porque nunca lleva
   cereal como fuente calórica en primer lugar — las proporciones BARF
   (carne/hueso/víscera como base, verdura al 10-25%) hacen que una
   legumbre nunca pudiera llegar a ser "fuente calórica principal" aunque
   se añadiera.
3. No hay ninguna necesidad nutricional que las legumbres cubran y que hoy
   falte — no aparecen en ningún hueco de `DATOS_QUE_FALTAN.md` ni en
   ninguna prioridad de catálogo.
4. El caso de la FDA sigue abierto (sin cerrar en 2024): mientras tanto,
   no hay urgencia real que justifique asumir aunque sea un riesgo
   pequeño y mal entendido, en una enfermedad cardiaca.

**Si algún día se decide añadir alguna**, la lenteja o la soja (no
implicadas por Quilliam 2023) son las candidatas más seguras — nunca el
guisante, que es el único señalado. Y aun así, con las proporciones BARF,
la bandera de nivel B del borrador (`legumbres: {no_como_fuente_
principal}`) casi nunca llegaría a activarse por diseño.

## 8. Reconciliar las 11 patologías de producción contra el borrador de 47

**Empezado el 6 de septiembre.** El borrador (`canislab-fuentes/
TRABAJO_RAWKU/code/patologias.json`, versión 0.1, marcado explícitamente
«NADA DE ESTO ESTA VERIFICADO») estructura por **estadio clínico**
(`erc_iris_1` a `_4`, `mmvd_acvim_a` a `_d`…) mientras que producción
tenía una entrada plana por enfermedad. Es un cambio de **modelo de
datos**, no solo de cifras, y reconciliar las 47 de golpe es su propio
proyecto — pero dos piezas ya tenían fuente sólida y se implementaron:

**Cardiopatía, con estadio ACVIM (`cardiopatia_b1/_b2/_c/_d`).** Antes
había una sola entrada con sodio a 900 mg/1000kcal, documentada en su
propio `por_que` como «se usa el estadio B2 porque la app no pregunta el
estadio». Ahora, si el estadio se conoce, hay cuatro entradas:
- **B1**: sin restricción — Keene et al. 2019 (ACVIM consensus, JVIM
  33:1127-1140): «no drug or dietary treatment is recommended».
- **B2**: 900 mg/1000kcal (rango 800-990, escala moderna por estadio).
- **C**: 790 mg/1000kcal (rango 500-790, extremo menos restrictivo:
  restringir de más activa el eje renina-angiotensina-aldosterona).
- **D**: 480 mg/1000kcal (<500, con margen sobre el mínimo FEDIAF adulto
  de 290).
La entrada genérica `cardiopatia` (900, sin estadio) se queda igual, para
quien no sepa el estadio de su perro. `auditar_patologias.py`: todo
cuadra. La app (canislab-web) tiene que empezar a preguntar el estadio y
mandar `cardiopatia_b1`/`_b2`/`_c`/`_d` en vez de `cardiopatia` a secas —
mientras no lo haga, nada cambia para nadie.

**Renal, con proteinuria (`renal_proteinuria`).** El consenso ACVIM 2013
pide bajar la proteína un 25-50% **respecto a la ingesta previa** cuando
el UPC (cociente proteína:creatinina en orina) supera 0,5 — no es una
cifra absoluta. Como Rawku no captura la ingesta previa del perro al
generar un menú nuevo, **no se aplica ningún recorte automático**: la
nueva entrada es solo informativa (explica el porqué y remite al
veterinario), pensada para combinarse con `renal` sin tocar el tope de
fósforo. Aplicar el recorte real necesitaría encadenar `/analizar` (que sí
lee la dieta actual) antes de `/menu/v2` — eso es trabajo de producto, no
solo de motor.

**Actualizado el 6-7 de septiembre, con SACN5 5ª ed. completo ya
disponible**: se verificaron y añadieron 23 patologías más (de 16 a 39 en
`patologias.json`), cada una cifra a cifra contra SACN5 + NRC 2006 +
FEDIAF, nunca de memoria ni del borrador sin comprobar — ver el detalle
completo, con las tablas y capítulos citados, en §10 más abajo.

**Actualizado el 7 de septiembre — la renal SÍ se partió, pero en DOS, no
en 4**: se buscó la fuente primaria que citaba el borrador para los 4
estadios IRIS ("IRIS 2023 + ACVN") y no existe en `canislab-fuentes` —
solo hay `IRIS_Guidelines/IRIS_CKD_Staging_Modified_2026.pdf`, que es
la guía de ESTADIAJE de verdad (creatinina/SDMA, sustadiaje por
proteinuria y presión) y no contiene ni un solo número de dieta. Con lo
que SÍ hay (SACN5 cap.37, Tabla 37-9 y 37-10), la única distinción
verificable es de DOS grupos, no cuatro: la restricción de fósforo tiene
evidencia real (Grade III) específicamente en IRIS 3-4, donde además la
proteína (35-50 g/1000kcal) ya cae bajo el mínimo FEDIAF; en IRIS 1-2 la
evidencia es más débil (Grade IV) y no hay un número de fósforo propio.
Se añadió `renal_avanzada` (bloqueada, mismo fósforo que `renal` pero con
la proteína documentada por debajo del mínimo) y se dejó `renal` tal cual
para 1-2 o cuando no se conoce el estadio. Partir en los 4 estadios
exactos del borrador significaría inventar tres números sin fuente —
exactamente lo que la regla de este proyecto prohíbe.

También se cruzó `cardiopatia_b2/_c/_d` contra SACN5 cap.36 Tabla 36-4
(sodio por clase ISACHC): confirma el PATRÓN de restringir más cuanto más
avanzada la enfermedad, pero no se cambiaron los números — SACN5 usa la
clasificación ISACHC (I/II/III), no la ACVIM (A-D) de esta app, y el
consenso ACVIM 2019 (Keene et al.) ya citado es la fuente más moderna y
específica para MMVD.

**Cerrado el 7 de septiembre — el resto de la Tabla 36-4, releída con la
página del PDF renderizada en vez del texto plano** (que salía con las
columnas descolocadas: `poppler-utils` no estaba instalado en esta sesión
y se reinstaló para esto). Con la tabla limpia (página 746 del libro):
fósforo 0,2-0,7%MS, potasio ≥0,4%MS, magnesio ≥0,06%MS, taurina ≥0,1%MS,
L-carnitina ≥0,02%MS (todo en perro). Contrastado contra los mínimos de
FEDIAF ya en vigor:

- **Fósforo** (500-1750 mg/1000kcal a 4000kcal/kgMS): el mínimo FEDIAF
  (1160) ya cae dentro del rango. Nada que restringir.
- **Potasio** (≥1000): el mínimo FEDIAF (1450) ya lo supera. Nada que
  añadir.
- **Magnesio** (≥150): el mínimo FEDIAF (200) ya lo supera. Nada que
  añadir.
- **Cloruro** (1,5× el sodio, para las tres clases): no es un número
  suelto, es una proporción sobre el sodio que ya se restringe — el
  mínimo FEDIAF (430) queda por debajo de 1,5× cualquiera de los topes
  de sodio ya aplicados (480 a 900), así que tampoco hace falta un tope
  nuevo.
- **Taurina y L-carnitina** (≥250 y ≥50 mg/1000kcal): ⚠️ **CERRADO el 7 de
  septiembre — los dos huecos que bloqueaban esto ya no existen.** Cuando
  se escribió este párrafo faltaban dos cosas: (a) el dato de taurina y
  L-carnitina en el catálogo, y (b) el mecanismo de suelos por patología.
  Las dos se resolvieron el mismo día: (a) las 159 fichas ya tienen
  `taurina`/`lcarnitina` (Spitze et al. 2003, principalmente; `sin_dato`
  donde no hay fuente fiable — nunca un número inventado), y (b) el
  mecanismo de suelos se construyó y se usó primero en `artrosis` y
  `dermatosis_zinc`. Con las dos piezas puestas, se activó el suelo real
  de `dcm_taurina_respondedora` (taurina 250, L-carnitina 50 mg/1000kcal,
  misma fuente SACN5 cap.36 Tabla 36-4 de aquí arriba), probado contra el
  solver y verificado también en `_garantizar_verificado()` — no se quedó
  en aviso.

**Conclusión: los 5 estadios MMVD completos ya no tienen ningún hueco
pendiente.** El reparto de macros "más allá del sodio" que proponía el
borrador está cubierto en su totalidad: los mínimos de FEDIAF vigentes
para fósforo/potasio/magnesio/cloruro, y desde el 7 de septiembre también
taurina y L-carnitina con su propio suelo activado.

`alergia_alimentaria`, `cachorro_raza_grande`,
`gestacion_lactancia_con_patologia`, `mucocele_biliar` y la partición de
`pancreatitis` en dos se dejaron fuera a propósito — el porqué de cada
una está en `VETERINARIOS.md` §12-bis, en la sección «Lo que falta para
que esta tabla esté completa».

## 9. `campos nuevos que hoy no existen en la app` — qué falta y por qué

Tres piezas de la auditoría del 6 de septiembre necesitan un campo de
entrada que **hoy no existe en ningún sitio** — ni en el schema de la API
(los `Peticion*` de `main.py`), ni en la ficha del perro de `canislab-web`:

- **El 10% de calorías para premios/complementos** (Hervera, Clinnutrivet
  17). No hay ningún concepto de "premio" o "snack" en la API: no hay
  campo que preguntar cuántas kcal vienen de fuera de la ración. Añadirlo
  necesita una pantalla nueva en la app y una decisión de producto sobre
  dónde se pregunta, no solo un parámetro nuevo en el backend.

  ⚠️ **Y ya van CUATRO fuentes** (actualizado el 9 de septiembre de 2026, de
  leer capítulos enteros de SACN5): FEDIAF §4.1, SACN5 cap.17, SACN5 cap.1
  (*«Intakes of treats and nutritional supplements should be recorded»*) y
  SACN5 cap.47, que es la única que da **la misma cifra que Hervera**:
  *«Generally, feeding excessive amounts (**>10 % of the total food intake** on
  a volume or calorie basis) of any treat is not recommended»*. El 10 % ya no
  es de una sola fuente. Lo que sigue sin existir es el campo.
- **La reformulación de adelgazamiento** (proteína≥25%MS, grasa≤9%MS,
  L-carnitina, fibra — Tabla 27-4 de SACN5). Hoy adelgazar solo baja las
  kcal (vía RER en `der.py`); no hay un perfil de macros dedicado. Además
  de una decisión de producto, la L-carnitina ni siquiera es un
  nutriente que el catálogo trackee — haría falta añadir una columna
  nueva a las 159 fichas antes de poder exigirla.
- El UPC renal y el estadio ACVIM cardíaco (arriba) **ya no necesitan
  campo nuevo en el motor** — se resolvieron reutilizando el mecanismo
  existente de `patologias` (una lista de nombres): en vez de un
  parámetro numérico nuevo, la app manda una clave de patología más
  específica (`cardiopatia_c` en vez de `cardiopatia`). Lo que falta es
  solo la pantalla en `canislab-web` que pregunte el estadio/UPC y elija
  la clave correcta — cero cambios de backend adicionales.

## 10. La ronda SACN5 (6-7 de septiembre): 23 patologías más, verificadas
     capítulo a capítulo

Con los 70 capítulos de SACN5 5ª ed. ya disponibles en
`canislab-fuentes/sacn5/cap*.txt` (subidos en un PR aparte de ese repo),
se hizo lo que pedía el punto anterior: cada patología nueva, verificada
cifra a cifra contra el capítulo que le toca, **nunca contra el borrador
sin comprobar ni de memoria**. `patologias.json` pasó de 16 a 39 entradas.
`auditar_patologias.py` (BLOQUE 36) y la batería completa, en verde.

**Refinamientos a las 16 que ya existían** (mismo número, fuente cruzada
con SACN5 para confirmarlo o para documentar un conflicto):
- `hepatopatia`: SACN5 cap.68 Tabla 68-8 da cobre ≤5 mg/kg de materia seca
  = 1,25 mg/1000kcal — casi idéntico al objetivo terapéutico ya citado
  (1,2, de Center 2026). Dos fuentes, veinte años de diferencia, mismo
  número.
- `cistina`: se corrigió un dato FALSO que llevaba desde antes de esta
  ronda — `motivo_no_formulable` decía que el catálogo no tenía
  aminograma de metionina/cistina, cuando SÍ lo tiene desde el 28 de
  agosto (94 de 159 fichas). El motivo real de bloqueo (pH urinario +
  objetivo por debajo del mínimo FEDIAF) seguía siendo correcto, solo el
  dato de "no hay aminograma" era falso y quedó reescrito.
- `estruvita` y `urato`: cruzados con SACN5 cap.43 y cap.39 — ambos
  confirman, con una fuente distinta a la ya citada, que la restricción
  real es también de proteína completa por debajo del mínimo FEDIAF, no
  solo del nutriente específico (pH, purinas) que ya se citaba.
- `oxalato`: SACN5 cap.40 (2010) todavía recomienda BAJAR el calcio
  (0,4-0,7% MS) — lo contrario de lo que ya se seguía (Today's Veterinary
  Practice 2025, que dice que bajar el calcio empeora el oxalato al
  aumentar su absorción intestinal). Es un conflicto de fuentes real,
  documentado en el propio JSON: se mantiene la posición más reciente
  porque tiene el mecanismo mejor descrito.

**23 patologías nuevas, con topes numéricos reales donde el número era
alcanzable con el catálogo** (`hiperlipidemia` grasa≤30, `obesidad`
grasa≤30 — SACN5 pide 22,5 pero NO es alcanzable con el catálogo real, se
probó contra el solver: 27 falla 0/5 intentos, 28 resuelve 5/5, se dejó en
30 con margen —, `ple_linfangiectasia` grasa≤37,5, `insuficiencia_
pancreatica_exocrina` grasa≤37,5) o bloqueadas por Razón A cuando el
objetivo terapéutico cae bajo el mínimo FEDIAF (`shunt_sin_encefalopatia`
proteína 37,5-50, `encefalopatia_hepatica` proteína 25-37,5, ambas de
SACN5 cap.68 Tabla 68-8). El resto (`cardiopatia_a`, `dcm_taurina_
respondedora`, `dcm_asociada_a_dieta`, `fracaso_renal_agudo`,
`enteropatia_cronica`, `riesgo_gdv`, `disfuncion_cognitiva`,
`raza_predispuesta_cobre`, `dermatitis_atopica`,
`epilepsia_idiopatica`, `mielopatia_degenerativa`, `cushing`, `addison`,
`cancer_soporte`, `inmunosupresion`) son informativas, sin tope numérico,
porque en cada caso o (a) el nutriente clave (taurina, L-carnitina, fibra,
MCT) no está entre los 41 que mide el motor, o (b) el propio SACN5 dice
que el tratamiento es farmacológico o de manejo, no dietético (Cushing,
Addison, GDV, epilepsia). La tabla completa con la razón de cada una está
en `VETERINARIOS.md` §12-bis.

**Actualizado el 7 de septiembre — `artrosis` y `dermatosis_zinc` ya NO
son informativas sin tope.** El motor solo sabía poner TECHOS por
patología (el `min()` de todas las activas); artrosis y dermatosis_zinc
necesitaban lo contrario, un SUELO más alto que el de FEDIAF, y eso no
existía. Se añadió `min_por_1000kcal` en `motor/motor_completo.py`
(espejo exacto de `max_por_1000kcal`, combinando con `max()` en vez de
`min()` porque un suelo reforzado solo puede EXIGIR más, nunca menos), un
campo nuevo `suelos_por_1000kcal` en `patologias.json`, y la comprobación
espejo en `auditar_patologias.py` (una formulable no puede pedir un suelo
por ENCIMA del máximo FEDIAF, igual que un tope no puede pedir MENOS del
mínimo). Con esto:
- `artrosis`: EPA+DHA ≥1,0 g/1000kcal (SACN5 cap.34 Tabla 34-2: EPA
  0,4-1,1% MS: se usa el extremo bajo, ya varias veces el suelo general
  de 0,11).
- `dermatosis_zinc`: zinc ≥25 mg/1000kcal (SACN5 cap.32 Tabla 32-1: zinc
  100-200 mg/kgMS; el extremo bajo, sobre el mínimo general de FEDIAF de
  20,8).

Los dos probados contra el solver real (varios pesos/etapas) antes de
darlos por buenos — mismo criterio que ya se aplicó a `obesidad`. ⚠️
**ACTUALIZADO 7 de septiembre**: ya sí es posible para
`dcm_taurina_respondedora` — taurina y L-carnitina se añadieron al
catálogo y al MAPA (43 nutrientes) el mismo día, y el suelo (250/50
mg/1000kcal) ya está activado y probado contra el solver, documentado en
la sección de MMVD, arriba.

**Un hallazgo de honestidad de datos que merece quedar escrito**: el
primer intento de `obesidad` usó literalmente el número de SACN5 (≤9% MS
= 22,5 g/1000kcal) sin probarlo contra el solver. No resolvía —ni en 40
segundos de reintentos—, porque una comida de verdad no puede bajar tanto
la grasa y seguir llegando a los mínimos de EFA y micronutrientes con las
kcal que quedan (un pienso sí puede, con premezcla vitamínica sintética
que no lleva grasa). Se probó en escalón (25, 26, 27, 28...) hasta
encontrar el punto real donde el catálogo empieza a resolver, y se dejó
ahí con margen. La lección: un número de un libro de texto no es
automáticamente un tope viable con comida de verdad, y hay que probarlo
contra el solver antes de darlo por bueno — exactamente lo que dice la
regla 1 del `CLAUDE.md`, aplicada a un tope nuevo, no solo al menú final.

**Actualizado el 7 de septiembre (2) — `hiperlipidemia` ya tiene suelo de
fibra, y era el único de los tres candidatos que lo admitía.** Al cerrar
el hueco de datos de fibra en el catálogo (159/159 fichas, ver más arriba)
se comprobó si de verdad se podía enganchar a alguna de las tres
patologías que la pedían -- diabetes, hiperlipidemia, colitis
(`enteropatia_cronica`) -- y la respuesta fue distinta para cada una,
leyendo SACN5 capítulo a capítulo y no de memoria:

- **`hiperlipidemia`: SÍ.** Cap.28 «Disorders of Lipid Metabolism» da un
  número único y accionable: «fiber levels of at least 10% DM are
  recommended for dogs» → 25 g/1000kcal a 4000kcal/kgMS. Se añadió como
  `suelos_por_1000kcal.fibra`, probado contra el solver real junto con el
  tope de grasa ya existente (30 g/1000kcal) en el BLOQUE 13 de
  `pruebas_completas.py`, tres tamaños de perro.
- **`diabetes`: NO.** Cap.29 «Endocrine Disorders», Tabla 29-3, da un
  rango de comida comercial (7-18% MS) pero el propio texto dice
  literalmente «although an ideal fiber content has not been
  established» -- la fuente se niega a dar un objetivo, así que poner uno
  sería inventarlo. Queda como aviso informativo, igual que antes.
- **`enteropatia_cronica` (colitis): NO, y por un motivo distinto.**
  Cap.57 «Inflammatory Bowel Disease», Tabla 57-1, da DOS enfoques
  válidos y opuestos: ≤5% MS ("highly digestible") o 7-15% MS
  ("increased-fiber", para normalizar motilidad) según el caso. Un suelo
  único aquí acertaría para un perro y se equivocaría para el otro -- no
  es un hueco de dato, es que la propia guía dice "depende".

Esto solo fue posible porque `verificar.MAPA` y `requerimientos_v2_final.json`
ya tienen la fila `Fibra` (seis campos a "-", ningún requisito nuevo para
un perro sano) -- ver el párrafo de arriba (5, punto 3) para el porqué de
esa fila y las dos comprobaciones que `auditar_fediaf.py` le añadió para
que no repita el fallo del 25 de agosto.

## 11. Fascetti & Delaney, 2ª ed. completo (7 de septiembre): tres verificaciones

Llegaron los 21 capítulos que faltaban (`canislab-fuentes` PR#1, extraídos
por Cowork desde Perlego). Verificado punto por punto, contra el libro y
no contra el resumen previo:

**RER y factor de enfermedad — confirmado que NO hace falta tocar nada.**
El método americano multiplica el RER por un factor de 1,1 a 2,3 según
gravedad (Remillard & Thatcher 1989, citada íntegra en Fascetti cap.3).
Esta app nunca ha aplicado ninguno — `der.py` usa el método europeo
(Thes 2015) para adultos y FEDIAF para crecimiento/gestación/lactancia,
sin ningún parámetro de enfermedad en absoluto. Comprobado que NO es un
hueco: es lo que la propia fuente recomienda — *"it seems reasonable to
target energy requirements for most sick or injured dogs and cats
initially at RER"* y *"it should rarely be necessary to feed injured or
ill cats and dogs above the predicted energy requirement for a healthy
animal at maintenance"*. Documentado ahora explícitamente en `der.py`
(antes no decía nada, que se podía leer como "no se pensó" en vez de "se
decidió no hacerlo").

**El hallazgo que sí requería un cambio.** La misma fuente, literal:
*"weight loss is never a goal during treatment and recovery from trauma
and critical illness"*. Comprobado: `obesidad` se podía combinar con una
patología aguda o crítica (`fracaso_renal_agudo`, `encefalopatia_
hepatica`, `cancer_soporte`, `inmunosupresion`, `pancreatitis`) sin
ningún aviso — el mecanismo `aviso_si_ademas` (nuevo, ver arriba junto a
los suelos) lo cubre ahora, sourced a este mismo capítulo.

**La pregunta de la vitamina E, ya cerrada.** El informe de Fascetti
dejaba pendiente confirmar la unidad de la columna de vitamina E del
catálogo. Verificado contra la Tabla VII-14 de FEDIAF (la fuente
primaria, no de memoria): nuestro ×0,67 (UI→mg) es la equivalencia de
tocoferol NATURAL (d-α-tocoferol, 1mg = 1,49 UI), correcta para
alimentos frescos. El 1 IU = 1 mg que cita Fascetti es la del acetato
SINTÉTICO (dl-α-tocoferil acetato), la forma de los premezclados de
suplemento — no la que llevan las fichas de carne, pescado o víscera del
catálogo. Confirmación, no bug; ya se aplicaba bien en
`auditar_fediaf.py`.

Las dos correcciones de cita que trae el mismo informe (§3.6: el rango
real es 1,1-2,3 y no 1,1-1,5, y la fuente no dice que los factores estén
"deprecados") son sobre la documentación interna de `canislab-fuentes`,
no sobre nada implementado aquí — no había ningún factor de enfermedad
en el código al que esa cita pudiera aplicar.

## 12. Ratio vitamina E / AGPI de NRC 2006 — real, no implementado, no urgente (7 de septiembre)

Leyendo NRC 2006 buscando el máximo de fósforo (punto 4 de arriba) apareció
otra frase, en otro sitio del mismo libro, que no tiene nada que ver con el
fósforo: *"A ratio of at least 0.6 mg of tocopherol per gram of PUFA in the
diet should be maintained"* (línea 21885 de `nrc2006.txt`). Es un requisito
real, cuantificable, y esta app no lo comprueba en ningún sitio hoy: no está
en `verificar.MAPA`, no está en el solver, no está en `seguridad.py`.

Antes de proponer añadirlo se probó contra el solver de verdad, en vez de
razonar solo con la fórmula: ~30 menús variados (raza pequeña y gigante,
cachorro sin pescado, artrosis con aceite de pescado forzado, adulto
estándar...), calculando en cada uno mg de vitamina E ÷ g de AGPI totales
(linoleico + linolénico + araquidónico + EPA + DHA). El peor ratio
encontrado fue ~1,19 — por encima de 0,6 en todos los casos reales, aunque
tres de los aceites de salmón del catálogo tengan vitE=0 en `sin_dato` por
separado (con AGPI alto): el resto del menú siempre aporta suficiente
vitamina E para compensar.

**Conclusión: el ratio existe y es real, pero hoy no aprieta ningún menú de
Rawku.** No se ha implementado como restricción nueva porque añadir un
suelo global sin verlo fallar nunca en la práctica es el tipo de cambio que
esta sesión decidió evitar (ver la advertencia de arriba sobre organizar el
git primero) — queda aquí escrito para que quien siga sepa que la fuente
existe y el número exacto, por si el catálogo cambia lo suficiente (más
aceites muy concentrados en AGPI con vitE=0, por ejemplo) como para que
empiece a importar. Si se implementa, va como suelo genérico en
`topes_de_patologias()` o como comprobación transversal en
`_garantizar_verificado()`, no como tope de una patología concreta: NRC lo
da para todos los perros, no para un diagnóstico.



## 13. `renal + pancreatitis` no da menú en ningún tamaño (8 de septiembre)

Encontrado por el BLOQUE 50, que cruza cinco perfiles de perro con doce
combinaciones de patologías. De los sesenta cruces, **el único que no da menú
en ninguno de los cinco tamaños** (3, 12, 30, 55 y 20 kg) es
`renal + pancreatitis`.

⚠️ **RESUELTO EL 8 DE SEPTIEMBRE DE 2026, y no como se esperaba.** Lo que
sigue debajo describe el estado hasta esa fecha; se deja porque el diagnóstico
era correcto y el desenlace enseña algo.

**No había incompatibilidad clínica entre las dos patologías: había un número
que no era el de la fuente que manda.** La grasa de pancreatitis estaba en 20
g/1000 kcal (Merck) cuando por la regla del propio proyecto —FEDIAF, y donde
FEDIAF no llega, SACN5— debía ser **37,5** (Tabla 67-3). Con 37,5, `renal +
pancreatitis` **sale verde**: peldaño 5, grasa 37,5 y fósforo 1198,8. Ver
`PATOLOGIAS.md` §1.5 y `PREGUNTAS_ABIERTAS.md` P-01, ya cerrada.

**Y el mensaje también se arregló**, por otro camino: desde ese día el motor
nombra los dos límites que chocan con su fuente en vez de pedir que se quite
una restricción (BLOQUE 52).

---

**Era coherente con los topes**, no un fallo del solver: la combinación dejaba
fósforo ≤ 1200 mg/1000 kcal (con el mínimo de FEDIAF en 1160 — un 3,4 % de
sitio), grasa ≤ 20 g/1000 kcal y proteína ≤ 75 g/1000 kcal **a la vez**, y
con esa ventana no hay ración BARF que cuadre. La escalera de relajación se
recorre entera y tampoco.

**Lo que sí es un problema es lo que se le dice.** El mensaje que recibe es
el del tutor: «No existe ninguna combinación de alimentos accesibles que
cumpla todos los requisitos para este perro, ni siquiera soltando las
proporciones habituales del BARF. Quita alguna restricción y vuelve a
probar». Un veterinario no puede quitar una de las dos enfermedades que tiene
el perro.

**Las preguntas, que son de nutrición y no de código:**

1. ¿Un perro renal **y** pancreático es un caso real que haya que cubrir, o
   es una dieta de prescripción comercial y punto?
2. Si hay que cubrirlo, ¿cuál de los tres topes cede, y con qué fuente?
   (La grasa de pancreatitis, 20 g/1000 kcal, es el extremo bajo de un rango
   que Merck da como «less than 20» y SACN5 Tabla 67-3 sitúa en 37,5-75.)
3. Y mientras tanto: ¿qué se le dice? Lo mínimo sería nombrar los topes en
   juego y su margen, en vez de pedirle que quite restricciones.

Mismo caso, más suave, en `mastín 55 kg + renal_proteinuria + artrosis`: sale
unas veces sí y otras no según lo cargada que vaya la máquina — ahí es el
presupuesto de tiempo del solver, no la nutrición.

---

## 14. Lo que abrió la cuarta pasada (8 de septiembre, tarde)

Detalle completo en `VERIFICACION_FILA_A_FILA.md` §cuarta pasada. Aquí solo lo
que queda **por hacer**, con dueño.

### 14.1 · Una fuente concentrada de EPA+DHA en el catálogo — **falta un dato**

La Tabla 30-5 pide para el cáncer **omega-3 > 5 % MS = 12,5 g/1000 kcal** y el
catálogo no llega: el techo medido está entre **11,5 y 12,0**. La fuente más
concentrada que hay es el aceite de linaza (62,5 g/1000 kcal), que además es ALA
y no EPA/DHA.

SACN5 enseña en su propia Tabla 30-6 que sí se alcanza: la Hill's n/d —el
alimento de los ensayos de Ogilvie en linfoma canino— trae **7,29 % MS**.

**Lo que falta es un producto real con su etiqueta**: un concentrado de EPA+DHA
(aceite de pescado de alta concentración) con los gramos por 100 g y la dosis
máxima del fabricante. Va en `DATOS_QUE_FALTAN.md` — **no lo rellena el
asistente**.

Mientras tanto la cifra está escrita en `patologias.json` bajo
`limites_escritos_que_el_solver_no_aplica`, con la medida y el motivo, y el menú
de cáncer lo dice en un aviso: lleva todo el omega-3 que se puede dar y no llega
a lo que pide la literatura.

### 14.2 · El ratio omega-6:omega-3 y el techo de carbohidrato — **falta motor**

La misma Tabla 30-5 pide «an omega-6:omega-3 ratio approximating 1:1» y «NFE
≤25 % DM».

- El **ratio**: ✅ **el motor está, desde el 10 de septiembre.** Se hizo por el
  otro extremo —el `ratio_ca_p` de los urolitos de calcio, que llevaba dos días
  escrito con `aplicado_por_el_solver: false`— y salió genérico: el bloque
  `ratios` de `patologias.json` admite cualquier par de nutrientes. **Para el
  omega-6:omega-3 ya no falta código: falta el número**, y ahí las fuentes van de
  <1:1 (artrosis) a 7:1 (renal). Es PREGUNTA 40 y la decide quien firma.
- El **NFE** no se puede calcular con lo que hay: haría falta el extracto libre
  de nitrógeno de cada ficha. Una ración BARF con la verdura topada al 10 % queda
  muy por debajo del 25 % por construcción, así que el riesgo real es bajo.

### 14.3 · El fósforo del perro sano — ✅ RESUELTO el mismo día, aplicándolo

> **⚠️ Esto se escribió como una pregunta para el nutricionista y no lo era.**
> «Si lo dice el manual, aplícalo» — y el manual lo dice. Se midió, cabe, y está
> aplicado desde el 8 de septiembre por la noche: `recomendaciones_libro.json`,
> `motor/recomendaciones.py`, BLOQUE 57, y `DECISIONES.md` **D-15** con las
> medidas. Los cuatro pesos probados salen en el peldaño 0 y en verde, y el de
> 3 kg pasa de ámbar a verde. Se deja el texto de abajo porque explica de dónde
> venía el problema, que sigue siendo lo que hay que entender.

Esta es la que más pesa de las tres, y sale de comparar tablas que hasta ahora no
se habían mirado juntas:

| Tabla | Para quién | Fósforo | Sodio |
|---|---|---|---|
| 13-3 | Perro adulto joven **sano** | 0,4-0,8 % MS = **1000-2000** mg/1000 kcal | 0,2-0,4 % = 500-1000 |
| 14-2 | Perro maduro **sano** | 0,3-0,7 % MS = **750-1750** | 0,15-0,4 % = 375-1000 |
| 34-2 | Artrosis | 0,3-0,7 % = **750-1750** (aplicado: techo 1750) | 0,2-0,4 % (aplicado: 1000) |
| 31-3 | Reacción adversa al alimento | 0,4-0,8 % = **1000-2000** (aplicado: 2000) | 0,2-0,4 % (aplicado: 1000) |

Las dos filas de patología **son las del perro sano**, repetidas. Sus notas lo
dicen: la 34-2 porque «dogs with osteoarthritis are often in age groups at risk
for kidney and/or heart disease», la 31-3 porque «phosphorus and sodium are
considered key nutritional factors for apparently healthy adult dogs… for
purposes of ameliorating or slowing the progression of subclinical kidney
disease».

Y el número que importa: **una ración BARF normal de este motor ronda los 4.000
mg de fósforo por 1000 kcal** (medido: 3.933 a 4.115 en menús verdes de adulto
sano). El doble del techo que SACN5 recomienda a **cualquier** perro adulto.

⚠️ **CORREGIDO EL 9 DE SEPTIEMBRE.** Aquí ponía «FEDIAF no pone máximo de
fósforo», y es falso: **sí lo pone en adulto, 4,00 g/1000 kcal** (Tabla III-3b,
«Adult: 4.00 (N)», nota h, y el texto de la sección 3.3.1). Se borró por error el
7 de septiembre y se devolvió la noche del 8. Lo que no tiene máximo es el
**crecimiento**.

Así que el problema no era que faltara el techo: es que **la ración BARF salía
pegada al máximo de seguridad de FEDIAF** y SACN5 recomienda la mitad. Antes de
aplicar el techo del libro, el motor solo apretaba el fósforo por debajo de 4.000
en las patologías cuya tabla lo repite, y eso sí era incoherente: **el mismo
perro pasaba de 4.000 a 1.750 por marcar «artrosis», y de 4.000 a 2.000 por
marcar «alergia alimentaria», sin que ninguna de las dos cosas tenga que ver con
el fósforo.**

(Lo que sí sigue en pie del párrafo viejo: NRC 2006 dice que no hay datos para
fijar un **SUL toxicológico** y Dobenecker 2021 que no se puede definir un
no-effect-level. Eso es otra cosa que el máximo **nutricional**, que sí existe.)

Las tres salidas posibles, y **ninguna la decide el asistente**:

1. **Dejarlo como está**: FEDIAF manda en el perro sano, y la patología aplica lo
   que dice su tabla. Es lo que hay hoy.
2. **Quitar esas dos filas de las patologías**, por ser recomendaciones del perro
   sano y no de la enfermedad. Deja artrosis y reacción adversa sin techo de
   fósforo.
3. **Aplicar el techo a todos los adultos**. Es el cambio grande: afecta a todos
   los menús, y hay que medir antes cuántos siguen saliendo.

Es decisión de nutrición. Apuntada también en `PENDIENTE_DECISIONES.md`.

### 14.4 · Al toy de 1,5 kg le cuesta más sacar menú con el techo de fósforo — ✅ **NO le pasa al dueño; queda un coste de tiempo**

> **⚠️ REMEDIDO EL 10 DE SEPTIEMBRE, POR LA VÍA DE LA API, QUE ES LA QUE USA LA
> APP.** El mismo toy de 1,5 kg y DER 200, 20 peticiones:
>
> | Presupuesto | Sin menú | En qué peldaño sale |
> |---|---|---|
> | 24 s (lo normal) | **0 de 20** | los 20 en **estricto** |
> | 3 s (imitando a Render lento) | **0 de 20** | 7 estrictos, 13 un peldaño más abajo, **y lo dice** |
>
> O sea que **hoy el dueño tiene su menú siempre**, y cuando se baja de peldaño
> se avisa, que es la regla 5. Lo arregló el reparto de tiempo del 8 de
> septiembre (`tiempo_de_un_intento()`: ninguna llamada se lleva más del 40 % del
> presupuesto, así que siempre queda para bajar de peldaño). Lo que queda escrito
> abajo es el **coste**: al perro pequeño le cuesta más, y con el presupuesto
> apretado paga bajando de peldaño.


Desde que existe el techo del perro adulto sano (2000 mg/1000 kcal, `DECISIONES.md`
D-15), **al perro más pequeño le cuesta más sacar menú**. Medido, toy de 1,5 kg
con DER 200, peldaño 0, dos suplementos, una semilla por intento y 1 s de solver:

```
con el techo .....  12 sin menú de 30
sin el techo .....   0 sin menú de 30
```

**El menú existe en las 30**: reintentar con otra semilla lo encuentra, y con 30
segundos de reloj salen las 30 (ver la corrección de abajo). En Render el
presupuesto de tiempo es real, así que el coste se paga en segundos o en bajar de
peldaño. En los perros de 3, 10, 22 y 40 kg no pasa: los cuatro salen en el
peldaño 0 a la primera.

### ⚠️ CORREGIDO EL 10 DE SEPTIEMBRE: LA CAUSA ESCRITA AQUÍ ERA FALSA

Aquí ponía: *«`elegir_alimentos` sortea candidatos por categoría sin saber qué
límites hay puestos»*, y de ahí salía un plan —sesgar el sorteo hacia los huesos
de mejor Ca:P— que **habría sido trabajo tirado**, porque arreglaba una función
que no interviene.

**`elegir_alimentos` no está en el camino vivo.** De todo `motor/modos.py`, el
motor importa **una sola cosa**: el diccionario `CUANTOS_MAX`
(`motor_completo.py:531`). Ni `elegir_alimentos`, ni `cambiar`, ni `quitar`, ni
`anadir` los llama nadie —ni la API, ni la batería—: los endpoints
`/menu/cambiar`, `/menu/quitar` y `/menu/anadir` tienen su propia implementación
en `main.py`. **No hay sorteo de candidatos**: `resolver()` recibe *todos* los
accesibles de cada categoría y **es el MILP quien elige**.

Lo único aleatorio es un ruido pequeño en el **objetivo** (0 a 0,4 sobre el coste
de usar cada alimento, más la penalización del pescado la mitad de las veces), y
**un objetivo no puede volver infactible un problema factible**: solo cambia por
dónde busca el solver y, por tanto, **cuánto tarda**.

**La causa real es el `time_limit`.** Medido el 10 de septiembre, el mismo toy de
1,5 kg con DER 200, peldaño 0, dos suplementos, 30 semillas fijas:

| `time_limit` | Sin menú | Semillas que fallan |
|---|---|---|
| 1 s | **11 de 30** | 0, 4, 7, 9, 12, 13, 19, 23… |
| 5 s | **6 de 30** | 4, 12, 23, 25, 27, 29 |
| **30 s** | **0 de 30** | ninguna |

Con 30 segundos **no falla ninguna**, así que las 30 son factibles y lo que
faltaba era tiempo para encontrar la primera solución entera. Y no es que se
tirara una solución ya encontrada: eso se arregló el 29 de agosto (se acepta el
incumbente cuando salta el `time_limit`). Aquí HiGHS **no llega a tener
ninguna** en un segundo.

**Y por eso el arreglo bueno ya estaba puesto, en otro sitio.**
`tiempo_de_un_intento()` (8 de septiembre) impide que una sola llamada se lleve
más del 40 % del presupuesto, así que siempre queda tiempo para **bajar de
peldaño** — y con cuatro huecos de suplemento el motor puede meter cáscara de
huevo (Ca:P de 370:1, o sea calcio sin fósforo) y el techo deja de apretar. Es
exactamente para lo que existe la escalera, y es lo que hace que la medida por la
vía de la API dé 0 sin menú de 20 arriba. El diagnóstico correcto llevaba desde
ese día escrito en el docstring de esa función; lo que no se actualizó fue este
punto.

**Y queda una pregunta pequeña de limpieza**: `motor/modos.py` son 190 líneas de
las que se usa un diccionario. Código muerto que *parece* vivo es justo lo que
mandó a este punto a diagnosticar la función equivocada.

⚠️ **Medido y descartado como atajo**: subir `max_suplementos` a 3 **no** lo
arregla (5 sin menú de 10 en la misma prueba). Más huecos hacen el MILP más
grande, no más fácil. El problema es qué entra en el sorteo, no cuántos huecos
hay.

---

## La disponibilidad del calcio del hueso molido no está medida (9 de septiembre de 2026)

Fascetti & Delaney 2ª ed., cap.8, literal:

> *«Grinding bones may help reduce the risk of trauma and obstruction, but **the
> availability of the calcium from these sources is unknown**.»*

**Qué usamos hoy.** El calcio del hueso carnoso sale de **Köber 2017** (abstract
del ESVCN 2017, Tabla 1: Ca, P y Ca:P de 15 huesos y cartílagos), que es la
fuente que `Bases.md` fija para el hueso precisamente porque BEDCA no lo trae. Y
el motor lo cuenta como calcio **disponible**, igual que el de cualquier otra
ficha.

**Qué falta.** Köber da el CONTENIDO. La frase de arriba dice que la ABSORCIÓN
del hueso molido no está cuantificada. No es un error de dato: es una
incertidumbre conocida sobre un número que decide menús — y el calcio es de los
que más deciden, porque tiene mínimo, máximo, la nota b de raza grande y el ratio
Ca:P encima.

**Lo que juega a favor, y por qué esto no es urgente.** El cap.10 del mismo libro
(Hazewinkel, que es quien hizo los estudios de absorción de calcio con trazador
⁴⁵Ca en gran danés y poodle) dice:

> *«The source of calcium – **bone meal, fresh bones**, or dairy products – **does
> not make a lot of difference**; it is the amount of calcium eaten and absorbed
> that counts.»*

O sea que las dos frases no se contradicen: la primera dice que para hueso
**molido** no hay cifra publicada; la segunda que en la práctica la fuente del
calcio importa poco frente a la cantidad. Y la absorción que sí está medida —27 %
en poodle a las 24 semanas, 53 % en beagle, 60 % en gran danés; ~13-20 % en
adulto— es de dietas normales, con el calcio de sales o de harina de hueso.

**Lo que NO se puede hacer**: inventarse un factor de disponibilidad para el
hueso. Sería exactamente lo que `CERRADO.md` prohíbe.

**Lo que sí se puede, si algún día hace falta**: buscar si hay balance de calcio
publicado con ración BARF real (no con sales), que es lo que cerraría esto. Y
mientras tanto, tener presente que **el margen de error del calcio del hueso es
mayor que el de los demás nutrientes del catálogo**, lo que es un argumento más
para no formular pegados al techo — ver `HALLAZGOS_LECTURA_FUENTES.md` §F-1, que
es justo lo que estamos haciendo hoy en los cachorros de raza grande.

---

## El techo de Ca:P del cachorro de raza grande: SACN5 dice 1,5 y aplicamos 1,6 (9 de septiembre de 2026)

**No es urgente y no está dando menús malos hoy, pero es una cifra de una
fuente que no se aplica, así que se escribe en vez de olvidarse.**

Al transcribir la Tabla 17-1 de SACN5 para los techos de calcio y fósforo del
cachorro (ver `DECISIONES.md` D-16) salió una tercera fila de la misma tabla:

| | cachorro <25 kg de adulto | cachorro >25 kg de adulto |
|---|---|---|
| Ca:P ratio (Tabla 17-1) | 1:1 a **1,8**:1 | 1:1 a **1,5**:1 |
| Ca:P ratio (Tabla 33-5) | — | 1,1:1 a 2:1, «the lower end of range is preferred» |

Y lo que aplica el motor hoy es la nota b de FEDIAF: **1,6** para el cachorro
de más de **15 kg** de adulto, 1,8 para el resto.

Hay dos discrepancias, y ninguna es un error de nadie:

1. **El umbral.** FEDIAF corta en 15 kg y SACN5 en 25. Son dos poblaciones
   distintas (la nota b de FEDIAF, y la enfermedad ortopédica del desarrollo de
   SACN5), así que los dos números pueden ser correctos a la vez.
2. **El número.** Para el cachorro de más de 25 kg, SACN5 pide 1,5 y FEDIAF
   1,6. La propia Tabla 33-5 del mismo libro dice 1,1-2:1 con el matiz de que
   se prefiere la parte baja, así que **el libro no se pone de acuerdo consigo
   mismo**: la 17-1 da 1,5 y la 33-5 da 2,0.

**Medido, para saber si esto cuesta algo:** los cachorros de raza grande que
saca el motor hoy salen con el ratio entre **1,03 y 1,29** (labrador temprano
1,03, gran danés tardío 1,11, labrador tardío 1,23, pastor alemán 1,26). O sea
que **aplicar 1,5 hoy no cambiaría ni un menú** — y por eso mismo no corre
prisa.

**Lo que haría falta para aplicarlo:** `recomendaciones.py` sabe de techos por
nutriente, no de ratios. El ratio Ca:P se aplica hoy desde
`requerimientos_v2_final.json` (`maxRatioCaP` en la fila
`Calcio_LateGrowth_RazaGrande`) y desde `_ratio_cap_raza_grande_roto` en
`main.py`, y ahí no se puede meter un número de SACN5: ese fichero **es** la
Tabla III-3b de FEDIAF y `auditar_fediaf.py` lo audita celda a celda. Haría
falta un mecanismo de ratio en `recomendaciones_libro.json`, con su fila en el
solver y su espejo en el filtro final.

**Pregunta abierta para el nutricionista** (no la decide el asistente): con la
17-1 diciendo 1,5 y la 33-5 diciendo 2,0 para el mismo perro, ¿cuál manda? Lo
seguro sería 1,5, y hoy sale gratis.

---

## La lactosa del yogur griego no está medida, y SACN5 da el umbral (9 de septiembre de 2026)

**De leer entero el capítulo 55 de SACN5.** Recuadro 55-3, literal: *«In one
study, **dogs developed diarrhea while consuming more than 1 g of lactose/kg body
weight**»*. El perro adulto tiene poca lactasa; lo que no se hidroliza llega al
colon y arrastra agua.

**Lo que hay en el catálogo:** un lácteo, «Yogur griego», en la categoría Extras.

**Lo medido hoy:** de los 216 menús del catálogo regenerado, **0 lo usan**. Hoy
no aprieta a nadie.

**Por qué sigue siendo un pendiente y no un no-problema:** Extras va **siempre
libre** (regla 5 del `CLAUDE.md`), así que un menú personalizado o una
formulación del veterinario sí puede meterlo, y no hay nada que lo tope por este
motivo. Los cinco topes de seguridad crónica no incluyen la lactosa.

**Por qué no se aplica hoy:** la lactosa **no es uno de los 41 nutrientes** del
catálogo, así que el motor no sabe cuánta lleva la ficha. Aplicarlo pide un dato
nuevo, y los datos del catálogo no los rellena el asistente.

**La cuenta, hecha, para cuando el dato exista:** el yogur griego natural va por
los 3-4 g de lactosa por 100 g. Con 4 g/100 g y el umbral de 1 g/kg, el tope
sale en **25 g de yogur por kg de peso**: 75 g para un perro de 3 kg, 250 g para
uno de 10, 1 kg para uno de 40. Los perros pequeños son los que quedan cerca.

**Lo que falta**, en este orden:
1. La lactosa del «Yogur griego» de BEDCA o USDA, con su fuente, en la ficha
   (`DATOS_QUE_FALTAN.md`).
2. Decidir si es un **tope de seguridad más** (como el mercurio del atún, que
   también se mide por peso del perro) o solo un **aviso**. Es criterio, no
   aritmética: el mercurio se acumula y una diarrea no.

---

## Lo que dejó la relectura íntegra de SACN5, caps. 50 al 70 (11 de septiembre de 2026)

De leer enteros los capítulos de digestivo, hígado y farmacología. **El cotejo
tabla por tabla salió limpio**: las Tablas 57-1, 58-1, 60-1, 62-1, 63-3, 64-2,
65-1, 66-1 y 67-3 están aplicadas enteras en sus ocho patologías digestivas, y
la 68-8 en seis de sus diez filas. Lo que queda son estos tres puntos. Ninguno
está aplicado; los tres son decisión tuya.

### 1 · El TECHO de hierro de la hepatopatía, que hoy solo usa el suelo

`hepatopatia` aplica `hierro` como **suelo** de 20 mg/1000 kcal, tomando el
extremo bajo de la Tabla 68-8 («*Iron (mg/kg) 80 to 140*»). El extremo alto no
se aplica, y **no es el borde de un rango cualquiera: es un techo con mecanismo
escrito**. El capítulo lo desarrolla en su propia sección:

> *«Iron is a potent catalyst of oxidative processes (Fenton reaction) and
> iron-associated hepatic injury may involve lipid peroxidation of membranes and
> damage to organelles»*

> *«Iron levels of 80 to 140 mg/kg DM meet the dietary allowance without
> providing excessive intake. This range is recommended for patients with liver
> disease»*

Y remata con *«Injectable or oral supplements containing iron should be avoided
in these patients»*.

**Por qué llama la atención:** para el potasio de la enteropatía crónica se tomó
la decisión **contraria** y está escrita — la Tabla 57-1 daba «0.8 to 1.1 %» y
se aplicó el **techo**, con el motivo de que el riesgo es el exceso. Aquí el
riesgo que la fuente describe también es el exceso (acumulación hepática) y se
aplicó el suelo.

**MEDIDO** sobre los 216 menús del catálogo regenerado, recalculando el hierro
de cada menú guardado con `valor_nutriente` y dividiendo por su DER:

| | mg de hierro / 1000 kcal |
|---|---|
| mínimo | 18,4 |
| mediana | 25,6 |
| máximo | 37,4 |
| por encima del techo de 35 | **3 de 216 (1,4 %)** |

Los tres que se pasan son `Gigante_GestanteTardia` (37,4),
`Mini_CachorroCrecimiento#3` (36,8) y `Toy_CachorroJoven` (35,4) — **los tres de
crecimiento o gestación**, que es donde sube el mínimo de hierro. En adulto no
se pasa ninguno. `hepatopatia` es además `formulable: false` y
`formulable_por_profesional: true`, así que solo entra por la puerta del
veterinario. La ventana quedaría en **20-35** y el margen del profesional en
10,4 (mínimo FEDIAF) a 35. El máximo de FEDIAF, 170,45, queda muy por encima.

**Decisión:** aplicarlo o dejarlo escrito sin aplicar. Cabe holgado.

### 2 · La dosis de omega-3 de la enteropatía crónica, que es del TEXTO y no de la tabla

El cap.57 la da y la Tabla 57-1 no, que es justo por lo que no la encontró el
trabajo de transcribir tablas:

> *«A reasonable starting dose estimated from human and animal trials is
> approximately 175 mg (range 50 to 300 mg) omega-3 fatty acids/kg body
> weight/day»*

Para un perro de 22 kg son 3,85 g de omega-3 al día. **No está en
`patologias.json` ni en su bloque de límites escritos sin aplicar.**

⚠️ Y el propio capítulo dice por qué no se puede aplicar tal cual: *«To date,
there are no published therapeutic trials investigating the efficacy of omega-3
fatty acid supplementation in dogs or cats with IBD»* y *«there is no
well-established effective dose for dogs and cats»*. Es el mismo caso que el
omega-3 del cáncer y el de la artrosis, que ya viven en
`limites_escritos_que_el_solver_no_aplica` con su medida. **Su sitio es ese**, y
hoy no está escrito en ninguna parte. El hueco es de registro, no de motor.

### 3 · La B12 de la insuficiencia pancreática exocrina

El aviso de `enteropatia_cronica` lleva la advertencia de la vitamina B12 con su
pauta. El de `insuficiencia_pancreatica_exocrina` **no la lleva**, teniendo la
cifra más alta de las dos:

> *«Reports have identified cobalamin deficiency in 82% of dogs»*

y, en la misma frase tras la cita del estudio, 60 % de los gatos. Además:
*«Cobalamin deficiency has been associated with poor outcomes in canine EPI»*.
No es un número del motor: es una frase que le falta a un aviso.

### Y una que ya tenía dueño

La **lactosa** salió otra vez al releer el cap.55, y ya está recogida más arriba
en este mismo fichero, en la sección «La lactosa del yogur griego…», con la
cuenta hecha y los dos pasos que faltan. No se duplica.

---

## ⚠️ Las kcal del hueso se calculan con unos factores que NRC excluye para el hueso (11 de septiembre de 2026)

De leer entero el capítulo 3 de NRC 2006. **Es el hallazgo más gordo de esta
lectura y no se puede resolver con lo que hay en el repo**, así que se escribe
entero aquí.

### Qué dice la fuente

NRC explica de dónde salen los factores de Atwater (4 kcal/g de proteína, 9 de
grasa, 4 de hidratos) y para qué alimentos valen, nombrando la excepción:

> *«The resulting Atwater factors of 4 for protein, 9 for fat, and 4 kcal·g–1 for
> carbohydrate (nitrogen-free extract; NFE) still work amazingly well for
> ingredients in homemade diets for dogs: meat, offal **(except bones and bone
> meal)**, poultry, fish, highly purified starch products, milk products, and
> even chocolate»*

Y la Tabla 3-1 pone la misma frontera en su columna «Application».

⚠️ **Y hay que decir la otra mitad, porque juega a favor**: NRC *recomienda*
Atwater justo para lo que hace Rawku — *«For dogs, Atwater factors are still
recommended for use for table food if no other data are available»*. El hueso es
una excepción **dentro** de una recomendación que por lo demás encaja.

### Qué hace el motor, comprobado

Las nueve fichas de «Hueso carnoso» tienen su `energia` **exactamente igual** a
4×proteína + 9×grasa, hasta el decimal, y sus notas lo dicen: «Energia calculada
de sus macros».

| Ficha | `energia` | 4×prot + 9×grasa |
|---|---|---|
| Carcasa de pollo | 240,2 | 240,2 |
| Cuello de pavo | 132,4 | 132,4 |
| Cuello de pato | 318,8 | 318,8 |
| Carcasa de conejo | 158,5 | 158,5 |
| Costillas de cordero | 185,9 | 185,9 |
| Carcasa de pato | 229,9 | 229,9 |

Y ese `energia` **no es decorativo**: es la fila de energía del MILP
(`motor_completo.py`) y el divisor con el que `verificar.py` calcula las kcal del
menú.

### Cuánto pesa, medido sobre los 216 menús del catálogo

| | % de las kcal del menú que vienen del hueso carnoso |
|---|---|
| mínimo | 16,6 |
| mediana | **34,8** |
| máximo | 56,7 |
| menús sin hueso | **0 de 216** |

O sea que **en el menú mediano, un tercio del denominador de todos los límites
del motor** —los 43 de FEDIAF, los cinco de seguridad crónica, los 12 del libro y
los 75 de patología, que van todos «por 1000 kcal»— sale del único ingrediente
que la fuente nombra como excepción.

### La DIRECCIÓN se sabe, y el TAMAÑO está ACOTADO Y MEDIDO (11 de septiembre, tarde)

Esto decía «ni el tamaño ni la dirección». Ya no: los dos se pueden deducir de lo
que la propia fuente dice, sin inventarse ninguna cifra.

**La dirección.** Los factores de Atwater llevan dentro una digestibilidad
supuesta, y NRC la escribe: *«Atwater factors include a digestibility of 98
percent for carbohydrate, 96 percent for fat, and 90 percent for protein»*. La
proteína del hueso carnoso es en buena parte colágeno. Si el colágeno se digiere
**por debajo** del 90 %, la energía real es **menor** que la calculada. Y como
todos los límites del motor van «por 1000 kcal», un denominador inflado hace que
el menú esté **más concentrado** de lo que el motor cree. Así que el riesgo no
está repartido: está **todo en los TECHOS**, y ninguno en los mínimos, donde el
error juega a favor.

**El tamaño.** El factor de proteína de Atwater es `(5,7 GE − 1,25 de pérdida
urinaria) × digestibilidad`, que a 0,90 da exactamente el 4,005 de Atwater. Con
otra digestibilidad sale otro factor, y basta con ver cuánta de la energía del
menú pasa por ahí. Medido sobre los 216 menús del catálogo:

| | % de las kcal del menú |
|---|---|
| que vienen del hueso carnoso (todo) | 19,1 · **mediana 36,8** · 56,7 |
| que vienen de la **proteína** del hueso | 7,8 · **mediana 13,1** · 30,2 |

La segunda fila es la que importa, porque el factor que está en duda es el de la
proteína. Aunque el colágeno se digiriera al **60 %** en vez del 90 % —que es un
supuesto deliberadamente brutal, no una medida—, las kcal del menú bajarían entre
un **2,6 % y un 10,1 %, mediana 4,4 %**.

**Y qué mueve eso en la práctica.** Resolviendo seis menús reales con la API y
recalculando su fósforo sobre las kcal corregidas:

| Perro | kcal | Fósforo hoy | Con la proteína del hueso al 75 % | Al 60 % |
|---|---|---|---|---|
| Adulto 3 kg | 325 | 1969 | 2019 | **2070** |
| Adulto 10 kg | 699 | 1753 | 1785 | 1819 |
| Adulto 22 kg | 1166 | 1610 | 1641 | 1674 |
| Adulto 40 kg | 1698 | 1609 | 1643 | 1678 |
| Senior 28 kg | 1213 | 1633 | 1667 | 1702 |
| Cachorro 25 kg | 1552 | 2616 | 2669 | 2723 |

O sea: **el error existe, va en la dirección mala y es de un dígito por ciento**.
Contra el máximo de FEDIAF (4000 en adulto) no lo acerca ni de lejos. Contra el
**techo del libro (2000)** sí muerde en un caso y solo en uno: el adulto pequeño,
que hoy sale a 1969 y en el supuesto más duro cruzaría a 2070. Es un margen del
1,5 %, así que ese perro ya estaba en el borde por su cuenta.

### Lo que NO se hace, y por qué

**No se corrige la energía de las nueve fichas.** Para corregirla haría falta un
número, y en el repo no hay ninguno:

· **Köber 2017**, que es la fuente de estas fichas (comprobado: sus macros
  coinciden celda a celda), **no da energía**. Solo materia seca, proteína bruta,
  grasa bruta, cenizas, calcio y fósforo.
· ⚠️ **CORREGIDO LA MISMA TARDE: NRC cap.13 SÍ trae energía de un ingrediente CON
  HUESO, y va en la dirección contraria a la que yo supuse.** Lo que escribí aquí
  primero —«NRC cap.13 no trae energía del hueso»— era **falso**, y salió de mirar
  solo la Tabla 13-8 (que es la de fuentes **inorgánicas** de mineral, sin columna
  de energía) y no la **Tabla 13-1**, que es la de análisis proximal y **sí tiene
  columna de EM para el perro**. En ella está *«Meal, with bone, rendered»* (IFN
  5-00-388), con **3,61 kcal/g para el perro**.

  Y lo que dice esa fila desmonta mi hipótesis:

  | | kcal/g |
  |---|---|
  | EM que publica NRC | **3,61** |
  | 4×proteína + 9×grasa, que es lo que hace Rawku | 2,92 (**NRC un 24 % MÁS**) |
  | + 4×ELN, que es como salen las demás filas de esa tabla | 3,37 (**NRC un 7 % MÁS**) |

  **Y el método de la tabla está comprobado**: en las seis filas de ingrediente
  animal SIN hueso, la EM que publica NRC coincide con 4×proteína + 9×grasa +
  4×ELN dentro del **1,3 %** (corazón 1,13 contra 1,13; hígado 1,38 contra 1,38;
  riñón 1,03 contra 1,03; callos 0,94 contra 0,93; pollo con piel 2,53 contra
  2,50; hígado de pollo 1,20 contra 1,20). O sea que la tabla **aplica Atwater al
  ingrediente con hueso**, y le sale un número más alto que el nuestro.

  **Por qué esto cambia la conclusión de arriba, y no un poco.** Yo había deducido
  que si el colágeno se digiere mal la energía real es MENOR y los menús están más
  concentrados de lo que el motor cree. Esta fila no lo apoya: la única EM
  publicada de un ingrediente con hueso es **más alta** que nuestro cálculo, no más
  baja. Y hay un motivo mecánico: **nuestras fichas no llevan el término del ELN**
  que sí lleva el método de NRC.

  **Lo que sigue siendo verdad**: NRC excluye el hueso de Atwater en el cap.3, con
  esas palabras. Lo que ya NO se puede afirmar es la DIRECCIÓN del error. Las dos
  cosas caben, y la tabla de sensibilidad de arriba hay que leerla como una de las
  dos mitades, no como la respuesta.

  **Y lo que sigue faltando es lo mismo**: esa fila es harina de carne y hueso
  **rendida y seca** (94 % de materia seca, 19 % de cenizas, 51 % de proteína), no
  hueso carnoso crudo. La propia tabla avisa de cómo usarla: *«Users should examine
  the standard deviation and N before using the mean value as an estimate of the
  nutritional content of a specific feed ingredient»*.
· **NRC cap.6 no da digestibilidad del colágeno.** Buscado «collagen» en el libro
  entero: sale en el metabolismo de la vitamina C, en la lisina, en el sodio y en
  una frase sobre el triptófano —*«tryptophan may be limiting when corn and
  high-collagen diets are used as protein sources»*—, y en ninguna con un
  coeficiente de digestibilidad.

Poner un 0,75 o un 0,60 porque suena razonable sería exactamente lo que este repo
tiene prohibido: un número con forma de dato bueno que nadie puede rehacer. El
supuesto del 60 % de arriba es una **cota**, y está escrito como cota.

⚠️ **Y NRC dice cuál es el método bueno para este caso**, que no es Atwater ni una
corrección inventada, sino ir por ingrediente: *«Either the energy content of
digestible nutrients (i.e., heat of combustion of nutrient × digestibility) is
summed with the aforementioned subtraction for digestible protein, or ME is taken
directly from the table for each ingredient and summed»*, y añade que *«it has
been used successfully for homemade and semi-purified experimental diets»* — que
es exactamente lo que formula Rawku. Para usarlo hace falta el mismo dato que
falta: la digestibilidad de la proteína del hueso carnoso, o su EM medida.

### Lo que falta, y es DATO, no código

**Una energía metabolizable medida del hueso carnoso crudo, o la digestibilidad
de su proteína.** Va a `DATOS_QUE_FALTAN.md`. Mientras no exista, el motor se
queda como está y esta página dice el tamaño del error, que es lo honesto.

Y si algún día aparece: corregir la energía de las nueve fichas **cambia todos
los menús del catálogo y el DER efectivo de todas las raciones**, así que no se
toca sin la medida y sin regenerar con `regenerar_catalogo.py`.

⚠️ **Nota de honestidad sobre este punto.** En la sesión del 11 de septiembre
afirmé este hallazgo **antes** de haber leído el capítulo, con una cifra
inventada. Eso fue un error y quedó corregido en el momento. Lo de arriba está
leído, citado literal y comprobado contra el catálogo; la medida del 34,8 % se
hizo después de leer, no antes.

---

## ⚠️ La fibra del catálogo y la fibra de las tablas no son la misma fibra (11 de septiembre de 2026)

De leer entero el capítulo 4 de NRC 2006. **Las dos mitades están comprobadas
contra su fuente**, así que esto no es una sospecha.

### Las dos mitades

**Las tablas están en fibra BRUTA.** Ocho patologías del motor ponen un suelo o
un techo de fibra, y las ocho cifras salen de tablas de SACN5. Tres lo dicen con
esas palabras en la propia fila —«Crude fiber ≤5%» (58-1), «Crude fiber ≥8%»
(63-3), «≥7% crude fiber» (64-2)— y el pie de la 63-3 explica por qué las demás
también: *«Crude fiber is the only fiber value readily available for pet
foods»*. El cap.5 del mismo libro dice de dónde viene esa costumbre —*«regulations
require that the maximum amount of crude fiber be listed on the label of all pet
foods»*— y lo que vale ese número: *«Because the crude fiber analysis
underestimates fermentable fiber, it does not accurately represent the total fiber
in a pet food»*.

**El catálogo está en fibra dietética TOTAL.** Dos fichas lo dicen literal en su
propia `nota_datos` —«BEDCA, "Coles de Bruselas" — fibra dietética total 4,3
g/100 g» y la misma frase en el puré de tomate—, y es lo que publican las tres
bases de `Bases.md`. El propio SACN5 lo sitúa en el otro lado: *«This analysis is
used to determine total fiber and is commonly used for measuring fiber content of
human foods»*.

### Cuánto separa a las dos

NRC lo cuantifica: *«The crude fiber method accounts for only 5 to 20 percent of
the total fiber in a food and, as such, underestimates the true DF
concentration»*. Y la Tabla 5-9 de SACN5 lo enseña con las dos columnas al lado,
ingrediente a ingrediente: la proporción va del **0 %** (pectina de manzana, goma
guar, goma arábiga: fibra bruta **cero** con 81-95 % de fibra total) al **82 %**
(celulosa). No es una constante, así que **no hay factor de conversión que
aplicar**.

### Medido

Perro de referencia (20 kg, DER 950, adulto), pidiendo el menú a la API con cada
patología marcada:

| Patología | Límite | Fibra total | En % MS | Fibra bruta real (5-20 %) | Pide la fuente |
|---|---|---|---|---|---|
| Obesidad | suelo 30 | 45,35 | 18,14 % | 0,91 a 3,63 % | 12 % |
| Hiperlipidemia | suelo 25 | 38,88 | 15,55 % | 0,78 a 3,11 % | 10 % |
| Estreñimiento | suelo 17,5 | 26,73 | 10,69 % | 0,53 a 2,14 % | 7 % |
| Diabetes | suelo 17,5 | 25,89 | 10,35 % | 0,52 a 2,07 % | 7 % |
| Intestino irritable | suelo 20 | 20,02 | 8,01 % | 0,40 a 1,60 % | 8 % |
| Flatulencia | techo 12,5 | 0,43 | 0,17 % | 0,01 a 0,03 % | ≤5 % |
| Insuf. pancreática exocrina | techo 12,5 | 2,54 | 1,02 % | 0,05 a 0,20 % | ≤5 % |
| Linfangiectasia (PLE) | techo 12,5 | 2,13 | 0,85 % | 0,04 a 0,17 % | ≤5 % |

**Ninguno de los cinco suelos se cumple en la unidad de su propia fuente**, ni en
el extremo más favorable del rango. Y **los tres techos no aprietan a nadie**: una
ración BARF sale con 0,2-1 % de fibra bruta de materia seca, diez veces por debajo
del techo, así que ahí el error de unidad no le quita el menú a ningún perro.

### Lo que se ha corregido ya

El `por_que` de `intestino_irritable` decía que se usaba la fila de fibra bruta
«porque es la unica que el catalogo sabe medir». **Era falso y está corregido**:
esa nota al pie de SACN5 habla de **piensos**, cuya etiqueta solo declara la
bruta; el catálogo de Rawku es el único de los dos que sí tiene la fibra
dietética total. Y `UNIDADES.md` no decía qué método mide el campo `fibra`;
ahora lo dice.

### Lo que NO se toca, y por qué

**Las ocho cifras se quedan como están.** Para cambiarlas haría falta una de dos
cosas, y ninguna existe:

1. Un factor bruta↔total. NRC da un rango de **cuatro veces** y la Tabla 5-9
   enseña que dentro de ese rango depende del ingrediente, con el **0** para la
   fibra soluble — que es justo la del psyllium del catálogo.
2. Elegir, en la Tabla 63-3, una de sus tres filas en términos de fibra dietética
   (soluble 1-5 %, mixta 5-10 %, insoluble 10-15 %). Pero el propio pie dice que
   eso es **clínico**: *«Any one of the three types of fiber listed at the
   recommended levels can be effective, depending on patient response»*.

### La pregunta para el nutricionista

Los cinco suelos de fibra están escritos en fibra bruta y se comprueban contra
fibra dietética total, así que el perro recibe **bastante menos** fibra bruta de
la que su fuente pide. ¿Se sube el suelo para compensar —y con qué criterio, si
la fuente da un rango de 4×—, se reescriben en la unidad del catálogo usando las
filas de tipo de fibra de la Tabla 63-3, o se dejan como están y se dice en la
pauta?

⚠️ **NRC además desmiente el mecanismo en un caso concreto, el de la diabetes**:
*«No relationship was found between crude fiber content of the diet and blood
glucose or insulin»*, y la explicación es justo esta — *«This was attributed to
the inability of the crude fiber analysis to recover soluble dietary fibers, which
can play a key role in mediating postprandial hyperglycemia»*. O sea que la unidad
en la que está escrito nuestro suelo de diabetes es la que la fuente dice que no
sirve para lo que ese suelo quiere conseguir.

---

## Lo que dejó la lectura íntegra de NRC 2006 (11 de septiembre de 2026)

Los 15 capítulos, con registro en `LECTURA_NRC2006.md`. Cuatro cosas quedan
**medidas y sin aplicar**, y cada una por un motivo distinto.

### 1 · Dos techos que FEDIAF no tiene y que caben de sobra (cap.5)

NRC da para el perro adulto un **límite superior seguro de grasa total de 82,5
g/1000 kcal** («approximately 70 percent ME or 82.5 g per 1,000 kcal ME») y de
**linoleico de 16,3 g/1000 kcal**. FEDIAF pone mínimo de grasa (13,75) y **ningún
máximo**, ni de grasa ni de linoleico.

| | mínimo | mediana | máximo | se pasan |
|---|---|---|---|---|
| Grasa (techo 82,5) | 44,91 | 61,22 | 76,07 | **0 de 36** |
| Linoleico (techo 16,3) | 3,20 | 3,53 | 7,23 | **0 de 36** |

**Cabe sin apretar nada**, que es la misma situación del techo de sodio del perro
sano. Y el de la grasa no es un número arbitrario: sale de un experimento que
**indujo pancreatitis** con unos 92 g/1000 kcal, menos un margen del 10 %.

**Qué falta para aplicarlo**: medirlo con el solver, no solo contra el catálogo
—la lección del 11 de septiembre por la mañana—, y decidir si un techo que hoy no
aprieta a nadie merece entrar. Yo diría que sí, por lo mismo que el sodio: seguirá
ahí el día que el catálogo cambie.

### 2 · Dos techos de vitamina A, y el del cachorro es ocho veces el de FEDIAF (cap.8)

| | NRC | FEDIAF | nuestro máximo |
|---|---|---|---|
| Cachorro y reproductora | **3.750 µg/1000 kcal** | 30.000 | 3.236 (0 de 12) |
| Adulto no reproductor | **16.000 µg/1000 kcal** | 30.000 | 5.052 (0 de 24) |

El del cachorro deja solo un **14 % de margen** sobre nuestro peor menú, así que
este **hay que medirlo con el solver sí o sí** antes de tocarlo: un techo al 86 %
de lo que el motor entrega puede quitarle el menú a un cachorro.

### 3 · ⚠️ La colina se pasa en los 36 menús (cap.8)

NRC: «A presumed safe maximum intake of 2,000 mg choline·kg–1 diet is proposed» =
**500 mg/1000 kcal**. FEDIAF no pone máximo. Nuestros menús: **1.071 a 1.125**, o
sea más del doble, y **36 de 36**.

**No se aplica, y no por comodidad.** Lo que la propia fuente dice de ese número lo
debilita: es un «presumed safe maximum» que sale de donde pararon los estudios
(McKibbin dio 1.500 y 2.000 mg/kg de **suplemento** sin problema), el único trabajo
que vio anemia lo critica NRC en la misma página por no tener controles, nuestra
colina es **de alimento** y no cloruro de colina, y el propio capítulo avisa de que
«dietary requirements for choline are not fixed but will respond to other components
of the diet that are potential methyl donors, particularly methionine» — y una
ración BARF va cargada de metionina.

**La pregunta para el nutricionista**: ¿1.100 mg de colina por 1000 kcal, toda de
alimento y con metionina de sobra, es un problema?

### 4 · ⚠️ Los topes de seguridad deberían APRETARSE en el perro de trabajo (cap.11)

> «safe upper limits (SULs) expressed relative to DM and ME should be decreased
> eightfold in diets intended for sled dogs running in a cold environment and
> halved in diets for working dogs»

Es aritmética: un tope «por 1000 kcal» deja pasar el doble de microgramos a un perro
que come el doble, y para la vitamina D y el yodo lo que hace daño es la cantidad
absoluta. **El motor no lo hace**, y **ya tiene el disparador**: la vitamina E del
perro de trabajo se aplica desde DER efectiva ≥150 kcal/kg^0,75.

| Tope crónico | Hoy | A la mitad | Máximo de FEDIAF | ¿Mordería? |
|---|---|---|---|---|
| Vitamina D | 20 µg | **10** | 14,1875 | **Sí** |
| Yodo | 1.275 µg | **637,5** | 2.750 | **Sí** |
| Selenio | 570 µg | 285 | 142 | No, FEDIAF ya aprieta más |

**Qué falta**: comprobar con el solver que un perro de trabajo sigue teniendo menú
con la vitamina D a 10 µg/1000 kcal. Es el nutriente que más aprieta cuando entra
un multivitamínico, así que no se puede dar por hecho.

⚠️ Y al aplicarlo hay que respetar que la regla de NRC habla de **SULs**, no de las
celdas de la Tabla III-3b: se apretarían los topes crónicos del motor, no los
máximos de FEDIAF.

### Y lo que NRC deja CONFIRMADO, que también cuenta

· El **tope de vitamina D del motor (20 µg/1000 kcal)** es literal de NRC, palabra
  por palabra y en la misma unidad.
· El **tope de yodo (1.275)** es la cifra más alta que NRC documenta como dada sin
  problema, y a 1.400 hubo función tiroidea deprimida en cachorros.
· El **máximo de calcio de crecimiento de FEDIAF (4.500)** y el **de sodio (3.750)**
  coinciden clavados con los SUL que da NRC.
· La **arginina que sube con la proteína** (+0,01 g por g) sale igual en NRC y en la
  Tabla VII-13 de FEDIAF, por caminos distintos.
· El **suelo de taurina de la DCM (250 mg/1000 kcal)** es el mismo número que da NRC
  para dietas bajas en proteína.
· La **densidad de 4.000 kcal/kg MS** con la que este repo convierte sus 110 cifras
  es la que NRC declara en el cap.15.
· Y **once de los doce minerales no tienen techo publicado para el perro**: el hueco
  no es nuestro, es de la literatura.
