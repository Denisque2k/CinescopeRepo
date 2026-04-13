from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movie import MovieDBModel
from db_models.transaction_template import AccountTransactionTemplate

class DBHelper:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        """Класс с методами для работы с БД в тестах"""

    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Создает тестового пользователя"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: str):
        """Получает пользователя по ID"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    def get_user_by_email(self, email: str):
        """Получает юзера по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).first()

    def get_movie_by_name(self, name: str):
        """Получает фильм про названию"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.name == name).first()

    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        return self.db_session.query(UserDBModel).filter(UserDBModel.email == email).count() > 0

    def delete_user(self, user: UserDBModel):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()

    def get_movie_by_id(self, movie_id: int):
        """Получаем фильм по ID"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.id == movie_id).first()

    def get_movie_by_location(self, location: str):
        """Получаем фильмы в из нужной нам локации"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.location == location).all()

    def get_movie_by_genre(self, genre_id: int):
        """Получаем фильмы нужного нам жанра"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.genre_id == genre_id).all()

    def get_movie_by_price(self, min_price: int, max_price: int):
        """Получаем фильмы в диапазоне нужных нам цен"""
        return self.db_session.query(MovieDBModel).filter(min_price < MovieDBModel.price < max_price).all()

    def get_movie_by_rating(self, rating: float):
        """Получаем фильмы нужного рейтина или выше"""
        return self.db_session.query(MovieDBModel).filter(MovieDBModel.rating >= rating).all()

    def create_test_movie(self, create_movie_data: dict) -> MovieDBModel:
        movie = MovieDBModel(**create_movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)

    def movie_exists_by_id(self, movie_id: int):
        return self.db_session.query(MovieDBModel.id).filter(MovieDBModel.id == movie_id).count() > 0