from src.common.models import Client
from src.common.models import TwilioWebHook as Event


class Context():
    """Context class to handle the context of the application."""

    def __init__(self, event: Event, client: Client | None, last_state: str | None) -> None:
        self.event_twilio: Event = event
        self.client: Client | None = client
        self.last_state: str | None = last_state
