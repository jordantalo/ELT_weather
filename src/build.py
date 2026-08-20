import duckdb
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "weather_warehouse.duckdb"

def build_gold_tables():
	print("[Gold] Starting Gold layer transformation...")

	connection = duckdb.connect(str(DB_PATH))

	query_insert_j1 = """


	"""

	query_insert_rolling_temp = """

	"""

	query_comp_normals = """
		
	"""

	df = connection.execute(query_insert_j1).df()
	print("\n--- Aperçu des données calculées (Pandas DataFrame) ---")
	print(df)

	connection.close()


if __name__ == "__main__":
    build_gold_tables()
