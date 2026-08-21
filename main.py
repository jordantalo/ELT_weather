from src.config import CITIES, DB_PATH, RAW_DIR, DEBUG_DIR, init_directories
from src.extract import fetch_city_data
from src.load import save_raw_data
from src.load import load_into_silver_table
from src.build import build_gold_table
from src.extract_histo import fetch_archive_data 

def main():

    init_directories()

    if not DB_PATH.exists():
        print("Need to get historical data to feed the climate reference temperature datatable")
        fetch_archive_data()

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
