# backend/main.py
"""
Punto de entrada principal del backend.
Inicia el servidor de la API.
"""
from api.app import crear_app
from config.settings import API_HOST, API_PORT, DEBUG_MODE

if __name__ == '__main__':
    # Crear aplicación Flask
    app = crear_app()
    
    # Mostrar información de inicio
    print("\n" + "="*50)
    print(" KESURGE API SERVER")
    print("="*50)
    print(f" Host: {API_HOST}")
    print(f" Puerto: {API_PORT}")
    print(f" Debug: {DEBUG_MODE}")
    print(f" URL: http://{API_HOST}:{API_PORT}")
    print("="*50 + "\n")
    
    # Iniciar servidor
    app.run(
        host=API_HOST,
        port=API_PORT,
        debug=DEBUG_MODE
    )
