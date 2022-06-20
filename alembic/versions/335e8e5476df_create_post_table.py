"""create post table

Revision ID: 335e8e5476df
Revises: 
Create Date: 2022-06-19 15:54:09.650108

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '335e8e5476df'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'posts',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('content', sa.String(length=255), nullable=False),
        sa.Column('published', sa.Boolean(), nullable=False, server_default=sa.text('TRUE')),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')),
        sa.Column('owner_id', sa.Integer(), nullable=False), sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    op.drop_table('posts')
