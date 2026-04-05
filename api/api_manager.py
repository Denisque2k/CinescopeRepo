from .auth_api import AuthAPI
from .user_api import UserAPI
from .movie_api import MovieAPI

class ApiManager:
    """
    Класс для управления API-классами с единой HTTP-сессией.
    """
    def __init__(self, session):
        """
        Инициализация ApiManager.
        :param session: HTTP-сессия, используемая всеми API-классами.
        """
        self.session = session
        self.auth_api = AuthAPI(session)
        self.user_api = UserAPI(session)
        self.movie_api = MovieAPI(session)

    def close_session(self):
        self.session.close()