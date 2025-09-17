"""
Unit-тесты для репозитория PerevalRepository.
"""
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.connection import Base
from repository.pereval_repository import PerevalRepository
from models.user import User
from models.coords import Coords
from models.level import Level
from models.image import Image
from models.pereval import Pereval, PerevalStatus
from schemas.user import UserCreate
from schemas.coords import CoordsCreate
from schemas.level import LevelCreate
from schemas.image import ImageCreate
from schemas.pereval import PerevalCreate
from datetime import datetime

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    """Фикстура для создания тестовой сессии базы данных."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def pereval_repo(db_session):
    """Фикстура для создания репозитория."""
    return PerevalRepository(db_session)

@pytest.fixture
def sample_user_data():
    """Фикстура с тестовыми данными пользователя."""
    return UserCreate(
        email="test@example.com",
        fam="Тестов",
        name="Тест",
        otc="Тестович",
        phone="+7 999 999 99 99"
    )

@pytest.fixture
def sample_pereval_data(sample_user_data):
    """Фикстура с тестовыми данными перевала."""
    return PerevalCreate(
        beauty_title="пер. Тестовый",
        title="Тестовый перевал",
        other_titles="Тест",
        connect="",
        add_time=datetime(2021, 9, 22, 13, 18, 13),
        user=sample_user_data,
        coords=CoordsCreate(
            latitude="45.3842",
            longitude="7.1525",
            height="1200"
        ),
        level=LevelCreate(
            winter="",
            summer="1А",
            autumn="1А",
            spring=""
        ),
        images=[
            ImageCreate(
                data="iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                title="Тестовое изображение"
            )
        ]
    )

def test_create_pereval(pereval_repo, sample_pereval_data):
    """Тест создания перевала."""
    pereval_id = pereval_repo.create_pereval(sample_pereval_data)
    assert pereval_id is not None
    assert isinstance(pereval_id, int)

def test_get_pereval_by_id(pereval_repo, sample_pereval_data):
    """Тест получения перевала по ID."""
    # Создаем перевал
    pereval_id = pereval_repo.create_pereval(sample_pereval_data)
    
    # Получаем перевал по ID
    pereval = pereval_repo.get_pereval_by_id(pereval_id)
    
    assert pereval is not None
    assert pereval.id == pereval_id
    assert pereval.beauty_title == sample_pereval_data.beauty_title
    assert pereval.title == sample_pereval_data.title

def test_get_pereval_by_id_not_found(pereval_repo):
    """Тест получения несуществующего перевала."""
    pereval = pereval_repo.get_pereval_by_id(999)
    assert pereval is None

def test_update_pereval_success(pereval_repo, sample_pereval_data):
    """Тест успешного обновления перевала в статусе 'new'."""
    # Создаем перевал
    pereval_id = pereval_repo.create_pereval(sample_pereval_data)
    
    # Обновляем перевал
    update_data = {
        "beauty_title": "Обновленное название",
        "title": "Обновленный перевал"
    }
    
    success = pereval_repo.update_pereval(pereval_id, update_data)
    assert success is True
    
    # Проверяем, что данные обновились
    updated_pereval = pereval_repo.get_pereval_by_id(pereval_id)
    assert updated_pereval.beauty_title == "Обновленное название"
    assert updated_pereval.title == "Обновленный перевал"

def test_update_pereval_wrong_status(pereval_repo, sample_pereval_data, db_session):
    """Тест обновления перевала с неподходящим статусом."""
    # Создаем перевал
    pereval_id = pereval_repo.create_pereval(sample_pereval_data)
    
    # Меняем статус на 'pending'
    pereval = db_session.query(Pereval).filter(Pereval.id == pereval_id).first()
    pereval.status = PerevalStatus.PENDING
    db_session.commit()
    
    # Пытаемся обновить
    update_data = {"title": "Новое название"}
    success = pereval_repo.update_pereval(pereval_id, update_data)
    
    assert success is False

def test_update_pereval_not_found(pereval_repo):
    """Тест обновления несуществующего перевала."""
    update_data = {"title": "Новое название"}
    success = pereval_repo.update_pereval(999, update_data)
    assert success is False

def test_list_perevals_by_user_email(pereval_repo, sample_pereval_data):
    """Тест получения списка перевалов по email пользователя."""
    # Создаем перевал
    pereval_id = pereval_repo.create_pereval(sample_pereval_data)
    
    # Получаем список перевалов
    perevals = pereval_repo.list_perevals_by_user_email("test@example.com")
    
    assert len(perevals) == 1
    assert perevals[0].id == pereval_id
    assert perevals[0].beauty_title == sample_pereval_data.beauty_title

def test_list_perevals_by_user_email_empty(pereval_repo):
    """Тест получения списка перевалов для несуществующего пользователя."""
    perevals = pereval_repo.list_perevals_by_user_email("nonexistent@example.com")
    assert len(perevals) == 0

def test_list_perevals_by_user_email_pagination(pereval_repo, sample_pereval_data):
    """Тест пагинации при получении списка перевалов."""
    # Создаем несколько перевалов
    for i in range(5):
        # Создаем новый объект для каждого перевала
        data = PerevalCreate(
            beauty_title=f"пер. Тестовый {i}",
            title=f"Перевал {i}",
            other_titles="Тест",
            connect="",
            add_time=datetime(2021, 9, 22, 13, 18, 13),
            user=sample_pereval_data.user,
            coords=sample_pereval_data.coords,
            level=sample_pereval_data.level,
            images=sample_pereval_data.images
        )
        pereval_repo.create_pereval(data)
    
    # Тестируем пагинацию
    perevals_page1 = pereval_repo.list_perevals_by_user_email("test@example.com", offset=0, limit=2)
    perevals_page2 = pereval_repo.list_perevals_by_user_email("test@example.com", offset=2, limit=2)
    
    assert len(perevals_page1) == 2
    assert len(perevals_page2) == 2
    assert perevals_page1[0].id != perevals_page2[0].id
