BASE_URL = "https://auth.dev-cinescope.coconutqa.ru/"
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json"
}
"""
Здесь эндпоинты к AuthAPI
"""
LOGIN_ENDPOINT = "login"
REGISTER_ENDPOINT = "register"
GET_LOGOUT_ENDPOINT = "logout"
GET_REFRESH_TOKENS = "refresh-tokens"
GET_CONFIRM_EMAIL = "confirm"
GET_USER_INFO = "user/"
DELETE_USER = "user/"
PATCH_USER = "user/"
CREATE_USER = "user"
GET_USER_LIST = "user"
"""
Здесь эндпоинты к MoviesAPI
"""
BASE_URL_MOVIES = "https://api.dev-cinescope.coconutqa.ru/"
GET_MOVIES = "movies"
POST_MOVIE = "movies"
GET_MOVIE = "movies/"
DELETE_MOVIE = "movies/"
PATCH_MOVIE = "movies/"

GENRES_URL = "genres"