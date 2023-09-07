from typing import (Any, LiteralString, Mapping, Optional, Self, Sequence,
                    Type, TypeVar)

import psycopg
from psycopg import Connection
from psycopg.rows import DictRow, class_row, dict_row

from src.db import DbConnection
from src.logger import Logger

T = TypeVar('T')


class PostgreSQLConnection(DbConnection):
    """Class to manage the connection to the PostgreSQL database."""

    def __init__(self, user: str, password: str, host: str, port: str, database: str):
        super().__init__()
        self._connection: Optional[Connection[DictRow]] = None
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database

    def __enter__(self) -> Self:
        """Connect to the PostgreSQL database."""
        try:
            conn_string = f"dbname={self._database} user={self._user} password={self._password} host={self._host} port={self._port}"
            self._connection = psycopg.connect(conn_string, row_factory=dict_row)
            Logger.info("Database connected")
            return self
        except Exception as e:
            Logger.error(f"Error connecting to database: {e}")
            raise e

    def execute_query(self,  # type: ignore
                      query: LiteralString,
                      params: Optional[Sequence[Any] | Mapping[str, Any]] = None,
                      bound: Type[T] = DictRow,
                      single: bool = False) -> list[T] | T | None:
        """Execute a query to the PostgreSQL database.

        Parameters:
        query (str): The query to execute
        params (tuple[any] | list[any] | dict[str, any] | None): The parameters to pass to the query (default None)
        bound (type): The type of the result of the query (default DictRow)
        single (bool): If the query returns a single result or not (default False)

        Returns:
        list[tuple] | None: The result of the query
        """
        try:
            if self._connection:
                with self._connection.cursor(row_factory=class_row(bound)) as cur:
                    cur.execute(query, params)
                    Logger.info(f"Query executed: {cur._query.query.decode() if cur._query else query}")  # type: ignore
                    self._connection.commit()

                    if single:
                        return cur.fetchone()

                    return cur.fetchall()
            else:
                Logger.error("Not connection to the database")
                return None
        except Exception as e:
            Logger.error(f"Error executing the query: {e}")
            return None

    def execute_mutation(self, query: LiteralString, params: Optional[Sequence[Any] | Mapping[str, Any]] = None) -> bool:
        """Execute a mutation to the PostgreSQL database.

        Parameters:
        query (str): The query to execute
        params (tuple[any] | list[any] | dict[str, any] | None): The parameters to pass to the query (default None)

        Returns:
        bool: If the mutation was successful or not
        """
        try:
            if self._connection:
                with self._connection.cursor() as cur:
                    cur.execute(query, params)
                    self._connection.commit()
                    return True
            else:
                Logger.error("Not connection to the database")
                return False
        except Exception as e:
            Logger.error(f"Error executing the query: {e}")
            return False

    def __exit__(self, exc_type: Optional[Type[BaseException]], exc_value: Optional[BaseException], traceback: Optional[Any]):
        if self._connection:
            try:
                self._connection.close()
                Logger.info("Database disconnected")
            except Exception as e:
                Logger.error(f"Error disconnecting to database: {e}")
                raise e
