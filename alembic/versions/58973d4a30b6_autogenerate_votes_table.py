"""autogenerate votes table

Revision ID: 58973d4a30b6
Revises: 34b6a7397567
Create Date: 2022-05-20 13:20:50.611531

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '58973d4a30b6'
down_revision = '34b6a7397567'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('post_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('user_id', 'post_id')
    )

def downgrade():
    op.drop_table('votes')