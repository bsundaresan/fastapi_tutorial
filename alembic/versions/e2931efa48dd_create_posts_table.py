"""Create Posts Table

Revision ID: e2931efa48dd
Revises: 
Create Date: 2022-05-20 12:23:47.640766

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e2931efa48dd'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'posts', 
        sa.Column('id', sa.INTEGER(), nullable=False, primary_key=True),
        sa.Column('title', sa.String(), nullable=False)
    )

    pass

def downgrade():
    op.drop_table('posts')
    pass
