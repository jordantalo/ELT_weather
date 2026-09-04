{{
	config (
		materialized='incremental',
		unique_key=['city_name', 'weather_timestamp'],
		incremental_strategy='merge'
	)
}}

WITH raw_data AS (
	SELECT
		city AS city_name,
		unnest(weather.time)::TIMESTAMP AS weather_timestamp,
		unnest(weather.temperature_2m)::DOUBLE AS temperature_celsius,
		unnest(air_quality.pm10)::DOUBLE AS pm10,
		unnest(air_quality.pm2_5)::DOUBLE AS pm2_5,
		current_timestamp AS ingested_at_utc,
		timezone('Europe/Paris', current_timestamp) AS ingested_at_fr,
		filename
	FROM read_json_auto('{{ env_var("DAILY_DIR") }}/*.json', filename = true)

	{% if is_incremental() %}

		WHERE filename = (
			SELECT filename
			FROM read_json_auto('{{ env_var("DAILY_DIR") }}/*.json', filename = true)
			ORDER BY extracted_at DESC
			LIMIT 1
		)

	{% endif %}
)

SELECT * FROM raw_data
