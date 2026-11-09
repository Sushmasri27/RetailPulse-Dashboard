import streamlit as st


def show_about_page():

    st.title("About")

    st.markdown("""
## Dynamic AI Chatbot

### Features

- 🤖 Local Llama 3.2 AI
- 💬 ChatGPT-style Interface
- 😊 Sentiment Analysis
- 💾 SQLite Database
- 📊 Analytics Dashboard
- 📄 Document Assistant
- ⚡ Streaming AI Responses

### Technologies

- Python
- Streamlit
- Ollama
- Llama 3.2
- SQLite
- Plotly
- TextBlob
""")