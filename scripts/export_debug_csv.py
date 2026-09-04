import duckdb
from src.config import PROJECT_DIR, DB_PATH, DEBUG_DIR

SQL_DIR = PROJECT_DIR / "scripts" / "sql"

DEBUG_DIR.mkdir(parents=True, exist_ok=True)

connection = duckdb.connect(str(DB_PATH))

tables_to_export = [
	'stg_weather_normals',
	'stg_weather',
	'fct_insert_normals'
]

for table in tables_to_export:
	print(f"Export of the table {table} in CSV...")
	connection.execute(f"COPY (SELECT * FROM {table}) TO '{DEBUG_DIR}/{table}.csv' (HEADER, DELIMITER ',');")

print("Exports ended !")

connection.close()
