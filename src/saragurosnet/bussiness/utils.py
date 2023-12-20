from src.common.cases import MessageUseCases
from src.common.logger import Logger
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.types import MessageType


def say_error(ctx: Context, e: Exception | None = None):
    Logger.error("Unexpected error in decisions tree", e)
    MessageUseCases().send_message(MessageType.ERROR_UNKNOW, ctx.event_twilio.from_number, ctx.conversation.id)
    return False


def verify_button(ctx: Context, option: str):
    return ctx.event_twilio.button_text == option or ctx.event_twilio.body == option
