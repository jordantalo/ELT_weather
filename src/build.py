import duckdb
from pathlib import Path
from src.config import SQL_DIR, DB_PATH

GOLD_DIR = SQL_DIR / "gold"

def build_gold_table():
	print("[Gold] Starting Gold layer transformation...")

	connection = duckdb.connect(str(DB_PATH))

	with open(GOLD_DIR / "01_create_gold_table.sql", "r", encoding="utf-8") as f:
		create_gold_table = f.read()

	connection.execute(create_gold_table)

	with open(GOLD_DIR / "02_insert_daily_j1.sql", "r", encoding="utf-8") as f:
		insert_daily_temp_j1 = f.read()

	connection.execute(insert_daily_temp_j1)

	with open(GOLD_DIR / "03_update_rolling_metrics.sql", "r", encoding="utf-8") as f:
		update_rolling_metrics = f.read()

	connection.execute(update_rolling_metrics)

	with open(GOLD_DIR / "04_update_climate_normals.sql", "r", encoding="utf-8") as f:
		update_climate_normals = f.read()

	connection.execute(update_climate_normals)

	connection.close()
