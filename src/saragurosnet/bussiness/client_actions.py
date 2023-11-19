from src.chatbot import ActionGroup, format_fullname
from src.common.cases import MessageUseCases
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.errors import say_error
from src.saragurosnet.types import MessageType, OptionType

group = ActionGroup[Context]()


@group.add_action("2.0", condition=lambda ctx: ctx.last_state == "0.2" and ctx.client != None and ctx.client.saraguros_id != None)
def say_welcome_client(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    fullname = format_fullname(ctx.client.names, ctx.client.lastnames)

    MessageUseCases().send_message(MessageType.WELCOME_CLIENT.format(
        name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.WELCOME_CLIENT.format(name=fullname), receiver="whatsapp:" + ctx.client.phone)


@group.add_action("2.1", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.STATUS)
def service_status(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    pass


@group.add_action("2.2", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.PAYMENT)
def service_payment(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@group.add_action("2.2.1", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.TRANSACTION)
def payment_transaction(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@group.add_action("2.2.2", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.CARD)
def payment_card(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@group.add_action("2.2.3", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.body == OptionType.CASH)
def payment_cash(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass


@group.add_action("2.3", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.SUPPORT)
def service_support(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass
