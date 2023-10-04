from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from src.common.models import Client, TwilioWebHook
from src.saragurosnet.bussiness import Context, tree

router = APIRouter(prefix="/twilio", tags=["Twilio"])


@router.post("/hook")
def twilio_hook(webhook: Annotated[TwilioWebHook, Depends()]):
    default_user = Client(id=-1, ci="", names="", lastnames="", phone="", last_state="",
                          saraguros_id=-1, created_at=datetime.utcnow(), updated_at=datetime.utcnow())

    tree.context = Context(webhook, default_user)
    tree()
