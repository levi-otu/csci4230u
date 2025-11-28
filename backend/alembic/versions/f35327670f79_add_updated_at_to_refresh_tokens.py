"""add_updated_at_to_refresh_tokens

Revision ID: f35327670f79
Revises: eee11d2ac369
Create Date: 2025-11-24 23:01:33.119232

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f35327670f79'
down_revision: Union[str, Sequence[str], None] = 'eee11d2ac369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add updated_at column to refresh_tokens table
    op.add_column(
        'refresh_tokens',
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False)
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Remove updated_at column from refresh_tokens table
    op.drop_column('refresh_tokens', 'updated_at')
