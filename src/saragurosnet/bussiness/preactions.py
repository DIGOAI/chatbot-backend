from src.chatbot import ActionGroup, get_phone_and_service
from src.common.cases import ConversationUseCases, MessageUseCases
from src.common.logger import Logger
from src.common.models import MessageInsert
from src.saragurosnet.bussiness import Context

group = ActionGroup[Context]()


@group.add_preaction()
def pre_action(ctx: Context):
    Logger.info(f"Pre action: {ctx.last_state}")

    sender_phone, _ = get_phone_and_service(ctx.event_twilio.from_number)
    receiver_phone, _ = get_phone_and_service(ctx.event_twilio.to_number)

    # Save the message in the database
    message_cases = MessageUseCases()
    new_message = MessageInsert(
        id=ctx.event_twilio.message_sid,
        sender=sender_phone,
        receiver=receiver_phone,
        message=ctx.event_twilio.body,
        media_url=ctx.event_twilio.media_url,
        conversation_id=ctx.conversation.id
    )

    message_saved = message_cases.add_new_message(new_message)

    if message_saved:
        Logger.info(f"Message saved: {new_message.id}")

        # Update the conversation last message id
        conversation_cases = ConversationUseCases()
        conversation_updated = conversation_cases.update_last_message_id(ctx.conversation, new_message.id)

        ctx.conversation = conversation_updated
