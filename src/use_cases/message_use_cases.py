from fastapi import status as STATUS

from src.db import Session
from src.models import MessageInsert, create_response
from src.repositories import MessageRepository


def write_message(new_message: MessageInsert):
    with Session() as session:
        message_repository = MessageRepository(session)
        message = message_repository.create(new_message)

    return create_response(message, "Message created", status_code=STATUS.HTTP_201_CREATED)


def get_last_messages(company_name: str, limit: int = 10):
    with Session() as session:
        message_repository = MessageRepository(session)
        messages = message_repository.get_messages_by_company(company_name, limit)

    return create_response(messages, f"Last {limit} messages", status_code=STATUS.HTTP_200_OK)
