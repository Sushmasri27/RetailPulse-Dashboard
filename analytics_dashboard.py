import streamlit as st
import plotly.express as px
from analytics import get_chat_data

st.set_page_config(
    page_title="Analytics Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Chatbot Analytics Dashboard")

df = get_chat_data()

if df.empty:
    st.warning("No chat data available.")
    st.stop()

# ---------------- KPI Cards ----------------

total_chats = len(df)
positive = (df["sentiment"] == "Positive").sum()
negative = (df["sentiment"] == "Negative").sum()
neutral = (df["sentiment"] == "Neutral").sum()

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric("💬 Total Chats", total_chats)

with c2:
    st.metric("😊 Positive", positive)

with c3:
    st.metric("😐 Neutral", neutral)

with c4:
    st.metric("😞 Negative", negative)

st.divider()

# ---------------- Pie Chart ----------------

sentiment_counts = df["sentiment"].value_counts().reset_index()
sentiment_counts.columns = ["Sentiment", "Count"]

fig1 = px.pie(
    sentiment_counts,
    names="Sentiment",
    values="Count",
    title="Sentiment Distribution"
)

st.plotly_chart(fig1, use_container_width=True)

# ---------------- Bar Chart ----------------

fig2 = px.bar(
    sentiment_counts,
    x="Sentiment",
    y="Count",
    title="Sentiment Count"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- Recent Chats ----------------

st.subheader("Recent Chats")

st.dataframe(
    df[["user_message", "sentiment", "timestamp"]],
    use_container_width=True
)