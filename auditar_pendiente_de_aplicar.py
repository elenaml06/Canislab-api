# -*- coding: utf-8 -*-
"""CUANTAS COSAS HEMOS LEIDO Y **NO** APLICADO, Y DONDE ESTAN.

⚠️ POR QUE EXISTE (11 de septiembre de 2026, de noche). Elena, y tenia toda la
razon:

    «antes me habias dicho que SACN5 esta cerrado y ahora dices que gestacion y
     lactancia tienen una tabla propia que no esta transcrita, y a eso me
     refiero cuando te digo que me dices que algo esta cerrado y siempre sale
     algo que demuestra que no lo esta. no estas planteando bien la manera de
     estudiar los documentos»

EL DIAGNOSTICO, y es de metodo y no de descuido. En este repo «cerrado»
significaba UNA cosa: que cada elemento de la fuente tiene VEREDICTO. No
significaba que no quedara nada por aplicar. La Tabla 15-5 de gestacion TIENE
veredicto -- «leida, no aplicada» -- asi que el contador marca cero pendientes,
y a la vez hay algo esperando. Las dos cosas eran verdad y se contaban como una.

Lo que faltaba es el SEGUNDO NUMERO: cuantas cosas se han leido, se ha decidido
no aplicarlas, y siguen esperando. Ese numero vivia desperdigado en seis
ficheros y nadie lo sumaba, asi que nadie podia ver que no estaba vacio.

⚠️ Y AL CONSTRUIRLO SALIO EL FALLO DE RAIZ, que es lo que Elena llamaba «no
estas planteando bien la manera de estudiar»:

    LOS TRES REGISTROS DE LECTURA USAN TRES VOCABULARIOS DISTINTOS.
    `lecturas_fascetti.json` guarda {veredicto, por} con seis valores de una
    lista, asi que se puede contar. `lecturas_sacn5.json` y
    `lecturas_nrc2006.json` guardan el veredicto como TEXTO LIBRE.

O sea que de SACN5 y de NRC 2006 se puede afirmar que cada elemento tiene una
nota, y NO se puede afirmar por maquina si esa nota dice «aplicado», «no
aplica» o «encontrado algo y aparcado». Sus «0 pendientes» significan «0 sin
nota», que es menos de lo que yo di a entender.

Este auditor cuenta lo que SI se puede contar y **declara en voz alta** lo que
no. Un contador cuyo punto ciego esta escrito vale; uno que calla, no.
"""
import io
import json
import os
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))

# Los veredictos que significan «leido, y NO aplicado». Lista cerrada: un
# veredicto nuevo que no este aqui hace fallar el auditor, que es lo que impide
# que alguien invente una etiqueta y se salga del recuento.
SIGNIFICAN_PENDIENTE = {"hallazgo", "hallazgo_sin_aplicar"}
SIGNIFICAN_RESUELTO = {"leido_no_aplica", "no_aplica", "leido_coincide",
                       "confirma_lo_que_ya_aplica", "aplicado", "aplicado_en_parte"}

# Registros cuyos veredictos son TEXTO LIBRE y por tanto no se pueden contar.
# ⚠️ No se quitan de la lista: se declaran, que es distinto.
SIN_VOCABULARIO = {
    "lecturas_sacn5.json": ("SACN5", 2999),
    "lecturas_nrc2006.json": ("NRC 2006", 1194),
    "lecturas_fuentes.json": ("FEDIAF", 2369),
}


def _lee(nombre):
    ruta = os.path.join(RAIZ, nombre)
    if not os.path.exists(ruta):
        return None
    return json.load(io.open(ruta, encoding="utf-8"))


def auditar():
    problemas, filas = [], []

    # 1. Los limites escritos y no aplicados de las patologias.
    pat = _lee("patologias.json")
    if pat:
        n = sum(len(v.get("limites_escritos_que_el_solver_no_aplica") or {})
                for v in pat["patologias"].values())
        filas.append(("patologias.json", "limites escritos que el solver no aplica", n))

    # 2. Lo que el libro recomienda al perro sano y esta apagado.
    reco = _lee("recomendaciones_libro.json")
    if reco:
        n = sum(1 for e in reco["por_etapa"].values()
                for tipo in ("topes_por_1000kcal", "suelos_por_1000kcal")
                for c in (e.get(tipo) or {}).values()
                if c.get("aplicado_por_el_solver") is False)
        filas.append(("recomendaciones_libro.json", "apagados (aplicado_por_el_solver: false)", n))

    # 3. Los condicionales que la fuente enuncia y no cuantifica.
    cond = _lee("requisitos_condicionales.json")
    if cond:
        def cuenta(o):
            s = 0
            if isinstance(o, dict):
                if o.get("tipo") == "documentado_sin_cifra":
                    s += 1
                for v in o.values():
                    s += cuenta(v)
            elif isinstance(o, list):
                for v in o:
                    s += cuenta(v)
            return s
        filas.append(("requisitos_condicionales.json", "documentados sin cifra", cuenta(cond)))

    # 4. Las tablas de SACN5 leidas CON hallazgo.
    tab = _lee("sacn5_tablas.json")
    if tab:
        tablas = tab.get("tablas") or {k: v for k, v in tab.items() if k != "_meta"}
        n = sum(1 for v in tablas.values()
                if isinstance(v, dict) and "hallazgo" in str(v.get("veredicto", "")))
        filas.append(("sacn5_tablas.json", "tablas leidas CON hallazgo", n))

    # 5. Los registros de lectura que SI tienen vocabulario.
    fas = _lee("lecturas_fascetti.json")
    if fas:
        n = 0
        for cap in fas["capitulos"].values():
            for v in (cap.get("veredictos") or {}).values():
                if not isinstance(v, dict):
                    continue
                ver = v.get("veredicto")
                if ver in SIGNIFICAN_PENDIENTE:
                    n += 1
                elif ver not in SIGNIFICAN_RESUELTO:
                    problemas.append(
                        f"lecturas_fascetti.json usa el veredicto «{ver}», que no esta en "
                        f"ninguna de las dos listas de este auditor. Un veredicto inventado se "
                        f"sale del recuento sin que nadie lo vea")
        filas.append(("lecturas_fascetti.json", "veredictos de hallazgo sin aplicar", n))

    total = sum(n for _, _, n in filas)
    print(f"  PENDIENTE DE APLICAR: {total}\n")
    for fichero, que, n in filas:
        print(f"    {n:4}  {fichero:32} {que}")

    # 6. ⚠️ Y LO QUE NO SE PUEDE CONTAR, dicho en voz alta.
    print("\n  ⚠️ NO SE PUEDE CONTAR (el veredicto es TEXTO LIBRE, no una etiqueta):")
    for fichero, (nombre, cuantos) in sorted(SIN_VOCABULARIO.items()):
        d = _lee(fichero)
        estado = "no esta" if d is None else f"{cuantos} elementos con nota"
        print(f"    {nombre:10} {fichero:26} {estado}")
    print("    De estos tres se puede afirmar que cada elemento tiene una nota, y NO se puede")
    print("    afirmar por maquina si esa nota dice «aplicado», «no aplica» o «encontrado algo")
    print("    y aparcado». Su «0 pendientes» significa «0 SIN NOTA», que es menos de lo que")
    print("    parece. Darles vocabulario es el trabajo que queda.")

    for p in problemas:
        print(f"  ❌ {p}")
    print(f"\nDiscrepancias: {len(problemas)}")
    return problemas


if __name__ == "__main__":
    sys.exit(1 if auditar() else 0)
