import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="testdb",
    user="myuser",
    password="MyPass2026!"
)

cursor = conn.cursor()
cursor.execute("SELECT * FROM employees")

for row in cursor.fetchall():
    print(row)

cursor.close()
conn.close()