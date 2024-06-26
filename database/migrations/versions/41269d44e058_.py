"""empty message

Revision ID: 41269d44e058
Revises: 
Create Date: 2024-04-21 20:28:22.957990

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '41269d44e058'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('names_man',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_names_man_name'), 'names_man', ['name'], unique=True)
    op.create_table('names_woman',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_names_woman_name'), 'names_woman', ['name'], unique=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_names_woman_name'), table_name='names_woman')
    op.drop_table('names_woman')
    op.drop_index(op.f('ix_names_man_name'), table_name='names_man')
    op.drop_table('names_man')
    # ### end Alembic commands ###
