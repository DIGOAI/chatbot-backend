from uuid import UUID

from fastapi import HTTPException

from src.common.cases import UseCaseBase
from src.common.cases.template_cases import MassiveTemplateUseCases
from src.common.logger import Logger
from src.common.models.whatsapp import PhoneWithData
from src.common.services.twilio import TwilioService
from src.config import Config

_twilio = TwilioService(Config.TWILIO_SID, Config.TWILIO_TOKEN,
                        Config.TWILIO_SENDER, '')


class WhatsAppUseCase(UseCaseBase):
    def send_massive_message(self, template_id: UUID, clients: list[PhoneWithData]):
        Logger.debug(f"Setting whatsapp sending to True")

        template = MassiveTemplateUseCases().get_template_by_id(template_id)

        for client in clients:
            message = template.template.replace("{{1}}", client.name or "Cliente")
            phone = f"whatsapp:{client.phone}"

            try:
                Logger.debug(f"Sending massive template to {phone}: {message}")
                _twilio.send_message(message, receiver=phone)
            except Exception as e:
                Logger.error(msg=f"Error sending massive template to {phone}: {message}", err=e)

                raise HTTPException(status_code=500, detail=f"Error sending massive template to {phone}: {message}")
