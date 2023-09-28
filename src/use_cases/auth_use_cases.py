from fastapi import status as STATUS

from src.models import LoginSchema, RegisterSchema, TokenSchema, User, create_response
from src.models.user import UserRole
from src.repositories import UserRepository
from src.use_cases.base_use_cases import UseCaseBase
from src.utils import decrypt, signJWT


def create_token_data(user: User) -> TokenSchema:
    payload = {
        "user_id": str(user.email),
        "role": user.role.value,
        "keyType": "PRIVATE",
        "exp_time_sec": 60 * 10
    }

    match user.role:
        case UserRole.ADMIN:
            payload["keyType"] = "PRIVATE"
            payload["exp_time_sec"] = 60 * 60

        case UserRole.WORKER:
            payload["keyType"] = "PRIVATE"
            payload["exp_time_sec"] = 60 * 10

        case UserRole.SUPPORT:
            payload["keyType"] = "SERVICE"
            payload["exp_time_sec"] = 60 * 60 * 24 * 365

    access_token, _ = signJWT(
        user_id=user.email,
        keyType=payload["keyType"],
        role=payload["role"],  # type: ignore
        exp_time_sec=payload["exp_time_sec"]
    )

    return TokenSchema(access_token=access_token)


class RegisterNewUser(UseCaseBase):

    def __call__(self, new_user: RegisterSchema):
        with self._session() as session:
            user_repository = UserRepository(session)
            user = user_repository.create(new_user)

        token_data = create_token_data(user)

        return create_response(token_data, "User registered", status_code=STATUS.HTTP_201_CREATED)


class LoginUser(UseCaseBase):

    def __call__(self, login: LoginSchema):
        with self._session() as session:
            user_repository = UserRepository(session)
            user = user_repository.get_user_by_email(login.email)

        if user is None:
            return create_response(None, "User not found", status_code=STATUS.HTTP_404_NOT_FOUND, status="error")

        if not decrypt(login.password, user.password):
            return create_response(None, "Wrong password", status_code=STATUS.HTTP_401_UNAUTHORIZED, status="error")

        token_data = create_token_data(user)

        return create_response(token_data, "User logged", status_code=STATUS.HTTP_200_OK)
