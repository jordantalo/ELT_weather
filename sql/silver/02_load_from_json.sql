CREATE TEMPORARY TABLE staging_data AS
	SELECT
		city AS city_name,
		unnest(weather.time)::TIMESTAMP AS weather_timestamp,
		unnest(weather.temperature_2m)::DOUBLE AS temperature_celsius,
		unnest(air_quality.pm10)::DOUBLE AS pm10,
		unnest(air_quality.pm2_5)::DOUBLE AS pm2_5,
		current_timestamp AS ingested_at
	FROM read_json_auto(?);
