// ===============================
// SECCIÓN 1: LOCALES DESTACADOS
// ===============================

async function obtenerLocales() {
  try {
    const respuesta = await fetch('locales.json');
    datosLocales = await respuesta.json(); 
    
    const contenedor = document.getElementById('contenedor-locales');
    if (!contenedor) return;
    
    contenedor.innerHTML = ''; // Limpiamos el mensaje de cargando

    datosLocales.forEach(local => {
      // AQUÍ DEFINIMOS LA VARIABLE (Asegúrate de que empiece con 'const')
      const tarjetaHTML = `
        <div class="group bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all">
          <div class="relative h-56 overflow-hidden">
            <img src="${local.foto_url}" class="w-full h-full object-cover group-hover:scale-110 transition-transform">
            <span class="absolute top-4 right-4 bg-white/90 text-tierra text-xs font-bold px-3 py-1 rounded-full">
              ${local.categoria}
            </span>
          </div>
          <div class="p-6">
            <h4 class="font-serif text-xl text-carbon mb-2">${local.nombre}</h4>
            <p class="text-gray-500 text-sm mb-4">${local.descripcion_corta}</p>
            <div class="flex items-center justify-between">
              <span class="text-monte font-bold">${local.precio_simbolo}</span>
              <button class="text-tierra hover:scale-110 transition-transform"> 
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      `;

      // Ahora que está definida, la agregamos al HTML
      contenedor.innerHTML += tarjetaHTML;
    });

    // Dibujamos los pines después de las tarjetas
    if (typeof dibujarPines === "function") {
        dibujarPines(mapPreview);
    }

  } catch (error) {
    console.error("Error cargando locales:", error);
    const contenedor = document.getElementById('contenedor-locales');
    if (contenedor) {
      contenedor.innerHTML = `<p class="col-span-full text-center py-10 text-red-500 font-bold">Error: Verifica que tu locales.json no tenga errores de sintaxis.</p>`;
    }
  }
}




// ===============================
// SECCIÓN 2: EVENTOS PRÓXIMOS
// ===============================

// Esta función carga los eventos destacados
async function cargarEventosProximos() {
  try {
    const respuesta = await fetch('eventos.json');
    const eventos = await respuesta.json();

    // Nos quedamos solo con eventos destacados y máximo 3
    const eventosAMostrar = eventos
      .filter(evento => evento.es_destacado === true)
      .slice(0, 3);

    const contenedor = document.getElementById('contenedor-eventos-proximos');
    contenedor.innerHTML = '';

    eventosAMostrar.forEach(evento => {
      const cardHTML = `
                <div class="group relative bg-white/5 border border-white/10 p-1 rounded-[2rem] transition-all duration-500 hover:bg-white/10 hover:-translate-y-2">
                    <div class="relative h-64 overflow-hidden rounded-[1.8rem]">
                        <img src="${evento.imagen}" class="w-full h-full object-cover transition-transform duration-700 group-hover:scale-110">
                        <div class="absolute inset-0 bg-gradient-to-t from-tierra via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-500 flex items-end p-6">
                            <button class="bg-ocaso text-tierra font-bold py-2 px-6 rounded-full text-sm transform translate-y-4 group-hover:translate-y-0 transition-transform">
                                Ver detalles
                            </button>
                        </div>
                    </div>
                    <div class="p-6">
                        <div class="flex justify-between items-start mb-2">
                            <h4 class="font-serif text-2xl">${evento.titulo}</h4>
                            <span class="bg-ocaso/20 text-ocaso text-[10px] px-2 py-1 rounded-md">${evento.fecha}</span>
                        </div>
                        <p class="text-arena/70 text-sm font-light">${evento.lugar}</p>
                        <div class="mt-4 pt-4 border-t border-white/10 flex items-center text-xs text-ocaso">
                             <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path></svg>
                             ${evento.hora} h
                        </div>
                    </div>
                </div>
            `;

      contenedor.innerHTML += cardHTML;
    });

  } catch (error) {
    console.error("Error cargando eventos:", error);
  }
}

//======================
// SECCION 3: KENMAP
//=======================

// Variables globales
let mapPreview;
let mapFull;
let datosLocales = []; 

// 1. Inicializar el mapa pequeño (Carga siempre)
function initPreviewMap() {
    if (mapPreview) return;
    mapPreview = L.map('map-preview').setView([-25.2967, -57.6270], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(mapPreview);
}

// 2. Inicializar el mapa grande (Carga solo al abrir modal)
function initFullMap() {
    if (!mapFull) {
        mapFull = L.map('map-full').setView([-25.2967, -57.6270], 14);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(mapFull);
    }
    
    setTimeout(() => {
        mapFull.invalidateSize();
        dibujarPines(mapFull);
    }, 200);
}

// 3. Función única para dibujar los pines
function dibujarPines(mapaDestino) {
    if (!mapaDestino) return;
    datosLocales.forEach(local => {
        if (local.lat && local.lng) {
            L.marker([local.lat, local.lng])
                .addTo(mapaDestino)
                .bindPopup(`<b class="text-tierra">${local.nombre}</b><br>${local.categoria}`);
        }
    });
}

// 4. Función de locales UNIFICADA (Aquí estaba el error)
async function obtenerLocales() {
  try {
    const respuesta = await fetch('locales.json');
    datosLocales = await respuesta.json(); 
    
    const contenedor = document.getElementById('contenedor-locales');
    if (!contenedor) return;
    contenedor.innerHTML = '';

    datosLocales.forEach(local => {
      // Definimos la tarjeta con los datos del JSON
      const tarjetaHTML = `
        <div class="group bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all">
          <div class="relative h-56 overflow-hidden">
            <img src="${local.foto_url}" class="w-full h-full object-cover group-hover:scale-110 transition-transform">
            <span class="absolute top-4 right-4 bg-white/90 text-tierra text-xs font-bold px-3 py-1 rounded-full">
              ${local.categoria}
            </span>
          </div>
          <div class="p-6">
            <h4 class="font-serif text-xl text-carbon mb-2">${local.nombre}</h4>
            <p class="text-gray-500 text-sm mb-4">${local.descripcion_corta}</p>
            <div class="flex items-center justify-between">
              <span class="text-monte font-bold">${local.precio_simbolo}</span>
              <button class="text-tierra hover:scale-110 transition-transform"> 
                <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" />
                </svg>
              </button>
            </div>
          </div>
        </div>
      `;
      contenedor.innerHTML += tarjetaHTML;
    });

    // Dibujamos los pines en el mapa pequeño
    dibujarPines(mapPreview);

  } catch (error) {
    console.error("Error cargando locales:", error);
  }
}

// 5. Función del Modal
window.toggleMapModal = function() {
    const modal = document.getElementById('mapModal');
    const isOpening = modal.classList.contains('hidden');
    
    modal.classList.toggle('hidden');
    document.body.classList.toggle('overflow-hidden');

    if (isOpening) {
        initFullMap();
    }
};

// ===============================
// SECCIÓN 4: INICIO GENERAL
// ===============================

document.addEventListener('DOMContentLoaded', () => {
  initPreviewMap();
  obtenerLocales();
  cargarEventosProximos();
});




