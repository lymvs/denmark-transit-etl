"""Create database schemas

Revision ID: dd5844ea8aab
Revises:
Create Date: 2026-04-12 20:14:30.598638

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'dd5844ea8aab'
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.execute("""
        CREATE SCHEMA IF NOT EXISTS bronze;
        CREATE SCHEMA IF NOT EXISTS silver;
        CREATE SCHEMA IF NOT EXISTS gold;
    """)


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("""
        DROP SCHEMA IF EXISTS bronze CASCADE;
        DROP SCHEMA IF EXISTS silver CASCADE;
        DROP SCHEMA IF EXISTS gold CASCADE;
    """)
