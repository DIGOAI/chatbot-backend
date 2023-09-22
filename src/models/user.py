from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, field_serializer


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
