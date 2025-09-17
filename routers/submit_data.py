"""
Роутер для обработки запросов submitData.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.connection import get_db
from repository.pereval_repository import PerevalRepository
from schemas.pereval import PerevalCreate, SubmitDataResponse
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/submitData", response_model=SubmitDataResponse)
async def submit_data(
        pereval_data: PerevalCreate,
        db: Session = Depends(get_db)
):
    """
    POST /submitData - создание нового перевала.

    Принимает JSON с данными о перевале и сохраняет их в PostgreSQL.
    Возвращает ID созданной записи или описание ошибки.
    """
    try:
        # Создаем репозиторий
        pereval_repo = PerevalRepository(db)

        # Создаем перевал и все связанные сущности
        pereval_id = pereval_repo.create_pereval(pereval_data)

        if pereval_id:
            logger.info(f"Успешно создан перевал с ID: {pereval_id}")
            return SubmitDataResponse(
                status=200,
                message=None,
                id=pereval_id
            )
        else:
            logger.error("Не удалось создать перевал")
            return SubmitDataResponse(
                status=500,
                message="Ошибка при создании перевала",
                id=None
            )

    except Exception as e:
        logger.error(f"Ошибка при создании перевала: {str(e)}")

        # Определяем тип ошибки для более точного ответа
        if "connection" in str(e).lower() or "database" in str(e).lower():
            return SubmitDataResponse(
                status=500,
                message="Ошибка подключения к базе данных",
                id=None
            )
        elif "validation" in str(e).lower() or "constraint" in str(e).lower():
            return SubmitDataResponse(
                status=400,
                message="Ошибка валидации данных",
                id=None
            )
        else:
            return SubmitDataResponse(
                status=500,
                message="Внутренняя ошибка сервера",
                id=None
            )
