import sqlite3
import os
# Connect to the database (or create it if it doesn't exist)
db_path = os.path.abspath('db/helpdesk_assistant.db')  # Get absolute path
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Execute the CREATE TABLE statement
cursor.execute('''
CREATE TABLE sessions (
    session_id TEXT,
    title TEXT ,
    create_ts TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    chat_history TEXT
);
''')


cursor.execute('''
CREATE TABLE chat_update (
    intent TEXT,
    summary TEXT,
    sentiment INTEGER ,
    suggestion TEXT,
    status TEXT,
    time TIMESTAMP
);
''')

cursor.execute('''
CREATE TABLE conv (
    conversation TEXT,
    time TIMESTAMP
);
''')
print("Tables created successfully!")
# Commit the changes and close the connection
conn.commit()
conn.close()

