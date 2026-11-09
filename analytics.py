import sqlite3
import pandas as pd

DB_NAME = "chatbot.db"


def get_chat_data():
    conn = sqlite3.connect(DB_NAME)

    query = """
    SELECT
        message AS user_message,
        sentiment,
        timestamp
    FROM messages
    WHERE role = 'user'
    ORDER BY timestamp DESC
    """

    df = pd.read_sql_query(query, conn)

    conn.close()

    return df