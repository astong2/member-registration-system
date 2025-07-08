import sqlite3 # imports python's built-in SQLite library

conn = sqlite3.connect('members.db') # This creates a file named members.db 
c = conn.cursor() # a cursor is an object that allows you to execute SQL commands

c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    username TEXT NOT NULL,
    email TEXT NOT NULL, 
    password TEXT NOT NULL
    )
''')

conn.commit() # This saves the changes to the database
conn.close() # This closes the connection to the database, like hanging up a phone call