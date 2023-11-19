from src.chatbot.decisions_tree import DecisionsTree
from src.chatbot.utils import format_fullname
from src.common.cases import ConversationUseCases, MessageUseCases
from src.common.logger import Logger
from src.common.services import TwilioService
from src.config import Config
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.initial_actions import group as initial_group
from src.saragurosnet.bussiness.preactions import group as pre_group
from src.saragurosnet.bussiness.types import MediaUrlType, MessageType, OptionType

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
tree.register_action_group(pre_group)
# === End pre actions ===

# === Initial actions ===
tree.register_action_group(initial_group)
# === End initial actions ===


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
