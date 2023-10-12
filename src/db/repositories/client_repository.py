from sqlalchemy import select, update
from sqlalchemy.orm import Session

from src.common.models import Client, ClientInsert
from src.db.models import Client as ClientModel


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

        if not client:
            return None

        return Client.model_validate(client)

    def update_status_client(self, client_id: int, status: str):
        stmt = (
            update(ClientModel)
            .where(ClientModel.id == client_id)
            .values(last_state=status)
            .returning(ClientModel)
        )

        # self._session.execute(stmt)
        client_updated = self._session.scalars(stmt).one()
        self._session.commit()

        return Client.model_validate(client_updated)
