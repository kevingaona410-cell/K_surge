# backend/config/settings.py
"""
Configuración centralizada del proyecto.
Todas las constantes y configuraciones en un solo lugar.
"""
import os
from pathlib import Path

# Directorio base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# API KEYS Y CREDENCIALES
# ==========================
# En producción, estas deberían venir de variables de entorno
GOOGLE_PLACES_API_KEY = os.getenv(
    "GOOGLE_PLACES_API_KEY", 
    "AIzaSyDiatTzAw9t3xGZzXsVPT-1FETZiKKNirk"  # Por defecto para desarrollo
)

# ==========================
# CONFIGURACIÓN DE BÚSQUEDA
# ==========================
# Coordenadas de Asunción, Paraguay
DEFAULT_LOCATION = {
    "lat": -25.2637,
    "lng": -57.5759,
    "radio": 2000  # Radio en metros
}

# Categorías y tipos de lugares según Google Places API
CATEGORIAS = {
    "comida": ["restaurant", "cafe", "bar", "meal_takeaway"],
    "turismo": ["tourist_attraction", "amusement_park", "zoo"],
    "cultura": ["museum", "art_gallery"],
    "recreacion": ["park", "stadium", "campground"]
}

# ==========================
# BASE DE DATOS
# ==========================
DATABASE_PATH = os.getenv("DATABASE_PATH", str(BASE_DIR / "lugares.db"))

# ==========================
# API BACKEND
# ==========================
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 5000))
DEBUG_MODE = os.getenv("DEBUG", "True").lower() == "true"

# CORS - Orígenes permitidos
ALLOWED_ORIGINS = os.getenv("ALLOWED_ORIGINS", "*").split(",")

# ==========================
# SCRAPING
# ==========================
# Intervalo de actualización (en horas)
SCRAPING_INTERVAL_HOURS = int(os.getenv("SCRAPING_INTERVAL", 24))

# Límite de resultados por categoría
MAX_RESULTS_PER_CATEGORY = int(os.getenv("MAX_RESULTS", 60))
