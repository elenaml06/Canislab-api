# -*- coding: utf-8 -*-
"""
CANISLAB — CORRER **UNOS POCOS** BLOQUES DE LA BATERIA, NO LOS 97.

⚠️ POR QUE EXISTE (11 de septiembre de 2026). Elena: «pero ¿de verdad cada vez
que se hace un bloque es necesario lanzar toda la bateria????».

No. Y que no se pudiera era un fallo de la bateria, no una regla del proyecto.
Lo que el CLAUDE.md pide es ejecutarla entera **antes de ENTREGAR** un cambio, y
eso no cambia: sigue siendo la puerta, y ademas la corre GitHub Actions en cada
empujon. Lo que no tiene sentido es esperar 33 minutos para saber si el bloque
que acabas de escribir funciona -- y eso es lo que se ha estado haciendo hoy,
tres veces seguidas.

COMO FUNCIONA, Y POR QUE ASI. `pruebas_completas.py` es UN solo fichero de
codigo de arriba abajo: no hay funciones por bloque que se puedan llamar
sueltas. Partirlo en 97 modulos seria un cambio grande y arriesgado en el unico
sitio del repo que no se puede permitir un fallo silencioso.

Asi que esto no lo parte: lo RECORTA. Lee el fichero, encuentra los `# BLOQUE N`
--que son los mismos marcadores que ya usa el cronometro-- y ejecuta la CABECERA
COMUN mas los bloques que se le pidan. Nada del fichero original se toca.

    python3 probar_bloques.py 95          # solo el 95
    python3 probar_bloques.py 43 95       # dos
    python3 probar_bloques.py 90-95       # un rango

⚠️ LO QUE ESTO **NO** ES, Y HAY QUE DECIRLO CLARO. No sustituye a la bateria:
    · Un bloque puede usar variables que define OTRO de mas arriba (`_al43`,
      `_c`, `_req_b16`...). Si pasa, esto falla con un NameError que dice
      exactamente que falta, y se anade ese bloque a la lista. No lo adivina
      solo, y no lo debe adivinar: adivinarlo seria arrastrar medio fichero y
      volver a tardar lo mismo.
    · Y sobre todo: un cambio puede romper un bloque que no se te ocurrio
      mirar. ESO es lo que caza la bateria entera, y por eso sigue siendo la
      unica que vale para entregar.

O sea: esto es para el bucle de escribir, y la bateria para el de entregar.
"""
import os
import re
import subprocess
import sys

RAIZ = os.path.dirname(os.path.abspath(__file__))
FICHERO = os.path.join(RAIZ, "pruebas_completas.py")
# El marcador es el mismo que usa el cronometro de la bateria: si alguien cambia
# la forma de los titulos, los dos se enteran a la vez.
_MARCA = re.compile(r"^# BLOQUE (\d+)\b", re.M)


def _trozos():
    """(numero, primera_linea, ultima_linea) de cada bloque, y la cabecera."""
    texto = open(FICHERO, encoding="utf-8").read()
    lineas = texto.splitlines(keepends=True)
    inicios = []
    for m in _MARCA.finditer(texto):
        n = int(m.group(1))
        linea = texto[:m.start()].count("\n")
        # El separador de «=» de arriba forma parte del bloque, igual que el
        # comentario largo que lo explica.
        while linea > 0 and lineas[linea - 1].startswith("# ====="):
            linea -= 1
        inicios.append((n, linea))
    if not inicios:
        raise SystemExit("no se ha encontrado ningun «# BLOQUE N» en pruebas_completas.py")
    cabecera = "".join(lineas[:inicios[0][1]])
    # ⚠️ EL FINAL DEL FICHERO NO ES PARTE DEL ULTIMO BLOQUE. Detras del ultimo
    # vienen el resumen de tiempos, el aviso de los bloques que necesitan
    # `canislab-fuentes` y el `sys.exit(1)`, y todo eso usa variables que
    # definen bloques de por medio (`_os_b18`). Arrastrarlo hacia una tirada de
    # dos bloques hacia que fallara SIEMPRE, con un NameError que no tenia nada
    # que ver con lo que se estaba probando. Se corta en el cierre del
    # cronometro, que es la primera linea del pie.
    # El pie empieza en la primera de estas dos, la que salga antes.
    _PIE = ("_hay_fuentes = ", "_cerrar_el_ultimo_bloque()")
    _fin_del_ultimo = len(lineas)
    for j, l in enumerate(lineas):
        if j > inicios[-1][1] and any(l.startswith(m) for m in _PIE):
            _fin_del_ultimo = j
            break
    trozos = {}
    for i, (n, ini) in enumerate(inicios):
        fin = inicios[i + 1][1] if i + 1 < len(inicios) else _fin_del_ultimo
        trozos[n] = "".join(lineas[ini:fin])
    return cabecera, trozos


def _pedidos(argv):
    fuera = []
    for a in argv:
        if "-" in a and not a.startswith("-"):
            desde, hasta = a.split("-", 1)
            fuera.extend(range(int(desde), int(hasta) + 1))
        else:
            fuera.append(int(a))
    return fuera


def _quien_define(nombre, trozos):
    """En que bloque se asigna `nombre` por primera vez, si es que se asigna."""
    patron = re.compile(r"^\s*" + re.escape(nombre) + r"\s*(?:,[^=]*)?=[^=]", re.M)
    for n in sorted(trozos):
        if patron.search(trozos[n]):
            return n
    return None


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cabecera, trozos = _trozos()
    quiero = _pedidos(sys.argv[1:])
    faltan = [n for n in quiero if n not in trozos]
    if faltan:
        raise SystemExit(f"no existen los bloques {faltan}. Hay del "
                         f"{min(trozos)} al {max(trozos)}.")

    # El final de la bateria -- el recuento y el `sys.exit(1)` -- se vuelve a
    # escribir aqui en vez de recortarse: el del fichero trae el resumen de
    # tiempos y el aviso de los bloques que necesitan `canislab-fuentes`, y eso
    # no tiene sentido en una tirada de dos bloques.
    final = '''
print("\\n" + "=" * 60)
if fallos:
    print(f"\\u274c {len(fallos)} FALLOS:\\n")
    for x in fallos:
        print("  -", x)
    sys.exit(1)
print("\\u2705 sin fallos en los bloques pedidos")
print("\\u26a0\\ufe0f  Esto NO es la bateria: solo dice que ESTOS bloques pasan.")
print("   Antes de entregar, `python3 pruebas_completas.py` entera.")
sys.exit(0)
'''
    # ⚠️ `__file__` SE FALSEA A PROPOSITO, Y ES OBLIGATORIO. El fichero
    # extraido vive en /tmp y varios bloques sacan la raiz del repo de
    # `Path(__file__).parent` (el 24 con `patologias.json`, el 46, y los que
    # lanzan auditores con `cwd=dirname(__file__)`). Sin esto buscarian
    # `/tmp/patologias.json` y darian un FileNotFoundError que no tiene nada
    # que ver con el bloque que se esta probando.
    falso_file = ("__file__ = %r\n" % os.path.join(RAIZ, "pruebas_completas.py"))
    codigo = (falso_file + cabecera
              + "".join(trozos[n] for n in sorted(set(quiero))) + final)
    destino = os.path.join("/tmp", f"bloques_{'_'.join(map(str, sorted(set(quiero))))}.py")
    open(destino, "w", encoding="utf-8").write(codigo)
    print(f"  bloques {sorted(set(quiero))} · {codigo.count(chr(10))} lineas · {destino}\n")
    # En un proceso aparte, con el mismo cwd: los bloques abren ficheros por
    # ruta relativa igual que la bateria.
    proceso = subprocess.run([sys.executable, destino], cwd=RAIZ,
                             capture_output=True, text=True)
    sys.stdout.write(proceso.stdout)
    sys.stderr.write(proceso.stderr)

    # ⚠️ Y SI FALTA UN NOMBRE, SE DICE QUIEN LO DEFINE. Un `NameError: '_c'` a
    # secas obliga a abrir el fichero de 14.000 lineas y buscar a mano, que es
    # justo el trabajo que esta herramienta existe para quitar. Se busca donde
    # se asigna ese nombre y se dice en que bloque cae.
    m = re.search(r"NameError: name '([^']+)' is not defined", proceso.stderr or "")
    if m:
        quien = _quien_define(m.group(1), trozos)
        print("\n" + "=" * 60)
        if quien is None:
            print(f"  Falta «{m.group(1)}» y no se ha encontrado quien lo define. "
                  f"Puede venir de un import o de la cabecera.")
        else:
            print(f"  Falta «{m.group(1)}», y lo define el BLOQUE {quien}. Prueba con:\n"
                  f"      python3 probar_bloques.py {quien} "
                  f"{' '.join(str(n) for n in sorted(set(quiero)))}")
        print("  (esto es lo esperado: los bloques comparten variables y esta "
              "herramienta\n   no adivina cuales -- adivinarlas seria arrastrar "
              "medio fichero.)")
    sys.exit(proceso.returncode)


if __name__ == "__main__":
    main()
