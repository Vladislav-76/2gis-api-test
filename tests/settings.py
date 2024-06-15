import logging
from pathlib import Path

LOG_FILE_PATH = f"{Path(__file__).parent}/logs/tests.log"
LOG_LEVEL = logging.INFO

LOCATION_RESPONSE_TYPES = {"id": int, "title": str, "lat": float, "lon": float, "color": str, "created_at": str}
OPTIONAL_LOCATION_FIELDS = ("color",)
REQUIED_LOCATION_FIELDS = ("title", "lat", "lon")
CORRECT_LOCATION_DATA = {"title": "Title", "lat": 8.028364, "lon": 73.925501, "color": "RED"}
CORRECT_LOCATION_TITLES = ("Fg Пюё;(50)", ".,;:-?!( )\"", "s", f"{'s' * 999}")
INCORRECT_LOCATION_TITLES = ("", f"{'s' * 1000}", "f#№$", 5, None, ["s"], {"s": "s"})
CORRECT_LOCATION_LATS = (90, 0, -90)
INCORRECT_LOCATION_LATS = (90.000001, -90.000001, "lat", None, [51, 55], {"lat": 51})
CORRECT_LOCATION_LONS = (180, 0, -180)
INCORRECT_LOCATION_LONS = (180.000001, -180.000001, "lon", None, [51, 55], {"lon": 51})
CORRECT_LOCATION_COLORS = ("BLUE", "GREEN", "RED", "YELLOW", None)
INCORRECT_LOCATION_COLORS = ("blue", "BLUEstarts", "endsBLUE", "BLACK", 6, ["BLUE", "GREEN"], {"BLUE": "GREEN"})

REQUESTS_NUMBERS = (10, 50, 100)
