from src.chatbot import ActionGroup
from src.common.cases import MessageUseCases
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.utils import say_error, verify_button
from src.saragurosnet.types import MediaUrlType, MessageType, OptionType

group = ActionGroup[Context]()


@group.add_action("1.0", condition=lambda ctx: ctx.last_state == "0.2" and ctx.client != None, next=["1.1", "1.2", "1.3"])
def say_welcome_unknown(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.WELCOME_UNKNOW.format(
        name="Cliente"), ctx.event_twilio.from_number, ctx.conversation.id)

    ctx.last_state = id_func


@group.add_action("1.1", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and verify_button(ctx, OptionType.PROMOTIONS), end=False, next="3.0")
def send_promotions(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.PROMOTIONS, ctx.event_twilio.from_number,
                                   ctx.conversation.id, media_url=MediaUrlType.PROMOTIONS)

    ctx.last_state = id_func


@group.add_action("1.2", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and verify_button(ctx, OptionType.COVERAGES), end=False, next="3.0")
def send_coverages(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.COVERAGES, ctx.event_twilio.from_number,
                                   ctx.conversation.id, media_url=MediaUrlType.COVERAGES)

    ctx.last_state = id_func


@group.add_action("1.3", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and verify_button(ctx, OptionType.AGENT))
def talk_with_agent(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    fullname = ctx.client.get_fullname()

    MessageUseCases().send_message(MessageType.CONNECT_AGENT.format(
        name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)

    # TODO: Generar ticket de atencion al cliente
    # TODO: Crear nuevo usuario en microwisp para tener su ID
    # TODO: Enviar notificacion al agente con el ID del usuario
