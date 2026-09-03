{{
	config (
		materialized='incremental',
		unique_key=['city_name', 'date'],
		incremental_strategy='merge'
	)
}}

WITH daily_j1 AS (
	SELECT
		city_name,
		date,

		AVG(temp_morning) AS temp_morning_avg,
		AVG(temp_afternoon) AS temp_afternoon_avg,
		AVG(temp_evening) AS temp_evening_avg,
		AVG(temp_night) AS temp_night_avg,
		MAX(temperature_celsius) AS temp_max,
		MIN(temperature_celsius) AS temp_min,

		AVG(pm2_5) AS pm2_5_avg,
		AVG(CASE WHEN period_of_day = 'morning' THEN pm2_5 END) AS pm2_5_morning_avg,
		AVG(CASE WHEN period_of_day = 'afternoon' THEN pm2_5 END) AS pm2_5_afternoon_avg,
		AVG(CASE WHEN period_of_day = 'evening' THEN pm2_5 END) AS pm2_5_evening_avg,
		AVG(CASE WHEN period_of_day = 'night' THEN pm2_5 END) AS pm2_5_night_avg,
		MAX(pm2_5) AS pm2_5_max,
		SUM(flag_oms_pm25_exceeded) AS hours_pm2_5_exceeded_oms,
		SUM(flag_fr_pm25_exceeded) AS hours_pm2_5_exceeded_fr,

		AVG(pm10) AS pm10_avg,
		AVG(CASE WHEN period_of_day = 'morning' THEN pm10 END) AS pm10_morning_avg,
		AVG(CASE WHEN period_of_day = 'afternoon' THEN pm10 END) AS pm10_afternoon_avg,
		AVG(CASE WHEN period_of_day = 'evening' THEN pm10 END) AS pm10_evening_avg,
		AVG(CASE WHEN period_of_day = 'night' THEN pm10 END) AS pm10_night_avg,
		MAX(pm10) AS pm10_max_j1,
		SUM(flag_oms_pm10_exceeded) AS hours_pm10_exceeded_oms,
		SUM(flag_fr_pm10_exceeded) AS hours_pm10_exceeded_fr

		FROM {{ref('int_weather_prepared')}}

		{% if is_incremental() %}

			WHERE date >= (SELECT MAX(date) - INTERVAL '31 days' FROM {{ this }})

		{% else %}

			WHERE date >= CURRENT_DATE - INTERVAL '31 days'

		{% endif %}

		GROUP BY city_name, date
),

add_rolling_metrics AS (
	SELECT
		*,

		AVG(temp_morning_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS r30_morning,
		AVG(temp_afternoon_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS r30_afternoon,
		AVG(temp_evening_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS r30_evening,
		AVG(temp_night_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS r30_night,

		AVG(temp_morning_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS r7_morning,
		AVG(temp_afternoon_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS r7_afternoon,
		AVG(temp_evening_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS r7_evening,
		AVG(temp_night_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS r7_night,

		AVG(temp_morning_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 1 FOLLOWING AND 3 FOLLOWING) AS f3_morning,
		AVG(temp_afternoon_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 1 FOLLOWING AND 3 FOLLOWING) AS f3_afternoon,
		AVG(temp_evening_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 1 FOLLOWING AND 3 FOLLOWING) AS f3_evening,
		AVG(temp_night_avg) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 1 FOLLOWING AND 3 FOLLOWING) AS f3_night

	FROM daily_j1
)

SELECT * FROM add_rolling_metrics

{% if is_incremental() %}

	WHERE date BETWEEN
		(SELECT MAX(date) - INTERVAL '1 day' FROM {{ this }})
		AND
		(CURRENT_DATE - INTERVAL '1 day')

{% else %}

	WHERE date = CURRENT_DATE - INTERVAL '1 day'

{% endif %}
