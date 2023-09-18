from fastapi import APIRouter
from fastapi import status as STATUS

from src.db import Session
from src.logger import Logger
from src.models import GenericResponse, create_response
from src.models.user import User, UserInsert
from src.services import UserService

router = APIRouter(prefix="/user", tags=["User"])


@router.get("/")
def get_users(company: str) -> list[User]:
    Logger.info(f"Company: {company}")

    with Session.begin() as session:
        user_service = UserService(session)
        users = user_service.get_all_users()

    return users


@router.post("/", response_model=GenericResponse[User], status_code=STATUS.HTTP_201_CREATED)
def add_user(user_insert: UserInsert):
    Logger.info(f"User: {user_insert}")

    with Session() as session:
        user_service = UserService(session)
        user_inserted = user_service.add_user(user_insert)
        session.commit()
        session.refresh(user_inserted)

    if not user_inserted:
        return {"message": "User Salready exists", "status": "error"}

    user_i = User.model_validate(user_inserted)
    return create_response(user_i, "User added successfully", status_code=STATUS.HTTP_201_CREATED)
