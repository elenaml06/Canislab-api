# -*- coding: utf-8 -*-
"""
HASTA DONDE PUEDE MOVER UN VETERINARIO CADA CIFRA, Y HASTA DONDE NO.

⚠️ POR QUE EXISTE (10 de septiembre). Elena lo pidio asi: «tenemos que
estipular que porcentajes puede variar el veterinario y cuales NO, y hasta
que punto o que techo, dentro de cada patologia, de cada caso concreto».

La respuesta ya estaba escrita, y ese era justo el problema: estaba en PROSA,
repartida entre el campo `por_que` de cada cifra de `patologias.json` («Margen
del profesional: 13,75 a 37,5») y el §2 de `PATOLOGIAS.md`. Una frase no se
ejecuta. Es literalmente el fallo que hizo nacer `auditar_conversiones.py`: una
conversion contada en prosa se copio x25 en vez de x2,5, tenia forma de dato
bueno, y lo unico que la cazo fue que alguien la leyo.

Y no es prosa inofensiva: la de la pancreatitis dice «Margen del profesional:
13,75 a 37,5» y el motor aplica 37,5 o 25 segun el perro. La frase se quedo
en la version de antes del tope condicional.

LO QUE HACE ESTE MODULO. Resuelve una CLAVE DE PROCEDENCIA a un numero vivo:

    minimo_fediaf:Grasa_total   -> el minimo de FEDIAF de ese requisito, HOY
    maximo_fediaf:Sodio         -> su maximo, HOY, y None si no tiene
    legal_ue:24_cardiaca:sodio  -> la cifra del Reglamento (UE) 2020/354
    seguridad:TOPE_VITD_KCAL    -> el tope de seguridad cronica
    sin_techo                   -> declarado a proposito: nadie pone techo

Asi el margen de cada cifra no es un numero copiado sino una CUENTA que se
rehace, y `auditar_margen_profesional.py` (BLOQUE 80) la rehace entera.

LAS TRES REGLAS QUE SALEN DE LAS FUENTES, y ninguna es opinion nuestra:

  1. **Por debajo del minimo de FEDIAF hace falta firma.** FEDIAF excluye de
     su ambito los alimentos para objetivos nutricionales especificos, y el
     Reglamento (UE) 2020/354 es donde estan: esa es la ruta legitima para
     salirse, y la recorre un profesional. Es la frontera de `VETERINARIOS.md`.
  2. **Por encima del techo legal no se sale nadie.** Ni el motor ni un
     veterinario: el techo del Reglamento es el techo.
  3. **Un techo terapeutico no autoriza a bajar de FEDIAF.** Lo dice la propia
     norma en su nota al pie (11): «The minimum recommendations according to the
     FEDIAF Nutritional Guidelines for all essential fatty acids shall be met in
     the daily ration». Es la regla 3 de `CLAUDE.md` en el Diario Oficial.

⚠️ Y LO QUE NO DICE NINGUNA FUENTE, que hay que decirlo con precision para no
citarla mal: el Reglamento **no da un rango de maniobra por nutriente**. Da un
techo o un suelo por objetivo. El unico rango que escribe es el del TIEMPO
(«inicialmente hasta 6 meses»), y su parte A punto 2 pone un +/-15 % que es
**tolerancia analitica de etiquetado**, no margen clinico -- citarlo como «se
puede subir un 15 %» seria un error. El rango de una cifra, cuando existe, lo
escribe SACN5 en sus tablas de key nutritional factors, y por eso el campo
`rango_de_la_fuente` sale de la conversion de esa tabla y no de aqui.
"""
import json, os

_AQUI = os.path.dirname(os.path.abspath(__file__))
_RUTA_LEGAL = os.path.join(_AQUI, "..", "limites_legales_ue_2020_354.json")

# El perro de referencia contra el que se publican los margenes. Se elige
# ADULTO a DER 95 y no otra cosa por un motivo: es el mismo perro con el que
# `PATOLOGIAS.md` §2 escribe sus margenes en prosa, asi que los dos numeros se
# pueden comparar. ⚠️ Y hay que decir en voz alta lo que esto NO es: los
# minimos de FEDIAF SUBEN cuando el perro come menos (`minimo_de()`, ecuacion
# 7.2.5), asi que en un perro pequeno el suelo esta MAS ALTO que aqui y el
# margen de apretado es mas corto. El margen publicado es el del perro de
# referencia; el que decide si un menu sale es el del perro que tienes delante,
# y ese lo comprueba `_garantizar_verificado` con la DER de verdad.
DER_DE_REFERENCIA = 95.0
ETAPA_DE_REFERENCIA = "Adulto"


def cargar_legal(ruta=None):
    with open(ruta or _RUTA_LEGAL, encoding="utf-8") as f:
        return json.load(f)


LEGAL = cargar_legal()


def _requisito(req, nombre):
    for r in req:
        if r.get("nutriente") == nombre:
            return r
    return None


def resolver(clave, req, etapa=None, der_efectiva=None):
    """Un numero VIVO a partir de su clave de procedencia.

    Devuelve (valor, explicacion). El valor puede ser None cuando la clave
    declara a proposito que no hay limite -- `sin_techo` y un maximo de FEDIAF
    que no existe son cosas distintas de un error, y por eso se distinguen aqui
    y no en el que llama.
    """
    from verificar import minimo_de, maximo_de

    etapa = etapa or ETAPA_DE_REFERENCIA
    if der_efectiva is None:
        der_efectiva = DER_DE_REFERENCIA

    if clave == "sin_techo":
        return None, ("nadie pone techo por arriba: ni FEDIAF, ni el Reglamento "
                      "(UE) 2020/354, ni un tope de seguridad cronica")
    if clave == "sin_suelo":
        return None, ("no hay minimo de FEDIAF para este nutriente, asi que por "
                      "abajo no hay frontera de firma")

    cabeza, _, resto = clave.partition(":")

    if cabeza == "minimo_fediaf":
        r = _requisito(req, resto)
        if r is None:
            raise KeyError("no existe el requisito de FEDIAF %r" % resto)
        return minimo_de(r, resto, etapa, der_efectiva=der_efectiva), (
            "minimo de FEDIAF de %s en %s a DER %g" % (resto, etapa, der_efectiva))

    if cabeza == "maximo_fediaf":
        r = _requisito(req, resto)
        if r is None:
            raise KeyError("no existe el requisito de FEDIAF %r" % resto)
        return maximo_de(r, resto, etapa), (
            "maximo de FEDIAF de %s en %s" % (resto, etapa))

    if cabeza == "legal_ue":
        entrada, _, nutriente = resto.partition(":")
        e = LEGAL["entradas"].get(entrada)
        if e is None:
            raise KeyError("no existe la entrada %r del Reglamento 2020/354" % entrada)
        for lim in e["limites"]:
            if lim["nutriente"] == nutriente:
                return float(lim["por_1000kcal"]), (
                    "Reglamento (UE) 2020/354, entrada %s: %s" % (entrada, lim["literal"]))
        raise KeyError("la entrada %r no pone cifra a %r" % (entrada, nutriente))

    if cabeza == "seguridad":
        import seguridad
        if not hasattr(seguridad, resto):
            raise KeyError("no existe el tope de seguridad %r" % resto)
        return float(getattr(seguridad, resto)), (
            "tope de seguridad cronica %s, que es una restriccion dura del "
            "solver y no un aviso" % resto)

    raise KeyError("clave de procedencia desconocida: %r" % clave)
