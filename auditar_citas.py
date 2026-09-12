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
import html
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
              "HALLAZGOS_SACN5_10SEP.md",
              # ⚠️ ENTRA EL 10 DE SEPTIEMBRE POR LA NOCHE, en el mismo commit que
              # nace. Es el registro de la relectura integra de SACN5 y va lleno de
              # citas literales, que es exactamente el material que este auditor
              # existe para vigilar. Dejarlo fuera seria abrir una puerta nueva por
              # la que puede colarse una cita que el libro no dice.
              "LECTURA_SACN5_INTEGRA.md",
              # NRC 2006, desde el 11 de septiembre. Su texto vive en
              # `canislab-fuentes/NRC2006/nrc2006.txt` y este auditor ya lo indexa,
              # porque recorre TODOS los .txt del repo de fuentes.
              "LECTURA_NRC2006.md",
    # El registro de donde las fuentes no dicen lo mismo, para el documento
    # que lee el nutricionista (11 septiembre). Va aqui por lo mismo que los
    # demas: es el sitio del repo donde mas facil es citar de memoria.
    "FEDIAF_CONTRA_OTRAS_FUENTES.md",
    # Los 19 hallazgos de las 286 tablas que faltaban (11 septiembre). Entra en
    # el mismo commit que nace, por lo mismo que su hermano del dia 10: son
    # citas literales de SACN5 y este es el sitio donde una mal copiada pasa
    # desapercibida.
    "HALLAZGOS_SACN5_11SEP.md",
    # El registro de la lectura de Fascetti (11 septiembre), en el mismo commit
    # en que nace. Va lleno de citas literales, que es el material que este
    # auditor existe para vigilar.
    "LECTURA_FASCETTI.md",
    # ⚠️ Y SUS HALLAZGOS, que se quedaron fuera al nacer (11 septiembre, tarde).
    # `LECTURA_FASCETTI.md` entro aqui el mismo dia y su hermano no, y es el que
    # mas citas literales lleva: las cifras que el motor NO aplica viven ahi con
    # la frase de la fuente al lado, que es justo donde una cita mal copiada
    # aguanta mas tiempo sin que nadie la abra. Al meterlo salieron 0 nuevas sin
    # encontrar, o sea que las que habia estaban bien -- pero eso no se sabia.
    "HALLAZGOS_FASCETTI.md",
    # ⚠️ EL REGISTRO DE LECTURAS, QUE ESTABA FUERA (12 de septiembre). `LECTURAS.md`
    # nacio el 11 sustituyendo a los cuatro scripts de contar lecturas, y es hoy el
    # sitio del repo donde MAS citas literales se escriben -- el metodo es leer y
    # anotar la frase de la fuente al lado. Se quedo sin auditar por haber nacido
    # despues de esta lista, que es exactamente como se cuela una cita que la
    # fuente no dice.
    "LECTURAS.md",
    # ⚠️ Y EL REGISTRO DE PREGUNTAS (12 de septiembre). Cada pregunta se sostiene
    # sobre la frase de la fuente que la abre -- P-19 entera es una cita del
    # consenso ACVIM --, y son las citas que mas lejos llegan: este fichero lo lee
    # quien va a contestar. Estaba fuera por lo mismo que `LECTURAS.md`: nacio
    # despues de la lista.
    "PREGUNTAS_ABIERTAS.md"]
JSONS = ["patologias.json", "recomendaciones_libro.json", "requisitos_condicionales.json",
         "requerimientos_v2_final.json", "sacn5_fuentes_de_minerales.json",
         "fediaf_conversiones_vitaminas.json"]

_CITA = re.compile(r"«([^»]{40,})»")
# ⚠️ BAJADO DE 40 A 25 EL 11 DE SEPTIEMBRE, y por un fallo mio concreto.
#
# El 10 de septiembre escribi en CUATRO documentos que la Tabla 13-1 de NRC 2006
# publica «Meal, with bone, rendered» con 3,61 kcal/g para el perro, y lo use
# para DESMENTIR una afirmacion anterior. Es falso: el cuerpo de esa tabla no
# esta en el .txt de NRC -- el capitulo 13 son 177 lineas con solo titulos y
# notas al pie, y donde iria la tabla hay dos numeros de pagina, «667 668» --, y
# las cadenas «Meal, with bone», «with bone, rendered» y «5-00-388» no aparecen
# en las 43.556 lineas.
#
# Este auditor no lo vio porque la cita tiene **26 caracteres** y el umbral eran
# 40. Una cifra atribuida a una tabla, con su numero de tabla y su codigo de
# ingrediente, y nada mirandola. Lo cazó el contador de NRC al montarlo, que es
# otra forma de decir que lo cazo la suerte.
#
# Medido antes de bajarlo: con 30, 25 y 20 no aparece ni una cita nueva sin
# encontrar. O sea que el umbral estaba alto sin ganar nada. Se deja en 25 -- por
# debajo se empiezan a recoger nombres propios y fragmentos de dos palabras que
# no son citas de verdad.
_LARGO_MINIMO = 25

# Cuantas citas quedan por comprobar contra una fuente que SI esta en el repo.
# Se pone a mano y se compara exacto. Ver el comentario del final de `auditar`.
# ⚠️ Y LOS OTROS DOS RECUENTOS, CLAVADOS TAMBIEN. Con solo el primero clavado,
# una cita mal copiada podia esconderse cambiando de casilla: basta con que su
# parrafo deje de nombrar la fuente para que pase de «hay que mirarla» a «no dice
# de donde sale», que no se contaba. Paso de verdad -- 46 citas vivian ahi, y 15
# eran la MISMA frase de FEDIAF copiada mal en 14 filas de
# `requerimientos_v2_final.json`: remataba con «instead the nutritional maximum
# applies» cuando la fuente dice «instead the nutritional maximum, WHEN INCLUDED
# IN THE RELEVANT TABLES, should be taken into account». Una condicion borrada.
SIN_DECIR_DECLARADAS = 0          # citas que no dicen de que fuente salen
SIN_TEXTO_DECLARADAS = 11         # citan una fuente que no esta en el repo.
                                  # ⚠️ SUBE A 11 EL 12 DE SEPTIEMBRE, y no porque
                                  # se haya perdido ninguna fuente: es que entra a
                                  # esta auditoria `PREGUNTAS_ABIERTAS.md`, que
                                  # tenia una cita de Merck (la grasa de la
                                  # pancreatitis) que nadie miraba. Es la MISMA
                                  # frase que ya estaba declarada en PATOLOGIAS.md
                                  # y en patologias.json: tres copias de una cita
                                  # que sigue sin poderse comprobar aqui.
                                  # ⚠️ ERAN 24 HASTA EL 11 DE SEPTIEMBRE y ese
                                  # dia BAJARON A 10, porque se consiguieron
                                  # cuatro de las fuentes que faltaban: WSAVA
                                  # (sus guias y las graficas de condicion
                                  # corporal y masa muscular), IRIS 2026
                                  # (estadificacion y recomendaciones del
                                  # perro), el consenso ACVIM de Keene 2019 por
                                  # PubMed Central, y el articulo de Today's
                                  # Veterinary Practice sobre oxalato calcico.
                                  # CATORCE citas que no se podian comprobar
                                  # ahora se encuentran LITERALES en su fuente.
                                  # Las 10 que quedan son de Merck, dvm360
                                  # --que devuelve 403 a la lectura desde
                                  # aqui-- y Purina. Siguen sin poder
                                  # comprobarse, y se DICE.

# ⚠️ ESTE NUMERO DEPENDE DE OTRO REPO, Y ESO YA COSTO UN ROJO (11 de septiembre).
# `SIN_TEXTO_DECLARADAS` cuenta las citas cuya fuente NO ESTA, asi que se mueve
# solo cuando `canislab-fuentes` cambia -- y ese repo tiene su propia rama por
# defecto y su propio ritmo. Ese dia se bajaron cuatro fuentes, el numero bajo de
# 24 a 10 en local, se clavo el 10... y LA CI SEGUIA VIENDO 24, porque trae las
# fuentes con un `sparse-checkout` de `main` y alli las fuentes nuevas todavia
# estaban en una rama. Verde aqui y rojo alli, sin que nada del motor estuviera
# mal. La regla que sale de ahi: **una fuente nueva se fusiona en su repo ANTES
# de clavar el recuento aqui**, y los dos commits van juntos o no va ninguno.
# Es la misma regla que ya tenia `der_casos.json`, que vive en dos repos.

PENDIENTES_DECLARADAS = 0         # 10 de septiembre de 2026, noche: no queda
                                  # ninguna. Las 31 que quedaban se abrieron una
                                  # a una contra su fuente; las 31 estaban en el
                                  # libro y ninguna decia algo que la fuente no
                                  # diga -- lo que fallaba era como se habian
                                  # copiado. Ver el comentario del final.

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


# ⚠️ Y EL ALEMAN (12 de septiembre). El Merkblatt 181 de la TVT —la fuente de la
# que sale el bloqueo de los cortes con tiroides— esta en aleman, y una cita suya
# no tiene palabras inglesas ni españolas: los dos contadores daban 0, «0 > 0» es
# falso, y la cita se saltaba la auditoria SIN DECIRLO. Una cita que no se
# comprueba y nadie sabe que no se comprueba es el peor de los tres estados.
_ES_ALEMAN = re.compile(r"\b(?:der|die|das|und|nicht|bei|von|mit|auch|werden|"
                        r"kann|zu|den|dem|ein|eine|ist|sind|aus|für|durch|"
                        r"oder|wird|sich|bis|Hunde|Hunden|Katzen)\b")


def _parece_de_fuente(c):
    """Una cita en ingles o en aleman. Las que estan en español son prosa nuestra."""
    n_es = len(_ES_ESPANOL.findall(c))
    n_en = len(_ES_INGLES.findall(c))
    n_de = len(_ES_ALEMAN.findall(c))
    return max(n_en, n_de) > n_es


def _norm(t):
    """Espacios, comillas y guiones de corte de linea, todos iguales."""
    t = unicodedata.normalize("NFKC", t)
    # ⚠️ EL GUION BLANDO (U+00AD), que no se ve y rompe la comparacion
    # (12 de septiembre). El PDF de Ishii 2025 lo trae 100 veces: «prevent\u00ad\ning»
    # es «preventing» a la vista y son dos cosas distintas al comparar. NFKC no
    # lo toca, y la regla de abajo —quitar «guion + espacio»— tampoco, porque
    # este guion no es ninguno de los ocho de la lista. Se borra entero: nunca
    # significa nada, solo dice donde SE PODRIA partir la palabra.
    t = t.replace("\u00ad", "")
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
    #   El circunflejo va con ellos: el PDF imprime «BW^0,75» con el 0,75 en
    #   superindice y la extraccion lo deja «BW075», asi que el «^» que
    #   escribimos al citar no esta en el texto -- es NUESTRO, como los
    #   asteriscos de negrita.
    for a, b in (("⁻", "-"), ("¹", "1"), ("²", "2"), ("³", "3"), ("⁰", "0"),
                 ("·", " "), ("•", " "), ("^", "")):
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


# ⚠️ EL NUMERO DE PAGINA, QUE SE METE EN MEDIO DE LA FRASE. El PDF pone el pie
# de pagina entre dos parrafos, y al extraer el texto queda una linea con un
# numero solo justo donde la frase se parte: el NRC dice «a diet severely
# limiting / 293 / in methionine», o sea que la frase de la fuente ES continua y
# el texto extraido NO. Una cita literal correcta salia «no encontrada» por eso.
#
# La forma de quitarlo sin riesgo es exigir las TRES cosas a la vez: una linea
# que sea SOLO un entero de hasta cuatro cifras, con linea en blanco ANTES y
# DESPUES. Un numero dentro de una frase nunca cumple eso -- va pegado a
# palabras en su misma linea --, asi que esto no puede comerse una cifra de
# verdad. Es la diferencia con el intento que se descarto (quitar del texto
# cualquier numero suelto), que si podia dar por buena una cita a la que le
# faltara un dato.
_PIE_DE_PAGINA = re.compile(r"\n[ \t]*\n+[ \t]*\d{1,4}[ \t]*\n[ \t]*\n+")


def textos():
    """Todo el texto de fuente que hay en el repo de al lado, ya normalizado.

    Devuelve dos versiones de cada fichero: la normal y la que no lleva los
    numeros de pagina sueltos (ver `_PIE_DE_PAGINA`).
    """
    fuera, sin_pie = {}, {}
    # ⚠️ Y LOS TEXTOS DE FUENTE QUE VIVEN EN ESTE REPO, no en el de al lado
    # (12 de septiembre). Hoy son tres: las dos tablas de FEDIAF transcritas del
    # PDF para que `auditar_transcripcion_fediaf.py` las rehaga, y las tablas de
    # AAHA 2021, que NO se pueden extraer del PDF porque estan dibujadas como
    # trazos vectoriales -- la pagina de la Tabla 8 entera devuelve 194
    # caracteres. Sin esto, una cita de la Tabla 8 de AAHA caia en «cita una
    # fuente que no esta en el repo», que es justo la casilla que no se mira, y
    # la fuente SI esta: esta transcrita, con su metodo escrito en la cabecera
    # de `aaha_2021_tablas_transcritas.txt`.
    rutas = sorted(glob.glob(os.path.join(FUENTES, "**", "*.txt"), recursive=True))
    rutas += sorted(glob.glob(os.path.join(RAIZ, "*.txt")))
    # ⚠️ Y LOS .XML (12 de septiembre). Hofmann 2025 -- uno de los dos estudios que
    # el repo cita para el fosforo -- vive SOLO como XML de PubMed Central, sin
    # .txt al lado. O sea que sus citas no se podian comprobar y NO SALTABA: caian
    # en «cita una fuente que no esta en el repo» estando la fuente en el repo,
    # que es la casilla que menos se mira. Se le quitan las etiquetas y se indexa
    # como cualquier otro texto.
    rutas += sorted(glob.glob(os.path.join(FUENTES, "**", "*.xml"), recursive=True))
    for ruta in rutas:
        if os.path.getsize(ruta) < 1024:
            continue
        nombre = os.path.relpath(ruta, FUENTES if ruta.startswith(FUENTES) else RAIZ)
        crudo = open(ruta, encoding="utf-8", errors="ignore").read()
        if ruta.endswith(".xml"):
            crudo = html.unescape(re.sub(r"<[^>]+>", " ", crudo))
        fuera[nombre] = _norm(crudo)
        sin_pie[nombre] = _norm(_PIE_DE_PAGINA.sub("\n\n", crudo))
    return fuera, sin_pie


# Las fuentes cuyo TEXTO esta en el repo de al lado. Si una cita dice venir de
# una de estas y no aparece, es que hay que mirarla. Si dice venir de otra
# (Merck, el consenso ACVIM, Today's Veterinary Practice, Purina), no se puede
# comprobar aqui -- y eso se DICE, no se da por bueno.
# ⚠️ AMPLIADA EL 11 DE SEPTIEMBRE, en el mismo commit en que esas fuentes pasan
# a tener texto. Hasta hoy seis de ellas solo estaban en PDF, asi que una cita
# suya no se podia comprobar Y NO SALTABA: caia en «no dice de donde sale», que
# es la casilla que menos se mira. Ahora que el texto esta, una cita de
# Dobenecker, Heer o Ishii que no aparezca literal TIENE que salir por la casilla
# de las que hay que mirar. La lista y el texto van juntos o no sirve ninguno.
_EN_EL_REPO = ("fediaf", "sacn5", "small animal clinical nutrition", "nrc",
               "fascetti", "köber", "kober", "reglamento", "iris", "aaha", "tvt",
               "dobenecker", "hofmann", "heer", "ishii", "malandain", "sturmer",
               "stürmer", "hervera")
# ⚠️ «purina institute» Y NO «purina» A SECAS (12 de septiembre). La marca se
# llama igual que el nutriente en español y en ingles («purinas», «purine»), asi
# que con la clave corta cualquier parrafo sobre purinas se atribuia a la marca y
# se iba a la casilla de «no se puede comprobar». Las cinco citas que de verdad
# son suyas dicen «Purina Institute», asi que la clave larga las coge todas.
_FUERA = ("acvim", "merck", "purina institute", "today's veterinary", "cavanaugh",
          "center", "consenso")


# ⚠️ SE BUSCA POR PALABRA ENTERA, Y NO ES COSMETICO (12 de septiembre). Antes se
# buscaba por trozo, y «purina» -- la marca, que esta en la lista de fuentes que
# NO estan en el repo -- casaba dentro de «purinas» y de «purine». O sea que
# CUALQUIER frase que hablara de purinas se atribuia a Purina y se iba a la
# casilla de «no se puede comprobar», que es la que menos se mira, estando su
# fuente (Ishii 2025) en el repo. Paso con dos citas el dia que se leyo ese
# estudio. Mismo riesgo con «center» dentro de «centered» o «nrc» dentro de otra
# cosa: se arregla para todas a la vez.
def _clave_en(claves, texto):
    for k in claves:
        if re.search(r"\b" + re.escape(k) + r"\b", texto):
            return k
    return None


def _quien_dice(contexto):
    # ⚠️ CON LOS ESPACIOS APLASTADOS, porque una clave de dos palabras se parte
    # con el salto de linea del Markdown: «Purina\nInstitute» no casaba con
    # «purina institute» y la cita se quedaba sin fuente (12 de septiembre).
    c = " ".join(contexto.lower().split())
    k = _clave_en(_FUERA, c)
    if k:
        return ("fuera", k)
    k = _clave_en(_EN_EL_REPO, c)
    if k:
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
                # el contexto es el PARRAFO de la cita, no un trozo fijo de
                # caracteres: con 400 hacia atras se pegaba la fuente de la cita
                # de al lado, y una cita de Today's Veterinary Practice salia
                # clasificada como de SACN5; con una sola linea se perdia la
                # linea «**Fuente:** Merck Veterinary Manual» que esta JUSTO
                # encima, y una cita de Merck -- que no se puede comprobar aqui
                # porque el manual no esta en el repo -- salia acusada de ser de
                # FEDIAF y no aparecer. El parrafo es el trozo que de verdad
                # comparte fuente.
                ini = t.rfind("\n\n", 0, m.start())
                fuera.append((f, c, t[ini + 2 if ini >= 0 else 0:m.end() + 200]))
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
                        # el contexto son las DOS cosas: la `fuente` del bloque
                        # padre Y el propio texto donde vive la cita. Con solo
                        # la primera, «el consenso ACVIM ... «no drug or dietary
                        # treatment is recommended»» salia como «no dice de donde
                        # sale» -- y lo dice, en su misma frase.
                        fuera.append((f, c, (ctx + " " + o).strip()))
        _anda(_d)
    return fuera


def auditar(mostrar_todas=False):
    fallos = []
    tx, tx_sin_pie = textos()
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
        # Tercer intento: el mismo texto sin los numeros de pagina sueltos.
        if donde is None:
            for nombre, t in tx_sin_pie.items():
                if all(x in t for x in trozos):
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
    if SIN_DECIR_DECLARADAS is not None and len(sin) != SIN_DECIR_DECLARADAS:
        fallos.append(
            f"hay {len(sin)} citas que no dicen de que fuente salen y el fichero declara "
            f"{SIN_DECIR_DECLARADAS}. Una cita sin fuente no la comprueba nadie: o se le "
            f"pone la fuente al lado, o deja de ir entre comillas angulares")
    if SIN_TEXTO_DECLARADAS is not None and len(fuera_) != SIN_TEXTO_DECLARADAS:
        fallos.append(
            f"hay {len(fuera_)} citas cuya fuente no esta en el repo y el fichero declara "
            f"{SIN_TEXTO_DECLARADAS}. Si ha subido, se ha escrito una cita nueva que aqui "
            f"no se puede comprobar; si ha bajado, se cambia este numero en el mismo commit")
    return fallos


if __name__ == "__main__":
    fs = auditar("--todas" in sys.argv)
    print("\nDiscrepancias:", len(fs))
    sys.exit(1 if fs else 0)
