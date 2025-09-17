"""
Pydantic схемы для пользователя.
"""
from pydantic import BaseModel, EmailStr
from typing import Optional


class UserBase(BaseModel):
    """Базовая схема пользователя."""
    email: EmailStr
    fam: str
    name: str
    otc: Optional[str] = None
    phone: str


class UserCreate(UserBase):
    """Схема для создания пользователя."""
    pass


class UserResponse(UserBase):
    """Схема для ответа с данными пользователя."""
    id: int

    class Config:
        from_attributes = True
