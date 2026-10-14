"""Paths and URLs used across the pipeline."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
RAW_DIR = BASE_DIR / "data" / "raw"
CLEAN_DIR = BASE_DIR / "data" / "clean"
LOG_DIR = BASE_DIR / "logs"

SAPS_CRIME_URL = (
    "https://data.code4sa.org/api/views/pknu-xarf/rows.csv?accessType=DOWNLOAD"
)
SAPS_CRIME_FILE = "saps_crime_provincial_2005_2015.csv"
