from fastapi import APIRouter, Depends, HTTPException

from src.api.middlewares import JWTBearer
from src.common.cases import MessageUseCases
from src.common.models import GenericResponse, Message, MessageInsert, create_response

router = APIRouter(prefix="/message", tags=["Message"], dependencies=[Depends(JWTBearer())])


@router.get("/", response_model=GenericResponse[list[Message]])
def get_messages(limit: int = 10):
    messages = MessageUseCases().get_last_messages(limit)

    return create_response(messages, message=f"Last {limit} messages.")


@router.post("/send_message", response_model=GenericResponse[Message])
def send_message(message: MessageInsert):
    # message_is_created = MessageUseCases().add_new_message(message)
    # return write_message(message)
    raise HTTPException(status_code=501, detail="Not implemented")
