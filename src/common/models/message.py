from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_serializer


class MessageType(str, Enum):
    """MessageType class to handle the message type enum."""

    IN = "IN"
    OUT = "OUT"


class MessageBase(BaseModel):
    id: str
    sender: str
    receiver: str
    message: str
    media_url: Optional[str]
    message_type: MessageType = Field(default=MessageType.IN)
    conversation_id: UUID

    model_config = {
        "from_attributes": True,
    }

    @field_serializer("conversation_id")
    def serialize_id(self, id: UUID, _info: Any) -> str:
        return str(id)


class Message(MessageBase):
    """Message class to handle the message model.

    Attributes:
    id (str): The Twilio Message SID (MSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX) of the message
    sender (str): The phone sender of the message
    receiver (str): The phone receiver of the message
    message (str): The message of the message
    media_url (str): The media url of the message
    message_type (str): Incoming (IN) or Outgoing (OUT) message type (default: IN)
    conversation_id (uuid): The id of the conversation of the message
    created_at (datetime): The datetime when the message was created
    """

    created_at: datetime

    @field_serializer("created_at")
    def serialize_dt(self, dt: datetime, _info: Any) -> float:
        return self.created_at.timestamp()

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "MSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "sender": "+593905997001",
                "receiver": "+593905997001",
                "message": "Hola",
                "media_url": "https://www.google.com",
                "message_type": "IN",
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "created_at": "2021-08-01T00:00:00.000000"
            }
        }
    }


class MessageInsert(MessageBase):
    """Message class to handle the message model.

    Attributes:
    id (str): The Twilio Message SID (MSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX) of the message
    sender (str): The phone sender of the message
    receiver (str): The phone receiver of the message
    message (str): The message of the message
    media_url (str): The media url of the message
    message_type (str): Incoming (IN) or Outgoing (OUT) message type (default: IN)
    conversation_id (uuid): The id of the conversation of the message
    """

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "example": {
                "id": "MSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
                "sender": "+593905997001",
                "receiver": "+593905997001",
                "message": "Hola",
                "media_url": "https://www.google.com",
                "message_type": "IN",
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000"
            }
        }
    }


class MessageInsertWeb(BaseModel):
    receiver: str
    message: str
    conversation_id: UUID

    @field_serializer("conversation_id")
    def serialize_id(self, id: UUID, _info: Any) -> str:
        return str(id)
