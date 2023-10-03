import json
from typing import Annotated

from fastapi import APIRouter, Depends, Response

from src.models import TwilioWebHook

router = APIRouter(prefix="/twilio", tags=["Twilio"])


@router.post("/hook")
def twilio_hook(webhook: Annotated[TwilioWebHook, Depends()]):
    response_content = """<?xml version="1.0" encoding="UTF-8"?>
    <Response>
        <Message>
        {message}
        </Message>
    </Response>
    """

    content = response_content.format(message=json.dumps(webhook.__dict__, indent=2))

    return Response(content, media_type="application/xml")
