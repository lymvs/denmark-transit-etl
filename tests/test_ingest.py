import os

import pandas as pd
import psycopg
import pytest
from dotenv import load_dotenv
from psycopg import sql

from pipelines.ingestion.ingest import (
    get_table_column_names,
    get_table_names,
    ingest_to_table,
)

load_dotenv()

TEST_CONFIG = {
    "dbname": "test_db",
    "user": os.getenv("POSTGRES_USER"),
    "password": os.getenv("POSTGRES_PASSWORD"),
    "host": "127.0.0.1",
    "port": "5432",
}


@pytest.fixture(scope="session")
def conn():
    with psycopg.connect(**TEST_CONFIG) as conn:
        yield conn


@pytest.fixture(autouse=True)
def rollback(conn):
    yield
    conn.rollback()


@pytest.fixture
def cur(conn):
    with conn.cursor() as cur:
        yield cur


@pytest.fixture
def dummy_tables(cur):
    tables = ["table1", "table2", "table3"]

    for table in tables:
        cur.execute(
            sql.SQL(
                """
                CREATE TABLE IF NOT EXISTS bronze.{} (
                    feed_version TEXT,
                    ingested_at DATE,
                    col1 TEXT,
                    col2 TEXT,
                    col3 TEXT
                );
                """).format(sql.Identifier(table))
        )
    yield


@pytest.fixture
def dummy_data_file(tmp_path):
    data = {
        "col1": ["1", "2", "3"],
        "col2": ["4", "5", "6"],
        "col3": ["7", "8", "9"],
    }
    file_path = tmp_path / "dummy_data.csv"
    pd.DataFrame(data).to_csv(file_path, index=False)
    return file_path


class TestTableNames:
    def test_get_table_names(self, cur, dummy_tables):
        result = get_table_names(cur, "bronze")
        assert {"table1", "table2", "table3"}.issubset(result)
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)


class TestTableColumnNames:
    def test_get_table_column_names(self, cur, dummy_tables):
        result = get_table_column_names(cur, "bronze", "table1")
        assert result == ["feed_version", "ingested_at", "col1", "col2", "col3"]
        assert isinstance(result, list)
        assert all(isinstance(item, str) for item in result)


class TestIngestToTable:
    def test_ingest_to_table(self, dummy_data_file, cur, dummy_tables):
        ingest_to_table(
            dummy_data_file,
            cur,
            "bronze",
            "table1",
            ["feed_version", "ingested_at", "col1", "col2", "col3"],
            "test_hex",
            )
        cur.execute("SELECT COUNT(*) FROM bronze.table1")
        assert cur.fetchone()[0] == 3
