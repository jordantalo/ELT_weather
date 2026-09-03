{{
	config (
		materialized='incremental',
		unique_key=['city_name', 'date'],
		incremental_strategy='merge'
	)
}}

WITH stg_normals AS (
	SELECT *
	FROM {{ ref('stg_weather_normals') }}
),

daily_j1_with_normals AS (
	SELECT weather.*,

	weather.temp_morning_avg - normals.normal_temp_avg_morning AS temp_gap_with_normals_morning,
	weather.temp_afternoon_avg - normals.normal_temp_avg_afternoon AS temp_gap_with_normals_afternoon,
	weather.temp_evening_avg - normals.normal_temp_avg_evening AS temp_gap_with_normals_evening,
	weather.temp_night_avg - normals.normal_temp_avg_night AS temp_gap_with_normals_night

	FROM {{ ref('fct_insert_daily_j1')}} weather

	LEFT JOIN stg_normals normals
		ON weather.city_name = normals.city_name
		AND STRFTIME(weather.date, '%m-%d') = normals.day_of_year

	{% if is_incremental() %}
		WHERE weather.date > (SELECT MAX(date) FROM {{ this }})

	{% endif %}
)

SELECT * FROM daily_j1_with_normals
