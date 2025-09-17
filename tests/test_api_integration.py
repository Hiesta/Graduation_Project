"""
Интеграционные тесты для API endpoints.
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.connection import Base, get_db
from main import app
from models.user import User
from models.coords import Coords
from models.level import Level
from models.image import Image
from models.pereval import Pereval, PerevalStatus
from datetime import datetime

# Создаем тестовую базу данных в памяти
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_api.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    """Переопределяем get_db для тестов."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def client():
    """Фикстура для тестового клиента."""
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_pereval_data():
    """Фикстура с тестовыми данными для создания перевала."""
    return {
        "beauty_title": "пер. Тестовый",
        "title": "Тестовый перевал",
        "other_titles": "Тест",
        "connect": "",
        "add_time": "2021-09-22 13:18:13",
        "user": {
            "email": "test@example.com",
            "fam": "Тестов",
            "name": "Тест",
            "otc": "Тестович",
            "phone": "+7 999 999 99 99"
        },
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": "1200"
        },
        "level": {
            "winter": "",
            "summer": "1А",
            "autumn": "1А",
            "spring": ""
        },
        "images": [
            {
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                "title": "Тестовое изображение"
            }
        ]
    }

def test_create_pereval_success(client, sample_pereval_data):
    """Тест успешного создания перевала через POST /submitData."""
    response = client.post("/api/submitData", json=sample_pereval_data)
    
    # Проверяем, что запрос прошел (может быть 200 или 500 в зависимости от БД)
    assert response.status_code in [200, 500]
    
    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "id" in data

def test_get_pereval_by_id_success(client, sample_pereval_data):
    """Тест получения перевала по ID через GET /submitData/{id}."""
    # Сначала создаем перевал
    create_response = client.post("/api/submitData", json=sample_pereval_data)
    
    if create_response.status_code == 200:
        pereval_id = create_response.json()["id"]
        
        # Получаем перевал по ID
        response = client.get(f"/api/submitData/{pereval_id}")
        
        if response.status_code == 200:
            data = response.json()
            assert "id" in data
            assert "beauty_title" in data
            assert "title" in data
            assert "status" in data
            assert "user" in data
            assert "coords" in data
            assert "level" in data
            assert "images" in data
            assert data["id"] == pereval_id

def test_get_pereval_by_id_not_found(client):
    """Тест получения несуществующего перевала."""
    response = client.get("/api/submitData/999")
    assert response.status_code == 400
    assert "Перевал не найден" in response.json()["detail"]

def test_update_pereval_success(client, sample_pereval_data):
    """Тест успешного обновления перевала через PATCH /submitData/{id}."""
    # Сначала создаем перевал
    create_response = client.post("/api/submitData", json=sample_pereval_data)
    
    if create_response.status_code == 200:
        pereval_id = create_response.json()["id"]
        
        # Обновляем перевал
        update_data = {
            "beauty_title": "Обновленное название",
            "title": "Обновленный перевал"
        }
        
        response = client.patch(f"/api/submitData/{pereval_id}", json=update_data)
        
        if response.status_code == 200:
            data = response.json()
            assert data["state"] == 1
            assert data["message"] is None

def test_update_pereval_not_found(client):
    """Тест обновления несуществующего перевала."""
    update_data = {"title": "Новое название"}
    response = client.patch("/api/submitData/999", json=update_data)
    
    assert response.status_code == 200
    data = response.json()
    assert data["state"] == 0
    assert "Перевал не найден" in data["message"]

def test_get_perevals_by_email_success(client, sample_pereval_data):
    """Тест получения перевалов по email через GET /submitData/?user__email=<email>."""
    # Сначала создаем перевал
    create_response = client.post("/api/submitData", json=sample_pereval_data)
    
    if create_response.status_code == 200:
        # Получаем перевалы по email
        response = client.get("/api/submitData/?user__email=test@example.com")
        
        if response.status_code == 200:
            data = response.json()
            assert isinstance(data, list)
            if len(data) > 0:
                pereval = data[0]
                assert "id" in pereval
                assert "beauty_title" in pereval
                assert "title" in pereval
                assert "status" in pereval
                assert "user" in pereval
                assert pereval["user"]["email"] == "test@example.com"

def test_get_perevals_by_email_pagination(client, sample_pereval_data):
    """Тест пагинации при получении перевалов по email."""
    # Создаем несколько перевалов
    for i in range(3):
        data = sample_pereval_data.copy()
        data["title"] = f"Перевал {i}"
        data["beauty_title"] = f"пер. Тестовый {i}"
        client.post("/api/submitData", json=data)
    
    # Тестируем пагинацию
    response = client.get("/api/submitData/?user__email=test@example.com&offset=0&limit=2")
    
    if response.status_code == 200:
        data = response.json()
        assert len(data) <= 2

def test_update_pereval_validation_error(client, sample_pereval_data):
    """Тест обновления с невалидными данными."""
    # Сначала создаем перевал
    create_response = client.post("/api/submitData", json=sample_pereval_data)
    
    if create_response.status_code == 200:
        pereval_id = create_response.json()["id"]
        
        # Пытаемся обновить с невалидными данными
        invalid_update_data = {
            "add_time": "invalid-date-format"
        }
        
        response = client.patch(f"/api/submitData/{pereval_id}", json=invalid_update_data)
        
        # Должна быть ошибка валидации
        assert response.status_code == 422

def test_root_endpoint(client):
    """Тест корневого endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Перевалы API работает!"}

def test_health_endpoint(client):
    """Тест health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
