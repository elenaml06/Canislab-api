"""
CANISLAB - API real del motor nutricional

Envuelve todo el codigo Python YA VALIDADO (especies.py, der.py,
optimizador.py, optimizador_semanal.py, transicion.py, recalculo.py,
persistencia.py) como un servicio web de verdad, para que la app pueda
consultarlo por internet en vez de simular nada.

Para probarlo en local:
    pip install fastapi uvicorn --break-system-packages
    uvicorn main:app --reload
    -> abre http://localhost:8000/docs para probarlo interactivamente

Para desplegarlo de verdad (gratis o muy barato), opciones sencillas:
    - Render.com (capa gratuita, sube el codigo y listo)
    - Railway.app (capa gratuita generosa)
    - Fly.io (capa gratuita)
Cualquiera de las tres funciona con este mismo archivo sin cambios.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import date
from typing import Optional

import sys
sys.path.insert(0, ".")
from especies import cargar_alimentos, filtrar_alimentos_disponibles
from der import calcular_der
from optimizador import optimizar_menu
from optimizador_semanal import optimizar_semana
from transicion import calcular_tramo_transicion, menu_activo_y_bloqueados, nivel_indicador_nutrientes
from recalculo import anadir_alimento, quitar_alimento, cambiar_alimento
from analizador import analizar_dieta
from plantillas import PLANTILLAS, plantillas_compatibles
import persistencia

app = FastAPI(title="CANISLAB API")

# permite que la app (en el navegador) pueda llamar a esta API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # en produccion, poner aqui el dominio real de la app
    allow_methods=["*"],
    allow_headers=["*"],
)

persistencia.crear_tablas()


# ---------- modelos de entrada ----------
class PeticionDER(BaseModel):
    peso_actual_kg: float
    etapa: str
    actividad_idx: int  # 0=sedentario .. 4=trabajo
    esterilizado: bool


class PeticionMenu(BaseModel):
    peso_perro_kg: float = None
    # peso ADULTO esperado: activa el tope de calcio de raza grande en cachorros
    peso_adulto_esperado_kg: float = None
    nombres_excluidos: list = None
    patologias: list = None
    # Lo que el usuario ha elegido A MANO en Personalizar o Aprovechar. Sin
    # esto, el optimizador podia ponerlo a 0 gramos y el usuario veia que su
    # eleccion desaparecia del menu sin explicacion.
    forzar_presencia: list = None
    nombres_alimentos: list[str]
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []


class PeticionCambiarAlimento(BaseModel):
    peso_perro_kg: float = None
    nombres_excluidos: list = None
    patologias: list = None
    menu_actual: list[str]
    alimento_viejo: str
    alimento_nuevo: str
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []


class PeticionAnadirQuitarAlimento(BaseModel):
    peso_perro_kg: float = None
    nombres_excluidos: list = None
    patologias: list = None
    menu_actual: list[str]
    alimento: str
    der_objetivo: float
    etapa_requisitos: str
    especies_excluidas: list[str] = []


class PeticionTransicion(BaseModel):
    fecha_inicio: str  # "2026-07-25"
    num_menus_elegidos: int
    fecha_hoy: Optional[str] = None


# ---------- endpoints ----------

@app.post("/der")
def endpoint_der(datos: PeticionDER):
    ACTIVIDAD_KEY = ["sedentario", "normal", "activo", "muy_activo", "trabajo"]
    actividad = ACTIVIDAD_KEY[datos.actividad_idx] if datos.etapa in ("adulto", "senior") else None
    resultado = calcular_der(datos.peso_actual_kg, datos.etapa, actividad, datos.esterilizado)
    return resultado


@app.post("/menu")
def endpoint_menu(datos: PeticionMenu):
    alimentos = cargar_alimentos()
    # Se filtra SIEMPRE, aunque no haya especies excluidas: los alimentos
    # concretos que el usuario marco para evitar tambien tienen que caer.
    alimentos = filtrar_alimentos_disponibles(
        alimentos, set(datos.especies_excluidas or []), set(datos.nombres_excluidos or []))
    por_nombre = {a["nombre"]: a for a in alimentos}
    candidatos = [por_nombre[n] for n in datos.nombres_alimentos if n in por_nombre]
    if not candidatos:
        raise HTTPException(400, "Ninguno de los alimentos indicados existe en la base de datos")
    resultado = optimizar_menu(candidatos, datos.der_objetivo, datos.etapa_requisitos,
                               forzar_presencia=datos.forzar_presencia,
                               peso_perro_kg=datos.peso_perro_kg,
                               patologias=datos.patologias,
                               peso_adulto_esperado_kg=datos.peso_adulto_esperado_kg)
    # Si forzar lo que el usuario eligio deja el menu sin solucion, se
    # reintenta sin forzar: mejor darle un menu (avisando) que un error.
    if not resultado.get("factible") and datos.forzar_presencia:
        resultado = optimizar_menu(candidatos, datos.der_objetivo, datos.etapa_requisitos,
                                   peso_perro_kg=datos.peso_perro_kg,
                                   patologias=datos.patologias)
        if resultado.get("factible"):
            resultado["no_se_pudo_forzar"] = True
    return resultado


@app.post("/transicion")
def endpoint_transicion(datos: PeticionTransicion):
    fecha_inicio = date.fromisoformat(datos.fecha_inicio)
    fecha_hoy = date.fromisoformat(datos.fecha_hoy) if datos.fecha_hoy else None
    tramo = calcular_tramo_transicion(fecha_inicio, fecha_hoy)
    menus = menu_activo_y_bloqueados(fecha_inicio, datos.num_menus_elegidos, fecha_hoy)
    nivel = nivel_indicador_nutrientes(fecha_inicio, datos.num_menus_elegidos, fecha_hoy)
    return {**tramo, **menus, "nivel_indicador_nutrientes": nivel}


@app.post("/menu/cambiar")
def endpoint_cambiar_alimento(datos: PeticionCambiarAlimento):
    """Sustituye un alimento por otro (el lapiz de editar) y recalcula TODO de verdad."""
    resultado = cambiar_alimento(
        datos.menu_actual, datos.alimento_viejo, datos.alimento_nuevo,
        datos.der_objetivo, datos.etapa_requisitos, set(datos.especies_excluidas),
        peso_perro_kg=datos.peso_perro_kg,
        nombres_excluidos=set(datos.nombres_excluidos or []),
    )
    return resultado


@app.post("/menu/anadir")
def endpoint_anadir_alimento(datos: PeticionAnadirQuitarAlimento):
    """Añade un alimento (ej. un suplemento) al menu y recalcula TODO de verdad."""
    resultado = anadir_alimento(
        datos.menu_actual, datos.alimento,
        datos.der_objetivo, datos.etapa_requisitos, set(datos.especies_excluidas),
        peso_perro_kg=datos.peso_perro_kg,
        nombres_excluidos=set(datos.nombres_excluidos or []),
    )
    return resultado


@app.post("/menu/quitar")
def endpoint_quitar_alimento(datos: PeticionAnadirQuitarAlimento):
    """Quita un alimento del menu y recalcula TODO de verdad."""
    resultado = quitar_alimento(
        datos.menu_actual, datos.alimento,
        datos.der_objetivo, datos.etapa_requisitos, set(datos.especies_excluidas),
        peso_perro_kg=datos.peso_perro_kg,
        nombres_excluidos=set(datos.nombres_excluidos or []),
    )
    return resultado


@app.get("/perro/{perro_id}/menus")
def endpoint_obtener_menus(perro_id: int):
    return persistencia.obtener_menus(perro_id)


@app.get("/")
def raiz():
    return {"estado": "CANISLAB API funcionando"}


# =====================================================================
# MODO ANALIZADOR — el usuario mete lo que YA le da y le decimos que tal
# =====================================================================
class AnalisisRequest(BaseModel):
    gramos_por_alimento: dict   # {"Carcasa de pollo": 680, "Calabaza": 68, ...}
    der_objetivo: float = None  # si no viene, se calcula con peso/etapa/actividad
    etapa_requisitos: str = "Adulto"
    # alternativa a mandar el DER ya calculado: mandar el perfil del perro
    peso_kg: float = None
    etapa_der: str = None       # clave de der.py: adulto, cachorro_crecimiento...
    actividad: str = None
    esterilizado: bool = False


@app.post("/analizar")
def analizar(req: AnalisisRequest):
    der = req.der_objetivo
    if der is None:
        if req.peso_kg is None or req.etapa_der is None:
            raise HTTPException(400, "Hacen falta el DER, o bien peso y etapa del perro.")
        d = calcular_der(req.peso_kg, req.etapa_der, req.actividad, req.esterilizado)
        der = d["der"] if isinstance(d, dict) else d
    return analizar_dieta(req.gramos_por_alimento, der, req.etapa_requisitos)


@app.get("/alimentos")
def listar_alimentos():
    """Catalogo agrupado por categoria, para que la app pinte los selectores
    del analizador sin tener que llevar la lista duplicada en el frontend."""
    from especies import cargar_alimentos as _ca
    por_cat = {}
    for a in _ca():
        por_cat.setdefault(a["categoria"], []).append({
            "nombre": a["nombre"],
            "kcal_100g": a["energia"],
            "especie": a.get("especie"),
        })
    for v in por_cat.values():
        v.sort(key=lambda x: x["nombre"])
    return por_cat


# =====================================================================
# PLANTILLAS BASE VALIDADAS
# =====================================================================
class MenuPlantillaRequest(BaseModel):
    der_objetivo: float
    etapa_requisitos: str = "Adulto"
    peso_perro_kg: float = None
    especies_excluidas: list = []
    plantilla_id: str = None   # si no viene, se elige rotando


@app.get("/plantillas")
def listar_plantillas(especies_excluidas: str = ""):
    """Plantillas disponibles para este perro. especies_excluidas separadas
    por comas, p.ej. ?especies_excluidas=Pollo,Pavo"""
    excl = {e.strip() for e in especies_excluidas.split(",") if e.strip()}
    catalogo = {a["nombre"]: a for a in cargar_alimentos()}
    disponibles = plantillas_compatibles(excl, catalogo)
    return [{"id": p["id"], "nombre": p["nombre"], "descripcion": p["descripcion"],
             "n_alimentos": len(p["alimentos"])} for p in disponibles]


@app.post("/menu/plantilla")
def menu_desde_plantilla(req: MenuPlantillaRequest):
    """Genera el menu a partir de una plantilla ya validada. Los gramos los
    calcula el optimizador igual que siempre, con todas sus restricciones."""
    excl = set(req.especies_excluidas or [])
    catalogo = {a["nombre"]: a for a in cargar_alimentos()}
    disponibles = plantillas_compatibles(excl, catalogo)
    if not disponibles:
        raise HTTPException(400, "No hay ninguna plantilla compatible con las "
                                 "alergias de este perro. Prueba el modo personalizado.")

    if req.plantilla_id:
        elegida = next((p for p in disponibles if p["id"] == req.plantilla_id), None)
        if elegida is None:
            raise HTTPException(404, "Esa plantilla no existe o no es compatible.")
        candidatas = [elegida]
    else:
        candidatas = disponibles

    # Se prueban en orden: primero las compactas (menos alimentos, mas facil
    # de preparar) y, si para este perro concreto no cuadran, las completas.
    # No todas las compactas valen para todos los tamaños: las dosis de
    # suplemento van por tramos de peso mientras que las necesidades escalan
    # de forma continua, asi que a algunos perros les hace falta mas variedad
    # de comida real. El usuario recibe siempre la mas sencilla que funcione.
    ultimo_motivo = None
    for p in sorted(candidatas, key=lambda x: (not x.get("compacta"), len(x["alimentos"]))):
        alimentos = [catalogo[n] for n in p["alimentos"] if n in catalogo]
        tope = 0.40 if p.get("compacta") else 0.30
        r = optimizar_menu(alimentos, req.der_objetivo, req.etapa_requisitos,
                           peso_perro_kg=req.peso_perro_kg, tope_por_alimento=tope)
        if r["factible"]:
            r["plantilla"] = {"id": p["id"], "nombre": p["nombre"],
                              "descripcion": p["descripcion"],
                              "compacta": bool(p.get("compacta"))}
            return r
        ultimo_motivo = r.get("motivo")
    raise HTTPException(400, ultimo_motivo or "Ninguna plantilla cuadra para este perro.")
