import urllib.parse

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm.session import sessionmaker

from src.config import Config as _Config
from src.logger import Logger

_connection_data = {
    'dbname': _Config.DB_NAME,
    'user': _Config.DB_USER,
    'password': urllib.parse.quote_plus(_Config.DB_PASSWORD),
    'host': _Config.DB_HOST,
    'port': _Config.DB_PORT
}

_database_url = "postgresql+psycopg://{user}:{password}@{host}:{port}/{dbname}".format(**_connection_data)

Logger.info(f"Database URL: {_database_url}")
engine = create_engine(_database_url, echo=True)

Session = sessionmaker(bind=engine)


class Base(DeclarativeBase):
    pass
