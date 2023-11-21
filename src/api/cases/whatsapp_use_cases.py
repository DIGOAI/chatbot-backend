import time
from uuid import UUID

from sqlalchemy import select

from src.common.cases import UseCaseBase
from src.common.models.ticket import Ticket, TicketStatus, TicketWithClient
from src.db.models.ticket import Ticket as TicketModel
from src.db.repositories import BaseRepository
from src.db.repositories.base_repository import IdNotFoundError


class WhatsAppUseCase(UseCaseBase):
    def send_massive_message(self, template_id: str, phones: list[str]):
        for i in range(len(phones)):
            print("sending: ", i)
            time.sleep(1)
