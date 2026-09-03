import requests
import json
from datetime import datetime
from pathlib import Path
from src.config import RAW_DIR

METEO_URL = "https://api.open-meteo.com/v1/forecast"
AIR_QUALITY_URL = "https://air-quality-api.open-meteo.com/v1/air-quality?"

def fetch_city_data(city_name: str, coords: dict) -> dict:
	base_params = {
		"latitude": coords["lat"],
		"longitude": coords["lon"],
		"past_days": 31,
		"forecast_days": 4,
        "timezone": "auto"
	}

	meteo_params = {
		"hourly": "temperature_2m",
		"models": "meteofrance_seamless"
	}

	air_params = {
		"hourly": "pm10,pm2_5"
	}

	final_meteo_params = base_params | meteo_params
	final_air_params = base_params | air_params

	meteo_res = requests.get(
		METEO_URL,
		params=final_meteo_params
	)

	air_res = requests.get(
		AIR_QUALITY_URL,
		params=final_air_params
	)

	if meteo_res.status_code == 200 and air_res.status_code == 200:
		return {
			"city":city_name,
			"extracted_at": datetime.now().isoformat(),
			"weather": meteo_res.json().get("hourly", {}),
			"air_quality": air_res.json().get("hourly", {})
		}

	else:
		print(
			f"Extract error when trying to retrieve {city_name} meteo data"
		)

	return None


def save_raw_data(data: list) -> Path:

	filename = f"weather_raw_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
	filepath = RAW_DIR / filename

	with open(filepath, "w", encoding="utf-8") as f:
		json.dump(data, f, ensure_ascii=False, indent=2)

	print(f"[LOAD] raw data saved in: {filepath}")
	return filepath
