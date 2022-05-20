"""Add users table

Revision ID: 418fc5a38280
Revises: 0181b80521c7
Create Date: 2022-05-20 12:57:58.078345

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '418fc5a38280'
down_revision = '0181b80521c7'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('password', sa.String(), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )
    
    pass


def downgrade():
    op.drop_table('users')
    pass
