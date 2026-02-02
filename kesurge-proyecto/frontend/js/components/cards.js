// frontend/js/components/cards.js
/**
 * Componente para renderizar tarjetas de lugares
 */

class LugarCard {
    /**
     * Genera el HTML de una tarjeta de lugar
     * @param {object} lugar - Datos del lugar
     * @returns {string} - HTML de la tarjeta
     */
    static render(lugar) {
        // Determinar símbolo de precio
        const precioSimbolos = {
            1: '$',
            2: '$$',
            3: '$$$',
            4: '$$$$'
        };
        const precio = lugar.precio_nivel 
            ? precioSimbolos[lugar.precio_nivel] 
            : 'N/A';

        // Rating visual
        const stars = this.renderStars(lugar.rating);

        return `
            <div class="group bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300">
                <div class="relative h-56 overflow-hidden bg-gray-200">
                    ${lugar.foto_referencia 
                        ? `<img src="https://maps.googleapis.com/maps/api/place/photo?maxwidth=600&photo_reference=${lugar.foto_referencia}&key=${CONFIG.MAP.API_KEY}" 
                               class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-500"
                               alt="${lugar.nombre}">`
                        : `<div class="w-full h-full flex items-center justify-center text-6xl">
                               ${CONFIG.CATEGORIAS[lugar.categoria]?.icono || '📍'}
                           </div>`
                    }
                    <span class="absolute top-4 right-4 bg-white/90 backdrop-blur-md text-tierra text-xs font-bold px-3 py-1 rounded-full">
                        ${CONFIG.CATEGORIAS[lugar.categoria]?.nombre || lugar.categoria}
                    </span>
                </div>
                
                <div class="p-6">
                    <h4 class="font-serif text-xl text-carbon mb-2">${lugar.nombre}</h4>
                    
                    <p class="text-gray-500 text-sm mb-3 truncate" title="${lugar.direccion}">
                        📍 ${lugar.direccion || 'Dirección no disponible'}
                    </p>
                    
                    <div class="flex items-center mb-3">
                        ${stars}
                        <span class="ml-2 text-sm text-gray-600">
                            ${lugar.rating.toFixed(1)} (${lugar.total_ratings || 0})
                        </span>
                    </div>
                    
                    <div class="flex items-center justify-between">
                        <span class="text-monte font-bold">${precio}</span>
                        <button 
                            onclick="verDetalles(${lugar.id})" 
                            class="text-tierra hover:scale-110 transition-transform">
                            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" 
                                      d="M13 7l5 5m0 0l-5 5m5-5H6"></path>
                            </svg>
                        </button>
                    </div>
                </div>
            </div>
        `;
    }

    /**
     * Genera estrellas para el rating
     * @param {number} rating - Rating del 0-5
     * @returns {string} - HTML con estrellas
     */
    static renderStars(rating) {
        const fullStars = Math.floor(rating);
        const hasHalfStar = rating % 1 >= 0.5;
        const emptyStars = 5 - fullStars - (hasHalfStar ? 1 : 0);

        let stars = '';

        // Estrellas llenas
        for (let i = 0; i < fullStars; i++) {
            stars += '<span class="text-ocaso">★</span>';
        }

        // Media estrella
        if (hasHalfStar) {
            stars += '<span class="text-ocaso">⯨</span>';
        }

        // Estrellas vacías
        for (let i = 0; i < emptyStars; i++) {
            stars += '<span class="text-gray-300">★</span>';
        }

        return stars;
    }

    /**
     * Renderiza múltiples tarjetas en un contenedor
     * @param {Array} lugares - Array de lugares
     * @param {string} containerId - ID del contenedor donde renderizar
     */
    static renderMultiple(lugares, containerId) {
        const container = document.getElementById(containerId);
        
        if (!container) {
            console.error(`Contenedor ${containerId} no encontrado`);
            return;
        }

        if (lugares.length === 0) {
            container.innerHTML = `
                <div class="col-span-full text-center py-12">
                    <p class="text-gray-500 text-lg">No se encontraron lugares</p>
                </div>
            `;
            return;
        }

        container.innerHTML = lugares.map(lugar => this.render(lugar)).join('');
    }
}

/**
 * Función global para ver detalles de un lugar
 * @param {number} lugarId - ID del lugar
 */
async function verDetalles(lugarId) {
    try {
        const lugar = await api.obtenerLugar(lugarId);
        
        // Aquí puedes implementar un modal o redirección
        console.log('Detalles del lugar:', lugar);
        
        // Por ahora, solo mostrar un alert
        alert(`${lugar.nombre}\n\n${lugar.direccion}\nRating: ${lugar.rating} ⭐`);
        
        // TODO: Implementar modal con información completa
        
    } catch (error) {
        console.error('Error al obtener detalles:', error);
        alert('Error al cargar los detalles del lugar');
    }
}
