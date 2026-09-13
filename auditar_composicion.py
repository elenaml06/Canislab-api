# -*- coding: utf-8 -*-
"""
BARRER EL CATÁLOGO ENTERO CONTRA SUS FUENTES, CELDA A CELDA
===========================================================

POR QUÉ EXISTE (13 de septiembre de 2026). Petición de Elena: «coge todos los
alimentos del catálogo y los buscas por orden en esas listas, si no aparece en
la que manda número 1 la buscas en la 2 y así… y compruebas que todos los datos
están bien, anotas los fallos y cambias lo que haya que cambiar».

Lo que YA había no servía para eso, y conviene decir exactamente por qué:

  · `contrastar_fuentes.py` mira UNA ficha y hay que darle los identificadores a
    mano. Es la herramienta de quien va a abrir una ficha concreta, y está bien
    así. Pero nadie la había pasado por las 163, así que nadie sabía cuántas
    celdas se separan de su fuente.
  · `fijar_identificadores.py` empareja la ficha con su FILA, que es el paso
    anterior, y no mira ni una cifra más allá de proteína, grasa, agua y energía.
  · `auditar_catalogo.py` compara el catálogo CONSIGO MISMO (huecos, ceros
    raros, coherencia interna). Nunca sale a la fuente.

O sea que entre la fuente y el catálogo había un paso a mano sin auditar, que es
la misma forma de fallo de `auditar_transcripcion_fediaf.py` y de
`auditar_kober.py`: lo que no se rehace no se audita.

LO QUE COMPRUEBA, Y POR QUÉ CADA COSA
-------------------------------------
1. **Que la unidad de la fuente se convierte a la nuestra.** Es el fallo que no
   da error: una cifra buena en la escala equivocada pasa cualquier validación
   de formato, y el semáforo la compara contra un requisito en otra escala y
   sale verde. Las conversiones están declaradas en
   `fuentes_de_composicion.json` y este script REHACE la lectura de la unidad
   que declara cada fuente (el `v_unit` de BEDCA, el `unit_name` de USDA, la
   unidad escrita dentro del nombre de columna de CIQUAL) y falla si no coincide
   con lo declarado.
2. **Que un hueco no se haya convertido en un cero.** Elena, el mismo día: «UN
   HUECO NO ES UN CERO. SOLO UN CERO ES UN CERO». BEDCA es la única fuente que
   lo sabe (`TR` con la celda vacía = no hay cifra), así que cuando ella dice
   que no hay dato y nosotros tenemos un 0 sin declararlo, se dice.
3. **Que un hueco nuestro no tenga ya respuesta en la fuente que manda.** Un
   `sin_dato` que la fuente SÍ publica no es un hueco: es una celda sin cerrar.
4. **Que ninguna cifra se haya separado de su fuente.** Y cuando se separa, se
   dice si la separación TIENE FORMA DE ERROR DE UNIDAD (un factor 10, 100,
   1000, el 4,184 de los kJ o el 1,542 del cloruro) en vez de meterlo en el
   mismo cajón que la variación biológica, que es real y no es un fallo.

LO QUE NO HACE, A PROPÓSITO
---------------------------
· **Sin `--cerrar` no escribe nada.** El modo por defecto saca un informe y se
  calla. Escribir en el catálogo es un acto aparte y hay que pedirlo.
· **No toca una DISCREPANCIA, nunca, ni con `--cerrar`.** Cuando las dos cifras
  existen y no coinciden, las dos fuentes son honestas y cuál vale es un
  JUICIO, no una cuenta: la composición de un alimento varía de verdad entre
  países (raza, pienso, suelo). Son 259 y están listadas para que las mire una
  persona.
· **No toca el calcio ni el fósforo de las diez fichas de hueso.** Esas las
  manda Köber 2017 (mandato 2) y las rehace `auditar_kober.py`. Las tres bases
  miden carne DESHUESADA: su calcio es el de la carne, no el del hueso.
· **No compara la vitamina A.** Las tres fuentes usan convenios distintos del
  β-caroteno y ninguno es el de FEDIAF (4:1 para el perro, Tabla VII-14).
  Comparar acusaría de error a fichas correctas. Se informa aparte.
· **No mira los suplementos contra las bases.** No tienen fila: su fuente es la
  etiqueta del fabricante (mandato 5). Lo que se les exige es otra cosa.
· **No obedece un cero de la fuente a ciegas.** Un 0 que la fuente publica como
  MEDIDA se escribe en `cero_verificado` y no como un 0 pelado -- un 0 a secas
  es indistinguible de un hueco, que es justo lo que esto separa. Y si ese cero
  no es creíble (un TEJIDO animal con 0 mg de calcio), no se escribe: se dice.

QUÉ HACE `--cerrar`, QUE ES EL ÚNICO QUE ESCRIBE
------------------------------------------------
Tres cosas, y las tres dejan rastro de dónde viene cada número:

  1. Donde tenemos un hueco o un cero mudo y la fuente que manda SÍ publica
     cifra, pone la cifra y escribe su procedencia en `composicion_fuente`
     (fuente, id, fila literal, columna, valor en bruto, unidad y factor), para
     que el BLOQUE 100 pueda REHACER la cuenta.
  2. Donde la fuente publica un 0 como medida, lo declara en `cero_verificado`
     con su fila.
  3. Donde la fuente dice que NO HAY CIFRA (`TR` con la celda vacía en BEDCA),
     declara el hueco en `sin_dato`. Un hueco no es un cero.

⚠️ **Los aminoácidos y los ácidos grasos NO se copian: se transfieren por
gramo.** Los aminoácidos por gramo de PROTEÍNA, que es la regla de
`UNIDADES.md` («se divide por SU proteína y se multiplica por la NUESTRA;
copiarlo tal cual mete el error de las dos proteínas a la vez»), y los ácidos
grasos por gramo de GRASA, con el mismo argumento sin cambiar una palabra: un
ácido graso es una FRACCIÓN de la grasa, no una cantidad independiente. Si la
fila trae 3,05 g de linoleico sobre 15,06 g de grasa y nuestra ficha tiene
9,25 g de grasa, copiar 3,05 declara un aceite que no está ahí.

CÓMO SE USA
-----------
    python3 auditar_composicion.py --instantanea   # baja las fuentes (red)
    python3 auditar_composicion.py                 # audita, SIN red
    python3 auditar_composicion.py --cerrar        # ESCRIBE en el catálogo

La instantánea (`fuentes_instantanea.json`) guarda el valor EN LA UNIDAD DE LA
FUENTE, su unidad y su `value_type`, más la descripción LITERAL de la fila. Así
la conversión se puede rehacer y el emparejamiento se puede leer: un
identificador a secas no dice si «pollo» trajo «repollo».
"""
import argparse
import collections
import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
CATALOGO = os.path.join(RAIZ, "alimentos_v3_final.json")
DECLARACION = os.path.join(RAIZ, "fuentes_de_composicion.json")
INSTANTANEA = os.path.join(RAIZ, "fuentes_instantanea.json")

# Las fichas cuya fuente es la etiqueta del fabricante (mandato 5): no tienen
# fila en ninguna base de composición, así que no entran en el barrido.
CATEGORIAS_DE_ETIQUETA = {"Multivitamínico", "Omega-3", "Calcio", "Vitamina B",
                          "Yodo", "Fibra", "Hierro"}
NOMBRES_DE_ETIQUETA = {"Sal común (cloruro sódico)"}

# Las diez fichas de hueso: su calcio y su fósforo los manda Köber 2017.
# La lista se IMPORTA de `auditar_kober.py` para que no haya dos copias -- el
# día que se añada una ficha de hueso, aquí se entera sola.
def _fichas_de_hueso():
    try:
        import auditar_kober
        return set(auditar_kober.DE_DONDE_SALE)
    except Exception:
        return set()

# Cuánto puede separarse nuestra cifra de la de la fuente antes de decirlo.
# No es tolerancia de exactitud: la composición de un alimento varía de verdad
# entre un país y otro (raza, pienso, suelo), y dos bases honestas discrepan.
# Lo que NO es variación biológica es un factor de diez.
TOLERANCIA = 0.25
SUELO_ABSOLUTO_RELATIVO = 1e-9

# Los factores que delatan un error de unidad en vez de una discrepancia real.
#
# ⚠️ ESTA TABLA NACIÓ MAL Y SE ARREGLÓ EL MISMO DÍA, y el fallo merece quedar
# escrito porque es el del araquidónico otra vez: la primera versión aceptaba
# un ±5 % alrededor de cada factor y aplicaba los cinco a CUALQUIER nutriente.
# El ±5 % alrededor de 1,542 cubre las razones 1,465 a 1,619, o sea TODA
# discrepancia de entre el 47 % y el 62 % -- que es variación biológica normal
# entre dos bases de países distintos. Resultado: 45 avisos de los que 42 eran
# falsos, y un aviso que se equivoca 42 veces de 45 enseña a no mirarlo. Es
# exactamente lo que el repo ya sabía: «No lo eran. La herramienta lo era.»
#
# Las dos reglas que lo arreglan:
#   1. UN FACTOR DE UNIDAD SOLO VALE DONDE ESA CONFUSIÓN ES POSIBLE. El 1,542
#      es la razón de los pesos atómicos del cloro y el sodio: solo significa
#      algo en la columna `cloruro`. El 4,184 son los kJ: solo en `energia`.
#   2. UN ERROR DE UNIDAD ES EXACTO. Un dígito de más da ×10 clavado, no ×10,3.
#      La variación biológica no cae en ×10,000. Tolerancia del 1 %, no del 5 %.
FACTORES_SOSPECHOSOS = (
    (1000.0, None, "×1000 — g contra mg, o mg contra µg"),
    (100.0, None, "×100 — dos dígitos, el factor de la tabla de Köber (g/kg contra mg/100 g)"),
    (10.0, None, "×10 — un dígito de más o de menos"),
    (4.184, ("energia",), "×4,184 — kJ leídos como kcal"),
    (1.542, ("cloruro",), "×1,542 — cloruro derivado del sodio por los pesos atómicos"),
)
# Un error de unidad es exacto; lo que no lo es, es otra cosa.
MARGEN_DEL_FACTOR = 0.01


def _num(x):
    if x is None:
        return None
    s = str(x).strip().replace(",", ".")
    if s in ("", "-", "traces", "tr") or s.startswith("<"):
        return None
    try:
        return float(s)
    except ValueError:
        return None


def huele_a_unidad(nuestro, suyo, clave):
    """¿La separación tiene forma de error de unidad EN ESTA COLUMNA?"""
    if not nuestro or not suyo:
        return None
    r = max(nuestro, suyo) / min(nuestro, suyo)
    for f, solo_en, texto in FACTORES_SOSPECHOSOS:
        if solo_en is not None and clave not in solo_en:
            continue
        if abs(r - f) / f <= MARGEN_DEL_FACTOR:
            quien = ("NUESTRO valor es el grande" if nuestro > suyo
                     else "el de la FUENTE es el grande")
            return f"{texto} ({quien}, razón {r:.4g})"
    return None


# =============================================================================
# LA INSTANTÁNEA — lo que publica cada fuente, tal cual, sin convertir
# =============================================================================
def construir_instantanea():
    import contrastar_fuentes as cf
    decl = json.load(open(DECLARACION, encoding="utf-8"))
    porn = decl["unidades"]["por_nutriente"]
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))

    fuera = {"_meta": {
        "que_es": ("Lo que publica cada fuente de cada alimento del catálogo, EN LA UNIDAD DE LA "
                   "FUENTE y sin convertir, con la descripción LITERAL de la fila de la que sale."),
        "por_que": ("Para que la batería pueda comprobar el catálogo contra su fuente SIN RED, y para "
                    "que la conversión se pueda rehacer en vez de creérsela. Es la misma idea que "
                    "`fediaf_tabla_III_3b.txt`: la fuente congelada en el repo, al lado de lo que "
                    "sale de ella."),
        "ojo": ("La descripción de la fila NO es decoración: es lo único que permite ver un "
                "emparejamiento equivocado. Un identificador a secas no dice si «pollo» trajo "
                "«Repollo» (BEDCA 2417, que sale de verdad al buscar «pollo»)."),
        "generado": "auditar_composicion.py --instantanea",
    }, "alimentos": {}}

    for n, ficha in enumerate(catalogo, 1):
        nombre = ficha["nombre"]
        ids = ficha.get("fuentes_id") or {}
        if not ids:
            continue
        print(f"[{n:3d}/{len(catalogo)}] {nombre[:46]:46s}", end=" ", flush=True)
        ent = {}
        for fuente, fid in sorted(ids.items()):
            try:
                if fuente == "bedca":
                    fila, vals = _bedca_crudo(cf, fid)
                elif fuente == "ciqual":
                    fila, vals = cf.ciqual_ficha(fid)
                    vals = {k: (v, None, None) for k, v in vals.items()}
                elif fuente == "usda":
                    fila, vals = _usda_crudo(cf, fid)
                else:
                    continue
            except Exception as e:
                print(f"({fuente}: {str(e)[:40]})", end=" ")
                continue
            celdas = {}
            for clave, meta in porn.items():
                e = (meta.get("por_fuente") or {}).get(fuente)
                if not e:
                    continue
                nombres = [e["columna"]] + list(e.get("alias_aceptados") or [])
                for col in nombres:
                    if col in vals:
                        v, uni, tipo = vals[col]
                        celdas[clave] = {"valor": v, "columna": col,
                                         "unidad": uni, "value_type": tipo}
                        break
            ent[fuente] = {"id": str(fid), "fila": fila, "celdas": celdas}
            print(f"{fuente}✓", end=" ")
        fuera["alimentos"][nombre] = ent
        print()

    with open(INSTANTANEA, "w", encoding="utf-8") as fh:
        json.dump(fuera, fh, ensure_ascii=False, indent=1, sort_keys=False)
        fh.write("\n")
    print(f"\n  instantánea de {len(fuera['alimentos'])} alimentos en "
          f"{os.path.basename(INSTANTANEA)}")
    return 0


def _bedca_crudo(cf, fid):
    """BEDCA con el `v_unit` y el `value_type`, que `bedca_ficha` tira.

    ⚠️ `contrastar_fuentes.bedca_ficha` devuelve (valor, value_type) y PIERDE la
    unidad. Sin unidad no se puede comprobar la conversión, que es justo lo que
    este barrido existe para comprobar.
    """
    import xml.etree.ElementTree as ET
    sel = "".join(f'<atribute name="{a}"/>' for a in cf._SEL_BEDCA_2)
    xml = ('<?xml version="1.0" encoding="utf-8"?><foodquery><type level="2"/>'
           f'<selection>{sel}</selection>'
           '<condition><cond1><atribute1 name="f_id"/></cond1>'
           f'<relation type="EQUAL"/><cond3>{fid}</cond3></condition>'
           '<condition><cond1><atribute1 name="publico"/></cond1>'
           '<relation type="EQUAL"/><cond3>1</cond3></condition></foodquery>')
    raiz = ET.fromstring(cf._bedca_post(xml))
    vals = {}
    for c in raiz.iter("foodvalue"):
        comp = (c.findtext("c_ori_name") or "").strip()
        if comp:
            vals[comp] = ((c.findtext("best_location") or "").strip() or None,
                          (c.findtext("v_unit") or "").strip() or None,
                          (c.findtext("value_type") or "").strip() or None)
    return (raiz.findtext(".//f_ori_name") or "").strip(), vals


def _usda_crudo(cf, fid):
    """USDA por `nutrient_id`, no por nombre.

    ⚠️ Por nombre, «Energy» son DOS filas -- 1008 en kcal y 1062 en kJ -- y gana
    la última. Ver `fuentes_de_composicion.json`.
    """
    import csv
    d, comidas, nutrientes = cf._usda_tablas()
    unidad = {}
    with open(os.path.join(d, "nutrient.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            unidad[r["id"]] = (r["name"], r["unit_name"])
    vals = {}
    with open(os.path.join(d, "food_nutrient.csv"), newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["fdc_id"] == str(fid):
                nid = r["nutrient_id"]
                nom, uni = unidad.get(nid, ("?", None))
                # la fila de energía se indexa por su identificador
                clave = f"Energy#{nid}" if nom == "Energy" else nom
                vals[clave] = (r["amount"], uni, None)
    # que el mapa pueda pedir «Energy» y recibir la de kcal
    if "Energy#1008" in vals:
        vals["Energy"] = vals["Energy#1008"]
    return comidas.get(str(fid), ""), vals


# =============================================================================
# LA AUDITORÍA — sin red, contra la instantánea
# =============================================================================
def _orden_para(decl, clave, es_hueso):
    """La lista de fuentes que manda para ESE nutriente, en orden."""
    exc = (decl.get("mandato_por_nutriente") or {}).get(clave)
    if exc and isinstance(exc, dict) and "orden" in exc:
        orden = list(exc["orden"])
        # Köber solo manda si la ficha es un corte con hueso
        if "kober2017" in orden and not es_hueso:
            orden = [f for f in orden if f != "kober2017"]
        return orden
    return [f for f in decl["orden_de_mandato"]
            if f not in ("kober2017", "etiqueta_del_fabricante")]


def _unidad_esperada(decl, clave, fuente):
    e = ((decl["unidades"]["por_nutriente"].get(clave) or {}).get("por_fuente") or {}).get(fuente)
    return (e or {}).get("unidad_de_la_fuente"), (e or {}).get("factor")


def auditar():
    decl = json.load(open(DECLARACION, encoding="utf-8"))
    catalogo = json.load(open(CATALOGO, encoding="utf-8"))
    if not os.path.exists(INSTANTANEA):
        print("No está la instantánea. Créala con:\n"
              "    python3 auditar_composicion.py --instantanea")
        return 2
    inst = json.load(open(INSTANTANEA, encoding="utf-8"))["alimentos"]
    porn = decl["unidades"]["por_nutriente"]
    huesos = _fichas_de_hueso()

    hallazgos = collections.defaultdict(list)
    cuenta = collections.Counter()
    sin_emparejar = []

    for ficha in catalogo:
        nombre = ficha["nombre"]
        if ficha["categoria"] in CATEGORIAS_DE_ETIQUETA or nombre in NOMBRES_DE_ETIQUETA:
            cuenta["fichas_de_etiqueta"] += 1
            continue
        fuentes = inst.get(nombre) or {}
        if not fuentes:
            sin_emparejar.append(nombre)
            cuenta["fichas_sin_emparejar"] += 1
            continue
        cuenta["fichas_barridas"] += 1
        es_hueso = nombre in huesos
        huecos = set(ficha.get("sin_dato") or [])
        ciertos = set(ficha.get("cero_verificado") or {})
        dudosos = set(ficha.get("dato_dudoso") or {})
        nut = dict(ficha["nutrientes"])
        nut["energia"] = ficha.get("energia")

        for clave in porn:
            meta = porn[clave]
            if meta.get("ninguna_de_las_bases_lo_publica"):
                continue
            if meta.get("conflicto_de_convenio"):
                continue                       # la vitamina A se informa aparte
            if es_hueso and clave in ("calcio", "fosforo"):
                continue                       # manda Köber, lo rehace su auditor
            if clave not in nut:
                continue
            nuestro = _num(nut.get(clave))

            # --- la fuente que manda para este nutriente, por orden ---
            elegida = tipo_fuente = col = None
            suyo = None
            hueco_declarado_por_la_fuente = False
            for fuente in _orden_para(decl, clave, es_hueso):
                celda = ((fuentes.get(fuente) or {}).get("celdas") or {}).get(clave)
                if not celda:
                    continue
                v = _num(celda.get("valor"))
                uni_esp, factor = _unidad_esperada(decl, clave, fuente)
                # ⚠️ LA UNIDAD SE REHACE: si la fuente declara otra, no se convierte
                uni_real = celda.get("unidad")
                if uni_real and uni_esp and uni_real.strip().lower() != str(uni_esp).strip().lower():
                    hallazgos["UNIDAD_CAMBIADA_EN_LA_FUENTE"].append(
                        f"{nombre} · {clave}: {fuente} declara «{uni_real}» y "
                        f"`fuentes_de_composicion.json` dice «{uni_esp}». NO se convierte nada "
                        f"hasta que alguien lo mire: el factor declarado ({factor}) ya no vale.")
                    continue
                if v is None:
                    # BEDCA sabe distinguir: TR con celda vacía es un HUECO
                    if (celda.get("value_type") or "").upper() == "TR":
                        hueco_declarado_por_la_fuente = True
                    continue
                if factor is None:
                    continue
                elegida, col, suyo = fuente, celda.get("columna"), v * factor
                tipo_fuente = (celda.get("value_type") or "").upper()
                break

            fila = ((fuentes.get(elegida) or {}).get("fila") or "") if elegida else ""

            # --- clasificar ---
            if suyo is None:
                if clave in huecos:
                    cuenta["hueco_real"] += 1
                elif clave in ciertos:
                    # ⚠️ `cero_verificado` TAMBIÉN es declarar. Esta rama se dejó
                    # fuera en la primera versión y el informe acusaba al apio de
                    # tener un hueco guardado como cero cuando su cero está
                    # declarado con su motivo (ninguna planta tiene colecalciferol
                    # ni cobalamina). Un auditor que acusa a lo que está bien
                    # hecho se deja de mirar.
                    cuenta["cero_verificado"] += 1
                elif nuestro in (0, None) and hueco_declarado_por_la_fuente:
                    hallazgos["CERO_QUE_ES_UN_HUECO"].append(
                        f"{nombre} · {clave} = {nuestro} y NO está en `sin_dato`, pero BEDCA dice "
                        f"`TR` con la celda vacía: NO HAY CIFRA. Un hueco no es un cero -- tiene "
                        f"que ir a `sin_dato`.")
                continue

            if clave in huecos:
                # ⚠️ Un 0 de la fuente NO cierra un hueco si ese cero no es
                # creíble. CASO REAL: BEDCA 2292 publica `calcio = 0` como MEDIDA
                # para el pollo entero con piel, y un tejido animal con 0 mg de
                # calcio no existe. Decir «se puede cerrar con 0» sería invitar a
                # meter el cero que este fichero entero existe para evitar.
                if suyo == 0 and _es_tejido_animal(ficha) and clave in CERO_NO_CREIBLE_EN_ANIMAL:
                    hallazgos["LA_FUENTE_DA_UN_CERO_QUE_NO_ES_CREIBLE"].append(
                        f"{nombre} · {clave}: sigue en `sin_dato` y {elegida} publica 0 — pero es "
                        f"TEJIDO animal y ese cero no es creíble (criterio de UNIDADES.md), así "
                        f"que el hueco NO se cierra con él. Nuestro valor de trabajo: {nuestro}. "
                        f"Fila: «{fila}».")
                    continue
                hallazgos["HUECO_QUE_SE_PUEDE_CERRAR"].append(
                    f"{nombre} · {clave}: está en `sin_dato` y {elegida} (mandato "
                    f"{decl['fuentes'][elegida]['mandato']}) publica {suyo:,.4g} "
                    f"{meta['catalogo']}. Fila: «{fila}» · columna «{col}».")
                continue
            if clave in dudosos:
                cuenta["ya_marcado_dato_dudoso"] += 1
                continue

            if nuestro in (None, 0):
                if clave in ciertos:
                    cuenta["cero_verificado"] += 1
                elif suyo > 0:
                    hallazgos["CERO_MUDO"].append(
                        f"{nombre} · {clave} = 0 sin declarar, y {elegida} da {suyo:,.4g} "
                        f"{meta['catalogo']}. Fila: «{fila}».")
                else:
                    cuenta["cero_en_las_dos"] += 1
                continue

            if suyo == 0:
                cuenta["la_fuente_da_cero_y_nosotros_no"] += 1
                continue

            dif = abs(nuestro - suyo) / max(abs(nuestro), abs(suyo), SUELO_ABSOLUTO_RELATIVO)
            if dif <= TOLERANCIA:
                cuenta["ok"] += 1
                continue
            pista = huele_a_unidad(nuestro, suyo, clave)
            pct = 100 * (nuestro - suyo) / max(abs(suyo), SUELO_ABSOLUTO_RELATIVO)
            linea = (f"{nombre} · {clave}: nuestro {nuestro:,.4g} contra {suyo:,.4g} "
                     f"{meta['catalogo']} de {elegida} ({pct:+.0f} %). Fila: «{fila}».")
            if pista:
                hallazgos["HUELE_A_ERROR_DE_UNIDAD"].append(linea + f"  ⚠️ {pista}")
            else:
                hallazgos["DISCREPA"].append(linea)

    # --- informe ---
    ORDEN = ["UNIDAD_CAMBIADA_EN_LA_FUENTE", "HUELE_A_ERROR_DE_UNIDAD",
             "CERO_QUE_ES_UN_HUECO", "CERO_MUDO",
             "LA_FUENTE_DA_UN_CERO_QUE_NO_ES_CREIBLE", "DISCREPA",
             "HUECO_QUE_SE_PUEDE_CERRAR"]
    TITULO = {
        "UNIDAD_CAMBIADA_EN_LA_FUENTE":
            "LA FUENTE YA NO PUBLICA EN LA UNIDAD DECLARADA — el factor de conversión no vale",
        "HUELE_A_ERROR_DE_UNIDAD":
            "SEPARACIÓN CON FORMA DE ERROR DE UNIDAD — un factor 10 no es variación biológica",
        "CERO_QUE_ES_UN_HUECO":
            "UN HUECO GUARDADO COMO CERO — la fuente dice que no hay cifra y nosotros tenemos 0",
        "CERO_MUDO":
            "CERO SIN DECLARAR Y LA FUENTE DA CIFRA",
        "DISCREPA":
            f"SE SEPARA MÁS DEL {int(TOLERANCIA*100)} % — puede ser variación real entre bases",
        "HUECO_QUE_SE_PUEDE_CERRAR":
            "HUECO CON RESPUESTA EN LA FUENTE QUE MANDA — se puede cerrar",
        "LA_FUENTE_DA_UN_CERO_QUE_NO_ES_CREIBLE":
            "LA FUENTE PUBLICA UN CERO QUE NO ES CREÍBLE — el hueco se queda abierto",
    }
    for k in ORDEN:
        if not hallazgos[k]:
            continue
        print(f"\n{'='*78}\n{TITULO[k]}  ({len(hallazgos[k])})\n{'='*78}")
        for l in hallazgos[k]:
            print(f"  · {l}")

    print(f"\n{'='*78}\nRESUMEN\n{'='*78}")
    for k, v in sorted(cuenta.items()):
        print(f"  {k:34s} {v:5d}")
    for k in ORDEN:
        print(f"  {k:34s} {len(hallazgos[k]):5d}")
    if sin_emparejar:
        print(f"\n  Sin emparejar con ninguna fuente ({len(sin_emparejar)}):")
        for n in sin_emparejar:
            print(f"    · {n}")

    # Lo que NO puede existir: un hueco guardado como cero y una unidad rota.
    graves = (len(hallazgos["CERO_QUE_ES_UN_HUECO"])
              + len(hallazgos["UNIDAD_CAMBIADA_EN_LA_FUENTE"]))
    print(f"\n  Hallazgos graves (hueco como cero · unidad rota): {graves}")
    return 0


# =============================================================================
# CERRAR CELDAS — rellenar lo que la fuente que manda SÍ publica
# =============================================================================
# ⚠️ SOLO DOS CLASES DE CELDA, y ninguna es una discrepancia:
#   · HUECO_QUE_SE_PUEDE_CERRAR: tenemos `sin_dato` y la fuente publica cifra.
#   · CERO_MUDO: tenemos 0 sin declararlo y la fuente publica cifra.
# Una DISCREPANCIA no se toca nunca desde aquí: ahí las dos fuentes son honestas
# y cuál vale es un juicio, no una cuenta. La composición de un alimento varía de
# verdad entre países.

# ⚠️ LOS AMINOÁCIDOS NO SE COPIAN: SE TRANSFIEREN POR GRAMO DE PROTEÍNA.
# Es la regla de `UNIDADES.md`, escrita allí con su motivo: «Se coge el perfil de
# la ficha parecida, se divide por SU proteína y se multiplica por la NUESTRA.
# Copiarlo tal cual mete el error de las dos proteínas a la vez.» Y aquí aplica
# igual aunque la fila sea del MISMO alimento, porque la proteína de la fila de
# USDA y la nuestra no son el mismo número: los doce aminoácidos son una
# fracción de la proteína, así que el que manda es el cociente.
#
# Y por el mismo razonamiento, los ÁCIDOS GRASOS se transfieren por gramo de
# GRASA. Esto NO está escrito en `UNIDADES.md` -- se añade aquí el 13 de
# septiembre de 2026 -- y el argumento es el mismo sin cambiar una palabra: un
# ácido graso es una fracción de la grasa, no una cantidad independiente. Si la
# fila trae 3,05 g de linoleico sobre 15,06 g de grasa y nuestra ficha tiene
# 9,25 g de grasa, copiar 3,05 declara un aceite que no está ahí.
AMINOACIDOS = ("arginina", "histidina", "isoleucina", "leucina", "lisina", "metionina",
               "cistina", "fenilalanina", "tirosina", "treonina", "triptofano", "valina")
ACIDOS_GRASOS = ("linoleico", "linolenico", "araquidonico", "epa", "dha")

ESCALAR_POR = {
    **{a: "proteina" for a in AMINOACIDOS},
    **{g: "grasa" for g in ACIDOS_GRASOS},
}
# Por debajo de esto el cociente no significa nada y escalar mete ruido.
SUELO_PARA_ESCALAR = {"proteina": 1.0, "grasa": 0.5}

# ⚠️ UN CERO DE LA FUENTE NO SE ESCRIBE COMO UN CERO PELADO.
# Si la fuente que manda publica 0 y lo publica como MEDIDA (`AR`/`BE` en BEDCA),
# ese cero es un dato -- pero un 0 a secas en el catálogo es indistinguible de un
# hueco, que es justo lo que este trabajo existe para separar. Así que se escribe
# en `cero_verificado`, que es el campo que el repo creó para esto: «un 0 al que
# alguien fue a la fuente, comprobó que es real, y dejó escrito cuál y cuándo».
# El caso masivo es la FIBRA de la carne y el pescado: cero de verdad, porque el
# tejido animal no tiene fibra dietética, y hasta hoy era un cero mudo.
#
# ⚠️ Y CON UNA EXCEPCIÓN, porque una fuente también se equivoca. Estos
# nutrientes NO pueden valer cero en un alimento de origen animal, y el criterio
# es de `UNIDADES.md`: «un cero solo es creíble si algún alimento de esa familia
# puede tenerlo de verdad... Un tejido no tiene nunca potasio, fósforo, magnesio,
# sodio, cloruro, hierro, cinc ni proteína a cero; un alimento animal no tiene la
# B12 a cero».
# CASO REAL ENCONTRADO: BEDCA 2292 «Pollo, entero, con piel, crudo» publica
# `calcio = 0` con `value_type` AR, o sea como medida. Con la primera versión de
# esto, la ficha «Pollo con piel (sin hueso)» pasaba de 10 mg de calcio a 0 -- un
# número real sustituido por un cero, obedeciendo a la fuente. No se obedece: se
# dice.
CERO_NO_CREIBLE_EN_ANIMAL = ("proteina", "calcio", "fosforo", "potasio", "sodio",
                             "cloruro", "magnesio", "hierro", "zinc", "vitB12")
CATEGORIAS_DE_ORIGEN_ANIMAL = {"Carne muscular", "Pescados y mariscos", "Vísceras",
                               "Hígado", "Hueso carnoso"}
NOMBRES_DE_ORIGEN_ANIMAL = ("huevo", "laringe")


# ⚠️ LO QUE UNA GRASA PURA NO PUEDE LLEVAR, Y POR QUÉ ESTO ES UN CERO Y NO UN
# HUECO.
#
# CASO REAL, Y LO CAUSÓ ESTE SCRIPT EL 13 DE SEPTIEMBRE. BEDCA publica la
# proteína y los minerales de sus aceites como `TR` con la celda vacía, que es
# «no hay cifra», así que la pasada que declara huecos marcó `proteina` como
# `sin_dato` en el aceite de oliva virgen extra y en el de girasol. Y eso es
# FALSO: un aceite refinado son triglicéridos — 100 g de grasa y 888 kcal no
# dejan sitio para proteína. `UNIDADES.md` ya lo dice con otras palabras: «Un
# aceite con 0 g de proteína tiene 0 de lisina de verdad».
#
# Y no era inofensivo: un hueco se imputa al PERCENTIL 90 de su familia contra
# los máximos, y la familia «Extras» incluye semillas con 17 g de proteína. Con
# esos dos huecos puestos, el chihuahua de 3 kg con patología RENAL se quedaba
# SIN MENÚ EN LOS SEIS PELDAÑOS de la escalera — con el catálogo de `main` sí
# salía. Lo cazaron los BLOQUES 9 y 76.
#
# La línea se traza por lo que una grasa SÍ puede llevar: las vitaminas
# LIPOSOLUBLES (A, D, E) y los ácidos grasos, que es precisamente para lo que
# está el aceite de hígado de bacalao. Todo lo demás — proteína, los doce
# aminoácidos, los minerales y las vitaminas hidrosolubles — no viaja en grasa.
ES_GRASA_PURA_DESDE = 80.0          # % de grasa, el mismo umbral que `sin_huella`
CERO_CIERTO_EN_GRASA_PURA = (
    ("proteina",)
    + AMINOACIDOS
    + ("calcio", "fosforo", "potasio", "sodio", "cloruro", "magnesio", "hierro",
       "cobre", "manganeso", "zinc", "yodo", "selenio")
    + ("tiamina", "riboflavina", "niacina", "acidoPantotenico", "vitB6", "folato",
       "vitB12", "colina")
    + ("fibra",)
)


def _es_grasa_pura(ficha):
    try:
        return float((ficha.get("nutrientes") or {}).get("grasa") or 0) >= ES_GRASA_PURA_DESDE
    except (TypeError, ValueError):
        return False


def _es_tejido_animal(ficha):
    """¿Es TEJIDO animal? La grasa fundida no lo es, y ahí sí hay ceros reales.

    ⚠️ LA PRIMERA VERSIÓN DECÍA «de origen animal» Y ERA DEMASIADO ANCHA: marcaba
    como no creíbles los ceros de `Grasa de pollo` y de `Manteca` -- doce celdas
    de trece --, y esos ceros son de verdad. Una grasa fundida no tiene músculo:
    no tiene proteína, ni potasio, ni B12, y BEDCA los publica como medida (AR)
    con razón. La regla de `UNIDADES.md` habla de un TEJIDO («un tejido no tiene
    nunca potasio, fósforo, magnesio…»), y un aceite o una manteca no lo es.
    Se separan por lo mismo que `sin_huella` separa los aceites: la grasa.
    """
    nut = ficha.get("nutrientes") or {}
    try:
        if float(nut.get("grasa") or 0) >= 80.0:
            return False                  # grasa fundida o aceite: no es tejido
    except (TypeError, ValueError):
        pass
    if ficha.get("categoria") in CATEGORIAS_DE_ORIGEN_ANIMAL:
        return True
    n = ficha["nombre"].lower()
    return any(x in n for x in NOMBRES_DE_ORIGEN_ANIMAL)


# ⚠️ LAS CELDAS QUE SE QUEDAN EN HUECO A PROPÓSITO, LEÍDAS DEL BLOQUE 51.
#
# No es un olvido: es una decisión del 8 de septiembre con medidas detrás, y el
# motivo va al revés de lo que parece. Un valor BAJO declarado DEFIENDE contra un
# techo, porque cuenta como medido; un hueco se imputa al PERCENTIL 90 de su
# familia (`constructor.valor_para_maximo`). Así que el hueco es lo CONSERVADOR
# contra un máximo, y rellenarlo con una cifra baja lo AFLOJA. Los dos techos en
# juego son crónicos: la vitamina D y el cobre de la hepatopatía.
#
# ⚠️ Y ESTE BARRIDO APORTÓ ALGO QUE NO SE SABÍA: cuatro de esas celdas SÍ tienen
# cifra publicada por una fuente con mandato (Bacalao cobre 0,028 y vitD 0,9 de
# USDA, Perca manganeso 0,7 de USDA, Calamar vitD 0,36 de CIQUAL). El 8 de
# septiembre lo que se sabía era que BEDCA no las publica, y de ahí se concluyó
# «no hay cifra». Sigue siendo más seguro el hueco, pero el argumento cambia: ya
# no es «no hay dato» sino «hay dato y preferimos el lado seguro». Eso es clínico
# y se pregunta, no se decide aquí. Ver `fuentes_de_composicion.json`.
#
# La lista SE LEE de `pruebas_completas.py` y no se copia: dos listas de lo mismo
# se desincronizan, que es el fallo que este repo lleva avisado en veinte sitios.
def _celdas_intocables():
    """(nombre, clave) que el BLOQUE 51 exige en `sin_dato`, leídas de allí."""
    import re
    ruta = os.path.join(RAIZ, "pruebas_completas.py")
    try:
        texto = open(ruta, encoding="utf-8").read()
    except OSError:
        return set()
    fuera = set()
    for nombre_lista in ("_MUESTRA51", "_TR51"):
        i = texto.find(nombre_lista + " = [")
        if i < 0:
            continue
        j = texto.find("]", i)
        for n, k in re.findall(r'\("([^"]+)",\s*"([^"]+)"\)', texto[i:j]):
            fuera.add((n, k))
    return fuera


# Fichas cuyas celdas NO se rellenan desde su fila, con el motivo.
NO_RELLENAR = {
    "Dorada": ("su fila de BEDCA (815) SE CONTRADICE A SÍ MISMA: da proteína 17 y grasa 7,22, "
               "que por 4 y por 9 son 133 kcal, y la misma fila declara 77,9. Es el caso de «dos "
               "alimentos en una fila» que ya cita `UNIDADES.md`. Nuestra ficha sí es coherente "
               "(17×4+1×9=77), así que aquí corregir hacia la fuente sería corregir hacia el error."),
    "Col lombarda": ("la identidad cuadra pero las cifras no: nuestros números no salen de BEDCA "
                     "2400, se separan hasta un 17 %. Rellenar huecos desde una fila que no es la "
                     "que sembró la ficha mezcla dos mediciones en una columna."),
}


def cerrar():
    decl = json.load(open(DECLARACION, encoding="utf-8"))
    if not os.path.exists(INSTANTANEA):
        print("Falta la instantánea."); return 2
    inst = json.load(open(INSTANTANEA, encoding="utf-8"))["alimentos"]
    porn = decl["unidades"]["por_nutriente"]
    huesos = _fichas_de_hueso()
    catalogo = json.load(open(CATALOGO, encoding="utf-8"),
                         object_pairs_hook=collections.OrderedDict)
    hoy = "2026-09-13"
    intocables = _celdas_intocables()
    if not intocables:
        print("  ⚠️ no se han podido leer las celdas intocables del BLOQUE 51. Se aborta: "
              "rellenarlas aflojaría los techos crónicos de la vitamina D y del cobre.")
        return 2
    puestas = saltadas = puestas_cero = declarados = deshechas = grasa_pura = 0
    resumen = collections.Counter()
    resumen_cero = collections.Counter()
    resumen_hueco = collections.Counter()
    dudas = []

    for ficha in catalogo:
        nombre = ficha["nombre"]
        if ficha["categoria"] in CATEGORIAS_DE_ETIQUETA or nombre in NOMBRES_DE_ETIQUETA:
            continue
        if nombre in NO_RELLENAR:
            continue
        fuentes = inst.get(nombre) or {}
        if not fuentes:
            continue
        es_hueso = nombre in huesos
        huecos = set(ficha.get("sin_dato") or [])
        ciertos = set(ficha.get("cero_verificado") or {})
        dudosos = set(ficha.get("dato_dudoso") or {})
        nut = ficha["nutrientes"]
        proc = ficha.get("composicion_fuente") or collections.OrderedDict()
        ciertos_nuevos = collections.OrderedDict()

        for clave in porn:
            meta = porn[clave]
            if meta.get("ninguna_de_las_bases_lo_publica") or meta.get("conflicto_de_convenio"):
                continue
            if es_hueso and clave in ("calcio", "fosforo"):
                continue
            if clave not in nut or clave in ciertos or clave in dudosos:
                continue
            if (nombre, clave) in intocables:
                continue            # el BLOQUE 51 la quiere en hueco, y con motivo
            era_hueco = clave in huecos
            actual = _num(nut.get(clave))
            if not era_hueco and actual not in (None, 0):
                continue                      # ya tiene cifra: no es nuestro caso

            for fuente in _orden_para(decl, clave, es_hueso):
                d = fuentes.get(fuente) or {}
                celda = (d.get("celdas") or {}).get(clave)
                if not celda:
                    continue
                v = _num(celda.get("valor"))
                uni_esp, factor = _unidad_esperada(decl, clave, fuente)
                uni_real = celda.get("unidad")
                if uni_real and uni_esp and uni_real.strip().lower() != str(uni_esp).strip().lower():
                    continue
                if v is None or factor is None:
                    continue
                valor = v * factor
                # --- la transferencia por gramo de proteína o de grasa ---
                escala = ESCALAR_POR.get(clave)
                nota_escala = ""
                if escala:
                    suyo_base = _num((d.get("celdas") or {}).get(escala, {}).get("valor"))
                    nuestro_base = _num(nut.get(escala))
                    suelo = SUELO_PARA_ESCALAR[escala]
                    if (suyo_base and nuestro_base and suyo_base >= suelo
                            and nuestro_base >= suelo):
                        razon = nuestro_base / suyo_base
                        if abs(razon - 1.0) > 0.02:
                            valor = valor * razon
                            nota_escala = (f" · transferido por gramo de {escala}: "
                                           f"{v}×{factor:g}×({nuestro_base}/{suyo_base})")
                valor = round(valor, 6)
                de_donde = (f"{fuente}:{d.get('id')} · «{d.get('fila')}» · columna "
                            f"«{celda.get('columna')}» = {v} {uni_real or uni_esp}")

                # --- el cero de la fuente: se declara, no se escribe a secas ---
                if valor == 0:
                    if _es_tejido_animal(ficha) and clave in CERO_NO_CREIBLE_EN_ANIMAL:
                        dudas.append(
                            f"{nombre} · {clave}: {fuente} publica 0 (tipo "
                            f"{celda.get('value_type') or '?'}) y es TEJIDO animal, donde ese "
                            f"cero NO ES CREÍBLE (criterio de UNIDADES.md). "
                            f"Nuestro valor: {actual}. NO se toca. Fila: «{d.get('fila')}»")
                        break
                    if actual not in (None, 0):
                        dudas.append(
                            f"{nombre} · {clave}: {fuente} publica 0 y nosotros {actual}. "
                            f"NO se sobrescribe un número con un cero -- eso lo decide una "
                            f"persona. Fila: «{d.get('fila')}»")
                        break
                    nut[clave] = 0
                    huecos.discard(clave)
                    ciertos_nuevos[clave] = (
                        f"Cero de la fuente que manda, comprobado el {hoy}: {de_donde}. "
                        f"`value_type` {celda.get('value_type') or 'sin tipo'}, o sea una MEDIDA "
                        f"y no una celda vacía.")
                    puestas_cero += 1
                    resumen_cero[clave] += 1
                    break

                nut[clave] = valor
                if era_hueco:
                    huecos.discard(clave)
                proc[clave] = (de_donde
                               + f"{'' if factor == 1 else f' ×{factor:g}'}{nota_escala}"
                               + f" → {valor} {meta['catalogo']} · {hoy}")
                puestas += 1
                resumen[clave] += 1
                break
            else:
                saltadas += 1

        # ── Y LO CONTRARIO: un 0 que la fuente dice que NO TIENE CIFRA ──
        # BEDCA es la única de las cuatro que sabe decirlo: `TR` con la celda
        # vacía significa «no hay número», no «vale cero». Al volcar BEDCA a una
        # tabla ese TR se convierte en 0 y deja de verse -- seis de los huecos
        # que se cerraron el 7 de septiembre eran exactamente esto.
        # Aquí el 0 se queda (el motor necesita un número), pero se DECLARA en
        # `sin_dato`, que es lo que hace que salga en `datos_incompletos` junto
        # al menú y que contra un MÁXIMO se impute por familia en vez de contar
        # como «no aporta».
        bedca = ((fuentes.get("bedca") or {}).get("celdas") or {})
        for clave, celda in bedca.items():
            if (celda.get("value_type") or "").upper() != "TR" or celda.get("valor"):
                continue
            if clave not in nut or clave in ciertos or clave in dudosos:
                continue
            if clave in (ficha.get("composicion_fuente") or {}):
                continue                  # se cerró desde otra fuente: ya no es hueco
            if _num(nut.get(clave)) not in (None, 0):
                continue                  # tiene cifra de otro sitio: no es un hueco
            # ⚠️ En una grasa pura, ese cero no es un hueco: es cierto por
            # composición. Declararlo hueco hace que se impute al percentil 90 de
            # su familia, y la familia de un aceite incluye semillas.
            if _es_grasa_pura(ficha) and clave in CERO_CIERTO_EN_GRASA_PURA:
                if clave not in ciertos:
                    ciertos_nuevos[clave] = (
                        f"Cero cierto por composición, comprobado el {hoy}: la ficha es grasa "
                        f"pura ({nut.get('grasa')} g por 100 g) y el {clave} no viaja en grasa. "
                        f"BEDCA lo deja con `value_type` TR y la celda vacía —que es «no hay "
                        f"cifra»— pero aquí lo decide la composición: un aceite refinado son "
                        f"triglicéridos. Lo que una grasa SÍ lleva son las vitaminas "
                        f"liposolubles (A, D, E) y los ácidos grasos, y esos NO entran en esta "
                        f"regla.")
                    grasa_pura += 1
                huecos.discard(clave)
                continue
            if clave not in huecos:
                huecos.add(clave)
                declarados += 1
                resumen_hueco[clave] += 1

        # ── EL GUARDIA DE GRUPO: una fracción no puede pasar de su total ──
        #
        # ⚠️ CASO REAL, Y LO CAUSÓ ESTE MISMO SCRIPT EL 13 DE SEPTIEMBRE. A la
        # ZANAHORIA se le puso el aminograma de USDA 170393 «Carrots, raw», cuyos
        # doce aminoácidos suman 0,89 g — sobre una proteína nuestra de 0,8 g. Eso
        # es el 111 % de la proteína y es imposible: los doce aminoácidos SON una
        # fracción de ella.
        #
        # Y el escalado por gramo de proteína no lo salvó, por un detalle del
        # suelo: `SUELO_PARA_ESCALAR["proteina"]` es 1,0 g y la zanahoria tiene
        # 0,8, así que la transferencia se saltó. Aunque se hubiera aplicado no
        # bastaba: la propia fila de USDA suma el 96 % de SU proteína (0,89 sobre
        # 0,93), o sea que la incoherencia viene de la fuente y no de la escala.
        #
        # Un aminograma se escribe ENTERO o no se escribe: celda a celda no hay
        # forma de ver que la suma se pasa. Así que si el grupo no cae en la banda
        # del 25-85 % que pide `UNIDADES.md`, se deshace el grupo completo y la
        # ficha se queda con sus huecos, que es la respuesta honesta.
        # ⚠️ SON DOS REGLAS Y NO UNA, y confundirlas acusa a fichas correctas.
        #   · LA SUMA NO PUEDE PASAR DEL TOTAL: siempre, en cualquier ficha. Es
        #     una imposibilidad aritmética, no un criterio.
        #   · LA BANDA DEL 25-85 %: solo donde hay proteína DE VERDAD.
        #     `UNIDADES.md` lo dice con esas palabras («en cualquier alimento con
        #     proteína de verdad»), y con razón: la manzana tiene 0,3 g de
        #     proteína y 0,073 g de aminoácidos, o sea el 24,3 %, y eso no es un
        #     error -- es que con cifras tan pequeñas el cociente no significa
        #     nada. La primera versión de este guardia no hacía la distinción y
        #     señalaba la manzana, que no tiene nada que ver con el caso de la
        #     zanahoria (111 %).
        SUELO_PARA_LA_BANDA = {"proteina": 1.0, "grasa": 1.0}
        for grupo, total_clave, banda in (
                (AMINOACIDOS, "proteina", (0.25, 0.85)),
                (ACIDOS_GRASOS, "grasa", (0.0, 1.0))):
            puestas_del_grupo = [k for k in grupo if k in proc]
            if not puestas_del_grupo:
                continue
            total = _num(nut.get(total_clave)) or 0
            if total <= 0:
                continue
            suma = sum((_num(nut.get(k)) or 0) * (0.001 if k == "araquidonico" else 1)
                       for k in grupo)
            razon = suma / total
            pasa_del_total = razon > 1.02
            fuera_de_banda = (total >= SUELO_PARA_LA_BANDA[total_clave]
                              and not (banda[0] <= razon <= banda[1]))
            if not pasa_del_total and not fuera_de_banda:
                continue
            for k in puestas_del_grupo:
                nut[k] = 0
                proc.pop(k, None)
                huecos.add(k)
                deshechas += 1
            dudas.append(
                f"{nombre}: el grupo «{total_clave}» se DESHACE entero. Los "
                f"{len(puestas_del_grupo)} valores que publicaba la fuente suman {suma:.3f} g "
                f"sobre {total:g} g de {total_clave} ({razon*100:.0f} %). "
                + ("PASA DEL TOTAL, que es imposible." if pasa_del_total
                   else f"Fuera de la banda plausible {banda[0]*100:.0f}-{banda[1]*100:.0f} %.")
                + " Se queda en hueco.")

        if proc:
            ficha["composicion_fuente"] = collections.OrderedDict(sorted(proc.items()))
        elif "composicion_fuente" in ficha:
            del ficha["composicion_fuente"]
        if ciertos_nuevos:
            todos = dict(ficha.get("cero_verificado") or {})
            todos.update(ciertos_nuevos)
            ficha["cero_verificado"] = collections.OrderedDict(sorted(todos.items()))
        ficha["sin_dato"] = sorted(huecos) if huecos else []
        if not ficha["sin_dato"]:
            del ficha["sin_dato"]

    with open(CATALOGO, "w", encoding="utf-8") as fh:
        json.dump(catalogo, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    print(f"  celdas con CIFRA de la fuente: {puestas}")
    print("    " + ", ".join(f"{k}:{v}" for k, v in resumen.most_common()))
    print(f"  ceros declarados con su fuente (`cero_verificado`): {puestas_cero}")
    print("    " + ", ".join(f"{k}:{v}" for k, v in resumen_cero.most_common(14)))
    print(f"  huecos DECLARADOS (la fuente dice que no hay cifra): {declarados}")
    if grasa_pura:
        print(f"  ceros CIERTOS en grasa pura (no son huecos): {grasa_pura}")
    if deshechas:
        print(f"  celdas DESHECHAS por el guardia de grupo: {deshechas}")
    if resumen_hueco:
        print("    " + ", ".join(f"{k}:{v}" for k, v in resumen_hueco.most_common(14)))
    if dudas:
        print(f"\n  ⚠️ {len(dudas)} celdas NO TOCADAS porque el cero de la fuente no se obedece "
              f"a ciegas:")
        for d in dudas:
            print(f"     · {d}")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__.split("\n")[2])
    p.add_argument("--instantanea", action="store_true",
                   help="baja las fuentes y escribe fuentes_instantanea.json (necesita red)")
    p.add_argument("--cerrar", action="store_true",
                   help="ESCRIBE en el catálogo: rellena los huecos y los ceros mudos que la "
                        "fuente que manda sí publica, con la procedencia de cada celda")
    a = p.parse_args()
    if a.instantanea:
        return construir_instantanea()
    return cerrar() if a.cerrar else auditar()


if __name__ == "__main__":
    sys.exit(main())
