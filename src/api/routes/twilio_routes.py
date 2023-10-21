from typing import Annotated, NamedTuple

from fastapi import APIRouter, Depends

from src.common.logger import Logger
from src.common.models import Client, TwilioWebHook
from src.saragurosnet.bussiness import Context, tree

router = APIRouter(prefix="/twilio", tags=["Twilio"])


class CacheClientTuple(NamedTuple):
    client: Client | None
    last_state: str | None


# TODO: Upgrade this cache for support only 100 clients and delete the old ones
clients_cache: dict[str, CacheClientTuple] = {}


@router.post("/hook")
def twilio_hook(webhook: Annotated[TwilioWebHook, Depends()]):
    global clients_cache  # Use the global clients cache

    client_cached = clients_cache.get(webhook.from_number)

    if client_cached:
        Logger.info(f"Client cached: {webhook.from_number}")
        tree.context = Context(webhook, client_cached.client, client_cached.last_state)
    else:
        Logger.info(f"Client not cached: {webhook.from_number}")
        # default_user = Client(id="", ci="", names="", lastnames="", phone="", saraguros_id=-1, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        tree.context = Context(webhook, None, None)

    # Execute the tree actions with the context setted
    tree()

    # Cache the client for the next request
    event = tree.context.event_twilio
    client_phone = event.from_number

    Logger.info(f"Caching client: {client_phone}")
    clients_cache[client_phone] = CacheClientTuple(client=tree.context.client, last_state=tree.context.last_state)
