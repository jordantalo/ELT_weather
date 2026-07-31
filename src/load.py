import json
import duckdb
from datetime import datetime
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
RAW_DIR = PROJECT_ROOT / "data" / "raw"
DB_PATH = PROJECT_ROOT / "data" / "weather_warehouse.duckdb"

def save_raw_data(data: list) -> Path:

	RAW_DIR.mkdir(parents=True, exist_ok=True)

	filename = f"weather_raw_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
	filepath = RAW_DIR / filename

	with open(filepath, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

	print(f"[LOAD] raw data saved in: {filepath}")
	return filepath

def sync_json_to_duckdb():

	json_files = list(RAW_DIR.glob("*.json"))
	if not json_files:
		print("[WARNING No json files found in data/raw")
		return

	latest_file = max(json_files, key=lambda f: f.stat().st_mtime)
	print(f"[DUCKDB] Last file found : {latest_file.name}")

	connection = duckdb.connect(str(DB_PATH))

	connection.execute("""
		CREATE TABLE IF NOT EXISTS silver_weather (
			city_name VARCHAR,
			weather_timestamp TIMESTAMP,
			temperature_celsius DOUBLE,
			pm2_5 DOUBLE,
			pm10 DOUBLE,
			ingested_at TIMESTAMP,
			PRIMARY KEY (city_name, weather_timestamp)
		);
	""")

	connection.execute(f"""
		CREATE TEMPORARY TABLE staging_data AS
		SELECT
			city AS city_name,
			unnest(weather.time)::TIMESTAMP AS weather_timestamp,
			unnest(weather.temperature_2m)::DOUBLE AS temperature_celsius,
			unnest(air_quality.pm10)::DOUBLE AS pm10,
			unnest(air_quality.pm2_5)::DOUBLE AS pm2_5,
			current_timestamp AS ingested_at
		FROM read_json_auto('{latest_file}')
	""")

	connection.execute("""
		INSERT INTO silver_weather
		SELECT city_name, weather_timestamp, temperature_celsius, pm2_5, pm10, ingested_at
		FROM staging_data
		ON CONFLICT (city_name, weather_timestamp)
		DO UPDATE SET
			temperature_celsius = EXCLUDED.temperature_celsius,
			pm2_5 = EXCLUDED.pm2_5,
			pm10 = EXCLUDED.pm10,
			ingested_at = EXCLUDED.ingested_at;
	""")

	connection.close()
