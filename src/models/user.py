from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, field_serializer
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from src.db.database import Base


class UserModel(Base):
    """UserModel class to handle the user model.

    Attributes:
    __tablename__ (str): The name of the table
    id (int): The id of the user
    ci (str): The cedula of the user
    name (str): The name of the user
    phone (str): The phone of the user
    last_state (str): The last state of the user
    saraguros_id (int): The id of the user in saragurosnet
    created_at (datetime): The datetime when the user was created
    updated_at (datetime): The datetime when the user was updated
    """

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    ci: Mapped[str] = mapped_column(String(13))
    name: Mapped[str] = mapped_column(String(80))
    phone: Mapped[str] = mapped_column(String(13))
    last_state: Mapped[str] = mapped_column(String(10))
    saraguros_id: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"<UserModel(id={self.id}, ci={self.ci}, name={self.name}, phone={self.phone}, last_state={self.last_state}, saraguros_id={self.saraguros_id}, created_at={self.created_at}, updated_at={self.updated_at})>"


class UserInsert(BaseModel):
    """User class to handle the user model.

    Attributes:
    ci (str): The cedula of the user
    name (str): The name of the user
    phone (str): The phone of the user
    saraguros_id (int): The id of the user in saragurosnet
    last_state (str): The last state of the user
    """

    ci: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    saraguros_id: Optional[int]
    last_state: Optional[str]

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "ci": "0105997001",
                "name": "Juan Perez",
                "phone": "+593986728536",
                "saraguros_id": 1,
                "last_state": "1.0"
            }
        }
    }


class User(BaseModel):
    """User class to handle the user model.

    Attributes:
    id (int): The id of the user
    ci (str): The cedula of the user
    name (str): The name of the user
    phone (str): The phone of the user
    last_state (str): The last state of the user
    saraguros_id (int): The id of the user in saragurosnet
    created_at (datetime): The datetime when the user was created
    updated_at (datetime): The datetime when the user was updated
    """

    id: int
    ci: Optional[str]
    name: Optional[str]
    phone: Optional[str]
    last_state: Optional[str]
    saraguros_id: Optional[int]
    created_at: datetime
    updated_at: datetime

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, dt: datetime, _info: Any) -> float:
        return self.created_at.timestamp()

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "ci": "0105997001",
                "name": "Juan Perez",
                "phone": "+593986728536",
                "last_state": "1.0",
                "saraguros_id": 1,
                "created_at": "2021-04-03T17:52:42.041338",
                "updated_at": "2021-04-03T17:52:42.041338"
            }
        }
    }
