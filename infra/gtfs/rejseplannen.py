"""Download and store zipfiles for GTFS data."""

import hashlib
import logging
from io import BytesIO
from zipfile import ZipFile

import requests

logger = logging.getLogger(__name__)

URL = "https://www.rejseplanen.info/labs/GTFS.zip"


def fetch_files(logger: logging.Logger, temp: str) -> str:
    """Download zipfile and extract files to directory.

    Zipfile is stored in-memory.
    Hashes the input data and returns a hexadecimal string.
    """
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()

        hex_dig = hashlib.sha256(response.content).hexdigest()

        response_bytes = BytesIO(response.content)
        with ZipFile(response_bytes) as zip_file:
            zip_file.extractall(path=temp)

    except requests.exceptions.HTTPError as e:
        logger.warning("HTTP error occured: %s", e)
        raise
    except requests.exceptions.ConnectionError as e:
        logger.warning("Connection error occured: %s", e)
        raise
    except requests.exceptions.Timeout as e:
        logger.warning("Error occured: %s", e)
        raise
    except requests.exceptions.RequestException as e:
        logger.warning("An unexcpected error occured: %s", e)
        raise
    else:
        logger.info("Files extracted successfully")
        logger.info("Feed version %s", hex_dig)
        return hex_dig
