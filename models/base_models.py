from pydantic import BaseModel, Field, field_validator
from enums.roles import Roles
from enums.locations_for_movies import Locations
from typing import Optional, List
import datetime
import re

def validate_email(value: str) -> str:
    if "@" not in value:
        raise ValueError("Email должен содержать знак '@'")
    return value

class TestUser(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(..., min_length=1, max_length=20, description="Пароли должны совпадать")
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None
    id: Optional[int] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        return validate_email(value)

# Добавляем кастомный JSON-сериализатор для Enum
    class Config:
        json_encoders = {
            Roles: lambda v: v.value,
            Locations: lambda v: v.value# Преобразуем Enum в строку
        }

class RegisterUserResponse(BaseModel):
    id: Optional[str] = None
    email: str = Field(pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    fullName: str
    verified: bool
    banned: bool
    roles: list[Roles]
    createdAt: str = Field(description="Дата и время создания пользователя в формате ISO 8601")

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError("Некорректный формат даты и времени")
        return value

class LoginUserRequest(BaseModel):
    email: str = Field(..., description="Email пользователя")
    password: str = Field(..., description="Пароль")

class LoginResponseUser(BaseModel):
    id: str
    email: str
    fullName: str
    roles: list[Roles]

class LoginUserResponse(BaseModel):
    user: LoginResponseUser
    accessToken: str
    refreshToken: str
    expiresIn: int

class ResponseGetRefreshTokens(BaseModel):
    accessToken: str
    refreshToken: str
    expiresIn: int

class RequestCreateUserBySuperAdmin(BaseModel):
    fullName: str = Field(...,description="Имя пользователя")
    email: str = Field(...,description="Email пользователя")
    password: str = Field(..., description="Пароль пользователя")
    verified: bool
    banned: bool

    @field_validator("email")
    def check_email(cls, value: str) -> str:
        return validate_email(value)

class RequestPatchUser(BaseModel):
    roles: list[Roles]
    verified: bool
    banned: bool

class RequestListUsers(BaseModel):
    roles: list[Roles] = Field(..., description="Роль пользователя")
    pageSize: int
    page: int
    createAt: str

class ResponseListUsers(BaseModel):
    users: list[RegisterUserResponse]
    count: int
    page: int
    pageSize: int

class RequestGetMovie(BaseModel):
    pageSize: int
    page: int
    minPrice: int
    maxPrice: int
    location: list[Locations]
    published: bool
    genreId: int
    createdAt: str

class RequestMovie(BaseModel):
    name: str = Field(...,description="Название фильма")
    imageUrl: str
    price: float = Field(...,description="Стоимость")
    description: str
    location: str
    published: bool
    genreId: int

class ResponseMovie(BaseModel):
    id: int = Field(...,description="ID фильма")
    name: str = Field(...,description="Название фильма")
    price: float = Field(...,description="Стоимость")
    description: str
    imageUrl: str
    location: str
    published: bool
    genreId: int
    genre: dict
    createdAt: str
    rating: float