import requests
import duckdb
from datetime import datetime
from pathlib import Path
from config import CITIES
from duckdb import DuckDBPyConnection
import pandas as pd
from src.config import SQL_DIR, DB_PATH

METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"
NORMALS_DIR = SQL_DIR / "normals"

def add_to_table(data: dict, city_name:  str, connection: DuckDBPyConnection):
	df = pd.DataFrame({
		"time": data["hourly"]["time"],
		"temperature_celsius": data["hourly"]["temperature_2m"]
	})

	with open(NORMALS_DIR / "02_save_normals_temp.sql", "r", encoding="utf-8") as f:
		query_temp_table = f.read()

	connection.execute(query_temp_table, [city_name])

	with open(NORMALS_DIR / "03_insert_into_normals_table.sql", "r", encoding="utf-8") as f:
		query_normals_table = f.read()

	connection.execute(query_normals_table)

	print(f"Archive data for {city_name} has been saved in ref_climate_normals")

def fetch_archive_data():

	connection = duckdb.connect(str(DB_PATH))

	with open(NORMALS_DIR / "01_create_normals_table.sql", "r", encoding="utf-8") as f:
		create_normal_table_sql = f.read()

	connection.execute(create_normal_table_sql)

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
