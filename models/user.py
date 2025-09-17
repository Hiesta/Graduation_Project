"""
Модель пользователя для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String
from database.connection import Base

class User(Base):
    """Информация о пользователе, который добавляет перевалы."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    fam = Column(String, nullable=False)  # Фамилия пользователя
    name = Column(String, nullable=False)  # Имя пользователя
    otc = Column(String, nullable=True)   # Отчество (может быть пустым)
    phone = Column(String, nullable=False)  # Номер телефона
