COPY (
	SELECT *
	FROM ref_climate_normals
	WHERE city_name = 'Paris'
	ORDER BY day_of_year DESC
)
TO 'data/debug_exports/normals_paris_check.csv'
(HEADER, DELIMITER ',');
