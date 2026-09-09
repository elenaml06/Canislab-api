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
                      peso_adulto_esperado_kg=None):
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
    """
    salida = {}
    for clave, t in _topes_crudos(etapa, peso_adulto_esperado_kg).items():
        valor = t["valor"]
        if req is not None and der_efectiva is not None:
            minimo = _minimo_de_fediaf(req, clave, etapa, der_efectiva)
            if minimo is not None and minimo > valor:
                # El techo se cae. No en silencio: `cedidos_ante_fediaf` lo
                # cuenta, y de ahí sale el aviso que lee quien pide el menú.
                continue
        salida[clave] = valor
    return salida


def cedidos_ante_fediaf(etapa, req, der_efectiva, peso_adulto_esperado_kg=None):
    """Los techos que se han caído por cruzarse con el mínimo de FEDIAF.

    Devuelve `[{clave, techo, minimo_de_fediaf}]`. Existe para poder DECIRLO:
    la regla 5 del CLAUDE.md es que se puede bajar de peldaño pero se dice, y
    esto es lo mismo un escalón más abajo -- un límite que estaba puesto y ha
    dejado de aplicarse a este perro concreto.
    """
    fuera = []
    for clave, t in _topes_crudos(etapa, peso_adulto_esperado_kg).items():
        minimo = _minimo_de_fediaf(req, clave, etapa, der_efectiva)
        if minimo is not None and minimo > t["valor"]:
            fuera.append({"clave": clave, "techo": t["valor"],
                          "minimo_de_fediaf": round(minimo, 1)})
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


def con_procedencia(etapa, peso_adulto_esperado_kg=None):
    """Lo mismo, pero cada techo sabiendo de dónde viene y por qué.

    Para poder decirle a alguien «lo que te está apretando el fósforo no es tu
    perro, es la recomendación del libro para cualquier adulto», que es la
    diferencia entre un límite y una pared.
    """
    fuera = []
    for clave, t in _topes_crudos(etapa, peso_adulto_esperado_kg).items():
        fuera.append({"tipo": "tope", "clave": clave, "valor": t["valor"],
                      "patologia": None,
                      "nombre_patologia": ("Recomendación del libro para el perro sano"
                                           if etapa in ("CachorroJoven", "CachorroCrecimiento")
                                           else "Recomendación para el perro adulto sano"),
                      "fuente": t.get("fuente"), "por_que": t.get("por_que")})
    return fuera
