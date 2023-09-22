from typing import Any, TypedDict

from psycopg import Cursor
from sqlalchemy import Connection, ExecutionContext, create_engine
from sqlalchemy.engine.url import URL
from sqlalchemy.event import listens_for
from sqlalchemy.orm.session import sessionmaker
from sqlalchemy.util import immutabledict

from src.config import Config as _Config
from src.logger import Logger

ConnectionDataType = TypedDict("ConnectionDataType", {
    "drivername": str,
    "database": str,
    "username": str,
    "password": str,
    "host": str,
    "port": int,
    "query": immutabledict[str, tuple[str, ...] | str]
})

_connection_data: ConnectionDataType = {
    'drivername': 'postgresql+psycopg',
    'database': _Config.DB_NAME,
    'username': _Config.DB_USER,
    'password': _Config.DB_PASSWORD,
    'host': _Config.DB_HOST,
    'port': int(_Config.DB_PORT),
    'query': immutabledict({})
}

_database_url = URL(**_connection_data)

_NAME = "database"

Logger.info(f"Database URL: {_database_url}", caller_name=_NAME)
engine = create_engine(_database_url, echo=False)


@listens_for(engine, "before_cursor_execute", named=True)
def before_cursor_execute(conn: Connection,
                          cursor: Cursor[Any],
                          statement: str,
                          parameters: dict[str, Any],
                          context: ExecutionContext,
                          executemany: bool):
    formatted_statement = statement.replace('\n', '') % parameters
    Logger.info(f"Query: {formatted_statement}", caller_name=_NAME)


Session = sessionmaker(bind=engine)
