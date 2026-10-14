"""Stage 1: Extract. Download the raw SAPS crime file into data/raw/."""

import logging

import requests

from src.config import RAW_DIR, SAPS_CRIME_FILE, SAPS_CRIME_URL

logger = logging.getLogger(__name__)


def download_file(url, destination):
    logger.info("Downloading %s", url)
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    destination.write_bytes(response.content)
    logger.info("Saved %s (%d bytes)", destination, len(response.content))


def extract():
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destination = RAW_DIR / SAPS_CRIME_FILE
    if destination.exists():
        logger.info("%s already exists, skipping download", destination)
        return
    download_file(SAPS_CRIME_URL, destination)


if __name__ == "__main__":
    from src.log_setup import setup_logging

    setup_logging()
    extract()
