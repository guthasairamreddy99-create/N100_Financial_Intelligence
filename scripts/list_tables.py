import sqlite3

conn = sqlite3.connect("nifty100.db")

cursor = conn.execute("""
SELECT name
FROM sqlite_master
WHERE type='table'
ORDER BY name
""")

print("\nTables in Database:\n")

for row in cursor:
    print(row[0])

conn.close()