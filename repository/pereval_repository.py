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
from typing import Optional


class PerevalRepository:
    """Репозиторий для работы с перевалами."""

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user_data: UserCreate) -> User:
        """Создание пользователя."""
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

    def create_coords(self, coords_data: CoordsCreate) -> Coords:
        """Создание координат."""
        db_coords = Coords(
            latitude=coords_data.latitude,
            longitude=coords_data.longitude,
            height=coords_data.height
        )
        self.db.add(db_coords)
        self.db.commit()
        self.db.refresh(db_coords)
        return db_coords

    def create_level(self, level_data: LevelCreate) -> Level:
        """Создание уровня сложности."""
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

    def create_images(self, images_data: list[ImageCreate], pereval_id: int) -> list[Image]:
        """Создание изображений."""
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
        