from src.chatbot import ActionGroup
from src.common.cases import ClientUseCases, MessageUseCases
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


@group.add_action("1.3", condition=lambda ctx: (ctx.last_state == "1.0" and ctx.client != None and verify_button(ctx, OptionType.AGENT)) or ctx.last_state == "1.3", end=False, next="3.0")
def talk_with_agent(ctx: Context, id_func: str):
    if ctx.client is None:
        return say_error(ctx)

    last_value: str = ""
    body = ctx.event_twilio.body

    # Verify if client has a name, lastname and email.
    # If not, ask for it.
    # If yes, continue to next state.

    if ctx.client.names is None:
        # TODO: Ask for names

        if body and not verify_button(ctx, OptionType.AGENT):
            # TODO: Verify if the message is a correct name
            ctx.client.names = body
            last_value = body
            # ClientUseCases().update_client(ctx.client)
            pass
        else:
            MessageUseCases().send_message(MessageType.TELL_ME_YOUR_NAMES.format(
                name='Cliente'), ctx.event_twilio.from_number, ctx.conversation.id)

            ctx.last_state = "1.3"
            return "1.3", True

    if ctx.client.lastnames is None:
        # TODO: Ask for lastnames

        if body and not verify_button(ctx, OptionType.AGENT) and last_value != body:
            # TODO: Verify if the message is a correct lastname
            ctx.client.lastnames = body
            last_value = body
            pass
        else:
            MessageUseCases().send_message(MessageType.TELL_ME_YOUR_LASTNAMES.format(
                name=ctx.client.names), ctx.event_twilio.from_number, ctx.conversation.id)

            ctx.last_state = "1.3"
            return "1.3", True

    if ctx.client.email is None:
        # TODO: Ask for email

        if body and not verify_button(ctx, OptionType.AGENT) and last_value != body:
            # TODO: Verify if the message is a correct email
            ctx.client.email = body
            last_value = body
            pass
        else:
            MessageUseCases().send_message(MessageType.TELL_ME_YOUR_EMAIL.format(
                name=ctx.client.get_fullname()), ctx.event_twilio.from_number, ctx.conversation.id)

            ctx.last_state = "1.3"
            return "1.3", True

    # Update the client data in the database
    client_updated = ClientUseCases().update_client(ctx.client)
    ctx.client = client_updated

    fullname = ctx.client.get_fullname()

    MessageUseCases().send_message(MessageType.CONNECT_AGENT.format(
        name=fullname), ctx.event_twilio.from_number, ctx.conversation.id)

    ctx.last_state = id_func

    # TODO: Generar ticket de atencion al cliente
    # TODO: Crear nuevo usuario en microwisp para tener su ID
    # TODO: Enviar notificacion al agente con el ID del usuario
