from src.config import Config
from src.db import PostgreSQLConnection


def main():
    db = PostgreSQLConnection(
        user=Config.DB_USER,
        password=Config.DB_PASSWORD,
        host=Config.DB_HOST,
        port=Config.DB_PORT,
        database=Config.DB_NAME
    )
    db.connect()
    db.close()


if __name__ == '__main__':
    main()
