import os

from src.logger import Logger


class Config:
    """Config class to load environment variables."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            Logger.info("Loading config...")
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """ Load environment variables. """

        self.DB_USER = os.environ.get("DB_USER", "postgres")
        self.DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
        self.DB_HOST = os.environ.get("DB_HOST", "localhost")
        self.DB_PORT = os.environ.get("DB_PORT", "5432")
        self.DB_NAME = os.environ.get("DB_NAME", "postgres")

        self.SARAGUROS_API_URL = os.environ.get("SARAGUROS_API_URL", "")
        self.SARAGUROS_API_TOKEN = os.environ.get("SARAGUROS_API_TOKEN", "")

        self.OCR_LAMBDA_URL = os.environ.get("OCR_LAMBDA_URL", "")

        self.TWILIO_SID = os.environ.get("TWILIO_SID", "")
        self.TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN", "")
        self.ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

        self.JWT_SECRET = os.environ.get("JWT_SECRET", default="")
        self.JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

        try:
            self._verify()
        except ValueError as e:
            Logger.error(str(e))
            raise SystemExit(1)

    def _verify(self):
        """ Verify that all required environment variables are set. """

        if not self.DB_PASSWORD.strip():
            raise ValueError("DB_PASSWORD is not set")
        if not self.SARAGUROS_API_URL.strip():
            raise ValueError("SARAGUROS_API_URL is not set")
        if not self.SARAGUROS_API_TOKEN.strip():
            raise ValueError("SARAGUROS_API_TOKEN is not set")
        if not self.OCR_LAMBDA_URL.strip():
            raise ValueError("OCR_LAMBDA_URL is not set")
        if not self.TWILIO_SID.strip():
            raise ValueError("TWILIO_SID is not set")
        if not self.TWILIO_TOKEN.strip():
            raise ValueError("TWILIO_TOKEN is not set")
        if not self.ALLOWED_ORIGINS:
            raise ValueError("ALLOWED_ORIGINS is not set")
        if not self.JWT_SECRET.strip():
            raise ValueError("JWT_SECRET is not set")
        if not self.JWT_ALGORITHM.strip():
            raise ValueError("JWT_ALGORITHM is not set")
