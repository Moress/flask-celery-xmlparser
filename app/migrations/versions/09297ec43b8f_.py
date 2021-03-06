"""empty message

Revision ID: 09297ec43b8f
Revises: 
Create Date: 2017-05-01 14:53:35.961303

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '09297ec43b8f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('parse_task_info',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('task_id', sa.String(length=155), nullable=True),
    sa.Column('filename', sa.String(length=200), nullable=True),
    sa.Column('state', sa.String(length=30), nullable=True),
    sa.Column('weight', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('date_add', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('task_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('parse_task_info')
    # ### end Alembic commands ###
