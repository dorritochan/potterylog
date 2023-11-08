"""empty message

Revision ID: 54ee1d3369f6
Revises: 07c506a13ce1
Create Date: 2023-08-10 22:20:36.662964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '54ee1d3369f6'
down_revision = '07c506a13ce1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('image',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('filename', sa.String(length=255), nullable=False),
    sa.Column('pot_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['pot_id'], ['pot.id'], name=op.f('fk_image_pot_id_pot')),
    sa.PrimaryKeyConstraint('id', name=op.f('pk_image'))
    )
    with op.batch_alter_table('pot', schema=None) as batch_op:
        batch_op.drop_column('photo_filename')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pot', schema=None) as batch_op:
        batch_op.add_column(sa.Column('photo_filename', sa.VARCHAR(length=255), nullable=True))

    op.drop_table('image')
    # ### end Alembic commands ###
