# scripts/run_scraper.py
"""
Script para ejecutar el scraping de lugares.
Puede ser ejecutado manualmente o mediante un cron job.
"""
import sys
import os

# Agregar el directorio padre al path para poder importar módulos del backend
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.services.scraper import ScraperService


def main():
    """Función principal del script."""
    print("\n" + "="*60)
    print(" KESURGE - SCRAPER DE LUGARES")
    print("="*60 + "\n")
    
    # Crear instancia del scraper
    scraper = ScraperService()
    
    # Ejecutar scraping completo
    try:
        estadisticas = scraper.ejecutar_scraping_completo()
        
        print("\n Scraping completado exitosamente!")
        print(f" Total de lugares procesados: {estadisticas['total_encontrados']}")
        
        return 0  # Código de salida exitoso
        
    except Exception as e:
        print(f"\n Error durante el scraping: {e}")
        return 1  # Código de salida con error


if __name__ == '__main__':
    exit_code = main()
    sys.exit(exit_code)
