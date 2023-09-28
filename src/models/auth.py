from pydantic import BaseModel, EmailStr, Field

from src.models.user import UserRole
from src.utils import PASSWORD_PATTERN


class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str = "not implemented"


class LoginSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32, pattern=PASSWORD_PATTERN)


class RegisterSchema(BaseModel):
    email: EmailStr
    role: UserRole = Field(default=UserRole.WORKER)
    password: str = Field(min_length=8, max_length=32, pattern=PASSWORD_PATTERN)
