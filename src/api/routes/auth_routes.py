from fastapi import APIRouter, Body
from fastapi import status as STATUS

from src.common.cases import UserUseCases
from src.common.models import (
    GenericResponse,
    LoginSchema,
    RegisterSchema,
    TokenSchema,
    create_response,
)

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=GenericResponse[TokenSchema])
def login(signin: LoginSchema = Body(...)):
    token = UserUseCases().login_user(signin)

    if token is None:
        return create_response(None, "User or password is incorrect.", status_code=STATUS.HTTP_401_UNAUTHORIZED, status="error")

    return create_response(token, "User logged", status_code=STATUS.HTTP_200_OK)


@router.post("/register", response_model=GenericResponse[TokenSchema], status_code=201)
def register(register_data: RegisterSchema = Body(...)):
    token = UserUseCases().register_user(register_data)
    return create_response(token, "User registered", status_code=STATUS.HTTP_201_CREATED)
