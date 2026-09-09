import os
import duckdb
from datetime import datetime
from langchain_ollama import ChatOllama

from src.config import DB_PATH
from src.prompts import SQL_GENERATION_PROMPT, FINAL_SYNTHESIS_PROMPT

def ask_weather_agent(question: str) -> str:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://ollama:11434")
    llm = ChatOllama(model="llama3.2:3b", temperature=0, base_url=base_url)

    today_str = datetime.now().strftime('%Y-%m-%d')

    prompt_formatted = SQL_GENERATION_PROMPT.format(
        question=question,
        today_date=today_str
    )
    sql_query = llm.invoke(prompt_formatted).content.strip()
    sql_query = sql_query.replace("```sql", "").replace("```", "").strip()

    try:
        with duckdb.connect(DB_PATH) as con:
            df_result = con.execute(sql_query).df()

        if df_result.empty:
            return "Désolé, aucune donnée ne correspond à cette recherche."

        data_str = df_result.to_string(index=False)
    except Exception as e:
        return f"Erreur lors de l'exécution SQL : {e}"

    final_prompt = FINAL_SYNTHESIS_PROMPT.format(
        data=data_str,
        question=question
    )

    return llm.invoke(final_prompt).content.strip()
