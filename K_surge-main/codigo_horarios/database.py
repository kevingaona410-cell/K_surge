import sqlite3
import json
import os
from datetime import datetime

class VillaMorraDB:
    def __init__(self, db_name="qsurge.db"):
        # Aseguramos que la DB se cree en la carpeta del script
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        self.db_name = os.path.join(ruta_base, db_name)
        self.crear_tablas()

    def conectar(self):
        return sqlite3.connect(self.db_name)

    def crear_tablas(self):
        conn = self.conectar()
        cursor = conn.cursor()
        
        # Tabla de eventos
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
        
        # Tabla de auditoría
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

# --- FUNCIONES DE INTEGRACIÓN CON EL FRONTEND ---

def obtener_eventos_json():
    try:
        # Buscamos la DB en la misma carpeta que este script
        ruta_db = os.path.join(os.path.dirname(os.path.abspath(__file__)), "qsurge.db")
        conn = sqlite3.connect(ruta_db)
        conn.row_factory = sqlite3.Row 
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM eventos ORDER BY id DESC")
        rows = cursor.fetchall()
        
        eventos_lista = []
        for row in rows:
            evento = {
                "id": row["id"],
                "titulo": row["titulo"],
                "categoria": "Cultura", 
                "lugar": row["lugar"],
                "fecha": row["fecha"],
                "hora": "20:00", 
                "imagen": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?q=80",
                "es_destacado": True,
                "descripcion": row["descripcion"]
            }
            eventos_lista.append(evento)
            
        conn.close()
        return json.dumps(eventos_lista, indent=4, ensure_ascii=False)
        
    except Exception as e:
        print(f"❌ Error al obtener JSON: {e}")
        return "[]"

def guardar_json_final(json_data):
    ruta_script = os.path.dirname(os.path.abspath(__file__))
    # Esta ruta sube un nivel para llegar a la carpeta donde está el index.html
    ruta_destino = os.path.abspath(os.path.join(ruta_script, "..", "eventos.json"))
    
    try:
        with open(ruta_destino, "w", encoding="utf-8") as f:
            f.write(json_data)
        print(f"📍 JSON generado con éxito en: {ruta_destino}")
    except Exception as e:
        print(f"❌ Error de escritura en JSON: {e}")