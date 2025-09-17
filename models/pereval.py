"""
Модель перевала для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from database.connection import Base
import enum


class PerevalStatus(enum.Enum):
    """Статусы обработки заявки на перевал."""
    NEW = "new"
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class Pereval(Base):
    """Информация о перевале - основная сущность."""

    __tablename__ = "pereval"

    id = Column(Integer, primary_key=True, index=True)
    beauty_title = Column(String, nullable=False)  # Красивое название перевала
    title = Column(String, nullable=False)  # Основное название
    other_titles = Column(String, nullable=True)  # Другие известные названия
    connect = Column(String, nullable=True)  # Соединение с другими перевалами
    add_time = Column(DateTime, nullable=False)  # Когда была добавлена заявка
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Кто добавил
    coords_id = Column(Integer, ForeignKey("coords.id"), nullable=False)  # Где находится
    level_id = Column(Integer, ForeignKey("levels.id"), nullable=False)  # Уровень сложности
    status = Column(Enum(PerevalStatus), default=PerevalStatus.NEW, nullable=False)  # Статус обработки
