# backend/config/database.py
"""
Configuración y gestión de la base de datos.
Proporciona funciones para crear y obtener conexiones a la BD.
"""
import sqlite3
from typing import Optional
from contextlib import contextmanager
from .settings import DATABASE_PATH


class Database:
    """Clase singleton para gestionar la conexión a la base de datos."""
    
    _instance: Optional['Database'] = None
    _connection: Optional[sqlite3.Connection] = None
    
    def __new__(cls):
        """Implementación del patrón Singleton."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        """Inicializa la base de datos si no existe."""
        if self._connection is None:
            self._connection = sqlite3.connect(
                DATABASE_PATH, 
                check_same_thread=False
            )
            self._connection.row_factory = sqlite3.Row  # Para obtener resultados como diccionarios
            self._create_tables()
    
    def _create_tables(self):
        """Crea las tablas necesarias si no existen."""
        cursor = self._connection.cursor()
        
        # Tabla de lugares
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS lugares (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            place_id TEXT UNIQUE NOT NULL,
            nombre TEXT NOT NULL,
            direccion TEXT,
            lat REAL NOT NULL,
            lng REAL NOT NULL,
            categoria TEXT NOT NULL,
            rating REAL DEFAULT 0,
            total_ratings INTEGER DEFAULT 0,
            precio_nivel INTEGER,
            horarios TEXT,
            telefono TEXT,
            sitio_web TEXT,
            foto_referencia TEXT,
            fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            fecha_actualizacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Índices para mejorar performance
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_categoria 
        ON lugares(categoria)
        """)
        
        cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_rating 
        ON lugares(rating DESC)
        """)
        
        self._connection.commit()
    
    def get_connection(self) -> sqlite3.Connection:
        """Retorna la conexión a la base de datos."""
        return self._connection
    
    @contextmanager
    def get_cursor(self):
        """Context manager para obtener un cursor y asegurar commit/rollback."""
        cursor = self._connection.cursor()
        try:
            yield cursor
            self._connection.commit()
        except Exception as e:
            self._connection.rollback()
            raise e
        finally:
            cursor.close()
    
    def close(self):
        """Cierra la conexión a la base de datos."""
        if self._connection:
            self._connection.close()
            self._connection = None


# Función helper para obtener una instancia de la base de datos
def get_db() -> Database:
    """Retorna la instancia singleton de la base de datos."""
    return Database()
