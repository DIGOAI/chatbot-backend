from src.config.config import Config as _Config

# Singleton pattern to load environment variables only once.
Config = _Config.Instance()
