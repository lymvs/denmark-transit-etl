"""Create bronze tables

Revision ID: e74bfa88414e
Revises: dd5844ea8aab
Create Date: 2026-04-12 20:41:46.840329

"""
from collections.abc import Sequence

import sqlalchemy as sa
import yaml

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e74bfa88414e"
down_revision: str | Sequence[str] | None = 'dd5844ea8aab'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

YAML_PATH = "config/bronze_schema.yaml"

with open(YAML_PATH) as f:
    BRONZE_SCHEMA = yaml.safe_load(f)


def bronze_table(table_name: str, columns: str) -> None:
    """Helper function to avoid repetition."""
    op.create_table(
        table_name,
        sa.Column("feed_version", sa.Text(), nullable=False),
        sa.Column("ingested_at", sa.Date(), nullable=False),
        *[sa.Column(col, sa.Text()) for col in columns],
        if_not_exists=True,
        schema="bronze",
    )


def upgrade() -> None:
    """Upgrade schema."""
    for table_name, columns in BRONZE_SCHEMA.items():
        bronze_table(table_name, columns)


def downgrade() -> None:
    """Downgrade schema."""
    for table_name in BRONZE_SCHEMA:
        op.drop_table(table_name, if_exists=True, schema="bronze")
