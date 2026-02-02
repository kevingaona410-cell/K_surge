#  Guía de Deployment - Kesurge

Esta guía te ayudará a desplegar Kesurge en producción.

##  Checklist Pre-Deployment

- [ ] API Key de Google Places configurada
- [ ] Variables de entorno configuradas
- [ ] Base de datos con datos (ejecutar scraping)
- [ ] CORS configurado para el dominio de producción
- [ ] Tests ejecutados y pasando
- [ ] Frontend apuntando a la URL correcta de la API

##  Backend - Opciones de Deployment

### Opción 1: Render (Recomendado - Gratis)

1. **Crear cuenta en [Render](https://render.com)**

2. **Crear nuevo Web Service**
   - Conectar con GitHub
   - Seleccionar repositorio de Kesurge

3. **Configurar el servicio:**
   - **Name**: kesurge-api
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT backend.api.app:crear_app()`
   - **Branch**: main

4. **Variables de entorno:**
   ```
   GOOGLE_PLACES_API_KEY=tu_key_aqui
   DATABASE_PATH=/opt/render/project/lugares.db
   ALLOWED_ORIGINS=https://tu-frontend.netlify.app
   DEBUG=False
   ```

5. **Agregar gunicorn a requirements.txt:**
   ```bash
   echo "gunicorn==21.2.0" >> requirements.txt
   ```

6. **Deploy** 🎉

Tu API estará en: `https://kesurge-api.onrender.com`

### Opción 2: Railway

1. **Crear cuenta en [Railway](https://railway.app)**

2. **New Project → Deploy from GitHub**

3. **Variables de entorno:**
   ```
   GOOGLE_PLACES_API_KEY=tu_key
   ALLOWED_ORIGINS=*
   ```

4. **Configuración automática** - Railway detecta Python

### Opción 3: PythonAnywhere

1. **Crear cuenta en [PythonAnywhere](https://www.pythonanywhere.com)**

2. **Subir código:**
   ```bash
   # En la consola de PythonAnywhere
   git clone https://github.com/tu-usuario/kesurge.git
   cd kesurge
   pip install --user -r requirements.txt
   ```

3. **Configurar Web App:**
   - Python 3.9
   - Framework: Flask
   - WSGI file: apuntar a `backend/api/app.py`

4. **Configurar WSGI:**
   ```python
   import sys
   path = '/home/tu_usuario/kesurge'
   if path not in sys.path:
       sys.path.append(path)
   
   from backend.api.app import crear_app
   application = crear_app()
   ```

##  Frontend - Deployment

### Opción 1: Netlify (Recomendado)

1. **Arrastrar carpeta `frontend/` a [Netlify Drop](https://app.netlify.com/drop)**

2. **Configurar variables:**
   - Editar `frontend/js/config.js`
   - Cambiar `API_BASE_URL` a tu URL de producción

3. **Deploy automático** 

### Opción 2: Vercel

1. **Instalar Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Deploy:**
   ```bash
   cd frontend
   vercel
   ```

### Opción 3: GitHub Pages

1. **Subir a rama `gh-pages`:**
   ```bash
   git checkout -b gh-pages
   git add frontend/*
   git commit -m "Deploy to GitHub Pages"
   git push origin gh-pages
   ```

2. **Activar GitHub Pages en Settings**

##  Base de Datos

### SQLite (Desarrollo/Pequeña Escala)

Para producción ligera, SQLite funciona bien. Asegúrate de:

```python
# En settings.py
DATABASE_PATH = os.getenv("DATABASE_PATH", "/ruta/persistente/lugares.db")
```

### PostgreSQL (Producción a Escala)

Para mayor escala, migrar a PostgreSQL:

1. **Instalar dependencias:**
   ```bash
   pip install psycopg2-binary
   ```

2. **Modificar `database.py`:**
   ```python
   import psycopg2
   
   DATABASE_URL = os.getenv("DATABASE_URL")
   conn = psycopg2.connect(DATABASE_URL)
   ```

3. **Servicios gratuitos:**
   - [Neon](https://neon.tech) - PostgreSQL gratis
   - [Supabase](https://supabase.com) - PostgreSQL + más

##  Automatizar Scraping

### Opción 1: Cron Job (Linux)

```bash
# Editar crontab
crontab -e

# Agregar línea (ejecutar diariamente a las 3 AM)
0 3 * * * /ruta/a/venv/bin/python /ruta/a/kesurge/scripts/run_scraper.py
```

### Opción 2: GitHub Actions

Crear `.github/workflows/scraper.yml`:

```yaml
name: Daily Scraper

on:
  schedule:
    - cron: '0 3 * * *'  # 3 AM diario
  workflow_dispatch:  # Manual

jobs:
  scrape:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - run: pip install -r requirements.txt
      - run: python scripts/run_scraper.py
        env:
          GOOGLE_PLACES_API_KEY: ${{ secrets.GOOGLE_PLACES_API_KEY }}
```

### Opción 3: Endpoint API + Servicio Externo

Usar un servicio como [cron-job.org](https://cron-job.org) para llamar a:

```
POST https://tu-api.com/api/scraper/ejecutar
```

##  Seguridad

### 1. Proteger API Key

**NUNCA** commitear el `.env`:

```bash
# Asegurarse que esté en .gitignore
echo ".env" >> .gitignore
```

### 2. Rate Limiting

Agregar rate limiting a la API:

```python
# pip install Flask-Limiter
from flask_limiter import Limiter

limiter = Limiter(app, default_limits=["100 per hour"])
```

### 3. HTTPS

Asegurarse que tu dominio use HTTPS (Netlify/Vercel lo hacen automáticamente)

##  Monitoreo

### Logs

Configurar logging en producción:

```python
# backend/utils/logger.py
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

### Métricas

Usar servicios como:
- [Sentry](https://sentry.io) para error tracking
- [Google Analytics](https://analytics.google.com) para frontend

##  CI/CD

### GitHub Actions para Deploy Automático

Crear `.github/workflows/deploy.yml`:

```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST https://api.render.com/deploy/srv-xxx?key=${{ secrets.RENDER_DEPLOY_KEY }}
```

##  Testing en Producción

```bash
# Health check
curl https://tu-api.com/health

# Obtener lugares
curl https://tu-api.com/api/lugares?categoria=comida
```

##  Checklist Final

- [ ] Backend desplegado y funcionando
- [ ] Frontend desplegado y conectado al backend
- [ ] CORS configurado correctamente
- [ ] Variables de entorno configuradas
- [ ] Base de datos con datos
- [ ] Scraping automatizado configurado
- [ ] SSL/HTTPS activo
- [ ] Logs y monitoreo configurados
- [ ] Documentación actualizada

##  Troubleshooting

### Error de CORS
```python
# Asegurarse que ALLOWED_ORIGINS incluya tu frontend
ALLOWED_ORIGINS = "https://tu-frontend.netlify.app"
```

### Base de datos no persiste
```python
# Usar ruta absoluta para DATABASE_PATH
DATABASE_PATH = "/opt/render/project/lugares.db"
```

### API no responde
- Verificar logs del servicio
- Verificar que el puerto esté correctamente configurado
- Verificar que gunicorn esté instalado

---


