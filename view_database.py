import sqlite3

conn = sqlite3.connect("chatbot.db")
cursor = conn.cursor()

# Show all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("\n===== TABLES IN DATABASE =====")
for table in tables:
    print(table[0])

# Display data from each table
for table in tables:
    table_name = table[0]

    print(f"\n===== {table_name.upper()} =====")

    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()

        if rows:
            for row in rows:
                print(row)
        else:
            print("No records found.")

    except Exception as e:
        print("Error:", e)

conn.close()