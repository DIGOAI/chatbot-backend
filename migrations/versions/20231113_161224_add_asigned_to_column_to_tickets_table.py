"""Add asigned_to column to tickets table.

Revision ID: 6f65129fa76d
Revises: a84dc5b80248
Create Date: 2023-11-13 16:12:24.333776

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '6f65129fa76d'
down_revision: str | Sequence[str] | None = 'a84dc5b80248'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # === Add asigned_to column to tickets table ===
    op.add_column('tickets', sa.Column('asigned_to', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'tickets', 'users', ['asigned_to'], ['id'], ondelete='CASCADE')


def downgrade() -> None:
    op.drop_constraint(None, 'tickets', type_='foreignkey')  # type: ignore
    op.drop_column('tickets', 'asigned_to')
