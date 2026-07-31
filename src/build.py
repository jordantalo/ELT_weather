import duckdb
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "weather_warehouse.duckdb"

def build_gold_tables():
	print("[Gold] Starting Gold layer transformation...")

	connection = duckdb.connect(str(DB_PATH))

	connection.execute("""
		CREATE TABLE IF NOT EXISTS gold_daily_city_metrics (
			city_name VARCHAR,
			date DATE,

			temp_morning_avg DOUBLE,
			temp_afternoon_avg DOUBLE,
			temp_evening_avg DOUBLE,
			temp_night_avg DOUBLE,
			temp_max_day DOUBLE,
			temp_min_day DOUBLE,

			pm2_5_day_avg DOUBLE,
			pm2_5_day_max DOUBLE,
			pm2_5_hours_above_threshold INT,
			pm10_day_avg DOUBLE,
			pm10_day_max DOUBLE,
			pm10_hours_above_threshold INT,

			temp_morning_avg_rolling_7d DOUBLE,
			temp_afternoon_avg_rolling_7d DOUBLE,
			temp_evening_avg_rolling_7d DOUBLE,
			temp_night_avg_rolling_7d DOUBLE,

			temp_morning_avg_rolling_30d DOUBLE,
			temp_afternoon_avg_rolling_30d DOUBLE,
			temp_evening_avg_rolling_30d DOUBLE,
			temp_night_avg_rolling_30d DOUBLE,

			temp_gap_with_normals_morning,
			temp_gap_with_normals_afternoon,
			temp_gap_with_normals_evening,
			temp_gap_with_normals_night
		);
	""")
