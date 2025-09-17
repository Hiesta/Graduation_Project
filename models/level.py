"""
Модель уровня сложности для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String
from database.connection import Base


class Level(Base):
    """Уровни сложности прохождения перевала по сезонам."""

    __tablename__ = "levels"

    id = Column(Integer, primary_key=True, index=True)
    winter = Column(String, nullable=True)  # Зимний уровень
    summer = Column(String, nullable=True)  # Летний уровень
    autumn = Column(String, nullable=True)  # Осенний уровень
    spring = Column(String, nullable=True)  # Весенний уровень
