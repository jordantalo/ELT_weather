CREATE TABLE IF NOT EXISTS gold_daily_city_metrics (
	city_name VARCHAR,
	date DATE,

	temp_morning_avg_j1 DOUBLE,
	temp_afternoon_avg_j1 DOUBLE,
	temp_evening_avg_j1 DOUBLE,
	temp_night_avg_j1 DOUBLE,
	temp_max_j1 DOUBLE,
	temp_min_j1 DOUBLE,

	temp_morning_avg_forecast_5d DOUBLE,
	temp_afternoon_avg_forecast_5d DOUBLE,
	temp_evening_avg_forecast_5d DOUBLE,
	temp_night_avg_forecast_5d DOUBLE,

	temp_morning_avg_rolling_7d DOUBLE,
	temp_afternoon_avg_rolling_7d DOUBLE,
	temp_evening_avg_rolling_7d DOUBLE,
	temp_night_avg_rolling_7d DOUBLE,

	temp_morning_avg_rolling_30d DOUBLE,
	temp_afternoon_avg_rolling_30d DOUBLE,
	temp_evening_avg_rolling_30d DOUBLE,
	temp_night_avg_rolling_30d DOUBLE,

	temp_gap_with_normals_morning DOUBLE,
	temp_gap_with_normals_afternoon DOUBLE,
	temp_gap_with_normals_evening DOUBLE,
	temp_gap_with_normals_night DOUBLE,

	pm2_5_avg_j1 DOUBLE,
	pm2_5_morning_avg DOUBLE,
	pm2_5_afternoon_avg DOUBLE,
	pm2_5_evening_avg DOUBLE,
	pm2_5_night_avg DOUBLE,

	pm2_5_max_j1 DOUBLE,
	hours_pm2_5_exceeded_oms_j1 INT,
	hours_pm2_5_exceeded_fr_j1 INT,

	pm10_avg_j1 DOUBLE,
	pm10_morning_avg DOUBLE,
	pm10_afternoon_avg DOUBLE,
	pm10_evening_avg DOUBLE,
	pm10_night_avg DOUBLE,

	pm10_max_j1 DOUBLE,
	hours_pm10_exceeded_oms_j1 INT,
	hours_pm10_exceeded_fr_j1 INT,

	PRIMARY KEY (city_name, date)
);
