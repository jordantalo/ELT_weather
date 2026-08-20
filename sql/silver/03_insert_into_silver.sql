INSERT INTO silver_weather
SELECT city_name, weather_timestamp, temperature_celsius, pm2_5, pm10, ingested_at
FROM staging_data
ON CONFLICT (city_name, weather_timestamp)
DO UPDATE SET
	temperature_celsius = EXCLUDED.temperature_celsius,
	pm2_5 = EXCLUDED.pm2_5,
	pm10 = EXCLUDED.pm10,
	ingested_at = EXCLUDED.ingested_at;
