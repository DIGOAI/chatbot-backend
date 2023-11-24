import time
from uuid import UUID

from sqlalchemy import select

from src.api.cache import whatsapp
from src.common.cases import UseCaseBase
from src.common.cases.template_cases import MassiveTemplateUseCases
from src.common.logger import Logger
from src.common.models.ticket import Ticket, TicketStatus, TicketWithClient
from src.common.models.whatsapp import PhoneWithData
from src.common.services.twilio import TwilioService
from src.common.utils.twilio import render_twilio_template
from src.config import Config
from src.db.models.ticket import Ticket as TicketModel
from src.db.repositories import BaseRepository
from src.db.repositories.base_repository import IdNotFoundError

_twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                        Config.TWILIO_SENDER, '')
template_cases = MassiveTemplateUseCases()


class WhatsAppUseCase(UseCaseBase):
    def send_massive_message(self, template_id: str, clients: list[PhoneWithData]):
        whatsapp["sending"] = True
        # Logger.debug(f"{clients}")s
        template = template_cases.get_templsate_by_id(template_id)
        # template = "Hola, {{1}}.\nASUNTO: {{2}}.\n\n{{3}}\n\n_Este mensaje es automático, no responda al mismo._"

        for i, client in enumerate(clients):
            print(client)
            message = render_twilio_template(template, client.name)
            phone = f"whatsapp:{client.phone}"
            try:
                Logger.debug(f"sending to {phone}: {message}")
                _twilio.send_message(message, receiver=phone)
            except Exception as e:
                Logger.error(str(e))
        whatsapp["sending"] = False
