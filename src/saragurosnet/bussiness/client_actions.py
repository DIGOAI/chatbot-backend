from src.chatbot import ActionGroup, format_fullname
from src.common.cases import ChatGPTUseCases, MessageUseCases, OCRUseCases
from src.common.logger import Logger
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.utils import say_error
from src.saragurosnet.types import MessageType, OptionType

group = ActionGroup[Context]()


@group.add_action("2.0", condition=lambda ctx: ctx.last_state in ["0.2", "3.2"] and ctx.client != None and ctx.client.saraguros_id != None, next=["2.1", "2.2", "2.3"])
def say_welcome_client(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    client_fullname = format_fullname(ctx.client.names, ctx.client.lastnames)

    MessageUseCases().send_message(MessageType.WELCOME_CLIENT.format(name=client_fullname),
                                   ctx.event_twilio.from_number,
                                   ctx.conversation.id)

    ctx.last_state = id_func


@group.add_action("2.1", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.STATUS)
def service_status(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    pass


@group.add_action("2.2", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.PAYMENT, next=["2.2.1"])
def service_payment(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.PLEASE_SEND_YOUR_INVOICE.format(name=ctx.client.get_fullname()),
                                   ctx.event_twilio.from_number,
                                   ctx.conversation.id)

    ctx.last_state = id_func


@group.add_action("2.2.1", condition=lambda ctx: ctx.last_state == "2.2" and ctx.event_twilio.media_url != None, end=False, next="3.0")
def receive_invoice(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    if ctx.event_twilio.media_url is None:
        MessageUseCases().send_message(MessageType.PLEASE_SEND_YOUR_INVOICE.format(name=ctx.client.get_fullname()),
                                       ctx.event_twilio.from_number, ctx.conversation.id)
        return "2.2.1", True

    if ctx.event_twilio.media_content_type in ["image/jpeg", "image/png"]:
        MessageUseCases().send_message(MessageType.PLEASE_SEND_CORRECT_INVOICE_FORMAT.format(name=ctx.client.get_fullname()),
                                       ctx.event_twilio.from_number, ctx.conversation.id)
        return "2.2.1", True

    try:
        MessageUseCases().send_message(MessageType.YOUR_INVOICE_IS_BEING_PROCESSED.format(name=ctx.client.get_fullname()),
                                       ctx.event_twilio.from_number, ctx.conversation.id)

        text, _ = OCRUseCases().extract_data_from_receibe(ctx.event_twilio.media_url)
        data_extracted = ChatGPTUseCases().ask_receibe_data(text)

        Logger.debug(f"OCR data extracted: {data_extracted}")

        MessageUseCases().send_message(f"OCR data extracted: {data_extracted}",
                                       ctx.event_twilio.from_number, ctx.conversation.id)

        MessageUseCases().send_message(MessageType.YOUR_INVOICE_IS_VALID.format(name=ctx.client.get_fullname()),
                                       ctx.event_twilio.from_number, ctx.conversation.id)

        # TODO: Save the invoice data in the database

        ctx.last_state = id_func
        return "3.0", False

    except Exception as e:
        MessageUseCases().send_message(MessageType.YOUR_INVOICE_IS_INVALID.format(name=ctx.client.get_fullname()),
                                       ctx.event_twilio.from_number, ctx.conversation.id)

        Logger.error("Unexpected error in decisions tree", e)

        ctx.last_state = id_func
        return "2.2.1", True


@group.add_action("2.3", condition=lambda ctx: ctx.last_state == "2.0" and ctx.event_twilio.body == OptionType.SUPPORT)
def service_support(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)
    pass
