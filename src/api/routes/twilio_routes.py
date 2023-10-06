from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, Depends

from src.common.logger import Logger
from src.common.models import Client, TwilioWebHook
from src.saragurosnet.bussiness import Context, tree

router = APIRouter(prefix="/twilio", tags=["Twilio"])

# TODO: Upgrade this cache for support only 100 clients and delete the old ones
clients_cache: dict[str, Client] = {}


@router.post("/hook")
def twilio_hook(webhook: Annotated[TwilioWebHook, Depends()]):
    global clients_cache  # Use the global clients cache

    client_cached = clients_cache.get(webhook.from_number)

    if client_cached:
        Logger.info(f"Client cached: {webhook.from_number}")
        tree.context = Context(webhook, client_cached)
    else:
        Logger.info(f"Client not cached: {webhook.from_number}")
        default_user = Client(id=-1, ci="", names="", lastnames="", phone="", last_state="",
                              saraguros_id=-1, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        tree.context = Context(webhook, default_user)

    # Execute the tree actions with the context setted
    tree()

    # Cache the client for the next request
    client = tree.context.client
    client_phone = f"whatsapp:{client.phone}"
    Logger.info(f"Caching client: {client_phone}")
    clients_cache[client_phone] = client