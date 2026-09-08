#!/bin/bash
set -e

echo "Vérification de la connexion à Ollama..."
until curl -s http://ollama:11434/api/tags > /dev/null; do
    echo "En attente du service Ollama..."
    sleep 2
done

echo "Installation/Vérification du modèle LLM..."
curl -s -X POST http://ollama:11434/api/pull -d '{"name": "llama3.2:3b", "stream": false}' > /dev/null

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
