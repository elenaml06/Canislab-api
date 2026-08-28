# -*- coding: utf-8 -*-
"""
Audita `patologias.json` contra `requerimientos_v2_final.json` y contra el
MAPA del verificador.

Existe por lo mismo que `auditar_fediaf.py`: los topes por patología deciden
si un menú se entrega, y hasta el 28 de agosto vivían en un `dict` de Python
donde nadie podía comprobarlos. Un número mal puesto ahí no da error: da un
menú, y el menú sale verde.

Ejecutar tras cualquier cambio en patologias.json:
    python3 auditar_patologias.py
"""
import json, os, sys

_AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_AQUI, "motor"))
from verificar import MAPA                                  # noqa: E402
from patologias import cargar_crudo                         # noqa: E402


def _num(v):
    if v in (None, "", "-"):
        return None
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def auditar(crudo=None, req=None):
    """Devuelve la lista de problemas. Vacía = todo cuadra."""
    crudo = crudo or cargar_crudo()
    if req is None:
        with open(os.path.join(_AQUI, "requerimientos_v2_final.json"), encoding="utf-8") as f:
            req = {r["nutriente"]: r for r in json.load(f)}
    # clave del alimento -> nombre del requisito (el MAPA va al revés)
    por_clave = {clave: nombre for nombre, clave in MAPA.items()}
    problemas = []

    for nombre_pat, p in crudo["patologias"].items():
        formulable = p.get("formulable")
        if formulable is None:
            problemas.append(f"{nombre_pat}: no dice si es `formulable`. Es lo primero que hay "
                             f"que saber de una patología: si se le puede dar menú o hay que "
                             f"mandarla al veterinario.")
        bloquea = bool(p.get("sin_dieta_automatica"))

        # 1. Formulable y bloqueante son la misma cosa dicha dos veces: si se
        #    separan, el motor hace una cosa y el documento dice otra.
        if formulable is False and not bloquea:
            problemas.append(f"{nombre_pat}: `formulable: false` pero NO tiene "
                             f"`sin_dieta_automatica`. El motor le va a generar menú igual.")
        if formulable is True and bloquea:
            problemas.append(f"{nombre_pat}: dice `formulable: true` y a la vez bloquea la "
                             f"generación. Una de las dos sobra.")
        if formulable is False and not (p.get("motivo_no_formulable") or "").strip():
            problemas.append(f"{nombre_pat}: no se formula y no dice por qué. El motivo es lo "
                             f"que se le enseña a quien pregunte, y lo que evita que dentro de "
                             f"seis meses alguien lo 'arregle' sin saber qué rompe.")

        for clave, tope in (p.get("topes_por_1000kcal") or {}).items():
            valor = _num(tope.get("valor"))

            # 2. Cada cifra con su fuente y su porqué. Regla del catálogo entero.
            if not (tope.get("fuente") or "").strip():
                problemas.append(f"{nombre_pat}/{clave}: el tope {valor} no tiene FUENTE.")
            if not (tope.get("por_que") or "").strip():
                problemas.append(f"{nombre_pat}/{clave}: el tope {valor} no dice POR QUÉ es ese "
                                 f"número y no otro.")

            # 3. Que el motor mire de verdad esa clave. Es el fallo de la
            #    'Fibra': una restricción sobre un nutriente que no está en el
            #    MAPA no se aplica nunca, y nadie se entera.
            if clave not in por_clave:
                problemas.append(f"{nombre_pat}/{clave}: esa clave NO está en el MAPA del "
                                 f"verificador, así que este tope no se aplica a nada. Es lo "
                                 f"que pasó con 'Fibra'. Claves válidas: {sorted(por_clave)}")
                continue

            # 4. LA REGLA GRANDE: una formulable no puede pedir menos de lo
            #    que FEDIAF exige para un perro sano. Si lo pide, no es un
            #    tope: es una dieta de prescripción, y va con formulable=false.
            r = req.get(por_clave[clave]) or {}
            etapas = [("Adulto", "minAdulto")]
            if not p.get("solo_en_adulto"):
                etapas += [("CachorroJoven", "minCachorroJoven"),
                           ("CachorroCrecimiento", "minCachorroCrecimiento")]
            for etiqueta, campo in etapas:
                minimo = _num(r.get(campo))
                if minimo is None or valor is None or valor >= minimo:
                    continue
                if formulable is False:
                    continue      # terapéutico declarado: es correcto que baje
                problemas.append(
                    f"{nombre_pat}/{clave}: tope {valor} POR DEBAJO del mínimo FEDIAF de "
                    f"{etiqueta} ({minimo}), y la patología está marcada como formulable. "
                    f"Eso no es un tope, es una dieta de prescripción: o se sube el número, "
                    f"o la patología pasa a `formulable: false` con su motivo. "
                    f"{'Si el tope solo vale en adulto, ponle `solo_en_adulto`.' if etiqueta != 'Adulto' else ''}")

        # 5. Soltar un tope en crecimiento se dice SIEMPRE (regla 5 del
        #    CLAUDE.md: se puede bajar de peldaño, pero nunca en silencio).
        if p.get("solo_en_adulto"):
            modo = p.get("en_crecimiento")
            if modo not in ("bloquear", "sin_tope"):
                problemas.append(f"{nombre_pat}: `solo_en_adulto` sin decir qué pasa en "
                                 f"crecimiento (`en_crecimiento` es {modo!r}, y tiene que ser "
                                 f"'bloquear' o 'sin_tope').")
            if modo == "sin_tope" and not ((p.get("avisos") or {}).get("crecimiento") or "").strip():
                problemas.append(f"{nombre_pat}: en crecimiento se suelta el tope y NO hay aviso "
                                 f"que lo diga. Cambiar la dieta en silencio es justo lo que la "
                                 f"regla 5 del CLAUDE.md prohíbe.")

        # 6. Un menú que se entrega tiene que poder explicarse.
        if formulable and not ((p.get("avisos") or {}).get("general") or "").strip():
            problemas.append(f"{nombre_pat}: se le genera menú y no hay aviso que explique qué "
                             f"se le ha ajustado.")
    return problemas


if __name__ == "__main__":
    crudo = cargar_crudo()
    fallos = auditar(crudo)
    n_topes = sum(len(p.get("topes_por_1000kcal") or {}) for p in crudo["patologias"].values())
    print("%d patologías, %d topes numéricos" % (len(crudo["patologias"]), n_topes))
    print("─" * 60)
    if fallos:
        print("\n%d PROBLEMAS:\n" % len(fallos))
        for f in fallos:
            print("  -", f)
        sys.exit(1)
    print("\nTodo cuadra.")
