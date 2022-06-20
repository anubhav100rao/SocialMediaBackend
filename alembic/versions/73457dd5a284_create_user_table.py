"""create user table

Revision ID: 73457dd5a284
Revises: 335e8e5476df
Create Date: 2022-06-20 12:50:53.508575

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73457dd5a284'
down_revision = '335e8e5476df'
branch_labels = None
depends_on = None


def upgrade() -> None:
    
    op.create_table(
        'users', 
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False, unique=True),
        sa.Column('password', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()'))
    )


def downgrade() -> None:
    op.drop_table('users')
