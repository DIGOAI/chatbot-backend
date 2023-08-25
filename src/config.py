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
        self.db_user = os.environ.get("DB_USER", "postgres")
        self.db_password = os.environ.get("DB_PASSWORD")
        self.db_host = os.environ.get("DB_HOST", "localhost")
        self.db_port = os.environ.get("DB_PORT", "5432")
        self.db_name = os.environ.get("DB_NAME", "postgres")

        self.saraguros_api_url = os.environ.get("SARAGUROS_API_URL")
        self.saraguros_token = os.environ.get("SARAGUROS_TOKEN")

        self._verify()

    def _verify(self):
        """ Verify that all required environment variables are set. """
        if not self.db_password:
            raise ValueError("DB_PASSWORD is not set")
        if not self.saraguros_api_url:
            raise ValueError("SARAGUROS_API_URL is not set")
        if not self.saraguros_token:
            raise ValueError("SARAGUROS_TOKEN is not set")


# Export a single instance of Config
config = Config()

if __name__ == "__main__":
    print("DB_USER (config1):", config.db_user)

    config2 = Config()
    print("DB_USER (config2):", config2.db_user)

    print("config1 is config2:", config is config2)
