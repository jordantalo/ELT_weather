WITH daily_temp_prepared AS (
	SELECT
		CAST(weather_timestamp AS DATE) AS date,
		city_name,

		AVG (CASE WHEN HOUR(weather_timestamp) BETWEEN 6 AND 11 THEN temperature_celsius END) AS temp_morning,
		AVG (CASE WHEN HOUR(weather_timestamp) BETWEEN 12 AND 17 THEN temperature_celsius END) AS temp_afternoon,
		AVG (CASE WHEN HOUR(weather_timestamp) BETWEEN 18 AND 22 THEN temperature_celsius END) AS temp_evening,
		AVG (CASE WHEN HOUR(weather_timestamp) BETWEEN 23 AND 5 THEN temperature_celsius END) AS temp_night,

	FROM silver_weather

	GROUP BY city_name, CAST(weather_timestamp AS DATE)
),

rolling_metrics AS (
	SELECT
		AVG(temp_morning) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS r30_morning,
		AVG(temp_afternoon) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS r30_afternoon,
		AVG(temp_evening) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS r30_evening,
		AVG(temp_night) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 30 PRECEDING AND 1 PRECEDING) AS r30_night,

		AVG(temp_morning) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS r7_morning,
		AVG(temp_afternoon) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS r7_afternoon,
		AVG(temp_evening) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS r7_evening,
		AVG(temp_night) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 7 PRECEDING AND 1 PRECEDING) AS r7_night,

		AVG(temp_morning) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 1 FOLLOWING AND 5 FOLLOWING) AS f5_morning,
		AVG(temp_afternoon) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 1 FOLLOWING AND 5 FOLLOWING) AS f5_afternoon,
		AVG(temp_evening) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 1 FOLLOWING AND 5 FOLLOWING) AS f5_evening,
		AVG(temp_night) OVER (PARTITION BY city_name ORDER BY date ROWS BETWEEN 1 FOLLOWING AND 5 FOLLOWING) AS f5_night,

	FROM daily_temp_prepared
),

UPDATE gold_daily_city_metrics
SET
	temp_morning_avg_forecast_5d = rm.f5_morning,
	temp_afternoon_avg_forecast_5d = rm.f5_afternoon,
	temp_evening_avg_forecast_5d = rm.f5_evening,
	temp_night_avg_forecast_5d = rm.f5_night,

	temp_morning_avg_rolling_7d = rm.r7_morning,
	temp_afternoon_avg_rolling_7d = rm.r7_afternoon,
	temp_evening_avg_rolling_7d = rm.r7_evening,
	temp_night_avg_rolling_7d = rm.r7_night,

	temp_morning_avg_rolling_30d = rm.r30_morning,
	temp_afternoon_avg_rolling_30d = rm.r30_afternoon,
	temp_evening_avg_rolling_30d = rm.r30_evening,
	temp_night_avg_rolling_30d = rm.r30_night,

FROM rolling_metrics rm

WHERE
	gold_daily_city_metrics.city_name = rm.city_name
	AND gold_daily_city_metrics.date = rm.date
	AND gold_daily_city_metrics.date = CURRENT_DATE - INTERVAL '1 day';
