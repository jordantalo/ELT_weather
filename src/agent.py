from langchain_community.utilities import SQLDatabase
from langchain_community.agent_toolkits import create_sql_agent
from langchain_ollama import ChatOllama
from src.config import DB_PATH

def ask_weather_agent(question: str) -> str:

	db = SQLDatabase.from_uri(
		f"duckdb:///{DB_PATH}",
		include_tables=["fct_insert_normals"]
	)

	llm = ChatOllama(
		model="qwen2.5-coder:1.5b",
		temperature=0,
		base_url="http://host.docker.internal:11434"
	)

	agent_executor = create_sql_agent(
		llm=llm,
		db=db,
		agent_type="tool-calling",
		verbose=True
	)

	response = agent_executor.invoke({"input": question})
	return response["output"]
