from datetime import datetime
from typing import NamedTuple
from uuid import UUID

from sqlalchemy import select

from src.common.cases.base_use_cases import UseCaseBase
from src.common.models import (
    Client,
    Conversation,
    ConversationInsert,
    ConversationStatus,
    ConversationWithData,
    ConversationWithLastMessage,
)
from src.db.models import Conversation as ConversationModel
from src.db.repositories import BaseRepository
from src.db.repositories.base_repository import IdNotFoundError


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

    def update_last_message_id(self, conversation: Conversation, message_id: str):
        with self._session() as session:
            conversation_repo = BaseRepository(ConversationModel, Conversation, session)
            conversation.updated_at = datetime.utcnow()
            conversation_updated = conversation_repo.update(
                conversation.id, last_message_id=message_id, updated_at=conversation.updated_at)

        return conversation_updated

    def end_conversation(self, conversation: Conversation):
        with self._session() as session:
            conversation_repo = BaseRepository(ConversationModel, Conversation, session)
            conversation.updated_at = datetime.utcnow()
            conversation_updated = conversation_repo.update(
                conversation.id, status=ConversationStatus.CLOSED, updated_at=conversation.updated_at)

        return conversation_updated

    def get_conversations_resume(self):
        ConversationResume = NamedTuple("ConversationResume", [("opened", int), ("closed", int)])

        with self._session() as session:
            opened = session.query(ConversationModel).filter(
                ConversationModel.status == ConversationStatus.OPENED).count()
            closed = session.query(ConversationModel).filter(
                ConversationModel.status == ConversationStatus.CLOSED).count()

        return ConversationResume(opened=opened, closed=closed)

    def get_conversations_with_last_message(self, from_: int, to: int):
        with self._session() as session:
            stmt = select(ConversationModel).limit(to).offset(from_).join(ConversationModel.last_message)
            conversations = session.scalars(stmt).all()

            convers = conversations
            conversations_with_last_message = [ConversationWithLastMessage.model_validate(c) for c in convers]

        return conversations_with_last_message

    def get_conversation_with_messages(self, conversation_id: UUID):
        with self._session() as session:
            stmt = select(ConversationModel).where(ConversationModel.id ==
                                                   conversation_id).join(ConversationModel.messages)
            conversations = session.scalar(stmt)

            if conversations is None:
                raise IdNotFoundError(conversation_id)
            conversation_with_data = ConversationWithData.model_validate(conversations)

        return conversation_with_data
