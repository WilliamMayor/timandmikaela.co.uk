"""empty message

Revision ID: 407033c7240e
Revises: 1850c8002412
Create Date: 2015-03-05 21:41:09.346238

"""

# revision identifiers, used by Alembic.
revision = '407033c7240e'
down_revision = '1850c8002412'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('access_token', sa.Text(), nullable=False),
    sa.Column('refresh_token', sa.Text(), nullable=False),
    sa.PrimaryKeyConstraint('uid')
    )
    op.drop_table('photo')
    op.drop_table('photo_album')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('photo',
    sa.Column('pid', sa.INTEGER(), nullable=False),
    sa.Column('url', sa.TEXT(), autoincrement=False, nullable=False),
    sa.Column('album_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['album_id'], [u'photo_album.aid'], name=u'photo_album_id_fkey'),
    sa.PrimaryKeyConstraint('pid', name=u'photo_pkey')
    )
    op.create_table('photo_album',
    sa.Column('aid', sa.INTEGER(), nullable=False),
    sa.Column('name', sa.TEXT(), autoincrement=False, nullable=False),
    sa.PrimaryKeyConstraint('aid', name=u'photo_album_pkey')
    )
    op.drop_table('user')
    ### end Alembic commands ###
