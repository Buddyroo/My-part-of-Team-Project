import sqlite3

conn = sqlite3.connect('easy_habit.db')
cur = conn.cursor()

cur.execute('''ALTER TABLE users RENAME TO user''')

conn.commit()
conn.close()

