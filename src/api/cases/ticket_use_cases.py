from uuid import UUID

from src.common.cases import UseCaseBase
from src.common.models.ticket import Ticket, TicketStatus
from src.db.models.ticket import Ticket as TicketModel
from src.db.repositories import BaseRepository


class TicketUseCase(UseCaseBase):
    def get_tickets(self, limit: int = 30, offset: int = 0):
        with self._session() as session:
            repository = BaseRepository(TicketModel, Ticket, session)
            items = repository.list(offset, limit)

        return items

    def get_ticket(self, item_id: UUID):
        with self._session() as session:
            repository = BaseRepository(TicketModel, Ticket, session)
            item = repository.get(item_id)

        return item

    def attend_ticket(self, item_id: UUID):
        with self._session() as session:
            ticket_repo = BaseRepository(TicketModel, Ticket, session)
            result = ticket_repo.update(item_id, status=TicketStatus.ATTENDING)

        return result

    def close_ticket(self, item_id: UUID):
        with self._session() as session:
            ticket_repo = BaseRepository(TicketModel, Ticket, session)
            result = ticket_repo.update(item_id, status=TicketStatus.CLOSED)

        return result
