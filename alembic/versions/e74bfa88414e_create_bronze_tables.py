"""Create bronze tables

Revision ID: e74bfa88414e
Revises: dd5844ea8aab
Create Date: 2026-04-12 20:41:46.840329

"""
from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "e74bfa88414e"
down_revision: str | Sequence[str] | None = 'dd5844ea8aab'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

BRONZE_SCHEMA: dict[str, list[str]] = {
    "agency": [
        "agency_id",
        "agency_name",
        "agency_url",
        "agency_timezone",
        "agency_lang",
        "agency_phone",
    ],
    "attributions": [
        "attribution_id",
        "is_producer",
        "organization_name",
        "attribution_url",
    ],
    "calendar_dates": [
        "service_id",
        "date",
        "exception_type",
    ],
    "calendar": [
        "service_id",
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
        "start_date",
        "end_date",
    ],
    "frequencies": [
        "trip_id",
        "start_time",
        "end_time",
        "headway_secs",
        "exact_times",
    ],
    "routes": [
        "route_id",
        "agency_id",
        "route_short_name",
        "route_long_name",
        "route_type",
        "route_color",
        "route_text_color",
        "route_desc",
    ],
    "shapes": [
        "shape_id",
        "shape_pt_lat",
        "shape_pt_lon",
        "shape_pt_sequence",
    ],
    "stop_times": [
        "trip_id",
        "arrival_time",
        "departure_time",
        "stop_id",
        "stop_sequence",
        "pickup_type",
        "drop_off_type",
        "stop_headsign",
    ],
    "stops": [
        "stop_id",
        "stop_code",
        "stop_name",
        "stop_desc",
        "stop_lat",
        "stop_lon",
        "location_type",
        "parent_station",
        "wheelchair_boarding",
        "platform_code",
        "stop_timezone",
    ],
    "transfers": [
        "from_stop_id",
        "to_stop_id",
        "transfer_type",
        "min_transfer_time",
        "from_route_id",
        "to_route_id",
        "from_trip_id",
        "to_trip_id",
    ],
    "trips": [
        "route_id",
        "service_id",
        "trip_id",
        "trip_headsign",
        "trip_short_name",
        "direction_id",
        "block_id",
        "shape_id",
        "wheelchair_accessible",
        "bikes_allowed",
    ],
}


def bronze_table(table_name: str, columns: str):
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
