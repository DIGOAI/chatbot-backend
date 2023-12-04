from fastapi import APIRouter, Depends

from src.api.middlewares import JWTBearer
from src.common.cases import MessageUseCases
from src.common.models import (
    GenericResponse,
    Message,
    MessageInsertWeb,
    create_response,
)

router = APIRouter(prefix="/message", tags=["Message"], dependencies=[Depends(JWTBearer())])


@router.get("/", response_model=GenericResponse[list[Message]])
def get_messages(limit: int = 10):
    messages = MessageUseCases().get_last_messages(limit)

    return create_response(messages, message=f"Last {limit} messages.")


@router.post("/send_message", response_model=GenericResponse[Message])
def send_message(message: MessageInsertWeb):
    message_sended = MessageUseCases().send_message_from_web(message)

    return create_response(message_sended, message="Message sended.")
