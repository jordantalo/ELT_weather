import duckdb

connection = duckdb.connect("data/weather_warehouse.duckdb")

count = connection.execute("SELECT COUNT(*) FROM ref_climate_normals").fetchone()[0]
print(f"total lines : {count}")

df = connection.execute("""
	SELECT *
	FROM ref_climate_normals
	WHERE city_name = 'Paris'
	ORDER BY day_of_year
	LIMIT 10
	""").df()

print(df)

connection.close()
