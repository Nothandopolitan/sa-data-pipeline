"""Downloads SAPS annual crime statistics (2019/2020 to 2024/2025)
and Stats SA unemployment data into data/raw/.
"""

import requests
from pathlib import Path

RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "saps"
RAW_DIR.mkdir(parents=True, exist_ok=True)

SAPS_FILES = {
    "2019_2020": "https://www.saps.gov.za/services/Crime-Statistics-2019_2020.xlsx",
    "2020_2021": "https://www.saps.gov.za/services/downloads/Crime-Statistics-2020_2021-Release.xlsx",
    "2021_2022": "https://www.saps.gov.za/services/downloads/Crime-Statistics-2021_2022-latest.xlsx",
    "2023_2024": "https://www.saps.gov.za/services/downloads/2023-2024%20_Annual_Financial%20year_WEB.xlsx",
    "2024_2025": "https://www.saps.gov.za/services/downloads/2024-2025%20_Annual_Financial%20year_WEB.xlsx",
}


def download_file(url, destination):
    if destination.exists():
        print(f"Already have {destination.name}, skipping.")
        return
    response = requests.get(url, timeout=60)
    response.raise_for_status()
    destination.write_bytes(response.content)
    print(f"Downloaded {destination.name}")


def extract():
    for year, url in SAPS_FILES.items():
        destination = RAW_DIR / f"saps_crime_{year}.xlsx"
        try:
            download_file(url, destination)
        except requests.RequestException as e:
            print(f"Failed to download {year}: {e}")


if __name__ == "__main__":
    extract()
