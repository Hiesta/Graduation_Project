"""
Pydantic схемы для уровня сложности.
"""
from pydantic import BaseModel
from typing import Optional


class LevelBase(BaseModel):
    """Базовая схема уровня сложности."""
    winter: Optional[str] = None
    summer: Optional[str] = None
    autumn: Optional[str] = None
    spring: Optional[str] = None


class LevelCreate(LevelBase):
    """Схема для создания уровня сложности."""
    pass


class LevelResponse(LevelBase):
    """Схема для ответа с данными уровня сложности."""
    id: int

    class Config:
        from_attributes = True
