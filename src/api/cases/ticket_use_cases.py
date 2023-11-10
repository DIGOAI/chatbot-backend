from src.common.cases import UseCaseBase
from src.common.cases.conversation_cases import ConversationUseCases
from src.common.models import create_response

#
from src.common.models.ticket import Ticket as TicketPYModel
from src.common.models.ticket import TicketStatus

# common
from src.common.types import idType

# models
from src.db.models.ticket import Ticket as TicketDBModel

# db
from src.db.repositories import BaseRepository


class TicketUseCase(UseCaseBase):
    def list(self, limit: int = 30, offset: int = 0):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            items = repository.list(offset, limit)
        return create_response(data=items)

    def get(self, item_id: idType):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            item = repository.get(item_id)
        return item

    def add(self, data: dict):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            item = repository.add(data, return_=True)
        return item

    def update(self, item_id: idType, data: dict):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            item = repository.update(item_id, **data)
        return item

    def delete(self, item_id: idType):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            result = repository.delete(item_id)
        return result

    def open_ticket(self, item_id: idType):
        data = {
            "status": TicketStatus.ATTENDING
        }
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            result = self.update(item_id, data)
        return result

    def close_ticket(self, item_id: idType):
        data = {
            "status": TicketStatus.CLOSED
        }
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            result = self.update(item_id, data)
        return result
