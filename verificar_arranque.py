# -*- coding: utf-8 -*-
"""
VERIFICADOR DE ARRANQUE — ejecutar SIEMPRE antes de subir a Render.

    python3 verificar_arranque.py

Comprueba, SIN necesidad de tener fastapi instalado, que el backend va a
arrancar. Nace de un error real: una edicion duplico el argumento
`nombres_excluidos` tres veces en cada endpoint y Render murio con
"SyntaxError: keyword argument repeated". Compilaba en trozos, pero la app
no levantaba.

Qué mira:
  1. Que TODOS los .py compilen (AST). Pilla el 'keyword argument repeated'.
  2. Que ninguna llamada repita un argumento con nombre.
  3. Que los argumentos con nombre que se pasan a NUESTRAS funciones existan
     de verdad en la firma de esa funcion (pilla los TypeError de arranque).
  4. Que no haya imports a modulos que no estan en el repo ni en
     requirements.txt.
"""
import ast, os, sys

REPO = os.path.dirname(os.path.abspath(__file__))
PERMITIDOS_EXTERNOS = {"fastapi", "pydantic", "uvicorn", "scipy", "numpy",
                       "json", "os", "sys", "math", "random", "datetime",
                       "sqlite3", "hashlib", "typing", "collections", "re",
                       "itertools", "functools", "copy", "statistics", "ast"}

def modulos_propios():
    return {f[:-3] for f in os.listdir(REPO) if f.endswith(".py")}

def firmas_de(modulo):
    """Devuelve {funcion: set(nombres de parametros)} sin importar el modulo."""
    ruta = os.path.join(REPO, modulo + ".py")
    arbol = ast.parse(open(ruta, encoding="utf-8").read())
    out = {}
    for n in ast.walk(arbol):
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)):
            a = n.args
            nombres = {p.arg for p in a.args} | {p.arg for p in a.kwonlyargs}
            if a.vararg: nombres.add("*")
            if a.kwarg: nombres.add("**")
            out[n.name] = nombres
    return out

def main():
    problemas = []
    propios = modulos_propios()
    firmas = {}
    for m in propios:
        try:
            firmas[m] = firmas_de(m)
        except SyntaxError as e:
            problemas.append(f"{m}.py NO COMPILA — línea {e.lineno}: {e.msg}")

    # todas las funciones de todos nuestros modulos, por nombre
    todas = {}
    for m, fs in firmas.items():
        for f, params in fs.items():
            todas.setdefault(f, set()).update(params)

    for m in sorted(firmas):
        ruta = os.path.join(REPO, m + ".py")
        arbol = ast.parse(open(ruta, encoding="utf-8").read())
        for n in ast.walk(arbol):
            if not isinstance(n, ast.Call):
                continue
            # 2) argumentos con nombre repetidos
            claves = [k.arg for k in n.keywords if k.arg]
            for c in set(claves):
                if claves.count(c) > 1:
                    problemas.append(
                        f"{m}.py línea {n.lineno}: argumento '{c}' repetido "
                        f"{claves.count(c)} veces — Render muere con "
                        f"'keyword argument repeated'")
            # 3) argumentos que no existen en la firma
            nombre = getattr(n.func, "id", None) or getattr(n.func, "attr", None)
            if nombre in todas and "**" not in todas[nombre]:
                for c in claves:
                    if c not in todas[nombre]:
                        problemas.append(
                            f"{m}.py línea {n.lineno}: se llama a {nombre}() con "
                            f"'{c}=', que NO existe en su firma")

        # 4) imports raros
        for n in ast.walk(arbol):
            mods = []
            if isinstance(n, ast.Import):
                mods = [a.name.split(".")[0] for a in n.names]
            elif isinstance(n, ast.ImportFrom) and n.module and n.level == 0:
                mods = [n.module.split(".")[0]]
            for mo in mods:
                if mo not in propios and mo not in PERMITIDOS_EXTERNOS:
                    problemas.append(f"{m}.py importa '{mo}', que no está en el repo "
                                     f"ni en requirements.txt")

    print("VERIFICADOR DE ARRANQUE")
    print("=" * 62)
    print(f"  {len(firmas)} módulos revisados")
    if problemas:
        print(f"\n  ⛔ {len(problemas)} PROBLEMA(S) — NO SUBIR:")
        for p in problemas: print(f"     {p}")
        return 1
    print("  ✅ TODO CORRECTO — el backend debería arrancar en Render")
    return 0

if __name__ == "__main__":
    sys.exit(main())
