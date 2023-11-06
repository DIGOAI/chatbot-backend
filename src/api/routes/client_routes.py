from fastapi import APIRouter, Depends

from src.api.cases import GetClients
from src.api.middlewares import JWTBearer
from src.api.middlewares.jwt_bearer import Role
from src.common.models import Client, GenericResponse

router = APIRouter(prefix="/client", tags=["Client"])


_worker_dependency = Depends(JWTBearer(Role.WORKER))


@router.get("/", dependencies=[_worker_dependency], response_model=GenericResponse[list[Client]])
def get_clients():
    get_clients = GetClients()
    return get_clients()


# @router.post("/", response_model=GenericResponse[Client], status_code=STATUS.HTTP_201_CREATED)
# def add_client(client_insert: ClientInsert):
#     register_new_client = RegisterNewClient()
#     return register_new_client(client_insert)


# @router.get("/{client_phone}", response_model=GenericResponse[Client], dependencies=[Depends(APITokenAuth())])
# def get_client_by_phone(client_phone: str):
#     get_client_by_phone = GetClientByPhone()
#     return get_client_by_phone(client_phone)


# @router.post("/activate")
# def activate_client(client_id: Annotated[str, Body(...)]):
#     raise HTTPException(status_code=501, detail="Not implemented")


# @router.post("/deactivate")
# def deactivate_client(client_id: Annotated[str, Body(...)]):
#     raise HTTPException(status_code=501, detail="Not implemented")
