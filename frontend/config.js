// frontend/js/config.js
/**
 * Configuración del frontend
 */

const CONFIG = {
    // URL de la API backend
    // En desarrollo: http://localhost:5000
    // En producción: https://tu-dominio.com
    API_BASE_URL: 'http://localhost:5000/api',
    
    // Configuración del mapa
    MAP: {
        center: {
            lat: -25.2637,
            lng: -57.5759
        },
        zoom: 13,
        // Tu API Key de Google Maps
        API_KEY: 'TU_GOOGLE_MAPS_API_KEY'
    },
    
    // Categorías disponibles
    CATEGORIAS: {
        'comida': {
            nombre: 'Gastronomía',
            icono: '🍽️',
            color: '#F7A00A'
        },
        'turismo': {
            nombre: 'Turismo',
            icono: '🏛️',
            color: '#2D5A27'
        },
        'cultura': {
            nombre: 'Arte y Cultura',
            icono: '🎨',
            color: '#A52A2A'
        },
        'recreacion': {
            nombre: 'Recreación',
            icono: '⚽',
            color: '#1A1A1A'
        }
    }
};

// Exportar configuración (si usas módulos ES6)
// export default CONFIG;
