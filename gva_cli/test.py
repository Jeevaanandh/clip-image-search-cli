import os
import sqlite3

path= "/Users/JeevaanandhIlayaraja/Desktop/Wallpapers"

conn= sqlite3.connect("embeddings.db")
cursor= conn.cursor()

lst= cursor.execute("SELECT name FROM Embeddings;").fetchall()

for f in lst:
    print(f)