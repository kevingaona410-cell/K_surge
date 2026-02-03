# Kesurge - Estructura del Proyecto

## 📁 Estructura de Carpetas

```
kesurge/
│
├── backend/
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py          # Configuración general (API keys, DB, etc.)
│   │   └── database.py          # Configuración de la base de datos
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── lugar.py             # Modelo de datos para Lugares
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── google_places.py     # Servicio de API Google Places
│   │   └── scraper.py           # Orquestador de scraping
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── lugar_repository.py  # Acceso a datos de lugares
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── app.py               # Aplicación Flask/FastAPI
│   │   ├── routes.py            # Endpoints de la API
│   │   └── schemas.py           # Esquemas de validación
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── logger.py            # Sistema de logging
│   │
│   └── main.py                  # Punto de entrada del backend
│
├── frontend/
│   ├── index.html               # Tu HTML actual
│   ├── css/
│   │   └── styles.css           # Estilos personalizados
│   ├── js/
│   │   ├── config.js            # Configuración del frontend
│   │   ├── api.js               # Cliente para llamadas a la API
│   │   ├── components/
│   │   │   ├── map.js           # Componente del mapa
│   │   │   ├── cards.js         # Componente de tarjetas
│   │   │   └── filters.js       # Componente de filtros
│   │   └── app.js               # Lógica principal
│   └── assets/
│       └── images/
│
├── scripts/
│   └── run_scraper.py           # Script para ejecutar scraping
│
├── tests/
│   ├── test_api.py
│   └── test_scraper.py
│
├── requirements.txt             # Dependencias Python
├── .env                         # Variables de entorno (NO subir a git)
├── .gitignore
└── README.md
```

##  Flujo de Comunicación Frontend-Backend

### 1. **Scraping (Actualización de Datos)**
```
Script de Scraping → Google Places API → Base de Datos
```

### 2. **Usuario consulta datos**
```
Frontend → Backend API → Base de Datos → Backend API → Frontend
```

### 3. **Proceso Completo**
```
┌─────────────────┐
│   Cron Job      │ (Cada X horas)
│  (Scraping)     │
└────────┬────────┘
         ↓
┌─────────────────┐
│ Google Places   │
│      API        │
└────────┬────────┘
         ↓
┌─────────────────┐
│   SQLite DB     │
└────────┬────────┘
         ↓
┌─────────────────┐
│  Backend API    │ (Flask/FastAPI)
│  (REST/JSON)    │
└────────┬────────┘
         ↓
┌─────────────────┐
│   Frontend      │ (HTML/JS)
│   (Navegador)   │
└─────────────────┘
```

##  Endpoints de la API

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/api/lugares` | Obtener todos los lugares |
| GET | `/api/lugares?categoria=comida` | Filtrar por categoría |
| GET | `/api/lugares/{id}` | Obtener lugar específico |
| GET | `/api/categorias` | Listar categorías disponibles |
| POST | `/api/scraper/run` | Ejecutar scraping manual |

##  Tecnologías Utilizadas

### Backend
- **Python 3.9+**
- **Flask** o **FastAPI** (Framework web)
- **SQLite** (Base de datos)
- **Requests** (Cliente HTTP)
- **SQLAlchemy** (ORM - opcional pero recomendado)

### Frontend
- **HTML5/CSS3**
- **JavaScript Vanilla**
- **Tailwind CSS**
- **Google Maps JavaScript API**

### Deployment
- **Backend**: Render, Railway, o PythonAnywhere
- **Frontend**: Netlify, Vercel, o GitHub Pages
- **Base de Datos**: SQLite local o PostgreSQL (producción)

##  Próximos Pasos

1.  Modularizar código actual
2.  Crear API REST
3.  Conectar frontend con API
4.  Implementar autenticación (opcional)
5.  Agregar más fuentes de datos
6.  Deploy a producción
