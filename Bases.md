# LAS BASES — CERRADAS. NO SE TOCAN.

> ## 🛑 ANTES DE PROPONER CUALQUIER CAMBIO: LEE `Ya_probado.md`
> Está en este mismo repo. Contiene lo que ya se intentó y NO funcionó,
> extraído de las 14 sesiones de trabajo.
> **Si propones algo que está ahí, estás haciendo perder el tiempo.**
> Los transcritos completos están en `/mnt/transcripts/` — se pueden
> buscar con grep antes de sugerir nada.


Este documento es la ÚNICA fuente de verdad sobre los tres pilares.
Si algo parece contradecir esto, **el equivocado es lo otro**, no este archivo.

Antes de tocar el backend, SIEMPRE:

    python3 verificar_arranque.py   # el backend arranca
    python3 verificar_pilares.py    # las bases están intactas

---

## PILAR 1 — ALIMENTOS  (`alimentos_v3_final.json`)

153 alimentos. 0 duplicados. Sello: `ded99a0da6999d16`

Fuentes, en este orden:
1. **BEDCA** (`LISTAS_BEDCA.docx` del usuario) — primaria
2. **Köber / Kienzle / Dobenecker (ESVCN 2017)** — único válido para Ca y P de
   huesos CON hueso, porque BEDCA mide siempre carne deshuesada
3. **CIQUAL (ANSES)** — para lo que no está en BEDCA

Reglas fijas:
- Los nombres dicen la verdad sobre si llevan hueso o no
  ("Pato (carne sin hueso)" vs "Codorniz entera")
- Cuando una fuente se contradice a sí misma, se documenta en `nota_datos`
  del alimento y se explica qué se hizo y por qué

## PILAR 2 — REQUISITOS  (`requerimientos_v2_final.json`)

32 requisitos. Sello: `73ab445f9881f543`
**99/99 valores verificados** contra el PDF oficial de FEDIAF.

### Qué tabla y qué columna  (esto es lo que hay que respetar)

| Nuestra etapa | Columna de FEDIAF |
|---|---|
| Adulto, Senior | Tabla III-3b, "Adult based on MER of **95 kcal/kg^0.75**" |
| CachorroJoven, **Gestante, Lactante** | "Early Growth (<14 weeks) **& Reproduction**" |
| CachorroCrecimiento | "Late Growth (≥14 weeks)" |

- **Tabla III-3b** = por 1000 kcal de EM. De aquí salen TODOS los mínimos y
  los máximos NUTRICIONALES (N).
- **Tabla III-3a** = por 100 g de materia seca. SOLO para los máximos
  LEGALES (L), porque en la III-3b vienen sin número.
- **Conversión (Tabla III-2): units/100g MS × 2.5 = units/1000 kcal.**
  NO ×10. Este error ya se cometió una vez.
- **Las vitaminas de la tabla van en UI**, nosotros en µg/mg:
  A: 1 UI = 0.30 µg · D: 1 UI = 0.025 µg · E: 1 UI = 0.67 mg.
  Comparar UI contra µg da falsos errores. Esto también ya pasó.

Verificado idéntico en las ediciones de **2020, 2021 y 2025**.

## PILAR 3 — KCAL DIARIAS  (`der.py`)

Sello: `7caac8124796443f`   ·   **MÉTODO EUROPEO**

    DER = coeficiente (kcal/kg^0.75) × peso^0.75

**Los ajustes se SUMAN al coeficiente, NO se multiplican.** Por eso aquí
no se pueden apilar factores por error.

### Fuentes
- **Crecimiento, gestación y lactancia** → FEDIAF
- **Adultos** → tesis Univ. de Múnich (edoc.ub.uni-muenchen.de/17585):
  consumo REAL de 586 perros de compañía privados europeos
- Recogidas en la calculadora alemana dr.ueke.de, que las declara

### ⚠️ LA ACTIVIDAD NO SE USA EN CACHORROS, GESTACIÓN NI LACTANCIA
La fuente, literal: *"Für Hunde im Wachstum und Reproduktion ist dies
**unerheblich**"* (para perros en crecimiento y reproducción esto es
irrelevante). Lo repite para actividad, convivencia, edad y raza.

### Crecimiento — ecuación de KLEIN et al. 2019
**Klein, Thes, Böswald & Kienzle (2019), J Anim Physiol Anim Nutr 103:1952.
Universidad de Múnich, 493 CACHORROS DE COMPAÑÍA REALES.**

    ME (MJ) = (1.063 − 0.565 × [PesoActual / PesoAdultoEsperado]) × Peso^0.75
    (× 239 para pasar a kcal)

Curva **continua**: sin los saltos bruscos de los 3 escalones de FEDIAF al
cruzar el 50% y el 80%. Klein confirmó además que el NRC 2006 sobreestima
~20% en menores de 6 meses, en línea con Norfolk y Yorkshire Terrier.
Suelo de seguridad: nunca por debajo de 98 kcal/kg^0.75 (un cachorro no
necesita menos que un adulto de su peso). Sin peso adulto conocido, cae al
escalón prudente de FEDIAF (140).

### Adultos y senior — base por actividad + ajustes aditivos
**TABLA VII-6 de FEDIAF.** Las bases 95 y 110 están confirmadas en el texto
oficial (secc. 3.2.1); el resto vía reproducción de UK Pet Food.

| Base (kcal/kg^0.75) | |
|---|---|
| sedentario — baja, <1 h/día | **95** |
| normal — moderada 1-3 h, bajo impacto | **110** |
| activo — moderada 1-3 h, ALTO impacto | **125** |
| muy activo — alta 3-6 h (trabajo) | **150** |
| trabajo — alta, extremo superior | **175** |

La media medida en 586 perros de compañía (Thes 2014) fue **98**, justo entre
"baja" y "moderada". FEDIAF llega a 860-1240 para perros de trineo en frío
extremo: eso no lo cubre esta app.

Ajustes: senior **−5** · con otros perros **+10** · macho entero **+10** ·
razas de más gasto **+15** · de menos gasto **−15**
**La castración NO cambia el gasto** (dato europeo; la fuente lo marca
con un "(!)"). El parámetro sigue existiendo por compatibilidad.

### Gestación y lactancia
- Gestación: `132 × peso^0.75`, y desde la semana 5 `+ 26 × peso`
- Lactancia: `145 × peso^0.75 + extra`, donde extra es `24 × n × peso`
  hasta 4 cachorros y `(96 + 12(n−4)) × peso` con más de 4, todo
  ponderado por semana: 0.75 / 0.95 / 1.10 / 1.40
  (**la fuente escribe `96 + 12n`, pero eso da un salto imposible entre
  4 y 5 cachorros; la forma continua del NRC es `96 + 12(n−4)`**)

### ✅ ADULTOS: VERIFICADO CONTRA FUENTE PRIMARIA EUROPEA REVISADA POR PARES
**Thes M, Köber N, Fritz J, Wendel F, Dillitzer N, Dobenecker B, Kienzle E
(2014). "Metabolizable energy intake of client owned adult dogs". Journal of
Animal Physiology and Animal Nutrition.** Universidad de Múnich (LMU),
cátedra de Nutrición Animal y Dietética. **586 perros de compañía REALES**
con el peso estable. Texto completo: edoc.ub.uni-muenchen.de/17585

Valores medidos (1 MJ = 239 kcal), y lo que tenemos:

| Medido | kcal/kg^0.75 | Nuestro |
|---|---|---|
| **Media de los 586 perros** | **98** | base "normal" = **98** ✅ |
| Razas de más gasto | 113 | +15 ✅ |
| Razas de menos gasto | 82 | −15 ✅ |
| Jóvenes ≤7 años | 100 | 0 ✅ |
| Mayores >7 años | 93 | −7 ✅ |
| Machos ENTEROS | 108 | +10 ✅ |
| Machos castrados | 95 | (sin ajuste) |
| Hembras enteras | 97 | (sin ajuste) |
| Hembras castradas | 92 | (sin ajuste) |

**La castración NO tuvo efecto significativo en hembras** (97 vs 92). El único
efecto de sexo significativo fue el macho entero. Confirma nuestro diseño.

**Sobrepeso**: sobre el peso ACTUAL comen 86, pero **sobre el peso IDEAL la
diferencia desaparece**. La tesis lo dice literal: *"calcular el mantenimiento
por el peso ideal es un método excelente"*. Confirma nuestro enfoque.

**Listas de razas — EXACTAS de la tesis:**
- **+15**: Jack Russell, Parson Russell, Dálmata, Braco Húngaro (Vizsla),
  Bearded Collie, Galgo Afgano, Galgo Español, Boxer, Rhodesian Ridgeback,
  Flat Coated Retriever *(faltan en la app: Kleiner Münsterländer, Sloughi,
  English Foxhound)*
- **−15**: Dachshund (estándar y miniatura), Lhasa Apso, Shih Tzu, West
  Highland White Terrier, **Border Collie**, Collie de Pelo Largo, Airedale
  Terrier, **American Staffordshire Terrier**, Golden Retriever
  *(falta en la app: Löwchen)*
- ⚠️ **El Border Collie está en la lista de MENOS gasto**, aunque sorprenda.
  Y "Collies" excluye expresamente al Bearded Collie.

### ⚠️ LO QUE SIGUE SIN VERIFICAR CONTRA LA FUENTE ORIGINAL
**Solo el CRECIMIENTO, la GESTACIÓN y la LACTANCIA.** Sus coeficientes
(210/175/140, 132+26, y la fórmula de lactancia) vienen de una fuente
SECUNDARIA que cita a FEDIAF, no del texto original. **La parte de ADULTOS
ya está verificada contra fuente primaria (ver arriba).** **El Anexo 7.2.4 del PDF de FEDIAF no se ha podido leer: se trunca
antes de esa página en las CUATRO ediciones probadas (2018 alemana, 2020,
2021 y 2025).** Lo que sí está verificado en el texto original:
- El mantenimiento adulto son 95-110 kcal/kg^0.75 (secc. 3.2.1 y cap. 6)
- FEDIAF recomienda partir de un MER bajo y subir (secc. 7.2.3.2)
Los coeficientes de crecimiento equivalen a RER ×3.0 / ×2.5 / ×2.0, que
encajan con la tabla clínica (Small Animal Clinical Nutrition 5ª ed.), pero
**no se puede enseñar una página de FEDIAF con esos números**.
**La lactancia es la parte más débil**: fórmula de fuente secundaria, escala
con el peso vivo y se dispara en perros grandes. Por eso lleva TOPE (×6 del
RER, el máximo de la tabla clínica) y devuelve `requiere_veterinario: True`.

### ⚠️ NO MEZCLAR EDICIONES DE FEDIAF
La edición de 2018 sigue circulando y tiene valores DISTINTOS: selenio 87 µg
(vs 67.50 húmedo en 2020+) y hierro máx. 142 mg (vs 68.18). Nuestros
requisitos son los de 2021/2025, que son los vigentes.

### El peso IDEAL manda sobre todo — YA CONECTADO AL FORMULARIO
El selector de condición corporal de la app (5 niveles) se traduce a la
escala validada de 9 puntos (Laflamme 1997, contrastada con DEXA):

| Selector | BCS | Desvío |
|---|---|---|
| Muy delgado | 2 | −30% |
| Delgado | 4 | −10% |
| Ideal | 5 | 0 |
| Sobrepeso | 7 | +20% |
| Obeso | 9 | +40% |

`peso_ideal = peso_actual / (1 + 0.10 × (BCS − 5))`, **con tope al alza del
20%**: un perro muy delgado daría un objetivo un 43% mayor, y ni se sube de
golpe ni suele estar delgado por comer poco (suele haber enfermedad detrás).

Sobrepeso ≥10% → se baja al **RER puro (70)** y se avisa. Eso equivale al
**64% del mantenimiento a peso ideal**, dentro de la banda 50-65% que
recomienda German et al. 2015 (Liverpool) para pérdida de peso.
Infrapeso ≥10% → **+20%**.

### ⚠️ VARIABILIDAD INDIVIDUAL — SE AVISA EN PANTALLA
**Bermingham et al. 2014** (PLOS ONE, metaanálisis de 713 perros): media
142.8 ± **55.3** kcal/kg^0.75, o sea **±38.7%**. Ninguna ecuación acierta con
un perro concreto. La app muestra el número como punto de partida y pide
pesar cada 2-3 semanas. Es el único punto en que TODAS las fuentes coinciden.

### Réplica en el frontend
`calcularDER()` en el .jsx es una copia exacta. **Verificado: 9/9 casos
dan el mismo número en Python y en JavaScript.** Si se toca uno, se toca
el otro.

---

## LO QUE SÍ SE PUEDE TOCAR

Todo lo demás: `optimizador.py` (salvo la cabecera [CIENCIA]/[CRITERIO]),
`recalculo.py`, `plantillas.py`, `analizador.py`, `main.py` y el frontend.
Ahí es donde se trabaja de ahora en adelante.
