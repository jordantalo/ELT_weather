import os
import duckdb
from langchain_ollama import ChatOllama
from langchain_core.prompts import PromptTemplate
from src.config import DB_PATH

def ask_weather_agent(question: str) -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    llm = ChatOllama(model="llama3.2:3b", temperature=0, base_url=base_url)

    # 1. Prompt pour générer UNIQUEMENT du SQL
    sql_prompt = PromptTemplate.from_template("""
Tu es un expert DuckDB. Génère UNE SEULE requête SQL valide pour répondre à la question.

Table: fct_insert_normals
Colonnes principales: city (ex: 'newyork'), date, temp_morning, temp_afternoon, temp_evening

Règles:
- Recherche de ville: utilise toujours `ILIKE '%<ville>%'`
- Ne renvoie RIEN d'autre que la requête SQL (pas de Markdown, pas de commentaires).

Question: {question}
SQL:""")

    # Génération du SQL par le LLM
    sql_query = llm.invoke(sql_prompt.format(question=question)).content.strip()

    # Nettoyage si le modèle entoure de ```sql ... ```
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    # 2. Exécution directe dans DuckDB via Python (Sécurisé et rapide)
    try:
        con = duckdb.connect(DB_PATH)
        df_result = con.execute(sql_query).df()
        con.close()

        if df_result.empty:
            return "Désolé, aucune donnée ne correspond à cette recherche."

        data_str = df_result.to_string(index=False)
    except Exception as e:
        return f"Erreur lors de l'exécution de la requête : {e}"

    # 3. Prompt pour la réponse finale en français
    final_prompt = PromptTemplate.from_template("""
En te basant uniquement sur ces données météo :
{data}

Réponds de façon synthétique et naturelle à la question suivante en français.
Question: {question}
Réponse:""")

    return llm.invoke(final_prompt.format(data=data_str, question=question)).content.strip()
