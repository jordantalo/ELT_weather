INSERT INTO ref_climate_normals
SELECT
	city_name,
	STRFTIME(weather_timestamp, '%m-%d') AS day_of_year,

	ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 6 AND 11 THEN temperature_celsius END), 2) AS normal_temp_avg_morning,
	ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 12 AND 17 THEN temperature_celsius END), 2) AS normal_temp_avg_afternoon,
	ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 18 AND 23 THEN temperature_celsius END), 2) AS normal_temp_avg_evening,
	ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 0 AND 5 THEN temperature_celsius END), 2) AS normal_temp_avg_night

FROM temp_raw_histo
GROUP BY city_name, STRFTIME(weather_timestamp, '%m-%d')
ON CONFLICT (city_name, day_of_year) DO UPDATE SET
	normal_temp_avg_morning = EXCLUDED.normal_temp_avg_morning,
	normal_temp_avg_afternoon = EXCLUDED.normal_temp_avg_afternoon,
	normal_temp_avg_evening = EXCLUDED.normal_temp_avg_evening,
	normal_temp_avg_night = EXCLUDED.normal_temp_avg_night;
