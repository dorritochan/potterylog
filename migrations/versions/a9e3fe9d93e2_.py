"""empty message

Revision ID: a9e3fe9d93e2
Revises: a392249cc3e6
Create Date: 2023-07-22 13:43:13.066776

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9e3fe9d93e2'
down_revision = 'a392249cc3e6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('glaze', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', sa.String(length=50), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('glaze', schema=None) as batch_op:
        batch_op.drop_column('name')

    # ### end Alembic commands ###
