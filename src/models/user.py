from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, EmailStr, Field, field_serializer


class UserRole(str, Enum):
    WORKER = "WORKER"
    ADMIN = "ADMIN"
    SUPPORT = "SUPPORT"


class User(BaseModel):
    id: int
    email: EmailStr
    role: UserRole = Field(default=UserRole.WORKER)
    password: str
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, dt: datetime, _info: Any) -> float:
        return dt.timestamp()

    model_config = {
        "from_attributes": True
    }
