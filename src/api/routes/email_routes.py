from dataclasses import dataclass
from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException

from src.api.middlewares import JWTBearer
from src.common.cases import EmailUseCases
from src.common.models import GenericResponse, create_response

router = APIRouter(prefix="/email", tags=["Email"], dependencies=[Depends(JWTBearer())])


@dataclass
class SendMassiveEmailPayload:
    emails: list[str]


@router.post("/{template_id}/send", response_model=GenericResponse[Literal[True]])
def send_massive_email(template_id: UUID, data: SendMassiveEmailPayload):
    email_cases = EmailUseCases().send_email(template_id, data.emails)

    if not email_cases:
        raise HTTPException(status_code=400, detail="Emails not sent")

    return create_response(data=email_cases, message="Emails sent")
