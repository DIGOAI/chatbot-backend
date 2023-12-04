"""Seed departments

Revision ID: 6b6cbfb1af05
Revises: 0424e1a7b66b
Create Date: 2023-10-26 18:49:33.226713

"""

from typing import Sequence

import sqlalchemy.orm as saorm
from alembic import op

from src.db.models.department import Department

# revision identifiers, used by Alembic.
revision: str = '6b6cbfb1af05'
down_revision: str | None = '0424e1a7b66b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def get_session():
    # Create a session to use the ORM
    conn = op.get_bind()
    Session = saorm.sessionmaker()
    return Session(bind=conn)


def upgrade() -> None:
    # Get a session
    session = get_session()

    # Create default departments
    departments = [
        Department(id="SUPPORT", name="Soporte", external_id=1),
        Department(id="SALES", name="Ventas", external_id=2),
        Department(id="CLAIMS", name="Reclamos", external_id=3),
    ]

    # Insert data to the departments table
    session.add_all(departments)
    session.commit()


def downgrade() -> None:
    # Get a session
    session = get_session()

    # Delete default departments
    session.query(Department).delete()
    session.commit()
