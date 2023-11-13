from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.cases.ticket_use_cases import TicketUseCase
from src.api.middlewares.jwt_bearer import JWTBearer, Role
from src.common.models import GenericResponse, create_response
from src.common.models.ticket import Ticket

_worker_dependency = Depends(JWTBearer(Role.WORKER))

router = APIRouter(prefix="/tickets", tags=["Tickets"], dependencies=[_worker_dependency])

controller = TicketUseCase()


@router.get("/", response_model=GenericResponse[list[Ticket]])
def get_tickets(limit: int = 10, offset: int = 0):
    result = controller.get_tickets(limit, offset)
    return create_response(result, "Tickets found")


@router.get("/{ticket_id}", response_model=GenericResponse[Ticket])
def get_ticket(ticket_id: UUID):
    result = controller.get_ticket(ticket_id)
    return create_response(result, "Ticket found")


@router.get("/{ticket_id}/open")
def open_ticket(ticket_id: UUID):
    result = controller.attend_ticket(ticket_id)
    return create_response(result, "Ticket opened")


@router.get("/{ticket_id}/close")
def close_ticket(ticket_id: UUID):
    result = controller.close_ticket(ticket_id)
    return create_response(result, "Ticket closed")
