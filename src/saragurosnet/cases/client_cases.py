from src.common.cases import UseCaseBase
from src.common.models import Client, ClientInsert
from src.db.models import Client as ClientModel
from src.db.repositories import BaseRepository, ClientRepository


class ClientUseCases(UseCaseBase):
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
            client_repository = ClientRepository(session)
            client = client_repository.get_client_by_phone(client_phone)

            if not client:
                # Create a new client
                new_client = ClientInsert.model_validate({"phone": client_phone})
                client = client_repository.add_client(new_client)

        return client
