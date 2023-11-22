from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID

from pydantic import Field

from src.common.models.base import BaseModel


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
