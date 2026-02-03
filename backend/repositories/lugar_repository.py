# backend/repositories/lugar_repository.py
"""
Repositorio para acceso a datos de lugares en la base de datos.
Implementa el patrón Repository para abstraer el acceso a datos.
"""
from typing import List, Optional, Dict, Any
from ..models.lugar import Lugar
from ..config.database import get_db


class LugarRepository:
    """Repositorio para operaciones CRUD de lugares."""
    
    def __init__(self):
        """Inicializa el repositorio con la conexión a la base de datos."""
        self.db = get_db()
    
    def crear(self, lugar: Lugar) -> Optional[int]:
        """
        Crea un nuevo lugar en la base de datos.
        
        Args:
            lugar: Instancia de Lugar a guardar
            
        Returns:
            ID del lugar creado o None si ya existe
        """
        with self.db.get_cursor() as cursor:
            try:
                cursor.execute("""
                INSERT INTO lugares 
                (place_id, nombre, direccion, lat, lng, categoria, rating, 
                 total_ratings, precio_nivel, foto_referencia)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    lugar.place_id,
                    lugar.nombre,
                    lugar.direccion,
                    lugar.lat,
                    lugar.lng,
                    lugar.categoria,
                    lugar.rating,
                    lugar.total_ratings,
                    lugar.precio_nivel,
                    lugar.foto_referencia
                ))
                return cursor.lastrowid
            except Exception as e:
                print(f"Error al crear lugar {lugar.nombre}: {e}")
                return None
    
    def actualizar(self, lugar: Lugar) -> bool:
        """
        Actualiza un lugar existente.
        
        Args:
            lugar: Instancia de Lugar con datos actualizados
            
        Returns:
            True si se actualizó correctamente, False en caso contrario
        """
        with self.db.get_cursor() as cursor:
            try:
                cursor.execute("""
                UPDATE lugares SET
                    nombre = ?,
                    direccion = ?,
                    lat = ?,
                    lng = ?,
                    categoria = ?,
                    rating = ?,
                    total_ratings = ?,
                    precio_nivel = ?,
                    foto_referencia = ?,
                    fecha_actualizacion = CURRENT_TIMESTAMP
                WHERE place_id = ?
                """, (
                    lugar.nombre,
                    lugar.direccion,
                    lugar.lat,
                    lugar.lng,
                    lugar.categoria,
                    lugar.rating,
                    lugar.total_ratings,
                    lugar.precio_nivel,
                    lugar.foto_referencia,
                    lugar.place_id
                ))
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error al actualizar lugar {lugar.place_id}: {e}")
                return False
    
    def obtener_por_id(self, lugar_id: int) -> Optional[Lugar]:
        """
        Obtiene un lugar por su ID interno.
        
        Args:
            lugar_id: ID del lugar
            
        Returns:
            Instancia de Lugar o None si no existe
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM lugares WHERE id = ?", (lugar_id,))
            row = cursor.fetchone()
            
            if row:
                return Lugar.from_db_row(row)
            return None
    
    def obtener_por_place_id(self, place_id: str) -> Optional[Lugar]:
        """
        Obtiene un lugar por su place_id de Google.
        
        Args:
            place_id: Place ID de Google Places
            
        Returns:
            Instancia de Lugar o None si no existe
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("SELECT * FROM lugares WHERE place_id = ?", (place_id,))
            row = cursor.fetchone()
            
            if row:
                return Lugar.from_db_row(row)
            return None
    
    def obtener_todos(
        self, 
        categoria: Optional[str] = None,
        limite: int = 100,
        orden: str = "rating DESC"
    ) -> List[Lugar]:
        """
        Obtiene todos los lugares, opcionalmente filtrados por categoría.
        
        Args:
            categoria: Filtrar por categoría (opcional)
            limite: Número máximo de resultados
            orden: Orden de los resultados (ej: "rating DESC", "nombre ASC")
            
        Returns:
            Lista de lugares
        """
        with self.db.get_cursor() as cursor:
            if categoria:
                query = f"""
                SELECT * FROM lugares 
                WHERE categoria = ? 
                ORDER BY {orden}
                LIMIT ?
                """
                cursor.execute(query, (categoria, limite))
            else:
                query = f"""
                SELECT * FROM lugares 
                ORDER BY {orden}
                LIMIT ?
                """
                cursor.execute(query, (limite,))
            
            rows = cursor.fetchall()
            return [Lugar.from_db_row(row) for row in rows]
    
    def existe(self, place_id: str) -> bool:
        """
        Verifica si un lugar ya existe en la base de datos.
        
        Args:
            place_id: Place ID de Google Places
            
        Returns:
            True si existe, False en caso contrario
        """
        with self.db.get_cursor() as cursor:
            cursor.execute(
                "SELECT 1 FROM lugares WHERE place_id = ? LIMIT 1", 
                (place_id,)
            )
            return cursor.fetchone() is not None
    
    def contar_por_categoria(self) -> Dict[str, int]:
        """
        Cuenta la cantidad de lugares por categoría.
        
        Returns:
            Diccionario con categoría como clave y cantidad como valor
        """
        with self.db.get_cursor() as cursor:
            cursor.execute("""
            SELECT categoria, COUNT(*) as total
            FROM lugares
            GROUP BY categoria
            """)
            
            resultado = {}
            for row in cursor.fetchall():
                resultado[row['categoria']] = row['total']
            
            return resultado
    
    def eliminar(self, lugar_id: int) -> bool:
        """
        Elimina un lugar de la base de datos.
        
        Args:
            lugar_id: ID del lugar a eliminar
            
        Returns:
            True si se eliminó correctamente, False en caso contrario
        """
        with self.db.get_cursor() as cursor:
            try:
                cursor.execute("DELETE FROM lugares WHERE id = ?", (lugar_id,))
                return cursor.rowcount > 0
            except Exception as e:
                print(f"Error al eliminar lugar {lugar_id}: {e}")
                return False
