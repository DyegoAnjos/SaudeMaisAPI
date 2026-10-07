"""campos do usuario institucional

Revision ID: a472ecb1d930
Revises: 6f21f8d9b4a2
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = 'a472ecb1d930'
down_revision: Union[str, Sequence[str], None] = '6f21f8d9b4a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('usuario_institucional') as batch_op:
        batch_op.add_column(
            sa.Column('razao_social', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('nome_responsavel', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('cargo_responsavel', sa.String(), nullable=True)
        )
        batch_op.add_column(sa.Column('site', sa.String(), nullable=True))
        batch_op.add_column(
            sa.Column('documento_cnpj', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('documento_responsavel', sa.String(), nullable=True)
        )
        batch_op.add_column(
            sa.Column('documento_vinculo', sa.String(), nullable=True)
        )


def downgrade() -> None:
    with op.batch_alter_table('usuario_institucional') as batch_op:
        batch_op.drop_column('documento_vinculo')
        batch_op.drop_column('documento_responsavel')
        batch_op.drop_column('documento_cnpj')
        batch_op.drop_column('site')
        batch_op.drop_column('cargo_responsavel')
        batch_op.drop_column('nome_responsavel')
        batch_op.drop_column('razao_social')
