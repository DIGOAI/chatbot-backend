from src.chatbot.decisions_tree import DecisionsTree
from src.chatbot.utils import format_fullname
from src.common.cases import ConversationUseCases, MessageUseCases
from src.common.services import TwilioService
from src.config import Config
from src.saragurosnet.bussiness.client_actions import group as client_group
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.errors import say_error
from src.saragurosnet.bussiness.initial_actions import group as initial_group
from src.saragurosnet.bussiness.no_client_actions import group as no_client_group
from src.saragurosnet.bussiness.preactions import group as pre_group
from src.saragurosnet.types import MessageType, OptionType

tree = DecisionsTree[Context]()

twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                       Config.TWILIO_SENDER, '')

# === Pre actions ===
tree.register_action_group(pre_group)
# === End pre actions ===

# === Initial actions ===
tree.register_action_group(initial_group)
# === End initial actions ===

# === No client actions ===
tree.register_action_group(no_client_group)
# === End no client actions ===

# === Client actions ===
tree.register_action_group(client_group)
# === End Client actions ===


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
