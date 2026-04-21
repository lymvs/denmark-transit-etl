import logging
from io import BytesIO
from zipfile import ZipFile

import requests

logger = logging.getLogger(__name__)

URL = "https://www.rejseplanen.info/labs/GTFS.zip"


def download_files() -> None:
    """Download zipfile and extract files to directory."""
    response = requests.get(URL, timeout=10)

    if response.status_code == 200:
        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(path="temp/")
        logger.info("Files extracted successfully.")
    else:
        msg = f"Failed to downlaod files: {response.text}"
        raise Exception(msg)
