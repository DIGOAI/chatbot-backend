from datetime import datetime, timezone
from typing import Any, cast

from src.chatbot.decisions_tree import DecisionsTree
from src.chatbot.utils import format_fullname, get_ci_or_ruc, get_phone_and_service
from src.common.cases import ConversationUseCases, MessageUseCases
from src.common.logger import Logger
from src.common.models import MessageInsert
from src.common.services import SaragurosNetService, TwilioService
from src.config import Config
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.types import MediaUrlType, MessageType, OptionType
from src.saragurosnet.cases import ClientUseCases, GetClientByPhone

tree = DecisionsTree[Context]()

twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                       Config.TWILIO_SENDER, '')

# === Util functions ===


def say_error(ctx: Context):
    Logger.error("Client is None")
    MessageUseCases().send_message(MessageType.ERROR_CLIENT_NOT_FOUND, ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=ctx.event_twilio.from_number)
    return False
# === End util functions ===


# === Pre actions ===
@tree.add_preaction()
def pre_action(ctx: Context):
    Logger.info(f"Pre action: {ctx.last_state}")

    sender_phone, _ = get_phone_and_service(ctx.event_twilio.from_number)
    receiver_phone, _ = get_phone_and_service(ctx.event_twilio.to_number)

    # Save the message in the database
    message_cases = MessageUseCases()
    new_message = MessageInsert(
        id=ctx.event_twilio.message_sid,
        sender=sender_phone,
        receiver=receiver_phone,
        message=ctx.event_twilio.body,
        media_url=ctx.event_twilio.media_url,
        conversation_id=ctx.conversation.id
    )

    message_saved = message_cases.add_new_message(new_message)

    if message_saved:
        Logger.info(f"Message saved: {new_message.id}")

        # Update the conversation last message id
        conversation_cases = ConversationUseCases()
        conversation_updated = conversation_cases.update_last_message_id(ctx.conversation, new_message.id)

        ctx.conversation = conversation_updated
# === End pre actions ===


@tree.add_action("0.0", condition=lambda ctx: False, end=False)
def load_context(ctx: Context, id_func: str):
    Logger.info("Loading context")

    # Instace the services
    get_client_by_phone = GetClientByPhone()

    # Get the client phone number in +5939XXXXXXXXX format and service name exp: twilio
    client_phone, _ = get_phone_and_service(ctx.event_twilio.from_number)

    user = get_client_by_phone(client_phone)

    if not user:
        Logger.warn(f"User doesn't exists: {client_phone}")
        MessageUseCases().send_message(MessageType.ERROR_CLIENT_NOT_FOUND, ctx.event_twilio.from_number, ctx.conversation.id)
        # twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=ctx.event_twilio.from_number)

        return False

    hours_diff = int((datetime.now(timezone.utc) - user.updated_at).seconds / 3600)

    Logger.info(
        f"Context loaded: [ ID: {user.id} | CI: {user.ci} | Phone: {user.phone} | Status: {ctx.last_state} | Hours: {hours_diff}]")

    ctx.client = user

    # return False  # TODO: Delete this line when the backend is ready


@tree.add_action("0.1", condition=lambda ctx: ctx.last_state == None or ctx.last_state == "3.1", next="0.2")
def say_welcome(ctx: Context, id_func: str):
    MessageUseCases().send_message(MessageType.SAY_HELLO, ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.SAY_HELLO, receiver=ctx.event_twilio.from_number)
    ctx.last_state = id_func


@tree.add_action("0.2", condition=lambda ctx: ctx.last_state == "0.1", end=False, next=["1.0", "2.0"])
def search_saraguros_client(ctx: Context, id_func: str):
    Logger.info("Searching if the client is a saraguros client")

    try:
        client_ci = get_ci_or_ruc(ctx.event_twilio.body)
        Logger.info(f"Client CI: {client_ci}")

        # Get the client phone number in +5939XXXXXXXXX format and service name exp: twilio
        client_phone, _ = get_phone_and_service(ctx.event_twilio.from_number)

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

        conversation_updated = ConversationUseCases().update_client_id(ctx.conversation, user)

        ctx.client = user
        ctx.last_state = id_func
        ctx.conversation = conversation_updated

    except ValueError as e:
        Logger.warn(str(e))
        MessageUseCases().send_message(MessageType.ERROR_INVALID_CI, ctx.event_twilio.from_number, ctx.conversation.id)
        # twilio.send_message(MessageType.ERROR_INVALID_CI, receiver=ctx.event_twilio.from_number)

        ctx.last_state = None

    except (KeyError, IndexError) as e:
        Logger.error(f'Error getting client data from SaragurosNet API: {e} key | index')
        MessageUseCases().send_message(MessageType.ERROR_CLIENT_NOT_FOUND, ctx.event_twilio.from_number, ctx.conversation.id)
        # twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=ctx.event_twilio.from_number)

        ctx.last_state = None


@tree.add_action("1.0", condition=lambda ctx: ctx.last_state == "0.2" and ctx.client != None and ctx.client.saraguros_id == None, next=["1.1", "1.2", "1.3"])
def say_welcome_unknown(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.WELCOME_UNKNOW.format(
        name="Cliente"), ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.WELCOME_UNKNOW.format(name="Cliente"), receiver="whatsapp:" + ctx.client.phone)

    ctx.last_state = id_func


@tree.add_action("1.1", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None and (ctx.event_twilio.button_text == OptionType.PROMOTIONS or ctx.event_twilio.body == OptionType.PROMOTIONS), end=False, next="3.0")
def send_promotions(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.PROMOTIONS, ctx.event_twilio.from_number,
                                   ctx.conversation.id, media_url=MediaUrlType.PROMOTIONS)

    # twilio.send_message(MessageType.PROMOTIONS,
    #                     receiver="whatsapp:" + ctx.client.phone,
    #                     media_url=MediaUrlType.PROMOTIONS)

    # fullname = format_fullname(ctx.client.names, ctx.client.lastnames)
    # say_goodbye(fullname, "whatsapp:" + ctx.client.phone)
    ctx.last_state = id_func


@tree.add_action("1.2", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None and (ctx.event_twilio.button_text == OptionType.COVERAGES or ctx.event_twilio.body == OptionType.COVERAGES), end=False, next="3.0")
def send_coverages(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.COVERAGES, ctx.event_twilio.from_number,
                                   ctx.conversation.id, media_url=MediaUrlType.COVERAGES)

    # twilio.send_message(MessageType.COVERAGES,
    #                     receiver="whatsapp:" + ctx.client.phone,
    #                     media_url=MediaUrlType.COVERAGES)

    # fullname = format_fullname(ctx.client.names, ctx.client.lastnames)
    # say_goodbye(fullname, "whatsapp:" + ctx.client.phone)
    ctx.last_state = id_func


@tree.add_action("1.3", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None and (ctx.event_twilio.button_text == OptionType.AGENT or ctx.event_twilio.body == OptionType.AGENT))
def talk_with_agent(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    fullname = format_fullname(ctx.client.names, ctx.client.lastnames)

    MessageUseCases().send_message(MessageType.CONNECT_AGENT.format(
        name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.CONNECT_AGENT.format(name=fullname), receiver="whatsapp:" + ctx.client.phone)

    # TODO: Generar ticket de atencion al cliente
    # TODO: Crear nuevo usuario en microwisp para tener su ID
    # TODO: Enviar notificacion al agente con el ID del usuario


@tree.add_action("2.0", condition=lambda ctx: ctx.last_state == "0.2" and ctx.client != None and ctx.client.saraguros_id != None)
def say_welcome_client(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    fullname = format_fullname(ctx.client.names, ctx.client.lastnames)

    MessageUseCases().send_message(MessageType.WELCOME_CLIENT.format(
        name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.WELCOME_CLIENT.format(name=fullname), receiver="whatsapp:" + ctx.client.phone)


@tree.add_action("2.1", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.STATUS)
def service_status(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    pass


@tree.add_action("2.2", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.PAYMENT)
def service_payment(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@tree.add_action("2.2.1", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.TRANSACTION)
def payment_transaction(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@tree.add_action("2.2.2", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.CARD)
def payment_card(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@tree.add_action("2.2.3", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.CASH)
def payment_cash(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@tree.add_action("2.3", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.SUPPORT)
def service_support(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@tree.add_action("3.0", condition=lambda ctx: ctx.last_state in ["1.1", "1.2"], next="3.1")
def end_conversation(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    fullname = format_fullname(ctx.client.names, ctx.client.lastnames)
    fullname = fullname if fullname != "" else "Cliente"

    MessageUseCases().send_message(MessageType.END_CONVERSATION.format(
        name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.END_CONVERSATION.format(name=fullname), receiver="whatsapp:" + ctx.client.phone)
    ctx.last_state = id_func


@tree.add_action("3.1", condition=lambda ctx: ctx.last_state == "3.0" and ctx.event_twilio.body == OptionType.END)
def say_goodbye(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.SAY_GOODBAY, ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.SAY_GOODBAY, receiver="whatsapp:" + ctx.client.phone)

    # TODO: End conversation and update th db
    conversation = ConversationUseCases().end_conversation(ctx.conversation)

    ctx.last_state = id_func
    ctx.client = None
    ctx.conversation = conversation


@tree.add_action("3.2", condition=lambda ctx: ctx.last_state == "3.0" and ctx.event_twilio.body == OptionType.ANOTHER)
def another_question(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    if ctx.client.saraguros_id:
        # Return to say_welcome_client
        pass
    else:
        # Return to say_welcome_unknown
        pass
