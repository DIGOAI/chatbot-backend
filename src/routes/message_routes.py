from fastapi import APIRouter

from src.models import GenericResponse, Message, MessageInsert
from src.use_cases import get_last_messages, write_message

router = APIRouter(prefix="/message", tags=["Message"])


@router.get("/", response_model=GenericResponse[list[Message]])
def get_messages(limit: int = 10):
    return get_last_messages(limit)


@router.post("/", response_model=GenericResponse[Message])
def save_message(message: MessageInsert):
    return write_message(message)
