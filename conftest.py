import random
from entities.user import User
import requests
from api.api_manager_movies import ApiManagerMovies
from api.api_manager import ApiManager
from constants import BASE_URL
import pytest
from utils.data_generator import DataGenerator
from faker import Faker
from custom_requester.custom_requester import CustomRequester
from resources.user_creds import SuperAdminCreds

faker = Faker()

@pytest.fixture(scope="session")
def test_user():
    """
    Генерация случайного пользователя для тестов.
    """

    random_email = DataGenerator.generate_random_email()
    random_name = DataGenerator.generate_random_name()
    random_password = DataGenerator.generate_random_password()

    return {
        "email": random_email,
        "fullName": random_name,
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": ["USER"]
    }

@pytest.fixture(scope="session")
def registered_user(api_manager, test_user):
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.register_user(test_user)
    response_data = response.json()
    registered_user = test_user.copy()
    registered_user["id"] = response_data["id"]
    return registered_user

@pytest.fixture(scope="session")
def admin_creds(api_manager):
    return ["api1@gmail.com", "asdqwe123Q"]

@pytest.fixture(scope="session")
def user_creds(api_manager):
    return ["testovyi@email.com", "12345678AaA"]

@pytest.fixture(scope="session")
def session():
    """
    Фикстура для создания HTTP-сессии.
    """
    http_session = requests.Session()
    yield http_session
    http_session.close()

@pytest.fixture(scope="session")
def api_manager(session):
    """
    Фикстура для создания экземпляра ApiManager.
    """
    return ApiManager(session)

@pytest.fixture(scope="session")
def api_manager_movies(session):
    return ApiManagerMovies(session)

@pytest.fixture(scope="session")
def requester():
    """
    Фикстура для создания экземпляра CustomRequester.
    """
    session = requests.Session()
    return CustomRequester(session=session, base_url=BASE_URL)

@pytest.fixture(scope="session")
def data_get_movies(session):
    return {
        "pageSize": 10,
        "page": 1,
        "minPrice": 1,
        "maxPrice": 1000,
        "locations": "SPB",
        "published": True,
        "genreId": 1,
        "createdAt": "asc"
    }

@pytest.fixture(scope="session")
def create_genre(api_manager_movies, admin_creds):
    api_manager_movies.auth_api.authenticate_admin(admin_creds)
    name = DataGenerator.generate_random_genre()
    response = api_manager_movies.movie_api.create_genre(name)
    response_data = response.json()
    return response_data["id"]



@pytest.fixture(scope="session")
def create_movie_data(session, api_manager_movies, create_genre):
    location_list = ["MSK", "SPB"]
    random_location = random.choice(location_list)
    return {
        "name": DataGenerator.generate_random_password(),
        "imageUrl": "https://randomurl.url",
        "price": random.randint(1,10000),
        "description": DataGenerator.generate_random_password(),
        "location": random_location,
        "published": True,
        "genreId": create_genre
    }

@pytest.fixture
def user_session():
    user_pool = []

    def _create_user_session():
        session = requests.Session()
        user_session = ApiManager(session)
        user_pool.append(user_session)
        return user_session

    yield _create_user_session

    for user in user_pool:
        user.close_session()

@pytest.fixture
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        ["SUPER_ADMIN"],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data