"""Create silver tables

Revision ID: 80a4e84fc686
Revises: e74bfa88414e
Create Date: 2026-06-05 20:55:52.895662

"""
from collections.abc import Sequence

import yaml

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '80a4e84fc686'
down_revision: str | Sequence[str] | None = 'e74bfa88414e'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

YAML_PATH = "config/silver_schema.yaml"

with open(YAML_PATH) as f:
    SILVER_SCHEMA = yaml.safe_load(f)


def silver_table(table_name: str, columns: list) -> None:
    col_definitions = ", ".join(
        f"{column_name} {dtype.upper()}"
        for col in columns
        for column_name, dtype in col.items()
    )
    op.execute(f"""
    CREATE TABLE IF NOT EXISTS silver.{table_name} (
        feed_version TEXT NOT NULL,
        ingested_at DATE NOT NULL,
        {col_definitions}
        )
    """
    )


def upgrade() -> None:
    """Upgrade schema."""
    for table_name, columns in SILVER_SCHEMA.items():
        silver_table(table_name, columns)


def downgrade() -> None:
    """Downgrade schema."""
    for table_name in SILVER_SCHEMA:
        op.drop_column(table_name, if_exists=True, schema="silver")
