// ===============================
// SECCIÓN 1: LOCALES DESTACADOS
// ===============================

// Esta función se encarga de pedir los locales y mostrarlos en pantalla
async function obtenerLocales() {
  try {
    // Pedimos los datos (por ahora desde un archivo local, luego será el backend)
    const respuesta = await fetch('locales.json');

    // Convertimos la respuesta en algo que JavaScript pueda usar
    const datos = await respuesta.json();

    // Buscamos el contenedor donde van las tarjetas
    const contenedor = document.getElementById('contenedor-locales');

    // Borramos el mensaje de "Cargando..."
    contenedor.innerHTML = '';

    // Recorremos cada local recibido
    datos.forEach(local => {
      // Creamos la tarjeta usando datos dinámicos
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

              <!-- Botón preparado para futuras acciones -->
              <button onclick="verDetalles(${local.id})" class="text-tierra hover:scale-110 transition-transform">
                +
              </button>
            </div>
          </div>
        </div>
      `;

      // Agregamos la tarjeta al contenedor
      contenedor.innerHTML += tarjetaHTML;
    });

  } catch (error) {
    // Si algo falla, mostramos un mensaje claro
    console.error("Error al cargar locales:", error);
    document.getElementById('contenedor-locales').innerHTML =
      "<p class='col-span-full text-center text-red-500'>No pudimos cargar los locales.</p>";
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


// ===============================
// SECCIÓN 3: MAPA (PREPARACIÓN)
// ===============================

// ===============================
// SECCIÓN MAPA – SIMULACIÓN BACKEND
// ===============================

async function cargarDatosMapa() {
  try {
    // 1. Pedimos los datos del "backend" (en realidad mapa.json)
    const respuesta = await fetch('mapa.json');

    // 2. Convertimos la respuesta en datos que JS entiende
    const puntos = await respuesta.json();

    // 3. Mostramos los datos en consola para entender qué llegó
    console.log("Datos recibidos del backend del mapa:");
    console.table(puntos);

    // 4. Acá más adelante se crearán los marcadores del mapa
    puntos.forEach(punto => {
      console.log(
        `📍 ${punto.nombre} (${punto.tipo}) en [${punto.lat}, ${punto.lng}]`
      );
    });

  } catch (error) {
    console.error("Error al cargar datos del mapa:", error);
  }
}


// ===============================
// SECCIÓN 4: INICIO GENERAL
// ===============================

// Cuando toda la página termina de cargar, arrancamos todo
document.addEventListener('DOMContentLoaded', () => {
  obtenerLocales();
  cargarEventosProximos();
  cargarDatosMapa(); // ← simulación del backend del mapa
});
