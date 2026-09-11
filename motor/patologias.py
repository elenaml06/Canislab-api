# -*- coding: utf-8 -*-
"""
LOS TOPES POR PATOLOGÍA, QUE AHORA SON DATOS.

Hasta el 28 de agosto esta tabla era un `dict` de 200 líneas dentro de
`motor_completo.py`, mezclando cuatro cosas que no se parecen: los números,
el motivo clínico de cada número, los textos que lee el usuario y la lógica
de qué pasa en crecimiento.

Se saca por lo mismo que se sacaron los menús del catálogo y la tabla de
FEDIAF: **un número que decide si un menú se entrega tiene que poder
auditarse**, y no se puede auditar lo que está enterrado entre `if`s. La
tabla de FEDIAF tiene `auditar_fediaf.py` desde el 25 de agosto y por eso
sabemos que sus 43 filas cuadran con el PDF. Esta no tenía nada.

⚠️ LO QUE VIGILA `auditar_patologias.py` (BLOQUE 32), y por qué cada cosa:

  1. Cada cifra con su FUENTE y su POR QUÉ. Es la regla del catálogo entero.
  2. Ninguna patología FORMULABLE puede tener un tope por debajo del mínimo
     de FEDIAF. Si lo tiene, no es un tope: es una dieta de prescripción, y
     entonces va con `formulable: false`. Medido: de las 47 patologías que
     propuso la revisión clínica, SIETE cifras estaban por debajo del
     mínimo -- fósforo 800 en IRIS 3, cobre 1,8 en hepatopatía, proteína 35.
     No eran errores: eran dietas terapéuticas mezcladas con topes normales
     en el mismo campo, y así no se distinguen.
  3. Que la clave del nutriente EXISTA en el MAPA del verificador. Es el
     fallo de la fibra otra vez: una fila que el motor no mira nunca porque
     su clave no está en el mapa, y nadie se entera porque el menú sale
     verde igual.
  4. Que soltar un tope en crecimiento venga SIEMPRE con su aviso. Regla 5
     del CLAUDE.md: se puede bajar de peldaño, pero se dice.

El motor sigue viendo exactamente la misma forma de diccionario que antes:
este módulo la reconstruye al cargar, así que `topes_de_patologias()`,
`patologias_bloquean()` y `avisos_de_patologias()` no se han tocado.
"""
import json, os

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RUTA = os.path.join(_AQUI, "..", "patologias.json")


def cargar_crudo(ruta=None):
    """El JSON tal cual, con fuentes y motivos. Lo usa la auditoría."""
    with open(ruta or _RUTA, encoding="utf-8") as f:
        return json.load(f)


def _a_forma_del_motor(crudo):
    """Reconstruye el dict que el solver espera, sin metadatos.

    La forma del motor es la que era: valores desnudos. Los metadatos
    (fuente, por_que, motivo_no_formulable) no llegan aquí a propósito --
    el solver no tiene nada que hacer con ellos y mezclarlos volvería a
    poner la documentación dentro del cálculo, que es de lo que veníamos.
    """
    salida = {}
    for clave, p in crudo["patologias"].items():
        e = {}
        topes = {n: t["valor"] for n, t in (p.get("topes_por_1000kcal") or {}).items()}
        if topes:
            e["max_por_1000kcal"] = topes
        # ⚠️ AÑADIDO (7 septiembre) — LOS SUELOS, EL ESPEJO DE LOS TOPES.
        # Hasta hoy una patología solo podía ENDURECER un máximo (artrosis
        # quería más omega-3 que el mínimo normal, y no había manera de
        # pedirlo). `suelos_por_1000kcal` es exactamente `topes_por_1000kcal`
        # boca abajo: un mínimo reforzado, no un máximo rebajado. Mismas
        # reglas de auditoría, en espejo -- ver `auditar_patologias.py`.
        suelos = {n: t["valor"] for n, t in (p.get("suelos_por_1000kcal") or {}).items()}
        if suelos:
            e["min_por_1000kcal"] = suelos
        # ⚠️ AÑADIDO (10 septiembre) — QUE UNA PATOLOGÍA PUEDA PEDIR SU PROPIO
        # RATIO ENTRE DOS NUTRIENTES.
        #
        # Estuvo dos días escrito y sin aplicar, y el motivo era exactamente
        # este hueco: el motor sabe de ratios Ca:P desde el principio -- los
        # aplica desde FEDIAF y desde la nota b de raza grande -- pero no había
        # forma de que una PATOLOGÍA pidiera el suyo, así que la Tabla 40-5 del
        # oxalato («maintain a normal Ca:P ratio (1.1:1 to 2:1)») se quedó en
        # `ratio_ca_p` con `aplicado_por_el_solver: false`.
        #
        # ⚠️ Y NO ERA COSMÉTICO: medido antes de aplicarlo, el menú de un perro
        # de 30 kg con oxalato salía con Ca:P 1,06 -- por debajo del 1,1 de la
        # fuente -- y salía EN VERDE, porque el mínimo de FEDIAF en adulto es
        # 1,0 y el semáforo mide contra los requisitos de un perro SANO.
        #
        # Es genérico a propósito, y no por elegancia: un cociente entre dos
        # sumas de nutrientes es lineal igual que el Ca:P, así que el día que
        # se decida qué hacer con el omega-6:omega-3 -- que hoy vive en
        # `limites_escritos_que_el_solver_no_aplica` porque las fuentes se
        # contradicen (de <1:1 a 7:1 según la enfermedad) -- no hace falta
        # maquinaria nueva, solo mover la celda de bloque.
        #
        # EN `ratios` SOLO VA LO QUE SE APLICA. Lo que está escrito y no se
        # aplica vive en `limites_escritos_que_el_solver_no_aplica`, como todo
        # lo demás: una celda aquí que dijera `aplicado_por_el_solver: false`
        # sería un límite que parece un límite y no hace nada, que es el fallo
        # de la fibra y el de las categorías de Personalizar otra vez. Lo
        # rechaza `auditar_patologias.py`.
        ratios = []
        for nombre_r, r in (p.get("ratios") or {}).items():
            ratios.append({
                "clave": nombre_r,
                "numerador": r["numerador"],
                "denominador": r["denominador"],
                "sentido": r["sentido"],
                "valor": float(r["valor"]),
            })
        if ratios:
            e["ratios"] = ratios
        cond = p.get("max_pct_kcal_grasa_si_ademas")
        if cond:
            e["max_pct_kcal_grasa_si_ademas"] = (cond["valor"], tuple(cond["requiere"]))
        # ⚠️ AÑADIDO (8 septiembre) — UN TOPE ABSOLUTO QUE SOLO APLICA CON OTRA
        # PATOLOGÍA MARCADA. Ya existía para el % de kcal de grasa (arriba);
        # faltaba para los topes normales, y hacía falta por un caso concreto:
        # SACN5 Tabla 67-3 GRADÚA la grasa de la pancreatitis -- «≤15% for
        # non-obese and non-hypertriglyceridemic dogs» y «≤10% for obese and/or
        # hypertriglyceridemic dogs» --, o sea 37,5 y 25. El motor solo aplicaba
        # el primero, así que un perro obeso con pancreatitis recibía el tope
        # del perro delgado. Mismo patrón, misma forma: (valor, patologías que
        # lo activan), por nutriente.
        cond_topes = p.get("topes_por_1000kcal_si_ademas")
        if cond_topes:
            e["max_por_1000kcal_si_ademas"] = {
                n: (t["valor"], tuple(t["requiere"])) for n, t in cond_topes.items()}
        # ⚠️ AÑADIDO (7 septiembre) — UN AVISO QUE SOLO SALTA POR LA
        # COMBINACIÓN, no por cada patología sola. Caso que lo motivó:
        # Fascetti & Delaney 2ª ed., cap.3, verificado contra el libro --
        # "weight loss is never a goal during treatment and recovery from
        # trauma and critical illness". `obesidad` sola es correcta; la
        # combinación con una patología aguda necesita decirlo. Mismo
        # patrón que `max_pct_kcal_grasa_si_ademas`, para texto en vez de
        # un número.
        aviso_cond = p.get("aviso_si_ademas")
        if aviso_cond:
            e["aviso_si_ademas"] = (aviso_cond["texto"], tuple(aviso_cond["requiere"]))
        for campo in ("solo_en_adulto", "en_crecimiento", "excluye_fruta",
                      "sin_dieta_automatica",
                      # ⚠️ LO DEL VETERINARIO (29 agosto). `formulable_por_
                      # profesional` dice si a un profesional acreditado se le
                      # formula; `necesita_bajo_fediaf` dice si para TRATAR de
                      # verdad haría falta bajar de un mínimo de FEDIAF, que es
                      # la frontera que exige firma (ver VETERINARIOS.md).
                      "formulable_por_profesional", "necesita_bajo_fediaf",
                      "nutriente_frontera", "objetivo_terapeutico_por_1000kcal"):
            if campo in p:
                e[campo] = p[campo]
        avisos = p.get("avisos") or {}
        if avisos.get("general"):
            e["aviso"] = avisos["general"]
        if avisos.get("crecimiento"):
            e["aviso_crecimiento"] = avisos["crecimiento"]
        if avisos.get("profesional"):
            e["aviso_profesional"] = avisos["profesional"]
        if avisos.get("profesional_crecimiento"):
            e["aviso_profesional_crecimiento"] = avisos["profesional_crecimiento"]
        # ⚠️ AÑADIDO (8 septiembre) — LOS AVISOS QUE NO SON NINGUNO DE ESOS
        # CUATRO. Hasta hoy `avisos` solo dejaba pasar «general»,
        # «crecimiento», «profesional» y «profesional_crecimiento»: cualquier
        # otra clave se cargaba del JSON y se quedaba aquí dentro, sin llegar
        # ni al menú ni a `GET /patologias`. O sea, texto escrito con su
        # fuente que no leía NADIE, y sin que saltara nada -- el menú sale
        # verde igual. Es el mismo fallo de la fibra, y el de las categorías
        # de Personalizar de las que solo se respetaban tres de las seis: una
        # cosa puesta a propósito que no hace nada y calla.
        #
        # Se descubrió al escribir la Tabla 31-3, que tiene tres avisos que
        # no son «el general»: que la fuente pide una o dos proteínas y no
        # más, que el omega-3 puede confundir la fase de diagnóstico, y por
        # qué se quitan el atún y la caballa. Los tres se habrían perdido.
        #
        # Van en una lista aparte y ORDENADA por su clave, para que el mismo
        # archivo dé siempre los mismos avisos en el mismo orden -- si
        # dependiera del orden del JSON, un reordenado cambiaría lo que lee
        # el usuario sin cambiar ni una palabra.
        _reservados = ("general", "crecimiento", "profesional", "profesional_crecimiento")
        extra = [avisos[k] for k in sorted(avisos) if k not in _reservados and avisos[k]]
        if extra:
            e["avisos_extra"] = extra
        salida[clave] = e
    return salida


CRUDO = cargar_crudo()
PATOLOGIAS = _a_forma_del_motor(CRUDO)
