#AIzaSyDiatTzAw9t3xGZzXsVPT-1FETZiKKNirk Llave del API google Places
import requests
import sqlite3

# =========================
# CONFIGURACIÓN
# =========================

API_KEY = "AIzaSyDiatTzAw9t3xGZzXsVPT-1FETZiKKNirk"

LAT = -25.2637
LNG = -57.5759
RADIO = 2000  # Coordenadas y radio de busqueda en metros

# Tipos permitidos por la API de Google Places
CATEGORIAS = {
    "comida": ["restaurant", "cafe", "bar", "meal_takeaway"],#tipos de lugares relacionados con comida
    "turismo": ["tourist_attraction", "amusement_park", "zoo"],#tipos de lugares relacionados con turismo
    "cultura": ["museum", "art_gallery"],#tipos de lugares relacionados con cultura
    "recreacion": ["park", "stadium", "campground"]#tipos de lugares relacionados con recreacion
}

# =========================
# BASE DE DATOS
# =========================
# Conexión a la base de datos SQLite
conn = sqlite3.connect("lugares.db")
cursor = conn.cursor()

# Crear tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS lugares (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id TEXT UNIQUE,
    nombre TEXT,
    direccion TEXT,
    lat REAL,
    lng REAL,
    categoria TEXT,
    rating REAL
)
""")

conn.commit()

# =========================
# FUNCIONES
# =========================
#Busqueda en la API de google places
def buscar_lugares(tipo):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    params = {
        "location": f"{LAT},{LNG}",
        "radius": RADIO,
        "type": tipo,
        "key": API_KEY
    }

    r = requests.get(url, params=params)
    return r.json()

#Guardar los lugares en la base de datos
def guardar_lugar(lugar, categoria):
    try:
        # Insertar lugar en la base de datos
        cursor.execute("""
        INSERT INTO lugares
        (place_id, nombre, direccion, lat, lng, categoria, rating)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            lugar["place_id"],
            lugar["name"],
            lugar.get("vicinity", ""),
            lugar["geometry"]["location"]["lat"],
            lugar["geometry"]["location"]["lng"],
            categoria,
            lugar.get("rating", 0)
        ))
            # Confirmar cambios
        conn.commit()

        print(f"Guardado: {lugar['name']} ({categoria})")

    except sqlite3.IntegrityError:
        # Ya existe
        pass


# =========================
# PROCESO PRINCIPAL
# =========================
#Buscar y guardar lugares
def main():
    # Recorrer categorías y tipos
    for categoria, tipos in CATEGORIAS.items():

        print(f"\nBuscando: {categoria.upper()}")
        # Recorrer tipos dentro de la categoría
        for tipo in tipos:

            data = buscar_lugares(tipo)
            # Verificar si hay resultados
            if "results" not in data:
                continue
            # Guardar cada lugar en la base de datos
            for lugar in data["results"]:
                guardar_lugar(lugar, categoria)

if __name__ == "__main__":
    main()