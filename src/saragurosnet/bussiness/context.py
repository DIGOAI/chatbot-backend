from src.common.models import Client
from src.common.models import TwilioWebHook as Event


class Context():
    """Context class to handle the context of the application."""

    def __init__(self, event: Event, client: Client | None, last_state: str | None) -> None:
        self.event_twilio: Event = event
        self.client: Client | None = client
        self.last_state: str | None = last_state

    def __str__(self) -> str:
        return f"Context(event_twilio={self.event_twilio}, client={self.client}, last_state={self.last_state})"
