import random
from entities.user import User
import requests
from api.api_manager import ApiManager
from constants import BASE_URL
import pytest
from utils.data_generator import DataGenerator
from faker import Faker
from custom_requester.custom_requester import CustomRequester
from resources.user_creds import SuperAdminCreds, AdminCreds
from enums.roles import Roles

faker = Faker()

@pytest.fixture(scope="function")
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
        "roles": [Roles.USER.value]
    }

@pytest.fixture(scope="function")
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

"""@pytest.fixture(scope="session")
def api_manager_movies(session):
    return ApiManagerMovies(session)"""

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

@pytest.fixture(scope="function")
def create_movie_data():
    location_list = ["MSK", "SPB"]
    random_location = random.choice(location_list)
    return {
        "name": DataGenerator.generate_random_password(),
        "imageUrl": "https://randomurl.url",
        "price": random.randint(1,10000),
        "description": DataGenerator.generate_random_password(),
        "location": random_location,
        "published": True,
        "genreId": 1
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
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture
def admin_user(user_session):
    new_session = user_session()

    admin_user = User(
        AdminCreds.USERNAME,
        AdminCreds.PASSWORD,
        [Roles.ADMIN.value],
        new_session
    )
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture(scope="function")
def creation_user_data(test_user):
    updated_data = test_user.copy()
    updated_data.update({
        "verified": True,
        "banned": False
    })
    return updated_data

@pytest.fixture
def common_user(user_session, super_admin, creation_user_data):
    new_session = user_session()

    common_user = User(
        creation_user_data["email"],
        creation_user_data["password"],
        [Roles.USER.value],
        new_session)

    create_response = super_admin.api.user_api.create_user(creation_user_data)
    user_data = create_response.json()
    common_user.id = user_data.get("id")
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user
