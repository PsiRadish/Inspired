"""empty message

Revision ID: 1e325fc9b3f
Revises: 59295bf3464
Create Date: 2015-09-17 01:02:28.238882

"""

# revision identifiers, used by Alembic.
revision = '1e325fc9b3f'
down_revision = '59295bf3464'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('chapter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('modified_at', sa.DateTime(), nullable=True),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('order', sa.Integer(), nullable=False),
    sa.Column('numeral', sa.String(), nullable=False),
    sa.Column('body', sa.Text(), nullable=False),
    sa.Column('work_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['work_id'], ['work.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('work', sa.Column('author_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'work', 'user', ['author_id'], ['id'])
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'work', type_='foreignkey')
    op.drop_column('work', 'author_id')
    op.drop_table('chapter')
    ### end Alembic commands ###
