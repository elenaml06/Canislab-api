# -*- coding: utf-8 -*-
"""
QUE LA TRANSCRIPCION DE LA TABLA III-3b SE REHAGA, EN VEZ DE CREERSE.

⚠️ POR QUE EXISTE (10 de septiembre de 2026).

`auditar_fediaf.py` comprueba las 43 filas de `requerimientos_v2_final.json`
contra una transcripcion de la Tabla III-3b que vive DENTRO de el, escrita a
mano. O sea que la cadena era:

    PDF de FEDIAF  --(a mano, una vez)-->  auditar_fediaf.FEDIAF
                   --(BLOQUE 18)-->        requerimientos_v2_final.json

El segundo tramo estaba vigilado desde el 25 de agosto y el primero NO. Y ese
primer tramo es el que decide todo: si un valor de la transcripcion esta mal,
`auditar_fediaf` dice que el JSON cuadra, la bateria sale verde, y TODOS los
menus cumplen bien un requisito equivocado. Nada del motor puede cazarlo,
porque el motor no tiene el PDF.

Ya paso una vez, y no con un digito: la transcripcion se habia saltado LOS DOCE
AMINOACIDOS ENTEROS, que estaban en la tabla desde siempre entre "Protein" y
"Fat". El motor decia cubrir "todo FEDIAF" con 29 de los 41 nutrientes que la
tabla pide. Lo encontro contar las filas a mano el 26 de agosto, no una prueba.

Lo que faltaba era exactamente lo mismo que `leer_fuente.py` hace con las
secciones de texto y `auditar_conversiones.py` con las cifras de patologia:
volver a la fuente y REHACER, en vez de confiar en que alguien lo copio bien.
`fediaf_tabla_III_3b.txt` es la tabla tal cual sale del PDF -- ni una palabra
tocada -- y este script la lee, saca sus 44 filas y las compara celda a celda
contra la transcripcion.

Y exige que NINGUNA fila se quede fuera: una fila de la tabla que no este
transcrita tiene que estar declarada aqui abajo con su motivo. Sin eso, saltarse
otros doce aminoacidos volveria a ser invisible.

    python3 auditar_transcripcion_fediaf.py
"""
import os
import re
import sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
RUTA_TABLA = os.path.join(_AQUI, "fediaf_tabla_III_3b.txt")

# Como se llama cada fila EN EL PDF y como se llama en la transcripcion.
# El nombre del PDF va sin el asterisco ni los parentesis de unidad quimica:
# se normaliza abajo, para que un cambio de maquetacion no rompa esto.
FILAS = {
    "Protein": "Protein",
    "Arginine": "Arginine",
    "Histidine": "Histidine",
    "Isoleucine": "Isoleucine",
    "Leucine": "Leucine",
    "Lysine": "Lysine",
    "Methionine": "Methionine",
    "Methionine + cystine": "Methionine_cystine",
    "Phenylalanine": "Phenylalanine",
    "Phenylalanine + tyrosine": "Phenylalanine_tyr",
    "Threonine": "Threonine",
    "Tryptophan": "Tryptophan",
    "Valine": "Valine",
    "Fat": "Fat",
    "Linoleic acid": "Linoleic",
    "Arachidonic acid": "Arachidonic",
    "Alpha-linolenic acid": "ALA",
    "EPA + DHA": "EPA_DHA",
    "Calcium": "Calcium",
    "Phosphorus": "Phosphorus",
    "Potassium": "Potassium",
    "Sodium": "Sodium",
    "Chloride": "Chloride",
    "Magnesium": "Magnesium",
    "Copper": "Copper",
    "Iodine": "Iodine",
    "Iron": "Iron",
    "Manganese": "Manganese",
    "Selenium (wet diets)": "Selenium_wet",
    "Zinc": "Zinc",
    "Vitamin A": "VitaminA",
    "Vitamin D": "VitaminD",
    "Vitamin E": "VitaminE",
    "Vitamin B1 (Thiamine)": "B1_Thiamine",
    "Vitamin B2 (Riboflavin)": "B2_Riboflavin",
    "Vitamin B5 (Pantothenic acid)": "B5_Pantothenic",
    "Vitamin B6 (Pyridoxine)": "B6_Pyridoxine",
    "Vitamin B12 (Cyanocobalamin)": "B12",
    "Vitamin B3 (Niacin)": "B3_Niacin",
    "Vitamin B9 (Folic acid)": "B9_Folic",
    "Choline": "Choline",
}

# Las filas de la tabla que NO estan en la transcripcion, cada una con su
# motivo. Esta lista es la parte que de verdad importa: mientras haya que
# escribir aqui el motivo, saltarse una fila deja de poder pasar en silencio.
NO_TRANSCRITAS = {
    "Selenium (dry diets)": (
        "La tabla da DOS filas de selenio, humeda y seca, y Rawku formula racion "
        "CRUDA -- o sea humeda. Se transcribe la humeda (67,50 / 57,50) porque es "
        "la del perro al que se le da de comer aqui. La seca (55,00 / 45,00) es "
        "MAS BAJA en adulto, asi que usar la humeda es ademas el lado exigente."),
    "Vitamin B7 (Biotin)": (
        "FEDIAF no da cifra: las cuatro columnas son «-». No hay nada que "
        "transcribir, y por eso tampoco esta en `requerimientos_v2_final.json`."),
    "Vitamin K": (
        "Igual que la biotina: las cuatro columnas son «-». FEDIAF la nombra en "
        "su seccion 3.3 (mas K en dietas con mucho pescado) y NO la cuantifica "
        "para el perro; eso vive en `requisitos_condicionales.json` como "
        "`documentado_sin_cifra`."),
    "Ca / P ratio": (
        "No es un nutriente con cuatro columnas: es un ratio con un unico minimo "
        "(1/1) y cuatro maximos por etapa. Vive en `requerimientos_v2_final.json` "
        "como la fila `Relacion_Ca_P` y lo comprueban el BLOQUE 53 (las dos "
        "mitades de la nota b) y el propio semaforo."),
}

# Las cuatro columnas de minimos, en el orden en que salen del PDF.
COLUMNAS = ("Adulto MER 95", "Adulto MER 110", "Early Growth", "Late Growth")


def _normaliza_nombre(txt):
    """El nombre de la fila sin el asterisco de FEDIAF ni el (ω-n) de la grasa."""
    txt = txt.replace("*", "").strip()
    txt = re.sub(r"\s*\(ω-\d\)\s*", "", txt)
    return re.sub(r"\s+", " ", txt).strip()


def _numeros(resto):
    """Los valores de la fila, en orden. «-» es None.

    ⚠️ El PDF escribe los miles con un espacio fino («1 754», «100 000»), asi
    que hay que pegarlos ANTES de partir por espacios o saldrian 1 y 754 como
    dos numeros distintos -- y la vitamina A pasaria a valer 1.
    """
    resto = re.sub(r"(?<=\d) (?=\d{3}(?:\D|$))", "", resto)
    fuera = []
    for token in resto.split():
        if token == "-":
            fuera.append(None)
        elif re.fullmatch(r"\d+(?:[.,]\d+)?[a-h]?", token):
            # El sufijo a/b del calcio en Late Growth es una nota al pie, no
            # parte del numero (2.00a = 2,00 con la nota a).
            fuera.append(float(re.sub(r"[a-h]$", "", token).replace(",", ".")))
        else:
            break          # a partir de aqui empieza la columna de maximos
    return fuera


def leer_tabla(ruta=RUTA_TABLA):
    """{nombre del PDF: (unidad, [valores])} leyendo el texto tal cual."""
    filas = {}
    lineas = open(ruta, encoding="utf-8").read().split("\n")
    for i, linea in enumerate(lineas):
        m = re.match(r"\s{6,}([A-Za-z][^|]*?)\s{2,}(g|mg|µg|IU)\s+(.*)$", linea)
        if not m:
            continue
        nombre = _normaliza_nombre(m.group(1))
        valores = _numeros(m.group(3))
        # ⚠️ EL CALCIO ES LA UNICA FILA PARTIDA EN TRES LINEAS, y no por
        # capricho del PDF: su celda de Late Growth tiene DOS valores, 2.00a
        # (raza pequena) y 2.50b (raza grande, nota b), uno encima y otro
        # debajo del resto de la fila. El motor aplica el 2,00 generico y el
        # 2,50 reforzado va aparte, en `Calcio_LateGrowth_RazaGrande`.
        if nombre == "Calcium" and len(valores) == 3:
            arriba = _numeros(lineas[i - 1]) if i else []
            if arriba:
                valores = valores + [arriba[0]]
        filas[nombre] = (m.group(2), valores)
    return filas


def _transcripcion():
    """La tabla transcrita a mano que hay dentro de `auditar_fediaf.py`.

    Se lee con `ast` y NO se importa el modulo, por dos motivos: ese modulo
    ejecuta su propio informe al importarse (y un script que imprime el informe
    de otro por el medio no se lee), y sobre todo REVIENTA si le falta una
    fila -- que es justo uno de los fallos que esto tiene que poder CONTAR en
    vez de morirse. Leyendo el literal, una fila borrada sale como lo que es:
    una fila de la tabla que ya no esta transcrita.
    """
    import ast
    arbol = ast.parse(open(os.path.join(_AQUI, "auditar_fediaf.py"),
                           encoding="utf-8").read())
    for nodo in arbol.body:
        if (isinstance(nodo, ast.Assign) and len(nodo.targets) == 1
                and getattr(nodo.targets[0], "id", None) == "FEDIAF"):
            return ast.literal_eval(nodo.value)
    raise SystemExit("auditar_fediaf.py ya no tiene un diccionario FEDIAF en el nivel "
                     "de arriba: sin el no hay transcripcion que comprobar")


def auditar():
    TRANSCRITA = _transcripcion()

    problemas = []
    tabla = leer_tabla()
    if len(tabla) < 40:
        problemas.append(
            f"solo se han leido {len(tabla)} filas de `fediaf_tabla_III_3b.txt`, y la "
            f"tabla tiene 44. O el fichero esta recortado o el patron ha dejado de "
            f"encajar: un barrido cuyo resultado no se compara contra el total no es "
            f"un barrido, es una muestra")
        return problemas, 0

    comprobadas = 0
    for nombre_pdf, (unidad_pdf, valores) in sorted(tabla.items()):
        clave = FILAS.get(nombre_pdf)
        if clave is None:
            if nombre_pdf in NO_TRANSCRITAS:
                continue
            problemas.append(
                f"«{nombre_pdf}» es una fila de la Tabla III-3b que NO esta en la "
                f"transcripcion de `auditar_fediaf.py` ni declarada en "
                f"NO_TRANSCRITAS con su motivo. Es exactamente asi como se colaron "
                f"los doce aminoacidos: la fila existe en el PDF, el motor no la "
                f"mira, y nada avisa")
            continue
        if clave not in TRANSCRITA:
            problemas.append(f"«{nombre_pdf}» esta mapeada a «{clave}» y esa clave no existe "
                             f"en `auditar_fediaf.FEDIAF`")
            continue
        *dichos, unidad_dicha = TRANSCRITA[clave]
        if unidad_dicha != unidad_pdf:
            problemas.append(f"{nombre_pdf}: el PDF dice «{unidad_pdf}» y la transcripcion "
                             f"«{unidad_dicha}». Una unidad mal es todos los menus mal, y el "
                             f"semaforo sale verde igual")
        if len(valores) < 4:
            problemas.append(f"{nombre_pdf}: del PDF solo se han sacado {len(valores)} valores "
                             f"({valores}) y la fila tiene cuatro columnas de minimo")
            continue
        for col, (dicho, leido) in enumerate(zip(dichos, valores[:4])):
            comprobadas += 1
            if dicho is None and leido is None:
                continue
            if dicho is None or leido is None or abs(float(dicho) - float(leido)) > 1e-9:
                problemas.append(
                    f"{nombre_pdf} / {COLUMNAS[col]}: el PDF dice {leido} y "
                    f"`auditar_fediaf.py` tiene transcrito {dicho}. La transcripcion es lo "
                    f"unico contra lo que se compara el JSON, asi que un error aqui hace que "
                    f"la bateria confirme un requisito equivocado")

    # Y al reves: una clave transcrita que ya no exista en la tabla.
    en_tabla = {FILAS[n] for n in tabla if n in FILAS}
    for clave in sorted(set(TRANSCRITA) - en_tabla):
        problemas.append(f"«{clave}» esta en la transcripcion y no se ha encontrado su fila en "
                         f"la tabla del PDF. O la fila cambio de nombre o la transcripcion "
                         f"lleva un requisito que FEDIAF ya no pide")
    return problemas, comprobadas


# ============================================================
# LA TABLA III-3a, QUE ES DONDE VIVEN LOS MAXIMOS
# ============================================================
#
# ⚠️ POR QUE (10 de septiembre). Todo lo de arriba comprueba las CUATRO COLUMNAS
# DE MINIMO de la Tabla III-3b. La columna de MAXIMO no la miraba nadie, y hay
# dos motivos por los que eso era un agujero de verdad:
#
# 1. En la III-3b los maximos LEGALES no llevan numero: solo pone «(L)». Es a
#    proposito y la propia §3.2.1 lo dice -- «Legal maxima in EU legislation are
#    expressed on 12 % moisture content and they do not account for energy
#    density. Therefore in these guidelines they are only provided on a dry
#    matter basis». O sea que los siete techos legales que aplica el motor
#    (cobre 7, yodo 2750, hierro 170,45, manganeso 42,5, selenio 142, zinc 56,75
#    y vitamina D 14,1875 por 1000 kcal) son conversiones NUESTRAS de la III-3a,
#    y no habia nada que las comparara con el PDF.
#
# 2. Un maximo mal transcrito es la peor clase de error de este fichero. Un
#    minimo bajo deja al perro corto y suele verse; un maximo alto deja pasar un
#    menu que envenena despacio, y el semaforo sale VERDE.
#
# ⚠️ Y NO ES HIPOTETICO. El 7 de septiembre se QUITO el maximo de fosforo del
# adulto escribiendo que «FEDIAF no da numero», y la nota del sello lo explica:
# «se colo porque en el texto extraido del PDF la columna de maximos cae
# visualmente sobre la fila ANTERIOR: leyendo linea a linea, el calcio parece
# tener cuatro maximos y el fosforo ninguno». Durante un dia el motor NO TUVO
# techo de fosforo en adulto y el catalogo llego a tener un menu con 4124 mg,
# por encima del maximo de FEDIAF. Era ya el fallo de las dos columnas pegadas,
# visto en una celda y sin encontrarle la causa.
#
# COMO SE REHACE. De `fediaf_tabla_III_3a.txt` (la pagina 15 del PDF tal cual)
# se saca, para cada fila, el numero que va justo antes de «(L)» o «(N)» con su
# etiqueta de etapa, y se convierte a la unidad del motor con el x2,5 de la
# Tabla III-2 -- y con el 0,3 y el 0,025 µg/IU de la Tabla VII-14 para las
# vitaminas A y D. Despues se compara contra `requerimientos_v2_final.json`.
import json as _json_3a

RUTA_3A = os.path.join(_AQUI, "fediaf_tabla_III_3a.txt")

# (fila del PDF, etapa que dice el PDF) -> (clave del JSON, columna, factor)
#
# El factor es el x2,5 de «unidades/100 g MS -> unidades/1000 kcal» (Tabla
# III-2), multiplicado por la conversion de unidad donde la hay: la vitamina A
# va en IU y el motor en µg de retinol (0,3 µg = 1 IU), y la D en IU y el motor
# en µg de colecalciferol (0,025 µg = 1 IU). El ratio Ca:P es adimensional.
MAXIMOS_3A = {
 # (fila del PDF, etapa) -> (clave del JSON, columna, factor, etiqueta que espera)
 #
 # ⚠️ EL FACTOR NO ES SIEMPRE 2,5, Y AQUI ES DONDE SE FALLA. El x2,5 es solo el
 # cambio de base («unidades/100 g MS -> unidades/1000 kcal», Tabla III-2). Si
 # ademas cambia la UNIDAD hay que multiplicar por eso: el calcio y el fosforo
 # van en g en la tabla y en mg en el motor (x2.500), el yodo en mg y en µg
 # (x2.500), la vitamina A en IU y en µg de retinol (0,3 µg = 1 IU) y la D en IU
 # y en µg de colecalciferol (0,025 µg = 1 IU). El selenio ya va en µg en las
 # dos (x2,5) y el ratio Ca:P es adimensional (x1).
 ("Lysine",            "Growth"):                 ("Lisina", "maxCachorroJoven", 2.5, "N"),
 ("Linoleic acid",     "Growth"):                 ("Linoleico", "maxCachorroJoven", 2.5, "N"),
 ("Calcium",           "Adult"):                  ("Calcio", "maxAdulto", 2500.0, "N"),
 ("Calcium",           "Early growth"):           ("Calcio", "maxCachorroJoven", 2500.0, "N"),
 ("Calcium",           "Late growth"):            ("Calcio", "maxCachorroCrecimiento", 2500.0, "N"),
 ("Phosphorus",        "Adult"):                  ("Fósforo", "maxAdulto", 2500.0, "N"),
 ("Ca / P ratio",      "Adult"):                  ("Relacion_Ca_P", "maxAdulto", 1.0, "N"),
 ("Ca / P ratio",      "Early growth & reprod."): ("Relacion_Ca_P", "maxCachorroJoven", 1.0, "N"),
 ("Ca / P ratio",      "Late growth"):            ("Relacion_Ca_P", "maxCachorroCrecimiento", 1.0, "N"),
 ("Copper",            None):                     ("Cobre", "maxAdulto", 2.5, "L"),
 ("Iodine",            None):                     ("Yodo", "maxAdulto", 2500.0, "L"),
 ("Iron",              None):                     ("Hierro", "maxAdulto", 2.5, "L"),
 ("Manganese",         None):                     ("Manganeso", "maxAdulto", 2.5, "L"),
 ("Zinc",              None):                     ("Zinc", "maxAdulto", 2.5, "L"),
 ("Selenium* (dry diets)", None):                 ("Selenio", "maxAdulto", 2.5, "L"),
 ("Vitamin A",         None):                     ("Vitamina_A", "maxAdulto", 2.5 * 0.3, "N"),
 ("Vitamin D",         None):                     ("Vitamina_D", "maxAdulto", 2.5 * 0.025, "L"),
}
# El (N) de la vitamina D, que el motor NO aplica pero deja anotado.
NUTRICIONAL_3A = {("Vitamin D", None): ("Vitamina_D", "maximo_nutricional_por_1000kcal",
                                        2.5 * 0.025, "N")}

_FILAS_3A = [
 "Protein", "Arginine", "Histidine", "Isoleucine", "Leucine", "Lysine", "Methionine",
 "Methionine + cystine", "Phenylalanine", "Phenylalanine + tyrosine", "Threonine",
 "Tryptophan", "Valine", "Fat", "Linoleic acid", "Arachidonic acid",
 "Alpha-linolenic acid", "EPA + DHA", "Calcium", "Phosphorus", "Ca / P ratio",
 "Potassium", "Sodium", "Chloride", "Magnesium", "Copper", "Iodine", "Iron",
 "Manganese", "Selenium* (wet diets)", "Selenium* (dry diets)", "Zinc",
 "Vitamin A", "Vitamin D", "Vitamin E", "Vitamin B1", "Vitamin B2", "Vitamin B5",
 "Vitamin B6", "Vitamin B12", "Vitamin B3", "Vitamin B9", "Vitamin B7", "Choline",
 "Vitamin K",
]
_MAX_3A = re.compile(r"(?:(Adult|Early growth(?: & reprod\.)?|Late growth|Growth)\s*:\s*)?"
                     r"((?:\d{1,3}(?: \d{3})+|\d+(?:\.\d+)?)(?:/1[ab]?)?)\s*\((L|N)\)")


def leer_maximos_3a():
    """{(fila, etapa): (valor, etiqueta)} de la columna MAXIMO de la III-3a."""
    if not os.path.exists(RUTA_3A):
        return None
    plano = " ".join(open(RUTA_3A, encoding="utf-8").read().split())
    pos = sorted((plano.find(f), f) for f in _FILAS_3A if plano.find(f) >= 0)
    salida = {}
    for k, (i, fila) in enumerate(pos):
        j = pos[k + 1][0] if k + 1 < len(pos) else len(plano)
        for m in _MAX_3A.finditer(plano[i:j]):
            etapa, valor, tag = m.group(1), m.group(2), m.group(3)
            v = valor.replace(" ", "")
            if "/1" in v:                      # el ratio: «2/1», «1.8/1a»
                v = v.split("/")[0]
            salida.setdefault((fila, etapa), []).append((float(v), tag))
    return salida


def auditar_maximos():
    tabla = leer_maximos_3a()
    if tabla is None:
        print("  (no esta fediaf_tabla_III_3a.txt: no se puede rehacer la columna de maximos)")
        return [], 0
    req = {r["nutriente"]: r for r in
           _json_3a.load(open(os.path.join(_AQUI, "requerimientos_v2_final.json"),
                              encoding="utf-8"))}
    problemas, hechas = [], 0

    def _mira(mapa):
        nonlocal hechas
        for (fila, etapa), (clave, columna, factor, etiqueta) in mapa.items():
            hits = tabla.get((fila, etapa.strip() if etapa else None))
            if not hits:
                problemas.append(
                    f"III-3a: no se encuentra el maximo de «{fila}»"
                    f"{' / ' + etapa if etapa else ''} en el PDF, y el JSON tiene un numero "
                    f"en {clave}.{columna}. O la tabla ha cambiado o el patron ha dejado de "
                    f"encajar -- y un maximo que deja de vigilarse no avisa a nadie")
                continue
            elegidos = [v for v, tag in hits if tag == etiqueta]
            if not elegidos:
                problemas.append(
                    f"III-3a: «{fila}»{' / ' + etapa if etapa else ''} tiene maximo en el PDF "
                    f"pero ninguno etiquetado ({etiqueta}), que es lo que el JSON dice que "
                    f"aplica en {clave}.{columna}")
                continue
            esperado = elegidos[0] * factor
            dicho = req.get(clave, {}).get(columna)
            try:
                dicho = float(dicho)
            except (TypeError, ValueError):
                problemas.append(
                    f"III-3a: el PDF da un maximo de {elegidos[0]} ({etiqueta}) para "
                    f"«{fila}»{' / ' + etapa if etapa else ''} y el JSON tiene "
                    f"{clave}.{columna} = {dicho!r}. Un maximo que existe en la fuente y no "
                    f"en el motor es un menu que envenena despacio y sale VERDE")
                continue
            if abs(dicho - esperado) > max(1e-4 * esperado, 1e-9):
                problemas.append(
                    f"III-3a: «{fila}»{' / ' + etapa if etapa else ''} vale {elegidos[0]} "
                    f"({etiqueta}) en el PDF, que por {factor:g} son {esperado:.4f}, y "
                    f"el JSON tiene {clave}.{columna} = {dicho}")
            hechas += 1

    _mira(MAXIMOS_3A)
    _mira(NUTRICIONAL_3A)

    # Y que la etiqueta escrita en el JSON sea la que pone el PDF.
    for (fila, etapa), (clave, columna, _f, _tag) in MAXIMOS_3A.items():
        hits = tabla.get((fila, etapa.strip() if etapa else None)) or []
        if not hits:
            continue
        tags = {tag for _v, tag in hits}
        dicho = req.get(clave, {}).get("maximo_origen")
        if dicho is None:
            problemas.append(
                f"III-3a: «{fila}» tiene maximo en el PDF y la fila {clave} del JSON no dice "
                f"si es LEGAL o NUTRICIONAL (`maximo_origen`). No es lo mismo: el legal solo "
                f"aplica si el nutriente se anade como ADITIVO (§3.1.3), y si viene solo del "
                f"alimento manda el nutricional")
            continue
        esperado = "legal_UE" if "L" in tags else "nutricional"
        if dicho != esperado:
            problemas.append(
                f"III-3a: «{fila}» lleva ({'/'.join(sorted(tags))}) en el PDF y el JSON dice "
                f"`maximo_origen: {dicho}`")
    return problemas, hechas


# ============================================================
# LA TABLA VII-14, LA DE LAS FORMAS QUIMICAS
# ============================================================
#
# ⚠️ POR QUE (10 de septiembre). `fediaf_conversiones_vitaminas.json` es la
# Tabla VII-14 transcrita a mano, y estaba en el mismo sitio que la III-3b: nadie
# la comparaba con el PDF. Sus numeros son factores de conversion, y un factor
# equivocado no se ve -- convertir la vitamina D con el factor de la A (0,3 en
# vez de 0,025) multiplica por DOCE el aporte de un multivitaminico y el semaforo
# sale verde igual. Es el motivo por el que existe el fichero, asi que el fichero
# tampoco puede creerse.
RUTA_VII_14 = os.path.join(_AQUI, "fediaf_tabla_VII_14.txt")

# (donde vive en el JSON · como se llama la fuente en el PDF · que lado de la
# igualdad es · valor esperado). El «lado» importa: la tabla escribe unas filas
# como «0.3 µg = 1 IU» (el numero esta a la izquierda) y otras como «1 mg =
# 1.49 IU» (a la derecha), y confundirlos es invertir el factor.
FILAS_VII_14 = [
    (("ui_a_microgramos", "vitA", "retinol"),               r"vitamin A alcohol \(retinol\).*IU", "izq", 0.3),
    (("ui_a_microgramos", "vitA", "acetato_de_retinilo"),   r"vitamin A acetate",             "izq", 0.344),
    (("ui_a_microgramos", "vitA", "propionato_de_retinilo"), r"vitamin A propionate",         "izq", 0.359),
    (("ui_a_microgramos", "vitA", "palmitato_de_retinilo"), r"vitamin A palmitate",           "izq", 0.55),
    (("ui_a_microgramos", "vitA", "betacaroteno_UI_por_mg_perro"), r"β-carotene", "der", 833.0),
    (("ui_a_microgramos", "vitD", "colecalciferol_D3"),     r"vitamins D3",                   "izq", 0.025),
    (("actividad_por_mg_de_fuente", "vitE", "d_alfa_tocoferol"),         r"d-α-tocopherol\s+1 mg", "der", 1.49),
    (("actividad_por_mg_de_fuente", "vitE", "d_alfa_tocoferol_acetato"), r"d-α-tocopherol acetate", "der", 1.36),
    (("actividad_por_mg_de_fuente", "vitE", "dl_alfa_tocoferol"),        r"dl-α-tocopherol\s+1", "der", 1.10),
    (("actividad_por_mg_de_fuente", "vitE", "dl_alfa_tocoferil_acetato"), r"dl-α-tocopheryl acetate\s+1", "der", 1.00),
    (("actividad_por_mg_de_fuente", "vitE", "dl_beta_tocoferol"),        r"dl-β-tocopherol", "der", 0.33),
    (("actividad_por_mg_de_fuente", "vitE", "dl_delta_tocoferol"),       r"dl-δ-tocopherol", "der", 0.25),
    (("actividad_por_mg_de_fuente", "vitE", "dl_gamma_tocoferol"),       r"dl-γ-tocopherol", "der", 0.01),
    (("actividad_por_mg_de_fuente", "tiamina", "tiamina_CL"),            r"thiamine CL", "der", 0.88),
    (("actividad_por_mg_de_fuente", "tiamina", "mononitrato_de_tiamina"), r"thiamine mononitrate", "der", 0.81),
    (("actividad_por_mg_de_fuente", "tiamina", "clorhidrato_de_tiamina"), r"thiamine hydrochloride", "der", 0.79),
    (("actividad_por_mg_de_fuente", "acidoPantotenico", "D_pantotenato_calcico"), r"calcium D-pantothenate", "der", 0.92),
    (("actividad_por_mg_de_fuente", "acidoPantotenico", "DL_pantotenato_calcico_min"), r"calcium DL-pantothenate", "der", 0.41),
    (("actividad_por_mg_de_fuente", "acidoPantotenico", "DL_pantotenato_calcico_max"), r"calcium DL-pantothenate", "der2", 0.52),
    (("actividad_por_mg_de_fuente", "vitB6", "clorhidrato_de_piridoxina"), r"pyridoxine hydrochloride", "der", 0.82),
    (("actividad_por_mg_de_fuente", "niacina", "acido_nicotinico"),      r"nicotinic acid", "der", 1.0),
    (("actividad_por_mg_de_fuente", "niacina", "nicotinamida"),          r"^\s*nicotinamide\b", "der", 1.0),
    (("actividad_por_mg_de_fuente", "colina", "cloruro_de_colina_base_ion_colina"), r"basis choline ion", "der", 0.75),
    (("actividad_por_mg_de_fuente", "colina", "cloruro_de_colina_base_analogo_hidroxilo"), r"basis choline hydroxyl-analogue", "der", 0.87),
    (("actividad_por_mg_de_fuente", "vitK3", "menadiona_bisulfito_sodico_MSB"), r"\(MSB\)", "der", 0.51),
    (("actividad_por_mg_de_fuente", "vitK3", "menadiona_bisulfito_de_pirimidinol_MPB"), r"\(MPB\)", "der", 0.45),
    (("actividad_por_mg_de_fuente", "vitK3", "menadiona_bisulfito_de_nicotinamida_MNB"), r"\(MNB\)", "der", 0.46),
]

# Las tres equivalencias de la tabla que NO son un numero suelto del JSON: viven
# dentro de una `nota`, que es prosa. Se declaran para que no puedan
# desaparecer sin que nadie lo note.
EN_UNA_NOTA_VII_14 = {
    "1.0 mg de retinol = 3,333 IU": "ui_a_microgramos.vitA.nota",
    "1.0 µg de retinol = 1 RE": "ui_a_microgramos.vitA.nota",
    "1 µg de D3 = 40 IU": "ui_a_microgramos.vitD.nota",
}


def _lado(linea, cual):
    """Los numeros de una fila «X unidad = Y unidad», por lado.

    ⚠️ SOLO LOS QUE LLEVAN UNIDAD PEGADA. Sin eso, la fila «vitamins D3  0.025 µg
    = 1 IU» devolvia un 3 -- el de «D3» -- y el auditor acusaba en falso a la
    conversion de la vitamina D, que es justo la que este fichero existe para
    proteger.
    """
    if "=" not in linea:
        return []
    izq, der = linea.split("=", 1)
    trozo = izq if cual == "izq" else der
    # El «-\s*\d» del final es por la unica fila con RANGO de toda la tabla:
    # «calcium DL-pantothenate 1 mg = 0.41 - 0.52 mg». Sin el, el 0,41 -- que es
    # el factor mas agresivo que publica FEDIAF -- se perdia porque no lleva
    # unidad pegada detras.
    return [float(x.replace(",", ""))
            for x in re.findall(r"(\d[\d,]*(?:\.\d+)?)\s*(?:(?:µg|mg|IU|RE)\b|(?=-\s*\d))",
                                trozo)]


def auditar_vii_14():
    import json
    problemas, comprobadas = [], 0
    lineas = open(RUTA_VII_14, encoding="utf-8").read().split("\n")
    tabla = json.load(open(os.path.join(_AQUI, "fediaf_conversiones_vitaminas.json"),
                           encoding="utf-8"))
    filas_usadas = set()
    for ruta, patron, cual, esperado in FILAS_VII_14:
        candidatas = [i for i, l in enumerate(lineas)
                      if "=" in l and re.search(patron, l)]
        if not candidatas:
            # la fila puede llevar el nombre en la linea de arriba o de abajo
            candidatas = [i for i, l in enumerate(lineas) if "=" in l and (
                (i and re.search(patron, lineas[i - 1]))
                or (i + 1 < len(lineas) and re.search(patron, lineas[i + 1])))]
        if len(candidatas) != 1:
            problemas.append(
                f"VII-14 {'.'.join(ruta)}: el patron «{patron}» encaja con {len(candidatas)} "
                f"filas del PDF y tiene que encajar con UNA. O la tabla cambio de maquetacion o "
                f"el patron ha dejado de identificar su fila -- y un ancla que ya no vigila nada "
                f"no avisa a nadie")
            continue
        i = candidatas[0]
        filas_usadas.add(i)
        nums = _lado(lineas[i], "izq" if cual == "izq" else "der")
        leido = None
        if cual == "der2":
            leido = nums[1] if len(nums) > 1 else None
        elif nums:
            leido = nums[0]
        dicho = tabla
        for paso in ruta:
            dicho = (dicho or {}).get(paso) if isinstance(dicho, dict) else None
        if dicho is None:
            problemas.append(f"VII-14: `fediaf_conversiones_vitaminas.json` ya no tiene "
                             f"{'.'.join(ruta)}, y esa fila SI esta en la tabla del PDF")
            continue
        comprobadas += 1
        if leido is None or abs(float(dicho) - leido) > 1e-9:
            problemas.append(
                f"VII-14 {'.'.join(ruta)}: el PDF dice {leido} y el JSON tiene {dicho}. Un factor "
                f"de conversion equivocado no se ve: convertir la vitamina D con el factor de la "
                f"A multiplica por doce el aporte y el menu sale verde igual")

    # Y ninguna fila del PDF se queda sin reclamar.
    _sin_reclamar = [l.strip() for i, l in enumerate(lineas)
                     if "=" in l and i not in filas_usadas and re.search(r"\d", l)]
    # Las tres que viven dentro de una `nota` se descuentan aqui, por su cifra.
    # ⚠️ Y LA FILA DEL PATRON DE LA VITAMINA E, que la tabla escribe DOS VECES:
    # una arriba como «unidad declarada» (dl-α-tocopheryl acetate 1 mg = 1 IU)
    # y otra dentro de la lista de bioequivalencias. Es el mismo hecho, y el
    # JSON lo guarda una sola vez, en `dl_alfa_tocoferil_acetato`.
    _de_nota = ("3,333", "1 RE", "40 IU")
    _sin_reclamar = [l for l in _sin_reclamar if not any(m in l for m in _de_nota)]
    _sin_reclamar = [l for l in _sin_reclamar
                     if not re.fullmatch(r"1 mg\s+=\s+1 IU", l.strip())]
    for _fila in _sin_reclamar:
        problemas.append(
            f"VII-14: la fila «{_fila[:80]}» del PDF no la reclama ninguna cifra del JSON ni "
            f"esta declarada como parte de una nota. Es asi como se pierde un factor entero")
    return problemas, comprobadas


if __name__ == "__main__":
    fallos, n = auditar()
    fallos_v, n_v = auditar_vii_14()
    fallos_m, n_m = auditar_maximos()
    print(f"Tabla III-3b: {n} celdas rehechas desde el texto del PDF, "
          f"{len(NO_TRANSCRITAS)} filas declaradas sin transcribir")
    print(f"Tabla III-3a: {n_m} MAXIMOS rehechos desde el texto del PDF, con su "
          f"etiqueta (L) legal o (N) nutricional")
    print(f"Tabla VII-14: {n_v} factores rehechos desde el texto del PDF, "
          f"{len(EN_UNA_NOTA_VII_14)} equivalencias que viven dentro de una nota")
    print("-" * 60)
    fallos = fallos + fallos_v + fallos_m
    if fallos:
        print(f"\n{len(fallos)} PROBLEMAS:\n")
        for f in fallos:
            print("  -", f)
        sys.exit(1)
    print("\nLas tres transcripciones cuadran con el PDF, celda a celda.")
