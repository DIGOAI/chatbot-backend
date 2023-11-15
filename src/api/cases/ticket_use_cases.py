from uuid import UUID

from sqlalchemy import select

from src.common.cases import UseCaseBase
from src.common.models.ticket import Ticket, TicketStatus, TicketWithClient
from src.db.models.ticket import Ticket as TicketModel
from src.db.repositories import BaseRepository
from src.db.repositories.base_repository import IdNotFoundError


class TicketUseCase(UseCaseBase):
    def get_tickets(self, limit: int = 30, offset: int = 0):
        with self._session() as session:
            repository = BaseRepository(TicketModel, Ticket, session)
            tickets = repository.list(offset, limit)

        return tickets

    def get_ticket(self, item_id: UUID):
        with self._session() as session:
            repository = BaseRepository(TicketModel, Ticket, session)
            ticket = repository.get(item_id)

        return ticket

    def attend_ticket(self, item_id: UUID):
        with self._session() as session:
            ticket_repo = BaseRepository(TicketModel, Ticket, session)
            ticket = ticket_repo.update(item_id, status=TicketStatus.ATTENDING)

        return ticket

    def close_ticket(self, item_id: UUID):
        with self._session() as session:
            ticket_repo = BaseRepository(TicketModel, Ticket, session)
            ticket = ticket_repo.update(item_id, status=TicketStatus.CLOSED)

        return ticket

    def get_tickets_with_client(self, limit: int = 30, offset: int = 0):
        with self._session() as session:
            stmt = select(TicketModel).order_by(TicketModel.created_at.desc()
                                                ).limit(limit).offset(offset).join(TicketModel.client)
            tickets = session.scalars(stmt).all()

            tickets_with_client = [TicketWithClient.model_validate(t) for t in tickets]
        return tickets_with_client

    def get_ticket_with_client(self, item_id: UUID):
        with self._session() as session:
            stmt = select(TicketModel).where(TicketModel.id == item_id).join(TicketModel.client)
            ticket = session.scalar(stmt)

            if ticket is None:
                raise IdNotFoundError(item_id)

            ticket_with_client = TicketWithClient.model_validate(ticket)

        return ticket_with_client
