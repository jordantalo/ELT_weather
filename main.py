from src.config import CITIES
from src.extract import fetch_city_data
from src.load import save_raw_data
from src.load import sync_json_to_duckdb

def main():

	all_data = []

	for city_name, coords in CITIES.items():
		print(f"Extraction for {city_name}...")
		data = fetch_city_data(city_name, coords)

		if (data):
			all_data.append(data)

	if all_data:
		saved_file_path = save_raw_data(all_data)
		print(f"\nExtraction ended ! {len(all_data)} processed")

		sync_json_to_duckdb()

	else:
		print("[WARNING] No data saved")

if __name__ == "__main__":
	main()
