from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException

from src.api.cases import get_last_messages, write_message
from src.api.middlewares import APITokenAuth, JWTBearer
from src.common.models import GenericResponse, Message, MessageInsert, create_response
from src.common.services.mock_data import messages as mock_messages

router = APIRouter(prefix="/message", tags=["Message"])


@router.get("/", response_model=GenericResponse[list[Message]], dependencies=[Depends(JWTBearer())])
def get_messages(limit: int = 10):
    # return get_last_messages(limit)

    messages = mock_messages.copy()
    messages.sort(key=lambda m: m.created_at)

    return create_response(messages[:limit], message=f"Last {limit} messages.")


@router.post("/", response_model=GenericResponse[Message], dependencies=[Depends(APITokenAuth())])
def save_message(message: MessageInsert):
    return write_message(message)


@router.post("/messages/send", dependencies=[Depends(APITokenAuth())])
def send_message(client_id: Annotated[str, Body(...)], message: Annotated[str, Body(...)]):
    raise HTTPException(status_code=501, detail="Not implemented")
