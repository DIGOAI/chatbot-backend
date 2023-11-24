from uuid import UUID

from fastapi import APIRouter, BackgroundTasks

from src.api.cache import whatsapp
from src.common.cases import WhatsAppUseCase
from src.common.models import create_response
from src.common.models.whatsapp import SendWhatsAppMessageForm

router = APIRouter(prefix="/whatsapp", tags=["Whatsapp"])

controller = WhatsAppUseCase()
# users = UsersUseCase()

# TODO: add cache


@router.post("/send")
def send_massive_whatsapp_message(template_id: UUID, form: SendWhatsAppMessageForm, background_tasks: BackgroundTasks):
    if not whatsapp.get("sending"):
        if form.type == "massive":
            clients = []
        if form.type == "specific":
            clients = form.clients
        background_tasks.add_task(controller.send_massive_message, template_id, clients)
        return create_response(data=None, message="Sending messages")
    else:
        return create_response(data=None, message="Server is busy", status_code=400)
