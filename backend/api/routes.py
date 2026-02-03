# backend/api/routes.py
"""
Definición de rutas y endpoints de la API.
Maneja todas las peticiones HTTP.
"""
from flask import Blueprint, request, jsonify
from ..repositories.lugar_repository import LugarRepository
from ..services.scraper import ScraperService
from ..config.settings import CATEGORIAS

# Crear blueprint para agrupar las rutas
api_blueprint = Blueprint('api', __name__)

# Instanciar servicios
repository = LugarRepository()
scraper = ScraperService()


@api_blueprint.route('/lugares', methods=['GET'])
def obtener_lugares():
    """
    GET /api/lugares
    
    Obtiene todos los lugares, con filtros opcionales.
    
    Query parameters:
        - categoria: Filtrar por categoría (comida, turismo, cultura, recreacion)
        - limite: Número máximo de resultados (default: 100)
        - orden: Campo por el que ordenar (rating, nombre)
    
    Ejemplo:
        GET /api/lugares?categoria=comida&limite=20&orden=rating
    
    Respuesta:
        {
            "total": 20,
            "lugares": [...]
        }
    """
    try:
        # Obtener parámetros de query
        categoria = request.args.get('categoria')
        limite = request.args.get('limite', 100, type=int)
        orden_param = request.args.get('orden', 'rating')
        
        # Validar categoría si se proporciona
        if categoria and categoria not in CATEGORIAS:
            return jsonify({
                "error": "Categoría inválida",
                "categorias_validas": list(CATEGORIAS.keys())
            }), 400
        
        # Determinar orden SQL
        orden_sql = "rating DESC" if orden_param == "rating" else "nombre ASC"
        
        # Obtener lugares desde el repositorio
        lugares = repository.obtener_todos(
            categoria=categoria,
            limite=limite,
            orden=orden_sql
        )
        
        # Convertir a diccionarios
        lugares_dict = [lugar.to_dict() for lugar in lugares]
        
        return jsonify({
            "total": len(lugares_dict),
            "categoria": categoria,
            "lugares": lugares_dict
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route('/lugares/<int:lugar_id>', methods=['GET'])
def obtener_lugar(lugar_id):
    """
    GET /api/lugares/{id}
    
    Obtiene un lugar específico por su ID.
    
    Parámetros:
        - lugar_id: ID del lugar
    
    Respuesta:
        {
            "id": 1,
            "nombre": "Tierra Colorada",
            "categoria": "comida",
            ...
        }
    """
    try:
        lugar = repository.obtener_por_id(lugar_id)
        
        if not lugar:
            return jsonify({"error": "Lugar no encontrado"}), 404
        
        return jsonify(lugar.to_dict()), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route('/categorias', methods=['GET'])
def obtener_categorias():
    """
    GET /api/categorias
    
    Obtiene todas las categorías disponibles con su conteo.
    
    Respuesta:
        {
            "categorias": {
                "comida": 45,
                "turismo": 30,
                "cultura": 15,
                "recreacion": 20
            }
        }
    """
    try:
        conteos = repository.contar_por_categoria()
        
        return jsonify({
            "categorias": conteos
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route('/scraper/ejecutar', methods=['POST'])
def ejecutar_scraper():
    """
    POST /api/scraper/ejecutar
    
    Ejecuta el proceso de scraping manualmente.
    
    Body (opcional):
        {
            "categoria": "comida"  # Para scrapear solo una categoría
        }
    
    Respuesta:
        {
            "status": "completado",
            "estadisticas": {
                "total_encontrados": 150,
                "total_nuevos": 45,
                ...
            }
        }
    """
    try:
        data = request.get_json() or {}
        categoria = data.get('categoria')
        
        if categoria:
            # Validar categoría
            if categoria not in CATEGORIAS:
                return jsonify({
                    "error": "Categoría inválida",
                    "categorias_validas": list(CATEGORIAS.keys())
                }), 400
            
            # Scraping de una categoría específica
            estadisticas = scraper.ejecutar_scraping_categoria(categoria)
        else:
            # Scraping completo
            estadisticas = scraper.ejecutar_scraping_completo()
        
        return jsonify({
            "status": "completado",
            "estadisticas": estadisticas
        }), 200
        
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@api_blueprint.route('/estadisticas', methods=['GET'])
def obtener_estadisticas():
    """
    GET /api/estadisticas
    
    Obtiene estadísticas generales de la base de datos.
    
    Respuesta:
        {
            "total_lugares": 110,
            "por_categoria": {...},
            "promedio_rating": 4.2
        }
    """
    try:
        # Obtener conteos por categoría
        por_categoria = repository.contar_por_categoria()
        total = sum(por_categoria.values())
        
        # Calcular promedio de rating
        lugares = repository.obtener_todos(limite=10000)
        if lugares:
            promedio_rating = sum(l.rating for l in lugares) / len(lugares)
        else:
            promedio_rating = 0
        
        return jsonify({
            "total_lugares": total,
            "por_categoria": por_categoria,
            "promedio_rating": round(promedio_rating, 2)
        }), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500
