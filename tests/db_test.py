import sqlite3

conn = sqlite3.connect('game.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    activate BOOLEAN NOT NULL,
    description TEXT,
    drop INTEGER,
    type TEXT,
    state INTEGER,
    user_choices TEXT
)
''')

conn.commit()

conn.close()