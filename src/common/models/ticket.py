from datetime import datetime
from enum import Enum
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_serializer


class TicketShiftSaraguros(str, Enum):
    """Enum to represent the shifts of a Saraguros ticket."""

    MORNING = "MAÑANA"
    AFTERNOON = "TARDE"


class TicketSaragurosBase(BaseModel):
    client_id: int = Field(..., alias="idcliente")
    department: str = Field(..., alias="dp")
    subject: str = Field(..., alias="asunto")
    applicant: str = Field(..., alias="solicitante")
    visit_date: str = Field(..., alias="fechavisita")
    shift: TicketShiftSaraguros = Field(default=TicketShiftSaraguros.MORNING, alias="turno")
    scheduled_by: str = Field(default="PAGINA WEB", alias="agendado")
    content: str = Field(..., alias="contenido")

    model_config = ConfigDict(populate_by_name=True)


class TicketSaragurosInsert(TicketSaragurosBase):
    """Class to represent a ticket in SaragurosNet.

    Attributes:
    client_id (str): The client id of the ticket
    department (str): The department of the ticket
    subject (str): The subject of the ticket
    applicant (str): The applicant of the ticket
    visit_date (str): The visit date of the ticket
    shift (str): The shift of the ticket
    scheduled_by (str): The scheduled by of the ticket
    content (str): The content of the ticket
    """

    pass


class TicketSaraguros(TicketSaragurosBase):
    """Class to represent a ticket in SaragurosNet.

    Attributes:
    id (int): The id of the ticket
    client_id (str): The client id of the ticket
    department (str): The department of the ticket
    subject (str): The subject of the ticket
    applicant (str): The applicant of the ticket
    visit_date (str): The visit date of the ticket
    shift (str): The shift of the ticket
    scheduled_by (str): The scheduled by of the ticket
    content (str): The content of the ticket

    support_date (str): The support date of the ticket
    closed_date (str): The closed date of the ticket
    last_date (str): The last date of the ticket
    closed_by (str): The closed by of the ticket
    """

    id: int
    support_date: str = Field(..., alias="fecha_soporte")
    closed_date: str = Field(..., alias="fecha_cerrado")
    last_date: str = Field(..., alias="lastdate")
    closed_by: str = Field(..., alias="motivo_cierre")


class TicketShift(str, Enum):
    """Enum to represent the shifts of a ticket."""

    MORNING = "MORNING"
    AFTERNOON = "AFTERNOON"


class TicketStatus(str, Enum):
    WAITING = "WAITING"
    ATTENDING = "ATTENDING"
    CLOSED = "CLOSED"
    UNSOLVED = "UNSOLVED"


class TicketBase(BaseModel):
    subject: str
    shift: Optional[TicketShift] = Field(default=None)
    department_id: str
    status: TicketStatus = Field(default=TicketStatus.WAITING)
    client_id: UUID
    conversation_id: Optional[UUID] = None

    model_config = {
        "from_attributes": True,
    }


class TicketInsert(TicketBase):
    """Class to represent a ticket in the database.

    Attributes:
    subject (str): The subject of the ticket
    shift (str): The shift of the ticket
    department_id (str): The id of the department of the ticket
    status (str): The status of the ticket
    client_id (uuid): The id of the client of the ticket
    conversation_id (uuid): The id of the conversation of the ticket
    """

    pass


class Ticket(TicketBase):
    """Class to represent a ticket in the database.

    Attributes:
    id (uuid): The id of the ticket
    external_id (int): The external id of the ticket (SaragurosNet)
    subject (str): The subject of the ticket
    shift (str): The shift of the ticket
    department_id (str): The id of the department of the ticket
    status (str): The status of the ticket
    client_id (uuid): The id of the client of the ticket
    conversation_id (uuid): The id of the conversation of the ticket
    created_at (datetime): The datetime when the ticket was created
    updated_at (datetime): The datetime when the ticket was updated
    """

    id: UUID
    external_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    @field_serializer("id", "client_id", "conversation_id")
    def serialize_id(self, id: UUID, _info: Any) -> str:
        return str(id)

    @field_serializer("created_at", "updated_at")
    def serialize_dt(self, dt: datetime, _info: Any) -> float:
        return dt.timestamp()
