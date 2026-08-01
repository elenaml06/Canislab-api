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
    nombres_alimentos: list[str]
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
    if datos.especies_excluidas:
        alimentos = filtrar_alimentos_disponibles(alimentos, set(datos.especies_excluidas))
    por_nombre = {a["nombre"]: a for a in alimentos}
    candidatos = [por_nombre[n] for n in datos.nombres_alimentos if n in por_nombre]
    if not candidatos:
        raise HTTPException(400, "Ninguno de los alimentos indicados existe en la base de datos")
    resultado = optimizar_menu(candidatos, datos.der_objetivo, datos.etapa_requisitos)
    return resultado


@app.post("/transicion")
def endpoint_transicion(datos: PeticionTransicion):
    fecha_inicio = date.fromisoformat(datos.fecha_inicio)
    fecha_hoy = date.fromisoformat(datos.fecha_hoy) if datos.fecha_hoy else None
    tramo = calcular_tramo_transicion(fecha_inicio, fecha_hoy)
    menus = menu_activo_y_bloqueados(fecha_inicio, datos.num_menus_elegidos, fecha_hoy)
    nivel = nivel_indicador_nutrientes(fecha_inicio, datos.num_menus_elegidos, fecha_hoy)
    return {**tramo, **menus, "nivel_indicador_nutrientes": nivel}


@app.get("/perro/{perro_id}/menus")
def endpoint_obtener_menus(perro_id: int):
    return persistencia.obtener_menus(perro_id)


@app.get("/")
def raiz():
    return {"estado": "CANISLAB API funcionando"}
