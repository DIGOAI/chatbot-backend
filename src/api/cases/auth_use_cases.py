from typing import TypedDict

from src.api.utils import decrypt, signJWT
from src.common.cases import UseCaseBase
from src.common.models import LoginSchema, RegisterSchema, TokenSchema, User
from src.common.models.user import SystemRole
from src.db.models import User as UserModel
from src.db.repositories.base_repository import BaseRepository


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
            user_repository = BaseRepository(UserModel, User, session)
            user = user_repository.add(new_user.model_dump())

        token_data = _create_token_data(user)
        return token_data

    def login_user(self, login: LoginSchema):
        with self._session() as session:
            user_repository = BaseRepository(UserModel, User, session)
            user = user_repository.filter(UserModel.email == login.email, first=True)

        if user is None or not decrypt(login.password, user.password):
            return None

        token_data = _create_token_data(user)
        return token_data
