import sqlite3

conn = sqlite3.connect("nifty100.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("=" * 50)
print("Tables in Database")
print("=" * 50)

for table in tables:
    print(table[0])

conn.close()