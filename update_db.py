import sqlite3

conn = sqlite3.connect("student_schedule.db")

cursor = conn.cursor()

try:
    cursor.execute(
        "ALTER TABLE assignments ADD COLUMN priority TEXT"
    )

    print("Priority Column Added")

except:
    print("Column Already Exists")

conn.commit()
conn.close()