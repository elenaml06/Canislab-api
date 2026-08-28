# -*- coding: utf-8 -*-
"""
PASOS 4 y 5: verificar contra FEDIAF y cerrar huecos con suplementos.

Esta es la parte que legitima la racion. La plantilla es solo el punto de
partida; lo que se puede defender ante un veterinario es ESTO: "cubre 26 de
27 nutrientes, y estos dos se quedan al 80%".
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constructor import perfil_nutricional, valor_nutriente

# Nombre del requisito -> clave en los nutrientes de cada alimento
MAPA = {
    "Proteína_total": "proteina", "Grasa_total": "grasa", "Calcio": "calcio",
    "Fósforo": "fosforo", "Potasio": "potasio", "Sodio": "sodio",
    "Cloruro": "cloruro", "Magnesio": "magnesio", "Cobre": "cobre",
    "Yodo": "yodo", "Hierro": "hierro", "Manganeso": "manganeso",
    "Selenio": "selenio", "Zinc": "zinc", "Vitamina_A": "vitA",
    "Vitamina_D": "vitD", "Vitamina_E": "vitE", "Tiamina": "tiamina",
    "Riboflavina": "riboflavina", "Acido_pantotenico": "acidoPantotenico",
    "Vitamina_B6": "vitB6", "Vitamina_B12": "vitB12", "Niacina": "niacina",
    "Folato": "folato", "Colina": "colina", "Linoleico": "linoleico",
    "Linolénico": "linolenico", "Araquidónico": "araquidonico",
    # ⚠️ "epa_dha" NO es una clave de los alimentos: es la SUMA de epa y dha,
    # que calcula `valor_nutriente` (constructor.py). Estuvo mapeado a "epa"
    # a secas hasta el 25 de agosto -- el requisito se llamaba EPA+DHA y
    # comprobaba solo la mitad. Ver el comentario largo de allí.
    "EPA_DHA_total": "epa_dha",
    # ⚠️ LOS DOCE AMINOÁCIDOS ESENCIALES — ACTIVADOS EL 28 DE AGOSTO.
    #
    # Estaban en requerimientos_v2_final.json desde el 26 de agosto y fuera
    # de aquí a propósito: ninguna ficha del catálogo traía el dato, y un
    # alimento sin aminograma no cuenta como "no lo sé", cuenta como CERO.
    # Con los 159 a cero, el mínimo era inalcanzable y no salía ni un menú.
    # Cargados los primeros 49, el fallo cambiaba de forma y dejaba de
    # verse: ya no bloqueaba, DESPLAZABA -- el motor se iría hacia los que
    # tuvieran dato, y el menú saldría verde porque el semáforo mide el
    # mismo cero.
    #
    # Se encienden ahora porque las tres cosas que hacían falta están
    # medidas, no supuestas:
    #   · 94 de las 159 fichas traen aminograma, y de un menú REAL solo el
    #     1,0 % de la proteína viene de alimentos sin él. Nueve de los diez
    #     huesos carnosos lo tienen -- era el que más pesaba, el 20-60 % de
    #     la ración.
    #   · El aminoácido más justo se queda en x2,12 de su mínimo (la
    #     metionina); el resto entre x2,26 y x5,02. Una ración de carne va
    #     sobrada, así que estos doce mínimos casi nunca van a apretar.
    #   · Con ellos puestos salen 20 de 20 menús, el hueso carnoso sigue en
    #     los 20 y su mediana sube de 207 a 216 g.
    #
    # Que casi nunca aprieten no los hace inútiles: existen para el menú que
    # NO es el de todos los días -- una dieta muy restringida por alergias,
    # una patología que aprieta, un menú que el usuario edita a la baja.
    # Ahí es donde un aminoácido se puede quedar corto, y hasta hoy nada lo
    # habría visto.
    #
    # ⚠️ "metionina_cistina" y "fenilalanina_tirosina" NO son claves de los
    # alimentos: son SUMAS que calcula `valor_nutriente` (constructor.py),
    # igual que "epa_dha". FEDIAF pide los cuatro requisitos -- el
    # aminoácido solo Y la suma con su pareja -- porque la cistina se
    # fabrica a partir de la metionina y la tirosina a partir de la
    # fenilalanina, así que la pareja ahorra al esencial.
    "Arginina": "arginina", "Histidina": "histidina",
    "Isoleucina": "isoleucina", "Leucina": "leucina", "Lisina": "lisina",
    "Metionina": "metionina", "Metionina_cistina": "metionina_cistina",
    "Fenilalanina": "fenilalanina",
    "Fenilalanina_tirosina": "fenilalanina_tirosina",
    "Treonina": "treonina", "Triptofano": "triptofano", "Valina": "valina",
}
# ⚠️ EL ÚNICO MÁXIMO DE FEDIAF QUE NO SE APLICA, Y AQUÍ ESTÁ POR QUÉ
# (28 agosto). La Tabla III-3b pone un solo máximo a un aminoácido: lisina
# 7,00 g/1000 kcal, y solo en crecimiento ("Growth: 7.00 (N)"). Está bien
# transcrito -- lo comprueba auditar_fediaf.py contra el PDF.
#
# Al encender los doce aminoácidos se midió qué pasaba con él:
# **0 de 15 menús de cachorro caben debajo.** Salen entre 8,79 y 12,12.
# No es que el motor se pase por poco en algún caso raro: es que NINGUNA
# ración BARF de cachorro cabe.
#
# Y el motivo se ve en la propia ración: esos menús llevan unos 134 g de
# proteína por 1000 kcal, y el mínimo de FEDIAF para un cachorro son 50.
# Una dieta de carne cruda tiene dos veces y media la proteína de
# referencia, y la lisina va detrás de la proteína. El 7,00 está pensado
# para un pienso al nivel de proteína de la tabla.
#
# Aplicarlo dejaría a TODOS los cachorros sin menú. No aplicarlo es dejar
# de comprobar un máximo de FEDIAF. Las dos cosas son malas, así que no se
# decide aquí a escondidas: se aplica lo segundo, se escribe, se prueba, y
# la pregunta ("¿el 7,00 se mide sobre la proteína de la tabla o sobre la
# del plato?") va a PENDIENTE.md para el nutricionista.
#
# Los once mínimos de lisina y los otros once aminoácidos SÍ se aplican.
# Esto es solo el techo.
#
# Está aquí, junto a MAPA, porque el solver y el semáforo tienen que leer
# la MISMA lista. Si cada uno tuviera la suya, el motor podría construir un
# menú que el semáforo rechazara, o al revés -- que es el fallo de la fibra.
MAXIMOS_NO_APLICADOS = {"Lisina"}

# Etapas que existen en requerimientos_v2_final.json. Senior, Gestante y
# Lactante NO tienen columna propia: FEDIAF no da un perfil de nutrientes
# distinto para senior, y gestacion/lactancia usan la columna de crecimiento
# temprano ("Early Growth & Reproduction"). Lo que SI cambia en esas etapas
# son las kcal, y de eso se encarga der.py.
EQUIVALENCIA = {"Senior": "Adulto", "Gestante": "CachorroJoven",
                "GestanteTemprana": "CachorroJoven", "GestanteTardia": "CachorroJoven",
                "Lactante": "CachorroJoven"}
SUFIJO = {"Adulto": "Adulto", "CachorroJoven": "CachorroJoven",
          "CachorroCrecimiento": "CachorroCrecimiento"}


def _num(v):
    if v in (None, "", "-"):
        return None
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def maximo_de(r, nombre_req, etapa):
    """El máximo de FEDIAF de un requisito, o None si no tiene.

    ES EL ÚNICO SITIO que sabe cuáles no se aplican. El solver, el semáforo,
    el analizador y `suplementar()` leen el máximo por aquí, para que no
    puedan discrepar: si el motor construyera un menú con un techo que el
    semáforo no aplica (o al revés), tendríamos otra vez lo de la fibra.
    """
    if nombre_req in MAXIMOS_NO_APLICADOS:
        return None
    return _num(r.get(f"max{etapa}")) or _num(r.get("maxAdulto"))


# ⚠️ LOS MINIMOS SUBEN CUANDO SE COME MENOS (28 agosto). Es la ecuacion
# de la propia FEDIAF, apartado 7.2.5, p. 60:
#
#     unidades/1000 kcal = requerimiento_por_kg^0,75 x 1000 / DER
#
# y su propio parrafo diciendo por que: «the energy needs may be satisfied
# before the requirements of protein, minerals or vitamins are met [...]
# hence a systematic adjustment applied to all essential nutrients is
# needed WHEN FED BELOW the NRC standard assumption».
#
# En cristiano: el perro necesita los mismos MILIGRAMOS de zinc coma lo que
# coma. Si come menos, esos miligramos tienen que caber en menos calorias,
# asi que el minimo POR 1000 KCAL sube. Hasta hoy no subia, y eso significa
# que un perro a dieta de adelgazamiento recibia la misma densidad de
# nutrientes que uno normal justo cuando menos margen tiene. A DER 63 -que
# es la media MEDIDA de una bajada de peso, AAHA 2021- la proteina minima
# pasa de 52,1 a 78,6 g/1000 kcal: un 51% mas.
#
# LAS DOS COLUMNAS DE FEDIAF NO SON CONSISTENTES ENTRE SI, y eso decide la
# forma de la regla. FEDIAF publica dos: la de DER 110 y la de DER 95.
# Derivar una de la otra deberia dar la publicada y no lo da:
#
#     selenio seco    55,00 / 45,00 = 1,222      <- no es redondeo
#     selenio humedo  67,50 / 57,50 = 1,174
#     todo lo demas                   1,158  ( = 110/95 )
#
# 55 y 45 son numeros redondos: FEDIAF subio el selenio mas que el resto a
# proposito. Asi que por debajo de 95, donde NO hay nada publicado, se coge
# el MAYOR de los dos anclajes escalados. Ninguno domina: en magnesio y
# cloruro gana el de 110, en selenio y calcio el de 95. Con el maximo, la
# inconsistencia de FEDIAF se resuelve siempre hacia la suficiencia.
#
# Y en 95 y en 110 se devuelve el valor PUBLICADO, exacto. Donde FEDIAF
# tiene un numero, no se inventa otro.
#
# ⚠️ SOLO EN ADULTO. Las dos columnas de la ecuacion son de mantenimiento;
# para crecimiento, gestacion y lactancia FEDIAF publica otras columnas y
# la ecuacion no esta verificada ahi. No se escala.
#
# ⚠️ LA GRASA ESTA EXENTA, y no es un olvido: FEDIAF publica 13,75 g/1000
# kcal en las DOS columnas. Escalarla haria que las kcal dejaran de cerrar.
DER_ANCLA_ALTA = 110.0
DER_ANCLA_BAJA = 95.0
NO_SE_ESCALAN = {"Grasa_total"}


# ⚠️ EL PESO OBJETIVO DESDE EL BCS (28 agosto). Regla de AAHA 2014,
# corroborada por Teixeira 2024: «Each BCS >= 5 (on a 9 point scale) ... is
# equivalent to being 10 % overweight». Y su ejemplo trabajado, que es el
# test: «a 45 kg Labrador retriever that has a BCS of 8 out of 9 is 30 %
# overweight and its ideal weight is approximately 32 kg».
#
#     45 x (1 - 0,30) = 31,5      <- RESTA
#     45 / (1 + 0,30) = 34,6      <- dividir. MAL. Tres kilos.
#
# Ninguna de las dos fuentes publicadas divide.
#
# SE ROMPE EN LOS DOS EXTREMOS, y uno falla hacia el lado peligroso:
#
# · POR ABAJO. Con BCS 3 la formula se da la vuelta y devuelve un objetivo
#   MAYOR que el peso real: un perro de 15 kg saldria a 18. La regla de
#   AAHA esta definida solo hacia arriba («BCS >= 5»). Y no es cosmetico:
#   con 18 en vez de 15 la DER efectiva sale un 15% mas baja y los minimos
#   escalarian un 15% de mas en un perro que ni esta a dieta. Sale por el
#   lado conservador, pero es un numero que no ha decidido nadie.
#
# · POR ARRIBA es peor. En BCS 9 la formula da un 40% de exceso, pero la
#   escala se satura: el 9/9 cubre desde un 40% hasta mas del 100%. La
#   referencia publicada solo llega a 8 -- la Global Pet Obesity Initiative
#   (2019, firmada por el ECVCN, la WSAVA y la ACVIM) define obesidad como
#   30% sobre el ideal y dice que eso equivale a 8/9. Por encima nadie
#   publica la equivalencia. Y ahi el error va hacia el lado MALO: si el
#   perro esta un 60% por encima y la formula dice 40%, el objetivo sale
#   demasiado alto y con el demasiadas kcal, justo en el perro que peor lo
#   lleva. En BCS 9 no se estima: hace falta el peso declarado.
#
# Los medios puntos valen 5%: la regla es lineal y un 6,5 o un 7,5 no se
# redondean.
BCS_NEUTRO = 5.0
BCS_MAXIMO_PUBLICADO = 8.0


def peso_objetivo_desde_bcs(peso_actual_kg, bcs):
    """El peso objetivo estimado desde el BCS, o None si no se puede.

    Devuelve None -y hay que pedir el peso declarado- por debajo de BCS 5
    (la regla no existe hacia abajo) y en BCS 9 (la escala se satura y la
    estimacion se queda corta justo donde mas duele).
    """
    try:
        p = float(peso_actual_kg)
        b = float(bcs)
    except (TypeError, ValueError):
        return None
    if p <= 0 or b <= BCS_NEUTRO or b > BCS_MAXIMO_PUBLICADO:
        return None
    exceso = 0.10 * (b - BCS_NEUTRO)
    return round(p * (1.0 - exceso), 3)


def minimo_de(r, nombre_req, etapa, der_efectiva=None):
    """El mínimo de FEDIAF de un requisito, escalado por la DER efectiva.

    ES EL ÚNICO SITIO que sabe escalar. El solver y el semáforo leen el
    mínimo por aquí, igual que leen el máximo por `maximo_de()`: si cada
    uno escalara por su cuenta, el motor podría construir un menú que el
    semáforo rechazara.

    `der_efectiva` son las kcal de la ración por kg de peso metabólico.
    Sin ella (o fuera de adulto) se devuelve el mínimo publicado tal cual.
    """
    mn = _num(r.get(f"min{etapa}"))
    if mn is None or der_efectiva is None or etapa != "Adulto":
        return mn
    if nombre_req in NO_SE_ESCALAN:
        return mn
    v110 = _num(r.get("minAdulto110"))
    if v110 is None:
        # Sin las dos anclas no se escala: son los tres que FEDIAF no da
        # para adulto (EPA+DHA, linolénico, araquidónico) y el ratio Ca:P.
        return mn
    # ⚠️ SOLO SE ESCALA HACIA ARRIBA, Y ESTA ES LA DECISION QUE HAY QUE
    # ENTENDER ANTES DE TOCARLA.
    #
    # La ecuacion de FEDIAF va en los dos sentidos: si el perro come MAS,
    # el minimo por 1000 kcal BAJA. Aplicada tal cual, un adulto normal
    # (DER 110) pasaria de 52,10 g de proteina a 45,00 -- un 14% menos --,
    # y un perro de trabajo (DER 175) tambien, porque el suelo publicado es
    # la columna de 110. Medido: de ocho perfiles reales, CINCO bajarian.
    #
    # Nuestra tabla es la columna de 95 de FEDIAF, o sea que hoy somos mas
    # estrictos que la guia para el perro activo. Alinearse hacia abajo es
    # RELAJAR NUTRICION, y la regla 3 del CLAUDE.md dice que lo que se
    # relaja es la FORMA, nunca la nutricion. Ser mas estricto que FEDIAF
    # esta siempre permitido; ser menos, no lo decide un refactor.
    #
    # Asi que el minimo publicado que ya usabamos es el SUELO y el escalado
    # solo puede subir por encima. Con eso:
    #   · el perro normal no cambia nada -- cero regresion
    #   · el perro a dieta sube, que es el agujero que habia que tapar
    # Si algun dia se decide adoptar la columna de 110 para el perro
    # activo, es una decision de nutricion aparte y con su medicion.
    d = float(der_efectiva)
    if d >= DER_ANCLA_BAJA:
        return mn                        # el publicado de siempre, sin tocar
    # Por debajo de 95 no hay nada publicado: se coge el MAYOR de los dos
    # anclajes escalados, porque las dos columnas de FEDIAF no son
    # consistentes entre si y ninguna domina a la otra.
    return max(mn, mn * DER_ANCLA_BAJA / d, v110 * DER_ANCLA_ALTA / d)


def der_efectiva_de(der, peso_referencia_kg):
    """Las kcal de la ración por kg de peso metabólico. Es lo que dispara
    el escalado de los mínimos, y tiene que salir de las kcal que DE VERDAD
    se sirven -- no de la etapa vital ni del ajuste teórico. Si saliera de
    la etapa, una dieta de adelgazamiento no se enteraría y el escalado no
    arreglaría nada, que es justo el caso para el que existe."""
    try:
        p = float(peso_referencia_kg)
        d = float(der)
    except (TypeError, ValueError):
        return None
    if p <= 0 or d <= 0:
        return None
    return d / (p ** 0.75)


def verificar(menu, alimentos, req, der, etapa="Adulto", peso_referencia_kg=None):
    """
    Paso 4. Devuelve la ficha honesta de la racion.

    A diferencia del LP, esto NUNCA falla: siempre dice que hay y que falta.
    Los requisitos de FEDIAF van POR 1000 kcal, asi que se escalan al DER.
    """
    etapa = EQUIVALENCIA.get(etapa, etapa)
    if etapa not in SUFIJO:
        raise ValueError(
            f"Etapa '{etapa}' no valida. Usa: {sorted(SUFIJO)} "
            f"(o una equivalente: {sorted(EQUIVALENCIA)}). "
            f"Cuidado: las claves de der.py (adulto, cachorro_crecimiento...) "
            f"NO son las mismas que las de los requisitos.")
    perfil = perfil_nutricional(menu, alimentos)
    # ⚠️ EL MISMO MENU SE MIDE DOS VECES, Y A PROPOSITO (27 agosto).
    # `perfil` usa los valores DECLARADOS y sirve para los MAXIMOS.
    # `perfil_min` sustituye los valores marcados como dudosos por su
    # `valor_plausible` y sirve para los MINIMOS.
    # El motivo, en una linea: un valor inflado protege contra el techo y
    # desprotege contra el suelo, asi que no se puede usar el mismo para
    # las dos cosas. Es el argumento de las cotas aplicado a un valor que
    # si esta pero no nos creemos. El caso que lo provoco: el polvo de
    # sangre declara 80 mg de cobre/100 g y la sangre desecada ronda 0,5;
    # forzandolo en un perro de 25 kg el menu declaraba 8,31 mg de cobre y
    # con el valor plausible se quedaba en 2,34 sobre un minimo de 2,60 --
    # por debajo, y el semaforo en verde.
    # Si ningun alimento del menu trae `valor_plausible`, los dos perfiles
    # son identicos y esto no cambia absolutamente nada.
    perfil_min = perfil_nutricional(menu, alimentos, conservador=True)
    escala = der / 1000.0

    # Si quien llama no manda el peso, no se escala nada y todo queda
    # exactamente como estaba. El escalado es aditivo, nunca una sorpresa.
    _der_ef = der_efectiva_de(der, peso_referencia_kg)

    faltan, se_pasa, correctos = [], [], []
    for nombre, clave in MAPA.items():
        r = req.get(nombre)
        if not r:
            continue
        tiene = perfil.get(clave, 0.0)
        tiene_min = perfil_min.get(clave, 0.0)     # con los dudosos a su valor plausible
        minimo = minimo_de(r, nombre, etapa, _der_ef)
        maximo = maximo_de(r, nombre, etapa)

        if minimo is not None:
            objetivo = minimo * escala
            tiene = tiene_min
            # tolerancia de redondeo: los gramos se redondean a 1 decimal, y
            # eso puede dejar un nutriente al 99.7%. Decirle al usuario que
            # "falta" algo que esta al 99.7% es ruido, no informacion.
            if tiene < objetivo * 0.995:
                faltan.append({"nutriente": nombre, "clave": clave,
                               "tiene": round(tiene, 2), "necesita": round(objetivo, 2),
                               "cubre_pct": round(tiene / objetivo * 100) if objetivo else 0,
                               "falta": round(objetivo - tiene, 2)})
                continue
            tiene = perfil.get(clave, 0.0)         # para el maximo, el declarado
        if maximo is not None and tiene > maximo * escala * 1.001:
            se_pasa.append({"nutriente": nombre, "clave": clave,
                            "tiene": round(tiene, 2), "maximo": round(maximo * escala, 2),
                            "veces": round(tiene / (maximo * escala), 2)})
            continue
        correctos.append(nombre)

    # ==================================================================
    # RATIO CALCIO:FOSFORO -- se comprueba APARTE, no como un nutriente mas
    # ==================================================================
    # Es de lo mas importante de toda la racion y no es un nutriente: es una
    # RELACION. Se puede tener el calcio bien y el fosforo bien por separado
    # y aun asi tener el ratio mal, porque lo que importa es como se absorben
    # el uno respecto al otro.
    #
    # FEDIAF (esta en requerimientos_v2_final.json como "Relacion_Ca_P"):
    #    adulto              1.0 : 1  a  2.0 : 1
    #    cachorro joven      1.0 : 1  a  1.6 : 1   <- mas estricto
    #    cachorro crecimiento 1.0 : 1 a  1.8 : 1
    # El margen es mas estrecho en cachorros porque un ratio malo durante el
    # crecimiento deforma el hueso, y eso no se recupera.
    #
    # ⚠️ Un ratio INVERTIDO (mas fosforo que calcio, <1) es el que causa el
    # hiperparatiroidismo nutricional secundario: el cuerpo saca calcio del
    # hueso para compensar. Es el clasico de las dietas de solo carne.
    r_cap = req.get("Relacion_Ca_P")
    ratio = None
    ca, p = perfil.get("calcio", 0.0), perfil.get("fosforo", 0.0)
    if r_cap and p > 0:
        ratio = ca / p
        mn = _num(r_cap.get(f"min{etapa}")) or _num(r_cap.get("minAdulto"))
        mx = _num(r_cap.get(f"max{etapa}")) or _num(r_cap.get("maxAdulto"))
        if mn is not None and ratio < mn * 0.995:
            faltan.append({
                "nutriente": "Relación Ca:P", "clave": "_ratio_cap",
                "tiene": round(ratio, 2), "necesita": mn,
                "cubre_pct": round(ratio / mn * 100),
                "falta": 0.0,   # no se arregla con suplemento, sino con hueso
                "critico": True,
                "explicacion": (f"Hay más fósforo del que debería para el calcio que lleva "
                                f"({ratio:.2f}:1, y el mínimo es {mn}:1). Un ratio invertido "
                                f"hace que el cuerpo saque calcio del hueso. Se arregla con "
                                f"MÁS HUESO CARNOSO, no con suplementos.")})
        elif mx is not None and ratio > mx * 1.005:
            se_pasa.append({
                "nutriente": "Relación Ca:P", "clave": "_ratio_cap",
                "tiene": round(ratio, 2), "maximo": mx,
                "veces": round(ratio / mx, 2), "critico": True,
                "explicacion": (f"Demasiado calcio para el fósforo que lleva ({ratio:.2f}:1, "
                                f"y el máximo es {mx}:1). El exceso de calcio bloquea la "
                                f"absorción de zinc, hierro y cobre, y en cachorros de raza "
                                f"grande favorece problemas de crecimiento. Se arregla con "
                                f"MENOS HUESO CARNOSO.")})
        else:
            correctos.append("Relación Ca:P")

    # ==================================================================
    # SEMAFORO -- no todos los huecos son iguales de graves
    # ==================================================================
    # Decir "27 de 29" esconde la diferencia entre un nutriente al 94% y
    # otro al 40%, y esa diferencia lo es todo:
    #   VERDE  cubre el minimo. Nada que hacer.
    #   AMBAR  85-100%. Los minimos de FEDIAF ya llevan margen de seguridad
    #          incorporado (estan pensados para pienso industrial con
    #          variabilidad de lote), y el perro no vive de un menu sino de
    #          meses. Un 94% un dia no significa nada.
    #   ROJO   por debajo del 85%. Esto SI importa si se mantiene, y es lo
    #          que hay que enseñarle al veterinario.
    # El corte en 85 es criterio de desarrollo, no una cifra de guia.
    UMBRAL_AMBAR = 85
    rojos  = [f for f in faltan if f["cubre_pct"] < UMBRAL_AMBAR]
    ambar  = [f for f in faltan if f["cubre_pct"] >= UMBRAL_AMBAR]
    # pasarse de un maximo es SIEMPRE rojo: los maximos son toxicidad,
    # no recomendacion
    rojos += se_pasa

    if not rojos and not ambar:
        semaforo = "verde"
    elif not rojos:
        semaforo = "ambar"
    else:
        semaforo = "rojo"

    # AVISO DE DATOS INCOMPLETOS
    # Un 0 en nuestro catálogo puede significar dos cosas muy distintas:
    #   · el alimento NO lo tiene (la ternera no tiene EPA: cero real)
    #   · NO LO SABEMOS porque el fabricante no lo declara
    # El segundo caso va marcado en `sin_dato`. Importa por dos motivos:
    #   MÍNIMOS  → contarlo como 0 es CONSERVADOR: como mucho pondremos un
    #              suplemento que no hacía falta. No es peligroso
    #   MÁXIMOS  → contarlo como 0 SÍ es peligroso: podríamos pasarnos de
    #              cobre o de selenio sin enterarnos
    # Por eso se avisa de qué alimentos traen huecos y en qué nutrientes.
    huecos = {}
    for nombre in menu:
        for k in (alimentos.get(nombre, {}).get("sin_dato") or []):
            huecos.setdefault(k, []).append(nombre)

    # AVISO DE DATOS DUDOSOS — la otra mitad del problema
    # `sin_dato` protege los HUECOS. Pero un valor DECLARADO Y ERRÓNEO no
    # dejaba rastro en ninguna parte, y es el que hace daño: pasa cualquier
    # validación de formato porque tiene la forma de un dato bueno.
    # ⚠️ CASO REAL ENCONTRADO (27 agosto), tres a la vez y los tres de
    # etiquetas reales: el omega-3 TOTAL de cuatro aceites de salmón metido
    # en la columna `linolenico` (que es solo el ALA, así que el EPA y el DHA
    # se contaban dos veces); el fósforo de las dos harinas de hueso, que da
    # un Ca:P de 1,28 cuando la hidroxiapatita da 2,15 por estequiometría; y
    # el cobre del polvo de sangre, 150 veces por encima de lo que tiene la
    # sangre desecada. Ninguno de los tres lo habría visto `sin_dato`.
    # Los dos primeros se arreglaron. Los que NO se pueden arreglar —porque
    # el valor es el de la etiqueta y el real no está publicado— se marcan
    # aquí, en `dato_dudoso`, y salen junto al menú.
    dudosos = {}
    for nombre in menu:
        for k, motivo in (alimentos.get(nombre, {}).get("dato_dudoso") or {}).items():
            dudosos.setdefault(k, []).append(nombre)

    return {
        "datos_incompletos": huecos,
        "datos_dudosos": dudosos,
        "semaforo": semaforo,
        "n_rojos": len(rojos), "n_ambar": len(ambar),
        "rojos": rojos, "ambar": ambar,
        "ratio_ca_p": round(ratio, 2) if ratio else None,
        "correctos": len(correctos),
        "total": len(correctos) + len(faltan) + len(se_pasa),
        "faltan": sorted(faltan, key=lambda x: x["cubre_pct"]),
        "se_pasa": se_pasa,
        "gramos": round(perfil["_gramos"], 1),
        "kcal": round(perfil["_kcal"], 1),
        "densidad_kcal_g": round(perfil["_kcal"] / perfil["_gramos"], 2) if perfil["_gramos"] else 0,
    }


def suplementar(menu, alimentos, req, der, etapa, catalogo_suplementos,
                peso_perro_kg, dosis_maxima_fn):
    """
    Paso 5. Cierra los huecos con suplementos.

    DOS TECHOS, y manda el MAS BAJO de los dos:
      1. la dosis maxima del FABRICANTE (no se puede pasar, y punto)
      2. no superar el MAXIMO FEDIAF de ningun nutriente que ese suplemento
         aporte (el alga sube el yodo, pero el yodo tiene tope)

    Si con el techo no se cierra el hueco, se pone el maximo posible Y SE
    AVISA. El LP en ese caso decia "no factible" y dejaba al usuario sin
    nada, sin explicar por que.
    """
    menu = dict(menu)
    avisos, puestos = [], []
    # La regla de "no dos de la misma categoria" solo vale para PRODUCTOS
    # COMERCIALES: dar dos aceites de salmon de marcas distintas es absurdo.
    # Pero "Extras" no es una marca, es una categoria amplia (aceites,
    # semillas, huevos): pipa de girasol + pipa de calabaza es perfectamente
    # normal, y bloquearlo dejaba el magnesio al 88% pudiendo cerrarlo (la
    # calabaza tiene 592 mg/100g frente a los 390 del girasol).
    COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                   "Calcio", "Hierro", "Vitamina B")
    # los maximos, calculados una vez
    topes_max = {}
    _et = EQUIVALENCIA.get(etapa, etapa)
    for _nom, _cl in MAPA.items():
        _r = req.get(_nom)
        if not _r:
            continue
        _mx = maximo_de(_r, _nom, _et)
        if _mx is not None:
            topes_max[_cl] = _mx * der / 1000.0

    catalogo_cats = {alimentos[n].get("categoria") for n in catalogo_suplementos
                     if n in alimentos and alimentos[n].get("categoria") in COMERCIALES}

    # Se recorren TODOS los huecos, no solo el primero. Antes el bucle se
    # rendia en cuanto uno no se podia cerrar y dejaba los demas sin tocar.
    # Se apunta la pareja (nutriente, suplemento), NO solo el nutriente.
    # Antes, tras probar el magnesio una vez se marcaba como "ya intentado" y
    # NUNCA se reintentaba con otro alimento: cogia pipa de girasol (390 mg),
    # se quedaba al 88%, y no llegaba a probar la de calabaza (592 mg) que lo
    # habria cerrado. Ahora puede reintentar el mismo hueco con otra fuente.
    intentados = set()
    for _ in range(24):
        ficha = verificar(menu, alimentos, req, der, etapa)
        pendientes = [h for h in ficha["faltan"]
                      if not any(k == h["clave"] for k, _s in intentados)
                      or h["clave"] in {k for k, _s in intentados}]
        pendientes = [h for h in ficha["faltan"]]
        if not pendientes:
            break
        hueco = pendientes[0]                # el mas grave que quede
        clave, falta = hueco["clave"], hueco["falta"]

        # ELEGIR EL SUPLEMENTO QUE TAPE MAS HUECOS A LA VEZ.
        #
        # Antes se cogia "el que mas aporta de ESE nutriente", y eso
        # fragmentaba la racion: cuatro huecos = cuatro suplementos
        # distintos, menus de 14-16 alimentos. Un multivitaminico tapa
        # manganeso, zinc, vitamina E y vitaminas B de una vez, pero nunca
        # salia elegido porque para cada nutriente suelto habia algo mas
        # concentrado.
        # Ahora se puntua por CUANTOS de los huecos pendientes cubre cada
        # suplemento, y solo se desempata por potencia. No es una regla
        # nueva: es elegir mejor.
        huecos_ahora = {h["clave"]: h["falta"] for h in ficha["faltan"]}
        mejor, mejor_puntos, mejor_aporte = None, -1, 0.0
        # NO METER DOS SUPLEMENTOS DE LA MISMA CATEGORIA. Salia una racion
        # con "AniForte Aceite de Salmon" Y "Oleum Canis Aceite de Salmon":
        # el mismo producto de dos marcas. Nadie hace eso. Si ya hay uno de
        # esa categoria, lo que toca es subirle la dosis (hasta su techo),
        # no anadir otro.
        cats_ya = {alimentos[n].get("categoria") for n in menu
                   if n in alimentos and alimentos[n].get("categoria") in catalogo_cats}

        for nombre in catalogo_suplementos:
            a = alimentos.get(nombre)
            if not a:
                continue
            # Si YA esta en el menu, no se descarta: se le puede SUBIR la
            # dosis hasta su techo. Antes se saltaba, y por eso el magnesio
            # se quedaba al 88% teniendo el alga (800 mg/100g) ya dentro:
            # estaba puesta para el yodo, en dosis pequeña, y nadie subia.
            if nombre not in menu and a.get("categoria") in cats_ya:
                continue
            # si esta fuente ya se probo para ESTE hueco y no lo cerro, no
            # volver a elegirla: hay que dar paso a la siguiente
            if (clave, nombre) in intentados:
                continue
            # NO USAR FUENTES CON DATO NO FIABLE si hay alternativa.
            # El kelp declara 109.900 ug de yodo/100 g, pero el yodo del alga
            # varia hasta 100 veces (Aakre 2021) y las etiquetas no coinciden
            # con el contenido real. Calcular 0,12 g con dos decimales sobre
            # ese dato es precision falsa.
            if a.get("dato_no_fiable"):
                continue
            nut = a.get("nutrientes", {})
            aporte = valor_nutriente(nut, clave)
            if aporte <= 0:
                continue
            # CUANTOS HUECOS PUEDE CERRAR DE VERDAD, no cuantos toca.
            #
            # Contar "cuantos toca" elegia el aceite de salmon para el
            # linoleico: toca EPA, DHA, vitamina E y linoleico, asi que
            # puntuaba altisimo. Pero tiene 16 g de linoleico/100g, asi que
            # harian falta 29 g = el 21% de las calorias del dia, y no cabe.
            # El aceite de girasol tiene 57.5 g/100g: bastan 8 g = el 6%.
            # Toca menos huecos pero CIERRA el que importa.
            techo_est = dosis_maxima_fn(a, peso_perro_kg)
            if techo_est is None:
                techo_est = (sum(menu.values()) or 1.0) * 0.03
            # ⚠️ EL TECHO REAL NO ES SOLO EL DEL FABRICANTE: tambien lo limita
            # no pasarse de ningun maximo FEDIAF. Sin esto se elegia NEKTON
            # para el yodo (3.100 ug/100g) sobre el yoduro potasico (80.000),
            # porque NEKTON "toca" mas huecos — pero su calcio lo dejaba en
            # 0,9 g y el yodo se quedaba al 11%. Un suplemento que no cabe no
            # sirve, por muchos huecos que toque.
            perfil_ahora = perfil_nutricional(menu, alimentos)
            for cl_mx, mx_val in topes_max.items():
                aporta_mx = valor_nutriente(nut, cl_mx)
                if not aporta_mx or not mx_val:
                    continue
                margen_mx = mx_val - perfil_ahora.get(cl_mx, 0.0)
                if margen_mx <= 0:
                    techo_est = 0.0
                    break
                techo_est = min(techo_est, margen_mx / (aporta_mx / 100.0))
            if techo_est <= 0:
                continue
            puntos = 0
            for cl, falta_cl in huecos_ahora.items():
                aporta_cl = valor_nutriente(nut, cl)
                if aporta_cl <= 0:
                    continue
                # ¿le da para cerrar ese hueco sin pasarse de su propio techo?
                if aporta_cl / 100.0 * techo_est >= falta_cl * 0.999:
                    puntos += 2          # lo cierra entero
                else:
                    puntos += 1          # ayuda pero no llega
            if (puntos, aporte) > (mejor_puntos, mejor_aporte):
                mejor, mejor_puntos, mejor_aporte = nombre, puntos, aporte
        if not mejor:
            avisos.append(f"No hay ningún suplemento disponible que aporte {hueco['nutriente']}.")
            intentados.add((hueco["clave"], None))
            if all((h["clave"], None) in intentados for h in ficha["faltan"]):
                break
            continue
        if (hueco["clave"], mejor) in intentados:
            # esta fuente ya se probo para este hueco y no lo cerro
            intentados.add((hueco["clave"], None))
            if all(any((h["clave"], s) in intentados for s in [None] + catalogo_suplementos)
                   for h in ficha["faltan"]):
                break
            continue
        intentados.add((hueco["clave"], mejor))

        # MARGEN DEL 4%: al anadir un suplemento la racion se pasa de kcal y
        # luego hay que reescalar la comida hacia abajo, y eso tira el
        # nutriente JUSTO por debajo del minimo. Se veia clarisimo: yodo 98%,
        # hierro 99%, linoleico 98%... todo a un pelo. Apuntando un 4% por
        # encima, el reescalado ya no lo saca de rango.
        # No es pasarse: los DOS TECHOS (fabricante y maximo FEDIAF) siguen
        # mandando, asi que este margen solo se aplica si cabe.
        gramos_necesarios = falta * 1.04 / (mejor_aporte / 100.0)

        # TECHO 1: fabricante
        techo = dosis_maxima_fn(alimentos[mejor], peso_perro_kg)
        if techo is None:
            # Sin dosis de fabricante (aceites, semillas, alimentos sueltos)
            # NO puede quedarse sin techo. Paso real: un Gran Danes lactante
            # acabo con 13.800 g de aceite de oliva y 132.628 kcal porque
            # aqui no habia limite. Se topa al 3% del peso de la racion, que
            # para un aceite ya es mucho.
            peso_actual = sum(menu.values()) or 1.0
            techo = peso_actual * 0.03

        # TECHO 2: no pasarse de ningun maximo FEDIAF POR SU CULPA.
        #
        # ⚠️ SOLO cuenta si el suplemento APORTA ese nutriente. Antes, si algo
        # ya venia pasado de la comida base (el menu de conejo salia con el
        # calcio al 170% del maximo por la carcasa), el techo se ponia a cero
        # y NO SE ANADIA NINGUN SUPLEMENTO — ni siquiera el yoduro potasico,
        # que solo lleva yodo y no tocaba el calcio para nada.
        # El exceso de calcio hay que arreglarlo bajando el hueso, no
        # castigando a un suplemento que no tiene nada que ver.
        for nom_req, cl in MAPA.items():
            r = req.get(nom_req)
            if not r:
                continue
            mx = maximo_de(r, nom_req, etapa)
            aporta = valor_nutriente(alimentos[mejor].get("nutrientes", {}), cl)
            if mx is None or not aporta:
                continue
            actual = perfil_nutricional(menu, alimentos).get(cl, 0.0)
            margen = mx * der / 1000.0 - actual
            if margen <= 0:
                techo = 0.0
                break   # este suplemento no cabe: ya hay algo al limite
            techo = min(techo, margen / (aporta / 100.0))

        ya_puesto = menu.get(mejor, 0.0)
        gramos = round(min(gramos_necesarios + ya_puesto, techo), 2)
        if gramos <= ya_puesto + 0.01:
            avisos.append(
                f"{hueco['nutriente']} se queda al {hueco['cubre_pct']}%. No se puede "
                f"subir más sin pasarse de un máximo de seguridad. Coméntalo con tu veterinario.")
            continue

        menu[mejor] = gramos
        puestos = [p for p in puestos if p["suplemento"] != mejor]
        puestos.append({"suplemento": mejor, "gramos": gramos,
                        "para": hueco["nutriente"],
                        "alcanza": gramos >= gramos_necesarios * 0.999})
        if gramos < gramos_necesarios * 0.999:
            avisos.append(
                f"{hueco['nutriente']}: se ha puesto la dosis máxima de {mejor} "
                f"({gramos} g) pero aún se queda corto. Coméntalo con tu veterinario.")

    return menu, puestos, avisos


def ajustar_excesos(menu, alimentos, req, der, etapa, protegidos=None):
    """
    Paso 6. Si algo se pasa de un maximo de seguridad, se baja el alimento
    que mas lo aporta y se recompensa la energia con el resto, para no
    perder kcal.

    Los 5 pilares estan PROTEGIDOS: se reducen, nunca se eliminan. Que
    desaparezca una categoria entera por un exceso del 6% seria peor que
    el exceso.
    """
    protegidos = protegidos or set()
    menu = dict(menu)
    notas = []

    for _ in range(5):
        ficha = verificar(menu, alimentos, req, der, etapa)
        if not ficha["se_pasa"]:
            break
        exceso = ficha["se_pasa"][0]
        clave, veces = exceso["clave"], exceso["veces"]

        # quien lo aporta mas, en valor absoluto
        culpable, aporte_max = None, 0.0
        for nombre, gramos in menu.items():
            v = valor_nutriente(alimentos.get(nombre, {}).get("nutrientes", {}), clave)
            if v and v * gramos > aporte_max:
                culpable, aporte_max = nombre, v * gramos
        if not culpable:
            break

        # bajarlo lo justo, con suelo del 25% para no hacerlo desaparecer
        # se baja de golpe a lo justo (con un 3% de margen) en vez de ir
        # acercandose poco a poco, que repetia el mismo aviso 5 veces
        factor = max(1.0 / veces * 0.97, 0.25)
        nuevo = round(menu[culpable] * factor, 1)
        if nuevo >= menu[culpable] - 0.05:
            break
        quitado_kcal = (menu[culpable] - nuevo) * alimentos[culpable]["energia"] / 100.0
        menu[culpable] = nuevo
        notas = [x for x in notas if not x.startswith(f"Se ha bajado {culpable} ")]
        notas.append(f"Se ha bajado {culpable} a {nuevo} g porque el "
                     f"{exceso['nutriente'].lower()} se pasaba del máximo.")

        # devolver las kcal perdidas al resto de la racion, proporcionalmente
        resto = {n: g for n, g in menu.items() if n != culpable
                 and alimentos.get(n, {}).get("categoria") in
                 ("Carne muscular", "Hueso carnoso", "Pescados y mariscos")}
        kcal_resto = sum(alimentos[n]["energia"] * g / 100.0 for n, g in resto.items())
        if kcal_resto > 0:
            f = 1 + quitado_kcal / kcal_resto
            for n in resto:
                menu[n] = round(menu[n] * f, 1)

    return menu, notas


def limitar_extras(menu, alimentos, der, tope_kcal=0.12):
    """
    Los EXTRAS (aceites, semillas, huevos, yogur) se topan POR ENERGIA.

    Un aceite tiene 888 kcal/100 g: 63 g son el 37% de las calorias del dia.
    El tope clasico del BARF ("extras <= 5% del peso") no significa nada
    porque ese mismo 5% son el 37% de las kcal si es aceite y el 6% si es
    huevo. Lo que hay que limitar es cuanta ENERGIA aportan, no cuanto pesan.

    Si se pasan, se bajan proporcionalmente y las kcal que faltan las asume
    la comida de verdad (carne, hueso, pescado).
    """
    extras = {n: g for n, g in menu.items()
              if alimentos.get(n, {}).get("categoria") == "Extras"}
    if not extras:
        return menu, None
    kcal_extras = sum(alimentos[n]["energia"] * g / 100.0 for n, g in extras.items())
    limite = der * tope_kcal
    if kcal_extras <= limite:
        return menu, None

    factor = limite / kcal_extras
    salida = dict(menu)
    for n in extras:
        salida[n] = round(extras[n] * factor, 1)
    sobra = kcal_extras - limite

    # devolver esas kcal a la comida base
    base = {n: g for n, g in salida.items()
            if alimentos.get(n, {}).get("categoria") in
            ("Carne muscular", "Hueso carnoso", "Pescados y mariscos")}
    kcal_base = sum(alimentos[n]["energia"] * g / 100.0 for n, g in base.items())
    if kcal_base > 0:
        f = 1 + sobra / kcal_base
        for n in base:
            salida[n] = round(salida[n] * f, 1)
    return salida, (f"Los extras (aceites, semillas, huevo) aportaban el "
                    f"{kcal_extras/der*100:.0f}% de las calorías del día. Se han "
                    f"bajado al {tope_kcal*100:.0f}%: son muy energéticos y "
                    f"desplazan comida con nutrientes.")
