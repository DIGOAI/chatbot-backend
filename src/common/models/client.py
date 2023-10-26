from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer


class ClientBase(BaseModel):
    """ClientBase class to handle the client model.

    Attributes:
    ci (str): The cedula of the client
    names (str): The names of the client
    lastnames (str): The lastnames of the client
    phone (str): The phone of the client
    saraguros_id (int): The id of the client in saragurosnet
    """

    ci: Optional[str] = Field(min_length=10, max_length=13, default=None)
    names: Optional[str] = Field(min_length=4, max_length=40, default=None)
    lastnames: Optional[str] = Field(min_length=4, max_length=40, default=None)
    phone: str = Field(min_length=10, max_length=13)
    saraguros_id: Optional[int] = Field(None)

    model_config = {
        "from_attributes": True,
    }


class ClientInsert(ClientBase):
    """ClientInsert class to handle the client model.

    Attributes:
    ci (str): The cedula of the client
    names (str): The names of the client
    lastnames (str): The lastnames of the client
    phone (str): The phone of the client
    saraguros_id (int): The id of the client in saragurosnet
    """

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "ci": "0105997001",
                "names": "Juan",
                "lastnames": "Perez",
                "phone": "+593986728536",
                "saraguros_id": 1,
            }
        }
    }


class Client(ClientBase):
    """Client class to handle the client model.

    Attributes:
    id (uuid): The id of the client
    ci (str): The cedula of the client
    names (str): The names of the client
    lastnames (str): The lastnames of the client
    phone (str): The phone of the client
    saraguros_id (int): The id of the client in saragurosnet
    created_at (datetime): The datetime when the client was created
    updated_at (datetime): The datetime when the client was updated
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    @field_serializer("id")
    def serialize_id(self, id: UUID, _info: Any) -> str:
        return str(id)

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, dt: datetime, _info: Any) -> float:
        return self.created_at.timestamp()

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "a0eebc99-9c0b-4ef8-bb6d-6bb9bd380a11",
                "ci": "0105997001",
                "names": "Juan",
                "lastnames": "Perez",
                "phone": "+593986728536",
                "last_state": "1.0",
                "created_at": "2021-04-03T17:52:42.041338",
                "updated_at": "2021-04-03T17:52:42.041338"
            }
        }
    }
