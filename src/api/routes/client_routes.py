from typing import Annotated

from fastapi import APIRouter, Body, Depends, HTTPException
from fastapi import status as STATUS

from src.api.cases import GetClients, RegisterNewClient
from src.api.middlewares import APITokenAuth, JWTBearer
from src.api.middlewares.jwt_bearer import Role
from src.common.models import Client, ClientInsert, GenericResponse

router = APIRouter(prefix="/client", tags=["Client"])


@router.get("/", dependencies=[Depends(JWTBearer(Role.ADMIN))], response_model=GenericResponse[list[Client]])
def get_clients(limit: int = 50, offset: int = 0):
    get_clients = GetClients()
    return get_clients()


@router.post("/", response_model=GenericResponse[Client], status_code=STATUS.HTTP_201_CREATED, dependencies=[Depends(APITokenAuth())])
def add_client(client_insert: ClientInsert):
    register_new_client = RegisterNewClient()
    return register_new_client(client_insert)


# @router.get("/{client_phone}", response_model=GenericResponse[Client], dependencies=[Depends(APITokenAuth())])
# def get_client_by_phone(client_phone: str):
#     get_client_by_phone = GetClientByPhone()
#     return get_client_by_phone(client_phone)


@router.post("/activate", dependencies=[Depends(APITokenAuth())])
def activate_client(client_id: Annotated[str, Body(...)]):
    raise HTTPException(status_code=501, detail="Not implemented")


@router.post("/deactivate", dependencies=[Depends(APITokenAuth())])
def deactivate_client(client_id: Annotated[str, Body(...)]):
    raise HTTPException(status_code=501, detail="Not implemented")
