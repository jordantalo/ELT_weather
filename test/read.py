import duckdb

connection = duckdb.connect("data/weather_warehouse.duckdb")

count = connection.execute("SELECT COUNT(*) FROM silver_weather").fetchone()[0]
print(f"total lines : {count}")

df = connection.execute("""
	SELECT *
	FROM silver_weather
	WHERE city_name = 'London'
	LIMIT 10
	""").df()

print(df)

connection.close()
