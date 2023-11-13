"""Add template column to massive_templates table.

Revision ID: a84dc5b80248
Revises: 974fb2ac8c97
Create Date: 2023-11-13 14:12:08.126578

"""

from typing import Sequence

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'a84dc5b80248'
down_revision: str | Sequence[str] | None = '974fb2ac8c97'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    # === Create ticketshift enum type ===
    sa.Enum('MORNING', 'AFTERNOON', name='ticketshift').create(op.get_bind())  # type: ignore

    # === Add template column to massive_templates table ===
    op.add_column('massive_templates', sa.Column('template', sa.Text(), nullable=False))

    # === Alter shift column on tickets table ===
    op.alter_column('tickets', 'shift',  # type: ignore
                    existing_type=sa.VARCHAR(length=13),
                    type_=sa.Enum('MORNING', 'AFTERNOON', name='ticketshift'),
                    existing_nullable=True, postgresql_using='shift::ticketshift')


def downgrade() -> None:
    op.alter_column('tickets', 'shift',  # type: ignore
                    existing_type=sa.Enum('MORNING', 'AFTERNOON', name='ticketshift'),
                    type_=sa.VARCHAR(length=13),
                    existing_nullable=True)
    op.drop_column('massive_templates', 'template')
    sa.Enum('MORNING', 'AFTERNOON', name='ticketshift').drop(op.get_bind())  # type: ignore
