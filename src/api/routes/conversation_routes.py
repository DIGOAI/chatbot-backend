from dataclasses import dataclass
from uuid import UUID

from fastapi import APIRouter, Depends

from src.api.middlewares import JWTBearer
from src.common.cases import ConversationUseCases
from src.common.models import (
    ConversationWithData,
    ConversationWithLastMessage,
    GenericResponse,
    create_response,
)


@dataclass
class ConversationResume:
    opened: int
    closed: int


router = APIRouter(prefix="/conversations", tags=["Conversations"], dependencies=[Depends(JWTBearer())])


@router.get("/", response_model=GenericResponse[list[ConversationWithLastMessage]])
def get_conversations(start: int = 0, end: int = 10):
    conversations = ConversationUseCases().get_conversations_with_last_message(start, end)

    return create_response(conversations, f"Conversations from {start} to {end}")


@router.get("/resume", response_model=GenericResponse[ConversationResume])
def get_conversation_resume():
    resume = ConversationUseCases().get_conversations_resume()

    return create_response(ConversationResume(resume.opened, resume.closed), "Conversation resume")


@router.get("/{conversation_id}", response_model=GenericResponse[ConversationWithData])
def get_conversation(conversation_id: UUID):
    conversation = ConversationUseCases().get_conversation_with_messages(conversation_id)

    return create_response(conversation, "Conversation found")


@router.put("/{conversation_id}")
def update_conversation():
    return {}


@router.delete("/{conversation_id}")
def delete_conversation(conversation_id: UUID):
    return {}
