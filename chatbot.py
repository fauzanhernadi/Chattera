import streamlit as st
import pandas as pd
from PyPDF2 import PdfReader
from langchain_openai.chat_models import ChatOpenAI

# Set up the app title
st.title("Chattera")

# Placeholder for OpenAI API key
openai_api_key = ''

# Initialize response history in session state to store all responses persistently
if "response_history" not in st.session_state:
    st.session_state.response_history = []

# Function to generate response from input text
def generate_response(input_text):
    model = ChatOpenAI(temperature=0.7, api_key=openai_api_key)
    response = model.invoke(input_text)
    response_text = response.content
    # Append new response to response history
    st.session_state.response_history.append(response_text)
    st.write(response_text)

# Function to load and process a CSV file
def process_csv(file):
    try:
        df = pd.read_csv(file)
        return df.to_string()
    except Exception as e:
        st.error(f"Error reading CSV: {e}")
        return ""

# Function to load and process a PDF file
def process_pdf(file):
    try:
        pdf_reader = PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
        return text
    except Exception as e:
        st.error(f"Error reading PDF: {e}")
        return ""

# File uploader
uploaded_file = st.file_uploader("Upload a CSV or PDF file", type=["csv", "pdf"])

# Text area input form
with st.form("my_form"):
    text = st.text_area("Enter text:", "What are the three key pieces of advice for learning how to code?")
    submitted = st.form_submit_button("Submit")

    # Check if API key is valid
    if not openai_api_key.startswith("sk-"):
        st.warning("Please enter your OpenAI API key!", icon="⚠")

    # Process text input or file content on form submission
    if submitted and openai_api_key.startswith("sk-"):
        if uploaded_file is not None:
            file_extension = uploaded_file.name.split(".")[-1].lower()
            if file_extension == "csv":
                file_text = process_csv(uploaded_file)
            elif file_extension == "pdf":
                file_text = process_pdf(uploaded_file)
            else:
                file_text = ""

            if file_text:
                generate_response(file_text)
        else:
            # Generate response from direct text input
            generate_response(text)

# Display all previous responses directly in sequence
for past_response in st.session_state.response_history:
    st.write(past_response)
