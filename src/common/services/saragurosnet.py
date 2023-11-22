import json
from enum import Enum
from typing import Any, Literal, Optional

import requests

from src.common.logger import Logger
from src.common.models.ticket import TicketSaragurosInsert as Ticket
from src.config import Config

_InstallationType = Literal['PENDIENTE', 'NO INSTALADO', 'INSTALADO']


class MikrowispEndpoint(str, Enum):
    """Enum to represent the endpoints of the Saraguros API."""

    ACTIVATE_SERVICE = "ActiveService"
    NEW_TICKET = "NewTicket"
    GET_CLIENTS = "GetClientsDetails"
    LIST_INSTALLS = "ListInstall"


class SaragurosNetService:
    """Class to manage the connection to the Saraguros API."""

    def __init__(self, token: str):
        self.base_url = Config.SARAGUROS_API_URL
        self.headers = {"Content-Type": "application/json"}
        self.token = token

    def _make_request(self, endpoint: MikrowispEndpoint, data: dict[str, Any]) -> Optional[dict[str, Any]]:
        """Make a request to the Saraguros API.

        Attributes:
        endpoint (str): The endpoint to make the request
        data (dict[str, Any]): The data to send in the request

        Returns:
        dict[str, Any] | None: The result of the request
        """

        url = f"{self.base_url}/{endpoint.value}"
        data["token"] = self.token

        Logger.info(f"Making request to {url} with data {data}")

        response = requests.post(
            url, headers=self.headers, data=json.dumps(data))

        if response.status_code >= 400:
            Logger.error(f"Error making request to {url} with data {data}")
            return None

        try:
            Logger.info(f"Parsing response from {url}")
            return response.json()
        except BaseException:
            Logger.error(f"Error parsing response from {url}")
            return None

    def activate_service(self, user_id: int) -> Optional[dict[str, Any]]:
        """Activate the service for a user.

        Parameters:
        usuario_id (str): The id of the user to activate the service

        Returns:
        dict[str, Any] | None: The result of the request
        """
        data = {"idcliente": user_id}

        return self._make_request(MikrowispEndpoint.ACTIVATE_SERVICE, data)

    def create_ticket(self, ticket: Ticket) -> Optional[dict[str, Any]]:
        """Create a ticket.

        Attributes:
        ticket (Ticket): The ticket to create

        Returns:
        dict[str, Any] | None: The result of the request
        """

        data = ticket.model_dump(by_alias=True)

        Logger.info(f"Creating ticket with data {data}")

        return self._make_request(MikrowispEndpoint.NEW_TICKET, data)

    def get_client_data(self, ci: str) -> Optional[dict[str, Any]]:
        """Get the data of a user.

        Attributes:
        cedula (str): The cedula of the user to get the data

        Returns:
        dict[str, Any] | None: The result of the request

        Example:
        ```json
        {
            "estado":"exito",
            "datos":[
                {
                    "id":6,
                    "nombre":"ARIEL Perez",
                    "estado":"ACTIVO",
                    "correo":"",
                    "telefono":"45434565",
                    "movil":"998283745",
                    "cedula":"65454323",
                    "pasarela":"",
                    "codigo":"l4o4gp",
                    "direccion_principal":"2301 Peger Rd.",
                    "servicios":[
                        {
                            "id":5,
                            "idperfil":2,
                            "nodo":2,
                            "costo":"150.00",
                            "ipap":"",
                            "mac":"00:44:56:56:78:17",
                            "ip":"192.168.33.3",
                            "instalado":"0000-00-00",
                            "pppuser":"User6",
                            "ppppass":"Pass6",
                            "tiposervicio":"internet",
                            "status_user":"OFFLINE",
                            "coordenadas":"-11.984449254433779,-77.0827752259944",
                            "direccion":"",
                            "snmp_comunidad":"public",
                            "perfil":"Plan 4Mbps"
                        }
                    ],
                    "facturacion":{
                        "facturas_nopagadas":4,
                        "total_facturas":"750.00"
                    }
                }
            ]
        }
        ```
        """

        data = {"cedula": ci}

        return self._make_request(MikrowispEndpoint.GET_CLIENTS, data)

    def get_list_installs(self, status: _InstallationType, ci: Optional[str]) -> Optional[dict[str, Any]]:
        """Get the list of installations.

        Attributes:
        status (str): The status of the installation
        ci (str): The cedula of the user to get the data

        Returns:
        dict[str, Any] | None: The result of the request

        Example:
        ```json
        {
            "estado": "exito",
            "instalaciones": [
                {
                    "id": 4,
                    "userid": 93,
                    "fecha_ingreso": "2018-10-30",
                    "fecha_salida": "0000-00-00",
                    "idtecnico": 0,
                    "direccion": "SAN CRESCENTE 240  101, Las Condes",
                    "telefono": "9652368914",
                    "movil": "933901439",
                    "idnodo": 0,
                    "email": "correo@gmail.com",
                    "cedula": "995658100",
                    "estate": "INSTALADO",
                    "cliente": "COMERCIAL C.W. CHILE LIMITADA",
                    "notas": "",
                    "fecha_instalacion": "0001-11-30 00:00:00",
                    "zona": 4,
                    "idvendedor": 0,
                    "cliente_pruebas": "",
                    "gaa": "",
                    "colonia": "",
                    "tipo_estrato": 0,
                    "N_orden": ""
                }
            ],
            "mensaje": "Se ha encontrado 1  Registros."
        }
        ```
        """

        if ci:
            data = {
                "estado": status,
                "cedula": ci
            }
        else:
            data = {
                "estado": status
            }

        return self._make_request(MikrowispEndpoint.LIST_INSTALLS, data)


if __name__ == "__main__":
    token = "R3Z4SlNrWVZvZzFsV1pvTTQ3ci9wZz09"
    usuario_id = 1

    service = SaragurosNetService(token)

    activar_result = service.activate_service(usuario_id)
    print("Resultado de activar_servicio:", activar_result)

    nuevo_ticket = Ticket(
        idcliente=usuario_id,
        contenido="Contenido del ticket",
        asunto="Asunto del ticket",
        dp="Soporte",
        fechavisita="2023-08-25",
        solicitante="Juan Gahona"
    )

    create_ticket_result = service.create_ticket(nuevo_ticket)
    print("Resultado de create_ticket:", create_ticket_result)
