import duckdb
from datetime import datetime
from pathlib import Path
from src.config import PROJECT_ROOT, DB_PATH, DEBUG_DIR

SQL_DIR = PROJECT_ROOT / "scripts" / "sql"

DEBUG_DIR.mkdir(parents=True, exist_ok=True)

connection = duckdb.connect(str(DB_PATH))

with open(SQL_DIR / "export_silver_paris_data.sql", "r", encoding="utf-8") as f:
	debug_query = f.read()

connection.execute(debug_query)

with open(SQL_DIR / "export_normals.sql", "r", encoding="utf-8") as f:
	debug_query = f.read()

connection.execute(debug_query)

with open(SQL_DIR / "export_gold_paris_data.sql", "r", encoding="utf-8") as f:
	debug_query = f.read()

connection.execute(debug_query)

connection.close()
