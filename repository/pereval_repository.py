"""
Репозиторий для работы с перевалами в базе данных.
"""
from sqlalchemy.orm import Session
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
from typing import Optional, List


class PerevalRepository:
    """Репозиторий для работы с перевалами."""

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """Создание пользователя."""
        try:
            # Проверяем, существует ли пользователь с таким email
            existing_user = self.db.query(User).filter(User.email == user_data.email).first()
            if existing_user:
                return existing_user
            
            # Создаем нового пользователя
            db_user = User(
                email=user_data.email,
                fam=user_data.fam,
                name=user_data.name,
                otc=user_data.otc,
                phone=user_data.phone
            )
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except Exception as e:
            self.db.rollback()
            raise e

    def create_coords(self, coords_data: CoordsCreate) -> Coords:
        """Создание координат."""
        try:
            db_coords = Coords(
                latitude=coords_data.latitude,
                longitude=coords_data.longitude,
                height=coords_data.height
            )
            self.db.add(db_coords)
            self.db.commit()
            self.db.refresh(db_coords)
            return db_coords
        except Exception as e:
            self.db.rollback()
            raise e

    def create_level(self, level_data: LevelCreate) -> Level:
        """Создание уровня сложности."""
        try:
            db_level = Level(
                winter=level_data.winter,
                summer=level_data.summer,
                autumn=level_data.autumn,
                spring=level_data.spring
            )
            self.db.add(db_level)
            self.db.commit()
            self.db.refresh(db_level)
            return db_level
        except Exception as e:
            self.db.rollback()
            raise e

    def create_images(self, images_data: list[ImageCreate], pereval_id: int) -> list[Image]:
        """Создание изображений."""
        try:
            db_images = []
            for image_data in images_data:
                db_image = Image(
                    data=image_data.data,
                    title=image_data.title,
                    pereval_id=pereval_id
                )
                self.db.add(db_image)
                db_images.append(db_image)
            
            self.db.commit()
            for db_image in db_images:
                self.db.refresh(db_image)
            
            return db_images
        except Exception as e:
            self.db.rollback()
            raise e

    def create_pereval(self, pereval_data: PerevalCreate) -> Optional[int]:
        """Создание перевала и всех связанных сущностей."""
        try:
            # Создаем пользователя
            user = self.create_user(pereval_data.user)

            # Создаем координаты
            coords = self.create_coords(pereval_data.coords)

            # Создаем уровень сложности
            level = self.create_level(pereval_data.level)

            # Создаем перевал
            db_pereval = Pereval(
                beauty_title=pereval_data.beauty_title,
                title=pereval_data.title,
                other_titles=pereval_data.other_titles,
                connect=pereval_data.connect,
                add_time=pereval_data.add_time,
                user_id=user.id,
                coords_id=coords.id,
                level_id=level.id,
                status=PerevalStatus.NEW
            )
            self.db.add(db_pereval)
            self.db.commit()
            self.db.refresh(db_pereval)

            # Создаем изображения
            self.create_images(pereval_data.images, db_pereval.id)

            return db_pereval.id

        except Exception as e:
            self.db.rollback()
            raise e
    
    def get_pereval_by_id(self, pereval_id: int) -> Optional[Pereval]:
        """Получение перевала по ID."""
        return self.db.query(Pereval).filter(Pereval.id == pereval_id).first()
    
    def update_pereval(self, pereval_id: int, data: dict) -> bool:
        """Обновление перевала (только если статус = new)."""
        try:
            pereval = self.get_pereval_by_id(pereval_id)
            if not pereval:
                return False
            
            # Проверяем статус
            if pereval.status != PerevalStatus.NEW:
                return False
            
            # Обновляем разрешенные поля
            allowed_fields = [
                'beauty_title', 'title', 'other_titles', 'connect', 'add_time'
            ]
            
            for field in allowed_fields:
                if field in data:
                    setattr(pereval, field, data[field])
            
            # Обновляем связанные сущности если они переданы
            if 'coords' in data:
                coords_data = data['coords']
                coords = self.db.query(Coords).filter(Coords.id == pereval.coords_id).first()
                if coords and isinstance(coords_data, dict):
                    coords.latitude = coords_data.get('latitude', coords.latitude)
                    coords.longitude = coords_data.get('longitude', coords.longitude)
                    coords.height = coords_data.get('height', coords.height)
            
            if 'level' in data:
                level_data = data['level']
                level = self.db.query(Level).filter(Level.id == pereval.level_id).first()
                if level and isinstance(level_data, dict):
                    level.winter = level_data.get('winter', level.winter)
                    level.summer = level_data.get('summer', level.summer)
                    level.autumn = level_data.get('autumn', level.autumn)
                    level.spring = level_data.get('spring', level.spring)
            
            if 'images' in data:
                images_data = data['images']
                if isinstance(images_data, list):
                    # Удаляем старые изображения
                    self.db.query(Image).filter(Image.pereval_id == pereval_id).delete()
                    
                    # Добавляем новые
                    for image_data in images_data:
                        if isinstance(image_data, dict) and 'data' in image_data and 'title' in image_data:
                            new_image = Image(
                                data=image_data['data'],
                                title=image_data['title'],
                                pereval_id=pereval_id
                            )
                            self.db.add(new_image)
            
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            raise e
    
    def list_perevals_by_user_email(self, email: str, offset: int = 0, limit: Optional[int] = None) -> List[Pereval]:
        """Получение списка перевалов по email пользователя."""
        query = self.db.query(Pereval).join(User).filter(User.email == email)
        
        if limit:
            query = query.offset(offset).limit(limit)
        else:
            query = query.offset(offset)
        
        return query.all()
