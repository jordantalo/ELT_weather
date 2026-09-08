#!/bin/bash
set -e

echo "=== Initialisation de la base de métadonnées Airflow ==="
airflow db init

echo "=== Création de l'utilisateur Admin ==="
airflow users create \
	--username "${AIRFLOW_ADMIN_USER:-admin}" \
	--password "${AIRFLOW_ADMIN_PASSWORD:-admin}" \
	--firstname Data \
	--lastname Engineer \
	--email admin@example.com \
	--role Admin || true

echo "=== Démarrage de l'interface Streamlit (Port 8501) ==="
streamlit run src/app.py --server.address=0.0.0.0 --server.port=8501 &

echo "=== Démarrage d'Airflow Standalone ==="
exec airflow standalone
