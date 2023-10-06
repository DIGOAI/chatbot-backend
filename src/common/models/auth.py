from pydantic import BaseModel, EmailStr, Field

from src.common.models.user import SystemRole
from src.common.utils import PASSWORD_PATTERN


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str = "not implemented"


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32, pattern=PASSWORD_PATTERN)


class RegisterSchema(BaseModel):
    email: EmailStr
    role: SystemRole = Field(default=SystemRole.WORKER)
    password: str = Field(min_length=8, max_length=32, pattern=PASSWORD_PATTERN)
