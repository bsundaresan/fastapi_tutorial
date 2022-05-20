"""Add remaining columns to post table

Revision ID: 34b6a7397567
Revises: 044e7b70e119
Create Date: 2022-05-20 13:11:07.262611

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '34b6a7397567'
down_revision = '044e7b70e119'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE')
    )
    op.add_column(
        'posts',
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, 
        server_default=sa.text('now()'))
    )
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
