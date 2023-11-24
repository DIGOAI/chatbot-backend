from pydantic import BaseModel


class PhoneWithData(BaseModel):
    phone: str
    name: str | None


class SendWhatsAppMessageForm(BaseModel):
    clients: list[PhoneWithData]
