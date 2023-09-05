from typing import Any

from src.bussiness import tree
from src.config import Config
from src.db import PostgreSQLConnection
from src.logger import Logger
from src.models import ContextType, Event
from src.services import ChatApiService, SaragurosService, TwilioService


def lambda_handler(event: dict[str, Any], __context: Any) -> None:
    # Setup the database connection
    conn = PostgreSQLConnection(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME
    )

    # Setup the chat api service
    chat_api_service = ChatApiService(conn)

    # Setup the saragurosnet service
    saragurosnet_service = SaragurosService(Config.SARAGUROS_API_TOKEN)

    # Parse the event to an Event object
    payload = Event(event)

    # Setup the twilio service
    twilio_service = TwilioService(
        Config.TWILIO_SID,
        Config.TWILIO_TOKEN,
        sender=payload.to_phone,
        receiver=payload.from_phone
    )

    # Get the client phone number in 09XXXXXXXXX format
    client_phone = payload.from_phone.replace('whatsapp:+593', '0')

    # Get the status, hours difference and user id of the user by the phone if exists
    status, hours_diff, user_id = chat_api_service.get_estado_usuario(
        client_phone)
    # Get the cedula of the user by the phone if exists
    user_ci = chat_api_service.get_cedula_by_celular(client_phone)

    Logger.info(f"Context loaded[ ID: {user_id} | CI: {user_ci} | Status: {status} | Hours: {hours_diff}]")

    # Create a global context
    context: ContextType = {
        "EVENT_TWILIO": payload,
        'DATA_USER_ID': user_id,
        'DATA_USER_CI': "0105997001",
        'DATA_LAST_STATUS': "",  # Set estatus in "1.0" for testing
        'SERVICE_API': chat_api_service,
        'SERVICE_SARAGUROS': saragurosnet_service,
        'SERVICE_TWILIO': twilio_service
    }

    # Create the decisions tree
    # decisions_tree = DecisionsTree(context)
    # Add the actions to the decisions tree
    # decisions_tree.addAction(Action("1.0", say_welcome))

    tree.context = context
    # Execute the actions in the decisions tree
    tree()


if __name__ == '__main__':
    lambda_handler({
        "Body": "Hola",
        "From": "whatsapp:+593959011576",
        "To": "whatsapp:+593986728536",
        "MediaUrl0": ""
    }, None)
