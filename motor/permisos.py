# -*- coding: utf-8 -*-
"""
LA FICHA DE PERMISOS: quién VE cada número y quién puede MOVERLO.

Es la condición 3 de las seis del cierre (`PROMPT_CIERRE_RAWKU_2.md`): «tiene
ficha de permisos». Hasta el 8 de septiembre de 2026 no existía en ninguna parte
del repo, y por eso ninguna decisión podía llamarse cerrada del todo.

⚠️ ESTA FICHA NO SE ESCRIBE: SE DERIVA. Y es lo más importante del módulo.

Escribirla a mano habría creado una tabla más con los mismos números que
`patologias.json` y `requerimientos_v2_final.json` — o sea, una tercera copia que
se desincroniza. Es el fallo que este repo lleva documentando desde la fibra, y
el mismo que ya pasó de verdad con la tabla de patologías del `POST /menu`.

Así que casi todo sale de lo que ya existe:

  · el VALOR y la FUENTE          → `patologias.json`
  · el TECHO legal                → el `maxAdulto` de los siete nutrientes que
                                    FEDIAF marca como límite legal de la UE
                                    (Reglamento 2017/1492)
  · el SUELO por debajo del cual   → `minimo_de()`, el mínimo de FEDIAF
    hace falta firma
  · quién puede moverlo            → la regla de `DECISIONES.md` D-13

Lo ÚNICO que se escribe a mano aquí es `visible_para`, porque no se deduce de
ninguna fuente: es criterio de producto. Un dueño no debe ver «fósforo ≤1200
mg/1000 kcal» — no le dice nada y le asusta; ve el aviso en cristiano. Un
profesional sí ve el número, su rango y su fuente.

Cambias un tope en `patologias.json` y el rango de esta ficha se recalcula solo.
No hay nada que mantener sincronizado.
"""
import json
import os

from constructor import cargar as _cargar_catalogo_y_req
from verificar import MAPA, minimo_de, maximo_de
from patologias import CRUDO as _CRUDO


# ── Los siete con techo LEGAL, no nutricional ────────────────────────────
#
# FEDIAF marca sus máximos con «(L)» cuando vienen de la ley de aditivos de la
# UE (Reglamento (UE) 2017/1492) y con «(N)» cuando son nutricionales. Los (L)
# NO los mueve nadie, tampoco un veterinario: no puede autorizar un alimento con
# más cobre del que permite la ley. Los (N) sí admiten criterio.
#
# La lista sale de las notas de auditoría de `requerimientos_v2_final.json`,
# donde cada uno de estos siete lleva escrito que su máximo es el legal. Se
# comprueba abajo, en `_comprobar_coherencia()`, para que no se quede vieja.
MAXIMO_ES_LEGAL = {
    "Vitamina_D", "Hierro", "Yodo", "Selenio", "Zinc", "Cobre", "Manganeso",
}

# ── Qué ve el dueño ──────────────────────────────────────────────────────
#
# Lo único que NO se deriva. Por defecto un límite de patología es cosa del
# profesional: el dueño ve el AVISO en cristiano (que ya vive en
# `patologias.json`, en `avisos.general`), no la cifra.
#
# La excepción son los nutrientes que el dueño reconoce y sobre los que puede
# actuar en la compra — la grasa y la fibra —, donde enseñar el número ayuda en
# vez de asustar: «este menú lleva poca grasa» se entiende.
VISIBLE_PARA_EL_DUENO = {"grasa", "fibra"}


_REQ_CACHE = {}


def _req():
    """La tabla de FEDIAF ya resuelta, cargada una sola vez."""
    if "r" not in _REQ_CACHE:
        _REQ_CACHE["r"] = _cargar_catalogo_y_req()[1]
    return _REQ_CACHE["r"]


def _tipo_de(nombre_req, clave, es_tope, valor):
    """Qué clase de número es. De aquí sale quién puede moverlo."""
    if es_tope and nombre_req in MAXIMO_ES_LEGAL:
        r = (_req() or {}).get(nombre_req) or {}
        mx = maximo_de(r, nombre_req, "Adulto")
        if mx is not None and abs(valor - mx) < 1e-9:
            # El tope de la patología ES el máximo legal, reproducido ahí para
            # que se vea (caso del oxalato con la vitamina D).
            return "legal"
    return "tope_de_patologia" if es_tope else "suelo_de_patologia"


def ficha(clave_pat, tipo_bloque, clave_nut, etapa="Adulto"):
    """La ficha de permisos de UN límite, derivada.

    `tipo_bloque` es "topes_por_1000kcal" o "suelos_por_1000kcal".
    """
    pats = _CRUDO["patologias"]
    info = pats.get(clave_pat) or {}
    bloque = info.get(tipo_bloque) or {}
    if clave_nut not in bloque:
        return None
    dato = bloque[clave_nut]
    valor = dato["valor"]
    es_tope = tipo_bloque == "topes_por_1000kcal"

    # El nombre del requisito de FEDIAF que corresponde a esta clave.
    nombre_req = next((n for n, c in MAPA.items() if c == clave_nut), None)
    req = _req() or {}
    r = req.get(nombre_req) or {}
    mn = minimo_de(r, nombre_req, etapa) if nombre_req and r else None
    mx = maximo_de(r, nombre_req, etapa) if nombre_req and r else None

    tipo = _tipo_de(nombre_req, clave_nut, es_tope, valor)
    legal = nombre_req in MAXIMO_ES_LEGAL and mx is not None

    # ── EL RANGO, DERIVADO ───────────────────────────────────────────────
    # Para un TECHO: se puede apretar hasta el mínimo de FEDIAF (por debajo es
    # prescripción) y aflojar hasta el máximo legal, si lo hay.
    # Para un SUELO: se puede aflojar hasta el mínimo de FEDIAF (por debajo el
    # requisito general manda igual) y apretar hasta el máximo legal.
    if es_tope:
        desde, hasta = mn, (mx if mx is not None else None)
        para_abajo = ("el mínimo de FEDIAF: por debajo deja de ser un menú y pasa "
                      "a ser una prescripción firmada") if mn is not None else \
                     "nada: FEDIAF no da mínimo para este nutriente"
        para_arriba = ("el máximo LEGAL de FEDIAF (Reg. UE 2017/1492), que no mueve "
                       "nadie") if legal else \
                      ("el máximo nutricional de FEDIAF" if mx is not None else
                       "nada: FEDIAF no da máximo para este nutriente")
    else:
        desde, hasta = mn, (mx if mx is not None else None)
        para_abajo = ("el mínimo de FEDIAF, que se aplica igual aunque se baje "
                      "este suelo") if mn is not None else \
                     "nada: FEDIAF no da mínimo para este nutriente"
        para_arriba = ("el máximo LEGAL de FEDIAF (Reg. UE 2017/1492), que no mueve "
                       "nadie") if legal else \
                      ("el máximo nutricional de FEDIAF" if mx is not None else
                       "nada: FEDIAF no da máximo para este nutriente")

    return {
        "patologia": clave_pat,
        "nutriente": clave_nut,
        "tipo": tipo,
        "defecto": valor,
        "fuente": dato.get("fuente"),
        "por_que": dato.get("por_que"),
        # Quién lo ve. Lo único escrito a mano.
        "visible_para": (["dueno", "profesional"] if clave_nut in VISIBLE_PARA_EL_DUENO
                         else ["profesional"]),
        # Quién lo mueve. Regla de DECISIONES.md D-13.
        "modificable_por": ([] if tipo == "legal" else ["profesional"]),
        # Hasta dónde, derivado.
        "rango_permitido": {"desde": desde, "hasta": hasta,
                            "lo_para_por_abajo": para_abajo,
                            "lo_para_por_arriba": para_arriba},
        # Qué hace falta y qué pasa al moverlo.
        "requiere": ("firma de un profesional si se cruza el mínimo de FEDIAF"
                     if mn is not None else None),
        "al_moverlo": (
            "Nada: es un límite legal y no se mueve." if tipo == "legal" else
            "Queda registrado quién, cuándo y de qué valor a qué valor. El menú "
            "se verifica igual contra el juego de requisitos que resulte; si el "
            "valor nuevo cruza el mínimo de FEDIAF, el resultado deja de ser un "
            "menú y pasa a ser una prescripción firmada."),
    }


def todas(etapa="Adulto"):
    """Las fichas de los límites de patología del motor, derivadas."""
    salida = []
    for clave_pat, info in (_CRUDO["patologias"] or {}).items():
        for tipo_bloque in ("topes_por_1000kcal", "suelos_por_1000kcal"):
            for clave_nut in (info.get(tipo_bloque) or {}):
                f = ficha(clave_pat, tipo_bloque, clave_nut, etapa)
                if f:
                    salida.append(f)
    return salida


def _comprobar_coherencia():
    """Que `MAXIMO_ES_LEGAL` siga siendo la lista de los que lo son.

    La lista está escrita a mano porque el JSON no tiene un campo booleano para
    ello -- lo que sí tiene es la nota de auditoría de cada fila, donde está
    escrito. Esto compara las dos y devuelve las diferencias, para que la lista
    no se quede vieja el día que FEDIAF cambie un máximo de (N) a (L) o al
    revés. Lo ejecuta la batería.
    """
    aqui = os.path.dirname(os.path.abspath(__file__))
    ruta = os.path.join(aqui, "..", "requerimientos_v2_final.json")
    filas = json.load(open(ruta, encoding="utf-8"))
    segun_notas = {
        x["nutriente"] for x in filas
        if "legal" in str(x.get("nota_auditoria", "")).lower()
        and str(x.get("maxAdulto", "-")) not in ("-", "None", "")
    }
    return {"solo_en_la_lista": sorted(MAXIMO_ES_LEGAL - segun_notas),
            "solo_en_las_notas": sorted(segun_notas - MAXIMO_ES_LEGAL)}
