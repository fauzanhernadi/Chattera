import os
from dotenv import load_dotenv
import streamlit as st
from groq import Groq

# Load environment variables from .env file
load_dotenv()
GROQ_API_KEY = os.getenv("llama_api_key")

# Streamlit page configuration
st.set_page_config(
    page_title="LLAMA 3.1 Chat",
    page_icon="🦙",
    layout="centered"
)

# Check if API key is loaded successfully
if not GROQ_API_KEY:
    st.error("GROQ API Key is missing. Please check your .env file.")
else:
    # Initialize Groq client with the API key
    client = Groq(api_key=GROQ_API_KEY)

    # Initialize chat history in session state if not present already
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # Streamlit page title
    st.title("🦙 LLAMA 3.1 ChatBot")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Input field for user's message
    user_prompt = st.chat_input("Ask LLAMA...")

    if user_prompt:
        # Display user message and add it to session history
        st.chat_message("user").markdown(user_prompt)
        st.session_state.chat_history.append({"role": "user", "content": user_prompt})

        # Prepare messages for model input
        messages = [
            {"role": "system", "content": "You are a helpful assistant"},
            *st.session_state.chat_history
        ]

        # Send user's message to the LLM and get a response
        response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=messages
        )

        assistant_response = response.choices[0].message.content
        st.session_state.chat_history.append({"role": "assistant", "content": assistant_response})

        # Display the LLM's response
        with st.chat_message("assistant"):
            st.markdown(assistant_response)
