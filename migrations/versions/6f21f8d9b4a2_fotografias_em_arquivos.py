"""fotografias em arquivos

Revision ID: 6f21f8d9b4a2
Revises: 0bc908e76bef
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '6f21f8d9b4a2'
down_revision: Union[str, Sequence[str], None] = '0bc908e76bef'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('fotografias') as batch_op:
        batch_op.add_column(sa.Column('caminho', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('tipo', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('tamanho', sa.Integer(), nullable=True))
        batch_op.create_unique_constraint(
            'uq_fotografias_caminho', ['caminho']
        )
        batch_op.drop_column('arquivo')


def downgrade() -> None:
    with op.batch_alter_table('fotografias') as batch_op:
        batch_op.add_column(
            sa.Column('arquivo', sa.LargeBinary(), nullable=True)
        )
        batch_op.drop_constraint('uq_fotografias_caminho', type_='unique')
        batch_op.drop_column('tamanho')
        batch_op.drop_column('tipo')
        batch_op.drop_column('caminho')
