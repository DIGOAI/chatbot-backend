from typing import TYPE_CHECKING, Optional

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.models.base import Base, ITimeControl, IUuidPk

if TYPE_CHECKING:
    from src.db.models.conversation import Conversation
    from src.db.models.ticket import Ticket


class Client(Base, IUuidPk, ITimeControl):
    """Client class to handle the client model.

    Attributes:
    id (uuid): The id of the client
    ci (str): The cedula of the client
    names (str): The names of the client
    lastnames (str): The lastnames of the client
    phone (str): The phone of the client
    email (str): The email of the client
    saraguros_id (int): The id of the client in saraguros
    created_at (datetime): The datetime when the client was created
    updated_at (datetime): The datetime when the client was updated

    conversations (list[Conversation]): The conversations of the client
    tickets (list[Ticket]): The tickets of the client
    """

    __tablename__ = "clients"

    ci: Mapped[Optional[str]] = mapped_column(String(13), nullable=True, index=True, unique=True)
    names: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    lastnames: Mapped[Optional[str]] = mapped_column(String(40), nullable=True)
    phone: Mapped[str] = mapped_column(String(13), nullable=False)
    email: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    saraguros_id: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)

    conversations: Mapped[list["Conversation"]] = relationship(back_populates="client")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="client")

    def __repr__(self) -> str:
        return f"<Client(id={self.id}, ci={self.ci}, name={self.names}, saraguros_net={self.saraguros_id}, conversations={self.conversations}, tickets={self.tickets}, created_at={self.created_at}, updated_at={self.updated_at})>"
