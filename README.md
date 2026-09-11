# End-to-End Weather Analytics & Local AI Pipeline

## Project Overview

This project is a fully containerized, locally executable weather data processing and natural language querying platform. Its primary goal is to demonstrate a robust, resource-efficient, and modern Data & AI pipeline.

## Supported Scope & Data
* **Current Cities**: New York, Paris, London, and Tokyo.
* **Extensibility**: Additional cities can easily be tracked by updating the configuration file at `src/config.py`.
* **AI Capabilities**: The Text-to-SQL assistant is designed to handle **focused, single-turn natural language questions** regarding weather metrics (e.g., *"What was the temperature in New York yesterday morning?"*).

### Pipeline Architecture
1. **Ingestion (Airflow & Open-Meteo)**: Automated daily weather data extraction from the Open-Meteo API, storing raw payloads as JSON files (*Data Lake / Bronze Layer*).
2. **Transformation & Data Quality (dbt & DuckDB)**:
   - **Silver Table**: Ingestion and parsing of raw JSON files. Data is processed **incrementally with deduplication** logic to guarantee pipeline idempotency.
   - **Gold Table**: Aggregation of key performance metrics (morning, afternoon, evening, min, and max average temperatures) optimized for analytical queries.
3. **Local LLM Interface (Ollama & LangChain)**:
   - A **deterministic Text-to-SQL system** querying the Gold table directly in response to natural language inputs.
   - Powered by a local `llama3.2:3b` model running via Ollama, removing any dependency on external paid APIs.
4. **User Interface (Streamlit)**: Interactive dashboard allowing users to query weather metrics in plain language and receive concise synthesized answers.

## 🛠️ Key Engineering Decisions

* **Deterministic Text-to-SQL vs. Autonomous Agents**: Replaced open-ended ReAct agent loops with a structured Text-to-SQL execution chain. This eliminates infinite reasoning loops on small parameters models (3B) and guarantees sub-second execution.
* **DuckDB for OLAP**: Used DuckDB for fast, serverless, column-oriented analytical querying directly on top of local transformations.
* **Separation of Concerns**: System prompts (`src/prompts.py`) and core agent logic (`src/agent.py`) are strictly decoupled for better maintainability and testing.

---

## Getting Started

### Prerequisites
* Docker and Docker Compose installed on your system.

### Quick Start

1. Clone the repository and navigate to the project root directory.
2. Run the build and startup command:
   make re

This command builds the Docker containers, initializes the DuckDB instance, and spins up all microservices (Airflow, Ollama, Streamlit).

### Service Access & Exploration

* **Apache Airflow**: `http://localhost:8080` (Default credentials: `airflow` / `airflow`)
  * Triggers and monitors the extraction and transformation DAGs.
* **Streamlit UI**: `http://localhost:8501`
  * Interface for submitting natural language queries to the weather database.
* **dbt Lineage & Table Documentation**:
  * You can inspect model lineage and column-level metadata directly using dbt CLI commands inside the container:
    ```bash
    dbt docs generate
    dbt docs serve --port 8081
    ```

> **Important Note**: To query the assistant via Streamlit, the Airflow pipeline must be executed at least once to populate the DuckDB Gold table with initial data.

---

## 📚 Resources & References

* [dbt Documentation](https://docs.getdbt.com/)
* [Apache Airflow Documentation](https://airflow.apache.org/docs/)
* [DuckDB Documentation](https://duckdb.org/docs/)
* [SQL Learning & Analytics Guide (Mode)](https://mode.com/sql-tutorial/)

---

## 🤖 AI Usage Disclosure

Artificial Intelligence was leveraged across two core aspects of this repository:

1. **In-App Inference**: Deployment of the `llama3.2:3b` model hosted locally through Ollama to translate incoming user queries into valid DuckDB SQL queries.
2. **Development Assistance**: Used an AI coding assistant as a pair-programming resource to optimize Docker Compose configurations, refine the Text-to-SQL architecture, and enforce code modularity (`prompts.py` / `agent.py`).
