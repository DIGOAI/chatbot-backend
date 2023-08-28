import json
from enum import Enum
from typing import Any, Optional

import requests

from models import Ticket
from src.config import Config


class SaragurosServiceEndpoint(str, Enum):
    """Enum to represent the endpoints of the Saraguros API."""

    ACTIVATE_SERVICE = "ActiveService"
    NEW_TICKET = "NewTicket"
    GET_CLIENTS = "GetClientsDetails"


class SaragurosService:
    """Class to manage the connection to the Saraguros API."""

    def __init__(self, token: str):
        self.base_url = Config.SARAGUROS_API_URL
        self.headers = {"Content-Type": "application/json"}
        self.token = token

    def _make_request(self, endpoint: str, data: dict[str, Any]) -> dict[str, Any]:
        """Make a request to the Saraguros API.

        Parameters:
        endpoint (str): The endpoint to make the request
        data (dict[str, Any]): The data to send in the request

        Returns:
        dict[str, Any]: The result of the request
        """

        url = f"{self.base_url}/{endpoint}"
        data["token"] = self.token

        response = requests.post(
            url, headers=self.headers, data=json.dumps(data))

        return response.json()

    def activar_servicio(self, usuario_id: str) -> Optional[dict[str, Any]]:
        """Activate the service for a user.

        Parameters:
        usuario_id (str): The id of the user to activate the service

        Returns:
        dict[str, Any] | None: The result of the request
        """
        data = {"idcliente": usuario_id}

        return self._make_request(SaragurosServiceEndpoint.ACTIVATE_SERVICE, data)

    def create_ticket(self, ticket: Ticket) -> Optional[dict[str, Any]]:
        """Create a ticket.

        Parameters:
        ticket (Ticket): The ticket to create

        Returns:
        dict[str, Any] | None: The result of the request
        """

        data = {
            "idcliente": ticket.id_cliente,
            "dp": ticket.departamento,
            "asunto": ticket.asunto,
            "fechavisita": ticket.fechavisita,
            "turno": ticket.turno,
            "agendado": ticket.agendado,
            "contenido": ticket.contenido
        }

        return self._make_request(SaragurosServiceEndpoint.NEW_TICKET, data)

    def getUsuarioData(self, cedula: str):
        """Get the data of a user.

        Parameters:
        cedula (str): The cedula of the user to get the data

        Returns:
        dict[str, Any] | None: The result of the request
        """

        data = {"cedula": cedula}

        return self._make_request(SaragurosServiceEndpoint.GET_CLIENTS, data)


if __name__ == "__main__":
    token = "R3Z4SlNrWVZvZzFsV1pvTTQ3ci9wZz09"
    usuario_id = "34fdd32g-4f3d-4f3d-4f3d-4f3d4f3d4f3d"

    service = SaragurosService(token)

    activar_result = service.activar_servicio(usuario_id)
    print("Resultado de activar_servicio:", activar_result)

    nuevo_ticket = Ticket(
        contenido="Contenido del ticket",
        asunto="Asunto del ticket",
        departamento="Soporte",
        turno="Tarde",
        fechavisita="2023-08-25",
        agendado=True
    )
    nuevo_ticket.id_cliente = usuario_id

    create_ticket_result = service.create_ticket(nuevo_ticket)
    print("Resultado de create_ticket:", create_ticket_result)
