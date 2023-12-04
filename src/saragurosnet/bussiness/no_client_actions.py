import time

from src.chatbot import ActionGroup
from src.common.cases import ClientUseCases, MessageUseCases, TicketUseCases
from src.common.logger import Logger
from src.common.models import TicketInsert, TicketStatus
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.utils import say_error, verify_button
from src.saragurosnet.types import MediaUrlType, MessageType, OptionType

group = ActionGroup[Context]()


@group.add_action("1.0", condition=lambda ctx: ctx.last_state in ["0.2", "3.2"] and ctx.client != None, next=["1.1", "1.2", "1.3"])
def say_welcome_unknown(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    client_fullname = ctx.client.get_fullname()

    MessageUseCases().send_message(MessageType.WELCOME_UNKNOW.format(
        name=client_fullname or "Cliente"), ctx.event_twilio.from_number, ctx.conversation.id)

    ctx.last_state = id_func


@group.add_action("1.1", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and verify_button(ctx, OptionType.PROMOTIONS), end=False, next="3.0")
def send_promotions(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.PROMOTIONS, ctx.event_twilio.from_number,
                                   ctx.conversation.id, media_url=MediaUrlType.PROMOTIONS)

    # Wait 5 seconds to send the next message
    time.sleep(5)

    ctx.last_state = id_func


@group.add_action("1.2", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and verify_button(ctx, OptionType.COVERAGES), end=False, next="3.0")
def send_coverages(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.COVERAGES, ctx.event_twilio.from_number,
                                   ctx.conversation.id, media_url=MediaUrlType.COVERAGES)

    # Wait 5 seconds to send the next message
    time.sleep(5)

    ctx.last_state = id_func


@group.add_action("1.3", condition=lambda ctx: (ctx.last_state == "1.0" and ctx.client != None and verify_button(ctx, OptionType.AGENT)) or ctx.last_state in ["1.3", "4.0", "4.1", "4.2", "4.3", "4.4"], end=False, next="3.0")
def talk_with_agent(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    body = ctx.event_twilio.body  # Get the body of the message

    # Request the client data if it is not complete
    if ctx.client.names is None:
        ctx.last_state = id_func
        ctx.event_twilio.body = ""
        ctx.waiting_for = "names"

        return "4.0", False

    if ctx.client.lastnames is None:
        ctx.last_state = id_func
        ctx.event_twilio.body = ""
        ctx.waiting_for = "lastnames"

        return "4.1", False

    if ctx.client.email is None:
        ctx.last_state = id_func
        ctx.event_twilio.body = ""
        ctx.waiting_for = "email"

        return "4.2", False

    # Update the client data in the database if it was modified
    if ctx.waiting_for == "update_data_client":
        client_updated = ClientUseCases().update_client(ctx.client)
        ctx.client = client_updated
        ctx.event_twilio.body = OptionType.AGENT
        ctx.waiting_for = None

    fullname = ctx.client.get_fullname()  # Get the client fullname

    if body and verify_button(ctx, OptionType.AGENT):
        MessageUseCases().send_message(MessageType.TELL_ME_YOUR_SUBJECT.format(
            name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)

        ctx.last_state = "1.3"
        return "1.3", True

    # Create a ticket for the client
    ticket = TicketInsert(
        subject=body.strip(),
        client_id=ctx.client.id,
        status=TicketStatus.WAITING,
    )

    try:
        ticket_created = TicketUseCases().create_ticket(ticket)
        Logger.debug(str(ticket_created))
        # Send a message to the client with the ticket ID if it was created successfully
        MessageUseCases().send_message(MessageType.CONNECT_AGENT, ctx.event_twilio.from_number, ctx.conversation.id)
        ctx.last_state = id_func

        return "3.3", False

    except Exception as e:
        Logger.error("Chatbot error creating ticket", e)
        MessageUseCases().send_message(MessageType.ERROR_UNKNOW, ctx.event_twilio.from_number, ctx.conversation.id)
        ctx.last_state = id_func
