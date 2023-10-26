"""Add email column to client table

Revision ID: 8ddf12cf14b8
Revises: 0424e1a7b66b
Create Date: 2023-10-26 13:25:53.035971

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '8ddf12cf14b8'
down_revision: str | None = '0424e1a7b66b'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('clients', sa.Column('email', sa.String(length=255), nullable=True))


def downgrade() -> None:
    op.drop_column('clients', 'email')
