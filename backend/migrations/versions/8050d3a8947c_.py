"""empty message

Revision ID: 8050d3a8947c
Revises: a0e71a13e17f
Create Date: 2023-06-30 11:12:21.801693

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8050d3a8947c'
down_revision = 'a0e71a13e17f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clay', schema=None) as batch_op:
        batch_op.add_column(sa.Column('grog_size_max', sa.Float(), nullable=True))
        batch_op.add_column(sa.Column('grog_size_unit', sa.String(length=10), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clay', schema=None) as batch_op:
        batch_op.drop_column('grog_size_unit')
        batch_op.drop_column('grog_size_max')

    # ### end Alembic commands ###