"""merge de heads das migracoes

Revision ID: cfffa7b5315f
Revises: 19c3a6ef87b2, 7f42616a6661
Create Date: 2026-10-14 01:09:02.003773

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cfffa7b5315f'
down_revision: Union[str, Sequence[str], None] = ('19c3a6ef87b2', '7f42616a6661')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
