# backend/api/app.py
"""
Aplicación Flask para la API REST.
Configura el servidor web y los middlewares.
"""
from flask import Flask
from flask_cors import CORS
from .routes import api_blueprint
from ..config.settings import DEBUG_MODE, ALLOWED_ORIGINS


def crear_app():
    """
    Factory function para crear la aplicación Flask.
    
    Returns:
        Instancia configurada de Flask
    """
    app = Flask(__name__)
    
    # Configuración de CORS para permitir peticiones desde el frontend
    CORS(app, resources={
        r"/api/*": {
            "origins": ALLOWED_ORIGINS,
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type"]
        }
    })
    
    # Configuración de la app
    app.config['JSON_SORT_KEYS'] = False  # No ordenar JSON alfabéticamente
    app.config['JSON_AS_ASCII'] = False   # Permitir caracteres UTF-8
    
    # Registrar blueprints (rutas)
    app.register_blueprint(api_blueprint, url_prefix='/api')
    
    # Ruta de salud (health check)
    @app.route('/health')
    def health():
        return {"status": "ok", "message": "API funcionando correctamente"}, 200
    
    # Manejo de errores 404
    @app.errorhandler(404)
    def not_found(error):
        return {
            "error": "Endpoint no encontrado",
            "message": str(error)
        }, 404
    
    # Manejo de errores 500
    @app.errorhandler(500)
    def internal_error(error):
        return {
            "error": "Error interno del servidor",
            "message": str(error)
        }, 500
    
    return app
