WITH hourly_prepared AS (
	SELECT
		CAST(weather_timestamp AS DATE) AS date,
		city_name,
		pm2_5,
		pm10,
		temperature_celsius,

	CASE
		WHEN HOUR(weather_timestamp) BETWEEN 6 AND 11 THEN 'morning'
		WHEN HOUR(weather_timestamp) BETWEEN 12 AND 17 THEN 'afternoon'
		WHEN HOUR(weather_timestamp) BETWEEN 18 AND 22 THEN 'evening'
		ELSE 'night'
		END AS period_of_day,

	CASE WHEN pm2_5 > 15 THEN 1 ELSE 0 END AS flag_oms_pm25_exceeded,
	CASE WHEN pm2_5 > 50 THEN 1 ELSE 0 END AS flag_fr_pm25_exceeded,
	CASE WHEN pm10 > 45 THEN 1 ELSE 0 END AS flag_oms_pm10_exceeded,
	CASE WHEN pm10 > 50 THEN 1 ELSE 0 END AS flag_fr_pm10_exceeded,

	FROM silver_weather

	WHERE CAST(weather_timestamp AS DATE) = CURRENT_DATE - INTERVAL '1 day'
)

INSERT INTO gold_daily_city_metrics (
	city_name, date,
	temp_morning_avg_j1, temp_afternoon_avg_j1, temp_evening_avg_j1, temp_night_avg_j1,
	temp_max_j1, temp_min_j1,
	pm2_5_avg_j1, pm2_5_morning_avg, pm2_5_afternoon_avg, pm2_5_evening_avg, pm2_5_night_avg,
	pm2_5_max_j1, hours_pm2_5_exceeded_oms_j1, hours_pm2_5_exceeded_fr_j1,
	pm10_avg_j1, pm10_morning_avg, pm10_afternoon_avg, pm10_evening_avg, pm10_night_avg,
	pm10_max_j1, hours_pm10_exceeded_oms_j1, hours_pm10_exceeded_fr_j1
)

SELECT
	city_name,
	date,

	AVG(CASE WHEN period_of_day = 'morning' THEN temperature_celsius),
	AVG(CASE WHEN period_of_day = 'afternoon' THEN temperature_celsius),
	AVG(CASE WHEN period_of_day = 'evening' THEN temperature_celsius),
	AVG(CASE WHEN period_of_day = 'night' THEN temperature_celsius),
	MAX(temperature_celsius),
	MIN(temperature_celsius),

	AVG(pm2_5),
	AVG(CASE WHEN period_of_day = 'morning' THEN pm2_5 END),
	AVG(CASE WHEN period_of_day = 'afternoon' THEN pm2_5 END),
	AVG(CASE WHEN period_of_day = 'evening' THEN pm2_5 END),
	AVG(CASE WHEN period_of_day = 'night' THEN pm2_5 END),
	MAX(pm2_5),
	SUM(flag_oms_pm25_exceeded),
	SUM(flag_fr_pm25_exceeded),

	AVG(pm10),
	AVG(CASE WHEN period_of_day = 'morning' THEN pm10 END),
	AVG(CASE WHEN period_of_day = 'afternoon' THEN pm10 END),
	AVG(CASE WHEN period_of_day = 'evening' THEN pm10 END),
	AVG(CASE WHEN period_of_day = 'night' THEN pm10 END),
	MAX(pm10),
	SUM(flag_oms_pm10_exceeded),
	SUM(flag_fr_pm10_exceeded),

	FROM hourly_yesterday_pm_flag

	GROUP BY city_name, date;
