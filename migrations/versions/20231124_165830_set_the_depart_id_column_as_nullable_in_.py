"""Set the depart_id column as nullable in the tickets table.

Revision ID: 090fb4fb3b58
Revises: 6f65129fa76d
Create Date: 2023-11-24 16:58:30.579592

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '090fb4fb3b58'
down_revision: str | Sequence[str] | None = '6f65129fa76d'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.alter_column('tickets', 'department_id',  # type: ignore
                    existing_type=sa.VARCHAR(length=10),
                    nullable=True)


def downgrade() -> None:
    op.alter_column('tickets', 'department_id',  # type: ignore
                    existing_type=sa.VARCHAR(length=10),
                    nullable=False)
