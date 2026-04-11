import pytest
from utils.data_generator import DataGenerator
from enums.roles import Roles
from typing import Optional

@pytest.fixture
def registration_user_data():
    random_password = DataGenerator.generate_random_password()

    return {
        "email": DataGenerator.generate_random_email(),
        "fullName": DataGenerator.generate_random_name(),
        "password": random_password,
        "passwordRepeat": random_password,
        "roles": [Roles.USER.value],
        "verified": Optional[bool],
        "banned": Optional[bool]

    }