COPY (
	SELECT *
	FROM silver_weather
	WHERE city_name = 'Paris'
	ORDER BY weather_timestamp DESC
)
TO 'data/debug_exports/silver_paris_metrics.csv'
(HEADER, DELIMITER ',');
