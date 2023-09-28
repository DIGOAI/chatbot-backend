from fastapi import APIRouter, Depends

from src.middlewares import APITokenAuth, JWTBearer
from src.middlewares.jwt_bearer import Role
from src.models import GenericResponse, Message, MessageInsert
from src.use_cases import get_last_messages, write_message

router = APIRouter(prefix="/message", tags=["Message"])


@router.get("/", response_model=GenericResponse[list[Message]], dependencies=[Depends(JWTBearer())])
def get_messages(limit: int = 10):
    return get_last_messages(limit)


@router.post("/", response_model=GenericResponse[Message], dependencies=[Depends(APITokenAuth())])
def save_message(message: MessageInsert):
    return write_message(message)
