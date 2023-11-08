from uuid import UUID

from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/whatsapp", tags=["Whatsapp"])


@router.post("/send")
def send_massive_whatsapp_message(template_id: UUID, phones: list[str]):
    raise HTTPException(status_code=501, detail="Not implemented")
