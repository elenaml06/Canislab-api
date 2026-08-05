# -*- coding: utf-8 -*-
"""
CANISLAB — MOTOR DE CONSTRUCCION DE RACIONES  (sustituye al LP)
================================================================

POR QUE NO UN LP
----------------
El motor anterior usaba programacion lineal: "minimiza un coste cumpliendo
estas restricciones". El problema es que NUESTRO PROBLEMA NO TIENE FUNCION
OBJETIVO. No hay ningun recurso escaso que repartir. Habia que inventarse un
"coste por categoria" (carne 1, higado 12) que no significa nada
nutricionalmente, y un LP siempre devuelve una solucion en un VERTICE: casi
todas las variables pegadas a algun limite. De ahi salian los menus con dos
alimentos exactamente iguales (454.8 g y 454.8 g), el higado siempre en su
minimo, y que cada restriccion nueva bajase la factibilidad (73% -> 68% ->
62%) porque las reglas peleaban entre si.

COMO FUNCIONA ESTE
------------------
No optimiza: CONSTRUYE y luego VERIFICA. Es lo que hace a mano un
nutricionista clinico.

    1. PLANTILLA    proporciones por categoria (deducidas, no heredadas)
    2. REPARTIR     entre los alimentos elegidos
    3. ESCALAR      hasta clavar el DER
    4. VERIFICAR    contra los requisitos FEDIAF
    5. SUPLEMENTAR  cerrar huecos con el tope del fabricante Y el de FEDIAF
    6. AJUSTAR      lo que siga corto, si se puede
    7. INFORMAR     decir la verdad de lo que queda

VENTAJAS MEDIDAS FRENTE AL LP
-----------------------------
  · SIEMPRE devuelve una racion. El LP fallaba en el 38-55% de los casos y
    el usuario se quedaba sin nada -- que tampoco cumple FEDIAF.
  · Cantidades naturales, no pegadas a los limites.
  · Las reglas dejan de contradecirse: casi no hay restricciones.
  · Es EXPLICABLE. A "por que 454.8 g?" la unica respuesta del LP era
    "porque el simplex acabo ahi". Aqui cada gramo tiene un porque.
  · El recalculo no puede desmontar la racion: la estructura esta fijada
    antes de empezar, asi que ninguna categoria puede desaparecer.

SOBRE LOS PORCENTAJES
---------------------
Los porcentajes clasicos del BARF (80/10/10, 70/10/10/10) son folclore de
divulgacion sin estudio detras, y asi hay que decirlo. Por eso aqui NO se
heredan: se DEDUCEN barriendo cada categoria y viendo que nutriente se rompe
primero, con nuestras propias tablas FEDIAF verificadas (ver deducir.py).
El BARF solo se usa como punto de partida de la busqueda.
Y lo que legitima la racion no es la plantilla, es la VERIFICACION: la
afirmacion no es "esto lleva 5% de higado", es "esto cubre 26 de 27
nutrientes FEDIAF, y estos dos se quedan cortos".
"""
import json, os

BASE = os.path.dirname(os.path.abspath(__file__))
# ⚠️ RUTA ROBUSTA (5 agosto). En el despliegue real, motor/ vive DENTRO de
# canislab-api/ (junto a alimentos_v3_final.json, en el padre directo).
# Antes esto apuntaba a "../backend", que solo era correcto en mi propia
# carpeta de pruebas (/home/claude/motor/ y /home/claude/backend/ como
# hermanas con nombres distintos) — en el repo real no hay ninguna carpeta
# llamada "backend", así que fallaba. Se prueban varias rutas candidatas,
# de la más probable a la menos, y se usa la primera que exista de verdad.
def _detectar_repo():
    candidatas = [
        os.path.join(BASE, ".."),              # motor/ dentro de canislab-api/ (el caso real)
        os.path.join(BASE, "..", "backend"),    # compatibilidad con la carpeta de pruebas
        BASE,                                    # todo en la misma carpeta
    ]
    for c in candidatas:
        if os.path.exists(os.path.join(c, "alimentos_v3_final.json")):
            return c
    return candidatas[0]   # si ninguna existe, la más probable, para que el error sea claro

REPO = _detectar_repo()


def cargar():
    with open(os.path.join(REPO, "alimentos_v3_final.json"), encoding="utf-8") as f:
        alimentos = {a["nombre"]: a for a in json.load(f)}
    with open(os.path.join(REPO, "requerimientos_v2_final.json"), encoding="utf-8") as f:
        req = {x["nutriente"]: x for x in json.load(f)}
    return alimentos, req


# Categorias que forman la racion BASE. Son COMIDA.
# Los 5 pilares BARF + pescado + extras.
#
# "Extras" son ALIMENTOS, no suplementos: aceites, huevos, yogur. Se compran
# en el supermercado y se pesan como cualquier otra cosa. Por eso van en la
# PLANTILLA, no en el paso de suplementacion.
# (Meterlos por error entre los suplementos hizo que el aceite de oliva se
# colara como "suplemento de linoleico" sin dosis de fabricante que lo
# frenara: 13.800 g en una racion.)
PILARES = ["Carne muscular", "Hueso carnoso", "Pescados y mariscos",
           "Vísceras", "Hígado", "Verduras y frutas", "Extras"]

# Los 5 pilares BARF de verdad: los que NUNCA pueden faltar ni desaparecer.
# Pescado y extras son deseables pero no imprescindibles.
PILARES_OBLIGATORIOS = ["Carne muscular", "Hueso carnoso", "Vísceras",
                        "Hígado", "Verduras y frutas"]

# SUPLEMENTOS: productos comerciales con dosis de etiqueta del fabricante.
# Solo estos entran en el paso 5. NO son comida.
CAT_SUPLEMENTO = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                  "Calcio", "Hierro", "Vitamina B")

# EXTRAS: aceites, semillas, huevos, yogur. NO son suplementos -- son comida,
# solo que muy densa. Van "fuera del 100%" de la estructura BARF.
#
# Se topan POR ENERGIA, no por peso. El tope clasico del BARF ("extras <= 5%
# del peso") no significa nada: 63 g de aceite (888 kcal/100g) son el 37% de
# las calorias del dia, y 63 g de huevo el 6%. El mismo 5% de peso, dos cosas
# distintas. Es el error de la verdura pero al reves: la verdura necesitaba
# tope POR PESO porque tiene pocas calorias; los extras lo necesitan POR
# ENERGIA porque tienen muchisimas.
# Lo que si esta fundamentado es limitarlos: diluyen la racion (un aceite no
# aporta ni proteina ni minerales) y cargan de grasa. El 12% es criterio de
# desarrollo, NO una cifra de ninguna guia.
CAT_EXTRA = ("Extras",)
TOPE_EXTRAS_KCAL = 0.12



# =============================================================================
# LA PLANTILLA BASE — estructura BARF clásica
# =============================================================================
#   50% hueso carnoso (pieza entera, como se pesa en la cocina)
#   30% carne y pescado (juntos: nutricionalmente son lo mismo)
#   10% verduras y frutas
#    5% vísceras
#    5% hígado
#   + extras (aceites, semillas, huevo) FUERA del 100%, topados por energía
#
# POR QUÉ ESTA Y NO OTRA
# ----------------------
# NO es ciencia: son convenciones de divulgación (Billinghurst 1993) sin
# estudio detrás, y así hay que decirlo. Pero se probaron cinco repartos
# distintos sobre 300 menús cada uno y el resultado fue que DA CASI IGUAL:
#     BARF 50/30/10/5/5      ratio Ca:P 1.55   5.5 problemas/menú
#     40 hueso / 40 carne    ratio Ca:P 1.54   5.0
#     30 hueso / 50 carne    ratio Ca:P 1.51   4.2
#     60 hueso / 20 carne    ratio Ca:P 1.57   5.7
# Ninguna estructura resuelve el problema ni lo empeora: los fallos están en
# los nutrientes concretos (zinc, magnesio), no en cómo se reparte.
#
# Así que se usa la del BARF por dos razones PRÁCTICAS:
#   1. el usuario la RECONOCE. Ver "50% hueso, 30% carne" le resulta
#      familiar; ver "37% hueso, 43% carne" le hace preguntarse de dónde sale
#   2. es la que usa la industria, así que comparar nuestros menús con los de
#      cualquier marca es directo
#
# Lo que legitima la ración NO es la plantilla: es la VERIFICACIÓN contra
# FEDIAF que viene después.
PLANTILLA_BARF = {
    "Hueso carnoso":       0.50,
    "Carne muscular":      0.30,   # carne Y/O pescado, el motor decide el reparto
    "Verduras y frutas":   0.10,
    "Vísceras":            0.05,
    "Hígado":              0.05,
}


# =============================================================================
# MÁRGENES DE LA PLANTILLA — dónde hay que ser estricto y dónde no
# =============================================================================
# La plantilla BARF es el PUNTO DE PARTIDA, no una camisa de fuerza. Si un
# menú cumple mejor los nutrientes con 60% de carne y 20% de hueso, que lo
# haga: lo que importa es que cumpla, no que respete un porcentaje que
# nadie ha demostrado.
#
# PERO hay dos categorías donde el tope SÍ tiene motivo de salud, medido con
# nuestros propios datos y los máximos de FEDIAF:
#
#   HÍGADO — lo limita el COBRE, no la vitamina A como se suele decir.
#     Hígado de vaca: 12 mg de cobre/100 g. Con el máximo FEDIAF de cobre
#     (9 mg/1000 kcal) solo caben 72 g en una ración de 1230 kcal = 7% del
#     plato. La vitamina A dejaría llegar a 360 g (36%), así que el cobre
#     manda mucho antes.
#
#   VÍSCERAS — lo limita el SELENIO. Riñón de ternera 118 µg/100 g; con el
#     máximo de 175 µg/1000 kcal caben 148 g = 15% del plato.
#     Así que el "5% de vísceras" del BARF es MÁS ESTRICTO de lo necesario:
#     se puede llegar al 12% sin problema.
#
# La carne, el pescado, el hueso y la verdura NO llevan tope de salud aquí:
# sus límites salen de los nutrientes (el ratio Ca:P frena el hueso, el
# exceso de verdura diluye). Se les deja margen amplio.
# ⚠️ EL PESCADO NO ES UNA CATEGORIA APARTE: es proteina, igual que la carne.
# Antes tenia su propio margen (0-25%) y su propio tramo en la plantilla, y
# el reparto carne/pescado se hacia a ciegas 2/3-1/3 en vez de dejar que el
# motor decidiera libremente cuanto de cada uno. "Carne muscular" en
# PILARES y MARGENES cubre AMBOS; Pescados y mariscos sigue siendo una
# CATEGORIA DE ALIMENTO (para elegir_alimentos, exclusiones, etc.), pero ya
# no tiene tramo propio en la plantilla ni margen propio.
MARGENES = {
    # categoria:            (mínimo, máximo)   — fracción del peso
    "Hueso carnoso":        (0.20, 0.60),   # el ratio Ca:P lo frena solo
    "Carne muscular":       (0.10, 0.60),   # incluye carne Y pescado
    # ⚠️ CORREGIDO 5 agosto: era 5-25%, y el programa lo usaba hasta el
    # borde (384 g de canónigos, el 25% del plato). La usuaria lo bajó a
    # un máximo del 10%, para que el resto del plato lo cubran carne,
    # hueso, víscera e hígado.
    "Verduras y frutas":    (0.02, 0.10),
    "Vísceras":             (0.02, 0.12),   # tope por SELENIO
    "Hígado":               (0.02, 0.06),   # tope por COBRE — el más estricto
}


def plantilla_valida(plantilla):
    """Comprueba que una plantilla respeta los márgenes de salud."""
    fallos = []
    for cat, pct in plantilla.items():
        mn, mx = MARGENES.get(cat, (0.0, 1.0))
        if pct < mn - 1e-9:
            fallos.append(f"{cat} al {pct*100:.0f}% (mínimo {mn*100:.0f}%)")
        if pct > mx + 1e-9:
            fallos.append(f"{cat} al {pct*100:.0f}% (máximo {mx*100:.0f}%)")
    total = sum(plantilla.values())
    if abs(total - 1.0) > 0.01:
        fallos.append(f"la plantilla suma {total*100:.0f}%, debería sumar 100%")
    return fallos


def variantes_plantilla(base=None, paso=0.10):
    """
    Genera variantes de la plantilla dentro de los márgenes, moviendo el
    reparto entre HUESO y CARNE (que son los que tienen margen amplio) y
    dejando fijos hígado y vísceras, que son los que llevan tope de salud.

    Sirve para que el motor pruebe varios repartos y se quede con el que
    mejor cumpla, en vez de estar atado a uno solo.
    """
    base = base or PLANTILLA_BARF
    fijas = {c: base[c] for c in ("Vísceras", "Hígado", "Verduras y frutas")
             if c in base}
    resto = 1.0 - sum(fijas.values())
    mn_h, mx_h = MARGENES["Hueso carnoso"]
    salida = []
    h = mn_h
    while h <= mx_h + 1e-9:
        if h > resto:
            break
        proteina = resto - h
        if proteina < MARGENES["Carne muscular"][0]:
            h += paso
            continue
        # el pescado ya no es tramo aparte: toda la proteina va a
        # "Carne muscular", que cubre carne Y pescado. El reparto entre
        # ambos lo decide `formular()`, no un 2/3-1/3 fijo.
        pl = dict(fijas)
        pl["Hueso carnoso"] = round(h, 3)
        pl["Carne muscular"] = round(proteina, 3)
        if not plantilla_valida(pl):
            salida.append(pl)
        h += paso
    return salida


def _fusionar_pescado_en_carne(elegidos):
    """
    El pescado comparte plaza de plantilla con la carne ("Carne muscular").
    `elegidos` puede traerlo bajo su propia clave (asi lo devuelve
    elegir_alimentos, por categoria de alimento); esta funcion lo fusiona
    para que `construir()` y `construir_con_pesos()` lo repartan junto con
    la carne en vez de perderlo en silencio.
    """
    salida = dict(elegidos)
    if "Pescados y mariscos" in salida:
        pesc = salida.pop("Pescados y mariscos")
        salida["Carne muscular"] = list(salida.get("Carne muscular", [])) + list(pesc)
    return salida


def construir(plantilla: dict, elegidos: dict, der: float, alimentos: dict) -> dict:
    """
    Pasos 1-3: reparte segun la plantilla y escala hasta clavar el DER.

    plantilla: {categoria: fraccion del peso}   ej. {"Carne muscular": 0.50, ...}
    elegidos:  {categoria: [nombres]}           lo que el usuario tiene o quiere
    Devuelve   {nombre: gramos}

    Si falta una categoria entera (p. ej. no tiene higado en casa), su parte
    NO se reparte entre las demas: se deja fuera y se avisa. Repartirla en
    silencio daria una racion que parece completa y no lo es.
    """
    elegidos_efectivo = _fusionar_pescado_en_carne(elegidos)

    crudo = {}
    for cat, pct in plantilla.items():
        lista = [n for n in elegidos_efectivo.get(cat, []) if n in alimentos]
        if not lista:
            continue
        for n in lista:
            crudo[n] = crudo.get(n, 0.0) + pct / len(lista)

    if not crudo:
        return {}

    # escalar para que las kcal cuadren exactamente con el DER
    kcal_por_unidad = sum(v * alimentos[n]["energia"] for n, v in crudo.items())
    if kcal_por_unidad <= 0:
        return {}
    factor = der / kcal_por_unidad * 100.0
    return {n: round(v * factor, 1) for n, v in crudo.items()}


def perfil_nutricional(menu: dict, alimentos: dict) -> dict:
    """Suma lo que aporta la racion. Simple aritmetica, sin sorpresas."""
    total = {}
    for nombre, gramos in menu.items():
        a = alimentos.get(nombre)
        if not a:
            continue
        for nutriente, valor in a.get("nutrientes", {}).items():
            try:
                total[nutriente] = total.get(nutriente, 0.0) + float(valor) * gramos / 100.0
            except (TypeError, ValueError):
                continue
    total["_kcal"] = sum(alimentos[n]["energia"] * g / 100.0
                         for n, g in menu.items() if n in alimentos)
    total["_gramos"] = sum(menu.values())
    return total


def ajustar_hueso_al_ratio(plantilla, elegidos, der, alimentos, req, etapa,
                           objetivo=1.4, min_pct=0.03, max_pct=0.45):
    """
    Calcula CUANTO HUESO hace falta para clavar el ratio Ca:P, en vez de
    usar un porcentaje fijo.

    POR QUE
    -------
    El ratio calcio:fosforo es de lo mas importante de la racion, y un
    porcentaje fijo de hueso NO lo garantiza: depende de QUE hueso sea. Con
    costillas de cordero (1690 mg Ca/100g) un 15% da un ratio de 0.80 --
    INVERTIDO. Con huesos de cuello de ternera (7310 mg) ese mismo 15% se
    pasaria por arriba.
    Un ratio invertido es el que causa el hiperparatiroidismo nutricional
    secundario: el cuerpo saca calcio del hueso para compensar. Es
    exactamente lo que les pasa a los perros alimentados solo con carne.

    COMO
    ----
    Busqueda binaria sobre el % de hueso hasta clavar el objetivo. El resto
    de categorias se reescalan proporcionalmente para que sigan sumando 1.
    Objetivo 1.4 por defecto: centro comodo del rango adulto (1-2) y dentro
    tambien del de cachorro (1-1.6 y 1-1.8), asi que vale para todas las
    etapas sin tener que decidir nada.

    Esto ELIMINA un numero arbitrario en vez de anadir una regla: el % de
    hueso deja de ser folclore y pasa a ser el que hace falta.
    """
    if "Hueso carnoso" not in plantilla or not elegidos.get("Hueso carnoso"):
        return plantilla, None

    otras = {c: p for c, p in plantilla.items() if c != "Hueso carnoso"}
    suma_otras = sum(otras.values()) or 1.0

    def ratio_con(pct_hueso):
        pl = {"Hueso carnoso": pct_hueso}
        for c, p in otras.items():
            pl[c] = p / suma_otras * (1 - pct_hueso)
        menu = construir(pl, elegidos, der, alimentos)
        perfil = perfil_nutricional(menu, alimentos)
        ca, p_ = perfil.get("calcio", 0.0), perfil.get("fosforo", 0.0)
        return (ca / p_ if p_ > 0 else 0.0), pl

    lo, hi = min_pct, max_pct
    r_lo, _ = ratio_con(lo)
    r_hi, pl_hi = ratio_con(hi)
    if r_hi < objetivo:          # ni con el maximo de hueso se llega
        return pl_hi, (f"Ni con un {max_pct*100:.0f}% de hueso se alcanza el ratio "
                       f"calcio:fósforo (se queda en {r_hi:.2f}:1). Hace falta un hueso "
                       f"más rico en calcio o un suplemento de calcio.")
    if r_lo > objetivo:          # ya se pasa con el minimo
        _, pl_lo = ratio_con(lo)
        return pl_lo, None

    for _ in range(30):
        medio = (lo + hi) / 2
        r, pl = ratio_con(medio)
        if abs(r - objetivo) < 0.01:
            return pl, None
        if r < objetivo:
            lo = medio
        else:
            hi = medio
    _, pl = ratio_con((lo + hi) / 2)
    return pl, None


def repartir_por_necesidad(plantilla, elegidos, der, alimentos, req, etapa,
                           pasos=5, fijos=None):
    """
    Reparte la parte de cada categoría entre sus alimentos SEGÚN LO QUE HAGA
    FALTA, en vez de a partes iguales.

    EL FALLO QUE ARREGLA
    --------------------
    `construir()` repartía la proporción de cada categoría a partes iguales:
    3 carnes = 33% cada una, salieran los números como salieran. Se veía en
    los menús (214 g / 214 g / 214 g, 53 / 53 / 53) y la usuaria lo detectó:
    "me resulta raro que los gramos salgan idénticos".
    No estaba calculado: estaba repartido a ciegas. Que en su menú saliera
    bien fue suerte, no criterio.

    CÓMO FUNCIONA
    -------------
    Para cada categoría con más de un alimento, prueba varios repartos y se
    queda con el que deja MÁS MARGEN en el nutriente que va más justo.
    Ese es el criterio correcto: no "cuántos nutrientes cubro" sino "cuánto
    colchón le queda al peor", porque el peor es el que rompe la ración.

    Las proporciones ENTRE categorías no se tocan: eso lo decide la plantilla.
    """
    from verificar import MAPA, _num, EQUIVALENCIA
    # fusionar pescado en carne AQUI, para que los "pesos" y la busqueda
    # trabajen sobre la lista ya unida (carnes y pescados compitiendo por
    # el mismo tramo), no sobre dos categorias separadas que luego
    # construir_con_pesos fusionaria por su cuenta perdiendo el reparto.
    elegidos = _fusionar_pescado_en_carne(elegidos)
    et = EQUIVALENCIA.get(etapa, etapa)
    objetivos = {}
    topes = {}
    for nombre, clave in MAPA.items():
        r = req.get(nombre)
        if not r:
            continue
        mn = _num(r.get(f"min{et}"))
        if mn is not None:
            objetivos[clave] = mn * der / 1000.0
        mx = _num(r.get(f"max{et}")) or _num(r.get("maxAdulto"))
        if mx is not None:
            topes[clave] = mx * der / 1000.0

    def margen(pesos):
        """
        Cuánto le sobra al nutriente que va más justo (1.0 = justo).

        ⚠️ SE EVALÚA EL MENÚ COMPLETO, CON LOS SUPLEMENTOS PUESTOS.
        Al principio se medía solo la comida base y salía fatal: el reparto
        se iba a 90% pollo / 10% pavo para exprimir un nutriente, y luego los
        suplementos no podían arreglar los nueve que se rompían por el camino.
        Optimizar media ración no sirve de nada.
        """
        menu = construir_con_pesos(plantilla, elegidos, der, alimentos, pesos)
        if not menu:
            return -1
        if fijos:
            menu = dict(menu)
            kf = sum(alimentos[n]["energia"] * g / 100.0
                     for n, g in fijos.items() if n in alimentos)
            kc = sum(alimentos[n]["energia"] * g / 100.0 for n, g in menu.items())
            if kc > 0 and der > kf:
                f = (der - kf) / kc
                menu = {n: round(g * f, 1) for n, g in menu.items()}
            menu.update(fijos)
        perfil = perfil_nutricional(menu, alimentos)
        peor = 99.0
        for cl, obj in objetivos.items():
            if obj > 0:
                peor = min(peor, perfil.get(cl, 0.0) / obj)
        # penalizar pasarse de un máximo: no sirve subir un nutriente si
        # eso rompe otro por arriba
        for cl, mx in (topes or {}).items():
            if mx and perfil.get(cl, 0.0) > mx:
                peor = min(peor, mx / perfil[cl])
        return peor

    # arrancar en reparto igual y mejorar categoría a categoría
    pesos = {cat: [1.0 / len(l)] * len(l) for cat, l in elegidos.items() if l}
    mejor = margen(pesos)

    for cat, lista in elegidos.items():
        if len(lista) < 2:
            continue
        for _ in range(pasos):
            mejoro = False
            for i in range(len(lista)):
                for delta in (0.10, -0.10, 0.05, -0.05):
                    prueba = {c: list(v) for c, v in pesos.items()}
                    nuevo = prueba[cat][i] + delta
                    if nuevo < 0.05 or nuevo > 0.95:
                        continue
                    prueba[cat][i] = nuevo
                    total = sum(prueba[cat])
                    prueba[cat] = [x / total for x in prueba[cat]]
                    m = margen(prueba)
                    if m > mejor + 1e-6:
                        pesos, mejor, mejoro = prueba, m, True
            if not mejoro:
                break
    return construir_con_pesos(plantilla, elegidos, der, alimentos, pesos), pesos, mejor


def construir_con_pesos(plantilla, elegidos, der, alimentos, pesos):
    """Como construir(), pero con el reparto interno de cada categoría dado."""
    elegidos = _fusionar_pescado_en_carne(elegidos)
    crudo = {}
    for cat, pct in plantilla.items():
        lista = [n for n in elegidos.get(cat, []) if n in alimentos]
        if not lista:
            continue
        w = pesos.get(cat) or [1.0 / len(lista)] * len(lista)
        if len(w) != len(lista):
            w = [1.0 / len(lista)] * len(lista)
        for n, f in zip(lista, w):
            crudo[n] = crudo.get(n, 0.0) + pct * f
    if not crudo:
        return {}
    kcal_u = sum(v * alimentos[n]["energia"] for n, v in crudo.items())
    if kcal_u <= 0:
        return {}
    factor = der / kcal_u * 100.0
    return {n: round(v * factor, 1) for n, v in crudo.items()}


def redondear_a_pesable(menu, alimentos, der, req=None, etapa="Adulto",
                        dosis_maxima_fn=None, peso_perro_kg=None):
    """
    Convierte los gramos a cantidades que alguien pueda pesar de verdad,
    Y VERIFICA CON ESAS, no con los decimales originales.

    EL FALLO QUE ARREGLA
    --------------------
    El motor daba "41.8 g de hígado" y la persona pesa 42. Daba "519.5 g de
    ternera" y se pesan 520. Verificar contra 41.8 cuando lo que va a comer
    el perro son 42 es verificar otra cosa.

    LA REGLA
    --------
      · más de 100 g → al múltiplo de 5 (nadie afina más en una báscula)
      · 10 a 100 g   → al gramo
      · 1 a 10 g     → a 0.5 g
      · menos de 1 g → a 0.05 g, y avisar de que se prepare por lotes

    ⚠️ SE REDONDEA A LA BAJA en lo que tiene MÁXIMO de seguridad (hígado,
    suplementos) y AL ALZA en el resto. Redondear al alza un suplemento
    puede pasarse de la dosis del fabricante; redondear a la baja la carne
    solo quita unas kcal.
    """
    import math
    CON_MAXIMO = ("Hígado", "Multivitamínico", "Omega-3", "Yodo", "Calcio",
                  "Hierro", "Vitamina B", "Vísceras")

    def paso_de(g):
        if g >= 100: return 5.0
        if g >= 10:  return 1.0
        if g >= 1:   return 0.5
        return 0.05

    # LOS SUPLEMENTOS COMERCIALES NO SE REDONDEAN COMO LA COMIDA.
    # Se pesan por SEMANA (0,16 g al día no los coge ninguna báscula) y se
    # redondean AL ALZA al 0,1 g de la semana, topando en la dosis máxima del
    # fabricante. Redondearlos a la baja como el resto tiraba el yodo al 98%.
    COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Calcio", "Hierro",
                   "Vitamina B", "Fibra")

    salida, avisos = {}, []
    for nombre, g in menu.items():
        cat = alimentos.get(nombre, {}).get("categoria", "")

        if cat in COMERCIALES:
            semana = math.ceil(g * 7 * 10) / 10
            if dosis_maxima_fn and peso_perro_kg:
                mx = dosis_maxima_fn(alimentos.get(nombre, {}), peso_perro_kg)
                if mx and semana / 7 > mx:
                    semana = math.floor(mx * 7 * 10) / 10
            salida[nombre] = round(semana / 7, 4)
            avisos.append("%s: pesa %.1f g para toda la semana y reparte en 7."
                          % (nombre, semana))
            continue

        p = paso_de(g)
        if cat in CON_MAXIMO:
            nuevo = math.floor(g / p) * p
            if nuevo <= 0:
                nuevo = round(g, 2)
        else:
            nuevo = math.ceil(g / p) * p
        salida[nombre] = round(nuevo, 2)
        if salida[nombre] < 1:
            avisos.append(
                "%s son %.2f g al día: pesa la cantidad de varios días junta "
                "y reparte, porque una báscula de cocina no baja de ahí."
                % (nombre, salida[nombre]))

    # el redondeo mueve las kcal: decir cuánto
    kcal = sum(alimentos[n]["energia"] * g / 100.0 for n, g in salida.items()
               if n in alimentos)
    desvio = (kcal - der) / der * 100 if der else 0
    if abs(desvio) > 2:
        avisos.append("Al redondear, las calorías quedan un %.1f%% %s del objetivo."
                      % (abs(desvio), "por encima" if desvio > 0 else "por debajo"))
    return salida, avisos, kcal
