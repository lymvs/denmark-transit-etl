"""ETL flow."""
import os
from sqlite3 import ProgrammingError

import psycopg
from dotenv import load_dotenv
from prefect import flow, task
from prefect.logging import get_run_logger

from infra.gtfs.rejseplannen import fetch_files
from pipelines.ingestion.ingest import (
    get_table_column_names,
    get_table_names,
    ingest_to_table,
)

load_dotenv()

URL = "https://www.rejseplannen.info/labs/GTFS.zip"
CONFIG = {
    "dbname": os.getenv("POSTGRES_DB"),
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "127.0.0.1",
    "port": "5432",
}
TEMP_PATH = "temp/"


@task(
    name="Extract GTFS files",
    retries=3,
    retry_delay_seconds=[2, 5, 15],
    log_prints=True,
    )
def download_files() -> str:
    """Download zipfile and extract files to directory."""
    logger = get_run_logger()
    return fetch_files(logger, TEMP_PATH)


@task(name="Bronze layer")
def ingest_data(hex_dig: str, schema: str = "bronze") -> None:
    """Append data into bronze layer with feed_version."""
    logger = get_run_logger()
    with psycopg.connect(**CONFIG) as conn, conn.cursor() as cur:
        tables = get_table_names(cur, schema)
        try:
            for table in tables:
                cur.execute(
                    psycopg.sql.SQL(
                        "SELECT feed_version FROM {} WHERE feed_version = %s LIMIT 1"
                        ).format(
                            psycopg.sql.Identifier(schema, table)
                            ),
                            (hex_dig,),
                            )

                if cur.fetchone():
                    logger.warning(
                        "WARNING Feed version %s already exists, skipping",
                        hex_dig,
                        )
                    continue

                logger.info("INFO Started to ingest data for table %s", table)
                cols = get_table_column_names(cur, schema, table)
                ingest_to_table(cur, schema, table, cols, hex_dig)
                conn.commit()
                logger.info("INFO %d records added into table %s", cur.rowcount, table)
        except ProgrammingError:
            conn.rollback()
            logger.exception("ERROR Ingestion failed, transaction rolled back")


@flow(name="gtfs_etl", log_prints=True)
def etl() -> None:
    """Run the end-to-end ETL for GTFS static data."""
    # Download and extract files from rejseplanen to temp folder
    hex_dig = download_files()
    # Trigger medallion architecture flow
    ingest_data(hex_dig)


if __name__ == "__main__":
    etl.serve(name="test-etl")
