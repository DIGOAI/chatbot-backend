from datetime import datetime, timezone

from src.chatbot.decisions_tree import DecisionsTree
from src.chatbot.utils import format_fullname, get_ci_or_ruc, get_phone_and_service
from src.common.logger import Logger
from src.common.services import BackendService, TwilioService
from src.config import Config
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.types import MediaUrlType, MessageType, OptionType

tree = DecisionsTree[Context]()

twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                       Config.TWILIO_SENDER, '')


def say_goodbye(name: str, receiver: str):
    twilio.send_message(MessageType.END_CONVERSATION.format(name=name), receiver=receiver)


@tree.add_action("0.0", condition=lambda _: True, end=False)
def load_context(context: Context):
    Logger.info("Loading context")

    # Instace the services
    backend = BackendService(Config.BACKEND_URL, Config.X_API_KEY)

    # Get the client phone number in +5939XXXXXXXXX format and service name exp: twilio
    client_phone, _ = get_phone_and_service(context.event_twilio.from_number)

    user = backend.get_user_by_phone(client_phone)

    if not user:
        Logger.warn(f"User doesn't exists: {client_phone}")
        twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=context.event_twilio.from_number)

        return False

    hours_diff = int((datetime.now(timezone.utc) - user.updated_at).seconds / 3600)

    Logger.info(
        f"Context loaded: [ ID: {user.id} | CI: {user.ci} | Phone: {user.phone} | Status: {user.last_state} | Hours: {hours_diff}]")

    context.client = user

    # return False  # TODO: Delete this line when the backend is ready


@tree.add_action("0.1", condition=lambda ctx: ctx.client.last_state == None)
def say_welcome(context: Context):
    twilio.send_message(MessageType.SAY_HELLO, receiver="whatsapp:" + context.client.phone)


@tree.add_action("0.2", condition=lambda ctx: ctx.client.last_state == "0.1")
def search_saraguros_client(context: Context):
    Logger.info("Searching saraguros client")

    try:
        client_ci = get_ci_or_ruc(context.event_twilio.body)
        Logger.info(f"Client CI: {client_ci}")

        backend = BackendService(Config.BACKEND_URL, Config.X_API_KEY)

        user = backend.get_saraguros_data_from_ci(client_ci)

        if not user:
            Logger.warn(f"User doesn't exists: {client_ci}")
            twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=context.event_twilio.from_number)

            return False

        Logger.info("Updating user data")

        context.client.ci = user.ci
        context.client.names = user.names
        context.client.lastnames = user.lastnames
        context.client.saraguros_id = user.saraguros_id

    except ValueError as e:
        Logger.warn(str(e))
        twilio.send_message(MessageType.ERROR_INVALID_CI, receiver=context.event_twilio.from_number)
        return


@tree.add_action("1.0", condition=lambda ctx: ctx.client.last_state == "0.2" and ctx.client.saraguros_id == None)
def say_welcome_unknown(context: Context):
    twilio.send_message(MessageType.WELCOME_UNKNOW, receiver="whatsapp:" + context.client.phone)


@tree.add_action("1.1", condition=lambda ctx: ctx.client.last_state == "0.2" and ctx.client.saraguros_id == None)
def send_promotions(context: Context):
    twilio.send_message(MessageType.PROMOTIONS,
                        receiver="whatsapp:" + context.client.phone,
                        media_url=MediaUrlType.PROMOTIONS)

    fullname = format_fullname(context.client.names, context.client.lastnames)
    say_goodbye(fullname, "whatsapp:" + context.client.phone)


@tree.add_action("1.2", condition=lambda ctx: ctx.client.last_state == "0.2" and ctx.client.saraguros_id == None)
def send_coverages(context: Context):
    twilio.send_message(MessageType.COVERAGES,
                        receiver="whatsapp:" + context.client.phone,
                        media_url=MediaUrlType.COVERAGES)

    fullname = format_fullname(context.client.names, context.client.lastnames)
    say_goodbye(fullname, "whatsapp:" + context.client.phone)


@tree.add_action("1.3", condition=lambda ctx: ctx.client.last_state == "0.2" and ctx.client.saraguros_id == None)
def talk_with_agent(context: Context):
    fullname = format_fullname(context.client.names, context.client.lastnames)
    twilio.send_message(MessageType.CONNECT_AGENT.format(name=fullname), receiver="whatsapp:" + context.client.phone)

    # TODO: Generar ticket de atencion al cliente
    # TODO: Crear nuevo usuario en microwisp para tener su ID
    # TODO: Enviar notificacion al agente con el ID del usuario


@tree.add_action("2.0", condition=lambda ctx: ctx.client.last_state == "0.2" and ctx.client.saraguros_id != None)
def say_welcome_client(context: Context):
    fullname = format_fullname(context.client.names, context.client.lastnames)
    twilio.send_message(MessageType.WELCOME_CLIENT.format(name=fullname), receiver="whatsapp:" + context.client.phone)


@tree.add_action("2.1", condition=lambda ctx: ctx.client.last_state == "2.0" and ctx.event_twilio.body == OptionType.STATUS)
def service_status(context: Context):
    pass


@tree.add_action("2.2", condition=lambda ctx: ctx.client.last_state == "2.0" and ctx.event_twilio.body == OptionType.PAYMENT)
def service_payment(context: Context):
    pass


@tree.add_action("2.2.1", condition=lambda ctx: ctx.client.last_state == "2.2" and ctx.event_twilio.body == OptionType.TRANSACTION)
def payment_transaction(context: Context):
    pass


@tree.add_action("2.2.2", condition=lambda ctx: ctx.client.last_state == "2.2" and ctx.event_twilio.body == OptionType.CARD)
def payment_card(context: Context):
    pass


@tree.add_action("2.2.3", condition=lambda ctx: ctx.client.last_state == "2.2" and ctx.event_twilio.body == OptionType.CASH)
def payment_cash(context: Context):
    pass


@tree.add_action("2.3", condition=lambda ctx: ctx.client.last_state == "2.0" and ctx.event_twilio.body == OptionType.SUPPORT)
def service_support(context: Context):
    pass


@tree.add_action("3.0", condition=lambda ctx: ctx.client.last_state in ["1.1", "1.2"] and ctx.event_twilio.body == OptionType.END)
def end_conversation(context: Context):
    twilio.send_message(MessageType.SAY_GOODBAY, receiver="whatsapp:" + context.client.phone)


@tree.add_action("3.1", condition=lambda ctx: ctx.client.last_state in ["1.1", "1.2"] and ctx.event_twilio.body == OptionType.ANOTHER)
def another_question(context: Context):
    if context.client.saraguros_id:
        # Return to say_welcome_client
        pass
    else:
        # Return to say_welcome_unknown
        pass
