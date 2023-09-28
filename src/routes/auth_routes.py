from fastapi import APIRouter, Body

from src.models import GenericResponse, LoginSchema, RegisterSchema, TokenSchema
from src.use_cases import LoginUser, RegisterNewUser

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/login", response_model=GenericResponse[TokenSchema])
def login(signin: LoginSchema = Body(...)):
    login_user = LoginUser()
    return login_user(signin)


@router.post("/register", response_model=GenericResponse[TokenSchema], status_code=201)
def register(register_data: RegisterSchema = Body(...)):
    register_user = RegisterNewUser()
    return register_user(register_data)
