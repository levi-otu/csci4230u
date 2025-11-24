"""add_reading_status_to_user_books

Revision ID: d7b7820a4247
Revises: a72582e4c369
Create Date: 2025-11-24 10:27:45.092407

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd7b7820a4247'
down_revision: Union[str, Sequence[str], None] = 'a72582e4c369'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add reading_status column with default 'unread'
    # Options: 'unread', 'reading', 'finished'
    op.add_column(
        'user_books',
        sa.Column('reading_status', sa.String(20), nullable=False, server_default='unread')
    )

    # Migrate existing data: if is_read is True, set status to 'finished', else 'reading'
    op.execute("""
        UPDATE user_books
        SET reading_status = CASE
            WHEN is_read = true THEN 'finished'
            ELSE 'reading'
        END
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('user_books', 'reading_status')
