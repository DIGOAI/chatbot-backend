from fastapi import APIRouter, Body

from src.api.cases import UserUseCases
from src.common.models import GenericResponse, LoginSchema, RegisterSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=GenericResponse[TokenSchema])
def login(signin: LoginSchema = Body(...)):
    return UserUseCases().login_user(signin)


@router.post("/register", response_model=GenericResponse[TokenSchema], status_code=201)
def register(register_data: RegisterSchema = Body(...)):
    return UserUseCases().register_user(register_data)
