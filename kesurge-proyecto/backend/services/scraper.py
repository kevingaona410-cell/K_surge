# backend/services/scraper.py
"""
Servicio orquestador de scraping.
Coordina la búsqueda de lugares y su almacenamiento en la base de datos.
"""
from typing import Dict, List
from ..config.settings import CATEGORIAS, MAX_RESULTS_PER_CATEGORY
from ..models.lugar import Lugar
from ..repositories.lugar_repository import LugarRepository
from ..services.google_places import GooglePlacesService


class ScraperService:
    """
    Servicio para orquestar el proceso de scraping.
    Coordina Google Places API y el almacenamiento en BD.
    """
    
    def __init__(self):
        """Inicializa el servicio con sus dependencias."""
        self.google_places = GooglePlacesService()
        self.repository = LugarRepository()
    
    def ejecutar_scraping_completo(self) -> Dict[str, int]:
        """
        Ejecuta el scraping completo de todas las categorías.
        
        Returns:
            Diccionario con estadísticas del scraping:
            {
                "total_encontrados": 150,
                "total_nuevos": 45,
                "total_actualizados": 105,
                "por_categoria": {
                    "comida": 50,
                    "turismo": 30,
                    ...
                }
            }
        """
        estadisticas = {
            "total_encontrados": 0,
            "total_nuevos": 0,
            "total_actualizados": 0,
            "por_categoria": {}
        }
        
        print(" Iniciando scraping de lugares...")
        
        # Iterar por cada categoría
        for categoria, tipos in CATEGORIAS.items():
            print(f"\n Procesando categoría: {categoria.upper()}")
            
            lugares_categoria = 0
            
            # Iterar por cada tipo dentro de la categoría
            for tipo in tipos:
                print(f"  → Buscando tipo: {tipo}")
                
                # Buscar lugares de este tipo
                resultados = self.google_places.buscar_todos_los_resultados(
                    tipo, 
                    max_resultados=MAX_RESULTS_PER_CATEGORY
                )
                
                print(f"    Encontrados: {len(resultados)} lugares")
                
                # Procesar cada lugar encontrado
                for data in resultados:
                    try:
                        # Crear modelo de Lugar desde los datos de Google
                        lugar = Lugar.from_google_places(data, categoria)
                        
                        # Verificar si ya existe
                        existe = self.repository.existe(lugar.place_id)
                        
                        if existe:
                            # Actualizar lugar existente
                            if self.repository.actualizar(lugar):
                                estadisticas["total_actualizados"] += 1
                                print(f"    ✓ Actualizado: {lugar.nombre}")
                        else:
                            # Crear nuevo lugar
                            if self.repository.crear(lugar):
                                estadisticas["total_nuevos"] += 1
                                lugares_categoria += 1
                                print(f"    + Nuevo: {lugar.nombre}")
                        
                        estadisticas["total_encontrados"] += 1
                        
                    except Exception as e:
                        print(f"    ✗ Error procesando lugar: {e}")
                        continue
            
            estadisticas["por_categoria"][categoria] = lugares_categoria
        
        # Resumen final
        print("\n" + "="*50)
        print(" RESUMEN DEL SCRAPING")
        print("="*50)
        print(f"Total encontrados: {estadisticas['total_encontrados']}")
        print(f"Nuevos agregados: {estadisticas['total_nuevos']}")
        print(f"Actualizados: {estadisticas['total_actualizados']}")
        print("\nPor categoría:")
        for cat, total in estadisticas['por_categoria'].items():
            print(f"  • {cat.capitalize()}: {total} lugares")
        print("="*50)
        
        return estadisticas
    
    def ejecutar_scraping_categoria(self, categoria: str) -> Dict[str, int]:
        """
        Ejecuta el scraping de una categoría específica.
        
        Args:
            categoria: Nombre de la categoría a scrapear
            
        Returns:
            Diccionario con estadísticas del scraping
        """
        if categoria not in CATEGORIAS:
            raise ValueError(f"Categoría '{categoria}' no válida. "
                        f"Categorías disponibles: {list(CATEGORIAS.keys())}")
        
        estadisticas = {
            "categoria": categoria,
            "total_encontrados": 0,
            "total_nuevos": 0,
            "total_actualizados": 0
        }
        
        print(f" Iniciando scraping de categoría: {categoria.upper()}")
        
        tipos = CATEGORIAS[categoria]
        
        for tipo in tipos:
            print(f"  → Buscando tipo: {tipo}")
            
            resultados = self.google_places.buscar_todos_los_resultados(
                tipo,
                max_resultados=MAX_RESULTS_PER_CATEGORY
            )
            
            print(f"    Encontrados: {len(resultados)} lugares")
            
            for data in resultados:
                try:
                    lugar = Lugar.from_google_places(data, categoria)
                    
                    existe = self.repository.existe(lugar.place_id)
                    
                    if existe:
                        if self.repository.actualizar(lugar):
                            estadisticas["total_actualizados"] += 1
                    else:
                        if self.repository.crear(lugar):
                            estadisticas["total_nuevos"] += 1
                    
                    estadisticas["total_encontrados"] += 1
                    
                except Exception as e:
                    print(f"    ✗ Error: {e}")
                    continue
        
        print(f"\n Scraping de '{categoria}' completado")
        print(f"   Encontrados: {estadisticas['total_encontrados']}")
        print(f"   Nuevos: {estadisticas['total_nuevos']}")
        print(f"   Actualizados: {estadisticas['total_actualizados']}")
        
        return estadisticas
