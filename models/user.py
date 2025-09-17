"""
Модель пользователя для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String
from database.connection import Base

class User(Base):
    """Модель пользователя в базе данных."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    fam = Column(String, nullable=False)  # Фамилия
    name = Column(String, nullable=False)  # Имя
    otc = Column(String, nullable=True)   # Отчество
    phone = Column(String, nullable=False)  # Телефон
