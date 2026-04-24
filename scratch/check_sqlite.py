import sqlite3
import os

db_path = r'c:\Users\johns\Videos\Projects\Pro\db.sqlite3'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Check if table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='pages_service';")
    if cursor.fetchone():
        print("--- SERVICES IN LOCAL SQLITE ---")
        cursor.execute("SELECT id, title, is_active FROM pages_service;")
        rows = cursor.fetchall()
        print(f"Total: {len(rows)}")
        for row in rows:
            print(f"ID: {row[0]} | Title: {row[1]} | Active: {row[2]}")
    else:
        print("Table pages_service not found in SQLite")
    conn.close()
else:
    print("SQLite DB not found")
