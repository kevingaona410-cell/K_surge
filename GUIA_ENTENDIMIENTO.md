# Entendiendo el Sistema Kesurge

Esta guía te ayudará a entender cómo funciona el sistema completo, ideal para un Project Manager que quiere involucrarse en los procesos técnicos.

## Conceptos Clave

### 1. Arquitectura Cliente-Servidor

```
┌──────────────┐                    ┌──────────────┐
│   FRONTEND   │ ←── HTTP/JSON ──→  │   BACKEND    │
│ (Navegador)  │                    │  (Servidor)  │
└──────────────┘                    └──────┬───────┘
                                           │
                                           ↓
                                    ┌──────────────┐
                                    │  BASE DATOS  │
                                    └──────────────┘
```

**Frontend**: Lo que ve el usuario (HTML, CSS, JavaScript)
**Backend**: Servidor que procesa solicitudes y maneja datos (Python, Flask)
**Base de Datos**: Almacena la información (SQLite)

### 2. API REST

Una API REST es como un menú de restaurante:
- Tienes **endpoints** (platos del menú)
- Haces **peticiones** (ordenas un plato)
- Recibes **respuestas** (te traen la comida)

**Ejemplo práctico:**

```javascript
// El frontend "pide" datos al backend
fetch('http://localhost:5000/api/lugares')
  .then(response => response.json())  // Convierte la respuesta a JSON
  .then(data => {
    console.log(data);  // { total: 45, lugares: [...] }
  });
```

### 3. Flujo de Datos Completo

```
USUARIO → Click en "Gastronomía"
   ↓
FRONTEND (app.js)
   → filtrarPorCategoria('comida')
   → api.obtenerLugares({ categoria: 'comida' })
   ↓
API CALL
   → GET http://localhost:5000/api/lugares?categoria=comida
   ↓
BACKEND (routes.py)
   → obtener_lugares()
   → repository.obtener_todos(categoria='comida')
   ↓
BASE DE DATOS
   → SELECT * FROM lugares WHERE categoria = 'comida'
   ↓
RESPUESTA
   ← { total: 45, lugares: [...] }
   ↓
FRONTEND
   → LugarCard.renderMultiple(lugares)
   ↓
USUARIO ve las tarjetas de restaurantes
```

##  Arquitectura del Backend

### Patrón de Capas

El backend está organizado en capas, cada una con una responsabilidad específica:

```
┌─────────────────────────────────────────┐
│           API Layer (routes.py)         │  ← Maneja HTTP requests
├─────────────────────────────────────────┤
│        Service Layer (scraper.py)       │  ← Lógica de negocio
├─────────────────────────────────────────┤
│   Repository Layer (lugar_repository)   │  ← Acceso a datos
├─────────────────────────────────────────┤
│      Database Layer (database.py)       │  ← Conexión a BD
└─────────────────────────────────────────┘
```

### ¿Por qué esta organización?

1. **Separación de Responsabilidades**: Cada capa hace una cosa y la hace bien
2. **Testeable**: Puedes probar cada capa independientemente
3. **Mantenible**: Cambios en una capa no afectan a las demás
4. **Escalable**: Fácil agregar nuevas funcionalidades

### Ejemplo de Flujo

Cuando un usuario pide lugares:

1. **API Layer** (`routes.py`):
   ```python
   @api_blueprint.route('/lugares')
   def obtener_lugares():
       categoria = request.args.get('categoria')
       lugares = repository.obtener_todos(categoria=categoria)
       return jsonify(lugares)
   ```

2. **Repository Layer** (`lugar_repository.py`):
   ```python
   def obtener_todos(self, categoria=None):
       cursor.execute("SELECT * FROM lugares WHERE categoria = ?", (categoria,))
       return [Lugar.from_db_row(row) for row in cursor.fetchall()]
   ```

3. **Database Layer** (`database.py`):
   ```python
   def get_cursor(self):
       cursor = self._connection.cursor()
       yield cursor
       self._connection.commit()
   ```

##  Proceso de Scraping

### ¿Qué es Scraping?

Scraping es **extraer datos de fuentes externas**. En nuestro caso, de Google Places API.

### Flujo del Scraping

```
1. INICIO
   ↓
2. Para cada CATEGORÍA (comida, turismo, etc.)
   ↓
3. Para cada TIPO dentro de la categoría (restaurant, cafe, etc.)
   ↓
4. Llamar a Google Places API
   ↓
5. Recibir lista de lugares
   ↓
6. Para cada LUGAR:
   ├─ ¿Ya existe en BD?
   │  ├─ SÍ → Actualizar datos
   │  └─ NO → Crear nuevo
   ↓
7. FIN
```

### Código Simplificado

```python
# 1. Obtener datos de Google
resultados = google_places.buscar_lugares_cercanos('restaurant')

# 2. Procesar cada resultado
for data in resultados:
    # 3. Crear modelo
    lugar = Lugar.from_google_places(data, 'comida')
    
    # 4. Guardar o actualizar
    if repository.existe(lugar.place_id):
        repository.actualizar(lugar)
    else:
        repository.crear(lugar)
```

##  Comunicación Frontend-Backend

### Métodos HTTP

- **GET**: Obtener datos (leer)
- **POST**: Crear datos (escribir)
- **PUT**: Actualizar datos (modificar)
- **DELETE**: Eliminar datos (borrar)

### Ejemplo Práctico

**Frontend hace una petición:**
```javascript
// GET /api/lugares?categoria=comida
const response = await fetch('http://localhost:5000/api/lugares?categoria=comida');
const data = await response.json();
console.log(data);
```

**Backend responde:**
```json
{
  "total": 45,
  "categoria": "comida",
  "lugares": [
    {
      "id": 1,
      "nombre": "Tierra Colorada",
      "categoria": "comida",
      "rating": 4.5
    },
    ...
  ]
}
```

### CORS (Cross-Origin Resource Sharing)

CORS es un mecanismo de seguridad del navegador.

**Problema**: Frontend (localhost:8000) quiere acceder a Backend (localhost:5000)
**Solución**: Configurar CORS en el backend

```python
# backend/api/app.py
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:8000"],  # Frontend permitido
        "methods": ["GET", "POST"]
    }
})
```

## 🗄️ Base de Datos

### SQLite

SQLite es una base de datos **simple y ligera**:
- No requiere servidor separado
- Los datos se guardan en un archivo `.db`
- Perfecto para desarrollo y aplicaciones pequeñas

### Modelo de Datos

Tabla `lugares`:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | INTEGER | ID único (autoincremental) |
| place_id | TEXT | ID de Google Places |
| nombre | TEXT | Nombre del lugar |
| direccion | TEXT | Dirección |
| lat | REAL | Latitud |
| lng | REAL | Longitud |
| categoria | TEXT | comida, turismo, etc. |
| rating | REAL | Calificación (0-5) |

### Consultas SQL Básicas

```sql
-- Obtener todos los lugares
SELECT * FROM lugares;

-- Filtrar por categoría
SELECT * FROM lugares WHERE categoria = 'comida';

-- Ordenar por rating
SELECT * FROM lugares ORDER BY rating DESC;

-- Contar lugares por categoría
SELECT categoria, COUNT(*) FROM lugares GROUP BY categoria;
```

##  Módulos y Clases

### ¿Qué es un Módulo?

Un módulo es un **archivo de código** que agrupa funcionalidades relacionadas.

**Ejemplo:**
- `google_places.py` → Todo lo relacionado con Google Places API
- `lugar_repository.py` → Todo lo relacionado con acceso a datos de lugares

### ¿Qué es una Clase?

Una clase es un **plano** para crear objetos con propiedades y métodos.

**Ejemplo:**

```python
class Lugar:
    def __init__(self, nombre, lat, lng):
        self.nombre = nombre
        self.lat = lat
        self.lng = lng
    
    def to_dict(self):
        return {
            'nombre': self.nombre,
            'lat': self.lat,
            'lng': self.lng
        }

# Usar la clase
lugar = Lugar('Tierra Colorada', -25.2637, -57.5759)
print(lugar.to_dict())  # {'nombre': 'Tierra Colorada', ...}
```

### Ventajas de las Clases

1. **Organización**: Datos y comportamiento juntos
2. **Reutilización**: Crear múltiples instancias
3. **Mantenibilidad**: Cambios en un solo lugar

##  Deployment

### Desarrollo vs Producción

**Desarrollo** (localhost):
- Servidor local en tu computadora
- Debug mode activado
- Base de datos local

**Producción** (internet):
- Servidor en la nube (Render, Railway, etc.)
- Debug mode desactivado
- Base de datos persistente

### Proceso de Deployment

```
1. CÓDIGO LOCAL
   ↓
2. Git Push a GitHub
   ↓
3. Servicio de Hosting (Render) detecta cambios
   ↓
4. Instala dependencias (requirements.txt)
   ↓
5. Ejecuta la aplicación
   ↓
6. Asigna una URL pública
   ↓
7. APLICACIÓN ONLINE ✨
```

## s Herramientas de Desarrollo

### 1. Virtual Environment (venv)

**¿Qué es?** Un "ambiente aislado" para tu proyecto

**¿Por qué?** Evita conflictos entre proyectos

```bash
# Crear venv
python -m venv venv

# Activar
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# Ahora todas las instalaciones van a venv/
pip install flask
```

### 2. Requirements.txt

**¿Qué es?** Lista de todas las dependencias del proyecto

**¿Por qué?** Para que otros puedan instalar lo mismo

```bash
# Generar requirements.txt
pip freeze > requirements.txt

# Instalar desde requirements.txt
pip install -r requirements.txt
```

### 3. Git & GitHub

**Git**: Control de versiones (historial de cambios)
**GitHub**: Almacenamiento en la nube de repositorios Git

```bash
# Comandos básicos
git add .                  # Agregar cambios
git commit -m "mensaje"    # Guardar cambios
git push                   # Subir a GitHub
```

##  Tiempos de Desarrollo (Estimados)

| Tarea | Tiempo | Dificultad |
|-------|--------|------------|
| Setup inicial | 1-2h | Fácil |
| Backend API básico | 3-4h | Media |
| Frontend básico | 4-6h | Media |
| Integración | 2-3h | Media |
| Deployment | 2-4h | Media-Alta |
| Testing | 2-3h | Media |
| **TOTAL** | **14-22h** | - |

## 🎓 Conceptos para Profundizar

Si quieres entender más:

1. **HTTP/REST**: Cómo funciona la web
2. **JSON**: Formato de intercambio de datos
3. **SQL**: Lenguaje de consulta de bases de datos
4. **Python OOP**: Programación orientada a objetos
5. **Git/GitHub**: Control de versiones

## s Preguntas Frecuentes

**Q: ¿Por qué separar frontend y backend?**
A: Para que cada uno pueda escalar y desplegarse independientemente.

**Q: ¿Puedo usar otra base de datos?**
A: Sí, fácilmente migrar a PostgreSQL o MySQL.

**Q: ¿Es escalable este diseño?**
A: Sí, la arquitectura modular permite crecer agregando más servidores, bases de datos, etc.

**Q: ¿Qué pasa si Google Places API cambia?**
A: Solo necesitas modificar `google_places.py`, el resto sigue igual.

---