from datetime import datetime

from src.common.cases.base_use_cases import UseCaseBase
from src.common.models import (
    Client,
    Conversation,
    ConversationInsert,
    ConversationStatus,
)
from src.db.models import Conversation as ConversationModel
from src.db.repositories import BaseRepository


class ConversationUseCases(UseCaseBase):

    def get_conversation_from_client_phone(self, client_phone: str):
        with self._session() as session:
            conversation_repo = BaseRepository(ConversationModel, Conversation, session)
            conversation = conversation_repo.filter(ConversationModel.client_phone == client_phone, first=True)

        return conversation

    def add_new_conversation(self, client_phone: str, assistant_phone: str):
        with self._session() as session:
            new_conversation = ConversationInsert.model_validate(
                {"client_phone": client_phone, "assistant_phone": assistant_phone, "status": ConversationStatus.OPENED})
            conversation_repo = BaseRepository(ConversationModel, Conversation, session)
            conversation = conversation_repo.add(new_conversation.model_dump())

        return conversation

    def update_client_id(self, conversation: Conversation, client: Client):
        with self._session() as session:
            conversation_repo = BaseRepository(ConversationModel, Conversation, session)
            conversation.updated_at = datetime.utcnow()
            conversation_updated = conversation_repo.update(
                conversation.id, client_id=client.id, updated_at=conversation.updated_at)

        return conversation_updated

    def end_conversation(self, conversation: Conversation):
        with self._session() as session:
            conversation_repo = BaseRepository(ConversationModel, Conversation, session)
            conversation.updated_at = datetime.utcnow()
            conversation_updated = conversation_repo.update(
                conversation.id, status=ConversationStatus.CLOSED, updated_at=conversation.updated_at)

        return conversation_updated
