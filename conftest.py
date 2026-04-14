import datetime
import random
from entities.user import User
import requests
from api.api_manager import ApiManager
from constants import BASE_URL
import pytest
from sqlalchemy.orm import Session
from db_requester.db_client import get_db_session
from enums.locations_for_movies import Locations
from models.base_models import TestUser, RegisterUserResponse, RequestMovie, ResponseMovie, RequestGetMovie
from utils.data_generator import DataGenerator
from faker import Faker
from custom_requester.custom_requester import CustomRequester
from resources.user_creds import SuperAdminCreds, AdminCreds
from enums.roles import Roles
from db_requester.db_helpers import DBHelper
from uuid import uuid4

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

@pytest.fixture(scope="function")
def data_get_movies(session) -> RequestGetMovie:
    return RequestGetMovie(
        pageSize=random.randint(1, 10),
        page=random.randint(1, 50),
        minPrice=random.randint(1, 300),
        maxPrice=random.randint(500, 10000),
        location=[Locations.MSK],
        published=True,
        genreId=1,
        createdAt="asc"
    )

@pytest.fixture(scope="function")
def create_movie_data() -> RequestMovie:
    return RequestMovie(
        name=DataGenerator.generate_name_movie(),
        imageUrl="https://randomstring.url",
        price=DataGenerator.generate_random_price(),
        description=DataGenerator.generate_description_movie(),
        location=DataGenerator.generate_random_locate(),
        published=True,
        genreId=1
    )

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

@pytest.fixture(scope="module")
def db_session() -> Session:
    """
    Фикстура, которая создает и возвращает сессию для работы с базой данных
    После завершения теста сессия автоматически закрывается
    """
    db_session = get_db_session()
    yield db_session
    db_session.close()

@pytest.fixture(scope="function")
def db_helper(db_session) -> DBHelper:
    """
    Фикстура для экземпляра хелпера
    """
    db_helper = DBHelper(db_session)
    return db_helper

@pytest.fixture(scope="function")
def created_test_user(db_helper):
    """
    Фикстура, которая создает тестового пользователя в БД
    и удаляет его после завершения теста
    """
    user = db_helper.create_test_user(DataGenerator.generate_user_data())
    yield user
    # Cleanup после теста
    if db_helper.get_user_by_id(user.id):
        db_helper.delete_user(user)

@pytest.fixture(scope="function")
def create_test_movie_hardcode():
    return {
        'id': 101010,
        'name': 'Фильмец для теста',
        'price': 500,
        'description': 'Тестовый фильм, так чисто, чтобы помусолить там, как оно крч воркает там, пук, воооот',
        'image_url': 'Имаге.урэлэ',
        'location': 'SPB',
        'published': True,
        'rating': 5,
        'genre_id': 1,
        'created_at': datetime.datetime.now()
    }