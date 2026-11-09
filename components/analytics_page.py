import streamlit as st
import plotly.express as px

from analytics import get_chat_data


def show_analytics_page():

    st.title("📊 Analytics Dashboard")

    df = get_chat_data()

    if df.empty:
        st.warning("No chat history available.")
        return

    total = len(df)
    positive = (df["sentiment"] == "Positive").sum()
    neutral = (df["sentiment"] == "Neutral").sum()
    negative = (df["sentiment"] == "Negative").sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("💬 Total Chats", total)
    c2.metric("😊 Positive", positive)
    c3.metric("😐 Neutral", neutral)
    c4.metric("😞 Negative", negative)

    st.divider()

    sentiment_counts = (
        df["sentiment"]
        .value_counts()
        .reset_index()
    )

    sentiment_counts.columns = [
        "Sentiment",
        "Count"
    ]

    fig1 = px.pie(
        sentiment_counts,
        names="Sentiment",
        values="Count",
        title="Sentiment Distribution"
    )

    st.plotly_chart(fig1, use_container_width=True)

    fig2 = px.bar(
        sentiment_counts,
        x="Sentiment",
        y="Count",
        title="Sentiment Count"
    )

    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Recent Chats")

    st.dataframe(
        df[
            [
                "user_message",
                "sentiment",
                "timestamp"
            ]
        ],
        use_container_width=True
    )