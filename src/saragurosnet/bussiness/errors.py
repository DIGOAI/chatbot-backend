from src.common.cases import MessageUseCases
from src.common.logger import Logger
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.types import MessageType


def say_error(ctx: Context):
    Logger.error("Client is None")
    MessageUseCases().send_message(MessageType.ERROR_CLIENT_NOT_FOUND, ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.ERROR_CLIENT_NOT_FOUND, receiver=ctx.event_twilio.from_number)
    return False
