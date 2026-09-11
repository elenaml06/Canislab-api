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
        -- ⚠️ AÑADIDA EL 11 DE SEPTIEMBRE. De quién es este perro: el uid de
        -- Supabase de su dueño. Sin esta columna no había forma NI EN
        -- PRINCIPIO de saber si quien pide los menús de un perro tiene algo
        -- que ver con él -- y `/perro/{id}/menus` los servía a quien los
        -- pidiera, con ids que van 1, 2, 3. Es el mismo agujero que tenía
        -- la columna `contexto`: no faltaba código, faltaba el dato.
        usuario_id TEXT,
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
        -- ⚠️ AÑADIDA EL 7 DE SEPTIEMBRE. Sin esto, un menú guardado NO SE
        -- PODÍA VERIFICAR NI EN PRINCIPIO: la tabla solo tenía nombre,
        -- gramos y kcal, y para pasar el semáforo hacen falta la etapa, el
        -- DER y el peso contra los que se verificó. `/perro/{id}/menus` lo
        -- devolvía con `verificado: false` y un aviso, que era honesto pero
        -- dejaba fuera de la regla 1 del CLAUDE.md al único camino que
        -- entrega menús. Ahora se guarda el contexto CON el menú y se
        -- verifica al leerlo, contra los mismos requisitos de aquel día.
        contexto TEXT,              -- JSON: etapa, der, pesos, patologías
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
    # ⚠️ MIGRACIÓN, no un CREATE. `CREATE TABLE IF NOT EXISTS` no toca una
    # tabla que ya existe, así que en cualquier base creada antes del 7 de
    # septiembre la columna `contexto` no aparecería nunca y los menús
    # seguirían sin poder verificarse, en silencio. Se añade a mano si falta.
    cur.execute("PRAGMA table_info(menus)")
    if "contexto" not in {fila[1] for fila in cur.fetchall()}:
        cur.execute("ALTER TABLE menus ADD COLUMN contexto TEXT")
    # Misma migración a mano, y por lo mismo, para el dueño del perro.
    cur.execute("PRAGMA table_info(perros)")
    if "usuario_id" not in {fila[1] for fila in cur.fetchall()}:
        cur.execute("ALTER TABLE perros ADD COLUMN usuario_id TEXT")
    con.commit()
    con.close()


def guardar_perro(datos: dict, ruta_db=RUTA_DB) -> int:
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO perros (usuario_id, nombre, sexo, raza, tamano,
                             peso_adulto_esperado_kg,
                             fecha_nacimiento, esterilizado, actividad,
                             especies_excluidas, patologias)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datos.get("usuario_id"),
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


def dueno_de(perro_id: int, ruta_db=RUTA_DB):
    """El uid de Supabase del dueño de este perro. None si no consta.

    ⚠️ None NO ES "PUES QUE PASE". Es "no se sabe de quién es", y de lo que
    no se sabe de quién es no se entregan los menús -- ver
    `endpoint_obtener_menus` en main.py. Las filas guardadas antes del 11
    de septiembre caen todas aquí, y es lo correcto: preferimos que su
    dueño tenga que volver a guardarlas a servírselas a cualquiera."""
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute("SELECT usuario_id FROM perros WHERE id=?", (perro_id,))
    fila = cur.fetchone()
    con.close()
    return (fila[0] or None) if fila else None


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


# Lo que hace falta para volver a verificar un menú meses después. Se
# guarda TAL CUAL se pidió: si el perro cambia de etapa o de peso, el menú
# guardado sigue teniendo que verificarse contra lo de ENTONCES para saber
# si cumplía; contra lo de hoy es otra pregunta, y para eso está
# /menu/revalidar.
CLAVES_CONTEXTO = ("etapa_requisitos", "der_objetivo", "peso_perro_kg",
                   "peso_objetivo_kg", "peso_adulto_esperado_kg",
                   "tamano", "patologias")


def guardar_menu(perro_id: int, nombre_menu: str, resultado_optimizador: dict,
                 contexto: dict = None, ruta_db=RUTA_DB) -> int:
    """resultado_optimizador es lo que devuelve optimizar_menu() (con 'gramos' y 'kcal_total').

    `contexto` son la etapa, el DER y los pesos contra los que se verificó
    este menú. Sin ellos el menú no se puede volver a verificar nunca --
    ver el comentario de la columna en `crear_tablas`."""
    ctx = {k: (contexto or {}).get(k) for k in CLAVES_CONTEXTO}
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute("""
        INSERT INTO menus (perro_id, nombre, alimentos_gramos, kcal_total, creado_en, contexto)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        perro_id, nombre_menu, json.dumps(resultado_optimizador["gramos"], ensure_ascii=False),
        resultado_optimizador["kcal_total"], date.today().isoformat(),
        json.dumps(ctx, ensure_ascii=False) if contexto else None,
    ))
    menu_id = cur.lastrowid
    con.commit()
    con.close()
    return menu_id


def obtener_menus(perro_id: int, ruta_db=RUTA_DB) -> list:
    con = sqlite3.connect(ruta_db)
    cur = con.cursor()
    cur.execute(
        "SELECT id, nombre, alimentos_gramos, kcal_total, creado_en, contexto "
        "FROM menus WHERE perro_id=? ORDER BY creado_en",
        (perro_id,),
    )
    filas = cur.fetchall()
    con.close()
    return [
        {"id": i, "nombre": n, "alimentos": json.loads(ag), "kcal_total": k, "creado_en": c,
         # None en las filas guardadas antes del 7 de septiembre: esas no se
         # pueden verificar y hay que decirlo, no fingir que sí.
         "contexto": json.loads(ctx) if ctx else None}
        for i, n, ag, k, c, ctx in filas
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
