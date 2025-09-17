"""
Pydantic схемы для изображения.
"""
from pydantic import BaseModel
from typing import Optional


class ImageBase(BaseModel):
    """Базовая схема изображения."""
    data: str  # Base64 данные
    title: str


class ImageCreate(ImageBase):
    """Схема для создания изображения."""
    pass


class ImageResponse(ImageBase):
    """Схема для ответа с данными изображения."""
    id: int
    pereval_id: int

    class Config:
        from_attributes = True
