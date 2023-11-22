from typing import TypedDict

from fastapi import status as STATUS

from src.api.utils import decrypt, signJWT
from src.common.cases import UseCaseBase
from src.common.models import (
    LoginSchema,
    RegisterSchema,
    TokenSchema,
    User,
    create_response,
)
from src.common.models.user import SystemRole
from src.db.repositories import UserRepository


class TokenPayload(TypedDict):
    user_id: str
    role: str
    keyType: str
    exp_time_sec: int


def _create_token_data(user: User) -> TokenSchema:
    payload: TokenPayload = {
        "user_id": str(user.email),
        "role": user.system_role.value,
        "keyType": "PRIVATE",
        "exp_time_sec": 60 * 10
    }

    match user.system_role:
        case SystemRole.ADMIN:
            payload["keyType"] = "PRIVATE"
            payload["exp_time_sec"] = 60 * 60

        case SystemRole.WORKER:
            payload["keyType"] = "PRIVATE"
            payload["exp_time_sec"] = 60 * 10

        case SystemRole.SUPPORT:
            payload["keyType"] = "SERVICE"
            payload["exp_time_sec"] = 60 * 60 * 24 * 365

        case SystemRole.OTHER:
            payload["keyType"] = "SERVICE"
            payload["exp_time_sec"] = 60 * 1

    access_token, _ = signJWT(
        user_id=user.email,
        keyType=payload["keyType"],
        role=payload["role"],
        exp_time_sec=payload["exp_time_sec"]
    )

    return TokenSchema(access_token=access_token)


class UserUseCases(UseCaseBase):

    def register_user(self, new_user: RegisterSchema):
        with self._session() as session:
            user_repository = UserRepository(session)
            user = user_repository.create(new_user)

        token_data = _create_token_data(user)

        return create_response(token_data, "User registered", status_code=STATUS.HTTP_201_CREATED)

    def login_user(self, login: LoginSchema):
        with self._session() as session:
            user_repository = UserRepository(session)
            user = user_repository.get_user_by_email(login.email)

        if user is None:
            return create_response(None, "User not found", status_code=STATUS.HTTP_404_NOT_FOUND, status="error")

        if not decrypt(login.password, user.password):
            return create_response(None, "Wrong password", status_code=STATUS.HTTP_401_UNAUTHORIZED, status="error")

        token_data = _create_token_data(user)

        return create_response(token_data, "User logged", status_code=STATUS.HTTP_200_OK)
