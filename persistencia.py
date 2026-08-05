"""
CANISLAB - Persistencia real (punto 5 del plan de backend)

Guarda de verdad en una base de datos (SQLite para la prueba -- en
produccion seria Postgres o similar, pero el esquema y la logica son
los mismos): perfil del perro, menus generados, fecha de inicio de la
transicion, e historial de peso. Nada vive solo en la pantalla.
"""
import sqlite3
import json
from datetime import date

RUTA_DB = "canislab.db"


def crear_tablas(ruta_db=RUTA_DB):
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.executescript("""
    CREATE TABLE IF NOT EXISTS perros (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        sexo TEXT,
        raza TEXT,
        tamano TEXT,
        peso_adulto_esperado_kg REAL,
        fecha_nacimiento TEXT,
        esterilizado INTEGER,
        actividad TEXT,
        especies_excluidas TEXT,  -- JSON: ["Pollo", "Pavo"]
        patologias TEXT           -- JSON
    );

    CREATE TABLE IF NOT EXISTS historial_peso (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perro_id INTEGER NOT NULL,
        fecha TEXT NOT NULL,
        peso_kg REAL NOT NULL,
        condicion_corporal TEXT,
        FOREIGN KEY (perro_id) REFERENCES perros(id)
    );

    CREATE TABLE IF NOT EXISTS menus (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perro_id INTEGER NOT NULL,
        nombre TEXT NOT NULL,       -- "Menú 1", "Menú 2"...
        alimentos_gramos TEXT NOT NULL,  -- JSON: {"Cuello de ternera": 559, ...}
        kcal_total REAL,
        creado_en TEXT NOT NULL,
        FOREIGN KEY (perro_id) REFERENCES perros(id)
    );

    CREATE TABLE IF NOT EXISTS transiciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        perro_id INTEGER NOT NULL,
        dieta_anterior TEXT NOT NULL,  -- "pienso" | "cocinada"
        fecha_inicio TEXT NOT NULL,
        num_menus_elegidos INTEGER NOT NULL,
        FOREIGN KEY (perro_id) REFERENCES perros(id)
    );
    """)
    con.commit()
    con.close()


def guardar_perro(datos: dict, ruta_db=RUTA_DB) -> int:
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO perros (nombre, sexo, raza, tamano, peso_adulto_esperado_kg,
                             fecha_nacimiento, esterilizado, actividad,
                             especies_excluidas, patologias)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datos["nombre"], datos.get("sexo"), datos.get("raza"), datos.get("tamano"),
        datos.get("peso_adulto_esperado_kg"), datos.get("fecha_nacimiento"),
        int(datos.get("esterilizado", False)), datos.get("actividad"),
        json.dumps(datos.get("especies_excluidas", [])),
        json.dumps(datos.get("patologias", [])),
    ))
    perro_id = cur.lastrowid
    con.commit()
    con.close()
    return perro_id


def registrar_peso(perro_id: int, peso_kg: float, condicion_corporal: str = None,
                    fecha: str = None, ruta_db=RUTA_DB):
    fecha = fecha or date.today().isoformat()
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO historial_peso (perro_id, fecha, peso_kg, condicion_corporal) VALUES (?, ?, ?, ?)",
        (perro_id, fecha, peso_kg, condicion_corporal),
    )
    con.commit()
    con.close()


def obtener_historial_peso(perro_id: int, ruta_db=RUTA_DB) -> list:
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute(
        "SELECT fecha, peso_kg, condicion_corporal FROM historial_peso WHERE perro_id=? ORDER BY fecha",
        (perro_id,),
    )
    filas = cur.fetchall()
    con.close()
    return [{"fecha": f, "peso_kg": p, "condicion_corporal": c} for f, p, c in filas]


def guardar_menu(perro_id: int, nombre_menu: str, resultado_optimizador: dict, ruta_db=RUTA_DB) -> int:
    """resultado_optimizador es lo que devuelve optimizar_menu() (con 'gramos' y 'kcal_total')."""
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO menus (perro_id, nombre, alimentos_gramos, kcal_total, creado_en)
        VALUES (?, ?, ?, ?, ?)
    """, (
        perro_id, nombre_menu, json.dumps(resultado_optimizador["gramos"], ensure_ascii=False),
        resultado_optimizador["kcal_total"], date.today().isoformat(),
    ))
    menu_id = cur.lastrowid
    con.commit()
    con.close()
    return menu_id


def obtener_menus(perro_id: int, ruta_db=RUTA_DB) -> list:
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute(
        "SELECT id, nombre, alimentos_gramos, kcal_total, creado_en FROM menus WHERE perro_id=? ORDER BY creado_en",
        (perro_id,),
    )
    filas = cur.fetchall()
    con.close()
    return [
        {"id": i, "nombre": n, "alimentos": json.loads(ag), "kcal_total": k, "creado_en": c}
        for i, n, ag, k, c in filas
    ]


def guardar_transicion(perro_id: int, dieta_anterior: str, num_menus_elegidos: int,
                        fecha_inicio: str = None, ruta_db=RUTA_DB) -> int:
    fecha_inicio = fecha_inicio or date.today().isoformat()
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO transiciones (perro_id, dieta_anterior, fecha_inicio, num_menus_elegidos) VALUES (?, ?, ?, ?)",
        (perro_id, dieta_anterior, fecha_inicio, num_menus_elegidos),
    )
    trans_id = cur.lastrowid
    con.commit()
    con.close()
    return trans_id


def obtener_transicion_activa(perro_id: int, ruta_db=RUTA_DB) -> dict:
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute(
        "SELECT dieta_anterior, fecha_inicio, num_menus_elegidos FROM transiciones WHERE perro_id=? ORDER BY id DESC LIMIT 1",
        (perro_id,),
    )
    fila = cur.fetchone()
    con.close()
    if not fila:
        return None
    return {"dieta_anterior": fila[0], "fecha_inicio": fila[1], "num_menus_elegidos": fila[2]}


if __name__ == "__main__":
    import os
    if os.path.exists(RUTA_DB):
        os.remove(RUTA_DB)  # empezar limpio para la prueba

    crear_tablas()
    print("=== Tablas creadas ===\n")

    # Guardar el perfil real de Cairo
    cairo_id = guardar_perro({
        "nombre": "Cairo",
        "sexo": "macho",
        "raza": "American Staffordshire Terrier",
        "tamano": "Mediano",
        "peso_adulto_esperado_kg": 32,
        "fecha_nacimiento": "2026-02-15",
        "esterilizado": False,
        "actividad": "normal",
        "especies_excluidas": ["Pollo", "Pavo"],
        "patologias": [],
    })
    print(f"Cairo guardado con id={cairo_id}")

    registrar_peso(cairo_id, 16.0, condicion_corporal="Ideal", fecha="2026-08-01")
    print("Peso registrado: 16kg el 2026-08-01")

    guardar_transicion(cairo_id, dieta_anterior="pienso", num_menus_elegidos=3, fecha_inicio="2026-07-25")
    print("Transición guardada: empezó 25 julio, viene de pienso, 3 menús elegidos")

    resultado_ejemplo = {
        "gramos": {"Cuello de ternera": 558.9, "Hígado de vaca": 131.5, "Espinaca": 50.0,
                   "Riñón de ternera": 18.1, "Pulmón de ternera": 11.9, "Mejillón": 10.6,
                   "Aceite de girasol": 10.1, "Ternera con grasa": 8.6, "Sonrisa de Diez Kelp": 0.3},
        "kcal_total": 1120.1,
    }
    menu_id = guardar_menu(cairo_id, "Menú 1", resultado_ejemplo)
    print(f"Menú 1 guardado con id={menu_id}")

    print("\n=== SIMULANDO CERRAR LA APP Y VOLVER A ABRIRLA (nueva conexión) ===\n")

    print("Historial de peso de Cairo:", obtener_historial_peso(cairo_id))
    print("\nTransición activa de Cairo:", obtener_transicion_activa(cairo_id))
    print("\nMenús guardados de Cairo:")
    for m in obtener_menus(cairo_id):
        print(f"  {m['nombre']} ({m['kcal_total']}kcal, creado {m['creado_en']}): {m['alimentos']}")
