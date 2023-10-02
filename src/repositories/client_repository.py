from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import Client as ClientModel
from src.models import Client, ClientInsert


class ClientRepository():
    def __init__(self, session: Session):
        self._session = session

    def get_all_clients(self):
        stmt = select(ClientModel)
        clients = self._session.scalars(stmt).all()
        return [Client.model_validate(user) for user in clients]

    def add_client(self, client: ClientInsert):
        client_model = ClientModel(**client.model_dump())
        self._session.add(client_model)
        self._session.commit()
        self._session.refresh(client_model)
        client_created = Client.model_validate(client_model)
        return client_created

    def get_client_by_phone(self, client_phone: str):
        stmt = select(ClientModel).where(ClientModel.phone == client_phone)
        client = self._session.scalars(stmt).first()
        return Client.model_validate(client)
