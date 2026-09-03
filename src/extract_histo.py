import requests
import duckdb
import json
from datetime import datetime
from pathlib import Path
from duckdb import DuckDBPyConnection
import pandas as pd
from src.config import CITIES, RAW_DIR

METEO_ARCHIVE_URL = "https://archive-api.open-meteo.com/v1/archive"

def save_normals_data(data: list) -> Path:

	filename = f"normals_{datetime.now().strftime('%Y')}.json"
	filepath = RAW_DIR / filename

	with open(filepath, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

	print(f"[LOAD] raw data saved in: {filepath}")
	return filepath

def fetch_archive_data():

	all_city_normals = []

	for city_name, coords in CITIES.items():

		params = {
			"latitude": coords["lat"],
			"longitude": coords["lon"],
			"start_date": "2000-01-01",
			"end_date": "2025-12-31",
			"hourly": "temperature_2m",
			"timezone": "auto"
		}

		res = requests.get(
			METEO_ARCHIVE_URL,
			params=params
		)

		if res.status_code == 200:
			all_city_normals.append({
				"city": city_name,
				"extracted_at": datetime.now().isoformat(),
				"data": res.json()
				})
		else:
			print(f"[WARNING] Erreur {res.status_code} pour {city_name}")

	if all_city_normals:
		save_normals_data(all_city_normals)
		print("=== Raw normals file saved !")
	else:
		print("[ERROR] No data saved !")

if (__name__ == "__main__"):
	fetch_archive_data()
