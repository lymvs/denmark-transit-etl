import logging

import requests
from zipfile import ZipFile
from io import BytesIO

logger = logging.getLogger(__name__)

URL = "https://www.rejseplanen.info/labs/GTFS.zip"


def download_files() -> None:
    response = requests.get(URL)

    if response.status_code == 200:
        with ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(path="temp/")
        logger.info("Files extracted successfully.")
    else:
        raise Exception(f"Failed to download files: {response.text}")
