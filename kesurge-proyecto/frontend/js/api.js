// frontend/js/api.js
/**
 * Cliente para comunicarse con la API del backend
 * Maneja todas las peticiones HTTP
 */

class APIClient {
    constructor(baseURL) {
        this.baseURL = baseURL;
    }

    /**
     * Método genérico para hacer peticiones HTTP
     * @param {string} endpoint - Endpoint de la API (ej: '/lugares')
     * @param {object} options - Opciones de fetch (method, headers, body, etc.)
     * @returns {Promise} - Promesa con la respuesta en JSON
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };

        const config = { ...defaultOptions, ...options };

        try {
            const response = await fetch(url, config);
            
            // Verificar si la respuesta es exitosa
            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.error || `HTTP Error ${response.status}`);
            }

            return await response.json();
        } catch (error) {
            console.error(`Error en ${endpoint}:`, error);
            throw error;
        }
    }

    /**
     * GET /api/lugares
     * Obtiene todos los lugares
     * @param {object} filters - Filtros opcionales { categoria, limite, orden }
     * @returns {Promise<{total: number, lugares: Array}>}
     */
    async obtenerLugares(filters = {}) {
        const params = new URLSearchParams();
        
        if (filters.categoria) params.append('categoria', filters.categoria);
        if (filters.limite) params.append('limite', filters.limite);
        if (filters.orden) params.append('orden', filters.orden);

        const queryString = params.toString();
        const endpoint = queryString ? `/lugares?${queryString}` : '/lugares';

        return await this.request(endpoint);
    }

    /**
     * GET /api/lugares/{id}
     * Obtiene un lugar específico
     * @param {number} id - ID del lugar
     * @returns {Promise<object>}
     */
    async obtenerLugar(id) {
        return await this.request(`/lugares/${id}`);
    }

    /**
     * GET /api/categorias
     * Obtiene todas las categorías con su conteo
     * @returns {Promise<{categorias: object}>}
     */
    async obtenerCategorias() {
        return await this.request('/categorias');
    }

    /**
     * GET /api/estadisticas
     * Obtiene estadísticas generales
     * @returns {Promise<object>}
     */
    async obtenerEstadisticas() {
        return await this.request('/estadisticas');
    }

    /**
     * POST /api/scraper/ejecutar
     * Ejecuta el proceso de scraping
     * @param {string} categoria - Categoría a scrapear (opcional)
     * @returns {Promise<object>}
     */
    async ejecutarScraper(categoria = null) {
        const body = categoria ? { categoria } : {};
        
        return await this.request('/scraper/ejecutar', {
            method: 'POST',
            body: JSON.stringify(body)
        });
    }
}

// Crear instancia global del cliente API
const api = new APIClient(CONFIG.API_BASE_URL);

// Exportar para uso en otros archivos
// export default api;
