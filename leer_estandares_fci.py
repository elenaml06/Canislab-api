# -*- coding: utf-8 -*-
"""
CANISLAB — LOS PESOS DE RAZA, LEIDOS DEL ESTANDAR DE LA FCI

⚠️ POR QUE EXISTE (11 de septiembre de 2026). `razas.json` llevaba en su `_meta`
una frase incomoda: **estas cifras no tienen fuente publicada**. 255 pesos
adultos que deciden las kcal, la etapa, el techo de calcio del cachorro de raza
grande y si al perro le toca la cifra de energia propia que FEDIAF da a dos
razas... y detras, nada que se pudiera abrir.

La FCI publica el estandar oficial de cada raza, gratis, y el estandar trae el
peso. Este script lee los textos que baja `canislab-fuentes/FCI/bajar_estandares.py`
y saca de cada uno:

  · el numero de raza y su grupo
  · el nombre en el idioma original y el nombre en castellano
  · el peso de macho y de hembra, y la altura a la cruz

⚠️ LO QUE NO HACE, Y ES DELIBERADO: **no renombra ninguna raza que ya este en
`razas.json`**. `der.py` reconoce al «Gran Danés» y al «Terranova» POR SU NOMBRE
LITERAL para darles su cifra propia de FEDIAF, y una tilde distinta y esa cifra
no se aplica nunca, sin error y con el menu en verde. Los nombres que ya existen
se quedan como estan y solo se les CUELGA la procedencia.

⚠️ Y NO TODO ESTANDAR DA PESO. Muchas razas se definen por la altura a la cruz y
no publican kilos. Eso no se rellena a ojo: la raza se queda con su peso de hoy
y con `peso_fuente: null`, que es un hueco declarado, igual que en el catalogo.

    python3 leer_estandares_fci.py            # informe por pantalla
    python3 leer_estandares_fci.py --json f   # vuelca lo leido a un fichero
"""
import argparse
import glob
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
TEXTOS = [os.environ.get("RUTA_FCI") or "",
          os.path.join(AQUI, "..", "canislab-fuentes", "FCI", "textos"),
          os.path.join(AQUI, "fuentes", "FCI", "textos")]

# «Weight: 30 kg to 40 kg» · «Peso: 30 a 40 kg» · «Weight: 25-30 kg»
_KG = r"(\d{1,3}(?:[.,]\d+)?)"
_PESO = re.compile(r"(?i)\b(?:weight|peso)\b\s*:?\s*" + _KG +
                   r"\s*(?:kg)?\s*(?:to|a|-|–|—|and|y)\s*" + _KG + r"\s*kg")
_PESO_UNO = re.compile(r"(?i)\b(?:weight|peso)\b\s*:?\s*(?:about|approx\.?|unos|aprox\.?)?\s*"
                       + _KG + r"\s*kg")
_ALTURA = re.compile(r"(?i)height at the withers|altura a la cruz")
_SEXO_M = re.compile(r"(?i)\b(males?|dogs?|machos?)\b")
_SEXO_H = re.compile(r"(?i)\b(females?|bitch(?:es)?|hembras?)\b")


def carpeta():
    for r in TEXTOS:
        if r and os.path.isdir(r) and glob.glob(os.path.join(r, "*-en.txt")):
            return r
    return None


def _nombre(texto, idioma):
    """El nombre del estandar: la linea en MAYUSCULAS tras «FCI-Standard N°»,
    y entre parentesis el nombre en el idioma de este documento."""
    lineas = [l.strip() for l in texto.split("\n")]
    for i, l in enumerate(lineas):
        if re.search(r"(?i)(FCI[- ]Standard|Est[áa]ndar[- ]FCI)\s*N", l):
            original = traducido = None
            for j in range(i + 1, min(i + 8, len(lineas))):
                s = lineas[j]
                if not s:
                    continue
                if original is None and s.upper() == s and len(s) > 2 and any(c.isalpha() for c in s):
                    original = s
                    continue
                m = re.match(r"^\((.+)\)$", s)
                if original is not None and m:
                    traducido = m.group(1).strip()
                    break
                if original is not None and not s.startswith("("):
                    break
            return original, traducido
    return None, None


def _pesos(texto):
    """El peso de macho y de hembra, en kg. None donde el estandar no lo da.

    ⚠️ ES UNA MAQUINA DE ESTADOS Y NO UNA EXPRESION REGULAR, porque el estandar
    NO pone el peso en la misma linea que la palabra «Weight». Medido sobre los
    textos de verdad, la seccion viene asi:

        SIZE AND WEIGHT:
        Height at the withers:
        Dogs:
        18 - 19,5    inches (45,5 to 49,5 cm).
        Weight:
        Dogs:
        33 lbs to 40 lbs (15 to 18 kg).
        Bitches:
        proportionately less.

    O sea que hay que arrastrar DOS estados a la vez -- de que se esta hablando
    (altura o peso) y de que sexo --, y que la cifra buena puede venir dentro de
    un parentesis detras de las libras. Un `re.search` por linea se traga la
    altura como si fuera peso, que es como salieron las primeras pruebas.
    """
    lineas = [l.strip() for l in texto.split("\n")]
    inicio = None
    for i, l in enumerate(lineas):
        if re.search(r"(?i)\b(size\s*(?:and|/|y)\s*weight|talla\s*(?:y|/)\s*peso|"
                     r"weight\s*(?:and|/)\s*size|peso\s*(?:y|/)\s*talla)\b", l):
            inicio = i
            break
    if inicio is None:
        return None, None
    macho = hembra = unico = None
    mirando = None      # "altura" | "peso"
    sexo = None
    for l in lineas[inicio:inicio + 45]:
        if not l:
            continue
        if _ALTURA.search(l):
            mirando = "altura"
        if re.search(r"(?i)\b(weight|peso)\b", l):
            mirando = "peso"
        if _SEXO_H.search(l):
            sexo = "h"
        elif _SEXO_M.search(l):
            sexo = "m"
        if mirando != "peso":
            continue
        rango = _kg_de(l)
        if rango is None:
            continue
        if sexo == "m" and macho is None:
            macho = rango
        elif sexo == "h" and hembra is None:
            hembra = rango
        elif sexo is None and unico is None:
            unico = rango
    if macho is None and hembra is None:
        macho = hembra = unico
    return macho, hembra


def _kg_de(linea):
    """Los kilos de una linea, si los hay. Devuelve [min, max] o None.

    ⚠️ Tres trampas medidas en los textos de verdad:
      · «33 lbs to 40 lbs (15 to 18 kg)» -- la cifra buena esta en el PARENTESIS.
      · «13 - 14, 5 kgs» -- el decimal viene con coma Y un espacio detras.
      · «45,5 to 49,5 cm» -- son centimetros y NO se pueden leer como kilos.
    """
    if not re.search(r"(?i)\bkgs?\b", linea):
        return None
    dentro = re.findall(r"\(([^)]*kgs?[^)]*)\)", linea, re.I)
    trozo = dentro[0] if dentro else linea
    trozo = re.sub(r"(\d),\s+(\d)", r"\1.\2", trozo)   # «14, 5» -> «14.5»
    trozo = trozo.replace(",", ".")
    nums = [float(x) for x in re.findall(r"\d{1,3}(?:\.\d+)?", trozo)]
    nums = [n for n in nums if 0.5 <= n <= 120]
    if not nums:
        return None
    return [min(nums), max(nums)]


def leer():
    c = carpeta()
    if not c:
        return []
    salida = []
    for ruta in sorted(glob.glob(os.path.join(c, "*-en.txt"))):
        numero = int(os.path.basename(ruta)[:3])
        texto = open(ruta, encoding="utf-8", errors="ignore").read()
        grupo = None
        m = re.search(r"# FCI \d{3} grupo (\d{2})", texto)
        if m:
            grupo = int(m.group(1))
        original, en = _nombre(texto, "en")
        macho, hembra = _pesos(texto)
        es = None
        ruta_es = ruta[:-7] + "-es.txt"
        if os.path.exists(ruta_es):
            t_es = open(ruta_es, encoding="utf-8", errors="ignore").read()
            _, es = _nombre(t_es, "es")
            if macho is None and hembra is None:
                macho, hembra = _pesos(t_es)
        salida.append({"fci": numero, "grupo": grupo, "nombre_original": original,
                       "nombre_en": en, "nombre_es": es,
                       "peso_macho_kg": macho, "peso_hembra_kg": hembra,
                       "estandar": f"FCI-Standard N° {numero}"})
    return salida


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()
    razas = leer()
    con_peso = [r for r in razas if r["peso_macho_kg"] or r["peso_hembra_kg"]]
    con_es = [r for r in razas if r["nombre_es"]]
    print(f"  {len(razas)} estándares leídos · {len(con_peso)} dan peso en kg · "
          f"{len(con_es)} traen nombre en castellano")
    if args.json:
        open(args.json, "w", encoding="utf-8").write(
            json.dumps(razas, ensure_ascii=False, indent=2) + "\n")
        print(f"  volcado a {args.json}")
    else:
        for r in razas[:10]:
            print(f"   {r['fci']:>3} g{r['grupo']:02d}  {str(r['nombre_es'] or r['nombre_en'])[:38]:<40} "
                  f"M {r['peso_macho_kg']}  H {r['peso_hembra_kg']}")


if __name__ == "__main__":
    main()
