import requests
from config import CITIES

url = "https://api.open-meteo.com/v1/forecast"

for city_name, coords in CITIES.items():

    params = {
        "latitude": coords["lat"],
        "longitude": coords["lon"],
        "past_days": 30,
        "forecast_days": 5,
        "hourly": "temperature_2m",
        "models": "meteofrance_seamless"
    }

    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        print(f"Success for {city_name}")
    else:
        print(
            f"Error {response.status_code} when retrieving {city_name} meteo data"
        )

