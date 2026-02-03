import sqlite3
from datetime import datetime

class VillaMorraDB:
    def __init__(self, db_name="qsurge.db"):
        self.db_name = db_name
        self.crear_tablas()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tablas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Tabla de eventos con columna de tiempo
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS eventos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT UNIQUE,
                lugar TEXT,
                fecha TEXT,
                descripcion TEXT,
                url TEXT UNIQUE,
                actualizado_en TEXT
            )
        ''')
        
        # Tabla de auditoría para el jurado
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs_actualizacion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha_ejecucion TEXT,
                total_eventos INTEGER
            )
        ''')
        conn.commit()
        conn.close()

    def registrar_evento(self, titulo, lugar, fecha, descripcion, url):
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT OR REPLACE INTO eventos (titulo, lugar, fecha, descripcion, url, actualizado_en)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (titulo.strip(), lugar, fecha, descripcion, url, ahora))
            conn.commit()
            conn.close()
        except Exception as e:
            print(f"❌ Error al registrar evento: {e}")

    def registrar_log_actualizacion(self, total):
        ahora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        try:
            conn = self.conectar()
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO logs_actualizacion (fecha_ejecucion, total_eventos)
                VALUES (?, ?)
            ''', (ahora, total))
            conn.commit()
            conn.close()
            print(f"📊 Log de actualización creado: {ahora}")
        except Exception as e:
            print(f"❌ Error en log: {e}")

    def obtener_conteo(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM eventos")
        total = cursor.fetchone()[0]
        conn.close()
        return total

    def borrar_todo(self):
        conn = self.conectar()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM eventos")
        conn.commit()
        conn.close()