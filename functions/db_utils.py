import sqlite3
import os
import datetime

def update_session_table(session_id,session_ts,title,chat_history):
    """Function block to update DB for session details"""
    db_path = os.path.abspath('db/helpdesk_assistant.db')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()  # Create a cursor object

        sessions=[]
        cursor.execute("SELECT session_id FROM sessions")
        rows = cursor.fetchall()
        for row in rows:
            sessions.append(row[0])
        # SQL INSERT statement
        if str(session_id) in sessions:
            query = """
            UPDATE sessions
            SET title = ?,chat_history= ?
            WHERE session_id = ?
            """

            # Execute the UPDATE statement with parameters
            cursor.execute(query, (title, chat_history, str(session_id)))

            print(f"Session:{session_id} updated successfully!")
            
        else:
            query = """
            INSERT INTO sessions (session_id,title,create_ts,chat_history)
            VALUES (?, ?,?,?)
            """

            # Execute the INSERT statement with parameters
            cursor.execute(query, (str(session_id),title,session_ts,str(chat_history)))

        # Commit the changes
        conn.commit()

        print("Data inserted successfully!")

        # (Optional) Retrieve the last inserted row's ID
        last_row_id = cursor.lastrowid
        print(f"Last inserted row ID: {last_row_id}")

    except sqlite3.Error as e:
        print(f"Database error: {e}")

def update_conv_and_fetch(conv):
    db_path = os.path.abspath('db/helpdesk_assistant.db')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()  # Create a cursor object

        #one more query to select and retrieve title and create_ts

        ts=datetime.datetime.now()
        # SQL INSERT statement
        query = """
        INSERT INTO conv (conversation,time)
        VALUES (?,?)
        """
        # Execute the INSERT statement with parameters
        cursor.execute(query, (conv,ts))
        print("Values updated succesfully in conv table")
        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    full_conv=""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT conversation FROM conv order by time;")
        rows = cursor.fetchall()
        print(type(rows))

        for row in rows:
            full_conv+= row[0]  
    except Exception as e:
        print(e)
    return full_conv

def get_full_conv():
    db_path = os.path.abspath('db/helpdesk_assistant.db')
    full_conv=""
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT conversation FROM conv order by time;")
        rows = cursor.fetchall()
        print(type(rows))

        for row in rows:
            full_conv+= row[0]  
    except Exception as e:
        print(e)
    return full_conv

def update_chat(intent,summary,sentiment,suggestion,status):
    db_path = os.path.abspath('db/helpdesk_assistant.db')

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()  # Create a cursor object

        #one more query to select and retrieve title and create_ts
        ts=datetime.datetime.now()
        # SQL INSERT statement
        query = """
        INSERT INTO chat_update (intent,summary,sentiment,suggestion,status,time)
        VALUES (?,?,?,?,?,?)
        """
        # Execute the INSERT statement with parameters
        cursor.execute(query, (intent,summary,sentiment,suggestion,status,ts))
        print("Values updated succesfully in chat table")
        # Commit the changes
        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")

    finally:
        if conn:
            conn.close()

def get_sentiment_values():
    db_path = os.path.abspath('db/helpdesk_assistant.db')
    sentiments=[0,]
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("SELECT sentiment FROM chat_update;")
        rows = cursor.fetchall()
        for row in rows:
            sentiments.append(row[0])  
        print(sentiments)
    except Exception as e:
        print(e)
        return []
    return sentiments

def get_chat_details():
    db_path = os.path.abspath('db/helpdesk_assistant.db')
    summary=""
    suggestion=""
    sentiment=[]
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()  # Create a cursor object

        #one more query to select and retrieve title and create_ts
        cursor.execute("SELECT summary,suggestion FROM chat_update order by time desc limit 1")
        rows = cursor.fetchall()
        # SQL INSERT statement
        if rows:
            summary=rows[0][0]
            suggestion=rows[0][1]
            sentiment=get_sentiment_values()

        conn.commit()

    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return "","",[]
    
    return summary,suggestion,sentiment

def clear_db(table_name):
    db_path = os.path.abspath('db/helpdesk_assistant.db')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = f"""
        Delete from {table_name}
        """

        # Execute the INSERT statement with parameters
        cursor.execute(query)

        # Commit the changes
        conn.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

# clear_db("sessions")
# clear_db("tickets")