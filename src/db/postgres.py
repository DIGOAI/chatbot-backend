from typing import Any, Optional

import psycopg2
from psycopg2.extensions import connection

from src.db import DbConnection
from src.logger import Logger


class PostgreSQLConnection(DbConnection):
    """Class to manage the connection to the PostgreSQL database."""

    def __init__(self, user: str, password: str, host: str, port: str, database: str):
        super().__init__()
        self._connection: Optional[connection] = None
        self._user = user
        self._password = password
        self._host = host
        self._port = port
        self._database = database

    def connect(self):
        """Connect to the PostgreSQL database."""
        try:
            conn_string = f"dbname={self._database} user={self._user} password={self._password} host={self._host} port={self._port}"
            self._connection = psycopg2.connect(conn_string)
            Logger.info("Database connected")
        except Exception as e:
            Logger.error(f"Error connecting to database: {e}")

    def execute_query(self,  # type: ignore
                      query: str,
                      params: Optional[tuple[Any, ...]] = None,
                      single: bool = False) -> Optional[list[tuple[Any, ...]] | tuple[Any, ...]]:
        """Execute a query to the PostgreSQL database.

        Parameters:
        query (str): The query to execute
        params (tuple[any] | None): The parameters to pass to the query (default None)
        single (bool): If the query returns a single result or not (default False)

        Returns:
        list[tuple] | None: The result of the query
        """
        try:
            if self._connection:
                with self._connection.cursor() as cursor:
                    cursor.execute(query, params)
                    Logger.info(f"Query executed: {cursor.query}")
                    self._connection.commit()

                    if single:
                        res = cursor.fetchone()
                        if res:
                            return res

                        return None

                    return cursor.fetchall()
            else:
                Logger.error("Not connection to the database")
                return None
        except Exception as e:
            Logger.error(f"Error executing the query: {e}")
            return None

    def execute_mutation(self, query: str, params: Optional[tuple[Any, ...]] = None) -> bool:
        """Execute a mutation to the PostgreSQL database.

        Parameters:
        query (str): The query to execute
        params (tuple[any] | None): The parameters to pass to the query (default None)

        Returns:
        bool: If the mutation was successful or not
        """
        try:
            if self._connection:
                with self._connection.cursor() as cursor:
                    cursor.execute(query, params)
                    self._connection.commit()
                    return True
            else:
                Logger.error("Not connection to the database")
                return False
        except Exception as e:
            Logger.error(f"Error executing the query: {e}")
            return False

    def close(self):
        if self._connection:
            self._connection.close()
            Logger.info("Database disconnected")


if __name__ == "__main__":
    import os

    db = PostgreSQLConnection(
        user=os.environ.get("DB_USER", "postgres"),
        password=os.environ.get("DB_PASSWORD", ""),
        host=os.environ.get("DB_HOST", "localhost"),
        port=os.environ.get("DB_PORT", "5432"),
        database=os.environ.get("DB_NAME", "postgres")
    )

    db.connect()
    db.close()
