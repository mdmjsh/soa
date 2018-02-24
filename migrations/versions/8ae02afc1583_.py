"""empty message

Revision ID: 8ae02afc1583
Revises: acbd3054d02d
Create Date: 2018-02-24 15:46:01.195160

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ae02afc1583'
down_revision = 'acbd3054d02d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('course', 'updated_up')
    op.add_column('institution', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.drop_column('institution', 'updated_up')
    op.add_column('module', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.drop_column('module', 'updated_up')
    op.add_column('tag', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.drop_column('tag', 'updated_up')
    op.add_column('user', sa.Column('updated_at', sa.DateTime(), nullable=True))
    op.drop_column('user', 'updated_up')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('updated_up', sa.DATETIME(), nullable=True))
    op.drop_column('user', 'updated_at')
    op.add_column('tag', sa.Column('updated_up', sa.DATETIME(), nullable=True))
    op.drop_column('tag', 'updated_at')
    op.add_column('module', sa.Column('updated_up', sa.DATETIME(), nullable=True))
    op.drop_column('module', 'updated_at')
    op.add_column('institution', sa.Column('updated_up', sa.DATETIME(), nullable=True))
    op.drop_column('institution', 'updated_at')
    op.add_column('course', sa.Column('updated_up', sa.DATETIME(), nullable=True))
    # ### end Alembic commands ###
