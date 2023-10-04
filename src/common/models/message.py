from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel, field_serializer


class MessageBase(BaseModel):
    sender: str
    message: str
    client_id: Optional[int]


class Message(MessageBase):
    """Message class to handle the message model.

    Attributes:
    id (int): The id of the message
    sender (str): The sender of the message
    message (str): The message of the message
    client_id (int): The id of the client
    created_at (datetime): The datetime when the message was created
    """

    id: int
    created_at: datetime

    @field_serializer("created_at")
    def serialize_dt(self, dt: datetime, _info: Any) -> float:
        return self.created_at.timestamp()

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": 1,
                "sender": "+593905997001",
                "message": "Hola",
                "client_id": 1,
                "created_at": "2021-08-01T00:00:00.000000"
            }
        }
    }


class MessageInsert(MessageBase):
    """Message class to handle the message model.

    Attributes:
    sender (str): The sender of the message
    message (str): The message of the message
    client_id (int): The id of the client
    """

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "sender": "+593905997001",
                "message": "Hola",
                "client_id": 1
            }
        }
    }
