from pydantic import BaseModel
from enums.roles import Roles
from typing import Optional
class User(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str
    roles: Roles
    verified: Optional[bool]
    banned: Optional[bool]