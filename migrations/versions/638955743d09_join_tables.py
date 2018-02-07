"""join tables

Revision ID: 638955743d09
Revises: aef37e019492
Create Date: 2018-01-31 21:20:31.471595

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '638955743d09'
down_revision = 'aef37e019492'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('category',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_up', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_category_name'), 'category', ['name'], unique=True)
    op.create_table('course',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_up', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_course_name'), 'course', ['name'], unique=True)
    op.create_table('institution',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_up', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_institution_name'), 'institution', ['name'], unique=True)
    op.create_table('module',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=64), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_up', sa.DateTime(), nullable=True),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_module_name'), 'module', ['name'], unique=True)
    op.create_table('course_institutions',
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('institution_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['institution_id'], ['institution.id'], )
    )
    op.create_table('course_modules',
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], )
    )
    op.create_table('institution_modules',
    sa.Column('institution_id', sa.Integer(), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['institution_id'], ['institution.id'], ),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], )
    )
    op.create_table('institution_users',
    sa.Column('institution_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['institution_id'], ['institution.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('module_categories',
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.Column('category_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['category_id'], ['category.id'], ),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], )
    )
    op.create_table('user_courses',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('course_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['course_id'], ['course.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.create_table('user_modules',
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('module_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['module_id'], ['module.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], )
    )
    op.drop_table('post')
    op.add_column('user', sa.Column('created_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('deleted_at', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('last_sign_in', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('updated_up', sa.DateTime(), nullable=True))
    op.add_column('user', sa.Column('user_type', sa.String(length=32), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'user_type')
    op.drop_column('user', 'updated_up')
    op.drop_column('user', 'last_sign_in')
    op.drop_column('user', 'deleted_at')
    op.drop_column('user', 'created_at')
    op.create_table('post',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('body', sa.VARCHAR(length=140), nullable=True),
    sa.Column('timestamp', sa.DATETIME(), nullable=True),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.drop_table('user_modules')
    op.drop_table('user_courses')
    op.drop_table('module_categories')
    op.drop_table('institution_users')
    op.drop_table('institution_modules')
    op.drop_table('course_modules')
    op.drop_table('course_institutions')
    op.drop_index(op.f('ix_module_name'), table_name='module')
    op.drop_table('module')
    op.drop_index(op.f('ix_institution_name'), table_name='institution')
    op.drop_table('institution')
    op.drop_index(op.f('ix_course_name'), table_name='course')
    op.drop_table('course')
    op.drop_index(op.f('ix_category_name'), table_name='category')
    op.drop_table('category')
    # ### end Alembic commands ###