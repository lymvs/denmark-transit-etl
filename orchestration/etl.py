"""ETL flow."""
import os
from pathlib import Path

import psycopg
from dotenv import load_dotenv
from prefect import flow, task
from prefect.logging import get_run_logger
from prefect_dbt import DbtCoreOperation
from psycopg import ProgrammingError

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
    "host": os.getenv("POSTGRES_HOST"),
    "port": os.getenv("POSTGRES_PORT"),
}
TEMP_PATH = "temp/"


def run_dbt(command: str) -> None:
    dbt_op = DbtCoreOperation(
        commands=[command],
        )
    dbt_op.run()


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


@task(
    name="Bronze layer",
    retries=3,
    retry_delay_seconds=[2, 5, 15],
    log_prints=True,
    )
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
                        "Feed version for table %s already exists, skipping",
                        table,
                        )
                    continue

                logger.info("Started to ingest data for table %s", table)
                cols = get_table_column_names(cur, schema, table)
                total_records = ingest_to_table(
                    "temp/" + table + ".txt",
                    cur,
                    schema,
                    table,
                    cols,
                    hex_dig,
                    )
                conn.commit()
                logger.info("%d records added into table %s", total_records, table)
        except ProgrammingError:
            conn.rollback()
            logger.exception("Ingestion failed, transaction rolled back")
            raise


@task(
    name="Seed Route Types",
    retries=3,
    retry_delay_seconds=[2, 5, 15],
    log_prints=True,
    )
def seed_route_types() -> None:
    run_dbt("dbt seed")


@task(
    name="Silver Layer",
    retries=3,
    retry_delay_seconds=[2, 5, 15],
    log_prints=True,
    )
def silver_layer() -> None:
    run_dbt("dbt build --select silver")


@task(
    name="Gold Layer",
    retries=3,
    retry_delay_seconds=[2, 5, 15],
    log_prints=True,
    )
def gold_layer() -> None:
    run_dbt("dbt build --select gold")


@flow(name="gtfs_etl", log_prints=True)
def etl() -> None:
    """Run the end-to-end ETL for GTFS static data."""
    # Download and extract files from rejseplanen to temp folder
    hex_dig = download_files()
    # Trigger medallion architecture flow
    # bronze layer
    ingest_data(hex_dig)

    seed_route_types()

    silver_layer()

    gold_layer()


if __name__ == "__main__":
    etl()
