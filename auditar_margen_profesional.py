# -*- coding: utf-8 -*-
"""
QUE EL MARGEN DEL VETERINARIO SE REHAGA, EN VEZ DE CREERSELO.

⚠️ POR QUE EXISTE (10 de septiembre). Elena pidió «estipular qué porcentajes
puede variar el veterinario y cuáles NO, y hasta qué punto o qué techo, dentro
de cada patología». La respuesta estaba escrita y ese era el problema: en PROSA,
dentro del campo `por_que` de cada cifra («Margen del profesional: 13,75 a
37,5») y en el §2 de `PATOLOGIAS.md`. Una frase no se ejecuta -- es el mismo
fallo que hizo nacer `auditar_conversiones.py`.

Y no era prosa inofensiva. Dos ejemplos de este mismo repo:

  · La de la pancreatitis decía «Margen del profesional: 13,75 a 37,5» y el
    motor aplica 37,5 **o 25** según el perro. La frase se quedó en la versión
    de antes del tope condicional.
  · El sodio cardíaco aplicaba **739** y su propia celda citaba el techo legal
    en **738,6**. Medio miligramo, clínicamente nada — y por encima de la ley.
    `auditar_conversiones.py` no lo veía porque tolera un 1 % de redondeo en las
    DOS direcciones, que está bien para una recomendación y no para un techo
    legal. Lo cazó esta comprobación el día que se escribió.

LO QUE COMPRUEBA, cifra a cifra:

  1. Que **cada** cifra numérica de `patologias.json` lleve su bloque
     `margen_profesional`. Sin él no hay ventana que enseñarle al profesional, y
     una cifra sin ventana es una cifra que nadie sabe si puede tocar.
  2. Que el suelo y el techo escritos sean los que devuelve la fuente VIVA:
     `minimo_fediaf:X` se resuelve contra `requerimientos_v2_final.json` de hoy,
     `legal_ue:...` contra `limites_legales_ue_2020_354.json`, `seguridad:...`
     contra `seguridad.py`. Así el día que cambie cualquiera de las tres, salta.
  3. Que **la cifra que aplica el motor caiga dentro de su propia ventana**.
     Esto es lo que caza el 739.
  4. Que el techo declarado sea **el más estricto** de los que existen. Declarar
     el máximo de FEDIAF teniendo encima un techo legal más bajo sería enseñar
     un margen que la ley no permite.
"""
import json, os, sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(RAIZ, "motor"))
sys.path.insert(0, RAIZ)

from requisitos import cargar_requerimientos
from verificar import MAPA
import margenes

# Los tres sitios donde vive una cifra por 1000 kcal, y su sentido.
BLOQUES = (("topes_por_1000kcal", "max"),
           ("suelos_por_1000kcal", "min"),
           ("topes_por_1000kcal_si_ademas", "max"))

# Los topes de seguridad crónica que son un techo para un NUTRIENTE del perfil.
# Los otros dos (tiaminasa, mercurio) no lo son: limitan un ALIMENTO, así que no
# tienen forma de ventana por nutriente y no entran aquí.
SEGURIDAD_POR_NUTRIENTE = {
    "vitD": "seguridad:TOPE_VITD_KCAL",
    "yodo": "seguridad:TOPE_YODO_KCAL",
    "selenio": "seguridad:TOPE_SELENIO_KCAL",
    "epa_dha": "seguridad:TOPE_EPA_DHA_SEMANAL_KCAL",
}

CAMPOS = ("sentido_de_la_cifra", "suelo", "suelo_de_donde", "techo",
          "techo_de_donde", "bajo_el_suelo_necesita_firma")


def _legal_por_patologia(legal):
    """(patología, nutriente, sentido) -> la clave legal MÁS ESTRICTA."""
    salida = {}
    for entrada, e in legal["entradas"].items():
        for lim in e["limites"]:
            if not lim["nutriente"]:
                continue
            for pat in e["patologias_del_motor"]:
                k = (pat, lim["nutriente"], lim["sentido"])
                if k in salida:
                    ent_previa = salida[k].split(":")[1]
                    previa = [x for x in legal["entradas"][ent_previa]["limites"]
                              if x["nutriente"] == lim["nutriente"]][0]
                    mejor = (min if lim["sentido"] == "max" else max)(
                        lim["por_1000kcal"], previa["por_1000kcal"])
                    if mejor == previa["por_1000kcal"]:
                        continue
                salida[k] = "legal_ue:%s:%s" % (entrada, lim["nutriente"])
    return salida


def auditar():
    req = cargar_requerimientos()
    tabla = json.load(open(os.path.join(RAIZ, "patologias.json"),
                           encoding="utf-8"))["patologias"]
    clave_a_nombre = {v: k for k, v in MAPA.items()}
    legal_por = _legal_por_patologia(margenes.LEGAL)

    fallos = []
    revisadas = con_ventana = con_techo = con_firma = 0

    def resolver(clave):
        return margenes.resolver(clave, req)[0]

    for pat, ficha in sorted(tabla.items()):
        celdas = []
        for bloque, sentido in BLOQUES:
            for nut, celda in sorted((ficha.get(bloque) or {}).items()):
                if isinstance(celda, dict) and celda.get("valor") is not None:
                    celdas.append((f"{pat}/{bloque}/{nut}", nut, sentido, celda))
        for nombre_r, celda in sorted((ficha.get("ratios") or {}).items()):
            if isinstance(celda, dict) and celda.get("valor") is not None:
                celdas.append((f"{pat}/ratios/{nombre_r}", None,
                               celda["sentido"], celda))

        for donde, nut, sentido, celda in celdas:
            revisadas += 1
            m = celda.get("margen_profesional")
            if not m:
                fallos.append(
                    f"{donde}: no dice hasta dónde puede moverla un profesional. "
                    f"Sin `margen_profesional` (suelo, techo y de dónde sale cada "
                    f"uno) esta cifra no tiene ventana que enseñar, y una cifra "
                    f"sin ventana es una cifra que nadie sabe si puede tocar")
                continue
            faltan = [c for c in CAMPOS if c not in m]
            if faltan:
                fallos.append(f"{donde}: al bloque `margen_profesional` le faltan {faltan}")
                continue
            if m["sentido_de_la_cifra"] != sentido:
                fallos.append(
                    f"{donde}: el margen dice que la cifra es un «{m['sentido_de_la_cifra']}» "
                    f"y está en un bloque de «{sentido}»")
                continue

            # ── 2 · el suelo y el techo, resueltos contra la fuente VIVA ─────
            malo = False
            for lado in ("suelo", "techo"):
                clave = m[lado + "_de_donde"]
                try:
                    vivo = resolver(clave)
                except KeyError as e:
                    fallos.append(f"{donde}: el {lado} dice venir de «{clave}» y "
                                  f"esa procedencia no existe: {e}")
                    malo = True
                    continue
                escrito = m[lado]
                if vivo is None and escrito is None:
                    continue
                if vivo is None or escrito is None:
                    fallos.append(
                        f"{donde}: el {lado} escrito es {escrito} y «{clave}» da "
                        f"{vivo}. Uno de los dos dice que no hay límite y el otro que sí")
                    malo = True
                    continue
                if abs(float(escrito) - float(vivo)) > max(1e-4 * abs(vivo), 1e-9):
                    fallos.append(
                        f"{donde}: el {lado} escrito es {escrito:g} y «{clave}» "
                        f"da hoy {vivo:g}. La fuente se ha movido y el margen "
                        f"publicado se ha quedado atrás")
                    malo = True
            if malo:
                continue

            # ── 3 · la cifra del motor DENTRO de su propia ventana ───────────
            v = float(celda["valor"])
            if m["suelo"] is not None and v < float(m["suelo"]) - 1e-9:
                fallos.append(
                    f"{donde}: el motor aplica {v:g} y su suelo es {m['suelo']:g} "
                    f"({m['suelo_de_donde']}). Está POR DEBAJO de su propia ventana")
                continue
            if m["techo"] is not None and v > float(m["techo"]) + 1e-9:
                fallos.append(
                    f"{donde}: el motor aplica {v:g} y su techo es {m['techo']:g} "
                    f"({m['techo_de_donde']}). Está POR ENCIMA de su propia ventana. "
                    f"Si el techo es legal, esto no es un redondeo: es incumplirlo")
                continue

            # ── 4 · el techo declarado tiene que ser el MÁS ESTRICTO ─────────
            if nut is not None:
                nombre = clave_a_nombre.get(nut)
                candidatos = []
                if nombre and resolver("maximo_fediaf:" + nombre) is not None:
                    candidatos.append("maximo_fediaf:" + nombre)
                if nut in SEGURIDAD_POR_NUTRIENTE:
                    candidatos.append(SEGURIDAD_POR_NUTRIENTE[nut])
                k = legal_por.get((pat, nut, "max"))
                if k:
                    candidatos.append(k)
                if candidatos:
                    mejor = min(candidatos, key=resolver)
                    if m["techo"] is None or float(m["techo"]) > resolver(mejor) + 1e-9:
                        fallos.append(
                            f"{donde}: el techo declarado es {m['techo']} "
                            f"({m['techo_de_donde']}) y existe uno más estricto: "
                            f"{resolver(mejor):g} ({mejor}). Enseñar el laxo sería "
                            f"darle al profesional un margen que la fuente no permite")
                        continue
                elif m["techo"] is not None:
                    fallos.append(
                        f"{donde}: declara un techo de {m['techo']} ({m['techo_de_donde']}) "
                        f"y no hay ninguna fuente que ponga techo a este nutriente")
                    continue

            # ── Y la frontera de firma, que es la del VETERINARIOS.md ────────
            if m["bajo_el_suelo_necesita_firma"] != m["suelo_de_donde"].startswith("minimo_fediaf"):
                fallos.append(
                    f"{donde}: dice `bajo_el_suelo_necesita_firma"
                    f"={m['bajo_el_suelo_necesita_firma']}` y su suelo viene de "
                    f"«{m['suelo_de_donde']}». La firma la marca UNA sola cosa: "
                    f"bajar de un mínimo de FEDIAF")
                continue

            con_ventana += 1
            if m["techo"] is not None:
                con_techo += 1
            if m["bajo_el_suelo_necesita_firma"]:
                con_firma += 1

    print(f"  {revisadas} cifras · {con_ventana} con la ventana rehecha y correcta · "
          f"{con_techo} con techo por arriba · {con_firma} cuyo suelo es un mínimo "
          f"de FEDIAF (bajar de ahí exige firma)")
    return fallos


if __name__ == "__main__":
    fallos = auditar()
    for f in fallos:
        print("  ✗", f)
    print("\nDiscrepancias:", len(fallos))
    raise SystemExit(1 if fallos else 0)
