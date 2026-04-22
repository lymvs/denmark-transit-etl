"""Download and store zipfiles for GTFS data."""
import logging
from io import BytesIO
from zipfile import ZipFile

import requests

logger = logging.getLogger(__name__)

URL = "https://www.rejseplanen.info/labs/GTFS.zip"


def download_files() -> None:
    """Download zipfile and extract files to directory."""
    try:
        response = requests.get(URL, timeout=10)
        response.raise_for_status()
        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(path="temp/")
        logger.info("Files extracted successfully.")
    except requests.exceptions.HTTPError as e:
        logger.info("HTTP error occured: %e", e)
    except requests.exceptions.ConnectionError as e:
        logger.info("Connection error occured: %e", e)
    except requests.exceptions.Timeout as e:
        logger.info("Timeout error occured: %s", e)
    except requests.exceptions.RequestException as e:
        logger.info("An unexcpected error occured: %s", e)
