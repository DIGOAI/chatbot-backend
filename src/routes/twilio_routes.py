from typing import Annotated

from fastapi import APIRouter, Depends

from src.models import TwilioWebHook

router = APIRouter(prefix="/twilio", tags=["Twilio"])


@router.post("/hook")
def twilio_hook(webhook: Annotated[TwilioWebHook, Depends()]):
    return webhook
