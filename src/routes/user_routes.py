from fastapi import APIRouter
from sqlalchemy import select

from src.db import Session
from src.logger import Logger
from src.models.user import User, UserModel

router = APIRouter(prefix="/user")


@router.get("/")
def get_users(company: str) -> list[User]:
    Logger.info(f"Company: {company}")

    with Session.begin() as session:
        user = UserModel(name="test", ci="1234567890", phone="0987654321", last_state="test", saraguros_id=1)
        print(user)

        session.add(user)
        # raise Exception("test")

        # insert_stm = insert(UserModel).values(name="test", ci="1234567890",
        #                                       phone="0987654321", last_state="test", saraguros_id=1)
        # res = session.execute(insert_stm.returning(UserModel)).scalar()

        # session.commit()

        users = session.query(UserModel).all()
        users = session.execute(select(UserModel)).scalars().all()

        users = [User.model_validate(user) for user in users]

    return users
