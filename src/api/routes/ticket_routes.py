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
    items = controller.list(limit, offset)
    return items


@router.get("/{ticket_id}", response_model=GenericResponse[Ticket])
def get_ticket(ticket_id: int):
    item = controller.get(ticket_id)
    return item


@router.post("/")
def create_ticket(form: TicketInsert):
    item = controller.add(form.dict())
    return item


@router.put("/{ticket_id}")
def update_ticket(ticket_id: int, form: TicketInsert):
    item = controller.update(ticket_id, form.dict())
    return item


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):
    result = controller.delete(ticket_id)
    return result
