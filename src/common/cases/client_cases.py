from typing import Literal

from src.common.cases.base_use_cases import UseCaseBase
from src.common.models.client import Client, ClientInsert
from src.db.models.client import Client as ClientModel
from src.db.repositories import BaseRepository

ClientType = Literal["all", "client", "non_client"]


class ClientUseCases(UseCaseBase):

    def get_clients(self, type: ClientType = "all"):
        with self._session() as session:
            client_repo = BaseRepository(ClientModel, Client, session)
            if type == "all":
                clients = client_repo.list()
            elif type == "client":
                clients = client_repo.filter(ClientModel.saraguros_id.isnot(None))
            elif type == "non_client":
                clients = client_repo.filter(ClientModel.saraguros_id.is_(None))
            else:
                raise ValueError(f"Invalid client type: {type}")

        return clients

    def update_client(self, client: Client):
        with self._session() as session:
            client_repo = BaseRepository(ClientModel, Client, session)
            client_updated = client_repo.update(client.id, client.model_dump())

        return client_updated

    def get_client_by_ci(self, client_ci: str, phone: str):
        with self._session() as session:
            client_repo = BaseRepository(ClientModel, Client, session)
            client = client_repo.filter(ClientModel.ci == client_ci, first=True)

            # Create a new client if not exists
            if not client:
                new_client = ClientInsert.model_validate({"ci": client_ci, "phone": phone})
                client = client_repo.add(new_client.model_dump())

        return client

    def get_client_by_phone(self, client_phone: str):
        with self._session() as session:
            client_repo = BaseRepository(ClientModel, Client, session)
            client = client_repo.filter(ClientModel.phone == client_phone, first=True)

            if not client:
                # Create a new client
                new_client = ClientInsert.model_validate({"phone": client_phone})
                client = client_repo.add(new_client.model_dump())

        return client
