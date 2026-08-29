# -*- coding: utf-8 -*-
"""
EL MOTOR DE VERDAD — una sola pregunta, no miles de intentos con nombres fijos.

POR QUÉ ESTE ARCHIVO EXISTE
-----------------------------
Toda la noche del 4→5 de agosto se probó: elegir a mano, elegir por
densidad con una sola pasada, comparar unas pocas combinaciones,
enumerar miles de combinaciones con nombres fijos ("menú de pollo",
"menú de pollo y sardina"...). La usuaria lo dijo claro:
    "no pruebes con menú de pollo... que saques menús viables, y si el
     menú es de cordero con pollo, pues cordero con pollo, con lo que
     salga"
Fijar la carne y el hueso de antemano y luego probar variantes alrededor
es la pregunta equivocada. La pregunta correcta es UNA SOLA:
    "de TODOS los alimentos disponibles, ¿cuál es la mejor combinación
     posible — qué alimentos Y cuánto de cada uno — que cumple los 30
     requisitos con máximo 2 suplementos?"

Eso es un problema de PROGRAMACIÓN LINEAL ENTERA MIXTA (MILP): unas
variables son continuas (cuántos gramos) y otras son binarias (¿se usa
este alimento sí/no?), porque hay que LIMITAR CUÁNTOS alimentos distintos
se usan por categoría (máx. 3 carnes, máx. 2 suplementos...), y eso no
se puede expresar solo con gramos.

`scipy.optimize.milp` lo resuelve de forma EXACTA: si existe una
combinación que funciona, la encuentra. Si no existe, lo dice con
certeza matemática, no porque no se haya probado lo suficiente.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from scipy.optimize import milp, LinearConstraint, Bounds
from verificar import (MAPA, _num, EQUIVALENCIA, maximo_de, minimo_de,
                       der_efectiva_de)
from constructor import (valor_nutriente, valor_plausible_de,
                         tabla_imputacion_maximos, valor_para_maximo)

# ⚠️ AÑADIDO (5 agosto, noche): copia local de especie_de() (la misma
# lógica que ya usan especies.py y el frontend) -- se define aquí en
# vez de importarla desde la carpeta raíz, para no depender de cómo
# esté configurado el path de imports en el despliegue real.
def especie_de(nombre: str) -> str:
    if " de " in nombre:
        resto = nombre.split(" de ", 1)[1]
        return resto.split(" ")[0].capitalize()
    return nombre.split(" ")[0]

# ⚠️ LOS TOPES POR PATOLOGÍA YA NO VIVEN AQUÍ (28 agosto). Eran 200 líneas
# de `dict` con cuatro cosas mezcladas: los números, el motivo clínico de
# cada número, los textos que lee el usuario y la lógica de qué pasa en
# crecimiento. Ahora son datos en `patologias.json`, con fuente y motivo
# por cifra, y los audita `auditar_patologias.py` (BLOQUE 32) igual que
# `auditar_fediaf.py` audita la tabla de FEDIAF desde el 25 de agosto.
#
# La forma que ve el solver es EXACTAMENTE la misma: `motor/patologias.py`
# la reconstruye al cargar, así que `topes_de_patologias()`,
# `patologias_bloquean()` y `avisos_de_patologias()` siguen intactas.
# Comprobado al hacer el cambio: la tabla reconstruida es idéntica a la que
# había, patología por patología y clave por clave.
from patologias import PATOLOGIAS, CRUDO as PATOLOGIAS_CRUDO


# ─── QUÉ TOPES APLICAN DE VERDAD, SEGÚN LA ETAPA ─────────────────────────────
#
# ⚠️ AÑADIDO (25 agosto). Antes los topes se leían directos de la tabla y se
# aplicaban igual a un cachorro que a un adulto. Eso está mal en los dos
# sentidos: el tope de fósforo renal (1200) es MENOR que el mínimo que
# FEDIAF exige a un cachorro (1750-2250), y el de grasa en pancreatitis
# (20 g) es MENOR que el mínimo de crecimiento (21,25 g). Aplicados a un
# cachorro no dan un menú más seguro: no dan menú, o lo dan rompiendo el
# mínimo. Por eso cada tope dice ahora en qué etapas vale.
#
# Se usa en DOS sitios -- al construir las restricciones y al verificar el
# menú terminado -- y por eso vive aquí y no dentro de resolver().
def _es_crecimiento(etapa):
    e = EQUIVALENCIA.get(etapa, etapa)
    return e in ("CachorroJoven", "CachorroCrecimiento")


def topes_de_patologias(patologias, etapa="Adulto"):
    """Devuelve (topes_por_1000kcal, pct_kcal_grasa, avisos_extra) ya
    resueltos para esta etapa y esta combinación de patologías."""
    lista = list(patologias or [])
    crece = _es_crecimiento(etapa)
    topes, pct_grasa, avisos = {}, None, []

    for p in lista:
        info = PATOLOGIAS.get(p, {})

        if info.get("solo_en_adulto") and crece:
            # En crecimiento este tope no se aplica. Si además hay que
            # decirlo (no bloquea, solo se relaja), se dice: nunca en
            # silencio.
            if info.get("en_crecimiento") == "sin_tope" and info.get("aviso_crecimiento"):
                avisos.append(info["aviso_crecimiento"])
            continue

        for clave, valor in (info.get("max_por_1000kcal") or {}).items():
            actual = topes.get(clave)
            topes[clave] = valor if actual is None else min(actual, valor)

        v = info.get("max_pct_kcal_grasa")
        if v is not None:
            pct_grasa = v if pct_grasa is None else min(pct_grasa, v)

        # Topes que solo aplican si además hay otra condición marcada.
        condicional = info.get("max_pct_kcal_grasa_si_ademas")
        if condicional:
            valor, requiere = condicional
            if any(otra in lista for otra in requiere):
                pct_grasa = valor if pct_grasa is None else min(pct_grasa, valor)

    return topes, pct_grasa, avisos

FRUTAS = {"Manzana", "Pera", "Plátano", "Fresa", "Sandía", "Melón", "Naranja",
         "Mandarina", "Piña", "Mango", "Frambuesa", "Arándano", "Albaricoque", "Dátil"}


def patologias_bloquean(patologias, etapa="Adulto", es_profesional=False):
    """Las que impiden generar dieta automática.

    ⚠️ EL VETERINARIO NO SE BLOQUEA (29 agosto). Hasta hoy un veterinario
    acreditado veía exactamente las mismas patologías bloqueadas que el
    dueño -- y el motivo de bloquear era, literalmente, «esto lo tiene que
    pautar un veterinario». Cuando el que está delante ES el veterinario,
    el muro deja de tener sentido: lo va a hacer igual, en una hoja de
    cálculo y sin que nadie verifique nada.

    La frontera de verdad ya estaba decidida y escrita en VETERINARIOS.md:
    lo que exige diagnóstico validado es que el motor aplique restricciones
    POR DEBAJO de los mínimos de FEDIAF. Todo lo que cabe DENTRO de FEDIAF
    no necesita firma. Así que al profesional se le formula todo, con el
    aviso de cada patología diciendo QUÉ SE HA HECHO y qué NO -- que en
    cuatro de ellas es «esto no trata la enfermedad, solo alimenta bien».

    ⚠️ AHORA DEPENDE DE LA ETAPA (25 agosto). La insuficiencia renal en un
    perro ADULTO se puede apoyar bajando el fósforo; en un cachorro o una
    perra gestante, no: el fósforo que hay que quitarle es menos del que
    necesita para crecer. Ahí no hay menú que dar, y decirlo es mejor que
    dar uno que no sirve."""
    bloquean = []
    for p in (patologias or []):
        info = PATOLOGIAS.get(p, {})
        if es_profesional and info.get("formulable_por_profesional"):
            continue
        if info.get("sin_dieta_automatica"):
            bloquean.append(p)
        elif info.get("en_crecimiento") == "bloquear" and _es_crecimiento(etapa):
            bloquean.append(p)
    return bloquean


def avisos_de_patologias(patologias, etapa="Adulto", es_profesional=False):
    """⚠️ AL PROFESIONAL SE LE DICE OTRA COSA, Y ES LA IMPORTANTE.

    Al dueño, de una patología bloqueada, se le dice «no generamos menú».
    Al veterinario se le genera -- así que hay que decirle QUÉ SE HA HECHO
    y, sobre todo, QUÉ NO. En cuatro de las once la respuesta honrada es
    «esto no trata la enfermedad, solo alimenta bien», y decirlo importa
    más que el propio menú: un menú de urato que no restringe purinas y no
    lo dice es peor que no dar menú."""
    salida = []
    for p in (patologias or []):
        info = PATOLOGIAS.get(p)
        if not info:
            continue
        if es_profesional:
            if _es_crecimiento(etapa) and info.get("aviso_profesional_crecimiento"):
                salida.append(info["aviso_profesional_crecimiento"]); continue
            if info.get("aviso_profesional"):
                salida.append(info["aviso_profesional"]); continue
        # En crecimiento, NINGÚN tope `solo_en_adulto` se ha aplicado: ni el
        # que bloquea (renal) ni el que se suelta (pancreatitis). El aviso de
        # adulto dice "se ha bajado el fósforo" o "se ha bajado la grasa", y
        # ahí eso es FALSO -- no se ha bajado nada. Hay que dar el de
        # crecimiento, que cuenta lo que ha pasado de verdad.
        #
        # ⚠️ Antes esta condición miraba solo `en_crecimiento == "bloquear"`,
        # así que a un cachorro con pancreatitis le habría tocado el `elif`
        # de abajo: el texto de adulto, afirmando una restricción que no
        # existía. No llegó a verse porque main.py solo llamaba aquí con las
        # patologías que BLOQUEAN -- pero el fallo estaba puesto y esperando
        # a la primera llamada que pasara una que no bloquea.
        if (info.get("solo_en_adulto") and _es_crecimiento(etapa)
                and info.get("aviso_crecimiento")):
            salida.append(info["aviso_crecimiento"])
        elif info.get("aviso"):
            salida.append(info["aviso"])
    return salida


def resolver(der, etapa, alimentos, req, peso_perro_kg, dosis_maxima_fn,
            excluidos=None, margenes_categoria=None, cuantos_max=None,
            max_suplementos=2, tolerancia_kcal=0.03,
            forzar=None, preferir=None, patologias=None, semilla_aleatoria=None,
            time_limit=15, restringir_especie=None, peso_adulto_esperado_kg=None,
            evitar_especies=None, restringir_a_elegidos=None, categorias_excluidas=None,
            presupuesto_semanal_restante=None, diagnostico=None,
            peso_objetivo_kg=None, gramos_fijos=None):
    """
    UNA sola llamada. Decide QUÉ alimentos usar Y cuántos gramos de cada
    uno, de entre TODOS los accesibles, a la vez.

    `forzar`: lista de nombres que SÍ O SÍ tienen que entrar en la ración
    (con gramos > 0). Es el modo PERSONALIZAR: el usuario elige alimentos
    concretos y el motor calcula el resto alrededor de esa elección. Si
    forzar algo hace que no exista solución, se devuelve (False, None) —
    igual que antes, una respuesta exacta, no una aproximación.

    `preferir`: lista de nombres que el motor debe usar CON PREFERENCIA
    sobre otros si hay varias soluciones igual de válidas — no obliga a
    que entren, solo hace que el "coste" de usarlos sea menor. Es el modo
    APROVECHAR: lo que el usuario ya tiene en casa gana la partida frente
    a alimentos que tendría que comprar, PERO SOLO si con eso sigue
    cumpliendo los 30 requisitos — si no llega, el motor añade lo que
    haga falta igualmente, avisando (eso se ve en qué más aparece en la
    ración final).

    `restringir_a_elegidos`: {categoría: [nombres]} — ⚠️ AÑADIDO (5
    agosto, madrugada), PEDIDO EXPRESO: en Personalizar, si el usuario
    elige 1-2 carnes concretas, antes el motor podía añadir OTRA carne
    más sin que hiciera falta, solo porque "le convenía" para cuadrar
    algo. Con esto, la categoría (típicamente Carne muscular, Pescados y
    mariscos, Hueso carnoso) queda restringida a SOLO los nombres dados
    -- ninguna otra especie de esa categoría entra, aunque sí se sigue
    decidiendo libremente CUÁNTOS gramos de cada una. Si con eso no hay
    solución viable, quien llama a resolver() debe reintentar sin esta
    restricción (igual que ya hace forzar cuando no hay solución) --
    aquí solo se aplica el filtro, la lógica de "inténtalo así primero,
    si no se puede afloja" vive en quien llama, no aquí dentro.

    `presupuesto_semanal_restante`: {clave_nutriente: tope_diario_efectivo}
    — ⚠️ AÑADIDO (5 agosto, madrugada), CAMBIO DE ARQUITECTURA PEDIDO
    EXPRESAMENTE: los topes de seguridad crónica (tiaminasa, mercurio,
    vitD, yodo, selenio) tienen un límite SEMANAL real, no solo por
    ración -- pero cada menú de una rotación se genera en una llamada
    aparte, sin memoria de lo que ya "gastaron" los menús anteriores de
    esa misma semana. Quien orquesta la generación de varios menús
    (main.py) calcula, ANTES de pedir este menú, cuánto presupuesto
    semanal queda tras los menús ya generados, lo reparte entre los
    días que faltan, y pasa aquí el tope diario EFECTIVO resultante --
    más estricto que el tope normal por ración. Aquí dentro solo se usa
    ese valor en vez del de por defecto si viene informado (nunca al
    revés: nunca se afloja un tope, solo se puede endurecer). Así, por
    diseño, es matemáticamente imposible que la suma de una semana
    entera supere el límite seguro, sin depender de que nadie revise un
    aviso después.

    Devuelve (factible: bool, gramos: {nombre: g} o None).
    """
    from accesibles import ACCESIBLES
    from exclusiones import filtrar

    if cuantos_max is None:
        from modos import CUANTOS_MAX as cuantos_max

    # ⚠️ AÑADIDO 5 agosto: "Extras" (aceites, huevos, semillas) NO estaba
    # en esta lista, así que ni siquiera entraban como candidatos — el
    # linoleico dependía solo de lo que aportara la carne, sin poder usar
    # aceite de girasol. Ahora entra, y junto con los suplementos
    # comerciales queda topado al 5% del peso (decisión de la usuaria).
    SUP_CATS = ("Multivitamínico", "Omega-3", "Yodo", "Fibra", "Calcio",
               "Hierro", "Vitamina B", "Extras")

    # Candidatos: TODOS los accesibles de cada categoría de comida, y
    # TODOS los suplementos del catálogo (no solo unos pocos elegidos).
    #
    # ⚠️ REESCRITO (5 agosto, noche) — DECISIÓN DE DISEÑO IMPORTANTE,
    # pedida expresamente por la usuaria: ACCESIBLES es la lista de "lo
    # fácil/seguro de encontrar" que usa el AUTOMÁTICO para no sugerir
    # cosas raras -- pero eso NUNCA debe impedir que el usuario, a mano,
    # use CUALQUIER cosa del catálogo entero si la elige explícitamente
    # (personalizar, o "todo el/la X"). Antes, si algo no estaba en
    # ACCESIBLES, era imposible usarlo aunque el usuario lo pidiera
    # expresamente -- fallaba siempre, sin explicación. Ahora, si el
    # usuario fuerza un alimento concreto o pide "todo el/la X" y eso no
    # está en la lista curada, se añade igualmente desde el catálogo
    # completo, siempre que exista de verdad y sea de esa categoría.
    candidatos_por_cat = {}
    for cat, lista in ACCESIBLES.items():
        disp = [n for n in lista if n in alimentos]
        if excluidos:
            disp, _f, _a = filtrar(disp, excluidos)

        # elección explícita del usuario (personalizar): si forzó un
        # alimento de ESTA categoría que no estaba en la lista curada,
        # se añade igual, tomándolo del catálogo completo
        if forzar:
            for n in forzar:
                if n in alimentos and alimentos[n].get("categoria") == cat and n not in disp:
                    disp.append(n)

        # "Todo el/la especie": si tras filtrar por la especie pedida no
        # queda NINGÚN candidato curado, se busca en el catálogo entero
        # cualquier alimento de esa categoría+especie, en vez de dejar
        # la categoría vacía (que antes hacía fallar todo el menú).
        if restringir_especie and cat in restringir_especie:
            especie_pedida = restringir_especie[cat].strip().lower()
            disp_curados = [n for n in disp if especie_de(n).strip().lower() == especie_pedida]
            if not disp_curados:
                disp_curados = [n for n, a in alimentos.items()
                                if a.get("categoria") == cat
                                and especie_de(n).strip().lower() == especie_pedida]
            disp = disp_curados

        # ⚠️ AÑADIDO (5 agosto, madrugada) — ver docstring de
        # restringir_a_elegidos arriba. Se aplica DESPUÉS de todo lo
        # anterior: si esta categoría tiene una lista de "solo estos",
        # se descarta cualquier otro candidato de la categoría, sean
        # cuales sean -- solo quedan los nombres pedidos (comprobando
        # que existan de verdad y sean de esta categoría, tomándolos
        # del catálogo completo si no estaban en la lista curada).
        if restringir_a_elegidos and cat in restringir_a_elegidos:
            pedidos = [n for n in restringir_a_elegidos[cat]
                      if n in alimentos and alimentos[n].get("categoria") == cat]
            if pedidos:
                disp = pedidos

        # ⚠️ CORREGIDO (21 agosto) — FALLO GRAVE ENCONTRADO POR UNA PRUEBA
        # NUEVA: LAS ALERGIAS SE PODÍAN SALTAR FORZANDO UN ALIMENTO.
        #
        # El filtro de exclusiones se aplicaba arriba del todo, ANTES que
        # `forzar` y `restringir_a_elegidos` -- y los dos vuelven a meter
        # alimentos en la lista sin volver a mirarlo: forzar hace
        # `disp.append(n)` y restringir_a_elegidos hace `disp = pedidos`,
        # que reemplaza la lista filtrada entera. Resultado: forzar un
        # alimento al que el perro es alérgico lo colaba en la ración,
        # anulando la alergia por completo. Va contra la regla del
        # proyecto que dice que las alergias no se tocan jamás porque
        # pueden ser médicas.
        #
        # No era teórico ni raro. Cualquier camino que fuerce alimentos lo
        # dispara, y el más probable es EDITAR un menú ya hecho: al
        # cambiar o añadir un alimento se fuerzan todos los demás para
        # conservarlos, así que un menú generado ANTES de apuntar una
        # alergia nueva se la saltaba entera al primer retoque. Lo
        # encontró la prueba de dos perros en la misma casa (a uno se le
        # fuerzan los alimentos del otro), pero el fallo estaba desde
        # mucho antes y no tiene nada que ver con tener varios perros.
        #
        # El arreglo es de ORDEN, no de caso particular: las exclusiones
        # se vuelven a aplicar AQUÍ, al final, igual que ya hacían las
        # categorías excluidas y las restricciones por patología, que
        # están justo debajo y por el mismo motivo. Así gana siempre la
        # exclusión, venga de donde venga el alimento y aunque mañana se
        # añada otra forma nueva de meterlo en la lista.
        #
        # Lo que el usuario elige a mano manda sobre ACCESIBLES -- la
        # lista curada de "lo fácil de encontrar", que es comodidad
        # nuestra -- pero nunca sobre una exclusión suya.
        if excluidos:
            disp, _quitados_final, _avisos_final = filtrar(disp, excluidos)

        # ⚠️ AÑADIDO (5 agosto, madrugada) — PEDIDO EXPRESO: perros que
        # no pueden masticar hueso carnoso con normalidad (senior,
        # dientes en mal estado, etc.) necesitan poder excluir esa
        # categoría ENTERA de la ración -- no elegir una especie
        # concreta, sino no usar NINGÚN hueso carnoso. Se aplica el
        # ÚLTIMO, después de cualquier otra restricción, y GANA sobre
        # todas ellas: si la categoría está excluida, se vacía sin
        # excepción, aunque forzar/restringir_a_elegidos hubiera puesto
        # algo ahí (nunca debería pasar en la práctica -- el frontend no
        # debe dejar elegir a mano una categoría que se acaba de excluir
        # -- pero por seguridad, la exclusión gana siempre).
        if categorias_excluidas and cat in categorias_excluidas:
            disp = []

        # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO,
        # pedido expreso: con oxalato cálcico, el aviso decía "no
        # debería dársele espinaca" pero la espinaca aparecía en el
        # menú de todas formas -- toda una categoría de restricciones
        # de patología (oxalato, urato, borraja, restricciones propias
        # de cada alimento) solo vivían como aviso de texto, nunca como
        # algo que el solver respetara al elegir. Se aplica AQUÍ, con
        # la MISMA prioridad final que categorias_excluidas (después de
        # forzar/restringir_a_elegidos, ganando sobre ellos) -- la
        # seguridad nunca debe poder saltarse ni siquiera si alguien
        # intenta forzar a mano un alimento prohibido por patología.
        #
        # ⚠️ CORREGIDO en el mismo momento -- CASO REAL ENCONTRADO
        # probando "urato": la primera versión de esto ponía TECHO=0
        # más abajo en vez de quitar el alimento de aquí -- pero dejarlo
        # presente como variable del LP (aunque con techo 0) podía
        # "gastar" el cupo de restricciones como "máximo 1 víscera"
        # (cuantos_max) sin aportar nada real, dejando sin cupo a una
        # víscera de verdad y volviendo el problema matemáticamente
        # infactible sin motivo real. Quitarlos aquí, del catálogo de
        # candidatos, evita que puedan "gastar" cupo de ninguna
        # restricción, sea la que sea.
        from seguridad import OXALATO_ALTO, PURINAS_ALTAS, BORRAJA_EXCLUIR, _es as _es_patologia
        if "oxalato" in (patologias or []):
            disp = [n for n in disp if not _es_patologia(n, OXALATO_ALTO)]
        if "urato" in (patologias or []) and cat in ("Hígado", "Vísceras", "Pescados y mariscos"):
            disp = [n for n in disp if not _es_patologia(n, PURINAS_ALTAS)]
        disp = [n for n in disp if not _es_patologia(n, BORRAJA_EXCLUIR)]
        disp = [n for n in disp
               if not any(pat in (patologias or [])
                         for pat in (alimentos.get(n, {}).get("restricciones_patologia") or {}))]

        candidatos_por_cat[cat] = disp
    # ⚠️ LAS EXCLUSIONES TAMBIÉN AQUÍ (29 agosto). CASO REAL: se excluye el
    # aceite de cacahuete por nombre y el menú lo lleva igual, 2 de cada 3
    # veces. Y lo mismo con la semilla de sésamo, el aceite de girasol y el
    # de linaza -- comprobado uno a uno.
    #
    # El motivo es de ORDEN, y es el mismo fallo que ya se arregló arriba en
    # el bucle de categorías: esta lista se construía del CATÁLOGO ENTERO, de
    # una sola pasada, saltándose todos los filtros que el bucle de arriba
    # aplica -- las exclusiones del usuario incluidas.
    #
    # Y no es una lista cualquiera. `SUP_CATS` mete dentro "Extras", que son
    # los aceites, las semillas, los huevos y la sal: aceite de cacahuete,
    # semilla de sésamo, huevo de gallina. Alérgenos de manual. La regla 4
    # del CLAUDE.md dice que las alergias y lo que se excluye a mano no se
    # tocan JAMÁS porque pueden ser médicas -- y por aquí se tocaban.
    #
    # Se pasa por los mismos filtros y en el mismo orden. Un extra es
    # "libre" en el sentido de que el usuario no lo elige en ninguna
    # pantalla; nunca en el de saltarse lo que ha prohibido.
    _sup = [a["nombre"] for a in alimentos.values() if a.get("categoria") in SUP_CATS]
    if excluidos:
        _sup, _qs, _as = filtrar(_sup, excluidos)
    if categorias_excluidas:
        _sup = [n for n in _sup
                if alimentos.get(n, {}).get("categoria") not in categorias_excluidas]
    if "oxalato" in (patologias or []):
        _sup = [n for n in _sup if not _es_patologia(n, OXALATO_ALTO)]
    _sup = [n for n in _sup if not _es_patologia(n, BORRAJA_EXCLUIR)]
    _sup = [n for n in _sup
            if not any(pat in (patologias or [])
                      for pat in (alimentos.get(n, {}).get("restricciones_patologia") or {}))]
    candidatos_por_cat["Suplementos"] = _sup


    # ⚠️ REESCRITO (5 agosto, mañana): antes solo se EXCLUÍA "V-INTEGRA
    # Perro Adulto" fuera de esa etapa, sin ofrecer ninguna alternativa
    # -- así que un cachorro se quedaba sin ningún V-INTEGRA disponible
    # (el motor tenía que buscarse la vida con otra marca). Ahora que
    # existen las 5 variantes reales del fabricante (Cachorro, Adulto,
    # Senior, Epato, Renal, con datos de la ficha oficial), se filtra la
    # lista para que SOLO esté disponible la variante correcta según la
    # etapa y la patología del perro -- nunca las demás, aunque
    # matemáticamente "cuadraran": cada una está formulada para una
    # necesidad concreta (más calcio en cachorro, cobre restringido en
    # hepatopatía, fósforo a cero en renal...), y mezclar no tiene sentido.
    TODAS_LAS_VINTEGRA = {"V-INTEGRA Cachorro", "V-INTEGRA Perro Adulto",
                          "V-INTEGRA Senior", "V-INTEGRA Epato", "V-INTEGRA Renal"}
    if patologias and "hepatopatia" in patologias:
        correcta = "V-INTEGRA Epato"
    elif patologias and "renal" in patologias:
        correcta = "V-INTEGRA Renal"
    elif etapa in ("CachorroJoven", "CachorroCrecimiento", "Gestante",
                   "GestanteTemprana", "GestanteTardia", "Lactante"):
        correcta = "V-INTEGRA Cachorro"  # misma exigencia nutricional que un cachorro
    elif etapa == "Senior":
        correcta = "V-INTEGRA Senior"
    else:
        correcta = "V-INTEGRA Perro Adulto"
    candidatos_por_cat["Suplementos"] = [
        n for n in candidatos_por_cat["Suplementos"]
        if n not in TODAS_LAS_VINTEGRA or n == correcta
    ]

    nombres = []
    categoria_de = {}
    for cat, lista in candidatos_por_cat.items():
        for n in lista:
            if n not in nombres:
                nombres.append(n)
                categoria_de[n] = cat
    n_var = len(nombres)
    # variables: [gramos_0..gramos_N-1, usa_0..usa_N-1] — la mitad continuas,
    # la mitad binarias (0/1), unidas por: gramos_i <= usa_i * TECHO_i
    idx = {n: i for i, n in enumerate(nombres)}

    et = EQUIVALENCIA.get(etapa, etapa)
    A_rows, lb_rows, ub_rows = [], [], []

    # ⚠️ AÑADIDO (24 agosto) — PARA PODER DEMOSTRAR QUE UNA REGLA EXISTE.
    #
    # Dos veces ha pasado ya que una restricción de este archivo no se
    # añadía NUNCA -- el límite de 2 suplementos y el suelo de 1 g -- las
    # dos por comparar `categoria_de[n]` (la CLAVE del diccionario de
    # candidatos) contra una categoría real. No da error, no da aviso: la
    # regla deja de existir y los menús siguen saliendo bien casi siempre.
    # Generar menús y mirarlos NO lo caza; por eso las dos veces las
    # encontró la casualidad, no las pruebas.
    #
    # Con esto sí se caza: quien llame puede pasar un diccionario vacío en
    # `diagnostico` y recibir cuántas filas puso cada regla. Si una regla
    # dice 0, esa regla no existe. Es solo contabilidad: no toca ni una
    # fila, ni un coeficiente, ni el resultado. Lo usa el BLOQUE 16.
    def _fila(regla, fila, lo, hi, alimento=None):
        A_rows.append(fila)
        lb_rows.append(lo)
        ub_rows.append(hi)
        if diagnostico is not None:
            # ⚠️ AÑADIDO (29 agosto): las reglas que ponen UNA FILA POR
            # ALIMENTO apuntan además de cuál. Contarlas no basta para
            # saber si alguna se queda fuera: el BLOQUE 16 comparaba el
            # número de filas del suelo de 1 g contra el número de
            # "Extras" del catálogo, y eso solo cuadra mientras el suelo
            # sea exactamente el de los extras. Con los nombres se puede
            # comprobar lo que de verdad importa -- que ningún candidato
            # que se pesa en una báscula se quede sin suelo -- sin que la
            # prueba tenga que adivinar cuáles son candidatos.
            if alimento is not None:
                diagnostico.setdefault("_alimentos", {}).setdefault(regla, []).append(alimento)
            # ⚠️ Se cuentan las filas Y sus coeficientes. Contar solo filas no
            # basta: el límite de 2 suplementos estuvo inerte con su fila
            # PUESTA -- lo que estaba vacío era la fila, porque el bucle que
            # la rellena comparaba `categoria_de` y no acertaba con nadie.
            # Una fila sin un solo coeficiente no restringe nada: es 0 <= 2.
            d = diagnostico.setdefault(regla, {"filas": 0, "coeficientes": 0})
            d["filas"] += 1
            d["coeficientes"] += sum(1 for v in fila if v)

    def fila_vacia():
        return [0.0] * (2 * n_var)

    # TECHOS por variable (para la vinculación gramos<=usa*techo)
    # ⚠️ AÑADIDO (5 agosto): diabetes quita la fruta del todo. Poniendo su
    # techo a 0, la vinculación gramos<=usa*techo obliga gramos=0 siempre,
    # sin tocar el resto de la formulación.
    excluye_fruta = any(PATOLOGIAS.get(p, {}).get("excluye_fruta") for p in (patologias or []))
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL GRAVE ENCONTRADO,
    # pedido expreso: "con oxalato cálcico avisa que no debería dársele
    # espinaca, y la mete en el menú de todas formas". Causa real: había
    # TODA una categoría de restricciones de patología (oxalato, urato,
    # borraja, y las restricciones propias de cada alimento como grelo/
    # nabo en hipotiroidismo) que solo vivían como AVISO de texto en
    # seguridad.py, sin ninguna exclusión real dentro del solver -- a
    # diferencia de los topes numéricos (fósforo, sodio, grasa%) que sí
    # eran restricciones duras. El solver podía meter espinaca sin nada
    # que se lo impidiera, y el aviso posterior decía "esto no debería
    # estar aquí" sobre un menú que él mismo ya había generado. Ahora se
    # excluyen con el MISMO mecanismo que ya usaba la fruta en diabetes
    # (techo a 0): oxalato con antecedente de urolitos, urato con
    # predisposición, borraja siempre (toxicidad real, no depende de
    # patología), y las restricciones propias de cada alimento en el
    # catálogo (grelo/nabo, dátil/mango/plátano, coco...).
    from seguridad import OXALATO_ALTO, PURINAS_ALTAS, BORRAJA_EXCLUIR, _es as _es_patologia
    excluye_oxalato = "oxalato" in (patologias or [])
    excluye_urato = "urato" in (patologias or [])
    CATEGORIAS_PURINAS_REALES = {"Hígado", "Vísceras", "Pescados y mariscos"}
    techos = []
    for n in nombres:
        a = alimentos[n]
        if excluye_fruta and n in FRUTAS:
            techos.append(0.0)
            continue
        if excluye_oxalato and _es_patologia(n, OXALATO_ALTO):
            techos.append(0.0)
            continue
        if excluye_urato and _es_patologia(n, PURINAS_ALTAS) and a.get("categoria") in CATEGORIAS_PURINAS_REALES:
            techos.append(0.0)
            continue
        if _es_patologia(n, BORRAJA_EXCLUIR):
            techos.append(0.0)
            continue
        restr_propia = a.get("restricciones_patologia") or {}
        if any(pat in (patologias or []) for pat in restr_propia):
            techos.append(0.0)
            continue
        if categoria_de[n] == "Suplementos":
            t = dosis_maxima_fn(a, peso_perro_kg)
            techos.append(t if t else 5.0)
        else:
            kcal100 = a.get("energia", 0) or 1.0
            techos.append((der * 0.55) / kcal100 * 100.0)  # ningún alimento >55% del día

    # ─── LOS GRAMOS QUE YA HA DECIDIDO EL VETERINARIO ────────────────────
    #
    # ⚠️ AÑADIDO (29 agosto) para el formulador del profesional, y el orden
    # importa: esto tiene que estar AQUÍ, tocando los techos, y no más abajo
    # tocando solo los `bounds`. La fila de vinculación (gramos <= usa *
    # techo) se construye con estos techos, así que fijar una cantidad por
    # encima del techo sin tocarlo daba un infactible imposible de explicar.
    #
    # Qué cede y qué no, que es la decisión de verdad:
    #
    #   · El "ningún alimento pasa del 55 % de las kcal del día" es criterio
    #     NUESTRO, de la forma de una ración BARF. Ante una cantidad que ha
    #     decidido un veterinario con el animal delante, cede -- igual que
    #     ceden las proporciones de categoría en la escalera de relajación
    #     (regla 3 del CLAUDE.md).
    #   · La dosis máxima del FABRICANTE de un suplemento NO cede. No es
    #     criterio nuestro: es la etiqueta del bote.
    #   · Un techo a CERO tampoco cede nunca. Ahí no hay una cantidad
    #     grande: hay un alimento excluido por una alergia o por la propia
    #     patología del paciente (oxalato, urato, borraja...). Regla 4.
    #
    # Y lo que NO se toca en ningún caso: los 41 requisitos, el ratio Ca:P,
    # los cinco topes de seguridad crónica y los topes por patología. Son
    # filas aparte, siguen midiéndose sobre la ración completa, y por eso
    # fijar una cantidad puede seguir saliendo infactible -- que es lo que
    # tiene que pasar si lo que se ha fijado no cabe.
    if gramos_fijos:
        for n, g in (gramos_fijos or {}).items():
            if n not in idx:
                # ⚠️ AQUÍ NO SE PUEDE SEGUIR EN SILENCIO (29 agosto). Un
                # alimento que no está entre los candidatos es uno al que se
                # le ha quitado el sitio antes: una alergia, la patología del
                # paciente (oxalato, urato, borraja...) o una categoría
                # excluida entera. `forzar` sí se lo puede saltar callando --
                # ahí la exclusión gana y ya está --, pero fijar una CANTIDAD
                # es otra cosa: el veterinario ha escrito 50 g de espinaca y
                # el menú salía verde, sin espinaca y sin una palabra. Lo
                # cazó el BLOQUE 41 el día que se escribió.
                return False, {"_imposible": (
                    f"{n} no puede entrar en la ración de este paciente: está fuera por "
                    f"una alergia, por su patología o por una categoría excluida.")}
            try:
                g = float(g)
            except (TypeError, ValueError):
                continue
            if g <= 0:
                continue
            i = idx[n]
            if techos[i] <= 0:
                return False, {"_imposible": (
                    f"{n} no puede entrar en la ración de este paciente: está excluido "
                    f"por una alergia o por su patología.")}
            if categoria_de[n] == "Suplementos" and g > techos[i] + 1e-9:
                return False, {"_imposible": (
                    f"{n}: {g:.0f} g pasan de la dosis máxima que marca el fabricante "
                    f"para un perro de este peso ({techos[i]:.1f} g).")}
            techos[i] = max(techos[i], g)

    # 1. kcal totales = DER (con tolerancia)
    fila = fila_vacia()
    for n in nombres:
        fila[idx[n]] = alimentos[n].get("energia", 0) / 100.0
    _fila("kcal_total", fila, der * (1 - tolerancia_kcal), der * (1 + tolerancia_kcal))

    # ⚠️ AÑADIDO (5 agosto): topes mas estrictos por patologia. Si una
    # patologia baja el maximo de un nutriente y ese maximo es MAS
    # RESTRICTIVO que el de FEDIAF, gana el de la patologia (el min de
    # los dos). Nunca al reves: una patologia no puede RELAJAR un tope.
    # ⚠️ Los topes salen de `topes_de_patologias`, que ya sabe qué aplica en
    # esta etapa (25 agosto). Antes se leían crudos de la tabla y se
    # aplicaban igual a un cachorro que a un adulto -- ver el comentario
    # largo de esa función.
    topes_patologia, pct_grasa_patologia, _avisos_pat = topes_de_patologias(patologias, etapa)

    # ⚠️ AÑADIDO (5 agosto, noche) — CONECTADO: "Calcio_LateGrowth_RazaGrande"
    # ya existía en los datos, con nota de auditoría explícita diciendo que
    # el motor nunca lo usaba porque no estaba en su MAPA. Fuente: 4.5g/1000kcal
    # como techo de calcio en cachorros de razas grandes/gigantes es la cifra
    # que cita la literatura veterinaria (Vet Clinics: Small Animal Practice,
    # citando FEDIAF) -- coincide con el techo genérico que YA aplicábamos a
    # TODOS los cachorros. Lo que de verdad falta para raza grande/gigante es
    # un MÍNIMO más alto (2500 en vez de 2000): necesitan una ingesta más
    # consistente, no tienen margen para quedarse cortas. Solo se activa para
    # razas grande/gigante (peso adulto esperado >= 25kg) Y en crecimiento --
    # nunca para razas pequeñas, donde este mínimo más alto no aplica.
    minimos_reforzados = {}
    RAZA_GRANDE_O_GIGANTE_KG = 25
    if (peso_adulto_esperado_kg and peso_adulto_esperado_kg >= RAZA_GRANDE_O_GIGANTE_KG
            and etapa in ("CachorroJoven", "CachorroCrecimiento")):
        r_grande = req.get("Calcio_LateGrowth_RazaGrande")
        if r_grande:
            mn_grande = _num(r_grande.get(f"min{et}"))
            if mn_grande:
                minimos_reforzados["calcio"] = mn_grande

    # 2. mínimos y máximos de FEDIAF
    #
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CAMBIO DE ARQUITECTURA PEDIDO
    # EXPRESAMENTE: hasta ahora, los topes de seguridad crónica
    # (mercurio, vitamina D, yodo, selenio) SOLO se comprobaban DESPUÉS
    # de generar el menú, como un aviso de texto -- el usuario podía
    # ignorarlo, y el sistema seguía dejando pasar la dieta igual. Se
    # pidió explícitamente que estos límites nunca puedan superarse,
    # ni con aviso ni sin él: la responsabilidad es del sistema, no del
    # usuario. Para vitamina D y yodo, algunos de nuestros umbrales de
    # seguridad crónica (NRC 2006) son MÁS ESTRICTOS que el máximo
    # nutricional/legal de FEDIAF -- así que aquí se usa siempre el más
    # estricto de los dos como techo REAL del solver, no solo el de
    # FEDIAF. Ver seguridad.py para el porqué de cada cifra.
    from seguridad import (TOPE_VITD_KCAL, TOPE_VITD_KG075, TOPE_YODO_KCAL,
                           TOPE_SELENIO_KCAL)
    # ⚠️ CORREGIDO (5 agosto, madrugada) — BUG REAL Y GRAVE ENCONTRADO,
    # pedido expreso: "si edito un menú, ¿sigue teniendo en cuenta los
    # límites semanales?" -- investigando eso se encontró un bug de
    # unidades MUCHO más amplio, presente en TODO el sistema (no solo
    # al editar). MAPA (usado más abajo para construir cada restricción
    # con "hi = mx * der / 1000.0") espera que "mx" sea una TASA "por
    # 1000kcal" -- pero "tope_vitd_activo" se calculaba AQUÍ ya
    # convertido a un valor ABSOLUTO (TOPE_VITD_KCAL * der / 1000.0),
    # y luego se mezclaba, vía min(), con el máximo FEDIAF (que SÍ es
    # una tasa) y con presupuesto_semanal_restante (también absoluto) --
    # tres magnitudes de unidades distintas comparadas como si fueran
    # la misma cosa. El resultado ganador de esos min() volvía a pasar
    # por "* der / 1000.0" en el bucle de más abajo, aplicando la
    # conversión de tasa a absoluto una SEGUNDA vez cuando el valor ya
    # era absoluto -- confirmado con un caso real: un tope real de 18µg
    # se convertía en un tope efectivo de 21.6µg (18 * der/1000 = 18*1.2),
    # una violación del 20% que solo aparecía cuando el solver se veía
    # empujado cerca de ese límite (de ahí que fuera intermitente, no
    # siempre). Ahora TODO se mantiene como tasa "por 1000kcal" hasta el
    # final del bucle, y solo se convierte a absoluto una única vez, ahí.
    tope_vitd_activo = TOPE_VITD_KCAL
    # ⚠️ CORREGIDO en el mismo momento, CASO REAL ENCONTRADO en producción
    # (segunda vez que se pedía este arreglo): la Fase 1 original solo
    # llevaba el tope por kcal de vitamina D como restricción dura --
    # NUNCA se calculaba ni comparaba el tope por peso (kg^0.75), que sí
    # se compara correctamente en el aviso de revisar_seguridad() (solo
    # avisa, no bloquea). Un cachorro/lactante pequeño puede tener un
    # tope por peso mucho más estricto que el de kcal (confirmado con
    # datos reales: 3.5µg por peso frente a 12.9µg por kcal para un Toy
    # Lactante de 1.5kg) -- así que el solver dejaba pasar menús que
    # violaban el límite real sin que nada lo impidiera, porque nunca
    # llegó a comparar contra el tope correcto. TOPE_CRONICO_KCAL usa
    # ahora siempre el más estricto de los dos, igual que ya hacía
    # revisar_seguridad() -- MAPA guarda "vitD" en kcal por 1000, así
    # que el de peso se convierte a esa misma unidad antes de comparar.
    if peso_perro_kg and peso_perro_kg > 0 and der:
        tope_vitd_por_peso_absoluto = TOPE_VITD_KG075 * (peso_perro_kg ** 0.75)
        tope_vitd_por_peso_en_kcal = tope_vitd_por_peso_absoluto / der * 1000.0
        tope_vitd_activo = min(tope_vitd_activo, tope_vitd_por_peso_en_kcal)
    # ⚠️ AÑADIDO en el mismo momento -- CASO REAL: probando el arreglo de
    # arriba, el solver se pegaba EXACTO al límite (matemáticamente
    # correcto con precisión completa), pero el redondeo de gramos a 2
    # decimales para enseñarlos podía empujar el valor final ligerísimamente
    # por encima del tope real -- mismo mecanismo que ya se documentó para
    # los mínimos (con su margen del 0.8%), pero nunca se había aplicado a
    # los máximos. Con márgenes de seguridad tan estrechos como estos
    # (algunos casos dejan muy poco margen entre el mínimo de FEDIAF y el
    # tope de seguridad crónica), ese redondeo puede marcar la diferencia
    # entre pasar o no pasar el límite real. Margen del 1% SOLO en estos 5
    # puntos concretos, no en el resto de los 30 requisitos de FEDIAF.
    MARGEN_REDONDEO_SEGURIDAD = 0.99
    tope_vitd_activo *= MARGEN_REDONDEO_SEGURIDAD
    TOPE_CRONICO_KCAL = {"vitD": tope_vitd_activo,
                         "yodo": TOPE_YODO_KCAL * MARGEN_REDONDEO_SEGURIDAD,
                         # ⚠️ CORREGIDO (26 agosto). El selenio se topaba
                         # con los 2 µg/g de Merck aplicados sobre el PESO
                         # FRESCO, y esos 2 mg/kg son en base MATERIA
                         # SECA: en BARF (70-75% de agua) eso dejaba pasar
                         # entre tres y cuatro veces el límite real, sin
                         # dar ningún error. Ahora va por energía, que no
                         # depende del agua de la ración. Ver el bloque de
                         # TOPE_SELENIO_KCAL en seguridad.py.
                         "selenio": TOPE_SELENIO_KCAL * MARGEN_REDONDEO_SEGURIDAD}
    # ⚠️ EPA+DHA SOLO SI VIENE PRESUPUESTO (26 agosto). No se siembra con un
    # valor por defecto a propósito: un menú suelto (/menu/v2) NO lleva techo
    # de EPA+DHA, porque los 2800 mg son el límite de la dieta habitual y no
    # el de un plato. Ponerlo por menú borraba el pescado azul del catálogo
    # entero -- 19 de los 20 pescados lo pasan ellos solos. Ver el comentario
    # largo de TOPE_EPA_DHA_SEMANAL_KCAL en seguridad.py.
    #
    # Cuando /menu/semana sí manda presupuesto, entra aquí y se convierte en
    # el techo de ESTE menú: lo que queda de la semana repartido entre los
    # días que faltan. El motor equilibra solo.
    if presupuesto_semanal_restante and der and presupuesto_semanal_restante.get("epa_dha"):
        TOPE_CRONICO_KCAL["epa_dha"] = (
            presupuesto_semanal_restante["epa_dha"] / der * 1000.0)
    if presupuesto_semanal_restante and der:
        # presupuesto_semanal_restante llega en valores ABSOLUTOS (µg
        # totales para el día) desde main.py -- se convierte aquí a la
        # misma tasa "por 1000kcal" que usa TOPE_CRONICO_KCAL, antes de
        # comparar con min(). La conversión a absoluto real ocurre una
        # única vez, más abajo en el bucle de MAPA (hi = mx * der / 1000).
        for clave_nut, tope_efectivo_absoluto in presupuesto_semanal_restante.items():
            if clave_nut in TOPE_CRONICO_KCAL:
                tope_efectivo_tasa = tope_efectivo_absoluto / der * 1000.0
                # nunca se afloja -- solo se usa si es MÁS estricto que el normal
                TOPE_CRONICO_KCAL[clave_nut] = min(TOPE_CRONICO_KCAL[clave_nut], tope_efectivo_tasa)
    tabla_max = tabla_imputacion_maximos(alimentos)

    # ⚠️ LOS MINIMOS ESCALADOS POR LA DER EFECTIVA (28 agosto). Va AQUI,
    # dentro del solver, y no como un aviso posterior: si un perro come
    # menos, necesita mas nutriente por caloria, y eso es una restriccion
    # del problema, no una nota al pie. Ver `minimo_de()` en verificar.py,
    # que es el unico sitio que sabe escalar -- el semaforo lee por ahi
    # tambien, para que no puedan discrepar.
    #
    # El peso de referencia es el OBJETIVO si se sabe: en un perro con
    # sobrepeso las kcal ya se calculan sobre el peso ideal, asi que la DER
    # efectiva tiene que salir del mismo peso o el numero no significa
    # nada. Si no llega, se usa el real y se escala un poco de mas -- que
    # es el lado seguro.
    _peso_ref = peso_objetivo_kg or peso_perro_kg
    _der_ef = der_efectiva_de(der, _peso_ref)

    for nombre_req, clave in MAPA.items():
        r = req.get(nombre_req)
        if not r:
            continue
        mn = minimo_de(r, nombre_req, et, _der_ef)
        # ⚠️ CUANDO EL MINIMO SUPERA AL MAXIMO NO ES «NO HAY COMBINACION»
        # (28 agosto). Los minimos suben al restringir calorias, pero los
        # maximos NO: son limites de CONCENTRACION en el alimento (la tabla
        # III-3a los da en base materia seca y marca los de la UE con «(L)»),
        # y una concentracion no depende de cuanto coma el perro. Asi que la
        # ventana entre los dos se cierra segun bajan las kcal.
        #
        # Medido sobre nuestra propia tabla: el primero en cruzarse es el
        # SELENIO en dieta humeda -que es la que aplica a una racion BARF-
        # a DER 45. Su minimo a DER 95 son 67,5 ug/1000 kcal y el maximo
        # legal de la UE son 142,0; 67,5 x 95/45 = 142,5. A DER 56 (el 80%
        # del RER, la bajada de AAHA) la ventana ya es de solo x1,24.
        #
        # Por debajo de ese cruce el problema es INFACTIBLE POR ARITMETICA:
        # no hay ningun alimento, ni ninguna combinacion, ni quitar ninguna
        # restriccion que lo arregle. Decir «quita alguna restriccion y
        # vuelve a probar» manda a la usuaria a un callejon sin salida.
        _mx_fediaf = maximo_de(r, nombre_req, et)
        if mn is not None and _mx_fediaf is not None and mn > _mx_fediaf:
            return False, {"_imposible": (
                f"A estas calorías, el mínimo de {nombre_req.replace('_', ' ').lower()} "
                f"({mn:.1f}) supera su máximo ({_mx_fediaf:.1f}). Cuando un perro come menos, "
                f"cada nutriente tiene que ir más concentrado para llegar a lo que necesita al "
                f"día — pero el máximo es un límite de concentración y no se mueve. Con esta "
                f"ración no existe ninguna combinación de alimentos que cumpla las dos cosas a "
                f"la vez, así que hace falta subir las calorías o una dieta formulada.")}
        if clave in minimos_reforzados:
            mn = minimos_reforzados[clave] if mn is None else max(mn, minimos_reforzados[clave])
        mx = maximo_de(r, nombre_req, et)
        if clave in topes_patologia:
            mx = topes_patologia[clave] if mx is None else min(mx, topes_patologia[clave])
        if clave in TOPE_CRONICO_KCAL:
            tope_cronico = TOPE_CRONICO_KCAL[clave]
            mx = tope_cronico if mx is None else min(mx, tope_cronico)
        fila = fila_vacia()
        # ⚠️ SEGUNDA FILA, LA CONSERVADORA (27 agosto). Cuando un alimento
        # tiene un valor DUDOSO con un `valor_plausible` conocido, el mismo
        # numero no puede servir para el minimo y para el maximo: inflado
        # protege contra el techo y DESPROTEGE contra el suelo, porque el
        # motor cree cubierto lo que no esta. Asi que el minimo se exige
        # sobre el valor plausible y el maximo sobre el declarado.
        # El caso: el polvo de sangre declara 80 mg de cobre/100 g y la
        # sangre bovina desecada ronda 0,5. Antes de esto, forzandolo en un
        # perro de 25 kg salia un menu con 2,34 mg de cobre real sobre un
        # minimo de 2,60 -- deficitario y en VERDE.
        # Si ningun alimento trae `valor_plausible`, las dos filas son
        # identicas y se pone una sola, como siempre.
        fila_min = fila_vacia()
        # ⚠️ TERCERA FILA (28 agosto): la de los TECHOS con los huecos del
        # catálogo imputados al percentil de su familia. Sin esto el solver
        # cuenta un `sin_dato` como cero contra el máximo, construye un menú
        # que se pasa, y es el verificador quien lo tira después -- o sea,
        # trabajo tirado y un menos de menús. Mismo criterio en los dos
        # sitios, calculado en `constructor.valor_para_maximo`.
        fila_max = fila_vacia()
        aporta_algo = False
        hay_dudoso = False
        hay_hueco = False
        for n in nombres:
            nut_n = alimentos[n].get("nutrientes", {})
            v = valor_nutriente(nut_n, clave) / 100.0
            plausible = valor_plausible_de(alimentos[n], clave)
            v_min = v if plausible is None else float(plausible) / 100.0
            v_max, estado = valor_para_maximo(alimentos[n], clave, tabla_max)
            v_max /= 100.0
            if v:
                fila[idx[n]] = v; aporta_algo = True
            if v_min:
                fila_min[idx[n]] = v_min
            if v_max:
                fila_max[idx[n]] = v_max
            if plausible is not None and v_min != v:
                hay_dudoso = True
            if estado == "imputado" and v_max != v:
                hay_hueco = True
        if not aporta_algo:
            continue
        # ⚠️ AÑADIDO (5 agosto): +1.5% de margen sobre el mínimo exacto.
        # Encontrado probando la aleatoriedad de arriba: el programa podía
        # resolver EXACTO al límite (matemáticamente correcto con toda su
        # precisión), pero al redondear los gramos a 2 decimales para
        # enseñarlos, ese redondeo empujaba el nutriente justo por debajo
        # del mínimo -- pasando de "cumple" a "no cumple" solo por el
        # redondeo, no por un fallo real de la solución. Con este margen,
        # el redondeo ya no puede tirarlo por debajo.
        # ⚠️ SUBIDO de 0.8% a 1.5% (5 agosto, madrugada) — CASO REAL: el
        # cloruro en un Toy CachorroJoven de 1.5kg tenía 156.36mg vs el
        # mínimo de 157.50mg -- diferencia de 1.14mg, equivalente a 0.002g
        # de sal (60.700mg cloruro/100g). El solver resolvía pidiendo 158.76mg
        # (0.8% sobre el mínimo) pero el redondeo a 2 decimales bajaba el
        # resultado 2.40mg por debajo de lo que el solver exigió. Con 1.5%
        # el solver pide 159.97mg, dejando un colchón real de 2.47mg por
        # encima del mínimo FEDIAF incluso después del redondeo.
        lo = mn * der / 1000.0 * 1.015 if mn is not None else -np.inf
        hi = mx * der / 1000.0 if mx is not None else np.inf
        # ⚠️ CADA COTA CON SU VECTOR, Y NUNCA AL REVÉS (28 agosto).
        #   suelo  -> el valor PLAUSIBLE del dato dudoso, y el hueco a CERO
        #   techo  -> el valor DECLARADO, y el hueco IMPUTADO a su familia
        # Es la misma regla de siempre ("un número que no nos creemos no puede
        # ser prudente en las dos direcciones"), ahora con el hueco además del
        # dato dudoso.
        # ⚠️ CASO REAL, y me lo comí yo al escribir esto: al principio la fila
        # imputada se usaba también cuando el nutriente NO tenía techo -- o
        # sea, para el MÍNIMO. El solver daba por cubierto el linoleico con un
        # valor que nadie ha medido, el verificador lo medía con el declarado,
        # y salían menús ROJOS al 28% del mínimo. La batería cazó 11 casos.
        fila_suelo = fila_min if hay_dudoso else fila
        fila_techo = fila_max if hay_hueco else fila
        tiene_suelo, tiene_techo = lo != -np.inf, hi != np.inf
        if tiene_suelo and tiene_techo and fila_suelo is not fila_techo:
            _fila("fediaf_minimo_conservador", fila_suelo, lo, np.inf)
            _fila("fediaf_maximo", fila_techo, -np.inf, hi)
        elif tiene_techo and not tiene_suelo:
            _fila("fediaf_maximo", fila_techo, -np.inf, hi)
        else:
            _fila("fediaf_absoluto", fila_suelo, lo, hi if not tiene_techo else hi)

        # ⚠️ AÑADIDO (21 agosto) — CASO REAL MEDIDO: con el tope renal de
        # fósforo en 1400, el motor devolvía menús con 1426. Se saltaba su
        # propio límite en un ~2%.
        #
        # La causa no era el solver: era la unidad. El tope de arriba se
        # convierte a absoluto con las kcal OBJETIVO (der), pero el menú
        # que sale puede tener hasta un 3% menos de kcal (tolerancia_kcal).
        # Menos kcal con el mismo total de nutriente = más concentración.
        # Y los requisitos de FEDIAF, y los topes por patología, se miden
        # POR 1000 KCAL DE LA DIETA REAL, no de las que se pidieron.
        #
        # Se añade el mismo tope expresado sobre las kcal de verdad, que
        # también es lineal -- mismo truco que ya se usaba abajo para el
        # selenio por gramo de dieta:
        #     suma(nut_i * g_i)  <=  (mx/1000) * suma(kcal_i * g_i)
        #   → suma((nut_i - (mx/1000) * kcal_i) * g_i)  <=  0
        #
        # Se deja TAMBIÉN la fila absoluta de arriba a propósito: cuando
        # el menú sale con MÁS kcal de las pedidas, la absoluta es la
        # estricta. Teniendo las dos, siempre manda la que más aprieta.
        if mx is not None:
            # ⚠️ AÑADIDO (24 agosto) — MARGEN DE REDONDEO, solo en los topes
            # que vienen de una PATOLOGÍA.
            #
            # CASO MEDIDO: un perro renal + hepático + cardiópata salía con
            # 1400.01 mg de fósforo y el tope es 1400. Son 7 partes por
            # millón -- clínicamente da igual --, pero el motor estaba
            # entregando un menú por encima de su propio límite, y estos
            # topes son duros, no avisos (regla 2 del CLAUDE.md).
            #
            # No es el solver: resuelve EXACTO en el límite, y luego los
            # gramos se redondean a 2 decimales para enseñarlos. Ese
            # redondeo es el que lo empuja por encima. Es el mismo problema
            # que ya tenían los MÍNIMOS, resuelto allí con un +1.5%.
            #
            # Se aprieta un 0,1%, y SOLO en los de patología: los máximos
            # de FEDIAF se quedan como están, porque tocarlos cambiaría el
            # comportamiento de todos los menús para arreglar algo que allí
            # no molesta -- pasarse una millonésima del máximo de un
            # nutriente no tiene consecuencia, saltarse el tope renal sí.
            mx_rel = mx * (1 - 0.001) if clave in topes_patologia else mx
            fila_rel = fila_vacia()
            for n in nombres:
                v_nut = valor_nutriente(alimentos[n].get("nutrientes", {}), clave) / 100.0
                kcal_n = (alimentos[n].get("energia", 0) or 0.0) / 100.0
                coef = v_nut - (mx_rel / 1000.0) * kcal_n
                if coef:
                    fila_rel[idx[n]] = coef
            _fila("fediaf_relativo", fila_rel, -np.inf, 0.0)

    # ⚠️ QUITADO (26 agosto) — aquí había una fila más en el sistema,
    # "selenio_por_gramo", que topaba el selenio a 2 µg por cada gramo de
    # dieta. El número era el de Merck, pero Merck lo da EN BASE MATERIA
    # SECA y aquí se multiplicaba por el peso fresco: con un 70-75% de
    # agua, el tope efectivo quedaba entre tres y cuatro veces por encima
    # del real. El selenio se topa ahora por energía, arriba, con
    # TOPE_CRONICO_KCAL -- la unidad en la que el agua de la ración no
    # puede falsear la cuenta.


    # ⚠️ AÑADIDO (5 agosto, madrugada) — TIAMINASA Y MERCURIO como
    # restricciones duras. Estos dos no son nutrientes numéricos con
    # dato por alimento -- son SETS de especies concretas (sardina/
    # caballa/arenque/boquerón/carpa para tiaminasa; atún para
    # mercurio), así que se restringe directamente la fracción de kcal
    # del día que pueden aportar ENTRE TODOS los alimentos de cada set,
    # igual que la restricción de kcal totales de arriba pero limitada
    # a ese subconjunto. Antes esto se comprobaba DESPUÉS de generar el
    # menú (revisar_seguridad) y solo avisaba -- ahora, si forzar algo
    # llevaría a superar el tope, el solver directamente no encuentra
    # solución, en vez de generarla y avisar después.
    from seguridad import TIAMINASA, MERCURIO_ALTO, TOPE_TIAMINASA_KCAL, TOPE_MERCURIO_KCAL, _es
    for clave_presupuesto, nombre_set, tope_frac in (
        ("tiaminasa", TIAMINASA, TOPE_TIAMINASA_KCAL),
        ("mercurio", MERCURIO_ALTO, TOPE_MERCURIO_KCAL),
    ):
        tope_frac_efectivo = tope_frac * MARGEN_REDONDEO_SEGURIDAD
        if presupuesto_semanal_restante and clave_presupuesto in presupuesto_semanal_restante:
            # aquí el presupuesto llega ya como fracción de kcal (0-1), igual que tope_frac
            tope_frac_efectivo = min(tope_frac_efectivo, presupuesto_semanal_restante[clave_presupuesto] * MARGEN_REDONDEO_SEGURIDAD)
        fila_set = fila_vacia()
        aporta_set = False
        for n in nombres:
            if _es(n, nombre_set):
                fila_set[idx[n]] = alimentos[n].get("energia", 0) / 100.0
                aporta_set = True
        if aporta_set:
            _fila("seguridad_cronica_" + clave_presupuesto, fila_set, -np.inf, tope_frac_efectivo * der)

    # 2b. RATIO Ca:P — se me olvidó la primera vez. Calcio y fósforo por
    # separado no bastan: la RELACIÓN entre ambos es su propio requisito,
    # y es lineal (Ca >= ratio_min * P  y  Ca <= ratio_max * P), así que
    # se puede meter igual que cualquier otra restricción.
    r_ratio = req.get("Relacion_Ca_P")
    if r_ratio:
        rmin = _num(r_ratio.get(f"min{et}"))
        rmax = _num(r_ratio.get(f"max{et}"))
        fila_ca = fila_vacia(); fila_p = fila_vacia()
        for n in nombres:
            ca = (_num(alimentos[n].get("nutrientes", {}).get("calcio")) or 0.0) / 100.0
            p = (_num(alimentos[n].get("nutrientes", {}).get("fosforo")) or 0.0) / 100.0
            fila_ca[idx[n]] = ca
            fila_p[idx[n]] = p
        if rmin is not None:
            fila = [fila_ca[j] - rmin * fila_p[j] for j in range(2 * n_var)]
            _fila("ratio_ca_p_min", fila, 0.0, np.inf)
        if rmax is not None:
            fila = [fila_ca[j] - rmax * fila_p[j] for j in range(2 * n_var)]
            _fila("ratio_ca_p_max", fila, -np.inf, 0.0)

    # 3. margen por peso de cada categoría de COMIDA (no suplementos)
    if margenes_categoria:
        # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO: las
        # exclusiones de patología recién añadidas arriba (oxalato,
        # urato, restricciones por alimento) pueden dejar una categoría
        # ENTERA vacía como efecto secundario -- por ejemplo, "urato"
        # excluye TODOS los alimentos de Hígado del catálogo (los 4/4
        # tienen purinas altas), pero Hígado sigue teniendo su mínimo
        # obligatorio del 3% del peso, matemáticamente imposible de
        # cumplir si no queda ningún candidato. A diferencia de
        # categorias_excluidas (donde el usuario pide excluir la
        # categoría a propósito), aquí nadie pidió vaciar "Hígado" --
        # es una consecuencia de excluir por seguridad los alimentos
        # concretos. Se detecta automáticamente qué categorías han
        # quedado sin ningún candidato disponible (techo>0 en ninguno
        # de sus miembros) y se tratan con el MISMO mecanismo que una
        # exclusión explícita: su mínimo se ignora, en vez de dejar el
        # problema matemáticamente irresoluble.
        categorias_con_candidato = {categoria_de[n] for n in nombres if techos[idx[n]] > 0}
        categorias_vaciadas_efectivo = {
            cat for cat in margenes_categoria
            if any(categoria_de[n] == cat for n in nombres) and cat not in categorias_con_candidato
        }
        categorias_excluidas_efectivo = set(categorias_excluidas or []) | categorias_vaciadas_efectivo
        # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO
        # completando la exclusión de categoría entera: quitar "Hueso
        # carnoso" (mínimo 20%, máximo 60% del peso) deja un hueco que
        # las demás categorías, con sus máximos actuales, no pueden
        # cubrir matemáticamente -- sumando los máximos del resto
        # (Carne 60% + Verdura 10% + Vísceras 12% + Hígado 6% + un 5%
        # de suplementos aparte) no se llega al 100% del peso del
        # menú, así que el problema era irresoluble aunque el mínimo
        # de Hueso carnoso ya se hubiera puesto a 0. Cuando se excluye
        # esta categoría a propósito, se sube el máximo de Carne
        # muscular (pescado incluido) para que pueda absorber ese
        # hueco -- es la categoría más natural para compensarlo, ya
        # que el hueso carnoso también aporta principalmente proteína
        # y grasa, no un nutriente exclusivo suyo.
        if "Hueso carnoso" in categorias_excluidas_efectivo:
            margenes_categoria = dict(margenes_categoria)
            mn_carne, mx_carne = margenes_categoria.get("Carne muscular", (0.10, 0.60))
            _mn_hueso, mx_hueso = margenes_categoria.get("Hueso carnoso", (0.20, 0.60))
            # ⚠️ CORREGIDO en el mismo momento -- probado con el motor
            # real: sumar una cifra fija (+0.20) no bastaba, seguía
            # siendo matemáticamente imposible llegar al 100% del peso.
            # El cálculo correcto es sumar el HUECO REAL que deja el
            # hueso (su máximo habitual), con 0.95 como techo -- no 1.0
            # exacto, para dejar algo de margen a las categorías con
            # mínimo obligatorio (verduras, vísceras, hígado).
            margenes_categoria["Carne muscular"] = (mn_carne, min(0.95, mx_carne + mx_hueso))
        fila_total = fila_vacia()
        for n in nombres:
            if categoria_de[n] != "Suplementos":
                fila_total[idx[n]] = 1.0
        for cat, (mnp, mxp) in margenes_categoria.items():
            miembros = [n for n in nombres if categoria_de[n] == cat]
            if not miembros:
                # ⚠️ CORREGIDO (5 agosto, noche) — FALLO GRAVE ENCONTRADO
                # por la usuaria: esto antes hacía "continue", saltándose
                # la restricción ENTERA en silencio si esta categoría se
                # quedaba sin ningún candidato disponible (por ejemplo,
                # tras aplicar exclusiones). Eso significaba que si
                # "Hueso carnoso" se quedaba sin candidatos, el mínimo del
                # 20% dejaba de exigirse del todo -- y el motor podía
                # devolver un menú SIN NINGÚN HUESO, marcado como
                # "factible" y "verde" (los 30 nutrientes no dicen nada
                # de los márgenes de categoría, así que verificar() no lo
                # pillaba). Si el mínimo de esta categoría es mayor que
                # cero y no hay NINGÚN candidato para cumplirlo, es
                # matemáticamente imposible cumplirlo -- así que ahora se
                # declara NO FACTIBLE de forma explícita y ruidosa, en
                # vez de fingir que no pasa nada.
                #
                # ⚠️ CORREGIDO (5 agosto, madrugada) — EXCEPCIÓN EXPLÍCITA
                # E INTENCIONAL: la protección de arriba es correcta para
                # el caso ACCIDENTAL (una combinación de exclusiones
                # individuales deja la categoría vacía sin que nadie lo
                # pidiera a propósito). Pero si la categoría está en
                # categorias_excluidas -- exclusión EXPLÍCITA de la
                # categoría entera, pedida a propósito (ver el bloque más
                # arriba que vacía "disp" para esta categoría) -- vaciarla
                # es justo lo que se pidió, así que el mínimo debe
                # ignorarse en ESTE caso concreto, no fallar.
                if mnp and mnp > 0 and not (categorias_excluidas_efectivo and cat in categorias_excluidas_efectivo):
                    return False, None
                continue
            fila_cat = fila_vacia()
            for n in miembros:
                fila_cat[idx[n]] = 1.0
            # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL ENCONTRADO: el
            # redondeo de cada alimento a 2 decimales al construir el
            # resultado final (más abajo) puede desplazar el peso total
            # de una categoría unas centésimas de gramo respecto a lo
            # que el LP calculó internamente con precisión completa --
            # normalmente inofensivo, pero si el LP resuelve JUSTO en el
            # límite del margen (p.ej. exactamente 20.000% cuando el
            # mínimo es 20%), ese redondeo posterior puede empujarlo a
            # 19.98% y salir fuera de rango pese a que el LP lo resolvió
            # bien. Mismo principio que el +0.8% que ya se aplica a los
            # mínimos de nutrientes: se pide un pelín más del mínimo y
            # un pelín menos del máximo, para que quede colchón real.
            mnp_con_margen = mnp * 1.01 if mnp else mnp
            mxp_con_margen = mxp * 0.99 if mxp else mxp
            fila_rel_max = [fila_cat[j] - mxp_con_margen * fila_total[j] for j in range(2 * n_var)]
            _fila("margen_categoria_max", fila_rel_max, -np.inf, 0.0)
            fila_rel_min = [-fila_cat[j] + mnp_con_margen * fila_total[j] for j in range(2 * n_var)]
            _fila("margen_categoria_min", fila_rel_min, -np.inf, 0.0)

    # ⚠️ AÑADIDO (5 agosto): grasa como % de las kcal (pancreatitis,
    # diabetes) -- restricción propia, no cabe en el bucle de arriba
    # porque compara contra las kcal totales, no contra un mínimo/máximo
    # por 1000kcal. grasa (g) x 9 kcal/g <= pct x der
    pct_grasa_max = pct_grasa_patologia
    if pct_grasa_max is not None:
        fila = fila_vacia()
        for n in nombres:
            g = (_num(alimentos[n].get("nutrientes", {}).get("grasa")) or 0.0) / 100.0
            fila[idx[n]] = g * 9.0
        _fila("grasa_patologia_absoluto", fila, -np.inf, pct_grasa_max * der)

        # ⚠️ AÑADIDO (24 agosto) — CASO REAL MEDIDO: en pancreatitis, con
        # el tope de grasa en el 25% de las kcal, el menú salía al 26%. En
        # diabetes, con el tope en 35%, salía al 36%. En LOS CUATRO pesos
        # probados, siempre por encima.
        #
        # Es exactamente el mismo fallo que se arregló el 21 de agosto para
        # los topes por 1000 kcal (fósforo renal: tope 1400, salía 1426), y
        # a este camino no le llegó: la fila de arriba compara contra las
        # kcal OBJETIVO (`der`), pero el menú entregado puede tener hasta
        # un 3% menos (tolerancia_kcal). Menos kcal con la misma grasa =
        # mayor porcentaje. Y el tope se mide sobre la dieta REAL, que es
        # la que se come.
        #
        # Se añade el mismo tope sobre las kcal de verdad, que también es
        # lineal:
        #     suma(grasa_i * 9 * g_i)  <=  pct * suma(kcal_i * g_i)
        #   → suma((grasa_i * 9 - pct * kcal_i) * g_i)  <=  0
        #
        # La fila absoluta de arriba se deja: cuando el menú sale con MÁS
        # kcal de las pedidas, es ella la que aprieta. Con las dos, manda
        # siempre la más estricta.
        # Mismo margen de redondeo que en los topes por 1000 kcal: el
        # solver resuelve exacto en el límite y el redondeo de los gramos a
        # 2 decimales lo empuja por encima (medido: 0,2500x contra 0,25).
        # Este tope siempre viene de una patología, así que siempre aplica.
        pct_rel = pct_grasa_max * (1 - 0.001)
        fila_rel = fila_vacia()
        for n in nombres:
            g = (_num(alimentos[n].get("nutrientes", {}).get("grasa")) or 0.0) / 100.0
            kcal_n = (alimentos[n].get("energia", 0) or 0.0) / 100.0
            coef = g * 9.0 - pct_rel * kcal_n
            if coef:
                fila_rel[idx[n]] = coef
        _fila("grasa_patologia_relativo", fila_rel, -np.inf, 0.0)

    # 4. VINCULACIÓN gramos <= usa * techo (y gramos >= 0, ya en bounds)
    for n in nombres:
        i = idx[n]
        fila = fila_vacia()
        fila[i] = 1.0
        fila[n_var + i] = -techos[i]
        _fila("vinculacion_usa_techo", fila, -np.inf, 0.0, alimento=n)

    # 4-bis. Y AL REVÉS: si un alimento se usa, que sea una cantidad que se
    # pueda PESAR.
    #
    # ⚠️ AÑADIDO (24 agosto) — CASO REAL MEDIDO: salían 0,35 g de sal
    # común. Una báscula de cocina normal mide de gramo en gramo, así que
    # eso no lo pesa nadie en casa: o se pone de más o se pone de menos, y
    # justo esa sal era la que cerraba el cloruro del menú.
    #
    # NO se arregla redondeando el resultado: cambiar los gramos después
    # de resolver cambia los nutrientes, y toda la app se sostiene sobre
    # que las cifras cuadran de verdad. Se arregla aquí: si el motor va a
    # usar un alimento, que use una cantidad medible, y si no le cuadra,
    # que use otra cosa.
    #
    # Solo en EXTRAS, y no por pereza: medido sobre 51 menús (todos los
    # tamaños, etapas, patologías y exclusiones), las ÚNICAS cantidades por
    # debajo de un gramo salían de ahí -- la sal. Las carnes, vísceras y
    # verduras nunca bajaban de ~1,9 g, así que ponerles suelo no arregla
    # nada y sí cuesta: cada fila de éstas ata una variable continua a una
    # binaria y le da trabajo de más al solver. Medido con el suelo en TODO
    # el catálogo, /menu/varios-perros pasaba de ~7s a ~11s con el
    # presupuesto en 24s -- en Render, que va más lento que esto, eso se
    # puede llevar por delante un menú de la semana. No compensa.
    #
    # Y NUNCA en los suplementos comerciales: no se pesan, se dosifican con
    # el cacito o el comprimido que trae el bote (la app ya convierte los
    # gramos a fracciones de comprimido, ver formatearComprimidos).
    # Ponerles suelo sería obligar a dar de más de un suplemento, que es
    # justo lo que no se puede hacer.
    #
    # Es la fila espejo de la de arriba: gramos_i >= minimo * usa_i.
    #
    # ⚠️ CORREGIDO (24 agosto) — ESTA FILA ERA CÓDIGO MUERTO. Decía
    # `categoria_de.get(n) != "Extras"`, y `categoria_de` NO es la categoría
    # del alimento: es la CLAVE del diccionario de candidatos. Los aceites,
    # la sal, las semillas y el huevo entran como candidatos bajo la clave
    # genérica "Suplementos" (ver SUP_CATS, que mete "Extras" ahí dentro), y
    # ACCESIBLES no tiene ninguna clave "Extras". O sea que la condición
    # nunca se cumplía para NADIE y la fila no se añadía ni una vez: el
    # suelo de 1 g llevaba sin existir desde que se escribió.
    #
    # Es LA MISMA trampa que ya cazó el límite de 2 suplementos unos cientos
    # de líneas más abajo, y por lo mismo: comparar la clave genérica contra
    # una categoría real. Se arregla igual, mirando la categoría REAL en el
    # catálogo. Si alguien añade otra fila que dependa de la categoría de un
    # alimento: `alimentos[n]["categoria"]`, nunca `categoria_de[n]`.
    #
    # Lo encontró BLOQUE 14 fallando 1 de cada 20 veces en el caso más
    # apretado (200 kcal con cuatro especies fuera): 0,55 g de aceite de
    # girasol. Se veía poco porque solo asoma cuando el menú va justo.
    # ⚠️ AMPLIADO (29 agosto) — EL SUELO SOLO CUBRÍA LOS EXTRAS, Y LA
    # COMIDA TAMBIÉN SE PESA. Aquí ponía `!= "Extras"`, con esta razón
    # escrita al lado: "medido sobre 51 menús, las ÚNICAS cantidades por
    # debajo de un gramo salían de ahí -- la sal. Las carnes, vísceras y
    # verduras nunca bajaban de ~1,9 g".
    #
    # No era verdad, solo era raro: el canario del BLOQUE 14 sacó **0,69 g
    # de salmón** en un adulto de 200 kcal. Que en 51 menús no asomara no
    # significa que no pueda pasar -- significa que hacen falta más de 51.
    # Y una báscula de cocina normal mide de gramo en gramo, así que 0,69 g
    # de salmón no lo pesa nadie, exactamente igual que los 0,35 g de sal
    # que hicieron nacer esta restricción.
    #
    # LO QUE QUEDA FUERA SIGUEN SIENDO LOS SUPLEMENTOS COMERCIALES, y por
    # el mismo motivo de siempre: no se pesan, se dosifican con el cacito o
    # el comprimido del bote. Obligarles a llegar a 1 g sería obligar a dar
    # de más de un suplemento. Antes esa exención se escribía "todo menos
    # Extras", que dejaba fuera de la protección a las 116 fichas de
    # comida; ahora se escribe al revés y se nombra lo que de verdad se
    # dosifica.
    #
    # El coste medido (mediana de 6 generaciones por perfil, este mismo
    # equipo) está en el PR: si alguien lo vuelve a tocar por tiempo, que
    # mida en vez de suponer -- es lo que falló la primera vez.
    SUELO_MEDIBLE_G = 1.0
    CATEGORIAS_QUE_SE_DOSIFICAN = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                                   "Calcio", "Hierro", "Vitamina B")
    for n in nombres:
        if alimentos[n].get("categoria") in CATEGORIAS_QUE_SE_DOSIFICAN:
            continue
        i = idx[n]
        # Nunca por encima de su propio techo: si un alimento no puede
        # llegar a 1 g, el suelo lo dejaría fuera del catálogo entero.
        suelo = min(SUELO_MEDIBLE_G, techos[i])
        if suelo <= 0:
            continue
        fila = fila_vacia()
        fila[i] = 1.0
        fila[n_var + i] = -suelo
        _fila("suelo_medible", fila, 0.0, np.inf, alimento=n)

    # 5. CUÁNTOS ALIMENTOS DISTINTOS por categoría (máx.)
    for cat, tope in cuantos_max.items():
        miembros = [n for n in nombres if categoria_de[n] == cat]
        if not miembros:
            continue
        fila = fila_vacia()
        for n in miembros:
            fila[n_var + idx[n]] = 1.0
        _fila("max_por_categoria", fila, 0, tope)

    # 6. MÁXIMO DE SUPLEMENTOS (solo los COMERCIALES cuentan para el
    # límite de "2" — los aceites/huevos de Extras no son "un suplemento"
    # en el sentido de producto de marca, cuentan aparte en el peso)
    SUP_COMERCIALES = ("Multivitamínico", "Omega-3", "Yodo", "Fibra",
                       "Calcio", "Hierro", "Vitamina B")
    # ⚠️ CORREGIDO (5 agosto, tarde) — FALLO GRAVE ENCONTRADO por la
    # batería de pruebas: esto comparaba categoria_de[n] (que vale
    # literalmente el texto genérico "Suplementos" para CUALQUIER
    # suplemento, es la clave del diccionario de candidatos, no la
    # categoría real del alimento) contra SUP_COMERCIALES (que tiene
    # categorías específicas como "Multivitamínico"). La condición NUNCA
    # era cierta, así que esta fila de restricción se quedaba a CEROS —
    # "0 ≤ 2" siempre, sin importar cuántos suplementos hubiera de
    # verdad. El límite de 2 llevaba SIN aplicarse matemáticamente desde
    # que se creó este archivo, no solo desde hoy: dependía por completo
    # de que el objetivo (minimizar alimentos) tendiera a pocos por
    # casualidad, sin ninguna garantía dura detrás. Ahora se consulta la
    # categoría REAL del alimento en el catálogo, no la clave genérica.
    fila = fila_vacia()
    for n in nombres:
        if alimentos[n].get("categoria") in SUP_COMERCIALES:
            fila[n_var + idx[n]] = 1.0
    _fila("max_suplementos", fila, 0, max_suplementos)

    # 6b. EXTRAS + SUPLEMENTOS JUNTOS, MÁXIMO 5% DEL PESO (decisión de la
    # usuaria 5 agosto: "los extras, suplementos también entrando dentro
    # de extras, no pueden superar un cinco por ciento").
    fila_total_con_sup = fila_vacia()
    for n in nombres:
        fila_total_con_sup[idx[n]] = 1.0
    fila_extras = fila_vacia()
    for n in nombres:
        if categoria_de[n] == "Suplementos":
            fila_extras[idx[n]] = 1.0
    fila_5pc = [fila_extras[j] - 0.05 * fila_total_con_sup[j] for j in range(2 * n_var)]
    _fila("extras_y_suplementos_5pc", fila_5pc, -np.inf, 0.0)

    constraints = LinearConstraint(np.array(A_rows), np.array(lb_rows), np.array(ub_rows))
    integrality = np.array([0] * n_var + [1] * n_var)   # 0=continua, 1=entera(binaria)
    bounds = Bounds(lb=[0.0] * n_var + [0] * n_var, ub=[np.inf] * n_var + [1] * n_var)

    # FORZAR: el alimento tiene que estar sí o sí (usa_i >= 1, o sea = 1)
    # ⚠️ CORREGIDO (5 agosto, mañana) — CASO REAL: la usuaria forzó "Pollo
    # muslo con piel" Y "Carcasa de pollo", y la carcasa desapareció del
    # menú final aunque la restricción "forzar" se cumplía matemáticamente.
    # La causa: forzar solo fijaba la variable BINARIA (usa=1), pero no
    # exigía una cantidad de gramos mínima -- así que el resolver podía
    # cumplir "se usa" con una cantidad ridícula (1-2 gramos), y entonces
    # desaparecía del resultado aunque "estuviera forzado".
    #
    # ⚠️ SEGUNDO FALLO ENCONTRADO Y CORREGIDO EN EL MISMO MOMENTO: el
    # primer intento de arreglo usaba "3% de las kcal del día" como
    # mínimo -- pero para un alimento con MUY pocas kcal por 100g (una
    # verdura, una hierba), eso se traduce en una cantidad de PESO
    # enorme (207 g de albahaca, en este caso real), que rompía el
    # margen máximo de peso de su categoría (Verduras y frutas: 10%).
    # Mezclaba kcal y peso sin darse cuenta -- el mismo tipo de error que
    # ya habíamos visto antes con el reescalado del catálogo. Ahora el
    # mínimo es un peso pequeño y FIJO (10 g), sin relación con las kcal
    # del alimento: suficiente para que sea una porción real y visible,
    # nunca tan grande como para poder romper ningún margen.
    #
    # ⚠️ AMPLIADO (5 agosto, madrugada) — CASO REAL: con ese mínimo
    # único de 10 g, cuando se fuerzan VARIOS alimentos de Carne
    # muscular a la vez (el mecanismo de "preservar todo al editar"
    # hace esto a menudo), el resolver podía repartir la carne entre
    # todos ellos dándole a cada uno justo esos 10 g -- técnicamente
    # "presentes", pero una cantidad ridícula que no representa una
    # porción real. 10 g de sal o de un extra es razonable; 10 g de
    # carne muscular no lo es. Ahora el mínimo depende de la categoría:
    # más alto para las proteínas de verdad (carne, pescado, hueso),
    # bajo para lo que sí suele darse en cantidades pequeñas (vísceras,
    # hígado, por su propio límite de dosis) o en extras/suplementos.
    MINIMO_POR_CATEGORIA = {
        "Carne muscular": 40.0,
        "Pescados y mariscos": 40.0,
        "Hueso carnoso": 25.0,
        "Verduras y frutas": 15.0,
    }
    # ⚠️ CORREGIDO (20 agosto) — CASO REAL ENCONTRADO AUDITANDO: estos
    # mínimos son FIJOS en gramos, y eso no puede ser: "una porción real
    # y visible" depende del tamaño del perro. En un perro de 20 kg el
    # menú entero son ~674 g y 40 g de pescado es una porción normal. En
    # uno de 3 kg el menú entero son ~137 g, así que esos mismos 40 g son
    # el 29% de la ración de golpe -- y en uno de 1,5 kg (73 g de menú)
    # serían más de la mitad. Medido: añadir sardina a un perro de 3 kg
    # fallaba SIEMPRE, con y sin alergias, y el mensaje decía "no existe
    # ninguna combinación", cuando lo que no existía era una que metiera
    # 40 g de sardina en un perro tan pequeño.
    #
    # El mínimo se topa ahora por el tamaño real de la ración. Los menús
    # reales pesan ~0,6 g por kcal (medido sobre 21 combinaciones de peso
    # y etapa), así que se limita a un 15% de esa ración estimada. Para
    # un perro mediano o grande no cambia nada -- el tope queda muy por
    # encima de los 40 g; solo actúa donde estaba el problema.
    tope_porcion_del_perro = 0.15 * 0.6 * der
    if forzar:
        for n in forzar:
            if n not in idx:
                continue  # no es un candidato válido; se ignora sin romper
            i = idx[n]
            minimo = MINIMO_POR_CATEGORIA.get(categoria_de.get(n), 10.0)
            minimo = min(minimo, tope_porcion_del_perro)
            bounds.lb[n_var + i] = 1
            bounds.lb[i] = min(minimo, techos[i])

    # ─── GRAMOS FIJOS: LO QUE EL VETERINARIO YA HA DECIDIDO ──────────────
    #
    # ⚠️ AÑADIDO (29 agosto) para el formulador del profesional. `forzar`
    # dice "que esté"; esto dice "que esté EXACTAMENTE en esta cantidad", y
    # el motor completa el resto de la ración alrededor. Es la diferencia
    # entre elegir ingredientes y formular: un veterinario pone 300 g de
    # pechuga porque ha decidido 300, no "algo de pechuga".
    #
    # Se implementa como el límite superior E inferior de la variable, que es
    # exactamente lo que significa. No toca ninguna restricción nutricional:
    # los 41 requisitos, el ratio Ca:P, los topes de seguridad crónica y los
    # de patología siguen siendo los mismos y se cumplen o no se entrega
    # menú. O sea que fijar una cantidad puede hacer el problema INFACTIBLE,
    # y tiene que poder hacerlo -- si alguien clava 400 g de hígado, lo que
    # hay que decirle es que no cabe, no darle un menú tóxico.
    #
    # El caso que sí conviene distinguir es cuando la cantidad fijada se pasa
    # ella sola de un tope de seguridad: ahí el infactible genérico ("no
    # existe combinación") es verdad pero inútil, porque la combinación no
    # existe POR ESE ALIMENTO. Se dice cuál y cuánto cabe.
    if gramos_fijos:
        for n, g in gramos_fijos.items():
            if n not in idx:
                continue
            try:
                g = float(g)
            except (TypeError, ValueError):
                continue
            if g <= 0:
                continue
            i = idx[n]
            bounds.lb[i] = g
            bounds.ub[i] = g
            bounds.lb[n_var + i] = 1     # y cuenta como usado

    # objetivo: minimizar cuántos alimentos distintos se usan en total
    # (ración simple, no 20 ingredientes), PERO con coste menor para los
    # que el usuario quiere aprovechar — así el resolver los prefiere
    # cuando dos soluciones son igual de válidas, sin obligarlos.
    #
    # ⚠️ AÑADIDO (5 agosto): el motor era determinista -- mismos datos,
    # mismo menú, siempre. Bien para fiabilidad, mal para variedad: pedir
    # el menú de un mismo perro dos veces daba idéntico resultado, y con
    # varios menús a la vez, sin rotar, salía siempre el mismo. Se añade
    # un ruido aleatorio PEQUEÑO al coste de cada alimento (no a las
    # restricciones nutricionales, esas no se tocan) para que, cuando hay
    # varias combinaciones igual de válidas, el motor no elija siempre la
    # misma. Con una semilla, se puede repetir el mismo resultado a
    # propósito (para depurar); sin ella, cada llamada es distinta.
    coste_binaria = [1.0] * n_var
    if preferir:
        for n in preferir:
            if n in idx:
                coste_binaria[idx[n]] = 0.1   # mucho más barato usarlo
    if semilla_aleatoria is not False:
        rng = np.random.RandomState(semilla_aleatoria)  # None = aleatorio de verdad cada vez
        for i in range(n_var):
            coste_binaria[i] += rng.uniform(0.0, 0.4)
        # ⚠️ AÑADIDO (5 agosto, mediodía) — CASO REAL: el pescado salía
        # SIEMPRE en la práctica (8/8 en la prueba), no "casi siempre"
        # como se pensaba. Su ventaja real en EPA/DHA es tan grande que
        # el ruido pequeño de arriba nunca bastaba para que ganara otra
        # cosa. La mitad de las veces (al azar), se penaliza un poco el
        # pescado en el objetivo -- así, cuando SÍ hay una alternativa
        # nutricionalmente válida sin pescado, el resolver la prefiere en
        # esa mitad de los casos. Nunca afecta a si el menú es correcto:
        # solo influye en qué alimento igual de válido se elige.
        #
        # ⚠️ CORREGIDO (26 agosto) — CASO REAL ENCONTRADO midiendo el
        # BLOQUE 17: al regenerar pidiendo conservar los alimentos, el
        # segundo menú perdía el suyo 1 de cada 12 veces, y el alimento
        # que se caía era SIEMPRE un pescado ("PERDIDOS: ['Boquerón']",
        # "PERDIDOS: ['Bacalao']"). La cuenta lo explica: un pescado
        # preferido cuesta 0,1 + ruido = 0,1-0,5, pero con esta
        # penalización pasa a 1,6-2,0 -- MÁS que un alimento cualquiera
        # que no se pidió (1,0-1,4). O sea que la penalización de
        # variedad se comía la preferencia del usuario y el motor
        # cambiaba justo lo que se le había pedido no cambiar.
        #
        # La penalización está para dar variedad cuando el motor elige
        # LIBREMENTE. Si el usuario ha dicho "quiero estos alimentos",
        # ahí no hay nada que variar: se respeta lo que pidió.
        if rng.random() < 0.5:
            preferidos = set(preferir or ())
            for n in nombres:
                if categoria_de[n] == "Pescados y mariscos" and n not in preferidos:
                    coste_binaria[idx[n]] += 1.5
    # ⚠️ AÑADIDO (5 agosto, madrugada) — CASO REAL: la rotación de
    # proteína entre varios menús automáticos EXCLUÍA por completo la
    # especie del menú anterior (especies_excluidas). Eso es una
    # restricción DURA e invisible para el usuario -- él nunca pidió
    # evitar esa especie, es una decisión interna para dar variedad. Si
    # esa especie resultaba ser la única forma razonable de cerrar los
    # 30 requisitos con este perro concreto, la exclusión dura podía
    # volver el problema mucho más difícil o directamente imposible, y
    # el usuario veía "no existe combinación" sin haber pedido nada raro.
    # Ahora, igual que con el pescado, solo se PENALIZA en el objetivo
    # -- el motor la evita si puede, pero nunca puede fallar por esto.
    if evitar_especies:
        evitar_lower = {e.strip().lower() for e in evitar_especies}
        for n in nombres:
            if categoria_de[n] in ("Carne muscular", "Pescados y mariscos", "Hueso carnoso",
                                   "Vísceras", "Hígado"):
                if especie_de(n).strip().lower() in evitar_lower:
                    coste_binaria[idx[n]] += 2.0
    c = np.array([0.0] * n_var + coste_binaria)

    # ⚠️ AÑADIDO (5 agosto, noche) — CASO REAL ENCONTRADO: cachorro pequeño
    # + alergia al pollo tardaba 72-75 segundos, siempre, de forma
    # constante. La causa: milp() sin límites intentaba DEMOSTRAR que la
    # solución encontrada era la óptima exacta (mínimo número de alimentos
    # distintos posible), no solo encontrar UNA que funcione. Esa prueba
    # de optimalidad exacta es la parte cara del problema, no encontrar
    # una solución valida. El objetivo (menos alimentos distintos) es un
    # capricho de presentación, no un requisito nutricional: conformarse
    # con estar cerca del óptimo (1%) es indistinguible para el usuario y
    # muchísimo más rápido.
    #
    # ⚠️ SUBIDO (5 agosto, madrugada) — CASO REAL: restringir a una sola
    # especie (personalizar, "todo el/la X") es un problema genuinamente
    # más difícil, y en el servidor real (más lento que este entorno de
    # pruebas) cada intento individual puede tardar mucho más -- dejando
    # sitio para MENOS reintentos dentro del mismo presupuesto de 18s.
    # Subido de 0.15 a 0.30: acepta una solución un poco menos "óptima"
    # en cuanto a minimizar cuántos alimentos distintos usa (un capricho
    # de presentación, no nutricional), a cambio de que cada intento
    # tarde bastante menos -- así caben más reintentos en el mismo
    # tiempo, sin tocar en absoluto la corrección nutricional, que sigue
    # siendo exacta (el gap no afecta a ninguna restricción, solo a la
    # prueba de que el objetivo es el mínimo posible).
    res = milp(c, constraints=constraints, integrality=integrality, bounds=bounds,
              options={"time_limit": time_limit, "mip_rel_gap": 0.30})

    # ⚠️ SE ACEPTA LA SOLUCIÓN AUNQUE SE ACABE EL TIEMPO (29 agosto), Y ESTO
    # ES LO QUE MÁS MENÚS DEVUELVE DE TODO LO QUE SE HA TOCADO HOY.
    #
    # `res.success` solo es cierto con status 0: "óptimo demostrado". Cuando
    # salta el time_limit, el estado es 1 -- y HiGHS YA TIENE una solución
    # entera factible guardada, que aquí se estaba tirando a la basura.
    #
    # MEDIDO, con el límite apretado a mano para imitar lo lento que va
    # Render (este equipo resuelve en 2-6 s; allí, 12-24 s):
    #
    #     time_limit  caso            status  ¿había solución?  se devolvía
    #     1 s         mestiza 20 kg     1           SÍ             nada
    #     1 s         cachorro 4 meses  1           SÍ             nada
    #     2 s         cachorro 4 meses  1           SÍ             nada
    #     3 s         toy 1,5 kg        1           SÍ             nada
    #
    # O sea que parte de los "el cálculo está tardando más de lo normal" de
    # producción eran menús QUE EXISTÍAN, ya calculados, tirados por no
    # haber terminado de demostrar que no había otro con un alimento menos.
    #
    # Y eso es exactamente lo que se puede soltar: el objetivo del MILP es
    # "usar los menos alimentos distintos posible", que es comodidad de
    # cocina. Las restricciones -- los 41 requisitos, el ratio Ca:P, los
    # cinco topes de seguridad crónica, los topes por patología, las
    # proporciones -- las cumple CUALQUIER solución factible, óptima o no.
    # Con el gap del 30 % que ya se aceptaba, la diferencia práctica es
    # como mucho un alimento más en la lista.
    #
    # La red de seguridad de las categorías (aquí abajo) y
    # `_garantizar_verificado` en main.py siguen mirando el resultado REAL,
    # así que nada de esto puede entregar un menú que no cumpla.
    hay_solucion = res.success or (getattr(res, "x", None) is not None
                                   and res.status == 1)

    if hay_solucion:
        x = res.x[:n_var]
        # ⚠️ CORREGIDO (5 agosto, mañana): el umbral de 0.5g podía borrar
        # del resultado un aporte PEQUEÑO PERO REAL y necesario -- por
        # ejemplo, el yoduro potásico funciona en dosis de fracciones de
        # gramo. Si el LP decidía que 0.3g de yoduro cerraban el yodo,
        # ese 0.3g desaparecía del diccionario final por el filtro,
        # dejando el yodo sin cerrar en el menú que de verdad se enseña,
        # aunque el LP internamente SÍ lo había resuelto bien. Bajado a
        # 0.02g -- bajo el umbral de lo que se puede pesar en casa, pero
        # sin perder aportes reales de suplementos muy concentrados.
        gramos = {n: round(x[idx[n]], 2) for n in nombres if x[idx[n]] > 0.02}

        # ⚠️ AÑADIDO (5 agosto, madrugada) — RED DE SEGURIDAD FINAL: caso
        # real de la usuaria, un menú de solo 4 alimentos (carne, víscera,
        # hígado, suplemento) SIN hueso ni verdura, aceptado como válido.
        # No se ha conseguido reproducir la causa exacta pese a más de 40
        # intentos dirigidos -- puede ser una imprecisión numérica del
        # propio solver en combinación con pesos muy desiguales entre
        # alimentos. En vez de seguir cazando la causa exacta, esto
        # comprueba el RESULTADO REAL (los gramos que se van a enseñar,
        # no la restricción teórica) antes de devolverlo: si a una
        # categoría con mínimo obligatorio le falta representación de
        # verdad, se rechaza aquí, pase lo que pase por dentro del LP.
        if margenes_categoria:
            for cat, (mnp, _mxp) in margenes_categoria.items():
                if not mnp or mnp <= 0:
                    continue
                # ⚠️ CORREGIDO (5 agosto, madrugada) — mismo motivo que la
                # excepción de arriba: si esta categoría se excluyó a
                # propósito (categorias_excluidas), no tiene sentido
                # exigirle representación aquí tampoco -- esta red de
                # seguridad final debe respetar la misma excepción, o
                # anula por su cuenta lo que ya se permitió arriba.
                if categorias_excluidas_efectivo and cat in categorias_excluidas_efectivo:
                    continue
                if not any(alimentos[n].get("categoria") == cat for n in gramos):
                    return False, None

        return True, gramos
    return False, None
