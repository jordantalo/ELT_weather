COPY (
	SELECT *
	FROM gold_daily_city_metrics
	WHERE city_name = 'Paris'
	ORDER BY date DESC
)
TO 'data/debug_exports/gold_paris_check.csv'
(HEADER, DELIMITER ',');
