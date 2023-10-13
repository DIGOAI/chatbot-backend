from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Enum as EnumType
from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models import MessageType
from src.db.models.base import Base, ICreatedAt

if TYPE_CHECKING:
    from src.db.models.conversation import Conversation


class Message(Base, ICreatedAt):
    """MessageModel class to handle the message model.

    Attributes:
    id (str): The Twilio Message SID (MSXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX) of the message
    sender (str): The phone sender of the message
    receiver (str): The phone receiver of the message
    message (str): The message of the message
    media_url (str): The media url of the message
    message_type (str): Incoming (IN) or Outgoing (OUT) message type (default: IN)
    conversation_id (uuid): The id of the conversation of the message
    created_at (datetime): The datetime when the message was created

    conversation (Conversation): The conversation of the message
    """

    __tablename__ = "messages"

    id: Mapped[str] = mapped_column(String(34), primary_key=True, index=True, nullable=False, server_default=None)
    sender: Mapped[str] = mapped_column(String(13), nullable=False)
    receiver: Mapped[str] = mapped_column(String(13), nullable=False)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    media_url: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    message_type: Mapped[MessageType] = mapped_column(EnumType(MessageType), default=MessageType.IN, nullable=False)
    conversation_id: Mapped[UUID] = mapped_column(ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False)

    conversation: Mapped["Conversation"] = relationship(back_populates="messages")

    def __repr__(self) -> str:
        return f"<Message id={self.id} sender={self.sender} receiver={self.receiver} message={self.message} media_url={self.media_url} message_type={self.message_type} conversation={self.conversation} created_at={self.created_at}>"
