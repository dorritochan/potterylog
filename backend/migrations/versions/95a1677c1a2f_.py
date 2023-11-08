"""empty message

Revision ID: 95a1677c1a2f
Revises: 2d9280c6ab46
Create Date: 2023-09-26 12:57:19.678335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '95a1677c1a2f'
down_revision = '2d9280c6ab46'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clay', schema=None) as batch_op:
        batch_op.add_column(sa.Column('url', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('clay', schema=None) as batch_op:
        batch_op.drop_column('url')

    # ### end Alembic commands ###
