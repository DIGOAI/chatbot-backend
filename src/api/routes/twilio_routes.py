from typing import Annotated, cast

from fastapi import APIRouter, Depends

from src.api.dependencies.cache import CacheConversationTuple, ConversationCache
from src.chatbot.utils import get_phone_and_service
from src.common.cases import ConversationUseCases
from src.common.logger import Logger
from src.common.models import Conversation, ConversationStatus, TwilioWebHook
from src.common.models.responses import create_response
from src.common.services import TwilioService
from src.config import Config
from src.saragurosnet.bussiness import tree
from src.saragurosnet.bussiness.context import Context

router = APIRouter(prefix="/twilio", tags=["Twilio"])


@router.post("/hook")
def twilio_hook(webhook: Annotated[TwilioWebHook, Depends()]):
    conversations_cache = ConversationCache().get_cache()

    # Get client and assistant phone number with the service name
    client_phone, _ = get_phone_and_service(webhook.from_number)
    assistant_phone, _ = get_phone_and_service(webhook.to_number)

    conversation_cached = conversations_cache.get(client_phone)

    if conversation_cached is None or conversation_cached.conversation is not None and conversation_cached.conversation.status == ConversationStatus.CLOSED:
        new_conversation = ConversationUseCases().add_new_conversation(client_phone, assistant_phone)

        conversation_cached = CacheConversationTuple(
            client=None, conversation=new_conversation, last_state=None, next_state=None)

    if conversation_cached.conversation is None and conversation_cached.waithing_for == "attend_ticket":
        _twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                                Config.TWILIO_SENDER, webhook.from_number)
        _twilio.send_message(msg="Gracias por contactarnos, en breve un asesor se comunicará con usted.")

        return

    Logger.debug(f"Client cached: {webhook.from_number}")
    tree.context = Context(webhook, conversation_cached.client,
                           conversation_cached.last_state, cast(Conversation, conversation_cached.conversation))

    # Execute the tree actions with the context setted
    next_state = tree(conversation_cached.next_state)

    # Cache the client for the next request
    client_phone = client_phone

    Logger.debug(f"Caching client: {client_phone}")
    conversations_cache[client_phone] = CacheConversationTuple(
        conversation=tree.context.conversation,
        client=tree.context.client,
        last_state=tree.context.last_state,
        next_state=next_state,
    )


@router.get("/show-cache")
def show_cache():
    conversations_cache = ConversationCache().get_cache()
    return create_response(conversations_cache, "Actual conversation cache")


@router.delete("/clear-cache")
def clear_cache():
    conversations_cache = ConversationCache().get_cache()
    conversations_cache.clear()

    return create_response(conversations_cache, "Conversation cache cleared")
