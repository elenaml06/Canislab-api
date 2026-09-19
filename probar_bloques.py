# -*- coding: utf-8 -*-
"""
CANISLAB — CORRER **UNOS POCOS** BLOQUES DE LA BATERIA, NO LOS 98.

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
sueltas. Partirlo en 98 modulos seria un cambio grande y arriesgado en el unico
sitio del repo que no se puede permitir un fallo silencioso.

Asi que esto no lo parte: lo RECORTA. Lee el fichero, encuentra los `# BLOQUE N`
--que son los mismos marcadores que ya usa el cronometro-- y ejecuta la CABECERA
COMUN mas los bloques que se le pidan. Nada del fichero original se toca.

    python3 probar_bloques.py 95          # solo el 95
    python3 probar_bloques.py 43 95       # dos
    python3 probar_bloques.py 90-95       # un rango
    python3 probar_bloques.py --rapida    # todos los BARATOS, para iterar

⚠️ EL MODO RAPIDO (18 de septiembre de 2026), y el porque es de Elena otra vez:
«tenemos que hacer algo para poder bajar el tiempo de las baterias..... es una
locura y tardamos dias en aplicar cosas diminutas» y «¿la gente que hace apps lo
hace asi, tirando baterias infinitas cada vez que hacen un cambio por minimo que
sea?».

No. La forma normal es una piramide: segundos en cada cambio, un par de minutos
al abrir el PR, y la larga antes de publicar. Aqui se estaba corriendo la de
«antes de publicar» para cambiar un texto.

`--rapida` corre TODOS los bloques que cuestan poco -- no una seleccion a mano,
que es lo que se desincroniza -- y deja fuera los que resuelven menus de verdad
con el solver, que es donde se va la mitad del reloj. La lista sale de
`reparto_de_la_bateria.json`, que **escribe la propia bateria al terminar**: es
una MEDIDA, no una opinion, y el dia que un bloque engorde se cae solo del modo
rapido sin que nadie tenga que acordarse.

⚠️ Y FALLA HACIA CORRER, NO HACIA SALTAR. Un bloque que no este en la medida
--porque es nuevo-- se ejecuta igual y se dice. Al reves seria lo peor posible:
un bloque nuevo que no corre en el bucle rapido y nadie se entera.

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
#
# ⚠️ Y PIDE EL SEPARADOR, QUE NO ES UN DETALLE (19 de septiembre de 2026). La
# regla era `^# BLOQUE (\d+)\b`, y `pruebas_completas.py` NOMBRA a otros bloques
# dentro de sus comentarios: «# BLOQUE 65 ancla 25 cifras de ...», «# BLOQUE 43,
# no de aqui.», «# BLOQUE 25 -- y por el mismo motivo...». Cuatro lineas de
# prosa que se leian como si fueran el principio de un bloque.
#
# Lo que hacia no era dar error: `trozos[n]` se quedaba con la ULTIMA aparicion,
# asi que el BLOQUE 65 de verdad --el que comprueba el documento que va a
# revision-- dejaba de existir y en su sitio entraban tres lineas de comentario.
# Pedirlo solo era pedir un bloque que no se ejecutaba, en silencio; y el BLOQUE
# 66, que lee una variable suya, moria con un NameError que no tenia nada que
# ver. Medido: con la regla vieja salian 128 marcas para 124 bloques.
#
# El separador es «—» o «:» porque las dos formas estan en el fichero (los
# BLOQUES 35, 36 y 80 usan «:»); lo que no vale es «,», «.», «--» ni una palabra
# pegada, que es como se escribe una REFERENCIA a otro bloque.
_MARCA = re.compile(r"^# BLOQUE (\d+) ?[—:] ", re.M)


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
    # ⚠️ Y DOS BLOQUES CON EL MISMO NUMERO SE DICEN EN VOZ ALTA, no se pisan. Ya
    # ha pasado tres veces en el repo (los dos BLOQUE 98 del 13 de septiembre, y
    # el 100 -> 101 -> 104), y aqui el efecto es peor que una referencia rota: el
    # segundo se come al primero y el primero deja de ejecutarse SIN QUE NADIE LO
    # DIGA.
    _vistos = {}
    for n, linea in inicios:
        if n in _vistos:
            raise SystemExit(
                f"hay DOS bloques con el numero {n} en pruebas_completas.py "
                f"(lineas {_vistos[n] + 1} y {linea + 1}). Un numero de bloque es la "
                f"unica forma que tiene el repo de decir quien vigila que: "
                f"renumera uno de los dos antes de seguir.")
        _vistos[n] = linea
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


# Cuanto puede costar un bloque para seguir siendo «barato». No es una cifra de
# ninguna fuente: es donde esta el corte natural de la medida -- por debajo
# estan los que no resuelven menus, por encima los que si.
SEGUNDOS_PARA_SER_RAPIDO = float(os.environ.get("CANISLAB_SEGUNDOS_RAPIDO", "8"))
MEDIDA = os.path.join(RAIZ, "reparto_de_la_bateria.json")


def _los_rapidos(trozos):
    """Los bloques baratos, segun la ultima medida de la bateria entera."""
    import json
    if not os.path.exists(MEDIDA):
        raise SystemExit(
            f"falta «{os.path.basename(MEDIDA)}», que es de donde sale la lista de bloques\n"
            f"baratos. Lo escribe la bateria entera al terminar, asi que hace falta correrla\n"
            f"una vez:  python3 pruebas_completas.py")
    medida = {int(x["bloque"]): x["segundos"]
              for x in json.load(open(MEDIDA, encoding="utf-8"))["bloques"]}
    rapidos, lentos, sin_medir = [], [], []
    for n in sorted(trozos):
        if n not in medida:
            sin_medir.append(n)
            rapidos.append(n)          # un bloque nuevo CORRE, no se salta
        elif medida[n] < SEGUNDOS_PARA_SER_RAPIDO:
            rapidos.append(n)
        else:
            lentos.append(n)
    return rapidos, lentos, sin_medir, medida


def _el_reparto(trozos, cual, de_cuantos):
    """Los bloques del trabajo `cual` de `de_cuantos`, equilibrados por TIEMPO.

    ⚠️ POR QUÉ NO SE PARTEN POR NÚMERO (18 de septiembre de 2026). La bateria
    entera son 71 minutos y el reparto NO es plano: los diez bloques mas caros
    se llevan la mitad, y el BLOQUE 50 el solo son 8 minutos. Partir «del 1 al
    30, del 31 al 60...» dejaria un trabajo de 30 minutos al lado de uno de
    cinco, y la CI tarda lo que tarde EL MAS LENTO -- o sea que no se ganaria
    casi nada.

    Se reparte por el reloj MEDIDO, con el mas caro al trabajo que menos lleva
    acumulado. Medido sobre el reparto de hoy:

        con 2 trabajos: el mas largo 35,7 min
        con 3 trabajos:              23,8 min
        con 4 trabajos:              17,8 min   <- 71 -> 18
        con 6 trabajos:              11,9 min

    ⚠️ Y UN BLOQUE SIN MEDIR VA AL TRABAJO 1, no se queda fuera. Es la misma
    regla que el modo rapido: fallar hacia CORRER. Un bloque nuevo que se
    cayera de todos los trabajos no lo ejecutaria nadie y la CI saldria verde.
    """
    import json
    if not os.path.exists(MEDIDA):
        raise SystemExit(f"falta «{os.path.basename(MEDIDA)}». Lo escribe la bateria entera.")
    medida = {int(x["bloque"]): x["segundos"]
              for x in json.load(open(MEDIDA, encoding="utf-8"))["bloques"]}
    trabajos = [[0.0, []] for _ in range(de_cuantos)]
    for n in sorted(trozos, key=lambda n: -medida.get(n, 0.0)):
        if n not in medida:
            trabajos[0][1].append(n)
            continue
        t = min(trabajos, key=lambda t: t[0])
        t[0] += medida[n]
        t[1].append(n)
    mios, segundos = sorted(trabajos[cual - 1][1]), trabajos[cual - 1][0]
    print(f"  TRABAJO {cual} de {de_cuantos}: {len(mios)} bloques, ~{segundos / 60:.0f} min "
          f"de los ~{sum(medida.values()) / 60:.0f} que cuesta la bateria entera")
    print(f"  ⚠️  Esto NO es la bateria: es un TROZO. Verde aqui solo dice que estos pasan.\n")
    return mios


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
    """En que bloque aparece `nombre` por primera vez, si es que aparece.

    ⚠️ NO BASTA CON MIRAR LAS ASIGNACIONES, y esto costo una tirada perdida:
    aqui solo se buscaba `nombre =`, y el BLOQUE 23 necesita `_os_b18`, que no
    se asigna en ningun sitio -- se crea con `import os as _os_b18`. Asi que la
    herramienta decia «no se ha encontrado quien lo define» de un nombre que
    esta a la vista en el BLOQUE 18. Se buscan las cuatro formas en que un
    bloque puede crear un nombre: asignarlo, importarlo con alias, importarlo
    a secas, y definir una funcion o una clase con ese nombre.
    """
    n_ = re.escape(nombre)
    patrones = [
        re.compile(r"^\s*" + n_ + r"\s*(?:,[^=]*)?=[^=]", re.M),      # x = ...
        re.compile(r"^\s*(?:import|from)\b.*\bas\s+" + n_ + r"\b", re.M),  # import y as x
        re.compile(r"^\s*import\s+" + n_ + r"\b", re.M),              # import x
        re.compile(r"^\s*from\b.*\bimport\b[^#]*\b" + n_ + r"\b", re.M),  # from y import x
        re.compile(r"^\s*(?:def|class)\s+" + n_ + r"\b", re.M),       # def x(...)
    ]
    for n in sorted(trozos):
        if any(p.search(trozos[n]) for p in patrones):
            return n
    return None


def main():
    if len(sys.argv) < 2:
        raise SystemExit(__doc__)
    cabecera, trozos = _trozos()
    if sys.argv[1].startswith("--reparto"):
        # --reparto 2/4  ->  el segundo trabajo de cuatro
        _cual, _de = (sys.argv[2] if len(sys.argv) > 2 else sys.argv[1].split("=")[-1]).split("/")
        quiero = _el_reparto(trozos, int(_cual), int(_de))
    elif sys.argv[1] in ("--rapida", "--rapido"):
        quiero, lentos, sin_medir, medida = _los_rapidos(trozos)
        _t_rap = sum(medida.get(n, 0.0) for n in quiero)
        _t_len = sum(medida.get(n, 0.0) for n in lentos)
        print(f"  MODO RAPIDO: {len(quiero)} bloques de {len(trozos)} "
              f"(~{_t_rap / 60:.0f} min de ~{(_t_rap + _t_len) / 60:.0f})")
        print(f"  NO se ejecutan los {len(lentos)} que resuelven menus con el solver: "
              f"{lentos}")
        if sin_medir:
            print(f"  ⚠️  y {len(sin_medir)} sin medir todavia (bloques nuevos), que SI se "
                  f"ejecutan: {sin_medir}")
        print()
    else:
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

    # ⚠️ LAS DEPENDENCIAS SE RESUELVEN SOLAS DESDE EL 12 DE SEPTIEMBRE, Y ESTE
    # ES EL CAMBIO QUE HACE QUE LA HERRAMIENTA SE USE.
    #
    # Antes, cuando faltaba un nombre, esto decia quien lo definia y te pedia
    # que volvieras a lanzarlo a mano. Suena a poco y no lo es: la noche del 11
    # al 12 de septiembre paso CUATRO veces, y una de ellas en cadena -- pedir
    # el 23 mandaba al 18, el 18 al 5 y el 5 al 1, o sea cuatro tiradas para
    # probar un bloque. Con esa friccion lo que se acaba haciendo es lanzar la
    # bateria entera, que son 40 minutos, que es exactamente lo que esta
    # herramienta existe para evitar. Elena, viendome lanzarla cuatro veces
    # seguidas: «dijimos que ibamos a hacer algo para no tener que lanzar las
    # baterias completas cada vez».
    #
    # Asi que ahora el bucle lo hace ella: lanza, y si el NameError apunta a un
    # bloque que puede anadir, lo anade y vuelve a lanzar. Se para cuando corre
    # o cuando no hay nada mas que anadir -- nunca da vueltas infinitas, porque
    # cada vuelta anade al menos un bloque y son finitos.
    #
    # LO QUE **NO** CAMBIA: los bloques que arrastra se DICEN, siempre. Que una
    # herramienta anada medio fichero en silencio seria peor que el NameError,
    # porque entonces «he probado el bloque 52» y «he probado media bateria»
    # se leen igual. Y sigue sin sustituir a la bateria entera: lo dice al
    # final de cada tirada.
    arrastrados = []
    intento = 0
    while True:
        intento += 1
        bloques = sorted(set(quiero) | set(arrastrados))
        codigo = (falso_file + cabecera
                  + "".join(trozos[n] for n in bloques) + final)
        destino = os.path.join("/tmp", f"bloques_{'_'.join(map(str, bloques))}.py")
        open(destino, "w", encoding="utf-8").write(codigo)
        if arrastrados:
            print(f"  bloques {sorted(set(quiero))} + {sorted(set(arrastrados))} "
                  f"(arrastrados por las variables que comparten) · "
                  f"{codigo.count(chr(10))} lineas · {destino}\n")
        else:
            print(f"  bloques {bloques} · {codigo.count(chr(10))} lineas · {destino}\n")

        # En un proceso aparte, con el mismo cwd: los bloques abren ficheros por
        # ruta relativa igual que la bateria.
        proceso = subprocess.run([sys.executable, destino], cwd=RAIZ,
                                 capture_output=True, text=True)

        m = re.search(r"NameError: name '([^']+)' is not defined", proceso.stderr or "")
        if not m:
            break
        quien = _quien_define(m.group(1), trozos)
        if quien is None or quien in bloques:
            # O no se sabe quien lo define, o ya esta dentro y el problema es
            # otro (un orden que no se puede arreglar anadiendo bloques).
            sys.stdout.write(proceso.stdout)
            sys.stderr.write(proceso.stderr)
            print("\n" + "=" * 60)
            if quien is None:
                print(f"  Falta «{m.group(1)}» y no se ha encontrado quien lo define. "
                      f"Puede venir de un import o de la cabecera.")
            else:
                print(f"  Falta «{m.group(1)}» y el BLOQUE {quien} que lo define YA esta "
                      f"dentro. Entonces no es una dependencia que falte: mira el orden.")
            sys.exit(proceso.returncode)
        print(f"  falta «{m.group(1)}» · lo define el BLOQUE {quien} · lo anado y repito\n")
        arrastrados.append(quien)

    sys.stdout.write(proceso.stdout)
    sys.stderr.write(proceso.stderr)
    if arrastrados:
        print(f"\n  (se han arrastrado los bloques {sorted(set(arrastrados))} porque los "
              f"pedidos usan variables suyas.\n   Lo que se ha ejecutado son "
              f"{len(bloques)} bloques, no {len(set(quiero))}.)")
    sys.exit(proceso.returncode)


if __name__ == "__main__":
    main()
