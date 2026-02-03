import sqlite3
from datetime import datetime

def generar():
    try:
        conn = sqlite3.connect("qsurge.db")
        cursor = conn.cursor()
        # Traemos los eventos más recientes
        cursor.execute("SELECT titulo, lugar, fecha, descripcion, url, actualizado_en FROM eventos ORDER BY id DESC")
        eventos = cursor.fetchall()
        conn.close()
    except Exception as e:
        print(f"❌ Error DB: {e}")
        return

    # Dividimos el HTML de tu compañero en partes para inyectar los datos
    html_inicio = """<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Kesurge?! - Agenda Inteligente</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script>
    tailwind.config = {
      theme: {
        extend: {
          colors: { tierra: '#A52A2A', monte: '#2D5A27', arena: '#FDF5E6', ocaso: '#F7A00A', carbon: '#1A1A1A' },
          fontFamily: { serif: ['Playfair Display', 'serif'], sans: ['Inter', 'sans-serif'] }
        }
      }
    }
  </script>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600&family=Playfair+Display:wght@700&display=swap" rel="stylesheet">
</head>
<body class="bg-arena">
    <nav id="main-header" class="bg-arena/80 backdrop-blur-md sticky top-0 z-50 px-8 py-4 flex justify-between items-center border-b border-tierra/10">
      <div class="flex items-center space-x-2">
        <div class="w-8 h-8 bg-tierra rounded-full"></div> 
        <span class="font-serif text-xl font-bold text-tierra tracking-tight">Kesurge?!</span>
      </div>
      <div class="hidden md:flex space-x-10 text-carbon font-medium">
        <a href="#" class="hover:text-tierra transition-colors">Explorar</a>
        <a href="#" class="hover:text-tierra transition-colors">Mapa</a>
        <a href="#" class="hover:text-tierra transition-colors">Agenda</a>
      </div>
      <div class="flex items-center space-x-6">
        <button class="bg-tierra text-white px-5 py-2 rounded-full text-sm font-bold hover:bg-monte transition-colors">ES</button>
      </div>
    </nav>

    <section class="relative h-[80vh] flex items-stretch overflow-hidden">
      <div class="absolute top-0 left-0 w-full h-full z-0">
        <img src="palacio_lopez.jpg" alt="Asunción" class="w-full h-full object-cover">
        <div class="absolute inset-0 bg-black/50"></div>
      </div>
      <div class="relative z-10 w-full flex items-center justify-center p-8">
        <div class="bg-arena/90 backdrop-blur-sm rounded-xl p-8 shadow-lg border border-tierra/20 max-w-2xl text-center">
          <h2 class="font-serif text-4xl text-tierra mb-4">¡Asunción está viva!</h2>
          <p class="text-carbon mb-6">Descubrí los eventos culturales detectados por nuestra IA en tiempo real.</p>
          <div class="flex justify-center space-x-4">
             <span class="badge bg-tierra text-white px-4 py-1 rounded-full text-xs">Actualización cada 10 min</span>
          </div>
        </div>
      </div>
    </section>

    <section class="bg-tierra py-20 px-6 text-arena">
      <div class="max-w-7xl mx-auto">
        <div class="mb-12">
          <h3 class="text-ocaso font-bold uppercase tracking-widest text-sm">Kesurge ahora mismo?!</h3>
          <h2 class="font-serif text-4xl mt-2">Agenda Detectada por QSurge</h2>
          <p class="text-arena/70 text-sm mt-2">Última sincronización: """ + datetime.now().strftime("%H:%M:%S") + """</p>
        </div>
        
        <div id="contenedor-eventos-proximos" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">"""

    # Generamos dinámicamente las tarjetas de eventos con el estilo de tu compañero
    html_eventos = ""
    for ev in eventos:
        titulo, lugar, fecha, desc, url, actualizado = ev
        html_eventos += f"""
          <div class="bg-white/10 backdrop-blur-md p-6 rounded-2xl border border-white/10 flex flex-col h-full hover:bg-white/20 transition-all group">
            <div class="flex justify-between items-start mb-4">
              <span class="text-ocaso text-xs font-bold tracking-widest uppercase">{desc}</span>
              <span class="text-arena/50 text-[10px]"><i class="bi bi-clock"></i> {actualizado}</span>
            </div>
            <h4 class="font-serif text-xl mb-3 group-hover:text-ocaso transition-colors">{titulo}</h4>
            <div class="space-y-2 mb-6">
              <p class="text-sm text-arena/80 flex items-center">
                <svg class="w-4 h-4 mr-2 text-ocaso" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"></path></svg>
                {lugar}
              </p>
              <p class="text-sm text-arena/80 flex items-center">
                <svg class="w-4 h-4 mr-2 text-ocaso" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z"></path></svg>
                {fecha}
              </p>
            </div>
            <a href="{url}" target="_blank" class="mt-auto inline-block border border-ocaso text-ocaso hover:bg-ocaso hover:text-tierra px-4 py-2 rounded-full text-center text-sm font-bold transition-all">
              Ver Detalles
            </a>
          </div>"""

    html_fin = """
        </div>
      </div>
    </section>

    <footer class="bg-arena text-carbon py-16 px-6 border-t border-tierra/10">
      <div class="max-w-7xl mx-auto text-center">
        <p class="text-xs text-gray-500">© 2026 Kesurge?! - Tecnología QSurge para Asunción.</p>
      </div>
    </footer>
</body>
</html>"""

    # Unimos todo y guardamos
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html_inicio + html_eventos + html_fin)
    print(f"✅ Interfaz 'Kesurge?!' actualizada con éxito.")