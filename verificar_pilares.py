# -*- coding: utf-8 -*-
"""
GUARDIÁN DE LOS TRES PILARES  —  ejecutar SIEMPRE antes de subir nada.

    python3 verificar_pilares.py

Los tres pilares son ALIMENTOS, REQUISITOS y CÁLCULO DE KCAL. Están dados
por buenos y verificados contra la fuente. NO SE TOCAN. Si algo aquí falla,
alguien ha cambiado algo que no debía.

QUÉ SE VERIFICÓ Y CONTRA QUÉ (2 agosto 2026):
  · REQUISITOS -> FEDIAF Nutritional Guidelines, TABLA III-3b
    "Recommended nutrient levels for complete DOG food, unit per 1000 kcal ME"
    Columna "Adult based on MER of 95 kcal/kg^0.75" para adulto y senior,
    "Early Growth (<14 weeks) & Reproduction" para cachorro joven, gestación
    y lactancia, y "Late Growth (>=14 weeks)" para cachorro en crecimiento.
    Máximos legales (L): TABLA III-3a (por 100 g de materia seca) convertidos
    con el factor de la TABLA III-2: x2.5.
    Vitaminas: la tabla va en UI. A 1 UI = 0.30 ug · D 1 UI = 0.025 ug ·
    E 1 UI = 0.67 mg.
    Verificado identico en las ediciones de octubre 2021 y septiembre 2025.
    Resultado: 99/99 valores correctos.
  · ALIMENTOS -> BEDCA (fuente primaria del usuario) + Kober/Kienzle para
    huesos con hueso + CIQUAL para lo que falta. 153 alimentos, 0 duplicados.
  · KCAL -> METODO EUROPEO. DER = coeficiente en kcal/kg^0.75, con ajustes
    que se SUMAN (no se multiplican). Crecimiento, gestacion y lactancia
    segun FEDIAF; adultos segun el estudio de la Univ. de Munich sobre 586
    perros europeos reales. La actividad NO se usa en cachorros, gestacion
    ni lactancia (la fuente lo dice literal). Ver der.py y BASES.md.
    ANTES (metodo americano, RER x factor):
    VERIFICADO contra FEDIAF: el mantenimiento adulto de referencia son
    95-110 kcal/kg^0.75 (secc. 3.2.1 y cap. 6), y nuestro "normal" (1.6 =
    112) coincide con el. FEDIAF ademas recomienda expresamente partir de
    un MER bajo y subir segun condicion corporal (secc. 7.2.3.2), que es
    por lo que nuestro "sedentario" queda por debajo de su rango.
    NO VERIFICADO: los valores exactos de la Tabla VII-6 (Anexo 7.2.4).
    El PDF se trunca antes de esa pagina en las 3 ediciones probadas.
    Los factores de actividad alta, senior, gestacion y lactancia vienen
    de NRC 2006 y uso clinico. Ver el detalle completo en der.py.
"""
import hashlib, json, os, sys

SELLOS = {
    "alimentos_v3_final.json":      "8a17063f7696f9b0",
    "requerimientos_v2_final.json": "73ab445f9881f543",
    "der.py":                       "1c5c8bb91ceac481",
}

def huella(ruta):
    return hashlib.sha256(open(ruta, "rb").read()).hexdigest()[:16]

def main():
    base = os.path.dirname(os.path.abspath(__file__))
    cambiados = []
    for fichero, sello in SELLOS.items():
        ruta = os.path.join(base, fichero)
        if not os.path.exists(ruta):
            cambiados.append(f"{fichero}: NO EXISTE")
            continue
        actual = huella(ruta)
        estado = "sin tocar" if actual == sello else "!!! CAMBIADO !!!"
        print(f"  {fichero:<32}{actual}   {estado}")
        if actual != sello:
            cambiados.append(f"{fichero}: era {sello}, ahora {actual}")

    # comprobaciones de fondo, por si el sello se actualizo a la ligera
    problemas = []
    al = json.load(open(os.path.join(base, "alimentos_v3_final.json"), encoding="utf-8"))
    nombres = [a["nombre"] for a in al]
    dup = {n for n in nombres if nombres.count(n) > 1}
    if dup: problemas.append(f"alimentos duplicados: {dup}")
    for a in al:
        if a.get("energia", 0) < 0: problemas.append(f"{a['nombre']}: energía negativa")
        for k, v in a.get("nutrientes", {}).items():
            if isinstance(v, (int, float)) and v < 0:
                problemas.append(f"{a['nombre']}: {k} negativo")

    req = {x["nutriente"]: x for x in json.load(
        open(os.path.join(base, "requerimientos_v2_final.json"), encoding="utf-8"))}
    # muestra de valores clave de la Tabla III-3b, columna 95 kcal
    CLAVE = {"Proteína_total": 52.10, "Calcio": 1450.0, "Fósforo": 1160.0,
             "Zinc": 20.80, "Cobre": 2.08, "Selenio": 67.50,
             "Vitamina_A": 526.20, "Vitamina_D": 3.975, "Vitamina_E": 6.968}
    for n, esperado in CLAVE.items():
        try: v = float(req[n]["minAdulto"])
        except Exception: problemas.append(f"{n}: mínimo adulto ilegible"); continue
        if abs(v - esperado) > esperado * 0.01:
            problemas.append(f"{n}: mínimo adulto {v}, la Tabla III-3b dice {esperado}")

    print()
    if cambiados or problemas:
        print("  ⚠️  ALGO HA CAMBIADO EN LOS PILARES:")
        for x in cambiados + problemas: print(f"     {x}")
        return 1
    print("  ✅ LOS TRES PILARES ESTÁN INTACTOS Y VERIFICADOS")
    return 0

if __name__ == "__main__":
    sys.exit(main())
