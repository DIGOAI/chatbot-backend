from fastapi import APIRouter, Depends
from fastapi import status as STATUS

from src.middlewares import APITokenAuth, JWTBearer
from src.middlewares.jwt_bearer import Role
from src.models import Client, ClientInsert, GenericResponse
from src.use_cases import GetClients, RegisterNewClient

router = APIRouter(prefix="/client", tags=["Client"])


@router.get("/", dependencies=[Depends(JWTBearer(Role.ADMIN))], response_model=GenericResponse[list[Client]])
def get_clients():
    get_clients = GetClients()
    return get_clients()


@router.post("/", response_model=GenericResponse[Client], status_code=STATUS.HTTP_201_CREATED, dependencies=[Depends(APITokenAuth())])
def add_client(client_insert: ClientInsert):
    register_new_client = RegisterNewClient()
    return register_new_client(client_insert)
