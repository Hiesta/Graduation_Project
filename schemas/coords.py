"""
Pydantic схемы для координат.
"""
from pydantic import BaseModel


class CoordsBase(BaseModel):
    """Базовая схема координат."""
    latitude: str
    longitude: str
    height: str


class CoordsCreate(CoordsBase):
    """Схема для создания координат."""
    pass


class CoordsResponse(CoordsBase):
    """Схема для ответа с данными координат."""
    id: int

    class Config:
        from_attributes = True
