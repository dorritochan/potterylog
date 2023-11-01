"""empty message

Revision ID: edba03505715
Revises: 8be71a866f8b
Create Date: 2023-10-23 14:43:14.182182

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'edba03505715'
down_revision = '8be71a866f8b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('commission',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('commissioner', sa.String(), nullable=True),
    sa.Column('object', sa.String(), nullable=True),
    sa.Column('amount', sa.Integer(), nullable=True),
    sa.Column('description', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_commission'))
    )
    with op.batch_alter_table('commission', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_commission_commissioner'), ['commissioner'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('commission', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_commission_commissioner'))

    op.drop_table('commission')
    # ### end Alembic commands ###
