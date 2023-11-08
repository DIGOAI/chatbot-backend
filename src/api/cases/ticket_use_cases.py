from src.common.cases import UseCaseBase
from src.common.models import create_response
from src.common.models.ticket import Ticket as TicketPYModel
from src.db.models.ticket import Ticket as TicketDBModel

# db
from src.db.repositories import BaseRepository


class TicketUseCase(UseCaseBase):
    def list(self, limit: int = 30, offset: int = 0):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            items = repository.list(offset, limit)
        return create_response(data=items)

    def get(self, item_id: int):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            item = repository.get(item_id)
        return item

    def add(self, data: dict):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            item = repository.add(data, return_=True)
        return item

    def update(self, item_id: int, data: dict):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            item = repository.update(item_id, **data)
        return item

    def delete(self, item_id: int):
        with self._session() as session:
            repository = BaseRepository(TicketDBModel, TicketPYModel, session)
            result = repository.delete(item_id)
        return result
