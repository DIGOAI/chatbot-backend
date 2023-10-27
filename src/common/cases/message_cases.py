from src.chatbot.utils import get_phone_and_service
from src.common.cases.base_use_cases import UseCaseBase
from src.common.models import Message, MessageInsert, MessageInsertWeb
from src.common.models.message import MessageType
from src.common.services import TwilioService
from src.config import Config
from src.db.models import Message as MessageModel
from src.db.repositories import BaseRepository

twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                       Config.TWILIO_SENDER, '')


class MessageUseCases(UseCaseBase):

    def get_last_messages(self, limit: int = 10):
        with self._session() as session:
            message_repo = BaseRepository(MessageModel, Message, session)
            messages = message_repo.list(to=limit)

        return messages

    def add_new_message(self, message_data: MessageInsert):
        with self._session() as session:
            message_repo = BaseRepository(MessageModel, Message, session)
            message = message_repo.add(message_data.model_dump(), return_=False)

        return message

    def send_message_from_web(self, message_data: MessageInsertWeb):
        sender_phone, service = get_phone_and_service(Config.TWILIO_SENDER)

        print(sender_phone, service)

        print(message_data.receiver, service + message_data.receiver)

        message = twilio.send_message(msg=message_data.message, receiver=service + message_data.receiver)

        new_message = MessageInsert(
            id=message.sid,  # type: ignore
            sender=sender_phone,
            receiver=message_data.receiver,
            message=message_data.message,
            media_url=None,
            message_type=MessageType.OUT,
            conversation_id=message_data.conversation_id
        )

        with self._session() as session:
            message_repo = BaseRepository(MessageModel, Message, session)
            message = message_repo.add(new_message.model_dump(), return_=True)

        return message
