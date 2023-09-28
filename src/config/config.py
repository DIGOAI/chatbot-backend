import os

from src.logger import Logger

Logger.add_func_names_to_ignore(["before_cursor_execute"])
Logger.module_char_length = 25


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

        self.DB_USER = os.environ.get("PGUSER", "postgres")
        self.DB_PASSWORD = os.environ.get("PGPASSWORD", "")
        self.DB_HOST = os.environ.get("PGHOST", "localhost")
        self.DB_PORT = os.environ.get("PGPORT", "5432")
        self.DB_NAME = os.environ.get("PGDATABASE", "postgres")

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
            Logger.error(str(e), caller_name=self._NAME)
            raise SystemExit(1)

    def _verify(self):
        """ Verify that all required environment variables are set. """

        ATTRIBUTES_TO_VERIFY = [
            self.DB_PASSWORD,
            self.SARAGUROS_API_URL,
            self.SARAGUROS_API_TOKEN,
            self.OCR_LAMBDA_URL,
            self.TWILIO_SID,
            self.TWILIO_TOKEN,
            self.ALLOWED_ORIGINS,
            self.JWT_SECRET,
            self.JWT_ALGORITHM,
        ]

        # Get attribute names in string format
        ATTRIBUTES_TO_VERIFY_NAMES = [
            attr_name
            for attr_name in dir(self)
            if not callable(getattr(self, attr_name)) and not attr_name.startswith("__")
        ]

        # Verify that all attributes are set
        for attr in ATTRIBUTES_TO_VERIFY:
            # Get attribute name
            attr_name = ATTRIBUTES_TO_VERIFY_NAMES[ATTRIBUTES_TO_VERIFY.index(attr)]

            # Verify attributes
            if isinstance(attr, str):
                if not attr.strip():
                    raise ValueError(f"{attr_name} is not set")
            elif not attr:
                raise ValueError(f"{attr_name} is not set")
