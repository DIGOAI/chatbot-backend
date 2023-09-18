from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user import User, UserInsert, UserModel


class UserService():
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all_users(self):
        users = self._session.execute(select(UserModel)).scalars().all()
        return [User.model_validate(user) for user in users]

    def add_user(self, user: UserInsert):
        user_model = UserModel(**user.model_dump())
        self._session.add(user_model)
        return user_model
