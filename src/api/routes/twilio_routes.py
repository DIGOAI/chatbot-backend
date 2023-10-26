from dataclasses import dataclass
from typing import Annotated

from fastapi import APIRouter, Depends

from src.chatbot.utils import get_phone_and_service
from src.common.cases import ConversationUseCases
from src.common.logger import Logger
from src.common.models import Client, Conversation, ConversationStatus, TwilioWebHook
from src.saragurosnet.bussiness import Context, tree

router = APIRouter(prefix="/twilio", tags=["Twilio"])


@dataclass
class CacheConversationTuple():
    conversation: Conversation
    client: Client | None = None
    last_state: str | None = None
    next_state: str | list[str] | None = None


# TODO: Upgrade this cache for support only 100 clients and delete the old ones
conversations_cache: dict[str, CacheConversationTuple] = {}


@router.post("/hook")
def twilio_hook(webhook: Annotated[TwilioWebHook, Depends()]):
    global conversations_cache  # Use the global clients cache

    # Get client and assistant phone number with the service name
    client_phone, _ = get_phone_and_service(webhook.from_number)
    assistant_phone, _ = get_phone_and_service(webhook.to_number)

    conversation_cached = conversations_cache.get(client_phone)

    if conversation_cached is None or conversation_cached.conversation.status == ConversationStatus.CLOSED:
        new_conversation = ConversationUseCases().add_new_conversation(client_phone, assistant_phone)

        conversation_cached = CacheConversationTuple(
            client=None, conversation=new_conversation, last_state=None, next_state=None)

    Logger.info(f"Client cached: {webhook.from_number}")
    tree.context = Context(webhook, conversation_cached.client,
                           conversation_cached.last_state, conversation_cached.conversation)

    # Execute the tree actions with the context setted
    next_state = tree(conversation_cached.next_state)

    # Cache the client for the next request
    client_phone = client_phone

    Logger.info(f"Caching client: {client_phone}")
    conversations_cache[client_phone] = CacheConversationTuple(
        conversation=tree.context.conversation,
        client=tree.context.client,
        last_state=tree.context.last_state,
        next_state=next_state,
    )


@router.get("/show-cache")
def show_cache():
    global conversations_cache

    return conversations_cache
