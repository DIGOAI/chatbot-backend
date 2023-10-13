from typing import TYPE_CHECKING, Optional
from uuid import UUID

from sqlalchemy import Enum as EnumType
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.common.models import TicketStatus
from src.db.models.base import Base, ITimeControl, IUuidPk
from src.db.models.conversation import Conversation

if TYPE_CHECKING:
    from src.common.models.client import Client
    from src.db.models.conversation import Conversation
    from src.db.models.department import Department


class Ticket(Base, IUuidPk, ITimeControl):
    """Ticket class to handle the ticket model.

    Attributes:
    id (uuid): The id of the ticket
    external_id (int): The external id of the ticket
    subject (str): The subject of the ticket
    shift (str): The shift of the ticket (TARDE ó MAÑANA)
    department_id (uuid): The id of the department of the ticket
    status (TicketStatus): The status of the ticket
    client_id (uuid): The id of the client of the ticket
    conversation_id (uuid): The id of the conversation of the ticket
    created_at (datetime): The datetime when the ticket was created
    updated_at (datetime): The datetime when the ticket was updated

    department (Department): The department of the ticket
    client (Client): The client of the ticket
    conversation (Conversation): The conversation of the ticket
    """

    __tablename__ = "tickets"

    external_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    subject: Mapped[str] = mapped_column(String(255), nullable=False)
    shift: Mapped[Optional[str]] = mapped_column(String(13), nullable=True)
    department_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("departments.id", ondelete="CASCADE"), nullable=False)
    status: Mapped[TicketStatus] = mapped_column(EnumType(TicketStatus), default=TicketStatus.WAITING, nullable=False)
    client_id: Mapped[UUID] = mapped_column(ForeignKey("clients.id", ondelete="CASCADE"), nullable=False)
    conversation_id: Mapped[Optional[UUID]] = mapped_column(
        ForeignKey("conversations.id", ondelete="CASCADE"), nullable=True)

    department: Mapped["Department"] = relationship(back_populates="tickets")
    client: Mapped["Client"] = relationship(back_populates="tickets")
    conversation: Mapped["Conversation"] = relationship(back_populates="ticket")

    def __repr__(self) -> str:
        return f"<Ticket(id={self.id}, external_id={self.external_id}, subject={self.subject}, shift={self.shift}, department={self.department}, status={self.status}, client={self.client}, conversation={self.conversation}, created_at={self.created_at}, updated_at={self.updated_at})>"
