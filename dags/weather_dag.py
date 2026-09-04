from datetime import datetime, timedelta
import os
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

DBT_PROJECT_DIR = "/workspaces/weather/weather_dbt"

default_args = {
	'owner': 'jordan',
	'depend_on_past': False,
	'retries': 2,
	'retry_delay': timedelta(minutes=60)
}

with DAG(
	dag_id='weather_pipeline',
	default_args=default_args,
	description='Daily pipeline: openMeteo API -> dbt / DuckDB (incremental tables)',
	schedule_interval='0 6 * * *',
	start_date=datetime(2026, 1, 1),
	catchup=False,
	tags=['weather', 'dbt', 'duckdb'],
) as dag:

	extract_task = BashOperator(
		task_id='extract_temp_data_api',
		bash_command='python3 /workspaces/weather/main.py',
	)

	dbt_transform_task = BashOperator(
		task_id='dbt_run_models',
		bash_command=f'cd {DBT_PROJECT_DIR} && dbt run --profiles-dir .',
	)

	extract_task >> dbt_transform_task
