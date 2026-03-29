from .auth_api import AuthAPI
from .movie_api import MovieAPI

class ApiManagerMovies:
    def __init__(self, session):
        self.session = session
        self.auth_api = AuthAPI(session)
        self.movie_api = MovieAPI(session)