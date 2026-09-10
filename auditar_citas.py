# -*- coding: utf-8 -*-
"""
CANISLAB — QUE CADA CITA ENTRECOMILLADA DIGA LO QUE DICE LA FUENTE

⚠️ POR QUÉ EXISTE (10 de septiembre de 2026). El texto de FEDIAF y el de SACN5
se habían extraído de sus PDF **conservando la disposición visual**, y los dos
libros van a dos columnas: cada línea pegaba la de la izquierda con la de la
derecha. El **49,3 %** de las líneas de FEDIAF y el **37,5 %** de las de SACN5.

O sea que durante días se pudo citar entrecomillado, de buena fe, una frase que
**la fuente no dice** — dos medias frases de dos párrafos distintos pegadas.

La extracción ya está rehecha (`canislab-fuentes/sacn5/extraer_texto.py`, y el
BLOQUE 81 vigila que no vuelva a pasar). Pero **las citas escritas antes siguen
ahí**, y son las que justifican cada cifra que aplica el motor: los campos
`fuente` y `por_que` de `patologias.json` son 398 citas.

Elena: «no me vale que haya cosas que descartes porque sí, porque ya has tenido
muchos errores».

QUÉ HACE. Saca toda cita entre «» de más de 40 caracteres, y la busca LITERAL
—normalizando espacios y guiones de corte de línea— en los textos de las fuentes
que hay en el repo. Cada cita acaba en uno de tres sitios:

  · encontrada           la fuente la dice, palabra por palabra
  · sin texto que mirar   su fuente no está en el repo (Merck, ACVIM, IRIS en
                          PDF, Purina...). No se puede comprobar, y se DICE
  · NO ENCONTRADA        su fuente sí está en el repo y la frase no aparece.
                          Es la que hay que mirar con ojos

⚠️ «No encontrada» no significa «falsa»: puede ser una cita con puntos
suspensivos, con una palabra cambiada de sitio o traducida. Significa **que nadie
puede darla por buena sin abrir la fuente**, que es exactamente lo que hay que
evitar.

CÓMO SE USA

    python3 auditar_citas.py            # el recuento y las que no cuadran
    python3 auditar_citas.py --todas    # además, la lista entera
"""
import glob
import json
import os
import re
import sys
import unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))
FUENTES = os.path.join(RAIZ, "..", "canislab-fuentes")

# Los ficheros del repo que citan una fuente entre comillas angulares.
# ⚠️ `PARA_EL_NUTRICIONISTA.md` NO está: se reescribe entero al final, y sus
# citas se comprobarán al reescribirlo (decisión de Elena, 10 de septiembre).
DOCUMENTOS = ["PATOLOGIAS.md", "LECTURA_SACN5.md", "HALLAZGOS_LECTURA_FUENTES.md",
              "HALLAZGOS_SACN5_10SEP.md"]
JSONS = ["patologias.json", "recomendaciones_libro.json", "requisitos_condicionales.json",
         "requerimientos_v2_final.json", "sacn5_fuentes_de_minerales.json",
         "fediaf_conversiones_vitaminas.json"]

_CITA = re.compile(r"«([^»]{40,})»")
_LARGO_MINIMO = 40

# Cuantas citas quedan por comprobar contra una fuente que SI esta en el repo.
# Se pone a mano y se compara exacto. Ver el comentario del final de `auditar`.
PENDIENTES_DECLARADAS = 31        # 10 de septiembre de 2026, tarde

# ⚠️ SOLO SE AUDITAN LAS CITAS EN INGLES, Y ESTE FILTRO SI ES LEGITIMO: las
# fuentes estan todas en ingles, asi que una cita entre comillas angulares en
# ESPAÑOL no es una cita de fuente -- es prosa nuestra entrecomillada para
# destacarla, o una frase de Elena. Buscarla en el texto de FEDIAF no tiene
# sentido y solo llenaria el informe de ruido.
#
# El filtro se aplica al REVES de como se hace normalmente: no se pregunta si
# parece inglesa, se pregunta si lleva palabras que en ingles NO existen. Asi
# una cita mal clasificada se queda DENTRO de la auditoria, que es el lado
# seguro -- el error caro es dejar fuera una cita de fuente, no meter una de
# mas.
_ES_ESPANOL = re.compile(r"\b(?:que|para|con|del|los|las|una|por|como|sin|"
                         r"esta|este|pero|cuando|donde|porque|segun|mas|ya|"
                         r"asi|solo|hay|ser|tiene|puede|debe|hace)\b", re.I)
_ES_INGLES = re.compile(r"\b(?:the|of|and|is|are|be|should|shall|in|for|with|"
                        r"that|this|which|from|may|must|not|per|dogs?|cats?)\b", re.I)


def _parece_de_fuente(c):
    """Una cita en ingles. Las que estan en español son prosa nuestra."""
    n_es = len(_ES_ESPANOL.findall(c))
    n_en = len(_ES_INGLES.findall(c))
    return n_en > n_es


def _norm(t):
    """Espacios, comillas y guiones de corte de linea, todos iguales."""
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("’", "'").replace("‘", "'")
    t = t.replace("“", '"').replace("”", '"')
    # ⚠️ TODOS LOS GUIONES DE UNICODE, que son ocho y se parecen. El que se
    # colo fue el SIGNO MENOS (U+2212), que en «kg⁻¹» sale al convertir el
    # superindice y NO es el guion ASCII: la cita quedaba «kg−1» y la fuente
    # «kg-1», identicas a la vista y distintas para una comparacion.
    for _g in "–—‐‑‒−﹘﹣－":
        t = t.replace(_g, "-")
    # ⚠️ EL GUION DE CORTE DE LINEA, que es la trampa de los PDF: «substan-
    # tiation» en el texto es «substantiation» en la cita. Se quita el guion
    # seguido de espacio, no cualquier guion -- «low-taurine» tiene que seguir
    # siendo «low-taurine».
    t = re.sub(r"-\s+", "", t)
    # ⚠️ Y LAS MARCAS DE MARKDOWN, que no son de la fuente sino nuestras: los
    # asteriscos de negrita y el «>» de cita. Sin quitarlos, 18 citas de FEDIAF
    # salian «no encontradas» y las 18 estaban bien -- el fallo era del auditor.
    t = t.replace("**", "").replace("*", "")
    t = re.sub(r"^\s*>\s*", " ", t, flags=re.M)
    t = t.replace(" > ", " ")
    # ⚠️ Y LAS DIFERENCIAS DE TECLADO, que tampoco son de la fuente. Cada una
    # de estas salio de mirar por que una cita que SI estaba salia como «no
    # encontrada»; el fallo era del auditor las cinco veces:
    #   · «≤» escrito como «<=» al copiar a un JSON
    #   · «—» de la fuente escrito como «--»
    #   · «0,3 % DM» y «0.3% DM», que es el mismo numero con otro espacio
    #   · los corchetes de aclaracion nuestra dentro de la cita
    t = t.replace("≤", "<=").replace("≥", ">=")
    t = re.sub(r"-{2,}", "-", t)
    t = re.sub(r"\s+%", "%", t)
    t = re.sub(r"\[[^\]]{0,60}\]", " ", t)
    # ⚠️ EL SEPARADOR DE LOS NUMEROS, que es nuestro y no de la fuente. Al
    # transcribir a español se escribe «4,91 % DM» donde el original pone
    # «4.91% DM» -- y al reves, el ingles escribe «1,000 kcal» donde nosotros
    # pondriamos «1.000». El numero es el mismo y la cita deja de ser literal
    # por una costumbre de teclado.
    #
    # Se quita el separador ENTERO, en los dos lados: «4.91», «4,91», «1,000» y
    # «1.000» pasan a ser «491» y «1000». Cambiarlo por punto NO valia -- lo
    # probé y subio de 74 a 90, porque convertia el separador de MILES ingles
    # en un decimal y rompia citas que estaban bien.
    #
    # Lo que NO se iguala nunca es que falte una palabra: eso es contenido, y
    # es justo lo que hay que cazar.
    t = re.sub(r"(?<=\d)[.,](?=\d)", "", t)
    # ⚠️ Y LOS EXPONENTES DEL NRC, que se escriben de dos maneras: el PDF pone
    # «cystine·kg-1» y al citar se copia «cystine·kg⁻¹» con los caracteres
    # superindice de Unicode. Es el mismo texto con otro teclado.
    for a, b in (("⁻", "-"), ("¹", "1"), ("²", "2"), ("³", "3"), ("⁰", "0"),
                 ("·", " "), ("•", " ")):
        t = t.replace(a, b)
    return " ".join(t.split()).lower()


def _sin_guiones(t):
    """La misma frase con TODOS los guiones fuera.

    ⚠️ HACE FALTA PORQUE EL GUION DEL PDF ES AMBIGUO. En el texto extraido hay
    dos clases y no se distinguen: el de cortar palabra al final de linea
    («substan- tiation» = «substantiation») y el que es parte de la palabra
    («n- 6:n-3» = «n-6:n-3»). Quitando el espacio se arregla uno y se rompe el
    otro; quitando el guion entero se arreglan los dos, a costa de que «low-fat»
    y «lowfat» pasen a ser lo mismo -- que para comprobar una cita da igual.
    """
    return re.sub(r"[-\s–—‐‑‒−]", "", t)


def textos():
    """Todo el texto de fuente que hay en el repo de al lado, ya normalizado."""
    fuera = {}
    for ruta in sorted(glob.glob(os.path.join(FUENTES, "**", "*.txt"), recursive=True)):
        if os.path.getsize(ruta) < 1024:
            continue
        nombre = os.path.relpath(ruta, FUENTES)
        fuera[nombre] = _norm(open(ruta, encoding="utf-8", errors="ignore").read())
    return fuera


# Las fuentes cuyo TEXTO esta en el repo de al lado. Si una cita dice venir de
# una de estas y no aparece, es que hay que mirarla. Si dice venir de otra
# (Merck, el consenso ACVIM, Today's Veterinary Practice, Purina), no se puede
# comprobar aqui -- y eso se DICE, no se da por bueno.
_EN_EL_REPO = ("fediaf", "sacn5", "small animal clinical nutrition", "nrc",
               "fascetti", "köber", "kober", "reglamento", "iris", "aaha", "tvt")
_FUERA = ("acvim", "merck", "purina", "today's veterinary", "cavanaugh", "center",
          "consenso")


def _quien_dice(contexto):
    c = contexto.lower()
    for k in _FUERA:
        if k in c:
            return ("fuera", k)
    for k in _EN_EL_REPO:
        if k in c:
            return ("dentro", k)
    return ("sin decir", "?")


def _citas_de(texto):
    return [m.group(1) for m in _CITA.finditer(texto)]


def recoger():
    """Cada cita con el fichero del repo donde vive."""
    fuera = []
    for f in DOCUMENTOS:
        p = os.path.join(RAIZ, f)
        if not os.path.exists(p):
            continue
        t = open(p, encoding="utf-8").read()
        for m in _CITA.finditer(t):
            c = m.group(1)
            if _parece_de_fuente(c):
                # el contexto es la MISMA linea o vinyeta, no un parrafo entero:
                # con 400 caracteres hacia atras se pegaba la fuente de la cita
                # de al lado, y una cita de Today's Veterinary Practice salia
                # clasificada como de SACN5.
                ini = t.rfind("\n", 0, m.start())
                fuera.append((f, c, t[ini + 1:m.end() + 200]))
    for f in JSONS:
        p = os.path.join(RAIZ, f)
        if not os.path.exists(p):
            continue
        _d = json.load(open(p, encoding="utf-8"))

        def _anda(o, ctx=""):
            if isinstance(o, dict):
                nc = " ".join(str(o.get(k, "")) for k in ("fuente", "fuente_cifra", "cita")) or ctx
                for v in o.values():
                    _anda(v, nc)
            elif isinstance(o, list):
                for v in o:
                    _anda(v, ctx)
            elif isinstance(o, str):
                for c in _CITA.findall(o):
                    if _parece_de_fuente(c):
                        fuera.append((f, c, ctx or o))
        _anda(_d)
    return fuera


def auditar(mostrar_todas=False):
    fallos = []
    tx = textos()
    if not tx:
        print("  ⚠️ NO ESTA el repo de fuentes al lado, asi que este control NO SE HA HECHO. "
              "Clona `canislab-fuentes` junto a este repo para que mire de verdad.")
        return fallos
    # El texto sin guiones se calcula UNA vez por fichero, no una por cita:
    # con 781 citas y 98 ficheros, hacerlo dentro del bucle tardaba minuto y
    # medio y asi tarda segundos.
    tx_sg = {n: _sin_guiones(t) for n, t in tx.items()}
    citas = recoger()
    encontradas, no_encontradas = [], []
    for fichero, cita, ctx in citas:
        n = _norm(cita)
        # Una cita con puntos suspensivos son DOS trozos: se comprueban los dos.
        # ⚠️ EL UMBRAL DE LOS TROZOS ERA DEMASIADO ALTO Y TIRABA CITAS BUENAS.
        # Con 25 caracteres, «L-carnitine … should contain ≥300 ppm» perdia sus
        # DOS trozos («l-carnitine» tiene 11 y «should contain >=300 ppm» tiene
        # 24) y se comparaba la cita entera contra un texto donde la fuente pone
        # otras siete palabras en medio. Salia «no encontrada» estando en cap27
        # palabra por palabra. Con 12 se comprueban los dos trozos por separado,
        # que es lo que significa una cita con puntos suspensivos.
        trozos = [x for x in re.split(r"\s*(?:\.\.\.|…|\[\.\.\.\])\s*", n) if len(x) >= 12]
        if not trozos:
            trozos = [n]
        # ⚠️ EL PUNTO FINAL DE LA CITA, que casi nunca esta en la fuente. Citar
        # media frase y cerrarla con punto es lo normal: «...sources of phytic
        # acid.» donde la fuente sigue «...phytic acid (e.g. cereals and
        # legumes)». Se quita SOLO del final de la cita, nunca del texto -- que
        # es la diferencia con la regla que probe antes, que quitaba puntuacion
        # en los dos lados y rompio quince citas que estaban bien.
        trozos = [re.sub(r"[.,;:]+$", "", x) for x in trozos]
        donde = None
        for nombre, t in tx.items():
            if all(x in t for x in trozos):
                donde = nombre
                break
        if donde is None:
            trozos_sg = [_sin_guiones(x) for x in trozos]
            for nombre, t in tx_sg.items():
                if all(x in t for x in trozos_sg):
                    donde = nombre
                    break
        # ⚠️ SE PROBO UN TERCER INTENTO QUITANDO DEL TEXTO LOS NUMEROS SUELTOS
        # -- el PDF del NRC mete el numero de pagina en medio de la frase
        # («severely limiting 293 in methionine») -- y SE HA QUITADO. No cazaba
        # ni una cita mas, y en cambio abria la puerta a un FALSO POSITIVO:
        # `\s\d{2,4}\s` se come tambien numeros de verdad («10 or 20 g» pasa a
        # « or g»), asi que una cita a la que le faltara una cifra podria salir
        # «encontrada». Vale mas dejar esas cuatro citas en la lista de mirar
        # que arriesgarse a dar por buena una cifra que no esta.
        if donde:
            encontradas.append((fichero, cita, donde))
        else:
            no_encontradas.append((fichero, cita, _quien_dice(ctx)))

    print(f"  {len(citas)} citas de mas de {_LARGO_MINIMO} caracteres en {len(DOCUMENTOS)} "
          f"documentos y {len(JSONS)} ficheros de datos")
    print(f"  {len(encontradas)} encontradas literales en el texto de su fuente")
    print(f"  {len(no_encontradas)} sin encontrar en ninguno de los {len(tx)} textos que hay")

    dentro = [x for x in no_encontradas if x[2][0] == "dentro"]
    fuera_ = [x for x in no_encontradas if x[2][0] == "fuera"]
    sin = [x for x in no_encontradas if x[2][0] == "sin decir"]
    print(f"     de esas, {len(fuera_)} citan una fuente que NO esta en el repo "
          f"(no se pueden comprobar aqui) y {len(sin)} no dicen de donde salen")
    print(f"  ⚠️ {len(dentro)} citan una fuente que SI esta y no aparecen: hay que mirarlas")

    if mostrar_todas:
        for f, c, d in encontradas:
            print(f"    ok  {f}: {c[:70]}...  [{d}]")
    for f, c, (_, quien) in dentro:
        print(f"    ??  [{quien}] {f}: {' '.join(c.split())[:110]}")
    # ⚠️ Y LAS CITAS ENTERAS A UN FICHERO, no cortadas. Cortar la cita para
    # imprimirla y luego triarla desde ahi es medir otra cosa: lo hice, y un
    # trozo de 110 caracteres «coincidia al 100 %» mientras la cita entera no
    # aparecia. El informe corta; el fichero no.
    if os.environ.get("CITAS_A"):
        json.dump([{"fichero": f, "quien": q, "cita": c}
                   for f, c, (_, q) in dentro],
                  open(os.environ["CITAS_A"], "w", encoding="utf-8"),
                  ensure_ascii=False, indent=1)

    # ⚠️ EL NUMERO VA CLAVADO, como los demas recuentos del repo: solo baja
    # cuando alguien abre la fuente y arregla la cita, y lo baja en el mismo
    # commit. Si sube, es que se ha escrito una cita nueva sin comprobarla.
    if PENDIENTES_DECLARADAS is not None and len(dentro) != PENDIENTES_DECLARADAS:
        fallos.append(
            f"quedan {len(dentro)} citas sin encontrar en su fuente y el fichero declara "
            f"{PENDIENTES_DECLARADAS}. Si ha subido, hay una cita nueva sin comprobar; si ha "
            f"bajado, se cambia este numero en el mismo commit")
    return fallos


if __name__ == "__main__":
    fs = auditar("--todas" in sys.argv)
    print("\nDiscrepancias:", len(fs))
    sys.exit(1 if fs else 0)
