from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import DateTime
from sqlalchemy import Enum as EnumType
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.api.db.models.base import Base, ITimeControl, IUuidPk

if TYPE_CHECKING:
    from src.common.models.client import Client


class ConversationStatus(str, Enum):
    OPENED = "OPENED"
    CLOSED = "CLOSED"


class Conversation(Base, IUuidPk, ITimeControl):
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

    client (Client): The client of the conversation
    """

    __tablename__ = "conversations"

    client_phone: Mapped[str] = mapped_column(String(13), nullable=False)
    assistant_phone: Mapped[str] = mapped_column(String(13), nullable=False)
    client_id: Mapped[Optional[UUID]] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=True)
    status: Mapped[ConversationStatus] = mapped_column(EnumType(ConversationStatus), default=ConversationStatus.OPENED)
    finished_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    client: Mapped["Client"] = relationship(back_populates="conversations")

    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, client_phone={self.client_phone}, assistant_phone={self.assistant_phone}, client={self.client}, status={self.status}, created_at={self.created_at}, updated_at={self.updated_at}, finished_at={self.finished_at})>"
