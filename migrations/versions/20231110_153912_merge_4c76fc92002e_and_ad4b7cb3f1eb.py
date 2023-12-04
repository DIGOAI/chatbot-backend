"""Merge 4c76fc92002e and ad4b7cb3f1eb 

Revision ID: 974fb2ac8c97
Revises: 4c76fc92002e, ad4b7cb3f1eb
Create Date: 2023-11-10 15:39:12.093146

"""

from typing import Sequence

import sqlalchemy as sa  # type: ignore
from alembic import op  # type: ignore

# revision identifiers, used by Alembic.
revision: str = '974fb2ac8c97'
down_revision: str | Sequence[str] | None = ('4c76fc92002e', 'ad4b7cb3f1eb')
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
