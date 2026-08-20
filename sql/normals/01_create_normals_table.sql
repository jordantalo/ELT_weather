CREATE TABLE IF NOT EXISTS ref_climate_normals (
	city_name VARCHAR,
	day_of_year VARCHAR,
	normal_temp_avg_morning DOUBLE,
	normal_temp_avg_afternoon DOUBLE,
	normal_temp_avg_evening DOUBLE,
	normal_temp_avg_night DOUBLE,

	PRIMARY KEY (city_name, day_of_year)
);
