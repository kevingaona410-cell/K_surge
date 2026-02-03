// frontend/js/app.js
/**
 * Lógica principal de la aplicación
 */

class KesurgeApp {
    constructor() {
        this.categoriaActual = null;
        this.lugares = [];
    }

    /**
     * Inicializa la aplicación
     */
    async init() {
        console.log('🚀 Inicializando Kesurge App...');
        
        // Cargar lugares iniciales
        await this.cargarLugares();
        
        // Configurar event listeners
        this.configurarEventos();
        
        // Cargar estadísticas
        await this.cargarEstadisticas();
        
        console.log('✅ App inicializada');
    }

    /**
     * Carga lugares desde la API
     * @param {string} categoria - Categoría a filtrar (opcional)
     */
    async cargarLugares(categoria = null) {
        try {
            // Mostrar loader
            this.mostrarLoader('lugares-container');
            
            // Petición a la API
            const response = await api.obtenerLugares({
                categoria: categoria,
                limite: 50,
                orden: 'rating'
            });

            this.lugares = response.lugares;
            this.categoriaActual = categoria;

            // Renderizar tarjetas
            LugarCard.renderMultiple(this.lugares, 'lugares-container');
            
            console.log(`✓ Cargados ${this.lugares.length} lugares`);

        } catch (error) {
            console.error('Error al cargar lugares:', error);
            this.mostrarError('lugares-container', 'Error al cargar lugares');
        }
    }

    /**
     * Carga y muestra estadísticas
     */
    async cargarEstadisticas() {
        try {
            const stats = await api.obtenerEstadisticas();
            
            console.log('Estadísticas:', stats);
            
            // Actualizar UI con estadísticas
            // TODO: Implementar visualización de estadísticas
            
        } catch (error) {
            console.error('Error al cargar estadísticas:', error);
        }
    }

    /**
     * Configura los event listeners
     */
    configurarEventos() {
        // Filtros por categoría
        const botonesCategoria = document.querySelectorAll('[data-categoria]');
        botonesCategoria.forEach(boton => {
            boton.addEventListener('click', (e) => {
                const categoria = e.currentTarget.dataset.categoria;
                this.filtrarPorCategoria(categoria);
            });
        });

        // Búsqueda
        const inputBusqueda = document.getElementById('busqueda');
        if (inputBusqueda) {
            inputBusqueda.addEventListener('input', (e) => {
                this.buscarLugares(e.target.value);
            });
        }
    }

    /**
     * Filtra lugares por categoría
     * @param {string} categoria - Categoría a filtrar
     */
    async filtrarPorCategoria(categoria) {
        console.log(`Filtrando por categoría: ${categoria}`);
        await this.cargarLugares(categoria);
    }

    /**
     * Busca lugares por nombre
     * @param {string} termino - Término de búsqueda
     */
    buscarLugares(termino) {
        if (!termino || termino.length < 2) {
            // Si no hay término, mostrar todos
            LugarCard.renderMultiple(this.lugares, 'lugares-container');
            return;
        }

        const terminoLower = termino.toLowerCase();
        const resultados = this.lugares.filter(lugar => 
            lugar.nombre.toLowerCase().includes(terminoLower) ||
            (lugar.direccion && lugar.direccion.toLowerCase().includes(terminoLower))
        );

        LugarCard.renderMultiple(resultados, 'lugares-container');
        
        console.log(`Encontrados ${resultados.length} resultados para "${termino}"`);
    }

    /**
     * Muestra un loader en un contenedor
     * @param {string} containerId - ID del contenedor
     */
    mostrarLoader(containerId) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="col-span-full flex justify-center items-center py-20">
                    <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-tierra"></div>
                </div>
            `;
        }
    }

    /**
     * Muestra un mensaje de error
     * @param {string} containerId - ID del contenedor
     * @param {string} mensaje - Mensaje de error
     */
    mostrarError(containerId, mensaje) {
        const container = document.getElementById(containerId);
        if (container) {
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <p class="text-red-500 text-lg">❌ ${mensaje}</p>
                    <button onclick="app.cargarLugares()" 
                            class="mt-4 bg-tierra text-white px-6 py-2 rounded-full hover:bg-monte">
                        Reintentar
                    </button>
                </div>
            `;
        }
    }
}

// Inicializar la app cuando el DOM esté listo
let app;

document.addEventListener('DOMContentLoaded', () => {
    app = new KesurgeApp();
    app.init();
});
