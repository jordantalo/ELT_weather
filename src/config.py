from pathlib import Path

# Project root directory
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Directory paths
DATA_DIR = PROJECT_ROOT / "data"
RAW_DIR = DATA_DIR / "raw"
DEBUG_DIR = DATA_DIR / "debug_exports"

# Database path
DB_PATH = DATA_DIR / "weather.duckdb"

def init_directories():
	RAW_DIR.mkdir(parents=True, exist_ok=True)
	DEBUG_DIR.mkdir(parents=True, exist_ok=True)
	print(f"[CONFIG] Target directories verified: {RAW_DIR} | {DEBUG_DIR}")

CITIES = {
	"Paris": {"lat": 48.8566, "lon": 2.3822},
	"London": {"lat": 51.5074, "lon": -0.1278},
	"Tokyo": {"lat": 35.6762, "lon": 139.6503},
	"NewYork": {"lat": 40.7128, "lon": -74.0060}
}
