import duckdb
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "weather_warehouse.duckdb"
SQL_DIR = PROJECT_ROOT / "sql" / "gold"

def build_gold_table():
	print("[Gold] Starting Gold layer transformation...")

	connection = duckdb.connect(str(DB_PATH))

	with open(SQL_DIR / "01_create_gold_table.sql", "r", encoding="utf-8") as f:
		create_gold_table = f.read()

	connection.execute(create_gold_table)

	with open(SQL_DIR / "02_insert_daily_j1.sql", "r", encoding="utf-8") as f:
		insert_daily_temp_j1 = f.read()

	connection.execute(insert_daily_temp_j1)

	with open(SQL_DIR / "03_update_rolling_metrics.sql", "r", encoding="utf-8") as f:
		update_rolling_metrics = f.read()

	connection.execute(update_rolling_metrics)

	with open(SQL_DIR / "04_update_climate_normals.sql", "r", encoding="utf-8") as f:
		update_climate_normals = f.read()

	connection.execute(update_climate_normals)

	connection.close()
