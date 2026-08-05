# -*- coding: utf-8 -*-
"""
PASOS 4 y 5: verificar contra FEDIAF y cerrar huecos con suplementos.

Esta es la parte que legitima la racion. La plantilla es solo el punto de
partida; lo que se puede defender ante un veterinario es ESTO: "cubre 26 de
27 nutrientes, y estos dos se quedan al 80%".
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from constructor import perfil_nutricional

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
    "Linolénico": "linolenico", "EPA_DHA_total": "epa", "Araquidónico": "araquidonico",
}
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


def verificar(menu, alimentos, req, der, etapa="Adulto"):
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
    escala = der / 1000.0

    faltan, se_pasa, correctos = [], [], []
    for nombre, clave in MAPA.items():
        r = req.get(nombre)
        if not r:
            continue
        tiene = perfil.get(clave, 0.0)
        minimo = _num(r.get(f"min{etapa}"))
        maximo = _num(r.get(f"max{etapa}")) or _num(r.get("maxAdulto"))

        if minimo is not None:
            objetivo = minimo * escala
            # tolerancia de redondeo: los gramos se redondean a 1 decimal, y
            # eso puede dejar un nutriente al 99.7%. Decirle al usuario que
            # "falta" algo que esta al 99.7% es ruido, no informacion.
            if tiene < objetivo * 0.995:
                faltan.append({"nutriente": nombre, "clave": clave,
                               "tiene": round(tiene, 2), "necesita": round(objetivo, 2),
                               "cubre_pct": round(tiene / objetivo * 100) if objetivo else 0,
                               "falta": round(objetivo - tiene, 2)})
                continue
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

    return {
        "datos_incompletos": huecos,
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
        _mx = _num(_r.get(f"max{_et}")) or _num(_r.get("maxAdulto"))
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
            aporte = _num(nut.get(clave)) or 0.0
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
                aporta_mx = _num(nut.get(cl_mx))
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
                aporta_cl = _num(nut.get(cl)) or 0.0
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
            mx = _num(r.get(f"max{etapa}")) or _num(r.get("maxAdulto"))
            aporta = _num(alimentos[mejor].get("nutrientes", {}).get(cl))
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
            v = _num(alimentos.get(nombre, {}).get("nutrientes", {}).get(clave))
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
