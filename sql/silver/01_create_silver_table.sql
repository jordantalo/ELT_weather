CREATE TABLE IF NOT EXISTS silver_weather (
	city_name VARCHAR,
	weather_timestamp TIMESTAMP,
	temperature_celsius DOUBLE,
	pm2_5 DOUBLE,
	pm10 DOUBLE,
	ingested_at TIMESTAMP,
	PRIMARY KEY (city_name, weather_timestamp)
);
