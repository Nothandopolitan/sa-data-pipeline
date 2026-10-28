"""Downloads SAPS annual crime statistics (2019/2020 to 2024/2025)
and Stats SA unemployment trends into data/raw/.
"""

import requests
import urllib3
from pathlib import Path

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

SAPS_RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "saps"
SAPS_RAW_DIR.mkdir(parents=True, exist_ok=True)

STATSSA_RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw" / "statssa"
STATSSA_RAW_DIR.mkdir(parents=True, exist_ok=True)

SAPS_FILES = {
    "2019_2020": "https://www.saps.gov.za/services/Crime-Statistics-2019_2020.xlsx",
    "2020_2021": "https://www.saps.gov.za/services/downloads/Crime-Statistics-2020_2021-Release.xlsx",
    "2021_2022": "https://www.saps.gov.za/services/downloads/Crime-Statistics-2021_2022-latest.xlsx",
    "2024_2025": "https://www.saps.gov.za/services/downloads/2024-2025%20_Annual_Financial%20year_WEB.xlsx",
}

STATSSA_URL = "https://www.statssa.gov.za/publications/P0211/QLFS%20Trends%202008-2025Q4.xlsx"


def download_file(url, destination):
    if destination.exists():
        print(f"Already have {destination.name}, skipping.")
        return
    response = requests.get(url, timeout=60, verify=False)
    response.raise_for_status()
    destination.write_bytes(response.content)
    print(f"Downloaded {destination.name}")


def extract():
    for year, url in SAPS_FILES.items():
        destination = SAPS_RAW_DIR / f"saps_crime_{year}.xlsx"
        try:
            download_file(url, destination)
        except requests.RequestException as e:
            print(f"Failed to download {year}: {e}")

    statssa_destination = STATSSA_RAW_DIR / "qlfs_trends_2008_2025.xlsx"
    try:
        download_file(STATSSA_URL, statssa_destination)
    except requests.RequestException as e:
        print(f"Failed to download Stats SA QLFS trends: {e}")


if __name__ == "__main__":
    extract()