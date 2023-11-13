import smtplib
from email.message import EmailMessage

from src.config import Config


class SMTPService():

    def __init__(self) -> None:
        self._sender = Config.SMTP_SENDER

    def send_email(self, receivers: list[str], subject: str, body: str):
        msg = EmailMessage()

        msg.set_content(body)
        msg['Subject'] = subject
        msg['From'] = self._sender
        msg['To'] = ', '.join(receivers)

        with smtplib.SMTP_SSL(Config.SMTP_HOST, Config.SMTP_PORT) as smtp:
            smtp.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            smtp.send_message(msg)

        return True
