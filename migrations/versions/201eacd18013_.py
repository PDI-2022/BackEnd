"""empty message

Revision ID: 201eacd18013
Revises: 
Create Date: 2022-11-15 23:28:15.479016

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '201eacd18013'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('models',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=True),
    sa.Column('path', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('models')
    # ### end Alembic commands ###
