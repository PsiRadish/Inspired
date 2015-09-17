"""empty message

Revision ID: 1bbd7594eeb
Revises: b1b555819e
Create Date: 2015-09-16 18:59:19.493513

"""

# revision identifiers, used by Alembic.
revision = '1bbd7594eeb'
down_revision = 'b1b555819e'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('roles_users')
    op.drop_table('role')
    op.drop_column('user', 'active')
    op.drop_column('user', 'password')
    op.add_column('user', sa.Column('password', sa.String(), nullable=False))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.BOOLEAN(), autoincrement=False, nullable=True))
    op.create_table('roles_users',
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.Column('role_id', sa.INTEGER(), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], name='roles_users_role_id_fkey'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], name='roles_users_user_id_fkey')
    )
    op.create_table('role',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.VARCHAR(length=80), autoincrement=False, nullable=True),
    sa.Column('description', sa.VARCHAR(length=255), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('id', name='role_pkey'),
    sa.UniqueConstraint('name', name='role_name_key')
    )
    ### end Alembic commands ###
