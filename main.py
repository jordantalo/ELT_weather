from src.config import CITIES
from src.extract import fetch_city_data
from src.load import save_raw_data
from src.load import load_into_silver_table
from src.build import build_gold_table

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

		load_into_silver_table()
		build_gold_table()

	else:
		print("[WARNING] No data saved")

if __name__ == "__main__":
	main()
