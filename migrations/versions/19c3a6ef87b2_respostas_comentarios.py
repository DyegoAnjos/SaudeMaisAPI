from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = '19c3a6ef87b2'
down_revision: Union[str, Sequence[str], None] = '6cd9d8beeb3a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table('comentario') as batch_op:
        batch_op.add_column(
            sa.Column('comentario_pai', sa.Integer(), nullable=True)
        )
        batch_op.create_foreign_key(
            'fk_comentario_comentario_pai',
            'comentario',
            ['comentario_pai'],
            ['id'],
        )


def downgrade() -> None:
    with op.batch_alter_table('comentario') as batch_op:
        batch_op.drop_constraint(
            'fk_comentario_comentario_pai', type_='foreignkey'
        )
        batch_op.drop_column('comentario_pai')
