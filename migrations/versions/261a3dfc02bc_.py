"""empty message

Revision ID: 261a3dfc02bc
Revises: 400d4b7e2e42
Create Date: 2015-03-01 22:57:30.302300

"""

# revision identifiers, used by Alembic.
revision = '261a3dfc02bc'
down_revision = '400d4b7e2e42'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('blog_post',
    sa.Column('bid', sa.Integer(), nullable=False),
    sa.Column('name', sa.Text(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('post', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('bid')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('blog_post')
    ### end Alembic commands ###
