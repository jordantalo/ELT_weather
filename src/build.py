import duckdb
from pathlib import Path

CURRENT_FILE = Path(__file__).resolve()
PROJECT_ROOT = CURRENT_FILE.parent.parent
DB_PATH = PROJECT_ROOT / "data" / "weather_warehouse.duckdb"

def build_gold_tables():
	print("[Gold] Starting Gold layer transformation...")

	connection = duckdb.connect(str(DB_PATH))

	connection.execute("""
		CREATE TABLE IF NOT EXISTS gold_daily_city_metrics (
			city_name VARCHAR,
			date DATE,

			temp_morning_avg_today DOUBLE,
			temp_afternoon_avg_today DOUBLE,
			temp_evening_avg_today DOUBLE,
			temp_night_avg_today DOUBLE,
			temp_max_today DOUBLE,
			temp_min_today DOUBLE,

			temp_morning_avg_forecast_5d DOUBLE,
			temp_afternoon_avg_forecast_5d DOUBLE,
			temp_evening_avg_forecast_5d DOUBLE,
			temp_night_avg_forecast_5d DOUBLE,

			temp_max_forecast_5d DOUBLE,
			temp_min_forecast_5d DOUBLE,

			pm2_5_day_avg DOUBLE,
			pm2_5_day_max DOUBLE,
			pm2_5_hours_above_threshold INT,
			pm10_day_avg DOUBLE,
			pm10_day_max DOUBLE,
			pm10_hours_above_threshold INT,

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

			PRIMARY KEY (city_name, date)
		);
	""")

	query = """

		WITH
			hourly_prepared AS (
				SELECT
					weather_timestamp,
					city_name,
					pm2_5,
					pm10,
					temperature_celsius,

				CASE
					WHEN HOUR(weather_timestamp BETWEEN 6 AND 11) THEN 'morning'
					WHEN HOUR(weather_timestamp BETWEEN 12 AND 17) THEN 'afternoon'
					WHEN HOUR(weather_timestamp BETWEEN 18 AND 22) THEN 'evening'
					ELSE 'night'
					END AS period_of_day

				FROM silver_weather

				WHERE CAST(weather_timestamp AS DATE) = CURRENT_DATE - INTERVAL '1 day'
			),

			hourly_yesterday_pm_flag AS (
			 	SELECT
					weather_timestamp,
					period_of_day,
					city_name,
					pm2_5,
					pm10,

				CAST(weather_timestamp AS DATE) AS date

				CASE
					WHEN pm2_5 > 15 THEN 1 ELSE 0 END AS flag_oms_pm25_exceeded

				CASE
					WHEN pm2_5 > 50 THEN 1 ELSE 0 END AS flag_fr_pm25_exceeded

				CASE
					WHEN pm10 > 45 THEN 1 ELSE 0 END AS flag_oms_pm10_exceeded

				CASE
					WHEN pm10 > 50 THEN 1 ELSE 0 END AS flag_fr_pm10_exceeded

				FROM hourly_prepared
			 ),

			daily_avg_pm AS (
				SELECT
					city_name,
					date,

				AVG(pm2_5) AS pm2_5_avg_j1,
				AVG(pm10) AS pm10_avg_j1,

				MAX(pm2_5) AS pm2_5_max_j1,
				MAX(pm10) AS pm10_max_j1,

				SUM(flag_oms_pm25_exceeded) AS hours_pm25_exceeded_oms_j1,
				SUM(flag_oms_pm10_exceeded) AS hours_pm10_exceeded_oms_j1,
				SUM(flag_fr_pm25_exceeded) AS hours_pm25_exceeded_fr_j1,
				SUM(flag_fr_pm25_exceeded) AS hours_pm25_exceeded_fr_j1,

				AVG(CASE WHEN period_of_day = 'morning' THEN pm2_5 END) AS pm2_5_morning_avg,
				AVG(CASE WHEN period_of_day = 'afternoon' THEN pm2_5 END) AS pm2_5_afternoon_avg,
				AVG(CASE WHEN period_of_day = 'evening' THEN pm2_5 END) AS pm2_5_evening_avg,
				AVG(CASE WHEN period_of_day = 'night' THEN pm2_5 END) AS pm2_5_night_avg,

				AVG(CASE WHEN period_of_day = 'morning' THEN pm10 END) AS pm10_morning_avg,
				AVG(CASE WHEN period_of_day = 'afternoon' THEN pm10 END) AS pm10_afternoon_avg,
				AVG(CASE WHEN period_of_day = 'evening' THEN pm10 END) AS pm10_evening_avg,
				AVG(CASE WHEN period_of_day = 'night' THEN pm10 END) AS pm10_night_avg

				FROM hourly_yesterday_pm_flag

				GROUP BY city_name, date
			)
	"""
	df = connection.execute(query).df()
	print("\n--- Aperçu des données calculées (Pandas DataFrame) ---")
	print(df)

	connection.close()


if __name__ == "__main__":
    build_gold_tables()
