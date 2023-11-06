from typing import Literal

from src.common.cases.base_use_cases import UseCaseBase
from src.common.models.client import Client
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
