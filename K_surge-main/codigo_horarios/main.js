// ===============================
// SECCIÓN 1: EVENTOS PRÓXIMOS
// ===============================
async function cargarEventosProximos() {
  try {
    const respuesta = await fetch('eventos.json');
    const eventos = await respuesta.json();

    const eventosAMostrar = eventos
      .filter(evento => evento.es_destacado === true)
      .slice(0, 3);

    const contenedor = document.getElementById('contenedor-eventos-proximos');
    if (!contenedor) return;
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
// SECCION 2: KENMAP
//=======================
let mapPreview;
let mapFull;
let datosLocales = []; 

function initPreviewMap() {
    if (mapPreview) return;
    mapPreview = L.map('map-preview').setView([-25.2967, -57.6270], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap'
    }).addTo(mapPreview);
}

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

async function obtenerLocales() {
  try {
    const respuesta = await fetch('lugares_frontend.json');
    datosLocales = await respuesta.json(); 
    const contenedor = document.getElementById('contenedor-locales');
    if (contenedor) {
        contenedor.innerHTML = '';
        datosLocales.forEach(local => {
          const tarjetaHTML = `
            <div class="group bg-white rounded-3xl overflow-hidden shadow-sm hover:shadow-xl transition-all">
              <div class="relative h-56 overflow-hidden">
                <img src="${local.foto_url}" class="w-full h-full object-cover group-hover:scale-110 transition-transform">
                <span class="absolute top-4 right-4 bg-white/90 text-tierra text-xs font-bold px-3 py-1 rounded-full">${local.categoria}</span>
              </div>
              <div class="p-6">
                <h4 class="font-serif text-xl text-carbon mb-2">${local.nombre}</h4>
                <p class="text-gray-500 text-sm mb-4">${local.telefono}</p>
                <div class="flex items-center justify-between">
                  <span class="text-monte font-bold">${local.rating}</span>
                  <button class="text-tierra hover:scale-110 transition-transform"> 
                    <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" class="w-6 h-6"><path stroke-linecap="round" stroke-linejoin="round" d="M12 4.5v15m7.5-7.5h-15" /></svg>
                  </button>
                </div>
              </div>
            </div>`;
          contenedor.innerHTML += tarjetaHTML;
        });
    }
    dibujarPines(mapPreview);
  } catch (error) {
    console.error("Error cargando locales:", error);
  }
}

window.toggleMapModal = function() {
    const modal = document.getElementById('mapModal');
    const isOpening = modal.classList.contains('hidden');
    modal.classList.toggle('hidden');
    document.body.classList.toggle('overflow-hidden');
    if (isOpening) initFullMap();
};

// ===============================
// SECCIÓN 3: AGENDA EDITORIAL
// ===============================
async function cargarAgendaCompleta() {
  try {
    const respuesta = await fetch('agenda.json'); 
    const eventos = await respuesta.json();
    const contenedor = document.getElementById('contenedor-eventos');
    if (!contenedor) return;
    contenedor.innerHTML = '';

    eventos.forEach((ev, index) => {
      const numero = (index + 1).toString().padStart(2, '0');
      const tarjetaHTML = `
        <div class="event-row group relative grid grid-cols-1 lg:grid-cols-12 gap-8 items-center opacity-0 translate-y-10 transition-all duration-700" id="event-row-${index}">
          <div class="lg:col-span-5 relative">
            <div class="aspect-[4/5] overflow-hidden rounded-[4rem] relative z-10 shadow-2xl">
              <img src="${ev.imagen}" class="w-full h-full object-cover grayscale group-hover:grayscale-0 transition-all duration-700">
            </div>
            <span class="absolute -bottom-10 -left-10 text-[10rem] md:text-[12rem] font-serif font-black text-tierra/10 leading-none select-none z-0">${numero}</span>
          </div>
          <div class="lg:col-span-7 lg:pl-12">
            <div class="flex items-center gap-4 mb-6">
              <span class="h-px w-12 bg-tierra"></span>
              <span class="text-tierra font-black uppercase tracking-[0.3em] text-[10px]">${ev.categoria}</span>
            </div>
            <h3 class="font-serif text-5xl md:text-7xl text-carbon mb-8 leading-none tracking-tighter group-hover:translate-x-4 transition-transform duration-500">${ev.titulo}</h3>
            <div class="flex items-end justify-between border-b border-carbon/10 pb-8">
              <div class="space-y-2">
                <p class="text-carbon font-bold text-xl italic">${ev.lugar}</p>
                <p class="text-gray-500 font-medium">${ev.fecha} — ${ev.hora}hs</p>
              </div>
              <button class="w-16 h-16 rounded-full bg-carbon text-white flex items-center justify-center group-hover:bg-tierra group-hover:rotate-45 transition-all duration-500">
                <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-width="2" d="M12 4.5v15m7.5-7.5h-15" /></svg>
              </button>
            </div>
          </div>
        </div>`;
      contenedor.innerHTML += tarjetaHTML;
      setTimeout(() => {
        const row = document.getElementById(`event-row-${index}`);
        if (row) row.classList.remove('opacity-0', 'translate-y-10');
      }, index * 150);
    });
  } catch (error) {
    console.error("Error cargando la agenda:", error);
  }
}

// ===============================
// SECCIÓN 4: INICIO GENERAL
// ===============================
document.addEventListener('DOMContentLoaded', () => {
  const contenedorAgenda = document.getElementById('contenedor-eventos');
  const contenedorProximos = document.getElementById('contenedor-eventos-proximos');
  const mapaPreview = document.getElementById('map-preview');

  if (contenedorAgenda) { cargarAgendaCompleta(); }
  if (contenedorProximos) { cargarEventosProximos(); }
  if (mapaPreview) {
    initPreviewMap();
    obtenerLocales();
  }

  // Inicializar listeners de formularios y popups
  initFormListener(); 
  
  // ACTIVACIÓN DEL POPUP DE REGISTRO (Lead Magnet)
  // Se dispara a los 8 segundos de entrar a la página
  setTimeout(() => {
      verificarYMostrarRegistro();
  }, 8000); 
});

// ==========================================
// SECCIÓN 5: FORMULARIO DE REGISTRO DE LOCAL
// ==========================================
window.toggleFormModal = function() {
    const formModal = document.getElementById('formModal');
    if (!formModal) return;
    formModal.classList.toggle('hidden');
    document.body.classList.toggle('overflow-hidden');
};

function initFormListener() {
    const formModal = document.getElementById('formModal');
    if (formModal) {
        formModal.addEventListener('click', (e) => {
            if (e.target === formModal) toggleFormModal();
        });
    }
}

// ==========================================
// SECCIÓN 6: POPUP DE SUSCRIPCIÓN (USUARIOS)
// ==========================================
function verificarYMostrarRegistro() {
    // Verificamos si el usuario ya se registró antes en este navegador
    const yaRegistrado = localStorage.getItem('usuario_suscrito');
    const modal = document.getElementById('userRegisterModal');

    if (!yaRegistrado && modal) {
        modal.classList.remove('hidden');
        document.body.classList.add('overflow-hidden'); // Bloquea el scroll
    }

    // Configuración del envío del formulario
    const form = document.getElementById('leadForm');
    if (form) {
        form.onsubmit = (e) => {
            e.preventDefault();
            // Guardamos la marca de registro exitoso
            
            
            // Cerramos y liberamos scroll
            modal.classList.add('hidden');
            document.body.classList.remove('overflow-hidden');
            
            alert('¡Gracias! Ahora recibirás nuestros reportes semanales.');
        };
    }
}