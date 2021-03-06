"""empty message

Revision ID: 89b80990b616
Revises: 
Create Date: 2021-11-21 18:02:30.364142

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '89b80990b616'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('project', 'description')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('project', sa.Column('description', mysql.VARCHAR(length=30), nullable=True))
    # ### end Alembic commands ###
