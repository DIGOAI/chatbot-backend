from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import User as UserModel
from src.models import RegisterSchema, User
from src.utils import encrypt


class UserRepository():
    def __init__(self, session: Session):
        self._session = session

    def create(self, new_user: RegisterSchema) -> User:
        password_hashed = encrypt(new_user.password)
        new_user.password = password_hashed
        user_model = UserModel(**new_user.model_dump())
        self._session.add(user_model)
        self._session.commit()
        self._session.refresh(user_model)
        user_created = User.model_validate(user_model)
        return user_created

    def get_user_by_email(self, email: str) -> User | None:
        stmt = select(UserModel).filter(UserModel.email == email)
        user = self._session.scalars(stmt).first()
        if user is None:
            return None
        return User.model_validate(user)
