from fastapi import APIRouter

# use cases
from src.api.cases.ticket_use_cases import TicketUseCase

# models
from src.common.models import GenericResponse

# schemas
from src.common.models.ticket import Ticket, TicketInsert

router = APIRouter(prefix="/tickets", tags=["Tickets"])


controller = TicketUseCase()


@router.get("/", response_model=GenericResponse[list[Ticket]])
def get_tickets(limit: int = 30, offset: int = 0):
    result = controller.list(limit, offset)
    return result


@router.get("/{ticket_id}", response_model=GenericResponse[Ticket])
def get_ticket(ticket_id: str):
    result = controller.get(ticket_id)
    return result


@router.post("/", response_model=GenericResponse[Ticket])
def create_ticket(form: TicketInsert):
    result = controller.add(form.model_dump())
    return result


@router.put("/{ticket_id}")
def update_ticket(ticket_id: str, form: TicketInsert):
    result = controller.update(ticket_id, form.model_dump())
    return result


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: str):
    result = controller.delete(ticket_id)
    return result


@router.put("/{ticket_id}/open")
def open_ticket():
    result = controller.open_ticket(ticket_id)
    return result


@router.put("/{ticket_id}/close")
def close_ticket(ticket_id: str):
    result = controller.close_ticket(item_id)
    return result
