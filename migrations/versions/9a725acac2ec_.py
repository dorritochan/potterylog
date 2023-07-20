"""empty message

Revision ID: 9a725acac2ec
Revises: b0ae5dd569a4
Create Date: 2023-06-30 14:21:49.375017

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9a725acac2ec'
down_revision = 'b0ae5dd569a4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pot', schema=None) as batch_op:
        batch_op.add_column(sa.Column('bisque_fire_program_id', sa.Integer(), nullable=True))
        batch_op.add_column(sa.Column('glaze_fire_program_id', sa.Integer(), nullable=True))
        batch_op.create_index(batch_op.f('ix_pot_bisque_fire_program_id'), ['bisque_fire_program_id'], unique=False)
        batch_op.create_index(batch_op.f('ix_pot_glaze_fire_program_id'), ['glaze_fire_program_id'], unique=False)
        batch_op.create_foreign_key(batch_op.f('fk_pot_bisque_fire_program_id_firing_program'), 'firing_program', ['bisque_fire_program_id'], ['id'])
        batch_op.create_foreign_key(batch_op.f('fk_pot_glaze_fire_program_id_firing_program'), 'firing_program', ['glaze_fire_program_id'], ['id'])

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('pot', schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f('fk_pot_glaze_fire_program_id_firing_program'), type_='foreignkey')
        batch_op.drop_constraint(batch_op.f('fk_pot_bisque_fire_program_id_firing_program'), type_='foreignkey')
        batch_op.drop_index(batch_op.f('ix_pot_glaze_fire_program_id'))
        batch_op.drop_index(batch_op.f('ix_pot_bisque_fire_program_id'))
        batch_op.drop_column('glaze_fire_program_id')
        batch_op.drop_column('bisque_fire_program_id')

    # ### end Alembic commands ###
