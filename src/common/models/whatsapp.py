from typing import Literal, Optional

from pydantic import BaseModel

#
SendWhatsAppMessageType = Literal["massive"] | Literal["specific"]


class SendWhatsAppMessageForm(BaseModel):
    type: SendWhatsAppMessageType
    phones: Optional[list[str]]
