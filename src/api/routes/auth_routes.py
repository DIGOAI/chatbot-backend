from fastapi import APIRouter, Body

from src.api.cases import LoginUser, RegisterNewUser
from src.common.models import GenericResponse, LoginSchema, RegisterSchema, TokenSchema

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=GenericResponse[TokenSchema])
def login(signin: LoginSchema = Body(...)):
    login_user = LoginUser()
    return login_user(signin)


@router.post("/register", response_model=GenericResponse[TokenSchema], status_code=201)
def register(register_data: RegisterSchema = Body(...)):
    register_user = RegisterNewUser()
    return register_user(register_data)
