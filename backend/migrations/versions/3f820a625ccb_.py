"""empty message

Revision ID: 3f820a625ccb
Revises: 96b79d4a4e20
Create Date: 2023-06-30 13:43:12.965274

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f820a625ccb'
down_revision = '96b79d4a4e20'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pot', schema=None) as batch_op:
        batch_op.drop_index('ix_pot_bisque_fire_kiln')
        batch_op.create_index(batch_op.f('ix_pot_bisque_fire_kiln'), ['bisque_fire_kiln'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pot', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_pot_bisque_fire_kiln'))
        batch_op.create_index('ix_pot_bisque_fire_kiln', ['bisque_fire_kiln'], unique=False)

    # ### end Alembic commands ###