from src.api.cases.base_use_cases import UseCaseBase
from src.api.repositories import ClientRepository


class GetClientByPhone(UseCaseBase):
    def __call__(self, client_phone: str):
        with self._session() as session:
            client_repository = ClientRepository(session)
            client = client_repository.get_client_by_phone(client_phone)

        return client
