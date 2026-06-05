import sqlite3

# CONNECT DATABASE
conn = sqlite3.connect("student_schedule.db")

# CURSOR
cursor = conn.cursor()

# EVENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS events(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    date TEXT,
    time TEXT
)
""")

# ASSIGNMENTS TABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    subject TEXT,
    deadline TEXT,
    priority TEXT
)
""")

print("Database Tables Created Successfully")

# SAVE
conn.commit()

# CLOSE
conn.close()