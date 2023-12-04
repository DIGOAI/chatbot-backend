from src.common.cases import MessageUseCases
from src.common.logger import Logger
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.types import MessageType


def say_error(ctx: Context):
    Logger.error("Client in context is None")
    MessageUseCases().send_message(MessageType.ERROR_CLIENT_NOT_FOUND, ctx.event_twilio.from_number, ctx.conversation.id)
    return False


def verify_button(ctx: Context, option: str):
    return ctx.event_twilio.button_text == option or ctx.event_twilio.body == option
