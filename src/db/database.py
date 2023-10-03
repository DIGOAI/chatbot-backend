from typing import Any

from psycopg import Cursor
from sqlalchemy import Connection, ExecutionContext, create_engine
from sqlalchemy.event import listens_for
from sqlalchemy.orm.session import sessionmaker

from src.config import Config as _Config
from src.logger import Logger

_database_url = _Config.DATABASE_URL.replace("postgresql://", "postgresql+psycopg://")

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
