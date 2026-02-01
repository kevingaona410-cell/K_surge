import requests
import sqlite3
import time
from datetime import datetime

# =========================
# CONFIGURACIÓN
# =========================
#Llave para el API
API_KEY = "AIzaSyDiatTzAw9t3xGZzXsVPT-1FETZiKKNirk"
#Punto desde el cual solicita los datos de busqueda cercana 
LAT = -25.2637
LNG = -57.5759
RADIO = 2000
#Maximo de resultados por categoria
MAX_RESULTADOS = 40  # Máximo por categoría

CATEGORIAS = {
    "comida": ["restaurant", "cafe", "bar", "meal_takeaway"],
    "turismo": ["tourist_attraction", "amusement_park", "zoo"],
    "cultura": ["museum", "art_gallery"],
    "recreacion": ["park", "stadium", "campground"]
}

# =========================
# BASE DE DATOS
# =========================

conn = sqlite3.connect("lugares2.db")
cursor = conn.cursor()

#Creacion de la tabla en la base de datos
cursor.execute("""
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

conn.commit()

# =========================
# PETICIONES SEGURAS
# =========================
#Medida de seguridad en caso de problemas de red
def peticion_segura(url, params):
    #Si funciona recupera el Json de la API
    try:
        r = requests.get(url, params=params, timeout=10)
        r.raise_for_status()
        return r.json()
    #Si no funciona muestra "Error de red"
    except requests.exceptions.RequestException as e:
        print("Error de red:", e)
        return None


# =========================
# BUSCAR LUGARES (PAGINADO)
# =========================

def buscar_lugares(tipo, maximo):

    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"

    resultados = []
    token = None

    while len(resultados) < maximo:

        params = {
            "location": f"{LAT},{LNG}",
            "radius": RADIO,
            "type": tipo,
            "key": API_KEY
        }

        if token:
            params["pagetoken"] = token
            time.sleep(2)  # Obligatorio por Google

        data = peticion_segura(url, params)

        if not data:
            break

        # Validación de API
        if data["status"] != "OK":
            print("Error API:", data["status"])
            break

        resultados.extend(data["results"])

        token = data.get("next_page_token")

        if not token:
            break

    return resultados[:maximo]


# =========================
# PLACE DETAILS
# =========================

def obtener_detalles(place_id):

    url = "https://maps.googleapis.com/maps/api/place/details/json"

    params = {
        "place_id": place_id,
        "fields": "formatted_phone_number,website",
        "key": API_KEY
    }

    data = peticion_segura(url, params)

    if not data or data["status"] != "OK":
        return {}

    return data["result"]


# =========================
# GUARDAR / ACTUALIZAR
# =========================

def guardar_lugar(lugar, categoria):

    detalles = obtener_detalles(lugar["place_id"])

    telefono = detalles.get("formatted_phone_number", "")
    web = detalles.get("website", "")

    tipos = ",".join(lugar.get("types", []))

    fecha = datetime.now().isoformat()

    cursor.execute("""
    INSERT OR REPLACE INTO lugares
    (
        place_id, nombre, direccion,
        lat, lng, categoria,
        tipos, rating,
        telefono, web,
        fecha_actualizacion
    )
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lugar["place_id"],
        lugar["name"],
        lugar.get("vicinity", ""),
        lugar["geometry"]["location"]["lat"],
        lugar["geometry"]["location"]["lng"],
        categoria,
        tipos,
        lugar.get("rating", 0),
        telefono,
        web,
        fecha
    ))

    conn.commit()

    print(f"Actualizado: {lugar['name']} ({categoria})")


# =========================
# PROCESO PRINCIPAL
# =========================

def main():

    for categoria, tipos in CATEGORIAS.items():

        print(f"\nBuscando: {categoria.upper()}")

        contador = 0

        for tipo in tipos:

            if contador >= MAX_RESULTADOS:
                break

            lugares = buscar_lugares(
                tipo,
                MAX_RESULTADOS - contador
            )

            for lugar in lugares:

                guardar_lugar(lugar, categoria)
                contador += 1

                if contador >= MAX_RESULTADOS:
                    break

            # Pausa para evitar bloqueo
            time.sleep(0.5)


if __name__ == "__main__":
    main()
