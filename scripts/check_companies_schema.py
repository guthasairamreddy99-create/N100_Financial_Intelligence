import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.execute("PRAGMA table_info(companies)")

print("Companies table schema:\n")

for row in cursor:
    print(row)

conn.close()