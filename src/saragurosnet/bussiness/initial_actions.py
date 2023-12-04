from datetime import datetime, timezone
from typing import Any, cast

from src.chatbot import ActionGroup, get_ci_or_ruc, get_phone_and_service
from src.common.cases import ClientUseCases, ConversationUseCases, MessageUseCases
from src.common.logger import Logger
from src.common.services import SaragurosNetService
from src.config import Config
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.types import MessageType

group = ActionGroup[Context]()


@group.add_action("0.0", condition=lambda ctx: False, end=False)
def load_context(ctx: Context, id_func: str):
    Logger.debug("Loading context")

    # Get the client phone number in +5939XXXXXXXXX format and service name exp: twilio
    client_phone, _ = get_phone_and_service(ctx.event_twilio.from_number)

    user = ClientUseCases().get_client_by_phone(client_phone)

    if not user:
        Logger.alert(f"User doesn't exists: {client_phone}")
        MessageUseCases().send_message(MessageType.ERROR_CLIENT_NOT_FOUND, ctx.event_twilio.from_number, ctx.conversation.id)

        return False

    hours_diff = int((datetime.now(timezone.utc) - user.updated_at).seconds / 3600)

    Logger.debug(
        f"Context loaded: [ ID: {user.id} | CI: {user.ci} | Phone: {user.phone} | Status: {ctx.last_state} | Hours: {hours_diff}]")

    ctx.client = user

    # return False  # TODO: Delete this line when the backend is ready


@group.add_action("0.1", condition=lambda ctx: ctx.last_state == None or ctx.last_state == "3.1", next="0.2")
def say_welcome(ctx: Context, id_func: str):
    MessageUseCases().send_message(MessageType.SAY_HELLO, ctx.event_twilio.from_number, ctx.conversation.id)

    ctx.last_state = id_func


@group.add_action("0.2", condition=lambda ctx: ctx.last_state == "0.1" or ctx.last_state == "0.2", end=False, next=["1.0", "2.0"])
def search_saraguros_client(ctx: Context, id_func: str):
    Logger.debug("Searching if the client is a saraguros client")

    try:
        client_ci = get_ci_or_ruc(ctx.event_twilio.body)
        Logger.debug(f"Client CI: {client_ci}")

        # Get the client phone number in +5939XXXXXXXXX format and service name exp: twilio
        client_phone, _ = get_phone_and_service(ctx.event_twilio.from_number)

        # Instace the services
        user = ClientUseCases().get_client_by_ci(client_ci, client_phone)

        # If the user is not a saraguros client then search in the SaragurosNet API
        if user.saraguros_id is None:
            Logger.debug("Updating user data with SaragurosNet API info")

            saraguros_api = SaragurosNetService(Config.SARAGUROS_API_TOKEN)
            client_data = saraguros_api.get_client_data(client_ci)

            Logger.debug(f"Client data: {client_data}")

            if client_data is not None:
                status = client_data["estado"]

                if status != "error":
                    client_data = cast(dict[str, Any], client_data["datos"][0])

                    user.saraguros_id = client_data["id"]
                    user.names = client_data["nombre"]
                    user.phone = client_data["movil"]

        conversation_updated = ConversationUseCases().update_client_id(ctx.conversation, user)

        ctx.client = user
        ctx.last_state = id_func
        ctx.conversation = conversation_updated

    except ValueError as e:
        Logger.alert(str(e))
        MessageUseCases().send_message(MessageType.ERROR_INVALID_CI, ctx.event_twilio.from_number, ctx.conversation.id)

        ctx.last_state = "0.2"

        return "0.2", True

    except (KeyError, IndexError) as e:
        Logger.error(f'Error getting client data from SaragurosNet API: {e} key | index', err=e)
        MessageUseCases().send_message(MessageType.ERROR_CLIENT_NOT_FOUND, ctx.event_twilio.from_number, ctx.conversation.id)

        ctx.last_state = None


@group.add_action("0.3", condition=lambda ctx: ctx.waiting_for == "attending_ticket")
def talk_in_ticket(ctx: Context, id_func: str):
    ctx.last_state = id_func
    return id_func, True
