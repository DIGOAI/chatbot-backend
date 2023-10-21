from datetime import datetime, timezone
from typing import Any, cast

from src.chatbot.decisions_tree import DecisionsTree
from src.chatbot.utils import format_fullname, get_ci_or_ruc, get_phone_and_service
from src.common.logger import Logger
from src.common.services import SaragurosNetService, TwilioService
from src.config import Config
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.types import MediaUrlType, MessageType, OptionType
from src.saragurosnet.cases import ClientUseCases, GetClientByPhone

tree = DecisionsTree[Context]()

twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                       Config.TWILIO_SENDER, '')


# === Util functions ===
def say_goodbye(name: str, receiver: str):
    twilio.send_message(MessageType.END_CONVERSATION.format(name=name), receiver=receiver)


def say_error(ctx: Context):
    Logger.error("Client is None")
    twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=ctx.event_twilio.from_number)
    return False
# === End util functions ===


@tree.add_action("0.0", condition=lambda ctx: False, end=False)
def load_context(context: Context, id_func: str):
    Logger.info("Loading context")

    # Instace the services
    get_client_by_phone = GetClientByPhone()

    # Get the client phone number in +5939XXXXXXXXX format and service name exp: twilio
    client_phone, _ = get_phone_and_service(context.event_twilio.from_number)

    user = get_client_by_phone(client_phone)

    if not user:
        Logger.warn(f"User doesn't exists: {client_phone}")
        twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=context.event_twilio.from_number)

        return False

    hours_diff = int((datetime.now(timezone.utc) - user.updated_at).seconds / 3600)

    Logger.info(
        f"Context loaded: [ ID: {user.id} | CI: {user.ci} | Phone: {user.phone} | Status: {context.last_state} | Hours: {hours_diff}]")

    context.client = user

    # return False  # TODO: Delete this line when the backend is ready


@tree.add_action("0.1", condition=lambda ctx: ctx.last_state == None)
def say_welcome(context: Context, id_func: str):
    twilio.send_message(MessageType.SAY_HELLO, receiver=context.event_twilio.from_number)
    context.last_state = id_func


@tree.add_action("0.2", condition=lambda ctx: ctx.last_state == "0.1", end=False)
def search_saraguros_client(context: Context, id_func: str):
    Logger.info("Searching if the client is a saraguros client")

    try:
        client_ci = get_ci_or_ruc(context.event_twilio.body)
        Logger.info(f"Client CI: {client_ci}")

        # Get the client phone number in +5939XXXXXXXXX format and service name exp: twilio
        client_phone, _ = get_phone_and_service(context.event_twilio.from_number)

        # Instace the services
        client_cases = ClientUseCases()
        user = client_cases.get_client_by_ci(client_ci, client_phone)

        # If the user is not a saraguros client then search in the SaragurosNet API
        if user.saraguros_id is None:
            Logger.info("Updating user data with SaragurosNet API info")

            saraguros_api = SaragurosNetService(Config.SARAGUROS_API_TOKEN)
            client_data = saraguros_api.get_client_data(client_ci)

            print(client_data)

            if client_data is not None:
                status = client_data["estado"]

                if status != "error":
                    client_data = cast(dict[str, Any], client_data["datos"][0])

                    user.saraguros_id = client_data["id"]
                    user.names = client_data["nombre"]
                    user.phone = client_data["movil"]

        context.client = user
        context.last_state = id_func

    except ValueError as e:
        Logger.warn(str(e))
        twilio.send_message(MessageType.ERROR_INVALID_CI, receiver=context.event_twilio.from_number)

        context.last_state = None

    except (KeyError, IndexError) as e:
        Logger.error(f'Error getting client data from SaragurosNet API: {e} key | index')
        twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=context.event_twilio.from_number)

        context.last_state = None


@tree.add_action("1.0", condition=lambda ctx: ctx.last_state == "0.2" and ctx.client != None and ctx.client.saraguros_id == None)
def say_welcome_unknown(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)

    twilio.send_message(MessageType.WELCOME_UNKNOW.format(name="Cliente"), receiver="whatsapp:" + context.client.phone)

    context.last_state = id_func


@tree.add_action("1.1", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None)
def send_promotions(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)

    twilio.send_message(MessageType.PROMOTIONS,
                        receiver="whatsapp:" + context.client.phone,
                        media_url=MediaUrlType.PROMOTIONS)

    fullname = format_fullname(context.client.names, context.client.lastnames)
    say_goodbye(fullname, "whatsapp:" + context.client.phone)
    context.last_state = id_func


@tree.add_action("1.2", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None)
def send_coverages(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)

    twilio.send_message(MessageType.COVERAGES,
                        receiver="whatsapp:" + context.client.phone,
                        media_url=MediaUrlType.COVERAGES)

    fullname = format_fullname(context.client.names, context.client.lastnames)
    say_goodbye(fullname, "whatsapp:" + context.client.phone)
    context.last_state = id_func


@tree.add_action("1.3", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None)
def talk_with_agent(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)

    fullname = format_fullname(context.client.names, context.client.lastnames)
    twilio.send_message(MessageType.CONNECT_AGENT.format(name=fullname), receiver="whatsapp:" + context.client.phone)

    # TODO: Generar ticket de atencion al cliente
    # TODO: Crear nuevo usuario en microwisp para tener su ID
    # TODO: Enviar notificacion al agente con el ID del usuario


@tree.add_action("2.0", condition=lambda ctx: ctx.last_state == "0.2" and ctx.client != None and ctx.client.saraguros_id != None)
def say_welcome_client(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)

    fullname = format_fullname(context.client.names, context.client.lastnames)
    twilio.send_message(MessageType.WELCOME_CLIENT.format(name=fullname), receiver="whatsapp:" + context.client.phone)


@tree.add_action("2.1", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.STATUS)
def service_status(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)

    pass


@tree.add_action("2.2", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.PAYMENT)
def service_payment(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)
    pass


@tree.add_action("2.2.1", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.TRANSACTION)
def payment_transaction(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)
    pass


@tree.add_action("2.2.2", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.CARD)
def payment_card(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)
    pass


@tree.add_action("2.2.3", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.CASH)
def payment_cash(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)
    pass


@tree.add_action("2.3", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.SUPPORT)
def service_support(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)
    pass


@tree.add_action("3.0", condition=lambda ctx: ctx.last_state in ["1.1", "1.2"] and ctx.event_twilio.body == OptionType.END)
def end_conversation(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)

    twilio.send_message(MessageType.SAY_GOODBAY, receiver="whatsapp:" + context.client.phone)
    context.last_state = None
    context.client = None


@tree.add_action("3.1", condition=lambda ctx: ctx.last_state in ["1.1", "1.2"] and ctx.event_twilio.body == OptionType.ANOTHER)
def another_question(context: Context, id_func: str):
    if context.client is None:
        return say_error(context)

    if context.client.saraguros_id:
        # Return to say_welcome_client
        pass
    else:
        # Return to say_welcome_unknown
        pass
