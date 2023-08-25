import os


class Config:
    """ Config class to load environment variables. """

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self):
        """ Load environment variables. """

        print("[INFO] Loading config...")

        self.DB_USER = os.environ.get("DB_USER", "postgres")
        self.DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
        self.DB_HOST = os.environ.get("DB_HOST", "localhost")
        self.DB_PORT = os.environ.get("DB_PORT", "5432")
        self.DB_NAME = os.environ.get("DB_NAME", "postgres")

        self.SARAGUROS_API_URL = os.environ.get("SARAGUROS_API_URL", "")
        self.SARAGUROS_API_TOKEN = os.environ.get("SARAGUROS_API_TOKEN", "")

        self._verify()

    def _verify(self):
        """ Verify that all required environment variables are set. """

        if not self.DB_PASSWORD.strip():
            raise ValueError("DB_PASSWORD is not set")
        if not self.SARAGUROS_API_URL.strip():
            raise ValueError("SARAGUROS_API_URL is not set")
        if not self.SARAGUROS_API_TOKEN.strip():
            raise ValueError("SARAGUROS_API_TOKEN is not set")


# Export a single instance of Config
config = Config()

if __name__ == "__main__":
    print("DB_USER (config1):", config.DB_USER)

    config2 = Config()
    print("DB_USER (config2):", config2.DB_USER)

    print("config1 is config2:", config is config2)
