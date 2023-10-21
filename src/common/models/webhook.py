from typing import Annotated, Optional

from fastapi import Form


class TwilioWebHook():
    """Model for Twilio's Event Webhook."""

    def __init__(self, MessageSid: Annotated[str, Form(max_length=34, alias="MessageSid",
                                                       description="Unique identifier for the message.")],
                 AccountSid: Annotated[str, Form(max_length=34, alias="AccountSid",
                                                 description="Unique identifier for the account.")],
                 MessagingServiceSid: Annotated[str, Form(max_length=34, alias="MessagingServiceSid",
                                                          description="Unique identifier for the messaging service.")],
                 From: Annotated[str, Form(max_length=22, alias="From", description="The number that sent the message.")],
                 To: Annotated[str, Form(max_length=22, alias="To", description="The number that received the message.")],
                 ProfileName: Annotated[str, Form(alias="ProfileName", description="The name of the WhatsApp profile.")],
                 WaId: Annotated[str, Form(alias="WaId", description="The WhatsApp ID of the sender.")],
                 SmsSid: Annotated[str, Form(max_length=34, alias="SmsSid",
                                             description="Unique identifier for the SMS (Deprecated).")] = "",
                 Body: Annotated[str, Form(max_length=1600, alias="Body",
                                           description="The text body of the message.")] = "",
                 NumMedia: Annotated[int, Form(alias="NumMedia",
                                               description="The number of media items associated with the message.")] = 0,
                 MediaContentType0: Annotated[Optional[str], Form(alias="MediaContentType0",
                                                                  description="The content type of the media.")] = None,
                 MediaUrl0: Annotated[Optional[str], Form(
                     alias="MediaUrl0", description="The URL of the media.")] = None,
                 Forwarded: Annotated[bool, Form(
                     alias="Forwarded", description="Whether the message was forwarded.")] = False,
                 FrequentlyForwarded: Annotated[bool, Form(alias="FrequentlyForwarded",
                                                           description="Whether the message was frequently forwarded.")] = False,
                 ButtonText: Annotated[Optional[str], Form(alias="ButtonText", description="The text of a Quick reply button.")] = None):
        self.message_sid = MessageSid
        self.sms_sid = SmsSid
        self.account_sid = AccountSid
        self.messaging_service_sid = MessagingServiceSid
        self.from_number = From
        self.to_number = To
        self.body = Body
        self.num_media = NumMedia
        self.media_content_type = MediaContentType0
        self.media_url = MediaUrl0
        self.profile_name = ProfileName
        self.wa_id = WaId
        self.forwarded = Forwarded
        self.frequently_forwarded = FrequentlyForwarded
        self.button_text = ButtonText

    def __str__(self) -> str:
        return f"TwilioWebHook(from_number={self.from_number}, to_number={self.to_number}, body={self.body}, num_media={self.num_media}, media_content_type={self.media_content_type}, media_url={self.media_url}, profile_name={self.profile_name}, wa_id={self.wa_id}, button_text={self.button_text})"
