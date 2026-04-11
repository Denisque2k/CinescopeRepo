import random
from entities.user import User
import requests
from api.api_manager import ApiManager
from constants import BASE_URL
import pytest

from models.base_models import TestUser, RegisterUserResponse
from utils.data_generator import DataGenerator
from faker import Faker
from custom_requester.custom_requester import CustomRequester
from resources.user_creds import SuperAdminCreds, AdminCreds
from enums.roles import Roles

faker = Faker()

@pytest.fixture(scope="function")
def test_user() -> TestUser:
    """
    Генерация случайного пользователя для тестов.
    """
    random_password = DataGenerator.generate_random_password()

    return TestUser(
        email=DataGenerator.generate_random_email(),
        fullName=DataGenerator.generate_random_name(),
        password=random_password,
        passwordRepeat=random_password,
        roles=[Roles.USER]
    )

@pytest.fixture(scope="function")
def registered_user(api_manager, test_user: TestUser) -> TestUser:
    """
    Фикстура для регистрации и получения данных зарегистрированного пользователя.
    """
    response = api_manager.auth_api.register_user(test_data=test_user.model_dump())
    response_data = RegisterUserResponse(**response.json())
    registered_user = test_user.model_copy(update={"id": response_data.id})
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

@pytest.fixture(scope="function")
def creation_user_data(test_user: TestUser) -> TestUser:
    updated_data = test_user.model_copy(update={"verified": True, "banned": False})
    return updated_data

@pytest.fixture(scope="function")
def super_admin(user_session):
    new_session = user_session()

    super_admin = User(
        SuperAdminCreds.USERNAME,
        SuperAdminCreds.PASSWORD,
        [Roles.SUPER_ADMIN.value],
        new_session)

    super_admin.api.auth_api.authenticate(super_admin.creds)
    return super_admin

@pytest.fixture(scope="function")
def common_user(user_session, super_admin, creation_user_data: TestUser):
    new_session = user_session()

    common_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.USER],
        new_session)

    create_response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
    user_data = RegisterUserResponse(**create_response.json())
    common_user.id = user_data.id
    common_user.api.auth_api.authenticate(common_user.creds)
    return common_user

@pytest.fixture(scope="function")
def admin_user(user_session, super_admin, creation_user_data: TestUser):
    new_session = user_session()

    admin_user = User(
        creation_user_data.email,
        creation_user_data.password,
        [Roles.ADMIN],
        new_session)

    create_response = super_admin.api.user_api.create_user(creation_user_data.model_dump())
    user_data = RegisterUserResponse(**create_response.json())
    admin_user.id = user_data.id
    patch_data = {
            "roles": [Roles.ADMIN],
            "verified": True,
            "banned": False
        }
    super_admin.api.user_api.patch_user(patch_data=patch_data, user_id=admin_user.id, expected_status=200)
    admin_user.api.auth_api.authenticate(admin_user.creds)
    return admin_user

@pytest.fixture
def admin_user_with_creds(user_session, creation_user_data: TestUser):
    new_session = user_session()

    admin_user_wth_creds = User(
        AdminCreds.USERNAME,
        AdminCreds.PASSWORD,
        [Roles.ADMIN],
        new_session)

    admin_user_wth_creds.api.auth_api.authenticate(admin_user_wth_creds.creds)
    return admin_user_wth_creds