"""Module to handle ingestion process."""
import itertools
from datetime import UTC, datetime

import pandas as pd
import psycopg
from psycopg import sql


def get_table_names(cur: psycopg.Cursor, schema: str) -> list[str]:
    """Get a list of all existed table names on schema."""
    cur.execute(
        """
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = %s
        AND table_type = 'BASE TABLE'
    """,
        (schema,),
    )
    return [row[0] for row in cur.fetchall()]


def get_table_column_names(
    cur: psycopg.Cursor,
    schema: str,
    table: str,
) -> list[str]:
    """Get column names of table schema."""
    cur.execute(
        """
        SELECT column_name, data_type, is_nullable
        FROM information_schema.columns
        WHERE table_schema = %s
        AND table_name = %s
        ORDER BY ordinal_position
    """,
        (schema, table),
    )
    return [row[0] for row in cur.fetchall()]


def ingest_to_table(
    data_file: str,
    cur: psycopg.Cursor,
    schema: str,
    table_name: str,
    table_cols: list[str],
    hex_dig: str,
) -> None:
    """Ingest into table in chunks for stressing out memory."""
    chunk_iter = pd.read_csv(
        data_file,
        chunksize=10000,
        )

    first_chunk = next(chunk_iter)
    if first_chunk.empty:
        return

    query = sql.SQL(
        "INSERT INTO {} ({}) VALUES ({});").format(
            sql.Identifier(schema, table_name),
            sql.SQL(", ").join(sql.Identifier(col) for col in table_cols),
            sql.SQL(", ").join(sql.Placeholder() * len(table_cols)),
        )

    # Metadata
    ingested_at = datetime.now(tz=UTC).strftime("%Y-%m-%d")

    for chunk in itertools.chain([first_chunk], chunk_iter):
        data = [
            (
                hex_dig,
                ingested_at,
                *x,
                ) for x in chunk.to_numpy()
        ]
        cur.executemany(query, data)
