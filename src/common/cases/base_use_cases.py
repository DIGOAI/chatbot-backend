from src.db import Session


class UseCaseBase():
    def __init__(self):
        self._session = Session
