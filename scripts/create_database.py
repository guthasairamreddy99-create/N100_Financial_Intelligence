import sqlite3

conn = sqlite3.connect("nifty100.db")

with open("db/schema.sql", "r") as f:
    conn.executescript(f.read())

conn.commit()
conn.close()

print("=" * 50)
print("SQLite Database Created Successfully")
print("Database : nifty100.db")
print("=" * 50)