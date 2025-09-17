"""
Pydantic схемы для перевала.
"""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from .user import UserCreate, UserResponse
from .coords import CoordsCreate, CoordsResponse
from .level import LevelCreate, LevelResponse
from .image import ImageCreate, ImageResponse


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


class PerevalUpdate(BaseModel):
    """Схема для обновления перевала."""
    beauty_title: Optional[str] = None
    title: Optional[str] = None
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: Optional[datetime] = None
    coords: Optional[CoordsCreate] = None
    level: Optional[LevelCreate] = None
    images: Optional[List[ImageCreate]] = None

class PerevalDetailResponse(BaseModel):
    """Схема для детального ответа с полной информацией о перевале."""
    id: int
    beauty_title: str
    title: str
    other_titles: Optional[str] = None
    connect: Optional[str] = None
    add_time: datetime
    status: str
    user: UserResponse
    coords: CoordsResponse
    level: LevelResponse
    images: List[ImageResponse]
    
    class Config:
        from_attributes = True

class SubmitDataResponse(BaseModel):
    """Схема ответа API для submitData."""
    status: int
    message: Optional[str] = None
    id: Optional[int] = None

class UpdateResponse(BaseModel):
    """Схема ответа для обновления."""
    state: int
    message: Optional[str] = None
