"""
Настройка подключения к PostgreSQL базе данных.
"""
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Получаем параметры подключения к базе данных
DB_HOST = os.getenv("FSTR_DB_HOST", "localhost")
DB_PORT = os.getenv("FSTR_DB_PORT", "5432")
DB_LOGIN = os.getenv("FSTR_DB_LOGIN", "postgres")
DB_PASS = os.getenv("FSTR_DB_PASS", "password")
DB_NAME = os.getenv("FSTR_DB_NAME", "pereval_db")

# Создание URL для подключения к PostgreSQL
DATABASE_URL = f"postgresql://{DB_LOGIN}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Создание движка SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Создаем фабрику сессий для работы с базой данных
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовый класс для моделей
Base = declarative_base()

def get_db():
    """
    Генератор для получения сессии базы данных.
    Используется как dependency в FastAPI.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
