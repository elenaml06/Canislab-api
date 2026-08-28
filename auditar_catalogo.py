# -*- coding: utf-8 -*-
"""
Audita el catálogo de alimentos por dentro, sin fuentes externas.

Existe porque el 21 de agosto, revisando si los nutrientes se medían en la
base correcta, aparecieron seis alimentos con huecos de datos que nadie
había declarado -- incluido un pescado azul con el omega-3 a cero y una
víscera con el 90% de su composición sin dato. Ninguna prueba del motor
podía detectarlo: el motor cumplía perfectamente unos datos incompletos.

Las cuatro comprobaciones que hace, y por qué cada una:

1. COHERENCIA ENERGETICA. Contrasta la energía declarada de cada alimento
   contra sus macros por Atwater. Si los nutrientes vinieran en materia
   seca y las kcal en fresco (o al revés), el ratio se dispararía. Es la
   forma de comprobar que todo el catálogo está en la misma base, que es
   lo que hace válido el cálculo "por 1000 kcal".

2. HUECOS SIN DECLARAR. Un cero puede significar "no lo tiene" o "no lo
   sabemos", y la diferencia es asimétrica: en los mínimos, contar un
   hueco como cero es conservador; en los MAXIMOS deja pasar un exceso sin
   detectarlo. El campo sin_dato existe para distinguirlos, y esto avisa
   de los alimentos donde no se ha usado.

3. PLAUSIBILIDAD POR CATEGORIA. Un hígado sin vitamina A, un hueso sin
   calcio o una carne con calcio de hueso son errores que ningún test
   numérico pilla, porque cada valor por separado es válido.

4. CUELLOS DE BOTELLA. Cuántos alimentos quedan por categoría al excluir
   especies. Es lo que decide si un perro con alergias se queda sin menú.

    python3 auditar_catalogo.py
"""
import json, collections, sys, os

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "motor"))
RUTA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "alimentos_v3_final.json")
al = json.load(open(RUTA, encoding="utf-8"))
def nut(a, k): return (a.get("nutrientes") or {}).get(k, 0) or 0
def es_grasa(a): return nut(a, "grasa") > 80          # aceites: sus ceros son reales
SUPLEMENTOS = ("Multivitamínico", "Vitamina B", "Hierro", "Calcio", "Yodo", "Fibra", "Omega-3")

def _envolver(texto, ancho):
    """Parte un texto largo en lineas, para que la lista de marcas se pueda leer."""
    palabras, lineas, actual = texto.split(), [], ""
    for w in palabras:
        if len(actual) + len(w) + 1 > ancho:
            lineas.append(actual); actual = w
        else:
            actual = (actual + " " + w).strip()
    if actual:
        lineas.append(actual)
    return lineas


avisos = []

# ── 1. coherencia energética ──────────────────────────────────────────
for a in al:
    e = a.get("energia", 0)
    if not e: continue
    calc = 4 * nut(a, "proteina") + 9 * nut(a, "grasa")
    if calc > e * 1.15:
        avisos.append(("BASE", a["nombre"],
                       f"los macros dan {calc:.0f} kcal pero declara {e} "
                       f"(ratio {calc/e:.2f}) — ¿nutrientes en seco y kcal en fresco?"))

# ── 2. huecos sin declarar ────────────────────────────────────────────
for a in al:
    n = a.get("nutrientes") or {}
    if not n or es_grasa(a) or a.get("categoria") in SUPLEMENTOS: continue
    sd = set(a.get("sin_dato") or [])
    # ⚠️ UN CERO CON FUENTE ESCRITA NO ES UN HUECO (28 agosto). Las purinas
    # de un huevo son CERO de verdad -- "Egg, chicken, raw" da 0,0 en las
    # cuatro bases -- y las de un aceite tambien, porque no tiene celulas.
    # Ese cero lleva su procedencia en `purinas_fuente`, asi que es un valor
    # medido y no una celda vacia. Contarlo como hueco empujaba al huevo de
    # pato de 9 ceros a 10 y disparaba este aviso por un dato que SI
    # tenemos, que es justo lo contrario de lo que vigila.
    if a.get("purinas_fuente"):
        sd = sd | {"purinas"}
    sin_declarar = [k for k, v in n.items() if not v and k not in sd]
    if len(sin_declarar) >= 10:
        avisos.append(("HUECOS", a["nombre"],
                       f"{len(sin_declarar)} nutrientes a cero sin declarar en sin_dato: "
                       + ", ".join(sin_declarar[:8]) + ("…" if len(sin_declarar) > 8 else "")))

# ── 2b. OMEGA-6 CONTRA OMEGA-3: los dos que se llaman casi igual ──────
#
# `linoleico` es omega-6 (C18:2) y `linolenico` es omega-3 (C18:3). Se
# diferencian en una letra y son cosas opuestas. Si alguien los cambia al
# cargar una tabla, NADA salta: los dos son nutrientes validos y los dos
# valores son plausibles, asi que el menu sale verde igual y el motor cree
# que equilibra el omega-3 con un aceite que no lo tiene.
#
# En la comida de verdad el omega-6 casi siempre gana, porque el omega-3
# de cadena corta esta concentrado en muy pocos alimentos. Que el omega-3
# supere al omega-6 no es un error -- pasa en el lino, en los aceites de
# salmon y en algun pescado magro -- pero es raro, y una lista corta se
# puede repasar a ojo. Si un dia esa lista se llena, es que se han
# invertido las columnas.
for a in al:
    n = a.get("nutrientes") or {}
    w6, w3 = n.get("linoleico") or 0, n.get("linolenico") or 0
    if w3 > w6 and (w6 or w3):
        avisos.append(("OMEGA", a["nombre"],
                       f"omega-3 ({w3} g) por encima del omega-6 ({w6} g). Es posible, pero "
                       f"revisa que no esten cambiados: linoleico=omega-6, linolenico=omega-3"))

# ── 2c. LOS GRASOS TIENEN QUE CABER DENTRO DE LA GRASA ────────────────
#
# El linoleico, el linolenico, el EPA y el DHA son PARTES de la grasa
# total, asi que sumados no pueden pasarse de ella. Es una ley fisica, no
# un criterio: si se pasan, el dato esta mal.
#
# Esto existe por la trampa de las unidades, que es la que mas se cuela:
# casi todas las tablas de composicion dan el EPA y el DHA en MILIGRAMOS y
# nosotros los guardamos en GRAMOS. Cargar la sardina con epa=254 en vez
# de 0.254 pondria 930 g de acidos grasos dentro de 7,5 g de grasa --
# imposible, y hasta ahora nada lo miraba. El menu habria salido verde: el
# EPA+DHA es un nutriente con minimo, y pasarse de largo no lo rompe.
#
# El araquidonico va en mg a proposito (asi lo da FEDIAF), por eso se
# divide entre 1000 antes de sumarlo.
#
# Margen del 5%: los valores vienen de fuentes distintas y de analisis
# distintos, asi que un pelo por encima no es un error de carga.
for a in al:
    n = a.get("nutrientes") or {}
    grasa = n.get("grasa") or 0
    if not grasa:
        continue
    suma = sum(n.get(k) or 0 for k in ("linoleico", "linolenico", "epa", "dha"))
    suma += (n.get("araquidonico") or 0) / 1000.0
    if suma > grasa * 1.05 and suma - grasa > 0.05:
        avisos.append(("GRASOS", a["nombre"],
                       f"los acidos grasos suman {suma:.2f} g y la grasa total es {grasa} g. "
                       f"No caben. Lo mas probable: EPA/DHA cargados en mg en vez de g"))

# ── 2d. DATO DUDOSO: el valor que SI esta y no nos lo creemos ─────────
#
# `sin_dato` marca los HUECOS, y los huecos son peligrosos por el lado del
# maximo. Pero un valor DECLARADO Y ERRONEO no dejaba rastro en ninguna
# parte, y es peor: tiene la forma de un dato bueno, asi que pasa cualquier
# validacion de formato.
#
# ⚠️ CASO REAL (27 agosto): tres a la vez, los tres de etiquetas reales.
# El omega-3 TOTAL de cuatro aceites de salmon guardado en `linolenico`
# (que es solo el ALA: el EPA y el DHA se contaban dos veces); el fosforo
# de las dos harinas de hueso, con un Ca:P de 1,28 cuando la hidroxiapatita
# da 2,15 por estequiometria; y el cobre del polvo de sangre, 150 veces por
# encima de lo que tiene la sangre desecada. Los tres pasaban las cuatro
# comprobaciones de arriba. Entraron por columnas cuyo nombre se parece al
# de la etiqueta lo bastante como para que nadie mire.
#
# Los que se pudieron arreglar, se arreglaron. Los que no —porque el valor
# es el de la etiqueta y el real no esta publicado— llevan `dato_dudoso`,
# y esto los lista para que nadie los olvide.
for a in al:
    for k, d in (a.get("dato_dudoso") or {}).items():
        valor = (a.get("nutrientes") or {}).get(k)
        avisos.append(("DUDOSO", a["nombre"],
                       f"{k}={valor} declarado pero no creible. {d.get('motivo','')[:150]}"))

# ── 2e. EL CERO BIOLOGICAMENTE IMPOSIBLE ──────────────────────────────
#
# La comprobacion 2 pilla los ceros SIN DECLARAR contandolos en bloque
# (10 o mas). Se le escapaban los sueltos, y los sueltos son los que hacen
# dano: un higado sin fosforo pasa desapercibido entre 30 valores buenos.
#
# ⚠️ CASO REAL ENCONTRADO (27 agosto): `Testículos de cordero` tenia 30 de
# sus 31 nutrientes a cero, `sin_dato` VACIO y 68 kcal con proteina 0 y
# grasa 0 -- la fila se contradecia sola, porque esa energia no puede salir
# de ningun sitio. Para el solver era una fuente de vitamina B12 que no
# costaba nada en ningun otro presupuesto, y MEDIDO la usaba en 2 de cada
# 24 menus automaticos, uno con 90,5 gramos. Cada uno de esos gramos dejaba
# la racion corta de todo lo demas, y el semaforo salia VERDE porque
# verifica contra estos mismos datos. El alimento se quito del catalogo.
#
# El criterio, que no necesita ninguna fuente externa: un cero solo es
# creible si algun alimento de esa familia puede tenerlo de verdad.
CLAVES_TEJIDO = ("potasio", "fosforo", "magnesio", "sodio", "cloruro",
                 "hierro", "zinc", "proteina")
ANIMAL = ("Carne muscular", "Vísceras", "Hígado", "Pescados y mariscos", "Hueso carnoso")
for a in al:
    if a.get("categoria") not in ANIMAL:
        continue
    n = a.get("nutrientes") or {}
    sd = set(a.get("sin_dato") or [])
    malos = [k for k in CLAVES_TEJIDO + ("vitB12",) if not nut(a, k) and k not in sd]
    if malos:
        avisos.append(("CERO0", a["nombre"],
                       f"tejido animal con {', '.join(malos)} a cero y sin declarar. "
                       f"Un tejido no tiene NUNCA esos a cero; si no lo sabemos, va en sin_dato"))
    # y la energia de un alimento animal solo puede venir de sus macros:
    # no hay hidratos que la expliquen, como si pasa en la fruta
    e = a.get("energia") or 0
    calc = 4 * nut(a, "proteina") + 9 * nut(a, "grasa")
    if e > 20 and calc < e * 0.35:
        avisos.append(("CERO0", a["nombre"],
                       f"declara {e} kcal pero sus macros solo dan {calc:.0f}. En un alimento "
                       f"animal no hay hidratos que expliquen la diferencia: la fila se "
                       f"contradice sola y el motor la usaria creyendola vacia"))

# ── 2f. EL CLORURO NO ES UNA MEDIDA, ES EL SODIO x 1,542 ──────────────
#
# Encontrado el 27 de agosto revisando la carga: en la inmensa mayoria de
# las filas con los dos valores, `cloruro` = `sodio` x 1,542 EXACTO, que es
# la razon entre los pesos atomicos del cloro y del sodio. O sea que la
# columna no es un analisis: es el sodio reescrito SUPONIENDO que todo el
# sodio del alimento viene de sal comun.
#
# En tejido animal la suposicion se sostiene a medias. En VEGETALES es
# sistematicamente falsa, porque el cloruro de la planta va sobre todo con
# potasio y no con sodio -- CIQUAL, que si lo analiza, da 61 mg para el
# champinon donde la derivacion da 7,7, y 45 para los canonigos donde da
# 6,2. Factores de 6x a 8x.
#
# No se corrige aqui porque cambiar la columna entera es una decision, no
# un arreglo. Esto solo impide que se olvide lo que es.
_der = [a["nombre"] for a in al
        if nut(a, "sodio") and nut(a, "cloruro")
        and abs(nut(a, "cloruro") / nut(a, "sodio") - 1.542) < 0.005]
if _der:
    avisos.append(("CLORURO", "(columna entera)",
                   f"{len(_der)} alimentos tienen cloruro = sodio x 1,542 exacto. La columna "
                   f"es una DERIVACION del sodio, no una medida, y en vegetales es falsa "
                   f"(CIQUAL mide 6-8 veces mas). Decidido dejarla asi por ahora"))

# ── 3. plausibilidad por categoría ────────────────────────────────────
for a in al:
    c, nombre = a.get("categoria"), a["nombre"]
    sd = set(a.get("sin_dato") or [])
    if c == "Hígado" and nut(a, "vitA") < 1000 and "vitA" not in sd:
        avisos.append(("RARO", nombre, f"hígado con vitA={nut(a,'vitA')} (rondan 5.000-20.000 µg)"))
    if c == "Hueso carnoso" and nut(a, "calcio") < 400:
        avisos.append(("RARO", nombre, f"en 'Hueso carnoso' con calcio={nut(a,'calcio'):.0f} mg — "
                                       f"los huesos de verdad traen 1.250-1.810. ¿Es hueso o cartílago?"))
    if c == "Carne muscular" and nut(a, "calcio") > 300:
        avisos.append(("RARO", nombre, f"carne muscular con calcio={nut(a,'calcio'):.0f} mg — ¿lleva hueso?"))
    if c == "Pescados y mariscos" and not nut(a, "epa") and not nut(a, "dha") and "epa" not in sd:
        avisos.append(("RARO", nombre, "pescado con EPA y DHA a cero sin declarar"))

# ── 4. cuellos de botella ─────────────────────────────────────────────
from motor_completo import especie_de
CLAVE = ("Carne muscular", "Hueso carnoso", "Vísceras", "Hígado")
print("CUELLOS DE BOTELLA — cuántos alimentos quedan al excluir especies")
print("(las categorías con mínimo obligatorio son las que dejan sin menú)")
for excl in ([], ["Pollo"], ["Pollo", "Ternera"], ["Pollo", "Ternera", "Cordero"],
             ["Pollo", "Ternera", "Cordero", "Cerdo", "Pavo"]):
    quedan = {c: len([a for a in al if a.get("categoria") == c
                      and especie_de(a["nombre"]) not in excl]) for c in CLAVE}
    critico = [c for c, n in quedan.items() if n <= 2]
    print("   %d alergias: %s%s" % (len(excl),
          "  ".join(f"{c.split()[0]}={n}" for c, n in quedan.items()),
          "   <<< al límite: " + ", ".join(critico) if critico else ""))

# ── 5. datos sin verificar contra su fuente original ──────────────────
# Lo mas importante de un dato de nutricion no es el numero: es de donde
# sale. Un valor recuperado de un espejo puede estar bien, pero nadie lo
# ha comprobado, y eso tiene que poder LISTARSE en cualquier momento en
# vez de vivir enterrado en una nota que nadie relee.
sin_verificar = [a for a in al if (a.get("procedencia") or {}).get("verificado_contra_original") is False]
if sin_verificar:
    print()
    print("DATOS SIN VERIFICAR CONTRA SU FUENTE ORIGINAL")
    for a in sin_verificar:
        p = a["procedencia"]
        print("   %-26s nivel=%-9s %s" % (a["nombre"][:26], p.get("nivel"), p.get("fuente_declarada","")))
        for x in p.get("deducidos", []):
            print("      DEDUCIDO, no leido: %s" % x)

# =====================================================================
# EL AMINOGRAMA: QUIEN LO TIENE Y QUIEN NO
# =====================================================================
#
# ⚠️ AÑADIDO (28 agosto). Los doce aminoacidos esenciales estan en la
# tabla de FEDIAF desde el 26 de agosto y NO se verifican, porque el
# catalogo no traia el dato. Hoy 49 fichas si lo traen, y la pregunta ha
# cambiado: ya no es "¿hay dato?", es "¿a QUIEN le falta?".
#
# Importa la respuesta por categoria y no el total, porque un alimento sin
# aminograma no cuenta como "no lo se": cuenta como CERO. Si al activar
# los requisitos el hueso carnoso entero cuenta como cero de lisina, el
# motor lo evita para llegar al minimo -- y el menu sale verde, porque el
# semaforo mide el mismo cero. El total no dice nada de eso; la lista por
# categoria, si.
#
# Por debajo de 3 g de proteina por 100 g no se cuenta: la manzana tiene
# 0,3 y la zanahoria 0,37, y su aminograma no mueve una racion carnica.
AA_AUDIT = ["arginina", "histidina", "isoleucina", "leucina", "lisina", "metionina",
            "cistina", "fenilalanina", "tirosina", "treonina", "triptofano", "valina"]
PROTEINA_QUE_CUENTA = 3.0
_falta_aa = {}
for a_ in al:
    if nut(a_, "proteina") < PROTEINA_QUE_CUENTA:
        continue
    huecos = set(a_.get("sin_dato") or [])
    nutr = a_.get("nutrientes") or {}
    if any(k in huecos or k not in nutr for k in AA_AUDIT):
        _falta_aa.setdefault(a_.get("categoria", "?"), []).append(a_["nombre"])
# =====================================================================
# LO QUE UNA SEGUNDA MAGNITUD PREDICE DE LA PRIMERA
# =====================================================================
#
# ⚠️ AÑADIDO (28 agosto). De los cuatro fallos de datos de hoy, NINGUNO
# daba error y los cuatro pasaban cualquier validacion de formato: el
# triptofano en miligramos, `Lenguado` cogiendo la ficha de la lengua de
# vacuno, el higado de ternera cogiendo musculo generico, y el peso
# objetivo que no llegaba al solver. Los cuatro «funcionaban».
#
# Lo unico que los cazo fue una comprobacion de COHERENCIA: una segunda
# magnitud independiente que predice la primera. La suma de los doce
# aminoacidos predice la proteina. La suma de las cuatro bases predice las
# purinas totales. El calcio predice cuanto hueso lleva la pieza.
#
# Donde no exista esa segunda magnitud, hay que inventarla ANTES de
# cargar, no despues.
AA_COH = ["arginina", "histidina", "isoleucina", "leucina", "lisina", "metionina",
          "cistina", "fenilalanina", "tirosina", "treonina", "triptofano", "valina"]

for a_ in al:
    n_ = a_.get("nutrientes") or {}
    sd_ = set(a_.get("sin_dato") or [])
    nom_ = a_["nombre"]
    prot_ = nut(a_, "proteina")
    cat_ = a_.get("categoria")

    # ── El hueso carnoso tiene que tener hueso ──────────────────────────
    # Las fichas de USDA de cuello de pollo NO llevan el hueso: 18 mg de
    # calcio contra los 1.700 del cuello entero. Un factor de 94. Si
    # alguna fila de hueso carnoso viniera de USDA, BEDCA, CIQUAL o
    # FINELI -todas dan PORCION COMESTIBLE- estaria mal por dos ordenes
    # de magnitud y el menu saldria verde igual, porque 18 mg es un
    # numero perfectamente plausible para una carne.
    # La LARINGE es la excepcion conocida y esta bien: es cartilago, no
    # hueso, asi que no esta mineralizada y el calcio no la ve. Es la misma
    # pieza que se deja sin aminograma a proposito.
    if cat_ == "Hueso carnoso" and nom_ != "Laringe de vacuno":
        ca_, fo_ = nut(a_, "calcio"), nut(a_, "fosforo")
        if ca_ and ca_ < 400:
            avisos.append(("HUESO", nom_,
                           f"{ca_:.0f} mg de calcio/100 g y es hueso carnoso. Por debajo de 400 la "
                           f"ficha es de porcion comestible SIN hueso (el cuello de pollo del USDA "
                           f"da 18 contra 1.700 del cuello entero)"))
        if ca_ and fo_:
            r_ = ca_ / fo_
            if not (1.3 <= r_ <= 2.2):
                avisos.append(("HUESO", nom_,
                               f"Ca:P = {r_:.2f}. La hidroxiapatita da 2,15 por estequiometria; por "
                               f"debajo de 1,3 hay carne de mas o el dato esta mal"))

    # ── El aminograma tiene que parecerse a una proteina ────────────────
    tiene_aa = prot_ > 0 and not (set(AA_COH) & sd_) and all(k in n_ for k in AA_COH)
    if tiene_aa:
        suma_ = sum(n_.get(k) or 0 for k in AA_COH)
        if prot_ >= 3 and not (0.25 <= suma_ / prot_ <= 0.85):
            avisos.append(("AMINO", nom_,
                           f"los 12 aminoacidos suman {suma_:.2f} g y la proteina son {prot_:.2f}: "
                           f"{suma_/prot_*100:.0f}% de ella, fuera de la banda 25-85%. Es la "
                           f"comprobacion que cazo el triptofano en miligramos"))
        # La isoleucina separa la sangre de todo lo demas: 4,43 g/100 g de
        # proteina en la carne, 1,1 en la harina de sangre y 0,50 en la
        # hemoglobina pura -- NUEVE veces menos. Pegarle a la sangre un
        # aminograma generico de proteina animal la sobreestimaria un 300%.
        if prot_ >= 10:
            ile_ = (n_.get("isoleucina") or 0) / prot_ * 100
            # ⚠️ LAS SIETE FICHAS DE PAVO SALEN AQUI Y ES UN FALLO REAL,
            # encontrado el 28 de agosto por esta misma comprobacion el dia
            # que se puso. Su aminograma viene de «Turkey, ground, raw» del
            # USDA y tiene la isoleucina y la valina un 40% bajas mientras
            # la leucina, la lisina y la treonina salen normales:
            #     Leu/Ile   pollo 1,47 · ternera 1,76 · salmon 1,76
            #               PAVO 2,42
            # Va en la direccion segura -infravalora, asi que el motor
            # compensa- pero esta mal. Pendiente de resembrar desde otra
            # ficha; hasta entonces se listan aqui para que el aviso no
            # cante lo mismo cada vez y tape uno nuevo.
            # ⚠️ EL HIGADO Y EL CORAZON SALIERON DE ESTA LISTA el 28 de
            # agosto: se resembraron desde el pollo del USDA (Leu/Ile 1,86 y
            # 1,63). Si vuelven a bajar del 3%, tienen que volver a cantar.
            PAVO_PENDIENTE = {"Pavo", "Cuello de pavo", "Pavo muslo con piel",
                              "Pavo pechuga con piel", "Pavo pechuga sin piel",
                              "Molleja de pavo", "Molleja de pollo"}
            if ile_ < 3.0 and "sangre" not in nom_.lower() and nom_ not in PAVO_PENDIENTE:
                avisos.append(("AMINO", nom_,
                               f"isoleucina al {ile_:.1f}% de la proteina. Por debajo del 3% solo "
                               f"estan la sangre (1,1) y la hemoglobina (0,50); la carne va a 4,4"))
        # ⚠️ NIVEL 2 — MIRAR LA COLUMNA, NO LA FILA (28 de agosto).
        #
        # Todo lo de arriba pregunta «¿este numero es posible?», y eso caza
        # el valor IMPOSIBLE. No caza el valor INVENTADO, porque quien lo
        # imputa lo hace con proporciones internamente coherentes: cuadra
        # consigo mismo y solo falla contra el resto del mundo.
        #
        # Lo que lo destapa es un COCIENTE entre dos aminoacidos de la misma
        # fila, y por un motivo estructural: un aminograma transferido se
        # reescala por la proteina del destino, asi que cualquier umbral
        # «por gramo de proteina» se mueve con ella -- pero un cociente entre
        # dos aminoacidos de la misma fila no se mueve con nada.
        #
        # Los dos casos reales que lo justifican:
        #   · El pavo del USDA: Leu/Ile = 2,419 en CUATRO tejidos distintos,
        #     a tres decimales. Seis analiticas independientes no dan la
        #     misma constante. Era un perfil unico mal calibrado.
        #   · La resiembra que llego para arreglarlo: histidina = isoleucina
        #     = valina, exactos, en cinco filas. En 91 fichas del catalogo
        #     His/Ile tiene mediana 0,601 y NINGUNA vale 1,000. Tres
        #     aminoacidos distintos con el mismo numero son una copia.
        # Ninguno de los dos lo cazaba el umbral de isoleucina de arriba.
        if prot_ >= 10 and (n_.get("isoleucina") or 0) > 0:
            ile2_ = n_["isoleucina"]
            leu_ile = (n_.get("leucina") or 0) / ile2_
            # La banda sale del catalogo medido: 42 de 45 entre 1,16 y 1,98,
            # con la col rizada (1,16) como borde bajo real.
            if not (1.10 <= leu_ile <= 2.05) and nom_ not in PAVO_PENDIENTE:
                avisos.append(("AMINO", nom_,
                               f"Leu/Ile = {leu_ile:.3f}, fuera de 1,10-2,05. Ese cociente no "
                               f"depende de la proteina, asi que sobrevive a un reescalado: "
                               f"fuera de banda casi siempre significa aminograma de otra fuente"))
            for otro in ("histidina", "valina"):
                v_ = n_.get(otro) or 0
                if v_ > 0 and abs(v_ / ile2_ - 1.0) < 0.005:
                    avisos.append(("AMINO", nom_,
                                   f"{otro} e isoleucina valen lo mismo ({v_:.3f}). Son dos "
                                   f"aminoacidos distintos: en 91 fichas ninguna los tiene "
                                   f"iguales. Es una copia, no una medida"))

        # Y el triptofano por los dos lados: cero en colageno puro, y
        # nunca por encima del 2% -- ahi es donde se ve un factor 1.000.
        if prot_ >= 3:
            tri_ = (n_.get("triptofano") or 0) / prot_ * 100
            # El huevo (2,03%) y el sesamo (2,19%) son legitimamente
            # ricos en triptofano; el techo se pone en 2,5 para que el
            # aviso siga sirviendo para lo que existe -- cazar un factor
            # 1.000, no discutir un decimal.
            if not (0.3 <= tri_ <= 2.5):
                avisos.append(("AMINO", nom_,
                               f"triptofano al {tri_:.2f}% de la proteina, fuera de 0,3-2,0%. El "
                               f"colageno tiene CERO y una tabla en miligramos da mil veces mas"))

# ── Las purinas: que el linaje de la tabla sea el bueno ────────────────
# El higado de vacuno es el patron: Souci da 231 y Kaneko 2014 mide 219,8
# por HPLC. Un 5%. Hay compilaciones alemanas que dan 122 para esa misma
# ficha -- y si el higado esta mal, las demas filas de esa tabla no valen
# aunque parezcan razonables.
_hig = next((a_ for a_ in al if a_["nombre"] == "Hígado de vaca"), None)
if _hig:
    _pv = nut(_hig, "purinas")
    # Nuestra cifra viene del USDA («Beef liver, raw», 197) y no de Souci
    # (231) ni de Kaneko (219,8 por HPLC). Un 10% entre metodos es normal;
    # lo que este aviso busca es el linaje MALO -- hay compilaciones
    # alemanas que dan 122 para esta misma ficha, y si el higado esta a la
    # mitad, ninguna otra fila de esa tabla vale.
    if _pv and not (190 <= _pv <= 240):
        avisos.append(("PURINA", "Hígado de vaca",
                       f"{_pv:.0f} mg de purinas. El patron son 200-240 (Souci 231, Kaneko 2014 "
                       f"mide 219,8 por HPLC). Si el higado no cuadra, el linaje de la tabla de "
                       f"donde salio no vale para ninguna otra fila"))

print()
print("═" * 74)
print("SIN AMINOGRAMA, entre los que tienen proteina (>= %.0f g/100 g)" % PROTEINA_QUE_CUENTA)
if not _falta_aa:
    print("   ninguno -- se pueden activar los 12 requisitos de FEDIAF (ver BLOQUE 27)")
else:
    for cat_ in sorted(_falta_aa, key=lambda c: -len(_falta_aa[c])):
        print("   %-26s %d" % (cat_, len(_falta_aa[cat_])))
        for n_ in sorted(_falta_aa[cat_]):
            print("        %s" % n_)

print()
print("═" * 74)
print("AVISOS: %d" % len(avisos))
# ⚠️ DOS ESPACIOS ENTRE EL NOMBRE Y EL DETALLE, Y EL NOMBRE SIN CORTAR.
# CASO REAL (26 agosto): esto era "%-34s %s" con nombre[:34], y el BLOQUE
# 19 lee cada línea con una expresión que separa el nombre del detalle por
# DOS espacios seguidos. Con un nombre de 34 caracteres justos, el relleno
# no añadía nada y solo quedaba el espacio del formato: el aviso de
# "Aceite de Salmón Natural Greatness" se leía mal, y el BLOQUE 19 decía
# que ese hueco había desaparecido cuando seguía ahí. Hay cinco alimentos
# con nombres de 34 o más -- y el corte a 34 además perdía el final de los
# de 38, así que dos alimentos distintos podían leerse como el mismo.
for tipo, nombre, det in avisos:
    print("  [%-6s] %-34s  %s" % (tipo, nombre, det))
# =====================================================================
# LAS MARCAS ABIERTAS, DE LA MAS VIEJA A LA MAS NUEVA
# =====================================================================
#
# Esto NO es un aviso mas: es la unica parte de la auditoria que no
# pregunta "¿esta el dato mal?" sino "¿sigue alguien intentando
# arreglarlo?". Y son dos preguntas distintas.
#
# La diferencia entre un aviso conocido y un `dato_dudoso` es de quien es
# la pelota. Un aviso conocido es un juicio CERRADO -- "lo miramos y esta
# bien". Un `dato_dudoso` es un juicio ABIERTO con una accion externa
# pegada: llamar a AniForte, llamar a GRAU, partir la ficha del sesamo.
# Ninguna ejecucion de la bateria va a hacer que AniForte coja el
# telefono.
#
# ⚠️ Y POR QUE NO ES UN TEST QUE SE PONGA ROJO A LOS 30 DIAS, que fue lo
# primero que se penso: un rojo que salta por el calendario es un rojo que
# nadie ha provocado, y lo que se aprende de el es a silenciarlo -- subir
# la fecha sin mirar es el mismo gesto de no revisar, con un paso mas de
# burocracia. Es exactamente el fallo del BLOQUE 19 otra vez: el aviso de
# los cuatro aceites sono en CADA ejecucion durante un mes y nadie
# pregunto por que. Un aviso que suena solo no arregla nada.
# Asi que sin umbral, sin rojo y sin fecha que subir: solo la lista, con
# los dias al lado y ordenada de mas vieja a mas nueva, para que se vuelva
# incomoda de leer sola.
import datetime as _dt
_abiertas = []
for a in al:
    for k, d in (a.get("dato_dudoso") or {}).items():
        desde = d.get("desde")
        try:
            dias = (_dt.date.today() - _dt.date.fromisoformat(desde)).days
        except (TypeError, ValueError):
            dias = None
        _abiertas.append((dias if dias is not None else -1, a["nombre"], k, desde,
                          d.get("resolver", "(sin decir que la resolveria)")))
if _abiertas:
    _abiertas.sort(reverse=True)
    print()
    print("MARCAS DE DATO DUDOSO ABIERTAS — de la mas vieja a la mas nueva")
    print("(no son fallos: son datos que sabemos malos y que solo se cierran desde fuera)")
    for dias, nombre, k, desde, resolver in _abiertas:
        cuanto = f"{dias} dias" if dias >= 0 else "fecha sin poner"
        print()
        print(f"  [{cuanto:>14}]  {nombre} · {k}   (desde {desde})")
        for linea in _envolver(resolver, 74):
            print(f"                    {linea}")
    print()
    print(f"  {len(_abiertas)} marcas abiertas. Cada una necesita que alguien haga algo FUERA")
    print("  de este repositorio: una llamada, una ficha tecnica, una carga de datos.")


sys.exit(1 if any(t == "BASE" for t, _, _ in avisos) else 0)
