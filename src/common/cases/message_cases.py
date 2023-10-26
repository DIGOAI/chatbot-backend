from src.common.cases.base_use_cases import UseCaseBase
from src.common.models import Message, MessageInsert
from src.db.models import Message as MessageModel
from src.db.repositories import BaseRepository


class MessageUseCases(UseCaseBase):
    def add_new_message(self, message_data: MessageInsert):
        with self._session() as session:
            message_repo = BaseRepository(MessageModel, Message, session)
            message = message_repo.add(message_data.model_dump(), return_=False)

        return message
