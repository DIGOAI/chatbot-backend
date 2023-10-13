from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, field_serializer

from src.common.utils import PASSWORD_PATTERN


class SystemRole(str, Enum):
    OTHER = "OTHER"
    WORKER = "WORKER"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"


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
    names: Optional[str] = Field(min_length=4, max_length=40, default=None,)
    lastnames: Optional[str] = Field(min_length=4, max_length=40, default=None)


class User(BaseModel):
    id: UUID
    email: EmailStr
    password: str
    names: Optional[str]
    lastnames: Optional[str]
    system_role: SystemRole
    job_role_id: Optional[UUID]
    active: bool
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, dt: datetime, _info: Any) -> float:
        return dt.timestamp()

    model_config = {
        "from_attributes": True
    }
