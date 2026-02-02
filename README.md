#  Kesurge - Plataforma de Descubrimiento Cultural

> Proyecto del Hackathon 5.0 - Sistema escalable de recopilación y visualización de lugares en Asunción, Paraguay

##  Descripción

Kesurge es una plataforma web que permite descubrir lugares de interés en Asunción, Paraguay. El sistema utiliza scraping automatizado de Google Places API para mantener una base de datos actualizada de restaurantes, museos, parques y más.

### ✨Características

-  **Scraping Automatizado**: Recopila datos de Google Places API
-  **API REST**: Backend robusto con Flask
-  **Frontend Moderno**: Interfaz responsive con Tailwind CSS
-  **Geolocalización**: Visualización de lugares en mapa
-  **Búsqueda y Filtros**: Por categoría, rating, etc.
-  **Escalable**: Arquitectura modular y preparada para crecer

##  Arquitectura

```
┌─────────────────┐
│   Frontend      │ (HTML/CSS/JS)
│   (Cliente)     │
└────────┬────────┘
         │ HTTP/JSON
         ↓
┌─────────────────┐
│   Backend API   │ (Flask)
│   (Servidor)    │
└────────┬────────┘
         │
         ↓
┌─────────────────┐      ┌──────────────────┐
│   Base Datos    │      │  Google Places   │
│   (SQLite)      │←─────│      API         │
└─────────────────┘      └──────────────────┘
```

##  Inicio Rápido

### Prerrequisitos

- Python 3.9 o superior
- Google Places API Key
- Git

### Instalación

1. **Clonar el repositorio**
```bash
git clone https://github.com/tu-usuario/kesurge.git
cd kesurge
```

2. **Configurar entorno virtual (recomendado)**
```bash
# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env y agregar tu API key
# GOOGLE_PLACES_API_KEY=tu_key_aqui
```

5. **Ejecutar scraping inicial**
```bash
python scripts/run_scraper.py
```

6. **Iniciar el servidor**
```bash
python backend/main.py
```

7. **Abrir el frontend**
```bash
# Opción 1: Usar Live Server de VS Code
# Opción 2: Abrir frontend/index.html en el navegador
# Opción 3: Servidor HTTP simple
cd frontend
python -m http.server 8000
```

Ahora accede a:
- Frontend: `http://localhost:8000`
- API: `http://localhost:5000`
- Health check: `http://localhost:5000/health`

## Estructura del Proyecto

```
kesurge/
│
├── backend/                    # Backend (Python/Flask)
│   ├── config/                # Configuración
│   │   ├── settings.py        # Variables globales
│   │   └── database.py        # Configuración DB
│   ├── models/                # Modelos de datos
│   │   └── lugar.py           # Modelo Lugar
│   ├── services/              # Lógica de negocio
│   │   ├── google_places.py   # Cliente API Google
│   │   └── scraper.py         # Orquestador scraping
│   ├── repositories/          # Acceso a datos
│   │   └── lugar_repository.py
│   ├── api/                   # API REST
│   │   ├── app.py            # Aplicación Flask
│   │   └── routes.py         # Endpoints
│   └── main.py               # Punto de entrada
│
├── frontend/                  # Frontend
│   ├── index.html            # Página principal
│   └── js/
│       ├── config.js         # Configuración
│       ├── api.js            # Cliente API
│       ├── app.js            # Lógica principal
│       └── components/       # Componentes UI
│
├── scripts/                  # Scripts utilitarios
│   └── run_scraper.py       # Script de scraping
│
├── requirements.txt         # Dependencias Python
└── README.md               # Este archivo
```

##  API Endpoints

### Lugares

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/lugares` | Obtener todos los lugares |
| GET | `/api/lugares?categoria=comida` | Filtrar por categoría |
| GET | `/api/lugares/{id}` | Obtener lugar específico |

**Ejemplo de respuesta:**
```json
{
  "total": 45,
  "categoria": "comida",
  "lugares": [
    {
      "id": 1,
      "place_id": "ChIJ...",
      "nombre": "Tierra Colorada",
      "direccion": "Av. Mariscal López...",
      "lat": -25.2637,
      "lng": -57.5759,
      "categoria": "comida",
      "rating": 4.5,
      "total_ratings": 234
    }
  ]
}
```

### Categorías

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/categorias` | Listar categorías y conteos |

### Estadísticas

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/estadisticas` | Estadísticas generales |

### Scraper

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | `/api/scraper/ejecutar` | Ejecutar scraping manual |

##  Desarrollo

### Ejecutar tests
```bash
pytest tests/
```

### Linting
```bash
# Instalar flake8
pip install flake8

# Ejecutar linter
flake8 backend/
```

### Agregar nueva categoría

1. Editar `backend/config/settings.py`:
```python
CATEGORIAS = {
    # ... existentes
    "nueva_categoria": ["tipo_google_places"],
}
```

2. Ejecutar scraping:
```bash
python scripts/run_scraper.py
```

##  Deployment

Ver [DEPLOYMENT.md](DEPLOYMENT.md) para instrucciones detalladas de despliegue en:
- Render
- Railway
- PythonAnywhere
- Vercel/Netlify (frontend)

##  Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

##  Licencia

Este proyecto está bajo la Licencia MIT. Ver `LICENSE` para más información.

##  Equipo

- **Project Manager & Co-Team Lead**: [Tu nombre]
- **Desarrolladores**: [Nombres del equipo]

##  Contacto

- Email: hola@kesurge.py
- GitHub: [@kesurge](https://github.com/kesurge)

---

