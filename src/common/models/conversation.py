from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer

from src.common.models.client import Client
from src.common.models.message import Message


class ConversationStatus(str, Enum):
    OPENED = "OPENED"
    CLOSED = "CLOSED"


class ConversationBase(BaseModel):
    """ConversationBase class to handle the conversation model.

    Attributes:
    client_phone (str): The phone of the client in the conversation
    assistant_phone (str): The phone of the assistant in the conversation
    client_id (uuid): The id of the client in the conversation
    status (str): The status of the conversation
    finished_at (datetime): The datetime when the conversation was finished
    """

    client_phone: str = Field(min_length=10, max_length=13)
    assistant_phone: str = Field(min_length=10, max_length=13)
    client_id: Optional[UUID] = Field(None)
    status: Optional[ConversationStatus] = Field(default=ConversationStatus.OPENED)
    finished_at: Optional[datetime] = Field(None)

    @field_serializer("finished_at")
    def serialize_dt_none(self, dt: datetime | None, _info: Any) -> float | None:
        if dt is None:
            return None
        return dt.timestamp()

    model_config = {
        "from_attributes": True,
    }


class ConversationInsert(ConversationBase):
    """ConversationInsert class to handle the conversation model.

    Attributes:
    client_phone (str): The phone of the client in the conversation
    assistant_phone (str): The phone of the assistant in the conversation
    client_id (uuid): The id of the client in the conversation
    status (str): The status of the conversation
    finished_at (datetime): The datetime when the conversation was finished
    """

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "client_phone": "+593986728536",
                "assistant_phone": "+593986728536",
                "client_id": "e6a3f1c4-9a9b-4f9c-9b7c-5f1b4a9c8f5c",
                "status": "OPENED",
                "finished_at": "2021-08-29T19:40:00.000Z"
            }
        }
    }


class Conversation(ConversationBase):
    """Conversation class to handle the conversation model.

    Attributes:
    id (uuid): The id of the conversation
    client_phone (str): The phone of the client in the conversation
    assistant_phone (str): The phone of the assistant in the conversation
    client_id (uuid): The id of the client in the conversation
    status (str): The status of the conversation
    created_at (datetime): The datetime when the conversation was created
    updated_at (datetime): The datetime when the conversation was updated
    finished_at (datetime): The datetime when the conversation was finished
    """

    id: UUID
    created_at: datetime
    updated_at: datetime

    @field_serializer("id", "client_id")
    def serialize_id(self, id: UUID, _info: Any) -> str:
        return str(id)

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, dt: datetime, _info: Any) -> float:
        return dt.timestamp()

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "e6a3f1c4-9a9b-4f9c-9b7c-5f1b4a9c8f5c",
                "client_phone": "+593986728536",
                "assistant_phone": "+593986728536",
                "client_id": "e6a3f1c4-9a9b-4f9c-9b7c-5f1b4a9c8f5c",
                "status": "OPENED",
                "created_at": "2021-08-29T19:40:00.000Z",
                "updated_at": "2021-08-29T19:40:00.000Z",
                "finished_at": "2021-08-29T19:40:00.000Z"
            }
        }
    }


class ConversationWithData(Conversation):
    """ConversationWithData class to handle the conversation model.

    Attributes:
    id (uuid): The id of the conversation
    client_phone (str): The phone of the client in the conversation
    assistant_phone (str): The phone of the assistant in the conversation
    client_id (uuid): The id of the client in the conversation
    status (str): The status of the conversation
    created_at (datetime): The datetime when the conversation was created
    updated_at (datetime): The datetime when the conversation was updated
    finished_at (datetime): The datetime when the conversation was finished

    client (Client): The client of the conversation
    messages (list[Message]): The messages of the conversation
    """

    client: Optional["Client"] = Field(default=None)
    messages: list["Message"] = Field(default=[])

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "e6a3f1c4-9a9b-4f9c-9b7c-5f1b4a9c8f5c",
                "client_phone": "+593986728536",
                "assistant_phone": "+593986728536",
                "client_id": "e6a3f1c4-9a9b-4f9c-9b7c-5f1b4a9c8f5c",
                "status": "OPENED",
                "created_at": "2021-08-29T19:40:00.000Z",
                "updated_at": "2021-08-29T19:40:00.000Z",
                "finished_at": "2021-08-29T19:40:00.000Z",
                "messages": [
                    {
                        "id": "MSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                        "conversation_id": "e6a3f1c4-9a9b-4f9c-9b7c-5f1b4a9c8f5c",
                        "sender": "+593986728536",
                        "receiver": "+593986728536",
                        "message": "Message 1 from +593986728536 to +593986728536",
                        "created_at": "2021-08-29T19:40:00.000Z",
                        "media_url": None,
                        "message_type": "IN"
                    },
                ]
            }
        }
    }