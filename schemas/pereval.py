"""
Pydantic схемы для перевала.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .user import UserCreate
from .coords import CoordsCreate
from .level import LevelCreate
from .image import ImageCreate


class PerevalBase(BaseModel):
    """Базовая схема перевала."""
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime


class PerevalCreate(PerevalBase):
    """Схема для создания перевала."""
    user: UserCreate
    coords: CoordsCreate
    level: LevelCreate
    images: List[ImageCreate]


class PerevalResponse(PerevalBase):
    """Схема для ответа с данными перевала."""
    id: int
    user_id: int
    coords_id: int
    level_id: int
    status: str

    class Config:
        from_attributes = True


class SubmitDataResponse(BaseModel):
    """Схема ответа API для submitData."""
    status: int
    message: Optional[str] = None
    id: Optional[int] = None
