from fastapi import APIRouter
from fastapi import status as STATUS

from src.db import Session
from src.logger import Logger
from src.models import Client, ClientInsert, GenericResponse, create_response
from src.services import ClientService

router = APIRouter(prefix="/client", tags=["Client"])


@router.get("/")
def get_clients(company: str) -> list[Client]:
    Logger.info(f"Company: {company}")

    with Session.begin() as session:
        client_service = ClientService(session)
        clients = client_service.get_all_users()

    return clients


@router.post("/", response_model=GenericResponse[Client], status_code=STATUS.HTTP_201_CREATED)
def add_client(client_insert: ClientInsert):
    Logger.info(f"Client: {client_insert}")

    with Session() as session:
        client_service = ClientService(session)
        client_inserted = client_service.add_user(client_insert)
        session.commit()
        session.refresh(client_inserted)

    if not client_inserted:
        return {"message": "Client already exists", "status": "error"}

    client = Client.model_validate(client_inserted)
    return create_response(client, "Client added successfully", status_code=STATUS.HTTP_201_CREATED)
