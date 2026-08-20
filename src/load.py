import json
import duckdb
from datetime import datetime
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "data" / "weather_warehouse.duckdb"
SQL_DIR = PROJECT_ROOT / "sql"

def save_raw_data(data: list) -> Path:

	RAW_DIR.mkdir(parents=True, exist_ok=True)

	filename = f"weather_raw_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
	filepath = RAW_DIR / filename

	with open(filepath, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

	print(f"[LOAD] raw data saved in: {filepath}")
	return filepath

def load_into_silver_table():

	json_files = list(RAW_DIR.glob("*.json"))
	if not json_files:
		print("[WARNING No json files found in data/raw")
		return

	latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
	print(f"[DUCKDB] Last file found : {latest_file.name}")

	connection = duckdb.connect(str(DB_PATH))

	with open(SQL_DIR / "01_create_silver_table.sql", "r", encoding="utf-8") as f:
		query_create_silver_table = f.read()

	connection.execute(query_create_silver_table)

	with open(SQL_DIR / "02_load_from_json.sql", "r", encoding="utf-8") as f:
		query_load_json = f.read()

	connection.execute(query_load_json, [str(latest_file)])

	with open(SQL_DIR / "03_insert_into_silver", "r", encoding="utf-8") as f:
		query_insert_into_silver = f.read()

	connection.execute(query_insert_into_silver)

	connection.close()
