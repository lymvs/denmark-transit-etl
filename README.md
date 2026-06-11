# denmark-transit-etl

![code coverage badge](https://github.com/lymvs/denmark-transit-etl/actions/workflows/ruff.yml/badge.svg)

An ETL pipeline for monitoring and analyzing public transit data from GTFS feeds.

## System Overview

The ETL pipeline implementation follows the medallion architecture. 

- GTFS data are being fetched in a zip file from Rejseplannen site via HTTP request
- The zip file is extracted and stored temporarily in the landing zone 
- Raw tables are being stored as bronze layer in a PostgreSQL database
- 

## Installation

## Contributing

## License

[MIT](https://chooselicense.com/licenses/mit/)
