# -*- coding: utf-8 -*-
"""La prescripción del veterinario: el único sitio que puede bajar de FEDIAF.

⚠️ POR QUÉ EXISTE, Y POR QUÉ NO ROMPE LA REGLA 1 (17 de septiembre de 2026).

Elena, y tiene razón clínica:

> «si pide mucha menos proteína de la que necesita un perro sano es
> indiferente, porque NO ES UN PERRO SANO y es una patología que tiene
> necesidades diferentes. Simplemente el veterinario tiene que saber todo.»

Los mínimos de la Tabla III-3b de FEDIAF son los de un perro SANO. Ocho
patologías del motor piden, por su propia fuente, bajar de ahí:

    hepatopatia              cobre     1,2 mg   (mínimo FEDIAF 2,08)
    renal_avanzada           proteína  42,5 g   (mínimo FEDIAF 52,1)
    shunt_sin_encefalopatia  proteína  43,75 g
    encefalopatia_hepatica   proteína  31,25 g
    urolitos_silice          proteína  35,0 g
    renal                    fósforo   1000 mg  (mínimo FEDIAF 1160)
    urato                    purinas   90
    cistina                  metionina+cistina

Hasta hoy el motor se paraba en el mínimo de FEDIAF y lo decía. Eso es
correcto **para un dueño** y es exactamente lo contrario de lo que necesita
quien firma: un veterinario colegiado es la persona que sí puede pautar por
debajo, y si la app no se lo deja, lo hará en una hoja de cálculo donde no
lo verifica nadie.

⚠️ **LA REGLA 1 NO DICE «TODO MENÚ CUMPLE FEDIAF». DICE «NINGÚN MENÚ SALE
SIN VERIFICAR».** Es la distinción que sostiene todo esto, y está escrita
desde el 28 de agosto en `VETERINARIOS.md` §10: un menú prescrito se
verifica de cero y entero, igual que cualquier otro. Lo que cambia no es SI
se comprueba: es CONTRA QUÉ. Y ese «contra qué» viaja con el menú, se enseña
y se guarda.

Lo que una prescripción PUEDE y NO PUEDE hacer, literal de aquel documento:

  · **Puede bajar un mínimo de FEDIAF** para un nutriente NOMBRADO.
  · **Puede apretar un máximo** por debajo del tope de patología.
  · **No puede aflojar ningún máximo** por encima de FEDIAF.
  · **No puede tocar los cinco topes de seguridad crónica.** Ni uno.
  · El semáforo **nunca dice «verde» a secas**: dice «verde con
    excepciones», y las lista.

⚠️ Y LA CUARTA NO ES SIMETRÍA CON LA PRIMERA, aunque lo parezca. Un mínimo
de FEDIAF es «esto le hace falta a un perro sano», y una patología puede
cambiar esa premisa. Los cinco topes crónicos —vitamina D, yodo, selenio,
mercurio, tiaminasa— son toxicidad acumulada: no dependen de si el perro
está sano, y ninguna patología los vuelve inofensivos. Por eso el primero
cede ante una firma y el segundo no.
"""

# Los topes crónicos que un nutriente PUEDE nombrar. Son tres y no cinco, y
# eso no es un olvido: el mercurio y la tiaminasa no son nutrientes del
# `MAPA` sino fracciones de las kcal del menú (qué parte del plato es
# pescado con mercurio), así que no hay ninguna clave con la que pedirlos y
# no hace falta prohibirlos aquí. Los tres que sí se pueden nombrar se
# RECHAZAN, y la prescripción entera con ellos: no se recorta en silencio,
# porque quien la escribió tiene que enterarse de que eso no se puede pedir.
CRONICOS_INTOCABLES = ("vitD", "yodo", "selenio")

# Lo que hace falta para que un papel sea una prescripción y no un número
# suelto. Sin esto no se aplica: lo que distingue a una prescripción de un
# objetivo del profesional es precisamente que alguien la FIRMA.
CAMPOS_DE_LA_FIRMA = ("motivo", "firmada_por", "colegiado", "fecha")


class PrescripcionInvalida(ValueError):
    """La prescripción pide algo que no se puede pedir, y se dice cuál."""


def normalizar(prescripcion):
    """Valida la prescripción y la deja en la forma que lee el motor.

    Devuelve `(limites, firma)` donde `limites` es
    `{clave_de_nutriente: {"min": x|None, "max": y|None}}`, o `(None, None)`
    si no hay prescripción.

    ⚠️ FALLA RUIDOSO, no recortando. Un objetivo del profesional que se pasa
    se RECORTA y se dice (`_objetivos_dentro_de_fediaf`), porque ahí el
    profesional está apretando y pasarse es un descuido. Aquí es al revés:
    quien prescribe está levantando un suelo a propósito, así que si pide
    algo que el motor no puede conceder —aflojar un máximo, tocar un tope
    crónico— devolverle un menú recortado sería dejarle firmar algo que no
    es lo que escribió.
    """
    if not prescripcion:
        return None, None
    if not isinstance(prescripcion, dict):
        raise PrescripcionInvalida(
            "La prescripción tiene que ser un objeto con el nutriente, su cifra y la firma.")

    firma = {c: prescripcion.get(c) for c in CAMPOS_DE_LA_FIRMA}
    faltan = [c for c in CAMPOS_DE_LA_FIRMA if not firma.get(c)]
    if faltan:
        raise PrescripcionInvalida(
            "Una prescripción se firma: falta " + ", ".join(faltan) + ". "
            "Sin eso es un número suelto, y un número suelto no levanta un mínimo de FEDIAF.")

    limites = {}
    for clave, valor in prescripcion.items():
        if clave in CAMPOS_DE_LA_FIRMA:
            continue
        if not isinstance(valor, dict):
            raise PrescripcionInvalida(
                f"«{clave}» tiene que traer «min» y/o «max», no un número suelto: "
                f"sin decir cuál de los dos se levanta, el motor no sabe qué hacer con él.")
        if clave in CRONICOS_INTOCABLES:
            raise PrescripcionInvalida(
                f"«{clave}» es uno de los cinco topes de seguridad crónica y no se puede "
                f"prescribir. Un mínimo de FEDIAF dice lo que le hace falta a un perro SANO, "
                f"y una patología puede cambiar esa premisa; un tope crónico es toxicidad "
                f"acumulada y no depende de que el perro esté sano.")
        mn = valor.get("min")
        mx = valor.get("max")
        if mn is None and mx is None:
            raise PrescripcionInvalida(
                f"«{clave}» no dice ni «min» ni «max»: no pide nada.")
        if mn is not None and mx is not None and float(mn) > float(mx):
            raise PrescripcionInvalida(
                f"«{clave}» pide un mínimo ({mn}) por encima de su máximo ({mx}).")
        limites[clave] = {"min": None if mn is None else float(mn),
                          "max": None if mx is None else float(mx)}
    if not limites:
        raise PrescripcionInvalida(
            "La prescripción va firmada y no nombra ningún nutriente.")
    return limites, firma


def limite_prescrito(prescripcion_normalizada, clave, cual):
    """La cifra que la prescripción pone a este nutriente, o None.

    `cual` es «min» o «max». Se lee por CLAVE de nutriente (la del catálogo y
    la del `MAPA`), no por el nombre del requisito, por lo mismo que todo lo
    demás del motor: el nombre es de presentación y la clave es la que indexa.
    """
    if not prescripcion_normalizada:
        return None
    fila = prescripcion_normalizada.get(clave)
    if not fila:
        return None
    return fila.get(cual)


def requisitos_del_paciente(req, etapa, patologias=None, prescripcion=None,
                            der_efectiva=None, es_profesional=False):
    """LOS REQUISITOS CONTRA LOS QUE SE MIDE ESTE PERRO. Una sola función.

    Devuelve un diccionario con:

        minimos      {nombre_req: cifra}   ya con la prescripción aplicada
        maximos      {nombre_req: cifra}   ya apretados por la prescripción
        topes        {clave: cifra}        los de las patologías marcadas
        suelos       {clave: cifra}        los de las patologías marcadas
        excepciones  [ ... ]               lo que NO cumple a un perro sano
        firma        {motivo, colegiado…}  quién responde de esas excepciones

    ⚠️ ES UNA Y NO TRES, Y ESO NO ES ESTILO. `VETERINARIOS.md` §10 lo dice con
    el caso delante: «el solver, `_tope_patologia_roto()` y
    `_garantizar_verificado()` tienen que llamar los tres a esta función, o el
    menú se construirá contra unos números y se comprobará contra otros». En
    este repo eso ya ha pasado DOS veces —el analizador y el semáforo con la
    fibra, y la tabla de patologías duplicada del motor anterior al MILP, con
    el fósforo renal a 1400 en un lado y a 1200 en el otro—.

    ⚠️ Y `excepciones` ES LA MITAD QUE IMPORTA. Un menú prescrito no cumple los
    requisitos de un perro sano **a propósito**, así que lo que hay que poder
    enseñar y guardar no es «verde»: es contra qué se ha medido y en qué se
    aparta. Sin esa lista, un menú con la proteína a 42,5 sería
    indistinguible de uno que la cumple.
    """
    from verificar import MAPA, minimo_de, maximo_de

    limites, firma = normalizar(prescripcion)
    if limites and not es_profesional:
        raise PrescripcionInvalida(
            "Una prescripción solo la aplica una cuenta de veterinario con el rol verificado. "
            "Sin eso, «bajar un mínimo de FEDIAF» lo pediría cualquiera desde una terminal.")

    # ⚠️ LAS DOS FORMAS, porque el repo tiene las dos vivas: `cargar_v2()`
    #    devuelve la tabla YA indexada por nombre de nutriente, y el fichero en
    #    disco es una LISTA de filas. Suponer una sola es lo que hizo que esta
    #    función devolviera un diccionario vacío sin dar ningún error -- que es
    #    la peor forma de fallar: los mínimos salen «sin requisito» y todo
    #    cuadra.
    if isinstance(req, dict):
        filas = req
    else:
        filas = {r.get("nutriente"): r for r in (req or []) if isinstance(r, dict)}
    minimos, maximos, excepciones = {}, {}, []
    if not filas:
        raise PrescripcionInvalida(
            "No llega la tabla de requisitos de FEDIAF, así que no hay contra qué medir. "
            "Esto no se puede resolver «sin requisitos»: sería entregar un menú sin verificar.")
    for nombre, clave in MAPA.items():
        r = filas.get(nombre)
        if not r:
            continue
        mn_sano = minimo_de(r, nombre, etapa, der_efectiva)
        mx_sano = maximo_de(r, nombre, etapa)
        mn = minimo_de(r, nombre, etapa, der_efectiva, prescripcion=limites)
        mx = maximo_de(r, nombre, etapa, prescripcion=limites)
        minimos[nombre] = mn
        maximos[nombre] = mx
        if not limites or clave not in limites:
            continue
        # ⚠️ SE DECLARA LO QUE SE APARTA DEL PERRO SANO, EN LOS DOS SENTIDOS Y
        #    TAMBIÉN CUANDO NO HACE NADA. Un techo prescrito por encima del de
        #    FEDIAF se queda en el de FEDIAF (`min()`), y callarlo dejaría al
        #    veterinario creyendo que firmó un número que el motor ignoró.
        pedido = limites[clave]
        if pedido.get("min") is not None and mn_sano is not None and pedido["min"] < mn_sano:
            excepciones.append({
                "nutriente": nombre, "clave": clave, "sentido": "min",
                "lo_que_pide_fediaf": mn_sano, "lo_que_firma_el_veterinario": pedido["min"],
                "que_pasa": "por_debajo_del_minimo_de_fediaf"})
        if pedido.get("max") is not None and mx_sano is not None and pedido["max"] > mx_sano:
            excepciones.append({
                "nutriente": nombre, "clave": clave, "sentido": "max",
                "lo_que_pide_fediaf": mx_sano, "lo_que_firma_el_veterinario": pedido["max"],
                "que_pasa": "techo_no_aplicado_manda_fediaf"})

    topes, suelos = {}, {}
    if patologias:
        try:
            from motor_completo import topes_de_patologias
            topes, _pct, _av, suelos = topes_de_patologias(list(patologias), etapa)
        except ImportError:
            pass

    return {"minimos": minimos, "maximos": maximos,
            "topes": topes or {}, "suelos": suelos or {},
            "excepciones": excepciones, "firma": firma,
            "limites_prescritos": limites}
