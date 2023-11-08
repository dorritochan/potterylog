"""empty message

Revision ID: 2fc9c2c63ade
Revises: edba03505715
Create Date: 2023-10-23 14:57:52.061688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2fc9c2c63ade'
down_revision = 'edba03505715'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commission', schema=None) as batch_op:
        batch_op.add_column(sa.Column('deadline', sa.Date(), nullable=True))
        batch_op.create_index(batch_op.f('ix_commission_deadline'), ['deadline'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commission', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_commission_deadline'))
        batch_op.drop_column('deadline')

    # ### end Alembic commands ###
