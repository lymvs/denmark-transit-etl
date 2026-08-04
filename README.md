# denmark-transit-etl

![ruff](https://github.com/lymvs/denmark-transit-etl/actions/workflows/ruff.yml/badge.svg)
![tests](https://github.com/lymvs/denmark-transit-etl/actions/workflows/run_tests.yml/badge.svg)

An ETL pipeline for fetching and analyzing public transit data for Denmark from GTFS feeds.

## Architecture

```mermaid
flowchart LR
    prefect[Prefect Orchestrator]

    subgraph fetch[HTTP request]
        subgraph sources[Files]
            src_a@{ shape: doc, label: [Agency] }
            src_b@{ shape: doc, label: [Routes] }
            src_c@{ shape: doc, label: [Trips] }
        end
    end

    subgraph postgres[Postgres]
        subgraph bronze[Bronze Layer]
            bronze_a@{ shape: cyl, label: [bronze_agency] }
            bronze_b@{ shape: cyl, label: [bronze_routes] }
            bronze_c@{ shape: cyl, label: [bronze_trips] }
        end

        subgraph dbt[Dbt]
            subgraph silver[Silver Layer]
                silver_a@{ shape: cyl, label: [silver_agency] }
                silver_b@{ shape: cyl, label: [silver_routes] }
                silver_c@{ shape: cyl, label: [silver_trips] }
            end

            subgraph gold[Gold Layer]
                gold_a@{ shape: cyl, label: [gold_trip_counts_by_route] }
            end
        end
    end

    subgraph streamlit[Streamlit]
        app_a[Visualization]
    end

    prefect -->|orchestrates| sources

    src_a --> bronze_a
    src_b --> bronze_b
    src_c --> bronze_c

    bronze_a --> silver_a
    bronze_b --> silver_b
    bronze_c --> silver_c

    silver_a --> gold_a
    silver_b --> gold_a
    silver_c --> gold_a

    gold_a --> app_a

```

The project is following the [Medallion architecture](https://www.databricks.com/blog/what-is-medallion-architecture) with bronze-silver-gold layers.

- Fetches GTFS data as a zip file from [Rejseplannen](https://labs.rejseplanen.dk/hc/da/articles/21639730766877-Om-GTFS-Schedule-Static) site via HTTP request
- Hashes the feed and checks version before re-ingesting the same feed
- Extracts and stores the zip file temporarily in a landing zone (/temp)
- Stores raw tables as bronze layer in [PostgreSQL](https://www.postgresql.org/) database - uses Alembic for schema migrations
- Seeds a csv file with the [full list](https://developers.google.com/transit/gtfs/reference/extended-route-types) of route types for reference
- [Dbt](https://www.getdbt.com/) handles the transformations and tests for silver layer storing the tables on PostgreSQL database
- Dbt also handles queries and aggregations for gold layer tables
- Hosts a simple UI locally by a [Streamlit](https://streamlit.io/) server
- Orchestrates the whole pipeline with [Prefect](https://www.prefect.io/)

## Design Decisions

### Why dbt

The primary motivation for using dbt was to gain hands-on experience with a modern transformation framework that is widely adopted in data engineering.

Beyond the learning aspect, dbt naturally fits the architecture of this project:

- It provides a clean separation between the Bronze, Silver, and Gold layers.
- Built-in testing (not_null, unique, relationships, custom tests) makes data quality validation straightforward.
- SQL transformations are version-controlled alongside the application code.
- Incremental models and modular SQL improve maintainability as the project grows.
- The generated documentation and lineage graph make it easier to understand dependencies between models.

### Why Prefect over Airflow

Although I have professional experience building production pipelines with Apache Airflow, I chose Prefect for this project because it better matches its current scale.

The project consists of a relatively small number of tasks with simple dependencies, where introducing Airflow would have added unnecessary infrastructure and operational complexity.

Prefect offers several advantages for this use case:

- Lightweight setup with minimal configuration.
- Pipelines can be written as standard Python code.
- Built-in retries, logging, scheduling and monitoring.
- Easy migration to a more robust orchestration platform if the project grows in complexity.

If this project were expanded into a larger production system with multiple teams, hundreds of workflows, or more complex scheduling requirements, Apache Airflow would likely become the more appropriate choice.

### Why Postgres over Databricks or Snowflake

PostgreSQL was chosen because it is lightweight, open-source, and easy to run locally, making it well suited for developing and testing the pipeline without requiring cloud infrastructure.

The project separates data ingestion, transformation, orchestration, and presentation into independent components. This modular architecture allows the storage layer to be replaced by cloud-native platforms such as Snowflake or Databricks with limited changes to the overall pipeline design.

One of the planned future improvements is to migrate the storage and transformation layers to either Snowflake or Databricks.

## Screenshots

![Dashboard](screenshots/screenshot_1.png)
![Dashboard](screenshots/screenshot_2.png)
![Dashboard](screenshots/screenshot_3.png)

## Prerequisites

[Docker](https://www.docker.com/get-started/) must be installed to build and run the container.

## Usage

Copy .env example and update Postgres credentials

```bash
cp .env.example .env
```

Build and run docker container

```bash
docker compose build
docker compose up
```

> **_NOTE:_** app will be served on <http://localhost:8501/>

## Project structure

| Path | Description |
| --- | --- |
| `orchestration/etl.py` | Prefect flow — orchestrates the end-to-end pipeline (migrations → fetch → bronze → seed → silver → gold) |
| `infra/gtfs/` | Fetches and extracts the GTFS feed from Rejseplannen |
| `pipelines/ingestion/` | Loads extracted GTFS files into the bronze layer in PostgreSQL |
| `alembic/` | Database schema migrations (bronze table definitions) |
| `models/` | Dbt models for the silver and gold layers, plus schema/source tests |
| `macros/` | Dbt macros shared across models |
| `seeds/` | Dbt seed data (GTFS route type reference list) |
| `config/` | YAML schema definitions for bronze/silver tables |
| `dashboard/` | Streamlit app serving the gold-layer dashboard |
| `tests/` | Pytest tests for the ingestion pipeline |
| `compose.yaml` | Docker Compose services: Postgres, ETL, and the dashboard app |
| `Dockerfile.etl` / `Dockerfile.app` | Container images for the ETL pipeline and the dashboard |

## Roadmap

- [ ] Add more visualizations on the UI (e.g. map)
- [ ] Add a cli for manual on demand triggering of the ETL pipeline
- [ ] Dbt docs
- [ ] Test silver_routes.route_type
- [ ] Mocked HTTP test for fetching data step
- [ ] FastAPI for communication between Streamlit UI and Postgres db
- [ ] Use live transit data using [Rejseplannen API](https://labs.rejseplanen.dk/hc/da/articles/21554723926557-Om-API-2-0)
- [ ] Migrate fetching and ingestion steps from Python to Golang
- [ ] Host the pipeline on [Prefect Cloud](https://www.prefect.io/prefect/cloud) for scheduled runs
- [ ] Database migration to [Snowflake](https://www.snowflake.com/en/) or [Databricks](https://www.databricks.com/)

## License

[MIT](https://chooselicense.com/licenses/mit/)
