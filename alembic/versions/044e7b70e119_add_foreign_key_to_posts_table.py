"""Add foreign key to posts table

Revision ID: 044e7b70e119
Revises: 418fc5a38280
Create Date: 2022-05-20 13:06:12.025429

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '044e7b70e119'
down_revision = '418fc5a38280'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False)
    )
    op.create_foreign_key(
        'posts_users_fkey', 
        source_table='posts', 
        referent_table='users',
        local_cols=['owner_id'], 
        remote_cols=['id'], 
        ondelete="CASCADE"
        )
    pass


def downgrade():
    op.drop_constraint('posts_users_fkey', table_name='posts')
    op.drop_column('posts', 'owner_id')
    pass
