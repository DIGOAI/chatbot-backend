from src.chatbot.utils import Requester
from src.common.logger import Logger
from src.common.models import Client, GenericResponse


class BackendService():
    """BackendService class to handle the backend service."""

    def __init__(self, base_url: str, token: str) -> None:
        self._fetcher = Requester(base_url, token)

    def get_user_by_phone(self, phone: str):

        try:
            res = self._fetcher.make_request("GET", f"/api/v1/client/{phone}", response_model=GenericResponse[Client])

            if res is None:
                return None

            return res.data

        except Exception as e:
            Logger.error(f"Error getting user by phone: {phone} | {e}")
            return None

    def get_saraguros_data_from_ci(self, ci: str):

        try:
            res = self._fetcher.make_request("GET", f"/api/v1/saraguros/{ci}", response_model=GenericResponse[Client])

            if res is None:
                return None

            return res.data

        except Exception as e:
            Logger.error(f"Error getting saraguros data from ci: {ci} | {e}")
            return None