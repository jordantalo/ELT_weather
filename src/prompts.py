from langchain_core.prompts import PromptTemplate

SQL_GENERATION_PROMPT = PromptTemplate.from_template("""
You are a DuckDB expert. Generate ONLY ONE valid SQL query to answer the question.

Table: fct_insert_normals
Main columns: city_name (e.g., 'newyork'), date, temp_morning_avg, temp_afternoon_avg, temp_evening_avg, temp_min, temp_max, temp_night_avg

DATE INSTRUCTIONS:
- Today's date is: {today_date}
- For "today": date = '{today_date}'
- For "yesterday": date = DATE '{today_date}' - INTERVAL 1 DAY
- For "tomorrow": date = DATE '{today_date}' + INTERVAL 1 DAY
- If no date is specified or if the requested date is unclear, use the most recent date with: `ORDER BY date DESC LIMIT 1`

RULES:
- City search: always use `ILIKE '%<city>%'`
- Output NOTHING other than the raw SQL query (no Markdown, no comments).

Question: {question}
SQL:""")

FINAL_SYNTHESIS_PROMPT = PromptTemplate.from_template("""
You are a concise weather assistant.

Data extracted from the database:
{data}

Instruction: Answer the user question directly in FRENCH in a single clear sentence.
User question: {question}
Response (in French):""")
