import logging
from pathlib import Path

LOG_FILE_PATH = f"{Path(__file__).parent}/logs/tests.log"
LOG_LEVEL = logging.INFO

LOCATION_RESPONSE_TYPES = {"id": int, "title": str, "lat": float, "lon": float, "color": str, "created_at": str}
OPTIONAL_LOCATION_FIELDS = ("color",)
REQUIED_LOCATION_FIELDS = ("title", "lat", "lon")
CORRECT_LOCATION_DATA = {"title": "Title", "lat": 8.028364, "lon": 73.925501, "color": "RED"}

