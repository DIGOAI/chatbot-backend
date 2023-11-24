from typing import Literal, Optional

from pydantic import BaseModel

#
SendWhatsAppMessageType = Literal["massive"] | Literal["specific"]


class PhoneWithData(BaseModel):
    phone: str
    name: str


class SendWhatsAppMessageForm(BaseModel):
    type: SendWhatsAppMessageType
    clients: Optional[list[PhoneWithData]]
