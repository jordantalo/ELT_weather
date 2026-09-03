{{
	config (
		materialized='view',
	)
}}

WITH weather_prepared AS (
	SELECT
		CAST(weather_timestamp AS DATE) AS date,
		city_name,
		pm2_5,
		pm10,
		temperature_celsius,
		weather_timestamp,

		CASE WHEN HOUR(weather_timestamp) BETWEEN 6 AND 11 THEN temperature_celsius END AS temp_morning,
		CASE WHEN HOUR(weather_timestamp) BETWEEN 12 AND 17 THEN temperature_celsius END AS temp_afternoon,
		CASE WHEN HOUR(weather_timestamp) BETWEEN 18 AND 22 THEN temperature_celsius END AS temp_evening,
		CASE WHEN HOUR(weather_timestamp) NOT BETWEEN 6 AND 22 THEN temperature_celsius END AS temp_night,

		CASE
			WHEN HOUR(weather_timestamp) BETWEEN 6 AND 11 THEN 'morning'
			WHEN HOUR(weather_timestamp) BETWEEN 12 AND 17 THEN 'afternoon'
			WHEN HOUR(weather_timestamp) BETWEEN 18 AND 22 THEN 'evening'
			ELSE 'night'
		END AS period_of_day,

		CASE WHEN pm2_5 > 15 THEN 1 ELSE 0 END AS flag_oms_pm25_exceeded,
		CASE WHEN pm2_5 > 50 THEN 1 ELSE 0 END AS flag_fr_pm25_exceeded,
		CASE WHEN pm10 > 45 THEN 1 ELSE 0 END AS flag_oms_pm10_exceeded,
		CASE WHEN pm10 > 50 THEN 1 ELSE 0 END AS flag_fr_pm10_exceeded

	FROM {{ref('stg_weather')}}
)

SELECT * FROM weather_prepared
