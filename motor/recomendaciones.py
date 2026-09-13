# -*- coding: utf-8 -*-
"""
LOS TECHOS DEL LIBRO PARA EL PERRO SANO, QUE NO SON DE FEDIAF NI DE UNA PATOLOGÍA.

Hasta el 8 de septiembre de 2026 el motor solo conocía dos clases de límite:
los de **FEDIAF** (los 43 requisitos, que valen para cualquier perro) y los de
**patología** (más estrictos, y solo si esa patología está marcada). Faltaba una
tercera, y se veía en el resultado: SACN5 recomienda que el alimento de
CUALQUIER perro adulto sano no pase de 2000 mg de fósforo por 1000 kcal, y una
ración BARF de este motor salía con ~4000.

Ese número solo entraba por la puerta de atrás, en las dos patologías cuya
tabla lo repite —artrosis (1750) y reacción adversa al alimento (2000)—, que lo
llevan porque su población es de riesgo renal y no porque la enfermedad tenga
que ver con el fósforo. El resultado era incoherente: **el mismo perro pasaba de
4000 a 1750 por marcar «artrosis»**, y un perro sin nada se quedaba en 4000.

⚠️ POR QUÉ ESTO ES UN FICHERO Y NO CUATRO LÍNEAS EN `motor_completo.py`

Es la misma regla que sacó la tabla de patologías de dentro del código el 28 de
agosto: **un número que decide si un menú se entrega tiene que poder
auditarse**, y no se audita lo que está enterrado entre `if`s. Aquí no hay ni
una cifra: están en `recomendaciones_libro.json`, con su fuente, su cita
literal y el porqué, y las vigila el BLOQUE 57.

⚠️ Y POR QUÉ NO VAN EN NINGUNO DE LOS DOS FICHEROS QUE YA HABÍA

- En `requerimientos_v2_final.json` no, porque ese fichero **es** la Tabla
  III-3b de FEDIAF y `auditar_fediaf.py` comprueba sus 43 filas contra el PDF
  celda a celda. Meter ahí un número de un libro de texto es exactamente cómo se
  coló en agosto una fila «Fibra» con mínimo y máximo inventados.
- En `patologias.json` tampoco, porque esto **no es una patología**: se aplica
  al perro que no tiene ninguna.

⚠️ Y DESDE EL 9 DE SEPTIEMBRE NO SON SOLO DEL ADULTO (por eso el fichero ya
no se llama `recomendaciones_adulto.json`)

SACN5 le da al cachorro sus propias tablas —la 17-1 para cualquier cachorro y
la 33-5 para el de raza grande y gigante— y ahí hay techos que **no existen en
FEDIAF**: el de fósforo en crecimiento, sin ir más lejos, donde las dos columnas
de máximo de FEDIAF están vacías. Es el mismo agujero que el del fósforo del
adulto, un piso más abajo.

Y el del calcio del cachorro de raza grande no es un número feo en una ficha:
es enfermedad ortopédica del desarrollo. El cachorro no regula su absorción de
calcio como el adulto.

⚠️ HAY DOS UMBRALES DE «RAZA GRANDE» Y NO SON EL MISMO NÚMERO

- **15 kg** (`RAZA_GRANDE_O_GIGANTE_KG` en `motor_completo.py`) es el corte de
  las notas a y b de la Tabla III-3b de FEDIAF: decide el mínimo de calcio
  reforzado (2500) y el techo del ratio Ca:P (1,6).
- **25 kg** es el corte de SACN5 para la enfermedad ortopédica del desarrollo
  («large- and giant-breed puppies (>25 kg adult weight)», cap.33), y es el que
  parte en dos las columnas de la Tabla 17-1.

Dos fuentes, dos poblaciones, dos números. Unificarlos sería inventarse uno de
los dos, así que cada uno vive donde vive su fuente y este comentario está aquí
para que nadie los «arregle».

CÓMO SE COMBINA CON LO DEMÁS

Igual que un tope de patología: con `min()`, así que solo puede APRETAR. Si el
perro además tiene una patología cuya tabla pide menos fósforo (la renal pide
1200), manda la patología. Nunca al revés.
"""
import json
import os

_RUTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "recomendaciones_libro.json")

with open(_RUTA, encoding="utf-8") as _f:
    CRUDO = json.load(_f)

POR_ETAPA = CRUDO["por_etapa"]


def _topes_crudos(etapa, peso_adulto_esperado_kg=None):
    """Los techos escritos para esta etapa, ya combinados con los de raza grande.

    Devuelve `{clave: ficha}`. La sección `si_peso_adulto_esperado_supera_kg`
    solo entra si el perro llega al umbral, y entra con `min()`: como todo en
    este fichero, un techo solo puede APRETAR. Nunca puede aflojar el de la
    columna general por el hecho de ser un perro grande.
    """
    ficha = POR_ETAPA.get(etapa) or {}
    salida = dict(ficha.get("topes_por_1000kcal") or {})
    grande = ficha.get("si_peso_adulto_esperado_supera_kg") or {}
    umbral = grande.get("umbral_kg")
    if (umbral is not None and peso_adulto_esperado_kg
            and peso_adulto_esperado_kg >= umbral):
        for clave, t in (grande.get("topes_por_1000kcal") or {}).items():
            actual = salida.get(clave)
            if actual is None or t["valor"] < actual["valor"]:
                salida[clave] = t
    return salida


def topes_de_la_etapa(etapa, req=None, der_efectiva=None,
                      peso_adulto_esperado_kg=None, factor_premios=1.0):
    """Los techos del libro para esta etapa, en la forma que espera el solver.

    Devuelve `{clave_nutriente: valor}`, o `{}` si la etapa no tiene ninguno.

    Las etapas que NO tienen ninguno son gestación y lactancia: SACN5 les da su
    propia tabla (la 15-5 de la reproductora) que todavía no se ha transcrito.
    Que devuelvan `{}` es el lado seguro y no un olvido silencioso —lo vigila el
    BLOQUE 62—, pero está apuntado como pendiente.

    ⚠️ `peso_adulto_esperado_kg` NO ES OPCIONAL PARA UN CACHORRO, aunque lo
    parezca por la firma. Sin él, un cachorro de raza grande recibe el techo de
    calcio del cachorro pequeño (4250 en vez de 2750), que para él es papel
    mojado. Es exactamente el olvido que el 7 de septiembre dejó sin efecto el
    mínimo de calcio reforzado en la vía rápida de `/menu/v2`, y por eso los
    tres sitios que llaman a `_tope_patologia_roto` se lo pasan.

    ⚠️ Y CON `req` Y `der_efectiva`, EL TECHO CEDE ANTE EL MÍNIMO DE FEDIAF.

    CASO REAL, y lo cazó el BLOQUE 34 en la primera batería con esto puesto:
    **a DER 49 dejaba de salir menú**. No era un fallo del techo: es la
    aritmética que `CLAUDE.md` ya avisa en «los mínimos escalan hacia arriba,
    nunca hacia abajo». Cuando el perro come menos, el mínimo de FEDIAF SUBE
    (ecuación 7.2.5); los máximos NO, porque son concentración. Así que la
    ventana entre los dos se cierra según bajan las kcal:

        DER 95 (normal) .... mínimo de fósforo 1160, techo 2000 -> caben
        DER 56 ............. mínimo 1968, techo 2000 -> caben por 32 mg
        DER 55 ............. mínimo 2004, techo 2000 -> YA NO CABEN
        DER 49 ............. mínimo 2249, techo 2000 -> imposible

    **Y quien vive por debajo de 55 no es un caso raro: es el perro a dieta.**
    El 80 % del RER que recomienda AAHA para adelgazar sale a 56, justo en el
    borde, y un plan de pérdida de peso de verdad baja al 60-70 % del RER, que
    son 42-49. O sea que el techo del perro sano habría dejado sin menú
    exactamente al perro obeso.

    Cuando cruzan, **manda el mínimo de FEDIAF y el techo se cae**, por lo mismo
    que ninguna patología formulable puede tener un tope por debajo del mínimo
    (lo vigila `auditar_patologias.py`): el mínimo es un REQUISITO y este techo
    es una RECOMENDACIÓN, escrita además pensando en un alimento para un perro
    que come lo normal. Preferir la recomendación sería dejar al perro sin
    comida para cumplir un consejo.

    Sin `req` y `der_efectiva` se devuelven los techos tal cual. Es el lado
    estricto, y así quien no pueda calcular el mínimo escalado nunca aplica uno
    de más por accidente.

    ⚠️ Y EL MÍNIMO CONTRA EL QUE CEDE ES EL QUE DE VERDAD SE APLICA, NO EL DE LA
    FILA A SECAS (13 de septiembre de 2026).

    CASO REAL, EN PRODUCCIÓN, encontrado por Elena con su propio perro: Cairo,
    American Staffordshire, cachorro de casi 7 meses, 20 kg, al que va a pesar
    unos 31 de adulto. **No salía ningún menú en cuanto se declaraban premios**,
    y el mensaje decía «quita alguna restricción» — que no sirve de nada, porque
    no había ninguna que quitar.

    Se cruzaban DOS cifras de calcio, y las dos son correctas:

        suelo  2500   FEDIAF, Tabla III-3b nota b: cachorro que pasará de 15 kg
        techo  2750   SACN5 Tabla 17-1, columna del que pasará de 25 kg

    Entre las dos hay un 10 % de sitio, y los premios se lo comen: el motor
    formula la ración con las kcal QUE QUEDAN y le sigue exigiendo el día entero
    de nutrientes, así que el SUELO sube por `der/der_racion` y el techo no se
    mueve (regla 3-bis del CLAUDE.md).

        sin premios ...... 2500  cabe
        5 % .............. 2632  cabe, justo
        10 % ............. 2778  NO CABE   <- el techo que la propia fuente recomienda
        20 % ............. 3125  NO CABE

    Esta función YA sabía ceder — es su párrafo de arriba, el del perro a dieta
    — y no cedía aquí por dos motivos, los dos de la misma forma: **miraba un
    mínimo que no es el que el solver aplica.**

      1. `_minimo_de_fediaf` daba el 2000 de la fila «Calcio» y el solver usa el
         **2500 reforzado de la nota b** (`Calcio_LateGrowth_RazaGrande`).
      2. No sabía nada de los premios, que es justo lo que lo cruza.

    Con las dos puestas, manda FEDIAF y el techo del libro se cae — que es la
    regla escrita y no una excepción nueva: **el suelo es un REQUISITO y el
    techo una RECOMENDACIÓN**. Dejar al cachorro sin comida para cumplir un
    consejo es preferir el consejo al perro.

    ⚠️ `factor_premios` TIENE QUE VALER LO MISMO AQUÍ QUE EN EL SOLVER. Es
    `der / der_racion`, lo mismo que `_factor_premios` de `motor_completo`, y si
    los dos no lo calculan igual esta función y la restricción dirían cosas
    distintas — que es exactamente el fallo del 8 de septiembre con los suelos de
    patología. Lo vigila el BLOQUE 104.
    """
    salida = {}
    for clave, t in _topes_crudos(etapa, peso_adulto_esperado_kg).items():
        valor = t["valor"]
        if req is not None and der_efectiva is not None:
            minimo = suelo_que_de_verdad_se_aplica(
                req, clave, etapa, der_efectiva, peso_adulto_esperado_kg,
                factor_premios)
            if minimo is not None and minimo > valor:
                # El techo se cae. No en silencio: `cedidos_ante_fediaf` lo
                # cuenta, y de ahí sale el aviso que lee quien pide el menú.
                continue
        salida[clave] = valor
    return salida


def _suelos_crudos(etapa, peso_adulto_esperado_kg=None):
    """Los suelos escritos para esta etapa, combinados con los de raza grande.

    Mismo esquema que `_topes_crudos`, con el signo cambiado: un suelo de la
    columna de raza grande solo entra si APRIETA, o sea si es MAYOR.
    """
    ficha = POR_ETAPA.get(etapa) or {}
    salida = dict(ficha.get("suelos_por_1000kcal") or {})
    grande = ficha.get("si_peso_adulto_esperado_supera_kg") or {}
    umbral = grande.get("umbral_kg")
    if (umbral is not None and peso_adulto_esperado_kg
            and peso_adulto_esperado_kg >= umbral):
        for clave, s in (grande.get("suelos_por_1000kcal") or {}).items():
            actual = salida.get(clave)
            if actual is None or s["valor"] > actual["valor"]:
                salida[clave] = s
    # ⚠️ `aplicado_por_el_solver: false` — LA CIFRA ESTÁ ESCRITA Y EL MOTOR NO LA
    # APLICA, A PROPÓSITO. Es el mismo mecanismo con el que el Ca:P de los
    # urolitos estuvo dos días escrito antes de poder aplicarse, y existe para
    # que una cifra que HOY no cabe siga auditada —su conversión se rehace, su
    # cita se comprueba, el BLOQUE 57 la vigila— en vez de desaparecer del repo
    # y tener que volver a descubrirla dentro de seis meses.
    #
    # Hoy hay una: la vitamina E del perro sano (67,1 mg/1000 kcal). Cabe en el
    # perro normal y NO cabe en el pequeño ni con el catálogo muy recortado,
    # porque en el catálogo no hay un suplemento de vitamina E suelto. El porqué
    # entero, con los seis fallos que provocó y la medida, está en su `por_que`.
    return {c: s for c, s in salida.items()
            if s.get("aplicado_por_el_solver", True)}


def suelos_de_la_etapa(etapa, req=None, peso_adulto_esperado_kg=None):
    """Los SUELOS que el libro recomienda para esta etapa, para el solver.

    Devuelve `{clave_nutriente: valor}`, o `{}` si la etapa no tiene ninguno.

    ⚠️ ESTE FICHERO NO ERA SOLO DE TECHOS DESDE EL 11 DE SEPTIEMBRE DE 2026.
    Hasta entonces `recomendaciones_libro.json` solo guardaba máximos, y eso
    tenía una consecuencia que no se veía: **una recomendación del libro que
    fuera un MÍNIMO no tenía dónde vivir**. La vitamina E del perro sano es el
    caso: SACN5 la pide en ≥400 UI/kg MS en cinco capítulos distintos, y el
    motor la aplicaba en cuatro PATOLOGÍAS y no al perro que no tiene nada. O
    sea el mismo desajuste que tenía el fósforo antes del 8 de septiembre --
    el mismo perro pasaba de 7 a 67 mg por marcar «artrosis».

    ⚠️ Y AQUÍ MANDA FEDIAF, QUE ES LA REGLA.

    Un suelo del libro solo puede subir el mínimo DENTRO de la ventana de
    FEDIAF. Si el suelo que recomienda un libro se pasara del MÁXIMO de FEDIAF
    de ese mismo nutriente, el suelo **se cae** y se aplica FEDIAF: un máximo de
    FEDIAF es un requisito y esto es la recomendación de un libro de texto.
    Es la imagen en espejo de lo que ya hacía `topes_de_la_etapa` con el mínimo
    de FEDIAF, y está escrito aquí aunque hoy no se dispare con ninguna cifra
    --la vitamina E no tiene máximo en la Tabla III-3b-- porque el día que
    entre una que sí choque, la decisión no puede depender de que alguien se
    acuerde. `cedidos_ante_fediaf_por_arriba` lo cuenta para poder DECIRLO.

    ⚠️ Y AL REVÉS QUE LOS TECHOS, UN SUELO NO CEDE ANTE LA DER.
    Un techo del libro se cae cuando el mínimo de FEDIAF escalado lo supera,
    porque el perro que come poco necesita más concentración y el requisito
    manda. Un suelo no tiene ese problema: cuando el perro come menos, el
    mínimo de FEDIAF sube y este suelo se queda donde está, así que la
    combinación `max()` sigue siendo válida sin tocar nada. Por eso esta
    función no pide `der_efectiva` y la de los techos sí.
    """
    salida = {}
    for clave, s in _suelos_crudos(etapa, peso_adulto_esperado_kg).items():
        valor = s["valor"]
        if req is not None:
            maximo = _maximo_de_fediaf(req, clave, etapa)
            if maximo is not None and maximo < valor:
                continue
        salida[clave] = valor
    return salida


def cedidos_ante_fediaf_por_arriba(etapa, req, peso_adulto_esperado_kg=None):
    """Los suelos del libro que se han caído por pasarse del máximo de FEDIAF.

    Devuelve `[{clave, suelo, maximo_de_fediaf}]`. Hoy sale siempre vacío, y
    eso es lo que tiene que salir: ninguna de las cifras escritas choca. Existe
    por lo mismo que su hermana de los techos -- para que el día que una choque
    se pueda decir, en vez de que desaparezca en silencio.
    """
    fuera = []
    for clave, s in _suelos_crudos(etapa, peso_adulto_esperado_kg).items():
        maximo = _maximo_de_fediaf(req, clave, etapa)
        if maximo is not None and maximo < s["valor"]:
            fuera.append({"clave": clave, "suelo": s["valor"],
                          "maximo_de_fediaf": round(maximo, 1)})
    return fuera


def _maximo_de_fediaf(req, clave, etapa):
    """El máximo de FEDIAF de este nutriente, o None si no pone ninguno.

    Se pregunta a `verificar.maximo_de`, que es el único sitio que sabe de
    máximos --y el único que conoce `MAXIMOS_NO_APLICADOS`--, por lo mismo que
    `_minimo_de_fediaf` pregunta a `minimo_de`: repetir la lógica es como el
    motor y el analizador acabaron discrepando por la fibra.
    """
    from verificar import MAPA, maximo_de
    nombre = next((n for n, c in MAPA.items() if c == clave), None)
    if not nombre:
        return None
    fila = (req or {}).get(nombre)
    if not fila:
        return None
    return maximo_de(fila, nombre, etapa)


def cedidos_ante_fediaf(etapa, req, der_efectiva, peso_adulto_esperado_kg=None,
                        factor_premios=1.0):
    """Los techos que se han caído por cruzarse con el suelo que sí se aplica.

    Devuelve `[{clave, techo, minimo_de_fediaf, por_que}]`. Existe para poder
    DECIRLO: la regla 5 del CLAUDE.md es que se puede bajar de peldaño pero se
    dice, y esto es lo mismo un escalón más abajo -- un límite que estaba puesto
    y ha dejado de aplicarse a este perro concreto.

    ⚠️ Y HASTA EL 13 DE SEPTIEMBRE DE 2026 NO LA LLAMABA NADIE. Su propio
    comentario decía «el techo se cae, no en silencio: `cedidos_ante_fediaf` lo
    cuenta», y era falso: la función existía, estaba bien escrita y no la
    invocaba ni un endpoint. O sea que el techo SÍ se caía en silencio, que es
    justo lo que decía que no pasaba. Ahora la llama `_garantizar_verificado`,
    que es por donde pasa TODO menú.

    ⚠️ Y compara contra `suelo_que_de_verdad_se_aplica`, no contra la fila a
    secas: si mirara otro número diría que no ha cedido nada cuando sí, y un
    aviso que no salta es peor que no tenerlo.
    """
    fuera = []
    for clave, t in _topes_crudos(etapa, peso_adulto_esperado_kg).items():
        minimo = suelo_que_de_verdad_se_aplica(
            req, clave, etapa, der_efectiva, peso_adulto_esperado_kg,
            factor_premios)
        if minimo is not None and minimo > t["valor"]:
            fuera.append({"clave": clave, "techo": t["valor"],
                          "minimo_de_fediaf": round(minimo, 1),
                          "con_premios": factor_premios not in (None, 1.0),
                          "por_que": ("El suelo que FEDIAF exige a este perro "
                                      f"({minimo:.0f}) está por encima de este techo "
                                      f"({t['valor']:.0f}), que es una RECOMENDACIÓN del "
                                      "libro y no un requisito. Manda FEDIAF: el techo no "
                                      "se aplica a este perro. El máximo de seguridad de "
                                      "FEDIAF sigue puesto.")})
    return fuera


def _minimo_de_fediaf(req, clave, etapa, der_efectiva):
    """El mínimo de FEDIAF de este nutriente, YA escalado a lo que come el perro.

    Se pregunta a `verificar`, que es el único sitio que sabe escalar (regla del
    CLAUDE.md: `minimo_de()` es el único que escala mínimos). Aquí no se repite
    esa lógica: repetirla es como el motor y el analizador acabaron discrepando
    por la fibra.
    """
    from verificar import MAPA, minimo_de
    nombre = next((n for n, c in MAPA.items() if c == clave), None)
    if not nombre:
        return None
    fila = (req or {}).get(nombre)
    if not fila:
        return None
    return minimo_de(fila, nombre, etapa, der_efectiva)


def suelo_que_de_verdad_se_aplica(req, clave, etapa, der_efectiva,
                                  peso_adulto_esperado_kg=None,
                                  factor_premios=1.0):
    """El suelo que el SOLVER le va a exigir a este nutriente, no el de la fila.

    Tres cosas lo separan del número de `requerimientos_v2_final.json`, y las
    tres las aplica el solver:

      1. El escalado por lo que come el perro (ecuación 7.2.5 de FEDIAF), que
         ya hace `minimo_de`.
      2. El **mínimo reforzado de la nota b** para el cachorro que pasará de
         `RAZA_GRANDE_O_GIGANTE_KG` de adulto, que vive en la fila
         `Calcio_LateGrowth_RazaGrande` y es 2500 en vez de 2000.
      3. **Los premios**, que suben todos los suelos por `der/der_racion`
         porque son suelos de CONCENTRACIÓN sobre el día entero y la ración es
         solo una parte de ese día.

    Existe porque `topes_de_la_etapa` tiene que decidir si un techo del libro
    cede, y para eso hay que compararlo con lo que de verdad se le pide al menú.
    Comparar contra otra cosa es el fallo de Cairo: dos cifras que se cruzan, un
    menú que no sale, y nadie capaz de decir por qué.

    ⚠️ NO REPITE LA LÓGICA DE NADIE: el escalado se lo pregunta a `minimo_de`
    (el único sitio que sabe escalar, regla del CLAUDE.md) y el umbral de raza
    grande a `motor_completo.RAZA_GRANDE_O_GIGANTE_KG`. Si mañana ese umbral
    cambia, cambia aquí con él.
    """
    minimo = _minimo_de_fediaf(req, clave, etapa, der_efectiva)
    if clave == "calcio" and etapa in ("CachorroJoven", "CachorroCrecimiento"):
        from motor_completo import RAZA_GRANDE_O_GIGANTE_KG as _UMBRAL_NOTA_B
        if peso_adulto_esperado_kg and peso_adulto_esperado_kg >= _UMBRAL_NOTA_B:
            fila = (req or {}).get("Calcio_LateGrowth_RazaGrande") or {}
            crudo = fila.get("min" + str(etapa))
            try:
                reforzado = float(crudo) if crudo not in (None, "", "-") else None
            except (TypeError, ValueError):
                reforzado = None
            if reforzado is not None and (minimo is None or reforzado > minimo):
                minimo = reforzado
    if minimo is not None and factor_premios and factor_premios != 1.0:
        minimo = minimo * float(factor_premios)
    return minimo


def con_procedencia(etapa, peso_adulto_esperado_kg=None):
    """Lo mismo, pero cada techo sabiendo de dónde viene y por qué.

    Para poder decirle a alguien «lo que te está apretando el fósforo no es tu
    perro, es la recomendación del libro para cualquier adulto», que es la
    diferencia entre un límite y una pared.
    """
    nombre = ("Recomendación del libro para el perro sano"
              if etapa in ("CachorroJoven", "CachorroCrecimiento")
              else "Recomendación para el perro adulto sano")
    fuera = []
    for clave, t in _topes_crudos(etapa, peso_adulto_esperado_kg).items():
        fuera.append({"tipo": "tope", "clave": clave, "valor": t["valor"],
                      "patologia": None, "nombre_patologia": nombre,
                      "fuente": t.get("fuente"), "por_que": t.get("por_que")})
    # ⚠️ Y LOS SUELOS (11 septiembre). Si esta función solo listara los techos,
    # quien pregunta «¿qué me está bloqueando?» recibiría la lista incompleta y
    # el diagnóstico culparía a otra restricción -- que es peor que no decir
    # nada, porque manda a mirar la fila equivocada.
    for clave, s in _suelos_crudos(etapa, peso_adulto_esperado_kg).items():
        fuera.append({"tipo": "suelo", "clave": clave, "valor": s["valor"],
                      "patologia": None, "nombre_patologia": nombre,
                      "fuente": s.get("fuente"), "por_que": s.get("por_que")})
    return fuera
