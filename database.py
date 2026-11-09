import sqlite3

DB_NAME = "chatbot.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def create_database():

    conn = get_connection()
    cursor = conn.cursor()

    # ---------------- Conversations ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS conversations(

        conversation_id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT DEFAULT 'New Chat',

        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

    )
    """)

    # ---------------- Messages ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS messages(

        message_id INTEGER PRIMARY KEY AUTOINCREMENT,

        conversation_id INTEGER,

        role TEXT,

        message TEXT,

        sentiment TEXT,

        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(conversation_id)
        REFERENCES conversations(conversation_id)

    )
    """)

    # ---------------- Documents ----------------

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents(

        document_id INTEGER PRIMARY KEY AUTOINCREMENT,

        conversation_id INTEGER,

        file_name TEXT,

        file_path TEXT,

        uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

        FOREIGN KEY(conversation_id)
        REFERENCES conversations(conversation_id)

    )
    """)

    conn.commit()
    conn.close()


# ----------------------------------------------------
# Conversation Functions
# ----------------------------------------------------

def create_new_conversation(title="New Chat"):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO conversations(title) VALUES(?)",
        (title,)
    )

    conn.commit()

    conversation_id = cursor.lastrowid

    conn.close()

    return conversation_id
def update_conversation_title(conversation_id, title):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE conversations
        SET title = ?
        WHERE conversation_id = ?
    """, (title, conversation_id))

    conn.commit()
    conn.close()
def rename_conversation(conversation_id, new_title):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE conversations
        SET title = ?
        WHERE conversation_id = ?
        """,
        (new_title, conversation_id)
    )

    conn.commit()
    conn.close()


def delete_conversation(conversation_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM messages WHERE conversation_id=?",
        (conversation_id,)
    )

    cursor.execute(
        "DELETE FROM documents WHERE conversation_id=?",
        (conversation_id,)
    )

    cursor.execute(
        "DELETE FROM conversations WHERE conversation_id=?",
        (conversation_id,)
    )

    conn.commit()
    conn.close()


def get_all_conversations():

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT conversation_id,title,created_at

        FROM conversations

        ORDER BY created_at DESC

    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


# ----------------------------------------------------
# Message Functions
# ----------------------------------------------------

def save_message(conversation_id, role, message, sentiment=None):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        INSERT INTO messages(

        conversation_id,

        role,

        message,

        sentiment)

        VALUES(?,?,?,?)

    """, (

        conversation_id,

        role,

        message,

        sentiment

    ))

    conn.commit()

    conn.close()


def load_messages(conversation_id):

    conn = get_connection()

    cursor = conn.cursor()

    cursor.execute("""

        SELECT role,message

        FROM messages

        WHERE conversation_id=?

        ORDER BY timestamp

    """,(conversation_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows


# ----------------------------------------------------
# Documents
# ----------------------------------------------------

def save_document(conversation_id,file_name,file_path):

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""

    INSERT INTO documents(

    conversation_id,

    file_name,

    file_path)

    VALUES(?,?,?)

    """,(conversation_id,file_name,file_path))

    conn.commit()

    conn.close()


def get_documents(conversation_id):

    conn=get_connection()

    cursor=conn.cursor()

    cursor.execute("""

    SELECT file_name,file_path

    FROM documents

    WHERE conversation_id=?

    """,(conversation_id,))

    docs=cursor.fetchall()

    conn.close()

    return docs


if __name__ == "__main__":

    create_database()

    print("Database Created Successfully")