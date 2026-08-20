CREATE OR REPLACE TEMPORARY TABLE temp_raw_histo AS
SELECT
	? AS city_name,
	time::TIMESTAMP AS weather_timestamp,
	temperature_celsius::DOUBLE AS temperature_celsius
FROM df;
