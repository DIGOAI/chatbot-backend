from typing import Any, Optional

import psycopg2
from psycopg2.extensions import connection


class PostgreSQLConnection:
    """ Class to manage the connection to the PostgreSQL database. """

    def __init__(self, user: str, password: str, host: str, port: str, database: str):
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
            print("Conexión exitosa a la base de datos.")
        except Exception as e:
            print("Error al conectar a la base de datos:", e)

    def execute_query(self, query: str, params: Optional[tuple[Any, ...]] = None) -> Optional[list[tuple]]:
        """Execute a query to the PostgreSQL database.

        Parameters:
        query (str): The query to execute
        params (tuple[any] | None): The parameters to pass to the query

        Returns:
        list[tuple] | None: The result of the query
        """
        try:
            if self._connection:
                with self._connection.cursor() as cursor:
                    cursor.execute(query, params)
                    self._connection.commit()
                    return cursor.fetchall()
            else:
                print("No hay conexión a la base de datos.")
                return None
        except Exception as e:
            print("Error al ejecutar la consulta:", e)
            return None

    def close(self):
        if self._connection:
            self._connection.close()


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
