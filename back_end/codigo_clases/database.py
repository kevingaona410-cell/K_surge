#Importamos nuestro gestor de SQL 
import sqlite3


class LugarDB:

    #La clase se conecta a la base de datos
    def __init__(self, archivo="lugares.db"):

        self.conn = sqlite3.connect(archivo)
        self.cursor = self.conn.cursor()

        self.crear_tabla()

    #En caso de existir una tabla se crea una y se completa
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
            fecha_actualizacion TEXT
        )
        """)

        self.conn.commit()

    #Se guardan los datos obtenidos por argumento obtenido(nombre, direccion, rating, etc)
    def guardar(self, lugar):

        self.cursor.execute("""
        INSERT OR REPLACE INTO lugares
        VALUES (NULL,?,?,?,?,?,?,?,?,?,?,?)
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
            lugar.fecha
        ))

        self.conn.commit()
