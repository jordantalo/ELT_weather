import streamlit as st
from src.agent import ask_weather_agent

st.title("Weather AI Assistant")

user_question = st.text_input("Your meteo question :")

if user_question:
	st.write(f"**Question:** {user_question}")

	with st.spinner("Agent is analysing our database..."):
		ai_response = ask_weather_agent(user_question)

	st.write(f"**Response:** {ai_response}")
