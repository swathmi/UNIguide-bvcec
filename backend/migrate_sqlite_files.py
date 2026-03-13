import os
import sqlite3

candidates = [
    os.path.join(os.path.dirname(__file__), 'db.sqlite3'),
    os.path.join(os.path.dirname(__file__), 'uniguide_users.db'),
    os.path.join(os.getcwd(), 'uniguide_users.db'),
    os.path.join(os.getcwd(), 'db.sqlite3'),
]

for path in candidates:
    if not os.path.exists(path):
        continue
    print('Checking', path)
    conn = sqlite3.connect(path)
    cur = conn.cursor()
    try:
        cur.execute("ALTER TABLE user ADD COLUMN reset_token VARCHAR(255);")
        print('Added reset_token to', path)
    except Exception as e:
        print('reset_token:', e)
    try:
        cur.execute("ALTER TABLE user ADD COLUMN reset_token_expiry DATETIME;")
        print('Added reset_token_expiry to', path)
    except Exception as e:
        print('reset_token_expiry:', e)
    conn.commit()
    conn.close()
print('Migration script finished')
