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

- [ ] **Contrastar esas cifras con la ficha original de USDA.** Se
      recuperaron de espejos por buscador porque el entorno no tiene
      acceso a `fdc.nal.usda.gov`. Dos valores de los testículos son
      **deducidos, no leídos**, y van marcados como tal: la grasa (del
      balance energético) y el selenio (del 48 % del valor diario que
      publica la fuente, porque no da la cifra absoluta).
- [ ] **El linoleico de la grasa de pollo sigue sin dato**, y esta vez no
      por descuido: USDA no publica un valor diferenciado para ese
      alimento. Importa porque el linoleico **tiene máximo** en cachorros,
      y un hueco contado como cero no lo detectaría.
- [ ] Plantearse que el aviso de datos incompletos no dependa de una lista
      mantenida a mano: un alimento con el 90 % de los valores a cero es
      sospechoso por sí solo, lo declare o no.

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

- [ ] **Conseguir cifras verificadas de EPA/DHA para esos seis pescados.**
      No se rellenaron a ojo a propósito: los valores que devuelve el
      buscador vienen redondeados y no coinciden entre sí, y un dato
      inventado con cara de dato es peor que un hueco declarado. Contarlos
      como cero solo los infravalora (el omega-3 no tiene máximo), así que
      no es peligroso — pero desaprovecha el pescado y mete aceite que
      quizá no hacía falta.
- [ ] **Completar las cuatro vísceras** con la ficha de su fuente, igual
      que se hizo con el timo y los testículos.

### Decisión pendiente: `Laringe de vacuno`

Está en la categoría **Hueso carnoso** con **66 mg de calcio**. Los huesos
carnosos de verdad traen entre 1.250 y 1.810. No es un error de dato: la
laringe es cartílago, no hueso.

El problema es que cuenta para el 20-60 % de hueso de la ración sin
aportar el calcio que esa proporción da por supuesto. No es peligroso —el
calcio tiene mínimo duro, así que el menú lo cubre igual— pero permite
menús que parecen BARF sin serlo.

- [ ] Decidir: moverla a `Extras`, o quitarla del catálogo.

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

- **Vísceras**: solo cordero, ternera y vaca. Faltan pollo, pavo, conejo,
  pato y cerdo.
- **Hígado**: solo conejo, cordero, pollo y vaca. Faltan pavo, pato, cerdo.

- [ ] Añadir vísceras e hígados de las especies que faltan. Lo más útil y
      lo más fácil de encontrar en una carnicería: **corazón y molleja de
      pollo y de pavo**, **hígado de pavo, de pato y de cerdo**, **riñón de
      cerdo**. Cada especie nueva en esas dos categorías vale más que diez
      cortes nuevos de carne muscular, que ya va sobrada.

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

### `DATOS_QUE_FALTAN.md`

Generado por `auditar_catalogo.py`: **57 alimentos y 431 valores** por
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
- **Taurina y L-carnitina** (≥250 y ≥50 mg/1000kcal): estos SÍ son
  huecos reales, pero no por falta de dato limpio — es que ninguno de
  los dos está entre los 41 nutrientes que mide el motor, ni en ninguna
  ficha del catálogo. Esto es exactamente lo que ya documenta el aviso
  de `dcm_taurina_respondedora` (añadida en la misma ronda): «la taurina
  no está entre los 41 nutrientes que este motor mide». Añadirlos de
  verdad significaría (a) sacar el dato de taurina y L-carnitina de las
  159 fichas del catálogo, cosa que ni BEDCA ni USDA dan de forma
  sistemática para muchos alimentos frescos, y (b) el motor solo sabe
  poner TECHOS por patología, no SUELOS — un mínimo de taurina necesita
  el mismo mecanismo nuevo que ya le faltaba a `artrosis` (omega-3) y
  `dermatosis_zinc` (zinc), ver §12-quinquies de `VETERINARIOS.md`.

**Conclusión: los 5 estadios MMVD completos NO necesitan más números de
los que ya tienen.** El reparto de macros "más allá del sodio" que
proponía el borrador ya está cubierto en su totalidad por los mínimos de
FEDIAF vigentes, excepto taurina y L-carnitina — y esos dos no son un
hueco de verificación, son un hueco de arquitectura (falta el mecanismo
de suelos por patología) y de catálogo (falta el dato). Se deja
documentado aquí para que quede cerrado, no abierto esperando "una fuente
más limpia" que ya se consiguió y no cambió la conclusión.

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
darlos por buenos — mismo criterio que ya se aplicó a `obesidad`. Sigue
sin ser posible para `dcm_taurina_respondedora` (taurina y L-carnitina no
están en el catálogo ni en el MAPA de 41 nutrientes: el mecanismo nuevo no
sirve de nada si no hay dato que sumar), documentado también en la
sección de MMVD, arriba.

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

