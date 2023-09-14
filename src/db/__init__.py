from src.db.database import Base, Session
from src.db.database import engine as _engine
from src.db.db_connnection import DbConnection
from src.db.postgres import PostgreSQLConnection

__all__ = [
    'Base',
    'Session',
    'DbConnection',
    'PostgreSQLConnection'
]


def setup_db():
    Base.metadata.create_all(bind=_engine)
