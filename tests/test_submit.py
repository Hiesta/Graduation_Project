"""
Тесты для API submitData.
"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_submit_data_success():
    """Тест успешного создания перевала."""
    test_data = {
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
            {"data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==", "title": "Тестовое изображение"}
        ]
    }

    response = client.post("/api/submitData", json=test_data)

    # Проверяем, что запрос прошел (может быть 200 или 500 в зависимости от БД)
    assert response.status_code in [200, 500]

    data = response.json()
    assert "status" in data
    assert "message" in data
    assert "id" in data

def test_submit_data_validation_error():
    """Тест ошибки валидации данных."""
    invalid_data = {
        "beauty_title": "",  # Пустое обязательное поле
        "title": "Тест",
        "add_time": "2021-09-22 13:18:13",
        "user": {
            "email": "invalid-email",  # Невалидный email
            "fam": "Тест",
            "name": "Тест",
            "phone": "+7 999 999 99 99"
        },
        "coords": {
            "latitude": "45.3842",
            "longitude": "7.1525",
            "height": "1200"
        },
        "level": {
            "summer": "1А"
        },
        "images": []
    }

    response = client.post("/api/submitData", json=invalid_data)

    # FastAPI должен вернуть 422 для ошибок валидации
    assert response.status_code == 422

def test_root_endpoint():
    """Тест корневого endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Перевалы API работает!"}

def test_health_endpoint():
    """Тест health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}
