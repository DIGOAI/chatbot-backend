from sqlalchemy import select
from sqlalchemy.orm import Session

from src.api.db.models import Message as MessageModel
from src.common.models import Message, MessageInsert


class MessageRepository:
    def __init__(self, session: Session):
        self._session = session

    def get_by_id(self, id: int) -> Message | None:
        # res = self.db.execute(select(MessageModel).filter(MessageModel.id == id)).scalar()
        message = self._session.get(MessageModel, id)

        if message is None:
            return None

        return Message.model_validate(message)

    def get_by_client_id(self, client_id: int) -> list[Message]:
        stmt = select(MessageModel).filter(MessageModel.client_id == client_id)
        messages = self._session.scalars(stmt).all()
        return [Message.model_validate(message) for message in messages]

    def get_by_sender(self, sender: str) -> list[Message]:
        stmt = select(MessageModel).filter(MessageModel.sender == sender)
        messages = self._session.scalars(stmt).all()
        return [Message.model_validate(message) for message in messages]

    def get_last_messages(self, limit: int | None = None) -> list[Message]:
        stmt = select(MessageModel).limit(limit)
        messages = self._session.scalars(stmt).all()
        return [Message.model_validate(message) for message in messages]

    def create(self, message: MessageInsert) -> Message:
        message_model = MessageModel(**message.model_dump())
        self._session.add(message_model)
        self._session.commit()
        self._session.refresh(message_model)
        message_created = Message.model_validate(message_model)
        return message_created

    def delete(self, id: int):
        message = self.get_by_id(id)
        self._session.delete(message)
        return message
