import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu

from chatbot import get_response, stream_response
from sentiment import analyze_sentiment
from database import (
    create_new_conversation,
    save_message,
    get_all_conversations,
    load_messages,
    update_conversation_title
)
from analytics import get_chat_data
from components.sidebar import show_sidebar
from components.chat_page import show_chat_page
from components.sidebar import show_sidebar
from components.chat_page import show_chat_page
from components.analytics_page import show_analytics_page
from components.document_page import show_document_page
from components.about_page import show_about_page
# ---------------- CSS ----------------

def load_css():
    with open("assets/style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ---------------- Page Config ----------------

st.set_page_config(
    page_title="Dynamic AI Chatbot",
    page_icon="🤖",
    layout="wide"
)

load_css()

# ---------------- Session State ----------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = create_new_conversation()

# ---------------- Sidebar ----------------

from components.sidebar import show_sidebar

page = show_sidebar()

# ==========================================================
# CHAT
# ==========================================================

if page == "Chat":
    show_chat_page()
# ==========================================================
# ANALYTICS
# ==========================================================

elif page == "Analytics":
    show_analytics_page()

# ==========================================================
# DOCUMENT ASSISTANT
# ==========================================================

elif page == "Document Assistant":
    show_document_page()

# ==========================================================
# ABOUT
# ==========================================================

else:
    show_about_page()
