from fastapi import status as STATUS

from src.api.cases.base_use_cases import UseCaseBase
from src.api.repositories import ClientRepository
from src.common.models import ClientInsert, create_response


class RegisterNewClient(UseCaseBase):
    def __call__(self, new_client: ClientInsert):
        with self._session() as session:
            client_repository = ClientRepository(session)
            client = client_repository.add_client(new_client)

        return create_response(client, "Client registered", status_code=STATUS.HTTP_201_CREATED)


class GetClients(UseCaseBase):
    def __call__(self):
        with self._session() as session:
            client_repository = ClientRepository(session)
            clients = client_repository.get_all_clients()

        return create_response(clients, "Clients retrieved")


class GetClientByPhone(UseCaseBase):
    def __call__(self, client_phone: str):
        with self._session() as session:
            client_repository = ClientRepository(session)
            client = client_repository.get_client_by_phone(client_phone)

        return create_response(client, "Client retrieved")
