from pathlib import Path
import os

# Directory paths
NORMALS_DIR = Path(os.getenv("NORMALS_DIR"))
DAILY_DIR = Path(os.getenv("DAILY_DIR"))
DEBUG_DIR = Path(os.getenv("DEBUG_DIR"))
RAW_DIR = Path(os.getenv("RAW_DIR"))
PROJECT_DIR = Path(os.getenv("PROJECT_DIR"))

# Database path
DB_PATH = Path(os.getenv("DB_PATH"))

def init_directories():
	RAW_DIR.mkdir(parents=True, exist_ok=True)
	DEBUG_DIR.mkdir(parents=True, exist_ok=True)
	NORMALS_DIR.mkdir(parents=True, exist_ok=True)
	DAILY_DIR.mkdir(parents=True, exist_ok=True)
	print(f"[CONFIG] Target directories verified: {RAW_DIR} | {DEBUG_DIR} | {NORMALS_DIR} | {DAILY_DIR}")

CITIES = {
	"Paris": {"lat": 48.8566, "lon": 2.3822},
	"London": {"lat": 51.5074, "lon": -0.1278},
	"Tokyo": {"lat": 35.6762, "lon": 139.6503},
	"NewYork": {"lat": 40.7128, "lon": -74.0060}
}
