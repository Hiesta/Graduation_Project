"""
Модель координат для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String
from database.connection import Base

class Coords(Base):
    """Координаты перевала на карте."""

    __tablename__ = "coords"

    id = Column(Integer, primary_key=True, index=True)
    latitude = Column(String, nullable=False)  # Широта перевала
    longitude = Column(String, nullable=False)  # Долгота перевала
    height = Column(String, nullable=False)    # Высота над уровнем моря
