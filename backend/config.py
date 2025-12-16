import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "data", "ticks.db")

TIMEFRAMES = {
    "1 Second": "1S",
    "5 Seconds": "5S",
    "1 Minute": "1T"
}
