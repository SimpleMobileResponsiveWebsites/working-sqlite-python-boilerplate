import streamlit as st
import sqlite3

# Function to create a connection to the SQLite database
def create_connection():
    conn = sqlite3.connect('database.db')
    return conn

# Function to create a table in the database if it doesn't exist
def create_table():
    conn = create_connection()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a new record to the database
def add_record(name):
    conn = create_connection()
    c = conn.cursor()
    c.execute('INSERT INTO records (name) VALUES (?)', (name,))
    conn.commit()
    conn.close()

# Function to get all records from the database
def get_records():
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM records')
    records = c.fetchall()
    conn.close()
    return records

# Create the database and table when the app starts
create_table()

# Streamlit app layout
st.title('SQLite and Streamlit Example')

# Input for new record
name = st.text_input("Enter name:")
if st.button("Add Record"):
    if name:
        add_record(name)
        st.success(f"Record '{name}' added!")
    else:
        st.error("Please enter a name!")

# Display records
st.subheader('Records:')
records = get_records()
if records:
    for record in records:
        st.write(f"{record[0]}: {record[1]}")
else:
    st.write("No records found.")
