import os
from datetime import datetime
from typing import cast

from src.db import PostgreSQLConnection
from src.logger import Logger
from src.models import User

if __name__ == "__main__":
    conn_params = {
        "user": os.environ.get("DB_USER", "postgres"),
        "password": os.environ.get("DB_PASSWORD", ""),
        "host": os.environ.get("DB_HOST", "localhost"),
        "port": os.environ.get("DB_PORT", "5432"),
        "database": os.environ.get("DB_NAME", "postgres")
    }

    with PostgreSQLConnection(**conn_params) as conn:
        new_user = User(id=0, ci="1900512623", name="Juan Gahona", phone="0999999999", last_state="1.0",
                        saraguros_id=1, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        Logger.info(new_user.model_dump_json())

        INSERT_QUERY = "INSERT INTO users (ci, name, phone, last_state, saraguros_id) VALUES (%s, %s, %s, %s, %s)"
        SELECT_QUERY = "SELECT * FROM users WHERE ci = %s"
        DELETE_QUERY = "DELETE FROM users WHERE ci = %s"

        res = conn.execute_mutation(query=INSERT_QUERY, params=(new_user.ci, new_user.name,
                                    new_user.phone, new_user.last_state, new_user.saraguros_id))

        if res:
            Logger.info("User created successfully")

        res = conn.execute_query(query=SELECT_QUERY, params=(new_user.ci,), bound=User, single=True)

        if res:
            Logger.info(cast(User, res).model_dump_json())

            res = conn.execute_mutation(query=DELETE_QUERY, params=(new_user.ci,))

            if res:
                Logger.info("User deleted successfully")

            else:
                Logger.info("User not deleted")
        else:
            Logger.info("User not found")
