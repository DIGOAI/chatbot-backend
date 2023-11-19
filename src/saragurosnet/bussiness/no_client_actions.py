from src.chatbot import ActionGroup, format_fullname
from src.common.cases import MessageUseCases
from src.saragurosnet.bussiness.context import Context
from src.saragurosnet.bussiness.errors import say_error
from src.saragurosnet.types import MediaUrlType, MessageType, OptionType

group = ActionGroup[Context]()


@group.add_action("1.0", condition=lambda ctx: ctx.last_state == "0.2" and ctx.client != None and ctx.client.saraguros_id == None, next=["1.1", "1.2", "1.3"])
def say_welcome_unknown(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.WELCOME_UNKNOW.format(
        name="Cliente"), ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.WELCOME_UNKNOW.format(name="Cliente"), receiver="whatsapp:" + ctx.client.phone)

    ctx.last_state = id_func


@group.add_action("1.1", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None and (ctx.event_twilio.button_text == OptionType.PROMOTIONS or ctx.event_twilio.body == OptionType.PROMOTIONS), end=False, next="3.0")
def send_promotions(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.PROMOTIONS, ctx.event_twilio.from_number,
                                   ctx.conversation.id, media_url=MediaUrlType.PROMOTIONS)

    # twilio.send_message(MessageType.PROMOTIONS,
    #                     receiver="whatsapp:" + ctx.client.phone,
    #                     media_url=MediaUrlType.PROMOTIONS)

    # fullname = format_fullname(ctx.client.names, ctx.client.lastnames)
    # say_goodbye(fullname, "whatsapp:" + ctx.client.phone)
    ctx.last_state = id_func


@group.add_action("1.2", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None and (ctx.event_twilio.button_text == OptionType.COVERAGES or ctx.event_twilio.body == OptionType.COVERAGES), end=False, next="3.0")
def send_coverages(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    MessageUseCases().send_message(MessageType.COVERAGES, ctx.event_twilio.from_number,
                                   ctx.conversation.id, media_url=MediaUrlType.COVERAGES)

    # twilio.send_message(MessageType.COVERAGES,
    #                     receiver="whatsapp:" + ctx.client.phone,
    #                     media_url=MediaUrlType.COVERAGES)

    # fullname = format_fullname(ctx.client.names, ctx.client.lastnames)
    # say_goodbye(fullname, "whatsapp:" + ctx.client.phone)
    ctx.last_state = id_func


@group.add_action("1.3", condition=lambda ctx: ctx.last_state == "1.0" and ctx.client != None and ctx.client.saraguros_id == None and (ctx.event_twilio.button_text == OptionType.AGENT or ctx.event_twilio.body == OptionType.AGENT))
def talk_with_agent(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    fullname = format_fullname(ctx.client.names, ctx.client.lastnames)

    MessageUseCases().send_message(MessageType.CONNECT_AGENT.format(
        name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)
    # twilio.send_message(MessageType.CONNECT_AGENT.format(name=fullname), receiver="whatsapp:" + ctx.client.phone)

    # TODO: Generar ticket de atencion al cliente
    # TODO: Crear nuevo usuario en microwisp para tener su ID
    # TODO: Enviar notificacion al agente con el ID del usuario
