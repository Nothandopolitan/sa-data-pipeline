"""Runs the whole pipeline from start to finish."""

import logging

from src.analyse import analyse
from src.clean import clean
from src.extract import extract
from src.load import load
from src.log_setup import setup_logging
from src.validate import validate

logger = logging.getLogger(__name__)


def main():
    setup_logging()
    logger.info("Pipeline started")
    extract()
    clean()
    validate()
    load()
    analyse()
    logger.info("Pipeline finished")


if __name__ == "__main__":
    main()
