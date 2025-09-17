"""
Модель изображения для SQLAlchemy.
"""
from sqlalchemy import Column, Integer, String, ForeignKey, Text
from database.connection import Base


class Image(Base):
    """Фотографии перевала в формате base64."""

    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(Text, nullable=False)  # Само изображение в base64
    title = Column(String, nullable=False)  # Название фотографии
    pereval_id = Column(Integer, ForeignKey("pereval.id"), nullable=False)  # К какому перевалу относится
