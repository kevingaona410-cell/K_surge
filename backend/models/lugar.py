# backend/models/lugar.py
"""
Modelo de datos para representar un lugar.
Define la estructura y validaciones de un lugar.
"""
from dataclasses import dataclass, asdict
from typing import Optional, Dict, Any
from datetime import datetime


@dataclass
class Lugar:
    """
    Representa un lugar (restaurante, museo, parque, etc.).
    
    Attributes:
        place_id: ID único de Google Places
        nombre: Nombre del lugar
        direccion: Dirección física
        lat: Latitud
        lng: Longitud
        categoria: Categoría del lugar (comida, turismo, cultura, recreacion)
        rating: Calificación promedio (0-5)
        total_ratings: Número total de reseñas
        precio_nivel: Nivel de precio (1-4, siendo 4 el más caro)
        horarios: Horarios de atención en formato JSON
        telefono: Número de teléfono
        sitio_web: URL del sitio web
        foto_referencia: Referencia de foto de Google Places
        id: ID interno de la base de datos (opcional)
        fecha_creacion: Timestamp de creación
        fecha_actualizacion: Timestamp de última actualización
    """
    
    place_id: str
    nombre: str
    lat: float
    lng: float
    categoria: str
    direccion: Optional[str] = None
    rating: float = 0.0
    total_ratings: int = 0
    precio_nivel: Optional[int] = None
    horarios: Optional[str] = None
    telefono: Optional[str] = None
    sitio_web: Optional[str] = None
    foto_referencia: Optional[str] = None
    id: Optional[int] = None
    fecha_creacion: Optional[datetime] = None
    fecha_actualizacion: Optional[datetime] = None
    
    @classmethod
    def from_google_places(cls, data: Dict[str, Any], categoria: str) -> 'Lugar':
        """
        Crea una instancia de Lugar desde los datos de Google Places API.
        
        Args:
            data: Diccionario con datos de la API de Google Places
            categoria: Categoría asignada al lugar
            
        Returns:
            Instancia de Lugar
        """
        # Extraer foto si existe
        foto_ref = None
        if "photos" in data and len(data["photos"]) > 0:
            foto_ref = data["photos"][0].get("photo_reference")
        
        return cls(
            place_id=data["place_id"],
            nombre=data["name"],
            direccion=data.get("vicinity", ""),
            lat=data["geometry"]["location"]["lat"],
            lng=data["geometry"]["location"]["lng"],
            categoria=categoria,
            rating=data.get("rating", 0.0),
            total_ratings=data.get("user_ratings_total", 0),
            precio_nivel=data.get("price_level"),
            foto_referencia=foto_ref
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el lugar a un diccionario.
        Útil para serializar a JSON.
        
        Returns:
            Diccionario con los datos del lugar
        """
        data = asdict(self)
        
        # Convertir datetime a string si existe
        if self.fecha_creacion:
            data['fecha_creacion'] = self.fecha_creacion.isoformat()
        if self.fecha_actualizacion:
            data['fecha_actualizacion'] = self.fecha_actualizacion.isoformat()
            
        return data
    
    @staticmethod
    def from_db_row(row) -> 'Lugar':
        """
        Crea una instancia de Lugar desde una fila de la base de datos.
        
        Args:
            row: Fila de SQLite (sqlite3.Row)
            
        Returns:
            Instancia de Lugar
        """
        return Lugar(
            id=row['id'],
            place_id=row['place_id'],
            nombre=row['nombre'],
            direccion=row['direccion'],
            lat=row['lat'],
            lng=row['lng'],
            categoria=row['categoria'],
            rating=row['rating'],
            total_ratings=row.get('total_ratings', 0),
            precio_nivel=row.get('precio_nivel'),
            horarios=row.get('horarios'),
            telefono=row.get('telefono'),
            sitio_web=row.get('sitio_web'),
            foto_referencia=row.get('foto_referencia'),
            fecha_creacion=row.get('fecha_creacion'),
            fecha_actualizacion=row.get('fecha_actualizacion')
        )
    
    def __repr__(self) -> str:
        """Representación en string del lugar."""
        return f"Lugar(id={self.id}, nombre='{self.nombre}', categoria='{self.categoria}')"
