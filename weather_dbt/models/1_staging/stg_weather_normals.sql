{{ config(materialized='table') }}

WITH normals_raw AS (
	SELECT
		city AS city_name,
		unnest(data.hourly.time)::TIMESTAMP AS weather_timestamp,
		unnest(data.hourly.temperature_2m)::DOUBLE AS temperature_celsius
	FROM read_json_auto('{{ env_var("NORMALS_DIR") }}/normals_*.json', filename = true)
),

normals_ref AS (
	SELECT
		city_name,
		STRFTIME(weather_timestamp, '%m-%d') AS day_of_year,
		ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 6 AND 11 THEN temperature_celsius END), 2) AS normal_temp_avg_morning,
		ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 12 AND 17 THEN temperature_celsius END), 2) AS normal_temp_avg_afternoon,
		ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 18 AND 23 THEN temperature_celsius END), 2) AS normal_temp_avg_evening,
		ROUND(AVG(CASE WHEN EXTRACT(HOUR FROM weather_timestamp) BETWEEN 0 AND 5 THEN temperature_celsius END), 2) AS normal_temp_avg_night
	FROM normals_raw
	GROUP BY city_name, day_of_year
)

SELECT * FROM normals_ref
