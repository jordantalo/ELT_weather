UPDATE gold_daily_city_metrics
SET
	temp_gap_with_normals_morning = gold_daily_city_metrics.temp_morning_avg_j1 - normals.normal_temp_avg_morning,
	temp_gap_with_normals_afternoon = gold_daily_city_metrics.temp_afternoon_avg_j1 - normals.normal_temp_avg_afternoon,
	temp_gap_with_normals_evening = gold_daily_city_metrics.temp_evening_avg_j1 - normals.normal_temp_avg_evening,
	temp_gap_with_normals_night = gold_daily_city_metrics.temp_night_avg_j1 - normals.normal_temp_avg_night,

FROM ref_climate_normals normals

WHERE
	gold_daily_city_metrics.city_name = normals.city_name
	AND STRFTIME(gold_daily_city_metrics.date, '%m-%d') = normals.day_of_year
	AND gold_daily_city_metrics.date = CURRENT_DATE - INTERVAL '1 day';
