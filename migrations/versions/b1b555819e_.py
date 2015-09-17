"""empty message

Revision ID: b1b555819e
Revises: 7e1b645f53
Create Date: 2015-09-15 19:54:47.893952

"""

# revision identifiers, used by Alembic.
revision = 'b1b555819e'
down_revision = '7e1b645f53'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('active', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'active')
    ### end Alembic commands ###