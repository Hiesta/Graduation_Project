#!/usr/bin/env python3
"""
Демонстрационный скрипт для тестирования API.
Показывает примеры использования всех endpoints.
"""
import requests
import json
from datetime import datetime

# Базовый URL API
BASE_URL = "http://localhost:8000/api"

def test_api():
    """Тестирование всех endpoints API."""
    
    print("Демонстрация API для работы с перевалами")
    print("=" * 50)
    
    # Тестовые данные
    test_data = {
        "beauty_title": "пер. Демонстрационный",
        "title": "Демо перевал",
        "other_titles": "Тестовый",
        "connect": "",
        "add_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": {
            "email": "demo@example.com",
            "fam": "Демо",
            "name": "Пользователь",
            "otc": "Тестович",
            "phone": "+7 999 123 45 67"
        },
        "coords": {
            "latitude": "45.5000",
            "longitude": "7.3000",
            "height": "1500"
        },
        "level": {
            "winter": "2А",
            "summer": "1А",
            "autumn": "1Б",
            "spring": "2А"
        },
        "images": [
            {
                "data": "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==",
                "title": "Демо изображение"
            }
        ]
    }
    
    try:
        # 1. Создание перевала
        print("Создание нового перевала...")
        response = requests.post(f"{BASE_URL}/submitData", json=test_data)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            pereval_id = result.get("id")
            print(f"Перевал создан с ID: {pereval_id}")
            print(f"Ответ: {json.dumps(result, indent=2, ensure_ascii=False)}")
        else:
            print(f"Ошибка создания: {response.text}")
            return
        
        print("\n" + "-" * 30 + "\n")
        
        # 2. Получение перевала по ID
        print("Получение перевала по ID...")
        response = requests.get(f"{BASE_URL}/submitData/{pereval_id}")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Перевал получен:")
            print(f"Название: {result['title']}")
            print(f"Статус: {result['status']}")
            print(f"Пользователь: {result['user']['email']}")
        else:
            print(f"Ошибка получения: {response.text}")
        
        print("\n" + "-" * 30 + "\n")
        
        # 3. Обновление перевала
        print("Обновление перевала...")
        update_data = {
            "beauty_title": "пер. Обновленный демо",
            "title": "Обновленный демо перевал",
            "coords": {
                "latitude": "45.6000",
                "longitude": "7.4000",
                "height": "1600"
            }
        }
        
        response = requests.patch(f"{BASE_URL}/submitData/{pereval_id}", json=update_data)
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Результат обновления:")
            print(f"Состояние: {result['state']}")
            print(f"Сообщение: {result['message']}")
        else:
            print(f"Ошибка обновления: {response.text}")
        
        print("\n" + "-" * 30 + "\n")
        
        # 4. Получение перевалов по email
        print("Получение перевалов по email...")
        response = requests.get(f"{BASE_URL}/submitData/?user__email=demo@example.com")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Найдено перевалов: {len(result)}")
            for i, pereval in enumerate(result, 1):
                print(f"  {i}. {pereval['title']} (ID: {pereval['id']}, статус: {pereval['status']})")
        else:
            print(f"Ошибка получения списка: {response.text}")
        
        print("\n" + "-" * 30 + "\n")
        
        # 5. Тест получения несуществующего перевала
        print("Тест получения несуществующего перевала...")
        response = requests.get(f"{BASE_URL}/submitData/99999")
        print(f"Статус: {response.status_code}")
        
        if response.status_code == 400:
            print("Корректно обработана ошибка 'Перевал не найден'")
        else:
            print(f"Неожиданный ответ: {response.text}")
        
        print("\n" + "=" * 50)
        print("Демонстрация завершена!")
        
    except requests.exceptions.ConnectionError:
        print("Ошибка подключения к API. Убедитесь, что сервер запущен на http://localhost:8000")
    except Exception as e:
        print(f"Неожиданная ошибка: {e}")

if __name__ == "__main__":
    test_api()
