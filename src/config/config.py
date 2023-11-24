import os

from src.common.logger import Logger


class Config:
    """Config class to load environment variables."""

    _instance = None
    _NAME = "config"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            Logger.info("Loading config", caller_name=cls._NAME)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """ Load environment variables. """
        self.ENVIRONMENT = os.environ.get("ENVIRONMENT", "development")

        self.DATABASE_URL = os.environ.get("DATABASE_URL", "")
        self.BACKEND_URL = os.environ.get("RAILWAY_PUBLIC_DOMAIN", "")

        self.SARAGUROS_API_URL = os.environ.get("SARAGUROS_API_URL", "")
        self.SARAGUROS_API_TOKEN = os.environ.get("SARAGUROS_API_TOKEN", "")

        self.OCR_LAMBDA_URL = os.environ.get("OCR_LAMBDA_URL", "")

        self.TWILIO_SID = os.environ.get("TWILIO_SID", "")
        self.TWILIO_TOKEN = os.environ.get("TWILIO_TOKEN", "")
        self.TWILIO_SENDER: str = os.environ.get("TWILIO_SENDER", "")

        self.ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "*").split(",")

        self.JWT_SECRET = os.environ.get("JWT_SECRET", default="")
        self.JWT_ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")

        self.X_API_KEY = os.environ.get("X_API_KEY", "")

        self.SMTP_HOST: str = os.environ.get("SMTP_HOST", "")
        self.SMTP_PORT: int = int(os.environ.get("SMTP_PORT", 587))
        self.SMTP_USER: str = os.environ.get("SMTP_USER", "")
        self.SMTP_PASSWORD: str = os.environ.get("SMTP_PASSWORD", "")
        self.SMTP_SENDER: str = os.environ.get("SMTP_SENDER", self.SMTP_USER or "")

        self.OPENAI_KEY = os.environ.get("OPENAI_KEY", "")

        try:
            self._verify()
        except ValueError as e:
            Logger.error(str(e), caller_name=self._NAME)
            raise SystemExit(1)

    def _verify(self):
        """ Verify that all required environment variables are set. """

        if self.ENVIRONMENT == "development":
            return

        ATTRIBUTES_TO_VERIFY = [
            "DATABASE_URL",
            "JWT_SECRET",
            "OPENAI_KEY",
            "SARAGUROS_API_TOKEN",
            "SARAGUROS_API_URL",
            "TWILIO_SENDER",
            "TWILIO_SID",
            "TWILIO_TOKEN",
            "SMTP_HOST",
            "SMTP_USER",
            "SMTP_PASSWORD",
        ]

        # Verify that all attributes are set
        for attr_name in ATTRIBUTES_TO_VERIFY:
            # Get attribute
            attr = getattr(self, attr_name)

            # Verify attributes
            if isinstance(attr, str) and attr.strip():  # type: ignore
                pass
            elif not attr:
                raise ValueError(f"{attr_name} is not set")
