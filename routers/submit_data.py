"""
Роутер для обработки запросов submitData.
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database.connection import get_db
from repository.pereval_repository import PerevalRepository
from schemas.pereval import PerevalCreate, SubmitDataResponse, PerevalUpdate, PerevalDetailResponse, UpdateResponse
from models.user import User
from models.coords import Coords
from models.level import Level
from models.image import Image
from models.pereval import Pereval
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

@router.get("/submitData/{pereval_id}", response_model=PerevalDetailResponse)
async def get_pereval_by_id(
    pereval_id: int,
    db: Session = Depends(get_db)
):
    """
    GET /submitData/{id} - получение перевала по ID.
    
    Возвращает полную информацию о перевале включая статус.
    """
    try:
        pereval_repo = PerevalRepository(db)
        pereval = pereval_repo.get_pereval_by_id(pereval_id)
        
        if not pereval:
            raise HTTPException(
                status_code=400,
                detail="Перевал не найден"
            )
        
        # Получаем связанные данные
        user = db.query(User).filter(User.id == pereval.user_id).first()
        coords = db.query(Coords).filter(Coords.id == pereval.coords_id).first()
        level = db.query(Level).filter(Level.id == pereval.level_id).first()
        images = db.query(Image).filter(Image.pereval_id == pereval_id).all()
        
        # Формируем ответ
        response_data = {
            "id": pereval.id,
            "beauty_title": pereval.beauty_title,
            "title": pereval.title,
            "other_titles": pereval.other_titles,
            "connect": pereval.connect,
            "add_time": pereval.add_time,
            "status": pereval.status.value,
            "user": user,
            "coords": coords,
            "level": level,
            "images": images
        }
        
        return PerevalDetailResponse(**response_data)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Ошибка при получении перевала {pereval_id}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )

@router.patch("/submitData/{pereval_id}", response_model=UpdateResponse)
async def update_pereval(
    pereval_id: int,
    update_data: PerevalUpdate,
    db: Session = Depends(get_db)
):
    """
    PATCH /submitData/{id} - обновление перевала.
    
    Обновляет перевал только если его статус = 'new'.
    Запрещено изменять ФИО, email и телефон пользователя.
    """
    try:
        pereval_repo = PerevalRepository(db)
        
        # Проверяем существование перевала
        pereval = pereval_repo.get_pereval_by_id(pereval_id)
        if not pereval:
            return UpdateResponse(
                state=0,
                message="Перевал не найден"
            )
        
        # Проверяем статус
        if pereval.status.value != "new":
            return UpdateResponse(
                state=0,
                message="Редактирование запрещено: статус не 'new'"
            )
        
        # Подготавливаем данные для обновления
        update_dict = update_data.dict(exclude_unset=True)
        
        # Удаляем запрещенные поля пользователя (если они случайно попали)
        forbidden_user_fields = ['email', 'fam', 'name', 'otc', 'phone']
        for field in forbidden_user_fields:
            update_dict.pop(field, None)
        
        # Преобразуем Pydantic объекты в словари для связанных сущностей
        if 'coords' in update_dict and hasattr(update_dict['coords'], 'dict'):
            update_dict['coords'] = update_dict['coords'].dict()
        
        if 'level' in update_dict and hasattr(update_dict['level'], 'dict'):
            update_dict['level'] = update_dict['level'].dict()
        
        if 'images' in update_dict:
            images_list = []
            for img in update_dict['images']:
                if hasattr(img, 'dict'):
                    images_list.append(img.dict())
                else:
                    images_list.append(img)
            update_dict['images'] = images_list
        
        # Обновляем перевал
        success = pereval_repo.update_pereval(pereval_id, update_dict)
        
        if success:
            return UpdateResponse(
                state=1,
                message=None
            )
        else:
            return UpdateResponse(
                state=0,
                message="Ошибка при обновлении перевала"
            )
            
    except Exception as e:
        logger.error(f"Ошибка при обновлении перевала {pereval_id}: {str(e)}")
        return UpdateResponse(
            state=0,
            message="Внутренняя ошибка сервера"
        )

@router.get("/submitData/", response_model=List[PerevalDetailResponse])
async def get_perevals_by_user_email(
    user__email: str = Query(..., description="Email пользователя"),
    offset: int = Query(0, ge=0, description="Смещение для пагинации"),
    limit: Optional[int] = Query(None, ge=1, description="Лимит записей для пагинации"),
    db: Session = Depends(get_db)
):
    """
    GET /submitData/?user__email=<email> - получение перевалов по email пользователя.
    
    Возвращает список всех перевалов, добавленных пользователем с указанным email.
    Поддерживает пагинацию через параметры offset и limit.
    """
    try:
        pereval_repo = PerevalRepository(db)
        perevals = pereval_repo.list_perevals_by_user_email(user__email, offset, limit)
        
        result = []
        for pereval in perevals:
            # Получаем связанные данные
            user = db.query(User).filter(User.id == pereval.user_id).first()
            coords = db.query(Coords).filter(Coords.id == pereval.coords_id).first()
            level = db.query(Level).filter(Level.id == pereval.level_id).first()
            images = db.query(Image).filter(Image.pereval_id == pereval.id).all()
            
            # Формируем ответ
            response_data = {
                "id": pereval.id,
                "beauty_title": pereval.beauty_title,
                "title": pereval.title,
                "other_titles": pereval.other_titles,
                "connect": pereval.connect,
                "add_time": pereval.add_time,
                "status": pereval.status.value,
                "user": user,
                "coords": coords,
                "level": level,
                "images": images
            }
            
            result.append(PerevalDetailResponse(**response_data))
        
        return result
        
    except Exception as e:
        logger.error(f"Ошибка при получении перевалов для email {user__email}: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail="Внутренняя ошибка сервера"
        )
