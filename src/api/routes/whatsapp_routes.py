from uuid import UUID

from fastapi import APIRouter, BackgroundTasks

from src.common.cases import WhatsAppUseCase
from src.common.models import create_response
from src.common.models.whatsapp import SendWhatsAppMessageForm

router = APIRouter(prefix="/whatsapp", tags=["Whatsapp"])

_whatsapp_cases = WhatsAppUseCase()


@router.post("/{template_id}/send")
def send_massive_whatsapp_message(template_id: UUID, form: SendWhatsAppMessageForm, background_tasks: BackgroundTasks):
    background_tasks.add_task(_whatsapp_cases.send_massive_message, template_id, form.clients)

    return create_response(data=None, message="Sending messages")
