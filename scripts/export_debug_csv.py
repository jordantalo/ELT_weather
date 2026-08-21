import duckdb
from datetime import datetime
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "data" / "weather_warehouse.duckdb"
SQL_DIR = PROJECT_ROOT / "scripts" / "sql"

connection = duckdb.connect(str(DB_PATH))

with open(SQL_DIR / "export_silver_paris_data.sql", "r", encoding="utf-8") as f:
	debug_query = f.read()

connection.execute(debug_query)

with open(SQL_DIR / "export_normals.sql", "r", encoding="utf-8") as f:
	debug_query = f.read()

connection.execute(debug_query)

with open(SQL_DIR / "export_gold_paris_data.sql", "r", encoding="utf-8") as f:
	debug_query = f.read()

connection.execute(debug_query)

connection.close()
