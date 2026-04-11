from pydantic import BaseModel, ValidationError, field_validator, Field
from venv import logger
from enums.roles import Roles
from typing import Optional

class User(BaseModel):
    email: str = Field(..., min_length=8, description="Электронная почта")
    fullName: str = Field(..., min_length=8, description="Имя")
    password: str = Field(..., min_length=8, description="Пароль")
    passwordRepeat: str = Field(..., min_length=8, description="Пароль")
    roles: list[Roles] = Field(..., description="Роль пользователя")
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        if "@" not in value:
            raise ValueError("Email должен содержать знак '@'")
        return value

def test_user_data(test_user):
    user = User(**test_user)
    json_data = user.model_dump_json(exclude_unset=True)
    print(json_data)
    #assert json_data["fullName"] == test_user["fullName"]
    logger.info(f"{user.email=} {user.fullName=} {user.password=} {user.passwordRepeat=} \n{user.roles=} {user.verified=} {user.banned=}")

def test_user_data_another_fixture(creation_user_data):
    user = User(**creation_user_data)
    json_data = user.model_dump_json()
    print(json_data)
    #assert user.fullName == creation_user_data["fullName"]
    logger.info(
        f"{user.email=} {user.fullName=} {user.password=} {user.passwordRepeat=} \n{user.roles=} {user.verified=} {user.banned=}")


