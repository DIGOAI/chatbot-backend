from sqlalchemy import select
from sqlalchemy.orm import Session

from src.db.models import Client as ClientModel
from src.models.user import User, UserInsert


class UserService():
    def __init__(self, session: Session) -> None:
        self._session = session

    def get_all_users(self):
        users = self._session.execute(select(ClientModel)).scalars().all()
        return [User.model_validate(user) for user in users]

    def add_user(self, user: UserInsert):
        user_model = ClientModel(**user.model_dump())
        self._session.add(user_model)
        return user_model
