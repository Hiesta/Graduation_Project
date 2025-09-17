"""
Модель координат для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String
from database.connection import Base

class Coords(Base):
    """Модель координат в базе данных."""
    
    __tablename__ = "coords"
    
    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, nullable=False)  # Широта
    longitude = Column(String, nullable=False)  # Долгота
    height = Column(String, nullable=False)    # Высота
