import sqlite3
import json


class LugarDB:

    def __init__(self, archivo="lugares.db"):

        self.conn = sqlite3.connect(archivo)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()

        self.crear_tabla()


    # ============================
    # CREAR TABLA
    # ============================
    def crear_tabla(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS lugares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_id TEXT UNIQUE,
            nombre TEXT,
            direccion TEXT,
            lat REAL,
            lng REAL,
            categoria TEXT,
            tipos TEXT,
            rating REAL,
            telefono TEXT,
            web TEXT,
            fecha_actualizacion TEXT,
            horarios TEXT
        )
        """)

        self.conn.commit()


    # ============================
    # GUARDAR REGISTRO
    # ============================
    def guardar(self, lugar):

        self.cursor.execute("""
        INSERT OR REPLACE INTO lugares
        VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?,?)
        """, (
            lugar.place_id,
            lugar.nombre,
            lugar.direccion,
            lugar.lat,
            lugar.lng,
            lugar.categoria,
            lugar.tipos,
            lugar.rating,
            lugar.telefono,
            lugar.web,
            lugar.fecha,
            lugar.horarios
        ))

        self.conn.commit()


    # ============================
    # OBTENER TODO EN JSON
    # ============================
    def obtener_todos_json(self):

        self.cursor.execute("""
        SELECT * FROM lugares
        """)

        filas = self.cursor.fetchall()

        datos = []

        for fila in filas:

            datos.append(dict(fila))

        return json.dumps(
            datos,
            indent=4,
            ensure_ascii=False
        )


    # ============================
    # EXPORTAR A ARCHIVO JSON
    # ============================
    def exportar_json_archivo(self, nombre="lugares.json"):

        json_data = self.obtener_todos_json()

        with open(nombre, "w", encoding="utf-8") as f:
            f.write(json_data)

        print("Archivo JSON generado:", nombre)
