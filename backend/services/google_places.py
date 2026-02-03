# backend/services/google_places.py
"""
Servicio para interactuar con Google Places API.
Encapsula toda la lógica de comunicación con la API externa.
"""
import requests
from typing import List, Dict, Any, Optional
from ..config.settings import GOOGLE_PLACES_API_KEY, DEFAULT_LOCATION


class GooglePlacesService:
    """Servicio para buscar lugares usando Google Places API."""
    
    BASE_URL = "https://maps.googleapis.com/maps/api/place"
    
    def __init__(self, api_key: str = GOOGLE_PLACES_API_KEY):
        """
        Inicializa el servicio.
        
        Args:
            api_key: Clave de API de Google Places
        """
        self.api_key = api_key
    
    def buscar_lugares_cercanos(
        self, 
        tipo: str,
        lat: float = DEFAULT_LOCATION["lat"],
        lng: float = DEFAULT_LOCATION["lng"],
        radio: int = DEFAULT_LOCATION["radio"],
        next_page_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Busca lugares cercanos a una ubicación.
        
        Args:
            tipo: Tipo de lugar según Google Places (ej: "restaurant", "museum")
            lat: Latitud del centro de búsqueda
            lng: Longitud del centro de búsqueda
            radio: Radio de búsqueda en metros
            next_page_token: Token para obtener la siguiente página de resultados
            
        Returns:
            Diccionario con los resultados de la API
            
        Raises:
            requests.RequestException: Si hay error en la petición HTTP
        """
        url = f"{self.BASE_URL}/nearbysearch/json"
        
        params = {
            "location": f"{lat},{lng}",
            "radius": radio,
            "type": tipo,
            "key": self.api_key
        }
        
        # Si hay token para siguiente página, usarlo
        if next_page_token:
            params = {
                "pagetoken": next_page_token,
                "key": self.api_key
            }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()  # Lanza excepción si status no es 200
            return response.json()
        except requests.RequestException as e:
            print(f"Error al buscar lugares del tipo '{tipo}': {e}")
            return {"results": [], "status": "ERROR"}
    
    def obtener_detalles_lugar(self, place_id: str) -> Optional[Dict[str, Any]]:
        """
        Obtiene detalles completos de un lugar específico.
        
        Args:
            place_id: ID del lugar en Google Places
            
        Returns:
            Diccionario con los detalles del lugar o None si hay error
        """
        url = f"{self.BASE_URL}/details/json"
        
        params = {
            "place_id": place_id,
            "fields": "name,rating,formatted_phone_number,website,opening_hours,price_level",
            "key": self.api_key
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("status") == "OK":
                return data.get("result")
            return None
        except requests.RequestException as e:
            print(f"Error al obtener detalles del lugar {place_id}: {e}")
            return None
    
    def buscar_todos_los_resultados(
        self,
        tipo: str,
        max_resultados: int = 60
    ) -> List[Dict[str, Any]]:
        """
        Busca todos los resultados disponibles para un tipo de lugar.
        Google Places API retorna máximo 60 resultados (3 páginas de 20).
        
        Args:
            tipo: Tipo de lugar a buscar
            max_resultados: Número máximo de resultados a obtener
            
        Returns:
            Lista de lugares encontrados
        """
        todos_los_lugares = []
        next_page_token = None
        
        while len(todos_los_lugares) < max_resultados:
            # Buscar lugares
            data = self.buscar_lugares_cercanos(tipo, next_page_token=next_page_token)
            
            if data.get("status") != "OK" and data.get("status") != "ZERO_RESULTS":
                print(f"Error en la búsqueda: {data.get('status')}")
                break
            
            # Agregar resultados
            resultados = data.get("results", [])
            todos_los_lugares.extend(resultados)
            
            # Verificar si hay más páginas
            next_page_token = data.get("next_page_token")
            if not next_page_token:
                break
            
            # Google requiere un delay antes de usar next_page_token
            import time
            time.sleep(2)
        
        return todos_los_lugares[:max_resultados]
