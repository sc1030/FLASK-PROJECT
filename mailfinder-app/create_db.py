import sqlite3

# Connect to SQLite database (this will create it if it doesn't exist)
conn = sqlite3.connect('mailfinder.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    email TEXT NOT NULL
)
''')

# Sample user data
users = [
    ("John Doe", "john.doe@example.com"),
    ("Jane Smith", "jane.smith@example.com"),
    ("Alice Johnson", "alice.johnson@example.com"),
    ("Johnny Deep", "deep.johnny@example.com")
]

# Insert sample data
cursor.executemany('INSERT INTO users (full_name, email) VALUES (?, ?)', users)

# Save and close
conn.commit()
conn.close()

print("Database created and seeded successfully!")
