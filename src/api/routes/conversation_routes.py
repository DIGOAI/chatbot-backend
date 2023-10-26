from dataclasses import dataclass
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.middlewares import JWTBearer
from src.common.models import Conversation, GenericResponse, Message, create_response
from src.common.models.conversation import ConversationStatus, ConversationWithData
from src.common.services.mock_data import clients as clients_mock
from src.common.services.mock_data import conversations as conversations_mock
from src.common.services.mock_data import messages as messages_mock

router = APIRouter(prefix="/conversations", tags=["Conversations"], dependencies=[Depends(JWTBearer())])


@dataclass
class ConversationResume:
    opened: int
    closed: int


@dataclass
class ConversationWithLastMessage:
    conversation: Conversation
    last_message: Message


@router.get("/", response_model=GenericResponse[list[Conversation]])
def get_conversations(limit: int = 10):
    conversations: list[ConversationWithLastMessage] = []

    for conversation_mock in conversations_mock[:limit]:
        last_message = next((m for m in messages_mock if m.conversation_id == conversation_mock.id))

        conversations.append(ConversationWithLastMessage(
            conversation=conversation_mock,
            last_message=last_message
        ))

    return create_response(conversations, f"Last {limit} conversations")


@router.get("/resume", response_model=GenericResponse[ConversationResume])
def get_conversation_resume():
    print("LLego aqui")
    opened = len([c for c in conversations_mock if c.status == ConversationStatus.OPENED])
    closed = len([c for c in conversations_mock if c.status == ConversationStatus.CLOSED])

    return create_response(ConversationResume(opened=opened, closed=closed), "Conversation resume")


@router.get("/{conversation_id}", response_model=GenericResponse[ConversationWithData])
def get_conversation(conversation_id: UUID):
    conversation = next((c for c in conversations_mock if c.id == conversation_id), None)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Conversation not found")

    conversation_with_data = ConversationWithData(**conversation.model_dump())
    conversation_with_data.messages = [m for m in messages_mock if m.conversation_id == conversation_id]
    conversation_with_data.messages.sort(key=lambda m: m.created_at)
    conversation_with_data.client = next((c for c in clients_mock if c.id == conversation.client_id), None)

    return create_response(conversation_with_data, "Conversation found")
