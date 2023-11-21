from dataclasses import dataclass
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.cases.ticket_use_cases import TicketUseCase
from src.api.middlewares.jwt_bearer import JWTBearer, Role
from src.common.models import GenericResponse, create_response
from src.common.models.ticket import TicketWithClient

_worker_dependency = Depends(JWTBearer(Role.WORKER))

router = APIRouter(prefix="/tickets", tags=["Tickets"], dependencies=[_worker_dependency])


@dataclass
class TicketsKPIPayload:
    ATTENDING: int
    CLOSED: int
    WAITING: int
    UNSOLVED: int


controller = TicketUseCase()


@router.get("/", response_model=GenericResponse[list[TicketWithClient]])
def get_tickets(limit: int = 10, offset: int = 0):
    result = controller.get_tickets_with_client(limit, offset)
    return create_response(result, "Tickets found")


@router.get("/kpi", response_model=GenericResponse[TicketsKPIPayload])
def get_tickets_kpi():
    result = controller.get_tickets_kpi()
    return create_response(data=result, message='Tickets KPI found')


@router.get("/{ticket_id}", response_model=GenericResponse[TicketWithClient])
def get_ticket(ticket_id: UUID):
    result = controller.get_ticket_with_client(ticket_id)
    return create_response(result, "Ticket found")


@router.get("/{ticket_id}/open")
def open_ticket(ticket_id: UUID):
    result = controller.attend_ticket(ticket_id)
    return create_response(result, "Ticket opened")


@router.get("/{ticket_id}/close")
def close_ticket(ticket_id: UUID):
    result = controller.close_ticket(ticket_id)
    return create_response(result, "Ticket closed")
