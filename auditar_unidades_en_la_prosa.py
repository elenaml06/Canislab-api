# -*- coding: utf-8 -*-
"""Que ningun documento escriba un nutriente en una unidad imposible.

⚠️ POR QUE EXISTE (15 de septiembre de 2026). Elena, despues de cazar ella un
error de unidad que la bateria no veia:

    «no podemos depender de que yo cace cosas, todo tienes que comprobarlo tu
     [...] yo he hecho esa pregunta del selenio, pero y si no la llego a hacer??»

EL ERROR QUE LO MOTIVO: `CLAUDE.md` listaba los siete maximos legales bajo una
unidad comun, «mg/100 g MS», y el selenio va en **µg**. O sea 568 mg/kg de
materia seca en vez de 0,568 mg/kg: MIL VECES. El JSON siempre lo tuvo bien y el
motor nunca aplico una cifra mala -- el solver lee el JSON, no el resumen --,
pero el documento que se lee para entender el motor decia algo falso, y quien lo
leyera se lo creeria. De hecho paso: lo lei yo media hora despues.

POR QUE NO BASTA EL BLOQUE 119. Ese ancla quince cifras **a mano**, y una lista
escrita a mano no da error cuando se queda corta: la cifra numero dieciseis no la
mira nadie. Es la leccion que este repo repite mas veces -- las seis categorias
de Personalizar, los cinco niveles de actividad, los 163 alimentos de la app, las
once copias de `CAT_SUPLEMENTO`. Esto no ancla nada: **barre**.

COMO FUNCIONA, Y POR QUE ES ESTRECHO A PROPOSITO.

Busca en la prosa los pares «<nutriente> … <cifra> <unidad>/<denominador>» y
convierte la cifra a UNA unidad canonica (mg). Luego la compara con TODO lo que
el motor tiene para ese nutriente en ese mismo denominador -- minimo y maximo de
FEDIAF, techo legal, techos y suelos del libro, topes cronicos -- y se queda con
el valor mas cercano.

Y solo acusa cuando la razon es una POTENCIA DE DIEZ LIMPIA (x10, x100, x1000, o
sus inversas, con un 2 % de tolerancia). Esa es la firma de un error de unidad y
casi de nada mas:

  · una cifra historica que el documento cita a proposito («antes ponia 4124»)
    esta en el mismo orden de magnitud -> no salta;
  · una atribucion equivocada del barrido -- el nutriente mas cercano en el texto
    no siempre es del que habla la frase -- suele dar una razon rara (67, 3,4)
    y no una potencia de diez -> no salta;
  · un mg escrito donde iba un µg da 1000 CLAVADO -> salta.

Una auditoria que acusa a quien no ha hecho nada se deja de mirar, que es el
fallo que `auditar_citas.py` ya cometio dos veces. Por eso prefiere callar antes
que gritar: lo que persigue es el fallo de mil, que es el que hace dano.

LOS DOS PUNTOS CIEGOS, declarados porque una auditoria tiene que decir donde NO
llega:

  1. Si el nutriente no se nombra dentro de los 220 caracteres anteriores al
     numero, la cifra NO se comprueba. Ese recuento se imprime -- hoy 287 de
     801 -- para que el hueco se vea: un barrido cuyo resultado no se compara
     contra el total es una muestra, no un barrido.
  2. Un error de unidad que caiga DENTRO del rango del propio nutriente. «671
     mg/1000 kcal» de vitamina E es x10 de su suelo (67,1) y solo x4 de su
     techo (167,75), asi que no esta fuera de rango y calla. Es el precio de no
     acusar a nadie sin motivo, y es el lado correcto por el que equivocarse.

COMPROBADO CON EL FALLO PUESTO DE OCHO FORMAS, y caza seis: selenio en mg (el
real), cobre x1000, zinc x1000, hierro /10, manganeso x100 y fosforo x1000. Los
dos que se le escapan son los dos puntos ciegos de arriba.

LO QUE **NO** MIRA, y va declarado: las cifras en UI. Para compararlas haria
falta saber en que forma quimica esta el nutriente (la vitamina E en
d-alfa-tocoferol son 0,671 mg/UI y en acetato sintetico otra cosa), y suponerla
seria inventarse justo el dato que `fediaf_conversiones_vitaminas.json` existe
para no inventar. Las UI las vigila el BLOQUE 116 contra la Tabla VII-14.
"""
import re, json, sys, glob, os, unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
sys.path.insert(0, os.path.join(RAIZ, "motor"))


def _norm(s):
    return ''.join(c for c in unicodedata.normalize('NFD', s.lower())
                   if unicodedata.category(c) != 'Mn')


# ⚠️ LOS NOMBRES SE DERIVAN DE LA TABLA, NO SE ESCRIBEN (15 de septiembre de
# 2026). La primera version llevaba diecisiete a mano y le faltaba «grasa»: en
# «… | Sodio | 750-1250 mg | 290 |  Más grasa ≤37,5 g/1000 kcal», la cifra de la
# GRASA se atribuia al SODIO de la celda de al lado --porque era el nutriente
# mas cercano DE LOS QUE ESTABAN EN LA LISTA-- y salia acusada de estar x10.
# Dos falsos positivos, los dos por lo mismo.
#
# Es la forma de fallo que este repo tiene escrita mas veces: una lista copiada
# a mano no da error cuando se queda corta. Asi que se derivan de la propia
# tabla de FEDIAF -- «Proteína_total» -> «proteina», «Vitamina_D» -> «vitamina
# d» --, y un nutriente nuevo entra solo. Los alias son para las formas en que
# la prosa los llama de verdad.
def _nombres_de_la_tabla():
    fuera = {}
    with open(os.path.join(RAIZ, "requerimientos_v2_final.json"), encoding="utf-8") as f:
        for fila in json.load(f):
            nom = fila["nutriente"]
            llano = _norm(nom).replace("_total", "").replace("_", " ").strip()
            if len(llano) >= 4:
                fuera[llano] = nom
    return fuera


ALIAS = {"fosforo": "Fósforo", "grasa": "Grasa_total", "proteina": "Proteína_total",
         "vitamina d": "Vitamina_D", "vitamina a": "Vitamina_A",
         "vitamina e": "Vitamina_E", "acido linoleico": "Linoleico"}

# ⚠️ LO QUE LA PROSA NOMBRA Y EL MOTOR NO TIENE. Si una de estas palabras esta
# MAS CERCA del numero que el nutriente reconocido, la cifra no es del
# reconocido y no se puede comprobar: se calla. Sin esto, «glutamina >=500
# mg/100 kcal = 5 g/1000 kcal» se atribuia a la PROTEINA --el nutriente
# conocido mas cercano-- y salia acusada de estar a x0,1.
#
# Esta lista solo sirve para CALLAR, nunca para acusar, asi que quedarse corta
# cuesta un falso positivo visible y no un fallo escondido. Es al reves que las
# listas que este repo tiene prohibido escribir a mano.
NO_LOS_TIENE_EL_MOTOR = ("glutamina", "glutamato", "glucosamina", "condroitina",
                         "creatina", "betaina", "inositol", "nucleotidos",
                         "colageno", "prebiotic", "probiotic", "levadura",
                         "psyllium", "pectina", "almidon", "lactosa")
# a miligramos
A_MG = {"µg": 1e-3, "ug": 1e-3, "mcg": 1e-3, "mg": 1.0, "g": 1e3}

PAT = re.compile(
    r"([0-9][0-9.,\s]{0,12}[0-9]|[0-9])\s*(µg|ug|mcg|mg|g)\b\s*(?:/|por\s+)\s*"
    r"(1000\s?kcal|100\s?g\s?MS|kg\s?MS|g\s?MS)", re.I)

# el denominador, llevado a «por 1000 kcal» o «por 100 g de MS»
def _denominador(t):
    t = _norm(t).replace(" ", "")
    if "1000kcal" in t:
        return "kcal"
    return "ms"          # 100 g MS, kg MS o g MS: todo materia seca


def _a_100g_ms(valor_mg, texto_den):
    """Lleva la cifra a mg por 100 g de materia seca."""
    t = _norm(texto_den).replace(" ", "")
    if t.startswith("100gms"):
        return valor_mg
    if t.startswith("kgms"):
        return valor_mg / 10.0        # 1 kg = 10 x 100 g
    if t.startswith("gms"):
        return valor_mg * 100.0
    return valor_mg


def _cifra(t):
    t = t.replace(" ", "").replace(" ", "")
    # 5.155 es cinco mil ciento cincuenta y cinco; 56,80 es coma decimal
    t = t.replace(".", "").replace(",", ".")
    try:
        return float(t)
    except ValueError:
        return None


def valores_del_motor():
    """Todo lo que el motor tiene para cada nutriente, en mg, por denominador."""
    import verificar
    import recomendaciones
    import seguridad
    req = {f["nutriente"]: f for f in
           json.load(open(os.path.join(RAIZ, "requerimientos_v2_final.json"),
                          encoding="utf-8"))}
    ETAPAS = ("Adulto", "CachorroJoven", "CachorroCrecimiento")
    out = {}
    for nom, fila in req.items():
        u = A_MG.get((fila.get("unidad") or "").strip())
        if u is None:
            continue                     # ratios, UI, g de proteina: fuera
        kcal, ms = set(), set()
        for et in ETAPAS:
            for f in (verificar.minimo_de, verificar.maximo_de):
                try:
                    v = f(fila, nom, et)
                except Exception:
                    v = None
                if v:
                    kcal.add(float(v) * u)
            try:
                v = verificar.maximo_por_g_de_materia_seca(fila, nom, et)
            except Exception:
                v = None
            if v:
                ms.add(float(v) * u * 100.0)        # por g MS -> por 100 g MS
        out[nom] = {"kcal": kcal, "ms": ms}
    # los techos y suelos del libro, y los topes cronicos, en las mismas unidades
    lib = json.load(open(os.path.join(RAIZ, "recomendaciones_libro.json"),
                         encoding="utf-8"))["por_etapa"]
    CLAVE_A_FILA = {"calcio": "Calcio", "fosforo": "Fósforo", "sodio": "Sodio",
                    "vitE": "Vitamina_E", "vitD": "Vitamina_D",
                    "linoleico": "Linoleico"}
    for et, d in lib.items():
        for bloque in ("topes_por_1000kcal", "suelos_por_1000kcal"):
            for clave, x in (d.get(bloque) or {}).items():
                fila = CLAVE_A_FILA.get(clave)
                if not fila or fila not in out:
                    continue
                u = A_MG.get((req[fila].get("unidad") or "").strip(), 1.0)
                # el libro escribe en la MISMA unidad que el motor para ese
                # nutriente, que es como lo aplica el solver
                out[fila]["kcal"].add(float(x["valor"]) * u)
    for nom, cte in (("Vitamina_D", "TOPE_VITD_KCAL"), ("Yodo", "TOPE_YODO_KCAL"),
                     ("Selenio", "TOPE_SELENIO_KCAL")):
        v = getattr(seguridad, cte, None)
        if v and nom in out:
            u = A_MG.get((req[nom].get("unidad") or "").strip(), 1.0)
            out[nom]["kcal"].add(float(v) * u)
    return out


POTENCIAS = (0.001, 0.01, 0.1, 10.0, 100.0, 1000.0)


def barrer(rutas=None, tolerancia=0.02):
    vals = valores_del_motor()
    NOMBRES = dict(_nombres_de_la_tabla())
    NOMBRES.update(ALIAS)
    NOMBRES = {k: v for k, v in NOMBRES.items() if v in vals}
    rutas = rutas or sorted(glob.glob(os.path.join(RAIZ, "*.md")))
    # ⚠️ SE CUENTA LO QUE NO SE HA PODIDO MIRAR, y no es decoracion: un barrido
    #    cuyo resultado no se compara contra el TOTAL no es un barrido, es una
    #    muestra -- la leccion de `VERIFICACION_FILA_A_FILA.md`, donde cortar la
    #    salida con `sed` dejo 40 tablas revisadas de 89 y nadie se entero.
    #    Aqui el punto ciego es real: si el nutriente no se nombra cerca del
    #    numero, la cifra no se comprueba. Que ese numero se vea obliga a
    #    saberlo en vez de creer que se miran todas.
    mirados, acusados, sin_atribuir = 0, [], 0
    for ruta in rutas:
        txt = open(ruta, encoding="utf-8").read()
        for m in PAT.finditer(txt):
            ctx = _norm(txt[max(0, m.start() - 220):m.start()])
            # ⚠️ GANA EL MAS CERCANO AL NUMERO, Y ESO ES `rfind`, NO EL ORDEN DEL
            #    DICCIONARIO. La primera version se quedaba con «el ultimo que
            #    casara» recorriendo `NOMBRES`, que esta en orden arbitrario, y
            #    por eso NO CAZABA EL FALLO QUE ESTE FICHERO EXISTE PARA CAZAR:
            #    en «… manganeso 17,00 mg/100 g MS · selenio 56,80 mg/100 g MS»
            #    la cifra del selenio se atribuia a manganeso -- que aparece
            #    despues en el diccionario -- y 56,80/0,17 son 334, que no es
            #    potencia de diez, asi que callaba. Comprobado: con esto puesto
            #    salta, y sin esto no.
            nut, _donde = None, -1
            for nombre, clave in NOMBRES.items():
                _i = ctx.rfind(nombre)
                if _i > _donde:
                    nut, _donde = clave, _i
            # y si uno de los que el motor NO tiene esta mas cerca, la cifra no
            # es del que hemos reconocido: no se puede comprobar, no se acusa
            if nut is not None and any(ctx.rfind(x) > _donde for x in NO_LOS_TIENE_EL_MOTOR):
                continue
            if not nut or nut not in vals:
                sin_atribuir += 1
                continue
            v = _cifra(m.group(1))
            if v is None:
                continue
            den = _denominador(m.group(3))
            mg = v * A_MG[m.group(2).lower()]
            if den == "ms":
                mg = _a_100g_ms(mg, m.group(3))
            candidatos = vals[nut][den]
            if not candidatos:
                continue
            mirados += 1
            razones = [mg / c for c in candidatos if c]

            def _lejania(r):
                return abs(1.0 - r) if r >= 1 else abs(1.0 - 1.0 / r)

            # Si ALGUNA cifra del motor cuadra, la de la prosa es plausible y no
            # se toca: puede ser un minimo, un maximo, un techo del libro o un
            # tope cronico, y todos son legitimos de citar.
            mejor = min(razones, key=_lejania)
            if 1.0 / (1 + tolerancia) <= mejor <= (1 + tolerancia):
                continue
            # ⚠️ Y SE MIRA LA RAZON MAS CERCANA, NO TODAS (15 de septiembre de
            #    2026). La primera version exigia que TODAS las razones fueran la
            #    misma potencia de diez, y con eso se le escapaba la vitamina D
            #    escrita en mg: sus tres cifras (tope cronico 20 µg, maximo legal
            #    14,19 y minimo 3,98) dan x1000, x1409 y x5031, que no coinciden,
            #    asi que callaba. Lo que delata un error de unidad es que la
            #    cifra este a UNA POTENCIA DE DIEZ LIMPIA del valor MAS PROXIMO
            #    -- si el nutriente tiene varias cifras, la de al lado es la que
            #    se estaba citando. Medido al aflojarlo: de 0 a 0 falsos
            #    positivos en las 253 cifras de los 26 documentos.
            # ⚠️ Y BASTA CON QUE **ALGUNA** RAZON SEA POTENCIA DE DIEZ LIMPIA,
            #    no la mas cercana. Con «la mas cercana» se escapaban dos de los
            #    ocho fallos de prueba: «671 mg/1000 kcal» de vitamina E esta x10
            #    del suelo del libro (67,1) y x4 del techo (167,75), y ganaba el
            #    x4, que no es potencia de diez. Un nutriente con varias cifras
            #    tiene varias razones, y la que delata el error de unidad es la
            #    que sale redonda, este donde este. Medido al aflojarlo: sigue en
            #    0 falsos positivos sobre las 514 cifras de los 26 documentos.
            # Hacen falta LAS DOS COSAS, y esto se midio con los ocho fallos de
            # prueba y los 26 documentos delante:
            #
            #   (a) que la cifra este fuera de rango para TODO lo que el motor
            #       tiene de ese nutriente (toda razon >= 10 o <= 0,1). Si cae
            #       DENTRO del rango, no se puede afirmar que este mal: «83,9
            #       mg/1000 kcal» de vitamina E es x10 del minimo del cachorro
            #       (8,39) y a la vez 1,25 veces el suelo del libro (67,1) --o
            #       sea una cifra perfectamente normal-- y con la regla suelta
            #       salia acusada. Siete falsos positivos asi.
            #   (b) y que ADEMAS alguna razon sea potencia de diez limpia, que
            #       es la firma del error de unidad.
            #
            # LO QUE ESTO **NO** CAZA, y va escrito porque una auditoria tiene
            # que decir donde no llega: un error de unidad que caiga dentro del
            # rango del propio nutriente. «671 mg/1000 kcal» de vitamina E es x10
            # de su suelo y solo x4 de su techo, asi que no esta fuera de rango y
            # calla. Es el precio de no acusar a nadie sin motivo, y es el lado
            # correcto por el que equivocarse: de los ocho fallos de prueba caza
            # seis, incluido el que lo motivo.
            fuera_de_rango = all(r >= 10.0 or r <= 0.1 for r in razones)
            pot = ([p for p in POTENCIAS
                    if any(abs(r / p - 1.0) <= tolerancia for r in razones)]
                   if fuera_de_rango else [])
            if pot:
                linea = txt[:m.start()].count("\n") + 1
                acusados.append((os.path.basename(ruta), linea, nut, v,
                                 m.group(2), m.group(3), pot[0],
                                 txt[max(0, m.start() - 70):m.end()].replace("\n", " ")))
    return mirados, acusados, sin_atribuir


if __name__ == "__main__":
    mirados, acusados, sin_atribuir = barrer()
    print(f"  {mirados} cifras «nutriente + numero + unidad» comprobadas contra el motor")
    print(f"  {sin_atribuir} encontradas y NO comprobadas: el nutriente no se nombra cerca "
          f"del numero, asi que no se sabe de cual habla")
    for f, ln, nut, v, u, den, pot, ctx in acusados:
        print(f"  ⚠️  {f}:{ln}  {nut}: «{v} {u}/{den}» esta x{pot:g} de TODO lo que el motor "
              f"tiene para ese nutriente. Mira la UNIDAD antes que la cifra.")
        print(f"        …{ctx[-90:]}")
    print()
    print(f"Discrepancias: {len(acusados)}")
    sys.exit(1 if acusados else 0)
