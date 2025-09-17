# Перевалы API

Backend REST API для работы с данными о перевалах, построенный на FastAPI и PostgreSQL.

## Описание

API предоставляет единственный endpoint `POST /submitData` для создания новых записей о перевалах с полной информацией о пользователе, координатах, уровне сложности и изображениях.

## Структура проекта

```
├── main.py                 # Главный файл приложения
├── requirements.txt        # Python зависимости
├── Dockerfile             # Docker образ приложения
├── docker-compose.yml     # Docker Compose конфигурация
├── alembic.ini           # Конфигурация Alembic
├── database/             # Настройки базы данных
│   ├── connection.py     # Подключение к PostgreSQL
│   └── migrations/       # Миграции Alembic
├── models/               # SQLAlchemy модели
│   ├── user.py          # Модель пользователя
│   ├── coords.py        # Модель координат
│   ├── level.py         # Модель уровня сложности
│   ├── image.py         # Модель изображения
│   └── pereval.py       # Модель перевала
├── schemas/              # Pydantic схемы
│   ├── user.py          # Схемы пользователя
│   ├── coords.py        # Схемы координат
│   ├── level.py         # Схемы уровня сложности
│   ├── image.py         # Схемы изображения
│   └── pereval.py       # Схемы перевала
├── repository/           # Репозиторий для работы с БД
│   └── pereval_repository.py
└── routers/              # API роутеры
    └── submit_data.py    # Роутер для submitData
```

## Установка и запуск

### Локальная установка

1. **Клонируйте репозиторий:**
   ```bash
   git clone <repository-url>
   cd GraduationWork
   ```

2. **Создайте виртуальное окружение:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # или
   venv\Scripts\activate     # Windows
   ```

3. **Установите зависимости:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Настройте переменные окружения:**
   Создайте файл `.env` в корне проекта:
   ```env
   FSTR_DB_HOST=localhost
   FSTR_DB_PORT=5432
   FSTR_DB_LOGIN=postgres
   FSTR_DB_PASS=password
   FSTR_DB_NAME=pereval_db
   ```

5. **Запустите PostgreSQL:**
   Убедитесь, что PostgreSQL запущен и доступен по указанным параметрам.

6. **Запустите приложение:**
   ```bash
   uvicorn main:app --reload
   ```

### Запуск с Docker

1. **Запустите все сервисы:**
   ```bash
   docker-compose up --build
   ```

2. **Приложение будет доступно по адресу:**
   - API: http://localhost:8000
   - Swagger UI: http://localhost:8000/docs
   - PostgreSQL: localhost:5432

## API Документация

### POST /api/submitData

Создает новую запись о перевале.

**Запрос:**
```json
{
  "beauty_title": "пер. ",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22 13:18:13",
  "user": {
    "email": "qwerty@mail.ru",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
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
    {"data": "<base64_encoded_image>", "title": "Седловина"},
    {"data": "<base64_encoded_image>", "title": "Подъём"}
  ]
}
```

**Ответ:**
```json
{
  "status": 200,
  "message": null,
  "id": 42
}
```

**Коды ответов:**
- `200` - Успешное создание записи
- `400` - Ошибка валидации данных
- `500` - Ошибка сервера или базы данных

### GET /api/submitData/{id}

Получает перевал по его ID.

**Запрос:**
```bash
curl -X GET "http://localhost:8000/api/submitData/42"
```

**Ответ:**
```json
{
  "id": 42,
  "beauty_title": "пер. Пхия",
  "title": "Пхия",
  "other_titles": "Триев",
  "connect": "",
  "add_time": "2021-09-22T13:18:13",
  "status": "new",
  "user": {
    "id": 1,
    "email": "qwerty@mail.ru",
    "fam": "Пупкин",
    "name": "Василий",
    "otc": "Иванович",
    "phone": "+7 555 55 55"
  },
  "coords": {
    "id": 1,
    "latitude": "45.3842",
    "longitude": "7.1525",
    "height": "1200"
  },
  "level": {
    "id": 1,
    "winter": "",
    "summer": "1А",
    "autumn": "1А",
    "spring": ""
  },
  "images": [
    {
      "id": 1,
      "data": "<base64_encoded_image>",
      "title": "Седловина",
      "pereval_id": 42
    }
  ]
}
```

**Коды ответов:**
- `200` - Успешное получение записи
- `400` - Перевал не найден
- `500` - Ошибка сервера

### PATCH /api/submitData/{id}

Обновляет существующий перевал (только если статус = 'new').

**Запрос:**
```bash
curl -X PATCH "http://localhost:8000/api/submitData/42" \
     -H "Content-Type: application/json" \
     -d '{
       "beauty_title": "Обновленное название",
       "title": "Обновленный перевал",
       "coords": {
         "latitude": "45.5000",
         "longitude": "7.2000",
         "height": "1300"
       }
     }'
```

**Ответ (успех):**
```json
{
  "state": 1,
  "message": null
}
```

**Ответ (ошибка - статус не 'new'):**
```json
{
  "state": 0,
  "message": "Редактирование запрещено: статус не 'new'"
}
```

**Ответ (перевал не найден):**
```json
{
  "state": 0,
  "message": "Перевал не найден"
}
```

**Ограничения:**
- Можно изменять только перевалы со статусом 'new'
- Запрещено изменять ФИО, email и телефон пользователя
- Разрешено изменять: beauty_title, title, other_titles, connect, add_time, coords, level, images

### GET /api/submitData/?user__email=<email>

Получает список всех перевалов пользователя по email.

**Запрос:**
```bash
curl -X GET "http://localhost:8000/api/submitData/?user__email=qwerty@mail.ru"
```

**Запрос с пагинацией:**
```bash
curl -X GET "http://localhost:8000/api/submitData/?user__email=qwerty@mail.ru&offset=0&limit=10"
```

**Ответ:**
```json
[
  {
    "id": 42,
    "beauty_title": "пер. Пхия",
    "title": "Пхия",
    "other_titles": "Триев",
    "connect": "",
    "add_time": "2021-09-22T13:18:13",
    "status": "new",
    "user": {
      "id": 1,
      "email": "qwerty@mail.ru",
      "fam": "Пупкин",
      "name": "Василий",
      "otc": "Иванович",
      "phone": "+7 555 55 55"
    },
    "coords": {
      "id": 1,
      "latitude": "45.3842",
      "longitude": "7.1525",
      "height": "1200"
    },
    "level": {
      "id": 1,
      "winter": "",
      "summer": "1А",
      "autumn": "1А",
      "spring": ""
    },
    "images": [
      {
        "id": 1,
        "data": "<base64_encoded_image>",
        "title": "Седловина",
        "pereval_id": 42
      }
    ]
  }
]
```

**Параметры запроса:**
- `user__email` (обязательный) - Email пользователя
- `offset` (опциональный, по умолчанию 0) - Смещение для пагинации
- `limit` (опциональный) - Лимит записей для пагинации

**Коды ответов:**
- `200` - Успешное получение списка
- `500` - Ошибка сервера

## Структура базы данных

### Таблица `users`
- `id` - Первичный ключ
- `email` - Email пользователя (уникальный)
- `fam` - Фамилия
- `name` - Имя
- `otc` - Отчество (опционально)
- `phone` - Телефон

### Таблица `coords`
- `id` - Первичный ключ
- `latitude` - Широта
- `longitude` - Долгота
- `height` - Высота

### Таблица `levels`
- `id` - Первичный ключ
- `winter` - Зимний уровень сложности
- `summer` - Летний уровень сложности
- `autumn` - Осенний уровень сложности
- `spring` - Весенний уровень сложности

### Таблица `images`
- `id` - Первичный ключ
- `data` - Base64 данные изображения
- `title` - Название изображения
- `pereval_id` - Внешний ключ на перевал

### Таблица `pereval`
- `id` - Первичный ключ
- `beauty_title` - Красивое название
- `title` - Название
- `other_titles` - Другие названия
- `connect` - Соединение
- `add_time` - Время добавления
- `user_id` - Внешний ключ на пользователя
- `coords_id` - Внешний ключ на координаты
- `level_id` - Внешний ключ на уровень
- `status` - Статус (new, pending, accepted, rejected)

## Миграции

Для работы с миграциями Alembic:

```bash
# Создание новой миграции
alembic revision --autogenerate -m "Описание изменений"

# Применение миграций
alembic upgrade head

# Откат миграций
alembic downgrade -1
```

## Тестирование

### Автоматические тесты

Запуск всех тестов:
```bash
pytest tests/
```

Запуск только unit-тестов репозитория:
```bash
pytest tests/test_repository.py
```

Запуск только интеграционных тестов API:
```bash
pytest tests/test_api_integration.py
```

### Ручное тестирование

1. **Swagger UI:** http://localhost:8000/docs
2. **curl примеры:**

   Создание перевала:
   ```bash
   curl -X POST "http://localhost:8000/api/submitData" \
        -H "Content-Type: application/json" \
        -d '{"beauty_title": "Тест", "title": "Тестовый перевал", ...}'
   ```

   Получение перевала по ID:
   ```bash
   curl -X GET "http://localhost:8000/api/submitData/1"
   ```

   Обновление перевала:
   ```bash
   curl -X PATCH "http://localhost:8000/api/submitData/1" \
        -H "Content-Type: application/json" \
        -d '{"title": "Обновленное название"}'
   ```

   Получение перевалов по email:
   ```bash
   curl -X GET "http://localhost:8000/api/submitData/?user__email=test@example.com"
   ```

3. **Демонстрационный скрипт:**
   ```bash
   python demo_api.py
   ```
   Скрипт автоматически протестирует все endpoints API.

## Особенности реализации

- **Валидация данных:** Используются Pydantic схемы для автоматической валидации
- **Обработка ошибок:** Централизованная обработка с детальными сообщениями
- **Транзакции:** Все операции выполняются в транзакциях с откатом при ошибках
- **Логирование:** Подробное логирование всех операций
- **Документация:** Автоматическая генерация OpenAPI/Swagger документации
- **Docker:** Полная контейнеризация с health checks

## Технологии

- **FastAPI** - веб-фреймворк
- **SQLAlchemy** - ORM для работы с базой данных
- **PostgreSQL** - реляционная база данных
- **Alembic** - система миграций
- **Pydantic** - валидация данных
- **Docker** - контейнеризация
- **Uvicorn** - ASGI сервер
