"""
Главный файл FastAPI приложения для работы с перевалами.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.submit_data import router as submit_data_router
from database.connection import engine
from models import user, coords, level, image, pereval

# Создание таблиц в базе данных
user.Base.metadata.create_all(bind=engine)
coords.Base.metadata.create_all(bind=engine)
level.Base.metadata.create_all(bind=engine)
image.Base.metadata.create_all(bind=engine)
pereval.Base.metadata.create_all(bind=engine)

# Создание экземпляра FastAPI
app = FastAPI(
    title="Перевалы API",
    description="API для работы с данными о перевалах",
    version="1.0.0"
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(submit_data_router, prefix="/api", tags=["submit"])

@app.get("/")
async def root():
    """Корневой endpoint для проверки работы API."""
    return {"message": "Перевалы API работает!"}

@app.get("/health")
async def health_check():
    """Endpoint для проверки состояния приложения."""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)