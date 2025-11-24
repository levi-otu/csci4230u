"""add_volume_fields_to_books

Revision ID: 6c8f534a6cef
Revises: d7b7820a4247
Create Date: 2025-11-24 10:58:03.981693

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6c8f534a6cef'
down_revision: Union[str, Sequence[str], None] = 'd7b7820a4247'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add volume/series fields to books table
    op.add_column('books', sa.Column('series_title', sa.String(500), nullable=True))
    op.add_column('books', sa.Column('volume_number', sa.Integer, nullable=True))
    op.add_column('books', sa.Column('volume_title', sa.String(500), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    # Remove volume/series fields from books table
    op.drop_column('books', 'volume_title')
    op.drop_column('books', 'volume_number')
    op.drop_column('books', 'series_title')
