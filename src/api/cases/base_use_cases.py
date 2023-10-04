from src.api.db import Session


class UseCaseBase():
    def __init__(self):
        self._session = Session
