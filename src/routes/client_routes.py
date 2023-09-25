from fastapi import APIRouter
from fastapi import status as STATUS

from src.db import Session
from src.logger import Logger
from src.models import Client, ClientInsert, GenericResponse, create_response
from src.services import ClientService

router = APIRouter(prefix="/client", tags=["Client"])


@router.get("/")
def get_users(company: str) -> list[Client]:
    Logger.info(f"Company: {company}")

    with Session.begin() as session:
        user_service = ClientService(session)
        users = user_service.get_all_users()

    return users


@router.post("/", response_model=GenericResponse[Client], status_code=STATUS.HTTP_201_CREATED)
def add_user(user_insert: ClientInsert):
    Logger.info(f"User: {user_insert}")

    with Session() as session:
        user_service = ClientService(session)
        user_inserted = user_service.add_user(user_insert)
        session.commit()
        session.refresh(user_inserted)

    if not user_inserted:
        return {"message": "Client Salready exists", "status": "error"}

    user_i = Client.model_validate(user_inserted)
    return create_response(user_i, "Client added successfully", status_code=STATUS.HTTP_201_CREATED)
