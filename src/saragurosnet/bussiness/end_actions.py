from src.chatbot import ActionGroup
from src.chatbot.utils import format_fullname
from src.common.cases import ConversationUseCases, MessageUseCases
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.errors import say_error
from src.saragurosnet.types import MessageType, OptionType

group = ActionGroup[Context]()


@group.add_action("3.0", condition=lambda ctx: ctx.last_state in ["1.1", "1.2"], next="3.1")
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

    if ctx.client.saraguros_id:
        # Return to say_welcome_client
        pass
    else:
        # Return to say_welcome_unknown
        pass
