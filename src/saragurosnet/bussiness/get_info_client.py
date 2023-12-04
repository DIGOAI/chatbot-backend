from src.chatbot import ActionGroup, get_email
from src.common.cases import MessageUseCases
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.utils import say_error
from src.saragurosnet.types import MessageType
from src.saragurosnet.types.option_types import OptionType

group = ActionGroup[Context]()

# TODO: Refactor this code to use the new ActionGroup for get the client info, and use the new Context class.


@group.add_action("4.0", lambda ctx: ctx.waiting_for == "names")
def get_names_data(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    body = ctx.event_twilio.body.strip()

    if body:
        ctx.client.names = body  # Set the client names
        ctx.event_twilio.body = OptionType.AGENT  # Reset the body
        ctx.last_state = id_func  # Set the last state
        ctx.waiting_for = "update_data_client"  # Set the waiting for value to update the client data

        return "1.3", False  # Return the next state

    else:
        # Send a message to the client asking for the names
        MessageUseCases().send_message(
            MessageType.TELL_ME_YOUR_NAMES.format(name='Cliente'),
            ctx.event_twilio.from_number, ctx.conversation.id
        )

        ctx.last_state = id_func  # Set the last state

        return id_func, True  # Return the same state


@group.add_action("4.1", lambda ctx: ctx.waiting_for == "lastnames")
def get_lastnames_data(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    body = ctx.event_twilio.body.strip()

    if body:
        ctx.client.lastnames = body  # Set the client lastnames
        ctx.event_twilio.body = OptionType.AGENT  # Reset the body
        ctx.last_state = id_func  # Set the last state
        ctx.waiting_for = "update_data_client"  # Set the waiting for value to update the client data

        return "1.3", False  # Return the next state

    else:
        # Send a message to the client asking for the lastnames
        MessageUseCases().send_message(
            MessageType.TELL_ME_YOUR_LASTNAMES.format(name=ctx.client.names),
            ctx.event_twilio.from_number, ctx.conversation.id
        )

        ctx.last_state = id_func

        return id_func, True  # Return the same state


@group.add_action("4.2", lambda ctx: ctx.waiting_for == "email")
def get_email_data(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    body = ctx.event_twilio.body.strip()

    if body:
        try:
            email = get_email(body)  # Get the email from the body
            ctx.client.email = email  # Set the client email
            ctx.event_twilio.body = OptionType.AGENT  # Reset the body
            ctx.last_state = id_func  # Set the last state
            ctx.waiting_for = "update_data_client"  # Set the waiting for value to update the client data

            return "1.3", False  # Return the next state

        except ValueError:
            # Send a message to the client telling that the email is invalid
            MessageUseCases().send_message(
                MessageType.ERROR_INVALID_EMAIL.format(name=ctx.client.get_fullname()),
                ctx.event_twilio.from_number, ctx.conversation.id
            )

            ctx.last_state = id_func

            return id_func, True  # Return the same state

    else:
        # Send a message to the client asking for the email
        MessageUseCases().send_message(
            MessageType.TELL_ME_YOUR_EMAIL.format(name=ctx.client.get_fullname()),
            ctx.event_twilio.from_number, ctx.conversation.id
        )

        ctx.last_state = id_func

        return id_func, True  # Return the same state


@group.add_action("4.3", lambda ctx: ctx.waiting_for == "phone")
def get_phone_data(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    body = ctx.event_twilio.body.strip()

    if body:
        ctx.client.phone = body  # Set the client phone
        ctx.event_twilio.body = OptionType.AGENT
        ctx.last_state = id_func
        ctx.waiting_for = "update_data_client"

        return "1.3", False

    else:
        # Send a message to the client asking for the phone
        MessageUseCases().send_message(
            MessageType.TELL_ME_YOUR_PHONE.format(name=ctx.client.get_fullname()),
            ctx.event_twilio.from_number, ctx.conversation.id
        )

        ctx.last_state = id_func

        return id_func, True  # Return the same state


@group.add_action("4.4", lambda ctx: ctx.waiting_for == "subject")
def get_subject_data(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    body = ctx.event_twilio.body.strip()

    if body:
        ctx.client.subject = body
