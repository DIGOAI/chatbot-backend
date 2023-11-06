from fastapi import APIRouter

router = APIRouter(prefix="/tickets", tags=["Tickets"])


@router.get("/")
def get_tickets(limit: int = 30, offset: int = 0):
    return []


@router.get("/{ticket_id}")
def get_ticket(ticket_id: int):
    return {}


@router.post("/")
def create_ticket():
    return {}


@router.put("/{ticket_id}")
def update_ticket(ticket_id: int):
    return {}


@router.delete("/{ticket_id}")
def delete_ticket(ticket_id: int):
    return {}
