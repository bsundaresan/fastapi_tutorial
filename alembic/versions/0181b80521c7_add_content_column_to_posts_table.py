"""add content column to posts table

Revision ID: 0181b80521c7
Revises: e2931efa48dd
Create Date: 2022-05-20 12:50:19.800153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0181b80521c7'
down_revision = 'e2931efa48dd'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass

def downgrade():

    op.drop_column(
        'posts', 
        'content'
    )
    pass
