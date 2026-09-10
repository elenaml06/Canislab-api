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


if __name__ == "__main__":
    fallos, n = auditar()
    print(f"Tabla III-3b: {n} celdas rehechas desde el texto del PDF, "
          f"{len(NO_TRANSCRITAS)} filas declaradas sin transcribir")
    print("-" * 60)
    if fallos:
        print(f"\n{len(fallos)} PROBLEMAS:\n")
        for f in fallos:
            print("  -", f)
        sys.exit(1)
    print("\nLa transcripcion cuadra con el PDF, celda a celda.")
