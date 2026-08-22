import os

import pandas as pd
import streamlit as st
from sqlalchemy import Engine, create_engine
from sqlalchemy.exc import SQLAlchemyError


def _db_engine() -> Engine:
    db_url = (
        f"postgresql+psycopg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}"
        f"@{os.getenv('POSTGRES_HOST')}:{os.getenv('POSTGRES_PORT')}/{os.getenv('POSTGRES_DB')}"
    )

    return create_engine(db_url)


def _query_top_10_stations(engine: Engine) -> pd.DataFrame:
    try:
        return pd.read_sql(
            """
            SELECT stop_name, departures
            FROM public_gold.gold_top_stops_by_departures
            LIMIT 10;
            """,
            engine,
        )
    except SQLAlchemyError:
        return pd.DataFrame(columns=["stop_name", "departures"])


def _query_top_10_routes(engine: Engine) -> pd.DataFrame:
    try:
        return pd.read_sql(
            """
            SELECT route_name, trips, agency_name
            FROM public_gold.gold_trip_counts_by_route
            LIMIT 10;
            """,
            engine,
        )
    except SQLAlchemyError:
        return pd.DataFrame(columns=["route_name", "trips", "agency_name"])


def _query_routes_per_route_type(engine: Engine) -> pd.DataFrame:
    try:
        return pd.read_sql(
            """
            SELECT description, routes
            FROM public_gold.gold_routes_per_route_type;
            """,
            engine,
        )
    except SQLAlchemyError:
        return pd.DataFrame(columns=["description", "routes"])


def render_top_10_stations(engine: Engine) -> None:
    st.header(
        "Top 10 Stations",
        anchor="top_10_stations",
        divider=True,
    )
    st.dataframe(
        _query_top_10_stations(engine),
        hide_index=True,
        column_config={
            "departures": st.column_config.NumberColumn(
                "Count of Departures",
                format="localized",
            ),
            "stop_name": st.column_config.TextColumn(
                "Station",
            ),
        },
        width="content",
    )


def render_top_10_routes(engine: Engine) -> None:
    st.header(
        "Top 10 Routes",
        anchor="top_10_routes",
        divider=True,
    )
    st.dataframe(
        _query_top_10_routes(engine),
        hide_index=True,
        column_config={
            "route_name": st.column_config.TextColumn(
                "Route",
            ),
            "trips": st.column_config.NumberColumn(
                "Count of Trips",
                format="localized",
            ),
        },
        width="content",
    )


def render_routes_per_route_type(engine: Engine) -> None:
    st.header(
        "Routes per Route Type",
        anchor="routes_per_route_type",
        divider=True,
    )
    st.dataframe(
        _query_routes_per_route_type(engine),
        hide_index=True,
        column_config={
            "description": st.column_config.TextColumn(
                "Route Type",
            ),
            "routes": st.column_config.NumberColumn(
                "Count of Routes",
                format="localized",
            ),
        },
        width="content",
    )


def main():
    st.title("Denmark Transit Dashboard")
    engine = _db_engine()

    render_top_10_stations(engine)
    render_top_10_routes(engine)
    render_routes_per_route_type(engine)

if __name__ == "__main__":
    main()
