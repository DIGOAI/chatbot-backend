from src.api.cases.base_use_cases import UseCaseBase
from src.api.repositories import ClientRepository
from src.common.models import ClientInsert


class GetClientByPhone(UseCaseBase):
    def __call__(self, client_phone: str):
        with self._session() as session:
            client_repository = ClientRepository(session)
            client = client_repository.get_client_by_phone(client_phone)

            if not client:
                # Create a new client
                new_client = ClientInsert.model_validate({"phone": client_phone})
                client = client_repository.add_client(new_client)

        return client
