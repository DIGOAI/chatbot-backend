"""Add last_message_id column to conversations table

Revision ID: 17b4741be087
Revises: 6b6cbfb1af05
Create Date: 2023-10-27 09:37:20.470221

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = '17b4741be087'
down_revision: str | None = '6b6cbfb1af05'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column('conversations', sa.Column('last_message_id', sa.String(length=34), nullable=True))
    op.create_foreign_key(None, 'conversations', 'messages', ['last_message_id'], ['id'], ondelete='SET NULL')
    op.drop_index('ix_departments_id', table_name='departments')


def downgrade() -> None:
    op.create_index('ix_departments_id', 'departments', ['id'], unique=False)
    op.drop_constraint(None, 'conversations', type_='foreignkey')  # type: ignore
    op.drop_column('conversations', 'last_message_id')
