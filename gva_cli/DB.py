import sqlite3

conn= sqlite3.connect('index.db')
cursor= conn.cursor()

cursor.execute("SELECT * FROM Hash")

rows= cursor.fetchall()

for path, hash in rows:    
    print(hash)