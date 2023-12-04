from uuid import UUID

from src.chatbot.utils import get_phone_and_service
from src.common.cases.base_use_cases import UseCaseBase
from src.common.models import Message, MessageInsert, MessageInsertWeb, MessageType
from src.common.services import TwilioService
from src.config import Config
from src.db.models import Message as MessageModel
from src.db.repositories import BaseRepository

_twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                        Config.TWILIO_SENDER, '')

_sender_phone, _service = get_phone_and_service(Config.TWILIO_SENDER)


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
        message = _twilio.send_message(msg=message_data.message, receiver=_service + message_data.receiver)

        new_message = MessageInsert(
            id=message.sid,  # type: ignore
            sender=_sender_phone,
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

    def send_message(self, msg: str, receiver: str, conversation_id: UUID, media_url: str | None = None):
        message = _twilio.send_message(msg=msg, receiver=receiver, media_url=media_url)

        receiver_phone, _service = get_phone_and_service(receiver)

        new_message = MessageInsert(
            id=message.sid,  # type: ignore
            sender=_sender_phone,
            receiver=receiver_phone,
            message=msg,
            media_url=media_url,
            message_type=MessageType.OUT,
            conversation_id=conversation_id
        )

        with self._session() as session:
            message_repo = BaseRepository(MessageModel, Message, session)
            message = message_repo.add(new_message.model_dump(), return_=True)

        return message
