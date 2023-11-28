from src.chatbot import ActionGroup
from src.chatbot.utils import format_fullname, get_phone_and_service
from src.common.cases import ConversationUseCases, MessageUseCases
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.utils import say_error
from src.saragurosnet.types import MessageType, OptionType

group = ActionGroup[Context]()


@group.add_action("3.0", condition=lambda ctx: ctx.last_state in ["1.1", "1.2", "1.3"], next=["3.1", "3.2"])
def end_conversation(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    fullname = format_fullname(ctx.client.names, ctx.client.lastnames)
    fullname = fullname if fullname != "" else "Cliente"

    MessageUseCases().send_message(MessageType.END_CONVERSATION.format(
        name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)

    ctx.last_state = id_func


@group.add_action("3.1", condition=lambda ctx: ctx.last_state == "3.0" and ctx.event_twilio.body == OptionType.END)
def say_goodbye(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.SAY_GOODBAY, ctx.event_twilio.from_number, ctx.conversation.id)

    # TODO: End conversation and update th db
    conversation = ConversationUseCases().end_conversation(ctx.conversation)

    ctx.last_state = id_func
    ctx.client = None
    ctx.conversation = conversation


@group.add_action("3.2", condition=lambda ctx: ctx.last_state == "3.0" and ctx.event_twilio.body == OptionType.ANOTHER)
def another_question(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    ctx.last_state = "3.2"
    # End conversation and update in db
    ConversationUseCases().end_conversation(ctx.conversation)

    # Get client and assistant phone number with the service name
    client_phone, _ = get_phone_and_service(ctx.event_twilio.from_number)
    assistant_phone, _ = get_phone_and_service(ctx.event_twilio.to_number)

    # Create a new conversation and update in db
    ctx.conversation = ConversationUseCases().add_new_conversation(client_phone, assistant_phone)

    if ctx.client.saraguros_id is not None:
        # Return to say_welcome_client
        return "2.0", False
    else:
        # Return to say_welcome_unknown
        return "1.0", False
