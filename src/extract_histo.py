import requests
import duckdb
from datetime import datetime
from pathlib import Path
from config import CITIES
from duckdb import DuckDBPyConnection
import pandas as pd

METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "weather_warehouse.duckdb"

def add_to_table(data: dict, city_name:  str, connection: DuckDBPyConnection):
	df = pd.DataFrame({
		"time": data["hourly"]["time"],
		"temperature_celsius": data["hourly"]["temperature_2m"]
	})

	connection.execute(f"""
		CREATE OR REPLACE TEMPORARY TABLE temp_raw_histo AS
		SELECT
		? AS city_name,
		time::TIMESTAMP AS weather_timestamp,
		temperature_celsius::DOUBLE AS temperature_celsius
		FROM df;
		""", [city_name])

	connection.execute("""
		INSERT INTO ref_climate_normals
		SELECT
			city_name,
			STRFTIME(weather_timestamp, '%m-%d') AS day_of_year,

			ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 6 AND 11 THEN temperature_celsius END), 2) AS normal_temp_avg_morning,
			ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 12 AND 17 THEN temperature_celsius END), 2) AS normal_temp_avg_afternoon,
			ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 18 AND 23 THEN temperature_celsius END), 2) AS normal_temp_avg_evening,
			ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 0 AND 5 THEN temperature_celsius END), 2) AS normal_temp_avg_night

			FROM temp_raw_histo
			GROUP BY city_name, STRFTIME(weather_timestamp, '%m-%d')
			ON CONFLICT (city_name, day_of_year) DO UPDATE SET
				normal_temp_avg_morning = EXCLUDED.normal_temp_avg_morning,
				normal_temp_avg_afternoon = EXCLUDED.normal_temp_avg_afternoon,
				normal_temp_avg_evening = EXCLUDED.normal_temp_avg_evening,
				normal_temp_avg_night = EXCLUDED.normal_temp_avg_night
		""")

	print(f"Archive data for {city_name} has been saved in ref_climate_normals")

def fetch_archive_data():

	connection = duckdb.connect(str(DB_PATH))

	connection.execute("""
		CREATE TABLE IF NOT EXISTS ref_climate_normals (
			city_name VARCHAR,
			day_of_year VARCHAR,
			normal_temp_avg_morning DOUBLE,
			normal_temp_avg_afternoon DOUBLE,
			normal_temp_avg_evening DOUBLE,
			normal_temp_avg_night DOUBLE,
			PRIMARY KEY (city_name, day_of_year)
		);
	""")

	for city_name, coords in CITIES.items():

		params = {
			"latitude": coords["lat"],
			"longitude": coords["lon"],
			"start_date": "2020-01-01",
			"end_date": "2025-12-31",
			"hourly": "temperature_2m"
		}

		res = requests.get(
			METEO_ARCHIVE_URL,
			params=params
		)

		if res.status_code == 200:
			add_to_table(res.json(), city_name, connection)

	print("=== [HISTO] TABLE ref_climate_normals initialized")

	connection.close()

if (__name__ == "__main__"):
	fetch_archive_data()
